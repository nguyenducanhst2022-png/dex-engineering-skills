---
name: dex-data-contracts
description: Define and enforce data contracts between data producers and data consumers, schema validation, semantic change alerts, and SLA guarantees. Use when establishing data contracts, preventing upstream breaking schema changes, or governing data pipelines.
---

# dex-data-contracts

## 1. Purpose & Scope
Thiết lập, quản lý và thực thi các Hợp đồng Dữ liệu (Data Contracts) chính thức giữa bên sản xuất dữ liệu (Data Producers - ví dụ Backend services) và bên tiêu thụ dữ liệu (Data Consumers - ví dụ Data Warehouse, Analytics, ML teams); ngăn chặn sự cố gãy vỡ đường ống dữ liệu (Broken Data Pipelines) do các thay đổi schema bất ngờ ở thượng nguồn.

## 2. When to Use
- Khi các thay đổi cấu trúc bảng cơ sở dữ liệu làm sập báo cáo Dashboard hoặc mô hình Machine Learning ở hạ nguồn.
- Khi cần chuẩn hóa schema trao đổi dữ liệu phân tích (JSON Schema, Avro, Protobuf, dbt Semantic Layer).
- Khi thiết lập cam kết chất lượng dữ liệu và thỏa thuận mức dịch vụ (SLAs / SLIs) về tính tươi mới của dữ liệu (Data Freshness).

## 3. When NOT to Use
- Hợp đồng API giao tiếp HTTP client-server thông thường (dùng `dex-api-engineering`).
- Lưu trữ dữ liệu cấu hình nội bộ trong một service độc lập.

## 4. Prerequisites & Input Context
**Đầu vào cần thiết:**
- Bản đặc tả dữ liệu nghiệp vụ cần chia sẻ.
- Schema định dạng (OpenDataContract Standard, JSON Schema, Protobuf).
- Danh sách các bên tiêu thụ và SLA cam kết.

**Điều kiện tiên quyết:**
- Có kho lưu trữ hợp đồng dữ liệu tập trung (Data Contract Registry hoặc Git repository).
- Có pipeline CI/CD kiểm tra tính tương thích của schema trước khi merge mã nguồn của bên sản xuất.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**: Nắm vững cơ chế vận hành theo chuẩn Agent Skills, tuân thủ nghiêm ngặt tính xác định và ranh giới trách nhiệm.
- **Quy tắc quyết định kỹ thuật**:
- **Tương Thích Ngược Bắt Buộc**: Producer chỉ được phép thêm trường mới tùy chọn; cấm xóa trường hoặc đổi kiểu dữ liệu mà không có lộ trình thông báo trước 30 ngày (Deprecation Notice).
- **Quy Trách Nhiệm Rõ Ràng**: Mỗi Data Contract bắt buộc phải có một Đội ngũ Sản xuất (Producing Team) chịu trách nhiệm chính về tính đúng đắn của dữ liệu.
- **Không Dùng Schema Mở (No Open Schemas)**: Cấm sử dụng các trường kiểu `JSON` hoặc `Map<String, Any>` vô định hình trong dữ liệu hợp đồng.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Producer xóa cột làm sập ETL pipeline đêm**: Do không có CI kiểm tra contract -> Khắc phục: Thiết lập CI gate chặn migration nếu vi phạm Data Contract đã ký kết.
- **Dữ liệu bị trễ 12 tiếng làm sai lệch báo cáo**: Producer gặp lỗi nghẽn worker -> Khắc phục: Cảnh báo tự động khi Data Freshness SLA bị vượt quá 60 phút.

## 6. Step-by-Step Execution Workflow
1. Khảo sát nhu cầu tiêu thụ dữ liệu của các team hạ nguồn (Analytics, ML, BI).
2. Soạn thảo bản Data Contract mô tả rõ: Thuộc tính (Properties), Kiểu dữ liệu (Data Types), Ràng buộc (Constraints, nullability), Tiêu chí chất lượng (Freshness, Volume) và Chủ sở hữu (Owner).
3. Tích hợp validation tự động vào CI/CD của producer: Chặn deploy nếu producer thay đổi trường dữ liệu mà vi phạm contract.
4. Xuất bản contract vào Data Contract Registry.
5. Thiết lập cảnh báo thời gian thực khi dữ liệu thực tế phát ra bị lệch so với hợp đồng.
6. Định kỳ xem xét và nâng cấp phiên bản contract theo chuẩn SemVer.

## 7. Concrete Examples
### Ví dụ triển khai chuẩn mực:
```yaml
# datacontract.yaml
version: 2.0.0
info:
  title: Order Completed Events Contract
  owner: checkout-team@company.com
models:
  orders:
    fields:
      order_id:
        type: string
        required: true
      total_amount_cents:
        type: integer
        minimum: 0
      created_at:
        type: timestamp
quality:
  freshness:
    max_delay: 15m
```

### Lệnh xác minh & thực thi:
- Kiểm tra tính hợp lệ của Data Contract YAML: `npx datacontract test datacontract.yaml`
- Chạy kiểm tra tương thích schema: `datacontract breaking-changes --current current.yaml --new new.yaml`
- Kiểm tra dữ liệu mẫu đối chiếu với contract: `datacontract test --data sample.json`

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước kiểm tra biên và giả định hệ thống luôn ở trạng thái lý tưởng.
- **Anti-Pattern 2**: Không ghi nhận nhật ký kiểm toán hoặc bỏ qua việc xử lý ngoại lệ lúc runtime.
- **Trap**: Bỏ qua các rào chắn an toàn hoặc cố tình chạy script không qua kiểm thử tự động.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Bản Data Contract định nghĩa đầy đủ 100% các trường, ràng buộc và SLAs.
- QG-06: Phân tích tương thích xác nhận 0 breaking changes đối với các bên tiêu thụ hiện tại.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động trước khi coi là hoàn thành.

## 10. Security & Safety Boundaries
- Đánh dấu rõ các trường chứa thông tin PII (Personally Identifiable Information) trong contract để tự động mã hóa hoặc làm sạch (masking) trước khi đưa vào data lake.
- Không bao giờ thực thi mã nguồn hoặc thay đổi cấu hình trên môi trường sản xuất mà thiếu cơ chế rollback an toàn.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Có thể kích hoạt trực tiếp từ terminal hoặc extension tương thích trong VS Code / Cursor / Windsurf.

## 12. Deliverables & Output Artifacts
- File Data Contract chuẩn hóa (`datacontract.yaml`).
- Bộ kiểm thử tự động kiểm tra tính tuân thủ hợp đồng.
- Báo cáo đánh giá tương thích schema.

## 13. Related & Complementary Skills
- `dex-development-workflow`: Quy trình phát triển tiêu chuẩn.
- `dex-code-verification`: Xác minh chất lượng và tính đúng đắn của mã nguồn.
- `dex-master-orchestrator`: Bộ điều phối trung tâm kết nối kỹ năng này với các kỹ năng khác trong hệ thống.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư hoặc AI Agent tiếp nhận yêu cầu liên quan đến **dex-data-contracts**.
1. Đọc kỹ đầu vào và các ràng buộc kỹ thuật tại mục 4.
2. Thực thi tuần tự 6 bước trong Workflow tại mục 6.
3. Chạy các lệnh kiểm chứng tại mục 7 và đối chiếu với Quality Gates tại mục 9.
4. Đóng gói deliverables theo danh sách tại mục 12 và báo cáo kết quả kèm bằng chứng xác thực.
