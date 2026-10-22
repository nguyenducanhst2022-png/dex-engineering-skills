---
name: dex-static-analysis-rule-authoring
description: Design, test, and tune custom static analysis rules (AST matching, Semgrep, ESLint custom rules, CodeQL) to catch architectural violations, API misuse, and security anti-patterns with near-zero false positives. Use when enforcing custom repo patterns or deprecating risky APIs.
---

# dex-static-analysis-rule-authoring

## 1. Purpose & Scope
Thiết kế, kiểm thử và tinh chỉnh các quy tắc Static Analysis tùy chỉnh (dựa trên Abstract Syntax Tree - AST, Semgrep, ESLint custom plugins, CodeQL queries) nhằm tự động hóa việc phát hiện các vi phạm kiến trúc, lạm dụng API nội bộ và các anti-pattern bảo mật trước khi code được review hoặc merge.

## 2. When to Use
- Cần ngăn chặn việc sử dụng API nội bộ không an toàn hoặc đã bị deprecated trong codebase lớn.
- Thiết lập quy chuẩn kiến trúc (ví dụ: cấm import direct Database layer từ Presentation layer).
- Tự động hóa kiểm tra các lỗ hổng phổ biến mang tính đặc thù của dự án mà scanner mặc định không bắt được.

## 3. When NOT to Use
- Không dùng khi quy tắc có thể giải quyết đơn giản bằng TypeScript type checker hoặc linter có sẵn.
- Không dùng để kiểm tra tính đúng đắn về mặt logic nghiệp vụ khi runtime (cần integration test).
- Không dùng cho việc format mã nguồn (dùng Prettier/Black/Biome).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- File mã nguồn mẫu chứa đoạn code vi phạm (negative fixtures) và code hợp lệ (positive fixtures).
- Đặc tả ngữ nghĩa của API hoặc kiến trúc cần cưỡng chế.
- Công cụ static analysis mục tiêu (Semgrep, ESLint, Python AST).
- **Điều kiện tiên quyết**:
- Môi trường có cài đặt công cụ phân tích (ví dụ: `semgrep` CLI hoặc `@eslint/rule-tester`).
- Bộ fixtures kiểm thử được cô lập rõ ràng.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Phân tích AST (Abstract Syntax Tree) so với Regex matching thông thường: AST hiểu cấu trúc ngữ cảnh ngữ pháp của ngôn ngữ, tránh các false positive do chú thích hoặc chuỗi ký tự.
- Tỉ lệ False Positive vs False Negative: Quy tắc tĩnh hữu dụng phải có tỉ lệ false positive gần như bằng 0 để các kỹ sư không bỏ qua cảnh báo.
- **Quy tắc quyết định kỹ thuật**:
- Nếu pattern xuất hiện trong hơn 50 file hiện tại: tạo autofix đi kèm quy tắc.
- Nếu quy tắc có độ phức tạp phân tích luồng dữ liệu (taint analysis): sử dụng Semgrep Pro/CodeQL thay vì linter AST cơ bản.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Viết quy tắc quá rộng khiến hàng trăm file vô tội bị báo lỗi làm nghẽn CI.
- Bỏ qua các trường hợp alias import (`import { riskyFunc as safeFunc }`).

## 6. Step-by-Step Execution Workflow
1. Thu thập tối thiểu 3 mẫu code vi phạm thực tế và 3 mẫu code hợp lệ tương đương.
2. Viết biểu thức AST pattern hoặc Semgrep YAML definition.
3. Chạy kiểm thử trên test fixtures và đo thời gian thực thi (phải dưới 100ms/file).
4. Tích hợp quy tắc vào CI pipeline dưới chế độ warning trước khi kích hoạt blocking error.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```yaml
rules:
  - id: ban-direct-db-import-in-controller
    languages: [typescript]
    message: 'Không được import Prisma client trực tiếp trong Controllers. Hãy dùng Service layer.'
    severity: ERROR
    pattern: import { $PRISMA } from '@prisma/client'
    paths:
      include:
        - 'src/controllers/**/*.ts'
```

### Lệnh xác minh & thực thi:
```bash
semgrep --config rules/custom-rules.yaml tests/fixtures/static-analysis/
```

## 8. Anti-Patterns & Common Traps
- Dùng Regex thô ráp thay vì AST parser để phân tích cú pháp ngôn ngữ lập trình.
- Không tạo negative test fixtures dẫn đến false positives tràn lan.

## 9. Quality Gates & Acceptance Criteria
- Quy tắc phải bắt được 100% negative fixtures và 0% positive fixtures trong test suite.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Quy tắc phân tích tĩnh phải chạy hoàn toàn offline, không gửi mã nguồn lên server bên thứ ba.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ thống hỗ trợ**: Linux (CI/CD runners), macOS, Windows 11 PowerShell/WSL2.

## 12. Deliverables & Output Artifacts
- File định nghĩa quy tắc (`.semgrep.yml` hoặc plugin file).
- Bộ test suite fixtures chứng minh độ chính xác.

## 13. Related & Complementary Skills
dex-sast-finding-triage, dex-code-review-excellence, dex-architecture-design

## 14. Realistic Usage Example
### Tình huống thực tế:
Một dự án phát hiện nhiều lập trình viên gọi `db.queryRawUnsafe()` trong Controllers thay vì đi qua Repository. Chuyên gia thiết kế rule Semgrep chặn hoàn toàn pattern này tại pre-commit hook và CI.
