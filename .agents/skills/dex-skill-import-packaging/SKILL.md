---
name: dex-skill-import-packaging
description: Package, adapt, and import validated third-party skills into isolated integrations with schema normalization, dry-run capabilities, and automated rollback. Use when expanding the skill catalog through external adoption.
---

# dex-skill-import-packaging

## 1. Purpose & Scope
Đóng gói, chuyển đổi tương thích và nhập khẩu các kỹ năng bên thứ ba đã qua thẩm định an ninh vào phân vùng tích hợp cô lập (`integrations/`); chuẩn hóa cấu trúc siêu dữ liệu theo quy chuẩn DEX, hỗ trợ chế độ chạy thử nghiệm an toàn (`--dry-run`), tự động sao lưu và cung cấp khả năng hoàn trả trạng thái ban đầu (Automated Rollback) khi xảy ra sự cố.

## 2. When to Use
- Nhập một hoặc nhiều kỹ năng mới từ các kho lưu trữ thượng nguồn đã được phê duyệt an ninh.
- Chuyển đổi định dạng kỹ năng từ các chuẩn khác (ví dụ: Claude Prompts, AutoGPT skills) sang định dạng Agent Skills Specification chuẩn.
- Thử nghiệm việc nhập kỹ năng trên môi trường local trước khi cam kết vào Git.

## 3. When NOT to Use
- Tuyệt đối không nhập kỹ năng bên thứ ba trực tiếp vào thư mục bản địa `.agents/skills/` (phải đặt trong `integrations/<source>/` để đảm bảo phân vùng ranh giới rõ ràng).
- Không thực hiện thao tác nhập đè nếu chưa chạy chế độ `--dry-run` để kiểm tra các file sẽ bị ảnh hưởng.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Đường dẫn tới gói kỹ năng nguồn đã được kiểm duyệt.
- Thư mục đích trong phân vùng tích hợp (`integrations/aas`, `integrations/reverse-skill`, `integrations/rea`).
- Cờ cấu hình thực thi (`--dry-run`, `--rollback-dir`).
- **Điều kiện tiên quyết**:
- Kỹ năng đã vượt qua bài kiểm tra an ninh (Skill Security Screening) và bài kiểm tra bản quyền (License Provenance).

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Segregated Integration Namespace: Giữ nguyên vẹn tính nguyên bản của kỹ năng ngoại nhập trong thư mục cách ly, gắn tiền tố hoặc đường dẫn rõ ràng để tránh xung đột tên với 200 kỹ năng cốt lõi của DEX.
- Dry-Run Execution: Giả lập toàn bộ quá trình đọc, biến đổi, chuẩn hóa và kiểm tra đường dẫn mà không ghi bất kỳ byte nào xuống ổ đĩa, giúp kỹ sư xem trước danh sách thay đổi.
- Atomic Rollback: Trước khi ghi file mới, hệ thống tự động tạo một snapshot lưu trữ tạm thời; nếu có bất kỳ lỗi nào xảy ra giữa chừng, toàn bộ trạng thái cũ sẽ được phục hồi nguyên vẹn ngay lập tức.
- **Quy tắc quyết định kỹ thuật**:
- Mọi thao tác nhập kỹ năng bắt buộc phải tạo hoặc cập nhật bản ghi trong `data/imported_skills_manifest.json`.
- Nếu phát hiện trùng tên với một kỹ năng DEX đã tồn tại: đổi tên theo namespace (ví dụ: `aas-github-actions-specialist`).
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Tiến trình nhập bị ngắt giữa chừng do mất điện hoặc hết dung lượng đĩa, để lại các file rác nửa chừng trong thư mục tích hợp.

## 6. Step-by-Step Execution Workflow
1. Khởi chạy công cụ nhập với cờ `--dry-run` để kiểm tra danh sách file và tính hợp lệ.
2. Tạo bản sao lưu trạng thái hiện tại vào thư mục `.rollback_cache/`.
3. Sao chép và chuẩn hóa cấu trúc file `SKILL.md` theo chuẩn 14 đề mục nếu cần thiết.
4. Cập nhật bản kê khai kỹ năng ngoại nhập `imported_skills_manifest.json`.
5. Chạy trình kiểm tra tính hợp lệ `validate_skills.py` trên thư mục vừa nhập.
6. Nếu có bất kỳ lỗi nào: tự động kích hoạt rollback hoàn trả trạng thái cũ.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```python
# Công cụ nhập kỹ năng an toàn hỗ trợ dry-run và rollback
class SafeSkillImporter:
    def __init__(self, dry_run=True):
        self.dry_run = dry_run
        self.backup_files = {}

    def import_skill(self, src_path: str, dest_path: str):
        if not os.path.exists(src_path):
            raise FileNotFoundError(f"Source skill not found at {src_path}")
        
        print(f"[IMPORTER] Chuẩn bị nhập {src_path} -> {dest_path} (Dry-run: {self.dry_run})")
        if self.dry_run:
            return True
            
        # Tạo backup trước khi ghi đè
        if os.path.exists(dest_path):
            self.backup_files[dest_path] = read_file(dest_path)
            
        copy_and_normalize_skill(src_path, dest_path)
        return True

    def rollback(self):
        for path, original_content in self.backup_files.items():
            write_file(path, original_content)
        print("[ROLLBACK] Đã hoàn trả nguyên trạng các file trước khi nhập!")
```

### Lệnh xác minh & thực thi:
```bash
# Chạy thử nghiệm nhập kỹ năng ở chế độ dry-run
python scripts/import_skills.py --source /tmp/new-skill --target integrations/aas --dry-run
```

## 8. Anti-Patterns & Common Traps
- Ghi đè trực tiếp lên các file kỹ năng đang có mà không có cơ chế sao lưu phục hồi.
- Nhập kỹ năng mà không cập nhật bản kê khai nguồn gốc xuất xứ đi kèm.

## 9. Quality Gates & Acceptance Criteria
- Chế độ `--dry-run` hoạt động chính xác 100% không tạo ra bất kỳ file rác nào.
- Tính năng Rollback phục hồi nguyên vẹn 100% trạng thái ban đầu khi gặp sự cố thử nghiệm.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Thư mục nhập khẩu phải được gán quyền hạn chế, không cho phép quyền thực thi đối với các file dữ liệu thuần túy.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ thống An ninh & SkillOps**: Tương thích GitHub Actions, SARIF, CycloneDX/SPDX, Semgrep, OWASP ZAP.

## 12. Deliverables & Output Artifacts
- Kỹ năng được nhập chuẩn hóa trong thư mục `integrations/`.
- File kê khai nhập khẩu cập nhật `data/imported_skills_manifest.json`.

## 13. Related & Complementary Skills
dex-skill-security-screening, dex-skill-upstream-sync, dex-skill-discovery-indexer

## 14. Realistic Usage Example
### Tình huống thực tế:
Một kỹ sư cần nhập 2 kỹ năng chuyên môn từ repository Reverse-Skill vào dự án. Sử dụng `dex_skill_importer.py` với cờ `--dry-run`, kỹ sư phát hiện một kỹ năng có tên trùng với kỹ năng DEX bản địa. Nhờ tính năng chuẩn hóa namespace tự động, kỹ năng được đổi tên an toàn thành `reverse-skill-analyzer` và nhập vào `integrations/reverse-skill/` chỉ trong vài giây mà không gây bất kỳ xung đột nào.
