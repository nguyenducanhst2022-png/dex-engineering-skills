---
name: dex-superpowers-adapter
description: Disciplined software engineering workflows, Test-Driven Development (TDD) loops, systematic defect isolation, and Git worktree isolation adapter. Bridges DEX engineering practices to Superpowers methodologies under strict Master Orchestrator control. Use when executing complex TDD cycles, structured plan executions, or worktree development.
version: 8.1.0
group: Integration
domain: Developer Workflow & Quality Automation
upstream_source: https://github.com/obra/superpowers
upstream_commit: 2ce8aa15d05bd57213e6f746f953aafb7ded7a8b
---

# DEX Superpowers Workflow & TDD Automation Adapter

## 1. Purpose & Scope
Cung cấp bộ quy trình kỹ thuật kỷ luật cao và tự động hóa phát triển phần mềm dựa trên phương pháp luận của **Superpowers** (`obra/superpowers`). Adapter này tích hợp các quy trình Test-Driven Development (TDD) nghiêm ngặt (Red-Green-Refactor), kỹ thuật cô lập lỗi có hệ thống (Systematic Debugging), phương thức thực thi kế hoạch theo danh mục kiểm tra nguyên tử (Atomic Checklists), và cơ chế quản lý không gian làm việc cô lập bằng Git Worktrees.

**Giới Hạn Tối Cao (Root Orchestrator Invariant)**:
Adapter này **TUYỆT ĐỐI KHÔNG** được phép thay thế hoặc chiếm quyền điều phối của `dex-master-orchestrator`. Quy trình `using-superpowers` từ upstream bị cô lập ở mức sub-workflow cấp dưới. Mọi quyết định định tuyến, phân loại ý định, đánh giá rủi ro và xác thực chất lượng cuối cùng đều do `dex-master-orchestrator` nắm giữ.

---

## 2. When to Use
Kích hoạt adapter này khi:
- Người dùng yêu cầu phát triển một tính năng mới theo chuẩn TDD nghiêm ngặt (viết test kiểm chứng thất bại trước khi viết code triển khai).
- Cần thực hiện quy trình Systematic Debugging trên một lỗi phức tạp khó tái lập, đòi hỏi dựng kịch bản kiểm chứng tối thiểu (minimal reproduction harness).
- Cần cô lập các nhánh tính năng song song bằng Git Worktrees mà không làm xáo trộn không gian làm việc chính của kho mã nguồn.
- Cần phân rã một kế hoạch phức tạp thành danh sách kiểm tra từng bước có đánh dấu trạng thái (`[ ]` → `[x]`) kèm bằng chứng kiểm chứng sau mỗi bước nhỏ.

---

## 3. When NOT to Use
Tuyệt đối không kích hoạt adapter này khi:
- Tác vụ là chỉnh sửa nhỏ lẻ (quick bugfix, cập nhật tài liệu, chỉnh sửa 1 dòng code) — nên dùng `QUICK MODE` với `dex-development-workflow`.
- Khi môi trường máy chủ là kho mã nguồn shallow clone (`--depth 1`) hoặc hệ thống CI/CD không hỗ trợ tạo Git Worktree.
- Khi người dùng muốn giao toàn quyền điều phối khởi tạo dự án cho meta-router bên ngoài mà không qua `dex-master-orchestrator`.
- Khi tác vụ là phân tích bảo mật nhị phân hoặc dịch ngược mã nguồn (chuyển sang `dex-binary-inspection` hoặc `dex-rea-adapter`).

---

## 4. Prerequisites & Input Context
1. **Kiểm tra môi trường Git**:
   ```bash
   # Kiểm tra tính khả dụng của Git và tính năng Worktree
   git --version
   git worktree list
   ```
2. **Khung kiểm thử hiện hữu**: Dự án phải có ít nhất một test runner hoạt động được (ví dụ `pytest`, `vitest`, `jest`, `cargo test`, `go test`).
3. **Trạng thái không gian làm việc**: Không còn các tệp chưa theo dõi (untracked files) gây xung đột trong thư mục làm việc chính trước khi tạo worktree.
4. **Quy tắc Zero-Hallucination**: Nếu môi trường không hỗ trợ worktree (lỗi `fatal: not a git repository` hoặc shallow clone), adapter tự động chuyển về chế độ phân nhánh cục bộ (`git checkout -b`) mà không dừng tiến trình đột ngột.

---

## 5. Core Concepts & Taxonomy

```
+---------------------------------------------------------------------------------+
|                         SUPERPOWERS ENGINEERING RIGOR                          |
+---------------------------------------------------------------------------------+
| 1. TEST-DRIVEN DEVELOPMENT (TDD) LOOP                                           |
|    - RED: Viết test mô tả hành vi mong muốn -> Xác nhận test THẤT BẠI           |
|    - GREEN: Viết lượng code tối thiểu để test VƯỢT QUA                          |
|    - REFACTOR: Dọn dẹp mã nguồn, loại bỏ trùng lặp mà không làm test gãy       |
+---------------------------------------------------------------------------------+
| 2. SYSTEMATIC DEBUGGING                                                         |
|    - Hypothesize: Đưa ra 1 giả thuyết duy nhất về nguyên nhân gốc rễ           |
|    - Prove: Dựng bài test hoặc lệnh để chứng minh giả thuyết đúng              |
|    - Isolate: Loại bỏ các biến số phụ để cô lập phạm vi ảnh hưởng               |
+---------------------------------------------------------------------------------+
| 3. WORKTREE ISOLATION                                                           |
|    - Isolated Workspace: Mỗi nhánh chạy trên một thư mục đĩa riêng biệt         |
|    - Zero-Interference: Tránh làm bẩn node_modules hoặc __pycache__ của main    |
|    - Atomic Tear-down: Xóa worktree và prune sau khi hoàn thành hoặc hủy bỏ     |
+---------------------------------------------------------------------------------+
```

### Các khái niệm kỹ thuật:
- **Red-Green-Refactor Invariant**: Tuyệt đối không viết mã nguồn nghiệp vụ nếu chưa có một bài test thất bại phản ánh chính xác yêu cầu mới hoặc lỗi cần sửa.
- **Atomic Checklist**: Danh sách nhiệm vụ dạng Markdown với mỗi bước có tiêu chí kiểm chứng (verification criteria) cụ thể. Một bước chỉ được tích `[x]` khi bài test của bước đó chạy thành công trên terminal.
- **Git Worktree Isolation**: Cho phép checkout nhiều nhánh của cùng một repo vào các thư mục đĩa khác nhau cùng lúc, rất hữu ích khi các tác nhân AI thực thi nhiều luồng công việc song song.

---

## 6. Step-by-Step Execution Workflow

```
BƯỚC 1: Khởi tạo Kế hoạch Thực thi Kèm Danh mục Kiểm tra Nguyên tử
  │
BƯỚC 2: Kiểm tra Hạ tầng Git & Cấu hình Không gian Làm việc (Branch/Worktree)
  │
BƯỚC 3: Pha Đỏ (RED) — Viết Unit/Integration Test Thất Bại Có Chủ Đích
  │
BƯỚC 4: Pha Xanh (GREEN) — Triển khai Code Tối Thiểu để Test Vượt Qua
  │
BƯỚC 5: Pha Tinh chỉnh (REFACTOR) — Tối ưu Hóa Cấu trúc & Bảo toàn Test
  │
BƯỚC 6: Thu dọn Không gian Làm việc & Ghi nhận Bằng chứng Kiểm chứng
```

### Chi tiết các bước thực hiện:
1. **Bước 1 — Phân rã kế hoạch thành Atomic Checklist**:
   - Soạn thảo kế hoạch thực thi trong tệp nhiệm vụ. Mỗi bước nhỏ phải có: Tệp cần sửa, test cần chạy, tiêu chí hoàn thành.
2. **Bước 2 — Thiết lập không gian làm việc**:
   - Nếu được phép và hỗ trợ worktree: `git worktree add ../feature-worktree -b feat/task-name`.
   - Nếu không hỗ trợ: `git checkout -b feat/task-name`.
3. **Bước 3 — Pha Đỏ (RED Phase)**:
   - Viết bài kiểm thử tự động mới phản ánh đúng hành vi nghiệp vụ.
   - Chạy test runner và quan sát lỗi thất bại cụ thể (phải thất bại vì logic chưa có, không phải vì lỗi cú pháp import).
4. **Bước 4 — Pha Xanh (GREEN Phase)**:
   - Viết phần mã nguồn triển khai đơn giản nhất có thể để vượt qua bài test.
   - Chạy lại test runner và xác nhận bài test vừa viết chuyển sang trạng thái PASS.
5. **Bước 5 — Pha Tinh chỉnh (REFACTOR Phase)**:
   - Rà soát code smells, chuẩn hóa kiểu dữ liệu, tách hàm dài thành các hàm nhỏ.
   - Chạy lại toàn bộ test suite để đảm bảo không phát sinh hồi quy (regression).
6. **Bước 6 — Dọn dẹp & Xác nhận hoàn thành**:
   - Xóa worktree tạm nếu có: `git worktree remove ../feature-worktree` và `git worktree prune`.
   - Tạo commit nguyên tử tuân thủ Conventional Commits.

---

## 7. Concrete Examples

### Ví dụ 1: Quy trình TDD Red-Green chuẩn mực
*Bước 1: Viết test trước (RED)*
```python
# tests/test_token_bucket.py
import pytest
from core.rate_limiter import TokenBucketRateLimiter

def test_rate_limiter_allows_under_limit():
    limiter = TokenBucketRateLimiter(capacity=5, refill_rate_per_sec=1.0)
    assert limiter.acquire("client-1") is True

def test_rate_limiter_blocks_over_capacity():
    limiter = TokenBucketRateLimiter(capacity=2, refill_rate_per_sec=0.1)
    assert limiter.acquire("client-2") is True
    assert limiter.acquire("client-2") is True
    # Thất bại có chủ đích: Lần thứ 3 phải bị chặn
    assert limiter.acquire("client-2") is False
```

*Bước 2: Thực thi code để GREEN*
```python
# core/rate_limiter.py
import time

class TokenBucketRateLimiter:
    def __init__(self, capacity: int, refill_rate_per_sec: float):
        self.capacity = capacity
        self.refill_rate = refill_rate_per_sec
        self.tokens = capacity
        self.last_update = time.monotonic()

    def acquire(self, client_id: str) -> bool:
        now = time.monotonic()
        elapsed = now - self.last_update
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
        self.last_update = now
        
        if self.tokens >= 1.0:
            self.tokens -= 1.0
            return True
        return False
```

---

## 8. Anti-Patterns & Common Traps
- **Bẫy 1: TDD ngược (Viết code trước, viết test sau)**: Triển khai toàn bộ tính năng rồi mới viết bài test để xác nhận code đã chạy. Cách làm này triệt tiêu hoàn toàn giá trị của thiết kế hướng kiểm thử và thường bỏ lọt các trường hợp biên.
- **Bẫy 2: Chiếm quyền Master Orchestrator**: Để các hook từ `using-superpowers` tự ý thay đổi system prompt gốc hoặc tự ý điều hướng yêu cầu mà không thông qua bảng định tuyến chuẩn của DEX.
- **Bẫy 3: Bỏ quên Worktrees mồ côi (Orphaned Worktrees)**: Tạo thư mục worktree nhưng không xóa sau khi merge hoặc hủy bỏ, làm đầy ổ đĩa và khóa các nhánh git khỏi việc checkout lại.
- **Bẫy 4: Fake Green (Làm test xanh bằng cách comment assert)**: Sửa bài test để test vượt qua thay vì sửa đúng mã nguồn nghiệp vụ.

---

## 9. Quality Gates & Acceptance Criteria
- **QG-SP-01 (Red Verification Gate)**: Có bằng chứng terminal chứng minh test thất bại trước khi mã nguồn nghiệp vụ được cập nhật.
- **QG-SP-02 (Green Verification Gate)**: 100% các bài test liên quan đều vượt qua sau khi viết code mà không cần tắt bất kỳ kiểm tra nào.
- **QG-SP-03 (Zero Regression Gate)**: Toàn bộ bộ kiểm thử hồi quy của dự án vẫn vượt qua 100%.
- **QG-SP-04 (Worktree Cleanliness Gate)**: Lệnh `git worktree list` không để lại các đường dẫn tạm không hợp lệ hoặc bị hỏng.
- **QG-SP-05 (Checklist Completeness Gate)**: Toàn bộ danh mục kiểm tra nguyên tử trong kế hoạch đều được hoàn tất và có dẫn chứng lệnh chạy.

---

## 10. Security & Safety Boundaries
- **Cô lập không gian làm việc**: Worktrees chỉ được tạo bên trong thư mục quy định hoặc thư mục cha của kho lưu trữ, tuyệt đối không tạo ra các đường dẫn hệ thống nhạy cảm (như `C:\Windows`, `/etc`, thư mục gốc).
- **Phòng chống lệnh hủy hoại**: Không bao giờ thực thi `git worktree remove --force` khi còn các tệp chưa được lưu trữ hoặc commit an toàn.
- **Bảo toàn quyền điều phối**: Chặn đứng mọi nỗ lực từ upstream nhằm inject các system prompt tự động ghi đè cơ chế an toàn của DEX.

---

## 11. Platform Adapters
- **Git Native Platform**: Tương thích hoàn toàn với Git 2.20+ trên Windows, Linux và macOS.
- **Node.js / Python / Rust / Go**: Tương thích với mọi test runner chuẩn (`pytest`, `vitest`, `cargo test`, `go test`).
- **Graceful Fallback Mode**: Khi chạy trong môi trường không có quyền truy cập đĩa bên ngoài repo để tạo worktree, adapter chuyển tiếp tự động sang phân nhánh Git cục bộ tiêu chuẩn (`git checkout -b`).

---

## 12. Deliverables & Output Artifacts
1. **Execution Checklist**: Bản kế hoạch các bước TDD với trạng thái cập nhật thời gian thực.
2. **Test Suite**: Các tệp kiểm thử mới được tạo trong thư mục `tests/`.
3. **Implementation Code**: Mã nguồn đáp ứng hoàn toàn bài test đã định hình.
4. **Báo cáo kiểm thử TDD**: Lịch sử thực thi Red-Green-Refactor chứng minh tính đúng đắn của logic.

---

## 13. Related & Complementary Skills
- [`dex-master-orchestrator`](../../.agents/skills/dex-master-orchestrator/SKILL.md): Cội nguồn điều phối điều phối yêu cầu tới adapter.
- [`dex-development-workflow`](../../.agents/skills/dex-development-workflow/SKILL.md): Quy trình 7 bước phát triển phần mềm chuẩn tắc của DEX.
- [`dex-testing-engineering`](../../.agents/skills/dex-testing-engineering/SKILL.md): Kỹ nghệ kiểm thử tự động, biên soạn kịch bản và phân tích độ bao phủ.
- [`dex-root-cause-debugging`](../../.agents/skills/dex-root-cause-debugging/SKILL.md): Phương pháp phân tích nguyên nhân gốc rễ và xử lý lỗi phần mềm.
- [`dex-git-workflow`](../../.agents/skills/dex-git-workflow/SKILL.md): Quản trị phiên bản Git và quy chuẩn commit nguyên tử.

---

## 14. Realistic Usage Example

### Tình huống thực tế:
Kỹ sư yêu cầu: *"Áp dụng quy trình TDD để bổ sung tính năng tự động làm mới JWT token khi còn dưới 60 giây hết hạn, sử dụng worktree cô lập để thực hiện."*

### Các lệnh kiểm tra và thực thi:
```bash
# 1. Kiểm tra tính khả dụng của worktree
git worktree list

# 2. Khởi tạo nhánh cô lập (hoặc fallback checkout)
git checkout -b feat/jwt-auto-refresh

# 3. Pha ĐỎ (RED) - Chạy test kiểm chứng thất bại
pytest tests/test_jwt_refresh.py -k "test_token_refreshes_when_expiring_soon"
# Kết quả mong đợi: FAILED (assert token_refreshed is True, got False)

# 4. Triển khai code nghiệp vụ trong auth_manager.py
# 5. Pha XANH (GREEN) - Chạy lại test kiểm chứng thành công
pytest tests/test_jwt_refresh.py -k "test_token_refreshes_when_expiring_soon"
# Kết quả mong đợi: 1 passed in 0.05s

# 6. Pha TINH CHỈNH (REFACTOR) & Hồi quy toàn bộ
pytest tests/
# Kết quả mong đợi: 100% passed
```
