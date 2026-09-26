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

    def test_multiple_periods_are_merged_into_one_delivery_set(self):
        skill = self.load_skill_text()
        workflow = (SKILL_DIR / "references" / "workflow.md").read_text(
            encoding="utf-8"
        )
        deliverables = (SKILL_DIR / "references" / "deliverables.md").read_text(
            encoding="utf-8"
        )
        validation = (SKILL_DIR / "references" / "validation.md").read_text(
            encoding="utf-8"
        )

        self.assertIn("无论参考材料包含几个课时", skill)
        self.assertIn("课时只作为内部教学阶段", workflow)
        self.assertIn("一套连续的 PPT 页纲", deliverables)
        self.assertIn("一份整体教学设计", deliverables)
        self.assertIn("一份逐页连续的逐字稿", deliverables)
        self.assertIn("不得按课时拆分", validation)

    def test_visual_second_approval_is_conditional_when_deselected(self):
        workflow = (SKILL_DIR / "references" / "workflow.md").read_text(
            encoding="utf-8"
        )
        self.assertIn(
            "只有视觉蓝图被保留或用户明确要求背景参考图时",
            workflow,
        )

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

    def test_visual_reference_and_image_generation_boundaries(self):
        visual = (SKILL_DIR / "references" / "visual.md").read_text(
            encoding="utf-8"
        )
        for phrase in (
            "两个原创视觉方向",
            "只提取抽象视觉规律",
            "用户明确要求背景参考图",
            "1–2 张",
            "最多自动重试 1 次",
            "不得阻断文本流程",
        ):
            self.assertIn(phrase, visual)

    def test_removed_external_routes_are_not_dependencies(self):
        combined = "\n".join(
            path.read_text(encoding="utf-8") for path in SKILL_DIR.rglob("*.md")
        )
        for forbidden in (
            "$smartedu-numbered-lesson-reader",
            "$frontend-slides",
            "references/wps.md",
        ):
            self.assertNotIn(forbidden, combined)

    def test_validation_contract_covers_cross_output_repairs(self):
        validation = (SKILL_DIR / "references" / "validation.md").read_text(
            encoding="utf-8"
        )
        for phrase in (
            "页码连续",
            "材料覆盖",
            "事实依据",
            "教学时长",
            "跨产物一致性",
            "只修复受影响的产物",
            "重新执行完整检查",
        ):
            self.assertIn(phrase, validation)

    def test_all_references_are_routed_and_no_scaffold_markers_remain(self):
        skill = self.load_skill_text()
        for name in (
            "workflow.md",
            "teaching.md",
            "deliverables.md",
            "visual.md",
            "validation.md",
        ):
            self.assertIn(name, skill)

        combined = "\n".join(
            path.read_text(encoding="utf-8")
            for path in SKILL_DIR.rglob("*.*")
            if path.is_file()
        )
        markers = (
            "T" + "BD",
            "T" + "ODO",
            "implement " + "later",
            "fill in " + "details",
        )
        for marker in markers:
            self.assertNotIn(marker, combined)

    def test_skill_has_no_runtime_scripts(self):
        self.assertFalse((SKILL_DIR / "scripts").exists())


if __name__ == "__main__":
    unittest.main()
