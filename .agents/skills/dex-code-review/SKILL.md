---
name: dex-code-review
description: Comprehensive Git diff code review, Pull Request assessment, quality gate validation, and constructive feedback generation. Inspects diffs for correctness, security vulnerabilities, edge cases, and architectural compliance. Use before merging pull requests, auditing commits, or verifying peer agent code.
---

# DEX Code Review & Pull Request Assessment

## 1. Purpose
Thực hiện rà soát mã nguồn (Code Review) chuyên nghiệp trên từng dòng Git Diff trước khi hợp nhất (Merge) vào nhánh chính; đảm bảo mã nguồn sạch sẽ, không có lỗi tiềm ẩn, không chứa rác debug, tuân thủ tiêu chuẩn an ninh và có đầy đủ bằng chứng kiểm thử thực tế.

Quy trình Code Review chuẩn:
`Hoàn thành code → Tạo Diff → Review → Phát hiện vấn đề → Sửa lỗi → Kiểm thử lại → Phê duyệt → Merge`

Nguyên tắc cốt lõi: **Tuyệt đối không merge code khi chưa được review kỹ lưỡng. Mọi thay đổi đưa vào nhánh chính phải sạch sẽ, dễ hiểu, an toàn và có kiểm chứng rõ ràng.**
Ghi nhớ sống còn: **Code Review tốt = Bắt lỗi sớm trước khi lên Production + Nâng cao tiêu chuẩn code + Không để lọt mã độc hoặc rác.**

## 2. When to Use
- Trước khi phê duyệt và merge bất kỳ Pull Request (PR) hoặc Merge Request (MR) nào.
- Trước khi đóng gói phiên bản phát hành hoặc commit vào nhánh `main`/`develop`.
- Khi đóng vai trò Agent Reviewer kiểm tra mã nguồn do Agent Coder tạo ra trong quy trình Multi-Agent.
- Khi người dùng yêu cầu: *"Hãy review lại toàn bộ những gì bạn vừa sửa"*.

## 3. When Not to Use
- Khi mã nguồn đang trong giai đoạn nháp ban đầu (WIP / Draft) chưa chạy được và chưa sẵn sàng để review.
- Tranh cãi vụn vặt về phong cách thụt lề (Tabs vs. Spaces) mà công cụ tự động (Linter / Prettier) đã có thể giải quyết được.

## 4. Inputs
- Bản Git Diff đầy đủ (`git diff main...feature-branch` hoặc `git diff HEAD~1`).
- Mô tả mục tiêu của Pull Request và liên kết đến đặc tả (`SPEC.md` / Ticket issue).
- Kết quả chạy kiểm thử tự động của CI/CD pipeline.

## 5. Workflow

### Bước 1: Kiểm Tra Tính Toàn Vẹn Tổng Thể Của PR (Sanity Check)
- Đọc mô tả PR: Mục tiêu có rõ ràng không?
- Kiểm tra quy mô PR: PR có quá lớn không? (Lý tưởng < 400 dòng diff). Nếu PR quá lớn (>1000 dòng), yêu cầu chia nhỏ.
- Kiểm tra trạng thái CI: Pipeline kiểm tra tĩnh và test suite có xanh (PASS) không? Nếu CI đang đỏ (FAIL) → **TỪ CHỐI REVIEW NGAY LẬP TỨC**.

### Bước 2: Soát Từng Dòng Git Diff (Line-by-Line Inspection)
- Đọc kỹ từng dòng thêm mới (`+`) và dòng bị xóa (`-`):
  - **Tính đúng đắn (Correctness)**: Đoạn mã có thực sự giải quyết đúng bài toán không? Có xử lý các trường hợp biên (`null`, `undefined`, mảng rỗng) không?
  - **Tính an toàn (Security)**: Có nguy cơ SQL Injection, XSS, lộ token bí mật hoặc bypass xác thực không?
  - **Hiệu năng (Performance)**: Có vòng lặp lồng nhau vô tận, query N+1, rò rỉ bộ nhớ hoặc gọi API tuần tự lãng phí không?
  - **Độ sạch (Cleanliness)**: Có sót lại `console.log`, code bị comment vô nghĩa (`// dead code`), file tạm (`.DS_Store`, `.env`) không?

### Bước 3: Đánh Giá Bộ Kiểm Thử Đi Kèm (Test Suite Quality)
- Code mới có bài test đi kèm không?
- Bài test có thực sự kiểm tra logic cốt lõi không, hay chỉ là test hình thức (Mocking quá đà / Assert true)?
- Các kịch bản lỗi (Unhappy path) có được kiểm thử không?

### Bước 4: Phân Loại Nhận Xét (Constructive Feedback)
- Đưa ra nhận xét có tính xây dựng, phân loại theo mức độ:
  - **[BLOCKER]**: Lỗi nghiêm trọng, lỗ hổng bảo mật hoặc vi phạm kiến trúc (Bắt buộc phải sửa mới được merge).
  - **[WARNING]**: Điểm cần cải thiện về hiệu năng hoặc đặt tên, không làm sập app nhưng nên sửa.
  - **[NITPICK / SUGGESTION]**: Đề xuất nhỏ mang tính cá nhân, tác giả có thể cân nhắc hoặc bỏ qua.

### Bước 5: Đưa Ra Kết Luận Cuối Cùng (Review Verdict)
- Đưa ra 1 trong 3 kết luận minh bạch:
  1. **APPROVE**: Mã nguồn xuất sắc, sạch sẽ, test đầy đủ → Cho phép merge.
  2. **REQUEST CHANGES**: Còn tồn tại lỗi [BLOCKER] cần sửa chữa → Nêu rõ các việc cần làm.
  3. **NOT VERIFIED**: Thiếu môi trường chạy test hoặc CI chưa chạy xong.

## 6. Quality Gates
- **QG-01 (Scope Confined)**: Không có file lạ hoặc không liên quan bị sửa trong PR.
- **QG-05 (Tests Included & PASS)**: Code mới có test tương ứng và 100% test đạt PASS.
- **QG-07 (Security Reviewed)**: Không phát hiện lỗ hổng bảo mật nào trong diff.
- **QG-08 (Clean Diff Guaranteed)**: 0 dòng code rác, 0 comment thừa, 0 console.log tạm thời.

## 7. Safety Rules
- **Không Tự Phê Duyệt (No Self-Approval)**: Agent viết code không được tự đưa ra kết luận APPROVE cho chính mình mà không thực hiện quy trình review khách quan từng dòng.
- **Không Phê Duyệt Khi Còn Lỗi Nghiêm Trọng**: Tuyệt đối không bao giờ bấm nút APPROVE "cho xong chuyện" khi còn lỗi [BLOCKER] chưa được giải quyết.
- **Tôn Trọng Quyền Quyết Định Của Con Người**: Mọi quyết định merge vào nhánh phát hành cuối cùng luôn cần sự đồng thuận của người dùng.

## 8. Expected Outputs
1. Bản báo cáo Code Review chi tiết theo từng dòng file.
2. Danh sách các vấn đề phân loại theo `[BLOCKER]`, `[WARNING]`, `[SUGGESTION]`.
3. Kết luận rõ ràng: `APPROVE`, `REQUEST CHANGES` hoặc `NOT VERIFIED`.

## 9. Failure Handling
- Nếu tác giả code không đồng ý với nhận xét: Tổ chức thảo luận dựa trên tài liệu đặc tả và các nguyên lý kỹ thuật khách quan, không tranh cãi cảm tính.

## 10. Completion Criteria
- Mọi nhận xét [BLOCKER] đều đã được giải quyết triệt để.
- Bản Git Diff cuối cùng đạt trạng thái sạch sẽ và được phê duyệt chính thức.

---

## Real-world Example
Nhận xét review mẫu cho một Pull Request:
```markdown
### DEX CODE REVIEW SUMMARY: PR #42 - Add Coupon Support

- **Kết luận**: **REQUEST CHANGES** ❌
- **Phân tích chi tiết**:
  1. `src/services/coupon.ts#L45`: **[BLOCKER]** Phát hiện SQL Injection tiềm ẩn khi nối chuỗi mã giảm giá vào query. Yêu cầu chuyển sang parameterized query `$1`.
  2. `src/services/coupon.ts#L88`: **[BLOCKER]** Chưa kiểm tra trường hợp `discount > total_amount`, có thể dẫn đến tổng tiền thanh toán bị âm.
  3. `src/controllers/coupon.ts#L12`: **[NITPICK]** Có một câu lệnh `console.log("DEBUG COUPON", code)` chưa xóa trước khi tạo PR.
- **Yêu cầu**: Vui lòng sửa 2 mục BLOCKER và xóa console.log, sau đó chạy lại test suite để được review lại.
```
