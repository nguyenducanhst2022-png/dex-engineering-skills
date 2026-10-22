---
name: dex-oauth-oidc-integration
description: Architect secure OAuth 2.1 and OpenID Connect (OIDC) client implementations with Authorization Code Flow + PKCE, state/nonce validation, token refresh rotation, and distributed session revocation. Use when building SSO enterprise integrations, third-party API clients, or federated authentication portals.
---

# dex-oauth-oidc-integration

## 1. Purpose & Scope
Thiết kế kiến trúc máy khách xác thực và ủy quyền chuẩn OAuth 2.1 và OpenID Connect (OIDC); ứng dụng luồng mã ủy quyền kèm khóa hoán vị mã hóa (Authorization Code Flow with PKCE), xác thực tham số trạng thái chống giả mạo (`state`, `nonce`), cơ chế quay vòng và thu hồi mã thông báo (Refresh Token Rotation) và quản trị phiên đăng nhập một lần (SSO) phân tán.

## 2. When to Use
- Khi tích hợp tính năng đăng nhập bằng tài khoản Google, Microsoft Entra ID hoặc Okta cho hệ thống doanh nghiệp.
- Khi xây dựng ứng dụng máy khách gọi API của bên thứ ba cần bảo vệ an toàn cho token xác thực.
- Khi nâng cấp hệ thống xác thực cũ lên chuẩn an ninh hiện đại nhất OAuth 2.1 (loại bỏ hoàn toàn luồng Implicit Flow).

## 3. When NOT to Use
- Khi chỉ cần xác thực giữa hai máy chủ nội bộ với nhau trong cùng mạng an toàn (nên dùng mTLS hoặc Client Credentials).
- Khi ứng dụng độc lập không có người dùng và không cần ủy quyền quyền hạn.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** OAuth 2.1/OIDC Provider (Keycloak, Auth0 hoặc Google Cloud Identity), cặp khóa client ID/secret, thư viện client OIDC chuẩn (`openid-client`).
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; tuân thủ nghiêm ngặt các ranh giới bảo mật và an toàn dữ liệu.

## 5. Core Concepts & Taxonomy
- **PKCE (Proof Key for Code Exchange):** Tạo mã xác minh `code_verifier` ngẫu nhiên và mã băm `code_challenge` SHA-256 để chống đánh chặn mã code trên đường truyền.
- **State & Nonce Validation:** Ngăn chặn tấn công giả mạo yêu cầu chéo trang (CSRF) và tấn công phát lại (Replay Attacks) đối với ID Token.
- **Refresh Token Rotation:** Mỗi lần đổi Access Token mới, máy chủ sẽ hủy Refresh Token cũ và cấp một Refresh Token mới; nếu Refresh Token cũ bị dùng lại, lập tức thu hồi toàn bộ phiên.

## 6. Step-by-Step Execution Workflow
1. Khởi tạo chuỗi ngẫu nhiên `code_verifier` và tính toán `code_challenge` bằng mã băm SHA-256.
2. Tạo chuỗi ngẫu nhiên `state` và `nonce`, lưu vào phiên an toàn của trình duyệt (HttpOnly Cookie).
3. Chuyển hướng người dùng đến URL đăng nhập của nhà cung cấp danh tính với đầy đủ tham số PKCE.
4. Tại callback endpoint, xác minh tính khớp của `state`, gửi `code_verifier` để đổi lấy bộ token.
5. Giải mã và thẩm định chữ ký số của `id_token` bằng bảng khóa công khai JWKS của nhà cung cấp.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```typescript
import { generators, Issuer } from 'openid-client';

export async function initiateOauthFlow(req: any, res: any) {
  const codeVerifier = generators.codeVerifier();
  const codeChallenge = generators.codeChallenge(codeVerifier);
  const state = generators.state();
  const nonce = generators.nonce();

  // Store in secure encrypted session cookie
  req.session.oauthData = { codeVerifier, state, nonce };

  const authUrl = client.authorizationUrl({
    scope: 'openid email profile',
    state,
    nonce,
    code_challenge: codeChallenge,
    code_challenge_method: 'S256',
  });

  res.redirect(authUrl);
}
```

## 8. Anti-Patterns & Common Traps
- Sử dụng luồng Implicit Grant (trả thẳng token qua URL fragment `#access_token=...`), khiến token bị lưu vào lịch sử trình duyệt và dễ bị đánh cắp.
- Không kiểm tra tham số `state` tại callback endpoint, mở đường cho cuộc tấn công Login CSRF.
- Lưu trữ Access Token và Refresh Token trong `localStorage` của trình duyệt thay vì lưu trong cookie bảo mật `HttpOnly, Secure, SameSite=Lax`.

## 9. Quality Gates & Acceptance Criteria
- QG-01: 100% các luồng đăng nhập bắt buộc sử dụng Authorization Code kèm PKCE S256.
- QG-02: Tham số `state` và `nonce` được xác thực nghiêm ngặt và hủy bỏ ngay sau lần sử dụng đầu tiên.
- QG-03: Triển khai thành công cơ chế Refresh Token Rotation với tính năng tự động khóa phiên khi phát hiện token cũ bị tái sử dụng.

## 10. Security & Safety Boundaries
- Không bao giờ để lộ Client Secret trong mã nguồn frontend; luôn lưu trữ token trong cookie HttpOnly để triệt tiêu nguy cơ bị đánh cắp qua tấn công XSS.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Module tích hợp đăng nhập OIDC bảo mật `OidcAuthManager.ts`.
1. Bộ quy tắc thẩm định mã thông báo JWT và kiểm tra JWKS.

## 13. Related & Complementary Skills
- [`dex-security-audit`](.agents/skills/dex-security-audit/SKILL.md)
- [`dex-access-control-tenancy`](.agents/skills/dex-access-control-tenancy/SKILL.md)
- [`dex-secrets-management`](.agents/skills/dex-secrets-management/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Xây dựng cổng đăng nhập SSO cho nhân viên tập đoàn liên kết với Microsoft Azure AD. Kỹ sư kích hoạt `dex-oauth-oidc-integration`, thiết lập luồng PKCE chuẩn OAuth 2.1, xác thực chữ ký số qua JWKS tự động và lưu token trong cookie HttpOnly, đạt điểm tuyệt đối trong đợt kiểm toán an ninh nội bộ.
