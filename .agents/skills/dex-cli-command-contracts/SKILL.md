---
name: dex-cli-command-contracts
description: Specify, validate, and test POSIX and GNU command-line interface conventions, flag semantics, JSON streaming output, exit codes, and shell completions. Use when engineering robust developer CLIs and automated agent tools.
---

# dex-cli-command-contracts

## 1. Purpose & Scope
Đặc tả, xác thực và kiểm thử các quy ước giao diện dòng lệnh (CLI), ngữ nghĩa các cờ lệnh (flags), định dạng đầu ra chuẩn (JSON/Text), mã thoát (exit codes) và kịch bản tự động hoàn thành lệnh (shell completions); bảo đảm CLI hoạt động đáng tin cậy cả với con người và các AI coding agents.

## 2. When to Use
- Khi xây dựng công cụ dòng lệnh nội bộ phục vụ hàng trăm kỹ sư trong tổ chức hoặc làm công cụ cho AI Agent tương tác.
- Khi các cờ lệnh của CLI thiếu nhất quán (chỗ thì dùng `--output`, chỗ thì dùng `-o`, chỗ thì trả text không thể parse).
- Khi cần hỗ trợ chế độ xuất dữ liệu JSON có cấu trúc (`--format=json`) phục vụ tự động hóa.

## 3. When NOT to Use
- Khi chỉ viết một đoạn script shell đơn giản dùng một lần không có nhu cầu tham số hóa.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Mã nguồn công cụ CLI, thư viện xử lý CLI (Click, Cobra, Commander, Clap).
- **Quyền hạn truy cập:** Quyền thực thi và kiểm thử câu lệnh trên máy trạm.

## 5. Core Concepts & Taxonomy
- **Standard Exit Codes:** Tuân thủ chuẩn POSIX (`0` = Thành công, `1` = Lỗi thông thường, `2` = Lỗi cú pháp lệnh, `130` = Bị ngắt bởi Ctrl+C).
- **Machine-Readable Output:** Cung cấp cờ `--json` hoặc `--format=json` để xuất dữ liệu JSON thuần túy ra `stdout` mà không bị trộn lẫn với nhật ký thông tin (logs/spinners phải đưa sang `stderr`).
- **Idempotent Flags:** Hỗ trợ các cờ lệnh an toàn: `--dry-run` (chạy thử không ghi dữ liệu), `--quiet` (chỉ xuất kết quả), `--verbose` (hiển thị chi tiết).

## 6. Step-by-Step Execution Workflow
1. Thiết kế bảng đặc tả câu lệnh, cờ tham số và mã thoát tuân thủ chuẩn GNU/POSIX.
2. Tách biệt hoàn toàn luồng dữ liệu kết quả (`stdout`) và luồng thông báo tiến trình/lỗi (`stderr`).
3. Cài đặt cờ `--dry-run` cho tất cả các thao tác có khả năng thay đổi hoặc phá hủy dữ liệu.
4. Thiết lập schema JSON kiểm chứng cho dữ liệu xuất ra khi người dùng truyền cờ `--json`.
5. Tự động sinh file hoàn thành lệnh (Shell Completions) cho Bash, Zsh, Fish và PowerShell.
6. Viết bộ test tự động kiểm thử toàn bộ các mã thoát và định dạng đầu ra.

## 7. Concrete Examples
### Xây dựng CLI chuẩn mực với cờ JSON và phân tách stderr trong Python (Click):
```python
import sys
import json
import click

@click.command()
@click.option('--format', type=click.Choice(['text', 'json']), default='text', help='Dinh dang dau ra')
@click.option('--dry-run', is_flag=True, help='Chay thu khong ghi du lieu')
def deploy(format: str, dry_run: bool):
    '''Trien khai ung dung voi quy uoc CLI chuan muc.'''
    # Thong bao tien trinh luon day sang stderr
    sys.stderr.write("Dang kiem tra cau hinh he thong...
")
    
    if dry_run:
        sys.stderr.write("[DRY-RUN] Khong co thay doi nao duoc thuc thi.
")
        
    result = {"status": "SUCCESS", "dry_run": dry_run, "code": 0}
    
    # Ket qua du lieu may doc duoc xuat ra stdout
    if format == 'json':
        click.echo(json.dumps(result))
    else:
        click.echo(f"Ket qua: {result['status']}")
        
    sys.exit(0)

if __name__ == '__main__':
    deploy()
```

## 8. Anti-Patterns & Common Traps
- **Polluting stdout with Spinners:** In con trỏ xoay hoặc thông báo 'Đang tải...' vào luồng `stdout` khiến câu lệnh `app --json | jq .` bị lỗi cú pháp.
- **Returning Exit Code 0 on Failures:** Câu lệnh gặp lỗi nghiêm trọng nhưng vẫn thoát với exit code `0` khiến script tự động hóa không phát hiện được sự cố.
- **Inconsistent Flag Naming:** Dùng lẫn lộn camelCase (`--dryRun`) và kebab-case (`--dry-run`) trong cùng một bộ công cụ.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Cờ `--json` xuất ra chuỗi JSON hợp lệ 100% không chứa bất kỳ ký tự rác nào trên `stdout`.
- **QG-04**: Khi gặp lỗi cú pháp hoặc tham số không hợp lệ, CLI luôn thoát với mã lỗi khác 0.
- **QG-07**: 100% các lệnh có thao tác phá hủy đều hỗ trợ cờ `--dry-run`.

## 10. Security & Safety Boundaries
- Ẩn giấu các giá trị mật khẩu hoặc API key trên dòng lệnh bằng cách hỗ trợ đọc từ file hoặc biến môi trường thay vì cờ dòng lệnh lộ trong `ps`.

## 11. Platform Adapters
- **CLI Frameworks**: Click/Typer (Python), Cobra (Go), Clap (Rust), Commander (Node.js).

## 12. Deliverables & Output Artifacts
- Mã nguồn công cụ CLI tuân thủ hợp đồng giao diện.
- Kịch bản tự động sinh Shell Completions.
- Bộ kiểm thử tự động xác minh các mã thoát và luồng dữ liệu.

## 13. Related & Complementary Skills
dex-windows-linux-path-compatibility, dex-developer-workstation-bootstrap, dex-polyglot-build-orchestration

## 14. Realistic Usage Example
```powershell
# Chạy kiểm thử xuất dữ liệu JSON và lọc bằng jq
python cli.py --format=json | jq .status

# Kiểm tra mã thoát của câu lệnh khi gặp lỗi
python cli.py --invalid-flag
echo "Exit code: $LASTEXITCODE"
```
