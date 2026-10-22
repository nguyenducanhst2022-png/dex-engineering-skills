---
name: dex-git-workflow
description: Professional Git version control and safe upgrade workflow. Manages branches, creates atomic commits with Conventional Commits standards, prevents destructive operations, and guarantees safe recovery checkpoints. Use when committing code, creating feature branches, merging pull requests, or preparing releases.
---

# DEX Git Workflow

## 1. Purpose
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

## 3. When Not to Use
- Khi mã nguồn đang trong trạng thái lỗi, dở dang, biên dịch thất bại (trừ khi cố ý tạo branch nháp để lưu tạm).
- Khi chưa được người dùng cho phép commit vào kho mã nguồn chính thức.

## 4. Inputs
- Trạng thái kho Git hiện tại (`git status`, `git branch`, `git log -n 5`).
- Danh sách file thay đổi đã qua kiểm chứng (Verified files).
- Thông điệp mô tả thay đổi theo chuẩn Conventional Commits.

## 5. Workflow

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

## 6. Quality Gates
- **QG-01 (Scope Bound)**: Commit chỉ chứa các file thuộc đúng phạm vi của nhiệm vụ.
- **QG-05 (Tests PASS Prior to Commit)**: Cấm commit khi test đang FAIL.
- **QG-08 (Diff Clean)**: Diff không chứa rác, secrets, comment thừa hoặc file nhạy cảm.

## 7. Safety Rules
- **Cấm Tuyệt Đối Lệnh Hủy Hoại (No Destructive Commands)**:
  - CẤM chạy `git push --force` hoặc `git push -f` lên các nhánh dùng chung (`main`, `master`, `develop`).
  - CẤM chạy `git reset --hard` khi chưa xác nhận người dùng đã sao lưu thay đổi.
  - CẤM xóa nhánh từ xa (`git push origin --delete <branch>`) mà không có sự cho phép rõ ràng.
- **Bảo Vệ Thay Đổi Chưa Lưu**: Luôn kiểm tra `git status` trước khi chuyển nhánh để tránh làm mất code của người dùng.

## 8. Expected Outputs
1. Lịch sử Git sạch sẽ, có ý nghĩa, dễ dàng truy vết và rollback.
2. Các nhánh tính năng độc lập, không làm ảnh hưởng nhánh chính.
3. Commit hash an toàn ghi nhận trạng thái hoàn thành.

## 9. Failure Handling
- Nếu commit nhầm: Sử dụng `git revert <commit-hash>` để tạo commit đảo ngược an toàn, thay vì dùng các lệnh xóa lịch sử nguy hiểm.
- Nếu gặp merge conflict: Tạo bản sao lưu dự phòng trước khi can thiệp giải quyết xung đột.

## 10. Completion Criteria
- Các thay đổi đã được commit an toàn với message chuẩn mực.
- Trạng thái git working tree sạch sẽ (`working tree clean`).
- Nhánh mã nguồn đã sẵn sàng để review hoặc phát hành.

---

## Real-world Example
```bash
# 1. Kiểm tra trạng thái và diff
git status
git diff src/services/auth.ts

# 2. Add chính xác file cần thiết
git add src/services/auth.ts tests/auth.test.ts

# 3. Tạo commit an toàn chuẩn Conventional Commits
git commit -m "fix(auth): prevent timing attack by using constant-time string comparison"

# 4. Kiểm tra lịch sử
git log -n 1 --oneline
```
