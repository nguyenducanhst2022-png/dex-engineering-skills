---
name: dex-color-contrast-systems
description: Engineer mathematical APCA and WCAG 2.1 AA/AAA color contrast relationships across semantic UI states, light/dark themes, and interactive focus states. Use when building accessible color palettes, styling data visualizations, or remediating contrast failures.
---

# dex-color-contrast-systems

## 1. Purpose & Scope
Xây dựng hệ thống bảng màu toán học đáp ứng tiêu chuẩn tương phản WCAG 2.1 (AA/AAA) và giải thuật APCA (Accessible Perceptual Contrast Algorithm); đảm bảo khả năng đọc hoàn hảo trên các trạng thái giao diện, chế độ sáng/tối (Light/Dark mode) và độ tương phản cao.

## 2. When to Use
- Khi xây dựng hoặc refactor bảng màu cho Design System của doanh nghiệp.
- Khi nhận báo cáo kiểm toán tiếp cận (Accessibility Audit) cảnh báo lỗi độ tương phản thấp.
- Khi thiết kế biểu đồ trực quan hóa dữ liệu có nhiều series màu sắc cần phân biệt rõ ràng.

## 3. When NOT to Use
- Khi làm việc với các phần tử đồ họa trang trí thuần túy không mang ý nghĩa thông tin hoặc điều hướng.
- Khi trạng thái phần tử bị vô hiệu hóa (disabled state) mà tiêu chuẩn WCAG có ngoại lệ cho phép.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Mã màu hex/hsl của thương hiệu, danh sách các trạng thái tương tác (default, hover, focus, active, disabled).
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn trong phạm vi dự án, không can thiệp vào tài nguyên sản xuất khi chưa có phê duyệt.

## 5. Core Concepts & Taxonomy
- **WCAG 2.1 Relative Luminance:** Tỷ lệ tương phản 4.5:1 (normal text) và 3:1 (large text / UI components).
- **APCA (Advanced Perceptual Contrast Algorithm):** Đo lường độ tương phản theo cảm nhận thị giác thực tế của não bộ.
- **Semantic Color Tokens:** Tách biệt màu sắc chức năng (success, warning, error, info) khỏi màu thương hiệu.

## 6. Step-by-Step Execution Workflow
1. Thu thập danh mục màu nền (surface/background) và màu tiền cảnh (text/icon).
2. Chạy script tính toán Relative Luminance và tỷ lệ tương phản cho từng cặp màu phối hợp.
3. Kiểm tra tính đọc được trên cả 2 nền Light và Dark mode, tự động điều chỉnh sắc độ (Lightness/Chroma) nếu vi phạm.
4. Thiết lập đường viền chỉ báo tiêu điểm (focus indicator) với tỷ lệ tương phản tối thiểu 3:1 so với nền lân cận.
5. Xuất ra ma trận kiểm toán tương phản màu sắc `CONTRAST_MATRIX.json`.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```typescript
// Mathematical WCAG Contrast Ratio Calculation
export function getLuminance(r: number, g: number, b: number): number {
  const [rs, gs, bs] = [r, g, b].map(c => {
    c = c / 255;
    return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
  });
  return 0.2126 * rs + 0.7152 * gs + 0.0722 * bs;
}

export function getContrastRatio(rgb1: [number, number, number], rgb2: [number, number, number]): number {
  const lum1 = getLuminance(...rgb1);
  const lum2 = getLuminance(...rgb2);
  const brightest = Math.max(lum1, lum2);
  const darkest = Math.min(lum1, lum2);
  return (brightest + 0.05) / (darkest + 0.05);
}
```

## 8. Anti-Patterns & Common Traps
- Dùng chữ màu xám nhạt `#A0AEC0` trên nền trắng `#FFFFFF` (tỷ lệ chỉ đạt ~2.4:1, vi phạm nặng WCAG).
- Chỉ dùng duy nhất màu sắc để biểu thị trạng thái (ví dụ chấm đỏ/xanh) mà không kèm icon hoặc nhãn văn bản cho người mù màu.
- Chuyển đổi sang Dark Mode bằng cách đảo ngược màu cơ học khiến nền xám quá chói mắt.

## 9. Quality Gates & Acceptance Criteria
- QG-01: 100% văn bản nội dung thông thường đạt tỷ lệ tương phản >= 4.5:1.
- QG-02: 100% thành phần điều khiển giao diện (inputs, borders, icons) đạt tỷ lệ >= 3:1.
- QG-03: Vượt qua bài kiểm tra mô phỏng 3 dạng mù màu chính: Protanopia, Deuteranopia và Tritanopia.

## 10. Security & Safety Boundaries
- Đảm bảo các thông báo cảnh báo bảo mật và lỗi xác thực luôn có độ tương phản cao nhất để người dùng chú ý kịp thời.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Ma trận tương phản màu sắc `CONTRAST_MATRIX.json`.
1. Hệ thống token màu CSS/Tailwind đã được hiệu chuẩn tương phản.

## 13. Related & Complementary Skills
- [`dex-design-system-tokens`](.agents/skills/dex-design-system-tokens/SKILL.md)
- [`dex-ux-accessibility`](.agents/skills/dex-ux-accessibility/SKILL.md)
- [`dex-ui-visual-qa-review`](.agents/skills/dex-ui-visual-qa-review/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Kiểm toán hệ thống ngân hàng trực tuyến. Áp dụng `dex-color-contrast-systems` để rà soát toàn bộ 48 cặp màu UI, phát hiện 12 cặp chữ xám không đủ tương phản trên nền xám phụ và tự động nâng sắc độ từ `#888` lên `#595959` để đạt chuẩn AA.
