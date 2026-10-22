---
name: dex-ui-visual-qa-review
description: Conduct rigorous visual quality assurance (Visual QA) reviews against production builds, verifying pixel alignment, spacing token adherence, font rendering, and edge-case states. Use prior to release sign-off, after major frontend refactors, or during design handoff verification.
---

# dex-ui-visual-qa-review

## 1. Purpose & Scope
Thực hiện quy trình kiểm thử chất lượng trực quan (Visual QA Review) nghiêm ngặt trên bản dựng môi trường thực tế; xác minh sự trùng khớp so với bản thiết kế Figma, tính đồng bộ của khoảng cách (spacing tokens), độ mượt mà khi hiển thị phông chữ và các trạng thái biên (edge cases).

## 2. When to Use
- Trước khi ký biên bản phát hành (Release Sign-off) cho các tính năng frontend lớn.
- Sau các đợt tái cấu trúc mã nguồn CSS hoặc nâng cấp thư viện UI component.
- Khi kiểm tra sự đồng nhất hiển thị giữa các hệ điều hành và trình duyệt khác nhau.

## 3. When NOT to Use
- Khi kiểm thử logic nghiệp vụ backend hoặc API integration.
- Khi mã nguồn frontend còn đang trong quá trình lập trình dở dang chưa hoàn thiện giao diện.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** File thiết kế Figma đã duyệt, đường dẫn môi trường Staging/Preview, danh sách các trạng thái dữ liệu (Empty, Loading, Error, Full).
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn trong phạm vi dự án, không can thiệp vào tài nguyên sản xuất khi chưa có phê duyệt.

## 5. Core Concepts & Taxonomy
- **Pixel-Precision Overlay:** So khớp ảnh chụp màn hình thực tế với bản thiết kế bằng kỹ thuật lớp phủ bán trong suốt (semi-transparent overlay).
- **Token Compliance Check:** Kiểm tra xem các giá trị padding, margin, font-size có lấy từ Design Tokens hay dùng giá trị tùy tiện (arbitrary values).
- **State Completeness:** Kiểm tra đầy đủ 5 trạng thái giao diện: Default, Hover, Focus, Active, Disabled.

## 6. Step-by-Step Execution Workflow
1. Chụp ảnh màn hình các component chính trên môi trường chạy thử nghiệm.
2. Đặt lớp phủ so sánh với thiết kế gốc để phát hiện sai lệch vị trí hoặc kích thước.
3. Kiểm tra việc sử dụng biến CSS token thay vì hardcode giá trị pixel.
4. Kích hoạt các trạng thái biên: văn bản cực dài gây tràn dòng, danh sách rỗng, lỗi mất mạng.
5. Lập biên bản Visual QA Report ghi nhận danh sách các lỗi lệch pixel kèm ảnh chụp minh họa.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```markdown
<!-- Visual QA Defect Log -->
### VQA-01: Header Spacing Mismatch
- **Component**: TopNavigationBar
- **Expected**: Padding 16px (var(--space-4))
- **Actual**: Padding 22px (hardcoded inline style)
- **Severity**: Minor
- **Remediation**: Thay thế class inline bằng `p-4` chuẩn Design Token.
```

## 8. Anti-Patterns & Common Traps
- Chỉ kiểm tra giao diện khi có dữ liệu đẹp lý tưởng mà không test trường hợp dữ liệu rỗng hoặc chữ quá dài.
- Bỏ qua kiểm tra trên màn hình Retina/High-DPI khiến hình ảnh bị mờ hoặc vỡ nét.
- Duyệt phát hành vội vàng mà không chụp ảnh bằng chứng so khớp.

## 9. Quality Gates & Acceptance Criteria
- QG-01: 100% các thành phần UI tuân thủ bảng mã Spacing Token quy định.
- QG-02: Sai lệch vị trí so với thiết kế Figma không vượt quá 2px cho các phần tử căn chỉnh.
- QG-03: Không có hiện tượng vỡ layout khi văn bản dài gấp đôi mức trung bình.

## 10. Security & Safety Boundaries
- Đảm bảo các trạng thái hiển thị thông tin người dùng nhạy cảm (như số thẻ tín dụng) luôn được che giấu đúng quy cách trên giao diện.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Biên bản nghiệm thu chất lượng hình ảnh `VISUAL_QA_REPORT.md`.
1. Bộ ảnh chụp so khớp trước và sau khi khắc phục lỗi lệch pixel.

## 13. Related & Complementary Skills
- [`dex-visual-regression`](.agents/skills/dex-visual-regression/SKILL.md)
- [`dex-design-handoff-verification`](.agents/skills/dex-design-handoff-verification/SKILL.md)
- [`dex-ux-accessibility`](.agents/skills/dex-ux-accessibility/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Kiểm tra phiên bản cập nhật trang thanh toán trước ngày Black Friday. Kỹ sư kích hoạt `dex-ui-visual-qa-review`, phát hiện 3 lỗi lệch spacing ở nút thanh toán trên Safari iOS và 1 lỗi tràn chữ khi tên người dùng dài hơn 40 ký tự, kịp thời vá lỗi trước giờ mở bán.
