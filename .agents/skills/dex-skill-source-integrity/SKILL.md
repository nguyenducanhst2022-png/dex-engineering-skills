---
name: dex-skill-source-integrity
description: Verify cryptographic source integrity, Git commit tree hashes, upstream tracking, and license attributions for imported and native skills. Use when guarding skill repositories against unauthorized modifications or supply chain tampering.
---

# dex-skill-source-integrity

## 1. Purpose & Scope
Xác minh tính toàn vẹn nguồn gốc mật mã (Cryptographic Source Integrity) của các kỹ năng Agent; theo dõi mã băm cây cam kết Git (Git Tree Hashes), truy vết kho nguồn gốc thượng nguồn (Upstream Tracking) và chứng nhận giấy phép cho cả kỹ năng nội bộ và kỹ năng nhập từ bên ngoài; bảo vệ kho kỹ năng khỏi các sửa đổi trái phép hoặc chèn mã độc trong chuỗi cung ứng.

## 2. When to Use
- Khi nhập một kỹ năng mới từ kho mã nguồn mở bên ngoài vào hệ thống DEX Skills.
- Trước mỗi đợt phát hành phiên bản framework lớn để kiểm tra tính toàn vẹn của toàn bộ kho kỹ năng.
- Khi kiểm toán nguồn gốc xuất xứ của từng dòng mã trong bộ kỹ năng doanh nghiệp.

## 3. When NOT to Use
- Khi đang chỉnh sửa nháp nội dung kỹ năng trên máy trạm cá nhân.
- Khi kiểm tra hiệu năng định tuyến của Agent.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Kho Git của dự án, tệp kê khai nguồn thượng nguồn `manifests/upstream-sources.json`, công cụ tính mã băm Git tree (`git rev-parse`, `git hash-object`).
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; bảo vệ toàn vẹn tài sản kỹ nghệ và dữ liệu sản xuất.

## 5. Core Concepts & Taxonomy
- **Git Tree Hash Integrity:** Mã băm SHA-1/SHA-256 của toàn bộ cây thư mục kỹ năng chứng minh rằng không có bất kỳ tệp tin nào bên trong bị thêm, bớt hoặc chỉnh sửa dù chỉ 1 ký tự.
- **Segregated Upstream Quarantine:** Các kỹ năng nhập từ nguồn bên ngoài bắt buộc phải nằm trong thư mục cách ly `integrations/` và không bao giờ được tính lẫn vào danh mục native.
- **Upstream Commit Pinning:** Khóa cứng mã commit hash chính xác của kho thượng nguồn để ngăn chặn việc tự động kéo về các phiên bản mới chưa qua kiểm duyệt an ninh.

## 6. Step-by-Step Execution Workflow
1. Đọc danh mục các nguồn tích hợp từ `manifests/upstream-sources.json`.
2. Tính toán mã băm Git tree hash cho từng thư mục kỹ năng trong `.agents/skills/` và `integrations/`.
3. Đối chiếu mã băm tính được với sổ cái toàn vẹn đã lưu trữ.
4. Kiểm tra thông tin giấy phép bản quyền và liên kết nguồn gốc thượng nguồn.
5. Nếu phát hiện mã băm không khớp hoặc kỹ năng bị sửa đổi không qua PR, phát cảnh báo vi phạm tính toàn vẹn.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```python
# Verifying Skill Directory Git Tree Integrity
import subprocess
import json

def verify_skill_integrity(skill_dir_path: str, expected_tree_hash: str) -> bool:
    # Compute git tree hash for the directory
    res = subprocess.run(
        ["git", "rev-parse", f"HEAD:{skill_dir_path}"],
        capture_output=True, text=True, check=True
    )
    current_tree_hash = res.stdout.strip()
    return current_tree_hash == expected_tree_hash
```

## 8. Anti-Patterns & Common Traps
- Nhập kỹ năng từ GitHub bên ngoài bằng cách copy paste thủ công mà không lưu lại commit hash gốc và thông tin giấy phép.
- Trộn lẫn kỹ năng của bên thứ ba vào thư mục kỹ năng native của hệ thống.
- Tự động đồng bộ mã nguồn kỹ năng từ nhánh `main` của bên ngoài mà không qua khâu thẩm định an ninh tĩnh.

## 9. Quality Gates & Acceptance Criteria
- QG-01: 100% các kỹ năng tích hợp bên ngoài đều có mã commit hash và giấy phép được ghi nhận trong `manifests/upstream-sources.json`.
- QG-02: Toàn bộ kỹ năng bên thứ ba được cách ly tuyệt đối trong thư mục `integrations/`.
- QG-03: Mã băm cây Git tree hash của toàn bộ kỹ năng trùng khớp 100% với sổ cái kiểm định.

## 10. Security & Safety Boundaries
- Ngăn chặn các cuộc tấn công đầu độc kỹ năng AI (Skill Poisoning Attack) thông qua việc kiểm soát chặt chẽ tính toàn vẹn nguồn gốc.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Sổ cái toàn vẹn nguồn kỹ năng `manifests/upstream-sources.json`.
1. Kịch bản kiểm tra tính toàn vẹn tự động `verify_skill_integrity.py`.

## 13. Related & Complementary Skills
- [`dex-skill-license-provenance`](.agents/skills/dex-skill-license-provenance/SKILL.md)
- [`dex-skill-security-screening`](.agents/skills/dex-skill-security-screening/SKILL.md)
- [`dex-skill-provenance-ledger`](.agents/skills/dex-skill-provenance-ledger/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Kiểm toán an ninh chuỗi cung ứng kỹ năng. Kỹ sư kích hoạt `dex-skill-source-integrity`, quét toàn bộ kho kỹ năng, xác minh 5 kỹ năng bên thứ ba nằm đúng trong `integrations/` có đầy đủ commit hash đối chiếu với 4 repo thượng nguồn, khẳng định hệ thống không bị can thiệp trái phép.
