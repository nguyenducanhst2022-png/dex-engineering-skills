---
name: dex-secretless-cicd-oidc
description: Eliminate static long-lived cloud credentials in CI/CD pipelines by implementing OpenID Connect (OIDC) federated identity with AWS, GCP, Azure, and Vault. Use when securing automated deployment pipelines against credential leakage.
---

# dex-secretless-cicd-oidc

## 1. Purpose & Scope
Triệt tiêu hoàn toàn các thông tin xác thực tĩnh có thời hạn dài (Static Long-Lived Credentials) trong pipeline CI/CD; triển khai liên kết định danh OpenID Connect (OIDC Workload Identity Federation) với AWS, Google Cloud, Azure và HashiCorp Vault; bảo đảm các runner chỉ nhận token ngắn hạn và có phạm vi quyền tối thiểu.

## 2. When to Use
- Khi kiểm toán an ninh phát hiện các khóa bí mật nguy hiểm (AWS Secret Access Key, GCP Service Account Key JSON) được lưu trong GitHub Secrets.
- Khi muốn loại bỏ nguy cơ lộ lọt credential khiến toàn bộ tài nguyên đám mây bị tin tặc chiếm quyền điều khiển.
- Khi thiết lập quy trình triển khai tự động từ GitHub Actions, GitLab CI tới AWS/GCP/Azure.

## 3. When NOT to Use
- Khi hệ thống CI/CD hoàn toàn cô lập trong mạng nội bộ (On-Premises Air-Gapped) không kết nối với bất kỳ dịch vụ định danh công cộng nào.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Nhà cung cấp CI/CD (GitHub Actions, GitLab CI), tài khoản Cloud IAM (AWS IAM, GCP IAM, Azure AD), chính sách phân quyền IAM.
- **Quyền hạn truy cập:** Quyền tạo OIDC Identity Provider và gán IAM Role trên nền tảng đám mây.

## 5. Core Concepts & Taxonomy
- **OIDC Workload Identity Federation:** Runner CI yêu cầu một token JWT có chữ ký mật mã từ nhà cung cấp CI; Cloud IAM xác thực token này qua endpoint công khai (`.well-known/openid-configuration`) và cấp phát token phiên tạm thời ngắn hạn (thường là 15-60 phút).
- **Subject Claims (sub) Binding:** Khóa chặt quyền truy cập vào đúng commit, branch hoặc environment cụ thể (ví dụ: chỉ branch `main` của repository `my-org/my-repo` mới được giả lập IAM Role sản xuất).
- **Zero Static Secrets:** Không có bất kỳ access key hoặc mật khẩu nào được lưu trữ cố định trong cài đặt repository.

## 6. Step-by-Step Execution Workflow
1. Khởi tạo OIDC Identity Provider trên Cloud IAM trỏ tới máy chủ phát hành token của CI (ví dụ: `https://token.actions.githubusercontent.com`).
2. Thiết lập Trust Policy trên IAM Role xác định rõ điều kiện `aud` (Audience) và `sub` (Subject Claim) của repository.
3. Gán các chính sách phân quyền tối thiểu (Least Privilege Policies) cho IAM Role.
4. Cấu hình quyền `id-token: write` trong file workflow CI (`.github/workflows/deploy.yml`).
5. Sử dụng action chính thức (như `aws-actions/configure-aws-credentials`) để hoán đổi token OIDC lấy STS Temporary Credentials.
6. Xóa bỏ vĩnh viễn toàn bộ các static secret keys cũ khỏi hệ thống quản lý secrets.

## 7. Concrete Examples
### Cấu hình GitHub Actions xác thực OIDC với AWS không cần static keys:
```yaml
name: Deploy to Production
on:
  push:
    branches: [main]

permissions:
  id-token: write # Bat buoc de xin token OIDC tu GitHub
  contents: read

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Configure AWS Credentials via OIDC
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789012:role/GitHubDeployRole
          aws-region: ap-southeast-1
          audience: sts.amazonaws.com

      - name: Verify STS Identity
        run: |
          aws sts get-caller-identity
          echo "Xac thuc OIDC thanh cong! Token co thoi han 15 phut."
```

## 8. Anti-Patterns & Common Traps
- **Wildcard Subject Condition:** Đặt điều kiện `"StringLike": { "token.actions.githubusercontent.com:sub": "*" }` cho phép bất kỳ ai trên GitHub cũng có thể giả lập IAM Role của bạn.
- **Storing JSON Service Account Keys:** Tải file khóa JSON của GCP về và paste vào Secret Variable thay vì dùng Workload Identity Federation.
- **Extended Token Duration:** Cấu hình thời hạn token phiên quá dài (hơn 1 giờ) cho các tác vụ CI chỉ chạy trong 2 phút.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: 0% static cloud access keys (AWS/GCP/Azure) tồn tại trong GitHub Actions Secrets.
- **QG-04**: IAM Trust Policy ràng buộc chính xác repository name và branch mục tiêu (`refs/heads/main`).
- **QG-09**: Thời hạn hiệu lực của token tạm thời không vượt quá 60 phút.

## 10. Security & Safety Boundaries
- Chặn đứng nguy cơ rò rỉ credential vĩnh viễn khi có sự cố lộ lọt biến môi trường hoặc script độc hại trong pull request.

## 11. Platform Adapters
- **Cloud IAM**: AWS IAM (STS AssumeRoleWithWebIdentity), GCP Workload Identity Federation, Azure AD Federated Credentials.
- **CI Platforms**: GitHub Actions, GitLab CI, CircleCI.

## 12. Deliverables & Output Artifacts
- File khai báo Terraform / CloudFormation tạo OIDC Provider và IAM Role.
- Workflow GitHub Actions triển khai hoàn toàn không chứa secret.
- Báo cáo kiểm toán loại bỏ 100% static credentials cũ.

## 13. Related & Complementary Skills
dex-ephemeral-test-credentials, dex-service-account-lifecycle, dex-container-runtime-isolation

## 14. Realistic Usage Example
```powershell
# Kiểm tra sự tồn tại của static secrets trong repository bằng GitHub CLI
gh secret list

# Kiểm tra cấu hình IAM Role Trust Policy trên AWS CLI
aws iam get-role --role-name GitHubDeployRole --query "Role.AssumeRolePolicyDocument"
```
