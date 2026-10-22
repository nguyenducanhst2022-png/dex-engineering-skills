---
name: dex-zero-downtime-rollouts
description: Execute blue-green, canary, and progressive rollouts using Argo Rollouts, Flagger, or ingress traffic shifting with automated metric analysis, health checks, and instant rollbacks. Use when deploying critical services without customer interruption.
---

# dex-zero-downtime-rollouts

## 1. Purpose & Scope
Thiết kế, tự động hóa và thực thi các chiến lược triển khai không thời gian chết (Zero-Downtime Rollouts: Blue-Green Deployment, Canary Releases, Progressive Delivery) cho các dịch vụ cốt lõi; tích hợp phân tích chỉ số thời gian thực (Prometheus / Datadog Metrics Analysis: Error Rate, Latency P99), chuyển dịch lưu lượng mạng theo từng bước và tự động kích hoạt Rollback tức thì khi phát hiện bất thường.

## 2. When to Use
- Khi triển khai phiên bản mới của các dịch vụ quan trọng (Core Payment, Auth, Checkout) mà không được phép làm gián đoạn người dùng.
- Khi cần thử nghiệm phiên bản mới trên một tập nhỏ người dùng (5% - 10% Canary traffic) trước khi mở rộng toàn bộ.
- Khi hệ thống có các thay đổi tiềm ẩn rủi ro hiệu năng cao cần đo lường thực tế dưới tải thực.

## 3. When NOT to Use
- Môi trường Development hoặc Staging thử nghiệm nội bộ (dùng rolling update tiêu chuẩn trong `dex-kubernetes-deployment`).
- Thay đổi phá vỡ tương thích cơ sở dữ liệu chưa qua bước migrate trung gian (dùng `dex-schema-evolution`).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Phiên bản ứng dụng mới (Stable vs Canary image).
- Tiêu chí đánh giá chất lượng tự động (Analysis Template: Error rate < 0.5%, P99 Latency < 300ms).
- Tỷ lệ phân bổ traffic theo thời gian (ví dụ: 10% -> 25% -> 50% -> 100%).
- **Điều kiện tiên quyết**:
- Service Mesh (Istio / Linkerd) hoặc Ingress Controller (Nginx, Traefik, AWS ALB) hỗ trợ Traffic Splitting.
- Hệ thống giám sát Prometheus / Datadog thu thập metrics độ trễ và mã lỗi theo thời gian thực.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- **Progressive Traffic Splitting**: Điều hướng một phần nhỏ lượng request thực tế (ví dụ 5%) vào phiên bản mới để phát hiện lỗi mà chỉ ảnh hưởng tới phạm vi tối thiểu.
- **Automated Metric Gating**: Sử dụng thuật toán so sánh metric giữa Canary và Stable (hoặc ngưỡng tĩnh); nếu Canary vi phạm ngưỡng quá 2 lần, tự động hủy bỏ rollout.
- **Instant Traffic Switch**: Trỏ lại Ingress/Router về Stable version trong vòng vài giây mà không cần chờ xóa Pods.
- **Quy tắc quyết định kỹ thuật**:
- **Quy Tắc Tương Thích Ngược Bắt Buộc**: Mọi phiên bản Canary phải tương thích ngược hoàn toàn với cấu trúc dữ liệu và API hiện tại (Forward & Backward Compatibility).
- **Tự Động Hóa Hoàn Toàn Quyết Định Rollback**: Không phụ thuộc vào sự can thiệp thủ công của con người khi tỷ lệ lỗi vượt quá ngưỡng cho phép (ví dụ: HTTP 5xx > 1% trong 2 phút liên tiếp).
- **Thời Gian Đánh Giá Đủ Lớn (Bake Time)**: Mỗi bước tăng traffic phải có khoảng thời gian bake time tối thiểu 5-10 phút để thu thập đủ mẫu dữ liệu thống kê.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Lỗi chỉ xuất hiện khi traffic đạt 50%**: Gây quá tải database connection pool -> Khắc phục: Phân tích metric database song song trong AnalysisTemplate, rollback ngay khi pool usage > 85%.
- **Canary bị rollback nhưng cache bẩn vẫn ảnh hưởng người dùng**: Phiên bản mới ghi dữ liệu sai định dạng vào Redis -> Khắc phục: Sử dụng namespace cache phân tách cho Canary hoặc tuân thủ strict versioning trong cache payload.

## 6. Step-by-Step Execution Workflow
1. Chuẩn bị tài nguyên `Rollout` thay thế cho `Deployment` tiêu chuẩn (sử dụng Argo Rollouts hoặc Flagger).
2. Định nghĩa `AnalysisTemplate` truy vấn Prometheus kiểm tra tỉ lệ lỗi HTTP 5xx và latency P99.
3. Thiết lập các bước điều phối lưu lượng mạng: 5% (bake 5m) -> 20% (bake 10m) -> 50% (bake 10m) -> 100%.
4. Kích hoạt phát hành: Cập nhật image tag của Rollout.
5. Giám sát tiến trình phân tích tự động: `kubectl argo rollouts get rollout my-service -w`.
6. Trường hợp metrics đạt yêu cầu: Tự động thăng cấp (Promote) Canary thành Stable và dừng phân tích.
7. Trường hợp metrics suy giảm: Hệ thống tự động chuyển traffic về Stable, emit alert và đưa Rollout về trạng thái Degraded.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: checkout-service
  namespace: production
spec:
  replicas: 10
  strategy:
    canary:
      canaryService: checkout-canary
      stableService: checkout-stable
      trafficRouting:
        istio:
          virtualService:
            name: checkout-vsvc
            routes:
            - primary
      steps:
      - setWeight: 10
      - pause: { duration: 5m }
      - setWeight: 30
      - pause: { duration: 10m }
      - setWeight: 60
      - pause: { duration: 10m }
      analysis:
        templates:
        - templateName: success-rate-metric
        args:
        - name: service-name
          value: checkout-service
```

### Lệnh xác minh & thực thi:
- Theo dõi trực quan tiến trình Canary: `kubectl argo rollouts get rollout checkout-service --watch`
- Thử nghiệm rollback khẩn cấp thủ công: `kubectl argo rollouts abort checkout-service`
- Xác minh tỷ lệ traffic splitting trên Istio/Ingress: `kubectl get virtualservice checkout-vsvc -o yaml`

## 8. Anti-Patterns & Common Traps
- **Chuyển thẳng từ 0% lên 100% không có bước dừng**: Phá hỏng mục tiêu của Canary Release.
- **Đánh giá Canary khi chưa có traffic**: Phân tích metric trên mẫu dữ liệu 0 request dẫn tới false positive.
- **Triển khai breaking schema change đồng thời với Canary**: Khiến Stable Pods chết khi đọc dữ liệu mới.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Cấu hình Rollout có đầy đủ chiến lược Canary và AnalysisTemplate.
- QG-09: Thời gian tự động rollback khi có lỗi dưới 30 giây.
- QG-11: Tỷ lệ lỗi người dùng trong toàn bộ quá trình phát hành không vượt quá 0.1%.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi deploy.

## 10. Security & Safety Boundaries
- Bảo vệ endpoint Canary không bị kẻ xấu khai thác lỗi zero-day trước khi vá rộng rãi.
- Cô lập logs và audit trail của từng phiên bản để phục vụ điều tra sự cố.
- Không bao giờ lưu trữ hardcoded secret hoặc cấp quyền quá mức (over-permissioned IAM).

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Môi trường Cloud & Container**: Hỗ trợ Docker, Kubernetes (EKS/GKE/AKS), Terraform/OpenTofu, OpenTelemetry.

## 12. Deliverables & Output Artifacts
- Tệp định nghĩa `rollout.yaml` và `analysis-template.yaml`.
- Biểu đồ Dashboard theo dõi tiến trình phân bổ traffic và tỉ lệ lỗi.
- Báo cáo kết quả phân tích rollout sau khi hoàn tất.

## 13. Related & Complementary Skills
- `dex-service-mesh-networking`: Quản trị routing và traffic splitting trên Service Mesh.
- `dex-slo-error-budgets`: Xác định ngưỡng lỗi cho phép dựa trên Error Budget.
- `dex-incident-postmortems`: Phân tích nguyên nhân nếu rollout thất bại.

## 14. Realistic Usage Example
### Tình huống thực tế:
Đội ngũ kỹ sư phát hành bản cập nhật lớn cho microservice Checkout. Sử dụng `dex-zero-downtime-rollouts` với Argo Rollouts, họ phân bổ 10% lưu lượng trong 10 phút. Hệ thống tự động truy vấn Prometheus; khi phát hiện P99 latency của Canary tăng từ 120ms lên 450ms, bộ máy phân tích tự động kích hoạt Abort, đưa 100% traffic về Stable ngay lập tức mà không làm gián đoạn giao dịch của khách hàng.
