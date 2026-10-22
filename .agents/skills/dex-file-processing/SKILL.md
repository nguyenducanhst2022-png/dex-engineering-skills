---
name: dex-file-processing
description: Implement streaming multipart file uploads, chunked uploads, magic-byte validation, secure cloud storage (S3/GCS), and virus scanning. Use when handling file uploads, processing large datasets, or securing document storage.
---

# dex-file-processing

## 1. Purpose & Scope
Thiết kế và triển khai quy trình xử lý tệp tin (File Processing & Uploads) hiệu năng cao và an toàn tuyệt đối; xử lý tải tệp theo luồng trực tiếp (Streaming Uploads), hỗ trợ tải từng phần (Chunked / Resumable Uploads), kiểm tra định dạng tệp thực tế qua Magic Bytes, tạo Presigned URLs tải trực tiếp lên Cloud Storage (S3 / GCS) và quét mã độc ngăn chặn tấn công máy chủ.

## 2. When to Use
- Khi xây dựng tính năng upload ảnh đại diện, hóa đơn PDF, video hoặc tệp dữ liệu lớn (CSV, Excel).
- Khi máy chủ bị tràn bộ nhớ RAM (Out Of Memory) mỗi khi có người dùng upload một file 500MB.
- Khi cần bảo vệ hệ thống khỏi các tệp độc hại giả mạo đuôi file (ví dụ: file mã độc `.exe` đổi tên thành `.jpg`).

## 3. When NOT to Use
- Lưu trữ các đoạn chuỗi văn bản nhỏ thuần túy (nên lưu trực tiếp vào database).
- Xử lý các phép toán dữ liệu phân tán quy mô lớn Big Data (dùng `dex-data-pipelines`).

## 4. Prerequisites & Input Context
**Đầu vào cần thiết:**
- Loại tệp cho phép (MIME Types whitelist: `image/jpeg`, `image/png`, `application/pdf`).
- Dung lượng tệp tối đa cho phép (File size limit, ví dụ: 5MB cho ảnh, 50MB cho PDF).
- Đích lưu trữ (AWS S3, Cloudflare R2, Google Cloud Storage, Local Storage).

**Điều kiện tiên quyết:**
- Thư viện xử lý stream multipart sẵn sàng (Busboy, Multer với memory limits, hoặc AWS S3 SDK).
- Cloud Storage Bucket được cấu hình phân quyền riêng tư (Private by default), chặn truy cập công khai trực tiếp.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**: Nắm vững cơ chế vận hành theo chuẩn Agent Skills, tuân thủ nghiêm ngặt tính xác định và ranh giới trách nhiệm.
- **Quy tắc quyết định kỹ thuật**:
- **Không Lưu Trực Tiếp Trên Disk Server**: Tuyệt đối không lưu tệp tải lên vào ổ cứng cục bộ của web server trong kiến trúc container/cloud vì các container có tính chất tạm thời (Ephemeral) và không chia sẻ giữa các máy chủ.
- **Chỉ Mở Quyền Đọc Qua Presigned GET URL**: Các tệp tài liệu nội bộ, hóa đơn nhạy cảm phải được bảo vệ bằng Private S3 Bucket và chỉ cấp Presigned GET URL có thời hạn ngắn (ví dụ: 15 phút) cho người có thẩm quyền.
- **Giới Hạn Kích Thước Ngay Tại Gateway**: Cấu hình Nginx hoặc API Gateway từ chối ngay lập tức các request có `Content-Length` vượt quá dung lượng quy định.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Máy chủ sập vì nghẽn đĩa hoặc RAM**: Khi 10 người cùng upload file lớn cùng lúc -> Khắc phục: Giới hạn `limits: { fileSize: 10 * 1024 * 1024 }` và sử dụng Stream pipe trực tiếp lên S3.
- **Tải tệp chứa mã độc làm hỏng máy chủ**: Hacker tải file PHP/Shell có đuôi `.png` lên thư mục static -> Khắc phục: Tách riêng domain lưu trữ static (CDN), cấm hoàn toàn quyền thực thi script trong storage bucket.

## 6. Step-by-Step Execution Workflow
1. Ưu tiên sử dụng **S3 Presigned URL Pattern**: Máy chủ chỉ cấp URL tạm thời có chữ ký, client tự upload trực tiếp lên S3 mà không đi qua server ứng dụng, giúp server giảm tải 100% băng thông I/O.
2. Nếu bắt buộc upload qua máy chủ: Đọc tệp bằng Stream trực tiếp, không bao giờ load toàn bộ tệp vào bộ nhớ RAM (`buffer`).
3. Kiểm tra định dạng tệp thực tế: Đọc các bytes đầu tiên (Magic Bytes / File Signatures) bằng thư viện `file-type` để xác minh nội dung thực tế, cấm tin tưởng phần mở rộng tệp `.ext` do client gửi lên.
4. Đổi tên tệp ngẫu nhiên bằng UUID (`v4()`) để tránh ghi đè tệp và ngăn tấn công Path Traversal (`../../etc/passwd`).
5. Xử lý ảnh: Nén ảnh, loại bỏ siêu dữ liệu EXIF (chứa thông tin GPS vị trí người dùng) bằng Sharp.
6. Tích hợp quét mã độc (ClamAV hoặc S3 Object Lambda) trước khi cho phép người dùng khác tải về.

## 7. Concrete Examples
### Ví dụ triển khai chuẩn mực:
```typescript
// src/services/s3PresignedService.ts
export async function getPresignedUploadUrl(userId: string, fileType: string, fileSize: number) {
  if (!ALLOWED_MIME_TYPES.includes(fileType)) throw new BadRequestError('Định dạng tệp không được hỗ trợ');
  if (fileSize > 10 * 1024 * 1024) throw new BadRequestError('Dung lượng tệp vượt quá 10MB');
  
  const fileKey = `uploads/${userId}/${crypto.randomUUID()}`;
  const command = new PutObjectCommand({ Bucket: BUCKET_NAME, Key: fileKey, ContentType: fileType });
  const uploadUrl = await getSignedUrl(s3Client, command, { expiresIn: 300 });
  return { uploadUrl, fileKey };
}
```

### Lệnh xác minh & thực thi:
- Kiểm tra Magic Bytes của file: `npx file-type-cli uploaded_sample.png`
- Chạy unit test upload file hợp lệ và file giả mạo: `npm test -- tests/storage/fileUpload.spec.ts`
- Kiểm tra cấu hình S3 Bucket Encryption: `aws s3api get-bucket-encryption --bucket my-app-bucket`

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước kiểm tra biên và giả định hệ thống luôn ở trạng thái lý tưởng.
- **Anti-Pattern 2**: Không ghi nhận nhật ký kiểm toán hoặc bỏ qua việc xử lý ngoại lệ lúc runtime.
- **Trap**: Bỏ qua các rào chắn an toàn hoặc cố tình chạy script không qua kiểm thử tự động.

## 9. Quality Gates & Acceptance Criteria
- QG-03: Kiểm tra định dạng tệp qua Magic Bytes bắt buộc phải vượt qua trước khi lưu trữ.
- QG-07: Tên tệp được sinh ngẫu nhiên UUID 100%, không chứa ký tự đặc biệt hay đường dẫn gốc của client.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động trước khi coi là hoàn thành.

## 10. Security & Safety Boundaries
- Tự động xóa sạch siêu dữ liệu EXIF của ảnh để bảo vệ quyền riêng tư người dùng.
- Đặt header `Content-Disposition: attachment; filename='...'` cho các tệp không an toàn để ép trình duyệt tải về thay vì tự ý thực thi trong context của domain chính.
- Không bao giờ thực thi mã nguồn hoặc thay đổi cấu hình trên môi trường sản xuất mà thiếu cơ chế rollback an toàn.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Có thể kích hoạt trực tiếp từ terminal hoặc extension tương thích trong VS Code / Cursor / Windsurf.

## 12. Deliverables & Output Artifacts
- Service tạo Presigned URL (`src/services/s3StorageService.ts`).
- Middleware kiểm tra Magic Bytes và dung lượng (`src/middleware/fileValidator.ts`).
- File unit test giả lập upload multipart.

## 13. Related & Complementary Skills
- `dex-development-workflow`: Quy trình phát triển tiêu chuẩn.
- `dex-code-verification`: Xác minh chất lượng và tính đúng đắn của mã nguồn.
- `dex-master-orchestrator`: Bộ điều phối trung tâm kết nối kỹ năng này với các kỹ năng khác trong hệ thống.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư hoặc AI Agent tiếp nhận yêu cầu liên quan đến **dex-file-processing**.
1. Đọc kỹ đầu vào và các ràng buộc kỹ thuật tại mục 4.
2. Thực thi tuần tự 6 bước trong Workflow tại mục 6.
3. Chạy các lệnh kiểm chứng tại mục 7 và đối chiếu với Quality Gates tại mục 9.
4. Đóng gói deliverables theo danh sách tại mục 12 và báo cáo kết quả kèm bằng chứng xác thực.
