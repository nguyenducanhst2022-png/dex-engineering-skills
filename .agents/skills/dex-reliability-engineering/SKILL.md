---
name: dex-reliability-engineering
description: System resilience, fault tolerance, graceful degradation, circuit breakers, timeout deadlines, and exponential backoff retry patterns. Guarantees business continuity and recovery under network failure or third-party outages. Use when integrating third-party APIs, handling network calls, or designing fault-tolerant systems.
---

# DEX Reliability Engineering

## 1. Purpose & Scope
Nâng cao độ tin cậy và khả năng chống chịu sự cố (Fault Tolerance) của hệ thống phần mềm; đảm bảo ứng dụng có thể tự động phục hồi khi gặp lỗi, suy thoái êm đẹp (Graceful Degradation) khi quá tải và tiếp tục phục vụ người dùng kể cả khi một số dịch vụ bên ngoài bị sập.

Quy trình tăng độ tin cậy chuẩn:
`Xác định điểm lỗi → Phân tích tình huống → Thiết kế xử lý → Triển khai bảo vệ → Kiểm thử lỗi giả lập → Đánh giá khả năng phục hồi → Ổn định → Lưu Git`

Nguyên tắc cốt lõi: **Mọi dịch vụ bên thứ ba và kết nối mạng đều CÓ THỂ BỊ LỖI bất kỳ lúc nào. Hệ thống phải được thiết kế để tự xử lý lỗi, giảm tải an toàn và không bao giờ để một lỗi cục bộ làm sập toàn bộ ứng dụng.**
Ghi nhớ sống còn: **Độ tin cậy cao = Có Timeout + Có Retry thông minh + Có Circuit Breaker + Suy thoái êm đẹp.**

## 2. When to Use
- Khi thực hiện các cuộc gọi HTTP ra dịch vụ bên ngoài (Payment Gateways, SMS, Email, 3rd Party APIs).
- Khi kết nối với Database hoặc Message Broker qua mạng.
- Khi cần cơ chế thử lại tự động (Retry Mechanism) kèm giãn cách theo số mũ (Exponential Backoff).
- Khi ngăn chặn sự cố dây chuyền (Cascading Failures) bằng mô hình Circuit Breaker.

## 3. When NOT to Use
- Thao tác tính toán nội bộ thuần túy trong RAM (Pure in-memory operations) không có rủi ro I/O mạng.
- Áp dụng cơ chế retry mù quáng cho các lỗi do dữ liệu client gửi sai (Mã HTTP 400, 401, 404 không bao giờ được retry).

## 4. Prerequisites & Input Context
- Danh sách các điểm tích hợp I/O mạng và dịch vụ bên thứ ba.
- Thời gian phản hồi tối đa cho phép (Timeout SLAs, ví dụ: API ngoài tối đa 3 giây).
- Kế hoạch dự phòng (Fallback plan) khi dịch vụ ngoài ngừng hoạt động.

## 5. Core Concepts & Taxonomy
- **Nguyên tắc cốt lõi**: Tuân thủ triệt để nguyên lý vận hành xác định và ranh giới trách nhiệm của chuẩn Agent Skills.
- **Tính nhất quán hệ thống**: Mọi thao tác kỹ thuật phải có thể kiểm chứng độc lập với số liệu rõ ràng.
- **Ngăn ngừa hồi quy**: Bất kỳ sửa đổi nào cũng phải bảo vệ tính tương thích ngược và chất lượng đã được nghiệm thu.

## 6. Step-by-Step Execution Workflow
### Bước 1: Xác Định Các Điểm Dễ Hỏng (Single Points of Failure - SPOF)
- Lập danh sách tất cả các lời gọi mạng:
  - Cổng thanh toán (Stripe/PayPal/VNPay).
  - Dịch vụ gửi email/SMS.
  - Redis cache / External storage (S3).
- Đặt câu hỏi: *Nếu dịch vụ này bị treo phản hồi trong 30 giây hoặc sập hoàn toàn, ứng dụng của chúng ta sẽ ứng xử ra sao?*

### Bước 2: Thiết Lập Hạn Giờ Bắt Buộc (Strict Timeouts)
- **Tuyệt đối không bao giờ gọi mạng mà không có Timeout**:
  - Đặt timeout kết nối (Connection timeout, ví dụ: 2 giây).
  - Đặt timeout đọc dữ liệu (Read timeout, ví dụ: 5 giây).
  - Sử dụng `AbortController` (JavaScript/TypeScript) hoặc context with timeout (Go/Python).

### Bước 3: Triển Khai Retry Thông Minh Với Exponential Backoff
- Chỉ retry các lỗi tạm thời (Transient errors: HTTP 502, 503, 504, Network disconnect).
- Tuyệt đối KHÔNG retry các lỗi client (HTTP 4xx).
- Công thức giãn cách: $T = \text{base\_delay} \times 2^{\text{attempt}} + \text{jitter}$ (bổ sung jitter ngẫu nhiên để tránh tình trạng hàng nghìn request cùng retry một lúc gây bão request - Thundering Herd).
- Giới hạn số lần thử lại tối đa (thường từ 2-3 lần).

### Bước 4: Thiết Lập Circuit Breaker (Cầu Dao Ngắt Mạch)
- Áp dụng mô hình Circuit Breaker 3 trạng thái:
  - **CLOSED**: Trạng thái bình thường, cho phép request đi qua.
  - **OPEN**: Khi tỷ lệ lỗi vượt ngưỡng (ví dụ >50% lỗi trong 10 giây), cầu dao lập tức NGẮT, từ chối mọi request tiếp theo và trả về phản hồi fallback ngay lập tức mà không cần chờ timeout.
  - **HALF-OPEN**: Sau một khoảng thời gian (ví dụ 30 giây), cho phép một vài request thử nghiệm đi qua để kiểm tra dịch vụ ngoài đã hồi phục chưa.

### Bước 5: Thiết Kế Cơ Chế Suy Thoái Êm Đẹp (Graceful Degradation / Fallback)
- Cung cấp trải nghiệm thay thế khi lỗi xảy ra:
  - Nếu Redis cache sập → Tự động đọc dữ liệu trực tiếp từ Database với tốc độ chậm hơn một chút thay vì báo lỗi.
  - Nếu dịch vụ gợi ý sản phẩm sập → Hiển thị danh sách sản phẩm bán chạy tĩnh thay vì trang trắng.

### Bước 6: Kiểm Thử Lỗi Giả Lập (Chaos & Fault Injection Testing)
- Giả lập tình huống lỗi mạng: Mock timeout, mock mã lỗi HTTP 500.
- Kiểm chứng hệ thống xử lý êm đẹp, không bị crash tiến trình (unhandled promise rejection).

## 7. Concrete Examples
```bash
# Lệnh thực thi & kiểm chứng tiêu chuẩn
dex verify --skill dex-reliability-engineering
```

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước xác minh tự động và dựa vào giả định chủ quan.
- **Anti-Pattern 2**: Thay đổi diện rộng vượt ngoài phạm vi (Scope Creep) làm mất kiểm soát rủi ro.
- **Trap**: Thực hiện thao tác phá hủy hoặc thay đổi trạng thái sản xuất khi chưa qua cổng kiểm duyệt an toàn.

## 9. Quality Gates & Acceptance Criteria
- **QG-01 (All External Calls Guarded)**: 100% các cuộc gọi ra bên ngoài đều có Timeout tường minh.
- **QG-05 (Fault Injection Tests PASS)**: Kịch bản giả lập dịch vụ ngoài sập được ứng dụng xử lý đúng fallback và đạt PASS.
- **QG-06 (No Unhandled Exceptions)**: Không có ngoại lệ mạng nào làm sập tiến trình máy chủ.

## 10. Security & Safety Boundaries
- **Cấm Vòng Lặp Retry Vô Tận (No Infinite Retries)**: Số lần retry tối đa không bao giờ vượt quá 3-5 lần.
- **Phải Có Tính Bất Biến Lặp Lại (Idempotency)**: Khi retry các thao tác làm thay đổi dữ liệu (POST/PUT), bắt buộc phải gửi kèm Idempotency Key để tránh trừ tiền 2 lần hoặc tạo 2 đơn hàng trùng nhau.
- **Không Nuốt Lỗi Âm Thầm (No Silent Error Swallowing)**: Fallback phải được ghi nhận vào hệ thống cảnh báo (Warning log) để đội ngũ kỹ thuật biết rằng dịch vụ đang hoạt động ở chế độ suy thoái.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Kích hoạt thông qua terminal hoặc tiện ích mở rộng IDE tương thích (VS Code, Cursor, Windsurf).

## 12. Deliverables & Output Artifacts
1. Mã nguồn tích hợp đầy đủ Timeout, Retry with Exponential Backoff và Circuit Breaker.
2. Logic Fallback dự phòng thân thiện với người dùng.
3. Bộ bài kiểm thử giả lập sự cố mạng đạt 100% PASS.

## 13. Related & Complementary Skills
- `dex-master-orchestrator`: Điều phối trung tâm.

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Kỹ sư hoặc AI Agent kích hoạt **dex-reliability-engineering** trong dự án.
1. Tiếp nhận ngữ cảnh đầu vào và kiểm tra điều kiện tiên quyết tại Mục 4.
2. Vận hành tuần tự các bước theo Quy trình tại Mục 6.
3. Kiểm chứng đầu ra đối chiếu với Tiêu chuẩn chấp thuận tại Mục 9.
4. Bàn giao đầy đủ hiện vật theo Mục 12 và cập nhật tài liệu liên quan.
