---
name: dex-browser-extension-mv3
description: Architect Manifest V3 browser extensions with non-persistent background service workers, declarativeNetRequest rules, minimal permission scopes, and cross-browser packaging (Chrome, Firefox, Edge, Safari). Use when bootstrapping extensions, migrating from Manifest V2, or passing Web Store security reviews.
---

# dex-browser-extension-mv3

## 1. Purpose & Scope
Thiết kế kiến trúc tiện ích mở rộng trình duyệt chuẩn Manifest V3 (MV3); chuyển đổi background page sang background service worker không duy trì trạng thái liên tục, thay thế blocking webRequest bằng declarativeNetRequest, thu hẹp phạm vi quyền hạn và đóng gói đa trình duyệt (Chrome, Firefox, Edge, Safari).

## 2. When to Use
- Khi khởi tạo dự án extension mới cho trình duyệt web.
- Khi di chuyển extension cũ từ Manifest V2 sang Manifest V3 theo yêu cầu của Google Chrome Web Store.
- Khi chuẩn bị hồ sơ kiểm duyệt an ninh bảo mật để xuất bản extension lên các chợ ứng dụng.

## 3. When NOT to Use
- Khi chỉ phát triển website hoặc ứng dụng web thông thường không chạy trong môi trường browser extension.
- Khi can thiệp trực tiếp vào mã nguồn C++ của engine trình duyệt Chromium/Gecko.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Tệp khai báo `manifest.json`, Node.js toolchain, hiểu biết về mô hình phân tách bối cảnh của extension (Popup, Options, Content Script, Service Worker).
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; tuyệt đối không can thiệp trái phép vào hệ thống của bên thứ ba.

## 5. Core Concepts & Taxonomy
- **Manifest V3 Security Model:** Cấm thực thi chuỗi ký tự dạng mã (No `eval()` hoặc nạp mã JavaScript từ CDN bên ngoài).
- **DeclarativeNetRequest API:** Chuyển quyền chặn và sửa đổi header mạng cho trình duyệt thực thi theo tập luật khai báo tĩnh.
- **Ephemeral Background Workers:** Service worker tự động bị đóng sau 30 giây rảnh rỗi để tiết kiệm pin và RAM.

## 6. Step-by-Step Execution Workflow
1. Đặc tả file `manifest.json` phiên bản 3 với các trường `manifest_version: 3`, `background.service_worker`.
2. Khai báo tối thiểu các quyền cần thiết (`permissions` và `host_permissions`) theo nguyên tắc đặc quyền tối thiểu.
3. Chuyển đổi các quy tắc sửa đổi header mạng sang tệp quy tắc tĩnh `rules.json` sử dụng `declarativeNetRequest`.
4. Đảm bảo toàn bộ mã JavaScript được đóng gói nội bộ trong gói cài đặt extension.
5. Đóng gói bản dựng `.zip` và kiểm tra tương thích trên Chrome, Edge và Firefox (sử dụng WebExtensions Polyfill).

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```json
{
  "manifest_version": 3,
  "name": "DEX Engineering Companion",
  "version": "1.0.0",
  "description": "Developer ergonomics and diagnostic companion extension.",
  "permissions": ["storage", "alarms", "declarativeNetRequest"],
  "host_permissions": ["https://api.dex.dev/*"],
  "background": {
    "service_worker": "background.bundle.js",
    "type": "module"
  },
  "action": {
    "default_popup": "popup.html",
    "default_icon": "icons/icon-48.png"
  }
}
```

## 8. Anti-Patterns & Common Traps
- Xin quyền rộng `*://*/*` hoặc `<all_urls>` khi chỉ cần gọi API đến một domain cụ thể, dẫn đến bị Chrome Web Store từ chối duyệt.
- Lưu biến trạng thái toàn cục trong service worker mà không lưu vào `chrome.storage`, khiến mất dữ liệu khi worker bị tắt.
- Nạp thư viện ngoài qua thẻ `<script src='https://cdn...'>` (vi phạm nghiêm trọng chính sách bảo mật CSP của MV3).

## 9. Quality Gates & Acceptance Criteria
- QG-01: File `manifest.json` vượt qua 100% tiêu chí xác thực cấu trúc của Chrome Extension Linter.
- QG-02: Không sử dụng bất kỳ hàm thực thi mã động nào (`eval`, `new Function`, `setTimeout(string)`).
- QG-03: Hoạt động trơn tru sau khi service worker bị trình duyệt buộc tắt giả lập (Terminate service worker test).

## 10. Security & Safety Boundaries
- Áp dụng Content Security Policy (CSP) nghiêm ngặt; không để lộ secret token trong các tệp nội dung extension tải xuống máy khách.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Hoạt động phân tích hoàn toàn hợp pháp, minh bạch và có sự ủy quyền chính thức từ chủ sở hữu hệ thống.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Tệp cấu hình Manifest V3 chuẩn `manifest.json`.
1. Gói đóng gói extension đa trình duyệt `extension-build.zip`.
1. Báo cáo giải trình quyền hạn phục vụ kiểm duyệt Store `PERMISSIONS_JUSTIFICATION.md`.

## 13. Related & Complementary Skills
- [`dex-browser-extension-hardening`](.agents/skills/dex-browser-extension-hardening/SKILL.md)
- [`dex-extension-message-security`](.agents/skills/dex-extension-message-security/SKILL.md)
- [`dex-extension-background-lifecycle`](.agents/skills/dex-extension-background-lifecycle/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Di chuyển tiện ích hỗ trợ nhà phát triển từ MV2 sang MV3. Sử dụng `dex-browser-extension-mv3` để thay thế background page bằng Service Worker module, chuyển đổi 8 quy tắc chặn mạng sang `declarativeNetRequest` và vượt qua vòng kiểm duyệt của Chrome Web Store trong 24 giờ.
