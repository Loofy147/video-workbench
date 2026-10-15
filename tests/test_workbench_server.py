from __future__ import annotations
import json
import shutil
import subprocess
import sys
import zipfile
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "src"))
import workbench_server as app


def valid_plan():
    return {
        "project_title": "Local demo campaign",
        "offering": "A specific service with owner-supplied facts.",
        "audience": "Small business operators",
        "objective": "Explain the offer and encourage a demo request.",
        "differentiators": "Owner to verify before publishing.",
        "call_to_action": "Request a demonstration",
        "scenes": [
            {"title": "What it is", "body": "A clear, concise offer.", "duration_seconds": 3, "background": "#101b2d"},
            {"title": "Next step", "body": "Review the details before publication.", "duration_seconds": 4, "background": "#18394b"},
        ],
    }


class PlanContractTests(unittest.TestCase):
    def test_build_campaign_is_watermarked_draft_with_bounded_card_scenes(self):
        plan = app.normalize_plan(valid_plan())
        campaign = app.build_campaign(plan, "a" * 32, 2)
        self.assertEqual(campaign["approval"]["status"], "draft")
        self.assertIn("NOT FOR PUBLICATION", campaign["output"]["watermark_text"])
        self.assertEqual(campaign["output"]["path"], "outputs/draft-v2.mp4")
        self.assertEqual([scene["kind"] for scene in campaign["scenes"]], ["card", "card"])
        self.assertEqual((campaign["output"]["width"], campaign["output"]["height"], campaign["output"]["fps"]), (1280, 720, 30))

    def test_brief_contains_required_review_checklist(self):
        brief = app.build_brief(app.normalize_plan(valid_plan()), 1)
        self.assertIn("Campaign brief: Local demo campaign", brief)
        self.assertIn("Review checklist", brief)
        self.assertIn("Confirm permission and license", brief)
        self.assertIn("not independently verify", brief)

    def test_rejects_invalid_scene_counts_durations_colors_and_missing_fields(self):
        raw = valid_plan()
        raw["scenes"] = []
        with self.assertRaisesRegex(ValueError, "between 1 and 8"):
            app.normalize_plan(raw)
        raw = valid_plan()
        raw["scenes"][0]["duration_seconds"] = float("inf")
        with self.assertRaisesRegex(ValueError, "duration"):
            app.normalize_plan(raw)
        raw = valid_plan()
        raw["scenes"][0]["background"] = "url(https://bad.example)"
        with self.assertRaisesRegex(ValueError, "six-digit hex"):
            app.normalize_plan(raw)
        raw = valid_plan()
        raw["project_title"] = "\u0000bad"
        with self.assertRaisesRegex(ValueError, "null character"):
            app.normalize_plan(raw)
        raw = valid_plan()
        raw["offering"] = ""
        with self.assertRaisesRegex(ValueError, "Offering is required"):
            app.normalize_plan(raw)

    def test_claim_ledger_preserves_status_and_requires_evidence_when_asserted(self):
        raw = valid_plan()
        raw["claims_evidence"] = [
            {"claim": "The workflow groups contributions by project", "status": "documented-source",
             "evidence": "https://example.org/product-docs"},
            {"claim": "The owner demonstrated the workflow", "status": "direct-observation",
             "evidence": "Observed during owner walkthrough on 2026-10-15"},
            {"claim": "The process may reduce coordination cost", "status": "inference", "evidence": ""},
            {"claim": "Payouts are guaranteed", "status": "unverified", "evidence": ""},
        ]
        plan = app.normalize_plan(raw)
        campaign = app.build_campaign(plan, "a" * 32, 1)
        brief = app.build_brief(plan, 1)
        self.assertEqual(campaign["claims_evidence"], plan["claims_evidence"])
        self.assertIn("The workflow groups contributions by project", brief)
        self.assertIn("status: unverified", brief)
        self.assertIn("does not open or independently verify references", brief)
        self.assertIsNone(plan["claims_evidence"][3]["evidence"])

    def test_claim_ledger_rejects_missing_required_evidence_invalid_status_and_too_many_claims(self):
        raw = valid_plan()
        raw["claims_evidence"] = [{"claim": "Observed fact", "status": "direct-observation", "evidence": ""}]
        with self.assertRaisesRegex(ValueError, "needs an evidence URL or observation note"):
            app.normalize_plan(raw)
        raw["claims_evidence"] = [{"claim": "Mystery claim", "status": "approved", "evidence": "some reference"}]
        with self.assertRaisesRegex(ValueError, "status must be one of"):
            app.normalize_plan(raw)
        raw["claims_evidence"] = [{"claim": "Malformed status", "status": []}]
        with self.assertRaisesRegex(ValueError, "status must be one of"):
            app.normalize_plan(raw)
        raw["claims_evidence"] = [{"claim": f"Claim {index}", "status": "unverified"} for index in range(31)]
        with self.assertRaisesRegex(ValueError, "at most 30"):
            app.normalize_plan(raw)

    def test_total_storyboard_duration_is_bounded(self):
        raw = valid_plan()
        raw["scenes"] = [{"title": f"Scene {i}", "duration_seconds": 20, "background": "#101b2d"} for i in range(5)]
        with self.assertRaisesRegex(ValueError, "must not exceed 90"):
            app.normalize_plan(raw)

    def test_external_origins_are_rejected(self):
        self.assertTrue(app.origin_allowed(None, 8765))
        self.assertTrue(app.origin_allowed("http://127.0.0.1:8765", 8765))
        self.assertTrue(app.origin_allowed("http://localhost:8765", 8765))
        self.assertFalse(app.origin_allowed("https://localhost:8765", 8765))
        self.assertFalse(app.origin_allowed("http://127.0.0.1:8766", 8765))
        self.assertFalse(app.origin_allowed("http://[::1]:8765", 8765))
        self.assertFalse(app.origin_allowed("http://attacker.example", 8765))
        self.assertFalse(app.origin_allowed("null", 8765))

    def test_project_ids_cannot_escape_workspace(self):
        for unsafe in ("../outside", "A" * 32, "", "1234"):
            with self.subTest(unsafe=unsafe), self.assertRaises(ValueError):
                app._project_dir(unsafe)


class ProjectPersistenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="vw-ui-test-")
        self.root = Path(self.temp.name) / "projects"
        self.root.mkdir(parents=True)
        self.root_patch = patch.object(app, "PROJECTS_ROOT", self.root)
        self.root_patch.start()
        self.addCleanup(self.root_patch.stop)
        self.addCleanup(self.temp.cleanup)

    def test_create_save_update_and_list_projects_with_versioned_artifacts(self):
        plan = valid_plan()
        plan["claims_evidence"] = [{
            "claim": "A measurable claim requiring owner review",
            "status": "documented-source",
            "evidence": "https://example.org/owner-reviewed-source",
        }]
        created = app.create_project(plan)
        project = created["project"]
        project_id = project["id"]
        folder = self.root / project_id
        self.assertEqual(project["version"], 1)
        self.assertTrue((folder / "brief-v1.md").is_file())
        manifest1 = json.loads((folder / "campaign-v1.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest1["output"]["path"], "outputs/draft-v1.mp4")
        self.assertEqual(manifest1["claims_evidence"][0]["claim"], "A measurable claim requiring owner review")
        self.assertIn("Claims and evidence ledger", (folder / "brief-v1.md").read_text(encoding="utf-8"))
        edited = valid_plan()
        edited["project_title"] = "Edited campaign"
        updated = app.update_project(project_id, edited)
        self.assertEqual(updated["project"]["version"], 2)
        self.assertEqual(updated["project"]["title"], "Edited campaign")
        self.assertTrue((folder / "brief-v1.md").is_file(), "prior version brief should remain immutable")
        self.assertTrue((folder / "campaign-v1.json").is_file(), "prior version manifest should remain immutable")
        manifest2 = json.loads((folder / "campaign-v2.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest2["output"]["path"], "outputs/draft-v2.mp4")
        loaded = app.get_project(project_id)
        self.assertEqual(loaded["plan"]["project_title"], "Edited campaign")
        self.assertEqual(len(loaded["version_history"]), 2)
        self.assertEqual(app.list_projects()[0]["id"], project_id)

        pack_path = app.build_draft_pack(project_id)
        with zipfile.ZipFile(pack_path) as pack:
            names = set(pack.namelist())
            self.assertTrue({"brief.md", "campaign.json", "PACK-STATUS.txt"}.issubset(names))
            self.assertFalse(any(name.endswith(".mp4") for name in names))
            status = pack.read("PACK-STATUS.txt").decode("utf-8")
            self.assertIn("NOT FOR PUBLICATION", status)
            self.assertIn("Rendered MP4 included: no", status)
            campaign_pack = json.loads(pack.read("campaign.json"))
            self.assertEqual(campaign_pack["project"]["title"], "Edited campaign")

    def test_render_records_technical_result_without_unblocking_publication(self):
        created = app.create_project(valid_plan())
        project_id = created["project"]["id"]
        with patch.object(app, "render_campaign", return_value={
            "status": "verified", "rendered_at_utc": "2026-10-15T00:00:00Z",
            "output": {"sha256": "0" * 64, "bytes": 1024, "container": "mp4", "video_codec": "h264", "audio_codec": None,
                       "width": 1280, "height": 720, "fps": 30, "duration_seconds": 7, "expected_frame_count": 210},
            "validation": {"ffprobe_passed": True},
            "release_gate": {"status": "blocked", "blockers": ["campaign approval is not approved"]},
            "renderer": {"name": "test-renderer", "version": "test"},
        }) as renderer:
            result = app.render_project(project_id)
        renderer.assert_called_once()
        self.assertEqual(result["project"]["state"], "rendered_draft")
        self.assertEqual(result["render"]["release_gate"]["status"], "blocked")
        with self.assertRaisesRegex(RuntimeError, "already been rendered"):
            app.render_project(project_id)
        edited = valid_plan()
        edited["project_title"] = "Edited after render"
        app.update_project(project_id, edited)
        self.assertEqual(app.get_project(project_id)["project"]["version"], 2)

    def test_render_failure_is_recorded(self):
        created = app.create_project(valid_plan())
        project_id = created["project"]["id"]
        with patch.object(app, "render_campaign", side_effect=app.RenderError("FFmpeg is missing")):
            with self.assertRaisesRegex(app.RenderError, "FFmpeg is missing"):
                app.render_project(project_id)
        failed = app.get_project(project_id)
        self.assertEqual(failed["project"]["state"], "render_failed")
        self.assertIn("FFmpeg is missing", failed["project"]["render_error"])


class BrowserAssetContractTests(unittest.TestCase):
    def test_local_assets_use_external_scripts_and_safe_text_rendering(self):
        html = (ROOT / "web" / "index.html").read_text(encoding="utf-8")
        script = (ROOT / "web" / "app.js").read_text(encoding="utf-8")
        server = (ROOT / "tools" / "workbench_server.py").read_text(encoding="utf-8")
        self.assertIn('<script src="/assets/app.js" defer></script>', html)
        self.assertIn('href="/assets/styles.css"', html)
        self.assertIn('id="claim-list"', html)
        self.assertIn('id="pack-link"', html)
        self.assertIn("files/pack", script)
        self.assertIn("claims_evidence", script)
        self.assertIn("savedPlanSignature", script)
        self.assertIn("Save edits before rendering", script)
        self.assertIn("JSON.stringify(collectPlan()) !== savedPlanSignature", script)
        self.assertIn('form.addEventListener("input", syncDirtyState)', script)
        self.assertIn('form.addEventListener("change", syncDirtyState)', script)
        self.assertNotRegex(html, r"(?i)\son[a-z]+\s*=")
        self.assertIn("textContent", script)
        self.assertNotRegex(script, r"\.innerHTML\s*=|insertAdjacentHTML|document\.write\s*\(")
        self.assertIn("script-src 'self'", server)

    def test_browser_javascript_parses_when_node_is_available(self):
        node = shutil.which("node")
        if not node:
            self.skipTest("Node.js is not installed in this environment.")
        result = subprocess.run(
            [node, "--check", str(ROOT / "web" / "app.js")],
            capture_output=True, text=True, timeout=15, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "FFmpeg/FFprobe not installed")
class BrowserRendererIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="vw-browser-render-e2e-")
        self.root = Path(self.temp.name) / "projects"
        self.root.mkdir(parents=True)
        self.root_patch = patch.object(app, "PROJECTS_ROOT", self.root)
        self.root_patch.start()
        self.addCleanup(self.root_patch.stop)
        self.addCleanup(self.temp.cleanup)

    def test_saved_browser_campaign_renders_real_mp4_and_provenance(self):
        created = app.create_project(valid_plan())
        project_id = created["project"]["id"]
        result = app.render_project(project_id)
        project_dir = self.root / project_id
        video = project_dir / "outputs" / "draft-v1.mp4"
        sidecar = project_dir / "outputs" / "draft-v1.mp4.manifest.json"
        self.assertEqual(result["project"]["state"], "rendered_draft")
        self.assertTrue(video.is_file())
        self.assertTrue(sidecar.is_file())
        self.assertGreater(video.stat().st_size, 1_024)
        saved = json.loads(sidecar.read_text(encoding="utf-8"))
        self.assertEqual(saved["output"]["video_codec"], "h264")
        self.assertEqual(saved["output"]["width"], 1280)
        self.assertEqual(saved["output"]["height"], 720)
        self.assertTrue(saved["validation"]["ffprobe_passed"])
        self.assertTrue(saved["validation"]["frame_count_passed"])
        self.assertEqual(saved["output"]["expected_frame_count"], 210)
        self.assertEqual(saved["output"]["sha256"], result["render"]["output"]["sha256"])
        self.assertEqual(saved["release_gate"]["status"], "blocked")
        self.assertIn("campaign approval is not approved", saved["release_gate"]["blockers"])
        self.assertIn("NOT FOR PUBLICATION", json.loads(
            (project_dir / "campaign-v1.json").read_text(encoding="utf-8")
        )["output"]["watermark_text"])
        pack_path = app.build_draft_pack(project_id)
        with zipfile.ZipFile(pack_path) as pack:
            names = set(pack.namelist())
            self.assertTrue({"brief.md", "campaign.json", "draft-v1.mp4", "draft-v1.mp4.manifest.json", "PACK-STATUS.txt"}.issubset(names))
            self.assertIn("Rendered MP4 included: yes", pack.read("PACK-STATUS.txt").decode("utf-8"))
            self.assertEqual(json.loads(pack.read("campaign.json"))["claims_evidence"], [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
