---
name: dex-development-workflow
description: Standard iterative development workflow for AI coding. Enforces breaking tasks down, writing modular code, verifying functionality, stabilizing before upgrading, and committing safe checkpoints. Use when executing software development tasks, building features incrementally, or preventing scope-creep.
---

# DEX Development Workflow

## 1. Purpose
Thiết lập quy trình phát triển phần mềm chuẩn mực cho AI Coding Agent dựa trên nguyên lý Vibe Coding cốt lõi:
`Chia nhỏ → Viết code → Kiểm tra → Sửa lỗi → Ổn định → Lưu Git → Nâng cấp`

Nguyên tắc tối thượng: **Không nâng cấp hoặc thêm tính năng mới khi chức năng hiện tại chưa chạy ổn định.**

## 2. When to Use
- Khi bắt tay vào lập trình bất kỳ tính năng, module hoặc đoạn mã nào.
- Khi người dùng giao một yêu cầu lớn cần được chia nhỏ thành nhiều bước khả thi.
- Khi cần đảm bảo mã nguồn luôn ở trạng thái ổn định (green/working state) sau mỗi chu kỳ làm việc.

## 3. When Not to Use
- Chỉ đọc mã nguồn, trả lời câu hỏi giải thích hoặc tra cứu tài liệu mà không thay đổi code.
- Xử lý các sự cố khẩn cấp trên production đòi hỏi quy trình rollback tức thì (sử dụng `dex-release-engineering` hoặc `dex-root-cause-debugging`).

## 4. Inputs
- Mô tả yêu cầu kỹ thuật hoặc user story cần triển khai.
- Danh sách file thuộc phạm vi chỉnh sửa (Scope).
- Điểm kiểm tra hiện tại (trạng thái tests và Git commit hash gần nhất).

## 5. Workflow

### Bước 1: Chia nhỏ Nhiệm vụ (Decomposition)
- Phân rã yêu cầu lớn thành các bước nhỏ độc lập có thời gian thực hiện ngắn.
- Xác định thứ tự logic: Tầng dữ liệu/Model → Tầng nghiệp vụ/Logic → Tầng giao diện/API.

### Bước 2: Viết Code Từng phần (Incremental Implementation)
- Chỉ viết code cho đúng một bước nhỏ tại một thời điểm.
- Giữ code đơn giản, tập trung vào mục tiêu duy nhất của bước đó.
- Không tự ý thêm tính năng phỏng đoán ngoài yêu cầu.

### Bước 3: Kiểm tra Ngay Lập tức (Immediate Verification)
- Chạy thử nghiệm ngay sau khi viết xong một phần mã (Unit test hoặc chạy script kiểm tra nhanh).
- Đảm bảo đoạn mã mới hoạt động đúng như mong đợi.

### Bước 4: Sửa lỗi Tức thời (Instant Bug Fixing)
- Nếu phát hiện lỗi hoặc test rớt, dừng lại và sửa lỗi ngay tại chỗ.
- Không chuyển sang bước kế tiếp khi bước hiện tại còn lỗi.

### Bước 5: Ổn định Mã nguồn (Stabilization)
- Rà soát toàn bộ chức năng vừa thêm: chạy type-check, linter và kiểm thử hồi quy.
- Xác nhận không có tác dụng phụ làm hỏng các phần khác.

### Bước 6: Lưu Điểm An toàn (Git Checkpoint)
- Tạo commit an toàn với thông điệp rõ ràng để ghi nhận trạng thái ổn định.
- Đây là điểm phục hồi (checkpoint) nếu các bước nâng cấp sau gặp sự cố.

### Bước 7: Nâng cấp Tiếp theo (Upgrade / Next Increment)
- Chỉ khi bước trước đã ổn định và lưu Git, mới chuyển sang bước nhỏ tiếp theo trong danh sách.

## 6. Quality Gates
- **QG-01 (Scope Confined)**: Chỉ chỉnh sửa các file thuộc phạm vi bước hiện tại.
- **QG-03 (Clean Code)**: Không để sót lỗi cú pháp, linter hoặc type check.
- **QG-05 (Working Verified)**: Bước vừa làm phải có bằng chứng kiểm tra chạy thành công (PASS).
- **QG-08 (Clean Commit)**: Mỗi bước ổn định được ghi nhận bằng một commit gọn gàng.

## 7. Safety Rules
- **Quy tắc Một Bước**: Tuyệt đối không yêu cầu hoặc cho phép AI viết toàn bộ hệ thống lớn trong một lần duy nhất.
- **Cấm Xây Dựng Trên Nền Hỏng**: Cấm viết thêm tính năng nâng cao khi nền tảng cơ bản chưa kiểm thử thành công.
- **Bảo toàn Mã nguồn Cũ**: Không viết lại toàn bộ file nếu chỉ cần sửa hoặc bổ sung một hàm.

## 8. Expected Outputs
1. Mã nguồn hoàn thiện theo từng phần tăng dần.
2. Bộ kiểm thử tương ứng cho từng chức năng mới.
3. Chuỗi các Git commits ổn định, minh bạch.
4. Báo cáo tiến độ hoàn thành theo từng bước nhỏ.

## 9. Failure Handling
- Khi một bước bị lỗi kéo dài quá 3 lần thử: Rollback về commit ổn định gần nhất (`git checkout/restore`), đánh giá lại thiết kế và tiếp cận theo cách đơn giản hơn.
- Không chèn thêm code chắp vá để che giấu lỗi nền tảng.

## 10. Completion Criteria
- Toàn bộ các bước nhỏ trong nhiệm vụ đã được thực hiện và kiểm chứng.
- Hệ thống đạt trạng thái ổn định, không còn lỗi tồn đọng.
- Mã nguồn đã được commit an toàn vào Git.

---

## Real-world Example
Triển khai tính năng "Xác thực người dùng bằng JWT":
1. *Bước 1 (Chia nhỏ)*: Chia thành: (a) Hash password, (b) Sinh token JWT, (c) Middleware xác thực.
2. *Bước 2 & 3 (Hash password)*: Viết hàm hash với bcrypt → Chạy unit test kiểm tra verify password → PASS.
3. *Bước 4 & 5 (Ổn định)*: Linter check pass → Commit: `feat(auth): implement password hashing with bcrypt`.
4. *Bước 6 & 7 (Nâng cấp)*: Tiếp tục bước (b) sinh token JWT chỉ khi bước (a) đã có commit an toàn.
