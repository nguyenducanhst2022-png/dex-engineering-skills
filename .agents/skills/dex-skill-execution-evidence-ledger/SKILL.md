---
name: dex-skill-execution-evidence-ledger
description: Establish tamper-evident JSONL execution evidence ledgers recording real terminal commands, exit codes, stdout/stderr captures, and cryptographic checksums for skill quality validation. Use when producing verifiable proof of work and enforcing zero-hallucination compliance.
---

# dex-skill-execution-evidence-ledger

## 1. Purpose & Scope
Thiết lập sổ cái bằng chứng thực thi chống giả mạo (Tamper-Evident Execution Evidence Ledger) định dạng JSONL; ghi nhận trung thực các câu lệnh terminal thực tế, mã thoát (Exit Codes), dữ liệu đầu ra stdout/stderr và mã băm mật mã chứng minh chất lượng hoàn thành của kỹ năng; phục vụ việc cung cấp bằng chứng nghiệm thu có thể kiểm chứng độc lập và triệt tiêu hoàn toàn thói quen tuyên bố hoàn thành dựa trên ảo giác.

## 2. When to Use
- Sau mỗi lần AI Agent hoàn thành một tác vụ kỹ thuật và cần cung cấp bằng chứng nghiệm thu cho người dùng.
- Khi kiểm toán chất lượng của các kỹ năng trong kho để đảm bảo kỹ năng đã được chạy thật chứ không phải chỉ là văn bản lý thuyết.
- Khi lưu trữ hồ sơ bằng chứng phục vụ kiểm định chất lượng phần mềm ISO/IEC 25010.

## 3. When NOT to Use
- Khi Agent chỉ trả lời các câu hỏi tư vấn mang tính lý thuyết không có thao tác kỹ thuật thực tế.
- Khi ghi nhật ký log gỡ lỗi tạm thời trên màn hình console.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Thư mục lưu trữ bằng chứng `.system_generated/logs/` hoặc thư mục artifacts, tiện ích tính mã băm SHA-256.
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; bảo vệ toàn vẹn tài sản kỹ nghệ và dữ liệu sản xuất.

## 5. Core Concepts & Taxonomy
- **Zero Fake Completion Guarantee:** Cấm tuyệt đối việc Agent tuyên bố 'Đã kiểm thử thành công' mà không đưa ra được câu lệnh terminal thực tế kèm exit code 0.
- **Tamper-Evident Hash Chaining:** Mỗi bản ghi bằng chứng trong sổ cái JSONL chứa mã băm của bản ghi liền trước (tương tự Blockchain), đảm bảo nhật ký không thể bị chỉnh sửa hay xóa bớt.
- **Verifiable Terminal Output:** Lưu trữ nguyên văn chuỗi byte đầu ra của terminal để người dùng có thể đối chiếu và chạy lại xác minh bất cứ lúc nào.

## 6. Step-by-Step Execution Workflow
1. Mỗi khi Agent chạy một lệnh qua terminal, trích xuất mã thoát `exitCode`, dữ liệu `stdout` và `stderr`.
2. Tính toán mã băm SHA-256 của chuỗi kết quả thực thi.
3. Đóng gói bản ghi bằng chứng kèm dấu thời gian UTC và mã định danh nhiệm vụ.
4. Ghi nối tiếp (Append-only) bản ghi vào tệp sổ cái `execution_evidence.jsonl`.
5. Trích dẫn trực tiếp mã bằng chứng (Evidence ID) vào phần báo cáo hoàn thành gửi cho người dùng.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```json
{
  "evidenceId": "EV-20261022-9901",
  "skillId": "dex-acceptance-testing",
  "command": "pytest tests/test_skill_structure.py -v",
  "exitCode": 0,
  "stdoutSnippet": "collected 301 items\ntests/test_skill_structure.py::test_skill_count PASSED [100%]",
  "stderrSnippet": "",
  "executionDurationMs": 840,
  "timestampUtc": "2026-10-22T15:30:00.412Z",
  "sha256Hash": "4a5e1e8...b3"
}
```

## 8. Anti-Patterns & Common Traps
- Tuyên bố 'Đã kiểm thử toàn bộ 300 kỹ năng đều vượt qua 100%' nhưng khi kiểm tra lại thì không hề có lệnh nào được chạy trong terminal.
- Cố tình che giấu các thông báo lỗi `stderr` hoặc sửa mã thoát từ 1 thành 0 trong báo cáo.
- Xóa tệp nhật ký thực thi cũ để che giấu các lần chạy thử nghiệm bị thất bại.

## 9. Quality Gates & Acceptance Criteria
- QG-01: 100% các tuyên bố hoàn thành tác vụ kỹ thuật đều đi kèm bản ghi bằng chứng thực thi trong sổ cái.
- QG-02: Toàn bộ các lệnh kiểm chứng nghiệm thu đều có mã thoát exit code bằng 0.
- QG-03: Sổ cái bằng chứng JSONL tuân thủ cấu trúc schema và duy trì chuỗi mã băm liên tục.

## 10. Security & Safety Boundaries
- Không ghi các thông tin nhạy cảm (như mật khẩu truyền qua tham số dòng lệnh) vào sổ cái bằng chứng công khai.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Sổ cái bằng chứng thực thi chống giả mạo `execution_evidence.jsonl`.
1. Bản báo cáo bằng chứng nghiệm thu có thể kiểm chứng `VERIFIABLE_PROOF_OF_WORK.md`.

## 13. Related & Complementary Skills
- [`dex-code-verification`](.agents/skills/dex-code-verification/SKILL.md)
- [`dex-reverse-evidence-chain`](.agents/skills/dex-reverse-evidence-chain/SKILL.md)
- [`dex-acceptance-testing`](.agents/skills/dex-acceptance-testing/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Trong quá trình nâng cấp framework, AI Agent báo cáo đã hoàn thành việc kiểm thử toàn bộ các kỹ năng. Người dùng yêu cầu bằng chứng minh bạch. Agent kích hoạt `dex-skill-execution-evidence-ledger`, trích xuất bản ghi JSONL ghi nhận lệnh chạy `pytest tests/` kèm exit code 0 và thời gian chạy 0.88s, cung cấp bằng chứng thuyết phục 100% không thể nghi ngờ.
