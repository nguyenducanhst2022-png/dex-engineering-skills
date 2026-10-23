---
name: dex-model-serving-canary-rollouts
description: Implement progressive canary rollouts, shadow traffic mirroring, and automated latency/accuracy rollbacks for production ML model serving clusters. Use when updating inference models without service disruption.
---

# dex-model-serving-canary-rollouts

## 1. Purpose & Scope
Triển khai chiến lược phát hành chim hoàng oanh (Canary Rollout), nhân bản lưu lượng bóng (Shadow Traffic) và tự động khôi phục (Rollback) dựa trên độ trễ và độ chính xác suy luận cho các cụm phục vụ mô hình Machine Learning; bảo đảm không gián đoạn dịch vụ sản xuất.

## 2. When to Use
- Khi nâng cấp phiên bản mô hình mới (v2) thay thế mô hình đang chạy (v1) trên môi trường live.
- Khi cần đo lường độ trễ p99 và mức tiêu hao GPU thực tế của mô hình mới dưới tải người dùng thật.
- Khi muốn xác minh hành vi suy luận của mô hình mới mà không gây ảnh hưởng trực tiếp đến trải nghiệm người dùng (Shadow Deployment).

## 3. When NOT to Use
- Khi triển khai mô hình nội bộ thử nghiệm (sandbox) không có lưu lượng truy cập thực tế.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Cụm phục vụ mô hình (Triton Inference Server, vLLM, KServe, TorchServe), Ingress/Service Mesh (Istio, Envoy).
- **Quyền hạn truy cập:** Quyền cấu hình định tuyến lưu lượng mạng và triển khai container mô hình.

## 5. Core Concepts & Taxonomy
- **Shadow Mirroring:** Sao chép 100% request thực tế gửi tới cả hai mô hình nhưng chỉ trả kết quả của mô hình hiện tại về cho client; kết quả của mô hình bóng được ghi log để phân tích.
- **Progressive Traffic Shifting:** Chuyển dần lưu lượng theo tỷ lệ phần trăm (1% -> 5% -> 25% -> 100%) kèm theo các tiêu chí đo lường an toàn (Health Checks).
- **Automated Anomaly Rollback:** Tự động cắt toàn bộ lưu lượng về phiên bản cũ nếu tỷ lệ lỗi HTTP 5xx > 1% hoặc độ trễ p99 vượt quá 200ms.

## 6. Step-by-Step Execution Workflow
1. Khởi tạo phiên bản dịch vụ mô hình mới (Canary/Shadow Pods) trong cụm Kubernetes.
2. Cấu hình Ingress/Service Mesh sao chép 100% lưu lượng live sang mô hình Shadow để đánh giá độ ổn định.
3. Đối soát độ trễ p99, tỷ lệ lỗi và mức tiêu hao GPU của mô hình Shadow với mô hình chính thức.
4. Mở dần lưu lượng thực tế sang Canary: bắt đầu từ 1%, tăng lên 5%, 25%, và 50% sau mỗi chu kỳ kiểm tra 15 phút.
5. Giám sát liên tục các cảnh báo độ lệch phân phối kết quả dự đoán và chỉ số kinh doanh.
6. Chuyển hoàn toàn 100% lưu lượng sang mô hình mới hoặc kích hoạt rollback tự động nếu phát hiện bất thường.

## 7. Concrete Examples
### Cấu hình Shadow Traffic và Canary Routing bằng Istio VirtualService:
```yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: ml-inference-routing
spec:
  hosts:
  - "inference.internal.domain"
  http:
  - match:
    - uri:
        prefix: /v1/predict
    # Nhân bản lưu lượng sang mô hình mới để kiểm tra an toàn
    mirror:
      host: ml-serving-canary.internal.domain
    mirrorPercentage:
      value: 100.0
    # Phục vụ người dùng thực tế bằng mô hình hiện tại ổn định
    route:
    - destination:
        host: ml-serving-stable.internal.domain
        weight: 95
    - destination:
        host: ml-serving-canary.internal.domain
        weight: 5
```

## 8. Anti-Patterns & Common Traps
- **Big Bang Model Swapping:** Chuyển đổi 100% lưu lượng truy cập sang mô hình mới ngay lập tức mà không qua kiểm tra shadow.
- **Ignoring Cold Start Latency:** Đẩy ngay tải cao vào pod mô hình mới khi GPU cache chưa được khởi động đầy đủ gây sập cụm serving.
- **Manual Rollback Reliance:** Phụ thuộc vào việc kỹ sư phải ngồi theo dõi màn hình để gõ lệnh rollback thủ công khi có sự cố.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Tỷ lệ lỗi 5xx trên mô hình canary giữ ở mức < 0.1% trong suốt 60 phút theo dõi.
- **QG-04**: Độ trễ suy luận p99 của mô hình mới không vượt quá 120% so với mô hình baseline.
- **QG-07**: Quy trình rollback tự động hoàn tất trong vòng dưới 30 giây khi vượt ngưỡng cảnh báo.

## 10. Security & Safety Boundaries
- Đảm bảo dữ liệu request nhân bản trong luồng shadow được ẩn danh hóa và tuân thủ các quy định bảo mật dữ liệu sản xuất.

## 11. Platform Adapters
- **Inference Platforms**: KServe, Seldon Core, Triton, vLLM, TorchServe.
- **Service Mesh**: Istio, Envoy, Linkerd.

## 12. Deliverables & Output Artifacts
- Cấu hình khai báo Canary & Shadow Routing (Kubernetes / Istio).
- Kịch bản tự động tăng tải và rollback theo dõi metric.
- Báo cáo phân tích so sánh hiệu năng giữa hai phiên bản mô hình.

## 13. Related & Complementary Skills
dex-online-offline-feature-parity, dex-batch-inference-pipeline-tuning, dex-inference-provider-rate-controls

## 14. Realistic Usage Example
```powershell
# Triển khai canary VirtualService vào cụm Kubernetes
kubectl apply -f k8s/ml-canary-routing.yaml

# Theo dõi metric độ trễ và tỷ lệ lỗi thời gian thực bằng Prometheus CLI
curl -s "http://prometheus:9090/api/v1/query?query=histogram_quantile(0.99,sum(rate(inference_duration_bucket[5m]))by(le,version))"
```
