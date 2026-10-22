---
name: dex-native-device-integration
description: Integrate device capabilities (Camera, Geolocation, Bluetooth BLE, Biometrics, File System Access) across mobile and desktop with runtime permissions and graceful fallbacks. Use when connecting apps to hardware sensors.
---

# dex-native-device-integration

## 1. Purpose & Scope
Thiết kế và hiện thực hóa kết nối an toàn, tin cậy giữa ứng dụng phần mềm và các cảm biến, phần cứng phần cứng nguyên bản của thiết bị (Native Device Capabilities: Camera, GPS/Geolocation, Bluetooth Low Energy - BLE, Biometrics FaceID/Fingerprint, Microphone, File System Access API); quản lý vòng đời yêu cầu cấp quyền lúc thực thi (Runtime Permissions Workflow), kiểm tra tính khả dụng của phần cứng và xây dựng cơ chế thoái lui duyên dáng (Graceful Fallback) khi thiết bị thiếu cảm biến hoặc người dùng từ chối cấp quyền.

## 2. When to Use
- Khi ứng dụng cần sử dụng camera để quét mã QR/chụp ảnh, định vị GPS, xác thực sinh trắc học hoặc kết nối thiết bị y tế/IoT qua Bluetooth.
- Khi ứng dụng bị crash đột ngột vì gọi hàm phần cứng mà người dùng chưa cấp quyền hoặc thiết bị không hỗ trợ.
- Khi cần xử lý trường hợp người dùng từ chối quyền vĩnh viễn (Permission Denied / Never Ask Again).

## 3. When NOT to Use
- Xử lý logic nghiệp vụ backend thuần túy trên máy chủ đám mây.
- Tương tác với cơ sở dữ liệu hoặc bộ nhớ cache cục bộ (dùng `dex-mobile-offline-sync`).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Danh sách phần cứng mục tiêu và các quyền hệ thống cần khai báo (`AndroidManifest.xml`, `Info.plist`, web capabilities).
- Lý do sử dụng (Permission Rationale) giải thích cho người dùng hiểu tại sao cần cấp quyền.
- Phương án xử lý thay thế khi không có phần cứng.
- **Điều kiện tiên quyết**:
- Cấu hình các thẻ quyền tương ứng trong manifest của nền tảng.
- Thiết bị thực tế hoặc giả lập có hỗ trợ mô phỏng cảm biến phần cứng.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- **Just-In-Time Permission Request**: Chỉ yêu cầu cấp quyền ngay tại thời điểm người dùng bấm vào tính năng cần sử dụng (Contextual Prompt), không xin tất cả quyền ngay khi vừa mở ứng dụng lần đầu.
- **Hardware Capability Probing**: Luôn kiểm tra xem thiết bị có hỗ trợ phần cứng tương ứng hay không (`isHardwareAvailable()`) trước khi tiến hành yêu cầu cấp quyền.
- **Graceful Degradation**: Nếu người dùng từ chối camera, cho phép họ chọn ảnh có sẵn từ thư viện; nếu không có FaceID, cho phép nhập mã PIN/mật khẩu dự phòng.
- **Quy tắc quyết định kỹ thuật**:
- **Giải Thích Trước Khi Xin Quyền (Rationale Dialog)**: Nếu hệ thống báo người dùng đã từng từ chối một lần, bắt buộc phải hiển thị hộp thoại giải thích rõ lợi ích trước khi gọi API xin quyền lại.
- **Không Treo Tính Năng Khi Bị Từ Chối**: Ứng dụng phải có đường dẫn thay thế (fallback path) và nút hướng dẫn người dùng tự mở màn hình Cài đặt hệ thống (System Settings) nếu muốn kích hoạt lại.
- **Ngắt Kết Nối Phần Cứng Khi Ứng Dụng Chạy Nền**: Ngắt quét Bluetooth BLE hoặc tắt GPS tracking khi ứng dụng vào trạng thái Background để bảo vệ thời lượng pin và quyền riêng tư.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Ứng dụng crash văng ra màn hình chính khi vừa bấm Quét Mã QR**: Do gọi `cameraProvider.bindToLifecycle()` mà không kiểm tra quyền `CAMERA` -> Khắc phục: Kiểm tra trạng thái quyền qua `ContextCompat.checkSelfPermission` trước khi khởi tạo Camera.
- **Quét Bluetooth làm cạn kiệt pin thiết bị chỉ sau 2 tiếng**: Do để cờ `ScanSettings.SCAN_MODE_LOW_LATENCY` chạy liên tục không timeout -> Khắc phục: Giới hạn thời gian quét Bluetooth tối đa 15-30 giây và chuyển sang chế độ low-power.

## 6. Step-by-Step Execution Workflow
1. Khai báo quyền rõ ràng trong tệp cấu hình nền tảng (`AndroidManifest.xml` hoặc iOS `Info.plist` kèm `NSCameraUsageDescription`).
2. Xây dựng Hardware Manager đóng gói việc kiểm tra tính khả dụng của thiết bị (`hasSystemFeature`).
3. Kiểm tra trạng thái quyền hiện tại: `GRANTED`, `DENIED`, hoặc `PERMANENTLY_DENIED`.
4. Nếu chưa cấp quyền: Hiển thị giao diện giải thích lý do (Permission Educational Screen).
5. Kích hoạt lời gọi yêu cầu cấp quyền chuẩn của hệ điều hành.
6. Nếu được cấp quyền: Khởi tạo phần cứng và thực thi tác vụ người dùng mong muốn.
7. Nếu bị từ chối: Kích hoạt cơ chế fallback và hiển thị thông báo hướng dẫn nhẹ nhàng.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```typescript
// Universal Device Permission & Hardware Adapter Pattern
export interface BiometricAuthResult {
  success: boolean;
  error?: 'HARDWARE_UNAVAILABLE' | 'NOT_ENROLLED' | 'PERMISSION_DENIED' | 'USER_CANCELED';
}

export class NativeBiometricAdapter {
  async authenticate(): Promise<BiometricAuthResult> {
    // 1. Kiểm tra phần cứng có hỗ trợ không
    const isAvailable = await checkBiometricHardwareAvailable();
    if (!isAvailable) {
      return { success: false, error: 'HARDWARE_UNAVAILABLE' };
    }

    // 2. Kiểm tra người dùng đã cài vân tay / khuôn mặt chưa
    const isEnrolled = await checkBiometricEnrolled();
    if (!isEnrolled) {
      return { success: false, error: 'NOT_ENROLLED' };
    }

    // 3. Thực thi xác thực an toàn
    try {
      const authSuccess = await promptNativeBiometric({
        title: 'Xác thực sinh trắc học',
        subtitle: 'Sử dụng FaceID hoặc Vân tay để đăng nhập',
        fallbackLabel: 'Nhập mã PIN dự phòng',
      });
      return { success: authSuccess };
    } catch (err: any) {
      return { success: false, error: err.code || 'PERMISSION_DENIED' };
    }
  }
}
```

### Lệnh xác minh & thực thi:
- Kiểm tra quyền camera trên thiết bị Android: `adb shell dumpsys package com.myapp | grep -A 5 "runtime permissions"`
- Thu hồi quyền để test luồng từ chối: `adb shell pm revoke com.myapp android.permission.CAMERA`
- Kiểm tra thiết bị giả lập có cảm biến BLE không: `adb shell pm list features | grep bluetooth`

## 8. Anti-Patterns & Common Traps
- **Spam hộp thoại xin quyền liên tục mỗi khi mở app**: Gây ức chế cho người dùng dẫn tới việc gỡ bỏ ứng dụng.
- **Chỉ cung cấp FaceID mà không có cách đăng nhập bằng mật khẩu**: Người dùng sẽ bị khóa tài khoản nếu cảm biến camera TrueDepth bị hỏng.
- **Thu thập dữ liệu vị trí GPS khi tính năng không hề cần**: Vi phạm chính sách quyền riêng tư của Google Play và Apple App Store.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Có đầy đủ thông điệp giải thích lý do xin quyền (Rationale strings) thân thiện và rõ ràng.
- QG-07: 0 trường hợp crash ứng dụng khi người dùng bấm Từ chối cấp quyền.
- QG-11: Cung cấp đầy đủ cơ chế dự phòng (Fallback) cho 100% các tính năng phần cứng quan trọng.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi deploy.

## 10. Security & Safety Boundaries
- Dữ liệu trích xuất từ camera/mic phải xử lý tại máy (On-device), không tự ý tải lên server khi chưa có sự đồng ý.
- Dữ liệu sinh trắc học (vân tay, khuôn mặt) luôn được bảo vệ trong Secure Enclave / TEE, ứng dụng chỉ nhận kết quả boolean True/False.
- Không bao giờ lưu trữ hardcoded secret hoặc cấp quyền quá mức (over-permissioned IAM).

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Môi trường Mobile & Desktop**: Hỗ trợ Android (Kotlin/Gradle), iOS (Swift/Xcode), Electron (Node.js/Chromium), Tauri (Rust/WebKit).

## 12. Deliverables & Output Artifacts
- Module quản lý quyền và cảm biến thiết bị chuẩn hóa.
- Giao diện giải thích quyền (Permission Rationale Component).
- Bộ kiểm thử unit tests giả lập các trạng thái cấp quyền.

## 13. Related & Complementary Skills
- `dex-ux-accessibility`: Đảm bảo các luồng tương tác phần cứng có hỗ trợ người khiếm thị/khiếm thính.
- `dex-privacy-impact-assessment`: Đánh giá tác động quyền riêng tư khi thu thập dữ liệu cảm biến.
- `dex-android-app-architecture`: Quản lý vòng đời Activity khi khởi tạo camera preview.

## 14. Realistic Usage Example
### Tình huống thực tế:
Một ứng dụng giao hàng cần tính năng quét mã vạch kiện hàng. Áp dụng `dex-native-device-integration`, kỹ sư kiểm tra quyền Camera trước khi mở máy quét. Khi người dùng từ chối quyền, ứng dụng không hề crash mà hiển thị một khung nhập liệu thủ công bằng tay (Fallback) kèm nút hướng dẫn mở Cài đặt nếu muốn bật lại camera. Kết quả loại bỏ hoàn toàn 100% các lỗi crash do camera permission trên toàn hệ thống.
