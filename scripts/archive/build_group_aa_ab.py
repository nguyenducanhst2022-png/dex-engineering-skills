# -*- coding: utf-8 -*-
"""
DEX SKILLOPS — BUILDER FOR GROUPS AA & AB (Skills 261–280)
Group AA: Advanced Data & Analytics (261–270)
Group AB: Native, Graphics & Game Engineering (271–280)
"""

import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SKILLS_DIR = os.path.join(ROOT, ".agents", "skills")

GROUP_AA_AB_SKILLS = [
    # --- GROUP AA: Advanced Data & Analytics ---
    {
        "id": "dex-sql-metric-semantic-layer",
        "index": 261,
        "group": "Group AA",
        "domain": "Advanced Data & Analytics",
        "description": "Engineer reusable business metric semantic layers (Cube, dbt Semantic Layer, MetricFlow) defining standardized dimensions, measures, time grains, and access policies. Use when eliminating conflicting business metric calculations across BI dashboards and AI query agents.",
        "purpose": "Thiết kế và hiện thực hóa tầng ngữ nghĩa chỉ số kinh doanh (SQL Metric Semantic Layer) sử dụng Cube, dbt Semantic Layer hoặc MetricFlow; chuẩn hóa các định nghĩa chiều dữ liệu (Dimensions), chỉ số đo lường (Measures), độ hạt thời gian (Time Grains) và chính sách kiểm soát truy cập; loại bỏ hoàn toàn hiện tượng xung đột công thức tính toán giữa các dashboard BI và các AI Query Agents.",
        "when_use": [
            "Khi các phòng ban khác nhau (Tài chính, Marketing, Sản phẩm) đưa ra các con số doanh thu hoặc tỷ lệ churn khác nhau do viết SQL tự do.",
            "Khi xây dựng giao diện Text-to-SQL cho AI Agent truy vấn dữ liệu kinh doanh an toàn.",
            "Khi cần quản trị tập trung công thức tính toán các chỉ số KPI trọng yếu của doanh nghiệp."
        ],
        "when_not_use": [
            "Khi hệ thống chỉ có một báo cáo đơn giản duy nhất không có sự phân kỳ số liệu.",
            "Khi thực hiện các truy vấn kỹ thuật nội bộ của hệ thống giám sát hạ tầng máy chủ."
        ],
        "prereqs": "Kho dữ liệu (Snowflake, BigQuery hoặc ClickHouse), công cụ tầng ngữ nghĩa (dbt hoặc Cube.js), kho mã nguồn kiểm soát phiên bản Git.",
        "concepts": [
            "Single Source of Metric Truth: Định nghĩa chỉ số kinh doanh một lần duy nhất dưới dạng mã nguồn (Code-as-Metric) thay vì viết lặp lại trong từng công cụ BI.",
            "Dimension & Measure Modeling: Phân biệt rõ giữa Measure (tính toán cộng dồn: `SUM(amount)`) và Dimension (thuộc tính phân loại: `country`, `user_tier`).",
            "Granularity & Additivity: Đảm bảo các chỉ số đo lường không bị tính toán sai (Double Counting) khi gom nhóm theo các mốc thời gian khác nhau."
        ],
        "steps": [
            "Xác định danh mục chỉ số nghiệp vụ cốt lõi cần chuẩn hóa (ví dụ: `Monthly Recurring Revenue - MRR`).",
            "Viết tệp khai báo ngữ nghĩa chuẩn bằng định dạng YAML (dbt Semantic Layer specification).",
            "Định nghĩa các phép nối dữ liệu (Joins) an toàn giữa các mô hình dữ liệu để chống lỗi Cartesian Product.",
            "Tích hợp tầng ngữ nghĩa vào giao diện truy vấn của AI Agent hoặc cổng BI.",
            "Kiểm thử tính nhất quán của kết quả trả về khi truy vấn qua nhiều chiều phân tích khác nhau."
        ],
        "code_lang": "yaml",
        "code_example": """# dbt Semantic Layer Metric Definition
version: 2

semantic_models:
  - name: revenue_orders
    model: ref('fct_orders')
    entities:
      - name: order_id
        type: primary
      - name: customer_id
        type: foreign
    dimensions:
      - name: order_date
        type: time
        type_params:
          time_granularity: day
      - name: order_status
        type: categorical
    measures:
      - name: net_revenue
        agg: sum
        expr: amount - discount_amount

metrics:
  - name: total_net_revenue
    label: "Total Net Revenue ($)"
    type: simple
    type_params:
      measure: net_revenue""",
        "antipatterns": [
            "Để mỗi nhân viên tự viết câu lệnh `SUM(sales)` trong Tableau hay Metabase dẫn đến mỗi báo cáo ra một con số doanh thu khác nhau.",
            "Cho phép AI Text-to-SQL tự do sinh câu lệnh SQL thô nối các bảng mà không qua tầng ngữ nghĩa kiểm soát.",
            "Định nghĩa chỉ số có phép chia tỷ lệ phần trăm nhưng lại cộng dồn trực tiếp (`AVG` trên các tỷ lệ phần trăm đã tính sẵn)."
        ],
        "quality_gates": [
            "QG-01: 100% các chỉ số KPI doanh nghiệp được định nghĩa tập trung bằng file YAML trong kho Git.",
            "QG-02: Kết quả tính toán từ tầng ngữ nghĩa khớp chính xác tuyệt đối với báo cáo tài chính đã kiểm toán.",
            "QG-03: Không có câu truy vấn nào sinh ra lỗi vòng lặp join hoặc nhân bản dữ liệu ngoài ý muốn."
        ],
        "security": "Áp dụng chính sách bảo mật dữ liệu ở cấp độ hàng (Row-Level Security) trực tiếp trong tầng ngữ nghĩa để ngăn chặn lộ dữ liệu nhạy cảm.",
        "deliverables": [
            "Bộ tệp định nghĩa chỉ số ngữ nghĩa `metrics_model.yml`.",
            "Tài liệu từ điển chỉ số kinh doanh chuẩn hóa `METRICS_DICTIONARY.md`."
        ],
        "related": ["dex-database-query-plans", "dex-data-contracts", "dex-analytics-instrumentation"],
        "scenario": "Ban giám đốc họp khẩn vì báo cáo của phòng Marketing ghi nhận doanh thu tháng là 10 tỷ VND trong khi phòng Kế toán báo chỉ có 8.5 tỷ VND. Kỹ sư kích hoạt `dex-sql-metric-semantic-layer`, phát hiện phòng Marketing chưa trừ tiền hoàn đơn và chiết khấu voucher. Chuẩn hóa công thức `net_revenue` vào dbt Semantic Layer, đưa tất cả báo cáo về cùng một con số duy nhất."
    },
    {
        "id": "dex-time-series-diagnostics",
        "index": 262,
        "group": "Group AA",
        "domain": "Advanced Data & Analytics",
        "description": "Diagnose temporal gaps, irregular sampling frequencies, seasonal trend decomposition (STL), stationarity violations, and sensor drift in high-volume time-series data. Use when preparing IoT telemetry, financial price series, or infrastructure monitoring for forecasting models.",
        "purpose": "Chẩn đoán và xử lý các vấn đề khuyết tật trong chuỗi thời gian (Time-Series Diagnostics); phát hiện khoảng trống thời gian (Temporal Gaps), tần suất lấy mẫu không đều, phân tích phân rã xu hướng và mùa vụ (STL Decomposition), kiểm tra tính dừng (Stationarity / ADF Test) và hiện tượng trôi lệch cảm biến (Sensor Drift); phục vụ chuẩn bị dữ liệu chuỗi thời gian cho các mô hình dự báo và cảnh báo sớm.",
        "when_use": [
            "Khi chuẩn bị dữ liệu chuỗi thời gian để huấn luyện mô hình dự báo nhu cầu hoặc dự đoán phụ tải điện.",
            "Khi dữ liệu cảm biến IoT bị mất gói tin ngắt quãng khiến chuỗi thời gian bị đứt đoạn không liên tục.",
            "Khi kiểm tra xem một chuỗi giá tài chính có tuân thủ giả định toán học của mô hình định lượng hay không."
        ],
        "when_not_use": [
            "Khi phân tích dữ liệu bảng chéo tĩnh không có yếu tố thời gian (Cross-Sectional Data).",
            "Khi thực hiện truy vấn giao dịch CRUD thông thường."
        ],
        "prereqs": "Thư viện phân tích chuỗi thời gian (Pandas, Statsmodels hoặc SciPy), bộ dữ liệu chuỗi thời gian có timestamp và giá trị đo lường.",
        "concepts": [
            "Temporal Regularity Check: Đo lường khoảng cách thời gian giữa các điểm dữ liệu liên tiếp để phát hiện các đoạn bị mất mẫu (Data Dropouts).",
            "STL Decomposition: Tách chuỗi thời gian $Y_t$ thành 3 thành phần độc lập: Xu hướng dài hạn ($T_t$), Mùa vụ chu kỳ ($S_t$) và Nhiễu ngẫu nhiên ($R_t$).",
            "Augmented Dickey-Fuller (ADF) Test: Kiểm tra giả thuyết thống kê xem chuỗi thời gian có nghiệm đơn vị (Unit Root) hay có tính dừng (Stationary)."
        ],
        "steps": [
            "Thiết lập chỉ mục thời gian chuẩn (`pd.DatetimeIndex`) và xác định tần suất lấy mẫu mong muốn (`1min`, `1hour`).",
            "Quét phát hiện các khoảng trống thời gian vượt quá ngưỡng dung sai và áp dụng phương pháp nội suy phù hợp (Linear hoặc Akima spline).",
            "Chạy phân rã STL để bóc tách yếu tố chu kỳ ngày/tuần.",
            "Thực hiện kiểm định ADF để xác định bậc vi phân cần thiết nhằm đưa chuỗi về trạng thái dừng.",
            "Lập báo cáo chẩn đoán chuỗi thời gian `TIME_SERIES_DIAGNOSTICS_REPORT.md`."
        ],
        "code_lang": "python",
        "code_example": """# Time-Series Gap Detection & STL Decomposition
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
    }""",
        "antipatterns": [
            "Đưa chuỗi thời gian bị khuyết dữ liệu trực tiếp vào mô hình ARIMA hoặc LSTM mà không xử lý bù đắp, dẫn đến mô hình dự báo sai lệch hoàn toàn.",
            "Áp dụng phương pháp điền giá trị trung bình toàn cục (Mean Imputation) cho chuỗi thời gian có xu hướng tăng trưởng mạnh.",
            "Bỏ qua kiểm tra tính mùa vụ khiến cảnh báo bất thường liên tục kêu giả vào giờ cao điểm hàng ngày."
        ],
        "quality_gates": [
            "QG-01: 100% các khoảng trống dữ liệu trong chuỗi thời gian được nhận diện và xử lý nội suy đúng quy cách.",
            "QG-02: Phân rã thành công thành phần mùa vụ và loại trừ chu kỳ trước khi phân tích bất thường.",
            "QG-03: Báo cáo kiểm định tính dừng ADF đi kèm giá trị p-value rõ ràng."
        ],
        "security": "Bảo vệ tính toàn vẹn của chuỗi thời gian kiểm toán; không nội suy làm biến đổi các bản ghi giao dịch tài chính gốc.",
        "deliverables": [
            "Báo cáo chẩn đoán chuỗi thời gian `TIME_SERIES_DIAGNOSTICS_REPORT.md`.",
            "Bộ dữ liệu chuỗi thời gian đã được làm sạch và chuẩn hóa tần suất."
        ],
        "related": ["dex-data-anomaly-detection", "dex-analytics-instrumentation", "dex-data-quality-audits"],
        "scenario": "Mô hình AI dự báo phụ tải điện lưới bị sai số tới 35% khiến việc mua điện bị lỗ nặng. Kỹ sư kích hoạt `dex-time-series-diagnostics`, phát hiện đồng hồ cảm biến trạm biến áp bị lệch 15 phút vào mỗi Chủ Nhật và có 120 khoảng trống dữ liệu bị khuyết, sau khi nội suy Akima và tách mùa vụ 24h, sai số dự báo giảm xuống dưới 3.8%."
    },
    {
        "id": "dex-data-anomaly-detection",
        "index": 263,
        "group": "Group AA",
        "domain": "Advanced Data & Analytics",
        "description": "Engineer real-time and batch data anomaly detection systems with statistical z-score/IQR baselines, Isolation Forests, dynamic adaptive thresholds, and alert dampening. Use when detecting financial fraud spikes, telemetry failures, or data pipeline corruption.",
        "purpose": "Thiết kế và xây dựng hệ thống phát hiện bất thường trong dữ liệu (Data Anomaly Detection) thời gian thực và dạng lô; ứng dụng các phương pháp thống kê vững (Z-Score, Interquartile Range - IQR), giải thuật học máy không giám sát (Isolation Forest), ngưỡng thích ứng động theo ngữ cảnh (Dynamic Thresholds) và cơ chế giảm nhiễu cảnh báo (Alert Dampening); phục vụ phát hiện sớm gian lận tài chính, sự cố telemetry và lỗi hỏng hóc đường ống dữ liệu.",
        "when_use": [
            "Khi cần phát hiện các giao dịch thanh toán có giá trị bất thường nghi vấn gian lận thẻ tín dụng.",
            "Khi giám sát lưu lượng truy cập mạng để phát hiện các đợt tấn công từ chối dịch vụ (DDoS) hoặc rò rỉ dữ liệu.",
            "Khi kiểm tra tính toàn vẹn của dữ liệu nạp vào Data Warehouse nhằm ngăn chặn việc chèn các bản ghi lỗi khổng lồ."
        ],
        "when_not_use": [
            "Khi bài toán đã có nhãn dữ liệu rõ ràng và có thể huấn luyện bằng mô hình phân loại có giám sát (Binary Classification).",
            "Khi dữ liệu có số lượng mẫu quá nhỏ dưới 30 điểm không đủ độ tin cậy thống kê."
        ],
        "prereqs": "Dữ liệu đo lường liên tục, thư viện phân tích học máy (Scikit-Learn, PyOD hoặc Numpy), hệ thống phát cảnh báo (Slack/PagerDuty).",
        "concepts": [
            "Robust Statistical IQR: Xác định ngưỡng bất thường bằng khoảng cách giữa tứ phân vị $Q3 + 1.5 \\times IQR$ và $Q1 - 1.5 \\times IQR$, không bị ảnh hưởng bởi các giá trị ngoại lai cực trị.",
            "Isolation Forest: Thuật toán cô lập các điểm bất thường bằng các cây quyết định ngẫu nhiên; các điểm bất thường có đường dẫn cô lập (Path Length) ngắn hơn hẳn điểm bình thường.",
            "Alert Dampening & Hysteresis: Thiết lập độ trễ xác nhận và giới hạn tần suất phát cảnh báo để ngăn chặn hiện tượng bão cảnh báo (Alert Fatigue)."
        ],
        "steps": [
            "Thu thập dữ liệu lịch sử chuẩn trong giai đoạn hệ thống vận hành ổn định để thiết lập baseline.",
            "Tính toán các thông số thống kê cơ sở: Trung vị (Median), Độ lệch chuẩn tuyệt đối (MAD) hoặc IQR.",
            "Huấn luyện mô hình Isolation Forest với tỷ lệ ngoại lai ước tính (Contamination Factor, ví dụ 0.01).",
            "Thiết lập luồng chấm điểm bất thường (Anomaly Scoring) theo thời gian thực cho từng điểm dữ liệu mới đến.",
            "Tích hợp cơ chế dập tắt cảnh báo trùng lặp và xuất cảnh báo kèm thông tin ngữ cảnh điều tra."
        ],
        "code_lang": "python",
        "code_example": """# Real-Time Anomaly Detection via Robust Z-Score (MAD)
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
        return abs(mod_z) > self.threshold, float(mod_z)""",
        "antipatterns": [
            "Dùng công thức Z-Score trung bình cộng thông thường ($\mu \pm 3\sigma$) trên tập dữ liệu có sẵn ngoại lai khổng lồ (bản thân ngoại lai đã làm méo mó độ lệch chuẩn $\sigma$).",
            "Đặt ngưỡng cố định cứng (Hardcoded threshold) cho dữ liệu có tính chu kỳ ngày đêm, dẫn đến cảnh báo kêu inh ỏi vào mỗi đêm.",
            "Gửi cảnh báo ngay lập tức cho từng điểm spike đơn lẻ mà không có bước lọc nhiễu xác nhận liên tiếp."
        ],
        "quality_gates": [
            "QG-01: Tỷ lệ báo động giả (False Positive Rate) duy trì dưới 1% trên tập dữ liệu vận hành thông thường.",
            "QG-02: Phát hiện thành công 100% các đột biến bất thường nhân tạo được tiêm thử nghiệm.",
            "QG-03: Thuật toán tính toán điểm bất thường có thời gian phản hồi dưới 5ms cho mỗi bản ghi thời gian thực."
        ],
        "security": "Không để lộ các thuật toán và ngưỡng phát hiện bất thường ra ngoài để tránh việc kẻ tấn công tìm cách lách qua ngưỡng phát hiện.",
        "deliverables": [
            "Module phát hiện bất thường dữ liệu `RobustAnomalyDetector.py`.",
            "Bảng phân tích độ nhạy và cấu hình ngưỡng cảnh báo `anomaly-thresholds.json`."
        ],
        "related": ["dex-time-series-diagnostics", "dex-alert-quality-engineering", "dex-security-logging-detection"],
        "scenario": "Cổng nạp tiền của sàn thương mại điện tử bị lỗi làm phát sinh các giao dịch nạp 0 đồng nhưng vẫn được cộng tiền. Kỹ sư kích hoạt `dex-data-anomaly-detection`, cài đặt thuật toán Modified Z-Score giám sát luồng giao dịch, phát hiện đột biến số lượng giao dịch 0 đồng sau 30 giây phát sinh và kích hoạt khóa cổng tự động, ngăn chặn thiệt hại hàng tỷ đồng."
    },
    {
        "id": "dex-feature-store-engineering",
        "index": 264,
        "group": "Group AA",
        "domain": "Advanced Data & Analytics",
        "description": "Architect enterprise feature stores (Feast, Hopsworks) with dual online/offline storage synchronization, point-in-time correct join queries, feature definitions as code, and latency SLA guarantees. Use when scaling machine learning models across recommendation, fraud, and prediction systems.",
        "purpose": "Thiết kế kiến trúc kho lưu trữ đặc trưng học máy (Feature Store) chuẩn doanh nghiệp sử dụng Feast hoặc Hopsworks; đồng bộ hóa dữ liệu giữa hai tầng lưu trữ trực tuyến (Online Store có độ trễ mili-giây) và ngoại tuyến (Offline Store phục vụ huấn luyện mô hình theo lô); đảm bảo tính chính xác theo thời điểm lịch sử (Point-in-Time Correctness / As-Of Joins) và quản lý đặc trưng dưới dạng mã nguồn (Features as Code).",
        "when_use": [
            "Khi các mô hình học máy (Gợi ý sản phẩm, phát hiện gian lận) bị lỗi rò rỉ dữ liệu tương lai (Data Leakage) trong quá trình huấn luyện.",
            "Khi các kỹ sư AI phải viết lại các câu lệnh tính toán đặc trưng phức tạp lặp đi lặp lại giữa môi trường train và môi trường serve (Train/Serve Skew).",
            "Khi cần phục vụ các đặc trưng người dùng trong thời gian thực (<10ms) cho các mô hình suy luận trực tiếp."
        ],
        "when_not_use": [
            "Khi tổ chức chỉ có một mô hình học máy duy nhất chạy báo cáo định kỳ mỗi tháng.",
            "Khi lưu trữ các bảng dữ liệu quan hệ nghiệp vụ thông thường không phục vụ huấn luyện AI."
        ],
        "prereqs": "Kho dữ liệu ngoại tuyến (BigQuery, Snowflake hoặc Parquet trên S3), kho dữ liệu trực tuyến độ trễ thấp (Redis hoặc DynamoDB), công cụ Feast SDK.",
        "concepts": [
            "Point-in-Time Correctness: Khi huấn luyện mô hình với sự kiện xảy ra ngày 1/1, chỉ được lấy các đặc trưng của người dùng tại đúng thời điểm ngày 1/1, không được lấy số liệu của ngày hôm nay.",
            "Train/Serve Skew Elimination: Định nghĩa logic tính toán đặc trưng một lần duy nhất, đảm bảo giá trị đưa vào mô hình lúc chạy thật khớp hoàn toàn với lúc học.",
            "Dual-Storage Architecture: Offline Store (Parquet/SQL) tối ưu cho việc đọc hàng triệu bản ghi, Online Store (Redis) tối ưu cho việc tra cứu theo khóa đơn lẻ (Key-value lookup)."
        ],
        "steps": [
            "Định nghĩa thực thể (`Entity`) và các tập đặc trưng (`FeatureView`) bằng mã nguồn Python.",
            "Thực thi lệnh `feast apply` để đồng bộ cấu hình vào sổ cái lưu trữ lược đồ đặc trưng.",
            "Xây dựng đường ống đồng bộ định kỳ (`feast materialize`) đẩy các đặc trưng mới nhất từ kho offline sang Redis.",
            "Sử dụng hàm `get_historical_features` để thực hiện phép nối thời gian chính xác (As-Of Join) cho tập huấn luyện.",
            "Gọi hàm `get_online_features` từ dịch vụ API suy luận với thời gian phản hồi dưới 10ms."
        ],
        "code_lang": "python",
        "code_example": """# Feast Feature View Definition as Code
from datetime import timedelta
from feast import Entity, Field, FeatureView, FileSource
from feast.types import Float32, Int64

user_entity = Entity(name="user_id", join_keys=["user_id"])

user_stats_view = FeatureView(
    name="user_transaction_stats",
    entities=[user_entity],
    ttl=timedelta(days=30),
    schema=[
        Field(name="avg_daily_spend_30d", dtype=Float32),
        Field(name="failed_logins_24h", dtype=Int64),
    ],
    online=True,
    source=FileSource(
        path="data/user_stats.parquet",
        timestamp_field="event_timestamp",
        created_timestamp_column="created_timestamp"
    )
)""",
        "antipatterns": [
            "Nối dữ liệu huấn luyện bằng lệnh SQL `LEFT JOIN` thông thường trên khóa chính mà không có điều kiện thời gian, dẫn đến mô hình 'nhìn thấy trước tương lai' và đạt điểm cao giả tạo lúc train.",
            "Tính toán đặc trưng ở tầng frontend rồi truyền vào API suy luận, khiến hacker có thể sửa đổi đặc trưng để qua mặt mô hình.",
            "Để dữ liệu trong Online Store bị lỗi thời do quên lập lịch tiến trình `materialize`."
        ],
        "quality_gates": [
            "QG-01: Độ trễ tra cứu đặc trưng trực tuyến qua Redis duy trì P99 dưới 10ms dưới tải 1,000 req/s.",
            "QG-02: 100% các tập dữ liệu huấn luyện được tạo ra tuân thủ nghiêm ngặt tính đúng đắn theo thời điểm (Point-in-time correctness).",
            "QG-03: Không có sự trôi lệch giá trị (Zero Drift) giữa đặc trưng lúc huấn luyện và lúc suy luận thực tế."
        ],
        "security": "Áp dụng phân quyền truy cập đặc trưng theo vai trò; mã hóa dữ liệu nhạy cảm lưu trữ trong Redis cache.",
        "deliverables": [
            "Kho mã nguồn định nghĩa đặc trưng `feature_definitions.py`.",
            "Quy trình tự động hóa nạp và đồng bộ đặc trưng `feast-sync-pipeline.yml`."
        ],
        "related": ["dex-machine-learning-data-drift", "dex-data-pipelines", "dex-parquet-arrow-data-interop"],
        "scenario": "Mô hình gợi ý sản phẩm thương mại điện tử đạt độ chính xác 95% trong phòng thí nghiệm nhưng khi đưa lên production thì doanh số không tăng. Kỹ sư kích hoạt `dex-feature-store-engineering`, phát hiện việc nối dữ liệu cũ bị rò rỉ dữ liệu mua hàng tương lai. Tái cấu trúc bằng Feast với Point-in-time join và Redis online store, giúp mô hình phản ánh năng lực thực tế và tăng 18% tỷ lệ chuyển đổi thật."
    },
    {
        "id": "dex-analytics-cohort-retention",
        "index": 265,
        "group": "Group AA",
        "domain": "Advanced Data & Analytics",
        "description": "Engineer scalable user retention cohort matrices, churn decay curves, lifetime value (LTV) projections, and behavioral cohort segmentation in SQL. Use when evaluating product-market fit, subscription health, or marketing acquisition quality.",
        "purpose": "Thiết kế và hiện thực hóa ma trận phân tích thuần tập (User Cohort Retention Matrices), đường cong suy giảm rời bỏ (Churn Decay Curves), mô hình dự phóng giá trị trọn đời (Customer Lifetime Value - LTV) và phân khúc hành vi khách hàng bằng câu lệnh SQL tối ưu hóa; phục vụ đánh giá mức độ phù hợp sản phẩm - thị trường (Product-Market Fit), sức khỏe dịch vụ thuê bao và chất lượng kênh chuyển đổi.",
        "when_use": [
            "Khi ban giám đốc cần đánh giá xem người dùng mới có tiếp tục quay lại sử dụng sản phẩm sau 7 ngày, 30 ngày, 90 ngày hay không.",
            "Khi so sánh chất lượng người dùng đến từ các chiến dịch quảng cáo khác nhau để tối ưu chi phí thu hút khách hàng (CAC).",
            "Khi xây dựng bảng điều khiển phân tích số liệu tăng trưởng cho các quỹ đầu tư mạo hiểm."
        ],
        "when_not_use": [
            "Khi phân tích các giao dịch bán hàng một lần không có sự quay lại của người dùng (One-off e-commerce).",
            "Khi xử lý nhật ký lỗi kỹ thuật của hệ thống máy chủ."
        ],
        "prereqs": "Kho dữ liệu chứa bảng nhật ký hoạt động người dùng (`user_events` hoặc `logins`), kỹ thuật SQL nâng cao (Window Functions, CTE).",
        "concepts": [
            "Acquisition Cohort: Gom nhóm người dùng dựa trên tuần hoặc tháng đầu tiên họ đăng ký tài khoản.",
            "Retention Matrix: Bảng ma trận hình tam giác hiển thị tỷ lệ phần trăm người dùng trong mỗi thuần tập còn hoạt động ở các chu kỳ tiếp theo (Day 0, Day 1, Day 7, Day 30).",
            "Flattening Retention Curve: Dấu hiệu vàng của Product-Market Fit là khi đường cong giữ chân người dùng đi ngang song song với trục hoành thay vì cắm thẳng xuống 0."
        ],
        "steps": [
            "Xác định hành động có ý nghĩa cốt lõi (Core Meaningful Action, ví dụ: 'Tạo tài liệu mới' thay vì chỉ 'Đăng nhập').",
            "Xác định thời điểm gia nhập của từng người dùng (`cohort_month`).",
            "Tính toán khoảng cách chu kỳ thời gian giữa hoạt động tiếp theo và thời điểm gia nhập (`period_number`).",
            "Viết câu lệnh SQL gom nhóm và tính tỷ lệ phần trăm giữ chân cho từng ô trong ma trận.",
            "Xuất dữ liệu ma trận trực quan hóa thành đồ thị nhiệt (Heatmap) và đường cong suy giảm."
        ],
        "code_lang": "sql",
        "code_example": """-- Scalable Monthly Cohort Retention Matrix in SQL
WITH user_cohort AS (
  SELECT user_id, DATE_TRUNC('month', MIN(created_at)) AS cohort_month
  FROM users GROUP BY user_id
),
user_activities AS (
  SELECT DISTINCT e.user_id, DATE_TRUNC('month', e.event_timestamp) AS activity_month
  FROM events e WHERE e.event_name = 'completed_transaction'
)
SELECT 
  c.cohort_month,
  COUNT(DISTINCT c.user_id) AS total_cohort_size,
  (DATE_PART('year', a.activity_month) - DATE_PART('year', c.cohort_month)) * 12 +
  (DATE_PART('month', a.activity_month) - DATE_PART('month', c.cohort_month)) AS month_number,
  ROUND(COUNT(DISTINCT a.user_id)::NUMERIC / COUNT(DISTINCT c.user_id) * 100, 2) AS retention_rate_pct
FROM user_cohort c
LEFT JOIN user_activities a ON c.user_id = a.user_id
GROUP BY 1, 3 ORDER BY 1, 3;""",
        "antipatterns": [
            "Định nghĩa 'hoạt động' chỉ là việc người dùng nhận được một email marketing tự động thay vì họ chủ động mở ứng dụng tương tác.",
            "Gộp chung toàn bộ người dùng vào một đường cong duy nhất, che giấu sự thật là các bản phát hành mới đang làm giảm trải nghiệm người dùng.",
            "Viết câu truy vấn SQL lồng nhau quá nhiều tầng không có chỉ mục khiến câu lệnh chạy mất hàng tiếng trên BigQuery."
        ],
        "quality_gates": [
            "QG-01: Câu truy vấn ma trận thuần tập thực thi dưới 15 giây trên bảng dữ liệu 50 triệu sự kiện.",
            "QG-02: Tỷ lệ giữ chân ở Month 0 luôn đạt chính xác 100.0%.",
            "QG-03: Số liệu đối soát khớp hoàn toàn với bảng báo cáo tài chính doanh thu định kỳ."
        ],
        "security": "Ẩn danh hóa ID người dùng (Hashing user_id) trước khi trích xuất dữ liệu ma trận phục vụ báo cáo đối tác bên ngoài.",
        "deliverables": [
            "Mẫu câu lệnh SQL phân tích thuần tập chuẩn hóa `cohort_retention_matrix.sql`.",
            "Biểu đồ nhiệt phân tích tỷ lệ giữ chân khách hàng `retention-heatmap.json`."
        ],
        "related": ["dex-sql-metric-semantic-layer", "dex-dashboard-data-storytelling", "dex-analytics-instrumentation"],
        "scenario": "Một startup công nghệ chuẩn bị gọi vốn vòng Series A. Nhà đầu tư yêu cầu cung cấp ma trận thuần tập giữ chân 12 tháng gần nhất. Kỹ sư kích hoạt `dex-analytics-cohort-retention`, viết query SQL tối ưu trên Snowflake, trích xuất ma trận Retention hoàn chỉnh chứng minh tỷ lệ giữ chân tháng thứ 6 ổn định ở mức 42% (chỉ số xuất sắc trong ngành), giúp công ty gọi vốn thành công."
    },
    {
        "id": "dex-ab-test-statistical-analysis",
        "index": 266,
        "group": "Group AA",
        "domain": "Advanced Data & Analytics",
        "description": "Conduct rigorous A/B test statistical analyses, verifying Sample Ratio Mismatch (SRM), applying two-tailed hypothesis tests, CUPED variance reduction, and sequential testing bounds. Use when validating product experiment conclusions without false discovery traps.",
        "purpose": "Thực hiện phân tích thống kê thử nghiệm A/B (A/B Testing Statistical Analysis) nghiêm ngặt; kiểm tra hiện tượng sai lệch tỷ lệ mẫu (Sample Ratio Mismatch - SRM), áp dụng kiểm định giả thuyết hai phía (Two-Tailed Hypothesis Testing), kỹ thuật giảm phương sai CUPED (Controlled-experiment Using Pre-Experiment Data) và cận kiểm định tuần tự (Sequential Testing); ngăn ngừa các cạm bẫy khám phá giả và quyết định sai lầm trong kinh doanh.",
        "when_use": [
            "Khi nghiệm thu kết quả của một đợt thử nghiệm A/B tính năng mới để quyết định có nên phát hành chính thức (Rollout 100%) hay không.",
            "Khi cần kiểm tra xem sự chênh lệch số lượng người dùng giữa nhóm A và nhóm B có phải do lỗi kỹ thuật chia nhóm (SRM) hay không.",
            "Khi muốn rút ngắn thời gian chạy thử nghiệm từ 4 tuần xuống 2 tuần bằng phương pháp giảm phương sai CUPED."
        ],
        "when_not_use": [
            "Khi thử nghiệm chỉ có vài chục người dùng không đủ quy mô mẫu thống kê (Sample Size).",
            "Khi kiểm tra sự cố kỹ thuật hạ tầng không liên quan đến hành vi người dùng."
        ],
        "prereqs": "Dữ liệu người dùng tham gia thử nghiệm có gắn nhãn nhóm (Variant A / Variant B), công cụ tính toán thống kê (SciPy hoặc script Python).",
        "concepts": [
            "Sample Ratio Mismatch (SRM): Hiện tượng tỷ lệ người dùng thực tế giữa nhóm Kiểm soát và nhóm Thử nghiệm bị lệch so với thiết kế (ví dụ kỳ vọng 50:50 nhưng thực tế là 52:48), báo hiệu lỗi kỹ thuật chia nhóm và làm vô hiệu hóa toàn bộ kết quả test.",
            "CUPED Variance Reduction: Tận dụng dữ liệu hành vi của người dùng trước khi thử nghiệm để loại bỏ nhiễu phương sai, giúp phát hiện hiệu ứng nhỏ hơn với cùng dung lượng mẫu.",
            "Peeking Problem & Sequential Bounds: Không được liên tục kiểm tra giá trị p-value mỗi ngày và dừng test ngay khi thấy p < 0.05 (vi phạm nghiêm trọng xác suất thống kê)."
        ],
        "steps": [
            "Kiểm tra tính hợp lệ của phân phối mẫu bằng bài kiểm định Chi-square ($p > 0.01$) để loại trừ lỗi SRM.",
            "Tính toán phương sai ban đầu và áp dụng công thức điều chỉnh CUPED dựa trên dữ liệu pre-experiment.",
            "Thực hiện kiểm định t-test hai mẫu độc lập hoặc kiểm định z-test cho tỷ lệ chuyển đổi.",
            "Tính toán khoảng tin cậy 95% cho mức độ nâng cao hiệu quả (Relative Lift).",
            "Lập biên bản báo cáo kết luận thử nghiệm `EXPERIMENT_DECISION_REPORT.md`."
        ],
        "code_lang": "python",
        "code_example": """# SRM Check & CUPED Variance Reduction
import scipy.stats as stats
import numpy as np

def verify_srm(control_count: int, treatment_count: int) -> tuple[bool, float]:
    total = control_count + treatment_count
    expected = [total / 2.0, total / 2.0]
    chi2, p_val = stats.chisquare([control_count, treatment_count], expected)
    # If p_val < 0.001, SRM is present (Critical Flaw)
    return p_val >= 0.001, p_val

def apply_cuped(y_variant: np.ndarray, x_pre_variant: np.ndarray, x_pre_all: np.ndarray) -> np.ndarray:
    # theta = cov(Y, X) / var(X)
    covariance = np.cov(y_variant, x_pre_variant)[0, 1]
    variance_x = np.var(x_pre_all)
    theta = covariance / variance_x if variance_x > 0 else 0
    return y_variant - theta * (x_pre_variant - np.mean(x_pre_all))""",
        "antipatterns": [
            "Liên tục mở dashboard xem p-value mỗi sáng và bấm dừng test ăn mừng ngay khi p-value vừa chạm 0.04 (lỗi 'Peeking Problem' làm tăng tỷ lệ dương tính giả lên 30%).",
            "Bỏ qua bước kiểm tra SRM, dẫn đến việc đưa ra kết luận kinh doanh dựa trên một mẫu thử nghiệm bị lỗi phân bổ trầm trọng.",
            "Chạy thử nghiệm cùng lúc 20 biến thể mà không hiệu chỉnh mức ý nghĩa thống kê (lỗi so sánh bội Bonferroni Correction)."
        ],
        "quality_gates": [
            "QG-01: Bài kiểm định SRM đạt $p > 0.001$ trước khi tiến hành bất kỳ phân tích số liệu chuyển đổi nào.",
            "QG-02: Thử nghiệm đạt đủ kích thước mẫu tối thiểu (Minimum Sample Size) đã được tính toán từ trước (Power >= 80%).",
            "QG-03: Khoảng tin cậy 95% của chỉ số đo lường không cắt qua điểm 0 đối với các tính năng được duyệt rollout."
        ],
        "security": "Bảo vệ thông tin chiến lược thử nghiệm kinh doanh; không công khai dữ liệu đo lường doanh thu chi tiết ra ngoài doanh nghiệp.",
        "deliverables": [
            "Báo cáo phân tích thống kê thử nghiệm `EXPERIMENT_DECISION_REPORT.md`.",
            "Script tự động kiểm tra SRM và tính toán CUPED `ab_evaluator.py`."
        ],
        "related": ["dex-analytics-cohort-retention", "dex-feature-flags", "dex-data-quality-audits"],
        "scenario": "Đội ngũ sản phẩm hào hứng vì nút bấm mua hàng mới làm tăng tỷ lệ chuyển đổi 8% với $p = 0.02$. Kỹ sư kích hoạt `dex-ab-test-statistical-analysis` để kiểm toán, phát hiện bài kiểm tra SRM có $p = 0.00001$ (lệch mẫu do một phiên bản Android cũ bị crash không nạp được nhóm B). Sau khi sửa lỗi phân chia nhóm và chạy lại, kết quả thật cho thấy nút mới không hề có tác dụng, cứu công ty khỏi một quyết định thiết kế sai lầm."
    },
    {
        "id": "dex-geospatial-data-pipelines",
        "index": 267,
        "group": "Group AA",
        "domain": "Advanced Data & Analytics",
        "description": "Architect high-throughput geospatial data pipelines using Uber H3 discrete global grids, Google S2 geometry, PostGIS spatial indexing, and GeoJSON/WKB serialization. Use when building ride-hailing routing, geofencing alert engines, or spatial delivery analytics.",
        "purpose": "Thiết kế và hiện thực hóa các đường ống xử lý dữ liệu không gian địa lý (Geospatial Data Pipelines) thông lượng cao; ứng dụng hệ thống lưới lục giác toàn cầu Uber H3, hình học Google S2, chỉ mục không gian PostGIS (R-Tree / GIST) và tuần tự hóa dữ liệu GeoJSON/WKB; phục vụ các hệ thống định tuyến gọi xe, hàng rào địa lý (Geofencing) thời gian thực và phân tích bán kính giao hàng.",
        "when_use": [
            "Khi xây dựng ứng dụng tìm kiếm tài xế hoặc địa điểm gần nhất trong bán kính 5km cho hàng triệu người dùng đồng thời.",
            "Khi cần gom cụm (Clustering) hàng triệu điểm tọa độ GPS thành các vùng lục giác đồng đều để trực quan hóa bản đồ nhiệt.",
            "Khi kiểm tra xem một phương tiện có đi vào hoặc đi ra khỏi khu vực hàng rào địa lý được chỉ định hay không."
        ],
        "when_not_use": [
            "Khi ứng dụng chỉ lưu trữ địa chỉ văn bản thông thường không cần tính toán khoảng cách hay ranh giới không gian.",
            "Khi tính toán khoảng cách phẳng thuần túy trong phòng thí nghiệm không xét đến độ cong của Trái Đất."
        ],
        "prereqs": "Thư viện Uber H3 (`h3-js` hoặc Python `h3`), cơ sở dữ liệu hỗ trợ không gian PostGIS hoặc DuckDB Spatial, hiểu biết về hệ tọa độ WGS84 (EPSG:4326).",
        "concepts": [
            "H3 Hexagonal Hierarchical Spatial Index: Chia bề mặt Trái Đất thành các ô lục giác đều với 16 cấp độ phân giải (Resolution 0 đến 15); mỗi ô có đúng một mã băm số nguyên 64-bit duy nhất.",
            "Neighbor Traversal Efficiency: Các ô lục giác có khoảng cách tới 6 ô lân cận hoàn toàn bằng nhau (không bị méo mó như ô vuông), giúp thuật toán tìm kiếm lân cận $O(1)$ cực nhanh.",
            "GIST Spatial Indexing: Cấu trúc cây R-Tree trong PostGIS giúp tìm kiếm các đối tượng hình học giao nhau (`ST_Intersects`) trong vài mili-giây."
        ],
        "steps": [
            "Chuyển đổi cặp tọa độ kinh độ/vĩ độ (Longitude, Latitude) thành mã lục giác H3 cấp độ phù hợp (ví dụ Res 8 ~ 460 mét).",
            "Lưu mã H3 index dưới dạng số nguyên 64-bit trong cơ sở dữ liệu để đánh chỉ mục B-Tree cực nhanh.",
            "Khi tìm kiếm lân cận, gọi hàm `h3.gridDisk(centerH3, kRing)` để lấy danh sách các ô xung quanh.",
            "Thực hiện truy vấn dữ liệu bằng toán tử `IN (:neighborH3List)` thay vì tính toán khoảng cách cầu Haversine tốn CPU trên từng dòng.",
            "Kiểm tra độ trễ truy vấn khi phục vụ 5,000 yêu cầu tìm tài xế mỗi giây."
        ],
        "code_lang": "typescript",
        "code_example": """import h3 from 'h3-js';

// High-Performance Geospatial Spatial Hashing
export function indexDriverLocation(lat: number, lng: number): string {
  // Resolution 8 corresponds to ~460m edge length
  return h3.latLngToCell(lat, lng, 8);
}

export function findNearbyDriverH3Cells(lat: number, lng: number, radiusKm: number): string[] {
  const originCell = h3.latLngToCell(lat, lng, 8);
  // Approx 1 ring is ~0.9km
  const kRings = Math.ceil(radiusKm / 0.9);
  return h3.gridDisk(originCell, kRings);
}

// SQL Query becomes super-fast B-Tree lookup:
// SELECT * FROM active_drivers WHERE h3_index = ANY($1);""",
        "antipatterns": [
            "Tính toán khoảng cách Haversine bằng lệnh toán học `acos(sin()...)` trên toàn bộ bảng 10 triệu dòng cho mỗi lần người dùng mở app (làm đơ toàn bộ database).",
            "Nhầm lẫn thứ tự giữa Kinh độ (Longitude/X) và Vĩ độ (Latitude/Y) dẫn đến việc định vị địa điểm rơi xuống biển.",
            "Dùng hệ thống lưới ô vuông (Latitude/Longitude Grid) khiến các ô bị méo mó nghiêm trọng khi tiến về hai cực của Trái Đất."
        ],
        "quality_gates": [
            "QG-01: Độ trễ tìm kiếm tài xế lân cận trong bán kính 3km duy trì dưới 5ms trên tập dữ liệu 500,000 xe.",
            "QG-02: 100% tọa độ vị trí được chuyển đổi chính xác sang mã H3 Index theo chuẩn WGS84.",
            "QG-03: Không có lỗi tràn số nguyên khi lưu trữ mã H3 Index 64-bit trong cơ sở dữ liệu."
        ],
        "security": "Làm mờ tọa độ GPS chính xác của người dùng ở khu vực nhạy cảm (nhà riêng) bằng cách chỉ lưu trữ ở độ phân giải H3 vừa phải để bảo vệ quyền riêng tư.",
        "deliverables": [
            "Module lập chỉ mục không gian địa lý H3 `GeospatialH3Pipeline.ts`.",
            "Kịch bản cấu hình bảng dữ liệu không gian PostGIS `postgis_spatial_setup.sql`."
        ],
        "related": ["dex-database-query-plans", "dex-data-pipelines", "dex-search-engineering"],
        "scenario": "Hệ thống giao đồ ăn bị sập máy chủ vào giờ ăn trưa do 200,000 khách hàng cùng lúc mở app tìm nhà hàng gần nhất, khiến câu lệnh tính khoảng cách Haversine làm nghẽn CPU database 100%. Kỹ sư kích hoạt `dex-geospatial-data-pipelines`, chuyển sang đánh chỉ mục lục giác Uber H3 Res 8, biến câu truy vấn hình học nặng nề thành một phép tra cứu B-Tree đơn giản, giảm tải CPU từ 100% xuống 8%."
    },
    {
        "id": "dex-data-warehouse-cost-tuning",
        "index": 268,
        "group": "Group AA",
        "domain": "Advanced Data & Analytics",
        "description": "Analyze and optimize BigQuery, Snowflake, and Databricks query compute costs, partition pruning, clustering strategies, slot reservations, and auto-suspend warehouse policies. Use when curtailing runaway cloud data warehouse spending without impacting analytics SLAs.",
        "purpose": "Phân tích, kiểm toán và tối ưu hóa chi phí tính toán trên các kho dữ liệu đám mây (Cloud Data Warehouse Cost Tuning) như Google BigQuery, Snowflake và Databricks; ứng dụng kỹ thuật cắt tỉa phân vùng (Partition Pruning), gom cụm dữ liệu (Clustering), cấp phát slot tính toán và chính sách tự động ngủ đông kho dữ liệu; cắt giảm tối thiểu 40% chi phí hóa đơn hàng tháng mà không ảnh hưởng đến cam kết thời gian hoàn thành truy vấn (SLA).",
        "when_use": [
            "Khi hóa đơn chi phí BigQuery/Snowflake tăng vọt bất thường vượt quá ngân sách của doanh nghiệp.",
            "Khi các câu lệnh truy vấn quét qua toàn bộ bảng dữ liệu hàng chục Terabyte một cách lãng phí.",
            "Khi cần thiết lập hạn ngạch chi phí (Cost Quotas) và cảnh báo cho từng đội nhóm kỹ thuật."
        ],
        "when_not_use": [
            "Khi kho dữ liệu chỉ có dung lượng nhỏ dưới 10GB với chi phí vài đô la mỗi tháng.",
            "Khi tối ưu hóa cơ sở dữ liệu giao dịch MySQL/PostgreSQL cục bộ."
        ],
        "prereqs": "Quyền xem bảng nhật ký chi phí `INFORMATION_SCHEMA.JOBS_BY_PROJECT` (BigQuery) hoặc `SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY`, hiểu biết về mô hình tính giá điện toán đám mây.",
        "concepts": [
            "Partition Pruning: Cấu hình bảng phân vùng theo ngày (`PARTITION BY DATE(created_at)`) để câu lệnh truy vấn chỉ đọc đúng thư mục ngày cần thiết, giảm 95% số byte bị quét.",
            "Clustering Strategy: Sắp xếp dữ liệu vật lý theo các cột thường xuyên dùng để lọc (`CLUSTER BY tenant_id, status`), giúp công cụ bỏ qua các khối dữ liệu không liên quan.",
            "Auto-Suspend & Auto-Resume: Cấu hình Snowflake Warehouse tự động tắt sau 60 giây không có truy vấn để triệt tiêu chi phí máy chủ nhàn rỗi."
        ],
        "steps": [
            "Truy vấn bảng lịch sử để tìm ra top 10 câu lệnh SQL tiêu tốn nhiều chi phí nhất trong tháng.",
            "Kiểm tra xem câu lệnh có quét toàn bộ bảng (Full Table Scan) do thiếu điều kiện phân vùng hay không.",
            "Tái cấu trúc bảng dữ liệu: áp dụng phân vùng theo ngày và gom cụm theo các khóa ngoại phổ biến.",
            "Bắt buộc người dùng phải có mệnh đề lọc trên cột phân vùng bằng cờ `require_partition_filter = true`.",
            "Lập báo cáo tổng kết chi phí tiết kiệm `DATA_WAREHOUSE_COST_AUDIT.md`."
        ],
        "code_lang": "sql",
        "code_example": """-- BigQuery Partition & Cluster Optimization Example
CREATE OR REPLACE TABLE `my_project.analytics.user_events`
PARTITION BY DATE(event_timestamp)
CLUSTER BY tenant_id, event_type
OPTIONS (
  require_partition_filter = TRUE,
  partition_expiration_days = 365
) AS
SELECT * FROM `my_project.staging.raw_events`;

-- Cost-Audit: Find most expensive queries in last 7 days
SELECT 
  query,
  user_email,
  ROUND(total_bytes_billed / 1024 / 1024 / 1024 / 1024, 2) AS tb_billed,
  ROUND((total_bytes_billed / 1024 / 1024 / 1024 / 1024) * 6.25, 2) AS estimated_cost_usd
FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE creation_time > TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 7 DAY)
ORDER BY total_bytes_billed DESC LIMIT 10;""",
        "antipatterns": [
            "Chạy lệnh `SELECT * FROM table` trên BigQuery mà không chỉ định danh sách cột (BigQuery là Columnar Storage, lệnh này sẽ quét toàn bộ dữ liệu của tất cả các cột).",
            "Cấu hình Snowflake Warehouse ở kích thước `X-Large` cho các tác vụ phân tích nhỏ và để thời gian chờ tự tắt là 30 phút.",
            "Không đặt giới hạn ngân sách tối đa trên từng dự án, dẫn đến một câu lệnh SQL sai của thực tập sinh có thể làm tốn hàng nghìn USD trong vài phút."
        ],
        "quality_gates": [
            "QG-01: 100% các bảng dữ liệu lớn hơn 100GB đều được cấu hình Partition và Cluster.",
            "QG-02: Bật cờ bắt buộc lọc phân vùng `require_partition_filter` trên toàn bộ bảng nhật ký sự kiện.",
            "QG-03: Chi phí hóa đơn truy vấn kho dữ liệu giảm tối thiểu 35% ngay trong tháng đầu tiên áp dụng."
        ],
        "security": "Phân quyền hạn ngạch chi phí truy vấn theo nhóm người dùng (Query Cost Limits) để ngăn ngừa việc tiêu tốn ngân sách công ty do sơ suất.",
        "deliverables": [
            "Báo cáo kiểm toán và tối ưu chi phí kho dữ liệu `DATA_WAREHOUSE_COST_AUDIT.md`.",
            "Bộ script tái cấu trúc phân vùng và gom cụm bảng dữ liệu."
        ],
        "related": ["dex-database-query-plans", "dex-capacity-planning", "dex-sql-metric-semantic-layer"],
        "scenario": "Doanh nghiệp giật mình khi hóa đơn Google Cloud BigQuery tăng vọt từ $3,000 lên $28,000 trong một tháng do dashboard BI quét qua toàn bộ bảng lịch sử 5 năm mỗi 5 phút. Kỹ sư kích hoạt `dex-data-warehouse-cost-tuning`, tìm ra câu query thủ phạm, cấu hình phân vùng bảng theo ngày và thêm bộ lọc thời gian 7 ngày gần nhất, đưa hóa đơn trở về mức $2,400/tháng."
    },
    {
        "id": "dex-backfill-reconciliation",
        "index": 269,
        "group": "Group AA",
        "domain": "Advanced Data & Analytics",
        "description": "Orchestrate safe, idempotent historical data backfills across partitioned analytical tables, verifying pre/post row counts, metric parity reconciliations, and preventing downstream cascade corruptions. Use when recalculating metrics, fixing historic ETL bugs, or migrating database schemas.",
        "purpose": "Điều phối quy trình nạp bù dữ liệu lịch sử (Historical Data Backfill) an toàn và có tính bất biến; chia nhỏ tác vụ theo phân vùng thời gian có kiểm soát, đối soát số lượng bản ghi (Pre/Post Row Counts), kiểm tra tính tương đương của chỉ số (Metric Parity Reconciliation) và ngăn chặn sự cố làm ô nhiễm dữ liệu của các đường ống xuôi dòng (Downstream Pipelines).",
        "when_use": [
            "Khi phát hiện lỗi công thức tính toán trong mã ETL cũ và cần chạy lại toàn bộ dữ liệu của 6 tháng trước.",
            "Khi bổ sung thêm một cột thông tin mới vào bảng lịch sử và cần nạp bù giá trị cho các năm cũ.",
            "Khi di chuyển dữ liệu từ hệ thống cũ sang nền tảng kho dữ liệu mới mà cần đảm bảo không thất thoát dữ liệu."
        ],
        "when_not_use": [
            "Khi chỉ sửa một bản ghi đơn lẻ trực tiếp bằng tay trong môi trường phát triển.",
            "Khi dữ liệu luồng thời gian thực đang chạy bình thường không có nhu cầu tính toán lại quá khứ."
        ],
        "prereqs": "Công cụ điều phối luồng công việc (Airflow, Dagster hoặc script Python), bản sao lưu dự phòng của bảng dữ liệu mục tiêu, chỉ số đối soát chuẩn.",
        "concepts": [
            "Partition-by-Partition Execution: Chia nhỏ việc nạp bù dữ liệu thành từng khoảng thời gian nhỏ (ví dụ từng ngày hoặc từng tuần) thay vì chạy một mẻ lớn làm sập hệ thống.",
            "Idempotent Overwrite: Sử dụng cơ chế ghi đè nguyên tử từng phân vùng (`INSERT OVERWRITE PARTITION`) để nếu có chạy lại nhiều lần thì kết quả vẫn không bị trùng lặp bản ghi.",
            "Metric Parity Check: So sánh tổng số tiền hoặc số lượng người dùng giữa bảng cũ và bảng vừa nạp bù; nếu sai lệch vượt quá ngưỡng cho phép (0.001%), lập tức hoàn tác."
        ],
        "steps": [
            "Tạo bản sao lưu ảnh chụp (Snapshot Backup) của bảng dữ liệu mục tiêu trước khi can thiệp.",
            "Viết kịch bản nạp bù dữ liệu có tham số hóa ngày bắt đầu `start_date` và ngày kết thúc `end_date`.",
            "Chạy thử nghiệm trên một phân vùng duy nhất và thực hiện đối soát số liệu pre/post.",
            "Kích hoạt chạy tuần tự cho toàn bộ các phân vùng lịch sử với cơ chế kiểm soát tốc độ (Throttling) để không làm nghẽn tài nguyên chung.",
            "Lập biên bản nghiệm thu đối soát dữ liệu nạp bù `BACKFILL_RECONCILIATION_REPORT.md`."
        ],
        "code_lang": "python",
        "code_example": """# Controlled Partitioned Backfill Runner with Parity Check
import datetime

def run_backfill_partition(date_str: str, db_conn):
    print(f"Starting atomic backfill for date: {date_str}")
    # 1. Snapshot baseline metric before update
    baseline_sum = db_conn.query(f"SELECT SUM(revenue) FROM fct_sales WHERE sale_date = '{date_str}'")

    # 2. Atomic overwrite partition
    db_conn.execute(f\"\"\"
        INSERT OVERWRITE TABLE fct_sales PARTITION (sale_date = '{date_str}')
        SELECT id, amount - discount AS revenue, customer_id, '{date_str}' 
        FROM staging_sales WHERE sale_date = '{date_str}';
    \"\"\")

    # 3. Reconcile parity
    new_sum = db_conn.query(f"SELECT SUM(revenue) FROM fct_sales WHERE sale_date = '{date_str}'")
    diff_pct = abs(new_sum - baseline_sum) / (baseline_sum + 1e-6)
    print(f"Partition {date_str} completed. Parity variance: {diff_pct:.4f}")
    assert diff_pct < 0.05, f"Parity check failed on {date_str}!" """,
        "antipatterns": [
            "Chạy một câu lệnh `UPDATE` khổng lồ trên toàn bộ bảng 500 triệu dòng mà không có phân vùng, làm khóa bảng cơ sở dữ liệu suốt 8 tiếng.",
            "Dùng lệnh `INSERT INTO` thông thường mà không có khóa bất biến, khiến việc chạy lại khi gặp lỗi mạng làm nhân đôi toàn bộ dữ liệu doanh thu.",
            "Không thông báo cho các đội ngũ phân tích hạ nguồn khiến họ tưởng số liệu bị đột biến và gửi báo cáo sai cho ban giám đốc."
        ],
        "quality_gates": [
            "QG-01: 100% các tác vụ nạp bù dữ liệu được thực thi dưới dạng ghi đè nguyên tử từng phân vùng (Idempotent Overwrite).",
            "QG-02: Số lượng bản ghi và tổng chỉ số kiểm soát sau khi nạp bù khớp chính xác với tiêu chí nghiệm thu đề ra.",
            "QG-03: Có sẵn kế hoạch hoàn tác (Rollback Plan) đã được kiểm chứng trước khi chạy trên dữ liệu sản xuất."
        ],
        "security": "Giới hạn quyền chạy backfill chỉ cho các tài khoản quản trị chuyên dụng; lưu nhật ký kiểm toán người kích hoạt và lý do thực hiện.",
        "deliverables": [
            "Script điều phối nạp bù dữ liệu có kiểm soát `backfill_orchestrator.py`.",
            "Biên bản đối soát số liệu nạp bù `BACKFILL_RECONCILIATION_REPORT.md`."
        ],
        "related": ["dex-schema-evolution", "dex-data-quality-audits", "dex-disaster-recovery"],
        "scenario": "Phát hiện mã tính thuế VAT trong bảng báo cáo tài chính của năm 2025 bị áp sai tỷ lệ 8% thay vì 10%. Kỹ sư kích hoạt `dex-backfill-reconciliation`, lập kịch bản nạp bù từng ngày cho 365 ngày của năm 2025, chạy đối soát tự động sau mỗi ngày nạp và hoàn thành tính lại toàn bộ số liệu chuẩn xác mà không làm gián đoạn các báo cáo đang chạy của công ty."
    },
    {
        "id": "dex-machine-learning-data-drift",
        "index": 270,
        "group": "Group AA",
        "domain": "Advanced Data & Analytics",
        "description": "Monitor and quantify covariate feature drift and concept drift in production ML pipelines using Population Stability Index (PSI), Kolmogorov-Smirnov (KS) tests, and Wasserstein distance metrics. Use when triggering automated model retraining or diagnosing post-deployment performance drops.",
        "purpose": "Giám sát, định lượng và cảnh báo hiện tượng trôi lệch dữ liệu (Data Drift / Covariate Shift) và trôi lệch khái niệm (Concept Drift) trong các đường ống học máy trên môi trường sản xuất; ứng dụng các chỉ số toán học chuẩn: Chỉ số ổn định quần thể (Population Stability Index - PSI), kiểm định thống kê Kolmogorov-Smirnov (KS Test) và khoảng cách Wasserstein; phục vụ kích hoạt tự động quy trình huấn luyện lại mô hình (Automated Retraining) khi độ chính xác bị suy giảm.",
        "when_use": [
            "Khi mô hình AI dự đoán rủi ro tín dụng hoặc chấm điểm khách hàng bị giảm sút độ chính xác sau một thời gian đưa vào vận hành.",
            "Khi hành vi người dùng hoặc bối cảnh thị trường bị thay đổi đột ngột (ví dụ thay đổi sau đại dịch hoặc lạm phát).",
            "Khi cần xây dựng hệ thống giám sát sức khỏe mô hình AI (ML Observability) theo tiêu chuẩn MLOps."
        ],
        "when_not_use": [
            "Khi hệ thống chỉ sử dụng các quy tắc logic cứng (Rule-based engine) không có mô hình học máy xác suất.",
            "Khi kích thước dữ liệu suy luận quá nhỏ dưới 100 mẫu không đủ để tính toán phân phối xác suất."
        ],
        "prereqs": "Tập dữ liệu huấn luyện gốc (Baseline Reference Data), tập dữ liệu suy luận thực tế gần nhất (Production Inference Data), thư viện tính toán (Evidently AI, SciPy hoặc NannyML).",
        "concepts": [
            "Covariate Shift: Phân phối của các đặc trưng đầu vào $P(X)$ bị thay đổi nhưng mối quan hệ với nhãn $P(Y|X)$ vẫn giữ nguyên.",
            "Concept Drift: Mối quan hệ giữa đặc trưng đầu vào và nhãn mục tiêu $P(Y|X)$ bị thay đổi (ví dụ: cùng một mức thu nhập nhưng hành vi trả nợ thay đổi).",
            "Population Stability Index (PSI): Chỉ số đo lường mức độ biến động phân phối: $PSI < 0.1$ (Ổn định), $0.1 \le PSI < 0.2$ (Biến động nhẹ), $PSI \ge 0.2$ (Trôi lệch nghiêm trọng, cần huấn luyện lại)."
        ],
        "steps": [
            "Thu thập mẫu dữ liệu đầu vào của mô hình trong tuần qua và đối chiếu với tập dữ liệu baseline lúc huấn luyện.",
            "Tính toán chỉ số PSI cho từng đặc trưng số học và đặc trưng phân loại.",
            "Áp dụng kiểm định hai mẫu Kolmogorov-Smirnov (KS-test) để phát hiện sự sai lệch phân phối liên tục.",
            "Nếu chỉ số PSI vượt ngưỡng 0.2 trên các đặc trưng quan trọng nhất, phát tín hiệu cảnh báo trôi lệch dữ liệu.",
            "Kích hoạt đường ống nạp dữ liệu mới và huấn luyện lại mô hình tự động."
        ],
        "code_lang": "python",
        "code_example": """# Population Stability Index (PSI) Calculation
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
    return float(psi_value)""",
        "antipatterns": [
            "Đợi đến khi khách hàng phàn nàn mô hình dự đoán sai mới biết mô hình đã bị trôi lệch dữ liệu từ vài tháng trước.",
            "Tự động huấn luyện lại mô hình liên tục hàng ngày khi chưa kiểm tra nguyên nhân trôi lệch (có thể do lỗi thu thập dữ liệu rác làm hỏng mô hình mới).",
            "Chỉ theo dõi điểm trung bình (Mean) của đặc trưng mà không theo dõi toàn bộ phân phối (Phân phối có thể bị biến dạng hai đỉnh nhưng điểm trung bình vẫn giữ nguyên)."
        ],
        "quality_gates": [
            "QG-01: Đường ống giám sát tự động tính toán chỉ số PSI định kỳ hàng tuần cho 100% các đặc trưng quan trọng.",
            "QG-02: Tự động gửi cảnh báo khi có bất kỳ đặc trưng nào chạm ngưỡng $PSI \ge 0.25$.",
            "QG-03: Báo cáo phân tích trôi lệch dữ liệu có trực quan hóa đồ thị so sánh phân phối trước và sau."
        ],
        "security": "Tuân thủ quy định bảo mật quyền riêng tư; chỉ lưu trữ phân phối thống kê của đặc trưng mà không lưu trữ dữ liệu cá nhân thô trong hệ thống giám sát drift.",
        "deliverables": [
            "Module đo lường trôi lệch dữ liệu `ModelDriftMonitor.py`.",
            "Báo cáo phân tích trôi lệch phân phối `DATA_DRIFT_REPORT.html`."
        ],
        "related": ["dex-feature-store-engineering", "dex-model-evaluation", "dex-ai-observability"],
        "scenario": "Mô hình phát hiện gian lận thanh toán bị tụt giảm tỷ lệ bắt gian lận từ 92% xuống còn 64% sau khi ngân hàng phát hành thẻ tín dụng loại mới. Kỹ sư kích hoạt `dex-machine-learning-data-drift`, chạy script tính PSI và phát hiện đặc trưng `transaction_velocity_hour` có $PSI = 0.42$ do hành vi quẹt thẻ một chạm nhanh hơn trước, kích hoạt cập nhật lại mô hình và phục hồi tỷ lệ phát hiện gian lận về 94%."
    },

    # --- GROUP AB: Native, Graphics & Game Engineering ---
    {
        "id": "dex-chess-engine-search-testing",
        "index": 271,
        "group": "Group AB",
        "domain": "Native, Graphics & Game Engineering",
        "description": "Design deterministic search verification suites for chess engines and tree search algorithms, verifying perft move generation correctness, alpha-beta pruning invariants, transposition table hits, and quiescence stability. Use when engineering game engines, minimax agents, or combinatorial search trees.",
        "purpose": "Thiết kế và xây dựng bộ kiểm thử xác minh thuật toán tìm kiếm cây trò chơi và động cơ cờ vua (Chess Engine Search Testing); kiểm chứng tính đúng đắn của hàm sinh nước đi bằng kiểm thử Perft (Performance Test), bảo toàn các bất biến của thuật toán tỉa cành Alpha-Beta (Alpha-Beta Pruning Invariants), tỷ lệ trúng bảng chuyển vị (Transposition Table Hits) và tính ổn định của tìm kiếm tĩnh (Quiescence Search).",
        "when_use": [
            "Khi lập trình động cơ cờ vua, cờ vây hoặc các thuật toán tìm kiếm Minimax cho game đối kháng.",
            "Khi tối ưu hóa thuật toán tỉa cành Alpha-Beta và cần đảm bảo không cắt bỏ nhầm các nước đi tối ưu.",
            "Khi kiểm tra tính đúng đắn tuyệt đối của bộ sinh nước đi hợp lệ (Move Generator) tại các thế cờ đặc biệt (phong cấp, nhập thành, bắt tốt qua đường)."
        ],
        "when_not_use": [
            "Khi xây dựng các game casual 2D đơn giản không có logic tìm kiếm cây nước đi thông minh.",
            "Khi kiểm thử giao diện đồ họa bên ngoài của bàn cờ."
        ],
        "prereqs": "Động cơ cờ viết bằng C++, Rust hoặc Go; bảng thế cờ tiêu chuẩn FEN; bộ dữ liệu chuẩn Perft (Perft Benchmark Suite).",
        "concepts": [
            "Perft (Performance Test): Thuật toán đếm tổng số lượng nút lá (Leaf Nodes) tại một độ sâu tìm kiếm nhất định để xác minh bộ sinh nước đi chuẩn xác 100%.",
            "Alpha-Beta Invariant: Đảm bảo điểm số tìm kiếm với cửa sổ hẹp $[\\alpha, \\beta]$ luôn đồng nhất với tìm kiếm toàn diện khi điểm số nằm trong khoảng cửa sổ.",
            "Transposition Table Zobrist Hashing: Sử dụng mã băm Zobrist 64-bit để lưu trữ và tái sử dụng kết quả đánh giá các thế cờ trùng lặp qua các nhánh đi khác nhau."
        ],
        "steps": [
            "Nạp các thế cờ FEN kinh điển (thế cờ ban đầu, thế cờ Kiwipete nhiều va chạm, thế cờ tàn cuộc phong cấp).",
            "Chạy kiểm thử Perft đệ quy từ độ sâu 1 đến độ sâu 6, so sánh số lượng nước đi với bảng số liệu chuẩn quốc tế.",
            "Kiểm tra tính nhất quán của bảng chuyển vị Transposition Table (tránh xung đột băm làm sai lệch nước đi).",
            "Xác minh thuật toán Quiescence Search để giải quyết triệt tiêu hiệu ứng chân trời (Horizon Effect).",
            "Xuất biên bản kiểm thử xác minh động cơ cờ `PERFT_VERIFICATION_REPORT.md`."
        ],
        "code_lang": "rust",
        "code_example": """// Perft (Performance Test) Move Generation Verifier in Rust
pub fn perft(depth: u32, board: &mut Board) -> u64 {
    if depth == 0 {
        return 1;
    }

    let mut nodes: u64 = 0;
    let moves = board.generate_legal_moves();

    for m in moves {
        board.make_move(m);
        nodes += perft(depth - 1, board);
        board.undo_move(m);
    }

    nodes
}

// Verification assertion against standard Kiwipete position at depth 4
// Expected nodes: 4,085,603
#[test]
fn test_kiwipete_depth_4() {
    let mut board = Board::from_fen("r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1");
    assert_eq!(perft(4, &mut board), 4085603);
}""",
        "antipatterns": [
            "Bỏ qua kiểm thử Perft trên các thế cờ phức tạp, dẫn đến lỗi sót nước đi bắt tốt qua đường (En Passant) chỉ lộ ra sau hàng triệu ván đấu.",
            "Lưu điểm số vào bảng Transposition Table mà không lưu độ sâu tìm kiếm, khiến lượt tìm kiếm nông ghi đè lên kết quả tìm kiếm sâu.",
            "Thuật toán tỉa cành Null Move Pruning bị lỗi cắt tỉa trong tình huống Zugzwang (tình thế bắt buộc phải đi nước cờ xấu)."
        ],
        "quality_gates": [
            "QG-01: Vượt qua 100% các bài kiểm tra Perft chuẩn quốc tế từ độ sâu 1 đến độ sâu 5 với sai số bằng 0.",
            "QG-02: Tốc độ sinh nước đi và tìm kiếm đạt tối thiểu 2 triệu nút/giây trên một luồng CPU hiện đại.",
            "QG-03: Tỉ lệ trúng bảng chuyển vị Transposition Table duy trì trên 45% trong các lượt tìm kiếm trung cuộc."
        ],
        "security": "Xử lý an toàn chuỗi ký tự FEN đầu vào để ngăn chặn lỗi tràn bộ đệm hoặc tấn công từ chối dịch vụ thông qua chuỗi thế cờ độc hại.",
        "deliverables": [
            "Bộ kịch bản kiểm thử Perft toàn diện `perft_suite.rs`.",
            "Báo cáo hiệu năng và tính đúng đắn của thuật toán tìm kiếm cờ."
        ],
        "related": ["dex-simulation-determinism", "dex-game-loop-timing", "dex-algorithm-optimization"],
        "scenario": "Phát triển động cơ cờ vua tự viết bằng Rust. Động cơ thỉnh thoảng đi các nước cờ ngớ ngẩn khi gần hết giờ. Kỹ sư kích hoạt `dex-chess-engine-search-testing`, chạy bộ kiểm thử Perft trên thế cờ Kiwipete, phát hiện hàm sinh nước đi bị sót điều kiện khi vua bị chiếu đôi, sửa lỗi và đưa sức mạnh động cơ tăng thêm 150 điểm Elo."
    },
    {
        "id": "dex-simulation-determinism",
        "index": 272,
        "group": "Group AB",
        "domain": "Native, Graphics & Game Engineering",
        "description": "Engineer bit-level deterministic simulation loops using fixed-point arithmetic, isolated PRNG streams, and zero-float divergence across heterogeneous OS architectures (Windows/Linux/macOS). Use when developing lockstep multiplayer games, physics replays, or scientific simulations.",
        "purpose": "Thiết kế và hiện thực hóa các vòng lặp mô phỏng có tính xác định tuyệt đối đến từng bit (Bit-Level Deterministic Simulation Loops); ứng dụng số học dấu phẩy tĩnh (Fixed-Point Arithmetic) triệt tiêu sai số dấu phẩy động (Float Divergence), luồng sinh số ngẫu nhiên cô lập (Seeded PRNG) và độc lập hoàn toàn với kiến trúc hệ điều hành (Windows, Linux, macOS); phục vụ các game nhiều người chơi đồng bộ khóa bước (Lockstep Multiplayer) và hệ thống phát lại mô phỏng vật lý.",
        "when_use": [
            "Khi xây dựng game chiến thuật thời gian thực (RTS) hoặc game đối kháng sử dụng mô hình mạng Lockstep hoặc Rollback Netcode (GGPO).",
            "Khi phát lại một trận đấu từ tệp ghi nhật ký thao tác (Input Replay) mà kết quả giữa hai máy tính khác nhau bị phân kỳ (Desync).",
            "Khi chạy các mô phỏng vật lý khoa học đòi hỏi kết quả lặp lại hoàn toàn trùng khớp 100% trên mọi nền tảng."
        ],
        "when_not_use": [
            "Khi game chơi đơn thông thường không có tính năng phát lại và không cần đồng bộ qua mạng.",
            "Khi các ứng dụng web kinh doanh thông thường không liên quan đến mô phỏng vật lý."
        ],
        "prereqs": "Thư viện toán học số thực dấu phẩy tĩnh (Fixed-point math như `Fixed64` hoặc `fpm`), bộ sinh số ngẫu nhiên xác định (Xoshiro256** hoặc PCG).",
        "concepts": [
            "Floating-Point Non-Determinism: Phép tính số thực dấu phẩy động `float/double` (IEEE 754) cho ra các kết quả khác nhau ở các bit cuối trên các CPU Intel, AMD, ARM và các mức cờ tối ưu của trình biên dịch.",
            "Lockstep State Synchronization: Chỉ truyền các nút bấm của người chơi qua mạng thay vì truyền tọa độ; tất cả các máy khách tự tính toán và ra kết quả giống hệt nhau.",
            "Desync Detection Checksum: Tính toán mã băm trạng thái thế giới (State Hash) ở mỗi khung hình để phát hiện sự phân kỳ ngay từ khung hình đầu tiên."
        ],
        "steps": [
            "Thay thế toàn bộ kiểu dữ liệu `float` và `double` trong logic mô phỏng bằng kiểu số thực dấu phẩy tĩnh `fp64` (Q32.32 hoặc Q48.16).",
            "Khởi tạo bộ sinh số ngẫu nhiên PRNG có hạt giống (Seed) được lưu trong trạng thái thế giới.",
            "Thực thi cập nhật trạng thái theo bước thời gian cố định (Fixed Delta Time).",
            "Tính toán mã băm trạng thái toàn cục `state_hash` sau mỗi 60 khung hình mô phỏng.",
            "Chạy mô phỏng 10,000 khung hình trên cả Windows x86-64 và Linux ARM64 để đối chiếu mã băm trạng thái."
        ],
        "code_lang": "cpp",
        "code_example": """// Fixed-Point 32.32 Deterministic Vector Implementation
#include <cstdint>

struct Fixed64 {
    int64_t raw;
    static constexpr int64_t SCALE = 1LL << 32;

    static Fixed64 from_int(int32_t val) { return { static_cast<int64_t>(val) * SCALE }; }
    Fixed64 operator+(const Fixed64& o) const { return { raw + o.raw }; }
    Fixed64 operator*(const Fixed64& o) const { return { (raw * o.raw) / SCALE }; }
};

struct DeterministicEntity {
    Fixed64 posX;
    Fixed64 posY;
    Fixed64 velX;
    Fixed64 velY;

    void tick() {
        posX = posX + velX;
        posY = posY + velY;
    }
};""",
        "antipatterns": [
            "Dùng `Math.random()` hoặc hàm ngẫu nhiên của hệ điều hành `rand()` bên trong logic gameplay đồng bộ lockstep.",
            "Sử dụng kiểu dữ liệu `float` cho vị trí và vận tốc trong game đồng bộ mạng lockstep.",
            "Duyệt qua các phần tử của bảng băm `std::unordered_map` mà không sắp xếp (thứ tự duyệt phần tử không xác định giữa các nền tảng)."
        ],
        "quality_gates": [
            "QG-01: Mã băm trạng thái (State Checksum) trùng khớp 100% từng bit sau 50,000 khung hình mô phỏng giữa Windows và Linux.",
            "QG-02: 100% các phép tính toán học trong logic trò chơi sử dụng Fixed-Point Math.",
            "QG-03: Tệp ghi lại thao tác người dùng (Replay file) phát lại ra kết quả trận đấu giống hệt nhau 100 lần liên tiếp."
        ],
        "security": "Ngăn chặn các phần mềm gian lận (Speedhack) can thiệp vào bộ đếm thời gian hệ thống bằng cách xác thực tính nhất quán của chuỗi tick từ client.",
        "deliverables": [
            "Thư viện toán học số học xác định `FixedPointMath.hpp`.",
            "Bộ test tự động kiểm tra hiện tượng phân kỳ trạng thái `desync_detector.py`."
        ],
        "related": ["dex-chess-engine-search-testing", "dex-physics-engine-validation", "dex-game-loop-timing"],
        "scenario": "Game chiến thuật nhiều người chơi bị lỗi mất đồng bộ (Desync) ngẫu nhiên mỗi khi người chơi trên PC thi đấu với người chơi trên iPhone. Kỹ sư kích hoạt `dex-simulation-determinism`, phát hiện việc tính toán góc quay dùng `std::sin(float)` cho ra kết quả lệch 1 bit ở số thập phân thứ 7 giữa chip Intel và Apple Silicon. Thay thế bằng bảng sin tra cứu Fixed-Point, triệt tiêu hoàn toàn lỗi desync."
    },
    {
        "id": "dex-physics-engine-validation",
        "index": 273,
        "group": "Group AB",
        "domain": "Native, Graphics & Game Engineering",
        "description": "Validate 2D/3D rigid-body physics engines, measuring energy conservation invariants, continuous collision detection (CCD) tunneling prevention, solver constraint stability, and restitution accuracy. Use when engineering physics simulations, robotics controllers, or action game mechanics.",
        "purpose": "Kiểm chứng và thẩm định tính đúng đắn của động cơ vật lý vật rắn (Rigid-Body Physics Engine Validation); đo lường sự bảo toàn cơ năng và động lượng (Energy & Momentum Conservation), cơ chế phát hiện va chạm liên tục (Continuous Collision Detection - CCD) chống hiện tượng vật thể xuyên tường (Tunneling), độ ổn định của bộ giải ràng buộc (Solver Constraints) và hệ số phục hồi va chạm (Restitution).",
        "when_use": [
            "Khi xây dựng hoặc tích hợp động cơ vật lý (Box2D, PhysX, Jolt Physics hoặc Rapier).",
            "Khi các vật thể di chuyển ở tốc độ cao bị xuyên thủng qua bức tường mỏng mà không phát sinh va chạm.",
            "Khi các chồng hộp hoặc vật thể xếp chồng lên nhau bị rung lắc dữ dội hoặc tự động nảy tung lên không rõ lý do."
        ],
        "when_not_use": [
            "Khi làm game theo lượt hoặc game giao diện không có yếu tố tương tác vật lý.",
            "Khi mô phỏng vật lý hạt hoặc biến dạng chất lỏng quy mô vi mô (CFD)."
        ],
        "prereqs": "Động cơ vật lý mục tiêu (Rapier, Box2D hoặc PhysX), kịch bản kiểm thử vật lý tiêu chuẩn (Stacking test, High-speed projectile test).",
        "concepts": [
            "Tunneling Effect: Hiện tượng viên đạn hoặc xe đua di chuyển một quãng đường quá lớn trong một bước thời gian $\\Delta t$, nhảy cóc từ phía trước tường sang phía sau tường mà không có điểm giao cắt tại thời điểm rời rạc.",
            "Continuous Collision Detection (CCD): Sử dụng thuật toán quét khối (Swept Volume) hoặc kiểm tra thời gian va chạm (Time of Impact - TOI) để bắt va chạm liên tục trên đoạn đường di chuyển.",
            "Constraint Solver Jitter: Hiện tượng dao động số học trong bộ giải ràng buộc tiếp xúc (Iterative Impulse Solver) khi giải quyết các chồng vật thể nặng xếp lên nhau."
        ],
        "steps": [
            "Xây dựng kịch bản kiểm thử viên đạn siêu tốc bắn vào tấm tường mỏng 1cm ở các góc nghiêng khác nhau.",
            "Kiểm tra xem cờ CCD có phát hiện chính xác thời điểm va chạm TOI hay không.",
            "Tạo kịch bản kiểm thử chồng 20 hộp chữ nhật để đo lường độ ổn định của bộ giải tiếp xúc và độ lún hình học (Penetration Slop).",
            "Tính toán tổng cơ năng (Động năng + Thế năng) của con lắc đơn qua 1,000 chu kỳ dao động để đo độ rò rỉ năng lượng.",
            "Lập biên bản đánh giá tính ổn định của động cơ vật lý `PHYSICS_STABILITY_REPORT.md`."
        ],
        "code_lang": "cpp",
        "code_example": """// Validating Energy Conservation in Rigid-Body Physics
#include <iostream>
#include <cmath>

struct PhysicalState {
    double kineticEnergy;
    double potentialEnergy;
    double totalEnergy() const { return kineticEnergy + potentialEnergy; }
};

bool validate_energy_conservation(const PhysicalState& initial, const PhysicalState& current, double tolerance = 0.01) {
    double initialE = initial.totalEnergy();
    double currentE = current.totalEnergy();
    double drift = std::abs(currentE - initialE) / initialE;
    return drift <= tolerance;
}""",
        "antipatterns": [
            "Tăng bước thời gian vật lý $\\Delta t$ quá lớn (ví dụ 100ms) để tiết kiệm CPU khiến toàn bộ hệ thống vật lý bị phát nổ (Explosion bug).",
            "Bỏ qua bước cấu hình CCD cho các vật thể nhỏ di chuyển nhanh khiến người chơi bị rớt xuống dưới đáy bản đồ.",
            "Đặt trọng lượng giữa hai vật thể nối với nhau chênh lệch hàng triệu lần (ví dụ vật 1g nối với vật 1,000,000kg) làm sập bộ giải tiếp xúc."
        ],
        "quality_gates": [
            "QG-01: Không có hiện tượng xuyên tường (Zero Tunneling) ở vận tốc vật thể lên tới 500 m/s khi bật CCD.",
            "QG-02: Chồng 15 hộp vật lý đứng yên ổn định không bị trôi dạt hoặc rung lắc trong 60 giây.",
            "QG-03: Sự suy giảm cơ năng của hệ dao động không ma sát không vượt quá 0.5% sau 1,000 bước tính toán."
        ],
        "security": "Đặt giới hạn vận tốc tối đa và số lượng va chạm tối đa cho mỗi khung hình để ngăn ngừa kẻ gian làm sập server game bằng cách tạo hàng nghìn va chạm cùng lúc.",
        "deliverables": [
            "Bộ kịch bản kiểm thử độ ổn định vật lý `PhysicsVerificationSuite.cpp`.",
            "Báo cáo thẩm định an toàn động cơ vật lý `PHYSICS_STABILITY_REPORT.md`."
        ],
        "related": ["dex-simulation-determinism", "dex-game-loop-timing", "dex-rendering-frame-pacing"],
        "scenario": "Game đua xe bắn súng gặp lỗi người chơi bắn tên lửa thường xuyên bay xuyên qua vỏ xe tăng của đối thủ mà không nổ. Kỹ sư kích hoạt `dex-physics-engine-validation`, phát hiện tên lửa di chuyển 12 mét mỗi frame trong khi vỏ xe chỉ dày 0.2 mét và chưa bật CCD. Kích hoạt tính năng Swept Shape CCD cho tên lửa, triệt tiêu hoàn toàn 100% hiện tượng xuyên vật thể."
    },
    {
        "id": "dex-game-loop-timing",
        "index": 274,
        "group": "Group AB",
        "domain": "Native, Graphics & Game Engineering",
        "description": "Implement rock-solid game loop architectures with fixed timestep physics updates, accumulator buffer smoothing, variable frame rendering interpolation, and spiral-of-death panics. Use when engineering deterministic game runtimes, interactive simulations, or VR render loops.",
        "purpose": "Thiết kế và hiện thực hóa kiến trúc vòng lặp trò chơi (Game Loop Architecture) vững chắc như bàn thạch; tách bạch hoàn toàn giữa bước cập nhật vật lý theo thời gian cố định (Fixed Timestep Update) và bước kết xuất đồ họa theo thời gian biến thiên (Variable Frame Rendering); ứng dụng bộ đệm tích lũy thời gian (Time Accumulator) kèm nội suy trạng thái (State Interpolation) và cơ chế phòng chống vòng xoáy tử thần (Spiral-of-Death Panic).",
        "when_use": [
            "Khi xây dựng game engine hoặc ứng dụng đồ họa tương tác thời gian thực từ đầu.",
            "Khi chuyển động của nhân vật game bị giật cục hoặc chạy nhanh gấp đôi trên màn hình tần số quét cao (144Hz/240Hz).",
            "Khi máy tính cấu hình yếu bị sập hoàn toàn do rơi vào vòng lặp cập nhật vật lý không hồi kết (Spiral of Death)."
        ],
        "when_not_use": [
            "Khi phát triển các ứng dụng form doanh nghiệp truyền thống cập nhật theo sự kiện bấm chuột.",
            "Khi xây dựng các dịch vụ backend xử lý theo lô."
        ],
        "prereqs": "Đồng hồ đo thời gian độ chính xác cao (`std::chrono::high_resolution_clock` hoặc `performance.now()`), kiến thức về bài toán 'Fix Your Timestep!'.",
        "concepts": [
            "Fixed Timestep for Physics: Cập nhật vật lý và logic gameplay luôn ở một khoảng thời gian cố định chính xác (ví dụ $\\Delta t = 1/60s = 16.66ms$) để bảo toàn tính xác định.",
            "Time Accumulator & Interpolation: Tích lũy thời gian thực tế đã trôi qua và chạy số lượng bước cố định tương ứng; nội suy hình ảnh giữa trạng thái cũ và mới bằng tỷ lệ dư thừa $\\alpha = accumulator / dt$.",
            "Spiral of Death Prevention: Giới hạn số lượng bước cập nhật tối đa trong một khung hình (ví dụ `maxSubSteps = 5`) để ngăn CPU bị quá tải khi frame render bị trễ."
        ],
        "steps": [
            "Khởi tạo đồng hồ đo thời gian có độ chính xác micro-giây.",
            "Đo lường thời gian trôi qua thực tế kể từ khung hình trước (`frameTime`).",
            "Cộng dồn `frameTime` vào biến tích lũy `accumulator`.",
            "Chạy vòng lặp cập nhật logic cố định `while (accumulator >= dt)` và trừ dần `accumulator`.",
            "Tính toán hệ số nội suy $\\alpha$ và gọi hàm kết xuất đồ họa `render(alpha)`."
        ],
        "code_lang": "cpp",
        "code_example": """// Canonical 'Fix Your Timestep' Game Loop Implementation
#include <chrono>

void run_game_loop() {
    using clock = std::chrono::high_resolution_clock;
    auto previousTime = clock::now();
    double accumulator = 0.0;
    const double dt = 1.0 / 60.0; // 60Hz fixed physics update
    const double maxFrameTime = 0.25; // Clamp to prevent Spiral of Death

    while (isRunning) {
        auto currentTime = clock::now();
        std::chrono::duration<double> elapsed = currentTime - previousTime;
        previousTime = currentTime;

        double frameTime = std::min(elapsed.count(), maxFrameTime);
        accumulator += frameTime;

        while (accumulator >= dt) {
            update_physics(dt);
            accumulator -= dt;
        }

        const double alpha = accumulator / dt;
        render_interpolated(alpha);
    }
}""",
        "antipatterns": [
            "Nhân trực tiếp biến thời gian `delta_time` vào vị trí nhân vật trong hàm render (`x += speed * dt`) khiến vật lý bị lỗi nhảy cóc khi máy tính bị lag.",
            "Không giới hạn thời gian khung hình tối đa, dẫn đến việc khi máy tính bị lag 1 giây, vòng lặp cố chạy 60 bước vật lý làm máy tính càng lag hơn và sập luôn ứng dụng (Spiral of Death).",
            "Không nội suy trạng thái khi render trên màn hình 144Hz, khiến hình ảnh nhìn bị giật rung dù FPS đo được rất cao."
        ],
        "quality_gates": [
            "QG-01: Logic vật lý chạy ở tốc độ cập nhật cố định tuyệt đối bất kể màn hình hiển thị ở 30Hz, 60Hz hay 144Hz.",
            "QG-02: Không bao giờ rơi vào vòng xoáy tử thần khi tạm dừng cửa sổ ứng dụng 5 giây.",
            "QG-03: Chuyển động hiển thị mượt mà không có hiện tượng rung giật vi mô (Micro-stuttering) nhờ hệ số nội suy $\\alpha$."
        ],
        "security": "Chống việc người dùng can thiệp vào đồng hồ hệ điều hành để tăng tốc độ nhân vật trong game (Speed-hacking) bằng cách kiểm tra bước thời gian từ máy chủ.",
        "deliverables": [
            "Kiến trúc vòng lặp game hoàn chỉnh `GameLoopEngine.cpp`.",
            "Bộ quy chuẩn nội suy trạng thái đồ họa theo hệ số alpha."
        ],
        "related": ["dex-simulation-determinism", "dex-rendering-frame-pacing", "dex-real-time-input-latency"],
        "scenario": "Một tựa game hành động khi chạy trên màn hình MacBook Pro 120Hz thì nhân vật di chuyển nhanh gấp đôi so với trên máy tính văn phòng 60Hz. Kỹ sư kích hoạt `dex-game-loop-timing`, triển khai vòng lặp Fixed Timestep 60Hz kết hợp nội suy Alpha cho bước render, giúp nhân vật di chuyển đúng tốc độ thiết kế trên mọi loại màn hình với độ mượt mà tuyệt đối."
    },
    {
        "id": "dex-rendering-frame-pacing",
        "index": 275,
        "group": "Group AB",
        "domain": "Native, Graphics & Game Engineering",
        "description": "Diagnose frame time variance, 1% low FPS, pipeline presentation latencies, and display VSync synchronization glitches. Use when eliminating micro-stutters, tuning Android/Vulkan frame pacers, or optimizing VR motion-to-photon latency.",
        "purpose": "Đo lường, chẩn đoán và đồng nhất hóa nhịp độ hiển thị khung hình (Rendering Frame Pacing); triệt tiêu phương sai thời gian khung hình (Frame Time Variance), tối ưu hóa chỉ số FPS thấp 1% (1% Low FPS), độ trễ đường ống hiển thị (Presentation Latency) và các lỗi không đồng bộ làm rách hình (VSync Tearing / Jitter); phục vụ mang lại trải nghiệm thị giác mượt mà không bị giật vi mô trên Android, Vulkan, DirectX và kính thực tế ảo VR.",
        "when_use": [
            "Khi game đo được chỉ số FPS trung bình là 60 nhưng người chơi vẫn cảm thấy hình ảnh bị giật khựng từng đợt (Micro-stutters).",
            "Khi tối ưu hóa game trên thiết bị di động Android sử dụng thư viện Android Frame Pacing Library (Swappy).",
            "Khi xây dựng ứng dụng thực tế ảo (VR) cần đảm bảo độ trễ từ chuyển động đến điểm ảnh (Motion-to-Photon Latency) dưới 20ms để chống say xe."
        ],
        "when_not_use": [
            "Khi ứng dụng không có hoạt cảnh chuyển động liên tục.",
            "Khi kiểm tra hiệu năng tính toán thuật toán không hiển thị đồ họa."
        ],
        "prereqs": "Công cụ đo lường thời gian hiển thị khung hình (PresentMon, CapFrameX hoặc Android GPU Inspector), card đồ họa hỗ trợ VSync/G-Sync/FreeSync.",
        "concepts": [
            "1% Low FPS Metric: Chỉ số trung bình của 1% các khung hình chạy chậm nhất trong phiên chơi; phản ánh chân thực độ mượt mà của game hơn nhiều so với chỉ số FPS trung bình.",
            "Buffer Queuing Latency: Số lượng khung hình nằm chờ trong hàng đợi hiển thị (Triple Buffering làm tăng FPS nhưng tăng độ trễ điều khiển con trỏ).",
            "Tearing vs Stuttering: Rách hình xảy ra khi GPU nạp khung hình mới giữa lúc màn hình đang quét tia; giật khựng xảy ra khi GPU bị lỡ nhịp quét VSync của màn hình."
        ],
        "steps": [
            "Thu thập biểu đồ phân bố thời gian từng khung hình (Frame Time Graph) bằng PresentMon.",
            "Nhận diện các đỉnh gai thời gian khung hình vượt quá 16.6ms (cho màn 60Hz) hoặc 8.3ms (cho màn 120Hz).",
            "Cấu hình cơ chế đồng bộ khung hình mượt mà (chế độ Mailbox hoặc FIFO trong Vulkan / DirectX).",
            "Tích hợp thư viện điều phối nhịp độ khung hình (Frame Pacer) để đồng bộ nhịp đẩy frame khớp với nhịp quét của màn hình.",
            "Xác nhận chỉ số 1% Low FPS được nâng lên sát với chỉ số FPS trung bình."
        ],
        "code_lang": "cpp",
        "code_example": """// Vulkan Frame Pacing Present Mode Selection
#include <vulkan/vulkan.h>
#include <vector>

VkPresentModeKHR selectOptimalPresentMode(const std::vector<VkPresentModeKHR>& availableModes) {
    // Prefer Mailbox (Triple Buffering without tearing & low latency)
    for (const auto& mode : availableModes) {
        if (mode == VK_PRESENT_MODE_MAILBOX_KHR) {
            return mode;
        }
    }
    // Fallback to FIFO (Standard VSync, guaranteed support)
    return VK_PRESENT_MODE_FIFO_KHR;
}""",
        "antipatterns": [
            "Chỉ tự hào khoe chỉ số FPS trung bình đạt 120 trong khi đồ thị frame time liên tục nhảy nhót từ 8ms lên 45ms khiến game thủ cảm thấy giật lag nặng.",
            "Để hàng đợi khung hình GPU (Max Pre-rendered Frames) lên tới 4 hoặc 5 khung hình làm tăng độ trễ điều khiển chuột gây cảm giác lướt trên băng.",
            "Bỏ qua việc khóa tốc độ khung hình (Frame Rate Limiting) dẫn đến việc GPU chạy hết 100% công suất gây quá nhiệt và bóp nghẹt xung nhịp (Thermal Throttling)."
        ],
        "quality_gates": [
            "QG-01: Phương sai thời gian khung hình duy trì dưới 1.5ms trong suốt 99% thời gian chơi.",
            "QG-02: Chỉ số 1% Low FPS đạt tối thiểu 85% giá trị của FPS trung bình.",
            "QG-03: Không có hiện tượng rách hình (Tearing) hoặc lỡ nhịp quét VSync trên màn hình thử nghiệm."
        ],
        "security": "Không sử dụng các tiện ích can thiệp hook vào API đồ họa không rõ nguồn gốc để đo đạc có thể bị hệ thống chống hack (Anti-cheat) cấm tài khoản.",
        "deliverables": [
            "Bản phân tích thời gian khung hình `FRAME_PACING_AUDIT.md`.",
            "Module cấu hình đồng bộ hiển thị màn hình chuẩn `FramePacerConfig.cpp`."
        ],
        "related": ["dex-game-loop-timing", "dex-gpu-shader-profiling", "dex-real-time-input-latency"],
        "scenario": "Game đối kháng 3D trên Android có FPS trung bình 60 nhưng người chơi liên tục than phiền bị khựng hình khi ra đòn. Kỹ sư kích hoạt `dex-rendering-frame-pacing`, dùng Android GPU Inspector phát hiện bộ đệm hiển thị bị trễ nhịp so với tần số quét của màn hình điện thoại, tích hợp thư viện Swappy Frame Pacing, đưa chỉ số 1% Low từ 28 FPS lên thẳng 58 FPS mượt mà."
    },
    {
        "id": "dex-gpu-shader-profiling",
        "index": 276,
        "group": "Group AB",
        "domain": "Native, Graphics & Game Engineering",
        "description": "Profile and optimize vertex, fragment, and compute shaders, minimizing register pressure, arithmetic intensity bottlenecks, texture bandwidth stalls, and branch divergence. Use when optimizing GPU performance across desktop GPUs, mobile chips, and WebGL/WebGPU pipelines.",
        "purpose": "Lập hồ sơ hiệu năng (Profiling) và tối ưu hóa mã lệnh đổ bóng đồ họa GPU (Vertex, Fragment và Compute Shaders); giảm thiểu áp lực thanh ghi (Register Pressure), triệt tiêu các nút thắt cường độ số học (Arithmetic Bottlenecks), độ trễ băng thông nạp vân bề mặt (Texture Bandwidth Stalls) và hiện tượng phân kỳ rẽ nhánh luồng (Branch Divergence); phục vụ tối ưu hóa đồ họa trên chip di động và máy tính.",
        "when_use": [
            "Khi GPU liên tục chạy ở mức 100% công suất làm tụt tốc độ khung hình của trò chơi.",
            "Khi mã shader phức tạp chứa quá nhiều nhánh rẽ điều kiện khiến các lõi GPU bị nhàn rỗi chờ đợi.",
            "Khi tối ưu hóa game 3D cho các dòng điện thoại di động chip đồ họa yếu (Mali, Adreno)."
        ],
        "when_not_use": [
            "Khi ứng dụng bị nghẽn ở luồng CPU chính (CPU-bound) chứ không phải do GPU.",
            "Khi tinh chỉnh các đoạn mã CSS animation đơn giản trên giao diện web."
        ],
        "prereqs": "Công cụ phân tích GPU chuyên dụng (RenderDoc, NVIDIA Nsight Graphics hoặc AMD Radeon Developer Tool Suite), mã nguồn Shader (GLSL, HLSL, WGSL hoặc SPIR-V).",
        "concepts": [
            "Warp / Wavefront Branch Divergence: Khi các luồng trong cùng một Warp (32 luồng) rẽ sang hai nhánh `if / else` khác nhau, GPU buộc phải thực thi cả hai nhánh tuần tự, làm giảm một nửa hiệu năng.",
            "Register Pressure & Occupancy: Shader sử dụng quá nhiều biến cục bộ làm tăng số thanh ghi cần dùng trên mỗi luồng, khiến GPU không thể chạy song song số lượng luồng tối đa.",
            "Texture Fetch Latency Hiding: Tận dụng các phép tính số học ALUs để che giấu độ trễ hàng trăm chu kỳ khi nạp dữ liệu ảnh từ bộ nhớ VRAM."
        ],
        "steps": [
            "Chụp lại khung hình đồ họa (Capture Frame) bằng công cụ RenderDoc.",
            "Xác định các lệnh vẽ (Draw Calls) tốn nhiều thời gian GPU nhất trên đường ống.",
            "Phân tích mã hợp ngữ shader (SPIR-V hoặc ISA) để kiểm tra số lượng thanh ghi sử dụng (VGPRs / SGPRs).",
            "Loại bỏ các nhánh rẽ điều kiện động, chuyển sang dùng hàm toán học nội suy (`mix`, `step`, `clamp`).",
            "Đo lường lại thời gian thực thi của shader trên GPU để xác nhận mức cải thiện."
        ],
        "code_lang": "glsl",
        "code_example": """// Shader Optimization: Eliminating Dynamic Branch Divergence
// SLOW: Dynamic branch divergence inside fragment shader
// if (lightIntensity > 0.5) { color = vec3(1.0); } else { color = vec3(0.0); }

// FAST: Branchless math using step()
vec3 calculateOptimizedLighting(float lightIntensity, vec3 baseColor) {
    float factor = step(0.5, lightIntensity);
    return mix(vec3(0.0), baseColor, factor);
}""",
        "antipatterns": [
            "Sử dụng các vòng lặp `for` có số bước lặp động thay đổi theo từng pixel khiến các luồng trong GPU bị lệch nhịp nghiêm trọng.",
            "Thực hiện các phép tính toán ma trận giống hệt nhau trong Fragment Shader (chạy hàng triệu lần cho mỗi pixel) thay vì tính trước một lần ở Vertex Shader.",
            "Nạp các texture độ phân giải khổng lồ 4K mà không có Mipmaps làm nghẽn băng thông bộ nhớ VRAM."
        ],
        "quality_gates": [
            "QG-01: Thời gian thực thi của shader chính giảm tối thiểu 30% sau khi tối ưu hóa.",
            "QG-02: Không còn nhánh rẽ phân kỳ động bên trong các vòng lặp tính toán nặng của Fragment Shader.",
            "QG-03: Mức chiếm dụng GPU (GPU Occupancy) đạt tối thiểu 75% trên kiến trúc mục tiêu."
        ],
        "security": "Kiểm tra giới hạn chỉ số mảng (Array Bounds Check) trong Compute Shader để ngăn ngừa việc đọc/ghi tràn bộ nhớ VRAM làm sập trình điều khiển card đồ họa.",
        "deliverables": [
            "Mã nguồn shader đã được tối ưu hóa `optimized_shading.frag`.",
            "Báo cáo phân tích hiệu năng shader từ RenderDoc/Nsight."
        ],
        "related": ["dex-rendering-frame-pacing", "dex-gpu-resource-lifetime", "dex-webgpu-rendering-fundamentals"],
        "scenario": "Trò chơi 3D bị tụt khung hình xuống 24 FPS mỗi khi bước vào khu vực có hiệu ứng sương mù ánh sáng. Kỹ sư kích hoạt `dex-gpu-shader-profiling`, dùng RenderDoc phân tích shader sương mù, phát hiện một nhánh rẽ `if` phức tạp chạy trên từng pixel, chuyển đổi sang phép tính toán không nhánh `step()` và giảm số thanh ghi từ 48 xuống 24, đưa FPS trở lại mức 60 mượt mà."
    },
    {
        "id": "dex-gpu-resource-lifetime",
        "index": 277,
        "group": "Group AB",
        "domain": "Native, Graphics & Game Engineering",
        "description": "Architect robust GPU memory allocators and resource lifetime managers across Vulkan, DirectX 12, and Metal, eliminating VRAM leaks, staging buffer stalls, and handling graphics device loss. Use when building AAA rendering engines, native CAD viewports, or compute pipelines.",
        "purpose": "Thiết kế kiến trúc quản lý vòng đời tài nguyên và bộ cấp phát bộ nhớ GPU (GPU Memory Allocator & Lifetime Management) trên các API đồ họa cấp thấp hiện đại: Vulkan, DirectX 12 và Metal; triệt tiêu hoàn toàn rò rỉ bộ nhớ đồ họa VRAM, tối ưu hóa các bộ đệm trung gian (Staging Buffers) và xử lý khôi phục sự cố mất thiết bị đồ họa (Device Loss Recovery).",
        "when_use": [
            "Khi phát triển động cơ kết xuất đồ họa hiệu năng cao sử dụng Vulkan (`vkAllocateMemory`) hoặc DirectX 12 (`ID3D12Resource`).",
            "Khi trò chơi bị sập với lỗi `VK_ERROR_OUT_OF_DEVICE_MEMORY` hoặc `DXGI_ERROR_DEVICE_REMOVED` sau một thời gian chơi dài.",
            "Khi cần tối ưu hóa tốc độ tải và giải phóng hàng nghìn texture mô hình 3D mà không làm khựng game."
        ],
        "when_not_use": [
            "Khi làm việc với các API đồ họa cấp cao tự động dọn rác như Three.js hoặc Babylon.js.",
            "Khi lập trình ứng dụng văn phòng thông thường."
        ],
        "prereqs": "Kiến thức về các loại bộ nhớ GPU (Device Local, Host Visible, Host Coherent), thư viện Vulkan Memory Allocator (VMA) hoặc D3D12MA.",
        "concepts": [
            "Sub-allocation from Large Heaps: Trình điều khiển GPU giới hạn số lần gọi cấp phát bộ nhớ trực tiếp (thường tối đa 4,096 lần); giải pháp chuẩn là cấp phát các khối VRAM lớn (256MB) và tự chia nhỏ (Sub-allocate) cho từng tài nguyên.",
            "Staging Buffer Ring: Bộ đệm trung gian nằm trên RAM CPU cho phép ghi dữ liệu nhanh và sử dụng lệnh DMA chuyển sang bộ nhớ siêu tốc của GPU trong nền.",
            "Device Loss Recovery Flow: Khi card màn hình bị tháo rời hoặc driver bị khởi động lại, phải giải phóng sạch toàn bộ tài nguyên cũ và tái tạo lại Swapchain và Pipeline."
        ],
        "steps": [
            "Tích hợp thư viện Vulkan Memory Allocator (VMA) vào dự án.",
            "Phân loại các tài nguyên theo mục đích sử dụng (Static Meshes, Dynamic Uniforms, Render Targets).",
            "Cấp phát các tài nguyên tĩnh vào vùng nhớ `VK_MEMORY_PROPERTY_DEVICE_LOCAL_BIT`.",
            "Sử dụng Staging Buffer dạng vòng tròn (Ring Buffer) để tải dữ liệu bất đồng bộ.",
            "Thiết lập cơ chế bắt mã lỗi `VK_ERROR_DEVICE_LOST` để thực hiện quy trình tái tạo tài nguyên an toàn."
        ],
        "code_lang": "cpp",
        "code_example": """// Safe GPU Memory Allocation using Vulkan Memory Allocator (VMA)
#include "vk_mem_alloc.h"

VkBuffer createGpuBuffer(VmaAllocator allocator, VkDeviceSize size, VkBufferUsageFlags usage) {
    VkBufferCreateInfo bufferInfo = { VK_STRUCTURE_TYPE_BUFFER_CREATE_INFO };
    bufferInfo.size = size;
    bufferInfo.usage = usage;
    bufferInfo.sharingMode = VK_SHARING_MODE_EXCLUSIVE;

    VmaAllocationCreateInfo allocInfo = {};
    allocInfo.usage = VMA_MEMORY_USAGE_AUTO_PREFER_DEVICE; // Prefer fast VRAM

    VkBuffer buffer;
    VmaAllocation allocation;
    vmaCreateBuffer(allocator, &bufferInfo, &allocInfo, &buffer, &allocation, nullptr);
    return buffer;
}""",
        "antipatterns": [
            "Gọi lệnh `vkAllocateMemory` trực tiếp cho từng tấm ảnh texture nhỏ vài KB làm cạn kiệt giới hạn cấp phát của driver và làm sập game.",
            "Quên giải phóng tài nguyên đồ họa khi chuyển đổi giữa các màn chơi, dẫn đến việc VRAM tăng lũy tiến đến khi đầy đĩa.",
            "Ghi dữ liệu từ CPU thẳng vào bộ nhớ Device Local của GPU mà không qua Staging Buffer khiến băng thông bị bóp nghẹt nghiêm trọng."
        ],
        "quality_gates": [
            "QG-01: Không có hiện tượng rò rỉ bộ nhớ VRAM (0 bytes leaked) sau khi chuyển đổi qua lại 10 màn chơi khác nhau.",
            "QG-02: 100% các tài nguyên tĩnh được nạp vào bộ nhớ Device Local thông qua Staging Buffer.",
            "QG-03: Khôi phục ứng dụng thành công sau khi giả lập sự kiện reset driver đồ họa."
        ],
        "security": "Xóa sạch dữ liệu trong các bộ đệm VRAM nhạy cảm trước khi tái sử dụng để ngăn ngừa rò rỉ hình ảnh giữa các tiến trình đồ họa khác nhau.",
        "deliverables": [
            "Lớp quản lý bộ nhớ GPU `GpuMemoryManager.cpp`.",
            "Quy trình xử lý sự cố mất thiết bị đồ họa `DeviceLossRecovery.hpp`."
        ],
        "related": ["dex-gpu-shader-profiling", "dex-webgpu-rendering-fundamentals", "dex-asset-pipeline-optimization"],
        "scenario": "Phần mềm mô phỏng bản vẽ kiến trúc 3D bị crash sau 30 phút sử dụng do ngốn hết 12GB VRAM card màn hình. Kỹ sư kích hoạt `dex-gpu-resource-lifetime`, tích hợp Vulkan Memory Allocator với cơ chế gộp khối và tự động dọn rác các mô hình khuất tầm nhìn, giảm mức tiêu thụ VRAM xuống ổn định ở 3.2GB và chấm dứt hoàn toàn hiện tượng sập phần mềm."
    },
    {
        "id": "dex-native-plugin-abi-testing",
        "index": 278,
        "group": "Group AB",
        "domain": "Native, Graphics & Game Engineering",
        "description": "Design cross-language C Foreign Function Interface (FFI) boundary tests, verifying struct memory layouts, calling conventions, string encoding boundaries, and pointer ownership transfer. Use when building native plugins for Node.js (N-API), Python (ctypes/CFFI), Unity, or Rust.",
        "purpose": "Thiết kế và xây dựng bộ kiểm thử ranh giới giao tiếp hàm ngoại lai (Foreign Function Interface - FFI) chuẩn C ABI xuyên ngôn ngữ; kiểm chứng tính tương thích của bố cục bộ nhớ cấu trúc (Struct Padding & Alignment), quy ước gọi hàm (`cdecl`, `stdcall`), ranh giới mã hóa chuỗi ký tự UTF-8/UTF-16 và quyền sở hữu con trỏ bộ nhớ (Pointer Ownership Transfer); ngăn ngừa các lỗi sập ứng dụng nghiêm trọng (Segmentation Faults) khi tích hợp module native C/C++/Rust vào Node.js, Python, C# Unity.",
        "when_use": [
            "Khi xây dựng thư viện native C++ hoặc Rust để nhúng vào ứng dụng Node.js (qua N-API) hoặc Python (qua ctypes).",
            "Khi tạo các plugin native cho động cơ game Unity (C# P/Invoke gọi thư viện C++ .dll/.so).",
            "Khi cập nhật phiên bản trình biên dịch native và cần đảm bảo không phá vỡ tính tương thích nhị phân (Binary Compatibility) với các ứng dụng máy khách."
        ],
        "when_not_use": [
            "Khi hai ứng dụng giao tiếp với nhau qua giao thức mạng HTTP hoặc gRPC (có ranh giới mạng cô lập).",
            "Khi làm việc hoàn toàn trong cùng một ngôn ngữ lập trình duy nhất."
        ],
        "prereqs": "Mã nguồn thư viện native C/C++/Rust, ứng dụng gọi cấp cao (Node.js/Python/C#), công cụ kiểm tra bố cục bộ nhớ (`offsetof`).",
        "concepts": [
            "C ABI Stability: Ngôn ngữ C được coi là ngôn ngữ giao tiếp chung phổ quát nhất; các ngôn ngữ cấp cao đều hỗ trợ gọi hàm theo chuẩn C ABI.",
            "Struct Alignment & Padding: Các trường dữ liệu trong struct được căn chỉnh theo bội số của kích thước (4 byte, 8 byte); nếu hai bên định nghĩa lệch nhau dù chỉ 1 byte đệm sẽ làm sai lệch toàn bộ dữ liệu.",
            "Memory Ownership Contract: Quy định rõ bên nào cấp phát bộ nhớ (Allocation) thì bên đó phải chịu trách nhiệm giải phóng bộ nhớ (Free), không bao giờ giải phóng con trỏ chéo ngôn ngữ."
        ],
        "steps": [
            "Định nghĩa giao diện công khai thuần túy theo chuẩn C với chỉ thị `extern \"C\"` và quy ước gọi hàm rõ ràng.",
            "Kiểm tra kích thước và độ dời (`sizeof` và `offsetof`) của từng trường trong struct ở cả hai ngôn ngữ.",
            "Viết hàm giải phóng bộ nhớ chuyên dụng do chính thư viện native cung cấp (`free_native_buffer`).",
            "Thực hiện truyền nhận chuỗi ký tự có kiểm tra độ dài và chuyển đổi mã hóa an toàn.",
            "Chạy bộ kiểm thử tự động với AddressSanitizer (ASan) để phát hiện rò rỉ hoặc đọc bộ nhớ ngoài phạm vi."
        ],
        "code_lang": "c",
        "code_example": """// C ABI Safe Export Interface Header (native_plugin.h)
#ifndef NATIVE_PLUGIN_H
#define NATIVE_PLUGIN_H

#include <stdint.h>

#ifdef _WIN32
  #define FFI_EXPORT __declspec(dllexport)
#else
  #define FFI_EXPORT __attribute__((visibility("default")))
#endif

#pragma pack(push, 8) // Enforce explicit 8-byte alignment
typedef struct {
    uint64_t entityId;
    double posX;
    double posY;
    int32_t health;
    int32_t padding; // Explicit padding
} EntityDataC;
#pragma pack(pop)

#ifdef __cplusplus
extern "C" {
#endif

FFI_EXPORT int32_t process_entities(const EntityDataC* entities, int32_t count);
FFI_EXPORT void free_string_buffer(char* ptr);

#ifdef __cplusplus
}
#endif

#endif""",
        "antipatterns": [
            "Truyền trực tiếp đối tượng C++ phức tạp (như `std::string` hoặc `std::vector`) qua ranh giới FFI (định dạng nội bộ của C++ STL thay đổi tùy theo từng trình biên dịch làm sập chương trình ngay lập tức).",
            "Cấp phát mảng trong C++ bằng `new[]` rồi bên C# giải phóng bằng `Marshal.FreeHGlobal` (gây hỏng bộ quản lý vùng nhớ heap).",
            "Bỏ qua quy ước đóng gói struct (`#pragma pack`), dẫn đến việc struct trên Windows 64-bit có kích thước 24 byte nhưng bên Python lại đọc thành 20 byte."
        ],
        "quality_gates": [
            "QG-01: Kích thước `sizeof` và độ dời `offsetof` của 100% các struct trùng khớp tuyệt đối giữa hai ngôn ngữ.",
            "QG-02: Vượt qua 10,000 lượt gọi hàm FFI liên tục mà không có hiện tượng rò rỉ bộ nhớ (kiểm tra bằng Valgrind / ASan).",
            "QG-03: Không có bất kỳ ngoại lệ C++ nào bị thoát ra ngoài ranh giới `extern \"C\"` (phải bao bọc bằng `try-catch`)."
        ],
        "security": "Kiểm tra giới hạn con trỏ và độ dài mảng truyền vào hàm FFI để triệt tiêu lỗ hổng tràn bộ đệm (Buffer Overflow).",
        "deliverables": [
            "Tệp tiêu đề C ABI chuẩn hóa `native_plugin.h`.",
            "Bộ test tự động kiểm tra ranh giới FFI chạy bằng AddressSanitizer."
        ],
        "related": ["dex-ffi-boundary-contracts", "dex-cpp-memory-safety", "dex-rust-unsafe-audit"],
        "scenario": "Game Unity tích hợp thư viện mã hóa viết bằng C++ bị sập ngẫu nhiên khi phát hành trên Android và iOS. Kỹ sư kích hoạt `dex-native-plugin-abi-testing`, phát hiện struct tọa độ trong C# bị lệch 4 byte padding so với định nghĩa trong C++ do trình biên dịch Clang trên ARM64 căn chỉnh theo 8 byte. Thêm chỉ thị `#pragma pack(8)` đồng bộ, chấm dứt hoàn toàn hiện tượng crash game."
    },
    {
        "id": "dex-real-time-input-latency",
        "index": 279,
        "group": "Group AB",
        "domain": "Native, Graphics & Game Engineering",
        "description": "Diagnose and minimize end-to-end user input latency, raw input device polling, OS event pump queuing, render pipeline latency, and display scanout synchronization. Use when building competitive esports games, audio DAWs, or high-responsiveness stylus drawing apps.",
        "purpose": "Đo lường, chẩn đoán và giảm thiểu độ trễ thao tác đầu vào từ đầu đến cuối (End-to-End Input Latency / Motion-to-Photon); tối ưu hóa việc lấy mẫu thiết bị đầu vào thô (Raw Input Polling), bơm xử lý sự kiện hệ điều hành (OS Event Pump), độ trễ đường ống kết xuất và đồng bộ hóa quét hình hiển thị; phục vụ các tựa game thể thao điện tử thi đấu chuyên nghiệp, phần mềm âm thanh kỹ thuật số (DAW) và ứng dụng vẽ bút cảm ứng có độ nhạy tức thì.",
        "when_use": [
            "Khi người chơi game bắn súng phàn nàn việc di chuột có cảm giác bị nặng, trễ hoặc trôi (Input Lag).",
            "Khi xây dựng ứng dụng vẽ trên máy tính bảng và cần nét vẽ bám sát đầu bút stylus mà không bị thụt lùi lại phía sau.",
            "Khi cần đo lường chính xác tổng độ trễ từ lúc bấm phím vật lý đến lúc pixel trên màn hình đổi màu."
        ],
        "when_not_use": [
            "Khi ứng dụng là các website đọc tin tức hoặc biểu mẫu văn phòng thông thường.",
            "Khi độ trễ vài chục mili-giây không ảnh hưởng đến trải nghiệm người dùng."
        ],
        "prereqs": "Chuột/Bàn phím có tần số phản hồi cao (1000Hz+ Polling Rate), màn hình tần số quét cao, công cụ đo độ trễ phần cứng (NVIDIA Reflex Analyzer hoặc máy quay tốc độ cao).",
        "concepts": [
            "Windows Raw Input API: Bỏ qua hàng đợi thông điệp cửa sổ thông thường (`WM_MOUSEMOVE`), đọc trực tiếp dữ liệu thô từ cổng USB để giảm thiểu độ trễ của hệ điều hành.",
            "Render Queue Latency: Hàng đợi khung hình render của GPU là thủ phạm lớn nhất gây trễ chuột; giải pháp là kích hoạt công nghệ NVIDIA Reflex hoặc AMD Anti-Lag để GPU chỉ bắt đầu dựng hình ngay khi nhận được input mới nhất.",
            "Predictive Input Modeling: Dự đoán tọa độ tiếp theo của đầu bút vẽ dựa trên vận tốc và gia tốc tức thời để vẽ trước vài mili-giây, tạo cảm giác mực chảy tức thì."
        ],
        "steps": [
            "Đăng ký thiết bị đầu vào thô bằng hàm `RegisterRawInputDevices` trên Windows.",
            "Lấy mẫu sự kiện chuột/phím ở tần số cao độc lập với tốc độ khung hình của game.",
            "Kích hoạt công nghệ NVIDIA Reflex Low Latency Mode trong động cơ kết xuất đồ họa.",
            "Đo lường tổng độ trễ hệ thống (System Latency) bằng bộ phân tích Reflex Analyzer.",
            "Kiểm tra và xác nhận độ trễ thao tác chuột giảm xuống dưới ngưỡng 15ms."
        ],
        "code_lang": "cpp",
        "code_example": """// Registering High-Precision Windows Raw Input for Mouse
#include <windows.h>

void registerRawMouseInput(HWND hwnd) {
    RAWINPUTDEVICE rid[1];
    rid[0].usUsagePage = 0x01; // Generic Desktop Controls
    rid[0].usUsage = 0x02;     // Mouse
    rid[0].dwFlags = RIDEV_INPUTSINK;
    rid[0].hwndTarget = hwnd;

    if (!RegisterRawInputDevices(rid, 1, sizeof(rid[0]))) {
        // Handle error
    }
}""",
        "antipatterns": [
            "Dùng tọa độ chuột lấy từ sự kiện cửa sổ thông thường kết hợp với cơ chế làm mượt chuột nội suy quá đà (Mouse Smoothing), gây cảm giác trễ và mất cảm giác rê chuột chân thực.",
            "Bật chế độ khử răng cưa toàn màn hình hoặc lọc đa mẫu quá nặng khiến GPU bị quá tải và đẩy độ trễ hàng đợi lên trên 60ms.",
            "Bỏ qua việc tắt cờ tăng tốc chuột của Windows (Mouse Acceleration / Enhance pointer precision)."
        ],
        "quality_gates": [
            "QG-01: Độ trễ thao tác chuột tổng thể từ lúc bấm đến lúc hiển thị giảm xuống dưới 18ms ở tốc độ 144Hz.",
            "QG-02: 100% dữ liệu chuột được nạp qua Raw Input API với tần số lấy mẫu 1000Hz đầy đủ.",
            "QG-03: Tích hợp thành công SDK giảm độ trễ NVIDIA Reflex hoặc AMD Anti-Lag."
        ],
        "security": "Chặn các phần mềm can thiệp gửi sự kiện chuột giả lập (Mouse injection scripts / Aimbot) bằng cách xác thực nguồn gốc phần cứng của Raw Input.",
        "deliverables": [
            "Module thu nhận đầu vào độ trễ cực thấp `RawInputManager.cpp`.",
            "Báo cáo đối chuẩn độ trễ thao tác hệ thống `INPUT_LATENCY_REPORT.md`."
        ],
        "related": ["dex-rendering-frame-pacing", "dex-game-loop-timing", "dex-performance-optimization"],
        "scenario": "Tựa game bắn súng FPS trực tuyến bị các game thủ thi đấu chê vì cảm giác bắn súng không nhạy bằng đối thủ cạnh tranh. Kỹ sư kích hoạt `dex-real-time-input-latency`, chuyển đổi sang Windows Raw Input và tích hợp NVIDIA Reflex Low Latency SDK, đưa tổng độ trễ từ 42ms xuống chỉ còn 14ms, nhận được sự khen ngợi nhiệt liệt từ cộng đồng thể thao điện tử."
    },
    {
        "id": "dex-asset-pipeline-optimization",
        "index": 280,
        "group": "Group AB",
        "domain": "Native, Graphics & Game Engineering",
        "description": "Architect modern game and graphics asset compilation pipelines with GPU texture compression (BC1-7, ASTC, KTX2/Basis Universal), mesh level-of-detail (LOD) simplification, and streaming bundles. Use when reducing game package sizes, eliminating runtime stalls, and optimizing VRAM footprints.",
        "purpose": "Thiết kế và xây dựng đường ống biên dịch và đóng gói tài nguyên đồ họa (Asset Pipeline Optimization) hiện đại; nén ảnh texture trực tiếp sang định dạng nén phần cứng GPU (BC1-BC7 trên PC, ASTC trên Mobile, KTX2/Basis Universal trên Web), tự động tạo các cấp độ chi tiết lưới đa giác (Mesh Level-of-Detail - LOD) và phân phối theo gói luồng (Streaming Bundles); phục vụ giảm 70% dung lượng gói cài đặt và giảm tải bộ nhớ VRAM.",
        "when_use": [
            "Khi dung lượng gói cài đặt game quá khổng lồ (vượt quá 50GB) và cần tối ưu hóa để người dùng tải nhanh.",
            "Khi game bị giật khựng mỗi khi chuyển vùng bản đồ do phải giải nén ảnh PNG/JPEG thô vào VRAM.",
            "Khi cần xuất bản trò chơi đa nền tảng từ máy tính để bàn cấu hình cao xuống điện thoại di động và WebGL."
        ],
        "when_not_use": [
            "Khi ứng dụng chỉ chứa một vài hình ảnh vector SVG đơn giản.",
            "Khi làm việc với các tệp văn bản mã nguồn."
        ],
        "prereqs": "Công cụ nén texture phần cứng (`basis_universal`, `astcenc`, `nvtt`), công cụ đơn giản hóa lưới đa giác (`meshoptimizer`), kịch bản tự động hóa đường ống tài nguyên.",
        "concepts": [
            "Block Compression (BC / ASTC): Định dạng nén ảnh mà GPU có thể đọc và giải nén trực tiếp trên chip nhớ VRAM mà không cần giải nén bung ra RAM, giúp tiết kiệm 75% bộ nhớ đồ họa.",
            "Basis Universal / KTX2: Định dạng texture trung gian siêu nhỏ gọn có thể tự động chuyển đổi (Transcode) sang định dạng phần cứng tốt nhất của thiết bị đích lúc chạy.",
            "Mesh LOD Simplification: Giảm số lượng đỉnh tam giác của các vật thể ở xa mà mắt người không nhận biết được, giúp giảm tải hàng triệu phép tính Vertex Shader."
        ],
        "steps": [
            "Quét toàn bộ thư mục tài nguyên hình ảnh gốc (PNG, TGA, TIFF) của dự án.",
            "Chuyển đổi các texture sang định dạng KTX2 sử dụng nén UASTC hoặc ETC1S.",
            "Tự động sinh chuỗi Mipmaps đầy đủ cho từng texture để chống răng cưa khi nhìn từ xa.",
            "Chạy công cụ `meshoptimizer` để tạo 3 cấp độ chi tiết LOD cho toàn bộ các mô hình 3D (LOD0: 100%, LOD1: 50%, LOD2: 15%).",
            "Đóng gói tài nguyên thành các tệp gói dữ liệu nén (Asset Bundles) có hỗ trợ tải luồng theo nhu cầu."
        ],
        "code_lang": "bash",
        "code_example": """# Compressing textures to KTX2 / Basis Universal
basisu -ktx2 -uastc -uastc_level 2 -mipmap input_texture.png -output_file albedo.ktx2

# Optimizing 3D mesh and generating LOD levels via gltfpack
gltfpack -i character_model.gltf -o character_optimized.glb -cc -tc -si 0.5

# Verifying VRAM savings
# Raw uncompressed 2048x2048 RGBA: 16 MB VRAM
# BC7 / ASTC 4x4 compressed: 4 MB VRAM (75% savings!)""",
        "antipatterns": [
            "Đóng gói ảnh PNG thô vào game rồi lúc chạy dùng hàm giải nén của CPU ra mảng byte khổng lồ để nạp vào GPU (làm đứng hình game và ngốn sạch VRAM).",
            "Quên tạo Mipmaps cho texture khiến các bề mặt ở xa bị lấp lánh chói mắt (Texture Shimmering) và lãng phí băng thông bộ nhớ.",
            "Hiển thị mô hình 100,000 tam giác cho một cái cây nằm ở đường chân trời cách xa nhân vật 1km."
        ],
        "quality_gates": [
            "QG-01: 100% texture trong bản dựng phát hành sử dụng định dạng nén GPU chuẩn (BC/ASTC/KTX2).",
            "QG-02: Dung lượng cài đặt gói tài nguyên giảm tối thiểu 60% so với dữ liệu gốc ban đầu.",
            "QG-03: Mọi mô hình phức tạp hơn 5,000 tam giác đều có tối thiểu 2 cấp độ LOD tự động."
        ],
        "security": "Xác minh mã băm toàn vẹn (Integrity Checksums) của các gói tài nguyên tải về từ mạng để ngăn ngừa việc người chơi chỉnh sửa tệp game để gian lận (Asset Modding).",
        "deliverables": [
            "Đường ống tự động hóa biên dịch tài nguyên `compile_assets_pipeline.py`.",
            "Báo cáo tối ưu hóa dung lượng gói và mức sử dụng VRAM `ASSET_OPTIMIZATION_REPORT.md`."
        ],
        "related": ["dex-gpu-resource-lifetime", "dex-media-delivery-pipelines", "dex-webgpu-rendering-fundamentals"],
        "scenario": "Một game thế giới mở trên di động có dung lượng gói cài đặt lên tới 14GB khiến 60% người dùng bỏ cuộc khi tải. Kỹ sư kích hoạt `dex-asset-pipeline-optimization`, chuyển đổi toàn bộ thư viện ảnh sang KTX2 Basis Universal và tạo LOD cho cây cối, giảm dung lượng cài đặt xuống chỉ còn 3.8GB và giảm 65% mức sử dụng VRAM, giúp game chạy mượt trên cả các điện thoại Android giá rẻ."
    }
]

def build_markdown(meta):
    md = f"""---
name: {meta['id']}
description: {meta['description']}
---

# {meta['id']}

## 1. Purpose & Scope
{meta['purpose']}

## 2. When to Use
"""
    for item in meta['when_use']:
        md += f"- {item}\n"

    md += "\n## 3. When NOT to Use\n"
    for item in meta['when_not_use']:
        md += f"- {item}\n"

    md += f"""
## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** {meta['prereqs']}
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; bảo vệ toàn vẹn tài sản kỹ nghệ và dữ liệu sản xuất.

## 5. Core Concepts & Taxonomy
"""
    for item in meta['concepts']:
        md += f"- **{item.split(':', 1)[0]}:**{item.split(':', 1)[1] if ':' in item else ''}\n"

    md += "\n## 6. Step-by-Step Execution Workflow\n"
    for i, step in enumerate(meta['steps'], 1):
        md += f"{i}. {step}\n"

    md += f"""
## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```{meta['code_lang']}
{meta['code_example']}
```

## 8. Anti-Patterns & Common Traps
"""
    for item in meta['antipatterns']:
        md += f"- {item}\n"

    md += "\n## 9. Quality Gates & Acceptance Criteria\n"
    for item in meta['quality_gates']:
        md += f"- {item}\n"

    md += f"""
## 10. Security & Safety Boundaries
- {meta['security']}
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
"""
    for item in meta['deliverables']:
        md += f"1. {item}\n"

    md += "\n## 13. Related & Complementary Skills\n"
    for r in meta['related']:
        md += f"- [`{r}`](.agents/skills/{r}/SKILL.md)\n"

    md += f"""
## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
{meta['scenario']}
"""
    return md

def generate_skills():
    if sys.stdout.encoding != "utf-8" and hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    for s in GROUP_AA_AB_SKILLS:
        skill_dir = os.path.join(SKILLS_DIR, s["id"])
        os.makedirs(skill_dir, exist_ok=True)
        skill_file = os.path.join(skill_dir, "SKILL.md")
        content = build_markdown(s)
        with open(skill_file, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[OK] Generated {s['id']} (Skill {s['index']:03d})")

if __name__ == "__main__":
    generate_skills()
