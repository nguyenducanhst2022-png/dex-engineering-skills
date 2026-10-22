# Hướng Dẫn Cài Đặt & Tích Hợp DEX Engineering Skills Pack

Tài liệu này hướng dẫn chi tiết cách cài đặt, kích hoạt và tích hợp **DEX Engineering Skills Pack v1.0.0** trên Windows 11 (PowerShell) cũng như các hệ điều hành Linux/macOS, tương thích với các AI Coding Agents hàng đầu.

---

## 1. Yêu Cầu Môi Trường (System Prerequisites)

- **Hệ điều hành**: Windows 11 / Windows 10 (hỗ trợ đầy đủ PowerShell 5.1+ hoặc PowerShell 7+), macOS, hoặc Linux Ubuntu 20.04+.
- **Python**: Phiên bản Python 3.10 trở lên (khuyến nghị Python 3.12).
- **Git**: Phiên bản Git 2.30+.
- **AI Coding Agent**: Bất kỳ agent nào hỗ trợ tiêu chuẩn [Agent Skills Specification](https://agentskills.io/specification) hoặc hỗ trợ đọc tài liệu `.agents/skills/`.

---

## 2. Hướng Dẫn Cài Đặt Trên Windows 11 (PowerShell)

Mở **PowerShell** (hoặc Windows Terminal) và thực hiện theo các bước sau:

### Bước 1: Sao chép hoặc Di chuyển Thư mục Kỹ năng vào Dự án
Giả sử dự án phần mềm của bạn nằm tại `D:\MyProject`:

```powershell
# Di chuyển vào thư mục dự án của bạn
cd D:\MyProject

# Tạo thư mục .agents nếu chưa có
New-Item -ItemType Directory -Force -Path ".agents\skills"

# Sao chép toàn bộ bộ kỹ năng DEX vào thư mục kỹ năng của dự án
Copy-Item -Recurse -Force "D:\VibeCoding\dex-engineering-skills\.agents\skills\*" ".agents\skills\"
```

### Bước 2: Tạo Liên Kết Mềm (Symbolic Link) — Cách Chuyên Nghiệp Nhất
Nếu bạn muốn tất cả các dự án trên máy cùng sử dụng chung một bản cập nhật duy nhất của bộ kỹ năng:

```powershell
# Mở PowerShell với quyền Administrator (Run as Administrator)
cd D:\MyProject

# Tạo Symbolic Link trỏ thẳng vào bộ kỹ năng DEX
New-Item -ItemType SymbolicLink -Path ".agents\skills" -Target "D:\VibeCoding\dex-engineering-skills\.agents\skills"
```

### Bước 3: Kiểm Tra Tính Toàn Vẹn Của Bộ Kỹ Năng
Chạy script kiểm tra tự động đi kèm để xác nhận mọi thứ đã sẵn sàng:

```powershell
python D:\VibeCoding\dex-engineering-skills\scripts\validate_pack.py
```

Nếu màn hình hiển thị `[OK] 31/31 skills are fully compliant with Agent Skills Specification!` nghĩa là quá trình cài đặt đã thành công 100%.

---

## 3. Hướng Dẫn Cài Đặt Trên Linux / macOS (Bash / Zsh)

```bash
# 1. Di chuyển vào thư mục dự án của bạn
cd /path/to/my-project

# 2. Tạo liên kết mềm tới bộ kỹ năng
mkdir -p .agents
ln -s /path/to/dex-engineering-skills/.agents/skills .agents/skills

# 3. Chạy script kiểm tra
python3 /path/to/dex-engineering-skills/scripts/validate_pack.py
```

---

## 4. Tích Hợp Với Từng Nền Tảng AI Coding Agent

### A. Tích Hợp Với OpenAI Codex
OpenAI Codex và các công cụ phát triển dựa trên chuẩn Agent Skills tự động quét thư mục `.agents/skills/` trong root của repository để nạp các tệp `SKILL.md`.
- Đảm bảo thư mục `.agents/skills/` nằm ngay tại thư mục gốc của repository dự án của bạn.
- Bổ sung file `AGENTS.md` vào thư mục gốc của dự án (sử dụng mẫu từ [`AGENTS.example.md`](AGENTS.example.md)) để hướng dẫn Codex luôn ưu tiên kích hoạt `dex-master-orchestrator`.

### B. Tích Hợp Với Google Antigravity
Google Antigravity nhận diện các kỹ năng tại thư mục `.gemini/antigravity/skills/` hoặc thư mục cấu hình toàn cục:
```powershell
# Ánh xạ kỹ năng sang thư mục của Antigravity
New-Item -ItemType Directory -Force -Path "$HOME\.gemini\antigravity\skills"
Copy-Item -Recurse -Force "D:\VibeCoding\dex-engineering-skills\.agents\skills\*" "$HOME\.gemini\antigravity\skills\"
```
Sau đó trong chat với Antigravity, bạn chỉ cần gõ:
> "Sử dụng skill `dex-master-orchestrator` để phân tích và thực hiện nhiệm vụ..."

### C. Tích Hợp Với Claude Code
Claude Code hỗ trợ đọc các kỹ năng tại `.claude/skills/` hoặc cấu hình trong `.clauderc`:
```powershell
New-Item -ItemType Directory -Force -Path ".claude\skills"
Copy-Item -Recurse -Force "D:\VibeCoding\dex-engineering-skills\.agents\skills\*" ".claude\skills\"
```

### D. Tích Hợp Với Cursor / Windsurf
Đối với Cursor hoặc Windsurf, tạo file `.cursorrules` hoặc `.windsurfrules` tại gốc dự án với nội dung:
```markdown
# DEX Engineering Rules
Whenever executing software engineering tasks, refer to the skills and workflows defined in `.agents/skills/`.
Always start by invoking `dex-master-orchestrator` to determine execution mode (QUICK, STANDARD, STRICT) and follow the 10 Quality Gates.
```

---

## 5. Hướng Dẫn Cập Nhật Bộ Kỹ Năng (Updating Skills)

Khi có phiên bản mới của DEX Engineering Skills Pack:
1. Kéo mã nguồn mới nhất từ kho lưu trữ Git:
   ```bash
   git pull origin main
   ```
2. Chạy lại công cụ kiểm thử:
   ```bash
   python scripts\validate_pack.py
   ```
3. Xem chi tiết các điểm cải tiến trong [`CHANGELOG.md`](CHANGELOG.md).
