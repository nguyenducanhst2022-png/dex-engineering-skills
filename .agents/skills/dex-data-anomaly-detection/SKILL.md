---
name: dex-data-anomaly-detection
description: Engineer real-time and batch data anomaly detection systems with statistical z-score/IQR baselines, Isolation Forests, dynamic adaptive thresholds, and alert dampening. Use when detecting financial fraud spikes, telemetry failures, or data pipeline corruption.
---

# dex-data-anomaly-detection

## 1. Purpose & Scope
Thiết kế và xây dựng hệ thống phát hiện bất thường trong dữ liệu (Data Anomaly Detection) thời gian thực và dạng lô; ứng dụng các phương pháp thống kê vững (Z-Score, Interquartile Range - IQR), giải thuật học máy không giám sát (Isolation Forest), ngưỡng thích ứng động theo ngữ cảnh (Dynamic Thresholds) và cơ chế giảm nhiễu cảnh báo (Alert Dampening); phục vụ phát hiện sớm gian lận tài chính, sự cố telemetry và lỗi hỏng hóc đường ống dữ liệu.

## 2. When to Use
- Khi cần phát hiện các giao dịch thanh toán có giá trị bất thường nghi vấn gian lận thẻ tín dụng.
- Khi giám sát lưu lượng truy cập mạng để phát hiện các đợt tấn công từ chối dịch vụ (DDoS) hoặc rò rỉ dữ liệu.
- Khi kiểm tra tính toàn vẹn của dữ liệu nạp vào Data Warehouse nhằm ngăn chặn việc chèn các bản ghi lỗi khổng lồ.

## 3. When NOT to Use
- Khi bài toán đã có nhãn dữ liệu rõ ràng và có thể huấn luyện bằng mô hình phân loại có giám sát (Binary Classification).
- Khi dữ liệu có số lượng mẫu quá nhỏ dưới 30 điểm không đủ độ tin cậy thống kê.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Dữ liệu đo lường liên tục, thư viện phân tích học máy (Scikit-Learn, PyOD hoặc Numpy), hệ thống phát cảnh báo (Slack/PagerDuty).
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; bảo vệ toàn vẹn tài sản kỹ nghệ và dữ liệu sản xuất.

## 5. Core Concepts & Taxonomy
- **Robust Statistical IQR:** Xác định ngưỡng bất thường bằng khoảng cách giữa tứ phân vị $Q3 + 1.5 \times IQR$ và $Q1 - 1.5 \times IQR$, không bị ảnh hưởng bởi các giá trị ngoại lai cực trị.
- **Isolation Forest:** Thuật toán cô lập các điểm bất thường bằng các cây quyết định ngẫu nhiên; các điểm bất thường có đường dẫn cô lập (Path Length) ngắn hơn hẳn điểm bình thường.
- **Alert Dampening & Hysteresis:** Thiết lập độ trễ xác nhận và giới hạn tần suất phát cảnh báo để ngăn chặn hiện tượng bão cảnh báo (Alert Fatigue).

## 6. Step-by-Step Execution Workflow
1. Thu thập dữ liệu lịch sử chuẩn trong giai đoạn hệ thống vận hành ổn định để thiết lập baseline.
2. Tính toán các thông số thống kê cơ sở: Trung vị (Median), Độ lệch chuẩn tuyệt đối (MAD) hoặc IQR.
3. Huấn luyện mô hình Isolation Forest với tỷ lệ ngoại lai ước tính (Contamination Factor, ví dụ 0.01).
4. Thiết lập luồng chấm điểm bất thường (Anomaly Scoring) theo thời gian thực cho từng điểm dữ liệu mới đến.
5. Tích hợp cơ chế dập tắt cảnh báo trùng lặp và xuất cảnh báo kèm thông tin ngữ cảnh điều tra.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```python
# Real-Time Anomaly Detection via Robust Z-Score (MAD)
import numpy as np

class RobustAnomalyDetector:
    def __init__(self, threshold=3.5):
        self.threshold = threshold
        self.median = None
        self.mad = None

    def fit(self, values: list[float]):
        arr = np.array(values)
        self.median = np.median(arr)
        # Median Absolute Deviation
        self.mad = np.median(np.abs(arr - self.median)) + 1e-6

    def is_anomaly(self, val: float) -> tuple[bool, float]:
        # Modified Z-Score calculation (Boris Iglewicz and David Hoaglin)
        mod_z = 0.6745 * (val - self.median) / self.mad
        return abs(mod_z) > self.threshold, float(mod_z)
```

## 8. Anti-Patterns & Common Traps
- Dùng công thức Z-Score trung bình cộng thông thường ($\mu \pm 3\sigma$) trên tập dữ liệu có sẵn ngoại lai khổng lồ (bản thân ngoại lai đã làm méo mó độ lệch chuẩn $\sigma$).
- Đặt ngưỡng cố định cứng (Hardcoded threshold) cho dữ liệu có tính chu kỳ ngày đêm, dẫn đến cảnh báo kêu inh ỏi vào mỗi đêm.
- Gửi cảnh báo ngay lập tức cho từng điểm spike đơn lẻ mà không có bước lọc nhiễu xác nhận liên tiếp.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Tỷ lệ báo động giả (False Positive Rate) duy trì dưới 1% trên tập dữ liệu vận hành thông thường.
- QG-02: Phát hiện thành công 100% các đột biến bất thường nhân tạo được tiêm thử nghiệm.
- QG-03: Thuật toán tính toán điểm bất thường có thời gian phản hồi dưới 5ms cho mỗi bản ghi thời gian thực.

## 10. Security & Safety Boundaries
- Không để lộ các thuật toán và ngưỡng phát hiện bất thường ra ngoài để tránh việc kẻ tấn công tìm cách lách qua ngưỡng phát hiện.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Module phát hiện bất thường dữ liệu `RobustAnomalyDetector.py`.
1. Bảng phân tích độ nhạy và cấu hình ngưỡng cảnh báo `anomaly-thresholds.json`.

## 13. Related & Complementary Skills
- [`dex-time-series-diagnostics`](.agents/skills/dex-time-series-diagnostics/SKILL.md)
- [`dex-alert-quality-engineering`](.agents/skills/dex-alert-quality-engineering/SKILL.md)
- [`dex-security-logging-detection`](.agents/skills/dex-security-logging-detection/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Cổng nạp tiền của sàn thương mại điện tử bị lỗi làm phát sinh các giao dịch nạp 0 đồng nhưng vẫn được cộng tiền. Kỹ sư kích hoạt `dex-data-anomaly-detection`, cài đặt thuật toán Modified Z-Score giám sát luồng giao dịch, phát hiện đột biến số lượng giao dịch 0 đồng sau 30 giây phát sinh và kích hoạt khóa cổng tự động, ngăn chặn thiệt hại hàng tỷ đồng.
