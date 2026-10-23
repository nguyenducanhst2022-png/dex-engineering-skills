---
name: dex-supabase-storage-access-policies
description: Architect, configure, and audit Supabase Storage bucket access policies and Row-Level Security on storage.objects. Manage signed URLs, file upload MIME validation, size limits, and CDN caching. Use when securing file uploads and digital asset distribution.
---

# dex-supabase-storage-access-policies

## 1. Purpose & Scope
Thiết kế, thiết lập cấu hình và kiểm toán bảo mật các chính sách truy cập thùng chứa tệp (Storage Buckets) trong Supabase Storage; áp dụng các chính sách Row-Level Security trên bảng `storage.objects`; quản lý tạo và kiểm tra thời hạn URL có chữ ký (Signed URLs); kiểm soát nghiêm ngặt định dạng MIME và kích thước tệp tải lên; và cấu hình bộ nhớ đệm CDN tối ưu.

## 2. When to Use
- Khi ứng dụng cho phép người dùng tải lên tài liệu cá nhân, ảnh đại diện, hoặc tệp hóa đơn nhạy cảm.
- Khi cần ngăn chặn người dùng này tải về hoặc xóa tệp tin của người dùng khác trong cùng một bucket lưu trữ.
- Khi cần cung cấp quyền truy cập tải tệp tạm thời trong 15 phút thông qua Signed URL mà không làm lộ tệp ra công cộng.

## 3. When NOT to Use
- Khi lưu trữ các tệp tĩnh công cộng hoàn toàn (favicon, logo thương hiệu) không yêu cầu bất kỳ bước xác thực danh tính nào.
- Khi hệ thống quản lý tệp trên máy chủ cục bộ hoặc NFS không sử dụng cơ chế Object Storage tương thích S3.

## 4. Prerequisites & Input Context
- **Thành phần hạ tầng:** Supabase Storage Bucket đã được tạo (Private hoặc Public).
- **Quyền hạn DDL:** Quyền thao tác trên schema `storage` và bảng `storage.objects`.

## 5. Core Concepts & Taxonomy
- **Private vs Public Buckets:** Bucket Public cho phép bất kỳ ai có đường link đều tải được tệp mà không cần token; Bucket Private yêu cầu phải vượt qua chính sách RLS hoặc có Signed URL hợp lệ.
- **Path-Based Storage RLS:** Quy tắc phân quyền dựa trên đường dẫn tệp (ví dụ: `(storage.foldername(name))[1] = auth.uid()::text`), bảo đảm người dùng chỉ có thể đọc/ghi trong thư mục mang tên ID của chính họ.
- **Signed Upload/Download URLs:** Đường link chứa token ký mật mã có thời hạn do server phát hành, cho phép client tương tác trực tiếp với storage mà không cần truyền tệp qua server trung gian.

## 6. Step-by-Step Execution Workflow
1. Khởi tạo bucket mới ở chế độ riêng tư (`public = false`) và giới hạn kích thước tệp tối đa (ví dụ: 10MB) cùng danh sách MIME types cho phép.
2. Viết chính sách RLS cho thao tác `INSERT`: Người dùng đã đăng nhập chỉ được tải tệp vào thư mục có tiền tố là `auth.uid()` của họ.
3. Viết chính sách RLS cho thao tác `SELECT`: Người dùng chỉ được xem các tệp trong thư mục của mình hoặc các tệp được chia sẻ rõ ràng.
4. Viết chính sách RLS cho thao tác `DELETE`: Chỉ chủ sở hữu tệp mới có quyền xóa tệp khỏi storage.
5. Xây dựng endpoint phát hành Signed URL có thời gian sống ngắn (TTL <= 900 giây) cho các tệp nhạy cảm.
6. Kiểm thử tấn công giả lập: Dùng token của User A cố tình tải xuống hoặc ghi đè tệp của User B và xác nhận bị chặn với mã lỗi 403 Forbidden.

## 7. Concrete Examples
### Chính sách RLS bảo vệ thư mục riêng của người dùng trong Supabase Storage:
```sql
-- 1. Cho phep nguoi dung upload tep vao dung thu muc mang UUID cua ho
CREATE POLICY "Users can upload to their own folder"
ON storage.objects FOR INSERT TO authenticated
WITH CHECK (
    bucket_id = 'user_documents' AND
    (storage.foldername(name))[1] = (SELECT auth.uid()::text)
);

-- 2. Cho phep nguoi dung chi doc cac tep trong thu muc cua minh
CREATE POLICY "Users can read their own files"
ON storage.objects FOR SELECT TO authenticated
USING (
    bucket_id = 'user_documents' AND
    (storage.foldername(name))[1] = (SELECT auth.uid()::text)
);

-- 3. Cho phep nguoi dung xoa tep cua chinh minh
CREATE POLICY "Users can delete their own files"
ON storage.objects FOR DELETE TO authenticated
USING (
    bucket_id = 'user_documents' AND
    (storage.foldername(name))[1] = (SELECT auth.uid()::text)
);
```

## 8. Anti-Patterns & Common Traps
- **Creating Public Buckets for Sensitive PII:** Tạo bucket ở chế độ Public cho các tệp nhạy cảm (CMND/CCCD, bảng sao kê lương, đơn thuốc), khiến ai quét được URL cũng xem được dữ liệu.
- **Missing Folder Isolation in RLS:** Viết policy cho phép `TO authenticated` upload mà không kiểm tra tiền tố thư mục, khiến User A có thể ghi đè làm hỏng tệp của User B.
- **Unrestricted MIME Types Upload:** Không giới hạn định dạng tệp, cho phép người dùng tải lên tệp `.html` hoặc `.svg` chứa mã độc XSS thực thi trực tiếp trên domain lưu trữ.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Tất cả các bucket chứa dữ liệu cá nhân (PII) hoặc tài liệu nội bộ đều ở trạng thái `public = false`.
- **QG-02**: 100% các thao tác `INSERT`, `UPDATE`, `DELETE` trên `storage.objects` đều có policy ràng buộc thư mục `auth.uid()`.
- **QG-03**: Danh sách MIME types được định nghĩa chặt chẽ (chặn tệp thực thi `.exe`, `.sh`, `.html`).

## 10. Security & Safety Boundaries
- Ngăn chặn rò rỉ dữ liệu nhạy cảm của khách hàng, chống tấn công Stored XSS qua file upload và chống ghi đè dữ liệu trái phép.

## 11. Platform Adapters
- **SDKs**: Supabase JavaScript Client (`supabase.storage`), AWS S3 SDK, TUS Resumable Upload Client.

## 12. Deliverables & Output Artifacts
- Tệp kịch bản khởi tạo bucket và chính sách RLS lưu trữ (`storage_policies.sql`).
- Module tạo Signed URL an toàn phía backend (`storage_signer.ts`).
- Bộ kiểm thử tự động kiểm tra ranh giới truy cập tệp giữa các người dùng.

## 13. Related & Complementary Skills
dex-supabase-adapter, dex-file-processing, dex-access-control-tenancy

## 14. Realistic Usage Example
```bash
# Kiem tra danh sach cac bucket va trang thai public/private
psql "$DATABASE_URL" -c "SELECT id, name, public, file_size_limit FROM storage.buckets;"

# Kiem tra cac policy RLS dang ap dung tren storage.objects
psql "$DATABASE_URL" -c "SELECT policyname, cmd, qual FROM pg_policies WHERE tablename = 'objects' AND schemaname = 'storage';"
```
