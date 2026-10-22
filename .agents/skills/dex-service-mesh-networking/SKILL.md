---
name: dex-service-mesh-networking
description: Architect and operate service mesh networking (Istio, Linkerd, Envoy) with mutual TLS (mTLS), fine-grained traffic routing, circuit breaking, fault injection, and telemetry. Use when securing and managing inter-service microservice communications.
---

# dex-service-mesh-networking

## 1. Purpose & Scope
Thiết kế, triển khai và quản trị hạ tầng mạng Service Mesh (Istio / Linkerd / Envoy Data Plane) cho kiến trúc microservices; thực thi mã hóa toàn diện trên đường truyền bằng mutual TLS (mTLS) tự động xoay vòng chứng chỉ, định tuyến lưu lượng thông minh (Traffic Shifting, Header Routing), cấu hình Circuit Breaking, Retry Policy, Rate Limiting và tiêm lỗi (Fault Injection) để kiểm thử độ bền hệ thống.

## 2. When to Use
- Khi hệ thống mở rộng thành nhiều microservice cần giao tiếp bảo mật không tin cậy (Zero Trust Network).
- Khi cần mã hóa mTLS giữa các dịch vụ mà không muốn sửa mã nguồn ứng dụng.
- Khi cần cấu hình Circuit Breaker và ngắt kết nối nhanh (Fast Failure) để ngăn chặn lỗi dây chuyền (Cascading Failure).

## 3. When NOT to Use
- Ứng dụng nguyên khối (Monolith) chỉ có 1 service duy nhất (không cần mạng mesh phức tạp).
- Khắc phục sự cố mạng ở mức socket/packet máy chủ cơ bản (dùng `dex-network-troubleshooting`).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Cấu trúc mạng dịch vụ và danh sách các service cần đưa vào Mesh.
- Chính sách bảo mật (mTLS PERMISSIVE vs STRICT).
- Ngưỡng circuit breaker (Max connections, consecutive 5xx errors, ejection time).
- **Điều kiện tiên quyết**:
- Cụm Kubernetes có Istio Control Plane (istiod) hoặc Linkerd Control Plane đang hoạt động.
- Các namespace mục tiêu được gắn nhãn injection: `istio-injection=enabled`.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- **Sidecar Proxy Interception**: Mỗi Pod ứng dụng được đính kèm một Envoy proxy tự động chặn và xử lý toàn bộ traffic vào/ra (inbound/outbound).
- **Zero-Trust Mutual TLS (mTLS)**: Cả client và server đều xác thực danh tính của nhau thông qua chứng chỉ X.509 được cấp phát ngắn hạn bởi SPIFFE/SPIRE hoặc Citadel.
- **Outlier Detection & Circuit Breaking**: Tự động loại bỏ các instance dịch vụ bị suy giảm hiệu năng (trả về liên tiếp lỗi 503) ra khỏi load balancing pool trong một khoảng thời gian.
- **Quy tắc quyết định kỹ thuật**:
- **Strict mTLS Trong Production**: Chuyển đổi chính sách PeerAuthentication sang chế độ `STRICT` để từ chối mọi traffic không mã hóa.
- **Luôn Khai Báo Connection Pool & Outlier Detection**: Mọi dịch vụ upstream quan trọng đều phải có `DestinationRule` hạn chế số kết nối tối đa.
- **Tránh Retry Bão Hòa**: Không cấu hình retry cho các request không idempotent (POST, PATCH) trừ khi có Idempotency-Key.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Lỗi kết nối sau khi bật STRICT mTLS**: Một service cũ chưa được gắn sidecar proxy cố kết nối bằng plain text -> Khắc phục: Sử dụng chế độ `PERMISSIVE` trong giai đoạn chuyển đổi và quét danh sách Pod thiếu proxy bằng Kiali.
- **Vòng lặp retry làm nghẽn toàn bộ hạ tầng mạng**: Do timeout quá ngắn và retry 5 lần liên tiếp -> Khắc phục: Giới hạn retry tối đa 2 lần kèm timeout tăng dần.

## 6. Step-by-Step Execution Workflow
1. Gắn nhãn tự động inject sidecar cho namespace ứng dụng: `kubectl label namespace core istio-injection=enabled`.
2. Thiết lập chính sách `PeerAuthentication` với chế độ `STRICT` trên toàn namespace.
3. Định nghĩa `VirtualService` để quản lý routing, URI prefix rewriting, timeout và retry policy.
4. Cấu hình `DestinationRule` xác lập thuật toán cân bằng tải (LEAST_REQUEST), Circuit Breaking và Outlier Detection.
5. Thực hiện tiêm lỗi (Fault Injection: delay 2s, abort 500 trên 10% traffic) để kiểm tra khả năng phục hồi của client.
6. Quan sát sơ đồ topo mạng và độ trễ trên giao diện Kiali / Jaeger / Prometheus.
7. Thiết lập `AuthorizationPolicy` kiểm soát chi tiết: Service A chỉ được phép gọi Service B qua đường dẫn `/api/v1/orders`.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```yaml
# DestinationRule với Circuit Breaking và Outlier Detection
apiVersion: networking.istio.io/v1beta1
kind: DestinationRule
metadata:
  name: inventory-circuit-breaker
  namespace: core
spec:
  host: inventory-service
  trafficPolicy:
    tls:
      mode: ISTIO_MUTUAL
    connectionPool:
      tcp:
        maxConnections: 100
      http:
        http1MaxPendingRequests: 50
        maxRequestsPerConnection: 10
    outlierDetection:
      consecutive5xxErrors: 3
      interval: 10s
      baseEjectionTime: 30s
      maxEjectionPercent: 50
```

### Lệnh xác minh & thực thi:
- Kiểm tra trạng thái đồng bộ Envoy proxy: `istioctl proxy-status`
- Kiểm tra cấu hình mTLS giữa 2 pods: `istioctl authn tls-check <pod-name>.core`
- Xem log access chi tiết của Envoy: `kubectl logs <pod-name> -c istio-proxy --tail=50`
- Phân tích cấu hình lỗi: `istioctl analyze -n core`

## 8. Anti-Patterns & Common Traps
- **Bật mesh mà không giám sát dung lượng CPU/RAM của Sidecar**: Envoy proxy có thể tốn từ 0.2 đến 0.5 CPU nếu traffic quá lớn.
- **Dùng wildcard `*` trong VirtualService**: Gây xung đột định tuyến giữa các đội ngũ phát triển khác nhau.
- **Không cấu hình Circuit Breaker**: Một service downstream chết kéo sập toàn bộ chuỗi dịch vụ upstream.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Tất cả traffic nội bộ đều được mã hóa mTLS STRICT thành công.
- QG-07: Outlier Detection tự động cô lập instance lỗi trong vòng dưới 10 giây.
- QG-10: Cấu hình `istioctl analyze` trả về 0 cảnh báo lỗi cú pháp.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi deploy.

## 10. Security & Safety Boundaries
- Nghiêm cấm bypass sidecar proxy qua direct IP routing trừ khi có ngoại lệ an ninh được phê duyệt.
- Cấu hình `AuthorizationPolicy` chỉ cho phép các service có ServiceAccount hợp lệ kết nối.
- Không bao giờ lưu trữ hardcoded secret hoặc cấp quyền quá mức (over-permissioned IAM).

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Môi trường Cloud & Container**: Hỗ trợ Docker, Kubernetes (EKS/GKE/AKS), Terraform/OpenTofu, OpenTelemetry.

## 12. Deliverables & Output Artifacts
- Các tệp manifest `virtual-service.yaml`, `destination-rule.yaml`, `peer-authentication.yaml`.
- Báo cáo phân tích `istioctl analyze` sạch lỗi.
- Sơ đồ lưu lượng dịch vụ trực quan trên Kiali.

## 13. Related & Complementary Skills
- `dex-zero-downtime-rollouts`: Phối hợp VirtualService để chuyển dịch traffic Canary.
- `dex-distributed-tracing`: Tận dụng trace context do Envoy proxy tự động lan truyền.
- `dex-network-troubleshooting`: Xử lý sự cố mạng khi sidecar proxy gặp lỗi.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư kiến trúc cần bảo vệ mạng lưới 20 microservice chống lại tấn công nghe lén nội bộ và lỗi domino. Áp dụng `dex-service-mesh-networking`, họ triển khai Istio, kích hoạt STRICT mTLS, tạo DestinationRule với Circuit Breaking ngắt instance trả về 3 lỗi 5xx liên tiếp trong 30s, đồng thời viết AuthorizationPolicy giới hạn chỉ Payment Service mới được gọi Order Service, nâng cao mức độ bảo mật Zero Trust.
