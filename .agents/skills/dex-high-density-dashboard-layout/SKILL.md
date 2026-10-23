---
name: dex-high-density-dashboard-layout
description: Architect high-density information layouts for data-intensive enterprise cockpits, financial terminals, and monitoring consoles. Use when structuring large volumes of real-time widgets without sacrificing visual hierarchy and cognitive load.
---

# dex-high-density-dashboard-layout

## 1. Purpose & Scope
Thiết kế và cấu trúc giao diện bảng điều khiển (Dashboard) mật độ thông tin cao cho các hệ thống giám sát thời gian thực, thiết bị đầu cuối tài chính và trung tâm điều hành; duy trì sự rõ ràng về mặt phân cấp thị giác và kiểm soát tải nhận thức của người vận hành.

## 2. When to Use
- Khi xây dựng giao diện giám sát viễn thám, sàn giao dịch tài chính, hoặc bảng điều khiển DevOps (NOC/SOC).
- Khi người dùng cần quan sát đồng thời hàng chục biểu đồ, bảng dữ liệu, và chỉ số KPI mà không phải cuộn trang liên tục.
- Khi cần hỗ trợ chế độ xem đa màn hình và kích thước lưới linh hoạt (bố cục widget tùy biến).

## 3. When NOT to Use
- Khi phát triển ứng dụng tiêu dùng (B2C) hoặc mobile onboarding đòi hỏi giao diện tối giản, nhiều khoảng trắng thoáng.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Danh sách widget dữ liệu, tần suất cập nhật dữ liệu thời gian thực, chuẩn kích thước màn hình người dùng mục tiêu.
- **Quyền hạn truy cập:** Quyền sửa đổi component layout và hệ thống Grid.

## 5. Core Concepts & Taxonomy
- **Information Density vs. Cognitive Overload:** Mật độ thông tin cao không đồng nghĩa với lộn xộn; cần áp dụng quy tắc nhóm thị giác (Gestalt Law of Proximity) và viền phân cách vi mô.
- **Virtual Widget Rendering:** Chỉ render các ô widget nằm trong khung nhìn hiển thị để tiết kiệm CPU/DOM nodes.
- **Data Sparklines & Micro-Visualizations:** Sử dụng biểu đồ đường mini không trục để tóm tắt xu hướng mà không chiếm diện tích quý giá.

## 6. Step-by-Step Execution Workflow
1. Xác định phân cấp độ ưu tiên của các luồng thông tin: Chỉ số cốt lõi (Tier 1), Biểu đồ xu hướng (Tier 2), Bảng chi tiết (Tier 3).
2. Thiết lập hệ thống lưới CSS Grid 12 hoặc 24 cột với rãnh (gutters) nhỏ gọn (8px hoặc 12px).
3. Tối ưu kích thước khoảng đệm (padding) trong các cell dữ liệu và áp dụng bảng màu trung tính cho khung chứa.
4. Triển khai kỹ thuật virtual rendering cho các bảng dữ liệu hàng nghìn dòng bên trong widget.
5. Áp dụng debounce và throttle cho các cập nhật thời gian thực qua WebSocket để tránh giật lag render.
6. Cung cấp phím tắt bàn phím và khả năng phóng to toàn màn hình (Focus Mode) cho từng widget riêng lẻ.

## 7. Concrete Examples
### Bố cục Dashboard mật độ cao bằng CSS Grid:
```css
.dashboard-grid {
  display: grid;
  grid-template-columns: repeat(12, minmax(0, 1fr));
  gap: 8px; /* Rãnh gọn gàng cho mật độ hiển thị cao */
  padding: 8px;
  background-color: var(--color-surface-sunken);
}

.widget-kpi {
  grid-column: span 3;
  padding: 8px 12px;
  background: var(--color-surface-card);
  border: 1px solid var(--color-border-subtle);
  border-radius: 4px;
}

.widget-chart-large {
  grid-column: span 8;
  height: 320px;
}

.widget-feed-stream {
  grid-column: span 4;
  height: 320px;
  overflow-y: auto;
}
```

## 8. Anti-Patterns & Common Traps
- **Color Rainbow Saturation:** Dùng quá nhiều màu sắc rực rỡ khiến mắt người dùng bị mỏi và không phân biệt được cảnh báo khẩn cấp.
- **DOM Tree Explosion:** Render hàng nghìn thẻ HTML div lồng nhau cho mỗi hàng dữ liệu làm đơ giao diện khi có luồng dữ liệu mới.
- **Layout Shifting on Live Push:** Cập nhật số liệu làm thay đổi chiều rộng widget khiến toàn bộ lưới dashboard bị giật nhảy liên tục.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Tốc độ khung hình duy trì ổn định >= 55 FPS khi nhận cập nhật dữ liệu 10 lần/giây.
- **QG-03**: Tất cả các màu sắc cảnh báo (Critical, Warning, Normal) đều có sự khác biệt rõ rệt về độ sáng và biểu tượng đi kèm (không phụ thuộc hoàn toàn vào màu sắc).
- **QG-08**: Số lượng DOM nodes trên toàn trang không vượt quá 2,500 nodes tại bất kỳ thời điểm nào.

## 10. Security & Safety Boundaries
- Khử khuẩn dữ liệu thời gian thực (XSS sanitization) trước khi hiển thị vào các feed stream của dashboard.

## 11. Platform Adapters
- **Layout & Virtualization**: CSS Grid, TanStack Virtual, React-Grid-Layout, ECharts, uPlot.

## 12. Deliverables & Output Artifacts
- Cấu trúc component Grid Dashboard responsive.
- Bộ stylesheet tối ưu mật độ hiển thị (High-Density Theme).
- Benchmark hiệu năng render dữ liệu thời gian thực.

## 13. Related & Complementary Skills
dex-virtualized-infinite-lists, dex-perceived-performance-patterns, dex-chart-visualization-accessibility

## 14. Realistic Usage Example
```powershell
# Đo số lượng DOM nodes và FPS khi nhận live data
npx playwright test tests/perf/high-density-dashboard.spec.ts

# Kiểm tra hiệu năng render bằng Chrome DevTools trace
npx lighthouse http://localhost:3000/dashboard --preset=desktop --view
```
