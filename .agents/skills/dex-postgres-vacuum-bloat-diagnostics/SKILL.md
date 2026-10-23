---
name: dex-postgres-vacuum-bloat-diagnostics
description: Analyze, diagnose, and mitigate PostgreSQL table and index bloat. Configure proactive autovacuum parameters, detect dead-tuple accumulation, inspect transaction wraparound risks, and safely reclaim storage without locking. Use when database size outpaces actual data volume.
---

# dex-postgres-vacuum-bloat-diagnostics

## 1. Purpose & Scope
Chẩn đoán, đo lường và triệt tiêu hiện tượng phình to dữ liệu (Bloat) trên bảng và chỉ mục trong PostgreSQL; tinh chỉnh các tham số autovacuum chủ động theo từng bảng lớn; phát hiện các giao dịch chạy dài (Long-Running Transactions) ngăn cản dọn dẹp bản ghi chết (Dead Tuples); giám sát rủi ro đóng băng transaction ID (Transaction ID Wraparound); và thu hồi dung lượng lưu trữ an toàn.

## 2. When to Use
- Khi dung lượng bảng tăng gấp nhiều lần nhưng số lượng bản ghi thực tế không đổi sau các đợt UPDATE hoặc DELETE ồ ạt.
- Khi autovacuum mặc định của Postgres chạy quá chậm, không theo kịp tốc độ sinh bản ghi chết của ứng dụng.
- Khi nhận được cảnh báo nguy hiểm về Transaction ID Wraparound (`WARNING: database must be vacuumed within...`).

## 3. When NOT to Use
- Khi cơ sở dữ liệu chủ yếu là dữ liệu chỉ đọc (Read-Only Data Warehouse) ít phát sinh thao tác sửa xóa.
- Khi hệ thống đang gặp sự cố nghẽn CPU hoặc I/O do ứng dụng gây ra mà nguyên nhân không xuất phát từ dead tuples.

## 4. Prerequisites & Input Context
- **Quyền quản trị:** Quyền đọc `pg_stat_user_tables`, `pg_stat_activity`, và thực thi lệnh `VACUUM`.
- **Thông tin cấu hình:** Các tham số `autovacuum_vacuum_scale_factor`, `autovacuum_vacuum_cost_limit`, `autovacuum_max_workers`.

## 5. Core Concepts & Taxonomy
- **Dead Tuples (MVCC Ghost Records):** Khi bản ghi bị cập nhật hoặc xóa trong kiến trúc MVCC của Postgres, bản ghi cũ không bị xóa vật lý ngay mà được đánh dấu là dead tuple để phục vụ các transaction khác đang đọc; chỉ khi không còn ai đọc thì VACUUM mới có thể giải phóng không gian này.
- **Autovacuum Scale Factor:** Tỷ lệ phần trăm số bản ghi chết trên tổng số bản ghi cần tích lũy trước khi autovacuum kích hoạt (mặc định 20%, quá lớn đối với các bảng hàng chục triệu hàng).
- **Long-Running Transactions:** Một transaction mở quên commit/rollback (hoặc một uncommitted prepared transaction) sẽ chặn VACUUM dọn dẹp toàn bộ dead tuple sinh ra sau nó trong toàn bộ database.

## 6. Step-by-Step Execution Workflow
1. Chạy truy vấn chẩn đoán dead tuples và bloat ratio trên toàn bộ các bảng người dùng thông qua `pg_stat_user_tables`.
2. Kiểm tra xem có giao dịch chạy dài nào đang giữ `backend_xmin` hay không bằng cách quét `pg_stat_activity`.
3. Hủy bỏ hoặc cảnh báo các kết nối chạy quá 15 phút không hoàn thành.
4. Tinh chỉnh autovacuum chuyên biệt cho từng bảng lớn có mật độ ghi cao: Giảm `autovacuum_vacuum_scale_factor` từ `0.2` xuống `0.02` hoặc `0.05` và tăng `autovacuum_cost_limit`.
5. Chạy lệnh `VACUUM (ANALYZE, VERBOSE) table_name;` thủ công ngoài giờ cao điểm để dọn dẹp dead tuples.
6. Nếu bảng bị phình to nghiêm trọng trên 50%, áp dụng `pg_repack` để sắp xếp lại dữ liệu vật lý mà không khóa bảng.

## 7. Concrete Examples
### Cấu hình autovacuum chuyên biệt cho bảng đơn hàng có tần suất cập nhật cao:
```sql
-- Giam nguong kich hoat xuong 2% (thay vi mac dinh 20%)
ALTER TABLE public.orders SET (
    autovacuum_vacuum_scale_factor = 0.02,
    autovacuum_vacuum_threshold = 1000,
    autovacuum_vacuum_cost_limit = 2000,
    autovacuum_vacuum_cost_delay = 2
);

-- Kiem tra danh sach cac transaction chay dai dang chan VACUUM
SELECT
    pid,
    now() - xact_start AS duration,
    query,
    state
FROM pg_stat_activity
WHERE state != 'idle'
  AND (now() - xact_start) > interval '10 minutes'
ORDER BY duration DESC;
```

## 8. Anti-Patterns & Common Traps
- **Running VACUUM FULL in Production:** Lệnh `VACUUM FULL` chiếm khóa `ACCESS EXCLUSIVE`, khóa chặt toàn bộ bảng trong hàng giờ và có thể làm sập toàn bộ hệ thống dịch vụ trực tuyến.
- **Disabling Autovacuum Entirely:** Tắt autovacuum để tăng tốc độ ghi tạm thời, dẫn đến bảng phình to gấp 10 lần và hệ thống đối mặt với thảm họa Transaction Wraparound Shutdown.
- **Leaving Uncommitted Open Transactions:** Mở transaction trên client và không đóng kết nối, khiến toàn bộ tiến trình dọn rác của PostgreSQL bị đóng băng.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Tỷ lệ dead tuples trên các bảng nghiệp vụ chính không vượt quá 10% tổng số bản ghi.
- **QG-02**: Tuyệt đối cấm sử dụng `VACUUM FULL` trên môi trường sản xuất; thay thế bằng `pg_repack` hoặc `VACUUM` thông thường.
- **QG-03**: Khoảng cách transaction age đến giới hạn wraparound (`2^31`) luôn được duy trì ở mức an toàn dưới 100 triệu transactions.

## 10. Security & Safety Boundaries
- Bảo vệ cơ sở dữ liệu khỏi nguy cơ buộc phải ngừng hoạt động khẩn cấp (Emergency Autovacuum Wraparound Shutdown).

## 11. Platform Adapters
- **Tools**: pg_stat_user_tables, pg_repack, pg_bloat_check, Supabase Storage Optimizer, AWS RDS Performance Insights.

## 12. Deliverables & Output Artifacts
- Báo cáo chẩn đoán tỷ lệ phình to bảng và chỉ mục (`bloat_report.md`).
- Tệp cấu hình autovacuum tối ưu hóa cho từng bảng lõi (`autovacuum_tuning.sql`).
- Script tự động ngắt kết nối các long-running idle transactions.

## 13. Related & Complementary Skills
dex-postgres-index-maintenance, dex-database-engineering, dex-reliability-engineering

## 14. Realistic Usage Example
```bash
# Kiem tra dead tuples va trang thai autovacuum bang script
psql "$DATABASE_URL" -c "SELECT relname, n_dead_tup, last_vacuum, last_autovacuum FROM pg_stat_user_tables ORDER BY n_dead_tup DESC LIMIT 10;"

# Chay vacuum thu cong tren bang lon
psql "$DATABASE_URL" -c "VACUUM (ANALYZE, VERBOSE) public.orders;"
```
