---
name: dex-sbom-verification
description: Generate, sign, and verify Software Bill of Materials (SBOM) using CycloneDX and SPDX standards, integrating Syft and Cosign to secure the software supply chain. Use when complying with cybersecurity supply-chain mandates.
---

# dex-sbom-verification

## 1. Purpose & Scope
Tạo lập, ký số điện tử và kiểm chứng danh mục thành phần phần mềm (Software Bill of Materials - SBOM) theo các tiêu chuẩn quốc tế (CycloneDX, SPDX); tích hợp các công cụ tự động hóa chuỗi cung ứng (Syft, Grype, Cosign, Sigstore) nhằm theo dõi nguồn gốc xuất xứ của từng thư viện phụ thuộc, bảo đảm tính toàn vẹn của mã nhị phân và tuân thủ các quy định an ninh chuỗi cung ứng (US Executive Order 14028).

## 2. When to Use
- Khách hàng doanh nghiệp hoặc cơ quan chính phủ yêu cầu cung cấp SBOM trước khi mua và triển khai phần mềm.
- Cần đối soát nhanh xem hệ thống có bị ảnh hưởng khi một lỗ hổng zero-day mới (như Log4j, XZ Utils) được công bố trên toàn cầu.
- Xây dựng quy trình xác thực chữ ký số cho container images trước khi cho phép chạy trên cụm Kubernetes production.

## 3. When NOT to Use
- Không tạo file SBOM tĩnh một lần rồi bỏ xó (SBOM bắt buộc phải được sinh tự động lại tại mỗi lần build phần mềm trong CI).
- Không chỉ tạo SBOM cho mã nguồn ứng dụng mà bỏ qua các gói hệ điều hành bên trong base container image.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Container image hoặc mã nguồn dự án.
- Khóa ký số (Cosign Keypair hoặc Sigstore OIDC keyless identity).
- Định dạng SBOM mong muốn (CycloneDX JSON hoặc SPDX).
- **Điều kiện tiên quyết**:
- CI pipeline có cài đặt công cụ `syft` và `cosign`.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- SBOM as the Ingredient List: Giống như danh sách thành phần trên bao bì thực phẩm, SBOM liệt kê chính xác mọi gói thư viện, phiên bản, tác giả, giấy phép và mã băm SHA-256 của từng file trong sản phẩm.
- Keyless Signing với Cosign/Sigstore: Sử dụng OpenID Connect của GitHub Actions để ký số tạm thời và ghi nhận chứng chỉ vào nhật ký công khai không thể sửa đổi (Rekor Transparency Log), loại bỏ nỗi lo quản lý khóa bí mật dài hạn.
- Admission Verification: Kubernetes Admission Controller (Kyverno/Cosign) tự động kiểm tra chữ ký số của container image; nếu image không có chữ ký hợp lệ từ CI của công ty, pod sẽ bị từ chối khởi động.
- **Quy tắc quyết định kỹ thuật**:
- Bắt buộc sinh SBOM định dạng CycloneDX JSON cho mọi bản build phát hành chính thức.
- Mọi container image deploy lên Production bắt buộc phải có chữ ký số Cosign hợp lệ đi kèm.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Kẻ tấn công xâm nhập vào Docker Registry và thay thế image ứng dụng bằng image chứa mã độc; do không có cơ chế kiểm chứng chữ ký số, Kubernetes vẫn thản nhiên chạy image độc hại.

## 6. Step-by-Step Execution Workflow
1. Biên dịch và đóng gói container image trong GitHub Actions.
2. Sử dụng công cụ `syft` để quét và sinh file SBOM (`sbom.cyclonedx.json`).
3. Đính kèm (Attest) file SBOM vào chính container image trên OCI Registry.
4. Ký số điện tử lên container image và bản khai SBOM bằng `cosign`.
5. Cấu hình chính sách Kyverno trên Kubernetes để chỉ cho phép các image có chữ ký số hợp lệ được phép chạy.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```yaml
# GitHub Actions: Tự động sinh SBOM và Ký số container image bằng Cosign
- name: Generate SBOM with Syft
  uses: anchore/sbom-action@v0
  with:
    image: ${{ env.IMAGE_NAME }}
    format: cyclonedx-json
    output-file: sbom.cyclonedx.json

- name: Sign Container Image and Attach SBOM
  run: |
    # Đính kèm SBOM vào OCI Registry
    cosign attest --yes --predicate sbom.cyclonedx.json --type cyclonedx ${{ env.IMAGE_NAME }}
    # Ký số image sử dụng GitHub OIDC Identity (Keyless)
    cosign sign --yes ${{ env.IMAGE_NAME }}
```

### Lệnh xác minh & thực thi:
```bash
# Xác minh chữ ký số của container image trực tiếp từ registry
cosign verify --certificate-identity-regexp "https://github.com/company/.*" --certificate-oidc-issuer "https://token.actions.githubusercontent.com" myregistry.azurecr.io/app:v5.0.0
```

## 8. Anti-Patterns & Common Traps
- Lưu trữ file SBOM ở một nơi riêng lẻ không liên kết với commit hoặc container digest cụ thể.
- Bỏ qua việc quét lỗ hổng trên chính file SBOM sau khi sinh ra.

## 9. Quality Gates & Acceptance Criteria
- 100% container images phát hành lên Production có file SBOM và chữ ký Cosign đi kèm.
- Cụm Kubernetes tự động chặn các image chưa được ký số.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Bảo vệ quyền ghi vào OCI registry và kiểm soát chặt chẽ quyền kích hoạt pipeline ký số.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ thống An ninh & SkillOps**: Tương thích GitHub Actions, SARIF, CycloneDX/SPDX, Semgrep, OWASP ZAP.

## 12. Deliverables & Output Artifacts
- File SBOM chuẩn CycloneDX JSON (`sbom.json`).
- Chứng nhận chữ ký số Cosign trên OCI Registry.

## 13. Related & Complementary Skills
dex-container-image-engineering, dex-vulnerability-remediation, dex-kubernetes-policy-enforcement

## 14. Realistic Usage Example
### Tình huống thực tế:
Khi lỗ hổng nghiêm trọng Log4j nổ ra trên toàn thế giới, các công ty khác mất 2 tuần rà soát thủ công từng máy chủ. Nhờ có hệ thống lưu trữ SBOM tập trung cho mọi container image, đội ngũ bảo mật chỉ mất đúng 45 giây chạy một câu lệnh truy vấn SBOM để xác định chính xác 3 microservices đang sử dụng thư viện bị lỗi và cập nhật bản vá ngay trong buổi sáng.
