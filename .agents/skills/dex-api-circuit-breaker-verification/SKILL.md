---
name: dex-api-circuit-breaker-verification
description: Design, implement, and verify distributed API Circuit Breaker state machines. Test CLOSED, OPEN, and HALF-OPEN transitions, fallback responses, and prevent cascading cascading system failures.
---

# dex-api-circuit-breaker-verification

## 1. Purpose & Scope
Thiết kế, cài đặt và kiểm chứng tính đúng đắn của máy trạng thái ngắt mạch phân tán (Distributed API Circuit Breaker State Machine); kiểm tra toàn diện các chu kỳ chuyển đổi trạng thái ĐÓNG (Closed - hoạt động bình thường), MỞ (Open - ngắt kết nối khẩn cấp) và NỬA MỞ (Half-Open - thử nghiệm phục hồi); cung cấp cơ chế phản hồi dự phòng tức thì (Graceful Fallback), ngăn ngừa hiện tượng lỗi dây chuyền (Cascading Failures) và triệt tiêu nguy cơ bão yêu cầu đè bẹp hệ thống phía sau (Thundering Herd).

## 2. When to Use
- Khi gọi các dịch vụ bên thứ ba (Cổng thanh toán, Dịch vụ gửi SMS, API Đối tác) có độ tin cậy không ổn định hoặc thường xuyên chập chờn.
- Khi bảo vệ các microservices nội bộ khỏi nguy cơ bị cạn kiệt tài nguyên luồng (Thread Starvation) do dịch vụ phụ thuộc phản hồi quá chậm.
- Khi thiết lập khả năng phục hồi tự động (Self-Healing) cho hệ thống phân tán trong điều kiện mạng suy giảm chất lượng.

## 3. When NOT to Use
- Khi tương tác với cơ sở dữ liệu nội bộ trong cùng một transaction nguyên tử (ACID transaction).
- Khi yêu cầu là các tác vụ ghi dữ liệu tài chính bắt buộc phải hoàn thành đồng bộ không được phép sử dụng dữ liệu dự phòng cũ.

## 4. Prerequisites & Input Context
- **Thư viện Circuit Breaker:** Resilience4j (Java/Kotlin), Polly (C#), go-breaker (Go), opossum (Node.js), hoặc tenacity/pybreaker (Python).
- **Hạ tầng kiểm thử:** WireMock hoặc Mountebank để giả lập lỗi và độ trễ mạng có chủ đích.

## 5. Core Concepts & Taxonomy
- **Sliding Window Metrics:** Cơ chế ghi nhận tỷ lệ lỗi dựa trên số lượng yêu cầu gần nhất (Count-based Sliding Window, ví dụ 100 requests) hoặc khoảng thời gian (Time-based, ví dụ 10s).
- **Failure Rate Threshold:** Tỷ lệ phần trăm yêu cầu thất bại hoặc phản hồi chậm (Slow Call Rate) kích hoạt chuyển trạng thái từ CLOSED sang OPEN (thường đặt ở mức 50%).
- **Half-Open Probe Requests:** Khi hết thời gian chờ (Wait Duration in Open State), Circuit Breaker cho phép một số lượng nhỏ yêu cầu (ví dụ 5 requests) đi qua để kiểm tra xem dịch vụ phía sau đã thực sự khỏe mạnh hay chưa.

## 6. Step-by-Step Execution Workflow
1. Khảo sát SLA và thời gian timeout tối đa của API dịch vụ phía sau.
2. Cấu hình tham số Circuit Breaker: `failureRateThreshold: 50%`, `waitDurationInOpenState: 15s`, `slidingWindowSize: 20`.
3. Định nghĩa hàm Fallback trả về dữ liệu bộ nhớ đệm (Cached Response) hoặc thông báo thân thiện cho người dùng.
4. Thực hiện bài kiểm thử tự động giả lập 20 yêu cầu lỗi liên tiếp và khẳng định mạch chuyển ngay sang trạng thái OPEN.
5. Khẳng định các yêu cầu tiếp theo trong thời gian OPEN bị chặn lập tức (Fail-Fast) với độ trễ <1ms mà không gửi ra mạng.
6. Chờ hết thời gian 15 giây, gửi 5 yêu cầu thành công và khẳng định mạch tự động chuyển về trạng thái CLOSED bình thường.

## 7. Concrete Examples
### Cai dat Circuit Breaker voi Opossum trong Node.js / TypeScript:
```typescript
import CircuitBreaker from 'opossum';
import axios from 'axios';

interface PaymentResponse {
  transactionId: string;
  status: string;
}

async function callPaymentGateway(orderId: string, amount: number): Promise<PaymentResponse> {
  const response = await axios.post('https://api.payment.example.com/v1/charge', {
    orderId,
    amount
  }, { timeout: 2000 }); // Timeout 2 giay
  return response.data;
}

const options: CircuitBreaker.Options = {
  timeout: 2500, // Thoi gian coi la timeout
  errorThresholdPercentage: 50, // Ty le loi >= 50% thi ngat mach
  resetTimeout: 10000, // Cho 10 giay truoc khi vao Half-Open de test lai
  rollingCountTimeout: 10000,
  rollingCountBuckets: 10
};

export const paymentBreaker = new CircuitBreaker(callPaymentGateway, options);

// Cung cap ham Fallback khi mach OPEN hoac loi
paymentBreaker.fallback((orderId, amount) => {
  console.warn(`[CIRCUIT BREAKER] Fallback triggered for order ${orderId}. Payment queued.`);
  return {
    transactionId: "PENDING_OFFLINE",
    status: "QUEUED_FOR_RETRY"
  };
});

paymentBreaker.on('open', () => console.error('[CIRCUIT BREAKER] State changed to OPEN! Failing fast.'));
paymentBreaker.on('halfOpen', () => console.log('[CIRCUIT BREAKER] State changed to HALF-OPEN. Probing...'));
paymentBreaker.on('close', () => console.log('[CIRCUIT BREAKER] State changed to CLOSED. Service healthy.'));
```

## 8. Anti-Patterns & Common Traps
- **Missing Timeout Configuration:** Bật Circuit Breaker nhưng quên đặt `requestTimeout` khiến các kết nối bị treo vĩnh viễn ở trạng thái chờ đợi thay vì tính là lỗi.
- **Shared Circuit Breaker for Different APIs:** Dùng chung một phiên bản Circuit Breaker duy nhất cho nhiều API khác nhau, khiến sự cố của API gửi mail làm sập luôn API thanh toán.
- **Zero Fallback Strategy:** Để mạch OPEN nhưng không có hàm fallback khiến người dùng nhận trang lỗi 500 thay vì thông báo hướng dẫn hoặc nội dung cached.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Mạch chuyển trạng thái từ CLOSED sang OPEN chính xác 100% khi tỷ lệ lỗi vượt ngưỡng quy định trong bài test tự động.
- **QG-02**: Trong trạng thái OPEN, 100% yêu cầu được xử lý Fail-Fast với thời gian phản hồi dưới 2ms mà không làm nghẽn kết nối mạng.
- **QG-03**: Mạch phục hồi an toàn về CLOSED sau khi các yêu cầu thăm dò trong giai đoạn HALF-OPEN thành công.

## 10. Security & Safety Boundaries
- Bảo đảm dữ liệu trả về từ hàm Fallback không làm lộ các thông tin nhạy cảm của người dùng khác được lưu trong cache.

## 11. Platform Adapters
- **Runtimes**: Resilience4j (Java), Polly (.NET), Opossum (Node.js), pybreaker (Python), Istio Circuit Breaker.

## 12. Deliverables & Output Artifacts
- Module quản lý Circuit Breaker phân tán (`circuit_breaker_service.ts`).
- Bộ kiểm thử tự động kiểm chứng 3 trạng thái máy trạng thái (`test_circuit_breaker.ts`).

## 13. Related & Complementary Skills
dex-cloud-database-failover-drills, dex-release-progressive-metrics, dex-queue-capacity-saturation

## 14. Realistic Usage Example
```bash
# Chay test kiem thu chuyen doi trang thai Circuit Breaker bang Jest
npx jest tests/test_circuit_breaker.test.ts --verbose
```
