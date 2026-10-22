---
name: dex-cpp-memory-safety
description: Detect, eliminate, and prevent memory safety bugs in modern C++ (C++17/20) using AddressSanitizer (ASan), UndefinedBehaviorSanitizer (UBSan), smart pointers, and RAII principles. Use when auditing legacy C++ or writing high-performance native engines.
---

# dex-cpp-memory-safety

## 1. Purpose & Scope
Phát hiện, loại bỏ và ngăn ngừa các lỗ hổng an toàn bộ nhớ trong C++ hiện đại (Modern C++17/20); chuyển đổi sang mô hình RAII (Resource Acquisition Is Initialization), sử dụng con trỏ thông minh (`std::unique_ptr`, `std::shared_ptr`), và khai thác triệt để các bộ kiểm tra động (AddressSanitizer, MemorySanitizer, UndefinedBehaviorSanitizer) nhằm triệt tiêu các lỗi Use-After-Free, Buffer Overflow và Memory Leaks.

## 2. When to Use
- C++ codebase gặp hiện tượng crash ngẫu nhiên với lỗi `Segmentation fault (core dumped)`.
- Phát hiện lỗ hổng bảo mật nghiêm trọng liên quan đến tràn bộ đệm (Buffer Overflow) hoặc Use-After-Free.
- Hiện đại hóa mã nguồn C++ legacy cũ (C++98/03) sang chuẩn C++20 an toàn.

## 3. When NOT to Use
- Không tự quản lý bộ nhớ thủ công bằng `malloc/free` hoặc `new/delete` trong mã nguồn C++ hiện đại.
- Không bật Sanitizers trong binary release production vì làm giảm hiệu năng thực thi.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Mã nguồn C/C++ cần kiểm tra.
- File cấu hình build (CMakeLists.txt, Makefile).
- Bộ dữ liệu kiểm thử tải và fuzzer inputs.
- **Điều kiện tiên quyết**:
- Trình biên dịch hiện đại (Clang 14+ hoặc GCC 11+) có hỗ trợ đầy đủ các cờ Sanitizer.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- RAII & Smart Pointers: Mọi tài nguyên (bộ nhớ, file descriptor, mutex) phải được quản lý bởi một đối tượng trên Stack có destructor tự động thu dọn khi rời khỏi phạm vi (scope).
- Memory Bugs phổ biến:
  + Use-After-Free (UAF): Truy cập vào vùng nhớ sau khi đã bị giải phóng.
  + Out-of-Bounds Access: Đọc/ghi ngoài giới hạn mảng.
  + Memory Leak: Cấp phát bộ nhớ nhưng đánh mất con trỏ trỏ tới nó.
- Sanitizers: ASan (bắt lỗi bộ nhớ), UBSan (bắt lỗi tràn số nguyên, null pointer dereference), TSan (bắt data race đa luồng).
- **Quy tắc quyết định kỹ thuật**:
- Tuyệt đối cấm sử dụng raw owning pointers (`T*` với `new`); luôn dùng `std::unique_ptr<T>` cho quyền sở hữu độc quyền.
- Mọi commit mã nguồn C++ trong CI bắt buộc phải chạy qua test suite được compile với cờ ASan và UBSan.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Trả về một tham chiếu (`return &localVar;`) trỏ tới một biến cục bộ trên Stack đã bị hủy sau khi hàm kết thúc.

## 6. Step-by-Step Execution Workflow
1. Cấu hình CMake kích hoạt các cờ AddressSanitizer và UndefinedBehaviorSanitizer.
2. Chạy toàn bộ test suite hiện có dưới trình biên dịch Clang/ASan để phát hiện lỗi ẩn.
3. Thay thế các con trỏ thô bằng `std::unique_ptr` và `std::span` (thay thế mảng C-style).
4. Rà soát việc khởi tạo biến để đảm bảo 100% biến được gán giá trị mặc định.
5. Tích hợp Clang-Tidy static analysis để cưỡng chế các quy tắc C++ Core Guidelines.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```cmake
# Cấu hình CMake kích hoạt Sanitizers trong chế độ Debug
set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -fsanitize=address,undefined -fno-omit-frame-pointer -g")
set(CMAKE_LINKER_FLAGS_DEBUG "${CMAKE_LINKER_FLAGS_DEBUG} -fsanitize=address,undefined")
```

```cpp
// Chuyển đổi mã nguồn C++ an toàn với RAII và smart pointers
#include <memory>
#include <span>
#include <vector>

class SecurePacketProcessor {
public:
    // Sử dụng std::span thay vì con trỏ thô kèm độ dài (Raw pointer + size)
    void process(std::span<const uint8_t> packetData) {
        if (packetData.empty()) return;
        // Tự động giải phóng bộ nhớ khi ra khỏi hàm
        auto buffer = std::make_unique<std::vector<uint8_t>>(packetData.begin(), packetData.end());
        parseHeader(*buffer);
    }
};
```

### Lệnh xác minh & thực thi:
```bash
# Build và chạy kiểm thử với Clang AddressSanitizer
cmake -B build -DCMAKE_BUILD_TYPE=Debug
cmake --build build
./build/bin/run_tests
```

## 8. Anti-Patterns & Common Traps
- Ép kiểu con trỏ bừa bãi bằng `reinterpret_cast` mà không kiểm tra quy tắc Strict Aliasing.
- Sử dụng mảng tĩnh C-style `char buffer[256]` kết hợp với các hàm nguy hiểm như `strcpy` hoặc `sprintf`.

## 9. Quality Gates & Acceptance Criteria
- 0 lỗi memory leak hoặc out-of-bounds nào được báo cáo bởi ASan/UBSan trên 100% test cases.
- Vượt qua kiểm tra của Clang-Tidy với bộ quy tắc C++ Core Guidelines.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Kích hoạt cờ bảo vệ Stack-Smashing (`-fstack-protector-strong`) và Control-Flow Integrity (CFI) trong bản release.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ thống hỗ trợ**: Cloud Runtimes (AWS Lambda, Cloudflare Workers, Kubernetes), Linux, Windows 11.

## 12. Deliverables & Output Artifacts
- File CMakeLists.txt tích hợp Sanitizers và Clang-Tidy.
- Báo cáo kết quả kiểm tra ASan sạch sẽ và mã nguồn C++ đã hiện đại hóa.

## 13. Related & Complementary Skills
dex-rust-unsafe-audit, dex-ffi-boundary-contracts, dex-reproducible-benchmarking

## 14. Realistic Usage Example
### Tình huống thực tế:
Một engine render đồ họa 3D bị sập bất thình lình khi người dùng mở các file mô hình phức tạp. Bằng cách kích hoạt Clang AddressSanitizer trong CI, nhóm kỹ sư phát hiện ngay lập tức một lỗi Use-After-Free trong cây phân nhánh vật liệu khi đối tượng con tham chiếu tới đối tượng cha đã bị hủy. Chuyển đổi sang `std::weak_ptr` đã giải quyết dứt điểm lỗi crash.
