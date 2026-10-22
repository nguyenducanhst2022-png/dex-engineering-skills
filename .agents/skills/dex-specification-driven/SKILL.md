---
name: dex-specification-driven
description: Specification-Driven Development (SDD) methodology. Authors formal functional specifications, concrete acceptance criteria, edge-case matrices, and end-to-end traceability before coding starts. Eliminates requirements ambiguity. Use when starting new features, defining requirements, or establishing acceptance criteria.
---

# DEX Specification-Driven Development

## 1. Purpose & Scope
Áp dụng phương pháp phát triển hướng đặc tả (Specification-Driven Development - SDD); bắt buộc phải viết và thống nhất tài liệu đặc tả kỹ thuật cùng các tiêu chí nghiệm thu rõ ràng trước khi AI bắt tay vào viết code, giúp triệt tiêu hoàn toàn sự hiểu sai yêu cầu và giảm tối đa số lần phải đập đi sửa lại.

Quy trình SDD chuẩn:
`Phân tích yêu cầu → Viết đặc tả → Xác định tiêu chí nghiệm thu → Chia nhiệm vụ → Viết code → Kiểm thử → Đối chiếu đặc tả → Sửa lỗi → Ổn định → Lưu Git`

Nguyên tắc cốt lõi: **AI phải hiểu chính xác CẦN LÀM GÌ, LÀM NHƯ THẾ NÀO và KHI NÀO ĐƯỢC COI LÀ HOÀN THÀNH trước khi viết bất kỳ dòng mã nguồn nào.**
Ghi nhớ sống còn: **Đặc tả rõ → AI hiểu đúng → Code đúng mục tiêu → Kiểm thử được → Ít phải sửa lại.**

## 2. When to Use
- Trước khi bắt đầu bất kỳ tính năng (Feature) mới nào.
- Khi người dùng đưa ra một yêu cầu chung chung, mơ hồ (ví dụ: "Hãy làm cho tôi chức năng thanh toán").
- Khi thay đổi các luồng nghiệp vụ quan trọng hoặc cập nhật logic cốt lõi.
- Khi cần tạo ma trận truy vết (Traceability Matrix) giữa yêu cầu và các bài kiểm thử.

## 3. When NOT to Use
- Sửa một lỗi chính tả nhỏ hoặc sửa cú pháp 1 dòng hiển nhiên.
- Các tác vụ khám phá thử nghiệm (Spike / PoC) dùng để đánh giá công nghệ trong vài phút.

## 4. Prerequisites & Input Context
- Yêu cầu ban đầu từ người dùng hoặc Product Owner.
- Các ràng buộc về hệ thống và luồng dữ liệu hiện có.
- Mẫu tài liệu đặc tả chuẩn tại [spec-template.md](references/spec-template.md).

## 5. Core Concepts & Taxonomy
- **Nguyên tắc cốt lõi**: Tuân thủ triệt để nguyên lý vận hành xác định và ranh giới trách nhiệm của chuẩn Agent Skills.
- **Tính nhất quán hệ thống**: Mọi thao tác phải có thể kiểm chứng độc lập với kết quả đo lường rõ ràng.
- **Ngăn ngừa hồi quy**: Bất kỳ sửa đổi nào cũng phải bảo vệ tính tương thích ngược và chất lượng đã được nghiệm thu.

## 6. Step-by-Step Execution Workflow
### Bước 1: Phân Tích & Làm Rõ Yêu Cầu (Requirements Clarification)
- Đặt câu hỏi làm rõ các điểm mơ hồ trước khi viết tài liệu:
  - Ai là người sử dụng tính năng này?
  - Dữ liệu đầu vào gồm những trường nào, kiểu dữ liệu gì?
  - Kết quả trả về mong muốn là gì?
  - Khi có lỗi xảy ra thì hệ thống ứng xử như thế nào?

### Bước 2: Soạn Thảo Bản Đặc Tả Kỹ Thuật (Technical Specification)
- Tạo file `SPEC.md` (hoặc `docs/specs/feature-name.md`) theo mẫu chuẩn:
  - **Mục tiêu tính năng (Objective)**: Giá trị mang lại cho người dùng.
  - **Mô tả hành vi (Behavior Specification)**: Luồng hoạt động chi tiết từng bước.
  - **Cấu trúc dữ liệu & Interface (Data Schema & API Contract)**: Kiểu dữ liệu, format JSON.

### Bước 3: Xác Định Tiêu Chí Nghiệm Thu Cụ Thể (Concrete Acceptance Criteria)
- Viết các tiêu chí nghiệm thu không thể chối cãi theo định dạng **Given - When - Then**:
  - *Given*: Khi người dùng đã đăng nhập và giỏ hàng có 2 sản phẩm...
  - *When*: Người dùng bấm nút "Thanh toán"...
  - *Then*: Đơn hàng mới được tạo ở trạng thái `PENDING` và chuyển hướng đến trang Stripe...

### Bước 4: Lập Ma Trận Trường Hợp Biên & Lỗi (Edge Cases & Failure Matrix)
- Liệt kê tường minh cách xử lý:
  - Người dùng nhập chuỗi rỗng / số âm / vượt quá giới hạn.
  - Mất kết nối mạng hoặc timeout dịch vụ ngoài.
  - Hành động trùng lặp (Double-click / Idempotency).

### Bước 5: Phân Rã Thành Các Task Kỹ Thuật (Task Breakdown with Traceability)
- Chia đặc tả thành các công việc nhỏ, mỗi công việc liên kết trực tiếp với một tiêu chí nghiệm thu cụ thể (Traceability).

### Bước 6: Lập Trình & Đối Chiếu Nghiệm Thu (Implementation & Verification)
- Viết code và viết test tương ứng với từng tiêu chí nghiệm thu.
- Đối chiếu từng mục: Đạt → Đánh dấu hoàn thành. Chưa đạt → Bổ sung code cho đến khi khớp 100% với đặc tả.

## 7. Concrete Examples
```bash
# Lệnh thực thi & kiểm chứng tiêu chuẩn
dex verify --skill dex-specification-driven
```

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước xác minh tự động và dựa vào giả định chủ quan.
- **Anti-Pattern 2**: Thay đổi diện rộng vượt ngoài phạm vi (Scope Creep) làm mất kiểm soát rủi ro.
- **Trap**: Thực hiện thao tác phá hủy hoặc thay đổi trạng thái sản xuất khi chưa qua cổng kiểm duyệt an toàn.

## 9. Quality Gates & Acceptance Criteria
- **QG-01 (Scope Defined in Spec)**: Bản đặc tả nêu rõ các file và endpoint sẽ được tạo hoặc sửa.
- **QG-02 (Spec Compliance)**: 100% các tiêu chí nghiệm thu trong `SPEC.md` đều có bài test tương ứng kiểm chứng.
- **QG-10 (Traceability Verified)**: Có bảng ma trận chứng minh mỗi yêu cầu đều được kiểm thử thành công.

## 10. Security & Safety Boundaries
1. **Spec First (Đặc tả đi trước code)**: Tuyệt đối không viết code khi chưa có bản đặc tả kỹ thuật và tiêu chí nghiệm thu được thống nhất.
2. **Clear Requirements (Yêu cầu rõ ràng, không mơ hồ)**: Loại bỏ các từ ngữ chung chung như "nhanh chóng", "đẹp mắt", "tối ưu"; thay bằng số liệu và hành vi đo đếm được.
3. **Acceptance Criteria (Mỗi chức năng có tiêu chí nghiệm thu)**: Bắt buộc phải có điều kiện cụ thể để biết khi nào được coi là xong.
4. **Traceability (Khả năng truy vết)**: Mỗi dòng code và bài test phải liên kết được với một yêu cầu cụ thể trong đặc tả.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Kích hoạt thông qua terminal hoặc tiện ích mở rộng IDE tương thích (VS Code, Cursor, Windsurf).

## 12. Deliverables & Output Artifacts
1. File đặc tả kỹ thuật `SPEC.md` hoàn chỉnh.
2. Bộ tiêu chí nghiệm thu chi tiết (Acceptance Criteria checklist).
3. Bộ bài kiểm thử tự động phản ánh trực tiếp các tiêu chí trong đặc tả.

## 13. Related & Complementary Skills
- `dex-master-orchestrator`: Điều phối trung tâm.

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Kỹ sư hoặc AI Agent kích hoạt **dex-specification-driven** trong dự án.
1. Tiếp nhận ngữ cảnh đầu vào và kiểm tra điều kiện tiên quyết tại Mục 4.
2. Vận hành tuần tự các bước theo Quy trình tại Mục 6.
3. Kiểm chứng đầu ra đối chiếu với Tiêu chuẩn chấp thuận tại Mục 9.
4. Bàn giao đầy đủ hiện vật theo Mục 12 và cập nhật tài liệu liên quan.
