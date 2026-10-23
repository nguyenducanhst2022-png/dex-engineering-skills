---
name: dex-data-label-quality-assessment
description: Audit, clean, and score dataset annotation quality using programmatic label error detection, inter-annotator agreement metrics, and confident learning algorithms. Use when elevating training data fidelity for supervised ML models.
---

# dex-data-label-quality-assessment

## 1. Purpose & Scope
Kiểm toán, làm sạch và chấm điểm chất lượng nhãn dữ liệu (Data Label Quality); sử dụng thuật toán Confident Learning, đo lường độ đồng thuận giữa các người dán nhãn (Inter-Annotator Agreement) và phát hiện nhãn nhiễu hoặc sai lệch trong tập dữ liệu giám sát.

## 2. When to Use
- Khi tập dữ liệu được dán nhãn bởi nhiều chuyên gia hoặc bên thứ ba dẫn tới tiêu chuẩn không đồng nhất.
- Khi mô hình gặp khó khăn trong việc hội tụ hoặc đưa ra dự đoán sai lệch trên các ca dữ liệu biên.
- Khi triển khai chiến lược Data-Centric AI nhằm nâng cao hiệu năng mô hình bằng cách cải thiện chất lượng dữ liệu thay vì đổi kiến trúc mạng.

## 3. When NOT to Use
- Khi dữ liệu nhãn là kết quả đo lường vật lý chính xác từ cảm biến phần cứng đã được hiệu chuẩn.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Tập dữ liệu có nhãn (văn bản, hình ảnh, bảng), danh sách nhãn dự đoán từ mô hình baseline (out-of-sample predicted probabilities).
- **Quyền hạn truy cập:** Quyền sửa đổi tập nhãn dữ liệu huấn luyện.

## 5. Core Concepts & Taxonomy
- **Confident Learning:** Kỹ thuật toán học ước lượng ma trận chuyển tiếp nhãn nhiễu để tìm ra các mẫu dữ liệu có khả năng bị gắn nhãn sai cao nhất.
- **Cohen's Kappa & Fleiss' Kappa:** Chỉ số thống kê đo lường mức độ đồng thuận giữa hai hoặc nhiều người dán nhãn có loại trừ yếu tố trùng hợp ngẫu nhiên.
- **Ambiguous vs. Mislabeled Samples:** Phân biệt giữa các mẫu dữ liệu thực sự gây tranh cãi (cần bổ sung quy chuẩn hướng dẫn) và các mẫu bị bấm nhầm nhãn đơn thuần.

## 6. Step-by-Step Execution Workflow
1. Tính toán ma trận xác suất dự đoán ngoài mẫu (Out-of-sample predicted probabilities) bằng kỹ thuật K-Fold Cross-Validation.
2. Áp dụng thuật toán Confident Learning (Cleanlab) để xếp hạng các mẫu có xác suất bị gắn nhãn sai cao nhất.
3. Tính toán chỉ số Cohen's Kappa giữa các kiểm toán viên dữ liệu trên một tập mẫu đại diện.
4. Trực quan hóa danh sách các mẫu bị nghi ngờ cho chuyên gia nghiệp vụ thẩm định lại.
5. Cập nhật nhãn chuẩn xác hoặc loại bỏ các mẫu dữ liệu có độ tin cậy quá thấp khỏi tập train.
6. Ban hành tài liệu hướng dẫn dán nhãn (Labeling Guidelines) bổ sung cho các trường hợp biên.

## 7. Concrete Examples
### Phát hiện nhãn lỗi tự động bằng Cleanlab trong Python:
```python
import numpy as np
from cleanlab.filter import find_label_issues
from cleanlab.dataset import health_summary

def detect_label_errors(labels: np.ndarray, pred_probs: np.ndarray):
    # Tìm kiếm các mẫu có nhãn nghi ngờ bị lỗi
    issues = find_label_issues(
        labels=labels,
        pred_probs=pred_probs,
        return_indices_ranked_by='self_confidence'
    )
    print(f"Phat hien {len(issues)} mau du lieu co kha nang bi gan sai nhan!")
    
    # In tom tat suc khoe tong the cua tap nhan du lieu
    health_summary(labels, pred_probs)
    return issues
```

## 8. Anti-Patterns & Common Traps
- **Blind Model Blaming:** Vội vàng thay đổi kiến trúc mô hình phức tạp hơn trong khi nguyên nhân chính là do 15% nhãn dữ liệu bị gán sai lệch.
- **Single Annotator Subjectivity:** Để một người duy nhất dán nhãn toàn bộ tập dữ liệu mà không có cơ chế đối soát chéo.
- **Deleting All Discrepancies:** Tự động xóa sạch tất cả các mẫu khó thay vì phân tích nguyên nhân tại sao con người và mô hình không đồng thuận.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Chỉ số độ đồng thuận giữa các người dán nhãn (Cohen's Kappa) đạt tối thiểu 0.80.
- **QG-04**: 100% các mẫu bị thuật toán Confident Learning gắn cờ nghi vấn đều được chuyên gia thẩm duyệt lại.
- **QG-07**: Tập dữ liệu sau khi làm sạch cải thiện độ chính xác của mô hình baseline tối thiểu 2-5%.

## 10. Security & Safety Boundaries
- Kiểm tra bảo vệ quyền riêng tư khi xuất dữ liệu mẫu cho nhân viên dán nhãn bên ngoài (ẩn danh hóa PII).

## 11. Platform Adapters
- **Tools**: Cleanlab, Label Studio, Prodigy, Scikit-Learn Metrics.

## 12. Deliverables & Output Artifacts
- Danh sách các chỉ mục mẫu dữ liệu bị phát hiện sai nhãn.
- Báo cáo phân tích chất lượng dữ liệu (Data Health Report).
- Bộ hướng dẫn dán nhãn đã được chuẩn hóa bổ sung.

## 13. Related & Complementary Skills
dex-training-data-leakage-audit, dex-ai-feedback-labeling, dex-ml-experiment-reproducibility

## 14. Realistic Usage Example
```powershell
# Chạy script phân tích lỗi nhãn bằng Cleanlab
python scripts/ml/find_label_issues.py --data dataset.csv --probs probabilities.npy

# Khởi động giao diện thẩm định nhãn Label Studio
label-studio start
```
