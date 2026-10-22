---
name: dex-skill-routing-conflict-tests
description: Design automated semantic disambiguation and routing conflict test suites, probing borderline intent prompts across overlapping skill domains to guarantee deterministic triage. Use when evaluating master orchestrator accuracy and eliminating skill routing collisions.
---

# dex-skill-routing-conflict-tests

## 1. Purpose & Scope
Thiết kế và xây dựng bộ kiểm thử xung đột định tuyến và khử nhập nhằng ngữ nghĩa (Semantic Disambiguation & Routing Conflict Testing); thử nghiệm các câu nhắc lệnh nằm ở ranh giới giao thoa giữa các kỹ năng có phạm vi tương tự nhau; đo lường độ chính xác phân loại của Master Orchestrator và đảm bảo tính xác định tuyệt đối trong việc điều phối kỹ năng.

## 2. When to Use
- Khi kho kỹ năng có nhiều kỹ năng cùng giải quyết các khía cạnh khác nhau của một bài toán (ví dụ: `dex-frontend-performance` vs `dex-web-animation-performance`).
- Khi Master Orchestrator thỉnh thoảng điều phối nhầm kỹ năng cho các yêu cầu có bối cảnh đa nghĩa.
- Trước khi bổ sung một kỹ năng mới để đảm bảo không xâm lấn vào phạm vi kích hoạt của các kỹ năng sẵn có.

## 3. When NOT to Use
- Khi các câu hỏi có ý định rõ ràng và không hề có sự giao thoa ngữ nghĩa.
- Khi kiểm thử hiệu năng tốc độ phản hồi của API.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Bộ định tuyến kỹ năng (Orchestrator Routing Engine), bộ câu hỏi kiểm thử ranh giới ngữ nghĩa (Borderline Prompts), ma trận nhầm lẫn (Confusion Matrix).
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; bảo vệ toàn vẹn tài sản kỹ nghệ và dữ liệu sản xuất.

## 5. Core Concepts & Taxonomy
- **Semantic Boundary Overlap:** Hiện tượng hai kỹ năng cùng chứa các từ khóa kích hoạt tương tự nhau (ví dụ: 'CSS', 'Performance', 'Animation').
- **Disambiguation Rules:** Các quy tắc phân định rõ ràng trong Mục 2 (When to Use) và Mục 3 (When NOT to Use) để bộ định tuyến biết cách lựa chọn chính xác.
- **Confusion Matrix Evaluation:** Đo lường tỷ lệ phân loại đúng (Precision/Recall) và nhận diện các cặp kỹ năng thường xuyên bị nhầm lẫn lẫn nhau.

## 6. Step-by-Step Execution Workflow
1. Xây dựng tập hợp 50 câu hỏi biên có chủ đích gây nhầm lẫn giữa các cặp kỹ năng lân cận.
2. Chạy quy trình định tuyến tự động qua Master Orchestrator.
3. Ghi nhận kỹ năng được chọn và đối chiếu với nhãn chuẩn kỳ vọng.
4. Vẽ ma trận nhầm lẫn (Confusion Matrix) để xác định các cặp kỹ năng có xung đột định tuyến.
5. Tinh chỉnh lại mô tả trong tệp `SKILL.md` của các kỹ năng liên quan và kiểm tra lại đạt F1-Score >= 0.85.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```python
# Routing Conflict Disambiguation Test Runner
def test_routing_conflict(orchestrator, test_cases: list[dict]):
    results = {"passed": 0, "failed": 0, "conflicts": []}

    for case in test_cases:
        selected_skill = orchestrator.route_intent(case["prompt"])
        if selected_skill == case["expected_skill"]:
            results["passed"] += 1
        else:
            results["failed"] += 1
            results["conflicts"].append({
                "prompt": case["prompt"],
                "expected": case["expected_skill"],
                "actual": selected_skill
            })

    f1_score = results["passed"] / len(test_cases)
    print(f"Routing Accuracy: {f1_score*100:.2f}% | Conflicts: {results['failed']}")
    assert f1_score >= 0.85, "Routing disambiguation failed target threshold!" 
```

## 8. Anti-Patterns & Common Traps
- Viết phần mô tả kỹ năng (Description) quá chung chung chứa hàng loạt từ khóa của các kỹ năng khác, khiến kỹ năng này liên tục bị chọn nhầm.
- Bỏ qua phần 'When NOT to Use' khiến Orchestrator không có căn cứ loại trừ khi gặp tình huống đa nghĩa.
- Chỉ kiểm tra định tuyến với các câu hỏi dễ hiển nhiên mà không bao giờ kiểm thử các câu hỏi ở vùng ranh giới.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Điểm số định tuyến tổng hợp F1-Score đạt tối thiểu 0.85 trên toàn bộ bộ kiểm thử ranh giới.
- QG-02: 100% các cặp kỹ năng có phạm vi tương tự đều có các quy tắc loại trừ lẫn nhau rõ ràng.
- QG-03: Không có kỹ năng nào bị chiếm đoạt 100% lưu lượng kích hoạt bởi một kỹ năng khác.

## 10. Security & Safety Boundaries
- Đảm bảo các kỹ năng có mức độ rủi ro cao không bao giờ bị kích hoạt nhầm khi người dùng chỉ yêu cầu một tác vụ thông thường.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Bộ kịch bản kiểm thử xung đột định tuyến `test_routing_conflicts.py`.
1. Ma trận nhầm lẫn và báo cáo tối ưu hóa định tuyến `ROUTING_CONFLICT_REPORT.md`.

## 13. Related & Complementary Skills
- [`dex-skill-semantic-deduplication`](.agents/skills/dex-skill-semantic-deduplication/SKILL.md)
- [`dex-master-orchestrator`](.agents/skills/dex-master-orchestrator/SKILL.md)
- [`dex-skill-catalog-taxonomy`](.agents/skills/dex-skill-catalog-taxonomy/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Người dùng đưa ra yêu cầu: 'Giao diện bảng điều khiển bị giật khi cuộn chuột qua biểu đồ'. Hai kỹ năng `dex-web-animation-performance` và `dex-dashboard-data-storytelling` cùng tranh nhau kích hoạt. Kỹ sư kích hoạt `dex-skill-routing-conflict-tests`, phân tích từ khóa trọng tâm là 'giật khi cuộn' (hiệu năng), tinh chỉnh lại phần loại trừ và định tuyến chính xác về `dex-web-animation-performance`.
