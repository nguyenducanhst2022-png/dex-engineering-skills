---
name: dex-kubernetes-secret-delivery
description: Architect, enforce, and audit secure secret delivery to Kubernetes workloads. Integrate External Secrets Operator, Vault Agent sidecars, and verify safe credential rotation.
---

# dex-kubernetes-secret-delivery

## 1. Purpose & Scope
Thiết kế, tích hợp và kiểm toán cơ chế phân phối bí mật an toàn cho các ứng dụng chạy trên Kubernetes (Kubernetes Secret Delivery Architecture); loại bỏ hoàn toàn việc lưu trữ bí mật dạng plaintext trong kho mã nguồn Git; tích hợp External Secrets Operator (ESO), HashiCorp Vault Agent Sidecar hoặc CSI Secret Store Driver; thực thi nguyên tắc đặc quyền tối thiểu (Least Privilege RBAC), cấp phát bí mật qua bộ nhớ tạm (tmpfs memory volumes) và tự động tải lại ứng dụng khi chứng chỉ/khóa được xoay vòng (Zero-Downtime Secret Rotation).

## 2. When to Use
- Khi triển khai các ứng dụng microservices trên cụm Kubernetes yêu cầu truy cập mật khẩu CSDL, API Token, hoặc chứng chỉ TLS.
- Khi chuyển đổi từ cơ chế Secret tĩnh của Kubernetes (base64 mã hóa yếu) sang cơ chế quản lý tập trung từ Cloud KMS (AWS Secrets Manager, Azure Key Vault, HashiCorp Vault).
- Khi kiểm toán an ninh phát hiện bí mật bị lộ trong tệp cấu hình YAML hoặc lịch sử commit Git.

## 3. When NOT to Use
- Khi cấu hình các thông số không nhạy cảm (như URL public, cổng dịch vụ, tên môi trường - nên dùng ConfigMap thông thường).
- Khi ứng dụng chạy trên môi trường máy chủ đơn lẻ không sử dụng bộ điều phối container Kubernetes.

## 4. Prerequisites & Input Context
- **Hạ tầng cụm:** Kubernetes 1.25+, Helm 3.0+.
- **Hệ thống quản lý khóa:** AWS Secrets Manager, HashiCorp Vault, hoặc GCP Secret Manager.

## 5. Core Concepts & Taxonomy
- **External Secrets Operator (ESO):** Bộ điều khiển Kubernetes Kubernetes Controller đồng bộ hóa dữ liệu từ các nhà cung cấp bên ngoài (External APIs) thành các native `Secret` trong cluster.
- **tmpfs In-Memory Volume:** Cơ chế gắn thư mục bí mật vào Pod dưới dạng RAM ảo, bảo đảm bí mật không bao giờ bị ghi xuống ổ đĩa cứng của node Kubernetes.
- **Reloader Controller:** Công cụ tự động kích hoạt Rolling Restart cho Deployment khi các Secret hoặc ConfigMap được cập nhật giá trị mới.

## 6. Step-by-Step Execution Workflow
1. Cài đặt External Secrets Operator trên cụm thông qua Helm Chart chính thức.
2. Thiết lập định danh bảo mật `ClusterSecretStore` sử dụng Kubernetes ServiceAccount kết nối tới AWS IAM Role (IRSA) hoặc Vault Role.
3. Định nghĩa đối tượng `ExternalSecret` ánh xạ từng khóa từ Cloud Secrets Manager sang Kubernetes Secret nội bộ.
4. Gắn Secret vào Pod thông qua Volume Mount (`mountPath: /var/run/secrets/app`) hoặc biến môi trường tham chiếu.
5. Cấu hình cờ `stakater.com/auto: "true"` trên Pod template để tự động reload khi secret thay đổi.
6. Kiểm tra quyền truy cập của Pod và khẳng định tiến trình bên trong Pod không thể đọc được secret của các namespace khác.

## 7. Concrete Examples
### Cau hinh ExternalSecret dong bo hoa tu AWS Secrets Manager:
```yaml
apiVersion: external-secrets.io/v1beta1
kind: ClusterSecretStore
metadata:
  name: aws-secretsmanager-store
spec:
  provider:
    aws:
      service: SecretsManager
      region: us-east-1
      auth:
        jwt:
          serviceAccountRef:
            name: eso-service-account
            namespace: external-secrets
---
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: database-credentials
  namespace: production
spec:
  refreshInterval: 1h # Tu dong quet xoay vong bi mat moi gio
  secretStoreRef:
    name: aws-secretsmanager-store
    kind: ClusterSecretStore
  target:
    name: db-app-secret
    creationPolicy: Owner
  data:
    - secretKey: DB_PASSWORD
      remoteRef:
        key: production/database
        property: password
    - secretKey: DB_USERNAME
      remoteRef:
        key: production/database
        property: username
```

## 8. Anti-Patterns & Common Traps
- **Committing Base64 Secrets in Git:** Đẩy các tệp `Secret.yaml` chứa chuỗi mã hóa base64 lên Git với suy nghĩ sai lầm rằng base64 là một hình thức mã hóa bảo mật.
- **Passing Secrets via Process CLI Arguments:** Truyền mật khẩu dưới dạng tham số dòng lệnh `args: ["--password", "$(SECRET)"]` khiến mật khẩu hiển thị rõ ràng trong lệnh `ps aux` hoặc Kubernetes API.
- **Root-Accessible Shared Volumes:** Gắn secret vào volume nhưng để quyền tệp là `0777` cho phép bất kỳ container nào cùng Pod đều đọc được dữ liệu nhạy cảm.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: 100% bí mật trong cụm được đồng bộ tự động từ External Secrets Store, 0 bí mật tĩnh trong Git.
- **QG-02**: Mọi volume gắn secret đều có quyền phân quyền tệp giới hạn nghiêm ngặt `defaultMode: 0400`.
- **QG-03**: Quá trình xoay vòng bí mật (Secret Rotation) kích hoạt cập nhật Pod tự động mà không gây gián đoạn dịch vụ.

## 10. Security & Safety Boundaries
- Bật mã hóa dữ liệu Secret khi lưu trữ tại tầng etcd (Encryption at Rest with KMS Provider) trên toàn cụm Kubernetes.

## 11. Platform Adapters
- **Runtimes**: External Secrets Operator, HashiCorp Vault Agent, Kubernetes CSI Driver, AWS Secrets Manager.

## 12. Deliverables & Output Artifacts
- Lược đồ khai báo External Secrets chuẩn mẫu (`external_secret_template.yaml`).
- Kịch bản kiểm toán rà soát cấu hình phân quyền Secret RBAC (`audit_k8s_secrets.sh`).

## 13. Related & Complementary Skills
dex-infrastructure-policy-as-code, dex-cloud-database-failover-drills, dex-platform-selfservice-templates

## 14. Realistic Usage Example
```bash
# Kiem tra trang thai dong bo hoa cua ExternalSecret
kubectl get externalsecret -n production -o wide
```
