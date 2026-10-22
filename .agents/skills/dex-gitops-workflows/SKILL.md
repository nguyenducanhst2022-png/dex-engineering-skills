---
name: dex-gitops-workflows
description: Implement declarative continuous deployment and reconciliation using GitOps engines (ArgoCD, FluxCD), managing environment drift, secrets, and rollbacks. Use to standardize Kubernetes application delivery.
---

# dex-gitops-workflows

## 1. Purpose & Scope
Thiết kế, xây dựng và quản trị quy trình triển khai ứng dụng khai báo liên tục (GitOps Workflows: ArgoCD, FluxCD) trên cụm Kubernetes; đồng bộ tự động trạng thái mong muốn từ Git Repository, phát hiện và tự sửa chữa sai lệch cấu hình (Drift Detection & Self-healing), tích hợp quản lý secrets an toàn và hỗ trợ rollback tức thì.

## 2. When to Use
- Triển khai nhiều ứng dụng microservices trên các cụm Kubernetes (EKS, GKE, On-prem).
- Quá trình deploy thủ công bằng lệnh `kubectl apply` từ máy dev gây ra sai lệch cấu hình giữa các môi trường.
- Cần lịch sử kiểm toán (Audit Trail) minh bạch cho mọi thay đổi hạ tầng và ứng dụng thông qua Git commits.

## 3. When NOT to Use
- Không áp dụng GitOps cho các ứng dụng monolith đơn giản chỉ chạy trên một máy chủ ảo EC2 đơn lẻ.
- Không lưu trữ plaintext credentials hoặc passwords trực tiếp vào Git repository.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Git Repository chứa cấu hình khai báo (Kustomize overlays hoặc Helm charts).
- Cụm Kubernetes mục tiêu và quyền truy cập cluster.
- Giải pháp mã hóa bí mật (SealedSecrets, SOPS, External Secrets Operator).
- **Điều kiện tiên quyết**:
- ArgoCD hoặc FluxCD controller đã được cài đặt và vận hành trên cụm Kubernetes.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Git as the Single Source of Truth: Trạng thái của cụm Kubernetes phải phản chiếu chính xác 100% nội dung khai báo trong Git repo.
- Reconciliation Loop: Controller liên tục so sánh trạng thái thực tế (Live state) với trạng thái mong muốn trong Git (Target state); nếu có ai sửa tay bằng `kubectl`, controller sẽ tự động ghi đè về trạng thái của Git (Self-healing).
- External Secrets Operator: Lấy secret từ AWS Secrets Manager/Vault và tạo Kubernetes Secret động.
- **Quy tắc quyết định kỹ thuật**:
- Cấu hình `autoSync` kèm `prune: true` để tự động dọn dẹp các tài nguyên bị xóa trong Git.
- Bắt buộc kích hoạt `selfHeal: true` để ngăn chặn các kỹ sư sửa đổi trực tiếp vào cụm cluster.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Cấu hình Git sai cú pháp YAML khiến ArgoCD liên tục sync lỗi làm nghẽn CPU của API Server.

## 6. Step-by-Step Execution Workflow
1. Cấu trúc GitOps repository tách biệt giữa Code Repo và Config/Manifests Repo.
2. Tổ chức manifests theo mô hình Kustomize (base và các overlays cho dev, staging, prod).
3. Định nghĩa đối tượng `Application` hoặc `ApplicationSet` trong ArgoCD.
4. Tích hợp External Secrets Operator để quản lý secret an toàn.
5. Thiết lập thông báo trạng thái đồng bộ hóa qua Slack/Teams.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```yaml
# ArgoCD Application Definition
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: payment-service-prod
  namespace: argocd
spec:
  project: default
  source:
    repoURL: 'https://github.com/company/gitops-manifests.git'
    targetRevision: main
    path: apps/payment-service/overlays/prod
  destination:
    server: 'https://kubernetes.default.svc'
    namespace: payment
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```

### Lệnh xác minh & thực thi:
```bash
# Kiểm tra trạng thái đồng bộ của ứng dụng qua ArgoCD CLI
argocd app get payment-service-prod
```

## 8. Anti-Patterns & Common Traps
- Chạy lệnh `kubectl edit` hoặc `kubectl apply` trực tiếp trên cụm production được quản lý bởi GitOps.
- Lưu trữ file `.env` chứa mật khẩu thật vào Git mà không mã hóa.

## 9. Quality Gates & Acceptance Criteria
- 100% tài nguyên trên Kubernetes được đồng bộ ở trạng thái `Synced` và `Healthy`.
- Mọi commit vào nhánh chính của GitOps repo phải có chữ ký GPG hoặc qua PR có phê duyệt.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Quyền truy cập vào giao diện web của ArgoCD phải tích hợp SSO (OAuth2/OIDC) kèm RBAC theo nhóm.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ thống hỗ trợ**: Cloud Runtimes (AWS Lambda, Cloudflare Workers, Kubernetes), Linux, Windows 11.

## 12. Deliverables & Output Artifacts
- Cấu trúc thư mục GitOps Kustomize chuẩn mực.
- File manifest ArgoCD Application / Flux Kustomization hoàn chỉnh.

## 13. Related & Complementary Skills
dex-kubernetes-policy-enforcement, dex-environment-promotion, dex-platform-service-catalog

## 14. Realistic Usage Example
### Tình huống thực tế:
Một kỹ sư mới vô tình chạy lệnh xóa nhầm Namespace trên cụm Kubernetes Staging. Nhờ cơ chế Self-healing của ArgoCD, toàn bộ 25 microservices, ingress và configs đã được tự động dựng lại nguyên vẹn sau 45 giây từ Git repository mà không mất công sức phục hồi thủ công.
