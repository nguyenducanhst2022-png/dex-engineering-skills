---
name: dex-llm-eval-benchmark-contamination
description: Detect, evaluate, and mitigate benchmark data contamination in LLM evaluation suites. Generate synthetic mutations, audit pre-training data leakage, and establish verifiable held-out test sets. Use when benchmarking coding agent capabilities.
---

# dex-llm-eval-benchmark-contamination

## 1. Purpose & Scope
Phát hiện, đánh giá và triệt tiêu hiện tượng ô nhiễm dữ liệu kiểm thử (Benchmark Data Contamination) trong các bộ benchmark đánh giá tác nhân AI; tạo lập các biến thể đột biến tổng hợp (Synthetic Mutations) để kiểm tra khả năng suy luận thực sự; phát hiện nguy cơ rò rỉ đề thi vào tập huấn luyện trước (Pre-training Data Leakage); và thiết lập các bộ kiểm thử độc lập được bảo vệ nghiêm ngặt (Verifiable Held-out Test Sets).

## 2. When to Use
- Khi đánh giá năng lực viết code của một mô hình AI mới trên các bài toán chuẩn (HumanEval, SWE-bench, MBPP) mà nghi ngờ mô hình đã học vẹt đáp án.
- Khi xây dựng bộ đề kiểm tra năng lực kỹ thuật nội bộ của doanh nghiệp để tuyển chọn hoặc tinh chỉnh mô hình AI.
- Khi cần chứng minh tính trung thực và khách quan của kết quả benchmark trước hội đồng thẩm định kỹ thuật.

## 3. When NOT to Use
- Khi bài kiểm tra chỉ nhằm xác nhận kết nối API hoạt động bình thường (Smoke Test).
- Khi ứng dụng sử dụng mô hình cho các tác vụ dịch thuật hoặc tóm tắt thông thường không liên quan đến giải toán logic phức tạp.

## 4. Prerequisites & Input Context
- **Bộ dữ liệu Benchmark:** Tập các bài toán lập trình kèm kịch bản kiểm thử đầu vào/đầu ra mẫu.
- **Công cụ Đột biến Cú pháp (AST Mutator):** Khả năng phân tích cú pháp mã nguồn và đổi tên biến, đảo ngược điều kiện logic, hoặc hoán đổi cấu trúc thuật toán.

## 5. Core Concepts & Taxonomy
- **Data Contamination / Memorization:** Hiện tượng mô hình ngôn ngữ lớn ghi nhớ nguyên văn đề bài và lời giải của các benchmark phổ biến do dữ liệu benchmark này nằm công khai trên internet và bị cào vào tập huấn luyện trước của mô hình.
- **Synthetic Semantic Mutation:** Phương pháp giữ nguyên bản chất bài toán nhưng thay đổi toàn bộ tên biến, cốt truyện nghiệp vụ, thứ tự tham số và cấu trúc dữ liệu để kiểm tra xem mô hình thực sự hiểu thuật toán hay chỉ học vẹt chuỗi ký tự.
- **Canary Strings:** Chuỗi ký tự mật mã đặc biệt (như GUID) được nhúng bí mật vào tệp benchmark; nếu chuỗi này xuất hiện trong dữ liệu huấn luyện, ta chứng minh được benchmark đã bị rò rỉ.

## 6. Step-by-Step Execution Workflow
1. Rà soát bộ benchmark hiện tại để phát hiện các bài toán quá phổ biến (như Fibonacci, Two Sum, FizzBuzz) có nguy cơ ô nhiễm 100%.
2. Áp dụng công cụ biến đổi ngữ nghĩa: Sinh ra 3 biến thể đột biến (Mutants) cho mỗi bài toán (thay đổi kiểu dữ liệu, đổi logic từ tăng dần sang giảm dần, bọc trong ngữ cảnh nghiệp vụ mới).
3. Đưa đề bài gốc và đề bài đột biến cho mô hình giải quyết.
4. So sánh tỷ lệ giải thành công: Nếu mô hình giải đúng 100% đề bài gốc nhưng thất bại hoàn toàn trên đề bài đột biến có cùng độ phức tạp, khẳng định mô hình bị ô nhiễm dữ liệu và học vẹt.
5. Xây dựng tập kiểm thử độc quyền (Held-Out Evaluation Suite) không bao giờ tải lên internet công cộng để phục vụ việc đánh giá lâu dài.

## 7. Concrete Examples
### Script biến đổi đột biến bài toán lập trình để kiểm tra hiện tượng học vẹt:
```python
import ast
import random

class CodeProblemMutator(ast.NodeTransformer):
    def __init__(self):
        self.var_map = {}

    def visit_Name(self, node):
        # Doi ten bien de tranh viec LLM nho ten bien quen thuoc trong tap train
        if isinstance(node.ctx, (ast.Store, ast.Load)) and not node.id.startswith("__"):
            if node.id not in self.var_map:
                self.var_map[node.id] = f"var_{random.randint(1000, 9999)}"
            node.id = self.var_map[node.id]
        return node

def mutate_code_sample(source_code: str) -> str:
    tree = ast.parse(source_code)
    mutator = CodeProblemMutator()
    mutated_tree = mutator.visit(tree)
    ast.fix_missing_locations(mutated_tree)
    return ast.unparse(mutated_tree)
```

## 8. Anti-Patterns & Common Traps
- **Evaluating Only on Public Standard Benchmarks:** Tuyên bố mô hình đạt 95% năng lực lập trình chỉ dựa trên HumanEval trong khi mô hình không thể giải quyết các bài toán nội bộ đơn giản.
- **Publishing Evaluation Datasets Publicly:** Tải toàn bộ tệp test case lên GitHub công khai không khóa bản quyền, khiến các công ty AI cào dữ liệu này vào tập huấn luyện của thế hệ mô hình tiếp theo.
- **Ignoring Performance Drops on Inverted Logic:** Bỏ qua việc mô hình giải được bài toán tìm số lớn nhất nhưng viết sai hoàn toàn khi đổi yêu cầu sang tìm số nhỏ nhất.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Bộ đánh giá benchmark bắt buộc phải bao gồm ít nhất 30% các bài toán đột biến ngữ nghĩa (Synthetic Mutants).
- **QG-02**: Độ chênh lệch hiệu năng (Performance Gap) giữa bài toán gốc và bài toán đột biến không được vượt quá 15%.
- **QG-03**: Mọi tệp dữ liệu kiểm thử nội bộ đều được gán nhãn Canary String để theo dõi nguy cơ rò rỉ.

## 10. Security & Safety Boundaries
- Bảo đảm tính liêm chính của các phép đo lường khoa học và ngăn chặn việc ra quyết định kiến trúc dựa trên số liệu ảo.

## 11. Platform Adapters
- **Tools**: Cleanlab, SWE-bench Harness, Inspect AI, Promptfoo, Custom AST Mutators.

## 12. Deliverables & Output Artifacts
- Bộ benchmark mã nguồn đột biến chống học vẹt (`mutated_benchmarks.json`).
- Báo cáo phân tích mức độ ô nhiễm dữ liệu của mô hình (`contamination_report.md`).
- Công cụ tự động tạo biến thể kiểm thử từ mã nguồn thực tế.

## 13. Related & Complementary Skills
dex-agent-output-reproducibility, dex-agent-trajectory-diffing, dex-skill-quality-scorecards

## 14. Realistic Usage Example
```bash
# Chay danh gia do nhiem du lieu tren bo test suite cua agent
python scripts/detect_benchmark_contamination.py --dataset evals/coding_tasks.json

# Phat sinh cac bien the dot bien tu dong
python scripts/generate_mutant_evals.py --input raw_tasks/ --output mutated_tasks/
```
