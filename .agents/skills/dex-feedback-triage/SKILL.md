---
name: dex-feedback-triage
description: Triage, classify, and route high-velocity user feedback, bug reports, and app reviews into actionable engineering tasks using automated categorization and deduplication. Use when managing user complaints and issue backlogs.
---

# dex-feedback-triage

## 1. Purpose & Scope
Thiết lập quy trình tiếp nhận, phân loại và điều phối phản hồi người dùng với tốc độ cao (High-Velocity User Feedback & Bug Triage); chuyển hóa các ý kiến phàn nàn, đánh giá trên App Store / Play Store, ticket hỗ trợ khách hàng (Zendesk / Intercom) và báo cáo lỗi thành các tác vụ kỹ thuật cụ thể (Actionable Engineering Issues); tự động phân loại mức độ nghiêm trọng (Severity), trích xuất công thức tái lập lỗi (Reproduction Recipe), phát hiện trùng lặp (Deduplication) và điều phối chính xác tới đội ngũ chịu trách nhiệm.

## 2. When to Use
- Khi số lượng phản hồi người dùng hoặc ticket hỗ trợ tăng đột biến (>50-100 tickets/ngày) khiến đội ngũ bị quá tải.
- Khi các lỗi nghiêm trọng (Critical Bugs) bị chìm nghỉm giữa hàng trăm góp ý tính năng thông thường, dẫn tới chậm trễ xử lý.
- Khi kỹ sư mất quá nhiều thời gian chỉ để hỏi lại khách hàng thông tin cơ bản: 'Bạn dùng phiên bản nào? Dùng hệ điều hành gì? Làm sao để bị lỗi?'.

## 3. When NOT to Use
- Tự động hóa khắc phục sự cố hạ tầng máy chủ nội bộ (dùng `dex-runbook-automation`).
- Lập trình tính năng mới trong ứng dụng (dùng `dex-development-workflow`).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Dữ liệu phản hồi thô: Đánh giá App Store / Google Play, Zendesk tickets, tin nhắn cộng đồng Discord/Slack.
- Metadata người dùng: Phiên bản app, Model thiết bị, Hệ điều hành, User ID.
- Quy tắc phân loại (Triage Rubric: P0 Blocker, P1 Critical, P2 Major, P3 Minor).
- **Điều kiện tiên quyết**:
- Công cụ quản lý công việc (GitHub Issues, Jira, Linear) có template báo cáo lỗi chuẩn hóa.
- Webhook hoặc công cụ tổng hợp phản hồi tập trung.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- **Triage Severity Matrix (P0 to P3)**: P0 (Hệ thống sập, mất tiền, không thể đăng nhập -> Sửa trong 2h); P1 (Tính năng chính bị hỏng không có giải pháp tạm thời -> Sửa trong 24h); P2 (Lỗi ảnh hưởng một phần có giải pháp thay thế -> Xếp vào Sprint tiếp theo); P3 (Lỗi hiển thị nhỏ, typo -> Xử lý khi rảnh).
- **Reproduction Recipe Extraction**: Một báo cáo lỗi chỉ có giá trị khi trích xuất được 3 yếu tố: Các bước thực hiện (Steps to Reproduce), Kết quả thực tế (Actual Result), và Kết quả mong đợi (Expected Result).
- **Semantic Deduplication**: Gom nhóm các phàn nàn có từ ngữ khác nhau nhưng cùng chung 1 nguyên nhân gốc (ví dụ: 'Không bấm được nút mua' và 'Màn hình thanh toán bị đơ' đều thuộc về Issue #402).
- **Quy tắc quyết định kỹ thuật**:
- **Triage Trong Vòng 4 Giờ Cho Lỗi Mới**: Mọi ticket mới gửi về phải được phân loại và gán độ ưu tiên trong tối đa 4 giờ làm việc.
- **Không Tạo Issue Kỹ Thuật Khi Chưa Có Cách Tái Lập**: Nếu thiếu thông tin thiết bị hoặc các bước tái lập, ticket phải được giữ ở trạng thái `needs-info` để đội CS hỏi thêm trước khi đẩy sang kỹ sư.
- **Gắn Liên Kết Tới Bug Bounty / Security Ngay Lập Tức**: Bất kỳ phản hồi nào nghi ngờ liên quan tới bảo mật, lộ lọt dữ liệu phải được chuyển thẳng sang kênh bảo mật khẩn cấp (Security Escalation Path).
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Kỹ sư tốn cả buổi sáng điều tra một lỗi không tồn tại**: Do người dùng dùng phiên bản app cũ từ 2 năm trước đã ngừng hỗ trợ -> Khắc phục: Tự động đính kèm metadata phiên bản vào báo cáo và từ chối báo cáo từ phiên bản hết hạn.
- **Lập 10 issue trùng nhau trên Jira cho cùng 1 lỗi**: Khiến 3 kỹ sư cùng nhảy vào sửa một chỗ -> Khắc phục: Sử dụng công cụ tìm kiếm ngữ nghĩa (Semantic Search / Embedding Deduplication) để phát hiện issue trùng lặp trước khi tạo mới.

## 6. Step-by-Step Execution Workflow
1. Thu thập phản hồi từ các nguồn (App Store reviews, In-app feedback form, CS tickets) về kho lưu trữ tập trung.
2. Tự động trích xuất metadata hệ thống (OS, device, network, app version, error logs).
3. Phân loại loại hình: Lỗi kỹ thuật (Bug), Yêu cầu tính năng (Feature Request), hay Trải nghiệm người dùng (UX Friction).
4. Đánh giá mức độ nghiêm trọng (P0, P1, P2, P3) theo ma trận Triage.
5. Kiểm tra trùng lặp với danh sách Issue đang mở trên GitHub/Linear; nếu trùng lặp thì gắn liên kết (link as duplicate).
6. Nếu là lỗi mới: Tạo Issue có cấu trúc chuẩn (Steps to reproduce, stack trace, logs) và gán cho Tech Lead của module tương ứng.
7. Đóng vòng lặp phản hồi (Close the Loop): Khi kỹ sư merge bản vá, tự động gửi thông báo cập nhật cho khách hàng đã báo lỗi.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```markdown
# Standard Bug Triage Report (GitHub Issue Template)

## [P1 - High] Không thể tải ảnh biên lai khi dùng Android 14

### 1. Phân Loại Triage
- **Category**: Bug Report
- **Severity**: P1 (Chức năng cốt lõi bị chặn, ảnh hưởng ~12% người dùng Android)
- **Affected Module**: `feature-expense-upload`
- **Assigned Team**: Mobile Team A

### 2. Môi Trường Gặp Lỗi
- **App Version**: v3.4.1 (Build 402)
- **OS**: Android 14 (API 34)
- **Device**: Samsung Galaxy S23, Pixel 7

### 3. Các Bước Tái Lập (Steps to Reproduce)
1. Mở màn hình Tạo Chi Phí Mới.
2. Bấm vào nút 'Chụp/Tải Ảnh Biên Lai'.
3. Chọn một ảnh định dạng `.heic` từ thư viện ảnh hệ thống.

### 4. Kết Quả Thực Tế vs Mong Đợi
- **Thực tế**: Ứng dụng hiện thông báo 'Lỗi không xác định' và nút Tải lên bị vô hiệu hóa.
- **Mong đợi**: Ảnh được nén và hiển thị bản xem trước thu nhỏ thành công.

### 5. Log & Stack Trace Trích Xuất
```text
java.lang.SecurityException: Permission Denial: opening provider MediaDocumentsProvider
  at com.myapp.feature.expense.ImagePicker.handleResult(ImagePicker.kt:84)
```

### 6. Nguyên Nhân Sơ Bộ & Đề Xuất
Do Android 14 áp dụng quyền Selected Photos Access (`READ_MEDIA_VISUAL_USER_SELECTED`) mới chưa được xử lý trong `ImagePicker`.
```

### Lệnh xác minh & thực thi:
- Kiểm tra thời gian phản hồi triage trung bình: Truy vấn chỉ số MTTA (Mean Time to Acknowledge) trên Linear/Jira (phải < 4h)
- Kiểm tra tỷ lệ trùng lặp: Xác nhận các issue trùng nhau được gom vào 1 master ticket
- Chạy script tự động phân loại phản hồi bằng AI/Rule: `python scripts/triage_feedback.py --input raw_reviews.json`

## 8. Anti-Patterns & Common Traps
- **Bỏ mặc phản hồi 1 sao trên App Store không ai đọc**: Khiến điểm đánh giá ứng dụng tụt dốc thảm hại.
- **Biến toàn bộ phàn nàn của khách hàng thành P0**: Làm loãng mức độ ưu tiên, khiến đội ngũ kiệt sức và mất niềm tin vào hệ thống triage.
- **Đóng ticket của khách hàng bằng câu trả lời tự động vô cảm**: 'Cảm ơn bạn, chúng tôi đã ghi nhận' mà không bao giờ có hành động tiếp theo.

## 9. Quality Gates & Acceptance Criteria
- QG-01: 100% các lỗi P0/P1 được phân loại và giao việc trong vòng dưới 2 giờ.
- QG-08: Tỷ lệ issue tạo mới có đầy đủ thông tin tái lập đạt >= 90%.
- QG-11: Tỷ lệ trùng lặp (Duplicate Issues) trong Backlog giảm trên 70% sau khi áp dụng deduplication.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi deploy.

## 10. Security & Safety Boundaries
- Tự động xóa sạch mật khẩu, số thẻ ngân hàng hoặc thông tin cá nhân mà khách hàng vô tình đính kèm trong ảnh chụp màn hình gửi lên.
- Giới hạn quyền truy cập thông tin định danh khách hàng trong công cụ triage nội bộ.
- Không bao giờ lưu trữ hardcoded secret hoặc cấp quyền quá mức (over-permissioned IAM).

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Môi trường Vận hành & Tuân thủ**: Hỗ trợ GDPR/CCPA tooling, SOC 2 / ISO 27001 automation, ArgoCD drift, RICE spreadsheets, Jira/GitHub triage.

## 12. Deliverables & Output Artifacts
- Quy trình và bảng tiêu chí phân loại lỗi (Triage Rubric Guide).
- Mẫu Issue Template chuẩn hóa trên GitHub / Jira.
- Báo cáo thống kê xu hướng lỗi người dùng phản hồi hàng tuần.

## 13. Related & Complementary Skills
- `dex-root-cause-debugging`: Tiếp nhận issue từ triage và tiến hành sửa lỗi trong code.
- `dex-feature-prioritization`: Đưa các phản hồi cải tiến sản phẩm vào ma trận RICE.
- `dex-incident-postmortems`: Nâng cấp lỗi P0 diện rộng thành quy trình xử lý sự cố chính thức.

## 14. Realistic Usage Example
### Tình huống thực tế:
Sau khi phát hành phiên bản mới, kênh hỗ trợ nhận về hơn 200 lượt phàn nàn của người dùng về việc 'không thanh toán được'. Sử dụng `dex-feedback-triage`, kỹ sư trực triage gom 200 ticket về 1 sự cố duy nhất (Deduplication), phân tích log đính kèm và phát hiện lỗi do thư viện cổng thanh toán vừa cập nhật chặn các thiết bị đã jailbreak/root. Kỹ sư gắn nhãn P0, chuyển thẳng cho Backend Team xử lý cấu hình server trong 30 phút, đồng thời tự động gửi email thông báo bản vá cho toàn bộ 200 khách hàng.
