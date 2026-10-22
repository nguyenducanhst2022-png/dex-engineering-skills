---
name: dex-skill-host-adapters
description: Adapt, negotiate capabilities, and transform Agent Skills for seamless execution across different AI coding hosts (OpenAI Codex, Claude Desktop, Cursor, Copilot Workspace). Use when ensuring universal host interoperability.
---

# dex-skill-host-adapters

## 1. Purpose & Scope
Thiết kế, chuyển đổi và điều đình năng lực kỹ thuật (Capability Negotiation & Transformation) của Agent Skills để có thể tương thích và vận hành mượt mà trên nhiều nền tảng AI Coding Agents khác nhau (OpenAI Codex, Claude Desktop, Cursor, GitHub Copilot Workspace, Windsurf); tự động điều chỉnh cấu trúc thư mục, định dạng chỉ dẫn và cơ chế gọi công cụ phù hợp với từng host mà không làm thay đổi bản chất nội dung chuyên môn.

## 2. When to Use
- Triển khai bộ kỹ năng DEX cho các đội ngũ sử dụng nhiều công cụ AI khác nhau trong cùng một công ty (ví dụ: một nhóm dùng Cursor, một nhóm dùng Claude Desktop, một nhóm dùng OpenAI Codex CLI).
- Host mục tiêu có các quy ước thư mục khác nhau (như `.cursor/rules/`, `.github/copilot-instructions.md`, hoặc `.agents/skills/`).
- Cần xuất bộ kỹ năng sang định dạng plugin tương thích cho một nền tảng mới.

## 3. When NOT to Use
- Không tạo ra các bản copy trùng lặp nội dung cho từng host (phải sử dụng một nguồn sự thật duy nhất `Single Source of Truth` và dùng adapter tự động sinh ra cấu hình cho từng host).
- Không giả định mọi host đều hỗ trợ đầy đủ các tính năng nâng cao như Tool Calling hoặc Terminal Execution.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Cấu trúc chuẩn của bộ kỹ năng (`.agents/skills/`).
- Nền tảng host mục tiêu (Target Host: `codex`, `claude`, `cursor`, `copilot`).
- Bảng ánh xạ tính năng của host (Host Capabilities Matrix: Filesystem, Terminal, Subagents, MCP).
- **Điều kiện tiên quyết**:
- Các kỹ năng gốc tuân thủ đầy đủ chuẩn Agent Skills Specification.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Universal Agent Skills Standard: Bộ kỹ năng được lưu trữ theo đặc tả chuẩn quốc tế tại `.agents/skills/<skill-name>/SKILL.md`. Đây là định dạng trung lập không phụ thuộc vào bất kỳ nhà cung cấp độc quyền nào.
- Capability Negotiation: Adapter kiểm tra xem host hiện tại có hỗ trợ công cụ cần thiết không. Nếu host không hỗ trợ chạy shell (như một số web chat thông thường), adapter tự động chuyển chế độ sang hướng dẫn người dùng tự copy lệnh chạy thủ công thay vì cố gắng gọi tool tự động.
- Host Target Transformers:
  + Cursor Adapter: Xuất các quy tắc kích hoạt thành các file `.cursorrules` hoặc `.cursor/rules/*.mdc`.
  + Claude Desktop Adapter: Đăng ký kỹ năng qua cấu hình MCP Server hoặc Project Instructions.
  + OpenAI Codex Adapter: Tương thích bản địa trực tiếp với thư mục `.agents/skills/`.
- **Quy tắc quyết định kỹ thuật**:
- Nếu host mục tiêu không hỗ trợ MCP: tự động chuyển các mô tả tool thành tài liệu hướng dẫn API tĩnh.
- Quá trình xuất adapter phải là quy trình một chiều tự động (Build artifact), tuyệt đối không sửa đổi file gốc.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Cố gắng gọi tool tự động trên một host chỉ hỗ trợ chat văn bản thuần túy, khiến cuộc hội thoại bị đứt gãy do lỗi không tìm thấy tool.

## 6. Step-by-Step Execution Workflow
1. Xác định danh sách các AI hosts cần hỗ trợ trong tổ chức.
2. Phân tích ma trận năng lực của từng host (Hỗ trợ Tool? Hỗ trợ File? Hỗ trợ Shell?).
3. Xây dựng script chuyển đổi (Adapter script) đọc từ `.agents/skills/`.
4. Sinh ra các cấu hình tương thích cho từng môi trường (ví dụ xuất ra `.cursor/rules/`).
5. Kiểm thử thực tế trên từng host để chứng minh kỹ năng được kích hoạt và hoạt động chính xác.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```python
# Adapter chuyển đổi DEX Skills sang Cursor MDC Rules
import os

def export_to_cursor_rules(skills_dir: str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    for skill_name in os.listdir(skills_dir):
        skill_file = os.path.join(skills_dir, skill_name, "SKILL.md")
        if os.path.isfile(skill_file):
            with open(skill_file, "r", encoding="utf-8") as f:
                content = f.read()
            # Chuyển đổi sang định dạng Cursor Rule có globs
            cursor_rule_content = f"---\ndescription: {skill_name}\nglobs: *\n---\n\n{content}"
            out_path = os.path.join(output_dir, f"{skill_name}.mdc")
            with open(out_path, "w", encoding="utf-8") as out:
                out.write(cursor_rule_content)
```

### Lệnh xác minh & thực thi:
```bash
# Chạy adapter kiểm tra khả năng tương thích đa nền tảng host
python scripts/test_host_compatibility.py --hosts codex,cursor,claude
```

## 8. Anti-Patterns & Common Traps
- Viết mã nguồn kỹ năng phụ thuộc cứng vào các API độc quyền của một công cụ AI duy nhất.
- Sửa đổi thủ công các file đích của từng host khiến tài liệu bị phân mảnh và không đồng bộ.

## 9. Quality Gates & Acceptance Criteria
- 100% kỹ năng tương thích hoàn toàn trên môi trường chuẩn OpenAI Codex và Agent Skills CLI.
- Script Adapter xuất cấu hình cho Cursor và Claude hoàn thành trong dưới 5 giây.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Adapter không được phép làm rò rỉ các secrets hoặc thông tin môi trường nội bộ vào các file cấu hình xuất ra ngoài.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ thống An ninh & SkillOps**: Tương thích GitHub Actions, SARIF, CycloneDX/SPDX, Semgrep, OWASP ZAP.

## 12. Deliverables & Output Artifacts
- Bộ kịch bản chuyển đổi Host Adapters trong `scripts/`.
- Tài liệu hướng dẫn cấu hình chi tiết cho từng nền tảng AI phổ biến.

## 13. Related & Complementary Skills
dex-mcp-server-design, dex-skill-discovery-indexer, dex-master-orchestrator

## 14. Realistic Usage Example
### Tình huống thực tế:
Một công ty phần mềm có đội Backend dùng OpenAI Codex trên VS Code, trong khi đội Frontend dùng Cursor. Thay vì phải bảo trì hai bộ tài liệu kỹ năng riêng biệt, họ duy trì một kho DEX Skills chuẩn duy nhất tại `.agents/skills/` và dùng Host Adapter tự động sinh ra các file `.cursor/rules/` trong tiến trình build, giúp cả hai đội ngũ đều được tận hưởng tri thức kỹ thuật chuẩn mực như nhau.
