---
name: dex-web-permission-ux
description: Design progressive, user-centric browser permission request experiences for Camera, Microphone, Geolocation, Notifications, and Storage with pre-prompt primers and graceful denial recovery. Use when improving permission opt-in rates, eliminating prompt fatigue, or guiding users through browser settings unlock.
---

# dex-web-permission-ux

## 1. Purpose & Scope
Thiết kế trải nghiệm yêu cầu quyền hạn trình duyệt (Browser Permissions UX) tiến bộ và lấy người dùng làm trung tâm cho Camera, Microphone, Vị trí (Geolocation), Thông báo và Lưu trữ; sử dụng màn hình giải thích trước (Pre-Prompt Primers), xử lý khéo léo khi người dùng từ chối và hướng dẫn mở lại quyền trong cài đặt trình duyệt.

## 2. When to Use
- Khi ứng dụng cần truy cập các phần cứng nhạy cảm (Webcam, Mic) hoặc dữ liệu định vị địa lý của người dùng.
- Khi tỷ lệ người dùng bấm 'Chặn' quyền quá cao làm tê liệt tính năng chính của ứng dụng.
- Khi cần kiểm tra trạng thái quyền bằng Permissions API trước khi thực hiện thao tác gọi thiết bị.

## 3. When NOT to Use
- Khi ứng dụng không sử dụng bất kỳ Web API nào yêu cầu sự đồng ý của người dùng.
- Khi thiết lập quyền truy cập cơ sở dữ liệu trên máy chủ backend.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Trình duyệt hỗ trợ `navigator.permissions.query()`, hiểu biết về 3 trạng thái quyền: `'granted'`, `'prompt'`, `'denied'`.
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; tuyệt đối không can thiệp trái phép vào hệ thống của bên thứ ba.

## 5. Core Concepts & Taxonomy
- **Contextual Value Exchange:** Chỉ xin quyền ngay tại thời điểm người dùng bấm vào một tính năng cụ thể mang lại giá trị rõ ràng.
- **Pre-Permission Primer Screen:** Giao diện nội bộ giải thích rõ lý do cần quyền và cách thức sử dụng dữ liệu trước khi kích hoạt hộp thoại hệ thống.
- **Denied State Recovery Flow:** Khi quyền bị khóa ở trạng thái 'denied', cung cấp hướng dẫn bằng hình ảnh từng bước giúp người dùng mở lại cài đặt trình duyệt.

## 6. Step-by-Step Execution Workflow
1. Truy vấn trạng thái quyền hiện tại bằng `navigator.permissions.query({ name: 'camera' })`.
2. Nếu trạng thái là `'prompt'`, hiển thị modal giải thích lý do trước khi kích hoạt hành động.
3. Chỉ gọi API thật (`navigator.mediaDevices.getUserMedia`) sau khi người dùng bấm xác nhận trên modal giải thích.
4. Nếu người dùng từ chối hoặc trạng thái là `'denied'`, hiển thị banner hướng dẫn mở quyền kèm hình ảnh minh họa cho trình duyệt tương ứng.
5. Lắng nghe sự kiện `permissionStatus.onchange` để tự động kích hoạt tính năng ngay khi người dùng cấp lại quyền.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```typescript
// Contextual Permission Request Flow
export async function requestCameraAccess(): Promise<MediaStream | null> {
  const status = await navigator.permissions.query({ name: 'camera' as PermissionName });
  
  if (status.state === 'denied') {
    showBrowserSettingsGuide('camera');
    return null;
  }

  if (status.state === 'prompt') {
    const userAgreed = await showPrePromptPrimerModal({
      title: 'Cho phép truy cập Camera để quét mã QR',
      description: 'Hình ảnh chỉ được xử lý trực tiếp trên thiết bị của bạn và không tải lên máy chủ.'
    });
    if (!userAgreed) return null;
  }

  try {
    return await navigator.mediaDevices.getUserMedia({ video: true });
  } catch (err) {
    console.warn('User dismissed native prompt', err);
    return null;
  }
}
```

## 8. Anti-Patterns & Common Traps
- Vừa vào trang web đã lập tức kích hoạt hộp thoại hỏi xin vị trí hoặc camera của người dùng khiến họ hoảng sợ và bấm 'Chặn'.
- Không cung cấp giải pháp thay thế khi người dùng từ chối (ví dụ: không cho nhập địa chỉ thủ công khi họ không muốn chia sẻ GPS).
- Hiển thị thông báo lỗi chung chung 'Lỗi thiết bị' khi thực tế là do người dùng chưa cấp quyền truy cập.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Tỷ lệ chấp thuận cấp quyền tăng tối thiểu 40% nhờ màn hình giải thích ngữ cảnh.
- QG-02: Luôn có luồng nhập liệu thay thế cho người dùng khi họ từ chối cấp quyền.
- QG-03: Giao diện hướng dẫn mở khóa quyền cài đặt hiển thị chính xác theo từng loại trình duyệt (Chrome, Safari, Firefox).

## 10. Security & Safety Boundaries
- Chỉ yêu cầu các quyền thực sự cần thiết cho tính năng; ngắt kết nối stream camera/mic ngay lập tức khi người dùng rời khỏi màn hình sử dụng.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Hoạt động phân tích hoàn toàn hợp pháp, minh bạch và có sự ủy quyền chính thức từ chủ sở hữu hệ thống.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Module quản trị quyền hạn người dùng `PermissionManager.ts`.
1. Component hướng dẫn mở lại cài đặt trình duyệt `PermissionRecoveryGuide.tsx`.

## 13. Related & Complementary Skills
- [`dex-user-consent-ux`](.agents/skills/dex-user-consent-ux/SKILL.md)
- [`dex-web-push-permission-flow`](.agents/skills/dex-web-push-permission-flow/SKILL.md)
- [`dex-native-device-integration`](.agents/skills/dex-native-device-integration/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Ứng dụng họp trực tuyến có tỷ lệ người dùng bị kẹt ở màn hình vào phòng do chặn mic. Kỹ sư kích hoạt `dex-web-permission-ux`, thêm màn hình kiểm tra thiết bị trước khi vào phòng và cung cấp hướng dẫn bấm vào biểu tượng ổ khóa trên thanh địa chỉ để cấp lại quyền, giúp giảm 85% số lượng vé hỗ trợ khách hàng.
