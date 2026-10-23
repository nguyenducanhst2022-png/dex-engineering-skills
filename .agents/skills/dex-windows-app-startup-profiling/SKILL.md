---
name: dex-windows-app-startup-profiling
description: Profile, measure, and optimize Windows desktop application startup performance. Trace cold and warm launch phases, diagnose static DLL loading delays, and analyze ETW traces.
---

# dex-windows-app-startup-profiling

## 1. Purpose & Scope
Đo lường, định hình (Profiling) và tối ưu hóa thời gian khởi động của ứng dụng desktop Windows; phân tích chi tiết hai giai đoạn Khởi động lạnh (Cold Start) và Khởi động ấm (Warm Start); phát hiện các nút thắt cổ chai do nạp DLL tĩnh (Static DLL Imports), nghẽn I/O đọc đĩa, hoặc khởi tạo dịch vụ đồng bộ trên Main Thread; sử dụng Event Tracing for Windows (ETW) và Windows Performance Analyzer (WPA) để đạt mục tiêu khởi chạy dưới 1 giây.

## 2. When to Use
- Khi ứng dụng desktop bị người dùng phàn nàn là khởi động quá chậm, xuất hiện hiện tượng chuột xoay vòng (Wait cursor) kéo dài.
- Khi bổ sung nhiều thư viện bên thứ ba khiến kích thước tệp và số lượng DLL nạp khi nạp chương trình tăng vọt.
- Khi cần thiết lập chỉ số hồi quy thời gian khởi động (Startup Regression Tests) trong pipeline CI/CD.

## 3. When NOT to Use
- Khi tối ưu hóa các ứng dụng server chạy ngầm liên tục 24/7 nơi thời gian khởi động ban đầu không ảnh hưởng tới người dùng cuối.
- Khi phân tích hiệu năng nạp trang web trên trình duyệt (sử dụng Lighthouse hoặc Chrome DevTools).

## 4. Prerequisites & Input Context
- **Hệ thống đo kiểm:** Windows 10/11 x64, Windows Performance Toolkit (WPT: `xperf`, `wpr`).
- **Ứng dụng mục tiêu:** Bản dựng Release kèm tệp ký hiệu gỡ lỗi đầy đủ (`.pdb`).

## 5. Core Concepts & Taxonomy
- **Cold Start vs Warm Start:** Khởi động lạnh diễn ra khi mã nhị phân và dữ liệu chưa có sẵn trong bộ nhớ đệm RAM (Standby List), đòi hỏi đọc từ ổ đĩa cứng; Khởi động ấm tận dụng dữ liệu đã được cache sẵn trong RAM.
- **Delay-Loaded DLLs (/DELAYLOAD):** Kỹ thuật biên dịch của MSVC cho phép hoãn việc nạp một DLL cho đến khi hàm đầu tiên trong DLL đó thực sự được gọi thay vì nạp ngay lúc khởi động tiến trình.
- **Event Tracing for Windows (ETW):** Hệ thống ghi vết nhân hệ điều hành hiệu năng siêu cao, cho phép theo dõi chi tiết từng sự kiện tạo luồng, cấp phát bộ nhớ, và I/O đĩa.

## 6. Step-by-Step Execution Workflow
1. Khởi động công cụ ghi vết Windows Performance Recorder: `wpr -start GeneralProfile -start CPU -start DiskIO`.
2. Khởi chạy ứng dụng mục tiêu và đo thời gian đến khi cửa sổ đầu tiên hiển thị và sẵn sàng nhận tương tác (Time to Interactive).
3. Dừng ghi vết và lưu tệp: `wpr -stop startup_trace.etl`.
4. Mở tệp `.etl` trong Windows Performance Analyzer (WPA) và nạp PDB Symbols.
5. Kiểm tra biểu đồ "Regions of Interest" và "CPU Usage (Sampled)" để tìm hàm chiếm dụng CPU lâu nhất trong `wWinMain`.
6. Chuyển đổi các DLL không cần thiết sang cờ `/DELAYLOAD` và dời các tác vụ khởi tạo mạng/CSDL sang Background Thread.

## 7. Concrete Examples
### Cau hinh Delay-Load DLL trong file CMakeLists.txt de tang toc khoi dong:
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
param([string]$AppPath = "C:\MyApp\app.exe")

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
```

## 8. Anti-Patterns & Common Traps
- **Heavy Synchronous Initialization in WinMain:** Đọc tệp cấu hình lớn, tạo kết nối CSDL hoặc gọi REST API đồng bộ ngay trên luồng giao diện chính trước khi hiển thị cửa sổ.
- **Static Linking of Hundreds of Unused DLLs:** Liên kết tĩnh hàng tá DLL tiện ích khiến hệ điều hành mất hàng trăm mili-giây để phân giải bảng import table khi nạp PE header.
- **Splash Screen Overhead:** Sử dụng màn hình chào (Splash Screen) quá phức tạp tự nó chiếm thêm 500ms CPU chỉ để vẽ hoạt ảnh khởi động.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Thời gian Warm Start (Time to Interactive) đạt dưới 800ms trên cấu hình máy tính văn phòng tiêu chuẩn.
- **QG-02**: Không có bất kỳ tác vụ I/O mạng nào được thực thi đồng bộ trên luồng chính trong quá trình khởi động.
- **QG-03**: 100% các DLL phụ trợ nặng đều được cấu hình `/DELAYLOAD`.

## 10. Security & Safety Boundaries
- Đảm bảo các thư viện Delay-Load được nạp từ các thư mục được bảo vệ của hệ thống; phòng chống tấn công DLL Hijacking.

## 11. Platform Adapters
- **Runtimes**: Windows Performance Toolkit (WPR/WPA), MSVC Linker (/DELAYLOAD), Intel VTune, Sysinternals RAMMap.

## 12. Deliverables & Output Artifacts
- Tệp cấu hình ghi vết ETW (`startup_profile.wprp`).
- Báo cáo phân tích thời gian khởi động ứng dụng (`startup_analysis_report.md`).

## 13. Related & Complementary Skills
dex-windows-input-api-integration, dex-win32-dpi-multi-monitor-layout, dex-windows-app-crash-dumps

## 14. Realistic Usage Example
```powershell
# Ghi vet ETW qua trinh khoi dong bang cong cu xperf
xperf -on PROC_THREAD+LOADER+CSWITCH+PROFILE -f trace.etl
Start-Process "my_app.exe"
xperf -d trace_final.etl
```
