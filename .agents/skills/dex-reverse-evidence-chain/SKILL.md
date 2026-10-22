---
name: dex-reverse-evidence-chain
description: Establish immutable forensic evidence chains for authorized technical audits with cryptographic artifact hashing (SHA-256, BLAKE3), timestamped execution logs, toolchain provenance tracking, and objective observation reporting. Use when documenting security investigations, IP audits, or compliance verifications.
---

# dex-reverse-evidence-chain

## 1. Purpose & Scope
Thiết lập chuỗi bằng chứng kỹ thuật pháp lý bất biến (Forensic Evidence Chain) cho các đợt kiểm toán kỹ thuật được ủy quyền; đảm bảo tính toàn vẹn của hiện vật thông qua mã băm mật mã (SHA-256, BLAKE3), nhật ký thực thi có gắn dấu thời gian (Timestamped Execution Logs), truy vết xuất xứ công cụ (Toolchain Provenance) và biên soạn báo cáo quan sát khách quan, loại bỏ các giả định chủ quan.

## 2. When to Use
- Khi thực hiện điều tra sự cố an ninh thông tin (Incident Response) cần thu thập bằng chứng phục vụ pháp lý.
- Khi kiểm toán sở hữu trí tuệ hoặc tranh chấp bản quyền mã nguồn phần mềm.
- Khi bàn giao kết quả thẩm định kỹ thuật độc lập cho ban giám đốc hoặc cơ quan chức năng.

## 3. When NOT to Use
- Khi ghi chép nhật ký phát triển hàng ngày trong các buổi họp kỹ thuật nội bộ thông thường.
- Khi thực hiện các tác vụ debug tạm thời không cần bảo toàn bằng chứng pháp lý.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Tài liệu ủy quyền kiểm toán bằng văn bản, tiện ích tạo mã băm mật mã (`sha256sum`, `b3sum`), môi trường ghi nhận nhật ký chỉ đọc (Append-only storage).
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; tuyệt đối không can thiệp trái phép vào hệ thống của bên thứ ba.

## 5. Core Concepts & Taxonomy
- **Chain of Custody:** Nhật ký ghi nhận chi tiết ai là người tiếp cận hiện vật, vào thời điểm nào, bằng công cụ gì và trạng thái mã băm có bị thay đổi hay không.
- **Cryptographic Timestamping:** Gắn dấu thời gian có ký điện tử để chứng minh bằng chứng tồn tại ở một mốc thời gian xác định và không bị chỉnh sửa hồi tố.
- **Objective Observation vs Speculation:** Chỉ ghi nhận các sự kiện có bằng chứng vật lý đo đạc được (ví dụ: 'Offset 0x100 chứa chuỗi ABC') thay vì phỏng đoán chủ quan.

## 6. Step-by-Step Execution Workflow
1. Ngay khi tiếp nhận hiện vật kỹ thuật, tính toán mã băm SHA-256 và BLAKE3 và lưu vào sổ cái kiểm toán.
2. Tạo một bản sao làm việc (Working Copy) và cất giữ bản gốc trong kho lưu trữ chỉ đọc (Read-only Quarantine).
3. Ghi lại toàn bộ phiên làm việc của terminal (sử dụng công cụ `script` hoặc session recording) kèm phiên bản chính xác của mọi công cụ sử dụng.
4. Mỗi kết luận đưa ra trong báo cáo phải trích dẫn trực tiếp mã băm của tệp và số dòng/offset của bằng chứng.
5. Ký số điện tử lên tài liệu báo cáo tổng kết cuối cùng bằng khóa PGP/GPG.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```json
{
  "$schema": "https://dex.dev/schemas/forensic-evidence.json",
  "auditId": "AUDIT-2026-X10",
  "investigator": "Lead Security Auditor",
  "timestampUtc": "2026-10-22T14:30:00Z",
  "evidenceArtifacts": [
    {
      "filename": "vendor_driver.sys",
      "sizeBytes": 1048576,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "blake3": "af1349b9f5f9a1a6a0404dea36dcc9499bcb25c9adc112b7cc9a93cae41f3262",
      "storageLocation": "vault/evidence/vendor_driver.sys.enc"
    }
  ],
  "toolchain": {
    "llvm-objdump": "18.1.0-win64",
    "diffoscope": "260-linux"
  }
}
```

## 8. Anti-Patterns & Common Traps
- Thao tác trực tiếp trên tệp hiện vật gốc duy nhất làm thay đổi dấu thời gian truy cập hoặc biến đổi nội dung tệp.
- Đưa ra các kết luận khẳng định mang tính quy chụp khi chưa có bằng chứng nhị phân xác thực đối chứng.
- Sử dụng các công cụ không rõ nguồn gốc hoặc không ghi lại số hiệu phiên bản của công cụ phân tích.

## 9. Quality Gates & Acceptance Criteria
- QG-01: 100% hiện vật đều có mã băm kép SHA-256 và BLAKE3 được đối chiếu bất biến trước và sau khi phân tích.
- QG-02: Báo cáo có đầy đủ nhật ký chuỗi lưu giữ (Chain of Custody) với mốc thời gian UTC chuẩn xác.
- QG-03: Tài liệu báo cáo cuối cùng được ký số toàn vẹn bằng chứng chỉ số hợp lệ.

## 10. Security & Safety Boundaries
- Bảo vệ nghiêm ngặt tính bảo mật của hồ sơ bằng chứng; lưu trữ tệp trong phân vùng mã hóa AES-256 có kiểm soát quyền truy cập.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Hoạt động phân tích hoàn toàn hợp pháp, minh bạch và có sự ủy quyền chính thức từ chủ sở hữu hệ thống.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Sổ cái chuỗi bằng chứng pháp lý `FORENSIC_EVIDENCE_CHAIN.json`.
1. Báo cáo thẩm định kỹ thuật có ký điện tử `TECHNICAL_EVIDENCE_REPORT.pdf`.

## 13. Related & Complementary Skills
- [`dex-pe-elf-structure-inspection`](.agents/skills/dex-pe-elf-structure-inspection/SKILL.md)
- [`dex-disassembly-cfg-reconstruction`](.agents/skills/dex-disassembly-cfg-reconstruction/SKILL.md)
- [`dex-security-audit`](.agents/skills/dex-security-audit/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Doanh nghiệp tiến hành thẩm tra độc lập để giải quyết tranh chấp mã nguồn với đối tác gia công. Kỹ sư kích hoạt `dex-reverse-evidence-chain` để tiếp nhận 4 tệp nhị phân, lập mã băm kép, ghi lại toàn bộ log phân tích trong môi trường air-gapped và xuất biên bản bằng chứng đạt chuẩn pháp lý, giúp hai bên giải quyết tranh chấp một cách minh bạch.
