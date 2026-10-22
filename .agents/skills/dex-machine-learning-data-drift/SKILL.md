---
name: dex-machine-learning-data-drift
description: Monitor and quantify covariate feature drift and concept drift in production ML pipelines using Population Stability Index (PSI), Kolmogorov-Smirnov (KS) tests, and Wasserstein distance metrics. Use when triggering automated model retraining or diagnosing post-deployment performance drops.
---

# dex-machine-learning-data-drift

## 1. Purpose & Scope
Giám sát, định lượng và cảnh báo hiện tượng trôi lệch dữ liệu (Data Drift / Covariate Shift) và trôi lệch khái niệm (Concept Drift) trong các đường ống học máy trên môi trường sản xuất; ứng dụng các chỉ số toán học chuẩn: Chỉ số ổn định quần thể (Population Stability Index - PSI), kiểm định thống kê Kolmogorov-Smirnov (KS Test) và khoảng cách Wasserstein; phục vụ kích hoạt tự động quy trình huấn luyện lại mô hình (Automated Retraining) khi độ chính xác bị suy giảm.

## 2. When to Use
- Khi mô hình AI dự đoán rủi ro tín dụng hoặc chấm điểm khách hàng bị giảm sút độ chính xác sau một thời gian đưa vào vận hành.
- Khi hành vi người dùng hoặc bối cảnh thị trường bị thay đổi đột ngột (ví dụ thay đổi sau đại dịch hoặc lạm phát).
- Khi cần xây dựng hệ thống giám sát sức khỏe mô hình AI (ML Observability) theo tiêu chuẩn MLOps.

## 3. When NOT to Use
- Khi hệ thống chỉ sử dụng các quy tắc logic cứng (Rule-based engine) không có mô hình học máy xác suất.
- Khi kích thước dữ liệu suy luận quá nhỏ dưới 100 mẫu không đủ để tính toán phân phối xác suất.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Tập dữ liệu huấn luyện gốc (Baseline Reference Data), tập dữ liệu suy luận thực tế gần nhất (Production Inference Data), thư viện tính toán (Evidently AI, SciPy hoặc NannyML).
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; bảo vệ toàn vẹn tài sản kỹ nghệ và dữ liệu sản xuất.

## 5. Core Concepts & Taxonomy
- **Covariate Shift:** Phân phối của các đặc trưng đầu vào $P(X)$ bị thay đổi nhưng mối quan hệ với nhãn $P(Y|X)$ vẫn giữ nguyên.
- **Concept Drift:** Mối quan hệ giữa đặc trưng đầu vào và nhãn mục tiêu $P(Y|X)$ bị thay đổi (ví dụ: cùng một mức thu nhập nhưng hành vi trả nợ thay đổi).
- **Population Stability Index (PSI):** Chỉ số đo lường mức độ biến động phân phối: $PSI < 0.1$ (Ổn định), $0.1 \le PSI < 0.2$ (Biến động nhẹ), $PSI \ge 0.2$ (Trôi lệch nghiêm trọng, cần huấn luyện lại).

## 6. Step-by-Step Execution Workflow
1. Thu thập mẫu dữ liệu đầu vào của mô hình trong tuần qua và đối chiếu với tập dữ liệu baseline lúc huấn luyện.
2. Tính toán chỉ số PSI cho từng đặc trưng số học và đặc trưng phân loại.
3. Áp dụng kiểm định hai mẫu Kolmogorov-Smirnov (KS-test) để phát hiện sự sai lệch phân phối liên tục.
4. Nếu chỉ số PSI vượt ngưỡng 0.2 trên các đặc trưng quan trọng nhất, phát tín hiệu cảnh báo trôi lệch dữ liệu.
5. Kích hoạt đường ống nạp dữ liệu mới và huấn luyện lại mô hình tự động.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```python
# Population Stability Index (PSI) Calculation
import numpy as np

def calculate_psi(baseline: np.ndarray, target: np.ndarray, num_buckets: int = 10) -> float:
    # Determine bucket cutoffs based on baseline quantiles
    percentiles = np.linspace(0, 100, num_buckets + 1)
    cutoffs = np.percentile(baseline, percentiles)
    cutoffs[0] = -np.inf
    cutoffs[-1] = np.inf

    # Calculate bucket proportions
    baseline_counts, _ = np.histogram(baseline, bins=cutoffs)
    target_counts, _ = np.histogram(target, bins=cutoffs)

    baseline_pct = baseline_counts / len(baseline) + 1e-4
    target_pct = target_counts / len(target) + 1e-4

    # PSI Formula: sum((actual - expected) * ln(actual / expected))
    psi_value = np.sum((target_pct - baseline_pct) * np.log(target_pct / baseline_pct))
    return float(psi_value)
```

## 8. Anti-Patterns & Common Traps
- Đợi đến khi khách hàng phàn nàn mô hình dự đoán sai mới biết mô hình đã bị trôi lệch dữ liệu từ vài tháng trước.
- Tự động huấn luyện lại mô hình liên tục hàng ngày khi chưa kiểm tra nguyên nhân trôi lệch (có thể do lỗi thu thập dữ liệu rác làm hỏng mô hình mới).
- Chỉ theo dõi điểm trung bình (Mean) của đặc trưng mà không theo dõi toàn bộ phân phối (Phân phối có thể bị biến dạng hai đỉnh nhưng điểm trung bình vẫn giữ nguyên).

## 9. Quality Gates & Acceptance Criteria
- QG-01: Đường ống giám sát tự động tính toán chỉ số PSI định kỳ hàng tuần cho 100% các đặc trưng quan trọng.
- QG-02: Tự động gửi cảnh báo khi có bất kỳ đặc trưng nào chạm ngưỡng $PSI \ge 0.25$.
- QG-03: Báo cáo phân tích trôi lệch dữ liệu có trực quan hóa đồ thị so sánh phân phối trước và sau.

## 10. Security & Safety Boundaries
- Tuân thủ quy định bảo mật quyền riêng tư; chỉ lưu trữ phân phối thống kê của đặc trưng mà không lưu trữ dữ liệu cá nhân thô trong hệ thống giám sát drift.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Module đo lường trôi lệch dữ liệu `ModelDriftMonitor.py`.
1. Báo cáo phân tích trôi lệch phân phối `DATA_DRIFT_REPORT.html`.

## 13. Related & Complementary Skills
- [`dex-feature-store-engineering`](.agents/skills/dex-feature-store-engineering/SKILL.md)
- [`dex-model-evaluation`](.agents/skills/dex-model-evaluation/SKILL.md)
- [`dex-ai-observability`](.agents/skills/dex-ai-observability/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Mô hình phát hiện gian lận thanh toán bị tụt giảm tỷ lệ bắt gian lận từ 92% xuống còn 64% sau khi ngân hàng phát hành thẻ tín dụng loại mới. Kỹ sư kích hoạt `dex-machine-learning-data-drift`, chạy script tính PSI và phát hiện đặc trưng `transaction_velocity_hour` có $PSI = 0.42$ do hành vi quẹt thẻ một chạm nhanh hơn trước, kích hoạt cập nhật lại mô hình và phục hồi tỷ lệ phát hiện gian lận về 94%.
