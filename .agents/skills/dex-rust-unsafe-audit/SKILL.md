---
name: dex-rust-unsafe-audit
description: Audit, verify, and minimize 'unsafe' code blocks in Rust, validating ownership invariants, raw pointer arithmetic, FFI boundaries, and undefined behavior using Miri and Loom. Use when building high-assurance systems.
---

# dex-rust-unsafe-audit

## 1. Purpose & Scope
Kiểm toán, thẩm định và tối thiểu hóa các khối mã nguồn không an toàn (`unsafe`) trong Rust; xác minh các bất biến về quyền sở hữu (Ownership Invariants), số học con trỏ thô (Raw Pointers), ranh giới FFI và triệt tiêu các hành vi không xác định (Undefined Behavior - UB) bằng các công cụ chuyên sâu như Miri và Loom.

## 2. When to Use
- Viết hoặc review các thư viện cốt lõi (Crates) có chứa từ khóa `unsafe`.
- Xây dựng các cấu trúc dữ liệu tùy chỉnh hiệu năng cao (Lock-free data structures, Ring buffers).
- Tích hợp giao tiếp FFI với các thư viện viết bằng C/C++.

## 3. When NOT to Use
- Không sử dụng `unsafe` nếu bài toán có thể giải quyết được bằng các cấu trúc an toàn có sẵn trong thư viện chuẩn (Safe Rust) với chi phí hiệu năng không đáng kể.
- Không dùng `unsafe` chỉ để 'lách luật' kiểm tra của Borrow Checker.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Mã nguồn Rust chứa các khối `unsafe`.
- Tài liệu đặc tả các điều kiện bất biến an toàn (Safety Invariants) của hàm.
- Bộ test cases kiểm thử các trường hợp biên.
- **Điều kiện tiên quyết**:
- Đã cài đặt Rust Nightly toolchain để chạy trình thông dịch Miri (`cargo miri`).

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Soundness vs Safety: Một hàm `unsafe fn` yêu cầu người gọi phải tự đảm bảo an toàn. Một hàm safe bọc ngoài unsafe code (Safe Abstraction) phải là 'sound' — nghĩa là bất kể tham số đầu vào là gì cũng không bao giờ kích hoạt Undefined Behavior.
- Undefined Behavior (UB) trong Rust: Vi phạm quy tắc Aliasing (hai con trỏ cùng trỏ tới một vùng nhớ và ít nhất một con trỏ có quyền ghi `&mut`), Đọc bộ nhớ chưa khởi tạo, Dereference con trỏ null hoặc dangling.
- Miri: Công cụ thông dịch mã trung gian (MIR) của Rust, có khả năng phát hiện 100% các lỗi vi phạm quy tắc aliasing (Stacked Borrows / Tree Borrows) khi runtime.
- **Quy tắc quyết định kỹ thuật**:
- Mọi khối `unsafe` bắt buộc phải có chú thích `// SAFETY:` giải thích chi tiết lý do tại sao đoạn code này không vi phạm bất biến an toàn.
- Giới hạn phạm vi của khối `unsafe` ở mức tối thiểu (chỉ bọc đúng 1-2 dòng cần thiết).
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Tạo một tham chiếu khả biến `&mut T` từ một con trỏ thô trong khi một tham chiếu bất biến `&T` khác vẫn đang tồn tại, vi phạm quy tắc aliasing và bị compiler tối ưu hóa sai.

## 6. Step-by-Step Execution Workflow
1. Quét tìm toàn bộ các vị trí sử dụng `unsafe` bằng công cụ `cargo geiger`.
2. Rà soát từng khối `unsafe`, kiểm tra xem có thể thay thế bằng safe code không.
3. Thêm tài liệu `// SAFETY:` bắt buộc cho từng khối.
4. Thực thi test suite dưới trình kiểm tra Undefined Behavior của Miri.
5. Kiểm tra các điều kiện Race condition đa luồng bằng thư viện Loom.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```rust
pub struct BoundedBuffer<T> {
    ptr: *mut T,
    capacity: usize,
}

impl<T> BoundedBuffer<T> {
    pub fn read_at(&self, index: usize) -> Option<&T> {
        if index >= self.capacity {
            return None;
        }
        // SAFETY: Chúng ta đã kiểm tra index < capacity,
        // con trỏ đã được cấp phát hợp lệ và không có luồng nào đang ghi vào index này.
        unsafe {
            Some(&*self.ptr.add(index))
        }
    }
}
```

### Lệnh xác minh & thực thi:
```bash
# Kiểm tra Undefined Behavior bằng Miri trong môi trường Rust Nightly
cargo +nightly miri test
# Quét thống kê tỉ lệ unsafe code trong project
cargo geiger
```

## 8. Anti-Patterns & Common Traps
- Viết `unsafe` mà không có comment `// SAFETY:` giải thích căn cứ kỹ thuật.
- Ép kiểu con trỏ tùy tiện làm sai lệch memory alignment của kiểu dữ liệu.

## 9. Quality Gates & Acceptance Criteria
- 100% test cases phải PASS hoàn toàn dưới `cargo miri test` mà không có cảnh báo UB nào.
- 0 khối unsafe nào không có phần giải trình `// SAFETY:`.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Mọi hàm expose ra ngoài public API bắt buộc phải là Safe Function hoặc được đánh dấu rõ ràng `pub unsafe fn`.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ thống hỗ trợ**: Cloud Runtimes (AWS Lambda, Cloudflare Workers, Kubernetes), Linux, Windows 11.

## 12. Deliverables & Output Artifacts
- Báo cáo kiểm toán `cargo geiger`.
- Mã nguồn Rust đã được thẩm định an toàn kèm chú thích `// SAFETY:` chuẩn chỉ.

## 13. Related & Complementary Skills
dex-cpp-memory-safety, dex-ffi-boundary-contracts, dex-reproducible-benchmarking

## 14. Realistic Usage Example
### Tình huống thực tế:
Một công ty blockchain viết cấu trúc lưu trữ trạng thái bằng Rust dùng unsafe pointer để tối ưu tốc độ. Khi chạy dưới `cargo miri test`, họ bàng hoàng phát hiện hàm giải phóng bộ nhớ vi phạm quy tắc Stacked Borrows làm phát sinh Undefined Behavior tiềm ẩn. Họ đã tái cấu trúc lại an toàn bằng `std::mem::ManuallyDrop` và bảo vệ thành công tài sản người dùng.
