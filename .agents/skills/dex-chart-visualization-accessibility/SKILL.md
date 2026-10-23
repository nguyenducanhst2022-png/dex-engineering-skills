---
name: dex-chart-visualization-accessibility
description: Engineer accessible, keyboard-navigable data visualizations and charts with high-contrast color palettes, tactile pattern textures, screen reader summaries, and alternative tabular representations. Use when building enterprise reporting and data dashboards.
---

# dex-chart-visualization-accessibility

## 1. Purpose & Scope
Thiết kế và triển khai các biểu đồ dữ liệu có khả năng tiếp cận cao (Accessible Charts); hỗ trợ điều hướng bàn phím, bảng màu tương phản thân thiện với người mù màu, hoa văn kết cấu (patterns), mô tả tóm tắt cho screen reader và chế độ xem bảng dữ liệu thay thế.

## 2. When to Use
- Khi các biểu đồ trong báo cáo chỉ phân biệt các chuỗi dữ liệu bằng màu sắc khiến người mù màu không đọc được.
- Khi người dùng sử dụng bàn phím không thể tương tác hoặc kiểm tra dữ liệu chi tiết của từng điểm dữ liệu trên biểu đồ.
- Khi hệ thống kiểm toán yêu cầu tuân thủ đầy đủ WCAG 2.2 AA cho các công cụ trực quan hóa dữ liệu.

## 3. When NOT to Use
- Khi hình ảnh trực quan chỉ là hình minh họa trang trí thuần túy (decorative icons) không mang giá trị thông tin số liệu.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Thư viện biểu đồ (D3, Chart.js, Recharts, ECharts), bộ dữ liệu định dạng JSON.
- **Quyền hạn truy cập:** Quyền sửa đổi component trực quan hóa dữ liệu.

## 5. Core Concepts & Taxonomy
- **Color-Blind Safe Palettes:** Bộ màu được thiết kế để phân biệt rõ ràng dưới các hội chứng mù màu phổ biến (Protanopia, Deuteranopia, Tritanopia).
- **Pattern Fills:** Bổ sung các đường sọc chéo, chấm bi hoặc nét đứt vào các thanh biểu đồ để phân biệt chuỗi dữ liệu mà không phụ thuộc vào màu sắc.
- **Accessible Data Table Alternative:** Luôn cung cấp một nút bấm để chuyển đổi linh hoạt giữa biểu đồ đồ họa và bảng số liệu HTML ngữ nghĩa (`<table>`).

## 6. Step-by-Step Execution Workflow
1. Lựa chọn bảng màu biểu đồ an toàn với người mù màu có độ tương phản tối thiểu 3:1 so với nền.
2. Tích hợp hoa văn họa tiết (SVG patterns) cho các vùng diện tích hoặc các cột biểu đồ.
3. Cấu hình cấu trúc SVG ngữ nghĩa: gắn thẻ `<title>`, `<desc>` và các thuộc tính `role="graphics-document"`.
4. Bổ sung hỗ trợ điều hướng bằng phím mũi tên giữa các điểm dữ liệu và thông báo giá trị qua `aria-live`.
5. Cung cấp nút chuyển đổi hiển thị bảng dữ liệu thay thế kèm chức năng tải file CSV.
6. Kiểm thử biểu đồ với công cụ giả lập mù màu và phần mềm đọc màn hình NVDA / VoiceOver.

## 7. Concrete Examples
### Tạo biểu đồ cột SVG có hỗ trợ Pattern và Screen Reader:
```html
<svg role="graphics-document" aria-label="Biểu đồ doanh thu quý 1 đến quý 4" viewBox="0 0 400 200">
  <defs>
    <!-- Hoa văn sọc chéo để phân biệt không cần màu -->
    <pattern id="diagonal-stripe" width="8" height="8" patternTransform="rotate(45)" patternUnits="userSpaceOnUse">
      <line x1="0" y1="0" x2="0" y2="8" stroke="#1e293b" stroke-width="2" />
    </pattern>
  </defs>
  
  <rect x="50" y="50" width="40" height="150" fill="url(#diagonal-stripe)" 
        tabindex="0" role="graphics-symbol" aria-label="Quý 1: 150 triệu VNĐ" />
  <rect x="120" y="30" width="40" height="170" fill="#3b82f6" 
        tabindex="0" role="graphics-symbol" aria-label="Quý 2: 170 triệu VNĐ" />
</svg>

<button type="button" aria-expanded="false" onclick="toggleTableView()">
  Xem dưới dạng bảng số liệu
</button>
```

## 8. Anti-Patterns & Common Traps
- **Color-Only Encoding:** Phân biệt 5 đường biểu đồ khác nhau chỉ bằng các sắc thái màu xanh lá cây và đỏ.
- **Canvas Black Box:** Vẽ biểu đồ lên thẻ `<canvas>` mà không cung cấp cấu trúc DOM dự phòng hoặc mô tả văn bản thay thế.
- **Hover-Only Data Tooltips:** Chỉ hiển thị giá trị số liệu khi di chuột, khiến người dùng duyệt bằng bàn phím hoàn toàn không thể tiếp cận.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Mọi biểu đồ đều có chế độ xem bảng dữ liệu HTML thay thế hoặc bản mô tả tóm tắt số liệu.
- **QG-03**: Tất cả các điểm dữ liệu đều có thể nhận focus và đọc được thông tin bằng bàn phím.
- **QG-06**: Bảng màu vượt qua bài kiểm tra mô phỏng mù màu không có chuỗi dữ liệu nào bị trùng độ sáng.

## 10. Security & Safety Boundaries
- Tránh đưa dữ liệu chưa khử khuẩn vào các nhãn tooltip SVG để ngăn ngừa lỗ hổng DOM-based XSS.

## 11. Platform Adapters
- **Chart Libraries**: D3.js, Chart.js, Recharts, Observable Plot, Highcharts Highcharts-A11y.

## 12. Deliverables & Output Artifacts
- Component biểu đồ tích hợp hỗ trợ a11y đầy đủ.
- Bảng màu tương thích mù màu và bộ SVG patterns.
- Chế độ xem bảng dữ liệu dự phòng có thể chuyển đổi.

## 13. Related & Complementary Skills
dex-accessibility-automation, dex-high-density-dashboard-layout, dex-component-state-matrix

## 14. Realistic Usage Example
```powershell
# Kiểm toán khả năng tiếp cận biểu đồ bằng axe-core
npx cypress run --spec "cypress/e2e/chart-a11y.cy.ts"

# Kiểm tra phân biệt màu sắc với công cụ giả lập mù màu
npx pa11y http://localhost:3000/reports/sales --reporter json
```
