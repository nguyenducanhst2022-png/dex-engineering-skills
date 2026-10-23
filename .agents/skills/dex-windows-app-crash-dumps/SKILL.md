---
name: dex-windows-app-crash-dumps
description: Capture, configure, and analyze native Windows crash dumps (Minidump, WER). Triage crash signatures using WinDbg and CDB, manage symbol servers, and isolate memory corruptions.
---

# dex-windows-app-crash-dumps

## 1. Purpose & Scope
Thu thập, cấu hình và phân tích chuyên sâu các tệp kết xuất sự cố ứng dụng Windows (Crash MiniDumps & Windows Error Reporting - WER); thiết lập cơ chế bắt ngoại lệ không được xử lý (`SetUnhandledExceptionFilter`), tự động ghi tệp dump nhị phân qua API `MiniDumpWriteDump`; sử dụng công cụ gỡ lỗi dòng lệnh CDB/WinDbg và máy chủ ký hiệu (Symbol Server) để phân tích vết ngăn xếp (Stack Trace), xác định chính xác nguyên nhân lỗi vi phạm truy cập bộ nhớ (Access Violation `0xC0000005`) hoặc hỏng vùng nhớ Heap.

## 2. When to Use
- Khi ứng dụng desktop bị biến mất đột ngột (Silent Crash) trên máy tính khách hàng mà không để lại thông báo lỗi.
- Khi điều tra các lỗi sập khó tái hiện ngẫu nhiên liên quan đến đa luồng, race conditions hoặc giải phóng bộ nhớ kép (Double Free).
- Khi xây dựng hạ tầng thu thập báo cáo lỗi tự động (Crash Reporting Pipeline: Sentry Native, Breakpad, Crashpad).

## 3. When NOT to Use
- Khi xử lý các ngoại lệ nghiệp vụ thông thường trong các ngôn ngữ có Garbage Collection (như C# Exception) đã có khối `try/catch` xử lý.
- Khi phân tích lỗi hệ điều hành xanh màn hình (BSOD Kernel Dump - thuộc phạm vi Driver Development).

## 4. Prerequisites & Input Context
- **Hệ thống phân tích:** Windows SDK Debugging Tools for Windows (`cdb.exe`, `windbg.exe`).
- **Kho lưu trữ ký hiệu:** Tệp `.pdb` khớp chính xác với mã băm nhị phân của bản phát hành ứng dụng.

## 5. Core Concepts & Taxonomy
- **MiniDumpWriteDump:** Hàm API Win32 thuộc thư viện `dbghelp.dll` cho phép kết xuất bộ nhớ của tiến trình và luồng gặp nạn thành tệp `.dmp` nhỏ gọn.
- **Access Violation (0xC0000005):** Ngoại lệ phần cứng do CPU phát hiện khi một tiến trình cố tình đọc/ghi vào một địa chỉ ô nhớ không hợp lệ hoặc không có quyền truy cập.
- **Source Indexing & Symbol Server:** Cơ chế lưu trữ và tự động liên kết các tệp PDB với kho mã nguồn Git thông qua `symstore.exe` và `srctool.exe`.

## 6. Step-by-Step Execution Workflow
1. Đăng ký bộ lọc ngoại lệ toàn cục tại điểm vào chương trình: `SetUnhandledExceptionFilter(CrashHandlerFilter)`.
2. Khi xảy ra sập, khởi tạo tiến trình con phụ trợ hoặc gọi an toàn `MiniDumpWriteDump` với các cờ `MiniDumpWithDataSegs` và `MiniDumpWithIndirectlyReferencedMemory`.
3. Lưu tệp `.dmp` vào thư mục AppData an toàn của người dùng.
4. Mở tệp dump bằng công cụ CDB tự động: `cdb -z crash.dmp -c "!analyze -v; q"`.
5. Nạp ký hiệu gỡ lỗi và kiểm tra khung ngăn xếp nơi xảy ra lỗi (FAULTING_IP, FAILURE_BUCKET_ID).
6. Phân tích trạng thái thanh ghi và câu lệnh Assembly tại thời điểm sập để xác định bản chất của bug.

## 7. Concrete Examples
### Cai dat Custom Unhandled Exception Filter tu dong ghi MiniDump trong C++:
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
```

## 8. Anti-Patterns & Common Traps
- **Allocating Dynamic Memory inside Crash Handler:** Cố gọi `new`, `malloc` hoặc hàm cấp phát heap bên trong Unhandled Exception Filter khi vùng nhớ Heap đã bị hỏng khiến tiến trình bị deadlock vĩnh viễn.
- **Discarding PDB Files after Build:** Xóa bỏ tệp `.pdb` sau khi build bản release khiến các tệp dump thu thập về từ người dùng không thể phân giải tên hàm và số dòng mã.
- **Writing Full Memory Dumps Unconditionally:** Luôn ghi Full Dump (vài Gigabyte) làm tràn ổ cứng người dùng và tốn băng thông truyền tải mạng.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Tệp MiniDump được tạo thành công 100% khi ứng dụng gặp sự cố Access Violation giả lập.
- **QG-02**: Lệnh `!analyze -v` trong WinDbg phân giải chính xác tên hàm và số dòng trong tệp nguồn gốc.
- **QG-03**: Bộ xử lý sự cố không thực hiện bất kỳ thao tác cấp phát Heap nào bên trong Exception Filter.

## 10. Security & Safety Boundaries
- Loại bỏ các thông tin nhạy cảm (như mật khẩu hoặc token trong bộ nhớ) khỏi dump nếu áp dụng cơ chế Full Memory Dump.

## 11. Platform Adapters
- **Runtimes**: Windows DbgHelp API, WinDbg / CDB CLI, Google Crashpad, Sentry Native SDK.

## 12. Deliverables & Output Artifacts
- Thư viện bắt sự cố native (`crash_reporter.cpp` / `crash.rs`).
- Kịch bản tự động phân tích crash dump bằng CDB (`triage_dump.py`).

## 13. Related & Complementary Skills
dex-windows-service-recovery, dex-windows-app-startup-profiling, dex-windows-com-interop

## 14. Realistic Usage Example
```powershell
# Phan tich crash dump tu dong bang cdb tu Windows SDK
& "C:\Program Files (x86)\Windows Kits\10\Debuggers\x64\cdb.exe" -z crash_dump.dmp -c "!analyze -v; kp; q"
```
