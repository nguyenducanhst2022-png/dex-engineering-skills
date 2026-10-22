---
name: dex-extension-content-script-isolation
description: Enforce strict DOM boundaries between untrusted host web page scripts and extension content scripts using isolated worlds, CustomEvent communication bridges, and Shadow DOM encapsulation. Use when preventing webpage DOM pollution, prototype poisoning, or XSS hijacking of extension capabilities.
---

# dex-extension-content-script-isolation

## 1. Purpose & Scope
Thiết lập ranh giới cách ly nghiêm ngặt giữa mã kịch bản của trang web đích (Main World) và Content Script của tiện ích mở rộng (Isolated World); ứng dụng Shadow DOM đóng kín (Closed Shadow DOM) để chống xung đột CSS/DOM, ngăn chặn tấn công ô nhiễm nguyên mẫu (Prototype Pollution) và bảo vệ giao diện extension không bị trang web can thiệp.

## 2. When to Use
- Khi tiện ích mở rộng cần nhúng các thành phần giao diện (UI Widgets, Buttons, Popups) trực tiếp vào trang web của bên thứ ba.
- Khi trang web đích có các kịch bản JavaScript phức tạp hoặc không đáng tin cậy có thể làm hỏng logic của extension.
- Khi cần truyền dữ liệu an toàn giữa Content Script và kịch bản trang web gốc mà không để lộ các API đặc quyền của extension.

## 3. When NOT to Use
- Khi extension chỉ hoạt động trên một cửa sổ Popup độc lập không chạm vào DOM của trang web.
- Khi trang web do chính tổ chức mình kiểm soát và có sẵn SDK tích hợp chính thức.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Kiến thức về mô hình thế giới cô lập (Isolated Worlds) trong trình duyệt, Web Components và Shadow DOM API.
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; tuyệt đối không can thiệp trái phép vào hệ thống của bên thứ ba.

## 5. Core Concepts & Taxonomy
- **Isolated World Security Boundary:** Content Script và trang web chia sẻ chung cấu trúc DOM nhưng có không gian biến JavaScript, nguyên mẫu prototype và đối tượng toàn cục `window` hoàn toàn tách biệt.
- **Closed Shadow DOM Encapsulation:** Ngăn chặn mã kịch bản của trang web đọc hoặc sửa đổi các nút DOM bên trong giao diện extension bằng `document.querySelector`.
- **Secure CustomEvent Bridge:** Truyền nhận dữ liệu qua lại giữa hai thế giới bằng các sự kiện tùy biến có làm sạch payload (Data Sanitization).

## 6. Step-by-Step Execution Workflow
1. Tạo một phần tử container mẹ trên trang web và gắn một Closed Shadow Root (`attachShadow({ mode: 'closed' })`).
2. Nhúng các kiểu dáng CSS của extension vào bên trong Shadow Root để chống ô nhiễm kiểu dáng hai chiều.
3. Xây dựng giao diện UI của extension bên trong không gian bảo vệ của Shadow DOM.
4. Thiết lập kênh liên lạc an toàn với trang web qua `CustomEvent` có kiểm tra nguồn gốc và kiểu dữ liệu.
5. Kiểm tra tính bất biến của các nguyên mẫu cốt lõi (`Array.prototype`, `Object.prototype`) trong môi trường content script.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```typescript
// Injected UI via Closed Shadow DOM
export function injectExtensionWidget() {
  const host = document.createElement('div');
  host.id = 'dex-extension-host';
  document.body.appendChild(host);

  // Closed mode prevents page script from inspecting shadowRoot
  const shadowRoot = host.attachShadow({ mode: 'closed' });

  const style = document.createElement('style');
  style.textContent = `
    :host { all: initial; position: fixed; bottom: 20px; right: 20px; z-index: 2147483647; }
    .badge { background: #1a202c; color: #fff; padding: 8px 12px; border-radius: 6px; font-family: sans-serif; }
  `;

  const widget = document.createElement('div');
  widget.className = 'badge';
  widget.textContent = 'DEX Verified';

  shadowRoot.appendChild(style);
  shadowRoot.appendChild(widget);
}
```

## 8. Anti-Patterns & Common Traps
- Chèn giao diện extension thẳng vào thẻ `<body>` mà không dùng Shadow DOM, dẫn đến CSS của trang web làm vỡ nát giao diện extension.
- Lắng nghe `window.addEventListener('message')` mà không kiểm tra cẩn thận thuộc tính `event.origin` và cấu trúc dữ liệu.
- Thực thi trực tiếp các hàm hoặc đọc các biến toàn cục mà trang web đặt sẵn trên `window` mà không xác minh tính toàn vẹn.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Giao diện extension được cô lập hoàn toàn bên trong Shadow DOM, không bị ảnh hưởng bởi CSS toàn cục của trang web.
- QG-02: Không có rò rỉ các đối tượng đặc quyền `chrome.*` sang môi trường thực thi của trang web.
- QG-03: Vượt qua các bài kiểm tra tấn công Prototype Pollution thử nghiệm.

## 10. Security & Safety Boundaries
- Không cho phép mã kịch bản độc hại của trang web can thiệp vào các nút bấm thanh toán hoặc form nhập mật khẩu của extension.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Hoạt động phân tích hoàn toàn hợp pháp, minh bạch và có sự ủy quyền chính thức từ chủ sở hữu hệ thống.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Module chèn giao diện cô lập `ShadowDOMContainer.ts`.
1. Cầu nối truyền tin an toàn giữa các thế giới `ContentScriptBridge.ts`.

## 13. Related & Complementary Skills
- [`dex-extension-message-security`](.agents/skills/dex-extension-message-security/SKILL.md)
- [`dex-browser-extension-hardening`](.agents/skills/dex-browser-extension-hardening/SKILL.md)
- [`dex-web-security-headers`](.agents/skills/dex-web-security-headers/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Phát triển tiện ích kiểm tra lỗi chính tả tự động trên web. Khi nhúng vào các trang web có CSS định nghĩa `* { color: red !important; }`, nút bấm của extension bị hỏng màu sắc. Áp dụng `dex-extension-content-script-isolation` với Closed Shadow DOM giúp nút bấm của tiện ích hiển thị hoàn hảo và bảo vệ an toàn trước các kịch bản theo dõi của trang web.
