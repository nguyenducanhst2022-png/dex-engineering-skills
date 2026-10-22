---
name: dex-idempotent-operations
description: Design strictly idempotent API endpoints, distributed idempotency keys, duplicate request filtering, and atomic token reservations. Use when processing payments, money transfers, external webhooks, or preventing double-charge operations.
---

# dex-idempotent-operations

## 1. Purpose & Scope
Thiết kế và triển khai cơ chế xử lý bất biến lặp lại (Idempotent Operations) cho các API và tác vụ quan trọng; đảm bảo một yêu cầu dù được gửi lại nhiều lần (do mạng lag, người dùng click liên tiếp hoặc hệ thống retry tự động) thì hệ thống chỉ thực thi nghiệp vụ duy nhất một lần và luôn trả về kết quả đồng nhất, triệt tiêu hoàn toàn rủi ro trừ tiền hai lần hoặc tạo đơn hàng trùng lặp.

## 2. When to Use
- Khi xây dựng các API liên quan trực tiếp đến tiền tệ, điểm thưởng hoặc thay đổi số dư ví.
- Khi xử lý các Webhook từ các nhà cung cấp bên thứ ba (Stripe, VNPay, PayPal, GitHub) vì Webhook luôn cam kết At-Least-Once Delivery.
- Khi triển khai cơ chế retry tự động cho các lời gọi mạng bất ổn định.

## 3. When NOT to Use
- Các câu truy vấn đọc dữ liệu (`GET`, `HEAD`) vốn dĩ đã có tính Idempotent tự nhiên theo chuẩn HTTP.
- Các thao tác cập nhật dữ liệu hàng loạt không có rủi ro trùng lặp.

## 4. Prerequisites & Input Context
**Đầu vào cần thiết:**
- Tên header định danh (thông thường là `Idempotency-Key` hoặc `X-Request-ID`).
- Thời gian sống của Idempotency Key (TTL, ví dụ: 24 giờ).
- Bộ lưu trữ trạng thái khóa (Redis hoặc bảng `idempotency_keys` trong PostgreSQL).

**Điều kiện tiên quyết:**
- Có hệ thống lưu trữ phân tán có khả năng ghi nguyên tử (Atomic Write) với TTL (như Redis).
- Client cam kết sinh một chuỗi UUID duy nhất cho mỗi thao tác người dùng độc lập.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**: Nắm vững cơ chế vận hành theo chuẩn Agent Skills, tuân thủ nghiêm ngặt tính xác định và ranh giới trách nhiệm.
- **Quy tắc quyết định kỹ thuật**:
- **Kiểm Tra Hash Payload**: Khi nhận cùng một `Idempotency-Key`, phải kiểm tra xem `sha256(request_body)` có khớp với request lần đầu không; nếu cùng Key nhưng Body lại khác nhau, lập tức từ chối với lỗi `400 Bad Request - Idempotency Key Reuse With Different Payload`.
- **Lưu Cả Status Code & Headers**: Phản hồi cached của Idempotency phải giữ nguyên mã HTTP ban đầu (ví dụ: `201 Created` kèm các header liên quan).
- **Bắt Buộc Cho Mọi Webhook**: 100% Webhook Controllers bắt buộc phải có bước kiểm tra Idempotency trước khi xử lý.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Server sập giữa lúc đang xử lý**: Khóa bị kẹt ở trạng thái `PROCESSING` vĩnh viễn -> Khắc phục: Khóa `PROCESSING` chỉ có TTL ngắn (120 giây) để tự động giải phóng nếu tiến trình server chết đột ngột.
- **Khách hàng bấm 2 lần thật nhanh làm 2 thread cùng chạy**: Do không dùng lệnh nguyên tử `SET NX` -> Khắc phục: Bắt buộc dùng atomic primitives của Redis hoặc Database Unique Constraint.

## 6. Step-by-Step Execution Workflow
1. Client gửi request kèm header: `Idempotency-Key: <UUID>`.
2. Máy chủ tiếp nhận và trích xuất `Idempotency-Key` qua Middleware.
3. Máy chủ cố gắng tạo một khóa phân tán trong Redis với trạng thái `PROCESSING`: `SET idempotency:<key> 'PROCESSING' NX EX 120`.
   - **Nếu khóa đã tồn tại với trạng thái `COMPLETED`**: Lập tức trả về phản hồi đã lưu trong cache mà không chạy lại nghiệp vụ.
   - **Nếu khóa đang ở trạng thái `PROCESSING`**: Trả về lỗi `409 Conflict` hoặc chờ kết quả (tránh 2 request chạy song song cùng lúc).
   - **Nếu tạo khóa thành công**: Cho phép request đi tiếp vào controller nghiệp vụ.
4. Controller thực thi logic nghiệp vụ (ví dụ trừ tiền, tạo hóa đơn).
5. Sau khi nghiệp vụ hoàn tất: Cập nhật khóa trong Redis sang trạng thái `COMPLETED` kèm toàn bộ HTTP Status Code và Body phản hồi với TTL 24 giờ.
6. Nếu nghiệp vụ bị lỗi ngoại lệ bất ngờ: Xóa khóa để client có thể thử lại sau.

## 7. Concrete Examples
### Ví dụ triển khai chuẩn mực:
```typescript
// src/middleware/idempotency.ts
export async function idempotencyMiddleware(req: Request, res: Response, next: NextFunction) {
  const key = req.header('Idempotency-Key');
  if (!key) return next();
  
  const cacheKey = `idemp:${req.userId}:${key}`;
  const payloadHash = crypto.createHash('sha256').update(JSON.stringify(req.body)).digest('hex');
  
  const existing = await redis.get(cacheKey);
  if (existing) {
    const parsed = JSON.parse(existing);
    if (parsed.hash !== payloadHash) return res.status(400).json({ error: 'Idempotency key reused with different payload' });
    return res.status(parsed.status).json(parsed.body);
  }
  // Tiến hành xử lý...
  next();
}
```

### Lệnh xác minh & thực thi:
- Bắn 2 request giống hệt nhau có cùng Idempotency-Key: `curl -H 'Idempotency-Key: key-123' ...`
- Chạy unit/integration test xử lý trùng lặp: `npm test -- tests/api/idempotency.spec.ts`
- Kiểm tra trạng thái key trong Redis: `redis-cli get idempotency:key-123`

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước kiểm tra biên và giả định hệ thống luôn ở trạng thái lý tưởng.
- **Anti-Pattern 2**: Không ghi nhận nhật ký kiểm toán hoặc bỏ qua việc xử lý ngoại lệ lúc runtime.
- **Trap**: Bỏ qua các rào chắn an toàn hoặc cố tình chạy script không qua kiểm thử tự động.

## 9. Quality Gates & Acceptance Criteria
- QG-02: Bắn 10 request đồng thời có cùng Idempotency-Key chỉ tạo ra duy nhất 1 đơn hàng trong cơ sở dữ liệu.
- QG-05: 10/10 request đều nhận được cùng một phản hồi JSON với mã HTTP `201 Created`.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động trước khi coi là hoàn thành.

## 10. Security & Safety Boundaries
- Idempotency Key phải được liên kết chặt chẽ với `userId` hoặc `tenantId` đã xác thực; không cho phép user A đọc kết quả của user B bằng cách đoán mò Idempotency-Key.
- Không bao giờ thực thi mã nguồn hoặc thay đổi cấu hình trên môi trường sản xuất mà thiếu cơ chế rollback an toàn.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Có thể kích hoạt trực tiếp từ terminal hoặc extension tương thích trong VS Code / Cursor / Windsurf.

## 12. Deliverables & Output Artifacts
- Middleware Idempotency tái sử dụng (`src/middleware/idempotencyMiddleware.ts`).
- Bảng lưu trữ hoặc Redis Adapter tương ứng.
- File kiểm thử bắn request đồng thời kiểm chứng kết quả.

## 13. Related & Complementary Skills
- `dex-development-workflow`: Quy trình phát triển tiêu chuẩn.
- `dex-code-verification`: Xác minh chất lượng và tính đúng đắn của mã nguồn.
- `dex-master-orchestrator`: Bộ điều phối trung tâm kết nối kỹ năng này với các kỹ năng khác trong hệ thống.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư hoặc AI Agent tiếp nhận yêu cầu liên quan đến **dex-idempotent-operations**.
1. Đọc kỹ đầu vào và các ràng buộc kỹ thuật tại mục 4.
2. Thực thi tuần tự 6 bước trong Workflow tại mục 6.
3. Chạy các lệnh kiểm chứng tại mục 7 và đối chiếu với Quality Gates tại mục 9.
4. Đóng gói deliverables theo danh sách tại mục 12 và báo cáo kết quả kèm bằng chứng xác thực.
