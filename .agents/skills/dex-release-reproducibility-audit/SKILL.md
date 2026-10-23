---
name: dex-release-reproducibility-audit
description: Audit and enforce bit-for-bit reproducible builds using diffoscope, containerized build environments, SOURCE_DATE_EPOCH timestamps, and deterministic compiler flags. Use when validating SLSA Level 3/4 provenance and eliminating build-time covert tampering.
---

# dex-release-reproducibility-audit

## 1. Purpose & Scope
Kiểm toán và thực thi quy trình biên dịch tái lập từng bit (Bit-for-Bit Reproducible Builds); sử dụng công cụ `diffoscope`, môi trường container đóng kín (Hermetic Build Environments), chuẩn hóa dấu thời gian `SOURCE_DATE_EPOCH` và cờ trình biên dịch xác định; đảm bảo hai lần biên dịch độc lập từ cùng một commit mã nguồn luôn tạo ra các tệp nhị phân có mã băm SHA-256 hoàn toàn trùng khớp; đạt chuẩn an ninh chuỗi cung ứng SLSA Level 3/4.

## 2. When to Use
- Khi xây dựng các phần mềm đòi hỏi độ tin cậy tuyệt đối (phần mềm ví tiền mã hóa, nhân hệ điều hành, công cụ an ninh mạng).
- Khi cần chứng minh với khách hàng và cơ quan kiểm toán rằng tệp nhị phân phân phối thực sự được sinh ra từ đúng mã nguồn mở công khai.
- Khi kiểm tra xem hạ tầng máy chủ build CI có bị cài cắm mã độc can thiệp ngầm vào quá trình biên dịch hay không.

## 3. When NOT to Use
- Khi phát triển các ứng dụng nội bộ thử nghiệm thay đổi mã nguồn liên tục từng phút.
- Khi ngôn ngữ lập trình hoặc công cụ đóng gói không hỗ trợ cơ chế biên dịch tái lập.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Công cụ phân tích sai khác nhị phân `diffoscope`, môi trường Docker đóng kín không có mạng (Hermetic container), biến môi trường `SOURCE_DATE_EPOCH`.
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; bảo vệ toàn vẹn tài sản kỹ nghệ và dữ liệu sản xuất.

## 5. Core Concepts & Taxonomy
- **Non-Deterministic Build Artifacts:** Các yếu tố làm lệch mã băm nhị phân: Dấu thời gian hiện tại được nhúng vào header, đường dẫn thư mục tạm `/tmp/build_123` bị ghi vào debug symbol, và thứ tự duyệt tệp tin ngẫu nhiên của hệ điều hành.
- **SOURCE_DATE_EPOCH Specification:** Tiêu chuẩn quốc tế thay thế thời gian hiện tại bằng dấu thời gian của commit Git gần nhất (Unix timestamp cố định).
- **Hermetic Build Sandbox:** Môi trường biên dịch bị cô lập hoàn toàn không có kết nối Internet và không bị ảnh hưởng bởi biến môi trường của máy chủ chủ quản.

## 6. Step-by-Step Execution Workflow
1. Thiết lập biến môi trường `export SOURCE_DATE_EPOCH=$(git log -1 --pretty=%ct)`.
2. Cấu hình cờ trình biên dịch để ánh xạ lại đường dẫn thư mục thành đường dẫn ảo đồng nhất (`-fdebug-prefix-map`).
3. Sắp xếp danh sách tệp tin đầu vào theo thứ tự bảng chữ cái trước khi đưa vào trình nén lưu trữ (tar/zip).
4. Thực hiện hai lần biên dịch độc lập trên hai máy chủ khác nhau hoàn toàn.
5. So sánh mã băm SHA-256 của hai bản dựng; nếu lệch, dùng `diffoscope` để bóc tách byte khác biệt và khắc phục.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```bash
# Setting deterministic build environment
export SOURCE_DATE_EPOCH=$(git log -1 --pretty=%ct)
export LC_ALL=C
export TZ=UTC

# Compiling with deterministic path mapping in GCC/Clang
gcc -O2 -g -fdebug-prefix-map=$(pwd)=/build_root -c main.c -o main.o

# Creating deterministic tarball without host metadata
tar --sort=name --mtime="@${SOURCE_DATE_EPOCH}" --owner=0 --group=0 --numeric-owner \
    -czf release-reproducible.tar.gz bin/

# Verifying bit-for-bit reproducibility
diffoscope build_run_1/release.tar.gz build_run_2/release.tar.gz
```

## 8. Anti-Patterns & Common Traps
- Nhúng macro thời gian `__DATE__` hoặc `__TIME__` trong mã nguồn C++ (khiến mỗi giây biên dịch tạo ra một bản nhị phân khác hẳn nhau).
- Nén tệp zip/tar mà không sắp xếp tên tệp, khiến thứ tự đọc tệp trên đĩa làm thay đổi mã băm của tệp nén.
- Để tệp nhị phân chứa đường dẫn thư mục máy trạm cá nhân của lập trình viên (ví dụ `C:\Users\John\...`).

## 9. Quality Gates & Acceptance Criteria
- QG-01: Hai lần biên dịch độc lập trên hai môi trường khác nhau cho ra mã băm SHA-256 hoàn toàn trùng khớp 100%.
- QG-02: Công cụ `diffoscope` so sánh hai bản dựng trả về kết quả 0 sai khác (Clean Diff).
- QG-03: Mọi tệp nén và nhị phân đều tuân thủ chuẩn `SOURCE_DATE_EPOCH`.

## 10. Security & Safety Boundaries
- Triệt tiêu hoàn toàn nguy cơ máy chủ CI bị cài cắm mã độc ngầm (như vụ tấn công XcodeGhost) bằng cách cho phép bất kỳ ai cũng có thể tự biên dịch và đối soát mã băm nhị phân.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Đường ống biên dịch tái lập từng bit `reproducible_build.sh`.
1. Báo cáo kiểm toán tái lập nhị phân `REPRODUCIBILITY_AUDIT.md`.

## 13. Related & Complementary Skills
- [`dex-binary-diff-regression`](.agents/skills/dex-binary-diff-regression/SKILL.md)
- [`dex-code-signing-release-process`](.agents/skills/dex-code-signing-release-process/SKILL.md)
- [`dex-build-slsa-controls`](.agents/skills/dex-build-slsa-controls/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Dự án phát triển thư viện mật mã học công khai mã nguồn. Kỹ sư kích hoạt `dex-release-reproducibility-audit`, loại bỏ macro thời gian biên dịch, ánh xạ lại đường dẫn debug prefix map và thiết lập `SOURCE_DATE_EPOCH`, giúp cộng đồng mạng có thể tự tải mã nguồn về biên dịch và đối soát ra đúng mã băm SHA-256 với tệp phát hành chính thức.
