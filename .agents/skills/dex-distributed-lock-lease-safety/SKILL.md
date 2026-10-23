---
name: dex-distributed-lock-lease-safety
description: Implement distributed locks and leases with fencing tokens, lock renewal heartbeats, and fail-safe timeouts. Use when coordinating exclusive access to non-transactional shared resources across distributed worker clusters.
---

# dex-distributed-lock-lease-safety

## 1. Purpose & Scope
Thiết kế và cài đặt khóa phân tán (Distributed Locks) và cơ chế thuê quyền (Leases) bảo đảm an toàn tuyệt đối; tích hợp Fencing Tokens để ngăn chặn xung đột dữ liệu do tiến trình bị trễ GC (Stop-The-World) hoặc phân mảnh mạng, kiểm soát heartbeat gia hạn khóa tự động.

## 2. When to Use
- Khi nhiều worker phân tán cùng cần truy cập độc quyền vào một tài nguyên không hỗ trợ transaction (ví dụ: tạo tệp PDF trên S3, gọi API của bên thứ ba không có concurrency control).
- Khi bầu chọn tiến trình trưởng (Leader Election) trong cụm worker chạy ngầm.
- Khi cần giới hạn chỉ một cron job duy nhất được thực thi tại một thời điểm trên toàn bộ cluster.

## 3. When NOT to Use
- Khi tài nguyên chia sẻ là một cơ sở dữ liệu quan hệ có hỗ trợ câu lệnh khóa dòng `SELECT ... FOR UPDATE`.
- Khi mục tiêu chỉ là đồng bộ hóa giữa các luồng (threads) bên trong cùng một tiến trình ứng dụng đơn lẻ.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Kho lưu trữ khóa phân tán có hỗ trợ thao tác nguyên tử và TTL (Redis, Consul, Etcd, Zookeeper), tài nguyên dùng chung cần bảo vệ.
- **Quyền hạn truy cập:** Quyền đọc/ghi các key phân tán trên cụm Redis/Etcd.

## 5. Core Concepts & Taxonomy
- **Fencing Token:** Số nguyên tăng đơn điệu được trả về mỗi khi khóa được cấp phát; tầng lưu trữ tài nguyên sẽ từ chối các thao tác ghi mang token nhỏ hơn token mới nhất đã thấy.
- **Lock Lease TTL:** Thời hạn tồn tại tự động hết hạn của khóa nhằm tránh trường hợp tiến trình nắm giữ khóa bị chết đột ngột khiến khóa bị khóa vĩnh viễn (deadlock).
- **Heartbeat Lock Renewal:** Tiến trình nền tự động gia hạn TTL của khóa định kỳ khi tác vụ vẫn đang tiếp tục chạy bình thường.

## 6. Step-by-Step Execution Workflow
1. Yêu cầu cấp phát khóa nguyên tử kèm theo thời gian sống TTL ngắn (ví dụ: 10 giây) và nhận Fencing Token tăng dần.
2. Khởi tạo tác vụ nền (background thread/coroutine) để tự động gia hạn khóa sau mỗi 1/3 chu kỳ TTL.
3. Gửi Fencing Token kèm theo mọi thao tác ghi tới tài nguyên chia sẻ bên ngoài.
4. Tầng lưu trữ tài nguyên xác nhận Fencing Token $\\ge$ Fencing Token hiện tại trước khi cho phép ghi.
5. Khi hoàn thành công việc: dừng heartbeat gia hạn và giải phóng khóa an toàn bằng cách so sánh đúng token sở hữu (tránh xóa nhầm khóa của tiến trình khác).
6. Bắt lỗi quá hạn khóa: nếu heartbeat thất bại và khóa hết hạn, tiến trình lập tức hủy bỏ tác vụ ngay để tránh ghi đè dữ liệu sai lệch.

## 7. Concrete Examples
### Ví dụ giải phóng khóa an toàn bằng Lua Script trong Redis:
```lua
-- Lua script giải phóng khóa an toàn: Chỉ xóa nếu giá trị token khớp chính xác
if redis.call("get", KEYS[1]) == ARGV[1] then
    return redis.call("del", KEYS[1])
else
    return 0
end
```

### Triển khai Fencing Token kiểm tra tại tầng lưu trữ:
```python
class StorageService:
    def __init__(self):
        self.highest_fencing_token = 0

    def write_data(self, fencing_token: int, payload: dict):
        if fencing_token < self.highest_fencing_token:
            # Phát hiện Zombie Process bị trễ GC cố ghi dữ liệu cũ
            raise RuntimeError(f"Fencing token {fencing_token} is stale. Current: {self.highest_fencing_token}")
        
        self.highest_fencing_token = fencing_token
        self.commit_to_disk(payload)
        return True
```

## 8. Anti-Patterns & Common Traps
- **Naive Redis Lock:** Dùng lệnh `SETNX` không có TTL khiến server crash làm hệ thống bị treo cứng vĩnh viễn.
- **Blind Lock Deletion:** Dùng lệnh `DEL key` đơn giản để giải phóng khóa, dẫn tới việc xóa mất khóa mới của tiến trình khác khi tiến trình hiện tại bị chạy quá giờ.
- **Locking without Fencing:** Nghĩ rằng có distributed lock là đủ an toàn mà không kiểm tra fencing token, để tiến trình bị lag GC ghi đè làm hỏng dữ liệu của tiến trình mới.

## 9. Quality Gates & Acceptance Criteria
- **QG-05**: Thao tác giải phóng khóa bắt buộc sử dụng Lua script hoặc CAS nguyên tử có so sánh token sở hữu.
- **QG-09**: Tất cả các thao tác ghi vào tài nguyên chia sẻ đều bắt buộc kiểm tra fencing token tăng đơn điệu.
- **QG-10**: Khóa tự động được giải phóng an toàn trong vòng 10 giây nếu tiến trình nắm giữ bị tắt đột ngột (`kill -9`).

## 10. Security & Safety Boundaries
- Token sở hữu khóa phải là chuỗi ngẫu nhiên có độ dài tối thiểu 128-bit (cryptographically secure random string).
- Phân quyền hạn chế các dịch vụ không liên quan có thể ghi đè các key khóa phân tán trên Redis.

## 11. Platform Adapters
- **Redis**: Redlock algorithm, redis-py, ioredis.
- **Consul / Etcd**: Distributed Sessions and Key-Value Leases with Raft consensus.

## 12. Deliverables & Output Artifacts
- Module quản lý Distributed Lock & Lease có tích hợp Fencing Token.
- Lua script giải phóng và gia hạn khóa nguyên tử.
- Bộ kiểm thử giả lập lỗi GC pause và network split-brain.

## 13. Related & Complementary Skills
dex-concurrency-state, dex-distributed-consistency, dex-clock-skew-resilience

## 14. Realistic Usage Example
```powershell
# Chạy bộ kiểm thử tính an toàn của Distributed Lock khi gặp kịch bản timeout
pytest tests/distributed/test_distributed_locks.py -v
```
