---
name: dex-shell-portability-testing
description: Audit and verify POSIX shell script portability across bash, dash, ash, and zsh, testing quoting correctness, path handling, and platform divergence (Linux, macOS, Windows Git Bash). Use when distributing cross-platform devops scripts.
---

# dex-shell-portability-testing

## 1. Purpose & Scope
Kiểm toán và bảo đảm tính khả chuyển của các script Shell (POSIX Shell Portability Testing); phát hiện và loại bỏ các cú pháp đặc thù riêng của Bash (Bashisms), kiểm tra tính tương thích trên nhiều shell runtimes (`bash`, `dash`, `ash`, `zsh`), xử lý ranh giới an toàn khi trích dẫn biến (Quoting), và đồng nhất đường dẫn giữa Linux, macOS và Windows Git Bash.

## 2. When to Use
- Khi viết các script cài đặt (installation scripts), CI/CD bootstrap, hoặc công cụ dòng lệnh được phân phối cho cộng đồng chạy trên nhiều bản phân phối Linux và macOS khác nhau.
- Khi script chạy tốt trên máy phát triển sử dụng Bash nhưng bị lỗi cú pháp khi chạy trong container Docker sử dụng Debian/Ubuntu (nơi `/bin/sh` là `dash`) hoặc Alpine Linux (nơi `/bin/sh` là `ash`).
- Khi cần loại bỏ các lỗi bảo mật liên quan tới Word Splitting và Globbing do thiếu dấu ngoặc kép quanh biến.

## 3. When NOT to Use
- Khi script được xác định rõ ràng chỉ chạy trong một môi trường container duy nhất có cài đặt Bash cố định và có shebang `#!/bin/bash` tường minh.
- Khi tác vụ quá phức tạp đòi hỏi các cấu trúc dữ liệu nâng cao (nên chuyển sang viết bằng Python, Go hoặc Rust).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Tệp shell script (`.sh`), công cụ linter tĩnh (`shellcheck`, `checkbashisms`), các shell môi trường kiểm thử (`dash`, `bash`, `zsh`).
- **Quyền hạn truy cập:** Quyền thực thi shell scripts trên môi trường kiểm thử.

## 5. Core Concepts & Taxonomy
- **POSIX Standard (`/bin/sh`):** Chuẩn mực tương thích tối thiểu mà mọi hệ điều hành họ Unix đều hỗ trợ; không bao gồm các tính năng nâng cao của Bash như `[[ ... ]]`, mảng (arrays), hoặc toán tử `==` trong kiểm tra điều kiện.
- **Bashisms:** Các cú pháp mở rộng chỉ hoạt động trên Bash; nếu tệp có shebang `#!/bin/sh` mà chứa bashism thì sẽ gây ra lỗi `syntax error: unexpected operator` khi chạy trên `dash`.
- **Proper Quoting (`"$VAR"`):** Luôn bọc biến trong dấu ngoặc kép kép để ngăn chặn cơ chế Word Splitting và Pathname Expansion khi giá trị của biến chứa khoảng trắng hoặc ký tự đặc biệt.

## 6. Step-by-Step Execution Workflow
1. Khai báo shebang tường minh: sử dụng `#!/bin/sh` nếu muốn tương thích tuyệt đối hoặc `#!/usr/bin/env bash` nếu bắt buộc dùng tính năng của Bash.
2. Chạy công cụ kiểm tra tĩnh `shellcheck --shell=sh` để phát hiện các lỗi vi phạm chuẩn POSIX và các cạm bẫy trích dẫn biến.
3. Chạy công cụ `checkbashisms` để quét và loại bỏ toàn bộ các cú pháp mở rộng đặc thù của Bash trong tệp có shebang `#!/bin/sh`.
4. Thay thế cú pháp `[[ ... ]]` bằng lệnh chuẩn `[ ... ]`, thay thế `==` bằng `=` trong phép so sánh chuỗi, và thay thế mảng bằng danh sách phân tách khoảng trắng.
5. Xử lý đường dẫn tương thích giữa các hệ điều hành: sử dụng biến môi trường và tránh giả định vị trí cố định của các lệnh hệ thống.
6. Chạy thử nghiệm script thực tế trong môi trường Docker đa nền tảng: Ubuntu (dash), Alpine (BusyBox ash), và macOS (zsh).

## 7. Concrete Examples
### Ví dụ chuẩn hóa mã nguồn Shell từ Bashism sang chuẩn POSIT an toàn:
```sh
#!/bin/sh
# Tuân thủ chuẩn POSIX thuần túy - Chạy được trên cả Ubuntu (dash), Alpine (ash) và macOS

set -eu

# SAI (Bashism): if [[ "$ENV" == "prod" ]]; then
# ĐÚNG (POSIX): Sử dụng [ ... ] đơn và toán tử =
if [ "${ENV:-}" = "prod" ]; then
    echo "Running in production mode."
fi

# SAI (Thiếu dấu ngoặc kép gây lỗi khi đường dẫn có dấu cách):
# target_dir=$1
# rm -rf $target_dir/cache

# ĐÚNG: Luôn bọc biến trong ngoặc kép
TARGET_DIR="${1:-}"
if [ -n "$TARGET_DIR" ] && [ -d "$TARGET_DIR" ]; then
    rm -rf "${TARGET_DIR}/cache"
fi

# SAI (Bashism array): files=(*.log)
# ĐÚNG (POSIX): Sử dụng positional parameters
set -- *.log
if [ -f "$1" ]; then
    for f in "$@"; do
        echo "Processing log: $f"
    done
fi
```

## 8. Anti-Patterns & Common Traps
- **Shebang Mismatch:** Để shebang là `#!/bin/sh` nhưng lại sử dụng cú pháp mảng `declare -a` của Bash khiến script chết trên Ubuntu.
- **Unquoted Variables:** Viết `rm -rf $DIR/*`, khi biến `$DIR` rỗng hoặc chứa dấu cách sẽ vô tình xóa sạch thư mục gốc của hệ thống.
- **Assuming GNU Utilities:** Sử dụng các cờ mở rộng của lệnh GNU (như `sed -i` không có tham số mở rộng) khiến script bị lỗi trên macOS BSD `sed`.

## 9. Quality Gates & Acceptance Criteria
- **QG-02**: Script vượt qua kiểm tra tĩnh của `shellcheck` ở mức độ kiểm tra nghiêm ngặt không có lỗi hoặc cảnh báo.
- **QG-05**: Công cụ `checkbashisms` xác nhận 0 cú pháp bashism tồn tại trong các script có shebang `#!/bin/sh`.
- **QG-12**: Script chạy thử nghiệm thành công với exit code 0 trên cả ba shell runtimes: `bash`, `dash` và `ash`.

## 10. Security & Safety Boundaries
- Luôn sử dụng cờ `set -eu` (hoặc `set -e -u -o pipefail` trên Bash) ở đầu script để dừng thực thi ngay lập tức khi có lệnh bị lỗi hoặc biến chưa được định nghĩa.
- Ngăn chặn việc thực thi chuỗi ký tự tùy ý bằng lệnh `eval` với dữ liệu đầu vào từ người dùng.

## 11. Platform Adapters
- **Linters**: ShellCheck, checkbashisms, shfmt.
- **Runtimes**: GNU Bash, Debian Dash, BusyBox Ash, Zsh.

## 12. Deliverables & Output Artifacts
- Tệp shell script đã được chuẩn hóa tương thích POSIX.
- Cấu hình kiểm tra tự động ShellCheck trong CI pipeline.
- Báo cáo kết quả kiểm thử chạy đa shell trên các container khác nhau.

## 13. Related & Complementary Skills
dex-cli-engineering, dex-cross-platform-portability, dex-windows-linux-path-compatibility

## 14. Realistic Usage Example
```powershell
# Chạy kiểm tra tính khả chuyển POSIX và lỗi cú pháp trên toàn bộ shell scripts
shellcheck --shell=sh scripts/*.sh
checkbashisms scripts/*.sh
```
