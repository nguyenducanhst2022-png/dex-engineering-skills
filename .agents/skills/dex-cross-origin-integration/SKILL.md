---
name: dex-cross-origin-integration
description: Architect secure cross-origin communication between parent applications and embedded iframes using postMessage with origin whitelisting, Content Security Policy frame-ancestors, and COOP/COEP isolation headers. Use when integrating third-party payment widgets, micro-frontend iframes, or cross-domain auth portals.
---

# dex-cross-origin-integration

## 1. Purpose & Scope
Thiết kế kiến trúc truyền thông xuyên nguồn gốc (Cross-Origin Communication) an toàn giữa ứng dụng cha và các thẻ `<iframe>` nhúng; ứng dụng phương thức `postMessage` với cơ chế kiểm tra danh sách trắng nguồn gốc (Origin Whitelisting), thiết lập chính sách bảo mật CSP `frame-ancestors` và các tiêu đề cô lập COOP/COEP ngăn ngừa tấn công Clickjacking và rò rỉ dữ liệu.

## 2. When to Use
- Khi nhúng các widget thanh toán từ cổng thanh toán bên thứ ba (như Stripe, VNPay) vào trang web.
- Khi xây dựng kiến trúc Micro-Frontend sử dụng các iframe độc lập để cô lập mã nguồn.
- Khi truyền nhận token xác thực an toàn giữa các tên miền con khác nhau (Cross-Domain Single Sign-On).

## 3. When NOT to Use
- Khi các component chạy trong cùng một ứng dụng đơn trang (Single Page App) cùng nguồn gốc (Same-Origin).
- Khi giao tiếp thông thường giữa client và server qua các API endpoints.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Kiến thức về Same-Origin Policy (SOP), API `window.postMessage`, các HTTP Headers: `Content-Security-Policy: frame-ancestors`, `Cross-Origin-Opener-Policy`.
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; tuyệt đối không can thiệp trái phép vào hệ thống của bên thứ ba.

## 5. Core Concepts & Taxonomy
- **Strict Target Origin:** Luôn chỉ định rõ domain đích khi gọi `postMessage(data, 'https://trusted.com')` thay vì dùng ký tự đại diện `'*'`.
- **Sender Origin Whitelisting:** Kiểm tra nghiêm ngặt `event.origin` trong bộ lắng nghe sự kiện trước khi phân tích cú pháp dữ liệu nhận được.
- **Frame-Ancestors Protection:** Giới hạn danh sách các tên miền được phép nhúng trang web của mình vào iframe để triệt tiêu hoàn toàn nguy cơ Clickjacking.

## 6. Step-by-Step Execution Workflow
1. Thiết lập header `Content-Security-Policy: frame-ancestors 'self' https://trusted-partner.com` trên máy chủ.
2. Tạo hợp đồng dữ liệu thông điệp (TypeScript Message Schema) cho các sự kiện truyền qua lại.
3. Gửi thông điệp từ trang cha sang iframe với tham số `targetOrigin` rõ ràng.
4. Cài đặt hàm lắng nghe `window.addEventListener('message', handler)` trên iframe có bước kiểm tra `event.origin`.
5. Kiểm thử bảo mật bằng cách thử gửi thông điệp từ một domain giả mạo để đảm bảo hệ thống từ chối xử lý.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```typescript
// Secure Cross-Origin Parent-Child Communication
const TRUSTED_ORIGIN = 'https://payments.secure-gateway.com';

// Parent sending message to iframe
export function sendPaymentInit(iframeElement: HTMLIFrameElement, orderId: string) {
  if (iframeElement.contentWindow) {
    iframeElement.contentWindow.postMessage(
      { type: 'INIT_ORDER', orderId, timestamp: Date.now() },
      TRUSTED_ORIGIN // Strict target origin, NEVER '*'
    );
  }
}

// Child iframe listening safely
window.addEventListener('message', (event: MessageEvent) => {
  if (event.origin !== 'https://ecommerce-store.com') {
    console.warn('Rejected untrusted message from origin:', event.origin);
    return;
  }
  if (event.data?.type === 'INIT_ORDER') {
    handleOrderInitialization(event.data.orderId);
  }
});
```

## 8. Anti-Patterns & Common Traps
- Gọi lệnh `postMessage(data, '*')` với ký tự đại diện, khiến bất kỳ trang web nào nhúng trộm iframe đều có thể đánh cắp payload.
- Lắng nghe sự kiện `message` mà không kiểm tra `event.origin`, mở toang cửa cho các cuộc tấn công Cross-Site Scripting (XSS).
- Sử dụng lệnh kiểm tra chuỗi lỏng lẻo như `event.origin.includes('mybrand.com')` (kẻ tấn công có thể dùng domain `mybrand.com.attacker.com`).

## 9. Quality Gates & Acceptance Criteria
- QG-01: 100% các lệnh `postMessage` đều có `targetOrigin` rõ ràng, không có bất kỳ lệnh nào dùng `'*'`. 
- QG-02: Tất cả các listener sự kiện đều kiểm tra so khớp chính xác tuyệt đối (`===`) với danh sách trắng nguồn gốc.
- QG-03: Header `frame-ancestors` được kiểm tra kích hoạt trên toàn bộ các trang nhạy cảm.

## 10. Security & Safety Boundaries
- Ngăn chặn các cuộc tấn công Clickjacking, giả mạo lệnh thanh toán và rò rỉ dữ liệu phiên làm việc xuyên nguồn gốc.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Hoạt động phân tích hoàn toàn hợp pháp, minh bạch và có sự ủy quyền chính thức từ chủ sở hữu hệ thống.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Module truyền thông hai chiều xuyên nguồn gốc `CrossOriginBridge.ts`.
1. Bộ quy tắc cấu hình tiêu đề HTTP CSP `frame-ancestors`.

## 13. Related & Complementary Skills
- [`dex-web-security-headers`](.agents/skills/dex-web-security-headers/SKILL.md)
- [`dex-api-abuse-prevention`](.agents/skills/dex-api-abuse-prevention/SKILL.md)
- [`dex-browser-extension-hardening`](.agents/skills/dex-browser-extension-hardening/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Tích hợp iframe thanh toán của ngân hàng đối tác vào trang giỏ hàng. Kỹ sư kích hoạt `dex-cross-origin-integration` để thiết lập kênh `postMessage` hai chiều có xác thực domain hai đầu khắt khe, áp dụng CSP `frame-ancestors` và ngăn chặn hoàn toàn nguy cơ kẻ xấu tạo trang giả mạo đánh cắp mã OTP của khách hàng.
