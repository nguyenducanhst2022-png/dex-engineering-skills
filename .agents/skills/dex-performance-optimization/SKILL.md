---
name: dex-performance-optimization
description: Metrics-driven software performance profiling, bottleneck detection, algorithmic optimization, and benchmark verification. Compares quantitative before-and-after metrics while preserving behavioral correctness. Use when diagnosing slow queries, reducing memory usage, optimizing latency, or profiling throughput.
---

# DEX Performance Optimization

## 1. Purpose
Tối ưu hóa hiệu năng phần mềm (tốc độ xử lý, thời gian phản hồi, mức tiêu thụ CPU và bộ nhớ) dựa trên số liệu đo lường định lượng thực tế, đảm bảo không đánh đổi tính đúng đắn và độ ổn định của hệ thống.

Quy trình tối ưu chuẩn:
`Đo hiệu năng → Tìm điểm nghẽn → Phân tích → Tối ưu → Đo lại → Kiểm tra hồi quy → Ổn định → Lưu Git`

Nguyên tắc cốt lõi: **Không tối ưu theo cảm tính. Bắt buộc phải có số liệu benchmark trước và sau để chứng minh sự cải thiện.**
Ghi nhớ sống còn: **Tối ưu tốt = Nhanh hơn + Ít tài nguyên hơn + Không giảm tính đúng đắn và độ ổn định.**

## 2. When to Use
- Khi hệ thống có thời gian phản hồi API chậm (High latency) hoặc vượt ngưỡng SLA cho phép.
- Khi xuất hiện tình trạng rò rỉ bộ nhớ (Memory leak) hoặc CPU duy trì ở mức 100% bất thường.
- Khi cơ sở dữ liệu gặp vấn đề N+1 queries hoặc quét toàn bộ bảng (Full table scan).
- Khi chuẩn bị hệ thống chịu tải lớn cho các đợt cao điểm (Peak traffic).

## 3. When Not to Use
- Khi mã nguồn chưa chạy đúng logic hoặc đang có lỗi nghiêm trọng chưa được giải quyết.
- Tối ưu hóa vi mô sớm (Premature optimization) trên các hàm hiếm khi được thực thi và không tạo ra khác biệt đo lường được.

## 4. Inputs
- Chỉ số hiệu năng hiện tại (Response time, p95/p99 latency, Memory heap, Throughput RPS).
- Công cụ profiling hoặc benchmark (ví dụ: `k6`, `autocannon`, `pytest-benchmark`, Chrome DevTools, Clinic.js).
- Đoạn mã nguồn hoặc truy vấn cơ sở dữ liệu bị nghi ngờ là nút cổ chai (Bottleneck).

## 5. Workflow

### Bước 1: Đo Lường Hiện Trạng (Baseline Measurement)
- Thiết lập kịch bản benchmark có khả năng lặp lại độc lập.
- Chạy đo đạc và ghi nhận số liệu cơ sở (Baseline Metrics) trước khi chạm vào bất kỳ dòng code nào:
  - Latency: p50, p95, p99.
  - Throughput: Requests per second.
  - Memory: RSS / Heap used.

### Bước 2: Định Vị Điểm Nghẽn (Bottleneck Identification)
- Sử dụng Profiler để phân tích Flamegraph:
  - Điểm nghẽn nằm ở CPU (thuật toán O(N^2), vòng lặp lồng nhau)?
  - Điểm nghẽn nằm ở I/O (chờ database, gọi HTTP tuần tự, đọc ghi file chậm)?
  - Điểm nghẽn nằm ở Garbage Collection / Memory allocation?

### Bước 3: Phân Tích & Chọn Giải Pháp Tối Ưu (Optimization Strategy)
- Chọn giải pháp có tác động lớn nhất với độ phức tạp tối thiểu:
  - Chuyển tuần tự sang song song (`Promise.all` / Concurrent workers).
  - Bổ sung Caching (In-memory LRU, Redis) cho các phép tính lặp lại hoặc dữ liệu ít thay đổi.
  - Tối ưu hóa truy vấn DB (đánh Index, loại bỏ N+1 query, chỉ SELECT cột cần dùng).
  - Tối ưu hóa cấu trúc dữ liệu và độ phức tạp thuật toán (từ O(N) sang O(1) dùng Map/Set).

### Bước 4: Triển Khai Tối Ưu Hóa (Targeted Refinement)
- Chỉnh sửa mã nguồn tập trung chính xác vào điểm nghẽn đã xác định.
- Giữ mã nguồn trong sáng, dễ hiểu, tránh các mẹo (micro-hacks) làm giảm tính bảo trì.

### Bước 5: Đo Lường Lại & So Sánh (Re-Benchmark & Verification)
- Chạy lại kịch bản benchmark ban đầu với cùng điều kiện môi trường và dữ liệu.
- Đối chiếu số liệu: Chứng minh rõ tỷ lệ phần trăm cải thiện (ví dụ: Latency giảm 65%, RAM giảm 40%).

### Bước 6: Kiểm Tra Hồi Quy Chức Năng (Functional Regression Check)
- Chạy toàn bộ bộ test chức năng để đảm bảo tối ưu hiệu năng không làm sai lệch kết quả nghiệp vụ.

### Bước 7: Ổn Định & Lưu Git (Stabilization & Commit)
- Ghi commit kèm số liệu đo lường: `perf(cache): reduce user profile response time from 420ms to 85ms`.

## 6. Quality Gates
- **QG-02 (Functional Correctness)**: Kết quả tính toán trước và sau tối ưu phải hoàn toàn đồng nhất.
- **QG-05 (Tests PASS)**: 100% bài kiểm thử hồi quy tiếp tục đạt PASS.
- **QG-10 (Quantitative Benchmark Evidence)**: Có bảng số liệu Trước/Sau rõ ràng từ công cụ đo lường.

## 7. Safety Rules
- **Không Tối Ưu Theo Linh Cảm**: Nghiêm cấm thay đổi cấu trúc mã nguồn nếu không có số liệu đo lường chứng minh nó là điểm nghẽn.
- **Không Đánh Đổi Bảo Mật Lấy Tốc Độ**: Tuyệt đối không tắt các bước validate dữ liệu hoặc mã hóa để làm code chạy nhanh hơn.
- **Kiểm Soát Bộ Nhớ Cache**: Khi dùng cache, bắt buộc phải có cơ chế giới hạn dung lượng (Max size) và thời gian hết hạn (TTL) để tránh Out-Of-Memory.

## 8. Expected Outputs
1. Bảng số liệu đối chiếu Before vs. After Benchmark.
2. Mã nguồn sau khi được tối ưu hóa.
3. Bằng chứng kiểm thử hồi quy đạt 100% PASS.

## 9. Failure Handling
- Nếu sau khi tối ưu mà số liệu không cải thiện hoặc code trở nên quá phức tạp, khó hiểu: Hoàn tác lại code cũ ngay lập tức và tìm kiếm giải pháp ở tầng kiến trúc hoặc database.

## 10. Completion Criteria
- Số liệu hiệu năng đo lường đạt mục tiêu đề ra (hoặc cải thiện rõ rệt có thể đo đếm).
- Toàn bộ bài kiểm thử chức năng đạt PASS. Không phát sinh rò rỉ tài nguyên.

---

## Real-world Example
Endpoint `/api/users/:id/orders` mất trung bình 850ms để tải 20 đơn hàng vì gặp lỗi N+1 queries.
- *Baseline*: `autocannon -c 10 -d 5s` → Latency p95: 850ms, 12 req/sec.
- *Điểm nghẽn*: Mỗi đơn hàng lại chạy thêm 1 câu query lấy thông tin sản phẩm (20 queries lẻ).
- *Tối ưu*: Sử dụng `JOIN` hoặc eager loading `include: ['items']` trong ORM để lấy tất cả trong 1 query duy nhất.
- *Re-benchmark*: Latency p95 giảm xuống còn 48ms (nhanh gấp 17 lần), đạt 210 req/sec.
- *Hồi quy*: Chạy 8 unit tests của Order module → PASS 100%.
