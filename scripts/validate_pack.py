# -*- coding: utf-8 -*-
"""
DEX ENGINEERING SKILLS FRAMEWORK — VALIDATION RUNNER v6.0.
Delegates to validate_skills.py to enforce the 14-section Agent Skills specification
across all 301 native DEX skills and segregated upstream integrations.
"""

import sys
import os

# Add scripts directory to path
sys.path.insert(0, os.path.dirname(__file__))

import validate_skills

if __name__ == "__main__":
    validate_skills.main()
