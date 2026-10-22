---
name: dex-feature-adoption-analysis
description: Measure, segment, and evaluate post-release feature adoption, retention curves, and engagement depth across user cohorts. Use to make data-driven decisions on whether to iterate, pivot, or sunset product features.
---

# dex-feature-adoption-analysis

## 1. Purpose & Scope
Đo lường, phân đoạn và đánh giá mức độ đón nhận tính năng sau phát hành (Feature Adoption & Engagement Analysis); xây dựng đường cong duy trì sử dụng (Retention Curves), đo lường độ sâu tương tác (Breadth, Depth, Frequency) và phân tích hành vi theo các nhóm thuần tập (Cohorts), cung cấp căn cứ dữ liệu xác thực để quyết định tiếp tục tối ưu hóa, chuyển hướng hay loại bỏ (sunset) tính năng.

## 2. When to Use
- Sau khi phát hành một tính năng lớn được 30-90 ngày và cần đánh giá hiệu quả thực tế.
- Đưa ra quyết định có nên loại bỏ một tính năng cũ ít người dùng để giảm nợ kỹ thuật (Technical Debt) hay không.
- Tìm hiểu xem nhóm khách hàng mang lại doanh thu cao nhất (Power Users) sử dụng tính năng theo cách nào.

## 3. When NOT to Use
- Không đánh giá mức độ thành công của tính năng chỉ dựa trên số lượt click mở ra xem thử trong ngày đầu tiên phát hành (cần đo lường tỉ lệ người dùng quay lại sử dụng sau 7 và 30 ngày).
- Không áp dụng chỉ tiêu adoption giống nhau cho tính năng dùng hàng ngày (Chat) và tính năng chỉ dùng định kỳ hàng năm (Kê khai thuế).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Lịch sử sự kiện tương tác với tính năng trong 90 ngày qua.
- Thuộc tính phân loại người dùng (User Role, Công ty, Gói cước Free/Enterprise).
- Mục tiêu sử dụng kỳ vọng (Expected Usage Frequency).
- **Điều kiện tiên quyết**:
- Tính năng đã có gắn cờ Feature Flag hoặc mã tracking sự kiện từ ngày đầu ra mắt.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Khung đo lường BDF Framework:
  + Breadth (Độ rộng): Bao nhiêu phần trăm tổng số người dùng đã sử dụng tính năng ít nhất một lần?
  + Depth (Độ sâu): Những người sử dụng tính năng đó dùng nó nhiều như thế nào (số lần/ngày)?
  + Frequency (Tần suất): Người dùng quay lại sử dụng tính năng đó đều đặn theo chu kỳ nào (Daily, Weekly, Monthly)?
- Churn Curve Flattening: Nếu đường cong duy trì sử dụng (Retention Curve) đi ngang (Flatten) ở một tỉ lệ nhất định (ví dụ 25%), tính năng đó đã tìm được Product-Market Fit trong một nhóm người dùng cốt lõi.
- **Quy tắc quyết định kỹ thuật**:
- Nếu một tính năng sau 90 ngày chỉ có < 1% người dùng hoạt động và tốn nhiều công bảo trì: lập kế hoạch Deprecate và Sunset.
- Nếu một tính năng có Depth cao ở nhóm khách hàng Enterprise nhưng Breadth thấp: tập trung cải thiện giao diện Onboarding để nhiều người khám phá ra nó hơn.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Tiếp tục dồn tài nguyên kỹ thuật để nâng cấp một tính năng phức tạp mà dữ liệu cho thấy không ai thực sự cần đến nó.

## 6. Step-by-Step Execution Workflow
1. Xác định hành động kích hoạt cốt lõi (Core Activation Action) của tính năng.
2. Tạo bảng phân tích nhóm thuần tập theo tuần kể từ ngày người dùng bắt đầu dùng tính năng.
3. Tính toán tỉ lệ người dùng quay lại ở Ngày 1, Ngày 7 và Ngày 30 (D1, D7, D30 Retention).
4. Phân đoạn nhóm người dùng nhiệt thành (Power Users) để tìm hiểu điểm khác biệt trong quy trình làm việc của họ.
5. Xuất báo cáo đánh giá ROI và đề xuất phương án hành động (Iterate, Maintain, or Sunset).

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```sql
-- Truy vấn SQL phân tích tỉ lệ Retention theo tuần của tính năng mới
WITH feature_first_use AS (
    SELECT user_id, MIN(DATE_TRUNC('week', event_time)) AS cohort_week
    FROM analytics_events
    WHERE event_name = 'ai_summary_generated'
    GROUP BY user_id
),
activity AS (
    SELECT f.user_id, f.cohort_week, 
           DATE_PART('week', a.event_time) - DATE_PART('week', f.cohort_week) AS week_number
    FROM feature_first_use f
    JOIN analytics_events a ON f.user_id = a.user_id
    WHERE a.event_name = 'ai_summary_generated'
)
SELECT cohort_week, week_number, COUNT(DISTINCT user_id) AS active_users
FROM activity
GROUP BY cohort_week, week_number
ORDER BY cohort_week, week_number;
```

### Lệnh xác minh & thực thi:
```bash
# Chạy script xuất biểu đồ Heatmap phân tích Cohort Retention
python scripts/generate_cohort_report.py --feature ai_summary
```

## 8. Anti-Patterns & Common Traps
- Đo lường thành công bằng 'Vanity Metrics' (như tổng số lượt xem trang) thay vì đo lường người dùng quay lại thường xuyên.
- Ngại ngùng không dám xóa bỏ các tính năng thừa đã chết khiến codebase ngày càng phình to và khó bảo trì.

## 9. Quality Gates & Acceptance Criteria
- Đường cong duy trì sử dụng D30 Retention phải đi ngang và đạt tối thiểu 20% đối với các tính năng cốt lõi.
- Báo cáo Adoption hoàn thành và trình bày trước Product Council sau 60 ngày kể từ khi release.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Dữ liệu phân tích hành vi người dùng phải được tổng hợp ẩn danh (Aggregated metrics) không để lộ danh tính cá nhân.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ sinh thái AI / UX**: Hỗ trợ Model Context Protocol (MCP), LangChain/LlamaIndex, Figma, Playwright axe-core.

## 12. Deliverables & Output Artifacts
- Báo cáo phân tích mức độ đón nhận tính năng (Feature Adoption Report).
- Biểu đồ đường cong Cohort Retention và đề xuất lộ trình phát triển tiếp theo.

## 13. Related & Complementary Skills
dex-conversion-funnel-analysis, dex-product-requirements-writing, dex-user-consent-ux

## 14. Realistic Usage Example
### Tình huống thực tế:
Một ứng dụng quản lý dự án ra mắt tính năng 'Biểu đồ Gantt 3D'. Sau 60 ngày, phân tích số liệu cho thấy chỉ có 0.4% người dùng sử dụng và 90% trong số họ không bao giờ mở lại lần thứ hai. Đội ngũ đã quyết định dũng cảm loại bỏ tính năng này, giải phóng 15,000 dòng code phức tạp và tập trung kỹ sư vào việc tối ưu hóa bảng Kanban 2D được 80% người dùng yêu thích.
