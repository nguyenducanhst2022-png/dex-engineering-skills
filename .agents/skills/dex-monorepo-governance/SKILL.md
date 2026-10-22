---
name: dex-monorepo-governance
description: Govern monorepo architectures, workspace dependencies, isolated package boundaries, task caching pipelines (Nx/Turborepo), affected graph builds, and cross-package versioning. Use when structuring, managing, or optimizing multi-package monorepos.
---

# dex-monorepo-governance

## 1. Purpose & Scope
Quản trị kiến trúc kho mã nguồn tập trung (Monorepo Governance) với quy mô hàng chục đến hàng trăm gói phần mềm (Packages/Apps); thiết lập ranh giới module rõ ràng, tối ưu hóa thời gian build thông qua đồ thị phụ thuộc (Dependency Graph) và cơ chế bộ nhớ đệm tác vụ phân tán (Turborepo / Nx / Bazel Remote Caching).

## 2. When to Use
- Khi dự án mở rộng thành nhiều ứng dụng (Web, Mobile, Admin, Docs) dùng chung thư viện core/UI.
- Khi thời gian chạy CI quá lâu (>30 phút) do phải build và test lại toàn bộ repo cho một thay đổi nhỏ.
- Khi các package phụ thuộc lẫn nhau một cách lộn xộn (Circular dependencies, Spaghetti imports).

## 3. When NOT to Use
- Dự án đơn lẻ (Single repository) chỉ có 1 artifact duy nhất (dùng `dex-repository-bootstrap`).
- Tách repo thành các kho mã nguồn độc lập (Multi-repo).

## 4. Prerequisites & Input Context
**Đầu vào cần thiết:**
- Danh sách các ứng dụng (`apps/`) và thư viện dùng chung (`packages/`).
- Công cụ quản lý monorepo (Turborepo, Nx, pnpm workspaces, Lerna).
- Cơ sở hạ tầng lưu trữ cache phân tán (Remote Cache S3, Vercel Remote Cache).

**Điều kiện tiên quyết:**
- Sử dụng package manager hỗ trợ workspaces (pnpm, yarn modern, cargo workspaces).
- Các package độc lập có file mô tả dependency riêng biệt (`package.json`, `Cargo.toml`).

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**: Nắm vững cơ chế vận hành theo chuẩn Agent Skills, tuân thủ nghiêm ngặt tính xác định và ranh giới trách nhiệm.
- **Quy tắc quyết định kỹ thuật**:
- **Strict Boundary Enforcement**: Cấm tuyệt đối import file tương đối xuyên package (ví dụ: `import '../../packages/ui/src/button'`); bắt buộc phải import qua tên package đã khai báo trong workspace (`@scope/ui`).
- **No Undeclared Dependencies (Phantom Dependencies)**: Mọi thư viện sử dụng trong package đều phải được khai báo tường minh trong `package.json` của chính nó.
- **Không Chạy Lại Tác Vụ Không Đổi**: Nếu hash đầu vào của package và các dependency không đổi, CI phải lấy kết quả từ Cache (Cache Hit: 100%).
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Vòng lặp phụ thuộc (Circular Dependency) giữa package A và B**: Gây lỗi khi bundle -> Khắc phục: Dùng eslint-plugin-import hoặc `turbo graph` để phát hiện và chặn commit vòng lặp.
- **Cache Poisoning (Cache chứa artifact lỗi)**: Do khai báo `outputs` hoặc `inputs` trong turbo.json thiếu sót -> Khắc phục: Khai báo tường minh tất cả biến môi trường ảnh hưởng tới build vào `dependsOn` (ví dụ: `"$ENV_VAR"`).

## 6. Step-by-Step Execution Workflow
1. Khởi tạo workspace root và định nghĩa cấu trúc phân loại: `apps/*` (entrypoints) và `packages/*` (shared libraries: ui, utils, config, types).
2. Thiết lập quy tắc ranh giới gói (Package Boundary Rules): Ngăn chặn package tầng dưới phụ thuộc ngược vào package tầng trên.
3. Cấu hình pipeline thực thi đồ thị phụ thuộc (Turborepo `turbo.json` hoặc Nx `nx.json`) với input/output hashes.
4. Kích hoạt cơ chế phát hiện thay đổi (Affected Calculation): Chỉ build, lint và test các gói bị ảnh hưởng bởi commit hiện tại.
5. Cấu hình bộ nhớ đệm từ xa (Remote Caching) để tái sử dụng artifact giữa các thành viên và máy CI.
6. Tự động hóa phát hành phiên bản và changelog đồng bộ bằng Changesets.

## 7. Concrete Examples
### Ví dụ triển khai chuẩn mực:
```json
// turbo.json
{
  "$schema": "https://turbo.build/schema.json",
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["dist/**", ".next/**", "!.next/cache/**"]
    },
    "test": {
      "dependsOn": ["build"],
      "inputs": ["src/**/*.tsx", "src/**/*.ts", "tests/**/*.ts"]
    }
  }
}
```

### Lệnh xác minh & thực thi:
- Trực quan hóa đồ thị phụ thuộc monorepo: `npx turbo graph graph.png` hoặc `nx graph`
- Chạy kiểm tra các package bị thay đổi: `npx turbo run test --filter=...[origin/main]`
- Kiểm tra tính hợp lệ của cấu trúc workspace: `pnpm check` hoặc `npx syncpack list-mismatches`

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước kiểm tra biên và giả định hệ thống luôn ở trạng thái lý tưởng.
- **Anti-Pattern 2**: Không ghi nhận nhật ký kiểm toán hoặc bỏ qua việc xử lý ngoại lệ lúc runtime.
- **Trap**: Bỏ qua các rào chắn an toàn hoặc cố tình chạy script không qua kiểm thử tự động.

## 9. Quality Gates & Acceptance Criteria
- QG-04: Đồ thị phụ thuộc không chứa bất kỳ chu trình khép kín (A -> B -> A) nào.
- QG-08: Tỷ lệ Cache Hit trong CI đạt tối thiểu 70% đối với các PR thay đổi nhỏ.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động trước khi coi là hoàn thành.

## 10. Security & Safety Boundaries
- Không lưu token bí mật trong cấu hình remote cache public.
- Đảm bảo các package nội bộ (private packages) không bị sơ ý xuất bản (publish) lên npm registry công cộng bằng cách gắn cờ `"private": true`.
- Không bao giờ thực thi mã nguồn hoặc thay đổi cấu hình trên môi trường sản xuất mà thiếu cơ chế rollback an toàn.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Có thể kích hoạt trực tiếp từ terminal hoặc extension tương thích trong VS Code / Cursor / Windsurf.

## 12. Deliverables & Output Artifacts
- File cấu hình monorepo (`pnpm-workspace.yaml`, `turbo.json`).
- Cấu hình Changesets (`.changeset/config.json`).
- Báo cáo đồ thị phụ thuộc không có lỗi.

## 13. Related & Complementary Skills
- `dex-development-workflow`: Quy trình phát triển tiêu chuẩn.
- `dex-code-verification`: Xác minh chất lượng và tính đúng đắn của mã nguồn.
- `dex-master-orchestrator`: Bộ điều phối trung tâm kết nối kỹ năng này với các kỹ năng khác trong hệ thống.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư hoặc AI Agent tiếp nhận yêu cầu liên quan đến **dex-monorepo-governance**.
1. Đọc kỹ đầu vào và các ràng buộc kỹ thuật tại mục 4.
2. Thực thi tuần tự 6 bước trong Workflow tại mục 6.
3. Chạy các lệnh kiểm chứng tại mục 7 và đối chiếu với Quality Gates tại mục 9.
4. Đóng gói deliverables theo danh sách tại mục 12 và báo cáo kết quả kèm bằng chứng xác thực.
