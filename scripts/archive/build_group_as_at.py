# -*- coding: utf-8 -*-
"""
DEX ENGINEERING SKILLS FRAMEWORK v9.0 — GENERATOR
Builds Group AS (Skills 441–450: Windows & Desktop Systems)
and Group AT (Skills 451–460: Platform Resilience & Infrastructure).
All skills strictly implement the 14 mandatory sections standard.
"""

import os
import sys

if sys.stdout.encoding != "utf-8" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SKILLS_DIR = os.path.join(ROOT, ".agents", "skills")

SKILLS_AS_AT = [
    # =========================================================================
    # GROUP AS: Windows & Desktop Systems (Skills 441–450)
    # =========================================================================
    {
        "id": "dex-windows-input-api-integration",
        "name": "dex-windows-input-api-integration",
        "desc": "Integrate authorized Windows input APIs for desktop automation, test harness orchestration, and accessibility. Model SendInput, Raw Input, UIPI boundaries, and virtual coordinate translation.",
        "purpose": "Tích hợp và kiểm soát an toàn các API đầu vào của hệ điều hành Windows (Windows Input APIs: SendInput, Raw Input API, RegisterHotKey) phục vụ tự động hóa kiểm thử UI, hỗ trợ người khuyết tật (Accessibility Tools) và điều khiển ngoại vi; xác định ranh giới bảo mật User Interface Privilege Isolation (UIPI), chuyển đổi hệ tọa độ ảo (Virtual Screen Space) và xử lý sự kiện bàn phím/chuột chuẩn xác.",
        "when_use": "- Khi xây dựng công cụ kiểm thử tự động hóa ứng dụng desktop native (Win32, WPF, WinUI) trên Windows.\n- Khi phát triển tiện ích trợ năng mô phỏng thao tác bàn phím, chuột hoặc trackball cho người dùng đặc biệt.\n- Khi lắng nghe thiết bị đầu vào chuyên dụng (Gaming controllers, Barcode Scanners, CAD 3D Mouse) qua Raw Input API.",
        "when_not_use": "- Khi tự động hóa ứng dụng web thông qua trình duyệt (nên dùng Playwright hoặc Selenium WebDriver).\n- Khi cố tình mô phỏng phím để ghi lén thao tác người dùng (Keylogging) hoặc can thiệp trò chơi trái phép (nghiêm cấm theo chính sách bảo mật DEX).",
        "prereqs": "- **Hệ điều hành:** Windows 10/11 x64, Visual Studio hoặc Windows SDK (C++, C#, Rust).\n- **Quyền hạn thực thi:** Tiến trình chạy với mức đặc quyền phù hợp hoặc cấu hình `uiAccess=true` nếu cần tương tác với ứng dụng Elevated.",
        "concepts": "- **User Interface Privilege Isolation (UIPI):** Cơ chế an ninh của Windows chặn các tiến trình có mức Integrity Level thấp gửi thông điệp `WM_COMMAND` hoặc `SendInput` tới tiến trình có Integrity Level cao hơn (ví dụ: tiến trình thường không thể gửi phím vào Task Manager).\n- **Normalized Coordinates (0 to 65535):** Cấu trúc `MOUSEINPUT` của `SendInput` yêu cầu tọa độ chuột chuẩn hóa theo tỷ lệ `dx = (x * 65536) / screen_width`.\n- **Raw Input Architecture:** Giao thức cho phép ứng dụng nhận dữ liệu thô trực tiếp từ driver thiết bị HID mà không bị Windows Message Loop can thiệp hoặc lọc.",
        "workflow": "1. Khảo sát cấu hình đa màn hình và tính toán kích thước màn hình ảo (`GetSystemMetrics(SM_CXVIRTUALSCREEN)`).\n2. Chuẩn bị mảng cấu trúc `INPUT` mô tả chuỗi hành động (ví dụ: nhấn phím -> nhả phím).\n3. Kiểm tra tính hợp lệ của cửa sổ mục tiêu và mức đặc quyền UIPI bằng `GetGUIThreadInfo`.\n4. Gọi hàm `SendInput()` trong khối kiểm soát lỗi và ghi nhận số lượng sự kiện được chèn thành công.\n5. Đăng ký nhận sự kiện thô qua `RegisterRawInputDevices()` nếu cần phân biệt nhiều chuột/bàn phím vật lý độc lập.\n6. Kiểm chứng việc tiếp nhận sự kiện trên ứng dụng mục tiêu và giải phóng tài nguyên.",
        "examples": """### Chuong trinh C++ mo phong nhap ban phim va chuot an toan bang SendInput:
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
```""",
        "antipatterns": "- **Ignoring UIPI Elevation Mismatch:** Cố gửi phím vào cửa sổ ứng dụng chạy dưới quyền Administrator từ tiến trình thường, khiến `SendInput` âm thầm bị chặn.\n- **Hardcoding 1920x1080 Resolution:** Giả định màn hình luôn có kích thước cố định khiến tọa độ chuột bị bấm lệch sang màn hình phụ hoặc ra ngoài vùng làm việc.\n- **Omitting Key-Up Events:** Gửi sự kiện nhấn phím (KeyDown) nhưng quên gửi sự kiện nhả phím (KeyUp) khiến phím bị kẹt ảo trong hệ điều hành.",
        "gates": "- **QG-01**: Tọa độ chuột mô phỏng chính xác tuyệt đối trên cả thiết lập đơn màn hình và đa màn hình có độ phân giải hỗn hợp.\n- **QG-02**: Mọi sự kiện mô phỏng phím đều có cặp KeyDown và KeyUp hoàn chỉnh.\n- **QG-03**: Hệ thống bắt và xử lý mã lỗi `ERROR_ACCESS_DENIED` khi vi phạm ranh giới UIPI.",
        "security": "- Tuân thủ ranh giới an toàn Windows; không thực hiện hook bàn phím toàn cục trái phép ngoài phạm vi ứng dụng được cấp quyền.",
        "adapters": "- **Runtimes**: C++20 Win32 API, C# P/Invoke, Rust `windows-rs` / `winapi`.",
        "deliverables": "- Module điều phối đầu vào Windows (`windows_input_manager.cpp` / `input.rs`).\n- Bộ kiểm thử tự động xác minh tọa độ chuột trên không gian đa màn hình.",
        "related": "dex-win32-dpi-multi-monitor-layout, dex-windows-native-ui-accessibility, dex-windows-app-startup-profiling",
        "usage": "```powershell\n# Kiem tra quyen UIPI cua tien trinh hien tai\nGet-Process -Id $PID | Select-Object Id, ProcessName, @{Name=\"Elevated\";Expression={$_.SessionId}}\n```"
    },
    {
        "id": "dex-win32-dpi-multi-monitor-layout",
        "name": "dex-win32-dpi-multi-monitor-layout",
        "desc": "Design, implement, and verify Per-Monitor V2 high-DPI awareness for Windows desktop applications. Handle dynamic scaling, non-client metrics, and coordinate translation across mixed-DPI displays.",
        "purpose": "Thiết kế, xử lý và kiểm chứng tính năng thích ứng độ phân giải cao theo từng màn hình (Per-Monitor V2 High-DPI Awareness) cho ứng dụng desktop Windows (Win32, MFC, WPF, WinForms); xử lý sự kiện thay đổi DPI thời gian thực (`WM_DPICHANGED`), dịch chuyển tọa độ cửa sổ mượt mà giữa các màn hình có tỉ lệ co giãn khác nhau (ví dụ: màn hình laptop 150% DPI và màn hình ngoài 100% DPI), và tự động vẽ lại các thành phần Non-Client (tiêu đề, thanh cuộn, icon).",
        "when_use": "- Khi ứng dụng desktop bị mờ nhòe (Bitmap Stretch Blurry) khi chạy trên màn hình 4K hoặc khi người dùng kéo cửa sổ sang màn hình phụ.\n- Khi các nút bấm, văn bản, icon bị vỡ bố cục hoặc co rúm lại sau khi thay đổi cài đặt hiển thị của Windows Display Settings.\n- Khi xây dựng ứng dụng native desktop hiện đại yêu cầu giao diện sắc nét 100% trên mọi cấu hình hiển thị.",
        "when_not_use": "- Khi ứng dụng chạy trong trình duyệt web nơi trình duyệt đã tự động xử lý `window.devicePixelRatio`.\n- Khi ứng dụng là CLI console thuần túy không có cửa sổ giao diện đồ họa.",
        "prereqs": "- **Hệ điều hành:** Windows 10 phiên bản 1703 (Creators Update) trở lên.\n- **Tệp Application Manifest:** Khai báo cờ `<dpiAwareness>PerMonitorV2</dpiAwareness>` trong manifest của tệp `.exe`.",
        "concepts": "- **Per-Monitor V2 Context:** Chế độ DPI awareness tiên tiến nhất của Windows, tự động nhân tỉ lệ các thành phần Non-client metrics, menu popup, và hộp thoại con (`DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2`).\n- **WM_DPICHANGED Message:** Thông điệp hệ thống gửi tới cửa sổ khi DPI thay đổi, cung cấp giá trị DPI mới trong `wParam` và hình chữ nhật gợi ý kích thước cửa sổ mới trong `lParam` (`RECT* prcNewWindow`).\n- **Coordinate Space Scaling:** Phép nhân tỷ lệ khoảng cách: `logical_pixel = physical_pixel * (dpi / 96)`.",
        "workflow": "1. Khai báo thuộc tính Per-Monitor V2 trong tệp `app.manifest` của dự án.\n2. Thiết lập nhận diện DPI ngay tại hàm `wWinMain` bằng `SetProcessDpiAwarenessContext(DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2)`.\n3. Bắt thông điệp `WM_DPICHANGED` trong hàm `WndProc` của cửa sổ chính.\n4. Đọc `RECT* prcNewWindow = (RECT*)lParam;` và gọi `SetWindowPos()` để cập nhật kích thước cửa sổ theo đúng gợi ý của Windows.\n5. Tải lại các tài nguyên hình ảnh (Icon, Bitmap) và font chữ tương ứng với giá trị DPI mới (`GetDpiForWindow(hWnd)`).\n6. Gọi hàm `InvalidateRect()` để kích hoạt vẽ lại toàn bộ giao diện.",
        "examples": """### Xu ly WM_DPICHANGED chuan muc trong WndProc cua Win32 API:
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
```""",
        "antipatterns": "- **System DPI Awareness Trap:** Chỉ bật cờ System-DPI aware, khiến ứng dụng hiển thị sắc nét trên màn hình chính nhưng bị mờ nhòe khủng khiếp khi kéo sang màn hình phụ.\n- **Hardcoding 96 DPI Fonts:** Khởi tạo font chữ với kích thước cứng không nhân tỷ lệ DPI làm văn bản quá nhỏ không thể đọc được trên màn hình 4K Surface/Laptop.\n- **Ignoring lParam in WM_DPICHANGED:** Tự tính toán lại kích thước cửa sổ thay vì sử dụng `prcNewWindow` trong `lParam`, dẫn đến hiện tượng cửa sổ bị nhảy vị trí lung tung trên màn hình.",
        "gates": "- **QG-01**: Ứng dụng khai báo đúng `PerMonitorV2` trong Application Manifest và nạp thành công khi khởi chạy.\n- **QG-02**: Không có bất kỳ hiện tượng mờ nhòe (Bitmap scaling blur) khi chuyển đổi qua lại giữa các màn hình 100%, 150%, và 200% DPI.\n- **QG-03**: Kích thước các nút bấm và khoảng cách padding giữ đúng tỷ lệ công thái học trên mọi màn hình.",
        "security": "- Đảm bảo các hàm gọi API vẽ không gây tràn bộ đệm khi xử lý kích thước hình ảnh co giãn động.",
        "adapters": "- **Runtimes**: C++ Win32 API, C# WPF (PerMonitorV2 support), Qt 6 HighDPI, Rust windows-rs.",
        "deliverables": "- Tệp kê khai ứng dụng chuẩn (`app.manifest`).\n- Lớp bao bọc xử lý DPI đa màn hình (`dpi_aware_window.hpp` / `dpi.rs`).",
        "related": "dex-windows-input-api-integration, dex-windows-native-ui-accessibility, dex-windows-app-startup-profiling",
        "usage": "```powershell\n# Kiem tra trang thai DPI Awareness cua mot ung dung dang chay\nGet-Process -Name \"my_app\" | ForEach-Object { (Get-Item $_.Path).VersionInfo }\n```"
    },
    {
        "id": "dex-windows-app-startup-profiling",
        "name": "dex-windows-app-startup-profiling",
        "desc": "Profile, measure, and optimize Windows desktop application startup performance. Trace cold and warm launch phases, diagnose static DLL loading delays, and analyze ETW traces.",
        "purpose": "Đo lường, định hình (Profiling) và tối ưu hóa thời gian khởi động của ứng dụng desktop Windows; phân tích chi tiết hai giai đoạn Khởi động lạnh (Cold Start) và Khởi động ấm (Warm Start); phát hiện các nút thắt cổ chai do nạp DLL tĩnh (Static DLL Imports), nghẽn I/O đọc đĩa, hoặc khởi tạo dịch vụ đồng bộ trên Main Thread; sử dụng Event Tracing for Windows (ETW) và Windows Performance Analyzer (WPA) để đạt mục tiêu khởi chạy dưới 1 giây.",
        "when_use": "- Khi ứng dụng desktop bị người dùng phàn nàn là khởi động quá chậm, xuất hiện hiện tượng chuột xoay vòng (Wait cursor) kéo dài.\n- Khi bổ sung nhiều thư viện bên thứ ba khiến kích thước tệp và số lượng DLL nạp khi nạp chương trình tăng vọt.\n- Khi cần thiết lập chỉ số hồi quy thời gian khởi động (Startup Regression Tests) trong pipeline CI/CD.",
        "when_not_use": "- Khi tối ưu hóa các ứng dụng server chạy ngầm liên tục 24/7 nơi thời gian khởi động ban đầu không ảnh hưởng tới người dùng cuối.\n- Khi phân tích hiệu năng nạp trang web trên trình duyệt (sử dụng Lighthouse hoặc Chrome DevTools).",
        "prereqs": "- **Hệ thống đo kiểm:** Windows 10/11 x64, Windows Performance Toolkit (WPT: `xperf`, `wpr`).\n- **Ứng dụng mục tiêu:** Bản dựng Release kèm tệp ký hiệu gỡ lỗi đầy đủ (`.pdb`).",
        "concepts": "- **Cold Start vs Warm Start:** Khởi động lạnh diễn ra khi mã nhị phân và dữ liệu chưa có sẵn trong bộ nhớ đệm RAM (Standby List), đòi hỏi đọc từ ổ đĩa cứng; Khởi động ấm tận dụng dữ liệu đã được cache sẵn trong RAM.\n- **Delay-Loaded DLLs (/DELAYLOAD):** Kỹ thuật biên dịch của MSVC cho phép hoãn việc nạp một DLL cho đến khi hàm đầu tiên trong DLL đó thực sự được gọi thay vì nạp ngay lúc khởi động tiến trình.\n- **Event Tracing for Windows (ETW):** Hệ thống ghi vết nhân hệ điều hành hiệu năng siêu cao, cho phép theo dõi chi tiết từng sự kiện tạo luồng, cấp phát bộ nhớ, và I/O đĩa.",
        "workflow": "1. Khởi động công cụ ghi vết Windows Performance Recorder: `wpr -start GeneralProfile -start CPU -start DiskIO`.\n2. Khởi chạy ứng dụng mục tiêu và đo thời gian đến khi cửa sổ đầu tiên hiển thị và sẵn sàng nhận tương tác (Time to Interactive).\n3. Dừng ghi vết và lưu tệp: `wpr -stop startup_trace.etl`.\n4. Mở tệp `.etl` trong Windows Performance Analyzer (WPA) và nạp PDB Symbols.\n5. Kiểm tra biểu đồ \"Regions of Interest\" và \"CPU Usage (Sampled)\" để tìm hàm chiếm dụng CPU lâu nhất trong `wWinMain`.\n6. Chuyển đổi các DLL không cần thiết sang cờ `/DELAYLOAD` và dời các tác vụ khởi tạo mạng/CSDL sang Background Thread.",
        "examples": """### Cau hinh Delay-Load DLL trong file CMakeLists.txt de tang toc khoi dong:
```cmake
# Toi uu hoa thoi gian khoi dong bang cach hoan nap cac DLL nang
target_link_options(my_desktop_app PRIVATE
    "/DELAYLOAD:heavy_ml_runtime.dll"
    "/DELAYLOAD:media_codec_x64.dll"
    "/DELAYLOAD:sqlite3.dll"
)

# Yeu cau link voi thu vien delayimp.lib cua MSVC
target_link_libraries(my_desktop_app PRIVATE delayimp.lib)
```

### Script do thoi gian khoi dong lanh va am tu dong bang PowerShell:
```powershell
param([string]$AppPath = "C:\\MyApp\\app.exe")

Write-Host "=== MEASURING COLD START ==="
# Xoa Standby Cache de gia lap Cold Start (Yeu cau quyen Admin voi RAMMap CLI)
& "RAMMap64.exe" -Ew
& "RAMMap64.exe" -Es

$coldTime = Measure-Command {
    $proc = Start-Process -FilePath $AppPath -PassThru
    $proc.WaitForInputIdle(5000)
    Stop-Process -Id $proc.Id -Force
}
Write-Host "Cold Start Time: $($coldTime.TotalMilliseconds) ms"

Write-Host "=== MEASURING WARM START ==="
$warmTime = Measure-Command {
    $proc = Start-Process -FilePath $AppPath -PassThru
    $proc.WaitForInputIdle(5000)
    Stop-Process -Id $proc.Id -Force
}
Write-Host "Warm Start Time: $($warmTime.TotalMilliseconds) ms"
```""",
        "antipatterns": "- **Heavy Synchronous Initialization in WinMain:** Đọc tệp cấu hình lớn, tạo kết nối CSDL hoặc gọi REST API đồng bộ ngay trên luồng giao diện chính trước khi hiển thị cửa sổ.\n- **Static Linking of Hundreds of Unused DLLs:** Liên kết tĩnh hàng tá DLL tiện ích khiến hệ điều hành mất hàng trăm mili-giây để phân giải bảng import table khi nạp PE header.\n- **Splash Screen Overhead:** Sử dụng màn hình chào (Splash Screen) quá phức tạp tự nó chiếm thêm 500ms CPU chỉ để vẽ hoạt ảnh khởi động.",
        "gates": "- **QG-01**: Thời gian Warm Start (Time to Interactive) đạt dưới 800ms trên cấu hình máy tính văn phòng tiêu chuẩn.\n- **QG-02**: Không có bất kỳ tác vụ I/O mạng nào được thực thi đồng bộ trên luồng chính trong quá trình khởi động.\n- **QG-03**: 100% các DLL phụ trợ nặng đều được cấu hình `/DELAYLOAD`.",
        "security": "- Đảm bảo các thư viện Delay-Load được nạp từ các thư mục được bảo vệ của hệ thống; phòng chống tấn công DLL Hijacking.",
        "adapters": "- **Runtimes**: Windows Performance Toolkit (WPR/WPA), MSVC Linker (/DELAYLOAD), Intel VTune, Sysinternals RAMMap.",
        "deliverables": "- Tệp cấu hình ghi vết ETW (`startup_profile.wprp`).\n- Báo cáo phân tích thời gian khởi động ứng dụng (`startup_analysis_report.md`).",
        "related": "dex-windows-input-api-integration, dex-win32-dpi-multi-monitor-layout, dex-windows-app-crash-dumps",
        "usage": "```powershell\n# Ghi vet ETW qua trinh khoi dong bang cong cu xperf\nxperf -on PROC_THREAD+LOADER+CSWITCH+PROFILE -f trace.etl\nStart-Process \"my_app.exe\"\nxperf -d trace_final.etl\n```"
    },
    {
        "id": "dex-windows-app-crash-dumps",
        "name": "dex-windows-app-crash-dumps",
        "desc": "Capture, configure, and analyze native Windows crash dumps (Minidump, WER). Triage crash signatures using WinDbg and CDB, manage symbol servers, and isolate memory corruptions.",
        "purpose": "Thu thập, cấu hình và phân tích chuyên sâu các tệp kết xuất sự cố ứng dụng Windows (Crash MiniDumps & Windows Error Reporting - WER); thiết lập cơ chế bắt ngoại lệ không được xử lý (`SetUnhandledExceptionFilter`), tự động ghi tệp dump nhị phân qua API `MiniDumpWriteDump`; sử dụng công cụ gỡ lỗi dòng lệnh CDB/WinDbg và máy chủ ký hiệu (Symbol Server) để phân tích vết ngăn xếp (Stack Trace), xác định chính xác nguyên nhân lỗi vi phạm truy cập bộ nhớ (Access Violation `0xC0000005`) hoặc hỏng vùng nhớ Heap.",
        "when_use": "- Khi ứng dụng desktop bị biến mất đột ngột (Silent Crash) trên máy tính khách hàng mà không để lại thông báo lỗi.\n- Khi điều tra các lỗi sập khó tái hiện ngẫu nhiên liên quan đến đa luồng, race conditions hoặc giải phóng bộ nhớ kép (Double Free).\n- Khi xây dựng hạ tầng thu thập báo cáo lỗi tự động (Crash Reporting Pipeline: Sentry Native, Breakpad, Crashpad).",
        "when_not_use": "- Khi xử lý các ngoại lệ nghiệp vụ thông thường trong các ngôn ngữ có Garbage Collection (như C# Exception) đã có khối `try/catch` xử lý.\n- Khi phân tích lỗi hệ điều hành xanh màn hình (BSOD Kernel Dump - thuộc phạm vi Driver Development).",
        "prereqs": "- **Hệ thống phân tích:** Windows SDK Debugging Tools for Windows (`cdb.exe`, `windbg.exe`).\n- **Kho lưu trữ ký hiệu:** Tệp `.pdb` khớp chính xác với mã băm nhị phân của bản phát hành ứng dụng.",
        "concepts": "- **MiniDumpWriteDump:** Hàm API Win32 thuộc thư viện `dbghelp.dll` cho phép kết xuất bộ nhớ của tiến trình và luồng gặp nạn thành tệp `.dmp` nhỏ gọn.\n- **Access Violation (0xC0000005):** Ngoại lệ phần cứng do CPU phát hiện khi một tiến trình cố tình đọc/ghi vào một địa chỉ ô nhớ không hợp lệ hoặc không có quyền truy cập.\n- **Source Indexing & Symbol Server:** Cơ chế lưu trữ và tự động liên kết các tệp PDB với kho mã nguồn Git thông qua `symstore.exe` và `srctool.exe`.",
        "workflow": "1. Đăng ký bộ lọc ngoại lệ toàn cục tại điểm vào chương trình: `SetUnhandledExceptionFilter(CrashHandlerFilter)`.\n2. Khi xảy ra sập, khởi tạo tiến trình con phụ trợ hoặc gọi an toàn `MiniDumpWriteDump` với các cờ `MiniDumpWithDataSegs` và `MiniDumpWithIndirectlyReferencedMemory`.\n3. Lưu tệp `.dmp` vào thư mục AppData an toàn của người dùng.\n4. Mở tệp dump bằng công cụ CDB tự động: `cdb -z crash.dmp -c \"!analyze -v; q\"`.\n5. Nạp ký hiệu gỡ lỗi và kiểm tra khung ngăn xếp nơi xảy ra lỗi (FAULTING_IP, FAILURE_BUCKET_ID).\n6. Phân tích trạng thái thanh ghi và câu lệnh Assembly tại thời điểm sập để xác định bản chất của bug.",
        "examples": """### Cai dat Custom Unhandled Exception Filter tu dong ghi MiniDump trong C++:
```cpp
#include <windows.h>
#include <dbghelp.h>
#include <iostream>

#pragma comment(lib, "dbghelp.lib")

LONG WINAPI CustomCrashFilter(EXCEPTION_POINTERS* pExceptionPointers) {
    HANDLE hFile = CreateFileA("crash_dump.dmp", GENERIC_WRITE, FILE_SHARE_READ, nullptr,
                               CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, nullptr);

    if (hFile != INVALID_HANDLE_VALUE) {
        MINIDUMP_EXCEPTION_INFORMATION mei;
        mei.ThreadId = GetCurrentThreadId();
        mei.ExceptionPointers = pExceptionPointers;
        mei.ClientPointers = FALSE;

        // Ghi minidump gom stack, data segs va thread info
        BOOL success = MiniDumpWriteDump(
            GetCurrentProcess(),
            GetCurrentProcessId(),
            hFile,
            static_cast<MINIDUMP_TYPE>(MiniDumpNormal | MiniDumpWithIndirectlyReferencedMemory | MiniDumpWithThreadInfo),
            &mei,
            nullptr,
            nullptr
        );

        CloseHandle(hFile);
        if (success) {
            std::cerr << "CRASH DUMP GENERATED: crash_dump.dmp" << std::endl;
        }
    }
    return EXCEPTION_EXECUTE_HANDLER; // Hoac EXCEPTION_CONTINUE_SEARCH de WER xu ly tiep
}

void setup_crash_reporting() {
    SetUnhandledExceptionFilter(CustomCrashFilter);
}
```""",
        "antipatterns": "- **Allocating Dynamic Memory inside Crash Handler:** Cố gọi `new`, `malloc` hoặc hàm cấp phát heap bên trong Unhandled Exception Filter khi vùng nhớ Heap đã bị hỏng khiến tiến trình bị deadlock vĩnh viễn.\n- **Discarding PDB Files after Build:** Xóa bỏ tệp `.pdb` sau khi build bản release khiến các tệp dump thu thập về từ người dùng không thể phân giải tên hàm và số dòng mã.\n- **Writing Full Memory Dumps Unconditionally:** Luôn ghi Full Dump (vài Gigabyte) làm tràn ổ cứng người dùng và tốn băng thông truyền tải mạng.",
        "gates": "- **QG-01**: Tệp MiniDump được tạo thành công 100% khi ứng dụng gặp sự cố Access Violation giả lập.\n- **QG-02**: Lệnh `!analyze -v` trong WinDbg phân giải chính xác tên hàm và số dòng trong tệp nguồn gốc.\n- **QG-03**: Bộ xử lý sự cố không thực hiện bất kỳ thao tác cấp phát Heap nào bên trong Exception Filter.",
        "security": "- Loại bỏ các thông tin nhạy cảm (như mật khẩu hoặc token trong bộ nhớ) khỏi dump nếu áp dụng cơ chế Full Memory Dump.",
        "adapters": "- **Runtimes**: Windows DbgHelp API, WinDbg / CDB CLI, Google Crashpad, Sentry Native SDK.",
        "deliverables": "- Thư viện bắt sự cố native (`crash_reporter.cpp` / `crash.rs`).\n- Kịch bản tự động phân tích crash dump bằng CDB (`triage_dump.py`).",
        "related": "dex-windows-service-recovery, dex-windows-app-startup-profiling, dex-windows-com-interop",
        "usage": "```powershell\n# Phan tich crash dump tu dong bang cdb tu Windows SDK\n& \"C:\\Program Files (x86)\\Windows Kits\\10\\Debuggers\\x64\\cdb.exe\" -z crash_dump.dmp -c \"!analyze -v; kp; q\"\n```"
    },
    {
        "id": "dex-windows-service-recovery",
        "name": "dex-windows-service-recovery",
        "desc": "Implement, configure, and test Windows Service architectures and recovery policies. Manage Service Control Manager (SCM) interactions, graceful shutdowns, and failure restart actions.",
        "purpose": "Thiết kế, cài đặt và kiểm tra độ bền vững của ứng dụng dịch vụ chạy ngầm trên Windows (Windows Service Lifecycle Management); cấu hình giao tiếp với Service Control Manager (SCM), xử lý chính xác các tín hiệu điều khiển `SERVICE_CONTROL_STOP`, `SERVICE_CONTROL_SHUTDOWN` và `SERVICE_CONTROL_PRESHUTDOWN`; thiết lập chính sách tự động phục hồi khi gặp sự cố (`SERVICE_FAILURE_ACTIONS`: tự khởi động lại, chạy chương trình cứu hộ) và bảo đảm thời gian dừng dịch vụ an toàn không làm mất dữ liệu.",
        "when_use": "- Khi phát triển các daemon xử lý dữ liệu ngầm, máy chủ agent giám sát bảo mật hoặc worker xử lý tác vụ nền trên Windows Server.\n- Khi dịch vụ bị SCM cưỡng chế tắt ngang (Killed) do không phản hồi kịp thời hạn dừng dịch vụ (Service Stop Timeout).\n- Khi cần tự động hóa cấu hình chính sách phục hồi dịch vụ tự động sau khi bị sập bằng lệnh `sc.exe` hoặc PowerShell.",
        "when_not_use": "- Khi ứng dụng có giao diện tương tác người dùng (kể từ Windows Vista, Session 0 Isolation cấm tuyệt đối Windows Service hiển thị UI).\n- Khi tác vụ là một công việc định kỳ chạy một lần (nên dùng Windows Task Scheduler thay vì duy trì một service chạy liên tục).",
        "prereqs": "- **Hệ điều hành:** Windows 10/11 hoặc Windows Server 2019/2022.\n- **Quyền hạn quản trị:** Quyền Administrator để cài đặt và điều khiển SCM qua `sc.exe`.",
        "concepts": "- **Session 0 Isolation:** Rào chắn an ninh của Windows cô lập toàn bộ các service trong Session 0 tách biệt hoàn toàn với Session của người dùng đăng nhập, triệt tiêu nguy cơ tấn công Shatter Attack.\n- **SCM Handshake & Status Updates:** Quy trình dịch vụ định kỳ cập nhật trạng thái `SERVICE_STATUS` (`SERVICE_START_PENDING`, `SERVICE_RUNNING`, `SERVICE_STOP_PENDING`) và chỉ số `dwCheckPoint` để báo cáo với SCM rằng tiến trình vẫn đang hoạt động bình thường.\n- **SERVICE_FAILURE_ACTIONS:** Cấu trúc định nghĩa hành vi của hệ điều hành khi service bị sập bất ngờ: Lần 1 tự restart sau 1 phút, Lần 2 restart sau 5 phút, Lần 3 chạy script khôi phục.",
        "workflow": "1. Khai báo hàm `ServiceMain` và bảng điều phối `SERVICE_TABLE_ENTRY` tại hàm `main`.\n2. Đăng ký hàm xử lý sự kiện điều khiển thông qua `RegisterServiceCtrlHandlerEx`.\n3. Báo cáo trạng thái `SERVICE_RUNNING` với SCM sau khi khởi tạo thành công các luồng worker.\n4. Khi nhận lệnh `SERVICE_CONTROL_STOP`, chuyển trạng thái sang `SERVICE_STOP_PENDING`, phát tín hiệu hủy cho worker và định kỳ tăng `dwCheckPoint`.\n5. Thu dọn kết nối CSDL, đóng tệp nhật ký và báo cáo `SERVICE_STOPPED`.\n6. Cấu hình chính sách tự phục hồi bằng lệnh `sc.exe failure` với các hành động khởi động lại.",
        "examples": """### Khung ma nguon C++ chuan cho Windows Service co ho tro Stop graceful:
```cpp
#include <windows.h>
#include <iostream>
#include <atomic>

SERVICE_STATUS        g_ServiceStatus{};
SERVICE_STATUS_HANDLE g_StatusHandle = nullptr;
std::atomic<bool>     g_StopSignal{false};

void UpdateStatus(DWORD currentState, DWORD win32ExitCode, DWORD waitHint) {
    static DWORD checkPoint = 1;
    g_ServiceStatus.dwCurrentState = currentState;
    g_ServiceStatus.dwWin32ExitCode = win32ExitCode;
    g_ServiceStatus.dwWaitHint = waitHint;
    g_ServiceStatus.dwCheckPoint = (currentState == SERVICE_RUNNING || currentState == SERVICE_STOPPED) ? 0 : checkPoint++;
    SetServiceStatus(g_StatusHandle, &g_ServiceStatus);
}

DWORD WINAPI ServiceCtrlHandler(DWORD dwControl, DWORD dwEventType, LPVOID lpEventData, LPVOID lpContext) {
    switch (dwControl) {
    case SERVICE_CONTROL_STOP:
    case SERVICE_CONTROL_SHUTDOWN:
        UpdateStatus(SERVICE_STOP_PENDING, NO_ERROR, 5000);
        g_StopSignal = true; // Phat tin hieu cho worker thread dung
        return NO_ERROR;
    default:
        return ERROR_CALL_NOT_IMPLEMENTED;
    }
}

void WINAPI ServiceMain(DWORD argc, LPTSTR* argv) {
    g_StatusHandle = RegisterServiceCtrlHandlerEx(L"DEXWorkerService", ServiceCtrlHandler, nullptr);
    if (!g_StatusHandle) return;

    g_ServiceStatus.dwServiceType = SERVICE_WIN32_OWN_PROCESS;
    UpdateStatus(SERVICE_START_PENDING, NO_ERROR, 3000);

    // Khoi tao tai nguyen
    UpdateStatus(SERVICE_RUNNING, NO_ERROR, 0);

    // Vong lap worker chinh
    while (!g_StopSignal) {
        Sleep(100);
    }

    // Don dep tai nguyen truoc khi dung
    UpdateStatus(SERVICE_STOPPED, NO_ERROR, 0);
}
```""",
        "antipatterns": "- **Attempting Interactive UI from Service:** Cố gắng gọi `MessageBox` hoặc tạo cửa sổ từ Windows Service, khiến tiến trình bị treo vô tận do Session 0 Isolation.\n- **Ignoring SERVICE_STOP_PENDING Checkpoints:** Thực hiện quá trình dọn dẹp kéo dài 20 giây mà không cập nhật `dwCheckPoint` cho SCM, khiến Windows coi service bị treo và kill tiến trình.\n- **Hardcoding LocalSystem Account:** Chạy service bằng tài khoản quyền lực tối cao `NT AUTHORITY\\SYSTEM` thay vì tạo tài khoản dịch vụ chuyên dụng `NT SERVICE\\<ServiceName>` với đặc quyền tối thiểu.",
        "gates": "- **QG-01**: Dịch vụ dừng hoàn toàn (Graceful Stop) trong vòng 5 giây sau khi nhận lệnh `net stop` mà không bị rò rỉ dữ liệu.\n- **QG-02**: Chính sách phục hồi (Recovery Actions) được cấu hình tự động khởi động lại dịch vụ sau khi tiến trình bị kill cưỡng bức.\n- **QG-03**: Dịch vụ hoạt động an toàn dưới tài khoản Virtual Account với nguyên tắc Least Privilege.",
        "security": "- Khóa chặt quyền truy cập Service ACL (Security Descriptor); ngăn chặn người dùng không có quyền quản trị sửa đổi đường dẫn tệp thực thi (Unquoted Service Path).",
        "adapters": "- **Runtimes**: C++ Win32 SCM API, C# TopShelf / Microsoft.Extensions.Hosting.WindowsServices, PowerShell `sc.exe`.",
        "deliverables": "- Mã nguồn dịch vụ Windows (`service_core.cpp` / `service.cs`).\n- Kịch bản cài đặt và cấu hình chính sách phục hồi tự động (`install_service.ps1`).",
        "related": "dex-windows-app-crash-dumps, dex-windows-code-signing-installer, dex-windows-usb-portability",
        "usage": "```powershell\n# Cau hinh chinh sach tu dong phuc hoi cho Service bang sc.exe\nsc.exe failure \"DEXWorkerService\" reset= 86400 actions= restart/60000/restart/120000/run/300000 command= \"C:\\Scripts\\alert.bat\"\n```"
    },
    {
        "id": "dex-windows-code-signing-installer",
        "name": "dex-windows-code-signing-installer",
        "desc": "Sign, timestamp, and verify Windows executables, DLLs, and installers (MSI, MSIX, NSIS, Inno Setup). Enforce Authenticode integrity, RFC 3161 timestamps, and smart UAC elevation handling.",
        "purpose": "Thiết kế và tự động hóa quy trình ký số mã nguồn (Code Signing) và đóng gói bộ cài đặt trên Windows; ký số điện tử theo tiêu chuẩn Microsoft Authenticode cho các tệp thực thi (`.exe`), thư viện (`.dll`) và gói cài đặt (`.msi`, `.msix`, NSIS, Inno Setup); cấu hình dấu thời gian hợp lệ theo chuẩn RFC 3161 (Secure Timestamping), loại bỏ cảnh báo Windows Defender SmartScreen và bảo đảm tính toàn vẹn của ứng dụng.",
        "when_use": "- Khi chuẩn bị xuất bản phần mềm desktop Windows ra thị trường hoặc phân phối nội bộ doanh nghiệp.\n- Khi ứng dụng bị Windows Defender SmartScreen chặn với thông báo cảnh báo màu xanh \"Windows protected your PC / Unknown Publisher\".\n- Khi cần xác minh chữ ký số tự động trong pipeline CI/CD trước khi phát hành phiên bản mới.",
        "when_not_use": "- Khi đóng gói ứng dụng cho các nền tảng di động (Android APK / iOS IPA) có quy trình ký số riêng biệt của Google/Apple.\n- Khi chỉ chạy thử nghiệm nội bộ trên máy phát triển cá nhân đã bật chế độ Developer Mode.",
        "prereqs": "- **Chứng chỉ ký số:** Chứng chỉ Code Signing hợp lệ (EV Code Signing Certificate trên Hardware Token hoặc Cloud HSM như Azure Key Vault / AWS KMS).\n- **Công cụ ký:** Microsoft `signtool.exe` trong Windows SDK.",
        "concepts": "- **Authenticode & PKCS #7:** Tiêu chuẩn mật mã của Microsoft nhúng chữ ký số và chứng chỉ X.509 vào phần thư mục bảo mật (Security Directory) của tệp định dạng PE.\n- **RFC 3161 Timestamping:** Cơ chế đóng dấu thời gian độc lập từ một Time Stamping Authority (TSA) chứng minh mã nguồn đã được ký trước khi chứng chỉ hết hạn, giúp chữ ký có hiệu lực vĩnh viễn.\n- **SmartScreen Reputation Score:** Chỉ số uy tín được tính toán bởi thuật toán đám mây của Microsoft dựa trên khối lượng tải về và chữ ký EV/Standard.",
        "workflow": "1. Biên dịch toàn bộ các tệp `.exe` và `.dll` ở cấu hình Release.\n2. Thực hiện ký số song song từng tệp nhị phân con bằng `signtool.exe` sử dụng thuật toán băm SHA-256.\n3. Đóng gói các tệp nhị phân đã ký vào bộ cài đặt (NSIS, Inno Setup, hoặc WiX Toolset MSI).\n4. Ký số chính tệp cài đặt cuối cùng kèm URL dấu thời gian RFC 3161 uy tín (DigiCert, Sectigo).\n5. Kiểm tra tính hợp lệ của chữ ký bằng lệnh `signtool verify /pa /v installer.exe`.\n6. Kiểm tra giao diện xác thực người dùng (UAC Prompt) để khẳng định tên nhà phát hành (Verified Publisher) hiển thị chuẩn xác.",
        "examples": """### Kich ban PowerShell ky so tu dong va dong dau thoi gian RFC 3161 bang signtool:
```powershell
param(
    [string]$TargetFile = "bin\\Release\\DEXDesktopApp.exe",
    [string]$CertThumbprint = "a1b2c3d4e5f6...",
    [string]$TimestampServer = "http://timestamp.digicert.com"
)

$signtool = "C:\\Program Files (x86)\\Windows Kits\\10\\bin\\10.0.22621.0\\x64\\signtool.exe"

Write-Host "Signing and Timestamping: $TargetFile"

# Ky so SHA-256 voi RFC 3161 Timestamp
& $signtool sign /sha1 $CertThumbprint `
                 /fd sha256 `
                 /tr $TimestampServer `
                 /td sha256 `
                 /v $TargetFile

if ($LASTEXITCODE -ne 0) {
    Write-Error "Code signing failed!"
    exit 1
}

# Xac minh chu ky vua ky
& $signtool verify /pa /v $TargetFile
if ($LASTEXITCODE -eq 0) {
    Write-Host "SUCCESS: Authenticode signature is 100% valid." -ForegroundColor Green
} else {
    Write-Error "Signature verification FAILED!"
    exit 1
}
```""",
        "antipatterns": "- **Omission of RFC 3161 Timestamp:** Ký số nhưng quên đóng dấu thời gian `/tr`, khiến ứng dụng bị Windows coi là không hợp lệ ngay khi chứng chỉ hết hạn 1 năm sau.\n- **Using Deprecated SHA-1 Hash:** Dùng thuật toán băm SHA-1 yếu (`/fd sha1`) bị Windows 10/11 chặn mặc định.\n- **Signing Installer but Not Bundled Binaries:** Chỉ ký tệp installer bên ngoài nhưng để các tệp `.exe` và `.dll` bên trong không có chữ ký, dẫn đến việc phần mềm diệt virus cách ly các tệp con.",
        "gates": "- **QG-01**: 100% các tệp `.exe`, `.dll` và bộ cài đặt đều có chữ ký số hợp lệ với thuật toán băm SHA-256.\n- **QG-02**: Mọi chữ ký đều chứa dấu thời gian RFC 3161 hợp lệ từ một TSA được chứng nhận.\n- **QG-03**: Hộp thoại UAC hiển thị đúng tên Verified Publisher mà không xuất hiện cảnh báo \"Unknown Publisher\".",
        "security": "- Bảo vệ tuyệt đối Private Key; không lưu chứng chỉ trong Git; sử dụng Hardware Security Module (HSM) hoặc Azure Key Vault để ký từ xa.",
        "adapters": "- **Runtimes**: Microsoft signtool.exe, Azure Trusted Signing, Inno Setup, WiX Toolset, NSIS.",
        "deliverables": "- Kịch bản ký số tự động tích hợp CI/CD (`sign_release_artifacts.ps1`).\n- Báo cáo kiểm định chữ ký số và chuỗi chứng chỉ (`code_signing_audit.json`).",
        "related": "dex-windows-service-recovery, dex-windows-usb-portability, dex-windows-app-crash-dumps",
        "usage": "```powershell\n# Kiem tra chu ky so Authenticode bang PowerShell cmdlet\nGet-AuthenticodeSignature -FilePath \".\\setup.exe\" | Format-List\n```"
    },
    {
        "id": "dex-windows-usb-portability",
        "name": "dex-windows-usb-portability",
        "desc": "Design, evaluate, and package zero-install portable Windows applications. Manage local relative pathing, registry-free configuration, runtime bundling, and safe USB execution.",
        "purpose": "Thiết kế, xây dựng và kiểm chứng ứng dụng Windows chạy độc lập không cần cài đặt (Zero-Install Portable Applications); quản lý đường dẫn tương đối (Relative Path Resolution), loại bỏ hoàn toàn sự phụ thuộc vào Windows Registry bằng cách chuyển hướng cấu hình về thư mục cục bộ (Local JSON/TOML Settings); nhúng sẵn bộ thư viện phụ thuộc (Static VC++ Runtime Linking hoặc Private Assembly Bundling) và bảo đảm ứng dụng có thể chạy trơn tru trực tiếp từ USB hoặc ổ cứng gắn ngoài.",
        "when_use": "- Khi phát triển công cụ cứu hộ hệ thống, phần mềm chẩn đoán phần cứng hoặc ứng dụng văn phòng chạy từ USB mà không cần quyền Administrator.\n- Khi người dùng muốn chạy nhiều phiên bản ứng dụng độc lập cạnh nhau trên cùng một máy tính mà không xung đột cấu hình.\n- Khi cần bảo đảm phần mềm không để lại bất kỳ dữ liệu rác (Zero-Trace) nào trong thư mục `%APPDATA%` hoặc Registry sau khi rút USB.",
        "when_not_use": "- Khi ứng dụng bắt buộc phải cài đặt Windows Kernel Driver hoặc Windows Service hệ thống (vốn yêu cầu quyền Admin và đăng ký SCM).\n- Khi ứng dụng yêu cầu tích hợp sâu vào hệ điều hành (như Shell Extension Context Menu của Windows Explorer).",
        "prereqs": "- **Kiến trúc ứng dụng:** Win32, .NET Self-Contained, Rust, hoặc Go cho phép đóng gói độc lập.\n- **Môi trường kiểm tra:** Máy tính Windows sạch (Clean VM) chưa cài đặt bất kỳ phiên bản Visual C++ Redistributable nào.",
        "concepts": "- **Relative Path Anchoring:** Luôn xác định đường dẫn gốc dựa trên vị trí của chính tệp thực thi bằng `GetModuleFileName(nullptr, ...)` thay vì tin tưởng thư mục hiện hành `GetCurrentDirectory()`.\n- **Registry Redirection / INI/JSON Storage:** Chuyển toàn bộ các giá trị cấu hình trước đây ghi vào `HKEY_CURRENT_USER\\Software\\MyApp` sang tệp `settings.json` nằm cùng thư mục ứng dụng.\n- **VCRT Static Linking (`/MT` flag):** Biên dịch ứng dụng với cờ `/MT` để nhúng thẳng mã máy của thư viện C Runtime vào tệp `.exe`, giúp ứng dụng chạy được trên máy tính thiếu VC++ Runtime.",
        "workflow": "1. Khảo sát mã nguồn và thay thế toàn bộ các lệnh đọc ghi Registry bằng module quản lý tệp cấu hình cục bộ.\n2. Cấu hình trình biên dịch bật cờ liên kết tĩnh C Runtime: `/MT` trên MSVC hoặc cấu hình Self-Contained trong `.NET` (`dotnet publish -r win-x64 --self-contained true`).\n3. Viết hàm tiện ích tính toán đường dẫn tuyệt đối cho các tệp phụ trợ dựa trên đường dẫn tệp `.exe` đang chạy.\n4. Đóng gói toàn bộ các DLL phụ trợ cần thiết trong cùng thư mục với tệp thực thi.\n5. Chạy thử nghiệm trên một máy ảo Windows sạch 100% không có kết nối internet và không cài phần mềm phụ trợ.\n6. Kiểm tra lại Registry và thư mục `%APPDATA%` để khẳng định ứng dụng không để lại dấu vết dữ liệu.",
        "examples": """### Ham lay duong dan tuyet doi an toan dua tren vi tri file EXE trong C++:
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
```""",
        "antipatterns": "- **Relying on GetCurrentDirectory():** Dùng thư mục hiện hành để tìm file dữ liệu khiến ứng dụng bị sập khi người dùng mở ứng dụng qua Shortcut hoặc qua ứng dụng khác.\n- **Dynamic VC++ Linking (/MD):** Dùng cờ `/MD` khiến ứng dụng không thể khởi động trên máy khách với thông báo lỗi thiếu `MSVCP140.dll` hoặc `VCRUNTIME140.dll`.\n- **Writing to C:\\Program Files at Runtime:** Cố ghi file cấu hình vào cùng thư mục khi ứng dụng bị người dùng copy vào `Program Files` mà không kiểm tra quyền ghi.",
        "gates": "- **QG-01**: Ứng dụng khởi chạy thành công trên máy ảo Windows sạch không cài VC++ Redistributable.\n- **QG-02**: Không tạo ra bất kỳ khóa mới nào trong Windows Registry (`HKCU` hoặc `HKLM`).\n- **QG-03**: Tất cả các đường dẫn tài nguyên nội bộ đều được giải quyết chuẩn xác bất kể ổ đĩa USB mang ký tự nào (D:, E:, F:).",
        "security": "- Kiểm tra thư mục chạy có quyền ghi hay không; nếu chạy trên USB chỉ đọc (Read-only CD/USB), chuyển hướng cấu hình an toàn về thư mục tạm trong RAM.",
        "adapters": "- **Runtimes**: C++20 (/MT), .NET 8 Self-Contained SingleFile, Rust target `x86_64-pc-windows-msvc`.",
        "deliverables": "- Lớp quản lý đường dẫn di động (`portable_paths.hpp` / `paths.rs`).\n- Bộ kiểm tra tự động phát hiện rò rỉ Registry và AppData.",
        "related": "dex-windows-code-signing-installer, dex-windows-service-recovery, dex-windows-app-startup-profiling",
        "usage": "```powershell\n# Kiem tra cac DLL phu thuoc cua ung dung bang dumpbin\ndumpbin /dependents .\\DEXApp.exe\n```"
    },
    {
        "id": "dex-windows-com-interop",
        "name": "dex-windows-com-interop",
        "desc": "Integrate, manage, and debug Component Object Model (COM) interfaces in Windows. Handle STA/MTA apartments, reference counting lifetimes, and diagnose marshaling and threading errors.",
        "purpose": "Tích hợp, điều phối và chẩn đoán các giao diện Component Object Model (COM / OLE / ActiveX) trong hệ điều hành Windows; khởi tạo và quản lý an toàn căn hộ luồng (Single-Threaded Apartments - STA vs Multi-Threaded Apartments - MTA) thông qua `CoInitializeEx`; quản lý vòng đời đếm tham chiếu (Reference Counting: `AddRef`, `Release`, CComPtr, winrt::com_ptr), ngăn chặn rò rỉ bộ nhớ COM và xử lý các lỗi truyền đối tượng xuyên luồng (Cross-Apartment Marshaling Errors: `RPC_E_WRONG_THREAD`).",
        "when_use": "- Khi tương tác với các API hệ thống Windows cốt lõi chỉ hỗ trợ COM (Windows Shell, Taskbar Progress, UI Automation, WMI, DirectShow, Media Foundation).\n- Khi tích hợp hoặc xây dựng các phần mở rộng cho bộ ứng dụng Microsoft Office qua COM Add-in.\n- Khi ứng dụng bị sập hoặc trả về mã lỗi `CO_E_NOTINITIALIZED`, `REGDB_E_CLASSNOTREG` hoặc `RPC_E_WRONG_THREAD`.",
        "when_not_use": "- Khi sử dụng các API Win32 thuần túy hoặc các dịch vụ mạng REST/gRPC không yêu cầu cơ chế COM.\n- Khi phát triển ứng dụng trên Linux hoặc macOS nơi COM không được hỗ trợ tự nhiên.",
        "prereqs": "- **Môi trường phát triển:** C++ (ATL/WRL/C++/WinRT), C# (COM Interop), hoặc Rust (`windows-rs`).\n- **Thư viện hệ thống:** `ole32.lib`, `oleaut32.lib`.",
        "concepts": "- **Apartment Threading Models (STA vs MTA):** STA ràng buộc các đối tượng COM với một luồng cụ thể và sử dụng Message Loop để đồng bộ hóa; MTA cho phép nhiều luồng gọi đồng thời vào đối tượng nhưng đòi hỏi đối tượng phải có cơ chế khóa an toàn (Thread-safe).\n- **Reference Counting Semantics:** Mỗi khi con trỏ COM được sao chép, phải gọi `AddRef()`; khi không sử dụng nữa, bắt buộc gọi `Release()`. Khi số đếm về 0, đối tượng tự hủy khỏi bộ nhớ.\n- **Interface Querying (IUnknown::QueryInterface):** Cơ chế định danh runtime chuẩn của COM cho phép kiểm tra và chuyển đổi giữa các giao diện của cùng một đối tượng dựa trên mã GUID/IID.",
        "workflow": "1. Khởi tạo COM Apartment phù hợp cho luồng hiện tại: `CoInitializeEx(nullptr, COINIT_APARTMENTTHREADED)` cho GUI hoặc `COINIT_MULTITHREADED` cho Worker.\n2. Sử dụng Smart Pointer chuyên dụng (`_com_ptr_t`, `CComPtr`, hoặc `winrt::com_ptr`) để tự động hóa việc gọi `Release()`.\n3. Tạo phiên bản đối tượng COM bằng hàm `CoCreateInstance()` với CLSID và IID mục tiêu.\n4. Thực hiện các thao tác trên giao diện và xử lý mã trả về `HRESULT` bằng macro `FAILED(hr)` hoặc `SUCCEEDED(hr)`.\n5. Nếu cần truyền con trỏ COM sang một luồng khác, sử dụng `RoGetAgileReference` hoặc `CoMarshalInterThreadInterfaceInStream` để sinh proxy an toàn.\n6. Đóng căn hộ COM bằng `CoUninitialize()` khi luồng kết thúc.",
        "examples": """### Tich hop Taskbar Progress API thong qua ITaskbarList3 COM Interface trong C++:
```cpp
#include <windows.h>
#include <shobjidl.h>
#include <wrl/client.h> // Microsoft::WRL::ComPtr
#include <iostream>

using Microsoft::WRL::ComPtr;

void update_taskbar_progress(HWND hWnd, ULONGLONG completed, ULONGLONG total) {
    // 1. Khoi tao COM cho luong GUI (STA)
    HRESULT hr = CoInitializeEx(nullptr, COINIT_APARTMENTTHREADED);
    if (FAILED(hr) && hr != RPC_E_CHANGED_MODE) {
        std::cerr << "Failed to init COM. HRESULT: " << std::hex << hr << std::endl;
        return;
    }

    // 2. Tao ComPtr quan ly vong doi tu dong
    ComPtr<ITaskbarList3> pTaskbar;
    hr = CoCreateInstance(CLSID_TaskbarList, nullptr, CLSCTX_INPROC_SERVER, IID_PPV_ARGS(&pTaskbar));
    
    if (SUCCEEDED(hr)) {
        pTaskbar->HrInit();
        // 3. Cap nhat thanh tien trinh tren Taskbar icon
        pTaskbar->SetProgressValue(hWnd, completed, total);
        pTaskbar->SetProgressState(hWnd, TBPF_NORMAL);
        std::cout << "Taskbar progress updated: " << completed << "/" << total << std::endl;
    } else {
        std::cerr << "CoCreateInstance failed. HRESULT: " << std::hex << hr << std::endl;
    }

    // Luu y: ComPtr tu dong goi Release() khi ra khoi scope
    CoUninitialize();
}
```""",
        "antipatterns": "- **Calling COM without CoInitializeEx:** Gọi các API COM trên luồng mới mà quên khởi tạo căn hộ luồng khiến hàm trả về lỗi `CO_E_NOTINITIALIZED`.\n- **Manual AddRef/Release Leaks:** Quản lý con trỏ COM bằng tay không dùng Smart Pointer, dẫn đến việc quên gọi `Release()` khi gặp nhánh rẽ lỗi (Exception) gây rò rỉ bộ nhớ.\n- **Passing Raw STA Pointer to MTA Thread:** Chia sẻ con trỏ giao diện STA cho luồng worker gọi trực tiếp mà không qua Marshaling, dẫn đến lỗi sập hoặc trả mã `RPC_E_WRONG_THREAD`.",
        "gates": "- **QG-01**: 100% các đối tượng COM được quản lý bởi Smart Pointers an toàn (`ComPtr`), 0 lỗi rò rỉ tham chiếu.\n- **QG-02**: Mọi cuộc gọi COM API đều kiểm tra mã trả về `HRESULT` bằng macro `SUCCEEDED` hoặc `FAILED`.\n- **QG-03**: Khởi tạo và giải phóng căn hộ luồng (`CoInitializeEx` / `CoUninitialize`) cân bằng chính xác trên mỗi luồng.",
        "security": "- Tránh nạp các COM Inproc Server không rõ nguồn gốc; kiểm tra tính toàn vẹn của đăng ký CLSID trong Registry.",
        "adapters": "- **Runtimes**: C++ (WRL, ATL, C++/WinRT), C# .NET COM Interop, Rust windows-rs.",
        "deliverables": "- Lớp bao bọc đối tượng COM tiện ích (`com_utility.hpp` / `com.rs`).\n- Bộ kiểm thử tự động xác minh quản lý vòng đời và bắt lỗi căn hộ luồng.",
        "related": "dex-windows-native-ui-accessibility, dex-windows-input-api-integration, dex-windows-service-recovery",
        "usage": "```powershell\n# Truy van cac COM Class duoc dang ky trong he thong bang PowerShell\nGet-ChildItem -Path Registry::HKEY_CLASSES_ROOT\\CLSID | Select-Object -First 10\n```"
    },
    {
        "id": "dex-windows-native-ui-accessibility",
        "name": "dex-windows-native-ui-accessibility",
        "desc": "Implement, test, and audit Windows UI Automation (UIA) and accessibility interfaces. Support screen readers (Narrator, NVDA), keyboard navigation, focus indicators, and High Contrast mode.",
        "purpose": "Thiết kế, tích hợp và kiểm chứng tiêu chuẩn tiếp cận người khuyết tật trên ứng dụng desktop Windows (Windows Accessibility & UI Automation - UIA); cài đặt các nhà cung cấp giao diện UIA (`IRawElementProviderSimple`, `IInvokeProvider`, `IValueProvider`); bảo đảm khả năng hỗ trợ hoàn hảo cho các trình đọc màn hình phổ biến (Windows Narrator, NVDA, JAWS), điều hướng bàn phím toàn diện (Tab Order, Focus Indicators) và khả năng thích ứng với giao diện tương phản cao (Windows High Contrast Themes).",
        "when_use": "- Khi phát triển các thành phần điều khiển giao diện người dùng tùy biến (Custom UI Controls) trong Win32 hoặc C++ cần hỗ trợ người khiếm thị.\n- Khi đáp ứng các tiêu chuẩn pháp lý về khả năng tiếp cận phần mềm của doanh nghiệp hoặc chính phủ (Section 508, WCAG 2.1 AA, EN 301 549).\n- Khi tự động hóa kiểm thử giao diện desktop thông qua cây phần tử Windows UI Automation Tree.",
        "when_not_use": "- Khi sử dụng các thành phần điều khiển chuẩn của hệ thống (Standard Windows Buttons/Edits) đã được OS tích hợp sẵn UIA mặc định.\n- Khi xây dựng ứng dụng dịch vụ chạy ngầm không có thành phần hiển thị giao diện.",
        "prereqs": "- **Công cụ kiểm tra:** Windows SDK Accessibility Insights for Windows, Inspect.exe, hoặc AccScope.\n- **Trình đọc màn hình:** Windows Narrator (phím tắt Win + Ctrl + Enter) hoặc NVDA.",
        "concepts": "- **UI Automation Tree:** Cấu trúc phân cấp hình cây phản ánh giao diện ứng dụng cho các công nghệ trợ năng, bao gồm các phần tử cha, con và anh em.\n- **Control Patterns:** Các giao diện xác định hành vi của phần tử: ví dụ `IInvokeProvider` cho nút bấm, `IToggleProvider` cho checkbox, `IRangeValueProvider` cho slider.\n- **Automation Events:** Các thông báo phát ra khi trạng thái giao diện thay đổi (ví dụ `UiaRaiseAutomationEvent` khi nút được click hoặc giá trị text thay đổi).",
        "workflow": "1. Khảo sát các thành phần giao diện tùy biến (Custom Controls) chưa có nhà cung cấp trợ năng.\n2. Cài đặt giao diện `IRawElementProviderSimple` cho cửa sổ tùy biến trong hàm xử lý thông điệp `WM_GETOBJECT`.\n3. Cung cấp các thuộc tính UIA cơ bản: `UIA_NamePropertyId`, `UIA_ControlTypePropertyId`, `UIA_LocalizedControlTypePropertyId`.\n4. Cài đặt các Control Patterns phù hợp với hành vi nghiệp vụ của phần tử.\n5. Bật Windows Narrator hoặc công cụ Inspect.exe để quét kiểm tra cây UI Automation.\n6. Xác nhận việc nhận diện chính xác tên nút, trạng thái kích hoạt và điều hướng phím Tab.",
        "examples": """### Cai dat nha cung cap UIA co ban cho Custom Control trong Win32:
```cpp
#include <windows.h>
#include <uiautomation.h>
#include <iostream>

class CustomButtonProvider : public IRawElementProviderSimple, public IInvokeProvider {
private:
    LONG m_refCount = 1;
    HWND m_hwnd;

public:
    CustomButtonProvider(HWND hwnd) : m_hwnd(hwnd) {}

    // IUnknown
    ULONG STDMETHODCALLTYPE AddRef() override { return InterlockedIncrement(&m_refCount); }
    ULONG STDMETHODCALLTYPE Release() override {
        LONG val = InterlockedDecrement(&m_refCount);
        if (val == 0) delete this;
        return val;
    }
    HRESULT STDMETHODCALLTYPE QueryInterface(REFIID riid, void** ppv) override {
        if (riid == IID_IUnknown || riid == IID_IRawElementProviderSimple) {
            *ppv = static_cast<IRawElementProviderSimple*>(this);
        } else if (riid == IID_IInvokeProvider) {
            *ppv = static_cast<IInvokeProvider*>(this);
        } else {
            *ppv = nullptr;
            return E_NOINTERFACE;
        }
        AddRef();
        return S_OK;
    }

    // IRawElementProviderSimple
    HRESULT STDMETHODCALLTYPE get_ProviderOptions(ProviderOptions* pRetVal) override {
        *pRetVal = ProviderOptions_ServerSideProvider;
        return S_OK;
    }
    HRESULT STDMETHODCALLTYPE GetPatternProvider(PATTERNID patternId, IUnknown** pRetVal) override {
        if (patternId == UIA_InvokePatternId) {
            *pRetVal = static_cast<IInvokeProvider*>(this);
            AddRef();
            return S_OK;
        }
        *pRetVal = nullptr;
        return S_OK;
    }
    HRESULT STDMETHODCALLTYPE GetPropertyValue(PROPERTYID propertyId, VARIANT* pRetVal) override {
        if (propertyId == UIA_ControlTypePropertyId) {
            pRetVal->vt = VT_I4;
            pRetVal->lVal = UIA_ButtonControlTypeId;
        } else if (propertyId == UIA_NamePropertyId) {
            pRetVal->vt = VT_BSTR;
            pRetVal->bstrVal = SysAllocString(L"Submit Order");
        } else {
            pRetVal->vt = VT_EMPTY;
        }
        return S_OK;
    }
    HRESULT STDMETHODCALLTYPE get_HostRawElementProvider(IRawElementProviderSimple** pRetVal) override {
        return UiaHostProviderFromHwnd(m_hwnd, pRetVal);
    }

    // IInvokeProvider
    HRESULT STDMETHODCALLTYPE Invoke() override {
        SendMessage(m_hwnd, BM_CLICK, 0, 0);
        return S_OK;
    }
};
```""",
        "antipatterns": "- **Missing WM_GETOBJECT Handler:** Tự vẽ nút bấm đồ họa phức tạp nhưng không bắt thông điệp `WM_GETOBJECT` khiến trình đọc màn hình coi cửa sổ là một vùng đen hoàn toàn.\n- **Unlabeled Graphic Buttons:** Nút bấm chỉ hiển thị icon mà không cung cấp chuỗi `UIA_NamePropertyId`, khiến Narrator chỉ đọc \"Button\" không rõ chức năng.\n- **Trapping Keyboard Focus:** Thiết kế danh sách phần tử khiến người dùng nhấn phím Tab bị kẹt lại vĩnh viễn không thể chuyển tới phần tử tiếp theo.",
        "gates": "- **QG-01**: 100% các phần tử tương tác tùy biến đều hiển thị đầy đủ tên, vai trò và trạng thái trong công cụ Inspect.exe.\n- **QG-02**: Trình đọc màn hình Windows Narrator đọc chính xác nội dung và hướng dẫn khi con trỏ bàn phím di chuyển tới.\n- **QG-03**: Toàn bộ luồng nghiệp vụ của ứng dụng có thể hoàn thành 100% chỉ bằng bàn phím mà không cần chạm vào chuột.",
        "security": "- Đảm bảo các hàm cung cấp chuỗi UIA không làm lộ các thông tin nhạy cảm (như mật khẩu trong trường Password).",
        "adapters": "- **Runtimes**: Windows UI Automation API, Accessibility Insights, Windows Narrator, NVDA screen reader.",
        "deliverables": "- Lớp nhà cung cấp trợ năng Windows UIA (`uia_custom_provider.cpp`).\n- Báo cáo kiểm định khả năng tiếp cận phần mềm (`accessibility_inspection.json`).",
        "related": "dex-windows-input-api-integration, dex-win32-dpi-multi-monitor-layout, dex-windows-com-interop",
        "usage": "```powershell\n# Kiem tra cay UIA cua ung dung bang Accessibility Insights CLI hoac PowerShell\nAdd-Type -AssemblyName UIAutomationClient\n$root = [System.Windows.Automation.AutomationElement]::RootElement\nWrite-Host \"Root Name: \" $root.Current.Name\n```"
    },
    {
        "id": "dex-desktop-gpu-inference-fallback",
        "name": "dex-desktop-gpu-inference-fallback",
        "desc": "Integrate desktop GPU AI inference engines (DirectML, ONNX Runtime, CUDA, Vulkan). Detect hardware capabilities and manage seamless fallback to optimized multi-threaded CPU paths.",
        "purpose": "Tích hợp và tối ưu hóa suy luận mô hình trí tuệ nhân tạo tăng tốc phần cứng (Desktop GPU Inference) cho ứng dụng máy tính cá nhân; cấu hình các Execution Providers tiên tiến (DirectML cho card đồ họa AMD/Intel/NVIDIA trên Windows, ONNX Runtime, Vulkan, TensorRT); tự động nhận diện năng lực thiết bị (Adapter Enumeration qua DirectX/DXGI) và xây dựng đường dự phòng chuyển tiếp mượt mà (Seamless CPU Fallback) sang tập lệnh CPU đa luồng (OpenVINO, AVX2/AVX-512) khi thiết bị không đủ VRAM hoặc thiếu driver phù hợp.",
        "when_use": "- Khi tích hợp các mô hình nơ-ron cục bộ (Local LLM, Whisper Audio Transcription, Object Detection, Background Removal) vào ứng dụng desktop.\n- Khi ứng dụng bị sập với lỗi Out of Device Memory (VRAM Exhaustion) trên các máy tính sử dụng card đồ họa tích hợp (iGPU).\n- Khi cần phần mềm chạy được trên 100% thiết bị của người dùng bất kể có card đồ họa rời hay không.",
        "when_not_use": "- Khi gọi các mô hình AI thông qua Cloud API (OpenAI, Anthropic, Gemini) nơi việc suy luận diễn ra trên máy chủ từ xa.\n- Khi khối lượng suy luận quá nhỏ (<1ms) mà chi phí sao chép dữ liệu từ CPU sang GPU (PCIe transfer overhead) lớn hơn thời gian tính toán.",
        "prereqs": "- **Hệ điều hành:** Windows 10/11 x64, DirectX 12 Agility SDK.\n- **Thư viện AI:** ONNX Runtime (`onnxruntime-directml`), DirectML SDK, hoặc llama.cpp.",
        "concepts": "- **DirectML (DirectX Machine Learning):** API tăng tốc học máy cấp thấp của Microsoft hoạt động trên mọi card đồ họa tương thích DirectX 12 của Intel, AMD, NVIDIA và Qualcomm.\n- **VRAM Budget Management:** Kiểm tra dung lượng bộ nhớ video khả dụng trước khi nạp mô hình; nếu mô hình yêu cầu 4GB VRAM nhưng máy chỉ còn 1.5GB, lập tức kích hoạt đường CPU Fallback.\n- **Execution Provider Priority Chain:** Chuỗi ưu tiên nạp backend: DirectML GPU -> OpenVINO NPU/CPU -> Multithreaded AVX2 CPU.",
        "workflow": "1. Sử dụng DXGI API (`IDXGIFactory6::EnumAdapterByGpuPreference`) để liệt kê tất cả card đồ họa có trên hệ thống.\n2. Kiểm tra dung lượng bộ nhớ video chuyên dụng (`DedicatedVideoMemory`) và phiên bản tính năng DirectX 12 (`D3D_FEATURE_LEVEL_12_0`).\n3. Thử nghiệm khởi tạo ONNX Runtime InferenceSession với DirectML Execution Provider trong khối kiểm soát ngoại lệ.\n4. Nếu khởi tạo thất bại (thiếu driver, không đủ VRAM), ghi log cảnh báo và chuyển sang CPU Execution Provider với các cờ tối ưu hóa luồng (`intra_op_num_threads`).\n5. Thực hiện suy luận thử nghiệm trên một tensor nhỏ (Warm-up Inference) để biên dịch shader đồ họa trước khi xử lý dữ liệu thật.\n6. Theo dõi mức tiêu thụ bộ nhớ và giải phóng tài nguyên session khi người dùng đóng tính năng.",
        "examples": """### Khoi tao ONNX Runtime linh hoat ho tro DirectML GPU va CPU Fallback trong C++:
```cpp
#include <onnxruntime_cxx_api.h>
#include <dml_provider_factory.h>
#include <dxgi1_6.h>
#include <iostream>
#include <memory>

std::unique_ptr<Ort::Session> create_inference_session(Ort::Env& env, const wchar_t* model_path) {
    Ort::SessionOptions session_options;
    session_options.SetGraphOptimizationLevel(GraphOptimizationLevel::ORT_ENABLE_ALL);

    bool gpu_initialized = false;

    // 1. Thu nghiem khoi tao DirectML GPU Backend
    try {
        // ID device 0 la GPU chinh
        OrtStatus* status = OrtSessionOptionsAppendExecutionProvider_DML(session_options, 0);
        if (status == nullptr) {
            auto session = std::make_unique<Ort::Session>(env, model_path, session_options);
            std::cout << "[AI ENGINE] Hardware Acceleration enabled via DirectML (GPU)." << std::endl;
            gpu_initialized = true;
            return session;
        }
    } catch (const std::exception& ex) {
        std::cerr << "[WARN] DirectML GPU init failed: " << ex.what() << ". Falling back to CPU..." << std::endl;
    }

    // 2. Fallback sang CPU da luong neu GPU that bai
    if (!gpu_initialized) {
        Ort::SessionOptions cpu_options;
        cpu_options.SetIntraOpNumThreads(4); // 4 luong CPU
        cpu_options.SetGraphOptimizationLevel(GraphOptimizationLevel::ORT_ENABLE_ALL);
        auto session = std::make_unique<Ort::Session>(env, model_path, cpu_options);
        std::cout << "[AI ENGINE] Running on Portable Optimized CPU Fallback." << std::endl;
        return session;
    }
    return nullptr;
}
```""",
        "antipatterns": "- **Unbounded GPU Memory Allocation:** Cố ép mô hình lớn 8GB vào card iGPU chia sẻ RAM hệ thống khiến toàn bộ máy tính bị đứng hình (TDR - Timeout Detection and Recovery).\n- **Hardcoded CUDA Dependency:** Chỉ hỗ trợ CUDA khiến 100% người dùng sử dụng card đồ họa AMD Radeon hoặc Intel Arc không thể sử dụng tính năng AI.\n- **Freezing UI Thread on Warm-up:** Chạy lượt suy luận warm-up đầu tiên trên Main Thread làm giao diện bị đơ 3-5 giây trong khi DirectML biên dịch pipeline state objects.",
        "gates": "- **QG-01**: Tự động nhận diện GPU và kích hoạt DirectML thành công trên các phần cứng có hỗ trợ DirectX 12.\n- **QG-02**: Tự động chuyển đổi sang CPU Fallback an toàn 100% khi chạy trên môi trường không có GPU hoặc khi GPU bị lỗi bộ nhớ.\n- **QG-03**: Kết quả đầu ra của mô hình giữa chế độ GPU và chế độ CPU hoàn toàn đồng nhất về mặt toán học.",
        "security": "- Quét kiểm tra tệp mô hình ONNX trước khi nạp; ngăn ngừa các mô hình chứa cấu trúc đồ thị độc hại (Model Serialization Exploits).",
        "adapters": "- **Runtimes**: ONNX Runtime DirectML, DirectX 12 / DXGI, PyTorch DirectML, OpenVINO CPU.",
        "deliverables": "- Lớp quản lý bộ máy suy luận AI đa nền tảng (`desktop_ai_engine.cpp` / `inference.rs`).\n- Báo cáo đo kiểm hiệu năng suy luận so sánh giữa GPU và CPU fallback.",
        "related": "dex-native-simd-dispatch, dex-windows-app-crash-dumps, dex-windows-app-startup-profiling",
        "usage": "```powershell\n# Kiem tra danh sach card do hoa DirectX tren may tinh bang dxdiag\ndxdiag /t dxdiag_report.txt; Select-String \"Card name:\" dxdiag_report.txt\n```"
    },

    # =========================================================================
    # GROUP AT: Platform Resilience & Infrastructure (Skills 451–460)
    # =========================================================================
    {
        "id": "dex-cloud-database-failover-drills",
        "name": "dex-cloud-database-failover-drills",
        "desc": "Plan, orchestrate, and audit cloud database failover drills (AWS RDS Multi-AZ, Azure Flexible, Cloud SQL HA). Verify RTO, RPO, connection pool draining, and client reconnection.",
        "purpose": "Lập kế hoạch, điều phối và kiểm toán các cuộc diễn tập chuyển đổi dự phòng cơ sở dữ liệu đám mây (Cloud Database Failover Drills: AWS RDS Multi-AZ, Azure Database Flexible Server HA, Google Cloud SQL HA); đo lường thực tế thời gian phục hồi mục tiêu (Recovery Time Objective - RTO) và điểm phục hồi mục tiêu (Recovery Point Objective - RPO); kiểm chứng tính bền bỉ của vùng đệm kết nối ứng dụng (Connection Pool Draining & Reconnection Logic), bảo đảm không xảy ra mất mát dữ liệu hoặc gián đoạn dịch vụ kéo dài.",
        "when_use": "- Khi tiến hành diễn tập khắc phục thảm họa định kỳ (Disaster Recovery GameDay) cho hệ thống tài chính, ngân hàng hoặc thương mại điện tử.\n- Khi cấu hình hoặc nâng cấp các cụm CSDL đám mây sang kiến trúc Multi-AZ hoặc Read-Replica tự động thăng cấp.\n- Khi kiểm thử khả năng tự động kết nối lại (Auto-reconnect with Exponential Backoff) của các backend microservices.",
        "when_not_use": "- Khi cơ sở dữ liệu chỉ là môi trường phát triển cục bộ một node duy nhất (Single-Instance Local Dev).\n- Khi bảo trì nâng cấp phần mềm ứng dụng thông thường không liên quan tới tầng lưu trữ dữ liệu.",
        "prereqs": "- **Hạ tầng CSDL:** Cụm CSDL đám mây đã bật cơ chế High Availability (Multi-AZ replication).\n- **Công cụ điều phối:** AWS CLI, Azure CLI, hoặc Terraform/Chaos Engineering tools (Chaos Mesh, Gremlin).",
        "concepts": "- **RTO (Recovery Time Objective):** Khoảng thời gian tối đa cho phép hệ thống CSDL ngừng trệ trước khi khôi phục lại trạng thái hoạt động bình thường (thường mục tiêu < 60s cho Multi-AZ).\n- **RPO (Recovery Point Objective):** Lượng dữ liệu tối đa chấp nhận bị mất mát tính theo đơn vị thời gian do sự cố (mục tiêu RPO = 0 cho replication đồng bộ).\n- **Split-Brain Prevention:** Cơ chế giải quyết tranh chấp ngăn chặn hai node CSDL cùng nhận quyền ghi (Primary) tại cùng một thời điểm.",
        "workflow": "1. Thiết lập giám sát liên tục luồng giao dịch của ứng dụng với tải giả lập (Synthetic Traffic Generator).\n2. Kích hoạt lệnh chuyển đổi dự phòng có chủ đích: `aws rds reboot-db-instance --force-failover`.\n3. Đo đạc chính xác thời điểm máy chủ chính bắt đầu ngừng nhận kết nối (t0) đến khi replica được thăng cấp và DNS chuyển hướng hoàn tất (t1).\n4. Theo dõi phản ứng của backend pooler (HikariCP, PgBouncer): ghi nhận tỷ lệ lỗi kết nối và thời gian tự phục hồi.\n5. Thực hiện kiểm toán toàn vẹn dữ liệu: đối chiếu số lượng bản ghi ghi nhận được trong suốt thời gian diễn tập.\n6. Lập báo cáo kiểm toán diễn tập failover kèm biểu đồ phân tích độ trễ và các khuyến nghị tối ưu tham số timeout.",
        "examples": """### Kich ban tu dong hoa dien tap failover AWS RDS va do RTO bang Python:
```python
import boto3
import time
import psycopg2

RDS_IDENTIFIER = "production-postgres-ha"
DB_HOST = "production-postgres-ha.cxyz.us-east-1.rds.amazonaws.com"

def measure_database_failover():
    rds = boto3.client('rds', region_name='us-east-1')
    print(f"Triggering manual failover for {RDS_IDENTIFIER}...")
    
    start_time = time.time()
    rds.reboot_db_instance(DBInstanceIdentifier=RDS_IDENTIFIER, ForceFailover=True)
    
    downtime_start = None
    recovered_time = None
    
    # Vong lap kiem tra ket noi moi 1 giay
    for attempt in range(120):
        try:
            conn = psycopg2.connect(
                host=DB_HOST, dbname="app_db", user="db_user",
                password="secret_password", connect_timeout=2
            )
            cur = conn.cursor()
            cur.execute("SELECT inet_server_addr(), now();")
            server_ip, current_ts = cur.fetchone()
            conn.close()
            
            if downtime_start and not recovered_time:
                recovered_time = time.time()
                rto_seconds = recovered_time - downtime_start
                print(f"[RECOVERED] Failover completed! RTO: {rto_seconds:.2f}s | New Master IP: {server_ip}")
                break
            print(f"[{attempt}s] Connection healthy to master ({server_ip})")
        except Exception as e:
            if not downtime_start:
                downtime_start = time.time()
                print(f"[OUTAGE DETECTED] Master unreachable at {downtime_start - start_time:.2f}s mark.")
        time.sleep(1)

measure_database_failover()
```""",
        "antipatterns": "- **Infinite Connection Pool Timeout:** Đặt `connectionTimeout` trong pooler quá lớn (ví dụ 60 giây) khiến các luồng ứng dụng bị treo chờ đợi thay vì fail-fast và retry.\n- **Hardcoded Master IP Addresses:** Cấu hình ứng dụng kết nối trực tiếp vào địa chỉ IP tĩnh thay vì sử dụng DNS CNAME Endpoint của AWS RDS, khiến ứng dụng không tự chuyển hướng sau khi failover.\n- **Conducting Drills in Production Without Rollback Plan:** Diễn tập failover trên môi trường production trong giờ cao điểm mà không có kịch bản hủy khẩn cấp khi hệ thống replica bị trễ sao chép (replication lag).",
        "gates": "- **QG-01**: Thời gian RTO thực tế đo được không vượt quá 60 giây trong suốt quá trình chuyển đổi dự phòng.\n- **QG-02**: Không có bất kỳ giao dịch nào đã commit thành công bị mất mát dữ liệu (RPO = 0).\n- **QG-03**: Backend connection pooler tự động kết nối lại 100% các kết nối sạch sau khi node mới thăng cấp.",
        "security": "- Diễn tập phải được cấp quyền hạn thông qua Ticket phê duyệt thay đổi (Change Request) có chữ ký của Security & Reliability Lead.",
        "adapters": "- **Runtimes**: AWS RDS Multi-AZ, Azure Database Flexible Server, Cloud SQL HA, Chaos Mesh, PgBouncer.",
        "deliverables": "- Kịch bản điều phối diễn tập tự động (`failover_drill_runner.py`).\n- Báo cáo kết quả kiểm toán thời gian gián đoạn và RTO/RPO (`failover_audit_report.md`).",
        "related": "dex-api-circuit-breaker-verification, dex-storage-backup-restore-drills, dex-operational-dependency-mapping",
        "usage": "```bash\n# Kich hoat failover co cuong che bang AWS CLI\naws rds reboot-db-instance --db-instance-identifier mydb --force-failover\n```"
    },
    {
        "id": "dex-kubernetes-secret-delivery",
        "name": "dex-kubernetes-secret-delivery",
        "desc": "Architect, enforce, and audit secure secret delivery to Kubernetes workloads. Integrate External Secrets Operator, Vault Agent sidecars, and verify safe credential rotation.",
        "purpose": "Thiết kế, tích hợp và kiểm toán cơ chế phân phối bí mật an toàn cho các ứng dụng chạy trên Kubernetes (Kubernetes Secret Delivery Architecture); loại bỏ hoàn toàn việc lưu trữ bí mật dạng plaintext trong kho mã nguồn Git; tích hợp External Secrets Operator (ESO), HashiCorp Vault Agent Sidecar hoặc CSI Secret Store Driver; thực thi nguyên tắc đặc quyền tối thiểu (Least Privilege RBAC), cấp phát bí mật qua bộ nhớ tạm (tmpfs memory volumes) và tự động tải lại ứng dụng khi chứng chỉ/khóa được xoay vòng (Zero-Downtime Secret Rotation).",
        "when_use": "- Khi triển khai các ứng dụng microservices trên cụm Kubernetes yêu cầu truy cập mật khẩu CSDL, API Token, hoặc chứng chỉ TLS.\n- Khi chuyển đổi từ cơ chế Secret tĩnh của Kubernetes (base64 mã hóa yếu) sang cơ chế quản lý tập trung từ Cloud KMS (AWS Secrets Manager, Azure Key Vault, HashiCorp Vault).\n- Khi kiểm toán an ninh phát hiện bí mật bị lộ trong tệp cấu hình YAML hoặc lịch sử commit Git.",
        "when_not_use": "- Khi cấu hình các thông số không nhạy cảm (như URL public, cổng dịch vụ, tên môi trường - nên dùng ConfigMap thông thường).\n- Khi ứng dụng chạy trên môi trường máy chủ đơn lẻ không sử dụng bộ điều phối container Kubernetes.",
        "prereqs": "- **Hạ tầng cụm:** Kubernetes 1.25+, Helm 3.0+.\n- **Hệ thống quản lý khóa:** AWS Secrets Manager, HashiCorp Vault, hoặc GCP Secret Manager.",
        "concepts": "- **External Secrets Operator (ESO):** Bộ điều khiển Kubernetes Kubernetes Controller đồng bộ hóa dữ liệu từ các nhà cung cấp bên ngoài (External APIs) thành các native `Secret` trong cluster.\n- **tmpfs In-Memory Volume:** Cơ chế gắn thư mục bí mật vào Pod dưới dạng RAM ảo, bảo đảm bí mật không bao giờ bị ghi xuống ổ đĩa cứng của node Kubernetes.\n- **Reloader Controller:** Công cụ tự động kích hoạt Rolling Restart cho Deployment khi các Secret hoặc ConfigMap được cập nhật giá trị mới.",
        "workflow": "1. Cài đặt External Secrets Operator trên cụm thông qua Helm Chart chính thức.\n2. Thiết lập định danh bảo mật `ClusterSecretStore` sử dụng Kubernetes ServiceAccount kết nối tới AWS IAM Role (IRSA) hoặc Vault Role.\n3. Định nghĩa đối tượng `ExternalSecret` ánh xạ từng khóa từ Cloud Secrets Manager sang Kubernetes Secret nội bộ.\n4. Gắn Secret vào Pod thông qua Volume Mount (`mountPath: /var/run/secrets/app`) hoặc biến môi trường tham chiếu.\n5. Cấu hình cờ `stakater.com/auto: \"true\"` trên Pod template để tự động reload khi secret thay đổi.\n6. Kiểm tra quyền truy cập của Pod và khẳng định tiến trình bên trong Pod không thể đọc được secret của các namespace khác.",
        "examples": """### Cau hinh ExternalSecret dong bo hoa tu AWS Secrets Manager:
```yaml
apiVersion: external-secrets.io/v1beta1
kind: ClusterSecretStore
metadata:
  name: aws-secretsmanager-store
spec:
  provider:
    aws:
      service: SecretsManager
      region: us-east-1
      auth:
        jwt:
          serviceAccountRef:
            name: eso-service-account
            namespace: external-secrets
---
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: database-credentials
  namespace: production
spec:
  refreshInterval: 1h # Tu dong quet xoay vong bi mat moi gio
  secretStoreRef:
    name: aws-secretsmanager-store
    kind: ClusterSecretStore
  target:
    name: db-app-secret
    creationPolicy: Owner
  data:
    - secretKey: DB_PASSWORD
      remoteRef:
        key: production/database
        property: password
    - secretKey: DB_USERNAME
      remoteRef:
        key: production/database
        property: username
```""",
        "antipatterns": "- **Committing Base64 Secrets in Git:** Đẩy các tệp `Secret.yaml` chứa chuỗi mã hóa base64 lên Git với suy nghĩ sai lầm rằng base64 là một hình thức mã hóa bảo mật.\n- **Passing Secrets via Process CLI Arguments:** Truyền mật khẩu dưới dạng tham số dòng lệnh `args: [\"--password\", \"$(SECRET)\"]` khiến mật khẩu hiển thị rõ ràng trong lệnh `ps aux` hoặc Kubernetes API.\n- **Root-Accessible Shared Volumes:** Gắn secret vào volume nhưng để quyền tệp là `0777` cho phép bất kỳ container nào cùng Pod đều đọc được dữ liệu nhạy cảm.",
        "gates": "- **QG-01**: 100% bí mật trong cụm được đồng bộ tự động từ External Secrets Store, 0 bí mật tĩnh trong Git.\n- **QG-02**: Mọi volume gắn secret đều có quyền phân quyền tệp giới hạn nghiêm ngặt `defaultMode: 0400`.\n- **QG-03**: Quá trình xoay vòng bí mật (Secret Rotation) kích hoạt cập nhật Pod tự động mà không gây gián đoạn dịch vụ.",
        "security": "- Bật mã hóa dữ liệu Secret khi lưu trữ tại tầng etcd (Encryption at Rest with KMS Provider) trên toàn cụm Kubernetes.",
        "adapters": "- **Runtimes**: External Secrets Operator, HashiCorp Vault Agent, Kubernetes CSI Driver, AWS Secrets Manager.",
        "deliverables": "- Lược đồ khai báo External Secrets chuẩn mẫu (`external_secret_template.yaml`).\n- Kịch bản kiểm toán rà soát cấu hình phân quyền Secret RBAC (`audit_k8s_secrets.sh`).",
        "related": "dex-infrastructure-policy-as-code, dex-cloud-database-failover-drills, dex-platform-selfservice-templates",
        "usage": "```bash\n# Kiem tra trang thai dong bo hoa cua ExternalSecret\nkubectl get externalsecret -n production -o wide\n```"
    },
    {
        "id": "dex-terraform-module-contract-tests",
        "name": "dex-terraform-module-contract-tests",
        "desc": "Design, implement, and automate contract tests for reusable Terraform and OpenTofu modules. Validate variable schemas, output guarantees, state drift, and prevent breaking changes.",
        "purpose": "Thiết kế, xây dựng và tự động hóa các bộ kiểm thử hợp đồng giao diện (Contract Testing) cho các mô-đun hạ tầng tái sử dụng viết bằng Terraform hoặc OpenTofu; kiểm chứng tính toàn vẹn của lược đồ biến đầu vào (Input Variable Schemas & Validation Rules), cam kết chất lượng đầu ra (Output Guarantees); sử dụng framework kiểm thử gốc `terraform test` hoặc Terratest để phát hiện sớm các thay đổi phá vỡ tương thích (Breaking Changes) trước khi xuất bản mô-đun lên Private Registry.",
        "when_use": "- Khi phát triển và duy trì các mô-đun hạ tầng cốt lõi dùng chung cho toàn bộ tổ chức (như VPC Module, EKS Module, S3 Bucket Module).\n- Khi nâng cấp phiên bản mô-đun (ví dụ từ v1.x lên v2.x) và cần chứng minh các dự án đang sử dụng không bị phá vỡ cấu trúc hạ tầng.\n- Khi tích hợp kiểm thử tự động Infrastructure as Code (IaC) vào quy trình CI/CD Pull Request.",
        "when_not_use": "- Khi viết các tệp cấu hình Terraform cục bộ dùng một lần cho một môi trường duy nhất mà không có ý định tái sử dụng thành module.\n- Khi kiểm thử logic ứng dụng nghiệp vụ không liên quan đến tầng cấp phát tài nguyên đám mây.",
        "prereqs": "- **Công cụ IaC:** Terraform 1.6+ hoặc OpenTofu 1.6+ hỗ trợ lệnh `test`.\n- **Môi trường giả lập:** AWS LocalStack hoặc tài khoản Sandbox hạn chế quyền để chạy kiểm thử thực tế.",
        "concepts": "- **Terraform Native Testing Framework (`.tftest.hcl`):** Khung kiểm thử chính thức được tích hợp sẵn từ phiên bản Terraform 1.6, cho phép viết các bài test kiểm tra điều kiện `assert` sau các giai đoạn `command = plan` hoặc `command = apply`.\n- **Input Contract Validation:** Khối `validation` bên trong định nghĩa `variable` nhằm chặn đứng các giá trị đầu vào sai quy chuẩn ngay từ trước khi chạy plan.\n- **Module Interface Stability:** Quy tắc bảo đảm không xóa bỏ hoặc đổi tên các biến `output` quan trọng mà các hệ thống khác đang phụ thuộc.",
        "workflow": "1. Khai báo các quy tắc kiểm tra ràng buộc chặt chẽ trong khối `variable` của module.\n2. Tạo thư mục `tests/` chứa các kịch bản kiểm thử hợp đồng dạng tệp `.tftest.hcl`.\n3. Định nghĩa các kịch bản kiểm thử tĩnh (Run Plan Only) để xác thực các giá trị mặc định và logic tính toán nội bộ mà không tốn chi phí tạo tài nguyên.\n4. Định nghĩa các kịch bản kiểm thử động (Run Apply) trên môi trường Sandbox để xác nhận tài nguyên được tạo đúng thuộc tính.\n5. Chạy lệnh `terraform test` hoặc `tofu test` trong pipeline CI.\n6. Xuất báo cáo kết quả kiểm thử và gắn thẻ phiên bản Semantic Versioning nếu bài test đạt 100%.",
        "examples": """### Kich ban kiem thu hop dong module S3 Bucket bang terraform test (.tftest.hcl):
```hcl
# tests/contract_validation.tftest.hcl

variables {
  bucket_name = "corp-secure-data-bucket-test"
  environment = "staging"
  enable_kms  = true
}

# Kiem thu Plan: Khang dinh bat buoc bat ma hoa KMS va khoa truy cap Public
run "verify_security_defaults_plan" {
  command = plan

  assert {
    condition     = aws_s3_bucket_server_side_encryption_configuration.this.rule[0].apply_server_side_encryption_by_default[0].sse_algorithm == "aws:kms"
    error_message = "S3 bucket must enforce AWS KMS encryption by default."
  }

  assert {
    condition     = aws_s3_bucket_public_access_block.this.block_public_acls == true
    error_message = "Block Public ACLs must be set to true."
  }

  assert {
    condition     = output.bucket_arn != ""
    error_message = "Output bucket_arn must not be empty."
  }
}

# Kiem thu loi khi truyen ten bucket vi pham quy tac dat ten
run "expect_invalid_bucket_name_failure" {
  command = plan

  variables {
    bucket_name = "INVALID_UPPERCASE_NAME"
  }

  expect_failures = [
    var.bucket_name,
  ]
}
```""",
        "antipatterns": "- **Unbounded Input Types:** Khai báo kiểu biến là `type = any` mà không có khối validation dẫn đến việc người dùng truyền nhầm cấu trúc dữ liệu gây sập runtime.\n- **Hardcoding Resource Names:** Gán nhãn cứng tên tài nguyên bên trong mô-đun khiến người dùng không thể tạo 2 phiên bản của mô-đun trên cùng một tài khoản đám mây.\n- **Skipping Destroy in Integration Tests:** Chạy `terraform apply` trong bài test nhưng quên tự động gọi `destroy` khi test xong, để lại tài nguyên rác tốn tiền trên cloud.",
        "gates": "- **QG-01**: 100% các biến đầu vào đều có mô tả (`description`), kiểu dữ liệu rõ ràng và quy tắc validation phù hợp.\n- **QG-02**: Tất cả các tệp `.tftest.hcl` vượt qua với kết quả PASS trong lệnh `terraform test`.\n- **QG-03**: Không có bất kỳ thay đổi nào làm gãy các biến `output` đã công bố trong phiên bản Minor/Patch.",
        "security": "- Bắt buộc kiểm tra các tiêu chuẩn an ninh hạ tầng (mã hóa at-rest, khóa public access, bật logging) ngay trong các bài test hợp đồng.",
        "adapters": "- **Runtimes**: Terraform CLI 1.6+, OpenTofu 1.6+, Terratest (Go), LocalStack.",
        "deliverables": "- Bộ tệp kiểm thử hợp đồng mô-đun (`tests/*.tftest.hcl`).\n- Báo cáo kết quả kiểm định hợp đồng tự động tích hợp CI/CD.",
        "related": "dex-infrastructure-policy-as-code, dex-platform-selfservice-templates, dex-cloud-database-failover-drills",
        "usage": "```bash\n# Chay toan bo bo test hop dong Terraform\nterraform init\nterraform test -verbose\n```"
    },
    {
        "id": "dex-infrastructure-policy-as-code",
        "name": "dex-infrastructure-policy-as-code",
        "desc": "Define, enforce, and audit Infrastructure Policy as Code (PaC) using Open Policy Agent (OPA/Rego) and Kyverno. Enforce security guardrails, validate exceptions, and block non-compliant resources.",
        "purpose": "Thiết kế, định nghĩa và thực thi chính sách quản trị hạ tầng dưới dạng mã nguồn (Policy as Code - PaC); sử dụng Open Policy Agent (OPA/Rego), Conftest, Trivy hoặc Kyverno để áp đặt các rào chắn bảo mật (Guardrails) trên các tệp cấu hình Terraform, Kubernetes Manifests và Dockerfile; tự động phát hiện và chặn đứng các vi phạm an ninh (như mở cổng 22 ra internet, thiếu thẻ gắn chi phí FinOps, hoặc chạy container dưới quyền root) trước khi hạ tầng được cấp phát.",
        "when_use": "- Khi thiết lập cổng kiểm soát chất lượng an ninh tự động trong pipeline CI/CD cho toàn bộ các nhóm kỹ thuật.\n- Khi ngăn chặn nguy cơ nhân sự cấu hình sai dẫn đến lộ lọt dữ liệu hoặc vi phạm các tiêu chuẩn tuân thủ (PCI-DSS, SOC 2, ISO 27001).\n- Khi cần cơ chế quản lý ngoại lệ chính sách (Policy Exceptions) có thời hạn và có kiểm toán minh bạch.",
        "when_not_use": "- Khi kiểm tra logic mã nguồn của ứng dụng phần mềm (sử dụng SonarQube hoặc SAST tools).\n- Khi quy mô hạ tầng quá nhỏ (1-2 máy chủ cá nhân) không đòi hỏi hệ thống kiểm soát tuân thủ tự động.",
        "prereqs": "- **Công cụ chính sách:** OPA CLI (`opa`), Conftest, hoặc Kyverno CLI.\n- **Tệp đầu vào:** Kế hoạch thực thi hạ tầng định dạng JSON (`terraform show -json tfplan.binary > tfplan.json`) hoặc Kubernetes YAML.",
        "concepts": "- **Open Policy Agent (OPA) & Rego:** Động cơ đánh giá chính sách nguồn mở cho phép viết các luật kiểm tra bằng ngôn ngữ khai báo Rego đối chiếu với bất kỳ cấu trúc dữ liệu JSON nào.\n- **Admission Controller Enforcer:** Thành phần trong Kubernetes (như OPA Gatekeeper hoặc Kyverno) chặn đứng các yêu cầu tạo tài nguyên vi phạm chính sách ngay tại API Server.\n- **Shift-Left Security:** Đẩy các bài kiểm tra bảo mật về phía bên trái của quy trình phát triển (ngay trên máy kỹ sư và tại bước tạo Pull Request).",
        "workflow": "1. Xây dựng bộ quy tắc an ninh dưới dạng tệp `.rego` trong thư mục `policies/`.\n2. Biên dịch kế hoạch triển khai hạ tầng thành định dạng JSON: `terraform show -json plan.tfplan > plan.json`.\n3. Thực thi kiểm tra đối soát bằng Conftest: `conftest test plan.json -p policies/`.\n4. Đánh giá kết quả: Phân loại mức độ vi phạm thành WARN (cảnh báo) và DENY (chặn đứng tiến trình build).\n5. Thiết lập quy trình xử lý ngoại lệ: Ghi nhận mã ngoại lệ được phê duyệt có chữ ký số vào tệp `exceptions.json`.\n6. Xuất báo cáo kiểm toán tuân thủ chính sách cho đội ngũ Security Operation Center (SOC).",
        "examples": """### Chinh sach OPA Rego ngan chan Security Group mo cong SSH (22) ra toan the gioi (0.0.0.0/0):
```rego
package terraform.security

import future.keywords.in

default allow = true

# Phat hien cac quy tac ingress mo cong 22 ra Internet
deny[msg] {
    resource := input.resource_changes[_]
    resource.type == "aws_security_group_rule"
    resource.change.after.type == "ingress"
    
    # Kiem tra cong 22
    from_port := resource.change.after.from_port
    to_port := resource.change.after.to_port
    22 >= from_port
    22 <= to_port

    # Kiem tra dai CIDR mo 0.0.0.0/0
    cidr_blocks := resource.change.after.cidr_blocks[_]
    cidr_blocks == "0.0.0.0/0"

    msg := sprintf("SECURITY VIOLATION: Resource '%v' opens SSH port 22 directly to the public Internet (0.0.0.0/0)!", [resource.address])
}
```""",
        "antipatterns": "- **Hardcoded Exceptions in Rule Body:** Viết thẳng tên tài nguyên ngoại lệ vào bên trong file luật Rego khiến mã chính sách bị ô nhiễm và khó bảo trì.\n- **Only Auditing Post-Deployment:** Chỉ kiểm tra vi phạm sau khi tài nguyên đã được tạo trên đám mây thay vì chặn ngay từ giai đoạn Plan trong CI/CD.\n- **Vague Denial Messages:** Xuất thông báo lỗi chung chung \"Policy Failed\" mà không chỉ rõ tài nguyên nào vi phạm và cách sửa đổi cụ thể.",
        "gates": "- **QG-01**: 100% các tệp hạ tầng IaC được quét tự động qua bộ chính sách PaC trước khi thực thi apply.\n- **QG-02**: Không có bất kỳ vi phạm mức DENY nào được phép vượt qua pipeline CI/CD nếu không có ngoại lệ phê duyệt hợp lệ.\n- **QG-03**: Mọi quy tắc chính sách đều có bộ kiểm thử đơn vị đi kèm (`*_test.rego`) đạt tỷ lệ bao phủ 100%.",
        "security": "- Bảo vệ tính toàn vẹn của kho chứa chính sách; chỉ những nhân sự thuộc nhóm Bảo mật mới có quyền phê duyệt thay đổi các tệp `.rego`.",
        "adapters": "- **Runtimes**: OPA (Rego), Conftest, Kyverno CLI, Trivy, Checkov, OPA Gatekeeper.",
        "deliverables": "- Kho thư viện chính sách bảo mật hạ tầng (`policies/terraform/*.rego`).\n- Báo cáo kết quả kiểm tra tuân thủ chính sách (`pac_compliance_report.json`).",
        "related": "dex-terraform-module-contract-tests, dex-kubernetes-secret-delivery, dex-platform-selfservice-templates",
        "usage": "```bash\n# Kiem tra ke hoach Terraform bang Conftest va OPA policies\nconftest test tfplan.json --policy ./policies --all-namespaces\n```"
    },
    {
        "id": "dex-release-progressive-metrics",
        "name": "dex-release-progressive-metrics",
        "desc": "Define, analyze, and automate progressive canary release metrics (Argo Rollouts, Flagger). Measure SLI/SLO error rates, latency regressions, and trigger automated rollbacks.",
        "purpose": "Thiết kế, định nghĩa và tự động hóa các chỉ số đánh giá phát hành lũy tiến (Progressive Canary Release Metrics); tích hợp các bộ điều khiển phát hành hiện đại (Argo Rollouts, Flagger, Istio Service Mesh); đo lường tự động các chỉ số cấp độ dịch vụ (SLI/SLO: Error Rates, Latency P95/P99, HTTP 5xx Statuses) so sánh giữa phiên bản Canary và phiên bản Baseline; tự động đưa ra quyết định tăng bậc phần trăm lưu lượng mạng hoặc kích hoạt hủy bỏ khẩn cấp (Automated Rollback) khi phát hiện dấu hiệu bất thường.",
        "when_use": "- Khi triển khai các bản cập nhật phần mềm quan trọng cho hệ thống phục vụ hàng triệu người dùng trực tuyến.\n- Khi muốn chuyển dịch từ phương pháp phát hành rủi ro cao (Big Bang Deployment) sang phương pháp thử nghiệm lưu lượng nhỏ (Canary 5% -> 20% -> 50% -> 100%).\n- Khi cần loại bỏ sự can thiệp thủ công của con người trong việc quan sát biểu đồ để quyết định thăng cấp phiên bản.",
        "when_not_use": "- Khi dịch vụ chỉ phục vụ môi trường nội bộ với lưu lượng truy cập quá thấp (<1 request/phút) không đủ dữ liệu thống kê để đánh giá.\n- Khi bản cập nhật chứa các thay đổi phá vỡ tương thích cấu trúc CSDL (Database Schema Breaking Changes) không thể chạy song song 2 phiên bản.",
        "prereqs": "- **Hạ tầng đo lường:** Prometheus, Datadog hoặc CloudWatch thu thập chỉ số thời gian thực với độ trễ <15 giây.\n- **Bộ điều phối:** Argo Rollouts hoặc Flagger cài đặt trên cụm Kubernetes.",
        "concepts": "- **Canary Step Weights:** Lộ trình tăng dần tỷ lệ phần trăm người dùng tiếp cận phiên bản mới (ví dụ: bước 1 cấp 10% trong 10 phút, bước 2 cấp 30% trong 20 phút).\n- **AnalysisRun:** Đối tượng trong Argo Rollouts định kỳ thực thi các câu truy vấn Prometheus để xác nhận tỷ lệ lỗi không vượt ngưỡng cho phép.\n- **Automated Rollback Trigger:** Hành động hoàn nguyên lưu lượng về 100% phiên bản Stable ngay lập tức khi chỉ số Canary vi phạm ngưỡng thất bại liên tiếp (Consecutive Failures).",
        "workflow": "1. Xác định các chỉ số SLI cốt lõi: Tỷ lệ lỗi thành công (`success_rate > 99.5%`) và độ trễ P95 (`latency_p95 < 200ms`).\n2. Cấu hình tài nguyên `AnalysisTemplate` định nghĩa câu truy vấn Prometheus và ngưỡng đánh giá.\n3. Khai báo đối tượng `Rollout` thay thế cho `Deployment` tiêu chuẩn trong Kubernetes.\n4. Kích hoạt cập nhật phiên bản mới bằng cách thay đổi container image tag.\n5. Argo Rollouts tự động định tuyến 10% lưu lượng sang Canary Pod và kích hoạt `AnalysisRun`.\n6. Nếu toàn bộ các lượt phân tích đều thành công, tự động chuyển 100% lưu lượng và dọn dẹp các Pod cũ; nếu vi phạm, tự động hoàn nguyên về bản Stable trong 15 giây.",
        "examples": """### Cau hinh Argo Rollouts AnalysisTemplate do luong ty le loi va do tre tu Prometheus:
```yaml
apiVersion: argoproj.io/v1alpha1
kind: AnalysisTemplate
metadata:
  name: success-rate-and-latency-check
  namespace: production
spec:
  metrics:
    - name: success-rate
      interval: 30s
      successCondition: result[0] >= 0.995 # Yeu cau ty le thanh cong >= 99.5%
      failureLimit: 2 # Cho phep toi da 2 lan fail truoc khi rollback
      provider:
        prometheus:
          address: http://prometheus.monitoring:9090
          query: |
            sum(rate(http_requests_total{status!~"5.*",app="web-api",role="canary"}[1m])) 
            / 
            sum(rate(http_requests_total{app="web-api",role="canary"}[1m]))

    - name: latency-p95
      interval: 30s
      successCondition: result[0] <= 0.250 # Do tre P95 khong vuot qua 250ms
      failureLimit: 2
      provider:
        prometheus:
          address: http://prometheus.monitoring:9090
          query: |
            histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket{app="web-api",role="canary"}[1m])) by (le))
```""",
        "antipatterns": "- **Too Short Analysis Intervals:** Đặt chu kỳ kiểm tra quá ngắn (dưới 5 giây) khiến mẫu dữ liệu quá thưa thớt dẫn đến việc đánh giá sai lệch (False Positive Rollback).\n- **Ignoring Client-Side Errors (4xx):** Chỉ theo dõi lỗi 5xx mà bỏ qua lỗi 4xx khi bản cập nhật mới vô tình làm gãy định dạng API khiến hàng loạt client gửi request lỗi.\n- **Manual Approval Bottle-neck:** Bắt buộc con người phải bấm nút Approve ở mỗi bước 5%, 10%, 20% làm mất hoàn toàn lợi ích của tự động hóa triển khai.",
        "gates": "- **QG-01**: Tỷ lệ thành công (Success Rate) của phiên bản Canary đạt tối thiểu 99.5% trong toàn bộ các bước triển khai.\n- **QG-02**: Độ trễ phản hồi P95 không tăng quá 15% so với phiên bản Stable hiện tại.\n- **QG-03**: Hệ thống tự động kích hoạt hoàn nguyên (Rollback) trong vòng dưới 30 giây khi phát hiện vi phạm ngưỡng an toàn.",
        "security": "- Hạn chế quyền can thiệp vào tiến trình Rollout; mọi thao tác Promote hoặc Abort thủ công đều phải được lưu vết kiểm toán (Audit Trail).",
        "adapters": "- **Runtimes**: Argo Rollouts, Flagger, Prometheus, Istio Service Mesh, Datadog.",
        "deliverables": "- Tệp định nghĩa mẫu phân tích lũy tiến (`canary_analysis_template.yaml`).\n- Báo cáo đánh giá kết quả triển khai canary (`canary_deployment_summary.json`).",
        "related": "dex-api-circuit-breaker-verification, dex-queue-capacity-saturation, dex-operational-dependency-mapping",
        "usage": "```bash\n# Theo doi trang thai phat hanh luy tien bang argo rollouts CLI\nkubectl argo rollouts get rollout web-api -n production --watch\n```"
    },
    {
        "id": "dex-queue-capacity-saturation",
        "name": "dex-queue-capacity-saturation",
        "desc": "Model, monitor, and stress-test asynchronous message queue saturation (RabbitMQ, Kafka, SQS). Detect consumer lag, head-of-line blocking, and configure KEDA auto-scaling.",
        "purpose": "Mô hình hóa, giám sát và kiểm thử độ bão hòa tải của hệ thống hàng đợi thông điệp bất đồng bộ (Message Queue Capacity & Saturation: Apache Kafka, RabbitMQ, AWS SQS); phát hiện sớm hiện tượng tích tụ độ trễ tiêu thụ (Consumer Lag), tắc nghẽn đầu hàng đợi (Head-of-Line Blocking) và tràn bộ đệm thư chết (Dead-Letter Queue - DLQ); cấu hình cơ chế tự động co giãn quy mô worker dựa trên sự kiện (Event-Driven Auto-scaling với KEDA) và thiết lập các biện pháp kiểm soát áp lực ngược (Backpressure).",
        "when_use": "- Khi hệ thống xử lý tác vụ nền gặp hiện tượng chậm trễ xử lý đơn hàng, gửi email hoặc phân tích dữ liệu trong các đợt cao điểm khuyến mãi.\n- Khi số lượng thông điệp chưa xử lý trong hàng đợi tăng trưởng đột biến nhưng số lượng worker không tự động tăng tương ứng.\n- Khi thiết lập các ngưỡng cảnh báo bão hòa dung lượng đĩa và bộ nhớ RAM của cụm máy chủ message broker.",
        "when_not_use": "- Khi các yêu cầu được xử lý đồng bộ thời gian thực thông qua REST API hoặc gRPC không có hàng đợi trung gian.\n- Khi khối lượng tác vụ quá nhỏ (<10 thông điệp/phút) không bao giờ chạm tới giới hạn tài nguyên của broker.",
        "prereqs": "- **Hạ tầng hàng đợi:** Cụm RabbitMQ, Kafka hoặc AWS SQS đang hoạt động.\n- **Công cụ đo kiểm:** Prometheus exporter cho hàng đợi (`rabbitmq_exporter`, `kafka_exporter`) và KEDA cài trên Kubernetes.",
        "concepts": "- **Consumer Lag:** Khoảng cách giữa offset của thông điệp mới nhất được ghi vào hàng đợi và offset của thông điệp mà consumer đang xử lý.\n- **Head-of-Line Blocking:** Hiện tượng một thông điệp bị lỗi liên tục thất bại và retry chặn đứng toàn bộ các thông điệp hợp lệ phía sau nó.\n- **KEDA (Kubernetes Event-driven Autoscaling):** Bộ điều phối tự động tăng số lượng Pod worker từ 0 lên N dựa trên độ sâu của hàng đợi (Queue Depth / Lag Metric).",
        "workflow": "1. Khảo sát thông lượng sản xuất (Producer Throughput) và thông lượng tiêu thụ tối đa của một worker (Consumer Capacity).\n2. Thiết lập đối tượng `ScaledObject` trong KEDA gắn với độ sâu hàng đợi mục tiêu (Target Queue Length, ví dụ: 30 thông điệp / 1 worker).\n3. Thực hiện bài kiểm thử ép tải (Stress Test) bằng công cụ sinh tải đẩy hàng triệu thông điệp vào hàng đợi trong 5 phút.\n4. Quan sát tốc độ co giãn của cụm worker và biểu đồ Consumer Lag trong Prometheus.\n5. Kiểm tra cơ chế định tuyến thông điệp lỗi: sau 3 lần retry thất bại, thông điệp phải được chuyển an toàn sang Dead-Letter Queue.\n6. Xác nhận hệ thống hạ tải mượt mà (Scale Down) về mức cơ sở khi hàng đợi được giải phóng hoàn toàn.",
        "examples": """### Cau hinh KEDA ScaledObject tu dong co gian Worker theo do sau hang doi RabbitMQ:
```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: order-processor-scaler
  namespace: processing
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: order-worker-deployment
  minReplicaCount: 2   # Duy tri toi thieu 2 worker san sang
  maxReplicaCount: 30  # Cho phep mo rong toi da 30 worker khi qua tai
  cooldownPeriod: 300  # Cho 5 phut sau khi hang doi trong moi giam pod
  triggers:
    - type: rabbitmq
      metadata:
        protocol: amqp
        queueName: orders_v1_queue
        mode: QueueLength
        value: "50" # Moi 50 message ton dong se them 1 worker pod
      authenticationRef:
        name: keda-rabbitmq-auth
```""",
        "antipatterns": "- **Unbounded Message Retries Without Backoff:** Cho phép worker retry vô tận một thông điệp lỗi mà không đẩy sang DLQ khiến toàn bộ hàng đợi bị tắc nghẽn vĩnh viễn.\n- **Aggressive Scale Down (Thrashing):** Đặt thời gian cooldown co cụm quá ngắn khiến các worker liên tục bị tạo mới rồi lại bị hủy (Flapping/Thrashing) tốn tài nguyên hệ thống.\n- **Unmonitored Dead-Letter Queues:** Tạo hàng đợi thư chết DLQ nhưng không có hệ thống cảnh báo, khiến hàng nghìn đơn hàng lỗi tích tụ âm thầm mà không ai hay biết.",
        "gates": "- **QG-01**: Hệ thống kích hoạt co giãn worker (Scale Out) trong vòng 30 giây khi độ sâu hàng đợi vượt ngưỡng quy định.\n- **QG-02**: 100% thông điệp lỗi được chuyển về Dead-Letter Queue sau đúng 3 lần retry có exponential backoff.\n- **QG-03**: Bộ nhớ RAM và đĩa cứng của cụm Message Broker không bao giờ vượt quá 80% công suất trong bài kiểm thử ép tải.",
        "security": "- Bắt buộc mã hóa luồng truyền tải thông điệp bằng TLS (mTLS); kiểm soát phân quyền đọc/ghi từng Topic/Queue bằng ACL.",
        "adapters": "- **Runtimes**: KEDA, RabbitMQ, Apache Kafka, AWS SQS, Prometheus.",
        "deliverables": "- Tệp định nghĩa co giãn sự kiện tự động (`keda_queue_scaler.yaml`).\n- Báo cáo phân tích năng lực chịu tải và độ bão hòa hàng đợi (`queue_saturation_report.md`).",
        "related": "dex-api-circuit-breaker-verification, dex-release-progressive-metrics, dex-operational-dependency-mapping",
        "usage": "```bash\n# Kiem tra consumer lag cua Kafka Consumer Group bang kafka CLI\nkafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group order-processors\n```"
    },
    {
        "id": "dex-api-circuit-breaker-verification",
        "name": "dex-api-circuit-breaker-verification",
        "desc": "Design, implement, and verify distributed API Circuit Breaker state machines. Test CLOSED, OPEN, and HALF-OPEN transitions, fallback responses, and prevent cascading cascading system failures.",
        "purpose": "Thiết kế, cài đặt và kiểm chứng tính đúng đắn của máy trạng thái ngắt mạch phân tán (Distributed API Circuit Breaker State Machine); kiểm tra toàn diện các chu kỳ chuyển đổi trạng thái ĐÓNG (Closed - hoạt động bình thường), MỞ (Open - ngắt kết nối khẩn cấp) và NỬA MỞ (Half-Open - thử nghiệm phục hồi); cung cấp cơ chế phản hồi dự phòng tức thì (Graceful Fallback), ngăn ngừa hiện tượng lỗi dây chuyền (Cascading Failures) và triệt tiêu nguy cơ bão yêu cầu đè bẹp hệ thống phía sau (Thundering Herd).",
        "when_use": "- Khi gọi các dịch vụ bên thứ ba (Cổng thanh toán, Dịch vụ gửi SMS, API Đối tác) có độ tin cậy không ổn định hoặc thường xuyên chập chờn.\n- Khi bảo vệ các microservices nội bộ khỏi nguy cơ bị cạn kiệt tài nguyên luồng (Thread Starvation) do dịch vụ phụ thuộc phản hồi quá chậm.\n- Khi thiết lập khả năng phục hồi tự động (Self-Healing) cho hệ thống phân tán trong điều kiện mạng suy giảm chất lượng.",
        "when_not_use": "- Khi tương tác với cơ sở dữ liệu nội bộ trong cùng một transaction nguyên tử (ACID transaction).\n- Khi yêu cầu là các tác vụ ghi dữ liệu tài chính bắt buộc phải hoàn thành đồng bộ không được phép sử dụng dữ liệu dự phòng cũ.",
        "prereqs": "- **Thư viện Circuit Breaker:** Resilience4j (Java/Kotlin), Polly (C#), go-breaker (Go), opossum (Node.js), hoặc tenacity/pybreaker (Python).\n- **Hạ tầng kiểm thử:** WireMock hoặc Mountebank để giả lập lỗi và độ trễ mạng có chủ đích.",
        "concepts": "- **Sliding Window Metrics:** Cơ chế ghi nhận tỷ lệ lỗi dựa trên số lượng yêu cầu gần nhất (Count-based Sliding Window, ví dụ 100 requests) hoặc khoảng thời gian (Time-based, ví dụ 10s).\n- **Failure Rate Threshold:** Tỷ lệ phần trăm yêu cầu thất bại hoặc phản hồi chậm (Slow Call Rate) kích hoạt chuyển trạng thái từ CLOSED sang OPEN (thường đặt ở mức 50%).\n- **Half-Open Probe Requests:** Khi hết thời gian chờ (Wait Duration in Open State), Circuit Breaker cho phép một số lượng nhỏ yêu cầu (ví dụ 5 requests) đi qua để kiểm tra xem dịch vụ phía sau đã thực sự khỏe mạnh hay chưa.",
        "workflow": "1. Khảo sát SLA và thời gian timeout tối đa của API dịch vụ phía sau.\n2. Cấu hình tham số Circuit Breaker: `failureRateThreshold: 50%`, `waitDurationInOpenState: 15s`, `slidingWindowSize: 20`.\n3. Định nghĩa hàm Fallback trả về dữ liệu bộ nhớ đệm (Cached Response) hoặc thông báo thân thiện cho người dùng.\n4. Thực hiện bài kiểm thử tự động giả lập 20 yêu cầu lỗi liên tiếp và khẳng định mạch chuyển ngay sang trạng thái OPEN.\n5. Khẳng định các yêu cầu tiếp theo trong thời gian OPEN bị chặn lập tức (Fail-Fast) với độ trễ <1ms mà không gửi ra mạng.\n6. Chờ hết thời gian 15 giây, gửi 5 yêu cầu thành công và khẳng định mạch tự động chuyển về trạng thái CLOSED bình thường.",
        "examples": """### Cai dat Circuit Breaker voi Opossum trong Node.js / TypeScript:
```typescript
import CircuitBreaker from 'opossum';
import axios from 'axios';

interface PaymentResponse {
  transactionId: string;
  status: string;
}

async function callPaymentGateway(orderId: string, amount: number): Promise<PaymentResponse> {
  const response = await axios.post('https://api.payment.example.com/v1/charge', {
    orderId,
    amount
  }, { timeout: 2000 }); // Timeout 2 giay
  return response.data;
}

const options: CircuitBreaker.Options = {
  timeout: 2500, // Thoi gian coi la timeout
  errorThresholdPercentage: 50, // Ty le loi >= 50% thi ngat mach
  resetTimeout: 10000, // Cho 10 giay truoc khi vao Half-Open de test lai
  rollingCountTimeout: 10000,
  rollingCountBuckets: 10
};

export const paymentBreaker = new CircuitBreaker(callPaymentGateway, options);

// Cung cap ham Fallback khi mach OPEN hoac loi
paymentBreaker.fallback((orderId, amount) => {
  console.warn(`[CIRCUIT BREAKER] Fallback triggered for order ${orderId}. Payment queued.`);
  return {
    transactionId: "PENDING_OFFLINE",
    status: "QUEUED_FOR_RETRY"
  };
});

paymentBreaker.on('open', () => console.error('[CIRCUIT BREAKER] State changed to OPEN! Failing fast.'));
paymentBreaker.on('halfOpen', () => console.log('[CIRCUIT BREAKER] State changed to HALF-OPEN. Probing...'));
paymentBreaker.on('close', () => console.log('[CIRCUIT BREAKER] State changed to CLOSED. Service healthy.'));
```""",
        "antipatterns": "- **Missing Timeout Configuration:** Bật Circuit Breaker nhưng quên đặt `requestTimeout` khiến các kết nối bị treo vĩnh viễn ở trạng thái chờ đợi thay vì tính là lỗi.\n- **Shared Circuit Breaker for Different APIs:** Dùng chung một phiên bản Circuit Breaker duy nhất cho nhiều API khác nhau, khiến sự cố của API gửi mail làm sập luôn API thanh toán.\n- **Zero Fallback Strategy:** Để mạch OPEN nhưng không có hàm fallback khiến người dùng nhận trang lỗi 500 thay vì thông báo hướng dẫn hoặc nội dung cached.",
        "gates": "- **QG-01**: Mạch chuyển trạng thái từ CLOSED sang OPEN chính xác 100% khi tỷ lệ lỗi vượt ngưỡng quy định trong bài test tự động.\n- **QG-02**: Trong trạng thái OPEN, 100% yêu cầu được xử lý Fail-Fast với thời gian phản hồi dưới 2ms mà không làm nghẽn kết nối mạng.\n- **QG-03**: Mạch phục hồi an toàn về CLOSED sau khi các yêu cầu thăm dò trong giai đoạn HALF-OPEN thành công.",
        "security": "- Bảo đảm dữ liệu trả về từ hàm Fallback không làm lộ các thông tin nhạy cảm của người dùng khác được lưu trong cache.",
        "adapters": "- **Runtimes**: Resilience4j (Java), Polly (.NET), Opossum (Node.js), pybreaker (Python), Istio Circuit Breaker.",
        "deliverables": "- Module quản lý Circuit Breaker phân tán (`circuit_breaker_service.ts`).\n- Bộ kiểm thử tự động kiểm chứng 3 trạng thái máy trạng thái (`test_circuit_breaker.ts`).",
        "related": "dex-cloud-database-failover-drills, dex-release-progressive-metrics, dex-queue-capacity-saturation",
        "usage": "```bash\n# Chay test kiem thu chuyen doi trang thai Circuit Breaker bang Jest\nnpx jest tests/test_circuit_breaker.test.ts --verbose\n```"
    },
    {
        "id": "dex-storage-backup-restore-drills",
        "name": "dex-storage-backup-restore-drills",
        "desc": "Automate, execute, and verify end-to-end storage and database backup restoration drills. Audit cryptographic checksums, snapshot integrity, and measure Recovery Time Objectives (RTO).",
        "purpose": "Thiết kế, tự động hóa và kiểm chứng toàn diện quy trình phục hồi sao lưu dữ liệu (Storage & Database Backup Restoration Drills); kiểm tra tính hợp lệ của các bản sao lưu (AWS S3 Versioning, PostgreSQL WAL-G/pg_dump, EBS Snapshots); thực hiện phục hồi thực tế vào một môi trường cách ly (Isolated Sandbox); đối soát mã băm mật mã học (Cryptographic SHA-256 Checksums), kiểm tra tính nhất quán giao dịch và chứng minh khả năng phục hồi dữ liệu trong thời gian cam kết RTO/RPO mà không làm ảnh hưởng tới hệ thống chính.",
        "when_use": "- Khi tiến hành diễn tập kiểm toán tuân thủ định kỳ hàng quý hoặc hàng năm theo tiêu chuẩn SOC 2, HIPAA, hoặc ISO 27001.\n- Khi thiết lập quy trình kiểm tra tự động xem các bản sao lưu hàng đêm có thực sự giải nén và nạp lại được vào database hay không.\n- Khi thay đổi phiên bản cơ sở dữ liệu lớn (Major Version Upgrade) và cần chắc chắn bản backup tương thích với engine mới.",
        "when_not_use": "- Khi sao chép tệp tạm thời giữa các thư mục cục bộ của máy tính phát triển.\n- Khi kiểm thử logic nghiệp vụ thông thường không liên quan tới sự cố mất mát dữ liệu hoặc thảm họa hạ tầng.",
        "prereqs": "- **Hạ tầng lưu trữ:** Kho lưu trữ sao lưu có bật bảo vệ chống ghi đè/xóa (S3 Object Lock / WORM storage).\n- **Môi trường diễn tập:** Cụm tài nguyên Sandbox biệt lập với hạ tầng production.",
        "concepts": "- **Backup vs Restore Verification:** Bản sao lưu chỉ có giá trị khi nó đã được chứng minh là có thể phục hồi thành công (An unverified backup is not a backup).\n- **WORM (Write Once, Read Many):** Chính sách khóa dữ liệu bất biến ngăn chặn mã độc tống tiền (Ransomware) hoặc kẻ tấn công có quyền quản trị xóa bỏ các bản sao lưu.\n- **Point-in-Time Recovery (PITR):** Khả năng phục hồi trạng thái cơ sở dữ liệu về đúng một giây cụ thể trong quá khứ bằng cách kết hợp bản Base Backup với chuỗi nhật ký Write-Ahead Logs (WAL).",
        "workflow": "1. Lựa chọn ngẫu nhiên một bản sao lưu gần nhất từ kho lưu trữ bất biến (S3 WORM Bucket).\n2. Xác thực tính toàn vẹn của tệp nhị phân thông qua chữ ký số hoặc mã băm SHA-256.\n3. Khởi tạo một cụm cơ sở dữ liệu hoặc máy chủ lưu trữ mới trong mạng VPC Sandbox cách ly.\n4. Thực hiện tiến trình nạp phục hồi dữ liệu (Restore) và ghi nhận thời gian hoàn thành (Actual RTO).\n5. Chạy bộ kịch bản kiểm tra tính toàn vẹn dữ liệu tự động (Data Consistency Checks): đếm số hàng các bảng quan trọng, kiểm tra ràng buộc khóa ngoại.\n6. Hủy bỏ môi trường Sandbox và xuất báo cáo kiểm toán diễn tập phục hồi có chữ ký số xác thực.",
        "examples": """### Kich ban tu dong phuc hoi PostgreSQL tu S3 vao Sandbox va kiem tra toan ven:
```bash
#!/usr/bin/env bash
set -euo pipefail

BACKUP_BUCKET="s3://corp-backups-immutable-worm/postgres"
SANDBOX_CONTAINER="postgres-restore-sandbox"
LATEST_BACKUP=$(aws s3 ls "${BACKUP_BUCKET}/" | sort | tail -n 1 | awk '{print $4}')

echo "=== STARTING RESTORE DRILL FOR: ${LATEST_BACKUP} ==="
START_TIME=$(date +%s)

# 1. Tai ban sao luu kem checksum
aws s3 cp "${BACKUP_BUCKET}/${LATEST_BACKUP}" ./latest_backup.dump
aws s3 cp "${BACKUP_BUCKET}/${LATEST_BACKUP}.sha256" ./latest_backup.sha256

# 2. Xac thuc ma bam toan ven
sha256sum -c latest_backup.sha256

# 3. Khoi tao container Postgres moi tinh trong sandbox
docker run -d --name "${SANDBOX_CONTAINER}" -e POSTGRES_PASSWORD=restore_pass -p 5433:5432 postgres:16-alpine
sleep 5

# 4. Thuc hien restore
pg_restore -h localhost -p 5433 -U postgres -d postgres -v latest_backup.dump

END_TIME=$(date +%s)
RTO_SECONDS=$((END_TIME - START_TIME))
echo "Restore completed successfully in ${RTO_SECONDS} seconds."

# 5. Kiem tra toan ven du lieu (Data Integrity Check)
COUNT_USERS=$(psql -h localhost -p 5433 -U postgres -t -c "SELECT COUNT(*) FROM public.users;")
echo "Integrity Verification: public.users count = ${COUNT_USERS}"

# 6. Don dep sandbox
docker rm -f "${SANDBOX_CONTAINER}"
rm -f latest_backup.dump latest_backup.sha256
echo "Restore drill PASSED and sandbox cleaned."
```""",
        "antipatterns": "- **Trusting Successful Backup Logs Blindly:** Tin tưởng tuyệt đối vào thông báo \"Backup Finished with Code 0\" mà không bao giờ thực hiện diễn tập khôi phục thực tế, đến khi thảm họa xảy ra mới phát hiện tệp backup bị rỗng hoặc lỗi mã hóa.\n- **Restoring Directly into Production VPC:** Chạy diễn tập phục hồi trong cùng mạng VPC của môi trường production làm phát sinh nguy cơ xung đột IP hoặc ghi đè nhầm vào CSDL thật.\n- **Ignoring Encryption Key Availability:** Sao lưu dữ liệu có mã hóa nhưng lưu khóa giải mã chung với máy chủ chính; khi máy chủ chính gặp nạn, không thể giải mã được bản sao lưu.",
        "gates": "- **QG-01**: Tệp sao lưu vượt qua kiểm tra mã băm SHA-256 khớp 100% với giá trị ghi nhận lúc tạo bản sao lưu.\n- **QG-02**: Quá trình phục hồi vào môi trường Sandbox hoàn tất thành công với mã thoát 0 mà không có lỗi cú pháp.\n- **QG-03**: Số lượng bản ghi và tính toàn vẹn của các bảng dữ liệu cốt lõi khớp chính xác với trạng thái tại thời điểm sao lưu.",
        "security": "- Kho lưu trữ bản sao lưu phải được cấu hình quyền bất biến (Object Lock / WORM) ngăn chặn việc xóa bỏ vô tình hoặc cố ý từ bất kỳ ai.",
        "adapters": "- **Runtimes**: AWS S3 Object Lock, PostgreSQL pg_restore / WAL-G, Velero (Kubernetes), Docker Sandbox.",
        "deliverables": "- Kịch bản diễn tập phục hồi sao lưu tự động (`automated_restore_drill.sh`).\n- Báo cáo kiểm toán kết quả diễn tập phục hồi hàng quý (`restore_drill_audit.pdf`).",
        "related": "dex-cloud-database-failover-drills, dex-api-circuit-breaker-verification, dex-operational-dependency-mapping",
        "usage": "```bash\n# Xac thuc ma bam cua tep backup truoc khi dien tap\nsha256sum -c backup_2026_10_23.dump.sha256\n```"
    },
    {
        "id": "dex-platform-selfservice-templates",
        "name": "dex-platform-selfservice-templates",
        "desc": "Design, validate, and govern internal developer platform self-service templates (Backstage, Cookiecutter, Copier). Enforce security guardrails, CI/CD scaffolding, and architectural standards.",
        "purpose": "Thiết kế, kiểm định và quản trị các mẫu dự án tự phục vụ cho nền tảng kỹ thuật nội bộ (Internal Developer Platform Self-Service Templates: Spotify Backstage Software Templates, Cookiecutter, Copier); cung cấp khả năng khởi tạo nhanh chóng các dự án microservices, thư viện hoặc hạ tầng mới tuân thủ 100% các tiêu chuẩn kiến trúc, rào chắn bảo mật mặc định (Security Guardrails), đường ống CI/CD tích hợp sẵn và quy định về quyền sở hữu (Ownership & Service Catalog).",
        "when_use": "- Khi xây dựng Nền tảng Kỹ thuật Nội bộ (Internal Developer Platform - IDP) để nâng cao trải nghiệm nhà phát triển (Developer Experience - DevEx).\n- Khi các đội ngũ kỹ thuật mất quá nhiều thời gian (nhiều ngày hoặc nhiều tuần) chỉ để khởi tạo một microservice mới với đầy đủ CI/CD, linting, logging và bảo mật.\n- Khi muốn chuẩn hóa cấu trúc thư mục, quy ước đặt tên và các phụ thuộc dùng chung trên toàn bộ công ty.",
        "when_not_use": "- Khi dự án là một thử nghiệm nghiên cứu một lần (PoC / Spike) không có kế hoạch đưa vào vận hành hoặc tích hợp vào hệ sinh thái chung.\n- Khi tạo các script ngắn đơn lẻ không có cấu trúc dự án hoàn chỉnh.",
        "prereqs": "- **Công cụ tạo mẫu:** Backstage Software Templates, Cookiecutter, hoặc Copier (hỗ trợ cập nhật mẫu).\n- **Kho lưu trữ mẫu:** Git repository chứa mã nguồn mẫu chuẩn hóa kèm tệp định nghĩa metadata.",
        "concepts": "- **Golden Path / Paved Road:** Lộ trình khuyến nghị tốt nhất được nền tảng kỹ thuật bảo đảm và hỗ trợ tối đa, giúp kỹ sư đi nhanh và an toàn mà không phải tự quyết định mọi thứ.\n- **Template Scaffolding:** Quy trình nhận các tham số đầu vào từ người dùng (tên dịch vụ, chủ sở hữu, loại CSDL) và điền vào các tệp khuôn mẫu Jinja2 để sinh ra kho mã nguồn mới.\n- **Template Drift & Lifecycle:** Khả năng cập nhật các thay đổi mới của mẫu mẹ (Template) vào các dự án con đã được sinh ra trước đó (sử dụng tính năng `copier update`).",
        "workflow": "1. Khảo sát các thành phần thiết yếu của một dịch vụ chuẩn: Lược đồ cấu trúc thư mục, tệp CI/CD, Dockerfile bảo mật, cấu hình SonarQube, Helm Chart.\n2. Xây dựng khuôn mẫu dự án sử dụng cú pháp Jinja2 trong Copier hoặc Cookiecutter.\n3. Định nghĩa tệp kê khai Backstage `template.yaml` với các bước kiểm tra tính hợp lệ của tham số đầu vào.\n4. Tự động hóa các bước hậu tạo mẫu: Tạo repository mới trên GitHub/GitLab, cấu hình Branch Protection Rules, và đăng ký vào Service Catalog.\n5. Viết bộ kiểm thử tự động sinh dự án thử nghiệm (Smoke Test) và kiểm tra khả năng build/test thành công của dự án sinh ra.\n6. Xuất bản mẫu lên Cổng thông tin nhà phát triển nội bộ (Developer Portal).",
        "examples": """### Dinh nghia Backstage Software Template khoi tao Microservice chuan:
```yaml
apiVersion: backstage.io/v1alpha1
kind: Template
metadata:
  name: standard-fastapi-service
  title: Standard FastAPI Microservice
  description: Scaffold a production-ready Python FastAPI microservice with CI/CD, Docker, and Security guardrails.
  tags:
    - python
    - fastapi
    - microservice
spec:
  owner: team-platform-engineering
  type: service

  parameters:
    - title: Service Configuration
      required:
        - service_name
        - owner
      properties:
        service_name:
          title: Service Name
          type: string
          description: Unique kebab-case identifier for the service
          pattern: '^[a-z0-9-]+$'
        owner:
          title: Owner Team
          type: string
          description: GitHub team slug responsible for this service
        enable_database:
          title: Enable PostgreSQL Database
          type: boolean
          default: false

  steps:
    - id: template
      name: Fetch and Render Template
      action: fetch:template
      input:
        url: ./skeleton
        values:
          service_name: ${{ parameters.service_name }}
          owner: ${{ parameters.owner }}
          enable_database: ${{ parameters.enable_database }}

    - id: publish
      name: Publish to GitHub
      action: publish:github
      input:
        repoUrl: github.com?owner=my-org&repo=${{ parameters.service_name }}
        defaultBranch: main
        protectDefaultBranch: true

    - id: register
      name: Register in Software Catalog
      action: catalog:register
      input:
        repoContentsUrl: ${{ steps['publish'].output.repoContentsUrl }}
        catalogInfoPath: '/catalog-info.yaml'
```""",
        "antipatterns": "- **Bloated Kitchen-Sink Templates:** Nhồi nhét tất cả các thư viện và tính năng có thể có vào một mẫu duy nhất khiến dự án sinh ra chứa hàng trăm tệp rác không sử dụng.\n- **Hardcoding Corporate Secrets in Skeletons:** Để lộ API key thử nghiệm hoặc mật khẩu mẫu trong các tệp skeleton của template.\n- **Zero Maintenance on Golden Paths:** Bỏ rơi các mẫu dự án sau khi tạo, không cập nhật phiên bản thư viện bảo mật khiến các dự án mới sinh ra đã chứa sẵn lỗ hổng CVE.",
        "gates": "- **QG-01**: 100% dự án được sinh ra từ mẫu vượt qua lệnh build và kiểm thử tự động với kết quả PASS ngay từ lần đầu tiên.\n- **QG-02**: Tệp `catalog-info.yaml` hợp lệ được tạo và liên kết chính xác với thông tin nhóm sở hữu (Team Ownership).\n- **QG-03**: Dự án mới tự động kích hoạt các luồng kiểm tra bảo mật (Secret Scanning, SAST, Dependency Audit) trên nhánh chính.",
        "security": "- Bắt buộc kích hoạt Branch Protection Rules và bắt buộc Review trước khi merge trên mọi kho mã nguồn mới được sinh ra từ template.",
        "adapters": "- **Runtimes**: Spotify Backstage, Copier, Cookiecutter, GitHub API, GitLab API.",
        "deliverables": "- Thư mục khung mẫu dự án chuẩn (`template_skeleton/`).\n- Tệp định nghĩa mẫu tự phục vụ (`template.yaml`).",
        "related": "dex-terraform-module-contract-tests, dex-infrastructure-policy-as-code, dex-kubernetes-secret-delivery",
        "usage": "```bash\n# Kiem thu sinh du an tu template Copier cuc bo\ncopier copy ./templates/fastapi-service ./output-test --data service_name=test-api\ncd ./output-test && pytest\n```"
    },
    {
        "id": "dex-operational-dependency-mapping",
        "name": "dex-operational-dependency-mapping",
        "desc": "Map, analyze, and visualize service dependency graphs and critical operational paths. Identify Single Points of Failure (SPOF), evaluate blast radius, and accelerate incident triage.",
        "purpose": "Thiết lập bản đồ phụ thuộc vận hành hệ thống (Operational Dependency Mapping); thu thập và trực quan hóa đồ thị phụ thuộc giữa các dịch vụ microservices, cơ sở dữ liệu, hàng đợi và API bên thứ ba dựa trên dấu vết phân tán (Distributed Traces - OpenTelemetry), Service Mesh (Istio) hoặc công nghệ eBPF; phân tích đường găng trọng yếu (Critical Path), phát hiện các điểm lỗi đơn lẻ (Single Point of Failure - SPOF), đánh giá bán kính ảnh hưởng sự cố (Blast Radius Modeling) và tăng tốc độ xử lý sự cố.",
        "when_use": "- Khi điều tra nguyên nhân gốc rễ (Root Cause Analysis - RCA) của các sự cố phức tạp liên quan đến nhiều dịch vụ gọi chéo nhau.\n- Khi chuẩn bị thực hiện các đợt bảo trì hoặc thay đổi lớn về kiến trúc và cần biết dịch vụ nào sẽ bị ảnh hưởng nếu một node bị gián đoạn.\n- Khi thiết kế kiến trúc hệ thống phân tán để loại bỏ các phụ thuộc vòng (Circular Dependencies) hoặc các nút thắt cổ chai ẩn.",
        "when_not_use": "- Khi hệ thống là một khối nguyên khối (Monolith) độc lập hoàn toàn không có tương tác với bất kỳ dịch vụ hay CSDL bên ngoài nào.\n- Khi chỉ theo dõi các chỉ số tài nguyên phần cứng đơn giản (CPU/RAM usage máy chủ đơn lẻ).",
        "prereqs": "- **Hạ tầng giám sát:** OpenTelemetry Instrumentation trên các dịch vụ, Jaeger/Tempo, hoặc eBPF-based agent (DeepFlow, Cilium Hubble).\n- **Cơ sở dữ liệu đồ thị:** Neo4j hoặc NetworkX (Python) để mô hình hóa đồ thị có hướng (Directed Graph).",
        "concepts": "- **Critical Path Analysis:** Tuyến đường thực thi dài nhất hoặc quan trọng nhất trong chuỗi các cuộc gọi dịch vụ quyết định trực tiếp tới độ trễ phản hồi của người dùng cuối.\n- **Blast Radius:** Phạm vi thiệt hại và danh sách tất cả các dịch vụ cấp dưới (Downstream Consumers) bị ngừng hoạt động nếu một dịch vụ cấp trên (Upstream Service) bị sập.\n- **Circular Dependency Lock:** Hiện tượng dịch vụ A gọi B, B gọi C, và C lại quay ngược lại gọi A, tạo thành vòng lặp vô tận có thể làm sập toàn bộ hệ thống khi có tải cao.",
        "workflow": "1. Thu thập dữ liệu dấu vết phân tán từ OpenTelemetry Collector hoặc dữ liệu mạng eBPF.\n2. Trích xuất các cặp quan hệ nguồn - đích: `(caller_service, target_service, p95_latency, error_rate)`.\n3. Xây dựng đồ thị có hướng (Directed Graph - DAG) bằng NetworkX hoặc truy vấn đồ thị Cypher trên Neo4j.\n4. Thực hiện thuật toán phát hiện chu trình (Cycle Detection) để khẳng định không tồn tại phụ thuộc vòng giữa các dịch vụ.\n5. Tính toán độ trung tâm (Betweenness Centrality) để xác định dịch vụ nào là Single Point of Failure (SPOF).\n6. Xuất bản đồ phụ thuộc tương tác và tích hợp vào quy trình cảnh báo trực ban (PagerDuty / Slack Alert Enrichment).",
        "examples": """### Script Python phan tich do thi phu thuoc dich vu va tim SPOF bang NetworkX:
```python
import networkx as nx
import json

def analyze_service_dependencies(edges_data):
    G = nx.DiGraph()

    # Them cac canh phu thuoc (Caller -> Callee)
    for edge in edges_data:
        G.add_edge(edge['caller'], edge['callee'], weight=edge.get('latency_ms', 10))

    print(f"Total Services: {G.number_of_nodes()} | Total Dependencies: {G.number_of_edges()}")

    # 1. Phat hien phu thuoc vong (Circular Dependencies)
    cycles = list(nx.simple_cycles(G))
    if cycles:
        print(f"[CRITICAL ALERT] Found {len(cycles)} Circular Dependency cycles:")
        for c in cycles:
            print("  Cycle: " + " -> ".join(c) + " -> " + c[0])
    else:
        print("[OK] No circular dependencies detected.")

    # 2. Xac dinh Single Point of Failure (SPOF) dua tren Betweenness Centrality
    centrality = nx.betweenness_centrality(G)
    sorted_spof = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:5]
    print("\nTop 5 Critical Central Services (Potential SPOF):")
    for svc, score in sorted_spof:
        print(f"  - {svc:<24}: Centrality Score = {score:.4f}")

    # 3. Tinh toan Blast Radius neu mot dich vu bi sap
    target_failed_service = sorted_spof[0][0]
    affected_services = nx.ancestors(G, target_failed_service)
    print(f"\nBlast Radius if '{target_failed_service}' fails: {len(affected_services)} upstream services affected!")
    for s in affected_services:
        print(f"  * {s}")

# Du lieu mau
edges = [
    {"caller": "api-gateway", "callee": "auth-service"},
    {"caller": "api-gateway", "callee": "order-service"},
    {"caller": "order-service", "callee": "payment-service"},
    {"caller": "order-service", "callee": "inventory-service"},
    {"caller": "payment-service", "callee": "auth-service"},
    {"caller": "inventory-service", "callee": "database-cluster"},
    {"caller": "auth-service", "callee": "database-cluster"}
]

analyze_service_dependencies(edges)
```""",
        "antipatterns": "- **Static Outdated Architecture Diagrams:** Dựa vào các biểu đồ vẽ tay trên Confluence hoặc Miro đã lỗi thời 2 năm trước thay vì sinh bản đồ tự động từ dữ liệu mạng thực tế.\n- **Hidden Transitive Dependencies:** Bỏ qua các phụ thuộc gián tiếp (A gọi B, B gọi C) dẫn đến việc đánh giá sai lệch bán kính ảnh hưởng khi bảo trì dịch vụ C.\n- **Ignoring Third-Party External APIs:** Không đưa các API của bên thứ ba (như Stripe, Twilio) vào đồ thị phụ thuộc khiến đội trực ban bị mù thông tin khi đối tác gặp sự cố.",
        "gates": "- **QG-01**: Đồ thị phụ thuộc được cập nhật tự động hàng ngày từ dữ liệu OpenTelemetry traces hoặc Service Mesh.\n- **QG-02**: Không có bất kỳ chu trình phụ thuộc vòng (Circular Dependency) nào tồn tại giữa các dịch vụ cốt lõi.\n- **QG-03**: Mọi dịch vụ được xác định là SPOF đều có phương án dự phòng hoặc Circuit Breaker bảo vệ.",
        "security": "- Dữ liệu dấu vết và bản đồ phụ thuộc phải được làm sạch các thông tin nhạy cảm (Sanitize authorization headers và credentials).",
        "adapters": "- **Runtimes**: OpenTelemetry, Jaeger, Istio Kiali, Cilium Hubble, NetworkX (Python), Neo4j.",
        "deliverables": "- Mô-đun phân tích đồ thị phụ thuộc (`dependency_graph_analyzer.py`).\n- Biểu đồ đồ thị phụ thuộc dạng ma trận và danh sách các điểm SPOF trọng yếu (`architecture_dependency_map.json`).",
        "related": "dex-cloud-database-failover-drills, dex-api-circuit-breaker-verification, dex-release-progressive-metrics",
        "usage": "```bash\n# Trich xuat danh sach phu thuoc tu Jaeger API va phan tich do thi\npython -m scripts.ops.map_dependencies --jaeger-url http://localhost:16686 --lookback 24h\n```"
    }
]

def generate_skills():
    total = len(SKILLS_AS_AT)
    created = 0
    print("=== GENERATING GROUP AS & AT (Skills 441–460) ===")

    for idx, skill in enumerate(SKILLS_AS_AT, 1):
        skill_id = skill["id"]
        skill_dir = os.path.join(SKILLS_DIR, skill_id)
        os.makedirs(skill_dir, exist_ok=True)
        file_path = os.path.join(skill_dir, "SKILL.md")

        content = f"""---
name: {skill["name"]}
description: {skill["desc"]}
---

# {skill["id"]}

## 1. Purpose & Scope
{skill["purpose"]}

## 2. When to Use
{skill["when_use"]}

## 3. When NOT to Use
{skill["when_not_use"]}

## 4. Prerequisites & Input Context
{skill["prereqs"]}

## 5. Core Concepts & Taxonomy
{skill["concepts"]}

## 6. Step-by-Step Execution Workflow
{skill["workflow"]}

## 7. Concrete Examples
{skill["examples"]}

## 8. Anti-Patterns & Common Traps
{skill["antipatterns"]}

## 9. Quality Gates & Acceptance Criteria
{skill["gates"]}

## 10. Security & Safety Boundaries
{skill["security"]}

## 11. Platform Adapters
{skill["adapters"]}

## 12. Deliverables & Output Artifacts
{skill["deliverables"]}

## 13. Related & Complementary Skills
{skill["related"]}

## 14. Realistic Usage Example
{skill["usage"]}
"""
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        created += 1
        print(f"[{idx:02d}/{total:02d}] Created: {skill_id}")

    print(f"\nSuccessfully generated {created}/{total} skills for Groups AS & AT.")

if __name__ == "__main__":
    generate_skills()
