"""Guard the initial product documentation structure and internal Markdown links."""

from pathlib import Path
import re
import unittest
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_FILES = (
    "README.md",
    "CONTRIBUTING.md",
    "docs/PRODUCT_BRIEF.md",
    "docs/ARCHITECTURE.md",
    "docs/LICENSING_AND_PROVENANCE.md",
    "docs/REUSE_AUDIT.md",
    "docs/ROADMAP.md",
    "docs/decisions/ADR-0001-separate-product-repository.md",
    "docs/examples/contribution-network-campaign-brief.md",
)
MARKDOWN_LINK = re.compile(r"!?(?:\[[^\]]*\])\(([^)\s]+)(?:\s+[^)]*)?\)")


class RepositoryFoundationTests(unittest.TestCase):
    def test_required_foundation_documents_exist_and_are_nonempty(self):
        for relative_path in REQUIRED_FILES:
            with self.subTest(path=relative_path):
                path = ROOT / relative_path
                self.assertTrue(path.is_file(), f"Missing required file: {relative_path}")
                self.assertGreater(path.stat().st_size, 0, f"Empty required file: {relative_path}")

    def test_relative_markdown_links_resolve(self):
        broken = []
        for markdown_file in ROOT.rglob("*.md"):
            if any(part in {".git", ".venv", "node_modules"} for part in markdown_file.parts):
                continue
            text = markdown_file.read_text(encoding="utf-8")
            for match in MARKDOWN_LINK.finditer(text):
                raw_target = match.group(1)
                if raw_target.startswith("#"):
                    continue
                parsed = urlparse(raw_target)
                if parsed.scheme or parsed.netloc:
                    continue
                target_path = raw_target.split("#", 1)[0]
                if not target_path:
                    continue
                candidate = (markdown_file.parent / target_path).resolve()
                try:
                    candidate.relative_to(ROOT.resolve())
                except ValueError:
                    broken.append(f"{markdown_file.relative_to(ROOT)} -> escapes repository: {raw_target}")
                    continue
                if not candidate.exists():
                    broken.append(f"{markdown_file.relative_to(ROOT)} -> missing: {raw_target}")
        self.assertEqual([], broken, "\n".join(broken))

    def test_provider_selection_is_not_locked_in_foundation_docs(self):
        brief = (ROOT / "docs/PRODUCT_BRIEF.md").read_text(encoding="utf-8")
        architecture = (ROOT / "docs/ARCHITECTURE.md").read_text(encoding="utf-8")
        self.assertIn("### Defer", brief)
        self.assertIn("provider-independent", architecture)
        self.assertIn("final-mile evaluation", brief)

    def test_pilot_campaign_brief_is_source_grounded_and_discloses_limits(self):
        brief = (ROOT / "docs/examples/contribution-network-campaign-brief.md").read_text(encoding="utf-8")
        self.assertIn("Draft for owner review", brief)
        self.assertIn("1–10 distinct acceptance criteria", brief)
        self.assertIn("Paid bounty listings are not processed payouts", brief)
        self.assertIn("five browser scenarios still need live execution", brief)
        self.assertIn("product-market fit", brief)
        self.assertIn("No finished video is represented by this document", brief)
        self.assertIn("Open Graph/share-preview metadata", brief)
        self.assertIn("engineering-task text rather than approved public marketing copy", brief)

    def test_fastvideo_reuse_audit_records_the_no-copy_decision_and_low-dependency_path(self):
        audit = (ROOT / "docs/REUSE_AUDIT.md").read_text(encoding="utf-8")
        self.assertIn("d5253fd71055927f12aa6c4aa679b93a00238851", audit)
        self.assertIn("Do not adopt either application as the Video Workbench product base", audit)
        self.assertIn("deterministic local media-assembly path", audit)
        self.assertIn("allow_origins=[\"*\"]", audit)
        self.assertIn("No FastVideo source or model artifacts were copied", audit)
        self.assertIn("repository is currently public and has no selected project license", audit)

    def test_ci_actions_are_pinned_to_full_commit_shas_with_release_comments(self):
        workflow = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
        for action in ("checkout", "setup-python"):
            self.assertRegex(
                workflow,
                rf"(?m)^\s+uses: actions/{action}@[0-9a-f]{{40}}\s+# v\d+\.\d+\.\d+\s*$",
            )

    def test_product_brief_captures_company_use_and_one_bounded_workflow(self):
        brief = (ROOT / "docs/PRODUCT_BRIEF.md").read_text(encoding="utf-8")
        self.assertIn("company owner/operator", brief)
        self.assertIn("Primary job-to-be-done", brief)
        self.assertIn("business offering to video campaign pack", brief)
        self.assertIn("Broader outcome families — not all MVP scope", brief)
        self.assertIn("project scopes", brief)
        self.assertIn("A mock/stub must never be represented as a real render or real model execution.", brief)
        self.assertIn("Contribution Network / its current ContribQuest prototype", brief)
        self.assertIn("there is no escrow, payment processing, or guaranteed payout", brief)
        self.assertIn("XP is not independently validated as a measure of skill", brief)
        self.assertIn("not as proven production-ready infrastructure", brief)


if __name__ == "__main__":
    unittest.main()
