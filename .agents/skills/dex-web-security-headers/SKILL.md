---
name: dex-web-security-headers
description: Design, configure, and audit HTTP security headers including strict Content Security Policy (CSP), HSTS, Permissions-Policy, and secure cookie attributes. Use when hardening web applications against XSS, clickjacking, and MITM.
---

# dex-web-security-headers

## 1. Purpose & Scope
Thiết kế, cấu hình và kiểm toán toàn diện các tiêu đề bảo mật HTTP (HTTP Security Headers); xây dựng chính sách bảo mật nội dung nghiêm ngặt (Strict Content Security Policy - CSP nonce-based), HSTS với preloading, Permissions-Policy, và các thuộc tính bảo vệ cookie (`Secure`, `HttpOnly`, `SameSite=Strict`), bảo vệ ứng dụng web chống lại các cuộc tấn công XSS, Clickjacking, MIME-sniffing và Man-in-the-Middle.

## 2. When to Use
- Kết quả quét bảo mật báo cáo thiếu các HTTP Security Headers cơ bản.
- Cần ngăn chặn việc thực thi các đoạn mã độc XSS từ các plugin hoặc tiện ích bên thứ ba.
- Chuẩn bị đánh giá tuân thủ an ninh thông tin theo thang điểm Mozilla Observatory hoặc SecurityHeaders.com (đạt điểm A+).

## 3. When NOT to Use
- Không áp dụng chính sách CSP quá ngặt nghèo ở chế độ `Content-Security-Policy` (chặn đứng) ngay lập tức mà chưa qua giai đoạn `Content-Security-Policy-Report-Only` để thu thập log vi phạm.
- Không dùng từ khóa `unsafe-inline` hoặc `unsafe-eval` trong CSP trừ khi thực sự bất khả kháng.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Danh sách các domain bên thứ ba mà ứng dụng cần kết nối (CDNs, Google Analytics, Stripe, Fonts).
- Cấu hình máy chủ web (Nginx, Cloudflare, Next.js, Express/Helmet).
- Điểm báo cáo an ninh hiện tại từ SecurityHeaders.com.
- **Điều kiện tiên quyết**:
- Ứng dụng đã được phục vụ hoàn toàn qua giao thức mã hóa HTTPS với chứng chỉ SSL hợp lệ.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Strict Nonce-based CSP: Thay vì whitelist theo domain (dễ bị bypass), mỗi lần render trang server sinh ra một chuỗi ngẫu nhiên duy nhất (nonce). Chỉ các thẻ `<script nonce="...">` có mã khớp mới được trình duyệt thực thi, chặn đứng 100% mã độc XSS tiêm nhiễm.
- HSTS Preload: Yêu cầu trình duyệt luôn luôn kết nối qua HTTPS ngay cả trước khi gửi request đầu tiên, bảo vệ người dùng khỏi tấn công SSL Stripping.
- Cookie Security Attributes: Ba thuộc tính bắt buộc cho session cookies:
  + `Secure`: Chỉ truyền qua HTTPS.
  + `HttpOnly`: Ngăn chặn JavaScript truy cập qua `document.cookie` (chống đánh cắp cookie qua XSS).
  + `SameSite=Strict/Lax`: Chống tấn công CSRF.
- **Quy tắc quyết định kỹ thuật**:
- Mọi ứng dụng web production bắt buộc phải đạt điểm A+ trên Mozilla Observatory.
- Bắt buộc khai báo header `Permissions-Policy` để vô hiệu hóa quyền truy cập Camera, Microphone và Geolocation nếu ứng dụng không dùng đến.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Cấu hình CSP quá vội vàng làm chặn mất script nạp form thanh toán của Stripe, khiến khách hàng không thể mua hàng trên production.

## 6. Step-by-Step Execution Workflow
1. Quét ứng dụng hiện tại bằng công cụ phân tích headers.
2. Cấu hình tiêu đề `Content-Security-Policy-Report-Only` và gửi báo cáo vi phạm về Sentry/Report-URI.
3. Rà soát log trong 7 ngày để thêm nonce cho các script hợp lệ và loại bỏ inline scripts.
4. Chuyển tiêu đề sang chế độ cưỡng chế chính thức `Content-Security-Policy`.
5. Bổ sung đầy đủ HSTS, X-Content-Type-Options, X-Frame-Options và Permissions-Policy.
6. Kiểm tra lại bằng bài quét tự động để xác nhận đạt điểm tối đa A+.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```nginx
# Cấu hình Nginx chuẩn bảo mật HTTP Security Headers đạt điểm A+
add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-Frame-Options "DENY" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Permissions-Policy "camera=(), microphone=(), geolocation=(), payment=(self)" always;
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'nonce-$request_id'; style-src 'self' 'unsafe-inline'; img-src 'self' data: https:; font-src 'self' data:; connect-src 'self' https://api.example.com; frame-ancestors 'none'; base-uri 'self'; form-action 'self';" always;
```

### Lệnh xác minh & thực thi:
```bash
# Kiểm tra headers an ninh trực tiếp từ dòng lệnh bằng curl
curl -I https://app.example.com
```

## 8. Anti-Patterns & Common Traps
- Cho phép `frame-ancestors *` khiến website dễ dàng bị nhúng vào iframe của kẻ tấn công để lừa bấm (Clickjacking).
- Đặt cookie phiên làm việc mà thiếu cờ `HttpOnly` và `Secure`.

## 9. Quality Gates & Acceptance Criteria
- Đạt điểm A hoặc A+ trên công cụ đánh giá Mozilla Observatory và SecurityHeaders.com.
- 0 lỗi vi phạm CSP được báo cáo từ người dùng chân chính sau khi kích hoạt.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Giá trị nonce trong CSP phải là chuỗi ngẫu nhiên tiền định mật mã (Cryptographically secure random) và sinh mới cho từng request.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ thống An ninh & SkillOps**: Tương thích GitHub Actions, SARIF, CycloneDX/SPDX, Semgrep, OWASP ZAP.

## 12. Deliverables & Output Artifacts
- File cấu hình Nginx / Helmet / Cloudflare Headers hoàn chỉnh.
- Báo cáo xác thực đạt điểm A+ từ công cụ kiểm tra độc lập.

## 13. Related & Complementary Skills
dex-browser-extension-hardening, dex-sast-finding-triage, dex-edge-runtime-engineering

## 14. Realistic Usage Example
### Tình huống thực tế:
Một sàn giao dịch tiền điện tử từng bị kẻ tấn công khai thác lỗ hổng trong một thư viện quảng cáo bên thứ ba để tiêm script ăn cắp token phiên. Sau khi triển khai Strict Nonce-based CSP kết hợp cookie `SameSite=Strict`, trình duyệt đã từ chối thực thi toàn bộ các script lạ được tiêm vào, bảo vệ an toàn tuyệt đối cho tài khoản của hàng triệu nhà đầu tư.
