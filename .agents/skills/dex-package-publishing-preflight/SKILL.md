---
name: dex-package-publishing-preflight
description: Execute automated dry-runs, artifact inspection, README checks, licensing audits, and provenance attestations prior to publishing packages to npm, PyPI, Crates.io, or NuGet. Use when safeguarding open-source and internal package releases.
---

# dex-package-publishing-preflight

## 1. Purpose & Scope
Thực thi quy trình kiểm tra tiền phát hành (Preflight Checks), đóng gói thử nghiệm (Dry-Run Packaging), kiểm tra nội dung artifact, tính đầy đủ của tài liệu, giấy phép bản quyền và chứng thực nguồn gốc (Provenance) trước khi xuất bản gói phần mềm lên npm, PyPI, Crates.io hoặc NuGet.

## 2. When to Use
- Khi chuẩn bị xuất bản một phiên bản thư viện mã nguồn mở hoặc gói phần mềm nội bộ lên registry công cộng.
- Khi muốn ngăn ngừa việc vô tình đóng gói các file rác, file test, hoặc khóa bí mật (`.env`) vào trong gói phát hành.
- Khi triển khai quy trình xuất bản an toàn không cần token lưu trữ cố định (Provenance & OIDC Publishing).

## 3. When NOT to Use
- Khi chỉ xây dựng ứng dụng cuối (End-User Application) không có nhu cầu đóng gói thành thư viện để phân phối.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Mã nguồn thư viện, file cấu hình xuất bản (`package.json`, `pyproject.toml`, `Cargo.toml`), tài khoản registry.
- **Quyền hạn truy cập:** Quyền thực thi lệnh đóng gói và kiểm toán artifact cục bộ.

## 5. Core Concepts & Taxonomy
- **Package Dry-Run:** Lệnh đóng gói và mô phỏng tải lên registry mà không thực sự phát hành (`npm publish --dry-run`, `cargo publish --dry-run`).
- **Tarball Inspection:** Giải nén và kiểm tra danh sách chính xác từng file sẽ được gửi tới người dùng cuối để loại trừ file nhạy cảm.
- **Signed Attestation (SLSA):** Ký số chứng thực xuất xứ nguồn gốc trực tiếp từ pipeline GitHub Actions tới npm/PyPI.

## 6. Step-by-Step Execution Workflow
1. Thực thi lệnh build và đóng gói thử nghiệm trong môi trường cô lập.
2. Liệt kê toàn bộ danh sách các file nằm trong tarball thành phẩm.
3. Quét phát hiện các file cấm: file cấu hình bí mật (`.env`, `.pem`), file kiểm thử nội bộ, tài liệu nháp.
4. Kiểm tra sự hiện diện của các file bắt buộc: `LICENSE`, `README.md`, `CHANGELOG.md`.
5. Xác minh tính hợp lệ của số phiên bản (Semantic Versioning) và bảo đảm chưa bị trùng lặp trên registry.
6. Kiểm tra các liên kết tài liệu và metadata trong manifest trước khi cấp phép xuất bản chính thức.

## 7. Concrete Examples
### Kiểm tra danh sách file đóng gói trước khi xuất bản npm / PyPI:
```powershell
# 1. Kiem tra danh sach file thuc te se duoc dong goi vao npm tarball
npm pack --dry-run

# 2. Dong goi va kiem tra do an toan bang Twine tren Python PyPI
python -m build
twine check dist/*

# 3. Kiem tra thu vien Rust truoc khi xuat ban len Crates.io
cargo publish --dry-run
```

```json
// package.json - Chi dinh ro rang cac file duoc phep xuat ban
{
  "name": "my-secure-lib",
  "version": "1.0.0",
  "files": [
    "dist",
    "README.md",
    "LICENSE"
  ]
}
```

## 8. Anti-Patterns & Common Traps
- **Publishing Without Whitelist:** Không khai báo trường `files` trong `package.json` khiến toàn bộ mã nguồn gốc, file test và cấu hình máy bị tải lên mạng.
- **Leaking Secrets in Tarball:** Vô tình đóng gói file `.env.local` chứa API keys vào gói phát hành công khai.
- **Skipping Build Verification:** Đóng gói mã nguồn mà quên chạy bước compile khiến người dùng tải về thư viện không có thư mục `dist`.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Lệnh đóng gói dry-run chạy thành công 100% không có bất kỳ cảnh báo nào.
- **QG-06**: Không có file chứa khóa bí mật, credentials hoặc file nháp nội bộ nào lọt vào tarball.
- **QG-08**: 100% gói phát hành đều có giấy phép `LICENSE` hợp lệ và tài liệu hướng dẫn `README.md`.

## 10. Security & Safety Boundaries
- Sử dụng cơ chế xuất bản không khóa (Keyless OIDC Trusted Publishing) trên GitHub Actions thay vì lưu trữ static API token.

## 11. Platform Adapters
- **Tools**: npm pack, Twine, cargo publish, NuGet CLI, pub, pkg-pr-new.

## 12. Deliverables & Output Artifacts
- Danh sách file cho phép đóng gói trong manifest.
- Script kiểm tra tiền xuất bản (Preflight Audit Script).
- Workflow xuất bản an toàn có gắn chứng chỉ xuất xứ.

## 13. Related & Complementary Skills
dex-binary-provenance-matching, dex-toolchain-reproducibility-audit, dex-monorepo-template-conformance

## 14. Realistic Usage Example
```powershell
# Chạy toàn bộ suite kiểm tra tiền phát hành
python scripts/release/preflight_check.py

# Kiểm tra tính toàn vẹn của package dist
twine check dist/*
```
