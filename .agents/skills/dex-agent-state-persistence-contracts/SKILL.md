---
name: dex-agent-state-persistence-contracts
description: Architect, serialize, and validate persistent state checkpoints for long-running autonomous AI agents. Ensure atomic state updates, schema version migration, and safe resumption after interruptions. Use when building resilient multi-step agent workflows.
---

# dex-agent-state-persistence-contracts

## 1. Purpose & Scope
Thiết kế hợp đồng lưu trữ và khôi phục trạng thái bền vững (Persistent State Checkpoints) cho các tác nhân AI tự động chạy dài hạn; bảo đảm tính nguyên tử khi lưu trữ trạng thái (Atomic State Updates); quản lý nâng cấp phiên bản lược đồ trạng thái (Schema Version Migration); và bảo đảm khả năng tiếp tục thực thi an toàn sau khi tiến trình bị gián đoạn hoặc gặp sự cố máy chủ.

## 2. When to Use
- Khi xây dựng các tác nhân AI thực hiện các dự án kỹ thuật kéo dài hàng giờ hoặc nhiều ngày.
- Khi cần hỗ trợ tính năng tạm dừng (Pause) và tiếp tục (Resume) phiên làm việc của agent theo yêu cầu của người dùng.
- Khi hệ thống chạy trên hạ tầng điện toán đám mây dễ bị thu hồi tài nguyên (Spot/Preemptible Instances).

## 3. When NOT to Use
- Khi tác nhân là Stateless hoặc chỉ hoạt động trong một lượt hỏi đáp ngắn gọn.
- Khi trạng thái phiên có thể dễ dàng tái tạo lại từ đầu trong vòng vài giây mà không tốn chi phí token.

## 4. Prerequisites & Input Context
- **Hạ tầng lưu trữ:** Cơ sở dữ liệu quan hệ (PostgreSQL / SQLite) hoặc Object Storage hỗ trợ ghi tệp nguyên tử.
- **Lược đồ Trạng thái:** Định nghĩa Pydantic / TypeScript Schema rõ ràng của toàn bộ bộ nhớ và tiến trình làm việc của agent.

## 5. Core Concepts & Taxonomy
- **Checkpoint Ledger:** Nhật ký lưu trữ tuần tự các trạng thái của agent sau mỗi bước hành vi hoàn tất (`step_index`, `state_snapshot`, `delta_changes`, `timestamp`).
- **Atomic Write via Tempfile:** Ghi trạng thái mới vào tệp tạm thời trên đĩa trước khi dùng lệnh atomic rename để thay thế tệp chính thức, ngăn chặn việc tệp trạng thái bị hỏng nếu mất điện đột ngột.
- **Idempotent Resume:** Khả năng agent đọc lại checkpoint gần nhất và nhận biết chính xác công việc dở dang mà không thực hiện lại các thao tác đã hoàn thành có tính thay đổi (như gửi email, tạo commit).

## 6. Step-by-Step Execution Workflow
1. Khai báo lược đồ trạng thái (`AgentStateSchema`) bao gồm: ID phiên, phiên bản schema, danh sách công việc (`tasks`), bộ nhớ ngữ cảnh (`messages`), và trạng thái môi trường (`env_snapshot`).
2. Sau khi hoàn thành mỗi bước gọi tool thành công: Đóng gói trạng thái hiện tại thành snapshot JSON.
3. Ghi snapshot vào cơ sở dữ liệu hoặc tệp đĩa sử dụng cơ chế ghi nguyên tử (Atomic Write).
4. Khi agent khởi động lại: Kiểm tra xem có checkpoint dở dang của phiên làm việc hay không.
5. Nếu có: Đối soát phiên bản schema; áp dụng hàm migration nếu checkpoint thuộc phiên bản cũ.
6. Tái tạo lại bộ nhớ ngữ cảnh và tiếp tục vòng lặp suy nghĩ từ bước tiếp theo mà không lặp lại bước trước đó.

## 7. Concrete Examples
### Lược đồ lưu trữ Checkpoint nguyên tử cho Agent bằng Pydantic và SQLite:
```python
import json
import os
import tempfile
from pydantic import BaseModel, Field
from typing import List, Dict, Any

class AgentCheckpoint(BaseModel):
    session_id: str
    schema_version: int = 1
    current_step: int
    completed_tasks: List[str] = Field(default_factory=list)
    pending_tasks: List[str] = Field(default_factory=list)
    context_variables: Dict[str, Any] = Field(default_factory=dict)

def save_checkpoint_atomic(checkpoint: AgentCheckpoint, target_filepath: str):
    data = checkpoint.model_dump_json(indent=2)
    dirname = os.path.dirname(target_filepath)
    os.makedirs(dirname, exist_ok=True)

    # Ghi vao tep tam cung o dia de dam bao lenh atomic rename thanh cong
    with tempfile.NamedTemporaryFile("w", dir=dirname, delete=False, encoding="utf-8") as tf:
        tf.write(data)
        temp_name = tf.name

    # Atomic replace tren he dieu hanh POSIX va Windows
    os.replace(temp_name, target_filepath)
```

## 8. Anti-Patterns & Common Traps
- **Direct In-Place File Overwrite:** Mở tệp trạng thái bằng `open('state.json', 'w')` và ghi trực tiếp; nếu tiến trình bị kill giữa chừng, toàn bộ trạng thái sẽ bị rỗng và không thể phục hồi.
- **Storing Unserializable Objects:** Lưu trữ các đối tượng socket, kết nối database hoặc thread pointers vào checkpoint, gây lỗi crash khi deserialize.
- **Unversioned Checkpoint Schemas:** Thay đổi cấu trúc trường trong code nhưng không nâng `schema_version`, khiến phiên bản code mới không thể đọc được các checkpoint cũ của người dùng.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: 100% các thao tác lưu trữ checkpoint đều sử dụng cơ chế ghi tệp nguyên tử (`atomic replace`) hoặc transaction CSDL.
- **QG-02**: Mọi checkpoint đều có trường `schema_version` tường minh và có kịch bản di chuyển tương thích ngược.
- **QG-03**: Agent có khả năng phục hồi và tiếp tục hoạt động thành công sau khi bị giả lập ngắt tiến trình (SIGKILL test).

## 10. Security & Safety Boundaries
- Mã hóa dữ liệu trạng thái lưu trên đĩa nếu chứa thông tin nhạy cảm; ngăn ngừa việc chỉnh sửa trái phép checkpoint để tiêm mã độc vào agent.

## 11. Platform Adapters
- **Storage**: SQLite, PostgreSQL Checkpointer (LangGraph), Redis State, AWS S3 Snapshots.

## 12. Deliverables & Output Artifacts
- Lược đồ hợp đồng trạng thái agent (`agent_state_schema.py`).
- Module ghi và khôi phục checkpoint nguyên tử (`checkpoint_manager.py`).
- Bộ kiểm thử tự động kiểm tra khả năng phục hồi sau sự cố giả lập.

## 13. Related & Complementary Skills
dex-agent-engineering, dex-agent-shutdown-and-cancellation, dex-concurrency-state

## 14. Realistic Usage Example
```bash
# Kiem tra tinh hop le cua tep checkpoint gan nhat
python scripts/inspect_checkpoint.py .agent_state/session_123.json

# Chay kiem thu phuc hoi trang thai sau su co
pytest tests/test_agent_state_persistence.py -v
```
