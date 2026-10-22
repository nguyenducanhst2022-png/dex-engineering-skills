---
name: dex-kubernetes-deployment
description: Design, deploy, and manage production Kubernetes workloads including Deployments, StatefulSets, DaemonSets, resource requests/limits, liveness/readiness/startup probes, PodDisruptionBudgets, and rolling updates. Use when deploying or hardening apps on Kubernetes.
---

# dex-kubernetes-deployment

## 1. Purpose & Scope
Thiết kế, định nghĩa và triển khai các tài nguyên Kubernetes đạt chuẩn Enterprise; thiết lập chiến lược cập nhật RollingUpdate không gián đoạn, cấu hình các probes (Startup, Liveness, Readiness), xác lập chính xác Resource Requests/Limits để tránh OOMKilled hoặc CPU throttling, thiết lập PodDisruptionBudget (PDB), Affinity, Topology Spread Constraints và quản lý cấu hình qua ConfigMaps / Secrets.

## 2. When to Use
- Khi triển khai dịch vụ mới lên cụm Kubernetes (EKS, GKE, AKS, On-premise).
- Khi Pod bị OOMKilled (Exit Code 137), CrashLoopBackOff hoặc gián đoạn dịch vụ khi scale Pod.
- Khi cấu hình các quy chuẩn vận hành cao cấp: Graceful Shutdown, PDB và Zero-downtime rolling update.

## 3. When NOT to Use
- Xây dựng container image (dùng `dex-container-image-engineering`).
- Thiết lập cụm cluster K8s từ đầu (dùng `dex-infrastructure-as-code`).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Container image URL kèm SHA256 digest.
- Yêu cầu tài nguyên tính toán (CPU, Memory baseline và peak).
- Cấu hình biến môi trường, ConfigMaps và External Secrets.
- **Điều kiện tiên quyết**:
- Cụm Kubernetes phiên bản 1.25+ sẵn sàng.
- `kubectl` hoặc Helm / Kustomize được cấu hình với quyền hạn namespace tương ứng.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- **Probe Lifecycle Triad**: Startup Probe (chờ app khởi động chậm), Liveness Probe (tự động khởi động lại khi deadlock), Readiness Probe (loại bỏ Pod khỏi Service endpoints khi quá tải).
- **QoS Classes (Guaranteed vs Burstable)**: Đặt Request = Limit cho các workload nhạy cảm latency để đạt QoS Guaranteed, tránh bị K8s evict khi node thiếu RAM.
- **Graceful Termination Lifecycle**: Gửi cờ SIGTERM, chờ xử lý nốt in-flight requests (`terminationGracePeriodSeconds: 60`), hoàn tất dọn dẹp trước khi K8s gửi SIGKILL.
- **Quy tắc quyết định kỹ thuật**:
- **Bắt Buộc Khai Báo Requests & Limits**: Mọi container trong Pod phải có requests.cpu, requests.memory, limits.cpu, limits.memory.
- **PodDisruptionBudget Bắt Buộc**: Mọi service phục vụ người dùng phải có `PodDisruptionBudget` với `minAvailable: 1` hoặc `maxUnavailable: 25%`.
- **Không Dùng Default Namespace**: Triển khai tài nguyên vào namespace phân định rõ ràng.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Service trả về lỗi 502/504 khi deploy version mới**: Pod mới được đưa vào Service trước khi server lắng nghe cổng -> Khắc phục: Cấu hình `readinessProbe` chính xác và thêm preStop hook `sleep 5` để kịp cập nhật iptables/kube-proxy.
- **Pod bị restart liên tục (CrashLoopBackOff)**: Liveness probe gọi nhầm endpoint kiểm tra database bên ngoài -> Khắc phục: Liveness probe chỉ kiểm tra process local nội tại (`/healthz/liveness`).

## 6. Step-by-Step Execution Workflow
1. Khảo sát yêu cầu tài nguyên, xác định loại workload (Deployment cho stateless, StatefulSet cho database/queue).
2. Định nghĩa Deployment manifest với RollingUpdate: `maxSurge: 25%`, `maxUnavailable: 0`.
3. Cấu hình Startup, Liveness và Readiness Probes với `initialDelaySeconds` và `failureThreshold` phù hợp.
4. Xác lập `resources.requests` và `resources.limits` dựa trên profile tải thực tế.
5. Thiết lập `PodDisruptionBudget` và `topologySpreadConstraints` để phân tán Pod đều qua các Availability Zones.
6. Cấu hình bảo mật `securityContext`: `runAsNonRoot: true`, `allowPrivilegeEscalation: false`, `readOnlyRootFilesystem: true`.
7. Triển khai qua Kustomize/Helm và xác minh trạng thái rollout: `kubectl rollout status deployment/myapp`.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: payment-service
  namespace: core
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 0
  selector:
    matchLabels:
      app: payment-service
  template:
    metadata:
      labels:
        app: payment-service
    spec:
      terminationGracePeriodSeconds: 45
      securityContext:
        runAsNonRoot: true
        runAsUser: 10001
        fsGroup: 10001
      containers:
      - name: payment-api
        image: registry.example.com/payment:v2.4.1
        resources:
          requests:
            cpu: "250m"
            memory: "512Mi"
          limits:
            cpu: "1000m"
            memory: "1024Mi"
        securityContext:
          readOnlyRootFilesystem: true
          allowPrivilegeEscalation: false
        ports:
        - containerPort: 8080
        readinessProbe:
          httpGet:
            path: /healthz/ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
        livenessProbe:
          httpGet:
            path: /healthz/live
            port: 8080
          periodSeconds: 10
```

### Lệnh xác minh & thực thi:
- Kiểm tra tính hợp lệ của manifest: `kubectl apply --dry-run=client -f deployment.yaml`
- Xác minh trạng thái rollout: `kubectl rollout status deployment/payment-service -n core`
- Kiểm tra tài nguyên thực tế: `kubectl top pods -n core -l app=payment-service`
- Kiểm tra sự kiện cảnh báo: `kubectl get events -n core --sort-by='.metadata.creationTimestamp'`

## 8. Anti-Patterns & Common Traps
- **Bỏ qua Readiness Probe**: Khiến traffic được điều hướng tới Pod khi app chưa kết nối xong Database.
- **Không đặt Memory Limit**: Một Pod bị memory leak sẽ ngốn cạn RAM của toàn bộ Node vật lý, gây crash các Pod hàng xóm.
- **Liveness Probe phụ thuộc vào Third-Party Service**: Nếu Redis chết, toàn bộ Pod app bị K8s kill liên tục.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Deployment manifest khai báo đầy đủ 3 loại probes và resource constraints.
- QG-05: PodDisruptionBudget được áp dụng thành công.
- QG-11: Quá trình rollout diễn ra với tỷ lệ lỗi HTTP 5xx bằng 0 (Zero Downtime).
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi deploy.

## 10. Security & Safety Boundaries
- Kích hoạt `securityContext.allowPrivilegeEscalation = false`.
- Tuyệt đối cấm mount Docker socket (`/var/run/docker.sock`) vào application Pods.
- Không bao giờ lưu trữ hardcoded secret hoặc cấp quyền quá mức (over-permissioned IAM).

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Môi trường Cloud & Container**: Hỗ trợ Docker, Kubernetes (EKS/GKE/AKS), Terraform/OpenTofu, OpenTelemetry.

## 12. Deliverables & Output Artifacts
- Tệp cấu hình `deployment.yaml`, `service.yaml`, `pdb.yaml` chuẩn hóa.
- Báo cáo xác thực rollout không gián đoạn.

## 13. Related & Complementary Skills
- `dex-container-image-engineering`: Chuẩn bị container image cho workload.
- `dex-zero-downtime-rollouts`: Chiến lược điều phối traffic nâng cao (Canary / Blue-Green).
- `dex-slo-error-budgets`: Đo lường tác động của deployment tới SLA/SLO.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư được giao triển khai một API thanh toán lên Kubernetes. Áp dụng `dex-kubernetes-deployment`, kỹ sư xây dựng manifest Kustomize, thiết lập rolling update không cho phép unavailable (`maxUnavailable: 0`), gắn probes kiểm tra sâu trạng thái kết nối pool database, thiết lập PDB chặn tình trạng cụm node upgrade làm gián đoạn toàn bộ Pods, và chạy `kubectl rollout status` xác nhận rollout an toàn 100%.
