---
name: dex-skill-catalog-reconciliation
description: Reconcile, validate, and synchronize skill catalog manifests, directory structures, unique skill indices, and cross-references across decentralized repositories. Use when maintaining unified skill governance across large ecosystems.
---

# dex-skill-catalog-reconciliation

## 1. Purpose & Scope
Đối soát, kiểm chứng và đồng bộ hóa danh mục kỹ năng (Skill Catalog Reconciliation), cấu trúc thư mục, chỉ mục kỹ năng duy nhất và các tham chiếu chéo giữa các repository phân tán; bảo đảm tính toàn vẹn 100% của hệ sinh thái DEX Skills.

## 2. When to Use
- Khi số lượng kỹ năng tăng lên hàng trăm và có nguy cơ xuất hiện kỹ năng mồ côi (tồn tại trên đĩa nhưng không có trong manifest hoặc ngược lại).
- Khi sáp nhập các nhánh phát triển lớn và cần đối soát tính duy nhất của mã ID kỹ năng.
- Khi cập nhật cấu trúc danh mục và muốn đảm bảo các liên kết tham chiếu chéo (`related`) không bị đứt gãy.

## 3. When NOT to Use
- Khi chỉ chỉnh sửa nội dung văn bản bên trong một file kỹ năng đơn lẻ mà không thay đổi cấu trúc danh mục.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Thư mục kỹ năng `.agents/skills/`, tệp manifest danh mục (`manifests/dex-skills.json`), bảng chỉ mục kỹ năng.
- **Quyền hạn truy cập:** Quyền đọc và cập nhật manifest danh mục.

## 5. Core Concepts & Taxonomy
- **Catalog Bi-directional Parity:** Tính đối xứng hai chiều: Mọi thư mục trên đĩa phải có mặt trong manifest, và mọi mục trong manifest phải có thư mục hợp lệ trên đĩa.
- **Cross-Reference Integrity:** Đảm bảo tất cả các ID kỹ năng được liệt kê trong mục `related` đều là các kỹ năng có thực và đang hoạt động.
- **Canonical Group Partitioning:** Phân chia nghiêm ngặt toàn bộ danh mục kỹ năng vào đúng 40 nhóm chuyên môn chuẩn tắc (Groups A đến AN, đúng 10 kỹ năng mỗi nhóm).

## 6. Step-by-Step Execution Workflow
1. Quét toàn bộ các thư mục con trong `.agents/skills/` để trích xuất danh sách kỹ năng thực tế trên đĩa.
2. Phân tích cú pháp tệp `manifests/dex-skills.json` để trích xuất danh mục khai báo.
3. So sánh sai lệch: phát hiện các kỹ năng chưa được đăng ký (Unregistered) hoặc kỹ năng bị mất file (Missing).
4. Kiểm tra tính duy nhất của mã định danh ID kỹ năng (0% trùng lặp).
5. Xác thực tính hợp lệ của tất cả các tham chiếu chéo giữa các kỹ năng liên quan.
6. Tự động cập nhật manifest chuẩn hóa và xuất báo cáo đối soát.

## 7. Concrete Examples
### Kịch bản đối soát danh mục kỹ năng hai chiều trong Python:
```python
import os
import json

SKILLS_DIR = ".agents/skills"
MANIFEST_PATH = "manifests/dex-skills.json"

def reconcile_skill_catalog():
    disk_skills = {d for d in os.listdir(SKILLS_DIR) if os.path.isdir(os.path.join(SKILLS_DIR, d))}
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest_skills = {s["id"] for s in json.load(f)["skills"]}
        
    missing_on_disk = manifest_skills - disk_skills
    unregistered_on_manifest = disk_skills - manifest_skills
    
    print(f"Tong so ky nang tren dia: {len(disk_skills)}")
    print(f"Tong so ky nang trong manifest: {len(manifest_skills)}")
    
    if missing_on_disk:
        raise ValueError(f"Loi doi soat: Co trong manifest nhung khong co tren dia: {missing_on_disk}")
    if unregistered_on_manifest:
        raise ValueError(f"Loi doi soat: Co tren dia nhung chua dang ky vao manifest: {unregistered_on_manifest}")
        
    print("Doi soat thanh cong! Danh muc hoan toan dong nhat hai chieu.")
```

## 8. Anti-Patterns & Common Traps
- **Dangling Unregistered Skill Directories:** Tạo thư mục kỹ năng mới để thử nghiệm nhưng bỏ quên không đăng ký vào manifest chính.
- **Broken Cross-References:** Liệt kê các kỹ năng liên quan trong mục `Related Skills` nhưng gõ sai chính tả mã ID.
- **Manual Manifest Desynchronization:** Sửa manifest bằng tay mà không chạy script kiểm chứng tự động.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Tính tương đương hai chiều giữa đĩa và manifest đạt chính xác 100% (0 sai lệch).
- **QG-04**: 0% trùng lặp mã định danh ID trên toàn bộ danh mục kỹ năng.
- **QG-08**: 100% các liên kết kỹ năng liên quan (`related`) đều trỏ tới kỹ năng có thực.

## 10. Security & Safety Boundaries
- Ngăn ngừa việc đưa vào các kỹ năng độc hại ngoài danh mục kiểm duyệt thông qua việc kiểm tra mã băm toàn vẹn.

## 11. Platform Adapters
- **Tools**: Python Script Engine, JSON Schema Validator, Git Hooks.

## 12. Deliverables & Output Artifacts
- Tệp manifest `manifests/dex-skills.json` đồng bộ hoàn toàn.
- Báo cáo đối soát danh mục chi tiết.
- Bộ kiểm thử tự động xác minh tính toàn vẹn danh mục trong CI.

## 13. Related & Complementary Skills
dex-agent-skills-spec-compatibility, dex-skill-quality-scorecards, dex-semantic-routing-evaluations

## 14. Realistic Usage Example
```powershell
# Chạy đối soát danh mục kỹ năng
python scripts/discover_skills.py --reconcile

# Kiểm tra tính toàn vẹn bằng pytest
pytest tests/test_skill_registry.py -v
```
