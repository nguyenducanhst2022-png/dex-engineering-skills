---
name: dex-metric-cardinality-control
description: Audit, manage, and prevent metric cardinality explosions in Prometheus and Datadog by enforcing label budgets, drop rules, and recording rules. Use when monitoring infrastructure costs surge or TSDB nodes crash.
---

# dex-metric-cardinality-control

## 1. Purpose & Scope
Kiểm toán, quản lý và ngăn ngừa thảm họa bùng nổ số chiều metric (Metric Cardinality Explosion) trong hệ thống giám sát (Prometheus, Cortex, M3DB, Datadog); thiết lập ngân sách nhãn (Label Budget), loại bỏ các nhãn có giá trị vô hạn (UUID, email, IP) và tối ưu hóa chi phí giám sát.

## 2. When to Use
- Cụm Prometheus bị sập liên tục do lỗi OOM (Out Of Memory) khi quét dữ liệu time-series.
- Hóa đơn chi phí Datadog/NewRelic tăng vọt hàng chục ngàn USD do số lượng custom metrics bùng nổ.
- Tốc độ tải dashboard Grafana bị chậm chạp nghiêm trọng (>10s cho mỗi query).

## 3. When NOT to Use
- Không loại bỏ các nhãn định danh cần thiết cho việc phân loại SLO cốt lõi (như `status_code`, `method`, `service`).
- Không dùng metrics để lưu trữ các dữ liệu mang tính sự kiện giao dịch (hãy dùng Distributed Tracing hoặc Logs).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Báo cáo thống kê TSDB status (Prometheus `/api/v1/status/tsdb`).
- Danh sách các metric có số lượng time-series lớn nhất.
- Cấu hình Prometheus scrape configs hoặc OpenTelemetry collector.
- **Điều kiện tiên quyết**:
- Có quyền truy cập vào giao diện quản trị Prometheus hoặc API giám sát hạ tầng.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Cardinality: Tổng số time-series duy nhất được tính bằng tích số các giá trị khả dĩ của tất cả các nhãn (Labels). Ví dụ: `http_requests_total{method="5", path="100", user_id="1,000,000"}` tạo ra 500 triệu chuỗi thời gian, làm sập bất kỳ TSDB nào.
- Bounded Labels: Chỉ sử dụng các nhãn có tập giá trị hữu hạn và nhỏ (ví dụ: HTTP status: 200, 400, 500; Region: us-east, ap-southeast).
- Metric Relabeling: Cơ chế cắt bỏ nhãn xấu (drop label) ngay tại tầng thu thập dữ liệu.
- **Quy tắc quyết định kỹ thuật**:
- Tuyệt đối cấm đưa `user_id`, `email`, `order_id`, `ip_address` vào làm nhãn của Prometheus metric.
- Bất kỳ metric nào sinh ra > 10,000 active series mà không có sự phê duyệt của SRE phải bị drop tại collector.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Một lập trình viên đưa URL raw có chứa dynamic ID (`/users/123e4567-e89b-12d3`) vào label `path` thay vì URL template (`/users/:id`), khiến Prometheus chết ngắc sau 10 phút.

## 6. Step-by-Step Execution Workflow
1. Truy vấn endpoint `/api/v1/status/tsdb` của Prometheus để tìm Top 10 metric có số series cao nhất.
2. Phân tích nguyên nhân: xác định label nào có cardinality cao bất thường.
3. Cập nhật mã nguồn ứng dụng để chuẩn hóa label (dùng route pattern thay vì raw path).
4. Cấu hình `metric_relabel_configs` tại Prometheus/Otel Collector để drop các nhãn vi phạm.
5. Áp dụng Recording Rules để tính toán trước các chỉ số tổng hợp, giảm tải cho Grafana.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```yaml
# Prometheus scrape config relabeling to drop dangerous high-cardinality labels
scrape_configs:
  - job_name: 'api-service'
    static_configs:
      - targets: ['localhost:8080']
    metric_relabel_configs:
      - regex: '(user_id|session_token|email)'
        action: labeldrop
      - source_labels: [__name__]
        regex: 'unwanted_debug_metric_.*'
        action: drop
```

### Lệnh xác minh & thực thi:
```bash
# Truy vấn top metrics có nhiều chuỗi thời gian nhất trên Prometheus
curl -s http://localhost:9090/api/v1/status/tsdb | jq '.data.seriesCountByMetricName[:10]'
```

## 8. Anti-Patterns & Common Traps
- Gắn `timestamp` hoặc `hash` vào metric label.
- Không thiết lập giới hạn `sample_limit` cho scrape job trong Prometheus.

## 9. Quality Gates & Acceptance Criteria
- Giữ tổng số active time-series trên toàn cụm Prometheus trong ngân sách kiểm soát (< 1 triệu series/node).
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Loại bỏ các nhãn có thể vô tình làm lộ thông tin định danh cá nhân (PII) ra giao diện dashboard.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ thống hỗ trợ**: Linux (CI/CD runners), macOS, Windows 11 PowerShell/WSL2.

## 12. Deliverables & Output Artifacts
- Báo cáo kiểm toán Cardinality và danh sách nhãn đã dọn dẹp.
- File cấu hình `relabel_configs` và Recording Rules chuẩn hóa.

## 13. Related & Complementary Skills
dex-alert-quality-engineering, dex-log-pipeline-design, dex-distributed-tracing

## 14. Realistic Usage Example
### Tình huống thực tế:
Một công ty công nghệ bị Prometheus OOM liên tục vào giờ cao điểm. Nhờ kiểm toán TSDB, họ phát hiện thư viện HTTP client tự động thêm header `User-Agent` của từng điện thoại khách hàng vào label của metric. Xóa bỏ label này lập tức giảm số series từ 2.4 triệu xuống còn 45,000, cứu sống hệ thống monitoring.
