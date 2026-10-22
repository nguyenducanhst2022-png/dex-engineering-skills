---
name: dex-notification-delivery
description: Architect multi-channel notification systems (Email, SMS, Push, In-app), dynamic templating, delivery providers (SendGrid/Twilio/FCM), rate limiting, and failure fallbacks. Use when dispatching alerts, transactional messages, or multi-channel notifications.
---

# dex-notification-delivery

## 1. Purpose & Scope
Thiết kế và triển khai kiến trúc phân phối thông báo đa kênh (Multi-Channel Notification Delivery: Email, SMS, Web Push, In-app Bell); quản lý mẫu thông báo động (Dynamic Templates), tích hợp các nhà cung cấp dịch vụ viễn thông (SendGrid, Twilio, Firebase Cloud Messaging, Zalo ZNS), kiểm soát tần suất thông báo (Rate Limiting) và cơ chế chuyển đổi dự phòng (Fallback Providers) khi một kênh bị lỗi.

## 2. When to Use
- Khi ứng dụng cần gửi mã xác thực OTP qua SMS, gửi hóa đơn qua Email và gửi thông báo đơn hàng qua Push Notification.
- Khi người dùng phàn nàn bị 'dội bom' thông báo (Spam notification) hoặc thông báo OTP đến quá chậm.
- Khi nhà cung cấp dịch vụ gửi SMS chính bị sự cố nghẽn mạng cần tự động chuyển sang nhà cung cấp phụ trong vòng 5 giây.

## 3. When NOT to Use
- Giao tiếp thời gian thực hai chiều trong một phiên làm việc trực tiếp (dùng `dex-realtime-protocols`).
- Ghi log hệ thống cho đội ngũ kỹ thuật (dùng `dex-production-monitoring`).

## 4. Prerequisites & Input Context
**Đầu vào cần thiết:**
- Danh sách các kênh thông báo và nhà cung cấp dịch vụ tích hợp.
- Mẫu nội dung thông báo (Templates with handlebars/mustache).
- Tùy chọn ưu tiên thông báo của người dùng (User notification preferences).

**Điều kiện tiên quyết:**
- Có tài khoản API và credentials hợp lệ của các nhà cung cấp (SendGrid, Twilio, FCM).
- Có hàng đợi tin nhắn (Queue) để gửi thông báo chạy ngầm không chặn HTTP thread.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**: Nắm vững cơ chế vận hành theo chuẩn Agent Skills, tuân thủ nghiêm ngặt tính xác định và ranh giới trách nhiệm.
- **Quy tắc quyết định kỹ thuật**:
- **Bắt Buộc Chạy Ngầm Bất Đồng Bộ**: Mọi thao tác gửi Email/SMS đều bắt buộc phải chạy qua Background Job Queue; tuyệt đối không gọi API của bên thứ ba trực tiếp trong luồng request chính của người dùng.
- **Bảo Vệ Chi Phí OTP**: Bắt buộc phải có Captcha (Cloudflare Turnstile) trước khi kích hoạt gửi OTP SMS để tránh bị tin tặc tấn công rút cạn ngân sách tin nhắn (SMS Toll Fraud).
- **Mẫu Nội Dung Phải Có Plaintext**: Mọi email HTML gửi đi đều bắt buộc phải có phiên bản văn bản thuần (Plain Text version) đi kèm để tránh bị rơi vào hộp thư Spam của Gmail/Outlook.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Nhà cung cấp SMS bị timeout làm treo hệ thống**: API gửi OTP bị đơ 30 giây -> Khắc phục: Đặt timeout nghiêm ngặt 3 giây cho lời gọi SMS và kích hoạt ngay kênh Zalo ZNS hoặc SMS dự phòng.
- **Email rơi vào Spam của người dùng**: Do thiếu cấu hình định danh tên miền -> Khắc phục: Kiểm tra đầy đủ bản ghi SPF, DKIM và DMARC của tên miền gửi thư.

## 6. Step-by-Step Execution Workflow
1. Thiết kế Hợp đồng Thông báo Chuẩn: Định nghĩa đối tượng `NotificationPayload` gồm `userId`, `channels`, `templateId`, `data`.
2. Kiểm tra tùy chọn người dùng (User Preferences): Kiểm tra xem người dùng có tắt thông báo qua Email hoặc có đang trong khung giờ Không Làm Phiền (Do Not Disturb) hay không.
3. Kiểm tra Tần suất Gửi (Rate Limiting): Giới hạn tối đa (ví dụ: tối đa 3 tin nhắn OTP trong 5 phút cho cùng 1 số điện thoại) để chống spam và thất thoát chi phí SMS.
4. Render Mẫu Động: Kết hợp template với dữ liệu thời gian thực, tự động làm sạch nội dung chống injection.
5. Đẩy vào hàng đợi phân phối tương ứng cho từng kênh.
6. Cơ chế Fallback Nhà Cung Cấp: Nếu gửi qua Provider A (ví dụ SendGrid) bị lỗi hoặc timeout quá 3 giây, tự động kích hoạt Provider B (ví dụ AWS SES) gửi thay thế.
7. Lưu trữ trạng thái và lịch sử thông báo vào Database để hiển thị trên quả chuông thông báo In-app.

## 7. Concrete Examples
### Ví dụ triển khai chuẩn mực:
```typescript
// src/notifications/notificationDispatcher.ts
export async function dispatchNotification(payload: NotificationRequest) {
  const userPrefs = await getUserPreferences(payload.userId);
  
  if (payload.channels.includes('EMAIL') && userPrefs.emailEnabled) {
    await emailQueue.add('send-email', {
      to: userPrefs.email,
      template: payload.template,
      data: payload.data
    });
  }
  if (payload.channels.includes('IN_APP')) {
    await inAppNotificationService.create(payload.userId, payload.data);
  }
}
```

### Lệnh xác minh & thực thi:
- Kiểm tra gửi thử email trên môi trường test: `npm run send:test-email -- user@example.com`
- Kiểm tra trạng thái webhook nhận báo cáo giao hàng (Delivery Receipt): `curl -X POST http://localhost:3000/webhooks/sendgrid`
- Chạy test phân phối thông báo: `npm test -- tests/notifications/delivery.spec.ts`

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước kiểm tra biên và giả định hệ thống luôn ở trạng thái lý tưởng.
- **Anti-Pattern 2**: Không ghi nhận nhật ký kiểm toán hoặc bỏ qua việc xử lý ngoại lệ lúc runtime.
- **Trap**: Bỏ qua các rào chắn an toàn hoặc cố tình chạy script không qua kiểm thử tự động.

## 9. Quality Gates & Acceptance Criteria
- QG-01: 100% các cuộc gọi ra nhà cung cấp bên ngoài đều có Timeout <= 3 giây.
- QG-05: Kịch bản kiểm tra Provider Fallback tự động gửi qua kênh thứ hai khi kênh thứ nhất giả lập mã lỗi 500.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động trước khi coi là hoàn thành.

## 10. Security & Safety Boundaries
- Tuyệt đối không ghi nội dung mã OTP bí mật vào log hệ thống ở dạng bản rõ.
- Tôn trọng quyền riêng tư: Luôn có liên kết hủy đăng ký (`Unsubscribe link`) ở chân trang của mọi email marketing theo quy định của luật bảo vệ người tiêu dùng.
- Không bao giờ thực thi mã nguồn hoặc thay đổi cấu hình trên môi trường sản xuất mà thiếu cơ chế rollback an toàn.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Có thể kích hoạt trực tiếp từ terminal hoặc extension tương thích trong VS Code / Cursor / Windsurf.

## 12. Deliverables & Output Artifacts
- Bộ điều phối thông báo đa kênh (`src/notifications/notificationDispatcher.ts`).
- Các Adapters nhà cung cấp dịch vụ (`SendGridAdapter.ts`, `TwilioAdapter.ts`).
- File kiểm thử tự động cơ chế fallback.

## 13. Related & Complementary Skills
- `dex-development-workflow`: Quy trình phát triển tiêu chuẩn.
- `dex-code-verification`: Xác minh chất lượng và tính đúng đắn của mã nguồn.
- `dex-master-orchestrator`: Bộ điều phối trung tâm kết nối kỹ năng này với các kỹ năng khác trong hệ thống.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư hoặc AI Agent tiếp nhận yêu cầu liên quan đến **dex-notification-delivery**.
1. Đọc kỹ đầu vào và các ràng buộc kỹ thuật tại mục 4.
2. Thực thi tuần tự 6 bước trong Workflow tại mục 6.
3. Chạy các lệnh kiểm chứng tại mục 7 và đối chiếu với Quality Gates tại mục 9.
4. Đóng gói deliverables theo danh sách tại mục 12 và báo cáo kết quả kèm bằng chứng xác thực.
