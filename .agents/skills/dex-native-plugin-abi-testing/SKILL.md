---
name: dex-native-plugin-abi-testing
description: Design cross-language C Foreign Function Interface (FFI) boundary tests, verifying struct memory layouts, calling conventions, string encoding boundaries, and pointer ownership transfer. Use when building native plugins for Node.js (N-API), Python (ctypes/CFFI), Unity, or Rust.
---

# dex-native-plugin-abi-testing

## 1. Purpose & Scope
Thiết kế và xây dựng bộ kiểm thử ranh giới giao tiếp hàm ngoại lai (Foreign Function Interface - FFI) chuẩn C ABI xuyên ngôn ngữ; kiểm chứng tính tương thích của bố cục bộ nhớ cấu trúc (Struct Padding & Alignment), quy ước gọi hàm (`cdecl`, `stdcall`), ranh giới mã hóa chuỗi ký tự UTF-8/UTF-16 và quyền sở hữu con trỏ bộ nhớ (Pointer Ownership Transfer); ngăn ngừa các lỗi sập ứng dụng nghiêm trọng (Segmentation Faults) khi tích hợp module native C/C++/Rust vào Node.js, Python, C# Unity.

## 2. When to Use
- Khi xây dựng thư viện native C++ hoặc Rust để nhúng vào ứng dụng Node.js (qua N-API) hoặc Python (qua ctypes).
- Khi tạo các plugin native cho động cơ game Unity (C# P/Invoke gọi thư viện C++ .dll/.so).
- Khi cập nhật phiên bản trình biên dịch native và cần đảm bảo không phá vỡ tính tương thích nhị phân (Binary Compatibility) với các ứng dụng máy khách.

## 3. When NOT to Use
- Khi hai ứng dụng giao tiếp với nhau qua giao thức mạng HTTP hoặc gRPC (có ranh giới mạng cô lập).
- Khi làm việc hoàn toàn trong cùng một ngôn ngữ lập trình duy nhất.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Mã nguồn thư viện native C/C++/Rust, ứng dụng gọi cấp cao (Node.js/Python/C#), công cụ kiểm tra bố cục bộ nhớ (`offsetof`).
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; bảo vệ toàn vẹn tài sản kỹ nghệ và dữ liệu sản xuất.

## 5. Core Concepts & Taxonomy
- **C ABI Stability:** Ngôn ngữ C được coi là ngôn ngữ giao tiếp chung phổ quát nhất; các ngôn ngữ cấp cao đều hỗ trợ gọi hàm theo chuẩn C ABI.
- **Struct Alignment & Padding:** Các trường dữ liệu trong struct được căn chỉnh theo bội số của kích thước (4 byte, 8 byte); nếu hai bên định nghĩa lệch nhau dù chỉ 1 byte đệm sẽ làm sai lệch toàn bộ dữ liệu.
- **Memory Ownership Contract:** Quy định rõ bên nào cấp phát bộ nhớ (Allocation) thì bên đó phải chịu trách nhiệm giải phóng bộ nhớ (Free), không bao giờ giải phóng con trỏ chéo ngôn ngữ.

## 6. Step-by-Step Execution Workflow
1. Định nghĩa giao diện công khai thuần túy theo chuẩn C với chỉ thị `extern "C"` và quy ước gọi hàm rõ ràng.
2. Kiểm tra kích thước và độ dời (`sizeof` và `offsetof`) của từng trường trong struct ở cả hai ngôn ngữ.
3. Viết hàm giải phóng bộ nhớ chuyên dụng do chính thư viện native cung cấp (`free_native_buffer`).
4. Thực hiện truyền nhận chuỗi ký tự có kiểm tra độ dài và chuyển đổi mã hóa an toàn.
5. Chạy bộ kiểm thử tự động với AddressSanitizer (ASan) để phát hiện rò rỉ hoặc đọc bộ nhớ ngoài phạm vi.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```c
// C ABI Safe Export Interface Header (native_plugin.h)
#ifndef NATIVE_PLUGIN_H
#define NATIVE_PLUGIN_H

#include <stdint.h>

#ifdef _WIN32
  #define FFI_EXPORT __declspec(dllexport)
#else
  #define FFI_EXPORT __attribute__((visibility("default")))
#endif

#pragma pack(push, 8) // Enforce explicit 8-byte alignment
typedef struct {
    uint64_t entityId;
    double posX;
    double posY;
    int32_t health;
    int32_t padding; // Explicit padding
} EntityDataC;
#pragma pack(pop)

#ifdef __cplusplus
extern "C" {
#endif

FFI_EXPORT int32_t process_entities(const EntityDataC* entities, int32_t count);
FFI_EXPORT void free_string_buffer(char* ptr);

#ifdef __cplusplus
}
#endif

#endif
```

## 8. Anti-Patterns & Common Traps
- Truyền trực tiếp đối tượng C++ phức tạp (như `std::string` hoặc `std::vector`) qua ranh giới FFI (định dạng nội bộ của C++ STL thay đổi tùy theo từng trình biên dịch làm sập chương trình ngay lập tức).
- Cấp phát mảng trong C++ bằng `new[]` rồi bên C# giải phóng bằng `Marshal.FreeHGlobal` (gây hỏng bộ quản lý vùng nhớ heap).
- Bỏ qua quy ước đóng gói struct (`#pragma pack`), dẫn đến việc struct trên Windows 64-bit có kích thước 24 byte nhưng bên Python lại đọc thành 20 byte.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Kích thước `sizeof` và độ dời `offsetof` của 100% các struct trùng khớp tuyệt đối giữa hai ngôn ngữ.
- QG-02: Vượt qua 10,000 lượt gọi hàm FFI liên tục mà không có hiện tượng rò rỉ bộ nhớ (kiểm tra bằng Valgrind / ASan).
- QG-03: Không có bất kỳ ngoại lệ C++ nào bị thoát ra ngoài ranh giới `extern "C"` (phải bao bọc bằng `try-catch`).

## 10. Security & Safety Boundaries
- Kiểm tra giới hạn con trỏ và độ dài mảng truyền vào hàm FFI để triệt tiêu lỗ hổng tràn bộ đệm (Buffer Overflow).
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Tệp tiêu đề C ABI chuẩn hóa `native_plugin.h`.
1. Bộ test tự động kiểm tra ranh giới FFI chạy bằng AddressSanitizer.

## 13. Related & Complementary Skills
- [`dex-ffi-boundary-contracts`](.agents/skills/dex-ffi-boundary-contracts/SKILL.md)
- [`dex-cpp-memory-safety`](.agents/skills/dex-cpp-memory-safety/SKILL.md)
- [`dex-rust-unsafe-audit`](.agents/skills/dex-rust-unsafe-audit/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Game Unity tích hợp thư viện mã hóa viết bằng C++ bị sập ngẫu nhiên khi phát hành trên Android và iOS. Kỹ sư kích hoạt `dex-native-plugin-abi-testing`, phát hiện struct tọa độ trong C# bị lệch 4 byte padding so với định nghĩa trong C++ do trình biên dịch Clang trên ARM64 căn chỉnh theo 8 byte. Thêm chỉ thị `#pragma pack(8)` đồng bộ, chấm dứt hoàn toàn hiện tượng crash game.
