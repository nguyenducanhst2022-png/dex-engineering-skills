---
name: dex-toolchain-reproducibility-audit
description: Audit build environments, toolchain configurations, timestamp non-determinism, and compilation flags to achieve bit-for-bit reproducible builds. Use when certifying supply chain integrity and eliminating compiler backdoors.
---

# dex-toolchain-reproducibility-audit

## 1. Purpose & Scope
Kiểm toán môi trường build, cấu hình toolchain, các yếu tố bất định (timestamps, thứ tự file, biến môi trường) và cờ biên dịch để đạt được khả năng tái tạo bản dựng chuẩn xác đến từng bit (Bit-for-Bit Reproducible Builds); loại trừ nguy cơ chèn mã độc ẩn từ compiler.

## 2. When to Use
- Khi chứng nhận an ninh chuỗi cung ứng cho các phần mềm quan trọng (hệ điều hành, ví tiền mã hóa, firmware).
- Khi hai kỹ sư biên dịch cùng một commit git nhưng sinh ra hai file nhị phân có mã băm SHA-256 khác nhau.
- Khi xây dựng quy trình kiểm toán độc lập cho phép bên thứ ba tự biên dịch và kiểm chứng artifact.

## 3. When NOT to Use
- Khi đang trong giai đoạn phát triển tính năng cục bộ (local prototyping) cần tốc độ lặp nhanh mà không quan tâm đến mã băm bản dựng.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Mã nguồn dự án, build scripts (Makefile, CMakeLists.txt, Cargo.toml), môi trường build container hóa.
- **Quyền hạn truy cập:** Quyền chạy quy trình build lặp lại trong môi trường cô lập.

## 5. Core Concepts & Taxonomy
- **Reproducible Builds:** Khả năng tạo ra các file nhị phân giống hệt nhau từng byte khi biên dịch từ cùng một mã nguồn trong cùng điều kiện toolchain.
- **SOURCE_DATE_EPOCH:** Tiêu chuẩn biến môi trường quy định mốc thời gian cố định thay cho thời gian thực của hệ thống khi đóng gói file.
- **Diffoscope:** Công cụ phân tích sâu sự khác biệt giữa hai gói nhị phân (archive, executable, container image).

## 6. Step-by-Step Execution Workflow
1. Thực hiện biên dịch bản dựng lần 1 trong môi trường A (ghi lại mã băm SHA-256).
2. Thực hiện biên dịch bản dựng lần 2 trong môi trường B có các biến thể có chủ đích (thay đổi múi giờ, tên thư mục, user build).
3. So sánh mã băm của hai artifact đầu ra; nếu khác biệt, sử dụng `diffoscope` để khoanh vùng nguyên nhân.
4. Khắc phục các nguồn gây bất định: cố định `SOURCE_DATE_EPOCH`, sắp xếp thứ tự file alphabet trước khi nén, loại bỏ macro `__DATE__` và `__TIME__`.
5. Cấu hình cờ biên dịch chuẩn hóa đường dẫn (ví dụ: `-ffile-prefix-map` trong GCC/Clang, `--remap-path-prefix` trong Rust).
6. Đóng gói môi trường build vào container không trạng thái và ban hành hướng dẫn tái tạo độc lập.

## 7. Concrete Examples
### Thiết lập cờ chuẩn hóa đường dẫn và thời gian cố định:
```bash
# Thiết lập biến môi trường chuẩn hóa thời gian
export SOURCE_DATE_EPOCH=$(git log -1 --pretty=%ct)

# Cờ biên dịch GCC / Clang triệt tiêu bất định về đường dẫn và macro thời gian
export CFLAGS="-ffile-prefix-map=$(pwd)=. -Wno-builtin-macro-redefined -D__DATE__=\"\" -D__TIME__=\"\""

# Cờ Rust Cargo chuẩn hóa đường dẫn
export RUSTFLAGS="--remap-path-prefix=$(pwd)=/build"

# Chạy so sánh sai khác chi tiết nếu bản dựng không đồng nhất
diffoscope build1/output.tar.gz build2/output.tar.gz --html diff_report.html
```

## 8. Anti-Patterns & Common Traps
- **Embedded Build Timestamps:** Nhúng trực tiếp thời gian biên dịch vào header của file khiến mỗi lần build đều sinh mã băm khác nhau.
- **Filesystem Order Dependence:** Đọc danh sách file nguồn bằng hàm duyệt thư mục không sắp xếp thứ tự dẫn tới thứ tự link các object files bị thay đổi.
- **Unpinned Floating Toolchains:** Sử dụng trình biên dịch phiên bản `latest` thay vì cố định chính xác compiler digest.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Hai lần build độc lập sinh ra file nhị phân có mã băm SHA-256 giống hệt nhau 100%.
- **QG-04**: Báo cáo diffoscope không phát hiện bất kỳ sự khác biệt nào ngoài những vùng dữ liệu đã được giải trình hợp lý.
- **QG-09**: Môi trường build hoàn toàn cô lập, không truy cập Internet trong quá trình compile.

## 10. Security & Safety Boundaries
- Ngăn ngừa các cuộc tấn công kiểu 'Reflections on Trusting Trust' và mã độc chèn vào toolchain bằng cách cho phép nhiều bên độc lập cùng biên dịch và đối soát mã băm.

## 11. Platform Adapters
- **Tools**: diffoscope, reprotest, Docker, Nix, Bazel.

## 12. Deliverables & Output Artifacts
- Container định nghĩa môi trường build tái tạo được.
- Báo cáo phân tích so sánh bit-for-bit từ diffoscope.
- Tài liệu hướng dẫn xác minh độc lập cho bên thứ ba.

## 13. Related & Complementary Skills
dex-binary-provenance-matching, dex-reproducible-build-audit, dex-debug-symbols-correlation

## 14. Realistic Usage Example
```powershell
# Chạy kiểm toán khả năng tái tạo với reprotest
reprotest --vary=-all "cargo build --release" ./target/release/app

# So sánh nhanh mã băm của 2 bản dựng độc lập
Get-FileHash ./build_a/app.exe, ./build_b/app.exe
```
