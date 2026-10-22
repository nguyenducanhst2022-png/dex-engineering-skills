---
name: dex-product-requirements-writing
description: Author structured, unambiguous, engineering-ready Product Requirement Documents (PRDs) with clear problem statements, user stories, edge cases, and measurable success metrics. Use when defining new features or systems.
---

# dex-product-requirements-writing

## 1. Purpose & Scope
Soạn thảo tài liệu đặc tả yêu cầu sản phẩm chuẩn mực, rõ ràng và sẵn sàng cho đội ngũ kỹ thuật triển khai (Engineering-Ready PRDs); định nghĩa chính xác tuyên bố vấn đề (Problem Statement), các câu chuyện người dùng (User Stories), các trường hợp biên nguy hiểm (Edge Cases) và các chỉ số thành công đo lường được (Measurable Success Metrics / OKRs).

## 2. When to Use
- Chuẩn bị khởi động một sáng kiến sản phẩm hoặc tính năng kỹ thuật mới.
- Đội ngũ kỹ sư thường xuyên phải hỏi lại Product Manager vì tài liệu yêu cầu quá mơ hồ, thiếu chi tiết hoặc thiếu các trường hợp ngoại lệ.
- Cần sự đồng thuận rõ ràng giữa các bên liên quan (Kinh doanh, Vận hành, Thiết kế, Kỹ thuật) trước khi viết dòng code đầu tiên.

## 3. When NOT to Use
- Không viết những tài liệu PRD dài lê thê hàng trăm trang theo phong cách Thác nước (Waterfall) mà không ai đọc hết.
- Không can thiệp quá sâu vào giải pháp kỹ thuật chi tiết của kỹ sư (PRD tập trung vào 'Vấn đề là gì' và 'Tại sao cần giải quyết', để kỹ sư quyết định 'Giải quyết như thế nào').

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Mục tiêu kinh doanh và chỉ số KPI/OKR cần đạt được.
- Phản hồi từ khách hàng và dữ liệu nghiên cứu thị trường.
- Các ràng buộc về kỹ thuật và thời gian bàn giao.
- **Điều kiện tiên quyết**:
- Đã xác thực được vấn đề thực sự của người dùng thông qua nghiên cứu sơ bộ.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Cấu trúc PRD chuẩn mực:
  1. Tuyên bố vấn đề (Problem Statement): Khách hàng đang gặp khó khăn gì? Tại sao vấn đề này đáng giải quyết lúc này?
  2. Mục tiêu & Không thuộc phạm vi (Goals & Non-Goals): Định rõ những gì sẽ làm và dứt khoát những gì KHÔNG làm trong phiên bản này.
  3. User Stories & Acceptance Criteria: Theo chuẩn `Given... When... Then...`.
  4. Edge Cases: Mất mạng, dữ liệu trùng lặp, tài khoản bị khóa, số tiền âm.
  5. Chỉ số thành công (Success Metrics): Đo lường bằng con số cụ thể sau khi ra mắt.
- Non-Goals (Ngoài phạm vi): Phần quan trọng nhất của PRD giúp bảo vệ đội ngũ khỏi hiện tượng phình to phạm vi (Scope Creep).
- **Quy tắc quyết định kỹ thuật**:
- Mỗi User Story bắt buộc phải có tối thiểu 3 Acceptance Criteria cụ thể có thể kiểm thử tự động được.
- Nếu một tính năng không có chỉ số đo lường thành công rõ ràng: hoãn phê duyệt PRD cho đến khi xác định được cách đo.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Viết yêu cầu chung chung như 'Hệ thống phải chạy nhanh và giao diện đẹp', khiến lập trình viên và kiểm thử viên không có căn cứ để nghiệm thu.

## 6. Step-by-Step Execution Workflow
1. Phỏng vấn các bên liên quan và tổng hợp dữ liệu định lượng.
2. Soạn thảo bản nháp PRD theo mẫu khung cấu trúc chuẩn.
3. Tổ chức phiên rà soát kỹ thuật (Engineering Review) để kỹ sư phản biện và bổ sung các trường hợp biên.
4. Thống nhất danh sách Non-Goals và chốt phiên bản v1.0.
5. Chuyển giao các User Stories vào công cụ quản lý dự án (Jira/Linear).

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```markdown
# PRD: Tính năng Hủy Đơn Hàng Tự Động cho Người Mua
**Trạng thái:** Sẵn sàng phát triển | **Owner:** PM Checkout

### 1. Vấn đề cốt lõi:
Hiện tại người mua muốn hủy đơn hàng phải gọi tổng đài, tốn 5 phút và tốn $2 chi phí hỗ trợ cho mỗi cuộc gọi (3,000 cuộc/tháng).

### 2. Mục tiêu (Goals):
- Cho phép người mua tự hủy đơn hàng trong vòng 15 phút kể từ lúc đặt hàng nếu người bán chưa đóng gói.
- Giảm 60% số lượng cuộc gọi khiếu nại hủy đơn tới tổng đài.

### 3. Ngoài phạm vi (Non-Goals):
- Không hỗ trợ hủy đơn sau khi đơn vị vận chuyển đã lấy hàng.

### 4. User Story & Acceptance Criteria:
**Story:** Là người mua hàng, tôi muốn tự hủy đơn trong vòng 15 phút để đổi ý khi đặt nhầm.
- *Scenario 1 (Hủy thành công):*
  GIVEN đơn hàng ở trạng thái 'Chờ xác nhận' VÀ thời gian đặt < 15 phút
  WHEN người dùng bấm 'Hủy đơn' và chọn lý do
  THEN đơn hàng chuyển sang 'Đã hủy' VÀ tiền được tự động hoàn lại ví trong 30 giây.
- *Scenario 2 (Edge case - Đang hủy thì đơn hàng đổi trạng thái):*
  GIVEN người dùng đang mở popup hủy đơn
  WHEN người bán bấm 'Đã đóng gói' cùng lúc
  THEN hệ thống từ chối hủy VÀ hiển thị thông báo: 'Đơn hàng đã được đóng gói, vui lòng liên hệ shop'.
```

### Lệnh xác minh & thực thi:
```bash
# Rà soát tính đầy đủ của PRD bằng checklist kiểm toán yêu cầu
python scripts/audit_prd_readiness.py --file docs/prds/auto-cancel-order.md
```

## 8. Anti-Patterns & Common Traps
- Thay đổi yêu cầu liên tục giữa chừng khi kỹ sư đang trong giai đoạn lập trình (Mid-sprint scope changes).
- Bỏ qua các trường hợp biên (Edge cases) và đẩy trách nhiệm suy nghĩ logic cho lập trình viên.

## 9. Quality Gates & Acceptance Criteria
- 100% User Stories có Acceptance Criteria rõ ràng theo chuẩn Gherkin.
- Được phê duyệt bằng văn bản bởi Tech Lead và Design Lead trước khi bắt đầu Sprint.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Mọi yêu cầu liên quan đến lưu trữ hoặc xử lý dữ liệu người dùng phải có phần đánh giá tác động bảo mật (Security & Privacy Impact).
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ sinh thái AI / UX**: Hỗ trợ Model Context Protocol (MCP), LangChain/LlamaIndex, Figma, Playwright axe-core.

## 12. Deliverables & Output Artifacts
- Tài liệu PRD chuẩn mực trên Markdown / Notion / Confluence.
- Danh sách backlog User Stories đã được ước lượng độ phức tạp.

## 13. Related & Complementary Skills
dex-user-journey-mapping, dex-conversion-funnel-analysis, dex-supportability-engineering

## 14. Realistic Usage Example
### Tình huống thực tế:
Một dự án ví điện tử từng thất bại vì PRD cũ chỉ ghi 'Hỗ trợ chuyển tiền qua số điện thoại' mà không tính đến trường hợp số điện thoại chưa đăng ký ví hoặc người nhận đổi số. Sau khi áp dụng chuẩn PRD mới với đầy đủ Edge Cases và Non-Goals, đội ngũ đã phát triển tính năng chuyển tiền hoàn thành đúng hạn 100% mà không phát sinh bất kỳ lỗi logic nghiêm trọng nào.
