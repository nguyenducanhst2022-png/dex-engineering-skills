---
name: dex-message-poison-queue-recovery
description: Architect dead-letter queues (DLQ), poison message triage workflows, bounded exponential backoff retries, and safe replay mechanisms. Use when handling malformed or unprocessable streaming messages without halting consumers.
---

# dex-message-poison-queue-recovery

## 1. Purpose & Scope
Thiết kế và quản trị hàng đợi thông điệp độc (Dead-Letter Queue - DLQ); cài đặt cơ chế thử lại có giới hạn với hàm mũ lùi (bounded exponential backoff), phân loại và cô lập thông điệp độc hại mà không làm tắc nghẽn toàn bộ hàng đợi của hệ thống, cùng công cụ phát lại an toàn (safe replay).

## 2. When to Use
- Khi consumer gặp phải thông điệp bị lỗi định dạng cú pháp (malformed JSON) hoặc vi phạm ràng buộc dữ liệu không thể xử lý thành công.
- Khi lỗi xảy ra liên tục khiến consumer bị crash lặp đi lặp lại (CrashLoopBackOff) làm nghẽn dòng thông điệp phía sau.
- Khi cần công cụ phân tích nguyên nhân gốc và phát lại các thông điệp đã sửa lỗi vào hàng đợi chính.

## 3. When NOT to Use
- Khi lỗi chỉ là lỗi tạm thời của mạng kết nối tới database có thể tự hết sau vài mili-giây (sử dụng in-memory retry ngắn).
- Khi hệ thống cho phép bỏ qua và loại bỏ thông điệp lỗi hoàn toàn mà không cần lưu vết kiểm toán.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Cấu hình Message Broker (Kafka, SQS, RabbitMQ), hàng đợi chính và hàng đợi phụ DLQ, chính sách retry tối đa (Max Deliveries).
- **Quyền hạn truy cập:** Quyền tạo hàng đợi DLQ và quyền di chuyển/phát lại thông điệp.

## 5. Core Concepts & Taxonomy
- **Poison Message:** Thông điệp gây ra lỗi không thể khắc phục mỗi khi được đọc, khiến consumer bị treo hoặc crash liên tục.
- **Dead-Letter Queue (DLQ):** Hàng đợi cách ly đặc biệt nơi các thông điệp đã thử lại vượt quá số lần cho phép (`max_retries`) được chuyển tới để phân tích thủ công.
- **Safe Redrive / Replay Tooling:** Quy trình kiểm duyệt, sửa đổi payload bị lỗi (nếu cần) và phát lại thông điệp từ DLQ vào hàng đợi chính có kiểm soát tốc độ.

## 6. Step-by-Step Execution Workflow
1. Thiết lập ngưỡng thử lại tối đa (ví dụ: `max_retries = 3`) và cấu hình DLQ tương ứng cho từng hàng đợi nghiệp vụ.
2. Cài đặt middleware bắt exception: phân biệt lỗi tạm thời (Transient error - retry với exponential backoff) và lỗi vĩnh viễn (Fatal error - đẩy ngay sang DLQ).
3. Đính kèm siêu dữ liệu chẩn đoán vào header của thông điệp khi đẩy sang DLQ: `x-exception-message`, `x-stack-trace`, `x-original-queue`, `x-failure-timestamp`.
4. Giám sát số lượng thông điệp trong DLQ và kích hoạt cảnh báo tới đội On-call khi số lượng thông điệp độc vượt ngưỡng 0.
5. Xây dựng CLI script hỗ trợ xem trước nội dung thông điệp trong DLQ và phát lại an toàn theo batch.

## 7. Concrete Examples
### Ví dụ xử lý poison message và đẩy sang DLQ an toàn trong Python:
```python
import json
import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)

def process_message_with_dlq(message: Dict[str, Any], broker_client) -> bool:
    max_retries = 3
    current_retries = message.get("headers", {}).get("retry_count", 0)

    try:
        # Giả lập xử lý nghiệp vụ
        payload = json.loads(message["body"])
        if "account_id" not in payload:
            raise ValueError("Malformed payload: Missing required account_id")
        
        execute_business_logic(payload)
        return True

    except Exception as exc:
        logger.error(f"Error processing message {message.get('id')}: {exc}")
        if current_retries < max_retries:
            # Thử lại có exponential backoff
            message.setdefault("headers", {})["retry_count"] = current_retries + 1
            broker_client.requeue_with_delay(message, delay_seconds=2 ** current_retries)
        else:
            # Vượt quá giới hạn -> Đẩy sang Dead Letter Queue
            dlq_message = {
                "original_message": message,
                "error_details": {
                    "exception_class": exc.__class__.__name__,
                    "error_message": str(exc),
                    "failed_at": "2026-10-22T00:00:00Z"
                }
            }
            broker_client.send_to_dlq(dlq_message)
            logger.critical(f"Poison message isolated into DLQ: {message.get('id')}")
        return False
```

## 8. Anti-Patterns & Common Traps
- **Infinite Retry Storm:** Thử lại thông điệp lỗi vĩnh viễn với tần suất liên tục không có backoff làm nghẽn CPU và tràn log.
- **Drop and Forget:** Bỏ qua thông điệp lỗi mà không lưu vào DLQ, dẫn tới mất mát dữ liệu khách hàng mà không ai hay biết.
- **Unbounded DLQ Accumulation:** Coi DLQ như một bãi rác và không bao giờ thiết lập cảnh báo hoặc quy trình xử lý định kỳ.

## 9. Quality Gates & Acceptance Criteria
- **QG-03**: Khi consumer gặp thông điệp độc, thông điệp được chuyển vào DLQ thành công và consumer tiếp tục xử lý các tin nhắn tiếp theo.
- **QG-06**: Header lỗi đính kèm trong DLQ không được chứa thông tin nhạy cảm hoặc mật khẩu.
- **QG-10**: Có kịch bản kiểm thử tự động chứng minh hàng đợi không bị nghẽn khi có 10% thông điệp độc hại.

## 10. Security & Safety Boundaries
- Giới hạn quyền truy cập vào DLQ vì payload trong DLQ có thể chứa các thông điệp lỗi mang dữ liệu nhạy cảm.
- Làm sạch dữ liệu trước khi phát lại để tránh việc đưa lại mã độc tấn công vào hệ thống chính.

## 11. Platform Adapters
- **AWS**: Amazon SQS Dead-Letter Queues with Redrive Policy.
- **RabbitMQ**: Dead Letter Exchanges (DLX) & x-dead-letter-routing-key.
- **Kafka**: Error-handling deserializer & Dead Letter Topic.

## 12. Deliverables & Output Artifacts
- Module Consumer bọc cơ chế xử lý Poison Message.
- Tệp cấu hình DLQ và Redrive Policy.
- CLI script hỗ trợ phân tích và phát lại thông điệp từ DLQ.

## 13. Related & Complementary Skills
dex-background-job-queues, dex-consumer-lag-control, dex-event-driven-architecture

## 14. Realistic Usage Example
```powershell
# Xem danh sách thông điệp trong DLQ và phát lại vào hàng đợi chính
python scripts/dlq_manager.py list --queue orders_dlq
python scripts/dlq_manager.py redrive --queue orders_dlq --limit 10
```
