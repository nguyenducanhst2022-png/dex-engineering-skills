---
name: dex-artifact-signature-verification
description: Implement cryptographic artifact signing and verification workflows using Sigstore (Cosign), GPG, and transparency logs (Rekor). Use when securing container images, CLI binary distributions, and release tarballs against supply-chain tampering.
---

# dex-artifact-signature-verification

## 1. Purpose & Scope
Hiện thực hóa quy trình ký số mật mã và xác thực tính toàn vẹn của hiện vật phần mềm (Cryptographic Artifact Signing & Verification) sử dụng Sigstore (Cosign), GPG và sổ cái minh bạch công khai (Rekor Transparency Log); bảo vệ hình ảnh container Docker, tệp nhị phân CLI và tệp nén phát hành khỏi các cuộc tấn công giả mạo hoặc chèn mã độc trong chuỗi cung ứng.

## 2. When to Use
- Khi xuất bản tệp nhị phân cài đặt hoặc container image ra ngoài công chúng.
- Khi thiết lập chính sách kiểm soát nhập khẩu hình ảnh (Admission Controller) trên cụm Kubernetes: chỉ cho phép triển khai các container có chữ ký số hợp lệ.
- Khi thực hiện các yêu cầu an ninh chuỗi cung ứng cấp độ SLSA Level 3.

## 3. When NOT to Use
- Khi xây dựng các bản dựng thử nghiệm tạm thời trên máy trạm cá nhân.
- Khi kiểm tra chữ ký số SSL của tên miền web (HTTPS certificates).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Công cụ dòng lệnh `cosign` hoặc `gpg`, chứng chỉ số nhận diện danh tính không khóa (Keyless signing qua OIDC) hoặc cặp khóa riêng/khóa công.
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; bảo vệ toàn vẹn tài sản kỹ nghệ và dữ liệu sản xuất.

## 5. Core Concepts & Taxonomy
- **Keyless Signing with Sigstore:** Tận dụng danh tính OpenID Connect (OIDC) của GitHub Actions để cấp phát chứng chỉ số ngắn hạn (Fulcio) và ghi lại dấu vết chữ ký vào sổ cái công khai (Rekor) mà không cần quản lý khóa riêng.
- **Cryptographic Transparency Log:** Sổ cái bất biến chỉ ghi nối tiếp (Append-only) chứng minh chữ ký đã được tạo ra ở một thời điểm xác định và không thể bị sửa đổi hồi tố.
- **Kubernetes Admission Verification:** Tự động từ chối chạy bất kỳ Pod nào có container image chưa được ký bởi khóa của tổ chức.

## 6. Step-by-Step Execution Workflow
1. Biên dịch tệp nhị phân hoặc đóng gói hình ảnh container trong đường ống CI.
2. Tạo chữ ký số điện tử cho hiện vật bằng Cosign hoặc GPG.
3. Ghi nhận chữ ký số và chứng chỉ vào sổ cái minh bạch Rekor.
4. Tại môi trường tiếp nhận hoặc máy trạm người dùng, thực hiện lệnh xác minh chữ ký `cosign verify`.
5. Đối chiếu danh tính người ký (Signer Identity) với kho mã nguồn chính thức trước khi cho phép cài đặt.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```bash
# Signing container image keylessly via Sigstore in GitHub Actions
cosign sign --yes ghcr.io/nguyenducanhst2022-png/dex-companion:v6.0.0

# Verifying container image signature and identity
cosign verify ghcr.io/nguyenducanhst2022-png/dex-companion:v6.0.0 \
  --certificate-identity "https://github.com/nguyenducanhst2022-png/dex-engineering-skills/.github/workflows/release.yml@refs/tags/v6.0.0" \
  --certificate-oidc-issuer "https://token.actions.githubusercontent.com"

# Signing standalone release tarball with GPG
gpg --armor --detach-sign release-v6.0.0.tar.gz
# Verifying GPG detached signature
gpg --verify release-v6.0.0.tar.gz.asc release-v6.0.0.tar.gz
```

## 8. Anti-Patterns & Common Traps
- Lưu trữ khóa riêng tư GPG Private Key không mã hóa trong biến môi trường CI thông thường mà không có mật khẩu bảo vệ.
- Người dùng tải tệp nhị phân từ Internet về và thực thi bằng lệnh `curl | bash` mà không kiểm tra chữ ký số hoặc mã băm SHA-256.
- Bỏ qua bước xác minh danh tính người ký (`certificate-identity`), khiến kẻ tấn công có thể tự ký bằng chứng chỉ rác của họ và qua mặt kiểm tra.

## 9. Quality Gates & Acceptance Criteria
- QG-01: 100% các bản phát hành sản xuất đều có chữ ký số mật mã hợp lệ và được ghi nhận vào sổ cái Rekor.
- QG-02: Lệnh `cosign verify` hoàn thành thành công với mã thoát exit code 0.
- QG-03: Cụm Kubernetes tự động chặn đứng việc triển khai container chưa có chữ ký số.

## 10. Security & Safety Boundaries
- Ngăn chặn các cuộc tấn công chuỗi cung ứng kiểu SolarWinds thông qua việc đảm bảo mọi tệp nhị phân đều có xuất xứ và chữ ký số không thể chối bỏ.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Quy trình tự động hóa ký số hiện vật `.github/workflows/sign-artifacts.yml`.
1. Tệp chữ ký số đính kèm bản phát hành `release.tar.gz.asc`.

## 13. Related & Complementary Skills
- [`dex-container-image-signing-cosign`](.agents/skills/dex-container-image-signing-cosign/SKILL.md)
- [`dex-slsa-provenance-verification`](.agents/skills/dex-slsa-provenance-verification/SKILL.md)
- [`dex-code-signing-release-process`](.agents/skills/dex-code-signing-release-process/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Hệ thống CI/CD bị hacker xâm nhập và cố tình thay đổi tệp nhị phân cài đặt trên máy chủ phát hành. Nhờ `dex-artifact-signature-verification`, khách hàng khi tải về chạy lệnh kiểm tra chữ ký phát hiện chữ ký số bị sai lệch và từ chối chạy tệp, kịp thời cảnh báo cho đội bảo mật ngăn chặn một thảm họa chuỗi cung ứng quy mô lớn.
