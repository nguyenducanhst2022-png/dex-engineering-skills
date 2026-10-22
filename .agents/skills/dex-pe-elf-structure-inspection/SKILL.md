---
name: dex-pe-elf-structure-inspection
description: Inspect compiled PE (Windows) and ELF (Linux) executable headers, section tables (.text, .rdata, .reloc), dynamic import/export tables, and compiler security flags (ASLR, DEP/NX, SafeSEH, Control Flow Guard). Use when verifying compiled binary provenance, supply chain build integrity, or native dependency linkage. (Strictly authorized/defensive).
---

# dex-pe-elf-structure-inspection

## 1. Purpose & Scope
Kiểm tra và thẩm định cấu trúc tệp thực thi nhị phân PE (Portable Executable trên Windows) và ELF (Executable and Linkable Format trên Linux); phân tích bảng phần tử (.text, .rdata, .reloc), bảng hàm nhập/xuất (Import/Export tables) và các cờ an ninh của trình biên dịch (ASLR, DEP/NX, Control Flow Guard); phục vụ xác minh nguồn gốc xuất xứ của bản dựng và chuỗi cung ứng phần mềm hợp pháp.

## 2. When to Use
- Khi kiểm toán tính toàn vẹn của tệp thực thi nhị phân trước khi đưa vào môi trường sản xuất của doanh nghiệp.
- Khi xác minh xem bản dựng đã được bật đầy đủ các cờ an ninh bảo vệ bộ nhớ của trình biên dịch hay chưa.
- Khi điều tra các xung đột liên kết thư viện động (DLL Hell hoặc SO missing dependencies).

## 3. When NOT to Use
- Khi cố tình dịch ngược phần mềm thương mại có bản quyền nhằm mục đích bẻ khóa (cracking) hoặc vi phạm DRM.
- Khi phân tích các tệp kịch bản mã nguồn mở thông thường như Python hay JavaScript.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Tệp thực thi nhị phân được cấp quyền kiểm toán, công cụ dòng lệnh tiêu chuẩn: `readelf`, `objdump`, `dumpbin` hoặc thư viện Python `pefile`.
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; tuyệt đối không can thiệp trái phép vào hệ thống của bên thứ ba.

## 5. Core Concepts & Taxonomy
- **Binary Headers Anatomy:** Phân tích DOS Header, PE Signature, COFF Header và Optional Header trên Windows; ELF Header và Program Header Table trên Linux.
- **Mitigation Flags Verification:** Kiểm tra cờ DYNAMIC_BASE (ASLR), NX_COMPAT (DEP), SafeSEH và Control Flow Guard (CFG).
- **Import Address Table (IAT):** Danh sách các hàm API hệ điều hành mà tệp nhị phân phụ thuộc vào khi nạp vào bộ nhớ.

## 6. Step-by-Step Execution Workflow
1. Trích xuất mã băm SHA-256 của tệp nhị phân để thiết lập chuỗi bằng chứng.
2. Đọc cấu trúc header của tệp bằng công cụ phân tích tĩnh an toàn.
3. Rà soát danh sách các section và kiểm tra tỷ lệ entropy để phát hiện trình đóng gói (Packer/Obfuscator).
4. Kiểm tra danh sách các cờ bảo vệ an ninh bộ nhớ của trình biên dịch.
5. Lập báo cáo kiểm định nhị phân `BINARY_INSPECTION_REPORT.md`.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```python
# Inspecting PE Security Flags via pefile (Defensive Audit)
import pefile

def audit_pe_security(filepath: str) -> dict:
    pe = pefile.PE(filepath)
    dll_characteristics = pe.OPTIONAL_HEADER.DllCharacteristics
    
    return {
        "ASLR_ENABLED": bool(dll_characteristics & 0x0040), # IMAGE_DLLCHARACTERISTICS_DYNAMIC_BASE
        "DEP_NX_ENABLED": bool(dll_characteristics & 0x0100), # IMAGE_DLLCHARACTERISTICS_NX_COMPAT
        "GUARD_CF_ENABLED": bool(dll_characteristics & 0x4000), # IMAGE_DLLCHARACTERISTICS_GUARD_CF
        "SECTIONS": [s.Name.decode('utf-8', errors='ignore').strip('\x00') for s in pe.sections]
    }
```

## 8. Anti-Patterns & Common Traps
- Thực thi trực tiếp tệp nhị phân không rõ nguồn gốc trong môi trường làm việc chính mà không có sandbox cô lập.
- Bỏ qua bước kiểm tra cờ an ninh ASLR/DEP khiến ứng dụng dễ bị tấn công khai thác tràn bộ đệm.
- Thay đổi cấu trúc byte của tệp nhị phân mà không có sự ủy quyền chính thức.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Báo cáo kiểm toán ghi nhận đầy đủ mã băm SHA-256 và danh sách cờ an ninh của tệp.
- QG-02: 100% các tệp nhị phân sản xuất đều kích hoạt cờ ASLR và DEP/NX.
- QG-03: Hoạt động phân tích diễn ra hoàn toàn tĩnh (Static Analysis), không thực thi mã lệnh.

## 10. Security & Safety Boundaries
- Nghiêm cấm tuyệt đối việc sử dụng kỹ năng để phá hoại, né tránh hệ thống DRM, vi phạm thỏa thuận EULA hoặc tạo phần mềm độc hại.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Hoạt động phân tích hoàn toàn hợp pháp, minh bạch và có sự ủy quyền chính thức từ chủ sở hữu hệ thống.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Báo cáo kiểm định cấu trúc nhị phân `BINARY_INSPECTION_REPORT.md`.
1. Bảng kiểm tra danh sách hàm nhập/xuất của tệp thực thi.

## 13. Related & Complementary Skills
- [`dex-binary-inspection`](.agents/skills/dex-binary-inspection/SKILL.md)
- [`dex-native-symbol-mapping`](.agents/skills/dex-native-symbol-mapping/SKILL.md)
- [`dex-reverse-evidence-chain`](.agents/skills/dex-reverse-evidence-chain/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Kiểm toán gói cài đặt phần mềm nội bộ của nhà cung cấp bên thứ ba trước khi phát hành cho 10,000 máy trạm ngân hàng. Sử dụng `dex-pe-elf-structure-inspection` để phân tích tệp `.exe`, phát hiện nhà cung cấp quên bật cờ ASLR và yêu cầu họ biên dịch lại với cờ bảo vệ trước khi nghiệm thu.
