---
name: dex-cqrs-projection-management
description: Manage asynchronous read-model projections in CQRS architectures with replay safety, eventual consistency lag monitoring, and zero-downtime projection rebuilds. Use when scaling complex reporting queries or separating read/write models.
---

# dex-cqrs-projection-management

## 1. Purpose & Scope
Quản lý vòng đời và tính toàn vẹn của các Read-Model Projections trong kiến trúc CQRS; thiết lập quy trình tính toán lại (replay/rebuild) hình chiếu dữ liệu mà không làm gián đoạn hệ thống, kiểm soát độ trễ nhất quán cuối cùng (eventual consistency lag).

## 2. When to Use
- Khi mô hình ghi (Write Model/Command) có cấu trúc nghiệp vụ phức tạp không tối ưu cho các câu truy vấn báo cáo, tìm kiếm hoặc hiển thị dashboard.
- Khi cần hỗ trợ nhiều dạng hiển thị khác nhau từ cùng một nguồn dữ liệu sự kiện (Event Store).
- Khi cần xây dựng lại toàn bộ read model sau khi thay đổi schema hoặc bổ sung tính năng mới.

## 3. When NOT to Use
- Khi ứng dụng CRUD đơn giản, lưu lượng đọc và ghi cân bằng trên cùng một mô hình dữ liệu.
- Khi hệ thống bắt buộc tính nhất quán tức thời (Strong Immediate Consistency) tại mọi điểm truy vấn.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Nguồn sự kiện nghiệp vụ (Domain Events stream), cơ sở dữ liệu read-model (PostgreSQL, Elasticsearch, Redis), cơ chế theo dõi offset.
- **Quyền hạn truy cập:** Quyền tạo/xóa bảng view và đăng ký consumer trên event stream.

## 5. Core Concepts & Taxonomy
- **Projection / Read Model:** Bảng biểu dữ liệu được tối ưu hóa riêng cho truy vấn đọc (denormalized data), được cập nhật bất đồng bộ từ các sự kiện.
- **Projection Versioning & Blue-Green Rebuild:** Tạo bảng projection mới (`orders_view_v2`), nạp lại dữ liệu từ đầu, sau đó tráo đổi alias mà không gián đoạn dịch vụ.
- **Catch-up Lag:** Khoảng cách thời gian hoặc số lượng sự kiện giữa vị trí mới nhất của Event Store và vị trí đã chiếu của Read Model.

## 6. Step-by-Step Execution Workflow
1. Thiết kế bảng projection tối ưu hóa cho các truy vấn đọc cụ thể với đầy đủ index cần thiết.
2. Đăng ký projection handler xử lý các sự kiện tương ứng kèm cơ chế cập nhật idempotent dựa trên `event_id` hoặc sequence number.
3. Thiết lập bảng lưu vết vị trí xử lý (`projection_checkpoints`) lưu giữ offset sự kiện gần nhất đã áp dụng thành công.
4. Xây dựng công cụ Rebuild Projections cho phép nạp lại sự kiện lịch sử vào bảng tạm mới theo cơ chế Blue-Green.
5. Giám sát độ trễ chiếu dữ liệu (Projection Lag) qua Prometheus metrics và cảnh báo khi lag vượt ngưỡng an toàn.

## 7. Concrete Examples
### Ví dụ triển khai Projection Handler có kiểm tra idempotency trong SQL:
```sql
-- Cập nhật read-model an toàn và idempotent từ Domain Event
INSERT INTO order_summary_projection (
    order_id, customer_id, total_amount, order_status, last_event_id, updated_at
) VALUES (
    $1, $2, $3, 'CREATED', $4, NOW()
)
ON CONFLICT (order_id) DO UPDATE SET
    order_status = CASE 
        WHEN EXCLUDED.last_event_id > order_summary_projection.last_event_id 
        THEN EXCLUDED.order_status 
        ELSE order_summary_projection.order_status 
    END,
    total_amount = EXCLUDED.total_amount,
    last_event_id = GREATEST(order_summary_projection.last_event_id, EXCLUDED.last_event_id),
    updated_at = NOW()
WHERE EXCLUDED.last_event_id >= order_summary_projection.last_event_id;
```

## 8. Anti-Patterns & Common Traps
- **Direct Read-Model Mutation:** Tự ý cập nhật bảng read-model từ các API bên ngoài thay vì lắng nghe sự kiện từ Command Model.
- **Blocking Command on Projection:** Chờ đợi read-model được cập nhật xong mới trả về phản hồi cho API ghi (phá vỡ lợi ích bất đồng bộ của CQRS).
- **Ignoring Out-of-Order Events:** Áp dụng sự kiện cũ đè lên dữ liệu mới hơn do thông điệp bị đến lệch thứ tự qua mạng.

## 9. Quality Gates & Acceptance Criteria
- **QG-04**: Có kiểm thử xác nhận khả năng chiếu lại (replay) 10,000 sự kiện tạo ra kết quả giống hệt dữ liệu ban đầu.
- **QG-07**: Thời gian xử lý một sự kiện trong projection handler dưới 10ms.
- **QG-10**: Có cơ chế tự động khôi phục từ checkpoint khi worker bị tắt đột ngột.

## 10. Security & Safety Boundaries
- Áp dụng phân quyền người dùng (Role-Based Access Control) ngay tại tầng đọc projection.
- Loại bỏ các trường thông tin nhạy cảm (như mật khẩu băm, token) trước khi đưa vào bảng read-model công khai.

## 11. Platform Adapters
- **Event Store**: Kafka, Debezium, EventStoreDB.
- **Read Storage**: PostgreSQL Read Replicas, Redis, Elasticsearch.

## 12. Deliverables & Output Artifacts
- Mã nguồn các Projection Handlers.
- Kịch bản Blue-Green Rebuild tự động.
- Dashboard giám sát Projection Lag trên Grafana.

## 13. Related & Complementary Skills
dex-event-driven-architecture, dex-database-query-plans, dex-data-contracts

## 14. Realistic Usage Example
```powershell
# Chạy script rebuild projection sang bảng mới
python scripts/rebuild_projection.py --projection order_summary --version v2

# Kiểm tra độ trễ (lag) của các projections hiện hành
python scripts/check_projection_lag.py
```
