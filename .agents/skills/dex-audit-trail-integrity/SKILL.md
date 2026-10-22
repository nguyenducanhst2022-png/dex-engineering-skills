---
name: dex-audit-trail-integrity
description: Implement append-only, tamper-evident audit logging with cryptographic hash chaining (Merkle trees, HMAC), immutable storage (S3 Object Lock / WORM), non-repudiation, and CloudEvents schemas. Use when building compliance-grade audit systems.
---

# dex-audit-trail-integrity

## 1. Purpose & Scope
Thiết kế và hiện thực hóa hệ thống ghi nhận nhật ký kiểm toán bất biến (Append-Only Tamper-Evident Audit Trail) đạt tiêu chuẩn chứng cứ pháp lý và tuân thủ kiểm toán; áp dụng kỹ thuật xâu chuỗi băm mật mã học (Cryptographic Hash Chaining / Merkle Trees / HMAC), lưu trữ trên phương tiện bất biến không thể xóa sửa (WORM - Write Once Read Many / S3 Object Lock Compliance Mode), đảm bảo tính toàn vẹn (Integrity), tính không thể chối bỏ (Non-Repudiation) và chuẩn hóa cấu trúc sự kiện theo định dạng CloudEvents / CADF.

## 2. When to Use
- Khi hệ thống xử lý các giao dịch tài chính, dữ liệu y tế hoặc thay đổi quyền quản trị nhạy cảm bắt buộc phải lưu vết không thể can thiệp.
- Khi cần chứng minh với kiểm toán viên hoặc cơ quan điều tra rằng các bản ghi log không bị quản trị viên nội bộ hay hacker chỉnh sửa sau sự cố.
- Khi xây dựng tính năng Activity Log / Audit Log cho khách hàng doanh nghiệp B2B.

## 3. When NOT to Use
- Thu thập log gỡ lỗi (debug logging) hoặc log ứng dụng thông thường có thể xoay vòng sau 7 ngày (dùng `dex-production-monitoring`).
- Lưu trữ dữ liệu nghiệp vụ có tính năng cập nhật/chỉnh sửa thường xuyên (dùng `dex-database-engineering`).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Định danh tác nhân thực hiện (Actor: ID, Email, Role, IP Address, User-Agent).
- Hành động nghiệp vụ (Action: `user.created`, `role.assigned`, `funds.transferred`).
- Trạng thái trước và sau khi thay đổi (State Diff: Previous vs New values).
- Khóa bí mật dùng để ký xác thực (HMAC Secret Key hoặc Private Key asymmetric).
- **Điều kiện tiên quyết**:
- Cơ chế lưu trữ hỗ trợ tính năng Object Lock (AWS S3 Object Lock, GCP Bucket Retention, Azure Immutable Blob).
- Thư viện mật mã học hỗ trợ hàm băm SHA-256 hoặc SHA-3.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- **Cryptographic Hash Chaining Invariance**: Mỗi bản ghi log thứ `N` chứa mã băm của bản ghi `N-1`: `Hash(N) = SHA256(Payload(N) + Hash(N-1))`. Nếu kẻ tấn công thay đổi 1 ký tự trong bản ghi quá khứ, toàn bộ chuỗi băm phía sau sẽ bị phá vỡ ngay lập tức.
- **WORM Storage (Write Once, Read Many)**: Cấu hình bucket ở chế độ `Compliance Mode` với thời hạn lưu giữ bắt buộc (ví dụ 7 năm); ngay cả tài khoản Root AWS cũng không thể xóa hoặc sửa tệp trước khi hết hạn.
- **Non-Repudiation (Không thể chối bỏ)**: Mọi hành động đều được gắn với chữ ký số hoặc JWT đã xác thực của tác nhân tại thời điểm xảy ra sự kiện.
- **Quy tắc quyết định kỹ thuật**:
- **Tách Biệt Audit Log Khỏi Database Ứng Dụng**: Nhật ký kiểm toán phải được chuyển ngay lập tức sang một tài khoản đám mây riêng biệt (Dedicated Security/Audit AWS Account) mà lập trình viên và quản trị viên vận hành không có quyền truy cập.
- **Cấm Tuyệt Đối Thao Tác UPDATE hoặc DELETE**: Hệ thống audit trail chỉ hỗ trợ duy nhất thao tác INSERT (Append-Only).
- **Không Lưu Thông Tin Bí Mật Vào Audit Log**: Che mờ mật khẩu, mã PIN hoặc số thẻ trước khi đưa vào payload sự kiện.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Quản trị viên bị lộ tài khoản và xóa sạch log để xóa dấu vết**: Do lưu log trên cùng một AWS account với app -> Khắc phục: Bật S3 Object Lock ở Compliance Mode và gửi log sang AWS Account cô lập qua S3 Cross-Region Cross-Account Replication.
- **Phát hiện chuỗi log bị can thiệp nhưng không biết vị trí sửa đổi**: Do không dùng Hash Chaining -> Khắc phục: Duyệt tuần tự chuỗi hash từ bản ghi đầu tiên; vị trí đầu tiên có mã hash tính lại không khớp chính là điểm bị tấn công.

## 6. Step-by-Step Execution Workflow
1. Định nghĩa Schema sự kiện kiểm toán chuẩn hóa theo CloudEvents: `id`, `source`, `type`, `time`, `actor`, `action`, `resource`, `diff`.
2. Lấy mã băm của bản ghi kiểm toán liền trước (`previous_hash`) từ kho lưu trữ.
3. Tính toán mã băm cho bản ghi hiện tại: `current_hash = SHA256(event_data + previous_hash)`.
4. Ký số hoặc tạo HMAC cho bản ghi bằng secret key an toàn.
5. Ghi bản ghi vào cơ sở dữ liệu kiểm toán và đẩy tệp log nén vào S3 Bucket có bật Object Lock Compliance Mode.
6. Xây dựng dịch vụ kiểm tra tính toàn vẹn (Integrity Verification Job) chạy định kỳ hàng tuần: Duyệt toàn bộ chuỗi băm để xác nhận không có mắt xích nào bị đứt.
7. Cung cấp giao diện truy vấn Audit Trail an toàn cho đội ngũ bảo mật và kiểm toán viên.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```typescript
import crypto from 'crypto';

export interface AuditEvent {
  id: string;
  timestamp: string;
  actor: { id: string; email: string; ip: string };
  action: string;
  resource: { type: string; id: string };
  diff?: { before: any; after: any };
  previousHash: string;
  hash: string;
}

export function createAuditEvent(
  actor: AuditEvent['actor'],
  action: string,
  resource: AuditEvent['resource'],
  diff: any,
  previousHash: string
): AuditEvent {
  const id = crypto.randomUUID();
  const timestamp = new Date().toISOString();
  
  // Gom dữ liệu để tạo chuỗi băm mật mã học (Hash Chaining)
  const payload = JSON.stringify({ id, timestamp, actor, action, resource, diff, previousHash });
  const hash = crypto.createHash('sha256').update(payload).digest('hex');
  
  return {
    id,
    timestamp,
    actor,
    action,
    resource,
    diff,
    previousHash,
    hash,
  };
}
```

### Lệnh xác minh & thực thi:
- Kiểm tra cấu hình S3 Object Lock: `aws s3api get-object-lock-configuration --bucket my-audit-logs-bucket`
- Chạy script kiểm chứng chuỗi hash: `python scripts/verify_audit_integrity.py --from 2026-01-01 --to 2026-10-22`
- Thử nghiệm xóa tệp log (phải bị AWS từ chối với lỗi `AccessDenied: Object is locked`): `aws s3 rm s3://my-audit-logs-bucket/audit-2026-10-01.json.gz`

## 8. Anti-Patterns & Common Traps
- **Lưu Audit Trail trong bảng MySQL thông thường không bật bảo vệ**: Bất kỳ ai có quyền root DB đều có thể chạy lệnh `UPDATE audit_logs SET action='...'` mà không để lại dấu vết.
- **Bỏ qua địa chỉ IP và danh tính người thực hiện**: Lưu log kiểu 'User updated' mà không biết là user nào từ IP nào.
- **Ghi nhật ký kiểm toán không đồng bộ bị mất khi server sập**: Không dùng cơ chế buffer/queue tin cậy dẫn tới mất mát các sự kiện trước khi crash.

## 9. Quality Gates & Acceptance Criteria
- QG-01: 100% các hành động thay đổi quyền và giao dịch quan trọng đều sinh sự kiện Audit Trail.
- QG-07: S3 Bucket lưu trữ log được cấu hình Object Lock ở Compliance Mode tối thiểu 365 ngày.
- QG-11: Thuật toán kiểm tra tính toàn vẹn (Hash Chain Verification) xác nhận 100% tính khớp nối của chuỗi băm.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi deploy.

## 10. Security & Safety Boundaries
- Khóa ký số của hệ thống audit trail phải được lưu trữ trong AWS KMS / HashiCorp Vault.
- Cấm mọi quyền can thiệp cấp quyền `s3:BypassGovernanceRetention` trong IAM Policy.
- Không bao giờ lưu trữ hardcoded secret hoặc cấp quyền quá mức (over-permissioned IAM).

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Môi trường Vận hành & Tuân thủ**: Hỗ trợ GDPR/CCPA tooling, SOC 2 / ISO 27001 automation, ArgoCD drift, RICE spreadsheets, Jira/GitHub triage.

## 12. Deliverables & Output Artifacts
- Module tạo và kiểm chứng nhật ký kiểm toán có Hash Chaining.
- Tệp cấu hình lưu trữ bất biến S3 Object Lock / WORM.
- Báo cáo kết quả kiểm chứng tính toàn vẹn của chuỗi log định kỳ.

## 13. Related & Complementary Skills
- `dex-compliance-control-mapping`: Cung cấp bằng chứng toàn vẹn cho tiêu chí SOC 2 CC7/CC8.
- `dex-incident-postmortems`: Sử dụng Audit Trail để tái dựng dòng thời gian sự cố.
- `dex-privacy-impact-assessment`: Lưu vết các yêu cầu truy cập và xóa dữ liệu của người dùng.

## 14. Realistic Usage Example
### Tình huống thực tế:
Một sàn giao dịch tiền mã hóa cần bảo vệ hệ thống trước nguy cơ quản trị viên nội bộ thông đồng sửa đổi số dư tài khoản. Áp dụng `dex-audit-trail-integrity`, mỗi lệnh chuyển tiền hoặc thay đổi số dư đều sinh ra một AuditEvent chứa mã băm liên kết với sự kiện trước đó. Toàn bộ sự kiện được đẩy vào S3 Object Lock Compliance Mode với thời hạn khóa 5 năm tại một AWS account bảo mật độc lập. Khi kiểm toán viên kiểm tra, hệ thống chạy script xác minh chuỗi băm 10 triệu giao dịch trong 3 phút, chứng minh không có bất kỳ bản ghi nào bị can thiệp.
