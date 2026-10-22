---
name: dex-design-brief-synthesis
description: Synthesize business requirements, user personas, and brand identity into an actionable visual design brief with aesthetic tokens, layout guidelines, and accessibility constraints. Use when kicking off new frontend projects, UI redesigns, or translating PRDs into design specifications.
---

# dex-design-brief-synthesis

## 1. Purpose & Scope
Tổng hợp yêu cầu kinh doanh, chân dung người dùng (personas) và định vị thương hiệu thành bản đặc tả thiết kế trực quan (Visual Design Brief) có tính hành động cao; xác lập ngôn ngữ thị giác, bảng màu ngữ nghĩa, tỷ lệ typography và tiêu chuẩn trải nghiệm người dùng.

## 2. When to Use
- Khi khởi động dự án frontend mới hoặc giai đoạn tái thiết kế giao diện (UI redesign).
- Khi cần chuyển đổi tài liệu Product Requirements Document (PRD) sang ngôn ngữ thị giác và cấu trúc component.
- Khi cần thống nhất phong cách thẩm mỹ giữa Product Managers, Designers và Frontend Engineers.

## 3. When NOT to Use
- Khi chỉ sửa các lỗi CSS nhỏ hoặc tinh chỉnh pixel đơn lẻ trong component đã có.
- Khi chưa có mục tiêu kinh doanh hoặc đối tượng người dùng rõ ràng.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Tài liệu yêu cầu sản phẩm (PRD), hướng dẫn nhận diện thương hiệu (Brand Guidelines), hồ sơ người dùng mục tiêu.
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn trong phạm vi dự án, không can thiệp vào tài nguyên sản xuất khi chưa có phê duyệt.

## 5. Core Concepts & Taxonomy
- **Aesthetic Intent:** Xác định rõ trạng thái cảm xúc (ví dụ: Modern Enterprise, Minimalist, Cyberpunk).
- **Design Token Primitives:** Thiết lập các biến số nền tảng về màu sắc, khoảng cách và kiểu chữ.
- **Accessibility Baselines:** Đặt mục tiêu tương phản tối thiểu WCAG 2.1 AA/AAA ngay từ khâu thiết kế.

## 6. Step-by-Step Execution Workflow
1. Thu thập mục tiêu sản phẩm, chân dung người dùng và ràng buộc thương hiệu từ stakeholder.
2. Xác định tính cách giao diện (archetype) và các nguyên lý thiết kế chủ đạo (Design Principles).
3. Đặc tả hệ thống màu sắc ngữ nghĩa (semantic palette), tỷ lệ font (type scale) và thang khoảng cách (spacing scale).
4. Thiết lập cấu trúc bố cục lưới (grid), breakpoints responsive và quy tắc phân cấp thị giác.
5. Xuất bản tài liệu `DESIGN_BRIEF.md` và đồng bộ token cơ sở vào hệ thống tokens.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```json
{
  "$schema": "https://dex.dev/schemas/design-brief.json",
  "project": "dex-cloud-console",
  "archetype": "High-Density Enterprise SaaS",
  "designPrinciples": [
    "Information density over decorative whitespace",
    "Instant telemetry readability with APCA 75+ contrast",
    "Predictable keyboard-driven navigation flows"
  ],
  "visualTokens": {
    "colorModes": ["light", "dark", "high-contrast"],
    "baseFontFamily": "Inter, system-ui, sans-serif",
    "baseUnit": 4,
    "targetWCAG": "WCAG_2_1_AA"
  }
}
```

## 8. Anti-Patterns & Common Traps
- Bắt đầu code giao diện mà không có tài liệu định hướng phong cách dẫn đến UI chắp vá.
- Lựa chọn màu sắc thuần túy theo sở thích cá nhân mà bỏ qua kiểm tra độ tương phản và ngữ cảnh sử dụng.
- Thiết kế bố cục cứng nhắc theo một độ phân giải duy nhất, gây vỡ giao diện trên màn hình khác.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Tài liệu `DESIGN_BRIEF.md` hoàn chỉnh với đầy đủ bảng màu, typography và lưới bố cục.
- QG-02: Bảng màu đáp ứng tỷ lệ tương phản tối thiểu 4.5:1 cho văn bản thông thường theo WCAG 2.1 AA.
- QG-03: Được phê duyệt bởi cả bộ phận kỹ thuật frontend và quản lý sản phẩm.

## 10. Security & Safety Boundaries
- Không nhúng các tài nguyên hình ảnh hoặc font chữ không có bản quyền thương mại; bảo vệ bí mật dự án trong tài liệu brief.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Tài liệu `DESIGN_BRIEF.md` chuẩn hóa.
1. Bảng token khởi tạo ban đầu `tokens.brief.json`.
1. Checklist tiêu chí kiểm tra thiết kế trực quan.

## 13. Related & Complementary Skills
- [`dex-visual-hierarchy-audit`](.agents/skills/dex-visual-hierarchy-audit/SKILL.md)
- [`dex-design-system-tokens`](.agents/skills/dex-design-system-tokens/SKILL.md)
- [`dex-color-contrast-systems`](.agents/skills/dex-color-contrast-systems/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Đội ngũ phát triển chuẩn bị xây dựng phân hệ quản trị hạ tầng đám mây. Kỹ sư kích hoạt `dex-design-brief-synthesis` để chuyển đổi tài liệu PRD dài 30 trang thành một Design Brief cô đọng, định hình giao diện bảng điều khiển mật độ cao với chế độ Dark Mode chuẩn xác.
