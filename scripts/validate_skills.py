# -*- coding: utf-8 -*-
"""
Validation script for DEX Engineering Skills Framework v5.0.
Verifies all 201 Native DEX Skills (200 Specialized Skills + 1 Master Orchestrator)
and segregated upstream integration skills against the Agent Skills Specification
and strict 14-section requirements.
"""

import os
import sys
import re
import json

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

def parse_frontmatter(content):
    """Extracts yaml frontmatter key-values without external dependencies."""
    if not content.startswith("---"):
        return None, "File does not start with ---"
    
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None, "Malformed frontmatter delimiters"
    
    fm_text = parts[1].strip()
    data = {}
    lines = fm_text.splitlines()
    current_key = None
    current_val = []

    for line in lines:
        if ":" in line and not line.startswith(" ") and not line.startswith("\t"):
            if current_key:
                data[current_key] = "\n".join(current_val).strip()
            k, v = line.split(":", 1)
            current_key = k.strip()
            current_val = [v.strip()]
        elif current_key:
            current_val.append(line.strip())
            
    if current_key:
        data[current_key] = " ".join(current_val).strip()

    return data, parts[2]

def validate_skill(skill_dir, skill_name):
    errors = []
    skill_file = os.path.join(skill_dir, "SKILL.md")
    
    if not os.path.exists(skill_file):
        return [f"SKILL.md missing in {skill_name}"]
    
    with open(skill_file, "r", encoding="utf-8") as f:
        content = f.read()

    if not content.strip():
        return [f"{skill_name}: SKILL.md is empty"]

    # 1. Frontmatter validation
    fm, body = parse_frontmatter(content)
    if fm is None:
        return [f"{skill_name}: {body}"]

    name = fm.get("name")
    desc = fm.get("description")

    if not name:
        errors.append(f"{skill_name}: Missing 'name' in frontmatter")
    elif name != skill_name:
        errors.append(f"{skill_name}: Frontmatter name '{name}' does not match directory name '{skill_name}'")
    elif len(name) > 64:
        errors.append(f"{skill_name}: Name exceeds 64 characters ({len(name)})")
    elif not re.match(r"^[a-z0-9-]+$", name):
        errors.append(f"{skill_name}: Name must be lowercase alphanumeric and hyphens")

    if not desc:
        errors.append(f"{skill_name}: Missing 'description' in frontmatter")
    elif len(desc) > 1024:
        errors.append(f"{skill_name}: Description exceeds 1024 characters ({len(desc)})")

    # 2. Section validation
    section_pattern = re.compile(r"^##\s+(\d+)\.\s*(.*?)$", re.MULTILINE)
    matches = list(section_pattern.finditer(body))
    
    found_sections = {}
    for i, match in enumerate(matches):
        num = int(match.group(1))
        header = match.group(2).strip()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        sec_content = body[start:end].strip()
        found_sections[num] = (header, sec_content)

    for num, expected_title in MANDATORY_SECTIONS:
        if num not in found_sections:
            errors.append(f"{skill_name}: Missing mandatory section '## {num}. {expected_title}'")
        else:
            header, text = found_sections[num]
            if expected_title.lower() not in header.lower() and header.lower() not in expected_title.lower():
                errors.append(f"{skill_name}: Section {num} title mismatch: expected '{expected_title}', got '{header}'")
            if not text:
                errors.append(f"{skill_name}: Section {num} '{header}' has no content (empty section)")

    return errors

def main():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    skills_base = os.path.join(root_dir, ".agents", "skills")
    integrations_base = os.path.join(root_dir, "integrations")

    print("=== DEX ENGINEERING SKILLS FRAMEWORK v5.0 SPECIFICATION VALIDATOR ===")
    print(f"Scanning native skills in: {skills_base}")

    if not os.path.exists(skills_base):
        print(f"ERROR: Skills base directory not found at {skills_base}")
        sys.exit(1)

    skill_dirs = [d for d in os.listdir(skills_base) if os.path.isdir(os.path.join(skills_base, d))]
    print(f"Native skill directories found: {len(skill_dirs)}")

    EXPECTED_NATIVE_COUNT = 201
    if len(skill_dirs) != EXPECTED_NATIVE_COUNT:
        print(f"ERROR: Expected exactly {EXPECTED_NATIVE_COUNT} native skills (200 specialized + 1 orchestrator), but found {len(skill_dirs)}.")

    total_errors = 0
    passed_skills = 0

    # 1. Validate Native DEX Skills
    for s_name in sorted(skill_dirs):
        s_path = os.path.join(skills_base, s_name)
        errs = validate_skill(s_path, s_name)
        if errs:
            print(f"\n[FAIL] {s_name}:")
            for e in errs:
                print(f"  - {e}")
            total_errors += len(errs)
        else:
            passed_skills += 1

    # 2. Validate Segregated Integrations
    integration_passed = 0
    integration_total = 0
    if os.path.exists(integrations_base):
        print(f"\nScanning segregated integrations in: {integrations_base}")
        for root, dirs, files in os.walk(integrations_base):
            for d in sorted(dirs):
                skill_path = os.path.join(root, d)
                if os.path.isfile(os.path.join(skill_path, "SKILL.md")):
                    integration_total += 1
                    errs = validate_skill(skill_path, d)
                    if errs:
                        print(f"\n[FAIL INTEGRATION] {d}:")
                        for e in errs:
                            print(f"  - {e}")
                        total_errors += len(errs)
                    else:
                        integration_passed += 1

    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY:")
    print(f"  Native DEX Skills (200 + 1) : {passed_skills} / {len(skill_dirs)} PASSED")
    print(f"  Segregated Integrations     : {integration_passed} / {integration_total} PASSED")
    print(f"  Total Errors                : {total_errors}")
    print("=" * 60)

    if total_errors > 0 or passed_skills != EXPECTED_NATIVE_COUNT:
        print("\nRESULT: FAILED")
        sys.exit(1)
    else:
        print(f"\nRESULT: 100% PASSED - ALL {passed_skills} NATIVE DEX SKILLS & {integration_passed} INTEGRATIONS FULLY VALIDATED!")
        sys.exit(0)

if __name__ == "__main__":
    main()

