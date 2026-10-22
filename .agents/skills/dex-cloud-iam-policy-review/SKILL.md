---
name: dex-cloud-iam-policy-review
description: Audit, sanitize, and enforce Least-Privilege IAM policies, role boundaries, and access conditions across AWS, GCP, and Azure. Use to eliminate privilege escalation paths and over-permissioned service accounts.
---

# dex-cloud-iam-policy-review

## 1. Purpose & Scope
Kiểm toán, rà soát và cưỡng chế nguyên tắc đặc quyền tối thiểu (Least Privilege) cho chính sách IAM (Identity & Access Management) trên AWS, GCP, Azure; phát hiện và loại bỏ các quyền nguy hiểm (`*`), các đường dẫn leo thang đặc quyền (Privilege Escalation), và bảo vệ các Service Accounts trong hệ thống Cloud.

## 2. When to Use
- Chuẩn bị cho kỳ đánh giá kiểm toán an ninh thông tin (SOC2, ISO 27001, PCI-DSS).
- Phát hiện các IAM Roles được cấp quyền Admin (`AdministratorAccess` hoặc `*.*`) vô tội vạ.
- Sau khi một nhân sự kỹ thuật rời khỏi dự án hoặc thay đổi nhà thầu phát triển.

## 3. When NOT to Use
- Không tự tiện thu hồi hàng loạt quyền trên production khi chưa phân tích CloudTrail/Access Analyzer để biết quyền đó có đang được ứng dụng sử dụng hay không.
- Không dùng để quản lý phân quyền trong ứng dụng người dùng cuối (dùng RBAC/ABAC nội bộ).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- File chính sách IAM (JSON/Terraform IAM definitions).
- Nhật ký sử dụng quyền thực tế (AWS CloudTrail, IAM Access Advisor, GCP Policy Analyzer).
- Danh sách các tài nguyên nhạy cảm (S3 buckets, KMS keys, Secret Manager).
- **Điều kiện tiên quyết**:
- Có quyền truy cập chỉ đọc vào IAM và các công cụ phân tích truy cập trên Cloud Console.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Least Privilege: Chỉ cấp đúng các action (như `s3:GetObject`) trên đúng ARN tài nguyên cụ thể (chứ không phải `s3:*` trên `*`).
- Permission Boundaries: Ranh giới tối đa mà một Role có thể cấp cho các Role khác, ngăn chặn việc dev tự tạo role mới để leo thang lên Admin.
- Unused Access Removal: Thu hồi các quyền không được sử dụng trong vòng 90 ngày qua.
- **Quy tắc quyết định kỹ thuật**:
- Bất kỳ policy nào chứa `Action: "*"` hoặc `Resource: "*"` phải bị gắn cờ nghiêm trọng (Critical Finding).
- Mọi IAM Role dùng cho ứng dụng bắt buộc phải có điều kiện `Condition` ràng buộc theo VPC, IP nội bộ hoặc tag hợp lệ.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Xóa nhầm quyền `kms:Decrypt` của một service đang chạy khiến dịch vụ không thể giải mã cơ sở dữ liệu và bị ngưng trệ.

## 6. Step-by-Step Execution Workflow
1. Quét toàn bộ IAM policies bằng công cụ tự động (Policy Sentry, Prowler, Checkov).
2. Xuất báo cáo Access Advisor để xác định các action không được gọi trong 90 ngày qua.
3. Viết lại chính sách IAM thu hẹp phạm vi vào các ARN cụ thể.
4. Áp dụng Permission Boundary để khóa chặt quyền tự cấp phép.
5. Kiểm tra lại bằng AWS IAM Policy Simulator trước khi apply chính thức.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```json
// Chính sách IAM chuẩn Least-Privilege cho microservice đơn hàng
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowSpecificS3BucketReadWrite",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:PutObject"
      ],
      "Resource": "arn:aws:s3:::company-order-invoices-prod/*"
    },
    {
      "Sid": "DenyUnencryptedTraffic",
      "Effect": "Deny",
      "Action": "s3:*",
      "Resource": "arn:aws:s3:::company-order-invoices-prod/*",
      "Condition": {
        "Bool": { "aws:SecureTransport": "false" }
      }
    }
  ]
}
```

### Lệnh xác minh & thực thi:
```bash
# Phân tích cú pháp và tìm lỗi wildcard trong IAM Policy bằng Parliament
parliament --file policies/app-iam-policy.json
```

## 8. Anti-Patterns & Common Traps
- Đính kèm policy `AdministratorAccess` cho các EC2 Instance hoặc ECS Tasks để 'chạy cho tiện'.
- Chia sẻ chung một IAM Role cho nhiều microservices khác nhau.

## 9. Quality Gates & Acceptance Criteria
- 0 quyền `Action: *` tồn tại trong mã nguồn Terraform triển khai production.
- 100% IAM Roles đều có Resource ARN chỉ định rõ ràng.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Mọi thao tác thay đổi IAM policy phải được thực hiện qua Pull Request có review và lưu audit log.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ thống hỗ trợ**: Cloud Runtimes (AWS Lambda, Cloudflare Workers, Kubernetes), Linux, Windows 11.

## 12. Deliverables & Output Artifacts
- Báo cáo kiểm toán IAM (Audit Report).
- Bộ file Terraform IAM policies đã được tinh chỉnh đạt chuẩn Least-Privilege.

## 13. Related & Complementary Skills
dex-cloud-network-design, dex-kubernetes-policy-enforcement, dex-security-logging-detection

## 14. Realistic Usage Example
### Tình huống thực tế:
Một startup fintech chuẩn bị thẩm định SOC2. Chuyên gia IAM rà soát và phát hiện Lambda xử lý thanh toán có quyền `iam:CreatePolicy` và `s3:*` toàn bộ tài khoản. Bằng cách tái cấu trúc policy về đúng 4 actions trên đúng 1 S3 bucket và 1 DynamoDB table, startup đã vượt qua bài kiểm toán bảo mật xuất sắc.
