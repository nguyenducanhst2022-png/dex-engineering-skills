---
name: dex-ffi-boundary-contracts
description: Design, document, and validate robust Foreign Function Interface (FFI) boundaries (C ABI) across languages, ensuring memory ownership contracts, alignment, and error translation. Use when binding native code across language ecosystems.
---

# dex-ffi-boundary-contracts

## 1. Purpose & Scope
Thiết kế, đặc tả tài liệu và kiểm chứng các hợp đồng ranh giới giao tiếp đa ngôn ngữ (Foreign Function Interface - FFI Contracts: C ABI); bảo đảm tính toàn vẹn về quyền sở hữu bộ nhớ (Memory Ownership Contracts), căn chỉnh dữ liệu (Data Alignment/Padding), lan truyền mã lỗi an toàn và chống sập tiến trình khi truyền dữ liệu giữa các hệ sinh thái ngôn ngữ khác nhau (Node.js/Python/Go kết nối với C/Rust/C++).

## 2. When to Use
- Viết Native Extensions cho Node.js (Node-API / N-API) hoặc Python (CFFI / PyO3 / ctypes).
- Tích hợp một thư viện mã nguồn gốc (C/C++ shared library `.so`/`.dll`) vào ứng dụng cấp cao.
- Xảy ra lỗi crash tiến trình bí ẩn hoặc hỏng dữ liệu (Memory Corruption) tại điểm giao tiếp giữa hai ngôn ngữ.

## 3. When NOT to Use
- Không sử dụng FFI nếu hai dịch vụ có thể giao tiếp hiệu quả qua các giao thức mạng nội bộ (gRPC / Unix Domain Sockets) mà không cần chung tiến trình.
- Không để các ngoại lệ (C++ Exceptions / Rust Panics) thoát ra ngoài ranh giới C ABI (dẫn đến Undefined Behavior và crash ngay lập tức).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Header file C (`.h`) đặc tả C ABI.
- Mã nguồn Native implementation và mã nguồn Caller wrapper.
- Định nghĩa cấu trúc dữ liệu (`struct`) ở cả hai phía.
- **Điều kiện tiên quyết**:
- Cả hai phía đều thống nhất tuân thủ chuẩn gọi hàm C calling convention (`extern "C"`, `__cdecl` hoặc `__stdcall`).

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- The C ABI as Lingua Franca: Chuẩn giao tiếp nhị phân C (C Application Binary Interface) là mẫu số chung duy nhất mà mọi ngôn ngữ lập trình đều hiểu và tương thích.
- Ownership Rule of Thumb: 'Bên nào cấp phát (Allocate) thì bên đó phải giải phóng (Deallocate)'. Tuyệt đối không để phía Python/JS tự ý free một con trỏ được cấp phát bởi thư viện C/Rust mà không thông qua hàm deallocator chính thức của thư viện đó.
- Panic / Exception Boundary: Ngoại lệ không bao giờ được bay qua ranh giới FFI. Mọi lỗi phải được bắt lại và chuyển thành mã số lỗi nguyên thủy (Error Code) hoặc cấu trúc kết quả.
- **Quy tắc quyết định kỹ thuật**:
- Bắt buộc đánh dấu cấu trúc dữ liệu dùng chung bằng thuộc tính `#[repr(C)]` trong Rust hoặc `#pragma pack` trong C để đảm bảo thứ tự và padding của các trường byte khớp nhau 100%.
- Mọi hàm FFI phải trả về `int32_t` mã lỗi hoặc `struct FfiResult` rõ ràng.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Cấu trúc struct ở phía C có padding 4 bytes nhưng phía Python ctypes không khai báo padding, khiến các giá trị đọc được bị lệch byte và làm sai lệch toàn bộ dữ liệu.

## 6. Step-by-Step Execution Workflow
1. Định nghĩa file C Header `.h` chuẩn mực chứa các hàm `extern "C"` và struct `#[repr(C)]`.
2. Viết mã nguồn thư viện gốc, bọc toàn bộ code trong khối `catch-all` để ngăn chặn panic/exception.
3. Cung cấp hàm giải phóng bộ nhớ đi kèm (ví dụ: `free_my_buffer(void* ptr)`).
4. Viết wrapper an toàn (Safe Wrapper) ở ngôn ngữ gọi (Python/Node.js) sử dụng RAII/Destructor để tự động gọi hàm free.
5. Xây dựng test suite kiểm tra rò rỉ bộ nhớ tại ranh giới FFI bằng Valgrind hoặc ASan.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```rust
// Rust: Định nghĩa C ABI an toàn cho thư viện native chia sẻ
#[repr(C)]
pub struct CalculationResult {
    pub value: f64,
    pub error_code: i32,
}

#[no_mangle]
pub extern "C" fn calculate_risk(input_ptr: *const f64, length: usize) -> CalculationResult {
    // Bắt toàn bộ panic không cho thoát ra ngoài C ABI
    std::panic::catch_unwind(|| {
        if input_ptr.is_null() {
            return CalculationResult { value: 0.0, error_code: -1 };
        }
        let slice = unsafe { std::slice::from_raw_parts(input_ptr, length) };
        let sum: f64 = slice.iter().sum();
        CalculationResult { value: sum * 1.5, error_code: 0 }
    }).unwrap_or(CalculationResult { value: 0.0, error_code: -99 })
}
```

### Lệnh xác minh & thực thi:
```bash
# Kiểm tra danh sách exported symbols của file thư viện nhị phân
nm -D target/release/libmymath.so | grep calculate_risk
```

## 8. Anti-Patterns & Common Traps
- Để Rust panic hoặc C++ exception văng trực tiếp qua ranh giới C ABI.
- Giải phóng vùng nhớ của chuỗi bằng hàm `free()` của C trong khi chuỗi được cấp phát bởi Go runtime.

## 9. Quality Gates & Acceptance Criteria
- 100% structs dùng qua FFI đều có khai báo `repr(C)` và căn chỉnh padding chuẩn xác.
- Không có bất kỳ rò rỉ bộ nhớ nào tại ranh giới FFI sau 1,000,000 lượt gọi lặp lại.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Kiểm tra con trỏ Null (`is_null()`) và kiểm tra kích thước bộ đệm (Buffer size bounds) trước khi đọc dữ liệu từ phía caller.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ thống hỗ trợ**: Cloud Runtimes (AWS Lambda, Cloudflare Workers, Kubernetes), Linux, Windows 11.

## 12. Deliverables & Output Artifacts
- File C header `.h` và mã nguồn native exports.
- Safe binding wrapper module cho ngôn ngữ cấp cao (Python/TypeScript).

## 13. Related & Complementary Skills
dex-rust-unsafe-audit, dex-webassembly-integration, dex-cpp-memory-safety

## 14. Realistic Usage Example
### Tình huống thực tế:
Một ứng dụng Python AI cần gọi thuật toán giải mã vector viết bằng C++. Ban đầu, ứng dụng hay bị crash ngẫu nhiên do C++ ném ngoại lệ khi dữ liệu hỏng. Sau khi thiết lập hợp đồng FFI chuẩn với `#[repr(C)]`, bọc ngoại lệ thành mã lỗi và xây dựng safe wrapper bằng `ctypes`, hệ thống hoạt động ổn định 100% và tăng tốc độ xử lý lên 40 lần so với Python thuần.
