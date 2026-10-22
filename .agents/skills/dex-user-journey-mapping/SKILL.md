---
name: dex-user-journey-mapping
description: Map, analyze, and optimize end-to-end user journeys, friction points, drop-off phases, and emotional arcs to align engineering delivery with user experience. Use when designing new product features or overhauling user flows.
---

# dex-user-journey-mapping

## 1. Purpose & Scope
Thiết kế, phân tích và tối ưu hóa bản đồ hành trình người dùng toàn trình (User Journey Mapping); nhận diện các điểm ma sát (Friction Points), các giai đoạn bỏ cuộc (Drop-off Phases), cung bậc cảm xúc của người dùng và chuyển hóa các phát hiện trải nghiệm thành các tiêu chí nghiệm thu kỹ thuật (Acceptance Criteria) chuẩn xác cho đội ngũ phát triển phần mềm.

## 2. When to Use
- Khởi động xây dựng một sản phẩm mới hoặc tái thiết kế một luồng nghiệp vụ cốt lõi (Onboarding, Thanh toán, Đổi mật khẩu).
- Tỉ lệ người dùng hoàn thành quy trình quá thấp dù hệ thống kỹ thuật không hề báo lỗi.
- Đội ngũ kỹ sư chỉ tập trung vào chức năng (features) mà mất đi góc nhìn tổng thể về trải nghiệm thực tế của người dùng.

## 3. When NOT to Use
- Không lập bản đồ hành trình dựa trên trí tưởng tượng thuần túy mà không có dữ liệu phỏng vấn người dùng hoặc số liệu phân tích hành vi.
- Không dùng cho các quy trình kỹ thuật ngầm hoàn toàn không có sự tham gia của con người.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Dữ liệu phỏng vấn người dùng thực tế (User Interviews) và khảo sát.
- Số liệu phân tích hành vi người dùng (Amplitude, Mixpanel, Google Analytics).
- Chân dung người dùng mục tiêu (User Personas) và mục tiêu nghiệp vụ.
- **Điều kiện tiên quyết**:
- Có sự tham gia đồng thuận giữa Product Manager, UX Designer và Lead Engineer.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- 5 Giai đoạn cốt lõi của hành trình: Nhận biết (Awareness) -> Khám phá (Consideration) -> Mua hàng/Kích hoạt (Activation) -> Sử dụng thường xuyên (Retention) -> Giới thiệu (Advocacy).
- Friction vs Value Exchange: Người dùng sẵn sàng bỏ công sức nếu giá trị nhận lại tương xứng. Bất kỳ bước nhập liệu nào không mang lại giá trị tức thì cho người dùng đều là điểm ma sát cần loại bỏ.
- 'Happy Path' vs Edge Journeys: Luồng lý tưởng người dùng đi suôn sẻ vs các luồng sự cố (mất mạng, thẻ hết tiền, quên mật khẩu).
- **Quy tắc quyết định kỹ thuật**:
- Bất kỳ quy trình quan trọng nào có hơn 4 bước trên mobile phải tìm cách rút ngắn xuống tối đa 3 bước.
- Mọi điểm ma sát mức độ Nghiêm trọng (Critical Friction) phải được chuyển thành User Story sửa lỗi trong sprint tiếp theo.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Thiết kế hành trình quá phức tạp bắt người dùng đăng ký tài khoản và xác minh email trước khi cho họ xem thử tính năng sản phẩm, khiến 70% người dùng thoát ứng dụng ngay từ màn hình đầu tiên.

## 6. Step-by-Step Execution Workflow
1. Xác định chân dung người dùng cụ thể và mục tiêu họ cần đạt được.
2. Liệt kê tuần tự từng hành động của người dùng từ lúc bắt đầu đến khi kết thúc.
3. Ghi nhận cảm xúc (Vui vẻ, Trung tính, Bực bội) và suy nghĩ của người dùng tại từng bước.
4. Xác định các điểm ma sát kỹ thuật (thời gian tải trang chậm, form nhập quá dài, thông báo lỗi tối nghĩa).
5. Đề xuất các giải pháp kỹ thuật cụ thể và chuyển đổi thành Product Requirements.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```markdown
# User Journey: Thanh toán mua hàng lần đầu trên Mobile
**Persona:** Lan, 28 tuổi, nhân viên văn phòng, mua sắm trên xe buýt.

| Giai đoạn | Hành động người dùng | Cảm xúc | Điểm ma sát kỹ thuật | Cơ hội tối ưu hóa (Engineering) |
| :--- | :--- | :--- | :--- | :--- |
| 1. Xem giỏ hàng | Bấm nút 'Thanh toán' | Hào hứng | Nút tải mất 3.5 giây | Tối ưu hóa bundle và nạp giỏ hàng từ LocalStorage |
| 2. Nhập địa chỉ | Phải gõ tay 6 trường thông tin | Bực bội | Bàn phím che mất nút Tiếp tục | Tự động điền địa chỉ qua GPS / Google Places API |
| 3. Chọn phương thức | Tìm thanh toán Apple Pay | Hài lòng | Apple Pay hiển thị mượt mà | Tích hợp Apple Pay / Google Pay 1-click checkout |
| 4. Xác nhận | Nhận email hóa đơn | An tâm | Không rõ khi nào nhận hàng | Hiển thị mã tracking đơn hàng thời gian thực trên màn hình |
```

### Lệnh xác minh & thực thi:
```bash
# Đánh giá độ dài và số lượng thao tác người dùng bằng Playwright Trace
npx playwright test tests/journeys/checkout-journey.spec.ts --trace on
```

## 8. Anti-Patterns & Common Traps
- Giả định mọi người dùng đều hiểu các thuật ngữ kỹ thuật viết tắt trong sản phẩm.
- Chỉ thiết kế hành trình cho máy tính để bàn (Desktop) trong khi 85% người dùng thực tế sử dụng điện thoại di động.

## 9. Quality Gates & Acceptance Criteria
- Giảm số lượng thao tác (Clicks/Taps) để hoàn thành quy trình chính tối thiểu 30%.
- 100% các điểm ma sát nghiêm trọng có ticket xử lý kỹ thuật tương ứng.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Quá trình thu thập thông tin người dùng trong bản đồ hành trình phải tuân thủ quyền riêng tư, không lưu trữ thông tin nhận dạng cá nhân.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ sinh thái AI / UX**: Hỗ trợ Model Context Protocol (MCP), LangChain/LlamaIndex, Figma, Playwright axe-core.

## 12. Deliverables & Output Artifacts
- Bản đồ hành trình người dùng toàn diện (User Journey Map Diagram/Document).
- Danh sách các User Stories cải tiến kỹ thuật theo thứ tự ưu tiên ROI.

## 13. Related & Complementary Skills
dex-information-architecture, dex-product-requirements-writing, dex-conversion-funnel-analysis

## 14. Realistic Usage Example
### Tình huống thực tế:
Một ứng dụng ngân hàng số có tỉ lệ mở sổ tiết kiệm online rất thấp. Sau khi lập bản đồ hành trình người dùng, nhóm phát hiện người dùng bị hoang mang ở bước 'Chọn tài khoản trích nợ' vì hệ thống hiển thị số tài khoản 16 chữ số thay vì hiển thị số dư khả dụng. Đổi sang hiển thị 'Tài khoản chi tiêu (Số dư: 15,000,000đ)' đã giúp tỉ lệ hoàn tất mở sổ tiết kiệm tăng vọt 42% trong 2 tuần.
