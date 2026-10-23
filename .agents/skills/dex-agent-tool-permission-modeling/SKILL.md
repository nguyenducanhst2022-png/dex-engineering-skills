---
name: dex-agent-tool-permission-modeling
description: Model, enforce, and audit granular authorization scopes for autonomous AI coding agents. Classify tools into read-only, mutating, and destructive tiers, and enforce explicit human-in-the-loop approvals. Use when designing safe agentic tool-execution frameworks.
---

# dex-agent-tool-permission-modeling

## 1. Purpose & Scope
Thiết kế mô hình phân quyền chi tiết (Granular Authorization Scopes) cho các công cụ (Tools) mà tác nhân AI tự động có thể gọi; phân tầng công cụ theo 3 cấp độ rủi ro (Chỉ đọc, Thay đổi an toàn, và Phá hủy/Nguy hiểm); thiết lập các ngưỡng phê duyệt bắt buộc có sự tham gia của con người (Human-in-the-loop Approval Gates); và ghi nhận lịch sử kiểm toán thẩm quyền.

## 2. When to Use
- Khi xây dựng hoặc cấu hình các AI Coding Agents có khả năng thực thi lệnh terminal, sửa tệp hoặc gọi API bên ngoài.
- Khi cần ngăn chặn tác nhân AI tự ý chạy các lệnh nguy hiểm (như `git push --force`, `rm -rf`, `DROP TABLE`, sửa biến môi trường sản xuất).
- Khi thiết lập ranh giới an toàn cho các tác nhân tự động chạy ngầm trong doanh nghiệp.

## 3. When NOT to Use
- Khi tác nhân AI chỉ hoạt động ở chế độ trò chuyện thuần túy (Chatbot) không có bất kỳ khả năng Tool Calling nào.
- Khi hệ thống là một script tự động hóa truyền thống không sử dụng mô hình trí tuệ nhân tạo để ra quyết định.

## 4. Prerequisites & Input Context
- **Danh mục Tool Manifest:** Danh sách định nghĩa JSON Schema của toàn bộ các tool được cung cấp cho agent.
- **Cơ chế Runtime Interceptor:** Khả năng chặn bắt lệnh gọi tool trước khi chuyển tiếp tới hệ điều hành hoặc hệ thống mạng.

## 5. Core Concepts & Taxonomy
- **Tiered Tool Classification:** Phân loại công cụ: Tier 1 (Read-Only: đọc tệp, tìm kiếm, liệt kê thư mục - tự động cho phép), Tier 2 (Safe Mutating: sửa tệp trong repo, chạy unit test - ghi log tự động), Tier 3 (High-Risk/Destructive: chạy lệnh shell tùy ý, push git, deploy, xóa tệp - bắt buộc người dùng xác nhận).
- **Least-Privilege Tool Scoping:** Chỉ cung cấp cho agent tập công cụ tối thiểu cần thiết để hoàn thành nhiệm vụ cụ thể thay vì cấp toàn quyền root/admin.
- **Human-in-the-Loop Interception:** Cơ chế tạm dừng chu kỳ suy nghĩ của agent và hiển thị modal xác nhận kèm thông số tham số rõ ràng cho người dùng trước khi thực thi lệnh Tier 3.

## 6. Step-by-Step Execution Workflow
1. Khai báo danh mục tool kèm metadata chỉ định cấp độ rủi ro (`risk_level: 'READ_ONLY' | 'MUTATING' | 'HIGH_RISK'`).
2. Cấu hình bộ chặn Runtime Tool Dispatcher trong framework agent.
3. Khi LLM phát sinh `tool_call`: Kiểm tra cấp độ rủi ro của công cụ được gọi.
4. Nếu là Tier 1 hoặc Tier 2 đã được cấp phép trước: Cho phép thực thi ngay và lưu vết vào execution trace.
5. Nếu là Tier 3: Tạm dừng tiến trình, định dạng tham số lệnh thành bảng dễ đọc và gửi yêu cầu phê duyệt tới người dùng.
6. Nếu người dùng từ chối: Trả về thông báo lỗi có cấu trúc (`PERMISSION_DENIED_BY_USER`) cho LLM để agent điều chỉnh kế hoạch thay thế.

## 7. Concrete Examples
### Schema định nghĩa phân quyền Tool và bộ lọc Interceptor trong Python:
```python
from enum import Enum
from typing import Dict, Any

class RiskTier(Enum):
    READ_ONLY = 1
    SAFE_MUTATING = 2
    HIGH_RISK = 3

TOOL_REGISTRY: Dict[str, Dict[str, Any]] = {
    "read_file": {"tier": RiskTier.READ_ONLY, "requires_approval": False},
    "write_file": {"tier": RiskTier.SAFE_MUTATING, "requires_approval": False},
    "run_terminal_command": {"tier": RiskTier.HIGH_RISK, "requires_approval": True},
    "delete_file": {"tier": RiskTier.HIGH_RISK, "requires_approval": True},
}

def authorize_tool_execution(tool_name: str, arguments: Dict[str, Any], user_approved: bool = False) -> bool:
    tool_meta = TOOL_REGISTRY.get(tool_name)
    if not tool_meta:
        raise ValueError(f"Unknown tool: {tool_name}")

    # Neu la High-Risk ma chua co phe duyet tu con nguoi thi chan ngay
    if tool_meta["requires_approval"] and not user_approved:
        # Kiem tra dac biet neu run_terminal_command chua lenh nguy hiem
        if tool_name == "run_terminal_command":
            cmd = arguments.get("command", "")
            dangerous_patterns = ["rm -rf", "force", "drop", "sudo"]
            if any(p in cmd.lower() for p in dangerous_patterns):
                return False
        return False

    return True
```

## 8. Anti-Patterns & Common Traps
- **Blind Omnipotent Shell Tool:** Cung cấp duy nhất một tool `execute_bash` với quyền root và cho phép agent tự do thực thi mọi chuỗi lệnh mà không có bất kỳ bộ lọc nào.
- **Silent Execution of Destructive Actions:** Tự động thực thi xóa tệp hoặc ghi đè cấu hình mà không cảnh báo cho người dùng biết trước.
- **Implicit Scope Escalation:** Cho phép agent tự động sửa đổi tệp cấu hình phân quyền của chính nó để tự nâng quyền.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: 100% các công cụ có khả năng xóa tệp hoặc thực thi shell tùy ý đều được phân loại là `HIGH_RISK`.
- **QG-02**: Mọi yêu cầu thực thi công cụ `HIGH_RISK` đều yêu cầu cờ xác nhận tường minh từ người dùng.
- **QG-03**: Không có bất kỳ công cụ nào cho phép truy cập ra ngoài thư mục làm việc của dự án (Path Traversal Protection).

## 10. Security & Safety Boundaries
- Triệt tiêu rủi ro mã độc hoặc hướng dẫn prompt injection thao túng agent phá hoại hệ thống máy chủ hoặc xóa mã nguồn.

## 11. Platform Adapters
- **Frameworks**: OpenAI Tool Calling, Anthropic Claude Tools, Model Context Protocol (MCP), LangChain Tools.

## 12. Deliverables & Output Artifacts
- Ma trận phân loại cấp độ rủi ro của toàn bộ công cụ trong hệ thống (`tool_permissions.json`).
- Lớp kiểm soát thẩm quyền tool execution (`permission_interceptor.py`).
- Bộ kiểm thử tự động giả lập các hành vi gọi tool trái phép.

## 13. Related & Complementary Skills
dex-agent-engineering, dex-agent-context-source-trust, dex-execution-sandbox-policies

## 14. Realistic Usage Example
```bash
# Chay bo kiem thu phan quyen tool cua agent bang pytest
pytest tests/test_agent_tool_permissions.py -v

# Kiem tra danh muc tool manifest da gan du risk tier chua
python scripts/audit_tool_manifests.py
```
