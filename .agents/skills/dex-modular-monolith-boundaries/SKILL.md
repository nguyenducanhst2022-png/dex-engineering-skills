---
name: dex-modular-monolith-boundaries
description: Enforce strict domain boundaries, module isolation, and dependency rules within a modular monolith architecture. Use when restructuring legacy monoliths, preventing package entanglement, or maintaining high maintainability without microservice overhead.
---

# dex-modular-monolith-boundaries

## 1. Purpose & Scope
Thiết kế và thực thi ranh giới module nghiêm ngặt trong kiến trúc Modular Monolith; ngăn chặn sự phụ thuộc chéo bất hợp lệ giữa các domain, phân tách rõ ràng Public API và Internal Implementation của từng module mà không phải chịu chi phí vận hành phân tán của microservices.

## 2. When to Use
- Khi tái cấu trúc ứng dụng nguyên khối lớn (monolith) bị rối rắm mã nguồn (spaghetti code).
- Khi muốn có tính độc lập cao giữa các domain nghiệp vụ nhưng vẫn triển khai trên cùng một artifact runtime duy nhất.
- Khi chuẩn bị lộ trình tách service trong tương lai một cách an toàn và có kiểm soát.

## 3. When NOT to Use
- Khi ứng dụng quy mô siêu nhỏ (micro-tool hoặc prototype) chỉ có 1-2 nghiệp vụ cơ bản.
- Khi hệ thống đã được phân tách thành các microservices hoàn toàn độc lập về hạ tầng.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Bản đồ domain nghiệp vụ (Bounded Contexts), cấu trúc thư mục module, công cụ kiểm tra ranh giới (ArchUnit, dependency-cruiser).
- **Quyền hạn truy cập:** Quyền sửa đổi cấu hình kiến trúc và build toolchain của dự án.

## 5. Core Concepts & Taxonomy
- **Module Encapsulation:** Mỗi module chỉ công khai `public-api` (interfaces, DTOs, events); toàn bộ implementation, entities, repositories nằm trong `internal`.
- **Acyclic Dependency Rule:** Đồ thị phụ thuộc giữa các module phải là Directed Acyclic Graph (DAG), cấm tuyệt đối circular dependency.
- **In-Memory Event Bus:** Giao tiếp bất đồng bộ giữa các module thông qua in-memory domain events thay vì gọi trực tiếp database của module khác.

## 6. Step-by-Step Execution Workflow
1. Định nghĩa ranh giới các bounded context theo nguyên lý Domain-Driven Design (ví dụ: `billing`, `inventory`, `identity`).
2. Cấu trúc mỗi module với hai thư mục con riêng biệt: `api/` và `internal/`.
3. Thiết lập bộ quy tắc kiểm tra phụ thuộc tự động trong CI (sử dụng ArchUnit cho Java/Kotlin, dependency-cruiser cho TypeScript, hoặc import-linter cho Python).
4. Thay thế việc truy vấn trực tiếp bảng dữ liệu của module khác bằng cách gọi API module hoặc đăng ký lắng nghe Domain Event.
5. Chạy kiểm thử kiến trúc để xác nhận 0 vi phạm ranh giới module trước khi merge.

## 7. Concrete Examples
### Ví dụ cấu hình quy tắc phụ thuộc module trong dependency-cruiser (`.dependency-cruiser.js`):
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
```

## 8. Anti-Patterns & Common Traps
- **Direct Foreign DB Querying:** Module Order truy vấn trực tiếp bảng của Module Customer bằng SQL JOIN xuyên schema.
- **God Shared Module:** Nhét toàn bộ logic nghiệp vụ dùng chung vào thư mục `shared/` hoặc `common/` làm mất ranh giới domain.
- **Leaky Internals:** Export trực tiếp Entity ORM (Hibernate, Prisma, TypeORM) qua public interface.

## 9. Quality Gates & Acceptance Criteria
- **QG-02**: Kiến trúc module tuân thủ 100% cấu trúc `api/` và `internal/`.
- **QG-05**: Bộ linter kiến trúc chạy đạt exit code 0, không có circular dependency.
- **QG-09**: Tất cả các giao tiếp liên module đều đi qua interface hoặc domain event.

## 10. Security & Safety Boundaries
- Phân quyền truy cập tài nguyên module dựa trên context security principal được truyền qua API boundary.
- Bảo đảm module dữ liệu nhạy cảm (thanh toán, PII) không bị truy cập trái phép từ các module nghiệp vụ thông thường.

## 11. Platform Adapters
- **TypeScript/Node**: dependency-cruiser, nx boundaries.
- **Java/Kotlin**: ArchUnit JUnit tests.
- **Python**: import-linter, tach.

## 12. Deliverables & Output Artifacts
- Tệp cấu hình quy tắc ranh giới kiến trúc.
- Báo cáo kết quả kiểm tra dependency graph không chu trình.
- Mã nguồn tuân thủ nghiêm ngặt chuẩn `api/` và `internal/`.

## 13. Related & Complementary Skills
dex-software-architecture, dex-code-organization, dex-architecture-decision-records

## 14. Realistic Usage Example
```powershell
# Kiểm tra vi phạm ranh giới giữa các module trong dự án
npx depcruise --config .dependency-cruiser.js src/modules

# Chạy kiến trúc test suite
pytest tests/architecture/test_module_boundaries.py -v
```
