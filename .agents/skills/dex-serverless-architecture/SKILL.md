---
name: dex-serverless-architecture
description: Architect, optimize, and secure event-driven serverless architectures (AWS Lambda, Google Cloud Run) mitigating cold starts, managing concurrency limits, and ensuring idempotency. Use when building autoscaling, pay-per-use backend systems.
---

# dex-serverless-architecture

## 1. Purpose & Scope
Thiết kế, xây dựng và tối ưu hóa kiến trúc không máy chủ (Serverless Architecture: AWS Lambda, GCP Cloud Run, Azure Functions); quản lý và triệt tiêu độ trễ khởi động nguội (Cold Start), kiểm soát giới hạn đồng thời (Concurrency Limits), bảo đảm tính bình thản (Idempotency) của các sự kiện và tối ưu hóa chi phí vận hành.

## 2. When to Use
- Xây dựng hệ thống backend xử lý sự kiện không đồng bộ (Event-driven) có lưu lượng biến thiên mạnh.
- Cần tối ưu chi phí hạ tầng máy chủ cho các ứng dụng có khoảng thời gian rảnh rỗi kéo dài.
- Chuyển đổi các tác vụ xử lý ảnh, video, dữ liệu hàng loạt (batch) sang kiến trúc phi tập trung.

## 3. When NOT to Use
- Không dùng Serverless cho các tác vụ tính toán kéo dài liên tục nhiều giờ (vượt quá giới hạn timeout 15 phút của Lambda).
- Không dùng khi cần duy trì kết nối WebSocket thường trực cho hàng triệu người dùng mà không có managed gateway.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Nguồn phát sự kiện (Event sources: S3, SQS, Kinesis, EventBridge, API Gateway).
- Ngân sách tài nguyên (Memory: 128MB - 10GB, Timeout limit).
- Yêu cầu về độ trễ phản hồi (P95 latency requirement).
- **Điều kiện tiên quyết**:
- Có tài khoản AWS/GCP với quyền tạo IAM Role và triển khai Lambda/Cloud Run.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Cold Start: Thời gian cloud provider khởi tạo container mới và nạp runtime. Giảm thiểu bằng cách tối ưu kích thước bundle, dùng ngôn ngữ biên dịch sẵn (Rust, Go) hoặc Provisioned Concurrency.
- Database Connection Exhaustion: Hàng ngàn Lambda instances sinh ra đồng thời có thể đánh sập PostgreSQL/MySQL truyền thống (phải dùng RDS Proxy hoặc Serverless DB như DynamoDB/Aurora Serverless).
- Event Deduplication: Sự kiện từ SQS/Kafka có thể bị gửi lặp lại (at-least-once delivery), bắt buộc xử lý idempotent.
- **Quy tắc quyết định kỹ thuật**:
- Nếu tác vụ yêu cầu độ trễ P99 < 50ms: sử dụng Provisioned Concurrency hoặc chuyển sang Go/Rust thay vì Java/Node.
- Khởi tạo SDK clients (AWS SDK, DB pool) bên ngoài hàm handler để tái sử dụng giữa các lần thực thi ấm (Warm execution).
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Cấu hình timeout của Lambda ngắn hơn timeout của downstream API khiến Lambda bị ngắt giữa chừng trong khi downstream vẫn đang thực thi.

## 6. Step-by-Step Execution Workflow
1. Thiết kế sơ đồ luồng sự kiện phân tán từ nguồn tới đích.
2. Cấu hình cấp phát RAM và CPU tương ứng (AWS Lambda tự động scale CPU theo RAM).
3. Tích hợp RDS Proxy để quản lý connection pooling.
4. Triển khai cơ chế lưu vết khóa Idempotency Key trên DynamoDB với TTL tự động.
5. Đóng gói mã nguồn tối giản (Tree-shaking, loại bỏ devDependencies) và triển khai qua Serverless Framework/SAM.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```typescript
import { SQSHandler } from 'aws-lambda';
import { DynamoDBClient } from '@aws-sdk/client-dynamodb';

// Khởi tạo client bên ngoài handler để tái sử dụng context
const ddb = new DynamoDBClient({});

export const handler: SQSHandler = async (event) => {
  for (const record of event.Records) {
    const messageId = record.messageId;
    // Kiểm tra idempotency key trước khi xử lý
    if (await isAlreadyProcessed(messageId)) continue;
    await processOrder(JSON.parse(record.body));
    await markProcessed(messageId);
  }
};
```

### Lệnh xác minh & thực thi:
```bash
# Kiểm tra độ trễ cold start bằng plugin serverless
sls invoke -f processOrder --log
```

## 8. Anti-Patterns & Common Traps
- Mở kết nối Database mới bên trong thân hàm handler cho mỗi request.
- Lưu trữ trạng thái tạm (in-memory state) và kỳ vọng nó tồn tại ở lần gọi tiếp theo.

## 9. Quality Gates & Acceptance Criteria
- Giảm dung lượng gói deploy zip < 15MB để giữ Cold Start dưới 250ms.
- 100% các event handler xử lý an toàn trước các tin nhắn trùng lặp.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Nguyên tắc đặc quyền tối thiểu (Least Privilege IAM): mỗi hàm chỉ có quyền đọc/ghi đúng resource cần thiết.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ thống hỗ trợ**: Cloud Runtimes (AWS Lambda, Cloudflare Workers, Kubernetes), Linux, Windows 11.

## 12. Deliverables & Output Artifacts
- File cấu hình kiến trúc Serverless (`serverless.yml` hoặc `template.yaml`).
- Mã nguồn handler tối ưu hóa kèm cơ chế chống trùng lặp sự kiện.

## 13. Related & Complementary Skills
dex-edge-runtime-engineering, dex-cloud-iam-policy-review, dex-distributed-consistency

## 14. Realistic Usage Example
### Tình huống thực tế:
Một công ty bảo hiểm sử dụng Lambda để bóc tách hồ sơ PDF gửi lên S3. Khi có bão lũ, lượng hồ sơ tăng đột biến gấp 50 lần. Nhờ kiến trúc Serverless kết hợp SQS Dead-Letter Queue và RDS Proxy, hệ thống tự động scale lên 1,500 worker đồng thời và xử lý xong 100,000 hồ sơ trong 20 phút mà không tốn một đồng chi phí máy chủ nhàn rỗi trước đó.
