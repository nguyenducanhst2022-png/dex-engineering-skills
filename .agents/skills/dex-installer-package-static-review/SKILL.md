---
name: dex-installer-package-static-review
description: Inspect desktop installer bundles (MSI, NSIS, Inno Setup, PKG, DMG, AppImage) for embedded scripts, privilege escalation risks, persistence mechanisms, and bundled payload integrity. Use when reviewing third-party desktop distributions.
---

# dex-installer-package-static-review

## 1. Purpose & Scope
Thanh tra và kiểm toán tĩnh các gói cài đặt phần mềm máy tính (MSI, NSIS, Inno Setup, PKG, DMG, AppImage); phát hiện các kịch bản thực thi ngầm, nguy cơ leo thang đặc quyền, cơ chế duy trì persistence bất thường và kiểm tra tính toàn vẹn của các payload đi kèm.

## 2. When to Use
- Khi đánh giá an ninh phần mềm của đối tác trước khi cấp phép cài đặt lên máy trạm nhân viên doanh nghiệp.
- Khi kiểm toán gói cài đặt do chính tổ chức đóng gói để phát hiện các file hoặc registry key thừa thãi.
- Khi thẩm định các phần mềm thương mại không cung cấp mã nguồn mở.

## 3. When NOT to Use
- Khi phân tích các ứng dụng SaaS chạy thuần túy trên nền tảng trình duyệt không yêu cầu cài đặt phần mềm cục bộ.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** File cài đặt (setup.exe, installer.msi, app.pkg, app.dmg), công cụ trích xuất và phân tích gói.
- **Quyền hạn truy cập:** Quyền thực thi công cụ giải nén trong môi trường phân tích tĩnh cô lập.

## 5. Core Concepts & Taxonomy
- **Custom Actions in MSI:** Các hành động tùy biến trong gói MSI (DLL, VBScript, JScript) thường là nơi ẩn giấu mã độc hoặc các hành vi nguy hiểm.
- **Persistence Mechanisms:** Các khóa Registry tự khởi động (`Run`, `RunOnce`), Scheduled Tasks hoặc Windows Services được tạo ra trong quá trình cài đặt.
- **Privilege Demarcation:** Gói cài đặt có đòi quyền Administrator/Root một cách không cần thiết cho các ứng dụng chỉ chạy ở phạm vi người dùng (Per-User Install) hay không.

## 6. Step-by-Step Execution Workflow
1. Trích xuất toàn bộ nội dung của gói cài đặt mà không thực thi file (sử dụng 7-Zip, lessmsi, innoextract, pkgutil).
2. Quét toàn bộ mã băm các file thành phần qua cơ sở dữ liệu mẫu mã độc (VirusTotal, nội bộ YARA).
3. Rà soát các kịch bản cài đặt tùy biến (Custom Actions, NSIS scripts, Pre/Post-install scripts trong PKG).
4. Kiểm tra các thay đổi cấu hình hệ thống: khóa Registry, biến môi trường PATH, dịch vụ hệ điều hành mới.
5. Xác minh chữ ký số của gói cài đặt và tất cả các file thực thi nhị phân con bên trong.
6. Lập báo cáo kiểm toán tĩnh đánh giá mức độ rủi ro và các khuyến nghị an toàn.

## 7. Concrete Examples
### Trích xuất và kiểm tra gói cài đặt MSI / Inno Setup:
```powershell
# Trích xuất bảng và file từ MSI bằng lessmsi
lessmsi x ./vendor-installer.msi ./extracted_msi/

# Xem danh sách các Custom Actions có thể chứa script can thiệp hệ thống
lessmsi table -t CustomAction ./vendor-installer.msi

# Giải nén gói cài đặt Inno Setup mà không cần chạy file thực thi
innoextract --extract ./setup-inno.exe

# Kiểm tra chữ ký Authenticode của gói cài đặt
Get-AuthenticodeSignature ./vendor-installer.msi
```

## 8. Anti-Patterns & Common Traps
- **Running Installer to Analyze It:** Nhấp đúp chuột để chạy file cài đặt trên máy làm việc chính thay vì trích xuất tĩnh trong môi trường cô lập.
- **Ignoring Bundled Dependencies:** Chỉ quét file `.exe` bọc ngoài mà bỏ qua các file DLL hoặc công cụ bên thứ ba nằm nén sâu bên trong gói.
- **Overprivileged Installation:** Đòi quyền SYSTEM / Administrator cho các tiện ích đơn giản chỉ cần ghi dữ liệu vào thư mục `%LocalAppData%`.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Chữ ký Authenticode / Apple Developer ID của gói cài đặt hoàn toàn hợp lệ.
- **QG-06**: Không chứa bất kỳ Custom Action nào thực thi các tập lệnh không rõ nguồn gốc (VBScript, PowerShell không ký số).
- **QG-08**: Toàn bộ các file nhị phân trích xuất đều sạch mã độc và được ghi nhận trong danh mục thành phần.

## 10. Security & Safety Boundaries
- Cảnh báo ngay lập tức nếu gói cài đặt cố tình tắt Windows Defender, sửa file hosts hoặc mở cổng tường lửa mà không thông báo cho người dùng.

## 11. Platform Adapters
- **Tools**: lessmsi, 7-Zip, innoextract, pkgutil, hdiutil, YARA, Sigcheck.

## 12. Deliverables & Output Artifacts
- Cây thư mục giải nén toàn bộ artifact từ bộ cài.
- Báo cáo kiểm toán các Custom Actions và Registry keys.
- Chứng chỉ đánh giá rủi ro an ninh cài đặt.

## 13. Related & Complementary Skills
dex-binary-provenance-matching, dex-sbom-binary-correlation, dex-macos-entitlements-review

## 14. Realistic Usage Example
```powershell
# Kiểm tra chi tiết chữ ký số và chứng chỉ của bộ cài
sigcheck.exe -h -vt ./vendor-installer.msi

# Quét các file đã giải nén bằng bộ luật YARA phát hiện persistence
yara -r rules/installer_persistence.yar ./extracted_msi/
```
