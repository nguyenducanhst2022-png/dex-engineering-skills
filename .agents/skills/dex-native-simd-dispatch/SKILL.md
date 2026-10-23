---
name: dex-native-simd-dispatch
description: Detect, benchmark, and implement portable runtime SIMD CPU dispatch (AVX2, AVX-512, ARM Neon). Ensure robust scalar fallbacks, vector alignment, and multiversioned execution paths.
---

# dex-native-simd-dispatch

## 1. Purpose & Scope
Thiết kế và triển khai cơ chế điều phối lệnh vector hóa thời gian thực (Portable Runtime SIMD Dispatch); tự động nhận diện tập lệnh phần cứng của CPU (x86-64 AVX2, AVX-512, SSE4.2 và ARM64 Neon); xây dựng cơ chế phân nhánh đa phiên bản (Function Multiversioning / Dynamic Function Pointer Dispatch) và duy trì đường dự phòng vô hướng (Scalar Fallback) đảm bảo tính tương thích phần mềm 100% trên mọi kiến trúc CPU.

## 2. When to Use
- Khi viết các thuật toán tính toán ma trận, xử lý tín hiệu âm thanh/hình ảnh hoặc hàm đánh giá NNUE đòi hỏi băng thông tính toán cực đại.
- Khi phần mềm được phân phối dưới dạng tệp nhị phân duy nhất (Universal Binary) nhưng phải chạy tối ưu trên cả máy tính đời mới lẫn máy tính đời cũ.
- Khi gặp lỗi sập chương trình với mã `SIGILL` (Illegal Instruction) trên các máy tính người dùng không có tập lệnh AVX2.

## 3. When NOT to Use
- Khi khối lượng tính toán là các tác vụ I/O mạng hoặc truy vấn cơ sở dữ liệu bị nghẽn bởi tốc độ đọc ghi đĩa.
- Khi trình biên dịch tự động vector hóa (Auto-vectorization) đã đạt hiệu quả tối ưu mà không cần can thiệp mã lắp ráp nội tại (Intrinsics).

## 4. Prerequisites & Input Context
- **Trình biên dịch:** Hỗ trợ C++20/Rust và các hàm nội tại SIMD (`<immintrin.h>` hoặc `core::arch`).
- **Môi trường đo kiểm:** CPU hỗ trợ tối thiểu tập lệnh cơ sở SSE4.2 kèm các tập lệnh mở rộng AVX2.

## 5. Core Concepts & Taxonomy
- **CPUID Instruction:** Lệnh phần cứng x86 cho phép truy vấn trực tiếp các tính năng được hỗ trợ bởi bộ vi xử lý tại thời điểm khởi động ứng dụng.
- **Dynamic Function Pointer Dispatch:** Kỹ thuật gán con trỏ hàm toàn cục một lần duy nhất khi khởi động chương trình trỏ tới phiên bản SIMD tối ưu nhất mà CPU hỗ trợ.
- **Vector Register Alignment:** Yêu cầu địa chỉ bộ nhớ phải là bội số của 16, 32 hoặc 64 byte để nạp dữ liệu bằng các lệnh vector không căn chỉnh (unaligned) hoặc căn chỉnh (aligned) với hiệu năng tối đa.

## 6. Step-by-Step Execution Workflow
1. Viết hàm kiểm tra CPUID phát hiện cờ hỗ trợ phần cứng: AVX2, FMA, AVX-512F, AVX-512BW, Neon.
2. Cài đặt thuật toán theo 3 phiên bản độc lập: Phiên bản chuẩn vô hướng (Scalar), phiên bản AVX2 (256-bit), và phiên bản AVX-512 (512-bit).
3. Định nghĩa con trỏ hàm: `typedef void (*compute_fn)(const float* in, float* out, size_t n);`.
4. Viết hàm khởi tạo hàm điều phối (Dispatch Resolver) thiết lập con trỏ hàm chính xác trước khi ứng dụng thực thi vòng lặp chính.
5. Thực hiện đo kiểm hiệu năng (Micro-benchmarking) so sánh tốc độ tăng tốc giữa các phiên bản.
6. Kiểm chứng đường fallback vô hướng bằng cách giả lập tắt cờ CPUID trong môi trường ảo hóa.

## 7. Concrete Examples
### Thuat toan Runtime CPU Dispatch cho phep tinh toan Vector tren C++20:
```cpp
#include <iostream>
#include <vector>
#include <immintrin.h>

#if defined(_MSC_VER)
#include <intrin.h>
#else
#include <cpuid.h>
#endif

// 1. Kiem tra CPUID thoi diem runtime
bool cpu_supports_avx2() {
#if defined(_MSC_VER)
    int info[4];
    __cpuidex(info, 7, 0);
    return (info[1] & (1 << 5)) != 0;
#else
    unsigned int eax, ebx, ecx, edx;
    if (__get_cpuid_max(0, nullptr) < 7) return false;
    __cpuid_count(7, 0, eax, ebx, ecx, edx);
    return (ebx & (1 << 5)) != 0;
#endif
}

// 2. Phien ban Scalar Fallback
void dot_product_scalar(const float* a, const float* b, float* result, size_t n) {
    float sum = 0.0f;
    for (size_t i = 0; i < n; ++i) sum += a[i] * b[i];
    *result = sum;
}

// 3. Phien ban AVX2 (256-bit)
void dot_product_avx2(const float* a, const float* b, float* result, size_t n) {
    __m256 sum_vec = _mm256_setzero_ps();
    size_t i = 0;
    for (; i + 8 <= n; i += 8) {
        __m256 va = _mm256_loadu_ps(&a[i]);
        __m256 vb = _mm256_loadu_ps(&b[i]);
        sum_vec = _mm256_fmadd_ps(va, vb, sum_vec);
    }
    // Horizontal add
    alignas(32) float buffer[8];
    _mm256_store_ps(buffer, sum_vec);
    float total = 0.0f;
    for (int k = 0; k < 8; ++k) total += buffer[k];
    
    // Xu ly phan du con lai
    for (; i < n; ++i) total += a[i] * b[i];
    *result = total;
}

// 4. Function Pointer Dispatch
using DotProductFn = void (*)(const float*, const float*, float*, size_t);

DotProductFn resolve_dot_product() {
    if (cpu_supports_avx2()) {
        std::cout << "[SIMD] Selected AVX2 hardware acceleration.\n";
        return dot_product_avx2;
    }
    std::cout << "[SIMD] Fallback to Portable Scalar implementation.\n";
    return dot_product_scalar;
}

DotProductFn dot_product = resolve_dot_product();
```

## 8. Anti-Patterns & Common Traps
- **Compiling with Global -mavx2 Flag:** Biên dịch toàn bộ dự án với cờ `-mavx2` khiến ngay cả mã khởi động hoặc hàm `main` cũng chứa lệnh AVX2, gây crash lập tức trên CPU cũ trước khi kịp chạy hàm kiểm tra CPUID.
- **Ignoring Remainder Elements:** Quên xử lý các phần tử thừa ở cuối mảng khi kích thước mảng không chia hết cho kích thước vector (8 đối với AVX, 16 đối với AVX-512).
- **Misaligned Store Crashes:** Dùng lệnh nạp yêu cầu căn chỉnh `_mm256_load_ps` trên con trỏ bộ nhớ ngẫu nhiên chưa được kiểm tra địa chỉ chia hết cho 32 byte.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Kết quả tính toán giữa phiên bản SIMD và phiên bản Scalar fallback trùng khớp với sai số epsilon < 1e-5.
- **QG-02**: Ứng dụng khởi động an toàn và chuyển về đường fallback trên môi trường giả lập không có AVX2 (0 lỗi `SIGILL`).
- **QG-03**: Phiên bản AVX2 đạt tốc độ tăng tốc tối thiểu 3.5x so với phiên bản Scalar trên các tập dữ liệu lớn.

## 10. Security & Safety Boundaries
- Ngăn ngừa lỗi đọc vượt biên (Buffer Over-read) ở các phần tử cuối mảng trong các phép toán vector.

## 11. Platform Adapters
- **Runtimes**: C++20 (GCC, Clang, MSVC), Rust (std::arch, is_x86_feature_detected!), ARM Neon.

## 12. Deliverables & Output Artifacts
- Thư viện điều phối SIMD đa nền tảng (`simd_dispatch.hpp` / `simd.rs`).
- Bộ benchmark đo lường thông lượng tính toán giữa các tập lệnh.

## 13. Related & Complementary Skills
dex-chess-nnue-evaluation-integration, dex-cpp-rust-ffi-validation

## 14. Realistic Usage Example
```bash
# Chay benchmark so sanh toc do cac tap lenh SIMD
./simd_benchmark --iterations 1000000 --size 65536
```
