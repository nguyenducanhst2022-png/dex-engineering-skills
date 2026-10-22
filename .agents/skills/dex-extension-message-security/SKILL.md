---
name: dex-extension-message-security
description: Secure asynchronous message channels between content scripts, popup UIs, devtools panels, and background service workers with strict sender origin validation and typed schemas. Use when preventing unauthorized message spoofing, privilege escalation, or cross-tab token interception.
---

# dex-extension-message-security

## 1. Purpose & Scope
Bảo vệ các kênh truyền thông điệp bất đồng bộ (Message Passing Channels) giữa Content Scripts, Popup UI, Devtools Panels và Background Service Worker; thiết lập cơ chế xác thực nguồn gửi (Sender Origin Validation), kiểm tra định kiểu dữ liệu (Typed Schemas) và ngăn chặn tấn công leo thang đặc quyền từ website chứa mã độc.

## 2. When to Use
- Khi xây dựng luồng truyền tin nội bộ trong browser extension.
- Khi extension giao tiếp với các trang web công khai qua `externally_connectable` hoặc `window.postMessage`.
- Khi xử lý các hành động nhạy cảm (như đọc token, gọi API đặc quyền) từ yêu cầu của Content Script.

## 3. When NOT to Use
- Khi chỉ truyền dữ liệu nội bộ giữa các hàm trong cùng một file script.
- Khi giao tiếp giữa client và server thông thường qua REST API hoặc WebSocket.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Kiến thức về các API `chrome.runtime.sendMessage`, `chrome.tabs.sendMessage`, `chrome.runtime.onMessageExternal`.
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; tuyệt đối không can thiệp trái phép vào hệ thống của bên thứ ba.

## 5. Core Concepts & Taxonomy
- **Sender Origin Verification:** Luôn kiểm tra `sender.id === chrome.runtime.id` và `sender.tab.url` trước khi thực thi lệnh.
- **Type-Safe RPC Messaging:** Định nghĩa hợp đồng thông điệp phân biệt (Discriminated Unions) để phân tích payload an toàn.
- **Privilege Separation:** Không bao giờ cho phép Content Script trực tiếp yêu cầu Service Worker thực thi các thao tác tùy tiện (Arbitrary Execution).

## 6. Step-by-Step Execution Workflow
1. Định nghĩa kiểu dữ liệu thông điệp bằng TypeScript (gồm trường `action`, `payload`, `timestamp`).
2. Cài đặt hàm lắng nghe `chrome.runtime.onMessage.addListener` trong background service worker.
3. Thực hiện kiểm tra tính hợp lệ của nguồn gửi (`sender.origin`, `sender.id`).
4. Sử dụng bộ xác thực schema (như Zod) để kiểm tra payload trước khi xử lý nghiệp vụ.
5. Trả lời kết quả qua callback `sendResponse` bất đồng bộ (`return true;`).

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```typescript
// Secure Extension Message Handler
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  // 1. Verify internal extension origin
  if (sender.id !== chrome.runtime.id) {
    console.error('Unauthorized message sender:', sender);
    sendResponse({ success: false, error: 'Forbidden' });
    return false;
  }

  // 2. Route typed action safely
  switch (message.type) {
    case 'FETCH_USER_TELEMETRY':
      handleTelemetry(message.payload).then(data => sendResponse({ success: true, data }));
      return true; // Keep message channel open for async response
    default:
      sendResponse({ success: false, error: 'Unknown message action' });
      return false;
  }
});
```

## 8. Anti-Patterns & Common Traps
- Tin tưởng tuyệt đối nội dung thông điệp gửi từ Content Script mà không kiểm tra URL nguồn (Content Script có thể bị tấn công XSS từ trang web).
- Thực thi trực tiếp mã JavaScript hoặc lệnh SQL nhận được qua message payload.
- Để mở quyền `externally_connectable: ["<all_urls>"]` mà không có danh sách whitelist tên miền được phép giao tiếp.

## 9. Quality Gates & Acceptance Criteria
- QG-01: 100% các message handler có bước xác minh `sender.id` ngay dòng đầu tiên.
- QG-02: Tất cả các thông điệp truyền nhận đều tuân thủ hợp đồng TypeScript Interface đã quy định.
- QG-03: Bộ test kiểm thử xâm nhập xác nhận việc gửi thông điệp giả mạo từ trang web khác bị chặn hoàn toàn.

## 10. Security & Safety Boundaries
- Ngăn chặn các trang web độc hại mạo danh extension để thực hiện các thao tác quản trị hoặc đánh cắp session token.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Hoạt động phân tích hoàn toàn hợp pháp, minh bạch và có sự ủy quyền chính thức từ chủ sở hữu hệ thống.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Hợp đồng giao tiếp an toàn `extension-message-contracts.ts`.
1. Bộ định tuyến thông điệp có xác thực `SecureMessageRouter.ts`.

## 13. Related & Complementary Skills
- [`dex-browser-extension-mv3`](.agents/skills/dex-browser-extension-mv3/SKILL.md)
- [`dex-extension-content-script-isolation`](.agents/skills/dex-extension-content-script-isolation/SKILL.md)
- [`dex-api-abuse-prevention`](.agents/skills/dex-api-abuse-prevention/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Kiểm toán extension quản lý mật khẩu doanh nghiệp. Phát hiện lỗi Content Script nhận tin nhắn từ bất kỳ website nào và chuyển tiếp thẳng vào Service Worker. Áp dụng `dex-extension-message-security` để thêm lớp kiểm tra nguồn gốc khắt khe và schema validation, ngăn chặn triệt để nguy cơ website đánh cắp thông tin tài khoản.
