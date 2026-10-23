---
name: dex-ephemeral-test-credentials
description: Provision, scope, and automatically destroy dynamic short-lived credentials for databases, cloud services, and third-party APIs during CI/CD test runs. Use when isolating automated tests and preventing credential sprawl.
---

# dex-ephemeral-test-credentials

## 1. Purpose & Scope
Khởi tạo, giới hạn phạm vi và tự động hủy bỏ các thông tin xác thực động ngắn hạn (Dynamic Ephemeral Credentials) cho cơ sở dữ liệu, dịch vụ đám mây và API bên thứ ba trong quá trình chạy kiểm thử CI/CD; ngăn ngừa tràn lan thông tin nhạy cảm và bảo đảm cô lập hoàn toàn giữa các lần chạy test.

## 2. When to Use
- Khi các bài test tự động cùng dùng chung một tài khoản database duy nhất gây xung đột ghi đè dữ liệu hoặc deadlock.
- Khi một bài test bị sập giữa chừng và để lại các quyền hạn thừa thãi không ai dọn dẹp.
- Khi tích hợp HashiCorp Vault hoặc Testcontainers để cấp phát tài khoản database động cho từng test runner.

## 3. When NOT to Use
- Khi tiến hành kiểm thử đơn vị (Unit Tests) thuần túy với các mock/stub trong bộ nhớ không tương tác với dịch vụ bên ngoài.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Hệ thống quản lý bí mật động (HashiCorp Vault, AWS Secrets Manager, Testcontainers), cơ sở dữ liệu hoặc dịch vụ đích.
- **Quyền hạn truy cập:** Quyền quản trị cho phép tạo người dùng tạm thời trong cơ sở dữ liệu.

## 5. Core Concepts & Taxonomy
- **Dynamic Secrets:** Thông tin đăng nhập được sinh ra theo yêu cầu (on-demand) với thời gian sống (TTL) định sẵn và tự động bị hủy (revocation) khi hết hạn.
- **Per-Run Database Role:** Mỗi lần chạy test suite sẽ nhận một username/password ngẫu nhiên duy nhất với schema riêng biệt.
- **Lease Management:** Cơ chế gia hạn hoặc hủy bỏ phiên làm việc ngay khi tiến trình test kết thúc (thông qua hook `teardown`).

## 6. Step-by-Step Execution Workflow
1. Cấu hình Database Secrets Engine trên HashiCorp Vault kết nối tới cơ sở dữ liệu kiểm thử.
2. Thiết lập Role mẫu định nghĩa câu lệnh SQL tạo user tạm thời kèm thời hạn sống (TTL = 10 phút).
3. Trước khi chạy test, script runner gọi API Vault để xin cấp phát cặp username/password động.
4. Thực thi test suite với thông tin đăng nhập vừa được cấp phát.
5. Ngay khi test kết thúc (thành công hoặc thất bại), gửi yêu cầu thu hồi (Revoke Lease) tới Vault để xóa user lập tức.
6. Nếu runner bị tắt đột ngột, cơ chế TTL tự động của Vault sẽ xóa user sau khi hết 10 phút.

## 7. Concrete Examples
### Cấp phát và thu hồi tài khoản Database động bằng HashiCorp Vault trong Python:
```python
import hvac
import pytest

@pytest.fixture(scope="session")
def dynamic_db_credentials():
    client = hvac.Client(url='https://vault.internal.domain:8200')
    client.auth.approle.login(role_id='ci-runner', secret_id='...')
    
    # Xin cap credentials dong voi TTL 5 phut
    secret = client.secrets.database.generate_credentials(name='ci-test-role')
    username = secret['data']['username']
    password = secret['data']['password']
    lease_id = secret['lease_id']
    
    yield {"username": username, "password": password, "conn_str": f"postgresql://{username}:{password}@db:5432/testdb"}
    
    # Teardown: Thu hoi va tieu huy tai khoan ngay lap tuc
    client.sys.revoke_lease(lease_id=lease_id)
    print(f"Da thu hoi va tieu huy tai khoan tam thoi: {username}")
```

## 8. Anti-Patterns & Common Traps
- **Hardcoding Root DB Passwords in CI:** Đặt mật khẩu `postgres/postgres` trong biến môi trường dùng chung cho toàn bộ công ty.
- **Failing to Revoke on Crash:** Không cài đặt cơ chế TTL tự động khiến cơ sở dữ liệu tích tụ hàng nghìn tài khoản rác sau vài tháng.
- **Sharing Write Permissions Across Parallel Tests:** Hai luồng test chạy song song dùng chung một tài khoản làm xáo trộn dữ liệu của nhau.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: 100% tài khoản test được tạo ra đều có thời hạn sống (TTL) tối đa dưới 30 phút.
- **QG-04**: Cơ chế thu hồi (Revocation) kích hoạt thành công kể cả khi bài test bị dừng đột ngột (Abort).
- **QG-07**: Mỗi phiên chạy test sở hữu một định danh người dùng độc lập hoàn toàn.

## 10. Security & Safety Boundaries
- Giới hạn quyền hạn của tài khoản tạm thời chỉ được thao tác trong cơ sở dữ liệu kiểm thử, tuyệt đối cấm truy cập vào production.

## 11. Platform Adapters
- **Secret Managers**: HashiCorp Vault Database Secrets Engine, AWS Secrets Manager, Testcontainers Cloud, Akeyless.

## 12. Deliverables & Output Artifacts
- Cấu hình Vault Database Engine và SQL Template tạo user.
- Pytest / Jest fixture quản lý vòng đời credential tạm thời.
- Kịch bản dọn dẹp và kiểm toán các lease quá hạn.

## 13. Related & Complementary Skills
dex-secretless-cicd-oidc, dex-service-account-lifecycle, dex-api-authorization-matrix-tests

## 14. Realistic Usage Example
```powershell
# Xin cấp phát thông tin đăng nhập tạm thời qua Vault CLI
vault read database/creds/ci-test-role

# Kiểm tra danh sách các lease đang hoạt động
vault list sys/leases/lookup/database/creds/ci-test-role
```
