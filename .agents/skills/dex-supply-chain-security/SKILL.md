---
name: dex-supply-chain-security
description: Secure software supply chain, Software Bill of Materials (SBOM) generation, dependency pinning and auditing, vulnerable package mitigation, container base image scanning, and build provenance with SLSA. Use when auditing third-party dependencies or securing CI/CD builds.
---

# dex-supply-chain-security

## 1. Purpose & Scope
Bảo vệ an ninh chuỗi cung ứng phần mềm (Software Supply Chain Security); tự động sinh Bản kê khai thành phần phần mềm (Software Bill of Materials - SBOM), cố định phiên bản gói phụ thuộc (Dependency Pinning), kiểm toán lỗ hổng bảo mật thư viện bên thứ ba (Dependency Auditing với OSV / Snyk / Dependabot), quét ảnh gốc container (Trivy), và đảm bảo nguồn gốc tin cậy của bản build theo tiêu chuẩn SLSA (Supply-chain Levels for Software Artifacts).

## 2. When to Use
- Khi cần đáp ứng các tiêu chuẩn bảo mật doanh nghiệp (SOC2, ISO 27001, Executive Order 14028) yêu cầu xuất trình SBOM.
- Khi các gói phụ thuộc npm/pip/cargo liên tục phát hiện lỗ hổng bảo mật nghiêm trọng (CVEs) hoặc tấn công chuỗi cung ứng (Typosquatting, Malicious Packages).
- Khi các base image container chứa hàng trăm lỗ hổng bảo mật đã lỗi thời.

## 3. When NOT to Use
- Rà soát logic nghiệp vụ tự viết trong ứng dụng (dùng `dex-security-audit`).
- Quản lý phiên bản phát hành ứng dụng (dùng `dex-semantic-version-automation`).

## 4. Prerequisites & Input Context
**Đầu vào cần thiết:**
- File khóa phụ thuộc (Lockfiles: `package-lock.json`, `pnpm-lock.yaml`, `poetry.lock`, `Cargo.lock`).
- Dockerfiles và Container Images.
- Yêu cầu định dạng SBOM: CycloneDX JSON hoặc SPDX.

**Điều kiện tiên quyết:**
- Sử dụng package manager có cơ chế xác thực mã băm toàn vẹn (Integrity Hash verification).

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**: Nắm vững cơ chế vận hành theo chuẩn Agent Skills, tuân thủ nghiêm ngặt tính xác định và ranh giới trách nhiệm.
- **Quy tắc quyết định kỹ thuật**:
- **Chặn Build Khi Có CVE Mức CRITICAL**: Nếu bất kỳ thư viện phụ thuộc nào phát hiện lỗ hổng mức CRITICAL có điểm CVSS >= 9.0 và đã có bản vá, pipeline CI bắt buộc phải fail ngay lập tức.
- **Lockfile Bắt Buộc Trong Git**: Mọi thay đổi về thư viện đều phải commit file lockfile; cấm chạy `npm install` không có lockfile trên máy CI (`npm ci` / `pnpm install --frozen-lockfile`).
- **Tối Thiểu Hóa Base Image Container**: Luôn ưu tiên dùng hình ảnh container tối giản (Distroless, Alpine, Scratch) để giảm thiểu diện tích bề mặt tấn công.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Cài nhầm gói mã độc do gõ sai tên (Typosquatting - ví dụ: `lodas-js`)**: Mã độc đánh cắp biến môi trường -> Khắc phục: Sử dụng công cụ Socket.dev hoặc Socket CLI để chặn cài đặt gói lạ.
- **Container production chứa hàng trăm CVE do dùng `node:latest`**: Do chứa toàn bộ công cụ compiler của Debian -> Khắc phục: Đổi sang `cgr.dev/chainguard/node` hoặc `gcr.io/distroless/nodejs` sạch lỗ hổng.

## 6. Step-by-Step Execution Workflow
1. Khóa chặt phiên bản mọi phụ thuộc bằng tệp lockfile chuẩn mực; cấm sử dụng phiên bản mở tự do (`*` hoặc `^`).
2. Tự động quét kiểm toán lỗ hổng phụ thuộc trong CI bằng `npm audit`, `pip-audit`, hoặc `cargo audit`.
3. Thiết lập công cụ tự động cập nhật bản vá bảo mật (Dependabot / Renovate Bot) với chiến lược tự động merge cho các bản vá lỗi patch.
4. Tự động sinh tệp SBOM theo chuẩn CycloneDX (`bom.json`) trong quy trình đóng gói phần mềm.
5. Quét lỗ hổng của base image container bằng Trivy: Chặn đứng các bản build có chứa CVE mức CRITICAL hoặc HIGH chưa có bản vá.
6. Ký số artifact và xuất trình chứng chỉ nguồn gốc xuất xứ (Provenance Attestation) bằng Sigstore Cosign.

## 7. Concrete Examples
### Ví dụ triển khai chuẩn mực:
```yaml
# .github/workflows/sbom-scan.yml
name: Supply Chain Security
on: [push]
jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Generate SBOM
        uses: anchore/sbom-action@v0
        with:
          format: 'cyclonedx-json'
          output-file: 'sbom.cyclonedx.json'
      - name: Scan SBOM with Grype
        uses: anchore/scan-action@v3
        with:
          sbom: 'sbom.cyclonedx.json'
          fail-build: true
          severity-cutoff: 'critical'
```

### Lệnh xác minh & thực thi:
- Quét lỗ hổng dependency: `npm audit --audit-level=high` hoặc `pip-audit`
- Sinh SBOM bằng Syft: `syft dir:. -o cyclonedx-json=bom.json`
- Quét container image bằng Trivy: `trivy image --severity HIGH,CRITICAL my-app:latest`

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước kiểm tra biên và giả định hệ thống luôn ở trạng thái lý tưởng.
- **Anti-Pattern 2**: Không ghi nhận nhật ký kiểm toán hoặc bỏ qua việc xử lý ngoại lệ lúc runtime.
- **Trap**: Bỏ qua các rào chắn an toàn hoặc cố tình chạy script không qua kiểm thử tự động.

## 9. Quality Gates & Acceptance Criteria
- QG-03: 0 lỗ hổng mức CRITICAL chưa được giải quyết trong dependencies và base image.
- QG-10: Tệp SBOM (CycloneDX / SPDX) được tạo và đính kèm vào mỗi bản phát hành.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động trước khi coi là hoàn thành.

## 10. Security & Safety Boundaries
- Xác thực nguồn gốc package registry: Cấu hình scoped registry để tránh tấn công thay thế phụ thuộc (Dependency Confusion).
- Không bao giờ thực thi mã nguồn hoặc thay đổi cấu hình trên môi trường sản xuất mà thiếu cơ chế rollback an toàn.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Có thể kích hoạt trực tiếp từ terminal hoặc extension tương thích trong VS Code / Cursor / Windsurf.

## 12. Deliverables & Output Artifacts
- Tệp Bản kê khai thành phần phần mềm (`bom.json`).
- Báo cáo quét lỗ hổng bảo mật Trivy/Audit.
- Cấu hình cập nhật phụ thuộc tự động (`.github/dependabot.yml` hoặc `renovate.json`).

## 13. Related & Complementary Skills
- `dex-development-workflow`: Quy trình phát triển tiêu chuẩn.
- `dex-code-verification`: Xác minh chất lượng và tính đúng đắn của mã nguồn.
- `dex-master-orchestrator`: Bộ điều phối trung tâm kết nối kỹ năng này với các kỹ năng khác trong hệ thống.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư hoặc AI Agent tiếp nhận yêu cầu liên quan đến **dex-supply-chain-security**.
1. Đọc kỹ đầu vào và các ràng buộc kỹ thuật tại mục 4.
2. Thực thi tuần tự 6 bước trong Workflow tại mục 6.
3. Chạy các lệnh kiểm chứng tại mục 7 và đối chiếu với Quality Gates tại mục 9.
4. Đóng gói deliverables theo danh sách tại mục 12 và báo cáo kết quả kèm bằng chứng xác thực.
