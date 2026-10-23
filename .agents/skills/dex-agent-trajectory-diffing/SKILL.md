---
name: dex-agent-trajectory-diffing
description: Compare, visualize, and analyze execution trajectories between different agent runs, prompt versions, or foundation models. Isolate reasoning divergence points, tool-calling regressions, and efficiency bottlenecks. Use when evaluating agent upgrades.
---

# dex-agent-trajectory-diffing

## 1. Purpose & Scope
So sánh, trực quan hóa và phân tích sự sai lệch giữa các quỹ đạo thực thi (Execution Trajectories) của tác nhân AI qua các lần chạy khác nhau, giữa các phiên bản prompt hoặc giữa các mô hình nền tảng; cô lập chính xác điểm phân kỳ suy luận (Reasoning Divergence Point); phát hiện các bước đi thụt lùi (Regressions) trong việc lựa chọn công cụ; và đo lường hiệu quả giải quyết vấn đề.

## 2. When to Use
- Khi nâng cấp system prompt của agent và cần biết chính xác agent đã thay đổi cách tiếp cận bài toán như thế nào.
- Khi chuyển đổi mô hình từ GPT-4 sang Claude 3.5 Sonnet hoặc ngược lại và cần đánh giá sự khác biệt về chuỗi tool calls.
- Khi một bài kiểm thử của agent bị thất bại và cần so sánh với quỹ đạo thành công trong quá khứ để tìm ra bước rẽ sai.

## 3. When NOT to Use
- Khi tác vụ chỉ là một bước đơn lẻ (Single-turn Call) không có chuỗi quỹ đạo nhiều bước.
- Khi kết quả đầu ra cuối cùng bị hỏng do lỗi cú pháp cơ bản có thể phát hiện bằng linter thông thường.

## 4. Prerequisites & Input Context
- **Tệp vết quỹ đạo (Trajectory Logs):** Định dạng lưu vết chuẩn tắc chứa chuỗi các sự kiện: `[Thought, Tool Call, Observation]` kèm timestamp và token counts.
- **Công cụ so sánh Diff:** Khả năng so sánh cấu trúc cây JSON hoặc đồ thị các bước đi.

## 5. Core Concepts & Taxonomy
- **Trajectory Divergence Point:** Bước đầu tiên trong chuỗi hành động mà Agent B đưa ra quyết định hoặc gọi công cụ khác biệt so với Agent A khi đối mặt cùng một ngữ cảnh trước đó.
- **Wasted Exploration Steps:** Các bước agent đi vào ngõ cụt (như đọc nhầm tệp, chạy lệnh lỗi nhiều lần rồi mới quay đầu), làm tăng chi phí và thời gian chạy.
- **Structural AST Diffing of Tool Calls:** So sánh ngữ nghĩa của tham số gọi công cụ thay vì chỉ so sánh chuỗi văn bản thô.

## 6. Step-by-Step Execution Workflow
1. Thu thập tệp log quỹ đạo chuẩn của lần chạy mẫu (Baseline Trajectory A) và lần chạy mới (Candidate Trajectory B).
2. Chuẩn hóa chuỗi hành động thành danh sách các bước có cấu trúc: `Step(index, thought_summary, tool_name, tool_args, status)`.
3. Duyệt tuần tự từ bước 1: So sánh `tool_name` và `tool_args` giữa hai quỹ đạo.
4. Xác định điểm phân kỳ đầu tiên: Ghi nhận ngữ cảnh dẫn đến quyết định khác biệt của Candidate.
5. Đánh giá chất lượng phân kỳ: Xác định xem ngã rẽ của Candidate là một cải tiến (ít bước hơn, hiệu quả hơn) hay là một lỗi thụt lùi (chọn nhầm công cụ, lặp bước vô ích).
6. Xuất bản báo cáo so sánh quỹ đạo dạng bảng Markdown kèm đồ thị trực quan hóa.

## 7. Concrete Examples
### Script so sánh quỹ đạo thực thi và tìm điểm phân kỳ giữa 2 lần chạy của Agent:
```python
import json
from typing import List, Dict, Any

def diff_trajectories(baseline_path: str, candidate_path: str) -> Dict[str, Any]:
    with open(baseline_path, "r", encoding="utf-8") as f:
        trace_a = json.load(f)["steps"]
    with open(candidate_path, "r", encoding="utf-8") as f:
        trace_b = json.load(f)["steps"]

    divergence_step = None
    min_len = min(len(trace_a), len(trace_b))

    for i in range(min_len):
        step_a = trace_a[i]
        step_b = trace_b[i]

        tool_a = step_a.get("tool_call", {}).get("name")
        tool_b = step_b.get("tool_call", {}).get("name")

        if tool_a != tool_b:
            divergence_step = {
                "step_index": i + 1,
                "baseline_choice": tool_a,
                "candidate_choice": tool_b,
                "reasoning_a": step_a.get("thought", "")[:100],
                "reasoning_b": step_b.get("thought", "")[:100],
            }
            break

    return {
        "baseline_total_steps": len(trace_a),
        "candidate_total_steps": len(trace_b),
        "step_delta": len(trace_b) - len(trace_a),
        "first_divergence": divergence_step
    }
```

## 8. Anti-Patterns & Common Traps
- **Comparing Raw Text Logs with git diff:** Dùng lệnh diff văn bản thông thường để so sánh hai tệp log, gây rối loạn bởi các thay đổi nhỏ về thời gian chạy hoặc UUID ngẫu nhiên.
- **Ignoring Wasted Exploration Steps:** Chỉ quan tâm đến việc agent có ra kết quả cuối cùng hay không mà bỏ qua việc agent mới tốn gấp 3 lần số bước và token so với bản cũ.
- **Declaring Superiority from Single Run:** Khẳng định một prompt mới vượt trội chỉ dựa trên việc so sánh 1 cặp quỹ đạo duy nhất mà không đo lường trung bình trên tập kiểm thử.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Tệp log quỹ đạo phải lưu đầy đủ cặp `tool_call` và `observation` có cấu trúc JSON hợp lệ.
- **QG-02**: Báo cáo so sánh phải chỉ rõ vị trí bước phân kỳ đầu tiên và lý do dẫn đến sự phân kỳ.
- **QG-03**: Phiên bản prompt mới không được làm tăng số bước thừa (Wasted Steps) quá 10% so với baseline.

## 10. Security & Safety Boundaries
- Giúp phát hiện sớm các hành vi bất thường, gọi tool ngoài dự kiến hoặc xu hướng bị jailbreak của agent khi nâng cấp mô hình.

## 11. Platform Adapters
- **Tools**: LangSmith, Phoenix Arize, OpenInference, Traceloop, Weights & Biases Weave.

## 12. Deliverables & Output Artifacts
- Công cụ so sánh quỹ đạo agent tự động (`trajectory_diff.py`).
- Báo cáo phân tích sai lệch bước đi và hiệu quả tài nguyên (`trajectory_diff_report.md`).
- Biểu đồ dòng thời gian trực quan hóa các ngã rẽ suy luận.

## 13. Related & Complementary Skills
dex-agent-output-reproducibility, dex-agent-execution-budget-controls, dex-agent-engineering

## 14. Realistic Usage Example
```bash
# So sanh quy dao giua lan chay cu va moi tren cung mot bai toan
python scripts/diff_trajectories.py traces/run_v1.json traces/run_v2.json

# Xuat bao cao markdown ve diem phan ky suy luan
python scripts/diff_trajectories.py --format markdown --output docs/evals/diff_report.md
```
