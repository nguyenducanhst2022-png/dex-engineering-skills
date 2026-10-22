---
name: dex-acceptance-testing
description: User Acceptance Testing (UAT), end-user journey simulation, acceptance criteria verification, and product acceptance reporting. Validates business value from the real user perspective. Use during product sign-offs, pre-delivery acceptance, or validating customer journey completeness.
---

# DEX User Acceptance Testing (UAT)

## 1. Purpose
Thực hiện kiểm thử nghiệm thu thực tế từ góc nhìn của người dùng cuối (User Acceptance Testing - UAT); xác nhận phần mềm không chỉ vượt qua các bài kiểm tra kỹ thuật máy móc mà thực sự đáp ứng đúng nhu cầu sử dụng thực tế, giải quyết trọn vẹn bài toán kinh doanh và sẵn sàng để bàn giao hoặc đưa vào sử dụng.

Quy trình nghiệm thu UAT chuẩn:
`Xác định yêu cầu → Tạo kịch bản → Kiểm thử thực tế → Thu thập kết quả → Đánh giá → Sửa lỗi → Nghiệm thu`

Nguyên tắc cốt lõi: **Phần mềm chỉ thực sự hoàn thiện khi người dùng sử dụng được một cách thuận tiện và đáp ứng đúng nhu cầu, không đơn thuần chỉ là vượt qua các bài kiểm thử kỹ thuật trong phòng thí nghiệm.**
Ghi nhớ sống còn: **Test kỹ thuật PASS ≠ Người dùng nghiệm thu. Kiểm thử thực tế = Thao tác thật + Dữ liệu thật + Kịch bản người dùng thật.**

## 2. When to Use
- Trước khi bàn giao sản phẩm hoặc tính năng hoàn thiện cho khách hàng / Product Owner.
- Khi cần kiểm chứng trọn vẹn các hành trình người dùng xuyên suốt (End-to-End User Journeys).
- Khi đánh giá tính năng trên môi trường Staging/UAT với dữ liệu mẫu thực tế.
- Khi chốt biên bản nghiệm thu kỹ thuật (Acceptance Sign-off).

## 3. When Not to Use
- Trong quá trình đang code dở dang từng hàm nhỏ bên trong module.
- Thay thế cho Unit test và Integration test của lập trình viên (UAT là tầng nghiệm thu cuối cùng, không phải tầng phát hiện cú pháp).

## 4. Inputs
- Bản đặc tả kỹ thuật và tiêu chí nghiệm thu (`SPEC.md` / User Stories).
- Môi trường kiểm thử UAT có dữ liệu tương đương môi trường thật (Staging environment).
- Danh sách các vai trò người dùng (Personas: Khách vãng lai, Khách hàng thân thiết, Quản trị viên).

## 5. Workflow

### Bước 1: Rà Soát Tiêu Chí Nghiệm Thu (Acceptance Criteria Alignment)
- Đọc lại toàn bộ danh sách tiêu chí nghiệm thu đã thống nhất trong `SPEC.md`.
- Xác định các luồng nghiệp vụ quan trọng nhất mang lại giá trị cốt lõi cho người dùng.

### Bước 2: Xây Dựng Bộ Kịch Bản UAT Thực Tế (UAT Scenario Design)
- Thiết kế các kịch bản kiểm thử theo ngôn ngữ người dùng, bao gồm:
  - **Mục tiêu hành trình**: Ví dụ: "Người dùng mới đăng ký tài khoản, tìm kiếm sản phẩm và đặt hàng thành công".
  - **Dữ liệu chuẩn bị**: Tài khoản test, thẻ ngân hàng test, sản phẩm có sẵn trong kho.
  - **Các bước thao tác**: Từng thao tác cụ thể người dùng sẽ bấm trên màn hình.
  - **Kết quả mong đợi thực tế**: Giao diện hiển thị gì, email xác nhận nhận được nội dung gì, số dư ví thay đổi ra sao.

### Bước 3: Chuẩn Bị Dữ Liệu & Môi Trường An Toàn (Test Environment Prep)
- Đảm bảo môi trường UAT hoàn toàn độc lập, sử dụng cổng thanh toán Sandbox và server gửi mail ảo (như Mailtrap) để tránh gửi thư thật cho khách hàng thật.

### Bước 4: Thực Thi Kiểm Thử Thực Tế Từng Bước (Live Scenario Execution)
- Thực hiện thao tác kiểm tra tuần tự từ đầu đến cuối hành trình (bằng tay hoặc bằng Playwright/Cypress tự động):
  - Kiểm tra hành trình thành công (Happy User Journey).
  - Kiểm tra hành trình xử lý tình huống bất ngờ: Người dùng nhập sai mã OTP, đổi ý hủy đơn giữa chừng, mất mạng khi đang thanh toán.

### Bước 5: Thu Thập Bằng Chứng & Đánh Giá Kết Quả (Evidence Collection)
- Ghi nhận kết quả minh bạch cho từng kịch bản:
  - **PASS**: Hành vi hoàn hảo đúng mong đợi.
  - **FAIL**: Gặp lỗi, giao diện khó hiểu hoặc luồng bị nghẽn (chụp ảnh màn hình / quay video minh chứng).
  - **NOT VERIFIED**: Chưa đủ điều kiện kiểm tra.

### Bước 6: Phân Loại Lỗi Theo Tác Động Người Dùng (Defect Severity)
- Phân loại lỗi phát hiện trong UAT:
  - **BLOCKER**: Người dùng không thể hoàn thành hành trình chính (Ví dụ nút Thanh toán không bấm được).
  - **MAJOR**: Hoàn thành được nhưng phải thao tác vòng vo, khó hiểu.
  - **COSMETIC**: Sai lỗi chính tả, lệch vị trí nút bấm nhẹ.

### Bước 7: Khắc Phục, Kiểm Thử Lại & Ký Biên Bản Nghiệm Thu (Sign-off)
- Sửa toàn bộ các lỗi BLOCKER và MAJOR được phê duyệt.
- Chạy lại kịch bản UAT để xác nhận đã PASS hoàn toàn.
- Lập biên bản báo cáo nghiệm thu sản phẩm (Product Acceptance Report).

## 6. Quality Gates
- **QG-02 (Acceptance Criteria 100% Met)**: Tất cả các tiêu chí nghiệm thu trong bản đặc tả đều được xác minh đạt.
- **QG-05 (All UAT Scenarios PASS)**: 100% các kịch bản hành trình người dùng chính đạt PASS.
- **QG-10 (Verified User Evidence)**: Có bằng chứng kiểm thử thực tế (ảnh chụp, log thao tác, video), không bịa đặt phản hồi giả của người dùng.

## 7. Safety Rules
- **Cấm Tuyệt Đối Bịa Đặt Nghiệm Thu Giả (No Fake Acceptance)**: Nghiêm cấm Agent tự ý tuyên bố "Khách hàng đã chấp nhận sản phẩm" khi chưa thực sự thực thi các bước kiểm thử theo kịch bản.
- **Cách Ly Triệt Để Dữ Liệu Thực**: Cấm thực hiện các kịch bản test UAT có dữ liệu rác trên cơ sở dữ liệu Production của khách hàng thật.
- **Không Bỏ Qua Ý Kiến Trải Nghiệm**: Nếu một thao tác gây bối rối nghiêm trọng cho người dùng dù code không có lỗi crash, vẫn phải ghi nhận là vấn đề cần cải thiện.

## 8. Expected Outputs
1. Bộ tài liệu kịch bản UAT (UAT Test Scenarios).
2. Biên bản ghi nhận kết quả kiểm thử thực tế kèm bằng chứng minh họa.
3. Báo cáo nghiệm thu sản phẩm (Acceptance Sign-off Report).

## 9. Failure Handling
- Nếu kịch bản UAT cốt lõi bị FAIL: Đưa tính năng về trạng thái `REJECTED`, yêu cầu đội ngũ phát triển sửa lỗi theo quy trình và tổ chức nghiệm thu lại.

## 10. Completion Criteria
- Tất cả hành trình người dùng chính thực thi trơn tru không lỗi.
- Toàn bộ tiêu chí nghiệm thu ban đầu được thỏa mãn và có báo cáo xác nhận.

---

## Real-world Example
Kịch bản UAT: "Áp dụng mã giảm giá HAPPYNEWYEAR":
- *Bước 1*: Người dùng chọn 1 áo thun trị giá 200.000đ vào giỏ hàng.
- *Bước 2*: Tại màn hình thanh toán, nhập mã `HAPPYNEWYEAR` và bấm "Áp dụng".
- *Kết quả thực tế*: Hệ thống hiển thị dòng giảm giá `-40.000đ (20%)`, tổng tiền cập nhật thành `160.000đ` ngay lập tức không cần tải lại trang.
- *Xác nhận*: PASS 100% đúng với kỳ vọng người dùng.
