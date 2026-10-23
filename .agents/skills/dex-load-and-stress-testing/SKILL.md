---
name: dex-load-and-stress-testing
description: Design, script, and execute realistic load, spike, endurance, and stress tests using tools like K6, Locust, or Gatling to establish saturation points, latency percentiles, and capacity limits. Use before high-traffic events or capacity sizing.
---

# dex-load-and-stress-testing

## 1. Purpose & Scope
Thiết kế kịch bản, lập trình và thực thi các bài kiểm thử tải (Load Testing), quá tải (Stress Testing), đột biến (Spike Testing) và ngâm tải dài hạn (Endurance Testing) bằng các công cụ chuyên dụng (K6, Locust, Gatling) để xác định ngưỡng bão hòa hệ thống, điểm đứt gãy, phân phối độ trễ (P95/P99) và năng lực xử lý tối đa.

## 2. When to Use
- Chuẩn bị cho các sự kiện lưu lượng truy cập lớn (Black Friday, Flash sale, Marketing campaigns).
- Xác định năng lực tối đa (Capacity Sizing) của cụm microservices.
- Đánh giá khả năng tự động co giãn (Auto-scaling) của hạ tầng Kubernetes/Cloud.

## 3. When NOT to Use
- Không chạy stress test lên production mà không có kế hoạch bảo trì hoặc sự đồng thuận của SRE on-call.
- Không dùng máy cá nhân phát tải nếu băng thông mạng cục bộ không đủ lớn để tạo áp lực tải thực sự.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Mục tiêu SLO/SLA (ví dụ: 5,000 RPS, P95 < 200ms, Error rate < 0.1%).
- Kịch bản hành vi người dùng điển hình (User journeys: Login -> Browse -> Add to Cart -> Checkout).
- Môi trường Staging có cấu hình tương đương (hoặc tỉ lệ 1:2) so với Production.
- **Điều kiện tiên quyết**:
- Hệ thống giám sát (APM, Prometheus, Grafana) đã sẵn sàng thu thập metrics của máy chủ mục tiêu.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Phân loại kiểm thử tải:
  + Load Test: Tải ổn định ở mức kỳ vọng để kiểm tra SLO.
  + Stress Test: Tăng dần tải cho đến khi hệ thống bắt đầu nghẽn hoặc sập để tìm giới hạn tối đa.
  + Spike Test: Đột ngột tăng vọt tải trong vài giây để kiểm tra khả năng co giãn và queue backpressure.
  + Soak/Endurance Test: Duy trì tải trung bình trong 12-24 giờ để phát hiện rò rỉ bộ nhớ (Memory Leak) hoặc cạn kiệt Connection Pool.
- **Quy tắc quyết định kỹ thuật**:
- Nếu Error rate vượt quá 1% hoặc P99 latency vượt quá 2 giây: ngừng tăng tải và xác định bottleneck.
- Nút thắt cổ chai thường gặp: Database connection pool bị đầy, CPU throttled, DNS lookup saturation.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Tải quá mạnh làm nghẽn luôn network của máy phát tải (Load Generator saturation), dẫn đến số liệu đo lường bị sai lệch.

## 6. Step-by-Step Execution Workflow
1. Thu thập số liệu traffic thực tế từ access logs để xây dựng mô hình tải (User mix percentage).
2. Viết mã kịch bản tải bằng K6 (JavaScript).
3. Chạy baseline test với 10 virtual users để kiểm tra tính chính xác của kịch bản.
4. Thực hiện Ramp-up tải theo các giai đoạn định sẵn.
5. Thu thập metrics CPU, RAM, IOPS, DB connections trong quá trình chạy tải.
6. Phân tích kết quả P95/P99 latency và đưa ra khuyến nghị tinh chỉnh tài nguyên.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```javascript
import http from 'k6/http';
import { check, sleep } from 'k6';

export const options = {
  stages: [
    { duration: '2m', target: 500 }, // ramp-up to 500 users
    { duration: '5m', target: 500 }, // stay at 500 users
    { duration: '1m', target: 0 },   // ramp-down
  ],
  thresholds: {
    http_req_duration: ['p(95)<300'], // 95% of requests must complete below 300ms
    http_req_failed: ['rate<0.01'],   // error rate < 1%
  },
};

export default function () {
  const res = http.get('https://staging-api.example.com/v1/catalog');
  check(res, { 'status is 200': (r) => r.status === 200 });
  sleep(1);
}
```

### Lệnh xác minh & thực thi:
```bash
k6 run --out json=results.json scripts/load-test.js
```

## 8. Anti-Patterns & Common Traps
- Chỉ test tải endpoint đọc (GET) mà bỏ qua các endpoint ghi (POST/PUT) có transaction nặng.
- Coi thường độ trễ P99 và chỉ nhìn vào độ trễ trung bình (Average).

## 9. Quality Gates & Acceptance Criteria
- Đạt tối thiểu mục tiêu RPS đặt ra với P95 latency dưới ngưỡng cam kết và error rate < 0.1%.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Kịch bản test tải không được phép làm lộ dữ liệu người dùng thật hoặc làm cạn kiệt số dư tài khoản thật.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ thống hỗ trợ**: Linux (CI/CD runners), macOS, Windows 11 PowerShell/WSL2.

## 12. Deliverables & Output Artifacts
- Script kịch bản K6/Locust hoàn chỉnh.
- Báo cáo phân tích hiệu năng và biểu đồ độ trễ kèm đề xuất cấu hình hạ tầng.

## 13. Related & Complementary Skills
dex-traffic-shaping-backpressure, dex-rate-limiting-quotas, dex-performance-optimization

## 14. Realistic Usage Example
### Tình huống thực tế:
Một sàn vé chuẩn bị mở bán concert âm nhạc. Đội SRE thực hiện stress test K6 lên 20,000 users đồng thời. Họ phát hiện DB Redis bị nghẽn connection pool tại 8,000 RPS. Sau khi chuyển sang dùng Redis Cluster và cấu hình connection pool tái sử dụng, hệ thống chịu tải mượt mà 15,000 RPS.
