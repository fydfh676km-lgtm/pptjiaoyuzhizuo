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

    def test_workflow_has_exactly_two_approval_gates(self):
        workflow = (SKILL_DIR / "references" / "workflow.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("第一次确认：产品简报", workflow)
        self.assertIn("第二次确认：内容与视觉方案", workflow)
        self.assertIn("不得增加第三次确认", workflow)

    def test_workflow_blocks_unreadable_materials(self):
        workflow = (SKILL_DIR / "references" / "workflow.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("阻止第一次确认", workflow)
        self.assertIn("一次最多询问四项", workflow)

    def test_workflow_separates_source_roles(self):
        workflow = (SKILL_DIR / "references" / "workflow.md").read_text(
            encoding="utf-8"
        )
        for label in ("教材", "教学要求", "教学设计", "参考图"):
            self.assertIn(label, workflow)

    def test_exact_output_labels_are_present(self):
        text = (SKILL_DIR / "references" / "deliverables.md").read_text(
            encoding="utf-8"
        )
        labels = (
            "页面标题：",
            "页面文字：",
            "画面风格：",
            "添加元素：",
            "文字字体与重点标注：",
            "布局排版：",
            "教学目标",
            "教学重点",
            "教学难点",
            "教学过程",
            "教师活动",
            "学生活动",
            "评价要点",
            "板书设计",
            "教师讲述",
            "课堂提问",
            "预设回答",
            "教师点拨",
            "过渡语",
        )
        for label in labels:
            self.assertIn(label, text)

    def test_material_only_facts_rule_is_present(self):
        teaching = (SKILL_DIR / "references" / "teaching.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("补充内容", teaching)
        self.assertIn("待核实", teaching)


if __name__ == "__main__":
    unittest.main()
