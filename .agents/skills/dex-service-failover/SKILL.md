---
name: dex-service-failover
description: Architect, configure, and validate automated service failover, multi-region routing, health-checking protocols, and circuit breakers (Envoy, Resilience4j). Use when engineering high-availability fault-tolerant services.
---

# dex-service-failover

## 1. Purpose & Scope
Thiết kế, cấu hình và kiểm chứng cơ chế chuyển đổi dự phòng tự động (Automated Failover), định tuyến đa vùng (Multi-region Routing), giao thức kiểm tra sức khỏe sâu (Deep Health Checks) và ngắt mạch (Circuit Breakers) nhằm bảo đảm dịch vụ duy trì hoạt động liên tục khi các cụm máy chủ hoặc vùng điện toán gặp sự cố nghiêm trọng.

## 2. When to Use
- Dịch vụ yêu cầu độ sẵn sàng cao (High Availability 99.99% - Four Nines).
- Chuẩn bị kế hoạch khôi phục sau thảm họa (Disaster Recovery - DR) cho datacenter/cloud region.
- Tránh tình trạng dịch vụ chết chìm khi phụ thuộc vào một nhà cung cấp bên thứ ba đang bị lỗi.

## 3. When NOT to Use
- Không cấu hình failover tự động cho các cơ sở dữ liệu Master-Slave nếu cơ chế chống phân rã não (Split-Brain) chưa được chứng minh an toàn.
- Không dùng Circuit Breaker cho các thao tác nội bộ siêu nhanh in-memory.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Kiến trúc phân bổ dịch vụ (Active-Active hoặc Active-Passive).
- Các ngưỡng phát hiện lỗi (Failure thresholds: số lần lỗi liên tiếp, timeout limit).
- Công cụ cân bằng tải và Service Mesh (Envoy, AWS Route53, Cloudflare, Resilience4j).
- **Điều kiện tiên quyết**:
- Có ít nhất 2 phiên bản độc lập của dịch vụ được triển khai ở 2 vùng/cụm máy chủ tách biệt.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Circuit Breaker States: `CLOSED` (bình thường) -> `OPEN` (ngắt mạch, fail-fast lập tức để downstream hồi phục) -> `HALF-OPEN` (thử nghiệm gửi vài request để kiểm tra sức khỏe).
- Split-Brain Prevention: Trong kiến trúc đa vùng, phải có cơ chế quorum (bầu chọn quá bán) để tránh 2 master cùng ghi dữ liệu gây hỏng database.
- Deep vs Shallow Health Check: Shallow chỉ kiểm tra process sống (HTTP 200), Deep kiểm tra cả khả năng kết nối DB và bộ nhớ.
- **Quy tắc quyết định kỹ thuật**:
- Nếu tỉ lệ lỗi của endpoint > 50% trong 10 giây: chuyển Circuit Breaker sang trạng thái `OPEN` và trả về fallback data.
- Chỉ kích hoạt chuyển vùng (Region Failover) khi mất kết nối hoàn toàn trên 3 kỳ health check liên tiếp (chống flap do mạng chập chờn ngắn hạn).
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Failover Thundering Herd: Khi Region A bị lỗi, toàn bộ traffic đổ dồn đột ngột sang Region B làm Region B cũng quá tải và sập theo (hiệu ứng domino).

## 6. Step-by-Step Execution Workflow
1. Thiết lập endpoint `/healthz` (liveness) và `/ready` (readiness) chuẩn hóa.
2. Cấu hình Circuit Breaker cho các lời gọi remote service với timeout và fallback rõ ràng.
3. Thiết lập DNS Health Check với TTL ngắn (30-60 giây) để chuyển hướng traffic nhanh khi cần.
4. Thực hiện diễn tập ngắt kết nối đột ngột của Region chính (Chaos drill).
5. Xác minh thời gian chuyển đổi (RTO) và tỉ lệ mất mát dữ liệu (RPO).

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```yaml
# Cấu hình Envoy Circuit Breakers
circuit_breakers:
  thresholds:
    - priority: DEFAULT
      max_connections: 1000
      max_pending_requests: 100
      max_requests: 1000
      max_retries: 3
outlier_detection:
  consecutive_5xx: 3
  interval: 10s
  base_ejection_time: 30s
  max_ejection_percent: 50
```

### Lệnh xác minh & thực thi:
```bash
# Giả lập ngắt kết nối để kiểm tra Circuit Breaker nhảy sang OPEN
for i in {1..20}; do curl -s -w "%{http_code}\n" http://localhost:8080/api/v1/external-data; done
```

## 8. Anti-Patterns & Common Traps
- Cấu hình retry vô hạn với fixed delay làm dịch vụ downstream vừa phục hồi đã bị đè bẹp trở lại (phải dùng Exponential Backoff với Jitter).
- Đặt Health Check kiểm tra quá nặng (ví dụ: quét toàn bộ bảng DB) khiến bản thân health check làm sập DB.

## 9. Quality Gates & Acceptance Criteria
- Thời gian phát hiện lỗi và chuyển đổi sang instance dự phòng dưới 30 giây mà không cần con người can thiệp.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Đảm bảo dữ liệu đồng bộ sang cụm dự phòng được mã hóa trên đường truyền (mTLS) và tại đích (Encryption at rest).
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ thống hỗ trợ**: Linux (CI/CD runners), macOS, Windows 11 PowerShell/WSL2.

## 12. Deliverables & Output Artifacts
- File cấu hình Envoy / Resilience4j / Route53 Failover.
- Biên bản diễn tập kiểm tra chuyển đổi dự phòng.

## 13. Related & Complementary Skills
dex-distributed-consistency, dex-traffic-shaping-backpressure, dex-operational-game-days

## 14. Realistic Usage Example
### Tình huống thực tế:
Dịch vụ cổng thanh toán tích hợp ngân hàng ngoài thường xuyên bị treo khiến các worker bị khóa hết luồng. Nhóm tích hợp Circuit Breaker với Resilience4j. Khi ngân hàng ngoài bị lỗi quá 5 lần liên tiếp, hệ thống lập tức mở mạch, trả về thông báo 'Ngân hàng đang bảo trì' trong 0.1ms và tự động thử lại sau 60 giây, bảo vệ ứng dụng chính chạy trơn tru.
