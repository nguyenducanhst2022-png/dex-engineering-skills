---
name: dex-developer-workstation-bootstrap
description: Automate declarative, idempotent developer machine provisioning across Windows, macOS, and Linux using unified dotfiles, package manifests, and posture verifications. Use when onboarding engineers and eliminating configuration drift.
---

# dex-developer-workstation-bootstrap

## 1. Purpose & Scope
Tự động hóa quá trình thiết lập môi trường máy trạm kỹ sư (Developer Workstation Bootstrap) theo hướng khai báo (declarative) và có tính lũy kế không đổi (idempotent) trên Windows, macOS và Linux; sử dụng dotfiles thống nhất, trình quản lý gói hệ điều hành và kiểm tra tuân thủ cấu hình.

## 2. When to Use
- Khi đón nhận kỹ sư mới vào đội ngũ và muốn rút ngắn thời gian thiết lập môi trường từ 3 ngày xuống dưới 30 phút.
- Khi môi trường máy tính của các thành viên trong đội bị sai lệch cấu hình (configuration drift) dẫn tới lỗi không đồng nhất.
- Khi thiết lập máy làm việc mới hoặc cài lại hệ điều hành sau sự cố.

## 3. When NOT to Use
- Khi triển khai cấu hình cho các máy chủ hạ tầng production (nên dùng Ansible, Terraform, hoặc Kubernetes).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** File khai báo công cụ (winget, Homebrew, apt), kho cấu hình dotfiles, tài khoản quyền Admin/Sudo cục bộ.
- **Quyền hạn truy cập:** Quyền thực thi các script tự động hóa trên máy trạm.

## 5. Core Concepts & Taxonomy
- **Idempotency:** Khả năng chạy script cài đặt nhiều lần liên tiếp mà không làm hỏng trạng thái hệ thống hoặc cài đè trùng lặp.
- **Declarative Package Manifests:** Danh sách gói phần mềm được khai báo rõ ràng trong file cấu hình (`Brewfile`, `winget-packages.json`).
- **Zero-Trust Posture Verification:** Tự động kiểm tra các tiêu chuẩn bảo mật tối thiểu: bật mã hóa ổ đĩa (BitLocker/FileVault), cập nhật bản vá OS, và cấu hình Git signing.

## 6. Step-by-Step Execution Workflow
1. Nhận diện hệ điều hành mục tiêu (Windows PowerShell, macOS Zsh, Linux Bash).
2. Cài đặt các trình quản lý gói chuẩn mực (Winget/Chocolatey trên Windows, Homebrew trên macOS/Linux).
3. Cài đặt tự động toàn bộ danh mục công cụ dòng lệnh (Git, Docker, Node.js, Python, VS Code).
4. Thiết lập liên kết tượng trưng (Symlinks) cho các file cấu hình dotfiles (`.gitconfig`, `.zshrc`, `settings.json`).
5. Cấu hình chữ ký số Git commit tự động bằng SSH keys hoặc GPG.
6. Chạy kịch bản kiểm tra xác thực (Health Check) để xác nhận 100% công cụ sẵn sàng hoạt động.

## 7. Concrete Examples
### Script khởi tạo máy trạm Windows bằng Winget và PowerShell:
```powershell
# bootstrap-windows.ps1 - Idempotent Developer Setup
$ErrorActionPreference = "Stop"

Write-Host "==> Khoi tao moi truong may tram DEX Engineer..." -ForegroundColor Cyan

# 1. Cai dat cac goi cong cu can thiet qua Winget
$packages = @(
    "Git.Git",
    "Microsoft.VisualStudioCode",
    "Docker.DockerDesktop",
    "Python.Python.3.12",
    "OpenJS.NodeJS.LTS"
)

foreach ($pkg in $packages) {
    Write-Host "Kiem tra / Cai dat: $pkg"
    winget install --id $pkg --exact --silent --accept-source-agreements --accept-package-agreements
}

# 2. Cau hinh Git toan cuc
git config --global core.autocrlf true
git config --global init.defaultBranch main

Write-Host "==> May tram da san sang lam viec!" -ForegroundColor Green
```

## 8. Anti-Patterns & Common Traps
- **Manual 20-Page Confluence Guide:** Bắt kỹ sư mới đọc tài liệu Word/Wiki dài dặc và tự tay tải từng file installer bằng trình duyệt.
- **Destructive Re-runs:** Script cài đặt ghi đè hoặc xóa sạch cấu hình cũ của người dùng khi chạy lại lần thứ hai.
- **Hardcoded Absolute User Paths:** Ghi cứng đường dẫn `/Users/john` khiến script thất bại trên máy của người khác.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Script chạy thành công từ đầu tới cuối trên máy mới hoàn toàn trong vòng dưới 30 phút mà không cần can thiệp thủ công.
- **QG-04**: Chạy lại script lần thứ hai (re-run) hoàn thành trong dưới 60 giây và giữ nguyên trạng thái đúng đắn.
- **QG-09**: Tất cả các công cụ cốt lõi (git, docker, python, node) đều phản hồi phiên bản hợp lệ từ terminal.

## 10. Security & Safety Boundaries
- Tuyệt đối không lưu trữ khóa riêng tư (Private Keys) hoặc token bí mật trong kho dotfiles công khai.

## 11. Platform Adapters
- **Package Managers**: Winget, Homebrew, Chocolatey, apt, mise, asdf.
- **Dotfile Managers**: Chezmoi, GNU Stow, Dotbot.

## 12. Deliverables & Output Artifacts
- Bộ script bootstrap đa nền tảng (`bootstrap.ps1`, `bootstrap.sh`).
- File khai báo gói ứng dụng chuẩn hóa.
- Script kiểm tra tư thế bảo mật và tính sẵn sàng của máy trạm.

## 13. Related & Complementary Skills
dex-toolchain-version-pinning, dex-reproducible-devcontainers, dex-windows-linux-path-compatibility

## 14. Realistic Usage Example
```powershell
# Chạy thiết lập máy trạm Windows
powershell -ExecutionPolicy Bypass -File scripts/bootstrap-windows.ps1

# Kiểm tra tính sẵn sàng của toàn bộ công cụ máy trạm
python scripts/doctor.py
```
