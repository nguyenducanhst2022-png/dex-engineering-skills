---
name: dex-distributed-tracing
description: Implement distributed tracing using OpenTelemetry (OTel), W3C tracecontext propagation, span lifecycle instrumentation, baggage attributes, and bottleneck latency analysis. Use when diagnosing latency issues across microservices.
---

# dex-distributed-tracing

## 1. Purpose & Scope
Hiện thực hóa hệ thống truy vết phân tán (Distributed Tracing) đạt chuẩn công nghiệp OpenTelemetry (OTel); cấu hình lan truyền ngữ cảnh vết (W3C TraceContext: `traceparent`, `tracestate`), quản lý vòng đời Spans, gắn nhãn dữ liệu ngữ cảnh (Span Attributes, Events, Baggage), tích hợp exporter gửi dữ liệu về Jaeger / Tempo / OTel Collector và phân tích định lượng các điểm nghẽn độ trễ (Latency Bottlenecks) xuyên suốt hàng chục microservice.

## 2. When to Use
- Khi một request của người dùng đi qua chuỗi nhiều microservice và bị chậm mà không rõ dịch vụ nào gây nghẽn.
- Khi mã lỗi xuất hiện ở service cuối nhưng không thể truy ngược lại nguồn gốc request ban đầu từ phía client.
- Khi chuẩn hóa việc quan sát (Observability) cho toàn bộ hệ sinh thái dịch vụ đa ngôn ngữ.

## 3. When NOT to Use
- Ứng dụng đơn khối (Monolith) chạy trong 1 process duy nhất (dùng profiler nội bộ trong `dex-performance-optimization`).
- Thu thập log văn bản thuần túy không có trace ID liên kết (dùng `dex-production-monitoring`).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Ngôn ngữ và runtime của các service (Node.js, Go, Python, Java).
- Giao thức truyền thông giữa các service (HTTP/REST, gRPC, Kafka/RabbitMQ message headers).
- Địa chỉ endpoint của OpenTelemetry Collector (OTLP gRPC/HTTP).
- **Điều kiện tiên quyết**:
- OpenTelemetry SDK và instrumentation packages phù hợp được tích hợp.
- Hệ thống lưu trữ và giao diện hiển thị Trace (Jaeger, Grafana Tempo, Datadog) sẵn sàng.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- **W3C TraceContext Standard**: Chuẩn header HTTP `traceparent: 00-{trace_id}-{span_id}-{trace_flags}` đảm bảo trace ID duy nhất được truyền xuyên suốt qua mọi biên giới mạng.
- **Trace Tree & Spans**: Một Trace đại diện cho toàn bộ hành trình của request; mỗi Span đại diện cho một đơn vị công việc có thời gian bắt đầu, kết thúc, trạng thái và metadata.
- **Context Propagation In Message Queues**: Khi gửi message vào Kafka/RabbitMQ, trace context phải được inject vào message headers/properties và extract ra khi worker tiêu thụ.
- **Quy tắc quyết định kỹ thuật**:
- **Bắt Buộc Lan Truyền Context (Propagate Context)**: Mọi HTTP client và gRPC stub đều phải đính kèm header `traceparent` khi gọi downstream.
- **Không Tạo Quá Nhiều Span Con Nhỏ Vụn**: Tránh tạo span cho các hàm nội bộ chạy dưới 1ms; tập trung vào ranh giới I/O (Database, Cache, Network, File system).
- **Bảo Vệ Quyền Riêng Tư (PII Sanitization)**: Tuyệt đối không đưa mật khẩu, token, thông tin thẻ tín dụng vào Span Attributes.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Trace bị đứt đoạn (Broken Trace)**: Một microservice ở giữa không truyền `traceparent` sang service tiếp theo -> Khắc phục: Sử dụng OpenTelemetry auto-instrumentation hoặc inject context rõ ràng vào outbound headers.
- **Hệ thống bị quá tải vì lưu lượng trace quá lớn**: Do cấu hình sampling rate 100% trong production có hàng triệu req/s -> Khắc phục: Áp dụng Head-based hoặc Tail-based Sampling (ví dụ: chỉ lưu 5% trace thành công và 100% trace có lỗi hoặc latency cao).

## 6. Step-by-Step Execution Workflow
1. Khởi tạo OpenTelemetry TracerProvider và cấu hình OTLP Exporter gửi dữ liệu về OTel Collector.
2. Cài đặt auto-instrumentation cho HTTP framework (Express, Gin, FastAPI) và Database drivers.
3. Thiết lập W3C TraceContext Propagator làm chuẩn mặc định trong ứng dụng.
4. Tạo manual span cho các tác vụ nghiệp vụ quan trọng: `tracer.startActiveSpan(...)`.
5. Đính kèm các attribute chuẩn semantic conventions (`http.status_code`, `db.system`, `user.id`).
6. Bắt và ghi nhận ngoại lệ vào Span: `span.recordException(err)` và đặt trạng thái `SpanStatusCode.ERROR`.
7. Truy vấn Jaeger / Tempo phân tích waterfall chart xác định dịch vụ chiếm nhiều thời gian nhất.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```go
package main

import (
	"context"
	"go.opentelemetry.io/otel"
	"go.opentelemetry.io/otel/attribute"
	"go.opentelemetry.io/otel/codes"
	"go.opentelemetry.io/otel/trace"
)

var tracer = otel.Tracer("order-service")

func ProcessOrder(ctx context.Context, orderID string) error {
	// Bắt đầu một Span mới liên kết với context truyền vào
	ctx, span := tracer.Start(ctx, "ProcessOrder",
		trace.WithAttributes(attribute.String("order.id", orderID)),
	)
	defer span.End()

	if err := chargePayment(ctx, orderID); err != nil {
		span.RecordError(err)
		span.SetStatus(codes.Error, err.Error())
		return err
	}

	span.SetStatus(codes.Ok, "Order processed successfully")
	return nil
}
```

### Lệnh xác minh & thực thi:
- Kiểm tra header traceparent trên request outbound: `curl -v -H "traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01" http://localhost:8080/order`
- Kiểm tra kết nối tới OTel Collector: `nc -zv otel-collector 4317`
- Truy vấn Jaeger API xác minh Trace tồn tại: `curl http://jaeger:16686/api/traces/<trace-id>`

## 8. Anti-Patterns & Common Traps
- **Bỏ rơi context trong Goroutine / Async Thread**: Gọi hàm bất đồng bộ mà truyền `context.Background()` thay vì truyền context của request, làm đứt trace tree.
- **Ghi đè Trace ID**: Tự ý sinh UUID mới thay vì kế thừa Trace ID nhận được từ header.
- **Lạm dụng Baggage**: Truyền lượng dữ liệu quá lớn qua HTTP headers làm tràn giới hạn header của reverse proxy.

## 9. Quality Gates & Acceptance Criteria
- QG-01: 100% các request xuyên suốt hệ thống đều duy trì một Trace ID duy nhất không bị đứt đoạn.
- QG-07: Không có thông tin nhạy cảm (PII) trong Span attributes.
- QG-10: Tỷ lệ lấy mẫu (Sampling rate) được cấu hình thích ứng, không làm tăng CPU ứng dụng quá 2%.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi deploy.

## 10. Security & Safety Boundaries
- Lọc bỏ thông tin xác thực (`Authorization` header) trước khi đưa vào span metadata.
- Cấu hình TLS khi truyền dữ liệu OTLP giữa ứng dụng và collector.
- Không bao giờ lưu trữ hardcoded secret hoặc cấp quyền quá mức (over-permissioned IAM).

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Môi trường Cloud & Container**: Hỗ trợ Docker, Kubernetes (EKS/GKE/AKS), Terraform/OpenTofu, OpenTelemetry.

## 12. Deliverables & Output Artifacts
- Module OpenTelemetry bootstrap và instrumentation chuẩn hóa.
- Sơ đồ tương tác dịch vụ và biểu đồ phân tích thời gian (Waterfall chart) trên Jaeger/Tempo.
- Dashboard độ trễ theo từng bước xử lý nghiệp vụ.

## 13. Related & Complementary Skills
- `dex-ai-observability`: Mở rộng tracing cho các tác vụ gọi LLM và sinh vector.
- `dex-performance-optimization`: Sử dụng dữ liệu trace để tối ưu hóa code tại điểm nghẽn.
- `dex-slo-error-budgets`: Đo lường Latency SLI dựa trên span durations.

## 14. Realistic Usage Example
### Tình huống thực tế:
Một request API checkout mất 4.2 giây mới hoàn thành. Sử dụng `dex-distributed-tracing`, kỹ sư mở Jaeger UI xem waterfall trace của đơn hàng. Biểu đồ chỉ ra rằng trong 4.2 giây, có tới 3.8 giây bị tiêu tốn tại Inventory Service do lặp N+1 query kiểm tra tồn kho trong vòng lặp. Nhờ trace span chi tiết, kỹ sư xác định chính xác vị trí cần gom batch query, rút ngắn latency xuống còn 180ms.
