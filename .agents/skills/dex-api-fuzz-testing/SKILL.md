---
name: dex-api-fuzz-testing
description: Execute coverage-guided and schema-based API fuzz testing (Schemathesis, RESTler) to discover 500 errors, unhandled boundary exceptions, memory leaks, and serialization flaws. Use when hardening REST/GraphQL APIs before production deployment.
---

# dex-api-fuzz-testing

## 1. Purpose & Scope
Thực hiện kiểm thử mờ (Fuzz Testing) tự động trên các giao diện API (REST, GraphQL, gRPC) dựa trên OpenAPI/GraphQL schema, bơm hàng nghìn payload dị dạng, giá trị biên cực đoan và kiểu dữ liệu bất thường để phát hiện lỗi unhandled exceptions (HTTP 500), crash server hoặc rò rỉ dữ liệu.

## 2. When to Use
- Chuẩn bị phát hành phiên bản API public ra bên ngoài hoặc cho bên thứ ba tích hợp.
- Cần kiểm tra độ bền vững (resilience) của input validation layer.
- Sau khi tái cấu trúc lớn bộ phân giải JSON/gRPC parser.

## 3. When NOT to Use
- Không chạy API fuzzing trực tiếp trên môi trường Production đang phục vụ khách hàng thực tế.
- Không dùng để kiểm thử luồng UI tương tác của người dùng.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- OpenAPI Specification (swagger.json/openapi.yaml) hoặc GraphQL Schema.
- URL endpoint của môi trường Staging/Test được cấp quyền.
- Thông tin xác thực (Bearer token / API key) của tài khoản test cô lập.
- **Điều kiện tiên quyết**:
- Môi trường Staging đã được backup dữ liệu và có thể rollback nhanh chóng.
- Rate limit của môi trường test được điều chỉnh phù hợp cho công cụ fuzz.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Schema-based Fuzzing: Dựa trên schema để sinh dữ liệu có cấu trúc hợp lệ về mặt cú pháp nhưng chứa giá trị biên nguy hiểm (ví dụ: chuỗi dài 1MB, số âm cực đại, null bytes, unicode đặc thù).
- Server Invariant: API không bao giờ được trả về mã lỗi HTTP 500 (Internal Server Error) bất kể payload đầu vào là gì (phải trả về 400 Bad Request hoặc 422 Unprocessable Entity).
- **Quy tắc quyết định kỹ thuật**:
- Nếu bất kỳ request nào kích hoạt HTTP 500: ghi lại payload tối thiểu (minimal reproducible curl) và phân loại là P1 defect.
- Nếu API bị crash hoặc rò rỉ stack trace: đánh dấu security vulnerability.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Fuzzer tạo ra quá nhiều bản ghi rác làm đầy cơ sở dữ liệu test (cần cấu hình tự động dọn dẹp hoặc dùng database in-memory).

## 6. Step-by-Step Execution Workflow
1. Tải và kiểm tra tính hợp lệ của OpenAPI specification.
2. Cấu hình phạm vi endpoints cho phép fuzz và cấp test auth token.
3. Chạy Schemathesis hoặc RESTler với kiểm tra các HTTP status invariants.
4. Phân loại các lỗi HTTP 500 và lỗi timeout thành danh sách reproduction steps.
5. Sửa lỗi validation trong backend và chạy regression fuzzing.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```bash
schemathesis run http://localhost:8080/api/v1/openapi.json \
  --header "Authorization: Bearer test-token" \
  --checks all \
  --max-response-time 500 \
  --hypothesis-max-examples 200
```

### Lệnh xác minh & thực thi:
```bash
# Xác minh bằng replay curl được sinh ra từ failure log
curl -X POST http://localhost:8080/api/v1/orders -H 'Content-Type: application/json' -d '{"quantity": -9223372036854775808}'
```

## 8. Anti-Patterns & Common Traps
- Fuzzing vào endpoint gửi email thật gây spam người dùng.
- Bỏ qua các lỗi HTTP 500 với lý do 'người dùng bình thường không bao giờ nhập thế này'.

## 9. Quality Gates & Acceptance Criteria
- 0 lỗi HTTP 500 phát hiện được qua 10,000 requests fuzzed trên schema.
- Mọi lỗi input validation phải trả về 4xx kèm error message cấu trúc an toàn.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Chỉ thực hiện trên môi trường test nội bộ đã được cấp quyền văn bản.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ thống hỗ trợ**: Linux (CI/CD runners), macOS, Windows 11 PowerShell/WSL2.

## 12. Deliverables & Output Artifacts
- Báo cáo tổng hợp Schemathesis JSON/HTML.
- Danh sách cURL reproducer cho từng lỗi phát hiện được.

## 13. Related & Complementary Skills
dex-contract-first-development, dex-api-abuse-prevention, dex-sast-finding-triage

## 14. Realistic Usage Example
### Tình huống thực tế:
Đội ngũ fintech kiểm tra endpoint chuyển tiền bằng Schemathesis, phát hiện khi gửi số tiền dưới dạng số thực thập phân có 300 chữ số làm microservice Java ném `NumberFormatException` và sập pod. Đội ngũ đã thêm validation regex ngay tại API Gateway.
