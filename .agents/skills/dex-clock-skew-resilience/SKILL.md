---
name: dex-clock-skew-resilience
description: Engineer distributed systems resilient to physical clock skew, leap seconds, and NTP drift using monotonic clocks, logical Lamport timestamps, and bounded lease timeouts. Use when ordering events across independent server nodes.
---

# dex-clock-skew-resilience

## 1. Purpose & Scope
Thiết kế hệ thống phân tán có khả năng kháng cự trước sai lệch đồng hồ vật lý (Physical Clock Skew, NTP Drift, Leap Seconds); loại bỏ sự phụ thuộc nguy hiểm vào đồng hồ thực tế (Wall-Clock Time), ứng dụng đồng hồ đơn điệu (Monotonic Clocks), thời gian logic (Logical Lamport Timestamps / Vector Clocks), và khoảng dung sai thời gian an toàn.

## 2. When to Use
- Khi sắp xếp thứ tự các sự kiện phát sinh từ nhiều máy chủ độc lập không có đồng hồ đồng bộ tuyệt đối.
- Khi triển khai thuật toán phát hiện xung đột dữ liệu (Last-Write-Wins / Conflict-Free Replicated Data Types - CRDTs).
- Khi thiết lập thời hạn hết hạn token, session hoặc lease khóa phân tán trên môi trường máy chủ đám mây ảo hóa.

## 3. When NOT to Use
- Khi chỉ hiển thị ngày giờ thân thiện cho người dùng trên giao diện frontend.
- Khi hệ thống vận hành trên hạ tầng phần cứng chuyên dụng có đồng hồ nguyên tử và GPS hỗ trợ TrueTime API (như Google Cloud Spanner).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Sai số NTP đo được giữa các nodes trong cluster, cơ chế sinh timestamp hiện tại, yêu cầu về thứ tự sự kiện (Causal Ordering vs Total Ordering).
- **Quyền hạn truy cập:** Quyền kiểm tra cấu hình NTP daemon (`chrony` hoặc `ntpd`) trên máy chủ.

## 5. Core Concepts & Taxonomy
- **Wall-Clock vs Monotonic Clock:** Đồng hồ thực tế (ví dụ: `time.time()` trong Python) có thể bị nhảy lùi lại khi NTP đồng bộ; đồng hồ đơn điệu (ví dụ: `time.monotonic()`) luôn chỉ tăng và không bao giờ lùi.
- **Lamport Logical Timestamp:** Mỗi tiến trình duy trì một số nguyên đơn giản; khi gửi tin đính kèm counter, khi nhận tin cập nhật counter = $\max(\text{local}, \text{received}) + 1$.
- **Clock Uncertainty Window ($\epsilon$):** Khoảng thời gian không chắc chắn $[	ext{timestamp} - \epsilon, 	ext{timestamp} + \epsilon]$ cần được tính đến khi thiết lập các thời hạn an toàn.

## 6. Step-by-Step Execution Workflow
1. Rà soát toàn bộ mã nguồn: thay thế tất cả các phép đo khoảng thời gian (duration) từ đồng hồ thực sang đồng hồ đơn điệu (`time.monotonic()` hoặc `System.nanoTime()`).
2. Thay thế cơ chế so sánh thứ tự sự kiện dựa trên wall-clock bằng Lamport Timestamp hoặc Vector Clocks cho các luồng nghiệp vụ yêu cầu quan hệ nhân quả (Causal Consistency).
3. Trong các giao dịch khóa phân tán: cộng thêm khoảng dung sai sai lệch tối đa ($\Delta_{\text{clock}}$ ví dụ: 200ms) vào thời gian giữ khóa để bảo đảm khóa cũ đã hết hạn ở mọi node trước khi cấp khóa mới.
4. Giám sát độ lệch NTP giữa các nodes trong cluster qua Prometheus node_exporter và cảnh báo khi offset vượt quá 50ms.
5. Kiểm thử hệ thống trong kịch bản giả lập đồng hồ máy chủ bị chỉnh lùi hoặc tiến 5 giây để chứng minh không xảy ra deadlock hoặc hỏng dữ liệu.

## 7. Concrete Examples
### Ví dụ bộ đếm Lamport Timestamp bảo đảm thứ tự nhân quả trong TypeScript:
```typescript
export class LamportClock {
  private counter: number = 0;

  // Lấy thời gian logic để gửi kèm thông điệp đi
  tick(): number {
    this.counter += 1;
    return this.counter;
  }

  // Cập nhật thời gian logic khi nhận được thông điệp từ node khác
  witness(receivedTimestamp: number): number {
    this.counter = Math.max(this.counter, receivedTimestamp) + 1;
    return this.counter;
  }

  getValue(): number {
    return this.counter;
  }
}

// Khi áp dụng: Sự kiện có Lamport Timestamp lớn hơn được bảo đảm xảy ra sau
// mà hoàn toàn không phụ thuộc vào đồng hồ giờ máy tính của hai bên!
```

## 8. Anti-Patterns & Common Traps
- **Measuring Durations with Date.now():** Đo thời gian thực thi bằng cách lấy `Date.now() - startTime`, dẫn tới kết quả bị âm khi NTP đồng bộ lùi giờ.
- **Blind Last-Write-Wins (LWW):** Giải quyết xung đột dữ liệu bằng cách so sánh `created_at` từ đồng hồ máy tính của hai server khác nhau, khiến server chạy nhanh hơn luôn ghi đè dữ liệu của server chạy chậm hơn.
- **Leap Second Ignorance:** Không cấu hình NTP Slewing (chrony) khiến bước nhảy 1 giây nhuận (Leap Second) làm sập các ứng dụng cơ sở dữ liệu phân tán.

## 9. Quality Gates & Acceptance Criteria
- **QG-05**: 100% các phép đo khoảng thời gian trong mã nguồn sử dụng Monotonic Clock.
- **QG-09**: Xung đột dữ liệu được giải quyết chính xác bằng Lamport/Vector Clocks hoặc CRDTs trong bài test mô phỏng đồng hồ lệch 10 giây.
- **QG-10**: Cảnh báo NTP drift được kích hoạt ngay lập tức khi độ lệch đồng hồ giữa 2 nodes bất kỳ vượt quá 50ms.

## 10. Security & Safety Boundaries
- Bắt buộc sử dụng giao thức NTP an toàn (NTS - Network Time Security) để chống lại các cuộc tấn công giả mạo thời gian (Time Shifting Attack) nhằm làm hết hạn sớm chứng chỉ SSL hoặc token bảo mật.
- Kiểm soát cấu hình tường lửa chỉ cho phép đồng bộ thời gian từ các NTP servers uy tín.

## 11. Platform Adapters
- **System**: `chrony`, `ntpd`, `node_exporter` (metric `node_timex_offset_seconds`).
- **Libraries**: HLC (Hybrid Logical Clocks), Google TrueTime API.

## 12. Deliverables & Output Artifacts
- Module thư viện Lamport Timestamp và Monotonic Timer.
- Quy tắc cấu hình chrony slewing chuẩn hóa cho cụm máy chủ.
- Bộ kiểm thử tự động kiểm tra khả năng kháng sai lệch đồng hồ (Clock Skew Chaos Test).

## 13. Related & Complementary Skills
dex-distributed-lock-lease-safety, dex-distributed-consistency, dex-scheduler-misfire-recovery

## 14. Realistic Usage Example
```powershell
# Chạy bộ kiểm thử kiểm tra tính ổn định của hệ thống khi đồng hồ bị lệch
pytest tests/distributed/test_clock_skew_resilience.py -v
```
