---
name: dex-php-framework-hardening
description: Harden modern PHP applications (Laravel, Symfony) with strict session isolation, CSRF defenses, SQL injection prevention in ORMs, and secure OPcache configurations. Use when securing PHP production environments or passing application penetration tests.
---

# dex-php-framework-hardening

## 1. Purpose & Scope
Gia cố bảo mật toàn diện cho các ứng dụng PHP hiện đại (Laravel, Symfony); thiết lập cơ chế cách ly phiên làm việc nghiêm ngặt (Strict Session Isolation), phòng chống tấn công CSRF/XSS, ngăn chặn lỗ hổng SQL Injection tiềm ẩn trong Eloquent/Doctrine ORM, và tối ưu hóa cấu hình an toàn cho PHP OPcache.

## 2. When to Use
- Khi chuẩn bị đưa ứng dụng Laravel hoặc Symfony lên môi trường sản xuất phục vụ người dùng thực tế.
- Khi thực hiện kiểm toán an ninh ứng dụng web hoặc chuẩn bị cho các đợt kiểm thử xâm nhập (Penetration Testing).
- Khi phát hiện cấu hình máy chủ PHP-FPM quá lỏng lẻo làm tăng nguy cơ leo thang đặc quyền.

## 3. When NOT to Use
- Khi phát triển ứng dụng bằng ngôn ngữ khác không liên quan tới PHP.
- Khi chỉ chạy PHP ở chế độ CLI cục bộ cho các tác vụ tính toán toán học không tiếp xúc với web.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Mã nguồn dự án Laravel/Symfony, tệp cấu hình `php.ini`, cấu hình máy chủ web (NGINX/Caddy/Apache).
- **Quyền hạn truy cập:** Quyền sửa đổi cấu hình `php.ini` và mã nguồn middleware ứng dụng.

## 5. Core Concepts & Taxonomy
- **Session Fixation Defense:** Bắt buộc tái sinh Session ID (`session_regenerate_id(true)`) ngay sau khi người dùng đăng nhập thành công để chống chiếm đoạt phiên.
- **ORM Raw Query Vulnerabilities:** Tránh việc sử dụng `DB::raw()` hoặc các phương thức tương tự với dữ liệu chưa được kiểm duyệt từ người dùng trong Eloquent/Doctrine.
- **OPcache Hardening:** Tắt tính năng tự động kiểm tra timestamp (`opcache.validate_timestamps=0`) trên production để tăng tốc độ và bảo vệ mã nguồn không bị ghi đè động.

## 6. Step-by-Step Execution Workflow
1. Khóa các hàm nguy hiểm trong `php.ini`: `disable_functions = exec,passthru,shell_exec,system,proc_open,popen,curl_exec`.
2. Cấu hình bảo mật Cookie và Session: bắt buộc `session.cookie_httponly = 1`, `session.cookie_secure = 1`, `session.cookie_samesite = 'Strict'`.
3. Rà soát toàn bộ mã nguồn: tìm kiếm và loại bỏ các vị trí sử dụng `DB::raw()`, `whereRaw()` có nối chuỗi trực tiếp dữ liệu từ request người dùng.
4. Kích hoạt Middleware bảo vệ CSRF trên toàn bộ các route có phương thức ghi dữ liệu (POST, PUT, DELETE, PATCH).
5. Thiết lập mã hóa đầu ra (Output Encoding) bằng công cụ Blade hoặc Twig để phòng chống triệt để lỗ hổng Cross-Site Scripting (XSS).
6. Chạy công cụ kiểm toán an ninh PHPStan và Psalm ở mức độ kiểm tra cao nhất để phát hiện lỗi tiềm ẩn.

## 7. Concrete Examples
### Ví dụ cấu hình bảo mật `php.ini` và truy vấn Eloquent an toàn trong Laravel:
```ini
; Cấu hình php.ini chuẩn hóa cho môi trường Production an toàn
expose_php = Off
display_errors = Off
log_errors = On
allow_url_fopen = Off
allow_url_include = Off
session.cookie_httponly = 1
session.cookie_secure = 1
session.cookie_samesite = "Strict"
session.use_strict_mode = 1
opcache.enable = 1
opcache.validate_timestamps = 0
```

```php
// TRÁNH: Lỗ hổng SQL Injection khi dùng DB::raw() nối chuỗi
// $users = DB::table('users')->whereRaw("email = '" . $request->input('email') . "'")->get();

// ĐÚNG: Luôn sử dụng Parameter Binding hoặc Eloquent Builder an toàn
$users = DB::table('users')
    ->where('email', '=', $request->validated('email'))
    ->first();
```

## 8. Anti-Patterns & Common Traps
- **Unsafe Raw SQL Fragments:** Nối chuỗi biến người dùng vào các mệnh đề `orderByRaw()` hoặc `groupByRaw()` vì nghĩ rằng ORM sẽ tự động bảo vệ.
- **Leaving Debug Mode On:** Để cấu hình `APP_DEBUG=true` trên production làm lộ toàn bộ biến môi trường và mật khẩu database khi có exception xảy ra.
- **Shared Storage Permissions:** Cấp quyền ghi `chmod 777` cho toàn bộ thư mục `storage/` và `bootstrap/cache/` tạo cơ hội cho tin tặc tải lên và thực thi mã độc Web Shell.

## 9. Quality Gates & Acceptance Criteria
- **QG-02**: Tệp cấu hình `.env` trên môi trường sản xuất có `APP_DEBUG=false`.
- **QG-06**: Quét kiểm tra mã nguồn bằng PHPStan ở Level 8 trả về 0 cảnh báo vi phạm bảo mật.
- **QG-14**: 100% các cookies do ứng dụng phát hành có đầy đủ cờ `HttpOnly`, `Secure` và `SameSite`.

## 10. Security & Safety Boundaries
- Bật bảo vệ Content Security Policy (CSP) header để ngăn chặn XSS và data exfiltration.
- Thường xuyên chạy `composer audit` để phát hiện và cập nhật các gói phụ thuộc PHP có lỗ hổng bảo mật đã công bố.

## 11. Platform Adapters
- **Frameworks**: Laravel 11.x, Symfony 7.x.
- **Security Tools**: PHPStan, Psalm, Enlightn, Composer Audit.

## 12. Deliverables & Output Artifacts
- Tệp cấu hình `php.ini` gia cố bảo mật cho production.
- Bộ quy tắc kiểm tra bảo mật tĩnh cho PHPStan/Enlightn.
- Báo cáo kiểm toán 0 lỗ hổng bảo mật ORM và Session.

## 13. Related & Complementary Skills
dex-sast-finding-triage, dex-web-security-headers, dex-dependency-vulnerability-intelligence

## 14. Realistic Usage Example
```powershell
# Chạy kiểm toán bảo mật mã nguồn PHP và kiểm tra lỗ hổng dependencies
./vendor/bin/phpstan analyse --level=8
composer audit
```
