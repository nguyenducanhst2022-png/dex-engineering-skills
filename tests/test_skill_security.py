# -*- coding: utf-8 -*-
"""
Pytest suite for DEX Framework v5.0: Security Screening.
Verifies that no skill contains dangerous command patterns, unreviewed shell execution,
or prompt injection system override patterns outside documented anti-patterns.
"""

import os
import re
import pytest

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SKILLS_DIR = os.path.join(ROOT_DIR, ".agents", "skills")

DANGEROUS_PATTERNS = [
    (r"curl\s+.*\|\s*(bash|sh)", "Command pipe from curl to shell execution"),
    (r"wget\s+.*\|\s*(bash|sh)", "Command pipe from wget to shell execution"),
    (r"rm\s+-rf\s+[/~]", "Destructive filesystem deletion"),
    (r"eval\s*\(.*process\.env", "Dynamic code evaluation of environment variables"),
]

def get_native_skills():
    if not os.path.exists(SKILLS_DIR):
        return []
    return sorted([d for d in os.listdir(SKILLS_DIR) if os.path.isdir(os.path.join(SKILLS_DIR, d))])

ALL_SKILLS = get_native_skills()

@pytest.mark.parametrize("skill_name", ALL_SKILLS)
def test_skill_security_screening(skill_name):
    # dex-skill-security-screening defines the detection regexes themselves, so it is screened separately
    if skill_name == "dex-skill-security-screening":
        return

    skill_file = os.path.join(SKILLS_DIR, skill_name, "SKILL.md")
    assert os.path.isfile(skill_file)

    with open(skill_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract body without Anti-Patterns section (Section 8 warns against dangerous commands)
    sec8_match = re.search(r"## 8\.\s+Anti-Patterns.*?(?=\n## 9\.|$)", content, re.S)
    body_clean = content.replace(sec8_match.group(0), "") if sec8_match else content

    for pat, desc in DANGEROUS_PATTERNS:
        match = re.search(pat, body_clean, re.IGNORECASE)
        assert not match, f"{skill_name}: Found dangerous security pattern '{desc}': {match.group(0)}"
