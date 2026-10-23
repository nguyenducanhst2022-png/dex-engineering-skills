---
name: dex-windows-input-api-integration
description: Integrate authorized Windows input APIs for desktop automation, test harness orchestration, and accessibility. Model SendInput, Raw Input, UIPI boundaries, and virtual coordinate translation.
---

# dex-windows-input-api-integration

## 1. Purpose & Scope
Tích hợp và kiểm soát an toàn các API đầu vào của hệ điều hành Windows (Windows Input APIs: SendInput, Raw Input API, RegisterHotKey) phục vụ tự động hóa kiểm thử UI, hỗ trợ người khuyết tật (Accessibility Tools) và điều khiển ngoại vi; xác định ranh giới bảo mật User Interface Privilege Isolation (UIPI), chuyển đổi hệ tọa độ ảo (Virtual Screen Space) và xử lý sự kiện bàn phím/chuột chuẩn xác.

## 2. When to Use
- Khi xây dựng công cụ kiểm thử tự động hóa ứng dụng desktop native (Win32, WPF, WinUI) trên Windows.
- Khi phát triển tiện ích trợ năng mô phỏng thao tác bàn phím, chuột hoặc trackball cho người dùng đặc biệt.
- Khi lắng nghe thiết bị đầu vào chuyên dụng (Gaming controllers, Barcode Scanners, CAD 3D Mouse) qua Raw Input API.

## 3. When NOT to Use
- Khi tự động hóa ứng dụng web thông qua trình duyệt (nên dùng Playwright hoặc Selenium WebDriver).
- Khi cố tình mô phỏng phím để ghi lén thao tác người dùng (Keylogging) hoặc can thiệp trò chơi trái phép (nghiêm cấm theo chính sách bảo mật DEX).

## 4. Prerequisites & Input Context
- **Hệ điều hành:** Windows 10/11 x64, Visual Studio hoặc Windows SDK (C++, C#, Rust).
- **Quyền hạn thực thi:** Tiến trình chạy với mức đặc quyền phù hợp hoặc cấu hình `uiAccess=true` nếu cần tương tác với ứng dụng Elevated.

## 5. Core Concepts & Taxonomy
- **User Interface Privilege Isolation (UIPI):** Cơ chế an ninh của Windows chặn các tiến trình có mức Integrity Level thấp gửi thông điệp `WM_COMMAND` hoặc `SendInput` tới tiến trình có Integrity Level cao hơn (ví dụ: tiến trình thường không thể gửi phím vào Task Manager).
- **Normalized Coordinates (0 to 65535):** Cấu trúc `MOUSEINPUT` của `SendInput` yêu cầu tọa độ chuột chuẩn hóa theo tỷ lệ `dx = (x * 65536) / screen_width`.
- **Raw Input Architecture:** Giao thức cho phép ứng dụng nhận dữ liệu thô trực tiếp từ driver thiết bị HID mà không bị Windows Message Loop can thiệp hoặc lọc.

## 6. Step-by-Step Execution Workflow
1. Khảo sát cấu hình đa màn hình và tính toán kích thước màn hình ảo (`GetSystemMetrics(SM_CXVIRTUALSCREEN)`).
2. Chuẩn bị mảng cấu trúc `INPUT` mô tả chuỗi hành động (ví dụ: nhấn phím -> nhả phím).
3. Kiểm tra tính hợp lệ của cửa sổ mục tiêu và mức đặc quyền UIPI bằng `GetGUIThreadInfo`.
4. Gọi hàm `SendInput()` trong khối kiểm soát lỗi và ghi nhận số lượng sự kiện được chèn thành công.
5. Đăng ký nhận sự kiện thô qua `RegisterRawInputDevices()` nếu cần phân biệt nhiều chuột/bàn phím vật lý độc lập.
6. Kiểm chứng việc tiếp nhận sự kiện trên ứng dụng mục tiêu và giải phóng tài nguyên.

## 7. Concrete Examples
### Chuong trinh C++ mo phong nhap ban phim va chuot an toan bang SendInput:
```cpp
#include <windows.h>
#include <vector>
#include <iostream>

void send_mouse_click(int x, int y) {
    // 1. Tinh toan toa do chuan hoa tren he man hinh ao
    int v_width = GetSystemMetrics(SM_CXVIRTUALSCREEN);
    int v_height = GetSystemMetrics(SM_CYVIRTUALSCREEN);
    int v_left = GetSystemMetrics(SM_XVIRTUALSCREEN);
    int v_top = GetSystemMetrics(SM_YVIRTUALSCREEN);

    DWORD norm_x = (DWORD)(((x - v_left) * 65536.0f) / v_width);
    DWORD norm_y = (DWORD)(((y - v_top) * 65536.0f) / v_height);

    std::vector<INPUT> inputs(3);

    // Di chuyen chuot
    inputs[0].type = INPUT_MOUSE;
    inputs[0].mi.dx = norm_x;
    inputs[0].mi.dy = norm_y;
    inputs[0].mi.dwFlags = MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE | MOUSEEVENTF_VIRTUALDESK;

    // Nhan chuot trai
    inputs[1].type = INPUT_MOUSE;
    inputs[1].mi.dwFlags = MOUSEEVENTF_LEFTDOWN;

    // Nha chuot trai
    inputs[2].type = INPUT_MOUSE;
    inputs[2].mi.dwFlags = MOUSEEVENTF_LEFTUP;

    UINT sent = SendInput(static_cast<UINT>(inputs.size()), inputs.data(), sizeof(INPUT));
    if (sent != inputs.size()) {
        std::cerr << "SendInput blocked or failed. Error: " << GetLastError() << std::endl;
    }
}
```

## 8. Anti-Patterns & Common Traps
- **Ignoring UIPI Elevation Mismatch:** Cố gửi phím vào cửa sổ ứng dụng chạy dưới quyền Administrator từ tiến trình thường, khiến `SendInput` âm thầm bị chặn.
- **Hardcoding 1920x1080 Resolution:** Giả định màn hình luôn có kích thước cố định khiến tọa độ chuột bị bấm lệch sang màn hình phụ hoặc ra ngoài vùng làm việc.
- **Omitting Key-Up Events:** Gửi sự kiện nhấn phím (KeyDown) nhưng quên gửi sự kiện nhả phím (KeyUp) khiến phím bị kẹt ảo trong hệ điều hành.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Tọa độ chuột mô phỏng chính xác tuyệt đối trên cả thiết lập đơn màn hình và đa màn hình có độ phân giải hỗn hợp.
- **QG-02**: Mọi sự kiện mô phỏng phím đều có cặp KeyDown và KeyUp hoàn chỉnh.
- **QG-03**: Hệ thống bắt và xử lý mã lỗi `ERROR_ACCESS_DENIED` khi vi phạm ranh giới UIPI.

## 10. Security & Safety Boundaries
- Tuân thủ ranh giới an toàn Windows; không thực hiện hook bàn phím toàn cục trái phép ngoài phạm vi ứng dụng được cấp quyền.

## 11. Platform Adapters
- **Runtimes**: C++20 Win32 API, C# P/Invoke, Rust `windows-rs` / `winapi`.

## 12. Deliverables & Output Artifacts
- Module điều phối đầu vào Windows (`windows_input_manager.cpp` / `input.rs`).
- Bộ kiểm thử tự động xác minh tọa độ chuột trên không gian đa màn hình.

## 13. Related & Complementary Skills
dex-win32-dpi-multi-monitor-layout, dex-windows-native-ui-accessibility, dex-windows-app-startup-profiling

## 14. Realistic Usage Example
```powershell
# Kiem tra quyen UIPI cua tien trinh hien tai
Get-Process -Id $PID | Select-Object Id, ProcessName, @{Name="Elevated";Expression={$_.SessionId}}
```
