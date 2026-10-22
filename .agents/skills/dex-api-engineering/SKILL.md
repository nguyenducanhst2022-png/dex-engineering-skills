---
name: dex-api-engineering
description: Production-grade API design, RESTful and GraphQL specifications, input schema validation, authentication middleware, error standardization, and backward compatibility contracts. Prevents breaking changes and enforces robust API contracts. Use when creating endpoints, updating API schemas, or contract testing.
---

# DEX API Engineering

## 1. Purpose & Scope
Thiết kế và triển khai giao diện lập trình ứng dụng (API) chuyên nghiệp, nhất quán, bảo mật và hiệu năng cao; đảm bảo khả năng tương thích ngược (Backward Compatibility) và định dạng phản hồi chuẩn hóa theo hợp đồng (API Contract).

Quy trình API chuẩn:
`Phân tích yêu cầu → Thiết kế API → Xác thực → Phân quyền → Triển khai → Kiểm thử → Tối ưu → Bảo mật → Ổn định → Lưu Git`

Nguyên tắc cốt lõi: **API phải dễ sử dụng, nhất quán, bảo mật, có khả năng mở rộng và không phá vỡ khả năng tương thích khi nâng cấp.**
Ghi nhớ sống còn: **API tốt = Dễ dùng + Nhất quán + Bảo mật + Hiệu năng tốt + Tương thích ngược.**

## 2. When to Use
- Khi tạo mới các endpoint RESTful, GraphQL queries/mutations hoặc gRPC services.
- Khi cập nhật cấu trúc request/response của các API hiện có.
- Khi xây dựng lớp middleware xác thực (Authentication), phân quyền (Authorization) và kiểm soát tần suất gọi (Rate Limiting).
- Khi chuẩn hóa định dạng mã lỗi và thông điệp phản hồi cho toàn hệ thống.

## 3. When NOT to Use
- Thao tác trên các hàm nội bộ trong cùng một tiến trình không phơi bày ra qua giao thức mạng.
- Khi thay đổi logic thuần túy ở tầng dữ liệu mà không làm thay đổi contract API.

## 4. Prerequisites & Input Context
- Yêu cầu nghiệp vụ hoặc đặc tả giao diện người dùng cần tiêu thụ dữ liệu.
- Quy chuẩn API hiện tại của dự án (Quy ước đặt tên URL, chuẩn phân trang, format ngày tháng).
- Bộ công cụ định nghĩa schema (OpenAPI / Swagger, GraphQL SDL, Protobuf, Zod, Pydantic).

## 5. Core Concepts & Taxonomy
- **Nguyên tắc cốt lõi**: Tuân thủ triệt để nguyên lý vận hành xác định và ranh giới trách nhiệm của chuẩn Agent Skills.
- **Tính nhất quán hệ thống**: Mọi thao tác phải có thể kiểm chứng độc lập với kết quả đo lường rõ ràng.
- **Ngăn ngừa hồi quy**: Bất kỳ sửa đổi nào cũng phải bảo vệ tính tương thích ngược và chất lượng đã được nghiệm thu.

## 6. Step-by-Step Execution Workflow
### Bước 1: Thiết Kế Định Dạng Endpoint Chuẩn RESTful (Contract Design)
- Đặt tên URI bằng danh từ số nhiều, đại diện cho tài nguyên:
  - `GET /api/v1/orders` (Lấy danh sách đơn hàng).
  - `POST /api/v1/orders` (Tạo đơn hàng mới).
  - `GET /api/v1/orders/:id` (Lấy chi tiết đơn hàng).
  - `PUT /api/v1/orders/:id` (Cập nhật toàn bộ đơn hàng).
  - `PATCH /api/v1/orders/:id` (Cập nhật một phần đơn hàng).
  - `DELETE /api/v1/orders/:id` (Xóa/Hủy đơn hàng).
- Tránh đưa động từ vào URI (ví dụ: cấm `POST /api/v1/createOrder`).

### Bước 2: Chuẩn Hóa Định Dạng Phản Hồi & Phân Trang (Standardized Response Envelope)
- Mọi phản hồi JSON đều tuân theo cấu trúc nhất quán:
  ```json
  {
    "success": true,
    "data": { ... },
    "meta": {
      "page": 1,
      "limit": 20,
      "total": 150
    }
  }
  ```
- Định dạng lỗi thống nhất (RFC 7807 Problem Details):
  ```json
  {
    "success": false,
    "error": {
      "code": "ORDER_NOT_FOUND",
      "message": "Không tìm thấy đơn hàng với mã ID đã cung cấp"
    }
  }
  ```

### Bước 3: Xác Thực Dữ Liệu Đầu Vào Chặt Chẽ (Input Validation)
- Validate 100% các trường trong Body, Query Params và Path Params bằng schema (Zod/Pydantic/Joi).
- Tự động từ chối ngay với mã `400 Bad Request` nếu payload không hợp lệ, nêu rõ trường bị lỗi.

### Bước 4: Bảo Vệ & Phân Quyền (Auth Middleware & Rate Limiting)
- Tích hợp middleware kiểm tra token xác thực (JWT/Bearer token).
- Kiểm tra quyền hạn của user đối với tài nguyên trước khi chuyển vào controller.
- Áp dụng Rate Limiting (ví dụ tối đa 60 requests/phút cho mỗi IP/User) để bảo vệ server khỏi tấn công lạm dụng.

### Bước 5: Kiểm Thử Hợp Đồng API (Contract & Integration Testing)
- Viết integration test (sử dụng Supertest, Requests, Postman Newman):
  - Test mã HTTP trả về đúng chuẩn (`200 OK`, `201 Created`, `400 Bad Request`, `401 Unauthorized`, `403 Forbidden`, `404 Not Found`).
  - Kiểm tra schema JSON của dữ liệu trả về không bị thiếu hoặc đổi kiểu.

### Bước 6: Duy Trì Tương Thích Ngược & Versioning (Backward Compatibility)
- Khi nâng cấp: Không được xóa trường cũ hoặc đổi kiểu dữ liệu của trường đang có trên phiên bản API hiện tại.
- Nếu bắt buộc có breaking changes: Tạo phiên bản mới (`/api/v2/...`) và giữ nguyên `/api/v1/...` trong thời gian chuyển đổi.

## 7. Concrete Examples
```bash
# Lệnh thực thi & kiểm chứng tiêu chuẩn
dex verify --skill dex-api-engineering
```

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước xác minh tự động và dựa vào giả định chủ quan.
- **Anti-Pattern 2**: Thay đổi diện rộng vượt ngoài phạm vi (Scope Creep) làm mất kiểm soát rủi ro.
- **Trap**: Thực hiện thao tác phá hủy hoặc thay đổi trạng thái sản xuất khi chưa qua cổng kiểm duyệt an toàn.

## 9. Quality Gates & Acceptance Criteria
- **QG-02 (API Contract Compliant)**: Schema input/output khớp chính xác 100% với tài liệu đặc tả OpenAPI.
- **QG-03 (Strict Validation)**: Tất cả các trường dữ liệu đều được xác thực kiểu dữ liệu chặt chẽ.
- **QG-05 (API Integration Tests PASS)**: Tất cả bài test API (cả Happy path và Edge cases) đạt PASS.

## 10. Security & Safety Boundaries
- **Cấm Breaking Changes Không Cảnh Báo**: Cấm tự ý xóa trường hoặc đổi tên thuộc tính trong JSON response khi chưa nâng version API.
- **Mã HTTP Status Phải Đúng Bản Chất**: Cấm trả về `200 OK` kèm theo body chứa `{"error": "Lỗi xảy ra"}`. Lỗi client phải dùng `4xx`, lỗi máy chủ phải dùng `5xx`.
- **Luôn Có Phân Trang Cho Danh Sách**: Không bao giờ tạo endpoint trả về danh sách mảng mà không có giới hạn `limit`/`page` tối đa (tránh việc trả về 100,000 bản ghi làm tràn RAM server và client).

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Kích hoạt thông qua terminal hoặc tiện ích mở rộng IDE tương thích (VS Code, Cursor, Windsurf).

## 12. Deliverables & Output Artifacts
1. Mã nguồn API endpoint kèm validation schema hoàn chỉnh.
2. Bộ bài kiểm thử tích hợp (Integration Tests) kiểm chứng mã HTTP và schema.
3. Tài liệu đặc tả API (OpenAPI spec hoặc Postman collection).

## 13. Related & Complementary Skills
- `dex-master-orchestrator`: Điều phối trung tâm.

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Kỹ sư hoặc AI Agent kích hoạt **dex-api-engineering** trong dự án.
1. Tiếp nhận ngữ cảnh đầu vào và kiểm tra điều kiện tiên quyết tại Mục 4.
2. Vận hành tuần tự các bước theo Quy trình tại Mục 6.
3. Kiểm chứng đầu ra đối chiếu với Tiêu chuẩn chấp thuận tại Mục 9.
4. Bàn giao đầy đủ hiện vật theo Mục 12 và cập nhật tài liệu liên quan.
