---
name: dex-fluid-typography-engineering
description: Implement mathematical fluid typography scales using CSS clamp(), responsive modular scales, dynamic optical sizing, and optimal line-height geometry. Use when establishing typography tokens, eliminating layout shifts from font loading, or optimizing reading comfort.
---

# dex-fluid-typography-engineering

## 1. Purpose & Scope
Hiện thực hóa hệ thống typography co giãn liên tục (Fluid Typography) dựa trên hàm toán học `clamp()`, modular scale tỷ lệ vàng, optical sizing động và tỷ lệ chiều cao dòng (line-height) tối ưu; loại bỏ hoàn toàn hiện tượng giật cục khi nhảy breakpoint màn hình.

## 2. When to Use
- Khi xây dựng typography tokens cho ứng dụng responsive đa màn hình.
- Khi muốn tiêu đề co giãn mượt mà theo kích thước viewport mà không cần viết hàng chục `@media` query rời rạc.
- Khi tối ưu trải nghiệm đọc cho các bài viết dạng dài (long-form editorial) hoặc tài liệu kỹ thuật.

## 3. When NOT to Use
- Cho các nhãn nhỏ trong bảng dữ liệu hoặc UI cố định không được phép co giãn.
- Khi các trình duyệt mục tiêu là trình duyệt nhúng cổ điển không hỗ trợ hàm toán học CSS `clamp()`.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Khoảng viewport tối thiểu và tối đa (ví dụ: 360px đến 1440px), kích thước font tối thiểu và tối đa tương ứng.
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn trong phạm vi dự án, không can thiệp vào tài nguyên sản xuất khi chưa có phê duyệt.

## 5. Core Concepts & Taxonomy
- **Linear Interpolation Equation:** `clamp(min, preferred_vw, max)` với độ dốc tính toán theo `slope = (max - min) / (max_vw - min_vw)`.
- **Dynamic Line-Height:** Kích thước chữ càng lớn thì tỷ lệ `line-height` càng giảm dần (ví dụ 1.1 cho H1, 1.5 cho Body).
- **Variable Font Optical Sizing:** Tự động điều chỉnh độ dày và chi tiết chữ theo kích thước hiển thị (`font-optical-sizing: auto`).

## 6. Step-by-Step Execution Workflow
1. Xác định kích thước cơ sở (base font-size) và tỷ lệ bước nhảy (Modular Ratio, ví dụ: 1.25 Major Third).
2. Thiết lập cận dưới màn hình `min_width` và cận trên `max_width`.
3. Áp dụng công thức nội suy tuyến tính để tính toán giá trị `y-axis intersection` và `slope in vw`.
4. Tạo biến CSS Custom Properties cho từng cấp bậc: `--font-display`, `--font-h1`, `--font-h2`, `--font-body`.
5. Kiểm tra trực quan độ mượt khi thay đổi kích thước cửa sổ trình duyệt (Window Resize Test).

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```css
/* Fluid Typography Calculation */
:root {
  /* min: 32px @ 375px viewport, max: 64px @ 1440px viewport */
  /* slope = (64 - 32) / (1440 - 375) = 0.03004 => 3.004vw */
  /* intercept = 32 - (375 * 0.03004) = 20.73px */
  --font-h1-fluid: clamp(2rem, 1.295rem + 3.004vw, 4rem);
  --font-body-fluid: clamp(1rem, 0.941rem + 0.25vw, 1.125rem);
}

h1 {
  font-size: var(--font-h1-fluid);
  line-height: 1.15;
  letter-spacing: -0.02em;
}
```

## 8. Anti-Patterns & Common Traps
- Dùng `font-size: 5vw` trực tiếp mà không có hàm `clamp()` bọc ngoài, dẫn đến chữ quá bé trên mobile hoặc quá khổng lồ trên màn hình 4K.
- Giữ nguyên `line-height: 1.5` cho tiêu đề kích thước 48px khiến khoảng trống giữa các dòng bị loãng quá mức.
- Dùng đơn vị pixel tuyệt đối làm mất khả năng phóng to chữ của người dùng khi cài đặt trợ năng trình duyệt.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Cỡ chữ co giãn liên tục, không có hiện tượng vỡ layout hoặc nhảy bước khi resize.
- QG-02: Đơn vị font cơ sở tôn trọng cài đặt gốc của người dùng (`rem` thay vì `px` cứng).
- QG-03: Chiều dài dòng đọc (Measure) của văn bản body duy trì trong ngưỡng tối ưu từ 45 đến 75 ký tự.

## 10. Security & Safety Boundaries
- Không nạp các webfont từ các CDN không đáng tin cậy để ngăn ngừa tấn công man-in-the-middle hoặc lộ dữ liệu người dùng qua font fingerprinting.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Module CSS Typography tokens `typography.fluid.css`.
1. Bảng tính toán tham số clamp cho toàn bộ các cấp bậc tiêu đề.

## 13. Related & Complementary Skills
- [`dex-design-system-tokens`](.agents/skills/dex-design-system-tokens/SKILL.md)
- [`dex-layout-composition-patterns`](.agents/skills/dex-layout-composition-patterns/SKILL.md)
- [`dex-frontend-performance`](.agents/skills/dex-frontend-performance/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Xây dựng portal tin tức công nghệ đa nền tảng. Sử dụng `dex-fluid-typography-engineering` để thiết lập thang đo tiêu đề co giãn mượt mà từ 28px trên iPhone mini lên tới 72px trên màn hình Ultrawide 34 inch mà không cần đến một dòng media query nào.
