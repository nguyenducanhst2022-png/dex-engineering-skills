---
name: dex-inference-provider-rate-controls
description: Engineer multi-provider LLM rate limiting, token-bucket throttling, adaptive exponential backoff, and transparent provider failover. Use when operating production LLM applications across OpenAI, Anthropic, Gemini, or local models.
---

# dex-inference-provider-rate-controls

## 1. Purpose & Scope
Thiết kế và quản trị hệ thống điều tiết lưu lượng và giới hạn tốc độ gọi mô hình AI (Multi-Provider Inference Rate Controls); cài đặt thuật toán Token Bucket / Leaky Bucket nhận biết số lượng token, cơ chế thử lại với exponential backoff có jitter, và tự động chuyển đổi dự phòng (Failover Routing) giữa các nhà cung cấp khi gặp lỗi quá hạn ngạch (HTTP 429).

## 2. When to Use
- Khi ứng dụng sản xuất gửi hàng ngàn request mỗi phút tới các API nhà cung cấp LLM (OpenAI, Anthropic, Google Gemini, Groq).
- Khi liên tục gặp lỗi `HTTP 429 Rate Limit Exceeded` (TPM - Tokens Per Minute hoặc RPM - Requests Per Minute) làm gián đoạn trải nghiệm người dùng.
- Khi muốn phân bổ lưu lượng thông minh giữa các nhà cung cấp để tối ưu chi phí và bảo đảm tính sẵn sàng 99.99%.

## 3. When NOT to Use
- Khi chỉ chạy thử nghiệm cục bộ với vài request mỗi ngày không bao giờ chạm giới hạn.
- Khi sử dụng cụm máy chủ tự host riêng biệt (Dedicated GPU Cluster) có thông lượng cố định không áp dụng rate limit của bên thứ ba.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Hạn ngạch RPM/TPM của từng API key của từng nhà cung cấp, kho lưu trữ bộ đếm dùng chung (Redis Cluster), danh sách provider fallback ưu tiên.
- **Quyền hạn truy cập:** Quyền quản lý API keys và cấu hình routing gateway.

## 5. Core Concepts & Taxonomy
- **Token-Aware Rate Limiting:** Giới hạn tốc độ không chỉ đếm số request mà còn ước lượng trước số lượng token của prompt để khấu trừ vào hạn ngạch TPM trước khi gửi đi.
- **Full Jitter Exponential Backoff:** Khi nhận lỗi 429: lùi thời gian thử lại theo hàm mũ kèm thành phần ngẫu nhiên để tránh việc toàn bộ các worker cùng gửi lại cùng một tích tắc (Thundering Herd Problem).
- **Circuit Breaker Failover:** Nếu Nhà cung cấp A bị lỗi liên tiếp hoặc quá tải kéo dài, tự động ngắt mạch (Open Circuit) và chuyển hướng 100% lưu lượng sang Nhà cung cấp B trong 5 phút.

## 6. Step-by-Step Execution Workflow
1. Khai báo bảng hạn ngạch RPM và TPM cho từng nhà cung cấp trong hệ thống lưu trữ tập trung (Redis).
2. Trước khi gửi request: ước lượng số token của prompt bằng tokenizer cục bộ và yêu cầu cấp quyền từ Token Bucket.
3. Nếu hạn ngạch tạm thời bị đầy: đưa request vào hàng đợi ưu tiên (Priority Queue) và chờ token được nạp thêm.
4. Gửi request tới nhà cung cấp chính; nếu nhận phản hồi thành công, cập nhật số token thực tế tiêu thụ từ header phản hồi.
5. Nếu nhận mã lỗi `HTTP 429 Rate Limit Exceeded`: phân tích header `retry-after` (nếu có), thực hiện lùi thời gian thử lại hoặc kích hoạt chuyển đổi sang nhà cung cấp dự phòng.
6. Theo dõi tỷ lệ sử dụng hạn ngạch (% Quota Used) trên Grafana và cảnh báo khi mức tiêu thụ vượt 80% ngưỡng cho phép.

## 7. Concrete Examples
### Ví dụ cơ chế Token-Bucket Rate Limiter hỗ trợ Failover trong Python:
```python
import time
import random

class LLMRateLimiter:
    def __init__(self, tpm_limit: int, rpm_limit: int):
        self.tpm_limit = tpm_limit
        self.rpm_limit = rpm_limit
        self.available_tokens = tpm_limit
        self.available_requests = rpm_limit
        self.last_refill = time.monotonic()

    def acquire(self, estimated_tokens: int, timeout=10.0) -> bool:
        start_time = time.monotonic()
        while time.monotonic() - start_time < timeout:
            self._refill()
            if self.available_tokens >= estimated_tokens and self.available_requests >= 1:
                self.available_tokens -= estimated_tokens
                self.available_requests -= 1
                return True
            # Ngủ ngắn có jitter tránh tranh chấp
            time.sleep(0.05 + random.uniform(0.01, 0.05))
        return False

    def _refill(self):
        now = time.monotonic()
        elapsed = now - self.last_refill
        # Nạp lại token và request theo tỷ lệ thời gian trôi qua trong 60 giây
        self.available_tokens = min(self.tpm_limit, self.available_tokens + int(elapsed * (self.tpm_limit / 60.0)))
        self.available_requests = min(self.rpm_limit, self.available_requests + int(elapsed * (self.rpm_limit / 60.0)))
        self.last_refill = now
```

## 8. Anti-Patterns & Common Traps
- **Blind Immediate Retry:** Khi nhận lỗi 429 lập tức gửi lại ngay trong vòng 1 mili-giây, khiến IP bị nhà cung cấp khóa vĩnh viễn vì nghi ngờ tấn công DDoS.
- **Ignoring Token Budget:** Chỉ đếm số lượng requests mà bỏ qua kích thước token, dẫn tới dù chỉ gửi 5 requests nhưng mỗi request 50k tokens làm sập hạn ngạch TPM.
- **Hardcoded Single Provider:** Phụ thuộc hoàn toàn vào một nhà cung cấp duy nhất mà không có cơ chế chuyển hướng khi dịch vụ đó bị ngừng hoạt động toàn cầu.

## 9. Quality Gates & Acceptance Criteria
- **QG-03**: Hệ thống tự động chuyển đổi sang nhà cung cấp dự phòng trong dưới 500ms khi nhận lỗi 429 từ nhà cung cấp chính.
- **QG-07**: Tỷ lệ request bị thất bại hoàn toàn do lỗi Rate Limit trên môi trường sản xuất dưới 0.01%.
- **QG-10**: Cơ chế Circuit Breaker tự động đóng lại (Half-Open) để thăm dò khi nhà cung cấp chính phục hồi.

## 10. Security & Safety Boundaries
- Quản lý API keys của các nhà cung cấp trong Secret Manager, tuyệt đối không in keys trong thông báo lỗi hoặc log retry.
- Mã hóa các khóa kết nối trong bộ nhớ đệm và phân quyền truy cập nghiêm ngặt.

## 11. Platform Adapters
- **Gateways**: LiteLLM Proxy, Portkey, Cloudflare AI Gateway, Langfuse.
- **Storage**: Redis Token Bucket, AWS ElastiCache.

## 12. Deliverables & Output Artifacts
- Module Rate Limiter nhận biết token hỗ trợ đa nhà cung cấp.
- Cơ chế Circuit Breaker và Failover Router tự động.
- Dashboard giám sát mức tiêu thụ hạn ngạch TPM/RPM theo thời gian thực.

## 13. Related & Complementary Skills
dex-rate-limiting-quotas, dex-traffic-shaping-backpressure, dex-llm-fallback-routing

## 14. Realistic Usage Example
```powershell
# Kiểm tra trạng thái hạn ngạch và chạy bài test chịu tải rate limiting
python scripts/test_rate_limiter.py --concurrency 20 --duration 30s
```
