---
name: dex-tauri-desktop-integration
description: Build lightweight, high-performance desktop apps using Tauri v2, Rust backend commands, strict permission capabilities, OS system tray, native window controls, and minimal memory footprint. Use when developing memory-efficient desktop applications.
---

# dex-tauri-desktop-integration

## 1. Purpose & Scope
Thiết kế và phát triển các ứng dụng máy tính đa nền tảng (Desktop Apps) siêu nhẹ và an toàn cao bằng Tauri v2; tích hợp backend bằng ngôn ngữ Rust với giao diện frontend web hiện đại; xây dựng các lệnh gọi an toàn (`#[tauri::command]`), áp dụng hệ thống phân quyền chi tiết (Tauri v2 Permissions & Capabilities), tích hợp System Tray, menu hệ điều hành và tối ưu hóa mức tiêu thụ bộ nhớ (RAM < 50MB, kích thước tệp cài đặt < 15MB).

## 2. When to Use
- Khi cần xây dựng ứng dụng desktop có hiệu năng cao, khởi động tức thì và tốn ít RAM hơn nhiều so với Electron.
- Khi ứng dụng cần thực hiện các tác vụ tính toán nặng, tương tác phần cứng hoặc mật mã học trực tiếp bằng Rust.
- Khi cần tuân thủ mô hình bảo mật Least Privilege thông qua hệ thống capability của Tauri v2.

## 3. When NOT to Use
- Ứng dụng phụ thuộc nặng nề vào các module C++ Node.js cũ chưa thể port sang Rust.
- Ứng dụng di động thuần túy (dùng `dex-android-app-architecture` hoặc `dex-ios-app-architecture`).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Mã nguồn Frontend (React, Vue, Svelte hoặc HTML tĩnh).
- Danh sách các hàm hệ thống cần truy cập (File system, Dialog, Shell, Notifications).
- Cấu hình cửa sổ trong `tauri.conf.json`.
- **Điều kiện tiên quyết**:
- Rust toolchain (cargo, rustc 1.75+) và Node.js/pnpm cài đặt sẵn.
- Thư viện WebKit/WebView2 trên hệ điều hành mục tiêu.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- **OS Native Webview Reuse**: Khác với Electron đóng gói cả trình duyệt Chromium nặng 150MB, Tauri tái sử dụng Webview có sẵn của OS (WebView2 trên Windows, WebKit trên macOS/Linux).
- **Type-Safe IPC via Serde**: Giao tiếp giữa JS và Rust được serialize/deserialize tự động và kiểm tra kiểu chặt chẽ thông qua thư viện `serde`.
- **Tauri v2 Capability System**: Mọi truy cập vào filesystem hay network đều phải được cấp phép tường minh qua các tệp JSON trong thư mục `src-tauri/capabilities/`.
- **Quy tắc quyết định kỹ thuật**:
- **Tách Biệt Luồng Tính Toán Nặng Trong Rust**: Các tác vụ tiêu tốn CPU trong Rust command phải chạy trên thread pool (`tauri::async_runtime::spawn_blocking`), không làm block main loop.
- **Không Mở Khóa Quyền Hạn Tùy Tiện (No Broad Capabilities)**: Chỉ cấp quyền đọc/ghi trên các đường dẫn cụ thể (ví dụ: `$APPDATA/*`), không cấp quyền truy cập toàn bộ đĩa cứng (`fs:allow-all`).
- **Xử Lý Lỗi Tường Minh Bằng `Result<T, E>`**: Mọi Tauri command phải trả về `Result<T, String>` để frontend có thể bắt lỗi qua Promise rejection.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Giao diện bị đơ khi Rust command xử lý file lớn**: Do chạy đồng bộ trên main thread -> Khắc phục: Đánh dấu lệnh bằng `async` hoặc spawn blocking task.
- **Frontend gọi lệnh bị từ chối quyền (Permission Denied)**: Quên khai báo quyền trong capability file của Tauri v2 -> Khắc phục: Khai báo quyền tương ứng trong `src-tauri/capabilities/default.json`.

## 6. Step-by-Step Execution Workflow
1. Khởi tạo dự án Tauri v2: `pnpm create tauri-app`.
2. Cấu hình định danh ứng dụng và bảo mật cửa sổ trong `src-tauri/tauri.conf.json`.
3. Viết các command trong Rust (`#[tauri::command]`) với tham số được validate chặt chẽ.
4. Đăng ký commands vào trình khởi tạo `tauri::Builder` qua `.invoke_handler()`.
5. Cấu hình tệp capabilities cấp quyền tối thiểu cho các plugin (fs, dialog, notification).
6. Gọi command từ frontend TypeScript: `import { invoke } from '@tauri-apps/api/core'`.
7. Đóng gói ứng dụng cho hệ điều hành mục tiêu: `pnpm tauri build` (sinh file MSI/NSIS trên Windows, DMG trên macOS).

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```rust
// src-tauri/src/main.rs
use tauri::Manager;

#[tauri::command]
async fn process_large_data(filepath: String) -> Result<usize, String> {
    // Chạy tác vụ nặng trên thread pool không làm treo giao diện
    tokio::task::spawn_blocking(move || {
        let content = std::fs::read_to_string(&filepath)
            .map_err(|e| format!("Failed to read file: {}", e))?;
        Ok(content.lines().count())
    })
    .await
    .map_err(|e| format!("Task join error: {}", e))?
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![process_large_data])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

### Lệnh xác minh & thực thi:
- Kiểm tra build Rust backend: `cargo check --manifest-path src-tauri/Cargo.toml`
- Chạy ứng dụng chế độ phát triển: `pnpm tauri dev`
- Đóng gói ứng dụng sản xuất: `pnpm tauri build`
- Kiểm tra dung lượng RAM: Đo Task Manager / Activity Monitor khi app khởi động (phải < 50MB)

## 8. Anti-Patterns & Common Traps
- **Cho phép Frontend chạy lệnh Shell tùy ý (`shell:allow-execute`)**: Mở ra nguy cơ bảo mật nghiêm trọng.
- **Lưu trữ dữ liệu lớn trong bộ nhớ frontend JS**: Nên lưu và xử lý trực tiếp trong bộ nhớ của Rust engine.
- **Bỏ qua lỗi trong Rust bằng `.unwrap()`**: Khiến toàn bộ ứng dụng desktop crash bất ngờ khi có lỗi I/O.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Bộ nhớ RAM tiêu thụ khi khởi động dưới 60MB.
- QG-07: Tệp capabilities chỉ cấp quyền hạn tối thiểu (Principle of Least Privilege).
- QG-11: Ứng dụng đóng gói thành công thành file cài đặt độc lập (Installer).
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi deploy.

## 10. Security & Safety Boundaries
- Kích hoạt Content Security Policy (CSP) trong cấu hình Tauri.
- Sử dụng chữ ký số mã nguồn (Code Signing) cho bộ cài đặt binary.
- Không bao giờ lưu trữ hardcoded secret hoặc cấp quyền quá mức (over-permissioned IAM).

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Môi trường Mobile & Desktop**: Hỗ trợ Android (Kotlin/Gradle), iOS (Swift/Xcode), Electron (Node.js/Chromium), Tauri (Rust/WebKit).

## 12. Deliverables & Output Artifacts
- Dự án Tauri v2 với cấu trúc Rust backend và Frontend chuẩn hóa.
- Tệp cấu hình capabilities và permissions.
- Bộ cài đặt ứng dụng nhẹ (<20MB).

## 13. Related & Complementary Skills
- `dex-electron-security`: So sánh mô hình bảo mật giữa Electron và Tauri.
- `dex-desktop-ipc-design`: Xây dựng giao thức truyền tin type-safe giữa Frontend và Rust.
- `dex-windows-packaging`: Đóng gói và phân phối ứng dụng cho môi trường Windows.

## 14. Realistic Usage Example
### Tình huống thực tế:
Một công ty muốn xây dựng công cụ đọc log file gigabyte cho lập trình viên. Thay vì dùng Electron ngốn 400MB RAM, họ sử dụng `dex-tauri-desktop-integration`. Backend Rust sử dụng memory-mapped files (`memmap2`) để đọc file log siêu tốc, trả kết quả phân trang về giao diện Svelte qua Tauri command. Ứng dụng khởi động trong 0.1 giây, tiêu tốn chỉ 35MB RAM và kích thước file cài đặt chỉ 8MB.
