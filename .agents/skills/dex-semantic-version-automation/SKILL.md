---
name: dex-semantic-version-automation
description: Automate Semantic Versioning (SemVer 2.0.0), Conventional Commits parsing, automated changelog generation, release tagging, and package publication pipelines. Use when automating releases, version bumps, or maintaining changelogs.
---

# dex-semantic-version-automation

## 1. Purpose & Scope
Tự động hóa hoàn toàn quy trình gắn phiên bản theo chuẩn Ngữ nghĩa (Semantic Versioning 2.0.0: MAJOR.MINOR.PATCH); phân tích lịch sử commit theo quy chuẩn Conventional Commits, tự động sinh nhật ký thay đổi (CHANGELOG.md), tạo Git release tag và kích hoạt luồng xuất bản phần mềm không cần can thiệp thủ công.

## 2. When to Use
- Khi việc nâng số phiên bản và viết changelog được thực hiện thủ công dễ nhầm lẫn hoặc bị bỏ quên.
- Khi cần quyết định tự động xem đợt release tiếp theo là patch, minor hay major dựa trên các pull request đã merge.
- Khi quản lý việc phát hành đồng thời cho nhiều gói thư viện trong monorepo.

## 3. When NOT to Use
- Các dự án triển khai liên tục dạng Continuous Deployment (CD) theo mã băm commit (Commit SHA release) không quan tâm tới số phiên bản người dùng.

## 4. Prerequisites & Input Context
**Đầu vào cần thiết:**
- Lịch sử Git commits kể từ tag phát hành gần nhất.
- Cấu hình công cụ tự động hóa phiên bản (Release-please, Semantic-release, Changesets).
- File đích ghi nhận phiên bản (`package.json`, `Cargo.toml`, `pyproject.toml`, `VERSION`).

**Điều kiện tiên quyết:**
- Đội ngũ tuân thủ nghiêm ngặt quy ước commit (ví dụ: `fix:`, `feat:`, `feat!:`, `BREAKING CHANGE:`).

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**: Nắm vững cơ chế vận hành theo chuẩn Agent Skills, tuân thủ nghiêm ngặt tính xác định và ranh giới trách nhiệm.
- **Quy tắc quyết định kỹ thuật**:
- **Quyết Định Phiên Bản Do Máy Tính Đảm Nhận (No Manual Version Bumps)**: Lập trình viên không bao giờ tự sửa số phiên bản bằng tay trong `package.json`; máy móc tự quyết định từ commit history.
- **Tuân Thủ Tuyệt Đối SemVer 2.0.0**: Bất kỳ thay đổi nào làm gãy vỡ tương thích ngược (Breaking Change) bắt buộc phải tăng số MAJOR.
- **Mỗi Release Đều Phải Có Git Tag Tương Ứng**: Không xuất bản artifact mà không có Git Tag được tạo trên branch chính thức.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Thay đổi breaking change nhưng chỉ tăng số minor**: Do lập trình viên quên ghi chú breaking change trong commit -> Khắc phục: Bắt buộc dùng PR template có checkbox xác nhận tính tương thích ngược.
- **Release bot bị lặp vô tận (Infinite CI loop)**: Bot tạo commit release và commit đó lại kích hoạt tiếp CI release -> Khắc phục: Thêm cờ `[skip ci]` vào commit release hoặc cấu hình bot token được bỏ qua trong workflow triggers.

## 6. Step-by-Step Execution Workflow
1. Thực thi kiểm tra quy ước commit ngay tại pull request (Commitlint CI check).
2. Khi code được merge vào branch chính, công cụ tự động quét lịch sử commits kể từ lần release trước:
   - Có `fix:` -> Tăng số PATCH (`1.0.0` -> `1.0.1`).
   - Có `feat:` -> Tăng số MINOR (`1.0.0` -> `1.1.0`).
   - Có `BREAKING CHANGE:` hoặc dấu chấm than `feat!:` -> Tăng số MAJOR (`1.0.0` -> `2.0.0`).
3. Tự động sinh hoặc cập nhật nội dung file `CHANGELOG.md` với các phân mục: Features, Bug Fixes, Breaking Changes, Documentation.
4. Cập nhật số phiên bản vào các file cấu hình dự án.
5. Tự động tạo commit phát hành, tạo Git Tag có chữ ký số (Annotated Tag `vX.Y.Z`) và tạo GitHub Release kèm ghi chú.
6. Kích hoạt downstream workflow để build và xuất bản artifact lên kho lưu trữ (npm, PyPI, Crates.io, Docker Hub).

## 7. Concrete Examples
### Ví dụ triển khai chuẩn mực:
```json
// .releaserc.json
{
  "branches": ["main"],
  "plugins": [
    "@semantic-release/commit-analyzer",
    "@semantic-release/release-notes-generator",
    ["@semantic-release/changelog", { "changelogFile": "CHANGELOG.md" }],
    ["@semantic-release/npm", { "npmPublish": true }],
    ["@semantic-release/git", { "assets": ["package.json", "CHANGELOG.md"], "message": "chore(release): ${nextRelease.version} [skip ci]" }],
    "@semantic-release/github"
  ]
}
```

### Lệnh xác minh & thực thi:
- Kiểm tra tính hợp lệ của commit message: `npx commitlint --from=HEAD~1`
- Chạy thử nghiệm giả định release (Dry run): `npx semantic-release --dry-run`
- Kiểm tra tag vừa tạo: `git describe --tags --abbrev=0`

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước kiểm tra biên và giả định hệ thống luôn ở trạng thái lý tưởng.
- **Anti-Pattern 2**: Không ghi nhận nhật ký kiểm toán hoặc bỏ qua việc xử lý ngoại lệ lúc runtime.
- **Trap**: Bỏ qua các rào chắn an toàn hoặc cố tình chạy script không qua kiểm thử tự động.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Toàn bộ commit tuân thủ đúng chuẩn Conventional Commits.
- QG-10: File `CHANGELOG.md` được sinh tự động, phân loại rõ ràng và liên kết chính xác tới commit/PR tương ứng.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động trước khi coi là hoàn thành.

## 10. Security & Safety Boundaries
- Token phát hành (GitHub Token, NPM Token) phải được lưu trữ trong Repository Secrets với quyền hạn tối thiểu (Chỉ cấp quyền write contents & packages).
- Không bao giờ thực thi mã nguồn hoặc thay đổi cấu hình trên môi trường sản xuất mà thiếu cơ chế rollback an toàn.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Có thể kích hoạt trực tiếp từ terminal hoặc extension tương thích trong VS Code / Cursor / Windsurf.

## 12. Deliverables & Output Artifacts
- File nhật ký thay đổi cập nhật (`CHANGELOG.md`).
- Git Release Tag được gắn trên repository (`v3.0.0`).
- GitHub Release hoàn chỉnh với release notes chi tiết.

## 13. Related & Complementary Skills
- `dex-development-workflow`: Quy trình phát triển tiêu chuẩn.
- `dex-code-verification`: Xác minh chất lượng và tính đúng đắn của mã nguồn.
- `dex-master-orchestrator`: Bộ điều phối trung tâm kết nối kỹ năng này với các kỹ năng khác trong hệ thống.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư hoặc AI Agent tiếp nhận yêu cầu liên quan đến **dex-semantic-version-automation**.
1. Đọc kỹ đầu vào và các ràng buộc kỹ thuật tại mục 4.
2. Thực thi tuần tự 6 bước trong Workflow tại mục 6.
3. Chạy các lệnh kiểm chứng tại mục 7 và đối chiếu với Quality Gates tại mục 9.
4. Đóng gói deliverables theo danh sách tại mục 12 và báo cáo kết quả kèm bằng chứng xác thực.
