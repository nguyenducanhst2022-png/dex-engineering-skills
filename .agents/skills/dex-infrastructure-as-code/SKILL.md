---
name: dex-infrastructure-as-code
description: Manage cloud and system resources declaratively using Terraform, OpenTofu, or Pulumi with remote state locking, modular design, drift detection, checkov security scanning, and strict plan validation. Use when provisioning, updating, or auditing cloud infrastructure.
---

# dex-infrastructure-as-code

## 1. Purpose & Scope
Quản trị cơ sở hạ tầng dưới dạng mã nguồn (Infrastructure as Code - IaC) bằng Terraform hoặc OpenTofu; thiết lập kiến trúc module hóa tái sử dụng, lưu trữ remote state an toàn kèm cơ chế lock (S3 + DynamoDB / GCS / Terraform Cloud), kiểm tra sai lệch cấu hình (Drift Detection), quét tuân thủ an ninh bằng Checkov / tfsec và thực thi quy trình phê duyệt nghiêm ngặt qua `plan` và `apply`.

## 2. When to Use
- Khi khởi tạo tài nguyên đám mây mới (VPC, Subnet, Database, K8s cluster, IAM Roles).
- Khi cần đồng bộ cấu hình giữa các môi trường (Dev, Staging, Production) một cách nhất quán.
- Khi phát hiện hạ tầng bị thay đổi thủ công qua console (ClickOps) gây ra sai lệch cấu hình (Configuration Drift).

## 3. When NOT to Use
- Quản lý mã nguồn cấu hình phần mềm nội bộ bên trong máy chủ (dùng Ansible hoặc Cloud-init).
- Triển khai ứng dụng container lên K8s (dùng `dex-kubernetes-deployment`).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Đặc tả kiến trúc tài nguyên đám mây (Cloud provider: AWS, GCP, Azure).
- Môi trường mục tiêu và ranh giới mạng (CIDR blocks, Security Groups).
- Khóa mã hóa KMS và chính sách tag bắt buộc.
- **Điều kiện tiên quyết**:
- Terraform phiên bản 1.6+ hoặc OpenTofu 1.7+ được cài đặt.
- Remote Backend (S3 Bucket với Versioning & Encryption + DynamoDB Lock table) đã sẵn sàng.
- Quyền Cloud IAM thực thi được giới hạn theo nguyên tắc đặc quyền tối thiểu (Least Privilege).

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- **Declarative State Immutability**: Tệp state (`.tfstate`) là nguồn chân lý duy nhất phản ánh thực tế hạ tầng; mọi can thiệp đều phải qua code IaC.
- **Remote State Locking**: Khóa state trong suốt quá trình `plan` và `apply` để ngăn chặn xung đột ghi đè song song giữa các kỹ sư.
- **Modular Abstraction Hierarchy**: Tách hạ tầng thành các module độc lập theo vòng đời: Core Network (VPC), Shared Data (RDS/Kafka), Application Compute (EKS/ECS).
- **Quy tắc quyết định kỹ thuật**:
- **Cấm Áp Dụng Lệnh `apply -auto-approve` trên Production**: Mọi thay đổi production bắt buộc phải tạo artifact plan file và có ít nhất 2 kỹ sư review.
- **Bắt Buộc Mã Hóa State**: Tệp state chứa metadata nhạy cảm phải được mã hóa at-rest (KMS AES-256) và truyền qua TLS.
- **Không Lưu Secret Trực Tiếp Trong Code**: Biến nhạy cảm phải lấy qua AWS Secrets Manager / Vault hoặc biến môi trường `TF_VAR_*` được inject lúc runtime.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Xóa nhầm Database do đổi tên định danh trong code**: Terraform destroy và recreate RDS instance -> Khắc phục: Bắt buộc cấu hình lifecycle block `prevent_destroy = true` cho mọi tài nguyên dữ liệu quan trọng.
- **Xung đột State do 2 pipeline chạy cùng lúc**: Thiếu DynamoDB Lock -> Khắc phục: Khai báo `dynamodb_table` trong S3 backend block.

## 6. Step-by-Step Execution Workflow
1. Khởi tạo cấu trúc dự án: `modules/` (reusable logic) và `environments/{dev,staging,prod}/` (variables, backend).
2. Định nghĩa remote backend với S3 bucket versioning và DynamoDB state locking.
3. Viết code tài nguyên với định dạng chuẩn (`terraform fmt -check`) và kiểm tra cú pháp (`terraform validate`).
4. Quét chính sách an ninh và tuân thủ bằng Checkov: `checkov -d . --framework terraform`.
5. Tạo bản kế hoạch thay đổi: `terraform plan -out=tfplan.binary`.
6. Phân tích `tfplan` để rà soát các hành động `destroy` hoặc `modify` không lường trước.
7. Áp dụng thay đổi từ plan đã duyệt: `terraform apply tfplan.binary`.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```hcl
# environments/prod/backend.tf
terraform {
  required_version = ">= 1.6.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.40"
    }
  }
  backend "s3" {
    bucket         = "mycorp-terraform-state-prod"
    key            = "networking/vpc.tfstate"
    region         = "ap-southeast-1"
    dynamodb_table = "terraform-lock-table"
    encrypt        = true
  }
}

# modules/database/main.tf
resource "aws_db_instance" "main" {
  identifier           = "prod-core-db"
  allocated_storage    = 100
  engine               = "postgres"
  engine_version       = "16.1"
  instance_class       = "db.r6g.xlarge"
  storage_encrypted    = true
  deletion_protection  = true

  lifecycle {
    prevent_destroy = true
  }
}
```

### Lệnh xác minh & thực thi:
- Định dạng và kiểm tra cú pháp: `terraform fmt -check && terraform validate`
- Quét lỗ hổng an ninh: `checkov -d . --compact`
- Lập kế hoạch thay đổi: `terraform plan -out=tfplan`
- Kiểm tra sai lệch hạ tầng (Drift): `terraform plan -detailed-exitcode` (mã 2 là có drift)

## 8. Anti-Patterns & Common Traps
- **Lưu `.tfstate` trên Git**: Rò rỉ toàn bộ password, connection strings và token hạ tầng.
- **Tạo Monolithic State File**: Đặt toàn bộ hệ thống từ VPC, K8s tới 50 database trong 1 file `main.tf` duy nhất (apply mất 2 tiếng và rủi ro cực cao).
- **Hardcode CIDR hoặc Credentials trong code**: Gây khó khăn khi scale và vi phạm bảo mật.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Mã nguồn IaC vượt qua `terraform validate` và `checkov` không có vi phạm CRITICAL.
- QG-07: Remote state được khóa và mã hóa hoàn toàn.
- QG-12: Mọi tài nguyên quan trọng đều gắn cờ `prevent_destroy = true`.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi deploy.

## 10. Security & Safety Boundaries
- Không bao giờ commit tệp `terraform.tfstate` hoặc `.tfvars` chứa secret lên Git.
- Áp dụng quyền tối thiểu (Least Privilege IAM) cho Terraform CI Service Account.
- Không bao giờ lưu trữ hardcoded secret hoặc cấp quyền quá mức (over-permissioned IAM).

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Môi trường Cloud & Container**: Hỗ trợ Docker, Kubernetes (EKS/GKE/AKS), Terraform/OpenTofu, OpenTelemetry.

## 12. Deliverables & Output Artifacts
- Module IaC chuẩn hóa, có thể tái sử dụng.
- File kế hoạch `tfplan` đã được kiểm duyệt.
- Báo cáo phân tích an ninh Checkov.

## 13. Related & Complementary Skills
- `dex-cloud-service-integration`: Tích hợp các dịch vụ cloud được tạo ra.
- `dex-configuration-drift`: Phát hiện và xử lý sai lệch cấu hình hạ tầng.
- `dex-secrets-management`: Quản lý an toàn các tham số nhạy cảm trong IaC.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư DevOps cần triển khai cụm Amazon RDS PostgreSQL đa vùng cho hệ thống mới. Sử dụng `dex-infrastructure-as-code`, kỹ sư tổ chức module tái sử dụng, bật cờ `deletion_protection = true` và `prevent_destroy = true`, cấu hình remote backend với DynamoDB lock, chạy Checkov xác nhận mã hóa KMS đầy đủ, xuất `tfplan` cho Tech Lead phê duyệt trước khi apply an toàn.
