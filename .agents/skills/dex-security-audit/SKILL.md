---
name: dex-security-audit
description: Static and dynamic software security auditing, vulnerability classification, OWASP Top 10 mitigation, secret scanning, and patch verification. Identifies injection risks, authentication flaws, and sensitive data leakage. Use before releases, during code audits, when handling credentials, or when validating patches.
---

# DEX Security Audit

## 1. Purpose & Scope
Rà soát toàn diện mã nguồn nhằm phát hiện, phân loại và khắc phục các lỗ hổng bảo mật tiềm ẩn trước khi phần mềm được triển khai lên môi trường thử nghiệm hoặc vận hành thực tế.

Quy trình bảo mật chuẩn:
`Quét bảo mật → Phát hiện lỗ hổng → Đánh giá rủi ro → Sửa lỗi → Kiểm thử bảo mật → Kiểm tra hồi quy → Ổn định → Lưu Git`

Nguyên tắc cốt lõi: **Bảo mật phải được kiểm tra chủ động trước khi phát hành, không phải chờ đến khi xảy ra sự cố mới vá.**
Ghi nhớ sống còn: **Code chạy đúng ≠ Code an toàn. Bảo mật tốt = Phòng ngừa + Phát hiện + Khắc phục + Kiểm chứng.**

## 2. When to Use
- Trước khi đóng gói phiên bản phát hành (Pre-release gate).
- Khi xây dựng các chức năng liên quan đến Xác thực (Authentication), Phân quyền (Authorization), Mã hóa, Quản lý Token hoặc Xử lý Thanh toán.
- Khi tiếp nhận mã nguồn bên ngoài hoặc tích hợp các thư viện bên thứ ba.
- Định kỳ kiểm toán an ninh dự án.

## 3. When NOT to Use
- Kiểm thử thâm nhập hạ tầng mạng hoặc tấn công từ chối dịch vụ vật lý (DDoS) đòi hỏi quyền hạn an ninh chuyên biệt.
- Tinh chỉnh giao diện hiển thị thuần túy không nhận bất kỳ input nào từ người dùng.

## 4. Prerequisites & Input Context
- Toàn bộ mã nguồn dự án, đặc biệt là các router, controller, middleware xác thực và truy vấn database.
- Danh sách dependencies (`package.json`, `requirements.txt`, `go.mod`...).
- Bảng tiêu chuẩn an ninh chi tiết tại [security-checklist.md](references/security-checklist.md).

## 5. Core Concepts & Taxonomy
- **Nguyên tắc cốt lõi**: Tuân thủ triệt để nguyên lý vận hành xác định và ranh giới trách nhiệm của chuẩn Agent Skills.
- **Tính nhất quán hệ thống**: Mọi thao tác phải có thể kiểm chứng độc lập với kết quả đo lường rõ ràng.
- **Ngăn ngừa hồi quy**: Bất kỳ sửa đổi nào cũng phải bảo vệ tính tương thích ngược và chất lượng đã được nghiệm thu.

## 6. Step-by-Step Execution Workflow
### Bước 1: Quét Tự Động & Rà Soát Bí Mật (Secret & Dependency Scanning)
- Quét tìm API keys, access tokens, mật khẩu hoặc private keys bị hardcode trong mã nguồn:
  - Dùng công cụ: `git-secrets`, `trufflehog`, hoặc regex quét chuỗi nhạy cảm.
- Kiểm tra lỗ hổng đã biết trong dependencies:
  - `npm audit`, `pip-audit`, hoặc `safety check`.

### Bước 2: Kiểm Toán Lỗ Hổng Theo OWASP Top 10 (Code Audit)
- Rà soát các nguy cơ kinh điển:
  - **Injection**: SQL Injection, Command Injection, NoSQL Injection (Kiểm tra xem có ghép chuỗi query trực tiếp không).
  - **Broken Authentication**: Session fixation, JWT không verify signature, brute force không rate limit.
  - **Sensitive Data Exposure**: Ghi mật khẩu/thẻ tín dụng vào log, truyền dữ liệu không qua HTTPS.
  - **Broken Access Control**: IDOR (truy cập tài nguyên của user khác bằng cách đổi ID trên URL).
  - **Security Misconfiguration**: Bật debug mode trên production, để lộ stack trace chi tiết cho người dùng cuối.
  - **Cross-Site Scripting (XSS)** & **CSRF**: Render HTML thô không qua sanitize, thiếu cookie `SameSite`/`HttpOnly`.

### Bước 3: Phân Loại & Đánh Giá Mức Độ Rủi Ro (Triage & Severity Rating)
- Phân loại rủi ro theo thang đo chuẩn:
  - **CRITICAL**: Có thể bị khai thác từ xa để chiếm quyền kiểm soát hệ thống hoặc rò rỉ toàn bộ cơ sở dữ liệu (Yêu cầu dừng ngay lập tức mọi hoạt động để vá).
  - **HIGH**: Có thể bypass xác thực hoặc đánh cắp dữ liệu người dùng.
  - **MEDIUM**: Thiếu rate limit, lộ thông tin phiên bản máy chủ.
  - **LOW**: Cảnh báo cấu hình lỏng lẻo không gây nguy hại trực tiếp.

### Bước 4: Sửa Chữa & Vá Lỗ Hổng Tận Gốc (Remediation)
- Áp dụng nguyên tắc phòng vệ theo chiều sâu (Defense-in-depth):
  - Dùng Parameterized Queries / Prepared Statements 100% để triệt tiêu SQL Injection.
  - Sử dụng thư viện sanitize (như DOMPurify) hoặc template engine an toàn chống XSS.
  - Bổ sung middleware kiểm tra quyền hạn (Role-Based Access Control) chặt chẽ.
  - Đưa toàn bộ cấu hình nhạy cảm sang biến môi trường (`.env`).

### Bước 5: Kiểm Thử Xác Minh Bản Vá (Security Verification)
- Viết test case tấn công giả lập (Penetration Test Case) với payload độc hại để chứng minh hệ thống đã từ chối an toàn.

### Bước 6: Kiểm Tra Hồi Quy & Ổn Định (Regression Check & Commit)
- Chạy lại toàn bộ test suite để đảm bảo bản vá bảo mật không làm hỏng tính năng bình thường của người dùng hợp lệ.
- Tạo commit an toàn: `fix(security): sanitize user input in search query to prevent XSS`.

## 7. Concrete Examples
```bash
# Lệnh thực thi & kiểm chứng tiêu chuẩn
dex verify --skill dex-security-audit
```

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước xác minh tự động và dựa vào giả định chủ quan.
- **Anti-Pattern 2**: Thay đổi diện rộng vượt ngoài phạm vi (Scope Creep) làm mất kiểm soát rủi ro.
- **Trap**: Thực hiện thao tác phá hủy hoặc thay đổi trạng thái sản xuất khi chưa qua cổng kiểm duyệt an toàn.

## 9. Quality Gates & Acceptance Criteria
- **QG-07 (Security Audit Clean)**: 
  - 0 secret/token bị commit trong mã nguồn.
  - 0 lỗ hổng CRITICAL hoặc HIGH trong audit report.
  - Các dependency không chứa lỗ hổng bảo mật nghiêm trọng đã công bố.
- **QG-05 (Security Tests PASS)**: Kịch bản thử nghiệm giả lập tấn công bị hệ thống chặn thành công.

## 10. Security & Safety Boundaries
- **Cấm Tuyệt Đối Hardcode Credentials**: Cấm ghi bất kỳ thông tin đăng nhập, private key hoặc token thật vào code, dù chỉ là tạm thời để test.
- **Không Ghi Dữ Liệu Nhạy Cảm Vào Log**: Cấm `console.log(password)` hay ghi thông tin PII (Personally Identifiable Information) của người dùng vào log server.
- **Cấm Dùng `eval()` và Hàm Thực Thi Chuỗi**: Không bao giờ sử dụng `eval()`, `Function()`, `exec()` với dữ liệu đầu vào chưa được làm sạch.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Kích hoạt thông qua terminal hoặc tiện ích mở rộng IDE tương thích (VS Code, Cursor, Windsurf).

## 12. Deliverables & Output Artifacts
1. Báo cáo kiểm toán bảo mật (Security Audit Report) liệt kê các phát hiện, mức độ nghiêm trọng và giải pháp.
2. Bản vá mã nguồn an toàn.
3. Kịch bản test bảo mật chứng minh bản vá hiệu quả.

## 13. Related & Complementary Skills
- `dex-master-orchestrator`: Điều phối trung tâm.

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Kỹ sư hoặc AI Agent kích hoạt **dex-security-audit** trong dự án.
1. Tiếp nhận ngữ cảnh đầu vào và kiểm tra điều kiện tiên quyết tại Mục 4.
2. Vận hành tuần tự các bước theo Quy trình tại Mục 6.
3. Kiểm chứng đầu ra đối chiếu với Tiêu chuẩn chấp thuận tại Mục 9.
4. Bàn giao đầy đủ hiện vật theo Mục 12 và cập nhật tài liệu liên quan.
