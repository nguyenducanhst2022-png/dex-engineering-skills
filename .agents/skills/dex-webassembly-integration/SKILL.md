---
name: dex-webassembly-integration
description: Compile, integrate, and optimize WebAssembly (WASM) modules across browser and server runtimes (Wasmtime, Wasmer), managing linear memory, FFI boundary overhead, and sandbox security. Use when running near-native compute in web or edge environments.
---

# dex-webassembly-integration

## 1. Purpose & Scope
Thiết kế, biên dịch, tích hợp và tối ưu hóa các module WebAssembly (WASM: Rust/C++ sang WebAssembly) trên môi trường trình duyệt web và máy chủ (Wasmtime, Wasmer); quản lý vùng nhớ tuyến tính (Linear Memory), tối ưu hóa chi phí vượt ranh giới giao tiếp (FFI Boundary Overhead), và thiết lập môi trường sandbox an toàn cho phép thực thi mã nguồn tính toán phức tạp.

## 2. When to Use
- Cần mang các thuật toán tính toán nặng (xử lý đồ họa, nén/giải nén video, mã hóa mật mã học, AI inference cục bộ) chạy mượt mà trên trình duyệt web.
- Xây dựng hệ thống Plugin cho phép người dùng chạy code mở rộng trong môi trường cô lập an toàn trên máy chủ.
- Tái sử dụng thư viện C++/Rust có sẵn trong dự án web/Node.js.

## 3. When NOT to Use
- Không dùng WebAssembly cho các thao tác thao tác DOM đơn giản hoặc CRUD thông thường (chi phí FFI giữa JS và WASM sẽ làm ứng dụng chậm hơn JS thuần).
- Không dùng WASM cho các ứng dụng yêu cầu truy cập trực tiếp vào phần cứng hoặc hệ thống file không thông qua WASI.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Mã nguồn ngôn ngữ gốc (Rust với `wasm-bindgen` hoặc C++ với Emscripten).
- Giao diện kết nối JavaScript/TypeScript (Bindings).
- Module WASM đã được biên dịch (`.wasm`).
- **Điều kiện tiên quyết**:
- Đã cài đặt `wasm-pack` (cho Rust) hoặc Emscripten SDK (cho C++).

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Linear Memory: Vùng nhớ của module WASM là một mảng byte liên tục (`ArrayBuffer`). Việc truyền dữ liệu lớn giữa JS và WASM nên được thực hiện bằng cách chia sẻ con trỏ trên linear memory thay vì copy chuỗi.
- WASI (WebAssembly System Interface): Giao diện chuẩn mực cho phép module WASM chạy ngoài trình duyệt trên máy chủ (Server-side WASM) có thể truy cập file, network an toàn.
- FFI Overhead: Lời gọi hàm giữa JavaScript và WebAssembly có độ trễ nhất định. Cần gom nhóm các thao tác (Batch processing) thay vì gọi hàng triệu lần qua lại ranh giới.
- **Quy tắc quyết định kỹ thuật**:
- Nếu truyền dữ liệu lớn (ảnh/video > 1MB): truyền con trỏ và kích thước bộ nhớ, thao tác trực tiếp trên `Uint8Array` của WASM Memory.
- Bắt buộc chạy công cụ tối ưu hóa `wasm-opt -O3` để giảm kích thước file WASM trước khi phân phối.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Cấp phát bộ nhớ trong WASM từ JavaScript nhưng quên gọi hàm giải phóng của module gốc, gây rò rỉ bộ nhớ nghiêm trọng trên trình duyệt.

## 6. Step-by-Step Execution Workflow
1. Viết logic tính toán lõi bằng Rust và định nghĩa các API export bằng `#[wasm_bindgen]`.
2. Biên dịch mã nguồn sang file `.wasm` tối ưu bằng lệnh `wasm-pack build --target web`.
3. Tối ưu kích thước file bằng công cụ `wasm-opt` (giảm tới 40% dung lượng).
4. Tích hợp module WASM vào ứng dụng Frontend/Node.js thông qua luồng nạp bất đồng bộ (`WebAssembly.instantiateStreaming`).
5. Xây dựng các bài benchmark so sánh hiệu năng trực tiếp với JavaScript.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```rust
// Rust: Mã nguồn thuật toán xử lý ảnh biên dịch sang WebAssembly
use wasm_bindgen::prelude::*;

#[wasm_bindgen]
pub fn apply_grayscale(image_data: &mut [u8]) {
    // Lặp qua các pixel (R, G, B, A) và tính độ xám trực tiếp trên linear memory
    for chunk in image_data.chunks_exact_mut(4) {
        let gray = (0.299 * chunk[0] as f32 + 0.587 * chunk[1] as f32 + 0.114 * chunk[2] as f32) as u8;
        chunk[0] = gray;
        chunk[1] = gray;
        chunk[2] = gray;
    }
}
```

### Lệnh xác minh & thực thi:
```bash
# Biên dịch và tối ưu hóa module Rust sang WASM
wasm-pack build --target web --release
wasm-opt -O3 pkg/image_filter_bg.wasm -o pkg/image_filter_bg.wasm
```

## 8. Anti-Patterns & Common Traps
- Gọi hàm WASM bên trong một vòng lặp JS hàng triệu lần (gây nghẽn FFI).
- Nạp file WASM lớn đồng bộ làm đơ luồng giao diện của người dùng (bắt buộc dùng `instantiateStreaming` và Web Workers).

## 9. Quality Gates & Acceptance Criteria
- Dung lượng file `.wasm` sau khi nén Gzip/Brotli phải dưới 200KB cho các module frontend.
- Hiệu năng xử lý thuật toán phải nhanh hơn JavaScript tối thiểu gấp 2 lần.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Module WASM không được phép có quyền truy cập trực tiếp vào DOM hoặc Cookies của người dùng nếu không qua sandbox proxy.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ thống hỗ trợ**: Cloud Runtimes (AWS Lambda, Cloudflare Workers, Kubernetes), Linux, Windows 11.

## 12. Deliverables & Output Artifacts
- Module WebAssembly (`.wasm`) và JavaScript bindings (`.js`, `.d.ts`).
- Bộ test suite tích hợp và benchmark so sánh hiệu năng.

## 13. Related & Complementary Skills
dex-ffi-boundary-contracts, dex-reproducible-benchmarking, dex-frontend-data-flow

## 14. Realistic Usage Example
### Tình huống thực tế:
Một ứng dụng chỉnh sửa ảnh trực tuyến gặp khó khăn khi bộ lọc làm mịn da viết bằng JavaScript mất 1,800ms cho mỗi bức ảnh 4K. Chuyển đổi thuật toán sang Rust và biên dịch sang WebAssembly chạy trong Web Worker, thời gian xử lý giảm xuống còn 140ms, mang lại trải nghiệm mượt mà thời gian thực cho người dùng.
