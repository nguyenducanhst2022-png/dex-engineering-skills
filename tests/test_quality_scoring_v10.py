# -*- coding: utf-8 -*-
"""
DEX Framework v10.0 — Test Suite for 100-Point Quality Scoring Engine
Verifies rubric weights, point boundaries, and evidence requirements.
"""

import os
import sys
import json
import pytest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.audit_skills import compute_quality_score


def test_rubric_weights_sum_to_100():
    """Validates that maximum possible points across all 6 dimensions sum to 100."""
    # Mocking a fully verified, perfect skill
    content = "# Mock"
    fm = {"name": "dex-test", "description": "A valid test skill description with adequate length exceeding twenty chars."}
    body = "Content"
    sample_text = "This is a detailed and comprehensive content block that easily exceeds one hundred characters for rigorous testing."
    found_sections = {i: (f"Section {i}", sample_text) for i in range(1, 15)}
    issues = []
    
    score = compute_quality_score("dex-test", content, fm, body, found_sections, issues, runtime_state="VERIFIED")
    
    breakdown = score["breakdown"]
    assert breakdown["functional_correctness"] == 30
    assert breakdown["activation_routing"] == 25
    assert breakdown["technical_precision"] == 15
    assert breakdown["security_safety"] == 10
    assert breakdown["documentation_usability"] == 10
    assert breakdown["maintainability_integration"] == 10
    assert score["total_score"] == 100


def test_not_tested_skill_capped_functional_score():
    """Unverified skills cannot receive 30 points in functional correctness."""
    content = "# Mock"
    fm = {"name": "dex-test", "description": "A valid test skill description with adequate length exceeding twenty chars."}
    body = "Content"
    sample_text = "This is a detailed and comprehensive content block that easily exceeds one hundred characters for rigorous testing."
    found_sections = {i: (f"Section {i}", sample_text) for i in range(1, 15)}
    issues = []
    
    score = compute_quality_score("dex-test", content, fm, body, found_sections, issues, runtime_state="NOT_TESTED")
    assert score["breakdown"]["functional_correctness"] == 15
    assert score["total_score"] <= 85
    assert score["runtime_state"] == "NOT_TESTED"


def test_dangling_references_penalize_maintainability():
    """Skills with dangling references are penalized in maintainability."""
    content = "# Mock"
    fm = {"name": "dex-test", "description": "A valid test skill description with adequate length exceeding twenty chars."}
    body = "Content"
    sample_text = "This is a detailed and comprehensive content block that easily exceeds one hundred characters for rigorous testing."
    found_sections = {i: (f"Section {i}", sample_text) for i in range(1, 15)}
    issues = [{"severity": "LOW", "message": "Dangling reference to unknown skill 'dex-unknown'"}]
    
    score = compute_quality_score("dex-test", content, fm, body, found_sections, issues, runtime_state="NOT_TESTED")
    assert score["breakdown"]["maintainability_integration"] == 5  # Lost 5 pts due to dangling reference


def test_all_501_skills_have_audit_records():
    """Verifies that docs/quality/SKILL_AUDIT_V10.json contains records for all 501 skills."""
    audit_file = ROOT / "docs" / "quality" / "SKILL_AUDIT_V10.json"
    assert audit_file.exists(), "SKILL_AUDIT_V10.json must exist"
    
    with open(audit_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    assert data["total_skills"] == 501
    assert len(data["skills_audit_data"]) == 501
    assert data["critical_issues"] == 0
    assert data["high_issues"] == 0
    assert data["low_issues"] == 0

    # Ensure all scores are between 70 and 100
    for s_name, s_data in data["skills_audit_data"].items():
        score = s_data["quality_score"]
        assert 70 <= score <= 100, f"Skill {s_name} score out of bounds: {score}"
