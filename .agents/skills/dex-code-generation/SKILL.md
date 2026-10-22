---
name: dex-code-generation
description: Design deterministic code generators, AST transformations, scaffolding engines (Plop/Hygen), schema-driven codegen (OpenAPI/Protobuf to client SDKs), and macro systems. Use when eliminating boilerplate, generating typed clients, or automating repetitive patterns.
---

# dex-code-generation

## 1. Purpose & Scope
Thiết kế và hiện thực hóa các công cụ tự động sinh mã nguồn (Code Generation) mang tính xác định (Deterministic); áp dụng biến đổi cây cú pháp trừu tượng (Abstract Syntax Tree - AST), công cụ sinh scaffolding (Plop.js / Hygen), và sinh mã nguồn định kiểu chặt chẽ từ bản đặc tả schema (OpenAPI / GraphQL / Protobuf sinh Client SDKs); triệt tiêu boilerplate code lặp lại.

## 2. When to Use
- Khi phải viết hàng chục file CRUD lặp đi lặp lại (Model, Controller, DTO, Service, Test).
- Khi phía Frontend phải gõ lại thủ công các TypeScript interfaces đã được định nghĩa ở Backend.
- Khi cần cập nhật Client SDK tự động mỗi khi OpenAPI schema thay đổi.

## 3. When NOT to Use
- Viết logic nghiệp vụ độc nhất chỉ xuất hiện một lần.
- Dùng AI sinh code ngẫu nhiên không có kiểm chứng cấu trúc (dùng `dex-development-workflow`).

## 4. Prerequisites & Input Context
**Đầu vào cần thiết:**
- Bản đặc tả dữ liệu nguồn (OpenAPI specs, JSON Schema, Protobuf `.proto`, GraphQL schema).
- Mẫu sinh mã (Templates: Handlebars, EJS, Jinja2).
- Vị trí tệp đích cần tạo hoặc cập nhật.

**Điều kiện tiên quyết:**
- Bản đặc tả nguồn phải hợp lệ về mặt cú pháp và tuân thủ schema validation.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**: Nắm vững cơ chế vận hành theo chuẩn Agent Skills, tuân thủ nghiêm ngặt tính xác định và ranh giới trách nhiệm.
- **Quy tắc quyết định kỹ thuật**:
- **Generated Files Are Read-Only**: Các file sinh tự động tuyệt đối không được sửa thủ công; mọi thay đổi phải xuất phát từ việc sửa template hoặc schema nguồn.
- **Idempotent Generation**: Chạy lại lệnh sinh mã nhiều lần với cùng đầu vào phải cho ra kết quả mã nguồn giống hệt nhau (Deterministic: Byte-for-byte identical).
- **Tự Động Format Sau Khi Sinh**: Mọi mã nguồn sinh ra phải tự động được format bằng code formatter chính thức của dự án trước khi lưu vào đĩa.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Lập trình viên sửa trực tiếp vào file sinh tự động và bị mất code khi chạy lại build**: Do không có cảnh báo -> Khắc phục: Đặt cờ header cảnh báo ở đầu file và cấu hình git hooks từ chối chỉnh sửa thủ công.
- **Schema đổi nhưng client SDK không cập nhật làm sập runtime**: Do quên chạy lệnh sinh mã -> Khắc phục: CI chạy lệnh kiểm tra `npm run codegen && git diff --exit-code`.

## 6. Step-by-Step Execution Workflow
1. Xác định mẫu thiết kế lặp lại cần tự động hóa (Scaffolding pattern).
2. Viết bản mẫu sinh mã (Template) sử dụng cú pháp giữ chỗ (Placeholders) rõ ràng.
3. Xây dựng bộ điều khiển sinh mã: Nhận tham số đầu vào (tên module, thuộc tính) và nạp template.
4. Thực hiện sinh mã và tự động chạy qua linter / code formatter (Prettier / Ruff) để chuẩn hóa định dạng.
5. Đánh dấu rõ ràng các file được tự động sinh (Generated File Header: `/* DO NOT EDIT DIRECTLY */`).
6. Tích hợp lệnh codegen vào quy trình CI: Chặn merge nếu mã nguồn sinh ra bị lệch so với schema nguồn.

## 7. Concrete Examples
### Ví dụ triển khai chuẩn mực:
```javascript
// plopfile.js - Scaffolding generator
module.exports = function (plop) {
  plop.setGenerator('service', {
    description: 'Generate backend domain service',
    prompts: [{ type: 'input', name: 'name', message: 'Service name:' }],
    actions: [
      {
        type: 'add',
        path: 'src/services/{{camelCase name}}.service.ts',
        templateFile: 'plop-templates/service.hbs',
      },
      {
        type: 'add',
        path: 'tests/services/{{camelCase name}}.test.ts',
        templateFile: 'plop-templates/service-test.hbs',
      }
    ]
  });
};
```

### Lệnh xác minh & thực thi:
- Chạy lệnh sinh mã từ OpenAPI: `npm run generate:api-client`
- Kiểm tra tính đồng bộ mã sinh trong CI: `git diff --exit-code` (phải trả về mã 0)
- Chạy scaffolding tương tác: `npx plop component MyNewButton`

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước kiểm tra biên và giả định hệ thống luôn ở trạng thái lý tưởng.
- **Anti-Pattern 2**: Không ghi nhận nhật ký kiểm toán hoặc bỏ qua việc xử lý ngoại lệ lúc runtime.
- **Trap**: Bỏ qua các rào chắn an toàn hoặc cố tình chạy script không qua kiểm thử tự động.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Mã nguồn sinh ra biên dịch sạch sẽ không có lỗi cú pháp hoặc cảnh báo linter.
- QG-06: 100% các kiểu dữ liệu và endpoints trong schema được ánh xạ chính xác sang Client SDK.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động trước khi coi là hoàn thành.

## 10. Security & Safety Boundaries
- Kiểm tra kỹ đầu vào của bộ sinh mã, ngăn chặn lỗ hổng Template Injection (SSTI) khi đọc các trường không tin cậy từ schema.
- Không bao giờ thực thi mã nguồn hoặc thay đổi cấu hình trên môi trường sản xuất mà thiếu cơ chế rollback an toàn.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Có thể kích hoạt trực tiếp từ terminal hoặc extension tương thích trong VS Code / Cursor / Windsurf.

## 12. Deliverables & Output Artifacts
- Bộ template sinh mã (`plop-templates/` hoặc OpenAPI generator config).
- Mã nguồn client SDK hoặc module được sinh hoàn chỉnh.
- Lệnh kiểm tra tính đồng bộ trong CI.

## 13. Related & Complementary Skills
- `dex-development-workflow`: Quy trình phát triển tiêu chuẩn.
- `dex-code-verification`: Xác minh chất lượng và tính đúng đắn của mã nguồn.
- `dex-master-orchestrator`: Bộ điều phối trung tâm kết nối kỹ năng này với các kỹ năng khác trong hệ thống.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư hoặc AI Agent tiếp nhận yêu cầu liên quan đến **dex-code-generation**.
1. Đọc kỹ đầu vào và các ràng buộc kỹ thuật tại mục 4.
2. Thực thi tuần tự 6 bước trong Workflow tại mục 6.
3. Chạy các lệnh kiểm chứng tại mục 7 và đối chiếu với Quality Gates tại mục 9.
4. Đóng gói deliverables theo danh sách tại mục 12 và báo cáo kết quả kèm bằng chứng xác thực.
