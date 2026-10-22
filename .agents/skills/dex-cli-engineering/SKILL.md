---
name: dex-cli-engineering
description: Engineer industrial-grade command-line interfaces (CLIs), argument parsing, interactive terminal UX, POSIX flag conventions, exit code semantics, structured stdout/stderr, and auto-completion. Use when developing developer tools, automation scripts, or CLI utilities.
---

# dex-cli-engineering

## 1. Purpose & Scope
Thiết kế và phát triển các ứng dụng dòng lệnh (CLI - Command-Line Interface) chuyên nghiệp, trực quan và mạnh mẽ; tuân thủ chuẩn cờ POSIX/GNU, xử lý tham số và cờ dòng lệnh (flags/options/subcommands), cung cấp giao diện terminal thân thiện (spinners, colors, progress bars), tách biệt stdout và stderr, mã thoát (Exit Codes) chuẩn xác và hỗ trợ gợi ý lệnh (Shell Autocompletion).

## 2. When to Use
- Khi đóng gói các tác vụ tự động hóa hoặc công cụ nội bộ thành một lệnh CLI trực quan cho lập trình viên sử dụng.
- Khi ứng dụng dòng lệnh bị chập chờn, in lẫn lộn giữa log hệ thống và kết quả dữ liệu ra màn hình.
- Khi cần cung cấp cả 2 chế độ: Chế độ tương tác đồ họa terminal (Interactive TUI/Prompt) và chế độ không tương tác phục vụ CI/CD (`--non-interactive` / `--json`).

## 3. When NOT to Use
- Xây dựng giao diện web trên trình duyệt (dùng `dex-ui-component-contracts`).
- Các đoạn mã shell script ngắn dưới 10 dòng (dùng `dex-windows-packaging` hoặc bash đơn giản).

## 4. Prerequisites & Input Context
**Đầu vào cần thiết:**
- Danh sách subcommands, flags bắt buộc, flags tùy chọn và biến môi trường hỗ trợ.
- Yêu cầu về định dạng xuất dữ liệu: Bảng biểu (Table), JSON, YAML, plain text.
- Ngôn ngữ triển khai (Go với Cobra, Rust với Clap, Node.js với Commander/Clipanion, Python với Click/Typer).

**Điều kiện tiên quyết:**
- Đã xác định rõ đối tượng sử dụng: Con người (Human UX) hay Máy móc (Machine-readable Unix pipelines).

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**: Nắm vững cơ chế vận hành theo chuẩn Agent Skills, tuân thủ nghiêm ngặt tính xác định và ranh giới trách nhiệm.
- **Quy tắc quyết định kỹ thuật**:
- **Tách Biệt Tuyệt Đối stdout và stderr**: Không bao giờ in spinner hay thông điệp 'Loading...' vào stdout khi người dùng yêu cầu xuất kết quả dạng JSON.
- **Hỗ Trợ Flag Khử Tương Tác**: Bắt buộc hỗ trợ `--yes` hoặc `--non-interactive` để có thể chạy an toàn trong môi trường CI/CD không có bàn phím can thiệp.
- **Tôn Trọng Chuẩn Biến Môi Trường Không Màu**: Nếu biến môi trường `NO_COLOR=1` hoặc terminal không phải TTY (`!isatty`), tự động tắt màu mè ANSI và spinners.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Lệnh pipe `dex list | jq` bị vỡ định dạng JSON**: Do CLI in dòng thông báo "Đang lấy dữ liệu..." ra stdout -> Khắc phục: Đưa dòng thông báo sang stderr (`process.stderr.write` hoặc `eprintln!`).
- **CLI bị treo vô tận trong CI khi hỏi xác nhận (Y/n)**: Do không phát hiện môi trường headless -> Khắc phục: Tự động phát hiện `isTTY` hoặc fail nhanh nếu không có cờ `--yes`.

## 6. Step-by-Step Execution Workflow
1. Thiết kế cây lệnh phân cấp rõ ràng (ví dụ: `dex auth login`, `dex project create --name my-app`).
2. Phân tích tham số bằng thư viện chuyên dụng, tự động sinh trợ giúp (`--help`, `-h`) và phiên bản (`--version`, `-v`).
3. Phân luồng dòng xuất dữ liệu: Dữ liệu chính in ra `stdout`, thông báo tiến trình, lỗi và log phụ in ra `stderr`.
4. Cung cấp cờ `--json` để cho phép các script hoặc pipeline khác dễ dàng phân tích dữ liệu đầu ra qua `jq`.
5. Xử lý tín hiệu ngắt (Graceful Interruption on SIGINT/Ctrl+C): Dọn dẹp tài nguyên tạm trước khi thoát.
6. Áp dụng mã thoát chuẩn hóa (0: Thành công, 1: Lỗi thông thường, 2: Lỗi cú pháp cờ lệnh, 130: Người dùng hủy qua Ctrl+C).
7. Sinh tệp cấu hình gợi ý lệnh cho Bash, Zsh, Fish và PowerShell.

## 7. Concrete Examples
### Ví dụ triển khai chuẩn mực:
```python
# cli.py using typer
import sys, typer, json
app = typer.Typer(help="DEX Developer CLI Utility")

@app.command()
def deploy(env: str = typer.Option(..., "--env", "-e"), output_json: bool = typer.Option(False, "--json")):
    "Deploy application to target environment."
    if not output_json:
        typer.echo(f"Deploying to {env}...", err=True)
    result = {"status": "success", "env": env, "version": "v3.0.0"}
    if output_json:
        sys.stdout.write(json.dumps(result) + "\n")
    else:
        typer.secho(f"Deployment complete!", fg=typer.colors.GREEN)
```

### Lệnh xác minh & thực thi:
- Kiểm tra định dạng JSON không chứa rác: `dex status --json | jq .`
- Kiểm tra mã thoát khi gõ sai cờ: `dex --invalid-flag; echo $?` (phải trả về mã != 0)
- Kiểm tra hiển thị trợ giúp: `dex --help`

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước kiểm tra biên và giả định hệ thống luôn ở trạng thái lý tưởng.
- **Anti-Pattern 2**: Không ghi nhận nhật ký kiểm toán hoặc bỏ qua việc xử lý ngoại lệ lúc runtime.
- **Trap**: Bỏ qua các rào chắn an toàn hoặc cố tình chạy script không qua kiểm thử tự động.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Cây lệnh phân cấp logic, có `--help` chi tiết cho từng subcommand.
- QG-07: Hỗ trợ đầy đủ cờ `--json` xuất dữ liệu chuẩn không lẫn log rác.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động trước khi coi là hoàn thành.

## 10. Security & Safety Boundaries
- Ẩn ký tự nhập (Mask input) khi người dùng gõ mật khẩu hoặc API Token trong terminal tương tác.
- Không in API Token hoặc Private Key ra terminal log hay màn hình trợ giúp.
- Không bao giờ thực thi mã nguồn hoặc thay đổi cấu hình trên môi trường sản xuất mà thiếu cơ chế rollback an toàn.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Có thể kích hoạt trực tiếp từ terminal hoặc extension tương thích trong VS Code / Cursor / Windsurf.

## 12. Deliverables & Output Artifacts
- Mã nguồn CLI hoàn chỉnh với argument parsing chặt chẽ.
- Script sinh shell completion (`dex completion bash > /etc/bash_completion.d/dex`).
- Bộ kiểm thử unit & E2E cho CLI.

## 13. Related & Complementary Skills
- `dex-development-workflow`: Quy trình phát triển tiêu chuẩn.
- `dex-code-verification`: Xác minh chất lượng và tính đúng đắn của mã nguồn.
- `dex-master-orchestrator`: Bộ điều phối trung tâm kết nối kỹ năng này với các kỹ năng khác trong hệ thống.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư hoặc AI Agent tiếp nhận yêu cầu liên quan đến **dex-cli-engineering**.
1. Đọc kỹ đầu vào và các ràng buộc kỹ thuật tại mục 4.
2. Thực thi tuần tự 6 bước trong Workflow tại mục 6.
3. Chạy các lệnh kiểm chứng tại mục 7 và đối chiếu với Quality Gates tại mục 9.
4. Đóng gói deliverables theo danh sách tại mục 12 và báo cáo kết quả kèm bằng chứng xác thực.
