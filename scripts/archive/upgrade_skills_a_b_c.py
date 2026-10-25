# -*- coding: utf-8 -*-
"""
Upgrades dex-master-orchestrator and Skills 01-30 (Groups A, B, C)
to strictly adhere to the 14 mandatory sections required by v3.0 specification.
"""

import os
import re

SKILLS_00_30 = [
    # Master Orchestrator
    "dex-master-orchestrator",
    # Group A: Core Engineering (01-10)
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
    # Group B: Software Architecture & AI Agents (11-20)
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
    # Group C: Production Engineering (21-30)
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

def parse_markdown_sections(content):
    """Parses markdown into frontmatter and sections."""
    frontmatter = ""
    body = content
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            frontmatter = parts[1].strip()
            body = parts[2].strip()

    # Find top level title
    title_match = re.search(r"^#\s+(.*)$", body, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else "DEX Skill"

    # Extract sections matching ## [0-9]+\.?\s*(.*)
    section_pattern = re.compile(r"^##\s+(\d+)\.?\s*(.*?)$", re.MULTILINE)
    matches = list(section_pattern.finditer(body))

    sections = {}
    for i, match in enumerate(matches):
        sec_num = match.group(1)
        sec_title = match.group(2).strip()
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        sec_content = body[start:end].strip()
        sections[sec_title.lower()] = {
            "num": sec_num,
            "title": sec_title,
            "content": sec_content
        }

    return frontmatter, title, sections

def find_sec(sections, keywords):
    for k, v in sections.items():
        for kw in keywords:
            if kw in k:
                return v["content"]
    return ""

def upgrade_skill(skill_id, base_dir):
    skill_file = os.path.join(base_dir, skill_id, "SKILL.md")
    if not os.path.exists(skill_file):
        print(f"  [MISSING] {skill_file}")
        return False

    with open(skill_file, "r", encoding="utf-8") as f:
        content = f.read()

    frontmatter, title, sections = parse_markdown_sections(content)

    # If the skill already has all 14 standard sections in the right names, skip or refresh
    # Extract components
    purpose = find_sec(sections, ["purpose"])
    when_to_use = find_sec(sections, ["when to use", "activation"])
    when_not = find_sec(sections, ["when not to use", "when not"])
    inputs = find_sec(sections, ["input", "prerequisite"])
    workflow = find_sec(sections, ["workflow", "procedure"])
    quality_gates = find_sec(sections, ["quality gate", "acceptance"])
    safety = find_sec(sections, ["safety", "security"])
    outputs = find_sec(sections, ["output", "deliverable"])
    related = find_sec(sections, ["related", "recommended"])
    example = find_sec(sections, ["example", "concrete"])
    concepts = find_sec(sections, ["core concept", "taxonomy", "decision rule"])
    anti_patterns_val = find_sec(sections, ["anti-pattern", "trap", "failure scenario"])

    # Fallbacks / enhancements for missing sections in 14-section format
    core_concepts = concepts if concepts else (
        "- **Nguyên tắc cốt lõi**: Tuân thủ triệt để nguyên lý vận hành xác định và ranh giới trách nhiệm của chuẩn Agent Skills.\n"
        "- **Tính nhất quán hệ thống**: Mọi thao tác kỹ thuật phải có thể kiểm chứng độc lập với số liệu rõ ràng.\n"
        "- **Ngăn ngừa hồi quy**: Bất kỳ sửa đổi nào cũng phải bảo vệ tính tương thích ngược và chất lượng đã được nghiệm thu."
    )

    anti_patterns = anti_patterns_val if anti_patterns_val else (
        "- **Anti-Pattern 1**: Bỏ qua các bước xác minh tự động và dựa vào giả định chủ quan.\n"
        "- **Anti-Pattern 2**: Thay đổi diện rộng vượt ngoài phạm vi (Scope Creep) làm mất kiểm soát rủi ro.\n"
        "- **Trap**: Thực hiện thao tác phá hủy hoặc thay đổi trạng thái sản xuất khi chưa qua cổng kiểm duyệt an toàn."
    )

    platform_adapters = (
        "- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.\n"
        "- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.\n"
        "- **CLI & IDE Adapters**: Kích hoạt thông qua terminal hoặc tiện ích mở rộng IDE tương thích (VS Code, Cursor, Windsurf)."
    )

    concrete_examples = example if example else (
        "```bash\n# Lệnh thực thi & kiểm chứng tiêu chuẩn\n"
        f"dex verify --skill {skill_id}\n"
        "```"
    )

    realistic_usage = (
        "### Tình huống triển khai thực tế:\n"
        f"Kỹ sư hoặc AI Agent kích hoạt **{skill_id}** trong dự án.\n"
        "1. Tiếp nhận ngữ cảnh đầu vào và kiểm tra điều kiện tiên quyết tại Mục 4.\n"
        "2. Vận hành tuần tự các bước theo Quy trình tại Mục 6.\n"
        "3. Kiểm chứng đầu ra đối chiếu với Tiêu chuẩn chấp thuận tại Mục 9.\n"
        "4. Bàn giao đầy đủ hiện vật theo Mục 12 và cập nhật tài liệu liên quan."
    )

    # Build the 14-section markdown
    upgraded_body = f"""---
{frontmatter}
---

# {title}

## 1. Purpose & Scope
{purpose if purpose else 'Mục đích và phạm vi hoạt động của kỹ năng.'}

## 2. When to Use
{when_to_use if when_to_use else '- Khi cần áp dụng quy trình chuẩn cho tác vụ này.'}

## 3. When NOT to Use
{when_not if when_not else '- Khi tác vụ thuộc phạm vi chuyên biệt của kỹ năng khác.'}

## 4. Prerequisites & Input Context
{inputs if inputs else '**Đầu vào yêu cầu:** Yêu cầu kỹ thuật và ngữ cảnh kho mã nguồn.'}

## 5. Core Concepts & Taxonomy
{core_concepts}

## 6. Step-by-Step Execution Workflow
{workflow if workflow else 'Quy trình thực thi từng bước.'}

## 7. Concrete Examples
{concrete_examples}

## 8. Anti-Patterns & Common Traps
{anti_patterns}

## 9. Quality Gates & Acceptance Criteria
{quality_gates if quality_gates else '- QG-01: Hoàn thành đầy đủ các tiêu chí kỹ thuật mà không phát sinh lỗi.'}

## 10. Security & Safety Boundaries
{safety if safety else '- Tuân thủ nghiêm ngặt các rào chắn an toàn hệ thống.'}

## 11. Platform Adapters
{platform_adapters}

## 12. Deliverables & Output Artifacts
{outputs if outputs else '- Mã nguồn đã qua kiểm thử và báo cáo xác minh hoàn chỉnh.'}

## 13. Related & Complementary Skills
{related if related else '- `dex-master-orchestrator`: Điều phối trung tâm.'}

## 14. Realistic Usage Example
{realistic_usage}
"""

    with open(skill_file, "w", encoding="utf-8") as f:
        f.write(upgraded_body.strip() + "\n")
    print(f"  [UPGRADED] {skill_id}/SKILL.md")
    return True

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".agents", "skills"))
    print(f"Upgrading dex-master-orchestrator and Skills 01-30 to 14-section format...")

    upgraded_count = 0
    for skill_id in SKILLS_00_30:
        if upgrade_skill(skill_id, base_dir):
            upgraded_count += 1

    print(f"Upgrade complete: {upgraded_count}/{len(SKILLS_00_30)} skills upgraded.")

if __name__ == "__main__":
    main()
