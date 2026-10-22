---
name: dex-traffic-shaping-backpressure
description: Implement traffic shaping, backpressure mechanisms, leaky/token buckets, priority queues, and load-shedding to prevent cascading failures under extreme load. Use when distributed services face traffic surges.
---

# dex-traffic-shaping-backpressure

## 1. Purpose & Scope
Thiết kế và triển khai các cơ chế điều tiết lưu lượng (Traffic Shaping), kiểm soát áp lực ngược (Backpressure), cắt giảm tải có chọn lọc (Load Shedding) và hàng đợi ưu tiên (Priority Queuing) nhằm bảo vệ dịch vụ hạ tầng không bị quá tải sụp đổ dây chuyền (cascading failure) khi gặp cơn sóng dữ liệu đột biến.

## 2. When to Use
- Dịch vụ downstream xử lý chậm hơn tốc độ đẩy dữ liệu vào của upstream, khiến hàng đợi (Queue) phình to vô hạn và tràn bộ nhớ OOM.
- Hệ thống đối mặt với traffic đột biến gấp 10 lần bình thường.
- Cần ưu tiên các request thanh toán quan trọng hơn các request xem ảnh/thông tin phụ.

## 3. When NOT to Use
- Không áp dụng backpressure nếu hệ thống chỉ cần mở rộng tài nguyên tính toán (Horizontal Pod Autoscaling) đơn giản.
- Không làm rớt các request của khách hàng nếu downstream service chưa thực sự cạn kiệt tài nguyên.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Giới hạn tài nguyên của dịch vụ (CPU, RAM, Maximum In-flight Requests).
- Phân loại độ ưu tiên của các luồng nghiệp vụ (Critical vs Non-critical).
- Cấu hình hàng đợi (RabbitMQ, Kafka, Async Channel).
- **Điều kiện tiên quyết**:
- Kiến trúc hệ thống cho phép phản hồi mã trạng thái 429 (Too Many Requests) hoặc 503 (Service Unavailable) khi quá tải.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Backpressure: Tín hiệu phản hồi từ downstream yêu cầu upstream chậm lại hoặc tạm dừng gửi tin.
- Load Shedding: Chủ động từ chối nhanh (fail-fast) các request có độ ưu tiên thấp để giữ cho các request cốt lõi vẫn hoàn thành đúng hạn.
- CoDel / Bounded Queues: Không bao giờ sử dụng hàng đợi không giới hạn (unbounded queue) vì sẽ dẫn đến OOM crash.
- **Quy tắc quyết định kỹ thuật**:
- Nếu độ trễ xếp hàng (Queue Waiting Time) vượt quá timeout của client: drop request ngay tại đầu vào thay vì tiếp tục xử lý vô ích.
- Nếu CPU dịch vụ > 85%: kích hoạt chế độ load-shedding đối với các API phụ (recommendations, analytics).
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Xử lý tất cả các request đến cùng một lúc khiến toàn bộ hệ thống bị treo, dẫn đến 100% người dùng đều bị timeout thay vì 90% thành công và 10% bị từ chối lịch sự.

## 6. Step-by-Step Execution Workflow
1. Xác định năng lực xử lý tối đa an toàn (Concurrency Limit) của service.
2. Cấu hình giới hạn kích thước hàng đợi (Bounded Queue capacity).
3. Tích hợp thuật toán điều tiết tải (ví dụ: Little's Law, CoDel hoặc Netflix Concurrency Limits).
4. Thiết lập cờ phân loại độ ưu tiên cho các request (Header `X-Priority: High`).
5. Kiểm thử giả lập quá tải để chứng minh dịch vụ không bị sập và tự phục hồi khi tải giảm.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```go
// Giới hạn số lượng request đồng thời bằng buffered channel semaphore
type BoundedLimiter struct {
    sem chan struct{}
}

func NewBoundedLimiter(maxConcurrent int) *BoundedLimiter {
    return &BoundedLimiter{sem: make(chan struct{}, maxConcurrent)}
}

func (l *BoundedLimiter) Execute(w http.ResponseWriter, r *http.Request, handler http.HandlerFunc) {
    select {
    case l.sem <- struct{}{}:
        defer func() { <-l.sem }()
        handler(w, r)
    default:
        // Drop tải ngay lập tức nếu hàng đợi đầy (Load Shedding)
        http.Error(w, "Server Busy - Try again later", http.StatusServiceUnavailable)
    }
}
```

### Lệnh xác minh & thực thi:
```bash
# Bắn spike test để kiểm tra load-shedding trả về 503 thay vì sập service
k6 run --vus 2000 --duration 30s scripts/spike-test.js
```

## 8. Anti-Patterns & Common Traps
- Dùng hàng đợi không giới hạn (Unbounded Queue) trong bộ nhớ dẫn đến sập container do OOMKilled.
- Tiếp tục xử lý request sau khi client đã disconnect hoặc hủy kết nối.

## 9. Quality Gates & Acceptance Criteria
- Dịch vụ vẫn duy trì P95 latency ổn định cho 80% request ưu tiên khi tổng traffic vượt 300% tải thiết kế.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Cơ chế load shedding không được làm rò rỉ thông tin kiến trúc nội bộ trong thông báo lỗi trả về client.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ thống hỗ trợ**: Linux (CI/CD runners), macOS, Windows 11 PowerShell/WSL2.

## 12. Deliverables & Output Artifacts
- Middleware điều tiết backpressure và load-shedding.
- Dashboard Grafana giám sát tỉ lệ shed requests và queue depth.

## 13. Related & Complementary Skills
dex-load-and-stress-testing, dex-rate-limiting-quotas, dex-service-failover

## 14. Realistic Usage Example
### Tình huống thực tế:
Một dịch vụ streaming video bị sập mỗi khi có trận bóng đá trực tiếp do hàng triệu người kết nối cùng lúc. Sau khi triển khai Adaptive Concurrency Limiting, dịch vụ tự động drop các request load comment và gợi ý phim, bảo vệ luồng phát video trực tiếp cho 98% khán giả không bị giật lag.
