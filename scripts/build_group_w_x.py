# -*- coding: utf-8 -*-
"""
DEX SKILLOPS — BUILDER FOR GROUPS W & X (Skills 221–240)
Group W: Browser Extensions & Automation (221–230)
Group X: Authorized Reverse Engineering (231–240)
"""

import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SKILLS_DIR = os.path.join(ROOT, ".agents", "skills")

GROUP_W_X_SKILLS = [
    # --- GROUP W: Browser Extensions & Automation ---
    {
        "id": "dex-browser-extension-mv3",
        "index": 221,
        "group": "Group W",
        "domain": "Browser Extensions & Automation",
        "description": "Architect Manifest V3 browser extensions with non-persistent background service workers, declarativeNetRequest rules, minimal permission scopes, and cross-browser packaging (Chrome, Firefox, Edge, Safari). Use when bootstrapping extensions, migrating from Manifest V2, or passing Web Store security reviews.",
        "purpose": "Thiết kế kiến trúc tiện ích mở rộng trình duyệt chuẩn Manifest V3 (MV3); chuyển đổi background page sang background service worker không duy trì trạng thái liên tục, thay thế blocking webRequest bằng declarativeNetRequest, thu hẹp phạm vi quyền hạn và đóng gói đa trình duyệt (Chrome, Firefox, Edge, Safari).",
        "when_use": [
            "Khi khởi tạo dự án extension mới cho trình duyệt web.",
            "Khi di chuyển extension cũ từ Manifest V2 sang Manifest V3 theo yêu cầu của Google Chrome Web Store.",
            "Khi chuẩn bị hồ sơ kiểm duyệt an ninh bảo mật để xuất bản extension lên các chợ ứng dụng."
        ],
        "when_not_use": [
            "Khi chỉ phát triển website hoặc ứng dụng web thông thường không chạy trong môi trường browser extension.",
            "Khi can thiệp trực tiếp vào mã nguồn C++ của engine trình duyệt Chromium/Gecko."
        ],
        "prereqs": "Tệp khai báo `manifest.json`, Node.js toolchain, hiểu biết về mô hình phân tách bối cảnh của extension (Popup, Options, Content Script, Service Worker).",
        "concepts": [
            "Manifest V3 Security Model: Cấm thực thi chuỗi ký tự dạng mã (No `eval()` hoặc nạp mã JavaScript từ CDN bên ngoài).",
            "DeclarativeNetRequest API: Chuyển quyền chặn và sửa đổi header mạng cho trình duyệt thực thi theo tập luật khai báo tĩnh.",
            "Ephemeral Background Workers: Service worker tự động bị đóng sau 30 giây rảnh rỗi để tiết kiệm pin và RAM."
        ],
        "steps": [
            "Đặc tả file `manifest.json` phiên bản 3 với các trường `manifest_version: 3`, `background.service_worker`.",
            "Khai báo tối thiểu các quyền cần thiết (`permissions` và `host_permissions`) theo nguyên tắc đặc quyền tối thiểu.",
            "Chuyển đổi các quy tắc sửa đổi header mạng sang tệp quy tắc tĩnh `rules.json` sử dụng `declarativeNetRequest`.",
            "Đảm bảo toàn bộ mã JavaScript được đóng gói nội bộ trong gói cài đặt extension.",
            "Đóng gói bản dựng `.zip` và kiểm tra tương thích trên Chrome, Edge và Firefox (sử dụng WebExtensions Polyfill)."
        ],
        "code_lang": "json",
        "code_example": """{
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
}""",
        "antipatterns": [
            "Xin quyền rộng `*://*/*` hoặc `<all_urls>` khi chỉ cần gọi API đến một domain cụ thể, dẫn đến bị Chrome Web Store từ chối duyệt.",
            "Lưu biến trạng thái toàn cục trong service worker mà không lưu vào `chrome.storage`, khiến mất dữ liệu khi worker bị tắt.",
            "Nạp thư viện ngoài qua thẻ `<script src='https://cdn...'>` (vi phạm nghiêm trọng chính sách bảo mật CSP của MV3)."
        ],
        "quality_gates": [
            "QG-01: File `manifest.json` vượt qua 100% tiêu chí xác thực cấu trúc của Chrome Extension Linter.",
            "QG-02: Không sử dụng bất kỳ hàm thực thi mã động nào (`eval`, `new Function`, `setTimeout(string)`).",
            "QG-03: Hoạt động trơn tru sau khi service worker bị trình duyệt buộc tắt giả lập (Terminate service worker test)."
        ],
        "security": "Áp dụng Content Security Policy (CSP) nghiêm ngặt; không để lộ secret token trong các tệp nội dung extension tải xuống máy khách.",
        "deliverables": [
            "Tệp cấu hình Manifest V3 chuẩn `manifest.json`.",
            "Gói đóng gói extension đa trình duyệt `extension-build.zip`.",
            "Báo cáo giải trình quyền hạn phục vụ kiểm duyệt Store `PERMISSIONS_JUSTIFICATION.md`."
        ],
        "related": ["dex-browser-extension-hardening", "dex-extension-message-security", "dex-extension-background-lifecycle"],
        "scenario": "Di chuyển tiện ích hỗ trợ nhà phát triển từ MV2 sang MV3. Sử dụng `dex-browser-extension-mv3` để thay thế background page bằng Service Worker module, chuyển đổi 8 quy tắc chặn mạng sang `declarativeNetRequest` và vượt qua vòng kiểm duyệt của Chrome Web Store trong 24 giờ."
    },
    {
        "id": "dex-extension-message-security",
        "index": 222,
        "group": "Group W",
        "domain": "Browser Extensions & Automation",
        "description": "Secure asynchronous message channels between content scripts, popup UIs, devtools panels, and background service workers with strict sender origin validation and typed schemas. Use when preventing unauthorized message spoofing, privilege escalation, or cross-tab token interception.",
        "purpose": "Bảo vệ các kênh truyền thông điệp bất đồng bộ (Message Passing Channels) giữa Content Scripts, Popup UI, Devtools Panels và Background Service Worker; thiết lập cơ chế xác thực nguồn gửi (Sender Origin Validation), kiểm tra định kiểu dữ liệu (Typed Schemas) và ngăn chặn tấn công leo thang đặc quyền từ website chứa mã độc.",
        "when_use": [
            "Khi xây dựng luồng truyền tin nội bộ trong browser extension.",
            "Khi extension giao tiếp với các trang web công khai qua `externally_connectable` hoặc `window.postMessage`.",
            "Khi xử lý các hành động nhạy cảm (như đọc token, gọi API đặc quyền) từ yêu cầu của Content Script."
        ],
        "when_not_use": [
            "Khi chỉ truyền dữ liệu nội bộ giữa các hàm trong cùng một file script.",
            "Khi giao tiếp giữa client và server thông thường qua REST API hoặc WebSocket."
        ],
        "prereqs": "Kiến thức về các API `chrome.runtime.sendMessage`, `chrome.tabs.sendMessage`, `chrome.runtime.onMessageExternal`.",
        "concepts": [
            "Sender Origin Verification: Luôn kiểm tra `sender.id === chrome.runtime.id` và `sender.tab.url` trước khi thực thi lệnh.",
            "Type-Safe RPC Messaging: Định nghĩa hợp đồng thông điệp phân biệt (Discriminated Unions) để phân tích payload an toàn.",
            "Privilege Separation: Không bao giờ cho phép Content Script trực tiếp yêu cầu Service Worker thực thi các thao tác tùy tiện (Arbitrary Execution)."
        ],
        "steps": [
            "Định nghĩa kiểu dữ liệu thông điệp bằng TypeScript (gồm trường `action`, `payload`, `timestamp`).",
            "Cài đặt hàm lắng nghe `chrome.runtime.onMessage.addListener` trong background service worker.",
            "Thực hiện kiểm tra tính hợp lệ của nguồn gửi (`sender.origin`, `sender.id`).",
            "Sử dụng bộ xác thực schema (như Zod) để kiểm tra payload trước khi xử lý nghiệp vụ.",
            "Trả lời kết quả qua callback `sendResponse` bất đồng bộ (`return true;`)."
        ],
        "code_lang": "typescript",
        "code_example": """// Secure Extension Message Handler
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
});""",
        "antipatterns": [
            "Tin tưởng tuyệt đối nội dung thông điệp gửi từ Content Script mà không kiểm tra URL nguồn (Content Script có thể bị tấn công XSS từ trang web).",
            "Thực thi trực tiếp mã JavaScript hoặc lệnh SQL nhận được qua message payload.",
            "Để mở quyền `externally_connectable: [\"<all_urls>\"]` mà không có danh sách whitelist tên miền được phép giao tiếp."
        ],
        "quality_gates": [
            "QG-01: 100% các message handler có bước xác minh `sender.id` ngay dòng đầu tiên.",
            "QG-02: Tất cả các thông điệp truyền nhận đều tuân thủ hợp đồng TypeScript Interface đã quy định.",
            "QG-03: Bộ test kiểm thử xâm nhập xác nhận việc gửi thông điệp giả mạo từ trang web khác bị chặn hoàn toàn."
        ],
        "security": "Ngăn chặn các trang web độc hại mạo danh extension để thực hiện các thao tác quản trị hoặc đánh cắp session token.",
        "deliverables": [
            "Hợp đồng giao tiếp an toàn `extension-message-contracts.ts`.",
            "Bộ định tuyến thông điệp có xác thực `SecureMessageRouter.ts`."
        ],
        "related": ["dex-browser-extension-mv3", "dex-extension-content-script-isolation", "dex-api-abuse-prevention"],
        "scenario": "Kiểm toán extension quản lý mật khẩu doanh nghiệp. Phát hiện lỗi Content Script nhận tin nhắn từ bất kỳ website nào và chuyển tiếp thẳng vào Service Worker. Áp dụng `dex-extension-message-security` để thêm lớp kiểm tra nguồn gốc khắt khe và schema validation, ngăn chặn triệt để nguy cơ website đánh cắp thông tin tài khoản."
    },
    {
        "id": "dex-extension-background-lifecycle",
        "index": 223,
        "group": "Group W",
        "domain": "Browser Extensions & Automation",
        "description": "Engineer resilient Manifest V3 background service workers with chrome.alarms scheduling, state serialization, asynchronous event registration, and idle termination recovery. Use when preventing background job drops, memory leaks, or unhandled promise rejections during worker suspension.",
        "purpose": "Thiết kế và quản trị vòng đời của Background Service Worker trong Manifest V3; xử lý hiện tượng trình duyệt tự động ngắt worker khi không hoạt động (Idle Suspension), lập lịch tác vụ định kỳ qua `chrome.alarms`, tuần tự hóa trạng thái vào bộ nhớ lưu trữ và khôi phục hoạt động tức thì khi có sự kiện mới mà không bị thất thoát dữ liệu.",
        "when_use": [
            "Khi extension thực hiện các tác vụ nền định kỳ như kiểm tra thông báo, đồng bộ dữ liệu hoặc làm mới token xác thực.",
            "Khi người dùng phản ánh extension thỉnh thoảng ngừng hoạt động sau vài phút không mở popup.",
            "Khi cần quản lý trạng thái phiên làm việc trong môi trường service worker vô trạng thái (stateless)."
        ],
        "when_not_use": [
            "Khi tác vụ chỉ cần thực thi khi người dùng đang mở popup giao diện (Popup Lifecycle).",
            "Khi xây dựng Web Worker tính toán song song dưới nền của trang web thông thường."
        ],
        "prereqs": "Kiến thức về cơ chế khởi động và đình chỉ của Service Worker trong Chromium, API `chrome.alarms` và `chrome.storage.local`.",
        "concepts": [
            "Event-Driven Architecture: Đăng ký các bộ lắng nghe sự kiện đồng bộ ở cấp độ cao nhất của tệp kịch bản (Top-level synchronous listener registration).",
            "Alarm-Based Scheduling: Thay thế hoàn toàn `setInterval` bằng `chrome.alarms` vì `setInterval` sẽ bị hủy khi worker bị đình chỉ.",
            "State Rehydration: Tự động tải lại trạng thái từ `chrome.storage` mỗi khi service worker được đánh thức bởi một sự kiện mới."
        ],
        "steps": [
            "Đăng ký các sự kiện `chrome.runtime.onStartup`, `chrome.runtime.onInstalled` và `chrome.alarms.onAlarm` ở cấp cao nhất của mã nguồn.",
            "Thay thế các hàm hẹn giờ `setTimeout/setInterval` bằng việc tạo lịch `chrome.alarms.create`.",
            "Lưu trạng thái đang chạy vào `chrome.storage.session` hoặc `chrome.storage.local` trước khi kết thúc tác vụ.",
            "Tái hiện trạng thái (Rehydrate) ngay khi worker thức dậy bằng cách đọc dữ liệu từ storage.",
            "Kiểm tra tính kiên cường bằng công cụ 'Terminate Service Worker' trong tab `chrome://extensions`."
        ],
        "code_lang": "typescript",
        "code_example": """// Resilient Service Worker Lifecycle Pattern
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
});""",
        "antipatterns": [
            "Đăng ký bộ lắng nghe sự kiện bên trong một hàm callback bất đồng bộ (ví dụ bên trong `storage.get()`), khiến trình duyệt không kích hoạt sự kiện khi worker thức dậy.",
            "Dùng biến toàn cục để lưu danh sách hàng đợi mà không ghi vào storage, dẫn đến mất trắng dữ liệu khi worker bị tắt sau 30 giây.",
            "Cố tình tạo các kết nối mạng rác để 'hack' giữ cho service worker không bao giờ ngủ (vi phạm chính sách và tốn pin người dùng)."
        ],
        "quality_gates": [
            "QG-01: 100% event listeners được đăng ký đồng bộ ở top-level của file background.",
            "QG-02: Không sử dụng `setInterval` cho các tác vụ nền định kỳ dài hơn 1 phút.",
            "QG-03: Kiểm thử thành công việc thực thi alarm sau khi cưỡng bức kill service worker."
        ],
        "security": "Không lưu các khóa giải mã hoặc thông tin nhạy cảm ở dạng plain-text không mã hóa trong `chrome.storage.local`.",
        "deliverables": [
            "Mẫu kịch bản Service Worker chuẩn vòng đời `BackgroundWorkerEngine.ts`.",
            "Module quản lý lập lịch tác vụ nền qua `chrome.alarms`."
        ],
        "related": ["dex-browser-extension-mv3", "dex-extension-storage-migration", "dex-scheduled-workflows"],
        "scenario": "Extension theo dõi giá vàng gặp lỗi thỉnh thoảng không thông báo khi giá biến động. Kỹ sư kích hoạt `dex-extension-background-lifecycle`, phát hiện lập trình viên cũ dùng `setInterval(checkPrice, 60000)` khiến tiến trình bị dừng khi worker ngủ. Chuyển sang dùng `chrome.alarms` và lưu trữ trạng thái vào storage, giúp cảnh báo hoạt động chính xác 24/7."
    },
    {
        "id": "dex-extension-content-script-isolation",
        "index": 224,
        "group": "Group W",
        "domain": "Browser Extensions & Automation",
        "description": "Enforce strict DOM boundaries between untrusted host web page scripts and extension content scripts using isolated worlds, CustomEvent communication bridges, and Shadow DOM encapsulation. Use when preventing webpage DOM pollution, prototype poisoning, or XSS hijacking of extension capabilities.",
        "purpose": "Thiết lập ranh giới cách ly nghiêm ngặt giữa mã kịch bản của trang web đích (Main World) và Content Script của tiện ích mở rộng (Isolated World); ứng dụng Shadow DOM đóng kín (Closed Shadow DOM) để chống xung đột CSS/DOM, ngăn chặn tấn công ô nhiễm nguyên mẫu (Prototype Pollution) và bảo vệ giao diện extension không bị trang web can thiệp.",
        "when_use": [
            "Khi tiện ích mở rộng cần nhúng các thành phần giao diện (UI Widgets, Buttons, Popups) trực tiếp vào trang web của bên thứ ba.",
            "Khi trang web đích có các kịch bản JavaScript phức tạp hoặc không đáng tin cậy có thể làm hỏng logic của extension.",
            "Khi cần truyền dữ liệu an toàn giữa Content Script và kịch bản trang web gốc mà không để lộ các API đặc quyền của extension."
        ],
        "when_not_use": [
            "Khi extension chỉ hoạt động trên một cửa sổ Popup độc lập không chạm vào DOM của trang web.",
            "Khi trang web do chính tổ chức mình kiểm soát và có sẵn SDK tích hợp chính thức."
        ],
        "prereqs": "Kiến thức về mô hình thế giới cô lập (Isolated Worlds) trong trình duyệt, Web Components và Shadow DOM API.",
        "concepts": [
            "Isolated World Security Boundary: Content Script và trang web chia sẻ chung cấu trúc DOM nhưng có không gian biến JavaScript, nguyên mẫu prototype và đối tượng toàn cục `window` hoàn toàn tách biệt.",
            "Closed Shadow DOM Encapsulation: Ngăn chặn mã kịch bản của trang web đọc hoặc sửa đổi các nút DOM bên trong giao diện extension bằng `document.querySelector`.",
            "Secure CustomEvent Bridge: Truyền nhận dữ liệu qua lại giữa hai thế giới bằng các sự kiện tùy biến có làm sạch payload (Data Sanitization)."
        ],
        "steps": [
            "Tạo một phần tử container mẹ trên trang web và gắn một Closed Shadow Root (`attachShadow({ mode: 'closed' })`).",
            "Nhúng các kiểu dáng CSS của extension vào bên trong Shadow Root để chống ô nhiễm kiểu dáng hai chiều.",
            "Xây dựng giao diện UI của extension bên trong không gian bảo vệ của Shadow DOM.",
            "Thiết lập kênh liên lạc an toàn với trang web qua `CustomEvent` có kiểm tra nguồn gốc và kiểu dữ liệu.",
            "Kiểm tra tính bất biến của các nguyên mẫu cốt lõi (`Array.prototype`, `Object.prototype`) trong môi trường content script."
        ],
        "code_lang": "typescript",
        "code_example": """// Injected UI via Closed Shadow DOM
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
}""",
        "antipatterns": [
            "Chèn giao diện extension thẳng vào thẻ `<body>` mà không dùng Shadow DOM, dẫn đến CSS của trang web làm vỡ nát giao diện extension.",
            "Lắng nghe `window.addEventListener('message')` mà không kiểm tra cẩn thận thuộc tính `event.origin` và cấu trúc dữ liệu.",
            "Thực thi trực tiếp các hàm hoặc đọc các biến toàn cục mà trang web đặt sẵn trên `window` mà không xác minh tính toàn vẹn."
        ],
        "quality_gates": [
            "QG-01: Giao diện extension được cô lập hoàn toàn bên trong Shadow DOM, không bị ảnh hưởng bởi CSS toàn cục của trang web.",
            "QG-02: Không có rò rỉ các đối tượng đặc quyền `chrome.*` sang môi trường thực thi của trang web.",
            "QG-03: Vượt qua các bài kiểm tra tấn công Prototype Pollution thử nghiệm."
        ],
        "security": "Không cho phép mã kịch bản độc hại của trang web can thiệp vào các nút bấm thanh toán hoặc form nhập mật khẩu của extension.",
        "deliverables": [
            "Module chèn giao diện cô lập `ShadowDOMContainer.ts`.",
            "Cầu nối truyền tin an toàn giữa các thế giới `ContentScriptBridge.ts`."
        ],
        "related": ["dex-extension-message-security", "dex-browser-extension-hardening", "dex-web-security-headers"],
        "scenario": "Phát triển tiện ích kiểm tra lỗi chính tả tự động trên web. Khi nhúng vào các trang web có CSS định nghĩa `* { color: red !important; }`, nút bấm của extension bị hỏng màu sắc. Áp dụng `dex-extension-content-script-isolation` với Closed Shadow DOM giúp nút bấm của tiện ích hiển thị hoàn hảo và bảo vệ an toàn trước các kịch bản theo dõi của trang web."
    },
    {
        "id": "dex-extension-storage-migration",
        "index": 225,
        "group": "Group W",
        "domain": "Browser Extensions & Automation",
        "description": "Manage schema versioning, asynchronous data migrations, and corruption recovery for chrome.storage.local and chrome.storage.sync across extension updates. Use when migrating user settings across major versions, syncing cross-device data, or recovering from quota-exceeded storage errors.",
        "purpose": "Quản lý cơ chế phân phiên bản lược đồ dữ liệu (Schema Versioning), di chuyển dữ liệu bất đồng bộ (Data Migration) và tự phục hồi khi dữ liệu bị hỏng trong `chrome.storage.local` và `chrome.storage.sync`; đảm bảo cập nhật phiên bản extension mượt mà, đồng bộ cài đặt đa thiết bị và xử lý sự cố vượt hạn mức dung lượng (Quota Exceeded).",
        "when_use": [
            "Khi nâng cấp phiên bản extension có thay đổi cấu trúc dữ liệu cài đặt của người dùng.",
            "Khi chuyển đổi từ lưu trữ cục bộ (`local`) sang lưu trữ đồng bộ đám mây (`sync`) hoặc ngược lại.",
            "Khi nhận được thông báo lỗi vượt quá giới hạn lưu trữ (Storage Quota Exceeded)."
        ],
        "when_not_use": [
            "Khi quản lý di chuyển cơ sở dữ liệu quan hệ PostgreSQL/MySQL dưới backend.",
            "Khi chỉ lưu trữ các giá trị tạm thời không cần bảo toàn qua các lần cập nhật extension."
        ],
        "prereqs": "Kiến thức về các hạn mức của `chrome.storage` (Sync quota: 100KB tổng, 8KB/item; Local quota: 10MB), sự kiện `chrome.runtime.onInstalled`.",
        "concepts": [
            "Linear Schema Migrations: Áp dụng tuần tự các bước nâng cấp cấu trúc từ phiên bản cũ lên phiên bản mới (v1 -> v2 -> v3).",
            "Storage Quota Governance: Tự động nén dữ liệu hoặc di dời các dữ liệu lớn sang `chrome.storage.local` khi `chrome.storage.sync` chạm ngưỡng cảnh báo.",
            "Safe Fallback & Corruption Recovery: Luôn tạo bản sao lưu dự phòng (Snapshot) trước khi thực hiện di chuyển dữ liệu."
        ],
        "steps": [
            "Lưu số hiệu phiên bản cấu trúc dữ liệu hiện tại trong khóa `__schema_version`.",
            "Lắng nghe sự kiện `chrome.runtime.onInstalled` với lý do `details.reason === 'update'`.",
            "So sánh phiên bản dữ liệu đã lưu với phiên bản yêu cầu của mã nguồn mới.",
            "Thực hiện chuỗi hàm di chuyển (Migration Pipeline) tuần tự cho từng bước nhảy phiên bản.",
            "Kiểm tra tính toàn vẹn của dữ liệu sau di chuyển và cập nhật lại `__schema_version`."
        ],
        "code_lang": "typescript",
        "code_example": """// Safe Storage Migration Runner
export async function runStorageMigrations() {
  const current = await chrome.storage.local.get(['__schema_version']);
  let version = current.__schema_version || 1;

  if (version < 2) {
    // Migration v1 -> v2: Flatten theme options
    const v1Data = await chrome.storage.local.get(['userTheme', 'fontSize']);
    await chrome.storage.local.set({
      preferences: {
        theme: v1Data.userTheme || 'system',
        fontSize: v1Data.fontSize || 14
      },
      __schema_version: 2
    });
    await chrome.storage.local.remove(['userTheme', 'fontSize']);
    version = 2;
  }
}""",
        "antipatterns": [
            "Thay đổi cấu trúc dữ liệu mà không viết hàm migration khiến người dùng bị mất toàn bộ cấu hình cũ khi extension tự động cập nhật.",
            "Lưu trữ dữ liệu nhị phân hoặc chuỗi base64 khổng lồ vào `chrome.storage.sync` làm sập giới hạn 8KB của trình duyệt.",
            "Xóa sạch dữ liệu của người dùng khi gặp lỗi đọc cấu hình thay vì kích hoạt luồng khôi phục dự phòng."
        ],
        "quality_gates": [
            "QG-01: 100% các lần cập nhật có thay đổi lược đồ đều có mã kiểm thử di chuyển dữ liệu tương ứng.",
            "QG-02: Không làm mất bất kỳ cài đặt người dùng nào khi nâng cấp từ phiên bản cũ nhất lên phiên bản mới nhất.",
            "QG-03: Có cơ chế tự động dọn dẹp các khóa dữ liệu lỗi thời (Orphaned keys)."
        ],
        "security": "Mã hóa các dữ liệu cấu hình nhạy cảm trước khi đồng bộ lên dịch vụ lưu trữ đám mây của trình duyệt.",
        "deliverables": [
            "Hệ thống di chuyển dữ liệu lưu trữ `StorageMigrationPipeline.ts`.",
            "Bộ test tự động kiểm thử di chuyển dữ liệu qua các phiên bản."
        ],
        "related": ["dex-schema-evolution", "dex-browser-extension-mv3", "dex-storage-lifecycle"],
        "scenario": "Phát hành phiên bản 3.0 của extension với cấu trúc cài đặt mới dạng module. Kỹ sư kích hoạt `dex-extension-storage-migration` để tự động chuyển đổi cấu hình của 50,000 người dùng hiện tại mà không ai bị mất dữ liệu phím tắt hoặc tài khoản liên kết đã lưu."
    },
    {
        "id": "dex-browser-automation-testing",
        "index": 226,
        "group": "Group W",
        "domain": "Browser Extensions & Automation",
        "description": "Design deterministic, flake-free browser automation suites using Playwright/Puppeteer with locator best practices, explicit network idle waits, and isolated browser contexts. Use when testing complex user checkout journeys, cross-browser interactions, or end-to-end web flows.",
        "purpose": "Thiết kế và xây dựng bộ kiểm thử tự động hóa trình duyệt (Browser Automation Testing) có tính xác định cao, triệt tiêu lỗi chập chờn (Flaky Tests); ứng dụng công nghệ Playwright/Puppeteer với chiến lược định vị phần tử theo ngữ nghĩa (Semantic Locators), quản lý ngữ cảnh trình duyệt cô lập (Isolated Browser Contexts) và cơ chế chờ mạng thông minh.",
        "when_use": [
            "Khi xây dựng bộ kiểm thử đầu-cuối (End-to-End E2E Testing) cho các luồng nghiệp vụ quan trọng.",
            "Khi bộ test hiện tại thường xuyên bị lỗi ngẫu nhiên (flaky) do phụ thuộc vào thời gian chờ cứng (`sleep`).",
            "Khi cần kiểm tra tính tương thích của ứng dụng trên cả 3 engine trình duyệt: Chromium, WebKit và Firefox."
        ],
        "when_not_use": [
            "Khi kiểm thử các hàm tính toán logic nội bộ không có tương tác giao diện (nên dùng Unit Test).",
            "Khi chỉ kiểm tra tính hợp lệ của cú pháp mã nguồn hoặc kiểm tra kiểu TypeScript."
        ],
        "prereqs": "Môi trường Node.js, framework Playwright hoặc Puppeteer, máy chủ kiểm thử ứng dụng có sẵn.",
        "concepts": [
            "User-Facing Locators: Định vị phần tử theo cách người dùng tương tác (`getByRole`, `getByText`, `getByLabel`) thay vì dùng XPath hoặc class CSS dễ vỡ.",
            "Auto-Waiting & Web-First Assertions: Tận dụng cơ chế tự động chờ phần tử hiển thị và có thể thao tác được của Playwright (`await expect(locator).toBeVisible()`).",
            "Browser Context Isolation: Mỗi ca kiểm thử chạy trong một Browser Context sạch hoàn toàn cookie và local storage để ngăn ngừa ảnh hưởng chéo."
        ],
        "steps": [
            "Cấu hình Playwright test runner với các thiết bị mục tiêu (Desktop Chrome, Mobile Safari).",
            "Viết kịch bản kiểm thử áp dụng mô hình Page Object Model (POM) để tái sử dụng mã nguồn.",
            "Sử dụng các bộ định vị ngữ nghĩa hướng người dùng như `page.getByRole('button', { name: 'Submit' })`.",
            "Chờ đợi các phản hồi API hoặc trạng thái mạng ổn định bằng `page.waitForResponse` thay vì `page.waitForTimeout`.",
            "Thu thập ảnh chụp màn hình, video và trace file khi có ca kiểm thử thất bại để phục vụ điều tra nguyên nhân."
        ],
        "code_lang": "typescript",
        "code_example": """import { test, expect } from '@playwright/test';

test('User completes multi-step checkout journey', async ({ page }) => {
  await page.goto('/catalog');

  // Semantic user-facing locator
  await page.getByRole('button', { name: 'Add to Cart' }).first().click();
  await page.getByRole('link', { name: 'View Cart' }).click();

  // Web-first assertion with auto-waiting
  await expect(page.getByTestId('cart-total')).toHaveText('$99.00');

  // Fill shipping form
  await page.getByLabel('Full Name').fill('Alex Rivera');
  await page.getByRole('button', { name: 'Confirm Purchase' }).click();

  // Await success screen
  await expect(page.getByRole('heading', { name: 'Order Confirmed' })).toBeVisible();
});""",
        "antipatterns": [
            "Sử dụng lệnh dừng chờ cứng như `page.waitForTimeout(5000)` khiến test chạy chậm và vẫn có thể fail nếu mạng bị lag.",
            "Dùng bộ định vị dựa vào cấu trúc DOM sâu như `div > div:nth-child(3) > span` (sẽ hỏng ngay khi sửa giao diện).",
            "Chia sẻ chung trạng thái đăng nhập hoặc dữ liệu giữa các ca kiểm thử khác nhau."
        ],
        "quality_gates": [
            "QG-01: Tỷ lệ thất bại do chập chờn (Flakiness Rate) dưới 0.1% qua 100 lần chạy kiểm thử liên tiếp.",
            "QG-02: 100% các bước tương tác sử dụng Semantic Locators hoặc `data-testid` chuẩn.",
            "QG-03: Mỗi ca kiểm thử thất bại đều tự động xuất file Playwright Trace để xem lại từng thao tác."
        ],
        "security": "Không đưa mật khẩu hoặc tài khoản quản trị thật vào kịch bản kiểm thử; sử dụng tài khoản thử nghiệm chuyên dụng trên môi trường staging.",
        "deliverables": [
            "Bộ kịch bản kiểm thử tự động Playwright hoàn chỉnh `e2e-suite.spec.ts`.",
            "Báo cáo kết quả kiểm thử kèm video và trace artifacts."
        ],
        "related": ["dex-end-to-end-engineering", "dex-flaky-test-remediation", "dex-headless-ui-verification"],
        "scenario": "Đội ngũ phát triển gặp khủng hoảng vì bộ test E2E 200 kịch bản chạy mất 45 phút và 20% ca test bị fail ngẫu nhiên mỗi lần chạy CI. Áp dụng `dex-browser-automation-testing` để refactor sang Playwright với semantic locators và isolated contexts, giảm thời gian chạy xuống 8 phút và tỷ lệ flaky về đúng 0%."
    },
    {
        "id": "dex-cdp-observability",
        "index": 227,
        "group": "Group W",
        "domain": "Browser Extensions & Automation",
        "description": "Harness the Chrome DevTools Protocol (CDP) for low-level performance trace capture, memory heap snapshot analysis, network throttle simulation, and console telemetry auditing. Use when diagnosing elusive browser memory leaks, profiling main thread blocking tasks, or automating deep performance audits.",
        "purpose": "Khai thác giao thức Chrome DevTools Protocol (CDP) để chẩn đoán chuyên sâu hiệu năng trình duyệt ở tầng thấp; tự động thu thập dấu vết thực thi (Performance Traces), chụp và so sánh ảnh chụp bộ nhớ heap (Heap Snapshots), mô phỏng bóp nghẹt mạng/CPU và kiểm toán nhật ký console của trình duyệt mà không làm rò rỉ phiên làm việc.",
        "when_use": [
            "Khi cần điều tra các lỗi rò rỉ bộ nhớ (Memory Leaks) phức tạp khiến ứng dụng bị đơ sau một thời gian dài sử dụng.",
            "Khi xây dựng các công cụ đo lường hiệu năng và chất lượng web tự động trong đường ống CI/CD.",
            "Khi cần mô phỏng chính xác các điều kiện mạng yếu, mất gói tin hoặc ngắt kết nối đột ngột ở tầng socket."
        ],
        "when_not_use": [
            "Khi chỉ cần kiểm tra các tính năng tương tác UI thông thường (dùng Playwright cấp cao là đủ).",
            "Khi chạy kiểm thử trên các trình duyệt không thuộc họ Chromium (như Safari/WebKit)."
        ],
        "prereqs": "Kết nối CDP WebSocket (`chrome-remote-interface` hoặc `CDPSession` của Playwright), kiến thức về các domain CDP: `Page`, `Network`, `Performance`, `HeapProfiler`.",
        "concepts": [
            "CDP Domain Architecture: Kiến trúc chia thành các miền chức năng độc lập (Domains) điều khiển qua các lệnh JSON-RPC.",
            "Heap Allocation Timeline: Ghi lại từng lần cấp phát đối tượng trên bộ nhớ JavaScript để tìm ra các đối tượng bị giữ lại không được thu gom rác (Retained Objects).",
            "Network Throttling Profiles: Giả lập chính xác độ trễ mạng (Latency), băng thông tải xuống (Download throughput) và tải lên (Upload throughput)."
        ],
        "steps": [
            "Mở phiên kết nối `CDPSession` từ Playwright hoặc Puppeteer.",
            "Kích hoạt các domain cần thiết: `await client.send('Performance.enable')` và `Network.enable`.",
            "Thiết lập điều kiện mạng mô phỏng (ví dụ mạng 3G Chậm: 400ms latency, 400kbps download).",
            "Chụp ảnh phân bổ bộ nhớ trước và sau khi thực hiện thao tác nghiệp vụ lặp lại 10 lần.",
            "So sánh hai file heap snapshot để tìm các đối tượng bị rò rỉ và lập báo cáo phân tích."
        ],
        "code_lang": "typescript",
        "code_example": """import { chromium } from '@playwright/test';

export async function profileMemoryWithCDP(url: string) {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  const cdp = await page.context().newCDPSession(page);

  await cdp.send('HeapProfiler.enable');
  await page.goto(url);

  // Collect initial garbage and take baseline snapshot
  await cdp.send('HeapProfiler.collectGarbage');
  
  // Track allocation metrics
  const metrics = await cdp.send('Performance.getMetrics');
  console.log('JS Heap Used Size:', metrics.metrics.find(m => m.name === 'JSHeapUsedSize')?.value);

  await browser.close();
}""",
        "antipatterns": [
            "Để mở phiên kết nối CDP mà không đóng lại gây rò rỉ tiến trình Chromium chạy ngầm làm nghẽn RAM server CI.",
            "Chụp heap snapshot quá thường xuyên trên ứng dụng đang tải dữ liệu lớn làm sập tiến trình trình duyệt.",
            "Bỏ qua bước cưỡng bức dọn rác (`collectGarbage`) trước khi đo lường bộ nhớ dẫn đến số liệu đo bị sai lệch."
        ],
        "quality_gates": [
            "QG-01: Bộ nhớ heap JavaScript không tăng tuyến tính sau 20 chu kỳ lặp lại hành động người dùng.",
            "QG-02: Dấu vết thực thi CDP thu thập đầy đủ thông tin về các tác vụ chặn luồng chính (Long Tasks > 50ms).",
            "QG-03: Mọi phiên CDP được dọn dẹp và giải phóng tài nguyên hoàn toàn sau khi hoàn thành đo lường."
        ],
        "security": "Không để cổng điều khiển từ xa CDP (`--remote-debugging-port`) lắng nghe trên giao diện mạng công cộng không có mật khẩu.",
        "deliverables": [
            "Script tự động đo lường hiệu năng sâu qua CDP `cdp-performance-audit.ts`.",
            "Báo cáo phân tích rò rỉ bộ nhớ kèm đồ thị heap memory."
        ],
        "related": ["dex-frontend-performance", "dex-browser-automation-testing", "dex-web-animation-performance"],
        "scenario": "Trang web dashboard theo dõi camera an ninh bị sập tab sau khi chạy liên tục 4 tiếng. Kỹ sư kích hoạt `dex-cdp-observability` để kết nối CDP, tự động chụp heap snapshot mỗi 30 phút, phát hiện một mảng mảng lưu trữ frame ảnh cũ không được xóa bỏ, sửa lỗi và giúp trang chạy ổn định suốt 7 ngày."
    },
    {
        "id": "dex-headless-ui-verification",
        "index": 228,
        "group": "Group W",
        "domain": "Browser Extensions & Automation",
        "description": "Detect and reconcile behavioral and visual discrepancies between headless browser runners (Linux CI) and actual user graphical browsers (Windows/macOS) including font subpixel antialiasing and GPU acceleration flags. Use when debugging CI-only test failures, font rendering shifts, or canvas test flakes.",
        "purpose": "Phát hiện, đối chiếu và đồng nhất hóa các sai lệch về mặt hiển thị và hành vi giữa trình duyệt chạy không giao diện (Headless Browsers trên môi trường Linux CI) và trình duyệt có giao diện thực tế của người dùng (Headed Browsers trên Windows/macOS); xử lý các vấn đề khử răng cưa phông chữ (Subpixel Antialiasing), cờ tăng tốc phần cứng GPU và kích thước viewport ảo.",
        "when_use": [
            "Khi các bài kiểm thử hình ảnh (Visual Regression Tests) chạy PASS trên máy cá nhân nhưng luôn bị FAIL trên GitHub Actions CI.",
            "Khi font chữ hiển thị trên Linux CI bị lệch vài pixel so với bản thiết kế trên macOS/Windows.",
            "Khi kiểm tra các thành phần giao diện sử dụng Canvas hoặc WebGL trong môi trường headless."
        ],
        "when_not_use": [
            "Khi chỉ chạy các bài kiểm thử unit test logic không có liên quan đến hiển thị trình duyệt.",
            "Khi kiểm thử hiệu năng API máy chủ."
        ],
        "prereqs": "Môi trường Docker/Linux CI, cài đặt gói font chuẩn (Noto Sans, Roboto), cờ cấu hình trình duyệt Chromium/Playwright.",
        "concepts": [
            "Headless Mode Discrepancies: Chế độ `--headless=new` hiện đại của Chromium gần gũi với trình duyệt thật hơn so với cờ headless cũ, nhưng vẫn thiếu GPU phần cứng thật.",
            "Font Rasterization Differences: Linux FreeType hiển thị chữ khác biệt nhẹ so với DirectWrite (Windows) và CoreText (macOS).",
            "Software Rendering Override: Sử dụng cờ `--use-gl=angle` hoặc SwiftShader để mô phỏng kết xuất đồ họa trên môi trường không có card đồ họa vật lý."
        ],
        "steps": [
            "Đồng bộ hóa môi trường chạy kiểm thử hình ảnh bằng một Docker container chuẩn hóa chứa đầy đủ bộ phông chữ hệ thống.",
            "Kích hoạt cờ trình duyệt `--headless=new` thay vì cờ headless cũ.",
            "Cấu hình cờ vô hiệu hóa sự khác biệt khử răng cưa của phông chữ (`--font-render-hinting=none`).",
            "Thiết lập độ dung sai hình ảnh (Threshold Tolerance) phù hợp (ví dụ 0.2% đến 0.5% số pixel khác biệt).",
            "Chạy thử nghiệm so khớp ảnh trên cả máy trạm cục bộ và máy chủ CI để xác nhận tính nhất quán."
        ],
        "code_lang": "typescript",
        "code_example": """// Deterministic Headless Browser Configuration
import { chromium, LaunchOptions } from 'playwright';

export const deterministicBrowserConfig: LaunchOptions = {
  headless: true,
  args: [
    '--headless=new',
    '--disable-gpu',
    '--font-render-hinting=none',
    '--disable-skia-runtime-opts',
    '--disable-font-subpixel-positioning',
    '--force-color-profile=srgb',
  ],
};""",
        "antipatterns": [
            "Chạy visual regression test trực tiếp trên hệ điều hành của lập trình viên mà không qua Docker, khiến mỗi người tạo ra một bản ảnh mẫu (snapshot) khác nhau.",
            "Đặt độ dung sai sai khác pixel bằng 0% tuyệt đối giữa các hệ điều hành khác nhau.",
            "Quên cài đặt các gói font cơ bản trên máy chủ Linux CI khiến trình duyệt phải fallback về font chữ xấu xí làm sai lệch bố cục."
        ],
        "quality_gates": [
            "QG-01: 100% các bài visual regression test chạy ổn định và đồng nhất giữa máy trạm cá nhân và server CI.",
            "QG-02: Bộ container kiểm thử tích hợp đầy đủ các gói font chuẩn hóa và cờ khử răng cưa.",
            "QG-03: Không có ca kiểm thử nào thất bại chỉ vì lý do sai khác khử răng cưa phông chữ ở mức vi mô."
        ],
        "security": "Đảm bảo các container chạy headless browser không chạy dưới quyền `root` mà không có sandbox bảo vệ.",
        "deliverables": [
            "Cấu hình Dockerfile chuẩn hóa cho CI visual testing `ci-runner.Dockerfile`.",
            "Module khởi tạo trình duyệt với cờ khử sai lệch `deterministicBrowserConfig.ts`."
        ],
        "related": ["dex-visual-regression", "dex-browser-automation-testing", "dex-compatibility-matrix-testing"],
        "scenario": "Đội ngũ kỹ thuật bực bội vì các pull request liên tục bị chặn lại bởi lỗi visual test lệch 0.1% font chữ trên GitHub Actions. Kỹ sư kích hoạt `dex-headless-ui-verification`, chuẩn hóa môi trường runner bằng Docker container chứa font Noto Sans và cờ `--font-render-hinting=none`, đưa tỷ lệ pass test trên CI lên 100%."
    },
    {
        "id": "dex-web-permission-ux",
        "index": 229,
        "group": "Group W",
        "domain": "Browser Extensions & Automation",
        "description": "Design progressive, user-centric browser permission request experiences for Camera, Microphone, Geolocation, Notifications, and Storage with pre-prompt primers and graceful denial recovery. Use when improving permission opt-in rates, eliminating prompt fatigue, or guiding users through browser settings unlock.",
        "purpose": "Thiết kế trải nghiệm yêu cầu quyền hạn trình duyệt (Browser Permissions UX) tiến bộ và lấy người dùng làm trung tâm cho Camera, Microphone, Vị trí (Geolocation), Thông báo và Lưu trữ; sử dụng màn hình giải thích trước (Pre-Prompt Primers), xử lý khéo léo khi người dùng từ chối và hướng dẫn mở lại quyền trong cài đặt trình duyệt.",
        "when_use": [
            "Khi ứng dụng cần truy cập các phần cứng nhạy cảm (Webcam, Mic) hoặc dữ liệu định vị địa lý của người dùng.",
            "Khi tỷ lệ người dùng bấm 'Chặn' quyền quá cao làm tê liệt tính năng chính của ứng dụng.",
            "Khi cần kiểm tra trạng thái quyền bằng Permissions API trước khi thực hiện thao tác gọi thiết bị."
        ],
        "when_not_use": [
            "Khi ứng dụng không sử dụng bất kỳ Web API nào yêu cầu sự đồng ý của người dùng.",
            "Khi thiết lập quyền truy cập cơ sở dữ liệu trên máy chủ backend."
        ],
        "prereqs": "Trình duyệt hỗ trợ `navigator.permissions.query()`, hiểu biết về 3 trạng thái quyền: `'granted'`, `'prompt'`, `'denied'`.",
        "concepts": [
            "Contextual Value Exchange: Chỉ xin quyền ngay tại thời điểm người dùng bấm vào một tính năng cụ thể mang lại giá trị rõ ràng.",
            "Pre-Permission Primer Screen: Giao diện nội bộ giải thích rõ lý do cần quyền và cách thức sử dụng dữ liệu trước khi kích hoạt hộp thoại hệ thống.",
            "Denied State Recovery Flow: Khi quyền bị khóa ở trạng thái 'denied', cung cấp hướng dẫn bằng hình ảnh từng bước giúp người dùng mở lại cài đặt trình duyệt."
        ],
        "steps": [
            "Truy vấn trạng thái quyền hiện tại bằng `navigator.permissions.query({ name: 'camera' })`.",
            "Nếu trạng thái là `'prompt'`, hiển thị modal giải thích lý do trước khi kích hoạt hành động.",
            "Chỉ gọi API thật (`navigator.mediaDevices.getUserMedia`) sau khi người dùng bấm xác nhận trên modal giải thích.",
            "Nếu người dùng từ chối hoặc trạng thái là `'denied'`, hiển thị banner hướng dẫn mở quyền kèm hình ảnh minh họa cho trình duyệt tương ứng.",
            "Lắng nghe sự kiện `permissionStatus.onchange` để tự động kích hoạt tính năng ngay khi người dùng cấp lại quyền."
        ],
        "code_lang": "typescript",
        "code_example": """// Contextual Permission Request Flow
export async function requestCameraAccess(): Promise<MediaStream | null> {
  const status = await navigator.permissions.query({ name: 'camera' as PermissionName });
  
  if (status.state === 'denied') {
    showBrowserSettingsGuide('camera');
    return null;
  }

  if (status.state === 'prompt') {
    const userAgreed = await showPrePromptPrimerModal({
      title: 'Cho phép truy cập Camera để quét mã QR',
      description: 'Hình ảnh chỉ được xử lý trực tiếp trên thiết bị của bạn và không tải lên máy chủ.'
    });
    if (!userAgreed) return null;
  }

  try {
    return await navigator.mediaDevices.getUserMedia({ video: true });
  } catch (err) {
    console.warn('User dismissed native prompt', err);
    return null;
  }
}""",
        "antipatterns": [
            "Vừa vào trang web đã lập tức kích hoạt hộp thoại hỏi xin vị trí hoặc camera của người dùng khiến họ hoảng sợ và bấm 'Chặn'.",
            "Không cung cấp giải pháp thay thế khi người dùng từ chối (ví dụ: không cho nhập địa chỉ thủ công khi họ không muốn chia sẻ GPS).",
            "Hiển thị thông báo lỗi chung chung 'Lỗi thiết bị' khi thực tế là do người dùng chưa cấp quyền truy cập."
        ],
        "quality_gates": [
            "QG-01: Tỷ lệ chấp thuận cấp quyền tăng tối thiểu 40% nhờ màn hình giải thích ngữ cảnh.",
            "QG-02: Luôn có luồng nhập liệu thay thế cho người dùng khi họ từ chối cấp quyền.",
            "QG-03: Giao diện hướng dẫn mở khóa quyền cài đặt hiển thị chính xác theo từng loại trình duyệt (Chrome, Safari, Firefox)."
        ],
        "security": "Chỉ yêu cầu các quyền thực sự cần thiết cho tính năng; ngắt kết nối stream camera/mic ngay lập tức khi người dùng rời khỏi màn hình sử dụng.",
        "deliverables": [
            "Module quản trị quyền hạn người dùng `PermissionManager.ts`.",
            "Component hướng dẫn mở lại cài đặt trình duyệt `PermissionRecoveryGuide.tsx`."
        ],
        "related": ["dex-user-consent-ux", "dex-web-push-permission-flow", "dex-native-device-integration"],
        "scenario": "Ứng dụng họp trực tuyến có tỷ lệ người dùng bị kẹt ở màn hình vào phòng do chặn mic. Kỹ sư kích hoạt `dex-web-permission-ux`, thêm màn hình kiểm tra thiết bị trước khi vào phòng và cung cấp hướng dẫn bấm vào biểu tượng ổ khóa trên thanh địa chỉ để cấp lại quyền, giúp giảm 85% số lượng vé hỗ trợ khách hàng."
    },
    {
        "id": "dex-cross-origin-integration",
        "index": 230,
        "group": "Group W",
        "domain": "Browser Extensions & Automation",
        "description": "Architect secure cross-origin communication between parent applications and embedded iframes using postMessage with origin whitelisting, Content Security Policy frame-ancestors, and COOP/COEP isolation headers. Use when integrating third-party payment widgets, micro-frontend iframes, or cross-domain auth portals.",
        "purpose": "Thiết kế kiến trúc truyền thông xuyên nguồn gốc (Cross-Origin Communication) an toàn giữa ứng dụng cha và các thẻ `<iframe>` nhúng; ứng dụng phương thức `postMessage` với cơ chế kiểm tra danh sách trắng nguồn gốc (Origin Whitelisting), thiết lập chính sách bảo mật CSP `frame-ancestors` và các tiêu đề cô lập COOP/COEP ngăn ngừa tấn công Clickjacking và rò rỉ dữ liệu.",
        "when_use": [
            "Khi nhúng các widget thanh toán từ cổng thanh toán bên thứ ba (như Stripe, VNPay) vào trang web.",
            "Khi xây dựng kiến trúc Micro-Frontend sử dụng các iframe độc lập để cô lập mã nguồn.",
            "Khi truyền nhận token xác thực an toàn giữa các tên miền con khác nhau (Cross-Domain Single Sign-On)."
        ],
        "when_not_use": [
            "Khi các component chạy trong cùng một ứng dụng đơn trang (Single Page App) cùng nguồn gốc (Same-Origin).",
            "Khi giao tiếp thông thường giữa client và server qua các API endpoints."
        ],
        "prereqs": "Kiến thức về Same-Origin Policy (SOP), API `window.postMessage`, các HTTP Headers: `Content-Security-Policy: frame-ancestors`, `Cross-Origin-Opener-Policy`.",
        "concepts": [
            "Strict Target Origin: Luôn chỉ định rõ domain đích khi gọi `postMessage(data, 'https://trusted.com')` thay vì dùng ký tự đại diện `'*'`.",
            "Sender Origin Whitelisting: Kiểm tra nghiêm ngặt `event.origin` trong bộ lắng nghe sự kiện trước khi phân tích cú pháp dữ liệu nhận được.",
            "Frame-Ancestors Protection: Giới hạn danh sách các tên miền được phép nhúng trang web của mình vào iframe để triệt tiêu hoàn toàn nguy cơ Clickjacking."
        ],
        "steps": [
            "Thiết lập header `Content-Security-Policy: frame-ancestors 'self' https://trusted-partner.com` trên máy chủ.",
            "Tạo hợp đồng dữ liệu thông điệp (TypeScript Message Schema) cho các sự kiện truyền qua lại.",
            "Gửi thông điệp từ trang cha sang iframe với tham số `targetOrigin` rõ ràng.",
            "Cài đặt hàm lắng nghe `window.addEventListener('message', handler)` trên iframe có bước kiểm tra `event.origin`.",
            "Kiểm thử bảo mật bằng cách thử gửi thông điệp từ một domain giả mạo để đảm bảo hệ thống từ chối xử lý."
        ],
        "code_lang": "typescript",
        "code_example": """// Secure Cross-Origin Parent-Child Communication
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
});""",
        "antipatterns": [
            "Gọi lệnh `postMessage(data, '*')` với ký tự đại diện, khiến bất kỳ trang web nào nhúng trộm iframe đều có thể đánh cắp payload.",
            "Lắng nghe sự kiện `message` mà không kiểm tra `event.origin`, mở toang cửa cho các cuộc tấn công Cross-Site Scripting (XSS).",
            "Sử dụng lệnh kiểm tra chuỗi lỏng lẻo như `event.origin.includes('mybrand.com')` (kẻ tấn công có thể dùng domain `mybrand.com.attacker.com`)."
        ],
        "quality_gates": [
            "QG-01: 100% các lệnh `postMessage` đều có `targetOrigin` rõ ràng, không có bất kỳ lệnh nào dùng `'*'`. ",
            "QG-02: Tất cả các listener sự kiện đều kiểm tra so khớp chính xác tuyệt đối (`===`) với danh sách trắng nguồn gốc.",
            "QG-03: Header `frame-ancestors` được kiểm tra kích hoạt trên toàn bộ các trang nhạy cảm."
        ],
        "security": "Ngăn chặn các cuộc tấn công Clickjacking, giả mạo lệnh thanh toán và rò rỉ dữ liệu phiên làm việc xuyên nguồn gốc.",
        "deliverables": [
            "Module truyền thông hai chiều xuyên nguồn gốc `CrossOriginBridge.ts`.",
            "Bộ quy tắc cấu hình tiêu đề HTTP CSP `frame-ancestors`."
        ],
        "related": ["dex-web-security-headers", "dex-api-abuse-prevention", "dex-browser-extension-hardening"],
        "scenario": "Tích hợp iframe thanh toán của ngân hàng đối tác vào trang giỏ hàng. Kỹ sư kích hoạt `dex-cross-origin-integration` để thiết lập kênh `postMessage` hai chiều có xác thực domain hai đầu khắt khe, áp dụng CSP `frame-ancestors` và ngăn chặn hoàn toàn nguy cơ kẻ xấu tạo trang giả mạo đánh cắp mã OTP của khách hàng."
    },

    # --- GROUP X: Authorized Reverse Engineering ---
    {
        "id": "dex-pe-elf-structure-inspection",
        "index": 231,
        "group": "Group X",
        "domain": "Authorized Reverse Engineering",
        "description": "Inspect compiled PE (Windows) and ELF (Linux) executable headers, section tables (.text, .rdata, .reloc), dynamic import/export tables, and compiler security flags (ASLR, DEP/NX, SafeSEH, Control Flow Guard). Use when verifying compiled binary provenance, supply chain build integrity, or native dependency linkage. (Strictly authorized/defensive).",
        "purpose": "Kiểm tra và thẩm định cấu trúc tệp thực thi nhị phân PE (Portable Executable trên Windows) và ELF (Executable and Linkable Format trên Linux); phân tích bảng phần tử (.text, .rdata, .reloc), bảng hàm nhập/xuất (Import/Export tables) và các cờ an ninh của trình biên dịch (ASLR, DEP/NX, Control Flow Guard); phục vụ xác minh nguồn gốc xuất xứ của bản dựng và chuỗi cung ứng phần mềm hợp pháp.",
        "when_use": [
            "Khi kiểm toán tính toàn vẹn của tệp thực thi nhị phân trước khi đưa vào môi trường sản xuất của doanh nghiệp.",
            "Khi xác minh xem bản dựng đã được bật đầy đủ các cờ an ninh bảo vệ bộ nhớ của trình biên dịch hay chưa.",
            "Khi điều tra các xung đột liên kết thư viện động (DLL Hell hoặc SO missing dependencies)."
        ],
        "when_not_use": [
            "Khi cố tình dịch ngược phần mềm thương mại có bản quyền nhằm mục đích bẻ khóa (cracking) hoặc vi phạm DRM.",
            "Khi phân tích các tệp kịch bản mã nguồn mở thông thường như Python hay JavaScript."
        ],
        "prereqs": "Tệp thực thi nhị phân được cấp quyền kiểm toán, công cụ dòng lệnh tiêu chuẩn: `readelf`, `objdump`, `dumpbin` hoặc thư viện Python `pefile`.",
        "concepts": [
            "Binary Headers Anatomy: Phân tích DOS Header, PE Signature, COFF Header và Optional Header trên Windows; ELF Header và Program Header Table trên Linux.",
            "Mitigation Flags Verification: Kiểm tra cờ DYNAMIC_BASE (ASLR), NX_COMPAT (DEP), SafeSEH và Control Flow Guard (CFG).",
            "Import Address Table (IAT): Danh sách các hàm API hệ điều hành mà tệp nhị phân phụ thuộc vào khi nạp vào bộ nhớ."
        ],
        "steps": [
            "Trích xuất mã băm SHA-256 của tệp nhị phân để thiết lập chuỗi bằng chứng.",
            "Đọc cấu trúc header của tệp bằng công cụ phân tích tĩnh an toàn.",
            "Rà soát danh sách các section và kiểm tra tỷ lệ entropy để phát hiện trình đóng gói (Packer/Obfuscator).",
            "Kiểm tra danh sách các cờ bảo vệ an ninh bộ nhớ của trình biên dịch.",
            "Lập báo cáo kiểm định nhị phân `BINARY_INSPECTION_REPORT.md`."
        ],
        "code_lang": "python",
        "code_example": """# Inspecting PE Security Flags via pefile (Defensive Audit)
import pefile

def audit_pe_security(filepath: str) -> dict:
    pe = pefile.PE(filepath)
    dll_characteristics = pe.OPTIONAL_HEADER.DllCharacteristics
    
    return {
        "ASLR_ENABLED": bool(dll_characteristics & 0x0040), # IMAGE_DLLCHARACTERISTICS_DYNAMIC_BASE
        "DEP_NX_ENABLED": bool(dll_characteristics & 0x0100), # IMAGE_DLLCHARACTERISTICS_NX_COMPAT
        "GUARD_CF_ENABLED": bool(dll_characteristics & 0x4000), # IMAGE_DLLCHARACTERISTICS_GUARD_CF
        "SECTIONS": [s.Name.decode('utf-8', errors='ignore').strip('\\x00') for s in pe.sections]
    }""",
        "antipatterns": [
            "Thực thi trực tiếp tệp nhị phân không rõ nguồn gốc trong môi trường làm việc chính mà không có sandbox cô lập.",
            "Bỏ qua bước kiểm tra cờ an ninh ASLR/DEP khiến ứng dụng dễ bị tấn công khai thác tràn bộ đệm.",
            "Thay đổi cấu trúc byte của tệp nhị phân mà không có sự ủy quyền chính thức."
        ],
        "quality_gates": [
            "QG-01: Báo cáo kiểm toán ghi nhận đầy đủ mã băm SHA-256 và danh sách cờ an ninh của tệp.",
            "QG-02: 100% các tệp nhị phân sản xuất đều kích hoạt cờ ASLR và DEP/NX.",
            "QG-03: Hoạt động phân tích diễn ra hoàn toàn tĩnh (Static Analysis), không thực thi mã lệnh."
        ],
        "security": "Nghiêm cấm tuyệt đối việc sử dụng kỹ năng để phá hoại, né tránh hệ thống DRM, vi phạm thỏa thuận EULA hoặc tạo phần mềm độc hại.",
        "deliverables": [
            "Báo cáo kiểm định cấu trúc nhị phân `BINARY_INSPECTION_REPORT.md`.",
            "Bảng kiểm tra danh sách hàm nhập/xuất của tệp thực thi."
        ],
        "related": ["dex-binary-inspection", "dex-native-symbol-mapping", "dex-reverse-evidence-chain"],
        "scenario": "Kiểm toán gói cài đặt phần mềm nội bộ của nhà cung cấp bên thứ ba trước khi phát hành cho 10,000 máy trạm ngân hàng. Sử dụng `dex-pe-elf-structure-inspection` để phân tích tệp `.exe`, phát hiện nhà cung cấp quên bật cờ ASLR và yêu cầu họ biên dịch lại với cờ bảo vệ trước khi nghiệm thu."
    },
    {
        "id": "dex-native-symbol-mapping",
        "index": 232,
        "group": "Group X",
        "domain": "Authorized Reverse Engineering",
        "description": "Reconstruct native symbol tables, demangle Itanium/MSVC C++ function signatures, map cross-reference graphs, and correlate debug symbol databases (PDB, DWARF) with stripped binaries. Use when analyzing crash dumps, tracing native exception stack traces, or auditing proprietary driver interfaces. (Strictly authorized/defensive).",
        "purpose": "Khôi phục và ánh xạ bảng biểu tượng bản địa (Native Symbol Mapping); giải mã ngược các chữ ký hàm C++ bị mã hóa (Name Demangling cho chuẩn MSVC và Itanium ABI), xây dựng đồ thị tham chiếu chéo (Cross-Reference Graphs) và đồng bộ cơ sở dữ liệu biểu tượng gỡ lỗi (PDB trên Windows, DWARF trên Linux) với các tệp nhị phân đã bị loại bỏ symbol; phục vụ điều tra lỗi sập ứng dụng (Crash Dump Analysis).",
        "when_use": [
            "Khi phân tích tệp crash dump (`.dmp` hoặc core dump) từ môi trường sản xuất mà stack trace chỉ hiện toàn địa chỉ bộ nhớ thô.",
            "Khi cần điều tra nguyên nhân gây lỗi ngoại lệ bộ nhớ (Memory Access Violation) trong các module native C/C++.",
            "Khi xây dựng máy chủ lưu trữ biểu tượng gỡ lỗi (Symbol Server) cho tổ chức."
        ],
        "when_not_use": [
            "Khi làm việc với các ứng dụng thuần JavaScript/Python không có thành phần native code.",
            "Khi cố tình dịch ngược phần mềm được bảo vệ để đánh cắp thuật toán độc quyền."
        ],
        "prereqs": "Tệp Crash Dump, tệp nhị phân và tệp biểu tượng tương ứng (.pdb hoặc .dbg), công cụ `llvm-cxxfilt`, `c++filt`, `dump_syms`.",
        "concepts": [
            "Mangled Names: Cơ chế trình biên dịch C++ mã hóa kiểu dữ liệu tham số và namespace vào tên hàm nhị phân (ví dụ `?Execute@TaskManager@@QEAAXXZ`).",
            "Symbol Server Integration: Cơ chế tự động tải tệp PDB/DWARF tương ứng dựa trên mã định danh GUID/Age của bản dựng.",
            "Stack Frame Walking: Quá trình phân tích con trỏ khung ngăn xếp để tái hiện lại chuỗi gọi hàm từ thời điểm ứng dụng gặp sự cố."
        ],
        "steps": [
            "Trích xuất mã định danh GUID và Age từ header Debug Directory của tệp thực thi.",
            "Tìm kiếm và nạp tệp PDB/DWARF tương ứng từ kho lưu trữ biểu tượng.",
            "Chuyển đổi các tên hàm bị mã hóa (Mangled Symbols) sang chữ ký hàm C++ đọc được bằng công cụ demangler.",
            "Đối chiếu địa chỉ instruction pointer (IP) từ tệp crash dump với bảng symbol để xác định tên hàm và số dòng mã nguồn.",
            "Xuất ra tài liệu phân tích ngăn xếp gọi hàm (Annotated Stack Trace)."
        ],
        "code_lang": "bash",
        "code_example": """# Demangling C++ Symbols via llvm-cxxfilt
# Input MSVC mangled symbol:
llvm-cxxfilt "?CalculateHash@CryptoManager@Engine@@QEAAHPEBE_K@Z"
# Output:
# public: int __cdecl Engine::CryptoManager::CalculateHash(unsigned char const *, unsigned __int64)

# Input GCC/Clang Itanium mangled symbol:
llvm-cxxfilt "_ZN6Engine13CryptoManager13CalculateHashEPKhm"
# Output:
# Engine::CryptoManager::CalculateHash(unsigned char const*, unsigned long)""",
        "antipatterns": [
            "Xóa bỏ tệp biểu tượng PDB sau khi phát hành phiên bản khiến việc phân tích crash dump trong tương lai trở nên bất khả thi.",
            "Cố tình đoán mò tên hàm dựa trên địa chỉ bộ nhớ mà không sử dụng bảng symbol chính xác.",
            "Sử dụng nhầm tệp PDB của bản dựng khác (sai lệch GUID) dẫn đến báo cáo sai lệch dòng code gây lỗi."
        ],
        "quality_gates": [
            "QG-01: 100% các địa chỉ bộ nhớ trong crash dump được ánh xạ chính xác về tên hàm và tệp nguồn tương ứng.",
            "QG-02: Bảng chữ ký hàm được giải mã hoàn toàn sang cú pháp C++ chuẩn không còn tiền tố mã hóa.",
            "QG-03: Mã GUID của tệp biểu tượng trùng khớp hoàn toàn với bản dựng thực thi."
        ],
        "security": "Bảo vệ các tệp biểu tượng PDB chứa thông tin đường dẫn mã nguồn nội bộ; không công khai ra bên ngoài mà không có chính sách bảo mật.",
        "deliverables": [
            "Bản phân tích Stack Trace đã được ánh xạ biểu tượng `RESOLVED_STACK_TRACE.md`.",
            "Bảng ánh xạ địa chỉ bộ nhớ và hàm C++ tương ứng."
        ],
        "related": ["dex-pe-elf-structure-inspection", "dex-disassembly-cfg-reconstruction", "dex-reverse-evidence-chain"],
        "scenario": "Ứng dụng máy tính để bàn của ngân hàng gặp sự cố crash ngẫu nhiên trên máy khách hàng. Nhận được tệp crash dump 50MB toàn địa chỉ hex. Kỹ sư kích hoạt `dex-native-symbol-mapping`, kết nối PDB của phiên bản đó và giải mã chữ ký C++, xác định chính xác lỗi con trỏ null tại dòng 142 trong tệp `NetworkSocket.cpp`."
    },
    {
        "id": "dex-disassembly-cfg-reconstruction",
        "index": 233,
        "group": "Group X",
        "domain": "Authorized Reverse Engineering",
        "description": "Analyze disassembled machine code (x86-64, ARM64) to reconstruct function basic blocks, control flow graphs (CFG), loop invariants, and calling convention parameter transfers using safe CLI utilities (objdump, llvm-objdump). Use when verifying compiler optimization soundness, investigating crash offsets, or analyzing suspicious binary blobs. (Strictly authorized/defensive).",
        "purpose": "Phân tích mã máy hợp ngữ (Disassembled Assembly x86-64 và ARM64) để tái hiện cấu trúc các khối cơ bản (Basic Blocks), đồ thị luồng điều khiển (Control Flow Graph - CFG), biến bất biến của vòng lặp và quy ước truyền tham số hàm (Calling Conventions); phục vụ xác minh tính đúng đắn của tối ưu hóa trình biên dịch hoặc phân tích các đoạn mã nhị phân đáng ngờ trong môi trường cô lập.",
        "when_use": [
            "Khi trình biên dịch tạo ra mã máy tối ưu hóa bị lỗi (Compiler Optimization Bug) ở cấp độ `-O3`.",
            "Khi cần điều tra nguyên nhân sâu xa của lỗi nhảy địa chỉ không hợp lệ (Invalid Jump / Segfault) tại một offset cụ thể.",
            "Khi thẩm tra tính toàn vẹn của một thư viện nhị phân độc lập không có mã nguồn đi kèm."
        ],
        "when_not_use": [
            "Khi ứng dụng có thể được debug dễ dàng bằng mã nguồn cấp cao (High-level Source Debugging).",
            "Khi cố tình phá hoại các cơ chế bảo vệ phần mềm hoặc tạo ra các công cụ bẻ khóa trái phép."
        ],
        "prereqs": "Kiến thức về kiến trúc tập lệnh x86-64 / ARM64, quy ước gọi hàm (System V AMD64 ABI hoặc Microsoft x64 calling convention), công cụ `objdump` hoặc `llvm-objdump`.",
        "concepts": [
            "Basic Block Partitioning: Chuỗi các lệnh máy tuần tự chỉ có duy nhất một điểm vào ở đầu và một điểm ra ở cuối (kết thúc bằng lệnh nhảy `jmp`, `call` hoặc `ret`).",
            "Control Flow Graph (CFG): Đồ thị có hướng trong đó mỗi nút là một khối cơ bản và mỗi cạnh là một nhánh điều kiện (`jz`, `jnz`).",
            "Parameter Passing Registers: Quy ước truyền tham số qua thanh ghi (x86-64 Windows: RCX, RDX, R8, R9; Linux: RDI, RSI, RDX, RCX, R8, R9)."
        ],
        "steps": [
            "Xuất mã hợp ngữ của hàm mục tiêu bằng `objdump -d --no-show-raw-insn`.",
            "Phân tách mã hợp ngữ thành các Basic Blocks dựa trên các nhãn địa chỉ nhảy.",
            "Xác định các cung điều hướng giữa các khối để dựng đồ thị luồng điều khiển dạng sơ đồ DOT.",
            "Theo dõi luồng dịch chuyển dữ liệu giữa các thanh ghi để tái hiện lại các tham số đầu vào và giá trị trả về.",
            "Tổng hợp thành tài liệu đồ thị luồng điều khiển `CONTROL_FLOW_GRAPH.md`."
        ],
        "code_lang": "bash",
        "code_example": """# Disassembling specific function using llvm-objdump
llvm-objdump --disassemble-symbols=verify_license_token --demangle binary_module.dll

# Extracting basic blocks and branch targets
# 0000000180001000 <verify_license_token>:
# 180001000:   sub    rsp, 0x28
# 180001004:   test   rcx, rcx          ; Check if token pointer is null
# 180001007:   je     18000101b         ; Jump to error block if null
# 180001009:   mov    eax, dword ptr [rcx]
# 18000100b:   cmp    eax, 0x44455801   ; Compare magic header
# 180001010:   jne    18000101b         ; Jump to error block if mismatch
# 180001012:   mov    eax, 1            ; Success return
# 180001017:   add    rsp, 0x28
# 18000101a:   ret
# 18000101b:   xor    eax, eax          ; Error return (0)
# 18000101d:   add    rsp, 0x28
# 18000101f:   ret""",
        "antipatterns": [
            "Cố gắng dịch ngược toàn bộ tệp nhị phân hàng trăm megabyte cùng lúc thay vì tập trung vào hàm nghi vấn.",
            "Nhầm lẫn giữa quy ước gọi hàm của Windows x64 và Linux System V x64 dẫn đến việc xác định sai tham số.",
            "Bỏ qua các lệnh căn chỉnh bộ đệm ngăn xếp (`sub rsp, 0x28`) dẫn đến hiểu sai độ dời của biến cục bộ."
        ],
        "quality_gates": [
            "QG-01: Đồ thị luồng điều khiển xác định đầy đủ tất cả các nhánh điều kiện và điểm thoát của hàm.",
            "QG-02: Quy ước gọi hàm và danh sách thanh ghi tham số được nhận diện chính xác theo ABI của hệ điều hành.",
            "QG-03: Toàn bộ quá trình phân tích được thực hiện bằng các công cụ mã nguồn mở hợp pháp."
        ],
        "security": "Tuyệt đối không sử dụng kỹ năng để tìm kiếm lỗ hổng 0-day nhằm mục đích tấn công hoặc bán thông tin khai thác trái phép.",
        "deliverables": [
            "Sơ đồ đồ thị luồng điều khiển dạng Mermaid hoặc DOT `cfg.mermaid`.",
            "Bản phân tích mã giả (Pseudocode) tái tạo lại logic nghiệp vụ của hàm."
        ],
        "related": ["dex-native-symbol-mapping", "dex-rea-adapter", "dex-binary-diff-regression"],
        "scenario": "Một module tính toán toán học viết bằng C++ gặp lỗi trả về kết quả sai sau khi nâng cấp trình biên dịch Clang lên bản mới nhất. Kỹ sư kích hoạt `dex-disassembly-cfg-reconstruction` để xem mã máy sinh ra ở mức `-O3`, phát hiện trình biên dịch đã tối ưu hóa quá mức làm loại bỏ một bước kiểm tra tràn số nguyên, từ đó đưa ra giải pháp cấu hình pragma thích hợp."
    },
    {
        "id": "dex-managed-assembly-inspection",
        "index": 234,
        "group": "Group X",
        "domain": "Authorized Reverse Engineering",
        "description": "Inspect compiled .NET Common Intermediate Language (CIL/MSIL) and Java/JVM bytecode metadata, type definitions, method signatures, embedded resources, and compiler attributes using ILDasm / javap. Use when auditing managed enterprise plugins, third-party NuGet/Maven dependencies, or cross-platform framework runtimes. (Strictly authorized/defensive).",
        "purpose": "Kiểm toán và phân tích cấu trúc siêu dữ liệu của các tệp mã nguồn trung gian được quản lý: Common Intermediate Language (CIL/MSIL trong .NET) và Java Bytecode (JVM); trích xuất bảng kiểu dữ liệu, chữ ký phương thức, tài nguyên nhúng và các thuộc tính biên dịch bằng các tiện ích chuẩn như `ildasm` và `javap`; phục vụ việc kiểm toán an toàn cho các plugin doanh nghiệp và gói phụ thuộc bên thứ ba.",
        "when_use": [
            "Khi kiểm toán một gói thư viện NuGet (.dll) hoặc Maven (.jar) từ nguồn mở trước khi tích hợp vào dự án tài chính.",
            "Khi cần kiểm tra xem thư viện đã biên dịch có chứa mã độc kích hoạt cửa sau (Backdoor) hoặc các lệnh nạp mã động hay không.",
            "Khi xác minh tính toàn vẹn của các ứng dụng đa nền tảng viết bằng .NET MAUI hoặc Spring Boot."
        ],
        "when_not_use": [
            "Khi làm việc với các ứng dụng nhị phân thuần túy viết bằng C/C++ hoặc Rust (không dùng máy ảo).",
            "Khi cố tình phá hoại các cơ chế bảo vệ phần mềm quản lý bản quyền."
        ],
        "prereqs": "Tệp `.dll` (.NET Assembly) hoặc `.class`/`.jar` (Java), công cụ dòng lệnh `javap` (thuộc JDK) hoặc `ildasm` (thuộc .NET SDK).",
        "concepts": [
            "Managed Metadata Tables: Bảng lưu trữ cấu trúc TypeDef, MethodDef, ParamDef và AssemblyRef trong header tệp.",
            "Intermediate Language Operations: Các lệnh bytecode hướng ngăn xếp (như `ldarg.0`, `callvirt`, `invokevirtual`).",
            "Embedded Resources Audit: Rà soát các tài nguyên tệp được nhúng ẩn bên trong assembly (hình ảnh, cấu hình XML, payload mã hóa)."
        ],
        "steps": [
            "Trích xuất thông tin manifest và siêu dữ liệu phiên bản của assembly bằng `ildasm /metadata` hoặc `javap -verbose`.",
            "Liệt kê tất cả các lớp công khai và phương thức kèm chữ ký tham số.",
            "Tìm kiếm các lệnh nguy hiểm như `Assembly.Load(byte[])` trong .NET hoặc `ClassLoader.defineClass` trong Java.",
            "Trích xuất và kiểm tra tính an toàn của toàn bộ các tài nguyên nhúng (Embedded Resources).",
            "Lập biên bản đánh giá an toàn mã bytecode `BYTECODE_SECURITY_AUDIT.md`."
        ],
        "code_lang": "bash",
        "code_example": """# Inspecting Java Class Bytecode via javap
javap -c -p -constants com.enterprise.auth.TokenValidator.class

# Inspecting .NET Assembly IL via ildasm CLI (or ilverify)
ildasm /text /item:EnterprisePlugin.Security::VerifyToken Plugin.dll

# Verifying managed assembly type safety
ilverify Plugin.dll""",
        "antipatterns": [
            "Nhúng các plugin bên thứ ba vào ứng dụng mà không kiểm tra xem chúng có gọi các API hệ thống nguy hiểm (`System.Diagnostics.Process.Start`) hay không.",
            "Lưu trữ chuỗi kết nối cơ sở dữ liệu hoặc khóa API nhạy cảm bên trong chuỗi hằng số (String Constants) của mã bytecode.",
            "Bỏ qua việc kiểm tra tính tương thích phiên bản khung làm việc (.NET Framework vs .NET Core/8)."
        ],
        "quality_gates": [
            "QG-01: Không phát hiện bất kỳ lệnh nạp mã động không kiểm soát nào trong toàn bộ bytecode của thư viện.",
            "QG-02: Danh sách các phụ thuộc bên ngoài (Assembly References) được lập danh mục đầy đủ và đối chiếu với SBOM.",
            "QG-03: Vượt qua công cụ xác thực an toàn kiểu dữ liệu `ilverify` với 0 lỗi vi phạm."
        ],
        "security": "Phát hiện và ngăn chặn các cuộc tấn công chuỗi cung ứng thông qua việc chèn mã độc vào các gói phụ thuộc mã nguồn mở phổ biến.",
        "deliverables": [
            "Báo cáo kiểm toán mã bytecode `BYTECODE_SECURITY_AUDIT.md`.",
            "Danh mục phụ thuộc và tài nguyên nhúng của assembly."
        ],
        "related": ["dex-dotnet-application-engineering", "dex-jvm-performance-diagnostics", "dex-supply-chain-security"],
        "scenario": "Doanh nghiệp chuẩn bị tích hợp một plugin xử lý PDF dạng .NET DLL từ nhà cung cấp ngoài. Kỹ sư kích hoạt `dex-managed-assembly-inspection`, quét mã CIL bằng `ildasm`, phát hiện plugin có một phương thức ẩn gửi thông tin cấu hình máy chủ về một IP lạ ở nước ngoài, kịp thời ngăn chặn rủi ro rò rỉ dữ liệu doanh nghiệp."
    },
    {
        "id": "dex-electron-artifact-analysis",
        "index": 235,
        "group": "Group X",
        "domain": "Authorized Reverse Engineering",
        "description": "Extract and audit packaged Electron ASAR archives, inspect webPreferences security flags (nodeIntegration, contextIsolation, sandbox), and audit preload script IPC boundary exposures. Use when performing defensive security audits of desktop Electron applications prior to enterprise deployment. (Strictly authorized/defensive).",
        "purpose": "Trích xuất, giải nén và kiểm toán an ninh gói lưu trữ ASAR của ứng dụng máy tính Electron; phân tích các cờ cấu hình bảo mật `webPreferences` (`nodeIntegration`, `contextIsolation`, `sandbox`), rà soát ranh giới kênh truyền thông liên tiến trình (IPC) trong kịch bản tiền nạp (Preload Script); phục vụ kiểm toán phòng thủ ứng dụng trước khi triển khai trong doanh nghiệp.",
        "when_use": [
            "Khi kiểm tra an ninh một ứng dụng desktop phát triển bằng Electron trước khi cài đặt hàng loạt trong mạng nội bộ công ty.",
            "Khi phát hiện nghi vấn ứng dụng Electron bị cấu hình sai khiến trang web bên ngoài có thể gọi lệnh thực thi hệ điều hành.",
            "Khi kiểm toán chuỗi cung ứng các module npm được đóng gói bên trong tệp `app.asar`."
        ],
        "when_not_use": [
            "Khi phát triển các ứng dụng desktop native viết bằng C++/C# hoặc Swift.",
            "Khi cố tình phá hoại hoặc sửa đổi mã nguồn ứng dụng để bẻ khóa bản quyền."
        ],
        "prereqs": "Gói cài đặt Electron (`resources/app.asar`), công cụ dòng lệnh `@electron/asar`, kiến thức về mô hình bảo mật đa tiến trình của Electron.",
        "concepts": [
            "ASAR Archive Structure: Định dạng lưu trữ không nén nối tiếp các tệp tin web và module Node.js kèm một bảng chỉ mục JSON ở đầu tệp.",
            "Context Isolation: Cơ chế cô lập môi trường thực thi của preload script với trang web đích để chống rò rỉ các API Node.js ra ngoài.",
            "IPC Boundary Hardening: Chỉ phơi bày các hàm nghiệp vụ được làm sạch qua `contextBridge.exposeInMainWorld`, không bao giờ phơi bày trực tiếp hàm `ipcRenderer.send`."
        ],
        "steps": [
            "Trích xuất tệp lưu trữ `app.asar` ra thư mục tạm bằng lệnh `asar extract resources/app.asar ./extracted_app`.",
            "Kiểm tra tệp kịch bản tiến trình chính (`main.js`) và rà soát cấu hình `webPreferences` của mọi `BrowserWindow`.",
            "Xác nhận các cờ an ninh: `contextIsolation: true`, `nodeIntegration: false`, `sandbox: true`.",
            "Phân tích tệp `preload.js` để kiểm tra các hàm được phơi bày qua `contextBridge`.",
            "Lập báo cáo kiểm toán bảo mật Electron `ELECTRON_SECURITY_AUDIT.md`."
        ],
        "code_lang": "javascript",
        "code_example": """// Safe Electron Configuration Checklist
// Main Process Window Creation
const mainWindow = new BrowserWindow({
  webPreferences: {
    contextIsolation: true,       // MUST BE TRUE
    nodeIntegration: false,      // MUST BE FALSE
    sandbox: true,               // MUST BE TRUE
    preload: path.join(__dirname, 'preload.js')
  }
});

// Preload Script - Hardened Context Bridge
contextBridge.exposeInMainWorld('electronAPI', {
  sendTelemetry: (data) => {
    // Validate payload schema before forwarding
    if (typeof data.action === 'string') {
      ipcRenderer.send('telemetry:log', { action: data.action });
    }
  }
});""",
        "antipatterns": [
            "Bật cờ `nodeIntegration: true` hoặc tắt cờ `contextIsolation: false`, biến mọi lỗi XSS trên trang web thành lỗi thực thi mã từ xa (RCE).",
            "Phơi bày trực tiếp toàn bộ đối tượng `ipcRenderer` lên `window` thông qua `contextBridge`.",
            "Bỏ qua việc vô hiệu hóa điều hướng tùy tiện (`will-navigate`), cho phép người dùng hoặc mã độc điều hướng cửa sổ tới một trang web độc hại bên ngoài."
        ],
        "quality_gates": [
            "QG-01: 100% các cửa sổ BrowserWindow đều kích hoạt `contextIsolation: true` và `nodeIntegration: false`.",
            "QG-02: Không phơi bày bất kỳ hàm gọi shell thực thi lệnh nào (`child_process.exec`) ra môi trường renderer.",
            "QG-03: Danh sách các gói npm trong `app.asar` được quét đối chiếu với cơ sở dữ liệu lỗ hổng CVE."
        ],
        "security": "Ngăn chặn các cuộc tấn công chiếm quyền điều khiển máy tính người dùng thông qua việc khai thác ứng dụng desktop Electron cấu hình yếu.",
        "deliverables": [
            "Báo cáo kiểm định an ninh Electron `ELECTRON_SECURITY_AUDIT.md`.",
            "Bảng danh mục cấu hình `webPreferences` của toàn bộ các cửa sổ trong ứng dụng."
        ],
        "related": ["dex-electron-security", "dex-javascript-bundle-deobfuscation", "dex-reverse-evidence-chain"],
        "scenario": "Ngân hàng chuẩn bị trang bị một ứng dụng chat nội bộ viết bằng Electron cho nhân viên. Kỹ sư kích hoạt `dex-electron-artifact-analysis`, giải nén tệp `app.asar`, phát hiện phiên bản này vẫn bật `nodeIntegration: true` ở một cửa sổ hỗ trợ kỹ thuật, yêu cầu đội phát hành sửa lại ngay để loại trừ nguy cơ bị hacker chiếm quyền máy trạm qua tin nhắn chat."
    },
    {
        "id": "dex-javascript-sourcemap-recovery",
        "index": 236,
        "group": "Group X",
        "domain": "Authorized Reverse Engineering",
        "description": "Reconstruct original TypeScript/JavaScript source trees from production sourcemap files (.map), analyze bundle composition, and detect inadvertently exposed private API keys or internal test endpoints. Use when auditing public web assets for data leakage or diagnosing production client errors. (Strictly authorized/defensive).",
        "purpose": "Khôi phục lại cây cấu trúc thư mục và mã nguồn TypeScript/JavaScript gốc từ các tệp Source Map (`.map`) vô tình bị để lộ trên môi trường sản xuất; phân tích thành phần gói đóng gói (Bundle Composition), phát hiện rò rỉ khóa bí mật (API Keys), thông tin cấu hình nhạy cảm và các đường dẫn endpoint thử nghiệm nội bộ; phục vụ kiểm toán phòng thủ rò rỉ dữ liệu web.",
        "when_use": [
            "Khi kiểm toán an ninh bề mặt tấn công bên ngoài (External Attack Surface) của website doanh nghiệp.",
            "Khi điều tra một lỗi sập client trên production cần đối chiếu với dòng mã nguồn gốc.",
            "Khi xác minh xem quy trình đóng gói CI/CD có vô tình đẩy các tệp `.map` bí mật lên CDN công khai hay không."
        ],
        "when_not_use": [
            "Khi cố tình khai thác để đánh cắp sở hữu trí tuệ của các tổ chức khác mà không có sự ủy quyền kiểm toán.",
            "Khi phân tích các tệp nhị phân đã biên dịch sang mã máy C++."
        ],
        "prereqs": "Đường dẫn tệp JavaScript đóng gói và tệp `.map` tương ứng, công cụ phục hồi `source-map` hoặc script Python/Node.js.",
        "concepts": [
            "VLQ (Variable-Length Quantity) Encoding: Giải thuật nén ánh xạ từng dòng và cột giữa mã nguồn đã nén (Minified) và mã nguồn gốc.",
            "Source Map Sources Content: Mảng `sourcesContent` bên trong file `.map` thường chứa toàn bộ 100% nội dung mã nguồn gốc chưa nén.",
            "Information Leakage Risk: Tệp sourcemap có thể để lộ chú thích mã nguồn, thông tin tác giả, biến môi trường nhúng và cấu trúc thư mục nội bộ."
        ],
        "steps": [
            "Kiểm tra sự tồn tại của header `SourceMap` hoặc chú thích `//# sourceMappingURL=` trong tệp JS.",
            "Tải và phân tích cú pháp tệp JSON của sourcemap.",
            "Trích xuất mảng `sources` và `sourcesContent` để tái tạo lại toàn bộ cây thư mục mã nguồn gốc.",
            "Quét tự động toàn bộ mã nguồn vừa khôi phục bằng công cụ Secret Scanner (như TruffleHog) để tìm khóa API bị lộ.",
            "Lập biên bản báo cáo rò rỉ và đề xuất biện pháp chặn tệp `.map` trên máy chủ web."
        ],
        "code_lang": "typescript",
        "code_example": """// Defensive Sourcemap Extractor Script
import fs from 'fs';
import path from 'path';

export function extractSourceMap(mapFilePath: string, outputDir: string) {
  const mapData = JSON.parse(fs.readFileSync(mapFilePath, 'utf-8'));
  const { sources, sourcesContent } = mapData;

  if (!sourcesContent) {
    console.warn('Sourcemap contains paths but no sourcesContent.');
    return;
  }

  sources.forEach((sourcePath: string, index: number) => {
    const cleanPath = sourcePath.replace(/^webpack:\\/\\//, '').replace(/^\\.\\//, '');
    const fullOutPath = path.join(outputDir, cleanPath);
    
    fs.mkdirSync(path.dirname(fullOutPath), { recursive: true });
    fs.writeFileSync(fullOutPath, sourcesContent[index] || '', 'utf-8');
  });
  console.log(`Reconstructed ${sources.length} original source files into ${outputDir}`);
}""",
        "antipatterns": [
            "Đẩy tệp sourcemap lên server web công khai mà không thiết lập xác thực hoặc hạn chế IP truy cập.",
            "Nhúng các token bảo mật thật vào tệp cấu hình frontend trong quá trình build rồi dựa vào việc nén mã (minification) để giấu.",
            "Không xóa các tài liệu nhạy cảm hoặc comment nội bộ trước khi xuất bản bản dựng ra công chúng."
        ],
        "quality_gates": [
            "QG-01: Phát hiện và cảnh báo 100% các tệp sourcemap bị phơi bày công khai trên CDN môi trường sản xuất.",
            "QG-02: Không tìm thấy bất kỳ secret key, password hoặc token nhạy cảm nào trong mã nguồn khôi phục được.",
            "QG-03: Cấu hình CI/CD được cập nhật để tự động tách biệt tệp `.map` vào hệ thống theo dõi lỗi nội bộ (Sentry)."
        ],
        "security": "Thông báo ngay lập tức cho đội ngũ an ninh thông tin khi phát hiện khóa API quản trị bị lộ trong tệp sourcemap công khai.",
        "deliverables": [
            "Báo cáo kiểm toán rò rỉ mã nguồn `SOURCEMAP_LEAKAGE_AUDIT.md`.",
            "Script tự động kiểm tra sự tồn tại của sourcemap trên đường ống triển khai."
        ],
        "related": ["dex-javascript-bundle-deobfuscation", "dex-secrets-management", "dex-security-audit"],
        "scenario": "Kiểm toán an ninh website thanh toán trước đợt kiểm tra PCI-DSS. Kỹ sư kích hoạt `dex-javascript-sourcemap-recovery`, phát hiện tệp `main.bundle.js.map` vẫn đang mở công khai trên CDN, chứa toàn bộ mã nguồn TypeScript gốc và một token Stripe Test Secret Key bị bỏ quên trong mã, giúp doanh nghiệp thu hồi token và khóa file map kịp thời."
    },
    {
        "id": "dex-mobile-package-static-audit",
        "index": 237,
        "group": "Group X",
        "domain": "Authorized Reverse Engineering",
        "description": "Perform static security audits on authorized Android APK/AAB packages and iOS IPA bundles, analyzing AndroidManifest.xml exported components, network security configurations, and embedded native libraries (.so). Use when auditing mobile client application releases for compliance and security baselines. (Strictly authorized/defensive).",
        "purpose": "Thực hiện kiểm toán an ninh tĩnh trên các gói cài đặt ứng dụng di động được ủy quyền: Android APK/AAB và iOS IPA; phân tích tệp cấu hình quyền hạn `AndroidManifest.xml`, các thành phần bị phơi bày công khai (Exported Activities/Receivers), chính sách an ninh mạng (Network Security Config) và các thư viện nhị phân nhúng (`.so`); đảm bảo tuân thủ tiêu chuẩn OWASP Mobile Application Security (MASVS).",
        "when_use": [
            "Trước khi phát hành phiên bản mới của ứng dụng ngân hàng hoặc ví điện tử lên Google Play và Apple App Store.",
            "Khi kiểm định an toàn của một ứng dụng di động nội bộ của doanh nghiệp.",
            "Khi rà soát các quyền hạn bị xin thừa thãi gây ảnh hưởng đến quyền riêng tư của khách hàng."
        ],
        "when_not_use": [
            "Khi phân tích ứng dụng của bên thứ ba mà không có sự đồng ý bằng văn bản của chủ sở hữu.",
            "Khi cố tình vượt qua cơ chế chống gian lận (Anti-tampering / Anti-cheat) của game di động."
        ],
        "prereqs": "Gói cài đặt ứng dụng APK/IPA, công cụ dòng lệnh `apktool`, `aapt2`, `keytool` hoặc công cụ phân tích tự động MobSF.",
        "concepts": [
            "Exported Component Risk: Các Activity, Service hoặc Content Provider có thuộc tính `android:exported=\"true\"` mà không có permission bảo vệ có thể bị các ứng dụng độc hại khác trên máy gọi lén.",
            "Cleartext Traffic Policy: Bắt buộc cấu hình `android:usesCleartextTraffic=\"false\"` để cấm hoàn toàn kết nối HTTP không mã hóa.",
            "Certificate Pinning Verification: Kiểm tra cấu hình ghim chứng chỉ số SSL/TLS để ngăn ngừa tấn công bắt gói tin Man-in-the-Middle."
        ],
        "steps": [
            "Giải nén gói cài đặt và trích xuất tệp manifest bằng `apktool d app.apk -o ./decompiled_apk`.",
            "Rà soát danh sách các quyền (`<uses-permission>`) và đánh giá mức độ cần thiết theo nguyên tắc đặc quyền tối thiểu.",
            "Kiểm tra toàn bộ các thẻ `<activity>`, `<service>`, `<receiver>` xem có thành phần nào bị mở `exported=\"true\"` trái phép hay không.",
            "Phân tích tệp `network_security_config.xml` để đảm bảo cấm hoàn toàn giao thức HTTP và chứng chỉ tự ký của người dùng.",
            "Xuất bản báo cáo kiểm toán di động `MOBILE_SECURITY_AUDIT.md`."
        ],
        "code_lang": "xml",
        "code_example": """<!-- Hardened Android Network Security Config -->
<?xml version="1.0" encoding="utf-8"?>
<network-security-config>
    <base-config cleartextTrafficPermitted="false">
        <trust-anchors>
            <!-- Only trust system CAs, disallow user-installed certs -->
            <certificates src="system" />
        </trust-anchors>
    </base-config>
    <domain-config>
        <domain includeSubdomains="true">api.dex.dev</domain>
        <pin-set expiration="2027-01-01">
            <pin digest="SHA-256">k2v657xUM4MpNGnb...=</pin>
        </pin-set>
    </domain-config>
</network-security-config>""",
        "antipatterns": [
            "Đặt `android:exported=\"true\"` cho các Activity quản trị nội bộ hoặc màn hình đổi mật khẩu mà không gắn permission.",
            "Cho phép ứng dụng tin tưởng chứng chỉ cài thêm của người dùng (`<certificates src=\"user\" />`) trong bản dựng sản xuất, mở đường cho việc nghe lén lưu lượng.",
            "Lưu trữ dữ liệu đăng nhập của người dùng vào thẻ nhớ ngoài (External Storage) không có mã hóa."
        ],
        "quality_gates": [
            "QG-01: 100% các thành phần exported đều có permission bảo vệ hoặc được chuyển về `exported=\"false\"`.",
            "QG-02: Cấm hoàn toàn lưu lượng truyền tin dạng bản rõ HTTP (`cleartextTrafficPermitted=\"false\"`).",
            "QG-03: Tuân thủ đầy đủ các tiêu chí bảo mật cấp L1 theo tiêu chuẩn OWASP MASVS."
        ],
        "security": "Bảo vệ thông tin cá nhân và dữ liệu tài chính của người dùng di động khỏi sự can thiệp của các phần mềm gián điệp cài cùng trên thiết bị.",
        "deliverables": [
            "Báo cáo kiểm toán tĩnh ứng dụng di động `MOBILE_SECURITY_AUDIT.md`.",
            "Bản vá cấu hình bảo mật `network_security_config.xml`."
        ],
        "related": ["dex-android-app-architecture", "dex-ios-app-architecture", "dex-reverse-evidence-chain"],
        "scenario": "Kiểm toán ứng dụng ví điện tử trước ngày phát hành chính thức. Kỹ sư kích hoạt `dex-mobile-package-static-audit`, phát hiện một BroadcastReceiver nhận thông báo biến động số dư bị bật `exported=\"true\"` mà không kiểm tra chữ ký gửi, giúp đội phát triển sửa lại thành `exported=\"false\"` để tránh bị các app khác đánh cắp thông báo giao dịch."
    },
    {
        "id": "dex-firmware-metadata-inspection",
        "index": 238,
        "group": "Group X",
        "domain": "Authorized Reverse Engineering",
        "description": "Examine embedded device firmware binary image headers, partition layouts (U-Boot, kernel, rootfs SquashFS), entropy distributions, and hardware architecture metadata using binwalk / dumpimage. Use when auditing authorized IoT device updates, verifying cryptographic signature blocks, or evaluating embedded supply chain integrity. (Strictly authorized/defensive).",
        "purpose": "Kiểm tra và thẩm định siêu dữ liệu hình ảnh nhị phân phần sụn thiết bị nhúng (Firmware Image Inspection); phân tích cấu trúc phân vùng (U-Boot bootloader, Linux kernel, hệ thống tệp SquashFS/UBIFS), đo lường phân bố độ hỗn loạn thông tin (Entropy Distribution) để phát hiện mã hóa/nén và xác minh khối chữ ký điện tử; phục vụ kiểm toán an ninh thiết bị IoT và chuỗi cung ứng nhúng.",
        "when_use": [
            "Khi kiểm toán tính an toàn của một bản cập nhật phần sụn (OTA Firmware Update) cho thiết bị IoT.",
            "Khi xác minh xem nhà sản xuất phần cứng có tuân thủ quy chuẩn mã hóa và bảo mật chữ ký số hay không.",
            "Khi cần kiểm tra danh mục các phần mềm mã nguồn mở có trong hệ thống tệp rootfs của thiết bị nhúng."
        ],
        "when_not_use": [
            "Khi can thiệp vào các thiết bị y tế hoặc hạ tầng công nghiệp đang vận hành trực tiếp.",
            "Khi cố tình trích xuất khóa bản quyền hoặc vượt qua cơ chế Secure Boot của nhà sản xuất nhằm mục đích phi pháp."
        ],
        "prereqs": "Tệp hình ảnh phần sụn nhị phân (.bin, .img), công cụ phân tích `binwalk`, `dumpimage`, `fdisk` hoặc thư viện đồ họa entropy.",
        "concepts": [
            "U-Boot Image Header: Khối 64-byte ở đầu tệp chứa thông tin kiến trúc CPU, hệ điều hành, kiểu nén và mã băm kiểm tra CRC32.",
            "Entropy Analysis: Biểu đồ đo mức độ ngẫu nhiên của các byte từ 0.0 đến 8.0. Vùng có entropy ~8.0 biểu thị dữ liệu bị mã hóa hoặc nén chặt, vùng entropy thấp là mã máy chưa nén hoặc bảng chuỗi.",
            "Root Filesystem Extraction: Quá trình bóc tách hệ thống tệp nén SquashFS để kiểm tra các tệp cấu hình và mật khẩu mặc định."
        ],
        "steps": [
            "Tạo biểu đồ phân bố entropy của tệp firmware để nhận diện các khối dữ liệu nén hoặc mã hóa.",
            "Quét các chữ ký ma thuật (Magic Bytes) bằng công cụ `binwalk firmware.bin`.",
            "Bóc tách phân vùng hệ thống tệp rootfs sang thư mục cách ly.",
            "Rà soát tệp `/etc/shadow` và các tệp cấu hình để phát hiện mật khẩu cứng (Hardcoded Credentials).",
            "Lập báo cáo kiểm toán phần sụn nhúng `FIRMWARE_SECURITY_AUDIT.md`."
        ],
        "code_lang": "bash",
        "code_example": """# Analyzing firmware headers and signatures
binwalk -B firmware_update.bin

# Generating entropy graph to spot encrypted blocks
binwalk -E firmware_update.bin

# Inspecting U-Boot multi-image header
dumpimage -l firmware_update.bin

# Extracting SquashFS filesystem safely
binwalk -e -M firmware_update.bin""",
        "antipatterns": [
            "Nạp thử nghiệm trực tiếp firmware không rõ nguồn gốc vào thiết bị phần cứng thật làm biến thiết bị thành cục gạch (Bricking).",
            "Bỏ qua bước kiểm tra khối chữ ký số ở cuối tệp firmware, cho phép kẻ xấu làm giả bản cập nhật.",
            "Để lộ mật khẩu root mặc định trong tệp shadow của hệ thống tệp thiết bị xuất xưởng."
        ],
        "quality_gates": [
            "QG-01: Báo cáo kiểm toán xác định rõ ràng bảng phân vùng bộ nhớ flash và kiến trúc CPU mục tiêu.",
            "QG-02: Khối chữ ký điện tử mật mã được xác minh tính hợp lệ trước khi phân tích sâu.",
            "QG-03: Không phát hiện bất kỳ mật khẩu tài khoản mặc định hoặc khóa SSH bí mật nào trong rootfs."
        ],
        "security": "Tuân thủ nghiêm ngặt các quy định về an toàn phần cứng; không thực hiện các thao tác có nguy cơ gây cháy nổ hoặc hỏng hóc vĩnh viễn thiết bị thí nghiệm.",
        "deliverables": [
            "Báo cáo kiểm toán phần sụn thiết bị `FIRMWARE_SECURITY_AUDIT.md`.",
            "Sơ đồ phân vùng bộ nhớ và biểu đồ phân tích entropy."
        ],
        "related": ["dex-pe-elf-structure-inspection", "dex-reverse-evidence-chain", "dex-supply-chain-security"],
        "scenario": "Công ty triển khai hệ thống 500 camera giám sát mới. Kỹ sư kích hoạt `dex-firmware-metadata-inspection` để phân tích tệp firmware cập nhật từ hãng sản xuất, phát hiện trong hệ thống tệp SquashFS có một tài khoản telnet bí mật với mật khẩu mặc định `admin1234`, kịp thời yêu cầu hãng vá lỗi trước khi lắp đặt."
    },
    {
        "id": "dex-binary-diff-regression",
        "index": 239,
        "group": "Group X",
        "domain": "Authorized Reverse Engineering",
        "description": "Perform binary-level diffing between build versions to isolate patch regression evidence, compiler flag shifts, and unintended symbol removals using safe utilities (radiff2, diffoscope). Use when analyzing third-party patch modifications, validating hotfix integrity, or verifying reproducible builds. (Strictly authorized/defensive).",
        "purpose": "Thực hiện so sánh sai khác ở cấp độ nhị phân (Binary Diffing) giữa hai phiên bản bản dựng khác nhau; cô lập các bằng chứng thay đổi do bản vá bảo mật (Patch Analysis), phát hiện sự thay đổi ngầm của các cờ trình biên dịch và các biểu tượng bị xóa ngoài ý muốn bằng các tiện ích chuẩn (`radiff2`, `diffoscope`); phục vụ xác minh tính toàn vẹn của bản vá nóng (Hotfix Integrity) và bản dựng tái lập (Reproducible Builds).",
        "when_use": [
            "Khi kiểm tra xem một bản vá khẩn cấp của nhà cung cấp chỉ sửa đúng lỗi đã công bố hay có kèm theo các thay đổi ẩn khác.",
            "Khi điều tra nguyên nhân một hàm bị suy giảm hiệu năng đột ngột sau khi nâng cấp phiên bản trình biên dịch.",
            "Khi thẩm định tính lặp lại từng bit (Bit-for-bit Reproducibility) của sản phẩm phần mềm độc lập."
        ],
        "when_not_use": [
            "Khi có sẵn mã nguồn Git rõ ràng có thể xem diff bằng lệnh `git diff` thông thường.",
            "Khi cố tình so sánh để tìm kiếm lỗ hổng chưa vá (1-day exploit) nhằm mục đích tấn công khai thác."
        ],
        "prereqs": "Hai tệp nhị phân cần so sánh (bản gốc và bản vá), công cụ phân tích diff nhị phân như `diffoscope`, `radiff2` hoặc `llvm-diff`.",
        "concepts": [
            "Structural vs Byte Diff: Phân biệt giữa sai khác do địa chỉ bộ nhớ bị trôi (Relocation Shift) và sai khác thực sự về logic mã máy bên trong thân hàm.",
            "Function Graph Matching: So khớp đồ thị luồng điều khiển của từng hàm giữa hai phiên bản để nhận diện các khối lệnh mới được thêm vào hoặc loại bỏ.",
            "Reproducible Build Verification: Hai lần biên dịch từ cùng một commit mã nguồn phải cho ra hai tệp nhị phân có mã băm SHA-256 hoàn toàn trùng khớp từng byte."
        ],
        "steps": [
            "Tạo mã băm SHA-256 cho cả hai tệp nhị phân `v1.dll` và `v2.dll`.",
            "Chạy công cụ `diffoscope` để bóc tách các tầng cấu trúc sai khác (headers, sections, symbols).",
            "Sử dụng `radiff2 -g` để so sánh đồ thị hàm nhị phân và xác định các hàm có sự thay đổi logic.",
            "Bóc tách mã hợp ngữ của phần thay đổi và phân tích tác động kỹ thuật.",
            "Lập biên bản kết quả so sánh nhị phân `BINARY_DIFF_REPORT.md`."
        ],
        "code_lang": "bash",
        "code_example": """# High-level structural binary difference via diffoscope
diffoscope build_v1.exe build_v2.exe --html diff_report.html

# Function-level binary diff using radiff2
radiff2 -C build_v1.dll build_v2.dll

# Compare specific function graphs and output graphviz dot
radiff2 -g verify_token build_v1.dll build_v2.dll > token_diff.dot""",
        "antipatterns": [
            "Chỉ dùng lệnh so sánh file thông thường `diff` khiến hàng triệu byte địa chỉ con trỏ bị trôi làm tràn ngập màn hình mà không thấy được logic thực sự.",
            "Kết luận bản dựng có mã độc chỉ vì mã băm thay đổi do dấu thời gian biên dịch (Timestamp Difference).",
            "Bỏ qua bước so sánh cấu trúc bảng import/export khi đánh giá bản vá."
        ],
        "quality_gates": [
            "QG-01: Báo cáo diff nhị phân tách biệt rõ ràng giữa sai khác do timestamp/relocation và sai khác logic nghiệp vụ.",
            "QG-02: 100% các hàm có mã máy thay đổi được lập danh mục và giải thích nguyên nhân kỹ thuật.",
            "QG-03: Không có bất kỳ biểu tượng xuất khẩu công khai (Exported Symbols) nào bị biến mất ngoài ý muốn."
        ],
        "security": "Không sử dụng thông tin phân tích diff bản vá bảo mật để tấn công các hệ thống chưa kịp cập nhật bản vá trong thực tế.",
        "deliverables": [
            "Báo cáo sai khác nhị phân trực quan `BINARY_DIFF_REPORT.html`.",
            "Danh mục các hàm bị biến đổi logic và đánh giá rủi ro hồi quy."
        ],
        "related": ["dex-disassembly-cfg-reconstruction", "dex-pe-elf-structure-inspection", "dex-release-reproducibility-audit"],
        "scenario": "Sau khi cập nhật bản vá khẩn cấp của thư viện mã hóa đối tác, hệ thống bị chậm 20%. Kỹ sư kích hoạt `dex-binary-diff-regression` để so sánh nhị phân giữa hai phiên bản DLL, phát hiện nhà cung cấp đã vô tình tắt cờ tối ưu hóa vector AVX2 trong bản dựng mới, giúp gửi phản hồi chính xác để đối tác phát hành bản sửa lỗi trong ngày."
    },
    {
        "id": "dex-reverse-evidence-chain",
        "index": 240,
        "group": "Group X",
        "domain": "Authorized Reverse Engineering",
        "description": "Establish immutable forensic evidence chains for authorized technical audits with cryptographic artifact hashing (SHA-256, BLAKE3), timestamped execution logs, toolchain provenance tracking, and objective observation reporting. Use when documenting security investigations, IP audits, or compliance verifications.",
        "purpose": "Thiết lập chuỗi bằng chứng kỹ thuật pháp lý bất biến (Forensic Evidence Chain) cho các đợt kiểm toán kỹ thuật được ủy quyền; đảm bảo tính toàn vẹn của hiện vật thông qua mã băm mật mã (SHA-256, BLAKE3), nhật ký thực thi có gắn dấu thời gian (Timestamped Execution Logs), truy vết xuất xứ công cụ (Toolchain Provenance) và biên soạn báo cáo quan sát khách quan, loại bỏ các giả định chủ quan.",
        "when_use": [
            "Khi thực hiện điều tra sự cố an ninh thông tin (Incident Response) cần thu thập bằng chứng phục vụ pháp lý.",
            "Khi kiểm toán sở hữu trí tuệ hoặc tranh chấp bản quyền mã nguồn phần mềm.",
            "Khi bàn giao kết quả thẩm định kỹ thuật độc lập cho ban giám đốc hoặc cơ quan chức năng."
        ],
        "when_not_use": [
            "Khi ghi chép nhật ký phát triển hàng ngày trong các buổi họp kỹ thuật nội bộ thông thường.",
            "Khi thực hiện các tác vụ debug tạm thời không cần bảo toàn bằng chứng pháp lý."
        ],
        "prereqs": "Tài liệu ủy quyền kiểm toán bằng văn bản, tiện ích tạo mã băm mật mã (`sha256sum`, `b3sum`), môi trường ghi nhận nhật ký chỉ đọc (Append-only storage).",
        "concepts": [
            "Chain of Custody: Nhật ký ghi nhận chi tiết ai là người tiếp cận hiện vật, vào thời điểm nào, bằng công cụ gì và trạng thái mã băm có bị thay đổi hay không.",
            "Cryptographic Timestamping: Gắn dấu thời gian có ký điện tử để chứng minh bằng chứng tồn tại ở một mốc thời gian xác định và không bị chỉnh sửa hồi tố.",
            "Objective Observation vs Speculation: Chỉ ghi nhận các sự kiện có bằng chứng vật lý đo đạc được (ví dụ: 'Offset 0x100 chứa chuỗi ABC') thay vì phỏng đoán chủ quan."
        ],
        "steps": [
            "Ngay khi tiếp nhận hiện vật kỹ thuật, tính toán mã băm SHA-256 và BLAKE3 và lưu vào sổ cái kiểm toán.",
            "Tạo một bản sao làm việc (Working Copy) và cất giữ bản gốc trong kho lưu trữ chỉ đọc (Read-only Quarantine).",
            "Ghi lại toàn bộ phiên làm việc của terminal (sử dụng công cụ `script` hoặc session recording) kèm phiên bản chính xác của mọi công cụ sử dụng.",
            "Mỗi kết luận đưa ra trong báo cáo phải trích dẫn trực tiếp mã băm của tệp và số dòng/offset của bằng chứng.",
            "Ký số điện tử lên tài liệu báo cáo tổng kết cuối cùng bằng khóa PGP/GPG."
        ],
        "code_lang": "json",
        "code_example": """{
  "$schema": "https://dex.dev/schemas/forensic-evidence.json",
  "auditId": "AUDIT-2026-X10",
  "investigator": "Lead Security Auditor",
  "timestampUtc": "2026-10-22T14:30:00Z",
  "evidenceArtifacts": [
    {
      "filename": "vendor_driver.sys",
      "sizeBytes": 1048576,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "blake3": "af1349b9f5f9a1a6a0404dea36dcc9499bcb25c9adc112b7cc9a93cae41f3262",
      "storageLocation": "vault/evidence/vendor_driver.sys.enc"
    }
  ],
  "toolchain": {
    "llvm-objdump": "18.1.0-win64",
    "diffoscope": "260-linux"
  }
}""",
        "antipatterns": [
            "Thao tác trực tiếp trên tệp hiện vật gốc duy nhất làm thay đổi dấu thời gian truy cập hoặc biến đổi nội dung tệp.",
            "Đưa ra các kết luận khẳng định mang tính quy chụp khi chưa có bằng chứng nhị phân xác thực đối chứng.",
            "Sử dụng các công cụ không rõ nguồn gốc hoặc không ghi lại số hiệu phiên bản của công cụ phân tích."
        ],
        "quality_gates": [
            "QG-01: 100% hiện vật đều có mã băm kép SHA-256 và BLAKE3 được đối chiếu bất biến trước và sau khi phân tích.",
            "QG-02: Báo cáo có đầy đủ nhật ký chuỗi lưu giữ (Chain of Custody) với mốc thời gian UTC chuẩn xác.",
            "QG-03: Tài liệu báo cáo cuối cùng được ký số toàn vẹn bằng chứng chỉ số hợp lệ."
        ],
        "security": "Bảo vệ nghiêm ngặt tính bảo mật của hồ sơ bằng chứng; lưu trữ tệp trong phân vùng mã hóa AES-256 có kiểm soát quyền truy cập.",
        "deliverables": [
            "Sổ cái chuỗi bằng chứng pháp lý `FORENSIC_EVIDENCE_CHAIN.json`.",
            "Báo cáo thẩm định kỹ thuật có ký điện tử `TECHNICAL_EVIDENCE_REPORT.pdf`."
        ],
        "related": ["dex-pe-elf-structure-inspection", "dex-disassembly-cfg-reconstruction", "dex-security-audit"],
        "scenario": "Doanh nghiệp tiến hành thẩm tra độc lập để giải quyết tranh chấp mã nguồn với đối tác gia công. Kỹ sư kích hoạt `dex-reverse-evidence-chain` để tiếp nhận 4 tệp nhị phân, lập mã băm kép, ghi lại toàn bộ log phân tích trong môi trường air-gapped và xuất biên bản bằng chứng đạt chuẩn pháp lý, giúp hai bên giải quyết tranh chấp một cách minh bạch."
    }
]

def build_markdown(meta):
    md = f"""---
name: {meta['id']}
description: {meta['description']}
---

# {meta['id']}

## 1. Purpose & Scope
{meta['purpose']}

## 2. When to Use
"""
    for item in meta['when_use']:
        md += f"- {item}\n"

    md += "\n## 3. When NOT to Use\n"
    for item in meta['when_not_use']:
        md += f"- {item}\n"

    md += f"""
## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** {meta['prereqs']}
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; tuyệt đối không can thiệp trái phép vào hệ thống của bên thứ ba.

## 5. Core Concepts & Taxonomy
"""
    for item in meta['concepts']:
        md += f"- **{item.split(':', 1)[0]}:**{item.split(':', 1)[1] if ':' in item else ''}\n"

    md += "\n## 6. Step-by-Step Execution Workflow\n"
    for i, step in enumerate(meta['steps'], 1):
        md += f"{i}. {step}\n"

    md += f"""
## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```{meta['code_lang']}
{meta['code_example']}
```

## 8. Anti-Patterns & Common Traps
"""
    for item in meta['antipatterns']:
        md += f"- {item}\n"

    md += "\n## 9. Quality Gates & Acceptance Criteria\n"
    for item in meta['quality_gates']:
        md += f"- {item}\n"

    md += f"""
## 10. Security & Safety Boundaries
- {meta['security']}
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Hoạt động phân tích hoàn toàn hợp pháp, minh bạch và có sự ủy quyền chính thức từ chủ sở hữu hệ thống.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
"""
    for item in meta['deliverables']:
        md += f"1. {item}\n"

    md += "\n## 13. Related & Complementary Skills\n"
    for r in meta['related']:
        md += f"- [`{r}`](.agents/skills/{r}/SKILL.md)\n"

    md += f"""
## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
{meta['scenario']}
"""
    return md

def generate_skills():
    if sys.stdout.encoding != "utf-8" and hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    for s in GROUP_W_X_SKILLS:
        skill_dir = os.path.join(SKILLS_DIR, s["id"])
        os.makedirs(skill_dir, exist_ok=True)
        skill_file = os.path.join(skill_dir, "SKILL.md")
        content = build_markdown(s)
        with open(skill_file, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[OK] Generated {s['id']} (Skill {s['index']:03d})")

if __name__ == "__main__":
    generate_skills()
