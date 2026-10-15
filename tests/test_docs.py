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
    "docs/ROADMAP.md",
    "docs/decisions/ADR-0001-separate-product-repository.md",
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
        self.assertIn("Deferred", brief)
        self.assertIn("provider-independent", architecture)
        self.assertIn("remain open", brief)

    def test_product_brief_captures_company_use_and_one_bounded_workflow(self):
        brief = (ROOT / "docs/PRODUCT_BRIEF.md").read_text(encoding="utf-8")
        self.assertIn("company owner/operator", brief)
        self.assertIn("Primary job-to-be-done", brief)
        self.assertIn("business offering to video campaign pack", brief)
        self.assertIn("Broader outcome families — not all MVP scope", brief)
        self.assertIn("project scopes", brief)
        self.assertIn("stub must never be represented as actual model execution", brief)


if __name__ == "__main__":
    unittest.main()
