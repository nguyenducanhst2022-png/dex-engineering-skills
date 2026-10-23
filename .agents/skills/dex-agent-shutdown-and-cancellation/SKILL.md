---
name: dex-agent-shutdown-and-cancellation
description: Handle abrupt cancellations, SIGINT signals, and graceful shutdowns in autonomous agent workflows. Clean up temporary files, terminate orphaned subprocesses, release locks, and preserve consistent state. Use when building reliable long-running agent runtimes.
---

# dex-agent-shutdown-and-cancellation

## 1. Purpose & Scope
Xử lý an toàn các tình huống dừng khẩn cấp (Graceful Shutdown) và hủy bỏ tác vụ (Cancellation Tokens) trong chu trình làm việc của tác nhân AI tự động; bắt và xử lý các tín hiệu hệ điều hành (`SIGINT`, `SIGTERM`); dọn dẹp triệt để các tệp tạm thời trên đĩa; kết liễu các tiến trình con mồ côi (Orphaned Subprocesses); giải phóng các khóa tài nguyên; và bảo tồn trạng thái nhất quán.

## 2. When to Use
- Khi người dùng bấm nút Hủy (Cancel / Stop Generating) trên giao diện hoặc nhấn `Ctrl+C` trên terminal.
- Khi hệ thống orchestrator quyết định hủy một agent chạy song song do một agent khác đã tìm ra lời giải trước.
- Khi máy chủ container nhận tín hiệu tắt máy từ Kubernetes (`SIGTERM`) và có 30 giây để dọn dẹp trước khi bị ép buộc tắt (`SIGKILL`).

## 3. When NOT to Use
- Khi tác vụ chạy đồng bộ siêu ngắn trong vài mili-giây không có tiến trình nền hoặc tệp tạm.
- Khi hệ điều hành gặp sự cố sập nguồn phần cứng đột ngột (trường hợp này phải dựa vào cơ chế WAL/Checkpoint phục hồi sau).

## 4. Prerequisites & Input Context
- **Signal Handlers:** Khả năng đăng ký các hàm xử lý tín hiệu hệ điều hành trong runtime (`signal.signal` trong Python, `process.on('SIGTERM')` trong Node.js).
- **CancellationToken Abstraction:** Đối tượng chuyển giao cờ hủy bỏ xuyên suốt các lời gọi hàm bất đồng bộ.

## 5. Core Concepts & Taxonomy
- **Orphaned Process Leak:** Khi tiến trình cha của agent bị hủy nhưng các tiến trình con do nó sinh ra (như máy chủ dev, trình duyệt Playwright, docker container) vẫn tiếp tục chạy ngầm, chiếm dụng 100% CPU và khóa các cổng mạng.
- **Process Group Termination:** Kỹ thuật gửi tín hiệu hủy tới toàn bộ nhóm tiến trình (`os.killpg`) thay vì chỉ gửi tới tiến trình con trực tiếp, bảo đảm toàn bộ cây tiến trình phụ trợ đều bị dọn dẹp sạch sẽ.
- **Compensation Rollback on Cancel:** Nếu agent đang sửa dở dang một tệp mã nguồn thì bị hủy, hệ thống tự động khôi phục lại tệp từ bản sao lưu trước đó để không để lại mã nguồn chắp vá gây lỗi build.

## 6. Step-by-Step Execution Workflow
1. Khởi tạo đối tượng `CancellationToken` và gắn vào chu trình suy luận của agent.
2. Đăng ký các signal handler bắt tín hiệu `SIGINT` (Ctrl+C) và `SIGTERM`.
3. Khi nhận tín hiệu hủy: Chuyển cờ `is_cancelled = True` và phát thông báo dừng tới các luồng con.
4. Lập tức gửi tín hiệu kết liễu tới toàn bộ cây tiến trình con đang chạy (sử dụng Process Group ID).
5. Kích hoạt danh sách các hàm thu dọn tài nguyên (Cleanup Callbacks): Xóa thư mục tạm, đóng kết nối database, giải phóng lock.
6. Lưu trạng thái dừng an toàn (Cancelled State) vào checkpoint để người dùng biết tác vụ đã bị dừng có chủ đích.
7. Thoát tiến trình với mã thoát chuẩn tắc (`exit code 130` cho SIGINT hoặc `143` cho SIGTERM).

## 7. Concrete Examples
### Xử lý tín hiệu hủy bỏ và dọn dẹp cây tiến trình con an toàn trong Python:
```python
import os
import signal
import sys
import subprocess
import time
from typing import List

ACTIVE_SUBPROCESSES: List[subprocess.Popen] = []

def signal_handler(signum, frame):
    print(f"\n[SHUTDOWN] Nhan tin hieu {signum}. Dang don dep tai nguyen...")
    
    # 1. Ket lieu toan bo cay tien trinh con
    for proc in ACTIVE_SUBPROCESSES:
        if proc.poll() is None: # Tien trinh van con song
            try:
                # Gui tin hieu terminate toi toan bo process group
                if sys.platform != "win32":
                    os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
                else:
                    proc.terminate()
                print(f"[CLEANUP] Da dung tien trinh con PID={proc.pid}")
            except Exception as e:
                print(f"[ERROR] Khong the dung PID={proc.pid}: {e}")

    # 2. Xoa cac tep tam neu co
    if os.path.exists(".agent_temp"):
        import shutil
        shutil.rmtree(".agent_temp", ignore_errors=True)
        print("[CLEANUP] Da xoa thu muc tam .agent_temp")

    sys.exit(128 + signum)

# Dang ky signal handlers
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
```

## 8. Anti-Patterns & Common Traps
- **Ignoring SIGINT / Bare Except:** Bắt lỗi bằng `except:` chung chung và bỏ qua `KeyboardInterrupt`, khiến người dùng không thể dừng agent bằng Ctrl+C trên terminal.
- **Leaving Orphaned Compilers/Browsers:** Khởi động trình duyệt Playwright hoặc lệnh `npm run dev` nhưng không dọn dẹp khi bị hủy, làm treo cổng 3000 cho các lần chạy sau.
- **Leaving Half-Written Corrupted Files:** Đang ghi đè tệp mã nguồn thì bị hủy, bỏ lại một tệp bị cụt một nửa khiến toàn bộ dự án không thể biên dịch.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: 100% các tín hiệu `SIGINT` và `SIGTERM` đều kích hoạt hàm dọn dẹp tiến trình con trước khi thoát.
- **QG-02**: Không để lại bất kỳ tiến trình mồ côi (Zombies/Orphans) nào sau khi tác vụ bị hủy bỏ.
- **QG-03**: Trạng thái mã nguồn trên đĩa được hoàn nguyên nguyên vẹn về trạng thái trước khi agent bắt đầu sửa đổi.

## 10. Security & Safety Boundaries
- Bảo vệ tài nguyên hệ thống máy trạm và máy chủ; ngăn ngừa rò rỉ bộ nhớ, treo cổng mạng và hỏng dữ liệu khi dừng tác vụ.

## 11. Platform Adapters
- **Runtimes**: Python signal/multiprocessing, Node.js AbortController, Kubernetes Pod Lifecycle PreStop.

## 12. Deliverables & Output Artifacts
- Module quản lý vòng đời hủy bỏ an toàn (`cancellation_manager.py`).
- Lớp bao bọc thực thi tiến trình con có theo dõi (`safe_subprocess_runner.py`).
- Kịch bản kiểm thử tự động giả lập gửi tín hiệu SIGINT.

## 13. Related & Complementary Skills
dex-agent-execution-budget-controls, dex-agent-state-persistence-contracts, dex-execution-sandbox-policies

## 14. Realistic Usage Example
```bash
# Kiem tra kha nang bat Ctrl+C va don dep tien trinh con cua agent
python -m agent.runner --task "Long task" &
KILL_PID=$!
sleep 2
kill -SIGINT $KILL_PID

# Kiem tra khong con tien trinh mo coi chay ngam tren cong
netstat -ano | findstr :3000
```
