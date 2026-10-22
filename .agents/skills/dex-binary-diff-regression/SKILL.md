---
name: dex-binary-diff-regression
description: Perform binary-level diffing between build versions to isolate patch regression evidence, compiler flag shifts, and unintended symbol removals using safe utilities (radiff2, diffoscope). Use when analyzing third-party patch modifications, validating hotfix integrity, or verifying reproducible builds. (Strictly authorized/defensive).
---

# dex-binary-diff-regression

## 1. Purpose & Scope
Thực hiện so sánh sai khác ở cấp độ nhị phân (Binary Diffing) giữa hai phiên bản bản dựng khác nhau; cô lập các bằng chứng thay đổi do bản vá bảo mật (Patch Analysis), phát hiện sự thay đổi ngầm của các cờ trình biên dịch và các biểu tượng bị xóa ngoài ý muốn bằng các tiện ích chuẩn (`radiff2`, `diffoscope`); phục vụ xác minh tính toàn vẹn của bản vá nóng (Hotfix Integrity) và bản dựng tái lập (Reproducible Builds).

## 2. When to Use
- Khi kiểm tra xem một bản vá khẩn cấp của nhà cung cấp chỉ sửa đúng lỗi đã công bố hay có kèm theo các thay đổi ẩn khác.
- Khi điều tra nguyên nhân một hàm bị suy giảm hiệu năng đột ngột sau khi nâng cấp phiên bản trình biên dịch.
- Khi thẩm định tính lặp lại từng bit (Bit-for-bit Reproducibility) của sản phẩm phần mềm độc lập.

## 3. When NOT to Use
- Khi có sẵn mã nguồn Git rõ ràng có thể xem diff bằng lệnh `git diff` thông thường.
- Khi cố tình so sánh để tìm kiếm lỗ hổng chưa vá (1-day exploit) nhằm mục đích tấn công khai thác.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Hai tệp nhị phân cần so sánh (bản gốc và bản vá), công cụ phân tích diff nhị phân như `diffoscope`, `radiff2` hoặc `llvm-diff`.
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; tuyệt đối không can thiệp trái phép vào hệ thống của bên thứ ba.

## 5. Core Concepts & Taxonomy
- **Structural vs Byte Diff:** Phân biệt giữa sai khác do địa chỉ bộ nhớ bị trôi (Relocation Shift) và sai khác thực sự về logic mã máy bên trong thân hàm.
- **Function Graph Matching:** So khớp đồ thị luồng điều khiển của từng hàm giữa hai phiên bản để nhận diện các khối lệnh mới được thêm vào hoặc loại bỏ.
- **Reproducible Build Verification:** Hai lần biên dịch từ cùng một commit mã nguồn phải cho ra hai tệp nhị phân có mã băm SHA-256 hoàn toàn trùng khớp từng byte.

## 6. Step-by-Step Execution Workflow
1. Tạo mã băm SHA-256 cho cả hai tệp nhị phân `v1.dll` và `v2.dll`.
2. Chạy công cụ `diffoscope` để bóc tách các tầng cấu trúc sai khác (headers, sections, symbols).
3. Sử dụng `radiff2 -g` để so sánh đồ thị hàm nhị phân và xác định các hàm có sự thay đổi logic.
4. Bóc tách mã hợp ngữ của phần thay đổi và phân tích tác động kỹ thuật.
5. Lập biên bản kết quả so sánh nhị phân `BINARY_DIFF_REPORT.md`.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```bash
# High-level structural binary difference via diffoscope
diffoscope build_v1.exe build_v2.exe --html diff_report.html

# Function-level binary diff using radiff2
radiff2 -C build_v1.dll build_v2.dll

# Compare specific function graphs and output graphviz dot
radiff2 -g verify_token build_v1.dll build_v2.dll > token_diff.dot
```

## 8. Anti-Patterns & Common Traps
- Chỉ dùng lệnh so sánh file thông thường `diff` khiến hàng triệu byte địa chỉ con trỏ bị trôi làm tràn ngập màn hình mà không thấy được logic thực sự.
- Kết luận bản dựng có mã độc chỉ vì mã băm thay đổi do dấu thời gian biên dịch (Timestamp Difference).
- Bỏ qua bước so sánh cấu trúc bảng import/export khi đánh giá bản vá.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Báo cáo diff nhị phân tách biệt rõ ràng giữa sai khác do timestamp/relocation và sai khác logic nghiệp vụ.
- QG-02: 100% các hàm có mã máy thay đổi được lập danh mục và giải thích nguyên nhân kỹ thuật.
- QG-03: Không có bất kỳ biểu tượng xuất khẩu công khai (Exported Symbols) nào bị biến mất ngoài ý muốn.

## 10. Security & Safety Boundaries
- Không sử dụng thông tin phân tích diff bản vá bảo mật để tấn công các hệ thống chưa kịp cập nhật bản vá trong thực tế.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Hoạt động phân tích hoàn toàn hợp pháp, minh bạch và có sự ủy quyền chính thức từ chủ sở hữu hệ thống.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Báo cáo sai khác nhị phân trực quan `BINARY_DIFF_REPORT.html`.
1. Danh mục các hàm bị biến đổi logic và đánh giá rủi ro hồi quy.

## 13. Related & Complementary Skills
- [`dex-disassembly-cfg-reconstruction`](.agents/skills/dex-disassembly-cfg-reconstruction/SKILL.md)
- [`dex-pe-elf-structure-inspection`](.agents/skills/dex-pe-elf-structure-inspection/SKILL.md)
- [`dex-release-reproducibility-audit`](.agents/skills/dex-release-reproducibility-audit/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Sau khi cập nhật bản vá khẩn cấp của thư viện mã hóa đối tác, hệ thống bị chậm 20%. Kỹ sư kích hoạt `dex-binary-diff-regression` để so sánh nhị phân giữa hai phiên bản DLL, phát hiện nhà cung cấp đã vô tình tắt cờ tối ưu hóa vector AVX2 trong bản dựng mới, giúp gửi phản hồi chính xác để đối tác phát hành bản sửa lỗi trong ngày.
