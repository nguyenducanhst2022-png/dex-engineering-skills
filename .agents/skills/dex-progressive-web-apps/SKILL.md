---
name: dex-progressive-web-apps
description: Engineer installable Progressive Web Apps (PWA) with Workbox offline caching strategies, background sync, Web App Manifests, service worker lifecycle governance, and seamless app updates. Use when building offline-capable web apps, mobile-friendly portals, or desktop web apps.
---

# dex-progressive-web-apps

## 1. Purpose & Scope
Xây dựng ứng dụng web lũy tiến (Progressive Web Apps - PWA) chuẩn công nghiệp có khả năng cài đặt như ứng dụng native; quản trị vòng đời Service Worker, thiết lập chiến lược lưu trữ bộ nhớ đệm ngoại tuyến (Offline Caching) qua Workbox, đồng bộ nền (Background Sync) và thông báo cập nhật phiên bản mượt mà.

## 2. When to Use
- Khi ứng dụng cần hoạt động ổn định kể cả khi mất kết nối Internet hoàn toàn (Offline-first experience).
- Khi muốn cung cấp trải nghiệm cài đặt lên màn hình chính (Home Screen) của điện thoại và máy tính mà không cần thông qua App Store.
- Khi cần tăng tốc độ tải trang tức thì cho các lần truy cập tiếp theo thông qua cache service worker.

## 3. When NOT to Use
- Khi ứng dụng yêu cầu các API phần cứng đặc thù mà trình duyệt không hỗ trợ (ví dụ can thiệp sâu hệ điều hành).
- Khi website chỉ là một trang tin tức tĩnh đơn giản cập nhật liên tục nội dung mới mà không cần cài đặt.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Môi trường kết nối bảo mật HTTPS, Web App Manifest (`manifest.json`), kiến thức về vòng đời Service Worker.
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn trong phạm vi dự án, không can thiệp vào tài nguyên sản xuất khi chưa có phê duyệt.

## 5. Core Concepts & Taxonomy
- **Service Worker Lifecycle:** Install -> Waiting -> Activate. Quản lý việc cập nhật phiên bản mà không làm gián đoạn phiên làm việc của người dùng.
- **Caching Strategies:** Stale-While-Revalidate cho tài nguyên thường xuyên thay đổi, Cache-First cho font và ảnh tĩnh, Network-First cho dữ liệu API quan trọng.
- **Background Synchronization:** Tự động lưu các hành động gửi dữ liệu khi mất mạng vào IndexedDB và gửi lại khi có mạng.

## 6. Step-by-Step Execution Workflow
1. Tạo tệp `manifest.webmanifest` chuẩn với đầy đủ icons, theme_color và display: standalone.
2. Đăng ký Service Worker và tích hợp Workbox để định nghĩa các chiến lược bộ nhớ đệm.
3. Thiết lập giao diện thông báo 'Đã có phiên bản mới, bấm để tải lại' (Skip Waiting Prompt).
4. Xây dựng trang dự phòng khi ngoại tuyến (`offline.html`) cung cấp hướng dẫn cho người dùng.
5. Kiểm tra ứng dụng vượt qua 100% tiêu chí PWA trong công cụ Google Lighthouse.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```javascript
// Service Worker with Workbox Stale-While-Revalidate
import { registerRoute } from 'workbox-routing';
import { StaleWhileRevalidate, CacheFirst } from 'workbox-strategies';
import { ExpirationPlugin } from 'workbox-expiration';

// Cache Google Fonts with CacheFirst
registerRoute(
  ({ url }) => url.origin === 'https://fonts.googleapis.com',
  new CacheFirst({
    cacheName: 'google-fonts-cache',
    plugins: [new ExpirationPlugin({ maxEntries: 20, maxAgeSeconds: 365 * 24 * 60 * 60 })]
  })
);

// Cache API Requests with StaleWhileRevalidate
registerRoute(
  ({ url }) => url.pathname.startsWith('/api/dashboard'),
  new StaleWhileRevalidate({
    cacheName: 'api-dashboard-cache',
    plugins: [new ExpirationPlugin({ maxEntries: 50, maxAgeSeconds: 5 * 60 })]
  })
);
```

## 8. Anti-Patterns & Common Traps
- Lưu cache API vĩnh viễn mà không có thời hạn hết hạn (Expiration Policy) khiến người dùng thấy dữ liệu cũ suốt đời.
- Tự động gọi `self.skipWaiting()` ngay lập tức trong nền làm tải lại trang bất ngờ khi người dùng đang nhập dữ liệu dở.
- Không cung cấp trang offline fallback khiến ứng dụng hiện màn hình lỗi khủng long của trình duyệt.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Điểm PWA trên Google Lighthouse đạt 100/100.
- QG-02: Ứng dụng tải được giao diện cơ sở (App Shell) hoàn chỉnh trong chế độ máy bay (Airplane Mode).
- QG-03: Có thông báo xác nhận cập nhật phiên bản mới một cách minh bạch.

## 10. Security & Safety Boundaries
- Chỉ chạy Service Worker trên giao thức HTTPS; thiết lập phạm vi điều khiển (scope) chính xác để ngăn chặn việc đánh chặn tài nguyên trái phép.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Tệp cấu hình Web App Manifest `manifest.webmanifest`.
1. Kịch bản Service Worker chuẩn `sw.ts` tích hợp Workbox.
1. Component React thông báo cập nhật ứng dụng `ReloadPrompt.tsx`.

## 13. Related & Complementary Skills
- [`dex-mobile-offline-sync`](.agents/skills/dex-mobile-offline-sync/SKILL.md)
- [`dex-caching-strategies`](.agents/skills/dex-caching-strategies/SKILL.md)
- [`dex-web-push-permission-flow`](.agents/skills/dex-web-push-permission-flow/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Phát triển ứng dụng ghi chú cho kỹ sư công trường nơi sóng di động chập chờn. Kỹ sư kích hoạt `dex-progressive-web-apps` để biến website thành PWA có thể cài đặt lên điện thoại, lưu toàn bộ ghi chú vào IndexedDB khi mất mạng và tự động đồng bộ lên máy chủ ngay khi có 4G trở lại.
