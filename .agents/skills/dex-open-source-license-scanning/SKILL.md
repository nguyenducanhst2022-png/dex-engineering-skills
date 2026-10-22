---
name: dex-open-source-license-scanning
description: Automate open-source software (OSS) license compliance scanning, detecting copyleft contamination (GPL/AGPL), dual-licensing clauses, and license incompatibility risks across dependency trees. Use when gating release builds, preparing M&A technical audits, or generating Software Bill of Materials (SBOM).
---

# dex-open-source-license-scanning

## 1. Purpose & Scope
Tự động hóa quy trình quét và thẩm định tính tuân thủ giấy phép mã nguồn mở (Open Source License Compliance Scanning); phát hiện sớm các nguy cơ ô nhiễm giấy phép bản quyền lây lan (Copyleft Contamination như GPL, AGPL trong phần mềm thương mại độc quyền), các điều khoản cấp phép kép (Dual-Licensing) và các xung đột giấy phép không tương thích trong toàn bộ cây phụ thuộc; phục vụ nghiệm thu bản dựng phát hành và thẩm tra kỹ thuật M&A.

## 2. When to Use
- Trước khi đóng gói phát hành phần mềm thương mại độc quyền cho khách hàng doanh nghiệp.
- Khi thêm mới một thư viện mã nguồn mở vào dự án cần kiểm tra giấy phép có phù hợp với chính sách công ty hay không.
- Khi tạo bảng danh mục vật liệu phần mềm (Software Bill of Materials - SBOM) chuẩn SPDX/CycloneDX.

## 3. When NOT to Use
- Khi toàn bộ dự án đã được phát hành công khai dưới giấy phép AGPL.
- Khi kiểm tra lỗi cú pháp mã nguồn thông thường.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Tệp khóa phụ thuộc (`package-lock.json`, `poetry.lock`, `Cargo.lock`), công cụ quét giấy phép (FOSSA, ScanCode Toolkit hoặc `license-checker`).
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; bảo vệ toàn vẹn tài sản kỹ nghệ và dữ liệu sản xuất.

## 5. Core Concepts & Taxonomy
- **Permissive vs Copyleft:** Phân biệt giữa giấy phép thoáng (Permissive: MIT, Apache-2.0, BSD - cho phép dùng trong phần mềm đóng mã) và giấy phép bản quyền lây lan (Copyleft: GPL, AGPL - bắt buộc phải mở toàn bộ mã nguồn liên kết).
- **Transitive Dependency Contamination:** Một thư viện MIT có thể kéo theo một thư viện con gián tiếp mang giấy phép GPL-3.0 làm lây nhiễm toàn bộ dự án.
- **SPDX Standard Identifiers:** Chuẩn hóa tên định danh giấy phép quốc tế (ví dụ: `Apache-2.0`, `MIT`, `GPL-3.0-only`).

## 6. Step-by-Step Execution Workflow
1. Trích xuất danh sách toàn bộ các phụ thuộc trực tiếp và bắc cầu từ tệp lockfile.
2. Quét và bóc tách các tệp `LICENSE`, `COPYING` và tiêu đề mã nguồn của từng gói phụ thuộc.
3. Chuẩn hóa tên giấy phép sang định dạng chuẩn SPDX Identifier.
4. Đối chiếu danh sách giấy phép với chính sách cho phép (Allowlist Policy) của tổ chức.
5. Nếu phát hiện giấy phép cấm (như AGPL trong dự án SaaS đóng mã), kích hoạt cảnh báo chặn đường ống CI.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```json
{
  "$schema": "https://dex.dev/schemas/license-policy.json",
  "policyName": "Commercial Proprietary SaaS Policy",
  "allowedLicenses": [
    "MIT",
    "Apache-2.0",
    "BSD-2-Clause",
    "BSD-3-Clause",
    "ISC"
  ],
  "prohibitedLicenses": [
    "GPL-1.0-only", "GPL-2.0-only", "GPL-3.0-only",
    "AGPL-3.0-only", "SSPL-1.0"
  ],
  "reviewRequired": [
    "MPL-2.0", "LGPL-3.0-only", "EPL-2.0"
  ]
}
```

## 8. Anti-Patterns & Common Traps
- Chỉ kiểm tra giấy phép của các phụ thuộc trực tiếp trong `package.json` mà bỏ qua hàng trăm phụ thuộc bắc cầu (Transitive Dependencies) trong lockfile.
- Tự ý nhúng mã nguồn có giấy phép GPL vào phần mềm đóng mã của công ty rồi bán cho khách hàng (vi phạm pháp luật bản quyền nghiêm trọng).
- Bỏ qua các phụ thuộc không có giấy phép rõ ràng (Unlicensed Code / No License - mặc định được pháp luật bảo lưu toàn bộ quyền).

## 9. Quality Gates & Acceptance Criteria
- QG-01: 100% các phụ thuộc trực tiếp và gián tiếp đều được định danh giấy phép chuẩn SPDX.
- QG-02: Không có bất kỳ gói phụ thuộc nào chứa giấy phép cấm (Prohibited Licenses) lọt vào bản dựng phát hành.
- QG-03: Cổng CI tự động chặn merge pull request nếu phát hiện vi phạm chính sách giấy phép.

## 10. Security & Safety Boundaries
- Ngăn ngừa các rủi ro pháp lý tranh chấp sở hữu trí tuệ có thể dẫn đến việc doanh nghiệp bị kiện hoặc bị ép buộc công khai toàn bộ mã nguồn bí mật kinh doanh.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Báo cáo kiểm toán giấy phép phụ thuộc `LICENSE_COMPLIANCE_AUDIT.md`.
1. Tệp cấu hình chính sách kiểm soát giấy phép tự động `.license-policy.json`.

## 13. Related & Complementary Skills
- [`dex-third-party-attribution`](.agents/skills/dex-third-party-attribution/SKILL.md)
- [`dex-dependency-vulnerability-intelligence`](.agents/skills/dex-dependency-vulnerability-intelligence/SKILL.md)
- [`dex-sbom-verification`](.agents/skills/dex-sbom-verification/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Doanh nghiệp chuẩn bị thương vụ M&A bán công ty giá 50 triệu USD. Đội ngũ kiểm toán kỹ thuật của quỹ đầu tư yêu cầu quét giấy phép mã nguồn. Kỹ sư kích hoạt `dex-open-source-license-scanning`, phát hiện 2 thư viện nhỏ mang giấy phép GPL-3.0 lọt vào backend, kịp thời thay thế bằng thư viện tương đương mang giấy phép MIT, bảo vệ thành công giá trị thương vụ.
