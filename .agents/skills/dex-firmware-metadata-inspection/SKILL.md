---
name: dex-firmware-metadata-inspection
description: Examine embedded device firmware binary image headers, partition layouts (U-Boot, kernel, rootfs SquashFS), entropy distributions, and hardware architecture metadata using binwalk / dumpimage. Use when auditing authorized IoT device updates, verifying cryptographic signature blocks, or evaluating embedded supply chain integrity. (Strictly authorized/defensive).
---

# dex-firmware-metadata-inspection

## 1. Purpose & Scope
Kiểm tra và thẩm định siêu dữ liệu hình ảnh nhị phân phần sụn thiết bị nhúng (Firmware Image Inspection); phân tích cấu trúc phân vùng (U-Boot bootloader, Linux kernel, hệ thống tệp SquashFS/UBIFS), đo lường phân bố độ hỗn loạn thông tin (Entropy Distribution) để phát hiện mã hóa/nén và xác minh khối chữ ký điện tử; phục vụ kiểm toán an ninh thiết bị IoT và chuỗi cung ứng nhúng.

## 2. When to Use
- Khi kiểm toán tính an toàn của một bản cập nhật phần sụn (OTA Firmware Update) cho thiết bị IoT.
- Khi xác minh xem nhà sản xuất phần cứng có tuân thủ quy chuẩn mã hóa và bảo mật chữ ký số hay không.
- Khi cần kiểm tra danh mục các phần mềm mã nguồn mở có trong hệ thống tệp rootfs của thiết bị nhúng.

## 3. When NOT to Use
- Khi can thiệp vào các thiết bị y tế hoặc hạ tầng công nghiệp đang vận hành trực tiếp.
- Khi cố tình trích xuất khóa bản quyền hoặc vượt qua cơ chế Secure Boot của nhà sản xuất nhằm mục đích phi pháp.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Tệp hình ảnh phần sụn nhị phân (.bin, .img), công cụ phân tích `binwalk`, `dumpimage`, `fdisk` hoặc thư viện đồ họa entropy.
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; tuyệt đối không can thiệp trái phép vào hệ thống của bên thứ ba.

## 5. Core Concepts & Taxonomy
- **U-Boot Image Header:** Khối 64-byte ở đầu tệp chứa thông tin kiến trúc CPU, hệ điều hành, kiểu nén và mã băm kiểm tra CRC32.
- **Entropy Analysis:** Biểu đồ đo mức độ ngẫu nhiên của các byte từ 0.0 đến 8.0. Vùng có entropy ~8.0 biểu thị dữ liệu bị mã hóa hoặc nén chặt, vùng entropy thấp là mã máy chưa nén hoặc bảng chuỗi.
- **Root Filesystem Extraction:** Quá trình bóc tách hệ thống tệp nén SquashFS để kiểm tra các tệp cấu hình và mật khẩu mặc định.

## 6. Step-by-Step Execution Workflow
1. Tạo biểu đồ phân bố entropy của tệp firmware để nhận diện các khối dữ liệu nén hoặc mã hóa.
2. Quét các chữ ký ma thuật (Magic Bytes) bằng công cụ `binwalk firmware.bin`.
3. Bóc tách phân vùng hệ thống tệp rootfs sang thư mục cách ly.
4. Rà soát tệp `/etc/shadow` và các tệp cấu hình để phát hiện mật khẩu cứng (Hardcoded Credentials).
5. Lập báo cáo kiểm toán phần sụn nhúng `FIRMWARE_SECURITY_AUDIT.md`.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```bash
# Analyzing firmware headers and signatures
binwalk -B firmware_update.bin

# Generating entropy graph to spot encrypted blocks
binwalk -E firmware_update.bin

# Inspecting U-Boot multi-image header
dumpimage -l firmware_update.bin

# Extracting SquashFS filesystem safely
binwalk -e -M firmware_update.bin
```

## 8. Anti-Patterns & Common Traps
- Nạp thử nghiệm trực tiếp firmware không rõ nguồn gốc vào thiết bị phần cứng thật làm biến thiết bị thành cục gạch (Bricking).
- Bỏ qua bước kiểm tra khối chữ ký số ở cuối tệp firmware, cho phép kẻ xấu làm giả bản cập nhật.
- Để lộ mật khẩu root mặc định trong tệp shadow của hệ thống tệp thiết bị xuất xưởng.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Báo cáo kiểm toán xác định rõ ràng bảng phân vùng bộ nhớ flash và kiến trúc CPU mục tiêu.
- QG-02: Khối chữ ký điện tử mật mã được xác minh tính hợp lệ trước khi phân tích sâu.
- QG-03: Không phát hiện bất kỳ mật khẩu tài khoản mặc định hoặc khóa SSH bí mật nào trong rootfs.

## 10. Security & Safety Boundaries
- Tuân thủ nghiêm ngặt các quy định về an toàn phần cứng; không thực hiện các thao tác có nguy cơ gây cháy nổ hoặc hỏng hóc vĩnh viễn thiết bị thí nghiệm.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Hoạt động phân tích hoàn toàn hợp pháp, minh bạch và có sự ủy quyền chính thức từ chủ sở hữu hệ thống.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Báo cáo kiểm toán phần sụn thiết bị `FIRMWARE_SECURITY_AUDIT.md`.
1. Sơ đồ phân vùng bộ nhớ và biểu đồ phân tích entropy.

## 13. Related & Complementary Skills
- [`dex-pe-elf-structure-inspection`](.agents/skills/dex-pe-elf-structure-inspection/SKILL.md)
- [`dex-reverse-evidence-chain`](.agents/skills/dex-reverse-evidence-chain/SKILL.md)
- [`dex-supply-chain-security`](.agents/skills/dex-supply-chain-security/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Công ty triển khai hệ thống 500 camera giám sát mới. Kỹ sư kích hoạt `dex-firmware-metadata-inspection` để phân tích tệp firmware cập nhật từ hãng sản xuất, phát hiện trong hệ thống tệp SquashFS có một tài khoản telnet bí mật với mật khẩu mặc định `admin1234`, kịp thời yêu cầu hãng vá lỗi trước khi lắp đặt.
