---
name: dex-schema-evolution
description: Manage backward and forward schema evolution for Avro, Protobuf, JSON Schema, and relational databases. Enforces compatibility rules (FULL, BACKWARD, FORWARD) with Schema Registries. Use when modifying event schemas, updating serialization contracts, or evolving APIs.
---

# dex-schema-evolution

## 1. Purpose & Scope
Quản lý quá trình tiến hóa lược đồ dữ liệu (Schema Evolution) an toàn và bền vững cho các định dạng nhị phân và sự kiện (Apache Avro, Protocol Buffers, JSON Schema, Parquet); áp dụng các quy tắc kiểm tra tương thích nghiêm ngặt (BACKWARD, FORWARD, FULL COMPATIBILITY) thông qua Schema Registry, đảm bảo các ứng dụng phiên bản cũ và mới có thể đọc ghi dữ liệu lẫn nhau mà không bị crash.

## 2. When to Use
- Khi cần thêm, sửa hoặc xóa một trường trong thông điệp Kafka Event hoặc gRPC Service.
- Khi hệ thống có nhiều bên tiêu thụ dữ liệu chạy các phiên bản phần mềm khác nhau và không thể deploy đồng thời cùng một giây.
- Khi Schema Registry từ chối đăng ký schema mới do vi phạm quy tắc tương thích.

## 3. When NOT to Use
- Migration bảng cơ sở dữ liệu quan hệ thuần túy (dùng `dex-database-engineering`).
- Thay đổi các biến nội bộ trong cùng một tiến trình ứng dụng.

## 4. Prerequisites & Input Context
**Đầu vào cần thiết:**
- File schema hiện tại và file schema dự kiến thay đổi (Avro `.avsc`, Protobuf `.proto`, JSON Schema).
- Chế độ tương thích mục tiêu (Compatibility Level: `BACKWARD`, `FORWARD`, `FULL`).
- Confluent Schema Registry hoặc Karapace endpoint.

**Điều kiện tiên quyết:**
- Schema Registry đang hoạt động và quản lý phiên bản schema cho các Topics liên quan.
- Đã thiết lập plugin kiểm tra tương thích schema trong build tool (Gradle / Maven / Buf CLI / Confluent CLI).

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**: Nắm vững cơ chế vận hành theo chuẩn Agent Skills, tuân thủ nghiêm ngặt tính xác định và ranh giới trách nhiệm.
- **Quy tắc quyết định kỹ thuật**:
- **Quy Tắc Vàng Của Trường Mới**: Mọi trường mới thêm vào Avro/Protobuf Schema bắt buộc phải có giá trị `default` hợp lệ.
- **Không Tái Sử Dụng Field Number Trong Protobuf**: Trong `.proto`, một khi một số tag (Field Number) đã được sử dụng rồi xóa, số đó phải được đánh dấu là `reserved` để không bao giờ bị tái sử dụng nhầm lẫn.
- **Full Compatibility Cho Dữ Liệu Dài Hạn**: Với các dữ liệu lưu trữ dài hạn trong Data Lake (Parquet/Iceberg), luôn duy trì chế độ tương thích `FULL`.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Consumer bị sập do không đọc được tin nhắn mới**: Do Producer thêm trường bắt buộc mà không có default value -> Khắc phục: Schema Registry chặn deploy từ CI và báo lỗi vi phạm BACKWARD compatibility.
- **Dữ liệu cũ bị đọc sai lệch sau khi tái sử dụng field id**: -> Khắc phục: Khai báo `reserved 4, 8; reserved "old_field_name";` trong file Protobuf.

## 6. Step-by-Step Execution Workflow
1. Khảo sát nhu cầu thay đổi schema: Cần thêm trường, đổi kiểu hay xóa trường?
2. Lựa chọn chế độ tương thích:
   - **BACKWARD (Khuyến nghị chuẩn)**: Ứng dụng mới có thể đọc dữ liệu do ứng dụng cũ tạo ra.
   - **FORWARD**: Ứng dụng cũ có thể đọc dữ liệu do ứng dụng mới tạo ra.
   - **FULL**: Đảm bảo cả hai chiều đồng thời (Lý tưởng nhất cho kiến trúc phân tán).
3. Áp dụng các quy tắc tiến hóa an toàn:
   - Khi THÊM trường mới: BẮT BUỘC phải có giá trị mặc định (`default: null` hoặc `default: ""`).
   - Khi XÓA trường: Trường đó phải là optional và đã ngưng sử dụng ở toàn bộ các bên tiêu thụ.
   - CẤM đổi kiểu dữ liệu của trường đang có (ví dụ từ `int` sang `string`).
   - CẤM đổi tên trường trực tiếp (hãy dùng bí danh `aliases` trong Avro).
4. Chạy công cụ kiểm tra tương thích trong CI/CD trước khi commit.
5. Đăng ký phiên bản schema mới vào Schema Registry.
6. Nâng cấp mã nguồn bên sản xuất và bên tiêu thụ tuần tự.

## 7. Concrete Examples
### Ví dụ triển khai chuẩn mực:
```json
// Avro Schema Evolution An Toàn: Thêm trường có giá trị mặc định
{
  "type": "record",
  "name": "OrderEvent",
  "fields": [
    { "name": "orderId", "type": "string" },
    { "name": "amount", "type": "double" },
    {
      "name": "discountCode",
      "type": ["null", "string"],
      "default": null
    }
  ]
}
```

### Lệnh xác minh & thực thi:
- Kiểm tra tương thích với Buf CLI (Protobuf): `buf breaking --against '.git#branch=main'`
- Kiểm tra tương thích Avro qua Confluent CLI: `confluent schema-registry compatibility validate --subject orders-value --schema schema_v2.avsc`
- Chạy unit test serialize/deserialize đa phiên bản: `npm test -- tests/schemas/avroCompat.spec.ts`

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước kiểm tra biên và giả định hệ thống luôn ở trạng thái lý tưởng.
- **Anti-Pattern 2**: Không ghi nhận nhật ký kiểm toán hoặc bỏ qua việc xử lý ngoại lệ lúc runtime.
- **Trap**: Bỏ qua các rào chắn an toàn hoặc cố tình chạy script không qua kiểm thử tự động.

## 9. Quality Gates & Acceptance Criteria
- QG-06: Schema mới đạt 100% kiểm tra tương thích (FULL hoặc BACKWARD) từ Schema Registry.
- QG-10: Có bài test chứng minh Consumer phiên bản v1 đọc được dữ liệu do Producer v2 sinh ra.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động trước khi coi là hoàn thành.

## 10. Security & Safety Boundaries
- Kiểm tra xem trường mới thêm vào có chứa dữ liệu nhạy cảm không; nếu có, phải gắn metadata phân loại bảo mật ngay trong schema.
- Không bao giờ thực thi mã nguồn hoặc thay đổi cấu hình trên môi trường sản xuất mà thiếu cơ chế rollback an toàn.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Có thể kích hoạt trực tiếp từ terminal hoặc extension tương thích trong VS Code / Cursor / Windsurf.

## 12. Deliverables & Output Artifacts
- File schema mới đã qua kiểm chứng (`schemas/orders.v2.avsc` hoặc `.proto`).
- Kết quả kiểm tra tương thích không có lỗi breaking changes.
- Mã nguồn client tự động sinh từ schema (Generated DTOs).

## 13. Related & Complementary Skills
- `dex-development-workflow`: Quy trình phát triển tiêu chuẩn.
- `dex-code-verification`: Xác minh chất lượng và tính đúng đắn của mã nguồn.
- `dex-master-orchestrator`: Bộ điều phối trung tâm kết nối kỹ năng này với các kỹ năng khác trong hệ thống.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư hoặc AI Agent tiếp nhận yêu cầu liên quan đến **dex-schema-evolution**.
1. Đọc kỹ đầu vào và các ràng buộc kỹ thuật tại mục 4.
2. Thực thi tuần tự 6 bước trong Workflow tại mục 6.
3. Chạy các lệnh kiểm chứng tại mục 7 và đối chiếu với Quality Gates tại mục 9.
4. Đóng gói deliverables theo danh sách tại mục 12 và báo cáo kết quả kèm bằng chứng xác thực.
