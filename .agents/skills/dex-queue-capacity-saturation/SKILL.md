---
name: dex-queue-capacity-saturation
description: Model, monitor, and stress-test asynchronous message queue saturation (RabbitMQ, Kafka, SQS). Detect consumer lag, head-of-line blocking, and configure KEDA auto-scaling.
---

# dex-queue-capacity-saturation

## 1. Purpose & Scope
Mô hình hóa, giám sát và kiểm thử độ bão hòa tải của hệ thống hàng đợi thông điệp bất đồng bộ (Message Queue Capacity & Saturation: Apache Kafka, RabbitMQ, AWS SQS); phát hiện sớm hiện tượng tích tụ độ trễ tiêu thụ (Consumer Lag), tắc nghẽn đầu hàng đợi (Head-of-Line Blocking) và tràn bộ đệm thư chết (Dead-Letter Queue - DLQ); cấu hình cơ chế tự động co giãn quy mô worker dựa trên sự kiện (Event-Driven Auto-scaling với KEDA) và thiết lập các biện pháp kiểm soát áp lực ngược (Backpressure).

## 2. When to Use
- Khi hệ thống xử lý tác vụ nền gặp hiện tượng chậm trễ xử lý đơn hàng, gửi email hoặc phân tích dữ liệu trong các đợt cao điểm khuyến mãi.
- Khi số lượng thông điệp chưa xử lý trong hàng đợi tăng trưởng đột biến nhưng số lượng worker không tự động tăng tương ứng.
- Khi thiết lập các ngưỡng cảnh báo bão hòa dung lượng đĩa và bộ nhớ RAM của cụm máy chủ message broker.

## 3. When NOT to Use
- Khi các yêu cầu được xử lý đồng bộ thời gian thực thông qua REST API hoặc gRPC không có hàng đợi trung gian.
- Khi khối lượng tác vụ quá nhỏ (<10 thông điệp/phút) không bao giờ chạm tới giới hạn tài nguyên của broker.

## 4. Prerequisites & Input Context
- **Hạ tầng hàng đợi:** Cụm RabbitMQ, Kafka hoặc AWS SQS đang hoạt động.
- **Công cụ đo kiểm:** Prometheus exporter cho hàng đợi (`rabbitmq_exporter`, `kafka_exporter`) và KEDA cài trên Kubernetes.

## 5. Core Concepts & Taxonomy
- **Consumer Lag:** Khoảng cách giữa offset của thông điệp mới nhất được ghi vào hàng đợi và offset của thông điệp mà consumer đang xử lý.
- **Head-of-Line Blocking:** Hiện tượng một thông điệp bị lỗi liên tục thất bại và retry chặn đứng toàn bộ các thông điệp hợp lệ phía sau nó.
- **KEDA (Kubernetes Event-driven Autoscaling):** Bộ điều phối tự động tăng số lượng Pod worker từ 0 lên N dựa trên độ sâu của hàng đợi (Queue Depth / Lag Metric).

## 6. Step-by-Step Execution Workflow
1. Khảo sát thông lượng sản xuất (Producer Throughput) và thông lượng tiêu thụ tối đa của một worker (Consumer Capacity).
2. Thiết lập đối tượng `ScaledObject` trong KEDA gắn với độ sâu hàng đợi mục tiêu (Target Queue Length, ví dụ: 30 thông điệp / 1 worker).
3. Thực hiện bài kiểm thử ép tải (Stress Test) bằng công cụ sinh tải đẩy hàng triệu thông điệp vào hàng đợi trong 5 phút.
4. Quan sát tốc độ co giãn của cụm worker và biểu đồ Consumer Lag trong Prometheus.
5. Kiểm tra cơ chế định tuyến thông điệp lỗi: sau 3 lần retry thất bại, thông điệp phải được chuyển an toàn sang Dead-Letter Queue.
6. Xác nhận hệ thống hạ tải mượt mà (Scale Down) về mức cơ sở khi hàng đợi được giải phóng hoàn toàn.

## 7. Concrete Examples
### Cau hinh KEDA ScaledObject tu dong co gian Worker theo do sau hang doi RabbitMQ:
```yaml
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: order-processor-scaler
  namespace: processing
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: order-worker-deployment
  minReplicaCount: 2   # Duy tri toi thieu 2 worker san sang
  maxReplicaCount: 30  # Cho phep mo rong toi da 30 worker khi qua tai
  cooldownPeriod: 300  # Cho 5 phut sau khi hang doi trong moi giam pod
  triggers:
    - type: rabbitmq
      metadata:
        protocol: amqp
        queueName: orders_v1_queue
        mode: QueueLength
        value: "50" # Moi 50 message ton dong se them 1 worker pod
      authenticationRef:
        name: keda-rabbitmq-auth
```

## 8. Anti-Patterns & Common Traps
- **Unbounded Message Retries Without Backoff:** Cho phép worker retry vô tận một thông điệp lỗi mà không đẩy sang DLQ khiến toàn bộ hàng đợi bị tắc nghẽn vĩnh viễn.
- **Aggressive Scale Down (Thrashing):** Đặt thời gian cooldown co cụm quá ngắn khiến các worker liên tục bị tạo mới rồi lại bị hủy (Flapping/Thrashing) tốn tài nguyên hệ thống.
- **Unmonitored Dead-Letter Queues:** Tạo hàng đợi thư chết DLQ nhưng không có hệ thống cảnh báo, khiến hàng nghìn đơn hàng lỗi tích tụ âm thầm mà không ai hay biết.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Hệ thống kích hoạt co giãn worker (Scale Out) trong vòng 30 giây khi độ sâu hàng đợi vượt ngưỡng quy định.
- **QG-02**: 100% thông điệp lỗi được chuyển về Dead-Letter Queue sau đúng 3 lần retry có exponential backoff.
- **QG-03**: Bộ nhớ RAM và đĩa cứng của cụm Message Broker không bao giờ vượt quá 80% công suất trong bài kiểm thử ép tải.

## 10. Security & Safety Boundaries
- Bắt buộc mã hóa luồng truyền tải thông điệp bằng TLS (mTLS); kiểm soát phân quyền đọc/ghi từng Topic/Queue bằng ACL.

## 11. Platform Adapters
- **Runtimes**: KEDA, RabbitMQ, Apache Kafka, AWS SQS, Prometheus.

## 12. Deliverables & Output Artifacts
- Tệp định nghĩa co giãn sự kiện tự động (`keda_queue_scaler.yaml`).
- Báo cáo phân tích năng lực chịu tải và độ bão hòa hàng đợi (`queue_saturation_report.md`).

## 13. Related & Complementary Skills
dex-api-circuit-breaker-verification, dex-release-progressive-metrics, dex-operational-dependency-mapping

## 14. Realistic Usage Example
```bash
# Kiem tra consumer lag cua Kafka Consumer Group bang kafka CLI
kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group order-processors
```
