---
name: dex-reverse-engineering-reporting
description: Synthesize technical findings from disassemblers, decompilers, binary diffing, and dynamic traces into authoritative, verifiable, and legally compliant engineering reports. Use when documenting authorized security assessments and interoperability research.
---

# dex-reverse-engineering-reporting

## 1. Purpose & Scope
Tổng hợp và biên soạn các phát hiện kỹ thuật từ công cụ dịch ngược (Ghidra, IDA Pro, Binary Ninja), công cụ diffing nhị phân và nhật ký trace động thành các báo cáo kỹ thuật chuẩn mực, có thể kiểm chứng độc lập và tuân thủ đầy đủ khuôn khổ pháp lý; phục vụ đánh giá an ninh được ủy quyền hoặc nghiên cứu khả năng tương tác.

## 2. When to Use
- Khi hoàn thành một đợt kiểm toán an ninh nhị phân hoặc dịch ngược phần mềm được ủy quyền hợp pháp.
- Khi cần giải thích các phát hiện kỹ thuật phức tạp (như buffer overflow, logic flaw) cho cả ban quản lý và đội ngũ kỹ thuật.
- Khi lưu trữ chuỗi bằng chứng (Chain of Custody) phục vụ các vụ việc pháp lý hoặc giải quyết tranh chấp quyền sở hữu trí tuệ.

## 3. When NOT to Use
- Khi tiến hành các hoạt động phân tích không được ủy quyền hoặc vi phạm thỏa thuận cấp phép người dùng cuối (EULA).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Nhật ký phân tích từ decompiler, đồ thị luồng điều khiển (CFG), mã băm mẫu thử, biên bản ủy quyền phân tích.
- **Quyền hạn truy cập:** Quyền tổng hợp tài liệu bảo mật và truy xuất kho lưu trữ bằng chứng.

## 5. Core Concepts & Taxonomy
- **Verifiability & Reproducibility:** Mọi nhận định trong báo cáo đều phải đi kèm địa chỉ bộ nhớ cụ thể (RVA), mã giả (pseudocode), hoặc kịch bản tái hiện (PoC) để người khác có thể kiểm chứng độc lập.
- **Executive Summary vs. Technical Deep-Dive:** Báo cáo phải có phần tóm tắt tác động nghiệp vụ cho lãnh đạo và phần phân tích chi tiết cấp byte cho kỹ sư.
- **Legal Compliance & Scope Boundaries:** Ghi rõ phạm vi ủy quyền (Scope of Authorization), các điều khoản miễn trừ trách nhiệm và các giới hạn đạo đức nghề nghiệp.

## 6. Step-by-Step Execution Workflow
1. Thu thập toàn bộ bằng chứng kỹ thuật: mã băm SHA-256 mẫu thử, phiên bản công cụ phân tích, ảnh chụp CFG, đoạn mã giả.
2. Lập cấu trúc báo cáo chuẩn mực: Tóm tắt tổng quan, Phạm vi công việc, Phương pháp luận, Phát hiện chi tiết, Khuyến nghị khắc phục.
3. Định dạng các địa chỉ bộ nhớ và mã giả theo quy chuẩn thống nhất (ví dụ: `sub_401000`, `RVA + 0x1200`).
4. Xếp hạng mức độ nghiêm trọng của từng phát hiện theo chuẩn CVSS v3.1 / v4.0.
5. Đính kèm hướng dẫn tái tạo từng bước (Step-by-step reproduction guide) có thể kiểm chứng.
6. Thực hiện bình duyệt chéo (Peer Review) nội bộ trước khi ban hành báo cáo chính thức.

## 7. Concrete Examples
### Cấu trúc một báo cáo phân tích dịch ngược kỹ thuật chuẩn mực:
```markdown
# Báo Cáo Đánh Giá An Ninh Nhị Phân — Mã Tài Liệu: SEC-REV-2026-01

### 1. Thông Tin Mẫu Phân Tích
- **Tên tệp:** `network_daemon.elf`
- **Mã băm SHA-256:** `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- **Kiến trúc:** x86_64 ELF (Linux 64-bit, dynamically linked)
- **Công cụ sử dụng:** Ghidra 11.0, GDB 14.1, Diffoscope 250

### 2. Tóm Tắt Phát Hiện (Executive Summary)
Phát hiện lỗ hổng tràn bộ đệm dựa trên ngăn xếp (Stack-based Buffer Overflow) tại hàm xử lý gói tin xác thực `parse_auth_packet()`. Lỗ hổng cho phép kẻ tấn công thực thi mã từ xa (RCE) với quyền root mà không cần đăng nhập.

### 3. Phân Tích Kỹ Thuật Chi Tiết (Technical Deep-Dive)
- **Địa chỉ bộ nhớ:** `0x004018A0` (`parse_auth_packet`)
- **Nguyên nhân cốt lõi:** Sử dụng hàm không an toàn `strcpy` để sao chép dữ liệu người dùng vào bộ đệm cố định 256 bytes trên stack.
```c
// Mã giả trích xuất từ Ghidra tại RVA 0x004018A0:
void parse_auth_packet(char *user_input) {
    char local_buffer[256];
    // Nguy cơ: user_input không được kiểm tra độ dài
    strcpy(local_buffer, user_input);
}
```

### 4. Hướng Dẫn Khắc Phục (Remediation)
Thay thế `strcpy` bằng hàm có giới hạn độ dài an toàn `strncpy(local_buffer, user_input, sizeof(local_buffer) - 1)` hoặc sử dụng các cấu trúc chuỗi có quản lý kích thước.
```

## 8. Anti-Patterns & Common Traps
- **Speculative Claims:** Đưa ra kết luận lỗ hổng bảo mật dựa trên suy đoán mà không có bằng chứng mã giả hoặc trace cụ thể.
- **Omitting Sample Hashes:** Không ghi lại mã băm SHA-256 của file nhị phân khiến việc đối chiếu lại mẫu thử trong tương lai bất khả thi.
- **Disclosing Raw Exploits Without Mitigation:** Cung cấp mã khai thác vũ khí hóa mà không đưa ra giải pháp vá lỗi phòng vệ tương ứng.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: 100% mẫu phân tích đều có mã băm SHA-256 bất biến và thông tin môi trường ghi nhận rõ ràng.
- **QG-04**: Mọi đoạn mã giả trích dẫn đều có địa chỉ bộ nhớ RVA chính xác tương ứng.
- **QG-09**: Báo cáo có đầy đủ khuyến nghị khắc phục chi tiết cho từng phát hiện được nêu.

## 10. Security & Safety Boundaries
- Tuân thủ nghiêm ngặt các quy định về tiết lộ thông tin có trách nhiệm (Coordinated Vulnerability Disclosure) để bảo vệ người dùng cuối.

## 11. Platform Adapters
- **Disassemblers**: Ghidra, IDA Pro, Binary Ninja, Radare2.
- **Documentation**: Markdown, Pandoc, LaTeX, AsciiDoc.

## 12. Deliverables & Output Artifacts
- Báo cáo phân tích dịch ngược kỹ thuật (PDF / Markdown).
- Kho lưu trữ các đoạn script phân tích và cấu hình IDA/Ghidra database.
- Bảng ma trận các phát hiện được phân loại theo điểm số CVSS.

## 13. Related & Complementary Skills
dex-debug-symbols-correlation, dex-binary-provenance-matching, dex-firmware-image-structure-diffing

## 14. Realistic Usage Example
```powershell
# Chuyển đổi báo cáo Markdown sang tài liệu PDF hoàn chỉnh bằng Pandoc
pandoc reverse_report.md -o reverse_report.pdf --toc --highlight-style=tango

# Xác thực mã băm SHA256 của mẫu thử ghi trong báo cáo
Get-FileHash -Algorithm SHA256 ./samples/target_sample.bin
```
