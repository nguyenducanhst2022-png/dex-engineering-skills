---
name: dex-win32-dpi-multi-monitor-layout
description: Design, implement, and verify Per-Monitor V2 high-DPI awareness for Windows desktop applications. Handle dynamic scaling, non-client metrics, and coordinate translation across mixed-DPI displays.
---

# dex-win32-dpi-multi-monitor-layout

## 1. Purpose & Scope
Thiết kế, xử lý và kiểm chứng tính năng thích ứng độ phân giải cao theo từng màn hình (Per-Monitor V2 High-DPI Awareness) cho ứng dụng desktop Windows (Win32, MFC, WPF, WinForms); xử lý sự kiện thay đổi DPI thời gian thực (`WM_DPICHANGED`), dịch chuyển tọa độ cửa sổ mượt mà giữa các màn hình có tỉ lệ co giãn khác nhau (ví dụ: màn hình laptop 150% DPI và màn hình ngoài 100% DPI), và tự động vẽ lại các thành phần Non-Client (tiêu đề, thanh cuộn, icon).

## 2. When to Use
- Khi ứng dụng desktop bị mờ nhòe (Bitmap Stretch Blurry) khi chạy trên màn hình 4K hoặc khi người dùng kéo cửa sổ sang màn hình phụ.
- Khi các nút bấm, văn bản, icon bị vỡ bố cục hoặc co rúm lại sau khi thay đổi cài đặt hiển thị của Windows Display Settings.
- Khi xây dựng ứng dụng native desktop hiện đại yêu cầu giao diện sắc nét 100% trên mọi cấu hình hiển thị.

## 3. When NOT to Use
- Khi ứng dụng chạy trong trình duyệt web nơi trình duyệt đã tự động xử lý `window.devicePixelRatio`.
- Khi ứng dụng là CLI console thuần túy không có cửa sổ giao diện đồ họa.

## 4. Prerequisites & Input Context
- **Hệ điều hành:** Windows 10 phiên bản 1703 (Creators Update) trở lên.
- **Tệp Application Manifest:** Khai báo cờ `<dpiAwareness>PerMonitorV2</dpiAwareness>` trong manifest của tệp `.exe`.

## 5. Core Concepts & Taxonomy
- **Per-Monitor V2 Context:** Chế độ DPI awareness tiên tiến nhất của Windows, tự động nhân tỉ lệ các thành phần Non-client metrics, menu popup, và hộp thoại con (`DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2`).
- **WM_DPICHANGED Message:** Thông điệp hệ thống gửi tới cửa sổ khi DPI thay đổi, cung cấp giá trị DPI mới trong `wParam` và hình chữ nhật gợi ý kích thước cửa sổ mới trong `lParam` (`RECT* prcNewWindow`).
- **Coordinate Space Scaling:** Phép nhân tỷ lệ khoảng cách: `logical_pixel = physical_pixel * (dpi / 96)`.

## 6. Step-by-Step Execution Workflow
1. Khai báo thuộc tính Per-Monitor V2 trong tệp `app.manifest` của dự án.
2. Thiết lập nhận diện DPI ngay tại hàm `wWinMain` bằng `SetProcessDpiAwarenessContext(DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2)`.
3. Bắt thông điệp `WM_DPICHANGED` trong hàm `WndProc` của cửa sổ chính.
4. Đọc `RECT* prcNewWindow = (RECT*)lParam;` và gọi `SetWindowPos()` để cập nhật kích thước cửa sổ theo đúng gợi ý của Windows.
5. Tải lại các tài nguyên hình ảnh (Icon, Bitmap) và font chữ tương ứng với giá trị DPI mới (`GetDpiForWindow(hWnd)`).
6. Gọi hàm `InvalidateRect()` để kích hoạt vẽ lại toàn bộ giao diện.

## 7. Concrete Examples
### Xu ly WM_DPICHANGED chuan muc trong WndProc cua Win32 API:
```cpp
#include <windows.h>

LRESULT CALLBACK WndProc(HWND hWnd, UINT message, WPARAM wParam, LPARAM lParam) {
    switch (message) {
    case WM_DPICHANGED: {
        WORD newDpiX = LOWORD(wParam);
        WORD newDpiY = HIWORD(wParam);
        RECT* const prcNewWindow = reinterpret_cast<RECT*>(lParam);

        // 1. Cap nhat kich thuoc va vi tri cua so theo de xuat cua he dieu hanh
        SetWindowPos(hWnd,
            nullptr,
            prcNewWindow->left,
            prcNewWindow->top,
            prcNewWindow->right - prcNewWindow->left,
            prcNewWindow->bottom - prcNewWindow->top,
            SWP_NOZORDER | SWP_NOACTIVATE);

        // 2. Cap nhat font chu va tai nguyen do hoa theo DPI moi
        HFONT hNewFont = CreateFontForDpi(newDpiX);
        SendMessage(hWnd, WM_SETFONT, reinterpret_cast<WPARAM>(hNewFont), TRUE);

        // 3. Ve lai toan bo cua so
        InvalidateRect(hWnd, nullptr, TRUE);
        return 0;
    }
    // Cac thong diep khac...
    default:
        return DefWindowProc(hWnd, message, wParam, lParam);
    }
}
```

## 8. Anti-Patterns & Common Traps
- **System DPI Awareness Trap:** Chỉ bật cờ System-DPI aware, khiến ứng dụng hiển thị sắc nét trên màn hình chính nhưng bị mờ nhòe khủng khiếp khi kéo sang màn hình phụ.
- **Hardcoding 96 DPI Fonts:** Khởi tạo font chữ với kích thước cứng không nhân tỷ lệ DPI làm văn bản quá nhỏ không thể đọc được trên màn hình 4K Surface/Laptop.
- **Ignoring lParam in WM_DPICHANGED:** Tự tính toán lại kích thước cửa sổ thay vì sử dụng `prcNewWindow` trong `lParam`, dẫn đến hiện tượng cửa sổ bị nhảy vị trí lung tung trên màn hình.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Ứng dụng khai báo đúng `PerMonitorV2` trong Application Manifest và nạp thành công khi khởi chạy.
- **QG-02**: Không có bất kỳ hiện tượng mờ nhòe (Bitmap scaling blur) khi chuyển đổi qua lại giữa các màn hình 100%, 150%, và 200% DPI.
- **QG-03**: Kích thước các nút bấm và khoảng cách padding giữ đúng tỷ lệ công thái học trên mọi màn hình.

## 10. Security & Safety Boundaries
- Đảm bảo các hàm gọi API vẽ không gây tràn bộ đệm khi xử lý kích thước hình ảnh co giãn động.

## 11. Platform Adapters
- **Runtimes**: C++ Win32 API, C# WPF (PerMonitorV2 support), Qt 6 HighDPI, Rust windows-rs.

## 12. Deliverables & Output Artifacts
- Tệp kê khai ứng dụng chuẩn (`app.manifest`).
- Lớp bao bọc xử lý DPI đa màn hình (`dpi_aware_window.hpp` / `dpi.rs`).

## 13. Related & Complementary Skills
dex-windows-input-api-integration, dex-windows-native-ui-accessibility, dex-windows-app-startup-profiling

## 14. Realistic Usage Example
```powershell
# Kiem tra trang thai DPI Awareness cua mot ung dung dang chay
Get-Process -Name "my_app" | ForEach-Object { (Get-Item $_.Path).VersionInfo }
```
