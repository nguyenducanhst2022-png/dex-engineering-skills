---
name: dex-online-offline-feature-parity
description: Detect, audit, and eliminate skew between offline training features and real-time online inference features using unified feature store definitions and dual-write testing. Use when deploying machine learning models into latency-critical production environments.
---

# dex-online-offline-feature-parity

## 1. Purpose & Scope
Phát hiện, kiểm toán và triệt tiêu độ lệch (training-serving skew) giữa các đặc trưng (features) huấn luyện ngoại tuyến (offline) và đặc trưng suy luận thời gian thực (online) thông qua định nghĩa kho đặc trưng thống nhất (Feature Store) và kiểm thử ghi kép (dual-write).

## 2. When to Use
- Khi mô hình Machine Learning đạt độ chính xác rất cao khi kiểm thử offline nhưng sụt giảm hiệu năng nghiêm trọng khi đưa vào phục vụ online.
- Khi các pipeline tính toán feature chạy bằng SQL/Spark ngoại tuyến nhưng khi online lại được viết lại bằng Python/Go dẫn tới sai lệch logic.
- Khi triển khai hệ thống Feature Store (Feast, Hopsworks, Tecton) để quản lý vòng đời đặc trưng tập trung.

## 3. When NOT to Use
- Khi mô hình suy luận hoàn toàn theo lô (Batch Inference) trên cùng một bảng dữ liệu huấn luyện mà không có yêu cầu tính toán real-time.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Định nghĩa Feature View, kho lưu trữ dữ liệu offline (Data Warehouse/Lake), kho lưu trữ online (Redis, DynamoDB).
- **Quyền hạn truy cập:** Quyền đọc/ghi Feature Store và quyền truy xuất nhật ký suy luận mô hình.

## 5. Core Concepts & Taxonomy
- **Training-Serving Skew:** Sự khác biệt về mặt phân phối hoặc giá trị của đặc trưng giữa thời điểm huấn luyện và thời điểm suy luận thực tế.
- **Point-in-Time Correctness:** Khả năng truy xuất chính xác giá trị của đặc trưng tại thời điểm sự kiện xảy ra trong quá khứ mà không bị rò rỉ dữ liệu tương lai.
- **Dual-Write Verification:** Ghi đồng thời đặc trưng tính toán từ cả hai pipeline (online và offline) vào môi trường kiểm thử để so sánh sai khác thống kê.

## 6. Step-by-Step Execution Workflow
1. Khảo sát mã nguồn tính toán đặc trưng ở cả hai môi trường: batch pipeline (Spark/SQL) và streaming/real-time service.
2. Hợp nhất định nghĩa logic tính toán vào một nguồn duy nhất (Single Definition) bằng Feast hoặc dbt.
3. Thiết lập kiểm thử tự động so sánh phân phối giá trị đặc trưng giữa hai kho dữ liệu bằng kiểm định Kolmogorov-Smirnov (KS-test).
4. Triển khai cơ chế time-travel queries để bảo đảm tính đúng đắn thời điểm (Point-in-Time Correctness).
5. Giám sát độ lệch phân phối (Drift Detection) bằng các chỉ số PSI (Population Stability Index) trong thời gian thực.
6. Tự động phát cảnh báo khi chỉ số PSI vượt ngưỡng quy định (> 0.2).

## 7. Concrete Examples
### Kiểm tra độ lệch đặc trưng bằng Kolmogorov-Smirnov Test trong Python:
```python
from scipy.stats import ks_2samp
import numpy as np

def check_feature_parity(offline_features: np.ndarray, online_features: np.ndarray, feature_name: str, p_threshold=0.05):
    statistic, p_value = ks_2samp(offline_features, online_features)
    print(f"Feature: {feature_name} | KS-Statistic: {statistic:.4f} | p-value: {p_value:.4f}")
    
    if p_value < p_threshold:
        raise ValueError(
            f"Canh bao: Phat hien Training-Serving Skew tren feature '{feature_name}'! "
            f"(p-value={p_value} < {p_threshold})"
        )
    return True
```

## 8. Anti-Patterns & Common Traps
- **Re-implementing Logic in Two Languages:** Viết logic trích xuất đặc trưng bằng PySpark khi train và viết lại bằng Go/C++ khi deploy online mà không có bộ test chung.
- **Future Data Leakage:** Dùng các hàm tổng hợp toàn cục (như trung bình tháng) bao trùm cả dữ liệu tương lai khi sinh tập training.
- **Unmonitored Feature Decay:** Không giám sát dữ liệu online dẫn tới việc các đặc trưng dần bị trôi dạt (drift) theo thời gian.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: 100% đặc trưng trong Feature Store có định nghĩa logic thống nhất giữa online và offline.
- **QG-04**: Giá trị kiểm định KS-test đạt p-value >= 0.05 trên tập dữ liệu kiểm chứng độc lập.
- **QG-08**: Độ trễ đồng bộ từ offline sang online cache không vượt quá giới hạn SLA (ví dụ: < 15 phút).

## 10. Security & Safety Boundaries
- Kiểm tra chính sách kiểm soát truy cập (RBAC) trên các kho đặc trưng để bảo vệ các đặc trưng nhạy cảm (PII, tài chính).

## 11. Platform Adapters
- **Feature Stores**: Feast, Hopsworks, Tecton, AWS Feature Store.
- **Monitoring**: Evidently AI, Whylogs, Great Expectations.

## 12. Deliverables & Output Artifacts
- File cấu hình Feast Feature View thống nhất.
- Bộ kiểm thử đối soát training-serving skew tự động.
- Dashboard giám sát chỉ số PSI và phân phối đặc trưng.

## 13. Related & Complementary Skills
dex-training-data-leakage-audit, dex-ml-experiment-reproducibility, dex-model-serving-canary-rollouts

## 14. Realistic Usage Example
```powershell
# Chạy đồng bộ hóa đặc trưng từ offline sang online bằng Feast
feast apply
feast materialize-incremental $(Get-Date -Format "yyyy-MM-ddTHH:mm:ss")

# Chạy test kiểm toán tính tương đương đặc trưng
pytest tests/ml/test_feature_parity.py -v
```
