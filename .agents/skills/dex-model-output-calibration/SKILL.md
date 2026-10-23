---
name: dex-model-output-calibration
description: Evaluate, calibrate, and report model output confidence scores using temperature scaling, Platt scaling, and Brier score metrics. Use when high-stakes decision agents must reject low-confidence outputs or quantify prediction uncertainty.
---

# dex-model-output-calibration

## 1. Purpose & Scope
Đánh giá, hiệu chuẩn và đo lường độ tin cậy của kết quả dự đoán từ mô hình AI (Model Output Calibration); áp dụng các kỹ thuật cân chỉnh nhiệt độ (Temperature Scaling), Platt Scaling và tính toán chỉ số Brier Score, xây dựng ngưỡng từ chối an toàn (Rejection Threshold) cho các quyết định rủi ro cao.

## 2. When to Use
- Khi AI Agent đưa ra các quyết định nhạy cảm có ảnh hưởng trực tiếp tới tài chính, y tế hoặc pháp lý.
- Khi mô hình AI có xu hướng quá tự tin (Overconfident) vào các câu trả lời sai (thường gặp ở các mạng nơ-ron sâu và LLMs hiện đại).
- Khi cần thiết lập ngưỡng tin cậy để tự động chuyển tiếp các câu hỏi có độ chắc chắn thấp cho chuyên gia con người xử lý (Human-in-the-loop).

## 3. When NOT to Use
- Khi ứng dụng chỉ phục vụ sáng tạo nghệ thuật, viết thơ hoặc giải trí thông thường không đòi hỏi độ chính xác tuyệt đối.
- Khi mô hình không cung cấp logits hoặc xác suất đầu ra (chỉ trả về text thuần túy mà không có logprobs).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Phân phối xác suất đầu ra của mô hình (Logits / Softmax probabilities / Logprobs), nhãn thực tế của tập kiểm định (Ground Truth).
- **Quyền hạn truy cập:** Quyền truy cập các thông số xác suất đầu ra của mô hình.

## 5. Core Concepts & Taxonomy
- **Well-Calibrated Model:** Mô hình được coi là hiệu chuẩn tốt nếu: trong số các dự đoán mà nó tự tin 80%, có chính xác khoảng 80% là dự đoán đúng trong thực tế.
- **Expected Calibration Error (ECE):** Chỉ số đo lường mức độ sai lệch trung bình giữa độ tự tin dự đoán (Confidence) và độ chính xác thực tế (Accuracy) qua các khoảng bin.
- **Temperature Scaling:** Phương pháp hậu xử lý đơn giản và hiệu quả nhất để cân chỉnh logits: $P_i = \frac{e^{z_i / T}}{\sum_j e^{z_j / T}}$, trong đó $T > 0$ là tham số nhiệt độ được học trên tập validation.

## 6. Step-by-Step Execution Workflow
1. Thu thập dự đoán (xác suất đầu ra) của mô hình trên tập kiểm định độc lập kèm nhãn thực tế.
2. Vẽ biểu đồ độ tin cậy (Reliability Diagram) và tính toán chỉ số lỗi hiệu chuẩn ban đầu (ECE và Brier Score).
3. Tối ưu hóa tham số nhiệt độ $T$ bằng phương pháp cực đại hóa hàm hợp lý (Negative Log-Likelihood) trên tập validation.
4. Áp dụng tham số nhiệt độ $T$ đã tối ưu vào các dự đoán trong môi trường thực tế.
5. Xác định ngưỡng tự tin an toàn (ví dụ: $P_{calibrated} \ge 0.85$); nếu độ tự tin thấp hơn ngưỡng, kích hoạt fallback hoặc chuyển cho con người xét duyệt.
6. Định kỳ kiểm tra lại calibration curve để phát hiện hiện tượng trôi dạt độ tin cậy (Calibration Drift).

## 7. Concrete Examples
### Ví dụ tối ưu hóa Temperature Scaling bằng PyTorch trong Python:
```python
import torch
import torch.nn as nn
import torch.optim as optim

class ModelCalibrator(nn.Module):
    def __init__(self):
        super().__init__()
        # Tham số nhiệt độ T ban đầu bằng 1.0
        self.temperature = nn.Parameter(torch.ones(1))

    def forward(self, logits: torch.Tensor) -> torch.Tensor:
        # Chia logits cho T trước khi đưa qua Softmax
        return logits / self.temperature

    def fit(self, val_logits: torch.Tensor, val_labels: torch.Tensor, lr=0.01, max_iter=50):
        optimizer = optim.LBFGS([self.temperature], lr=lr, max_iter=max_iter)
        criterion = nn.CrossEntropyLoss()

        def eval_loss():
            optimizer.zero_grad()
            loss = criterion(self.forward(val_logits), val_labels)
            loss.backward()
            return loss

        optimizer.step(eval_loss)
        print(f"Optimal Temperature T: {self.temperature.item():.4f}")
```

## 8. Anti-Patterns & Common Traps
- **Confusing Accuracy with Calibration:** Nghĩ rằng một model có Accuracy 95% là đã đáng tin cậy, trong khi 5% còn lại nó tự tin 99% vào các dự đoán sai nghiêm trọng.
- **Calibrating on Training Data:** Học tham số nhiệt độ $T$ trực tiếp trên tập huấn luyện dẫn tới over-fitting và mất tác dụng hiệu chuẩn.
- **Static Confidence Thresholds:** Áp dụng một ngưỡng tự tin duy nhất cho tất cả các lớp nghiệp vụ mà không phân biệt mức độ rủi ro.

## 9. Quality Gates & Acceptance Criteria
- **QG-04**: Chỉ số Expected Calibration Error (ECE) giảm tối thiểu 40% sau khi áp dụng Temperature Scaling.
- **QG-07**: Thời gian tính toán cân chỉnh xác suất cho mỗi dự đoán dưới 1ms.
- **QG-13**: Hệ thống từ chối tự động phê duyệt 100% các quyết định có độ tự tin sau hiệu chuẩn dưới ngưỡng an toàn.

## 10. Security & Safety Boundaries
- Ngăn chặn việc tấn công adversarial bằng cách làm nhiễu logits đầu ra nhằm đánh lừa ngưỡng an toàn của hệ thống.
- Lưu vết phân phối độ tự tin của các dự đoán vào audit log để phục vụ giải trình trách nhiệm giải thuật.

## 11. Platform Adapters
- **Libraries**: `netcal` (Python Calibration Toolbox), PyTorch, Scikit-learn (CalibratedClassifierCV).
- **LLM APIs**: OpenAI Logprobs, Anthropic Logprobs.

## 12. Deliverables & Output Artifacts
- Module ModelCalibrator hỗ trợ Temperature Scaling và Platt Scaling.
- Biểu đồ Reliability Diagram và báo cáo chỉ số ECE / Brier Score.
- Ngưỡng từ chối quyết định tự động dựa trên độ tự tin đã hiệu chuẩn.

## 13. Related & Complementary Skills
dex-machine-learning-data-drift, dex-ai-safety-red-teaming, dex-llm-human-review-gates

## 14. Realistic Usage Example
```powershell
# Chạy đánh giá và hiệu chuẩn độ tin cậy của mô hình
python scripts/calibrate_model.py --val-predictions val_preds.json --plot-reliability
```
