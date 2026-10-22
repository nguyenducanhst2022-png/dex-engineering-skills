---
name: dex-cross-platform-portability
description: Achieve cross-platform portability across Windows, Linux, and macOS, addressing POSIX vs Windows paths, line endings (CRLF vs LF), shell differences, file system case sensitivity, and environment variable handling. Use when ensuring applications run reliably across OS targets.
---

# dex-cross-platform-portability

## 1. Purpose & Scope
Đảm bảo tính tương thích và khả chuyển đa nền tảng (Cross-Platform Portability) tuyệt đối giữa Windows (PowerShell/CMD), Linux (POSIX Bash/Zsh) và macOS; triệt tiêu các lỗi ngầm liên quan đến ký tự phân tách đường dẫn (`/` vs `\`), định dạng kết thúc dòng (CRLF vs LF), phân biệt chữ hoa/thường trên hệ thống tệp (Case sensitivity), quyền thực thi file (`chmod +x`) và biến môi trường.

## 2. When to Use
- Khi mã nguồn chạy tốt trên máy tính của lập trình viên (macOS/Linux) nhưng gặp lỗi khi chạy trên Windows hoặc máy CI.
- Khi các script tự động hóa bị lỗi cú pháp do ký tự xuống dòng `\r\n` không tương thích.
- Khi ứng dụng cần đóng gói và phân phối cho cả 3 hệ điều hành lớn.

## 3. When NOT to Use
- Ứng dụng chỉ nhắm mục tiêu duy nhất vào một môi trường Linux container độc quyền và không có kế hoạch chạy ở nơi khác.

## 4. Prerequisites & Input Context
**Đầu vào cần thiết:**
- Danh sách các nền tảng mục tiêu (Windows 11, Ubuntu 22.04 LTS, macOS Sonoma).
- Các module xử lý I/O tệp, đường dẫn và gọi lệnh hệ thống (Subprocess / Shell calls).

**Điều kiện tiên quyết:**
- Có pipeline CI đa nền tảng (Matrix Build trên `windows-latest`, `ubuntu-latest`, `macos-latest`).

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**: Nắm vững cơ chế vận hành theo chuẩn Agent Skills, tuân thủ nghiêm ngặt tính xác định và ranh giới trách nhiệm.
- **Quy tắc quyết định kỹ thuật**:
- **Cấm Ghép Chuỗi Đường Dẫn Thủ Công (No String Concatenation for Paths)**: Mọi thao tác đường dẫn đều phải thông qua thư viện chuẩn hóa của ngôn ngữ.
- **Mặc Định Luôn Dùng LF**: Tất cả các tệp mã nguồn và script trong repository bắt buộc phải lưu ở định dạng LF.
- **Không Gọi Shell Khi Không Cần Thiết**: Ưu tiên gọi trực tiếp binary với mảng tham số (`execFile(['arg1', 'arg2'])`) thay vì kích hoạt shell (`exec('cmd string')`), giúp tránh các vấn đề escape ký tự giữa CMD, PowerShell và Bash.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Bash script báo lỗi `: not found` hoặc `^M: bad interpreter` trên Linux**: Do file script được lưu ở định dạng Windows CRLF -> Khắc phục: Chuyển sang LF qua `dos2unix` và cố định bằng `.gitattributes`.
- **Node import `import './Button'` chạy được trên macOS nhưng lỗi trên Linux**: Do tên file trên đĩa là `button.tsx` (Linux phân biệt hoa/thường, macOS mặc định không) -> Khắc phục: Đặt tên đồng nhất và dùng linter phát hiện case-sensitive imports.

## 6. Step-by-Step Execution Workflow
1. Chuẩn hóa ký tự kết thúc dòng bằng cấu hình `.gitattributes` (`* text=auto eol=lf`).
2. Thay thế toàn bộ việc ghép chuỗi đường dẫn thủ công (`folder + '/' + file`) bằng các hàm thư viện chuẩn (`path.join()`, `pathlib.Path`, `filepath.Join()`).
3. Tránh phụ thuộc vào các lệnh shell đặc thù của OS (như `rm -rf` hay `del /f`): Thay bằng các thư viện đa nền tảng (Node: `rimraf`/`shx`, Python: `shutil.rmtree`).
4. Xử lý phân biệt chữ hoa/thường: Đảm bảo tên file trong mã nguồn khớp chính xác 100% với tên file trên đĩa để không bị lỗi trên Linux.
5. Đọc biến môi trường an toàn: Không phân biệt chữ hoa thường khi xử lý trên Windows (`PATH` vs `Path`).
6. Kiểm tra quyền thực thi (Executable bit): Đảm bảo các shell script được commit với quyền thực thi `git update-index --chmod=+x script.sh`.
7. Chạy ma trận kiểm thử CI đồng thời trên cả 3 hệ điều hành trước khi merge mã nguồn.

## 7. Concrete Examples
### Ví dụ triển khai chuẩn mực:
```gitattributes
# .gitattributes - Enforce consistent line endings
* text=auto eol=lf
*.bat text eol=crlf
*.cmd text eol=crlf
*.ps1 text eol=crlf
*.sh text eol=lf
```

### Lệnh xác minh & thực thi:
- Kiểm tra định dạng line ending của repo: `git ls-files --stage` hoặc `file scripts/*.sh`
- Chạy ma trận kiểm thử CI đa nền tảng: `gh run list --workflow=ci.yml`
- Kiểm tra đường dẫn đa nền tảng trong Python: `python -c "import pathlib; print(pathlib.Path('a/b/c'))"`

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước kiểm tra biên và giả định hệ thống luôn ở trạng thái lý tưởng.
- **Anti-Pattern 2**: Không ghi nhận nhật ký kiểm toán hoặc bỏ qua việc xử lý ngoại lệ lúc runtime.
- **Trap**: Bỏ qua các rào chắn an toàn hoặc cố tình chạy script không qua kiểm thử tự động.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Tệp `.gitattributes` được thiết lập chuẩn xác ở thư mục gốc.
- QG-04: Toàn bộ bài kiểm tra trong Matrix CI pass trên cả Windows, Ubuntu và macOS.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động trước khi coi là hoàn thành.

## 10. Security & Safety Boundaries
- Kiểm tra đường dẫn chống lỗ hổng Path Traversal (`../../etc/passwd` hoặc `..\..\Windows\System32`) trên cả hai kiểu phân tách (`/` và `\`).
- Không bao giờ thực thi mã nguồn hoặc thay đổi cấu hình trên môi trường sản xuất mà thiếu cơ chế rollback an toàn.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Có thể kích hoạt trực tiếp từ terminal hoặc extension tương thích trong VS Code / Cursor / Windsurf.

## 12. Deliverables & Output Artifacts
- Tệp cấu hình `.gitattributes` chuẩn hóa.
- GitHub Actions matrix workflow (`matrix: os: [ubuntu-latest, windows-latest, macos-latest]`).
- Mã nguồn chuẩn hóa xử lý path bằng thư viện native.

## 13. Related & Complementary Skills
- `dex-development-workflow`: Quy trình phát triển tiêu chuẩn.
- `dex-code-verification`: Xác minh chất lượng và tính đúng đắn của mã nguồn.
- `dex-master-orchestrator`: Bộ điều phối trung tâm kết nối kỹ năng này với các kỹ năng khác trong hệ thống.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư hoặc AI Agent tiếp nhận yêu cầu liên quan đến **dex-cross-platform-portability**.
1. Đọc kỹ đầu vào và các ràng buộc kỹ thuật tại mục 4.
2. Thực thi tuần tự 6 bước trong Workflow tại mục 6.
3. Chạy các lệnh kiểm chứng tại mục 7 và đối chiếu với Quality Gates tại mục 9.
4. Đóng gói deliverables theo danh sách tại mục 12 và báo cáo kết quả kèm bằng chứng xác thực.
