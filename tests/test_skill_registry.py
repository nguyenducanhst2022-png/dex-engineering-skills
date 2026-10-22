# -*- coding: utf-8 -*-
"""
Pytest suite for DEX Framework v5.0: Skill Registry & Catalog Audit.
Asserts:
- Exactly 200 specialized skills exist.
- Exactly 1 Master Orchestrator exists.
- Exactly 201 native skill directories in .agents/skills/.
- No duplicate names.
- All 20 groups (A to T) contain exactly 10 skills each.
"""

import os
import json
import pytest

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SKILLS_DIR = os.path.join(ROOT_DIR, ".agents", "skills")
MANIFEST_FILE = os.path.join(ROOT_DIR, "manifests", "dex-skills.json")

def test_exact_skill_inventory():
    dirs = [d for d in os.listdir(SKILLS_DIR) if os.path.isdir(os.path.join(SKILLS_DIR, d))]
    assert len(dirs) == 201, f"Expected 201 skill directories, found {len(dirs)}"

    orchestrators = [d for d in dirs if d == "dex-master-orchestrator"]
    assert len(orchestrators) == 1, "Expected exactly 1 Master Orchestrator"

    specialized = [d for d in dirs if d != "dex-master-orchestrator"]
    assert len(specialized) == 200, f"Expected exactly 200 specialized skills, found {len(specialized)}"

    # Check for duplicate names
    assert len(set(dirs)) == 201, "Detected duplicate skill directory names"

def test_manifest_synchronization():
    assert os.path.isfile(MANIFEST_FILE), f"Manifest file missing at {MANIFEST_FILE}"
    with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    native_skills = data.get("native_skills", [])
    assert len(native_skills) == 201, f"Expected 201 native skills in manifest, found {len(native_skills)}"

    # Check group counts: Groups A to T should each have exactly 10 skills
    group_counts = {}
    for s in native_skills:
        grp = s.get("group")
        group_counts[grp] = group_counts.get(grp, 0) + 1

    assert group_counts.get("Root") == 1, "Expected 1 Root Master Orchestrator in manifest"

    expected_groups = [f"Group {chr(c)}" for c in range(ord('A'), ord('T') + 1)]
    for grp in expected_groups:
        count = group_counts.get(grp, 0)
        assert count == 10, f"{grp}: Expected exactly 10 skills, found {count}"

def test_segregated_integrations():
    int_dir = os.path.join(ROOT_DIR, "integrations")
    assert os.path.isdir(int_dir)
    found_skills = []
    for root, dirs, files in os.walk(int_dir):
        for d in dirs:
            if os.path.isfile(os.path.join(root, d, "SKILL.md")):
                found_skills.append(d)

    assert len(found_skills) == 4, f"Expected 4 segregated integration skills, found {len(found_skills)}"
    assert "dex-api-mocking-virtualization" in found_skills
    assert "dex-binary-inspection" in found_skills
    assert "dex-javascript-bundle-deobfuscation" in found_skills
    assert "dex-rea-adapter" in found_skills
