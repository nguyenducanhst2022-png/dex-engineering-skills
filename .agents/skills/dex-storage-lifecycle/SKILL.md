---
name: dex-storage-lifecycle
description: Architect object storage tiering, lifecycle transition policies, cold-storage archiving (Glacier/Archive), and multipart retention on AWS S3 / Cloudflare R2. Use when optimizing cloud storage costs, archiving historical data, or automating bucket lifecycles.
---

# dex-storage-lifecycle

## 1. Purpose & Scope
Thiết kế và triển khai chính sách vòng đời lưu trữ dữ liệu (Object Storage Lifecycle Management) trên các nền tảng đám mây (AWS S3, Google Cloud Storage, Cloudflare R2); tự động chuyển dịch các tầng lưu trữ (Storage Tiering: Hot -> Warm -> Cold / Glacier -> Deep Archive), thiết lập thời gian tự động xóa tệp tạm, hủy các phần tải dở (Incomplete Multipart Uploads) và cắt giảm tối đa chi phí hạ tầng lưu trữ.

## 2. When to Use
- Khi chi phí lưu trữ đám mây (AWS S3 bill) tăng vọt bất thường theo từng tháng.
- Khi hệ thống tích lũy hàng terabytes log, hóa đơn, video hoặc bản sao lưu cũ không còn ai truy cập thường xuyên.
- Khi cần tuân thủ quy định lưu trữ dữ liệu bắt buộc trong 7 năm nhưng phải tối ưu chi phí ở mức thấp nhất.

## 3. When NOT to Use
- Quản lý bộ nhớ RAM tạm thời của Redis (dùng `dex-caching-strategies`).
- Thiết lập chính sách xóa dòng dữ liệu trong cơ sở dữ liệu quan hệ (dùng `dex-data-retention`).

## 4. Prerequisites & Input Context
**Đầu vào cần thiết:**
- Mô hình truy cập dữ liệu (Data Access Patterns: thường xuyên trong 30 ngày đầu, hiếm khi đọc sau 90 ngày).
- Danh sách các S3 Buckets hoặc Prefixes cần áp dụng quy tắc.
- Yêu cầu thời gian khôi phục khi cần (Retrieval Time SLA: vài phút hay vài giờ).

**Điều kiện tiên quyết:**
- Có quyền quản trị hạ tầng đám mây (AWS IAM permissions: `s3:PutLifecycleConfiguration`).
- Đã kích hoạt tính năng phân tích bộ nhớ (S3 Storage Lens hoặc CloudWatch metrics).

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**: Nắm vững cơ chế vận hành theo chuẩn Agent Skills, tuân thủ nghiêm ngặt tính xác định và ranh giới trách nhiệm.
- **Quy tắc quyết định kỹ thuật**:
- **Tránh Chuyển Tầng Tệp Quá Nhỏ**: Không áp dụng chuyển sang Glacier cho các tệp có dung lượng < 128KB vì phí chuyển đổi và metadata sẽ đắt hơn tiền tiết kiệm được.
- **Luôn Có Quy Tắc Hủy Multipart Dở Dang**: 100% các bucket có tính năng upload lớn bắt buộc phải có quy tắc `AbortIncompleteMultipartUpload` sau 7 ngày.
- **Cân Nhắc Phí Rút Dữ Liệu (Retrieval Fees)**: Không chuyển dữ liệu sang Glacier nếu ứng dụng vẫn có nhu cầu đọc ngẫu nhiên hàng ngày vì phí lấy dữ liệu từ Glacier rất đắt.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Hóa đơn AWS tăng vọt vì chuyển hàng triệu tệp nhỏ sang Glacier**: Do phí API request `PutObject` chuyển tầng nhiều hơn tiền lưu trữ -> Khắc phục: Gom các tệp nhỏ thành file nén zip/tar lớn trước khi đưa vào kho lưu trữ lạnh.
- **Không khôi phục được tệp khi khách hàng yêu cầu gấp**: Do chọn Deep Archive cần tới 12 tiếng để giải nén -> Khắc phục: Phân loại dữ liệu quan trọng dùng Glacier Instant Retrieval (lấy lại trong vài miligiây).

## 6. Step-by-Step Execution Workflow
1. Phân tích mô hình truy cập dữ liệu qua S3 Storage Lens: Xác định tỷ lệ dữ liệu không được đọc trong 30, 90, 365 ngày.
2. Thiết kế chính sách chuyển tầng lưu trữ tự động (Tiering Rules):
   - *0 - 30 ngày*: S3 Standard (Hot) - Cho phép đọc ghi tức thì tốc độ cao nhất.
   - *Sau 30 ngày*: Tự động chuyển sang S3 Infrequent Access (Standard-IA) - Giảm 50% chi phí lưu trữ.
   - *Sau 90 ngày*: Tự động chuyển sang S3 Glacier Flexible Retrieval - Giảm 80% chi phí.
   - *Sau 365 ngày*: Chuyển sang S3 Glacier Deep Archive ($0.00099/GB/tháng) cho dữ liệu tuân thủ pháp lý.
3. Cấu hình quy tắc dọn dẹp các mảnh tải dở: Tự động hủy và xóa các tệp `AbortIncompleteMultipartUpload` sau 7 ngày để tránh bị tính tiền rác.
4. Cấu hình xóa các phiên bản cũ không hiện hành (Noncurrent Version Expiration) nếu bật S3 Versioning.
5. Đóng gói chính sách bằng Infrastructure as Code (Terraform / CloudFormation / AWS CDK).
6. Kiểm tra cấu hình và theo dõi chi phí giảm thiểu.

## 7. Concrete Examples
### Ví dụ triển khai chuẩn mực:
```hcl
# terraform/s3_lifecycle.tf
resource "aws_s3_bucket_lifecycle_configuration" "data_lifecycle" {
  bucket = aws_s3_bucket.storage.id
  rule {
    id     = "archive-and-cleanup"
    status = "Enabled"
    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }
    transition {
      days          = 90
      storage_class = "GLACIER"
    }
    abort_incomplete_multipart_upload {
      days_after_initiation = 7
    }
  }
}
```

### Lệnh xác minh & thực thi:
- Kiểm tra chính sách lifecycle của bucket: `aws s3api get-bucket-lifecycle-configuration --bucket my-company-data`
- Kiểm tra dung lượng incomplete multipart uploads: `aws s3api list-multipart-uploads --bucket my-company-data`
- Ước tính chi phí tiết kiệm bằng AWS Cost Explorer CLI.

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước kiểm tra biên và giả định hệ thống luôn ở trạng thái lý tưởng.
- **Anti-Pattern 2**: Không ghi nhận nhật ký kiểm toán hoặc bỏ qua việc xử lý ngoại lệ lúc runtime.
- **Trap**: Bỏ qua các rào chắn an toàn hoặc cố tình chạy script không qua kiểm thử tự động.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Chính sách Lifecycle được định nghĩa tường minh bằng Terraform/IaC, không cấu hình thủ công bằng tay trên console.
- QG-07: Tất cả các bucket lưu trữ lạnh đều có cấu hình mã hóa mặc định (SSE-S3 hoặc SSE-KMS).
- Mọi thay đổi phải vượt qua bài kiểm thử tự động trước khi coi là hoàn thành.

## 10. Security & Safety Boundaries
- Áp dụng S3 Object Lock (WORM - Write Once, Read Many) cho các bản sao lưu tài chính quan trọng để chống mã độc tống tiền (Ransomware) xóa hoặc mã hóa dữ liệu sao lưu.
- Không bao giờ thực thi mã nguồn hoặc thay đổi cấu hình trên môi trường sản xuất mà thiếu cơ chế rollback an toàn.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Có thể kích hoạt trực tiếp từ terminal hoặc extension tương thích trong VS Code / Cursor / Windsurf.

## 12. Deliverables & Output Artifacts
- File mã nguồn Terraform cấu hình vòng đời S3 (`terraform/s3_lifecycle.tf`).
- Bản phân tích chi phí ước tính trước và sau khi áp dụng chính sách.

## 13. Related & Complementary Skills
- `dex-development-workflow`: Quy trình phát triển tiêu chuẩn.
- `dex-code-verification`: Xác minh chất lượng và tính đúng đắn của mã nguồn.
- `dex-master-orchestrator`: Bộ điều phối trung tâm kết nối kỹ năng này với các kỹ năng khác trong hệ thống.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư hoặc AI Agent tiếp nhận yêu cầu liên quan đến **dex-storage-lifecycle**.
1. Đọc kỹ đầu vào và các ràng buộc kỹ thuật tại mục 4.
2. Thực thi tuần tự 6 bước trong Workflow tại mục 6.
3. Chạy các lệnh kiểm chứng tại mục 7 và đối chiếu với Quality Gates tại mục 9.
4. Đóng gói deliverables theo danh sách tại mục 12 và báo cáo kết quả kèm bằng chứng xác thực.
