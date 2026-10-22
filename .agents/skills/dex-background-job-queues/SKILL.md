---
name: dex-background-job-queues
description: Architect robust background job processing with message queues (BullMQ/Celery/Sidekiq), dead-letter queues (DLQ), rate limiting, worker concurrency, and progress tracking. Use when offloading slow tasks, sending bulk emails, or processing asynchronous workflows.
---

# dex-background-job-queues

## 1. Purpose & Scope
Thiết kế và triển khai hệ thống xử lý tác vụ chạy ngầm bất đồng bộ (Background Job Processing) sử dụng hàng đợi thông điệp (BullMQ, Celery, SQS); giải phóng luồng chính của máy chủ, đảm bảo tác vụ nặng (gửi email hàng loạt, xử lý video, xuất báo cáo) được thực hiện bền bỉ, có cơ chế Dead-Letter Queue (DLQ) cách ly lỗi và theo dõi tiến độ thời gian thực.

## 2. When to Use
- Khi một API endpoint mất quá nhiều thời gian (>1-2 giây) để phản hồi do phải gửi email, tạo PDF hoặc gọi nhiều API bên thứ ba.
- Khi cần xử lý các tác vụ có tải đột biến (Spike) mà không làm sập server chính.
- Khi cần lập lịch chạy lại các tác vụ thất bại một cách có kiểm soát kèm giãn cách số mũ.

## 3. When NOT to Use
- Các tác vụ bắt buộc phải có kết quả tức thì để phản hồi ngay cho người dùng trong cùng một HTTP request (như kiểm tra mật khẩu đăng nhập).
- Các phép tính toán nhỏ trong RAM diễn ra dưới 5ms.

## 4. Prerequisites & Input Context
**Đầu vào cần thiết:**
- Nền tảng Message Queue (Redis / RabbitMQ / AWS SQS / Kafka).
- Định dạng payload của Job (Job Name, Parameters, Metadata).
- Chính sách xử lý lỗi: Số lần retry, Delay giữa các lần, Dead-Letter Queue.

**Điều kiện tiên quyết:**
- Redis hoặc Message Broker mục tiêu đang chạy và có kết nối ổn định.
- Worker process được cấu hình chạy độc lập với API Web server process.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**: Nắm vững cơ chế vận hành theo chuẩn Agent Skills, tuân thủ nghiêm ngặt tính xác định và ranh giới trách nhiệm.
- **Quy tắc quyết định kỹ thuật**:
- **Tính Bất Biến Lặp Lại (Job Idempotency)**: Mọi Job Worker đều CÓ THỂ bị thực thi lại nhiều lần do lỗi mạng; vì vậy logic xử lý bên trong Job bắt buộc phải Idempotent (chạy 1 lần hay 10 lần kết quả vẫn như nhau).
- **Payload Nhỏ Gọn**: Không bao giờ truyền toàn bộ object dữ liệu khổng lồ vào payload của Job; chỉ truyền ID (ví dụ: `{ orderId: '123' }`) và để Worker tự truy vấn dữ liệu mới nhất từ DB.
- **Worker Concurrency Hợp Lý**: Giới hạn số lượng job chạy đồng thời trên mỗi worker để không làm nghẽn CPU hoặc cạn kiệt Connection Pool của Database.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Server khởi động lại làm mất Job đang chạy dở**: Job bị biến mất không vết tích -> Khắc phục: Sử dụng cơ chế khóa phân tán và `stalledInterval` của BullMQ để tự động gắp lại job bị bỏ rơi khi worker crash.
- **Thư viện bên ngoài lỗi làm đầy hàng đợi**: Hàng triệu job bị kẹt và thử lại liên tục -> Khắc phục: Thiết lập Circuit Breaker ngắt hàng đợi tạm thời và chuyển sang DLQ.

## 6. Step-by-Step Execution Workflow
1. Định nghĩa Job Contract: Tên job, Schema payload dữ liệu và kết quả trả về.
2. Thiết lập Queue và gắn cấu hình retry an toàn (ví dụ: `attempts: 3`, `backoff: { type: 'exponential', delay: 1000 }`).
3. Tại Web API: Chỉ validate dữ liệu rồi đẩy Job vào Queue bằng `queue.add()` và trả về HTTP `202 Accepted` kèm `jobId` ngay lập tức.
4. Tại Worker: Lắng nghe và tiêu thụ Job, báo cáo tiến độ bằng `job.updateProgress()`.
5. Cấu hình Dead-Letter Queue (DLQ): Nếu sau số lần retry quy định mà Job vẫn thất bại, tự động chuyển Job sang DLQ để cảnh báo và điều tra thủ công mà không làm nghẽn hàng đợi chính.
6. Xử lý Graceful Shutdown cho Worker để không làm mất Job đang xử lý dở khi deploy phiên bản mới.

## 7. Concrete Examples
### Ví dụ triển khai chuẩn mực:
```typescript
// src/workers/orderEmailWorker.ts
export const orderEmailWorker = new Worker('order-emails', async (job) => {
  const { orderId } = job.data;
  job.updateProgress(10);
  const order = await db.orders.findById(orderId);
  if (!order) throw new UnrecoverableError('Đơn hàng không tồn tại');
  await emailService.sendOrderReceipt(order);
  job.updateProgress(100);
}, { connection: redisConfig, concurrency: 5 });
```

### Lệnh xác minh & thực thi:
- Kiểm tra kết nối Redis Queue: `redis-cli ping`
- Chạy worker kiểm thử cục bộ: `npm run worker:dev`
- Chạy unit/integration test xử lý job: `npm test -- tests/jobs/emailJob.spec.ts`

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước kiểm tra biên và giả định hệ thống luôn ở trạng thái lý tưởng.
- **Anti-Pattern 2**: Không ghi nhận nhật ký kiểm toán hoặc bỏ qua việc xử lý ngoại lệ lúc runtime.
- **Trap**: Bỏ qua các rào chắn an toàn hoặc cố tình chạy script không qua kiểm thử tự động.

## 9. Quality Gates & Acceptance Criteria
- QG-04: API endpoint đẩy job vào hàng đợi phản hồi dưới 100ms.
- QG-05: Kịch bản giả lập job lỗi 3 lần được tự động chuyển vào Dead-Letter Queue thành công.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động trước khi coi là hoàn thành.

## 10. Security & Safety Boundaries
- Dữ liệu nhạy cảm (mật khẩu, khóa riêng tư) tuyệt đối không được đưa vào payload của Job vì payload thường được lưu trữ dưới dạng bản rõ trong Redis/Queue logs.
- Không bao giờ thực thi mã nguồn hoặc thay đổi cấu hình trên môi trường sản xuất mà thiếu cơ chế rollback an toàn.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Có thể kích hoạt trực tiếp từ terminal hoặc extension tương thích trong VS Code / Cursor / Windsurf.

## 12. Deliverables & Output Artifacts
- File khai báo Queue và Producer (`src/queues/emailQueue.ts`).
- File triển khai Consumer Worker (`src/workers/emailWorker.ts`).
- File test tích hợp xử lý hàng đợi.

## 13. Related & Complementary Skills
- `dex-development-workflow`: Quy trình phát triển tiêu chuẩn.
- `dex-code-verification`: Xác minh chất lượng và tính đúng đắn của mã nguồn.
- `dex-master-orchestrator`: Bộ điều phối trung tâm kết nối kỹ năng này với các kỹ năng khác trong hệ thống.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư hoặc AI Agent tiếp nhận yêu cầu liên quan đến **dex-background-job-queues**.
1. Đọc kỹ đầu vào và các ràng buộc kỹ thuật tại mục 4.
2. Thực thi tuần tự 6 bước trong Workflow tại mục 6.
3. Chạy các lệnh kiểm chứng tại mục 7 và đối chiếu với Quality Gates tại mục 9.
4. Đóng gói deliverables theo danh sách tại mục 12 và báo cáo kết quả kèm bằng chứng xác thực.
