---
name: dex-rate-limiting-quotas
description: Design and enforce multi-tier rate limiting and quota management using algorithms like Sliding Window Log, Token Bucket, and Redis-backed distributed stores. Use to prevent API abuse, ensure tenant fairness, and enforce subscription tiers.
---

# dex-rate-limiting-quotas

## 1. Purpose & Scope
Thiết kế, xây dựng và triển khai hệ thống phân tầng giới hạn tần suất gọi API (Rate Limiting) và hạn mức tài nguyên (Quotas) dựa trên các thuật toán tối ưu (Token Bucket, Leaky Bucket, Sliding Window Counter) với backend phân tán (Redis/Memcached); bảo đảm sự công bằng giữa các tenant, ngăn chặn lạm dụng và bảo vệ hệ sinh thái dịch vụ.

## 2. When to Use
- Một số người dùng hoặc bot tự động spam request làm cạn kiệt tài nguyên hệ sinh thái.
- Triển khai gói dịch vụ SaaS phân tầng (Free: 100 req/min, Pro: 10,000 req/min).
- Bảo vệ các API nhạy cảm (Đăng nhập, Quên mật khẩu, Gửi OTP SMS) chống tấn công Brute-force.

## 3. When NOT to Use
- Không áp dụng rate limit quá khắt khe đối với các giao tiếp nội bộ giữa các microservices tin cậy (dùng service mesh auth).
- Không dùng thuật toán Fixed Window đơn giản cho các hệ thống yêu cầu độ chính xác cao vì dễ bị bùng nổ traffic tại điểm giao giữa 2 cửa sổ.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Quy tắc hạn mức (Rate limits: số request trên đơn vị thời gian) theo từng route hoặc User Tier.
- Khóa định danh khách hàng (API Key, User ID, Client IP, JWT Claim).
- Cụm Redis phân tán hỗ trợ thực thi kịch bản nguyên tử (Lua script).
- **Điều kiện tiên quyết**:
- Hạ tầng Redis/Key-value store có độ trễ cực thấp (<2ms) để không làm tăng đáng kể độ trễ của API Gateway.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Sliding Window Counter: Thuật toán cân bằng giữa độ chính xác của Sliding Log và tính tiết kiệm bộ nhớ của Fixed Window.
- Distributed Rate Limiting: Dùng Redis Lua script để bảo đảm thao tác kiểm tra và tăng biến đếm là nguyên tử (Atomic Check-and-Set), tránh Race Condition.
- HTTP Headers chuẩn: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `Retry-After`.
- **Quy tắc quyết định kỹ thuật**:
- Nếu request vượt hạn mức: trả về HTTP 429 Too Many Requests kèm header `Retry-After: <seconds>`.
- Nếu Redis gặp sự cố: chuyển sang chế độ Fail-Open (cho phép đi qua) kèm cảnh báo khẩn tới SRE thay vì chặn đứng toàn bộ traffic khách hàng.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Sử dụng Client IP làm khóa định danh duy nhất cho người dùng sau NAT proxy chung (ví dụ văn phòng công ty), khiến một người spam làm toàn bộ văn phòng bị khóa oan.

## 6. Step-by-Step Execution Workflow
1. Xác định tiêu chí phân tầng quota theo tài khoản người dùng và loại endpoint.
2. Viết Redis Lua script thực hiện thuật toán Sliding Window Counter.
3. Xây dựng Middleware tích hợp tại API Gateway (Kong, Envoy, hoặc Express/FastAPI).
4. Trả về đầy đủ các headers RateLimit tiêu chuẩn trong mọi phản hồi.
5. Thiết lập cơ chế Fail-Open và giám sát tỉ lệ 429 trên Grafana.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```lua
-- Redis Lua Script: Sliding Window Counter Rate Limiter
local key = KEYS[1]
local now = tonumber(ARGV[1])
local window = tonumber(ARGV[2])
local limit = tonumber(ARGV[3])
local clearBefore = now - window

redis.call('ZREMRANGEBYSCORE', key, 0, clearBefore)
local currentRequests = redis.call('ZCARD', key)

if currentRequests < limit then
    redis.call('ZADD', key, now, now)
    redis.call('EXPIRE', key, window)
    return 1 -- Cho phép
else
    return 0 -- Bị chặn (Rate limited)
end
```

### Lệnh xác minh & thực thi:
```bash
# Kiểm tra rate limit bằng curl lặp lại nhanh
for i in {1..15}; do curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8080/api/v1/auth/login; done
```

## 8. Anti-Patterns & Common Traps
- Không sử dụng Lua Script dẫn đến Race condition khi hai request đến song song vượt qua kiểm tra hạn mức.
- Đặt thời gian timeout của Redis quá lớn làm nghẽn toàn bộ luồng xử lý của API Gateway khi Redis chậm.

## 9. Quality Gates & Acceptance Criteria
- Middleware rate limiter chỉ được phép làm tăng độ trễ trung bình của API tối đa 2ms.
- Chặn chính xác 100% các request vượt ngưỡng hạn mức trong các bài test tự động.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Chống việc người dùng qua mặt rate limiter bằng cách giả mạo Header `X-Forwarded-For` (chỉ tin tưởng IP từ trusted proxy).
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ thống hỗ trợ**: Linux (CI/CD runners), macOS, Windows 11 PowerShell/WSL2.

## 12. Deliverables & Output Artifacts
- Script Lua và mã nguồn middleware Rate Limiter.
- Bộ test suite tự động kiểm chứng các kịch bản biên của rate limit.

## 13. Related & Complementary Skills
dex-api-abuse-prevention, dex-traffic-shaping-backpressure, dex-backend-architecture

## 14. Realistic Usage Example
### Tình huống thực tế:
Một dịch vụ AI bị một bên thứ ba viết script crawl tự động làm tăng vọt chi phí inference OpenAI. Đội ngũ triển khai Sliding Window Rate Limiting tại Envoy Gateway, giới hạn mỗi API Key chỉ được 60 requests/phút. Chi phí API lập tức giảm 45% mà không ảnh hưởng tới khách hàng thông thường.
