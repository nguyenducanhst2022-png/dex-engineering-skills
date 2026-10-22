---
name: dex-security-logging-detection
description: Design, instrument, and validate tamper-evident security audit logs and detection rules (Sigma, SIEM) capturing authentication, authorization, and privilege escalation events. Use when establishing SOC visibility and audit compliance.
---

# dex-security-logging-detection

## 1. Purpose & Scope
Thiết kế, xây dựng và kiểm chứng hệ thống ghi nhật ký an ninh không thể chối bỏ (Tamper-evident Security Audit Logging) và các quy tắc phát hiện tấn công (Detection Rules: Sigma, Elastic, Splunk, AWS GuardDuty); ghi nhận đầy đủ các sự kiện nhạy cảm (Đăng nhập, Thay đổi phân quyền, Truy cập dữ liệu nhạy cảm, Leo thang đặc quyền) phục vụ điều tra sự cố (Digital Forensics) và tuân thủ kiểm toán an toàn thông tin.

## 2. When to Use
- Yêu cầu bắt buộc tuân thủ các tiêu chuẩn kiểm toán quốc tế (PCI-DSS Yêu cầu 10, SOC 2, HIPAA, ISO 27001).
- Cần phát hiện sớm các hành vi bất thường của nhân viên nội bộ (Insider Threats) hoặc tài khoản quản trị bị chiếm đoạt.
- Xây dựng trung tâm điều hành an ninh mạng (SOC) cần nguồn dữ liệu sự kiện an ninh chuẩn mực.

## 3. When NOT to Use
- Không ghi nhật ký dữ liệu nhạy cảm của người dùng (Mật khẩu thô, Khóa bí mật, Số thẻ tín dụng đầy đủ, Dữ liệu PII y tế) vào Security Logs.
- Không lưu trữ Security Logs chung trên cùng một máy chủ ứng dụng mà kẻ tấn công có quyền xóa hoặc sửa đổi.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Danh mục các sự kiện an ninh cần giám sát (Security Events Taxonomy).
- Định dạng nhật ký chuẩn (Common Event Format - CEF, JSON OCSF).
- Hệ thống lưu trữ và phân tích SIEM (Elasticsearch, Splunk, Datadog Cloud SIEM).
- **Điều kiện tiên quyết**:
- Máy chủ ứng dụng đã đồng bộ thời gian chuẩn xác qua giao thức NTP (chống sai lệch timestamp trong điều tra).

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Bảy trường thông tin bắt buộc trong Security Audit Log:
  1. Timestamp: Thời gian chính xác đến mili-giây (UTC ISO 8601).
  2. Actor (Who): Ai thực hiện hành động (User ID, IP, User-Agent).
  3. Action (What): Hành động cụ thể là gì (ví dụ: `auth.login.failed`, `role.permission.grant`).
  4. Resource (Where): Thao tác trên đối tượng nào (ví dụ: `document_id: 12345`).
  5. Status (Result): Thành công hay Thất bại (`SUCCESS` / `FAILURE`).
  6. Reason: Lý do nếu thất bại (ví dụ: `INVALID_CREDENTIALS`).
  7. Context: Định danh phiên và Correlation ID để truy vết toàn trình.
- Append-Only & Immutability: Nhật ký an ninh phải được đẩy ngay lập tức về kho lưu trữ chỉ ghi (WORM - Write Once, Read Many) như S3 Object Lock, ngăn chặn kẻ tấn công xóa log để phi tang dấu vết.
- **Quy tắc quyết định kỹ thuật**:
- Mọi sự kiện đăng nhập thất bại, đổi mật khẩu hoặc cấp quyền Admin bắt buộc phải sinh một Security Audit Event độc lập.
- Tuyệt đối cấm sử dụng câu lệnh `logger.debug` để log các tham số chứa thông tin xác thực.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Ứng dụng log chuỗi URL truy vấn có chứa session token hoặc reset-password-token, khiến nhân viên xem log có thể chiếm quyền tài khoản khách hàng.

## 6. Step-by-Step Execution Workflow
1. Xây dựng thư viện chuẩn `SecurityLogger` dùng chung cho toàn bộ các dịch vụ.
2. Tích hợp ghi log an ninh tại các tầng Auth Middleware và Service Controllers.
3. Cấu hình làm sạch tự động (Sanitization) bôi đen toàn bộ các trường nhạy cảm.
4. Đẩy log thời gian thực về kho lưu trữ S3 có khóa bất biến (Object Lock).
5. Viết quy tắc phát hiện Sigma Rules để phát hiện các mẫu hình tấn công phổ biến.
6. Kiểm thử giả lập hành vi tấn công để xác nhận cảnh báo được kích hoạt tới SOC.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```json
// Định dạng Security Audit Log chuẩn mực JSON OCSF
{
  "time": "2026-10-22T15:00:00.123Z",
  "event_type": "USER_MANAGEMENT",
  "action": "role.grant",
  "status": "SUCCESS",
  "actor": {
    "user_id": "usr_admin_987",
    "ip_address": "203.0.113.45",
    "session_id": "sess_abc123"
  },
  "target_resource": {
    "type": "user",
    "id": "usr_dev_456",
    "changes": {
      "added_role": "SUPER_ADMIN"
    }
  },
  "correlation_id": "req-trace-uuid-7788"
}
```

### Lệnh xác minh & thực thi:
```bash
# Kiểm thử cú pháp quy tắc Sigma và chuyển đổi sang query SIEM
sigmac -t splunk -c rules/sigma/privilege_escalation.yml
```

## 8. Anti-Patterns & Common Traps
- Ghi log an ninh dưới dạng văn bản thô không có cấu trúc khiến máy SIEM không thể bóc tách trường tự động.
- Cho phép ứng dụng ghi đè hoặc sửa đổi các bản ghi log đã lưu trong quá khứ.

## 9. Quality Gates & Acceptance Criteria
- 100% các hành động thay đổi phân quyền và đăng nhập thất bại đều được ghi nhận vào Security Audit Log.
- Thời gian từ khi sự kiện diễn ra đến khi xuất hiện trên SIEM dưới 60 giây.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Quyền truy cập vào Security Logs phải được kiểm soát nghiêm ngặt theo nguyên tắc Four-Eyes Principle (cần 2 người phê duyệt).
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ thống An ninh & SkillOps**: Tương thích GitHub Actions, SARIF, CycloneDX/SPDX, Semgrep, OWASP ZAP.

## 12. Deliverables & Output Artifacts
- Module Security Logger chuẩn hóa JSON.
- Bộ quy tắc phát hiện tấn công Sigma Rules và tài liệu kiểm toán tuân thủ.

## 13. Related & Complementary Skills
dex-log-pipeline-design, dex-cloud-iam-policy-review, dex-secure-build-runners

## 14. Realistic Usage Example
### Tình huống thực tế:
Một công ty công nghệ bị một tài khoản quản trị viên thực hiện hành vi nội gián, tự thêm quyền truy cập vào dữ liệu lương nhân viên. Nhờ hệ thống Security Audit Logging ghi nhận bất biến và đẩy cảnh báo Sigma Rule 'Privilege Escalation Detected' về kênh Slack của đội ngũ An ninh thông tin trong vòng 30 giây, vụ việc đã bị chặn đứng ngay lập tức và thu hồi toàn bộ quyền truy cập.
