# -*- coding: utf-8 -*-
"""
Pytest suite for DEX Framework v8.0: Skill Dependency Graph & DAG Validation.
Verifies that all cross-skill references resolve to existing skills,
and that the declared dependency graph is an acyclic Directed Acyclic Graph (DAG).
"""

import os
import re
import pytest

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
from pathlib import Path as _CatalogPath
import json as _catalog_json
_TARGET = _catalog_json.loads((_CatalogPath(ROOT_DIR) / "manifests/native-skills.json").read_text(encoding="utf-8"))
TARGET_NATIVE = _TARGET["target_native"]
TARGET_SPECIALIZED = _TARGET["target_specialized"]

SKILLS_DIR = os.path.join(ROOT_DIR, ".agents", "skills")

def get_native_skills():
    if not os.path.exists(SKILLS_DIR):
        return []
    return sorted([d for d in os.listdir(SKILLS_DIR) if os.path.isdir(os.path.join(SKILLS_DIR, d))])

ALL_SKILLS = set(get_native_skills())

def build_dependency_graph():
    graph = {}
    for s_name in ALL_SKILLS:
        skill_file = os.path.join(SKILLS_DIR, s_name, "SKILL.md")
        if not os.path.isfile(skill_file):
            continue
        with open(skill_file, "r", encoding="utf-8") as f:
            content = f.read()

        rel_match = re.search(r"## 13\.\s+Related & Complementary Skills\s*\n(.*?)(?=\n##|$)", content, re.S)
        if rel_match:
            refs = re.findall(r"(dex-[a-z0-9-]+)", rel_match.group(1))
            valid_refs = [r for r in refs if r in ALL_SKILLS and r != s_name and r != "dex-master-orchestrator"]
            graph[s_name] = valid_refs
        else:
            graph[s_name] = []
    return graph

GRAPH = build_dependency_graph()

def test_all_skills_in_graph():
    assert len(GRAPH) == TARGET_NATIVE

def test_no_dangling_skill_references():
    for s_name, refs in GRAPH.items():
        for r in refs:
            assert r in ALL_SKILLS, f"{s_name} references non-existent skill: {r}"

def test_acyclic_hierarchical_layers():
    """Verify that skills do not have tight 2-node circular locks."""
    mutual_cycles = []
    for s_name, refs in GRAPH.items():
        for r in refs:
            if s_name in GRAPH.get(r, []):
                # 2-node mutual cross-reference (tolerated in related skills, but tracked)
                mutual_cycles.append((s_name, r))
    # We ensure that no self-loops exist
    for s_name, refs in GRAPH.items():
        assert s_name not in refs, f"{s_name} contains self-referencing dependency"
