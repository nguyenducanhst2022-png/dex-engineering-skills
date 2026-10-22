---
name: dex-browser-extension-hardening
description: Harden browser extensions across Manifest V3, content script isolation, cross-origin communication, and CSP to prevent token theft and malicious page injection. Use when building or auditing Chromium/Firefox extensions.
---

# dex-browser-extension-hardening

## 1. Purpose & Scope
Gia cố, bảo mật và kiểm toán các tiện ích mở rộng trình duyệt (Browser Extension Hardening: Manifest V3 cho Chrome/Edge/Firefox); thiết lập cơ chế cô lập Content Script, bảo vệ kênh truyền tin nội bộ (Cross-origin Message Passing), ngăn chặn việc bị trang web độc hại tấn công ngược (Web-to-Extension Exploits) và chống đánh cắp khóa API/Token nhạy cảm.

## 2. When to Use
- Phát triển tiện ích mở rộng trình duyệt có tương tác với ví tiền điện tử, mật khẩu hoặc dữ liệu công việc nội bộ.
- Nâng cấp extension từ Manifest V2 lên Manifest V3 theo quy định bắt buộc của Google Web Store.
- Chuẩn bị đánh giá bảo mật trước khi submit extension lên Chrome/Firefox Add-ons Store.

## 3. When NOT to Use
- Không sử dụng quyền truy cập toàn bộ các trang web (`<all_urls>` hoặc `*://*/*`) nếu extension chỉ cần hoạt động trên một số trang web chỉ định.
- Không lưu trữ Secret API Keys vĩnh viễn trong mã nguồn JavaScript của extension (người dùng có thể bóc tách dễ dàng).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- File cấu hình `manifest.json` (Manifest V3).
- Mã nguồn Background Service Worker, Content Scripts và Popup.
- Danh sách các quyền (Permissions) được yêu cầu.
- **Điều kiện tiên quyết**:
- Extension được viết tuân thủ hoàn toàn tiêu chuẩn Manifest V3 (không sử dụng `eval`, không nạp script từ xa qua mạng).

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Manifest V3 Security Paradigms:
  + Không cho phép chạy Remote Code: 100% mã nguồn JavaScript phải được đóng gói sẵn trong package của extension, ngăn chặn việc tải mã độc từ máy chủ điều khiển ngầm.
  + Background Service Workers thay thế Background Pages: Service worker chỉ chạy khi có sự kiện và tự tắt khi rảnh rỗi, tiết kiệm RAM và bảo mật hơn.
- Content Script Isolation: Content script chia sẻ cây DOM với trang web nhưng chạy trong một môi trường thực thi JavaScript tách biệt (Isolated World). Tuy nhiên, trang web vẫn có thể lừa content script thông qua việc sửa đổi các thuộc tính DOM hoặc gửi thông điệp `window.postMessage` giả mạo.
- Sender Validation: Khi nhận thông điệp qua `chrome.runtime.onMessage`, background worker bắt buộc phải kiểm tra `sender.id` và `sender.origin`.
- **Quy tắc quyết định kỹ thuật**:
- Chỉ xin các quyền tối thiểu thông qua `optional_permissions` thay vì xin quyền tràn lan lúc cài đặt.
- Tuyệt đối cấm sử dụng `externally_connectable` mở rộng tới tất cả các domain.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Background script nhận lệnh `chrome.runtime.onMessageExternal` mà không kiểm tra URL của trang web gửi đến, cho phép bất kỳ website độc hại nào cũng có thể gọi extension để lấy thông tin đăng nhập của người dùng.

## 6. Step-by-Step Execution Workflow
1. Khởi tạo `manifest.json` chuẩn Manifest V3 với danh sách permissions tối thiểu.
2. Cấu hình kiểm tra tính hợp lệ của `sender` trong mọi listener nhận tin nhắn nội bộ.
3. Sử dụng `chrome.storage.session` để lưu trữ dữ liệu tạm thời (tự động xóa khi đóng trình duyệt) thay vì `chrome.storage.local`.
4. Áp dụng Content Security Policy nghiêm ngặt khóa chặt extension.
5. Chạy công cụ kiểm toán bảo mật tự động `ext-audit` để phát hiện lỗ hổng.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```json
// manifest.json chuẩn Manifest V3 an toàn tối đa
{
  "manifest_version": 3,
  "name": "Enterprise Security Vault",
  "version": "5.0.0",
  "permissions": ["storage", "activeTab"],
  "background": {
    "service_worker": "background.js",
    "type": "module"
  },
  "content_security_policy": {
    "extension_pages": "script-src 'self'; object-src 'none'; frame-ancestors 'none';"
  }
}
```

### Lệnh xác minh & thực thi:
```bash
# Kiểm tra extension có vi phạm quy định Manifest V3 của Chrome Web Store không
npx chrome-webstore-upload-cli verify --source dist/
```

## 8. Anti-Patterns & Common Traps
- Sử dụng hàm `window.postMessage` để truyền mật khẩu giữa trang web và extension mà không mã hóa.
- Nạp thư viện jQuery hoặc SDK ngoài từ đường link CDN bên ngoài trong extension.

## 9. Quality Gates & Acceptance Criteria
- 0 quyền dư thừa (Over-privileged permissions) trong file `manifest.json`.
- Vượt qua bài kiểm tra tự động của Chrome Web Store mà không có cảnh báo bảo mật.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Mọi dữ liệu người dùng lưu trong extension phải được mã hóa bằng Web Crypto API nếu lưu lâu dài.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ thống An ninh & SkillOps**: Tương thích GitHub Actions, SARIF, CycloneDX/SPDX, Semgrep, OWASP ZAP.

## 12. Deliverables & Output Artifacts
- Gói Extension Manifest V3 hoàn chỉnh đạt chuẩn bảo mật.
- Báo cáo kiểm toán quyền hạn và ranh giới truyền thông điệp.

## 13. Related & Complementary Skills
dex-web-security-headers, dex-sast-finding-triage, dex-typescript-type-safety

## 14. Realistic Usage Example
### Tình huống thực tế:
Một công ty bảo mật phát triển tiện ích quản lý mật khẩu cho nhân viên. Kẻ tấn công cố tình tạo một trang web lừa đảo gửi thông điệp giả mạo tới extension để yêu cầu xuất danh sách mật khẩu. Nhờ cơ chế kiểm tra `sender.origin` chặt chẽ và chỉ chấp nhận lệnh từ domain nội bộ công ty, extension đã từ chối lệnh tấn công ngay lập tức và ghi log cảnh báo tới đội ngũ an ninh.
