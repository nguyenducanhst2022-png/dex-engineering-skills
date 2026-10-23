---
name: dex-hot-partition-mitigation
description: Detect and mitigate hot partition key skew using synthetic salting, compound keys, and adaptive sharding. Use when streaming or storage partitions suffer from severe resource saturation due to skewed data distributions.
---

# dex-hot-partition-mitigation

## 1. Purpose & Scope
Phát hiện và giảm thiểu hiện tượng lệch tải phân vùng (Hot Partition / Key Skew) trong hệ thống lưu trữ và streaming phân tán; áp dụng kỹ thuật gieo muối nhân tạo (synthetic salting), khóa phân vùng kết hợp (compound partition keys), và phân mảnh thích ứng nhằm phân bổ tải đều lên toàn bộ các máy chủ trong cụm.

## 2. When to Use
- Khi một partition đơn lẻ trong Kafka topic hoặc DynamoDB/Cassandra table bị quá tải CPU/IOPS trong khi các partition khác hầu như nhàn rỗi.
- Khi hệ thống có các đối tượng 'người nổi tiếng' (Celebrity problem / High-cardinality skew) như tài khoản có hàng triệu followers hoặc sản phẩm flash sale tạo ra 80% lưu lượng ghi.
- Khi xảy ra hiện tượng throttling hoặc tăng độ trễ p99 do nghẽn tại một điểm đơn lẻ trong cụm lưu trữ phân tán.

## 3. When NOT to Use
- Khi dữ liệu được phân bố đồng đều tự nhiên (ví dụ: sử dụng UUIDv4 ngẫu nhiên làm partition key).
- Khi bắt buộc phải bảo đảm thứ tự tuần tự tuyệt đối (Strict Global Ordering) cho toàn bộ các sự kiện của hệ thống.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Khóa phân vùng hiện tại (Partition Key), phân tích phân bố tần suất của khóa (Key Distribution Histogram), broker/database metrics theo từng partition.
- **Quyền hạn truy cập:** Quyền thay đổi logic sinh khóa phân vùng tại Producer và logic tổng hợp tại Consumer.

## 5. Core Concepts & Taxonomy
- **Hot Partition Skew:** Tình trạng mất cân bằng nghiêm trọng khi một partition phải tiếp nhận lượng dữ liệu lớn gấp nhiều lần mức trung bình do cùng một partition key.
- **Key Salting (Gieo muối):** Bổ sung một hậu tố ngẫu nhiên hoặc có chu kỳ (ví dụ: `account_id + '_' + random(1, 10)`) vào khóa phân vùng để phân tán dữ liệu sang 10 partitions khác nhau.
- **Scatter-Gather Read Pattern:** Khi truy vấn dữ liệu đã được gieo muối, tầng đọc sẽ phát lệnh đọc song song tới tất cả 10 partitions và hợp nhất kết quả lại.

## 6. Step-by-Step Execution Workflow
1. Đo lường phân bố lưu lượng theo từng partition trên Broker hoặc Cơ sở dữ liệu phân tán để xác định mức độ lệch tải (Gini coefficient hoặc Max/Avg ratio).
2. Nhận diện các khóa phân vùng có tần suất xuất hiện vượt quá 5% tổng lưu lượng ghi của hệ thống.
3. Triển khai thuật toán Dynamic Salting tại Producer: chỉ áp dụng gieo muối cho các khóa nằm trong danh sách 'hot keys', các khóa bình thường giữ nguyên.
4. Cải tiến Consumer / Query Engine theo mẫu Scatter-Gather: đọc song song từ các partitions con và tổng hợp lại kết quả.
5. Kiểm tra phân bố lại tải trên dashboard: bảo đảm độ lệch giữa partition cao nhất và trung bình không vượt quá 20%.
6. Tự động điều chỉnh số lượng muối (salt factor) dựa trên lưu lượng thực tế đo được.

## 7. Concrete Examples
### Ví dụ kỹ thuật Dynamic Key Salting trong Python Producer:
```python
import hashlib
import random

HOT_TENANTS = {"tenant_celebrity_01", "tenant_megacorp_99"}
SALT_BUCKETS = 8

def compute_partition_key(tenant_id: str, record_id: str) -> str:
    # 1. Nếu là tenant bình thường -> Dùng nguyên tenant_id để bảo toàn thứ tự cục bộ
    if tenant_id not in HOT_TENANTS:
        return tenant_id

    # 2. Nếu là Hot Tenant -> Gieo muối ngẫu nhiên (hoặc dựa trên hash của record_id)
    # để phân tán đều ra 8 partitions khác nhau, tránh nghẽn 1 partition đơn lẻ
    salt = random.randint(0, SALT_BUCKETS - 1)
    return f"{tenant_id}_salt_{salt}"

def scatter_gather_read_keys(tenant_id: str) -> list[str]:
    # Khi cần đọc toàn bộ dữ liệu của Hot Tenant: Đọc từ tất cả các buckets đã gieo muối
    if tenant_id not in HOT_TENANTS:
        return [tenant_id]
    return [f"{tenant_id}_salt_{i}" for i in range(SALT_BUCKETS)]
```

## 8. Anti-Patterns & Common Traps
- **Universal Over-Salting:** Gieo muối cho toàn bộ 100% các keys kể cả các keys lưu lượng nhỏ, làm tăng độ phức tạp và chi phí truy vấn đọc không cần thiết.
- **Loss of Ordering Guarantee:** Áp dụng gieo muối mà không tính đến việc các sự kiện phụ thuộc lẫn nhau của cùng một đơn hàng bị phân tán sang các partitions khác nhau làm mất thứ tự xử lý.
- **Static Salt Values:** Sử dụng số lượng muối cố định không thể thay đổi khi lượng truy cập của sự kiện tăng gấp 100 lần trong thực tế.

## 9. Quality Gates & Acceptance Criteria
- **QG-03**: Dashboard đo lường chứng minh độ chênh lệch tải giữa partition lớn nhất và nhỏ nhất giảm tối thiểu 60% sau khi áp dụng salting.
- **QG-07**: Tăng tải ghi lên 50,000 req/s mà không có partition nào bị kích hoạt cảnh báo throttling.
- **QG-09**: Logic truy vấn Scatter-Gather bảo đảm không bỏ sót bất kỳ bản ghi nào đã được ghi vào các partition muối.

## 10. Security & Safety Boundaries
- Sử dụng hàm băm an toàn và bộ sinh số ngẫu nhiên đáng tin cậy để tạo muối, tránh việc muối bị dự đoán trước trong các tấn công DoS nhằm vào một partition cụ thể.
- Phân quyền đồng nhất cho các partition con của cùng một dữ liệu khách hàng.

## 11. Platform Adapters
- **Storage**: DynamoDB Partition Keys, Cassandra Row Keys, Bigtable Row Keys.
- **Streaming**: Kafka Murmur2 Partitioner, Kinesis Hash Keys.

## 12. Deliverables & Output Artifacts
- Module Producer hỗ trợ Dynamic Key Salting.
- Logic Scatter-Gather Query Resolver cho tầng đọc.
- Biểu đồ phân tích độ lệch tải (Skewness Distribution Chart) trước và sau khi tối ưu.

## 13. Related & Complementary Skills
dex-consumer-lag-control, dex-database-query-plans, dex-load-and-stress-testing

## 14. Realistic Usage Example
```powershell
# Chạy phân tích độ lệch phân vùng của Kafka topic
python scripts/analyze_partition_skew.py --topic user_actions --window 1h
```
