---
name: dex-chaos-experiments
description: Design and execute chaos engineering experiments, fault injection, latency simulation, network partitions, circuit breaker verification, and resilience validation. Use when validating system fault tolerance, high availability, or disaster scenarios.
---

# dex-chaos-experiments

## 1. Purpose & Scope
Thiết kế và thực thi các thí nghiệm kỹ thuật hỗn loạn (Chaos Engineering Experiments) và tiêm lỗi có chủ đích (Fault Injection); mô phỏng độ trễ mạng bất thường, đứt gãy kết nối (Network Partitions), sập đột ngột các dịch vụ phụ thuộc (Dependency Outages), và tràn bộ nhớ; nhằm xác minh tính tự phục hồi (Resilience), cơ chế ngắt mạch (Circuit Breakers), và khả năng suy giảm chất lượng dịch vụ có kiểm soát (Graceful Degradation).

## 2. When to Use
- Khi hệ thống microservices có quá nhiều điểm phụ thuộc và chưa rõ nếu Redis hoặc dịch vụ thanh toán sập thì hệ thống có sập dây chuyền (Cascading Failure) hay không.
- Khi cần chứng minh cơ chế Circuit Breaker và Retry with Exponential Backoff hoạt động đúng như thiết kế.
- Trước các đợt cao điểm bán hàng (Black Friday, Tết) cần diễn tập độ bền hệ thống.

## 3. When NOT to Use
- Chạy trực tiếp trên môi trường production mà không có ranh giới an toàn (Blast Radius Control) hoặc chưa có cơ chế nút bấm dừng khẩn cấp (Emergency Stop Button).
- Ứng dụng đơn khối monolith chạy trên 1 server độc lập không có thành phần phân tán.

## 4. Prerequisites & Input Context
**Đầu vào cần thiết:**
- Giả thuyết hệ thống (Hypothesis: Ví dụ: Nếu Redis sập, API chỉ chậm đi 50ms nhưng vẫn trả về 200 từ Database chính).
- Điểm tiêm lỗi (Toxiproxy, Chaos Mesh, LitmusChaos, hoặc thư viện tiêm lỗi ứng dụng).
- Số liệu đo lường trạng thái ổn định (Steady State Metrics: Error rate < 1%, P99 Latency < 500ms).

**Điều kiện tiên quyết:**
- Hệ thống giám sát và cảnh báo thời gian thực đang hoạt động tốt.
- Có cơ chế Rollback hoặc hủy thí nghiệm ngay lập tức nếu chỉ số người dùng bị ảnh hưởng vượt quá ngưỡng an toàn.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**: Nắm vững cơ chế vận hành theo chuẩn Agent Skills, tuân thủ nghiêm ngặt tính xác định và ranh giới trách nhiệm.
- **Quy tắc quyết định kỹ thuật**:
- **Bắt Buộc Phải Có Nút Dừng Khẩn Cấp (Emergency Kill Switch)**: Mọi thí nghiệm hỗn loạn phải có thể dừng lại lập tức trong vòng 10 giây nếu các chỉ số nghiệp vụ chính bị suy giảm nghiêm trọng.
- **Bắt Đầu Từ Phạm Vi Nhỏ Nhất**: Không bao giờ tiêm lỗi toàn diện 100% ngay từ đầu; bắt đầu từ 1 container, 1 instance, hoặc một nhóm người dùng nội bộ trước.
- **Không Làm Chaos Nếu Chưa Có Observability**: Không được tiến hành thí nghiệm nếu hệ thống giám sát mù mờ, không thể đo lường được trạng thái ổn định.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Một service phụ bị chậm kéo sập toàn bộ thread pool của API Gateway**: Do không cấu hình timeout và circuit breaker -> Phát hiện qua Chaos test -> Khắc phục: Áp dụng timeout 1000ms và cấu hình Resilience4j / Cockatiel circuit breaker.
- **Database chính bị nghẽn kết nối khi Redis sập (Cache Stampede)**: Do hàng nghìn request tràn thẳng vào DB cùng lúc -> Khắc phục: Cài đặt Mutex Locking hoặc SingleFlight pattern.

## 6. Step-by-Step Execution Workflow
1. Định nghĩa trạng thái ổn định (Steady State) của hệ thống bằng các số liệu cụ thể (SLIs: Tỷ lệ lỗi < 0.1%, Doanh thu đặt hàng bình thường).
2. Đưa ra giả thuyết kiểm chứng (Hypothesis): Khi dịch vụ Đề xuất (Recommendation Service) bị trễ 3000ms, trang sản phẩm vẫn tải bình thường với danh sách mặc định nhờ Fallback cache.
3. Thiết lập bán kính ảnh hưởng tối thiểu (Blast Radius): Chỉ tiêm lỗi trên 5% lưu lượng thử nghiệm hoặc môi trường Staging tiệm cận production.
4. Thực hiện tiêm lỗi bằng công cụ (ví dụ: dùng Toxiproxy thêm 5000ms latency vào cổng kết nối upstream).
5. Quan sát hành vi hệ thống: Kiểm chứng Circuit Breaker có nhảy sang trạng thái OPEN để ngắt lưu lượng sau 5 lần timeout hay không.
6. Xác nhận cơ chế Fallback hoạt động: Người dùng vẫn nhận được phản hồi hữu ích thay vì nhận lỗi màn hình trắng 500.
7. Khôi phục trạng thái ban đầu và ghi nhận các điểm yếu kiến trúc vào báo cáo cải tiến.

## 7. Concrete Examples
### Ví dụ triển khai chuẩn mực:
```javascript
// resilience-policy.ts using cockatiel (Circuit Breaker & Fallback)
import { circuitBreaker, fallback, wrap, handleAll } from 'cockatiel';

const breaker = circuitBreaker(handleAll, {
  halfOpenAfter: 10_000,
  breaker: new ConsecutiveBreaker(5),
});

const fallbackPolicy = fallback(handleAll, () => {
  return { data: getStaleCachedData(), fromFallback: true };
});

export const resilientFetch = wrap(fallbackPolicy, breaker);
```

### Lệnh xác minh & thực thi:
- Bật tiêm độ trễ mạng qua Toxiproxy: `toxiproxy-cli toxic add -t latency -a latency=3000 redis_proxy`
- Chạy kịch bản kiểm thử tải trong lúc có lỗi: `k6 run tests/load/resilience-test.js`
- Xóa độc tố và khôi phục mạng: `toxiproxy-cli toxic remove -n latency_downstream redis_proxy`

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước kiểm tra biên và giả định hệ thống luôn ở trạng thái lý tưởng.
- **Anti-Pattern 2**: Không ghi nhận nhật ký kiểm toán hoặc bỏ qua việc xử lý ngoại lệ lúc runtime.
- **Trap**: Bỏ qua các rào chắn an toàn hoặc cố tình chạy script không qua kiểm thử tự động.

## 9. Quality Gates & Acceptance Criteria
- QG-04: Tỷ lệ lỗi của hệ thống trong lúc tiêm lỗi không vượt quá ngưỡng cho phép (Error Rate <= 1%).
- QG-08: Circuit breaker tự động chuyển sang OPEN trong vòng 5 giây khi dịch vụ đích không phản hồi.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động trước khi coi là hoàn thành.

## 10. Security & Safety Boundaries
- Đảm bảo các công cụ tiêm lỗi được phân quyền bảo mật chặt chẽ, không để kẻ xấu lợi dụng cổng điều khiển của Toxiproxy/Chaos Mesh để tấn công hệ thống.
- Không bao giờ thực thi mã nguồn hoặc thay đổi cấu hình trên môi trường sản xuất mà thiếu cơ chế rollback an toàn.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Có thể kích hoạt trực tiếp từ terminal hoặc extension tương thích trong VS Code / Cursor / Windsurf.

## 12. Deliverables & Output Artifacts
- Kịch bản thí nghiệm hỗn loạn (`tests/chaos/circuit-breaker-experiment.json`).
- Báo cáo kết quả thí nghiệm Chaos Report kèm biểu đồ so sánh trước/trong/sau khi tiêm lỗi.
- Danh sách hành động cải tiến độ bền hệ thống.

## 13. Related & Complementary Skills
- `dex-development-workflow`: Quy trình phát triển tiêu chuẩn.
- `dex-code-verification`: Xác minh chất lượng và tính đúng đắn của mã nguồn.
- `dex-master-orchestrator`: Bộ điều phối trung tâm kết nối kỹ năng này với các kỹ năng khác trong hệ thống.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư hoặc AI Agent tiếp nhận yêu cầu liên quan đến **dex-chaos-experiments**.
1. Đọc kỹ đầu vào và các ràng buộc kỹ thuật tại mục 4.
2. Thực thi tuần tự 6 bước trong Workflow tại mục 6.
3. Chạy các lệnh kiểm chứng tại mục 7 và đối chiếu với Quality Gates tại mục 9.
4. Đóng gói deliverables theo danh sách tại mục 12 và báo cáo kết quả kèm bằng chứng xác thực.
