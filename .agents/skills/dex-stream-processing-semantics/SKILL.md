---
name: dex-stream-processing-semantics
description: Design deterministic stream processing pipelines with Kafka/Pulsar partition ordering, consumer offset commits, idempotency keys, and at-least-once to exactly-once delivery semantics. Use when building event-driven microservices, transaction ledgers, or telemetry ingest engines.
---

# dex-stream-processing-semantics

## 1. Purpose & Scope
Thiết kế kiến trúc đường ống xử lý luồng sự kiện (Stream Processing Pipelines) có tính xác định cao; bảo toàn thứ tự phân vùng (Partition Ordering), quản lý commit độ lệch người tiêu thụ (Consumer Offset Commits), tích hợp khóa bất biến (Idempotency Keys) và chuyển đổi ngữ nghĩa từ At-least-once sang Exactly-once Processing; phục vụ các hệ thống sổ cái tài chính và vi dịch vụ hướng sự kiện.

## 2. When to Use
- Khi xây dựng đường ống xử lý luồng dữ liệu sự kiện quy mô lớn với Apache Kafka, Redpanda hoặc Apache Pulsar.
- Khi người tiêu thụ (Consumer) bị lỗi hoặc khởi động lại làm dữ liệu bị xử lý trùng lặp (Duplicate Processing).
- Khi thứ tự xử lý sự kiện của một thực thể (ví dụ: Tài khoản khách hàng) bắt buộc phải tuân thủ tuyệt đối theo thời gian thực.

## 3. When NOT to Use
- Khi chỉ cần các hàng đợi công việc đơn giản như RabbitMQ hoặc Redis BullMQ không cần lưu trữ lịch sử luồng.
- Khi xử lý các tệp dữ liệu dạng lô (Batch Processing) chạy định kỳ vào ban đêm.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Cụm Apache Kafka / Pulsar, thư viện client (KafkaJS, confluent-kafka), cơ sở dữ liệu lưu trữ trạng thái bất biến.
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; tuân thủ nghiêm ngặt các ranh giới bảo mật và an toàn dữ liệu.

## 5. Core Concepts & Taxonomy
- **Partition Key Routing:** Gán khóa phân vùng (ví dụ `accountId`) để đảm bảo toàn bộ sự kiện của một tài khoản luôn rơi vào đúng một phân vùng duy nhất.
- **Manual Offset Management:** Chỉ commit offset sau khi bản ghi đã được ghi thành công vào cơ sở dữ liệu đích, không bật `enable.auto.commit`.
- **Transactional Producer:** Sử dụng giao dịch Producer hai pha (2PC) để đảm bảo việc đọc bản ghi và xuất bản ghi mới diễn ra nguyên tử.

## 6. Step-by-Step Execution Workflow
1. Cấu hình Producer với cờ `enable.idempotence=true` và `acks=all`.
2. Chọn khóa phân vùng có ý nghĩa nghiệp vụ để đảm bảo thứ tự tuyến tính của sự kiện.
3. Vô hiệu hóa `auto-commit` trên Consumer, chuyển sang commit offset thủ công sau khi xử lý xong lô dữ liệu.
4. Kiểm tra tính trùng lặp bằng bảng tra cứu khóa bất biến `processed_event_ids` trước khi thực thi nghiệp vụ.
5. Kiểm thử khả năng phục hồi khi dừng đột ngột (Kill -9) Consumer giữa chừng trong lúc đang nhận dữ liệu.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```typescript
import { Kafka } from 'kafkajs';

const kafka = new Kafka({ clientId: 'dex-ledger', brokers: ['kafka:9092'] });
const consumer = kafka.consumer({ groupId: 'ledger-group' });

export async function runIdempotentConsumer(dbPool: any) {
  await consumer.connect();
  await consumer.subscribe({ topic: 'account-events', fromBeginning: false });

  await consumer.run({
    autoCommit: false, // Explicit manual commit
    eachMessage: async ({ topic, partition, message }) => {
      const event = JSON.parse(message.value!.toString());
      const eventId = message.key!.toString();

      await dbPool.transaction(async (trx: any) => {
        // 1. Check idempotency
        const exists = await trx('processed_events').where({ id: eventId }).first();
        if (exists) return; // Skip duplicate safely

        // 2. Process business logic
        await trx('ledger').insert({ accountId: event.accountId, amount: event.amount });
        await trx('processed_events').insert({ id: eventId, processedAt: new Date() });
      });

      // 3. Commit offset only after successful DB transaction
      await consumer.commitOffsets([{ topic, partition, offset: (BigInt(message.offset) + 1n).toString() }]);
    }
  });
}
```

## 8. Anti-Patterns & Common Traps
- Bật `enable.auto.commit: true` dẫn đến việc offset bị đánh dấu là đã xử lý mặc dù logic nghiệp vụ bên trong bị crash.
- Không gán partition key khiến các sự kiện của cùng một khách hàng bị phân tán ra nhiều partition khác nhau và xử lý sai thứ tự.
- Xử lý các bản ghi song song bằng `Promise.all` không có giới hạn làm phá vỡ thứ tự tuần tự trong cùng một phân vùng.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Không có sự kiện nào bị xử lý lặp lại hai lần làm sai lệch số dư tài khoản (100% Idempotent).
- QG-02: Thứ tự xử lý sự kiện trong cùng một Partition Key được bảo toàn tuyệt đối 100%.
- QG-03: Offset commit thành công khớp chính xác với bản ghi giao dịch đã lưu trong cơ sở dữ liệu.

## 10. Security & Safety Boundaries
- Mã hóa toàn bộ dữ liệu luồng sự kiện qua giao thức SASL/SCRAM và TLS; quản lý phân quyền theo dõi topic bằng ACLs.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Module người tiêu thụ luồng bất biến `IdempotentStreamConsumer.ts`.
1. Bảng kiểm tra tính xác định thứ tự sự kiện `ordering-validation-suite.ts`.

## 13. Related & Complementary Skills
- [`dex-event-driven-architecture`](.agents/skills/dex-event-driven-architecture/SKILL.md)
- [`dex-idempotent-operations`](.agents/skills/dex-idempotent-operations/SKILL.md)
- [`dex-event-schema-registry`](.agents/skills/dex-event-schema-registry/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Hệ thống ví điện tử bị lỗi khi xử lý sự kiện nạp tiền: một lệnh nạp 500,000 VND bị xử lý hai lần khi Consumer bị khởi động lại do lỗi mạng. Kỹ sư kích hoạt `dex-stream-processing-semantics`, chuyển sang commit offset thủ công kèm bảng khóa bất biến `processed_events`, triệt tiêu hoàn toàn lỗi nạp trùng tiền.
