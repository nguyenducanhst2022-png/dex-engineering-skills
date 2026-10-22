---
name: dex-extension-background-lifecycle
description: Engineer resilient Manifest V3 background service workers with chrome.alarms scheduling, state serialization, asynchronous event registration, and idle termination recovery. Use when preventing background job drops, memory leaks, or unhandled promise rejections during worker suspension.
---

# dex-extension-background-lifecycle

## 1. Purpose & Scope
Thiết kế và quản trị vòng đời của Background Service Worker trong Manifest V3; xử lý hiện tượng trình duyệt tự động ngắt worker khi không hoạt động (Idle Suspension), lập lịch tác vụ định kỳ qua `chrome.alarms`, tuần tự hóa trạng thái vào bộ nhớ lưu trữ và khôi phục hoạt động tức thì khi có sự kiện mới mà không bị thất thoát dữ liệu.

## 2. When to Use
- Khi extension thực hiện các tác vụ nền định kỳ như kiểm tra thông báo, đồng bộ dữ liệu hoặc làm mới token xác thực.
- Khi người dùng phản ánh extension thỉnh thoảng ngừng hoạt động sau vài phút không mở popup.
- Khi cần quản lý trạng thái phiên làm việc trong môi trường service worker vô trạng thái (stateless).

## 3. When NOT to Use
- Khi tác vụ chỉ cần thực thi khi người dùng đang mở popup giao diện (Popup Lifecycle).
- Khi xây dựng Web Worker tính toán song song dưới nền của trang web thông thường.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Kiến thức về cơ chế khởi động và đình chỉ của Service Worker trong Chromium, API `chrome.alarms` và `chrome.storage.local`.
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; tuyệt đối không can thiệp trái phép vào hệ thống của bên thứ ba.

## 5. Core Concepts & Taxonomy
- **Event-Driven Architecture:** Đăng ký các bộ lắng nghe sự kiện đồng bộ ở cấp độ cao nhất của tệp kịch bản (Top-level synchronous listener registration).
- **Alarm-Based Scheduling:** Thay thế hoàn toàn `setInterval` bằng `chrome.alarms` vì `setInterval` sẽ bị hủy khi worker bị đình chỉ.
- **State Rehydration:** Tự động tải lại trạng thái từ `chrome.storage` mỗi khi service worker được đánh thức bởi một sự kiện mới.

## 6. Step-by-Step Execution Workflow
1. Đăng ký các sự kiện `chrome.runtime.onStartup`, `chrome.runtime.onInstalled` và `chrome.alarms.onAlarm` ở cấp cao nhất của mã nguồn.
2. Thay thế các hàm hẹn giờ `setTimeout/setInterval` bằng việc tạo lịch `chrome.alarms.create`.
3. Lưu trạng thái đang chạy vào `chrome.storage.session` hoặc `chrome.storage.local` trước khi kết thúc tác vụ.
4. Tái hiện trạng thái (Rehydrate) ngay khi worker thức dậy bằng cách đọc dữ liệu từ storage.
5. Kiểm tra tính kiên cường bằng công cụ 'Terminate Service Worker' trong tab `chrome://extensions`.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```typescript
// Resilient Service Worker Lifecycle Pattern
// MUST be registered synchronously at top-level
chrome.alarms.onAlarm.addListener(async (alarm) => {
  if (alarm.name === 'SYNC_TELEMETRY') {
    const state = await chrome.storage.local.get(['pendingQueue']);
    const queue = state.pendingQueue || [];
    if (queue.length > 0) {
      await flushQueueToServer(queue);
      await chrome.storage.local.set({ pendingQueue: [] });
    }
  }
});

chrome.runtime.onInstalled.addListener(() => {
  // Setup recurring alarm every 15 minutes
  chrome.alarms.create('SYNC_TELEMETRY', { periodInMinutes: 15 });
});
```

## 8. Anti-Patterns & Common Traps
- Đăng ký bộ lắng nghe sự kiện bên trong một hàm callback bất đồng bộ (ví dụ bên trong `storage.get()`), khiến trình duyệt không kích hoạt sự kiện khi worker thức dậy.
- Dùng biến toàn cục để lưu danh sách hàng đợi mà không ghi vào storage, dẫn đến mất trắng dữ liệu khi worker bị tắt sau 30 giây.
- Cố tình tạo các kết nối mạng rác để 'hack' giữ cho service worker không bao giờ ngủ (vi phạm chính sách và tốn pin người dùng).

## 9. Quality Gates & Acceptance Criteria
- QG-01: 100% event listeners được đăng ký đồng bộ ở top-level của file background.
- QG-02: Không sử dụng `setInterval` cho các tác vụ nền định kỳ dài hơn 1 phút.
- QG-03: Kiểm thử thành công việc thực thi alarm sau khi cưỡng bức kill service worker.

## 10. Security & Safety Boundaries
- Không lưu các khóa giải mã hoặc thông tin nhạy cảm ở dạng plain-text không mã hóa trong `chrome.storage.local`.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Hoạt động phân tích hoàn toàn hợp pháp, minh bạch và có sự ủy quyền chính thức từ chủ sở hữu hệ thống.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Mẫu kịch bản Service Worker chuẩn vòng đời `BackgroundWorkerEngine.ts`.
1. Module quản lý lập lịch tác vụ nền qua `chrome.alarms`.

## 13. Related & Complementary Skills
- [`dex-browser-extension-mv3`](.agents/skills/dex-browser-extension-mv3/SKILL.md)
- [`dex-extension-storage-migration`](.agents/skills/dex-extension-storage-migration/SKILL.md)
- [`dex-scheduled-workflows`](.agents/skills/dex-scheduled-workflows/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Extension theo dõi giá vàng gặp lỗi thỉnh thoảng không thông báo khi giá biến động. Kỹ sư kích hoạt `dex-extension-background-lifecycle`, phát hiện lập trình viên cũ dùng `setInterval(checkPrice, 60000)` khiến tiến trình bị dừng khi worker ngủ. Chuyển sang dùng `chrome.alarms` và lưu trữ trạng thái vào storage, giúp cảnh báo hoạt động chính xác 24/7.
