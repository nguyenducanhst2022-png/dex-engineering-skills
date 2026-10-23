---
name: dex-terraform-module-contract-tests
description: Design, implement, and automate contract tests for reusable Terraform and OpenTofu modules. Validate variable schemas, output guarantees, state drift, and prevent breaking changes.
---

# dex-terraform-module-contract-tests

## 1. Purpose & Scope
Thiết kế, xây dựng và tự động hóa các bộ kiểm thử hợp đồng giao diện (Contract Testing) cho các mô-đun hạ tầng tái sử dụng viết bằng Terraform hoặc OpenTofu; kiểm chứng tính toàn vẹn của lược đồ biến đầu vào (Input Variable Schemas & Validation Rules), cam kết chất lượng đầu ra (Output Guarantees); sử dụng framework kiểm thử gốc `terraform test` hoặc Terratest để phát hiện sớm các thay đổi phá vỡ tương thích (Breaking Changes) trước khi xuất bản mô-đun lên Private Registry.

## 2. When to Use
- Khi phát triển và duy trì các mô-đun hạ tầng cốt lõi dùng chung cho toàn bộ tổ chức (như VPC Module, EKS Module, S3 Bucket Module).
- Khi nâng cấp phiên bản mô-đun (ví dụ từ v1.x lên v2.x) và cần chứng minh các dự án đang sử dụng không bị phá vỡ cấu trúc hạ tầng.
- Khi tích hợp kiểm thử tự động Infrastructure as Code (IaC) vào quy trình CI/CD Pull Request.

## 3. When NOT to Use
- Khi viết các tệp cấu hình Terraform cục bộ dùng một lần cho một môi trường duy nhất mà không có ý định tái sử dụng thành module.
- Khi kiểm thử logic ứng dụng nghiệp vụ không liên quan đến tầng cấp phát tài nguyên đám mây.

## 4. Prerequisites & Input Context
- **Công cụ IaC:** Terraform 1.6+ hoặc OpenTofu 1.6+ hỗ trợ lệnh `test`.
- **Môi trường giả lập:** AWS LocalStack hoặc tài khoản Sandbox hạn chế quyền để chạy kiểm thử thực tế.

## 5. Core Concepts & Taxonomy
- **Terraform Native Testing Framework (`.tftest.hcl`):** Khung kiểm thử chính thức được tích hợp sẵn từ phiên bản Terraform 1.6, cho phép viết các bài test kiểm tra điều kiện `assert` sau các giai đoạn `command = plan` hoặc `command = apply`.
- **Input Contract Validation:** Khối `validation` bên trong định nghĩa `variable` nhằm chặn đứng các giá trị đầu vào sai quy chuẩn ngay từ trước khi chạy plan.
- **Module Interface Stability:** Quy tắc bảo đảm không xóa bỏ hoặc đổi tên các biến `output` quan trọng mà các hệ thống khác đang phụ thuộc.

## 6. Step-by-Step Execution Workflow
1. Khai báo các quy tắc kiểm tra ràng buộc chặt chẽ trong khối `variable` của module.
2. Tạo thư mục `tests/` chứa các kịch bản kiểm thử hợp đồng dạng tệp `.tftest.hcl`.
3. Định nghĩa các kịch bản kiểm thử tĩnh (Run Plan Only) để xác thực các giá trị mặc định và logic tính toán nội bộ mà không tốn chi phí tạo tài nguyên.
4. Định nghĩa các kịch bản kiểm thử động (Run Apply) trên môi trường Sandbox để xác nhận tài nguyên được tạo đúng thuộc tính.
5. Chạy lệnh `terraform test` hoặc `tofu test` trong pipeline CI.
6. Xuất báo cáo kết quả kiểm thử và gắn thẻ phiên bản Semantic Versioning nếu bài test đạt 100%.

## 7. Concrete Examples
### Kich ban kiem thu hop dong module S3 Bucket bang terraform test (.tftest.hcl):
```hcl
# tests/contract_validation.tftest.hcl

variables {
  bucket_name = "corp-secure-data-bucket-test"
  environment = "staging"
  enable_kms  = true
}

# Kiem thu Plan: Khang dinh bat buoc bat ma hoa KMS va khoa truy cap Public
run "verify_security_defaults_plan" {
  command = plan

  assert {
    condition     = aws_s3_bucket_server_side_encryption_configuration.this.rule[0].apply_server_side_encryption_by_default[0].sse_algorithm == "aws:kms"
    error_message = "S3 bucket must enforce AWS KMS encryption by default."
  }

  assert {
    condition     = aws_s3_bucket_public_access_block.this.block_public_acls == true
    error_message = "Block Public ACLs must be set to true."
  }

  assert {
    condition     = output.bucket_arn != ""
    error_message = "Output bucket_arn must not be empty."
  }
}

# Kiem thu loi khi truyen ten bucket vi pham quy tac dat ten
run "expect_invalid_bucket_name_failure" {
  command = plan

  variables {
    bucket_name = "INVALID_UPPERCASE_NAME"
  }

  expect_failures = [
    var.bucket_name,
  ]
}
```

## 8. Anti-Patterns & Common Traps
- **Unbounded Input Types:** Khai báo kiểu biến là `type = any` mà không có khối validation dẫn đến việc người dùng truyền nhầm cấu trúc dữ liệu gây sập runtime.
- **Hardcoding Resource Names:** Gán nhãn cứng tên tài nguyên bên trong mô-đun khiến người dùng không thể tạo 2 phiên bản của mô-đun trên cùng một tài khoản đám mây.
- **Skipping Destroy in Integration Tests:** Chạy `terraform apply` trong bài test nhưng quên tự động gọi `destroy` khi test xong, để lại tài nguyên rác tốn tiền trên cloud.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: 100% các biến đầu vào đều có mô tả (`description`), kiểu dữ liệu rõ ràng và quy tắc validation phù hợp.
- **QG-02**: Tất cả các tệp `.tftest.hcl` vượt qua với kết quả PASS trong lệnh `terraform test`.
- **QG-03**: Không có bất kỳ thay đổi nào làm gãy các biến `output` đã công bố trong phiên bản Minor/Patch.

## 10. Security & Safety Boundaries
- Bắt buộc kiểm tra các tiêu chuẩn an ninh hạ tầng (mã hóa at-rest, khóa public access, bật logging) ngay trong các bài test hợp đồng.

## 11. Platform Adapters
- **Runtimes**: Terraform CLI 1.6+, OpenTofu 1.6+, Terratest (Go), LocalStack.

## 12. Deliverables & Output Artifacts
- Bộ tệp kiểm thử hợp đồng mô-đun (`tests/*.tftest.hcl`).
- Báo cáo kết quả kiểm định hợp đồng tự động tích hợp CI/CD.

## 13. Related & Complementary Skills
dex-infrastructure-policy-as-code, dex-platform-selfservice-templates, dex-cloud-database-failover-drills

## 14. Realistic Usage Example
```bash
# Chay toan bo bo test hop dong Terraform
terraform init
terraform test -verbose
```
