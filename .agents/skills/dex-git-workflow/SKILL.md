---
name: dex-git-workflow
description: Professional Git version control and safe upgrade workflow. Manages branches, creates atomic commits with Conventional Commits standards, prevents destructive operations, and guarantees safe recovery checkpoints. Use when committing code, creating feature branches, merging pull requests, or preparing releases.
---

# DEX Git Workflow

## 1. Purpose & Scope
Quản lý phiên bản mã nguồn an toàn, tạo điểm khôi phục dự phòng và bảo vệ tính toàn vẹn của nhánh chính trong quá trình phát triển bằng AI.

Quy trình Git chuẩn:
`Code ổn định → Test PASS → Git Commit → Tạo Branch → Nâng cấp → Test lại → Merge`

Nguyên tắc cốt lõi: **Luôn lưu phiên bản ổn định trước khi nâng cấp để có thể khôi phục khi gặp sự cố.**
Ghi nhớ sống còn: **Git Commit = Điểm lưu an toàn. Git Branch = Khu vực thử nghiệm.**

## 2. When to Use
- Sau khi hoàn thành một bước làm việc ổn định và test đạt PASS.
- Trước khi bắt đầu một tính năng mới hoặc một thử nghiệm rủi ro lớn (tạo branch mới).
- Khi chuẩn bị hợp nhất (merge) code từ branch thử nghiệm vào branch chính (`main`/`develop`).
- Khi cần phục hồi lại mã nguồn về trạng thái an toàn trước đó.

## 3. When NOT to Use
- Khi mã nguồn đang trong trạng thái lỗi, dở dang, biên dịch thất bại (trừ khi cố ý tạo branch nháp để lưu tạm).
- Khi chưa được người dùng cho phép commit vào kho mã nguồn chính thức.

## 4. Prerequisites & Input Context
- Trạng thái kho Git hiện tại (`git status`, `git branch`, `git log -n 5`).
- Danh sách file thay đổi đã qua kiểm chứng (Verified files).
- Thông điệp mô tả thay đổi theo chuẩn Conventional Commits.

## 5. Core Concepts & Taxonomy
- **Nguyên tắc cốt lõi**: Tuân thủ triệt để nguyên lý vận hành xác định và ranh giới trách nhiệm của chuẩn Agent Skills.
- **Tính nhất quán hệ thống**: Mọi thao tác phải có thể kiểm chứng độc lập với kết quả đo lường rõ ràng.
- **Ngăn ngừa hồi quy**: Bất kỳ sửa đổi nào cũng phải bảo vệ tính tương thích ngược và chất lượng đã được nghiệm thu.

## 6. Step-by-Step Execution Workflow
### Bước 1: Xác Nhận Mã Ổn Định (State Verification)
- Chạy `git status` để xem tất cả các file đã thay đổi và file chưa theo dõi (`untracked`).
- Xác nhận các bài kiểm tra liên quan đã đạt PASS trước khi commit.

### Bước 2: Tạo Nhánh Thử Nghiệm Cho Việc Mới (Branch Isolation)
- Khi bắt đầu một tính năng hoặc bugfix mới, luôn tạo nhánh riêng:
  ```bash
  git checkout -b feature/ten-tinh-nang
  # hoặc: git checkout -b fix/ten-loi
  ```
- Không bao giờ code trực tiếp trên nhánh `main` khi chưa có sự đồng ý.

### Bước 3: Soát Git Diff Từng Dòng (Diff Inspection)
- Chạy `git diff` để kiểm tra từng dòng thay đổi.
- Đảm bảo không commit nhầm file môi trường (`.env`), file tạm (`.DS_Store`, `node_modules`), secrets hoặc debug print (`console.log`, `print`).

### Bước 4: Tạo Atomic Commit Có Ý Nghĩa (Clean Commit)
- Gom các file liên quan bằng `git add <files>`.
- Viết commit message theo chuẩn Conventional Commits:
  - `feat: ...` (Thêm tính năng mới)
  - `fix: ...` (Sửa lỗi)
  - `refactor: ...` (Tái cấu trúc mã nguồn)
  - `test: ...` (Thêm hoặc sửa bài kiểm tra)
  - `docs: ...` (Cập nhật tài liệu)

### Bước 5: Kiểm Thử Lại Sau Thay Đổi (Re-test)
- Chạy lại test suite để đảm bảo mã nguồn trên nhánh mới vẫn hoạt động chính xác.

### Bước 6: Hợp Nhất An Toàn (Safe Merge)
- Chuyển về nhánh đích và cập nhật mã mới nhất.
- Hợp nhất nhánh tính năng vào nhánh chính (ưa chuộng `--no-ff` hoặc Pull Request review).
- Nếu phát sinh xung đột (conflict): Dừng lại, giải quyết xung đột thủ công, chạy lại test và mới hoàn tất merge.

## 7. Concrete Examples
```bash
# Lệnh thực thi & kiểm chứng tiêu chuẩn
dex verify --skill dex-git-workflow
```

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước xác minh tự động và dựa vào giả định chủ quan.
- **Anti-Pattern 2**: Thay đổi diện rộng vượt ngoài phạm vi (Scope Creep) làm mất kiểm soát rủi ro.
- **Trap**: Thực hiện thao tác phá hủy hoặc thay đổi trạng thái sản xuất khi chưa qua cổng kiểm duyệt an toàn.

## 9. Quality Gates & Acceptance Criteria
- **QG-01 (Scope Bound)**: Commit chỉ chứa các file thuộc đúng phạm vi của nhiệm vụ.
- **QG-05 (Tests PASS Prior to Commit)**: Cấm commit khi test đang FAIL.
- **QG-08 (Diff Clean)**: Diff không chứa rác, secrets, comment thừa hoặc file nhạy cảm.

## 10. Security & Safety Boundaries
- **Cấm Tuyệt Đối Lệnh Hủy Hoại (No Destructive Commands)**:
  - CẤM chạy `git push --force` hoặc `git push -f` lên các nhánh dùng chung (`main`, `master`, `develop`).
  - CẤM chạy `git reset --hard` khi chưa xác nhận người dùng đã sao lưu thay đổi.
  - CẤM xóa nhánh từ xa (`git push origin --delete <branch>`) mà không có sự cho phép rõ ràng.
- **Bảo Vệ Thay Đổi Chưa Lưu**: Luôn kiểm tra `git status` trước khi chuyển nhánh để tránh làm mất code của người dùng.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Kích hoạt thông qua terminal hoặc tiện ích mở rộng IDE tương thích (VS Code, Cursor, Windsurf).

## 12. Deliverables & Output Artifacts
1. Lịch sử Git sạch sẽ, có ý nghĩa, dễ dàng truy vết và rollback.
2. Các nhánh tính năng độc lập, không làm ảnh hưởng nhánh chính.
3. Commit hash an toàn ghi nhận trạng thái hoàn thành.

## 13. Related & Complementary Skills
- `dex-master-orchestrator`: Điều phối trung tâm.

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Kỹ sư hoặc AI Agent kích hoạt **dex-git-workflow** trong dự án.
1. Tiếp nhận ngữ cảnh đầu vào và kiểm tra điều kiện tiên quyết tại Mục 4.
2. Vận hành tuần tự các bước theo Quy trình tại Mục 6.
3. Kiểm chứng đầu ra đối chiếu với Tiêu chuẩn chấp thuận tại Mục 9.
4. Bàn giao đầy đủ hiện vật theo Mục 12 và cập nhật tài liệu liên quan.
