---
name: dex-event-schema-registry
description: Govern asynchronous event schemas using Confluent/Apicurio Schema Registry, enforcing Backward/Forward/Full compatibility rules, Avro/Protobuf/JSON Schema validation, and CI schema drift gates. Use when scaling event-driven microservices across distributed engineering teams.
---

# dex-event-schema-registry

## 1. Purpose & Scope
Quản trị lược đồ sự kiện bất đồng bộ (Event Schema Governance) thông qua Schema Registry (Confluent hoặc Apicurio); thực thi nghiêm ngặt các quy tắc tương thích (Backward, Forward, Full Compatibility), xác thực định dạng dữ liệu (Apache Avro, Protobuf, JSON Schema) và thiết lập cổng kiểm soát trôi lược đồ (Schema Drift Gates) trong đường ống CI/CD.

## 2. When to Use
- Khi hệ thống có nhiều đội ngũ kỹ thuật cùng xuất bản và tiêu thụ sự kiện từ cụm Message Broker chung.
- Khi cần thay đổi cấu trúc dữ liệu sự kiện (thêm trường, xóa trường) mà không làm sập các dịch vụ cũ chưa kịp cập nhật.
- Khi kiểm toán chất lượng và tính nhất quán của dữ liệu sự kiện trong kiến trúc Event-Driven.

## 3. When NOT to Use
- Khi hệ thống chỉ là một ứng dụng nguyên khối (Monolith) không có giao tiếp sự kiện bất đồng bộ.
- Khi dữ liệu chỉ lưu trữ nội bộ trong cơ sở dữ liệu và không phát tán ra bên ngoài.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Confluent Schema Registry hoặc Apicurio Registry, định dạng tệp schema (`.avsc` hoặc `.proto`), công cụ dòng lệnh kiểm tra tương thích schema.
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; tuân thủ nghiêm ngặt các ranh giới bảo mật và an toàn dữ liệu.

## 5. Core Concepts & Taxonomy
- **Compatibility Modes:** BACKWARD (người tiêu thụ mới đọc được dữ liệu cũ), FORWARD (người tiêu thụ cũ đọc được dữ liệu mới), FULL (kết hợp cả hai).
- **Magic Byte & Schema ID Framing:** 5 byte đầu tiên trong payload tin nhắn Kafka (1 byte magic + 4 byte ID lược đồ) giúp consumer tra cứu đúng schema.
- **Default Values for Evolution:** Luôn cung cấp giá trị mặc định cho các trường mới được bổ sung để đảm bảo tính tương thích ngược.

## 6. Step-by-Step Execution Workflow
1. Định nghĩa lược đồ sự kiện ban đầu bằng định dạng Apache Avro hoặc Protobuf.
2. Đăng ký lược đồ vào Schema Registry dưới subject tương ứng (ví dụ `user-events-value`).
3. Cấu hình chế độ tương thích mục tiêu (khuyến nghị `BACKWARD_TRANSITIVE` hoặc `FULL`).
4. Cài đặt plugin kiểm tra tương thích schema trong quy trình CI/CD trước khi cho phép merge mã nguồn.
5. Kiểm thử việc xuất bản sự kiện có cấu trúc vi phạm để xác nhận Schema Registry từ chối tiếp nhận.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```json
{
  "type": "record",
  "name": "UserAccountCreated",
  "namespace": "com.dex.events",
  "doc": "Fired whenever a new user completes onboarding.",
  "fields": [
    { "name": "userId", "type": "string" },
    { "name": "email", "type": "string" },
    { "name": "tier", "type": "string", "default": "standard" },
    { "name": "createdAtUtc", "type": "long" }
  ]
}
```

## 8. Anti-Patterns & Common Traps
- Xóa bỏ một trường bắt buộc trong schema khiến toàn bộ các Consumer đang chạy phiên bản cũ bị crash do không parse được dữ liệu.
- Gửi payload JSON thô không qua schema registry, dẫn đến dữ liệu rác làm ô nhiễm topic.
- Thay đổi kiểu dữ liệu của một trường hiện có (ví dụ đổi từ `int` sang `string`) làm phá vỡ tính tương thích ngược.

## 9. Quality Gates & Acceptance Criteria
- QG-01: 100% các thay đổi lược đồ đều vượt qua bài kiểm tra tương thích tự động của Schema Registry.
- QG-02: Mọi trường mới được bổ sung vào schema đều bắt buộc phải có giá trị mặc định (`default`).
- QG-03: Cổng CI chặn đứng 100% các pull request làm thay đổi schema mà không thông qua bài test tương thích.

## 10. Security & Safety Boundaries
- Phân quyền truy cập Schema Registry qua mTLS hoặc HTTP Basic Auth; chỉ cấp quyền ghi (Write) cho đường ống CI/CD tự động.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Tệp định nghĩa lược đồ Avro `UserAccountCreated.avsc`.
1. Kịch bản kiểm tra tương thích schema trong CI `validate-schema-compatibility.sh`.

## 13. Related & Complementary Skills
- [`dex-stream-processing-semantics`](.agents/skills/dex-stream-processing-semantics/SKILL.md)
- [`dex-schema-evolution`](.agents/skills/dex-schema-evolution/SKILL.md)
- [`dex-data-contracts`](.agents/skills/dex-data-contracts/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Một đội backend tự ý đổi tên trường `user_id` thành `customerId` trong sự kiện giao dịch, làm sập toàn bộ hệ thống phân tích BI và báo cáo doanh thu. Kỹ sư kích hoạt `dex-event-schema-registry`, áp dụng chế độ `BACKWARD_TRANSITIVE` và tích hợp kiểm tra tự động vào GitHub Actions, ngăn chặn mọi thay đổi làm vỡ tương thích dữ liệu.
