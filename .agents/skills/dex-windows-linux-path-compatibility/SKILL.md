---
name: dex-windows-linux-path-compatibility
description: Audit and eliminate cross-platform path separator bugs, CRLF/LF line-ending corruption, drive-letter handling flaws, and case-sensitivity defects across polyglot codebases. Use when ensuring Windows and POSIX operational parity.
---

# dex-windows-linux-path-compatibility

## 1. Purpose & Scope
Kiểm toán và triệt tiêu các lỗi tương thích đường dẫn đa nền tảng; giải quyết dứt điểm các lỗi dấu phân cách thư mục (`/` vs `\`), sai hỏng ký tự ngắt dòng (`CRLF` vs `LF`), xử lý ổ đĩa Windows (`C:`) và sự khác biệt về phân biệt hoa thường (Case-Sensitivity) giữa Windows và Linux.

## 2. When to Use
- Khi script kiểm thử hoặc build chạy thành công trên máy tính Windows của lập trình viên nhưng bị sập trên máy chủ Linux của CI.
- Khi Git liên tục báo toàn bộ các dòng trong file đều bị thay đổi do khác biệt ký tự ngắt dòng CRLF/LF.
- Khi mã nguồn sử dụng phép nối chuỗi đường dẫn thủ công dạng `dir + "/" + file` gây lỗi trên Windows.

## 3. When NOT to Use
- Khi phần mềm được thiết kế độc quyền chỉ chạy trên duy nhất một hệ điều hành cụ thể (ví dụ: Windows Kernel Driver hoặc Linux Kernel Module).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Mã nguồn đa nền tảng, file cấu hình `.gitattributes`, môi trường kiểm thử chạy cả Windows và Linux.
- **Quyền hạn truy cập:** Quyền sửa đổi mã nguồn xử lý file I/O và cấu hình Git.

## 5. Core Concepts & Taxonomy
- **Path Normalization:** Sử dụng các thư viện chuẩn đa nền tảng (`pathlib` trong Python, `path` trong Node.js, `filepath` trong Go) thay vì tự nối chuỗi.
- **Case Sensitivity Discrepancy:** Hệ thống tệp Linux phân biệt hoa thường (`File.txt` khác `file.txt`), trong khi Windows (NTFS) mặc định không phân biệt hoa thường.
- **Git CRLF Normalization:** Cấu hình file `.gitattributes` để chuẩn hóa toàn bộ ký tự ngắt dòng về LF khi commit vào repository.

## 6. Step-by-Step Execution Workflow
1. Khởi tạo file `.gitattributes` tại thư mục gốc với quy tắc `* text=auto eol=lf` để thống nhất ký tự ngắt dòng.
2. Rà soát toàn bộ mã nguồn: thay thế các phép nối chuỗi đường dẫn bằng `pathlib.Path` hoặc `path.join()`.
3. Quét phát hiện các file có tên trùng nhau nhưng khác nhau về chữ hoa chữ thường trong cùng một thư mục.
4. Kiểm tra các đoạn mã bóc tách đường dẫn: đảm bảo xử lý an toàn cho cả định dạng Windows UNC (`\\server\share`) và ký tự ổ đĩa (`C:`).
5. Thiết lập ma trận kiểm thử CI chạy đồng thời trên cả hai hệ điều hành: `windows-latest` và `ubuntu-latest`.
6. Xác thực toàn bộ các đường dẫn sinh ra trong các file log hoặc JSON đều sử dụng dấu gạch chéo chuẩn (`/`).

## 7. Concrete Examples
### Xử lý đường dẫn chuẩn mực đa nền tảng trong Python và cấu hình .gitattributes:
```ini
# .gitattributes - Ep buoc chuan hoa ngat dong LF
* text=auto eol=lf
*.bat text eol=crlf
*.ps1 text eol=crlf
```

```python
# Chuan hoa duong dan an toan tren ca Windows va Linux
from pathlib import Path

def get_config_file_path(base_dir: str, filename: str) -> Path:
    # Su dung pathlib de tu dong xu ly dau phan cach theo he dieu hanh
    path = Path(base_dir).resolve() / filename
    
    # Chuyen doi sang duong dan tieu chuan dau gach cheo khi ghi log hoac JSON
    posix_path_str = path.as_posix()
    print(f"Duong dan tieu chuan: {posix_path_str}")
    return path
```

## 8. Anti-Patterns & Common Traps
- **Hardcoded Backslash or Slash:** Nối chuỗi đường dẫn cứng bằng `folder + "\\" + file` làm gãy hoàn toàn ứng dụng trên Linux.
- **Ignoring Git Line Endings:** Không cấu hình `.gitattributes` dẫn tới việc các file shell script `.sh` bị lỗi ký tự `\r` không chạy được trên Linux.
- **Assuming Case-Insensitive Filesystems:** Đặt tên file là `UserCard.tsx` nhưng trong mã lệnh lại import `./usercard.tsx` (chạy được trên Windows nhưng sập trên Linux).

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: 100% file văn bản trong kho mã nguồn được chuẩn hóa ngắt dòng LF thông qua `.gitattributes`.
- **QG-04**: Test suite vượt qua 100% trên cả hai runner `windows-latest` và `ubuntu-latest` trong ma trận CI.
- **QG-07**: Không có phép nối chuỗi đường dẫn thủ công nào còn sót lại trong codebase.

## 10. Security & Safety Boundaries
- Ngăn ngừa các lỗ hổng tấn công duyệt thư mục (Path Traversal) bằng cách sử dụng phương thức `resolve()` và kiểm tra tiền tố an toàn.

## 11. Platform Adapters
- **Runtimes**: Python `pathlib`, Node.js `path`, Go `path/filepath`, Rust `std::path::Path`.
- **Tools**: dos2unix, gitattributes, ESLint import/no-unresolved.

## 12. Deliverables & Output Artifacts
- File `.gitattributes` chuẩn hóa toàn bộ repository.
- Bộ quy tắc linter phát hiện nối chuỗi đường dẫn không an toàn.
- Ma trận kiểm thử CI đa nền tảng (Windows + Linux).

## 13. Related & Complementary Skills
dex-developer-workstation-bootstrap, dex-reproducible-devcontainers, dex-cli-command-contracts

## 14. Realistic Usage Example
```powershell
# Chuyển đổi toàn bộ ký tự ngắt dòng trong repo theo quy chuẩn gitattributes
git add --renormalize .

# Kiểm tra đường dẫn đa nền tảng bằng pytest
pytest tests/test_path_compatibility.py -v
```
