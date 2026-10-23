---
name: dex-macos-entitlements-review
description: Inspect, diff, and audit macOS application entitlements, sandbox escape vectors, Hardened Runtime configurations, and code signing provisions. Use when conducting macOS application security architecture and compliance reviews.
---

# dex-macos-entitlements-review

## 1. Purpose & Scope
Thanh tra, so sánh và kiểm toán các quyền cấp phép (Entitlements), cấu hình Hardened Runtime, tính toàn vẹn của chữ ký số (Code Signing) và rủi ro thoát hộp cát (Sandbox Escape) trên các ứng dụng macOS (.app); bảo đảm ứng dụng tuân thủ nguyên tắc đặc quyền tối thiểu của Apple.

## 2. When to Use
- Khi chuẩn bị nộp ứng dụng macOS lên Mac App Store hoặc phân phối qua cơ chế công chứng (Notarization).
- Khi kiểm toán an ninh ứng dụng máy tính chạy trên hệ điều hành macOS.
- Khi phát hiện ứng dụng yêu cầu các quyền hạn nguy hiểm như tắt xác thực thư viện (`com.apple.security.cs.disable-library-validation`).

## 3. When NOT to Use
- Khi phát triển ứng dụng di động iOS thuần túy hoặc ứng dụng chạy trên máy chủ Linux/Windows.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** File ứng dụng macOS (`.app`), chứng chỉ Apple Developer, công cụ dòng lệnh macOS (`codesign`, `security`, `spctl`).
- **Quyền hạn truy cập:** Quyền thực thi các tiện ích phân tích chữ ký trên máy macOS hoặc môi trường giả lập.

## 5. Core Concepts & Taxonomy
- **App Sandbox:** Cơ chế cô lập ứng dụng trong một thư mục sandbox riêng biệt, chỉ được truy cập tài nguyên hệ thống thông qua các quyền khai báo tường minh.
- **Hardened Runtime:** Cơ chế bảo vệ tính toàn vẹn của tiến trình, ngăn chặn kỹ thuật chèn mã (code injection), can thiệp bộ nhớ hoặc tải thư viện không có chữ ký.
- **Dangerous Entitlements:** Các quyền làm suy yếu hàng rào bảo vệ như `allow-jit`, `allow-unsigned-executable-memory`, `disable-library-validation`.

## 6. Step-by-Step Execution Workflow
1. Trích xuất thông tin chữ ký số và trạng thái Notarization của file `.app` bằng `codesign` và `spctl`.
2. Trích xuất toàn bộ danh sách Entitlements ở định dạng XML Property List.
3. Rà soát từng entitlement: đối chiếu với yêu cầu nghiệp vụ thực tế của ứng dụng.
4. Đánh giá rủi ro đặc biệt đối với quyền tắt kiểm tra thư viện (`disable-library-validation`) do có thể bị tấn công DLL Hijacking (Dylib Injection).
5. Kiểm tra các quyền truy cập phần cứng nhạy cảm: Camera, Microphone, Location, AddressBook.
6. Lập báo cáo kiểm toán an ninh macOS kèm danh sách các quyền cần thu hồi hoặc thắt chặt.

## 7. Concrete Examples
### Trích xuất và kiểm toán Entitlements trên macOS:
```bash
# Trích xuất toàn bộ entitlements từ file binary của ứng dụng
codesign -d --entitlements :- /Applications/TargetApp.app/Contents/MacOS/TargetApp

# Kiểm tra trạng thái Hardened Runtime và cờ bảo vệ
codesign -dvvv --deep /Applications/TargetApp.app

# Đánh giá tính hợp lệ với hệ thống Gatekeeper của Apple
spctl --assess --type execute --verbose=4 /Applications/TargetApp.app
```

```xml
<!-- Ví dụ entitlements XML cần kiểm toán kỹ lưỡng -->
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>com.apple.security.app-sandbox</key>
    <true/>
    <!-- Rủi ro cao: Cho phép nạp dylib không cùng nhóm chữ ký số -->
    <key>com.apple.security.cs.disable-library-validation</key>
    <true/>
</dict>
</plist>
```

## 8. Anti-Patterns & Common Traps
- **Disabling Library Validation by Default:** Tắt xác thực dylib chỉ để tiện debug trong quá trình phát triển nhưng quên gỡ bỏ khi đóng gói release.
- **Unsandboxed Distribution:** Phân phối ứng dụng không bật App Sandbox mà không có lý do kiến trúc chính đáng.
- **Temporary Exception Abuse:** Lạm dụng quyền ngoại lệ tạm thời (`com.apple.security.temporary-exception.files.all-files`) để đọc toàn bộ ổ đĩa người dùng.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Ứng dụng vượt qua kiểm tra Gatekeeper (`spctl --assess`) với trạng thái accepted.
- **QG-06**: Quyền `disable-library-validation` bị cấm tuyệt đối trừ khi có giải trình ngoại lệ kiến trúc bắt buộc.
- **QG-08**: Tất cả các entitlements khai báo đều tương ứng trực tiếp với tính năng người dùng có thể kiểm chứng.

## 10. Security & Safety Boundaries
- Triệt tiêu các nguy cơ tấn công leo thang đặc quyền cục bộ (Local Privilege Escalation) thông qua Dylib Hijacking.

## 11. Platform Adapters
- **Tools**: codesign, spctl, security, plutil, otool, dyld_info.

## 12. Deliverables & Output Artifacts
- File XML danh mục entitlements đã được làm sạch.
- Báo cáo kiểm toán chữ ký số và Hardened Runtime.
- Bảng đối soát rủi ro các quyền đặc quyền.

## 13. Related & Complementary Skills
dex-installer-package-static-review, dex-mobile-permission-surface-diffing, dex-binary-provenance-matching

## 14. Realistic Usage Example
```powershell
# Chạy script Python phân tích cú pháp entitlements XML
python -c "
import plistlib, subprocess
# Trích xuất và đọc entitlements từ app macOS
xml_data = subprocess.check_output(['codesign', '-d', '--entitlements', ':-', '/Applications/TargetApp.app'])
plist = plistlib.loads(xml_data)
for k, v in plist.items():
    print(f'{k} => {v}')
"
```
