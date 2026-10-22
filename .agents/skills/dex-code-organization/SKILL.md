---
name: dex-code-organization
description: Clean project structuring and modular codebase organization. Establishes intuitive directory hierarchies, enforces separation of concerns, decouples dependencies, and prevents god-files or tangled circular imports. Use when scaffolding projects, refactoring monolithic files, or structuring new modules.
---

# DEX Code Organization

## 1. Purpose
Tổ chức cấu trúc thư mục, tệp tin và các module mã nguồn theo các nguyên lý thiết kế phần mềm sạch (Clean Architecture / Modular Design), đảm bảo hệ thống dễ đọc, dễ sửa, dễ kiểm tra và dễ mở rộng.

Quy trình tổ chức chuẩn:
`Phân tích → Thiết kế cấu trúc → Chia Module → Viết code → Kiểm tra liên kết → Tối ưu → Ổn định`

Nguyên tắc cốt lõi: **Mỗi module đảm nhiệm một chức năng duy nhất và rõ ràng. Tuyệt đối không dồn toàn bộ dự án vào một file khổng lồ.**
Ghi nhớ: **Code tốt = Dễ đọc + Dễ sửa + Dễ kiểm tra + Dễ mở rộng.**

## 2. When to Use
- Khi khởi tạo một dự án phần mềm mới từ đầu (scaffolding).
- Khi một file mã nguồn phình to quá mức (>300 - 500 dòng) hoặc có quá nhiều trách nhiệm hỗn tạp (God-file).
- Khi các phụ thuộc giữa các module bị rối loạn hoặc xuất hiện lỗi phụ thuộc vòng (Circular Dependencies).
- Khi cần chuẩn hóa kiến trúc thư mục cho toàn đội ngũ hoặc các AI Agent khác tiếp quản.

## 3. When Not to Use
- Sửa lỗi cú pháp nhỏ trong một hàm độc lập không ảnh hưởng đến cấu trúc tổng thể.
- Khi dự án đã có cấu trúc chuẩn mực được phê duyệt và không cần tái cơ cấu.

## 4. Inputs
- Danh sách các tính năng và nghiệp vụ của ứng dụng.
- Cấu trúc thư mục hiện tại của dự án.
- Công nghệ, framework và quy ước đặt tên chuẩn của hệ sinh thái (Node.js, Python, Go, Java...).

## 5. Workflow

### Bước 1: Phân Tích Trách Nhiệm Nghiệp Vụ (Responsibility Analysis)
- Liệt kê các luồng xử lý chính: Routing, Controller/Handler, Service (Business Logic), Data Access (Repository/Model), Utils, DTO/Types.
- Xác định ranh giới giữa các module (Domain Boundaries).

### Bước 2: Thiết Kế Cây Thư Mục Trực Quan (Directory Hierarchy Design)
- Thiết lập cấu trúc thư mục theo tính năng (Feature-based) hoặc theo tầng (Layer-based).
- Đảm bảo cấu trúc phản ánh đúng nghiệp vụ:
  ```
  src/
    ├── modules/ (hoặc features/)
    │   ├── auth/
    │   ├── cart/
    │   └── billing/
    ├── shared/ (components, utils, types dùng chung)
    └── config/
  ```

### Bước 3: Chia Nhỏ Module & Đặt Tên Chuẩn Mực (Modularization)
- Tách các trách nhiệm riêng biệt thành các file chuyên trách:
  - `user.controller.ts`: Tiếp nhận HTTP request & validate input.
  - `user.service.ts`: Xử lý nghiệp vụ người dùng.
  - `user.repository.ts`: Thao tác trực tiếp với cơ sở dữ liệu.
  - `user.types.ts`: Định nghĩa interface, enum, types.

### Bước 4: Kiểm Soát Liên Kết & Chiều Phụ Thuộc (Dependency Control)
- Đảm bảo luồng phụ thuộc một chiều: Controller phụ thuộc vào Service, Service phụ thuộc vào Repository.
- Không để tầng dữ liệu gọi ngược lên tầng Controller.
- Sử dụng Barrel exports (`index.ts`) một cách có kiểm soát, tránh tạo vòng lặp import.

### Bước 5: Kiểm Tra Liên Kết & Biên Dịch (Linkage Verification)
- Chạy type-check và linter để phát hiện các import bị hỏng, import thừa hoặc circular imports.
- Đảm bảo các đường dẫn import tương đối/tuyệt đối (alias paths như `@/`) nhất quán.

### Bước 6: Tối Ưu & Ổn Định (Optimization & Stabilization)
- Xóa các file mồ côi (dead files / unused files).
- Cập nhật tài liệu cấu trúc thư mục trong `README.md` hoặc `ARCHITECTURE.md`.

## 6. Quality Gates
- **QG-01 (Scope Defined)**: Các module mới được đặt đúng thư mục quy định.
- **QG-03 (No Circular Imports & Type Clean)**: Không có lỗi circular dependency hoặc unresolved path.
- **QG-04 (Build Clean)**: Dự án build thành công với cấu trúc thư mục mới.

## 7. Safety Rules
- **Không Di Chuyển File Bừa Bãi**: Khi đổi vị trí hoặc đổi tên file, phải cập nhật 100% các câu lệnh import ở mọi file liên quan.
- **Tránh Quá Nhiều Tầng Thư Mục Không Cần Thiết**: Tránh tạo cây thư mục quá sâu (lồng quá 5 cấp thư mục) gây khó đọc và khó import.
- **Giữ File Dưới 300 Dòng**: Bất kỳ file nào vượt quá 300 dòng cần được xem xét tách nhỏ thành các hàm phụ trợ hoặc component con.

## 8. Expected Outputs
1. Cấu trúc thư mục sạch sẽ, module hóa cao.
2. Mã nguồn được phân tách trách nhiệm rõ ràng (Single Responsibility Principle).
3. Không còn file khổng lồ (God-files) hoặc mớ bòng bong import.

## 9. Failure Handling
- Nếu việc di chuyển file gây lỗi import trên diện rộng không kiểm soát được: Sử dụng Git để khôi phục lại trạng thái cũ, lập danh sách ánh xạ import trước và di chuyển từng file một.

## 10. Completion Criteria
- Các trách nhiệm nghiệp vụ được phân chia vào đúng file/thư mục.
- Không có circular dependencies. Toàn bộ dự án biên dịch thành công.

---

## Real-world Example
Tái cấu trúc một file `server.js` 1200 dòng chứa cả kết nối DB, routes, logic thanh toán và gửi email:
- `src/config/database.js`: Chỉ chứa kết nối MongoDB.
- `src/routes/payment.routes.js`: Định nghĩa các endpoint `/api/payments`.
- `src/services/payment.service.js`: Chứa hàm tính tiền và gọi cổng Stripe.
- `src/services/email.service.js`: Chứa hàm gửi email biên lai.
- Kết quả: `server.js` giảm xuống còn 35 dòng làm nhiệm vụ bootstrap server.
