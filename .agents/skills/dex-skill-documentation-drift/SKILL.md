---
name: dex-skill-documentation-drift
description: Detect, quantify, and reconcile documentation drift between executable CLI scripts, manifest registries, and markdown specification files across the skill framework. Use when preventing out-of-sync documentation, stale examples, or unversioned skill modifications.
---

# dex-skill-documentation-drift

## 1. Purpose & Scope
Phát hiện, định lượng và đồng nhất hóa hiện tượng trôi lệch tài liệu (Documentation Drift); rà soát sự bất đồng bộ giữa các kịch bản thực thi CLI, sổ cái bản kê manifest và các tệp đặc tả Markdown `SKILL.md` trong toàn bộ hệ thống; loại bỏ các ví dụ code lỗi thời, các tham số dòng lệnh không còn hỗ trợ và các thay đổi kỹ năng chưa được ghi chép.

## 2. When to Use
- Sau khi sửa đổi mã nguồn của một script công cụ trong `scripts/` và cần kiểm tra xem các tài liệu `SKILL.md` liên quan đã được cập nhật tương ứng hay chưa.
- Khi kiểm tra xem các số liệu thống kê trong `README.md` có khớp chính xác với số lượng kỹ năng thực tế trên đĩa hay không.
- Trước mỗi đợt nghiệm thu phát hành phiên bản mới của DEX Skills Framework.

## 3. When NOT to Use
- Khi chỉnh sửa các tài liệu ghi chú cá nhân tạm thời.
- Khi kiểm thử hiệu năng tốc độ xử lý của thuật toán.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Mã nguồn các script trong `scripts/`, danh mục `manifests/dex-skills.json`, toàn bộ các tệp tài liệu `README.md`, `SKILLS_INDEX.md`, `SKILL.md`.
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; bảo vệ toàn vẹn tài sản kỹ nghệ và dữ liệu sản xuất.

## 5. Core Concepts & Taxonomy
- **Drift Detection Automation:** So sánh tự động giữa danh sách cờ tham số của script Python (`argparse`) với phần hướng dẫn sử dụng trong tài liệu Markdown.
- **Metric Parity in Documentation:** Đảm bảo các con số (như '300 skills', '30 groups', '659 tests') phải đồng nhất tuyệt đối trên mọi trang tài liệu.
- **Executable Documentation as Tests:** Kiểm tra xem các khối mã ví dụ trong tài liệu có thực sự chạy được không (Doctest / Markdown Code Testing).

## 6. Step-by-Step Execution Workflow
1. Đếm số lượng thư mục kỹ năng thực tế trong `.agents/skills/` và các tệp trong `integrations/`.
2. Đối chiếu số lượng với các con số ghi trong `README.md`, `SKILLS_INDEX.md` và `ROUTING_MATRIX.md`.
3. Kiểm tra xem các lệnh gọi script (ví dụ `python scripts/discover_skills.py`) trong các file `SKILL.md` có sử dụng đúng tên cờ tham số hiện tại hay không.
4. Liệt kê danh sách các điểm trôi lệch tài liệu phát hiện được.
5. Tự động chạy script tái tạo tài liệu để đồng bộ lại toàn bộ hệ thống.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```python
# Documentation Drift Detector Script
import os
import re

def detect_documentation_drift(root_dir: str):
    skills_dir = os.path.join(root_dir, ".agents", "skills")
    actual_skills_count = len([d for d in os.listdir(skills_dir) if os.path.isdir(os.path.join(skills_dir, d))])

    readme_path = os.path.join(root_dir, "README.md")
    with open(readme_path, "r", encoding="utf-8") as f:
        readme_content = f.read()

    # Find reported skill count in README
    match = re.search(r'(\d+)\s+Native DEX Skills', readme_content)
    reported_count = int(match.group(1)) if match else None

    drifts = []
    if reported_count != actual_skills_count:
        drifts.append(f"README.md reports {reported_count} skills, but disk contains {actual_skills_count} skills!")

    return drifts
```

## 8. Anti-Patterns & Common Traps
- Sửa đổi chức năng hoặc tham số của script nhưng không cập nhật tài liệu hướng dẫn, khiến người dùng chạy lệnh theo tài liệu bị báo lỗi.
- Cập nhật số lượng kỹ năng trong `README.md` nhưng quên cập nhật trong `SKILLS_INDEX.md` và `ARCHITECTURE.md`.
- Để các đoạn code mẫu trong tài liệu sử dụng các hàm đã bị xóa bỏ từ phiên bản trước.

## 9. Quality Gates & Acceptance Criteria
- QG-01: 100% các số liệu thống kê kỹ năng và nhóm đồng nhất tuyệt đối trên toàn bộ các tệp tài liệu.
- QG-02: Tất cả các câu lệnh mẫu trong tài liệu đều khớp chính xác với cú pháp hỗ trợ của script thực thi.
- QG-03: Không có bất kỳ cảnh báo trôi lệch tài liệu nào tồn tại trong báo cáo nghiệm thu.

## 10. Security & Safety Boundaries
- Ngăn ngừa việc tài liệu lỗi thời hướng dẫn người dùng thực hiện các cấu hình bảo mật yếu kém đã bị bãi bỏ.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Báo cáo phát hiện trôi lệch tài liệu `DOCUMENTATION_DRIFT_REPORT.md`.
1. Script tự động đối soát và đồng bộ tài liệu `scripts/build_docs_v6.py`.

## 13. Related & Complementary Skills
- [`dex-documentation-as-code`](.agents/skills/dex-documentation-as-code/SKILL.md)
- [`dex-skill-catalog-taxonomy`](.agents/skills/dex-skill-catalog-taxonomy/SKILL.md)
- [`dex-skill-execution-evidence-ledger`](.agents/skills/dex-skill-execution-evidence-ledger/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Sau khi nâng cấp từ 200 lên 300 kỹ năng, kỹ sư kích hoạt `dex-skill-documentation-drift` để rà soát toàn bộ kho tài liệu, phát hiện một số chỗ trong `INSTALL.md` và `ARCHITECTURE.md` vẫn còn ghi '201 native skills', tự động đồng bộ hóa toàn bộ tài liệu về chuẩn '301 Native DEX Skills' chính xác 100%.
