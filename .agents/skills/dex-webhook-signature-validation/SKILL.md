---
name: dex-webhook-signature-validation
description: Implement robust webhook ingestion endpoints with HMAC-SHA256 signature verification, replay attack prevention using timestamp tolerances, raw body preservation, and dead-letter queue routing. Use when receiving event notifications from Stripe, GitHub, Shopify, or external SaaS providers.
---

# dex-webhook-signature-validation

## 1. Purpose & Scope
Hiện thực hóa các điểm tiếp nhận sự kiện Webhook (Webhook Ingestion Endpoints) an toàn và kiên cường; xác minh chữ ký điện tử HMAC-SHA256, ngăn chặn tấn công phát lại (Replay Attacks) bằng cửa sổ dung sai thời gian (Timestamp Tolerance), bảo toàn nguyên vẹn chuỗi byte phần thân thô (Raw Body Preservation) và định tuyến xử lý lỗi qua hàng đợi chết (Dead-Letter Queue).

## 2. When to Use
- Khi xây dựng endpoint tiếp nhận thông báo thanh toán thành công từ cổng thanh toán (Stripe, VNPay, PayPal).
- Khi tích hợp webhook nhận thông báo commit từ GitHub hoặc đơn hàng mới từ Shopify.
- Khi cần bảo vệ máy chủ không bị kẻ xấu gửi các gói tin webhook giả mạo để gian lận giao dịch.

## 3. When NOT to Use
- Khi xây dựng API gửi dữ liệu đi ra bên ngoài cho khách hàng (Outgoing Webhooks).
- Khi giao tiếp nội bộ giữa các microservices qua kết nối tin cậy có mTLS.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Khóa bí mật Webhook Secret chia sẻ giữa hai bên, kiến thức về thuật toán mã hóa băm HMAC (Hash-based Message Authentication Code).
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; tuân thủ nghiêm ngặt các ranh giới bảo mật và an toàn dữ liệu.

## 5. Core Concepts & Taxonomy
- **Raw Body Immutability:** Bắt buộc phải tính toán chữ ký HMAC trên chuỗi byte thô ban đầu nhận được từ mạng trước khi qua bất kỳ bộ parse JSON nào.
- **Timestamp Drift Window:** Từ chối các gói tin có dấu thời gian sai lệch quá 5 phút so với đồng hồ máy chủ để triệt tiêu tấn công bắt gói tin phát lại.
- **Constant-Time Comparison:** Sử dụng hàm so sánh an toàn `crypto.timingSafeEqual` để ngăn chặn tấn công dò khóa bằng độ trễ thời gian (Timing Attack).

## 6. Step-by-Step Execution Workflow
1. Cấu hình middleware web server giữ nguyên chuỗi `req.rawBody` ở dạng Buffer.
2. Trích xuất chữ ký và dấu thời gian từ header HTTP (ví dụ `Stripe-Signature: t=1600000000,v1=abc...`).
3. Kiểm tra xem dấu thời gian `t` có nằm trong ngưỡng dung sai cho phép (±300 giây) hay không.
4. Tính toán mã băm HMAC-SHA256 từ chuỗi kết hợp `t + '.' + rawBody` bằng khóa bí mật `webhook_secret`.
5. So sánh mã băm vừa tính với chữ ký nhận được bằng hàm so sánh thời gian bất biến `timingSafeEqual`.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```typescript
import crypto from 'crypto';

export function verifyWebhookSignature(rawBody: Buffer, signatureHeader: string, secret: string, toleranceSeconds = 300): boolean {
  const parts = Object.fromEntries(signatureHeader.split(',').map(item => item.split('=')));
  const timestamp = parseInt(parts.t, 10);
  const signature = parts.v1;

  // 1. Replay attack prevention
  const now = Math.floor(Date.now() / 1000);
  if (Math.abs(now - timestamp) > toleranceSeconds) {
    return false;
  }

  // 2. Compute expected HMAC
  const payloadToSign = `${timestamp}.${rawBody.toString('utf-8')}`;
  const expectedSignature = crypto.createHmac('sha256', secret).update(payloadToSign).digest('hex');

  // 3. Constant-time comparison
  const expectedBuf = Buffer.from(expectedSignature, 'utf-8');
  const actualBuf = Buffer.from(signature, 'utf-8');
  
  return expectedBuf.length === actualBuf.length && crypto.timingSafeEqual(expectedBuf, actualBuf);
}
```

## 8. Anti-Patterns & Common Traps
- Parse JSON phần thân thành object rồi dùng `JSON.stringify()` để tính chữ ký (thứ tự các key bị thay đổi sẽ làm sai lệch mã băm HMAC).
- Dùng toán tử so sánh thông thường `===` để kiểm tra chữ ký, khiến hệ thống có nguy cơ bị tấn công Timing Attack dò từng ký tự của chữ ký.
- Bỏ qua bước kiểm tra dấu thời gian khiến kẻ tấn công có thể bắt gói tin thanh toán cũ và phát lại nhiều lần để cộng tiền tài khoản.

## 9. Quality Gates & Acceptance Criteria
- QG-01: 100% các request webhook đến đều được xác thực chữ ký thành công trước khi xử lý logic nghiệp vụ.
- QG-02: Toàn bộ quá trình so sánh chữ ký sử dụng thuật toán thời gian bất biến `timingSafeEqual`.
- QG-03: Các webhook bị lỗi hoặc không thể xử lý được tự động chuyển hướng vào hàng đợi Dead-Letter Queue (DLQ).

## 10. Security & Safety Boundaries
- Khóa bí mật Webhook Secret phải được bảo vệ nghiêm ngặt trong Secret Manager; lập tức thay thế khóa khi có nghi ngờ rò rỉ.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Middleware xác thực chữ ký Webhook an toàn `verifyWebhookMiddleware.ts`.
1. Bộ test tự động kiểm thử các kịch bản tấn công giả mạo chữ ký và phát lại gói tin.

## 13. Related & Complementary Skills
- [`dex-api-abuse-prevention`](.agents/skills/dex-api-abuse-prevention/SKILL.md)
- [`dex-idempotent-operations`](.agents/skills/dex-idempotent-operations/SKILL.md)
- [`dex-security-audit`](.agents/skills/dex-security-audit/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Trang thương mại điện tử bị hacker lợi dụng lỗ hổng webhook để tạo đơn hàng thành công giả mạo. Kỹ sư kích hoạt `dex-webhook-signature-validation`, tái cấu trúc endpoint tiếp nhận với bước kiểm tra raw body HMAC-SHA256 và chặn cửa sổ thời gian 5 phút, loại bỏ hoàn toàn 100% các yêu cầu giả mạo từ bên ngoài.
