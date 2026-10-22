---
name: dex-compliance-control-mapping
description: Map engineering, cloud, and process controls to compliance frameworks (SOC 2 Type II, ISO 27001, HIPAA, PCI-DSS) with automated evidence collection. Use when preparing for security audits and demonstrating regulatory compliance.
---

# dex-compliance-control-mapping

## 1. Purpose & Scope
Ánh xạ các biện pháp kiểm soát kỹ thuật, hạ tầng đám mây và quy trình phát triển phần mềm vào các khung tiêu chuẩn tuân thủ an toàn thông tin quốc tế (SOC 2 Type II, ISO/IEC 27001:2022, HIPAA, PCI-DSS 4.0); tự động hóa việc thu thập bằng chứng kiểm toán (Automated Evidence Collection) từ Git, AWS/GCP, Identity Provider và CI/CD; thiết lập ma trận kiểm soát (Control Mapping Matrix) phục vụ việc đánh giá của kiểm toán viên độc lập.

## 2. When to Use
- Khi doanh nghiệp chuẩn bị bước vào đợt đánh giá chứng nhận SOC 2 Type II hoặc ISO 27001.
- Khi khách hàng doanh nghiệp (Enterprise B2B) gửi bảng câu hỏi đánh giá bảo mật nhà cung cấp (Vendor Security Assessment) dài hàng trăm câu hỏi.
- Khi cần kết nối các công cụ giám sát tuân thủ tự động (Vanta, Drata, Secureframe) vào hệ thống kỹ thuật.

## 3. When NOT to Use
- Tối ưu hóa hiệu năng ứng dụng máy tính (dùng `dex-mobile-performance-profiling`).
- Thiết lập cấu hình mạng Kubernetes (dùng `dex-service-mesh-networking`).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Khung tiêu chuẩn mục tiêu (SOC 2 Trust Services Criteria: Security, Availability, Confidentiality; ISO 27001 Annex A).
- Danh sách hệ thống công nghệ thông tin và nhà cung cấp dịch vụ đám mây.
- Các chính sách nội bộ (Access Control Policy, Change Management Policy, Incident Response Plan).
- **Điều kiện tiên quyết**:
- Có quyền truy cập cấu hình hệ thống hạ tầng và công cụ quản trị mã nguồn (GitHub/GitLab admin).
- Đã thiết lập Single Sign-On (SSO) và xác thực đa yếu tố (MFA) trên toàn bộ tổ chức.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- **Trust Services Criteria (TSC)**: Khung 5 tiêu chí của SOC 2: CC6 (Logical & Physical Access Controls), CC7 (System Operations), CC8 (Change Management).
- **Continuous Evidence Collection**: Thay vì chụp màn hình thủ công 6 tháng một lần, hệ thống sử dụng API để tự động kiểm tra định kỳ hàng ngày: 'Toàn bộ repo có bật branch protection không? Toàn bộ S3 bucket có bật encryption không?'.
- **Point-in-Time (Type I) vs Period-of-Time (Type II)**: Type I chỉ đánh giá thiết kế tại 1 thời điểm; Type II chứng minh các biện pháp kiểm soát vận hành liên tục và hiệu quả trong suốt 6-12 tháng.
- **Quy tắc quyết định kỹ thuật**:
- **Bắt Buộc Bật Branch Protection Trên 100% Repository**: Mọi commit vào nhánh chính phải thông qua Pull Request, có ít nhất 1 code review và pass bài kiểm tra CI tự động (kiểm soát CC8.1).
- **Bắt Buộc Mã Hóa Dữ Liệu Lưu Trữ (At-Rest) và Trên Đường Truyền (In-Transit)**: 100% cơ sở dữ liệu và lưu trữ object phải bật mã hóa chuẩn tối thiểu AES-256.
- **Không Dùng Tài Khoản Chung (No Shared Credentials)**: Mọi kỹ sư phải đăng nhập bằng tài khoản cá nhân có gắn MFA; cấm dùng chung user `admin` hay `root`.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Trượt bài kiểm toán SOC 2 do có commit đẩy thẳng vào nhánh main**: Một kỹ sư dùng quyền admin bypass branch rule để vá lỗi nhanh -> Khắc phục: Khóa vĩnh viễn quyền bypass trên GitHub Branch Ruleset, lưu vết mọi thay đổi qua PR.
- **Bị phạt do nhân viên nghỉ việc vẫn còn quyền truy cập AWS**: Do quy trình offboarding làm thủ công sót tài khoản -> Khắc phục: Áp dụng SSO tập trung (Okta / Google Workspace); vô hiệu hóa tài khoản SSO sẽ tự động cắt quyền toàn bộ hệ thống.

## 6. Step-by-Step Execution Workflow
1. Lựa chọn các danh mục kiểm soát tương ứng trong khung tiêu chuẩn (SOC 2 CC1 đến CC9).
2. Xây dựng Ma trận Ánh xạ Kiểm soát (Control Mapping Matrix): Nối từng yêu cầu tiêu chuẩn với bằng chứng kỹ thuật cụ thể.
3. Thiết lập chính sách Change Management: Bắt buộc PR, 2 reviewer, CI checks, không có exception.
4. Cấu hình bảo mật hạ tầng đám mây: Bật AWS CloudTrail, AWS Config Rules, S3 Block Public Access, KMS Encryption.
5. Tự động hóa việc quét bằng chứng định kỳ qua CLI hoặc công cụ tuân thủ (Vanta / Drata).
6. Thu thập mẫu bằng chứng (Sampling Evidence) cho giai đoạn kiểm toán: Danh sách 25 PR ngẫu nhiên, danh sách nhân viên mới tuyển/nghỉ việc.
7. Phối hợp với kiểm toán viên độc lập (CPA firm) rà soát bằng chứng và giải trình các ngoại lệ.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```markdown
# SOC 2 Type II Control Mapping Matrix (Trích đoạn)

| Control ID | Tiêu Chuẩn SOC 2 | Mô Tả Kiểm Soát Kỹ Thuật | Nguồn Bằng Chứng Kỹ Thuật | Tần Suất |
|:---|:---|:---|:---|:---|
| **SEC-01** | CC6.1 (Logical Access) | Xác thực tập trung qua SSO + Bắt buộc MFA | Cấu hình Okta / Google Workspace Admin Export | Liên tục |
| **SEC-02** | CC6.3 (Least Privilege) | Phân quyền truy cập đám mây qua IAM Roles ngắn hạn | AWS IAM Credential Report & Terraform Code | Hàng ngày |
| **SEC-03** | CC6.6 (Encryption at Rest) | Toàn bộ RDS và S3 bật mã hóa KMS AES-256 | AWS Config Rule `encrypted-volumes-check` | Hàng ngày |
| **CHG-01** | CC8.1 (Change Authorization) | 100% code thay đổi phải qua PR có review và pass CI | GitHub API `/repos/{owner}/{repo}/branches/main/protection` | Liên tục |
| **OPS-01** | A1.2 (Data Backup) | Tự động snapshot RDS hàng ngày và test restore định kỳ | AWS Backup Vault Report & Log diễn tập khôi phục | Hàng tháng |
| **VUL-01** | CC7.1 (Vulnerability Scanning) | Tự động quét lỗ hổng mã nguồn và container trong CI | Báo cáo GitHub Dependabot & Trivy Scan Logs | Mỗi build |
```

### Lệnh xác minh & thực thi:
- Kiểm tra cấu hình bảo vệ branch GitHub qua API: `gh api /repos/:owner/:repo/branches/main/protection --jq '{required_reviews: .required_pull_request_reviews.required_approving_review_count, enforce_admins: .enforce_admins.enabled}'`
- Tạo báo cáo chứng thực tài khoản AWS IAM: `aws iam generate-credential-report && aws iam get-credential-report --output text --query 'Content' | base64 -d`
- Kiểm tra tình trạng mã hóa S3: `aws s3api get-bucket-encryption --bucket my-app-prod-data`

## 8. Anti-Patterns & Common Traps
- **Lập tài liệu quy trình hình thức nhưng thực tế làm khác**: Khi kiểm toán viên kiểm tra ngẫu nhiên 5 PR phát hiện có 2 PR merge không cần review sẽ bị đánh lỗi nghiêm trọng (Qualified Opinion).
- **Chỉ tập trung vào công nghệ mà bỏ qua quy trình nhân sự**: Không kiểm tra lý lịch nhân viên (Background check) hoặc không ký cam kết bảo mật NDA.
- **Tắt log kiểm toán để tiết kiệm chi phí lưu trữ**: Khiến hệ thống không thể cung cấp bằng chứng cho kiểm toán viên.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Ma trận kiểm soát bao phủ 100% các tiêu chí bắt buộc của khung tiêu chuẩn mục tiêu.
- QG-08: Tỷ lệ bằng chứng thu thập tự động đạt tối thiểu 90%.
- QG-12: Không có bất kỳ ngoại lệ (exceptions) nào vi phạm chính sách Change Management trong thời kỳ kiểm toán.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi deploy.

## 10. Security & Safety Boundaries
- Bằng chứng kiểm toán phải được lưu trữ bất biến (Immutable storage) để chống làm giả hoặc sửa đổi sau sự cố.
- Giới hạn quyền truy cập vào các bằng chứng kiểm toán nhạy cảm (chỉ định rõ ai được xem báo cáo pentest).
- Không bao giờ lưu trữ hardcoded secret hoặc cấp quyền quá mức (over-permissioned IAM).

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Môi trường Vận hành & Tuân thủ**: Hỗ trợ GDPR/CCPA tooling, SOC 2 / ISO 27001 automation, ArgoCD drift, RICE spreadsheets, Jira/GitHub triage.

## 12. Deliverables & Output Artifacts
- Bảng Ma trận Kiểm soát Tuân thủ (Compliance Control Matrix).
- Bộ kịch bản thu thập bằng chứng tự động (Evidence Collection Scripts).
- Báo cáo kiểm toán SOC 2 Type II / ISO 27001 từ đơn vị kiểm toán độc lập.

## 13. Related & Complementary Skills
- `dex-privacy-impact-assessment`: Đảm bảo các biện pháp tuân thủ quyền riêng tư dữ liệu cá nhân.
- `dex-audit-trail-integrity`: Cung cấp bằng chứng log không thể chối cãi cho kiểm toán viên.
- `dex-code-review`: Thực thi cửa ải duyệt mã nguồn theo chuẩn Change Management.

## 14. Realistic Usage Example
### Tình huống thực tế:
Một công ty SaaS phần mềm B2B cần đạt chứng nhận SOC 2 Type II để ký hợp đồng với khách hàng ngân hàng. Áp dụng `dex-compliance-control-mapping`, kỹ sư trưởng lập ma trận ánh xạ cho 45 tiêu chí kiểm soát, tự động hóa việc xuất log GitHub PR và cấu hình mã hóa AWS S3/RDS, khóa chặt quyền merge code chỉ qua PR có ít nhất 2 approvals. Trong đợt kiểm toán 6 tháng, đơn vị kiểm toán CPA đã xác minh 100% bằng chứng sạch sẽ và cấp chứng chỉ SOC 2 Type II không có bất kỳ điểm lưu ý ngoại lệ nào.
