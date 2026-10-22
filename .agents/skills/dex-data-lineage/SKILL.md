---
name: dex-data-lineage
description: Track and visualize data lineage, metadata graphs, column-level provenance, impact analysis, and OpenLineage/Marquez integrations. Use when mapping data dependencies, auditing data origin, or assessing data pipeline impact.
---

# dex-data-lineage

## 1. Purpose & Scope
Thiết lập, theo dõi và trực quan hóa nguồn gốc và luồng di chuyển của dữ liệu (Data Lineage & Provenance) xuyên suốt từ hệ thống nguồn đến các bảng tổng hợp và báo cáo; theo dõi nguồn gốc đến tận cấp độ cột (Column-level Lineage), giúp đội ngũ kỹ sư hiểu rõ mọi dữ liệu đến từ đâu, qua những phép biến đổi nào và việc sửa một bảng sẽ ảnh hưởng đến những báo cáo nào.

## 2. When to Use
- Khi cần phân tích tác động trước khi thay đổi cấu trúc bảng dữ liệu lớn (bảng này có bao nhiêu dashboard đang đọc?).
- Khi số liệu báo cáo tài chính bị sai và cần truy ngược lại nguồn gốc xem dữ liệu sai từ bước biến đổi nào.
- Khi cần tuân thủ các quy định pháp lý về bảo vệ dữ liệu (GDPR, HIPAA, Basel) đòi hỏi phải chứng minh được nguồn gốc của dữ liệu.

## 3. When NOT to Use
- Ứng dụng web đơn giản chỉ có 3 bảng cơ sở dữ liệu quan hệ.
- Theo dõi luồng gọi hàm trong mã nguồn ứng dụng (dùng `dex-change-impact-analysis`).

## 4. Prerequisites & Input Context
**Đầu vào cần thiết:**
- Danh sách các đường ống dữ liệu (Airflow DAGs, dbt models, Spark jobs, SQL queries).
- Công cụ thu thập siêu dữ liệu (OpenLineage, Marquez, DataHub, Amundsen).
- Schema của các bảng dữ liệu thượng nguồn và hạ nguồn.

**Điều kiện tiên quyết:**
- Các công cụ chạy dữ liệu (Airflow, dbt, Spark) được gắn plugin phát sự kiện OpenLineage.
- Data Lineage Server (Marquez hoặc DataHub) đang hoạt động và có API tiếp nhận metadata.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**: Nắm vững cơ chế vận hành theo chuẩn Agent Skills, tuân thủ nghiêm ngặt tính xác định và ranh giới trách nhiệm.
- **Quy tắc quyết định kỹ thuật**:
- **Tự Động Thu Thập Metadata (Automated Collection)**: Tuyệt đối không vẽ sơ đồ nguồn gốc dữ liệu thủ công bằng tay; toàn bộ lineage phải được trích xuất tự động từ mã SQL và pipeline execution.
- **Bắt Buộc Theo Dõi Cấp Cột Cho Dữ Liệu Nhạy Cảm**: Với các cột PII (Email, Phone, Số CCCD), bắt buộc phải có Column-level lineage để kiểm soát dữ liệu đó đã lan truyền đi những đâu trong data lake.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Đồ thị Lineage bị đứt đoạn**: Do một bước biến đổi dùng script Python ngoài không phát sự kiện OpenLineage -> Khắc phục: Sử dụng OpenLineage Python Client để phát sự kiện thủ công cho task đó.
- **Không phát hiện được bảng hạ nguồn bị lỗi**: Do tên bảng bị alias đổi khác -> Khắc phục: Chuẩn hóa định danh Dataset theo chuẩn Universal URN (`namespace:dataset_name`).

## 6. Step-by-Step Execution Workflow
1. Tích hợp OpenLineage hook vào Airflow và dbt để tự động trích xuất metadata mỗi khi job chạy.
2. Thu thập thông tin Dataset Inputs và Dataset Outputs của từng tác vụ.
3. Phân tích cú pháp câu lệnh SQL để dựng bản đồ nguồn gốc tới cấp độ cột (Column-level lineage: cột `revenue` được tính từ `price * quantity - discount`).
4. Dựng đồ thị luồng dữ liệu (Lineage DAG Graph) trên giao diện trực quan.
5. Khi có yêu cầu thay đổi schema: Tra cứu đồ thị để lập danh sách toàn bộ các dashboard và bảng hạ nguồn bị ảnh hưởng.
6. Định kỳ kiểm toán các luồng dữ liệu mồ côi (Datasets không có ai tiêu thụ).

## 7. Concrete Examples
### Ví dụ triển khai chuẩn mực:
```yaml
# openlineage.yml
transport:
  type: http
  url: http://marquez:5000/api/v1/lineage
  timeout: 5.0
```

### Lệnh xác minh & thực thi:
- Kiểm tra API phát sự kiện OpenLineage: `curl http://localhost:5000/api/v1/lineage?nodeId=dataset:postgres.public.orders`
- Sinh sơ đồ lineage bằng dbt: `dbt docs generate` && `dbt docs serve`
- Kiểm tra phân tích cú pháp SQL lineage: `sqllineage -e 'INSERT INTO gold SELECT a, b FROM silver'`

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước kiểm tra biên và giả định hệ thống luôn ở trạng thái lý tưởng.
- **Anti-Pattern 2**: Không ghi nhận nhật ký kiểm toán hoặc bỏ qua việc xử lý ngoại lệ lúc runtime.
- **Trap**: Bỏ qua các rào chắn an toàn hoặc cố tình chạy script không qua kiểm thử tự động.

## 9. Quality Gates & Acceptance Criteria
- QG-01: 100% các bảng Gold Mart đều có bản đồ nguồn gốc truy ngược về bảng Bronze ban đầu.
- QG-09: Tài liệu dbt docs hiển thị đầy đủ sơ đồ Lineage Graph hoàn chỉnh không có mắt xích đứt gãy.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động trước khi coi là hoàn thành.

## 10. Security & Safety Boundaries
- Quyền truy cập vào sơ đồ Lineage phải được phân quyền; không để lộ thông tin cấu trúc cơ sở dữ liệu nội bộ cho người dùng không có thẩm quyền.
- Không bao giờ thực thi mã nguồn hoặc thay đổi cấu hình trên môi trường sản xuất mà thiếu cơ chế rollback an toàn.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Có thể kích hoạt trực tiếp từ terminal hoặc extension tương thích trong VS Code / Cursor / Windsurf.

## 12. Deliverables & Output Artifacts
- Sơ đồ đồ thị nguồn gốc dữ liệu (Data Lineage Graph).
- Báo cáo phân tích tác động hạ nguồn khi thay đổi schema.
- File cấu hình tích hợp OpenLineage (`openlineage.yml`).

## 13. Related & Complementary Skills
- `dex-development-workflow`: Quy trình phát triển tiêu chuẩn.
- `dex-code-verification`: Xác minh chất lượng và tính đúng đắn của mã nguồn.
- `dex-master-orchestrator`: Bộ điều phối trung tâm kết nối kỹ năng này với các kỹ năng khác trong hệ thống.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư hoặc AI Agent tiếp nhận yêu cầu liên quan đến **dex-data-lineage**.
1. Đọc kỹ đầu vào và các ràng buộc kỹ thuật tại mục 4.
2. Thực thi tuần tự 6 bước trong Workflow tại mục 6.
3. Chạy các lệnh kiểm chứng tại mục 7 và đối chiếu với Quality Gates tại mục 9.
4. Đóng gói deliverables theo danh sách tại mục 12 và báo cáo kết quả kèm bằng chứng xác thực.
