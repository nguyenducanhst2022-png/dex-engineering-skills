---
name: dex-code-verification
description: Rigorous code verification and quality assurance protocol for AI-generated code. Inspects syntax, runs automated test suites, validates functional correctness, detects edge-case defects, and requires execution evidence. Use after code generation, before accepting tasks as complete, or to eliminate false-completion claims.
---

# DEX Code Verification

## 1. Purpose
Xác minh thực tế chất lượng và tính đúng đắn của mã nguồn do AI tạo ra thông qua kiểm tra đa tầng, thực thi lệnh thật và thu thập bằng chứng thực nghiệm.

Quy trình xác minh:
`Đọc code → Chạy thử → Test chức năng → Phát hiện lỗi → Sửa lỗi → Test lại → Xác nhận đạt`

Nguyên tắc tối thượng: **Không tin AI báo "hoàn thành" khi chưa có bằng chứng kiểm thử thực tế.**
Ghi nhớ sống còn: **Code chạy được ≠ Code đúng ≠ Code ổn định.**

## 2. When to Use
- Ngay sau khi AI viết hoặc chỉnh sửa bất kỳ đoạn mã nào.
- Trước khi báo cáo hoàn thành nhiệm vụ cho người dùng.
- Trước khi tạo Git commit hoặc chuyển sang bước kế tiếp.
- Khi nghi ngờ AI tạo mã giả, mock ảo hoặc che giấu lỗi biên dịch.

## 3. When Not to Use
- Khi chỉ thực hiện việc đọc hiểu hoặc giải thích mã nguồn mà không có thay đổi file.
- Khi kiểm thử quy mô lớn toàn bộ hành trình người dùng E2E (khi đó sử dụng `dex-acceptance-testing`).

## 4. Inputs
- Mã nguồn mới tạo hoặc vừa được sửa đổi.
- Bộ test hiện có của dự án hoặc kịch bản kiểm tra chức năng.
- Lệnh thực thi kiểm tra (Test runner, script, CLI tool).

## 5. Workflow

### Bước 1: Đọc & Soát Mã nguồn (Code Inspection)
- Đọc lại toàn bộ đoạn code vừa thay đổi.
- Kiểm tra tính logic: có hàm rỗng (stub/placeholder), `TODO`, hoặc biến chưa khai báo không?
- Kiểm tra xử lý trường hợp biên (null, undefined, mảng rỗng, chuỗi rỗng).

### Bước 2: Chạy Thử Biên Dịch / Linter (Syntax & Type Check)
- Thực thi công cụ kiểm tra tĩnh của dự án:
  - TypeScript/JavaScript: `tsc --noEmit` hoặc `npm run type-check`.
  - Python: `mypy .` hoặc `flake8`.
  - Rust/Go: `cargo check` / `go vet`.
- Đảm bảo 0 lỗi biên dịch, 0 cảnh báo nghiêm trọng.

### Bước 3: Test Chức Năng (Functional Testing)
- Thực thi test suite liên quan đến chức năng vừa sửa:
  - Chạy unit test / integration test.
  - Kiểm tra cả kịch bản thành công (Happy Path) và kịch bản lỗi (Unhappy Path).

### Bước 4: Phát Hiện & Bóc Tách Lỗi (Defect Detection)
- Nếu lệnh chạy trả về mã lỗi (`exit code != 0`), thu thập log lỗi chi tiết.
- Không bỏ qua bất kỳ cảnh báo ngoại lệ nào trong terminal output.

### Bước 5: Sửa Lỗi Tận Gốc (Fix Defects)
- Phân tích nguyên nhân và sửa đúng vị trí phát sinh lỗi.
- Không sửa kiểu che giấu lỗi (như dùng `try-catch` nuốt lỗi hoặc ép kiểu `any` bừa bãi).

### Bước 6: Test Lại Toàn Diện (Re-test & Regression Check)
- Chạy lại bài kiểm tra bị rớt để xác nhận đã chuyển sang trạng thái PASS.
- Chạy lại các bài kiểm tra liền kề để đảm bảo không làm hỏng tính năng cũ.

### Bước 7: Xác Nhận Đạt với Bằng Chứng (Verified Confirmation)
- Chỉ tuyên bố "Hoàn thành" khi có output thực tế của terminal chứng minh PASS 100%.

## 6. Quality Gates
- **QG-03 (Lint & Type Clean)**: Lệnh kiểm tra tĩnh trả về exit code 0.
- **QG-04 (Build Clean)**: Dự án build thành công không lỗi cú pháp.
- **QG-05 (Tests PASS)**: Kết quả test suite đạt 100% PASS cho các ca kiểm thử liên quan.
- **QG-10 (Real Terminal Evidence)**: Có bằng chứng output thực tế từ terminal, không bịa đặt log.

## 7. Safety Rules
- **Cấm Tuyệt Đối "Báo Hoàn Thành Ảo" (No False Completion)**: Nghiêm cấm việc khẳng định tính năng đã chạy tốt mà không chạy lệnh kiểm chứng.
- **Không Dùng Test Giả (No Mock Cheating)**: Không được viết test luôn trả về `expect(true).toBe(true)` chỉ để vượt qua CI/CD.
- **Phân Biệt Rõ Trạng Thái**: Nếu môi trường không hỗ trợ chạy test (thiếu runtime), phải khai báo rõ là `NOT VERIFIED`, cấm khai khống là `PASS`.

## 8. Expected Outputs
1. Log thực thi lệnh từ terminal (stdout & stderr).
2. Tóm tắt kết quả kiểm tra định lượng: Tổng số test, số test PASS, số test FAIL.
3. Danh sách các lỗi đã phát hiện và đã sửa chữa trong quá trình xác minh.

## 9. Failure Handling
- Nếu test liên tục thất bại sau 2 lần sửa: Chuyển giao ngay cho `dex-root-cause-debugging` để phân tích sâu hơn cấu trúc dữ liệu và logic ngầm.

## 10. Completion Criteria
- Mã nguồn vượt qua kiểm tra tĩnh (Typecheck/Lint).
- Toàn bộ test case liên quan đạt trạng thái PASS.
- Bằng chứng thực nghiệm được ghi nhận đầy đủ vào báo cáo.

---

## Real-world Example
Agent vừa sửa hàm tính thuế `calculateTax(price, rate)`.
1. *Đọc code*: Phát hiện nếu `price < 0` hàm trả về số âm vô lý.
2. *Chạy test*: `pytest tests/test_tax.py` → FAIL: `assert calculateTax(-10, 0.1) == 0`.
3. *Sửa lỗi*: Bổ sung guard clause: `if price < 0: raise ValueError("Price cannot be negative")`.
4. *Test lại*: `pytest tests/test_tax.py` → Output: `2 passed in 0.05s`.
5. *Xác nhận đạt*: Ghi nhận trạng thái PASS kèm log terminal thật.
