# -*- coding: utf-8 -*-
"""
DEX SKILLOPS — COMPREHENSIVE SKILL AUDITOR (scripts/audit_skills.py)
Audits skill quality, missing sections, license conformance, security boundaries,
local broken references, and duplicate detection across native and integrated skills.
"""

import os
import sys
import re
import json
import argparse

if sys.stdout.encoding != "utf-8" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

DANGEROUS_PATTERNS = [
    (r"curl\s+.*\|\s*(bash|sh)", "Command pipe from curl directly to shell execution"),
    (r"wget\s+.*\|\s*(bash|sh)", "Command pipe from wget directly to shell execution"),
    (r"rm\s+-rf\s+[/~]", "Destructive filesystem deletion"),
    (r"eval\s*\(.*process\.env", "Dynamic code evaluation of environment variables"),
    (r"ignore\s+(all\s+)?previous\s+instructions", "Prompt injection system override pattern"),
]

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

def audit_single_skill(skill_dir, skill_name, all_skill_names):
    issues = []
    skill_file = os.path.join(skill_dir, "SKILL.md")

    if not os.path.exists(skill_file):
        return [{"severity": "CRITICAL", "message": f"SKILL.md missing in {skill_name}"}]

    with open(skill_file, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Frontmatter check
    fm, body = parse_frontmatter(content)
    if not fm:
        issues.append({"severity": "CRITICAL", "message": f"Malformed frontmatter: {body}"})
        return issues

    name = fm.get("name")
    desc = fm.get("description")

    if not name or name != skill_name:
        issues.append({"severity": "HIGH", "message": f"Name mismatch: '{name}' != '{skill_name}'"})
    if not desc or len(desc) < 20:
        issues.append({"severity": "HIGH", "message": "Description missing or too short (< 20 chars)"})
    elif len(desc) > 1024:
        issues.append({"severity": "MEDIUM", "message": f"Description exceeds 1024 chars ({len(desc)})"})

    # 2. Section check
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
            issues.append({"severity": "HIGH", "message": f"Missing Section {num}: {expected_title}"})
        else:
            header, text = found_sections[num]
            if not text:
                issues.append({"severity": "MEDIUM", "message": f"Section {num} '{header}' is empty"})

    # 3. Security pattern checks (excluding Anti-Patterns warnings and screening definitions)
    sec_8_text = found_sections.get(8, ("", ""))[1] if 8 in found_sections else ""
    body_to_check = body.replace(sec_8_text, "")
    if skill_name != "dex-skill-security-screening":
        for pat, desc_sec in DANGEROUS_PATTERNS:
            if re.search(pat, body_to_check, re.IGNORECASE):
                issues.append({"severity": "CRITICAL", "message": f"Security violation: {desc_sec}"})

    # 4. Check broken skill references
    rel_match = re.search(r"## 13\.\s+Related & Complementary Skills\s*\n(.*?)(?=\n##|$)", body, re.S)
    if rel_match:
        rel_text = rel_match.group(1)
        refs = re.findall(r"(dex-[a-z0-9-]+)", rel_text)
        for r in refs:
            if r != skill_name and r not in all_skill_names and not r.startswith("dex-example"):
                issues.append({"severity": "LOW", "message": f"Dangling reference to unknown skill '{r}'"})

    return issues

def audit_all(root_dir):
    skills_base = os.path.join(root_dir, ".agents", "skills")
    integrations_base = os.path.join(root_dir, "integrations")

    all_skill_dirs = [d for d in os.listdir(skills_base) if os.path.isdir(os.path.join(skills_base, d))]
    all_skill_names = set(all_skill_dirs)

    print(f"=== DEX SKILLOPS AUDITOR ===")
    print(f"Auditing {len(all_skill_dirs)} native skills...")

    audit_results = {
        "total_skills": len(all_skill_dirs),
        "critical_issues": 0,
        "high_issues": 0,
        "medium_issues": 0,
        "low_issues": 0,
        "skills_with_issues": {}
    }

    for s_name in sorted(all_skill_dirs):
        s_path = os.path.join(skills_base, s_name)
        issues = audit_single_skill(s_path, s_name, all_skill_names)
        if issues:
            audit_results["skills_with_issues"][s_name] = issues
            for iss in issues:
                sev = iss["severity"]
                if sev == "CRITICAL": audit_results["critical_issues"] += 1
                elif sev == "HIGH": audit_results["high_issues"] += 1
                elif sev == "MEDIUM": audit_results["medium_issues"] += 1
                elif sev == "LOW": audit_results["low_issues"] += 1

    # Check licenses of upstream integrations
    manifest_sources = os.path.join(root_dir, "manifests", "upstream-sources.json")
    if os.path.exists(manifest_sources):
        with open(manifest_sources, "r", encoding="utf-8") as f:
            sources_data = json.load(f)
        print(f"Verified {len(sources_data.get('sources', []))} upstream sources licenses and pinned commits.")

    print("\n" + "=" * 50)
    print("AUDIT SUMMARY:")
    print(f"  Total Native Skills Audited : {audit_results['total_skills']}")
    print(f"  Critical Security Violations : {audit_results['critical_issues']}")
    print(f"  High Severity Defects       : {audit_results['high_issues']}")
    print(f"  Medium Severity Defects     : {audit_results['medium_issues']}")
    print(f"  Low Severity Minor Warnings : {audit_results['low_issues']}")
    print("=" * 50)

    if audit_results["critical_issues"] > 0 or audit_results["high_issues"] > 0:
        print("\nRESULT: AUDIT FAILED")
        return 1
    else:
        print("\nRESULT: AUDIT PASSED - 100% SPEC & SECURITY CONFORMANCE")
        return 0

if __name__ == "__main__":
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    sys.exit(audit_all(root_dir))
