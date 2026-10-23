---
name: dex-agent-output-reproducibility
description: Design, benchmark, and enforce reproducibility standards in autonomous AI agent outputs. Pin random seeds, record tool execution traces, freeze mock input fixtures, and explain nondeterministic variations. Use when building regression test suites for AI agents.
---

# dex-agent-output-reproducibility

## 1. Purpose & Scope
Thiết kế, đo lường và thực thi các chuẩn mực về tính tái lập (Reproducibility) trong kết quả đầu ra của tác nhân AI; cố định hạt giống ngẫu nhiên (Seed Pinning); ghi nhận và lưu trữ toàn bộ vết thực thi của công cụ (Tool Traces); đóng băng các bộ dữ liệu kiểm thử giả lập (Mock Input Fixtures); và giải trình minh bạch sự khác biệt giữa các lần chạy không tất định (Nondeterministic Variations).

## 2. When to Use
- Khi xây dựng bộ kiểm thử hồi quy (Regression Test Suites) cho các AI Coding Agents.
- Khi cần đánh giá xem một thay đổi trong system prompt có thực sự cải thiện khả năng viết code hay chỉ là sự may mắn ngẫu nhiên.
- Khi bàn giao kết quả của agent cho khách hàng doanh nghiệp đòi hỏi bằng chứng kiểm toán tính nhất quán của thuật toán.

## 3. When NOT to Use
- Khi agent hoạt động trong chế độ sáng tạo tự do (Creative Ideation / Brainstorming) đòi hỏi tính bất ngờ và đa dạng cao.
- Khi các công cụ phụ thuộc vào dữ liệu thời gian thực biến đổi liên tục (như giá chứng khoán trực tiếp hoặc thời tiết).

## 4. Prerequisites & Input Context
- **Hỗ trợ của Model Provider:** Khả năng cấu hình tham số `seed` và `temperature = 0.0` trong lệnh gọi LLM API.
- **Môi trường giả lập (Hermetic Environment):** Toàn bộ các lệnh gọi mạng và filesystem đều có thể mock hoặc snapshot lại.

## 5. Core Concepts & Taxonomy
- **Seed Pinning:** Gửi cùng một số nguyên `seed` tới OpenAI/Anthropic API để mô hình cố gắng sinh ra cùng một chuỗi token khi nhận cùng một prompt.
- **VCR/Replay Pattern:** Ghi lại toàn bộ request và response của các tool vào tệp fixture (Cassette) trong lần chạy đầu tiên, và phát lại (replay) trong các lần chạy sau mà không cần thực thi lệnh thật.
- **Behavioral Equivalence vs Lexical Equivalence:** Đánh giá tính tái lập dựa trên tính tương đương về mặt hành vi (cùng giải quyết được bài toán, cùng pass test) thay vì bắt buộc từng ký tự code phải giống hệt nhau.

## 6. Step-by-Step Execution Workflow
1. Cấu hình tham số mô hình cố định: `temperature: 0.0`, `seed: 42`.
2. Thiết lập cơ chế ghi vết (Execution Trace Recorder) lưu lại: Prompt đầu vào, các bước suy luận, các lệnh gọi tool và kết quả trả về của tool.
3. Khởi tạo kho lưu trữ cassette kiểm thử (`tests/fixtures/agent_cassettes/`).
4. Chạy tác vụ kiểm thử và so sánh kết quả với bản ghi cơ sở (Gold Baseline Trace).
5. Nếu có sự phân kỳ (Divergence): Phân tích xem sự khác biệt xuất phát từ việc LLM chọn đường đi khác hay do tool trả về dữ liệu không đồng nhất.
6. Xuất bản báo cáo chỉ số tái lập (Reproducibility Score) dựa trên tỷ lệ vượt qua bài test và mức độ tương đồng hành vi.

## 7. Concrete Examples
### Cấu hình kiểm thử agent có tính tái lập với Seed và Cassette Replay:
```python
import os
import json
import pytest

class ReproducibleAgentTestRunner:
    def __init__(self, cassette_path: str, record_mode: bool = False):
        self.cassette_path = cassette_path
        self.record_mode = record_mode
        self.cassette = {}
        if os.path.exists(cassette_path) and not record_mode:
            with open(cassette_path, "r", encoding="utf-8") as f:
                self.cassette = json.load(f)

    def execute_mocked_tool(self, tool_name: str, args: dict) -> str:
        key = f"{tool_name}:{json.dumps(args, sort_keys=True)}"
        if self.record_mode:
            # Chay tool that va ghi lai ket qua
            res = self._real_tool_call(tool_name, args)
            self.cassette[key] = res
            return res
        else:
            # Tra ve ket qua da ghi tu truoc de bao dam tinh tai lap 100%
            if key not in self.cassette:
                raise KeyError(f"Cassette miss for tool call: {key}")
            return self.cassette[key]

    def _real_tool_call(self, name: str, args: dict) -> str:
        return f"MOCKED_OUTPUT_FOR_{name}"
```

## 8. Anti-Patterns & Common Traps
- **High Temperature in Regression Benchmarks:** Chạy kiểm thử đánh giá agent với `temperature = 0.7` hoặc `1.0`, khiến kết quả bài test lúc pass lúc fail hoàn toàn do xác suất ngẫu nhiên.
- **Unpinned External Tools:** Cho phép agent gọi tool truy vấn internet trực tiếp trong test runner, khiến kết quả kiểm thử thay đổi khi trang web bên ngoài cập nhật.
- **Overly Strict String Matching:** Khẳng định code sinh ra phải trùng khớp từng khoảng trắng với mẫu chuẩn, dẫn đến các false positive failures khi logic hoàn toàn đúng.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: 100% các bài kiểm thử hồi quy của agent đều cấu hình `temperature: 0.0` và cố định `seed`.
- **QG-02**: Toàn bộ các lệnh gọi tool ngoại vi trong test suite đều sử dụng dữ liệu giả lập đóng băng (Hermetic Fixtures).
- **QG-03**: Chỉ số tương đương hành vi (Behavioral Equivalence Score) đạt ít nhất 95% qua 5 lần chạy liên tiếp.

## 10. Security & Safety Boundaries
- Bảo đảm tính đáng tin cậy của các hệ thống tự động hóa và ngăn ngừa việc chấp thuận các bản vá ngẫu nhiên không có căn cứ.

## 11. Platform Adapters
- **Frameworks**: VCR.py, pytest-recording, OpenAI Seed Parameter, LangSmith Datasets.

## 12. Deliverables & Output Artifacts
- Khung kiểm thử tính tái lập của agent (`reproducible_runner.py`).
- Bộ dữ liệu fixtures mẫu đã được đóng băng (`fixtures/agent_traces/*.json`).
- Báo cáo phân tích độ ổn định kết quả qua các phiên bản mô hình.

## 13. Related & Complementary Skills
dex-agent-engineering, dex-agent-trajectory-diffing, dex-llm-eval-benchmark-contamination

## 14. Realistic Usage Example
```bash
# Ghi lai cassette cho mot tinh huong kiem thu agent moi
python -m pytest tests/test_agent_reproducibility.py --record-mode

# Chay kiem thu hoi quy agent voi che do replay khong ton phi API
python -m pytest tests/test_agent_reproducibility.py -v
```
