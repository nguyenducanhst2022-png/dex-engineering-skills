---
name: dex-batch-inference-pipeline-tuning
description: Optimize throughput, GPU memory allocation, dynamic batching, and distributed worker pipelines for large-scale offline batch inference. Use when scoring millions of records within strict operational windows.
---

# dex-batch-inference-pipeline-tuning

## 1. Purpose & Scope
Tối ưu hóa thông lượng (throughput), cấp phát bộ nhớ GPU, phân đoạn batch động và kiến trúc worker phân tán cho các pipeline suy luận theo lô (Batch Inference) quy mô lớn; bảo đảm hoàn thành tính toán hàng triệu bản ghi trong khung thời gian vận hành cho phép.

## 2. When to Use
- Khi cần chấm điểm tín dụng hoặc tính toán khuyến nghị cho 50 triệu người dùng mỗi đêm trong khung giờ 4 tiếng.
- Khi GPU chỉ hoạt động ở mức 20-30% công suất do bị nghẽn cổ chai tại khâu nạp và tiền xử lý dữ liệu (I/O Bottleneck).
- Khi gặp lỗi tràn bộ nhớ GPU (CUDA Out of Memory) khi xử lý các bản ghi có kích thước không đồng đều.

## 3. When NOT to Use
- Khi phục vụ API suy luận thời gian thực với yêu cầu độ trễ dưới 50ms cho từng request đơn lẻ vị trí biên.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Mô hình đã huấn luyện, kho dữ liệu đầu vào (Parquet trên S3/GCS), cụm máy chủ GPU/CPU.
- **Quyền hạn truy cập:** Quyền điều phối job tính toán phân tán (Ray, Spark, Kubernetes Jobs).

## 5. Core Concepts & Taxonomy
- **GPU Saturation vs. I/O Bottleneck:** Giữ cho GPU luôn được nạp đầy tensor tính toán bằng cơ chế bất đồng bộ nạp trước (Prefetching & Pin Memory).
- **Dynamic Bucket Batching:** Gom các bản ghi có độ dài tương đương vào cùng một batch để giảm thiểu lượng padding vô ích.
- **vLLM / TensorRT-LLM PagedAttention:** Tối ưu hóa phân mảnh bộ nhớ KV Cache khi chạy suy luận lô cho các mô hình ngôn ngữ lớn.

## 6. Step-by-Step Execution Workflow
1. Đo lường tỷ lệ tận dụng GPU (GPU Utilization) và thông lượng (records/sec) của pipeline hiện tại.
2. Triển khai cơ chế Multi-threaded / Async DataLoader với bộ đệm Prefetch để loại bỏ nghẽn I/O đọc đĩa.
3. Sắp xếp dữ liệu theo độ dài chuỗi và chia nhóm (bucket sorting) trước khi đưa vào batching để giảm lượng padding thừa.
4. Chuyển đổi mô hình sang định dạng tối ưu phần cứng (TensorRT, ONNX Runtime, FP16/BF16).
5. Phân bổ công việc phân tán qua nhiều GPU/Node sử dụng Ray Data hoặc PySpark ML.
6. Kiểm tra giám sát bộ nhớ GPU để bảo đảm không xảy ra hiện tượng tràn RAM (OOM) ở các batch đỉnh.

## 7. Concrete Examples
### Tối ưu hóa Batch Inference phân tán bằng Ray Data:
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
```

## 8. Anti-Patterns & Common Traps
- **Sequential Disk Reads in GPU Loop:** Đọc từng file ảnh hoặc text từ đĩa trong vòng lặp chính của GPU làm GPU phải chờ nhàn rỗi (idle).
- **Fixed Excessive Batch Size:** Đặt kích thước batch cố định quá lớn dẫn tới sập OOM khi gặp phải chuỗi văn bản dài đột biến.
- **Floating Point 32 on GPUs:** Chạy suy luận ở độ chính xác FP32 thay vì FP16 hoặc INT8 làm giảm một nửa thông lượng tính toán khả thi.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Tỷ lệ tận dụng GPU (GPU Core Utilization) duy trì ổn định >= 85% trong suốt quá trình chạy.
- **QG-04**: Tốc độ thông lượng suy luận tăng tối thiểu 3x so với cấu hình mặc định ban đầu.
- **QG-07**: 0% lỗi CUDA Out of Memory xảy ra trên toàn bộ tập dữ liệu kiểm thử.

## 10. Security & Safety Boundaries
- Mã hóa dữ liệu tạm thời (Scratch disks) trên các worker node trong quá trình xử lý lô dữ liệu nhạy cảm.

## 11. Platform Adapters
- **Engines**: Ray Data, PySpark, TensorRT, vLLM, ONNX Runtime, DeepSpeed-Inference.

## 12. Deliverables & Output Artifacts
- Pipeline suy luận theo lô phân tán tối ưu hóa phần cứng.
- Cấu hình Dynamic Batching và bucket sorter.
- Báo cáo benchmark thông lượng và chi phí tính toán trên mỗi triệu bản ghi.

## 13. Related & Complementary Skills
dex-model-serving-canary-rollouts, dex-vector-embedding-migration, dex-inference-provider-rate-controls

## 14. Realistic Usage Example
```powershell
# Chạy job Ray phân tán phục vụ suy luận lô
ray job submit --address="http://ray-head:8265" -- python batch_inference.py

# Giám sát thông lượng và tải GPU bằng nvidia-smi
nvidia-smi --query-gpu=utilization.gpu,memory.used,memory.total --format=csv -l 1
```
