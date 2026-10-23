---
name: dex-cross-platform-release-matrices
description: Build, test, matrix-validate, and package release artifacts across Windows, Linux, and macOS environments. Use when ensuring release candidates achieve full cross-platform parity before deployment.
---

# dex-cross-platform-release-matrices

## 1. Purpose & Scope
Biên dịch, kiểm thử, xác thực ma trận (Matrix Validation) và đóng gói các artifact phát hành đồng bộ trên cả ba môi trường hệ điều hành: Windows, Linux và macOS; bảo đảm phiên bản phát hành đạt được tính tương đương và ổn định 100% trước khi triển khai chính thức.

## 2. When to Use
- Khi chuẩn bị phát hành một phiên bản lớn (Major Release v8.0.0) của bộ kỹ năng và công cụ dòng lệnh.
- Khi script hoặc công cụ có các thành phần đặc thù hệ điều hành (như đường dẫn, shell wrappers, quản lý tiến trình).
- Khi thiết lập ma trận kiểm thử tự động trong GitHub Actions nhằm bảo đảm không có lỗi riêng lẻ trên một hệ điều hành cụ thể.

## 3. When NOT to Use
- Khi chỉ chỉnh sửa một tài liệu Markdown đơn lẻ không ảnh hưởng đến bất kỳ mã lệnh thực thi nào.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Mã nguồn framework, script điều phối Polyglot (`dex.py`, `dex.ps1`, `dex.sh`), runner ma trận CI (Windows, Ubuntu, macOS).
- **Quyền hạn truy cập:** Quyền cấu hình workflow GitHub Actions và quyền ký số bản phát hành.

## 5. Core Concepts & Taxonomy
- **Matrix Strategy:** Chiến lược chạy song song các job kiểm thử trên một lưới các biến thể: `os: [windows-latest, ubuntu-latest, macos-latest]` kết hợp `python-version: ['3.10', '3.11', '3.12']`.
- **Unified Release Manifest:** Bản ghi siêu dữ liệu chứa thông tin mã băm SHA-256 của các artifact đóng gói trên từng nền tảng kèm chữ ký chứng thực.
- **Parity Gate:** Yêu cầu 100% các ô trong ma trận kiểm thử đều phải đạt trạng thái Thành công (Green) mới cho phép kích hoạt bước phát hành.

## 6. Step-by-Step Execution Workflow
1. Cấu hình file workflow GitHub Actions với ma trận kiểm thử bao quát 3 hệ điều hành và các phiên bản runtime mục tiêu.
2. Chạy bộ kiểm thử toàn diện (Unit Tests, Skill Validation, Polyglot Diagnostics) trên từng runner.
3. Đóng gói các artifact phân phối: file zip cho Windows, tar.gz cho Linux/macOS, kèm các wrapper tương ứng.
4. Tính toán mã băm SHA-256 cho từng artifact đóng gói và tạo file `SHA256SUMS`.
5. Tự động kiểm tra tính tương đương kết quả đầu ra giữa các nền tảng.
6. Xuất bản phiên bản phát hành chính thức lên GitHub Releases kèm Release Notes đầy đủ.

## 7. Concrete Examples
### Cấu hình ma trận phát hành đa nền tảng trong GitHub Actions (.github/workflows/release.yml):
```yaml
name: Cross-Platform Release Matrix
on:
  push:
    tags: ['v*']

jobs:
  matrix-test-and-package:
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: ['3.12']
    runs-on: ${{ matrix.os }}
    
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          
      - name: Run Test Suite
        run: |
          python -m pytest tests/ scripts/polyglot/tests/ -v
          
      - name: Package Release Artifact
        shell: bash
        run: |
          mkdir dist
          if [ "$RUNNER_OS" == "Windows" ]; then
            7z a dist/dex-skills-${{ matrix.os }}.zip .agents manifests scripts
          else
            tar -czf dist/dex-skills-${{ matrix.os }}.tar.gz .agents manifests scripts
          fi
```

## 8. Anti-Patterns & Common Traps
- **Releasing From Single OS:** Chỉ kiểm thử và đóng gói trên máy tính của trưởng nhóm (thường là macOS) rồi phát hành dẫn tới việc người dùng Windows bị lỗi.
- **Ignoring OS-Specific Line Endings:** Nén file zip cho Windows nhưng để nguyên ký tự ngắt dòng LF cho file batch `.bat` khiến file không chạy được.
- **Skipping Failure Isolation:** Dùng cờ `fail-fast: true` khiến khi 1 hệ điều hành gặp lỗi thì các hệ điều hành khác bị hủy, làm mất thông tin chẩn đoán.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: 100% các job trong ma trận (Windows, Linux, macOS) đều vượt qua kiểm thử thành công.
- **QG-04**: Mọi artifact phát hành đều có mã băm SHA-256 được công bố minh bạch.
- **QG-08**: Toàn bộ các script wrapper (`dex.ps1`, `dex.bat`, `dex.sh`) hoạt động hoàn hảo trên hệ điều hành tương ứng.

## 10. Security & Safety Boundaries
- Ký số các bản phát hành nhị phân bằng chứng chỉ số hợp lệ để tránh cảnh báo SmartScreen hoặc Gatekeeper.

## 11. Platform Adapters
- **CI Systems**: GitHub Actions Matrix, Azure Pipelines Multi-job, GitLab CI Parallel.

## 12. Deliverables & Output Artifacts
- File workflow kiểm thử và đóng gói ma trận hoàn chỉnh.
- Các gói phân phối nén chuẩn cho từng hệ điều hành.
- Tệp kiểm tra mã băm SHA-256 toàn vẹn.

## 13. Related & Complementary Skills
dex-windows-linux-path-compatibility, dex-toolchain-reproducibility-audit, dex-package-publishing-preflight

## 14. Realistic Usage Example
```powershell
# Chạy mô phỏng ma trận kiểm thử cục bộ bằng act
act -j matrix-test-and-package

# Tạo và kiểm tra mã băm SHA256 cho bản phát hành
Get-FileHash dist/* -Algorithm SHA256
```
