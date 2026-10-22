---
name: dex-layout-composition-patterns
description: Evaluate and engineer responsive layout compositions including 12-column grids, asymmetric Bento boxes, editorial flows, and split-screen dashboards. Use when selecting page architecture, organizing multi-card views, or designing responsive breakpoints.
---

# dex-layout-composition-patterns

## 1. Purpose & Scope
Đánh giá, lựa chọn và hiện thực hóa các mô hình bố cục không gian (Layout Compositions) hiện đại: hệ thống lưới 12 cột, bố cục Bento Box bất đối xứng, dòng chảy bài viết (editorial flow) và bố cục chia màn hình (split-screen); đảm bảo co giãn mượt mà trên mọi thiết bị.

## 2. When to Use
- Khi xây dựng cấu trúc trang mới cho landing page, portal quản trị hoặc ứng dụng đa phương tiện.
- Khi tổ chức các thẻ nội dung có kích thước và mức độ quan trọng không đồng đều.
- Khi giải quyết vấn đề tràn nội dung (overflow) hoặc khoảng trống thừa vô lý trên màn hình siêu rộng (Ultrawide).

## 3. When NOT to Use
- Khi thiết kế các phần tử nội dòng (inline elements) đơn giản như badge, icon hoặc breadcrumbs.
- Khi hệ thống đã có template khung cứng cố định không cho phép thay đổi cấu trúc trang.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Đặc tả các thành phần nội dung, kích thước màn hình mục tiêu (mobile, tablet, desktop, ultrawide), hệ thống spacing token.
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn trong phạm vi dự án, không can thiệp vào tài nguyên sản xuất khi chưa có phê duyệt.

## 5. Core Concepts & Taxonomy
- **Bento Grid Architecture:** Gom nhóm thông tin theo các khối chữ nhật có kích thước tỷ lệ hài hòa (1x1, 1x2, 2x2).
- **CSS Subgrid & Grid Template Areas:** Định nghĩa cấu trúc lưới phân tầng bảo toàn sự gióng hàng giữa các thẻ con.
- **Container Queries (`@container`):** Co giãn bố cục dựa trên không gian thực của component cha thay vì viewport toàn trang.

## 6. Step-by-Step Execution Workflow
1. Phân tích dạng nội dung và xác định mô hình bố cục phù hợp (Bento, 12-col grid, Masonry hoặc Master-Detail).
2. Thiết lập CSS Grid layout với các vùng định danh `grid-template-areas` trực quan.
3. Khai báo Container Queries để các component con tự thích ứng khi nằm ở cột hẹp hay cột rộng.
4. Kiểm tra co giãn trên các mốc kích thước cực hạn (320px mobile đến 3840px 4K monitor).
5. Xác nhận các quy tắc chuyển đổi bố cục không gây giật cục hoặc chồng chéo nội dung.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```css
/* Bento Grid Layout Pattern */
.bento-container {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-auto-rows: minmax(180px, auto);
  gap: var(--space-4);
}

.bento-card-featured {
  grid-column: span 2;
  grid-row: span 2;
}

.bento-card-stat {
  grid-column: span 1;
}

@container (max-width: 640px) {
  .bento-container {
    grid-template-columns: 1fr;
  }
}
```

## 8. Anti-Patterns & Common Traps
- Sử dụng lồng ghép quá nhiều thẻ `div` với `display: flex` phức tạp thay vì dùng một cấu trúc `CSS Grid` duy nhất.
- Cố định chiều cao phần tử bằng pixel cứng (`height: 300px`) khiến nội dung bị tràn khi chữ phóng to.
- Thiết kế chỉ nghĩ đến desktop rồi ép co cụm trên mobile khiến người dùng phải cuộn ngang bất tiện.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Không xuất hiện thanh cuộn ngang (horizontal scrollbar) không mong muốn ở bất kỳ breakpoint nào.
- QG-02: Cấu trúc lưới duy trì khoảng cách `gap` đồng bộ theo thang spacing chuẩn.
- QG-03: Kiểm tra hiển thị đạt chuẩn trên cả 4 kích thước: Mobile (375px), Tablet (768px), Desktop (1440px), 4K (2560px).

## 10. Security & Safety Boundaries
- Ngăn ngừa hiện tượng Clickjacking bằng cách kiểm soát cấu trúc frame và không cho phép chèn đè iframe vô hình lên bố cục.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Mẫu CSS Layout module chuẩn hóa (`layout.bento.css`).
1. Bộ quy tắc responsive breakpoint và container query guidelines.

## 13. Related & Complementary Skills
- [`dex-visual-hierarchy-audit`](.agents/skills/dex-visual-hierarchy-audit/SKILL.md)
- [`dex-fluid-typography-engineering`](.agents/skills/dex-fluid-typography-engineering/SKILL.md)
- [`dex-ui-component-contracts`](.agents/skills/dex-ui-component-contracts/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Xây dựng dashboard tổng hợp telemetry IoT. Áp dụng kỹ năng `dex-layout-composition-patterns` để tạo Bento Grid đa tầng hiển thị biểu đồ nhiệt độ chính ở khung 2x2, các trạng thái pin ở khung 1x1 và tự động gập thành 1 cột trên mobile.
