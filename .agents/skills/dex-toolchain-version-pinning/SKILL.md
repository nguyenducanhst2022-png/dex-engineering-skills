---
name: dex-toolchain-version-pinning
description: Enforce strict, automated toolchain version pinning across compilers, runtimes, package managers, and linters using universal version managers and pre-commit hooks. Use when preventing environmental drift across distributed engineering teams.
---

# dex-toolchain-version-pinning

## 1. Purpose & Scope
Thực thi việc khóa cứng và tự động hóa phiên bản của toàn bộ chuỗi công cụ (compilers, runtimes, package managers, linters); sử dụng công cụ quản lý phiên bản toàn cầu (mise, asdf) và pre-commit hooks để ngăn chặn sai lệch môi trường giữa các kỹ sư.

## 2. When to Use
- Khi lỗi 'chạy được trên máy của người này nhưng vỡ trên máy của người khác' xảy ra do khác biệt phiên bản Node.js, Python hoặc Go.
- Khi nâng cấp phiên bản runtime toàn hệ thống và cần đảm bảo toàn bộ thành viên trong nhóm chuyển đổi đồng bộ.
- Khi pipeline CI/CD và máy lập trình viên cục bộ sử dụng các phiên bản compiler khác nhau gây sai khác mã sinh ra.

## 3. When NOT to Use
- Khi đang làm các dự án thử nghiệm cá nhân nhanh không có yêu cầu phối hợp đồng đội.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** File cấu hình phiên bản công cụ (`.tool-versions`, `.mise.toml`, `package.json#engines`), mã nguồn dự án.
- **Quyền hạn truy cập:** Quyền ghi vào thư mục gốc repository.

## 5. Core Concepts & Taxonomy
- **Universal Version Management:** Quản lý đa ngôn ngữ (Python, Node, Go, Rust, Java) trong cùng một file cấu hình duy nhất bằng `mise` hoặc `asdf`.
- **Engine Strictness:** Chặn đứng việc cài đặt thư viện (`npm install`, `poetry install`) nếu phiên bản runtime hiện tại của máy không khớp với quy định.
- **Pre-commit Toolchain Gate:** Hook tự động kiểm tra phiên bản các công cụ kiểm tra tĩnh (Linters/Formatters) trước khi cho phép commit mã nguồn.

## 6. Step-by-Step Execution Workflow
1. Khởi tạo file định nghĩa phiên bản công cụ thống nhất (`.mise.toml` hoặc `.tool-versions`) tại thư mục gốc.
2. Cố định phiên bản chính xác đến số bản vá (ví dụ: `nodejs 20.11.1`, `python 3.12.2`).
3. Cấu hình ràng buộc phiên bản trong manifest của từng ngôn ngữ (như `"engines": { "node": "20.x" }` trong `package.json`).
4. Viết script kiểm tra trước khi commit (pre-commit hook) so sánh phiên bản công cụ đang chạy với file cấu hình.
5. Tích hợp cùng một file cấu hình phiên bản vào các file định nghĩa pipeline CI/CD (GitHub Actions).
6. Bật cảnh báo tự động khi các phiên bản công cụ chuẩn bị hết hạn hỗ trợ (End of Life - EOL).

## 7. Concrete Examples
### Cấu hình khóa cứng phiên bản đa ngôn ngữ bằng .mise.toml:
```toml
# .mise.toml - Dinh nghia phien ban cong cu bat buoc
[tools]
python = "3.12.2"
node = "20.11.1"
pnpm = "8.15.4"
rust = "1.76.0"
golang = "1.22.1"

[settings]
legacy_version_file = false
experimental = true
```

```json
// package.json - Khoa cung runtime va package manager
{
  "name": "my-polyglot-app",
  "engines": {
    "node": ">=20.11.0 <21.0.0",
    "pnpm": ">=8.15.0"
  },
  "packageManager": "pnpm@8.15.4"
}
```

## 8. Anti-Patterns & Common Traps
- **Floating Latest Versions:** Khai báo phiên bản `node: latest` hoặc `python: 3.x` trong CI khiến pipeline có thể sụp đổ bất kỳ lúc nào khi có bản phát hành mới.
- **Multiple Conflicting Version Files:** Vừa duy trì `.nvmrc`, vừa có `.node-version`, vừa có `asdf` với các số phiên bản khác nhau gây xung đột.
- **Ignoring Linter Versions:** Dùng các phiên bản linter khác nhau giữa các máy khiến git diff bị nhiễu loạn định dạng mã nguồn.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: 100% các runtime và compiler cốt lõi được định nghĩa phiên bản chính xác trong `.mise.toml`.
- **QG-04**: CI/CD và máy trạm cục bộ sử dụng cùng một hash/phiên bản công cụ biên dịch.
- **QG-07**: Quy trình pre-commit chặn đứng ngay lập tức các commit nếu phát hiện sai lệch phiên bản.

## 10. Security & Safety Boundaries
- Tránh sử dụng các phiên bản runtime đã chạm ngưỡng End-of-Life (EOL) có nguy cơ chứa lỗ hổng bảo mật không được vá.

## 11. Platform Adapters
- **Version Managers**: mise-en-place, asdf, nvm, pyenv, Corepack, aqua.

## 12. Deliverables & Output Artifacts
- File cấu hình `.mise.toml` hoặc `.tool-versions` chuẩn mực.
- Hook kiểm tra phiên bản pre-commit.
- Tài liệu hướng dẫn đồng bộ hóa công cụ cho thành viên mới.

## 13. Related & Complementary Skills
dex-developer-workstation-bootstrap, dex-reproducible-devcontainers, dex-polyglot-build-orchestration

## 14. Realistic Usage Example
```powershell
# Cài đặt chính xác các phiên bản công cụ được chỉ định
mise install

# Kiểm tra tính tương thích của toàn bộ toolchain
mise doctor
```
