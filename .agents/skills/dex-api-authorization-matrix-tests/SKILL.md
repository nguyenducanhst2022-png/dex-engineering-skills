---
name: dex-api-authorization-matrix-tests
description: Automate exhaustive Cartesian-product authorization matrix testing to detect Broken Object Level Authorization (BOLA/IDOR) and Broken Object Property Level Authorization (BOPLA). Use when auditing API security boundaries.
---

# dex-api-authorization-matrix-tests

## 1. Purpose & Scope
Tự động hóa kiểm thử ma trận phân quyền tích Descartes (Cartesian-Product Authorization Matrix Tests); phát hiện triệt để các lỗ hổng phân quyền cấp đối tượng (BOLA / IDOR) và phân quyền cấp thuộc tính (BOPLA / Mass Assignment) trên các API REST và GraphQL.

## 2. When to Use
- Khi hệ thống có nhiều vai trò người dùng (Admin, Manager, Member, Guest) và các ranh giới sở hữu tài nguyên phức tạp (Tenant A vs Tenant B).
- Khi kiểm toán định kỳ bảo mật API theo danh mục OWASP API Security Top 10.
- Khi bổ sung API endpoint mới và muốn bảo đảm người dùng không thể xem hoặc sửa dữ liệu của người khác bằng cách đổi ID trên URL.

## 3. When NOT to Use
- Khi API là endpoint công khai thuần túy (như bảng giá công cộng hoặc trang tin tức không yêu cầu đăng nhập).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Đặc tả API (OpenAPI spec), ma trận phân quyền vai trò (Role-Permission Matrix), người dùng thử nghiệm đại diện cho từng vai trò và tenant.
- **Quyền hạn truy cập:** Quyền thực thi các bài kiểm thử tự động trên môi trường staging.

## 5. Core Concepts & Taxonomy
- **BOLA / IDOR (Broken Object Level Authorization):** Người dùng A đăng nhập hợp lệ nhưng có thể đọc hoặc ghi đè tài nguyên của người dùng B bằng cách thay đổi ID (`/api/orders/999`).
- **BOPLA (Broken Object Property Level Authorization):** Người dùng thông thường có thể tự cấp quyền admin hoặc thay đổi số dư tài khoản thông qua việc gửi thêm trường trong request payload (`{ "isAdmin": true }`).
- **Cartesian Product Matrix:** Tích của (Danh sách Roles) x (Danh sách Tenants) x (Danh sách Endpoints) x (Danh sách HTTP Methods) để kiểm thử toàn diện mọi kịch bản khả dĩ.

## 6. Step-by-Step Execution Workflow
1. Khảo sát và lập bảng ma trận phân quyền mong đợi (Expected Permission Matrix) cho từng endpoint và thuộc tính.
2. Khởi tạo tối thiểu hai tenant độc lập (Tenant A, Tenant B) với các vai trò tương ứng (Admin, Member, Guest).
3. Tự động sinh các ca kiểm thử tích Descartes: Người dùng Tenant A cố gắng truy cập tài nguyên của Tenant B.
4. Thực hiện các request cập nhật chứa các trường nhạy cảm (`role`, `is_verified`, `balance`) để kiểm tra BOPLA.
5. Tự động kiểm tra mã phản hồi HTTP: Mọi hành vi truy cập trái phép bắt buộc phải nhận về mã `403 Forbidden` hoặc `404 Not Found` (không được trả về `200 OK`).
6. Xuất báo cáo ma trận phân quyền trực quan và gắn cờ các lỗ hổng phát hiện được.

## 7. Concrete Examples
### Kiểm thử tự động phát hiện BOLA/IDOR bằng Pytest:
```python
import pytest
import requests

ROLES = ["admin", "member", "guest"]
TENANTS = ["tenant_alpha", "tenant_beta"]

@pytest.mark.parametrize("role", ROLES)
def test_cross_tenant_isolation_bola(role):
    # Lay token cua user thuoc Tenant Beta
    token_beta = get_user_token(tenant="tenant_beta", role=role)
    headers = {"Authorization": f"Bearer {token_beta}"}
    
    # Co tinh truy cap tai nguyen cua Tenant Alpha
    alpha_resource_id = "res_alpha_12345"
    response = requests.get(f"https://api.staging.internal/documents/{alpha_resource_id}", headers=headers)
    
    # Bat buoc he thong phai tu choi truy cap
    assert response.status_code in [403, 404], (
        f"LOHONG BOLA: User role {role} cua Tenant Beta da doc duoc tai nguyen cua Tenant Alpha! "
        f"HTTP Status: {response.status_code}"
    )
```

## 8. Anti-Patterns & Common Traps
- **Relying on Client-Side Hiding:** Ẩn nút bấm trên giao diện web nhưng không kiểm tra quyền trên API endpoint backend.
- **Testing Only Happy Path:** Chỉ kiểm tra xem admin có vào được hay không mà quên kiểm tra xem user thường có bị chặn hay không.
- **Returning Detailed Error Messages on BOLA:** Trả về lỗi `403 Forbidden: Ban khong so huu don hang 123` làm lộ thông tin sự tồn tại của đơn hàng cho tin tặc.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: 100% các ca kiểm thử truy cập chéo tenant đều bị chặn với mã 403 hoặc 404.
- **QG-04**: Không có bất kỳ trường dữ liệu cấm nào bị cập nhật thành công qua tấn công Mass Assignment (BOPLA).
- **QG-09**: Độ phủ kiểm toán ma trận phân quyền đạt 100% các endpoint thay đổi trạng thái (POST, PUT, DELETE).

## 10. Security & Safety Boundaries
- Triệt tiêu hoàn toàn lỗ hổng bảo mật số 1 trong danh mục OWASP API Security Top 10.

## 11. Platform Adapters
- **Testing Tools**: Pytest, REST-assured, Playwright, Newman (Postman), OWASP ZAP.

## 12. Deliverables & Output Artifacts
- Bảng ma trận phân quyền tích Descartes hoàn chỉnh.
- Test suite kiểm thử BOLA/BOPLA tự động chạy trong CI.
- Báo cáo kết quả đánh giá các điểm rò rỉ phân quyền.

## 13. Related & Complementary Skills
dex-ephemeral-test-credentials, dex-secretless-cicd-oidc, dex-privacy-safe-observability

## 14. Realistic Usage Example
```powershell
# Chạy suite kiểm toán ma trận phân quyền API
pytest tests/security/test_authz_matrix.py -v

# Quét kiểm tra Mass Assignment bằng kịch bản tự động
python scripts/security/audit_bopla_endpoints.py --spec openapi.yaml
```
