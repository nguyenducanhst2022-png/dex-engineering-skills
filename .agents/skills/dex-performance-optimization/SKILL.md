---
name: dex-performance-optimization
description: Metrics-driven software performance profiling, bottleneck detection, algorithmic optimization, and benchmark verification. Compares quantitative before-and-after metrics while preserving behavioral correctness. Use when diagnosing slow queries, reducing memory usage, optimizing latency, or profiling throughput.
---

# DEX Performance Optimization

## 1. Purpose & Scope
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

## 3. When NOT to Use
- Khi mã nguồn chưa chạy đúng logic hoặc đang có lỗi nghiêm trọng chưa được giải quyết.
- Tối ưu hóa vi mô sớm (Premature optimization) trên các hàm hiếm khi được thực thi và không tạo ra khác biệt đo lường được.

## 4. Prerequisites & Input Context
- Chỉ số hiệu năng hiện tại (Response time, p95/p99 latency, Memory heap, Throughput RPS).
- Công cụ profiling hoặc benchmark (ví dụ: `k6`, `autocannon`, `pytest-benchmark`, Chrome DevTools, Clinic.js).
- Đoạn mã nguồn hoặc truy vấn cơ sở dữ liệu bị nghi ngờ là nút cổ chai (Bottleneck).

## 5. Core Concepts & Taxonomy
- **Nguyên tắc cốt lõi**: Tuân thủ triệt để nguyên lý vận hành xác định và ranh giới trách nhiệm của chuẩn Agent Skills.
- **Tính nhất quán hệ thống**: Mọi thao tác phải có thể kiểm chứng độc lập với kết quả đo lường rõ ràng.
- **Ngăn ngừa hồi quy**: Bất kỳ sửa đổi nào cũng phải bảo vệ tính tương thích ngược và chất lượng đã được nghiệm thu.

## 6. Step-by-Step Execution Workflow
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

## 7. Concrete Examples
```bash
# Lệnh thực thi & kiểm chứng tiêu chuẩn
dex verify --skill dex-performance-optimization
```

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước xác minh tự động và dựa vào giả định chủ quan.
- **Anti-Pattern 2**: Thay đổi diện rộng vượt ngoài phạm vi (Scope Creep) làm mất kiểm soát rủi ro.
- **Trap**: Thực hiện thao tác phá hủy hoặc thay đổi trạng thái sản xuất khi chưa qua cổng kiểm duyệt an toàn.

## 9. Quality Gates & Acceptance Criteria
- **QG-02 (Functional Correctness)**: Kết quả tính toán trước và sau tối ưu phải hoàn toàn đồng nhất.
- **QG-05 (Tests PASS)**: 100% bài kiểm thử hồi quy tiếp tục đạt PASS.
- **QG-10 (Quantitative Benchmark Evidence)**: Có bảng số liệu Trước/Sau rõ ràng từ công cụ đo lường.

## 10. Security & Safety Boundaries
- **Không Tối Ưu Theo Linh Cảm**: Nghiêm cấm thay đổi cấu trúc mã nguồn nếu không có số liệu đo lường chứng minh nó là điểm nghẽn.
- **Không Đánh Đổi Bảo Mật Lấy Tốc Độ**: Tuyệt đối không tắt các bước validate dữ liệu hoặc mã hóa để làm code chạy nhanh hơn.
- **Kiểm Soát Bộ Nhớ Cache**: Khi dùng cache, bắt buộc phải có cơ chế giới hạn dung lượng (Max size) và thời gian hết hạn (TTL) để tránh Out-Of-Memory.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Kích hoạt thông qua terminal hoặc tiện ích mở rộng IDE tương thích (VS Code, Cursor, Windsurf).

## 12. Deliverables & Output Artifacts
1. Bảng số liệu đối chiếu Before vs. After Benchmark.
2. Mã nguồn sau khi được tối ưu hóa.
3. Bằng chứng kiểm thử hồi quy đạt 100% PASS.

## 13. Related & Complementary Skills
- `dex-master-orchestrator`: Điều phối trung tâm.

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Kỹ sư hoặc AI Agent kích hoạt **dex-performance-optimization** trong dự án.
1. Tiếp nhận ngữ cảnh đầu vào và kiểm tra điều kiện tiên quyết tại Mục 4.
2. Vận hành tuần tự các bước theo Quy trình tại Mục 6.
3. Kiểm chứng đầu ra đối chiếu với Tiêu chuẩn chấp thuận tại Mục 9.
4. Bàn giao đầy đủ hiện vật theo Mục 12 và cập nhật tài liệu liên quan.
