---
name: dex-distributed-consistency
description: Analyze, design, and resolve distributed consistency challenges across microservices, including Saga patterns, transactional outboxes, idempotency keys, and conflict resolution. Use when splitting monoliths or managing multi-database transactions.
---

# dex-distributed-consistency

## 1. Purpose & Scope
Phân tích, thiết kế và xử lý các bài toán nhất quán dữ liệu phân tán (Distributed Consistency) giữa các microservices và cơ sở dữ liệu phân tán; áp dụng mô hình Saga, Transactional Outbox, Idempotency Keys và các chiến lược giải quyết xung đột (Conflict Resolution) thay thế cho distributed transactions (2PC) nặng nề.

## 2. When to Use
- Tách ứng dụng đơn khối (Monolith) thành Microservices khiến một nghiệp vụ phải cập nhật dữ liệu trên nhiều cơ sở dữ liệu độc lập.
- Hệ thống xử lý thanh toán, trừ tồn kho và gửi email thông báo cần đảm bảo tính nhất quán cuối cùng (Eventual Consistency).
- Dữ liệu bị sai lệch, mất mát hoặc bị nhân đôi do network partition và service retry.

## 3. When NOT to Use
- Không áp dụng kiến trúc Saga phức tạp nếu toàn bộ dữ liệu vẫn nằm chung trong một cơ sở dữ liệu quan hệ (chỉ cần ACID transaction đơn giản).
- Không áp dụng cho các dữ liệu phân tích chỉ đọc (read-only analytics).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Luồng nghiệp vụ phân tán (Business transaction workflow).
- Danh sách các dịch vụ và cơ sở dữ liệu tham gia.
- Broker tin cậy cho messaging (Kafka, RabbitMQ, SQS).
- **Điều kiện tiên quyết**:
- Các dịch vụ có cơ chế lưu trữ bền vững (Durable storage) và hỗ trợ giao dịch cục bộ (Local ACID transaction).

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Định lý CAP và BASE: Chấp nhận tính Nhất quán cuối cùng (Eventual Consistency) để đổi lấy tính Sẵn sàng (Availability) và Khả năng chịu lỗi phân vùng (Partition Tolerance).
- Transactional Outbox Pattern: Ghi sự kiện vào bảng Outbox trong cùng một local database transaction với dữ liệu nghiệp vụ, sau đó dùng Debezium hoặc Poller đẩy sang Message Broker để chống mất tin.
- Idempotency Key: Khóa duy nhất đi kèm mỗi request giúp server phát hiện và bỏ qua các lệnh trùng lặp do mạng thử lại (retry).
- **Quy tắc quyết định kỹ thuật**:
- Với chuỗi hành động có khả năng lỗi ở giữa: bắt buộc thiết kế các hành động bù trừ (Compensating Transactions - ví dụ: Hoàn tiền nếu đặt vé máy bay thất bại).
- Mọi message consumer phải thiết kế có tính chất bình thản (Idempotent Consumer).
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Thực hiện gọi REST API gửi sự kiện ngay giữa database transaction, nếu commit DB thất bại nhưng sự kiện đã bắn đi thì dữ liệu vĩnh viễn bị lệch.

## 6. Step-by-Step Execution Workflow
1. Vẽ sơ đồ chuỗi trạng thái và các điểm thất bại tiềm năng trong quy trình phân tán.
2. Thiết kế bảng `outbox` và bảng `idempotency_records` trong database của mỗi service.
3. Triển khai Saga Orchestrator hoặc Choreography với các bước bù trừ rõ ràng.
4. Tích hợp cơ chế kiểm tra Idempotency Key tại tầng API và Consumer.
5. Viết kịch bản Chaos test ngắt kết nối giữa chừng để chứng minh dữ liệu tự phục hồi về trạng thái nhất quán.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```sql
-- Bảng Transactional Outbox bảo đảm không mất sự kiện
CREATE TABLE outbox_events (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    aggregate_type VARCHAR(64) NOT NULL,
    aggregate_id VARCHAR(64) NOT NULL,
    event_type VARCHAR(64) NOT NULL,
    payload JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    processed BOOLEAN DEFAULT FALSE
);
```

### Lệnh xác minh & thực thi:
```bash
# Kiểm thử kịch bản gửi lặp lại 5 lần cùng 1 Idempotency-Key
for i in {1..5}; do curl -X POST http://localhost:8080/api/v1/orders -H 'Idempotency-Key: test-uuid-001' -d '{"amount": 100}'; done
```

## 8. Anti-Patterns & Common Traps
- Lạm dụng Two-Phase Commit (2PC) trên môi trường Cloud/Microservices gây nghẽn và sập hệ thống khi có mạng chập chờn.
- Viết Compensating transaction thiếu trường hợp xử lý lỗi khi chính hành động bù trừ cũng bị fail.

## 9. Quality Gates & Acceptance Criteria
- 0 giao dịch bị treo ở trạng thái không xác định sau khi giả lập mất kết nối mạng giữa các dịch vụ.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Khóa Idempotency và dữ liệu Event Payload phải được mã hóa nếu chứa thông tin PII hoặc thẻ tín dụng.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ thống hỗ trợ**: Linux (CI/CD runners), macOS, Windows 11 PowerShell/WSL2.

## 12. Deliverables & Output Artifacts
- Sơ đồ kiến trúc Saga và danh sách Compensating actions.
- Mã nguồn triển khai Transactional Outbox và Idempotent Handler.

## 13. Related & Complementary Skills
dex-distributed-tracing, dex-database-design, dex-service-failover

## 14. Realistic Usage Example
### Tình huống thực tế:
Một sàn thương mại điện tử gặp sự cố khách hàng bị trừ tiền trong ví nhưng đơn hàng không được tạo do mạng timeout. Áp dụng Transactional Outbox kết hợp Saga Orchestration, khi bước tạo đơn lỗi, orchestrator tự động phát lệnh hoàn tiền vào ví trong vòng 3 giây, loại bỏ hoàn toàn các khiếu nại của khách.
