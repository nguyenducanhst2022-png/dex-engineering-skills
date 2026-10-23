---
name: dex-architecture-decision-records
description: Establish and govern Architecture Decision Records (ADR) capturing technical context, evaluated alternatives, tradeoffs, and consequences. Use when proposing major architectural changes, selecting core frameworks, or establishing lasting technical consensus.
---

# dex-architecture-decision-records

## 1. Purpose & Scope
Thiết lập quy trình ghi nhận và quản trị các Quyết định Kiến trúc (Architecture Decision Records - ADR); lưu vết bối cảnh kỹ thuật, các giải pháp thay thế được đánh giá, đánh đổi chi phí/hiệu năng, và hệ quả dài hạn nhằm bảo đảm tính minh bạch trong quá trình tiến hóa hệ thống.

## 2. When to Use
- Khi đề xuất thay đổi kiến trúc trọng yếu (chuyển đổi database, giao thức giao tiếp, mô hình phân tách service).
- Khi lựa chọn ngôn ngữ, framework hoặc công cụ nền tảng cho tổ chức.
- Khi cần bảo lưu lý do kỹ thuật đằng sau các quyết định phức tạp để tránh tranh cãi lặp lại.

## 3. When NOT to Use
- Khi thực hiện các sửa đổi triển khai chi tiết hoặc bugfix nhỏ không ảnh hưởng cấu trúc hệ thống.
- Khi viết tài liệu hướng dẫn sử dụng sản phẩm dành cho người dùng cuối.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Đề xuất kỹ thuật, phân tích yêu cầu phi chức năng (NFR), danh sách các phương án kỹ thuật khả dĩ.
- **Quyền hạn truy cập:** Quyền ghi tài liệu kiến trúc trong thư mục `docs/adr/` hoặc repository tài liệu tập trung.

## 5. Core Concepts & Taxonomy
- **MADR / Nygard ADR Template:** Cấu trúc chuẩn hóa gồm Status, Context, Decision Drivers, Considered Options, Decision Outcome, Pros/Cons.
- **Immutability of Historical Records:** ADR đã chốt ở trạng thái `Accepted` không được sửa đổi nội dung; khi thay đổi quyết định, tạo ADR mới với trạng thái `Supersedes [ADR-XXXX]`.
- **Consequences & Tradeoffs:** Phân tích rõ cả mặt tích cực lẫn mặt tiêu cực, nợ kỹ thuật phát sinh sau quyết định.

## 6. Step-by-Step Execution Workflow
1. Khởi tạo tệp ADR mới trong `docs/adr/` theo định dạng `NNNN-short-title.md` với trạng thái `Proposed`.
2. Đặc tả bối cảnh kỹ thuật, động lực thúc đẩy quyết định và các ràng buộc hệ thống.
3. Liệt kê tối thiểu 2-3 phương án thay thế kèm theo bảng so sánh ưu nhược điểm định lượng.
4. Trình bày quyết định được chọn cùng lý do xác đáng và các hệ quả liên quan.
5. Tổ chức buổi Architecture Review họp bàn với các Tech Leads để đạt đồng thuận.
6. Cập nhật trạng thái sang `Accepted` hoặc `Rejected`, lưu vết commit vào Git.

## 7. Concrete Examples
### Ví dụ tệp Architecture Decision Record chuẩn MADR:
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
```

## 8. Anti-Patterns & Common Traps
- **Silent Decisions:** Tự ý thay đổi kiến trúc nền tảng trong pull request mà không tạo ADR thảo luận.
- **Retroactive Justification:** Tạo ADR chỉ để hợp thức hóa một quyết định đã làm mà không phân tích các phương án khác.
- **Zombie ADRs:** Để ADR ở trạng thái `Proposed` kéo dài nhiều tháng mà không chốt hoặc loại bỏ.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Tệp ADR phải tuân thủ chuẩn cấu trúc (Status, Context, Options, Outcome).
- **QG-08**: Liên kết tới các ADR liên quan hoặc bị thay thế (`Supersedes`) phải hợp lệ.
- **QG-14**: Đã được ký duyệt từ tối thiểu 2 reviewers có vai trò Architect/Staff Engineer.

## 10. Security & Safety Boundaries
- Không ghi lộ các thông tin mật (API keys, connection strings, credentials) trong nội dung ADR.
- Rà soát các quyết định kiến trúc để bảo đảm tuân thủ nguyên tắc Least Privilege và Zero Trust.

## 11. Platform Adapters
- **ADR CLI Tools**: Tích hợp với `adr-tools` hoặc `log4brains` để tự động hóa sinh số thứ tự và cập nhật chỉ mục.
- **Linter Integration**: Cấu hình markdownlint để kiểm tra cấu trúc định dạng ADR trong CI.

## 12. Deliverables & Output Artifacts
- Tệp tài liệu `docs/adr/NNNN-<title>.md` hợp lệ.
- Cập nhật chỉ mục `docs/adr/README.md`.
- Bằng chứng phê duyệt trên Git pull request.

## 13. Related & Complementary Skills
dex-software-architecture, dex-contract-first-development, dex-modular-monolith-boundaries

## 14. Realistic Usage Example
```powershell
# 1. Khởi tạo ADR mới
python scripts/adr_manager.py new "Use-gRPC-For-Internal-Communication"

# 2. Kiểm tra tính toàn vẹn và liên kết của danh mục ADR
python scripts/adr_manager.py validate
```
