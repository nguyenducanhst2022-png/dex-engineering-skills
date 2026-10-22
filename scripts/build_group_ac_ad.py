# -*- coding: utf-8 -*-
"""
DEX SKILLOPS — BUILDER FOR GROUPS AC & AD (Skills 281–300)
Group AC: Software Trust & Distribution (281–290)
Group AD: Advanced SkillOps Governance (291–300)
"""

import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SKILLS_DIR = os.path.join(ROOT, ".agents", "skills")

GROUP_AC_AD_SKILLS = [
    # --- GROUP AC: Software Trust & Distribution ---
    {
        "id": "dex-open-source-license-scanning",
        "index": 281,
        "group": "Group AC",
        "domain": "Software Trust & Distribution",
        "description": "Automate open-source software (OSS) license compliance scanning, detecting copyleft contamination (GPL/AGPL), dual-licensing clauses, and license incompatibility risks across dependency trees. Use when gating release builds, preparing M&A technical audits, or generating Software Bill of Materials (SBOM).",
        "purpose": "Tự động hóa quy trình quét và thẩm định tính tuân thủ giấy phép mã nguồn mở (Open Source License Compliance Scanning); phát hiện sớm các nguy cơ ô nhiễm giấy phép bản quyền lây lan (Copyleft Contamination như GPL, AGPL trong phần mềm thương mại độc quyền), các điều khoản cấp phép kép (Dual-Licensing) và các xung đột giấy phép không tương thích trong toàn bộ cây phụ thuộc; phục vụ nghiệm thu bản dựng phát hành và thẩm tra kỹ thuật M&A.",
        "when_use": [
            "Trước khi đóng gói phát hành phần mềm thương mại độc quyền cho khách hàng doanh nghiệp.",
            "Khi thêm mới một thư viện mã nguồn mở vào dự án cần kiểm tra giấy phép có phù hợp với chính sách công ty hay không.",
            "Khi tạo bảng danh mục vật liệu phần mềm (Software Bill of Materials - SBOM) chuẩn SPDX/CycloneDX."
        ],
        "when_not_use": [
            "Khi toàn bộ dự án đã được phát hành công khai dưới giấy phép AGPL.",
            "Khi kiểm tra lỗi cú pháp mã nguồn thông thường."
        ],
        "prereqs": "Tệp khóa phụ thuộc (`package-lock.json`, `poetry.lock`, `Cargo.lock`), công cụ quét giấy phép (FOSSA, ScanCode Toolkit hoặc `license-checker`).",
        "concepts": [
            "Permissive vs Copyleft: Phân biệt giữa giấy phép thoáng (Permissive: MIT, Apache-2.0, BSD - cho phép dùng trong phần mềm đóng mã) và giấy phép bản quyền lây lan (Copyleft: GPL, AGPL - bắt buộc phải mở toàn bộ mã nguồn liên kết).",
            "Transitive Dependency Contamination: Một thư viện MIT có thể kéo theo một thư viện con gián tiếp mang giấy phép GPL-3.0 làm lây nhiễm toàn bộ dự án.",
            "SPDX Standard Identifiers: Chuẩn hóa tên định danh giấy phép quốc tế (ví dụ: `Apache-2.0`, `MIT`, `GPL-3.0-only`)."
        ],
        "steps": [
            "Trích xuất danh sách toàn bộ các phụ thuộc trực tiếp và bắc cầu từ tệp lockfile.",
            "Quét và bóc tách các tệp `LICENSE`, `COPYING` và tiêu đề mã nguồn của từng gói phụ thuộc.",
            "Chuẩn hóa tên giấy phép sang định dạng chuẩn SPDX Identifier.",
            "Đối chiếu danh sách giấy phép với chính sách cho phép (Allowlist Policy) của tổ chức.",
            "Nếu phát hiện giấy phép cấm (như AGPL trong dự án SaaS đóng mã), kích hoạt cảnh báo chặn đường ống CI."
        ],
        "code_lang": "json",
        "code_example": """{
  "$schema": "https://dex.dev/schemas/license-policy.json",
  "policyName": "Commercial Proprietary SaaS Policy",
  "allowedLicenses": [
    "MIT",
    "Apache-2.0",
    "BSD-2-Clause",
    "BSD-3-Clause",
    "ISC"
  ],
  "prohibitedLicenses": [
    "GPL-1.0-only", "GPL-2.0-only", "GPL-3.0-only",
    "AGPL-3.0-only", "SSPL-1.0"
  ],
  "reviewRequired": [
    "MPL-2.0", "LGPL-3.0-only", "EPL-2.0"
  ]
}""",
        "antipatterns": [
            "Chỉ kiểm tra giấy phép của các phụ thuộc trực tiếp trong `package.json` mà bỏ qua hàng trăm phụ thuộc bắc cầu (Transitive Dependencies) trong lockfile.",
            "Tự ý nhúng mã nguồn có giấy phép GPL vào phần mềm đóng mã của công ty rồi bán cho khách hàng (vi phạm pháp luật bản quyền nghiêm trọng).",
            "Bỏ qua các phụ thuộc không có giấy phép rõ ràng (Unlicensed Code / No License - mặc định được pháp luật bảo lưu toàn bộ quyền)."
        ],
        "quality_gates": [
            "QG-01: 100% các phụ thuộc trực tiếp và gián tiếp đều được định danh giấy phép chuẩn SPDX.",
            "QG-02: Không có bất kỳ gói phụ thuộc nào chứa giấy phép cấm (Prohibited Licenses) lọt vào bản dựng phát hành.",
            "QG-03: Cổng CI tự động chặn merge pull request nếu phát hiện vi phạm chính sách giấy phép."
        ],
        "security": "Ngăn ngừa các rủi ro pháp lý tranh chấp sở hữu trí tuệ có thể dẫn đến việc doanh nghiệp bị kiện hoặc bị ép buộc công khai toàn bộ mã nguồn bí mật kinh doanh.",
        "deliverables": [
            "Báo cáo kiểm toán giấy phép phụ thuộc `LICENSE_COMPLIANCE_AUDIT.md`.",
            "Tệp cấu hình chính sách kiểm soát giấy phép tự động `.license-policy.json`."
        ],
        "related": ["dex-third-party-attribution", "dex-dependency-vulnerability-intelligence", "dex-sbom-verification"],
        "scenario": "Doanh nghiệp chuẩn bị thương vụ M&A bán công ty giá 50 triệu USD. Đội ngũ kiểm toán kỹ thuật của quỹ đầu tư yêu cầu quét giấy phép mã nguồn. Kỹ sư kích hoạt `dex-open-source-license-scanning`, phát hiện 2 thư viện nhỏ mang giấy phép GPL-3.0 lọt vào backend, kịp thời thay thế bằng thư viện tương đương mang giấy phép MIT, bảo vệ thành công giá trị thương vụ."
    },
    {
        "id": "dex-third-party-attribution",
        "index": 282,
        "group": "Group AC",
        "domain": "Software Trust & Distribution",
        "description": "Generate accurate, legally compliant NOTICE and THIRD_PARTY_NOTICES files, aggregating copyright statements, author credits, and license texts from vendored dependencies. Use when packaging desktop apps, mobile releases, or distributed on-premise appliances.",
        "purpose": "Tự động hóa việc tổng hợp và xuất bản tệp ghi nhận công lao bên thứ ba (`NOTICE` và `THIRD_PARTY_NOTICES.md`) tuân thủ nghiêm ngặt pháp lý; thu thập đầy đủ tuyên bố bản quyền (Copyright Statements), thông tin tác giả và nguyên văn nội dung giấy phép từ toàn bộ các gói thư viện được đóng gói kèm; phục vụ việc phát hành ứng dụng máy tính, ứng dụng di động hoặc giải pháp phần mềm tại chỗ (On-Premise).",
        "when_use": [
            "Trước khi đóng gói phát hành phần mềm phân phối (Desktop/Mobile/CLI) theo yêu cầu bắt buộc của các giấy phép Apache-2.0, MIT và BSD.",
            "Khi xây dựng trang 'Open Source Licenses' trong mục Cài đặt (Settings) của ứng dụng di động.",
            "Khi xuất bản thư viện mã nguồn mở ra cộng đồng và cần ghi nhận công lao các thành phần đã sử dụng."
        ],
        "when_not_use": [
            "Khi ứng dụng web nội bộ chỉ chạy trên máy chủ đám mây của chính công ty và không bao giờ phân phối nhị phân cho bên ngoài.",
            "Khi quản lý danh mục tài sản phần cứng."
        ],
        "prereqs": "Thư mục `node_modules` hoặc kho gói phụ thuộc đã tải đầy đủ, công cụ tự động tổng hợp thông báo (`license-checker` hoặc script Python/Go).",
        "concepts": [
            "Mandatory Attribution Clause: Hầu hết các giấy phép mã nguồn mở (kể cả MIT và Apache 2.0) đều bắt buộc bên phân phối phải đính kèm nguyên văn thông báo bản quyền và nội dung giấy phép trong sản phẩm phân phối.",
            "Apache NOTICE Preservation: Giấy phép Apache 2.0 yêu cầu mọi thông tin ghi nhận trong tệp `NOTICE` của thư viện gốc phải được bảo toàn nguyên vẹn trong tệp `NOTICE` của sản phẩm phái sinh.",
            "Multi-Ecosystem Aggregation: Khả năng thu thập thông báo bản quyền xuyên suốt nhiều hệ sinh thái trong cùng một sản phẩm (npm, PyPI, Cargo, NuGet)."
        ],
        "steps": [
            "Quét cây phụ thuộc và tìm kiếm toàn bộ các tệp `LICENSE*` và `NOTICE*` trong các gói được đóng gói.",
            "Trích xuất dòng bản quyền (ví dụ: `Copyright (c) 2024 Jane Doe`).",
            "Gom nhóm và định dạng các thông báo theo từng thành phần rõ ràng kèm đường dẫn kho mã nguồn.",
            "Xuất bản tệp chuẩn hóa `THIRD_PARTY_NOTICES.md` ở thư mục gốc của bản dựng phân phối.",
            "Kiểm tra tính đầy đủ của thông tin trước khi đóng gói tệp cài đặt (Installer)."
        ],
        "code_lang": "markdown",
        "code_example": """# Third-Party Software Notices & Licenses

This distribution includes third-party software components subject to the following licenses:

---

Component: Undici (v6.19.8)
- **License**: Apache-2.0
- **Copyright**: Copyright Node.js contributors. All rights reserved.
- **Repository**: https://github.com/nodejs/undici

```text
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
...
```""",
        "antipatterns": [
            "Phân phối tệp cài đặt phần mềm thương mại nhưng không đính kèm tệp `THIRD_PARTY_NOTICES` (vi phạm trực tiếp điều khoản của giấy phép MIT và Apache 2.0).",
            "Chỉ liệt kê tên gói mà không sao chép nguyên văn nội dung giấy phép của tác giả gốc.",
            "Xóa bỏ thông báo bản quyền của tác giả ban đầu khi chỉnh sửa mã nguồn mở."
        ],
        "quality_gates": [
            "QG-01: Tệp `THIRD_PARTY_NOTICES.md` chứa đầy đủ 100% các thành phần mã nguồn mở được đóng gói trong bản dựng.",
            "QG-02: Nguyên văn nội dung giấy phép và dòng Copyright của từng tác giả được bảo toàn nguyên vẹn.",
            "QG-03: Tệp thông báo bản quyền được tích hợp tự động vào mục 'About/Licenses' của giao diện ứng dụng."
        ],
        "security": "Đảm bảo tuân thủ đầy đủ nghĩa vụ pháp lý, triệt tiêu nguy cơ bị thu hồi quyền sử dụng mã nguồn mở do vi phạm điều khoản thông báo bản quyền.",
        "deliverables": [
            "Tệp ghi nhận bản quyền bên thứ ba hoàn chỉnh `THIRD_PARTY_NOTICES.md`.",
            "Kịch bản tự động cập nhật tài liệu bản quyền trong CI `generate-notices.py`."
        ],
        "related": ["dex-open-source-license-scanning", "dex-sbom-verification", "dex-documentation-as-code"],
        "scenario": "Phát hành ứng dụng desktop cho 50,000 khách hàng doanh nghiệp. Kỹ sư kích hoạt `dex-third-party-attribution` để quét toàn bộ 340 gói npm và Rust crates được nhúng trong ứng dụng, tự động tổng hợp thành tệp `THIRD_PARTY_NOTICES.md` chuẩn mực tích hợp vào menu Help của ứng dụng, đáp ứng 100% yêu cầu kiểm toán pháp lý."
    },
    {
        "id": "dex-artifact-signature-verification",
        "index": 283,
        "group": "Group AC",
        "domain": "Software Trust & Distribution",
        "description": "Implement cryptographic artifact signing and verification workflows using Sigstore (Cosign), GPG, and transparency logs (Rekor). Use when securing container images, CLI binary distributions, and release tarballs against supply-chain tampering.",
        "purpose": "Hiện thực hóa quy trình ký số mật mã và xác thực tính toàn vẹn của hiện vật phần mềm (Cryptographic Artifact Signing & Verification) sử dụng Sigstore (Cosign), GPG và sổ cái minh bạch công khai (Rekor Transparency Log); bảo vệ hình ảnh container Docker, tệp nhị phân CLI và tệp nén phát hành khỏi các cuộc tấn công giả mạo hoặc chèn mã độc trong chuỗi cung ứng.",
        "when_use": [
            "Khi xuất bản tệp nhị phân cài đặt hoặc container image ra ngoài công chúng.",
            "Khi thiết lập chính sách kiểm soát nhập khẩu hình ảnh (Admission Controller) trên cụm Kubernetes: chỉ cho phép triển khai các container có chữ ký số hợp lệ.",
            "Khi thực hiện các yêu cầu an ninh chuỗi cung ứng cấp độ SLSA Level 3."
        ],
        "when_not_use": [
            "Khi xây dựng các bản dựng thử nghiệm tạm thời trên máy trạm cá nhân.",
            "Khi kiểm tra chữ ký số SSL của tên miền web (HTTPS certificates)."
        ],
        "prereqs": "Công cụ dòng lệnh `cosign` hoặc `gpg`, chứng chỉ số nhận diện danh tính không khóa (Keyless signing qua OIDC) hoặc cặp khóa riêng/khóa công.",
        "concepts": [
            "Keyless Signing with Sigstore: Tận dụng danh tính OpenID Connect (OIDC) của GitHub Actions để cấp phát chứng chỉ số ngắn hạn (Fulcio) và ghi lại dấu vết chữ ký vào sổ cái công khai (Rekor) mà không cần quản lý khóa riêng.",
            "Cryptographic Transparency Log: Sổ cái bất biến chỉ ghi nối tiếp (Append-only) chứng minh chữ ký đã được tạo ra ở một thời điểm xác định và không thể bị sửa đổi hồi tố.",
            "Kubernetes Admission Verification: Tự động từ chối chạy bất kỳ Pod nào có container image chưa được ký bởi khóa của tổ chức."
        ],
        "steps": [
            "Biên dịch tệp nhị phân hoặc đóng gói hình ảnh container trong đường ống CI.",
            "Tạo chữ ký số điện tử cho hiện vật bằng Cosign hoặc GPG.",
            "Ghi nhận chữ ký số và chứng chỉ vào sổ cái minh bạch Rekor.",
            "Tại môi trường tiếp nhận hoặc máy trạm người dùng, thực hiện lệnh xác minh chữ ký `cosign verify`.",
            "Đối chiếu danh tính người ký (Signer Identity) với kho mã nguồn chính thức trước khi cho phép cài đặt."
        ],
        "code_lang": "bash",
        "code_example": """# Signing container image keylessly via Sigstore in GitHub Actions
cosign sign --yes ghcr.io/nguyenducanhst2022-png/dex-companion:v6.0.0

# Verifying container image signature and identity
cosign verify ghcr.io/nguyenducanhst2022-png/dex-companion:v6.0.0 \\
  --certificate-identity "https://github.com/nguyenducanhst2022-png/dex-engineering-skills/.github/workflows/release.yml@refs/tags/v6.0.0" \\
  --certificate-oidc-issuer "https://token.actions.githubusercontent.com"

# Signing standalone release tarball with GPG
gpg --armor --detach-sign release-v6.0.0.tar.gz
# Verifying GPG detached signature
gpg --verify release-v6.0.0.tar.gz.asc release-v6.0.0.tar.gz""",
        "antipatterns": [
            "Lưu trữ khóa riêng tư GPG Private Key không mã hóa trong biến môi trường CI thông thường mà không có mật khẩu bảo vệ.",
            "Người dùng tải tệp nhị phân từ Internet về và thực thi bằng lệnh `curl | bash` mà không kiểm tra chữ ký số hoặc mã băm SHA-256.",
            "Bỏ qua bước xác minh danh tính người ký (`certificate-identity`), khiến kẻ tấn công có thể tự ký bằng chứng chỉ rác của họ và qua mặt kiểm tra."
        ],
        "quality_gates": [
            "QG-01: 100% các bản phát hành sản xuất đều có chữ ký số mật mã hợp lệ và được ghi nhận vào sổ cái Rekor.",
            "QG-02: Lệnh `cosign verify` hoàn thành thành công với mã thoát exit code 0.",
            "QG-03: Cụm Kubernetes tự động chặn đứng việc triển khai container chưa có chữ ký số."
        ],
        "security": "Ngăn chặn các cuộc tấn công chuỗi cung ứng kiểu SolarWinds thông qua việc đảm bảo mọi tệp nhị phân đều có xuất xứ và chữ ký số không thể chối bỏ.",
        "deliverables": [
            "Quy trình tự động hóa ký số hiện vật `.github/workflows/sign-artifacts.yml`.",
            "Tệp chữ ký số đính kèm bản phát hành `release.tar.gz.asc`."
        ],
        "related": ["dex-container-image-signing-cosign", "dex-slsa-provenance-verification", "dex-code-signing-release-process"],
        "scenario": "Hệ thống CI/CD bị hacker xâm nhập và cố tình thay đổi tệp nhị phân cài đặt trên máy chủ phát hành. Nhờ `dex-artifact-signature-verification`, khách hàng khi tải về chạy lệnh kiểm tra chữ ký phát hiện chữ ký số bị sai lệch và từ chối chạy tệp, kịp thời cảnh báo cho đội bảo mật ngăn chặn một thảm họa chuỗi cung ứng quy mô lớn."
    },
    {
        "id": "dex-dependency-vulnerability-intelligence",
        "index": 284,
        "group": "Group AC",
        "domain": "Software Trust & Distribution",
        "description": "Triage and remediate software dependency vulnerabilities using OSV, NVD, and GitHub Advisory databases, prioritizing by Exploit Prediction Scoring System (EPSS), CISA KEV catalogs, and call-graph reachability analysis. Use when cutting vulnerability noise and fixing critical supply-chain risks.",
        "purpose": "Sàng lọc, phân loại và khắc phục các lỗ hổng bảo mật trong phụ thuộc phần mềm (Dependency Vulnerability Intelligence); đối chiếu dữ liệu từ OSV, NVD và GitHub Security Advisories; ưu tiên xử lý dựa trên điểm số dự đoán khả năng bị khai thác (EPSS), danh mục lỗ hổng bị khai thác trong thực tế (CISA KEV) và phân tích tính chạm tới được trong đồ thị gọi hàm (Reachability Analysis); giảm 90% cảnh báo rác và tập trung vá các lỗ hổng nguy hiểm thực sự.",
        "when_use": [
            "Khi công cụ quét lỗ hổng (Snyk, Dependabot, Trivy) báo cáo hàng trăm lỗ hổng CVE khiến đội ngũ phát triển bị quá tải không biết sửa cái nào trước.",
            "Khi cần đánh giá xem một lỗ hổng CVE được báo cáo có thực sự bị ứng dụng gọi tới hay chỉ nằm ở đoạn code chết (Dead Code).",
            "Khi chuẩn bị báo cáo kiểm toán bảo mật chuỗi cung ứng phần mềm định kỳ."
        ],
        "when_not_use": [
            "Khi quét lỗ hổng cấu hình máy chủ hoặc mạng hạ tầng (dùng scanner hạ tầng).",
            "Khi kiểm tra lỗi logic nghiệp vụ trong mã nguồn do chính mình viết."
        ],
        "prereqs": "Bản kê SBOM (Software Bill of Materials), công cụ quét lỗ hổng dựa trên cơ sở dữ liệu OSV (`osv-scanner`), quyền truy vấn API điểm số EPSS.",
        "concepts": [
            "EPSS (Exploit Prediction Scoring System): Điểm số xác suất từ 0.0 đến 1.0 dự đoán khả năng một lỗ hổng CVE sẽ bị khai thác trong thực tế trong 30 ngày tới.",
            "CISA KEV Catalog: Danh sách các lỗ hổng đã được cơ quan an ninh mạng xác nhận đang bị hacker khai thác tích cực ngoài đời thực (Bắt buộc phải vá khẩn cấp).",
            "Call-Graph Reachability Analysis: Kiểm tra xem mã nguồn ứng dụng có thực sự gọi tới phương thức chứa lỗ hổng bên trong thư viện hay không."
        ],
        "steps": [
            "Quét toàn bộ cây phụ thuộc bằng `osv-scanner --lockfile=package-lock.json`.",
            "Truy vấn điểm số EPSS và trạng thái CISA KEV cho từng mã định danh CVE phát hiện được.",
            "Phân tích đồ thị gọi hàm (Call Graph) để lọc bỏ các lỗ hổng nằm ở các module không bao giờ được kích hoạt.",
            "Ưu tiên xử lý ngay lập tức các lỗ hổng thuộc nhóm: Nằm trong CISA KEV HOẶC (EPSS > 0.5 VÀ Reachable).",
            "Tự động tạo Pull Request nâng cấp phiên bản thư viện đã được vá lỗi."
        ],
        "code_lang": "python",
        "code_example": """# Vulnerability Triage Prioritization Algorithm
import requests

def triage_vulnerability(cve_id: str, is_reachable: bool) -> str:
    # 1. Check CISA Known Exploited Vulnerabilities (KEV)
    # 2. Fetch EPSS probability score
    epss_res = requests.get(f"https://api.first.org/data/v1/epss?cve={cve_id}").json()
    epss_score = float(epss_res['data'][0]['epss']) if epss_res.get('data') else 0.0

    if epss_score > 0.3 and is_reachable:
        return "CRITICAL_IMMEDIATE_PATCH"
    elif is_reachable:
        return "HIGH_SCHEDULED_PATCH"
    elif epss_score > 0.5:
        return "MEDIUM_DEFENSE_IN_DEPTH"
    else:
        return "LOW_NO_IMMEDIATE_ACTION" """,
        "antipatterns": [
            "Chỉ dựa vào điểm số CVSS cơ bản (ví dụ CVSS 9.8) để hoảng loạn vá lỗi, trong khi lỗ hổng đó không có mã khai thác và ứng dụng không hề gọi tới phương thức đó.",
            "Phớt lờ các lỗ hổng có điểm CVSS trung bình (6.5) nhưng đang bị hacker khai thác ồ ạt trên mạng (nằm trong danh mục CISA KEV).",
            "Nâng cấp đồng loạt 50 thư viện cùng lúc mà không chạy lại bộ kiểm thử hồi quy làm gãy toàn bộ ứng dụng."
        ],
        "quality_gates": [
            "QG-01: 100% các lỗ hổng nằm trong danh mục CISA KEV được khắc phục trong vòng 48 giờ.",
            "QG-02: Phân tích tính chạm tới được (Reachability Analysis) được áp dụng để phân loại 100% các cảnh báo CVE.",
            "QG-03: Không có bất kỳ lỗ hổng Critical nào còn tồn tại trên đường dẫn mã nguồn thực thi chính."
        ],
        "security": "Thường xuyên cập nhật cơ sở dữ liệu lỗ hổng hàng ngày; chủ động gỡ bỏ các thư viện đã bị tác giả bỏ hoang (Abandoned Packages).",
        "deliverables": [
            "Báo cáo phân loại thông minh lỗ hổng phụ thuộc `VULNERABILITY_INTELLIGENCE_REPORT.md`.",
            "Script tự động đối soát CVE với cơ sở dữ liệu EPSS và CISA KEV."
        ],
        "related": ["dex-open-source-license-scanning", "dex-vulnerability-remediation", "dex-sbom-verification"],
        "scenario": "Báo cáo bảo mật định kỳ phát hiện 142 lỗ hổng CVE trong dự án, khiến đội dev mất ăn mất ngủ. Kỹ sư kích hoạt `dex-dependency-vulnerability-intelligence`, phân tích Reachability và điểm EPSS, sàng lọc chỉ còn 3 lỗ hổng thực sự nguy hiểm đang bị khai thác và có thể gọi tới, giúp đội ngũ tập trung vá xong trong 2 tiếng thay vì tốn 3 tuần vô ích."
    },
    {
        "id": "dex-secret-rotation-drills",
        "index": 285,
        "group": "Group AC",
        "domain": "Software Trust & Distribution",
        "description": "Design zero-downtime secret rotation drills for database credentials, API signing keys, JWT secrets, and TLS certificates using dual-key overlaps and automated validation. Use when validating security incident readiness or meeting regulatory compliance mandates.",
        "purpose": "Thiết kế và diễn tập quy trình quay vòng khóa bí mật không gián đoạn dịch vụ (Zero-Downtime Secret Rotation Drills) cho thông tin đăng nhập cơ sở dữ liệu, khóa ký API, mã bí mật JWT và chứng chỉ số TLS; ứng dụng mô hình gối đầu hai khóa (Dual-Key Overlap), kiểm tra xác thực tự động và cơ chế hoàn tác khẩn cấp; phục vụ nâng cao năng lực ứng phó sự cố rò rỉ khóa và đáp ứng các tiêu chuẩn tuân thủ SOC 2, PCI-DSS.",
        "when_use": [
            "Khi thực hiện diễn tập quay vòng khóa bảo mật định kỳ (hàng quý) theo yêu cầu của kiểm toán bảo mật.",
            "Khi nghi ngờ một khóa API của bên thứ ba hoặc mật khẩu cơ sở dữ liệu bị lộ ra ngoài.",
            "Trước khi hết hạn chứng chỉ số TLS hoặc khóa ký mã nguồn."
        ],
        "when_not_use": [
            "Khi tạo khóa mới lần đầu cho một hệ thống chưa bao giờ chạy trên môi trường thực tế.",
            "Khi chỉ thay đổi mật khẩu tài khoản người dùng cá nhân."
        ],
        "prereqs": "Hệ thống quản lý bí mật (AWS Secrets Manager, HashiCorp Vault hoặc GCP Secret Manager), quyền truy cập cấu hình dịch vụ.",
        "concepts": [
            "Dual-Secret Grace Period: Trong giai đoạn chuyển tiếp, hệ thống hỗ trợ đồng thời cả khóa cũ và khóa mới (chấp nhận xác thực bằng cả 2 khóa) để các máy khách có thời gian cập nhật.",
            "Zero-Downtime Database Rotation: Tạo tài khoản database thứ hai với mật khẩu mới, cập nhật chuỗi kết nối ứng dụng, kiểm tra kết nối thành công rồi mới vô hiệu hóa tài khoản cũ.",
            "Automated Canary Validation: Gửi request thử nghiệm có chữ ký của khóa mới trước khi chính thức hủy bỏ khóa cũ."
        ],
        "steps": [
            "Tạo khóa bí mật mới (Secret B) trong hệ thống Secret Manager.",
            "Cập nhật máy chủ xác thực để chấp nhận cả Secret A (cũ) và Secret B (mới).",
            "Triển khai Secret B tới các ứng dụng máy khách để bắt đầu sử dụng khóa mới để ký request.",
            "Theo dõi nhật ký kiểm toán trong 24 giờ cho đến khi 100% lưu lượng chuyển sang Secret B.",
            "Vô hiệu hóa và xóa bỏ hoàn toàn Secret A cũ khỏi hệ thống."
        ],
        "code_lang": "typescript",
        "code_example": """// Dual-Key JWT Verification Supporting Zero-Downtime Rotation
import jwt from 'jsonwebtoken';

const ACTIVE_KEYS = {
  'key-2026-v2': process.env.JWT_SECRET_PRIMARY,   // New Key
  'key-2025-v1': process.env.JWT_SECRET_SECONDARY, // Old Key (Grace Period)
};

export function verifyTokenWithRotation(token: string): any {
  const decodedHeader = jwt.decode(token, { complete: true })?.header;
  const keyId = decodedHeader?.kid || 'key-2025-v1';
  const secret = ACTIVE_KEYS[keyId as keyof typeof ACTIVE_KEYS];

  if (!secret) {
    throw new Error('Invalid or expired key identifier');
  }

  return jwt.verify(token, secret);
}""",
        "antipatterns": [
            "Đổi mật khẩu cơ sở dữ liệu ngay lập tức trên máy chủ mà không cập nhật trước cho ứng dụng, làm sập toàn bộ hệ thống ngay trong giây tiếp theo.",
            "Đổi khóa bí mật mà không có kế hoạch dự phòng (Rollback Plan) khi phát sinh lỗi không tương thích.",
            "Quay vòng khóa bằng tay thủ công qua giao diện web, dễ gõ nhầm ký tự và không thể tự động hóa."
        ],
        "quality_gates": [
            "QG-01: Quá trình quay vòng khóa diễn ra đạt 100% Zero-Downtime, không có bất kỳ request hợp lệ nào bị lỗi 401/500.",
            "QG-02: Khóa cũ được thu hồi và xóa bỏ hoàn toàn sau khi giai đoạn gối đầu kết thúc.",
            "QG-03: Diễn tập quay vòng khóa được ghi lại đầy đủ bằng biên bản kiểm toán có đóng dấu thời gian."
        ],
        "security": "Không bao giờ gửi khóa bí mật qua các kênh liên lạc không an toàn (Slack, Email); chỉ truyền tải qua hệ thống Secret Manager có mã hóa.",
        "deliverables": [
            "Kịch bản diễn tập quay vòng khóa tự động `secret-rotation-drill.sh`.",
            "Biên bản nghiệm thu diễn tập quay vòng khóa `SECRET_ROTATION_REPORT.md`."
        ],
        "related": ["dex-crypto-key-rotation-kms", "dex-secrets-management", "dex-security-audit"],
        "scenario": "Doanh nghiệp tổ chức diễn tập ứng phó sự cố rò rỉ khóa JWT bí mật phục vụ kiểm toán SOC 2 Type II. Kỹ sư kích hoạt `dex-secret-rotation-drills`, áp dụng cơ chế xác thực gối đầu hai khóa `kid` trong 24 giờ, luân chuyển khóa mới cho 500,000 phiên đăng nhập mà không làm bất kỳ người dùng nào bị văng ra khỏi ứng dụng, hoàn thành diễn tập đạt điểm xuất sắc."
    },
    {
        "id": "dex-code-signing-release-process",
        "index": 286,
        "group": "Group AC",
        "domain": "Software Trust & Distribution",
        "description": "Establish automated, tamper-proof code signing pipelines for Windows Authenticode, macOS Notarization, and Linux GPG packages using Hardware Security Modules (HSM) and cloud key management. Use when eliminating Windows SmartScreen warnings and passing macOS Gatekeeper.",
        "purpose": "Thiết lập quy trình ký mã nguồn (Code Signing Release Pipeline) tự động và chống giả mạo cho các gói phần mềm Windows (Microsoft Authenticode), macOS (Apple Notarization & Stapling) và Linux (GPG/RPM/DEB); tích hợp mô-đun bảo mật phần cứng (Hardware Security Module - HSM) hoặc dịch vụ quản lý khóa đám mây (Cloud KMS); triệt tiêu hoàn toàn cảnh báo bảo mật Windows Defender SmartScreen và vượt qua rào chắn kiểm duyệt macOS Gatekeeper.",
        "when_use": [
            "Trước khi xuất bản tệp cài đặt phần mềm máy tính (`.exe`, `.msi`, `.dmg`, `.pkg`) cho người dùng cuối.",
            "Khi ứng dụng cài đặt bị hệ điều hành Windows hiển thị cảnh báo đỏ 'Windows protected your PC' gây mất uy tín.",
            "Khi phát hành ứng dụng trên macOS yêu cầu chứng chỉ Apple Developer và tiến trình công chứng Notarization hợp lệ."
        ],
        "when_not_use": [
            "Khi chỉ triển khai mã nguồn lên máy chủ nội bộ hoặc container Docker (nên dùng Sigstore/Cosign).",
            "Khi xuất bản trang web thông thường."
        ],
        "prereqs": "Chứng chỉ số ký mã nguồn (EV Code Signing Certificate hoặc Apple Developer ID), công cụ `signtool.exe` trên Windows hoặc `codesign`/`notarytool` trên macOS.",
        "concepts": [
            "EV Code Signing & SmartScreen Reputation: Chứng chỉ số mở rộng (Extended Validation) giúp phần mềm có ngay uy tín tức thì trên Windows SmartScreen mà không cần tích lũy lượt tải.",
            "Apple Notarization & Stapling: Quá trình gửi ứng dụng lên máy chủ Apple để quét mã độc tự động, sau đó đính kèm vé công chứng (Staple) vào tệp `.dmg` để ứng dụng mở được khi ngoại tuyến.",
            "RFC 3161 Trusted Timestamping: Ký kèm dấu thời gian tin cậy để chữ ký của phần mềm vẫn có hiệu lực vĩnh viễn ngay cả khi chứng chỉ ký mã nguồn hết hạn trong tương lai."
        ],
        "steps": [
            "Xây dựng bản dựng phần mềm nhị phân sạch trong môi trường CI khép kín.",
            "Gọi lệnh ký số kết nối với HSM hoặc Azure Trusted Signing / AWS KMS.",
            "Đóng dấu thời gian tin cậy RFC 3161 từ máy chủ timestamp có uy tín (DigiCert hoặc Sectigo).",
            "Đối với macOS, gửi gói lên dịch vụ Apple Notary Service và đính kèm vé công chứng bằng `xcrun staple`.",
            "Kiểm tra tính toàn vẹn của chữ ký số bằng lệnh `signtool verify` hoặc `spctl -a`."
        ],
        "code_lang": "bash",
        "code_example": """# Windows Authenticode Signing with RFC 3161 Timestamp
signtool.exe sign /tr http://timestamp.digicert.com /td sha256 /fd sha256 /a "bin/DEX_Installer.exe"
signtool.exe verify /pa /v "bin/DEX_Installer.exe"

# macOS Hardened Runtime Signing & Notarization
codesign --deep --force --options runtime --sign "Developer ID Application: DEX Engineering (TEAM123)" "dist/DEX.app"
xcrun notarytool submit "dist/DEX.dmg" --keychain-profile "AC_PASSWORD" --wait
xcrun stapler staple "dist/DEX.dmg"
spctl --assess --type execute --verbose "dist/DEX.dmg" """,
        "antipatterns": [
            "Ký mã nguồn mà quên gắn dấu thời gian RFC 3161 Timestamp, khiến phần mềm bị Windows báo lỗi chứng chỉ hết hạn ngay sau 1 năm phát hành.",
            "Lưu tệp chứng chỉ ký mã nguồn `.pfx` kèm mật khẩu thẳng vào kho mã nguồn Git của dự án (vi phạm bảo mật nghiêm trọng).",
            "Bỏ qua cờ Hardened Runtime trên macOS khiến ứng dụng bị từ chối công chứng bởi Apple."
        ],
        "quality_gates": [
            "QG-01: 100% các tệp `.exe`, `.dll`, `.dmg` phát hành đều có chữ ký số hợp lệ kèm RFC 3161 Timestamp.",
            "QG-02: Vượt qua kiểm tra macOS Gatekeeper (`spctl --assess`) với thông báo `accepted`.",
            "QG-03: Khóa riêng tư ký mã nguồn được lưu trữ độc quyền trong HSM/Cloud KMS, không bao giờ xuất ra tệp thô."
        ],
        "security": "Áp dụng quy trình phê duyệt kép trước khi kích hoạt lệnh ký mã nguồn phát hành chính thức để chống việc mã độc bị ký lén.",
        "deliverables": [
            "Kịch bản tự động hóa ký mã nguồn Windows/macOS trong CI `sign-release.sh`.",
            "Bản báo cáo thẩm định chứng chỉ số và công chứng phần mềm."
        ],
        "related": ["dex-artifact-signature-verification", "dex-software-update-trust-chains", "dex-release-reproducibility-audit"],
        "scenario": "Doanh nghiệp phát hành phần mềm quản lý kho cho các đại lý bán lẻ. Khách hàng phàn nàn không cài đặt được vì Windows 11 hiện màn hình cảnh báo xanh chặn đứng. Kỹ sư kích hoạt `dex-code-signing-release-process`, tích hợp Azure Trusted Signing với chứng chỉ EV và timestamp SHA-256 vào GitHub Actions, giúp tệp cài đặt mở lên tức thì không còn bất kỳ cảnh báo nào."
    },
    {
        "id": "dex-software-update-trust-chains",
        "index": 287,
        "group": "Group AC",
        "domain": "Software Trust & Distribution",
        "description": "Architect secure software auto-update trust frameworks incorporating The Update Framework (TUF) principles, cryptographic manifest verification, downgrade attack prevention, and differential binary patches. Use when engineering auto-updaters for desktop apps or IoT devices.",
        "purpose": "Thiết kế kiến trúc chuỗi tin cậy cập nhật phần mềm tự động (Software Update Trust Frameworks); ứng dụng các nguyên lý bảo mật của The Update Framework (TUF), thẩm định bản kê cập nhật có chữ ký điện tử (Signed Update Manifests), cơ chế chống tấn công hạ cấp phiên bản (Downgrade/Rollback Attack Prevention) và vá nhị phân vi sai (Differential Binary Patching); đảm bảo quá trình cập nhật phần mềm máy tính và thiết bị IoT diễn ra an toàn tuyệt đối.",
        "when_use": [
            "Khi xây dựng cơ chế tự động cập nhật phiên bản mới (Auto-Updater) cho ứng dụng máy tính (Electron, Tauri, C++).",
            "Khi phát hành các bản cập nhật qua mạng (OTA Updates) cho thiết bị phần cứng nhúng.",
            "Khi cần bảo vệ hệ thống cập nhật không bị kẻ tấn công đánh chặn máy chủ để phát tán phiên bản chứa mã độc."
        ],
        "when_not_use": [
            "Khi ứng dụng web được triển khai tập trung trên máy chủ (người dùng chỉ cần tải lại trang).",
            "Khi phát hành ứng dụng qua các kho chợ có sẵn cơ chế cập nhật như Apple App Store hay Google Play."
        ],
        "prereqs": "Đặc tả chuẩn The Update Framework (TUF), khóa ký bản kê cập nhật, công cụ tạo bản vá vi sai (bsdiff hoặc courgette).",
        "concepts": [
            "The Update Framework (TUF) Roles: Phân tách trách nhiệm thành 4 vai trò độc lập: Root (Quản lý khóa), Targets (Mô tả tệp tải), Snapshot (Trạng thái phiên bản) và Timestamp (Chống tấn công phát lại).",
            "Freeze Attack Prevention: Cơ chế kiểm tra thời hạn hiệu lực của bản kê cập nhật để kẻ tấn công không thể giữ người dùng ở phiên bản cũ chứa lỗ hổng.",
            "Monotonic Version Progression: Máy khách từ chối cài đặt bất kỳ bản cập nhật nào có số phiên bản thấp hơn hoặc bằng phiên bản hiện tại để chống hạ cấp."
        ],
        "steps": [
            "Tạo tệp bản kê cập nhật `update-manifest.json` chứa số phiên bản mới, mã băm SHA-256 và kích thước tệp tải.",
            "Ký điện tử lên tệp manifest bằng khóa riêng bí mật tách biệt khỏi máy chủ web phân phối.",
            "Ứng dụng máy khách tải tệp manifest, xác thực chữ ký số bằng khóa công khai đã nhúng sẵn trong mã nguồn.",
            "Kiểm tra số phiên bản mới phải lớn hơn phiên bản hiện tại.",
            "Tải gói cập nhật, xác minh mã băm byte đối chiếu với manifest trước khi thực hiện cài đặt ghi đè."
        ],
        "code_lang": "typescript",
        "code_example": """// Secure Update Manifest Verification Pattern
import crypto from 'crypto';

export interface UpdateManifest {
  version: string;
  minSupportedVersion: string;
  downloadUrl: string;
  sha256: string;
  publishedAt: string;
  signature: string;
}

export function verifyUpdateManifest(manifest: UpdateManifest, trustedPublicKey: string): boolean {
  const { signature, ...dataToVerify } = manifest;
  const verifier = crypto.createVerify('RSA-SHA256');
  verifier.update(JSON.stringify(dataToVerify));
  return verifier.verify(trustedPublicKey, signature, 'base64');
}""",
        "antipatterns": [
            "Tải tệp cập nhật `.exe` qua giao thức HTTP không mã hóa và thực thi thẳng mà không kiểm tra chữ ký số hoặc mã băm.",
            "Cho phép cài đặt phiên bản có số hiệu cũ hơn phiên bản đang chạy (mở đường cho tấn công hạ cấp để khai thác lỗ hổng cũ đã vá).",
            "Lưu khóa ký bản cập nhật trên cùng một máy chủ web chứa tệp tải (nếu web server bị hack, kẻ tấn công sẽ ký luôn mã độc)."
        ],
        "quality_gates": [
            "QG-01: 100% các bản cập nhật bắt buộc phải có manifest được ký số và mã băm SHA-256 trùng khớp từng byte.",
            "QG-02: Chặn đứng hoàn toàn mọi nỗ lực hạ cấp phiên bản (Downgrade rejection test đạt 100%).",
            "QG-03: Cơ chế cập nhật tự động rollback an toàn nếu quá trình cài đặt phiên bản mới gặp sự cố."
        ],
        "security": "Khóa gốc (Root Key) của hệ thống cập nhật phải được lưu trữ ngoại tuyến hoàn toàn (Offline Cold Storage) trong két sắt an toàn.",
        "deliverables": [
            "Module xác thực cập nhật an toàn `SecureUpdateManager.ts`.",
            "Đặc tả kiến trúc cập nhật phần mềm chuẩn TUF `UPDATE_TRUST_FRAMEWORK.md`."
        ],
        "related": ["dex-code-signing-release-process", "dex-artifact-signature-verification", "dex-vulnerability-disclosure-workflows"],
        "scenario": "Xây dựng hệ thống tự động cập nhật cho ứng dụng ví tiền mã hóa desktop. Kỹ sư kích hoạt `dex-software-update-trust-chains`, triển khai kiến trúc TUF với khóa ký offline và xác thực kép SHA-256, ngăn chặn hoàn toàn nguy cơ kẻ tấn công hack vào máy chủ DNS để chuyển hướng người dùng tải về bản cập nhật giả mạo đánh cắp tiền."
    },
    {
        "id": "dex-vulnerability-disclosure-workflows",
        "index": 288,
        "group": "Group AC",
        "domain": "Software Trust & Distribution",
        "description": "Establish standardized Coordinated Vulnerability Disclosure (CVD) workflows, drafting security.md policies, encrypted communication channels (PGP), CVE assignment coordination, and security advisory publications. Use when hardening open-source repositories and managing external security reports.",
        "purpose": "Thiết lập quy trình công bố lỗ hổng bảo mật phối hợp chuẩn quốc tế (Coordinated Vulnerability Disclosure - CVD); soạn thảo chính sách an ninh `SECURITY.md`, thiết lập kênh tiếp nhận thông tin mã hóa bảo mật (PGP Key), quy trình phối hợp cấp mã định danh CVE (CNA Coordination) và xuất bản các khuyến cáo an ninh (Security Advisories); đảm bảo việc tiếp nhận và xử lý báo cáo lỗ hổng từ các nhà nghiên cứu bảo mật diễn ra chuyên nghiệp, đúng luật và có trách nhiệm.",
        "when_use": [
            "Khi thiết lập kho mã nguồn mở hoặc sản phẩm phần mềm thương mại có tiếp nhận báo cáo bảo mật từ cộng đồng.",
            "Khi nhận được một báo cáo lỗ hổng zero-day từ một hacker mũ trắng bên ngoài và cần quy trình xử lý vá lỗi bí mật.",
            "Khi cần xuất bản một bản vá an ninh kèm thông báo khuyến cáo chính thức (Security Advisory) cho khách hàng."
        ],
        "when_not_use": [
            "Khi tiếp nhận các yêu cầu hỗ trợ kỹ thuật hoặc tính năng sản phẩm thông thường.",
            "Khi điều tra nội bộ các lỗi cú pháp mã nguồn không ảnh hưởng đến an ninh."
        ],
        "prereqs": "Tệp chính sách `SECURITY.md`, cặp khóa PGP công khai để nhận thư mã hóa, tài khoản ủy quyền đăng ký mã định danh CVE.",
        "concepts": [
            "Coordinated Vulnerability Disclosure (CVD): Thỏa thuận giữa nhà nghiên cứu và đội phát triển: nhà nghiên cứu giữ bí mật trong thời hạn thỏa thuận (thường 90 ngày) để đội phát triển kịp thời phát hành bản vá trước khi công bố ra công chúng.",
            "Embargo Period: Khoảng thời gian cấm tiết lộ thông tin ra bên ngoài trong khi bản vá đang được bí mật phát triển và thử nghiệm.",
            "GitHub Private Vulnerability Reporting: Tính năng cho phép nhà nghiên cứu gửi báo cáo trực tiếp trong kho Git mà không làm lộ thông tin ra tab Issues công khai."
        ],
        "steps": [
            "Soạn thảo tệp chính sách `SECURITY.md` ở thư mục gốc của repository.",
            "Công bố khóa PGP công khai và địa chỉ email bảo mật chuyên dụng (`security@domain.com`).",
            "Kích hoạt tính năng Private Vulnerability Reporting trên GitHub.",
            "Khi nhận được báo cáo, xác minh tính tái lập của lỗ hổng trong môi trường cô lập trong vòng 48 giờ.",
            "Phát triển bản vá trong kho riêng tư, đăng ký mã CVE và xuất bản bản vá cùng khuyến cáo an ninh đồng thời."
        ],
        "code_lang": "markdown",
        "code_example": """# Security Policy

## Supported Versions
| Version | Supported          |
| :---    | :---               |
| 6.x     | :white_check_mark: |
| 5.x     | :white_check_mark: |
| < 5.0   | :x:                |

## Reporting a Vulnerability
Xin vui lòng **KHÔNG** tạo issue công khai trên GitHub.

1. Báo cáo trực tiếp qua tính năng [Private Vulnerability Reporting](https://github.com/nguyenducanhst2022-png/dex-engineering-skills/security/advisories/new).
2. Hoặc gửi email mã hóa PGP về: `security@dex.dev`.
- PGP Fingerprint: `9B42 5A1C 882E 1F09 ...`

Chúng tôi cam kết phản hồi xác nhận trong vòng 48 giờ làm việc.""",
        "antipatterns": [
            "Yêu cầu người dùng báo lỗi bảo mật bằng cách mở Issue công khai trên GitHub, khiến kẻ xấu lập tức thấy lỗi và đi tấn công các hệ thống khác.",
            "Phớt lờ hoặc đe dọa kiện tụng các nhà nghiên cứu bảo mật thiện chí khi họ thông báo lỗi một cách có trách nhiệm.",
            "Âm thầm sửa lỗi bảo mật nghiêm trọng mà không phát hành Security Advisory cảnh báo khách hàng nâng cấp."
        ],
        "quality_gates": [
            "QG-01: Tệp `SECURITY.md` hoàn chỉnh hiện diện ở thư mục gốc của kho mã nguồn.",
            "QG-02: Khóa PGP công khai và kênh tiếp nhận bảo mật được kiểm tra hoạt động bình thường.",
            "QG-03: Thời gian phản hồi xác nhận ban đầu cho báo cáo bảo mật dưới 48 giờ."
        ],
        "security": "Giữ bí mật tuyệt đối toàn bộ chi tiết kỹ thuật của lỗ hổng trong thời gian cấm tiết lộ (Embargo) cho đến khi bản vá được phát hành chính thức.",
        "deliverables": [
            "Tệp chính sách an ninh chuẩn hóa `SECURITY.md`.",
            "Mẫu khuyến cáo an ninh bảo mật `SECURITY_ADVISORY_TEMPLATE.md`."
        ],
        "related": ["dex-vulnerability-remediation", "dex-dependency-vulnerability-intelligence", "dex-security-audit"],
        "scenario": "Một chuyên gia bảo mật phát hiện lỗ hổng nghiêm trọng cho phép vượt qua xác thực trong framework. Nhờ tệp `SECURITY.md` có hướng dẫn rõ ràng, chuyên gia gửi báo cáo mã hóa qua kênh riêng tư, đội ngũ kỹ thuật bí mật phát triển bản vá trong 5 ngày, đăng ký mã CVE-2026-XXXX và phát hành phiên bản mới an toàn cho toàn bộ người dùng mà không có sự cố rò rỉ nào."
    },
    {
        "id": "dex-maintainer-contribution-governance",
        "index": 289,
        "group": "Group AC",
        "domain": "Software Trust & Distribution",
        "description": "Establish open-source maintainer governance, automated CODEOWNERS enforcement, Contributor License Agreements (CLA/DCO), PR review checklists, and branch protection rules. Use when scaling open-source communities, protecting codebase integrity, or formalizing contributor workflows.",
        "purpose": "Thiết lập cấu trúc quản trị người duy trì dự án (Maintainer Contribution Governance) và cộng đồng mã nguồn mở; tự động hóa thực thi quyền sở hữu mã nguồn (`.github/CODEOWNERS`), thỏa thuận cấp phép người đóng góp (CLA / Developer Certificate of Origin - DCO), danh mục kiểm tra đánh giá Pull Request và các quy tắc bảo vệ nhánh (Branch Protection Rules); đảm bảo tính toàn vẹn của mã nguồn và tính bền vững của dự án.",
        "when_use": [
            "Khi một dự án phần mềm bắt đầu mở rộng cho nhiều kỹ sư hoặc cộng đồng bên ngoài cùng đóng góp mã nguồn.",
            "Khi cần đảm bảo mọi thay đổi trong các thư mục quan trọng (như bảo mật, thanh toán) bắt buộc phải có sự phê duyệt của kỹ sư trưởng.",
            "Khi bảo vệ tính pháp lý của mã nguồn bằng cách yêu cầu người đóng góp xác nhận cam kết bản quyền DCO (Signed-off-by)."
        ],
        "when_not_use": [
            "Khi dự án cá nhân một người làm không có người đóng góp thứ hai.",
            "Khi xây dựng kịch bản tự động hóa hạ tầng phần cứng."
        ],
        "prereqs": "Kho lưu trữ GitHub/GitLab, tệp quy tắc `CODEOWNERS`, cấu hình bot kiểm tra DCO/CLA trong pull request.",
        "concepts": [
            "Developer Certificate of Origin (DCO): Cam kết pháp lý đơn giản của người đóng góp (thông qua dòng `Signed-off-by: Name <email>` trong commit message) xác nhận họ tự viết mã nguồn này hoặc có quyền đóng góp.",
            "Granular CODEOWNERS Enforcement: Tự động chỉ định người đánh giá PR dựa trên đường dẫn tệp tin bị thay đổi (ví dụ thư mục `auth/` do nhóm Security duyệt).",
            "Strict Branch Protection: Cấm push trực tiếp vào nhánh `main`, bắt buộc vượt qua 100% CI checks và có tối thiểu 2 lượt phê duyệt (Approve) từ người có thẩm quyền."
        ],
        "steps": [
            "Thiết lập tệp `.github/CODEOWNERS` phân công rõ ràng các thư mục chuyên trách cho từng nhóm.",
            "Cài đặt GitHub Action kiểm tra cam kết DCO trên 100% các commit của pull request.",
            "Khai báo các quy tắc bảo vệ nhánh `main`: cấm force-push, yêu cầu nhánh phải cập nhật mới nhất trước khi merge.",
            "Xây dựng biểu mẫu Pull Request Template chuẩn hóa yêu cầu mô tả rõ mục đích, bằng chứng kiểm thử và tài liệu cập nhật.",
            "Biên soạn tài liệu hướng dẫn người đóng góp `CONTRIBUTING.md`."
        ],
        "code_lang": "text",
        "code_example": """# .github/CODEOWNERS
# Global default owners for everything
*       @nguyenducanhst2022-png

# Security and Auth modules require Lead Security Auditor
/.agents/skills/dex-security*   @nguyenducanhst2022-png/security-team
/integrations/                  @nguyenducanhst2022-png/integration-team

# Core Orchestrator requires Principal Architect approval
/.agents/skills/dex-master-orchestrator/   @nguyenducanhst2022-png/architecture-leads""",
        "antipatterns": [
            "Cho phép bất kỳ ai cũng có thể push thẳng vào nhánh `main` mà không cần qua PR hay kiểm thử tự động.",
            "Tiếp nhận các đóng góp mã nguồn lớn từ người ngoài mà không có xác nhận DCO/CLA, dẫn đến nguy cơ bị kiện bản quyền sau này.",
            "Để các pull request của cộng đồng bị bỏ quên hàng tháng không ai phản hồi, làm triệt tiêu nhiệt huyết của người đóng góp."
        ],
        "quality_gates": [
            "QG-01: Nhánh `main` được kích hoạt bảo vệ 100%: cấm push trực tiếp và cấm force-push.",
            "QG-02: 100% các commit từ bên ngoài đều có chữ ký cam kết DCO (`Signed-off-by`).",
            "QG-03: Tệp `CODEOWNERS` được cấu hình đầy đủ và tự động gán đúng người phụ trách khi mở PR."
        ],
        "security": "Ngăn chặn các cuộc tấn công chiếm quyền kho mã nguồn mở bằng cách yêu cầu tài khoản maintainer bắt buộc phải bật xác thực 2 yếu tố (2FA).",
        "deliverables": [
            "Tệp cấu hình sở hữu mã nguồn `.github/CODEOWNERS`.",
            "Tài liệu hướng dẫn đóng góp `CONTRIBUTING.md` và PR Template `.github/PULL_REQUEST_TEMPLATE.md`."
        ],
        "related": ["dex-git-workflow", "dex-code-review", "dex-vulnerability-disclosure-workflows"],
        "scenario": "Dự án nguồn mở nhận được nhiều sự quan tâm từ cộng đồng nhưng mã nguồn bắt đầu bị hỗn loạn do các PR merge tùy tiện. Kỹ sư kích hoạt `dex-maintainer-contribution-governance`, thiết lập tệp CODEOWNERS, bật kiểm tra DCO tự động và khóa nhánh `main`, đưa quy trình đóng góp vào khuôn khổ chuyên nghiệp và bảo vệ an toàn cho dự án."
    },
    {
        "id": "dex-release-reproducibility-audit",
        "index": 290,
        "group": "Group AC",
        "domain": "Software Trust & Distribution",
        "description": "Audit and enforce bit-for-bit reproducible builds using diffoscope, containerized build environments, SOURCE_DATE_EPOCH timestamps, and deterministic compiler flags. Use when validating SLSA Level 3/4 provenance and eliminating build-time covert tampering.",
        "purpose": "Kiểm toán và thực thi quy trình biên dịch tái lập từng bit (Bit-for-Bit Reproducible Builds); sử dụng công cụ `diffoscope`, môi trường container đóng kín (Hermetic Build Environments), chuẩn hóa dấu thời gian `SOURCE_DATE_EPOCH` và cờ trình biên dịch xác định; đảm bảo hai lần biên dịch độc lập từ cùng một commit mã nguồn luôn tạo ra các tệp nhị phân có mã băm SHA-256 hoàn toàn trùng khớp; đạt chuẩn an ninh chuỗi cung ứng SLSA Level 3/4.",
        "when_use": [
            "Khi xây dựng các phần mềm đòi hỏi độ tin cậy tuyệt đối (phần mềm ví tiền mã hóa, nhân hệ điều hành, công cụ an ninh mạng).",
            "Khi cần chứng minh với khách hàng và cơ quan kiểm toán rằng tệp nhị phân phân phối thực sự được sinh ra từ đúng mã nguồn mở công khai.",
            "Khi kiểm tra xem hạ tầng máy chủ build CI có bị cài cắm mã độc can thiệp ngầm vào quá trình biên dịch hay không."
        ],
        "when_not_use": [
            "Khi phát triển các ứng dụng nội bộ thử nghiệm thay đổi mã nguồn liên tục từng phút.",
            "Khi ngôn ngữ lập trình hoặc công cụ đóng gói không hỗ trợ cơ chế biên dịch tái lập."
        ],
        "prereqs": "Công cụ phân tích sai khác nhị phân `diffoscope`, môi trường Docker đóng kín không có mạng (Hermetic container), biến môi trường `SOURCE_DATE_EPOCH`.",
        "concepts": [
            "Non-Deterministic Build Artifacts: Các yếu tố làm lệch mã băm nhị phân: Dấu thời gian hiện tại được nhúng vào header, đường dẫn thư mục tạm `/tmp/build_123` bị ghi vào debug symbol, và thứ tự duyệt tệp tin ngẫu nhiên của hệ điều hành.",
            "SOURCE_DATE_EPOCH Specification: Tiêu chuẩn quốc tế thay thế thời gian hiện tại bằng dấu thời gian của commit Git gần nhất (Unix timestamp cố định).",
            "Hermetic Build Sandbox: Môi trường biên dịch bị cô lập hoàn toàn không có kết nối Internet và không bị ảnh hưởng bởi biến môi trường của máy chủ chủ quản."
        ],
        "steps": [
            "Thiết lập biến môi trường `export SOURCE_DATE_EPOCH=$(git log -1 --pretty=%ct)`.",
            "Cấu hình cờ trình biên dịch để ánh xạ lại đường dẫn thư mục thành đường dẫn ảo đồng nhất (`-fdebug-prefix-map`).",
            "Sắp xếp danh sách tệp tin đầu vào theo thứ tự bảng chữ cái trước khi đưa vào trình nén lưu trữ (tar/zip).",
            "Thực hiện hai lần biên dịch độc lập trên hai máy chủ khác nhau hoàn toàn.",
            "So sánh mã băm SHA-256 của hai bản dựng; nếu lệch, dùng `diffoscope` để bóc tách byte khác biệt và khắc phục."
        ],
        "code_lang": "bash",
        "code_example": """# Setting deterministic build environment
export SOURCE_DATE_EPOCH=$(git log -1 --pretty=%ct)
export LC_ALL=C
export TZ=UTC

# Compiling with deterministic path mapping in GCC/Clang
gcc -O2 -g -fdebug-prefix-map=$(pwd)=/build_root -c main.c -o main.o

# Creating deterministic tarball without host metadata
tar --sort=name --mtime="@${SOURCE_DATE_EPOCH}" --owner=0 --group=0 --numeric-owner \\
    -czf release-reproducible.tar.gz bin/

# Verifying bit-for-bit reproducibility
diffoscope build_run_1/release.tar.gz build_run_2/release.tar.gz""",
        "antipatterns": [
            "Nhúng macro thời gian `__DATE__` hoặc `__TIME__` trong mã nguồn C++ (khiến mỗi giây biên dịch tạo ra một bản nhị phân khác hẳn nhau).",
            "Nén tệp zip/tar mà không sắp xếp tên tệp, khiến thứ tự đọc tệp trên đĩa làm thay đổi mã băm của tệp nén.",
            "Để tệp nhị phân chứa đường dẫn thư mục máy trạm cá nhân của lập trình viên (ví dụ `C:\\Users\\John\\...`)."
        ],
        "quality_gates": [
            "QG-01: Hai lần biên dịch độc lập trên hai môi trường khác nhau cho ra mã băm SHA-256 hoàn toàn trùng khớp 100%.",
            "QG-02: Công cụ `diffoscope` so sánh hai bản dựng trả về kết quả 0 sai khác (Clean Diff).",
            "QG-03: Mọi tệp nén và nhị phân đều tuân thủ chuẩn `SOURCE_DATE_EPOCH`."
        ],
        "security": "Triệt tiêu hoàn toàn nguy cơ máy chủ CI bị cài cắm mã độc ngầm (như vụ tấn công XcodeGhost) bằng cách cho phép bất kỳ ai cũng có thể tự biên dịch và đối soát mã băm nhị phân.",
        "deliverables": [
            "Đường ống biên dịch tái lập từng bit `reproducible_build.sh`.",
            "Báo cáo kiểm toán tái lập nhị phân `REPRODUCIBILITY_AUDIT.md`."
        ],
        "related": ["dex-binary-diff-regression", "dex-code-signing-release-process", "dex-slsa-provenance-verification"],
        "scenario": "Dự án phát triển thư viện mật mã học công khai mã nguồn. Kỹ sư kích hoạt `dex-release-reproducibility-audit`, loại bỏ macro thời gian biên dịch, ánh xạ lại đường dẫn debug prefix map và thiết lập `SOURCE_DATE_EPOCH`, giúp cộng đồng mạng có thể tự tải mã nguồn về biên dịch và đối soát ra đúng mã băm SHA-256 với tệp phát hành chính thức."
    },

    # --- GROUP AD: Advanced SkillOps Governance ---
    {
        "id": "dex-skill-catalog-taxonomy",
        "index": 291,
        "group": "Group AD",
        "domain": "Advanced SkillOps Governance",
        "description": "Govern multi-tier Agent Skill catalog taxonomies, classifying skills across domain groups (A-AD), capability primitives, operational risk levels, and progressive disclosure scopes. Use when scaling skill libraries past 300+ skills without routing confusion or context bloat.",
        "purpose": "Quản trị hệ thống phân loại danh mục kỹ năng AI Agent đa tầng (Multi-Tier Agent Skill Catalog Taxonomy); phân bổ chuẩn mực 300 kỹ năng trên 30 nhóm nghiệp vụ (Groups A đến AD), phân loại theo nguyên mẫu năng lực (Capability Primitives), mức độ rủi ro vận hành và phạm vi công bố tiệm tiến (Progressive Disclosure); ngăn ngừa hiện tượng quá tải ngữ cảnh và xung đột định tuyến khi kho kỹ năng mở rộng quy mô lớn.",
        "when_use": [
            "Khi số lượng kỹ năng trong hệ thống vượt quá 200-300 skills và cần cấu trúc phân tầng khoa học.",
            "Khi bộ định tuyến Orchestrator bị nhầm lẫn giữa các kỹ năng có tên gọi hoặc phạm vi gần giống nhau.",
            "Khi cần sinh tự động tài liệu chỉ mục kỹ năng `SKILLS_INDEX.md` và bản đồ định tuyến `ROUTING_MATRIX.md`."
        ],
        "when_not_use": [
            "Khi kho kỹ năng chỉ có một vài kỹ năng cơ bản dưới 10 skills.",
            "Khi quản lý danh mục sản phẩm hàng hóa kinh doanh."
        ],
        "prereqs": "Tập hợp các tệp `SKILL.md` trong `.agents/skills/`, tệp siêu dữ liệu phân loại `manifests/dex-skills.json`, quy tắc đặt tên chuẩn.",
        "concepts": [
            "Progressive Disclosure: Không bao giờ nhồi nhét toàn bộ 300 kỹ năng vào lời nhắc của Agent cùng lúc; phân loại thành 30 nhóm tổng quát và chỉ nạp chi tiết các kỹ năng thuộc nhóm nghiệp vụ được kích hoạt.",
            "Orthogonal Domain Separation: Đảm bảo ranh giới giữa các nhóm A-AD là trực giao (không chồng chéo trách nhiệm lên nhau).",
            "Hierarchical Skill Addressing: Mỗi kỹ năng được định danh theo cấp bậc: Group -> Domain -> Specialized Skill ID."
        ],
        "steps": [
            "Phân tích toàn bộ kho kỹ năng và đối chiếu với bảng ánh xạ 30 nhóm nghiệp vụ (Groups A đến AD).",
            "Gán nhãn phân loại chính xác cho từng kỹ năng vào cơ sở dữ liệu `manifests/dex-skills.json`.",
            "Kiểm tra tính cân bằng số lượng (đảm bảo mỗi nhóm có đúng 10 kỹ năng chuyên môn).",
            "Tự động sinh tài liệu mục lục phân loại có cấu trúc `SKILLS_INDEX.md`.",
            "Xác nhận bộ định tuyến Master Orchestrator có thể tra cứu kỹ năng theo cấu trúc phân tầng mới."
        ],
        "code_lang": "json",
        "code_example": """{
  "$schema": "https://dex.dev/schemas/skill-taxonomy.json",
  "taxonomyVersion": "6.0.0",
  "totalGroups": 30,
  "skillsPerGroup": 10,
  "groups": {
    "Group U": {
      "domain": "Visual Design Intelligence",
      "range": [201, 210],
      "riskProfile": "LOW_READ_WRITE"
    },
    "Group X": {
      "domain": "Authorized Reverse Engineering",
      "range": [231, 240],
      "riskProfile": "HIGH_READ_ONLY_AUDIT"
    }
  }
}""",
        "antipatterns": [
            "Để danh mục kỹ năng phát triển tự phát không có quy hoạch nhóm, dẫn đến trùng lặp chức năng giữa nhiều kỹ năng.",
            "Nhồi nhét nguyên văn nội dung của 300 file SKILL.md vào context window làm cạn kiệt bộ nhớ và gây ảo giác cho mô hình.",
            "Đặt tên kỹ năng mập mờ, chung chung như `dex-helper` hoặc `dex-tools` không thể hiện rõ năng lực chuyên ngành."
        ],
        "quality_gates": [
            "QG-01: Toàn bộ 300 kỹ năng chuyên ngành được phân bổ chính xác tuyệt đối vào 30 nhóm (mỗi nhóm đúng 10 skills).",
            "QG-02: Không có bất kỳ kỹ năng nào bị mồ côi hoặc không thể tra cứu qua bảng phân loại taxonomy.",
            "QG-03: Tệp kê khai `manifests/dex-skills.json` vượt qua 100% tiêu chuẩn JSON Schema."
        ],
        "security": "Phân loại rõ các kỹ năng có quyền can thiệp hệ thống cao để áp dụng chính sách kiểm duyệt phù hợp trong bộ định tuyến.",
        "deliverables": [
            "Bản kê phân loại danh mục máy đọc được `manifests/dex-skills.json`.",
            "Tài liệu mục lục phân loại toàn diện `SKILLS_INDEX.md`."
        ],
        "related": ["dex-skill-discovery-indexer", "dex-skill-reference-graph", "dex-master-orchestrator"],
        "scenario": "Hệ thống nâng cấp từ 200 kỹ năng lên 300 kỹ năng. Kỹ sư kích hoạt `dex-skill-catalog-taxonomy`, quy hoạch 10 nhóm nghiệp vụ mới từ Group U đến Group AD, đảm bảo mỗi nhóm có đúng 10 kỹ năng chuyên ngành với ranh giới rõ ràng, giúp Master Orchestrator định tuyến chính xác 100% không bị nhầm lẫn."
    },
    {
        "id": "dex-skill-source-integrity",
        "index": 292,
        "group": "Group AD",
        "domain": "Advanced SkillOps Governance",
        "description": "Verify cryptographic source integrity, Git commit tree hashes, upstream tracking, and license attributions for imported and native skills. Use when guarding skill repositories against unauthorized modifications or supply chain tampering.",
        "purpose": "Xác minh tính toàn vẹn nguồn gốc mật mã (Cryptographic Source Integrity) của các kỹ năng Agent; theo dõi mã băm cây cam kết Git (Git Tree Hashes), truy vết kho nguồn gốc thượng nguồn (Upstream Tracking) và chứng nhận giấy phép cho cả kỹ năng nội bộ và kỹ năng nhập từ bên ngoài; bảo vệ kho kỹ năng khỏi các sửa đổi trái phép hoặc chèn mã độc trong chuỗi cung ứng.",
        "when_use": [
            "Khi nhập một kỹ năng mới từ kho mã nguồn mở bên ngoài vào hệ thống DEX Skills.",
            "Trước mỗi đợt phát hành phiên bản framework lớn để kiểm tra tính toàn vẹn của toàn bộ kho kỹ năng.",
            "Khi kiểm toán nguồn gốc xuất xứ của từng dòng mã trong bộ kỹ năng doanh nghiệp."
        ],
        "when_not_use": [
            "Khi đang chỉnh sửa nháp nội dung kỹ năng trên máy trạm cá nhân.",
            "Khi kiểm tra hiệu năng định tuyến của Agent."
        ],
        "prereqs": "Kho Git của dự án, tệp kê khai nguồn thượng nguồn `manifests/upstream-sources.json`, công cụ tính mã băm Git tree (`git rev-parse`, `git hash-object`).",
        "concepts": [
            "Git Tree Hash Integrity: Mã băm SHA-1/SHA-256 của toàn bộ cây thư mục kỹ năng chứng minh rằng không có bất kỳ tệp tin nào bên trong bị thêm, bớt hoặc chỉnh sửa dù chỉ 1 ký tự.",
            "Segregated Upstream Quarantine: Các kỹ năng nhập từ nguồn bên ngoài bắt buộc phải nằm trong thư mục cách ly `integrations/` và không bao giờ được tính lẫn vào danh mục native.",
            "Upstream Commit Pinning: Khóa cứng mã commit hash chính xác của kho thượng nguồn để ngăn chặn việc tự động kéo về các phiên bản mới chưa qua kiểm duyệt an ninh."
        ],
        "steps": [
            "Đọc danh mục các nguồn tích hợp từ `manifests/upstream-sources.json`.",
            "Tính toán mã băm Git tree hash cho từng thư mục kỹ năng trong `.agents/skills/` và `integrations/`.",
            "Đối chiếu mã băm tính được với sổ cái toàn vẹn đã lưu trữ.",
            "Kiểm tra thông tin giấy phép bản quyền và liên kết nguồn gốc thượng nguồn.",
            "Nếu phát hiện mã băm không khớp hoặc kỹ năng bị sửa đổi không qua PR, phát cảnh báo vi phạm tính toàn vẹn."
        ],
        "code_lang": "python",
        "code_example": """# Verifying Skill Directory Git Tree Integrity
import subprocess
import json

def verify_skill_integrity(skill_dir_path: str, expected_tree_hash: str) -> bool:
    # Compute git tree hash for the directory
    res = subprocess.run(
        ["git", "rev-parse", f"HEAD:{skill_dir_path}"],
        capture_output=True, text=True, check=True
    )
    current_tree_hash = res.stdout.strip()
    return current_tree_hash == expected_tree_hash""",
        "antipatterns": [
            "Nhập kỹ năng từ GitHub bên ngoài bằng cách copy paste thủ công mà không lưu lại commit hash gốc và thông tin giấy phép.",
            "Trộn lẫn kỹ năng của bên thứ ba vào thư mục kỹ năng native của hệ thống.",
            "Tự động đồng bộ mã nguồn kỹ năng từ nhánh `main` của bên ngoài mà không qua khâu thẩm định an ninh tĩnh."
        ],
        "quality_gates": [
            "QG-01: 100% các kỹ năng tích hợp bên ngoài đều có mã commit hash và giấy phép được ghi nhận trong `manifests/upstream-sources.json`.",
            "QG-02: Toàn bộ kỹ năng bên thứ ba được cách ly tuyệt đối trong thư mục `integrations/`.",
            "QG-03: Mã băm cây Git tree hash của toàn bộ kỹ năng trùng khớp 100% với sổ cái kiểm định."
        ],
        "security": "Ngăn chặn các cuộc tấn công đầu độc kỹ năng AI (Skill Poisoning Attack) thông qua việc kiểm soát chặt chẽ tính toàn vẹn nguồn gốc.",
        "deliverables": [
            "Sổ cái toàn vẹn nguồn kỹ năng `manifests/upstream-sources.json`.",
            "Kịch bản kiểm tra tính toàn vẹn tự động `verify_skill_integrity.py`."
        ],
        "related": ["dex-skill-license-provenance", "dex-skill-security-screening", "dex-skill-provenance-ledger"],
        "scenario": "Kiểm toán an ninh chuỗi cung ứng kỹ năng. Kỹ sư kích hoạt `dex-skill-source-integrity`, quét toàn bộ kho kỹ năng, xác minh 5 kỹ năng bên thứ ba nằm đúng trong `integrations/` có đầy đủ commit hash đối chiếu với 4 repo thượng nguồn, khẳng định hệ thống không bị can thiệp trái phép."
    },
    {
        "id": "dex-skill-risk-scoring",
        "index": 293,
        "group": "Group AD",
        "domain": "Advanced SkillOps Governance",
        "description": "Quantify operational, security, and privilege risk scores for Agent Skills based on tool access, filesystem mutation scope, network egress, and execution authority. Use when enforcing principle of least privilege and gating autonomous agent execution.",
        "purpose": "Định lượng và đánh giá điểm số rủi ro vận hành, an ninh và đặc quyền của các kỹ năng Agent (Agent Skill Risk Scoring); dựa trên danh mục công cụ được phép gọi, phạm vi ghi/xóa hệ thống tệp, quyền truy cập mạng ra ngoài (Egress) và thẩm quyền thực thi lệnh; phục vụ việc thực thi nguyên tắc đặc quyền tối thiểu và thiết lập rào chắn kiểm soát Agent tự trị.",
        "when_use": [
            "Trước khi cấp phép cho một kỹ năng mới được đưa vào danh mục kích hoạt tự động của Agent.",
            "Khi phân loại các kỹ năng cần có sự phê duyệt của con người (HITL) và các kỹ năng được tự do chạy.",
            "Khi xây dựng hồ sơ rủi ro an ninh cho toàn bộ hệ sinh thái kỹ năng của tổ chức."
        ],
        "when_not_use": [
            "Khi đánh giá rủi ro tài chính của một khoản đầu tư.",
            "Khi kiểm thử hiệu năng tốc độ xử lý của kỹ năng."
        ],
        "prereqs": "Tệp `SKILL.md` và mã nguồn công cụ đi kèm, bảng trọng số rủi ro tiêu chuẩn (Risk Weight Matrix).",
        "concepts": [
            "Multi-Factor Risk Scoring: Tính toán điểm số từ 0.0 (An toàn tuyệt đối) đến 10.0 (Nguy cơ cực cao) dựa trên 4 yếu tố: Thao tác tệp (Filesystem), Mạng (Network), Lệnh shell (Execution) và Tính phá hủy (Destructiveness).",
            "Read-Only vs Mutating Capability: Các kỹ năng chỉ đọc (như kiểm tra header nhị phân) có điểm rủi ro thấp hơn nhiều so với kỹ năng sửa đổi mã nguồn hoặc xóa cơ sở dữ liệu.",
            "Risk Tier Classification: Tier 1 (Safe: 0-3), Tier 2 (Moderate: 4-6), Tier 3 (High Risk: 7-8), Tier 4 (Critical: 9-10 - Bắt buộc duyệt kép)."
        ],
        "steps": [
            "Phân tích cú pháp tệp `SKILL.md` để trích xuất danh sách công cụ và quyền hạn được đề cập trong Mục 4 và Mục 10.",
            "Kiểm tra xem kỹ năng có yêu cầu quyền chạy lệnh terminal (`run_command`), sửa tệp (`edit_file`) hay kết nối mạng bên ngoài hay không.",
            "Tính toán điểm rủi ro tổng hợp dựa trên công thức trọng số chuẩn hóa.",
            "Gán cấp bậc rủi ro (Risk Tier) tương ứng vào siêu dữ liệu của kỹ năng trong manifest.",
            "Lập báo cáo đánh giá rủi ro kho kỹ năng `SKILL_RISK_AUDIT_REPORT.md`."
        ],
        "code_lang": "python",
        "code_example": """# Skill Operational Risk Scoring Calculator
def calculate_skill_risk(tool_permissions: list[str], network_egress: bool, destructive_actions: bool) -> tuple[float, str]:
    score = 1.0 # Baseline safe score

    if "run_command" in tool_permissions:
        score += 3.5
    if "write_file" in tool_permissions or "edit_file" in tool_permissions:
        score += 2.0
    if network_egress:
        score += 2.0
    if destructive_actions:
        score += 2.5

    score = min(10.0, score)

    if score <= 3.0: tier = "TIER_1_SAFE"
    elif score <= 6.0: tier = "TIER_2_MODERATE"
    elif score <= 8.5: tier = "TIER_3_HIGH"
    else: tier = "TIER_4_CRITICAL"

    return score, tier""",
        "antipatterns": [
            "Đánh đồng tất cả các kỹ năng đều có mức độ an toàn như nhau và cho phép Agent tự do chạy mọi công cụ.",
            "Cấp quyền thực thi shell (`run_command`) cho một kỹ năng chỉ làm nhiệm vụ đọc và tóm tắt tài liệu văn bản.",
            "Bỏ qua việc đánh giá quyền truy cập mạng, khiến kỹ năng có nguy cơ gửi dữ liệu ra máy chủ lạ."
        ],
        "quality_gates": [
            "QG-01: 100% các kỹ năng trong catalog đều được gán điểm rủi ro và Risk Tier rõ ràng trong manifest.",
            "QG-02: Toàn bộ kỹ năng thuộc Tier 3 và Tier 4 đều có quy định kiểm duyệt con người (HITL) bắt buộc.",
            "QG-03: Không có kỹ năng chỉ đọc nào bị cấp thừa quyền ghi hoặc quyền chạy lệnh terminal."
        ],
        "security": "Ngăn chặn việc Agent bị lạm dụng quyền hạn để thực thi các hành động phá hoại thông qua việc kiểm soát rủi ro chặt chẽ.",
        "deliverables": [
            "Bảng điểm số rủi ro kho kỹ năng `manifests/skill-risk-scores.json`.",
            "Báo cáo kiểm toán hồ sơ rủi ro `SKILL_RISK_AUDIT_REPORT.md`."
        ],
        "related": ["dex-agent-permissions", "dex-llm-human-review-gates", "dex-skill-security-screening"],
        "scenario": "Thẩm định an toàn cho 100 kỹ năng mới. Kỹ sư kích hoạt `dex-skill-risk-scoring`, tự động chấm điểm cho toàn bộ 100 skills, nhận diện 12 kỹ năng thuộc Tier 3 (chứa lệnh can thiệp nhị phân hoặc sửa file) và tự động gắn cờ yêu cầu phê duyệt con người khi Agent kích hoạt, đảm bảo an toàn tuyệt đối."
    },
    {
        "id": "dex-skill-reference-graph",
        "index": 294,
        "group": "Group AD",
        "domain": "Advanced SkillOps Governance",
        "description": "Construct and validate the bidirectional cross-skill reference graph across all 300 skills, detecting broken relative links, orphaned skills, circular delegation deadlocks, and missing prerequisite relationships. Use when validating catalog integrity and documentation graph completeness.",
        "purpose": "Xây dựng, trực quan hóa và kiểm chứng đồ thị tham chiếu chéo hai chiều (Bidirectional Skill Reference Graph) giữa toàn bộ 300 kỹ năng; phát hiện các liên kết tương đối bị hỏng (Broken Markdown Links), các kỹ năng bị cô lập (Orphaned Skills), các bế tắc ủy quyền vòng tròn (Circular Delegation Deadlocks) và thiếu sót quan hệ kỹ năng bổ trợ; đảm bảo tính toàn vẹn và liên kết chặt chẽ của mạng lưới tri thức kỹ năng.",
        "when_use": [
            "Trước khi đóng gói phát hành phiên bản framework mới để kiểm tra tính toàn vẹn của tất cả các đường dẫn liên kết.",
            "Khi thêm mới hoặc đổi tên một kỹ năng và cần cập nhật lại toàn bộ các kỹ năng khác đang tham chiếu tới nó.",
            "Khi phân tích cấu trúc mạng lưới kỹ năng để tối ưu hóa khả năng gợi ý kỹ năng bổ trợ cho AI Agent."
        ],
        "when_not_use": [
            "Khi kiểm tra liên kết web ra các trang bên ngoài Internet.",
            "Khi chỉ sửa lỗi chính tả nhỏ trong một file tài liệu duy nhất."
        ],
        "prereqs": "Toàn bộ thư mục `.agents/skills/`, công cụ phân tích đồ thị (NetworkX hoặc script Python bóc tách Markdown AST).",
        "concepts": [
            "Bidirectional Link Consistency: Nếu kỹ năng A liệt kê kỹ năng B là kỹ năng liên quan trong Mục 13, thì kỹ năng B cũng nên nhận biết được mối quan hệ với kỹ năng A.",
            "Zero Dead Link Guarantee: Mọi đường dẫn Markdown `[link](.agents/skills/xxx/SKILL.md)` phải trỏ tới một tệp tin thực sự tồn tại trên đĩa.",
            "Graph Centrality Analysis: Đo lường độ trung tâm của từng kỹ năng để xác định những kỹ năng nền tảng cốt lõi được sử dụng nhiều nhất (Hub Skills)."
        ],
        "steps": [
            "Quét toàn bộ 300 tệp `SKILL.md` và bóc tách các liên kết trong Mục 13 (Related & Complementary Skills).",
            "Kiểm tra sự tồn tại vật lý trên đĩa của từng đường dẫn liên kết được trích xuất.",
            "Xây dựng ma trận kề (Adjacency Matrix) đại diện cho đồ thị mạng lưới kỹ năng.",
            "Chạy thuật toán phát hiện các nút bị cô lập (độ vào và độ ra bằng 0) hoặc các chu trình ủy quyền kín.",
            "Xuất ra tệp sơ đồ mạng lưới kỹ năng `skill_reference_network.json`."
        ],
        "code_lang": "python",
        "code_example": """# Skill Reference Graph Validator
import os
import re

def validate_skill_reference_graph(skills_root: str):
    skill_names = set(os.listdir(skills_root))
    broken_links = []
    graph = {}

    for name in skill_names:
        file_path = os.path.join(skills_root, name, "SKILL.md")
        if not os.path.isfile(file_path): continue
        
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract related skill references
        links = re.findall(r'\[`?([a-z0-9-]+)`?\]\(\.agents/skills/([a-z0-9-]+)/SKILL\.md\)', content)
        graph[name] = []
        for text, target in links:
            if target not in skill_names:
                broken_links.append(f"{name} -> broken reference: {target}")
            else:
                graph[name].append(target)

    return graph, broken_links""",
        "antipatterns": [
            "Đổi tên một kỹ năng nhưng không cập nhật lại các kỹ năng khác đang trỏ tới nó, dẫn đến hàng loạt lỗi 404 hỏng liên kết.",
            "Kỹ năng hoàn toàn bị cô lập, không có bất kỳ kỹ năng nào liên kết tới và cũng không liên kết tới ai (Orphaned Skill).",
            "Tạo liên kết tham chiếu tròn kín giữa 2 Agent khiến chúng liên tục ủy quyền công việc qua lại cho nhau mà không bao giờ thực hiện."
        ],
        "quality_gates": [
            "QG-01: 100% các liên kết tham chiếu kỹ năng trong Mục 13 đều trỏ tới tệp tin tồn tại thực tế (0 Broken Links).",
            "QG-02: Không có kỹ năng nào bị cô lập hoàn toàn khỏi đồ thị tri thức kỹ năng.",
            "QG-03: Đồ thị tham chiếu được xuất bản đầy đủ dưới dạng tệp dữ liệu máy đọc được."
        ],
        "security": "Ngăn chặn các liên kết độc hại trỏ ra các đường dẫn tương đối vượt ra ngoài thư mục dự án (`../../etc/passwd`).",
        "deliverables": [
            "Đồ thị mạng lưới tham chiếu kỹ năng `skill_reference_network.json`.",
            "Báo cáo kiểm toán tính toàn vẹn liên kết kỹ năng `LINK_INTEGRITY_REPORT.md`."
        ],
        "related": ["dex-skill-catalog-taxonomy", "dex-skill-dependency-graph", "dex-skill-discovery-indexer"],
        "scenario": "Kiểm tra tính toàn vẹn của 301 kỹ năng trước ngày phát hành v6.0. Kỹ sư kích hoạt `dex-skill-reference-graph`, quét hơn 1,200 liên kết chéo trong toàn bộ kho, phát hiện 4 đường dẫn cũ bị gõ sai chính tả tên thư mục, tự động sửa chữa và đưa tỷ lệ liên kết hợp lệ đạt chuẩn 100%."
    },
    {
        "id": "dex-skill-routing-conflict-tests",
        "index": 295,
        "group": "Group AD",
        "domain": "Advanced SkillOps Governance",
        "description": "Design automated semantic disambiguation and routing conflict test suites, probing borderline intent prompts across overlapping skill domains to guarantee deterministic triage. Use when evaluating master orchestrator accuracy and eliminating skill routing collisions.",
        "purpose": "Thiết kế và xây dựng bộ kiểm thử xung đột định tuyến và khử nhập nhằng ngữ nghĩa (Semantic Disambiguation & Routing Conflict Testing); thử nghiệm các câu nhắc lệnh nằm ở ranh giới giao thoa giữa các kỹ năng có phạm vi tương tự nhau; đo lường độ chính xác phân loại của Master Orchestrator và đảm bảo tính xác định tuyệt đối trong việc điều phối kỹ năng.",
        "when_use": [
            "Khi kho kỹ năng có nhiều kỹ năng cùng giải quyết các khía cạnh khác nhau của một bài toán (ví dụ: `dex-frontend-performance` vs `dex-web-animation-performance`).",
            "Khi Master Orchestrator thỉnh thoảng điều phối nhầm kỹ năng cho các yêu cầu có bối cảnh đa nghĩa.",
            "Trước khi bổ sung một kỹ năng mới để đảm bảo không xâm lấn vào phạm vi kích hoạt của các kỹ năng sẵn có."
        ],
        "when_not_use": [
            "Khi các câu hỏi có ý định rõ ràng và không hề có sự giao thoa ngữ nghĩa.",
            "Khi kiểm thử hiệu năng tốc độ phản hồi của API."
        ],
        "prereqs": "Bộ định tuyến kỹ năng (Orchestrator Routing Engine), bộ câu hỏi kiểm thử ranh giới ngữ nghĩa (Borderline Prompts), ma trận nhầm lẫn (Confusion Matrix).",
        "concepts": [
            "Semantic Boundary Overlap: Hiện tượng hai kỹ năng cùng chứa các từ khóa kích hoạt tương tự nhau (ví dụ: 'CSS', 'Performance', 'Animation').",
            "Disambiguation Rules: Các quy tắc phân định rõ ràng trong Mục 2 (When to Use) và Mục 3 (When NOT to Use) để bộ định tuyến biết cách lựa chọn chính xác.",
            "Confusion Matrix Evaluation: Đo lường tỷ lệ phân loại đúng (Precision/Recall) và nhận diện các cặp kỹ năng thường xuyên bị nhầm lẫn lẫn nhau."
        ],
        "steps": [
            "Xây dựng tập hợp 50 câu hỏi biên có chủ đích gây nhầm lẫn giữa các cặp kỹ năng lân cận.",
            "Chạy quy trình định tuyến tự động qua Master Orchestrator.",
            "Ghi nhận kỹ năng được chọn và đối chiếu với nhãn chuẩn kỳ vọng.",
            "Vẽ ma trận nhầm lẫn (Confusion Matrix) để xác định các cặp kỹ năng có xung đột định tuyến.",
            "Tinh chỉnh lại mô tả trong tệp `SKILL.md` của các kỹ năng liên quan và kiểm tra lại đạt F1-Score >= 0.85."
        ],
        "code_lang": "python",
        "code_example": """# Routing Conflict Disambiguation Test Runner
def test_routing_conflict(orchestrator, test_cases: list[dict]):
    results = {"passed": 0, "failed": 0, "conflicts": []}

    for case in test_cases:
        selected_skill = orchestrator.route_intent(case["prompt"])
        if selected_skill == case["expected_skill"]:
            results["passed"] += 1
        else:
            results["failed"] += 1
            results["conflicts"].append({
                "prompt": case["prompt"],
                "expected": case["expected_skill"],
                "actual": selected_skill
            })

    f1_score = results["passed"] / len(test_cases)
    print(f"Routing Accuracy: {f1_score*100:.2f}% | Conflicts: {results['failed']}")
    assert f1_score >= 0.85, "Routing disambiguation failed target threshold!" """,
        "antipatterns": [
            "Viết phần mô tả kỹ năng (Description) quá chung chung chứa hàng loạt từ khóa của các kỹ năng khác, khiến kỹ năng này liên tục bị chọn nhầm.",
            "Bỏ qua phần 'When NOT to Use' khiến Orchestrator không có căn cứ loại trừ khi gặp tình huống đa nghĩa.",
            "Chỉ kiểm tra định tuyến với các câu hỏi dễ hiển nhiên mà không bao giờ kiểm thử các câu hỏi ở vùng ranh giới."
        ],
        "quality_gates": [
            "QG-01: Điểm số định tuyến tổng hợp F1-Score đạt tối thiểu 0.85 trên toàn bộ bộ kiểm thử ranh giới.",
            "QG-02: 100% các cặp kỹ năng có phạm vi tương tự đều có các quy tắc loại trừ lẫn nhau rõ ràng.",
            "QG-03: Không có kỹ năng nào bị chiếm đoạt 100% lưu lượng kích hoạt bởi một kỹ năng khác."
        ],
        "security": "Đảm bảo các kỹ năng có mức độ rủi ro cao không bao giờ bị kích hoạt nhầm khi người dùng chỉ yêu cầu một tác vụ thông thường.",
        "deliverables": [
            "Bộ kịch bản kiểm thử xung đột định tuyến `test_routing_conflicts.py`.",
            "Ma trận nhầm lẫn và báo cáo tối ưu hóa định tuyến `ROUTING_CONFLICT_REPORT.md`."
        ],
        "related": ["dex-skill-semantic-deduplication", "dex-master-orchestrator", "dex-skill-catalog-taxonomy"],
        "scenario": "Người dùng đưa ra yêu cầu: 'Giao diện bảng điều khiển bị giật khi cuộn chuột qua biểu đồ'. Hai kỹ năng `dex-web-animation-performance` và `dex-dashboard-data-storytelling` cùng tranh nhau kích hoạt. Kỹ sư kích hoạt `dex-skill-routing-conflict-tests`, phân tích từ khóa trọng tâm là 'giật khi cuộn' (hiệu năng), tinh chỉnh lại phần loại trừ và định tuyến chính xác về `dex-web-animation-performance`."
    },
    {
        "id": "dex-skill-execution-evidence-ledger",
        "index": 296,
        "group": "Group AD",
        "domain": "Advanced SkillOps Governance",
        "description": "Establish tamper-evident JSONL execution evidence ledgers recording real terminal commands, exit codes, stdout/stderr captures, and cryptographic checksums for skill quality validation. Use when producing verifiable proof of work and enforcing zero-hallucination compliance.",
        "purpose": "Thiết lập sổ cái bằng chứng thực thi chống giả mạo (Tamper-Evident Execution Evidence Ledger) định dạng JSONL; ghi nhận trung thực các câu lệnh terminal thực tế, mã thoát (Exit Codes), dữ liệu đầu ra stdout/stderr và mã băm mật mã chứng minh chất lượng hoàn thành của kỹ năng; phục vụ việc cung cấp bằng chứng nghiệm thu có thể kiểm chứng độc lập và triệt tiêu hoàn toàn thói quen tuyên bố hoàn thành dựa trên ảo giác.",
        "when_use": [
            "Sau mỗi lần AI Agent hoàn thành một tác vụ kỹ thuật và cần cung cấp bằng chứng nghiệm thu cho người dùng.",
            "Khi kiểm toán chất lượng của các kỹ năng trong kho để đảm bảo kỹ năng đã được chạy thật chứ không phải chỉ là văn bản lý thuyết.",
            "Khi lưu trữ hồ sơ bằng chứng phục vụ kiểm định chất lượng phần mềm ISO/IEC 25010."
        ],
        "when_not_use": [
            "Khi Agent chỉ trả lời các câu hỏi tư vấn mang tính lý thuyết không có thao tác kỹ thuật thực tế.",
            "Khi ghi nhật ký log gỡ lỗi tạm thời trên màn hình console."
        ],
        "prereqs": "Thư mục lưu trữ bằng chứng `.system_generated/logs/` hoặc thư mục artifacts, tiện ích tính mã băm SHA-256.",
        "concepts": [
            "Zero Fake Completion Guarantee: Cấm tuyệt đối việc Agent tuyên bố 'Đã kiểm thử thành công' mà không đưa ra được câu lệnh terminal thực tế kèm exit code 0.",
            "Tamper-Evident Hash Chaining: Mỗi bản ghi bằng chứng trong sổ cái JSONL chứa mã băm của bản ghi liền trước (tương tự Blockchain), đảm bảo nhật ký không thể bị chỉnh sửa hay xóa bớt.",
            "Verifiable Terminal Output: Lưu trữ nguyên văn chuỗi byte đầu ra của terminal để người dùng có thể đối chiếu và chạy lại xác minh bất cứ lúc nào."
        ],
        "steps": [
            "Mỗi khi Agent chạy một lệnh qua terminal, trích xuất mã thoát `exitCode`, dữ liệu `stdout` và `stderr`.",
            "Tính toán mã băm SHA-256 của chuỗi kết quả thực thi.",
            "Đóng gói bản ghi bằng chứng kèm dấu thời gian UTC và mã định danh nhiệm vụ.",
            "Ghi nối tiếp (Append-only) bản ghi vào tệp sổ cái `execution_evidence.jsonl`.",
            "Trích dẫn trực tiếp mã bằng chứng (Evidence ID) vào phần báo cáo hoàn thành gửi cho người dùng."
        ],
        "code_lang": "json",
        "code_example": """{
  "evidenceId": "EV-20261022-9901",
  "skillId": "dex-acceptance-testing",
  "command": "pytest tests/test_skill_structure.py -v",
  "exitCode": 0,
  "stdoutSnippet": "collected 301 items\\ntests/test_skill_structure.py::test_skill_count PASSED [100%]",
  "stderrSnippet": "",
  "executionDurationMs": 840,
  "timestampUtc": "2026-10-22T15:30:00.412Z",
  "sha256Hash": "4a5e1e8...b3"
}""",
        "antipatterns": [
            "Tuyên bố 'Đã kiểm thử toàn bộ 300 kỹ năng đều vượt qua 100%' nhưng khi kiểm tra lại thì không hề có lệnh nào được chạy trong terminal.",
            "Cố tình che giấu các thông báo lỗi `stderr` hoặc sửa mã thoát từ 1 thành 0 trong báo cáo.",
            "Xóa tệp nhật ký thực thi cũ để che giấu các lần chạy thử nghiệm bị thất bại."
        ],
        "quality_gates": [
            "QG-01: 100% các tuyên bố hoàn thành tác vụ kỹ thuật đều đi kèm bản ghi bằng chứng thực thi trong sổ cái.",
            "QG-02: Toàn bộ các lệnh kiểm chứng nghiệm thu đều có mã thoát exit code bằng 0.",
            "QG-03: Sổ cái bằng chứng JSONL tuân thủ cấu trúc schema và duy trì chuỗi mã băm liên tục."
        ],
        "security": "Không ghi các thông tin nhạy cảm (như mật khẩu truyền qua tham số dòng lệnh) vào sổ cái bằng chứng công khai.",
        "deliverables": [
            "Sổ cái bằng chứng thực thi chống giả mạo `execution_evidence.jsonl`.",
            "Bản báo cáo bằng chứng nghiệm thu có thể kiểm chứng `VERIFIABLE_PROOF_OF_WORK.md`."
        ],
        "related": ["dex-code-verification", "dex-reverse-evidence-chain", "dex-acceptance-testing"],
        "scenario": "Trong quá trình nâng cấp framework, AI Agent báo cáo đã hoàn thành việc kiểm thử toàn bộ các kỹ năng. Người dùng yêu cầu bằng chứng minh bạch. Agent kích hoạt `dex-skill-execution-evidence-ledger`, trích xuất bản ghi JSONL ghi nhận lệnh chạy `pytest tests/` kèm exit code 0 và thời gian chạy 0.88s, cung cấp bằng chứng thuyết phục 100% không thể nghi ngờ."
    },
    {
        "id": "dex-skill-documentation-drift",
        "index": 297,
        "group": "Group AD",
        "domain": "Advanced SkillOps Governance",
        "description": "Detect, quantify, and reconcile documentation drift between executable CLI scripts, manifest registries, and markdown specification files across the skill framework. Use when preventing out-of-sync documentation, stale examples, or unversioned skill modifications.",
        "purpose": "Phát hiện, định lượng và đồng nhất hóa hiện tượng trôi lệch tài liệu (Documentation Drift); rà soát sự bất đồng bộ giữa các kịch bản thực thi CLI, sổ cái bản kê manifest và các tệp đặc tả Markdown `SKILL.md` trong toàn bộ hệ thống; loại bỏ các ví dụ code lỗi thời, các tham số dòng lệnh không còn hỗ trợ và các thay đổi kỹ năng chưa được ghi chép.",
        "when_use": [
            "Sau khi sửa đổi mã nguồn của một script công cụ trong `scripts/` và cần kiểm tra xem các tài liệu `SKILL.md` liên quan đã được cập nhật tương ứng hay chưa.",
            "Khi kiểm tra xem các số liệu thống kê trong `README.md` có khớp chính xác với số lượng kỹ năng thực tế trên đĩa hay không.",
            "Trước mỗi đợt nghiệm thu phát hành phiên bản mới của DEX Skills Framework."
        ],
        "when_not_use": [
            "Khi chỉnh sửa các tài liệu ghi chú cá nhân tạm thời.",
            "Khi kiểm thử hiệu năng tốc độ xử lý của thuật toán."
        ],
        "prereqs": "Mã nguồn các script trong `scripts/`, danh mục `manifests/dex-skills.json`, toàn bộ các tệp tài liệu `README.md`, `SKILLS_INDEX.md`, `SKILL.md`.",
        "concepts": [
            "Drift Detection Automation: So sánh tự động giữa danh sách cờ tham số của script Python (`argparse`) với phần hướng dẫn sử dụng trong tài liệu Markdown.",
            "Metric Parity in Documentation: Đảm bảo các con số (như '300 skills', '30 groups', '659 tests') phải đồng nhất tuyệt đối trên mọi trang tài liệu.",
            "Executable Documentation as Tests: Kiểm tra xem các khối mã ví dụ trong tài liệu có thực sự chạy được không (Doctest / Markdown Code Testing)."
        ],
        "steps": [
            "Đếm số lượng thư mục kỹ năng thực tế trong `.agents/skills/` và các tệp trong `integrations/`.",
            "Đối chiếu số lượng với các con số ghi trong `README.md`, `SKILLS_INDEX.md` và `ROUTING_MATRIX.md`.",
            "Kiểm tra xem các lệnh gọi script (ví dụ `python scripts/discover_skills.py`) trong các file `SKILL.md` có sử dụng đúng tên cờ tham số hiện tại hay không.",
            "Liệt kê danh sách các điểm trôi lệch tài liệu phát hiện được.",
            "Tự động chạy script tái tạo tài liệu để đồng bộ lại toàn bộ hệ thống."
        ],
        "code_lang": "python",
        "code_example": """# Documentation Drift Detector Script
import os
import re

def detect_documentation_drift(root_dir: str):
    skills_dir = os.path.join(root_dir, ".agents", "skills")
    actual_skills_count = len([d for d in os.listdir(skills_dir) if os.path.isdir(os.path.join(skills_dir, d))])

    readme_path = os.path.join(root_dir, "README.md")
    with open(readme_path, "r", encoding="utf-8") as f:
        readme_content = f.read()

    # Find reported skill count in README
    match = re.search(r'(\d+)\s+Native DEX Skills', readme_content)
    reported_count = int(match.group(1)) if match else None

    drifts = []
    if reported_count != actual_skills_count:
        drifts.append(f"README.md reports {reported_count} skills, but disk contains {actual_skills_count} skills!")

    return drifts""",
        "antipatterns": [
            "Sửa đổi chức năng hoặc tham số của script nhưng không cập nhật tài liệu hướng dẫn, khiến người dùng chạy lệnh theo tài liệu bị báo lỗi.",
            "Cập nhật số lượng kỹ năng trong `README.md` nhưng quên cập nhật trong `SKILLS_INDEX.md` và `ARCHITECTURE.md`.",
            "Để các đoạn code mẫu trong tài liệu sử dụng các hàm đã bị xóa bỏ từ phiên bản trước."
        ],
        "quality_gates": [
            "QG-01: 100% các số liệu thống kê kỹ năng và nhóm đồng nhất tuyệt đối trên toàn bộ các tệp tài liệu.",
            "QG-02: Tất cả các câu lệnh mẫu trong tài liệu đều khớp chính xác với cú pháp hỗ trợ của script thực thi.",
            "QG-03: Không có bất kỳ cảnh báo trôi lệch tài liệu nào tồn tại trong báo cáo nghiệm thu."
        ],
        "security": "Ngăn ngừa việc tài liệu lỗi thời hướng dẫn người dùng thực hiện các cấu hình bảo mật yếu kém đã bị bãi bỏ.",
        "deliverables": [
            "Báo cáo phát hiện trôi lệch tài liệu `DOCUMENTATION_DRIFT_REPORT.md`.",
            "Script tự động đối soát và đồng bộ tài liệu `scripts/build_docs_v6.py`."
        ],
        "related": ["dex-documentation-as-code", "dex-skill-catalog-taxonomy", "dex-skill-execution-evidence-ledger"],
        "scenario": "Sau khi nâng cấp từ 200 lên 300 kỹ năng, kỹ sư kích hoạt `dex-skill-documentation-drift` để rà soát toàn bộ kho tài liệu, phát hiện một số chỗ trong `INSTALL.md` và `ARCHITECTURE.md` vẫn còn ghi '201 native skills', tự động đồng bộ hóa toàn bộ tài liệu về chuẩn '301 Native DEX Skills' chính xác 100%."
    },
    {
        "id": "dex-skill-upgrade-migrations",
        "index": 298,
        "group": "Group AD",
        "domain": "Advanced SkillOps Governance",
        "description": "Orchestrate automated breaking change migrations for Agent Skills across framework versions, transforming deprecated frontmatter schemas, section reorganizations, and API adapters with compatibility shims. Use when upgrading skill packs across major versions (e.g., v5 to v6).",
        "purpose": "Điều phối quy trình di chuyển và nâng cấp kỹ năng tự động khi có thay đổi phá vỡ (Breaking Change Migrations) giữa các phiên bản framework lớn; tự động chuyển đổi cấu trúc YAML Frontmatter lỗi thời, tái cấu trúc các đề mục bắt buộc và cung cấp các lớp tương thích chuyển tiếp (Compatibility Shims); đảm bảo quá trình nâng cấp kho kỹ năng diễn ra trơn tru mà không làm gián đoạn các luồng làm việc sẵn có.",
        "when_use": [
            "Khi nâng cấp DEX Skills Framework từ phiên bản v5.0 lên v6.0 với các yêu cầu chuẩn hóa mới.",
            "Khi đặc tả Agent Skills quốc tế (`agentskills.io/specification`) bổ sung thêm các trường siêu dữ liệu bắt buộc mới.",
            "Khi cần tự động hóa việc định dạng lại hàng trăm tệp `SKILL.md` theo quy chuẩn mới."
        ],
        "when_not_use": [
            "Khi chỉ sửa nội dung câu chữ nhỏ không làm thay đổi cấu trúc lược đồ.",
            "Khi di chuyển cơ sở dữ liệu quan hệ khách hàng."
        ],
        "prereqs": "Lược đồ cũ và lược đồ mới của tệp `SKILL.md`, kịch bản chuyển đổi tự động (Migration Script), bản sao lưu dự phòng Git.",
        "concepts": [
            "Automated AST-Based Migration: Phân tích cú pháp Markdown thành cây cú pháp trừu tượng (AST), sửa đổi các nút cần thiết và xuất lại văn bản mà không làm mất định dạng gốc.",
            "Deprecation Shims: Cung cấp các alias tạm thời cho các kỹ năng đã đổi tên để các quy trình cũ vẫn hoạt động trong thời gian chuyển đổi.",
            "Two-Phase Migration: Giai đoạn 1 đánh dấu cảnh báo lỗi thời (Deprecation Warning), Giai đoạn 2 mới chính thức loại bỏ hoặc chuyển đổi hoàn toàn."
        ],
        "steps": [
            "Tạo một nhánh Git mới dành riêng cho việc nâng cấp phiên bản (`feat/dex-upgrade`).",
            "Quét toàn bộ các tệp `SKILL.md` và nhận diện các phần tử thuộc cấu trúc cũ cần chuyển đổi.",
            "Chạy script di chuyển tự động để tái cấu trúc lại các phần mục và frontmatter.",
            "Chạy lại toàn bộ bộ kiểm thử xác thực `validate_skills.py` để đảm bảo 100% kỹ năng đáp ứng chuẩn mới.",
            "Lập biên bản báo cáo nâng cấp di chuyển `UPGRADE_MIGRATION_REPORT.md`."
        ],
        "code_lang": "python",
        "code_example": """# Skill Frontmatter & Section Migration Runner
def migrate_skill_to_v6(skill_md_content: str) -> str:
    # 1. Update frontmatter version if present
    # 2. Ensure all 14 mandatory sections exist
    # 3. Standardize section headers to English canonical format
    headers_map = {
        "## 1. Mục đích": "## 1. Purpose & Scope",
        "## 2. Khi nào sử dụng": "## 2. When to Use",
        "## 3. Khi nào không sử dụng": "## 3. When NOT to Use",
        # ...
    }
    updated_content = skill_md_content
    for old_h, new_h in headers_map.items():
        updated_content = updated_content.replace(old_h, new_h)

    return updated_content""",
        "antipatterns": [
            "Thực hiện thay đổi phá vỡ cấu trúc kỹ năng trên nhánh `main` mà không có nhánh thử nghiệm và kiểm thử hồi quy.",
            "Ép buộc người dùng phải tự sửa đổi bằng tay hàng trăm file `SKILL.md` thay vì cung cấp công cụ nâng cấp tự động.",
            "Xóa bỏ ngay lập tức các kỹ năng cũ mà không có giai đoạn cảnh báo và shims chuyển tiếp."
        ],
        "quality_gates": [
            "QG-01: 100% các kỹ năng được chuyển đổi thành công sang cấu trúc mới mà không bị mất mát nội dung.",
            "QG-02: Bộ kiểm tra hợp lệ `validate_skills.py` đạt 100% PASSED sau khi chạy quy trình migration.",
            "QG-03: Có sẵn hướng dẫn nâng cấp chi tiết cho người dùng trong tài liệu `CHANGELOG.md`."
        ],
        "security": "Kiểm tra kỹ lưỡng các kịch bản di chuyển để đảm bảo không vô tình làm lộ hoặc xóa bỏ các cấu hình bảo mật quan trọng của kỹ năng.",
        "deliverables": [
            "Script tự động hóa di chuyển kỹ năng `scripts/migrate_skills_v6.py`.",
            "Báo cáo chi tiết quá trình nâng cấp di chuyển `UPGRADE_MIGRATION_REPORT.md`."
        ],
        "related": ["dex-schema-evolution", "dex-skill-retirement-governance", "dex-skill-rollback-verification"],
        "scenario": "Nâng cấp toàn bộ hệ thống DEX Skills lên phiên bản v6.0 với 14 đề mục tiếng Anh chuẩn hóa. Kỹ sư kích hoạt `dex-skill-upgrade-migrations`, chạy script tự động duyệt qua toàn bộ 301 kỹ năng, chuẩn hóa cấu trúc và bảo toàn nội dung chuyên môn tiếng Việt phong phú, hoàn thành nâng cấp trong 5 phút với 0 lỗi cú pháp."
    },
    {
        "id": "dex-skill-rollback-verification",
        "index": 299,
        "group": "Group AD",
        "domain": "Advanced SkillOps Governance",
        "description": "Design deterministic rollback procedures, state restoration drills, and backup verification for skill deployments, guaranteeing zero-downtime recovery from flawed skill updates. Use when deploying critical skill updates or establishing disaster recovery plans.",
        "purpose": "Thiết kế và kiểm chứng quy trình hoàn tác xác định (Deterministic Rollback Procedures); thực hiện diễn tập khôi phục trạng thái (State Restoration Drills) và xác minh tính toàn vẹn của bản sao lưu; đảm bảo khả năng quay trở lại phiên bản kỹ năng an toàn trước đó trong vòng dưới 60 giây khi một bản cập nhật kỹ năng phát sinh lỗi; bảo toàn tính liên tục của hệ thống Agent.",
        "when_use": [
            "Trước khi triển khai một bản cập nhật kỹ năng lớn có tác động sâu rộng lên toàn bộ hệ thống.",
            "Khi một kỹ năng vừa cập nhật bị phát hiện có lỗi làm gián đoạn quá trình điều phối của Master Orchestrator.",
            "Khi thực hiện các bài diễn tập khôi phục sau thảm họa (Disaster Recovery Drills) định kỳ."
        ],
        "when_not_use": [
            "Khi bản cập nhật chỉ sửa một lỗi chính tả nhỏ không gây rủi ro vận hành.",
            "Khi hệ thống đang trong giai đoạn phát triển ban đầu chưa có người sử dụng."
        ],
        "prereqs": "Hệ thống kiểm soát phiên bản Git có gắn thẻ phát hành (Release Tags), bản sao lưu trạng thái trước khi triển khai, kịch bản hoàn tác tự động.",
        "concepts": [
            "Atomic Rollback via Git Revert / Tag Checkout: Khôi phục trạng thái kho kỹ năng về đúng mã commit hash của phiên bản ổn định gần nhất một cách nguyên tử.",
            "Zero-Data-Loss State Cache: Đảm bảo các phiên làm việc đang chạy dở dang của Agent không bị mất dữ liệu khi hệ thống thực hiện hoàn tác kỹ năng.",
            "Post-Rollback Smoke Test: Tự động chạy ngay một bộ kiểm thử nhanh (Smoke Test) sau khi hoàn tác để xác nhận hệ thống đã hồi phục hoàn toàn."
        ],
        "steps": [
            "Trước khi deploy bản cập nhật, tạo một điểm đánh dấu an toàn (Safety Tag hoặc Snapshot).",
            "Mô phỏng tình huống sự cố: bản cập nhật mới làm hỏng khả năng phân tích của Master Orchestrator.",
            "Kích hoạt lệnh hoàn tác tự động đưa kho kỹ năng về điểm an toàn gần nhất.",
            "Chạy bài kiểm thử khói tự động `pytest tests/test_skill_structure.py` để xác nhận trạng thái.",
            "Lập biên bản diễn tập hoàn tác `ROLLBACK_VERIFICATION_REPORT.md` ghi nhận thời gian phục hồi."
        ],
        "code_lang": "bash",
        "code_example": """# Automated Atomic Skill Rollback Script
#!/usr/bin/env bash
set -e

LATEST_STABLE_TAG="v5.0.0"

echo "CRITICAL: Initiating automated rollback to ${LATEST_STABLE_TAG}..."
git checkout "${LATEST_STABLE_TAG}"

# Re-index manifest immediately
python scripts/discover_skills.py --output manifests/dex-skills.json

# Run immediate smoke test verification
python scripts/validate_skills.py

echo "SUCCESS: Rollback to ${LATEST_STABLE_TAG} completed and verified!" """,
        "antipatterns": [
            "Triển khai cập nhật kỹ năng mà không tạo điểm sao lưu hoặc không có phương án hoàn tác khẩn cấp.",
            "Cố gắng sửa lỗi trực tiếp trên môi trường đang gặp sự cố (Hot-patching under panic) thay vì lập tức hoàn tác về bản ổn định.",
            "Hoàn tác mã nguồn kỹ năng nhưng quên cập nhật lại tệp manifest `dex-skills.json`, khiến hệ thống bị lệch trạng thái."
        ],
        "quality_gates": [
            "QG-01: Thời gian hoàn tác toàn bộ kho kỹ năng về trạng thái ổn định dưới 60 giây.",
            "QG-02: Bộ kiểm thử xác thực tự động chạy thành công 100% ngay sau khi hoàn tác.",
            "QG-03: Bản sao lưu dự phòng được kiểm tra tính toàn vẹn định kỳ hàng tháng."
        ],
        "security": "Bảo vệ các thẻ phát hành Git an toàn (Protected Tags) để ngăn ngừa việc xóa nhầm các điểm khôi phục ổn định.",
        "deliverables": [
            "Kịch bản hoàn tác tự động khẩn cấp `scripts/emergency_rollback.sh`.",
            "Biên bản diễn tập hoàn tác và khôi phục trạng thái `ROLLBACK_VERIFICATION_REPORT.md`."
        ],
        "related": ["dex-skill-upgrade-migrations", "dex-disaster-recovery", "dex-skill-retirement-governance"],
        "scenario": "Một bản cập nhật kỹ năng vô tình làm thay đổi cấu trúc bảng phân loại khiến Master Orchestrator bị lỗi định tuyến. Kỹ sư kích hoạt `dex-skill-rollback-verification`, thực thi kịch bản hoàn tác khẩn cấp đưa hệ thống về tag `v5.0.0` trong 22 giây, chạy smoke test xác nhận hệ thống hoạt động ổn định trở lại, bảo vệ uy tín dịch vụ."
    },
    {
        "id": "dex-skill-retirement-governance",
        "index": 300,
        "group": "Group AD",
        "domain": "Advanced SkillOps Governance",
        "description": "Govern the graceful deprecation, sunsetting, and archival lifecycle of obsolete Agent Skills, decoupling downstream dependencies, redirecting semantic intents, and maintaining historical provenance. Use when retiring legacy skills without breaking existing workflows.",
        "purpose": "Quản trị toàn bộ vòng đời bãi bỏ, ngừng hỗ trợ và lưu trữ (Deprecation, Sunsetting & Archival Lifecycle) cho các kỹ năng AI Agent đã lỗi thời; tách rời an toàn các phụ thuộc hạ nguồn, tự động chuyển hướng ý định ngữ nghĩa sang kỹ năng thay thế hiện đại hơn và duy trì sổ cái nguồn gốc lịch sử; đảm bảo việc loại bỏ kỹ năng cũ diễn ra êm đẹp không làm vỡ các quy trình tự động hóa sẵn có.",
        "when_use": [
            "Khi một kỹ năng cũ đã được thay thế hoàn toàn bởi một kỹ năng mới mạnh mẽ hơn (ví dụ: chuyển từ kỹ năng MV2 sang MV3).",
            "Khi một công cụ hoặc API bên thứ ba mà kỹ năng dựa vào đã bị nhà cung cấp khai tử vĩnh viễn.",
            "Khi tinh gọn danh mục kỹ năng để loại bỏ các kỹ năng trùng lặp hoặc không còn giá trị thực tế."
        ],
        "when_not_use": [
            "Khi kỹ năng vẫn đang được sử dụng tích cực trong các quy trình quan trọng.",
            "Khi chỉ tạm thời vô hiệu hóa kỹ năng trong một khoảng thời gian ngắn để bảo trì."
        ],
        "prereqs": "Kỹ năng thay thế đã sẵn sàng và được kiểm chứng, danh sách các kỹ năng phụ thuộc, chính sách thông báo lỗi thời (Sunsetting Policy).",
        "concepts": [
            "Graceful Deprecation Phases: Giai đoạn 1: Thông báo lỗi thời (Deprecated Warning) kèm gợi ý kỹ năng mới -> Giai đoạn 2: Ngừng hỗ trợ (Sunsetting) -> Giai đoạn 3: Lưu trữ lịch sử (Archived).",
            "Intent Redirection: Khi người dùng hoặc Agent yêu cầu kỹ năng cũ đã bị bãi bỏ, bộ định tuyến tự động chuyển hướng sang kỹ năng thay thế mới kèm thông báo giải thích.",
            "Historical Provenance Preservation: Không xóa vĩnh viễn mã nguồn kỹ năng cũ mà di chuyển vào thư mục lưu trữ `archive/` để phục vụ tra cứu lịch sử."
        ],
        "steps": [
            "Đánh dấu trạng thái `status: deprecated` và trường `superseded_by: new-skill-id` trong frontmatter của kỹ năng.",
            "Cập nhật Master Orchestrator để tự động chuyển hướng các lệnh gọi kỹ năng cũ sang kỹ năng mới.",
            "Rà soát và cập nhật toàn bộ các kỹ năng khác đang liên kết tới kỹ năng cũ trong Mục 13.",
            "Duy trì giai đoạn thông báo lỗi thời trong tối thiểu 30 ngày trước khi chính thức lưu trữ.",
            "Di dời thư mục kỹ năng vào kho lưu trữ lịch sử và cập nhật `SKILLS_INDEX.md`."
        ],
        "code_lang": "yaml",
        "code_example": """# Deprecated Skill Frontmatter Header
---
name: dex-legacy-manifest-v2
description: (DEPRECATED) Legacy Manifest V2 browser extension skill. Superseded by dex-browser-extension-mv3.
status: deprecated
deprecated_at: "2026-10-22"
superseded_by: dex-browser-extension-mv3
---

> [!WARNING]
> Kỹ năng này đã chính thức ngừng hỗ trợ (Deprecated). 
> Vui lòng sử dụng kỹ năng thay thế hiện đại hơn: [`dex-browser-extension-mv3`](.agents/skills/dex-browser-extension-mv3/SKILL.md).""",
        "antipatterns": [
            "Xóa bỏ đột ngột một kỹ năng khỏi kho mà không có thông báo trước, làm sập toàn bộ các kịch bản tự động hóa đang gọi kỹ năng đó.",
            "Bãi bỏ kỹ năng cũ khi chưa có kỹ năng mới sẵn sàng thay thế hoàn chỉnh.",
            "Không chuyển hướng ý định trong bộ định tuyến khiến người dùng nhận được thông báo lỗi không tìm thấy kỹ năng."
        ],
        "quality_gates": [
            "QG-01: 100% các kỹ năng bãi bỏ đều có trường chỉ định kỹ năng thay thế `superseded_by` hợp lệ.",
            "QG-02: Bộ định tuyến tự động chuyển hướng thành công các yêu cầu kỹ năng cũ sang kỹ năng mới đạt tỷ lệ 100%.",
            "QG-03: Không còn bất kỳ kỹ năng đang hoạt động nào phụ thuộc vào kỹ năng đã bãi bỏ."
        ],
        "security": "Ngăn chặn việc kẻ xấu khai thác các kỹ năng cũ chứa mã lỗi thời bằng cách vô hiệu hóa hoàn toàn quyền thực thi của các kỹ năng trong kho lưu trữ.",
        "deliverables": [
            "Chính sách bãi bỏ và chuyển hướng kỹ năng `SKILL_RETIREMENT_POLICY.md`.",
            "Kho lưu trữ kỹ năng lịch sử `archive/legacy-skills/`."
        ],
        "related": ["dex-skill-upgrade-migrations", "dex-skill-catalog-taxonomy", "dex-master-orchestrator"],
        "scenario": "DEX Framework chuẩn hóa lên v6.0 và cần bãi bỏ các kỹ năng thử nghiệm cũ. Kỹ sư kích hoạt `dex-skill-retirement-governance`, đánh dấu deprecated cho 3 kỹ năng cũ, cấu hình Master Orchestrator tự động chuyển hướng sang các kỹ năng Group W mới, di dời mã cũ vào archive, giúp toàn bộ hệ sinh thái chuyển mình sang phiên bản mới êm đẹp mà không có bất kỳ lỗi gián đoạn nào."
    }
]

def build_markdown(meta):
    md = f"""---
name: {meta['id']}
description: {meta['description']}
---

# {meta['id']}

## 1. Purpose & Scope
{meta['purpose']}

## 2. When to Use
"""
    for item in meta['when_use']:
        md += f"- {item}\n"

    md += "\n## 3. When NOT to Use\n"
    for item in meta['when_not_use']:
        md += f"- {item}\n"

    md += f"""
## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** {meta['prereqs']}
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; bảo vệ toàn vẹn tài sản kỹ nghệ và dữ liệu sản xuất.

## 5. Core Concepts & Taxonomy
"""
    for item in meta['concepts']:
        md += f"- **{item.split(':', 1)[0]}:**{item.split(':', 1)[1] if ':' in item else ''}\n"

    md += "\n## 6. Step-by-Step Execution Workflow\n"
    for i, step in enumerate(meta['steps'], 1):
        md += f"{i}. {step}\n"

    md += f"""
## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```{meta['code_lang']}
{meta['code_example']}
```

## 8. Anti-Patterns & Common Traps
"""
    for item in meta['antipatterns']:
        md += f"- {item}\n"

    md += "\n## 9. Quality Gates & Acceptance Criteria\n"
    for item in meta['quality_gates']:
        md += f"- {item}\n"

    md += f"""
## 10. Security & Safety Boundaries
- {meta['security']}
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
"""
    for item in meta['deliverables']:
        md += f"1. {item}\n"

    md += "\n## 13. Related & Complementary Skills\n"
    for r in meta['related']:
        md += f"- [`{r}`](.agents/skills/{r}/SKILL.md)\n"

    md += f"""
## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
{meta['scenario']}
"""
    return md

def generate_skills():
    if sys.stdout.encoding != "utf-8" and hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    for s in GROUP_AC_AD_SKILLS:
        skill_dir = os.path.join(SKILLS_DIR, s["id"])
        os.makedirs(skill_dir, exist_ok=True)
        skill_file = os.path.join(skill_dir, "SKILL.md")
        content = build_markdown(s)
        with open(skill_file, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[OK] Generated {s['id']} (Skill {s['index']:03d})")

if __name__ == "__main__":
    generate_skills()
