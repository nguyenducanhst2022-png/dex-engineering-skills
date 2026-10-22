---
name: dex-secret-rotation-drills
description: Design zero-downtime secret rotation drills for database credentials, API signing keys, JWT secrets, and TLS certificates using dual-key overlaps and automated validation. Use when validating security incident readiness or meeting regulatory compliance mandates.
---

# dex-secret-rotation-drills

## 1. Purpose & Scope
Thiết kế và diễn tập quy trình quay vòng khóa bí mật không gián đoạn dịch vụ (Zero-Downtime Secret Rotation Drills) cho thông tin đăng nhập cơ sở dữ liệu, khóa ký API, mã bí mật JWT và chứng chỉ số TLS; ứng dụng mô hình gối đầu hai khóa (Dual-Key Overlap), kiểm tra xác thực tự động và cơ chế hoàn tác khẩn cấp; phục vụ nâng cao năng lực ứng phó sự cố rò rỉ khóa và đáp ứng các tiêu chuẩn tuân thủ SOC 2, PCI-DSS.

## 2. When to Use
- Khi thực hiện diễn tập quay vòng khóa bảo mật định kỳ (hàng quý) theo yêu cầu của kiểm toán bảo mật.
- Khi nghi ngờ một khóa API của bên thứ ba hoặc mật khẩu cơ sở dữ liệu bị lộ ra ngoài.
- Trước khi hết hạn chứng chỉ số TLS hoặc khóa ký mã nguồn.

## 3. When NOT to Use
- Khi tạo khóa mới lần đầu cho một hệ thống chưa bao giờ chạy trên môi trường thực tế.
- Khi chỉ thay đổi mật khẩu tài khoản người dùng cá nhân.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Hệ thống quản lý bí mật (AWS Secrets Manager, HashiCorp Vault hoặc GCP Secret Manager), quyền truy cập cấu hình dịch vụ.
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; bảo vệ toàn vẹn tài sản kỹ nghệ và dữ liệu sản xuất.

## 5. Core Concepts & Taxonomy
- **Dual-Secret Grace Period:** Trong giai đoạn chuyển tiếp, hệ thống hỗ trợ đồng thời cả khóa cũ và khóa mới (chấp nhận xác thực bằng cả 2 khóa) để các máy khách có thời gian cập nhật.
- **Zero-Downtime Database Rotation:** Tạo tài khoản database thứ hai với mật khẩu mới, cập nhật chuỗi kết nối ứng dụng, kiểm tra kết nối thành công rồi mới vô hiệu hóa tài khoản cũ.
- **Automated Canary Validation:** Gửi request thử nghiệm có chữ ký của khóa mới trước khi chính thức hủy bỏ khóa cũ.

## 6. Step-by-Step Execution Workflow
1. Tạo khóa bí mật mới (Secret B) trong hệ thống Secret Manager.
2. Cập nhật máy chủ xác thực để chấp nhận cả Secret A (cũ) và Secret B (mới).
3. Triển khai Secret B tới các ứng dụng máy khách để bắt đầu sử dụng khóa mới để ký request.
4. Theo dõi nhật ký kiểm toán trong 24 giờ cho đến khi 100% lưu lượng chuyển sang Secret B.
5. Vô hiệu hóa và xóa bỏ hoàn toàn Secret A cũ khỏi hệ thống.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```typescript
// Dual-Key JWT Verification Supporting Zero-Downtime Rotation
import jwt from 'jsonwebtoken';

const ACTIVE_KEYS = {
  'key-2026-v2': process.env.JWT_SECRET_PRIMARY,   // New Key
  'key-2025-v1': process.env.JWT_SECRET_SECONDARY, // Old Key (Grace Period)
};

export function verifyTokenWithRotation(token: string): any {
  const decodedHeader = jwt.decode(token, { complete: true })?.header;
  const keyId = decodedHeader?.kid || 'key-2025-v1';
  const secret = ACTIVE_KEYS[keyId as keyof typeof ACTIVE_KEYS];

  if (!secret) {
    throw new Error('Invalid or expired key identifier');
  }

  return jwt.verify(token, secret);
}
```

## 8. Anti-Patterns & Common Traps
- Đổi mật khẩu cơ sở dữ liệu ngay lập tức trên máy chủ mà không cập nhật trước cho ứng dụng, làm sập toàn bộ hệ thống ngay trong giây tiếp theo.
- Đổi khóa bí mật mà không có kế hoạch dự phòng (Rollback Plan) khi phát sinh lỗi không tương thích.
- Quay vòng khóa bằng tay thủ công qua giao diện web, dễ gõ nhầm ký tự và không thể tự động hóa.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Quá trình quay vòng khóa diễn ra đạt 100% Zero-Downtime, không có bất kỳ request hợp lệ nào bị lỗi 401/500.
- QG-02: Khóa cũ được thu hồi và xóa bỏ hoàn toàn sau khi giai đoạn gối đầu kết thúc.
- QG-03: Diễn tập quay vòng khóa được ghi lại đầy đủ bằng biên bản kiểm toán có đóng dấu thời gian.

## 10. Security & Safety Boundaries
- Không bao giờ gửi khóa bí mật qua các kênh liên lạc không an toàn (Slack, Email); chỉ truyền tải qua hệ thống Secret Manager có mã hóa.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Kịch bản diễn tập quay vòng khóa tự động `secret-rotation-drill.sh`.
1. Biên bản nghiệm thu diễn tập quay vòng khóa `SECRET_ROTATION_REPORT.md`.

## 13. Related & Complementary Skills
- [`dex-crypto-key-rotation-kms`](.agents/skills/dex-crypto-key-rotation-kms/SKILL.md)
- [`dex-secrets-management`](.agents/skills/dex-secrets-management/SKILL.md)
- [`dex-security-audit`](.agents/skills/dex-security-audit/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Doanh nghiệp tổ chức diễn tập ứng phó sự cố rò rỉ khóa JWT bí mật phục vụ kiểm toán SOC 2 Type II. Kỹ sư kích hoạt `dex-secret-rotation-drills`, áp dụng cơ chế xác thực gối đầu hai khóa `kid` trong 24 giờ, luân chuyển khóa mới cho 500,000 phiên đăng nhập mà không làm bất kỳ người dùng nào bị văng ra khỏi ứng dụng, hoàn thành diễn tập đạt điểm xuất sắc.
