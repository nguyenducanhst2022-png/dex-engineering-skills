---
name: dex-skill-example-test-fixtures
description: Scaffold, validate, and execute isolated test fixtures and reproducible code examples for every specialized skill. Use when ensuring skills provide verifiable, functioning code patterns rather than speculative instructions.
---

# dex-skill-example-test-fixtures

## 1. Purpose & Scope
Khởi tạo, kiểm chứng và thực thi các bộ mẫu thử nghiệm cô lập (Test Fixtures) và ví dụ mã lệnh có thể tái lập cho từng kỹ năng chuyên môn; bảo đảm mọi đoạn mã ví dụ trong kỹ năng đều hoạt động chính xác trong thực tế thay vì chỉ là các chỉ dẫn phỏng đoán trên lý thuyết.

## 2. When to Use
- Khi kiểm toán chất lượng mã nguồn ví dụ trong tài liệu kỹ năng để bảo đảm không bị lỗi thời (Code Drift).
- Khi nâng cấp phiên bản runtime và muốn xác thực xem các đoạn code ví dụ có còn chạy được hay không.
- Khi xây dựng kho dữ liệu mẫu kiểm thử tự động cho toàn bộ hệ sinh thái kỹ năng.

## 3. When NOT to Use
- Khi kỹ năng chỉ mô tả các quy trình tổ chức nhân sự hoặc phương pháp luận quản trị thuần túy không có mã lệnh.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Các đoạn mã ví dụ trích xuất từ mục 7 và 14 của các file `SKILL.md`, môi trường thực thi ngôn ngữ tương ứng.
- **Quyền hạn truy cập:** Quyền thực thi các đoạn mã kiểm thử trong môi trường sandbox.

## 5. Core Concepts & Taxonomy
- **Executable Documentation:** Tài liệu kỹ thuật đi kèm với khả năng tự kiểm thử; mọi khối mã ví dụ đều được trích xuất thành file tạm và biên dịch/chạy thử nghiệm.
- **Isolated Sandbox Fixtures:** Mỗi ví dụ chạy trong một thư mục tạm thời độc lập, tự động dọn dẹp sau khi kiểm thử xong.
- **Syntax & Execution Pass Rate:** Tỷ lệ phần trăm các đoạn mã ví dụ vượt qua kiểm tra cú pháp (Syntax Check) và thực thi thành công (Execution Test).

## 6. Step-by-Step Execution Workflow
1. Quét toàn bộ các file `SKILL.md` để trích xuất các khối mã lệnh (Code Blocks) theo từng ngôn ngữ (Python, TS, Bash, PowerShell).
2. Lưu các khối mã vào thư mục fixture tạm thời (`tests/fixtures/skills/<skill-id>/`).
3. Chạy công cụ kiểm tra cú pháp tĩnh (Python `py_compile`, TypeScript `tsc --noEmit`, ShellCheck).
4. Thực thi các đoạn mã có thể chạy được trong môi trường container sandbox có giới hạn thời gian.
5. Ghi nhận các đoạn mã bị lỗi biên dịch hoặc sập runtime vào danh sách cần sửa đổi.
6. Tự động thông báo cho tác giả kỹ năng để cập nhật lại ví dụ mã nguồn chính xác.

## 7. Concrete Examples
### Kịch bản tự động trích xuất và kiểm tra cú pháp mã ví dụ trong file SKILL.md:
```python
import re
import tempfile
import py_compile
from pathlib import Path

def test_extract_and_compile_python_examples(skill_path: str):
    with open(skill_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Trich xuat tat ca cac khoi ma Python
    python_blocks = re.findall(r"```python
(.*?)
```", content, re.DOTALL)
    print(f"Tim thay {len(python_blocks)} khoi ma Python trong {Path(skill_path).parent.name}")
    
    for idx, code in enumerate(python_blocks):
        with tempfile.NamedTemporaryFile(suffix=".py", mode="w", encoding="utf-8", delete=False) as tmp:
            tmp.write(code)
            tmp_path = tmp.name
            
        try:
            # Kiem tra cu phap bien dich Python
            py_compile.compile(tmp_path, doraise=True)
            print(f" -> Khoi ma #{idx+1}: Cu phap hop le 100%")
        except py_compile.PyCompileError as e:
            raise AssertionError(f"Loi cu phap trong vi du ma #{idx+1} tai {skill_path}:
{e}")
```

## 8. Anti-Patterns & Common Traps
- **Pseudo-Code Masked as Real Code:** Đưa mã giả định dạng tùy tiện vào khối mã lệnh ngôn ngữ khiến người dùng copy vào bị lỗi cú pháp.
- **Outdated Deprecated APIs:** Ví dụ sử dụng các hàm API đã bị khai tử từ 3 năm trước khiến người áp dụng gặp lỗi ngay lập tức.
- **Unpinned Dependencies in Examples:** Gọi các thư viện bên thứ ba mà không chỉ định phiên bản hoặc hướng dẫn cài đặt tương ứng.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: 100% các khối mã ví dụ trong kỹ năng vượt qua kiểm tra cú pháp (Syntax Check) thành công.
- **QG-04**: Các ví dụ độc lập có thể chạy được (Executable Snippets) hoàn thành với mã thoát 0.
- **QG-08**: Tất cả các lệnh kiểm tra trong mục 14 có thể thực thi được trên môi trường tiêu chuẩn.

## 10. Security & Safety Boundaries
- Cách ly môi trường chạy mã ví dụ trong sandbox an toàn để ngăn chặn việc thực thi vô ý các lệnh nguy hiểm (như `rm -rf`).

## 11. Platform Adapters
- **Linters & Compilers**: py_compile, tsc, ShellCheck, ESLint, PSScriptAnalyzer.

## 12. Deliverables & Output Artifacts
- Suite kiểm thử tự động trích xuất và thẩm định mã ví dụ kỹ năng.
- Thư mục test fixtures cho từng kỹ năng trọng điểm.
- Báo cáo tỷ lệ mã ví dụ đạt chuẩn trên toàn bộ hệ thống.

## 13. Related & Complementary Skills
dex-agent-skills-spec-compatibility, dex-skill-quality-scorecards, dex-execution-sandbox-policies

## 14. Realistic Usage Example
```powershell
# Trích xuất và kiểm tra cú pháp toàn bộ mã ví dụ trong các kỹ năng
pytest tests/test_skill_examples.py -v

# Kiểm tra các script shell trong kỹ năng bằng ShellCheck
find .agents/skills -name "SKILL.md" -exec python scripts/lint_skill_code.py {} +
```
