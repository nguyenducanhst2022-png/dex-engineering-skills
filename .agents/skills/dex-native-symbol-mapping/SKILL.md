---
name: dex-native-symbol-mapping
description: Reconstruct native symbol tables, demangle Itanium/MSVC C++ function signatures, map cross-reference graphs, and correlate debug symbol databases (PDB, DWARF) with stripped binaries. Use when analyzing crash dumps, tracing native exception stack traces, or auditing proprietary driver interfaces. (Strictly authorized/defensive).
---

# dex-native-symbol-mapping

## 1. Purpose & Scope
Khôi phục và ánh xạ bảng biểu tượng bản địa (Native Symbol Mapping); giải mã ngược các chữ ký hàm C++ bị mã hóa (Name Demangling cho chuẩn MSVC và Itanium ABI), xây dựng đồ thị tham chiếu chéo (Cross-Reference Graphs) và đồng bộ cơ sở dữ liệu biểu tượng gỡ lỗi (PDB trên Windows, DWARF trên Linux) với các tệp nhị phân đã bị loại bỏ symbol; phục vụ điều tra lỗi sập ứng dụng (Crash Dump Analysis).

## 2. When to Use
- Khi phân tích tệp crash dump (`.dmp` hoặc core dump) từ môi trường sản xuất mà stack trace chỉ hiện toàn địa chỉ bộ nhớ thô.
- Khi cần điều tra nguyên nhân gây lỗi ngoại lệ bộ nhớ (Memory Access Violation) trong các module native C/C++.
- Khi xây dựng máy chủ lưu trữ biểu tượng gỡ lỗi (Symbol Server) cho tổ chức.

## 3. When NOT to Use
- Khi làm việc với các ứng dụng thuần JavaScript/Python không có thành phần native code.
- Khi cố tình dịch ngược phần mềm được bảo vệ để đánh cắp thuật toán độc quyền.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Tệp Crash Dump, tệp nhị phân và tệp biểu tượng tương ứng (.pdb hoặc .dbg), công cụ `llvm-cxxfilt`, `c++filt`, `dump_syms`.
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; tuyệt đối không can thiệp trái phép vào hệ thống của bên thứ ba.

## 5. Core Concepts & Taxonomy
- **Mangled Names:** Cơ chế trình biên dịch C++ mã hóa kiểu dữ liệu tham số và namespace vào tên hàm nhị phân (ví dụ `?Execute@TaskManager@@QEAAXXZ`).
- **Symbol Server Integration:** Cơ chế tự động tải tệp PDB/DWARF tương ứng dựa trên mã định danh GUID/Age của bản dựng.
- **Stack Frame Walking:** Quá trình phân tích con trỏ khung ngăn xếp để tái hiện lại chuỗi gọi hàm từ thời điểm ứng dụng gặp sự cố.

## 6. Step-by-Step Execution Workflow
1. Trích xuất mã định danh GUID và Age từ header Debug Directory của tệp thực thi.
2. Tìm kiếm và nạp tệp PDB/DWARF tương ứng từ kho lưu trữ biểu tượng.
3. Chuyển đổi các tên hàm bị mã hóa (Mangled Symbols) sang chữ ký hàm C++ đọc được bằng công cụ demangler.
4. Đối chiếu địa chỉ instruction pointer (IP) từ tệp crash dump với bảng symbol để xác định tên hàm và số dòng mã nguồn.
5. Xuất ra tài liệu phân tích ngăn xếp gọi hàm (Annotated Stack Trace).

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```bash
# Demangling C++ Symbols via llvm-cxxfilt
# Input MSVC mangled symbol:
llvm-cxxfilt "?CalculateHash@CryptoManager@Engine@@QEAAHPEBE_K@Z"
# Output:
# public: int __cdecl Engine::CryptoManager::CalculateHash(unsigned char const *, unsigned __int64)

# Input GCC/Clang Itanium mangled symbol:
llvm-cxxfilt "_ZN6Engine13CryptoManager13CalculateHashEPKhm"
# Output:
# Engine::CryptoManager::CalculateHash(unsigned char const*, unsigned long)
```

## 8. Anti-Patterns & Common Traps
- Xóa bỏ tệp biểu tượng PDB sau khi phát hành phiên bản khiến việc phân tích crash dump trong tương lai trở nên bất khả thi.
- Cố tình đoán mò tên hàm dựa trên địa chỉ bộ nhớ mà không sử dụng bảng symbol chính xác.
- Sử dụng nhầm tệp PDB của bản dựng khác (sai lệch GUID) dẫn đến báo cáo sai lệch dòng code gây lỗi.

## 9. Quality Gates & Acceptance Criteria
- QG-01: 100% các địa chỉ bộ nhớ trong crash dump được ánh xạ chính xác về tên hàm và tệp nguồn tương ứng.
- QG-02: Bảng chữ ký hàm được giải mã hoàn toàn sang cú pháp C++ chuẩn không còn tiền tố mã hóa.
- QG-03: Mã GUID của tệp biểu tượng trùng khớp hoàn toàn với bản dựng thực thi.

## 10. Security & Safety Boundaries
- Bảo vệ các tệp biểu tượng PDB chứa thông tin đường dẫn mã nguồn nội bộ; không công khai ra bên ngoài mà không có chính sách bảo mật.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Hoạt động phân tích hoàn toàn hợp pháp, minh bạch và có sự ủy quyền chính thức từ chủ sở hữu hệ thống.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Bản phân tích Stack Trace đã được ánh xạ biểu tượng `RESOLVED_STACK_TRACE.md`.
1. Bảng ánh xạ địa chỉ bộ nhớ và hàm C++ tương ứng.

## 13. Related & Complementary Skills
- [`dex-pe-elf-structure-inspection`](.agents/skills/dex-pe-elf-structure-inspection/SKILL.md)
- [`dex-disassembly-cfg-reconstruction`](.agents/skills/dex-disassembly-cfg-reconstruction/SKILL.md)
- [`dex-reverse-evidence-chain`](.agents/skills/dex-reverse-evidence-chain/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Ứng dụng máy tính để bàn của ngân hàng gặp sự cố crash ngẫu nhiên trên máy khách hàng. Nhận được tệp crash dump 50MB toàn địa chỉ hex. Kỹ sư kích hoạt `dex-native-symbol-mapping`, kết nối PDB của phiên bản đó và giải mã chữ ký C++, xác định chính xác lỗi con trỏ null tại dòng 142 trong tệp `NetworkSocket.cpp`.
