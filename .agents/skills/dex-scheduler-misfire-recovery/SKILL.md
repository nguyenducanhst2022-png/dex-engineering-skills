---
name: dex-scheduler-misfire-recovery
description: Diagnose missed distributed scheduler triggers, engineer catch-up recovery policies, and enforce leader election concurrency safeguards. Use when running mission-critical periodic jobs or financial reconciliation schedules.
---

# dex-scheduler-misfire-recovery

## 1. Purpose & Scope
Chẩn đoán và khắc phục sự cố lịch trình phân tán bị trượt lượt chạy (Scheduler Misfire); thiết lập các chính sách bù đắp (catch-up / backfill policies) có kiểm soát, ngăn chặn hiện tượng chạy bão lặp lại sau sự cố, và bảo đảm tính độc quyền thực thi lịch trình qua cơ chế Leader Election.

## 2. When to Use
- Khi hệ thống lập lịch định kỳ (Cron, Quartz, Celery Beat, CloudWatch Events) bị trễ hoặc bỏ lỡ thời điểm kích hoạt do quá tải hoặc sập máy chủ.
- Khi vận hành các tác vụ định kỳ tối quan trọng như chốt sổ tài chính hàng đêm, tạo hóa đơn tự động định kỳ hàng tháng.
- Khi triển khai cụm scheduler dự phòng nhiều node (High Availability) cần bảo đảm chỉ có đúng một node được quyền kích hoạt job.

## 3. When NOT to Use
- Khi tác vụ chỉ là việc dọn dẹp bộ nhớ đệm tạm thời cho phép bỏ qua nếu bị trượt lượt.
- Khi tác vụ được kích hoạt theo luồng sự kiện thời gian thực (Event-Driven) thay vì dựa trên đồng hồ thời gian.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Biểu thức Cron, bảng ghi nhận lịch sử thực thi (`job_executions`), chính sách xử lý trượt lịch (Fire Now, Ignore, Catch-up All).
- **Quyền hạn truy cập:** Quyền cấu hình hệ thống scheduler và bảng metadata trạng thái job.

## 5. Core Concepts & Taxonomy
- **Misfire Instruction:** Quy tắc xác định hành vi cần làm khi thời điểm kích hoạt của job bị bỏ lỡ quá ngưỡng chịu đựng (misfire threshold).
- **Catch-Up Policy:** Quyết định thực thi bù: chạy bù tất cả các lượt đã mất (Run all missed), gộp lại thành một lượt duy nhất (Coalesce into single run), hoặc bỏ qua chờ lượt tiếp theo (Ignore).
- **Idempotent Job Run:** Mỗi lượt thực thi định kỳ mang một `scheduled_tick_time` duy nhất; nếu lượt đó đã được ghi nhận hoàn thành thì không được chạy lại.

## 6. Step-by-Step Execution Workflow
1. Khảo sát danh mục toàn bộ cron jobs và phân loại mức độ quan trọng cùng chính sách misfire tương ứng.
2. Thiết lập bảng lưu vết lịch sử kích hoạt (`job_execution_history`) lưu giữ `job_name`, `scheduled_at`, `status`, `started_at`, `finished_at`.
3. Cài đặt cơ chế Leader Election sử dụng lease/lock phân tán để bảo đảm chỉ có 1 node scheduler duy nhất đóng vai trò active coordinator.
4. Xây dựng logic phát hiện misfire: khi scheduler khởi động lại, so sánh thời điểm chạy dự kiến gần nhất với thời gian hiện tại.
5. Áp dụng chính sách bù đắp: nếu là tác vụ tài chính thì chạy bù tuần tự từng khoảng thời gian bị lỡ; nếu là tác vụ tổng hợp dữ liệu thì chạy gộp một lần duy nhất.
6. Ghi log kiểm toán và bắn cảnh báo về số lượng lượt chạy bị misfire đã được xử lý.

## 7. Concrete Examples
### Ví dụ cấu hình chính sách Misfire và bảng theo dõi trong SQL:
```sql
CREATE TABLE scheduled_job_runs (
    job_name VARCHAR(100) NOT NULL,
    expected_tick TIMESTAMPTZ NOT NULL,
    status VARCHAR(20) NOT NULL, -- PENDING, RUNNING, COMPLETED, MISFIRED
    node_id VARCHAR(100),
    executed_at TIMESTAMPTZ,
    PRIMARY KEY (job_name, expected_tick)
);

-- Khi scheduler kích hoạt: Thử chiếm quyền chạy cho lượt expected_tick cụ thể
INSERT INTO scheduled_job_runs (job_name, expected_tick, status, node_id, executed_at)
VALUES ('generate_nightly_invoices', '2026-10-22 00:00:00Z', 'RUNNING', 'node-prod-01', NOW())
ON CONFLICT (job_name, expected_tick) DO NOTHING;
-- Nếu INSERT thành công (rows affected = 1) -> Node được phép chạy job!
```

## 8. Anti-Patterns & Common Traps
- **Misfire Stampede:** Máy chủ bị sập 10 ngày, khi bật lại lập tức kích hoạt 10,000 lượt chạy bù cùng một giây làm sập toàn bộ hệ thống cơ sở dữ liệu.
- **Silent Dropping:** Scheduler bị treo trong đêm khiến không có bất kỳ báo cáo tài chính nào được tạo ra nhưng sáng hôm sau không ai nhận được cảnh báo.
- **Multiple Leader Dual Execution:** Hai node scheduler cùng tưởng mình là leader và kích hoạt gửi hai lần email sao kê cho toàn bộ khách hàng.

## 9. Quality Gates & Acceptance Criteria
- **QG-03**: Hệ thống có khả năng tự động phát hiện và chạy bù lượt misfire theo đúng chính sách đã cấu hình.
- **QG-09**: Không có bất kỳ khoảng thời gian scheduled tick nào bị thực thi hai lần do xung đột giữa các nodes.
- **QG-10**: Leader election chuyển giao quyền kích hoạt lịch trình sang node dự phòng trong dưới 15 giây khi node chính gặp sự cố.

## 10. Security & Safety Boundaries
- Ngăn ngừa việc can thiệp trái phép vào bảng lịch trình để kích hoạt các job nhạy cảm ngoài giờ quy định.
- Phân quyền tối thiểu cho tiến trình scheduler chỉ được gọi các endpoint đã được chứng thực.

## 11. Platform Adapters
- **Python**: APScheduler, Celery Beat with RedBeat.
- **Java**: Quartz Scheduler with JDBC JobStore.
- **Go**: gocron, robfig/cron with distributed locks.

## 12. Deliverables & Output Artifacts
- Module quản lý chính sách Scheduler Misfire Recovery.
- Bảng schema lưu vết lịch sử thực thi các lượt chạy định kỳ.
- Kịch bản kiểm thử giả lập mất điện server scheduler và kiểm tra quá trình chạy bù.

## 13. Related & Complementary Skills
dex-background-job-queues, dex-distributed-lock-lease-safety, dex-clock-skew-resilience

## 14. Realistic Usage Example
```powershell
# Kiểm tra lịch sử thực thi và các job bị misfire trong 24 giờ qua
python scripts/scheduler_health.py --check-misfires --window 24h
```
