---
name: dex-semantic-routing-evaluations
description: Benchmark, evaluate, and optimize master orchestrator routing accuracy, intent classification, and fallback mechanisms across complex multi-skill user prompts. Use when maintaining high routing precision across hundreds of skills.
---

# dex-semantic-routing-evaluations

## 1. Purpose & Scope
Đo lường chuẩn đối sánh (Benchmark), đánh giá và tối ưu hóa độ chính xác định tuyến (Routing Accuracy), phân loại ý định (Intent Classification) và cơ chế dự phòng (Fallback) của Master Orchestrator; bảo đảm tỷ lệ định tuyến chính xác cao (Precision, Recall, F1 >= 0.85) trên danh mục gồm 400 kỹ năng chuyên môn.

## 2. When to Use
- Khi mở rộng số lượng kỹ năng từ 100 lên 400 và xuất hiện hiện tượng chồng lấn hoặc định tuyến sai lệch giữa các kỹ năng có ngữ cảnh tương tự.
- Khi người dùng gửi yêu cầu bằng tiếng Việt phức tạp hoặc kết hợp nhiều tác vụ đồng thời và cần phân rã thành chuỗi kỹ năng hợp lý.
- Khi kiểm toán chất lượng định tuyến định kỳ trong quy trình phát hành bản dựng mới.

## 3. When NOT to Use
- Khi hệ thống chỉ có dưới 5 kỹ năng đơn giản có ranh giới hoàn toàn tách biệt không có nguy cơ nhầm lẫn.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Bộ dữ liệu kiểm chứng định tuyến (Routing Benchmark Datasets) gồm các câu prompt thực tế và nhãn kỹ năng mục tiêu mong đợi, Master Orchestrator.
- **Quyền hạn truy cập:** Quyền chạy kịch bản đánh giá và cập nhật ma trận định tuyến.

## 5. Core Concepts & Taxonomy
- **F1 Score Benchmark:** Trung bình điều hòa giữa Độ chuẩn xác (Precision) và Độ bao phủ (Recall); tiêu chuẩn vàng đánh giá chất lượng mô hình phân loại định tuyến.
- **Progressive Disclosure:** Cơ chế Master Orchestrator tra cứu theo 2 tầng: Xác định nhóm chuyên môn cấp cao (40 Groups A-AN) trước, sau đó mới tra cứu chi tiết trong 10 kỹ năng của nhóm đó để tiết kiệm ngữ cảnh.
- **Confusion Matrix:** Bảng ma trận nhầm lẫn thể hiện rõ những cặp kỹ năng nào thường xuyên bị định tuyến nhầm sang nhau để tinh chỉnh lại từ khóa kích hoạt.

## 6. Step-by-Step Execution Workflow
1. Xây dựng bộ dữ liệu benchmark đa dạng bao gồm tối thiểu 40 kịch bản thực tế đại diện cho toàn bộ 40 nhóm chuyên môn.
2. Nạp câu prompt vào cơ chế phân tích định tuyến của Master Orchestrator.
3. So sánh kỹ năng được Orchestrator lựa chọn với nhãn mục tiêu chuẩn (Ground Truth).
4. Tính toán ma trận nhầm lẫn, điểm số Precision, Recall và F1-score tổng thể.
5. Nhận diện các điểm nghẽn: tinh chỉnh lại trường `description` và `when_use` của các kỹ năng bị nhầm lẫn.
6. Chặn đứng việc phát hành bản dựng nếu điểm F1-score tổng thể giảm xuống dưới ngưỡng 0.85.

## 7. Concrete Examples
### Kịch bản đánh giá độ chính xác định tuyến tự động trong Python:
```python
from sklearn.metrics import precision_recall_fscore_support
import json

def evaluate_routing_benchmark(test_cases: list[dict], routing_engine):
    y_true = []
    y_pred = []
    
    for case in test_cases:
        prompt = case["prompt"]
        expected_skill = case["expected_skill"]
        predicted_skill = routing_engine.route(prompt)
        
        y_true.append(expected_skill)
        y_pred.append(predicted_skill)
        
    precision, recall, f1, _ = precision_recall_fscore_support(y_true, y_pred, average='weighted', zero_division=0)
    print(f"=== KET QUA EVALUATION ROUTING ===")
    print(f"Weighted Precision: {precision:.4f}")
    print(f"Weighted Recall:    {recall:.4f}")
    print(f"Weighted F1-Score:  {f1:.4f}")
    
    assert f1 >= 0.85, f"CANH BAO: F1-score ({f1:.4f}) thap hon tieu chuan toi thieu 0.85!"
    return f1
```

## 8. Anti-Patterns & Common Traps
- **Overlapping Vague Descriptions:** Đặt mô tả kỹ năng quá chung chung khiến Orchestrator luôn chọn sai một kỹ năng duy nhất cho mọi câu hỏi.
- **Single Keyword Matching:** Chỉ dựa vào một từ khóa duy nhất (như 'docker') thay vì hiểu toàn bộ ý định ngữ cảnh của người dùng.
- **Testing Only on Training Prompts:** Đánh giá định tuyến trên chính những câu prompt đã dùng để viết mô tả kỹ năng dẫn tới hiện tượng quá khớp (Overfitting).

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Điểm F1-Score định tuyến trên bộ benchmark 40 kịch bản đạt tối thiểu >= 0.85.
- **QG-04**: Tỷ lệ định tuyến chính xác nhóm chuyên môn (Group-level routing) đạt >= 95%.
- **QG-08**: Độ trễ ra quyết định định tuyến của Orchestrator không vượt quá 500ms.

## 10. Security & Safety Boundaries
- Đảm bảo quy trình phân tích câu prompt của người dùng không bị tiêm nhiễm các chỉ thị thao túng kết quả định tuyến.

## 11. Platform Adapters
- **Engines**: Scikit-Learn Metrics, Embeddings Cross-Encoder, Regex Matcher, LLM Evaluator.

## 12. Deliverables & Output Artifacts
- Bộ dữ liệu 40 kịch bản kiểm chứng định tuyến thực tế.
- Kịch bản tự động chấm điểm F1 và vẽ ma trận nhầm lẫn (`evaluate_routing.py`).
- Bảng đối soát cải tiến độ chính xác định tuyến qua từng phiên bản.

## 13. Related & Complementary Skills
dex-skill-catalog-reconciliation, dex-skill-quality-scorecards, dex-master-orchestrator

## 14. Realistic Usage Example
```powershell
# Chạy bộ đánh giá định tuyến tự động trên toàn bộ 40 scenarios
python scripts/evaluate_routing.py

# Kiểm tra định tuyến bằng pytest
pytest tests/test_skill_routing.py -v
```
