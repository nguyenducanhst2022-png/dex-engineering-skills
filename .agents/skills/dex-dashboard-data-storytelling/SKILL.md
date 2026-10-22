---
name: dex-dashboard-data-storytelling
description: Architect analytical dashboard layouts that convey data stories, prioritize high-value KPI metrics, separate operational signals from decorative charts, and facilitate decision-making. Use when building enterprise BI portals, executive dashboards, or telemetry interfaces.
---

# dex-dashboard-data-storytelling

## 1. Purpose & Scope
Thiết kế kiến trúc bảng điều khiển (Dashboard) và trực quan hóa dữ liệu theo lối kể chuyện (Data Storytelling); tổ chức phân cấp các chỉ số KPI then chốt, tách bạch tín hiệu vận hành thực tế khỏi các biểu đồ trang trí vô ích, giúp người dùng ra quyết định nhanh chóng và chuẩn xác.

## 2. When to Use
- Khi xây dựng bảng điều khiển quản trị (Executive Dashboard) hoặc cổng phân tích dữ liệu BI.
- Khi người dùng phàn nàn dashboard có quá nhiều đồ thị nhưng không biết thông tin nào cần hành động ngay.
- Khi thiết kế hệ thống giám sát cảnh báo và telemetry thời gian thực.

## 3. When NOT to Use
- Khi xây dựng các biểu mẫu nhập liệu CRUD thông thường.
- Khi xử lý logic truy vấn SQL dưới tầng cơ sở dữ liệu.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Danh sách các chỉ số kinh doanh mục tiêu, tần suất cập nhật dữ liệu, vai trò người xem (Giám đốc, Kỹ sư vận hành, Nhân viên phân tích).
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn trong phạm vi dự án, không can thiệp vào tài nguyên sản xuất khi chưa có phê duyệt.

## 5. Core Concepts & Taxonomy
- **Inverted Pyramid of Information:** Đặt số liệu tổng quan (High-level KPIs) ở trên cùng, xu hướng ở giữa và chi tiết giao dịch ở dưới.
- **Chart-to-Data Matching:** Chọn đúng loại biểu đồ (Line chart cho xu hướng thời gian, Bar chart cho so sánh danh mục, Bullet chart cho mục tiêu).
- **Cognitive Load Reduction:** Loại bỏ rác biểu đồ (Chartjunk) như lưới quá đậm, bóng đổ thừa thãi hoặc 3D không cần thiết.

## 6. Step-by-Step Execution Workflow
1. Xác định câu hỏi kinh doanh cốt lõi mà dashboard cần giải đáp trong 5 giây đầu tiên.
2. Thiết kế thẻ tóm tắt chỉ số chính (Hero KPI Cards) kèm chỉ báo phần trăm biến động so với kỳ trước.
3. Lựa chọn loại biểu đồ trực quan chính xác và áp dụng bảng màu dữ liệu có chủ đích (Màu xám cho bối cảnh, màu nổi bật cho ngoại lệ).
4. Tạo cơ chế lọc dữ liệu tương tác (date range, categories) đồng bộ trên tất cả biểu đồ.
5. Kiểm tra khả năng giải thích dữ liệu với người dùng thực tế.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```typescript
// KPI Metric Visual Model Contract
export interface DashboardMetricSummary {
  metricId: string;
  label: string;
  currentValue: number;
  formattedValue: string;
  changeRate: number; // e.g. +0.125 for +12.5%
  trendDirection: 'upward' | 'downward' | 'neutral';
  isAnomaly: boolean;
  sparklinePoints: number[];
}
```

## 8. Anti-Patterns & Common Traps
- Sử dụng biểu đồ tròn (Pie chart) có nhiều hơn 5 lát cắt khiến người xem không thể so sánh tỷ lệ chính xác.
- Dùng biểu đồ 3D làm méo mó góc nhìn dữ liệu thực tế.
- Trộn lẫn quá nhiều màu sắc rực rỡ không đồng nhất khiến người dùng tưởng nhầm mọi dữ liệu đều đang bị cảnh báo lỗi.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Chỉ số KPI quan trọng nhất được định vị tại vị trí ưu tiên góc trên bên trái màn hình.
- QG-02: Mỗi biểu đồ đều có tiêu đề rõ ràng, đơn vị đo lường và ghi chú nguồn dữ liệu.
- QG-03: Trực quan hóa dữ liệu hiển thị tốt ở độ phân giải tiêu chuẩn 1366x768 mà không bị cắt cụt trục số.

## 10. Security & Safety Boundaries
- Áp dụng cơ chế phân quyền xem dữ liệu theo vai trò (Role-Based Row Level Security) để không làm lộ số liệu nhạy cảm trên dashboard.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Bản thiết kế cấu trúc dashboard `dashboard.architecture.json`.
1. Hướng dẫn trực quan hóa dữ liệu và lựa chọn biểu đồ cho hệ thống.

## 13. Related & Complementary Skills
- [`dex-visual-hierarchy-audit`](.agents/skills/dex-visual-hierarchy-audit/SKILL.md)
- [`dex-layout-composition-patterns`](.agents/skills/dex-layout-composition-patterns/SKILL.md)
- [`dex-analytics-instrumentation`](.agents/skills/dex-analytics-instrumentation/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Phát triển dashboard tài chính cho ban giám đốc. Áp dụng `dex-dashboard-data-storytelling` để dọn dẹp 15 biểu đồ hỗn loạn, quy hoạch lại thành 3 thẻ KPI doanh thu - chi phí - lợi nhuận ở đầu trang, kèm một biểu đồ vùng so sánh kế hoạch và một bảng drill-down chi tiết giao dịch bất thường.
