---
name: dex-consumer-lag-control
description: Monitor, analyze, and mitigate streaming consumer lag with adaptive backpressure, partition rebalancing, and lag-driven autoscaling. Use when maintaining sub-second streaming SLAs across Kafka, Pulsar, or Kinesis pipelines.
---

# dex-consumer-lag-control

## 1. Purpose & Scope
Giám sát, phân tích và kiểm soát độ trễ của Consumer trong các đường ống dữ liệu phân tán (Consumer Lag Control trên Kafka, Pulsar, Kinesis); thiết lập cơ chế điều tiết áp lực ngược (adaptive backpressure), tối ưu hóa tái cân bằng partition (partition rebalancing) và tự động mở rộng quy mô (Autoscaling) dựa trên tốc độ tích lũy backlog.

## 2. When to Use
- Khi lưu lượng sự kiện đầu vào tăng đột biến trong các đợt flash sale khiến consumer không xử lý kịp và tạo ra backlog hàng triệu tin nhắn.
- Khi hệ thống có cam kết thỏa thuận mức dịch vụ (SLA) về độ trễ xử lý dữ liệu tính theo thời gian thực (dưới 500ms).
- Khi các consumer gặp sự cố 'Stop-The-World' do Rebalance kéo dài làm gián đoạn toàn bộ luồng đọc dữ liệu.

## 3. When NOT to Use
- Khi ứng dụng chỉ xử lý các hàng đợi batch đơn giản không đòi hỏi ràng buộc về thời gian thực.
- Khi hệ thống chỉ có một partition duy nhất và không thể mở rộng quy mô đọc song song.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Broker streaming (Kafka, Pulsar), công cụ đo lag (Burrow, Kafka Exporter), hệ thống tự động co giãn pods (KEDA / HPA trên Kubernetes).
- **Quyền hạn truy cập:** Quyền theo dõi consumer group offsets và cấu hình HPA trên Kubernetes cluster.

## 5. Core Concepts & Taxonomy
- **Consumer Lag:** Khoảng cách giữa offset của thông điệp mới nhất được ghi vào partition (Log End Offset) và offset của thông điệp gần nhất mà Consumer Group đã commit (Current Offset).
- **Cooperative Sticky Rebalance:** Cơ chế tái phân bổ partition mới của Kafka giúp tránh hiện tượng dừng toàn bộ các consumers (Stop-the-world) trong khi rebalance.
- **Lag-Driven Scaling:** Tự động tăng số lượng consumer replicas dựa trên tổng lượng lag hoặc tốc độ tăng trưởng của backlog (sử dụng Kubernetes KEDA).

## 6. Step-by-Step Execution Workflow
1. Xuất các chỉ số độ trễ chi tiết theo từng partition: `kafka_consumergroup_lag` và `kafka_consumergroup_lag_seconds` vào Prometheus.
2. Cấu hình consumer sử dụng giao thức `CooperativeStickyAssignor` để loại bỏ thời gian chết do rebalancing.
3. Thiết lập cơ chế xử lý theo batch và song song hóa xử lý bên trong consumer bằng worker thread pool trước khi commit offset.
4. Cài đặt KEDA ScaledObject trên Kubernetes tự động tăng số lượng consumer pods tương ứng khi lag vượt ngưỡng 10,000 messages.
5. Tích hợp cơ chế Backpressure: khi downstream database bị nghẽn, consumer tự động giảm tần suất poll hoặc tạm dừng nhận tin (`pause()`) để bảo vệ database.

## 7. Concrete Examples
### Ví dụ cấu hình Kubernetes KEDA ScaledObject tự động co giãn theo Kafka Lag:
```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: order-consumer-scaler
  namespace: streaming
spec:
  scaleTargetRef:
    name: order-processing-consumer
  minReplicaCount: 2
  maxReplicaCount: 16 # Bằng tổng số partitions của Kafka topic
  pollingInterval: 15
  cooldownPeriod: 300
  triggers:
    - type: kafka
      metadata:
        bootstrapServers: kafka-cluster.internal:9092
        consumerGroup: order-consumer-group
        topic: orders.v1
        lagThreshold: "2500" # Tăng 1 pod cho mỗi 2500 messages tồn đọng
        activationLagThreshold: "50"
```

## 8. Anti-Patterns & Common Traps
- **Scaling Beyond Partition Count:** Tăng số lượng consumer pods nhiều hơn số lượng partition của topic, khiến các pods dư thừa bị rảnh rỗi 100% không nhận được partition nào.
- **Synchronous Heavy I/O in Poll Loop:** Thực hiện các cuộc gọi API chậm chạp bên trong luồng `poll()`, khiến consumer bị broker coi là đã chết (vượt quá `max.poll.interval.ms`) và kích hoạt rebalance liên tục.
- **Blind Commit Without Processing:** Tự động commit offset ngay khi vừa đọc được tin nhắn trước khi xử lý xong, dẫn tới mất dữ liệu hoàn toàn khi consumer bị sập.

## 9. Quality Gates & Acceptance Criteria
- **QG-03**: Thời gian phục hồi độ trễ (drain backlog) sau đợt tăng tải đột biến được chứng minh bằng kiểm thử tải thực tế.
- **QG-07**: Độ trễ trung bình của consumer duy trì dưới 500ms trong điều kiện tải bình thường.
- **QG-10**: Khi một consumer node bị crash, các partition còn lại được phân bổ lại trong dưới 3 giây mà không làm gián đoạn các nodes khác.

## 10. Security & Safety Boundaries
- Sử dụng chứng thực mTLS và SASL/SCRAM để bảo vệ kết nối giữa Consumer và Kafka Broker.
- Phân quyền ACL tối thiểu chỉ cho phép consumer group đọc dữ liệu trên đúng topic được chỉ định.

## 11. Platform Adapters
- **Streaming**: Apache Kafka, Apache Pulsar, AWS Kinesis.
- **Orchestration**: Kubernetes KEDA (Kubernetes Event-driven Autoscaling), Prometheus.

## 12. Deliverables & Output Artifacts
- Cấu hình tối ưu hóa Consumer Group và cơ chế Cooperative Rebalance.
- Tệp cấu hình KEDA ScaledObject tự động co giãn theo độ trễ.
- Dashboard Grafana giám sát Consumer Lag theo từng partition.

## 13. Related & Complementary Skills
dex-traffic-shaping-backpressure, dex-load-and-stress-testing, dex-stream-processing-semantics

## 14. Realistic Usage Example
```powershell
# Kiểm tra độ trễ consumer lag hiện tại trên Kafka cluster
kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group order-consumer-group
```
