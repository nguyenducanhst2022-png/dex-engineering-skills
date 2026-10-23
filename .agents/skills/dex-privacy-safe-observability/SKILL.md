---
name: dex-privacy-safe-observability
description: Architect privacy-first telemetry pipelines with automated PII masking, token scrubbing, client-side differential privacy, and GDPR/CCPA data retention controls. Use when maintaining deep observability without compliance violations.
---

# dex-privacy-safe-observability

## 1. Purpose & Scope
Thiết kế và triển khai hệ thống quan sát (Observability - Logs, Metrics, Traces) an toàn quyền riêng tư; tự động làm mờ và lọc sạch thông tin PII, token xác thực, mật khẩu, và dữ liệu thẻ thanh toán trước khi lưu trữ; bảo đảm tuân thủ nghiêm ngặt các quy định GDPR, CCPA và PCI-DSS.

## 2. When to Use
- Khi vô tình phát hiện số thẻ tín dụng, mật khẩu hoặc số căn cước công dân của người dùng xuất hiện trong bảng log ElasticSearch hoặc Datadog.
- Khi kiểm toán viên bảo mật yêu cầu chứng minh dữ liệu giám sát tuân thủ quyền được lãng quên (Right to be Forgotten).
- Khi chuẩn hóa pipeline thu thập dữ liệu OpenTelemetry cho toàn bộ hệ sinh thái dịch vụ.

## 3. When NOT to Use
- Khi tiến hành debug cục bộ trên máy trạm cá nhân với dữ liệu hoàn toàn giả lập không có người dùng thật.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Collector thu thập telemetry (OpenTelemetry Collector, Vector, Fluentbit), hệ thống lưu trữ log/trace.
- **Quyền hạn truy cập:** Quyền sửa đổi pipeline xử lý của OpenTelemetry Collector hoặc logging framework.

## 5. Core Concepts & Taxonomy
- **Telemetry Redaction at Ingestion:** Lọc bỏ thông tin nhạy cảm ngay tại bộ thu thập biên (Collector) trước khi dữ liệu được truyền qua mạng hoặc ghi vào đĩa lưu trữ dài hạn.
- **Pattern Scrubbing Regex:** Các biểu thức chính quy chuẩn hóa nhận diện số thẻ tín dụng (Luhn algorithm), email, số điện thoại, JWT tokens và API keys.
- **TTL & Retention Enforcement:** Quy định chính sách lưu trữ nhật ký tự động phân tầng: Log chi tiết xóa sau 14 ngày, log tổng hợp lưu 90 ngày.

## 6. Step-by-Step Execution Workflow
1. Khảo sát toàn bộ các trường dữ liệu và payload được ghi nhận vào nhật ký (Logs) và nhãn truy vết (Span Attributes).
2. Xây dựng bộ quy tắc lọc (Scrubbing Rules) trong OpenTelemetry Collector hoặc thư viện logging của ứng dụng.
3. Áp dụng kỹ thuật băm một chiều có muối hoặc thay thế bằng chuỗi `[REDACTED]` cho các trường PII.
4. Cấu hình kiểm tra tự động phát hiện rò rỉ PII trong CI/CD bằng cách nạp dữ liệu thử nghiệm chứa thông tin giả lập.
5. Thiết lập chính sách tự động xóa hoặc chuyển vùng lưu trữ lạnh (Data Tiering) theo thời gian sống (TTL).
6. Đào tạo lập trình viên sử dụng các phương thức ghi log có cấu trúc an toàn (Structured Logging).

## 7. Concrete Examples
### Cấu hình bộ lọc PII và Secrets trong OpenTelemetry Collector (otel-collector-config.yaml):
```yaml
processors:
  transform/redact_pii:
    error_mode: ignore
    log_statements:
      - context: log
        statements:
          # Lam mo dia chi Email
          - replace_pattern(body, "[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", "[REDACTED_EMAIL]")
          # Lam mo so the tin dung
          - replace_pattern(body, "\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14})\b", "[REDACTED_CC]")
          # Loc bo Authorization Bearer Token
          - replace_pattern(body, "Bearer\s+[A-Za-z0-9-_=]+\.[A-Za-z0-9-_=]+\.?[A-Za-z0-9-_.+/=]*", "Bearer [REDACTED_JWT]")

service:
  pipelines:
    logs:
      receivers: [otlp]
      processors: [transform/redact_pii, batch]
      exporters: [elasticsearch]
```

## 8. Anti-Patterns & Common Traps
- **Logging Raw HTTP Request Payloads:** Tự động in toàn bộ body của request `/api/login` hoặc `/api/checkout` vào file nhật ký.
- **Storing Telemetry Forever:** Không đặt chính sách hết hạn (TTL) khiến log chứa thông tin cá nhân tồn tại vĩnh viễn trên cloud storage.
- **Client-Side Sensitive Traces:** Gửi toàn bộ dữ liệu người dùng vào các span attributes của công cụ giám sát hiệu năng frontend.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: 0% số thẻ tín dụng, mật khẩu hoặc JWT token xuất hiện trong hệ thống lưu trữ log trung tâm.
- **QG-04**: 100% luồng dữ liệu telemetry đi qua bộ xử lý làm sạch PII trước khi xuất bản.
- **QG-08**: Chính sách lưu trữ dữ liệu log (Log Retention TTL) được tự động thực thi đúng hạn.

## 10. Security & Safety Boundaries
- Tránh các khoản phạt nặng nề từ các cơ quan quản lý (GDPR lên tới 4% doanh thu toàn cầu) do lưu trữ trái phép thông tin PII trong hệ thống giám sát.

## 11. Platform Adapters
- **Collectors**: OpenTelemetry Collector, Vector by Datadog, Fluent Bit, Logstash.
- **Storage**: ElasticSearch, Loki, Datadog, Grafana Tempo.

## 12. Deliverables & Output Artifacts
- File cấu hình OpenTelemetry Collector tích hợp bộ lọc PII.
- Bộ quy tắc Regex nhận diện thông tin nhạy cảm tiếng Việt và quốc tế.
- Dashboard kiểm toán tuân thủ chính sách lưu trữ dữ liệu giám sát.

## 13. Related & Complementary Skills
dex-data-masking-synthetic-generation, dex-api-authorization-matrix-tests, dex-incident-evidence-preservation

## 14. Realistic Usage Example
```powershell
# Kiểm tra bộ lọc OpenTelemetry Collector với dữ liệu mẫu
otelcol validate --config otel-collector-config.yaml

# Quét phát hiện PII trong log bằng script kiểm toán
python scripts/security/scan_log_pii.py --log-sample elastic_logs.json
```
