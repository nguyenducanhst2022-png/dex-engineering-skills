# DEX Engineering Skills Pack v3.0 — Installation & Integration Guide

Hướng dẫn chi tiết cài đặt, cấu hình và sử dụng **DEX Engineering Skills Pack v3.0** (91 Agent Skills) trên các nền tảng: **Windows 11**, **OpenAI Codex**, **VS Code**, **Cursor**, **Windsurf**, **Claude Code**, và **GitHub Actions CI**.

---

## 1. Yêu Cầu Môi Trường (Prerequisites)

- **Hệ điều hành**: Windows 11 / Windows 10 (hỗ trợ đầy đủ PowerShell 7+), Ubuntu 20.04+, macOS Sonoma+.
- **Git**: Phiên bản 2.38 trở lên.
- **Python**: Phiên bản 3.10 trở lên (khuyến nghị 3.12).
- **Test Runner**: `pytest` (`pip install pytest`).

---

## 2. Cài Đặt Vào Dự Án Mới (Installation)

### Cách 1: Tích hợp trực tiếp (Khuyến nghị cho dự án độc lập)
Sao chép thư mục `.agents/skills` vào thư mục gốc của repository dự án của bạn:
```bash
# Từ thư mục dự án của bạn:
git clone https://github.com/nguyenducanhst2022-png/dex-engineering-skills.git temp-dex
cp -r temp-dex/.agents ./
rm -rf temp-dex
```

### Cách 2: Sử dụng Git Submodule (Khuyến nghị cho cập nhật định kỳ)
```bash
git submodule add https://github.com/nguyenducanhst2022-png/dex-engineering-skills.git .agents/dex-skills
```

---

## 3. Cấu Hình Cho OpenAI Codex & AI Coding Agents

Tạo hoặc cập nhật tệp `AGENTS.md` tại thư mục gốc của dự án:
```markdown
# AGENTS.md - DEX Skills Instructions

Bạn có quyền truy cập vào bộ kỹ năng **DEX Engineering Skills Pack v3.0** đặt tại `.agents/skills/`.

### Quy tắc làm việc bắt buộc:
1. Luôn bắt đầu mọi tác vụ bằng cách kích hoạt `dex-master-orchestrator`.
2. Phân loại độ phức tạp của yêu cầu thành một trong ba chế độ:
   - **QUICK MODE**: Lỗi nhỏ, sửa chính tả, cấu hình tối thiểu -> Chỉ dùng `dex-development-workflow` + `dex-code-verification`.
   - **STANDARD MODE**: Thêm tính năng, API, refactoring -> Kích hoạt 3-5 skills chuyên biệt trên branch riêng.
   - **STRICT MODE**: Đụng chạm Database, Auth, Payment, hoặc Release -> Thực thi toàn diện kèm threat model và rollback plan.
3. Tuyệt đối không báo cáo hoàn thành nếu chưa chạy lệnh kiểm chứng thật trong terminal (QG-04).
4. Không thực hiện các lệnh phá hủy (`rm -rf`, `DROP TABLE`, `git push --force`).
```

---

## 4. Tích Hợp Vào IDE (VS Code, Cursor, Windsurf)

Thư mục `.agents/skills/` tuân thủ chuẩn mở Agent Skills. Các IDE hỗ trợ chuẩn này sẽ tự động nhận diện toàn bộ 91 kỹ năng thông qua file `SKILL.md` và trường YAML frontmatter `description`.

Để gán lệnh tắt nhanh trong VS Code, bạn có thể thêm vào `.vscode/tasks.json`:
```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "DEX: Validate All Skills",
      "type": "shell",
      "command": "python scripts/validate_skills.py",
      "group": "test"
    },
    {
      "label": "DEX: Run Pytest Suite",
      "type": "shell",
      "command": "pytest tests/ -v",
      "group": "test"
    }
  ]
}
```

---

## 5. Kiểm Tra & Xác Nhận Cài Đặt (Verification)

Chạy 2 lệnh kiểm thử sau để đảm bảo 100% các kỹ năng hợp lệ:
```bash
# 1. Kiểm tra cấu trúc 14 mục và cú pháp frontmatter
python scripts/validate_skills.py

# 2. Chạy bộ kiểm thử tự động (103 bài test)
pytest tests/ -v
```

Kết quả mong đợi: `103 passed in ~0.1s`.
