---
name: dex-data-quality-audits
description: Implement automated data quality testing, Great Expectations suites, anomaly detection, nullability audits, and statistical distributions. Use when verifying data integrity, detecting corrupt datasets, or setting up data pipeline tests.
---

# dex-data-quality-audits

## 1. Purpose & Scope
Thiết lập hệ thống kiểm toán chất lượng dữ liệu (Data Quality Audits) tự động hóa; phát hiện sớm các hiện tượng dữ liệu bị rác, giá trị null bất thường, phân phối thống kê sai lệch (Statistical Drift), dữ liệu vi phạm ràng buộc miền giá trị thông qua các bộ kiểm thử chuyên dụng (Great Expectations / Soda / dbt-expectations).

## 2. When to Use
- Khi số liệu trên Dashboard doanh thu bỗng nhiên hiển thị số âm hoặc tụt giảm 90% không rõ nguyên nhân.
- Trước khi đưa tập dữ liệu mới vào huấn luyện mô hình AI / Machine Learning.
- Khi sáp nhập dữ liệu từ hệ thống legacy cũ vào hệ thống mới và cần kiểm chứng tính toàn vẹn.

## 3. When NOT to Use
- Kiểm thử tính đúng đắn của logic mã nguồn frontend (dùng `dex-code-verification`).
- Quét lỗ hổng an ninh mã nguồn phần mềm (dùng `dex-security-audit`).

## 4. Prerequisites & Input Context
**Đầu vào cần thiết:**
- Bảng dữ liệu hoặc tệp dữ liệu cần kiểm toán (Postgres table, Parquet file, Snowflake table).
- Bộ quy tắc kỳ vọng chất lượng dữ liệu (Expectation Suite: Uniqueness, Range, Nullability, Regex).
- Ngưỡng cảnh báo độ lệch thống kê.

**Điều kiện tiên quyết:**
- Có quyền truy cập chỉ đọc (Read-only) vào kho lưu trữ dữ liệu.
- Công cụ kiểm toán (Great Expectations / Soda / dbt) đã được kết nối với nguồn dữ liệu.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**: Nắm vững cơ chế vận hành theo chuẩn Agent Skills, tuân thủ nghiêm ngặt tính xác định và ranh giới trách nhiệm.
- **Quy tắc quyết định kỹ thuật**:
- **Chặn Dữ Liệu Độc Hại Ngay Tại Cửa Vào**: Nếu một đợt nạp dữ liệu có tỷ lệ lỗi vượt quá 1%, lập tức ngắt pipeline và không ghi đè vào bảng sản xuất (Fail Fast).
- **Kiểm Soát Độ Trôi Phân Phối (Distribution Drift)**: Không chỉ kiểm tra null, mà phải kiểm tra số lượng dòng nạp vào có bị tụt giảm bất thường (>30% so với ngày hôm trước) hay không.
- **Tự Động Hóa Không Cần Can Thiệp Thủ Công**: Mọi đợt nạp dữ liệu đều phải tự động chạy audit và sinh báo cáo.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Bảng dữ liệu nhận hàng triệu bản ghi rác có giá trị 0đ**: Do lỗi API phía đối tác -> Khắc phục: Expectation `expect_column_values_to_be_between(min_value=1000)` bắt được lỗi và chặn ghi dữ liệu.
- **Công cụ kiểm toán làm chậm toàn bộ database**: Do chạy câu truy vấn đếm phức tạp trên bảng 500 triệu dòng -> Khắc phục: Chạy kiểm toán trên mẫu ngẫu nhiên (Sampling 5%) hoặc chạy trên phân vùng dữ liệu mới nạp trong ngày.

## 6. Step-by-Step Execution Workflow
1. Khảo sát dữ liệu lịch sử và xác định các đặc trưng quan trọng cần kiểm toán.
2. Thiết lập bộ quy tắc kỳ vọng (Expectation Suite):
   - *Tính duy nhất (Uniqueness)*: Cột ID không được trùng lặp.
   - *Tính đầy đủ (Completeness)*: Cột ngày tạo và mã khách hàng không được null (0% nulls).
   - *Tính hợp lệ (Validity)*: Giá trị tiền phải >= 0; trạng thái đơn hàng nằm trong tập hợp hợp lệ.
   - *Tính nhất quán (Consistency)*: Tổng tiền sản phẩm khớp với tổng tiền đơn hàng.
3. Tự động kích hoạt kiểm toán sau mỗi lần nạp dữ liệu (Post-ingestion audit).
4. Chặn dữ liệu bẩn di chuyển tiếp vào tầng phân tích nếu bài kiểm tra vi phạm mức nghiêm trọng (CRITICAL).
5. Xuất báo cáo trực quan về tình trạng sức khỏe dữ liệu (Data Docs / Quality Dashboard).
6. Bắn cảnh báo tức thì vào kênh Slack/Teams của đội ngũ Data Engineering.

## 7. Concrete Examples
### Ví dụ triển khai chuẩn mực:
```python
# Great Expectations Suite Definition
validator.expect_column_values_to_not_be_null(column='order_id')
validator.expect_column_values_to_be_unique(column='order_id')
validator.expect_column_values_to_be_in_set(
    column='status',
    value_set=['PENDING', 'PROCESSING', 'COMPLETED', 'CANCELLED']
)
validator.expect_column_values_to_be_between(column='amount_cents', min_value=0, max_value=1000000000)
```

### Lệnh xác minh & thực thi:
- Chạy bộ kiểm thử Great Expectations: `great_expectations checkpoint run orders_checkpoint`
- Chạy kiểm tra chất lượng bằng dbt: `dbt test --select test_type:data`
- Xem tài liệu báo cáo dữ liệu: `great_expectations docs build`

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước kiểm tra biên và giả định hệ thống luôn ở trạng thái lý tưởng.
- **Anti-Pattern 2**: Không ghi nhận nhật ký kiểm toán hoặc bỏ qua việc xử lý ngoại lệ lúc runtime.
- **Trap**: Bỏ qua các rào chắn an toàn hoặc cố tình chạy script không qua kiểm thử tự động.

## 9. Quality Gates & Acceptance Criteria
- QG-03: 100% các kỳ vọng chất lượng dữ liệu mức CRITICAL đạt PASS.
- QG-10: Có báo cáo kiểm toán HTML hiển thị chi tiết số lượng bản ghi đã kiểm tra và tỷ lệ đạt chuẩn.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động trước khi coi là hoàn thành.

## 10. Security & Safety Boundaries
- Các bản báo cáo chất lượng dữ liệu (Data Docs) tuyệt đối không được hiển thị trực tiếp dữ liệu nhạy cảm hoặc PII của người dùng mẫu.
- Không bao giờ thực thi mã nguồn hoặc thay đổi cấu hình trên môi trường sản xuất mà thiếu cơ chế rollback an toàn.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Có thể kích hoạt trực tiếp từ terminal hoặc extension tương thích trong VS Code / Cursor / Windsurf.

## 12. Deliverables & Output Artifacts
- File cấu hình kỳ vọng chất lượng dữ liệu (`expectations/orders_suite.json`).
- Báo cáo HTML kiểm toán chất lượng dữ liệu.
- Script chạy kiểm tra tự động tích hợp trong CI/CD pipeline.

## 13. Related & Complementary Skills
- `dex-development-workflow`: Quy trình phát triển tiêu chuẩn.
- `dex-code-verification`: Xác minh chất lượng và tính đúng đắn của mã nguồn.
- `dex-master-orchestrator`: Bộ điều phối trung tâm kết nối kỹ năng này với các kỹ năng khác trong hệ thống.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư hoặc AI Agent tiếp nhận yêu cầu liên quan đến **dex-data-quality-audits**.
1. Đọc kỹ đầu vào và các ràng buộc kỹ thuật tại mục 4.
2. Thực thi tuần tự 6 bước trong Workflow tại mục 6.
3. Chạy các lệnh kiểm chứng tại mục 7 và đối chiếu với Quality Gates tại mục 9.
4. Đóng gói deliverables theo danh sách tại mục 12 và báo cáo kết quả kèm bằng chứng xác thực.
