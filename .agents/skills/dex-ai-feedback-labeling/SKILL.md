---
name: dex-ai-feedback-labeling
description: Design human-in-the-loop AI feedback collection pipelines, preference dataset curations (RLHF/DPO), and inter-annotator agreement metrics. Use when continuously aligning production LLMs or evaluating model generations with human graders.
---

# dex-ai-feedback-labeling

## 1. Purpose & Scope
Thiết kế và vận hành quy trình thu thập phản hồi của con người (Human-in-the-loop AI Feedback); chuẩn hóa bộ dữ liệu ưu tiên cặp đôi (Pairwise Preference Datasets cho DPO/RLHF), xử lý bất đồng giữa các người gán nhãn, và đo lường độ tin cậy thẩm định qua các chỉ số Inter-Annotator Agreement (Cohen's Kappa, Fleiss' Kappa).

## 2. When to Use
- Khi thu thập phản hồi từ người dùng thực tế (Thumbs Up/Down, Edit response) trên ứng dụng AI đang chạy sản xuất.
- Khi xây dựng bộ dữ liệu đánh giá chất lượng mô hình nội bộ phục vụ tinh chỉnh (Fine-tuning / Alignment).
- Khi phát hiện sự mâu thuẫn lớn giữa các chuyên gia đánh giá và cần quy chuẩn hóa bộ hướng dẫn gán nhãn (Annotation Guidelines).

## 3. When NOT to Use
- Khi tác vụ có thể đánh giá tự động 100% bằng kiểm thử phần mềm xác định (như cú pháp JSON, biên dịch code).
- Khi không có người gán nhãn con người và chỉ sử dụng mô hình LLM khác để chấm điểm (LLM-as-a-judge).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Cặp câu trả lời được sinh ra từ các mô hình khác nhau ($y_w$ và $y_l$), bộ tiêu chí đánh giá (Rubric), công cụ gán nhãn (Label Studio, Argilla).
- **Quyền hạn truy cập:** Quyền lưu trữ và xử lý dữ liệu phản hồi người dùng.

## 5. Core Concepts & Taxonomy
- **Pairwise Preference ($y_w \succ y_l$):** Đánh giá so sánh trực tiếp giữa hai câu trả lời cho cùng một câu hỏi, xác định câu trả lời nào được con người ưa thích hơn ($y_w$: chosen, $y_l$: rejected).
- **Inter-Annotator Agreement (Cohen's Kappa / Fleiss' Kappa):** Chỉ số thống kê đo lường mức độ đồng thuận giữa các chuyên gia đánh giá, loại trừ yếu tố trùng hợp ngẫu nhiên (chỉ số $\kappa > 0.6$ là đạt yêu cầu).
- **Feedback Loop Quality Gates:** Cơ chế loại bỏ các dữ liệu gán nhãn kém chất lượng (ví dụ: người đánh giá chọn bừa trong dưới 2 giây).

## 6. Step-by-Step Execution Workflow
1. Soạn thảo bộ tài liệu hướng dẫn gán nhãn chi tiết (Annotation Guidelines) với các tiêu chí định lượng: Độ chính xác, Tính an toàn, Mức độ hữu ích và Tính ngắn gọn.
2. Thu thập các cặp phản hồi từ môi trường sản xuất hoặc chạy A/B test giữa 2 model checkpoints.
3. Phân bổ các cặp dữ liệu cho tối thiểu 2 người đánh giá độc lập (đối với các mẫu quan trọng).
4. Tính toán chỉ số đồng thuận Fleiss' Kappa: nếu $\kappa < 0.6$, tổ chức họp giải quyết bất đồng và làm rõ lại hướng dẫn gán nhãn.
5. Chuẩn hóa dữ liệu đã đạt đồng thuận thành định dạng DPO tiêu chuẩn: `{'prompt': ..., 'chosen': ..., 'rejected': ...}`.
6. Đóng gói bộ dữ liệu huấn luyện và đưa vào pipeline tinh chỉnh mô hình định kỳ.

## 7. Concrete Examples
### Ví dụ tính toán chỉ số đồng thuận Cohen's Kappa trong Python:
```python
from sklearn.metrics import cohen_kappa_score

def evaluate_annotator_agreement(grader_1_labels: list[int], grader_2_labels: list[int]) -> dict:
    # 1: Prefer Model A, 2: Prefer Model B, 0: Tie
    kappa = cohen_kappa_score(grader_1_labels, grader_2_labels)
    
    status = "ACCEPTABLE"
    if kappa < 0.4:
        status = "POOR_AGREEMENT_NEEDS_GUIDELINE_REVIEW"
    elif kappa < 0.6:
        status = "MODERATE_AGREEMENT"
    else:
        status = "EXCELLENT_AGREEMENT"

    return {
        "cohen_kappa": round(kappa, 4),
        "total_samples": len(grader_1_labels),
        "agreement_status": status
    }
```

## 8. Anti-Patterns & Common Traps
- **Vague Guidelines:** Cung cấp hướng dẫn chung chung như 'Hãy chọn câu trả lời hay hơn', khiến mỗi người hiểu một kiểu và tạo ra dữ liệu nhiễu loạn.
- **Ignoring Rater Fatigue:** Bắt người đánh giá làm việc 8 tiếng liên tục không nghỉ, dẫn tới chất lượng gán nhãn tụt dốc vào cuối ngày.
- **Unbalanced Preference Datasets:** Chỉ thu thập các mẫu người dùng chê (Negative feedback) mà không có mẫu khen, làm mất cân bằng dữ liệu huấn luyện DPO.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Bộ hướng dẫn gán nhãn (Rubric) được ban hành chính thức kèm ví dụ mẫu trước khi bắt đầu thu thập dữ liệu.
- **QG-04**: Chỉ số Inter-Annotator Agreement Fleiss' Kappa đạt tối thiểu 0.65 trên tập mẫu kiểm định chéo.
- **QG-06**: 100% dữ liệu phản hồi người dùng được làm sạch thông tin PII trước khi đưa vào tập dataset công khai.

## 10. Security & Safety Boundaries
- Tuân thủ quy định quyền riêng tư: người dùng phải có quyền từ chối (opt-out) việc sử dụng dữ liệu hội thoại của họ cho mục đích huấn luyện AI.
- Ẩn danh hóa người đánh giá và người dùng trong toàn bộ tập dữ liệu phản hồi.

## 11. Platform Adapters
- **Tools**: Label Studio, Argilla, Prodigy, HuggingFace Datasets.
- **Format**: DPO JSONL format, RLHF Comparison format.

## 12. Deliverables & Output Artifacts
- Tài liệu hướng dẫn đánh giá (Annotation Rubric Guidelines).
- Bộ dữ liệu cặp ưu tiên chuẩn hóa (Chosen vs Rejected DPO dataset).
- Báo cáo phân tích chỉ số đồng thuận Inter-Annotator Agreement.

## 13. Related & Complementary Skills
dex-llm-evaluation-dataset-design, dex-llm-human-review-gates, dex-multimodal-evaluation

## 14. Realistic Usage Example
```powershell
# Tính toán chỉ số đồng thuận giữa các người đánh giá trên file dữ liệu
python scripts/compute_kappa_agreement.py --input annotations.jsonl
```
