---
name: dex-domain-driven-design
description: Implement Domain-Driven Design (DDD) tactical patterns: Entities, Value Objects, Aggregates, Domain Events, Repositories, and Clean Architecture boundaries. Use when modeling complex business domains, refactoring bloated services, or isolating business logic from infrastructure.
---

# dex-domain-driven-design

## 1. Purpose & Scope
Thiết kế và triển khai mã nguồn theo phương pháp Thiết kế Hướng Miền (Domain-Driven Design - DDD) với các mẫu hình chiến thuật (Tactical Patterns); phân tách rạch ròi giữa Thực thể (Entities), Đối tượng Giá trị (Value Objects), Cụm Tổng hợp (Aggregates), Sự kiện Miền (Domain Events) và Kho Lưu trữ (Repositories), giữ cho logic nghiệp vụ hoàn toàn trong sáng và độc lập với cơ sở dữ liệu hay framework.

## 2. When to Use
- Khi logic nghiệp vụ của ứng dụng trở nên phức tạp, nhiều quy tắc ràng buộc chằng chịt trong các file Service khổng lồ.
- Khi các quy tắc toàn vẹn nghiệp vụ bị vi phạm do dữ liệu bị cập nhật phân tán từ nhiều nơi.
- Khi cần xây dựng một hệ thống phần mềm có tuổi thọ cao, dễ bảo trì và dễ dàng thay thế cơ sở dữ liệu hoặc framework bên ngoài.

## 3. When NOT to Use
- Ứng dụng CRUD đơn giản chỉ làm nhiệm vụ đọc ghi bảng cơ sở dữ liệu mà không có logic nghiệp vụ phức tạp.
- Các script tự động hóa hoặc công cụ CLI nhỏ.

## 4. Prerequisites & Input Context
**Đầu vào cần thiết:**
- Tài liệu phân tích nghiệp vụ từ Domain Experts (Ubiquitous Language).
- Danh sách các thực thể cốt lõi, quy tắc bất biến (Invariants) và ranh giới nghiệp vụ (Bounded Contexts).

**Điều kiện tiên quyết:**
- Đội ngũ kỹ thuật đã thống nhất ngôn ngữ nghiệp vụ chung (Ubiquitous Language).
- Kiến trúc dự án tuân theo mô hình Hexagonal, Onion hoặc Clean Architecture.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**: Nắm vững cơ chế vận hành theo chuẩn Agent Skills, tuân thủ nghiêm ngặt tính xác định và ranh giới trách nhiệm.
- **Quy tắc quyết định kỹ thuật**:
- **Aggregate Root Là Điểm Truy Cập Duy Nhất**: Các thành phần bên ngoài chỉ được phép gọi vào Aggregate Root; cấm truy cập trực tiếp vào các thực thể con bên trong Aggregate.
- **Domain Trong Sáng Tuyệt Đối**: Tầng Domain không được import bất kỳ thư viện ORM nào (Prisma, TypeORM, Mongoose); chỉ dùng pure TypeScript/Python/Go.
- **Giao Dịch Trong Một Aggregate**: Một giao dịch (Transaction) chỉ nên sửa đổi trạng thái của DUY NHẤT một Aggregate; sự đồng bộ giữa các Aggregate khác nhau phải xử lý qua Domain Events và tính nhất quán sau cùng (Eventual Consistency).
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Dữ liệu bị sửa đổi không hợp lệ**: Do controller tự gọi DB update cột tiền mà không qua hàm `deposit()` của Aggregate -> Khắc phục: Đóng gói các thuộc tính ở dạng private và chỉ cung cấp các phương thức nghiệp vụ.
- **Aggregate quá lớn gây nghẽn hiệu năng**: Cố nhét toàn bộ lịch sử 10,000 đơn hàng vào một User Aggregate -> Khắc phục: Tách Order thành Aggregate độc lập có tham chiếu `userId`.

## 6. Step-by-Step Execution Workflow
1. Xây dựng Value Objects cho các giá trị có quy tắc validation riêng (ví dụ: `Email`, `Money`, `OrderId`) với tính chất bất biến (Immutable).
2. Xây dựng Entities có định danh duy nhất (Identity) và vòng đời độc lập.
3. Nhóm các Entities và Value Objects liên quan chặt chẽ thành một Aggregate; chỉ định một Aggregate Root làm đầu mối truy cập duy nhất.
4. Đảm bảo mọi thay đổi trạng thái bên trong Aggregate đều bảo toàn quy tắc bất biến (Enforce Invariants).
5. Phát ra Sự kiện Miền (Domain Events) khi trạng thái thay đổi quan trọng (ví dụ: `OrderPlacedEvent`).
6. Định nghĩa Repository Interface ở tầng Domain và chỉ triển khai chi tiết kết nối SQL/NoSQL ở tầng Infrastructure.

## 7. Concrete Examples
### Ví dụ triển khai chuẩn mực:
```typescript
// domain/Money.ts (Value Object bất biến)
export class Money {
  constructor(public readonly amount: number, public readonly currency: 'VND' | 'USD') {
    if (amount < 0) throw new Error('Số tiền không được âm');
  }
  add(other: Money): Money {
    if (this.currency !== other.currency) throw new Error('Không thể cộng khác loại tiền');
    return new Money(this.amount + other.amount, this.currency);
  }
}
```

### Lệnh xác minh & thực thi:
- Chạy unit test tầng Domain (không cần mock DB, tốc độ siêu nhanh): `npm test -- src/domain/`
- Kiểm tra tính phụ thuộc sạch (Domain không import Infra): `npx dependency-cruiser --validate .dependency-cruiser.js src/`

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước kiểm tra biên và giả định hệ thống luôn ở trạng thái lý tưởng.
- **Anti-Pattern 2**: Không ghi nhận nhật ký kiểm toán hoặc bỏ qua việc xử lý ngoại lệ lúc runtime.
- **Trap**: Bỏ qua các rào chắn an toàn hoặc cố tình chạy script không qua kiểm thử tự động.

## 9. Quality Gates & Acceptance Criteria
- QG-01: 100% logic nghiệp vụ cốt lõi nằm ở tầng Domain, không nằm trong Controller hay Repository.
- QG-05: Unit test cho Aggregate và Value Objects đạt độ bao phủ nhánh (Branch Coverage) >= 95%.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động trước khi coi là hoàn thành.

## 10. Security & Safety Boundaries
- Tất cả các giá trị đầu vào đều được đóng gói và validate ngay tại thời điểm tạo Value Object, ngăn chặn dữ liệu độc hại đi sâu vào lõi hệ thống.
- Không bao giờ thực thi mã nguồn hoặc thay đổi cấu hình trên môi trường sản xuất mà thiếu cơ chế rollback an toàn.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Có thể kích hoạt trực tiếp từ terminal hoặc extension tương thích trong VS Code / Cursor / Windsurf.

## 12. Deliverables & Output Artifacts
- Các file Domain Models (`Order.ts`, `Money.ts`, `OrderStatus.ts`).
- Repository Interface (`OrderRepository.interface.ts`).
- File Domain Events (`OrderPlaced.event.ts`).

## 13. Related & Complementary Skills
- `dex-development-workflow`: Quy trình phát triển tiêu chuẩn.
- `dex-code-verification`: Xác minh chất lượng và tính đúng đắn của mã nguồn.
- `dex-master-orchestrator`: Bộ điều phối trung tâm kết nối kỹ năng này với các kỹ năng khác trong hệ thống.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư hoặc AI Agent tiếp nhận yêu cầu liên quan đến **dex-domain-driven-design**.
1. Đọc kỹ đầu vào và các ràng buộc kỹ thuật tại mục 4.
2. Thực thi tuần tự 6 bước trong Workflow tại mục 6.
3. Chạy các lệnh kiểm chứng tại mục 7 và đối chiếu với Quality Gates tại mục 9.
4. Đóng gói deliverables theo danh sách tại mục 12 và báo cáo kết quả kèm bằng chứng xác thực.
