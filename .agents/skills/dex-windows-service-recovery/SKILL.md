---
name: dex-windows-service-recovery
description: Implement, configure, and test Windows Service architectures and recovery policies. Manage Service Control Manager (SCM) interactions, graceful shutdowns, and failure restart actions.
---

# dex-windows-service-recovery

## 1. Purpose & Scope
Thiết kế, cài đặt và kiểm tra độ bền vững của ứng dụng dịch vụ chạy ngầm trên Windows (Windows Service Lifecycle Management); cấu hình giao tiếp với Service Control Manager (SCM), xử lý chính xác các tín hiệu điều khiển `SERVICE_CONTROL_STOP`, `SERVICE_CONTROL_SHUTDOWN` và `SERVICE_CONTROL_PRESHUTDOWN`; thiết lập chính sách tự động phục hồi khi gặp sự cố (`SERVICE_FAILURE_ACTIONS`: tự khởi động lại, chạy chương trình cứu hộ) và bảo đảm thời gian dừng dịch vụ an toàn không làm mất dữ liệu.

## 2. When to Use
- Khi phát triển các daemon xử lý dữ liệu ngầm, máy chủ agent giám sát bảo mật hoặc worker xử lý tác vụ nền trên Windows Server.
- Khi dịch vụ bị SCM cưỡng chế tắt ngang (Killed) do không phản hồi kịp thời hạn dừng dịch vụ (Service Stop Timeout).
- Khi cần tự động hóa cấu hình chính sách phục hồi dịch vụ tự động sau khi bị sập bằng lệnh `sc.exe` hoặc PowerShell.

## 3. When NOT to Use
- Khi ứng dụng có giao diện tương tác người dùng (kể từ Windows Vista, Session 0 Isolation cấm tuyệt đối Windows Service hiển thị UI).
- Khi tác vụ là một công việc định kỳ chạy một lần (nên dùng Windows Task Scheduler thay vì duy trì một service chạy liên tục).

## 4. Prerequisites & Input Context
- **Hệ điều hành:** Windows 10/11 hoặc Windows Server 2019/2022.
- **Quyền hạn quản trị:** Quyền Administrator để cài đặt và điều khiển SCM qua `sc.exe`.

## 5. Core Concepts & Taxonomy
- **Session 0 Isolation:** Rào chắn an ninh của Windows cô lập toàn bộ các service trong Session 0 tách biệt hoàn toàn với Session của người dùng đăng nhập, triệt tiêu nguy cơ tấn công Shatter Attack.
- **SCM Handshake & Status Updates:** Quy trình dịch vụ định kỳ cập nhật trạng thái `SERVICE_STATUS` (`SERVICE_START_PENDING`, `SERVICE_RUNNING`, `SERVICE_STOP_PENDING`) và chỉ số `dwCheckPoint` để báo cáo với SCM rằng tiến trình vẫn đang hoạt động bình thường.
- **SERVICE_FAILURE_ACTIONS:** Cấu trúc định nghĩa hành vi của hệ điều hành khi service bị sập bất ngờ: Lần 1 tự restart sau 1 phút, Lần 2 restart sau 5 phút, Lần 3 chạy script khôi phục.

## 6. Step-by-Step Execution Workflow
1. Khai báo hàm `ServiceMain` và bảng điều phối `SERVICE_TABLE_ENTRY` tại hàm `main`.
2. Đăng ký hàm xử lý sự kiện điều khiển thông qua `RegisterServiceCtrlHandlerEx`.
3. Báo cáo trạng thái `SERVICE_RUNNING` với SCM sau khi khởi tạo thành công các luồng worker.
4. Khi nhận lệnh `SERVICE_CONTROL_STOP`, chuyển trạng thái sang `SERVICE_STOP_PENDING`, phát tín hiệu hủy cho worker và định kỳ tăng `dwCheckPoint`.
5. Thu dọn kết nối CSDL, đóng tệp nhật ký và báo cáo `SERVICE_STOPPED`.
6. Cấu hình chính sách tự phục hồi bằng lệnh `sc.exe failure` với các hành động khởi động lại.

## 7. Concrete Examples
### Khung ma nguon C++ chuan cho Windows Service co ho tro Stop graceful:
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
```

## 8. Anti-Patterns & Common Traps
- **Attempting Interactive UI from Service:** Cố gắng gọi `MessageBox` hoặc tạo cửa sổ từ Windows Service, khiến tiến trình bị treo vô tận do Session 0 Isolation.
- **Ignoring SERVICE_STOP_PENDING Checkpoints:** Thực hiện quá trình dọn dẹp kéo dài 20 giây mà không cập nhật `dwCheckPoint` cho SCM, khiến Windows coi service bị treo và kill tiến trình.
- **Hardcoding LocalSystem Account:** Chạy service bằng tài khoản quyền lực tối cao `NT AUTHORITY\SYSTEM` thay vì tạo tài khoản dịch vụ chuyên dụng `NT SERVICE\<ServiceName>` với đặc quyền tối thiểu.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Dịch vụ dừng hoàn toàn (Graceful Stop) trong vòng 5 giây sau khi nhận lệnh `net stop` mà không bị rò rỉ dữ liệu.
- **QG-02**: Chính sách phục hồi (Recovery Actions) được cấu hình tự động khởi động lại dịch vụ sau khi tiến trình bị kill cưỡng bức.
- **QG-03**: Dịch vụ hoạt động an toàn dưới tài khoản Virtual Account với nguyên tắc Least Privilege.

## 10. Security & Safety Boundaries
- Khóa chặt quyền truy cập Service ACL (Security Descriptor); ngăn chặn người dùng không có quyền quản trị sửa đổi đường dẫn tệp thực thi (Unquoted Service Path).

## 11. Platform Adapters
- **Runtimes**: C++ Win32 SCM API, C# TopShelf / Microsoft.Extensions.Hosting.WindowsServices, PowerShell `sc.exe`.

## 12. Deliverables & Output Artifacts
- Mã nguồn dịch vụ Windows (`service_core.cpp` / `service.cs`).
- Kịch bản cài đặt và cấu hình chính sách phục hồi tự động (`install_service.ps1`).

## 13. Related & Complementary Skills
dex-windows-app-crash-dumps, dex-windows-code-signing-installer, dex-windows-usb-portability

## 14. Realistic Usage Example
```powershell
# Cau hinh chinh sach tu dong phuc hoi cho Service bang sc.exe
sc.exe failure "DEXWorkerService" reset= 86400 actions= restart/60000/restart/120000/run/300000 command= "C:\Scripts\alert.bat"
```
