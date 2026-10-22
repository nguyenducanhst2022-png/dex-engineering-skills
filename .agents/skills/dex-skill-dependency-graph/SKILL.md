---
name: dex-skill-dependency-graph
description: Model, validate, and traverse the directed acyclic graph (DAG) of skill dependencies and orchestration pipelines, detecting circular references and sequencing errors. Use when composing complex multi-skill workflows.
---

# dex-skill-dependency-graph

## 1. Purpose & Scope
Mô hình hóa, kiểm chứng và duyệt đồ thị có hướng không chu trình (Directed Acyclic Graph - DAG) của các mối quan hệ phụ thuộc giữa các kỹ năng trong hệ thống (Skill Dependency Graph); phát hiện và triệt tiêu các tham chiếu vòng tròn (Circular References), xác thực tính hợp lệ của các liên kết chéo (`related_skills`), và bảo đảm thứ tự thực thi tuần tự chuẩn xác cho các kịch bản điều phối đa kỹ năng phức tạp.

## 2. When to Use
- Master Orchestrator cần phối hợp nhiều kỹ năng để giải quyết một bài toán lớn (ví dụ: Audit -> Fix -> Test -> Deploy).
- Xuất hiện lỗi vòng lặp phụ thuộc (ví dụ: Skill A gọi Skill B, Skill B lại đòi hỏi Skill A), khiến tiến trình điều phối bị đóng băng.
- Phân tích mức độ gắn kết (Coupling) và tính độc lập của các kỹ năng trong kho lưu trữ.

## 3. When NOT to Use
- Không tạo ra các chuỗi phụ thuộc quá dài (>6 tầng kỹ năng lồng nhau) làm tăng độ trễ và độ phức tạp không cần thiết.
- Không biến các kỹ năng độc lập thành phụ thuộc cứng nếu chúng chỉ mang tính chất tham khảo tùy chọn.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Danh mục toàn bộ 200 kỹ năng của DEX Framework.
- Các trường khai báo quan hệ phụ thuộc (`dependencies`, `related_skills` trong metadata).
- Kịch bản điều phối thực tế cần lập lịch thực thi.
- **Điều kiện tiên quyết**:
- Toàn bộ các kỹ năng được tham chiếu đều phải tồn tại thực tế trong danh mục.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Directed Acyclic Graph (DAG): Đồ thị trong đó các đỉnh là các kỹ năng, các cạnh có hướng đại diện cho quan hệ phụ thuộc ('Skill B cần kết quả của Skill A'). Đồ thị tuyệt đối không được có chu trình (No Cycles).
- Topological Sort: Thuật toán sắp xếp thứ tự thực thi hợp lệ của các kỹ năng sao cho mỗi kỹ năng chỉ được chạy sau khi tất cả các kỹ năng tiền đề của nó đã hoàn thành thành công.
- Dangling References: Tình huống một kỹ năng khai báo phụ thuộc vào một kỹ năng `dex-old-feature` nhưng kỹ năng đó đã bị xóa hoặc đổi tên trong hệ thống.
- **Quy tắc quyết định kỹ thuật**:
- Bất kỳ tham chiếu vòng tròn (Circular Dependency) nào được phát hiện trong đồ thị phải bị coi là lỗi nghiêm trọng (Critical Test Failure).
- Mọi liên kết trong mục `Related & Complementary Skills` bắt buộc phải trỏ tới một kỹ năng có thật trong thư mục `.agents/skills/`.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Orchestrator bắt đầu thực thi một chuỗi 5 kỹ năng nhưng đến bước thứ 4 thì bị dừng đột ngột vì kỹ năng phụ thuộc không tồn tại trên đĩa.

## 6. Step-by-Step Execution Workflow
1. Quét toàn bộ các file `SKILL.md` và trích xuất danh sách các kỹ năng liên quan (`related_skills`).
2. Xây dựng ma trận kề (Adjacency List) biểu diễn đồ thị phụ thuộc toàn hệ thống.
3. Áp dụng thuật toán tìm kiếm theo chiều sâu (DFS) để kiểm tra chu trình (Cycle Detection).
4. Kiểm tra toàn bộ các tham chiếu mồ côi (Dangling References).
5. Xuất sơ đồ đồ thị quan hệ trực quan dưới định dạng Mermaid diagram và chạy thuật toán sắp xếp tô-pô.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```python
# Kiểm tra chu trình trong đồ thị phụ thuộc kỹ năng bằng thuật toán DFS
def detect_cycles_in_skills(graph: dict[str, list[str]]) -> list[list[str]]:
    visited = set()
    rec_stack = set()
    cycles = []

    def dfs(node, path):
        visited.add(node)
        rec_stack.add(node)
        path.append(node)

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                dfs(neighbor, path)
            elif neighbor in rec_stack:
                cycle_start = path.index(neighbor)
                cycles.append(path[cycle_start:] + [neighbor])

        rec_stack.remove(node)
        path.pop()

    for skill in graph:
        if skill not in visited:
            dfs(skill, [])
    return cycles
```

### Lệnh xác minh & thực thi:
```bash
# Chạy bài kiểm thử tự động kiểm tra đồ thị phụ thuộc và liên kết của toàn bộ 201 skills
pytest tests/test_skill_dependencies.py
```

## 8. Anti-Patterns & Common Traps
- Để kỹ năng con phụ thuộc ngược lại vào chính Master Orchestrator.
- Khai báo các liên kết kỹ năng bằng các tên không nhất quán (sai chính tả hoặc thiếu tiền tố `dex-`).

## 9. Quality Gates & Acceptance Criteria
- 0 chu trình (Cycles) tồn tại trong toàn bộ đồ thị phụ thuộc của 200 kỹ năng.
- 100% các tham chiếu kỹ năng liên quan đều phân giải (resolve) thành công tới file thực tế trên đĩa.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Giới hạn độ sâu tối đa của chuỗi phụ thuộc (Max Execution Depth <= 5) để ngăn chặn cạn kiệt tài nguyên tính toán.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ thống An ninh & SkillOps**: Tương thích GitHub Actions, SARIF, CycloneDX/SPDX, Semgrep, OWASP ZAP.

## 12. Deliverables & Output Artifacts
- Sơ đồ đồ thị phụ thuộc Mermaid hoàn chỉnh.
- Bộ test suite `test_skill_dependencies.py` kiểm chứng tính toàn vẹn của đồ thị.

## 13. Related & Complementary Skills
dex-master-orchestrator, dex-skill-discovery-indexer, dex-skill-quality-benchmarking

## 14. Realistic Usage Example
### Tình huống thực tế:
Khi thiết kế kịch bản tự động xử lý sự cố an ninh, Master Orchestrator cần phối hợp 4 kỹ năng: Phân loại cảnh báo -> Kiểm tra ranh giới mạng -> Vá mã nguồn -> Xác minh hồi quy. Nhờ có Dependency Graph, hệ thống tự động lập lịch thực thi tuần tự chuẩn xác theo đúng thứ tự logic, không bao giờ xảy ra tình trạng chạy bài kiểm tra hồi quy trước khi bản vá được áp dụng.
