---
name: dex-secrets-management
description: Manage application secrets, zero-hardcoded credentials policy, secret rotation, HashiCorp Vault / AWS Secrets Manager integration, runtime secret injection, and pre-commit leak detection. Use when handling sensitive credentials, API keys, or certificates.
---

# dex-secrets-management

## 1. Purpose & Scope
Quản lý và bảo vệ bí mật hệ thống (Secrets Management); thực thi chính sách 'Không mật khẩu tĩnh trong mã nguồn' (Zero-Hardcoded Credentials), tự động hóa xoay vòng mật khẩu (Secret Rotation), tích hợp kho lưu trữ bí mật tập trung (HashiCorp Vault, AWS Secrets Manager, Doppler), tiêm bí mật vào ứng dụng lúc runtime (Runtime Secret Injection) và quét phát hiện lộ lọt bí mật trước khi commit.

## 2. When to Use
- Khi chuẩn bị đưa ứng dụng lên môi trường production và cần loại bỏ toàn bộ mật khẩu cứng khỏi tệp cấu hình.
- Khi phát hiện lập trình viên vô tình commit API Key của Stripe hoặc AWS Access Key lên GitHub.
- Khi chính sách bảo mật công ty yêu cầu mật khẩu kết nối database phải được đổi định kỳ 30 ngày một lần.

## 3. When NOT to Use
- Quản lý các cấu hình phi nhạy cảm như theme giao diện hoặc số cổng chạy app (dùng file `.env` thông thường).

## 4. Prerequisites & Input Context
**Đầu vào cần thiết:**
- Danh sách bí mật ứng dụng (Database Passwords, Third-party API Keys, JWT Secrets, TLS Certificates).
- Kho lưu trữ bí mật đích (HashiCorp Vault, AWS Secrets Manager, GCP Secret Manager).
- Phương thức tiêm bí mật (Kubernetes Secrets, Env Injection, Vault Agent Sidecar).

**Điều kiện tiên quyết:**
- Có quyền quản trị trên kho lưu trữ bí mật và hạ tầng triển khai.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**: Nắm vững cơ chế vận hành theo chuẩn Agent Skills, tuân thủ nghiêm ngặt tính xác định và ranh giới trách nhiệm.
- **Quy tắc quyết định kỹ thuật**:
- **Tuyệt Đối Không Commit File `.env` Chứa Secret Thực Tế**: File `.env.example` chỉ chứa tên biến và giá trị giữ chỗ giả định; file `.env` thực sự phải nằm trong `.gitignore`.
- **Không Lưu Secret Trong Container Image**: Cấm sử dụng lệnh `ENV SECRET=xyz` trong Dockerfile; bí mật chỉ được đưa vào lúc container khởi động.
- **Ghi Log Bí Mật Là Vi Phạm Nghiêm Trọng**: Toàn bộ logger phải có bộ lọc khử dữ liệu nhạy cảm (Sanitization filter: ẩn các trường `password`, `token`, `authorization`).
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Lập trình viên push nhầm AWS Key lên GitHub công khai bị hacker quét trong 60 giây**: Do không có pre-commit scan -> Khắc phục: Tích hợp Gitleaks vào git hook và kích hoạt GitHub Secret Scanning để tự động vô hiệu hóa key bị lộ.
- **Ứng dụng bị sập khi đổi mật khẩu database**: Do ứng dụng không hỗ trợ reload credential động -> Khắc phục: Sử dụng cơ chế xoay vòng 2 tài khoản xen kẽ (Dual-account rotation).

## 6. Step-by-Step Execution Workflow
1. Thực hiện quét toàn bộ lịch sử Git của dự án bằng Gitleaks hoặc Trufflehog để đảm bảo không còn bí mật lịch sử nào sót lại.
2. Thiết lập Pre-commit hook chặn đứng mọi nỗ lực commit tệp chứa khóa bí mật hoặc file `.env`.
3. Khởi tạo kho lưu trữ bí mật tập trung và phân loại theo môi trường: `development`, `staging`, `production`.
4. Cấu hình tiêm bí mật lúc khởi chạy (Runtime Injection): Sử dụng Vault Agent, Doppler, hoặc External Secrets Operator trên Kubernetes để nạp biến môi trường trực tiếp vào bộ nhớ của tiến trình.
5. Thiết lập quy trình Xoay vòng bí mật tự động (Automated Secret Rotation): Tự động tạo mật khẩu database mới, cập nhật vào Vault và thông báo cho ứng dụng làm mới kết nối mà không gây gián đoạn (Zero-Downtime Rotation).
6. Thiết lập cảnh báo khẩn cấp khi phát hiện bí mật bị rò rỉ trên internet (GitHub Secret Scanning integration).

## 7. Concrete Examples
### Ví dụ triển khai chuẩn mực:
```toml
# .gitleaks.toml - Custom rules for secret detection
[extend]
useDefault = true

[[rules]]
id = "dex-api-key"
description = "DEX Secret API Key"
regex = '''(?i)(dex_sec_[0-9a-zA-Z]{32})'''
secretGroup = 1
```

### Lệnh xác minh & thực thi:
- Quét tìm bí mật trong toàn bộ repo: `gitleaks detect --source . -v`
- Kiểm tra lấy bí mật từ Vault: `vault kv get secret/dex/production`
- Kiểm tra biến môi trường không bị ghi đè vào file build: `grep -rn 'AIza' dist/`

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước kiểm tra biên và giả định hệ thống luôn ở trạng thái lý tưởng.
- **Anti-Pattern 2**: Không ghi nhận nhật ký kiểm toán hoặc bỏ qua việc xử lý ngoại lệ lúc runtime.
- **Trap**: Bỏ qua các rào chắn an toàn hoặc cố tình chạy script không qua kiểm thử tự động.

## 9. Quality Gates & Acceptance Criteria
- QG-03: Gitleaks scan hoàn thành với 0 phát hiện rò rỉ bí mật (Leaks: 0).
- QG-09: 100% bí mật môi trường production được quản lý qua Secret Manager tập trung.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động trước khi coi là hoàn thành.

## 10. Security & Safety Boundaries
- Khóa truy cập vào Secret Manager phải được cấp quyền theo vai trò IAM ngắn hạn (OIDC / IAM Roles), không dùng Static Service Account Keys.
- Không bao giờ thực thi mã nguồn hoặc thay đổi cấu hình trên môi trường sản xuất mà thiếu cơ chế rollback an toàn.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Có thể kích hoạt trực tiếp từ terminal hoặc extension tương thích trong VS Code / Cursor / Windsurf.

## 12. Deliverables & Output Artifacts
- Tệp mẫu cấu hình bí mật an toàn (`.env.example`).
- Cấu hình Pre-commit Gitleaks hook (`.gitleaks.toml`).
- Kịch bản nạp bí mật từ Vault / AWS Secrets Manager vào runtime.

## 13. Related & Complementary Skills
- `dex-development-workflow`: Quy trình phát triển tiêu chuẩn.
- `dex-code-verification`: Xác minh chất lượng và tính đúng đắn của mã nguồn.
- `dex-master-orchestrator`: Bộ điều phối trung tâm kết nối kỹ năng này với các kỹ năng khác trong hệ thống.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư hoặc AI Agent tiếp nhận yêu cầu liên quan đến **dex-secrets-management**.
1. Đọc kỹ đầu vào và các ràng buộc kỹ thuật tại mục 4.
2. Thực thi tuần tự 6 bước trong Workflow tại mục 6.
3. Chạy các lệnh kiểm chứng tại mục 7 và đối chiếu với Quality Gates tại mục 9.
4. Đóng gói deliverables theo danh sách tại mục 12 và báo cáo kết quả kèm bằng chứng xác thực.
