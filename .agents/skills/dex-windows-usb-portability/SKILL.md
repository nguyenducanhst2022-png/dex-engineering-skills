---
name: dex-windows-usb-portability
description: Design, evaluate, and package zero-install portable Windows applications. Manage local relative pathing, registry-free configuration, runtime bundling, and safe USB execution.
---

# dex-windows-usb-portability

## 1. Purpose & Scope
Thiết kế, xây dựng và kiểm chứng ứng dụng Windows chạy độc lập không cần cài đặt (Zero-Install Portable Applications); quản lý đường dẫn tương đối (Relative Path Resolution), loại bỏ hoàn toàn sự phụ thuộc vào Windows Registry bằng cách chuyển hướng cấu hình về thư mục cục bộ (Local JSON/TOML Settings); nhúng sẵn bộ thư viện phụ thuộc (Static VC++ Runtime Linking hoặc Private Assembly Bundling) và bảo đảm ứng dụng có thể chạy trơn tru trực tiếp từ USB hoặc ổ cứng gắn ngoài.

## 2. When to Use
- Khi phát triển công cụ cứu hộ hệ thống, phần mềm chẩn đoán phần cứng hoặc ứng dụng văn phòng chạy từ USB mà không cần quyền Administrator.
- Khi người dùng muốn chạy nhiều phiên bản ứng dụng độc lập cạnh nhau trên cùng một máy tính mà không xung đột cấu hình.
- Khi cần bảo đảm phần mềm không để lại bất kỳ dữ liệu rác (Zero-Trace) nào trong thư mục `%APPDATA%` hoặc Registry sau khi rút USB.

## 3. When NOT to Use
- Khi ứng dụng bắt buộc phải cài đặt Windows Kernel Driver hoặc Windows Service hệ thống (vốn yêu cầu quyền Admin và đăng ký SCM).
- Khi ứng dụng yêu cầu tích hợp sâu vào hệ điều hành (như Shell Extension Context Menu của Windows Explorer).

## 4. Prerequisites & Input Context
- **Kiến trúc ứng dụng:** Win32, .NET Self-Contained, Rust, hoặc Go cho phép đóng gói độc lập.
- **Môi trường kiểm tra:** Máy tính Windows sạch (Clean VM) chưa cài đặt bất kỳ phiên bản Visual C++ Redistributable nào.

## 5. Core Concepts & Taxonomy
- **Relative Path Anchoring:** Luôn xác định đường dẫn gốc dựa trên vị trí của chính tệp thực thi bằng `GetModuleFileName(nullptr, ...)` thay vì tin tưởng thư mục hiện hành `GetCurrentDirectory()`.
- **Registry Redirection / INI/JSON Storage:** Chuyển toàn bộ các giá trị cấu hình trước đây ghi vào `HKEY_CURRENT_USER\Software\MyApp` sang tệp `settings.json` nằm cùng thư mục ứng dụng.
- **VCRT Static Linking (`/MT` flag):** Biên dịch ứng dụng với cờ `/MT` để nhúng thẳng mã máy của thư viện C Runtime vào tệp `.exe`, giúp ứng dụng chạy được trên máy tính thiếu VC++ Runtime.

## 6. Step-by-Step Execution Workflow
1. Khảo sát mã nguồn và thay thế toàn bộ các lệnh đọc ghi Registry bằng module quản lý tệp cấu hình cục bộ.
2. Cấu hình trình biên dịch bật cờ liên kết tĩnh C Runtime: `/MT` trên MSVC hoặc cấu hình Self-Contained trong `.NET` (`dotnet publish -r win-x64 --self-contained true`).
3. Viết hàm tiện ích tính toán đường dẫn tuyệt đối cho các tệp phụ trợ dựa trên đường dẫn tệp `.exe` đang chạy.
4. Đóng gói toàn bộ các DLL phụ trợ cần thiết trong cùng thư mục với tệp thực thi.
5. Chạy thử nghiệm trên một máy ảo Windows sạch 100% không có kết nối internet và không cài phần mềm phụ trợ.
6. Kiểm tra lại Registry và thư mục `%APPDATA%` để khẳng định ứng dụng không để lại dấu vết dữ liệu.

## 7. Concrete Examples
### Ham lay duong dan tuyet doi an toan dua tren vi tri file EXE trong C++:
```cpp
#include <windows.h>
#include <string>
#include <filesystem>
#include <iostream>

namespace fs = std::filesystem;

fs::path get_app_directory() {
    wchar_t buffer[MAX_PATH];
    GetModuleFileNameW(nullptr, buffer, MAX_PATH);
    return fs::path(buffer).parent_path();
}

fs::path get_portable_config_path() {
    // Luon luu tru config tai thu muc chua ung dung
    return get_app_directory() / L"settings.json";
}

int main() {
    fs::path config_file = get_portable_config_path();
    std::wcout << L"Portable config location: " << config_file.wstring() << std::endl;

    if (!fs::exists(config_file)) {
        std::wcout << L"Initializing first-run portable settings..." << std::endl;
        // Ghi file cau hinh mac dinh
    }
    return 0;
}
```

## 8. Anti-Patterns & Common Traps
- **Relying on GetCurrentDirectory():** Dùng thư mục hiện hành để tìm file dữ liệu khiến ứng dụng bị sập khi người dùng mở ứng dụng qua Shortcut hoặc qua ứng dụng khác.
- **Dynamic VC++ Linking (/MD):** Dùng cờ `/MD` khiến ứng dụng không thể khởi động trên máy khách với thông báo lỗi thiếu `MSVCP140.dll` hoặc `VCRUNTIME140.dll`.
- **Writing to C:\Program Files at Runtime:** Cố ghi file cấu hình vào cùng thư mục khi ứng dụng bị người dùng copy vào `Program Files` mà không kiểm tra quyền ghi.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Ứng dụng khởi chạy thành công trên máy ảo Windows sạch không cài VC++ Redistributable.
- **QG-02**: Không tạo ra bất kỳ khóa mới nào trong Windows Registry (`HKCU` hoặc `HKLM`).
- **QG-03**: Tất cả các đường dẫn tài nguyên nội bộ đều được giải quyết chuẩn xác bất kể ổ đĩa USB mang ký tự nào (D:, E:, F:).

## 10. Security & Safety Boundaries
- Kiểm tra thư mục chạy có quyền ghi hay không; nếu chạy trên USB chỉ đọc (Read-only CD/USB), chuyển hướng cấu hình an toàn về thư mục tạm trong RAM.

## 11. Platform Adapters
- **Runtimes**: C++20 (/MT), .NET 8 Self-Contained SingleFile, Rust target `x86_64-pc-windows-msvc`.

## 12. Deliverables & Output Artifacts
- Lớp quản lý đường dẫn di động (`portable_paths.hpp` / `paths.rs`).
- Bộ kiểm tra tự động phát hiện rò rỉ Registry và AppData.

## 13. Related & Complementary Skills
dex-windows-code-signing-installer, dex-windows-service-recovery, dex-windows-app-startup-profiling

## 14. Realistic Usage Example
```powershell
# Kiem tra cac DLL phu thuoc cua ung dung bang dumpbin
dumpbin /dependents .\DEXApp.exe
```
