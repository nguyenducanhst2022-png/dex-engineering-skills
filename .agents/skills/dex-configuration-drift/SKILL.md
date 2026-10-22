---
name: dex-configuration-drift
description: Detect, analyze, and reconcile configuration drift across Kubernetes GitOps (ArgoCD/Flux), cloud infrastructure (Terraform/OpenTofu), and application settings. Use when ensuring real-world environments match declared state.
---

# dex-configuration-drift

## 1. Purpose & Scope
Phát hiện, phân tích và tự động khắc phục hiện tượng sai lệch cấu hình (Configuration Drift Detection & Reconciliation) giữa trạng thái khai báo trong mã nguồn (Declared State trong Git/IaC) và trạng thái thực tế đang chạy trên môi trường hạ tầng (Live State trong Cloud/Kubernetes); quản lý công cụ GitOps (ArgoCD / Flux), lập lịch quét sai lệch tự động, gửi cảnh báo tức thì khi có can thiệp thủ công (Out-of-band ClickOps changes) và thực thi cơ chế tự phục hồi (Self-Healing).

## 2. When to Use
- Khi có người sửa đổi trực tiếp tài nguyên qua AWS Console hoặc lệnh `kubectl edit` trên môi trường production mà không qua Git.
- Khi pipeline Terraform báo lỗi xung đột vì hạ tầng thực tế đã bị ai đó thay đổi thủ công.
- Khi ứng dụng hoạt động khác biệt giữa 2 môi trường dù cùng sử dụng một tag phiên bản phát hành.

## 3. When NOT to Use
- Xây dựng module Terraform từ đầu (dùng `dex-infrastructure-as-code`).
- Quản lý rollout phiên bản ứng dụng (dùng `dex-zero-downtime-rollouts`).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Kho mã nguồn GitOps chứa manifests khai báo (Kubernetes YAML, Kustomize, Helm, Terraform HCL).
- Kết nối API tới hạ tầng thực tế (K8s API Server, AWS/GCP APIs).
- Ngưỡng cho phép sai lệch (Tolerations: ví dụ cờ auto-scaling replicas do HPA quản lý không tính là drift).
- **Điều kiện tiên quyết**:
- Hệ thống GitOps (ArgoCD / Flux) hoặc Terraform Cloud / Driftctl được cài đặt.
- Quyền đọc cấu hình hạ tầng trực tiếp.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- **Git as the Single Source of Truth**: Mọi cấu hình thực tế bắt buộc phải là hình ảnh phản chiếu 100% của Git; bất kỳ khác biệt nào xuất hiện trên cluster mà không có commit trong Git đều được coi là lỗi sai lệch (Drift).
- **Automated Drift Detection vs Self-Healing**: Phát hiện sai lệch (báo động cho kỹ sư) vs Tự động đồng bộ (ArgoCD tự động ghi đè lại trạng thái Git lên cluster, xóa sạch thay đổi thủ công trong 60 giây).
- **Intentional Drift Ignore Rules**: Phân biệt giữa sai lệch ngoài ý muốn và các trường hợp thay đổi động hợp lệ (như số lượng replica do HPA điều chỉnh hoặc metadata do cloud provider tự gán).
- **Quy tắc quyết định kỹ thuật**:
- **Bật Chế Độ Tự Phục Hồi (Self-Healing) Cho Production K8s**: Cấu hình ArgoCD với `selfHeal: true` và `prune: true` để triệt tiêu vĩnh viễn văn hóa 'ClickOps'.
- **Cấm Tuyệt Đối Phê Duyệt Drift Mà Không Cập Nhật Git**: Nếu thay đổi thủ công trong lúc xử lý sự cố khẩn cấp (Emergency Hotfix) được giữ lại, bắt buộc phải tạo PR đưa thay đổi đó ngược lại vào Git trong vòng 4 giờ.
- **Kiểm Tra Drift Hàng Ngày Cho IaC**: Thiết lập lịch chạy `terraform plan -detailed-exitcode` lúc 6h sáng mỗi ngày; nếu phát hiện drift, tự động tạo Issue cảnh báo đội ngũ.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **ArgoCD liên tục đồng bộ vô tận (Sync Loop)**: Do manifest Git khai báo `replicas: 3` nhưng trên cluster HPA lại tự động scale lên 10 Pod -> Khắc phục: Sử dụng cấu hình `ignoreDifferences` trong Application CRD của ArgoCD để bỏ qua trường `spec.replicas`.
- **Xóa nhầm tài nguyên do cờ `prune: true`**: Kỹ sư xóa nhầm 1 file manifest trong Git khiến ArgoCD xóa luôn database trên cluster -> Khắc phục: Bật cờ `prevent_destroy` và gán annotation `argocd.argoproj.io/sync-options: Delete=false` cho tài nguyên sống còn.

## 6. Step-by-Step Execution Workflow
1. Kết nối ArgoCD / Terraform với kho mã nguồn Git và cluster mục tiêu.
2. Cấu hình quy tắc loại trừ các trường động hợp lệ (`ignoreDifferences` cho replicas, resource limits tự scale).
3. Kích hoạt tính năng Auto-Sync và Self-Heal trên ArgoCD Application.
4. Thiết lập công cụ quét sai lệch hạ tầng đám mây (Driftctl hoặc scheduled GitHub Actions Terraform Plan).
5. Thiết lập webhook cảnh báo qua Slack khi trạng thái chuyển sang `OutOfSync`.
6. Khi phát hiện Drift: Trực quan hóa phần khác biệt (Diff Viewer: Red/Green) để xác định ai đã sửa trường gì.
7. Thực thi hành động: Hoặc kích hoạt Sync để đưa cluster về chuẩn Git, hoặc tạo PR commit thay đổi vào Git.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```yaml
# ArgoCD Application với tính năng Self-Healing và Ignore Differences
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: core-payment-api
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/myorg/gitops-manifests.git
    targetRevision: HEAD
    path: apps/payment/production
  destination:
    server: https://kubernetes.default.svc
    namespace: core
  syncPolicy:
    automated:
      prune: true
      selfHeal: true # Tự động hoàn nguyên nếu có ai sửa bằng kubectl edit
    syncOptions:
    - CreateNamespace=true
  ignoreDifferences:
  - group: apps
    kind: Deployment
    jsonPointers:
    - /spec/replicas # Bỏ qua số replicas do HPA tự động điều chỉnh
```

### Lệnh xác minh & thực thi:
- Kiểm tra trạng thái đồng bộ ArgoCD: `argocd app get core-payment-api --output json | jq .status.sync.status` (phải trả về `"Synced"`)
- Kiểm tra sai lệch Terraform qua exit code: `terraform plan -detailed-exitcode` (mã 0: không đổi, mã 2: có drift)
- Chạy quét toàn diện bằng driftctl: `driftctl scan --from tfstate+s3://my-bucket/terraform.tfstate`

## 8. Anti-Patterns & Common Traps
- **Tắt tính năng Auto-Sync trong thời gian dài rồi quên bật lại**: Khiến môi trường thực tế trôi dạt quá xa so với Git, không thể đồng bộ lại được.
- **Dùng quyền Root/Admin để chỉnh sửa trực tiếp trên Production**: Phá vỡ nguyên tắc quản trị thay đổi và kiểm toán.
- **Bỏ qua các thông báo OutOfSync từ hệ thống giám sát**: Coi thường cảnh báo dẫn tới sự cố khi có đợt phát hành mới.

## 9. Quality Gates & Acceptance Criteria
- QG-01: 100% các ứng dụng Kubernetes sản xuất được quản lý bằng ArgoCD/Flux ở chế độ Synced.
- QG-08: Thời gian tự động phục hồi khi có sai lệch (Self-Heal Time) dưới 180 giây.
- QG-11: Quét sai lệch hạ tầng Terraform không phát hiện bất kỳ tài nguyên mồ côi ngoài luồng nào.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi deploy.

## 10. Security & Safety Boundaries
- Khóa quyền ghi trực tiếp vào K8s API server trên production; chỉ cấp quyền ServiceAccount cho ArgoCD controller.
- Không lưu trữ credentials hạ tầng dạng plain text trong Git repository.
- Không bao giờ lưu trữ hardcoded secret hoặc cấp quyền quá mức (over-permissioned IAM).

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Môi trường Vận hành & Tuân thủ**: Hỗ trợ GDPR/CCPA tooling, SOC 2 / ISO 27001 automation, ArgoCD drift, RICE spreadsheets, Jira/GitHub triage.

## 12. Deliverables & Output Artifacts
- Tệp cấu hình GitOps Application với chính sách Self-Healing.
- Kịch bản quét sai lệch hạ tầng đám mây định kỳ.
- Báo cáo phân tích sai lệch và nhật ký hoàn nguyên tự động.

## 13. Related & Complementary Skills
- `dex-infrastructure-as-code`: Quản lý tài nguyên hạ tầng bằng Terraform.
- `dex-kubernetes-deployment`: Định nghĩa tài nguyên Kubernetes chuẩn hóa.
- `dex-compliance-control-mapping`: Chứng minh với kiểm toán viên rằng môi trường luôn khớp với mã nguồn đã duyệt.

## 14. Realistic Usage Example
### Tình huống thực tế:
Trong một ca trực đêm, một kỹ sư vận hành đã dùng lệnh `kubectl edit` để tạm thời tăng CPU limit của một Pod nhằm dập tắt cảnh báo quá tải, nhưng sau đó quên không báo lại cho đội ngũ. Nhờ áp dụng `dex-configuration-drift`, hệ thống ArgoCD phát hiện sai lệch và gửi cảnh báo Slack tới Tech Lead sau 2 phút, đồng thời kích hoạt Self-Heal hoàn nguyên lại cấu hình chuẩn trong Git sau khi sự cố lắng xuống, ngăn chặn tình trạng cấu hình chắp vá âm thầm tích tụ trên production.
