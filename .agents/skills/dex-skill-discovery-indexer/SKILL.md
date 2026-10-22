---
name: dex-skill-discovery-indexer
description: Discover, parse, validate, and index Agent Skills across local and remote repositories, generating structured catalogs and searchable capability manifests. Use to catalog available skills across large multi-repo ecosystems.
---

# dex-skill-discovery-indexer

## 1. Purpose & Scope
Khám phá, phân tích cú pháp, thẩm định tính hợp lệ và lập chỉ mục cho các kỹ năng AI Agent (Agent Skills Discovery & Indexing); quét qua các kho lưu trữ cục bộ và từ xa, trích xuất siêu dữ liệu YAML Frontmatter, phân loại thẻ chức năng và tự động sinh ra các danh mục tìm kiếm máy đọc được (Machine-readable Catalogs & Manifests) theo chuẩn Agent Skills Specification.

## 2. When to Use
- Số lượng skills trong hệ thống vượt quá 50 skills và cần xây dựng danh mục tìm kiếm tập trung.
- Tích hợp các kho kỹ năng mới từ cộng đồng mã nguồn mở vào hệ sinh thái của tổ chức.
- Cần tự động hóa việc cập nhật tài liệu `SKILLS_INDEX.md` và `manifests/dex-skills.json` khi có kỹ năng mới được thêm vào.

## 3. When NOT to Use
- Không tự ý kích hoạt hoặc thực thi mã nguồn bên trong skill chỉ vì nó vừa được quét thấy trong quá trình discovery.
- Không nhập các thư mục không chứa file `SKILL.md` hợp lệ.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Đường dẫn thư mục gốc chứa các skills (`.agents/skills/` hoặc `integrations/`).
- Chuẩn đặc tả Agent Skills (`agentskills.io/specification`).
- Các quy tắc lọc và phân loại nhóm chức năng (Groups A–T).
- **Điều kiện tiên quyết**:
- Có công cụ phân tích cú pháp Markdown và YAML không phụ thuộc thư viện ngoài cồng kềnh.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Agent Skills Manifest Schema: File `manifests/dex-skills.json` lưu trữ thông tin chuẩn hóa của từng skill bao gồm: `id`, `name`, `description`, `version`, `category`, `path`, `tags`, `dependencies`.
- Frontmatter Parser Resilience: Bộ bóc tách phải có khả năng xử lý an toàn các file Markdown có hoặc không có Frontmatter mà không bị crash.
- Multi-Source Indexing: Phân biệt rành mạch giữa các Native Skills của hệ thống và các Segregated Third-Party Skills trong bản kê.
- **Quy tắc quyết định kỹ thuật**:
- Bất kỳ thư mục nào thiếu file `SKILL.md` hoặc có `name` trong frontmatter không khớp với tên thư mục phải bị gắn cờ cảnh báo (Warning) và loại khỏi manifest chính thức.
- Tự động sinh chỉ mục tìm kiếm theo từ khóa ngữ nghĩa để phục vụ việc định tuyến (Routing).
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- File `SKILL.md` bị lỗi cú pháp YAML làm dừng đột ngột toàn bộ tiến trình quét của cả kho lưu trữ.

## 6. Step-by-Step Execution Workflow
1. Quét đệ quy toàn bộ các thư mục trong cây thư mục được chỉ định.
2. Đọc và phân tích cú pháp file `SKILL.md` của từng skill.
3. Kiểm tra tính hợp lệ của frontmatter (`name`, `description`).
4. Phân loại skill vào nhóm nghiệp vụ tương ứng dựa trên tiền tố hoặc thẻ cấu hình.
5. Xuất file manifest tổng hợp `manifests/dex-skills.json` và cập nhật bảng `SKILLS_INDEX.md`.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```python
# Trích xuất và lập chỉ mục Agent Skills tự động
import os, yaml

def index_agent_skills(skills_root: str) -> list[dict]:
    catalog = []
    for entry in sorted(os.listdir(skills_root)):
        skill_path = os.path.join(skills_root, entry, "SKILL.md")
        if os.path.isfile(skill_path):
            with open(skill_path, "r", encoding="utf-8") as f:
                content = f.read()
            fm = parse_yaml_frontmatter(content)
            if fm and fm.get("name") == entry:
                catalog.append({
                    "id": entry,
                    "name": fm.get("name"),
                    "description": fm.get("description"),
                    "version": fm.get("version", "5.0.0"),
                    "path": f".agents/skills/{entry}/SKILL.md"
                })
    return catalog
```

### Lệnh xác minh & thực thi:
```bash
# Chạy công cụ khám phá và lập chỉ mục danh mục skills
python scripts/discover_skills.py --output manifests/dex-skills.json
```

## 8. Anti-Patterns & Common Traps
- Cập nhật danh mục `SKILLS_INDEX.md` bằng tay dẫn đến sai lệch đường dẫn hoặc quên cập nhật khi thêm skill mới.
- Cho phép trùng lặp `name` giữa các skills khác nhau trong cùng một manifest.

## 9. Quality Gates & Acceptance Criteria
- Lập chỉ mục thành công 100% các skills hợp lệ mà không có lỗi parse nào.
- File manifest sinh ra phải tuân thủ đúng định dạng JSON Schema chuẩn.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Quá trình index chỉ đọc dữ liệu thụ động, tuyệt đối không cấp quyền thực thi (execution permission) cho các script được tìm thấy.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ thống An ninh & SkillOps**: Tương thích GitHub Actions, SARIF, CycloneDX/SPDX, Semgrep, OWASP ZAP.

## 12. Deliverables & Output Artifacts
- File kê khai máy đọc được `manifests/dex-skills.json`.
- Bảng mục lục cập nhật tự động `SKILLS_INDEX.md`.

## 13. Related & Complementary Skills
dex-skill-semantic-deduplication, dex-skill-license-provenance, dex-skill-security-screening

## 14. Realistic Usage Example
### Tình huống thực tế:
Một tổ chức phát triển kho kỹ năng AI với hơn 200 skills khác nhau. Mỗi khi có kỹ sư đóng góp một skill mới qua PR, công cụ Discovery Indexer tự động quét kiểm tra tính hợp lệ của metadata, gán nhãn nhóm chức năng và cập nhật tự động bảng mục lục toàn hệ thống trong vòng 2 giây tại CI pipeline.
