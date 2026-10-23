---
name: dex-metadata-catalog-lineage
description: Build automated data cataloging, column-level data lineage, and schema governance pipelines across modern data architectures. Use when implementing data mesh governance and data impact analysis.
---

# dex-metadata-catalog-lineage

## 1. Purpose & Scope
Xây dựng hệ thống danh mục siêu dữ liệu tự động (Metadata Catalog), truy vết nguồn gốc dữ liệu đến cấp cột (Column-Level Data Lineage) và quản trị lược đồ (Schema Governance); phục vụ phân tích tác động thay đổi (Impact Analysis) và quản trị kiến trúc Data Mesh.

## 2. When to Use
- Khi chuẩn bị sửa đổi một cột trong bảng cơ sở dữ liệu nguồn nhưng không rõ có những báo cáo BI hoặc dashboard nào bị ảnh hưởng.
- Khi cần chứng minh nguồn gốc dữ liệu (Data Provenance) phục vụ các tiêu chuẩn tuân thủ bảo vệ dữ liệu (GDPR, CCPA, Basel III).
- Khi triển khai mô hình quản trị dữ liệu liên kết (Federated Data Governance) trên nhiều nhóm kỹ thuật.

## 3. When NOT to Use
- Khi ứng dụng chỉ là một dịch vụ web đơn lẻ sử dụng 3 bảng cơ sở dữ liệu nội bộ không có luồng ETL/ELT.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Kho dữ liệu (Snowflake, BigQuery, Databricks), công cụ ETL (dbt, Airflow, Spark), metadata store.
- **Quyền hạn truy cập:** Quyền đọc siêu dữ liệu hệ thống (Information Schema, query history logs).

## 5. Core Concepts & Taxonomy
- **Column-Level Lineage:** Khả năng truy vết chính xác nguồn gốc của một cột trong báo cáo cuối cùng được tổng hợp từ những cột cụ thể nào của các bảng gốc ban đầu.
- **OpenLineage Standard:** Chuẩn mở định dạng sự kiện thu thập lineage phục vụ trao đổi thông tin giữa các hệ thống (Spark, Airflow, Flink).
- **Data Contract:** Thỏa thuận có cấu trúc ràng buộc giữa đội ngũ sản xuất dữ liệu (Data Producer) và đội ngũ tiêu thụ dữ liệu (Data Consumer).

## 6. Step-by-Step Execution Workflow
1. Thu thập siêu dữ liệu tự động từ các nguồn: cơ sở dữ liệu quan hệ, data warehouse, dbt manifest, và Airflow DAGs.
2. Phân tích cú pháp các câu lệnh SQL (SQL AST Parsing bằng sqlglot) để trích xuất quan hệ phụ thuộc giữa các bảng và cột.
3. Đóng gói thông tin thành các sự kiện OpenLineage và đẩy về máy chủ Metadata Catalog (DataHub, Marquez, Amundsen).
4. Xây dựng đồ thị có hướng (DAG) thể hiện luồng di chuyển của dữ liệu từ nguồn gốc tới đích đến.
5. Cấu hình kiểm tra phân tích tác động tự động trong CI/CD: cảnh báo nếu PR có nguy cơ phá vỡ các bảng downstream.
6. Cung cấp giao diện tra cứu danh mục dữ liệu và đánh giá độ tin cậy của các tài sản dữ liệu.

## 7. Concrete Examples
### Trích xuất Lineage cấp cột từ câu lệnh SQL bằng sqlglot:
```python
from sqlglot import parse_one, exp
from sqlglot.lineage import lineage

sql = '''
CREATE VIEW v_user_spend AS 
SELECT u.user_id, u.email, SUM(o.amount) as total_spent 
FROM users u 
JOIN orders o ON u.user_id = o.user_id 
GROUP BY u.user_id, u.email
'''

# Truy vet nguon goc cua cot 'total_spent'
node = lineage("total_spent", sql)
print("Truy vet nguon goc cot total_spent:")
for source in node.sources:
    print(f" -> Den tu cot/bieu thuc: {source.name} (Source: {source.expression})")
```

## 8. Anti-Patterns & Common Traps
- **Manual Documentation Spreadsheets:** Quản lý danh mục dữ liệu bằng file Excel thủ công dẫn tới việc tài liệu bị lỗi thời ngay sau 1 tuần.
- **Table-Only Lineage:** Chỉ theo dõi dữ liệu ở mức bảng mà không biết cột nào liên kết với cột nào khiến việc phân tích tác động thiếu chính xác.
- **Ignoring Ephemeral Temp Tables:** Không theo dõi các bảng tạm trong luồng ETL dẫn tới việc đồ thị lineage bị đứt đoạn.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: 100% các mô hình dbt và bảng warehouse đều có đồ thị lineage tự động ghi nhận.
- **QG-04**: CI/CD tự động cảnh báo các thay đổi làm hỏng cấu trúc (Breaking Schema Changes) đối với các bảng hạ nguồn.
- **QG-08**: Độ trễ cập nhật siêu dữ liệu mới vào catalog không vượt quá 2 giờ kể từ khi pipeline chạy xong.

## 10. Security & Safety Boundaries
- Gắn thẻ phân loại bảo mật (Confidential, PII, Public) tự động kế thừa dọc theo luồng lineage của dữ liệu.

## 11. Platform Adapters
- **Metadata Platforms**: DataHub, Marquez, OpenMetadata, Amundsen.
- **Lineage Extractors**: OpenLineage, sqlglot, dbt, Apache Atlas.

## 12. Deliverables & Output Artifacts
- Pipeline thu thập siêu dữ liệu tự động từ kho dữ liệu.
- Đồ thị truy vết nguồn gốc cấp cột hoàn chỉnh.
- Bot cảnh báo tác động schema trong quy trình Pull Request.

## 13. Related & Complementary Skills
dex-data-masking-synthetic-generation, dex-configuration-schema-design, dex-contract-first-development

## 14. Realistic Usage Example
```powershell
# Đẩy metadata từ dự án dbt sang DataHub
datahub ingest -c ./datahub-dbt-recipe.yaml

# Phân tích cú pháp SQL để trích xuất lineage cấp cột
python scripts/extract_column_lineage.py --sql-dir ./models/
```
