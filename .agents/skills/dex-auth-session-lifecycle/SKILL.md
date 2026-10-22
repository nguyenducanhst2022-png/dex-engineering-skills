---
name: dex-auth-session-lifecycle
description: Implement robust authentication and session lifecycle management, JWT issuance and validation, refresh token rotation, revocation blacklists, CSRF/CORS defenses, and session hijacking mitigations. Use when securing user authentication, login flows, or session states.
---

# dex-auth-session-lifecycle

## 1. Purpose & Scope
Hiện thực hóa toàn bộ vòng đời xác thực người dùng và quản lý phiên làm việc (Auth & Session Lifecycle); xây dựng cơ chế cấp phát và kiểm tra JSON Web Tokens (JWT), xoay vòng refresh token an toàn (Refresh Token Rotation), danh sách thu hồi phiên (Revocation Blacklists / Redis Sessions), phòng chống tấn công CSRF, cấu hình CORS chuẩn xác và ngăn chặn đánh cắp phiên (Session Hijacking).

## 2. When to Use
- Khi xây dựng luồng Đăng nhập, Đăng ký, Đăng xuất và Làm mới phiên (Token Refresh).
- Khi hệ thống lưu access token không an toàn trong `localStorage` dẫn đến nguy cơ bị đánh cắp qua tấn công XSS.
- Khi người dùng đổi mật khẩu nhưng các phiên đăng nhập cũ trên thiết bị khác vẫn không bị đăng xuất.

## 3. When NOT to Use
- Phân quyền dựa trên vai trò hoặc quyền hạn người dùng (dùng `dex-access-control-tenancy`).
- Xác thực giữa các microservices nội bộ bằng mTLS (dùng `dex-security-audit`).

## 4. Prerequisites & Input Context
**Đầu vào cần thiết:**
- Cơ chế xác thực (OAuth2 Authorization Code Flow with PKCE, OpenID Connect, Session-based, Stateless JWT).
- Thuộc tính phiên: Thời hạn sống của Access Token (ví dụ: 15 phút), Refresh Token (ví dụ: 7 ngày).
- Kho lưu trữ trạng thái phiên (Redis cluster, PostgreSQL session table).

**Điều kiện tiên quyết:**
- Đã thiết lập HTTPS/TLS bắt buộc cho toàn bộ endpoint xác thực.
- Khóa bí mật ký token (JWT Secret hoặc RSA/ECDSA Private Key) được quản lý an toàn.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**: Nắm vững cơ chế vận hành theo chuẩn Agent Skills, tuân thủ nghiêm ngặt tính xác định và ranh giới trách nhiệm.
- **Quy tắc quyết định kỹ thuật**:
- **Tuyệt Đối Không Lưu Access/Refresh Token Trong LocalStorage**: Lưu token trong localStorage khiến ứng dụng dễ dàng bị mất tài khoản nếu dính mã độc XSS; bắt buộc dùng HttpOnly Cookies.
- **Access Token Phải Có Hạn Ngắn**: Thời hạn sống của Access Token tối đa không quá 15 phút để giảm thiểu thiệt hại nếu token bị rò rỉ.
- **Thu Hồi Phiên Khi Đổi Mật Khẩu**: Khi người dùng thay đổi mật khẩu hoặc bật 2FA, bắt buộc phải hủy toàn bộ các phiên làm việc hiện có ngoại trừ phiên hiện tại.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Lỗ hổng tấn công phát lại (Replay Attack)**: Kẻ gian đánh cắp Refresh Token cũ và dùng để lấy token mới -> Khắc phục: Triển khai Token Rotation và phát hiện tái sử dụng, lập tức khóa tài khoản khi phát hiện token cũ được nộp lại.
- **CSRF làm người dùng tự động chuyển tiền**: Do dùng cookie không có `SameSite` -> Khắc phục: Thiết lập `SameSite=Lax` hoặc `Strict` và kiểm tra header `Origin` / `Referer`.

## 6. Step-by-Step Execution Workflow
1. Thiết kế mô hình Token kép: Access Token ngắn hạn (15 phút, stateless) và Refresh Token dài hạn (7 ngày, stateful lưu trong database/Redis).
2. Lưu trữ Refresh Token trong Cookie an toàn (`httpOnly`, `Secure`, `SameSite=Strict`, `Path=/api/auth/refresh`).
3. Triển khai cơ chế Xoay vòng Refresh Token (Refresh Token Rotation): Mỗi khi dùng Refresh Token để lấy Access Token mới, lập tức hủy Refresh Token cũ và cấp Refresh Token mới.
4. Phát hiện tái sử dụng Token (Token Reuse Detection): Nếu một Refresh Token cũ đã bị thu hồi mà lại được gửi lên, lập tức vô hiệu hóa toàn bộ chuỗi token của người dùng đó (nghi ngờ bị đánh cắp).
5. Hiện thực hóa chức năng Đăng xuất khỏi mọi thiết bị (Global Sign-out): Xóa toàn bộ token của người dùng trong Redis blacklist.
6. Triển khai biện pháp chống CSRF: Áp dụng Double Submit Cookie hoặc Anti-CSRF Token cho các yêu cầu biến đổi trạng thái.

## 7. Concrete Examples
### Ví dụ triển khai chuẩn mực:
```typescript
// auth.service.ts - Refresh token rotation & reuse detection
export async function refreshSession(oldRefreshToken: string) {
  const tokenRecord = await db.refreshToken.findUnique({ where: { token: hashToken(oldRefreshToken) } });
  if (!tokenRecord) {
    // Suspected token reuse! Revoke all tokens for this user
    const compromisedUserId = decodeTokenSubject(oldRefreshToken);
    await db.refreshToken.deleteMany({ where: { userId: compromisedUserId } });
    throw new SecurityException('Compromised session detected. All sessions revoked.');
  }
  // Invalidate old token and issue new pair
  await db.refreshToken.delete({ where: { id: tokenRecord.id } });
  return issueNewTokenPair(tokenRecord.userId);
}
```

### Lệnh xác minh & thực thi:
- Kiểm tra thuộc tính Cookie trả về: `curl -i -X POST https://api.dex.dev/auth/login` (tìm `HttpOnly; Secure; SameSite=Strict`)
- Kiểm tra giải mã JWT: `jwt decode <token>`
- Chạy bài kiểm thử luồng xoay vòng token: `npm run test:auth-lifecycle`

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước kiểm tra biên và giả định hệ thống luôn ở trạng thái lý tưởng.
- **Anti-Pattern 2**: Không ghi nhận nhật ký kiểm toán hoặc bỏ qua việc xử lý ngoại lệ lúc runtime.
- **Trap**: Bỏ qua các rào chắn an toàn hoặc cố tình chạy script không qua kiểm thử tự động.

## 9. Quality Gates & Acceptance Criteria
- QG-03: Triển khai thành công luồng Token Rotation và phát hiện tái sử dụng Refresh Token.
- QG-09: Toàn bộ cookie xác thực được bảo vệ bởi cờ `HttpOnly`, `Secure`, và `SameSite`.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động trước khi coi là hoàn thành.

## 10. Security & Safety Boundaries
- Ký JWT bằng thuật toán bất đối xứng mạnh (Ed25519 hoặc RS256); tuyệt đối cấm sử dụng thuật toán `none` hoặc dùng khóa đối xứng yếu.
- Không bao giờ thực thi mã nguồn hoặc thay đổi cấu hình trên môi trường sản xuất mà thiếu cơ chế rollback an toàn.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Có thể kích hoạt trực tiếp từ terminal hoặc extension tương thích trong VS Code / Cursor / Windsurf.

## 12. Deliverables & Output Artifacts
- Module xử lý xác thực và quản lý vòng đời phiên (`auth.service.ts`).
- Middleware kiểm tra và làm mới token tự động (`auth.middleware.ts`).
- Bộ kiểm thử E2E xác minh các kịch bản đánh cắp và thu hồi phiên.

## 13. Related & Complementary Skills
- `dex-development-workflow`: Quy trình phát triển tiêu chuẩn.
- `dex-code-verification`: Xác minh chất lượng và tính đúng đắn của mã nguồn.
- `dex-master-orchestrator`: Bộ điều phối trung tâm kết nối kỹ năng này với các kỹ năng khác trong hệ thống.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư hoặc AI Agent tiếp nhận yêu cầu liên quan đến **dex-auth-session-lifecycle**.
1. Đọc kỹ đầu vào và các ràng buộc kỹ thuật tại mục 4.
2. Thực thi tuần tự 6 bước trong Workflow tại mục 6.
3. Chạy các lệnh kiểm chứng tại mục 7 và đối chiếu với Quality Gates tại mục 9.
4. Đóng gói deliverables theo danh sách tại mục 12 và báo cáo kết quả kèm bằng chứng xác thực.
