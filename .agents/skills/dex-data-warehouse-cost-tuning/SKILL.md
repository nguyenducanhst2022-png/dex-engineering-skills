---
name: dex-data-warehouse-cost-tuning
description: Analyze and optimize BigQuery, Snowflake, and Databricks query compute costs, partition pruning, clustering strategies, slot reservations, and auto-suspend warehouse policies. Use when curtailing runaway cloud data warehouse spending without impacting analytics SLAs.
---

# dex-data-warehouse-cost-tuning

## 1. Purpose & Scope
Phân tích, kiểm toán và tối ưu hóa chi phí tính toán trên các kho dữ liệu đám mây (Cloud Data Warehouse Cost Tuning) như Google BigQuery, Snowflake và Databricks; ứng dụng kỹ thuật cắt tỉa phân vùng (Partition Pruning), gom cụm dữ liệu (Clustering), cấp phát slot tính toán và chính sách tự động ngủ đông kho dữ liệu; cắt giảm tối thiểu 40% chi phí hóa đơn hàng tháng mà không ảnh hưởng đến cam kết thời gian hoàn thành truy vấn (SLA).

## 2. When to Use
- Khi hóa đơn chi phí BigQuery/Snowflake tăng vọt bất thường vượt quá ngân sách của doanh nghiệp.
- Khi các câu lệnh truy vấn quét qua toàn bộ bảng dữ liệu hàng chục Terabyte một cách lãng phí.
- Khi cần thiết lập hạn ngạch chi phí (Cost Quotas) và cảnh báo cho từng đội nhóm kỹ thuật.

## 3. When NOT to Use
- Khi kho dữ liệu chỉ có dung lượng nhỏ dưới 10GB với chi phí vài đô la mỗi tháng.
- Khi tối ưu hóa cơ sở dữ liệu giao dịch MySQL/PostgreSQL cục bộ.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Quyền xem bảng nhật ký chi phí `INFORMATION_SCHEMA.JOBS_BY_PROJECT` (BigQuery) hoặc `SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY`, hiểu biết về mô hình tính giá điện toán đám mây.
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; bảo vệ toàn vẹn tài sản kỹ nghệ và dữ liệu sản xuất.

## 5. Core Concepts & Taxonomy
- **Partition Pruning:** Cấu hình bảng phân vùng theo ngày (`PARTITION BY DATE(created_at)`) để câu lệnh truy vấn chỉ đọc đúng thư mục ngày cần thiết, giảm 95% số byte bị quét.
- **Clustering Strategy:** Sắp xếp dữ liệu vật lý theo các cột thường xuyên dùng để lọc (`CLUSTER BY tenant_id, status`), giúp công cụ bỏ qua các khối dữ liệu không liên quan.
- **Auto-Suspend & Auto-Resume:** Cấu hình Snowflake Warehouse tự động tắt sau 60 giây không có truy vấn để triệt tiêu chi phí máy chủ nhàn rỗi.

## 6. Step-by-Step Execution Workflow
1. Truy vấn bảng lịch sử để tìm ra top 10 câu lệnh SQL tiêu tốn nhiều chi phí nhất trong tháng.
2. Kiểm tra xem câu lệnh có quét toàn bộ bảng (Full Table Scan) do thiếu điều kiện phân vùng hay không.
3. Tái cấu trúc bảng dữ liệu: áp dụng phân vùng theo ngày và gom cụm theo các khóa ngoại phổ biến.
4. Bắt buộc người dùng phải có mệnh đề lọc trên cột phân vùng bằng cờ `require_partition_filter = true`.
5. Lập báo cáo tổng kết chi phí tiết kiệm `DATA_WAREHOUSE_COST_AUDIT.md`.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```sql
-- BigQuery Partition & Cluster Optimization Example
CREATE OR REPLACE TABLE `my_project.analytics.user_events`
PARTITION BY DATE(event_timestamp)
CLUSTER BY tenant_id, event_type
OPTIONS (
  require_partition_filter = TRUE,
  partition_expiration_days = 365
) AS
SELECT * FROM `my_project.staging.raw_events`;

-- Cost-Audit: Find most expensive queries in last 7 days
SELECT 
  query,
  user_email,
  ROUND(total_bytes_billed / 1024 / 1024 / 1024 / 1024, 2) AS tb_billed,
  ROUND((total_bytes_billed / 1024 / 1024 / 1024 / 1024) * 6.25, 2) AS estimated_cost_usd
FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE creation_time > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
ORDER BY total_bytes_billed DESC LIMIT 10;
```

## 8. Anti-Patterns & Common Traps
- Chạy lệnh `SELECT * FROM table` trên BigQuery mà không chỉ định danh sách cột (BigQuery là Columnar Storage, lệnh này sẽ quét toàn bộ dữ liệu của tất cả các cột).
- Cấu hình Snowflake Warehouse ở kích thước `X-Large` cho các tác vụ phân tích nhỏ và để thời gian chờ tự tắt là 30 phút.
- Không đặt giới hạn ngân sách tối đa trên từng dự án, dẫn đến một câu lệnh SQL sai của thực tập sinh có thể làm tốn hàng nghìn USD trong vài phút.

## 9. Quality Gates & Acceptance Criteria
- QG-01: 100% các bảng dữ liệu lớn hơn 100GB đều được cấu hình Partition và Cluster.
- QG-02: Bật cờ bắt buộc lọc phân vùng `require_partition_filter` trên toàn bộ bảng nhật ký sự kiện.
- QG-03: Chi phí hóa đơn truy vấn kho dữ liệu giảm tối thiểu 35% ngay trong tháng đầu tiên áp dụng.

## 10. Security & Safety Boundaries
- Phân quyền hạn ngạch chi phí truy vấn theo nhóm người dùng (Query Cost Limits) để ngăn ngừa việc tiêu tốn ngân sách công ty do sơ suất.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Báo cáo kiểm toán và tối ưu chi phí kho dữ liệu `DATA_WAREHOUSE_COST_AUDIT.md`.
1. Bộ script tái cấu trúc phân vùng và gom cụm bảng dữ liệu.

## 13. Related & Complementary Skills
- [`dex-database-query-plans`](.agents/skills/dex-database-query-plans/SKILL.md)
- [`dex-capacity-planning`](.agents/skills/dex-capacity-planning/SKILL.md)
- [`dex-sql-metric-semantic-layer`](.agents/skills/dex-sql-metric-semantic-layer/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Doanh nghiệp giật mình khi hóa đơn Google Cloud BigQuery tăng vọt từ $3,000 lên $28,000 trong một tháng do dashboard BI quét qua toàn bộ bảng lịch sử 5 năm mỗi 5 phút. Kỹ sư kích hoạt `dex-data-warehouse-cost-tuning`, tìm ra câu query thủ phạm, cấu hình phân vùng bảng theo ngày và thêm bộ lọc thời gian 7 ngày gần nhất, đưa hóa đơn trở về mức $2,400/tháng.
