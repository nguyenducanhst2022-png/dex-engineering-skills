---
name: dex-web-animation-performance
description: Profile and optimize 60fps web animation performance, eliminating layout thrashing, forced synchronous layouts, and excessive composite layers using GPU transforms and Will-Change budgets. Use when diagnosing UI jank, dropped frames, or heavy scroll animations.
---

# dex-web-animation-performance

## 1. Purpose & Scope
Đo lường, lập hồ sơ hiệu năng (Profiling) và tối ưu hóa chuyển động web đạt chuẩn mượt mà 60fps/120fps; triệt tiêu hiện tượng giật hình (UI Jank), hiện tượng tính toán lại layout cưỡng bức (Forced Synchronous Layout / Layout Thrashing) và quản trị bộ nhớ GPU composite layers.

## 2. When to Use
- Khi các hiệu ứng cuộn trang (scroll-driven animations) hoặc chuyển cảnh bị giật cục, rớt khung hình.
- Khi quạt tản nhiệt của máy tính người dùng kêu to bất thường khi lướt web do ngốn CPU.
- Trước khi triển khai các hiệu ứng thị giác phức tạp trên thiết bị di động cấu hình trung bình.

## 3. When NOT to Use
- Khi animation chỉ là một hiệu ứng mờ dần (fade-in) đơn giản kéo dài 100ms trên một button duy nhất.
- Khi kiểm tra hiệu năng truy vấn API dưới backend.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Chrome DevTools Performance trace file, mã nguồn CSS/JS của animation, danh sách các thiết bị mục tiêu.
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn trong phạm vi dự án, không can thiệp vào tài nguyên sản xuất khi chưa có phê duyệt.

## 5. Core Concepts & Taxonomy
- **Pixel Pipeline:** JS -> Style -> Layout -> Paint -> Composite. Chỉ animate thuộc tính Composite (transform, opacity).
- **Layout Thrashing:** Đọc thuộc tính hình học (`offsetHeight`) rồi ghi thuộc tính kiểu dáng lặp đi lặp lại trong vòng lặp.
- **Will-Change Budget:** Khai báo `will-change: transform` có chọn lọc để đưa phần tử lên layer GPU riêng và thu hồi bộ nhớ sau khi hoàn tất.

## 6. Step-by-Step Execution Workflow
1. Ghi lại trace hiệu năng 5 giây bằng Chrome DevTools Performance tab khi đang chạy animation.
2. Xác định các khung hình màu đỏ (Dropped Frames / Long Tasks) và kiểm tra nguyên nhân (Layout, Recalculate Style hay Paint).
3. Thay thế toàn bộ các thuộc tính gây layout (`top`, `left`, `margin`) bằng `transform: translate3d()`.
4. Đảm bảo các tác vụ đọc DOM được gom cụm trước các tác vụ ghi DOM (sử dụng `requestAnimationFrame`).
5. Xác nhận lại khung hình đạt 60fps ổn định trên cấu hình CPU bị giảm tốc độ 4x (4x CPU Throttling).

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```javascript
// Eliminating Layout Thrashing via RequestAnimationFrame
function animateCards(cards) {
  // 1. Batch Read Phase
  const heights = cards.map(c => c.getBoundingClientRect().height);
  
  // 2. Batch Write Phase inside RAF
  requestAnimationFrame(() => {
    cards.forEach((card, i) => {
      card.style.transform = `translate3d(0, ${heights[i]}px, 0)`;
    });
  });
}
```

## 8. Anti-Patterns & Common Traps
- Gán `will-change: transform` lên hàng trăm phần tử cùng lúc gây cạn kiệt VRAM bộ nhớ đồ họa.
- Đọc `element.scrollTop` ngay giữa vòng lặp cập nhật vị trí khiến trình duyệt phải tính toán lại toàn bộ trang liên tục.
- Dùng `setInterval` hoặc `setTimeout` để làm animation thay vì `requestAnimationFrame`.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Không có sự kiện 'Layout' hoặc 'Paint' xuất hiện trong suốt quá trình chạy vòng lặp animation.
- QG-02: Tỷ lệ khung hình duy trì >= 58fps trên thiết bị mô phỏng 4x CPU Throttling.
- QG-03: Bộ nhớ GPU layer được giải phóng hoàn toàn sau khi animation kết thúc.

## 10. Security & Safety Boundaries
- Không cho phép mã người dùng chèn các kịch bản animation vô tận tiêu thụ 100% CPU trên trình duyệt client.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Bản phân tích Performance Profile trước và sau khi tối ưu.
1. Mã nguồn animation CSS/JS đã được chuyển đổi sang chuẩn GPU Composite.

## 13. Related & Complementary Skills
- [`dex-motion-interaction-specification`](.agents/skills/dex-motion-interaction-specification/SKILL.md)
- [`dex-frontend-performance`](.agents/skills/dex-frontend-performance/SKILL.md)
- [`dex-ui-visual-qa-review`](.agents/skills/dex-ui-visual-qa-review/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Trang giới thiệu sản phẩm mới bị giật mạnh khi người dùng cuộn chuột qua danh sách thẻ 3D. Sử dụng `dex-web-animation-performance` để phân tích trace, phát hiện hiệu ứng đang animate thuộc tính `top` và `box-shadow`, thay thế bằng `transform: translate3d` và đưa FPS từ 22fps lên thẳng 60fps mượt mà.
