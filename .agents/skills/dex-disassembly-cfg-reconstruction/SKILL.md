---
name: dex-disassembly-cfg-reconstruction
description: Analyze disassembled machine code (x86-64, ARM64) to reconstruct function basic blocks, control flow graphs (CFG), loop invariants, and calling convention parameter transfers using safe CLI utilities (objdump, llvm-objdump). Use when verifying compiler optimization soundness, investigating crash offsets, or analyzing suspicious binary blobs. (Strictly authorized/defensive).
---

# dex-disassembly-cfg-reconstruction

## 1. Purpose & Scope
Phân tích mã máy hợp ngữ (Disassembled Assembly x86-64 và ARM64) để tái hiện cấu trúc các khối cơ bản (Basic Blocks), đồ thị luồng điều khiển (Control Flow Graph - CFG), biến bất biến của vòng lặp và quy ước truyền tham số hàm (Calling Conventions); phục vụ xác minh tính đúng đắn của tối ưu hóa trình biên dịch hoặc phân tích các đoạn mã nhị phân đáng ngờ trong môi trường cô lập.

## 2. When to Use
- Khi trình biên dịch tạo ra mã máy tối ưu hóa bị lỗi (Compiler Optimization Bug) ở cấp độ `-O3`.
- Khi cần điều tra nguyên nhân sâu xa của lỗi nhảy địa chỉ không hợp lệ (Invalid Jump / Segfault) tại một offset cụ thể.
- Khi thẩm tra tính toàn vẹn của một thư viện nhị phân độc lập không có mã nguồn đi kèm.

## 3. When NOT to Use
- Khi ứng dụng có thể được debug dễ dàng bằng mã nguồn cấp cao (High-level Source Debugging).
- Khi cố tình phá hoại các cơ chế bảo vệ phần mềm hoặc tạo ra các công cụ bẻ khóa trái phép.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Kiến thức về kiến trúc tập lệnh x86-64 / ARM64, quy ước gọi hàm (System V AMD64 ABI hoặc Microsoft x64 calling convention), công cụ `objdump` hoặc `llvm-objdump`.
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; tuyệt đối không can thiệp trái phép vào hệ thống của bên thứ ba.

## 5. Core Concepts & Taxonomy
- **Basic Block Partitioning:** Chuỗi các lệnh máy tuần tự chỉ có duy nhất một điểm vào ở đầu và một điểm ra ở cuối (kết thúc bằng lệnh nhảy `jmp`, `call` hoặc `ret`).
- **Control Flow Graph (CFG):** Đồ thị có hướng trong đó mỗi nút là một khối cơ bản và mỗi cạnh là một nhánh điều kiện (`jz`, `jnz`).
- **Parameter Passing Registers:** Quy ước truyền tham số qua thanh ghi (x86-64 Windows: RCX, RDX, R8, R9; Linux: RDI, RSI, RDX, RCX, R8, R9).

## 6. Step-by-Step Execution Workflow
1. Xuất mã hợp ngữ của hàm mục tiêu bằng `objdump -d --no-show-raw-insn`.
2. Phân tách mã hợp ngữ thành các Basic Blocks dựa trên các nhãn địa chỉ nhảy.
3. Xác định các cung điều hướng giữa các khối để dựng đồ thị luồng điều khiển dạng sơ đồ DOT.
4. Theo dõi luồng dịch chuyển dữ liệu giữa các thanh ghi để tái hiện lại các tham số đầu vào và giá trị trả về.
5. Tổng hợp thành tài liệu đồ thị luồng điều khiển `CONTROL_FLOW_GRAPH.md`.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```bash
# Disassembling specific function using llvm-objdump
llvm-objdump --disassemble-symbols=verify_license_token --demangle binary_module.dll

# Extracting basic blocks and branch targets
# 0000000180001000 <verify_license_token>:
# 180001000:   sub    rsp, 0x28
# 180001004:   test   rcx, rcx          ; Check if token pointer is null
# 180001007:   je     18000101b         ; Jump to error block if null
# 180001009:   mov    eax, dword ptr [rcx]
# 18000100b:   cmp    eax, 0x44455801   ; Compare magic header
# 180001010:   jne    18000101b         ; Jump to error block if mismatch
# 180001012:   mov    eax, 1            ; Success return
# 180001017:   add    rsp, 0x28
# 18000101a:   ret
# 18000101b:   xor    eax, eax          ; Error return (0)
# 18000101d:   add    rsp, 0x28
# 18000101f:   ret
```

## 8. Anti-Patterns & Common Traps
- Cố gắng dịch ngược toàn bộ tệp nhị phân hàng trăm megabyte cùng lúc thay vì tập trung vào hàm nghi vấn.
- Nhầm lẫn giữa quy ước gọi hàm của Windows x64 và Linux System V x64 dẫn đến việc xác định sai tham số.
- Bỏ qua các lệnh căn chỉnh bộ đệm ngăn xếp (`sub rsp, 0x28`) dẫn đến hiểu sai độ dời của biến cục bộ.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Đồ thị luồng điều khiển xác định đầy đủ tất cả các nhánh điều kiện và điểm thoát của hàm.
- QG-02: Quy ước gọi hàm và danh sách thanh ghi tham số được nhận diện chính xác theo ABI của hệ điều hành.
- QG-03: Toàn bộ quá trình phân tích được thực hiện bằng các công cụ mã nguồn mở hợp pháp.

## 10. Security & Safety Boundaries
- Tuyệt đối không sử dụng kỹ năng để tìm kiếm lỗ hổng 0-day nhằm mục đích tấn công hoặc bán thông tin khai thác trái phép.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Hoạt động phân tích hoàn toàn hợp pháp, minh bạch và có sự ủy quyền chính thức từ chủ sở hữu hệ thống.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Sơ đồ đồ thị luồng điều khiển dạng Mermaid hoặc DOT `cfg.mermaid`.
1. Bản phân tích mã giả (Pseudocode) tái tạo lại logic nghiệp vụ của hàm.

## 13. Related & Complementary Skills
- [`dex-native-symbol-mapping`](.agents/skills/dex-native-symbol-mapping/SKILL.md)
- [`dex-rea-adapter`](.agents/skills/dex-rea-adapter/SKILL.md)
- [`dex-binary-diff-regression`](.agents/skills/dex-binary-diff-regression/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Một module tính toán toán học viết bằng C++ gặp lỗi trả về kết quả sai sau khi nâng cấp trình biên dịch Clang lên bản mới nhất. Kỹ sư kích hoạt `dex-disassembly-cfg-reconstruction` để xem mã máy sinh ra ở mức `-O3`, phát hiện trình biên dịch đã tối ưu hóa quá mức làm loại bỏ một bước kiểm tra tràn số nguyên, từ đó đưa ra giải pháp cấu hình pragma thích hợp.
