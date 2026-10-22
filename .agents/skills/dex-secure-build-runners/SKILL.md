---
name: dex-secure-build-runners
description: Harden CI/CD execution environments and GitHub Actions runners, enforcing least-privilege tokens, ephemeral sandboxes, and protection against untrusted pull requests (pwn-request attacks). Use when securing build pipelines against supply-chain compromise.
---

# dex-secure-build-runners

## 1. Purpose & Scope
Gia cố, cô lập và bảo mật môi trường thực thi CI/CD (Secure Build Runners: GitHub Actions, GitLab CI, Self-hosted Runners); cưỡng chế nguyên tắc đặc quyền tối thiểu cho token phiên (`GITHUB_TOKEN`), bảo vệ quy trình chống lại các cuộc tấn công chiếm quyền qua Pull Request không tin cậy (Pwn-Request Attacks), sử dụng môi trường thực thi tạm thời (Ephemeral Runners) và ngăn chặn việc đánh cắp bí mật (Secrets Exfiltration).

## 2. When to Use
- Repository mã nguồn mở hoặc nội bộ tiếp nhận các Pull Request từ các cộng tác viên bên ngoài.
- Sử dụng Self-hosted Runners trong mạng nội bộ công ty (nguy cơ bị hacker chiếm runner để tấn công mạng văn phòng).
- Chuẩn bị đánh giá bảo mật chuỗi cung ứng phần mềm theo khung SLSA (Supply-chain Levels for Software Artifacts).

## 3. When NOT to Use
- Tuyệt đối không kích hoạt sự kiện `pull_request_target` kết hợp với việc checkout mã nguồn của PR chưa được kiểm duyệt (đây là lỗ hổng Pwn-Request kinh điển cho phép kẻ tấn công đọc toàn bộ secrets của repo).
- Không cấp quyền `permissions: write-all` cho các workflow CI thông thường.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Các file cấu hình workflow CI/CD (`.github/workflows/*.yml`).
- Danh sách các Secrets và Variables được nạp vào pipeline.
- Cấu hình hạ tầng runner (GitHub-hosted vs Self-hosted K8s ARC).
- **Điều kiện tiên quyết**:
- Có quyền quản trị cấu hình bảo mật của GitHub Repository hoặc Organization.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Pwn-Request Attack: Kẻ tấn công tạo PR sửa file test hoặc script để in toàn bộ biến môi trường chứa token ra ngoài. Nếu workflow chạy tự động với quyền đọc secrets, toàn bộ thông tin bảo mật của dự án sẽ bị đánh cắp.
- Ephemeral Runners: Mỗi job CI được chạy trên một máy ảo hoặc container hoàn toàn mới được sinh ra và xóa sạch ngay sau khi job kết thúc, loại bỏ nguy cơ mã độc bám rễ lâu dài trên máy chủ build.
- OIDC over Long-lived Credentials: Thay vì lưu trữ AWS Access Key cứng trong GitHub Secrets, sử dụng OpenID Connect (OIDC) để xin token ngắn hạn (15 phút) từ AWS, loại bỏ hoàn toàn nguy cơ lộ khóa dài hạn.
- **Quy tắc quyết định kỹ thuật**:
- Mọi workflow GitHub Actions bắt buộc phải khai báo khối `permissions` rõ ràng ở đầu file; mặc định đặt `permissions: read-all` hoặc chỉ cấp quyền tối thiểu cần thiết.
- Mọi commit của bên ngoài (First-time contributors) bắt buộc phải có sự phê duyệt thủ công của Maintainer mới được phép chạy CI.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Cấu hình workflow tự động deploy lên AWS khi có ai đó mở PR, kẻ tấn công fork repo, sửa code và gửi PR, chiếm đoạt toàn bộ hạ tầng đám mây của công ty.

## 6. Step-by-Step Execution Workflow
1. Rà soát toàn bộ các workflow trong `.github/workflows/` bằng công cụ `actionlint` và `step-security/harden-runner`.
2. Cấu hình quyền mặc định tối thiểu cho `GITHUB_TOKEN` trong cài đặt Repository.
3. Khóa các Actions bên thứ ba bằng Commit SHA đầy đủ (40 ký tự) thay vì dùng tag trôi nổi như `@v3`.
4. Chuyển đổi toàn bộ thông tin xác thực Cloud sang cơ chế OpenID Connect (OIDC).
5. Tích hợp giải pháp giám sát lưu lượng mạng ra ngoài (Egress Monitoring) của runner để chặn việc gửi trộm dữ liệu.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```yaml
# Workflow GitHub Actions an toàn đạt chuẩn SLSA
name: Secure CI Pipeline
on:
  pull_request:
    branches: [main]

# Khóa quyền tối thiểu cho GITHUB_TOKEN
permissions:
  contents: read
  pull-requests: write

jobs:
  build-and-test:
    runs-on: ubuntu-latest
    steps:
      # 1. Giám sát và chặn các kết nối mạng bất thường từ runner
      - name: Harden Runner Security
        uses: step-security/harden-runner@v2.7.0
        with:
          egress-policy: audit

      # 2. Pin Action bằng commit SHA đầy đủ để chống supply-chain attack
      - name: Checkout Code
        uses: actions/checkout@b4ffde65f46336ab88eb53be808477a3936bae11 # v4.1.1

      - name: Run Tests Safely
        run: |
          npm ci
          npm test
```

### Lệnh xác minh & thực thi:
```bash
# Phân tích cú pháp và tìm lỗi bảo mật trong GitHub Actions workflows
actionlint -color
```

## 8. Anti-Patterns & Common Traps
- Sử dụng tag trôi nổi như `uses: actions/checkout@v4` (nếu tài khoản tác giả bị hack, họ có thể đẩy mã độc vào tag v4).
- In trực tiếp nội dung issue hoặc PR title vào câu lệnh bash shell (`run: echo "${{ github.event.issue.title }}"`) gây lỗ hổng Command Injection.

## 9. Quality Gates & Acceptance Criteria
- 100% workflows có khai báo khối `permissions` hạn chế quyền hạn rõ ràng.
- 100% Actions bên thứ ba được khóa bằng commit SHA đầy đủ.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Tuyệt đối cấm chạy mã nguồn không tin cậy trên các self-hosted runners có kết nối trực tiếp vào mạng nội bộ công ty.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ thống An ninh & SkillOps**: Tương thích GitHub Actions, SARIF, CycloneDX/SPDX, Semgrep, OWASP ZAP.

## 12. Deliverables & Output Artifacts
- Tập hợp các file workflow GitHub Actions đã được gia cố an toàn.
- Báo cáo kiểm toán bảo mật CI/CD từ công cụ `actionlint` và Scorecards.

## 13. Related & Complementary Skills
dex-sbom-verification, dex-vulnerability-remediation, dex-security-logging-detection

## 14. Realistic Usage Example
### Tình huống thực tế:
Một dự án mã nguồn mở lớn bị kẻ xấu mở Pull Request chèn script gửi toàn bộ GitHub Secrets về một máy chủ ở nước ngoài. Nhờ workflow đã được gia cố với `permissions: contents: read`, không nạp secrets trong sự kiện PR và khóa chặn egress network qua Harden-Runner, nỗ lực đánh cắp token đã bị chặn đứng hoàn toàn và hệ thống tự động gắn cờ cảnh báo cho các maintainers.
