---
name: dex-skill-upgrade-migrations
description: Orchestrate automated breaking change migrations for Agent Skills across framework versions, transforming deprecated frontmatter schemas, section reorganizations, and API adapters with compatibility shims. Use when upgrading skill packs across major versions (e.g., v5 to v6).
---

# dex-skill-upgrade-migrations

## 1. Purpose & Scope
Điều phối quy trình di chuyển và nâng cấp kỹ năng tự động khi có thay đổi phá vỡ (Breaking Change Migrations) giữa các phiên bản framework lớn; tự động chuyển đổi cấu trúc YAML Frontmatter lỗi thời, tái cấu trúc các đề mục bắt buộc và cung cấp các lớp tương thích chuyển tiếp (Compatibility Shims); đảm bảo quá trình nâng cấp kho kỹ năng diễn ra trơn tru mà không làm gián đoạn các luồng làm việc sẵn có.

## 2. When to Use
- Khi nâng cấp DEX Skills Framework từ phiên bản v5.0 lên v6.0 với các yêu cầu chuẩn hóa mới.
- Khi đặc tả Agent Skills quốc tế (`agentskills.io/specification`) bổ sung thêm các trường siêu dữ liệu bắt buộc mới.
- Khi cần tự động hóa việc định dạng lại hàng trăm tệp `SKILL.md` theo quy chuẩn mới.

## 3. When NOT to Use
- Khi chỉ sửa nội dung câu chữ nhỏ không làm thay đổi cấu trúc lược đồ.
- Khi di chuyển cơ sở dữ liệu quan hệ khách hàng.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Lược đồ cũ và lược đồ mới của tệp `SKILL.md`, kịch bản chuyển đổi tự động (Migration Script), bản sao lưu dự phòng Git.
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; bảo vệ toàn vẹn tài sản kỹ nghệ và dữ liệu sản xuất.

## 5. Core Concepts & Taxonomy
- **Automated AST-Based Migration:** Phân tích cú pháp Markdown thành cây cú pháp trừu tượng (AST), sửa đổi các nút cần thiết và xuất lại văn bản mà không làm mất định dạng gốc.
- **Deprecation Shims:** Cung cấp các alias tạm thời cho các kỹ năng đã đổi tên để các quy trình cũ vẫn hoạt động trong thời gian chuyển đổi.
- **Two-Phase Migration:** Giai đoạn 1 đánh dấu cảnh báo lỗi thời (Deprecation Warning), Giai đoạn 2 mới chính thức loại bỏ hoặc chuyển đổi hoàn toàn.

## 6. Step-by-Step Execution Workflow
1. Tạo một nhánh Git mới dành riêng cho việc nâng cấp phiên bản (`feat/dex-upgrade`).
2. Quét toàn bộ các tệp `SKILL.md` và nhận diện các phần tử thuộc cấu trúc cũ cần chuyển đổi.
3. Chạy script di chuyển tự động để tái cấu trúc lại các phần mục và frontmatter.
4. Chạy lại toàn bộ bộ kiểm thử xác thực `validate_skills.py` để đảm bảo 100% kỹ năng đáp ứng chuẩn mới.
5. Lập biên bản báo cáo nâng cấp di chuyển `UPGRADE_MIGRATION_REPORT.md`.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```python
# Skill Frontmatter & Section Migration Runner
def migrate_skill_to_v6(skill_md_content: str) -> str:
    # 1. Update frontmatter version if present
    # 2. Ensure all 14 mandatory sections exist
    # 3. Standardize section headers to English canonical format
    headers_map = {
        "## 1. Mục đích": "## 1. Purpose & Scope",
        "## 2. Khi nào sử dụng": "## 2. When to Use",
        "## 3. Khi nào không sử dụng": "## 3. When NOT to Use",
        # ...
    }
    updated_content = skill_md_content
    for old_h, new_h in headers_map.items():
        updated_content = updated_content.replace(old_h, new_h)

    return updated_content
```

## 8. Anti-Patterns & Common Traps
- Thực hiện thay đổi phá vỡ cấu trúc kỹ năng trên nhánh `main` mà không có nhánh thử nghiệm và kiểm thử hồi quy.
- Ép buộc người dùng phải tự sửa đổi bằng tay hàng trăm file `SKILL.md` thay vì cung cấp công cụ nâng cấp tự động.
- Xóa bỏ ngay lập tức các kỹ năng cũ mà không có giai đoạn cảnh báo và shims chuyển tiếp.

## 9. Quality Gates & Acceptance Criteria
- QG-01: 100% các kỹ năng được chuyển đổi thành công sang cấu trúc mới mà không bị mất mát nội dung.
- QG-02: Bộ kiểm tra hợp lệ `validate_skills.py` đạt 100% PASSED sau khi chạy quy trình migration.
- QG-03: Có sẵn hướng dẫn nâng cấp chi tiết cho người dùng trong tài liệu `CHANGELOG.md`.

## 10. Security & Safety Boundaries
- Kiểm tra kỹ lưỡng các kịch bản di chuyển để đảm bảo không vô tình làm lộ hoặc xóa bỏ các cấu hình bảo mật quan trọng của kỹ năng.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Script tự động hóa di chuyển kỹ năng `scripts/migrate_skills_v6.py`.
1. Báo cáo chi tiết quá trình nâng cấp di chuyển `UPGRADE_MIGRATION_REPORT.md`.

## 13. Related & Complementary Skills
- [`dex-schema-evolution`](.agents/skills/dex-schema-evolution/SKILL.md)
- [`dex-skill-retirement-governance`](.agents/skills/dex-skill-retirement-governance/SKILL.md)
- [`dex-skill-rollback-verification`](.agents/skills/dex-skill-rollback-verification/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Nâng cấp toàn bộ hệ thống DEX Skills lên phiên bản v6.0 với 14 đề mục tiếng Anh chuẩn hóa. Kỹ sư kích hoạt `dex-skill-upgrade-migrations`, chạy script tự động duyệt qua toàn bộ 301 kỹ năng, chuẩn hóa cấu trúc và bảo toàn nội dung chuyên môn tiếng Việt phong phú, hoàn thành nâng cấp trong 5 phút với 0 lỗi cú pháp.
