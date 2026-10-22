---
name: dex-formal-invariant-checks
description: Specify, model, and verify critical domain invariants using stateful property-based testing and formal assertion contracts. Use when guaranteeing correctness in financial ledgers, cryptographic protocols, and consensus mechanisms.
---

# dex-formal-invariant-checks

## 1. Purpose & Scope
Đặc tả, mô hình hóa và kiểm chứng các bất biến nghiệp vụ quan trọng (domain invariants) thông qua Stateful Property-based Testing và Assertion Contracts; đảm bảo rằng bất kể chuỗi hành động nào diễn ra, trạng thái của hệ thống vẫn luôn bảo toàn các quy tắc bất di bất dịch (ví dụ: tổng tiền trong sổ cái luôn cân bằng).

## 2. When to Use
- Phát triển hệ thống sổ cái tài chính, ví điện tử, sàn giao dịch.
- Xây dựng máy trạng thái hữu hạn (Finite State Machine) phức tạp.
- Cần chứng minh tính toàn vẹn dữ liệu trong các điều kiện xử lý đồng thời (concurrency).

## 3. When NOT to Use
- Không tuyên bố đây là 'chứng minh toán học tuyệt đối' (Formal Verification / Coq / TLA+) nếu chỉ chạy property-based testing.
- Không cần thiết cho các trang CRUD thông tin cá nhân đơn giản.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Danh sách các bất biến nghiệp vụ cốt lõi (Core Invariants).
- Mô hình máy trạng thái của thực thể.
- Bộ sinh chuỗi thao tác ngẫu nhiên (Hypothesis, fast-check).
- **Điều kiện tiên quyết**:
- Hệ thống có thể chuyển trạng thái thông qua các hàm/phương thức rõ ràng.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Invariant: Mệnh đề logic luôn đúng trước và sau bất kỳ thao tác hợp lệ nào (ví dụ: `Balance >= 0`, `Total Credits == Total Debits`).
- Stateful Testing: Sinh ra một chuỗi ngẫu nhiên các lệnh (Nạp -> Rút -> Khóa tài khoản -> Chuyển tiền) và kiểm tra bất biến sau mỗi bước.
- **Quy tắc quyết định kỹ thuật**:
- Nếu bất biến bị vi phạm tại bất kỳ chuỗi lệnh nào: framework phải tự động thu nhỏ chuỗi lệnh (Shrinking) thành chuỗi ngắn nhất để lập trình viên sửa lỗi.
- Nếu trạng thái không thể phục hồi: ném InvariantViolationException ngay lập tức.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Bỏ sót một nhánh trạng thái biên trong mô hình khiến lỗ hổng không được kiểm tra.

## 6. Step-by-Step Execution Workflow
1. Phỏng vấn chuyên gia nghiệp vụ để liệt kê các bất biến toán học và kế toán.
2. Viết State Machine Model đại diện bằng thư viện property testing (ví dụ: `hypothesis.stateful`).
3. Định nghĩa các quy tắc chuyển đổi trạng thái (Rules).
4. Chạy hàng vạn chuỗi thao tác ngẫu nhiên để tìm kiếm chuỗi phá vỡ bất biến.
5. Thu thập lỗi nhỏ nhất (shrunk example) và tạo regression test.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```python
from hypothesis.stateful import RuleBasedStateMachine, rule, invariant

class BankLedgerMachine(RuleBasedStateMachine):
    def __init__(self):
        super().__init__()
        self.ledger = Ledger()

    @rule(amount=st.integers(min_value=1, max_value=10000))
    def deposit(self, amount):
        self.ledger.deposit(amount)

    @invariant()
    def balance_must_equal_sum_of_transactions(self):
        assert self.ledger.get_balance() == sum(t.amount for t in self.ledger.transactions)
```

### Lệnh xác minh & thực thi:
```bash
pytest tests/stateful/test_ledger.py --hypothesis-seed=42
```

## 8. Anti-Patterns & Common Traps
- Nhầm lẫn giữa Unit Test (kiểm tra 1 input cụ thể) với Invariant Check (kiểm tra chân lý tổng quát).
- Bỏ qua bước kiểm tra invariant sau khi rollback giao dịch lỗi.

## 9. Quality Gates & Acceptance Criteria
- Kiểm chứng thành công tối thiểu 50,000 chuỗi chuyển đổi trạng thái ngẫu nhiên mà không vi phạm bất biến.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Invariant check phải áp dụng kiểm tra chống Race condition (TOCTOU) trong môi trường concurrency.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ thống hỗ trợ**: Linux (CI/CD runners), macOS, Windows 11 PowerShell/WSL2.

## 12. Deliverables & Output Artifacts
- Bộ mã nguồn Stateful Property-based Tests.
- Tài liệu đặc tả các bất biến nghiệp vụ chính thức.

## 13. Related & Complementary Skills
dex-unit-testing, dex-database-design, dex-mutation-testing

## 14. Realistic Usage Example
### Tình huống thực tế:
Một sàn giao dịch tiền điện tử áp dụng Stateful Invariant Testing cho hệ thống khớp lệnh. Sau 10,000 bước sinh lệnh ngẫu nhiên, họ phát hiện chuỗi: Đặt lệnh -> Hủy 1 phần -> Khớp lệnh -> Sửa giá làm số dư ví bị âm 0.00000001 do làm tròn số học.
