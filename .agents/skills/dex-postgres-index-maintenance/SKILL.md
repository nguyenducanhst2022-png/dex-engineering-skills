---
name: dex-postgres-index-maintenance
description: Inspect, diagnose, and maintain PostgreSQL indexes. Detect unused and duplicate indexes, monitor B-tree bloat, rebuild corrupted indexes concurrently, and optimize composite index column ordering. Use when tuning query performance and reclaiming disk storage.
---

# dex-postgres-index-maintenance

## 1. Purpose & Scope
Kiểm toán, chẩn đoán và duy trì hiệu năng của hệ thống chỉ mục (Indexes) trong PostgreSQL; phát hiện các chỉ mục không bao giờ được sử dụng (Unused Indexes) làm chậm thao tác ghi, loại bỏ chỉ mục trùng lặp (Duplicate Indexes), phát hiện và xử lý hiện tượng phình to chỉ mục (Index Bloat) bằng `REINDEX CONCURRENTLY`, và chuẩn hóa thứ tự các cột trong composite index.

## 2. When to Use
- Khi dung lượng đĩa của cơ sở dữ liệu tăng nhanh bất thường do chỉ mục chiếm tỷ trọng lớn hơn cả dữ liệu bảng.
- Khi tốc độ các câu lệnh `INSERT`, `UPDATE`, `DELETE` bị suy giảm nghiêm trọng do phải cập nhật quá nhiều chỉ mục dư thừa.
- Khi cần rà soát định kỳ hàng quý sức khỏe hệ thống chỉ mục trên PostgreSQL sản xuất.

## 3. When NOT to Use
- Khi bảng dữ liệu có dưới 1,000 bản ghi (PostgreSQL thường chọn quét tuần tự Sequential Scan thay vì dùng index).
- Khi vấn đề nằm ở cấu trúc câu truy vấn logic phức tạp cần tối ưu hóa tầng thuật toán (chuyển sang `dex-database-query-plans`).

## 4. Prerequisites & Input Context
- **Quyền hạn truy cập:** Quyền đọc các bảng view thống kê hệ thống: `pg_stat_user_indexes`, `pg_statio_user_indexes`, `pg_index`.
- **Dung lượng đĩa khả dụng:** Ít nhất 1.5 lần kích thước của chỉ mục cần rebuild để thực thi `REINDEX CONCURRENTLY`.

## 5. Core Concepts & Taxonomy
- **Unused Indexes (`idx_scan = 0`):** Các chỉ mục được tạo ra nhưng trình tối ưu hóa truy vấn của Postgres không bao giờ lựa chọn trong suốt thời gian hệ thống hoạt động; gây lãng phí RAM buffer cache và làm chậm thao tác ghi.
- **Index Bloat:** Hiện tượng các trang đĩa B-tree bị phân mảnh do thao tác xóa hoặc cập nhật bản ghi liên tục, khiến chỉ mục chiếm dung lượng gấp 3-5 lần kích thước thực tế.
- **REINDEX CONCURRENTLY:** Tái tạo lại cấu trúc chỉ mục trong nền mà không khóa các câu lệnh đọc và ghi trên bảng gốc.

## 6. Step-by-Step Execution Workflow
1. Chạy truy vấn thống kê từ `pg_stat_user_indexes` để liệt kê toàn bộ các chỉ mục có `idx_scan = 0` hoặc số lần scan không đáng kể sau thời gian dài tích lũy số liệu.
2. Kiểm tra chỉ mục trùng lặp: Xác định các chỉ mục là tập con của chỉ mục composite khác (ví dụ: có index `(a, b)` thì index đơn `(a)` là dư thừa).
3. Ước tính độ phình to (Bloat Estimation) của các B-tree index thông qua tiện ích hoặc công thức thống kê.
4. Soạn thảo lệnh xóa chỉ mục an toàn: Sử dụng `DROP INDEX CONCURRENTLY IF EXISTS index_name;`.
5. Lập lịch tái cấu trúc các chỉ mục bị phình to bằng lệnh `REINDEX INDEX CONCURRENTLY index_name;` trong khung giờ thấp điểm.

## 7. Concrete Examples
### Truy vấn phát hiện chỉ mục dư thừa không được sử dụng:
```sql
SELECT
    schemaname || '.' || relname AS table_name,
    indexrelname AS index_name,
    pg_size_pretty(pg_relation_size(i.indexrelid)) AS index_size,
    idx_scan AS number_of_scans
FROM pg_stat_user_indexes ui
JOIN pg_index i ON ui.indexrelid = i.indexrelid
WHERE NOT i.indisunique -- Khong xoa chi muc rang buoc UNIQUE/PRIMARY
  AND idx_scan = 0
  AND pg_relation_size(i.indexrelid) > 10 * 1024 * 1024 -- Lon hon 10MB
ORDER BY pg_relation_size(i.indexrelid) DESC;
```

## 8. Anti-Patterns & Common Traps
- **Dropping Unique/Primary Key Indexes:** Xóa chỉ mục không sử dụng nhưng vô tình xóa nhầm chỉ mục đang bảo vệ ràng buộc toàn vẹn khóa chính hoặc tính duy nhất của dữ liệu.
- **Reindexing during Peak Traffic without CONCURRENTLY:** Chạy `REINDEX TABLE` thông thường vào giờ cao điểm, khóa hoàn toàn bảng và làm sập ứng dụng.
- **Wrong Column Order in Composite Index:** Đặt cột có độ phân biệt thấp (Low Cardinality) lên đầu composite index thay vì cột có độ lọc cao thường xuyên xuất hiện trong mệnh đề WHERE.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Tuyệt đối không xóa bất kỳ chỉ mục nào có cờ `indisunique = true` hoặc `indisprimary = true`.
- **QG-02**: Mọi thao tác tạo, xóa, hoặc rebuild chỉ mục trên môi trường sản xuất bắt buộc phải sử dụng từ khóa `CONCURRENTLY`.
- **QG-03**: Giải phóng ít nhất 15% dung lượng lưu trữ chỉ mục sau các đợt dọn dẹp bảo trì định kỳ.

## 10. Security & Safety Boundaries
- Ngăn chặn cạn kiệt tài nguyên đĩa máy chủ (Disk Full Outage) và giảm thiểu rủi ro nghẽn I/O hệ thống lưu trữ.

## 11. Platform Adapters
- **Engines**: PostgreSQL 12+, pg_repack, pgbadger, Supabase Index Advisor, Datadog Database Monitoring.

## 12. Deliverables & Output Artifacts
- Báo cáo danh sách chỉ mục không sử dụng và trùng lặp kèm dung lượng lãng phí.
- Tệp kịch bản dọn dẹp và rebuild chỉ mục an toàn (`reindex_maintenance.sql`).
- Biểu đồ theo dõi tỷ lệ hit cache của chỉ mục trước và sau khi tối ưu.

## 13. Related & Complementary Skills
dex-database-query-plans, dex-database-engineering, dex-postgres-vacuum-bloat-diagnostics

## 14. Realistic Usage Example
```bash
# Quet va lap bao cao chi muc thua tren database san xuat
psql "$DATABASE_URL" -f scripts/sql/find_unused_indexes.sql

# Thuc hien reindex concurrently cho bang orders
psql "$DATABASE_URL" -c "REINDEX TABLE CONCURRENTLY public.orders;"
```
