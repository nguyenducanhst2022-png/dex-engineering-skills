---
name: dex-zig-build-engineering
description: Architect high-performance systems and C/C++ integrations using Zig build.zig pipelines, cross-compilation toolchains, and memory safety testing. Use when building native libraries, embedded systems, or zero-dependency CLI utilities.
---

# dex-zig-build-engineering

## 1. Purpose & Scope
Thiết kế và quản trị quy trình biên dịch hệ thống với Zig (`build.zig`); tận dụng khả năng biên dịch chéo (Cross-compilation) không phụ thuộc hạ tầng bên ngoài, tích hợp mã nguồn C/C++ trực tiếp vào pipeline của Zig, và kiểm soát an toàn bộ nhớ qua hệ thống kiểm thử tự động với bộ cấp phát phát hiện rò rỉ (GeneralPurposeAllocator).

## 2. When to Use
- Khi phát triển các công cụ dòng lệnh (CLI tools) hoặc thư viện hệ thống yêu cầu khởi động tức thì và nhị phân kích thước siêu nhỏ, không phụ thuộc libc động.
- Khi cần một công cụ biên dịch chéo C/C++ mạnh mẽ thay thế cho CMake/GCC phức tạp trên nhiều nền tảng (Linux musl/glibc, Windows x86_64, macOS aarch64).
- Khi xây dựng các module hiệu năng cao cần kiểm soát thủ công từng byte bộ nhớ nhưng có sự hỗ trợ của các cơ chế phát hiện lỗi bộ nhớ tại thời điểm kiểm thử.

## 3. When NOT to Use
- Khi ứng dụng là hệ thống doanh nghiệp cấp cao sử dụng garbage collector (như Java, C#, Go).
- Khi dự án đã có sẵn hạ tầng CMake ổn định và không có nhu cầu thay đổi công cụ build.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Mã nguồn Zig (`.zig`), tệp cấu hình `build.zig`, mã nguồn C/C++ tích hợp (nếu có), trình biên dịch Zig compiler.
- **Quyền hạn truy cập:** Quyền thực thi lệnh `zig` trên terminal.

## 5. Core Concepts & Taxonomy
- **`build.zig` as Code:** Toàn bộ quy trình build được viết bằng chính ngôn ngữ Zig, mang lại sức mạnh lập trình đầy đủ, kiểm tra kiểu tĩnh và không cần cú pháp DSL kỳ dị như Make hay CMake.
- **Out-of-the-Box Cross-Compilation:** Zig tích hợp sẵn trình biên dịch Clang và bộ thư viện musl/glibc cho hàng chục kiến trúc CPU; chỉ cần truyền cờ `-Dtarget=x86_64-linux-musl` là có thể biên dịch ra file binary độc lập.
- **`std.testing.allocator`:** Bộ cấp phát bộ nhớ dành riêng cho kiểm thử tự động phát hiện rò rỉ bộ nhớ (Memory Leak) và lỗi giải phóng hai lần (Double Free) ngay khi kết thúc bài test.

## 6. Step-by-Step Execution Workflow
1. Khởi tạo dự án Zig bằng lệnh `zig init` để tạo cấu trúc `src/main.zig` và `build.zig`.
2. Cấu hình các targets mục tiêu và chế độ tối ưu hóa (`ReleaseSafe`, `ReleaseFast`, `ReleaseSmall`) trong `build.zig`.
3. Nếu có tích hợp thư viện C: sử dụng `exe.addCSourceFile()` hoặc `exe.addIncludePath()` trực tiếp trong `build.zig`.
4. Viết các bài kiểm thử đơn vị sử dụng `std.testing.allocator` để bảo đảm mọi vùng nhớ xin cấp phát đều được giải phóng qua `defer allocator.free()`.
5. Thực hiện biên dịch chéo sang các nền tảng mục tiêu (Windows PE, Linux ELF static, macOS Mach-O).
6. Kiểm tra tính toàn vẹn của tệp nhị phân đầu ra: xác nhận không phụ thuộc vào thư viện động bên ngoài bằng lệnh `ldd` hoặc `dumpbin`.

## 7. Concrete Examples
### Ví dụ tệp cấu hình `build.zig` hỗ trợ biên dịch ứng dụng và chạy tests:
```zig
const std = @import("std");

pub fn build(b: *std.Build) void {
    const target = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});

    // 1. Định nghĩa tệp thực thi nhị phân chính
    const exe = b.addExecutable(.{
        .name = "dex-fast-indexer",
        .root_source_file = b.path("src/main.zig"),
        .target = target,
        .optimize = optimize,
    });
    b.installArtifact(exe);

    // 2. Định nghĩa bước chạy unit tests
    const unit_tests = b.addTest(.{
        .root_source_file = b.path("src/main.zig"),
        .target = target,
        .optimize = optimize,
    });
    const run_unit_tests = b.addRunArtifact(unit_tests);

    const test_step = b.step("test", "Run all unit tests with leak detection");
    test_step.dependOn(&run_unit_tests.step);
}
```

## 8. Anti-Patterns & Common Traps
- **Ignoring Allocation Errors:** Bỏ qua việc kiểm tra lỗi cấp phát bộ nhớ (out of memory) khi gọi `allocator.alloc()`.
- **Missing defer Deallocation:** Quên đặt lệnh `defer allocator.free(slice)` ngay sau khi cấp phát bộ nhớ gây rò rỉ RAM.
- **Hardcoding Host Paths in build.zig:** Đặt các đường dẫn tuyệt đối của máy chủ phát triển vào tệp build khiến người khác không thể biên dịch được dự án.

## 9. Quality Gates & Acceptance Criteria
- **QG-02**: Mã nguồn Zig biên dịch thành công không có cảnh báo nào ở chế độ `ReleaseSafe`.
- **QG-04**: 100% các bài test chạy qua `zig build test` đạt kết quả pass với 0 memory leaks được báo cáo.
- **QG-07**: Tệp binary phát hành ở chế độ `ReleaseSmall` có kích thước nhỏ gọn và khởi động dưới 10ms.

## 10. Security & Safety Boundaries
- Sử dụng chế độ `ReleaseSafe` trên các môi trường nhạy cảm để giữ lại các kiểm tra an toàn tràn số và truy cập mảng ngoài ranh giới.
- Kiểm toán mã nguồn C tích hợp kèm theo để ngăn ngừa các lỗ hổng bảo mật cổ điển (Buffer Overflow, Use-After-Free).

## 11. Platform Adapters
- **Compilers**: Zig Compiler (`zig build`, `zig cc`, `zig c++`).
- **C Integrations**: C ABI, Musl Libc, SQLite, zlib.

## 12. Deliverables & Output Artifacts
- Tệp cấu hình `build.zig` chuẩn hóa.
- Mã nguồn nhị phân hiệu năng cao viết bằng Zig.
- Báo cáo kiểm thử an toàn bộ nhớ không rò rỉ từ `std.testing.allocator`.

## 13. Related & Complementary Skills
dex-cpp-memory-safety, dex-pe-elf-structure-inspection, dex-cli-engineering

## 14. Realistic Usage Example
```powershell
# Chạy bộ kiểm thử tự động phát hiện rò rỉ bộ nhớ bằng Zig
zig build test

# Biên dịch chéo ra nhị phân độc lập tĩnh cho Linux x86_64
zig build -Dtarget=x86_64-linux-musl -Doptimize=ReleaseFast
```
