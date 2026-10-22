---
name: dex-software-architecture
description: Software architectural design, component decomposition, modular boundary definition, and architectural decision records (ADRs). Designs scalable, maintainable architectures following KISS and YAGNI principles. Use when architecting systems, scaffolding projects, evaluating scalability, or recording ADRs.
---

# DEX Software Architecture

## 1. Purpose
Thiết kế kiến trúc hệ thống phần mềm đơn giản, mô đun hóa cao, dễ bảo trì và có khả năng mở rộng linh hoạt theo thời gian, tuân thủ nghiêm ngặt các nguyên lý kỹ thuật đã được kiểm chứng (KISS, YAGNI, Separation of Concerns).

Quy trình thiết kế chuẩn:
`Phân tích yêu cầu → Thiết kế kiến trúc → Chia Module → Xác định luồng dữ liệu → Triển khai → Kiểm thử → Đánh giá khả năng mở rộng → Ổn định → Lưu Git`

Nguyên tắc cốt lõi: **Thiết kế hệ thống đơn giản, dễ bảo trì và có khả năng mở rộng khi cần. Tuyệt đối không làm kiến trúc phức tạp quá mức cần thiết.**
Ghi nhớ sống còn: **Kiến trúc tốt = Đơn giản + Module độc lập + Dễ bảo trì + Dễ mở rộng + Có kiểm chứng.**

## 2. When to Use
- Khi bắt đầu khởi tạo dự án mới từ ý tưởng ban đầu (Greenfield Architecture).
- Khi mở rộng hệ thống hiện có để đáp ứng quy mô người dùng hoặc khối lượng dữ liệu tăng cao.
- Khi cần quyết định lựa chọn công nghệ lõi, cơ sở dữ liệu, mô hình giao tiếp (REST, GraphQL, gRPC, Event-driven).
- Khi ghi nhận các quyết định kiến trúc quan trọng thông qua Architecture Decision Record (ADR).

## 3. When Not to Use
- Sửa đổi các hàm cục bộ hoặc giải quyết các lỗi logic nhỏ không làm thay đổi ranh giới hệ thống.
- Khi áp đặt các kiến trúc phân tán phức tạp (như microservices) cho các ứng dụng nhỏ hoặc MVP chỉ cần Monolith sạch sẽ.

## 4. Inputs
- Yêu cầu chức năng (Functional Requirements) và Yêu cầu phi chức năng (Non-Functional Requirements: SLA, tải dự kiến, tính khả dụng).
- Các ràng buộc về hạ tầng, ngân sách và công nghệ sẵn có.
- Mẫu tài liệu ghi nhận quyết định kiến trúc tại [architecture-decision-record.md](references/architecture-decision-record.md).

## 5. Workflow

### Bước 1: Phân Tích Yêu Cầu & Ranh Giới Nghiệp Vụ (Domain Boundaries)
- Xác định các thực thể chính và các miền nghiệp vụ (Bounded Contexts).
- Tách biệt rõ ràng giữa logic nghiệp vụ (Core Domain) và các dịch vụ bổ trợ (Hạ tầng, Tiện ích, Gửi thư, Thanh toán).

### Bước 2: Thiết Kế Mô Hình Kiến Trúc Tối Giản (Architectural Style Selection)
- Ưu tiên kiến trúc Modular Monolith cho hầu hết các giai đoạn đầu để tối ưu tốc độ phát triển và tính đơn giản trong vận hành.
- Phân tách theo các tầng chuẩn:
  - **Presentation Layer**: HTTP Controllers, UI views, CLI interfaces.
  - **Domain / Application Layer**: Business logic, Use cases, Services thuần túy không phụ thuộc framework.
  - **Infrastructure Layer**: Cơ sở dữ liệu, API bên thứ ba, Message Broker.

### Bước 3: Xác Định Luồng Dữ Liệu Một Chiều (Data Flow Specification)
- Thiết lập quy tắc phụ thuộc: Tầng ngoài phụ thuộc tầng trong (Dependency Inversion).
- Dữ liệu di chuyển theo luồng rõ ràng: `Request → Controller → DTO Validation → Use Case / Service → Repository → DB → Response`.

### Bước 4: Soạn Thảo Quyết Định Kiến Trúc (Document ADR)
- Với mỗi quyết định kỹ thuật lớn (ví dụ chọn PostgreSQL thay vì MongoDB, chọn Redis cache): Soạn thảo một tài liệu ADR chuẩn mực nêu rõ: Ngữ cảnh, Các phương án đã cân nhắc, Lý do lựa chọn và Hệ quả (Consequences).

### Bước 5: Triển Khai Bộ Khung Kiến Trúc (Architecture Scaffolding)
- Tạo cấu trúc thư mục, thiết lập dependency injection container (nếu có) và interface hợp đồng giữa các module.
- Viết một kịch bản End-to-End mẫu (Vertical Slice) đi qua đủ các tầng để kiểm chứng tính thông suốt của kiến trúc.

### Bước 6: Kiểm Thử Ranh Giới & Đánh Giá Mở Rộng (Boundary Testing)
- Kiểm tra xem các module có bị phụ thuộc chéo hoặc rò rỉ chi tiết cài đặt của nhau không.
- Đánh giá khả năng mở rộng theo chiều ngang (Statelessness, horizontal scaling).

## 6. Quality Gates
- **QG-01 (Architecture Scoped)**: Ranh giới các module được định nghĩa rõ, không có sự chồng chéo trách nhiệm.
- **QG-03 (No Layer Leaks)**: Tầng nghiệp vụ không import trực tiếp các chi tiết kỹ thuật của tầng hạ tầng.
- **QG-09 (ADR Documented)**: Mỗi quyết định kiến trúc cốt lõi đều có file ADR lưu trong `docs/adr/`.

## 7. Safety Rules
- **Tránh Kỹ Thuật Hóa Quá Mức (Over-engineering)**: Cấm áp dụng các mẫu thiết kế phức tạp (Microservices, Event Sourcing, CQRS) khi bài toán chỉ ở mức đơn giản hoặc trung bình.
- **Không Tạo Điểm Nghẽn Đơn Lẻ (Single Point of Failure)**: Tránh thiết kế các dịch vụ tập trung mà khi sập sẽ làm toàn bộ ứng dụng tê liệt hoàn toàn.
- **Kiểm Soát Tính Phụ Thuộc**: Các module giao tiếp với nhau qua interfaces và DTOs rõ ràng, không truy cập trực tiếp vào bảng cơ sở dữ liệu của nhau.

## 8. Expected Outputs
1. Bản thiết kế kiến trúc hệ thống (Sơ đồ luồng, phân tầng, ranh giới module).
2. Bản ghi Architecture Decision Record (ADR) hoàn chỉnh.
3. Bộ khung mã nguồn (Scaffolded baseline) với một lát cắt dọc (Vertical slice) mẫu.

## 9. Failure Handling
- Nếu kiến trúc đề xuất gây nghẽn hiệu năng hoặc quá cồng kềnh trong việc viết test: Đơn giản hóa kiến trúc ngay lập tức, đưa logic về gần hơn với phong cách Modular Monolith.

## 10. Completion Criteria
- Các ranh giới module độc lập, rõ ràng. Luồng dữ liệu nhất quán một chiều.
- Quyết định kiến trúc được ghi nhận trong ADR. Vertical slice chạy thành công từ đầu đến cuối.

---

## Real-world Example
Dự án Quản lý Đặt vé (Booking System):
- *ADR-001*: Chọn cấu trúc Modular Monolith thay vì Microservices để giảm độ phức tạp vận hành mạng.
- *Chia module*: `modules/booking`, `modules/cinema`, `modules/payment`, `modules/notification`.
- *Luồng dữ liệu*: `BookingController` tiếp nhận request → `BookingService` giữ vé tạm thời và gọi `PaymentService` qua interface → `BookingRepository` ghi DB với transaction an toàn.
