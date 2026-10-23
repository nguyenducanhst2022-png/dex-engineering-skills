---
name: dex-design-token-migration
description: Automate migration from hardcoded CSS/SCSS styling and legacy design tokens to modern W3C Design Tokens Community Group (DTCG) formats and CSS custom properties. Use when consolidating divergent design tokens or refactoring legacy component stylesheets.
---

# dex-design-token-migration

## 1. Purpose & Scope
Tự động hóa chuyển đổi các giá trị giao diện hardcoded (màu sắc, khoảng cách, font, shadow) và hệ thống token cũ sang định dạng chuẩn W3C Design Tokens Community Group (DTCG) và CSS Custom Properties; bảo đảm tính nhất quán đa nền tảng và hỗ trợ chuyển đổi theme động.

## 2. When to Use
- Khi chuẩn hóa hệ thống Design System từ các biến Sass/Less rời rạc sang chuẩn DTCG JSON.
- Khi triển khai cơ chế Dark Mode hoặc Multi-branding yêu cầu các token ngữ nghĩa (semantic tokens) động.
- Khi thực hiện kiểm toán CSS codebase để triệt tiêu các mã màu hex và kích thước px phân mảnh.

## 3. When NOT to Use
- Khi dự án là landing page đơn lẻ, tĩnh, không có kế hoạch mở rộng hoặc đa theme.
- Khi chưa có sự đồng thuận giữa đội ngũ UI/UX Design (Figma) và Engineering về quy ước đặt tên token.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** File định nghĩa token (Figma Tokens JSON, Style Dictionary config, SCSS variables) và codebase giao diện hiện hữu.
- **Quyền hạn truy cập:** Quyền ghi vào thư mục style/tokens và component libraries.

## 5. Core Concepts & Taxonomy
- **Design Tokens Format Module (DTCG):** Chuẩn mở JSON quy định kiểu dữ liệu token (`$value`, `$type`, `$description`).
- **Token Tiering:** Kiến trúc 3 tầng: Global/Reference Tokens (`color.blue.500`) -> Semantic Tokens (`color.background.interactive.hover`) -> Component Tokens (`button.primary.bg`).
- **Style Dictionary:** Công cụ build biến đổi token từ nguồn JSON sang CSS, SCSS, Swift, Android XML.

## 6. Step-by-Step Execution Workflow
1. Khảo sát và trích xuất tất cả các biến màu sắc, typography, spacing từ SCSS, CSS Modules, Styled Components.
2. Chuẩn hóa phân loại token thành 3 tầng: Base/Primitive, Semantic/Alias, và Component-specific.
3. Biên dịch cấu trúc JSON tuân thủ đặc tả W3C DTCG Format.
4. Cấu hình Style Dictionary để xuất ra CSS Custom Properties có fallback an toàn.
5. Xây dựng AST Codemod (jscodeshift hoặc Stylelint plugin) để tự động thay thế mã màu hardcoded bằng biến token tương ứng.
6. Chạy visual regression testing để xác thực giao diện không bị lệch pixel sau khi chuyển đổi.

## 7. Concrete Examples
### Cấu trúc W3C DTCG Token và cấu hình Style Dictionary:
```json
{
  "color": {
    "semantic": {
      "surface": {
        "primary": {
          "$value": "{color.base.neutral.0}",
          "$type": "color",
          "$description": "Nền chính cho các card và view viewports"
        },
        "brand": {
          "$value": "{color.base.blue.600}",
          "$type": "color",
          "$description": "Màu nhận diện thương hiệu cho các điểm nhấn chính"
        }
      }
    }
  }
}
```

```javascript
// style-dictionary.config.js
export default {
  source: ['tokens/**/*.json'],
  platforms: {
    css: {
      transformGroup: 'css',
      buildPath: 'src/styles/',
      files: [{
        destination: 'variables.css',
        format: 'css/variables',
        options: { outputReferences: true }
      }]
    }
  }
};
```

## 8. Anti-Patterns & Common Traps
- **Direct Global Token Usage:** Sử dụng trực tiếp token cơ sở như `var(--color-blue-500)` trong component thay vì dùng token ngữ nghĩa `var(--color-action-primary)`.
- **Unbound Circular Tokens:** Khai báo token tham chiếu vòng lặp khiến trình biên dịch bị treo.
- **Silent Breaking Overrides:** Ghi đè biến CSS cục bộ làm phá vỡ tính nhất quán của theme toàn hệ thống.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: 100% token JSON vượt qua xác thực cú pháp JSON Schema của W3C DTCG.
- **QG-04**: Quá trình biên dịch token xuất ra CSS variables hợp lệ không bị cảnh báo Stylelint.
- **QG-07**: Không còn mã màu hex hoặc kích thước px hardcoded trong các component mới.

## 10. Security & Safety Boundaries
- Kiểm tra định dạng token file không chứa các payload CSS injection hoặc biểu thức `url()` độc hại.

## 11. Platform Adapters
- **Build Tools**: Style Dictionary v4, Token Studio, Stylelint.
- **Platforms**: Web (CSS/SCSS), iOS (Swift), Android (Compose/XML).

## 12. Deliverables & Output Artifacts
- File JSON chuẩn W3C DTCG token.
- File CSS variables và TypeScript type definitions cho token.
- Script Codemod tự động chuyển đổi mã nguồn cũ.

## 13. Related & Complementary Skills
dex-design-system-foundations, dex-visual-hierarchy-composition, dex-theme-lifecycle-management

## 14. Realistic Usage Example
```powershell
# Chạy Style Dictionary để biên dịch tokens sang CSS custom properties
npx style-dictionary build

# Kiểm tra các giá trị hardcoded còn sót lại trong CSS codebase
npx stylelint "src/**/*.css" --config .stylelintrc-token-check.json
```
