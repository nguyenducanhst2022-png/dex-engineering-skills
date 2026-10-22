---
name: dex-caching-strategies
description: Implement multi-layer caching strategies (Cache-Aside, Write-Through, Write-Behind), TTL expirations, cache stampede mitigation, and Redis clustering. Use when reducing database read load, accelerating latency-critical endpoints, or avoiding thundering herds.
---

# dex-caching-strategies

## 1. Purpose & Scope
Thiết kế và triển khai các chiến lược lưu bộ nhớ đệm (Caching Strategies) đa tầng (In-Memory, Distributed Redis Cache, CDN Edge Cache); ngăn chặn triệt để hiện tượng sập hàng loạt do bão truy vấn (Cache Stampede / Thundering Herd), rò rỉ dữ liệu cũ (Stale Data), và tối ưu hóa thời gian sống (TTL).

## 2. When to Use
- Khi cơ sở dữ liệu bị quá tải do phải xử lý hàng nghìn câu lệnh đọc giống hệt nhau mỗi giây.
- Khi thời gian phản hồi của các API đọc dữ liệu tĩnh hoặc dữ liệu ít thay đổi vượt quá ngưỡng SLA cho phép.
- Khi hệ thống chuẩn bị đối mặt với các sự kiện truy cập bùng nổ (Flash sale, sự kiện thể thao live).

## 3. When NOT to Use
- Dữ liệu có tính biến động cực cao và đòi hỏi tính nhất quán thời gian thực tuyệt đối (ví dụ: giao dịch khớp lệnh sàn chứng khoán).
- Các bảng dữ liệu rất nhỏ (< 50 dòng) mà database query đã chạy trong vòng 0.2ms.

## 4. Prerequisites & Input Context
**Đầu vào cần thiết:**
- Loại dữ liệu cần cache và tần suất cập nhật.
- Yêu cầu về thời gian sống TTL (Time-To-Live, ví dụ: 60s, 5m, 1h).
- Cơ sở dữ liệu cache mục tiêu (Redis / Memcached / Node-Cache).

**Điều kiện tiên quyết:**
- Redis cluster hoặc Redis instance đã được cấu hình bộ nhớ tối đa (`maxmemory`) và chính sách loại bỏ khóa (`maxmemory-policy: allkeys-lru`).
- Có kết nối mạng tốc độ cao có độ trễ cực thấp (< 2ms) giữa Web server và Cache server.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**: Nắm vững cơ chế vận hành theo chuẩn Agent Skills, tuân thủ nghiêm ngặt tính xác định và ranh giới trách nhiệm.
- **Quy tắc quyết định kỹ thuật**:
- **Xóa Cache Khi Cập Nhật (Evict, Don't Update)**: Luôn xóa khóa cache khi dữ liệu DB thay đổi thay vì cập nhật trực tiếp vào cache để tránh race condition giữa 2 request ghi đồng thời.
- **Mọi Khóa Phải Có TTL**: Tuyệt đối không bao giờ tạo một khóa trong Redis mà không gắn thời gian hết hạn TTL (trừ khi có lý do kiến trúc đặc biệt được ghi nhận).
- **Bảo Vệ Khỏi Cache Penetration**: Nếu truy vấn DB không tìm thấy bản ghi, hãy lưu một giá trị rỗng (`null`) với TTL ngắn (30s) để ngăn tin tặc liên tục gửi ID rác làm nghẽn DB.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Database sập vì Cache chết**: Redis bị mất điện, toàn bộ traffic đổ dồn thẳng vào database làm DB sập theo dây chuyền -> Khắc phục: Triển khai Circuit Breaker và Graceful Degradation đọc DB có giới hạn rate limit.
- **Dữ liệu không đồng bộ giữa 2 cụm máy chủ**: Người dùng sửa avatar nhưng vẫn thấy avatar cũ -> Khắc phục: Sử dụng cơ chế Pub/Sub để phát tín hiệu xóa cache trên toàn bộ các node.

## 6. Step-by-Step Execution Workflow
1. Lựa chọn mô hình Cache: Ưu tiên **Cache-Aside Pattern** cho hầu hết các tác vụ đọc.
2. Thiết kế Cấu trúc Key phân cấp có namespace rõ ràng: `app:users:v1:profile:{userId}`.
3. Khi Đọc (Read Path): Tra cứu Cache trước -> Nếu trúng (Cache Hit), trả về ngay; nếu trượt (Cache Miss), truy vấn Database, nạp vào Cache kèm TTL rồi mới trả về.
4. Khi Ghi (Write Path): Cập nhật Database trước -> Xóa (Invalidate) key tương ứng trong Cache để tránh stale data.
5. Chống Bão Truy Vấn (Cache Stampede): Bổ sung cơ chế Mutex Lock (Distributed Lock) khi tái tạo cache hoặc áp dụng XFetch / Probabilistic Early Expiration.
6. Phân bổ TTL ngẫu nhiên (Jitter): Cộng thêm một khoảng thời gian ngẫu nhiên nhỏ vào TTL (ví dụ: `300s + rand(0, 30s)`) để tránh hàng triệu key cùng hết hạn tại một giây duy nhất.

## 7. Concrete Examples
### Ví dụ triển khai chuẩn mực:
```typescript
// src/services/userCacheService.ts
export async function getUserWithCache(userId: string): Promise<User | null> {
  const cacheKey = `users:${userId}`;
  const cached = await redis.get(cacheKey);
  if (cached) return JSON.parse(cached);

  // Cache miss -> Truy vấn DB
  const user = await db.users.findById(userId);
  if (user) {
    const jitter = Math.floor(Math.random() * 30);
    await redis.set(cacheKey, JSON.stringify(user), 'EX', 300 + jitter);
  } else {
    await redis.set(cacheKey, 'null', 'EX', 30); // Chống Cache Penetration
  }
  return user;
}
```

### Lệnh xác minh & thực thi:
- Kiểm tra tỷ lệ Cache Hit/Miss trong Redis: `redis-cli info stats | grep -E '(keyspace_hits|keyspace_misses)'`
- Chạy kịch bản test cache hit/miss: `npm test -- tests/cache/userCache.spec.ts`
- Kiểm tra TTL của khóa: `redis-cli ttl app:users:v1:profile:123`

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước kiểm tra biên và giả định hệ thống luôn ở trạng thái lý tưởng.
- **Anti-Pattern 2**: Không ghi nhận nhật ký kiểm toán hoặc bỏ qua việc xử lý ngoại lệ lúc runtime.
- **Trap**: Bỏ qua các rào chắn an toàn hoặc cố tình chạy script không qua kiểm thử tự động.

## 9. Quality Gates & Acceptance Criteria
- QG-04: Tỷ lệ Cache Hit Rate đạt tối thiểu >= 80% trong các kịch bản đọc lặp lại.
- QG-10: Có bằng chứng kiểm tra không có khóa nào bị thiếu TTL.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động trước khi coi là hoàn thành.

## 10. Security & Safety Boundaries
- Tuyệt đối không lưu trữ thông tin xác thực chưa mã hóa (JWT refresh tokens, mật khẩu) trong bộ nhớ cache công cộng.
- Cấu hình Redis bắt buộc phải có mật khẩu mạnh (`requirepass`) và tắt các lệnh nguy hiểm (`FLUSHALL`, `CONFIG`).
- Không bao giờ thực thi mã nguồn hoặc thay đổi cấu hình trên môi trường sản xuất mà thiếu cơ chế rollback an toàn.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Có thể kích hoạt trực tiếp từ terminal hoặc extension tương thích trong VS Code / Cursor / Windsurf.

## 12. Deliverables & Output Artifacts
- Lớp Service triển khai Cache-Aside (`src/services/cacheService.ts`).
- File quản lý Cache Keys (`src/cache/keys.ts`).
- Bộ test xác minh luồng Hit, Miss và Invalidation.

## 13. Related & Complementary Skills
- `dex-development-workflow`: Quy trình phát triển tiêu chuẩn.
- `dex-code-verification`: Xác minh chất lượng và tính đúng đắn của mã nguồn.
- `dex-master-orchestrator`: Bộ điều phối trung tâm kết nối kỹ năng này với các kỹ năng khác trong hệ thống.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư hoặc AI Agent tiếp nhận yêu cầu liên quan đến **dex-caching-strategies**.
1. Đọc kỹ đầu vào và các ràng buộc kỹ thuật tại mục 4.
2. Thực thi tuần tự 6 bước trong Workflow tại mục 6.
3. Chạy các lệnh kiểm chứng tại mục 7 và đối chiếu với Quality Gates tại mục 9.
4. Đóng gói deliverables theo danh sách tại mục 12 và báo cáo kết quả kèm bằng chứng xác thực.
