---
name: dex-root-cause-debugging
description: Root cause analysis and deterministic bug resolution methodology. Reproduces defects with failing tests, isolates fundamental root causes, applies targeted fixes, and prevents regressions. Use when investigating bugs, fixing unexpected test failures, resolving exceptions, or eliminating persistent software defects.
---

# DEX Root Cause Debugging

## 1. Purpose
Điều tra, cô lập và giải quyết triệt để các lỗi phần mềm tận gốc rễ, ngăn chặn tình trạng "sửa mò", che giấu triệu chứng hoặc làm phát sinh lỗi hồi quy ở các phần khác.

Quy trình debug chuẩn:
`Phát hiện lỗi → Tái hiện lỗi → Phân tích nguyên nhân → Sửa tận gốc → Test lại → Kiểm tra hồi quy → Ổn định`

Nguyên tắc cốt lõi: **Không sửa mò, không che giấu lỗi, không chỉ sửa triệu chứng bề mặt mà bỏ qua nguyên nhân gốc.**
Ghi nhớ sống còn: **Sửa hết thông báo lỗi (Error message) ≠ Đã giải quyết được nguyên nhân gốc.**

## 2. When to Use
- Khi nhận được thông báo lỗi, exception stack trace hoặc hành vi sai khác kỳ vọng.
- Khi một bài kiểm thử tự động bị rớt (FAIL).
- Khi người dùng báo cáo lỗi chập chờn (flaky bug) hoặc dữ liệu bị sai lệch bất thường.
- Khi mã nguồn sửa trước đó làm phát sinh lỗi mới ở nơi khác.

## 3. When Not to Use
- Thêm tính năng mới hoàn toàn khi hệ thống không có bug nào cần giải quyết.
- Tối ưu hóa hiệu năng thuần túy cho mã nguồn vốn dĩ đã chạy đúng (dùng `dex-performance-optimization`).

## 4. Inputs
- Thông báo lỗi đầy đủ, Stack trace, file log hệ thống.
- Các bước thao tác dẫn đến lỗi (Steps to Reproduce) và dữ liệu đầu vào cụ thể.
- Mã nguồn tại các vị trí nghi ngờ phát sinh sự cố.

## 5. Workflow

### Bước 1: Tiếp Nhận & Ghi Nhận Lỗi (Defect Triage)
- Đọc kỹ thông báo lỗi và stack trace: Xác định chính xác file, hàm và dòng code xảy ra sự cố.
- Phân biệt giữa lỗi cú pháp (Syntax), lỗi thực thi (Runtime exception) và lỗi logic nghiệp vụ (Logic bug).

### Bước 2: Tái Hiện Lỗi Xác Thực (Deterministic Reproduction)
- **Tạo một bài kiểm tra tự động bị rớt (Failing Test)** tái hiện chính xác 100% tình huống gây lỗi với dữ liệu cụ thể.
- Nếu không thể viết test ngay: Tạo một script kiểm thử độc lập ngắn gọn để kích hoạt lỗi.
- Không bao giờ bắt đầu sửa code khi chưa tái hiện được lỗi.

### Bước 3: Phân Tích Nguyên Nhân Gốc (Root Cause Analysis - 5 Whys)
- Đặt câu hỏi tìm nguyên nhân sâu xa:
  - *Tại sao biến bị undefined?* → Vì hàm `getUser` trả về null khi không tìm thấy ID.
  - *Tại sao ID không tìm thấy?* → Vì tham số truyền từ client bị thiếu padding số 0.
- Xác định điểm sai lệch gốc thay vì chỉ chèn `if (!x) return` để tắt thông báo lỗi.

### Bước 4: Sửa Lỗi Tận Gốc (Targeted Root Fix)
- Chỉnh sửa logic tại đúng nơi phát sinh nguyên nhân.
- Giữ giải pháp sửa lỗi tối giản, không viết lại những vùng code xung quanh không liên quan.
- Bổ sung validation hoặc xử lý biên đúng chuẩn mực.

### Bước 5: Kiểm Thử Lại (Test Verification)
- Chạy lại bài kiểm tra tái hiện lỗi ở Bước 2.
- Bài kiểm tra phải chuyển từ trạng thái `FAIL` sang `PASS` hoàn toàn.

### Bước 6: Kiểm Tra Hồi Quy Toàn Diện (Regression Testing)
- Chạy toàn bộ test suite của module và các module phụ thuộc.
- Xác nhận bản vá lỗi không làm rớt bất kỳ bài test nào đã có từ trước.

### Bước 7: Ổn Định & Lưu Git (Stabilization & Commit)
- Lưu commit chuẩn: `fix(scope): resolve root cause of [defect description]`.
- Giữ lại bài kiểm tra mới tạo ở Bước 2 trong repository để trở thành regression test vĩnh viễn ngăn lỗi tái diễn.

## 6. Quality Gates
- **QG-01 (Scope Confined)**: Bản sửa lỗi chỉ can thiệp vào các thành phần liên quan trực tiếp đến nguyên nhân gốc.
- **QG-05 (Failing Test Passes)**: Test case tái hiện lỗi chuyển từ FAIL sang PASS.
- **QG-06 (No Regressions)**: 100% các bài test cũ vẫn đạt PASS.
- **QG-08 (Clean Diff)**: Không để sót console log, debug print hoặc comment tạm thời.

## 7. Safety Rules
- **Cấm Tuyệt Đối "Bịt Lỗ Hổng Ảo"**: Cấm dùng `catch (e) {}` rỗng hoặc `@ts-ignore` bừa bãi để dập tắt lỗi.
- **Không Đoán Mò**: Không thay đổi code ngẫu nhiên theo kiểu "thử xem có hết lỗi không" khi chưa hiểu nguyên nhân.
- **Bảo Vệ Dữ Liệu**: Không chạy các câu lệnh xóa hoặc cập nhật dữ liệu hàng loạt trên môi trường thật để debug.

## 8. Expected Outputs
1. Bản phân tích nguyên nhân gốc (Root Cause Summary).
2. Test case tái hiện lỗi mới được bổ sung vào bộ kiểm thử.
3. Bản vá lỗi mã nguồn sạch sẽ, dứt điểm.
4. Bằng chứng kiểm thử PASS sau khi sửa.

## 9. Failure Handling
- Nếu sau 3 lần sửa mà bài test tái hiện vẫn FAIL: Dừng lại, xóa bỏ các thay đổi tạm (`git restore`), xem xét lại giả thuyết nguyên nhân gốc, đọc thêm log hoặc tham vấn tài liệu/người dùng.

## 10. Completion Criteria
- Lỗi được tái hiện và triệt tiêu hoàn toàn.
- Test case tái hiện lỗi đã PASS và được lưu vào kho mã nguồn.
- Không gây phát sinh lỗi hồi quy ở bất kỳ chức năng nào khác.

---

## Real-world Example
Ứng dụng bị sập với lỗi: `TypeError: Cannot read properties of undefined (reading 'toUpperCase')`.
1. *Tái hiện lỗi*: Viết test `test_format_name_with_null_input()` → Test rớt (FAIL).
2. *Phân tích gốc*: API trả về `middle_name: null` thay vì chuỗi rỗng khi người dùng không có tên đệm.
3. *Sửa gốc*: Bổ sung chuẩn hóa dữ liệu tại DTO parser: `middleName: raw.middle_name ?? ''` thay vì chỉ bọc `try-catch` tại hàm render.
4. *Test lại*: Test `test_format_name_with_null_input()` PASS.
5. *Kiểm tra hồi quy*: Toàn bộ 42 tests của module User PASS 100%.
