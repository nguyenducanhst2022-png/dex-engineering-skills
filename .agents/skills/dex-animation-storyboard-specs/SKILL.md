---
name: dex-animation-storyboard-specs
description: Specify, storyboard, and engineer performant UI motion choreography with strict respects for prefers-reduced-motion media queries and 60fps compositor limits. Use when designing cohesive micro-interactions and transitions.
---

# dex-animation-storyboard-specs

## 1. Purpose & Scope
Đặc tả, vẽ kịch bản (storyboard) và lập trình các hiệu ứng chuyển động (motion choreography) mượt mà 60fps; bảo đảm hiệu năng tối ưu trên GPU compositor và tuân thủ nghiêm ngặt cài đặt giảm chuyển động `prefers-reduced-motion` của người dùng.

## 2. When to Use
- Khi thiết kế chuỗi chuyển động phức tạp (như mở modal, chuyển tiếp trang, hoặc các vi tương tác phản hồi thao tác).
- Khi các hiệu ứng hoạt họa gây giật lag (frame drops) hoặc gây chóng mặt, buồn nôn cho người dùng có chứng rối loạn tiền đình.
- Khi cần đồng nhất ngôn ngữ chuyển động (timing curves, duration) giữa bản thiết kế Figma và mã nguồn thực tế.

## 3. When NOT to Use
- Khi xây dựng giao diện tài liệu tĩnh thuần túy không có yếu tố tương tác động.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Bảng thông số chuyển động (Duration, Easing curve, Delay), thiết bị thử nghiệm đo lường FPS.
- **Quyền hạn truy cập:** Quyền sửa đổi CSS animations và motion scripts.

## 5. Core Concepts & Taxonomy
- **Compositor-Only Properties:** Chỉ hoạt họa hóa các thuộc tính `transform` và `opacity` để trình duyệt thực thi trên GPU mà không kích hoạt Layout và Paint.
- **Choreography Timing Tokens:** Sử dụng các token thời gian chuẩn hóa: Micro (100-150ms), Macro (200-300ms), Complex (400-500ms).
- **WCAG 2.3.3 Animation from Interactions:** Tôn trọng truy vấn `prefers-reduced-motion: reduce` bằng cách vô hiệu hóa hoặc thay thế chuyển động dịch chuyển bằng hiệu ứng fade đơn giản.

## 6. Step-by-Step Execution Workflow
1. Xây dựng kịch bản chuyển cảnh (Storyboard) chi tiết cho từng giai đoạn: Enter, Active, Exit.
2. Lựa chọn đường cong chuyển động (Easing Bézier) phù hợp với tính chất vật lý của thương hiệu.
3. Viết mã CSS hoặc Framer Motion chỉ sử dụng `transform` và `opacity`.
4. Bổ sung truy vấn `@media (prefers-reduced-motion: reduce)` để tắt hoàn toàn các chuyển động di chuyển lớn.
5. Đo lường hiệu năng chuyển động bằng Chrome DevTools Rendering Panel, bảo đảm đạt 60fps ổn định.
6. Xuất mã token chuyển động vào hệ thống Design Token dùng chung.

## 7. Concrete Examples
### Khai báo Animation mượt mà và tôn trọng cài đặt giảm chuyển động:
```css
/* Đường cong chuyển dịch tiêu chuẩn */
:root {
  --motion-duration-enter: 250ms;
  --motion-ease-out: cubic-bezier(0.16, 1, 0.3, 1);
}

.modal-dialog {
  opacity: 1;
  transform: translateY(0) scale(1);
  transition: opacity var(--motion-duration-enter) ease-out,
              transform var(--motion-duration-enter) var(--motion-ease-out);
  will-change: transform, opacity;
}

/* Vô hiệu hóa chuyển động cho người dùng nhạy cảm tiền đình */
@media (prefers-reduced-motion: reduce) {
  .modal-dialog {
    transition: opacity 150ms ease-in-out !important;
    transform: none !important;
  }
}
```

## 8. Anti-Patterns & Common Traps
- **Animating Layout Triggers:** Hoạt họa hóa các thuộc tính `top`, `left`, `width`, `height`, `margin` khiến CPU liên tục tính toán lại layout (Reflow) gây giật màn hình.
- **Ignoring Reduced Motion:** Không hỗ trợ `prefers-reduced-motion` gây khó chịu nghiêm trọng cho người dùng mắc chứng nhạy cảm chuyển động.
- **Endless Uncontrolled Spinners:** Để các hiệu ứng xoay tròn hoạt động liên tục trong nền làm hao pin thiết bị di động.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Tốc độ khung hình duy trì ổn định 60fps trong suốt quá trình thực thi hiệu ứng.
- **QG-03**: 100% hiệu ứng chuyển động đều bị tắt hoặc chuyển sang fade-in khi kích hoạt `prefers-reduced-motion: reduce`.
- **QG-05**: Không có thuộc tính gây Layout hoặc Paint nào bị đưa vào danh sách transition.

## 10. Security & Safety Boundaries
- Tránh các hiệu ứng nhấp nháy vượt quá 3 lần/giây để ngăn ngừa nguy cơ co giật do nhạy cảm ánh sáng (Photosensitive Seizures - WCAG 2.3.1).

## 11. Platform Adapters
- **Libraries**: Framer Motion, GSAP, Web Animations API (WAAPI), CSS Animations.

## 12. Deliverables & Output Artifacts
- Bảng đặc tả Storyboard và Motion Tokens.
- Module CSS/TS Animation hiệu năng cao.
- Báo cáo kiểm thử FPS và tuân thủ WCAG Motion.

## 13. Related & Complementary Skills
dex-web-animation-performance, dex-component-state-matrix, dex-perceived-performance-patterns

## 14. Realistic Usage Example
```powershell
# Kiểm tra hỗ trợ prefers-reduced-motion tự động bằng Playwright
npx playwright test tests/a11y/reduced-motion.spec.ts

# Ghi lại dấu vết hiệu năng chuyển động bằng Chrome Trace
npx lighthouse http://localhost:3000 --only-categories=performance
```
