---
name: dex-analytics-cohort-retention
description: Engineer scalable user retention cohort matrices, churn decay curves, lifetime value (LTV) projections, and behavioral cohort segmentation in SQL. Use when evaluating product-market fit, subscription health, or marketing acquisition quality.
---

# dex-analytics-cohort-retention

## 1. Purpose & Scope
Thiết kế và hiện thực hóa ma trận phân tích thuần tập (User Cohort Retention Matrices), đường cong suy giảm rời bỏ (Churn Decay Curves), mô hình dự phóng giá trị trọn đời (Customer Lifetime Value - LTV) và phân khúc hành vi khách hàng bằng câu lệnh SQL tối ưu hóa; phục vụ đánh giá mức độ phù hợp sản phẩm - thị trường (Product-Market Fit), sức khỏe dịch vụ thuê bao và chất lượng kênh chuyển đổi.

## 2. When to Use
- Khi ban giám đốc cần đánh giá xem người dùng mới có tiếp tục quay lại sử dụng sản phẩm sau 7 ngày, 30 ngày, 90 ngày hay không.
- Khi so sánh chất lượng người dùng đến từ các chiến dịch quảng cáo khác nhau để tối ưu chi phí thu hút khách hàng (CAC).
- Khi xây dựng bảng điều khiển phân tích số liệu tăng trưởng cho các quỹ đầu tư mạo hiểm.

## 3. When NOT to Use
- Khi phân tích các giao dịch bán hàng một lần không có sự quay lại của người dùng (One-off e-commerce).
- Khi xử lý nhật ký lỗi kỹ thuật của hệ thống máy chủ.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Kho dữ liệu chứa bảng nhật ký hoạt động người dùng (`user_events` hoặc `logins`), kỹ thuật SQL nâng cao (Window Functions, CTE).
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; bảo vệ toàn vẹn tài sản kỹ nghệ và dữ liệu sản xuất.

## 5. Core Concepts & Taxonomy
- **Acquisition Cohort:** Gom nhóm người dùng dựa trên tuần hoặc tháng đầu tiên họ đăng ký tài khoản.
- **Retention Matrix:** Bảng ma trận hình tam giác hiển thị tỷ lệ phần trăm người dùng trong mỗi thuần tập còn hoạt động ở các chu kỳ tiếp theo (Day 0, Day 1, Day 7, Day 30).
- **Flattening Retention Curve:** Dấu hiệu vàng của Product-Market Fit là khi đường cong giữ chân người dùng đi ngang song song với trục hoành thay vì cắm thẳng xuống 0.

## 6. Step-by-Step Execution Workflow
1. Xác định hành động có ý nghĩa cốt lõi (Core Meaningful Action, ví dụ: 'Tạo tài liệu mới' thay vì chỉ 'Đăng nhập').
2. Xác định thời điểm gia nhập của từng người dùng (`cohort_month`).
3. Tính toán khoảng cách chu kỳ thời gian giữa hoạt động tiếp theo và thời điểm gia nhập (`period_number`).
4. Viết câu lệnh SQL gom nhóm và tính tỷ lệ phần trăm giữ chân cho từng ô trong ma trận.
5. Xuất dữ liệu ma trận trực quan hóa thành đồ thị nhiệt (Heatmap) và đường cong suy giảm.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```sql
-- Scalable Monthly Cohort Retention Matrix in SQL
WITH user_cohort AS (
  SELECT user_id, DATE_TRUNC('month', MIN(created_at)) AS cohort_month
  FROM users GROUP BY user_id
),
user_activities AS (
  SELECT DISTINCT e.user_id, DATE_TRUNC('month', e.event_timestamp) AS activity_month
  FROM events e WHERE e.event_name = 'completed_transaction'
)
SELECT 
  c.cohort_month,
  COUNT(DISTINCT c.user_id) AS total_cohort_size,
  (DATE_PART('year', a.activity_month) - DATE_PART('year', c.cohort_month)) * 12 +
  (DATE_PART('month', a.activity_month) - DATE_PART('month', c.cohort_month)) AS month_number,
  ROUND(COUNT(DISTINCT a.user_id)::NUMERIC / COUNT(DISTINCT c.user_id) * 100, 2) AS retention_rate_pct
FROM user_cohort c
LEFT JOIN user_activities a ON c.user_id = a.user_id
GROUP BY 1, 3 ORDER BY 1, 3;
```

## 8. Anti-Patterns & Common Traps
- Định nghĩa 'hoạt động' chỉ là việc người dùng nhận được một email marketing tự động thay vì họ chủ động mở ứng dụng tương tác.
- Gộp chung toàn bộ người dùng vào một đường cong duy nhất, che giấu sự thật là các bản phát hành mới đang làm giảm trải nghiệm người dùng.
- Viết câu truy vấn SQL lồng nhau quá nhiều tầng không có chỉ mục khiến câu lệnh chạy mất hàng tiếng trên BigQuery.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Câu truy vấn ma trận thuần tập thực thi dưới 15 giây trên bảng dữ liệu 50 triệu sự kiện.
- QG-02: Tỷ lệ giữ chân ở Month 0 luôn đạt chính xác 100.0%.
- QG-03: Số liệu đối soát khớp hoàn toàn với bảng báo cáo tài chính doanh thu định kỳ.

## 10. Security & Safety Boundaries
- Ẩn danh hóa ID người dùng (Hashing user_id) trước khi trích xuất dữ liệu ma trận phục vụ báo cáo đối tác bên ngoài.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Mẫu câu lệnh SQL phân tích thuần tập chuẩn hóa `cohort_retention_matrix.sql`.
1. Biểu đồ nhiệt phân tích tỷ lệ giữ chân khách hàng `retention-heatmap.json`.

## 13. Related & Complementary Skills
- [`dex-sql-metric-semantic-layer`](.agents/skills/dex-sql-metric-semantic-layer/SKILL.md)
- [`dex-dashboard-data-storytelling`](.agents/skills/dex-dashboard-data-storytelling/SKILL.md)
- [`dex-analytics-instrumentation`](.agents/skills/dex-analytics-instrumentation/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Một startup công nghệ chuẩn bị gọi vốn vòng Series A. Nhà đầu tư yêu cầu cung cấp ma trận thuần tập giữ chân 12 tháng gần nhất. Kỹ sư kích hoạt `dex-analytics-cohort-retention`, viết query SQL tối ưu trên Snowflake, trích xuất ma trận Retention hoàn chỉnh chứng minh tỷ lệ giữ chân tháng thứ 6 ổn định ở mức 42% (chỉ số xuất sắc trong ngành), giúp công ty gọi vốn thành công.
