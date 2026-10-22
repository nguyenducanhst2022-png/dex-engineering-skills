---
name: dex-developer-tooling
description: Configure developer tooling, Devcontainers, Nix/Mise environments, Git hooks (Lefthook), editor integration (VS Code / Neovim), language server protocol (LSP), and debug configurations. Use when optimizing developer inner loop and local setup.
---

# dex-developer-tooling

## 1. Purpose & Scope
Xây dựng và tối ưu hóa hệ thống công cụ phát triển phần mềm (Developer Tooling & Inner Loop); cấu hình môi trường lập trình cô lập có thể tái tạo (Devcontainers, Mise, Nix), Git hooks tốc độ cao (Lefthook), cấu hình gỡ lỗi (Launch Debugger configurations) và cấu hình trình soạn thảo (VS Code Workspace Settings, LSP); rút ngắn thời gian phản hồi từ lúc gõ code đến lúc nhìn thấy kết quả.

## 2. When to Use
- Khi lập trình viên mới mất 3 ngày mới cài đặt xong môi trường và chạy thử được dự án.
- Khi xảy ra hiện tượng 'chạy được trên máy tôi nhưng lỗi trên máy bạn' (Works on my machine).
- Khi Git hooks quá chậm (>10 giây mỗi commit) khiến lập trình viên phải dùng cờ `--no-verify` để bỏ qua.

## 3. When NOT to Use
- Cấu hình hạ tầng triển khai trên Kubernetes production (dùng `dex-cicd-automation`).
- Tối ưu hóa hiệu năng runtime của ứng dụng người dùng cuối (dùng `dex-performance-optimization`).

## 4. Prerequisites & Input Context
**Đầu vào cần thiết:**
- Danh sách công cụ, SDKs và phiên bản runtime cần thiết (Node.js v20, Go 1.22, Python 3.12, Docker, Redis).
- Các tiện ích mở rộng khuyến nghị cho trình soạn thảo (VS Code Extensions).
- Các tác vụ cần tự động hóa khi commit hoặc push.

**Điều kiện tiên quyết:**
- Có quyền thiết lập các tệp cấu hình trong thư mục `.vscode/`, `.devcontainer/` hoặc root.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**: Nắm vững cơ chế vận hành theo chuẩn Agent Skills, tuân thủ nghiêm ngặt tính xác định và ranh giới trách nhiệm.
- **Quy tắc quyết định kỹ thuật**:
- **Commit Hook Không Được Quá 3 Giây**: Pre-commit hook chỉ chạy các tác vụ cực nhanh trên các file đang staged (Staged Files Only); các tác vụ kiểm thử toàn diện chuyển giao cho CI đảm nhận.
- **Cung Cấp Cấu Hình F5 Sẵn Sàng Gỡ Lỗi**: Lập trình viên phải có thể đặt breakpoint và ấn F5 để gỡ lỗi mã nguồn mà không cần gõ lệnh dòng lệnh phức tạp.
- **Khóa Chặt Phiên Bản Công Cụ**: Không dùng phiên bản thả nổi (như `node: latest`); bắt buộc dùng phiên bản cố định (`node: 20.12.2`).
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Lập trình viên dùng `--no-verify` để lách luật commit**: Do hook chạy toàn bộ test suite mất 2 phút -> Khắc phục: Chuyển sang Lefthook chỉ chạy linter trên các tệp staged bằng cờ `{staged_files}`.
- **Không thể debug ứng dụng trong container**: Do thiếu ánh xạ cổng debug -> Khắc phục: Mở cổng `9229` (Node) hoặc `5678` (Python) trong file devcontainer.

## 6. Step-by-Step Execution Workflow
1. Khai báo phiên bản runtime thống nhất bằng file `.tool-versions` hoặc `mise.toml`.
2. Xây dựng môi trường Devcontainer (`.devcontainer/devcontainer.json`) để người dùng có thể mở và lập trình tức thì trên GitHub Codespaces hoặc Docker cục bộ.
3. Thiết lập Git hooks siêu tốc bằng Lefthook (viết bằng Go, chạy song song) thay thế các hook Node.js cồng kềnh.
4. Cấu hình file `.vscode/launch.json` cung cấp sẵn các profile gỡ lỗi F5 (Debug Unit Tests, Debug Web Server, Attach to Process).
5. Thiết lập file `.vscode/extensions.json` gợi ý danh sách extension tối thiểu cần cài đặt.
6. Tự động hóa kiểm tra tính sẵn sàng của môi trường bằng script chẩn đoán (`doctor.sh` hoặc `pnpm doctor`).

## 7. Concrete Examples
### Ví dụ triển khai chuẩn mực:
```yaml
# lefthook.yml - Blazing fast parallel git hooks
pre-commit:
  parallel: true
  commands:
    lint:
      glob: "*.{js,ts,jsx,tsx}"
      run: npx biome check --apply {staged_files} && git add {staged_files}
    typecheck:
      run: pnpm typecheck
```

### Lệnh xác minh & thực thi:
- Chạy chẩn đoán môi trường: `mise doctor` hoặc `./scripts/doctor.sh`
- Thử nghiệm chạy Git hook: `npx lefthook run pre-commit`
- Kiểm tra cấu hình devcontainer: `devcontainer validate`

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước kiểm tra biên và giả định hệ thống luôn ở trạng thái lý tưởng.
- **Anti-Pattern 2**: Không ghi nhận nhật ký kiểm toán hoặc bỏ qua việc xử lý ngoại lệ lúc runtime.
- **Trap**: Bỏ qua các rào chắn an toàn hoặc cố tình chạy script không qua kiểm thử tự động.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Cung cấp đầy đủ cấu hình `.devcontainer`, `.vscode`, và git hooks.
- QG-08: Thời gian thực thi pre-commit hook hoàn thành dưới 3000ms.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động trước khi coi là hoàn thành.

## 10. Security & Safety Boundaries
- Tuyệt đối không mount các thư mục nhạy cảm của máy host (như `~/.ssh` hoặc `~/.aws`) vào bên trong devcontainer không tin cậy.
- Không bao giờ thực thi mã nguồn hoặc thay đổi cấu hình trên môi trường sản xuất mà thiếu cơ chế rollback an toàn.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Có thể kích hoạt trực tiếp từ terminal hoặc extension tương thích trong VS Code / Cursor / Windsurf.

## 12. Deliverables & Output Artifacts
- Cấu hình Devcontainer (`.devcontainer/devcontainer.json`).
- Cấu hình Lefthook (`lefthook.yml`).
- Cấu hình gỡ lỗi VS Code (`.vscode/launch.json`, `.vscode/settings.json`).

## 13. Related & Complementary Skills
- `dex-development-workflow`: Quy trình phát triển tiêu chuẩn.
- `dex-code-verification`: Xác minh chất lượng và tính đúng đắn của mã nguồn.
- `dex-master-orchestrator`: Bộ điều phối trung tâm kết nối kỹ năng này với các kỹ năng khác trong hệ thống.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư hoặc AI Agent tiếp nhận yêu cầu liên quan đến **dex-developer-tooling**.
1. Đọc kỹ đầu vào và các ràng buộc kỹ thuật tại mục 4.
2. Thực thi tuần tự 6 bước trong Workflow tại mục 6.
3. Chạy các lệnh kiểm chứng tại mục 7 và đối chiếu với Quality Gates tại mục 9.
4. Đóng gói deliverables theo danh sách tại mục 12 và báo cáo kết quả kèm bằng chứng xác thực.
