---
name: dex-api-contract-evolution
description: Manage API contract evolution, backward compatibility guarantees, schema diffing, deprecation policies, sunset headers, migration adapters, and versioning strategies. Use when modifying existing APIs, deprecating endpoints, or introducing breaking changes.
---

# dex-api-contract-evolution

## 1. Purpose & Scope
Quản lý quá trình tiến hóa hợp đồng giao diện lập trình ứng dụng (API Contract Evolution); đảm bảo tính tương thích ngược tuyệt đối (Backward Compatibility Guarantees), tự động phát hiện các thay đổi phá vỡ tương thích (Breaking Changes Diffing), thiết lập chính sách ngừng hỗ trợ có lộ trình (Deprecation Policies & Sunset HTTP Headers), xây dựng các adapter chuyển đổi dữ liệu và chiến lược phiên bản hóa (Versioning Strategies: URL Path, Header, Content Negotiation).

## 2. When to Use
- Khi cần thay đổi cấu trúc dữ liệu của một API đang phục vụ hàng triệu ứng dụng di động hoặc khách hàng bên thứ ba.
- Khi cần xóa bỏ hoặc tái cấu trúc một trường dữ liệu đã lỗi thời mà không làm crash các phiên bản app cũ chưa kịp nâng cấp.
- Khi cần nâng cấp từ API v1 lên API v2 một cách an toàn và êm thắm.

## 3. When NOT to Use
- API nội bộ dùng cho một tác vụ tạm thời chưa từng có bên nào tích hợp.
- Thiết kế API mới từ đầu chưa có người dùng (dùng `dex-api-engineering`).

## 4. Prerequisites & Input Context
**Đầu vào cần thiết:**
- Bản đặc tả API hiện tại và bản đặc tả API đề xuất (OpenAPI / Swagger specs, GraphQL schemas, Protobuf files).
- Danh sách các bên đang tiêu thụ API và phiên bản họ đang sử dụng.
- Lộ trình ngừng hỗ trợ dự kiến (Deprecation Timeline: Tối thiểu 90 ngày).

**Điều kiện tiên quyết:**
- Bản đặc tả API OpenAPI được quản lý theo phiên bản trong Git.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**: Nắm vững cơ chế vận hành theo chuẩn Agent Skills, tuân thủ nghiêm ngặt tính xác định và ranh giới trách nhiệm.
- **Quy tắc quyết định kỹ thuật**:
- **Không Được Phép Đưa Ra Breaking Change Đột Ngột**: Mọi thay đổi phá vỡ tương thích phải có thông báo deprecation trước tối thiểu 90 ngày kèm Sunset header.
- **Ưu Tiên Tiến Hóa Tự Nhiên Hơn Là Tăng Phiên Bản Lớn**: Thay vì tạo `/api/v2/` cho một thay đổi nhỏ, ưu tiên thêm trường mới không bắt buộc vào `/api/v1/`.
- **Chặn Breaking Changes Tự Động Trong CI**: Pipeline CI phải tự động fail nếu phát hiện breaking change không được phê duyệt thông qua schema diffing.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Ứng dụng iOS của khách hàng bị crash khi mở app**: Do backend vừa đổi trường `user_name` thành `username` -> Khắc phục: Schema diffing chặn commit trong CI; giữ lại trường `user_name` cũ và trả về song song cả 2 trường.
- **Khách hàng bên thứ ba phàn nàn vì API bị tắt bất ngờ**: Do không có thông báo -> Khắc phục: Gửi header `Sunset` và gửi email cảnh báo tự động tới các tài khoản có phát sinh lưu lượng vào endpoint cũ.

## 6. Step-by-Step Execution Workflow
1. Thực hiện so sánh tự động (Automated Schema Diffing) giữa schema cũ và schema mới bằng công cụ `oasdiff` hoặc `graphql-inspector`.
2. Phân loại các thay đổi theo mức độ rủi ro:
   - *Tương thích ngược (Non-breaking)*: Thêm endpoint mới, thêm trường tùy chọn (optional field) vào response.
   - *Phá vỡ tương thích (Breaking)*: Xóa endpoint, đổi tên trường, đổi kiểu dữ liệu, thêm trường bắt buộc (required field) vào request.
3. Nếu bắt buộc phải thay đổi cấu trúc: Áp dụng mô hình Mở rộng và Thu hẹp (Expand and Contract Pattern). Tạo trường mới song song với trường cũ và duy trì cả hai trong giai đoạn chuyển tiếp.
4. Đánh dấu trường cũ là Deprecated trong OpenAPI schema và gắn HTTP headers chuẩn RFC 8594 (`Deprecation: true`, `Sunset: Wed, 11 Nov 2026 00:00:00 GMT`).
5. Cung cấp Adapter Middleware để tự động ánh xạ dữ liệu qua lại giữa cấu trúc cũ và mới.
6. Theo dõi số liệu lưu lượng gọi vào endpoint cũ để xác định khi nào lưu lượng về 0 trước khi chính thức xóa bỏ hoàn toàn.

## 7. Concrete Examples
### Ví dụ triển khai chuẩn mực:
```typescript
// deprecation.middleware.ts - RFC 8594 Sunset Header Injection
import { Request, Response, NextFunction } from 'express';

export function deprecationNotice(sunsetDate: string, docUrl: string) {
  return (req: Request, res: Response, next: NextFunction) => {
    res.setHeader('Deprecation', 'true');
    res.setHeader('Sunset', sunsetDate);
    res.setHeader('Link', `<${docUrl}>; rel="sunset-documentation"`);
    next();
  };
}
```

### Lệnh xác minh & thực thi:
- So sánh schema tìm breaking changes: `oasdiff breaking current-spec.yaml new-spec.yaml`
- Kiểm tra tính tương thích GraphQL: `npx graphql-inspector diff old.graphql new.graphql`
- Kiểm tra Sunset header trả về: `curl -i https://api.dex.dev/v1/orders` (tìm header `Sunset:` và `Deprecation:`)

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước kiểm tra biên và giả định hệ thống luôn ở trạng thái lý tưởng.
- **Anti-Pattern 2**: Không ghi nhận nhật ký kiểm toán hoặc bỏ qua việc xử lý ngoại lệ lúc runtime.
- **Trap**: Bỏ qua các rào chắn an toàn hoặc cố tình chạy script không qua kiểm thử tự động.

## 9. Quality Gates & Acceptance Criteria
- QG-06: 0 breaking changes không được phê duyệt trong schema diff so với phiên bản phát hành gần nhất.
- QG-10: Các endpoint bị deprecate đều có đầy đủ header `Sunset` và tài liệu hướng dẫn chuyển đổi (Migration Guide).
- Mọi thay đổi phải vượt qua bài kiểm thử tự động trước khi coi là hoàn thành.

## 10. Security & Safety Boundaries
- Đảm bảo các adapter chuyển đổi tương thích cũ vẫn thực thi đầy đủ các biện pháp xác thực và kiểm soát quyền hạn như phiên bản mới.
- Không bao giờ thực thi mã nguồn hoặc thay đổi cấu hình trên môi trường sản xuất mà thiếu cơ chế rollback an toàn.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Có thể kích hoạt trực tiếp từ terminal hoặc extension tương thích trong VS Code / Cursor / Windsurf.

## 12. Deliverables & Output Artifacts
- Báo cáo phân tích khác biệt schema (API Diff Report).
- Bản đặc tả OpenAPI cập nhật kèm các thẻ `@deprecated`.
- Adapter middleware chuyển đổi dữ liệu tương thích ngược.

## 13. Related & Complementary Skills
- `dex-development-workflow`: Quy trình phát triển tiêu chuẩn.
- `dex-code-verification`: Xác minh chất lượng và tính đúng đắn của mã nguồn.
- `dex-master-orchestrator`: Bộ điều phối trung tâm kết nối kỹ năng này với các kỹ năng khác trong hệ thống.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư hoặc AI Agent tiếp nhận yêu cầu liên quan đến **dex-api-contract-evolution**.
1. Đọc kỹ đầu vào và các ràng buộc kỹ thuật tại mục 4.
2. Thực thi tuần tự 6 bước trong Workflow tại mục 6.
3. Chạy các lệnh kiểm chứng tại mục 7 và đối chiếu với Quality Gates tại mục 9.
4. Đóng gói deliverables theo danh sách tại mục 12 và báo cáo kết quả kèm bằng chứng xác thực.
