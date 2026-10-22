---
name: dex-test-data-management
description: Architect secure, isolated, synthetic, and ephemeral test data fixtures and databases with automated teardown and masking. Use when managing complex state across integration and end-to-end tests without test pollution.
---

# dex-test-data-management

## 1. Purpose & Scope
Thiết kế, xây dựng và quản lý dữ liệu kiểm thử (test data) an toàn, biệt lập và có thể dọn dẹp tức thì (ephemeral); tạo lập synthetic data, làm sạch (masking/sanitization) dữ liệu nhạy cảm và bảo đảm tính độc lập giữa các test cases.

## 2. When to Use
- Các bài test phụ thuộc lẫn nhau do dùng chung cơ sở dữ liệu và sửa đổi cùng một bản ghi.
- Cần dữ liệu phong phú để test các kịch bản biên nhưng không được dùng dữ liệu production thật do luật bảo mật (GDPR/HIPAA).
- Quá trình reset database giữa các lần test quá chậm.

## 3. When NOT to Use
- Không dùng dữ liệu thật từ production mà chưa qua quy trình anonymization/masking nghiêm ngặt.
- Không dùng cho các unit test đơn giản chỉ cần in-memory mocks.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Lược đồ cơ sở dữ liệu (DML/DDL hoặc ORM models).
- Các quy tắc ràng buộc toàn vẹn dữ liệu.
- Danh sách các trường nhạy cảm cần ẩn danh (PII).
- **Điều kiện tiên quyết**:
- Có quyền tạo và hủy database schema tạm thời trong môi trường test (Docker/Testcontainers).

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Ephemeral Fixtures: Dữ liệu chỉ tồn tại trong phạm vi bài test và được rollback qua database transaction hoặc xóa sạch ngay sau đó.
- Synthetic Data Generation: Dùng thư viện (Faker, FactoryBoy) sinh dữ liệu hợp lệ về mặt logic nhưng hoàn toàn giả lập.
- Deterministic Seeding: Khởi tạo dữ liệu mẫu với fixed random seed để tái hiện chính xác lỗi khi cần.
- **Quy tắc quyết định kỹ thuật**:
- Với integration tests: ưu tiên bọc mỗi test case trong một Transaction và Rollback ở teardown.
- Với E2E tests: sinh account/workspace riêng biệt với UUID ngẫu nhiên cho từng test run.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Lỗi rò rỉ dữ liệu test vào môi trường production do sai lệch biến môi trường `DATABASE_URL`.

## 6. Step-by-Step Execution Workflow
1. Phân loại các trường dữ liệu nhạy cảm trong hệ thống.
2. Xây dựng Factory classes để sinh model entities với các giá trị mặc định an toàn.
3. Thiết lập cơ chế Transaction Rollback hoặc Docker Testcontainers cho mỗi suite.
4. Tích hợp kịch bản dọn dẹp dữ liệu mồ côi (cleanup sweep).
5. Kiểm tra thời gian khởi tạo dữ liệu không vượt quá 10% tổng thời gian chạy test.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```python
import factory
from src.models import User

class UserFactory(factory.Factory):
    class Meta:
        model = User
    
    id = factory.Faker('uuid4')
    email = factory.Faker('safe_email')
    full_name = factory.Faker('name')
    is_active = True
```

### Lệnh xác minh & thực thi:
```bash
pytest --setup-show tests/integration/
```

## 8. Anti-Patterns & Common Traps
- Hardcode ID như `user_id = 1` trong toàn bộ test suite.
- Copy nguyên database production về máy local để test mà không che PII.

## 9. Quality Gates & Acceptance Criteria
- 100% dữ liệu thử nghiệm được dọn dẹp sạch sau khi test runner kết thúc.
- 0 trường PII thực tế nào xuất hiện trong fixtures repository.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Tuyệt đối cấm sử dụng số thẻ tín dụng hoặc mật khẩu thật trong test factories.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ thống hỗ trợ**: Linux (CI/CD runners), macOS, Windows 11 PowerShell/WSL2.

## 12. Deliverables & Output Artifacts
- Module Factories/Fixtures chuẩn hóa.
- Script seed và reset database tự động.

## 13. Related & Complementary Skills
dex-flaky-test-remediation, dex-database-design, dex-integration-testing

## 14. Realistic Usage Example
### Tình huống thực tế:
Một hệ thống SaaS bị chậm CI do phải seed 50MB SQL dump trước mỗi bài test. Đội ngũ chuyển đổi sang dùng FactoryBoy kết hợp PostgreSQL template databases, giảm thời gian chuẩn bị dữ liệu từ 45 giây xuống còn 800ms cho mỗi worker.
