---
name: dex-service-account-lifecycle
description: Govern, audit, rotate, and decommission machine identities and service accounts across cloud platforms and Kubernetes clusters. Use when eliminating orphaned credentials and enforcing least privilege for automated agents.
---

# dex-service-account-lifecycle

## 1. Purpose & Scope
Quản trị, kiểm toán, luân chuyển khóa (Rotation) và giải phóng (Decommission) vòng đời của các định danh máy (Machine Identities) và tài khoản dịch vụ (Service Accounts) trên hạ tầng đám mây và Kubernetes; triệt tiêu các tài khoản mồ côi và thực thi nguyên tắc đặc quyền tối thiểu cho các hệ thống tự động.

## 2. When to Use
- Khi kiểm toán phát hiện hàng chục tài khoản dịch vụ (Service Accounts) không rõ ai tạo ra và không rõ đang phục vụ ứng dụng nào.
- Khi cần tự động hóa quy trình luân chuyển khóa mật mã định kỳ 90 ngày một lần theo tiêu chuẩn bảo mật.
- Khi một ứng dụng hoặc microservice bị ngừng hoạt động vĩnh viễn và cần dọn dẹp an toàn toàn bộ các quyền hạn liên quan.

## 3. When NOT to Use
- Khi quản lý tài khoản định danh người dùng cá nhân (Human Users) thuộc thẩm quyền của hệ thống HR/IdP.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Danh sách tài khoản dịch vụ trên AWS IAM, GCP IAM, Azure AD hoặc Kubernetes ServiceAccounts, nhật ký truy cập hoạt động (CloudTrail, Audit Logs).
- **Quyền hạn truy cập:** Quyền quản trị IAM cho phép tạo, sửa đổi và xóa tài khoản dịch vụ.

## 5. Core Concepts & Taxonomy
- **Orphaned Service Account:** Tài khoản máy vẫn tồn tại và giữ quyền hạn cao trong hệ thống dù ứng dụng hoặc dự án liên quan đã bị khai tử từ lâu.
- **Last Used Activity Audit:** Theo dõi thời điểm gần nhất mà tài khoản máy thực sự thực hiện một API call; nếu không có hoạt động trong 60 ngày, tài khoản sẽ tự động bị vô hiệu hóa tạm thời.
- **Dual-Key Rotation Window:** Quy trình luân chuyển khóa an toàn: Tạo khóa mới (Key B) -> Cập nhật ứng dụng dùng Key B -> Kiểm tra hoạt động -> Xóa khóa cũ (Key A) mà không làm gián đoạn dịch vụ.

## 6. Step-by-Step Execution Workflow
1. Quét toàn bộ hệ thống để lập danh mục tập trung tất cả các Machine Identities kèm thông tin chủ sở hữu (Owner Tag).
2. Đối chiếu với nhật ký kiểm toán (CloudTrail / Kubernetes Audit) để xác định các tài khoản không hoạt động trong 60 ngày qua.
3. Gửi thông báo cảnh báo và tự động vô hiệu hóa (Disable) tài khoản không sử dụng trong 14 ngày tiếp theo.
4. Thực hiện xóa vĩnh viễn (Decommission) nếu không có khiếu nại hoặc sự cố phát sinh.
5. Tự động hóa quy trình luân chuyển khóa định kỳ cho các tài khoản đang hoạt động.
6. Rà soát lại các quyền hạn được gán (IAM Permissions) để cắt giảm các quyền thừa thãi không được sử dụng.

## 7. Concrete Examples
### Kịch bản phát hiện và cảnh báo Service Accounts không hoạt động trên AWS bằng Python:
```python
import boto3
from datetime import datetime, timezone, timedelta

iam = boto3.client('iam')

def audit_inactive_service_accounts(days_inactive=60):
    users = iam.list_users()['Users']
    cutoff = datetime.now(timezone.utc) - timedelta(days=days_inactive)
    
    for u in users:
        # Chi kiem tra cac tai khoan may (Service Accounts co prefix 'svc_')
        if not u['UserName'].startswith('svc_'): continue
        
        # Kiem tra ngay su dung access key gan nhat
        keys = iam.list_access_keys(UserName=u['UserName'])['AccessKeyMetadata']
        for k in keys:
            last_used = iam.get_access_key_last_used(AccessKeyId=k['AccessKeyId'])['AccessKeyLastUsed']
            last_date = last_used.get('LastUsedDate')
            
            if not last_date or last_date < cutoff:
                print(f"CANH BAO MO COI: Tai khoan {u['UserName']} (Key: {k['AccessKeyId']}) khong hoat dong hon {days_inactive} ngay!")
```

## 8. Anti-Patterns & Common Traps
- **Infinite Key Lifespans:** Để một Access Key hoạt động suốt 5 năm không bao giờ thay đổi.
- **Generic Admin Service Accounts:** Dùng chung một tài khoản dịch vụ có quyền `AdministratorAccess` cho 20 ứng dụng khác nhau.
- **Deleting Without Grace Period:** Xóa ngay lập tức một tài khoản dịch vụ mà không có giai đoạn vô hiệu hóa thử nghiệm (Disable) dẫn tới sự cố sập hệ thống không thể khôi phục.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: 100% tài khoản dịch vụ đều có thẻ gán chủ sở hữu (`Owner`) và mục đích sử dụng rõ ràng.
- **QG-04**: 0% Access Keys có tuổi thọ vượt quá 90 ngày mà không được luân chuyển.
- **QG-09**: Tất cả các tài khoản không hoạt động quá 60 ngày đều được tự động vô hiệu hóa.

## 10. Security & Safety Boundaries
- Ngăn ngừa nguy cơ kẻ tấn công tái sử dụng các tài khoản dịch vụ cũ bị bỏ quên để duy trì chỗ đứng bí mật trong hệ thống.

## 11. Platform Adapters
- **Cloud IAM**: AWS IAM, GCP Service Accounts, Azure Managed Identities, Kubernetes RBAC.

## 12. Deliverables & Output Artifacts
- Bảng danh mục quản trị vòng đời tài khoản dịch vụ.
- Pipeline tự động luân chuyển khóa không gián đoạn.
- Kịch bản dọn dẹp các tài khoản mồ côi định kỳ.

## 13. Related & Complementary Skills
dex-secretless-cicd-oidc, dex-ephemeral-test-credentials, dex-saas-risk-surface-review

## 14. Realistic Usage Example
```powershell
# Liệt kê các ServiceAccount trong cụm Kubernetes
kubectl get serviceaccounts -A -o custom-columns="NAMESPACE:.metadata.namespace,NAME:.metadata.name"

# Kiểm tra báo cáo thông tin xác thực IAM trên AWS
aws iam get-credential-report
```
