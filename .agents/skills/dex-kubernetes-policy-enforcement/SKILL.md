---
name: dex-kubernetes-policy-enforcement
description: Author, validate, and enforce cluster governance policies using admission controllers (OPA Gatekeeper, Kyverno) to prevent privilege escalations and unconstrained resource usage. Use when securing multi-tenant Kubernetes clusters.
---

# dex-kubernetes-policy-enforcement

## 1. Purpose & Scope
Thiết kế, kiểm thử và cưỡng chế các chính sách quản trị cụm Kubernetes (Cluster Governance Policies) thông qua Admission Controllers (Kyverno, OPA Gatekeeper); ngăn chặn việc chạy container dưới quyền root, chặn gắn cờ privileged, bắt buộc khai báo resource limits/requests, và bảo đảm an toàn cho các cụm máy chủ đa người dùng (Multi-tenant Clusters).

## 2. When to Use
- Cần tuân thủ các tiêu chuẩn bảo mật container (CIS Kubernetes Benchmark, NSA/CISA Hardening Guide).
- Ngăn chặn các lập trình viên quên khai báo giới hạn RAM/CPU làm ảnh hưởng đến các pod khác (Noisy Neighbors).
- Chặn việc pull image từ các public registry không tin cậy (chỉ cho phép pull từ private ECR/Artifact Registry).

## 3. When NOT to Use
- Không áp dụng chính sách ở chế độ `Enforce` (chặn đứng) ngay lập tức khi chưa qua giai đoạn `Audit` (chỉ cảnh báo) để tránh làm gián đoạn các dịch vụ đang chạy.
- Không dùng để thay thế Network Policies hoặc IAM Roles.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Tiêu chuẩn bảo mật cần cưỡng chế (Pod Security Standards: Baseline, Restricted).
- Công cụ Admission Controller (Kyverno hoặc OPA Gatekeeper).
- Danh sách các namespaces được miễn trừ (ví dụ `kube-system`).
- **Điều kiện tiên quyết**:
- Cụm Kubernetes đã cài đặt Kyverno hoặc OPA Gatekeeper controller.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Validating Webhooks: Chặn đứng các tài nguyên không hợp lệ ngay tại cổng API Server trước khi ghi vào etcd.
- Mutating Webhooks: Tự động sửa đổi hoặc chèn thêm các trường mặc định (ví dụ: tự động chèn securityContext non-root nếu người dùng quên khai báo).
- Pod Security Standards (PSS): Ba cấp độ bảo mật chuẩn của Kubernetes: Privileged, Baseline, Restricted.
- **Quy tắc quyết định kỹ thuật**:
- Ban đầu triển khai policy ở chế độ `validationFailureAction: Audit` trong 7 ngày để thu thập danh sách vi phạm.
- Chuyển sang chế độ `Enforce` sau khi toàn bộ mã nguồn manifest đã được cập nhật tuân thủ.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Viết webhook chặn nhầm các Pods của hệ thống giám sát hoặc mạng (`kube-proxy`, `calico`), khiến cụm cluster bị tê liệt.

## 6. Step-by-Step Execution Workflow
1. Lập danh sách các quy tắc bắt buộc: cấm root, cấm hostNetwork, yêu cầu readOnlyRootFilesystem, giới hạn CPU/RAM.
2. Viết Kyverno ClusterPolicy hoặc Gatekeeper ConstraintTemplates.
3. Kiểm thử chính sách trên tệp manifests bằng Kyverno CLI cục bộ.
4. Triển khai chính sách lên cụm ở chế độ Audit.
5. Xem xét các báo cáo vi phạm và chuyển sang Enforce.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```yaml
# Kyverno Policy: Bắt buộc chạy container dưới non-root user
apiVersion: kyverno.io/v1
kind: ClusterPolicy
metadata:
  name: require-run-as-non-root
spec:
  validationFailureAction: Enforce
  background: true
  rules:
    - name: check-runAsNonRoot
      match:
        any:
        - resources:
            kinds: [Pod]
      exclude:
        any:
        - resources:
            namespaces: [kube-system]
      validate:
        message: "Container bắt buộc phải chạy dưới user non-root!"
        pattern:
          spec:
            securityContext:
              runAsNonRoot: true
```

### Lệnh xác minh & thực thi:
```bash
# Kiểm tra chính sách cục bộ trước khi apply bằng Kyverno CLI
kyverno test ./policies/
```

## 8. Anti-Patterns & Common Traps
- Cho phép pod mount thư mục nhạy cảm của host (`/var/run/docker.sock`, `/etc`).
- Không loại trừ namespace hệ thống (`kube-system`) khỏi các chính sách ngặt nghèo.

## 9. Quality Gates & Acceptance Criteria
- 0 pod nào trong namespace ứng dụng vi phạm tiêu chuẩn Pod Security Standard Restricted.
- 100% manifest deployment đều có khai báo `resources.limits` và `resources.requests`.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Webhook của admission controller phải có cơ chế `failurePolicy: Ignore` hoặc timeout an toàn để tránh khóa toàn bộ API server khi controller bị lag.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ thống hỗ trợ**: Cloud Runtimes (AWS Lambda, Cloudflare Workers, Kubernetes), Linux, Windows 11.

## 12. Deliverables & Output Artifacts
- Tập hợp các file YAML chính sách Kyverno / Gatekeeper.
- Báo cáo kiểm toán vi phạm chính sách trên cụm (Policy Report).

## 13. Related & Complementary Skills
dex-container-image-engineering, dex-gitops-workflows, dex-cloud-iam-policy-review

## 14. Realistic Usage Example
### Tình huống thực tế:
Một công ty công nghệ bị một tài khoản dev bị lộ token và kẻ tấn công cố tình deploy một pod đào tiền ảo chạy dưới quyền root kèm mount ổ đĩa host. Nhờ Kyverno Policy chặn đứng ngay lập tức tại API Server với thông báo 'Containers must not run as root', cuộc tấn công đã bị vô hiệu hóa hoàn toàn trước khi pod kịp khởi động.
