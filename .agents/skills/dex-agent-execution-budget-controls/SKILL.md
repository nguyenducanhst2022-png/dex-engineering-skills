---
name: dex-agent-execution-budget-controls
description: Enforce strict resource budget limits on autonomous AI agent execution. Bound token consumption, tool-calling loop counts, wall-clock durations, and API expenditures. Use when preventing runaway agent loops and controlling inference costs.
---

# dex-agent-execution-budget-controls

## 1. Purpose & Scope
Thiết lập và thực thi các giới hạn ngân sách tài nguyên nghiêm ngặt (Resource Budget Limits) cho các tác nhân AI tự động; kiểm soát trần chi phí suy luận (Token Consumption Budgets); giới hạn số vòng lặp gọi công cụ tối đa (Tool-Call Loop Bounds); thiết lập ngưỡng thời gian chạy thực tế (Wall-Clock Timeout); và ngăn chặn hiện tượng vòng lặp vô tận (Runaway Agent Loops).

## 2. When to Use
- Khi triển khai các tác nhân tự trị chạy giải quyết các bài toán kỹ thuật phức tạp trong nhiều bước liên tiếp.
- Khi cần bảo đảm một tác nhân gặp lỗi logic không tự động gọi API hàng nghìn lần làm cạn kiệt ngân sách OpenAI/Anthropic.
- Khi thiết lập hạn mức chi phí (Cost Quotas) cho từng đầu việc hoặc từng kỹ sư trong đội ngũ.

## 3. When NOT to Use
- Khi tác vụ là một câu hỏi đơn giản một lần trả lời (Single-turn QA) không có vòng lặp suy nghĩ nhiều bước.
- Khi quá trình chạy đang thực hiện sao lưu hoặc migration khẩn cấp cần được ưu tiên hoàn thành bằng mọi giá.

## 4. Prerequisites & Input Context
- **Đồng hồ đo lường:** Khả năng đếm số lượng token input/output và chi phí ước tính theo từng model.
- **Bộ đếm bước lặp:** Biến đếm `step_count` tăng dần sau mỗi lần agent nhận phản hồi từ môi trường.

## 5. Core Concepts & Taxonomy
- **Runaway Agent Loop:** Tình trạng agent bị kẹt giữa 2 bước suy nghĩ, liên tục gọi cùng một công cụ với cùng một tham số dù lệnh đó liên tục trả về kết quả lỗi.
- **Token Budget Ceiling:** Ngưỡng token tối đa được phép tiêu thụ trong một phiên (ví dụ: tối đa 500,000 tokens cho một feature request).
- **Graceful Termination on Budget Exhaustion:** Khi chạm ngưỡng ngân sách, agent không bị crash đột ngột mà được chuyển sang trạng thái dừng an toàn, lưu lại các thay đổi đã làm và thông báo rõ nguyên nhân dừng lại cho người dùng.

## 6. Step-by-Step Execution Workflow
1. Khởi tạo đối tượng ngân sách thực thi (`ExecutionBudget`) với các tham số: `max_steps = 25`, `max_tokens = 200_000`, `timeout_seconds = 300`.
2. Trước mỗi bước suy luận: Kiểm tra thời gian đã trôi qua so với `timeout_seconds`; nếu vượt quá, kích hoạt ngắt phiên.
3. Sau mỗi lượt phản hồi từ mô hình: Cộng dồn `prompt_tokens` và `completion_tokens` vào ngân sách đã dùng.
4. Sau mỗi lần gọi tool: Tăng `step_count` lên 1 và kiểm tra tính lặp lại (nếu 3 bước liên tiếp gọi cùng một tool với cùng tham số bị lỗi, kích hoạt cảnh báo Loop Detection).
5. Khi chạm 90% ngân sách: Inject cảnh báo vào ngữ cảnh của agent yêu cầu tổng hợp kết quả dở dang và dừng lại.
6. Khi chạm 100% ngân sách: Ngắt hoàn toàn vòng lặp thực thi và xuất bản báo cáo chi phí minh bạch.

## 7. Concrete Examples
### Lớp quản lý ngân sách và phát hiện vòng lặp vô tận cho Agent:
```python
import time
from typing import Dict, Any, List

class ExecutionBudgetExhausted(Exception):
    pass

class AgentBudgetTracker:
    def __init__(self, max_steps: int = 25, max_tokens: int = 200_000, timeout_sec: float = 300.0):
        self.max_steps = max_steps
        self.max_tokens = max_tokens
        self.timeout_sec = timeout_sec
        self.start_time = time.monotonic()
        self.current_steps = 0
        self.total_tokens = 0
        self.tool_history: List[str] = []

    def record_step(self, tokens_used: int, tool_name: str = None, tool_args: str = None):
        self.current_steps += 1
        self.total_tokens += tokens_used
        elapsed = time.monotonic() - self.start_time

        # 1. Kiem tra Wall-clock Timeout
        if elapsed > self.timeout_sec:
            raise ExecutionBudgetExhausted(f"Timeout: Chay qua {self.timeout_sec}s.")

        # 2. Kiem tra Step Count
        if self.current_steps > self.max_steps:
            raise ExecutionBudgetExhausted(f"Step Limit: Vuot qua {self.max_steps} buoc.")

        # 3. Kiem tra Token Ceiling
        if self.total_tokens > self.max_tokens:
            raise ExecutionBudgetExhausted(f"Token Budget: Vuot qua {self.max_tokens} tokens.")

        # 4. Phat hien vong lap vo tan (Loop Detection)
        if tool_name:
            sig = f"{tool_name}:{tool_args}"
            self.tool_history.append(sig)
            if len(self.tool_history) >= 3 and self.tool_history[-3:] == [sig, sig, sig]:
                raise ExecutionBudgetExhausted(f"Runaway Loop: Cong cu {tool_name} bi goi lap 3 lan.")
```

## 8. Anti-Patterns & Common Traps
- **Infinite While Loop:** Viết vòng lặp agent `while True:` mà không có bất kỳ điều kiện dừng cứng nào về số bước hoặc thời gian.
- **Ignoring Failed API Responses in Loop:** Bỏ qua lỗi 429 Rate Limit hoặc lỗi logic của tool, tiếp tục retry ngay lập tức mà không có exponential backoff khiến ngân sách bị đốt cháy trong vài giây.
- **Silent Budget Extension:** Tự động tăng gấp đôi ngân sách mà không hỏi ý kiến người dùng khi agent sắp chạm ngưỡng giới hạn.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: 100% các phiên chạy của tác nhân AI đều có giới hạn bước tối đa (`max_steps <= 50`).
- **QG-02**: Có cơ chế phát hiện và chặn đứng vòng lặp lặp lại (Loop Detection) sau tối đa 3 lần lặp cùng hành vi.
- **QG-03**: Khi dừng do hết ngân sách, toàn bộ các tệp dở dang được giữ ở trạng thái nhất quán và có báo cáo nguyên nhân rõ ràng.

## 10. Security & Safety Boundaries
- Chống tấn công làm cạn kiệt tài nguyên tài chính (Denial of Wallet / Resource Exhaustion) và ngăn chặn agent gây nghẽn máy trạm.

## 11. Platform Adapters
- **Engines**: LangGraph StateGraph, AutoGen, CrewAI, Custom Loop Runners, OpenCode Agent Framework.

## 12. Deliverables & Output Artifacts
- Module quản lý ngân sách thực thi (`budget_tracker.py`).
- Bảng cấu hình hạn mức tài nguyên theo từng loại tác vụ (`budget_policies.json`).
- Báo cáo tổng hợp số lượng token, chi phí và thời gian chạy sau mỗi phiên.

## 13. Related & Complementary Skills
dex-agent-engineering, dex-tool-error-recovery-policy, dex-agent-shutdown-and-cancellation

## 14. Realistic Usage Example
```bash
# Chay agent voi ngan sach nghiem ngat 15 buoc va toi da 100k tokens
python -m agent.runner --task "Fix issue #12" --max-steps 15 --max-tokens 100000

# Chay kiem thu unit test co che ngat ngan sach
pytest tests/test_agent_budget_controls.py -v
```
