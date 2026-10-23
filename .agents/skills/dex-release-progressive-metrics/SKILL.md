---
name: dex-release-progressive-metrics
description: Define, analyze, and automate progressive canary release metrics (Argo Rollouts, Flagger). Measure SLI/SLO error rates, latency regressions, and trigger automated rollbacks.
---

# dex-release-progressive-metrics

## 1. Purpose & Scope
Thiết kế, định nghĩa và tự động hóa các chỉ số đánh giá phát hành lũy tiến (Progressive Canary Release Metrics); tích hợp các bộ điều khiển phát hành hiện đại (Argo Rollouts, Flagger, Istio Service Mesh); đo lường tự động các chỉ số cấp độ dịch vụ (SLI/SLO: Error Rates, Latency P95/P99, HTTP 5xx Statuses) so sánh giữa phiên bản Canary và phiên bản Baseline; tự động đưa ra quyết định tăng bậc phần trăm lưu lượng mạng hoặc kích hoạt hủy bỏ khẩn cấp (Automated Rollback) khi phát hiện dấu hiệu bất thường.

## 2. When to Use
- Khi triển khai các bản cập nhật phần mềm quan trọng cho hệ thống phục vụ hàng triệu người dùng trực tuyến.
- Khi muốn chuyển dịch từ phương pháp phát hành rủi ro cao (Big Bang Deployment) sang phương pháp thử nghiệm lưu lượng nhỏ (Canary 5% -> 20% -> 50% -> 100%).
- Khi cần loại bỏ sự can thiệp thủ công của con người trong việc quan sát biểu đồ để quyết định thăng cấp phiên bản.

## 3. When NOT to Use
- Khi dịch vụ chỉ phục vụ môi trường nội bộ với lưu lượng truy cập quá thấp (<1 request/phút) không đủ dữ liệu thống kê để đánh giá.
- Khi bản cập nhật chứa các thay đổi phá vỡ tương thích cấu trúc CSDL (Database Schema Breaking Changes) không thể chạy song song 2 phiên bản.

## 4. Prerequisites & Input Context
- **Hạ tầng đo lường:** Prometheus, Datadog hoặc CloudWatch thu thập chỉ số thời gian thực với độ trễ <15 giây.
- **Bộ điều phối:** Argo Rollouts hoặc Flagger cài đặt trên cụm Kubernetes.

## 5. Core Concepts & Taxonomy
- **Canary Step Weights:** Lộ trình tăng dần tỷ lệ phần trăm người dùng tiếp cận phiên bản mới (ví dụ: bước 1 cấp 10% trong 10 phút, bước 2 cấp 30% trong 20 phút).
- **AnalysisRun:** Đối tượng trong Argo Rollouts định kỳ thực thi các câu truy vấn Prometheus để xác nhận tỷ lệ lỗi không vượt ngưỡng cho phép.
- **Automated Rollback Trigger:** Hành động hoàn nguyên lưu lượng về 100% phiên bản Stable ngay lập tức khi chỉ số Canary vi phạm ngưỡng thất bại liên tiếp (Consecutive Failures).

## 6. Step-by-Step Execution Workflow
1. Xác định các chỉ số SLI cốt lõi: Tỷ lệ lỗi thành công (`success_rate > 99.5%`) và độ trễ P95 (`latency_p95 < 200ms`).
2. Cấu hình tài nguyên `AnalysisTemplate` định nghĩa câu truy vấn Prometheus và ngưỡng đánh giá.
3. Khai báo đối tượng `Rollout` thay thế cho `Deployment` tiêu chuẩn trong Kubernetes.
4. Kích hoạt cập nhật phiên bản mới bằng cách thay đổi container image tag.
5. Argo Rollouts tự động định tuyến 10% lưu lượng sang Canary Pod và kích hoạt `AnalysisRun`.
6. Nếu toàn bộ các lượt phân tích đều thành công, tự động chuyển 100% lưu lượng và dọn dẹp các Pod cũ; nếu vi phạm, tự động hoàn nguyên về bản Stable trong 15 giây.

## 7. Concrete Examples
### Cau hinh Argo Rollouts AnalysisTemplate do luong ty le loi va do tre tu Prometheus:
```yaml
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: success-rate-and-latency-check
  namespace: production
spec:
  metrics:
    - name: success-rate
      interval: 30s
      successCondition: result[0] >= 0.995 # Yeu cau ty le thanh cong >= 99.5%
      failureLimit: 2 # Cho phep toi da 2 lan fail truoc khi rollback
      provider:
        prometheus:
          address: http://prometheus.monitoring:9090
          query: |
            sum(rate(http_requests_total{status!~"5.*",app="web-api",role="canary"}[1m])) 
            / 
            sum(rate(http_requests_total{app="web-api",role="canary"}[1m]))

    - name: latency-p95
      interval: 30s
      successCondition: result[0] <= 0.250 # Do tre P95 khong vuot qua 250ms
      failureLimit: 2
      provider:
        prometheus:
          address: http://prometheus.monitoring:9090
          query: |
            histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket{app="web-api",role="canary"}[1m])) by (le))
```

## 8. Anti-Patterns & Common Traps
- **Too Short Analysis Intervals:** Đặt chu kỳ kiểm tra quá ngắn (dưới 5 giây) khiến mẫu dữ liệu quá thưa thớt dẫn đến việc đánh giá sai lệch (False Positive Rollback).
- **Ignoring Client-Side Errors (4xx):** Chỉ theo dõi lỗi 5xx mà bỏ qua lỗi 4xx khi bản cập nhật mới vô tình làm gãy định dạng API khiến hàng loạt client gửi request lỗi.
- **Manual Approval Bottle-neck:** Bắt buộc con người phải bấm nút Approve ở mỗi bước 5%, 10%, 20% làm mất hoàn toàn lợi ích của tự động hóa triển khai.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Tỷ lệ thành công (Success Rate) của phiên bản Canary đạt tối thiểu 99.5% trong toàn bộ các bước triển khai.
- **QG-02**: Độ trễ phản hồi P95 không tăng quá 15% so với phiên bản Stable hiện tại.
- **QG-03**: Hệ thống tự động kích hoạt hoàn nguyên (Rollback) trong vòng dưới 30 giây khi phát hiện vi phạm ngưỡng an toàn.

## 10. Security & Safety Boundaries
- Hạn chế quyền can thiệp vào tiến trình Rollout; mọi thao tác Promote hoặc Abort thủ công đều phải được lưu vết kiểm toán (Audit Trail).

## 11. Platform Adapters
- **Runtimes**: Argo Rollouts, Flagger, Prometheus, Istio Service Mesh, Datadog.

## 12. Deliverables & Output Artifacts
- Tệp định nghĩa mẫu phân tích lũy tiến (`canary_analysis_template.yaml`).
- Báo cáo đánh giá kết quả triển khai canary (`canary_deployment_summary.json`).

## 13. Related & Complementary Skills
dex-api-circuit-breaker-verification, dex-queue-capacity-saturation, dex-operational-dependency-mapping

## 14. Realistic Usage Example
```bash
# Theo doi trang thai phat hanh luy tien bang argo rollouts CLI
kubectl argo rollouts get rollout web-api -n production --watch
```
