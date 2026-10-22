---
name: dex-cicd-automation
description: Continuous Integration and Continuous Delivery (CI/CD) pipeline design, configuration, and automated test orchestration. Builds pipelines, writes GitHub Actions workflows, automates linting, test suites, and security scans. Use when configuring CI/CD, repairing broken pipelines, or automating test enforcement.
---

# DEX CI/CD Automation

## 1. Purpose & Scope
Tự động hóa hoàn toàn quy trình kiểm tra chất lượng mã nguồn, biên dịch, chạy test và quét bảo mật mỗi khi có thay đổi được đẩy lên kho lưu trữ (Git), đảm bảo tính đồng nhất và loại bỏ hoàn toàn các lỗi do yếu tố con người.

Quy trình CI/CD chuẩn:
`Git Push → CI chạy → Kiểm tra code → Build → Test → Quét bảo mật → PASS/FAIL → Merge hoặc Deploy`

Nguyên tắc cốt lõi: **Mọi thay đổi mã nguồn phải được kiểm tra tự động trước khi được phép hợp nhất (Merge) hoặc phát hành (Deploy).**
Ghi nhớ sống còn: **CI/CD tốt = Tự động kiểm tra + Phát hiện lỗi sớm + Phát hành an toàn.**

## 2. When to Use
- Thiết lập quy trình CI/CD mới cho dự án (ví dụ: GitHub Actions, GitLab CI).
- Bổ sung các bước kiểm tra tự động: Linting, Type checking, Unit test, Security scan, Build artifact.
- Chẩn đoán và sửa lỗi khi pipeline CI/CD bị gãy (Broken build).
- Thiết lập quy tắc bảo vệ nhánh (Branch Protection Rules) yêu cầu CI phải PASS mới cho merge.

## 3. When NOT to Use
- Viết code nghiệp vụ thông thường trên máy cục bộ (Local development).
- Triển khai thủ công các lệnh script tạm thời trên máy cá nhân không qua pipeline.

## 4. Prerequisites & Input Context
- Cấu hình dự án (Ngôn ngữ, phiên bản runtime: Node 20, Python 3.12...).
- Các lệnh script có sẵn trong `package.json`, `Makefile` hoặc script build.
- Cấu hình hệ thống CI mục tiêu (thư mục `.github/workflows/` đối với GitHub Actions).

## 5. Core Concepts & Taxonomy
- **Nguyên tắc cốt lõi**: Tuân thủ triệt để nguyên lý vận hành xác định và ranh giới trách nhiệm của chuẩn Agent Skills.
- **Tính nhất quán hệ thống**: Mọi thao tác phải có thể kiểm chứng độc lập với kết quả đo lường rõ ràng.
- **Ngăn ngừa hồi quy**: Bất kỳ sửa đổi nào cũng phải bảo vệ tính tương thích ngược và chất lượng đã được nghiệm thu.

## 6. Step-by-Step Execution Workflow
### Bước 1: Khảo Sát & Chuẩn Hóa Lệnh Cục Bộ (Script Readiness)
- Đảm bảo các script chạy độc lập trên máy cục bộ trước khi đưa lên CI:
  - Lệnh linter / format: `npm run lint`
  - Lệnh type check: `npm run type-check`
  - Lệnh test: `npm test`
  - Lệnh build: `npm run build`

### Bước 2: Thiết Kế Workflow Pipeline (Pipeline Architecture)
- Thiết kế các Job logic độc lập và có thể chạy song song hoặc tuần tự:
  1. **Job 1: Lint & Code Style**: Chạy linter, format check (nhanh, tốn ít tài nguyên).
  2. **Job 2: Test Suite**: Chạy unit test và integration test trên ma trận môi trường cần hỗ trợ.
  3. **Job 3: Security Audit**: Quét lỗ hổng dependencies (`npm audit` / `trivy`).
  4. **Job 4: Build & Packaging**: Biên dịch artifact và kiểm tra tính toàn vẹn.

### Bước 3: Cấu Hình Cache Để Tối Ưu Tốc Độ CI (Caching Strategy)
- Cấu hình caching cho dependencies (như `~/.npm`, `~/.cache/pip`, Cargo registry) để giảm thời gian chạy pipeline từ vài chục phút xuống còn 1-2 phút.

### Bước 4: Thiết Lập Quản Lý Biến Môi Trường Bí Mật (Secrets Handling)
- Sử dụng cơ chế Secrets của hệ thống CI (ví dụ: `secrets.GITHUB_TOKEN`, `secrets.NPM_TOKEN`).
- Tuyệt đối không hardcode credentials trong file YAML workflow.

### Bước 5: Chạy Thử & Tinh Chỉnh Pipeline (Local Validation & Dry-run)
- Sử dụng công cụ chạy CI cục bộ nếu có (như `act` đối với GitHub Actions) hoặc tạo pull request nháp để kiểm tra pipeline hoạt động ổn định.

### Bước 6: Khóa Nhánh Bằng Branch Protection (Enforcement)
- Hướng dẫn thiết lập Branch Protection: Bắt buộc các status checks của CI phải chuyển sang màu xanh (`green`) trước khi nút `Merge Pull Request` được mở khóa.

## 7. Concrete Examples
```bash
# Lệnh thực thi & kiểm chứng tiêu chuẩn
dex verify --skill dex-cicd-automation
```

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước xác minh tự động và dựa vào giả định chủ quan.
- **Anti-Pattern 2**: Thay đổi diện rộng vượt ngoài phạm vi (Scope Creep) làm mất kiểm soát rủi ro.
- **Trap**: Thực hiện thao tác phá hủy hoặc thay đổi trạng thái sản xuất khi chưa qua cổng kiểm duyệt an toàn.

## 9. Quality Gates & Acceptance Criteria
- **QG-03 (Static Analysis Automated)**: Bước Lint/Typecheck trong CI đạt PASS.
- **QG-04 (Build Step Automated)**: Bước Build trong CI thành công và sinh đúng artifact.
- **QG-05 (Automated Test Pass)**: Bước Test trong CI đạt 100% PASS.
- **QG-07 (Security Scan Automated)**: Bước quét bảo mật tự động không phát hiện lỗ hổng nghiêm trọng.

## 10. Security & Safety Boundaries
- **Cấm Bỏ Qua Thất Bại (No `continue-on-error: true` Bừa Bãi)**: Không bao giờ gắn `continue-on-error` cho các bước Test hoặc Security Scan chỉ để pipeline trông có vẻ xanh.
- **Cách Ly Môi Trường Production**: Các bước deploy lên Production phải có phê duyệt thủ công (Manual Environment Approval Gate).
- **Ghim Phiên Bản Action (Pin Actions)**: Ghim phiên bản của các bên thứ ba trong file workflow (ví dụ `actions/checkout@v4`) để tránh bị tấn công chuỗi cung ứng (Supply Chain Attack).

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Kích hoạt thông qua terminal hoặc tiện ích mở rộng IDE tương thích (VS Code, Cursor, Windsurf).

## 12. Deliverables & Output Artifacts
1. File cấu hình workflow CI/CD chuẩn mực (ví dụ: `.github/workflows/ci.yml`).
2. Pipeline tự động kích hoạt trên các sự kiện `push` và `pull_request`.
3. Báo cáo trạng thái trực quan (Status badge) trên `README.md`.

## 13. Related & Complementary Skills
- `dex-master-orchestrator`: Điều phối trung tâm.

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Kỹ sư hoặc AI Agent kích hoạt **dex-cicd-automation** trong dự án.
1. Tiếp nhận ngữ cảnh đầu vào và kiểm tra điều kiện tiên quyết tại Mục 4.
2. Vận hành tuần tự các bước theo Quy trình tại Mục 6.
3. Kiểm chứng đầu ra đối chiếu với Tiêu chuẩn chấp thuận tại Mục 9.
4. Bàn giao đầy đủ hiện vật theo Mục 12 và cập nhật tài liệu liên quan.
