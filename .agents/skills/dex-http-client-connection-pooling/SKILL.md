---
name: dex-http-client-connection-pooling
description: Benchmark and optimize HTTP client connection pools, socket reuse, keep-alive lifecycles, and DNS caching across high-throughput microservice communication. Use when diagnosing socket exhaustion, connection timeouts, or high P99 latencies in distributed systems.
---

# dex-http-client-connection-pooling

## 1. Purpose & Scope
Đo lường chuẩn đối sánh (Benchmarking) và tối ưu hóa hồ chứa kết nối máy khách HTTP (HTTP Client Connection Pooling); tối ưu hóa việc tái sử dụng socket, vòng đời kết nối Keep-Alive, bộ nhớ đệm phân giải tên miền (DNS Caching) và giới hạn kết nối đồng thời; phục vụ xử lý triệt để hiện tượng cạn kiệt cổng mạng (Socket Exhaustion) và độ trễ đuôi P99 cao trong giao tiếp giữa các vi dịch vụ.

## 2. When to Use
- Khi máy chủ backend phát sinh lỗi `EADDRNOTAVAIL` hoặc `Connection timed out` dưới tải cao.
- Khi độ trễ gọi API nội bộ giữa các microservices bị chậm bất thường do liên tục phải thiết lập lại bắt tay TCP/TLS.
- Khi xây dựng các API Gateway hoặc Web Proxy xử lý hàng chục nghìn request mỗi giây.

## 3. When NOT to Use
- Khi ứng dụng chỉ gửi một vài request HTTP đơn lẻ mỗi ngày.
- Khi giao tiếp nội bộ đã chuyển hoàn toàn sang kết nối dài hạn qua gRPC/HTTP2 multiplexing.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Môi trường Node.js (Undici, Axios/AgentKeepAlive) hoặc Go/Java, công cụ kiểm thử tải (k6 hoặc autocannon).
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; tuân thủ nghiêm ngặt các ranh giới bảo mật và an toàn dữ liệu.

## 5. Core Concepts & Taxonomy
- **Keep-Alive Reuse:** Duy trì kết nối TCP mở sau khi hoàn thành request để các request tiếp theo dùng lại mà không tốn 3 lượt bắt tay TCP và TLS handshake.
- **Socket Exhaustion (TIME_WAIT):** Khi đóng kết nối TCP liên tục, cổng mạng bị giữ ở trạng thái TIME_WAIT trong 60 giây, làm cạn kiệt dải cổng tạm thời (Ephemeral Ports).
- **DNS TTL Cache:** Bộ nhớ đệm phân giải IP của domain để tránh phải gửi truy vấn DNS UDP lặp lại cho mỗi request.

## 6. Step-by-Step Execution Workflow
1. Đo lường số lượng kết nối ở trạng thái TIME_WAIT và TIME_CLOSE bằng lệnh `netstat -an`.
2. Cấu hình HTTP Agent với các tham số `keepAlive: true`, `maxSockets: 256`, `keepAliveMsecs: 60000`.
3. Bật bộ nhớ đệm phân giải DNS nội bộ trong ứng dụng với thời gian TTL hợp lý (30 giây).
4. Chạy bài test tải 5,000 req/s bằng Autocannon để đo lường độ trễ P99 trước và sau khi bật connection pool.
5. Lập báo cáo đối chuẩn hiệu năng kết nối `HTTP_POOL_BENCHMARK.md`.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```typescript
import { Agent, setGlobalDispatcher } from 'undici';

// High-Throughput HTTP Client Connection Pool via Undici
export const optimizedHttpAgent = new Agent({
  keepAliveTimeout: 60 * 1000,    // Keep sockets alive for 60 seconds
  keepAliveMaxTimeout: 120 * 1000,
  connections: 256,              // Max simultaneous connections per host
  pipelining: 1,                 // Safe HTTP/1.1 pipelining
});

setGlobalDispatcher(optimizedHttpAgent);
```

## 8. Anti-Patterns & Common Traps
- Khởi tạo một instance HTTP Client mới trong mỗi lần gọi hàm (ví dụ gọi `new http.Agent()` bên trong route handler).
- Đặt giá trị `maxSockets` quá nhỏ (ví dụ mặc định là 5 trong Node.js cũ) khiến hàng trăm request phải xếp hàng chờ socket trống.
- Lưu cache DNS vĩnh viễn không hết hạn khiến ứng dụng không nhận diện được IP mới khi hạ tầng đám mây tự động chuyển đổi dự phòng.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Độ trễ P99 gọi nội bộ giảm tối thiểu 50% sau khi kích hoạt HTTP Connection Pool.
- QG-02: Số lượng kết nối bị rơi vào trạng thái TIME_WAIT duy trì dưới 500 cổng dưới tải 2,000 req/s.
- QG-03: Tỷ lệ tái sử dụng socket (Socket Reuse Rate) đạt trên 95%.

## 10. Security & Safety Boundaries
- Đặt giới hạn thời gian chờ tối đa (`timeout`) cho kết nối để tránh việc máy chủ đối tác treo làm giữ chặt socket trong pool vô thời hạn (Slowloris attack).
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Module cấu hình HTTP Client Pool chuẩn hóa `HttpClientPool.ts`.
1. Báo cáo đối chuẩn hiệu năng tải trước và sau khi tối ưu.

## 13. Related & Complementary Skills
- [`dex-performance-optimization`](.agents/skills/dex-performance-optimization/SKILL.md)
- [`dex-service-contract-simulation`](.agents/skills/dex-service-contract-simulation/SKILL.md)
- [`dex-reliability-engineering`](.agents/skills/dex-reliability-engineering/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Dịch vụ thanh toán bị sập nghẽn trong đợt sale do liên tục tạo kết nối mới tới cổng thanh toán ngân hàng, dẫn đến hết sạch cổng socket trên máy chủ Linux. Kỹ sư kích hoạt `dex-http-client-connection-pooling`, cấu hình Undici Agent với 256 persistent sockets và DNS cache 30s, đưa thông lượng từ 400 req/s lên 4,500 req/s mà không rơi rớt kết nối nào.
