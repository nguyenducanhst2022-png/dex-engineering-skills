---
name: dex-repository-bootstrap
description: Scaffold production-grade software repositories from scratch with standardized directory layouts, linting, formatting, pre-commit hooks, CI templates, license, editorconfig, and reproducible dev environments. Use when initializing a new project or standardizing repo templates.
---

# dex-repository-bootstrap

## 1. Purpose & Scope
Khởi tạo và thiết lập nền tảng dự án phần mềm mới (Repository Bootstrap) đạt tiêu chuẩn kỹ thuật doanh nghiệp; thiết lập cấu trúc thư mục chuẩn, công cụ định dạng mã nguồn (formatters), linter, pre-commit hooks, cấu hình biên dịch, mẫu issue/PR và pipeline CI ban đầu; đảm bảo lập trình viên mới có thể sẵn sàng code (zero-to-code) trong vòng 5 phút.

## 2. When to Use
- Khi bắt đầu khởi tạo một dự án phần mềm mới từ con số 0 (Greenfield project).
- Khi chuẩn hóa một repository cũ đang thiếu các công cụ kiểm soát chất lượng cơ bản.
- Khi xây dựng repository template dùng chung cho toàn bộ kỹ sư trong công ty.

## 3. When NOT to Use
- Refactor mã nguồn bên trong một module hiện hữu (dùng `dex-technical-debt-refactoring`).
- Quản lý kiến trúc monorepo phức tạp nhiều package (dùng `dex-monorepo-governance`).

## 4. Prerequisites & Input Context
**Đầu vào cần thiết:**
- Tên dự án, ngôn ngữ lập trình chủ đạo, framework và runtime target (Node.js, Python, Rust, Go).
- Tiêu chuẩn license (MIT, Apache 2.0, Proprietary).
- Yêu cầu về môi trường phát triển (Docker, Devcontainer, ASDF, Mise).

**Điều kiện tiên quyết:**
- Đã khởi tạo Git repository (`git init`).
- Đã xác định rõ quy ước đặt tên và phân quyền người đóng góp.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**: Nắm vững cơ chế vận hành theo chuẩn Agent Skills, tuân thủ nghiêm ngặt tính xác định và ranh giới trách nhiệm.
- **Quy tắc quyết định kỹ thuật**:
- **Quy Chuẩn Một Lệnh Khởi Động**: Mọi repo phải có một lệnh duy nhất để thiết lập môi trường (ví dụ: `make setup` hoặc `pnpm install && pnpm setup`).
- **Zero Ignored Warnings**: Cấu hình linter không để warning lơ lửng, xử lý warning như error trong CI (`--max-warnings 0`).
- **Bảo Vệ Branch Main Ngay Từ Ngày Đầu**: Cấu hình branch protection yêu cầu CI pass và ít nhất 1 review trước khi merge.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Lập trình viên commit file rác hoặc .env lên Git**: Do thiếu `.gitignore` chuẩn -> Khắc phục: Khởi tạo tệp `.gitignore` chính thức từ gitignore.io và tích hợp git-secrets vào pre-commit.
- **Mỗi người một định dạng dấu cách/tab/dấu ngoặc**: Do thiếu `.editorconfig` và auto-formatter -> Khắc phục: Cấu hình Ruff/Prettier chạy tự động khi lưu file.

## 6. Step-by-Step Execution Workflow
1. Khởi tạo cấu trúc thư mục tiêu chuẩn (`src/`, `tests/`, `docs/`, `scripts/`, `.github/`).
2. Cấu hình tệp điều khiển trình soạn thảo (`.editorconfig`) và bỏ qua file thừa (`.gitignore`, `.dockerignore`).
3. Cài đặt và cấu hình công cụ linting & formatting tự động (Biome/ESLint/Prettier, Ruff, Rustfmt/Clippy, Golangci-lint).
4. Thiết lập Git hooks bảo vệ chất lượng commit bằng Lefthook hoặc Husky (chặn commit có lỗi lint hoặc secret).
5. Thiết lập file `README.md` chuẩn hóa với các lệnh: Build, Test, Run, Lint, Clean.
6. Cấu hình GitHub Actions CI tối thiểu: Kiểm tra lint và chạy smoke test trên pull request.
7. Cung cấp file cấu hình `devcontainer.json` để đồng bộ môi trường lập trình qua VS Code / Codespaces.

## 7. Concrete Examples
### Ví dụ triển khai chuẩn mực:
```json
// .devcontainer/devcontainer.json
{
  "name": "DEX Modern Node Project",
  "image": "mcr.microsoft.com/devcontainers/typescript-node:20",
  "customizations": {
    "vscode": {
      "settings": {
        "editor.defaultFormatter": "biomejs.biome",
        "editor.formatOnSave": true
      },
      "extensions": ["biomejs.biome", "eamodio.gitlens"]
    }
  },
  "postCreateCommand": "corepack enable && pnpm install"
}
```

### Lệnh xác minh & thực thi:
- Kiểm tra toàn bộ mã nguồn với linter: `npm run lint` hoặc `ruff check .`
- Chạy pre-commit trên toàn bộ repo: `npx lefthook run pre-commit --all-files`
- Kiểm tra khả năng build sạch: `npm run build` hoặc `cargo check`

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước kiểm tra biên và giả định hệ thống luôn ở trạng thái lý tưởng.
- **Anti-Pattern 2**: Không ghi nhận nhật ký kiểm toán hoặc bỏ qua việc xử lý ngoại lệ lúc runtime.
- **Trap**: Bỏ qua các rào chắn an toàn hoặc cố tình chạy script không qua kiểm thử tự động.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Có đầy đủ `.gitignore`, `.editorconfig`, `README.md`, `LICENSE`, và cấu hình CI.
- QG-03: Pre-commit hook chặn thành công các commit vi phạm định dạng hoặc chứa secret.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động trước khi coi là hoàn thành.

## 10. Security & Safety Boundaries
- Tự động quét và ngăn chặn commit secret nhạy cảm bằng Gitleaks hook.
- Khóa phiên bản dependency (lockfile: `pnpm-lock.yaml`, `poetry.lock`, `Cargo.lock`) phải được commit vào Git.
- Không bao giờ thực thi mã nguồn hoặc thay đổi cấu hình trên môi trường sản xuất mà thiếu cơ chế rollback an toàn.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Có thể kích hoạt trực tiếp từ terminal hoặc extension tương thích trong VS Code / Cursor / Windsurf.

## 12. Deliverables & Output Artifacts
- Cấu trúc repository sạch sẽ và hoàn chỉnh.
- Tệp cấu hình tooling (`.editorconfig`, `.gitignore`, `.github/workflows/ci.yml`).
- Hướng dẫn `README.md` rõ ràng với hướng dẫn đóng góp.

## 13. Related & Complementary Skills
- `dex-development-workflow`: Quy trình phát triển tiêu chuẩn.
- `dex-code-verification`: Xác minh chất lượng và tính đúng đắn của mã nguồn.
- `dex-master-orchestrator`: Bộ điều phối trung tâm kết nối kỹ năng này với các kỹ năng khác trong hệ thống.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư hoặc AI Agent tiếp nhận yêu cầu liên quan đến **dex-repository-bootstrap**.
1. Đọc kỹ đầu vào và các ràng buộc kỹ thuật tại mục 4.
2. Thực thi tuần tự 6 bước trong Workflow tại mục 6.
3. Chạy các lệnh kiểm chứng tại mục 7 và đối chiếu với Quality Gates tại mục 9.
4. Đóng gói deliverables theo danh sách tại mục 12 và báo cáo kết quả kèm bằng chứng xác thực.
