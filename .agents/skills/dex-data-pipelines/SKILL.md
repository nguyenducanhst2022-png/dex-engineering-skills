---
name: dex-data-pipelines
description: Architect scalable data pipelines, batch ETL/ELT workflows, stream processing (Kafka/Spark/Flink), idempotent data transformations, and stateful DAGs with Airflow/Dagster. Use when building data extraction, transformation, ingestion, or analytics pipelines.
---

# dex-data-pipelines

## 1. Purpose & Scope
Thiết kế và triển khai các đường ống dẫn dữ liệu (Data Pipelines) quy mô lớn theo cả hai mô hình Xử lý theo lô (Batch ETL/ELT) và Xử lý thời gian thực (Stream Processing); xây dựng đồ thị có hướng không chu trình (DAGs) bằng Apache Airflow / Dagster, đảm bảo tính biến đổi bất biến (Idempotent Transformations) và khả năng xử lý lại dữ liệu lịch sử (Backfilling) không sai lệch.

## 2. When to Use
- Khi cần trích xuất dữ liệu từ nhiều nguồn phân tán (OLTP databases, APIs, logs) để tổng hợp vào Data Warehouse (Snowflake, BigQuery, ClickHouse).
- Khi cần xử lý luồng dữ liệu thời gian thực (Streaming data) với Apache Kafka, Spark Streaming hoặc Flink.
- Khi cần chạy các tác vụ biến đổi dữ liệu định kỳ nặng (dbt transformations) phục vụ kinh doanh.

## 3. When NOT to Use
- Xử lý các tác vụ nghiệp vụ transactional CRUD nhanh trong ứng dụng web (dùng `dex-background-job-queues`).
- Các script backup cơ sở dữ liệu đơn giản một lệnh.

## 4. Prerequisites & Input Context
**Đầu vào cần thiết:**
- Nguồn dữ liệu (Data Sources: Postgres CDC, MongoDB, S3 files, Webhook events).
- Đích dữ liệu (Data Sinks: BigQuery, Iceberg, Parquet on S3, PostgreSQL Data Mart).
- Chu kỳ thực thi (Realtime, Hourly, Daily at 02:00 AM).

**Điều kiện tiên quyết:**
- Hệ thống điều phối luồng dữ liệu (Airflow / Dagster / Prefect) đang hoạt động và có kết nối an toàn tới các kho dữ liệu.
- Đã thiết lập các khu vực lưu trữ theo tầng: Bronze/Raw -> Silver/Cleaned -> Gold/Aggregated.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**: Nắm vững cơ chế vận hành theo chuẩn Agent Skills, tuân thủ nghiêm ngặt tính xác định và ranh giới trách nhiệm.
- **Quy tắc quyết định kỹ thuật**:
- **Tất Cả Các Batch Job Đều Phải Re-run Được (Idempotency)**: Bất kỳ ngày nào trong quá khứ cũng có thể chạy lại lệnh backfill mà không làm nhân đôi số liệu hoặc phát sinh sai lệch.
- **ELT Thay Vì ETL Cho Dữ Liệu Lớn**: Trích xuất và nạp dữ liệu thô vào Data Warehouse trước (Extract & Load), sau đó dùng sức mạnh tính toán của SQL/dbt để biến đổi (Transform) bên trong warehouse.
- **Không Lưu Mật Khẩu Trong DAG**: Tất cả thông tin kết nối phải được lưu trong Airflow Connections / Secret Manager, cấm hardcode trong mã Python.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Dữ liệu bị trùng lặp sau khi pipeline chạy lại**: Do dùng câu lệnh `INSERT INTO` mà không xóa dữ liệu cũ -> Khắc phục: Luôn dùng `MERGE INTO` hoặc phân vùng theo ngày `WHERE date = execution_date`.
- **DAG bị treo vĩnh viễn (Zombie Tasks)**: Do worker bị kill đột ngột -> Khắc phục: Thiết lập timeout cho từng task (`execution_timeout = timedelta(hours=2)`).

## 6. Step-by-Step Execution Workflow
1. Thiết kế kiến trúc hồ dữ liệu đa tầng (Medallion Architecture): Bronze (Lưu thô nguyên bản) -> Silver (Làm sạch, khử trùng lặp) -> Gold (Tổng hợp phục vụ nghiệp vụ).
2. Xây dựng DAGs điều phối tác vụ với các bước phụ thuộc rõ ràng.
3. Triển khai cơ chế Ghi Bất Biến (Idempotent Writes): Sử dụng kỹ thuật ghi đè theo phân vùng (`INSERT OVERWRITE PARTITION`) hoặc Upsert dựa trên khóa chính (`MERGE INTO`).
4. Xử lý dữ liệu đến muộn (Late-arriving data) bằng Watermarking trong stream processing.
5. Tự động kiểm tra chất lượng dữ liệu giữa các bước (Data Quality Gates).
6. Cấu hình cơ chế tự động thử lại (Retry with Backoff) khi gặp lỗi mạng tạm thời.

## 7. Concrete Examples
### Ví dụ triển khai chuẩn mực:
```python
# dags/orders_etl.py
@dag(schedule_interval='@daily', start_date=datetime(2026, 1, 1), catchup=False)
def daily_orders_pipeline():
    extract_task = PythonOperator(task_id='extract_raw', python_callable=extract_to_bronze)
    transform_task = BashOperator(task_id='dbt_silver_gold', bash_command='dbt run')
    test_task = BashOperator(task_id='dbt_test', bash_command='dbt test')
    extract_task >> transform_task >> test_task
```

### Lệnh xác minh & thực thi:
- Kiểm tra cú pháp DAG Airflow: `python dags/orders_etl_dag.py`
- Chạy thử nghiệm 1 task trong DAG: `airflow tasks test orders_etl extract_orders 2026-10-22`
- Chạy kiểm tra mô hình dbt: `dbt run --select tag:daily` && `dbt test`

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước kiểm tra biên và giả định hệ thống luôn ở trạng thái lý tưởng.
- **Anti-Pattern 2**: Không ghi nhận nhật ký kiểm toán hoặc bỏ qua việc xử lý ngoại lệ lúc runtime.
- **Trap**: Bỏ qua các rào chắn an toàn hoặc cố tình chạy script không qua kiểm thử tự động.

## 9. Quality Gates & Acceptance Criteria
- QG-04: Pipeline hoàn thành toàn bộ các tasks trong khung thời gian quy định (SLA Window).
- QG-05: 100% các bài kiểm tra dbt test (unique, not_null, accepted_values) đạt PASS.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động trước khi coi là hoàn thành.

## 10. Security & Safety Boundaries
- Dữ liệu lưu trong Data Lake phải được mã hóa ở trạng thái nghỉ (Encryption at Rest - SSE-KMS).
- Áp dụng kiểm soát truy cập dựa trên cột (Column-level security) cho các cột doanh thu nhạy cảm.
- Không bao giờ thực thi mã nguồn hoặc thay đổi cấu hình trên môi trường sản xuất mà thiếu cơ chế rollback an toàn.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Có thể kích hoạt trực tiếp từ terminal hoặc extension tương thích trong VS Code / Cursor / Windsurf.

## 12. Deliverables & Output Artifacts
- File định nghĩa DAG (`dags/orders_daily_etl.py`).
- Các mô hình biến đổi dữ liệu SQL/dbt (`models/marts/orders_summary.sql`).
- File kiểm thử chất lượng dữ liệu.

## 13. Related & Complementary Skills
- `dex-development-workflow`: Quy trình phát triển tiêu chuẩn.
- `dex-code-verification`: Xác minh chất lượng và tính đúng đắn của mã nguồn.
- `dex-master-orchestrator`: Bộ điều phối trung tâm kết nối kỹ năng này với các kỹ năng khác trong hệ thống.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư hoặc AI Agent tiếp nhận yêu cầu liên quan đến **dex-data-pipelines**.
1. Đọc kỹ đầu vào và các ràng buộc kỹ thuật tại mục 4.
2. Thực thi tuần tự 6 bước trong Workflow tại mục 6.
3. Chạy các lệnh kiểm chứng tại mục 7 và đối chiếu với Quality Gates tại mục 9.
4. Đóng gói deliverables theo danh sách tại mục 12 và báo cáo kết quả kèm bằng chứng xác thực.
