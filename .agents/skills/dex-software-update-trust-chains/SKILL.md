---
name: dex-software-update-trust-chains
description: Architect secure software auto-update trust frameworks incorporating The Update Framework (TUF) principles, cryptographic manifest verification, downgrade attack prevention, and differential binary patches. Use when engineering auto-updaters for desktop apps or IoT devices.
---

# dex-software-update-trust-chains

## 1. Purpose & Scope
Thiết kế kiến trúc chuỗi tin cậy cập nhật phần mềm tự động (Software Update Trust Frameworks); ứng dụng các nguyên lý bảo mật của The Update Framework (TUF), thẩm định bản kê cập nhật có chữ ký điện tử (Signed Update Manifests), cơ chế chống tấn công hạ cấp phiên bản (Downgrade/Rollback Attack Prevention) và vá nhị phân vi sai (Differential Binary Patching); đảm bảo quá trình cập nhật phần mềm máy tính và thiết bị IoT diễn ra an toàn tuyệt đối.

## 2. When to Use
- Khi xây dựng cơ chế tự động cập nhật phiên bản mới (Auto-Updater) cho ứng dụng máy tính (Electron, Tauri, C++).
- Khi phát hành các bản cập nhật qua mạng (OTA Updates) cho thiết bị phần cứng nhúng.
- Khi cần bảo vệ hệ thống cập nhật không bị kẻ tấn công đánh chặn máy chủ để phát tán phiên bản chứa mã độc.

## 3. When NOT to Use
- Khi ứng dụng web được triển khai tập trung trên máy chủ (người dùng chỉ cần tải lại trang).
- Khi phát hành ứng dụng qua các kho chợ có sẵn cơ chế cập nhật như Apple App Store hay Google Play.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Đặc tả chuẩn The Update Framework (TUF), khóa ký bản kê cập nhật, công cụ tạo bản vá vi sai (bsdiff hoặc courgette).
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; bảo vệ toàn vẹn tài sản kỹ nghệ và dữ liệu sản xuất.

## 5. Core Concepts & Taxonomy
- **The Update Framework (TUF) Roles:** Phân tách trách nhiệm thành 4 vai trò độc lập: Root (Quản lý khóa), Targets (Mô tả tệp tải), Snapshot (Trạng thái phiên bản) và Timestamp (Chống tấn công phát lại).
- **Freeze Attack Prevention:** Cơ chế kiểm tra thời hạn hiệu lực của bản kê cập nhật để kẻ tấn công không thể giữ người dùng ở phiên bản cũ chứa lỗ hổng.
- **Monotonic Version Progression:** Máy khách từ chối cài đặt bất kỳ bản cập nhật nào có số phiên bản thấp hơn hoặc bằng phiên bản hiện tại để chống hạ cấp.

## 6. Step-by-Step Execution Workflow
1. Tạo tệp bản kê cập nhật `update-manifest.json` chứa số phiên bản mới, mã băm SHA-256 và kích thước tệp tải.
2. Ký điện tử lên tệp manifest bằng khóa riêng bí mật tách biệt khỏi máy chủ web phân phối.
3. Ứng dụng máy khách tải tệp manifest, xác thực chữ ký số bằng khóa công khai đã nhúng sẵn trong mã nguồn.
4. Kiểm tra số phiên bản mới phải lớn hơn phiên bản hiện tại.
5. Tải gói cập nhật, xác minh mã băm byte đối chiếu với manifest trước khi thực hiện cài đặt ghi đè.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```typescript
// Secure Update Manifest Verification Pattern
import crypto from 'crypto';

export interface UpdateManifest {
  version: string;
  minSupportedVersion: string;
  downloadUrl: string;
  sha256: string;
  publishedAt: string;
  signature: string;
}

export function verifyUpdateManifest(manifest: UpdateManifest, trustedPublicKey: string): boolean {
  const { signature, ...dataToVerify } = manifest;
  const verifier = crypto.createVerify('RSA-SHA256');
  verifier.update(JSON.stringify(dataToVerify));
  return verifier.verify(trustedPublicKey, signature, 'base64');
}
```

## 8. Anti-Patterns & Common Traps
- Tải tệp cập nhật `.exe` qua giao thức HTTP không mã hóa và thực thi thẳng mà không kiểm tra chữ ký số hoặc mã băm.
- Cho phép cài đặt phiên bản có số hiệu cũ hơn phiên bản đang chạy (mở đường cho tấn công hạ cấp để khai thác lỗ hổng cũ đã vá).
- Lưu khóa ký bản cập nhật trên cùng một máy chủ web chứa tệp tải (nếu web server bị hack, kẻ tấn công sẽ ký luôn mã độc).

## 9. Quality Gates & Acceptance Criteria
- QG-01: 100% các bản cập nhật bắt buộc phải có manifest được ký số và mã băm SHA-256 trùng khớp từng byte.
- QG-02: Chặn đứng hoàn toàn mọi nỗ lực hạ cấp phiên bản (Downgrade rejection test đạt 100%).
- QG-03: Cơ chế cập nhật tự động rollback an toàn nếu quá trình cài đặt phiên bản mới gặp sự cố.

## 10. Security & Safety Boundaries
- Khóa gốc (Root Key) của hệ thống cập nhật phải được lưu trữ ngoại tuyến hoàn toàn (Offline Cold Storage) trong két sắt an toàn.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Module xác thực cập nhật an toàn `SecureUpdateManager.ts`.
1. Đặc tả kiến trúc cập nhật phần mềm chuẩn TUF `UPDATE_TRUST_FRAMEWORK.md`.

## 13. Related & Complementary Skills
- [`dex-code-signing-release-process`](.agents/skills/dex-code-signing-release-process/SKILL.md)
- [`dex-artifact-signature-verification`](.agents/skills/dex-artifact-signature-verification/SKILL.md)
- [`dex-vulnerability-disclosure-workflows`](.agents/skills/dex-vulnerability-disclosure-workflows/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Xây dựng hệ thống tự động cập nhật cho ứng dụng ví tiền mã hóa desktop. Kỹ sư kích hoạt `dex-software-update-trust-chains`, triển khai kiến trúc TUF với khóa ký offline và xác thực kép SHA-256, ngăn chặn hoàn toàn nguy cơ kẻ tấn công hack vào máy chủ DNS để chuyển hướng người dùng tải về bản cập nhật giả mạo đánh cắp tiền.
