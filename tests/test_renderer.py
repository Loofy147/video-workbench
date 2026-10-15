"""Contract and local-media acceptance tests for the FFmpeg campaign renderer."""
from __future__ import annotations

import json
from contextlib import redirect_stderr
from io import StringIO
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from video_workbench.render import RenderError, load_campaign, render_campaign, main  # noqa: E402


class CampaignManifestTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="vw-render-test-")
        self.root = Path(self.temp.name)
        self.manifest = self.root / "campaign.json"
        self.sample = {
            "schema_version": 1,
            "project": {"id": "test-project", "title": "Renderer Test"},
            "output": {"path": "output/test.mp4", "width": 640, "height": 360, "fps": 24,
                       "watermark_text": "TEST RENDER"},
            "scenes": [
                {"id": "scene-1", "kind": "card", "duration_seconds": 1,
                 "title": "A test title", "body": "A test caption", "background": "#101b2d"},
                {"id": "scene-2", "kind": "card", "duration_seconds": 1,
                 "title": "A second title", "body": "A second caption", "background": "#18394b"},
            ],
        }
        self.write_manifest()

    def tearDown(self):
        self.temp.cleanup()

    def write_manifest(self):
        self.manifest.write_text(json.dumps(self.sample, indent=2), encoding="utf-8")

    def test_valid_manifest_is_normalized_with_manifest_checksum(self):
        campaign, root, scenes, audio = load_campaign(self.manifest)
        self.assertEqual(root, self.root.resolve())
        self.assertEqual(len(scenes), 2)
        self.assertIsNone(audio)
        self.assertEqual(campaign["_validated"]["duration_seconds"], 2.0)
        self.assertEqual(len(campaign["_validated"]["manifest_sha256"]), 64)

    def test_rejects_duplicate_scene_ids(self):
        self.sample["scenes"][1]["id"] = self.sample["scenes"][0]["id"]
        self.write_manifest()
        with self.assertRaisesRegex(RenderError, "Duplicate scene id"):
            load_campaign(self.manifest)

    def test_rejects_invalid_duration_and_odd_dimensions(self):
        self.sample["scenes"][0]["duration_seconds"] = -1
        self.write_manifest()
        with self.assertRaisesRegex(RenderError, "duration_seconds"):
            load_campaign(self.manifest)
        self.sample["scenes"][0]["duration_seconds"] = 1
        self.sample["output"]["width"] = 641
        self.write_manifest()
        with self.assertRaisesRegex(RenderError, "must be even"):
            load_campaign(self.manifest)

    def test_unwatermarked_export_requires_approval_and_evidence(self):
        self.sample["output"]["watermark_text"] = ""
        self.write_manifest()
        with self.assertRaisesRegex(RenderError, "Unwatermarked release export blocked"):
            load_campaign(self.manifest)
        self.sample["approval"] = {
            "status": "approved", "approved_by": "reviewer",
            "approved_at": "2026-10-15T17:00:00Z",
        }
        self.sample["claims_evidence"] = [{
            "claim": "Claim from reviewed source", "status": "documented-source",
            "evidence": "https://example.org/source",
        }]
        self.write_manifest()
        campaign, _, _, _ = load_campaign(self.manifest)
        self.assertEqual(campaign["_approval"]["status"], "approved")
        self.assertEqual(campaign["_release_blockers"], [])

    def test_unwatermarked_export_rejects_naive_approval_timestamp(self):
        self.sample["output"]["watermark_text"] = ""
        self.sample["approval"] = {
            "status": "approved", "approved_by": "reviewer",
            "approved_at": "2026-10-15T17:00:00",
        }
        self.write_manifest()
        with self.assertRaisesRegex(RenderError, "must include a timezone"):
            load_campaign(self.manifest)

    def test_rejects_output_path_escape(self):
        self.sample["output"]["path"] = "../escape.mp4"
        self.write_manifest()
        with self.assertRaisesRegex(RenderError, "must stay inside the campaign directory"):
            load_campaign(self.manifest)

    def test_rejects_input_asset_path_escape(self):
        outside = self.root.parent / "outside-image.png"
        outside.write_bytes(b"not-an-image")
        self.sample["scenes"][0].update({"kind": "image", "source": "../outside-image.png"})
        self.write_manifest()
        try:
            with self.assertRaisesRegex(RenderError, "must stay inside the campaign directory"):
                load_campaign(self.manifest)
        finally:
            outside.unlink(missing_ok=True)

    def test_rejects_missing_or_unsupported_asset(self):
        self.sample["scenes"][0].update({"kind": "image", "source": "missing.gif"})
        self.write_manifest()
        with self.assertRaisesRegex(RenderError, "does not exist or is not a file"):
            load_campaign(self.manifest)


    def test_cli_serializes_filesystem_errors_without_traceback(self):
        blocked_parent = self.root / "not-a-directory"
        blocked_parent.write_text("this path is a file", encoding="utf-8")
        stderr = StringIO()
        with redirect_stderr(stderr):
            status = main([str(self.manifest), "--output", str(blocked_parent / "campaign.mp4")])
        self.assertEqual(status, 2)
        message = stderr.getvalue()
        self.assertNotIn("Traceback", message)
        payload = json.loads(message)
        self.assertEqual(payload["status"], "failed")
        self.assertTrue(payload["error"])

    def test_does_not_overwrite_existing_output_by_default(self):
        output = self.root / "existing.mp4"
        output.write_bytes(b"keep")
        with self.assertRaisesRegex(RenderError, "already exists"):
            render_campaign(self.manifest, output)
        self.assertEqual(output.read_bytes(), b"keep")


@unittest.skipUnless(shutil.which("ffmpeg") and shutil.which("ffprobe"), "FFmpeg/FFprobe not installed")
class RendererIntegrationTests(unittest.TestCase):
    def test_renders_validated_mp4_and_sidecar_manifest(self):
        with tempfile.TemporaryDirectory(prefix="vw-render-e2e-") as temp_name:
            root = Path(temp_name)
            manifest = root / "campaign.json"
            payload = {
                "schema_version": 1,
                "project": {"id": "e2e", "title": "E2E Campaign"},
                "output": {"path": "dist/test.mp4", "width": 640, "height": 360, "fps": 24,
                           "watermark_text": "INTEGRATION TEST"},
                "scenes": [
                    {"id": "opening", "kind": "card", "duration_seconds": 1,
                     "title": "Render works", "body": "First real local MP4", "background": "#101b2d"},
                    {"id": "closing", "kind": "card", "duration_seconds": 1,
                     "title": "Check the output", "body": "Manifest, codec, frame rate, and duration", "background": "#18394b"},
                ],
            }
            manifest.write_text(json.dumps(payload), encoding="utf-8")
            result = render_campaign(manifest)
            output_path = root / "dist/test.mp4"
            sidecar = output_path.with_suffix(".mp4.manifest.json")
            self.assertEqual(result["status"], "verified")
            self.assertTrue(output_path.is_file())
            self.assertGreater(output_path.stat().st_size, 1024)
            self.assertTrue(sidecar.is_file())
            saved = json.loads(sidecar.read_text(encoding="utf-8"))
            self.assertEqual(saved["output"]["video_codec"], "h264")
            self.assertEqual(saved["output"]["duration_seconds"], 2.0)
            self.assertEqual(saved["output"]["width"], 640)
            self.assertEqual(saved["output"]["height"], 360)
            self.assertTrue(saved["validation"]["ffprobe_passed"])
            self.assertTrue(saved["validation"]["frame_count_passed"])
            self.assertEqual(saved["output"]["expected_frame_count"], 48)
            probe = subprocess.run(
                [shutil.which("ffprobe"), "-v", "error", "-show_entries",
                 "stream=codec_name,width,height,avg_frame_rate", "-of", "json", str(output_path)],
                capture_output=True, text=True, check=True, timeout=20,
            )
            stream = json.loads(probe.stdout)["streams"][0]
            self.assertEqual(
                (stream["codec_name"], stream["width"], stream["height"], stream["avg_frame_rate"]),
                ("h264", 640, 360, "24/1"),
            )

    def test_image_video_and_audio_assets_keep_provenance_and_audio_stream(self):
        with tempfile.TemporaryDirectory(prefix="vw-assets-e2e-") as temp_name:
            root = Path(temp_name)
            assets = root / "assets"
            assets.mkdir()
            image_path, video_path, audio_path = assets / "source.png", assets / "source.mp4", assets / "source.wav"
            subprocess.run([
                shutil.which("ffmpeg"), "-hide_banner", "-loglevel", "error", "-y",
                "-f", "lavfi", "-i", "color=c=0x17394f:s=640x360:d=1", "-frames:v", "1", str(image_path),
            ], check=True, capture_output=True, timeout=20)
            subprocess.run([
                shutil.which("ffmpeg"), "-hide_banner", "-loglevel", "error", "-y",
                "-f", "lavfi", "-i", "testsrc2=s=640x360:r=24:d=1", "-c:v", "libx264", "-pix_fmt", "yuv420p", str(video_path),
            ], check=True, capture_output=True, timeout=30)
            subprocess.run([
                shutil.which("ffmpeg"), "-hide_banner", "-loglevel", "error", "-y",
                "-f", "lavfi", "-i", "sine=frequency=440:duration=1", "-c:a", "pcm_s16le", str(audio_path),
            ], check=True, capture_output=True, timeout=20)
            manifest = root / "campaign.json"
            provenance = {"origin": "generated test fixture", "rights_status": "owner_created",
                          "reviewed_by": "test", "reviewed_at": "2026-10-15T00:00:00Z"}
            payload = {
                "schema_version": 1,
                "project": {"id": "assets-e2e", "title": "Asset and Audio Test"},
                "output": {"path": "dist/assets.mp4", "width": 640, "height": 360, "fps": 24, "watermark_text": "ASSET TEST"},
                "scenes": [
                    {"id": "still", "kind": "image", "source": "assets/source.png", "duration_seconds": 1,
                     "title": "Still image", "body": "Scale and crop", "background": "#101b2d", "provenance": provenance},
                    {"id": "clip", "kind": "video", "source": "assets/source.mp4", "start_seconds": 0, "duration_seconds": 1,
                     "title": "Source video", "body": "Trim and loop", "background": "#18394b", "provenance": provenance},
                ],
                "audio": {"source": "assets/source.wav", "volume": 0.1, "provenance": provenance},
            }
            manifest.write_text(json.dumps(payload), encoding="utf-8")
            result = render_campaign(manifest)
            self.assertEqual(result["status"], "verified")
            self.assertEqual(result["output"]["audio_codec"], "aac")
            self.assertEqual(len(result["sources"]), 3)
            self.assertTrue(all(source["provenance"]["rights_status"] == "owner_created" for source in result["sources"]))
            self.assertEqual(result["release_gate"]["status"], "blocked", "watermarked drafts remain non-release-approved")


if __name__ == "__main__":
    unittest.main(verbosity=2)
