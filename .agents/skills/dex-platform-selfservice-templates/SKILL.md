---
name: dex-platform-selfservice-templates
description: Design, validate, and govern internal developer platform self-service templates (Backstage, Cookiecutter, Copier). Enforce security guardrails, CI/CD scaffolding, and architectural standards.
---

# dex-platform-selfservice-templates

## 1. Purpose & Scope
Thiết kế, kiểm định và quản trị các mẫu dự án tự phục vụ cho nền tảng kỹ thuật nội bộ (Internal Developer Platform Self-Service Templates: Spotify Backstage Software Templates, Cookiecutter, Copier); cung cấp khả năng khởi tạo nhanh chóng các dự án microservices, thư viện hoặc hạ tầng mới tuân thủ 100% các tiêu chuẩn kiến trúc, rào chắn bảo mật mặc định (Security Guardrails), đường ống CI/CD tích hợp sẵn và quy định về quyền sở hữu (Ownership & Service Catalog).

## 2. When to Use
- Khi xây dựng Nền tảng Kỹ thuật Nội bộ (Internal Developer Platform - IDP) để nâng cao trải nghiệm nhà phát triển (Developer Experience - DevEx).
- Khi các đội ngũ kỹ thuật mất quá nhiều thời gian (nhiều ngày hoặc nhiều tuần) chỉ để khởi tạo một microservice mới với đầy đủ CI/CD, linting, logging và bảo mật.
- Khi muốn chuẩn hóa cấu trúc thư mục, quy ước đặt tên và các phụ thuộc dùng chung trên toàn bộ công ty.

## 3. When NOT to Use
- Khi dự án là một thử nghiệm nghiên cứu một lần (PoC / Spike) không có kế hoạch đưa vào vận hành hoặc tích hợp vào hệ sinh thái chung.
- Khi tạo các script ngắn đơn lẻ không có cấu trúc dự án hoàn chỉnh.

## 4. Prerequisites & Input Context
- **Công cụ tạo mẫu:** Backstage Software Templates, Cookiecutter, hoặc Copier (hỗ trợ cập nhật mẫu).
- **Kho lưu trữ mẫu:** Git repository chứa mã nguồn mẫu chuẩn hóa kèm tệp định nghĩa metadata.

## 5. Core Concepts & Taxonomy
- **Golden Path / Paved Road:** Lộ trình khuyến nghị tốt nhất được nền tảng kỹ thuật bảo đảm và hỗ trợ tối đa, giúp kỹ sư đi nhanh và an toàn mà không phải tự quyết định mọi thứ.
- **Template Scaffolding:** Quy trình nhận các tham số đầu vào từ người dùng (tên dịch vụ, chủ sở hữu, loại CSDL) và điền vào các tệp khuôn mẫu Jinja2 để sinh ra kho mã nguồn mới.
- **Template Drift & Lifecycle:** Khả năng cập nhật các thay đổi mới của mẫu mẹ (Template) vào các dự án con đã được sinh ra trước đó (sử dụng tính năng `copier update`).

## 6. Step-by-Step Execution Workflow
1. Khảo sát các thành phần thiết yếu của một dịch vụ chuẩn: Lược đồ cấu trúc thư mục, tệp CI/CD, Dockerfile bảo mật, cấu hình SonarQube, Helm Chart.
2. Xây dựng khuôn mẫu dự án sử dụng cú pháp Jinja2 trong Copier hoặc Cookiecutter.
3. Định nghĩa tệp kê khai Backstage `template.yaml` với các bước kiểm tra tính hợp lệ của tham số đầu vào.
4. Tự động hóa các bước hậu tạo mẫu: Tạo repository mới trên GitHub/GitLab, cấu hình Branch Protection Rules, và đăng ký vào Service Catalog.
5. Viết bộ kiểm thử tự động sinh dự án thử nghiệm (Smoke Test) và kiểm tra khả năng build/test thành công của dự án sinh ra.
6. Xuất bản mẫu lên Cổng thông tin nhà phát triển nội bộ (Developer Portal).

## 7. Concrete Examples
### Dinh nghia Backstage Software Template khoi tao Microservice chuan:
```yaml
apiVersion: backstage.io/v1alpha1
kind: Template
metadata:
  name: standard-fastapi-service
  title: Standard FastAPI Microservice
  description: Scaffold a production-ready Python FastAPI microservice with CI/CD, Docker, and Security guardrails.
  tags:
    - python
    - fastapi
    - microservice
spec:
  owner: team-platform-engineering
  type: service

  parameters:
    - title: Service Configuration
      required:
        - service_name
        - owner
      properties:
        service_name:
          title: Service Name
          type: string
          description: Unique kebab-case identifier for the service
          pattern: '^[a-z0-9-]+$'
        owner:
          title: Owner Team
          type: string
          description: GitHub team slug responsible for this service
        enable_database:
          title: Enable PostgreSQL Database
          type: boolean
          default: false

  steps:
    - id: template
      name: Fetch and Render Template
      action: fetch:template
      input:
        url: ./skeleton
        values:
          service_name: ${{ parameters.service_name }}
          owner: ${{ parameters.owner }}
          enable_database: ${{ parameters.enable_database }}

    - id: publish
      name: Publish to GitHub
      action: publish:github
      input:
        repoUrl: github.com?owner=my-org&repo=${{ parameters.service_name }}
        defaultBranch: main
        protectDefaultBranch: true

    - id: register
      name: Register in Software Catalog
      action: catalog:register
      input:
        repoContentsUrl: ${{ steps['publish'].output.repoContentsUrl }}
        catalogInfoPath: '/catalog-info.yaml'
```

## 8. Anti-Patterns & Common Traps
- **Bloated Kitchen-Sink Templates:** Nhồi nhét tất cả các thư viện và tính năng có thể có vào một mẫu duy nhất khiến dự án sinh ra chứa hàng trăm tệp rác không sử dụng.
- **Hardcoding Corporate Secrets in Skeletons:** Để lộ API key thử nghiệm hoặc mật khẩu mẫu trong các tệp skeleton của template.
- **Zero Maintenance on Golden Paths:** Bỏ rơi các mẫu dự án sau khi tạo, không cập nhật phiên bản thư viện bảo mật khiến các dự án mới sinh ra đã chứa sẵn lỗ hổng CVE.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: 100% dự án được sinh ra từ mẫu vượt qua lệnh build và kiểm thử tự động với kết quả PASS ngay từ lần đầu tiên.
- **QG-02**: Tệp `catalog-info.yaml` hợp lệ được tạo và liên kết chính xác với thông tin nhóm sở hữu (Team Ownership).
- **QG-03**: Dự án mới tự động kích hoạt các luồng kiểm tra bảo mật (Secret Scanning, SAST, Dependency Audit) trên nhánh chính.

## 10. Security & Safety Boundaries
- Bắt buộc kích hoạt Branch Protection Rules và bắt buộc Review trước khi merge trên mọi kho mã nguồn mới được sinh ra từ template.

## 11. Platform Adapters
- **Runtimes**: Spotify Backstage, Copier, Cookiecutter, GitHub API, GitLab API.

## 12. Deliverables & Output Artifacts
- Thư mục khung mẫu dự án chuẩn (`template_skeleton/`).
- Tệp định nghĩa mẫu tự phục vụ (`template.yaml`).

## 13. Related & Complementary Skills
dex-terraform-module-contract-tests, dex-infrastructure-policy-as-code, dex-kubernetes-secret-delivery

## 14. Realistic Usage Example
```bash
# Kiem thu sinh du an tu template Copier cuc bo
copier copy ./templates/fastapi-service ./output-test --data service_name=test-api
cd ./output-test && pytest
```
