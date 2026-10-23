---
name: dex-training-data-leakage-audit
description: Detect and eliminate target leakage, future data leakage, cross-split sample contamination, and group-level data leakage across machine learning training datasets. Use when validating predictive validity and real-world generalizability.
---

# dex-training-data-leakage-audit

## 1. Purpose & Scope
Phát hiện, kiểm toán và triệt tiêu các dạng rò rỉ dữ liệu huấn luyện (Data Leakage) bao gồm rò rỉ nhãn mục tiêu (Target Leakage), rò rỉ dữ liệu tương lai (Future Leakage), nhiễm chéo tập dữ liệu (Cross-Split Contamination) và rò rỉ cấp nhóm (Group-Level Leakage).

## 2. When to Use
- Khi mô hình huấn luyện đạt kết quả độ chính xác cao bất thường (ví dụ: AUC = 0.999) nhưng thất bại khi thử nghiệm thực tế.
- Khi dữ liệu có yếu tố chuỗi thời gian (Time-Series) nhưng lại bị phân chia ngẫu nhiên (Random Train-Test Split).
- Khi chuẩn bị phát hành các mô hình chấm điểm tín dụng, chẩn đoán y tế hoặc phát hiện gian lận.

## 3. When NOT to Use
- Khi tiến hành học không giám sát (Unsupervised Learning) hoặc phân cụm dữ liệu không có nhãn mục tiêu.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Pipeline xử lý tiền dữ liệu, tập dữ liệu huấn luyện và kiểm thử, nhãn mục tiêu (Target Variable).
- **Quyền hạn truy cập:** Quyền phân tích cấu trúc pipeline xử lý dữ liệu và mã nguồn huấn luyện.

## 5. Core Concepts & Taxonomy
- **Target Leakage:** Sử dụng các biến đầu vào mà giá trị của nó chỉ xuất hiện SAU KHI sự kiện mục tiêu xảy ra (ví dụ: sử dụng mã hóa đơn hoàn tiền để dự đoán hủy đơn).
- **Temporal Split vs. Random Split:** Với dữ liệu chuỗi thời gian, tập test phải nằm ở tương lai so với tập train, không được dùng phép shuffle ngẫu nhiên.
- **Group Contamination:** Các bản ghi từ cùng một bệnh nhân hoặc một thiết bị xuất hiện đồng thời ở cả tập train và test.

## 6. Step-by-Step Execution Workflow
1. Rà soát ma trận tương quan giữa tất cả các đặc trưng đầu vào và nhãn mục tiêu; gắn cờ các đặc trưng có hệ số tương quan cao bất thường (> 0.95).
2. Kiểm tra quy trình tiền xử lý (Scaling, Imputation, Encoding): bảo đảm các giá trị thống kê (mean, std) chỉ được tính toán trên tập train.
3. Kiểm tra cơ chế phân chia dữ liệu: chuyển đổi từ Random Split sang Time-based Split hoặc GroupKFold nếu có thuộc tính nhóm.
4. Thực hiện kiểm thử Feature Ablation (loại trừ từng đặc trưng) để đo lường mức độ phụ thuộc đáng ngờ của mô hình.
5. Kiểm tra thời gian sinh của từng đặc trưng đối chiếu với thời điểm đưa ra quyết định dự đoán.
6. Xuất báo cáo kiểm toán rò rỉ dữ liệu kèm các khuyến nghị cấu trúc lại pipeline.

## 7. Concrete Examples
### Kiểm tra rò rỉ tiền xử lý và phân chia theo nhóm bằng Scikit-Learn Pipeline:
```python
from sklearn.model_selection import GroupKFold
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

# Pipeline chuẩn: StandardScaler chỉ fit trên fold huấn luyện, chống rò rỉ thống kê
pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('model', RandomForestClassifier(random_state=42))
])

# GroupKFold bảo đảm các bản ghi của cùng 1 user_id không xuất hiện ở cả train và test
group_kfold = GroupKFold(n_splits=5)
for train_idx, test_idx in group_kfold.split(X, y, groups=user_ids):
    X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
    y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]
    
    # Fit pipeline
    pipeline.fit(X_train, y_train)
    score = pipeline.score(X_test, y_test)
    print(f"Fold Accuracy (Chong ro ri nhom): {score:.4f}")
```

## 8. Anti-Patterns & Common Traps
- **Global Imputation Before Splitting:** Điền giá trị khuyết thiếu (mean/median) trên toàn bộ bảng dữ liệu TRƯỚC KHI chia tập train/test.
- **Random Shuffling Time Series:** Trộn ngẫu nhiên dữ liệu giao dịch tài chính khiến mô hình dùng thông tin ngày mai để đoán hôm nay.
- **Proxy Target Features:** Giữ lại các đặc trưng đại diện gián tiếp cho nhãn (như trạng thái tài khoản đóng sau khi gian lận).

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Không có bất kỳ phép biến đổi dữ liệu nào (fit transformer) được thực thi trên tập kiểm thử.
- **QG-04**: Dữ liệu có thuộc tính thời gian bắt buộc sử dụng chiến lược Temporal Split.
- **QG-08**: 0% trùng lặp mã định danh thực thể (ID) giữa tập train và test khi áp dụng Group Split.

## 10. Security & Safety Boundaries
- Bảo đảm không để lộ nhãn nhạy cảm hoặc thuộc tính PII trong các đặc trưng trung gian.

## 11. Platform Adapters
- **Frameworks**: Scikit-Learn Pipelines, Great Expectations, Cleanlab, PySpark ML.

## 12. Deliverables & Output Artifacts
- Script kiểm toán tương quan và thời gian sinh đặc trưng.
- Pipeline huấn luyện đã được tái cấu trúc chống rò rỉ.
- Báo cáo đánh giá hiệu năng thực tế sau khi loại bỏ rò rỉ.

## 13. Related & Complementary Skills
dex-online-offline-feature-parity, dex-ml-experiment-reproducibility, dex-data-label-quality-assessment

## 14. Realistic Usage Example
```powershell
# Chạy suite kiểm toán rò rỉ dữ liệu tự động
pytest tests/ml/test_data_leakage.py -v

# Quét tương quan đặc trưng bằng script kiểm toán
python scripts/ml/audit_feature_correlation.py --threshold 0.90
```
