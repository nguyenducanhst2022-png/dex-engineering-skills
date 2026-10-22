---
name: dex-privacy-impact-assessment
description: Conduct Data Protection and Privacy Impact Assessments (DPIA/PIA) adhering to GDPR, CCPA, and ISO 27701 with personal data classification, data flow mapping, and minimization safeguards. Use when processing personal data or auditing privacy compliance.
---

# dex-privacy-impact-assessment

## 1. Purpose & Scope
Thực hiện đánh giá tác động quyền riêng tư và bảo vệ dữ liệu (Data Protection & Privacy Impact Assessment - DPIA/PIA) tuân thủ các quy định quốc tế (GDPR, CCPA/CPRA, ISO 27701, Nghị định 13/2023/NĐ-CP); phân loại dữ liệu cá nhân (Personal Data vs Sensitive PII), lập sơ đồ luồng dữ liệu (Data Flow Mapping), áp dụng nguyên tắc giảm thiểu dữ liệu (Data Minimization), kiểm soát cơ chế đồng ý của người dùng (Consent Management) và thiết lập các rào chắn kỹ thuật bảo vệ quyền của chủ thể dữ liệu (Quyền được quên, Quyền xuất dữ liệu).

## 2. When to Use
- Khi ra mắt tính năng mới thu thập, lưu trữ hoặc xử lý thông tin định danh cá nhân (PII: Tên, Email, Số điện thoại, Địa chỉ, Căn cước, Vị trí).
- Khi tích hợp dịch vụ bên thứ ba (Analytics, CRM, AI Model Providers) có hành vi truyền dữ liệu người dùng ra bên ngoài.
- Khi mở rộng dịch vụ sang thị trường Liên minh Châu Âu (EU), Bắc Mỹ hoặc các quốc gia có luật bảo vệ dữ liệu nghiêm ngặt.

## 3. When NOT to Use
- Đánh giá lỗ hổng bảo mật hạ tầng mạng hoặc tấn công thâm nhập pentest (dùng `dex-security-audit` hoặc `dex-threat-modeling`).
- Thiết lập mã hóa lưu trữ ở mức tệp/đĩa cứng (dùng `dex-secrets-management`).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Danh mục các trường dữ liệu thu thập (Data Schema).
- Mục đích xử lý cụ thể của từng trường dữ liệu và cơ sở pháp lý tương ứng (Lawful Basis: Hợp đồng, Đồng ý, Nghĩa vụ pháp lý).
- Sơ đồ lưu trữ và các bên thứ ba nhận dữ liệu (Sub-processors).
- **Điều kiện tiên quyết**:
- Hiểu rõ các nguyên tắc cốt lõi của GDPR/CCPA (Purpose Limitation, Storage Limitation, Accountability).
- Danh sách các bên xử lý phụ (Sub-processors: AWS, Stripe, Google Analytics, OpenAI).

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- **Data Minimization Principle**: Chỉ thu thập đúng và đủ những trường thông tin tối thiểu phục vụ cho mục đích đã công bố; cấm thu thập 'dự phòng cho tương lai'.
- **Privacy by Design & by Default**: Quyền riêng tư phải được tích hợp vào kiến trúc hệ thống ngay từ giai đoạn thiết kế ban đầu; mặc định cài đặt luôn ở mức bảo vệ cao nhất (Opt-in thay vì Opt-out).
- **Data Subject Rights Automation**: Hệ thống phải có khả năng kỹ thuật để tự động tìm kiếm, xuất bản hoặc xóa sạch toàn bộ dữ liệu của một người dùng cụ thể (Right to Erasure / RTBF) trong tối đa 30 ngày.
- **Quy tắc quyết định kỹ thuật**:
- **Tách Biệt Bảng Dữ Liệu PII Nhạy Cảm**: Dữ liệu PII nhạy cảm (Căn cước, Sinh trắc học, Y tế) phải được lưu ở bảng phân tách, mã hóa cấp trường (Field-Level Encryption) với khóa KMS riêng biệt.
- **Không Lưu Dữ Liệu Cá Nhân Trong Log**: Cấm tuyệt đối ghi email, số điện thoại, token, mật khẩu vào hệ thống log tập trung (ELK, Datadog, CloudWatch).
- **Thời Hạn Lưu Trữ Rõ Ràng (Retention Policy)**: Mọi bảng dữ liệu người dùng phải có chính sách xóa tự động sau khi kết thúc mục đích hợp đồng hoặc quá hạn lưu trữ.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Bị phạt hàng triệu Euro do lưu trữ dữ liệu người dùng đã yêu cầu xóa**: Do tính năng xóa tài khoản chỉ xóa trên DB chính nhưng bỏ quên trên Read Replicas, Data Lake và Backups -> Khắc phục: Thiết lập sự kiện `UserDeletedEvent` kích hoạt quy trình xóa cascading xuyên suốt toàn bộ hệ sinh thái dữ liệu.
- **Lộ PII ra ngoài khi truyền cho công cụ Analytics**: Tự động gửi toàn bộ URL chứa query param `?email=user@example.com` vào Google Analytics -> Khắc phục: Áp dụng middleware client-side tự động làm sạch URL trước khi emit event.

## 6. Step-by-Step Execution Workflow
1. Khảo sát danh mục dữ liệu: Lập bảng kiểm kê tài sản dữ liệu (Data Inventory / RoPA - Record of Processing Activities).
2. Phân loại mức độ nhạy cảm: Public, Internal, Confidential, Sensitive PII.
3. Lập sơ đồ luồng dữ liệu (Data Flow Diagram): Xác định điểm vào, nơi lưu trữ, bên xử lý phụ và điểm ra.
4. Đánh giá tính cần thiết và cân xứng (Proportionality Assessment): Loại bỏ các trường dữ liệu thừa thãi.
5. Đánh giá rủi ro đối với quyền của chủ thể dữ liệu (Khả năng lộ lọt, rủi ro phân biệt đối xử).
6. Đề xuất các biện pháp giảm thiểu rủi ro: Ẩn danh hóa (Anonymization), Giả danh hóa (Pseudonymization), Mã hóa.
7. Hoàn thiện báo cáo DPIA chính thức, ký duyệt cùng Data Protection Officer (DPO) và lưu trữ hồ sơ tuân thủ.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```markdown
# Data Protection Impact Assessment (DPIA) Template Summary

### 1. Thông Tin Chung Dự Án
- **Dự án**: Tính năng Xác thực Sinh trắc học & Đăng ký Khách hàng mới
- **Ngày đánh giá**: 2026-10-22 | **Phiên bản**: 1.0

### 2. Danh Mục Dữ Liệu Thu Thập & Cơ Sở Pháp Lý
| Trường Dữ Liệu | Phân Loại | Mục Đích Thu Thập | Cơ Sở Pháp Lý | Thời Gian Lưu Trữ |
|:---|:---|:---|:---|:---|
| Email | PII Thông thường | Tạo tài khoản, liên lạc | Hợp đồng (Art 6.1.b) | Xóa sau khi đóng tài khoản |
| Số điện thoại | PII Thông thường | Xác thực OTP 2FA | Nghĩa vụ pháp lý bảo mật | Xóa sau khi đóng tài khoản |
| Ảnh CCCD | PII Nhạy cảm | Định danh eKYC theo luật NH | Nghĩa vụ pháp lý (Art 6.1.c) | 5 năm theo Luật Phòng chống rửa tiền |
| Khuôn mặt (Biometrics) | PII Đặc biệt | Đối chiếu khuôn mặt | Đồng ý tường minh (Art 9.2.a) | Không lưu ảnh gốc; chỉ lưu vector mã hóa |

### 3. Biện Pháp Giảm Thiểu Kỹ Thuật (Safeguards)
- **Pseudonymization**: Mã hóa một chiều ID người dùng bằng muối bí mật trước khi lưu vào Data Warehouse.
- **Field-Level Encryption**: Dữ liệu CCCD được mã hóa bằng AES-256-GCM với AWS KMS Master Key độc lập.
- **Zero Log PII**: Cấu hình bộ lọc log Winston/Logback tự động regex che dấu email và số điện thoại.
```

### Lệnh xác minh & thực thi:
- Quét mã nguồn kiểm tra PII trong log: `grep -rEi "(password|email|phone|ssn|token)" src/ | grep -Ei "(console.log|logger|print)"`
- Kiểm tra endpoint xuất dữ liệu người dùng (GDPR Export API): `curl -X GET https://api.example.com/api/v1/users/me/privacy-export -H "Authorization: Bearer <token>"`
- Xác minh tính năng xóa tài khoản (GDPR Erasure API): Kiểm tra truy vấn database sau khi xóa trả về 0 bản ghi

## 8. Anti-Patterns & Common Traps
- **Bắt người dùng đồng ý với điều khoản chung chung không thể tách rời (Bundled Consent)**: Buộc phải đồng ý nhận email quảng cáo mới được dùng app.
- **Chỉ che mờ (mask) trên giao diện nhưng vẫn trả về đầy đủ PII qua JSON API**: Hacker chỉ cần mở DevTools Network tab là thấy toàn bộ dữ liệu thô.
- **Lưu trữ dữ liệu nhạy cảm vĩnh viễn không có hạn xóa**: Vi phạm nghiêm trọng nguyên tắc Storage Limitation.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Báo cáo DPIA được hoàn thành đầy đủ các trường và có sự phê chuẩn của DPO.
- QG-07: 0 trường dữ liệu PII nhạy cảm bị lưu trữ dưới dạng văn bản thuần (plain text).
- QG-11: Chức năng xuất dữ liệu (Data Portability) và Xóa dữ liệu (Erasure) được kiểm thử hoạt động tự động.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi deploy.

## 10. Security & Safety Boundaries
- Mọi luồng truyền dữ liệu xuyên biên giới (Cross-border data transfer) phải tuân thủ điều kiện Standard Contractual Clauses (SCCs).
- Cấm sử dụng dữ liệu PII thật trong môi trường Development và Staging; bắt buộc dùng synthetic/mock data.
- Không bao giờ lưu trữ hardcoded secret hoặc cấp quyền quá mức (over-permissioned IAM).

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Môi trường Vận hành & Tuân thủ**: Hỗ trợ GDPR/CCPA tooling, SOC 2 / ISO 27001 automation, ArgoCD drift, RICE spreadsheets, Jira/GitHub triage.

## 12. Deliverables & Output Artifacts
- Bản tài liệu Đánh giá Tác động Quyền riêng tư (DPIA Report).
- Sơ đồ luồng dữ liệu (Data Flow Diagram).
- Quy trình tự động xử lý yêu cầu quyền của người dùng (Data Subject Request Runbook).

## 13. Related & Complementary Skills
- `dex-compliance-control-mapping`: Khớp nối các yêu cầu bảo vệ dữ liệu với khung tuân thủ tổng thể.
- `dex-analytics-instrumentation`: Làm sạch dữ liệu trước khi gửi sang hệ thống phân tích.
- `dex-audit-trail-integrity`: Ghi vết kiểm toán các thao tác truy cập dữ liệu nhạy cảm.

## 14. Realistic Usage Example
### Tình huống thực tế:
Một công ty công nghệ y tế chuẩn bị ra mắt tính năng đặt lịch khám bệnh trực tuyến. Áp dụng `dex-privacy-impact-assessment`, kỹ sư phân tích luồng dữ liệu, phát hiện form đăng ký đang đòi hỏi cả tiền sử bệnh án gia đình không cần thiết (vi phạm Data Minimization). Đội ngũ loại bỏ trường này, mã hóa trường số bảo hiểm y tế bằng AWS KMS, tích hợp chức năng cho phép người dùng tự tải về toàn bộ hồ sơ bệnh án của họ dưới dạng file ZIP mã hóa, đảm bảo tuân thủ đầy đủ chuẩn HIPAA và GDPR.
