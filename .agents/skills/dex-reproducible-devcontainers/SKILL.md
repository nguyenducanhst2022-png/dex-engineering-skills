---
name: dex-reproducible-devcontainers
description: Standardize development environments using OCI Dev Containers, dotfile integration, non-root user permissions, and host volume optimization across Windows, macOS, and Linux. Use when onboarding developers into complex distributed codebases.
---

# dex-reproducible-devcontainers

## 1. Purpose & Scope
Chuẩn hóa môi trường làm việc của lập trình viên bằng OCI Dev Containers; tích hợp dotfiles cá nhân, bảo đảm quyền hạn người dùng phi root (non-root), và tối ưu hóa hiệu năng gắn kết ổ đĩa (Host Volume Mounts) trên Windows, macOS và Linux.

## 2. When to Use
- Khi dự án yêu cầu nhiều dependency phức tạp (PostgreSQL, Redis, C++ compilers, Python packages) khó cài đặt đồng nhất trên máy thật.
- Khi muốn lập trình viên mới có thể mở repo trong VS Code / Cursor và bắt đầu viết code ngay lập tức mà không cần cài đặt gì thêm vào máy chủ.
- Khi muốn cách ly môi trường chạy mã nguồn khỏi hệ điều hành máy tính cá nhân.

## 3. When NOT to Use
- Khi phát triển các ứng dụng đòi hỏi can thiệp sâu vào phần cứng máy tính (Kernel drivers, Bluetooth, thiết bị USB ngoại vi).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** File cấu hình `.devcontainer/devcontainer.json`, Dockerfile, Docker Desktop hoặc Finch/Podman.
- **Quyền hạn truy cập:** Quyền thực thi Docker và quyền gắn kết thư mục workspace.

## 5. Core Concepts & Taxonomy
- **Development Containers Specification:** Chuẩn mở định nghĩa môi trường phát triển bên trong container bao gồm phần mềm, biến môi trường và extension của IDE.
- **Non-Root Safety:** Chạy phiên làm việc dưới quyền người dùng thông thường (`vscode` hoặc `node`) thay vì quyền `root` để bảo vệ an toàn tệp tin trên máy trạm.
- **Volume Performance on Windows/macOS:** Tránh mount trực tiếp ổ đĩa Windows NTFS (`/mnt/c`) vào Docker container do độ trễ dịch I/O; nên clone mã nguồn trực tiếp vào WSL2 hoặc Docker Volume.

## 6. Step-by-Step Execution Workflow
1. Khởi tạo thư mục `.devcontainer` kèm file `devcontainer.json` và `Dockerfile` cơ sở tối ưu hóa.
2. Cấu hình người dùng phi root (`remoteUser: "vscode"`) và cấp quyền sudo có giới hạn nếu cần thiết.
3. Định nghĩa danh sách các extension VS Code và cấu hình IDE mặc định cần tự động kích hoạt khi mở container.
4. Tích hợp chuyển tiếp cổng mạng (Forward Ports) cho các dịch vụ web và database nội bộ.
5. Thiết lập cache cho các thư mục gói phụ thuộc (`node_modules`, `.cargo`, `.cache`) bằng Named Volumes để tăng tốc độ I/O.
6. Kiểm thử quy trình mở container tự động từ giao diện VS Code và GitHub Codespaces.

## 7. Concrete Examples
### Cấu hình .devcontainer/devcontainer.json chuẩn mực:
```json
{
  "name": "DEX Polyglot Workspace",
  "build": {
    "dockerfile": "Dockerfile",
    "context": ".."
  },
  "remoteUser": "vscode",
  "features": {
    "ghcr.io/devcontainers/features/common-utils:2": {
      "username": "vscode",
      "upgradePackages": true
    },
    "ghcr.io/devcontainers/features/git:1": {}
  },
  "customizations": {
    "vscode": {
      "settings": {
        "editor.formatOnSave": true,
        "terminal.integrated.defaultProfile.linux": "zsh"
      },
      "extensions": [
        "ms-python.python",
        "dbaeumer.vscode-eslint",
        "rust-lang.rust-analyzer"
      ]
    }
  },
  "forwardPorts": [3000, 8000],
  "postCreateCommand": "bash .devcontainer/post-create.sh"
}
```

## 8. Anti-Patterns & Common Traps
- **Running Everything as Root:** Chạy container dưới quyền `root` khiến các file tạo ra trên máy thật bị khóa quyền và khó xóa bỏ.
- **Mounting Slow Windows Paths:** Đặt repository tại `C:\workspace` rồi mount vào container khiến tốc độ `git status` và `npm install` chậm đi 10 lần so với chạy trong WSL2.
- **Monolithic 20GB Images:** Cài đặt toàn bộ các công cụ trên thế giới vào một image duy nhất thay vì sử dụng Dev Container Features modular.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Container khởi động thành công và vượt qua script `post-create.sh` trong dưới 5 phút.
- **QG-04**: Tiến trình người dùng trong container chạy dưới quyền phi root (UID != 0).
- **QG-09**: Tất cả các cổng mạng cần thiết (API, Web) được chuyển tiếp và kết nối thông suốt.

## 10. Security & Safety Boundaries
- Tuyệt đối không mount Docker socket (`/var/run/docker.sock`) vào container trừ khi thực sự cần tính năng Docker-in-Docker an toàn.

## 11. Platform Adapters
- **Tools**: VS Code Remote - Containers, Dev Container CLI, GitHub Codespaces, Docker, Podman.

## 12. Deliverables & Output Artifacts
- Thư mục cấu hình `.devcontainer` hoàn chỉnh.
- Dockerfile cơ sở đã được tối ưu bảo mật và kích thước.
- Script thiết lập sau khởi tạo `post-create.sh`.

## 13. Related & Complementary Skills
dex-developer-workstation-bootstrap, dex-toolchain-version-pinning, dex-windows-linux-path-compatibility

## 14. Realistic Usage Example
```powershell
# Chạy kiểm tra và build Dev Container bằng devcontainer CLI
npx @devcontainers/cli up --workspace-folder .

# Thực thi lệnh kiểm tra môi trường bên trong container
npx @devcontainers/cli exec --workspace-folder . whoami
```
