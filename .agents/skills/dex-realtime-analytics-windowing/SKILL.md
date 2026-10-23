---
name: dex-realtime-analytics-windowing
description: Design and tune streaming window aggregations including tumbling, hopping, sliding, and session windows with watermarking for late-arriving event processing. Use when engineering robust stream processing and operational telemetry pipelines.
---

# dex-realtime-analytics-windowing

## 1. Purpose & Scope
Thiết kế, tinh chỉnh và kiểm chứng các cơ chế gom nhóm cửa sổ thời gian thực (Streaming Window Aggregations) bao gồm Tumbling, Hopping, Sliding, và Session Windows; áp dụng kỹ thuật đánh dấu mốc thời gian (Watermarking) để xử lý hoàn hảo dữ liệu đến muộn (Late-Arriving Events).

## 2. When to Use
- Khi xây dựng hệ thống phát hiện gian lận thanh toán (ví dụ: phát hiện 5 giao dịch trong vòng 1 phút từ các vị trí địa lý khác nhau).
- Khi tổng hợp số liệu đo lường theo dõi (Metrics Aggregation) từ hàng triệu thiết bị IoT theo cửa sổ thời gian trượt.
- Khi các sự kiện mạng bị trễ do mất sóng di động và gửi về máy chủ sau vài phút đến vài giờ.

## 3. When NOT to Use
- Khi dữ liệu chỉ cần tổng hợp tĩnh cuối ngày bằng batch job SQL truyền thống trong Data Warehouse.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Nguồn dữ liệu streaming (Kafka, Kinesis, Redpanda), công cụ xử lý dòng (Apache Flink, Spark Streaming, Faust).
- **Quyền hạn truy cập:** Quyền quản lý consumer group và triển khai job streaming.

## 5. Core Concepts & Taxonomy
- **Event Time vs. Processing Time:** Xử lý dữ liệu dựa trên thời gian sự kiện thực tế xảy ra tại thiết bị client (Event Time) thay vì thời gian máy chủ nhận được dữ liệu (Processing Time).
- **Watermarks:** Mốc thời gian báo hiệu cho engine biết rằng mọi sự kiện trước mốc $t$ được coi như đã đến đủ, cho phép chốt kết quả cửa sổ tính toán.
- **Allowed Lateness & Side Outputs:** Cơ chế cho phép chấp nhận các sự kiện đến muộn trong một khoảng thời gian bổ sung và đẩy vào nhánh phụ để cập nhật lại kết quả.

## 6. Step-by-Step Execution Workflow
1. Xác định loại cửa sổ phù hợp với nghiệp vụ: Tumbling (không giao thoa), Hopping (giao thoa cố định), hoặc Session (dựa trên khoảng lặng tương tác).
2. Cấu hình bộ trích xuất Event Time từ trường timestamp của bản tin Kafka.
3. Thiết lập chiến lược sinh Watermark có tính đến độ trễ dự kiến (ví dụ: `forBoundedOutOfOrderness(Duration.ofSeconds(10))` phán đoán trễ tối đa 10s).
4. Định nghĩa hàm tổng hợp gia tăng (Incremental AggregateFunction) để tiết kiệm bộ nhớ trạng thái (State).
5. Cấu hình cơ chế Allowed Lateness và cổng xả sự kiện quá muộn (Side Output Dead-Letter Queue).
6. Kiểm thử dòng dữ liệu với kịch bản các bản tin bị đảo lộn thứ tự và trễ thời gian để xác thực độ chính xác số liệu.

## 7. Concrete Examples
### Cấu hình Windowing và Watermark trong Apache Flink (Java / Python PyFlink):
```python
from pyflink.common import WatermarkStrategy, Duration, Time
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.window import TumblingEventTimeWindows

env = StreamExecutionEnvironment.get_execution_environment()

# Thiet lap Watermark chap nhan tre toi da 5 giay
watermark_strategy = WatermarkStrategy.for_bounded_out_of_orderness(
    Duration.of_seconds(5)
).with_timestamp_assigner(lambda event, timestamp: event["event_time"])

stream = env.from_source(kafka_source, watermark_strategy, "KafkaSource")

# Gom nhom cua so Tumbling 1 phut dua tren Event Time
windowed_stream = stream \
    .key_by(lambda event: event["user_id"]) \
    .window(TumblingEventTimeWindows.of(Time.minutes(1))) \
    .allowed_lateness(Time.seconds(30)) \
    .aggregate(TransactionSumAggregate())

windowed_stream.print()
```

## 8. Anti-Patterns & Common Traps
- **Relying on Processing Time for Business Logic:** Sử dụng thời gian của máy chủ làm sai lệch hoàn toàn thống kê khi mạng gặp sự cố nghẽn kết nối.
- **Zero Tolerance Watermarks:** Đóng cửa sổ ngay lập tức khiến toàn bộ dữ liệu đến trễ vài mili-giây bị loại bỏ làm mất mát số liệu.
- **Unbounded Session Inactivity Gap:** Đặt thời gian chờ phiên quá lớn khiến trạng thái (State) của session không bao giờ được giải phóng gây tràn RAM RocksDB.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: 100% các phép tính toán nghiệp vụ tài chính/giao dịch đều dựa trên Event Time.
- **QG-04**: Các sự kiện đến muộn trong ngưỡng cho phép (Allowed Lateness) được cập nhật chính xác vào kết quả tổng hợp.
- **QG-08**: Bộ nhớ State của streaming job ổn định, không bị rò rỉ bộ nhớ sau 72 giờ vận hành liên tục.

## 10. Security & Safety Boundaries
- Đảm bảo tính toán toàn vẹn dữ liệu và mã hóa kênh truyền Kafka/Flink trong suốt quá trình xử lý dòng.

## 11. Platform Adapters
- **Engines**: Apache Flink, Spark Structured Streaming, Kafka Streams, RisingWave, Bytewax.

## 12. Deliverables & Output Artifacts
- Kịch bản Stream Processing tích hợp cơ chế Watermark.
- Cấu hình quản lý State và cơ chế xử lý dữ liệu trễ.
- Bộ kiểm thử giả lập dòng sự kiện xáo trộn thời gian.

## 13. Related & Complementary Skills
dex-consumer-lag-control, dex-event-replay-safety, dex-batch-inference-pipeline-tuning

## 14. Realistic Usage Example
```powershell
# Chạy Flink Job xử lý dòng sự kiện
flink run -m localhost:8081 -py streaming_window_job.py

# Giả lập gửi sự kiện trễ vào Kafka topic để test Watermark
python scripts/simulate_late_events.py --topic transactions --delay-sec 15
```
