---
name: dex-technical-debt-refactoring
description: Systematic technical debt assessment, safe code refactoring, code smell eradication, and behavioral preservation. Improves modularity, readability, and maintainability while guaranteeing zero breaking regressions with automated test harnesses. Use when refactoring legacy code, cleaning up duplicated logic, or untangling complex methods.
---

# DEX Technical Debt & Refactoring

## 1. Purpose
Đánh giá và kiểm soát nợ kỹ thuật (Technical Debt), thực hiện tái cấu trúc mã nguồn (Refactoring) an toàn và bài bản nhằm cải thiện khả năng đọc, tính dễ bảo trì và khả năng mở rộng của phần mềm mà tuyệt đối **không làm thay đổi hành vi nghiệp vụ hiện tại**.

Quy trình tái cấu trúc chuẩn:
`Phân tích code → Phát hiện nợ kỹ thuật → Đánh giá mức độ → Lập kế hoạch → Refactor → Kiểm thử hồi quy → Ổn định → Lưu Git`

Nguyên tắc cốt lõi: **Cải thiện cấu trúc nội tại của code mà không làm thay đổi hành vi bên ngoài hoặc phá vỡ các chức năng hiện có.**
Ghi nhớ sống còn: **Refactoring tốt = Code sạch hơn + Dễ bảo trì hơn + Không phá chức năng cũ.**

## 2. When to Use
- Khi một hàm hoặc module trở nên quá phức tạp, khó đọc, độ phức tạp Cyclomatic quá cao (>10-15).
- Khi xuất hiện tình trạng lặp code (Code duplication / Copy-paste programming) ở nhiều nơi.
- Khi cần chuẩn bị nền tảng mã nguồn sạch trước khi bổ sung một tính năng phức tạp mới.
- Khi cần loại bỏ các "mùi khó chịu của code" (Code Smells: Long Method, Large Class, Primitive Obsession, Feature Envy).

## 3. When Not to Use
- Sửa lỗi phần mềm đang xảy ra (khi đó phải dùng `dex-root-cause-debugging` trước).
- Đồng thời vừa thêm tính năng mới vừa viết lại toàn bộ cấu trúc trong cùng một commit.
- Khi mã nguồn hiện tại hoàn toàn chưa có bất kỳ bài kiểm tra (Unit test) nào để bảo vệ hành vi cũ.

## 4. Inputs
- Vùng mã nguồn legacy hoặc phức tạp cần tái cấu trúc.
- Bộ kiểm thử hiện hữu của module (nếu chưa có, phải viết bổ sung Characterization Tests trước).
- Bản phân tích các chỉ số code quality (ví dụ: SonarQube, ESLint complexity report).

## 5. Workflow

### Bước 1: Khảo Sát & Phát Hiện Mùi Code (Code Smell Detection)
- Nhận diện các vấn đề nợ kỹ thuật phổ biến:
  - Hàm quá dài (>50 dòng), có quá nhiều mức thụt đầu dòng (Nested if-else).
  - Tên biến, tên hàm tối nghĩa, không phản ánh đúng ý đồ kinh doanh.
  - Sử dụng "Magic numbers" hoặc "Magic strings" rải rác.
  - Phụ thuộc cứng vào các triển khai cụ thể thay vì abstraction.

### Bước 2: Thiết Lập Lưới An Toàn Kiểm Thử (Establish Test Harness)
- **Bắt buộc**: Kiểm tra xem module đã có đủ bài kiểm thử để bao quát toàn bộ các ca sử dụng hiện tại hay chưa.
- Nếu chưa có: Viết ngay các bài kiểm tra đặc tả hành vi hiện tại (Characterization Tests) để "đóng băng" hành vi của hệ thống trước khi tái cấu trúc.
- Chạy test đảm bảo 100% PASS trước khi sửa bất kỳ dòng mã nguồn nào.

### Bước 3: Lập Kế Hoạch Từng Bước Nhỏ (Micro-step Planning)
- Chia quá trình tái cấu trúc thành các thao tác vi mô:
  - Tách hàm (Extract Method).
  - Đổi tên biến/hàm cho rõ nghĩa (Rename Variable/Function).
  - Thay thế câu lệnh điều kiện lồng nhau bằng Guard Clauses.
  - Thay thế tham số rời rạc bằng Đối tượng tham số (Introduce Parameter Object).

### Bước 4: Thực Hiện Tái Cấu Trúc Vi Mô (Incremental Refactoring)
- Chỉ thực hiện một thao tác vi mô duy nhất tại một thời điểm.
- Giữ logic bên ngoài (Public API / Interface) hoàn toàn không thay đổi.

### Bước 5: Chạy Kiểm Thử Hồi Quy Sau Mỗi Bước Nhỏ (Instant Regression Test)
- Ngay sau mỗi thao tác (ví dụ vừa tách xong một hàm), chạy lại toàn bộ test suite.
- Nếu test xanh (PASS): Tiếp tục thao tác nhỏ kế tiếp.
- Nếu test đỏ (FAIL): Lập tức hoàn tác lại thao tác vừa làm, kiểm tra tại sao hành vi bị thay đổi.

### Bước 6: Ổn Định & Ghi Nhận Lịch Sử (Stabilize & Commit)
- Lưu commit chuẩn: `refactor(billing): extract discount calculation into separate pure function`.
- Không gộp nhiều thay đổi không liên quan vào cùng một commit.

## 6. Quality Gates
- **QG-01 (Scope Confined)**: Chỉ tái cấu trúc nội bộ module mục tiêu, không đổi interface công khai.
- **QG-05 (100% Tests Pass)**: Toàn bộ bài test cũ đạt PASS 100% mà không cần phải sửa đổi assertion của test.
- **QG-06 (Zero Behavior Change)**: Xác nhận không có sự thay đổi nào về hành vi đầu ra đối với cùng một tập dữ liệu đầu vào.
- **QG-08 (Clean Refactor Diff)**: Git diff thể hiện rõ mục đích dọn dẹp, không trộn lẫn tính năng mới.

## 7. Safety Rules
- **Không Refactor Khi Chưa Có Test**: Tuyệt đối không bao giờ tái cấu trúc một đoạn mã legacy phức tạp khi chưa có test suite bảo vệ.
- **Không Đổi Hành Vi Trong Quá Trình Refactor**: Nếu muốn thay đổi logic nghiệp vụ, phải làm thành 2 bước riêng biệt: Refactor trước để code sạch → Sau đó mới thêm tính năng trong commit khác.
- **Nguyên Tắc Hướng Đạo Sinh (Boy Scout Rule)**: Hãy luôn để mã nguồn sạch hơn lúc bạn mới tiếp cận một chút, nhưng không được biến nhiệm vụ sửa một lỗi nhỏ thành cuộc đại tu toàn bộ dự án.

## 8. Expected Outputs
1. Mã nguồn sạch sẽ, dễ hiểu, tuân thủ nguyên tắc SOLID và DRY.
2. Bộ kiểm thử hồi quy bảo vệ hành vi cũ.
3. Không có bất kỳ lỗi hồi quy nào phát sinh.

## 9. Failure Handling
- Nếu việc tái cấu trúc làm rớt test mà không tìm ra nguyên nhân nhanh chóng: Dùng `git restore` đưa file về commit ổn định gần nhất và chia thao tác thành các bước nhỏ hơn nữa.

## 10. Completion Criteria
- Mã nguồn dễ đọc hơn, độ phức tạp giảm rõ rệt.
- Toàn bộ test suite vượt qua với kết quả tương đương 100% hành vi cũ.

---

## Real-world Example
Hàm `processOrder()` dài 120 dòng với 4 tầng `if (user != null) { if (user.isActive) { ... } }`:
1. *Bảo vệ bằng test*: Đảm bảo 6 unit tests cho các trường hợp active, inactive, null user đều PASS.
2. *Thao tác 1*: Áp dụng Guard Clauses:
   ```typescript
   if (!user) throw new Error("User required");
   if (!user.isActive) throw new Error("User inactive");
   ```
3. *Chạy test*: 6 tests PASS.
4. *Thao tác 2*: Tách hàm gửi email ra `sendOrderConfirmation(order)` riêng biệt.
5. *Chạy test*: 6 tests PASS → Commit: `refactor(order): apply guard clauses and extract email notification`.
