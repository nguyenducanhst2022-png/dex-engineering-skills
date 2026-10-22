---
name: dex-electron-security
description: Harden Electron desktop applications by enforcing process isolation, contextIsolation, nodeIntegration disablement, sandboxing, minimal contextBridge IPC APIs, and CSP. Use when building, auditing, or securing Electron desktop apps.
---

# dex-electron-security

## 1. Purpose & Scope
Thiết lập kiến trúc bảo mật kiên cố (Security Hardening) cho ứng dụng máy tính đa nền tảng viết bằng Electron; triệt tiêu các bề mặt tấn công Remote Code Execution (RCE) và Cross-Site Scripting (XSS); cấu hình nghiêm ngặt: vô hiệu hóa `nodeIntegration`, kích hoạt `contextIsolation`, bật OS Sandboxing, chỉ phơi bày các API tối thiểu qua `contextBridge`, áp dụng Content Security Policy (CSP) chặt chẽ và lọc an toàn các liên kết ngoài / window navigation.

## 2. When to Use
- Khi bắt đầu xây dựng ứng dụng desktop mới bằng Electron (Slack, VS Code, Notion style app).
- Khi ứng dụng Electron cần render nội dung web từ xa hoặc nội dung người dùng tải lên (Untrusted User Content).
- Khi kiểm toán an ninh phát hiện lỗ hổng cho phép kẻ tấn công thực thi mã shell từ giao diện Renderer.

## 3. When NOT to Use
- Xây dựng ứng dụng desktop nhẹ bằng Rust và webview hệ thống (dùng `dex-tauri-desktop-integration`).
- Thiết kế kiến trúc IPC thuần túy không tập trung vào bảo mật Electron (dùng `dex-desktop-ipc-design`).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Cấu hình BrowserWindow và webPreferences trong mã nguồn Main process.
- Danh sách các hàm Node.js/OS mà Renderer thực sự cần truy cập.
- Quy tắc Content Security Policy (CSP).
- **Điều kiện tiên quyết**:
- Electron phiên bản 28+ (hỗ trợ sandbox và context isolation mặc định).
- Công cụ kiểm tra bảo mật tĩnh (Electronegativity / ESLint plugin Electron).

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- **Context Isolation Invariance**: Tách biệt hoàn toàn ngữ cảnh JavaScript của Renderer (trang web) khỏi ngữ cảnh của Preload script; ngăn chặn mã độc web ghi đè hoặc truy cập các hàm nguyên bản của Node.js.
- **Privilege Separation via IPC**: Renderer không bao giờ được phép trực tiếp gọi `fs.readFile()` hay `child_process.exec()`; Renderer chỉ được gửi thông điệp yêu cầu Main process thực thi sau khi đã kiểm tra quyền hạn.
- **Strict Preload Surface Minimization**: Chỉ truyền các hàm wrapper cụ thể qua `contextBridge.exposeInMainWorld`, không bao giờ phơi bày trực tiếp toàn bộ `ipcRenderer`.
- **Quy tắc quyết định kỹ thuật**:
- **`nodeIntegration: false` Bắt Buộc**: Tuyệt đối không bật Node integration trong Renderer process.
- **`contextIsolation: true` Bắt Buộc**: Không bao giờ tắt context isolation trong bất kỳ cửa sổ nào.
- **Không Expose `ipcRenderer.send` Trực Tiếp**: Cấm expose hàm gửi IPC tự do; bắt buộc validate channel và payload trong preload wrapper.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Lỗ hổng XSS dẫn tới chiếm toàn bộ máy tính (Full RCE)**: Do bật `nodeIntegration: true`, kẻ tấn công chèn mã `<script>require('child_process').exec('calc')</script>` -> Khắc phục: Tắt `nodeIntegration`, bật `contextIsolation` và áp dụng CSP chặn `unsafe-inline`.
- **Renderer mở trang web lừa đảo chiếm quyền cửa sổ**: Do không chặn sự kiện `will-navigate` -> Khắc phục: Chặn toàn bộ navigation sang domain lạ trong Main process.

## 6. Step-by-Step Execution Workflow
1. Cấu hình `webPreferences` trong Main process: tắt `nodeIntegration`, bật `contextIsolation`, bật `sandbox`.
2. Thiết lập header Content Security Policy (CSP) chặn thực thi script nội dòng (`unsafe-eval`, `unsafe-inline`).
3. Xây dựng `preload.ts`: Định nghĩa các API an toàn và xuất ra qua `contextBridge.exposeInMainWorld('electronAPI', {...})`.
4. Lắng nghe IPC trong Main process bằng `ipcMain.handle()`: Kiểm tra kỹ lưỡng tham số truyền vào (Input Validation bằng Zod).
5. Đăng ký hook bảo vệ cửa sổ: Chặn `will-navigate` và `setWindowOpenHandler` đối với mọi URL không nằm trong whitelist.
6. Tắt tính năng tự động mở DevTools trong môi trường production.
7. Quét mã nguồn bằng công cụ phân tích bảo mật Electronegativity.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```typescript
// main.ts - Secure BrowserWindow Initialization
import { app, BrowserWindow, shell } from 'electron';
import path from 'path';

function createWindow() {
  const mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      sandbox: true,
      preload: path.join(__dirname, 'preload.js'),
    },
  });

  // Chặn mở cửa sổ mới trái phép
  mainWindow.webContents.setWindowOpenHandler(({ url }) => {
    if (url.startsWith('https://trustedsite.com')) {
      shell.openExternal(url); // Mở trên trình duyệt ngoài an toàn
    }
    return { action: 'deny' };
  });

  mainWindow.loadFile('index.html');
}

// preload.ts - Minimal Secure Bridge
import { contextBridge, ipcRenderer } from 'electron';

contextBridge.exposeInMainWorld('secureDesktopAPI', {
  saveDocument: (content: string) => {
    if (typeof content !== 'string' || content.length > 10_000_000) {
      throw new Error('Invalid content');
    }
    return ipcRenderer.invoke('document:save', content);
  },
});
```

### Lệnh xác minh & thực thi:
- Quét lỗ hổng an ninh Electron: `npx @doyensec/electronegativity -i src/`
- Kiểm tra CSP trong header cửa sổ: Kiểm tra log console không có cảnh báo CSP violation
- Test thử nghiệm chèn mã độc: Mở Renderer console gõ `window.require` (phải trả về `undefined`)

## 8. Anti-Patterns & Common Traps
- **Expose toàn bộ `ipcRenderer` qua contextBridge**: `contextBridge.exposeInMainWorld('electron', ipcRenderer)` hoàn toàn vô hiệu hóa mục đích bảo vệ của preload.
- **Cho phép `webSecurity: false` để né lỗi CORS**: Khiến ứng dụng dễ bị tấn công đánh cắp dữ liệu local files.
- **Không validate tham số IPC ở Main Process**: Tin tưởng mù quáng payload gửi từ Renderer.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Cấu hình `webPreferences` có `contextIsolation: true` và `nodeIntegration: false`.
- QG-07: Electronegativity không phát hiện bất kỳ lỗ hổng mức HIGH hay CRITICAL nào.
- QG-10: Mọi URL mở ngoài đều đi qua `shell.openExternal` với whitelist chặt chẽ.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi deploy.

## 10. Security & Safety Boundaries
- Tuyệt đối cấm load các URL HTTP không bảo mật vào BrowserWindow.
- Vô hiệu hóa tính năng `experimentalFeatures` và `allowRunningInsecureContent`.
- Không bao giờ lưu trữ hardcoded secret hoặc cấp quyền quá mức (over-permissioned IAM).

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Môi trường Mobile & Desktop**: Hỗ trợ Android (Kotlin/Gradle), iOS (Swift/Xcode), Electron (Node.js/Chromium), Tauri (Rust/WebKit).

## 12. Deliverables & Output Artifacts
- Tệp `main.ts` và `preload.ts` được bảo vệ kiên cố.
- Cấu hình Content Security Policy (CSP).
- Báo cáo kiểm toán Electronegativity sạch lỗi.

## 13. Related & Complementary Skills
- `dex-desktop-ipc-design`: Thiết kế schema truyền tin IPC hai chiều.
- `dex-tauri-desktop-integration`: Đánh giá phương án thay thế nhẹ hơn bằng Tauri.
- `dex-desktop-update-delivery`: Ký số và cập nhật an toàn cho file cài đặt Electron.

## 14. Realistic Usage Example
### Tình huống thực tế:
Một công ty Fintech phát triển ứng dụng giao dịch tài chính bằng Electron. Kỹ sư bảo mật áp dụng `dex-electron-security`, rà soát thấy dự án cũ đang bật `nodeIntegration: true`. Kỹ sư tiến hành refactor: tắt node integration, bật context isolation, viết lại preload script chỉ phơi bày 4 hàm nghiệp vụ có kiểm tra kiểu dữ liệu qua contextBridge, thiết lập CSP chặn script từ bên ngoài, ngăn chặn hoàn toàn nguy cơ RCE nếu chẳng may có lỗ hổng XSS trong giao diện.
