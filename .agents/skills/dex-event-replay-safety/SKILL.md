---
name: dex-event-replay-safety
description: Architect event replay capabilities with deterministic side-effect suppression, idempotency boundaries, and time-travel projection auditing. Use when rebuilding state from event streams or reprocessing historical records.
---

# dex-event-replay-safety

## 1. Purpose & Scope
Thiết kế và triển khai cơ chế phát lại sự kiện (Event Replay) an toàn tuyệt đối; cô lập và triệt tiêu có chọn lọc các tác dụng phụ bên ngoài (External Side-Effects như gửi email, trừ tiền thẻ tín dụng, gọi webhook đối tác), bảo đảm quá trình tái tạo trạng thái từ Event Stream có tính xác định (deterministic).

## 2. When to Use
- Khi hệ thống kiến trúc Event Sourcing cần tính toán lại toàn bộ dữ liệu trạng thái hiện tại từ đầu lịch sử.
- Khi phát hiện một bug logic trong projection cũ và cần sửa mã nguồn rồi phát lại 2 năm sự kiện lịch sử để sửa sai dữ liệu.
- Khi huấn luyện các mô hình Machine Learning hoặc chạy các kịch bản phân tích hồi quy dựa trên luồng sự kiện thực tế trong quá khứ.

## 3. When NOT to Use
- Khi hệ thống chỉ là CRUD thông thường không lưu trữ nhật ký sự kiện bất biến (Event Log).
- Khi xử lý luồng sự kiện trực tiếp thời gian thực (Live Stream Processing) nơi mọi tác dụng phụ đều bắt buộc phải kích hoạt.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Kho lưu trữ sự kiện bất biến (Event Store), cờ ngữ cảnh `is_replaying`, giao diện trừu tượng hóa các side-effect dispatchers.
- **Quyền hạn truy cập:** Quyền đọc stream sự kiện lịch sử và quyền ghi vào bảng dữ liệu mục tiêu.

## 5. Core Concepts & Taxonomy
- **Side-Effect Suppression:** Cơ chế chặn đứng các lời gọi tới thế giới bên ngoài (external APIs, email, push notification, payment gateways) trong suốt quá trình phát lại sự kiện lịch sử.
- **Deterministic Event Handlers:** Hàm xử lý sự kiện chỉ được phép phụ thuộc vào dữ liệu có trong payload của sự kiện và trạng thái hiện tại, tuyệt đối không phụ thuộc vào `Date.now()` hoặc số ngẫu nhiên.
- **Time-Travel Debugging:** Khả năng dừng và kiểm tra trạng thái chính xác của toàn bộ hệ thống tại một mốc thời gian cụ thể trong quá khứ bằng cách chỉ phát lại sự kiện đến thời điểm đó.

## 6. Step-by-Step Execution Workflow
1. Bọc toàn bộ các dịch vụ gửi thông tin ra bên ngoài (NotificationService, PaymentGateway, WebhookDispatcher) sau một interface kiểm tra cờ `ReplayContext`.
2. Khi khởi động tiến trình Replay: bật cờ `is_replaying = true` trong ngữ cảnh thực thi (Execution Context / AsyncLocalStorage).
3. Định tuyến các side-effects trong chế độ replay vào một NullDispatcher (hoặc ghi log phục vụ kiểm toán mà không thực sự gửi đi).
4. Bảo đảm các hàm xử lý projection sử dụng `event.timestamp` làm mốc thời gian thay vì gọi hàm lấy giờ hệ thống hiện tại.
5. Thực hiện phát lại hàng loạt sự kiện lịch sử theo lô (batching) để tối ưu hóa hiệu năng nạp dữ liệu.
6. Sau khi hoàn tất nạp lịch sử: tắt cờ replay và chuyển consumer sang chế độ lắng nghe sự kiện trực tiếp (Live Mode).

## 7. Concrete Examples
### Ví dụ kiểm soát triệt tiêu side-effects trong Event Handler bằng TypeScript:
```typescript
export class OrderEventHandler {
  constructor(
    private readonly orderRepository: OrderRepository,
    private readonly notificationService: NotificationService
  ) {}

  async handleOrderPaid(event: OrderPaidEvent, context: { isReplaying: boolean }): Promise<void> {
    // 1. Cập nhật trạng thái cơ sở dữ liệu (Luôn thực thi dù là Replay hay Live)
    await this.orderRepository.updateStatus(event.orderId, 'PAID', event.timestamp);

    // 2. Tác dụng phụ bên ngoài: BẮT BUỘC TRIỆT TIÊU khi đang Replay!
    if (context.isReplaying) {
      console.log(`[REPLAY-MODE] Suppressed sending email for order: ${event.orderId}`);
      return;
    }

    // 3. Chỉ gửi email cho khách hàng trong luồng trực tiếp thực tế
    await this.notificationService.sendPaymentReceiptEmail(event.orderId, event.customerEmail);
  }
}
```

## 8. Anti-Patterns & Common Traps
- **Accidental Email Storm:** Phát lại 500,000 sự kiện lịch sử trong đêm và vô tình gửi lại 500,000 email xác nhận đơn hàng cho các khách hàng từ 2 năm trước.
- **Wall-Clock Time Reliance:** Sử dụng `new Date()` trong logic chiếu dữ liệu khiến giá trị tính toán khi replay khác hoàn toàn so với khi chạy trực tiếp ban đầu.
- **Direct External Webhook Calls:** Gọi trực tiếp thư viện `axios` hoặc `fetch` bên trong event handler mà không bọc qua interface kiểm soát ngữ cảnh replay.

## 9. Quality Gates & Acceptance Criteria
- **QG-03**: Quá trình phát lại sự kiện kiểm thử chứng minh 0 cuộc gọi mạng nào được gửi ra ngoài môi trường thử nghiệm.
- **QG-09**: Trạng thái cuối cùng sau khi Replay khớp bit-for-bit với trạng thái snapshot của hệ thống tại cùng thời điểm.
- **QG-10**: Hệ thống có khả năng ngắt tiến trình Replay và tiếp tục lại từ checkpoint gần nhất mà không bị trùng lặp.

## 10. Security & Safety Boundaries
- Cô lập môi trường replay trong một mạng sandbox riêng biệt không có route ra Internet công cộng.
- Kiểm soát quyền hạn của tài khoản chạy replay: chỉ cấp quyền đọc trên Event Store và quyền ghi trên bảng projection mới.

## 11. Platform Adapters
- **Event Stores**: EventStoreDB, Apache Kafka, AWS Kinesis.
- **Frameworks**: Axon Framework, Eventuate, custom TypeScript Event Sourcing.

## 12. Deliverables & Output Artifacts
- Interface và cơ chế quản lý Execution Context với cờ `is_replaying`.
- Bộ Mock/Null Dispatchers cho toàn bộ dịch vụ ngoại vi.
- Kiểm thử tự động chứng minh không có side-effect rò rỉ trong quá trình Replay.

## 13. Related & Complementary Skills
dex-cqrs-projection-management, dex-idempotent-operations, dex-event-driven-architecture

## 14. Realistic Usage Example
```powershell
# Chạy lệnh replay sự kiện với cơ chế triệt tiêu side-effects
python scripts/replay_events.py --stream orders --from 2026-01-01 --suppress-side-effects
```
