---
name: dex-environment-promotion
description: Design deterministic, automated promotion pipelines moving identical immutable release artifacts across Dev, Staging, and Production with rigorous gate checks. Use to eliminate environment drift and release surprises.
---

# dex-environment-promotion

## 1. Purpose & Scope
Thiết kế và quản trị quy trình thăng cấp môi trường (Environment Promotion Pipelines) chuyển dịch các gói phát hành bất biến (Immutable Artifacts) qua chuỗi môi trường Dev -> Staging -> Production; áp dụng các cổng kiểm soát nghiêm ngặt (Release Gates), loại bỏ hiện tượng 'chạy được trên dev nhưng lỗi trên staging', và đảm bảo tính nhất quán tuyệt đối của mã nhị phân.

## 2. When to Use
- Xuất hiện tình trạng mã nguồn được build lại độc lập ở từng môi trường dẫn đến sai lệch phiên bản thư viện hoặc binary.
- Quy trình release lên production thủ công, dễ nhầm lẫn và phụ thuộc vào một vài cá nhân.
- Cần tự động hóa việc thăng cấp phiên bản sau khi các bài kiểm thử tự động trên Staging vượt qua thành công.

## 3. When NOT to Use
- Không build lại Docker image từ source code khi thăng cấp lên môi trường tiếp theo (phải thăng cấp chính digest SHA của image đã test ở Dev/Staging).
- Không áp dụng cho các môi trường thử nghiệm tạm thời (Ephemeral Preview Environments).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Digest SHA của container image hoặc build artifact bất biến.
- Danh sách các biến môi trường và file cấu hình theo từng môi trường.
- Tiêu chí thăng cấp (Pass 100% smoke test, approval từ QA/Lead).
- **Điều kiện tiên quyết**:
- Hệ thống CI/CD có hỗ trợ pipeline gates (GitHub Actions Environments, GitLab Environments).

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Build Once, Deploy Everywhere: Một container image duy nhất được build tại nhánh main và được test qua tất cả môi trường; cấu hình được bơm qua environment variables, tuyệt đối không thay đổi mã máy bên trong image.
- GitOps Branch/Directory Promotion: Thăng cấp bằng cách cập nhật image tag trong file manifest của từng thư mục môi trường (`overlays/staging` -> `overlays/prod`) qua Pull Request.
- Automated Smoke Testing: Sau khi deploy lên Staging, pipeline tự động chạy kiểm thử hồi quy trước khi cho phép kích hoạt nút thăng cấp Prod.
- **Quy tắc quyết định kỹ thuật**:
- Nếu bất kỳ bài smoke test nào trên Staging thất bại: khóa tự động tiến trình thăng cấp lên Production.
- Triển khai lên Production bắt buộc phải có tối thiểu 1 phê duyệt từ người có thẩm quyền (Required Approvers).
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Deploy thẳng lên Production một image tag trôi nổi như `latest` thay vì immutable semantic version hoặc git commit SHA.

## 6. Step-by-Step Execution Workflow
1. Build container image tại CI, gắn tag bằng Git commit SHA và digest (`sha256:...`).
2. Tự động deploy lên môi trường Dev và chạy unit/integration tests.
3. Thăng cấp lên Staging: cập nhật manifest Staging và kích hoạt E2E/Load tests.
4. Khi Staging đạt 100% tiêu chí xanh: mở cổng yêu cầu phê duyệt Production.
5. Thăng cấp lên Production kèm chiến lược Canary hoặc Blue/Green.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```yaml
# GitHub Actions Environment Promotion Workflow
jobs:
  deploy-prod:
    needs: deploy-staging
    runs-on: ubuntu-latest
    environment:
      name: production
      url: https://app.example.com
    steps:
      - name: Promote Immutable Image to Production Manifest
        run: |
          IMAGE_SHA="${{ needs.deploy-staging.outputs.image_sha }}"
          # Cập nhật GitOps manifest của production với đúng SHA đã test tại Staging
          yq eval ".images[0].digest = \"$IMAGE_SHA\"" -i kustomize/overlays/prod/kustomization.yaml
```

### Lệnh xác minh & thực thi:
```bash
# So sánh image digest giữa môi trường Staging và Production
kustomize build kustomize/overlays/staging | grep 'image:'
kustomize build kustomize/overlays/prod | grep 'image:'
```

## 8. Anti-Patterns & Common Traps
- Biên dịch lại mã nguồn từ nhánh `staging` rồi lại biên dịch từ nhánh `production` (nguy cơ sai lệch commit).
- Sửa trực tiếp biến môi trường của Production bằng tay trên console mà không lưu vào cấu hình quản lý.

## 9. Quality Gates & Acceptance Criteria
- 100% artifact được deploy lên Production phải trùng khớp hoàn toàn Digest SHA với artifact đã chạy thành công trên Staging.
- Phải có biên bản phê duyệt điện tử trước khi release Production.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Quyền thăng cấp lên Production chỉ được cấp cho những người được ủy quyền thông qua quy trình phê duyệt MFA.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ thống hỗ trợ**: Cloud Runtimes (AWS Lambda, Cloudflare Workers, Kubernetes), Linux, Windows 11.

## 12. Deliverables & Output Artifacts
- Pipeline CI/CD đa môi trường với Approval Gates.
- Lịch sử audit log của từng đợt thăng cấp môi trường.

## 13. Related & Complementary Skills
dex-gitops-workflows, dex-platform-service-catalog, dex-container-image-engineering

## 14. Realistic Usage Example
### Tình huống thực tế:
Một công ty SaaS trước đây build lại Dockerfile ở mỗi môi trường, dẫn đến sự cố một thư viện npm bị tác giả cập nhật âm thầm khiến Production bị sập trong khi Staging vẫn chạy tốt. Sau khi áp dụng nguyên lý Build Once với immutable digest promotion, họ đã chấm dứt hoàn toàn các lỗi bất ngờ khi đưa code lên môi trường thật.
