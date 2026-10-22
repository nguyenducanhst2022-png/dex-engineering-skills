---
name: dex-threat-modeling
description: Conduct structured threat modeling, STRIDE analysis, attack surface mapping, abuse case definition, security control mapping, and risk prioritization. Use when designing new architectures, major feature additions, or security evaluations.
---

# dex-threat-modeling

## 1. Purpose & Scope
Thực hiện mô hình hóa mối đe dọa an ninh có cấu trúc (Threat Modeling); áp dụng phương pháp luận STRIDE (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege), lập bản đồ diện tích bề mặt tấn công (Attack Surface Mapping), phân tích các kịch bản lạm dụng (Abuse Cases) và thiết lập các biện pháp kiểm soát an ninh tương ứng ngay từ giai đoạn thiết kế kiến trúc.

## 2. When to Use
- Khi bắt đầu thiết kế một hệ thống phần mềm mới hoặc bổ sung tính năng tài chính, thanh toán, dữ liệu nhạy cảm.
- Trước khi tiến hành kiểm thử xâm nhập (Penetration Testing) để định hướng các khu vực rủi ro cao.
- Khi cần chứng minh sự an toàn của kiến trúc trong báo cáo thẩm định kỹ thuật (Security Compliance Review).

## 3. When NOT to Use
- Rà soát nhanh các lỗi cú pháp code thông thường (dùng `dex-security-audit`).
- Thiết lập cấu hình mạng tường lửa cấp hạ tầng thuần túy.

## 4. Prerequisites & Input Context
**Đầu vào cần thiết:**
- Sơ đồ luồng dữ liệu kiến trúc hệ thống (Data Flow Diagram - DFD).
- Danh sách các tác nhân (Actors: Khách vãng lai, Người dùng đã đăng nhập, Quản trị viên, Hacker bên ngoài).
- Tài sản cần bảo vệ (Dữ liệu thẻ ngân hàng, PII, Mã nguồn, Khóa giải mã).

**Điều kiện tiên quyết:**
- Đã xác định rõ các ranh giới tin cậy (Trust Boundaries) trong sơ đồ hệ thống.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**: Nắm vững cơ chế vận hành theo chuẩn Agent Skills, tuân thủ nghiêm ngặt tính xác định và ranh giới trách nhiệm.
- **Quy tắc quyết định kỹ thuật**:
- **Ranh Giới Tin Cậy Là Vùng Trọng Yếu**: Bất kỳ dữ liệu nào vượt qua ranh giới tin cậy (từ ngoài internet vào ứng dụng) đều phải được coi là dữ liệu độc hại và phải trải qua validation nghiêm ngặt.
- **Không Chấp Nhận Mối Đe Dọa Mức High/Critical Mà Không Có Biện Pháp Giảm Thiểu**: Không cho phép hệ thống lên production nếu tồn tại mối đe dọa nghiêm trọng chưa có phương án xử lý hoặc chưa được cấp lãnh đạo phê duyệt miễn trừ rủi ro.
- **Bảo Vệ Tính Toàn Vẹn Của Nhật Ký Kiểm Toán (Audit Logs)**: Ngăn chặn nguy cơ Chối bỏ (Repudiation) bằng cách lưu log hành động vào kho lưu trữ bất biến (Append-only storage).
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Lỗi IDOR cho phép đổi ID trong URL để đọc dữ liệu người khác**: Do thiếu kiểm tra phân quyền sở hữu bản ghi -> Phát hiện từ bước STRIDE: Information Disclosure & Elevation of Privilege -> Khắc phục: Áp dụng Row-Level Security hoặc kiểm tra quyền sở hữu đối tượng trước khi trả về dữ liệu.
- **Khách gửi payload JSON 50MB làm sập toàn bộ Node.js process**: Do thiếu giới hạn dung lượng body -> Phát hiện từ bước STRIDE: Denial of Service -> Khắc phục: Cấu hình giới hạn `body-parser limit: 1mb`.

## 6. Step-by-Step Execution Workflow
1. Vẽ sơ đồ luồng dữ liệu (DFD): Xác định rõ Thực thể bên ngoài (External Entities), Quy trình xử lý (Processes), Kho lưu trữ dữ liệu (Data Stores) và Ranh giới tin cậy (Trust Boundaries).
2. Rà soát từng thành phần dựa trên 6 khía cạnh của mô hình STRIDE:
   - *Spoofing (Giả mạo)*: Kẻ tấn công có thể mạo danh người dùng hoặc service khác không?
   - *Tampering (Can thiệp)*: Dữ liệu truyền trên mạng hoặc lưu trong database có thể bị sửa đổi trái phép không?
   - *Repudiation (Chối bỏ)*: Kẻ xấu có thể chối bỏ hành vi vừa thực hiện do thiếu nhật ký kiểm toán không?
   - *Information Disclosure (Lộ thông tin)*: Dữ liệu nhạy cảm có nguy cơ bị đọc trộm qua logs, error message, hoặc mạng không mã hóa?
   - *Denial of Service (Từ chối dịch vụ)*: Kẻ tấn công có thể gửi request nặng làm sập API hoặc hết RAM hệ thống không?
   - *Elevation of Privilege (Leo thang đặc quyền)*: Người dùng thường có thể lợi dụng lỗi để trở thành admin không?
3. Đánh giá mức độ rủi ro của từng mối đe dọa theo ma trận DREAD hoặc thang đo CVSS.
4. Đề xuất biện pháp kiểm soát kỹ thuật (Mitigations) cho từng mối đe dọa được phát hiện.
5. Chuyển các biện pháp kiểm soát thành các nhiệm vụ kỹ thuật cụ thể (Security User Stories) trong backlog dự án.

## 7. Concrete Examples
### Ví dụ triển khai chuẩn mực:
```markdown
# Threat Model: Payment Processing Workflow (STRIDE Analysis)

| STRIDE Element | Threat Scenario | Impact | Mitigation Strategy |
|---|---|---|---|
| **Spoofing** | Attacker fakes webhook from Payment Gateway | High | Verify cryptographic HMAC signature in `X-Signature` header |
| **Tampering** | User alters order amount in browser before checkout | Critical | Re-calculate total price strictly on server side from DB records |
| **Repudiation** | User denies authorizing a \$5,000 transaction | Medium | Store signed audit trail with timestamp, IP, and 2FA confirmation |
| **Information Disclosure** | Credit card CVV logged in application traces | Critical | Strip sensitive PCI fields before logging using sanitize middleware |
| **Denial of Service** | Script spams checkout endpoint 1,000 times/sec | High | Implement Redis token-bucket rate limiting (10 req/min/IP) |
| **Elevation of Privilege**| Normal customer accesses merchant refund panel | High | Enforce strict RBAC with `can('refund', 'order')` guard |
```

### Lệnh xác minh & thực thi:
- Rà soát tài liệu Threat Model: `cat docs/security/threat-model.md`
- Chạy công cụ mô hình hóa mối đe dọa dạng code: `pytm --dfd` hoặc `threat-composer-cli export`
- Kiểm tra các bài test bảo mật mô phỏng kịch bản tấn công: `npm run test:security-scenarios`

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước kiểm tra biên và giả định hệ thống luôn ở trạng thái lý tưởng.
- **Anti-Pattern 2**: Không ghi nhận nhật ký kiểm toán hoặc bỏ qua việc xử lý ngoại lệ lúc runtime.
- **Trap**: Bỏ qua các rào chắn an toàn hoặc cố tình chạy script không qua kiểm thử tự động.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Tài liệu Threat Model phân tích đầy đủ 6 khía cạnh STRIDE trên toàn bộ các luồng dữ liệu chính.
- QG-09: 100% các mối đe dọa mức High và Critical đều có biện pháp kỹ thuật giảm thiểu cụ thể.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động trước khi coi là hoàn thành.

## 10. Security & Safety Boundaries
- Đảm bảo tính bảo mật của tài liệu Threat Model; chỉ chia sẻ nội bộ cho đội ngũ phát triển và bảo mật, không xuất bản công khai ra ngoài.
- Không bao giờ thực thi mã nguồn hoặc thay đổi cấu hình trên môi trường sản xuất mà thiếu cơ chế rollback an toàn.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Có thể kích hoạt trực tiếp từ terminal hoặc extension tương thích trong VS Code / Cursor / Windsurf.

## 12. Deliverables & Output Artifacts
- Tài liệu Mô hình hóa mối đe dọa (`docs/security/threat-model.md`).
- Sơ đồ luồng dữ liệu DFD kèm ranh giới tin cậy trực quan.
- Danh sách các câu chuyện bảo mật (Security Tasks) cần triển khai.

## 13. Related & Complementary Skills
- `dex-development-workflow`: Quy trình phát triển tiêu chuẩn.
- `dex-code-verification`: Xác minh chất lượng và tính đúng đắn của mã nguồn.
- `dex-master-orchestrator`: Bộ điều phối trung tâm kết nối kỹ năng này với các kỹ năng khác trong hệ thống.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư hoặc AI Agent tiếp nhận yêu cầu liên quan đến **dex-threat-modeling**.
1. Đọc kỹ đầu vào và các ràng buộc kỹ thuật tại mục 4.
2. Thực thi tuần tự 6 bước trong Workflow tại mục 6.
3. Chạy các lệnh kiểm chứng tại mục 7 và đối chiếu với Quality Gates tại mục 9.
4. Đóng gói deliverables theo danh sách tại mục 12 và báo cáo kết quả kèm bằng chứng xác thực.
