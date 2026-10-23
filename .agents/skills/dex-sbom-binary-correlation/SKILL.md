---
name: dex-sbom-binary-correlation
description: Correlate declared Software Bill of Materials (SBOM) manifests in CycloneDX or SPDX format with actual strings, embedded libraries, and symbols found inside compiled binaries. Use when verifying supply-chain honesty and identifying undeclared dependencies.
---

# dex-sbom-binary-correlation

## 1. Purpose & Scope
Đối chiếu và tương quan giữa danh mục thành phần phần mềm được công bố (SBOM) theo định dạng CycloneDX/SPDX với các chuỗi ký tự, thư viện nhúng và bảng ký hiệu thực tế tìm thấy bên trong file nhị phân đã biên dịch; phát hiện các phụ thuộc khai báo thiếu hoặc mã nguồn mở bị che giấu.

## 2. When to Use
- Khi kiểm tra tính trung thực của SBOM do nhà cung cấp phần mềm cung cấp trước khi mua bản quyền.
- Khi xác minh xem một lỗ hổng bảo mật mới công bố (CVE) có thực sự hiện diện trong file nhị phân đang chạy hay không.
- Khi kiểm toán tuân thủ bản quyền mã nguồn mở (Open Source License Compliance).

## 3. When NOT to Use
- Khi dự án là ứng dụng monolith nội bộ đã có quy trình phân tích thành phần phụ thuộc trực tiếp từ lockfiles.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** File nhị phân mục tiêu, file SBOM công bố (CycloneDX JSON hoặc SPDX JSON).
- **Quyền hạn truy cập:** Quyền chạy công cụ quét thành phần nhị phân (Syft, Tern, strings, binwalk).

## 5. Core Concepts & Taxonomy
- **Declared vs. Observed SBOM:** Sự khác biệt giữa danh mục thành phần mà nhà phát triển tuyên bố (Declared) và những gì thực sự có mặt trong bản nhị phân cuối cùng (Observed).
- **Fingerprinting Embedded Libraries:** Nhận diện thư viện C/C++ nhúng tĩnh (static linking) thông qua các chuỗi bản quyền, bảng hằng số mã hóa, hoặc hàm đặc trưng.
- **PURL (Package URL):** Chuẩn định danh định dạng gói tin duy nhất (`pkg:cargo/tokio@1.28.0`, `pkg:npm/express@4.18.2`).

## 6. Step-by-Step Execution Workflow
1. Phân tích cú pháp file SBOM công bố (CycloneDX/SPDX) để trích xuất danh sách PURL và phiên bản.
2. Chạy công cụ phân tích nhị phân (Syft, cve-bin-tool) trực tiếp trên file thực thi để sinh danh mục quan sát được (Observed SBOM).
3. Thực hiện trích xuất chuỗi ký tự (strings) và bảng import để tìm các dấu hiệu nhận biết thư viện bên thứ ba.
4. So sánh hai danh mục: gắn cờ các thư viện có trong file nhị phân nhưng không được khai báo trong SBOM (Undeclared Dependencies).
5. Kiểm tra các thư viện có khai báo trong SBOM nhưng không tìm thấy dấu vết sử dụng (Dead Dependencies).
6. Xuất báo cáo chênh lệch (SBOM Discrepancy Matrix) kèm đánh giá rủi ro an ninh và bản quyền.

## 7. Concrete Examples
### Tạo SBOM quan sát từ nhị phân và đối chiếu với SBOM khai báo:
```powershell
# Tạo SBOM thực tế từ file nhị phân bằng Syft
syft packages file:./target-binary.exe -o cyclonedx-json=observed-sbom.json

# Chạy script Python đối chiếu giữa Declared và Observed SBOM
python -c "
import json
with open('declared-sbom.json') as f: dec = json.load(f)
with open('observed-sbom.json') as f: obs = json.load(f)

dec_comps = {c['name'] for c in dec.get('components', [])}
obs_comps = {c['name'] for c in obs.get('components', [])}

undeclared = obs_comps - dec_comps
print(f'Phat hien {len(undeclared)} thu vien khong khai bao: {undeclared}')
"
```

## 8. Anti-Patterns & Common Traps
- **Trusting Vendor SBOM Unchecked:** Chấp nhận tài liệu SBOM của đối tác mà không có bất kỳ bước kiểm tra đối soát độc lập nào trên file nhị phân thực tế.
- **Missing Static Links:** Bỏ sót các thư viện C/C++ nhúng tĩnh như OpenSSL, zlib, SQLite được compile trực tiếp vào file thực thi.
- **Ignoring Outdated Transitive Deps:** Chỉ liệt kê các thư viện cấp 1 mà che giấu các thư viện phụ thuộc bắc cầu chứa lỗ hổng bảo mật.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: 100% các thành phần nhị phân bên thứ ba tìm thấy đều có mặt trong SBOM đã phê duyệt.
- **QG-04**: Không có thư viện nào bị phát hiện sai lệch phiên bản so với bản công bố.
- **QG-09**: Độ phủ kiểm toán đối chiếu đạt tối thiểu 95% diện tích các file nhị phân phân phối.

## 10. Security & Safety Boundaries
- Phát hiện các thành phần phần mềm bị nhiễm mã độc hoặc các phiên bản thư viện đã bị thu hồi (yanked/deprecated) vì lý do bảo mật.

## 11. Platform Adapters
- **Tools**: Syft, Grype, cve-bin-tool, Binwalk, CycloneDX CLI, SPDX Tools.

## 12. Deliverables & Output Artifacts
- Ma trận sai lệch SBOM (Declared vs Observed).
- Danh sách các thư viện nhúng không khai báo.
- Báo cáo rủi ro lỗ hổng CVE tương ứng với các thành phần thực tế.

## 13. Related & Complementary Skills
dex-binary-provenance-matching, dex-open-source-license-scanning, dex-dependency-management

## 14. Realistic Usage Example
```powershell
# Quét lỗ hổng trực tiếp từ file nhị phân bằng Grype
grype file:./target-binary.exe

# Chuyển đổi và chuẩn hóa định dạng SBOM bằng cyclonedx-cli
cyclonedx-cli validate --input-file observed-sbom.json
```
