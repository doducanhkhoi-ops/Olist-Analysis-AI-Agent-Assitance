import py_compile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


class TestRepositoryIntegrity(unittest.TestCase):
    def test_all_python_scripts_compile(self):
        py_files = [p for p in REPO_ROOT.glob("*.py")]
        self.assertGreaterEqual(len(py_files), 8)
        for py_file in py_files:
            with self.subTest(file=py_file.name):
                py_compile.compile(str(py_file), doraise=True)

    def test_diagnostic_html_cockpits_are_present(self):
        expected_html = [
            "Olist_Freight_Deadweight_Cockpit.html",
            "Olist_Fulfillment_Handover_Cockpit.html",
            "payment_financing_diagnostic.html",
            "year_end_logistics_diagnostic.html",
        ]
        for name in expected_html:
            path = REPO_ROOT / name
            self.assertTrue(path.exists(), f"Missing {name}")
            content = path.read_text(encoding="utf-8", errors="ignore")
            self.assertIn("<html", content.lower())

    def test_agent_skills_have_skill_markdown(self):
        skills_dir = REPO_ROOT / ".agents" / "skills"
        self.assertTrue(skills_dir.is_dir())
        skill_dirs = [d for d in skills_dir.iterdir() if d.is_dir()]
        self.assertGreaterEqual(len(skill_dirs), 15)
        for skill_dir in skill_dirs:
            self.assertTrue((skill_dir / "SKILL.md").exists(), f"Missing SKILL.md in {skill_dir.name}")


if __name__ == "__main__":
    unittest.main()
