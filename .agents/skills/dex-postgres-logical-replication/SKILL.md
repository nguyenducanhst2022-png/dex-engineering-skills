---
name: dex-postgres-logical-replication
description: Architect, configure, and monitor PostgreSQL logical replication. Manage publications, subscriptions, replication slots, lag metrics, and conflict resolution. Use when building read replicas, cross-region replication, or real-time event streaming pipelines.
---

# dex-postgres-logical-replication

## 1. Purpose & Scope
Thiết kế, thiết lập cấu hình và giám sát hệ thống sao chép logic (Logical Replication) trong PostgreSQL; quản lý vòng đời của Publications, Subscriptions và Replication Slots; theo dõi độ trễ sao chép (Replication Lag); ngăn chặn nguy cơ tràn ổ đĩa do tích tụ Write-Ahead Logging (WAL); và xử lý xung đột dữ liệu (Conflict Resolution).

## 2. When to Use
- Khi cần sao chép một phần bảng dữ liệu sang cơ sở dữ liệu phân tích (Analytics/Warehouse) theo thời gian thực.
- Khi thực hiện nâng cấp phiên bản PostgreSQL lớn (Major Version Upgrade) với thời gian downtime tiệm cận bằng 0.
- Khi tích hợp đường ống truyền phát sự kiện Change Data Capture (CDC) với Kafka hoặc Debezium.

## 3. When NOT to Use
- Khi cần sao chép toàn bộ cụm CSDL nguyên trạng bao gồm cả bảng tạm, chỉ mục, và cấu hình người dùng (nên dùng Physical Streaming Replication).
- Khi ứng dụng đòi hỏi sao chép các thao tác DDL tự động (Logical Replication chuẩn của Postgres chỉ sao chép DML: INSERT, UPDATE, DELETE).

## 4. Prerequisites & Input Context
- **Cấu hình máy chủ nguồn (Publisher):** `wal_level = logical`, `max_replication_slots >= 4`, `max_wal_senders >= 4`.
- **Định danh bản ghi:** Tất cả các bảng tham gia sao chép phải có Primary Key hoặc `REPLICA IDENTITY FULL`.

## 5. Core Concepts & Taxonomy
- **Replication Slot:** Cơ chế giữ chân các phân đoạn tệp WAL trên Publisher cho tới khi Subscriber xác nhận đã nhận và áp dụng dữ liệu an toàn.
- **Slot Invalidation & Disk Overflow:** Nếu Subscriber bị treo hoặc mạng ngắt kết nối kéo dài, Publisher sẽ không bao giờ xóa WAL cho slot đó, dẫn đến ổ đĩa Publisher bị đầy 100% và làm tê liệt toàn bộ database.
- **Replica Identity:** Cấu hình quyết định PostgreSQL sẽ ghi thông tin gì vào WAL khi có thao tác `UPDATE` hoặc `DELETE` (mặc định chỉ ghi Primary Key cũ).

## 6. Step-by-Step Execution Workflow
1. Kiểm tra cấu hình `wal_level` trên Publisher và yêu cầu reload nếu chưa bật chế độ `logical`.
2. Tạo Publication trên Publisher: `CREATE PUBLICATION pub_events FOR TABLE users, orders;`.
3. Khởi tạo lược đồ bảng đích (Schema DDL) trên Subscriber khớp với cấu trúc Publisher.
4. Tạo Subscription trên Subscriber: `CREATE SUBSCRIPTION sub_events CONNECTION '...' PUBLICATION pub_events;`.
5. Thiết lập cảnh báo giám sát Replication Slot: Theo dõi số byte WAL đang chờ xử lý từ `pg_replication_slots` và kích hoạt ngắt kết nối hoặc xóa slot nếu vượt quá ngưỡng an toàn (`max_slot_wal_keep_size`).
6. Kiểm chứng luồng sao chép: Chèn dữ liệu mẫu trên Publisher và xác nhận dữ liệu xuất hiện trên Subscriber trong vòng dưới 100ms.

## 7. Concrete Examples
### Giám sát độ trễ và kích thước giữ chân WAL của Replication Slots:
```sql
SELECT
    slot_name,
    plugin,
    active,
    pg_size_pretty(pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn)) AS retained_wal_bytes,
    active_pid,
    wal_status
FROM pg_replication_slots
ORDER BY pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn) DESC;
```

## 8. Anti-Patterns & Common Traps
- **Orphaned Inactive Replication Slots:** Tạo slot để thử nghiệm rồi quên xóa bỏ, khiến Publisher tiếp tục lưu trữ toàn bộ WAL cho đến khi cạn kiệt dung lượng ổ đĩa máy chủ.
- **Replicating Tables without Primary Key:** Sao chép bảng không có khóa chính và cũng không cấu hình `REPLICA IDENTITY FULL`, khiến các lệnh `UPDATE`/`DELETE` trên Subscriber báo lỗi và dừng toàn bộ luồng sao chép.
- **Ignoring Conflict Errors:** Bỏ qua lỗi xung đột khóa chính trên Subscriber, khiến tiến trình replication worker bị crash loop.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Tham số `max_slot_wal_keep_size` bắt buộc phải được cấu hình trên Publisher để chặn nguy cơ tràn đĩa khi subscriber mất kết nối.
- **QG-02**: 100% các bảng nằm trong Publication đều có khóa chính hoặc được gán `REPLICA IDENTITY FULL`.
- **QG-03**: Độ trễ sao chép (Replication Lag) đo lường trong điều kiện tải bình thường phải nhỏ hơn 500ms.

## 10. Security & Safety Boundaries
- Mã hóa đường truyền kết nối sao chép bằng SSL/TLS (`sslmode=verify-full`); cấp quyền tối thiểu bằng role chuyên dụng có quyền `REPLICATION`.

## 11. Platform Adapters
- **Components**: PostgreSQL Built-in Logical Replication, Debezium CDC, AWS DMS, Supabase Realtime CDC, Kafka Connect.

## 12. Deliverables & Output Artifacts
- Tệp kịch bản thiết lập Publication và Subscription an toàn (`logical_replication_setup.sql`).
- Bộ câu lệnh truy vấn giám sát slot lag và dung lượng WAL.
- Kịch bản xử lý sự cố khi subscriber bị mất đồng bộ hoặc xung đột bản ghi.

## 13. Related & Complementary Skills
dex-database-engineering, dex-event-driven-architecture, dex-realtime-protocols

## 14. Realistic Usage Example
```bash
# Kiem tra trang thai logical replication slot tu terminal
psql "$PUBLISHER_URL" -c "SELECT slot_name, active, wal_status FROM pg_replication_slots;"

# Theo doi lag truc tiep tren subscriber
psql "$SUBSCRIBER_URL" -c "SELECT subname, received_lsn, last_msg_receipt_time FROM pg_stat_subscription;"
```
