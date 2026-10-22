---
name: dex-database-engineering
description: Database engineering, relational schema design, safe migrations, index optimization, ACID transaction management, and automated backup strategies. Guarantees zero-downtime schema evolution and data integrity. Use when altering database schemas, writing migrations, optimizing slow queries, or managing transactions.
---

# DEX Database Engineering

## 1. Purpose & Scope
Thiết kế, quản lý và tối ưu hóa cơ sở dữ liệu chuyên nghiệp, đảm bảo dữ liệu luôn chính xác, nhất quán, an toàn và có khả năng khôi phục khi xảy ra sự cố; thực hiện các đợt migration cấu trúc dữ liệu không gây gián đoạn hệ thống (Zero-downtime migrations).

Quy trình database chuẩn:
`Phân tích dữ liệu → Thiết kế Schema → Xác định quan hệ → Tạo Database → Migration → Tối ưu truy vấn → Kiểm thử → Backup → Ổn định → Lưu Git`

Nguyên tắc cốt lõi: **Dữ liệu phải chính xác, nhất quán, an toàn và có khả năng khôi phục khi xảy ra sự cố.**
Ghi nhớ sống còn: **Database tốt = Dữ liệu chính xác + Truy vấn hiệu quả + Bảo mật + Khôi phục được + Dễ mở rộng.**

## 2. When to Use
- Khi thiết kế bảng (tables), thực thể hoặc schema dữ liệu mới.
- Khi tạo hoặc sửa đổi các tệp migration dữ liệu (Prisma, TypeORM, Alembic, Flyway, Knex, Goose).
- Khi tối ưu hóa các câu lệnh SQL chạy chậm thông qua việc đánh chỉ mục (Indexing) hoặc phân tích `EXPLAIN ANALYZE`.
- Khi cần bọc các thao tác cập nhật nhiều bảng liên quan trong các giao dịch an toàn (ACID Transactions).

## 3. When NOT to Use
- Thao tác trên các file lưu trữ tạm thời trong bộ nhớ không có tính bền vững (In-memory mock).
- Trực tiếp chạy các lệnh DDL phá hủy dữ liệu (`DROP TABLE`, `TRUNCATE`) thẳng vào database production mà không qua migration có kế hoạch.

## 4. Prerequisites & Input Context
- Mô hình dữ liệu thực thể (ERD) hoặc mô tả yêu cầu lưu trữ thông tin.
- Hệ quản trị cơ sở dữ liệu (PostgreSQL, MySQL, SQLite, MongoDB...).
- Bảng hướng dẫn an toàn migration chi tiết tại [migration-safety-checklist.md](references/migration-safety-checklist.md).

## 5. Core Concepts & Taxonomy
- **Nguyên tắc cốt lõi**: Tuân thủ triệt để nguyên lý vận hành xác định và ranh giới trách nhiệm của chuẩn Agent Skills.
- **Tính nhất quán hệ thống**: Mọi thao tác phải có thể kiểm chứng độc lập với kết quả đo lường rõ ràng.
- **Ngăn ngừa hồi quy**: Bất kỳ sửa đổi nào cũng phải bảo vệ tính tương thích ngược và chất lượng đã được nghiệm thu.

## 6. Step-by-Step Execution Workflow
### Bước 1: Thiết Kế Schema Chuẩn Hóa (Schema Normalization & Types)
- Chuẩn hóa dữ liệu theo chuẩn 3NF để giảm thiểu dư thừa, chỉ phi chuẩn hóa (denormalize) có chủ đích khi cần tối ưu đọc.
- Chọn kiểu dữ liệu chặt chẽ và tiết kiệm dung lượng: `UUID`/`BIGINT` cho ID, `TIMESTAMP WITH TIME ZONE` cho thời gian, `DECIMAL`/`NUMERIC` cho tiền tệ (CẤM dùng float/double cho tiền).
- Thiết lập ràng buộc toàn vẹn (Constraints): `NOT NULL`, `UNIQUE`, `CHECK`, `FOREIGN KEY` kèm quy tắc xóa (`ON DELETE RESTRICT` hoặc `CASCADE` có kiểm soát).

### Bước 2: Viết File Migration Hai Chiều (Reversible Migrations)
- Mọi thay đổi cấu trúc bảng bắt buộc phải được đóng gói trong file migration có thể tự động hóa:
  - Hàm `UP` (Apply): Thực hiện thêm bảng, thêm cột, tạo index.
  - Hàm `DOWN` (Rollback): Thực hiện hoàn tác chính xác những gì hàm `UP` đã làm.
- Tuân thủ quy tắc mở rộng và co hẹp (Expand and Contract Pattern) cho các cột đang có dữ liệu.

### Bước 3: Đánh Chỉ Mục Thông Minh (Targeted Indexing)
- Tạo Index cho các cột thường xuyên xuất hiện trong mệnh đề `WHERE`, `JOIN` hoặc `ORDER BY`.
- Tránh đánh index bừa bãi làm chậm tốc độ ghi (`INSERT`/`UPDATE`).
- Sử dụng Composite Index đúng thứ tự (cột có độ chọn lọc cao nhất đứng trước).
- Trong PostgreSQL/MySQL trên bảng lớn: Luôn tạo index với cờ không khóa bảng (`CREATE INDEX CONCURRENTLY` / `ALGORITHM=INPLACE`).

### Bước 4: Đảm Bảo Tính Toàn Vẹn Bằng Transaction (ACID Enforcement)
- Gom các thao tác ghi liên quan mật thiết vào trong một Transaction duy nhất:
  - Bắt đầu: `BEGIN TRANSACTION`.
  - Thực thi các câu lệnh.
  - Kết thúc: `COMMIT` khi thành công, hoặc `ROLLBACK` lập tức khi có bất kỳ ngoại lệ nào.

### Bước 5: Kiểm Thử Migration Trên Môi Trường Cô Lập (Dry-Run & Rollback Test)
- Chạy thử migration trên database kiểm thử:
  1. Chạy `migration up` → Kiểm tra schema mới.
  2. Chạy `migration down` → Kiểm tra schema cũ được khôi phục nguyên vẹn.
  3. Chạy `migration up` lại lần nữa.
- Kiểm tra dữ liệu mẫu hiện hữu không bị mất mát hay biến dạng.

### Bước 6: Chiến Lược Sao Lưu & Khôi Phục (Backup & Recovery)
- Thiết lập quy trình sao lưu tự động định kỳ (Daily snapshot, WAL archiving / Point-in-time recovery).

## 7. Concrete Examples
```bash
# Lệnh thực thi & kiểm chứng tiêu chuẩn
dex verify --skill dex-database-engineering
```

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước xác minh tự động và dựa vào giả định chủ quan.
- **Anti-Pattern 2**: Thay đổi diện rộng vượt ngoài phạm vi (Scope Creep) làm mất kiểm soát rủi ro.
- **Trap**: Thực hiện thao tác phá hủy hoặc thay đổi trạng thái sản xuất khi chưa qua cổng kiểm duyệt an toàn.

## 9. Quality Gates & Acceptance Criteria
- **QG-01 (DB Scope Confined)**: Migration chỉ tác động đến đúng bảng và cột trong phạm vi yêu cầu.
- **QG-04 (Migration Up/Down PASS)**: Cả hai chiều migration UP và DOWN đều thực thi thành công không lỗi cú pháp.
- **QG-06 (Data Preserved)**: Không làm mất mát hoặc hỏng dữ liệu của các bản ghi hiện có.

## 10. Security & Safety Boundaries
- **Quy Tắc Bất Khả Xâm Phạm**: TUYỆT ĐỐI KHÔNG BAO GIỜ chạy migration trực tiếp sửa schema mà không có file migration được lưu vào Git.
- **Cấm Xóa Cột Đột Ngột**: Cấm xóa cột (DROP COLUMN) hoặc đổi tên cột (RENAME COLUMN) trên bảng đang chạy live trong cùng một bước. Phải trải qua 3 giai đoạn: (1) Thêm cột mới → (2) Đồng bộ dữ liệu hai chiều → (3) Dừng dùng cột cũ rồi mới xóa sau.
- **Tiền Tệ Phải Chính Xác**: Luôn dùng `DECIMAL(18, 4)` hoặc lưu trữ số nguyên đơn vị cents/xu, cấm dùng kiểu số thực `FLOAT`/`DOUBLE` vì sai số làm tròn.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Kích hoạt thông qua terminal hoặc tiện ích mở rộng IDE tương thích (VS Code, Cursor, Windsurf).

## 12. Deliverables & Output Artifacts
1. File migration mới có cả `UP` và `DOWN` đầy đủ.
2. Cập nhật schema definition file (ví dụ `schema.prisma` hoặc `models.py`).
3. Bằng chứng chạy thử migration UP/DOWN thành công.

## 13. Related & Complementary Skills
- `dex-master-orchestrator`: Điều phối trung tâm.

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Kỹ sư hoặc AI Agent kích hoạt **dex-database-engineering** trong dự án.
1. Tiếp nhận ngữ cảnh đầu vào và kiểm tra điều kiện tiên quyết tại Mục 4.
2. Vận hành tuần tự các bước theo Quy trình tại Mục 6.
3. Kiểm chứng đầu ra đối chiếu với Tiêu chuẩn chấp thuận tại Mục 9.
4. Bàn giao đầy đủ hiện vật theo Mục 12 và cập nhật tài liệu liên quan.
