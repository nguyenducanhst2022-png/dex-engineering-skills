#!/usr/bin/env python3
"""
DEX Engineering Skills Pack — Automated Validation Script
Verifies compliance with the Agent Skills Specification (https://agentskills.io/specification).
Checks:
  - Exact directory and SKILL.md existence (31 skills total: 1 master + 30 specialized).
  - YAML frontmatter format (enclosed in ---, contains name & description).
  - Name constraints: exact match with parent dir, <= 64 chars, regex ^[a-z0-9]+(-[a-z0-9]+)*$.
  - Description constraints: non-empty, <= 1024 chars, describes what and when to use.
  - 10 mandatory content sections present in markdown headers.
  - Real-world practical example section present.
  - Markdown reference link integrity (all relative file links must resolve).
"""

import os
import re
import sys

# Ensure UTF-8 output on Windows consoles
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# Required 31 skills in exact catalog order
EXPECTED_SKILLS = [
    "dex-master-orchestrator",
    "dex-development-workflow",
    "dex-task-delegation",
    "dex-code-verification",
    "dex-git-workflow",
    "dex-code-organization",
    "dex-root-cause-debugging",
    "dex-performance-optimization",
    "dex-security-audit",
    "dex-cicd-automation",
    "dex-release-engineering",
    "dex-production-monitoring",
    "dex-technical-debt-refactoring",
    "dex-software-architecture",
    "dex-database-engineering",
    "dex-api-engineering",
    "dex-testing-engineering",
    "dex-agent-engineering",
    "dex-multi-agent-orchestration",
    "dex-context-engineering",
    "dex-specification-driven",
    "dex-change-impact-analysis",
    "dex-dependency-management",
    "dex-reliability-engineering",
    "dex-concurrency-state",
    "dex-ux-accessibility",
    "dex-feature-flags",
    "dex-code-review",
    "dex-acceptance-testing",
    "dex-software-maintenance",
    "dex-end-to-end-engineering",
]

MANDATORY_SECTIONS = [
    ("1. Purpose", r"##\s*1\.\s*(Purpose|Mục tiêu)"),
    ("2. When to Use", r"##\s*2\.\s*(When to Use|Khi nào kích hoạt|Khi nào dùng)"),
    ("3. When Not to Use", r"##\s*3\.\s*(When Not to Use|Khi nào không nên|Không dùng)"),
    ("4. Inputs", r"##\s*4\.\s*(Inputs|Đầu vào|Ngữ cảnh)"),
    ("5. Workflow", r"##\s*5\.\s*(Workflow|Quy trình)"),
    ("6. Quality Gates", r"##\s*6\.\s*(Quality Gates|Điều kiện kiểm chứng)"),
    ("7. Safety Rules", r"##\s*7\.\s*(Safety Rules|Ràng buộc an toàn)"),
    ("8. Expected Outputs", r"##\s*8\.\s*(Expected Outputs|Kết quả đầu ra)"),
    ("9. Failure Handling", r"##\s*9\.\s*(Failure Handling|Cách xử lý khi thất bại|Xử lý sự cố)"),
    ("10. Completion Criteria", r"##\s*10\.\s*(Completion Criteria|Tiêu chí hoàn thành|Điều kiện hoàn thành)"),
]

NAME_REGEX = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
LINK_REGEX = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def parse_frontmatter(content: str):
    """Extract YAML frontmatter between leading --- delimiters."""
    if not content.startswith("---"):
        return None, "File does not start with YAML frontmatter delimiters ('---')"
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None, "Unclosed YAML frontmatter delimiter ('---')"
    yaml_text = parts[1]
    body = parts[2]

    # Simple regex parsing for name and description without requiring external yaml library
    name_match = re.search(r"^name:\s*([^\r\n]+)", yaml_text, re.MULTILINE)
    # Match description which can be single-line or multi-line
    desc_match = re.search(r"^description:\s*([^\r\n]+(?:\r?\n(?:\s+[^\r\n]+))*?)", yaml_text, re.MULTILINE)

    if not name_match:
        return None, "Missing required frontmatter field: 'name'"
    if not desc_match:
        return None, "Missing required frontmatter field: 'description'"

    name = name_match.group(1).strip().strip("'\"")
    desc = desc_match.group(1).strip().strip("'\"")
    # Clean multi-line indentation in description
    desc = re.sub(r"\s+", " ", desc)

    return {"name": name, "description": desc, "body": body}, None


def validate_skill(skills_root: str, skill_name: str):
    errors = []
    warnings = []

    skill_dir = os.path.join(skills_root, skill_name)
    if not os.path.isdir(skill_dir):
        return {"status": "FAIL", "errors": [f"Skill directory does not exist: {skill_dir}"], "warnings": []}

    skill_file = os.path.join(skill_dir, "SKILL.md")
    if not os.path.isfile(skill_file):
        return {"status": "FAIL", "errors": [f"SKILL.md missing in {skill_dir}"], "warnings": []}

    with open(skill_file, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    # 1. Frontmatter Validation
    fm, err = parse_frontmatter(content)
    if err:
        errors.append(f"Frontmatter error: {err}")
        return {"status": "FAIL", "errors": errors, "warnings": warnings}

    name = fm["name"]
    desc = fm["description"]
    body = fm["body"]

    # 2. Name validation
    if name != skill_name:
        errors.append(f"Name '{name}' does not match parent directory name '{skill_name}'")
    if len(name) > 64:
        errors.append(f"Name '{name}' exceeds 64 characters limit ({len(name)} chars)")
    if not NAME_REGEX.match(name):
        errors.append(f"Name '{name}' violates Agent Skills format: lowercase, numbers, single hyphens only")

    # 3. Description validation
    if not desc:
        errors.append("Description is empty")
    if len(desc) > 1024:
        errors.append(f"Description exceeds 1024 characters limit ({len(desc)} chars)")
    if "use" not in desc.lower() and "sử dụng" not in desc.lower() and "khi" not in desc.lower():
        warnings.append("Description should ideally state when to trigger the skill (e.g., 'Use when...')")

    # 4. Mandatory Sections Validation
    for sec_name, pattern in MANDATORY_SECTIONS:
        if not re.search(pattern, body, re.IGNORECASE):
            errors.append(f"Missing mandatory section: '{sec_name}'")

    # 5. Real-world example validation
    if not re.search(r"##\s*(Real-world Example|Ví dụ thực tế|Example)", body, re.IGNORECASE):
        warnings.append("Missing recommended section: 'Real-world Example'")

    # 6. Reference Links Integrity Check
    for link_text, link_target in LINK_REGEX.findall(body):
        # Ignore web links, anchor links, and mailto
        if link_target.startswith(("http://", "https://", "#", "mailto:")):
            continue
        # Strip query params or anchors from file target
        clean_target = link_target.split("#")[0].split("?")[0]
        if not clean_target:
            continue
        # Target path relative to SKILL.md directory
        target_path = os.path.normpath(os.path.join(skill_dir, clean_target))
        if not os.path.exists(target_path):
            errors.append(f"Broken markdown link: [{link_text}]({link_target}) -> Target not found: {target_path}")

    status = "FAIL" if errors else "PASS"
    return {"status": status, "errors": errors, "warnings": warnings, "name": name, "desc_len": len(desc)}


def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    skills_root = os.path.join(base_dir, ".agents", "skills")

    print("=" * 70)
    print("  DEX ENGINEERING SKILLS PACK — VALIDATION SUITE v1.0")
    print(f"  Target Directory: {skills_root}")
    print("=" * 70)

    if not os.path.isdir(skills_root):
        print(f"\n[FATAL] Skills root directory not found: {skills_root}")
        sys.exit(1)

    results = {}
    pass_count = 0
    fail_count = 0

    for idx, skill in enumerate(EXPECTED_SKILLS, 1):
        res = validate_skill(skills_root, skill)
        results[skill] = res
        if res["status"] == "PASS":
            pass_count += 1
            warn_msg = f" (Warnings: {len(res['warnings'])})" if res["warnings"] else ""
            print(f"[{idx:02d}/31] [PASS] {skill} (Desc: {res.get('desc_len', 0)} chars){warn_msg}")
        else:
            fail_count += 1
            print(f"[{idx:02d}/31] [FAIL] {skill}")
            for err in res["errors"]:
                print(f"       ERROR: {err}")
            for warn in res["warnings"]:
                print(f"       WARN:  {warn}")

    print("\n" + "=" * 70)
    print("  VALIDATION SUMMARY")
    print("=" * 70)
    print(f"  Total Skills Checked : {len(EXPECTED_SKILLS)}")
    print(f"  PASS                 : {pass_count}")
    print(f"  FAIL                 : {fail_count}")
    print(f"  SKIP                 : 0")
    print(f"  NOT VERIFIED         : 0")
    print("=" * 70)

    if fail_count == 0:
        print("\n>>> SUCCESS: 31/31 skills are fully compliant with Agent Skills Specification!\n")
        sys.exit(0)
    else:
        print(f"\n>>> FAILURE: {fail_count} skill(s) failed validation. Please fix errors above.\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
