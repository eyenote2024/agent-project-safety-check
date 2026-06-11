import tempfile
import unittest
from pathlib import Path

import agent_project_safety_check as checker


class SafetyCheckTests(unittest.TestCase):
    def test_flags_sensitive_file_names_without_reading_contents(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".env.local").write_text("SECRET_VALUE=do-not-print", encoding="utf-8")

            finding = checker.check_sensitive_files(root)

            self.assertIsNotNone(finding)
            self.assertEqual(finding.severity, "HIGH")
            self.assertEqual(finding.items, [".env.local"])

    def test_gitignore_passes_with_recommended_patterns(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".gitignore").write_text(
                "\n".join(checker.RECOMMENDED_GITIGNORE),
                encoding="utf-8",
            )

            self.assertIsNone(checker.check_gitignore(root))

    def test_agents_md_passes_when_present(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "AGENTS.md").write_text("# Rules\n", encoding="utf-8")

            self.assertIsNone(checker.check_agents_md(root))


if __name__ == "__main__":
    unittest.main()
