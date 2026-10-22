---
name: dex-time-series-diagnostics
description: Diagnose temporal gaps, irregular sampling frequencies, seasonal trend decomposition (STL), stationarity violations, and sensor drift in high-volume time-series data. Use when preparing IoT telemetry, financial price series, or infrastructure monitoring for forecasting models.
---

# dex-time-series-diagnostics

## 1. Purpose & Scope
Chẩn đoán và xử lý các vấn đề khuyết tật trong chuỗi thời gian (Time-Series Diagnostics); phát hiện khoảng trống thời gian (Temporal Gaps), tần suất lấy mẫu không đều, phân tích phân rã xu hướng và mùa vụ (STL Decomposition), kiểm tra tính dừng (Stationarity / ADF Test) và hiện tượng trôi lệch cảm biến (Sensor Drift); phục vụ chuẩn bị dữ liệu chuỗi thời gian cho các mô hình dự báo và cảnh báo sớm.

## 2. When to Use
- Khi chuẩn bị dữ liệu chuỗi thời gian để huấn luyện mô hình dự báo nhu cầu hoặc dự đoán phụ tải điện.
- Khi dữ liệu cảm biến IoT bị mất gói tin ngắt quãng khiến chuỗi thời gian bị đứt đoạn không liên tục.
- Khi kiểm tra xem một chuỗi giá tài chính có tuân thủ giả định toán học của mô hình định lượng hay không.

## 3. When NOT to Use
- Khi phân tích dữ liệu bảng chéo tĩnh không có yếu tố thời gian (Cross-Sectional Data).
- Khi thực hiện truy vấn giao dịch CRUD thông thường.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Thư viện phân tích chuỗi thời gian (Pandas, Statsmodels hoặc SciPy), bộ dữ liệu chuỗi thời gian có timestamp và giá trị đo lường.
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; bảo vệ toàn vẹn tài sản kỹ nghệ và dữ liệu sản xuất.

## 5. Core Concepts & Taxonomy
- **Temporal Regularity Check:** Đo lường khoảng cách thời gian giữa các điểm dữ liệu liên tiếp để phát hiện các đoạn bị mất mẫu (Data Dropouts).
- **STL Decomposition:** Tách chuỗi thời gian $Y_t$ thành 3 thành phần độc lập: Xu hướng dài hạn ($T_t$), Mùa vụ chu kỳ ($S_t$) và Nhiễu ngẫu nhiên ($R_t$).
- **Augmented Dickey-Fuller (ADF) Test:** Kiểm tra giả thuyết thống kê xem chuỗi thời gian có nghiệm đơn vị (Unit Root) hay có tính dừng (Stationary).

## 6. Step-by-Step Execution Workflow
1. Thiết lập chỉ mục thời gian chuẩn (`pd.DatetimeIndex`) và xác định tần suất lấy mẫu mong muốn (`1min`, `1hour`).
2. Quét phát hiện các khoảng trống thời gian vượt quá ngưỡng dung sai và áp dụng phương pháp nội suy phù hợp (Linear hoặc Akima spline).
3. Chạy phân rã STL để bóc tách yếu tố chu kỳ ngày/tuần.
4. Thực hiện kiểm định ADF để xác định bậc vi phân cần thiết nhằm đưa chuỗi về trạng thái dừng.
5. Lập báo cáo chẩn đoán chuỗi thời gian `TIME_SERIES_DIAGNOSTICS_REPORT.md`.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```python
# Time-Series Gap Detection & STL Decomposition
import pandas as pd
from statsmodels.tsa.seasonal import STL
from statsmodels.tsa.stattools import adfuller

def diagnose_time_series(df: pd.DataFrame, time_col: str, value_col: str, expected_freq='1h'):
    df[time_col] = pd.to_datetime(df[time_col])
    df = df.sort_values(time_col).set_index(time_col)

    # 1. Detect temporal gaps
    expected_range = pd.date_range(start=df.index.min(), end=df.index.max(), freq=expected_freq)
    missing_timestamps = expected_range.difference(df.index)
    
    # 2. Resample and interpolate missing gaps
    series = df[value_col].resample(expected_freq).interpolate(method='time')

    # 3. STL Seasonal Decomposition
    stl = STL(series, period=24)
    res = stl.fit()

    # 4. Stationarity Test
    adf_result = adfuller(series.dropna())
    is_stationary = adf_result[1] < 0.05

    return {
        "missing_gaps_count": len(missing_timestamps),
        "is_stationary": is_stationary,
        "p_value": adf_result[1],
        "seasonal_strength": max(0, 1 - (res.resid.var() / (res.seasonal + res.resid).var()))
    }
```

## 8. Anti-Patterns & Common Traps
- Đưa chuỗi thời gian bị khuyết dữ liệu trực tiếp vào mô hình ARIMA hoặc LSTM mà không xử lý bù đắp, dẫn đến mô hình dự báo sai lệch hoàn toàn.
- Áp dụng phương pháp điền giá trị trung bình toàn cục (Mean Imputation) cho chuỗi thời gian có xu hướng tăng trưởng mạnh.
- Bỏ qua kiểm tra tính mùa vụ khiến cảnh báo bất thường liên tục kêu giả vào giờ cao điểm hàng ngày.

## 9. Quality Gates & Acceptance Criteria
- QG-01: 100% các khoảng trống dữ liệu trong chuỗi thời gian được nhận diện và xử lý nội suy đúng quy cách.
- QG-02: Phân rã thành công thành phần mùa vụ và loại trừ chu kỳ trước khi phân tích bất thường.
- QG-03: Báo cáo kiểm định tính dừng ADF đi kèm giá trị p-value rõ ràng.

## 10. Security & Safety Boundaries
- Bảo vệ tính toàn vẹn của chuỗi thời gian kiểm toán; không nội suy làm biến đổi các bản ghi giao dịch tài chính gốc.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Báo cáo chẩn đoán chuỗi thời gian `TIME_SERIES_DIAGNOSTICS_REPORT.md`.
1. Bộ dữ liệu chuỗi thời gian đã được làm sạch và chuẩn hóa tần suất.

## 13. Related & Complementary Skills
- [`dex-data-anomaly-detection`](.agents/skills/dex-data-anomaly-detection/SKILL.md)
- [`dex-analytics-instrumentation`](.agents/skills/dex-analytics-instrumentation/SKILL.md)
- [`dex-data-quality-audits`](.agents/skills/dex-data-quality-audits/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Mô hình AI dự báo phụ tải điện lưới bị sai số tới 35% khiến việc mua điện bị lỗ nặng. Kỹ sư kích hoạt `dex-time-series-diagnostics`, phát hiện đồng hồ cảm biến trạm biến áp bị lệch 15 phút vào mỗi Chủ Nhật và có 120 khoảng trống dữ liệu bị khuyết, sau khi nội suy Akima và tách mùa vụ 24h, sai số dự báo giảm xuống dưới 3.8%.
