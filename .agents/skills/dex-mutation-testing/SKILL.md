---
name: dex-mutation-testing
description: Evaluate test suite effectiveness by injecting controlled faults (mutations) into source code to verify whether existing tests catch them, identifying assertion weaknesses. Use when improving high-risk system test suites beyond superficial code coverage metrics.
---

# dex-mutation-testing

## 1. Purpose & Scope
Đánh giá chất lượng thực tế của bộ unit test bằng cách cấy các lỗi giả lập (mutations: đổi toán tử, đảo điều kiện boolean, xóa lệnh gọi hàm) vào source code nhằm kiểm chứng xem test suite có phát hiện và fail (kill mutant) hay không, vượt qua nhược điểm đánh lừa của line coverage thông thường.

## 2. When to Use
- Bộ kiểm thử đạt >80% line coverage nhưng vẫn để lọt lỗi ngớ ngẩn lên production.
- Các module tài chính, thanh toán, phân quyền hoặc tính toán logic cốt lõi cần độ tin cậy tuyệt đối.
- Cần xác định các test assertions rỗng hoặc test case vô bổ.

## 3. When NOT to Use
- Không chạy mutation testing trên toàn bộ codebase monorepo lớn mà không có diff/incremental filter vì thời gian chạy rất lâu.
- Không dùng cho code chỉ chứa boilerplate getters/setters/DTOs.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Source code của module cần kiểm tra.
- Bộ test suite hiện có của module đó.
- Cấu hình công cụ mutation testing (`mutmut` cho Python, `Stryker` cho JS/TS, `PITest` cho Java).
- **Điều kiện tiên quyết**:
- Tất cả unit tests hiện tại phải đang PASS 100% trước khi bắt đầu đột biến.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Mutation Score = (Killed Mutants / Total Mutants) * 100.
- Survived Mutant: Lỗi cấy vào mã nguồn nhưng test suite vẫn PASS => Test assertion yếu hoặc thiếu test case biên.
- **Quy tắc quyết định kỹ thuật**:
- Nếu Mutation Score < 75% trên module cốt lõi: từ chối merge PR cho đến khi bổ sung assertion.
- Với các mutant sống sót do dead code: loại bỏ dead code thay vì viết test thừa.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Chạy mutation testing gây infinite loop do đột biến biến đếm vòng lặp (cần cấu hình timeout an toàn cho mỗi test runner).

## 6. Step-by-Step Execution Workflow
1. Chạy test suite cơ sở để đảm bảo 100% test xanh.
2. Cấu hình mutation runner cho các tệp đã sửa đổi trong PR (incremental mutation).
3. Sinh ra mutants và thực thi test suite cho từng mutant.
4. Phân tích danh sách Survived Mutants và bổ sung assertions thích hợp.
5. Xuất báo cáo Mutation Score.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```json
// stryker.config.json
{
  "mutate": ["src/core/pricing-calculator.ts"],
  "testRunner": "jest",
  "reporters": ["html", "clear-text"],
  "thresholds": { "high": 85, "low": 75, "break": 70 }
}
```

### Lệnh xác minh & thực thi:
```bash
npx stryker run
# Hoặc cho Python:
mutmut run --paths-to-mutate=src/payment/
```

## 8. Anti-Patterns & Common Traps
- Chỉ tin tưởng vào 100% line coverage mà không kiểm tra độ sâu của assertion.
- Bỏ qua timeout dẫn đến CI treo vô tận khi mutant tạo vòng lặp vô hạn.

## 9. Quality Gates & Acceptance Criteria
- Mutation Score đạt tối thiểu 80% đối với các module thanh toán và bảo mật.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Chỉ thực thi mutation testing trong môi trường sandbox với tài nguyên CPU/RAM được giới hạn.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ thống hỗ trợ**: Linux (CI/CD runners), macOS, Windows 11 PowerShell/WSL2.

## 12. Deliverables & Output Artifacts
- Báo cáo HTML/JSON về tỉ lệ đột biến bị tiêu diệt.
- PR cập nhật các test assertions bổ sung.

## 13. Related & Complementary Skills
dex-coverage-risk-analysis, dex-unit-testing, dex-formal-invariant-checks

## 14. Realistic Usage Example
### Tình huống thực tế:
Một hàm tính lãi suất đạt 95% line coverage. Sau khi chạy Stryker, phát hiện mutant đổi `>` thành `>=` vẫn không làm test fail. Đội ngũ kỹ sư đã bổ sung test case tại đúng giá trị ngưỡng biên.
