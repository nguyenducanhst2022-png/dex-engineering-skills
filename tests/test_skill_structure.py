# -*- coding: utf-8 -*-
"""
Pytest suite for DEX Engineering Skills Pack v8.0: Structural Verification.
Validates that all skills (401 Native + 5 Segregated Upstream Skills) adhere strictly
to Agent Skills Specification and contain the 14 mandatory sections with valid YAML frontmatter.
"""

import os
import re
import json
import pytest

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SKILLS_DIR = os.path.join(ROOT_DIR, ".agents", "skills")

MANDATORY_SECTIONS = [
    (1, ["purpose & scope", "purpose", "mục đích & phạm vi", "mục đích"]),
    (2, ["when to use", "khi nào sử dụng", "khi nào nên dùng", "trường hợp sử dụng"]),
    (3, ["when not to use", "khi nào không nên dùng", "khi không nên dùng"]),
    (4, ["prerequisites & input context", "prerequisites", "tiền đề & ngữ cảnh đầu vào", "tiền đề"]),
    (5, ["core concepts & taxonomy", "core concepts", "khái niệm cốt lõi & phân loại", "khái niệm cốt lõi"]),
    (6, ["step-by-step execution workflow", "execution workflow", "quy trình thực thi từng bước", "quy trình thực thi"]),
    (7, ["concrete examples", "examples", "ví dụ cụ thể"]),
    (8, ["anti-patterns & common traps", "anti-patterns", "bẫy thường gặp & anti-patterns", "anti-patterns & cạm bẫy"]),
    (9, ["quality gates & acceptance criteria", "quality gates", "tiêu chí nghiệm thu & quality gates", "tiêu chí nghiệm thu", "verification quality gates"]),
    (10, ["security & safety boundaries", "security boundaries", "ranh giới an toàn & bảo mật", "an toàn & bảo mật"]),
    (11, ["platform adapters", "adapters", "adapter nền tảng"]),
    (12, ["deliverables & output artifacts", "deliverables", "sản phẩm bàn giao & artifacts"]),
    (13, ["related & complementary skills", "related skills", "kỹ năng liên quan & bổ trợ"]),
    (14, ["realistic usage example", "usage example", "ví dụ tình huống thực tế"]),
]

def get_all_skills():
    if not os.path.exists(SKILLS_DIR):
        return []
    return sorted([d for d in os.listdir(SKILLS_DIR) if os.path.isdir(os.path.join(SKILLS_DIR, d))])

ALL_SKILLS = get_all_skills()

def test_total_skill_count():
    """Verify skill count matches exactly 400 specialized skills + 1 master orchestrator = 401 DEX skills."""
    expected_count = 401
    assert len(ALL_SKILLS) == expected_count, f"Expected {expected_count} skills, found {len(ALL_SKILLS)}"

def test_integration_skills_exist():
    """Verify third-party integration skills exist under integrations/."""
    int_dir = os.path.join(ROOT_DIR, "integrations")
    assert os.path.isdir(int_dir)
    found_skills = []
    for root, dirs, files in os.walk(int_dir):
        for d in dirs:
            if os.path.isfile(os.path.join(root, d, "SKILL.md")):
                found_skills.append(d)
    assert len(found_skills) == 8
    assert "dex-api-mocking-virtualization" in found_skills
    assert "dex-binary-inspection" in found_skills
    assert "dex-javascript-bundle-deobfuscation" in found_skills
    assert "dex-rea-adapter" in found_skills
    assert "dex-ui-ux-pro-max-adapter" in found_skills
    assert "dex-supabase-adapter" in found_skills
    assert "dex-superpowers-adapter" in found_skills
    assert "dex-mattpocock-adapter" in found_skills

def test_master_orchestrator_exists():
    """Verify dex-master-orchestrator is present."""
    assert "dex-master-orchestrator" in ALL_SKILLS

@pytest.mark.parametrize("skill_name", ALL_SKILLS)
def test_skill_structure(skill_name):
    """Verify each skill has valid directory, SKILL.md, frontmatter, and 14 sections."""
    skill_path = os.path.join(SKILLS_DIR, skill_name, "SKILL.md")
    assert os.path.isfile(skill_path), f"SKILL.md missing for {skill_name}"

    with open(skill_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert content.strip(), f"SKILL.md is empty for {skill_name}"
    assert content.startswith("---"), f"SKILL.md does not start with --- frontmatter for {skill_name}"

    parts = content.split("---", 2)
    assert len(parts) >= 3, f"SKILL.md has malformed frontmatter delimiters for {skill_name}"

    fm_text = parts[1]
    body = parts[2]

    # Frontmatter key checks
    assert "name:" in fm_text, f"Missing 'name:' in frontmatter of {skill_name}"
    assert "description:" in fm_text, f"Missing 'description:' in frontmatter of {skill_name}"

    # Name matching
    name_match = re.search(r"^name:\s*(.*)$", fm_text, re.MULTILINE)
    assert name_match, f"Unable to extract name from frontmatter in {skill_name}"
    fm_name = name_match.group(1).strip()
    assert fm_name == skill_name, f"Frontmatter name '{fm_name}' != folder '{skill_name}'"
    assert len(fm_name) <= 64, f"Skill name exceeds 64 chars ({len(fm_name)})"
    assert re.match(r"^[a-z0-9-]+$", fm_name), f"Invalid chars in skill name: {fm_name}"

    # Description length check
    desc_match = re.search(r"^description:\s*(.*?)(?=\n[a-z_]+:|\Z)", fm_text, re.DOTALL | re.MULTILINE)
    assert desc_match, f"Unable to extract description in {skill_name}"
    desc = desc_match.group(1).strip()
    assert len(desc) <= 1024, f"Description in {skill_name} exceeds 1024 characters ({len(desc)})"
    assert len(desc) > 20, f"Description in {skill_name} too short ({len(desc)})"

    # 14 Mandatory sections
    section_pattern = re.compile(r"^##\s+(\d+)\.\s*(.*?)$", re.MULTILINE)
    matches = list(section_pattern.finditer(body))
    found_nums = {int(m.group(1)): m.group(2).strip() for m in matches}

    for num, aliases in MANDATORY_SECTIONS:
        assert num in found_nums, f"{skill_name}: Missing mandatory section '## {num}'"
        actual_title = found_nums[num]
        assert any(alias in actual_title.lower() or actual_title.lower() in alias for alias in aliases), \
            f"{skill_name}: Section {num} title mismatch: expected one of {aliases}, got '{actual_title}'"
