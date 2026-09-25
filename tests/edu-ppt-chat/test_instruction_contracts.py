from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
SKILL_DIR = ROOT / "edu-ppt-chat"


class SkillContractTests(unittest.TestCase):
    @classmethod
    def load_skill_text(cls) -> str:
        return (SKILL_DIR / "SKILL.md").read_text(encoding="utf-8")

    def test_required_files_exist(self):
        self.assertTrue((SKILL_DIR / "SKILL.md").is_file())
        self.assertTrue((SKILL_DIR / "agents" / "openai.yaml").is_file())

    def test_skill_identity_and_explicit_only_policy(self):
        skill = self.load_skill_text()
        metadata = (SKILL_DIR / "agents" / "openai.yaml").read_text(
            encoding="utf-8"
        )
        self.assertIn("name: edu-ppt-chat", skill)
        self.assertIn("allow_implicit_invocation: false", metadata)


if __name__ == "__main__":
    unittest.main()
