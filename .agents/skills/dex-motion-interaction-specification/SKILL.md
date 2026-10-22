---
name: dex-motion-interaction-specification
description: Specify purposeful UI motion choreographies, spring physics curves, transition durations, and strict prefers-reduced-motion accessibility fallbacks. Use when authoring design tokens for animation, adding micro-interactions, or engineering page transitions.
---

# dex-motion-interaction-specification

## 1. Purpose & Scope
Đặc tả các chuyển động tương tác (UI Motion & Micro-interactions) có mục đích rõ ràng, dựa trên vật lý đàn hồi (spring physics) và đường cong gia tốc tự nhiên; thiết lập các khoảng thời gian chuyển tiếp tối ưu và cơ chế an toàn cho người dùng mẫn cảm tiền đình (`prefers-reduced-motion`).

## 2. When to Use
- Khi thêm hiệu ứng chuyển cảnh trang (page transition) hoặc mở modal dialog.
- Khi đặc tả chuyển động cho các nút bấm, menu thả xuống và thanh thông báo toast.
- Khi cần đồng bộ ngôn ngữ chuyển động (Motion Tokens) giữa Figma và mã nguồn frontend.

## 3. When NOT to Use
- Khi tạo các animation trang trí lặp đi lặp lại vô tận gây mất tập trung người dùng.
- Khi tối ưu hiệu năng tính toán dữ liệu của backend.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Danh sách các tương tác UI cần hiệu ứng, thời gian thực thi mong muốn, thư viện animation mục tiêu (CSS, Framer Motion, GSAP).
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn trong phạm vi dự án, không can thiệp vào tài nguyên sản xuất khi chưa có phê duyệt.

## 5. Core Concepts & Taxonomy
- **Choreography & Staggering:** Trình tự xuất hiện có thứ bậc giữa các phần tử liên quan (ví dụ các item trong danh sách xuất hiện cách nhau 50ms).
- **Physics-Based Easing:** Sử dụng cubic-bezier tự nhiên (Deceleration curve cho phần tử vào, Acceleration cho phần tử ra).
- **Vestibular Safety:** Tôn trọng hoàn toàn truy vấn `@media (prefers-reduced-motion: reduce)` bằng cách chuyển chuyển động trượt sang mờ dần (fade).

## 6. Step-by-Step Execution Workflow
1. Phân loại các dạng chuyển động: Micro-interaction (<200ms), Context Transition (200-400ms), Expressive (>400ms).
2. Xác định đường cong chuyển động chuẩn: `--ease-out-back`, `--ease-in-out-smooth`.
3. Triển khai quy tắc CSS hoặc hook React có xử lý `prefers-reduced-motion`.
4. Kiểm tra hiệu năng animation đạt chuẩn 60fps/120fps bằng Chrome DevTools Performance panel.
5. Đóng gói thành bộ token `motion.tokens.json`.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```css
/* Motion Tokens with Vestibular Safety */
:root {
  --motion-duration-fast: 150ms;
  --motion-duration-normal: 250ms;
  --motion-ease-out: cubic-bezier(0.16, 1, 0.3, 1);
}

.modal-sheet {
  transition: transform var(--motion-duration-normal) var(--motion-ease-out),
              opacity var(--motion-duration-fast) linear;
}

@media (prefers-reduced-motion: reduce) {
  .modal-sheet {
    transition: opacity var(--motion-duration-fast) linear;
    transform: none !important;
  }
}
```

## 8. Anti-Patterns & Common Traps
- Lạm dụng animation dài hơn 500ms cho các tác vụ thường ngày khiến người dùng cảm thấy hệ thống chậm chạp.
- Animate các thuộc tính kích hoạt Layout Thrashing như `left`, `top`, `width`, `height` thay vì dùng `transform` và `opacity`.
- Bỏ qua truy vấn `prefers-reduced-motion` khiến người dùng bị chóng mặt hoặc buồn nôn khi sử dụng.

## 9. Quality Gates & Acceptance Criteria
- QG-01: 100% animation chỉ tác động lên thuộc tính `transform` và `opacity`.
- QG-02: Có kiểm thử tự động xác nhận hiệu ứng trượt bị vô hiệu hóa khi bật `prefers-reduced-motion`.
- QG-03: Tốc độ khung hình duy trì ổn định không rớt dưới 58fps trong suốt quá trình chuyển động.

## 10. Security & Safety Boundaries
- Không chèn mã JavaScript độc hại thông qua các trình phân tích SVG animation hoặc lặp lại vô hạn gây nghẽn CPU (Denial of Service).
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Bộ Motion Tokens chuẩn `motion.tokens.json`.
1. Bộ quy tắc CSS chuyển động an toàn trợ năng.

## 13. Related & Complementary Skills
- [`dex-web-animation-performance`](.agents/skills/dex-web-animation-performance/SKILL.md)
- [`dex-ux-accessibility`](.agents/skills/dex-ux-accessibility/SKILL.md)
- [`dex-ui-component-contracts`](.agents/skills/dex-ui-component-contracts/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Thiết kế tương tác mở ngăn kéo sidebar cho ứng dụng SaaS. Áp dụng `dex-motion-interaction-specification` để tạo đường cong trượt gia tốc 250ms tự nhiên và tự động chuyển sang hiệu ứng mờ dần nhẹ nhàng 100ms khi người dùng kích hoạt cài đặt giảm chuyển động trên hệ điều hành.
