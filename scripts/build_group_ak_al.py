# -*- coding: utf-8 -*-
"""
DEX ENGINEERING SKILLS FRAMEWORK v8.0 — GENERATOR
Builds Group AK (Skills 361–370: ML Platform & Data Systems)
and Group AL (Skills 371–380: Developer Platform & Polyglot Tooling).
All skills strictly implement the 14 mandatory sections standard.
"""

import os
import sys

if sys.stdout.encoding != "utf-8" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SKILLS_DIR = os.path.join(ROOT, ".agents", "skills")

SKILLS_AK_AL = [
    # =========================================================================
    # GROUP AK: ML Platform & Data Systems (Skills 361–370)
    # =========================================================================
    {
        "id": "dex-online-offline-feature-parity",
        "name": "dex-online-offline-feature-parity",
        "desc": "Detect, audit, and eliminate skew between offline training features and real-time online inference features using unified feature store definitions and dual-write testing. Use when deploying machine learning models into latency-critical production environments.",
        "purpose": "Phát hiện, kiểm toán và triệt tiêu độ lệch (training-serving skew) giữa các đặc trưng (features) huấn luyện ngoại tuyến (offline) và đặc trưng suy luận thời gian thực (online) thông qua định nghĩa kho đặc trưng thống nhất (Feature Store) và kiểm thử ghi kép (dual-write).",
        "when_use": "- Khi mô hình Machine Learning đạt độ chính xác rất cao khi kiểm thử offline nhưng sụt giảm hiệu năng nghiêm trọng khi đưa vào phục vụ online.\n- Khi các pipeline tính toán feature chạy bằng SQL/Spark ngoại tuyến nhưng khi online lại được viết lại bằng Python/Go dẫn tới sai lệch logic.\n- Khi triển khai hệ thống Feature Store (Feast, Hopsworks, Tecton) để quản lý vòng đời đặc trưng tập trung.",
        "when_not_use": "- Khi mô hình suy luận hoàn toàn theo lô (Batch Inference) trên cùng một bảng dữ liệu huấn luyện mà không có yêu cầu tính toán real-time.",
        "prereqs": "- **Ngữ cảnh đầu vào:** Định nghĩa Feature View, kho lưu trữ dữ liệu offline (Data Warehouse/Lake), kho lưu trữ online (Redis, DynamoDB).\n- **Quyền hạn truy cập:** Quyền đọc/ghi Feature Store và quyền truy xuất nhật ký suy luận mô hình.",
        "concepts": "- **Training-Serving Skew:** Sự khác biệt về mặt phân phối hoặc giá trị của đặc trưng giữa thời điểm huấn luyện và thời điểm suy luận thực tế.\n- **Point-in-Time Correctness:** Khả năng truy xuất chính xác giá trị của đặc trưng tại thời điểm sự kiện xảy ra trong quá khứ mà không bị rò rỉ dữ liệu tương lai.\n- **Dual-Write Verification:** Ghi đồng thời đặc trưng tính toán từ cả hai pipeline (online và offline) vào môi trường kiểm thử để so sánh sai khác thống kê.",
        "workflow": "1. Khảo sát mã nguồn tính toán đặc trưng ở cả hai môi trường: batch pipeline (Spark/SQL) và streaming/real-time service.\n2. Hợp nhất định nghĩa logic tính toán vào một nguồn duy nhất (Single Definition) bằng Feast hoặc dbt.\n3. Thiết lập kiểm thử tự động so sánh phân phối giá trị đặc trưng giữa hai kho dữ liệu bằng kiểm định Kolmogorov-Smirnov (KS-test).\n4. Triển khai cơ chế time-travel queries để bảo đảm tính đúng đắn thời điểm (Point-in-Time Correctness).\n5. Giám sát độ lệch phân phối (Drift Detection) bằng các chỉ số PSI (Population Stability Index) trong thời gian thực.\n6. Tự động phát cảnh báo khi chỉ số PSI vượt ngưỡng quy định (> 0.2).",
        "examples": """### Kiểm tra độ lệch đặc trưng bằng Kolmogorov-Smirnov Test trong Python:
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
```""",
        "antipatterns": "- **Re-implementing Logic in Two Languages:** Viết logic trích xuất đặc trưng bằng PySpark khi train và viết lại bằng Go/C++ khi deploy online mà không có bộ test chung.\n- **Future Data Leakage:** Dùng các hàm tổng hợp toàn cục (như trung bình tháng) bao trùm cả dữ liệu tương lai khi sinh tập training.\n- **Unmonitored Feature Decay:** Không giám sát dữ liệu online dẫn tới việc các đặc trưng dần bị trôi dạt (drift) theo thời gian.",
        "gates": "- **QG-01**: 100% đặc trưng trong Feature Store có định nghĩa logic thống nhất giữa online và offline.\n- **QG-04**: Giá trị kiểm định KS-test đạt p-value >= 0.05 trên tập dữ liệu kiểm chứng độc lập.\n- **QG-08**: Độ trễ đồng bộ từ offline sang online cache không vượt quá giới hạn SLA (ví dụ: < 15 phút).",
        "security": "- Kiểm tra chính sách kiểm soát truy cập (RBAC) trên các kho đặc trưng để bảo vệ các đặc trưng nhạy cảm (PII, tài chính).",
        "adapters": "- **Feature Stores**: Feast, Hopsworks, Tecton, AWS Feature Store.\n- **Monitoring**: Evidently AI, Whylogs, Great Expectations.",
        "deliverables": "- File cấu hình Feast Feature View thống nhất.\n- Bộ kiểm thử đối soát training-serving skew tự động.\n- Dashboard giám sát chỉ số PSI và phân phối đặc trưng.",
        "related": "dex-training-data-leakage-audit, dex-ml-experiment-reproducibility, dex-model-serving-canary-rollouts",
        "usage": """```powershell
# Chạy đồng bộ hóa đặc trưng từ offline sang online bằng Feast
feast apply
feast materialize-incremental $(Get-Date -Format "yyyy-MM-ddTHH:mm:ss")

# Chạy test kiểm toán tính tương đương đặc trưng
pytest tests/ml/test_feature_parity.py -v
```"""
    },
    {
        "id": "dex-training-data-leakage-audit",
        "name": "dex-training-data-leakage-audit",
        "desc": "Detect and eliminate target leakage, future data leakage, cross-split sample contamination, and group-level data leakage across machine learning training datasets. Use when validating predictive validity and real-world generalizability.",
        "purpose": "Phát hiện, kiểm toán và triệt tiêu các dạng rò rỉ dữ liệu huấn luyện (Data Leakage) bao gồm rò rỉ nhãn mục tiêu (Target Leakage), rò rỉ dữ liệu tương lai (Future Leakage), nhiễm chéo tập dữ liệu (Cross-Split Contamination) và rò rỉ cấp nhóm (Group-Level Leakage).",
        "when_use": "- Khi mô hình huấn luyện đạt kết quả độ chính xác cao bất thường (ví dụ: AUC = 0.999) nhưng thất bại khi thử nghiệm thực tế.\n- Khi dữ liệu có yếu tố chuỗi thời gian (Time-Series) nhưng lại bị phân chia ngẫu nhiên (Random Train-Test Split).\n- Khi chuẩn bị phát hành các mô hình chấm điểm tín dụng, chẩn đoán y tế hoặc phát hiện gian lận.",
        "when_not_use": "- Khi tiến hành học không giám sát (Unsupervised Learning) hoặc phân cụm dữ liệu không có nhãn mục tiêu.",
        "prereqs": "- **Ngữ cảnh đầu vào:** Pipeline xử lý tiền dữ liệu, tập dữ liệu huấn luyện và kiểm thử, nhãn mục tiêu (Target Variable).\n- **Quyền hạn truy cập:** Quyền phân tích cấu trúc pipeline xử lý dữ liệu và mã nguồn huấn luyện.",
        "concepts": "- **Target Leakage:** Sử dụng các biến đầu vào mà giá trị của nó chỉ xuất hiện SAU KHI sự kiện mục tiêu xảy ra (ví dụ: sử dụng mã hóa đơn hoàn tiền để dự đoán hủy đơn).\n- **Temporal Split vs. Random Split:** Với dữ liệu chuỗi thời gian, tập test phải nằm ở tương lai so với tập train, không được dùng phép shuffle ngẫu nhiên.\n- **Group Contamination:** Các bản ghi từ cùng một bệnh nhân hoặc một thiết bị xuất hiện đồng thời ở cả tập train và test.",
        "workflow": "1. Rà soát ma trận tương quan giữa tất cả các đặc trưng đầu vào và nhãn mục tiêu; gắn cờ các đặc trưng có hệ số tương quan cao bất thường (> 0.95).\n2. Kiểm tra quy trình tiền xử lý (Scaling, Imputation, Encoding): bảo đảm các giá trị thống kê (mean, std) chỉ được tính toán trên tập train.\n3. Kiểm tra cơ chế phân chia dữ liệu: chuyển đổi từ Random Split sang Time-based Split hoặc GroupKFold nếu có thuộc tính nhóm.\n4. Thực hiện kiểm thử Feature Ablation (loại trừ từng đặc trưng) để đo lường mức độ phụ thuộc đáng ngờ của mô hình.\n5. Kiểm tra thời gian sinh của từng đặc trưng đối chiếu với thời điểm đưa ra quyết định dự đoán.\n6. Xuất báo cáo kiểm toán rò rỉ dữ liệu kèm các khuyến nghị cấu trúc lại pipeline.",
        "examples": """### Kiểm tra rò rỉ tiền xử lý và phân chia theo nhóm bằng Scikit-Learn Pipeline:
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
```""",
        "antipatterns": "- **Global Imputation Before Splitting:** Điền giá trị khuyết thiếu (mean/median) trên toàn bộ bảng dữ liệu TRƯỚC KHI chia tập train/test.\n- **Random Shuffling Time Series:** Trộn ngẫu nhiên dữ liệu giao dịch tài chính khiến mô hình dùng thông tin ngày mai để đoán hôm nay.\n- **Proxy Target Features:** Giữ lại các đặc trưng đại diện gián tiếp cho nhãn (như trạng thái tài khoản đóng sau khi gian lận).",
        "gates": "- **QG-01**: Không có bất kỳ phép biến đổi dữ liệu nào (fit transformer) được thực thi trên tập kiểm thử.\n- **QG-04**: Dữ liệu có thuộc tính thời gian bắt buộc sử dụng chiến lược Temporal Split.\n- **QG-08**: 0% trùng lặp mã định danh thực thể (ID) giữa tập train và test khi áp dụng Group Split.",
        "security": "- Bảo đảm không để lộ nhãn nhạy cảm hoặc thuộc tính PII trong các đặc trưng trung gian.",
        "adapters": "- **Frameworks**: Scikit-Learn Pipelines, Great Expectations, Cleanlab, PySpark ML.",
        "deliverables": "- Script kiểm toán tương quan và thời gian sinh đặc trưng.\n- Pipeline huấn luyện đã được tái cấu trúc chống rò rỉ.\n- Báo cáo đánh giá hiệu năng thực tế sau khi loại bỏ rò rỉ.",
        "related": "dex-online-offline-feature-parity, dex-ml-experiment-reproducibility, dex-data-label-quality-assessment",
        "usage": """```powershell
# Chạy suite kiểm toán rò rỉ dữ liệu tự động
pytest tests/ml/test_data_leakage.py -v

# Quét tương quan đặc trưng bằng script kiểm toán
python scripts/ml/audit_feature_correlation.py --threshold 0.90
```"""
    },
    {
        "id": "dex-model-serving-canary-rollouts",
        "name": "dex-model-serving-canary-rollouts",
        "desc": "Implement progressive canary rollouts, shadow traffic mirroring, and automated latency/accuracy rollbacks for production ML model serving clusters. Use when updating inference models without service disruption.",
        "purpose": "Triển khai chiến lược phát hành chim hoàng oanh (Canary Rollout), nhân bản lưu lượng bóng (Shadow Traffic) và tự động khôi phục (Rollback) dựa trên độ trễ và độ chính xác suy luận cho các cụm phục vụ mô hình Machine Learning; bảo đảm không gián đoạn dịch vụ sản xuất.",
        "when_use": "- Khi nâng cấp phiên bản mô hình mới (v2) thay thế mô hình đang chạy (v1) trên môi trường live.\n- Khi cần đo lường độ trễ p99 và mức tiêu hao GPU thực tế của mô hình mới dưới tải người dùng thật.\n- Khi muốn xác minh hành vi suy luận của mô hình mới mà không gây ảnh hưởng trực tiếp đến trải nghiệm người dùng (Shadow Deployment).",
        "when_not_use": "- Khi triển khai mô hình nội bộ thử nghiệm (sandbox) không có lưu lượng truy cập thực tế.",
        "prereqs": "- **Ngữ cảnh đầu vào:** Cụm phục vụ mô hình (Triton Inference Server, vLLM, KServe, TorchServe), Ingress/Service Mesh (Istio, Envoy).\n- **Quyền hạn truy cập:** Quyền cấu hình định tuyến lưu lượng mạng và triển khai container mô hình.",
        "concepts": "- **Shadow Mirroring:** Sao chép 100% request thực tế gửi tới cả hai mô hình nhưng chỉ trả kết quả của mô hình hiện tại về cho client; kết quả của mô hình bóng được ghi log để phân tích.\n- **Progressive Traffic Shifting:** Chuyển dần lưu lượng theo tỷ lệ phần trăm (1% -> 5% -> 25% -> 100%) kèm theo các tiêu chí đo lường an toàn (Health Checks).\n- **Automated Anomaly Rollback:** Tự động cắt toàn bộ lưu lượng về phiên bản cũ nếu tỷ lệ lỗi HTTP 5xx > 1% hoặc độ trễ p99 vượt quá 200ms.",
        "workflow": "1. Khởi tạo phiên bản dịch vụ mô hình mới (Canary/Shadow Pods) trong cụm Kubernetes.\n2. Cấu hình Ingress/Service Mesh sao chép 100% lưu lượng live sang mô hình Shadow để đánh giá độ ổn định.\n3. Đối soát độ trễ p99, tỷ lệ lỗi và mức tiêu hao GPU của mô hình Shadow với mô hình chính thức.\n4. Mở dần lưu lượng thực tế sang Canary: bắt đầu từ 1%, tăng lên 5%, 25%, và 50% sau mỗi chu kỳ kiểm tra 15 phút.\n5. Giám sát liên tục các cảnh báo độ lệch phân phối kết quả dự đoán và chỉ số kinh doanh.\n6. Chuyển hoàn toàn 100% lưu lượng sang mô hình mới hoặc kích hoạt rollback tự động nếu phát hiện bất thường.",
        "examples": """### Cấu hình Shadow Traffic và Canary Routing bằng Istio VirtualService:
```yaml
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: ml-inference-routing
spec:
  hosts:
  - "inference.internal.domain"
  http:
  - match:
    - uri:
        prefix: /v1/predict
    # Nhân bản lưu lượng sang mô hình mới để kiểm tra an toàn
    mirror:
      host: ml-serving-canary.internal.domain
    mirrorPercentage:
      value: 100.0
    # Phục vụ người dùng thực tế bằng mô hình hiện tại ổn định
    route:
    - destination:
        host: ml-serving-stable.internal.domain
        weight: 95
    - destination:
        host: ml-serving-canary.internal.domain
        weight: 5
```""",
        "antipatterns": "- **Big Bang Model Swapping:** Chuyển đổi 100% lưu lượng truy cập sang mô hình mới ngay lập tức mà không qua kiểm tra shadow.\n- **Ignoring Cold Start Latency:** Đẩy ngay tải cao vào pod mô hình mới khi GPU cache chưa được khởi động đầy đủ gây sập cụm serving.\n- **Manual Rollback Reliance:** Phụ thuộc vào việc kỹ sư phải ngồi theo dõi màn hình để gõ lệnh rollback thủ công khi có sự cố.",
        "gates": "- **QG-01**: Tỷ lệ lỗi 5xx trên mô hình canary giữ ở mức < 0.1% trong suốt 60 phút theo dõi.\n- **QG-04**: Độ trễ suy luận p99 của mô hình mới không vượt quá 120% so với mô hình baseline.\n- **QG-07**: Quy trình rollback tự động hoàn tất trong vòng dưới 30 giây khi vượt ngưỡng cảnh báo.",
        "security": "- Đảm bảo dữ liệu request nhân bản trong luồng shadow được ẩn danh hóa và tuân thủ các quy định bảo mật dữ liệu sản xuất.",
        "adapters": "- **Inference Platforms**: KServe, Seldon Core, Triton, vLLM, TorchServe.\n- **Service Mesh**: Istio, Envoy, Linkerd.",
        "deliverables": "- Cấu hình khai báo Canary & Shadow Routing (Kubernetes / Istio).\n- Kịch bản tự động tăng tải và rollback theo dõi metric.\n- Báo cáo phân tích so sánh hiệu năng giữa hai phiên bản mô hình.",
        "related": "dex-online-offline-feature-parity, dex-batch-inference-pipeline-tuning, dex-inference-provider-rate-controls",
        "usage": """```powershell
# Triển khai canary VirtualService vào cụm Kubernetes
kubectl apply -f k8s/ml-canary-routing.yaml

# Theo dõi metric độ trễ và tỷ lệ lỗi thời gian thực bằng Prometheus CLI
curl -s "http://prometheus:9090/api/v1/query?query=histogram_quantile(0.99,sum(rate(inference_duration_bucket[5m]))by(le,version))"
```"""
    },
    {
        "id": "dex-ml-experiment-reproducibility",
        "name": "dex-ml-experiment-reproducibility",
        "desc": "Track, containerize, and audit ML experiments with deterministic seeds, data versioning (DVC), hardware profiles, and environment freezing. Use when institutionalizing reproducible machine learning research and engineering.",
        "purpose": "Theo dõi, container hóa và kiểm toán các thử nghiệm Machine Learning; bảo đảm khả năng tái lập kết quả thử nghiệm 100% nhờ cố định seed ngẫu nhiên, lập phiên bản dữ liệu (DVC/LakeFS), ghi nhận cấu hình phần cứng và đóng băng môi trường thư viện phụ thuộc.",
        "when_use": "- Khi một kỹ sư rời nhóm và không ai có thể tái hiện lại kết quả mô hình mà họ đã công bố trước đây.\n- Khi cần nộp tài liệu kiểm chứng kết quả mô hình cho các cơ quan quản lý (FDA, ngân hàng trung ương).\n- Khi chuẩn hóa quy trình MLOps nhằm loại bỏ tình trạng 'chạy được trên máy của tôi'.",
        "when_not_use": "- Khi thực hiện viết mã khám phá nhanh ban đầu (Jupyter Notebook scratchpad) chỉ để kiểm tra ý tưởng trong vài phút.",
        "prereqs": "- **Ngữ cảnh đầu vào:** Mã nguồn huấn luyện, dữ liệu huấn luyện, công cụ theo dõi thử nghiệm (MLflow, Weights & Biases, DVC).\n- **Quyền hạn truy cập:** Quyền ghi vào máy chủ lưu trữ artifact và remote storage dữ liệu (S3/GCS).",
        "concepts": "- **Deterministic Seeding:** Thiết lập hạt giống ngẫu nhiên cố định cho tất cả các thư viện: Python random, NumPy, PyTorch (CPU và CUDA determinism).\n- **Data Version Control (DVC):** Quản lý phiên bản các tập dữ liệu lớn bằng cách lưu mã băm siêu dữ liệu trong Git thay vì commit trực tiếp file nhị phân.\n- **Environment Freezing:** Khóa cứng phiên bản các package bằng lockfiles (Poetry, Conda lock) và Docker container image digest.",
        "workflow": "1. Cấu hình hàm thiết lập deterministic seed trên toàn bộ các runtime (Python, NumPy, PyTorch, TensorFlow).\n2. Kích hoạt cờ thực thi tất định trên GPU (`torch.use_deterministic_algorithms(True)`).\n3. Liên kết tập dữ liệu huấn luyện với mã băm Git commit thông qua DVC (`dvc.lock`).\n4. Ghi nhận toàn bộ siêu dữ liệu: Git SHA, phiên bản CUDA, driver GPU, hyper-parameters vào MLflow/W&B.\n5. Đóng gói môi trường thực thi vào Docker container có digest cố định.\n6. Thực hiện huấn luyện độc lập trên hai máy khác nhau để xác minh tính nhất quán của trọng số mô hình cuối cùng.",
        "examples": """### Hàm thiết lập môi trường hoàn toàn tất định trong PyTorch:
```python
import os
import random
import numpy as np
import torch

def make_deterministic(seed: int = 42):
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    
    # Ép buộc các thuật toán cuDNN chạy tất định
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    
    # Bật kiểm tra thuật toán tất định trên PyTorch
    torch.use_deterministic_algorithms(True)
    os.environ['CUBLAS_WORKSPACE_CONFIG'] = ':4096:8'
    print(f"He thong da duoc thiet lap che do tat dinh voi Seed: {seed}")
```""",
        "antipatterns": "- **Unseeded Data Shuffling:** Trộn ngẫu nhiên dữ liệu mà không truyền seed dẫn tới mỗi lần chạy sinh ra một tập train khác nhau.\n- **Unpinned Python Packages:** Khai báo phụ thuộc `torch>=2.0` khiến bản cập nhật thư viện sau này làm thay đổi kết quả tính toán số thực.\n- **Data Ingestion via Mutable URLs:** Tải dữ liệu từ một đường link web có thể bị thay đổi nội dung mà không kiểm tra mã băm SHA-256.",
        "gates": "- **QG-01**: Mã nguồn, siêu tham số và phiên bản dữ liệu được liên kết 1-1 với commit Git SHA.\n- **QG-04**: Hai lần huấn luyện với cùng seed sinh ra hàm mất mát (Loss) giống hệt nhau với sai số floating-point < 1e-6.\n- **QG-08**: Môi trường huấn luyện chạy thành công từ container Docker độc lập không cần cài đặt thêm bên ngoài.",
        "security": "- Kiểm tra không ghi lại các thông tin bí mật (API keys, credentials) vào nhật ký tham số của công cụ tracking thử nghiệm.",
        "adapters": "- **Experiment Tracking**: MLflow, Weights & Biases, ClearML, Neptune.ai.\n- **Data Versioning**: DVC, LakeFS, Pachyderm.",
        "deliverables": "- Script huấn luyện tất định có thể tái lập.\n- File `dvc.lock` và `poetry.lock` khóa cứng môi trường.\n- Báo cáo đối chiếu kết quả giữa các lần chạy độc lập.",
        "related": "dex-training-data-leakage-audit, dex-online-offline-feature-parity, dex-model-serving-canary-rollouts",
        "usage": """```powershell
# Đồng bộ hóa phiên bản dữ liệu chính xác bằng DVC
dvc pull

# Chạy thử nghiệm có theo dõi đầy đủ qua MLflow
python train.py --seed 42 --config configs/production.yaml
```"""
    },
    {
        "id": "dex-data-label-quality-assessment",
        "name": "dex-data-label-quality-assessment",
        "desc": "Audit, clean, and score dataset annotation quality using programmatic label error detection, inter-annotator agreement metrics, and confident learning algorithms. Use when elevating training data fidelity for supervised ML models.",
        "purpose": "Kiểm toán, làm sạch và chấm điểm chất lượng nhãn dữ liệu (Data Label Quality); sử dụng thuật toán Confident Learning, đo lường độ đồng thuận giữa các người dán nhãn (Inter-Annotator Agreement) và phát hiện nhãn nhiễu hoặc sai lệch trong tập dữ liệu giám sát.",
        "when_use": "- Khi tập dữ liệu được dán nhãn bởi nhiều chuyên gia hoặc bên thứ ba dẫn tới tiêu chuẩn không đồng nhất.\n- Khi mô hình gặp khó khăn trong việc hội tụ hoặc đưa ra dự đoán sai lệch trên các ca dữ liệu biên.\n- Khi triển khai chiến lược Data-Centric AI nhằm nâng cao hiệu năng mô hình bằng cách cải thiện chất lượng dữ liệu thay vì đổi kiến trúc mạng.",
        "when_not_use": "- Khi dữ liệu nhãn là kết quả đo lường vật lý chính xác từ cảm biến phần cứng đã được hiệu chuẩn.",
        "prereqs": "- **Ngữ cảnh đầu vào:** Tập dữ liệu có nhãn (văn bản, hình ảnh, bảng), danh sách nhãn dự đoán từ mô hình baseline (out-of-sample predicted probabilities).\n- **Quyền hạn truy cập:** Quyền sửa đổi tập nhãn dữ liệu huấn luyện.",
        "concepts": "- **Confident Learning:** Kỹ thuật toán học ước lượng ma trận chuyển tiếp nhãn nhiễu để tìm ra các mẫu dữ liệu có khả năng bị gắn nhãn sai cao nhất.\n- **Cohen's Kappa & Fleiss' Kappa:** Chỉ số thống kê đo lường mức độ đồng thuận giữa hai hoặc nhiều người dán nhãn có loại trừ yếu tố trùng hợp ngẫu nhiên.\n- **Ambiguous vs. Mislabeled Samples:** Phân biệt giữa các mẫu dữ liệu thực sự gây tranh cãi (cần bổ sung quy chuẩn hướng dẫn) và các mẫu bị bấm nhầm nhãn đơn thuần.",
        "workflow": "1. Tính toán ma trận xác suất dự đoán ngoài mẫu (Out-of-sample predicted probabilities) bằng kỹ thuật K-Fold Cross-Validation.\n2. Áp dụng thuật toán Confident Learning (Cleanlab) để xếp hạng các mẫu có xác suất bị gắn nhãn sai cao nhất.\n3. Tính toán chỉ số Cohen's Kappa giữa các kiểm toán viên dữ liệu trên một tập mẫu đại diện.\n4. Trực quan hóa danh sách các mẫu bị nghi ngờ cho chuyên gia nghiệp vụ thẩm định lại.\n5. Cập nhật nhãn chuẩn xác hoặc loại bỏ các mẫu dữ liệu có độ tin cậy quá thấp khỏi tập train.\n6. Ban hành tài liệu hướng dẫn dán nhãn (Labeling Guidelines) bổ sung cho các trường hợp biên.",
        "examples": """### Phát hiện nhãn lỗi tự động bằng Cleanlab trong Python:
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
```""",
        "antipatterns": "- **Blind Model Blaming:** Vội vàng thay đổi kiến trúc mô hình phức tạp hơn trong khi nguyên nhân chính là do 15% nhãn dữ liệu bị gán sai lệch.\n- **Single Annotator Subjectivity:** Để một người duy nhất dán nhãn toàn bộ tập dữ liệu mà không có cơ chế đối soát chéo.\n- **Deleting All Discrepancies:** Tự động xóa sạch tất cả các mẫu khó thay vì phân tích nguyên nhân tại sao con người và mô hình không đồng thuận.",
        "gates": "- **QG-01**: Chỉ số độ đồng thuận giữa các người dán nhãn (Cohen's Kappa) đạt tối thiểu 0.80.\n- **QG-04**: 100% các mẫu bị thuật toán Confident Learning gắn cờ nghi vấn đều được chuyên gia thẩm duyệt lại.\n- **QG-07**: Tập dữ liệu sau khi làm sạch cải thiện độ chính xác của mô hình baseline tối thiểu 2-5%.",
        "security": "- Kiểm tra bảo vệ quyền riêng tư khi xuất dữ liệu mẫu cho nhân viên dán nhãn bên ngoài (ẩn danh hóa PII).",
        "adapters": "- **Tools**: Cleanlab, Label Studio, Prodigy, Scikit-Learn Metrics.",
        "deliverables": "- Danh sách các chỉ mục mẫu dữ liệu bị phát hiện sai nhãn.\n- Báo cáo phân tích chất lượng dữ liệu (Data Health Report).\n- Bộ hướng dẫn dán nhãn đã được chuẩn hóa bổ sung.",
        "related": "dex-training-data-leakage-audit, dex-ai-feedback-labeling, dex-ml-experiment-reproducibility",
        "usage": """```powershell
# Chạy script phân tích lỗi nhãn bằng Cleanlab
python scripts/ml/find_label_issues.py --data dataset.csv --probs probabilities.npy

# Khởi động giao diện thẩm định nhãn Label Studio
label-studio start
```"""
    },
    {
        "id": "dex-batch-inference-pipeline-tuning",
        "name": "dex-batch-inference-pipeline-tuning",
        "desc": "Optimize throughput, GPU memory allocation, dynamic batching, and distributed worker pipelines for large-scale offline batch inference. Use when scoring millions of records within strict operational windows.",
        "purpose": "Tối ưu hóa thông lượng (throughput), cấp phát bộ nhớ GPU, phân đoạn batch động và kiến trúc worker phân tán cho các pipeline suy luận theo lô (Batch Inference) quy mô lớn; bảo đảm hoàn thành tính toán hàng triệu bản ghi trong khung thời gian vận hành cho phép.",
        "when_use": "- Khi cần chấm điểm tín dụng hoặc tính toán khuyến nghị cho 50 triệu người dùng mỗi đêm trong khung giờ 4 tiếng.\n- Khi GPU chỉ hoạt động ở mức 20-30% công suất do bị nghẽn cổ chai tại khâu nạp và tiền xử lý dữ liệu (I/O Bottleneck).\n- Khi gặp lỗi tràn bộ nhớ GPU (CUDA Out of Memory) khi xử lý các bản ghi có kích thước không đồng đều.",
        "when_not_use": "- Khi phục vụ API suy luận thời gian thực với yêu cầu độ trễ dưới 50ms cho từng request đơn lẻ vị trí biên.",
        "prereqs": "- **Ngữ cảnh đầu vào:** Mô hình đã huấn luyện, kho dữ liệu đầu vào (Parquet trên S3/GCS), cụm máy chủ GPU/CPU.\n- **Quyền hạn truy cập:** Quyền điều phối job tính toán phân tán (Ray, Spark, Kubernetes Jobs).",
        "concepts": "- **GPU Saturation vs. I/O Bottleneck:** Giữ cho GPU luôn được nạp đầy tensor tính toán bằng cơ chế bất đồng bộ nạp trước (Prefetching & Pin Memory).\n- **Dynamic Bucket Batching:** Gom các bản ghi có độ dài tương đương vào cùng một batch để giảm thiểu lượng padding vô ích.\n- **vLLM / TensorRT-LLM PagedAttention:** Tối ưu hóa phân mảnh bộ nhớ KV Cache khi chạy suy luận lô cho các mô hình ngôn ngữ lớn.",
        "workflow": "1. Đo lường tỷ lệ tận dụng GPU (GPU Utilization) và thông lượng (records/sec) của pipeline hiện tại.\n2. Triển khai cơ chế Multi-threaded / Async DataLoader với bộ đệm Prefetch để loại bỏ nghẽn I/O đọc đĩa.\n3. Sắp xếp dữ liệu theo độ dài chuỗi và chia nhóm (bucket sorting) trước khi đưa vào batching để giảm lượng padding thừa.\n4. Chuyển đổi mô hình sang định dạng tối ưu phần cứng (TensorRT, ONNX Runtime, FP16/BF16).\n5. Phân bổ công việc phân tán qua nhiều GPU/Node sử dụng Ray Data hoặc PySpark ML.\n6. Kiểm tra giám sát bộ nhớ GPU để bảo đảm không xảy ra hiện tượng tràn RAM (OOM) ở các batch đỉnh.",
        "examples": """### Tối ưu hóa Batch Inference phân tán bằng Ray Data:
```python
import ray
import torch

# Khởi tạo mô hình trên từng Worker GPU
class InferenceWorker:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = torch.jit.load("optimized_model.pt").to(self.device).eval()

    def __call__(self, batch: dict[str, np.ndarray]) -> dict[str, np.ndarray]:
        with torch.inference_mode():
            inputs = torch.from_numpy(batch["features"]).to(self.device, non_blocking=True)
            predictions = self.model(inputs).cpu().numpy()
        return {"predictions": predictions}

# Đọc và suy luận lô phân tán trên hàng triệu bản ghi
ds = ray.data.read_parquet("s3://data-lake/input_features/")
ds = ds.map_batches(
    InferenceWorker,
    concurrency=4, # 4 GPU workers
    batch_size=1024,
    num_gpus=1
)
ds.write_parquet("s3://data-lake/predictions/")
```""",
        "antipatterns": "- **Sequential Disk Reads in GPU Loop:** Đọc từng file ảnh hoặc text từ đĩa trong vòng lặp chính của GPU làm GPU phải chờ nhàn rỗi (idle).\n- **Fixed Excessive Batch Size:** Đặt kích thước batch cố định quá lớn dẫn tới sập OOM khi gặp phải chuỗi văn bản dài đột biến.\n- **Floating Point 32 on GPUs:** Chạy suy luận ở độ chính xác FP32 thay vì FP16 hoặc INT8 làm giảm một nửa thông lượng tính toán khả thi.",
        "gates": "- **QG-01**: Tỷ lệ tận dụng GPU (GPU Core Utilization) duy trì ổn định >= 85% trong suốt quá trình chạy.\n- **QG-04**: Tốc độ thông lượng suy luận tăng tối thiểu 3x so với cấu hình mặc định ban đầu.\n- **QG-07**: 0% lỗi CUDA Out of Memory xảy ra trên toàn bộ tập dữ liệu kiểm thử.",
        "security": "- Mã hóa dữ liệu tạm thời (Scratch disks) trên các worker node trong quá trình xử lý lô dữ liệu nhạy cảm.",
        "adapters": "- **Engines**: Ray Data, PySpark, TensorRT, vLLM, ONNX Runtime, DeepSpeed-Inference.",
        "deliverables": "- Pipeline suy luận theo lô phân tán tối ưu hóa phần cứng.\n- Cấu hình Dynamic Batching và bucket sorter.\n- Báo cáo benchmark thông lượng và chi phí tính toán trên mỗi triệu bản ghi.",
        "related": "dex-model-serving-canary-rollouts, dex-vector-embedding-migration, dex-inference-provider-rate-controls",
        "usage": """```powershell
# Chạy job Ray phân tán phục vụ suy luận lô
ray job submit --address="http://ray-head:8265" -- python batch_inference.py

# Giám sát thông lượng và tải GPU bằng nvidia-smi
nvidia-smi --query-gpu=utilization.gpu,memory.used,memory.total --format=csv -l 1
```"""
    },
    {
        "id": "dex-vector-embedding-migration",
        "name": "dex-vector-embedding-migration",
        "desc": "Orchestrate zero-downtime migration, re-indexing, and dimension alignment across dense vector embeddings and vector databases. Use when upgrading embedding models or transitioning vector infrastructure.",
        "purpose": "Điều phối quy trình chuyển đổi (migration), tái lập chỉ mục (re-indexing) và căn chỉnh chiều vector (dimension alignment) giữa các mô hình embedding hoặc cơ sở dữ liệu vector mà không làm gián đoạn dịch vụ truy hồi đang chạy (Zero-Downtime).",
        "when_use": "- Khi nâng cấp mô hình embedding từ phiên bản cũ (ví dụ: OpenAI Ada-002, 1536 chiều) sang mô hình mới hơn (text-embedding-3-small/large, Voyage, BGE).\n- Khi di chuyển hạ tầng vector database từ giải pháp tự host (Chroma, Faiss) sang nền tảng phân tán đám mây (Qdrant, Pinecone, pgvector).\n- Khi số lượng vector tăng lên hàng trăm triệu cần tái cấu trúc chỉ mục HNSW/IVFFlat để tiết kiệm RAM.",
        "when_not_use": "- Khi hệ thống chỉ là ứng dụng cá nhân nhỏ có thể tạm dừng dịch vụ trong vài giờ để chạy lại toàn bộ từ đầu.",
        "prereqs": "- **Ngữ cảnh đầu vào:** Vector database hiện tại, kho dữ liệu gốc (raw documents), mô hình embedding mới, chỉ mục vector đích.\n- **Quyền hạn truy cập:** Quyền tạo collection mới và chuyển đổi alias định tuyến truy vấn trong vector database.",
        "concepts": "- **Dual-Indexing (Blue/Green Collections):** Nạp và sinh embedding mới vào Collection Green trong khi Collection Blue vẫn tiếp tục phục vụ lưu lượng tìm kiếm của người dùng.\n- **Dimension Incompatibility:** Vector sinh từ hai mô hình embedding khác nhau không thể so sánh khoảng cách với nhau (kể cả khi chúng có cùng số chiều).\n- **Alias Flipping:** Hoán đổi trỏ alias của ứng dụng từ collection cũ sang collection mới trong 1 thao tác nguyên tử (atomic operation) khi re-indexing hoàn tất.",
        "workflow": "1. Khởi tạo Collection mới (Target/Green) với cấu hình số chiều và độ đo khoảng cách (Cosine, Dot Product) của mô hình mới.\n2. Cấu hình cơ chế ghi kép (Dual-Writing): các bản ghi tạo mới hoặc cập nhật được sinh embedding và ghi vào cả hai Collection.\n3. Chạy pipeline xử lý lô nạp lại toàn bộ dữ liệu lịch sử từ kho lưu trữ gốc vào Collection mới bằng mô hình embedding mới.\n4. Thực hiện kiểm thử đối soát chất lượng truy hồi (Retrieval Benchmark): so sánh điểm NDCG@10 giữa hai collection trên tập câu hỏi chuẩn.\n5. Thực hiện đổi hướng truy vấn (Alias Switch) từ Blue sang Green một cách nguyên tử.\n6. Theo dõi lỗi và độ trễ trong 48 giờ trước khi giải phóng tài nguyên của Collection cũ.",
        "examples": """### Hoán đổi Alias nguyên tử trong Qdrant sau khi hoàn tất Re-indexing:
```python
from qdrant_client import QdrantClient
from qdrant_client.http import models

client = QdrantClient(host="localhost", port=6333)

def switch_vector_collection_alias(alias_name: str, old_coll: str, new_coll: str):
    # Thao tac nguyen tu: xoa alias khoi coll cu va tro sang coll moi ngay lap tuc
    client.update_collection_aliases(
        change_aliases_operations=[
            models.DeleteAliasOperation(delete_alias=models.DeleteAlias(alias_name=alias_name)),
            models.CreateAliasOperation(create_alias=models.CreateAlias(collection_name=new_coll, alias_name=alias_name))
        ]
    )
    print(f"Da hoan doi alias '{alias_name}' tu {old_coll} sang {new_coll} thanh cong khong downtime!")
```""",
        "antipatterns": "- **Direct In-Place Mutation:** Xóa và ghi đè vector trực tiếp trên collection đang chạy khiến người dùng gặp lỗi gián đoạn tìm kiếm trong nhiều giờ.\n- **Cross-Model Distance Calculation:** Dùng vector query của mô hình mới để tìm kiếm trong collection chứa vector của mô hình cũ.\n- **Missing Document Backlog:** Quên nạp các bản ghi được tạo ra trong khoảng thời gian pipeline re-indexing đang chạy.",
        "gates": "- **QG-01**: Tỷ lệ lỗi truy vấn của người dùng duy trì ở mức 0% trong suốt quá trình hoán đổi alias.\n- **QG-04**: Số lượng vector trong Collection mới khớp chính xác 100% với số lượng tài liệu trong kho dữ liệu gốc.\n- **QG-06**: Điểm chất lượng truy hồi (NDCG@10) của mô hình mới cao hơn hoặc bằng mô hình cũ trên tập benchmark.",
        "security": "- Duy trì các bộ lọc phân quyền bảo mật (Tenant ID / Metadata ACLs) nguyên vẹn trên collection mới.",
        "adapters": "- **Vector Databases**: Qdrant, Pinecone, Milvus, Weaviate, pgvector.\n- **Embeddings**: OpenAI, Cohere, Voyage AI, HuggingFace Transformers.",
        "deliverables": "- Kịch bản điều phối Re-indexing không downtime.\n- Pipeline kiểm thử chất lượng truy hồi so sánh (A/B retrieval eval).\n- Hướng dẫn rollback dự phòng khi xảy ra sự cố.",
        "related": "dex-embedding-data-preparation, dex-hybrid-search-fusion, dex-rag-freshness-control",
        "usage": """```powershell
# Chạy job nạp lại embedding vào collection mới
python scripts/ml/reindex_embeddings.py --source s3://knowledge-base/ --target-collection v2_knowledge

# Hoán đổi alias sang collection mới
python scripts/ml/swap_collection_alias.py --alias knowledge_prod --new-collection v2_knowledge
```"""
    },
    {
        "id": "dex-realtime-analytics-windowing",
        "name": "dex-realtime-analytics-windowing",
        "desc": "Design and tune streaming window aggregations including tumbling, hopping, sliding, and session windows with watermarking for late-arriving event processing. Use when engineering robust stream processing and operational telemetry pipelines.",
        "purpose": "Thiết kế, tinh chỉnh và kiểm chứng các cơ chế gom nhóm cửa sổ thời gian thực (Streaming Window Aggregations) bao gồm Tumbling, Hopping, Sliding, và Session Windows; áp dụng kỹ thuật đánh dấu mốc thời gian (Watermarking) để xử lý hoàn hảo dữ liệu đến muộn (Late-Arriving Events).",
        "when_use": "- Khi xây dựng hệ thống phát hiện gian lận thanh toán (ví dụ: phát hiện 5 giao dịch trong vòng 1 phút từ các vị trí địa lý khác nhau).\n- Khi tổng hợp số liệu đo lường theo dõi (Metrics Aggregation) từ hàng triệu thiết bị IoT theo cửa sổ thời gian trượt.\n- Khi các sự kiện mạng bị trễ do mất sóng di động và gửi về máy chủ sau vài phút đến vài giờ.",
        "when_not_use": "- Khi dữ liệu chỉ cần tổng hợp tĩnh cuối ngày bằng batch job SQL truyền thống trong Data Warehouse.",
        "prereqs": "- **Ngữ cảnh đầu vào:** Nguồn dữ liệu streaming (Kafka, Kinesis, Redpanda), công cụ xử lý dòng (Apache Flink, Spark Streaming, Faust).\n- **Quyền hạn truy cập:** Quyền quản lý consumer group và triển khai job streaming.",
        "concepts": "- **Event Time vs. Processing Time:** Xử lý dữ liệu dựa trên thời gian sự kiện thực tế xảy ra tại thiết bị client (Event Time) thay vì thời gian máy chủ nhận được dữ liệu (Processing Time).\n- **Watermarks:** Mốc thời gian báo hiệu cho engine biết rằng mọi sự kiện trước mốc $t$ được coi như đã đến đủ, cho phép chốt kết quả cửa sổ tính toán.\n- **Allowed Lateness & Side Outputs:** Cơ chế cho phép chấp nhận các sự kiện đến muộn trong một khoảng thời gian bổ sung và đẩy vào nhánh phụ để cập nhật lại kết quả.",
        "workflow": "1. Xác định loại cửa sổ phù hợp với nghiệp vụ: Tumbling (không giao thoa), Hopping (giao thoa cố định), hoặc Session (dựa trên khoảng lặng tương tác).\n2. Cấu hình bộ trích xuất Event Time từ trường timestamp của bản tin Kafka.\n3. Thiết lập chiến lược sinh Watermark có tính đến độ trễ dự kiến (ví dụ: `forBoundedOutOfOrderness(Duration.ofSeconds(10))` phán đoán trễ tối đa 10s).\n4. Định nghĩa hàm tổng hợp gia tăng (Incremental AggregateFunction) để tiết kiệm bộ nhớ trạng thái (State).\n5. Cấu hình cơ chế Allowed Lateness và cổng xả sự kiện quá muộn (Side Output Dead-Letter Queue).\n6. Kiểm thử dòng dữ liệu với kịch bản các bản tin bị đảo lộn thứ tự và trễ thời gian để xác thực độ chính xác số liệu.",
        "examples": """### Cấu hình Windowing và Watermark trong Apache Flink (Java / Python PyFlink):
```python
from pyflink.common import WatermarkStrategy, Duration, Time
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.window import TumblingEventTimeWindows

env = StreamExecutionEnvironment.get_execution_environment()

# Thiet lap Watermark chap nhan tre toi da 5 giay
watermark_strategy = WatermarkStrategy.for_bounded_out_of_orderness(
    Duration.of_seconds(5)
).with_timestamp_assigner(lambda event, timestamp: event["event_time"])

stream = env.from_source(kafka_source, watermark_strategy, "KafkaSource")

# Gom nhom cua so Tumbling 1 phut dua tren Event Time
windowed_stream = stream \\
    .key_by(lambda event: event["user_id"]) \\
    .window(TumblingEventTimeWindows.of(Time.minutes(1))) \\
    .allowed_lateness(Time.seconds(30)) \\
    .aggregate(TransactionSumAggregate())

windowed_stream.print()
```""",
        "antipatterns": "- **Relying on Processing Time for Business Logic:** Sử dụng thời gian của máy chủ làm sai lệch hoàn toàn thống kê khi mạng gặp sự cố nghẽn kết nối.\n- **Zero Tolerance Watermarks:** Đóng cửa sổ ngay lập tức khiến toàn bộ dữ liệu đến trễ vài mili-giây bị loại bỏ làm mất mát số liệu.\n- **Unbounded Session Inactivity Gap:** Đặt thời gian chờ phiên quá lớn khiến trạng thái (State) của session không bao giờ được giải phóng gây tràn RAM RocksDB.",
        "gates": "- **QG-01**: 100% các phép tính toán nghiệp vụ tài chính/giao dịch đều dựa trên Event Time.\n- **QG-04**: Các sự kiện đến muộn trong ngưỡng cho phép (Allowed Lateness) được cập nhật chính xác vào kết quả tổng hợp.\n- **QG-08**: Bộ nhớ State của streaming job ổn định, không bị rò rỉ bộ nhớ sau 72 giờ vận hành liên tục.",
        "security": "- Đảm bảo tính toán toàn vẹn dữ liệu và mã hóa kênh truyền Kafka/Flink trong suốt quá trình xử lý dòng.",
        "adapters": "- **Engines**: Apache Flink, Spark Structured Streaming, Kafka Streams, RisingWave, Bytewax.",
        "deliverables": "- Kịch bản Stream Processing tích hợp cơ chế Watermark.\n- Cấu hình quản lý State và cơ chế xử lý dữ liệu trễ.\n- Bộ kiểm thử giả lập dòng sự kiện xáo trộn thời gian.",
        "related": "dex-consumer-lag-control, dex-event-replay-safety, dex-batch-inference-pipeline-tuning",
        "usage": """```powershell
# Chạy Flink Job xử lý dòng sự kiện
flink run -m localhost:8081 -py streaming_window_job.py

# Giả lập gửi sự kiện trễ vào Kafka topic để test Watermark
python scripts/simulate_late_events.py --topic transactions --delay-sec 15
```"""
    },
    {
        "id": "dex-metadata-catalog-lineage",
        "name": "dex-metadata-catalog-lineage",
        "desc": "Build automated data cataloging, column-level data lineage, and schema governance pipelines across modern data architectures. Use when implementing data mesh governance and data impact analysis.",
        "purpose": "Xây dựng hệ thống danh mục siêu dữ liệu tự động (Metadata Catalog), truy vết nguồn gốc dữ liệu đến cấp cột (Column-Level Data Lineage) và quản trị lược đồ (Schema Governance); phục vụ phân tích tác động thay đổi (Impact Analysis) và quản trị kiến trúc Data Mesh.",
        "when_use": "- Khi chuẩn bị sửa đổi một cột trong bảng cơ sở dữ liệu nguồn nhưng không rõ có những báo cáo BI hoặc dashboard nào bị ảnh hưởng.\n- Khi cần chứng minh nguồn gốc dữ liệu (Data Provenance) phục vụ các tiêu chuẩn tuân thủ bảo vệ dữ liệu (GDPR, CCPA, Basel III).\n- Khi triển khai mô hình quản trị dữ liệu liên kết (Federated Data Governance) trên nhiều nhóm kỹ thuật.",
        "when_not_use": "- Khi ứng dụng chỉ là một dịch vụ web đơn lẻ sử dụng 3 bảng cơ sở dữ liệu nội bộ không có luồng ETL/ELT.",
        "prereqs": "- **Ngữ cảnh đầu vào:** Kho dữ liệu (Snowflake, BigQuery, Databricks), công cụ ETL (dbt, Airflow, Spark), metadata store.\n- **Quyền hạn truy cập:** Quyền đọc siêu dữ liệu hệ thống (Information Schema, query history logs).",
        "concepts": "- **Column-Level Lineage:** Khả năng truy vết chính xác nguồn gốc của một cột trong báo cáo cuối cùng được tổng hợp từ những cột cụ thể nào của các bảng gốc ban đầu.\n- **OpenLineage Standard:** Chuẩn mở định dạng sự kiện thu thập lineage phục vụ trao đổi thông tin giữa các hệ thống (Spark, Airflow, Flink).\n- **Data Contract:** Thỏa thuận có cấu trúc ràng buộc giữa đội ngũ sản xuất dữ liệu (Data Producer) và đội ngũ tiêu thụ dữ liệu (Data Consumer).",
        "workflow": "1. Thu thập siêu dữ liệu tự động từ các nguồn: cơ sở dữ liệu quan hệ, data warehouse, dbt manifest, và Airflow DAGs.\n2. Phân tích cú pháp các câu lệnh SQL (SQL AST Parsing bằng sqlglot) để trích xuất quan hệ phụ thuộc giữa các bảng và cột.\n3. Đóng gói thông tin thành các sự kiện OpenLineage và đẩy về máy chủ Metadata Catalog (DataHub, Marquez, Amundsen).\n4. Xây dựng đồ thị có hướng (DAG) thể hiện luồng di chuyển của dữ liệu từ nguồn gốc tới đích đến.\n5. Cấu hình kiểm tra phân tích tác động tự động trong CI/CD: cảnh báo nếu PR có nguy cơ phá vỡ các bảng downstream.\n6. Cung cấp giao diện tra cứu danh mục dữ liệu và đánh giá độ tin cậy của các tài sản dữ liệu.",
        "examples": """### Trích xuất Lineage cấp cột từ câu lệnh SQL bằng sqlglot:
```python
from sqlglot import parse_one, exp
from sqlglot.lineage import lineage

sql = '''
CREATE VIEW v_user_spend AS 
SELECT u.user_id, u.email, SUM(o.amount) as total_spent 
FROM users u 
JOIN orders o ON u.user_id = o.user_id 
GROUP BY u.user_id, u.email
'''

# Truy vet nguon goc cua cot 'total_spent'
node = lineage("total_spent", sql)
print("Truy vet nguon goc cot total_spent:")
for source in node.sources:
    print(f" -> Den tu cot/bieu thuc: {source.name} (Source: {source.expression})")
```""",
        "antipatterns": "- **Manual Documentation Spreadsheets:** Quản lý danh mục dữ liệu bằng file Excel thủ công dẫn tới việc tài liệu bị lỗi thời ngay sau 1 tuần.\n- **Table-Only Lineage:** Chỉ theo dõi dữ liệu ở mức bảng mà không biết cột nào liên kết với cột nào khiến việc phân tích tác động thiếu chính xác.\n- **Ignoring Ephemeral Temp Tables:** Không theo dõi các bảng tạm trong luồng ETL dẫn tới việc đồ thị lineage bị đứt đoạn.",
        "gates": "- **QG-01**: 100% các mô hình dbt và bảng warehouse đều có đồ thị lineage tự động ghi nhận.\n- **QG-04**: CI/CD tự động cảnh báo các thay đổi làm hỏng cấu trúc (Breaking Schema Changes) đối với các bảng hạ nguồn.\n- **QG-08**: Độ trễ cập nhật siêu dữ liệu mới vào catalog không vượt quá 2 giờ kể từ khi pipeline chạy xong.",
        "security": "- Gắn thẻ phân loại bảo mật (Confidential, PII, Public) tự động kế thừa dọc theo luồng lineage của dữ liệu.",
        "adapters": "- **Metadata Platforms**: DataHub, Marquez, OpenMetadata, Amundsen.\n- **Lineage Extractors**: OpenLineage, sqlglot, dbt, Apache Atlas.",
        "deliverables": "- Pipeline thu thập siêu dữ liệu tự động từ kho dữ liệu.\n- Đồ thị truy vết nguồn gốc cấp cột hoàn chỉnh.\n- Bot cảnh báo tác động schema trong quy trình Pull Request.",
        "related": "dex-data-masking-synthetic-generation, dex-configuration-schema-design, dex-contract-first-development",
        "usage": """```powershell
# Đẩy metadata từ dự án dbt sang DataHub
datahub ingest -c ./datahub-dbt-recipe.yaml

# Phân tích cú pháp SQL để trích xuất lineage cấp cột
python scripts/extract_column_lineage.py --sql-dir ./models/
```"""
    },
    {
        "id": "dex-data-masking-synthetic-generation",
        "name": "dex-data-masking-synthetic-generation",
        "desc": "Architect realistic data masking, pseudonymization, differential privacy, and synthetic data generation pipelines for staging environments. Use when safeguarding PII while enabling high-fidelity testing.",
        "purpose": "Thiết kế và triển khai quy trình che mờ dữ liệu (Data Masking), giả danh hóa (Pseudonymization), quyền riêng tư vi sai (Differential Privacy) và sinh dữ liệu tổng hợp (Synthetic Data) chân thực cho môi trường staging; bảo vệ thông tin PII trong khi vẫn đảm bảo độ tin cậy cao cho việc kiểm thử phần mềm.",
        "when_use": "- Khi cần trích xuất dữ liệu từ môi trường production về môi trường staging/dev để tái hiện lỗi nhưng bị cấm bởi quy định bảo mật dữ liệu.\n- Khi kiểm thử tải hoặc kiểm thử hệ thống đòi hỏi hàng triệu bản ghi có phân phối thống kê chân thực.\n- Khi chia sẻ dữ liệu với đối tác nghiên cứu bên ngoài mà không được làm lộ thông tin khách hàng.",
        "when_not_use": "- Khi làm việc trên môi trường sản xuất thực tế phục vụ các giao dịch tiền tệ đòi hỏi thông tin khách hàng nguyên bản.",
        "prereqs": "- **Ngữ cảnh đầu vào:** Lược đồ cơ sở dữ liệu, từ điển phân loại dữ liệu nhạy cảm, công cụ sinh dữ liệu (Faker, SDV, Presidio).\n- **Quyền hạn truy cập:** Quyền đọc dữ liệu nguồn đã qua phân quyền kiểm toán và quyền ghi vào database staging.",
        "concepts": "- **Consistent Pseudonymization:** Mã hóa giả danh có tính tất định (Deterministic Masking) để cùng một mã khách hàng vẫn duy trì được các liên kết khóa ngoại (Foreign Keys) giữa các bảng.\n- **Differential Privacy:** Thêm nhiễu toán học có kiểm soát vào dữ liệu thống kê để không một ai có thể suy đoán ngược lại sự hiện diện của một cá nhân cụ thể.\n- **Synthetic Distribution Preservation:** Dữ liệu tổng hợp duy trì chính xác tỷ lệ phân phối, giá trị ngoại lai và tương quan giữa các cột giống như dữ liệu thật.",
        "workflow": "1. Quét lược đồ dữ liệu để tự động nhận diện các cột chứa thông tin PII (Họ tên, Email, Số điện thoại, Số CCCD, Địa chỉ).\n2. Áp dụng quy tắc biến đổi phù hợp cho từng loại trường: Che mờ một phần (Masking), Băm có muối (Salted Hash), hoặc Thay thế bằng dữ liệu giả hợp lệ (Faker).\n3. Đảm bảo tính toàn vẹn tham chiếu (Referential Integrity) giữa các khóa ngoại trên toàn bộ các bảng liên quan.\n4. Sử dụng mô hình tổng hợp thống kê (Copula hoặc GANs) để sinh các bảng dữ liệu số duy trì đúng phân phối xác suất.\n5. Kiểm tra rà soát tập dữ liệu đầu ra để bảo đảm không còn bất kỳ dấu vết thông tin thật nào bị rò rỉ.\n6. Đóng gói pipeline nạp dữ liệu sạch vào quy trình tự động làm mới môi trường Staging hàng tuần.",
        "examples": """### Che mờ dữ liệu PII duy trì khóa ngoại nhất quán bằng Python:
```python
import hashlib
from faker import Faker

fake = Faker(['vi_VN'])
SALT = "c98fbc923a104e76a"

def mask_user_record(raw_user: dict) -> dict:
    # Băm tất định ID để bảo toàn khóa ngoại giữa các bảng
    user_hash = hashlib.sha256((str(raw_user["user_id"]) + SALT).encode()).hexdigest()[:12]
    masked_id = f"usr_{user_hash}"
    
    # Sinh dữ liệu giả lập tiếng Việt hợp lệ thay thế PII
    return {
        "user_id": masked_id,
        "full_name": fake.name(),
        "email": f"{masked_id}@example-staging.internal",
        "phone_number": fake.phone_number(),
        "created_at": raw_user["created_at"] # Giữ nguyên thuộc tính thời gian
    }
```""",
        "antipatterns": "- **Random Non-Deterministic Masking of Foreign Keys:** Che mờ ngẫu nhiên các khóa ID khiến toàn bộ các liên kết khóa ngoại (JOINs) giữa các bảng bị gãy đổ.\n- **Reversible Weak Obfuscation:** Dùng phép mã hóa yếu (như Base64 hoặc phép dịch chuyển ký tự Caesar) có thể bị giải mã ngược lại dễ dàng.\n- **Leaking PII in Unstructured Notes:** Che mờ các cột bảng nhưng bỏ quên các trường văn bản tự do (Notes/Logs) chứa thông tin nhạy cảm của khách hàng.",
        "gates": "- **QG-01**: 0% thông tin định danh PII thực tế xuất hiện trong cơ sở dữ liệu Staging.\n- **QG-04**: 100% các ràng buộc khóa ngoại (Foreign Key Constraints) vẫn hợp lệ sau khi che mờ.\n- **QG-06**: Phân phối thống kê của các trường số liệu tổng hợp đạt độ tương đồng Cosine >= 0.95 so với dữ liệu gốc.",
        "security": "- Tiêu hủy muối băm (Salt) hoặc lưu trữ trong Vault bảo mật để ngăn chặn các cuộc tấn công tra cứu ngược Rainbow Table.",
        "adapters": "- **Tools**: Microsoft Presidio, Faker, SDV (Synthetic Data Vault), PostgreSQL Anonymizer, dbt-osmosis.",
        "deliverables": "- Kịch bản che mờ dữ liệu tự động cho database.\n- Bộ quy tắc nhận diện PII và định nghĩa trường giả lập.\n- Báo cáo kiểm toán xác nhận môi trường Staging sạch thông tin nhạy cảm.",
        "related": "dex-metadata-catalog-lineage, dex-training-data-leakage-audit, dex-online-offline-feature-parity",
        "usage": """```powershell
# Chạy pipeline che mờ dữ liệu từ dump production sang staging
python scripts/data/mask_database.py --source prod_dump.sql --target staging.sql

# Quét kiểm tra dữ liệu PII còn sót lại bằng Microsoft Presidio
python scripts/data/scan_pii_leakage.py --db-url "postgresql://staging-db/app"
```"""
    },

    # =========================================================================
    # GROUP AL: Developer Platform & Polyglot Tooling (Skills 371–380)
    # =========================================================================
    {
        "id": "dex-developer-workstation-bootstrap",
        "name": "dex-developer-workstation-bootstrap",
        "desc": "Automate declarative, idempotent developer machine provisioning across Windows, macOS, and Linux using unified dotfiles, package manifests, and posture verifications. Use when onboarding engineers and eliminating configuration drift.",
        "purpose": "Tự động hóa quá trình thiết lập môi trường máy trạm kỹ sư (Developer Workstation Bootstrap) theo hướng khai báo (declarative) và có tính lũy kế không đổi (idempotent) trên Windows, macOS và Linux; sử dụng dotfiles thống nhất, trình quản lý gói hệ điều hành và kiểm tra tuân thủ cấu hình.",
        "when_use": "- Khi đón nhận kỹ sư mới vào đội ngũ và muốn rút ngắn thời gian thiết lập môi trường từ 3 ngày xuống dưới 30 phút.\n- Khi môi trường máy tính của các thành viên trong đội bị sai lệch cấu hình (configuration drift) dẫn tới lỗi không đồng nhất.\n- Khi thiết lập máy làm việc mới hoặc cài lại hệ điều hành sau sự cố.",
        "when_not_use": "- Khi triển khai cấu hình cho các máy chủ hạ tầng production (nên dùng Ansible, Terraform, hoặc Kubernetes).",
        "prereqs": "- **Ngữ cảnh đầu vào:** File khai báo công cụ (winget, Homebrew, apt), kho cấu hình dotfiles, tài khoản quyền Admin/Sudo cục bộ.\n- **Quyền hạn truy cập:** Quyền thực thi các script tự động hóa trên máy trạm.",
        "concepts": "- **Idempotency:** Khả năng chạy script cài đặt nhiều lần liên tiếp mà không làm hỏng trạng thái hệ thống hoặc cài đè trùng lặp.\n- **Declarative Package Manifests:** Danh sách gói phần mềm được khai báo rõ ràng trong file cấu hình (`Brewfile`, `winget-packages.json`).\n- **Zero-Trust Posture Verification:** Tự động kiểm tra các tiêu chuẩn bảo mật tối thiểu: bật mã hóa ổ đĩa (BitLocker/FileVault), cập nhật bản vá OS, và cấu hình Git signing.",
        "workflow": "1. Nhận diện hệ điều hành mục tiêu (Windows PowerShell, macOS Zsh, Linux Bash).\n2. Cài đặt các trình quản lý gói chuẩn mực (Winget/Chocolatey trên Windows, Homebrew trên macOS/Linux).\n3. Cài đặt tự động toàn bộ danh mục công cụ dòng lệnh (Git, Docker, Node.js, Python, VS Code).\n4. Thiết lập liên kết tượng trưng (Symlinks) cho các file cấu hình dotfiles (`.gitconfig`, `.zshrc`, `settings.json`).\n5. Cấu hình chữ ký số Git commit tự động bằng SSH keys hoặc GPG.\n6. Chạy kịch bản kiểm tra xác thực (Health Check) để xác nhận 100% công cụ sẵn sàng hoạt động.",
        "examples": """### Script khởi tạo máy trạm Windows bằng Winget và PowerShell:
```powershell
# bootstrap-windows.ps1 - Idempotent Developer Setup
$ErrorActionPreference = "Stop"

Write-Host "==> Khoi tao moi truong may tram DEX Engineer..." -ForegroundColor Cyan

# 1. Cai dat cac goi cong cu can thiet qua Winget
$packages = @(
    "Git.Git",
    "Microsoft.VisualStudioCode",
    "Docker.DockerDesktop",
    "Python.Python.3.12",
    "OpenJS.NodeJS.LTS"
)

foreach ($pkg in $packages) {
    Write-Host "Kiem tra / Cai dat: $pkg"
    winget install --id $pkg --exact --silent --accept-source-agreements --accept-package-agreements
}

# 2. Cau hinh Git toan cuc
git config --global core.autocrlf true
git config --global init.defaultBranch main

Write-Host "==> May tram da san sang lam viec!" -ForegroundColor Green
```""",
        "antipatterns": "- **Manual 20-Page Confluence Guide:** Bắt kỹ sư mới đọc tài liệu Word/Wiki dài dặc và tự tay tải từng file installer bằng trình duyệt.\n- **Destructive Re-runs:** Script cài đặt ghi đè hoặc xóa sạch cấu hình cũ của người dùng khi chạy lại lần thứ hai.\n- **Hardcoded Absolute User Paths:** Ghi cứng đường dẫn `/Users/john` khiến script thất bại trên máy của người khác.",
        "gates": "- **QG-01**: Script chạy thành công từ đầu tới cuối trên máy mới hoàn toàn trong vòng dưới 30 phút mà không cần can thiệp thủ công.\n- **QG-04**: Chạy lại script lần thứ hai (re-run) hoàn thành trong dưới 60 giây và giữ nguyên trạng thái đúng đắn.\n- **QG-09**: Tất cả các công cụ cốt lõi (git, docker, python, node) đều phản hồi phiên bản hợp lệ từ terminal.",
        "security": "- Tuyệt đối không lưu trữ khóa riêng tư (Private Keys) hoặc token bí mật trong kho dotfiles công khai.",
        "adapters": "- **Package Managers**: Winget, Homebrew, Chocolatey, apt, mise, asdf.\n- **Dotfile Managers**: Chezmoi, GNU Stow, Dotbot.",
        "deliverables": "- Bộ script bootstrap đa nền tảng (`bootstrap.ps1`, `bootstrap.sh`).\n- File khai báo gói ứng dụng chuẩn hóa.\n- Script kiểm tra tư thế bảo mật và tính sẵn sàng của máy trạm.",
        "related": "dex-toolchain-version-pinning, dex-reproducible-devcontainers, dex-windows-linux-path-compatibility",
        "usage": """```powershell
# Chạy thiết lập máy trạm Windows
powershell -ExecutionPolicy Bypass -File scripts/bootstrap-windows.ps1

# Kiểm tra tính sẵn sàng của toàn bộ công cụ máy trạm
python scripts/doctor.py
```"""
    },
    {
        "id": "dex-toolchain-version-pinning",
        "name": "dex-toolchain-version-pinning",
        "desc": "Enforce strict, automated toolchain version pinning across compilers, runtimes, package managers, and linters using universal version managers and pre-commit hooks. Use when preventing environmental drift across distributed engineering teams.",
        "purpose": "Thực thi việc khóa cứng và tự động hóa phiên bản của toàn bộ chuỗi công cụ (compilers, runtimes, package managers, linters); sử dụng công cụ quản lý phiên bản toàn cầu (mise, asdf) và pre-commit hooks để ngăn chặn sai lệch môi trường giữa các kỹ sư.",
        "when_use": "- Khi lỗi 'chạy được trên máy của người này nhưng vỡ trên máy của người khác' xảy ra do khác biệt phiên bản Node.js, Python hoặc Go.\n- Khi nâng cấp phiên bản runtime toàn hệ thống và cần đảm bảo toàn bộ thành viên trong nhóm chuyển đổi đồng bộ.\n- Khi pipeline CI/CD và máy lập trình viên cục bộ sử dụng các phiên bản compiler khác nhau gây sai khác mã sinh ra.",
        "when_not_use": "- Khi đang làm các dự án thử nghiệm cá nhân nhanh không có yêu cầu phối hợp đồng đội.",
        "prereqs": "- **Ngữ cảnh đầu vào:** File cấu hình phiên bản công cụ (`.tool-versions`, `.mise.toml`, `package.json#engines`), mã nguồn dự án.\n- **Quyền hạn truy cập:** Quyền ghi vào thư mục gốc repository.",
        "concepts": "- **Universal Version Management:** Quản lý đa ngôn ngữ (Python, Node, Go, Rust, Java) trong cùng một file cấu hình duy nhất bằng `mise` hoặc `asdf`.\n- **Engine Strictness:** Chặn đứng việc cài đặt thư viện (`npm install`, `poetry install`) nếu phiên bản runtime hiện tại của máy không khớp với quy định.\n- **Pre-commit Toolchain Gate:** Hook tự động kiểm tra phiên bản các công cụ kiểm tra tĩnh (Linters/Formatters) trước khi cho phép commit mã nguồn.",
        "workflow": "1. Khởi tạo file định nghĩa phiên bản công cụ thống nhất (`.mise.toml` hoặc `.tool-versions`) tại thư mục gốc.\n2. Cố định phiên bản chính xác đến số bản vá (ví dụ: `nodejs 20.11.1`, `python 3.12.2`).\n3. Cấu hình ràng buộc phiên bản trong manifest của từng ngôn ngữ (như `\"engines\": { \"node\": \"20.x\" }` trong `package.json`).\n4. Viết script kiểm tra trước khi commit (pre-commit hook) so sánh phiên bản công cụ đang chạy với file cấu hình.\n5. Tích hợp cùng một file cấu hình phiên bản vào các file định nghĩa pipeline CI/CD (GitHub Actions).\n6. Bật cảnh báo tự động khi các phiên bản công cụ chuẩn bị hết hạn hỗ trợ (End of Life - EOL).",
        "examples": """### Cấu hình khóa cứng phiên bản đa ngôn ngữ bằng .mise.toml:
```toml
# .mise.toml - Dinh nghia phien ban cong cu bat buoc
[tools]
python = "3.12.2"
node = "20.11.1"
pnpm = "8.15.4"
rust = "1.76.0"
golang = "1.22.1"

[settings]
legacy_version_file = false
experimental = true
```

```json
// package.json - Khoa cung runtime va package manager
{
  "name": "my-polyglot-app",
  "engines": {
    "node": ">=20.11.0 <21.0.0",
    "pnpm": ">=8.15.0"
  },
  "packageManager": "pnpm@8.15.4"
}
```""",
        "antipatterns": "- **Floating Latest Versions:** Khai báo phiên bản `node: latest` hoặc `python: 3.x` trong CI khiến pipeline có thể sụp đổ bất kỳ lúc nào khi có bản phát hành mới.\n- **Multiple Conflicting Version Files:** Vừa duy trì `.nvmrc`, vừa có `.node-version`, vừa có `asdf` với các số phiên bản khác nhau gây xung đột.\n- **Ignoring Linter Versions:** Dùng các phiên bản linter khác nhau giữa các máy khiến git diff bị nhiễu loạn định dạng mã nguồn.",
        "gates": "- **QG-01**: 100% các runtime và compiler cốt lõi được định nghĩa phiên bản chính xác trong `.mise.toml`.\n- **QG-04**: CI/CD và máy trạm cục bộ sử dụng cùng một hash/phiên bản công cụ biên dịch.\n- **QG-07**: Quy trình pre-commit chặn đứng ngay lập tức các commit nếu phát hiện sai lệch phiên bản.",
        "security": "- Tránh sử dụng các phiên bản runtime đã chạm ngưỡng End-of-Life (EOL) có nguy cơ chứa lỗ hổng bảo mật không được vá.",
        "adapters": "- **Version Managers**: mise-en-place, asdf, nvm, pyenv, Corepack, aqua.",
        "deliverables": "- File cấu hình `.mise.toml` hoặc `.tool-versions` chuẩn mực.\n- Hook kiểm tra phiên bản pre-commit.\n- Tài liệu hướng dẫn đồng bộ hóa công cụ cho thành viên mới.",
        "related": "dex-developer-workstation-bootstrap, dex-reproducible-devcontainers, dex-polyglot-build-orchestration",
        "usage": """```powershell
# Cài đặt chính xác các phiên bản công cụ được chỉ định
mise install

# Kiểm tra tính tương thích của toàn bộ toolchain
mise doctor
```"""
    },
    {
        "id": "dex-polyglot-build-orchestration",
        "name": "dex-polyglot-build-orchestration",
        "desc": "Orchestrate multi-language, multi-package monorepo builds with incremental compilation, graph-aware task scheduling, and remote caching. Use when scaling complex software architectures composed of heterogeneous languages.",
        "purpose": "Điều phối và tối ưu hóa quy trình biên dịch monorepo đa ngôn ngữ (Polyglot Build Orchestration); áp dụng cơ chế biên dịch gia tăng (incremental compilation), lập lịch thực thi dựa trên đồ thị phụ thuộc (Graph-Aware Task Scheduling) và bộ nhớ đệm từ xa (Remote Caching).",
        "when_use": "- Khi repository chứa nhiều module viết bằng các ngôn ngữ khác nhau (frontend TypeScript, backend Go, ML Python, native core Rust).\n- Khi thời gian build toàn bộ dự án kéo dài hàng chục phút làm chậm chu kỳ phản hồi của lập trình viên.\n- Khi chỉ sửa một dòng code ở một module nhưng hệ thống bắt biên dịch lại toàn bộ các dự án không liên quan.",
        "when_not_use": "- Khi dự án là một repository đơn ngôn ngữ nhỏ chỉ có vài trăm dòng code và thời gian build dưới 10 giây.",
        "prereqs": "- **Ngữ cảnh đầu vào:** Mã nguồn monorepo đa ngôn ngữ, công cụ điều phối build (Bazel, Nx, Turborepo, Pants, Earthly).\n- **Quyền hạn truy cập:** Quyền sửa đổi file cấu hình build hệ thống và máy chủ lưu trữ cache.",
        "concepts": "- **Task Dependency Graph:** Đồ thị có hướng (DAG) thể hiện thứ tự các bước build và kiểm thử; các tác vụ độc lập được thực thi song song tự động.\n- **Remote Caching:** Lưu trữ kết quả đầu ra của các tác vụ build vào bộ nhớ đệm đám mây dựa trên mã băm nội dung đầu vào (Input Hash); nếu đầu vào không đổi, kết quả được khôi phục ngay lập tức mà không cần biên dịch lại.\n- **Hermetic Builds:** Quá trình biên dịch hoàn toàn khép kín, chỉ phụ thuộc vào các đầu vào đã khai báo tường minh, không bị ảnh hưởng bởi file rác trên máy chủ.",
        "workflow": "1. Khảo sát cấu trúc repository và phân ranh giới các gói module độc lập.\n2. Khai báo các mục tiêu build (Targets) và đồ thị phụ thuộc giữa các module trong file cấu hình (Nx, Bazel, Earthly).\n3. Cấu hình cơ chế tính mã băm đầu vào (Inputs Hash) bao gồm mã nguồn, biến môi trường và phiên bản compiler.\n4. Kích hoạt bộ nhớ đệm cục bộ và kết nối tới dịch vụ Remote Cache (S3 hoặc HTTP Cache Server).\n5. Tối ưu hóa việc thực thi song song các tác vụ kiểm thử và linting trên các nhân CPU khả dụng.\n6. Đo lường tỷ lệ trúng cache (Cache Hit Ratio) và thời gian hoàn thành build qua từng commit.",
        "examples": """### Cấu hình điều phối tác vụ và Remote Cache bằng Turborepo (turbo.json):
```json
{
  "$schema": "https://turbo.build/schema.json",
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "inputs": ["src/**", "package.json", "tsconfig.json"],
      "outputs": ["dist/**", "build/**"]
    },
    "test": {
      "dependsOn": ["build"],
      "inputs": ["src/**", "tests/**"],
      "outputs": []
    },
    "lint": {
      "outputs": []
    }
  }
}
```""",
        "antipatterns": "- **Blind Monolithic Scripts:** Viết một script shell tuần tự `cd frontend && npm run build && cd ../backend && go build` không có cache và không chạy song song.\n- **Undeclared Task Dependencies:** Chạy test backend phụ thuộc vào binary của module khác nhưng không khai báo quan hệ phụ thuộc trong build graph.\n- **Non-Hermetic Build Inputs:** Nhúng các biến động như thời gian hiện tại vào input hash khiến cache luôn bị trượt (Cache Miss).",
        "gates": "- **QG-01**: 100% các module có quan hệ phụ thuộc được thể hiện chính xác trong đồ thị DAG.\n- **QG-04**: Tỷ lệ trúng cache (Cache Hit Rate) trên CI đạt tối thiểu 70% đối với các PR chỉ sửa đổi cục bộ.\n- **QG-08**: Thời gian build khi trúng cache giảm tối thiểu 80% so với build sạch từ đầu.",
        "security": "- Bảo vệ toàn vẹn Remote Cache bằng chữ ký mật mã (HMAC) để ngăn ngừa việc đầu độc cache với mã độc biên dịch sẵn.",
        "adapters": "- **Orchestrators**: Turborepo, Nx, Bazel, Pantsbuild, Earthly, Make.",
        "deliverables": "- File cấu hình đồ thị build monorepo hoàn chỉnh.\n- Cấu hình tích hợp Remote Caching an toàn trên CI/CD.\n- Dashboard đo lường thời gian build và hiệu suất cache.",
        "related": "dex-build-cache-integrity, dex-toolchain-version-pinning, dex-cross-language-contract-tests",
        "usage": """```powershell
# Chạy build song song có sử dụng cache bằng Turborepo
npx turbo run build --cache-dir=.turbo

# Kiểm tra trực quan đồ thị phụ thuộc của monorepo
npx nx graph
```"""
    },
    {
        "id": "dex-build-cache-integrity",
        "name": "dex-build-cache-integrity",
        "desc": "Safeguard, audit, and cryptographically verify local and remote build artifact caches against cache poisoning, stale dependency injection, and non-hermetic invalidation leaks. Use when operating enterprise-scale shared build caches.",
        "purpose": "Bảo vệ, kiểm toán và xác minh mật mã tính toàn vẹn của bộ nhớ đệm bản dựng (Build Cache Integrity); ngăn ngừa các cuộc tấn công đầu độc cache (Cache Poisoning), tiêm nhiễm phụ thuộc lỗi thời và rò rỉ vô hiệu hóa không khép kín trong các hệ thống cache dùng chung.",
        "when_use": "- Khi nhiều kỹ sư và máy chủ CI cùng đọc/ghi vào một bộ nhớ đệm bản dựng từ xa (Shared Remote Cache).\n- Khi phát hiện một artifact bị lỗi hoặc chứa mã độc vô tình được lưu vào cache và lây lan sang máy của các kỹ sư khác.\n- Khi hệ thống không tự động vô hiệu hóa cache (invalidation) dù mã nguồn thư viện liên quan đã thay đổi.",
        "when_not_use": "- Khi chỉ sử dụng bộ nhớ đệm cục bộ cá nhân trên một máy đơn lẻ không chia sẻ với bất kỳ ai.",
        "prereqs": "- **Ngữ cảnh đầu vào:** Máy chủ lưu trữ remote cache (S3, MinIO, GCP Storage), khóa bí mật ký cache (HMAC secret), cấu hình build tool.\n- **Quyền hạn truy cập:** Quyền quản trị máy chủ cache và cấu hình phân quyền truy cập read/write.",
        "concepts": "- **Cache Poisoning:** Kẻ tấn công hoặc một máy bị nhiễm gửi một artifact độc hại ứng với một mã băm đầu vào hợp lệ vào cache chung, khiến toàn bộ hệ thống tải về mã độc đó.\n- **Cryptographic Cache Signing:** Mọi artifact đưa vào remote cache phải được ký bằng khóa bí mật chỉ có máy chủ CI tin cậy nắm giữ; máy trạm của lập trình viên chỉ có quyền Đọc (Read-Only).\n- **Input Key Determinism:** Đảm bảo mã băm của cache key bao quát toàn bộ các yếu tố môi trường (compiler flags, OS architecture, dependencies hashes).",
        "workflow": "1. Thiết lập phân quyền truy cập cache nghiêm ngặt: Chỉ các runner CI chính thức mới có quyền Ghi (Write) vào remote cache; máy cá nhân chỉ có quyền Đọc (Read-Only).\n2. Cấu hình cơ chế ký số mã băm (HMAC-SHA256) cho từng artifact được đưa lên cache.\n3. Quét định kỳ kho lưu trữ cache để phát hiện và tiêu hủy các artifact bất thường hoặc quá hạn.\n4. Kiểm tra độ nhạy của cache key: thay đổi một cờ compiler và xác minh rằng cache key bị thay đổi tương ứng.\n5. Xây dựng nút khẩn cấp (Emergency Flush Button) cho phép xóa sạch toàn bộ remote cache trong vòng 30 giây khi phát hiện sự cố.\n6. Lập báo cáo kiểm toán tính toàn vẹn và tỷ lệ trúng/trượt của hệ thống cache.",
        "examples": """### Xác minh chữ ký số của artifact trước khi giải nén cache trong Python:
```python
import hmac
import hashlib

def verify_and_extract_cache(artifact_bytes: bytes, received_signature: str, secret_key: bytes, output_path: str):
    # Tinh toan chu ky HMAC cua du lieu artifact
    expected_signature = hmac.new(secret_key, artifact_bytes, hashlib.sha256).hexdigest()
    
    # So sanh chu ky an toan theo thoi gian co dinh (Timing-Safe)
    if not hmac.compare_digest(expected_signature, received_signature):
        raise SecurityError("Canh bao an ninh: Chu ky cache khong hop le! Nghi van dau doc cache!")
        
    with open(output_path, "wb") as f:
        f.write(artifact_bytes)
    print(f"Xac thuc toan ven thanh cong: {output_path}")
```""",
        "antipatterns": "- **Global Read-Write Cache Tokens:** Chia sẻ một token có quyền Ghi vào remote cache cho toàn bộ máy lập trình viên cá nhân.\n- **Excluding Compiler Flags from Cache Key:** Chỉ băm nội dung file nguồn mà bỏ qua cờ biên dịch (như `-O3` vs `-O0`) khiến lấy nhầm bản build debug cho production.\n- **Never Evicting Stale Cache:** Để cache tích tụ qua nhiều năm tiêu tốn hàng terabyte dung lượng mà không có chính sách hết hạn (TTL).",
        "gates": "- **QG-01**: Máy trạm cá nhân không có quyền ghi đè hoặc đưa artifact mới vào remote cache sản xuất.\n- **QG-04**: 100% artifact tải về từ remote cache đều vượt qua kiểm tra tính toàn vẹn chữ ký HMAC.\n- **QG-09**: Khả năng dọn sạch toàn bộ cache bị ô nhiễm (Cache Invalidation) thực hiện thành công trong dưới 60 giây.",
        "security": "- Cách ly máy chủ cache trong mạng nội bộ và yêu cầu xác thực TLS có chứng chỉ tương hỗ (mTLS) khi truyền tải artifact.",
        "adapters": "- **Storage**: AWS S3, MinIO, GCP Cloud Storage, Azure Blob.\n- **Build Caches**: Bazel Remote Cache, Turborepo Remote Cache, Gradle Enterprise, sccache.",
        "deliverables": "- Cấu hình phân quyền truy cập Remote Cache (Read-Only vs Read-Write).\n- Script ký số và xác minh chữ ký HMAC cho artifact.\n- Quy trình xử lý khẩn cấp khi nghi ngờ cache bị đầu độc.",
        "related": "dex-polyglot-build-orchestration, dex-toolchain-reproducibility-audit, dex-binary-provenance-matching",
        "usage": """```powershell
# Kiểm tra kết nối và tính toàn vẹn của sccache (Rust / C++ compiler cache)
sccache --show-stats

# Xóa sạch cache cục bộ và kiểm tra lại trạng thái
sccache --zero-stats
```"""
    },
    {
        "id": "dex-cross-language-contract-tests",
        "name": "dex-cross-language-contract-tests",
        "desc": "Design and verify cross-language API contracts, Protocol Buffers schemas, OpenAPI specifications, and consumer-driven contracts between polyglot microservices. Use when eliminating integration drift across diverse programming stacks.",
        "purpose": "Thiết kế, kiểm thử và xác minh các giao ước API đa ngôn ngữ (Cross-Language Contract Tests), lược đồ Protocol Buffers, đặc tả OpenAPI và hợp đồng hướng người tiêu dùng (Consumer-Driven Contracts) giữa các microservices viết bằng các ngôn ngữ khác nhau.",
        "when_use": "- Khi dịch vụ backend viết bằng Go/Java cung cấp API cho client viết bằng TypeScript/Swift và thường xuyên bị lỗi không khớp kiểu dữ liệu.\n- Khi cập nhật một trường dữ liệu trong API và cần bảo đảm không làm gãy các dịch vụ tiêu thụ khác.\n- Khi muốn kiểm thử khả năng tương thích dịch vụ mà không cần khởi động toàn bộ cụm microservices phức tạp.",
        "when_not_use": "- Khi tất cả các dịch vụ đều nằm trong cùng một ứng dụng nguyên khối (Monolith) và chia sẻ chung các struct nội bộ.",
        "prereqs": "- **Ngữ cảnh đầu vào:** File định nghĩa giao ước (OpenAPI YAML, `.proto` files, Pact contracts), mã nguồn client và server.\n- **Quyền hạn truy cập:** Quyền chạy test suite kiểm thử hợp đồng và truy cập Pact Broker.",
        "concepts": "- **Consumer-Driven Contracts (Pact):** Phía tiêu thụ (Consumer) định nghĩa chính xác những dữ liệu mà họ kỳ vọng nhận được; phía cung cấp (Provider) chạy kiểm thử để chứng minh họ đáp ứng đầy đủ kỳ vọng đó.\n- **Schema Compatibility Rules:** Các quy tắc tương thích xuôi và ngược (Backward / Forward Compatibility) khi thêm, bớt hoặc đổi tên trường trong protobuf.\n- **Pact Broker:** Máy chủ trung tâm lưu trữ và xác nhận trạng thái tương thích giữa các phiên bản dịch vụ trước khi cho phép deploy (`can-i-deploy`).",
        "workflow": "1. Phía Consumer viết kiểm thử hợp đồng mô tả yêu cầu request và response mong đợi.\n2. Chạy test Consumer để tự động sinh file hợp đồng chuẩn hóa (Pact JSON).\n3. Đẩy file hợp đồng lên Pact Broker trung tâm kèm số phiên bản commit Git.\n4. Phía Provider chạy kiểm thử xác thực hợp đồng (Provider Verification Test) đối chiếu mã nguồn của họ với Pact file.\n5. Tích hợp lệnh kiểm tra `can-i-deploy` vào pipeline CI/CD trước khi triển khai dịch vụ.\n6. Chặn đứng việc phát hành nếu phát hiện thay đổi phá vỡ giao dịch giữa hai ngôn ngữ.",
        "examples": """### Kiểm thử xác thực Provider bằng Pact trong Python / TypeScript:
```typescript
// consumer.test.ts (TypeScript)
import { PactV3, MatchersV3 } from '@pact-foundation/pact';

const provider = new PactV3({
  consumer: 'WebFrontend-TS',
  provider: 'OrderService-Go',
});

it('nhan ve thong tin don hang hop le tu Go Service', async () => {
  provider
    .given('don hang ton tai voi ID 100')
    .uponReceiving('yeu cau lay chi tiet don hang')
    .withRequest({ method: 'GET', path: '/orders/100' })
    .willRespondWith({
      status: 200,
      body: {
        id: MatchersV3.integer(100),
        amount: MatchersV3.decimal(150.50),
        status: MatchersV3.like('COMPLETED'),
      },
    });

  await provider.executeTest(async (mockServer) => {
    const res = await fetch(`${mockServer.url}/orders/100`);
    const data = await res.json();
    expect(data.status).toBe('COMPLETED');
  });
});
```""",
        "antipatterns": "- **End-to-End Test Reliance:** Chỉ dựa vào các bài test E2E cồng kềnh, chạy chậm và hay gặp lỗi chập chờn (flaky) để phát hiện sai lệch API.\n- **Unversioned Breaking Changes:** Xóa hoặc sửa kiểu của một trường dữ liệu trong protobuf mà không tạo phiên bản mới (v1 -> v2).\n- **Manual Mock Verification:** Viết các mock dữ liệu giả lập thủ công ở phía client mà không bao giờ đối soát lại với API thực tế của server.",
        "gates": "- **QG-01**: 100% các endpoint liên dịch vụ có hợp đồng Pact hoặc protobuf schema được kiểm thử tự động.\n- **QG-04**: Lệnh `pact-broker can-i-deploy` trả về kết quả thành công trước khi bước deploy bắt đầu.\n- **QG-07**: Không có thay đổi phá vỡ tương thích ngược (Breaking Change) nào được chấp thuận vào main branch.",
        "security": "- Không đưa dữ liệu thật hoặc thông tin bí mật vào các fixture mẫu của hợp đồng API.",
        "adapters": "- **Contract Testing**: Pact (TypeScript, Go, Python, Java, Rust), Buf (Protobuf), OpenAPI Tools, Spectral.",
        "deliverables": "- File hợp đồng Pact JSON hoặc Protocol Buffers schemas.\n- Test suite kiểm thử giao ước hai đầu Consumer và Provider.\n- Cấu hình kiểm tra `can-i-deploy` trong pipeline CI.",
        "related": "dex-contract-first-development, dex-configuration-schema-design, dex-polyglot-build-orchestration",
        "usage": """```powershell
# Chạy kiểm tra tính tương thích trước khi triển khai dịch vụ
npx pact-broker can-i-deploy --pacticipant WebFrontend-TS --version 1.2.0 --to-environment production

# Kiểm tra tính tương thích của Protobuf bằng Buf
buf breaking --against ".git#branch=main"
```"""
    },
    {
        "id": "dex-reproducible-devcontainers",
        "name": "dex-reproducible-devcontainers",
        "desc": "Standardize development environments using OCI Dev Containers, dotfile integration, non-root user permissions, and host volume optimization across Windows, macOS, and Linux. Use when onboarding developers into complex distributed codebases.",
        "purpose": "Chuẩn hóa môi trường làm việc của lập trình viên bằng OCI Dev Containers; tích hợp dotfiles cá nhân, bảo đảm quyền hạn người dùng phi root (non-root), và tối ưu hóa hiệu năng gắn kết ổ đĩa (Host Volume Mounts) trên Windows, macOS và Linux.",
        "when_use": "- Khi dự án yêu cầu nhiều dependency phức tạp (PostgreSQL, Redis, C++ compilers, Python packages) khó cài đặt đồng nhất trên máy thật.\n- Khi muốn lập trình viên mới có thể mở repo trong VS Code / Cursor và bắt đầu viết code ngay lập tức mà không cần cài đặt gì thêm vào máy chủ.\n- Khi muốn cách ly môi trường chạy mã nguồn khỏi hệ điều hành máy tính cá nhân.",
        "when_not_use": "- Khi phát triển các ứng dụng đòi hỏi can thiệp sâu vào phần cứng máy tính (Kernel drivers, Bluetooth, thiết bị USB ngoại vi).",
        "prereqs": "- **Ngữ cảnh đầu vào:** File cấu hình `.devcontainer/devcontainer.json`, Dockerfile, Docker Desktop hoặc Finch/Podman.\n- **Quyền hạn truy cập:** Quyền thực thi Docker và quyền gắn kết thư mục workspace.",
        "concepts": "- **Development Containers Specification:** Chuẩn mở định nghĩa môi trường phát triển bên trong container bao gồm phần mềm, biến môi trường và extension của IDE.\n- **Non-Root Safety:** Chạy phiên làm việc dưới quyền người dùng thông thường (`vscode` hoặc `node`) thay vì quyền `root` để bảo vệ an toàn tệp tin trên máy trạm.\n- **Volume Performance on Windows/macOS:** Tránh mount trực tiếp ổ đĩa Windows NTFS (`/mnt/c`) vào Docker container do độ trễ dịch I/O; nên clone mã nguồn trực tiếp vào WSL2 hoặc Docker Volume.",
        "workflow": "1. Khởi tạo thư mục `.devcontainer` kèm file `devcontainer.json` và `Dockerfile` cơ sở tối ưu hóa.\n2. Cấu hình người dùng phi root (`remoteUser: \"vscode\"`) và cấp quyền sudo có giới hạn nếu cần thiết.\n3. Định nghĩa danh sách các extension VS Code và cấu hình IDE mặc định cần tự động kích hoạt khi mở container.\n4. Tích hợp chuyển tiếp cổng mạng (Forward Ports) cho các dịch vụ web và database nội bộ.\n5. Thiết lập cache cho các thư mục gói phụ thuộc (`node_modules`, `.cargo`, `.cache`) bằng Named Volumes để tăng tốc độ I/O.\n6. Kiểm thử quy trình mở container tự động từ giao diện VS Code và GitHub Codespaces.",
        "examples": """### Cấu hình .devcontainer/devcontainer.json chuẩn mực:
```json
{
  "name": "DEX Polyglot Workspace",
  "build": {
    "dockerfile": "Dockerfile",
    "context": ".."
  },
  "remoteUser": "vscode",
  "features": {
    "ghcr.io/devcontainers/features/common-utils:2": {
      "username": "vscode",
      "upgradePackages": true
    },
    "ghcr.io/devcontainers/features/git:1": {}
  },
  "customizations": {
    "vscode": {
      "settings": {
        "editor.formatOnSave": true,
        "terminal.integrated.defaultProfile.linux": "zsh"
      },
      "extensions": [
        "ms-python.python",
        "dbaeumer.vscode-eslint",
        "rust-lang.rust-analyzer"
      ]
    }
  },
  "forwardPorts": [3000, 8000],
  "postCreateCommand": "bash .devcontainer/post-create.sh"
}
```""",
        "antipatterns": "- **Running Everything as Root:** Chạy container dưới quyền `root` khiến các file tạo ra trên máy thật bị khóa quyền và khó xóa bỏ.\n- **Mounting Slow Windows Paths:** Đặt repository tại `C:\\workspace` rồi mount vào container khiến tốc độ `git status` và `npm install` chậm đi 10 lần so với chạy trong WSL2.\n- **Monolithic 20GB Images:** Cài đặt toàn bộ các công cụ trên thế giới vào một image duy nhất thay vì sử dụng Dev Container Features modular.",
        "gates": "- **QG-01**: Container khởi động thành công và vượt qua script `post-create.sh` trong dưới 5 phút.\n- **QG-04**: Tiến trình người dùng trong container chạy dưới quyền phi root (UID != 0).\n- **QG-09**: Tất cả các cổng mạng cần thiết (API, Web) được chuyển tiếp và kết nối thông suốt.",
        "security": "- Tuyệt đối không mount Docker socket (`/var/run/docker.sock`) vào container trừ khi thực sự cần tính năng Docker-in-Docker an toàn.",
        "adapters": "- **Tools**: VS Code Remote - Containers, Dev Container CLI, GitHub Codespaces, Docker, Podman.",
        "deliverables": "- Thư mục cấu hình `.devcontainer` hoàn chỉnh.\n- Dockerfile cơ sở đã được tối ưu bảo mật và kích thước.\n- Script thiết lập sau khởi tạo `post-create.sh`.",
        "related": "dex-developer-workstation-bootstrap, dex-toolchain-version-pinning, dex-windows-linux-path-compatibility",
        "usage": """```powershell
# Chạy kiểm tra và build Dev Container bằng devcontainer CLI
npx @devcontainers/cli up --workspace-folder .

# Thực thi lệnh kiểm tra môi trường bên trong container
npx @devcontainers/cli exec --workspace-folder . whoami
```"""
    },
    {
        "id": "dex-cli-command-contracts",
        "name": "dex-cli-command-contracts",
        "desc": "Specify, validate, and test POSIX and GNU command-line interface conventions, flag semantics, JSON streaming output, exit codes, and shell completions. Use when engineering robust developer CLIs and automated agent tools.",
        "purpose": "Đặc tả, xác thực và kiểm thử các quy ước giao diện dòng lệnh (CLI), ngữ nghĩa các cờ lệnh (flags), định dạng đầu ra chuẩn (JSON/Text), mã thoát (exit codes) và kịch bản tự động hoàn thành lệnh (shell completions); bảo đảm CLI hoạt động đáng tin cậy cả với con người và các AI coding agents.",
        "when_use": "- Khi xây dựng công cụ dòng lệnh nội bộ phục vụ hàng trăm kỹ sư trong tổ chức hoặc làm công cụ cho AI Agent tương tác.\n- Khi các cờ lệnh của CLI thiếu nhất quán (chỗ thì dùng `--output`, chỗ thì dùng `-o`, chỗ thì trả text không thể parse).\n- Khi cần hỗ trợ chế độ xuất dữ liệu JSON có cấu trúc (`--format=json`) phục vụ tự động hóa.",
        "when_not_use": "- Khi chỉ viết một đoạn script shell đơn giản dùng một lần không có nhu cầu tham số hóa.",
        "prereqs": "- **Ngữ cảnh đầu vào:** Mã nguồn công cụ CLI, thư viện xử lý CLI (Click, Cobra, Commander, Clap).\n- **Quyền hạn truy cập:** Quyền thực thi và kiểm thử câu lệnh trên máy trạm.",
        "concepts": "- **Standard Exit Codes:** Tuân thủ chuẩn POSIX (`0` = Thành công, `1` = Lỗi thông thường, `2` = Lỗi cú pháp lệnh, `130` = Bị ngắt bởi Ctrl+C).\n- **Machine-Readable Output:** Cung cấp cờ `--json` hoặc `--format=json` để xuất dữ liệu JSON thuần túy ra `stdout` mà không bị trộn lẫn với nhật ký thông tin (logs/spinners phải đưa sang `stderr`).\n- **Idempotent Flags:** Hỗ trợ các cờ lệnh an toàn: `--dry-run` (chạy thử không ghi dữ liệu), `--quiet` (chỉ xuất kết quả), `--verbose` (hiển thị chi tiết).",
        "workflow": "1. Thiết kế bảng đặc tả câu lệnh, cờ tham số và mã thoát tuân thủ chuẩn GNU/POSIX.\n2. Tách biệt hoàn toàn luồng dữ liệu kết quả (`stdout`) và luồng thông báo tiến trình/lỗi (`stderr`).\n3. Cài đặt cờ `--dry-run` cho tất cả các thao tác có khả năng thay đổi hoặc phá hủy dữ liệu.\n4. Thiết lập schema JSON kiểm chứng cho dữ liệu xuất ra khi người dùng truyền cờ `--json`.\n5. Tự động sinh file hoàn thành lệnh (Shell Completions) cho Bash, Zsh, Fish và PowerShell.\n6. Viết bộ test tự động kiểm thử toàn bộ các mã thoát và định dạng đầu ra.",
        "examples": """### Xây dựng CLI chuẩn mực với cờ JSON và phân tách stderr trong Python (Click):
```python
import sys
import json
import click

@click.command()
@click.option('--format', type=click.Choice(['text', 'json']), default='text', help='Dinh dang dau ra')
@click.option('--dry-run', is_flag=True, help='Chay thu khong ghi du lieu')
def deploy(format: str, dry_run: bool):
    '''Trien khai ung dung voi quy uoc CLI chuan muc.'''
    # Thong bao tien trinh luon day sang stderr
    sys.stderr.write("Dang kiem tra cau hinh he thong...\n")
    
    if dry_run:
        sys.stderr.write("[DRY-RUN] Khong co thay doi nao duoc thuc thi.\n")
        
    result = {"status": "SUCCESS", "dry_run": dry_run, "code": 0}
    
    # Ket qua du lieu may doc duoc xuat ra stdout
    if format == 'json':
        click.echo(json.dumps(result))
    else:
        click.echo(f"Ket qua: {result['status']}")
        
    sys.exit(0)

if __name__ == '__main__':
    deploy()
```""",
        "antipatterns": "- **Polluting stdout with Spinners:** In con trỏ xoay hoặc thông báo 'Đang tải...' vào luồng `stdout` khiến câu lệnh `app --json | jq .` bị lỗi cú pháp.\n- **Returning Exit Code 0 on Failures:** Câu lệnh gặp lỗi nghiêm trọng nhưng vẫn thoát với exit code `0` khiến script tự động hóa không phát hiện được sự cố.\n- **Inconsistent Flag Naming:** Dùng lẫn lộn camelCase (`--dryRun`) và kebab-case (`--dry-run`) trong cùng một bộ công cụ.",
        "gates": "- **QG-01**: Cờ `--json` xuất ra chuỗi JSON hợp lệ 100% không chứa bất kỳ ký tự rác nào trên `stdout`.\n- **QG-04**: Khi gặp lỗi cú pháp hoặc tham số không hợp lệ, CLI luôn thoát với mã lỗi khác 0.\n- **QG-07**: 100% các lệnh có thao tác phá hủy đều hỗ trợ cờ `--dry-run`.",
        "security": "- Ẩn giấu các giá trị mật khẩu hoặc API key trên dòng lệnh bằng cách hỗ trợ đọc từ file hoặc biến môi trường thay vì cờ dòng lệnh lộ trong `ps`.",
        "adapters": "- **CLI Frameworks**: Click/Typer (Python), Cobra (Go), Clap (Rust), Commander (Node.js).",
        "deliverables": "- Mã nguồn công cụ CLI tuân thủ hợp đồng giao diện.\n- Kịch bản tự động sinh Shell Completions.\n- Bộ kiểm thử tự động xác minh các mã thoát và luồng dữ liệu.",
        "related": "dex-windows-linux-path-compatibility, dex-developer-workstation-bootstrap, dex-polyglot-build-orchestration",
        "usage": """```powershell
# Chạy kiểm thử xuất dữ liệu JSON và lọc bằng jq
python cli.py --format=json | jq .status

# Kiểm tra mã thoát của câu lệnh khi gặp lỗi
python cli.py --invalid-flag
echo "Exit code: $LASTEXITCODE"
```"""
    },
    {
        "id": "dex-windows-linux-path-compatibility",
        "name": "dex-windows-linux-path-compatibility",
        "desc": "Audit and eliminate cross-platform path separator bugs, CRLF/LF line-ending corruption, drive-letter handling flaws, and case-sensitivity defects across polyglot codebases. Use when ensuring Windows and POSIX operational parity.",
        "purpose": "Kiểm toán và triệt tiêu các lỗi tương thích đường dẫn đa nền tảng; giải quyết dứt điểm các lỗi dấu phân cách thư mục (`/` vs `\\`), sai hỏng ký tự ngắt dòng (`CRLF` vs `LF`), xử lý ổ đĩa Windows (`C:`) và sự khác biệt về phân biệt hoa thường (Case-Sensitivity) giữa Windows và Linux.",
        "when_use": "- Khi script kiểm thử hoặc build chạy thành công trên máy tính Windows của lập trình viên nhưng bị sập trên máy chủ Linux của CI.\n- Khi Git liên tục báo toàn bộ các dòng trong file đều bị thay đổi do khác biệt ký tự ngắt dòng CRLF/LF.\n- Khi mã nguồn sử dụng phép nối chuỗi đường dẫn thủ công dạng `dir + \"/\" + file` gây lỗi trên Windows.",
        "when_not_use": "- Khi phần mềm được thiết kế độc quyền chỉ chạy trên duy nhất một hệ điều hành cụ thể (ví dụ: Windows Kernel Driver hoặc Linux Kernel Module).",
        "prereqs": "- **Ngữ cảnh đầu vào:** Mã nguồn đa nền tảng, file cấu hình `.gitattributes`, môi trường kiểm thử chạy cả Windows và Linux.\n- **Quyền hạn truy cập:** Quyền sửa đổi mã nguồn xử lý file I/O và cấu hình Git.",
        "concepts": "- **Path Normalization:** Sử dụng các thư viện chuẩn đa nền tảng (`pathlib` trong Python, `path` trong Node.js, `filepath` trong Go) thay vì tự nối chuỗi.\n- **Case Sensitivity Discrepancy:** Hệ thống tệp Linux phân biệt hoa thường (`File.txt` khác `file.txt`), trong khi Windows (NTFS) mặc định không phân biệt hoa thường.\n- **Git CRLF Normalization:** Cấu hình file `.gitattributes` để chuẩn hóa toàn bộ ký tự ngắt dòng về LF khi commit vào repository.",
        "workflow": "1. Khởi tạo file `.gitattributes` tại thư mục gốc với quy tắc `* text=auto eol=lf` để thống nhất ký tự ngắt dòng.\n2. Rà soát toàn bộ mã nguồn: thay thế các phép nối chuỗi đường dẫn bằng `pathlib.Path` hoặc `path.join()`.\n3. Quét phát hiện các file có tên trùng nhau nhưng khác nhau về chữ hoa chữ thường trong cùng một thư mục.\n4. Kiểm tra các đoạn mã bóc tách đường dẫn: đảm bảo xử lý an toàn cho cả định dạng Windows UNC (`\\\\server\\share`) và ký tự ổ đĩa (`C:`).\n5. Thiết lập ma trận kiểm thử CI chạy đồng thời trên cả hai hệ điều hành: `windows-latest` và `ubuntu-latest`.\n6. Xác thực toàn bộ các đường dẫn sinh ra trong các file log hoặc JSON đều sử dụng dấu gạch chéo chuẩn (`/`).",
        "examples": """### Xử lý đường dẫn chuẩn mực đa nền tảng trong Python và cấu hình .gitattributes:
```ini
# .gitattributes - Ep buoc chuan hoa ngat dong LF
* text=auto eol=lf
*.bat text eol=crlf
*.ps1 text eol=crlf
```

```python
# Chuan hoa duong dan an toan tren ca Windows va Linux
from pathlib import Path

def get_config_file_path(base_dir: str, filename: str) -> Path:
    # Su dung pathlib de tu dong xu ly dau phan cach theo he dieu hanh
    path = Path(base_dir).resolve() / filename
    
    # Chuyen doi sang duong dan tieu chuan dau gach cheo khi ghi log hoac JSON
    posix_path_str = path.as_posix()
    print(f"Duong dan tieu chuan: {posix_path_str}")
    return path
```""",
        "antipatterns": "- **Hardcoded Backslash or Slash:** Nối chuỗi đường dẫn cứng bằng `folder + \"\\\\\" + file` làm gãy hoàn toàn ứng dụng trên Linux.\n- **Ignoring Git Line Endings:** Không cấu hình `.gitattributes` dẫn tới việc các file shell script `.sh` bị lỗi ký tự `\\r` không chạy được trên Linux.\n- **Assuming Case-Insensitive Filesystems:** Đặt tên file là `UserCard.tsx` nhưng trong mã lệnh lại import `./usercard.tsx` (chạy được trên Windows nhưng sập trên Linux).",
        "gates": "- **QG-01**: 100% file văn bản trong kho mã nguồn được chuẩn hóa ngắt dòng LF thông qua `.gitattributes`.\n- **QG-04**: Test suite vượt qua 100% trên cả hai runner `windows-latest` và `ubuntu-latest` trong ma trận CI.\n- **QG-07**: Không có phép nối chuỗi đường dẫn thủ công nào còn sót lại trong codebase.",
        "security": "- Ngăn ngừa các lỗ hổng tấn công duyệt thư mục (Path Traversal) bằng cách sử dụng phương thức `resolve()` và kiểm tra tiền tố an toàn.",
        "adapters": "- **Runtimes**: Python `pathlib`, Node.js `path`, Go `path/filepath`, Rust `std::path::Path`.\n- **Tools**: dos2unix, gitattributes, ESLint import/no-unresolved.",
        "deliverables": "- File `.gitattributes` chuẩn hóa toàn bộ repository.\n- Bộ quy tắc linter phát hiện nối chuỗi đường dẫn không an toàn.\n- Ma trận kiểm thử CI đa nền tảng (Windows + Linux).",
        "related": "dex-developer-workstation-bootstrap, dex-reproducible-devcontainers, dex-cli-command-contracts",
        "usage": """```powershell
# Chuyển đổi toàn bộ ký tự ngắt dòng trong repo theo quy chuẩn gitattributes
git add --renormalize .

# Kiểm tra đường dẫn đa nền tảng bằng pytest
pytest tests/test_path_compatibility.py -v
```"""
    },
    {
        "id": "dex-package-publishing-preflight",
        "name": "dex-package-publishing-preflight",
        "desc": "Execute automated dry-runs, artifact inspection, README checks, licensing audits, and provenance attestations prior to publishing packages to npm, PyPI, Crates.io, or NuGet. Use when safeguarding open-source and internal package releases.",
        "purpose": "Thực thi quy trình kiểm tra tiền phát hành (Preflight Checks), đóng gói thử nghiệm (Dry-Run Packaging), kiểm tra nội dung artifact, tính đầy đủ của tài liệu, giấy phép bản quyền và chứng thực nguồn gốc (Provenance) trước khi xuất bản gói phần mềm lên npm, PyPI, Crates.io hoặc NuGet.",
        "when_use": "- Khi chuẩn bị xuất bản một phiên bản thư viện mã nguồn mở hoặc gói phần mềm nội bộ lên registry công cộng.\n- Khi muốn ngăn ngừa việc vô tình đóng gói các file rác, file test, hoặc khóa bí mật (`.env`) vào trong gói phát hành.\n- Khi triển khai quy trình xuất bản an toàn không cần token lưu trữ cố định (Provenance & OIDC Publishing).",
        "when_not_use": "- Khi chỉ xây dựng ứng dụng cuối (End-User Application) không có nhu cầu đóng gói thành thư viện để phân phối.",
        "prereqs": "- **Ngữ cảnh đầu vào:** Mã nguồn thư viện, file cấu hình xuất bản (`package.json`, `pyproject.toml`, `Cargo.toml`), tài khoản registry.\n- **Quyền hạn truy cập:** Quyền thực thi lệnh đóng gói và kiểm toán artifact cục bộ.",
        "concepts": "- **Package Dry-Run:** Lệnh đóng gói và mô phỏng tải lên registry mà không thực sự phát hành (`npm publish --dry-run`, `cargo publish --dry-run`).\n- **Tarball Inspection:** Giải nén và kiểm tra danh sách chính xác từng file sẽ được gửi tới người dùng cuối để loại trừ file nhạy cảm.\n- **Signed Attestation (SLSA):** Ký số chứng thực xuất xứ nguồn gốc trực tiếp từ pipeline GitHub Actions tới npm/PyPI.",
        "workflow": "1. Thực thi lệnh build và đóng gói thử nghiệm trong môi trường cô lập.\n2. Liệt kê toàn bộ danh sách các file nằm trong tarball thành phẩm.\n3. Quét phát hiện các file cấm: file cấu hình bí mật (`.env`, `.pem`), file kiểm thử nội bộ, tài liệu nháp.\n4. Kiểm tra sự hiện diện của các file bắt buộc: `LICENSE`, `README.md`, `CHANGELOG.md`.\n5. Xác minh tính hợp lệ của số phiên bản (Semantic Versioning) và bảo đảm chưa bị trùng lặp trên registry.\n6. Kiểm tra các liên kết tài liệu và metadata trong manifest trước khi cấp phép xuất bản chính thức.",
        "examples": """### Kiểm tra danh sách file đóng gói trước khi xuất bản npm / PyPI:
```powershell
# 1. Kiem tra danh sach file thuc te se duoc dong goi vao npm tarball
npm pack --dry-run

# 2. Dong goi va kiem tra do an toan bang Twine tren Python PyPI
python -m build
twine check dist/*

# 3. Kiem tra thu vien Rust truoc khi xuat ban len Crates.io
cargo publish --dry-run
```

```json
// package.json - Chi dinh ro rang cac file duoc phep xuat ban
{
  "name": "my-secure-lib",
  "version": "1.0.0",
  "files": [
    "dist",
    "README.md",
    "LICENSE"
  ]
}
```""",
        "antipatterns": "- **Publishing Without Whitelist:** Không khai báo trường `files` trong `package.json` khiến toàn bộ mã nguồn gốc, file test và cấu hình máy bị tải lên mạng.\n- **Leaking Secrets in Tarball:** Vô tình đóng gói file `.env.local` chứa API keys vào gói phát hành công khai.\n- **Skipping Build Verification:** Đóng gói mã nguồn mà quên chạy bước compile khiến người dùng tải về thư viện không có thư mục `dist`.",
        "gates": "- **QG-01**: Lệnh đóng gói dry-run chạy thành công 100% không có bất kỳ cảnh báo nào.\n- **QG-06**: Không có file chứa khóa bí mật, credentials hoặc file nháp nội bộ nào lọt vào tarball.\n- **QG-08**: 100% gói phát hành đều có giấy phép `LICENSE` hợp lệ và tài liệu hướng dẫn `README.md`.",
        "security": "- Sử dụng cơ chế xuất bản không khóa (Keyless OIDC Trusted Publishing) trên GitHub Actions thay vì lưu trữ static API token.",
        "adapters": "- **Tools**: npm pack, Twine, cargo publish, NuGet CLI, pub, pkg-pr-new.",
        "deliverables": "- Danh sách file cho phép đóng gói trong manifest.\n- Script kiểm tra tiền xuất bản (Preflight Audit Script).\n- Workflow xuất bản an toàn có gắn chứng chỉ xuất xứ.",
        "related": "dex-binary-provenance-matching, dex-toolchain-reproducibility-audit, dex-monorepo-template-conformance",
        "usage": """```powershell
# Chạy toàn bộ suite kiểm tra tiền phát hành
python scripts/release/preflight_check.py

# Kiểm tra tính toàn vẹn của package dist
twine check dist/*
```"""
    },
    {
        "id": "dex-monorepo-template-conformance",
        "name": "dex-monorepo-template-conformance",
        "desc": "Audit, enforce, and scaffold standardized directory structures, toolchain files, linting configs, and GitHub workflows across monorepo packages. Use when scaling multi-package repositories without architectural decay.",
        "purpose": "Kiểm toán, thực thi và khởi tạo cấu trúc thư mục chuẩn mực (Monorepo Template Conformance); chuẩn hóa các file cấu hình công cụ, quy tắc linter, kịch bản CI GitHub Actions và tài liệu giữa các gói package bên trong monorepo; ngăn ngừa sự suy thoái kiến trúc theo thời gian.",
        "when_use": "- Khi monorepo phát triển lên hàng chục hoặc hàng trăm packages và mỗi nhóm lại tự ý cấu hình một kiểu khác nhau.\n- Khi cần tạo nhanh một package mới (service, library, UI component) tuân thủ 100% tiêu chuẩn kỹ thuật của công ty.\n- Khi cập nhật cấu hình chung (tsconfig, eslint, license) và muốn tự động đồng bộ tới toàn bộ các packages.",
        "when_not_use": "- Khi dự án là một repository đơn lẻ độc lập không nằm trong kiến trúc monorepo đa gói.",
        "prereqs": "- **Ngữ cảnh đầu vào:** Monorepo chứa nhiều packages, bộ template mẫu chuẩn mực, công cụ scaffold (Plop, Turborepo generators, Manypkg).\n- **Quyền hạn truy cập:** Quyền sửa đổi cấu hình các gói package con trong monorepo.",
        "concepts": "- **Golden Template Pattern:** Gói mẫu tiêu chuẩn chứa đầy đủ cấu hình chuẩn mực nhất mà mọi gói mới đều phải tuân theo.\n- **Conformance Linter:** Công cụ tự động quét toàn bộ các package để phát hiện các file cấu hình bị thiếu, phiên bản thư viện dùng chung bị lệch, hoặc cấu trúc thư mục sai quy chuẩn.\n- **Dependency Synchronization:** Đảm bảo các packages bên trong monorepo luôn sử dụng cùng một phiên bản của các thư viện bên ngoài (ví dụ: tất cả cùng dùng `react@18.2.0`).",
        "workflow": "1. Xây dựng các mẫu khởi tạo chuẩn (Golden Templates) cho từng loại gói: UI Library, Node API Service, Python Worker, Go Microservice.\n2. Định nghĩa danh mục các file bắt buộc phải có trong mỗi package: `package.json`, `tsconfig.json`, `README.md`, `tests/`.\n3. Sử dụng công cụ `manypkg` hoặc script tùy biến để kiểm toán tính nhất quán của các trường manifest.\n4. Kế thừa các cấu hình gốc dùng chung (Shared Base Configs) thông qua cơ chế `extends`.\n5. Tích hợp lệnh kiểm tra tuân thủ cấu trúc vào pipeline CI: gắn cờ các package không tuân thủ.\n6. Cung cấp lệnh dòng lệnh tự động sửa lỗi (Auto-Fix) để đồng bộ hóa cấu hình toàn bộ monorepo chỉ bằng một thao tác.",
        "examples": """### Kiểm toán tính nhất quán của monorepo bằng manypkg và script Conformance:
```json
// packages/my-lib/tsconfig.json - Ke thua cau hinh chuan muc
{
  "extends": "../../tsconfig.base.json",
  "compilerOptions": {
    "outDir": "./dist",
    "rootDir": "./src"
  },
  "include": ["src/**/*"]
}
```

```powershell
# Chay kiem toan tinh nhat quan cua cac dependencies giua cac packages
npx @manypkg/cli check

# Tu dong dong bo phien ban thu vien dung chung bi sai lech
npx @manypkg/cli fix
```""",
        "antipatterns": "- **Copy-Paste Package Scaffolding:** Tạo package mới bằng cách sao chép nguyên vẹn một package cũ kèm theo các file rác và cấu hình lỗi thời.\n- **Fragmented Dependency Versions:** Package A dùng `lodash@4.17.20`, trong khi Package B dùng `lodash@4.17.21` làm tăng dung lượng bundle và gây lỗi khó lường.\n- **Standalone Unlinked Configs:** Tự viết các file `tsconfig` hoặc `eslint` riêng rẽ trong từng package mà không kế thừa từ cấu hình chuẩn dùng chung.",
        "gates": "- **QG-01**: 100% các packages trong monorepo tuân thủ đầy đủ cấu trúc thư mục quy định.\n- **QG-04**: Lệnh kiểm toán `manypkg check` không phát hiện bất kỳ sự sai lệch phiên bản thư viện dùng chung nào.\n- **QG-07**: Tất cả các package mới đều được tạo ra từ công cụ scaffold chuẩn.",
        "security": "- Đảm bảo các file cấu hình bảo mật (như chính sách quét phụ thuộc, linters) được áp dụng đồng bộ không có ngoại lệ.",
        "adapters": "- **Tools**: @manypkg/cli, Syncpack, Plop.js, Turborepo Generators, Nx Generators.",
        "deliverables": "- Bộ template chuẩn mực cho các loại package monorepo.\n- Công cụ tự động scaffold và kiểm toán tuân thủ cấu trúc.\n- Script kiểm tra và tự động đồng bộ hóa phiên bản thư viện dùng chung.",
        "related": "dex-polyglot-build-orchestration, dex-package-publishing-preflight, dex-toolchain-version-pinning",
        "usage": """```powershell
# Kiểm tra sự tuân thủ quy chuẩn của toàn bộ packages
npx syncpack list-mismatches

# Tạo một package mới tuân thủ 100% quy chuẩn
npx turbo gen workspace
```"""
    }
]

def generate_skills():
    total = len(SKILLS_AK_AL)
    created = 0
    print("=== GENERATING GROUP AK & AL (Skills 361–380) ===")

    for idx, skill in enumerate(SKILLS_AK_AL, 1):
        skill_id = skill["id"]
        skill_dir = os.path.join(SKILLS_DIR, skill_id)
        os.makedirs(skill_dir, exist_ok=True)
        file_path = os.path.join(skill_dir, "SKILL.md")

        content = f"""---
name: {skill["name"]}
description: {skill["desc"]}
---

# {skill["id"]}

## 1. Purpose & Scope
{skill["purpose"]}

## 2. When to Use
{skill["when_use"]}

## 3. When NOT to Use
{skill["when_not_use"]}

## 4. Prerequisites & Input Context
{skill["prereqs"]}

## 5. Core Concepts & Taxonomy
{skill["concepts"]}

## 6. Step-by-Step Execution Workflow
{skill["workflow"]}

## 7. Concrete Examples
{skill["examples"]}

## 8. Anti-Patterns & Common Traps
{skill["antipatterns"]}

## 9. Verification Quality Gates
{skill["gates"]}

## 10. Security & Risk Mitigation
{skill["security"]}

## 11. Platform Adapters & Extensibility
{skill["adapters"]}

## 12. Expected Deliverables
{skill["deliverables"]}

## 13. Related Skills & Synergy
{skill["related"]}

## 14. Realistic Usage Scenario & Verification Commands
{skill["usage"]}
"""
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        created += 1
        print(f"[{idx:02d}/{total:02d}] Created: {skill_id}")

    print(f"\nSuccessfully generated {created}/{total} skills for Groups AK & AL.")

if __name__ == "__main__":
    generate_skills()
