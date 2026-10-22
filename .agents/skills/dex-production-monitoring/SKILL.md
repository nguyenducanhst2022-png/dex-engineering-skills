---
name: dex-production-monitoring
description: Production observability, structured logging, application health checks, alerting thresholds, error telemetry, and post-deployment stability monitoring. Tracks system health metrics, logs anomalies, and diagnoses live incidents. Use when designing monitoring infrastructure, adding health endpoints, or triaging production alerts.
---

# DEX Production Monitoring

## 1. Purpose
Thiết lập hệ thống quan sát (Observability) toàn diện cho ứng dụng trong môi trường vận hành thực tế thông qua việc chuẩn hóa Logging, cung cấp Health Check endpoints, theo dõi chỉ số sức khỏe hệ thống (Metrics) và phát hiện sớm các sự cố trước khi người dùng kịp phàn nàn.

Quy trình giám sát chuẩn:
`Thu thập Log → Giám sát → Phát hiện lỗi → Cảnh báo → Phân tích → Khắc phục → Kiểm chứng → Ổn định`

Nguyên tắc cốt lõi: **Phần mềm chạy tốt khi vừa phát hành chưa chắc sẽ ổn định lâu dài. Phải liên tục theo dõi để phát hiện và xử lý sự cố kịp thời.**
Ghi nhớ sống còn: **Phần mềm ổn định = Giám sát tốt + Phát hiện sớm + Xử lý nhanh + Ngăn lỗi tái diễn.**

## 2. When to Use
- Khi chuẩn bị đưa ứng dụng vào môi trường Staging hoặc Production.
- Khi cần tích hợp cơ chế Structured Logging (Winston, Pino, Loguru, Zerolog) kèm Correlation ID để truy vết request xuyên suốt.
- Khi xây dựng các endpoint kiểm tra sức khỏe `/healthz`, `/live`, `/ready` phục vụ Kubernetes, Docker swarm hoặc load balancer.
- Khi thiết lập ngưỡng cảnh báo (Alert thresholds) cho tỷ lệ lỗi 5xx, CPU cao hoặc thời gian phản hồi vượt mức cho phép.

## 3. When Not to Use
- Trong môi trường kiểm thử Unit test độc lập không có kết nối dịch vụ ngoài.
- Tùy tiện thêm các câu lệnh log bừa bãi không có cấp độ (`console.log`) làm ô nhiễm hệ thống log.

## 4. Inputs
- Cấu hình logging của ứng dụng.
- Yêu cầu về SLA / SLO của hệ thống (ví dụ: Uptime 99.9%, Latency p95 < 200ms).
- Nền tảng thu thập log và metrics mục tiêu (Prometheus, Grafana, Datadog, Sentry, CloudWatch, OpenTelemetry).

## 5. Workflow

### Bước 1: Chuẩn Hóa Cấu Trúc Log (Structured JSON Logging)
- Chuyển toàn bộ output log sang định dạng JSON có cấu trúc để các hệ thống phân tích (Elasticsearch, Loki) dễ dàng lập chỉ mục:
  - Timestamp (ISO 8601).
  - Log Level (`INFO`, `WARN`, `ERROR`, `FATAL`).
  - `correlation_id` / `trace_id` (gắn liền với từng request của người dùng).
  - Thông điệp tóm tắt và metadata liên quan.

### Bước 2: Thiết Kế Health Check Endpoints (/healthz)
- Triển khai 2 cấp độ kiểm tra sức khỏe:
  - **Liveness probe (`/healthz/live`)**: Kiểm tra ứng dụng có còn sống và phản hồi HTTP không (tránh zombie process).
  - **Readiness probe (`/healthz/ready`)**: Kiểm tra các phụ thuộc thiết yếu có sẵn sàng nhận traffic không (kết nối database, redis, message queue).

### Bước 3: Thu Thập Các Chỉ Số Trọng Yếu (RED Metrics)
- Theo dõi các chỉ số vàng theo chuẩn RED:
  - **Rate**: Số lượng request trên giây (Throughput).
  - **Errors**: Tỷ lệ request trả về lỗi HTTP 5xx.
  - **Duration**: Thời gian xử lý request (Latency histogram: p50, p90, p99).

### Bước 4: Thiết Lập Cơ Chế Cảnh Báo Sớm (Alerting Rules)
- Đặt ngưỡng kích hoạt thông báo tự động (qua Slack, Telegram, PagerDuty, Email):
  - Cảnh báo nếu tỷ lệ lỗi HTTP 5xx vượt quá 1% trong 5 phút liên tiếp.
  - Cảnh báo nếu thời gian phản hồi p95 vượt quá 1 giây trong 3 phút.
  - Cảnh báo khi Readiness probe trả về status `UNHEALTHY`.

### Bước 5: Phân Tích & Truy Vết Sự Cố (Incident Investigation)
- Khi có cảnh báo: Sử dụng `trace_id` để tra cứu toàn bộ hành trình của request bị lỗi từ gateway đến database.
- Tách biệt lỗi do hệ thống bên thứ ba, do đường truyền hay do bug mã nguồn.

### Bước 6: Khắc Phục, Kiểm Chứng & Ngăn Tái Diễn (Post-Incident Stabilization)
- Sau khi xử lý sự cố: Đánh giá xem hệ thống giám sát có phát hiện lỗi đủ nhanh không, bổ sung chỉ số mới nếu cần và viết báo cáo Post-mortem.

## 6. Quality Gates
- **QG-04 (Health Check Working)**: Endpoint `/healthz` phản hồi mã HTTP `200 OK` khi chạy kiểm tra.
- **QG-07 (No Sensitive Data in Logs)**: Log tuyệt đối không chứa mật khẩu, số thẻ ngân hàng, JWT secret hoặc PII của người dùng.
- **QG-10 (Monitoring Evidence)**: Có bằng chứng kiểm tra endpoint liveness/readiness hoạt động đúng.

## 7. Safety Rules
- **Lọc Dữ Liệu Nhạy Cảm (Log Masking)**: Bắt buộc cấu hình cơ chế tự động làm sạch (masking) các trường nhạy cảm: `password`, `token`, `credit_card` thành `***`.
- **Tránh Làm Sập Hệ Thống Vì Log (Non-blocking I/O)**: Không sử dụng các cơ chế ghi log đồng bộ (blocking I/O) làm nghẽn Event Loop.
- **Bảo Vệ Endpoint Giám Sát**: Không để lộ thông tin nhạy cảm về phiên bản thư viện hoặc connection string trong phản hồi của endpoint health check.

## 8. Expected Outputs
1. Cấu hình logging chuẩn hóa JSON theo cấp độ rõ ràng.
2. Endpoint `/healthz/live` và `/healthz/ready` hoạt động ổn định.
3. Tài liệu mô tả các chỉ số giám sát và hướng dẫn thiết lập cảnh báo.

## 9. Failure Handling
- Nếu endpoint health check báo `DOWN`: Tự động ngắt traffic từ load balancer chuyển sang các node khỏe mạnh khác, đồng thời kích hoạt cảnh báo khẩn cấp cho đội ngũ vận hành.

## 10. Completion Criteria
- Các luồng log được cấu trúc chuẩn JSON và có trace ID.
- Health check endpoints phản hồi chính xác trạng thái của app và các dịch vụ phụ thuộc.
- Không có dữ liệu nhạy cảm bị rò rỉ qua log.

---

## Real-world Example
Triển khai endpoint kiểm tra sức khỏe hệ thống Express.js:
```typescript
app.get('/healthz/ready', async (req, res) => {
  try {
    await db.query('SELECT 1'); // Kiểm tra DB kết nối tốt
    await redisClient.ping();   // Kiểm tra Redis cache sẵn sàng
    res.status(200).json({ status: 'HEALTHY', timestamp: new Date().toISOString() });
  } catch (error) {
    logger.error('Readiness check failed', { error: error.message });
    res.status(503).json({ status: 'UNHEALTHY', error: 'Dependency unavailable' });
  }
});
```
Load balancer dựa vào endpoint này để tự động định tuyến traffic an toàn.
