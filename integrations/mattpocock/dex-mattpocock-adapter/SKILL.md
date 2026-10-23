---
name: dex-mattpocock-adapter
description: Developer-agent collaboration protocols, hypothesis-driven bug diagnosis, specification-to-ticket decomposition, and structured session handoff adapter. Bridges DEX engineering practices to Matt Pocock agent skills. Use when diagnosing elusive bugs, decomposing features into atomic tickets, or handing off agent context.
version: 8.1.0
group: Integration
domain: Developer Productivity & Agent Collaboration
upstream_source: https://github.com/mattpocock/skills
upstream_commit: 5beb35b040e3de97e54fa9e386d7e42d15c295c2
---

# DEX Matt Pocock Developer Collaboration & Diagnosis Adapter

## 1. Purpose & Scope
Cung cấp cầu nối kỹ thuật giữa DEX Engineering Skills và repository **Matt Pocock Skills** (`mattpocock/skills`). Kỹ năng này chuẩn hóa các quy trình tương tác cấp cao giữa lập trình viên và tác nhân AI, bao gồm: phương pháp chẩn đoán lỗi dựa trên giả thuyết có thể kiểm chứng (Hypothesis-Driven Bug Diagnosis), kỹ thuật phân rã yêu cầu thành các thẻ công việc nguyên tử (Specification-to-Tickets Decomposition), giao thức bàn giao phiên làm việc không làm mất ngữ cảnh (Session Handoff & Writing for Agents), và quy trình thiết kế mô hình nghiệp vụ (Domain Modeling).

Phạm vi bao phủ:
1. Chuẩn hóa quy trình chẩn đoán lỗi: xây dựng harness tái lập tối thiểu, lập giả thuyết có thể bác bỏ (falsifiable hypothesis), và xác thực chứng minh trước khi sửa code.
2. Quy trình `to-tickets`: phân giải tài liệu đặc tả hoặc yêu cầu tính năng thành danh sách ticket kỹ thuật độc lập, khả thi, có tiêu chí nghiệm thu rõ ràng cho từng ticket.
3. Giao thức `handoff`: lưu trữ trạng thái phiên làm việc, quyết định kiến trúc, công việc còn lại và trở ngại vào tài liệu bàn giao chuẩn tắc (`handoff.md`).
4. Định hình hướng dẫn `writing-for-agents`: tối ưu hóa cách viết tài liệu kỹ thuật để các tác nhân AI đọc và xử lý chính xác nhất mà không gây hiểu lầm ngữ cảnh.

---

## 2. When to Use
Kích hoạt adapter này khi:
- Người dùng báo cáo một lỗi phức tạp, khó tái lập hoặc chập chờn (flaky bug) và cần chẩn đoán nguyên nhân gốc rễ theo phương pháp khoa học.
- Bắt đầu một tính năng lớn cần phân chia thành các thẻ công việc (atomic engineering tickets) trước khi phân bổ cho các tác nhân hoặc nhà phát triển khác nhau.
- Cần bàn giao phiên làm việc giữa các agent hoặc giữa agent và con người khi hết context window hoặc chuyển giao ca làm việc.
- Cần rà soát và cấu trúc lại tài liệu dự án để AI agents đọc hiểu dự án nhanh chóng và chính xác.

---

## 3. When NOT to Use
Tuyệt đối không kích hoạt adapter này khi:
- Tác vụ là thực thi truy vấn cơ sở dữ liệu Supabase hay tối ưu RLS (chuyển sang `dex-supabase-adapter`).
- Tác vụ thuần túy về tạo bảng màu, CSS hoặc typography (chuyển sang `dex-ui-ux-pro-max-adapter`).
- Tác vụ phân tích an ninh nhị phân hoặc dịch ngược (chuyển sang `dex-binary-inspection` hoặc `dex-rea-adapter`).
- Tác vụ yêu cầu điều phối tổng thể toàn bộ kho kỹ năng (chuyển quyền về `dex-master-orchestrator`).

---

## 4. Prerequisites & Input Context
1. **Mô tả lỗi hoặc đặc tả tính năng**: Báo cáo lỗi (stack trace, hành vi thực tế vs mong đợi) hoặc tài liệu yêu cầu (PRD, user story).
2. **Khung kiểm thử hiện tại**: Khả năng chạy lệnh kiểm thử để tạo harness tái lập lỗi tối thiểu.
3. **Môi trường tài liệu**: Thư mục `docs/` hoặc vị trí lưu trữ tài liệu bàn giao `handoff.md`.
4. **Kiểm tra công cụ thực tế (Runtime Tool Checks)**:
   ```bash
   # Kiểm tra node/npm nếu cần các tiện ích phụ trợ của Matt Pocock
   node --version
   npm --version
   ```
   *Quy tắc Zero-Hallucination*: Nếu thiếu các extension chuyên biệt của Claude Code hoặc plugin ngoài, adapter tự động chuyển sang chế độ mẫu quy trình Markdown chuẩn tắc (Pure Markdown Protocol) mà không bị phụ thuộc vào môi trường máy chủ.

---

## 5. Core Concepts & Taxonomy

```
+---------------------------------------------------------------------------------+
|                       MATT POCOCK COLLABORATION PARADIGM                        |
+---------------------------------------------------------------------------------+
| 1. HYPOTHESIS-DRIVEN BUG DIAGNOSIS                                              |
|    - Observe: Ghi nhận chính xác triệu chứng và sai lệch hành vi                |
|    - Minimal Repro: Dựng bài test tối thiểu chỉ chứa đúng đoạn code gây lỗi     |
|    - Falsifiable Hypothesis: Giả thuyết rõ ràng có thể chứng minh đúng/sai      |
|    - Prove Mutation: Chứng minh việc sửa đổi giải quyết đúng nguyên nhân gốc   |
+---------------------------------------------------------------------------------+
| 2. ATOMIC TICKET DECOMPOSITION (to-tickets)                                     |
|    - Independent: Mỗi ticket có thể triển khai và kiểm thử độc lập              |
|    - Explicit Contract: Input rõ ràng, output định hình trước                   |
|    - Acceptance Criteria: Tiêu chí nghiệm thu có thể tự động hóa               |
+---------------------------------------------------------------------------------+
| 3. STRUCTURED SESSION HANDOFF (handoff)                                         |
|    - Context Summary: Tóm tắt những gì đã hoàn thành                            |
|    - Key Decisions: Các quyết định kỹ thuật đã thống nhất                       |
|    - Next Immediate Steps: Hành động tiếp theo cho ca làm việc kế tiếp          |
|    - Known Blockers: Rủi ro hoặc trở ngại còn tồn đọng                          |
+---------------------------------------------------------------------------------+
```

### Các khái niệm kỹ thuật:
- **Minimal Reproduction Harness**: Đoạn mã kiểm thử ngắn gọn nhất có thể tái hiện lỗi mà không phụ thuộc vào toàn bộ hệ thống lớn hay mạng bên ngoài.
- **Atomic Engineering Ticket**: Một đơn vị công việc hoàn chỉnh có kích thước vừa đủ để một tác nhân AI giải quyết trong một chu kỳ ngữ cảnh duy nhất.
- **Context Handoff Contract**: Bản tóm lược có cấu trúc dạng Markdown giúp khôi phục toàn bộ trạng thái tư duy và định hướng kỹ thuật của tác nhân mà không cần đọc lại hàng nghìn dòng lịch sử hội thoại trước đó.

---

## 6. Step-by-Step Execution Workflow

```
BƯỚC 1: Tiếp nhận Vấn đề & Xác định Chế độ (Diagnosis / Tickets / Handoff)
  │
BƯỚC 2: [Nếu Diagnosis] Dựng Repro Tối Thiểu & Đặt Giả Thuyết Bác Bỏ Được
  │
BƯỚC 3: [Nếu to-tickets] Phân rã Tính năng Thành Các Thẻ Công Việc Nguyên Tử
  │
BƯỚC 4: [Nếu Handoff] Đóng Gói Trạng Thái Dự Án Vào handoff.md Chuẩn Tắc
  │
BƯỚC 5: Đánh giá Chất Lượng Đầu Ra & Bàn Giao Kiểm Chứng
```

### Chi tiết các bước thực hiện:
1. **Bước 1 — Phân loại tác vụ**:
   - Xác định rõ mục tiêu: Chẩn đoán lỗi hóc búa, phân chia tính năng lớn, hay bàn giao phiên làm việc.
2. **Bước 2 — Quy trình Chẩn đoán Lỗi (Diagnosing Bugs)**:
   - Dựng 1 test case tái lập lỗi với dữ liệu tĩnh tối thiểu.
   - Viết ra giả thuyết: *"Lỗi xảy ra do hàm X giả định mảng Y luôn có ít nhất 1 phần tử khi xử lý async"* thay vì đoán mò.
   - Đặt breakpoint hoặc log có mục tiêu để xác nhận hoặc bác bỏ giả thuyết.
   - Áp dụng bản vá tối thiểu và chứng minh test tái lập chuyển sang màu xanh.
3. **Bước 3 — Quy trình Phân rã Thẻ Công Việc (to-tickets)**:
   - Đọc kỹ tài liệu đặc tả yêu cầu.
   - Chia thành các ticket: Ticket 1 (Schema & Types), Ticket 2 (Core Logic & Unit Tests), Ticket 3 (API Endpoint), Ticket 4 (UI Integration).
   - Mỗi ticket bắt buộc có: Tệp tác động, Test cần chạy, Tiêu chuẩn hoàn thành.
4. **Bước 4 — Quy trình Bàn Giao Phiên (Session Handoff)**:
   - Soạn thảo `handoff.md` với các mục: Mục tiêu ban đầu, Những gì đã làm được, Quyết định kỹ thuật, Việc cần làm tiếp theo, Lệnh kiểm chứng hiện tại.
5. **Bước 5 — Xác thực đầu ra**:
   - Kiểm tra tài liệu tạo ra có chứa thông tin mơ hồ hay không; đảm bảo lập trình viên hoặc agent tiếp theo có thể bắt tay làm việc ngay lập tức.

---

## 7. Concrete Examples

### Ví dụ 1: Phiếu chẩn đoán lỗi tối thiểu (Minimal Reproduction Case)
```python
# reproduction/test_reproduce_null_tenant_leak.py
"""
MINIMAL REPRODUCTION HARNESS for Issue #402:
Hypothesis: When tenant_id header is missing, the auth middleware falls back to
DEFAULT_TENANT instead of rejecting the request with 401 Unauthorized.
"""
import pytest
from core.auth_middleware import resolve_tenant_context

def test_missing_tenant_header_must_raise_unauthorized():
    request_headers = {"Authorization": "Bearer valid_jwt_token"}
    
    # Giả thuyết: Hàm hiện tại trả về 'default_tenant' thay vì ném lỗi
    # Kiểm chứng: Test này thất bại trên code cũ, chứng minh lỗi tồn tại
    with pytest.raises(PermissionError, match="Missing X-Tenant-ID header"):
        resolve_tenant_context(request_headers)
```

### Ví dụ 2: Cấu trúc tệp Bàn giao Ngữ cảnh `handoff.md`
```markdown
# Session Handoff: JWT Refresh & Multi-Tenant Middleware

### Section 1: Goal & Current Status
- **Goal:** Hoàn thiện xác thực token JWT và cô lập tenant header.
- **Status:** Core middleware đã xong, đang viết integration test cho Edge cases.

### Section 2: Completed Items
- [x] Tạo `TokenBucketRateLimiter` với 100% test coverage (`tests/test_rate_limiter.py`).
- [x] Sửa lỗi rò rỉ tenant khi thiếu header trong `resolve_tenant_context`.

### Section 3: Immediate Next Steps
1. Mở tệp `tests/test_auth_integration.py`.
2. Bổ sung test case kiểm tra token hết hạn sau 3600 giây.
3. Chạy lệnh: `pytest tests/test_auth_integration.py -v`.

### Section 4: Key Architectural Decisions
- Sử dụng UUIDv7 cho `tenant_id` thay vì chuỗi ngẫu nhiên.
- Luôn kiểm tra header `X-Tenant-ID` trước khi giải mã JWT để tiết kiệm CPU.
```

---

## 8. Anti-Patterns & Common Traps
- **Bẫy 1: Sửa code mò mẫm (Shotgun Debugging)**: Thay đổi lung tung nhiều chỗ trong code mà không hiểu nguyên nhân gốc rễ, hy vọng code sẽ chạy.
- **Bẫy 2: Viết ticket quá lớn (Mega-Tickets)**: Gom toàn bộ tính năng backend + frontend + database vào một ticket duy nhất, khiến AI agent bị tràn ngữ cảnh và sinh code dở dang.
- **Bẫy 3: Bàn giao hời hợt (Lazy Handoff)**: Viết tóm tắt kiểu "Đã sửa xong một số lỗi, hãy tiếp tục làm" mà không cung cấp lệnh chạy cụ thể hoặc vị trí công việc dở dang.
- **Bẫy 4: Viết tài liệu kiểu văn học cho Agent**: Viết các đoạn văn dài mơ hồ thay vì dùng bullet points, code blocks và danh mục kiểm tra có cấu trúc.

---

## 9. Quality Gates & Acceptance Criteria
- **QG-MP-01 (Hypothesis Reproducibility)**: Có tệp test hoặc script tái lập lỗi tối thiểu chứng minh được sự tồn tại của lỗi trước khi can thiệp code.
- **QG-MP-02 (Atomic Ticket Independence)**: Mỗi ticket tạo ra từ `to-tickets` đều có thể giải quyết độc lập mà không bị vòng phụ thuộc lẫn nhau.
- **QG-MP-03 (Handoff Executability)**: Tệp `handoff.md` chứa đủ lệnh kiểm tra cụ thể để tác nhân kế tiếp có thể chạy và bắt đầu công việc trong vòng 30 giây.
- **QG-MP-04 (Specification Alignment)**: Toàn bộ tiêu chí nghiệm thu trong yêu cầu gốc đều được phản ánh đầy đủ trong các thẻ công việc.

---

## 10. Security & Safety Boundaries
- **Không nhúng dữ liệu người dùng thật vào Repro Case**: Khi tạo kịch bản tái lập lỗi, bắt buộc phải sử dụng dữ liệu giả lập (synthetic data/mock fixtures), tuyệt đối không copy PII từ production logs.
- **Bảo vệ khóa bí mật trong Handoff**: Tệp `handoff.md` tuyệt đối không được ghi các API keys, database passwords hoặc token bí mật còn hiệu lực.
- **Bảo toàn quy trình thẩm định mã nguồn**: Các ticket phân rã phải giữ nguyên các bước kiểm tra an ninh và rà soát lỗ hổng của DEX.

---

## 11. Platform Adapters
- **Markdown Universal Protocol**: Hoạt động không phụ thuộc môi trường trên bất kỳ editor hay AI agent nào (VS Code, Codex, Claude Code, Cursor).
- **Issue Trackers**: Có khả năng xuất các ticket sang định dạng GitHub Issues Markdown hoặc Jira format.
- **Testing Runtimes**: Tương thích với pytest, Jest, Vitest, Go test, Cargo test.

---

## 12. Deliverables & Output Artifacts
1. **Reproduction Script**: Tệp kiểm thử tối thiểu tái hiện lỗi `test_reproduce_<issue>.py`.
2. **Decomposed Tickets**: Tài liệu danh sách ticket `docs/tickets/<feature>-tickets.md`.
3. **Session Handoff Document**: Tệp `docs/handoff.md` cập nhật chi tiết trạng thái công việc.
4. **Changelog Evidence**: Bằng chứng chứng minh lỗi đã được khắc phục triệt để.

---

## 13. Related & Complementary Skills
- [`dex-master-orchestrator`](../../.agents/skills/dex-master-orchestrator/SKILL.md): Cội nguồn điều phối điều phối yêu cầu người dùng tới adapter.
- [`dex-root-cause-debugging`](../../.agents/skills/dex-root-cause-debugging/SKILL.md): Kỹ thuật phân tích nguyên nhân gốc rễ và triệt tiêu lỗi phần mềm.
- [`dex-specification-driven`](../../.agents/skills/dex-specification-driven/SKILL.md): Phương pháp luận phát triển hướng đặc tả (SDD).
- [`dex-task-delegation`](../../.agents/skills/dex-task-delegation/SKILL.md): Phân chia và ủy quyền nhiệm vụ kỹ thuật cho các tác nhân AI.
- [`dex-context-engineering`](../../.agents/skills/dex-context-engineering/SKILL.md): Quản trị bộ nhớ dự án và ngữ cảnh cho AI coding agents.

---

## 14. Realistic Usage Example

### Tình huống thực tế:
Kỹ sư yêu cầu: *"Chúng tôi nhận được phản ánh từ khách hàng rằng khi thanh toán giỏ hàng có trên 50 sản phẩm thì API trả về lỗi 500 ngẫu nhiên. Hãy dựng repro case, đưa ra giả thuyết và lập kế hoạch sửa."*

### Các lệnh kiểm tra và thực thi:
```bash
# 1. Dựng test case tái lập tối thiểu
cat << 'EOF' > tests/test_reproduce_cart_timeout.py
import pytest

def test_large_cart_payload_under_timeout():
    # Tạo payload 60 items giả lập
    payload = [{"id": f"item_{i}", "qty": 1, "price": 10.0} for i in range(60)]
    # Giả thuyết: Hàm calculate_totals thực hiện N truy vấn SQL tuần tự thay vì batch query
    # Khi n > 50, vượt quá 1000ms timeout
    from services.cart_service import calculate_totals
    res = calculate_totals(payload)
    assert res["status"] == "SUCCESS"
EOF

# 2. Chạy test tái lập
pytest tests/test_reproduce_cart_timeout.py -v
# Quan sát kết quả FAILED (Timeout > 1000ms), chứng minh lỗi tái lập thành công

# 3. Tạo ticket phân rã giải pháp
cat << 'EOF' > docs/tickets/cart-performance-tickets.md
# Tickets: Cart Checkout Performance Fix

### Ticket 1: Batch Item Price Lookup
- **Task:** Chuyển đổi N truy vấn `SELECT price FROM items WHERE id = ?` thành 1 truy vấn `SELECT id, price FROM items WHERE id IN (...)`.
- **Target File:** `services/cart_service.py`
- **Verification:** `pytest tests/test_reproduce_cart_timeout.py -v` (Must PASS under 100ms).
EOF

# 4. Xác nhận tạo ticket thành công
python -c "print('DIAGNOSIS_AND_TICKETS_COMPLETE: Repro harness and batch tickets generated.')"
```
