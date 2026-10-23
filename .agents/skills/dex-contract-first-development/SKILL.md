---
name: dex-contract-first-development
description: Architect and enforce contract-first API development using OpenAPI, Protobuf, or AsyncAPI schemas with automated code generation, mock servers, and breaking change diffing. Use when coordinating cross-team APIs or building resilient service contracts.
---

# dex-contract-first-development

## 1. Purpose & Scope
Thiết lập và thực thi phương pháp phát triển hướng hợp đồng (Contract-First Development); sử dụng các đặc tả OpenAPI, Protocol Buffers hoặc AsyncAPI làm nguồn chân lý duy nhất (Single Source of Truth), tự động sinh mã nguồn client/server, dựng mock server cho frontend song song, và tự động phát hiện thay đổi phá vỡ tương thích (breaking changes).

## 2. When to Use
- Khi phát triển API phục vụ cho nhiều đội ngũ độc lập (Frontend, Mobile, Third-party partners).
- Khi muốn đội ngũ client có thể tiến hành phát triển và kiểm thử ngay lập tức dựa trên mock server mà không cần chờ backend viết xong.
- Khi cần ngăn chặn các sự cố tương thích phiên bản trước khi triển khai lên môi trường thử nghiệm.

## 3. When NOT to Use
- Khi xây dựng các script nhỏ dùng nội bộ dùng một lần không có sự phân tách giữa client và server.
- Khi cấu trúc API đang thay đổi liên tục từng giờ trong giai đoạn hackathon sơ khai.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Đặc tả nghiệp vụ, công cụ schema linter (Spectral, buf), công cụ sinh mã (OpenAPI Generator, protoc).
- **Quyền hạn truy cập:** Quyền quản lý kho lưu trữ schema hợp đồng tập trung (Schema Registry hoặc Git repo).

## 5. Core Concepts & Taxonomy
- **Single Source of Truth:** Schema tệp đặc tả là chuẩn mực tối cao; code server và client đều được sinh tự động hoặc kiểm thử đối soát với schema này.
- **Breaking Change Detection:** Tự động so sánh phiên bản schema mới với phiên bản đã phát hành trước đó trong CI/CD để phát hiện vi phạm quy tắc tương thích.
- **Prism / Mock Server:** Công cụ tự động tạo HTTP server giả lập trả về dữ liệu mẫu chuẩn theo schema mà không cần viết mã backend.

## 6. Step-by-Step Execution Workflow
1. Viết bản thiết kế hợp đồng API bằng OpenAPI v3.1 hoặc Protobuf v3 trước khi viết bất kỳ dòng mã backend nào.
2. Chạy linter kiểm tra chuẩn đặt tên, tài liệu hóa trường dữ liệu và bảo mật bằng Spectral hoặc Buf lint.
3. Khởi tạo mock server tự động để các đội ngũ Frontend và Mobile bắt đầu tích hợp ngay.
4. Sử dụng công cụ sinh mã tự động để sinh ra Server Interfaces và Client SDKs cho các ngôn ngữ đích.
5. Cài đặt kiểm tra breaking changes trong CI pipeline so sánh với branch chính (ví dụ: `buf breaking` hoặc `oasdiff`).
6. Triển khai backend thực tế dựa trên Server Interfaces đã sinh và chạy kiểm thử contract test để chứng minh tính tương thích.

## 7. Concrete Examples
### Ví dụ quy trình kiểm tra breaking changes và sinh mã từ OpenAPI trong CI (`buf` / `oasdiff`):
```bash
# 1. Kiểm tra linter chất lượng của OpenAPI schema
npx spectral lint specs/order-service-api.yaml

# 2. Khởi tạo mock server tức thời cho đội Frontend
npx prism mock specs/order-service-api.yaml -p 4010 &

# 3. Kiểm tra thay đổi phá vỡ tương thích so với bản phát hành trước trên Git
oasdiff -base main.yaml -revision specs/order-service-api.yaml -fail-on-breaking

# 4. Tự động sinh TypeScript API Client SDK
npx @openapitools/openapi-generator-cli generate \
  -i specs/order-service-api.yaml \
  -g typescript-axios \
  -o generated/clients/typescript
```

## 8. Anti-Patterns & Common Traps
- **Code-First Drift:** Viết code backend xong rồi dùng annotation để sinh ngược lại schema, dẫn tới schema bị méo mó theo ngôn ngữ lập trình và mất tính trung lập.
- **Uncommunicated Schema Mutations:** Tự ý sửa đổi kiểu dữ liệu của một trường trong API mà không thông qua quy trình review hợp đồng.
- **Handcrafted Client SDKs:** Tự viết tay hàng ngàn dòng code gọi API trên client dẫn tới dễ sai sót chính tả và tốn công bảo trì.

## 9. Quality Gates & Acceptance Criteria
- **QG-02**: Schema đặc tả hợp đồng vượt qua 100% các bài kiểm tra linter theo bộ quy tắc của tổ chức.
- **QG-08**: Không có breaking change nào xuất hiện mà không được tăng số phiên bản Major theo chuẩn SemVer.
- **QG-09**: Tất cả các trường dữ liệu và mã lỗi HTTP đều có mô tả tài liệu chi tiết.

## 10. Security & Safety Boundaries
- Bắt buộc định nghĩa cơ chế bảo mật (Security Schemes như OAuth2, Bearer JWT, APIKey) trực tiếp trong schema hợp đồng.
- Xác định rõ ràng các trường dữ liệu bắt buộc và kiểm tra giới hạn kích thước payload (max length, regex format) để phòng chống DoS.

## 11. Platform Adapters
- **OpenAPI Tools**: Spectral, Prism, OpenAPI Generator, oasdiff.
- **Protobuf / gRPC Tools**: Buf CLI, protoc, grpc-gateway.
- **AsyncAPI**: AsyncAPI Studio, Generator.

## 12. Deliverables & Output Artifacts
- Tệp đặc tả hợp đồng API chuẩn hóa (`.yaml` hoặc `.proto`).
- SDK client được sinh tự động cho các nền tảng client.
- Báo cáo kiểm tra tương thích ngược tự động từ CI.

## 13. Related & Complementary Skills
dex-api-engineering, dex-architecture-decision-records, dex-semantic-version-automation

## 14. Realistic Usage Example
```powershell
# Chạy công cụ kiểm tra vi phạm tương thích ngược của hợp đồng API
oasdiff -base specs/v1.0.0.yaml -revision specs/v1.1.0.yaml -fail-on-breaking
```
