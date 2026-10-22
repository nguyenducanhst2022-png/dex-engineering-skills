---
name: dex-skill-reference-graph
description: Construct and validate the bidirectional cross-skill reference graph across all 300 skills, detecting broken relative links, orphaned skills, circular delegation deadlocks, and missing prerequisite relationships. Use when validating catalog integrity and documentation graph completeness.
---

# dex-skill-reference-graph

## 1. Purpose & Scope
Xây dựng, trực quan hóa và kiểm chứng đồ thị tham chiếu chéo hai chiều (Bidirectional Skill Reference Graph) giữa toàn bộ 300 kỹ năng; phát hiện các liên kết tương đối bị hỏng (Broken Markdown Links), các kỹ năng bị cô lập (Orphaned Skills), các bế tắc ủy quyền vòng tròn (Circular Delegation Deadlocks) và thiếu sót quan hệ kỹ năng bổ trợ; đảm bảo tính toàn vẹn và liên kết chặt chẽ của mạng lưới tri thức kỹ năng.

## 2. When to Use
- Trước khi đóng gói phát hành phiên bản framework mới để kiểm tra tính toàn vẹn của tất cả các đường dẫn liên kết.
- Khi thêm mới hoặc đổi tên một kỹ năng và cần cập nhật lại toàn bộ các kỹ năng khác đang tham chiếu tới nó.
- Khi phân tích cấu trúc mạng lưới kỹ năng để tối ưu hóa khả năng gợi ý kỹ năng bổ trợ cho AI Agent.

## 3. When NOT to Use
- Khi kiểm tra liên kết web ra các trang bên ngoài Internet.
- Khi chỉ sửa lỗi chính tả nhỏ trong một file tài liệu duy nhất.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Toàn bộ thư mục `.agents/skills/`, công cụ phân tích đồ thị (NetworkX hoặc script Python bóc tách Markdown AST).
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; bảo vệ toàn vẹn tài sản kỹ nghệ và dữ liệu sản xuất.

## 5. Core Concepts & Taxonomy
- **Bidirectional Link Consistency:** Nếu kỹ năng A liệt kê kỹ năng B là kỹ năng liên quan trong Mục 13, thì kỹ năng B cũng nên nhận biết được mối quan hệ với kỹ năng A.
- **Zero Dead Link Guarantee:** Mọi đường dẫn Markdown `[link](.agents/skills/xxx/SKILL.md)` phải trỏ tới một tệp tin thực sự tồn tại trên đĩa.
- **Graph Centrality Analysis:** Đo lường độ trung tâm của từng kỹ năng để xác định những kỹ năng nền tảng cốt lõi được sử dụng nhiều nhất (Hub Skills).

## 6. Step-by-Step Execution Workflow
1. Quét toàn bộ 300 tệp `SKILL.md` và bóc tách các liên kết trong Mục 13 (Related & Complementary Skills).
2. Kiểm tra sự tồn tại vật lý trên đĩa của từng đường dẫn liên kết được trích xuất.
3. Xây dựng ma trận kề (Adjacency Matrix) đại diện cho đồ thị mạng lưới kỹ năng.
4. Chạy thuật toán phát hiện các nút bị cô lập (độ vào và độ ra bằng 0) hoặc các chu trình ủy quyền kín.
5. Xuất ra tệp sơ đồ mạng lưới kỹ năng `skill_reference_network.json`.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```python
# Skill Reference Graph Validator
import os
import re

def validate_skill_reference_graph(skills_root: str):
    skill_names = set(os.listdir(skills_root))
    broken_links = []
    graph = {}

    for name in skill_names:
        file_path = os.path.join(skills_root, name, "SKILL.md")
        if not os.path.isfile(file_path): continue
        
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Extract related skill references
        links = re.findall(r'\[`?([a-z0-9-]+)`?\]\(\.agents/skills/([a-z0-9-]+)/SKILL\.md\)', content)
        graph[name] = []
        for text, target in links:
            if target not in skill_names:
                broken_links.append(f"{name} -> broken reference: {target}")
            else:
                graph[name].append(target)

    return graph, broken_links
```

## 8. Anti-Patterns & Common Traps
- Đổi tên một kỹ năng nhưng không cập nhật lại các kỹ năng khác đang trỏ tới nó, dẫn đến hàng loạt lỗi 404 hỏng liên kết.
- Kỹ năng hoàn toàn bị cô lập, không có bất kỳ kỹ năng nào liên kết tới và cũng không liên kết tới ai (Orphaned Skill).
- Tạo liên kết tham chiếu tròn kín giữa 2 Agent khiến chúng liên tục ủy quyền công việc qua lại cho nhau mà không bao giờ thực hiện.

## 9. Quality Gates & Acceptance Criteria
- QG-01: 100% các liên kết tham chiếu kỹ năng trong Mục 13 đều trỏ tới tệp tin tồn tại thực tế (0 Broken Links).
- QG-02: Không có kỹ năng nào bị cô lập hoàn toàn khỏi đồ thị tri thức kỹ năng.
- QG-03: Đồ thị tham chiếu được xuất bản đầy đủ dưới dạng tệp dữ liệu máy đọc được.

## 10. Security & Safety Boundaries
- Ngăn chặn các liên kết độc hại trỏ ra các đường dẫn tương đối vượt ra ngoài thư mục dự án (`../../etc/passwd`).
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Đồ thị mạng lưới tham chiếu kỹ năng `skill_reference_network.json`.
1. Báo cáo kiểm toán tính toàn vẹn liên kết kỹ năng `LINK_INTEGRITY_REPORT.md`.

## 13. Related & Complementary Skills
- [`dex-skill-catalog-taxonomy`](.agents/skills/dex-skill-catalog-taxonomy/SKILL.md)
- [`dex-skill-dependency-graph`](.agents/skills/dex-skill-dependency-graph/SKILL.md)
- [`dex-skill-discovery-indexer`](.agents/skills/dex-skill-discovery-indexer/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Kiểm tra tính toàn vẹn của 301 kỹ năng trước ngày phát hành v6.0. Kỹ sư kích hoạt `dex-skill-reference-graph`, quét hơn 1,200 liên kết chéo trong toàn bộ kho, phát hiện 4 đường dẫn cũ bị gõ sai chính tả tên thư mục, tự động sửa chữa và đưa tỷ lệ liên kết hợp lệ đạt chuẩn 100%.
