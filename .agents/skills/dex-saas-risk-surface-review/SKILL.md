---
name: dex-saas-risk-surface-review
description: Audit, score, and govern third-party SaaS integrations, OAuth application permissions, Webhook security, and data sharing postures. Use when mitigating third-party supply-chain exposure across corporate ecosystems.
---

# dex-saas-risk-surface-review

## 1. Purpose & Scope
Kiểm toán, chấm điểm và quản trị các tích hợp SaaS của bên thứ ba, quyền cấp phép ứng dụng OAuth (OAuth Apps), tính bảo mật của Webhook và tư thế chia sẻ dữ liệu; bảo đảm kiểm soát chặt chẽ bề mặt rủi ro chuỗi cung ứng từ các đối tác phần mềm.

## 2. When to Use
- Khi các phòng ban trong công ty tự ý kết nối các ứng dụng SaaS bên ngoài vào Slack, Google Workspace, GitHub hoặc Microsoft 365 (Hiện tượng Shadow IT).
- Khi kiểm toán định kỳ các ứng dụng OAuth của bên thứ ba có quyền đọc email, mã nguồn hoặc tài liệu nội bộ.
- Khi triển khai một giải pháp SaaS mới và cần đánh giá mức độ rủi ro tuân thủ bảo mật thông tin (SOC2, ISO 27001).

## 3. When NOT to Use
- Khi phân tích các thư viện mã nguồn nội bộ thuần túy không có kết nối ra dịch vụ đám mây bên ngoài.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Danh mục ứng dụng SaaS đang sử dụng, bảng phân quyền OAuth scopes, tài khoản quản trị viên Workspace / GitHub / Slack.
- **Quyền hạn truy cập:** Quyền kiểm tra nhật ký ứng dụng kết nối và cấu hình bảo mật của tổ chức.

## 5. Core Concepts & Taxonomy
- **Overprivileged OAuth Scopes:** Các ứng dụng chỉ cần đọc thông tin cá nhân nhưng lại đòi toàn quyền truy cập hộp thư (`mail.readwrite`) hoặc toàn bộ mã nguồn private (`repo`).
- **Shadow IT Discovery:** Phát hiện các công cụ SaaS được nhân viên sử dụng mà không thông qua phê duyệt của phòng Công nghệ và An ninh thông tin.
- **Webhook Authenticity:** Bảo đảm các webhook từ SaaS gửi về máy chủ nội bộ đều được xác thực bằng chữ ký mật mã (HMAC SHA-256), chống giả mạo dữ liệu.

## 6. Step-by-Step Execution Workflow
1. Quét toàn bộ danh sách các ứng dụng OAuth bên thứ ba đã được cấp quyền trong Google Workspace, Microsoft 365, GitHub và Slack.
2. Phân loại và chấm điểm rủi ro cho từng ứng dụng dựa trên độ nhạy cảm của các Scopes được yêu cầu.
3. Thu hồi quyền (Revoke Access) ngay lập tức đối với các ứng dụng đã ngừng sử dụng trên 90 ngày hoặc có nhà phát triển không rõ nguồn gốc.
4. Rà soát cơ chế xác thực Webhook của các dịch vụ SaaS đối tác (kiểm tra Secret Key, IP Whitelisting).
5. Thiết lập chính sách kiểm duyệt ứng dụng tập trung (Admin Approval Required): nhân viên không thể tự ý cấp quyền cho ứng dụng mới.
6. Lập báo cáo kiểm toán bề mặt rủi ro SaaS định kỳ hàng quý cho ban giám đốc.

## 7. Concrete Examples
### Kiểm tra và thu hồi quyền các ứng dụng OAuth nguy hiểm trên GitHub bằng API:
```python
import requests

GITHUB_TOKEN = "ghp_..."
ORG_NAME = "my-corporate-org"

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

def audit_github_oauth_apps():
    url = f"https://api.github.com/orgs/{ORG_NAME}/installations"
    resp = requests.get(url, headers=headers).json()
    
    for app in resp.get("installations", []):
        app_name = app["app_slug"]
        permissions = app["permissions"]
        print(f"App: {app_name} | Quyen han: {permissions}")
        
        # Canh bao neu ung dung co quyen ghi vao tat ca repositories
        if permissions.get("administration") == "write" or permissions.get("contents") == "write":
            print(f"CANH BAO RUI RO CAO: Ung dung '{app_name}' co toan quyen ghi vao codebase!")
```

## 8. Anti-Patterns & Common Traps
- **Permissive Self-Service App Install:** Cho phép mọi nhân viên thoải mái bấm 'Allow' cài đặt các ứng dụng và plugin bên ngoài mà không có kiểm duyệt.
- **Unsigned Webhooks:** Chấp nhận xử lý dữ liệu Webhook từ đối tác SaaS mà không kiểm tra chữ ký HMAC trong HTTP headers.
- **Abandoned Integrations:** Cấp quyền cho một công cụ dùng thử trong 14 ngày nhưng sau đó quên không thu hồi quyền truy cập trong nhiều năm.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Bật chế độ phê duyệt của quản trị viên (Admin Approval) trên 100% các nền tảng SaaS cốt lõi.
- **QG-04**: 0% ứng dụng bên thứ ba không hoạt động trong 90 ngày còn giữ quyền truy cập.
- **QG-08**: 100% endpoint nhận Webhook đều có xác thực chữ ký số HMAC hợp lệ.

## 10. Security & Safety Boundaries
- Ngăn ngừa các vụ tấn công chuỗi cung ứng nghiêm trọng tương tự như các vụ rò rỉ token thông qua ứng dụng OAuth của đối tác.

## 11. Platform Adapters
- **Platforms**: Google Workspace Admin SDK, Microsoft Entra ID (Azure AD), GitHub App Management, Slack Admin APIs.

## 12. Deliverables & Output Artifacts
- Danh mục kiểm toán toàn bộ ứng dụng OAuth bên thứ ba.
- Bảng chấm điểm rủi ro các tích hợp SaaS (SaaS Risk Matrix).
- Quy trình chuẩn phê duyệt và thu hồi ứng dụng tự động.

## 13. Related & Complementary Skills
dex-service-account-lifecycle, dex-dependency-update-risk-scoring, dex-secretless-cicd-oidc

## 14. Realistic Usage Example
```powershell
# Liệt kê các ứng dụng OAuth đã cài đặt trong GitHub Organization
gh api orgs/my-org/installations --jq ".installations[].app_slug"

# Quét phát hiện Shadow IT qua bản ghi DNS / SSO logs
python scripts/security/audit_saas_integrations.py
```
