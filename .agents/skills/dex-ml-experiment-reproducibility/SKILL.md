---
name: dex-ml-experiment-reproducibility
description: Track, containerize, and audit ML experiments with deterministic seeds, data versioning (DVC), hardware profiles, and environment freezing. Use when institutionalizing reproducible machine learning research and engineering.
---

# dex-ml-experiment-reproducibility

## 1. Purpose & Scope
Theo dõi, container hóa và kiểm toán các thử nghiệm Machine Learning; bảo đảm khả năng tái lập kết quả thử nghiệm 100% nhờ cố định seed ngẫu nhiên, lập phiên bản dữ liệu (DVC/LakeFS), ghi nhận cấu hình phần cứng và đóng băng môi trường thư viện phụ thuộc.

## 2. When to Use
- Khi một kỹ sư rời nhóm và không ai có thể tái hiện lại kết quả mô hình mà họ đã công bố trước đây.
- Khi cần nộp tài liệu kiểm chứng kết quả mô hình cho các cơ quan quản lý (FDA, ngân hàng trung ương).
- Khi chuẩn hóa quy trình MLOps nhằm loại bỏ tình trạng 'chạy được trên máy của tôi'.

## 3. When NOT to Use
- Khi thực hiện viết mã khám phá nhanh ban đầu (Jupyter Notebook scratchpad) chỉ để kiểm tra ý tưởng trong vài phút.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Mã nguồn huấn luyện, dữ liệu huấn luyện, công cụ theo dõi thử nghiệm (MLflow, Weights & Biases, DVC).
- **Quyền hạn truy cập:** Quyền ghi vào máy chủ lưu trữ artifact và remote storage dữ liệu (S3/GCS).

## 5. Core Concepts & Taxonomy
- **Deterministic Seeding:** Thiết lập hạt giống ngẫu nhiên cố định cho tất cả các thư viện: Python random, NumPy, PyTorch (CPU và CUDA determinism).
- **Data Version Control (DVC):** Quản lý phiên bản các tập dữ liệu lớn bằng cách lưu mã băm siêu dữ liệu trong Git thay vì commit trực tiếp file nhị phân.
- **Environment Freezing:** Khóa cứng phiên bản các package bằng lockfiles (Poetry, Conda lock) và Docker container image digest.

## 6. Step-by-Step Execution Workflow
1. Cấu hình hàm thiết lập deterministic seed trên toàn bộ các runtime (Python, NumPy, PyTorch, TensorFlow).
2. Kích hoạt cờ thực thi tất định trên GPU (`torch.use_deterministic_algorithms(True)`).
3. Liên kết tập dữ liệu huấn luyện với mã băm Git commit thông qua DVC (`dvc.lock`).
4. Ghi nhận toàn bộ siêu dữ liệu: Git SHA, phiên bản CUDA, driver GPU, hyper-parameters vào MLflow/W&B.
5. Đóng gói môi trường thực thi vào Docker container có digest cố định.
6. Thực hiện huấn luyện độc lập trên hai máy khác nhau để xác minh tính nhất quán của trọng số mô hình cuối cùng.

## 7. Concrete Examples
### Hàm thiết lập môi trường hoàn toàn tất định trong PyTorch:
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
```

## 8. Anti-Patterns & Common Traps
- **Unseeded Data Shuffling:** Trộn ngẫu nhiên dữ liệu mà không truyền seed dẫn tới mỗi lần chạy sinh ra một tập train khác nhau.
- **Unpinned Python Packages:** Khai báo phụ thuộc `torch>=2.0` khiến bản cập nhật thư viện sau này làm thay đổi kết quả tính toán số thực.
- **Data Ingestion via Mutable URLs:** Tải dữ liệu từ một đường link web có thể bị thay đổi nội dung mà không kiểm tra mã băm SHA-256.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Mã nguồn, siêu tham số và phiên bản dữ liệu được liên kết 1-1 với commit Git SHA.
- **QG-04**: Hai lần huấn luyện với cùng seed sinh ra hàm mất mát (Loss) giống hệt nhau với sai số floating-point < 1e-6.
- **QG-08**: Môi trường huấn luyện chạy thành công từ container Docker độc lập không cần cài đặt thêm bên ngoài.

## 10. Security & Safety Boundaries
- Kiểm tra không ghi lại các thông tin bí mật (API keys, credentials) vào nhật ký tham số của công cụ tracking thử nghiệm.

## 11. Platform Adapters
- **Experiment Tracking**: MLflow, Weights & Biases, ClearML, Neptune.ai.
- **Data Versioning**: DVC, LakeFS, Pachyderm.

## 12. Deliverables & Output Artifacts
- Script huấn luyện tất định có thể tái lập.
- File `dvc.lock` và `poetry.lock` khóa cứng môi trường.
- Báo cáo đối chiếu kết quả giữa các lần chạy độc lập.

## 13. Related & Complementary Skills
dex-training-data-leakage-audit, dex-online-offline-feature-parity, dex-model-serving-canary-rollouts

## 14. Realistic Usage Example
```powershell
# Đồng bộ hóa phiên bản dữ liệu chính xác bằng DVC
dvc pull

# Chạy thử nghiệm có theo dõi đầy đủ qua MLflow
python train.py --seed 42 --config configs/production.yaml
```
