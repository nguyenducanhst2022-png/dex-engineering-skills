---
name: dex-execution-sandbox-policies
description: Define, enforce, and audit process-level execution sandboxes, filesystem write allowlists, network egress filters, and execution time limits for agent script runners. Use when securing agent execution runtimes against malicious tool use.
---

# dex-execution-sandbox-policies

## 1. Purpose & Scope
Định nghĩa, thực thi và kiểm toán các chính sách hộp cát thực thi cấp tiến trình (Process-Level Execution Sandboxes), danh sách trắng ghi hệ thống tệp (Filesystem Allowlist), bộ lọc kết nối mạng ra ngoài (Network Egress Filters) và giới hạn thời gian thực thi cho các script runner của AI Agent; bảo vệ máy trạm của lập trình viên trước các thao tác độc hại hoặc lỗi vô ý.

## 2. When to Use
- Khi AI Agent được cấp quyền thực thi các lệnh dòng lệnh (Shell Commands) hoặc chạy các script tự động sinh ra.
- Khi muốn ngăn chặn Agent vô tình xóa các thư mục hệ thống quan trọng (như `C:\Windows` hoặc `/etc`).
- Khi chạy các bài kiểm thử hoặc mã nguồn của bên thứ ba không rõ nguồn gốc.

## 3. When NOT to Use
- Khi tiến hành cài đặt phần mềm cấp hệ thống hoặc cấu hình nhân hệ điều hành đòi hỏi quyền truy cập toàn diện.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Bộ thực thi Polyglot Executor (`scripts/polyglot/core/executor.py`), chính sách an ninh định nghĩa bằng JSON/YAML.
- **Quyền hạn truy cập:** Quyền cấu hình tiến trình con (Subprocess) và cơ chế giới hạn tài nguyên hệ điều hành.

## 5. Core Concepts & Taxonomy
- **Filesystem Write Allowlist:** Tiến trình thực thi chỉ được phép ghi dữ liệu vào các thư mục được chỉ định rõ ràng (như `workspace/`, `dist/`, hoặc thư mục tạm thời `tmp/`); mọi nỗ lực ghi ra ngoài đều bị chặn đứng.
- **Process Isolation & Subprocess Flags:** Thực thi lệnh bằng mảng tham số (`shell=False`) để triệt tiêu hoàn toàn nguy cơ tấn công Command Injection qua ký tự phân cách chuỗi (`|`, `;`, `&&`).
- **Bounded Buffer & Hard Timeout:** Bắt buộc giới hạn kích thước bộ đệm `stdout/stderr` (tối đa 512KB) và thời gian thực thi cứng (ví dụ: tối đa 60 giây) để ngăn chặn hiện tượng treo máy hoặc cạn kiệt bộ nhớ.

## 6. Step-by-Step Execution Workflow
1. Khảo sát danh mục các thư mục và lệnh mà script runner được phép thao tác.
2. Cấu hình cơ chế kiểm tra đường dẫn an toàn: giải quyết liên kết tượng trưng (resolve symlinks) và kiểm tra tiền tố để chống Path Traversal.
3. Thiết lập cờ thực thi an toàn trong module `executor.py`: luôn sử dụng `shell=False` với mảng tham số tường minh.
4. Cài đặt giới hạn thời gian (Timeout) và bộ đệm đầu ra có kích thước giới hạn (Bounded Output Buffering).
5. Thiết lập bộ lọc khử khuẩn dữ liệu nhạy cảm: tự động xóa bỏ các token bí mật khỏi nhật ký lỗi hoặc kết quả trả về.
6. Kiểm thử tự động bằng cách chạy các lệnh vi phạm chính sách và xác nhận hệ thống chặn đứng thành công.

## 7. Concrete Examples
### Triển khai thực thi Subprocess an toàn có hộp cát trong Python (Polyglot Executor Core):
```python
import subprocess
import os
from pathlib import Path

MAX_OUTPUT_BYTES = 512 * 1024 # Gioi han 512KB phong chong tran bo nho
DEFAULT_TIMEOUT = 30 # Toi da 30 giay

def safe_sandbox_execute(command_args: list[str], working_dir: str, allowed_dirs: list[str]) -> dict:
    # 1. Kiem tra quyen ghi thu muc an toan (Path Traversal Protection)
    resolved_cwd = Path(working_dir).resolve()
    is_allowed = any(resolved_cwd.is_relative_to(Path(ad).resolve()) for ad in allowed_dirs)
    if not is_allowed:
        raise PermissionError(f"TU CHOI THUC THI: Thu muc {working_dir} nam ngoai vung Sandbox cho phep!")
        
    # 2. Thuc thi tien trinh khong su dung shell=True
    try:
        proc = subprocess.run(
            command_args,
            cwd=str(resolved_cwd),
            shell=False, # Bat buoc false chong Command Injection
            capture_output=True,
            timeout=DEFAULT_TIMEOUT
        )
        # 3. Cat bot dau ra neu vuot qua gioi han bo dem an toan
        stdout = proc.stdout[:MAX_OUTPUT_BYTES].decode("utf-8", errors="replace")
        stderr = proc.stderr[:MAX_OUTPUT_BYTES].decode("utf-8", errors="replace")
        
        return {"status": "SUCCESS", "exit_code": proc.returncode, "stdout": stdout, "stderr": stderr}
    except subprocess.TimeoutExpired:
        return {"status": "TIMEOUT", "exit_code": -1, "error": f"Lenh bi huy do chay qua {DEFAULT_TIMEOUT} giay."}
```

## 8. Anti-Patterns & Common Traps
- **Using shell=True with String Concat:** Chạy lệnh dạng `subprocess.run(f"echo {user_input}", shell=True)` mở toang cánh cửa cho tấn công Command Injection.
- **Unbounded Infinite Loops:** Chạy script không có timeout khiến tiến trình chạy ngầm vô tận và làm treo máy chủ.
- **Unrestricted Filesystem Access:** Cho phép script tự do đọc ghi vào bất kỳ thư mục nào trên ổ đĩa máy tính người dùng.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: 100% các lệnh con được thực thi với `shell=False` và mảng tham số phân tách rõ ràng.
- **QG-04**: Mọi nỗ lực ghi tệp ra ngoài phạm vi thư mục cho phép đều bị chặn và ghi nhận nhật ký vi phạm.
- **QG-07**: Toàn bộ các tiến trình con đều có giới hạn thời gian (Timeout <= 60s) và giới hạn bộ đệm (<= 512KB).

## 10. Security & Safety Boundaries
- Bảo vệ tuyệt đối an toàn môi trường máy trạm của lập trình viên và cụm máy chủ tự động hóa trước các hành vi phá hoại.

## 11. Platform Adapters
- **Engines**: Python Subprocess, Linux Bubblewrap, Docker Sandbox, Windows AppContainer, gVisor.

## 12. Deliverables & Output Artifacts
- Module thực thi lệnh an toàn có kiểm soát hộp cát (`executor.py`).
- Chính sách danh sách trắng thư mục và tài nguyên cho phép.
- Bộ kiểm thử tự động xác minh ranh giới bảo vệ hộp cát.

## 13. Related & Complementary Skills
dex-container-runtime-isolation, dex-runtime-capability-probing, dex-instruction-injection-testing

## 14. Realistic Usage Example
```powershell
# Chạy thực thi lệnh kiểm thử qua Polyglot Sandbox an toàn
python -m scripts.polyglot.dex validate --dry-run

# Kiểm tra bộ lọc bảo mật của executor bằng pytest
pytest scripts/polyglot/tests/test_executor.py -v
```
