---
name: dex-postgres-migration-lock-budget
description: Analyze, predict, and control table locks induced by PostgreSQL DDL migrations. Set strict lock timeout budgets, sequence non-blocking schema changes, and prevent service outages. Use when executing zero-downtime database migrations.
---

# dex-postgres-migration-lock-budget

## 1. Purpose & Scope
Phân tích, ước tính và kiểm soát chặt chẽ cấp độ khóa bảng (Lock Levels) do các lệnh DDL gây ra trong PostgreSQL; áp dụng ngân sách thời gian chờ khóa (Lock Timeout Budget) để bảo đảm migration không bao giờ làm treo hệ thống hoặc chặn đứng các truy vấn đọc/ghi của người dùng; xây dựng lộ trình nâng cấp zero-downtime.

## 2. When to Use
- Khi thực hiện thêm cột mới, đổi kiểu dữ liệu, thêm ràng buộc `NOT NULL`, hoặc tạo chỉ mục trên các bảng lớn hàng chục triệu bản ghi.
- Khi cần bảo đảm tính sẵn sàng 99.99% của hệ thống trong thời gian chạy migration hạ tầng cơ sở dữ liệu.
- Khi thiết lập quy trình kiểm duyệt migration tự động trong pipeline CI/CD.

## 3. When NOT to Use
- Khi ứng dụng đang trong giai đoạn phát triển ban đầu (Development/PoC) chưa có người dùng thật và có thể chấp nhận thời gian bảo trì ngắn.
- Khi thao tác trên cơ sở dữ liệu SQLite cục bộ không có cơ chế đa người dùng đồng thời.

## 4. Prerequisites & Input Context
- **Mã nguồn Migration:** Các tệp SQL migration dự kiến thực thi.
- **Số liệu bảng thực tế:** Kích thước bảng (table size), số lượng hàng, tần suất truy vấn TPS (Transactions Per Second) và độ nhạy cảm của dịch vụ.

## 5. Core Concepts & Taxonomy
- **ACCESS EXCLUSIVE Lock:** Cấp độ khóa cao nhất trong PostgreSQL, chặn hoàn toàn mọi truy vấn đọc và ghi (kể cả `SELECT`); gây ra bởi các lệnh như `ALTER TABLE ADD COLUMN` có rewrite bảng, `DROP TABLE`, hoặc `ALTER TABLE ALTER TYPE`.
- **Lock Queue Starvation:** Khi một lệnh DDL yêu cầu khóa độc quyền đang phải chờ một truy vấn dài hoàn thành, tất cả các truy vấn đọc ghi đến sau nó cũng bị dồn ứ sau DDL, dẫn đến cạn kiệt pool kết nối chỉ sau vài giây.
- **Lock Timeout Budget:** Kỹ thuật đặt `SET lock_timeout = '2s';` trước khi chạy DDL. Nếu sau 2 giây chưa lấy được khóa, migration lập tức hủy bỏ và thử lại sau thay vì làm nghẽn toàn bộ hệ thống.

## 6. Step-by-Step Execution Workflow
1. Rà soát từng câu lệnh trong tệp migration để xác định cấp độ khóa mà PostgreSQL sẽ yêu cầu.
2. Thay thế các mẫu DDL nguy hiểm: Thay vì `ALTER TABLE t ADD COLUMN c DEFAULT val;` (rewrite bảng trên Postgres cũ) hoặc thêm `NOT NULL` trực tiếp, chia nhỏ thành: thêm cột nullable → cập nhật dữ liệu ngầm → thêm ràng buộc `CHECK (c IS NOT NULL) NOT VALID` → xác thực ràng buộc bằng `VALIDATE CONSTRAINT`.
3. Thay thế tạo chỉ mục trực tiếp bằng `CREATE INDEX CONCURRENTLY`.
4. Đóng gói migration với thiết lập an toàn: `SET lock_timeout = '3s';` và `SET statement_timeout = '30s';`.
5. Chạy thử nghiệm migration trên bản sao staging có lưu lượng tải mô phỏng để đo lường thời gian chiếm giữ khóa thực tế.

## 7. Concrete Examples
### Mẫu Migration an toàn thêm cột NOT NULL trên bảng lớn không downtime:
```sql
-- Phase 1: Dat lock timeout budget nghiem ngat
SET lock_timeout = '2s';
SET statement_timeout = '10s';

-- Phase 2: Them cot Nullable (chi ton ACCESS EXCLUSIVE micro-giay, khong rewrite bang)
ALTER TABLE public.orders 
ADD COLUMN IF NOT EXISTS status_code varchar(32);

-- Phase 3: Them rang buoc CHECK chua validate (chi can SHARE UPDATE EXCLUSIVE rat ngan)
ALTER TABLE public.orders 
ADD CONSTRAINT chk_orders_status_valid 
CHECK (status_code IS NOT NULL) NOT VALID;

-- Phase 4: Validate rang buoc khong khoa ghi (SHARE UPDATE EXCLUSIVE, quet tuan tu)
ALTER TABLE public.orders 
VALIDATE CONSTRAINT chk_orders_status_valid;
```

## 8. Anti-Patterns & Common Traps
- **Adding Foreign Key Direct without NOT VALID:** Tạo khóa ngoại trực tiếp bằng `ALTER TABLE ... ADD CONSTRAINT FOREIGN KEY` sẽ chiếm `ACCESS EXCLUSIVE` và quét toàn bộ bảng để kiểm tra dữ liệu, gây nghẽn hệ thống.
- **Running CREATE INDEX inside a Multi-Statement Transaction:** `CREATE INDEX CONCURRENTLY` không thể chạy bên trong một transaction block (`BEGIN ... COMMIT`), việc gộp chung sẽ gây lỗi cú pháp.
- **Infinite Lock Timeout:** Để mặc định `lock_timeout = 0`, khiến lệnh DDL chờ vô thời hạn và chặn đứng toàn bộ traffic sản xuất.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: 100% các tệp migration DDL trên môi trường sản xuất đều có khai báo `SET lock_timeout` rõ ràng (<= 5s).
- **QG-02**: Không có lệnh tạo chỉ mục thông thường (`CREATE INDEX`) trên bảng trên 100,000 bản ghi; bắt buộc dùng `CONCURRENTLY`.
- **QG-03**: Mọi ràng buộc kiểm tra toàn vẹn (`CHECK`, `FOREIGN KEY`) đều áp dụng chiến lược 2 bước: `NOT VALID` tiếp theo là `VALIDATE CONSTRAINT`.

## 10. Security & Safety Boundaries
- Bảo vệ tính sẵn sàng cao (High Availability) của hệ thống thanh toán và dữ liệu lõi trước nguy cơ tê liệt do tắc nghẽn khóa CSDL.

## 11. Platform Adapters
- **Tooling**: Strong Migrations, Squawk Linter, PostgreSQL pg_stat_activity, Flyway, Prisma Migrate.

## 12. Deliverables & Output Artifacts
- Bản vá migration tối ưu hóa ngân sách khóa (`safe_migration.sql`).
- Báo cáo phân tích cấp độ khóa và thời gian chiếm giữ dự kiến.
- Kịch bản rollback khẩn cấp nếu migration chạm trần timeout.

## 13. Related & Complementary Skills
dex-database-engineering, dex-database-query-plans, dex-postgres-index-maintenance

## 14. Realistic Usage Example
```bash
# Quet kiem tra cac cau lenh khoa nguy hiem trong migrations bang squawk
npx squawk-cli supabase/migrations/*.sql

# Chay migration voi co che fallback retry tu dong
python scripts/safe_migrate.py --timeout 2s --file migration.sql
```
