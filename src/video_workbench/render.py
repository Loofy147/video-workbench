"""Render a campaign manifest into a validated MP4 using local FFmpeg.

The renderer uses Python's standard library plus an installed FFmpeg/FFprobe
build. It does not download models, call APIs, or claim synthetic title cards
are real product footage.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

RENDERER_VERSION = "0.1.0"
SUPPORTED_FPS = {24, 25, 30, 50, 60}
MAX_SCENES = 24
MAX_SCENE_SECONDS = 90.0
MAX_TOTAL_SECONDS = 300.0
MAX_DIMENSION = 3840
MAX_PIXELS = 8_294_400
HEX_COLOR = re.compile(r"^#?[0-9a-fA-F]{6}$")
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}
VIDEO_EXTENSIONS = {".mp4", ".mov", ".mkv", ".webm"}
AUDIO_EXTENSIONS = {".wav", ".mp3", ".m4a", ".aac", ".ogg", ".flac"}


class RenderError(Exception):
    """Expected render or validation failure suitable for an operator."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _require_text(value: Any, label: str, *, optional: bool = False, limit: int = 1200) -> str:
    if value is None and optional:
        return ""
    if not isinstance(value, str):
        raise RenderError(f"{label} must be a string.")
    value = value.strip()
    if not value and not optional:
        raise RenderError(f"{label} cannot be empty.")
    if len(value) > limit:
        raise RenderError(f"{label} is longer than the allowed {limit} characters.")
    return value


def _safe_project_file(project_root: Path, value: Any, label: str, allowed_extensions: set[str]) -> Path:
    relative = _require_text(value, label)
    candidate = (project_root / relative).resolve()
    try:
        candidate.relative_to(project_root.resolve())
    except ValueError as exc:
        raise RenderError(f"{label} must stay inside the campaign directory: {relative}") from exc
    if not candidate.is_file():
        raise RenderError(f"{label} does not exist or is not a file: {relative}")
    if candidate.suffix.lower() not in allowed_extensions:
        raise RenderError(f"{label} has an unsupported extension: {candidate.suffix or '(none)'}")
    if candidate.stat().st_size > 2 * 1024 * 1024 * 1024:
        raise RenderError(f"{label} exceeds the 2 GiB per-source limit.")
    return candidate


def _parse_provenance(raw: Any, label: str) -> dict[str, Any]:
    if not isinstance(raw, dict):
        raise RenderError(f"{label}.provenance is required for sourced media and must be an object.")
    origin = _require_text(raw.get("origin"), f"{label}.provenance.origin", limit=500)
    rights_status = raw.get("rights_status")
    allowed = {"owner_created", "licensed", "permission_confirmed", "public_domain", "unverified"}
    if rights_status not in allowed:
        raise RenderError(f"{label}.provenance.rights_status must be one of {sorted(allowed)}.")
    evidence = _require_text(raw.get("evidence", ""), f"{label}.provenance.evidence", optional=True, limit=1000)
    if rights_status in {"licensed", "permission_confirmed", "public_domain"} and not evidence:
        raise RenderError(f"{label}.provenance.evidence is required when rights_status is {rights_status}.")
    return {
        "origin": origin, "rights_status": rights_status, "evidence": evidence or None,
        "reviewed_by": _require_text(raw.get("reviewed_by", ""), f"{label}.provenance.reviewed_by", optional=True, limit=200) or None,
        "reviewed_at": _require_text(raw.get("reviewed_at", ""), f"{label}.provenance.reviewed_at", optional=True, limit=80) or None,
    }


def _parse_claim_evidence(raw: Any) -> list[dict[str, str | None]]:
    if raw is None:
        return []
    if not isinstance(raw, list) or len(raw) > 100:
        raise RenderError("claims_evidence must be an array with at most 100 entries.")
    allowed_statuses = {"documented-source", "direct-observation", "inference", "unverified"}
    records: list[dict[str, str | None]] = []
    for index, entry in enumerate(raw):
        label = f"claims_evidence[{index}]"
        if not isinstance(entry, dict):
            raise RenderError(f"{label} must be an object.")
        claim = _require_text(entry.get("claim"), f"{label}.claim", limit=600)
        status = entry.get("status")
        if status not in allowed_statuses:
            raise RenderError(f"{label}.status must be one of {sorted(allowed_statuses)}.")
        evidence = _require_text(entry.get("evidence", ""), f"{label}.evidence", optional=True, limit=1000)
        if status in {"documented-source", "direct-observation"} and not evidence:
            raise RenderError(f"{label}.evidence is required for status {status}.")
        records.append({"claim": claim, "status": status, "evidence": evidence or None})
    return records


def _parse_approval(raw: Any) -> dict[str, str | None]:
    if raw is None:
        raw = {"status": "draft"}
    if not isinstance(raw, dict):
        raise RenderError("approval must be an object when supplied.")
    status = raw.get("status", "draft")
    if status not in {"draft", "approved", "rejected"}:
        raise RenderError("approval.status must be draft, approved, or rejected.")
    approved_by = _require_text(raw.get("approved_by", ""), "approval.approved_by", optional=True, limit=200) or None
    approved_at = _require_text(raw.get("approved_at", ""), "approval.approved_at", optional=True, limit=80) or None
    if status == "approved":
        if not approved_by or not approved_at:
            raise RenderError("An approved campaign requires approval.approved_by and approval.approved_at.")
        try:
            parsed_date = datetime.fromisoformat(approved_at.replace("Z", "+00:00"))
        except ValueError as exc:
            raise RenderError("approval.approved_at must be an ISO-8601 timestamp.") from exc
        if parsed_date.tzinfo is None:
            raise RenderError("approval.approved_at must include a timezone.")
    return {"status": status, "approved_by": approved_by, "approved_at": approved_at}


def _release_blockers(approval: dict[str, str | None], claims: list[dict[str, str | None]], scenes: list[dict[str, Any]], audio_path: Path | None, audio_provenance: dict[str, Any] | None) -> list[str]:
    blockers: list[str] = []
    if approval.get("status") != "approved":
        blockers.append("campaign approval is not approved")
    for claim in claims:
        if claim.get("status") not in {"documented-source", "direct-observation"} or not claim.get("evidence"):
            blockers.append(f"claim lacks verified evidence: {claim.get('claim', '')}")
    for scene in scenes:
        provenance = scene.get("provenance")
        if provenance and provenance.get("rights_status") == "unverified":
            blockers.append(f"media rights are unverified for scene {scene['id']}")
    if audio_path and audio_provenance and audio_provenance.get("rights_status") == "unverified":
        blockers.append("audio rights are unverified")
    return blockers


def load_campaign(manifest_path: Path) -> tuple[dict[str, Any], Path, list[dict[str, Any]], Path | None]:
    manifest_path = manifest_path.expanduser().resolve()
    if not manifest_path.is_file():
        raise RenderError(f"Campaign manifest not found: {manifest_path}")
    try:
        raw = manifest_path.read_bytes()
        campaign = json.loads(raw.decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RenderError(f"Cannot read UTF-8 JSON campaign manifest: {exc}") from exc
    if not isinstance(campaign, dict):
        raise RenderError("Campaign manifest root must be a JSON object.")
    if campaign.get("schema_version") != 1:
        raise RenderError("schema_version must be 1.")
    project = campaign.get("project")
    if not isinstance(project, dict):
        raise RenderError("project must be an object.")
    project_id = _require_text(project.get("id"), "project.id", limit=100)
    project_title = _require_text(project.get("title"), "project.title", limit=200)
    output = campaign.get("output")
    if not isinstance(output, dict):
        raise RenderError("output must be an object.")
    try:
        width, height, fps = int(output.get("width", 1920)), int(output.get("height", 1080)), int(output.get("fps", 30))
    except (TypeError, ValueError) as exc:
        raise RenderError("output.width, output.height, and output.fps must be integers.") from exc
    if width < 320 or height < 320 or width > MAX_DIMENSION or height > MAX_DIMENSION or width * height > MAX_PIXELS:
        raise RenderError(f"Output dimensions must be at least 320x320 and no more than {MAX_PIXELS:,} pixels.")
    if width % 2 or height % 2:
        raise RenderError("Output width and height must be even for yuv420p/H.264 compatibility.")
    if fps not in SUPPORTED_FPS:
        raise RenderError(f"output.fps must be one of {sorted(SUPPORTED_FPS)}.")
    if output.get("container", "mp4") != "mp4":
        raise RenderError("Only MP4 output is currently supported.")
    watermark = _require_text(output.get("watermark_text", "INTERNAL REVIEW DRAFT"), "output.watermark_text", optional=True, limit=120)
    requested_output = _require_text(output.get("path", "dist/campaign.mp4"), "output.path", limit=500)
    relative_output = Path(requested_output)
    if relative_output.is_absolute() or ".." in relative_output.parts:
        raise RenderError("output.path must stay inside the campaign directory; use --output for an explicit external destination.")
    if relative_output.suffix.lower() != ".mp4":
        raise RenderError("output.path must end in .mp4.")

    raw_scenes = campaign.get("scenes")
    if not isinstance(raw_scenes, list) or not 1 <= len(raw_scenes) <= MAX_SCENES:
        raise RenderError(f"scenes must contain between 1 and {MAX_SCENES} scenes.")
    project_root = manifest_path.parent.resolve()
    scenes: list[dict[str, Any]] = []
    total_duration = 0.0
    seen_ids: set[str] = set()
    for i, raw_scene in enumerate(raw_scenes):
        label = f"scenes[{i}]"
        if not isinstance(raw_scene, dict):
            raise RenderError(f"{label} must be an object.")
        scene_id = _require_text(raw_scene.get("id"), f"{label}.id", limit=80)
        if scene_id in seen_ids:
            raise RenderError(f"Duplicate scene id: {scene_id}")
        seen_ids.add(scene_id)
        kind = raw_scene.get("kind", "card")
        if kind not in {"card", "image", "video"}:
            raise RenderError(f"{label}.kind must be card, image, or video.")
        try:
            duration = float(raw_scene.get("duration_seconds"))
        except (TypeError, ValueError) as exc:
            raise RenderError(f"{label}.duration_seconds must be numeric.") from exc
        if not math.isfinite(duration) or duration <= 0 or duration > MAX_SCENE_SECONDS:
            raise RenderError(f"{label}.duration_seconds must be greater than 0 and at most {MAX_SCENE_SECONDS:g}.")
        title = _require_text(raw_scene.get("title"), f"{label}.title", limit=180)
        body = _require_text(raw_scene.get("body", ""), f"{label}.body", optional=True, limit=1800)
        color = raw_scene.get("background", "#101b2d")
        if not isinstance(color, str) or not HEX_COLOR.fullmatch(color):
            raise RenderError(f"{label}.background must be a six-digit hex color such as #101b2d.")
        color = color.lstrip("#").lower()
        scene: dict[str, Any] = {"id": scene_id, "kind": kind, "duration_seconds": duration, "title": title, "body": body, "background": f"0x{color}"}
        if kind in {"image", "video"}:
            extensions = IMAGE_EXTENSIONS if kind == "image" else VIDEO_EXTENSIONS
            source = _safe_project_file(project_root, raw_scene.get("source"), f"{label}.source", extensions)
            scene["source_path"] = source
            scene["source_relative_path"] = source.relative_to(project_root).as_posix()
            scene["source_sha256"] = sha256_file(source)
            scene["provenance"] = _parse_provenance(raw_scene.get("provenance"), label)
            if kind == "video":
                try:
                    start_seconds = float(raw_scene.get("start_seconds", 0))
                except (TypeError, ValueError) as exc:
                    raise RenderError(f"{label}.start_seconds must be numeric.") from exc
                if not math.isfinite(start_seconds) or start_seconds < 0 or start_seconds > 86_400:
                    raise RenderError(f"{label}.start_seconds must be between 0 and 86400.")
                scene["start_seconds"] = start_seconds
        scenes.append(scene)
        total_duration += duration
    if total_duration > MAX_TOTAL_SECONDS:
        raise RenderError(f"Campaign duration exceeds the {MAX_TOTAL_SECONDS:g}-second limit.")

    audio_path = None
    audio_provenance = None
    audio = campaign.get("audio")
    if audio is not None:
        if not isinstance(audio, dict):
            raise RenderError("audio must be an object when supplied.")
        audio_path = _safe_project_file(project_root, audio.get("source"), "audio.source", AUDIO_EXTENSIONS)
        audio_provenance = _parse_provenance(audio.get("provenance"), "audio")
        try:
            volume = float(audio.get("volume", 0.25))
        except (TypeError, ValueError) as exc:
            raise RenderError("audio.volume must be numeric between 0 and 1.") from exc
        if not math.isfinite(volume) or not 0 <= volume <= 1:
            raise RenderError("audio.volume must be between 0 and 1.")
        campaign["_audio_volume"] = volume
    approval = _parse_approval(campaign.get("approval"))
    claims = _parse_claim_evidence(campaign.get("claims_evidence"))
    blockers = _release_blockers(approval, claims, scenes, audio_path, audio_provenance)
    if not watermark and blockers:
        raise RenderError("Unwatermarked release export blocked: " + "; ".join(blockers))
    campaign["_approval"] = approval
    campaign["_claims_evidence"] = claims
    campaign["_audio_provenance"] = audio_provenance
    campaign["_release_blockers"] = blockers
    campaign["_validated"] = {
        "manifest_sha256": hashlib.sha256(raw).hexdigest(), "project_id": project_id, "project_title": project_title,
        "project_root": str(project_root), "width": width, "height": height, "fps": fps,
        "watermark_text": watermark, "output_relative_path": requested_output, "duration_seconds": round(total_duration, 6),
    }
    return campaign, project_root, scenes, audio_path


def _find_font() -> Path:
    candidates: list[Path] = []
    fc_match = shutil.which("fc-match")
    if fc_match:
        try:
            probe = subprocess.run([fc_match, "-f", "%{file}", "sans"], check=True, capture_output=True, text=True, timeout=5)
            if probe.stdout.strip():
                candidates.append(Path(probe.stdout.strip()))
        except (OSError, subprocess.SubprocessError):
            pass
    candidates.extend([
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
        Path("/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"),
        Path("/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf"),
        Path("/System/Library/Fonts/Supplemental/Arial.ttf"),
        Path("/Library/Fonts/Arial.ttf"), Path("C:/Windows/Fonts/arial.ttf"),
    ])
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    raise RenderError("No usable TrueType font found. Install fontconfig plus a Unicode-capable TTF font, or install a supported system font.")


def _version(executable: str) -> str:
    try:
        result = subprocess.run([executable, "-version"], check=True, capture_output=True, text=True, timeout=10)
    except (OSError, subprocess.SubprocessError) as exc:
        raise RenderError(f"Cannot execute {executable}: {exc}") from exc
    return (result.stdout or result.stderr).splitlines()[0].strip()


def _wrap_text(value: str, width: int) -> str:
    output: list[str] = []
    for paragraph in value.splitlines() or [""]:
        if paragraph.strip():
            output.extend(textwrap.wrap(paragraph, width=width, break_long_words=False, break_on_hyphens=False) or [""])
        else:
            output.append("")
    return "\n".join(output)


def _run(command: list[str], *, cwd: Path, timeout: int, label: str) -> subprocess.CompletedProcess[str]:
    try:
        result = subprocess.run(command, cwd=cwd, capture_output=True, text=True, timeout=timeout, check=False)
    except subprocess.TimeoutExpired as exc:
        raise RenderError(f"{label} timed out after {timeout} seconds.") from exc
    except OSError as exc:
        raise RenderError(f"Could not start {label}: {exc}") from exc
    if result.returncode != 0:
        detail = (result.stderr or result.stdout or "No diagnostic supplied by tool.").strip()
        raise RenderError(f"{label} failed (exit {result.returncode}): {detail[-2400:]}")
    return result


def render_campaign(manifest_path: Path, output_override: Path | None = None, *, overwrite: bool = False) -> dict[str, Any]:
    campaign, project_root, scenes, audio_path = load_campaign(manifest_path)
    settings = campaign["_validated"]
    ffmpeg = shutil.which(os.environ.get("FFMPEG_BIN", "ffmpeg"))
    ffprobe = shutil.which(os.environ.get("FFPROBE_BIN", "ffprobe"))
    if not ffmpeg:
        raise RenderError("FFmpeg executable not found. Install FFmpeg or set FFMPEG_BIN to its executable path.")
    if not ffprobe:
        raise RenderError("FFprobe executable not found. Install FFprobe or set FFPROBE_BIN to its executable path.")
    ffmpeg_version, ffprobe_version, font_path = _version(ffmpeg), _version(ffprobe), _find_font()
    output_raw = output_override if output_override is not None else project_root / settings["output_relative_path"]
    output_path = output_raw.expanduser().resolve()
    if output_path.suffix.lower() != ".mp4":
        raise RenderError("Output file must use the .mp4 extension.")
    if output_path.exists() and not overwrite:
        raise RenderError(f"Output already exists: {output_path}. Pass --overwrite to replace it.")
    if output_path in {scene.get("source_path") for scene in scenes} or (audio_path and output_path == audio_path):
        raise RenderError("Output path must not overwrite a source asset.")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    total_duration, width, height, fps = settings["duration_seconds"], settings["width"], settings["height"], settings["fps"]
    title_chars = max(20, int(width / max(1, (height * 0.052) * 0.54)))
    body_chars = max(28, int(width / max(1, (height * 0.027) * 0.52)))
    title_px, body_px, watermark_px = max(22, int(height * 0.052)), max(16, int(height * 0.027)), max(12, int(height * 0.016))

    with tempfile.TemporaryDirectory(prefix="video-workbench-render-") as temp_name:
        temp_dir = Path(temp_name).resolve()
        shutil.copyfile(font_path, temp_dir / "font.ttf")
        inputs: list[str] = [ffmpeg, "-hide_banner", "-loglevel", "error", "-nostdin", "-y"]
        graph_lines: list[str] = []
        video_labels: list[str] = []
        for i, scene in enumerate(scenes):
            duration = scene["duration_seconds"]
            if scene["kind"] == "card":
                inputs.extend(["-f", "lavfi", "-i", f"color=c={scene['background']}:s={width}x{height}:r={fps}:d={duration:.6f}"])
            elif scene["kind"] == "image":
                inputs.extend(["-loop", "1", "-framerate", str(fps), "-t", f"{duration:.6f}", "-i", str(scene["source_path"])])
            else:
                inputs.extend(["-stream_loop", "-1", "-ss", f"{scene['start_seconds']:.6f}", "-i", str(scene["source_path"])])
            title_file, body_file = f"scene_{i:02d}_title.txt", f"scene_{i:02d}_body.txt"
            (temp_dir / title_file).write_text(_wrap_text(scene["title"], title_chars), encoding="utf-8")
            (temp_dir / body_file).write_text(_wrap_text(scene["body"], body_chars), encoding="utf-8")
            filters = [
                f"[{i}:v]fps={fps},scale={width}:{height}:force_original_aspect_ratio=increase,crop={width}:{height},setsar=1,trim=duration={duration:.6f},setpts=PTS-STARTPTS,format=yuv420p",
                "drawbox=x=0:y=0:w=iw:h=12:color=0xe8b45b@0.95:t=fill",
                f"drawtext=fontfile=font.ttf:textfile={title_file}:fontcolor=white:fontsize={title_px}:line_spacing=10:x=(w-text_w)/2:y=h*0.25:shadowcolor=black@0.7:shadowx=2:shadowy=2:expansion=none",
            ]
            if scene["body"]:
                filters.append(f"drawtext=fontfile=font.ttf:textfile={body_file}:fontcolor=white:fontsize={body_px}:line_spacing=10:x=(w-text_w)/2:y=h*0.44:box=1:boxcolor=black@0.12:boxborderw=18:shadowcolor=black@0.6:shadowx=1:shadowy=1:expansion=none")
            if settings["watermark_text"]:
                watermark_file = f"scene_{i:02d}_watermark.txt"
                (temp_dir / watermark_file).write_text(_wrap_text(settings["watermark_text"], max(24, body_chars)), encoding="utf-8")
                filters.append(f"drawtext=fontfile=font.ttf:textfile={watermark_file}:fontcolor=0xffd98a:fontsize={watermark_px}:x=36:y=h-th-28:box=1:boxcolor=black@0.3:boxborderw=8:expansion=none")
            output_label = f"scenev{i}"
            graph_lines.append(",".join(filters) + f"[{output_label}]")
            video_labels.append(f"[{output_label}]")
        graph_lines.append("".join(video_labels) + f"concat=n={len(scenes)}:v=1:a=0[vout]")
        audio_label = None
        if audio_path:
            inputs.extend(["-stream_loop", "-1", "-i", str(audio_path)])
            volume = campaign.get("_audio_volume", 0.25)
            graph_lines.append(f"[{len(scenes)}:a]aresample=48000,volume={volume:.4f},atrim=duration={total_duration:.6f},asetpts=PTS-STARTPTS[aout]")
            audio_label = "[aout]"
        graph_path = temp_dir / "filtergraph.txt"
        graph_path.write_text(";\n".join(graph_lines), encoding="utf-8")
        temporary_output = temp_dir / "campaign.mp4"
        command = inputs + ["-filter_complex_script", str(graph_path), "-map", "[vout]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", "-r", str(fps), "-movflags", "+faststart"]
        command += ["-map", audio_label, "-c:a", "aac", "-b:a", "192k"] if audio_label else ["-an"]
        command += ["-t", f"{total_duration:.6f}", str(temporary_output)]
        _run(command, cwd=temp_dir, timeout=max(120, int(total_duration * 12)), label="FFmpeg render")
        probe_result = _run([ffprobe, "-v", "error", "-show_streams", "-show_format", "-of", "json", str(temporary_output)], cwd=temp_dir, timeout=30, label="FFprobe validation")
        try:
            probe = json.loads(probe_result.stdout)
        except json.JSONDecodeError as exc:
            raise RenderError("FFprobe returned invalid JSON for rendered video.") from exc
        if not temporary_output.is_file() or temporary_output.stat().st_size < 1024:
            raise RenderError("FFmpeg did not create a plausible non-empty MP4 output.")
        video_streams = [s for s in probe.get("streams", []) if s.get("codec_type") == "video"]
        if len(video_streams) != 1:
            raise RenderError(f"Expected exactly one video stream, got {len(video_streams)}.")
        stream = video_streams[0]
        if stream.get("codec_name") != "h264" or stream.get("width") != width or stream.get("height") != height:
            raise RenderError("Rendered video failed codec or dimension validation.")
        duration_reported = float(probe.get("format", {}).get("duration", 0))
        if abs(duration_reported - total_duration) > max(0.15, 1.0 / fps):
            raise RenderError(f"Rendered duration mismatch: expected {total_duration:.3f}s, got {duration_reported:.3f}s.")
        rate = stream.get("avg_frame_rate") or stream.get("r_frame_rate") or "0/1"
        try:
            numerator, denominator = (int(part) for part in rate.split("/", 1))
            actual_fps = numerator / denominator if denominator else 0
        except (ValueError, ZeroDivisionError):
            actual_fps = 0
        if abs(actual_fps - fps) > 0.01:
            raise RenderError(f"Rendered frame-rate mismatch: expected {fps}, got {rate}.")
        if audio_path and not any(s.get("codec_type") == "audio" and s.get("codec_name") == "aac" for s in probe.get("streams", [])):
            raise RenderError("Audio was requested but the output has no AAC audio stream.")
        if not audio_path and any(s.get("codec_type") == "audio" for s in probe.get("streams", [])):
            raise RenderError("Unexpected audio stream in a silent render.")
        staging_output = output_path.with_name(f".{output_path.stem}.staging-{os.getpid()}.mp4")
        shutil.copyfile(temporary_output, staging_output)
        os.replace(staging_output, output_path)
        output_sha = sha256_file(output_path)
        sources = [{
            "scene_id": scene["id"], "kind": scene["kind"], "source": scene.get("source_relative_path"),
            "sha256": scene.get("source_sha256"), "provenance": scene.get("provenance"),
            "duration_seconds": scene["duration_seconds"], "title": scene["title"],
        } for scene in scenes]
        if audio_path:
            sources.append({"kind": "audio", "source": audio_path.relative_to(project_root).as_posix(), "sha256": sha256_file(audio_path), "provenance": campaign.get("_audio_provenance")})
        result = {
            "schema_version": 1, "status": "verified",
            "renderer": {"name": "video-workbench-ffmpeg", "version": RENDERER_VERSION, "ffmpeg": ffmpeg_version, "ffprobe": ffprobe_version},
            "rendered_at_utc": datetime.now(timezone.utc).isoformat(),
            "project": {"id": settings["project_id"], "title": settings["project_title"]},
            "input_manifest": {"path": Path(manifest_path).name, "sha256": settings["manifest_sha256"]},
            "output": {"path": str(output_path), "sha256": output_sha, "bytes": output_path.stat().st_size, "container": "mp4",
                       "video_codec": "h264", "audio_codec": "aac" if audio_path else None, "width": width, "height": height,
                       "fps": fps, "duration_seconds": round(duration_reported, 6), "expected_frame_count": int(round(total_duration * fps))},
            "sources": sources, "approval": campaign.get("_approval"), "claims_evidence": campaign.get("_claims_evidence", []),
            "release_gate": {"status": "blocked" if campaign.get("_release_blockers") else "passed", "blockers": campaign.get("_release_blockers", [])},
            "validation": {"ffprobe_passed": True, "codec_and_dimensions_passed": True, "duration_passed": True, "frame_rate_passed": True, "audio_expectation_passed": True},
            "limitations": ["Successful rendering verifies media assembly and file structure, not factual accuracy, product behavior, rights ownership, or publication approval. A watermark is not a substitute for human review."],
        }
        sidecar = output_path.with_suffix(output_path.suffix + ".manifest.json")
        sidecar_tmp = sidecar.with_name(sidecar.name + f".tmp-{os.getpid()}")
        sidecar_tmp.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        os.replace(sidecar_tmp, sidecar)
        return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Render and verify a Video Workbench campaign manifest.")
    parser.add_argument("manifest", type=Path, help="Path to a campaign JSON manifest.")
    parser.add_argument("--output", type=Path, help="Override output path. Defaults to output.path in the manifest.")
    parser.add_argument("--overwrite", action="store_true", help="Replace an existing output file.")
    args = parser.parse_args(argv)
    try:
        result = render_campaign(args.manifest, args.output, overwrite=args.overwrite)
    except RenderError as exc:
        print(json.dumps({"status": "failed", "error": str(exc)}, indent=2), file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
