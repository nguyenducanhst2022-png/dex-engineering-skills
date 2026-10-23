---
name: dex-postgres-partition-lifecycle
description: Design, automate, and maintain declarative PostgreSQL table partitioning. Implement automated partition creation, retention policies, boundary enforcement, and concurrent detachment. Use when managing high-volume time-series or multi-tenant datasets.
---

# dex-postgres-partition-lifecycle

## 1. Purpose & Scope
Thiết kế, tự động hóa và quản lý toàn bộ vòng đời phân vùng (Table Partitioning) trong PostgreSQL; áp dụng kỹ thuật Declarative Partitioning theo phạm vi thời gian (Range) hoặc danh sách (List); thiết lập chính sách lưu trữ và xóa bỏ dữ liệu cũ (Data Retention); tự động tạo trước phân vùng tương lai; và thực hiện tách phân vùng cũ không downtime bằng `DETACH PARTITION CONCURRENTLY`.

## 2. When to Use
- Khi bảng dữ liệu thời gian (Logs, Events, Audit Trails, Timeseries) vượt quá 50 triệu bản ghi hoặc hàng trăm gigabyte.
- Khi nhu cầu truy vấn chủ yếu tập trung vào khoảng thời gian gần đây (ví dụ: 30 ngày qua) và cần tăng tốc độ lọc qua Partition Pruning.
- Khi cần xóa dữ liệu cũ cực nhanh bằng `DROP TABLE partition_name;` thay vì chạy lệnh `DELETE` tốn nhiều tài nguyên.

## 3. When NOT to Use
- Khi bảng dữ liệu có quy mô nhỏ dưới vài gigabyte (việc phân vùng chỉ làm tăng độ phức tạp quản trị mà không đem lại lợi ích hiệu năng).
- Khi câu truy vấn thường xuyên phải quét toàn bộ các phân vùng mà không thể lọc theo Partition Key.

## 4. Prerequisites & Input Context
- **Lược đồ CSDL:** Cấu trúc bảng nguồn và định nghĩa khóa phân vùng (`Partition Key`).
- **PostgreSQL Version:** PostgreSQL 11 trở lên (khuyến nghị 14+ để hỗ trợ đầy đủ `DETACH CONCURRENTLY`).

## 5. Core Concepts & Taxonomy
- **Declarative Range Partitioning:** Cơ chế phân chia một bảng cha trừu tượng thành các bảng con vật lý dựa trên giá trị nhỏ nhất và lớn nhất của cột thời gian (`FOR VALUES FROM (...) TO (...)`).
- **Partition Pruning:** Khả năng của bộ lập kế hoạch truy vấn tự động loại trừ các bảng con không chứa dữ liệu cần tìm, giảm số trang đĩa phải quét từ hàng triệu xuống vài nghìn.
- **DETACH PARTITION CONCURRENTLY:** Tách một bảng con ra khỏi bảng cha mà chỉ yêu cầu khóa `SHARE UPDATE EXCLUSIVE` thay vì `ACCESS EXCLUSIVE`, giúp hệ thống duy trì hoạt động liên tục trong quá trình archive dữ liệu cũ.

## 6. Step-by-Step Execution Workflow
1. Thiết kế bảng cha phân vùng với cấu trúc khóa chính chứa Partition Key: `CREATE TABLE events (...) PARTITION BY RANGE (created_at);`.
2. Soạn thảo hàm tự động tạo trước các phân vùng cho 3 tháng tiếp theo để ngăn lỗi chèn dữ liệu khi thiếu phân vùng tương ứng.
3. Thiết lập cronjob hoặc pg_cron định kỳ kiểm tra và tạo partition mới trước ngày đầu tiên của mỗi tháng.
4. Xây dựng quy trình dọn dẹp dữ liệu cũ (Retention Workflow): Tách phân vùng cũ hơn 12 tháng bằng `ALTER TABLE events DETACH PARTITION events_y2025m01 CONCURRENTLY;`.
5. Đóng gói bảng đã tách vào kho lưu trữ lạnh (Cold Storage / Parquet trên S3) hoặc xóa bảng bằng `DROP TABLE events_y2025m01;`.
6. Kiểm tra kế hoạch truy vấn bằng `EXPLAIN (ANALYZE)` để khẳng định Partition Pruning hoạt động chính xác.

## 7. Concrete Examples
### Tạo cấu trúc Declarative Partitioning và tách bảng con không downtime:
```sql
-- 1. Tao bang cha phan vung theo thang
CREATE TABLE public.audit_logs (
    id bigint GENERATED ALWAYS AS IDENTITY,
    tenant_id uuid NOT NULL,
    action varchar(64) NOT NULL,
    created_at timestamptz NOT NULL,
    PRIMARY KEY (id, created_at) -- Partition key phai nam trong Primary Key
) PARTITION BY RANGE (created_at);

-- 2. Tao bang con cho thang hien tai
CREATE TABLE public.audit_logs_y2026m10 PARTITION OF public.audit_logs
FOR VALUES FROM ('2026-10-01 00:00:00+00') TO ('2026-11-01 00:00:00+00');

-- 3. Tach phan vung cu khong gay gian doan dich vu (Zero Downtime)
ALTER TABLE public.audit_logs 
DETACH PARTITION public.audit_logs_y2025m01 CONCURRENTLY;

-- 4. Xoa bang da tach ngay lap tuc ma khong gay lock bang cha
DROP TABLE IF EXISTS public.audit_logs_y2025m01;
```

## 8. Anti-Patterns & Common Traps
- **Missing Future Partitions:** Quên tạo trước bảng con cho tháng tiếp theo, khiến ứng dụng ném lỗi `no partition of relation ... found for row` ngay thời khắc bước sang tháng mới.
- **Non-Concurrently Detaching Large Partitions:** Chạy `ALTER TABLE DETACH PARTITION` thông thường, chiếm khóa độc quyền và làm nghẽn toàn bộ truy vấn trên bảng cha.
- **Primary Key Without Partition Key:** Cố gắng tạo khóa chính chỉ trên cột `id` mà không đưa cột phân vùng vào, khiến PostgreSQL từ chối tạo bảng.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Luôn có sẵn ít nhất 2 phân vùng tương lai được tạo trước thời hạn.
- **QG-02**: Mọi thao tác tách phân vùng trên hệ thống sản xuất đều sử dụng mệnh đề `CONCURRENTLY`.
- **QG-03**: Kế hoạch thực thi `EXPLAIN` trên các truy vấn lọc theo ngày chứng minh chỉ có phân vùng liên quan được quét (`Partition Pruning: SUCCESS`).

## 10. Security & Safety Boundaries
- Bảo đảm an toàn toàn vẹn dữ liệu lịch sử và tuân thủ các quy định pháp lý về thời hạn lưu trữ dữ liệu (GDPR/HIPAA Data Retention).

## 11. Platform Adapters
- **Extensions**: pg_partman, pg_cron, TimescaleDB, AWS RDS Postgres, Supabase Database Extensions.

## 12. Deliverables & Output Artifacts
- Lược đồ DDL bảng phân vùng chuẩn tắc (`partitioned_schema.sql`).
- Hàm tự động hóa tạo phân vùng định kỳ (`create_monthly_partitions.sql`).
- Quy trình kiểm tra và lưu trữ dữ liệu hết hạn (`retention_cleanup.sh`).

## 13. Related & Complementary Skills
dex-database-engineering, dex-postgres-migration-lock-budget, dex-database-query-plans

## 14. Realistic Usage Example
```bash
# Kiem tra danh sach cac phan vung hien co cua bang audit_logs
psql "$DATABASE_URL" -c "SELECT inhrelid::regclass AS partition_name FROM pg_inherits WHERE inhparent = 'public.audit_logs'::regclass;"

# Chay job tu dong tao phan vung cho quy tiep theo
psql "$DATABASE_URL" -c "SELECT create_future_partitions('public.audit_logs', 3);"
```
