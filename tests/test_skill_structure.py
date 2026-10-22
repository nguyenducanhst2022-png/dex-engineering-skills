# -*- coding: utf-8 -*-
"""
Pytest suite for DEX Engineering Skills Pack v3.0: Structural Verification.
Validates that all skills (91 Native + Imported Upstream Skills) adhere strictly
to Agent Skills Specification and contain the 14 mandatory sections with valid YAML frontmatter.
"""

import os
import re
import json
import pytest

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SKILLS_DIR = os.path.join(ROOT_DIR, ".agents", "skills")

MANDATORY_SECTIONS = [
    (1, "Purpose & Scope"),
    (2, "When to Use"),
    (3, "When NOT to Use"),
    (4, "Prerequisites & Input Context"),
    (5, "Core Concepts & Taxonomy"),
    (6, "Step-by-Step Execution Workflow"),
    (7, "Concrete Examples"),
    (8, "Anti-Patterns & Common Traps"),
    (9, "Quality Gates & Acceptance Criteria"),
    (10, "Security & Safety Boundaries"),
    (11, "Platform Adapters"),
    (12, "Deliverables & Output Artifacts"),
    (13, "Related & Complementary Skills"),
    (14, "Realistic Usage Example"),
]

def get_all_skills():
    if not os.path.exists(SKILLS_DIR):
        return []
    return sorted([d for d in os.listdir(SKILLS_DIR) if os.path.isdir(os.path.join(SKILLS_DIR, d))])

ALL_SKILLS = get_all_skills()

def test_total_skill_count():
    """Verify skill count matches 91 native + imported manifest skills."""
    manifest_path = os.path.join(ROOT_DIR, "data", "imported_skills_manifest.json")
    imported_count = 0
    if os.path.exists(manifest_path):
        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                imported_count = len(data.get("imported_skills", {}))
        except Exception:
            pass

    expected_count = 91 + imported_count
    assert len(ALL_SKILLS) == expected_count, f"Expected {expected_count} skills, found {len(ALL_SKILLS)}"

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

    for num, expected_title in MANDATORY_SECTIONS:
        assert num in found_nums, f"{skill_name}: Missing mandatory section '## {num}. {expected_title}'"
        actual_title = found_nums[num]
        assert (expected_title.lower() in actual_title.lower() or actual_title.lower() in expected_title.lower()), \
            f"{skill_name}: Section {num} title mismatch: expected '{expected_title}', got '{actual_title}'"
