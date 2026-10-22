---
name: dex-alert-quality-engineering
description: Audit, refine, and eliminate noisy monitoring alerts by tuning thresholds, implementing deduplication, and ensuring all alerts are actionable with runbooks. Use to eradicate on-call alert fatigue and improve incident response.
---

# dex-alert-quality-engineering

## 1. Purpose & Scope
Kiểm toán, tinh chỉnh và loại bỏ các cảnh báo giám sát gây nhiễu (Alert Fatigue); đánh giá ngưỡng cảnh báo dựa trên triệu chứng (Symptom-based Alerting) thay vì nguyên nhân phỏng đoán, thiết lập gom nhóm cảnh báo và bảo đảm 100% cảnh báo gửi tới kỹ sư trực đều có tính hành động (Actionable) kèm runbook xử lý rõ ràng.

## 2. When to Use
- Kỹ sư on-call nhận hàng chục cảnh báo mỗi đêm nhưng hầu hết là 'tự hết' hoặc không cần làm gì.
- Alert fatigue dẫn đến việc kỹ sư bỏ lỡ cảnh báo sự cố nghiêm trọng thực sự.
- Bị phàn nàn về các cảnh báo vô nghĩa như 'CPU > 80%' trong khi người dùng không hề bị ảnh hưởng.

## 3. When NOT to Use
- Không tắt các cảnh báo vi phạm SLO/SLA nghiêm trọng ảnh hưởng trực tiếp tới khách hàng.
- Không xóa cảnh báo khi chưa tìm hiểu lý do tại sao nó được tạo ra ban đầu.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Lịch sử cảnh báo trong 30-90 ngày qua từ PagerDuty/Opsgenie/Alertmanager.
- Danh sách các cảnh báo thường xuyên bị 'Acknowledge rồi bỏ đó'.
- Chỉ số SLO/SLI hiện tại của dịch vụ.
- **Điều kiện tiên quyết**:
- Có quyền truy cập vào cấu hình Prometheus Alertmanager hoặc Datadog/Grafana Alert rules.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Symptom-based Alerting: Cảnh báo khi người dùng bị ảnh hưởng (ví dụ: Tỉ lệ lỗi HTTP 5xx tăng cao, Độ trễ thanh toán P99 > 2s). Không bao giờ đánh thức kỹ sư nửa đêm chỉ vì 'CPU máy chủ đạt 85%'.
- Actionability: Một cảnh báo hợp lệ phải trả lời được câu hỏi: 'Kỹ sư nhận cảnh báo này cần làm hành động cụ thể gì ngay lập tức?'. Nếu câu trả lời là 'Không làm gì', hãy xóa cảnh báo hoặc chuyển sang kênh email/slack thông báo định kỳ.
- **Quy tắc quyết định kỹ thuật**:
- Nếu một cảnh báo kích hoạt hơn 3 lần một ngày nhưng không sinh ra incident nào: xóa bỏ hoặc nâng ngưỡng.
- Mọi cảnh báo Pager/SMS bắt buộc phải có đường dẫn trực tiếp tới `runbook_url` hợp lệ.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Tắt hết cảnh báo để 'yên tĩnh' dẫn đến hệ thống sập nửa ngày mà không ai hay biết.

## 6. Step-by-Step Execution Workflow
1. Xuất báo cáo thống kê top 10 cảnh báo xuất hiện nhiều nhất trong tháng.
2. Phân loại từng cảnh báo: Actionable vs Non-actionable.
3. Chuyển đổi các cảnh báo đo nguyên nhân (Cause-based) sang đo lường vi phạm ngân sách lỗi SLO (Multi-window Multi-burn-rate Alerting).
4. Bổ sung `runbook_url` chi tiết vào nhãn của mỗi rule.
5. Đánh giá lại sau 2 tuần: mục tiêu giảm tối thiểu 60% số lượng cảnh báo rác đánh thức ban đêm.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```yaml
# Rule cảnh báo chuẩn Google SRE: Multi-burn-rate Alerting
- alert: HighErrorRateBurnRate
  expr: (
      rate(http_requests_total{status=~"5.."}[1h]) / rate(http_requests_total[1h])
    ) > (14.4 * (1 - 0.999))
  for: 2m
  labels:
    severity: critical
  annotations:
    summary: "Dịch vụ đang tiêu thụ ngân sách lỗi (Error Budget) quá nhanh trong 1 giờ qua."
    runbook_url: "https://wiki.example.com/runbooks/high-error-rate"
```

### Lệnh xác minh & thực thi:
```bash
# Kiểm tra cú pháp và unit test cho alert rules của Prometheus
promtool check rules rules/alerts.yaml
promtool test rules tests/alerts-test.yaml
```

## 8. Anti-Patterns & Common Traps
- Gửi cảnh báo rác vào một kênh Slack chung không ai đọc (kênh 'nghĩa địa cảnh báo').
- Cảnh báo dựa trên con số tĩnh không tính đến chu kỳ ngày/đêm (ví dụ số đơn hàng giảm lúc 3 giờ sáng là bình thường).

## 9. Quality Gates & Acceptance Criteria
- Giảm tỉ lệ false-positive alerts xuống dưới 5% tổng số cảnh báo nhận được.
- 100% cảnh báo critical có runbook và dashboard đi kèm.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Nội dung thông báo cảnh báo không được chứa mật khẩu, API keys hay thông tin PII của khách hàng.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ thống hỗ trợ**: Linux (CI/CD runners), macOS, Windows 11 PowerShell/WSL2.

## 12. Deliverables & Output Artifacts
- Bảng kiểm toán chất lượng cảnh báo (Alert Audit Matrix).
- File cấu hình alert rules đã được tinh chỉnh kèm bộ unit tests `promtool`.

## 13. Related & Complementary Skills
dex-metric-cardinality-control, dex-oncall-handover, dex-log-pipeline-design

## 14. Realistic Usage Example
### Tình huống thực tế:
Một đội SRE bị quá tải với hơn 400 cảnh báo PagerDuty mỗi tuần, khiến các kỹ sư kiệt sức và xin nghỉ việc. Bằng cách áp dụng kiểm toán Alert Quality và chuyển sang mô hình Google SRE Multi-Burn-Rate, số lượng cảnh báo giảm từ 400 xuống còn 12 cảnh báo/tuần, và 100% các cảnh báo đó đều là sự cố thực sự cần xử lý.
