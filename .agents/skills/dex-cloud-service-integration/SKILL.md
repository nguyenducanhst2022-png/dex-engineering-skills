---
name: dex-cloud-service-integration
description: Integrate application services securely with managed cloud resources (IAM, S3/GCS, SQS/PubSub, RDS, DynamoDB/Firestore) using Workload Identity Federation, exponential backoff, and least privilege access. Use when connecting code to cloud provider services.
---

# dex-cloud-service-integration

## 1. Purpose & Scope
Thiết lập kết nối bảo mật, tin cậy giữa ứng dụng phần mềm và các dịch vụ đám mây được quản lý (Managed Cloud Services: AWS, GCP, Azure); áp dụng Workload Identity Federation (OIDC) để loại bỏ hoàn toàn long-lived credentials, cấu hình quyền hạn IAM tối thiểu (Least Privilege), thực thi cơ chế retry với Exponential Backoff & Jitter và kiểm soát circuit breaker khi tương tác với cloud API.

## 2. When to Use
- Khi ứng dụng cần đọc/ghi dữ liệu vào Object Storage (S3, GCS), gửi message tới Cloud Queue (SQS, Pub/Sub) hoặc kết nối Managed DB.
- Khi phát hiện ứng dụng đang sử dụng access key/secret key tĩnh hardcode trong biến môi trường.
- Khi ứng dụng bị lỗi `429 Too Many Requests` hoặc `ThrottlingException` từ Cloud Provider APIs.

## 3. When NOT to Use
- Khởi tạo tài nguyên đám mây từ đầu (dùng `dex-infrastructure-as-code`).
- Thiết lập mạng nội bộ Service Mesh giữa các microservice (dùng `dex-service-mesh-networking`).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Dịch vụ cloud mục tiêu (Storage, Message Broker, NoSQL, KMS).
- Identity của ứng dụng (Kubernetes Service Account, ECS Task Role, Cloud Run Service Account).
- Định mức throughput và SLA kết nối.
- **Điều kiện tiên quyết**:
- Identity Provider (OIDC / IAM Role Trust Policy) đã được liên kết với cụm ứng dụng.
- Cloud SDK (AWS SDK v3, Google Cloud Client Libraries) được tích hợp trong dự án.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- **Short-Lived Token Exchange (OIDC)**: Ứng dụng dùng JWT của môi trường chạy (K8s ServiceAccount) để đổi lấy short-lived IAM credentials (thời hạn 1 giờ), không lưu secret vĩnh viễn.
- **Full Jitter Exponential Backoff**: Khi gặp lỗi rate limit hoặc network flake, thời gian chờ retry được tính toán: `t = random(0, min(max_backoff, base * 2^attempt))` để tránh thundering herd.
- **Client Connection Pooling**: Tái sử dụng HTTP/2 persistent connections để tránh overhead của TLS handshake trên mỗi cloud request.
- **Quy tắc quyết định kỹ thuật**:
- **Tuyệt Đối Không Dùng Long-Lived IAM Keys**: Cấm tạo `AWS_ACCESS_KEY_ID` tĩnh cho ứng dụng chạy trên cloud; bắt buộc dùng IRSA (IAM Roles for Service Accounts) hoặc GCP Workload Identity.
- **Scope Quyền Hạn Tới Từng Resource ARN**: Không dùng ký tự đại diện `*` trong IAM Policy (`s3:GetObject` trên `arn:aws:s3:::my-bucket/*` thay vì `*`).
- **Timeout Tường Minh Cho Mọi Cloud Call**: Không để SDK timeout mặc định vô hạn; cấu hình timeout tối đa 3-5 giây cho mỗi cloud operation.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Rò rỉ Access Key khi commit mã nguồn**: Do lập trình viên dùng key tĩnh để test local -> Khắc phục: Áp dụng Workload Identity và pre-commit git-secrets để quét key.
- **Cloud API bị nghẽn đồng loạt khi phục hồi sau sự cố**: 1000 Pod cùng retry API một lúc không có jitter -> Khắc phục: Cấu hình chuẩn Full Jitter trong SDK retry configuration.

## 6. Step-by-Step Execution Workflow
1. Xác định danh sách quyền hạn API cloud tối thiểu cần thiết cho ứng dụng.
2. Thiết lập IAM Role Trust Policy liên kết với K8s Service Account (IRSA) hoặc Cloud Run SA.
3. Khởi tạo Cloud SDK client với DefaultCredentialProvider (tự động nhận diện IAM metadata/OIDC token).
4. Cấu hình timeout tường minh và Exponential Backoff with Jitter cho HTTP client.
5. Thực hiện đóng gói thao tác cloud thành Interface / Repository Pattern để dễ dàng mock trong unit test.
6. Giám sát metrics Cloud API call (Latency, Error Rate, Throttled Requests) qua OpenTelemetry / CloudWatch.
7. Xác minh thu hồi quyền hạn thành công khi thay đổi tác vụ.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```typescript
import { S3Client, GetObjectCommand } from "@aws-sdk/client-s3";
import { NodeHttpHandler } from "@smithy/node-http-handler";

// Khởi tạo S3 Client sử dụng WebIdentityToken (OIDC/IRSA), không cần secret key tĩnh
export const s3Client = new S3Client({
  region: process.env.AWS_REGION || "ap-southeast-1",
  maxAttempts: 4,
  requestHandler: new NodeHttpHandler({
    connectionTimeout: 2000,
    requestTimeout: 3000,
  }),
});

export async function fetchDocument(bucket: string, key: string): Promise<Uint8Array> {
  const command = new GetObjectCommand({ Bucket: bucket, Key: key });
  const response = await s3Client.send(command);
  return await response.Body?.transformToByteArray() ?? new Uint8Array();
}
```

### Lệnh xác minh & thực thi:
- Kiểm tra quyền IAM thực tế: `aws sts get-caller-identity` (phải trả về assumed role, không phải IAM user)
- Test retry và timeout: Chạy unit test giả lập HTTP 429 response để verify retry 4 lần kèm exponential backoff
- Kiểm tra CloudTrail audit log: Xác nhận API call được log với assumed role hợp lệ

## 8. Anti-Patterns & Common Traps
- **Cấp quyền `AdministratorAccess` hoặc `*` cho ứng dụng**: Gây rủi ro bảo mật nghiêm trọng nếu ứng dụng bị RCE.
- **Khởi tạo SDK Client mới trong mỗi Request**: Khiến cạn kiệt TCP sockets và phá vỡ connection pool.
- **Hardcode tên Bucket hoặc Queue trong mã nguồn**: Gây khó khăn khi triển khai đa môi trường.

## 9. Quality Gates & Acceptance Criteria
- QG-03: Không có bất kỳ static access key nào trong mã nguồn hoặc tệp cấu hình.
- QG-07: IAM Policy tuân thủ nguyên tắc Least Privilege (chỉ định rõ Action và Resource ARN).
- QG-10: SDK Client cấu hình timeout <= 5s và có cơ chế retry with jitter.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi deploy.

## 10. Security & Safety Boundaries
- Mọi giao tiếp với Cloud Services bắt buộc phải qua HTTPS / TLS 1.3.
- Bật mã hóa SSE-KMS khi lưu trữ dữ liệu trên cloud storage.
- Không bao giờ lưu trữ hardcoded secret hoặc cấp quyền quá mức (over-permissioned IAM).

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Môi trường Cloud & Container**: Hỗ trợ Docker, Kubernetes (EKS/GKE/AKS), Terraform/OpenTofu, OpenTelemetry.

## 12. Deliverables & Output Artifacts
- Module client cloud adapter chuẩn hóa, có connection pool và retry logic.
- Tệp IAM Policy JSON định nghĩa quyền hạn tối thiểu.
- Báo cáo xác thực không sử dụng long-lived credentials.

## 13. Related & Complementary Skills
- `dex-infrastructure-as-code`: Tạo IAM roles và cloud resources.
- `dex-secrets-management`: Quản lý kết nối và credentials an toàn.
- `dex-resilience-engineering`: Kiểm soát circuit breaker và timeout khi gọi dịch vụ ngoài.

## 14. Realistic Usage Example
### Tình huống thực tế:
Một service xử lý hóa đơn cần tải PDF từ AWS S3. Áp dụng `dex-cloud-service-integration`, kỹ sư gán IAM Role cho K8s Service Account qua IRSA, cấu hình S3 Client v3 với timeout 3s, áp dụng full jitter retry khi gặp lỗi mạng, viết interface IFileStorage để unit test bằng in-memory mock mà không cần gọi S3 thật, bảo đảm an ninh và độ ổn định cao.
