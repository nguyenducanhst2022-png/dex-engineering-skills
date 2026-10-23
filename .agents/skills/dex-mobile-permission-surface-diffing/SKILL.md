---
name: dex-mobile-permission-surface-diffing
description: Extract, diff, and risk-score Android manifests (AndroidManifest.xml) and iOS Property Lists (Info.plist) across application releases to detect silent permission creep and capability expansion. Use when conducting mobile app security reviews.
---

# dex-mobile-permission-surface-diffing

## 1. Purpose & Scope
Trích xuất, so sánh sai khác (diffing) và chấm điểm rủi ro các quyền hạn ứng dụng di động trong `AndroidManifest.xml` (Android) và `Info.plist` (iOS) qua các phiên bản phát hành; phát hiện hiện tượng leo thang quyền âm thầm (permission creep) và mở rộng bề mặt tấn công không cần thiết.

## 2. When to Use
- Khi đánh giá phiên bản cập nhật của ứng dụng di động trước khi duyệt phát hành lên Play Store / App Store.
- Khi kiểm toán ứng dụng của bên thứ ba để đảm bảo không đòi hỏi quyền vị trí nền, danh bạ, hoặc micro bất thường.
- Khi triển khai chính sách quyền tối thiểu (Least Privilege) cho các ứng dụng mobile doanh nghiệp.

## 3. When NOT to Use
- Khi phân tích các ứng dụng backend web API không chạy trên thiết bị di động.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** File cài đặt ứng dụng Android (.apk, .aab) hoặc iOS (.ipa), công cụ trích xuất manifest (aapt2, apkanalyzer, plutil).
- **Quyền hạn truy cập:** Quyền chạy công cụ giải mã và phân tích file cài đặt di động.

## 5. Core Concepts & Taxonomy
- **Dangerous Permissions:** Nhóm quyền yêu cầu người dùng cấp phép tại thời điểm chạy (Runtime Permissions) trên Android (Camera, Location, Contacts, Microphone).
- **Silent Permission Creep:** Việc phiên bản mới âm thầm bổ sung thêm các quyền truy cập nhạy cảm mà người dùng không để ý khi nhấn cập nhật.
- **Exported Components:** Các Activity, Service, Broadcast Receiver có `android:exported="true"` có thể bị các ứng dụng độc hại khác trên máy gọi tới.

## 6. Step-by-Step Execution Workflow
1. Giải nén và trích xuất `AndroidManifest.xml` từ file APK bằng `aapt2` hoặc `apktool`.
2. Trích xuất `Info.plist` và các chuỗi giải thích quyền (`NS...UsageDescription`) từ file IPA.
3. So sánh danh sách quyền hạn giữa phiên bản hiện tại ($v_N$) và phiên bản trước ($v_{N-1}$).
4. Chấm điểm rủi ro cho từng quyền mới được bổ sung dựa trên mức độ nhạy cảm dữ liệu.
5. Kiểm tra tính hợp lệ và minh bạch của chuỗi lý do xin quyền (Usage Descriptions) hiển thị cho người dùng.
6. Rà soát các thành phần được export để đảm bảo có gắn quyền bảo vệ (custom permission) phù hợp.

## 7. Concrete Examples
### Trích xuất và so sánh quyền Android bằng aapt2:
```powershell
# Trích xuất danh sách permissions từ file APK v1 và v2
aapt2 dump permissions app-v1.apk > perms-v1.txt
aapt2 dump permissions app-v2.apk > perms-v2.txt

# So sánh sự khác biệt để phát hiện quyền mới được thêm vào
Compare-Object -ReferenceObject (Get-Content perms-v1.txt) -DifferenceObject (Get-Content perms-v2.txt)

# Trích xuất chuỗi lý do xin quyền trên iOS IPA
plutil -p Payload/App.app/Info.plist | Select-String -Pattern "UsageDescription"
```

## 8. Anti-Patterns & Common Traps
- **Blanket Permissions Request:** Xin toàn bộ các quyền nhạy cảm (Vị trí chính xác, Đọc danh bạ) ngay khi người dùng vừa mở app lần đầu.
- **Vague Usage Descriptions:** Ghi lý do xin quyền hời hợt như 'Ứng dụng cần quyền này để hoạt động tốt hơn' vi phạm chính sách của Apple App Store.
- **Unprotected Exported Services:** Đặt `exported="true"` cho Service xử lý thanh toán mà không yêu cầu chữ ký bảo vệ (Signature Permission).

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: 100% các quyền mới bổ sung đều có văn bản giải trình nghiệp vụ được phê duyệt.
- **QG-06**: Không có quyền nguy hiểm (Dangerous Permission) nào bị thêm vào mà không thông qua đánh giá an ninh.
- **QG-08**: Tất cả các trường `NSUsageDescription` trên iOS đều mô tả chi tiết, rõ ràng mục đích sử dụng.

## 10. Security & Safety Boundaries
- Chặn đứng việc rò rỉ dữ liệu cá nhân thông qua việc lạm dụng quyền đọc bộ nhớ chung (External Storage) hoặc ghi âm nền.

## 11. Platform Adapters
- **Tools**: aapt2, apkanalyzer, apktool, plutil, MobSF, androguard.

## 12. Deliverables & Output Artifacts
- Báo cáo đối chiếu quyền hạn giữa hai phiên bản (Diff Matrix).
- Bảng chấm điểm rủi ro bề mặt tấn công ứng dụng.
- Khuyến nghị thu hẹp danh sách quyền về mức tối thiểu cần thiết.

## 13. Related & Complementary Skills
dex-installer-package-static-review, dex-macos-entitlements-review, dex-binary-provenance-matching

## 14. Realistic Usage Example
```powershell
# Phân tích tự động APK bằng apkanalyzer
apkanalyzer manifest permissions app-release.apk

# Kiểm tra các components exported không an toàn
python -c "
import xml.etree.ElementTree as ET
# Phân tích file AndroidManifest.xml đã decode
tree = ET.parse('AndroidManifest.xml')
for elem in tree.findall('.//*[@android:exported="true"]', {'android': 'http://schemas.android.com/apk/res/android'}):
    print('Exported component:', elem.tag, elem.attrib)
"
```
