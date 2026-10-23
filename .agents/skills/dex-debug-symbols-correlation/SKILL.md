---
name: dex-debug-symbols-correlation
description: Correlate stripped and unstripped binaries with debug symbols (PDB, DWARF, dSYM) to reconstruct call stacks, demangle symbols, and verify source-code mapping accuracy. Use when triaging native crash dumps and conducting authorized binary analysis.
---

# dex-debug-symbols-correlation

## 1. Purpose & Scope
Tương quan và liên kết giữa file nhị phân đã tước bỏ ký hiệu (stripped) với kho debug symbols (PDB, DWARF, dSYM); tái tạo call stack chính xác, giải mã tên hàm (symbol demangling) và xác thực tính khớp đúng của source code mapping phục vụ điều tra sự cố crash hoặc phân tích nhị phân được ủy quyền.

## 2. When to Use
- Khi phân tích các file crash dump (minidump `.dmp`, core dump) từ môi trường sản xuất không có mã nguồn đi kèm.
- Khi xác minh symbol server có cung cấp đúng phiên bản PDB/DWARF khớp với bản build nhị phân đang chạy hay không.
- Khi kiểm toán tính bảo mật để đảm bảo file nhị phân thương mại đã được tước bỏ hoàn toàn thông tin đường dẫn nhạy cảm.

## 3. When NOT to Use
- Khi làm việc với các ngôn ngữ thông dịch (Python, JavaScript) đã có source maps ở định dạng web chuẩn.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** File nhị phân thực thi, tệp debug symbol tương ứng (.pdb trên Windows, .dwarf/.debug trên Linux, .dSYM trên macOS).
- **Quyền hạn truy cập:** Quyền chạy công cụ phân tích debug symbols (llvm-symbolizer, dumpbin, gdb, c++filt).

## 5. Core Concepts & Taxonomy
- **Debug Identifier / GUID:** Mã định danh duy nhất (RSDS GUID và Age trên Windows PE; Build ID trên Linux ELF) dùng để ghép cặp chính xác giữa binary và symbol file.
- **Symbol Demangling:** Chuyển đổi tên hàm bị mã hóa nội bộ của compiler (mangled name như `_ZN7MyClass8doActionEi`) về dạng dễ đọc (`MyClass::doAction(int)`).
- **Stripping Verification:** Kiểm tra bảo đảm các bảng ký hiệu không cần thiết đã được loại bỏ khỏi file phát hành thương mại.

## 6. Step-by-Step Execution Workflow
1. Trích xuất Build ID (Linux) hoặc Debug Directory RSDS GUID (Windows) từ file nhị phân mục tiêu.
2. Tìm kiếm và nạp tệp debug symbols (DWARF/PDB) có mã định danh khớp chính xác từ Symbol Server.
3. Đối chiếu địa chỉ bộ nhớ tương đối (RVA) trong crash dump với các hàm và dòng code trong source map.
4. Thực hiện demangle tên các hàm C++/Rust để tái cấu trúc cây gọi hàm (Call Stack).
5. Kiểm tra rà soát các đường dẫn file mã nguồn nhúng trong symbol để phát hiện lộ lọt cấu trúc thư mục nội bộ.
6. Tổng hợp báo cáo tương quan ký hiệu và cấu trúc ngăn xếp điều tra.

## 7. Concrete Examples
### Kiểm tra RSDS GUID và demangle symbol:
```powershell
# Kiểm tra thông tin Debug Directory của file PE trên Windows
dumpbin /HEADERS /LOADCONFIG ./app.exe | Select-String -Pattern "RSDS", "Format"

# Demangle ký hiệu C++ bị mã hóa
c++filt _ZN4Core8Database10initializeERKNSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE
# Kết quả: Core::Database::initialize(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&)

# Tương quan địa chỉ crash với mã nguồn bằng llvm-symbolizer
llvm-symbolizer --obj=./app.elf 0x401124
```

## 8. Anti-Patterns & Common Traps
- **Mismatched Symbol Age:** Dùng file PDB có cùng tên nhưng khác phiên bản build khiến call stack bị dịch chuyển sai địa chỉ dòng code.
- **Leaking Internal Paths:** Để nguyên đường dẫn ổ đĩa phát triển tuyệt đối (`C:\Users\admin\SecretProject\src`) trong file nhị phân phát hành ra ngoài.
- **Ignoring Optimization Inlining:** Quên tính toán các hàm đã bị trình biên dịch inline dẫn tới việc thiếu mắt xích trong cây gọi hàm.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Mã GUID / Build ID giữa file nhị phân và file debug symbol khớp tuyệt đối 100%.
- **QG-04**: Toàn bộ các địa chỉ trong call stack điều tra đều được giải mã thành tên hàm và số dòng code cụ thể.
- **QG-08**: Bản nhị phân phát hành thương mại không chứa các bảng ký hiệu nội bộ không mong muốn.

## 10. Security & Safety Boundaries
- Kiểm tra loại bỏ thông tin nhạy cảm và credentials tình cờ bị nhúng vào bảng chuỗi (string table) của debug symbols.

## 11. Platform Adapters
- **Tools**: dumpbin, llvm-symbolizer, c++filt, gdb, WinDbg, symchk, dwarfdump.

## 12. Deliverables & Output Artifacts
- Báo cáo phân giải call stack chi tiết.
- Bảng đối chiếu mã định danh Build ID / GUID.
- Khuyến nghị cấu hình compiler flags phục vụ strip symbols an toàn.

## 13. Related & Complementary Skills
dex-binary-provenance-matching, dex-reverse-engineering-reporting, dex-toolchain-reproducibility-audit

## 14. Realistic Usage Example
```powershell
# Xác thực tính tương thích của symbol PDB trên Windows
symchk /v ./app.exe /s C:\Symbols

# Kiểm tra Build ID của file nhị phân Linux ELF
readelf -n ./app.elf | grep "Build ID"
```
