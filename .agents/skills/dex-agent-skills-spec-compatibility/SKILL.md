---
name: dex-agent-skills-spec-compatibility
description: Validate, lint, and certify skill definitions against official Agent Skills specifications (agentskills.io) and emerging open agent standards. Use when certifying skills for cross-platform agent runtime compatibility.
---

# dex-agent-skills-spec-compatibility

## 1. Purpose & Scope
Kiểm chứng, lint và chứng nhận tính tương thích của các định nghĩa kỹ năng theo đúng đặc tả kỹ thuật chuẩn mở Agent Skills (agentskills.io); bảo đảm các kỹ năng có thể hoạt động liền mạch trên OpenAI Codex, Claude Code, Antigravity và các AI Coding Agents khác.

## 2. When to Use
- Khi xây dựng hoặc cập nhật kỹ năng mới và cần xác nhận tuân thủ 100% đặc tả chuẩn mở.
- Khi tích hợp các kỹ năng từ bên thứ ba và muốn kiểm tra tính hợp lệ của YAML frontmatter và cấu trúc file.
- Khi kiểm toán định kỳ toàn bộ kho kỹ năng để chuẩn bị phát hành phiên bản mới.

## 3. When NOT to Use
- Khi viết các kịch bản tự động hóa nội bộ không đóng gói dưới dạng Agent Skill chuẩn.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** File `SKILL.md` của các kỹ năng, schema định nghĩa chuẩn Agent Skills specification.
- **Quyền hạn truy cập:** Quyền đọc và kiểm tra cú pháp file mã nguồn kỹ năng.

## 5. Core Concepts & Taxonomy
- **Agent Skills Specification Standard:** Quy chuẩn quốc tế quy định cấu trúc file `SKILL.md` gồm YAML frontmatter bắt buộc (`name`, `description`) và các tiêu chuẩn nội dung hướng dẫn agent.
- **Mandatory 14 Sections Standard:** Tiêu chuẩn nâng cao của DEX Engineering Skills yêu cầu mỗi kỹ năng phải triển khai đầy đủ 14 phần chuyên biệt từ mục đích, điều kiện kích hoạt, ví dụ mã lệnh đến kiểm thử và chất lượng.
- **Deterministic Header Formatting:** Định dạng tiêu đề Markdown chuẩn xác để parser của các agent có thể bóc tách thông tin một cách tất định.

## 6. Step-by-Step Execution Workflow
1. Đọc và phân tích cú pháp YAML frontmatter của file `SKILL.md`.
2. Xác thực tính hợp lệ của trường `name`: viết thường, phân cách bằng dấu gạch ngang (kebab-case), độ dài tối đa 64 ký tự.
3. Xác thực trường `description`: mô tả rõ ràng mục đích và ngữ cảnh kích hoạt ('Use when...').
4. Kiểm tra sự hiện diện đầy đủ của toàn bộ 14 phần tiêu đề bắt buộc theo đúng quy chuẩn.
5. Kiểm tra tính hợp lệ của các khối mã lệnh (Code Blocks): cú pháp Markdown chuẩn, có chỉ định ngôn ngữ.
6. Cấp chứng chỉ tương thích (Compatibility Certification) cho kỹ năng vượt qua kiểm định.

## 7. Concrete Examples
### Kịch bản kiểm tra tuân thủ đặc tả Agent Skills trong Python:
```python
import re
import yaml

MANDATORY_SECTIONS = [
    "## 1. Purpose & Scope", "## 2. When to Use", "## 3. When NOT to Use",
    "## 4. Prerequisites & Input Context", "## 5. Core Concepts & Taxonomy",
    "## 6. Step-by-Step Execution Workflow", "## 7. Concrete Examples",
    "## 8. Anti-Patterns & Common Traps", "## 9. Quality Gates & Acceptance Criteria",
    "## 10. Security & Safety Boundaries", "## 11. Platform Adapters",
    "## 12. Deliverables & Output Artifacts", "## 13. Related & Complementary Skills",
    "## 14. Realistic Usage Example"
]

def validate_skill_spec(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Kiem tra YAML frontmatter
    assert content.startswith("---"), "Thieu phan mo dau YAML frontmatter (---)"
    parts = content.split("---", 2)
    meta = yaml.safe_load(parts[1])
    
    assert "name" in meta and re.match(r"^[a-z0-9-]+$", meta["name"]), "Field 'name' khong hop le!"
    assert "description" in meta and len(meta["description"]) >= 20, "Field 'description' qua ngan!"
    
    # Kiem tra 14 sections bat buoc
    body = parts[2]
    for sec in MANDATORY_SECTIONS:
        assert sec in body, f"Thieu section bat buoc: {sec}"
        
    print(f"Xac thuc dat chuan: {meta['name']}")
```

## 8. Anti-Patterns & Common Traps
- **Missing Frontmatter Delimiters:** Quên đóng mở dấu `---` khiến parser coi toàn bộ frontmatter là nội dung văn bản thường.
- **Generic Descriptions:** Viết mô tả hời hợt như 'Kỹ năng này dùng để code' khiến AI Agent không thể định tuyến chính xác.
- **Omission of Verification Sections:** Bỏ qua phần kiểm thử và quality gates biến kỹ năng thành tài liệu lý thuyết suông.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: 100% kỹ năng có YAML frontmatter hợp lệ với schema chuẩn Agent Skills.
- **QG-04**: 100% kỹ năng triển khai đầy đủ không thiếu bất kỳ section nào trong 14 phần bắt buộc.
- **QG-07**: Không có lỗi cú pháp Markdown hoặc khối mã không đóng thẻ.

## 10. Security & Safety Boundaries
- Ngăn chặn các cú pháp chèn mã độc vào YAML frontmatter thông qua việc sử dụng hàm nạp an toàn `yaml.safe_load`.

## 11. Platform Adapters
- **Agents**: OpenAI Codex, Anthropic Claude Code, Antigravity, GitHub Copilot Workspace.

## 12. Deliverables & Output Artifacts
- Linter kiểm tra tuân thủ đặc tả kỹ năng tự động.
- Báo cáo chứng nhận mức độ tương thích trên toàn catalog.
- Bộ quy tắc GitHub Actions kiểm tra PR tự động.

## 13. Related & Complementary Skills
dex-skill-catalog-reconciliation, dex-skill-quality-scorecards, dex-instruction-injection-testing

## 14. Realistic Usage Example
```powershell
# Chạy kiểm tra tính tương thích đặc tả trên toàn bộ kỹ năng
python scripts/validate_skills.py

# Chạy test suite kiểm tra metadata bằng pytest
pytest tests/test_skill_metadata.py -v
```
