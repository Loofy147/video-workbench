#!/usr/bin/env python3
"""Run a local-only Video Workbench browser workflow using the standard library."""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import sys
import threading
import uuid
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from video_workbench.render import RenderError, render_campaign  # noqa: E402

WEB_ROOT = ROOT / "web"
PROJECTS_ROOT = ROOT / ".workbench" / "projects"
MAX_REQUEST_BYTES = 1_000_000
MAX_SCENES = 8
MAX_SCENE_SECONDS = 20.0
MAX_TOTAL_SECONDS = 90.0
PROJECT_ID_PATTERN = re.compile(r"^[0-9a-f]{32}$")
HEX_COLOR_PATTERN = re.compile(r"^#[0-9a-fA-F]{6}$")
WATERMARK_TEXT = "INTERNAL REVIEW DRAFT - NOT FOR PUBLICATION"
DEFAULT_SCENES = [
    {
        "title": "Start with the business outcome",
        "body": "Define the audience, problem, and objective before choosing the format.",
        "duration_seconds": 3,
        "background": "#101b2d",
    },
    {
        "title": "Make the offering clear",
        "body": "Brief, storyboard, draft video, and source-aware review in one workflow.",
        "duration_seconds": 3,
        "background": "#18394b",
    },
    {
        "title": "Review before publication",
        "body": "Verify claims, media rights, brand use, and approval before release.",
        "duration_seconds": 3,
        "background": "#26364b",
    },
]

_LOCKS_GUARD = threading.Lock()
_PROJECT_LOCKS: dict[str, threading.RLock] = {}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def project_lock(project_id: str) -> threading.RLock:
    with _LOCKS_GUARD:
        return _PROJECT_LOCKS.setdefault(project_id, threading.RLock())


def _text(value: Any, label: str, *, required: bool = True, limit: int = 2_000) -> str:
    if value is None and not required:
        return ""
    if not isinstance(value, str):
        raise ValueError(f"{label} must be text.")
    value = value.strip()
    if "\x00" in value:
        raise ValueError(f"{label} contains an invalid null character.")
    if required and not value:
        raise ValueError(f"{label} is required.")
    if len(value) > limit:
        raise ValueError(f"{label} must be at most {limit} characters.")
    return value


def normalize_plan(payload: Any) -> dict[str, Any]:
    """Validate and normalize browser input into a deliberately narrow card-only contract."""
    if not isinstance(payload, dict):
        raise ValueError("Request body must be a JSON object.")
    plan = {
        "project_title": _text(payload.get("project_title"), "Project title", limit=160),
        "offering": _text(payload.get("offering"), "Offering", limit=2_000),
        "audience": _text(payload.get("audience"), "Audience", limit=1_000),
        "objective": _text(payload.get("objective"), "Objective", limit=1_000),
        "differentiators": _text(payload.get("differentiators", ""), "Differentiators", required=False, limit=2_000),
        "call_to_action": _text(payload.get("call_to_action"), "Call to action", limit=500),
        "scenes": [],
    }
    raw_claims = payload.get("claims_evidence", [])
    if not isinstance(raw_claims, list) or len(raw_claims) > 30:
        raise ValueError("Claims and evidence must be a list with at most 30 entries.")
    allowed_claim_statuses = {"documented-source", "direct-observation", "inference", "unverified"}
    claims: list[dict[str, str | None]] = []
    for index, raw_claim in enumerate(raw_claims, start=1):
        label = f"Claim {index}"
        if not isinstance(raw_claim, dict):
            raise ValueError(f"{label} must be an object.")
        claim_text = _text(raw_claim.get("claim"), f"{label} text", limit=600)
        status = raw_claim.get("status")
        if status not in allowed_claim_statuses:
            raise ValueError(f"{label} status must be one of {sorted(allowed_claim_statuses)}.")
        evidence = _text(raw_claim.get("evidence", ""), f"{label} evidence", required=False, limit=1_000)
        if status in {"documented-source", "direct-observation"} and not evidence:
            raise ValueError(f"{label} needs an evidence URL or observation note for status {status}.")
        claims.append({"claim": claim_text, "status": status, "evidence": evidence or None})
    plan["claims_evidence"] = claims

    raw_scenes = payload.get("scenes")
    if not isinstance(raw_scenes, list) or not 1 <= len(raw_scenes) <= MAX_SCENES:
        raise ValueError(f"Storyboard must contain between 1 and {MAX_SCENES} scenes.")
    total_duration = 0.0
    for index, raw in enumerate(raw_scenes, start=1):
        label = f"Scene {index}"
        if not isinstance(raw, dict):
            raise ValueError(f"{label} must be an object.")
        title = _text(raw.get("title"), f"{label} title", limit=180)
        body = _text(raw.get("body", ""), f"{label} body", required=False, limit=900)
        raw_duration = raw.get("duration_seconds", 3)
        if isinstance(raw_duration, bool):
            raise ValueError(f"{label} duration must be a number.")
        try:
            duration = float(raw_duration)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"{label} duration must be a number.") from exc
        if not math.isfinite(duration) or duration < 1 or duration > MAX_SCENE_SECONDS:
            raise ValueError(f"{label} duration must be between 1 and {MAX_SCENE_SECONDS:g} seconds.")
        color = raw.get("background", "#101b2d")
        if not isinstance(color, str) or not HEX_COLOR_PATTERN.fullmatch(color):
            raise ValueError(f"{label} background must be a six-digit hex color such as #101b2d.")
        total_duration += duration
        plan["scenes"].append({
            "title": title,
            "body": body,
            "duration_seconds": duration,
            "background": color.lower(),
        })
    if total_duration > MAX_TOTAL_SECONDS:
        raise ValueError(f"Storyboard duration must not exceed {MAX_TOTAL_SECONDS:g} seconds.")
    return plan


def build_campaign(plan: dict[str, Any], project_id: str, version: int) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "project": {"id": project_id, "title": plan["project_title"]},
        "output": {
            "path": f"outputs/draft-v{version}.mp4",
            "width": 1280,
            "height": 720,
            "fps": 30,
            "watermark_text": WATERMARK_TEXT,
        },
        "scenes": [
            {
                "id": f"scene-{index:02d}",
                "kind": "card",
                "duration_seconds": scene["duration_seconds"],
                "title": scene["title"],
                "body": scene["body"],
                "background": scene["background"],
            }
            for index, scene in enumerate(plan["scenes"], start=1)
        ],
        "claims_evidence": plan["claims_evidence"],
        "approval": {"status": "draft"},
        "claims_evidence": [],
    }


def build_brief(plan: dict[str, Any], version: int) -> str:
    lines = [
        f"# Campaign brief: {plan['project_title']}",
        "",
        f"_Saved version: {version}. State: internal review draft._",
        "",
        "## Offering",
        plan["offering"],
        "",
        "## Target audience",
        plan["audience"],
        "",
        "## Objective",
        plan["objective"],
        "",
        "## Differentiators",
        plan["differentiators"] or "Not specified yet.",
        "",
        "## Call to action",
        plan["call_to_action"],
        "",
        "## Claims and evidence ledger",
    ]
    if plan["claims_evidence"]:
        for item in plan["claims_evidence"]:
            evidence = item["evidence"] or "No evidence reference supplied."
            lines.append(f"- {item['claim']} — status: {item['status']}; reference/note: {evidence}")
    else:
        lines.append("No claims have been explicitly tracked yet. Review factual statements in the storyboard separately.")
    lines.extend([
        "",
        "This ledger records owner-entered evidence references or observation notes. The application does not open or independently verify references and does not establish claim truth.",
        "",
        "## Storyboard",
    ]
    for index, scene in enumerate(plan["scenes"], start=1):
        lines.extend([
            "",
            f"### Scene {index}: {scene['title']}",
            f"Duration: {scene['duration_seconds']:g} seconds",
            f"Background: {scene['background']}",
            "",
            scene["body"] or "No body copy supplied.",
        ])
    lines.extend([
        "",
        "## Review checklist — required before any publication",
        "- Verify every factual/product claim against current source evidence.",
        "- Confirm permission and license for every image, clip, font, logo, and audio asset.",
        "- Check audience, brand, spelling, accessibility, and call-to-action destination.",
        "- Obtain approval from an authorized reviewer outside this local draft form.",
        "- Keep the watermark on draft exports; a successful render is not publication approval.",
        "",
        "## Status and limitations",
        "This brief is user-entered planning content. The app does not independently verify claims, ownership, legal rights, or product behavior.",
        "",
    ])
    return "\n".join(lines)


def _project_dir(project_id: str) -> Path:
    if not isinstance(project_id, str) or not PROJECT_ID_PATTERN.fullmatch(project_id):
        raise ValueError("Invalid project identifier.")
    return PROJECTS_ROOT / project_id


def _write_atomic(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp-" + uuid.uuid4().hex)
    try:
        temporary.write_text(content, encoding="utf-8")
        os.replace(temporary, path)
    finally:
        try:
            temporary.unlink(missing_ok=True)
        except OSError:
            pass


def _write_json(path: Path, value: Any) -> None:
    _write_atomic(path, json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def _read_record(project_id: str) -> dict[str, Any]:
    path = _project_dir(project_id) / "project.json"
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise KeyError("Project not found.") from exc
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RuntimeError("Saved project record could not be read.") from exc
    if not isinstance(raw, dict) or raw.get("id") != project_id:
        raise RuntimeError("Saved project record is invalid.")
    return raw


def _store_plan(project_dir: Path, plan: dict[str, Any], project_id: str, version: int) -> None:
    _write_atomic(project_dir / f"brief-v{version}.md", build_brief(plan, version))
    _write_json(project_dir / f"campaign-v{version}.json", build_campaign(plan, project_id, version))


def _render_public_summary(result: dict[str, Any] | None) -> dict[str, Any] | None:
    if not result:
        return None
    output = result.get("output", {})
    return {
        "rendered_at_utc": result.get("rendered_at_utc"),
        "output": {
            "sha256": output.get("sha256"),
            "bytes": output.get("bytes"),
            "container": output.get("container"),
            "video_codec": output.get("video_codec"),
            "audio_codec": output.get("audio_codec"),
            "width": output.get("width"),
            "height": output.get("height"),
            "fps": output.get("fps"),
            "duration_seconds": output.get("duration_seconds"),
            "expected_frame_count": output.get("expected_frame_count"),
        },
        "validation": result.get("validation"),
        "release_gate": result.get("release_gate"),
        "renderer": result.get("renderer"),
    }


def _public_project(record: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": record["id"],
        "title": record["title"],
        "version": record["version"],
        "state": record["state"],
        "created_at": record["created_at"],
        "updated_at": record["updated_at"],
        "render_error": record.get("render_error"),
        "render": _render_public_summary(record.get("render_result")),
    }


def create_project(payload: Any) -> dict[str, Any]:
    plan = normalize_plan(payload)
    project_id = uuid.uuid4().hex
    PROJECTS_ROOT.mkdir(parents=True, exist_ok=True)
    project_dir = _project_dir(project_id)
    project_dir.mkdir(parents=True, mode=0o700, exist_ok=False)
    try:
        try:
            os.chmod(project_dir, 0o700)
        except OSError:
            pass
        now = utc_now()
        _store_plan(project_dir, plan, project_id, 1)
        record = {
            "schema_version": 1,
            "id": project_id,
            "title": plan["project_title"],
            "created_at": now,
            "updated_at": now,
            "version": 1,
            "state": "draft",
            "plan": plan,
            "render_result": None,
            "render_error": None,
            "versions": [{"version": 1, "saved_at": now, "render": None}],
        }
        _write_json(project_dir / "project.json", record)
        try:
            os.chmod(project_dir / "project.json", 0o600)
        except OSError:
            pass
        return {"project": _public_project(record), "plan": plan}
    except Exception:
        import shutil
        shutil.rmtree(project_dir, ignore_errors=True)
        raise


def update_project(project_id: str, payload: Any) -> dict[str, Any]:
    plan = normalize_plan(payload)
    lock = project_lock(project_id)
    with lock:
        record = _read_record(project_id)
        if record.get("state") == "rendering":
            raise RuntimeError("This project is rendering; wait for that render to finish before saving edits.")
        version = int(record["version"]) + 1
        project_dir = _project_dir(project_id)
        now = utc_now()
        _store_plan(project_dir, plan, project_id, version)
        record.update({
            "title": plan["project_title"],
            "updated_at": now,
            "version": version,
            "state": "draft",
            "plan": plan,
            "render_result": None,
            "render_error": None,
        })
        record.setdefault("versions", []).append({"version": version, "saved_at": now, "render": None})
        _write_json(project_dir / "project.json", record)
        return {"project": _public_project(record), "plan": plan}


def list_projects() -> list[dict[str, Any]]:
    PROJECTS_ROOT.mkdir(parents=True, exist_ok=True)
    projects: list[dict[str, Any]] = []
    for directory in PROJECTS_ROOT.iterdir():
        if not directory.is_dir() or not PROJECT_ID_PATTERN.fullmatch(directory.name):
            continue
        try:
            projects.append(_public_project(_read_record(directory.name)))
        except (KeyError, RuntimeError, OSError, ValueError):
            continue
    return sorted(projects, key=lambda item: item["updated_at"], reverse=True)


def get_project(project_id: str) -> dict[str, Any]:
    record = _read_record(project_id)
    return {
        "project": _public_project(record),
        "plan": record["plan"],
        "version_history": record.get("versions", []),
    }


def render_project(project_id: str) -> dict[str, Any]:
    with project_lock(project_id):
        record = _read_record(project_id)
        if record.get("state") == "rendering":
            raise RuntimeError("This project is already rendering.")
        version = int(record["version"])
        project_dir = _project_dir(project_id)
        if record.get("state") == "rendered_draft" and record.get("render_result"):
            raise RuntimeError("This version has already been rendered. Save edits to create a new version before rendering again.")
        campaign_path = project_dir / f"campaign-v{version}.json"
        if not campaign_path.is_file():
            raise RuntimeError("The saved campaign manifest for this version is missing.")
        record["state"] = "rendering"
        record["updated_at"] = utc_now()
        record["render_error"] = None
        _write_json(project_dir / "project.json", record)
        try:
            result = render_campaign(campaign_path)
        except (RenderError, OSError, ValueError, RuntimeError) as exc:
            record["state"] = "render_failed"
            record["render_error"] = str(exc)[:1_000]
            record["updated_at"] = utc_now()
            _write_json(project_dir / "project.json", record)
            raise RenderError(str(exc)) from exc
        summary = _render_public_summary(result)
        record["state"] = "rendered_draft"
        record["updated_at"] = utc_now()
        record["render_result"] = summary
        record["render_error"] = None
        for item in record.get("versions", []):
            if item.get("version") == version:
                item["render"] = summary
                break
        _write_json(project_dir / "project.json", record)
        return {"project": _public_project(record), "render": summary}


def origin_allowed(origin: str | None, port: int) -> bool:
    if not origin:
        return True
    parsed = urlsplit(origin)
    return parsed.scheme == "http" and parsed.netloc.lower() in {
        f"127.0.0.1:{port}", f"localhost:{port}"
    } and parsed.path == "" and not parsed.query and not parsed.fragment


class WorkbenchHandler(BaseHTTPRequestHandler):
    server_version = "VideoWorkbenchLocal/0.1"
    sys_version = ""

    def log_message(self, _format: str, *_args: Any) -> None:
        # Do not log request bodies or user-entered campaign copy.
        return

    def _security_headers(self) -> None:
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Cross-Origin-Resource-Policy", "same-origin")
        self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; media-src 'self'; img-src 'self' data:; object-src 'none'; base-uri 'none'; frame-ancestors 'none'; form-action 'self'")

    def _send_bytes(self, status: int, body: bytes, content_type: str = "application/json; charset=utf-8") -> None:
        self.send_response(status)
        self._security_headers()
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _json(self, status: int, value: Any) -> None:
        body = (json.dumps(value, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")
        self._send_bytes(status, body)

    def _check_host(self) -> bool:
        allowed = {
            f"127.0.0.1:{self.server.server_port}",
            f"localhost:{self.server.server_port}",
        }
        if self.headers.get("Host", "").lower() in allowed:
            return True
        self._json(HTTPStatus.MISDIRECTED_REQUEST, {"error": "Only the local workbench host is accepted."})
        return False

    def _check_origin(self) -> bool:
        if origin_allowed(self.headers.get("Origin"), self.server.server_port):
            return True
        self._json(HTTPStatus.FORBIDDEN, {"error": "Cross-origin requests are not allowed."})
        return False

    def _read_json_body(self) -> Any:
        content_type = self.headers.get("Content-Type", "").split(";", 1)[0].strip().lower()
        if content_type != "application/json":
            raise ValueError("Content-Type must be application/json.")
        raw_length = self.headers.get("Content-Length")
        if not raw_length or not raw_length.isdigit():
            raise ValueError("A valid Content-Length header is required.")
        size = int(raw_length)
        if size < 1 or size > MAX_REQUEST_BYTES:
            raise ValueError(f"Request body must be between 1 and {MAX_REQUEST_BYTES:,} bytes.")
        raw = self.rfile.read(size)
        try:
            return json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ValueError("Request body must be valid UTF-8 JSON.") from exc

    def _artifact_file(self, project_id: str, name: str) -> tuple[Path, str, str, bool] | None:
        record = _read_record(project_id)
        version = int(record["version"])
        project_dir = _project_dir(project_id)
        choices: dict[str, tuple[Path, str, str, bool]] = {
            "brief": (project_dir / f"brief-v{version}.md", "text/markdown; charset=utf-8", f"brief-v{version}.md", False),
            "campaign": (project_dir / f"campaign-v{version}.json", "application/json; charset=utf-8", f"campaign-v{version}.json", False),
            "video": (project_dir / "outputs" / f"draft-v{version}.mp4", "video/mp4", f"draft-v{version}.mp4", True),
            "provenance": (project_dir / "outputs" / f"draft-v{version}.mp4.manifest.json", "application/json; charset=utf-8", f"draft-v{version}.mp4.manifest.json", False),
        }
        return choices.get(name)

    def _send_file(self, path: Path, content_type: str, filename: str, *, inline: bool) -> None:
        try:
            size = path.stat().st_size
            stream = path.open("rb")
        except FileNotFoundError:
            self._json(HTTPStatus.NOT_FOUND, {"error": "That artifact has not been generated for the current version."})
            return
        except OSError:
            self._json(HTTPStatus.INTERNAL_SERVER_ERROR, {"error": "The local artifact could not be read."})
            return
        with stream:
            start, end, status = 0, size - 1, HTTPStatus.OK
            range_header = self.headers.get("Range") if content_type == "video/mp4" else None
            if range_header:
                match = re.fullmatch(r"bytes=(\d*)-(\d*)", range_header.strip())
                if not match or (not match.group(1) and not match.group(2)):
                    self.send_response(HTTPStatus.REQUESTED_RANGE_NOT_SATISFIABLE)
                    self._security_headers()
                    self.send_header("Content-Range", f"bytes */{size}")
                    self.send_header("Content-Length", "0")
                    self.end_headers()
                    return
                if not match.group(1):
                    suffix = int(match.group(2))
                    if suffix <= 0:
                        start = size
                    else:
                        start = max(0, size - suffix)
                else:
                    start = int(match.group(1))
                    end = int(match.group(2)) if match.group(2) else size - 1
                if start >= size or end < start:
                    self.send_response(HTTPStatus.REQUESTED_RANGE_NOT_SATISFIABLE)
                    self._security_headers()
                    self.send_header("Content-Range", f"bytes */{size}")
                    self.send_header("Content-Length", "0")
                    self.end_headers()
                    return
                end = min(end, size - 1)
                status = HTTPStatus.PARTIAL_CONTENT
            length = max(0, end - start + 1)
            self.send_response(status)
            self._security_headers()
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(length))
            self.send_header("Content-Disposition", f"{'inline' if inline else 'attachment'}; filename=\"{filename}\"")
            if content_type == "video/mp4":
                self.send_header("Accept-Ranges", "bytes")
                if status == HTTPStatus.PARTIAL_CONTENT:
                    self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
            self.end_headers()
            stream.seek(start)
            remaining = length
            while remaining:
                chunk = stream.read(min(64 * 1024, remaining))
                if not chunk:
                    break
                self.wfile.write(chunk)
                remaining -= len(chunk)

    def do_GET(self) -> None:  # noqa: N802
        if not self._check_host():
            return
        path = urlsplit(self.path).path
        if path == "/":
            target = WEB_ROOT / "index.html"
            content_type = "text/html; charset=utf-8"
        elif path == "/assets/app.js":
            target = WEB_ROOT / "app.js"
            content_type = "text/javascript; charset=utf-8"
        elif path == "/assets/styles.css":
            target = WEB_ROOT / "styles.css"
            content_type = "text/css; charset=utf-8"
        else:
            target = None
            content_type = ""
        if target is not None:
            try:
                body = target.read_bytes()
            except OSError:
                self._json(HTTPStatus.INTERNAL_SERVER_ERROR, {"error": "The local interface asset could not be read."})
                return
            self._send_bytes(HTTPStatus.OK, body, content_type)
            return
        if path == "/api/projects":
            self._json(HTTPStatus.OK, {"projects": list_projects()})
            return
        match = re.fullmatch(r"/api/projects/([0-9a-f]{32})", path)
        if match:
            try:
                self._json(HTTPStatus.OK, get_project(match.group(1)))
            except KeyError:
                self._json(HTTPStatus.NOT_FOUND, {"error": "Project not found."})
            except (RuntimeError, ValueError):
                self._json(HTTPStatus.INTERNAL_SERVER_ERROR, {"error": "Saved project data is invalid."})
            return
        artifact_match = re.fullmatch(r"/api/projects/([0-9a-f]{32})/files/(brief|campaign|video|provenance)", path)
        if artifact_match:
            try:
                artifact = self._artifact_file(artifact_match.group(1), artifact_match.group(2))
            except KeyError:
                self._json(HTTPStatus.NOT_FOUND, {"error": "Project not found."})
                return
            except (RuntimeError, ValueError):
                self._json(HTTPStatus.INTERNAL_SERVER_ERROR, {"error": "Saved project data is invalid."})
                return
            if not artifact:
                self._json(HTTPStatus.NOT_FOUND, {"error": "Artifact not found."})
                return
            self._send_file(artifact[0], artifact[1], artifact[2], inline=artifact[3])
            return
        self._json(HTTPStatus.NOT_FOUND, {"error": "Route not found."})

    def do_POST(self) -> None:  # noqa: N802
        if not self._check_host() or not self._check_origin():
            return
        try:
            payload = self._read_json_body()
        except ValueError as exc:
            self._json(HTTPStatus.BAD_REQUEST, {"error": str(exc)})
            return
        path = urlsplit(self.path).path
        if path == "/api/projects":
            try:
                created = create_project(payload)
            except ValueError as exc:
                self._json(HTTPStatus.BAD_REQUEST, {"error": str(exc)})
            except OSError:
                self._json(HTTPStatus.INTERNAL_SERVER_ERROR, {"error": "The local project could not be saved."})
            else:
                self._json(HTTPStatus.CREATED, created)
            return
        render_match = re.fullmatch(r"/api/projects/([0-9a-f]{32})/render", path)
        if render_match:
            try:
                result = render_project(render_match.group(1))
            except KeyError:
                self._json(HTTPStatus.NOT_FOUND, {"error": "Project not found."})
            except (ValueError, RuntimeError) as exc:
                self._json(HTTPStatus.CONFLICT, {"error": str(exc)})
            except RenderError as exc:
                self._json(HTTPStatus.UNPROCESSABLE_ENTITY, {"error": str(exc)})
            except OSError:
                self._json(HTTPStatus.INTERNAL_SERVER_ERROR, {"error": "The local render failed because a filesystem operation failed."})
            else:
                self._json(HTTPStatus.OK, result)
            return
        self._json(HTTPStatus.NOT_FOUND, {"error": "Route not found."})

    def do_PUT(self) -> None:  # noqa: N802
        if not self._check_host() or not self._check_origin():
            return
        try:
            payload = self._read_json_body()
        except ValueError as exc:
            self._json(HTTPStatus.BAD_REQUEST, {"error": str(exc)})
            return
        match = re.fullmatch(r"/api/projects/([0-9a-f]{32})", urlsplit(self.path).path)
        if not match:
            self._json(HTTPStatus.NOT_FOUND, {"error": "Route not found."})
            return
        try:
            saved = update_project(match.group(1), payload)
        except KeyError:
            self._json(HTTPStatus.NOT_FOUND, {"error": "Project not found."})
        except ValueError as exc:
            self._json(HTTPStatus.BAD_REQUEST, {"error": str(exc)})
        except RuntimeError as exc:
            self._json(HTTPStatus.CONFLICT, {"error": str(exc)})
        except OSError:
            self._json(HTTPStatus.INTERNAL_SERVER_ERROR, {"error": "The local project could not be saved."})
        else:
            self._json(HTTPStatus.OK, saved)


class LocalWorkbenchServer(ThreadingHTTPServer):
    daemon_threads = True
    allow_reuse_address = True


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the local-only Video Workbench browser UI.")
    parser.add_argument("--port", type=int, default=8765, help="Loopback HTTP port (default: 8765).")
    args = parser.parse_args(argv)
    if not 1024 <= args.port <= 65535:
        parser.error("--port must be between 1024 and 65535.")
    try:
        PROJECTS_ROOT.mkdir(parents=True, exist_ok=True)
        try:
            os.chmod(PROJECTS_ROOT.parent, 0o700)
            os.chmod(PROJECTS_ROOT, 0o700)
        except OSError:
            pass
        server = LocalWorkbenchServer(("127.0.0.1", args.port), WorkbenchHandler)
    except OSError as exc:
        print(f"Could not start local workbench: {exc}", file=sys.stderr)
        return 2
    print("Video Workbench local UI is listening at http://127.0.0.1:%d/" % server.server_port)
    print("Local-only server. Keep this terminal open; press Ctrl+C to stop.")
    print("Project records, briefs, manifests, and videos are stored in ignored .workbench/projects/.")
    try:
        server.serve_forever(poll_interval=0.5)
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
