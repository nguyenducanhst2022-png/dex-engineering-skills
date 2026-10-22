---
name: dex-visual-hierarchy-audit
description: Audit and restructure visual hierarchy, content emphasis, information density, and reading order across complex screens to eliminate competing focal points. Use when evaluating confusing UI layouts, cluttered dashboards, or high-friction landing pages.
---

# dex-visual-hierarchy-audit

## 1. Purpose & Scope
Kiểm toán và tái cấu trúc phân cấp thị giác (Visual Hierarchy), độ nổi bật của nội dung, mật độ thông tin và thứ tự đọc trên các màn hình phức tạp; triệt tiêu các điểm nhấn thị giác cạnh tranh nhau, dẫn dắt ánh nhìn người dùng đến các hành động chuyển đổi chính.

## 2. When to Use
- Khi màn hình hiển thị quá nhiều nút bấm, thẻ thông tin khiến người dùng bị quá tải nhận thức (cognitive overload).
- Khi tỷ lệ chuyển đổi hoặc hoàn thành tác vụ trên trang quan trọng bị sụt giảm.
- Trước khi phát hành một tính năng phức tạp có nhiều mức độ ưu tiên thông tin khác nhau.

## 3. When NOT to Use
- Khi kiểm tra hiệu năng tải trang thuần túy (Network/Render latency) - dùng `dex-frontend-performance`.
- Khi viết unit test cho các logic tính toán nội bộ không có giao diện người dùng.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Ảnh chụp màn hình (Figma/Live UI), DOM tree hiện tại, thứ tự ưu tiên nghiệp vụ của từng khối nội dung.
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn trong phạm vi dự án, không can thiệp vào tài nguyên sản xuất khi chưa có phê duyệt.

## 5. Core Concepts & Taxonomy
- **Visual Weight:** Mức độ hút mắt dựa trên kích thước, độ tương phản màu sắc, vị trí và khoảng trống.
- **F-Shape / Z-Pattern:** Đường quét mắt tự nhiên của người dùng theo thói quen đọc văn hóa.
- **Focal Point Isolation:** Giới hạn tối đa một điểm nhấn thị giác chính (Primary CTA) trên mỗi vùng nhìn.

## 6. Step-by-Step Execution Workflow
1. Liệt kê tất cả các phần tử trên màn hình và gắn nhãn mức độ ưu tiên: Primary, Secondary, Tertiary.
2. Áp dụng phương pháp làm mờ (Squint Test / Blur Filter) để nhận diện các điểm sáng gây phân tán ánh nhìn.
3. Đo lường tỷ lệ tương phản và độ lớn phông chữ để đảm bảo trật tự đọc tuyến tính rõ ràng.
4. Tái cấu trúc bố cục, tăng padding âm (whitespace) xung quanh phần tử trọng tâm và giảm sắc độ của phần tử phụ.
5. Lập biên bản đánh giá phân cấp thị giác kèm kiến nghị tinh chỉnh CSS/DOM.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```css
/* Enforcing Strict Visual Hierarchy */
.primary-action-card {
  border: 2px solid var(--color-brand-primary);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
  z-index: 2;
}

.secondary-meta-card {
  border: 1px solid var(--color-border-subtle);
  background-color: var(--color-surface-subdued);
  color: var(--color-text-muted);
  opacity: 0.85;
}
```

## 8. Anti-Patterns & Common Traps
- Đặt từ 3 nút bấm phong cách `filled primary` cạnh nhau trên cùng một thẻ.
- Dùng màu đỏ báo động cho các thông tin trạng thái thông thường làm mất tác dụng của cảnh báo lỗi.
- Thu nhỏ cỡ chữ quá mức (<11px) để nhồi nhét dữ liệu thay vì cấu trúc lại thông tin.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Điểm nhấn thị giác chính (Primary Focal Point) chiếm vị trí ưu tiên và được nhận diện trong 3 giây đầu.
- QG-02: Tỷ lệ phân cấp kích cỡ font chữ giữa Title, Subtitle và Body tuân thủ hệ số tỷ lệ tối thiểu 1.25x.
- QG-03: Không có xung đột màu sắc giữa các trạng thái cảnh báo và màu sắc nhận diện thương hiệu.

## 10. Security & Safety Boundaries
- Không ẩn giấu các điều khoản dịch vụ hoặc cảnh báo bảo mật quan trọng bằng kỹ thuật giảm kích thước chữ.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Báo cáo `VISUAL_HIERARCHY_AUDIT.md` phân tích trước và sau khi tối ưu.
1. Sơ đồ luồng quét mắt (Eye-path diagram) và bản vá CSS định hình phân cấp.

## 13. Related & Complementary Skills
- [`dex-design-brief-synthesis`](.agents/skills/dex-design-brief-synthesis/SKILL.md)
- [`dex-layout-composition-patterns`](.agents/skills/dex-layout-composition-patterns/SKILL.md)
- [`dex-ux-accessibility`](.agents/skills/dex-ux-accessibility/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Trang thanh toán của hệ thống e-commerce có 4 nút bấm cùng màu xanh lá cây gây nhầm lẫn khi người dùng muốn nhập mã giảm giá. Áp dụng `dex-visual-hierarchy-audit` để hạ cấp nút áp dụng mã thành dạng ghost button và làm nổi bật nút 'Đặt hàng ngay'.
