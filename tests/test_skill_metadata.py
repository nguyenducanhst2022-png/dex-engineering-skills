# -*- coding: utf-8 -*-
"""
Pytest suite for DEX Framework v8.0: Metadata Conformance.
Verifies YAML frontmatter, naming constraints, and description lengths
across all 401 native skills in .agents/skills/.
"""

import os
import re
import pytest

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SKILLS_DIR = os.path.join(ROOT_DIR, ".agents", "skills")

def get_native_skills():
    if not os.path.exists(SKILLS_DIR):
        return []
    return sorted([d for d in os.listdir(SKILLS_DIR) if os.path.isdir(os.path.join(SKILLS_DIR, d))])

ALL_SKILLS = get_native_skills()

def test_all_skills_found():
    assert len(ALL_SKILLS) == 401, f"Expected 401 native skills, found {len(ALL_SKILLS)}"

@pytest.mark.parametrize("skill_name", ALL_SKILLS)
def test_frontmatter_metadata_validity(skill_name):
    skill_file = os.path.join(SKILLS_DIR, skill_name, "SKILL.md")
    assert os.path.isfile(skill_file)

    with open(skill_file, "r", encoding="utf-8") as f:
        content = f.read()

    assert content.startswith("---"), f"{skill_name}: Does not start with frontmatter '---'"
    parts = content.split("---", 2)
    assert len(parts) >= 3, f"{skill_name}: Malformed frontmatter delimiters"

    fm = parts[1]
    name_match = re.search(r"^name:\s*(.*?)$", fm, re.MULTILINE)
    assert name_match, f"{skill_name}: Missing 'name' in frontmatter"
    name = name_match.group(1).strip()

    assert name == skill_name, f"{skill_name}: Frontmatter name '{name}' does not match directory '{skill_name}'"
    assert re.match(r"^[a-z0-9-]+$", name), f"{skill_name}: Name contains invalid characters"
    assert len(name) <= 64, f"{skill_name}: Name exceeds 64 characters"

    desc_match = re.search(r"^description:\s*(.*?)(?=\n[a-z_]+:|\Z)", fm, re.DOTALL | re.MULTILINE)
    assert desc_match, f"{skill_name}: Missing 'description' in frontmatter"
    desc = desc_match.group(1).strip()
    assert len(desc) >= 20, f"{skill_name}: Description too short ({len(desc)} chars)"
    assert len(desc) <= 1024, f"{skill_name}: Description exceeds 1024 chars ({len(desc)} chars)"
