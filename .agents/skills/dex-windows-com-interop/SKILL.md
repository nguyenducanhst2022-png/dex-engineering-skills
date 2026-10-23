---
name: dex-windows-com-interop
description: Integrate, manage, and debug Component Object Model (COM) interfaces in Windows. Handle STA/MTA apartments, reference counting lifetimes, and diagnose marshaling and threading errors.
---

# dex-windows-com-interop

## 1. Purpose & Scope
Tích hợp, điều phối và chẩn đoán các giao diện Component Object Model (COM / OLE / ActiveX) trong hệ điều hành Windows; khởi tạo và quản lý an toàn căn hộ luồng (Single-Threaded Apartments - STA vs Multi-Threaded Apartments - MTA) thông qua `CoInitializeEx`; quản lý vòng đời đếm tham chiếu (Reference Counting: `AddRef`, `Release`, CComPtr, winrt::com_ptr), ngăn chặn rò rỉ bộ nhớ COM và xử lý các lỗi truyền đối tượng xuyên luồng (Cross-Apartment Marshaling Errors: `RPC_E_WRONG_THREAD`).

## 2. When to Use
- Khi tương tác với các API hệ thống Windows cốt lõi chỉ hỗ trợ COM (Windows Shell, Taskbar Progress, UI Automation, WMI, DirectShow, Media Foundation).
- Khi tích hợp hoặc xây dựng các phần mở rộng cho bộ ứng dụng Microsoft Office qua COM Add-in.
- Khi ứng dụng bị sập hoặc trả về mã lỗi `CO_E_NOTINITIALIZED`, `REGDB_E_CLASSNOTREG` hoặc `RPC_E_WRONG_THREAD`.

## 3. When NOT to Use
- Khi sử dụng các API Win32 thuần túy hoặc các dịch vụ mạng REST/gRPC không yêu cầu cơ chế COM.
- Khi phát triển ứng dụng trên Linux hoặc macOS nơi COM không được hỗ trợ tự nhiên.

## 4. Prerequisites & Input Context
- **Môi trường phát triển:** C++ (ATL/WRL/C++/WinRT), C# (COM Interop), hoặc Rust (`windows-rs`).
- **Thư viện hệ thống:** `ole32.lib`, `oleaut32.lib`.

## 5. Core Concepts & Taxonomy
- **Apartment Threading Models (STA vs MTA):** STA ràng buộc các đối tượng COM với một luồng cụ thể và sử dụng Message Loop để đồng bộ hóa; MTA cho phép nhiều luồng gọi đồng thời vào đối tượng nhưng đòi hỏi đối tượng phải có cơ chế khóa an toàn (Thread-safe).
- **Reference Counting Semantics:** Mỗi khi con trỏ COM được sao chép, phải gọi `AddRef()`; khi không sử dụng nữa, bắt buộc gọi `Release()`. Khi số đếm về 0, đối tượng tự hủy khỏi bộ nhớ.
- **Interface Querying (IUnknown::QueryInterface):** Cơ chế định danh runtime chuẩn của COM cho phép kiểm tra và chuyển đổi giữa các giao diện của cùng một đối tượng dựa trên mã GUID/IID.

## 6. Step-by-Step Execution Workflow
1. Khởi tạo COM Apartment phù hợp cho luồng hiện tại: `CoInitializeEx(nullptr, COINIT_APARTMENTTHREADED)` cho GUI hoặc `COINIT_MULTITHREADED` cho Worker.
2. Sử dụng Smart Pointer chuyên dụng (`_com_ptr_t`, `CComPtr`, hoặc `winrt::com_ptr`) để tự động hóa việc gọi `Release()`.
3. Tạo phiên bản đối tượng COM bằng hàm `CoCreateInstance()` với CLSID và IID mục tiêu.
4. Thực hiện các thao tác trên giao diện và xử lý mã trả về `HRESULT` bằng macro `FAILED(hr)` hoặc `SUCCEEDED(hr)`.
5. Nếu cần truyền con trỏ COM sang một luồng khác, sử dụng `RoGetAgileReference` hoặc `CoMarshalInterThreadInterfaceInStream` để sinh proxy an toàn.
6. Đóng căn hộ COM bằng `CoUninitialize()` khi luồng kết thúc.

## 7. Concrete Examples
### Tich hop Taskbar Progress API thong qua ITaskbarList3 COM Interface trong C++:
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
```

## 8. Anti-Patterns & Common Traps
- **Calling COM without CoInitializeEx:** Gọi các API COM trên luồng mới mà quên khởi tạo căn hộ luồng khiến hàm trả về lỗi `CO_E_NOTINITIALIZED`.
- **Manual AddRef/Release Leaks:** Quản lý con trỏ COM bằng tay không dùng Smart Pointer, dẫn đến việc quên gọi `Release()` khi gặp nhánh rẽ lỗi (Exception) gây rò rỉ bộ nhớ.
- **Passing Raw STA Pointer to MTA Thread:** Chia sẻ con trỏ giao diện STA cho luồng worker gọi trực tiếp mà không qua Marshaling, dẫn đến lỗi sập hoặc trả mã `RPC_E_WRONG_THREAD`.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: 100% các đối tượng COM được quản lý bởi Smart Pointers an toàn (`ComPtr`), 0 lỗi rò rỉ tham chiếu.
- **QG-02**: Mọi cuộc gọi COM API đều kiểm tra mã trả về `HRESULT` bằng macro `SUCCEEDED` hoặc `FAILED`.
- **QG-03**: Khởi tạo và giải phóng căn hộ luồng (`CoInitializeEx` / `CoUninitialize`) cân bằng chính xác trên mỗi luồng.

## 10. Security & Safety Boundaries
- Tránh nạp các COM Inproc Server không rõ nguồn gốc; kiểm tra tính toàn vẹn của đăng ký CLSID trong Registry.

## 11. Platform Adapters
- **Runtimes**: C++ (WRL, ATL, C++/WinRT), C# .NET COM Interop, Rust windows-rs.

## 12. Deliverables & Output Artifacts
- Lớp bao bọc đối tượng COM tiện ích (`com_utility.hpp` / `com.rs`).
- Bộ kiểm thử tự động xác minh quản lý vòng đời và bắt lỗi căn hộ luồng.

## 13. Related & Complementary Skills
dex-windows-native-ui-accessibility, dex-windows-input-api-integration, dex-windows-service-recovery

## 14. Realistic Usage Example
```powershell
# Truy van cac COM Class duoc dang ky trong he thong bang PowerShell
Get-ChildItem -Path Registry::HKEY_CLASSES_ROOT\CLSID | Select-Object -First 10
```
