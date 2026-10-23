---
name: dex-binary-provenance-matching
description: Verify cryptographic provenance, build attestation signatures, and SLSA Level 3/4 compliance between compiled executable binaries and their authoritative source repositories. Use when conducting authorized supply-chain security audits.
---

# dex-binary-provenance-matching

## 1. Purpose & Scope
Xác minh nguồn gốc mật mã (Cryptographic Provenance), chữ ký chứng thực bản dựng (Build Attestation) và mức độ tuân thủ tiêu chuẩn SLSA giữa file thực thi nhị phân đã biên dịch và kho mã nguồn gốc; ngăn ngừa các nguy cơ chèn mã độc trong chuỗi cung ứng phần mềm.

## 2. When to Use
- Khi kiểm toán an ninh chuỗi cung ứng trước khi triển khai các file nhị phân của bên thứ ba vào môi trường production.
- Khi xác minh tính xác thực của các bản phát hành nhị phân từ các dự án mã nguồn mở.
- Khi triển khai quy chuẩn SLSA (Supply-chain Levels for Software Artifacts) cho pipeline CI/CD nội bộ.

## 3. When NOT to Use
- Khi tiến hành kiểm thử các bản dựng thử nghiệm nội bộ cục bộ không yêu cầu chứng thực nguồn gốc.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** File nhị phân mục tiêu (ELF, PE, Mach-O), file chữ ký số, chứng chỉ x509, hoặc bản ghi in-toto / Sigstore Cosign attestation.
- **Quyền hạn truy cập:** Quyền chạy công cụ phân tích nhị phân và truy cập transparency log (Rekor).

## 5. Core Concepts & Taxonomy
- **SLSA Attestation:** Bản ghi chứng nhận bản dựng được ký số mô tả quy trình, môi trường và commit SHA đã tạo ra artifact.
- **Sigstore / Cosign:** Công nghệ ký số không khóa (keyless signing) dựa trên OpenID Connect và nhật ký minh bạch Rekor.
- **Deterministic Hash Matching:** So sánh mã băm SHA-256 của file nhị phân với bản ghi đã công bố trên kênh phân phối chính thức.

## 6. Step-by-Step Execution Workflow
1. Trích xuất mã băm mật mã (SHA-256, SHA-512) của file nhị phân mục tiêu.
2. Truy vấn chứng thực bản dựng (attestation predicate) từ Sigstore Rekor log hoặc tệp `.attestation` đính kèm.
3. Kiểm tra tính hợp lệ của chuỗi chứng chỉ x509 và danh tính người ký (OIDC Issuer, Repository Workflow).
4. So sánh commit SHA được ghi nhận trong attestation với commit trên authoritative git branch.
5. Đối chiếu môi trường build (GitHub Actions runner, hardened builder container) với chính sách SLSA yêu cầu.
6. Lập báo cáo kết luận mức độ tin cậy và chứng chỉ xuất xứ của file nhị phân.

## 7. Concrete Examples
### Xác minh chữ ký và chứng thực xuất xứ bằng Cosign:
```powershell
# Xác minh chữ ký bản dựng nhị phân qua Sigstore
cosign verify-blob `
  --certificate ./release-binary.cert `
  --signature ./release-binary.sig `
  --certificate-identity "https://github.com/my-org/my-repo/.github/workflows/release.yml@refs/heads/main" `
  --certificate-oidc-issuer "https://token.actions.githubusercontent.com" `
  ./target-executable.exe

# Kiểm tra bản ghi chứng thực nguồn gốc SLSA
cosign verify-blob-attestation `
  --type slsaprovenance `
  --certificate ./release-binary.cert `
  --signature ./release-binary.attestation `
  ./target-executable.exe
```

## 8. Anti-Patterns & Common Traps
- **Blind Hash Download:** Tải file hash từ cùng một máy chủ không bảo mật với file nhị phân mà không có xác thực chữ ký PGP/Cosign độc lập.
- **Ignoring Builder Identity:** Chỉ kiểm tra file có chữ ký nhưng không xác minh danh tính người ký có thuộc tổ chức được ủy quyền hay không.
- **Trusting Modifiable Tags:** Xác minh bản dựng dựa trên Git Tag thay vì dùng Git Commit SHA bất biến.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Chữ ký số và chuỗi chứng chỉ x509 của file nhị phân hoàn toàn hợp lệ.
- **QG-04**: Bản chứng thực nguồn gốc (attestation) liên kết chính xác tới commit SHA trong kho mã nguồn chính thức.
- **QG-09**: Mức độ tuân thủ SLSA đạt tối thiểu Level 3 (bản dựng được tạo từ môi trường cô lập, không thể sửa đổi).

## 10. Security & Safety Boundaries
- Cảnh báo và cô lập ngay lập tức các tệp nhị phân có chữ ký không hợp lệ hoặc danh tính người ký không trùng khớp với tác giả chính thức.

## 11. Platform Adapters
- **Tools**: Cosign, Rekor CLI, in-toto, slsa-verifier, GitHub CLI (`gh attestation verify`).

## 12. Deliverables & Output Artifacts
- Báo cáo xác minh nguồn gốc mật mã của file nhị phân.
- Bản sao dữ liệu attestation đã được giải mã.
- Chứng chỉ kết quả kiểm toán tuân thủ SLSA.

## 13. Related & Complementary Skills
dex-build-slsa-controls, dex-open-source-license-scanning, dex-sbom-binary-correlation

## 14. Realistic Usage Example
```powershell
# Xác minh attestation bản dựng bằng GitHub CLI
gh attestation verify target-binary.tar.gz --repo my-org/my-repo

# Kiểm tra mã băm SHA256 đối chiếu
Get-FileHash -Algorithm SHA256 ./target-binary.tar.gz
```
