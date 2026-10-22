---
name: dex-design-system-tokens
description: Manage design system tokens, typography scales, color palettes, spacing units, and dark mode theming variables across web platforms. Use when implementing design systems, synchronizing Figma tokens, or standardizing UI themes.
---

# dex-design-system-tokens

## 1. Purpose & Scope
Thiết lập, quản lý và đồng bộ hóa hệ thống Design Tokens (Màu sắc, Typography, Khoảng cách Spacing, Bo góc Radius, Bóng đổ Elevation) theo tiêu chuẩn W3C Design Tokens, hỗ trợ đa chủ đề (Light/Dark mode) và đảm bảo tính nhất quán trực quan toàn diện trên mọi màn hình.

## 2. When to Use
- Khi bắt đầu xây dựng hoặc cập nhật Design System cho tổ chức.
- Khi cần hỗ trợ chuyển đổi giao diện Sáng / Tối (Light / Dark theme switching).
- Khi các giá trị màu sắc, padding, margin bị hardcode rải rác dưới dạng magic numbers trong CSS.

## 3. When NOT to Use
- Sửa một nút bấm cá biệt trong một landing page dùng một lần.
- Khi dự án đã sử dụng thư viện UI có sẵn (như MUI, AntD) và không có nhu cầu tùy biến tokens.

## 4. Prerequisites & Input Context
**Đầu vào cần thiết:**
- Bảng mã màu, kiểu chữ và spacing từ đội ngũ Design (Figma Tokens / Style Dictionary).
- Định dạng đích cần xuất (CSS Variables, Tailwind Config, SCSS variables, JSON).

**Điều kiện tiên quyết:**
- Đã thống nhất quy tắc đặt tên token theo phân cấp: Global Tokens -> Alias/Semantic Tokens -> Component Tokens.
- Môi trường build hỗ trợ xử lý CSS Custom Properties hoặc Tailwind CSS.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**: Nắm vững cơ chế vận hành theo chuẩn Agent Skills, tuân thủ nghiêm ngặt tính xác định và ranh giới trách nhiệm.
- **Quy tắc quyết định kỹ thuật**:
- **Semantic First**: Không bao giờ sử dụng trực tiếp Global Token (như `blue-500`) trong component; luôn dùng Semantic Token (`bg-primary`).
- **Tỷ lệ 8-point Grid**: Quy chuẩn hóa spacing dựa trên bội số của 4px hoặc 8px.
- **Không Thừa Thãi**: Loại bỏ các token màu sắc hoặc kích cỡ font chữ không có trong bản thiết kế chính thức.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Lỗi nhấp nháy giao diện khi tải trang (FOUC Theme Flash)**: Trình duyệt tải light mode trước rồi mới đổi sang dark mode -> Khắc phục: Nhúng script nhỏ đồng bộ theme tại `<head>` trước khi DOM render.
- **Độ tương phản Dark Mode quá thấp**: Chữ xám trên nền đen không đọc được -> Khắc phục: Chạy kiểm toán độ tương phản và tinh chỉnh semantic token `text-secondary`.

## 6. Step-by-Step Execution Workflow
1. Khai báo Global Tokens (bảng màu cơ bản, font families, base spacing unit 4px/8px).
2. Ánh xạ sang Semantic Tokens phản ánh ngữ cảnh sử dụng (ví dụ: `color-bg-primary`, `color-text-danger`).
3. Khai báo các biến thể theme (Light mode và Dark mode) bằng CSS Custom Properties.
4. Tích hợp Tokens vào cấu hình build hệ thống (ví dụ `tailwind.config.js`).
5. Kiểm tra tính tương thích và độ tương phản màu sắc đạt chuẩn WCAG AA.

## 7. Concrete Examples
### Ví dụ triển khai chuẩn mực:
```css
/* tokens.css */
:root {
  --color-bg-canvas: #ffffff;
  --color-text-primary: #111827;
  --color-action-primary: #2563eb;
  --space-4: 1rem;
  --radius-md: 0.375rem;
}

[data-theme='dark'] {
  --color-bg-canvas: #0f172a;
  --color-text-primary: #f8fafc;
  --color-action-primary: #3b82f6;
}
```

### Lệnh xác minh & thực thi:
- Kiểm tra tính hợp lệ của token schema: `npx style-dictionary build`
- Kiểm tra độ tương phản tự động: `npx pa11y http://localhost:3000`
- Kiểm tra CSS output không có biến rỗng: `grep 'var(--' dist/styles.css`

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước kiểm tra biên và giả định hệ thống luôn ở trạng thái lý tưởng.
- **Anti-Pattern 2**: Không ghi nhận nhật ký kiểm toán hoặc bỏ qua việc xử lý ngoại lệ lúc runtime.
- **Trap**: Bỏ qua các rào chắn an toàn hoặc cố tình chạy script không qua kiểm thử tự động.

## 9. Quality Gates & Acceptance Criteria
- QG-03: 0 magic hex color codes được phép tồn tại trong các file component UI.
- QG-07: Tỷ lệ tương phản giữa Text Token và Background Token đạt tối thiểu 4.5:1.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động trước khi coi là hoàn thành.

## 10. Security & Safety Boundaries
- Tránh nạp token qua các URL không an toàn hoặc cho phép người dùng tự inject CSS token tùy tiện gây lỗ hổng CSS Injection.
- Không bao giờ thực thi mã nguồn hoặc thay đổi cấu hình trên môi trường sản xuất mà thiếu cơ chế rollback an toàn.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Có thể kích hoạt trực tiếp từ terminal hoặc extension tương thích trong VS Code / Cursor / Windsurf.

## 12. Deliverables & Output Artifacts
- File định nghĩa Tokens nguồn (`tokens/design-tokens.json`).
- File CSS variables xuất xưởng (`dist/tokens.css`).
- Cấu hình theme tích hợp (`tailwind.config.ts`).

## 13. Related & Complementary Skills
- `dex-development-workflow`: Quy trình phát triển tiêu chuẩn.
- `dex-code-verification`: Xác minh chất lượng và tính đúng đắn của mã nguồn.
- `dex-master-orchestrator`: Bộ điều phối trung tâm kết nối kỹ năng này với các kỹ năng khác trong hệ thống.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư hoặc AI Agent tiếp nhận yêu cầu liên quan đến **dex-design-system-tokens**.
1. Đọc kỹ đầu vào và các ràng buộc kỹ thuật tại mục 4.
2. Thực thi tuần tự 6 bước trong Workflow tại mục 6.
3. Chạy các lệnh kiểm chứng tại mục 7 và đối chiếu với Quality Gates tại mục 9.
4. Đóng gói deliverables theo danh sách tại mục 12 và báo cáo kết quả kèm bằng chứng xác thực.
