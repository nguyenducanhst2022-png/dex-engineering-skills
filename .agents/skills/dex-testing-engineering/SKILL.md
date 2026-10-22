---
name: dex-testing-engineering
description: Comprehensive automated testing engineering, test plan formulation, unit testing, integration testing, end-to-end (E2E) testing, regression suites, and boundary analysis. Guarantees behavioral correctness and test coverage. Use when designing test plans, authoring automated test suites, or preventing regressions.
---

# DEX Testing Engineering

## 1. Purpose & Scope
Xây dựng và duy trì hệ thống kiểm thử tự động chuyên sâu và toàn diện (Kim tự tháp kiểm thử: Unit, Integration, E2E), đảm bảo phần mềm hoạt động chính xác theo đặc tả, xử lý an toàn các trường hợp biên và ngăn chặn triệt để các lỗi hồi quy.

Quy trình testing chuẩn:
`Phân tích yêu cầu → Lập Test Plan → Viết Test Case → Unit Test → Integration Test → E2E Test → Regression Test → Sửa lỗi → Kiểm thử lại → Ổn định → Lưu Git`

Nguyên tắc cốt lõi: **Không chỉ kiểm tra xem code có chạy được hay không, mà phải xác minh chức năng đúng yêu cầu, xử lý được các tình huống lỗi và không phá vỡ chức năng cũ.**
Ghi nhớ sống còn: **Testing tốt = Kiểm thử đúng + Phát hiện lỗi sớm + Tự động hóa + Bao phủ tình huống thực tế.**

## 2. When to Use
- Trước hoặc trong khi phát triển tính năng mới (Test-Driven Development / Test-First).
- Khi bổ sung độ bao phủ kiểm thử (Code Coverage) cho mã nguồn chưa có test.
- Khi cần xây dựng Test Plan toàn diện cho một đợt phát hành quan trọng.
- Khi kiểm thử các tình huống biên (Boundary values, Null values, Timeout, Network partitions).

## 3. When NOT to Use
- Chạy các lệnh kiểm thử hồi quy nhanh cục bộ sau một dòng sửa typo (sử dụng `dex-code-verification`).
- Tự động nghiệm thu sản phẩm cuối cùng từ góc nhìn người dùng thực tế mà không có kịch bản UAT (sử dụng `dex-acceptance-testing`).

## 4. Prerequisites & Input Context
- Đặc tả yêu cầu kỹ thuật, Tiêu chí nghiệm thu (Acceptance Criteria).
- Mã nguồn của hệ thống cần kiểm thử.
- Test runner và assertion framework sẵn có (Jest, Vitest, Pytest, Go testing, Playwright, Cypress).

## 5. Core Concepts & Taxonomy
- **Nguyên tắc cốt lõi**: Tuân thủ triệt để nguyên lý vận hành xác định và ranh giới trách nhiệm của chuẩn Agent Skills.
- **Tính nhất quán hệ thống**: Mọi thao tác phải có thể kiểm chứng độc lập với kết quả đo lường rõ ràng.
- **Ngăn ngừa hồi quy**: Bất kỳ sửa đổi nào cũng phải bảo vệ tính tương thích ngược và chất lượng đã được nghiệm thu.

## 6. Step-by-Step Execution Workflow
### Bước 1: Lập Kế Hoạch Kiểm Thử (Test Plan Formulation)
- Xác định phạm vi kiểm thử theo mô hình Kim tự tháp kiểm thử (Testing Pyramid):
  - **Unit Tests (70%)**: Kiểm thử các hàm thuần túy, tính toán logic, validation, transformer (chạy cực nhanh, độc lập).
  - **Integration Tests (20%)**: Kiểm thử sự phối hợp giữa Service, Repository và Database thật (hoặc testcontainer).
  - **E2E Tests (10%)**: Kiểm thử các luồng hành trình người dùng quan trọng nhất (Happy path chính) từ frontend đến backend.

### Bước 2: Thiết Kế Ma Trận Ca Kiểm Thử (Test Case Matrix)
- Với mỗi chức năng, thiết kế tối thiểu 3 nhóm ca kiểm thử:
  1. **Happy Path**: Dữ liệu chuẩn, kết quả thành công mong đợi.
  2. **Boundary / Edge Cases**: Giá trị rỗng, giá trị cực đại, số 0, số âm, ký tự Unicode đặc biệt.
  3. **Error / Negative Cases**: Sai quyền, sai định dạng, tài nguyên không tồn tại, lỗi timeout.

### Bước 3: Triển Khai Unit Tests (Fast & Isolated)
- Viết các test case cô lập, tuân thủ cấu trúc **AAA (Arrange - Act - Assert)** hoặc **Given - When - Then**.
- Mock các phụ thuộc I/O nặng (mạng, email, cổng thanh toán) bằng test doubles (stubs/mocks) có kiểm soát.

### Bước 4: Triển Khai Integration & Contract Tests
- Kiểm thử các luồng giao tiếp thật với database (sử dụng SQLite in-memory hoặc PostgreSQL test container).
- Đảm bảo các giao dịch (Transactions) được rollback sạch sẽ sau mỗi ca kiểm thử để tránh làm bẩn dữ liệu test giữa các ca.

### Bước 5: Thực Thi Kiểm Thử Tự Động & Đo Độ Bao Phủ (Execution & Coverage)
- Chạy toàn bộ test suite bằng test runner:
  ```bash
  npm test -- --coverage
  # hoặc: pytest --cov=src tests/
  ```
- Rà soát các nhánh rẽ (branch coverage) chưa được test ghé thăm.

### Bước 6: Phân Tích Lỗi & Sửa Lỗi Tận Gốc (Defect Remediation)
- Nếu có bài test rớt: Không được sửa assertion của test để ép PASS, mà phải sửa mã nguồn của ứng dụng để đáp ứng đúng kỳ vọng kiểm thử.

### Bước 7: Kiểm Thử Hồi Quy Toàn Hệ Thống (Full Regression Run)
- Chạy toàn bộ test suite của toàn dự án để khẳng định không có tác dụng phụ nào làm hỏng code cũ.

## 7. Concrete Examples
```bash
# Lệnh thực thi & kiểm chứng tiêu chuẩn
dex verify --skill dex-testing-engineering
```

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước xác minh tự động và dựa vào giả định chủ quan.
- **Anti-Pattern 2**: Thay đổi diện rộng vượt ngoài phạm vi (Scope Creep) làm mất kiểm soát rủi ro.
- **Trap**: Thực hiện thao tác phá hủy hoặc thay đổi trạng thái sản xuất khi chưa qua cổng kiểm duyệt an toàn.

## 9. Quality Gates & Acceptance Criteria
- **QG-05 (100% Tests Pass)**: 100% các bài kiểm thử trong test suite đạt PASS.
- **QG-06 (Regression Suite Clean)**: Không có bất kỳ bài test hồi quy nào bị rớt.
- **QG-10 (Deterministic Output)**: Kết quả test ổn định, không có hiện tượng test chập chờn (Flaky tests).

## 10. Security & Safety Boundaries
- **Cấm Viết Test Vô Nghĩa (No Assert True Cheats)**: Cấm viết test không có assertion thực chất (ví dụ gọi hàm mà không kiểm tra giá trị trả về hoặc chỉ `expect(true).toBe(true)`).
- **Môi Trường Test Cách Ly Tuyệt Đối**: Cấm chạy bài test integration kết nối thẳng vào database production hoặc database dùng chung của dev khác.
- **Test Phải Độc Lập**: Thứ tự chạy các bài test không được ảnh hưởng đến kết quả của nhau (Mỗi test phải tự dọn dẹp trạng thái của mình).

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Kích hoạt thông qua terminal hoặc tiện ích mở rộng IDE tương thích (VS Code, Cursor, Windsurf).

## 12. Deliverables & Output Artifacts
1. Bản kế hoạch kiểm thử (Test Plan) bao quát các kịch bản quan trọng.
2. Bộ bài kiểm thử tự động (Unit, Integration, E2E) có cấu trúc sạch sẽ.
3. Báo cáo độ bao phủ mã nguồn (Coverage Report) và kết quả chạy test 100% PASS.

## 13. Related & Complementary Skills
- `dex-master-orchestrator`: Điều phối trung tâm.

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Kỹ sư hoặc AI Agent kích hoạt **dex-testing-engineering** trong dự án.
1. Tiếp nhận ngữ cảnh đầu vào và kiểm tra điều kiện tiên quyết tại Mục 4.
2. Vận hành tuần tự các bước theo Quy trình tại Mục 6.
3. Kiểm chứng đầu ra đối chiếu với Tiêu chuẩn chấp thuận tại Mục 9.
4. Bàn giao đầy đủ hiện vật theo Mục 12 và cập nhật tài liệu liên quan.
