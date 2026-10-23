---
name: dex-runtime-capability-probing
description: Probe, detect, and adapt to host runtime capabilities, available toolchains, CLI versions, and OS environments without failing or making destructive assumptions. Use when ensuring skills operate reliably across heterogeneous host environments.
---

# dex-runtime-capability-probing

## 1. Purpose & Scope
Thăm dò, phát hiện và tự động thích ứng với năng lực môi trường thực thi máy chủ (Runtime Capability Probing); kiểm tra các công cụ sẵn có, phiên bản CLI, quyền hạn người dùng và hệ điều hành; bảo đảm kỹ năng hoạt động bền bỉ, không bị crash hoặc đưa ra các giả định phá hoại khi thiếu công cụ.

## 2. When to Use
- Khi kỹ năng cần sử dụng một công cụ bên ngoài (như Docker, Rust, Go, CMake) nhưng máy chủ của người dùng có thể chưa cài đặt công cụ đó.
- Khi thực thi trên nhiều hệ điều hành khác nhau (Windows 11, Ubuntu Linux, macOS) với các công cụ tương đương khác nhau.
- Khi triển khai chính sách phản hồi mềm dẻo (Graceful Degradation): cung cấp giải pháp thay thế hoặc hướng dẫn cài đặt chuẩn xác thay vì báo lỗi không xử lý.

## 3. When NOT to Use
- Khi môi trường thực thi đã được cố định cứng trong một Docker container chuẩn hóa 100%.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Danh sách công cụ cần kiểm tra, script thăm dò môi trường (`shutil.which`, lệnh kiểm tra phiên bản).
- **Quyền hạn truy cập:** Quyền thực thi các lệnh đọc thông tin hệ điều hành không phá hủy.

## 5. Core Concepts & Taxonomy
- **Graceful Tool Degradation:** Nếu công cụ tối ưu (ví dụ: `ripgrep`) không có sẵn, hệ thống tự động hạ cấp xuống công cụ có sẵn (như `grep` hoặc tìm kiếm nội bộ Python) kèm thông báo rõ ràng.
- **Standardized Not-Available Protocol:** Khi công cụ bắt buộc hoàn toàn vắng mặt, kỹ năng trả về mã trạng thái chuẩn `TOOL_NOT_AVAILABLE` kèm hướng dẫn cài đặt chính xác, tuyệt đối không tự ý chạy lệnh cài đặt không xin phép.
- **Windows .CMD Resolution:** Trên hệ điều hành Windows, các công cụ Node.js (`npm`, `npx`) là các file kịch bản `.cmd`, bắt buộc phải phân giải đường dẫn đầy đủ khi gọi qua tiến trình con.

## 6. Step-by-Step Execution Workflow
1. Khởi tạo danh mục các công cụ phụ thuộc của kỹ năng kèm phiên bản tối thiểu yêu cầu.
2. Thực hiện thăm dò sự hiện diện của công cụ trong biến môi trường `PATH` bằng hàm kiểm tra an toàn (`shutil.which`).
3. Thực thi lệnh kiểm tra phiên bản với timeout ngắn (ví dụ: `tool --version`, tối đa 3 giây).
4. Đánh giá tính sẵn sàng của môi trường: Đầy đủ (Full), Một phần (Degraded), hoặc Thiếu (Missing).
5. Nếu thiếu công cụ không bắt buộc, tự động chuyển đổi sang phương thức thay thế dự phòng.
6. Nếu thiếu công cụ cốt lõi, trả về báo cáo chẩn đoán kèm lệnh cài đặt chính thức cho hệ điều hành hiện tại.

## 7. Concrete Examples
### Kịch bản thăm dò năng lực runtime đa nền tảng an toàn trong Python:
```python
import shutil
import subprocess
import platform

def probe_tool_capability(tool_name: str, min_version: str = None) -> dict:
    # 1. Xu ly phan giai ten file tren Windows cho cac cong cu script
    resolved_cmd = tool_name
    if platform.system() == "Windows" and not tool_name.endswith((".exe", ".cmd", ".bat")):
        cmd_path = shutil.which(f"{tool_name}.cmd") or shutil.which(f"{tool_name}.exe")
        if cmd_path: resolved_cmd = cmd_path
        
    path = shutil.which(resolved_cmd)
    if not path:
        return {
            "status": "TOOL_NOT_AVAILABLE",
            "available": False,
            "install_guide": f"Hay cai dat {tool_name} qua: winget install {tool_name} (Windows) hoac brew install {tool_name} (macOS)"
        }
        
    # 2. Kiem tra phien ban an toan
    try:
        proc = subprocess.run([resolved_cmd, "--version"], capture_output=True, text=True, timeout=3)
        version_str = proc.stdout.strip() or proc.stderr.strip()
        return {"status": "READY", "available": True, "path": path, "version": version_str}
    except Exception as e:
        return {"status": "ERROR", "available": True, "error": str(e)}
```

## 8. Anti-Patterns & Common Traps
- **Crashing on Missing Binaries:** Gọi trực tiếp `subprocess.run(['cargo', 'build'])` mà không kiểm tra xem `cargo` có tồn tại hay không khiến ứng dụng sập unhandled exception.
- **Unprompted Auto-Installation:** Tự ý chạy lệnh `npm install -g` hoặc `pip install` ngầm mà không có sự đồng ý của người dùng.
- **Assuming Linux Tools on Windows:** Mặc định các công cụ Linux (`grep`, `sed`, `awk`, `bash`) luôn có sẵn trên Windows Command Prompt.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: 100% các công cụ bên ngoài đều được kiểm tra sự hiện diện trước khi gọi lệnh thực thi.
- **QG-04**: Khi công cụ vắng mặt, kỹ năng trả về mã `TOOL_NOT_AVAILABLE` kèm hướng dẫn cài đặt chuẩn xác.
- **QG-07**: Không bao giờ thực hiện cài đặt ngầm phần mềm vào máy người dùng mà không có phê duyệt.

## 10. Security & Safety Boundaries
- Ngăn chặn các cuộc tấn công chiếm quyền nạp file nhị phân (Binary Hijacking) bằng cách kiểm tra đường dẫn thực thi an toàn trong thư mục hệ thống.

## 11. Platform Adapters
- **Platforms**: Windows (PowerShell/Winget), macOS (Homebrew), Linux (apt/dnf), WSL2.

## 12. Deliverables & Output Artifacts
- Module thăm dò năng lực runtime đa nền tảng (`detector.py`).
- Báo cáo chẩn đoán trạng thái công cụ máy trạm (`doctor`).
- Bộ kiểm thử tự động giả lập môi trường thiếu công cụ.

## 13. Related & Complementary Skills
dex-developer-workstation-bootstrap, dex-windows-linux-path-compatibility, dex-execution-sandbox-policies

## 14. Realistic Usage Example
```powershell
# Chạy chẩn đoán năng lực toàn bộ runtime trên máy
python -m scripts.polyglot.dex doctor

# Kiểm tra sự sẵn sàng của một công cụ cụ thể
python -c "from scripts.polyglot.core.detector import probe_tool; print(probe_tool('git'))"
```
