---
name: dex-sql-metric-semantic-layer
description: Engineer reusable business metric semantic layers (Cube, dbt Semantic Layer, MetricFlow) defining standardized dimensions, measures, time grains, and access policies. Use when eliminating conflicting business metric calculations across BI dashboards and AI query agents.
---

# dex-sql-metric-semantic-layer

## 1. Purpose & Scope
Thiết kế và hiện thực hóa tầng ngữ nghĩa chỉ số kinh doanh (SQL Metric Semantic Layer) sử dụng Cube, dbt Semantic Layer hoặc MetricFlow; chuẩn hóa các định nghĩa chiều dữ liệu (Dimensions), chỉ số đo lường (Measures), độ hạt thời gian (Time Grains) và chính sách kiểm soát truy cập; loại bỏ hoàn toàn hiện tượng xung đột công thức tính toán giữa các dashboard BI và các AI Query Agents.

## 2. When to Use
- Khi các phòng ban khác nhau (Tài chính, Marketing, Sản phẩm) đưa ra các con số doanh thu hoặc tỷ lệ churn khác nhau do viết SQL tự do.
- Khi xây dựng giao diện Text-to-SQL cho AI Agent truy vấn dữ liệu kinh doanh an toàn.
- Khi cần quản trị tập trung công thức tính toán các chỉ số KPI trọng yếu của doanh nghiệp.

## 3. When NOT to Use
- Khi hệ thống chỉ có một báo cáo đơn giản duy nhất không có sự phân kỳ số liệu.
- Khi thực hiện các truy vấn kỹ thuật nội bộ của hệ thống giám sát hạ tầng máy chủ.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Kho dữ liệu (Snowflake, BigQuery hoặc ClickHouse), công cụ tầng ngữ nghĩa (dbt hoặc Cube.js), kho mã nguồn kiểm soát phiên bản Git.
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; bảo vệ toàn vẹn tài sản kỹ nghệ và dữ liệu sản xuất.

## 5. Core Concepts & Taxonomy
- **Single Source of Metric Truth:** Định nghĩa chỉ số kinh doanh một lần duy nhất dưới dạng mã nguồn (Code-as-Metric) thay vì viết lặp lại trong từng công cụ BI.
- **Dimension & Measure Modeling:** Phân biệt rõ giữa Measure (tính toán cộng dồn: `SUM(amount)`) và Dimension (thuộc tính phân loại: `country`, `user_tier`).
- **Granularity & Additivity:** Đảm bảo các chỉ số đo lường không bị tính toán sai (Double Counting) khi gom nhóm theo các mốc thời gian khác nhau.

## 6. Step-by-Step Execution Workflow
1. Xác định danh mục chỉ số nghiệp vụ cốt lõi cần chuẩn hóa (ví dụ: `Monthly Recurring Revenue - MRR`).
2. Viết tệp khai báo ngữ nghĩa chuẩn bằng định dạng YAML (dbt Semantic Layer specification).
3. Định nghĩa các phép nối dữ liệu (Joins) an toàn giữa các mô hình dữ liệu để chống lỗi Cartesian Product.
4. Tích hợp tầng ngữ nghĩa vào giao diện truy vấn của AI Agent hoặc cổng BI.
5. Kiểm thử tính nhất quán của kết quả trả về khi truy vấn qua nhiều chiều phân tích khác nhau.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```yaml
# dbt Semantic Layer Metric Definition
version: 2

semantic_models:
  - name: revenue_orders
    model: ref('fct_orders')
    entities:
      - name: order_id
        type: primary
      - name: customer_id
        type: foreign
    dimensions:
      - name: order_date
        type: time
        type_params:
          time_granularity: day
      - name: order_status
        type: categorical
    measures:
      - name: net_revenue
        agg: sum
        expr: amount - discount_amount

metrics:
  - name: total_net_revenue
    label: "Total Net Revenue ($)"
    type: simple
    type_params:
      measure: net_revenue
```

## 8. Anti-Patterns & Common Traps
- Để mỗi nhân viên tự viết câu lệnh `SUM(sales)` trong Tableau hay Metabase dẫn đến mỗi báo cáo ra một con số doanh thu khác nhau.
- Cho phép AI Text-to-SQL tự do sinh câu lệnh SQL thô nối các bảng mà không qua tầng ngữ nghĩa kiểm soát.
- Định nghĩa chỉ số có phép chia tỷ lệ phần trăm nhưng lại cộng dồn trực tiếp (`AVG` trên các tỷ lệ phần trăm đã tính sẵn).

## 9. Quality Gates & Acceptance Criteria
- QG-01: 100% các chỉ số KPI doanh nghiệp được định nghĩa tập trung bằng file YAML trong kho Git.
- QG-02: Kết quả tính toán từ tầng ngữ nghĩa khớp chính xác tuyệt đối với báo cáo tài chính đã kiểm toán.
- QG-03: Không có câu truy vấn nào sinh ra lỗi vòng lặp join hoặc nhân bản dữ liệu ngoài ý muốn.

## 10. Security & Safety Boundaries
- Áp dụng chính sách bảo mật dữ liệu ở cấp độ hàng (Row-Level Security) trực tiếp trong tầng ngữ nghĩa để ngăn chặn lộ dữ liệu nhạy cảm.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Bộ tệp định nghĩa chỉ số ngữ nghĩa `metrics_model.yml`.
1. Tài liệu từ điển chỉ số kinh doanh chuẩn hóa `METRICS_DICTIONARY.md`.

## 13. Related & Complementary Skills
- [`dex-database-query-plans`](.agents/skills/dex-database-query-plans/SKILL.md)
- [`dex-data-contracts`](.agents/skills/dex-data-contracts/SKILL.md)
- [`dex-analytics-instrumentation`](.agents/skills/dex-analytics-instrumentation/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Ban giám đốc họp khẩn vì báo cáo của phòng Marketing ghi nhận doanh thu tháng là 10 tỷ VND trong khi phòng Kế toán báo chỉ có 8.5 tỷ VND. Kỹ sư kích hoạt `dex-sql-metric-semantic-layer`, phát hiện phòng Marketing chưa trừ tiền hoàn đơn và chiết khấu voucher. Chuẩn hóa công thức `net_revenue` vào dbt Semantic Layer, đưa tất cả báo cáo về cùng một con số duy nhất.
