---
name: dex-firmware-image-structure-diffing
description: Extract, unpack, and structurally compare IoT and embedded firmware images across releases to identify changed partitions, updated kernel modules, modified rootfs assets, and exposed secrets. Use when conducting authorized hardware security reviews.
---

# dex-firmware-image-structure-diffing

## 1. Purpose & Scope
Trích xuất, giải nén và so sánh cấu trúc các ảnh firmware nhúng (IoT, thiết bị mạng, vi điều khiển); xác định các phân vùng bị thay đổi, các kernel modules được cập nhật, tài nguyên rootfs bị chỉnh sửa và phát hiện các khóa bí mật hoặc mật khẩu hardcoded bị lộ qua các bản cập nhật.

## 2. When to Use
- Khi kiểm toán an ninh thiết bị IoT trước khi đưa vào hệ thống mạng doanh nghiệp.
- Khi phân tích bản cập nhật firmware của nhà cung cấp để kiểm tra xem lỗ hổng đã thực sự được vá hay chưa.
- Khi kiểm tra tính toàn vẹn của firmware tự build so với firmware chuẩn của nhà sản xuất.

## 3. When NOT to Use
- Khi phân tích các ứng dụng phần mềm thuần túy không có yếu tố nhúng hoặc hệ thống tệp nhị phân nén phần cứng.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** File ảnh firmware (.bin, .img, .hex), công cụ trích xuất firmware (binwalk, squashfs-tools, sasquatch).
- **Quyền hạn truy cập:** Quyền chạy công cụ phân tích nhị phân trong môi trường an toàn.

## 5. Core Concepts & Taxonomy
- **Firmware Anatomy:** Cấu trúc điển hình gồm: Bootloader (U-Boot) + Kernel (uImage/zImage) + Root Filesystem (SquashFS, UBIFS, CramFS) + Cấu hình NVRAM.
- **Signature Entropy Analysis:** Đồ thị entropy giúp phân biệt vùng dữ liệu nén, vùng mã thực thi và vùng mã hóa dữ liệu.
- **Silent Shadow Updates:** Nhà sản xuất cập nhật tính năng hoặc vá lỗi nhưng không ghi rõ trong changelog chính thức.

## 6. Step-by-Step Execution Workflow
1. Thực hiện quét chữ ký và tính toán entropy của ảnh firmware bằng `binwalk` để xác định cấu trúc phân vùng.
2. Trích xuất toàn bộ hệ thống tệp root filesystem (SquashFS / UBIFS) sang thư mục phân tích.
3. Thực hiện tương tự cho phiên bản firmware trước đó ($v_{N-1}$).
4. Chạy công cụ so sánh cấu trúc thư mục để phát hiện các file nhị phân, cấu hình, script bị thêm mới hoặc sửa đổi.
5. Quét tìm các chuỗi nhạy cảm: khóa SSH private keys, mật khẩu shadow, API tokens trong hệ thống tệp đã trích xuất.
6. Kiểm tra phiên bản Linux kernel và các driver hạt nhân (.ko) để phát hiện các CVE chưa được xử lý.

## 7. Concrete Examples
### Phân tích và trích xuất hệ thống tệp firmware bằng binwalk:
```bash
# Quét chữ ký cấu trúc bên trong ảnh firmware
binwalk firmware-v2.0.bin

# Trích xuất tự động toàn bộ phân vùng SquashFS
binwalk -e -M firmware-v2.0.bin

# So sánh sai khác cấu trúc hệ thống tệp giữa 2 bản firmware
diff -ruN _firmware-v1.0.bin.extracted/squashfs-root _firmware-v2.0.bin.extracted/squashfs-root > firmware_diff.patch

# Quét tìm SSH keys hoặc chứng chỉ nhúng trong rootfs
find _firmware-v2.0.bin.extracted/ -name "*.pem" -o -name "*.key" -o -name "id_rsa*"
```

## 8. Anti-Patterns & Common Traps
- **Flashing Directly Without Review:** Nạp trực tiếp firmware mới vào thiết bị phần cứng thực tế mà không qua phân tích tĩnh trước.
- **Ignoring Monolithic Blobs:** Bỏ qua các phân vùng dữ liệu không nén được mà không kiểm tra entropy để xem liệu chúng có bị mã hóa hay không.
- **Overlooking Default Credentials:** Quên kiểm tra file `/etc/passwd` và `/etc/shadow` xem có tài khoản backdoor mặc định hay không.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Trích xuất thành công tối thiểu phân vùng root filesystem chính của ảnh firmware.
- **QG-06**: Không có private key, mật khẩu mặc định hoặc token nhạy cảm nào bị nhúng trong rootfs.
- **QG-09**: Tất cả các tệp nhị phân thay đổi đều được ghi nhận và đối chiếu với changelog phát hành.

## 10. Security & Safety Boundaries
- Ngăn ngừa các lỗ hổng nghiêm trọng cho phép chiếm quyền điều khiển từ xa (RCE) trên các thiết bị biên IoT hoặc router mạng.

## 11. Platform Adapters
- **Tools**: binwalk, squashfs-tools, sasquatch, ubi_reader, cve-bin-tool, strings.

## 12. Deliverables & Output Artifacts
- Cây thư mục root filesystem đã được giải nén hoàn chỉnh.
- Bản so sánh sai khác (patch diff) giữa hai phiên bản firmware.
- Báo cáo lỗ hổng CVE và các phát hiện khóa bí mật bị lộ.

## 13. Related & Complementary Skills
dex-installer-package-static-review, dex-binary-provenance-matching, dex-reverse-engineering-reporting

## 14. Realistic Usage Example
```powershell
# Quét entropy của file firmware để phát hiện vùng dữ liệu mã hóa
binwalk -E firmware.bin

# Tìm kiếm các chuỗi mật khẩu hoặc API keys nhúng
Select-String -Path "_firmware.bin.extracted/**/*" -Pattern "password", "api_key", "secret"
```
