---
name: dex-web-push-permission-flow
description: Design high-conversion, contextual Web Push notification permission request flows, VAPID key authentication, and graceful push message delivery with fallback notification badges. Use when implementing user notifications, engagement alerts, or real-time web messaging.
---

# dex-web-push-permission-flow

## 1. Purpose & Scope
Thiết kế luồng yêu cầu quyền nhận thông báo đẩy web (Web Push Notification Permission) theo ngữ cảnh với tỷ lệ chấp thuận cao; thiết lập cơ chế xác thực khóa VAPID an toàn, quản lý vòng đời đăng ký PushSubscription và xử lý thông điệp đẩy nền kèm biểu tượng chỉ báo số lượng.

## 2. When to Use
- Khi triển khai tính năng gửi thông báo tức thời cho người dùng trên trình duyệt máy tính và điện thoại.
- Khi muốn cải thiện tỷ lệ người dùng bấm 'Cho phép' nhận thông báo thay vì bấm 'Chặn' do bị hỏi quá đột ngột.
- Khi cần cấu hình bảo mật truyền tin giữa máy chủ ứng dụng và dịch vụ Push Service của trình duyệt.

## 3. When NOT to Use
- Khi người dùng chỉ cần nhận thông báo qua email hoặc tin nhắn SMS.
- Khi ứng dụng đang trong môi trường phát triển cục bộ không có kết nối HTTPS.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Cặp khóa định danh VAPID (Public/Private Key), quyền HTTPS, Service Worker đã được đăng ký thành công.
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn trong phạm vi dự án, không can thiệp vào tài nguyên sản xuất khi chưa có phê duyệt.

## 5. Core Concepts & Taxonomy
- **Contextual Pre-Permission Primer:** Hiển thị một modal giải thích lý do trước khi kích hoạt hộp thoại xin quyền mặc định của trình duyệt.
- **VAPID (Voluntary Application Server Identification):** Khóa ký điện tử xác thực máy chủ gửi tin nhắn với dịch vụ thông báo đẩy.
- **Notification Action Buttons:** Đính kèm các nút thao tác nhanh (như 'Xem chi tiết', 'Bỏ qua') ngay trên thông báo hệ thống.

## 6. Step-by-Step Execution Workflow
1. Tạo cặp khóa VAPID an toàn trên máy chủ backend.
2. Xác định thời điểm vàng để xin quyền (ví dụ: ngay sau khi người dùng bấm 'Theo dõi đơn hàng').
3. Hiển thị giao diện giải thích giá trị của việc nhận thông báo (Soft Ask Prompt).
4. Khi người dùng đồng ý, gọi API `Notification.requestPermission()` và chuyển đổi `pushManager.subscribe()`.
5. Gửi đối tượng `PushSubscription` lên máy chủ backend để lưu vào cơ sở dữ liệu.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```typescript
// Contextual Push Permission Subscription
export async function subscribeUserToPush(publicVapidKey: string) {
  const registration = await navigator.serviceWorker.ready;
  
  // Convert URL base64 to Uint8Array for applicationServerKey
  const convertedVapidKey = urlBase64ToUint8Array(publicVapidKey);
  
  const subscription = await registration.pushManager.subscribe({
    userVisibleOnly: true,
    applicationServerKey: convertedVapidKey
  });
  
  // Send subscription object to backend server
  await fetch('/api/push/subscribe', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(subscription)
  });
  return subscription;
}
```

## 8. Anti-Patterns & Common Traps
- Bắn pop-up xin quyền thông báo ngay ở mili-giây đầu tiên khi người dùng vừa đặt chân vào trang web.
- Gửi các thông báo rác tiếp thị với tần suất dày đặc khiến người dùng vào cài đặt trình duyệt chặn hoàn toàn quyền của trang.
- Không xử lý trường hợp người dùng chọn 'Từ chối' (Denied), dẫn đến việc liên tục hiển thị lại nhắc nhở gây khó chịu.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Tỷ lệ chấp nhận quyền thông báo tăng tối thiểu 35% so với việc xin quyền thô không có giao diện đệm.
- QG-02: Khóa riêng VAPID Private Key được lưu trữ an toàn trong Secret Manager, không bị lộ ra frontend.
- QG-03: Thông báo hiển thị đúng tiêu đề, nội dung và icon đại diện trên cả Windows, macOS và Android.

## 10. Security & Safety Boundaries
- Bảo vệ thông điệp đẩy bằng mã hóa payload tiêu chuẩn RFC 8291; không gửi các dữ liệu nhạy cảm cá nhân trong nội dung thông báo thô.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Module kích hoạt quyền thông báo theo ngữ cảnh `PushPermissionManager.ts`.
1. Kịch bản Service Worker lắng nghe sự kiện push `sw-push-handler.js`.

## 13. Related & Complementary Skills
- [`dex-notification-delivery`](.agents/skills/dex-notification-delivery/SKILL.md)
- [`dex-progressive-web-apps`](.agents/skills/dex-progressive-web-apps/SKILL.md)
- [`dex-user-consent-ux`](.agents/skills/dex-user-consent-ux/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Trang web đặt đồ ăn trực tuyến muốn thông báo trạng thái tài xế cho khách hàng. Áp dụng `dex-web-push-permission-flow` để chỉ hiển thị hộp thoại xin quyền sau khi đơn hàng được thanh toán thành công, giải thích rõ 'Bật thông báo để biết khi nào tài xế tới', giúp nâng tỷ lệ cấp quyền từ 12% lên 68%.
