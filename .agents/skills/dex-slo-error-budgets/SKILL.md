---
name: dex-slo-error-budgets
description: Define, track, and operationalize Service Level Indicators (SLIs), Service Level Objectives (SLOs), Error Budgets, and multi-window burn rate alerts. Use when establishing reliability targets or driving deployment freeze policies.
---

# dex-slo-error-budgets

## 1. Purpose & Scope
Thiết lập, theo dõi và vận hành hệ thống chỉ số độ tin cậy dịch vụ chuẩn SRE (Site Reliability Engineering); định nghĩa Service Level Indicators (SLIs) có thể đo lường định lượng, xác lập Service Level Objectives (SLOs) thực tế (ví dụ: 99.9% availability), tính toán ngân sách lỗi (Error Budget), cấu hình cảnh báo tốc độ đốt ngân sách đa khung giờ (Multi-Window Multi-Burn-Rate Alerts) và ban hành chính sách đóng băng phát hành khi cạn kiệt ngân sách lỗi.

## 2. When to Use
- Khi đội ngũ kỹ thuật và sản phẩm cần thống nhất cam kết chất lượng dịch vụ (SLA/SLO) dựa trên dữ liệu.
- Khi hệ thống bị quá nhiều cảnh báo giả (Alert Fatigue) hoặc cảnh báo tới chậm khi có sự cố lớn.
- Khi cần cơ chế định lượng để quyết định: Tiếp tục release tính năng mới hay tập trung cải thiện độ tin cậy hạ tầng.

## 3. When NOT to Use
- Đo lường chi phí đám mây (dùng `dex-cloud-cost-finops`).
- Giám sát APM thông thường cho 1 function nhỏ (dùng `dex-production-monitoring`).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Dữ liệu telemetry (Prometheus metrics: `http_requests_total`, mã trạng thái HTTP, latency histograms).
- Mục tiêu SLO kinh doanh (ví dụ: 99.9% request thành công trong 30 ngày lăn bánh).
- Ngưỡng giới hạn độ trễ (ví dụ: P95 < 250ms).
- **Điều kiện tiên quyết**:
- Hệ thống giám sát Prometheus / Thanos / VictoriaMetrics lưu trữ dữ liệu tối thiểu 30-90 ngày.
- Phân loại rõ ràng request hợp lệ của người dùng (loại bỏ health check probes nội bộ).

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- **Good Events over Valid Events (SLI Ratio)**: Tỷ lệ giữa số sự kiện đạt yêu cầu trên tổng số sự kiện hợp lệ: `SLI = sum(good_requests) / sum(valid_requests)`.
- **Error Budget (Ngân Sách Lỗi)**: Tỷ lệ lỗi được phép tồn tại: `Budget = 100% - SLO` (Ví dụ SLO 99.9% -> Budget là 0.1% lỗi, tương đương 43.8 phút downtime/tháng).
- **Multi-Window Multi-Burn-Rate Alerting**: Thay vì cảnh báo theo ngưỡng tức thời, cảnh báo dựa trên tốc độ tiêu hao ngân sách lỗi (Burn Rate 14.4x trong 1 giờ đốt hết 2% budget -> PagerDuty khẩn cấp).
- **Quy tắc quyết định kỹ thuật**:
- **Đóng Băng Triển Khai Khi Hết Budget**: Nếu Error Budget của tháng bị tiêu hao > 100%, tạm dừng mọi tính năng mới, toàn bộ đội ngũ tập trung sửa lỗi kỹ thuật và độ ổn định.
- **Đo Lường Trải Nghiệm Người Dùng Cuối**: SLI phải phản ánh chính xác sự thất vọng của người dùng (Bad Requests từ góc nhìn client), không đo CPU hay RAM máy chủ.
- **Cửa Sổ Thời Gian Lăn Bánh (Rolling Window)**: Luôn tính SLO trên cửa sổ trượt 30 ngày (Rolling 30-day window) thay vì tháng dương lịch cố định.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Cảnh báo liên tục lúc 2h sáng vì 5 request lỗi khi traffic thấp**: Do cấu hình cảnh báo theo % lỗi cố định -> Khắc phục: Áp dụng Multi-burn-rate yêu cầu cả cửa sổ ngắn (Short Window) và cửa sổ dài (Long Window) cùng vượt ngưỡng.
- **SLO 99.99% bất khả thi gây nản lòng cho đội ngũ**: Đặt mục tiêu quá cao trong khi dependency bên thứ ba chỉ có SLA 99.5% -> Khắc phục: Điều chỉnh lại SLO phù hợp với thực tế phụ thuộc.

## 6. Step-by-Step Execution Workflow
1. Xác định User Journey quan trọng (Đăng nhập, Thêm giỏ hàng, Thanh toán).
2. Định nghĩa công thức SLI rõ ràng cho từng hành trình (Availability SLI và Latency SLI).
3. Thống nhất mục tiêu SLO và ghi nhận vào tài liệu đặc tả độ tin cậy.
4. Viết các rule ghi nhận chỉ số trong Prometheus (`PrometheusRule`: tính SLI 1h, 6h, 30d).
5. Thiết lập cảnh báo Multi-window Multi-burn-rate (Page Alert cho Burn Rate 14.4x/6h, Ticket Alert cho Burn Rate 3x/3d).
6. Xây dựng Dashboard Grafana trực quan hóa % Error Budget còn lại theo thời gian thực.
7. Thiết lập quy trình đánh giá Error Budget định kỳ hàng tuần với Product Manager.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```yaml
# PrometheusRule: Cảnh báo đốt ngân sách lỗi đa cửa sổ (Burn Rate 14.4x trong 1h và 5m)
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: slo-alerts-checkout
  namespace: monitoring
spec:
  groups:
  - name: checkout-slo
    rules:
    - alert: CheckoutHighErrorBudgetBurn
      expr: |
        (
          sum(rate(http_requests_total{job="checkout",status=~"5.."}[1h]))
          /
          sum(rate(http_requests_total{job="checkout"}[1h]))
        ) > (1 - 0.999) * 14.4
        and
        (
          sum(rate(http_requests_total{job="checkout",status=~"5.."}[5m]))
          /
          sum(rate(http_requests_total{job="checkout"}[5m]))
        ) > (1 - 0.999) * 14.4
      for: 2m
      labels:
        severity: critical
      annotations:
        summary: "Checkout Service đang đốt ngân sách lỗi với tốc độ 14.4x (Mất 2% budget trong 1h)"
```

### Lệnh xác minh & thực thi:
- Kiểm tra cú pháp Prometheus rule: `promtool check rules slo-rules.yaml`
- Truy vấn tỷ lệ Error Budget còn lại: `promtool query instant http://prometheus:9090 '1 - (sum(increase(http_errors[30d])) / (0.001 * sum(increase(http_total[30d]))))'`
- Kiểm tra tính hợp lệ của alert firing trên Alertmanager UI

## 8. Anti-Patterns & Common Traps
- **Đặt SLO 100% Availability**: Bất khả thi trong hệ thống phân tán và ngăn chặn hoàn toàn việc triển khai đổi mới.
- **Đo SLI tại máy chủ nội bộ bỏ qua Ingress**: Không phát hiện được lỗi 502/504 do Ingress controller hoặc Gateway sinh ra.
- **Không hành động gì khi cạn Error Budget**: Khiến khái niệm SLO trở thành lý thuyết hình thức.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Định nghĩa SLI có công thức PromQL toán học chính xác, không mơ hồ.
- QG-08: Tỷ lệ cảnh báo giả (False Positive Alerts) giảm trên 80% sau khi áp dụng Multi-burn-rate.
- QG-11: Dashboard trực quan hóa hiển thị chính xác % budget tiêu hao.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi deploy.

## 10. Security & Safety Boundaries
- Bảo vệ endpoint Prometheus metrics không để lộ dữ liệu nhạy cảm của khách hàng trong label query.
- Giới hạn quyền chỉnh sửa mục tiêu SLO để tránh hành vi tự ý hạ chuẩn khi gặp sự cố.
- Không bao giờ lưu trữ hardcoded secret hoặc cấp quyền quá mức (over-permissioned IAM).

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Môi trường Cloud & Container**: Hỗ trợ Docker, Kubernetes (EKS/GKE/AKS), Terraform/OpenTofu, OpenTelemetry.

## 12. Deliverables & Output Artifacts
- Tệp định nghĩa `PrometheusRule` chứa SLI recording rules và alert rules.
- Dashboard Grafana trực quan hóa SLO/Error Budget.
- Chính sách vận hành khi cạn ngân sách lỗi (Error Budget Policy).

## 13. Related & Complementary Skills
- `dex-production-monitoring`: Thu thập chỉ số APM và hệ thống.
- `dex-incident-postmortems`: Đánh giá thiệt hại ngân sách lỗi sau mỗi sự cố.
- `dex-zero-downtime-rollouts`: Dừng phát hành Canary khi vi phạm ngân sách lỗi.

## 14. Realistic Usage Example
### Tình huống thực tế:
Đội ngũ kỹ thuật Checkout liên tục bị bất đồng với Product Manager về việc có nên hoãn release để dọn technical debt. Áp dụng `dex-slo-error-budgets`, họ thống nhất SLO 99.9% cho cổng thanh toán. Khi một sự cố hạ tầng tuần trước đã đốt 85% ngân sách lỗi của tháng, chính sách Error Budget Policy tự động kích hoạt hoãn release các tính năng mới trong 2 tuần tiếp theo, giúp toàn đội tập trung gia cố hạ tầng mà không có tranh cãi cảm tính.
