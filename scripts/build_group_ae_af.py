# -*- coding: utf-8 -*-
"""
DEX ENGINEERING SKILLS FRAMEWORK v8.0 — GENERATOR
Builds Group AE (Skills 301–310: Enterprise Software Architecture)
and Group AF (Skills 311–320: Distributed Systems Deep Engineering).
All skills strictly implement the 14 mandatory sections standard.
"""

import os
import sys

if sys.stdout.encoding != "utf-8" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SKILLS_DIR = os.path.join(ROOT, ".agents", "skills")

SKILLS_AE_AF = [
    # =========================================================================
    # GROUP AE: Enterprise Software Architecture (Skills 301–310)
    # =========================================================================
    {
        "id": "dex-architecture-decision-records",
        "name": "dex-architecture-decision-records",
        "desc": "Establish and govern Architecture Decision Records (ADR) capturing technical context, evaluated alternatives, tradeoffs, and consequences. Use when proposing major architectural changes, selecting core frameworks, or establishing lasting technical consensus.",
        "purpose": "Thiết lập quy trình ghi nhận và quản trị các Quyết định Kiến trúc (Architecture Decision Records - ADR); lưu vết bối cảnh kỹ thuật, các giải pháp thay thế được đánh giá, đánh đổi chi phí/hiệu năng, và hệ quả dài hạn nhằm bảo đảm tính minh bạch trong quá trình tiến hóa hệ thống.",
        "when_use": "- Khi đề xuất thay đổi kiến trúc trọng yếu (chuyển đổi database, giao thức giao tiếp, mô hình phân tách service).\n- Khi lựa chọn ngôn ngữ, framework hoặc công cụ nền tảng cho tổ chức.\n- Khi cần bảo lưu lý do kỹ thuật đằng sau các quyết định phức tạp để tránh tranh cãi lặp lại.",
        "when_not_use": "- Khi thực hiện các sửa đổi triển khai chi tiết hoặc bugfix nhỏ không ảnh hưởng cấu trúc hệ thống.\n- Khi viết tài liệu hướng dẫn sử dụng sản phẩm dành cho người dùng cuối.",
        "prereqs": "- **Ngữ cảnh đầu vào:** Đề xuất kỹ thuật, phân tích yêu cầu phi chức năng (NFR), danh sách các phương án kỹ thuật khả dĩ.\n- **Quyền hạn truy cập:** Quyền ghi tài liệu kiến trúc trong thư mục `docs/adr/` hoặc repository tài liệu tập trung.",
        "concepts": "- **MADR / Nygard ADR Template:** Cấu trúc chuẩn hóa gồm Status, Context, Decision Drivers, Considered Options, Decision Outcome, Pros/Cons.\n- **Immutability of Historical Records:** ADR đã chốt ở trạng thái `Accepted` không được sửa đổi nội dung; khi thay đổi quyết định, tạo ADR mới với trạng thái `Supersedes [ADR-XXXX]`.\n- **Consequences & Tradeoffs:** Phân tích rõ cả mặt tích cực lẫn mặt tiêu cực, nợ kỹ thuật phát sinh sau quyết định.",
        "workflow": "1. Khởi tạo tệp ADR mới trong `docs/adr/` theo định dạng `NNNN-short-title.md` với trạng thái `Proposed`.\n2. Đặc tả bối cảnh kỹ thuật, động lực thúc đẩy quyết định và các ràng buộc hệ thống.\n3. Liệt kê tối thiểu 2-3 phương án thay thế kèm theo bảng so sánh ưu nhược điểm định lượng.\n4. Trình bày quyết định được chọn cùng lý do xác đáng và các hệ quả liên quan.\n5. Tổ chức buổi Architecture Review họp bàn với các Tech Leads để đạt đồng thuận.\n6. Cập nhật trạng thái sang `Accepted` hoặc `Rejected`, lưu vết commit vào Git.",
        "examples": """### Ví dụ tệp Architecture Decision Record chuẩn MADR:
```markdown
# ADR-0012: Chuyển đổi giao tiếp liên Service sang gRPC với Protobuf v3

* Status: Accepted
* Date: 2026-10-22
* Deciders: Staff Architect, Backend Lead, DevOps Lead

## Bối cảnh và Động lực Quyết định
Hệ thống xử lý giao dịch thanh toán hiện tại sử dụng HTTP/JSON REST giữa 14 microservices.
Độ trễ serialize/deserialize JSON chiếm 35% thời gian xử lý một transaction; thông lượng đỉnh chạm ngưỡng giới hạn 4,500 req/s.

## Các phương án đã xem xét
1. Giữ nguyên HTTP/1.1 JSON, tối ưu hóa parser với thư viện `sonic` / `simdjson`.
2. HTTP/2 gRPC với Protocol Buffers v3 và strictly typed contracts.
3. Asynchronous Messaging hoàn toàn qua Apache Kafka (Event-driven).

## Kết quả Quyết định
Chọn Phương án 2 (gRPC / Protobuf v3) cho các luồng request-response đồng bộ yêu cầu độ trễ < 15ms.

### Hệ quả tích cực
* Kích thước payload giảm 68% so với JSON.
* CPU overhead cho quá trình serialize/deserialize giảm 4.2 lần.
* Sinh mã tự động (code generation) cho Go, TypeScript và Python từ schema duy nhất.

### Hệ quả tiêu cực & Đánh đổi
* Cần triển khai Envoy proxy để biên dịch gRPC-Web cho các client frontend.
* Độ phức tạp trong việc debug mạng bằng các công cụ thông thường (curl, Postman).
```""",
        "antipatterns": "- **Silent Decisions:** Tự ý thay đổi kiến trúc nền tảng trong pull request mà không tạo ADR thảo luận.\n- **Retroactive Justification:** Tạo ADR chỉ để hợp thức hóa một quyết định đã làm mà không phân tích các phương án khác.\n- **Zombie ADRs:** Để ADR ở trạng thái `Proposed` kéo dài nhiều tháng mà không chốt hoặc loại bỏ.",
        "gates": "- **QG-01**: Tệp ADR phải tuân thủ chuẩn cấu trúc (Status, Context, Options, Outcome).\n- **QG-08**: Liên kết tới các ADR liên quan hoặc bị thay thế (`Supersedes`) phải hợp lệ.\n- **QG-14**: Đã được ký duyệt từ tối thiểu 2 reviewers có vai trò Architect/Staff Engineer.",
        "security": "- Không ghi lộ các thông tin mật (API keys, connection strings, credentials) trong nội dung ADR.\n- Rà soát các quyết định kiến trúc để bảo đảm tuân thủ nguyên tắc Least Privilege và Zero Trust.",
        "adapters": "- **ADR CLI Tools**: Tích hợp với `adr-tools` hoặc `log4brains` để tự động hóa sinh số thứ tự và cập nhật chỉ mục.\n- **Linter Integration**: Cấu hình markdownlint để kiểm tra cấu trúc định dạng ADR trong CI.",
        "deliverables": "- Tệp tài liệu `docs/adr/NNNN-<title>.md` hợp lệ.\n- Cập nhật chỉ mục `docs/adr/README.md`.\n- Bằng chứng phê duyệt trên Git pull request.",
        "related": "dex-software-architecture, dex-contract-first-development, dex-modular-monolith-boundaries",
        "usage": """```powershell
# 1. Khởi tạo ADR mới
python scripts/adr_manager.py new \"Use-gRPC-For-Internal-Communication\"

# 2. Kiểm tra tính toàn vẹn và liên kết của danh mục ADR
python scripts/adr_manager.py validate
```"""
    },
    {
        "id": "dex-modular-monolith-boundaries",
        "name": "dex-modular-monolith-boundaries",
        "desc": "Enforce strict domain boundaries, module isolation, and dependency rules within a modular monolith architecture. Use when restructuring legacy monoliths, preventing package entanglement, or maintaining high maintainability without microservice overhead.",
        "purpose": "Thiết kế và thực thi ranh giới module nghiêm ngặt trong kiến trúc Modular Monolith; ngăn chặn sự phụ thuộc chéo bất hợp lệ giữa các domain, phân tách rõ ràng Public API và Internal Implementation của từng module mà không phải chịu chi phí vận hành phân tán của microservices.",
        "when_use": "- Khi tái cấu trúc ứng dụng nguyên khối lớn (monolith) bị rối rắm mã nguồn (spaghetti code).\n- Khi muốn có tính độc lập cao giữa các domain nghiệp vụ nhưng vẫn triển khai trên cùng một artifact runtime duy nhất.\n- Khi chuẩn bị lộ trình tách service trong tương lai một cách an toàn và có kiểm soát.",
        "when_not_use": "- Khi ứng dụng quy mô siêu nhỏ (micro-tool hoặc prototype) chỉ có 1-2 nghiệp vụ cơ bản.\n- Khi hệ thống đã được phân tách thành các microservices hoàn toàn độc lập về hạ tầng.",
        "prereqs": "- **Ngữ cảnh đầu vào:** Bản đồ domain nghiệp vụ (Bounded Contexts), cấu trúc thư mục module, công cụ kiểm tra ranh giới (ArchUnit, dependency-cruiser).\n- **Quyền hạn truy cập:** Quyền sửa đổi cấu hình kiến trúc và build toolchain của dự án.",
        "concepts": "- **Module Encapsulation:** Mỗi module chỉ công khai `public-api` (interfaces, DTOs, events); toàn bộ implementation, entities, repositories nằm trong `internal`.\n- **Acyclic Dependency Rule:** Đồ thị phụ thuộc giữa các module phải là Directed Acyclic Graph (DAG), cấm tuyệt đối circular dependency.\n- **In-Memory Event Bus:** Giao tiếp bất đồng bộ giữa các module thông qua in-memory domain events thay vì gọi trực tiếp database của module khác.",
        "workflow": "1. Định nghĩa ranh giới các bounded context theo nguyên lý Domain-Driven Design (ví dụ: `billing`, `inventory`, `identity`).\n2. Cấu trúc mỗi module với hai thư mục con riêng biệt: `api/` và `internal/`.\n3. Thiết lập bộ quy tắc kiểm tra phụ thuộc tự động trong CI (sử dụng ArchUnit cho Java/Kotlin, dependency-cruiser cho TypeScript, hoặc import-linter cho Python).\n4. Thay thế việc truy vấn trực tiếp bảng dữ liệu của module khác bằng cách gọi API module hoặc đăng ký lắng nghe Domain Event.\n5. Chạy kiểm thử kiến trúc để xác nhận 0 vi phạm ranh giới module trước khi merge.",
        "examples": """### Ví dụ cấu hình quy tắc phụ thuộc module trong dependency-cruiser (`.dependency-cruiser.js`):
```javascript
module.exports = {
  forbidden: [
    {
      name: 'no-cross-module-internal-access',
      comment: 'Modules must only depend on public api of other modules, never internal code',
      severity: 'error',
      from: { path: '^src/modules/([^/]+)/internal/' },
      to: {
        path: '^src/modules/([^/]+)/internal/',
        pathNot: '^src/modules/$1/' // Allow internal access within the SAME module
      }
    },
    {
      name: 'no-circular-module-dependencies',
      comment: 'Circular dependencies between modules are strictly forbidden',
      severity: 'error',
      from: { path: '^src/modules/' },
      to: { circular: true }
    }
  ]
};
```""",
        "antipatterns": "- **Direct Foreign DB Querying:** Module Order truy vấn trực tiếp bảng của Module Customer bằng SQL JOIN xuyên schema.\n- **God Shared Module:** Nhét toàn bộ logic nghiệp vụ dùng chung vào thư mục `shared/` hoặc `common/` làm mất ranh giới domain.\n- **Leaky Internals:** Export trực tiếp Entity ORM (Hibernate, Prisma, TypeORM) qua public interface.",
        "gates": "- **QG-02**: Kiến trúc module tuân thủ 100% cấu trúc `api/` và `internal/`.\n- **QG-05**: Bộ linter kiến trúc chạy đạt exit code 0, không có circular dependency.\n- **QG-09**: Tất cả các giao tiếp liên module đều đi qua interface hoặc domain event.",
        "security": "- Phân quyền truy cập tài nguyên module dựa trên context security principal được truyền qua API boundary.\n- Bảo đảm module dữ liệu nhạy cảm (thanh toán, PII) không bị truy cập trái phép từ các module nghiệp vụ thông thường.",
        "adapters": "- **TypeScript/Node**: dependency-cruiser, nx boundaries.\n- **Java/Kotlin**: ArchUnit JUnit tests.\n- **Python**: import-linter, tach.",
        "deliverables": "- Tệp cấu hình quy tắc ranh giới kiến trúc.\n- Báo cáo kết quả kiểm tra dependency graph không chu trình.\n- Mã nguồn tuân thủ nghiêm ngặt chuẩn `api/` và `internal/`.",
        "related": "dex-software-architecture, dex-code-organization, dex-architecture-decision-records",
        "usage": """```powershell
# Kiểm tra vi phạm ranh giới giữa các module trong dự án
npx depcruise --config .dependency-cruiser.js src/modules

# Chạy kiến trúc test suite
pytest tests/architecture/test_module_boundaries.py -v
```"""
    },
    {
        "id": "dex-saga-compensation-workflows",
        "name": "dex-saga-compensation-workflows",
        "desc": "Architect and implement distributed Saga orchestration and choreography patterns with deterministic compensation workflows. Use when managing long-running distributed business transactions across multiple autonomous services or databases.",
        "purpose": "Thiết kế và triển khai mẫu kiến trúc Saga (Orchestrated và Choreographed) để duy trì tính nhất quán dữ liệu trong các giao dịch phân tán kéo dài; cài đặt cơ chế giao dịch bù trừ (compensating transactions) có tính chất bình thản (idempotent) để tự động hoàn tác khi xảy ra lỗi cục bộ.",
        "when_use": "- Khi thực hiện giao dịch nghiệp vụ trải dài qua nhiều microservices hoặc cơ sở dữ liệu độc lập.\n- Khi không thể áp dụng giao thức 2-Phase Commit (2PC) do yêu cầu về hiệu năng, độ trễ và khả năng mở rộng.\n- Khi xử lý các luồng nghiệp vụ phức tạp như đặt vé máy bay/khách sạn, thanh toán thương mại điện tử đa bước.",
        "when_not_use": "- Khi tất cả các bảng dữ liệu nằm trong cùng một cơ sở dữ liệu quan hệ hỗ trợ giao dịch ACID cục bộ.\n- Khi không thể thiết kế được hành động bù trừ tương ứng (ví dụ: gửi email hoặc bắn thông báo SMS cho khách hàng).",
        "prereqs": "- **Ngữ cảnh đầu vào:** Sơ đồ trạng thái giao dịch (State Machine), danh sách các bước giao dịch thuận và giao dịch bù, cơ chế lưu trữ outbox/inbox.\n- **Quyền hạn truy cập:** Quyền định nghĩa schema hàng đợi tin nhắn và logic điều phối giao dịch.",
        "concepts": "- **Compensating Transaction:** Giao dịch đảo ngược lại tác động của giao dịch thuận (ví dụ: `ReleaseInventory` bù trừ cho `ReserveInventory`).\n- **Saga Orchestrator:** Một coordinator tập trung quản lý trạng thái, gửi lệnh thực thi và kích hoạt bù trừ khi có bước thất bại.\n- **Idempotent Reversal:** Giao dịch bù trừ phải an toàn khi được gọi nhiều lần mà không làm sai lệch số dư hoặc trạng thái.",
        "workflow": "1. Phân rã giao dịch tổng thể thành chuỗi các bước cục bộ $T_1, T_2, ..., T_n$ kèm các bước bù trừ $C_1, C_2, ..., C_{n-1}$.\n2. Thiết kế bảng ghi nhận trạng thái Saga (`saga_instance`) lưu vết trạng thái hiện tại, payload và lịch sử các bước đã hoàn thành.\n3. Triển khai Transactional Outbox pattern để bảo đảm gửi lệnh đi một cách nguyên tử cùng với việc cập nhật trạng thái cục bộ.\n4. Định nghĩa quy trình xử lý lỗi: nếu bước $T_k$ thất bại, Orchestrator tự động gọi tuần tự ngược lại $C_{k-1}, C_{k-2}, ..., C_1$.\n5. Cấu hình dead-letter queue và cảnh báo cho các trường hợp bước bù trừ thất bại liên tiếp sau khi đã retry tối đa.",
        "examples": """### Ví dụ triển khai Saga Orchestrator bằng TypeScript:
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
```""",
        "antipatterns": "- **Missing Compensation:** Triển khai các bước giao dịch thuận nhưng bỏ sót bước bù trừ tương ứng.\n- **Non-Idempotent Compensations:** Hành động bù trừ gọi hai lần làm hoàn tiền gấp đôi cho khách hàng.\n- **Synchronous Saga Cascading:** Nối tiếp các lệnh saga qua HTTP đồng bộ gây nghẽn kết nối và tăng nguy cơ timeout.",
        "gates": "- **QG-04**: 100% các bước giao dịch và bước bù trừ có unit test bao phủ kịch bản thành công và lỗi.\n- **QG-09**: Tất cả các hàm bù trừ đã được chứng minh tính idempotent qua property-based test.\n- **QG-10**: Cơ chế lưu trạng thái saga có khả năng phục hồi sau khi process bị crash đột ngột.",
        "security": "- Mã hóa dữ liệu nhạy cảm lưu trong payload của bảng theo dõi Saga.\n- Kiểm tra chữ ký hoặc HMAC trên các thông điệp sự kiện giao dịch bù trừ để ngăn chặn việc kích hoạt hoàn tác giả mạo.",
        "adapters": "- **Temporal / Cadence**: Orchestration engine phân tán cấp doanh nghiệp.\n- **Kafka / RabbitMQ**: Hệ thống truyền tải sự kiện cho Choreographed Sagas.",
        "deliverables": "- Mã nguồn Saga Orchestrator / State Machine.\n- Bảng schema lưu vết trạng thái Saga.\n- Bộ kịch bản kiểm thử giả lập lỗi từng bước (fault injection).",
        "related": "dex-event-driven-architecture, dex-idempotent-operations, dex-distributed-consistency",
        "usage": """```powershell
# Chạy bộ kiểm thử kịch bản bù trừ giao dịch phân tán
pytest tests/distributed/test_saga_compensation.py -v
```"""
    },
    {
        "id": "dex-cqrs-projection-management",
        "name": "dex-cqrs-projection-management",
        "desc": "Manage asynchronous read-model projections in CQRS architectures with replay safety, eventual consistency lag monitoring, and zero-downtime projection rebuilds. Use when scaling complex reporting queries or separating read/write models.",
        "purpose": "Quản lý vòng đời và tính toàn vẹn của các Read-Model Projections trong kiến trúc CQRS; thiết lập quy trình tính toán lại (replay/rebuild) hình chiếu dữ liệu mà không làm gián đoạn hệ thống, kiểm soát độ trễ nhất quán cuối cùng (eventual consistency lag).",
        "when_use": "- Khi mô hình ghi (Write Model/Command) có cấu trúc nghiệp vụ phức tạp không tối ưu cho các câu truy vấn báo cáo, tìm kiếm hoặc hiển thị dashboard.\n- Khi cần hỗ trợ nhiều dạng hiển thị khác nhau từ cùng một nguồn dữ liệu sự kiện (Event Store).\n- Khi cần xây dựng lại toàn bộ read model sau khi thay đổi schema hoặc bổ sung tính năng mới.",
        "when_not_use": "- Khi ứng dụng CRUD đơn giản, lưu lượng đọc và ghi cân bằng trên cùng một mô hình dữ liệu.\n- Khi hệ thống bắt buộc tính nhất quán tức thời (Strong Immediate Consistency) tại mọi điểm truy vấn.",
        "prereqs": "- **Ngữ cảnh đầu vào:** Nguồn sự kiện nghiệp vụ (Domain Events stream), cơ sở dữ liệu read-model (PostgreSQL, Elasticsearch, Redis), cơ chế theo dõi offset.\n- **Quyền hạn truy cập:** Quyền tạo/xóa bảng view và đăng ký consumer trên event stream.",
        "concepts": "- **Projection / Read Model:** Bảng biểu dữ liệu được tối ưu hóa riêng cho truy vấn đọc (denormalized data), được cập nhật bất đồng bộ từ các sự kiện.\n- **Projection Versioning & Blue-Green Rebuild:** Tạo bảng projection mới (`orders_view_v2`), nạp lại dữ liệu từ đầu, sau đó tráo đổi alias mà không gián đoạn dịch vụ.\n- **Catch-up Lag:** Khoảng cách thời gian hoặc số lượng sự kiện giữa vị trí mới nhất của Event Store và vị trí đã chiếu của Read Model.",
        "workflow": "1. Thiết kế bảng projection tối ưu hóa cho các truy vấn đọc cụ thể với đầy đủ index cần thiết.\n2. Đăng ký projection handler xử lý các sự kiện tương ứng kèm cơ chế cập nhật idempotent dựa trên `event_id` hoặc sequence number.\n3. Thiết lập bảng lưu vết vị trí xử lý (`projection_checkpoints`) lưu giữ offset sự kiện gần nhất đã áp dụng thành công.\n4. Xây dựng công cụ Rebuild Projections cho phép nạp lại sự kiện lịch sử vào bảng tạm mới theo cơ chế Blue-Green.\n5. Giám sát độ trễ chiếu dữ liệu (Projection Lag) qua Prometheus metrics và cảnh báo khi lag vượt ngưỡng an toàn.",
        "examples": """### Ví dụ triển khai Projection Handler có kiểm tra idempotency trong SQL:
```sql
-- Cập nhật read-model an toàn và idempotent từ Domain Event
INSERT INTO order_summary_projection (
    order_id, customer_id, total_amount, order_status, last_event_id, updated_at
) VALUES (
    $1, $2, $3, 'CREATED', $4, NOW()
)
ON CONFLICT (order_id) DO UPDATE SET
    order_status = CASE 
        WHEN EXCLUDED.last_event_id > order_summary_projection.last_event_id 
        THEN EXCLUDED.order_status 
        ELSE order_summary_projection.order_status 
    END,
    total_amount = EXCLUDED.total_amount,
    last_event_id = GREATEST(order_summary_projection.last_event_id, EXCLUDED.last_event_id),
    updated_at = NOW()
WHERE EXCLUDED.last_event_id >= order_summary_projection.last_event_id;
```""",
        "antipatterns": "- **Direct Read-Model Mutation:** Tự ý cập nhật bảng read-model từ các API bên ngoài thay vì lắng nghe sự kiện từ Command Model.\n- **Blocking Command on Projection:** Chờ đợi read-model được cập nhật xong mới trả về phản hồi cho API ghi (phá vỡ lợi ích bất đồng bộ của CQRS).\n- **Ignoring Out-of-Order Events:** Áp dụng sự kiện cũ đè lên dữ liệu mới hơn do thông điệp bị đến lệch thứ tự qua mạng.",
        "gates": "- **QG-04**: Có kiểm thử xác nhận khả năng chiếu lại (replay) 10,000 sự kiện tạo ra kết quả giống hệt dữ liệu ban đầu.\n- **QG-07**: Thời gian xử lý một sự kiện trong projection handler dưới 10ms.\n- **QG-10**: Có cơ chế tự động khôi phục từ checkpoint khi worker bị tắt đột ngột.",
        "security": "- Áp dụng phân quyền người dùng (Role-Based Access Control) ngay tại tầng đọc projection.\n- Loại bỏ các trường thông tin nhạy cảm (như mật khẩu băm, token) trước khi đưa vào bảng read-model công khai.",
        "adapters": "- **Event Store**: Kafka, Debezium, EventStoreDB.\n- **Read Storage**: PostgreSQL Read Replicas, Redis, Elasticsearch.",
        "deliverables": "- Mã nguồn các Projection Handlers.\n- Kịch bản Blue-Green Rebuild tự động.\n- Dashboard giám sát Projection Lag trên Grafana.",
        "related": "dex-event-driven-architecture, dex-database-query-plans, dex-data-contracts",
        "usage": """```powershell
# Chạy script rebuild projection sang bảng mới
python scripts/rebuild_projection.py --projection order_summary --version v2

# Kiểm tra độ trễ (lag) của các projections hiện hành
python scripts/check_projection_lag.py
```"""
    },
    {
        "id": "dex-multi-region-data-residency",
        "name": "dex-multi-region-data-residency",
        "desc": "Architect multi-region data partitioning and replication topologies complying with strict legal data residency and sovereignty requirements (GDPR, APRA, HIPAA). Use when deploying global applications handling region-locked user data.",
        "purpose": "Thiết kế kiến trúc phân vùng dữ liệu đa vùng (Multi-Region Data Partitioning) và cấu hình topo sao chép tuân thủ nghiêm ngặt các quy định pháp lý về chủ quyền dữ liệu (Data Residency & Data Sovereignty như GDPR, HIPAA, APRA); ngăn chặn việc dữ liệu nhạy cảm bị sao chép trái phép ra khỏi biên giới quốc gia.",
        "when_use": "- Khi triển khai hệ thống toàn cầu phục vụ người dùng ở nhiều khu vực pháp lý có quy định khắt khe về nơi lưu trữ dữ liệu (EU, Mỹ, Singapore, Việt Nam).\n- Khi cần cung cấp độ trễ đọc/ghi thấp cho người dùng ở nhiều lục địa khác nhau mà vẫn tôn trọng chủ quyền dữ liệu.\n- Khi chuẩn bị hồ sơ kiểm toán bảo mật và tuân thủ pháp lý quốc tế.",
        "when_not_use": "- Khi ứng dụng chỉ hoạt động và phục vụ người dùng tại một quốc gia duy nhất.\n- Khi dữ liệu xử lý là dữ liệu công khai, không chứa PII hoặc bí mật kinh doanh chịu ràng buộc địa lý.",
        "prereqs": "- **Ngữ cảnh đầu vào:** Yêu cầu pháp lý theo từng vùng lãnh thổ, sơ đồ phân loại dữ liệu (Data Classification), topo mạng và hạ tầng đa đám mây (Multi-Region Cloud).\n- **Quyền hạn truy cập:** Quyền cấu hình replication và phân quyền mạng trên cơ sở dữ liệu.",
        "concepts": "- **Geographic Partitioning (Geo-sharding):** Chia partition bảng dữ liệu dựa trên thuộc tính vị trí địa lý của người dùng (ví dụ: `region = 'eu-west-1'`).\n- **Data Sovereignty Constraints:** Dữ liệu cá nhân (PII) bắt buộc lưu trữ và xử lý tại máy chủ thuộc ranh giới địa lý quy định.\n- **Global Table Routing:** Hệ thống định tuyến ứng dụng tự động chuyển hướng kết nối database tới đúng cụm máy chủ khu vực dựa trên JWT token của tenant.",
        "workflow": "1. Phân loại toàn bộ bảng dữ liệu thành 3 nhóm: Global Shared Data (không PII), Region-Pinned PII Data, và Ephemeral Logs.\n2. Thiết lập cấu hình cơ sở dữ liệu hỗ trợ geo-partitioning (như CockroachDB, Spanner, hoặc PostgreSQL Sharding với Citus).\n3. Gắn partition key theo khu vực (`jurisdiction_code`) cho toàn bộ bảng chứa dữ liệu nhạy cảm.\n4. Cấu hình quy tắc sao chép (Replication Policy) ngăn chặn đồng bộ bảng Region-Pinned sang các vùng địa lý khác.\n5. Xây dựng integration test tự động xác nhận câu truy vấn không bao giờ ghi dữ liệu EU sang cụm database đặt tại US.",
        "examples": """### Ví dụ định nghĩa bảng Geo-Partitioned trong CockroachDB:
```sql
-- Định nghĩa bảng người dùng có ràng buộc vị trí địa lý dữ liệu
CREATE TABLE customer_profiles (
    customer_id UUID DEFAULT gen_random_uuid(),
    residence_region VARCHAR(10) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    encrypted_national_id BYTEA,
    created_at TIMESTAMPTZ DEFAULT clock_timestamp(),
    PRIMARY KEY (residence_region, customer_id)
) PARTITION BY LIST (residence_region) (
    PARTITION eu_region VALUES IN ('EU', 'DE', 'FR', 'NL'),
    PARTITION us_region VALUES IN ('US', 'CA'),
    PARTITION apac_region VALUES IN ('VN', 'SG', 'JP')
);

-- Cấu hình lưu trữ vật lý cho từng partition theo vùng dữ liệu
ALTER PARTITION eu_region OF TABLE customer_profiles 
    CONFIGURE ZONE USING constraints = '[+region=europe-west1]';

ALTER PARTITION us_region OF TABLE customer_profiles 
    CONFIGURE ZONE USING constraints = '[+region=us-central1]';

ALTER PARTITION apac_region OF TABLE customer_profiles 
    CONFIGURE ZONE USING constraints = '[+region=asia-southeast1]';
```""",
        "antipatterns": "- **Unbounded Global Replication:** Đồng bộ toàn bộ database ra toàn cầu mà không lọc các bảng chứa dữ liệu cá nhân.\n- **Centralized Foreign Logging:** Bắn log chứa thông tin PII của người dùng châu Âu về cụm lưu trữ log tập trung đặt tại Mỹ.\n- **Client-Side Region Spoofing:** Cho phép client tự ý gửi header khu vực mà không xác thực lại từ chứng thực người dùng.",
        "gates": "- **QG-06**: Không có dữ liệu PII nào được lưu trữ bên ngoài vùng địa lý được chỉ định trong cấu hình.\n- **QG-11**: Các kết nối cross-region chỉ áp dụng cho dữ liệu đã được mã hóa và không chứa thông tin định danh cá nhân.\n- **QG-14**: Đáp ứng các yêu cầu kiểm toán của GDPR Article 44-50 về chuyển giao dữ liệu quốc tế.",
        "security": "- Bắt buộc mã hóa dữ liệu cả khi lưu trữ (at rest) và khi truyền tải (in transit) bằng giao thức TLS 1.3 với cipher suites mạnh.\n- Khóa mã hóa (KMS keys) cho từng vùng phải được quản lý tại hạ tầng của chính vùng đó (Regional KMS).",
        "adapters": "- **Database**: CockroachDB, Google Cloud Spanner, AWS Aurora Global Database with Write Forwarding.\n- **Cloud**: AWS, GCP, Azure Multi-Region VPC Peering.",
        "deliverables": "- Tệp DDL cấu hình phân vùng địa lý cơ sở dữ liệu.\n- Ma trận phân loại dữ liệu và vị trí lưu trữ (Data Residency Matrix).\n- Bộ kiểm thử tự động kiểm tra vi phạm lưu trữ dữ liệu ngoài vùng.",
        "related": "dex-compliance-control-mapping, dex-privacy-impact-assessment, dex-database-engineering",
        "usage": """```powershell
# Chạy bài kiểm thử xác minh ranh giới lưu trữ dữ liệu địa lý
pytest tests/compliance/test_data_residency_boundaries.py -v
```"""
    },
    {
        "id": "dex-tenant-provisioning-lifecycle",
        "name": "dex-tenant-provisioning-lifecycle",
        "desc": "Orchestrate end-to-end multi-tenant provisioning, migration, suspension, and offboarding lifecycles with strict resource isolation. Use when building B2B SaaS platforms with automated self-service onboarding or enterprise tenant tiering.",
        "purpose": "Điều phối toàn diện vòng đời của tenant trong kiến trúc đa người thuê (Multi-Tenant SaaS); tự động hóa các giai đoạn khởi tạo (provisioning), nâng cấp schema, tạm khóa (suspension), di chuyển dữ liệu (migration) và xóa sạch dữ liệu (offboarding/purging) bảo đảm cách ly triệt để tài nguyên.",
        "when_use": "- Khi xây dựng nền tảng B2B SaaS cho phép khách hàng doanh nghiệp tự đăng ký và khởi tạo workspace tự động.\n- Khi cần nâng cấp hoặc chuyển đổi mô hình tenant giữa Shared Database (Row-Level Security) và Dedicated Database (Database-per-tenant).\n- Khi thực hiện quy trình hủy hợp đồng và xóa toàn bộ dữ liệu khách hàng theo quyền được lãng quên (Right to be Forgotten).",
        "when_not_use": "- Khi ứng dụng chỉ phục vụ một tổ chức duy nhất (Single-tenant on-premise).\n- Khi quản trị người dùng thông thường trong một ứng dụng B2C không có khái niệm tổ chức/tenant.",
        "prereqs": "- **Ngữ cảnh đầu vào:** Mô hình cách ly tenant (Schema-per-tenant, DB-per-tenant, hoặc Table-RLS), kịch bản migration database, hệ thống thông báo trạng thái.\n- **Quyền hạn truy cập:** Quyền tạo database/schema mới và gán quyền truy cập người dùng trong cơ sở dữ liệu.",
        "concepts": "- **Tenant Lifecycle State Machine:** Các trạng thái hợp lệ gồm: `PROVISIONING` -> `ACTIVE` -> `SUSPENDED` -> `ARCHIVED` -> `PURGED`.\n- **Automated Provisioning Hook:** Chuỗi tác vụ tự động: tạo schema, nạp seed data mặc định, cấp quyền IAM, cấu hình DNS subdomain và tạo tài khoản quản trị.\n- **Cryptographic Shredding:** Hủy khóa mã hóa riêng của tenant khi xóa để bảo đảm dữ liệu trên bản backup cũ cũng không thể bị giải mã.",
        "workflow": "1. Nhận yêu cầu khởi tạo tenant mới từ hệ thống thanh toán hoặc onboarding flow kèm gói dịch vụ (tier).\n2. Kích hoạt workflow khởi tạo: tạo schema database riêng hoặc gán `tenant_id` với Row-Level Security tương ứng.\n3. Áp dụng toàn bộ database migrations mới nhất vào schema của tenant mới.\n4. Nạp dữ liệu cấu hình ban đầu (seed roles, permissions, default settings) và phát sinh credentials quản trị.\n5. Kiểm tra tính sẵn sàng bằng lệnh smoke test truy vấn schema tenant mới khởi tạo.\n6. Chuyển trạng thái tenant sang `ACTIVE` và gửi thông báo sẵn sàng sử dụng cho khách hàng.",
        "examples": """### Ví dụ workflow điều phối vòng đời tenant bằng TypeScript:
```typescript
export enum TenantStatus {
  PROVISIONING = 'PROVISIONING',
  ACTIVE = 'ACTIVE',
  SUSPENDED = 'SUSPENDED',
  PURGED = 'PURGED'
}

export class TenantLifecycleManager {
  async provisionTenant(tenantId: string, companyName: string): Promise<void> {
    console.log(`Starting automated provisioning for tenant: ${tenantId}`);
    try {
      // 1. Tạo database schema riêng biệt
      await db.raw(`CREATE SCHEMA IF NOT EXISTS tenant_${tenantId}`);
      
      // 2. Chạy migration schema
      await runMigrationsForSchema(`tenant_${tenantId}`);
      
      // 3. Khởi tạo tài khoản quản trị mặc định
      await seedTenantAdmin(`tenant_${tenantId}`);
      
      // 4. Cập nhật trạng thái
      await updateTenantRecord(tenantId, { status: TenantStatus.ACTIVE, provisionedAt: new Date() });
      console.log(`Tenant ${tenantId} successfully provisioned.`);
    } catch (error) {
      console.error(`Provisioning failed for ${tenantId}. Rolling back...`, error);
      await this.rollbackProvisioning(tenantId);
      throw error;
    }
  }

  async purgeTenant(tenantId: string): Promise<void> {
    // Thu hồi quyền truy cập ngay lập tức
    await updateTenantRecord(tenantId, { status: TenantStatus.PURGED });
    // Xóa sạch schema vật lý
    await db.raw(`DROP SCHEMA IF EXISTS tenant_${tenantId} CASCADE`);
  }
}
```""",
        "antipatterns": "- **Manual Tenant Setup:** Kỹ sư phải vào terminal chạy tay các lệnh SQL để tạo schema cho mỗi khách hàng mới.\n- **Incomplete Offboarding:** Khách hàng hủy hợp đồng nhưng dữ liệu trong cache, S3 bucket và bảng phụ trợ vẫn bị bỏ quên.\n- **Shared Encryption Key:** Dùng chung một encryption key cho tất cả tenants khiến không thể áp dụng cryptographic shredding khi hủy dịch vụ.",
        "gates": "- **QG-01**: Bắt buộc có cơ chế rollback tự động hoàn toàn nếu quá trình khởi tạo thất bại ở bất kỳ bước nào.\n- **QG-06**: Xác nhận tenant mới không thể truy cập bất kỳ dữ liệu nào thuộc về tenant khác.\n- **QG-14**: Quá trình xóa tenant loại bỏ 100% dữ liệu PII đáp ứng tiêu chuẩn tuân thủ GDPR.",
        "security": "- Cô lập kết nối database qua connection pool riêng biệt hoặc gán session variable `app.current_tenant_id` trước mỗi truy vấn.\n- Kiểm toán mọi hành động quản trị liên quan tới tenant trong audit trail không thể chỉnh sửa.",
        "adapters": "- **Database**: PostgreSQL Schemas, AWS Aurora Multi-Tenant, CockroachDB.\n- **Identity**: Auth0 Organizations, AWS Cognito User Pools, Keycloak Realms.",
        "deliverables": "- Mã nguồn Tenant Lifecycle Orchestration Engine.\n- Kịch bản migration tự động cho multi-tenant.\n- Bộ kiểm thử tự động kiểm tra rò rỉ dữ liệu chéo giữa các tenants.",
        "related": "dex-access-control-tenancy, dex-database-engineering, dex-compliance-control-mapping",
        "usage": """```powershell
# Chạy kiểm thử tự động quy trình khởi tạo và hủy tenant
pytest tests/tenancy/test_tenant_lifecycle.py -v
```"""
    },
    {
        "id": "dex-legacy-strangler-migration",
        "name": "dex-legacy-strangler-migration",
        "desc": "Execute legacy system modernization using the Strangler Fig pattern with routing facades, shadow traffic verification, and incremental cutover. Use when replacing monolithic systems with modern services while maintaining continuous production availability.",
        "purpose": "Thực hiện lộ trình hiện đại hóa ứng dụng cũ theo mẫu Strangler Fig Pattern; thiết lập API facade định tuyến thông minh, sao chép lưu lượng thực tế để kiểm tra chạy song song (shadow traffic verification), và chuyển đổi từng phần tính năng sang hệ thống mới với khả năng rollback tức thời.",
        "when_use": "- Khi cần thay thế một hệ thống monolithic legacy cồng kềnh nhưng không thể dừng hoạt động để viết lại từ đầu (Big Bang rewrite).\n- Khi muốn giảm thiểu rủi ro kinh doanh bằng cách bóc tách từng dịch vụ nhỏ và đưa vào sản xuất từng bước.\n- Khi cần đối chiếu độ chính xác của kết quả xử lý giữa hệ thống mới và hệ thống cũ trên dữ liệu thực.",
        "when_not_use": "- Khi ứng dụng cũ quá nhỏ và không còn người sử dụng, có thể viết lại và chuyển đổi trong vài ngày.\n- Khi hệ thống cũ không có bất kỳ API hoặc giao diện nào để gắn lớp định tuyến Facade.",
        "prereqs": "- **Ngữ cảnh đầu vào:** Bản đồ chức năng hệ thống cũ, reverse proxy hoặc API gateway có khả năng định tuyến theo trọng số (weighted routing), hệ thống so sánh dữ liệu kết quả.\n- **Quyền hạn truy cập:** Quyền cấu hình API Gateway / Load Balancer và phân tích log truy cập.",
        "concepts": "- **Strangler Facade:** Lớp trung gian đứng trước cả hệ thống cũ và mới, tiếp nhận toàn bộ request từ client và quyết định chuyển tiếp tới hệ thống phù hợp.\n- **Dark Launch / Shadow Traffic:** Nhân bản request thật từ client để gửi song song tới hệ thống mới mà không trả kết quả cho client, dùng để so sánh độ trễ và tính chính xác.\n- **Canary Cutover:** Chuyển dần lưu lượng thực từ 1%, 5%, 25%, 50% tới 100% sang hệ thống mới sau khi đã xác nhận tính ổn định.",
        "workflow": "1. Đặt API Gateway hoặc Reverse Proxy (Envoy, Kong, NGINX) làm Strangler Facade đứng trước hệ thống legacy.\n2. Lựa chọn một module nghiệp vụ cụ thể có ranh giới rõ ràng để xây dựng lại trên kiến trúc mới.\n3. Cấu hình Shadow Traffic tại Facade để sao chép 100% request của module đó sang service mới và ghi log so sánh kết quả (`diff`).\n4. Phân tích kết quả so sánh để khắc phục toàn bộ các điểm sai lệch logic trước khi phục vụ người dùng thật.\n5. Bắt đầu chuyển đổi lưu lượng thực tế theo cơ chế Canary Cutover từ 5% lên 100% kèm theo giám sát lỗi.\n6. Vô hiệu hóa và xóa bỏ mã nguồn legacy tương ứng sau khi hệ thống mới chạy ổn định sau thời gian bảo hành.",
        "examples": """### Ví dụ cấu hình NGINX làm Strangler Facade hỗ trợ phân chia lưu lượng theo endpoint:
```nginx
upstream legacy_backend {
    server legacy-app.internal:8080;
}

upstream modern_service {
    server payment-v2.internal:3000;
}

server {
    listen 80;
    server_name api.dex.dev;

    # 1. Endpoint cũ đã được chuyển đổi hoàn toàn sang hệ thống mới
    location /api/v1/payments {
        proxy_pass http://modern_service;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $remote_addr;
    }

    # 2. Toàn bộ các endpoint còn lại tiếp tục trỏ về hệ thống Legacy
    location / {
        proxy_pass http://legacy_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $remote_addr;
    }
}
```""",
        "antipatterns": "- **Big Bang Switchover:** Cố gắng chuyển đổi 100% hệ thống trong một đêm gây ra thảm họa mất dữ liệu và dừng dịch vụ.\n- **Dual Write without Reconciliation:** Ghi dữ liệu đồng thời vào hai database nhưng không có công cụ tự động đối soát sai lệch.\n- **Permanent Half-Strangled State:** Dừng dự án khi mới chuyển đổi được 30%, để lại hai hệ thống chạy song song vĩnh viễn gây tăng gấp đôi chi phí vận hành.",
        "gates": "- **QG-03**: Hệ thống mới vượt qua giai đoạn shadow traffic với tỷ lệ kết quả khớp tối thiểu 99.99%.\n- **QG-07**: Độ trễ p99 của service mới phải thấp hơn hoặc bằng hệ thống cũ trước khi cutover.\n- **QG-10**: Cơ chế rollback về hệ thống cũ được kiểm tra và kích hoạt thành công trong dưới 60 giây.",
        "security": "- Kiểm tra xác thực và phân quyền nhất quán giữa lớp Facade và cả hai hệ thống backend.\n- Ngăn chặn việc nhân bản request nhạy cảm trong shadow traffic gây trùng lặp giao dịch tài chính (ví dụ: cấm shadow các API trừ tiền trực tiếp).",
        "adapters": "- **API Gateways**: Envoy, Kong, NGINX, Cloudflare Workers.\n- **Traffic Mirroring**: AWS VPC Traffic Mirroring, Istio VirtualService mirroring.",
        "deliverables": "- Tệp cấu hình Strangler Facade Proxy.\n- Báo cáo kết quả so sánh dữ liệu Shadow Traffic.\n- Kế hoạch chuyển đổi từng giai đoạn và kịch bản rollback khẩn cấp.",
        "related": "dex-zero-downtime-rollouts, dex-feature-flags, dex-change-impact-analysis",
        "usage": """```powershell
# Chạy công cụ đối soát kết quả phản hồi giữa hệ thống cũ và mới
python scripts/diff_shadow_traffic.py --endpoint /api/v1/payments --samples 5000
```"""
    },
    {
        "id": "dex-public-api-deprecation",
        "name": "dex-public-api-deprecation",
        "desc": "Manage public API deprecation lifecycles according to RFC 8594 standards, consumer migration communication, sunset telemetry, and backward-compatible evolution. Use when retiring legacy API versions or breaking interface contracts.",
        "purpose": "Quản trị quy trình khai tử API công khai (Public API Deprecation Lifecycle) tuân thủ tiêu chuẩn RFC 8594 (Sunset & Deprecation HTTP headers); đo lường mức độ sử dụng của các đối tác tích hợp, cung cấp tài liệu di chuyển và bảo đảm chuyển đổi mượt mà không làm sập ứng dụng client.",
        "when_use": "- Khi cần loại bỏ các API endpoint cũ không còn an toàn hoặc không phù hợp với kiến trúc mới.\n- Khi thực hiện thay đổi phá vỡ tương thích (breaking changes) trên các API công khai cho bên thứ ba.\n- Khi xây dựng lộ trình chấm dứt hỗ trợ phiên bản API v1 để chuyển sang v2 theo hợp đồng dịch vụ (SLA).",
        "when_not_use": "- Khi chỉ sửa đổi logic nội bộ không thay đổi cấu trúc request/response của API.\n- Khi thêm trường mới có tính tương thích ngược hoàn toàn (non-breaking additions).",
        "prereqs": "- **Ngữ cảnh đầu vào:** Danh sách endpoint cần khai tử, thời hạn sunset chính thức, hệ thống phân tích API access logs nhận diện client theo API Key / Client ID.\n- **Quyền hạn truy cập:** Quyền sửa đổi mã nguồn API gateway hoặc middleware response headers.",
        "concepts": "- **RFC 8594 Sunset Header:** Header chuẩn hóa thông báo thời điểm chính xác endpoint sẽ ngừng hoạt động vĩnh viễn (ví dụ: `Sunset: Wed, 11 Nov 2026 00:00:00 GMT`).\n- **Deprecation HTTP Header:** Báo hiệu endpoint đã bị phản đối và cung cấp link dẫn tới tài liệu di chuyển (ví dụ: `Deprecation: @1762819200; link=\"<https://api.dex.dev/migrations/v1-to-v2>\"`).\n- **Brownout Testing:** Tạm thời tắt API cũ trong khoảng thời gian ngắn (ví dụ: 15 phút) trước ngày sunset để phát hiện các client còn dùng mà chưa liên hệ.",
        "workflow": "1. Công bố thông báo deprecation chính thức kèm theo Migration Guide tối thiểu 6-12 tháng trước ngày sunset.\n2. Cài đặt middleware tự động trả về các HTTP header `Deprecation` và `Sunset` trên tất cả endpoint thuộc diện khai tử.\n3. Thiết lập dashboard đo lường số lượng request hàng ngày theo từng API Key / Client ID còn gọi vào endpoint cũ.\n4. Gửi email cảnh báo tự động tới các khách hàng vẫn còn lưu lượng truy cập cao khi thời hạn sunset đến gần.\n5. Tiến hành Brownout testing định kỳ (tắt tạm thời trong giờ thấp điểm) để cảnh tỉnh các lập trình viên client.\n6. Đến ngày Sunset: chuyển đổi response vĩnh viễn sang mã lỗi `HTTP 410 Gone` kèm theo link hướng dẫn nâng cấp.",
        "examples": """### Ví dụ middleware thêm header Deprecation & Sunset trong Node.js Express:
```typescript
import { Request, Response, NextFunction } from 'express';

export function deprecationMiddleware(sunsetDate: string, docUrl: string) {
  return (req: Request, res: Response, next: NextFunction) => {
    // 1. Thêm chuẩn header theo RFC 8594
    res.setHeader('Deprecation', 'true');
    res.setHeader('Sunset', sunsetDate); // e.g., "Wed, 11 Nov 2026 00:00:00 GMT"
    res.setHeader('Link', `<${docUrl}>; rel="deprecation"; type="text/html"`);

    // 2. Ghi nhận telemetry client ID đang gọi endpoint cũ
    const clientId = req.headers['x-api-key'] || 'anonymous';
    console.warn(`[API-DEPRECATION] Client ${clientId} called deprecated endpoint: ${req.originalUrl}`);

    next();
  };
}
```""",
        "antipatterns": "- **Silent Breaking Changes:** Đột ngột xóa hoặc sửa kiểu dữ liệu endpoint mà không báo trước cho khách hàng bên thứ ba.\n- **Indefinite Deprecation:** Đánh dấu deprecated nhưng để tồn tại 10 năm không bao giờ sunset khiến hệ thống gánh nợ kỹ thuật nặng nề.\n- **Generic Error Codes:** Trả về `500 Internal Server Error` thay vì mã chuẩn `410 Gone` khi endpoint chính thức bị tắt.",
        "gates": "- **QG-02**: Tất cả response từ deprecated endpoint phải chứa đầy đủ header `Sunset` và `Link`.\n- **QG-08**: Đường dẫn migration guide trong header `Link` phải hoạt động và trả về HTTP 200.\n- **QG-14**: Tỷ lệ lưu lượng gọi vào endpoint cũ dưới 0.1% tổng lưu lượng trước khi tiến hành tắt hẳn.",
        "security": "- Đảm bảo các API endpoint cũ sắp bị khai tử vẫn nhận được các bản vá bảo mật khẩn cấp trong suốt thời gian bảo trì.\n- Thu hồi quyền truy cập của các client không chịu nâng cấp sau khi thời hạn sunset đã kết thúc.",
        "adapters": "- **API Gateways**: Kong Deprecation Plugin, AWS API Gateway custom response parameters.\n- **Frameworks**: Express.js, FastAPI, Spring Boot Interceptors.",
        "deliverables": "- Middleware gắn header RFC 8594 Deprecation & Sunset.\n- Tài liệu Migration Guide chuyển đổi phiên bản API.\n- Dashboard theo dõi lưu lượng client còn sót lại trước ngày sunset.",
        "related": "dex-api-engineering, dex-semantic-version-automation, dex-contract-first-development",
        "usage": """```powershell
# Kiểm tra sự hiện diện của các header Deprecation chuẩn mực trên endpoint
curl -I https://api.dex.dev/v1/legacy-resource
```"""
    },
    {
        "id": "dex-configuration-schema-design",
        "name": "dex-configuration-schema-design",
        "desc": "Design strictly typed, validated application configuration schemas with layered precedence, environment variable overrides, and secret leakage prevention. Use when bootstrapping applications or standardizing enterprise config management.",
        "purpose": "Thiết kế và chuẩn hóa schema cấu hình ứng dụng được định kiểu nghiêm ngặt (Strictly Typed Configuration Schema); quản lý độ ưu tiên đa tầng (Defaults < File < Env Vars < CLI flags), tự động xác thực tính hợp lệ lúc khởi động (fail-fast), và tuyệt đối ngăn ngừa rò rỉ secrets.",
        "when_use": "- Khi khởi tạo dự án mới cần hệ thống cấu hình vững chắc, tránh lỗi runtime do thiếu biến môi trường.\n- Khi chuẩn hóa cấu hình cho ứng dụng triển khai trên nhiều môi trường khác nhau (Local, Staging, Production, Multi-Cloud).\n- Khi bảo vệ các thông tin bí mật không bị in ra log hoặc serialize nhầm vào response.",
        "when_not_use": "- Khi chỉ cần lưu trữ các cờ bật/tắt tính năng động theo thời gian thực (nên sử dụng feature flag system như LaunchDarkly/Unleash).\n- Khi lưu trữ dữ liệu nghiệp vụ có tính thay đổi liên tục của người dùng.",
        "prereqs": "- **Ngữ cảnh đầu vào:** Danh sách các tham số cấu hình, kiểu dữ liệu, giá trị mặc định an toàn, và nguồn cung cấp (Environment Variables, YAML/JSON file, Vault).\n- **Quyền hạn truy cập:** Quyền định nghĩa tệp cấu hình và biến môi trường của ứng dụng.",
        "concepts": "- **Fail-Fast Startup Validation:** Ứng dụng từ chối khởi động ngay lập tức nếu thiếu bất kỳ biến cấu hình bắt buộc nào hoặc sai định dạng.\n- **Layered Configuration Precedence:** Thứ tự ưu tiên ghi đè rõ ràng: CLI arguments > Environment Variables > `.env` file > `config.yaml` > Hardcoded Safe Defaults.\n- **Secret Masking & Redaction:** Tự động che giấu các trường nhạy cảm (`password`, `secret`, `api_key`) trong hàm `toString()` và logging formatter.",
        "workflow": "1. Khai báo schema cấu hình bằng thư viện schema validation (Zod, Pydantic, Joi, hoặc JSON Schema).\n2. Gán các ràng buộc kiểm tra chi tiết (độ dài, khoảng giá trị cổng mạng 1-65535, định dạng URI hợp lệ, regex).\n3. Tải cấu hình theo thứ tự ưu tiên đa tầng và nạp giá trị vào schema.\n4. Thực hiện xác thực schema trong hàm `main()` hoặc entrypoint trước khi khởi tạo bất kỳ kết nối mạng hoặc database nào.\n5. Đánh dấu các trường nhạy cảm để loại bỏ khỏi output khi in cấu hình lúc khởi động ứng dụng.",
        "examples": """### Ví dụ schema cấu hình nghiêm ngặt bằng Pydantic v2 trong Python:
```python
from pydantic import BaseModel, Field, HttpUrl, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal

class DatabaseConfig(BaseModel):
    dsn: PostgresDsn = Field(..., description="PostgreSQL connection URI")
    max_connections: int = Field(default=20, ge=1, le=100)
    timeout_seconds: float = Field(default=5.0, ge=0.5)

class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        env_file=".env",
        extra="forbid" # Từ chối khởi động nếu có biến lạ không khai báo
    )

    environment: Literal["local", "staging", "production"] = "local"
    port: int = Field(default=8080, ge=1024, le=65535)
    database: DatabaseConfig
    api_secret_key: str = Field(..., min_length=32)

    def print_safe_summary(self):
        dump = self.model_dump()
        dump["api_secret_key"] = "[REDACTED]"
        dump["database"]["dsn"] = str(self.database.dsn).split("@")[-1] # Giấu credentials
        return dump

# Khi khởi động ứng dụng:
# settings = AppSettings() -> Tự động ném lỗi nếu thiếu biến bắt buộc!
```""",
        "antipatterns": "- **Lazy Configuration Evaluation:** Đọc biến môi trường `process.env.MY_VAR` rải rác bên trong các hàm sâu, khiến lỗi chỉ xuất hiện khi khách hàng gọi vào luồng đó.\n- **Permissive Defaults for Secrets:** Đặt giá trị mặc định cho secret key là chuỗi `change-me-in-prod` và quên đổi trên production.\n- **Printing Unredacted Config:** In toàn bộ đối tượng cấu hình ra stdout lúc khởi động làm lộ connection string chứa mật khẩu database trong log.",
        "gates": "- **QG-02**: Schema cấu hình có kiểu dữ liệu tường minh 100%, không sử dụng kiểu `any` hoặc chuỗi tự do.\n- **QG-06**: Quá trình khởi động kiểm tra không có secret key nào bị hardcode trong mã nguồn Git.\n- **QG-07**: Thời gian parse và validate cấu hình lúc khởi động dưới 100ms.",
        "security": "- Bắt buộc mã hóa các biến môi trường nhạy cảm khi lưu trữ trên CI/CD và quản lý thông qua Secret Managers (AWS Secrets Manager, HashiCorp Vault).\n- Khóa quyền truy cập tệp `.env` chỉ cho phép người dùng sở hữu tiến trình đọc được (chmod 600).",
        "adapters": "- **Python**: Pydantic Settings.\n- **Node/TypeScript**: Zod, Envalid.\n- **Go**: Viper, envconfig.\n- **Java**: Spring Boot ConfigurationProperties, Quarkus Config.",
        "deliverables": "- Mã nguồn khai báo Schema cấu hình được định kiểu chặt chẽ.\n- Tệp cấu hình mẫu `.env.example` với đầy đủ chú thích.\n- Bộ unit test kiểm tra cơ chế fail-fast khi thiếu biến môi trường.",
        "related": "dex-secrets-management, dex-code-organization, dex-development-workflow",
        "usage": """```powershell
# Chạy kiểm thử xác minh tính hợp lệ của schema cấu hình
pytest tests/config/test_configuration_schema.py -v
```"""
    },
    {
        "id": "dex-contract-first-development",
        "name": "dex-contract-first-development",
        "desc": "Architect and enforce contract-first API development using OpenAPI, Protobuf, or AsyncAPI schemas with automated code generation, mock servers, and breaking change diffing. Use when coordinating cross-team APIs or building resilient service contracts.",
        "purpose": "Thiết lập và thực thi phương pháp phát triển hướng hợp đồng (Contract-First Development); sử dụng các đặc tả OpenAPI, Protocol Buffers hoặc AsyncAPI làm nguồn chân lý duy nhất (Single Source of Truth), tự động sinh mã nguồn client/server, dựng mock server cho frontend song song, và tự động phát hiện thay đổi phá vỡ tương thích (breaking changes).",
        "when_use": "- Khi phát triển API phục vụ cho nhiều đội ngũ độc lập (Frontend, Mobile, Third-party partners).\n- Khi muốn đội ngũ client có thể tiến hành phát triển và kiểm thử ngay lập tức dựa trên mock server mà không cần chờ backend viết xong.\n- Khi cần ngăn chặn các sự cố tương thích phiên bản trước khi triển khai lên môi trường thử nghiệm.",
        "when_not_use": "- Khi xây dựng các script nhỏ dùng nội bộ dùng một lần không có sự phân tách giữa client và server.\n- Khi cấu trúc API đang thay đổi liên tục từng giờ trong giai đoạn hackathon sơ khai.",
        "prereqs": "- **Ngữ cảnh đầu vào:** Đặc tả nghiệp vụ, công cụ schema linter (Spectral, buf), công cụ sinh mã (OpenAPI Generator, protoc).\n- **Quyền hạn truy cập:** Quyền quản lý kho lưu trữ schema hợp đồng tập trung (Schema Registry hoặc Git repo).",
        "concepts": "- **Single Source of Truth:** Schema tệp đặc tả là chuẩn mực tối cao; code server và client đều được sinh tự động hoặc kiểm thử đối soát với schema này.\n- **Breaking Change Detection:** Tự động so sánh phiên bản schema mới với phiên bản đã phát hành trước đó trong CI/CD để phát hiện vi phạm quy tắc tương thích.\n- **Prism / Mock Server:** Công cụ tự động tạo HTTP server giả lập trả về dữ liệu mẫu chuẩn theo schema mà không cần viết mã backend.",
        "workflow": "1. Viết bản thiết kế hợp đồng API bằng OpenAPI v3.1 hoặc Protobuf v3 trước khi viết bất kỳ dòng mã backend nào.\n2. Chạy linter kiểm tra chuẩn đặt tên, tài liệu hóa trường dữ liệu và bảo mật bằng Spectral hoặc Buf lint.\n3. Khởi tạo mock server tự động để các đội ngũ Frontend và Mobile bắt đầu tích hợp ngay.\n4. Sử dụng công cụ sinh mã tự động để sinh ra Server Interfaces và Client SDKs cho các ngôn ngữ đích.\n5. Cài đặt kiểm tra breaking changes trong CI pipeline so sánh với branch chính (ví dụ: `buf breaking` hoặc `oasdiff`).\n6. Triển khai backend thực tế dựa trên Server Interfaces đã sinh và chạy kiểm thử contract test để chứng minh tính tương thích.",
        "examples": """### Ví dụ quy trình kiểm tra breaking changes và sinh mã từ OpenAPI trong CI (`buf` / `oasdiff`):
```bash
# 1. Kiểm tra linter chất lượng của OpenAPI schema
npx spectral lint specs/order-service-api.yaml

# 2. Khởi tạo mock server tức thời cho đội Frontend
npx prism mock specs/order-service-api.yaml -p 4010 &

# 3. Kiểm tra thay đổi phá vỡ tương thích so với bản phát hành trước trên Git
oasdiff -base main.yaml -revision specs/order-service-api.yaml -fail-on-breaking

# 4. Tự động sinh TypeScript API Client SDK
npx @openapitools/openapi-generator-cli generate \\
  -i specs/order-service-api.yaml \\
  -g typescript-axios \\
  -o generated/clients/typescript
```""",
        "antipatterns": "- **Code-First Drift:** Viết code backend xong rồi dùng annotation để sinh ngược lại schema, dẫn tới schema bị méo mó theo ngôn ngữ lập trình và mất tính trung lập.\n- **Uncommunicated Schema Mutations:** Tự ý sửa đổi kiểu dữ liệu của một trường trong API mà không thông qua quy trình review hợp đồng.\n- **Handcrafted Client SDKs:** Tự viết tay hàng ngàn dòng code gọi API trên client dẫn tới dễ sai sót chính tả và tốn công bảo trì.",
        "gates": "- **QG-02**: Schema đặc tả hợp đồng vượt qua 100% các bài kiểm tra linter theo bộ quy tắc của tổ chức.\n- **QG-08**: Không có breaking change nào xuất hiện mà không được tăng số phiên bản Major theo chuẩn SemVer.\n- **QG-09**: Tất cả các trường dữ liệu và mã lỗi HTTP đều có mô tả tài liệu chi tiết.",
        "security": "- Bắt buộc định nghĩa cơ chế bảo mật (Security Schemes như OAuth2, Bearer JWT, APIKey) trực tiếp trong schema hợp đồng.\n- Xác định rõ ràng các trường dữ liệu bắt buộc và kiểm tra giới hạn kích thước payload (max length, regex format) để phòng chống DoS.",
        "adapters": "- **OpenAPI Tools**: Spectral, Prism, OpenAPI Generator, oasdiff.\n- **Protobuf / gRPC Tools**: Buf CLI, protoc, grpc-gateway.\n- **AsyncAPI**: AsyncAPI Studio, Generator.",
        "deliverables": "- Tệp đặc tả hợp đồng API chuẩn hóa (`.yaml` hoặc `.proto`).\n- SDK client được sinh tự động cho các nền tảng client.\n- Báo cáo kiểm tra tương thích ngược tự động từ CI.",
        "related": "dex-api-engineering, dex-architecture-decision-records, dex-semantic-version-automation",
        "usage": """```powershell
# Chạy công cụ kiểm tra vi phạm tương thích ngược của hợp đồng API
oasdiff -base specs/v1.0.0.yaml -revision specs/v1.1.0.yaml -fail-on-breaking
```"""
    },

    # =========================================================================
    # GROUP AF: Distributed Systems Deep Engineering (Skills 311–320)
    # =========================================================================
    {
        "id": "dex-exactly-once-claims-audit",
        "name": "dex-exactly-once-claims-audit",
        "desc": "Audit and rigorously verify distributed message delivery guarantees, debunking impossible exactly-once claims and enforcing idempotent consumer patterns with transactional outboxes. Use when verifying payment pipelines or critical distributed transactions.",
        "purpose": "Kiểm toán và phản biện các tuyên bố bảo đảm phân phối tin nhắn 'Exactly-Once' trong hệ thống phân tán; phân tích giới hạn của bài toán Hai Vị Tướng (Two Generals' Problem) và FLP Impossibility, thiết kế giải pháp thực tế dựa trên phân phối At-Least-Once kết hợp xử lý Idempotent Consumer và Transactional Outbox.",
        "when_use": "- Khi kiểm toán hệ thống thanh toán, kế toán hoặc xử lý đơn hàng có rủi ro trùng lặp giao dịch tài chính.\n- Khi đánh giá đề xuất kỹ thuật tuyên bố hệ thống có thể đạt được 'end-to-end exactly-once' qua mạng không đáng tin cậy.\n- Khi thiết kế cơ chế bảo vệ chống trùng lặp thông điệp (deduplication) trên hạ tầng Kafka, RabbitMQ hoặc AWS SQS.",
        "when_not_use": "- Khi dữ liệu chỉ là số liệu đo lường IoT cảm biến hoặc log phân tích thông thường cho phép sai số nhỏ.\n- Khi toàn bộ quá trình đọc ghi chỉ diễn ra trong một tiến trình đơn lẻ có giao dịch ACID trên một cơ sở dữ liệu duy nhất.",
        "prereqs": "- **Ngữ cảnh đầu vào:** Sơ đồ luồng dữ liệu thông điệp phân tán, cấu hình broker/queue, cơ chế lưu trữ deduplication key và database transaction log.\n- **Quyền hạn truy cập:** Quyền kiểm tra mã nguồn consumer và lịch sử xử lý thông điệp.",
        "concepts": "- **Network Impossibility Proof:** Không thể bảo đảm exactly-once delivery qua mạng vật lý nếu không có sự phối hợp giữa stateful deduplication và transactional boundary tại tầng ứng dụng.\n- **Transactional Outbox Pattern:** Ghi thông điệp cần gửi vào bảng `outbox` trong cùng một database transaction với dữ liệu nghiệp vụ, sau đó worker riêng biệt đọc và gửi đi.\n- **Idempotency Key & Deduplication Window:** Khóa duy nhất đại diện cho giao dịch được lưu trữ trong bảng `processed_messages` với thời gian tồn tại (TTL) xác định.",
        "workflow": "1. Khảo sát toàn bộ các điểm giao tiếp mạng trong đường ống thông điệp từ Producer, Broker tới Consumer.\n2. Phân tích kịch bản Producer retry khi bị network timeout: chứng minh thông điệp có thể bị gửi trùng lặp tới Broker.\n3. Phân tích kịch bản Consumer crash ngay sau khi xử lý nghiệp vụ nhưng trước khi gửi ACK tới Broker: chứng minh thông điệp sẽ bị gửi lại lần thứ hai.\n4. Thiết lập bảng lưu vết khóa trùng lặp (`idempotency_keys`) với khóa chính duy nhất trên cơ sở dữ liệu của Consumer.\n5. Đóng gói logic xử lý của Consumer bên trong một database transaction duy nhất bao gồm: chèn khóa idempotency và cập nhật nghiệp vụ.\n6. Chạy kịch bản kiểm thử truyền tin nhắn trùng lặp (duplicate injection) để chứng minh số dư không bị thay đổi hai lần.",
        "examples": """### Ví dụ cơ chế Consumer Deduplication bảo đảm tính idempotent trong PostgreSQL:
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
```""",
        "antipatterns": "- **Believing Broker Exactly-Once Magic:** Tin tưởng hoàn toàn vào cờ `enable.idempotence=true` của Kafka mà không triển khai deduplication tại database của Consumer cuối.\n- **In-Memory Deduplication Cache:** Lưu trữ các message ID đã xử lý trong RAM của consumer, dẫn tới khi tiến trình bị khởi động lại sẽ xử lý lại toàn bộ thông điệp trùng lặp.\n- **Separate Deduplication Step:** Kiểm tra trùng lặp và ghi dữ liệu nghiệp vụ trong hai transaction rời rạc tạo ra race condition nghiêm trọng.",
        "gates": "- **QG-06**: Hệ thống từ chối các đề xuất kiến trúc tuyên bố 'Exactly-Once' mà không có bảng lưu vết idempotency key.\n- **QG-09**: Khả năng chống trùng lặp được chứng minh bằng test tự động bơm 1,000 thông điệp trùng lặp liên tiếp.\n- **QG-10**: Không có bất kỳ sai lệch số dư nào xảy ra sau các đợt kiểm thử crash fault injection.",
        "security": "- Khóa idempotency phải được tạo ra từ nguồn dữ liệu đáng tin cậy (client signature hoặc UUID cryptographically secure).\n- Ngăn chặn việc tấn công làm nghẽn bảng deduplication bằng cách cấu hình TTL tự động dọn dẹp các khóa quá cũ.",
        "adapters": "- **Brokers**: Apache Kafka, AWS SQS FIFO, RabbitMQ.\n- **Databases**: PostgreSQL Unique Constraints, Redis SETNX with TTL.",
        "deliverables": "- Báo cáo kiểm toán độ tin cậy của đường ống thông điệp phân tán.\n- Mã nguồn Idempotent Consumer và Transactional Outbox.\n- Bộ kiểm thử tự động bơm thông điệp trùng lặp (Duplicate Injection Test Suite).",
        "related": "dex-idempotent-operations, dex-distributed-consistency, dex-event-driven-architecture",
        "usage": """```powershell
# Chạy bộ kiểm thử khả năng chống trùng lặp khi bơm tin nhắn lặp lại
pytest tests/distributed/test_idempotent_deduplication.py -v
```"""
    },
    {
        "id": "dex-message-poison-queue-recovery",
        "name": "dex-message-poison-queue-recovery",
        "desc": "Architect dead-letter queues (DLQ), poison message triage workflows, bounded exponential backoff retries, and safe replay mechanisms. Use when handling malformed or unprocessable streaming messages without halting consumers.",
        "purpose": "Thiết kế và quản trị hàng đợi thông điệp độc (Dead-Letter Queue - DLQ); cài đặt cơ chế thử lại có giới hạn với hàm mũ lùi (bounded exponential backoff), phân loại và cô lập thông điệp độc hại mà không làm tắc nghẽn toàn bộ hàng đợi của hệ thống, cùng công cụ phát lại an toàn (safe replay).",
        "when_use": "- Khi consumer gặp phải thông điệp bị lỗi định dạng cú pháp (malformed JSON) hoặc vi phạm ràng buộc dữ liệu không thể xử lý thành công.\n- Khi lỗi xảy ra liên tục khiến consumer bị crash lặp đi lặp lại (CrashLoopBackOff) làm nghẽn dòng thông điệp phía sau.\n- Khi cần công cụ phân tích nguyên nhân gốc và phát lại các thông điệp đã sửa lỗi vào hàng đợi chính.",
        "when_not_use": "- Khi lỗi chỉ là lỗi tạm thời của mạng kết nối tới database có thể tự hết sau vài mili-giây (sử dụng in-memory retry ngắn).\n- Khi hệ thống cho phép bỏ qua và loại bỏ thông điệp lỗi hoàn toàn mà không cần lưu vết kiểm toán.",
        "prereqs": "- **Ngữ cảnh đầu vào:** Cấu hình Message Broker (Kafka, SQS, RabbitMQ), hàng đợi chính và hàng đợi phụ DLQ, chính sách retry tối đa (Max Deliveries).\n- **Quyền hạn truy cập:** Quyền tạo hàng đợi DLQ và quyền di chuyển/phát lại thông điệp.",
        "concepts": "- **Poison Message:** Thông điệp gây ra lỗi không thể khắc phục mỗi khi được đọc, khiến consumer bị treo hoặc crash liên tục.\n- **Dead-Letter Queue (DLQ):** Hàng đợi cách ly đặc biệt nơi các thông điệp đã thử lại vượt quá số lần cho phép (`max_retries`) được chuyển tới để phân tích thủ công.\n- **Safe Redrive / Replay Tooling:** Quy trình kiểm duyệt, sửa đổi payload bị lỗi (nếu cần) và phát lại thông điệp từ DLQ vào hàng đợi chính có kiểm soát tốc độ.",
        "workflow": "1. Thiết lập ngưỡng thử lại tối đa (ví dụ: `max_retries = 3`) và cấu hình DLQ tương ứng cho từng hàng đợi nghiệp vụ.\n2. Cài đặt middleware bắt exception: phân biệt lỗi tạm thời (Transient error - retry với exponential backoff) và lỗi vĩnh viễn (Fatal error - đẩy ngay sang DLQ).\n3. Đính kèm siêu dữ liệu chẩn đoán vào header của thông điệp khi đẩy sang DLQ: `x-exception-message`, `x-stack-trace`, `x-original-queue`, `x-failure-timestamp`.\n4. Giám sát số lượng thông điệp trong DLQ và kích hoạt cảnh báo tới đội On-call khi số lượng thông điệp độc vượt ngưỡng 0.\n5. Xây dựng CLI script hỗ trợ xem trước nội dung thông điệp trong DLQ và phát lại an toàn theo batch.",
        "examples": """### Ví dụ xử lý poison message và đẩy sang DLQ an toàn trong Python:
```python
import json
import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)

def process_message_with_dlq(message: Dict[str, Any], broker_client) -> bool:
    max_retries = 3
    current_retries = message.get("headers", {}).get("retry_count", 0)

    try:
        # Giả lập xử lý nghiệp vụ
        payload = json.loads(message["body"])
        if "account_id" not in payload:
            raise ValueError("Malformed payload: Missing required account_id")
        
        execute_business_logic(payload)
        return True

    except Exception as exc:
        logger.error(f"Error processing message {message.get('id')}: {exc}")
        if current_retries < max_retries:
            # Thử lại có exponential backoff
            message.setdefault("headers", {})["retry_count"] = current_retries + 1
            broker_client.requeue_with_delay(message, delay_seconds=2 ** current_retries)
        else:
            # Vượt quá giới hạn -> Đẩy sang Dead Letter Queue
            dlq_message = {
                "original_message": message,
                "error_details": {
                    "exception_class": exc.__class__.__name__,
                    "error_message": str(exc),
                    "failed_at": "2026-10-22T00:00:00Z"
                }
            }
            broker_client.send_to_dlq(dlq_message)
            logger.critical(f"Poison message isolated into DLQ: {message.get('id')}")
        return False
```""",
        "antipatterns": "- **Infinite Retry Storm:** Thử lại thông điệp lỗi vĩnh viễn với tần suất liên tục không có backoff làm nghẽn CPU và tràn log.\n- **Drop and Forget:** Bỏ qua thông điệp lỗi mà không lưu vào DLQ, dẫn tới mất mát dữ liệu khách hàng mà không ai hay biết.\n- **Unbounded DLQ Accumulation:** Coi DLQ như một bãi rác và không bao giờ thiết lập cảnh báo hoặc quy trình xử lý định kỳ.",
        "gates": "- **QG-03**: Khi consumer gặp thông điệp độc, thông điệp được chuyển vào DLQ thành công và consumer tiếp tục xử lý các tin nhắn tiếp theo.\n- **QG-06**: Header lỗi đính kèm trong DLQ không được chứa thông tin nhạy cảm hoặc mật khẩu.\n- **QG-10**: Có kịch bản kiểm thử tự động chứng minh hàng đợi không bị nghẽn khi có 10% thông điệp độc hại.",
        "security": "- Giới hạn quyền truy cập vào DLQ vì payload trong DLQ có thể chứa các thông điệp lỗi mang dữ liệu nhạy cảm.\n- Làm sạch dữ liệu trước khi phát lại để tránh việc đưa lại mã độc tấn công vào hệ thống chính.",
        "adapters": "- **AWS**: Amazon SQS Dead-Letter Queues with Redrive Policy.\n- **RabbitMQ**: Dead Letter Exchanges (DLX) & x-dead-letter-routing-key.\n- **Kafka**: Error-handling deserializer & Dead Letter Topic.",
        "deliverables": "- Module Consumer bọc cơ chế xử lý Poison Message.\n- Tệp cấu hình DLQ và Redrive Policy.\n- CLI script hỗ trợ phân tích và phát lại thông điệp từ DLQ.",
        "related": "dex-background-job-queues, dex-consumer-lag-control, dex-event-driven-architecture",
        "usage": """```powershell
# Xem danh sách thông điệp trong DLQ và phát lại vào hàng đợi chính
python scripts/dlq_manager.py list --queue orders_dlq
python scripts/dlq_manager.py redrive --queue orders_dlq --limit 10
```"""
    },
    {
        "id": "dex-distributed-lock-lease-safety",
        "name": "dex-distributed-lock-lease-safety",
        "desc": "Implement distributed locks and leases with fencing tokens, lock renewal heartbeats, and fail-safe timeouts. Use when coordinating exclusive access to non-transactional shared resources across distributed worker clusters.",
        "purpose": "Thiết kế và cài đặt khóa phân tán (Distributed Locks) và cơ chế thuê quyền (Leases) bảo đảm an toàn tuyệt đối; tích hợp Fencing Tokens để ngăn chặn xung đột dữ liệu do tiến trình bị trễ GC (Stop-The-World) hoặc phân mảnh mạng, kiểm soát heartbeat gia hạn khóa tự động.",
        "when_use": "- Khi nhiều worker phân tán cùng cần truy cập độc quyền vào một tài nguyên không hỗ trợ transaction (ví dụ: tạo tệp PDF trên S3, gọi API của bên thứ ba không có concurrency control).\n- Khi bầu chọn tiến trình trưởng (Leader Election) trong cụm worker chạy ngầm.\n- Khi cần giới hạn chỉ một cron job duy nhất được thực thi tại một thời điểm trên toàn bộ cluster.",
        "when_not_use": "- Khi tài nguyên chia sẻ là một cơ sở dữ liệu quan hệ có hỗ trợ câu lệnh khóa dòng `SELECT ... FOR UPDATE`.\n- Khi mục tiêu chỉ là đồng bộ hóa giữa các luồng (threads) bên trong cùng một tiến trình ứng dụng đơn lẻ.",
        "prereqs": "- **Ngữ cảnh đầu vào:** Kho lưu trữ khóa phân tán có hỗ trợ thao tác nguyên tử và TTL (Redis, Consul, Etcd, Zookeeper), tài nguyên dùng chung cần bảo vệ.\n- **Quyền hạn truy cập:** Quyền đọc/ghi các key phân tán trên cụm Redis/Etcd.",
        "concepts": "- **Fencing Token:** Số nguyên tăng đơn điệu được trả về mỗi khi khóa được cấp phát; tầng lưu trữ tài nguyên sẽ từ chối các thao tác ghi mang token nhỏ hơn token mới nhất đã thấy.\n- **Lock Lease TTL:** Thời hạn tồn tại tự động hết hạn của khóa nhằm tránh trường hợp tiến trình nắm giữ khóa bị chết đột ngột khiến khóa bị khóa vĩnh viễn (deadlock).\n- **Heartbeat Lock Renewal:** Tiến trình nền tự động gia hạn TTL của khóa định kỳ khi tác vụ vẫn đang tiếp tục chạy bình thường.",
        "workflow": "1. Yêu cầu cấp phát khóa nguyên tử kèm theo thời gian sống TTL ngắn (ví dụ: 10 giây) và nhận Fencing Token tăng dần.\n2. Khởi tạo tác vụ nền (background thread/coroutine) để tự động gia hạn khóa sau mỗi 1/3 chu kỳ TTL.\n3. Gửi Fencing Token kèm theo mọi thao tác ghi tới tài nguyên chia sẻ bên ngoài.\n4. Tầng lưu trữ tài nguyên xác nhận Fencing Token $\\\\ge$ Fencing Token hiện tại trước khi cho phép ghi.\n5. Khi hoàn thành công việc: dừng heartbeat gia hạn và giải phóng khóa an toàn bằng cách so sánh đúng token sở hữu (tránh xóa nhầm khóa của tiến trình khác).\n6. Bắt lỗi quá hạn khóa: nếu heartbeat thất bại và khóa hết hạn, tiến trình lập tức hủy bỏ tác vụ ngay để tránh ghi đè dữ liệu sai lệch.",
        "examples": """### Ví dụ giải phóng khóa an toàn bằng Lua Script trong Redis:
```lua
-- Lua script giải phóng khóa an toàn: Chỉ xóa nếu giá trị token khớp chính xác
if redis.call("get", KEYS[1]) == ARGV[1] then
    return redis.call("del", KEYS[1])
else
    return 0
end
```

### Triển khai Fencing Token kiểm tra tại tầng lưu trữ:
```python
class StorageService:
    def __init__(self):
        self.highest_fencing_token = 0

    def write_data(self, fencing_token: int, payload: dict):
        if fencing_token < self.highest_fencing_token:
            # Phát hiện Zombie Process bị trễ GC cố ghi dữ liệu cũ
            raise RuntimeError(f"Fencing token {fencing_token} is stale. Current: {self.highest_fencing_token}")
        
        self.highest_fencing_token = fencing_token
        self.commit_to_disk(payload)
        return True
```""",
        "antipatterns": "- **Naive Redis Lock:** Dùng lệnh `SETNX` không có TTL khiến server crash làm hệ thống bị treo cứng vĩnh viễn.\n- **Blind Lock Deletion:** Dùng lệnh `DEL key` đơn giản để giải phóng khóa, dẫn tới việc xóa mất khóa mới của tiến trình khác khi tiến trình hiện tại bị chạy quá giờ.\n- **Locking without Fencing:** Nghĩ rằng có distributed lock là đủ an toàn mà không kiểm tra fencing token, để tiến trình bị lag GC ghi đè làm hỏng dữ liệu của tiến trình mới.",
        "gates": "- **QG-05**: Thao tác giải phóng khóa bắt buộc sử dụng Lua script hoặc CAS nguyên tử có so sánh token sở hữu.\n- **QG-09**: Tất cả các thao tác ghi vào tài nguyên chia sẻ đều bắt buộc kiểm tra fencing token tăng đơn điệu.\n- **QG-10**: Khóa tự động được giải phóng an toàn trong vòng 10 giây nếu tiến trình nắm giữ bị tắt đột ngột (`kill -9`).",
        "security": "- Token sở hữu khóa phải là chuỗi ngẫu nhiên có độ dài tối thiểu 128-bit (cryptographically secure random string).\n- Phân quyền hạn chế các dịch vụ không liên quan có thể ghi đè các key khóa phân tán trên Redis.",
        "adapters": "- **Redis**: Redlock algorithm, redis-py, ioredis.\n- **Consul / Etcd**: Distributed Sessions and Key-Value Leases with Raft consensus.",
        "deliverables": "- Module quản lý Distributed Lock & Lease có tích hợp Fencing Token.\n- Lua script giải phóng và gia hạn khóa nguyên tử.\n- Bộ kiểm thử giả lập lỗi GC pause và network split-brain.",
        "related": "dex-concurrency-state, dex-distributed-consistency, dex-clock-skew-resilience",
        "usage": """```powershell
# Chạy bộ kiểm thử tính an toàn của Distributed Lock khi gặp kịch bản timeout
pytest tests/distributed/test_distributed_locks.py -v
```"""
    },
    {
        "id": "dex-scheduler-misfire-recovery",
        "name": "dex-scheduler-misfire-recovery",
        "desc": "Diagnose missed distributed scheduler triggers, engineer catch-up recovery policies, and enforce leader election concurrency safeguards. Use when running mission-critical periodic jobs or financial reconciliation schedules.",
        "purpose": "Chẩn đoán và khắc phục sự cố lịch trình phân tán bị trượt lượt chạy (Scheduler Misfire); thiết lập các chính sách bù đắp (catch-up / backfill policies) có kiểm soát, ngăn chặn hiện tượng chạy bão lặp lại sau sự cố, và bảo đảm tính độc quyền thực thi lịch trình qua cơ chế Leader Election.",
        "when_use": "- Khi hệ thống lập lịch định kỳ (Cron, Quartz, Celery Beat, CloudWatch Events) bị trễ hoặc bỏ lỡ thời điểm kích hoạt do quá tải hoặc sập máy chủ.\n- Khi vận hành các tác vụ định kỳ tối quan trọng như chốt sổ tài chính hàng đêm, tạo hóa đơn tự động định kỳ hàng tháng.\n- Khi triển khai cụm scheduler dự phòng nhiều node (High Availability) cần bảo đảm chỉ có đúng một node được quyền kích hoạt job.",
        "when_not_use": "- Khi tác vụ chỉ là việc dọn dẹp bộ nhớ đệm tạm thời cho phép bỏ qua nếu bị trượt lượt.\n- Khi tác vụ được kích hoạt theo luồng sự kiện thời gian thực (Event-Driven) thay vì dựa trên đồng hồ thời gian.",
        "prereqs": "- **Ngữ cảnh đầu vào:** Biểu thức Cron, bảng ghi nhận lịch sử thực thi (`job_executions`), chính sách xử lý trượt lịch (Fire Now, Ignore, Catch-up All).\n- **Quyền hạn truy cập:** Quyền cấu hình hệ thống scheduler và bảng metadata trạng thái job.",
        "concepts": "- **Misfire Instruction:** Quy tắc xác định hành vi cần làm khi thời điểm kích hoạt của job bị bỏ lỡ quá ngưỡng chịu đựng (misfire threshold).\n- **Catch-Up Policy:** Quyết định thực thi bù: chạy bù tất cả các lượt đã mất (Run all missed), gộp lại thành một lượt duy nhất (Coalesce into single run), hoặc bỏ qua chờ lượt tiếp theo (Ignore).\n- **Idempotent Job Run:** Mỗi lượt thực thi định kỳ mang một `scheduled_tick_time` duy nhất; nếu lượt đó đã được ghi nhận hoàn thành thì không được chạy lại.",
        "workflow": "1. Khảo sát danh mục toàn bộ cron jobs và phân loại mức độ quan trọng cùng chính sách misfire tương ứng.\n2. Thiết lập bảng lưu vết lịch sử kích hoạt (`job_execution_history`) lưu giữ `job_name`, `scheduled_at`, `status`, `started_at`, `finished_at`.\n3. Cài đặt cơ chế Leader Election sử dụng lease/lock phân tán để bảo đảm chỉ có 1 node scheduler duy nhất đóng vai trò active coordinator.\n4. Xây dựng logic phát hiện misfire: khi scheduler khởi động lại, so sánh thời điểm chạy dự kiến gần nhất với thời gian hiện tại.\n5. Áp dụng chính sách bù đắp: nếu là tác vụ tài chính thì chạy bù tuần tự từng khoảng thời gian bị lỡ; nếu là tác vụ tổng hợp dữ liệu thì chạy gộp một lần duy nhất.\n6. Ghi log kiểm toán và bắn cảnh báo về số lượng lượt chạy bị misfire đã được xử lý.",
        "examples": """### Ví dụ cấu hình chính sách Misfire và bảng theo dõi trong SQL:
```sql
CREATE TABLE scheduled_job_runs (
    job_name VARCHAR(100) NOT NULL,
    expected_tick TIMESTAMPTZ NOT NULL,
    status VARCHAR(20) NOT NULL, -- PENDING, RUNNING, COMPLETED, MISFIRED
    node_id VARCHAR(100),
    executed_at TIMESTAMPTZ,
    PRIMARY KEY (job_name, expected_tick)
);

-- Khi scheduler kích hoạt: Thử chiếm quyền chạy cho lượt expected_tick cụ thể
INSERT INTO scheduled_job_runs (job_name, expected_tick, status, node_id, executed_at)
VALUES ('generate_nightly_invoices', '2026-10-22 00:00:00Z', 'RUNNING', 'node-prod-01', NOW())
ON CONFLICT (job_name, expected_tick) DO NOTHING;
-- Nếu INSERT thành công (rows affected = 1) -> Node được phép chạy job!
```""",
        "antipatterns": "- **Misfire Stampede:** Máy chủ bị sập 10 ngày, khi bật lại lập tức kích hoạt 10,000 lượt chạy bù cùng một giây làm sập toàn bộ hệ thống cơ sở dữ liệu.\n- **Silent Dropping:** Scheduler bị treo trong đêm khiến không có bất kỳ báo cáo tài chính nào được tạo ra nhưng sáng hôm sau không ai nhận được cảnh báo.\n- **Multiple Leader Dual Execution:** Hai node scheduler cùng tưởng mình là leader và kích hoạt gửi hai lần email sao kê cho toàn bộ khách hàng.",
        "gates": "- **QG-03**: Hệ thống có khả năng tự động phát hiện và chạy bù lượt misfire theo đúng chính sách đã cấu hình.\n- **QG-09**: Không có bất kỳ khoảng thời gian scheduled tick nào bị thực thi hai lần do xung đột giữa các nodes.\n- **QG-10**: Leader election chuyển giao quyền kích hoạt lịch trình sang node dự phòng trong dưới 15 giây khi node chính gặp sự cố.",
        "security": "- Ngăn ngừa việc can thiệp trái phép vào bảng lịch trình để kích hoạt các job nhạy cảm ngoài giờ quy định.\n- Phân quyền tối thiểu cho tiến trình scheduler chỉ được gọi các endpoint đã được chứng thực.",
        "adapters": "- **Python**: APScheduler, Celery Beat with RedBeat.\n- **Java**: Quartz Scheduler with JDBC JobStore.\n- **Go**: gocron, robfig/cron with distributed locks.",
        "deliverables": "- Module quản lý chính sách Scheduler Misfire Recovery.\n- Bảng schema lưu vết lịch sử thực thi các lượt chạy định kỳ.\n- Kịch bản kiểm thử giả lập mất điện server scheduler và kiểm tra quá trình chạy bù.",
        "related": "dex-background-job-queues, dex-distributed-lock-lease-safety, dex-clock-skew-resilience",
        "usage": """```powershell
# Kiểm tra lịch sử thực thi và các job bị misfire trong 24 giờ qua
python scripts/scheduler_health.py --check-misfires --window 24h
```"""
    },
    {
        "id": "dex-regional-outage-exercises",
        "name": "dex-regional-outage-exercises",
        "desc": "Simulate and execute controlled multi-region cloud outage drills, DNS failover rerouting, stateful database promotion, and RTO/RPO measurement. Use when proving disaster recovery readiness or passing enterprise business continuity audits.",
        "purpose": "Mô phỏng và thực thi có kiểm soát các bài tập ứng phó sự cố sập trung tâm dữ liệu khu vực (Regional Cloud Outage Drills / Disaster Recovery); kiểm chứng cơ chế tự động chuyển vùng DNS, nâng cấp cơ sở dữ liệu phụ thành chính (Database Promotion), và đo lường chính xác các chỉ số RTO (Recovery Time Objective) và RPO (Recovery Point Objective).",
        "when_use": "- Khi chuẩn bị cho các đợt diễn tập ứng phó thảm họa định kỳ theo yêu cầu của hội đồng quản trị hoặc kiểm toán tuân thủ (SOC 2, ISO 22301).\n- Khi xác nhận năng lực phục vụ liên tục của hệ thống đa vùng (Multi-Region Active-Passive hoặc Active-Active).\n- Khi kiểm chứng xem quy trình tài liệu vận hành thảm họa (Disaster Recovery Runbook) có thực sự hoạt động trong thực tế hay không.",
        "when_not_use": "- Khi hệ thống chỉ được mua gói hạ tầng đơn vùng (Single Region) và chưa có môi trường dự phòng thứ hai.\n- Khi chưa có sự phê duyệt và giám sát trực tiếp từ đội ngũ chỉ huy sự cố (Incident Commander).",
        "prereqs": "- **Ngữ cảnh đầu vào:** Kế hoạch diễn tập thảm họa đã phê duyệt, hệ thống DNS có hỗ trợ Health Checks và Failover (Route53, Cloudflare), cụm database có Replica tại vùng dự phòng.\n- **Quyền hạn truy cập:** Quyền quản trị hạ tầng đám mây và DNS định tuyến mạng.",
        "concepts": "- **RTO (Recovery Time Objective):** Khoảng thời gian tối đa cho phép hệ thống phục hồi lại dịch vụ bình thường sau sự cố (ví dụ: RTO < 15 phút).\n- **RPO (Recovery Point Objective):** Lượng dữ liệu tối đa chấp nhận bị mất mát tính theo đơn vị thời gian do độ trễ sao chép bất đồng bộ (ví dụ: RPO < 1 phút).\n- **Split-Brain Prevention:** Cơ chế bảo đảm khi vùng dự phòng được nâng cấp làm chính thì vùng cũ phải bị cách ly hoàn toàn (fenced off) để tránh hai vùng cùng ghi dữ liệu mâu thuẫn.",
        "workflow": "1. Họp thống nhất phạm vi diễn tập, phân công vai trò (Incident Commander, Tech Leads, Scribe) và xác định điều kiện dừng khẩn cấp (Abort Criteria).\n2. Ghi nhận chỉ số latency sao chép database hiện tại để ước tính RPO ban đầu.\n3. Kích hoạt giả lập sự cố sập vùng chính: ngắt toàn bộ lưu lượng vào vùng chính tại tầng DNS hoặc cô lập Security Groups.\n4. Bắt đầu bấm giờ đo RTO; theo dõi hệ thống DNS tự động chuyển hướng request sang vùng dự phòng hoặc thực hiện chuyển đổi thủ công theo runbook.\n5. Nâng cấp database replica tại vùng dự phòng thành primary write master.\n6. Chạy bộ smoke test kiểm thử toàn diện trên vùng mới để xác nhận chức năng đọc/ghi bình thường.\n7. Dừng bấm giờ, tính toán RTO/RPO thực tế, và thực hiện quy trình phục hồi về trạng thái ban đầu (Failback).",
        "examples": """### Ví dụ kịch bản kiểm tra chuyển đổi DNS Failover trong Route53 bằng AWS CLI:
```bash
# 1. Giả lập vùng us-east-1 bị lỗi bằng cách chuyển trạng thái Health Check sang UNHEALTHY
aws route53 change-resource-record-sets \\
  --hosted-zone-id Z123456EXAMPLE \\
  --change-batch '{
    "Changes": [{
      "Action": "UPSERT",
      "ResourceRecordSet": {
        "Name": "health-primary.dex.dev.",
        "Type": "A",
        "TTL": 60,
        "ResourceRecords": [{"Value": "192.0.2.1"}]
      }
    }]
  }'

# 2. Theo dõi bản ghi DNS công khai xem đã chuyển hướng sang vùng dự phòng us-west-2 chưa
watch -n 5 "dig +short api.dex.dev"

# 3. Nâng cấp Read Replica tại us-west-2 thành Standalone Primary
aws rds promote-read-replica \\
  --db-instance-identifier dex-db-us-west-2-replica
```""",
        "antipatterns": "- **Unannounced Production Drills:** Tự ý cắt mạng vùng chính trên môi trường thật mà không thông báo trước cho các bên liên quan.\n- **Ignoring the Failback Phase:** Diễn tập chuyển đổi sang vùng mới thành công nhưng không có kế hoạch đưa dữ liệu và lưu lượng quay trở lại vùng ban đầu.\n- **Unmeasured Drills:** Diễn tập xong nhưng không đo đạc thời gian RTO hoặc không tính toán lượng bản ghi bị mất mát (RPO).",
        "gates": "- **QG-01**: Có kế hoạch diễn tập và phê duyệt chính thức bằng văn bản từ cấp quản lý.\n- **QG-03**: Thời gian phục hồi RTO thực tế đo được đáp ứng ngưỡng cam kết trong SLA.\n- **QG-10**: Toàn bộ dữ liệu sau khi failover bảo đảm tính toàn vẹn và không bị xung đột khóa.",
        "security": "- Bảo đảm các chứng chỉ SSL/TLS và bí mật cấu hình (Secrets) đã được đồng bộ sẵn sàng tại vùng dự phòng từ trước.\n- Cách ly triệt để vùng bị sập cũ để ngăn ngừa hiện tượng split-brain ghi đè dữ liệu.",
        "adapters": "- **DNS**: AWS Route 53 Application Recovery Controller, Cloudflare Load Balancing.\n- **Databases**: AWS Aurora Global Database failover, PostgreSQL pg_promote.",
        "deliverables": "- Báo cáo kết quả diễn tập thảm họa (Disaster Recovery Drill Report) kèm chỉ số RTO/RPO đo được.\n- Tài liệu cập nhật Disaster Recovery Runbook.\n- Danh sách các điểm cần khắc phục và cải tiến (Action Items).",
        "related": "dex-operational-readiness-review, dex-reliability-engineering, dex-service-failover",
        "usage": """```powershell
# Chạy script tự động đo lường độ trễ sao chép giữa hai vùng trước khi diễn tập
python scripts/measure_replication_lag.py --primary us-east-1 --standby us-west-2
```"""
    },
    {
        "id": "dex-partition-fault-simulation",
        "name": "dex-partition-fault-simulation",
        "desc": "Simulate and verify distributed network partition faults (split-brain scenarios), analyzing CP vs AP tradeoffs, quorum consensus, and self-healing convergence. Use when verifying distributed databases or multi-node consensus algorithms.",
        "purpose": "Mô phỏng và kiểm thử hành vi của hệ thống phân tán khi xảy ra phân mảnh mạng (Network Partition / Split-Brain Fault Simulation); phân tích thực tế các đánh đổi CAP (Consistency vs Availability), kiểm chứng cơ chế đồng thuận đa số (Quorum Consensus) và khả năng tự phục hồi hội tụ dữ liệu sau khi kết nối mạng được nối lại.",
        "when_use": "- Khi phát triển hoặc kiểm thử các hệ thống sử dụng thuật toán đồng thuận phân tán (Raft, Paxos, Zab).\n- Khi cấu hình cụm cơ sở dữ liệu phân tán (Elasticsearch, MongoDB Replica Set, Kafka, Redis Cluster) và cần xác minh cụm không bị chia đôi nhận ghi đồng thời.\n- Khi thiết kế ứng dụng theo hướng Offline-First hoặc Partition-Tolerant.",
        "when_not_use": "- Khi hệ thống chỉ là một máy chủ đơn lẻ hoặc ứng dụng kết nối trực tiếp vào một database tập trung duy nhất.\n- Khi chưa có môi trường staging cách ly an toàn (tuyệt đối không chạy bài test partition mạng trên production khi chưa có chuẩn bị).",
        "prereqs": "- **Ngữ cảnh đầu vào:** Cụm phân tán tối thiểu 3-5 nodes, công cụ tiêm lỗi mạng (Toxiproxy, Chaos Mesh, Pumba, iptables), kịch bản phân tách cụm.\n- **Quyền hạn truy cập:** Quyền thao tác iptables hoặc cấu hình proxy mạng trên môi trường thử nghiệm.",
        "concepts": "- **Network Partition (Split-Brain):** Hiện tượng một cụm $N$ node bị chia cắt thành hai hoặc nhiều phân vùng không thể gửi gói tin mạng cho nhau nhưng các node vẫn đang chạy.\n- **Majority Quorum ($Q > N/2$):** Phân vùng nào nắm giữ đa số phiếu (> 50% số node) mới được quyền bầu chọn Leader và nhận lệnh ghi; phân vùng thiểu số bắt buộc phải từ chối ghi hoặc chuyển sang trạng thái read-only.\n- **State Convergence:** Quá trình các node ở phân vùng thiểu số đồng bộ lại toàn bộ dữ liệu mới nhất từ Leader sau khi mạng được hàn gắn (network healed).",
        "workflow": "1. Khởi động cụm thử nghiệm gồm 5 nodes phân tán (Node A, B, C, D, E) và xác định Leader hiện tại (ví dụ: Node A).\n2. Sử dụng `iptables` hoặc Toxiproxy để chia cắt mạng: Phân vùng 1 gồm {A, B} và Phân vùng 2 gồm {C, D, E}.\n3. Gửi lệnh ghi vào Phân vùng 1 {A, B}: xác nhận lệnh ghi bị từ chối hoặc timeout vì không đủ đa số (chỉ có 2/5 phiếu).\n4. Xác nhận Phân vùng 2 {C, D, E} tự động phát hiện mất liên lạc với Leader A, tiến hành bầu cử mới và chọn ra Leader mới (ví dụ: Node C).\n5. Gửi lệnh ghi vào Leader mới C: xác nhận ghi thành công vì có đủ đa số (3/5 phiếu).\n6. Hàn gắn lại mạng (xóa luật iptables): xác nhận Node A từ bỏ quyền Leader cũ, chấp nhận hạ cấp thành Follower và đồng bộ lại các dữ liệu đã bỏ lỡ từ Node C.",
        "examples": """### Ví dụ tiêm lỗi phân mảnh mạng bằng iptables trên môi trường Linux testing:
```bash
# Giả lập phân tách mạng giữa node-01 (Phân vùng thiểu số) và node-02, node-03
# Tại node-01: Chặn toàn bộ gói tin tới node-02 và node-03
iptables -A INPUT -s 10.0.0.2 -j DROP
iptables -A INPUT -s 10.0.0.3 -j DROP
iptables -A OUTPUT -d 10.0.0.2 -j DROP
iptables -A OUTPUT -d 10.0.0.3 -j DROP

# Kiểm tra xem node-01 có tự hạ cấp hoặc từ chối ghi không
curl -X POST http://localhost:8080/api/write -d '{"val": 42}'
# Kỳ vọng: HTTP 503 Service Unavailable / Quorum Not Reached

# Sau khi kiểm tra xong: Hàn gắn mạng bằng cách xóa các rule iptables
iptables -D INPUT -s 10.0.0.2 -j DROP
iptables -D INPUT -s 10.0.0.3 -j DROP
iptables -D OUTPUT -d 10.0.0.2 -j DROP
iptables -D OUTPUT -d 10.0.0.3 -j DROP
```""",
        "antipatterns": "- **Split-Brain Dual Leader:** Hệ thống bị chia đôi và cả hai bên đều tự nhận mình là Leader rồi nhận ghi dữ liệu, dẫn tới xung đột dữ liệu vĩnh viễn không thể hòa giải.\n- **Even-Numbered Cluster without Arbiter:** Dựng cụm 2 hoặc 4 nodes mà không có node trọng tài (Arbiter), dẫn tới khi chia đôi tỷ lệ là 1:1 hoặc 2:2 và cả hai bên đều không đạt đa số.\n- **Indefinite Hang on Partition:** Client gửi request vào phân vùng bị cô lập và bị treo kết nối vô thời hạn do không cấu hình timeout.",
        "gates": "- **QG-03**: Hệ thống chứng minh khả năng từ chối lệnh ghi tại phân vùng thiểu số khi bị phân mảnh mạng.\n- **QG-09**: Sau khi hàn gắn mạng, 100% các nodes đạt trạng thái đồng thuận và dữ liệu hội tụ nhất quán hoàn toàn.\n- **QG-10**: Quá trình bầu cử Leader mới tại phân vùng đa số hoàn tất trong vòng dưới 5 giây.",
        "security": "- Kiểm tra tính toàn vẹn của các gói tin bầu cử Leader thông qua chữ ký hoặc TLS mutual authentication (mTLS).\n- Đảm bảo các node bị cô lập không tiếp tục cấp phát token hoặc phiên đăng nhập hợp lệ cho client.",
        "adapters": "- **Chaos Tools**: Chaos Mesh, Toxiproxy, Pumba, Jepsen.\n- **Protocols**: Raft (etcd, HashiCorp Serf), Paxos.",
        "deliverables": "- Kịch bản tự động hóa mô phỏng phân mảnh mạng (Chaos Experiment).\n- Báo cáo phân tích hành vi Quorum Consensus và tính nhất quán dữ liệu.\n- Kết quả kiểm chứng tự động hội tụ dữ liệu sau sự cố.",
        "related": "dex-distributed-consistency, dex-clock-skew-resilience, dex-service-failover",
        "usage": """```powershell
# Chạy bài kiểm tra tự động phân mảnh mạng với Toxiproxy
pytest tests/distributed/test_network_partition_chaos.py -v
```"""
    },
    {
        "id": "dex-event-replay-safety",
        "name": "dex-event-replay-safety",
        "desc": "Architect event replay capabilities with deterministic side-effect suppression, idempotency boundaries, and time-travel projection auditing. Use when rebuilding state from event streams or reprocessing historical records.",
        "purpose": "Thiết kế và triển khai cơ chế phát lại sự kiện (Event Replay) an toàn tuyệt đối; cô lập và triệt tiêu có chọn lọc các tác dụng phụ bên ngoài (External Side-Effects như gửi email, trừ tiền thẻ tín dụng, gọi webhook đối tác), bảo đảm quá trình tái tạo trạng thái từ Event Stream có tính xác định (deterministic).",
        "when_use": "- Khi hệ thống kiến trúc Event Sourcing cần tính toán lại toàn bộ dữ liệu trạng thái hiện tại từ đầu lịch sử.\n- Khi phát hiện một bug logic trong projection cũ và cần sửa mã nguồn rồi phát lại 2 năm sự kiện lịch sử để sửa sai dữ liệu.\n- Khi huấn luyện các mô hình Machine Learning hoặc chạy các kịch bản phân tích hồi quy dựa trên luồng sự kiện thực tế trong quá khứ.",
        "when_not_use": "- Khi hệ thống chỉ là CRUD thông thường không lưu trữ nhật ký sự kiện bất biến (Event Log).\n- Khi xử lý luồng sự kiện trực tiếp thời gian thực (Live Stream Processing) nơi mọi tác dụng phụ đều bắt buộc phải kích hoạt.",
        "prereqs": "- **Ngữ cảnh đầu vào:** Kho lưu trữ sự kiện bất biến (Event Store), cờ ngữ cảnh `is_replaying`, giao diện trừu tượng hóa các side-effect dispatchers.\n- **Quyền hạn truy cập:** Quyền đọc stream sự kiện lịch sử và quyền ghi vào bảng dữ liệu mục tiêu.",
        "concepts": "- **Side-Effect Suppression:** Cơ chế chặn đứng các lời gọi tới thế giới bên ngoài (external APIs, email, push notification, payment gateways) trong suốt quá trình phát lại sự kiện lịch sử.\n- **Deterministic Event Handlers:** Hàm xử lý sự kiện chỉ được phép phụ thuộc vào dữ liệu có trong payload của sự kiện và trạng thái hiện tại, tuyệt đối không phụ thuộc vào `Date.now()` hoặc số ngẫu nhiên.\n- **Time-Travel Debugging:** Khả năng dừng và kiểm tra trạng thái chính xác của toàn bộ hệ thống tại một mốc thời gian cụ thể trong quá khứ bằng cách chỉ phát lại sự kiện đến thời điểm đó.",
        "workflow": "1. Bọc toàn bộ các dịch vụ gửi thông tin ra bên ngoài (NotificationService, PaymentGateway, WebhookDispatcher) sau một interface kiểm tra cờ `ReplayContext`.\n2. Khi khởi động tiến trình Replay: bật cờ `is_replaying = true` trong ngữ cảnh thực thi (Execution Context / AsyncLocalStorage).\n3. Định tuyến các side-effects trong chế độ replay vào một NullDispatcher (hoặc ghi log phục vụ kiểm toán mà không thực sự gửi đi).\n4. Bảo đảm các hàm xử lý projection sử dụng `event.timestamp` làm mốc thời gian thay vì gọi hàm lấy giờ hệ thống hiện tại.\n5. Thực hiện phát lại hàng loạt sự kiện lịch sử theo lô (batching) để tối ưu hóa hiệu năng nạp dữ liệu.\n6. Sau khi hoàn tất nạp lịch sử: tắt cờ replay và chuyển consumer sang chế độ lắng nghe sự kiện trực tiếp (Live Mode).",
        "examples": """### Ví dụ kiểm soát triệt tiêu side-effects trong Event Handler bằng TypeScript:
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
```""",
        "antipatterns": "- **Accidental Email Storm:** Phát lại 500,000 sự kiện lịch sử trong đêm và vô tình gửi lại 500,000 email xác nhận đơn hàng cho các khách hàng từ 2 năm trước.\n- **Wall-Clock Time Reliance:** Sử dụng `new Date()` trong logic chiếu dữ liệu khiến giá trị tính toán khi replay khác hoàn toàn so với khi chạy trực tiếp ban đầu.\n- **Direct External Webhook Calls:** Gọi trực tiếp thư viện `axios` hoặc `fetch` bên trong event handler mà không bọc qua interface kiểm soát ngữ cảnh replay.",
        "gates": "- **QG-03**: Quá trình phát lại sự kiện kiểm thử chứng minh 0 cuộc gọi mạng nào được gửi ra ngoài môi trường thử nghiệm.\n- **QG-09**: Trạng thái cuối cùng sau khi Replay khớp bit-for-bit với trạng thái snapshot của hệ thống tại cùng thời điểm.\n- **QG-10**: Hệ thống có khả năng ngắt tiến trình Replay và tiếp tục lại từ checkpoint gần nhất mà không bị trùng lặp.",
        "security": "- Cô lập môi trường replay trong một mạng sandbox riêng biệt không có route ra Internet công cộng.\n- Kiểm soát quyền hạn của tài khoản chạy replay: chỉ cấp quyền đọc trên Event Store và quyền ghi trên bảng projection mới.",
        "adapters": "- **Event Stores**: EventStoreDB, Apache Kafka, AWS Kinesis.\n- **Frameworks**: Axon Framework, Eventuate, custom TypeScript Event Sourcing.",
        "deliverables": "- Interface và cơ chế quản lý Execution Context với cờ `is_replaying`.\n- Bộ Mock/Null Dispatchers cho toàn bộ dịch vụ ngoại vi.\n- Kiểm thử tự động chứng minh không có side-effect rò rỉ trong quá trình Replay.",
        "related": "dex-cqrs-projection-management, dex-idempotent-operations, dex-event-driven-architecture",
        "usage": """```powershell
# Chạy lệnh replay sự kiện với cơ chế triệt tiêu side-effects
python scripts/replay_events.py --stream orders --from 2026-01-01 --suppress-side-effects
```"""
    },
    {
        "id": "dex-consumer-lag-control",
        "name": "dex-consumer-lag-control",
        "desc": "Monitor, analyze, and mitigate streaming consumer lag with adaptive backpressure, partition rebalancing, and lag-driven autoscaling. Use when maintaining sub-second streaming SLAs across Kafka, Pulsar, or Kinesis pipelines.",
        "purpose": "Giám sát, phân tích và kiểm soát độ trễ của Consumer trong các đường ống dữ liệu phân tán (Consumer Lag Control trên Kafka, Pulsar, Kinesis); thiết lập cơ chế điều tiết áp lực ngược (adaptive backpressure), tối ưu hóa tái cân bằng partition (partition rebalancing) và tự động mở rộng quy mô (Autoscaling) dựa trên tốc độ tích lũy backlog.",
        "when_use": "- Khi lưu lượng sự kiện đầu vào tăng đột biến trong các đợt flash sale khiến consumer không xử lý kịp và tạo ra backlog hàng triệu tin nhắn.\n- Khi hệ thống có cam kết thỏa thuận mức dịch vụ (SLA) về độ trễ xử lý dữ liệu tính theo thời gian thực (dưới 500ms).\n- Khi các consumer gặp sự cố 'Stop-The-World' do Rebalance kéo dài làm gián đoạn toàn bộ luồng đọc dữ liệu.",
        "when_not_use": "- Khi ứng dụng chỉ xử lý các hàng đợi batch đơn giản không đòi hỏi ràng buộc về thời gian thực.\n- Khi hệ thống chỉ có một partition duy nhất và không thể mở rộng quy mô đọc song song.",
        "prereqs": "- **Ngữ cảnh đầu vào:** Broker streaming (Kafka, Pulsar), công cụ đo lag (Burrow, Kafka Exporter), hệ thống tự động co giãn pods (KEDA / HPA trên Kubernetes).\n- **Quyền hạn truy cập:** Quyền theo dõi consumer group offsets và cấu hình HPA trên Kubernetes cluster.",
        "concepts": "- **Consumer Lag:** Khoảng cách giữa offset của thông điệp mới nhất được ghi vào partition (Log End Offset) và offset của thông điệp gần nhất mà Consumer Group đã commit (Current Offset).\n- **Cooperative Sticky Rebalance:** Cơ chế tái phân bổ partition mới của Kafka giúp tránh hiện tượng dừng toàn bộ các consumers (Stop-the-world) trong khi rebalance.\n- **Lag-Driven Scaling:** Tự động tăng số lượng consumer replicas dựa trên tổng lượng lag hoặc tốc độ tăng trưởng của backlog (sử dụng Kubernetes KEDA).",
        "workflow": "1. Xuất các chỉ số độ trễ chi tiết theo từng partition: `kafka_consumergroup_lag` và `kafka_consumergroup_lag_seconds` vào Prometheus.\n2. Cấu hình consumer sử dụng giao thức `CooperativeStickyAssignor` để loại bỏ thời gian chết do rebalancing.\n3. Thiết lập cơ chế xử lý theo batch và song song hóa xử lý bên trong consumer bằng worker thread pool trước khi commit offset.\n4. Cài đặt KEDA ScaledObject trên Kubernetes tự động tăng số lượng consumer pods tương ứng khi lag vượt ngưỡng 10,000 messages.\n5. Tích hợp cơ chế Backpressure: khi downstream database bị nghẽn, consumer tự động giảm tần suất poll hoặc tạm dừng nhận tin (`pause()`) để bảo vệ database.",
        "examples": """### Ví dụ cấu hình Kubernetes KEDA ScaledObject tự động co giãn theo Kafka Lag:
```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: order-consumer-scaler
  namespace: streaming
spec:
  scaleTargetRef:
    name: order-processing-consumer
  minReplicaCount: 2
  maxReplicaCount: 16 # Bằng tổng số partitions của Kafka topic
  pollingInterval: 15
  cooldownPeriod: 300
  triggers:
    - type: kafka
      metadata:
        bootstrapServers: kafka-cluster.internal:9092
        consumerGroup: order-consumer-group
        topic: orders.v1
        lagThreshold: "2500" # Tăng 1 pod cho mỗi 2500 messages tồn đọng
        activationLagThreshold: "50"
```""",
        "antipatterns": "- **Scaling Beyond Partition Count:** Tăng số lượng consumer pods nhiều hơn số lượng partition của topic, khiến các pods dư thừa bị rảnh rỗi 100% không nhận được partition nào.\n- **Synchronous Heavy I/O in Poll Loop:** Thực hiện các cuộc gọi API chậm chạp bên trong luồng `poll()`, khiến consumer bị broker coi là đã chết (vượt quá `max.poll.interval.ms`) và kích hoạt rebalance liên tục.\n- **Blind Commit Without Processing:** Tự động commit offset ngay khi vừa đọc được tin nhắn trước khi xử lý xong, dẫn tới mất dữ liệu hoàn toàn khi consumer bị sập.",
        "gates": "- **QG-03**: Thời gian phục hồi độ trễ (drain backlog) sau đợt tăng tải đột biến được chứng minh bằng kiểm thử tải thực tế.\n- **QG-07**: Độ trễ trung bình của consumer duy trì dưới 500ms trong điều kiện tải bình thường.\n- **QG-10**: Khi một consumer node bị crash, các partition còn lại được phân bổ lại trong dưới 3 giây mà không làm gián đoạn các nodes khác.",
        "security": "- Sử dụng chứng thực mTLS và SASL/SCRAM để bảo vệ kết nối giữa Consumer và Kafka Broker.\n- Phân quyền ACL tối thiểu chỉ cho phép consumer group đọc dữ liệu trên đúng topic được chỉ định.",
        "adapters": "- **Streaming**: Apache Kafka, Apache Pulsar, AWS Kinesis.\n- **Orchestration**: Kubernetes KEDA (Kubernetes Event-driven Autoscaling), Prometheus.",
        "deliverables": "- Cấu hình tối ưu hóa Consumer Group và cơ chế Cooperative Rebalance.\n- Tệp cấu hình KEDA ScaledObject tự động co giãn theo độ trễ.\n- Dashboard Grafana giám sát Consumer Lag theo từng partition.",
        "related": "dex-traffic-shaping-backpressure, dex-load-and-stress-testing, dex-stream-processing-semantics",
        "usage": """```powershell
# Kiểm tra độ trễ consumer lag hiện tại trên Kafka cluster
kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group order-consumer-group
```"""
    },
    {
        "id": "dex-hot-partition-mitigation",
        "name": "dex-hot-partition-mitigation",
        "desc": "Detect and mitigate hot partition key skew using synthetic salting, compound keys, and adaptive sharding. Use when streaming or storage partitions suffer from severe resource saturation due to skewed data distributions.",
        "purpose": "Phát hiện và giảm thiểu hiện tượng lệch tải phân vùng (Hot Partition / Key Skew) trong hệ thống lưu trữ và streaming phân tán; áp dụng kỹ thuật gieo muối nhân tạo (synthetic salting), khóa phân vùng kết hợp (compound partition keys), và phân mảnh thích ứng nhằm phân bổ tải đều lên toàn bộ các máy chủ trong cụm.",
        "when_use": "- Khi một partition đơn lẻ trong Kafka topic hoặc DynamoDB/Cassandra table bị quá tải CPU/IOPS trong khi các partition khác hầu như nhàn rỗi.\n- Khi hệ thống có các đối tượng 'người nổi tiếng' (Celebrity problem / High-cardinality skew) như tài khoản có hàng triệu followers hoặc sản phẩm flash sale tạo ra 80% lưu lượng ghi.\n- Khi xảy ra hiện tượng throttling hoặc tăng độ trễ p99 do nghẽn tại một điểm đơn lẻ trong cụm lưu trữ phân tán.",
        "when_not_use": "- Khi dữ liệu được phân bố đồng đều tự nhiên (ví dụ: sử dụng UUIDv4 ngẫu nhiên làm partition key).\n- Khi bắt buộc phải bảo đảm thứ tự tuần tự tuyệt đối (Strict Global Ordering) cho toàn bộ các sự kiện của hệ thống.",
        "prereqs": "- **Ngữ cảnh đầu vào:** Khóa phân vùng hiện tại (Partition Key), phân tích phân bố tần suất của khóa (Key Distribution Histogram), broker/database metrics theo từng partition.\n- **Quyền hạn truy cập:** Quyền thay đổi logic sinh khóa phân vùng tại Producer và logic tổng hợp tại Consumer.",
        "concepts": "- **Hot Partition Skew:** Tình trạng mất cân bằng nghiêm trọng khi một partition phải tiếp nhận lượng dữ liệu lớn gấp nhiều lần mức trung bình do cùng một partition key.\n- **Key Salting (Gieo muối):** Bổ sung một hậu tố ngẫu nhiên hoặc có chu kỳ (ví dụ: `account_id + '_' + random(1, 10)`) vào khóa phân vùng để phân tán dữ liệu sang 10 partitions khác nhau.\n- **Scatter-Gather Read Pattern:** Khi truy vấn dữ liệu đã được gieo muối, tầng đọc sẽ phát lệnh đọc song song tới tất cả 10 partitions và hợp nhất kết quả lại.",
        "workflow": "1. Đo lường phân bố lưu lượng theo từng partition trên Broker hoặc Cơ sở dữ liệu phân tán để xác định mức độ lệch tải (Gini coefficient hoặc Max/Avg ratio).\n2. Nhận diện các khóa phân vùng có tần suất xuất hiện vượt quá 5% tổng lưu lượng ghi của hệ thống.\n3. Triển khai thuật toán Dynamic Salting tại Producer: chỉ áp dụng gieo muối cho các khóa nằm trong danh sách 'hot keys', các khóa bình thường giữ nguyên.\n4. Cải tiến Consumer / Query Engine theo mẫu Scatter-Gather: đọc song song từ các partitions con và tổng hợp lại kết quả.\n5. Kiểm tra phân bố lại tải trên dashboard: bảo đảm độ lệch giữa partition cao nhất và trung bình không vượt quá 20%.\n6. Tự động điều chỉnh số lượng muối (salt factor) dựa trên lưu lượng thực tế đo được.",
        "examples": """### Ví dụ kỹ thuật Dynamic Key Salting trong Python Producer:
```python
import hashlib
import random

HOT_TENANTS = {"tenant_celebrity_01", "tenant_megacorp_99"}
SALT_BUCKETS = 8

def compute_partition_key(tenant_id: str, record_id: str) -> str:
    # 1. Nếu là tenant bình thường -> Dùng nguyên tenant_id để bảo toàn thứ tự cục bộ
    if tenant_id not in HOT_TENANTS:
        return tenant_id

    # 2. Nếu là Hot Tenant -> Gieo muối ngẫu nhiên (hoặc dựa trên hash của record_id)
    # để phân tán đều ra 8 partitions khác nhau, tránh nghẽn 1 partition đơn lẻ
    salt = random.randint(0, SALT_BUCKETS - 1)
    return f"{tenant_id}_salt_{salt}"

def scatter_gather_read_keys(tenant_id: str) -> list[str]:
    # Khi cần đọc toàn bộ dữ liệu của Hot Tenant: Đọc từ tất cả các buckets đã gieo muối
    if tenant_id not in HOT_TENANTS:
        return [tenant_id]
    return [f"{tenant_id}_salt_{i}" for i in range(SALT_BUCKETS)]
```""",
        "antipatterns": "- **Universal Over-Salting:** Gieo muối cho toàn bộ 100% các keys kể cả các keys lưu lượng nhỏ, làm tăng độ phức tạp và chi phí truy vấn đọc không cần thiết.\n- **Loss of Ordering Guarantee:** Áp dụng gieo muối mà không tính đến việc các sự kiện phụ thuộc lẫn nhau của cùng một đơn hàng bị phân tán sang các partitions khác nhau làm mất thứ tự xử lý.\n- **Static Salt Values:** Sử dụng số lượng muối cố định không thể thay đổi khi lượng truy cập của sự kiện tăng gấp 100 lần trong thực tế.",
        "gates": "- **QG-03**: Dashboard đo lường chứng minh độ chênh lệch tải giữa partition lớn nhất và nhỏ nhất giảm tối thiểu 60% sau khi áp dụng salting.\n- **QG-07**: Tăng tải ghi lên 50,000 req/s mà không có partition nào bị kích hoạt cảnh báo throttling.\n- **QG-09**: Logic truy vấn Scatter-Gather bảo đảm không bỏ sót bất kỳ bản ghi nào đã được ghi vào các partition muối.",
        "security": "- Sử dụng hàm băm an toàn và bộ sinh số ngẫu nhiên đáng tin cậy để tạo muối, tránh việc muối bị dự đoán trước trong các tấn công DoS nhằm vào một partition cụ thể.\n- Phân quyền đồng nhất cho các partition con của cùng một dữ liệu khách hàng.",
        "adapters": "- **Storage**: DynamoDB Partition Keys, Cassandra Row Keys, Bigtable Row Keys.\n- **Streaming**: Kafka Murmur2 Partitioner, Kinesis Hash Keys.",
        "deliverables": "- Module Producer hỗ trợ Dynamic Key Salting.\n- Logic Scatter-Gather Query Resolver cho tầng đọc.\n- Biểu đồ phân tích độ lệch tải (Skewness Distribution Chart) trước và sau khi tối ưu.",
        "related": "dex-consumer-lag-control, dex-database-query-plans, dex-load-and-stress-testing",
        "usage": """```powershell
# Chạy phân tích độ lệch phân vùng của Kafka topic
python scripts/analyze_partition_skew.py --topic user_actions --window 1h
```"""
    },
    {
        "id": "dex-clock-skew-resilience",
        "name": "dex-clock-skew-resilience",
        "desc": "Engineer distributed systems resilient to physical clock skew, leap seconds, and NTP drift using monotonic clocks, logical Lamport timestamps, and bounded lease timeouts. Use when ordering events across independent server nodes.",
        "purpose": "Thiết kế hệ thống phân tán có khả năng kháng cự trước sai lệch đồng hồ vật lý (Physical Clock Skew, NTP Drift, Leap Seconds); loại bỏ sự phụ thuộc nguy hiểm vào đồng hồ thực tế (Wall-Clock Time), ứng dụng đồng hồ đơn điệu (Monotonic Clocks), thời gian logic (Logical Lamport Timestamps / Vector Clocks), và khoảng dung sai thời gian an toàn.",
        "when_use": "- Khi sắp xếp thứ tự các sự kiện phát sinh từ nhiều máy chủ độc lập không có đồng hồ đồng bộ tuyệt đối.\n- Khi triển khai thuật toán phát hiện xung đột dữ liệu (Last-Write-Wins / Conflict-Free Replicated Data Types - CRDTs).\n- Khi thiết lập thời hạn hết hạn token, session hoặc lease khóa phân tán trên môi trường máy chủ đám mây ảo hóa.",
        "when_not_use": "- Khi chỉ hiển thị ngày giờ thân thiện cho người dùng trên giao diện frontend.\n- Khi hệ thống vận hành trên hạ tầng phần cứng chuyên dụng có đồng hồ nguyên tử và GPS hỗ trợ TrueTime API (như Google Cloud Spanner).",
        "prereqs": "- **Ngữ cảnh đầu vào:** Sai số NTP đo được giữa các nodes trong cluster, cơ chế sinh timestamp hiện tại, yêu cầu về thứ tự sự kiện (Causal Ordering vs Total Ordering).\n- **Quyền hạn truy cập:** Quyền kiểm tra cấu hình NTP daemon (`chrony` hoặc `ntpd`) trên máy chủ.",
        "concepts": "- **Wall-Clock vs Monotonic Clock:** Đồng hồ thực tế (ví dụ: `time.time()` trong Python) có thể bị nhảy lùi lại khi NTP đồng bộ; đồng hồ đơn điệu (ví dụ: `time.monotonic()`) luôn chỉ tăng và không bao giờ lùi.\n- **Lamport Logical Timestamp:** Mỗi tiến trình duy trì một số nguyên đơn giản; khi gửi tin đính kèm counter, khi nhận tin cập nhật counter = $\\max(\\text{local}, \\text{received}) + 1$.\n- **Clock Uncertainty Window ($\\epsilon$):** Khoảng thời gian không chắc chắn $[\text{timestamp} - \\epsilon, \text{timestamp} + \\epsilon]$ cần được tính đến khi thiết lập các thời hạn an toàn.",
        "workflow": "1. Rà soát toàn bộ mã nguồn: thay thế tất cả các phép đo khoảng thời gian (duration) từ đồng hồ thực sang đồng hồ đơn điệu (`time.monotonic()` hoặc `System.nanoTime()`).\n2. Thay thế cơ chế so sánh thứ tự sự kiện dựa trên wall-clock bằng Lamport Timestamp hoặc Vector Clocks cho các luồng nghiệp vụ yêu cầu quan hệ nhân quả (Causal Consistency).\n3. Trong các giao dịch khóa phân tán: cộng thêm khoảng dung sai sai lệch tối đa ($\\Delta_{\\text{clock}}$ ví dụ: 200ms) vào thời gian giữ khóa để bảo đảm khóa cũ đã hết hạn ở mọi node trước khi cấp khóa mới.\n4. Giám sát độ lệch NTP giữa các nodes trong cluster qua Prometheus node_exporter và cảnh báo khi offset vượt quá 50ms.\n5. Kiểm thử hệ thống trong kịch bản giả lập đồng hồ máy chủ bị chỉnh lùi hoặc tiến 5 giây để chứng minh không xảy ra deadlock hoặc hỏng dữ liệu.",
        "examples": """### Ví dụ bộ đếm Lamport Timestamp bảo đảm thứ tự nhân quả trong TypeScript:
```typescript
export class LamportClock {
  private counter: number = 0;

  // Lấy thời gian logic để gửi kèm thông điệp đi
  tick(): number {
    this.counter += 1;
    return this.counter;
  }

  // Cập nhật thời gian logic khi nhận được thông điệp từ node khác
  witness(receivedTimestamp: number): number {
    this.counter = Math.max(this.counter, receivedTimestamp) + 1;
    return this.counter;
  }

  getValue(): number {
    return this.counter;
  }
}

// Khi áp dụng: Sự kiện có Lamport Timestamp lớn hơn được bảo đảm xảy ra sau
// mà hoàn toàn không phụ thuộc vào đồng hồ giờ máy tính của hai bên!
```""",
        "antipatterns": "- **Measuring Durations with Date.now():** Đo thời gian thực thi bằng cách lấy `Date.now() - startTime`, dẫn tới kết quả bị âm khi NTP đồng bộ lùi giờ.\n- **Blind Last-Write-Wins (LWW):** Giải quyết xung đột dữ liệu bằng cách so sánh `created_at` từ đồng hồ máy tính của hai server khác nhau, khiến server chạy nhanh hơn luôn ghi đè dữ liệu của server chạy chậm hơn.\n- **Leap Second Ignorance:** Không cấu hình NTP Slewing (chrony) khiến bước nhảy 1 giây nhuận (Leap Second) làm sập các ứng dụng cơ sở dữ liệu phân tán.",
        "gates": "- **QG-05**: 100% các phép đo khoảng thời gian trong mã nguồn sử dụng Monotonic Clock.\n- **QG-09**: Xung đột dữ liệu được giải quyết chính xác bằng Lamport/Vector Clocks hoặc CRDTs trong bài test mô phỏng đồng hồ lệch 10 giây.\n- **QG-10**: Cảnh báo NTP drift được kích hoạt ngay lập tức khi độ lệch đồng hồ giữa 2 nodes bất kỳ vượt quá 50ms.",
        "security": "- Bắt buộc sử dụng giao thức NTP an toàn (NTS - Network Time Security) để chống lại các cuộc tấn công giả mạo thời gian (Time Shifting Attack) nhằm làm hết hạn sớm chứng chỉ SSL hoặc token bảo mật.\n- Kiểm soát cấu hình tường lửa chỉ cho phép đồng bộ thời gian từ các NTP servers uy tín.",
        "adapters": "- **System**: `chrony`, `ntpd`, `node_exporter` (metric `node_timex_offset_seconds`).\n- **Libraries**: HLC (Hybrid Logical Clocks), Google TrueTime API.",
        "deliverables": "- Module thư viện Lamport Timestamp và Monotonic Timer.\n- Quy tắc cấu hình chrony slewing chuẩn hóa cho cụm máy chủ.\n- Bộ kiểm thử tự động kiểm tra khả năng kháng sai lệch đồng hồ (Clock Skew Chaos Test).",
        "related": "dex-distributed-lock-lease-safety, dex-distributed-consistency, dex-scheduler-misfire-recovery",
        "usage": """```powershell
# Chạy bộ kiểm thử kiểm tra tính ổn định của hệ thống khi đồng hồ bị lệch
pytest tests/distributed/test_clock_skew_resilience.py -v
```"""
    }
]

def generate_skills():
    print(f"=== GENERATING GROUP AE & AF (Skills 301–320) ===")
    total = len(SKILLS_AE_AF)
    created = 0

    for idx, skill in enumerate(SKILLS_AE_AF, 1):
        skill_id = skill["id"]
        skill_dir = os.path.join(SKILLS_DIR, skill_id)
        os.makedirs(skill_dir, exist_ok=True)
        file_path = os.path.join(skill_dir, "SKILL.md")

        content = f"""---
name: {skill["name"]}
description: {skill["desc"]}
---

# {skill["id"]}

## 1. Purpose & Scope
{skill["purpose"]}

## 2. When to Use
{skill["when_use"]}

## 3. When NOT to Use
{skill["when_not_use"]}

## 4. Prerequisites & Input Context
{skill["prereqs"]}

## 5. Core Concepts & Taxonomy
{skill["concepts"]}

## 6. Step-by-Step Execution Workflow
{skill["workflow"]}

## 7. Concrete Examples
{skill["examples"]}

## 8. Anti-Patterns & Common Traps
{skill["antipatterns"]}

## 9. Verification Quality Gates
{skill["gates"]}

## 10. Security & Risk Mitigation
{skill["security"]}

## 11. Platform Adapters & Extensibility
{skill["adapters"]}

## 12. Expected Deliverables
{skill["deliverables"]}

## 13. Related Skills & Synergy
{skill["related"]}

## 14. Realistic Usage Scenario & Verification Commands
{skill["usage"]}
"""
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        created += 1
        print(f"[{idx:02d}/{total:02d}] Created: {skill_id}")

    print(f"\nSuccessfully generated {created}/{total} skills for Groups AE & AF.")

if __name__ == "__main__":
    generate_skills()
