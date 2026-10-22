---
name: dex-dast-scoping
description: Define authorized scopes, scan profiles, boundary exclusions, and rate limits for Dynamic Application Security Testing (DAST) using OWASP ZAP or Burp Suite. Use when setting up automated live security scans without breaking environments.
---

# dex-dast-scoping

## 1. Purpose & Scope
Xác định phạm vi ủy quyền (Authorized Scoping), hồ sơ quét (Scan Profiles), các điểm loại trừ an toàn (Boundary Exclusions) và giới hạn tần suất quét (Rate Limits) cho việc kiểm thử an ninh ứng dụng động (DAST: OWASP ZAP, Burp Suite Enterprise); bảo đảm quét phát hiện lỗ hổng runtime một cách triệt để mà không gây sập môi trường, không làm đầy dữ liệu rác và không kích hoạt các hành động nguy hiểm ngoài ý muốn.

## 2. When to Use
- Thiết lập quy trình quét DAST định kỳ tự động trên môi trường Staging/UAT.
- Chuẩn bị đánh giá kiểm thử thâm nhập (Penetration Testing) ứng dụng web/API.
- Sau khi triển khai các thay đổi lớn liên quan đến cơ chế xác thực hoặc Session Management.

## 3. When NOT to Use
- Tuyệt đối không chạy DAST trên môi trường Production đang phục vụ khách hàng thực tế mà không có văn bản chấp thuận rủi ro từ ban giám đốc.
- Tuyệt đối không quét DAST vào các hệ thống bên thứ ba tích hợp (như cổng thanh toán ngân hàng, dịch vụ gửi SMS) nằm ngoài phạm vi sở hữu.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- OpenAPI Specification hoặc tài liệu endpoint của ứng dụng.
- Văn bản cấp quyền quét an ninh (Rules of Engagement / RoE) có chữ ký phê duyệt.
- Thông tin tài khoản thử nghiệm chuyên dụng (Test Credentials).
- **Điều kiện tiên quyết**:
- Môi trường Staging đã được backup toàn bộ và có thể tự động khôi phục (Reset) về trạng thái sạch sau khi quét.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Safe DAST Scanning:
  + Passive Scan: Chỉ phân tích các request/response đi qua proxy mà không can thiệp, không sinh payload độc hại (an toàn 100%, có thể chạy trên prod).
  + Active Scan: Bơm các payload tấn công (SQLi, XSS, SSRF) vào ứng dụng để kiểm tra phản hồi. Tiềm ẩn nguy cơ làm sập máy chủ hoặc ghi dữ liệu rác khổng lồ.
- Critical Exclusions: Bắt buộc loại trừ các nút/link nguy hiểm khỏi phạm vi quét của spider (ví dụ: nút 'Xóa tài khoản', link 'Gửi email hàng loạt', nút 'Reset mật khẩu toàn bộ công ty').
- Session Handling: Duy trì phiên đăng nhập hợp lệ cho DAST crawler để quét được các trang nằm sau màn hình login.
- **Quy tắc quyết định kỹ thuật**:
- Giới hạn tốc độ quét tối đa 20 requests/giây để tránh làm tê liệt máy chủ test.
- Bắt buộc gắn Header nhận dạng quét chuyên dụng (ví dụ: `X-Security-Scan: Authorized-DAST-Zap`) để đội ngũ SRE không bị nhầm là tấn công thật.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Fuzzer của DAST quét vào endpoint `POST /api/v1/users/delete-all`, khiến toàn bộ cơ sở dữ liệu môi trường test bị xóa sạch giữa chừng.

## 6. Step-by-Step Execution Workflow
1. Xác định ranh giới URL mục tiêu (Target Scope: `https://staging.example.com/*`).
2. Cấu hình danh sách URL loại trừ (Exclude Regex: `logout`, `delete`, `reset`, `payment`).
3. Thiết lập thông số xác thực tự động (Form-based auth hoặc Script-based auth) trong OWASP ZAP.
4. Chạy kiểm thử Spider nạp toàn bộ cấu trúc trang web.
5. Khởi động Active Scan với policy được tùy chỉnh (tập trung vào Top 10 OWASP).
6. Xuất báo cáo lỗ hổng và khôi phục môi trường test.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```yaml
# OWASP ZAP Automation Framework (AF) Scope Configuration
env:
  contexts:
    - name: "Staging-App-Context"
      urls:
        - "https://staging.app.example.com/"
      includePaths:
        - "https://staging.app.example.com/api/v1/.*"
      excludePaths:
        - "https://staging.app.example.com/api/v1/auth/logout"
        - "https://staging.app.example.com/api/v1/account/delete"
        - "https://staging.app.example.com/.*\\?.*action=destroy.*"
      authentication:
        method: "json"
        parameters:
          loginPageUrl: "https://staging.app.example.com/api/v1/auth/login"
          loginBody: '{"email": "scanner@example.com", "password": "test_pass_123"}'
```

### Lệnh xác minh & thực thi:
```bash
# Chạy OWASP ZAP quét tự động theo cấu hình phạm vi an toàn
zap.sh -cmd -autorun zap-config.yaml
```

## 8. Anti-Patterns & Common Traps
- Chạy Active Scan với cấu hình mặc định thả nổi spider tự do bấm vào mọi nút trên màn hình.
- Quét vào ban ngày trên môi trường dùng chung làm gián đoạn công việc của các đội ngũ QA khác.

## 9. Quality Gates & Acceptance Criteria
- 100% các endpoint nhạy cảm được cấu hình loại trừ an toàn trong file phạm vi.
- Không có bất kỳ sự cố sập máy chủ hoặc mất dữ liệu ngoài ý muốn nào trong quá trình quét.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Mọi payload DAST phải có header định danh ủy quyền hợp pháp rõ ràng.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ thống An ninh & SkillOps**: Tương thích GitHub Actions, SARIF, CycloneDX/SPDX, Semgrep, OWASP ZAP.

## 12. Deliverables & Output Artifacts
- File cấu hình phạm vi quét DAST an toàn (`zap-context.yaml`).
- Báo cáo lỗ hổng động kèm bằng chứng request/response tái hiện lỗi.

## 13. Related & Complementary Skills
dex-sast-finding-triage, dex-api-fuzz-testing, dex-vulnerability-remediation

## 14. Realistic Usage Example
### Tình huống thực tế:
Một công ty bảo hiểm muốn tích hợp DAST vào pipeline kiểm thử trước khi release. Ban đầu, tool quét tự động kích hoạt chức năng gửi email làm ngập hòm thư của 1,000 khách hàng thử nghiệm. Sau khi chuyên gia DAST Scoping thiết lập ranh giới loại trừ chính xác các endpoint gửi mail và đặt rate limit 15 req/s, quá trình quét diễn ra êm đẹp mỗi đêm, phát hiện 2 lỗ hổng Reflected XSS mà không làm phiền bất kỳ ai.
