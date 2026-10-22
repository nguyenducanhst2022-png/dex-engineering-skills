---
name: dex-api-abuse-prevention
description: Architect, detect, and mitigate automated API abuse, credential stuffing, scraping, and bot attacks using behavioral fingerprinting, proof-of-work challenges, and adaptive throttling. Use when protecting public API gateways from malicious bots.
---

# dex-api-abuse-prevention

## 1. Purpose & Scope
Thiết kế, xây dựng và triển khai hệ thống chống lạm dụng API tự động (API Abuse Prevention: Bot Detection, Credential Stuffing, Scraping, Bẻ khóa OTP/Voucher); áp dụng kỹ thuật nhận diện dấu vân tay hành vi (Behavioral Fingerprinting), thách thức giải mã Proof-of-Work / Turnstile, và cơ chế điều tiết thích ứng (Adaptive Throttling) nhằm bảo vệ cửa ngõ API Gateway mà không gây phiền hà cho người dùng chân chính.

## 2. When to Use
- Phát hiện các đợt tấn công nhồi thông tin đăng nhập (Credential Stuffing) quy mô lớn nhằm chiếm đoạt tài khoản người dùng.
- Dữ liệu giá cả, danh mục sản phẩm bị đối thủ cạnh tranh cào quét (scraping) tự động liên tục.
- Hệ thống gửi mã OTP SMS bị bot spam làm thất thoát hàng ngàn USD chi phí viễn thông.

## 3. When NOT to Use
- Không chặn IP vội vã chỉ dựa trên địa chỉ IP đơn thuần (nguy cơ chặn nhầm người dùng cùng mạng công ty sau NAT proxy).
- Không ép buộc người dùng chân chính phải giải các bài toán CAPTCHA hình ảnh biến dạng phức tạp gây suy giảm tỉ lệ chuyển đổi.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Nhật ký truy cập API Gateway (Nginx/Envoy logs, Cloudflare logs).
- Dấu hiệu bất thường (Tỉ lệ login thất bại cao, Tốc độ gọi API nhanh hơn phản xạ con người).
- Công cụ bảo vệ (Cloudflare Turnstile, AWS WAF Bot Control, hCaptcha, FingerprintJS).
- **Điều kiện tiên quyết**:
- Có quyền cấu hình WAF (Web Application Firewall) hoặc API Gateway middleware.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Credential Stuffing vs Brute Force: Brute Force thử nhiều mật khẩu cho 1 user; Credential Stuffing thử hàng triệu cặp username/password rò rỉ từ các vụ lộ lọt dữ liệu khác lên hệ thống của bạn để tìm tài khoản dùng chung mật khẩu.
- Invisible Proof-of-Work (PoW): Yêu cầu trình duyệt giải một bài toán băm SHA-256 nhỏ trong 100ms dưới nền. Người dùng bình thường không nhận ra, nhưng bot chạy 1 triệu requests sẽ bị cạn kiệt CPU ngay lập tức.
- Behavioral Velocity Checking: Theo dõi tốc độ hành động: Nếu 1 địa chỉ IP thử đăng nhập vào 15 tài khoản khác nhau trong 1 phút => Hành vi bot rõ ràng, tự động chặn ngay lập tức.
- **Quy tắc quyết định kỹ thuật**:
- Nếu một tài khoản đăng nhập sai 5 lần liên tiếp: tạm khóa đăng nhập trong 15 phút hoặc kích hoạt xác thực 2 lớp qua email.
- Với endpoint gửi OTP SMS: bắt buộc giải Turnstile token hợp lệ ở phía client trước khi server phát lệnh gửi tin nhắn.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Cấu hình bot detection quá nhạy cảm, chặn nhầm toàn bộ các lượt truy cập của người dùng sử dụng trình duyệt bảo mật Brave hoặc tính năng ẩn danh iCloud Private Relay.

## 6. Step-by-Step Execution Workflow
1. Phân tích access logs để lập danh sách các endpoint nhạy cảm thường xuyên bị tấn công.
2. Tích hợp Cloudflare Turnstile hoặc mCaptcha không gây phiền hà tại màn hình đăng nhập và đăng ký.
3. Xây dựng middleware kiểm tra tốc độ hành động (Velocity Check) dựa trên Redis phân tán.
4. Triển khai dấu vân tay thiết bị (Device Fingerprint) để theo dõi các hành vi lạm dụng vượt qua thay đổi IP.
5. Thiết lập dashboard giám sát tỉ lệ chặn bot và tỉ lệ khiếu nại của người dùng thật.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```python
# Middleware kiểm tra tốc độ bất thường trên endpoint đăng nhập
async def check_credential_stuffing_risk(request: Request, redis_client):
    client_ip = get_trusted_client_ip(request)
    failed_key = f"abuse:login_fail:ip:{client_ip}"
    
    # Đếm số lần đăng nhập sai từ IP này trong 5 phút qua
    failed_count = await redis_client.get(failed_key)
    if failed_count and int(failed_count) > 10:
        # Yêu cầu giải Turnstile CAPTCHA bắt buộc nếu nghi ngờ bot
        turnstile_token = request.headers.get("X-Turnstile-Token")
        if not await verify_turnstile_token(turnstile_token):
            raise HTTPException(status_code=403, detail="Hành vi bất thường - Vui lòng xác thực CAPTCHA")
```

### Lệnh xác minh & thực thi:
```bash
# Giả lập tấn công credential stuffing để kiểm tra cơ chế chặn tự động
python scripts/simulate_bot_attack.py --target http://localhost:8080/api/v1/auth/login
```

## 8. Anti-Patterns & Common Traps
- Để lộ thông báo phân biệt 'Tài khoản không tồn tại' và 'Mật khẩu không đúng' (giúp kẻ tấn công dò tìm danh sách user hợp lệ - Username Enumeration).
- Không áp dụng rate limit đối với các endpoint nhạy cảm như Quên mật khẩu hoặc Gửi lại OTP.

## 9. Quality Gates & Acceptance Criteria
- Chặn đứng tối thiểu 99% các nỗ lực tấn công Credential Stuffing tự động.
- Tỉ lệ chặn nhầm người dùng hợp lệ (False Positive Block Rate) dưới 0.1%.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Dữ liệu dấu vân tay thiết bị (Fingerprint) phải tuân thủ chính sách quyền riêng tư và không được dùng để theo dõi người dùng trái phép.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ thống An ninh & SkillOps**: Tương thích GitHub Actions, SARIF, CycloneDX/SPDX, Semgrep, OWASP ZAP.

## 12. Deliverables & Output Artifacts
- Middleware phát hiện và ngăn chặn bot tự động.
- Bảng quy tắc WAF và cấu hình chống lạm dụng trên API Gateway.

## 13. Related & Complementary Skills
dex-rate-limiting-quotas, dex-web-security-headers, dex-api-abuse-prevention

## 14. Realistic Usage Example
### Tình huống thực tế:
Một ứng dụng đặt vé xem phim bị các đối thủ sử dụng bot tự động giữ hết các ghế đẹp để bán lại chợ đen. Sau khi triển khai Invisible Proof-of-Work kết hợp giới hạn tốc độ đặt chỗ theo Device Fingerprint, 99.8% bot đầu cơ đã bị vô hiệu hóa hoàn toàn, trả lại cơ hội mua vé đúng giá cho người hâm mộ chân chính.
