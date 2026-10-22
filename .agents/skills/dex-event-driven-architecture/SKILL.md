---
name: dex-event-driven-architecture
description: Architect event-driven distributed systems, pub/sub topologies, event schemas, Outbox Pattern, message brokers (Kafka/RabbitMQ), and consumer error handling. Use when decoupling services, processing domain events, or ensuring reliable event delivery.
---

# dex-event-driven-architecture

## 1. Purpose & Scope
Thiết kế và triển khai kiến trúc hướng sự kiện (Event-Driven Architecture - EDA); phân tách sự phụ thuộc giữa các dịch vụ thông qua cơ chế Publish/Subscribe (Kafka, RabbitMQ); bảo đảm sự kiện được phát đi tin cậy 100% không bị thất thoát thông qua Mẫu hình Hộp thư đi (Transactional Outbox Pattern) và xử lý lỗi người tiêu thụ (Consumer Error Handling).

## 2. When to Use
- Khi một hành động nghiệp vụ cần kích hoạt hàng loạt hệ thống khác nhau (ví dụ: Đơn hàng thanh toán thành công -> Cần trừ kho, gửi hóa đơn, tích điểm, gửi thông báo cho shipper).
- Khi các dịch vụ đang gọi HTTP lẫn nhau quá nhiều tạo thành một chuỗi phụ thuộc nghẽn mạng (Distributed Monolith).
- Khi cần ghi nhận toàn bộ lịch sử biến đổi trạng thái của hệ thống theo thời gian (Audit trail / Event Sourcing).

## 3. When NOT to Use
- Các tác vụ nghiệp vụ nội bộ trong cùng một module đơn giản chỉ cần gọi hàm thông thường.
- Hệ thống quy mô nhỏ mà độ phức tạp của việc vận hành Message Broker vượt quá lợi ích mang lại.

## 4. Prerequisites & Input Context
**Đầu vào cần thiết:**
- Danh sách các Sự kiện Nghiệp vụ (Domain Events: `OrderCreated`, `PaymentReceived`, `InventoryReserved`).
- Định dạng Schema của Sự kiện (JSON Schema / CloudEvents / Apache Avro / Protobuf).
- Hạ tầng Message Broker (Apache Kafka, RabbitMQ, Redis Streams, Google Cloud Pub/Sub).

**Điều kiện tiên quyết:**
- Message Broker đã được thiết lập các Topics/Queues với cơ chế phân vùng (Partitioning) và sao lưu (Replication).
- Database hỗ trợ ACID Transaction để lưu trữ bảng Outbox cùng với bảng dữ liệu nghiệp vụ.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**: Nắm vững cơ chế vận hành theo chuẩn Agent Skills, tuân thủ nghiêm ngặt tính xác định và ranh giới trách nhiệm.
- **Quy tắc quyết định kỹ thuật**:
- **Không Bắn Event Trực Tiếp Trước Khi Commit DB**: Tuyệt đối không gọi `broker.send()` trước khi câu lệnh `COMMIT` database thành công; luôn dùng Outbox Pattern.
- **Sự Kiện Là Sự Thật Bất Biến (Immutable Facts)**: Sự kiện đại diện cho một điều ĐÃ XẢY RA trong quá khứ (đặt tên ở thì quá khứ: `OrderPaid`); không bao giờ được phép sửa đổi hoặc xóa sự kiện đã phát đi.
- **Tương Thích Ngược Schema**: Khi nâng cấp Event Schema, chỉ được thêm trường mới tùy chọn; cấm xóa trường cũ hoặc đổi kiểu dữ liệu của trường đang có.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Sự kiện kép (Duplicate Events)**: Do mạng chập chờn, broker gửi lại cùng một sự kiện 2 lần -> Khắc phục: Phía Consumer bắt buộc phải lưu `processed_event_ids` để bỏ qua các sự kiện đã xử lý.
- **Consumer bị nghẽn (High Consumer Lag)**: Tốc độ tạo sự kiện nhanh gấp 10 lần tốc độ xử lý của Consumer -> Khắc phục: Tăng số lượng Partition trên Kafka và tăng số lượng Consumer instances chạy song song.

## 6. Step-by-Step Execution Workflow
1. Thiết kế Event Schema tuân theo chuẩn **CloudEvents**: Bao gồm `id`, `source`, `type`, `time`, `datacontenttype`, `data`.
2. Áp dụng **Transactional Outbox Pattern**: Khi lưu dữ liệu nghiệp vụ vào DB, đồng thời ghi sự kiện vào bảng `outbox_events` trong CÙNG MỘT TRANSACTION duy nhất để đảm bảo 100% không bao giờ bị mất sự kiện kể cả khi broker sập.
3. Triển khai Outbox Publisher Worker: Định kỳ quét bảng `outbox_events` hoặc dùng CDC (Debezium) để bắn sự kiện sang Message Broker rồi đánh dấu đã gửi.
4. Phía Consumer: Lắng nghe sự kiện, kiểm tra Idempotency Key để đảm bảo không xử lý lặp lại thông điệp (At-Least-Once Delivery).
5. Thiết lập Dead-Letter Queue (DLQ) cho các sự kiện không thể tiêu thụ sau số lần retry quy định.
6. Theo dõi Consumer Lag để phát hiện kịp thời tình trạng nghẽn hàng đợi.

## 7. Concrete Examples
### Ví dụ triển khai chuẩn mực:
```json
// CloudEvents Specification Format
{
  "specversion": "1.0",
  "type": "com.shop.order.paid",
  "source": "/services/order-service",
  "id": "evt_a8f9c123-4567",
  "time": "2026-10-22T14:00:00Z",
  "datacontenttype": "application/json",
  "data": {
    "orderId": "ord_9999",
    "customerId": "cust_1234",
    "amountCents": 250000,
    "currency": "VND"
  }
}
```

### Lệnh xác minh & thực thi:
- Kiểm tra bảng Outbox còn tồn đọng không: `SELECT count(*) FROM outbox_events WHERE status = 'PENDING';`
- Kiểm tra Consumer Lag trên Kafka: `kafka-consumer-groups --bootstrap-server localhost:9092 --describe --group order-group`
- Chạy unit test xử lý sự kiện: `npm test -- tests/events/orderEvents.spec.ts`

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước kiểm tra biên và giả định hệ thống luôn ở trạng thái lý tưởng.
- **Anti-Pattern 2**: Không ghi nhận nhật ký kiểm toán hoặc bỏ qua việc xử lý ngoại lệ lúc runtime.
- **Trap**: Bỏ qua các rào chắn an toàn hoặc cố tình chạy script không qua kiểm thử tự động.

## 9. Quality Gates & Acceptance Criteria
- QG-01: 100% sự kiện được sinh ra tuân thủ đúng định dạng CloudEvents schema.
- QG-05: Kịch bản Outbox Pattern đảm bảo khi DB rollback thì không có sự kiện nào bị phát nhầm ra ngoài.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động trước khi coi là hoàn thành.

## 10. Security & Safety Boundaries
- Mã hóa dữ liệu nhạy cảm trong payload của sự kiện nếu truyền qua hạ tầng mạng công cộng.
- Kiểm soát chặt chẽ quyền đọc/ghi trên từng Topic của Message Broker bằng SASL/SSL Authentication.
- Không bao giờ thực thi mã nguồn hoặc thay đổi cấu hình trên môi trường sản xuất mà thiếu cơ chế rollback an toàn.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Có thể kích hoạt trực tiếp từ terminal hoặc extension tương thích trong VS Code / Cursor / Windsurf.

## 12. Deliverables & Output Artifacts
- Định nghĩa Event Schemas (`src/events/schemas/orderPlaced.schema.ts`).
- Bộ thư viện Outbox Publisher (`src/events/outboxPublisher.ts`).
- Base Event Consumer có xử lý Idempotent (`src/events/baseConsumer.ts`).

## 13. Related & Complementary Skills
- `dex-development-workflow`: Quy trình phát triển tiêu chuẩn.
- `dex-code-verification`: Xác minh chất lượng và tính đúng đắn của mã nguồn.
- `dex-master-orchestrator`: Bộ điều phối trung tâm kết nối kỹ năng này với các kỹ năng khác trong hệ thống.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư hoặc AI Agent tiếp nhận yêu cầu liên quan đến **dex-event-driven-architecture**.
1. Đọc kỹ đầu vào và các ràng buộc kỹ thuật tại mục 4.
2. Thực thi tuần tự 6 bước trong Workflow tại mục 6.
3. Chạy các lệnh kiểm chứng tại mục 7 và đối chiếu với Quality Gates tại mục 9.
4. Đóng gói deliverables theo danh sách tại mục 12 và báo cáo kết quả kèm bằng chứng xác thực.
