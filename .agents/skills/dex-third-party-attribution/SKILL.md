---
name: dex-third-party-attribution
description: Generate accurate, legally compliant NOTICE and THIRD_PARTY_NOTICES files, aggregating copyright statements, author credits, and license texts from vendored dependencies. Use when packaging desktop apps, mobile releases, or distributed on-premise appliances.
---

# dex-third-party-attribution

## 1. Purpose & Scope
Tự động hóa việc tổng hợp và xuất bản tệp ghi nhận công lao bên thứ ba (`NOTICE` và `THIRD_PARTY_NOTICES.md`) tuân thủ nghiêm ngặt pháp lý; thu thập đầy đủ tuyên bố bản quyền (Copyright Statements), thông tin tác giả và nguyên văn nội dung giấy phép từ toàn bộ các gói thư viện được đóng gói kèm; phục vụ việc phát hành ứng dụng máy tính, ứng dụng di động hoặc giải pháp phần mềm tại chỗ (On-Premise).

## 2. When to Use
- Trước khi đóng gói phát hành phần mềm phân phối (Desktop/Mobile/CLI) theo yêu cầu bắt buộc của các giấy phép Apache-2.0, MIT và BSD.
- Khi xây dựng trang 'Open Source Licenses' trong mục Cài đặt (Settings) của ứng dụng di động.
- Khi xuất bản thư viện mã nguồn mở ra cộng đồng và cần ghi nhận công lao các thành phần đã sử dụng.

## 3. When NOT to Use
- Khi ứng dụng web nội bộ chỉ chạy trên máy chủ đám mây của chính công ty và không bao giờ phân phối nhị phân cho bên ngoài.
- Khi quản lý danh mục tài sản phần cứng.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Thư mục `node_modules` hoặc kho gói phụ thuộc đã tải đầy đủ, công cụ tự động tổng hợp thông báo (`license-checker` hoặc script Python/Go).
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; bảo vệ toàn vẹn tài sản kỹ nghệ và dữ liệu sản xuất.

## 5. Core Concepts & Taxonomy
- **Mandatory Attribution Clause:** Hầu hết các giấy phép mã nguồn mở (kể cả MIT và Apache 2.0) đều bắt buộc bên phân phối phải đính kèm nguyên văn thông báo bản quyền và nội dung giấy phép trong sản phẩm phân phối.
- **Apache NOTICE Preservation:** Giấy phép Apache 2.0 yêu cầu mọi thông tin ghi nhận trong tệp `NOTICE` của thư viện gốc phải được bảo toàn nguyên vẹn trong tệp `NOTICE` của sản phẩm phái sinh.
- **Multi-Ecosystem Aggregation:** Khả năng thu thập thông báo bản quyền xuyên suốt nhiều hệ sinh thái trong cùng một sản phẩm (npm, PyPI, Cargo, NuGet).

## 6. Step-by-Step Execution Workflow
1. Quét cây phụ thuộc và tìm kiếm toàn bộ các tệp `LICENSE*` và `NOTICE*` trong các gói được đóng gói.
2. Trích xuất dòng bản quyền (ví dụ: `Copyright (c) 2024 Jane Doe`).
3. Gom nhóm và định dạng các thông báo theo từng thành phần rõ ràng kèm đường dẫn kho mã nguồn.
4. Xuất bản tệp chuẩn hóa `THIRD_PARTY_NOTICES.md` ở thư mục gốc của bản dựng phân phối.
5. Kiểm tra tính đầy đủ của thông tin trước khi đóng gói tệp cài đặt (Installer).

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```markdown
# Third-Party Software Notices & Licenses

This distribution includes third-party software components subject to the following licenses:

---

Component: Undici (v6.19.8)
- **License**: Apache-2.0
- **Copyright**: Copyright Node.js contributors. All rights reserved.
- **Repository**: https://github.com/nodejs/undici

```text
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
...
```
```

## 8. Anti-Patterns & Common Traps
- Phân phối tệp cài đặt phần mềm thương mại nhưng không đính kèm tệp `THIRD_PARTY_NOTICES` (vi phạm trực tiếp điều khoản của giấy phép MIT và Apache 2.0).
- Chỉ liệt kê tên gói mà không sao chép nguyên văn nội dung giấy phép của tác giả gốc.
- Xóa bỏ thông báo bản quyền của tác giả ban đầu khi chỉnh sửa mã nguồn mở.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Tệp `THIRD_PARTY_NOTICES.md` chứa đầy đủ 100% các thành phần mã nguồn mở được đóng gói trong bản dựng.
- QG-02: Nguyên văn nội dung giấy phép và dòng Copyright của từng tác giả được bảo toàn nguyên vẹn.
- QG-03: Tệp thông báo bản quyền được tích hợp tự động vào mục 'About/Licenses' của giao diện ứng dụng.

## 10. Security & Safety Boundaries
- Đảm bảo tuân thủ đầy đủ nghĩa vụ pháp lý, triệt tiêu nguy cơ bị thu hồi quyền sử dụng mã nguồn mở do vi phạm điều khoản thông báo bản quyền.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Tệp ghi nhận bản quyền bên thứ ba hoàn chỉnh `THIRD_PARTY_NOTICES.md`.
1. Kịch bản tự động cập nhật tài liệu bản quyền trong CI `generate-notices.py`.

## 13. Related & Complementary Skills
- [`dex-open-source-license-scanning`](.agents/skills/dex-open-source-license-scanning/SKILL.md)
- [`dex-sbom-verification`](.agents/skills/dex-sbom-verification/SKILL.md)
- [`dex-documentation-as-code`](.agents/skills/dex-documentation-as-code/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Phát hành ứng dụng desktop cho 50,000 khách hàng doanh nghiệp. Kỹ sư kích hoạt `dex-third-party-attribution` để quét toàn bộ 340 gói npm và Rust crates được nhúng trong ứng dụng, tự động tổng hợp thành tệp `THIRD_PARTY_NOTICES.md` chuẩn mực tích hợp vào menu Help của ứng dụng, đáp ứng 100% yêu cầu kiểm toán pháp lý.
