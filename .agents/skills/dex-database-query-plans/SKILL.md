---
name: dex-database-query-plans
description: Analyze and optimize database execution plans using EXPLAIN ANALYZE, detect Seq Scans, eliminate temporary spills, tune index strategies, and benchmark SQL queries. Use when diagnosing slow queries, optimizing database CPU load, or tuning complex SQL joins.
---

# dex-database-query-plans

## 1. Purpose & Scope
Phân tích chuyên sâu và tối ưu hóa kế hoạch thực thi câu lệnh cơ sở dữ liệu (Execution Plans) bằng công cụ `EXPLAIN ANALYZE` (trên PostgreSQL, MySQL); nhận diện và triệt tiêu các câu lệnh quét toàn bộ bảng (Sequential Scans / Full Table Scans), loại bỏ tràn bộ nhớ tạm ra đĩa (WorkMem Spills), tối ưu hóa các phép nối bảng (Nested Loop, Hash Join, Merge Join) và thiết kế chỉ mục (Index Strategy) chuẩn xác.

## 2. When to Use
- Khi một câu truy vấn SQL chạy chậm bất thường (> 500ms - 2s) làm nghẽn CPU database.
- Khi hệ thống giám sát cảnh báo Database CPU duy trì ở mức 90-100%.
- Khi một bảng dữ liệu phình to từ 10,000 dòng lên 5 triệu dòng và các chức năng tra cứu bắt đầu bị timeout.

## 3. When NOT to Use
- Tối ưu hóa code thuật toán CPU trong RAM ứng dụng (dùng `dex-performance-optimization`).
- Thiết kế kiến trúc phân vùng dữ liệu tổng thể (dùng `dex-software-architecture`).

## 4. Prerequisites & Input Context
**Đầu vào cần thiết:**
- Câu truy vấn SQL chạy chậm cần tối ưu.
- Đầu ra của câu lệnh `EXPLAIN (ANALYZE, BUFFERS, VERBOSE)` từ cơ sở dữ liệu.
- Cấu trúc bảng hiện tại và danh sách các chỉ mục (Indexes) đang có.

**Điều kiện tiên quyết:**
- Có quyền thực thi lệnh `EXPLAIN` trên môi trường cơ sở dữ liệu thử nghiệm có lượng dữ liệu tương đương sản xuất.
- Không chạy các lệnh `EXPLAIN ANALYZE` có chứa thao tác xóa/cập nhật dữ liệu thật mà không bọc trong transaction rollback.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**: Nắm vững cơ chế vận hành theo chuẩn Agent Skills, tuân thủ nghiêm ngặt tính xác định và ranh giới trách nhiệm.
- **Quy tắc quyết định kỹ thuật**:
- **Thứ Tự Cột Trong Composite Index Là Sống Còn**: Cột có độ chọn lọc cao nhất (High Cardinality) và sử dụng phép so sánh bằng (`=`) PHẢI luôn đứng trước các cột so sánh khoảng (`<`, `>`, `BETWEEN`).
- **Tránh Bọc Hàm Quanh Cột Index**: Cấm viết `WHERE LOWER(email) = 'abc'`; nếu cần tìm kiếm không phân biệt hoa thường, phải tạo Functional Index: `CREATE INDEX idx_users_lower_email ON users(LOWER(email))`.
- **Không Index Quá Nhiều**: Mỗi bảng chỉ nên có từ 3 đến 7 index thực sự hữu ích; quá nhiều index sẽ làm chậm nghiêm trọng tốc độ ghi dữ liệu và tốn dung lượng RAM.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Tạo index xong nhưng database vẫn không chịu dùng (vẫn Seq Scan)**: Do dữ liệu trong bảng quá ít (Postgres thấy Seq Scan nhanh hơn) hoặc kiểu dữ liệu so sánh không khớp (so sánh chuỗi với số làm ép kiểu ngầm) -> Khắc phục: Kiểm tra đúng kiểu dữ liệu của tham số và kiểm tra độ phân tán của dữ liệu.
- **Tạo index trên bảng 100 triệu dòng làm treo hệ thống**: Do lệnh `CREATE INDEX` khóa bảng -> Khắc phục: Luôn sử dụng cờ `CREATE INDEX CONCURRENTLY` trong PostgreSQL.

## 6. Step-by-Step Execution Workflow
1. Thu thập câu lệnh `EXPLAIN (ANALYZE, BUFFERS)` của câu query chậm.
2. Đọc cây kế hoạch thực thi (Execution Tree): Xác định node nào chiếm thời gian lâu nhất (Actual Time) và tốn tài nguyên I/O nhất (Shared Read Buffers).
3. Nhận diện các điểm nghẽn kinh điển:
   - *Seq Scan trên bảng lớn*: Thiếu chỉ mục cho các cột trong mệnh đề `WHERE` hoặc `JOIN`.
   - *Sort Method: external merge Disk*: Do dung lượng bộ nhớ `work_mem` quá nhỏ, việc sắp xếp bị tràn ra ổ cứng chậm chạp.
   - *Nested Loop với số dòng ước lượng sai*: Do thống kê database (Statistics) bị lỗi thời; cần chạy `ANALYZE table_name`.
4. Đề xuất giải pháp tối ưu:
   - Tạo Composite Index đúng thứ tự (cột lọc bằng `=` đứng trước, cột lọc khoảng `>` đứng sau).
   - Áp dụng Covering Index (`INCLUDE` clause) để đạt Index Only Scan (không cần đọc lại heap table).
   - Viết lại câu query: Thay thế toán tử `OR` bằng `UNION ALL`, loại bỏ các hàm bọc quanh cột lọc (như `WHERE DATE(created_at) = ...` làm vô hiệu hóa index).
5. Thực thi giải pháp và chạy lại `EXPLAIN ANALYZE` để đối chiếu số liệu thời gian thực thi (Execution Time) và số lượng Buffer đọc được giảm thiểu.
6. Kiểm tra hồi quy: Đảm bảo chỉ mục mới không làm chậm tốc độ ghi (`INSERT`/`UPDATE`) của bảng quá mức.

## 7. Concrete Examples
### Ví dụ triển khai chuẩn mực:
```sql
-- Tối ưu triệt để bằng Covering Index trong PostgreSQL
-- Trước: Seq Scan mất 450ms
-- Giải pháp: Tạo Composite Index hỗ trợ lọc và sắp xếp không cần đọc heap
CREATE INDEX CONCURRENTLY idx_orders_user_status_created 
ON orders (user_id, status, created_at DESC) 
INCLUDE (total_amount);

-- Sau: Index Only Scan mất 1.2ms (nhanh gấp 375 lần!)
```

### Lệnh xác minh & thực thi:
- Chạy phân tích kế hoạch chi tiết: `EXPLAIN (ANALYZE, BUFFERS) SELECT * FROM orders WHERE user_id = 123 ORDER BY created_at DESC LIMIT 10;`
- Kiểm tra kích thước index: `SELECT pg_size_pretty(pg_relation_size('idx_orders_user_created'));`
- Cập nhật thống kê database: `ANALYZE orders;`

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước kiểm tra biên và giả định hệ thống luôn ở trạng thái lý tưởng.
- **Anti-Pattern 2**: Không ghi nhận nhật ký kiểm toán hoặc bỏ qua việc xử lý ngoại lệ lúc runtime.
- **Trap**: Bỏ qua các rào chắn an toàn hoặc cố tình chạy script không qua kiểm thử tự động.

## 9. Quality Gates & Acceptance Criteria
- QG-04: Thời gian thực thi của câu query (Execution Time) giảm tối thiểu 80% sau khi tối ưu.
- QG-10: Kế hoạch thực thi chuyển từ `Seq Scan` sang `Index Scan` hoặc `Index Only Scan` có bằng chứng rõ ràng.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động trước khi coi là hoàn thành.

## 10. Security & Safety Boundaries
- Khi chạy `EXPLAIN ANALYZE` có chứa câu lệnh `UPDATE` hoặc `DELETE`, BẮT BUỘC phải đặt trong transaction và ROLLBACK ngay: `BEGIN; EXPLAIN ANALYZE UPDATE ...; ROLLBACK;` để không làm thay đổi dữ liệu thật.
- Không bao giờ thực thi mã nguồn hoặc thay đổi cấu hình trên môi trường sản xuất mà thiếu cơ chế rollback an toàn.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Có thể kích hoạt trực tiếp từ terminal hoặc extension tương thích trong VS Code / Cursor / Windsurf.

## 12. Deliverables & Output Artifacts
- Bản so sánh Execution Plan Trước và Sau tối ưu.
- Câu lệnh tạo Index tối ưu (`CREATE INDEX CONCURRENTLY ...`).
- Bản viết lại của câu truy vấn SQL (nếu có tái cấu trúc query).

## 13. Related & Complementary Skills
- `dex-development-workflow`: Quy trình phát triển tiêu chuẩn.
- `dex-code-verification`: Xác minh chất lượng và tính đúng đắn của mã nguồn.
- `dex-master-orchestrator`: Bộ điều phối trung tâm kết nối kỹ năng này với các kỹ năng khác trong hệ thống.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư hoặc AI Agent tiếp nhận yêu cầu liên quan đến **dex-database-query-plans**.
1. Đọc kỹ đầu vào và các ràng buộc kỹ thuật tại mục 4.
2. Thực thi tuần tự 6 bước trong Workflow tại mục 6.
3. Chạy các lệnh kiểm chứng tại mục 7 và đối chiếu với Quality Gates tại mục 9.
4. Đóng gói deliverables theo danh sách tại mục 12 và báo cáo kết quả kèm bằng chứng xác thực.
