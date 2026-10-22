---
name: dex-code-signing-release-process
description: Establish automated, tamper-proof code signing pipelines for Windows Authenticode, macOS Notarization, and Linux GPG packages using Hardware Security Modules (HSM) and cloud key management. Use when eliminating Windows SmartScreen warnings and passing macOS Gatekeeper.
---

# dex-code-signing-release-process

## 1. Purpose & Scope
Thiết lập quy trình ký mã nguồn (Code Signing Release Pipeline) tự động và chống giả mạo cho các gói phần mềm Windows (Microsoft Authenticode), macOS (Apple Notarization & Stapling) và Linux (GPG/RPM/DEB); tích hợp mô-đun bảo mật phần cứng (Hardware Security Module - HSM) hoặc dịch vụ quản lý khóa đám mây (Cloud KMS); triệt tiêu hoàn toàn cảnh báo bảo mật Windows Defender SmartScreen và vượt qua rào chắn kiểm duyệt macOS Gatekeeper.

## 2. When to Use
- Trước khi xuất bản tệp cài đặt phần mềm máy tính (`.exe`, `.msi`, `.dmg`, `.pkg`) cho người dùng cuối.
- Khi ứng dụng cài đặt bị hệ điều hành Windows hiển thị cảnh báo đỏ 'Windows protected your PC' gây mất uy tín.
- Khi phát hành ứng dụng trên macOS yêu cầu chứng chỉ Apple Developer và tiến trình công chứng Notarization hợp lệ.

## 3. When NOT to Use
- Khi chỉ triển khai mã nguồn lên máy chủ nội bộ hoặc container Docker (nên dùng Sigstore/Cosign).
- Khi xuất bản trang web thông thường.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Chứng chỉ số ký mã nguồn (EV Code Signing Certificate hoặc Apple Developer ID), công cụ `signtool.exe` trên Windows hoặc `codesign`/`notarytool` trên macOS.
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; bảo vệ toàn vẹn tài sản kỹ nghệ và dữ liệu sản xuất.

## 5. Core Concepts & Taxonomy
- **EV Code Signing & SmartScreen Reputation:** Chứng chỉ số mở rộng (Extended Validation) giúp phần mềm có ngay uy tín tức thì trên Windows SmartScreen mà không cần tích lũy lượt tải.
- **Apple Notarization & Stapling:** Quá trình gửi ứng dụng lên máy chủ Apple để quét mã độc tự động, sau đó đính kèm vé công chứng (Staple) vào tệp `.dmg` để ứng dụng mở được khi ngoại tuyến.
- **RFC 3161 Trusted Timestamping:** Ký kèm dấu thời gian tin cậy để chữ ký của phần mềm vẫn có hiệu lực vĩnh viễn ngay cả khi chứng chỉ ký mã nguồn hết hạn trong tương lai.

## 6. Step-by-Step Execution Workflow
1. Xây dựng bản dựng phần mềm nhị phân sạch trong môi trường CI khép kín.
2. Gọi lệnh ký số kết nối với HSM hoặc Azure Trusted Signing / AWS KMS.
3. Đóng dấu thời gian tin cậy RFC 3161 từ máy chủ timestamp có uy tín (DigiCert hoặc Sectigo).
4. Đối với macOS, gửi gói lên dịch vụ Apple Notary Service và đính kèm vé công chứng bằng `xcrun staple`.
5. Kiểm tra tính toàn vẹn của chữ ký số bằng lệnh `signtool verify` hoặc `spctl -a`.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```bash
# Windows Authenticode Signing with RFC 3161 Timestamp
signtool.exe sign /tr http://timestamp.digicert.com /td sha256 /fd sha256 /a "bin/DEX_Installer.exe"
signtool.exe verify /pa /v "bin/DEX_Installer.exe"

# macOS Hardened Runtime Signing & Notarization
codesign --deep --force --options runtime --sign "Developer ID Application: DEX Engineering (TEAM123)" "dist/DEX.app"
xcrun notarytool submit "dist/DEX.dmg" --keychain-profile "AC_PASSWORD" --wait
xcrun stapler staple "dist/DEX.dmg"
spctl --assess --type execute --verbose "dist/DEX.dmg" 
```

## 8. Anti-Patterns & Common Traps
- Ký mã nguồn mà quên gắn dấu thời gian RFC 3161 Timestamp, khiến phần mềm bị Windows báo lỗi chứng chỉ hết hạn ngay sau 1 năm phát hành.
- Lưu tệp chứng chỉ ký mã nguồn `.pfx` kèm mật khẩu thẳng vào kho mã nguồn Git của dự án (vi phạm bảo mật nghiêm trọng).
- Bỏ qua cờ Hardened Runtime trên macOS khiến ứng dụng bị từ chối công chứng bởi Apple.

## 9. Quality Gates & Acceptance Criteria
- QG-01: 100% các tệp `.exe`, `.dll`, `.dmg` phát hành đều có chữ ký số hợp lệ kèm RFC 3161 Timestamp.
- QG-02: Vượt qua kiểm tra macOS Gatekeeper (`spctl --assess`) với thông báo `accepted`.
- QG-03: Khóa riêng tư ký mã nguồn được lưu trữ độc quyền trong HSM/Cloud KMS, không bao giờ xuất ra tệp thô.

## 10. Security & Safety Boundaries
- Áp dụng quy trình phê duyệt kép trước khi kích hoạt lệnh ký mã nguồn phát hành chính thức để chống việc mã độc bị ký lén.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Kịch bản tự động hóa ký mã nguồn Windows/macOS trong CI `sign-release.sh`.
1. Bản báo cáo thẩm định chứng chỉ số và công chứng phần mềm.

## 13. Related & Complementary Skills
- [`dex-artifact-signature-verification`](.agents/skills/dex-artifact-signature-verification/SKILL.md)
- [`dex-software-update-trust-chains`](.agents/skills/dex-software-update-trust-chains/SKILL.md)
- [`dex-release-reproducibility-audit`](.agents/skills/dex-release-reproducibility-audit/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Doanh nghiệp phát hành phần mềm quản lý kho cho các đại lý bán lẻ. Khách hàng phàn nàn không cài đặt được vì Windows 11 hiện màn hình cảnh báo xanh chặn đứng. Kỹ sư kích hoạt `dex-code-signing-release-process`, tích hợp Azure Trusted Signing với chứng chỉ EV và timestamp SHA-256 vào GitHub Actions, giúp tệp cài đặt mở lên tức thì không còn bất kỳ cảnh báo nào.
