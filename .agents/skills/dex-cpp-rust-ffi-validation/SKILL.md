---
name: dex-cpp-rust-ffi-validation
description: Verify, test, and audit Foreign Function Interface (FFI) contracts between C++ and Rust. Validate memory layout alignment, ownership transfers, exception/panic firewalls, and sanitize with ASan/Miri.
---

# dex-cpp-rust-ffi-validation

## 1. Purpose & Scope
Kiểm chứng, kiểm toán an toàn và tối ưu hóa ranh giới tương tác liên ngôn ngữ (FFI - Foreign Function Interface) giữa C++ (C++20/C++23) và Rust; xác thực tính tương thích của bố cục bộ nhớ (`#[repr(C)]` vs `struct layout`), quyền sở hữu và chuyển giao con trỏ (Ownership & Lifetimes), cơ chế bắt ngoại lệ ngăn chặn Panic tràn qua ranh giới C-ABI (Panic Firewall), và kiểm thử tự động với AddressSanitizer (ASan), UndefinedBehaviorSanitizer (UBSan) và Miri.

## 2. When to Use
- Khi tích hợp các thư viện hiệu năng cao bằng C++ (như engine cờ vua, codec media, SIMD math) vào ứng dụng quản lý an toàn bằng Rust.
- Khi phát hiện các lỗi rò rỉ bộ nhớ bí ẩn (Memory Leaks), vi phạm vùng nhớ (Segfault) hoặc hỏng dữ liệu heap (Heap Corruption) tại tầng FFI.
- Khi định nghĩa các hàm trao đổi chuỗi ký tự UTF-8, mảng cắt lát (slices), hoặc đối tượng gọi ngược (callbacks) giữa hai ngôn ngữ.

## 3. When NOT to Use
- Khi hai dịch vụ giao tiếp với nhau qua mạng thông qua gRPC, REST hoặc Message Queue (IPC/RPC).
- Khi chương trình chỉ được viết hoàn toàn bằng một ngôn ngữ duy nhất mà không có thành phần native đa ngôn ngữ.

## 4. Prerequisites & Input Context
- **Trình biên dịch:** Rust 1.75+ (Cargo), Clang/GCC hỗ trợ C++20.
- **Công cụ hỗ trợ:** `cxx`, `bindgen`, AddressSanitizer (`-fsanitize=address`), và Miri.

## 5. Core Concepts & Taxonomy
- **#[repr(C)] Layout Alignment:** Thuộc tính bắt buộc trên các cấu trúc dữ liệu Rust để bảo đảm các trường dữ liệu được sắp xếp và đệm kích thước theo chuẩn ABI của C/C++.
- **Panic Firewall (catch_unwind):** Vùng đệm bắt toàn bộ panic trong Rust trước khi trả về C++, vì việc để một Rust panic lan truyền sang ngăn xếp C++ là hành vi Undefined Behavior (UB).
- **Opaque Pointers & Box Leak/From_raw:** Kỹ thuật chuyển giao quyền sở hữu con trỏ an toàn qua ranh giới FFI bằng cách cấp phát `Box::into_raw` và thu hồi bằng `Box::from_raw`.

## 6. Step-by-Step Execution Workflow
1. Khai báo các kiểu dữ liệu dùng chung với thuộc tính `#[repr(C)]` trong Rust và `struct` tương ứng trong C++.
2. Sử dụng thư viện `cxx` hoặc `bindgen` để sinh ra các hàm bao an toàn (Safe Wrapper Bridges).
3. Thiết lập Panic Firewall cho tất cả các hàm `extern "C"` phía Rust bằng `std::panic::catch_unwind`.
4. Định nghĩa rõ ràng quy ước giải phóng bộ nhớ: bên nào cấp phát (allocate) thì bên đó chịu trách nhiệm giải phóng (deallocate).
5. Biên dịch toàn bộ dự án với cờ AddressSanitizer (`-fsanitize=address`) trên Clang và `RUSTFLAGS="-Zsanitizer=address"`.
6. Chạy bộ kiểm thử FFI tự động kiểm tra ranh giới dữ liệu và khẳng định 0 lỗi bộ nhớ rò rỉ.

## 7. Concrete Examples
### Cau truc FFI an toan giua Rust va C++ co Panic Firewall va Repr(C):
```rust
// Rust implementation (lib.rs)
use std::ffi::{c_char, c_int, CStr};
use std::panic::catch_unwind;

#[repr(C)]
pub struct EngineMetrics {
    pub nodes_searched: u64,
    pub nps: u32,
    pub depth: u8,
}

#[no_mangle]
pub extern "C" fn rust_compute_eval(fen: *const c_char, out_metrics: *mut EngineMetrics) -> c_int {
    // Panic Firewall: Ngan khong cho panic thoat ra C ABI
    let result = catch_unwind(|| {
        if fen.is_null() || out_metrics.is_null() {
            return -1; // Loi con tro null
        }
        let c_str = unsafe { CStr::from_ptr(fen) };
        let fen_str = match c_str.to_str() {
            Ok(s) => s,
            Err(_) => return -2, // Loi ma hoa UTF-8
        };

        // Gia lap tinh toan an toan
        unsafe {
            (*out_metrics).nodes_searched = 1_500_000;
            (*out_metrics).nps = 2_500_000;
            (*out_metrics).depth = 18;
        }
        0 // Thanh cong
    });

    result.unwrap_or(-99) // Tra ma loi neu xay ra panic
}
```

```cpp
// C++ consumer (main.cpp)
#include <iostream>
#include <cstdint>

extern "C" {
    struct EngineMetrics {
        uint64_t nodes_searched;
        uint32_t nps;
        uint8_t depth;
    };

    int rust_compute_eval(const char* fen, EngineMetrics* out_metrics);
}

int main() {
    EngineMetrics metrics{};
    int status = rust_compute_eval("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", &metrics);
    if (status == 0) {
        std::cout << "Success! Depth: " << (int)metrics.depth << ", NPS: " << metrics.nps << "\n";
    }
    return status;
}
```

## 8. Anti-Patterns & Common Traps
- **Uncaught Panic over FFI Boundary:** Để xảy ra `panic!` bên trong hàm `extern "C"` làm sập toàn bộ tiến trình hoặc làm rách nát stack frame của C++.
- **Mismatched Allocator Deallocation:** Cấp phát bộ nhớ bằng `malloc` trong C++ nhưng lại giải phóng bằng `Box::from_raw` trong Rust (hoặc ngược lại) gây sập Heap Manager.
- **Passing Raw Non-repr(C) Structs:** Truyền các cấu trúc dữ liệu Rust mặc định (không có `#[repr(C)]`) sang C++ dẫn đến việc đọc sai lệch offset dữ liệu do trình biên dịch tự ý sắp xếp lại thứ tự trường.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: 100% các hàm FFI đều có `catch_unwind` hoặc `noexcept` bảo đảm không phát tán ngoại lệ xuyên biên giới.
- **QG-02**: Vượt qua bộ kiểm thử kiểm tra bộ nhớ AddressSanitizer (ASan) với 0 byte memory leak.
- **QG-03**: Kích thước và căn chỉnh byte (`sizeof` và `alignof`) của các struct dùng chung khớp nhau 100% giữa C++ và Rust.

## 10. Security & Safety Boundaries
- Luôn kiểm tra con trỏ `null` và tính hợp lệ của chuỗi ký tự UTF-8 trước khi thực hiện các thao tác trong khối `unsafe`.

## 11. Platform Adapters
- **Runtimes**: C++20 (Clang/GCC), Rust 2021 (Cargo), cxx crate, bindgen, LLVM ASan/UBSan.

## 12. Deliverables & Output Artifacts
- Tệp tiêu đề C-ABI dùng chung (`engine_bridge.h` / `bridge.rs`).
- Bộ kiểm thử tự động kiểm tra tính an toàn bộ nhớ FFI (`test_ffi_sanitizers.sh`).

## 13. Related & Complementary Skills
dex-chess-legal-movegen-perft, dex-native-simd-dispatch, dex-chess-nnue-evaluation-integration

## 14. Realistic Usage Example
```bash
# Chay kiem thu FFI co bat AddressSanitizer
clang++ -fsanitize=address -std=c++20 main.cpp -L./target/debug -lengine_rust -o ffi_test && ./ffi_test
```
