---
name: dex-api-engineering
description: Production-grade API design, RESTful and GraphQL specifications, input schema validation, authentication middleware, error standardization, and backward compatibility contracts. Prevents breaking changes and enforces robust API contracts. Use when creating endpoints, updating API schemas, or contract testing.
---

# DEX API Engineering

## 1. Purpose
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

## 3. When Not to Use
- Thao tác trên các hàm nội bộ trong cùng một tiến trình không phơi bày ra qua giao thức mạng.
- Khi thay đổi logic thuần túy ở tầng dữ liệu mà không làm thay đổi contract API.

## 4. Inputs
- Yêu cầu nghiệp vụ hoặc đặc tả giao diện người dùng cần tiêu thụ dữ liệu.
- Quy chuẩn API hiện tại của dự án (Quy ước đặt tên URL, chuẩn phân trang, format ngày tháng).
- Bộ công cụ định nghĩa schema (OpenAPI / Swagger, GraphQL SDL, Protobuf, Zod, Pydantic).

## 5. Workflow

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

## 6. Quality Gates
- **QG-02 (API Contract Compliant)**: Schema input/output khớp chính xác 100% với tài liệu đặc tả OpenAPI.
- **QG-03 (Strict Validation)**: Tất cả các trường dữ liệu đều được xác thực kiểu dữ liệu chặt chẽ.
- **QG-05 (API Integration Tests PASS)**: Tất cả bài test API (cả Happy path và Edge cases) đạt PASS.

## 7. Safety Rules
- **Cấm Breaking Changes Không Cảnh Báo**: Cấm tự ý xóa trường hoặc đổi tên thuộc tính trong JSON response khi chưa nâng version API.
- **Mã HTTP Status Phải Đúng Bản Chất**: Cấm trả về `200 OK` kèm theo body chứa `{"error": "Lỗi xảy ra"}`. Lỗi client phải dùng `4xx`, lỗi máy chủ phải dùng `5xx`.
- **Luôn Có Phân Trang Cho Danh Sách**: Không bao giờ tạo endpoint trả về danh sách mảng mà không có giới hạn `limit`/`page` tối đa (tránh việc trả về 100,000 bản ghi làm tràn RAM server và client).

## 8. Expected Outputs
1. Mã nguồn API endpoint kèm validation schema hoàn chỉnh.
2. Bộ bài kiểm thử tích hợp (Integration Tests) kiểm chứng mã HTTP và schema.
3. Tài liệu đặc tả API (OpenAPI spec hoặc Postman collection).

## 9. Failure Handling
- Nếu người dùng client gửi dữ liệu sai định dạng: Trả về mã lỗi 400 rõ ràng kèm danh sách chi tiết các trường cần sửa, không được để crash tiến trình server.

## 10. Completion Criteria
- API hoạt động đúng chuẩn RESTful/GraphQL, phân trang và mã lỗi nhất quán.
- Bộ test tích hợp đạt 100% PASS và tài liệu API được cập nhật đầy đủ.

---

## Real-world Example
Endpoint tạo bài viết mới `POST /api/v1/posts`:
```typescript
// Validation schema chặt chẽ
const CreatePostSchema = z.object({
  title: z.string().min(5).max(100),
  content: z.string().min(20),
  tags: z.array(z.string()).max(5).optional()
});

router.post('/posts', authenticate, validate(CreatePostSchema), async (req, res) => {
  const post = await postService.create(req.userId, req.validatedBody);
  res.status(201).json({ success: true, data: post });
});
```
Test kiểm tra: Gửi title rỗng trả về đúng `400 Bad Request`, gửi hợp lệ trả về đúng `201 Created`.
