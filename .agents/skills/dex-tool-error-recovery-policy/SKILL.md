---
name: dex-tool-error-recovery-policy
description: Classify tool-calling failures, implement bounded exponential backoff, define graceful fallback policies, and prevent repetitive destructive retries. Use when building robust, fault-tolerant autonomous agent loops.
---

# dex-tool-error-recovery-policy

## 1. Purpose & Scope
Phân loại các lỗi phát sinh khi gọi công cụ (Tool Execution Errors); xây dựng cơ chế phục hồi lỗi có hệ thống (Error Recovery Policy); áp dụng cơ chế thử lại có giới hạn kèm độ trễ hàm mũ (Bounded Exponential Backoff with Jitter); định nghĩa các lộ trình công cụ thay thế (Graceful Fallback Paths); và ngăn chặn hành vi thử lại mù quáng gây phá hoại dữ liệu.

## 2. When to Use
- Khi các công cụ phụ thuộc vào kết nối mạng, API bên ngoài hoặc dịch vụ cơ sở dữ liệu có khả năng gặp lỗi tạm thời (Transient Errors).
- Khi agent nhận được lỗi quyền hạn (Permission Denied) hoặc lỗi cú pháp và cần được hướng dẫn điều chỉnh hành vi thay vì retry liên tục.
- Khi xây dựng hệ thống agent vận hành tự động không có con người giám sát trực tiếp 24/7.

## 3. When NOT to Use
- Khi lỗi xuất phát từ vi phạm chính sách an toàn nghiêm trọng (Security Policy Violation) bắt buộc phải dừng ngay lập tức.
- Khi tác vụ là một chuỗi xử lý cứng nhắc không cho phép bất kỳ sự suy thoái hay phương án thay thế nào.

## 4. Prerequisites & Input Context
- **Mã lỗi và phản hồi:** Khả năng thu thập mã lỗi (`exit_code`, HTTP status) và thông báo lỗi chi tiết từ công cụ.
- **Hệ thống phân loại:** Bảng quy tắc phân loại lỗi thành 3 nhóm: Transient (Tạm thời), Correctable (Có thể sửa được), và Fatal (Bất khả kháng).

## 5. Core Concepts & Taxonomy
- **Transient vs Correctable vs Fatal Errors:**
  - *Transient:* Lỗi mạng, 429 Rate Limit, 503 Service Unavailable -> Cần Retry có backoff.
  - *Correctable:* Lỗi sai đường dẫn tệp, sai kiểu dữ liệu tham số -> Agent đọc lỗi và tự sửa tham số ở bước kế tiếp.
  - *Fatal:* 401 Unauthorized, Lệnh cấm, Filesystem Read-Only -> Dừng ngay lập tức, không được retry.
- **Fallback Tool Chain:** Nếu công cụ chính bị lỗi, agent được phép chuyển sang công cụ dự phòng (ví dụ: `fetch_webpage` bị chặn Cloudflare -> chuyển sang dùng `search_cached_snippet`).
- **Error Feedback Sanitization:** Định dạng lại thông báo lỗi trả về cho LLM sao cho ngắn gọn, chỉ ra đúng nguyên nhân cần khắc phục thay vì nhồi toàn bộ 50 dòng stack trace gây tràn context.

## 6. Step-by-Step Execution Workflow
1. Khi công cụ trả về kết quả lỗi: Bộ chặn lỗi (Error Interceptor) phân tích mã lỗi và nội dung phản hồi.
2. Xác định nhóm lỗi tương ứng (Transient, Correctable, Fatal).
3. Nếu là Fatal Error: Ngắt tiến trình và thông báo rõ nguyên nhân không thể khắc phục.
4. Nếu là Transient Error: Áp dụng thuật toán thử lại tối đa 3 lần với khoảng thời gian chờ tăng dần: $t = 2^{attempt} + jitter$.
5. Nếu là Correctable Error: Rút gọn thông báo lỗi thành gợi ý hành động cụ thể và gửi lại cho LLM (ví dụ: *"Lỗi: Tệp 'src/utils.py' không tồn tại. Hãy dùng tool 'list_directory' để kiểm tra lại đường dẫn đúng."*).
6. Đếm số lần gặp lỗi liên tiếp; nếu vượt quá 4 lần thử sửa không thành công, chuyển sang cơ chế dừng an toàn.

## 7. Concrete Examples
### Module xử lý lỗi và định hình thông báo phản hồi cho Agent:
```python
import time
import random
from typing import Dict, Any, Tuple

class ToolErrorPolicy:
    MAX_TRANSIENT_RETRIES = 3

    @staticmethod
    def handle_error(tool_name: str, error: Exception, attempt: int) -> Tuple[str, bool]:
        err_msg = str(error)

        # 1. Nhom loi Bat kha khang (Fatal)
        if "Permission denied" in err_msg or "401" in err_msg:
            return f"FATAL_ERROR: Khong co quyen thuc thi '{tool_name}'. Dung ngay lap tuc.", False

        # 2. Nhom loi Tam thoi (Transient)
        if "429" in err_msg or "Timeout" in err_msg or "Connection refused" in err_msg:
            if attempt < ToolErrorPolicy.MAX_TRANSIENT_RETRIES:
                sleep_time = (2 ** attempt) + random.uniform(0.1, 0.5)
                time.sleep(sleep_time)
                return f"TRANSIENT_ERROR: Loi tam thoi. Dang thu lai lan {attempt + 1}...", True
            else:
                return f"TRANSIENT_EXHAUSTED: Da thu lai {attempt} lan nhung dich vu van loi.", False

        # 3. Nhom loi Co the sua duoc (Correctable)
        if "No such file or directory" in err_msg:
            return f"CORRECTABLE_ERROR: Duong dan khong hop le. Hay kiem tra lai cay thu muc truoc khi thu lai.", False

        return f"UNKNOWN_ERROR: {err_msg[:200]}", False
```

## 8. Anti-Patterns & Common Traps
- **Immediate Tight Retry Loops:** Thử lại liên tục ngay trong mili-giây khi gặp lỗi 429, dẫn đến việc bị nhà cung cấp dịch vụ khóa IP vĩnh viễn.
- **Hiding Errors from the Agent:** Nuốt lỗi và trả về chuỗi rỗng cho LLM, khiến agent tưởng rằng lệnh đã thành công và tiếp tục triển khai các bước sai lầm tiếp theo.
- **Infinite Retry on Missing Files:** Agent liên tục gọi lệnh đọc một tệp không tồn tại 20 lần mà không bao giờ kiểm tra lại xem tệp đó nằm ở đâu.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Số lần thử lại tối đa cho lỗi tạm thời không vượt quá 3 lần.
- **QG-02**: Mọi lỗi bất khả kháng (Fatal) đều ngắt vòng lặp thực thi ngay lập tức.
- **QG-03**: Thông báo lỗi trả về cho agent không chứa các chuỗi stack trace rác vượt quá 500 ký tự.

## 10. Security & Safety Boundaries
- Ngăn chặn agent tấn công từ chối dịch vụ (DoS) vào các API nội bộ và bảo vệ hệ sinh thái dịch vụ phụ trợ.

## 11. Platform Adapters
- **Frameworks**: Tenacity, Resilience4j, LangChain Fallbacks, Custom Tool Interceptors.

## 12. Deliverables & Output Artifacts
- Lớp chính sách phân loại và phục hồi lỗi công cụ (`tool_error_policy.py`).
- Bảng ma trận mã lỗi và hành vi ứng phó chuẩn (`error_action_matrix.json`).
- Bộ kiểm thử unit test giả lập các kịch bản lỗi mạng và lỗi cú pháp.

## 13. Related & Complementary Skills
dex-agent-execution-budget-controls, dex-agent-engineering, dex-resilience-circuit-breaker

## 14. Realistic Usage Example
```bash
# Chay kiem thu chinh sach phuc hoi loi cong cu
pytest tests/test_tool_error_recovery.py -v

# Theo doi ty le loi tool trong log thuc thi cua agent
grep -rn "CORRECTABLE_ERROR" logs/agent_execution.log
```
