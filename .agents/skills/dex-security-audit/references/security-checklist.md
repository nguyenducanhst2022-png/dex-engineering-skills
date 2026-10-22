# DEX Security Audit Checklist & Mitigation Guide

## 1. Authentication & Session Management
- [ ] Mật khẩu được băm (hash) bằng thuật toán an toàn với salt (Argon2id, bcrypt với cost >= 12, PBKDF2). Cấm dùng MD5, SHA1, SHA256 thô.
- [ ] JWT tokens được ký bằng thuật toán mạnh (RS256 hoặc HS256 với secret đủ dài >= 256 bits).
- [ ] JWT có thời hạn hết hạn (`exp`) hợp lý, có cơ chế refresh token an toàn.
- [ ] Cookie session có các cờ bảo mật bắt buộc: `HttpOnly`, `Secure`, `SameSite=Strict` hoặc `Lax`.
- [ ] Có cơ chế giới hạn số lần đăng nhập sai (Rate Limiting / Account Lockout) chống Brute-force.

## 2. Input Validation & Data Sanitization
- [ ] Tất cả đầu vào từ người dùng (Params, Query, Body, Headers) đều được validate kiểu dữ liệu, độ dài và định dạng thông qua schema (Zod, Joi, Pydantic).
- [ ] 100% câu truy vấn cơ sở dữ liệu sử dụng Parameterized Queries hoặc ORM chuẩn, không ghép chuỗi.
- [ ] Dữ liệu người dùng render lên HTML được escape đầy đủ hoặc làm sạch bằng thư viện chuyên dụng (DOMPurify).
- [ ] Tệp tải lên (File Upload) được kiểm tra định dạng thực tế (Magic bytes/MIME), đổi tên ngẫu nhiên và lưu ở kho lưu trữ cách ly (S3 bucket không cho phép thực thi script).

## 3. Access Control (Phân quyền)
- [ ] Kiểm tra quyền truy cập (Authorization) ở cấp độ đối tượng (Object-level / IDOR prevention): Đảm bảo `user_id` sở hữu tài nguyên trước khi cho phép xem hoặc sửa.
- [ ] API endpoints nhạy cảm yêu cầu kiểm tra quyền tường minh (RBAC / ABAC middleware).
- [ ] Không để lộ thông tin nhạy cảm qua các thông báo lỗi hoặc stack trace.

## 4. Secrets & Configuration
- [ ] Không có API key, mật khẩu, private key nào tồn tại trong mã nguồn hoặc lịch sử commit.
- [ ] Mọi cấu hình nhạy cảm được nạp qua biến môi trường (`.env`), file `.env` được đưa vào `.gitignore`.
- [ ] Cấu hình CORS được thắt chặt: Không sử dụng `Access-Control-Allow-Origin: *` kèm theo `credentials: true`.
- [ ] Các header bảo mật HTTP được kích hoạt đầy đủ (dùng `Helmet` hoặc cấu hình web server):
  - `Content-Security-Policy`
  - `X-Content-Type-Options: nosniff`
  - `X-Frame-Options: DENY`
  - `Strict-Transport-Security` (HSTS)
