---
name: dex-electron-artifact-analysis
description: Extract and audit packaged Electron ASAR archives, inspect webPreferences security flags (nodeIntegration, contextIsolation, sandbox), and audit preload script IPC boundary exposures. Use when performing defensive security audits of desktop Electron applications prior to enterprise deployment. (Strictly authorized/defensive).
---

# dex-electron-artifact-analysis

## 1. Purpose & Scope
Trích xuất, giải nén và kiểm toán an ninh gói lưu trữ ASAR của ứng dụng máy tính Electron; phân tích các cờ cấu hình bảo mật `webPreferences` (`nodeIntegration`, `contextIsolation`, `sandbox`), rà soát ranh giới kênh truyền thông liên tiến trình (IPC) trong kịch bản tiền nạp (Preload Script); phục vụ kiểm toán phòng thủ ứng dụng trước khi triển khai trong doanh nghiệp.

## 2. When to Use
- Khi kiểm tra an ninh một ứng dụng desktop phát triển bằng Electron trước khi cài đặt hàng loạt trong mạng nội bộ công ty.
- Khi phát hiện nghi vấn ứng dụng Electron bị cấu hình sai khiến trang web bên ngoài có thể gọi lệnh thực thi hệ điều hành.
- Khi kiểm toán chuỗi cung ứng các module npm được đóng gói bên trong tệp `app.asar`.

## 3. When NOT to Use
- Khi phát triển các ứng dụng desktop native viết bằng C++/C# hoặc Swift.
- Khi cố tình phá hoại hoặc sửa đổi mã nguồn ứng dụng để bẻ khóa bản quyền.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Gói cài đặt Electron (`resources/app.asar`), công cụ dòng lệnh `@electron/asar`, kiến thức về mô hình bảo mật đa tiến trình của Electron.
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; tuyệt đối không can thiệp trái phép vào hệ thống của bên thứ ba.

## 5. Core Concepts & Taxonomy
- **ASAR Archive Structure:** Định dạng lưu trữ không nén nối tiếp các tệp tin web và module Node.js kèm một bảng chỉ mục JSON ở đầu tệp.
- **Context Isolation:** Cơ chế cô lập môi trường thực thi của preload script với trang web đích để chống rò rỉ các API Node.js ra ngoài.
- **IPC Boundary Hardening:** Chỉ phơi bày các hàm nghiệp vụ được làm sạch qua `contextBridge.exposeInMainWorld`, không bao giờ phơi bày trực tiếp hàm `ipcRenderer.send`.

## 6. Step-by-Step Execution Workflow
1. Trích xuất tệp lưu trữ `app.asar` ra thư mục tạm bằng lệnh `asar extract resources/app.asar ./extracted_app`.
2. Kiểm tra tệp kịch bản tiến trình chính (`main.js`) và rà soát cấu hình `webPreferences` của mọi `BrowserWindow`.
3. Xác nhận các cờ an ninh: `contextIsolation: true`, `nodeIntegration: false`, `sandbox: true`.
4. Phân tích tệp `preload.js` để kiểm tra các hàm được phơi bày qua `contextBridge`.
5. Lập báo cáo kiểm toán bảo mật Electron `ELECTRON_SECURITY_AUDIT.md`.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```javascript
// Safe Electron Configuration Checklist
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
});
```

## 8. Anti-Patterns & Common Traps
- Bật cờ `nodeIntegration: true` hoặc tắt cờ `contextIsolation: false`, biến mọi lỗi XSS trên trang web thành lỗi thực thi mã từ xa (RCE).
- Phơi bày trực tiếp toàn bộ đối tượng `ipcRenderer` lên `window` thông qua `contextBridge`.
- Bỏ qua việc vô hiệu hóa điều hướng tùy tiện (`will-navigate`), cho phép người dùng hoặc mã độc điều hướng cửa sổ tới một trang web độc hại bên ngoài.

## 9. Quality Gates & Acceptance Criteria
- QG-01: 100% các cửa sổ BrowserWindow đều kích hoạt `contextIsolation: true` và `nodeIntegration: false`.
- QG-02: Không phơi bày bất kỳ hàm gọi shell thực thi lệnh nào (`child_process.exec`) ra môi trường renderer.
- QG-03: Danh sách các gói npm trong `app.asar` được quét đối chiếu với cơ sở dữ liệu lỗ hổng CVE.

## 10. Security & Safety Boundaries
- Ngăn chặn các cuộc tấn công chiếm quyền điều khiển máy tính người dùng thông qua việc khai thác ứng dụng desktop Electron cấu hình yếu.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Hoạt động phân tích hoàn toàn hợp pháp, minh bạch và có sự ủy quyền chính thức từ chủ sở hữu hệ thống.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Báo cáo kiểm định an ninh Electron `ELECTRON_SECURITY_AUDIT.md`.
1. Bảng danh mục cấu hình `webPreferences` của toàn bộ các cửa sổ trong ứng dụng.

## 13. Related & Complementary Skills
- [`dex-electron-security`](.agents/skills/dex-electron-security/SKILL.md)
- [`dex-javascript-bundle-deobfuscation`](.agents/skills/dex-javascript-bundle-deobfuscation/SKILL.md)
- [`dex-reverse-evidence-chain`](.agents/skills/dex-reverse-evidence-chain/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Ngân hàng chuẩn bị trang bị một ứng dụng chat nội bộ viết bằng Electron cho nhân viên. Kỹ sư kích hoạt `dex-electron-artifact-analysis`, giải nén tệp `app.asar`, phát hiện phiên bản này vẫn bật `nodeIntegration: true` ở một cửa sổ hỗ trợ kỹ thuật, yêu cầu đội phát hành sửa lại ngay để loại trừ nguy cơ bị hacker chiếm quyền máy trạm qua tin nhắn chat.
