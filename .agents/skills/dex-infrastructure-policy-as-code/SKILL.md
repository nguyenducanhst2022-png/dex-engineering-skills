---
name: dex-infrastructure-policy-as-code
description: Define, enforce, and audit Infrastructure Policy as Code (PaC) using Open Policy Agent (OPA/Rego) and Kyverno. Enforce security guardrails, validate exceptions, and block non-compliant resources.
---

# dex-infrastructure-policy-as-code

## 1. Purpose & Scope
Thiết kế, định nghĩa và thực thi chính sách quản trị hạ tầng dưới dạng mã nguồn (Policy as Code - PaC); sử dụng Open Policy Agent (OPA/Rego), Conftest, Trivy hoặc Kyverno để áp đặt các rào chắn bảo mật (Guardrails) trên các tệp cấu hình Terraform, Kubernetes Manifests và Dockerfile; tự động phát hiện và chặn đứng các vi phạm an ninh (như mở cổng 22 ra internet, thiếu thẻ gắn chi phí FinOps, hoặc chạy container dưới quyền root) trước khi hạ tầng được cấp phát.

## 2. When to Use
- Khi thiết lập cổng kiểm soát chất lượng an ninh tự động trong pipeline CI/CD cho toàn bộ các nhóm kỹ thuật.
- Khi ngăn chặn nguy cơ nhân sự cấu hình sai dẫn đến lộ lọt dữ liệu hoặc vi phạm các tiêu chuẩn tuân thủ (PCI-DSS, SOC 2, ISO 27001).
- Khi cần cơ chế quản lý ngoại lệ chính sách (Policy Exceptions) có thời hạn và có kiểm toán minh bạch.

## 3. When NOT to Use
- Khi kiểm tra logic mã nguồn của ứng dụng phần mềm (sử dụng SonarQube hoặc SAST tools).
- Khi quy mô hạ tầng quá nhỏ (1-2 máy chủ cá nhân) không đòi hỏi hệ thống kiểm soát tuân thủ tự động.

## 4. Prerequisites & Input Context
- **Công cụ chính sách:** OPA CLI (`opa`), Conftest, hoặc Kyverno CLI.
- **Tệp đầu vào:** Kế hoạch thực thi hạ tầng định dạng JSON (`terraform show -json tfplan.binary > tfplan.json`) hoặc Kubernetes YAML.

## 5. Core Concepts & Taxonomy
- **Open Policy Agent (OPA) & Rego:** Động cơ đánh giá chính sách nguồn mở cho phép viết các luật kiểm tra bằng ngôn ngữ khai báo Rego đối chiếu với bất kỳ cấu trúc dữ liệu JSON nào.
- **Admission Controller Enforcer:** Thành phần trong Kubernetes (như OPA Gatekeeper hoặc Kyverno) chặn đứng các yêu cầu tạo tài nguyên vi phạm chính sách ngay tại API Server.
- **Shift-Left Security:** Đẩy các bài kiểm tra bảo mật về phía bên trái của quy trình phát triển (ngay trên máy kỹ sư và tại bước tạo Pull Request).

## 6. Step-by-Step Execution Workflow
1. Xây dựng bộ quy tắc an ninh dưới dạng tệp `.rego` trong thư mục `policies/`.
2. Biên dịch kế hoạch triển khai hạ tầng thành định dạng JSON: `terraform show -json plan.tfplan > plan.json`.
3. Thực thi kiểm tra đối soát bằng Conftest: `conftest test plan.json -p policies/`.
4. Đánh giá kết quả: Phân loại mức độ vi phạm thành WARN (cảnh báo) và DENY (chặn đứng tiến trình build).
5. Thiết lập quy trình xử lý ngoại lệ: Ghi nhận mã ngoại lệ được phê duyệt có chữ ký số vào tệp `exceptions.json`.
6. Xuất báo cáo kiểm toán tuân thủ chính sách cho đội ngũ Security Operation Center (SOC).

## 7. Concrete Examples
### Chinh sach OPA Rego ngan chan Security Group mo cong SSH (22) ra toan the gioi (0.0.0.0/0):
```rego
package terraform.security

import future.keywords.in

default allow = true

# Phat hien cac quy tac ingress mo cong 22 ra Internet
deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_security_group_rule"
    resource.change.after.type == "ingress"
    
    # Kiem tra cong 22
    from_port := resource.change.after.from_port
    to_port := resource.change.after.to_port
    22 >= from_port
    22 <= to_port

    # Kiem tra dai CIDR mo 0.0.0.0/0
    cidr_blocks := resource.change.after.cidr_blocks[_]
    cidr_blocks == "0.0.0.0/0"

    msg := sprintf("SECURITY VIOLATION: Resource '%v' opens SSH port 22 directly to the public Internet (0.0.0.0/0)!", [resource.address])
}
```

## 8. Anti-Patterns & Common Traps
- **Hardcoded Exceptions in Rule Body:** Viết thẳng tên tài nguyên ngoại lệ vào bên trong file luật Rego khiến mã chính sách bị ô nhiễm và khó bảo trì.
- **Only Auditing Post-Deployment:** Chỉ kiểm tra vi phạm sau khi tài nguyên đã được tạo trên đám mây thay vì chặn ngay từ giai đoạn Plan trong CI/CD.
- **Vague Denial Messages:** Xuất thông báo lỗi chung chung "Policy Failed" mà không chỉ rõ tài nguyên nào vi phạm và cách sửa đổi cụ thể.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: 100% các tệp hạ tầng IaC được quét tự động qua bộ chính sách PaC trước khi thực thi apply.
- **QG-02**: Không có bất kỳ vi phạm mức DENY nào được phép vượt qua pipeline CI/CD nếu không có ngoại lệ phê duyệt hợp lệ.
- **QG-03**: Mọi quy tắc chính sách đều có bộ kiểm thử đơn vị đi kèm (`*_test.rego`) đạt tỷ lệ bao phủ 100%.

## 10. Security & Safety Boundaries
- Bảo vệ tính toàn vẹn của kho chứa chính sách; chỉ những nhân sự thuộc nhóm Bảo mật mới có quyền phê duyệt thay đổi các tệp `.rego`.

## 11. Platform Adapters
- **Runtimes**: OPA (Rego), Conftest, Kyverno CLI, Trivy, Checkov, OPA Gatekeeper.

## 12. Deliverables & Output Artifacts
- Kho thư viện chính sách bảo mật hạ tầng (`policies/terraform/*.rego`).
- Báo cáo kết quả kiểm tra tuân thủ chính sách (`pac_compliance_report.json`).

## 13. Related & Complementary Skills
dex-terraform-module-contract-tests, dex-kubernetes-secret-delivery, dex-platform-selfservice-templates

## 14. Realistic Usage Example
```bash
# Kiem tra ke hoach Terraform bang Conftest va OPA policies
conftest test tfplan.json --policy ./policies --all-namespaces
```
