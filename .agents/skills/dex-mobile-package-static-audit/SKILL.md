---
name: dex-mobile-package-static-audit
description: Perform static security audits on authorized Android APK/AAB packages and iOS IPA bundles, analyzing AndroidManifest.xml exported components, network security configurations, and embedded native libraries (.so). Use when auditing mobile client application releases for compliance and security baselines. (Strictly authorized/defensive).
---

# dex-mobile-package-static-audit

## 1. Purpose & Scope
Thực hiện kiểm toán an ninh tĩnh trên các gói cài đặt ứng dụng di động được ủy quyền: Android APK/AAB và iOS IPA; phân tích tệp cấu hình quyền hạn `AndroidManifest.xml`, các thành phần bị phơi bày công khai (Exported Activities/Receivers), chính sách an ninh mạng (Network Security Config) và các thư viện nhị phân nhúng (`.so`); đảm bảo tuân thủ tiêu chuẩn OWASP Mobile Application Security (MASVS).

## 2. When to Use
- Trước khi phát hành phiên bản mới của ứng dụng ngân hàng hoặc ví điện tử lên Google Play và Apple App Store.
- Khi kiểm định an toàn của một ứng dụng di động nội bộ của doanh nghiệp.
- Khi rà soát các quyền hạn bị xin thừa thãi gây ảnh hưởng đến quyền riêng tư của khách hàng.

## 3. When NOT to Use
- Khi phân tích ứng dụng của bên thứ ba mà không có sự đồng ý bằng văn bản của chủ sở hữu.
- Khi cố tình vượt qua cơ chế chống gian lận (Anti-tampering / Anti-cheat) của game di động.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Gói cài đặt ứng dụng APK/IPA, công cụ dòng lệnh `apktool`, `aapt2`, `keytool` hoặc công cụ phân tích tự động MobSF.
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; tuyệt đối không can thiệp trái phép vào hệ thống của bên thứ ba.

## 5. Core Concepts & Taxonomy
- **Exported Component Risk:** Các Activity, Service hoặc Content Provider có thuộc tính `android:exported="true"` mà không có permission bảo vệ có thể bị các ứng dụng độc hại khác trên máy gọi lén.
- **Cleartext Traffic Policy:** Bắt buộc cấu hình `android:usesCleartextTraffic="false"` để cấm hoàn toàn kết nối HTTP không mã hóa.
- **Certificate Pinning Verification:** Kiểm tra cấu hình ghim chứng chỉ số SSL/TLS để ngăn ngừa tấn công bắt gói tin Man-in-the-Middle.

## 6. Step-by-Step Execution Workflow
1. Giải nén gói cài đặt và trích xuất tệp manifest bằng `apktool d app.apk -o ./decompiled_apk`.
2. Rà soát danh sách các quyền (`<uses-permission>`) và đánh giá mức độ cần thiết theo nguyên tắc đặc quyền tối thiểu.
3. Kiểm tra toàn bộ các thẻ `<activity>`, `<service>`, `<receiver>` xem có thành phần nào bị mở `exported="true"` trái phép hay không.
4. Phân tích tệp `network_security_config.xml` để đảm bảo cấm hoàn toàn giao thức HTTP và chứng chỉ tự ký của người dùng.
5. Xuất bản báo cáo kiểm toán di động `MOBILE_SECURITY_AUDIT.md`.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```xml
<!-- Hardened Android Network Security Config -->
<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <base-config cleartextTrafficPermitted="false">
        <trust-anchors>
            <!-- Only trust system CAs, disallow user-installed certs -->
            <certificates src="system" />
        </trust-anchors>
    </base-config>
    <domain-config>
        <domain includeSubdomains="true">api.dex.dev</domain>
        <pin-set expiration="2027-01-01">
            <pin digest="SHA-256">k2v657xUM4MpNGnb...=</pin>
        </pin-set>
    </domain-config>
</network-security-config>
```

## 8. Anti-Patterns & Common Traps
- Đặt `android:exported="true"` cho các Activity quản trị nội bộ hoặc màn hình đổi mật khẩu mà không gắn permission.
- Cho phép ứng dụng tin tưởng chứng chỉ cài thêm của người dùng (`<certificates src="user" />`) trong bản dựng sản xuất, mở đường cho việc nghe lén lưu lượng.
- Lưu trữ dữ liệu đăng nhập của người dùng vào thẻ nhớ ngoài (External Storage) không có mã hóa.

## 9. Quality Gates & Acceptance Criteria
- QG-01: 100% các thành phần exported đều có permission bảo vệ hoặc được chuyển về `exported="false"`.
- QG-02: Cấm hoàn toàn lưu lượng truyền tin dạng bản rõ HTTP (`cleartextTrafficPermitted="false"`).
- QG-03: Tuân thủ đầy đủ các tiêu chí bảo mật cấp L1 theo tiêu chuẩn OWASP MASVS.

## 10. Security & Safety Boundaries
- Bảo vệ thông tin cá nhân và dữ liệu tài chính của người dùng di động khỏi sự can thiệp của các phần mềm gián điệp cài cùng trên thiết bị.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Hoạt động phân tích hoàn toàn hợp pháp, minh bạch và có sự ủy quyền chính thức từ chủ sở hữu hệ thống.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Báo cáo kiểm toán tĩnh ứng dụng di động `MOBILE_SECURITY_AUDIT.md`.
1. Bản vá cấu hình bảo mật `network_security_config.xml`.

## 13. Related & Complementary Skills
- [`dex-android-app-architecture`](.agents/skills/dex-android-app-architecture/SKILL.md)
- [`dex-ios-app-architecture`](.agents/skills/dex-ios-app-architecture/SKILL.md)
- [`dex-reverse-evidence-chain`](.agents/skills/dex-reverse-evidence-chain/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Kiểm toán ứng dụng ví điện tử trước ngày phát hành chính thức. Kỹ sư kích hoạt `dex-mobile-package-static-audit`, phát hiện một BroadcastReceiver nhận thông báo biến động số dư bị bật `exported="true"` mà không kiểm tra chữ ký gửi, giúp đội phát triển sửa lại thành `exported="false"` để tránh bị các app khác đánh cắp thông báo giao dịch.
