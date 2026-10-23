---
name: dex-exactly-once-claims-audit
description: Audit and rigorously verify distributed message delivery guarantees, debunking impossible exactly-once claims and enforcing idempotent consumer patterns with transactional outboxes. Use when verifying payment pipelines or critical distributed transactions.
---

# dex-exactly-once-claims-audit

## 1. Purpose & Scope
Kiểm toán và phản biện các tuyên bố bảo đảm phân phối tin nhắn 'Exactly-Once' trong hệ thống phân tán; phân tích giới hạn của bài toán Hai Vị Tướng (Two Generals' Problem) và FLP Impossibility, thiết kế giải pháp thực tế dựa trên phân phối At-Least-Once kết hợp xử lý Idempotent Consumer và Transactional Outbox.

## 2. When to Use
- Khi kiểm toán hệ thống thanh toán, kế toán hoặc xử lý đơn hàng có rủi ro trùng lặp giao dịch tài chính.
- Khi đánh giá đề xuất kỹ thuật tuyên bố hệ thống có thể đạt được 'end-to-end exactly-once' qua mạng không đáng tin cậy.
- Khi thiết kế cơ chế bảo vệ chống trùng lặp thông điệp (deduplication) trên hạ tầng Kafka, RabbitMQ hoặc AWS SQS.

## 3. When NOT to Use
- Khi dữ liệu chỉ là số liệu đo lường IoT cảm biến hoặc log phân tích thông thường cho phép sai số nhỏ.
- Khi toàn bộ quá trình đọc ghi chỉ diễn ra trong một tiến trình đơn lẻ có giao dịch ACID trên một cơ sở dữ liệu duy nhất.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Sơ đồ luồng dữ liệu thông điệp phân tán, cấu hình broker/queue, cơ chế lưu trữ deduplication key và database transaction log.
- **Quyền hạn truy cập:** Quyền kiểm tra mã nguồn consumer và lịch sử xử lý thông điệp.

## 5. Core Concepts & Taxonomy
- **Network Impossibility Proof:** Không thể bảo đảm exactly-once delivery qua mạng vật lý nếu không có sự phối hợp giữa stateful deduplication và transactional boundary tại tầng ứng dụng.
- **Transactional Outbox Pattern:** Ghi thông điệp cần gửi vào bảng `outbox` trong cùng một database transaction với dữ liệu nghiệp vụ, sau đó worker riêng biệt đọc và gửi đi.
- **Idempotency Key & Deduplication Window:** Khóa duy nhất đại diện cho giao dịch được lưu trữ trong bảng `processed_messages` với thời gian tồn tại (TTL) xác định.

## 6. Step-by-Step Execution Workflow
1. Khảo sát toàn bộ các điểm giao tiếp mạng trong đường ống thông điệp từ Producer, Broker tới Consumer.
2. Phân tích kịch bản Producer retry khi bị network timeout: chứng minh thông điệp có thể bị gửi trùng lặp tới Broker.
3. Phân tích kịch bản Consumer crash ngay sau khi xử lý nghiệp vụ nhưng trước khi gửi ACK tới Broker: chứng minh thông điệp sẽ bị gửi lại lần thứ hai.
4. Thiết lập bảng lưu vết khóa trùng lặp (`idempotency_keys`) với khóa chính duy nhất trên cơ sở dữ liệu của Consumer.
5. Đóng gói logic xử lý của Consumer bên trong một database transaction duy nhất bao gồm: chèn khóa idempotency và cập nhật nghiệp vụ.
6. Chạy kịch bản kiểm thử truyền tin nhắn trùng lặp (duplicate injection) để chứng minh số dư không bị thay đổi hai lần.

## 7. Concrete Examples
### Ví dụ cơ chế Consumer Deduplication bảo đảm tính idempotent trong PostgreSQL:
```sql
-- Hàm xử lý giao dịch tài chính an toàn trước thông điệp trùng lặp
CREATE OR REPLACE FUNCTION process_payment_idempotent(
    p_message_id UUID,
    p_account_id UUID,
    p_amount NUMERIC
) RETURNS BOOLEAN AS $$
DECLARE
    v_already_processed BOOLEAN;
BEGIN
    -- 1. Thử ghi nhận message_id vào bảng deduplication
    INSERT INTO processed_messages (message_id, processed_at)
    VALUES (p_message_id, NOW())
    ON CONFLICT (message_id) DO NOTHING;

    -- 2. Kiểm tra xem message đã được xử lý từ trước chưa
    IF NOT FOUND THEN
        -- Message đã tồn tại, bỏ qua không xử lý lại nghiệp vụ
        RAISE NOTICE 'Message % already processed. Skipping duplicate execution.', p_message_id;
        RETURN FALSE;
    END IF;

    -- 3. Thực thi nghiệp vụ thay đổi số dư một cách an toàn
    UPDATE accounts 
    SET balance = balance + p_amount, updated_at = NOW()
    WHERE account_id = p_account_id;

    RETURN TRUE;
END;
$$ LANGUAGE plpgsql;
```

## 8. Anti-Patterns & Common Traps
- **Believing Broker Exactly-Once Magic:** Tin tưởng hoàn toàn vào cờ `enable.idempotence=true` của Kafka mà không triển khai deduplication tại database của Consumer cuối.
- **In-Memory Deduplication Cache:** Lưu trữ các message ID đã xử lý trong RAM của consumer, dẫn tới khi tiến trình bị khởi động lại sẽ xử lý lại toàn bộ thông điệp trùng lặp.
- **Separate Deduplication Step:** Kiểm tra trùng lặp và ghi dữ liệu nghiệp vụ trong hai transaction rời rạc tạo ra race condition nghiêm trọng.

## 9. Quality Gates & Acceptance Criteria
- **QG-06**: Hệ thống từ chối các đề xuất kiến trúc tuyên bố 'Exactly-Once' mà không có bảng lưu vết idempotency key.
- **QG-09**: Khả năng chống trùng lặp được chứng minh bằng test tự động bơm 1,000 thông điệp trùng lặp liên tiếp.
- **QG-10**: Không có bất kỳ sai lệch số dư nào xảy ra sau các đợt kiểm thử crash fault injection.

## 10. Security & Safety Boundaries
- Khóa idempotency phải được tạo ra từ nguồn dữ liệu đáng tin cậy (client signature hoặc UUID cryptographically secure).
- Ngăn chặn việc tấn công làm nghẽn bảng deduplication bằng cách cấu hình TTL tự động dọn dẹp các khóa quá cũ.

## 11. Platform Adapters
- **Brokers**: Apache Kafka, AWS SQS FIFO, RabbitMQ.
- **Databases**: PostgreSQL Unique Constraints, Redis SETNX with TTL.

## 12. Deliverables & Output Artifacts
- Báo cáo kiểm toán độ tin cậy của đường ống thông điệp phân tán.
- Mã nguồn Idempotent Consumer và Transactional Outbox.
- Bộ kiểm thử tự động bơm thông điệp trùng lặp (Duplicate Injection Test Suite).

## 13. Related & Complementary Skills
dex-idempotent-operations, dex-distributed-consistency, dex-event-driven-architecture

## 14. Realistic Usage Example
```powershell
# Chạy bộ kiểm thử khả năng chống trùng lặp khi bơm tin nhắn lặp lại
pytest tests/distributed/test_idempotent_deduplication.py -v
```
