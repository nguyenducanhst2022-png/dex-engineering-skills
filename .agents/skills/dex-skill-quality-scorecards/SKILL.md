---
name: dex-skill-quality-scorecards
description: Calculate, visualize, and enforce multidimensional engineering quality scorecards across all skills covering documentation completeness, code validity, security posture, and test coverage. Use when maintaining high engineering standards across large skill portfolios.
---

# dex-skill-quality-scorecards

## 1. Purpose & Scope
Tính toán, trực quan hóa và thực thi bảng điểm chất lượng kỹ thuật đa chiều (Multidimensional Quality Scorecards) cho toàn bộ danh mục kỹ năng; đánh giá tính đầy đủ của tài liệu, tính đúng đắn của mã lệnh, tư thế an ninh và độ phủ kiểm thử; bảo đảm tiêu chuẩn kỹ thuật đỉnh cao trên toàn bộ 400 kỹ năng chuyên môn.

## 2. When to Use
- Khi tiến hành nghiệm thu chất lượng trước khi phát hành phiên bản lớn của DEX Framework.
- Khi cần xác định những kỹ năng nào có chất lượng chưa đạt yêu cầu (nội dung sơ sài, thiếu ví dụ mã, thiếu quality gates) để tiến hành nâng cấp.
- Khi thiết lập cổng chất lượng tự động (Quality Gate) trong quy trình tích hợp liên tục CI.

## 3. When NOT to Use
- Khi đang trong giai đoạn phác thảo ý tưởng ban đầu của một kỹ năng mới trong vài giờ đầu tiên.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Toàn bộ file `SKILL.md` trong `.agents/skills/`, kết quả chạy kiểm thử tự động, bảng trọng số tiêu chí đánh giá.
- **Quyền hạn truy cập:** Quyền đọc mã nguồn kỹ năng và xuất báo cáo chất lượng.

## 5. Core Concepts & Taxonomy
- **Composite Quality Score (0–100):** Điểm số tổng hợp được tính toán dựa trên 4 trụ cột chính: Tài liệu & Cấu trúc (30%), Độ phong phú & Ví dụ mã (30%), An ninh & Giảm thiểu rủi ro (20%), Khả năng kiểm chứng & Gates (20%).
- **Zero-Stub Policy:** Bất kỳ kỹ năng nào có nội dung rỗng, sao chép máy móc, hoặc chứa từ khóa placeholder (như 'TODO', 'Chưa có', 'Cần cập nhật') đều bị đánh điểm 0 ngay lập tức.
- **Tiered Classification:** Phân loại chất lượng: Gold (>= 90 điểm), Silver (80-89 điểm), Bronze (70-79 điểm), Failed (< 70 điểm).

## 6. Step-by-Step Execution Workflow
1. Thu thập toàn bộ nội dung của từng kỹ năng và phân tích các chỉ số định lượng: số lượng từ, số khối mã code, số lượng quality gates.
2. Kiểm tra tính hiện diện của 14 phần bắt buộc và tính xác thực của các lệnh trong mục 14.
3. Quét phát hiện các từ khóa placeholder hoặc dấu hiệu sao chép nội dung hàng loạt.
4. Tính toán điểm số thành phần cho từng trụ cột và tổng hợp thành điểm số chất lượng cuối cùng.
5. Phân loại kỹ năng vào các thứ hạng (Gold, Silver, Bronze).
6. Xuất báo cáo Scorecard trực quan dưới dạng bảng Markdown và biểu đồ phân phối.

## 7. Concrete Examples
### Kịch bản tính toán bảng điểm chất lượng kỹ năng trong Python:
```python
import os
import re

def score_skill(skill_path: str) -> dict:
    with open(skill_path, "r", encoding="utf-8") as f:
        text = f.read()
        
    score = 0
    penalties = []
    
    # 1. Kiem tra tinh day du cua 14 phan (toi da 30 diem)
    sections_found = len(re.findall(r"^## \d+\.", text, re.MULTILINE))
    score += min(30, int((sections_found / 14) * 30))
    
    # 2. Kiem tra vi du ma lenh (toi da 30 diem)
    code_blocks = len(re.findall(r"```[a-z]+", text))
    if code_blocks >= 2: score += 30
    elif code_blocks == 1: score += 15
    else: penalties.append("Thieu khoi ma vi du thuc te (-30)")
    
    # 3. Kiem tra Quality Gates (toi da 20 diem)
    qg_count = len(re.findall(r"QG-\d+", text))
    if qg_count >= 2: score += 20
    else: penalties.append("Thieu cac Quality Gates cu the (-20)")
    
    # 4. Kiem tra do phong phu cua tu ngu (toi da 20 diem)
    words = len(text.split())
    if words >= 500: score += 20
    elif words >= 300: score += 10
    else: penalties.append("Noi dung qua ngan duoi 300 tu (-10)")
    
    # Kiem tra Placeholder (Phat nang)
    if re.search(r"(TODO|placeholder|chua co|dang cap nhat)", text, re.IGNORECASE):
        score = 0
        penalties.append("PHAT HIEN PLACEHOLDER: Danh diem 0!")
        
    return {"score": score, "tier": "Gold" if score >= 90 else "Silver" if score >= 80 else "Failed", "penalties": penalties}
```

## 8. Anti-Patterns & Common Traps
- **Template Rubber-Stamping:** Chấm điểm cao cho các kỹ năng chỉ sao chép nguyên văn khung sườn mà không có kiến thức kỹ thuật chuyên sâu.
- **Ignoring Code Snippet Quality:** Chỉ đếm số lượng từ mà không quan tâm đến việc kỹ năng có chứa mã lệnh cụ thể hay không.
- **Tolerating TODOs in Releases:** Bỏ qua các mục ghi chú tạm thời và phát hành kỹ năng dở dang ra môi trường sản xuất.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: 100% kỹ năng trong danh mục đạt điểm số từ 85 điểm trở lên (Hạng Gold / Silver).
- **QG-04**: 0% kỹ năng chứa từ khóa placeholder hoặc nội dung sao chép rỗng.
- **QG-07**: 100% kỹ năng có tối thiểu 2 khối mã ví dụ thực tế và các quality gates cụ thể.

## 10. Security & Safety Boundaries
- Đảm bảo các tiêu chuẩn an ninh và phòng thủ rủi ro được tích hợp đồng bộ vào mọi kỹ năng chuyên môn.

## 11. Platform Adapters
- **Reporting**: Markdown Tables, JSON Reports, GitHub Step Summary.

## 12. Deliverables & Output Artifacts
- Script tính toán bảng điểm chất lượng tự động (`audit_skills.py`).
- Báo cáo phân loại thứ hạng kỹ năng (Scorecard Report).
- Danh sách các khuyến nghị cải tiến cho các kỹ năng có điểm số thấp.

## 13. Related & Complementary Skills
dex-skill-catalog-reconciliation, dex-agent-skills-spec-compatibility, dex-skill-example-test-fixtures

## 14. Realistic Usage Example
```powershell
# Chạy kiểm toán và xuất bảng điểm chất lượng toàn bộ kỹ năng
python scripts/audit_skills.py --scorecard

# Xem tóm tắt phân bố điểm số chất lượng
python -c "import json; d = json.load(open('reports/audit-report.json')); print('Diem trung binh:', d['summary']['average_score'])"
```
