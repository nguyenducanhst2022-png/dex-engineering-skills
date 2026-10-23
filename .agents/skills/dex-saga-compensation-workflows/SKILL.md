---
name: dex-saga-compensation-workflows
description: Architect and implement distributed Saga orchestration and choreography patterns with deterministic compensation workflows. Use when managing long-running distributed business transactions across multiple autonomous services or databases.
---

# dex-saga-compensation-workflows

## 1. Purpose & Scope
Thiết kế và triển khai mẫu kiến trúc Saga (Orchestrated và Choreographed) để duy trì tính nhất quán dữ liệu trong các giao dịch phân tán kéo dài; cài đặt cơ chế giao dịch bù trừ (compensating transactions) có tính chất bình thản (idempotent) để tự động hoàn tác khi xảy ra lỗi cục bộ.

## 2. When to Use
- Khi thực hiện giao dịch nghiệp vụ trải dài qua nhiều microservices hoặc cơ sở dữ liệu độc lập.
- Khi không thể áp dụng giao thức 2-Phase Commit (2PC) do yêu cầu về hiệu năng, độ trễ và khả năng mở rộng.
- Khi xử lý các luồng nghiệp vụ phức tạp như đặt vé máy bay/khách sạn, thanh toán thương mại điện tử đa bước.

## 3. When NOT to Use
- Khi tất cả các bảng dữ liệu nằm trong cùng một cơ sở dữ liệu quan hệ hỗ trợ giao dịch ACID cục bộ.
- Khi không thể thiết kế được hành động bù trừ tương ứng (ví dụ: gửi email hoặc bắn thông báo SMS cho khách hàng).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Sơ đồ trạng thái giao dịch (State Machine), danh sách các bước giao dịch thuận và giao dịch bù, cơ chế lưu trữ outbox/inbox.
- **Quyền hạn truy cập:** Quyền định nghĩa schema hàng đợi tin nhắn và logic điều phối giao dịch.

## 5. Core Concepts & Taxonomy
- **Compensating Transaction:** Giao dịch đảo ngược lại tác động của giao dịch thuận (ví dụ: `ReleaseInventory` bù trừ cho `ReserveInventory`).
- **Saga Orchestrator:** Một coordinator tập trung quản lý trạng thái, gửi lệnh thực thi và kích hoạt bù trừ khi có bước thất bại.
- **Idempotent Reversal:** Giao dịch bù trừ phải an toàn khi được gọi nhiều lần mà không làm sai lệch số dư hoặc trạng thái.

## 6. Step-by-Step Execution Workflow
1. Phân rã giao dịch tổng thể thành chuỗi các bước cục bộ $T_1, T_2, ..., T_n$ kèm các bước bù trừ $C_1, C_2, ..., C_{n-1}$.
2. Thiết kế bảng ghi nhận trạng thái Saga (`saga_instance`) lưu vết trạng thái hiện tại, payload và lịch sử các bước đã hoàn thành.
3. Triển khai Transactional Outbox pattern để bảo đảm gửi lệnh đi một cách nguyên tử cùng với việc cập nhật trạng thái cục bộ.
4. Định nghĩa quy trình xử lý lỗi: nếu bước $T_k$ thất bại, Orchestrator tự động gọi tuần tự ngược lại $C_{k-1}, C_{k-2}, ..., C_1$.
5. Cấu hình dead-letter queue và cảnh báo cho các trường hợp bước bù trừ thất bại liên tiếp sau khi đã retry tối đa.

## 7. Concrete Examples
### Ví dụ triển khai Saga Orchestrator bằng TypeScript:
```typescript
interface SagaStep<TContext> {
  name: string;
  execute: (ctx: TContext) => Promise<void>;
  compensate: (ctx: TContext) => Promise<void>;
}

export class OrderSagaOrchestrator {
  private steps: SagaStep<OrderContext>[] = [];

  addStep(step: SagaStep<OrderContext>): this {
    this.steps.push(step);
    return this;
  }

  async run(ctx: OrderContext): Promise<boolean> {
    const executedSteps: SagaStep<OrderContext>[] = [];
    for (const step of this.steps) {
      try {
        console.log(`Executing step: ${step.name}`);
        await step.execute(ctx);
        executedSteps.push(step);
      } catch (err) {
        console.error(`Step ${step.name} failed. Initiating compensation rollback...`, err);
        await this.rollback(executedSteps, ctx);
        return false;
      }
    }
    return true;
  }

  private async rollback(executedSteps: SagaStep<OrderContext>[], ctx: OrderContext): Promise<void> {
    for (const step of executedSteps.reverse()) {
      try {
        console.log(`Compensating step: ${step.name}`);
        await step.compensate(ctx);
      } catch (compErr) {
        // Ghi log nghiêm trọng để kích hoạt can thiệp thủ công
        console.error(`FATAL: Compensation failed for ${step.name}`, compErr);
      }
    }
  }
}
```

## 8. Anti-Patterns & Common Traps
- **Missing Compensation:** Triển khai các bước giao dịch thuận nhưng bỏ sót bước bù trừ tương ứng.
- **Non-Idempotent Compensations:** Hành động bù trừ gọi hai lần làm hoàn tiền gấp đôi cho khách hàng.
- **Synchronous Saga Cascading:** Nối tiếp các lệnh saga qua HTTP đồng bộ gây nghẽn kết nối và tăng nguy cơ timeout.

## 9. Quality Gates & Acceptance Criteria
- **QG-04**: 100% các bước giao dịch và bước bù trừ có unit test bao phủ kịch bản thành công và lỗi.
- **QG-09**: Tất cả các hàm bù trừ đã được chứng minh tính idempotent qua property-based test.
- **QG-10**: Cơ chế lưu trạng thái saga có khả năng phục hồi sau khi process bị crash đột ngột.

## 10. Security & Safety Boundaries
- Mã hóa dữ liệu nhạy cảm lưu trong payload của bảng theo dõi Saga.
- Kiểm tra chữ ký hoặc HMAC trên các thông điệp sự kiện giao dịch bù trừ để ngăn chặn việc kích hoạt hoàn tác giả mạo.

## 11. Platform Adapters
- **Temporal / Cadence**: Orchestration engine phân tán cấp doanh nghiệp.
- **Kafka / RabbitMQ**: Hệ thống truyền tải sự kiện cho Choreographed Sagas.

## 12. Deliverables & Output Artifacts
- Mã nguồn Saga Orchestrator / State Machine.
- Bảng schema lưu vết trạng thái Saga.
- Bộ kịch bản kiểm thử giả lập lỗi từng bước (fault injection).

## 13. Related & Complementary Skills
dex-event-driven-architecture, dex-idempotent-operations, dex-distributed-consistency

## 14. Realistic Usage Example
```powershell
# Chạy bộ kiểm thử kịch bản bù trừ giao dịch phân tán
pytest tests/distributed/test_saga_compensation.py -v
```
