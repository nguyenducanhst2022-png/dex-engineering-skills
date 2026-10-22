---
name: dex-skill-activation-evaluation
description: Evaluate, benchmark, and optimize skill activation precision and recall across realistic user intent prompts, tuning metadata to eradicate false activations. Use when the orchestrator triggers the wrong skills.
---

# dex-skill-activation-evaluation

## 1. Purpose & Scope
Đánh giá, đo lường và tối ưu hóa độ chính xác kích hoạt kỹ năng (Skill Activation Evaluation & Tuning); đo lường tỉ lệ kích hoạt đúng (Precision), tỉ lệ bỏ sót kỹ năng (Recall) và tỉ lệ kích hoạt nhầm (False Positive Activations) trên tập dữ liệu câu hỏi thực tế của người dùng, từ đó tinh chỉnh mô tả (`description`) và các từ khóa ngữ nghĩa trong `SKILL.md` để Master Orchestrator luôn chọn đúng kỹ năng chuyên môn phù hợp nhất.

## 2. When to Use
- Master Orchestrator thường xuyên kích hoạt nhầm kỹ năng không liên quan khi nhận được câu hỏi của người dùng.
- Người dùng yêu cầu một tác vụ kỹ thuật nhưng Orchestrator lại báo không tìm thấy kỹ năng nào phù hợp (Missed Activation).
- Vừa thêm một nhóm kỹ năng mới vào hệ thống và cần kiểm chứng xem có bị xung đột kích hoạt với các kỹ năng cũ hay không.

## 3. When NOT to Use
- Không tối ưu hóa mô tả bằng cách nhồi nhét hàng trăm từ khóa vô nghĩa (Keyword Stuffing) vào trường `description`.
- Không đánh giá độ chính xác chỉ trên 1-2 câu hỏi đơn giản tự nghĩ ra (cần tập dữ liệu kiểm thử tối thiểu 50+ kịch bản đa dạng).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Tập dữ liệu kịch bản kiểm thử kích hoạt (Evaluation Dataset: User Prompts, Ground Truth Expected Skills).
- Danh mục 200 kỹ năng của DEX Framework.
- Bộ công cụ đo lường routing (Routing Evaluator).
- **Điều kiện tiên quyết**:
- Có thuật toán hoặc LLM router đại diện cho Master Orchestrator hoạt động ổn định.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Precision & Recall trong Kích hoạt Kỹ năng:
  + Precision: Trong các kỹ năng được kích hoạt, có bao nhiêu kỹ năng thực sự cần thiết cho tác vụ? (Kích hoạt thừa = Lãng phí context token và gây nhiễu).
  + Recall: Trong tất cả các kỹ năng cần thiết để giải quyết tác vụ, Orchestrator đã chọn ra được bao nhiêu kỹ năng? (Bỏ sót = Tác vụ không được giải quyết trọn vẹn).
- Negative Test Prompts: Các câu hỏi đánh bẫy có chứa từ khóa nhưng ngữ cảnh không phù hợp (ví dụ: 'Hãy giải thích cơ chế của Docker' không nên kích hoạt kỹ năng `dex-container-image-engineering` nếu người dùng chỉ muốn hỏi lý thuyết chung).
- Activation Tuning: Viết lại phần `description` súc tích, nêu rõ hành động ('Engineer production-grade minimal container images...') và điều kiện kích hoạt rõ ràng.
- **Quy tắc quyết định kỹ thuật**:
- Độ chính xác kích hoạt (Routing Precision) tổng thể của hệ sinh thái phải đạt tối thiểu 90%.
- Với một câu hỏi thông thường: Orchestrator chỉ được phép kích hoạt tối đa từ 1 đến 3 kỹ năng chuyên sâu nhất.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Một kỹ năng viết mô tả quá rộng (ví dụ: 'Giúp lập trình mọi thứ trong phần mềm') khiến bất kỳ câu hỏi nào Orchestrator cũng lôi kỹ năng đó vào thực thi.

## 6. Step-by-Step Execution Workflow
1. Xây dựng bộ dữ liệu đánh giá gồm 100 câu hỏi thực tế bao phủ 20 nhóm ngành (Groups A–T) kèm danh sách skills kỳ vọng.
2. Chạy kịch bản đánh giá tự động: gửi từng câu hỏi qua bộ chọn kỹ năng của Orchestrator.
3. So sánh danh sách kỹ năng được chọn với Ground Truth để tính toán Precision, Recall và F1-Score.
4. Phân tích các trường hợp kích hoạt sai (False Positives) và kích hoạt thiếu (False Negatives).
5. Tinh chỉnh lại trường `description` của các kỹ năng liên quan.
6. Chạy lại bài kiểm tra hồi quy để chứng minh việc sửa không làm hỏng các trường hợp khác.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```python
# Đánh giá độ chính xác kích hoạt của bộ kỹ năng
def evaluate_skill_activation(test_cases, orchestrator_router):
    total_precision = []
    total_recall = []
    
    for case in test_cases:
        selected_skills = set(orchestrator_router.route(case["prompt"]))
        expected_skills = set(case["expected_skills"])
        
        true_positives = len(selected_skills.intersection(expected_skills))
        precision = true_positives / len(selected_skills) if selected_skills else 0
        recall = true_positives / len(expected_skills) if expected_skills else 0
        
        total_precision.append(precision)
        total_recall.append(recall)
        
    print(f"Average Precision: {sum(total_precision)/len(total_precision):.2f}")
    print(f"Average Recall: {sum(total_recall)/len(total_recall):.2f}")
```

### Lệnh xác minh & thực thi:
```bash
# Chạy bài đánh giá độ chính xác kích hoạt kỹ năng tự động
python scripts/evaluate_routing.py --testset tests/data/routing_eval_dataset.json
```

## 8. Anti-Patterns & Common Traps
- Kích hoạt cùng lúc 15 kỹ năng cho một câu hỏi đơn giản.
- Viết mô tả kỹ năng bằng những tính từ chung chung như 'tuyệt vời', 'chuyên gia hàng đầu' thay vì mô tả năng lực kỹ thuật cụ thể.

## 9. Quality Gates & Acceptance Criteria
- Điểm F1-Score kích hoạt tổng thể đạt tối thiểu 0.88 trên bộ dữ liệu kiểm thử chuẩn.
- 0 trường hợp kích hoạt kỹ năng hoàn toàn không liên quan (Zero False-Domain Trigger).
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Bộ dữ liệu đánh giá không chứa thông tin bí mật hay thông tin nhạy cảm của dự án khách hàng.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ thống An ninh & SkillOps**: Tương thích GitHub Actions, SARIF, CycloneDX/SPDX, Semgrep, OWASP ZAP.

## 12. Deliverables & Output Artifacts
- Báo cáo ma trận kích hoạt kỹ năng (Confusion Matrix & F1-Scores).
- Phiên bản cập nhật trường `description` chuẩn hóa cho các kỹ năng có độ chính xác thấp.

## 13. Related & Complementary Skills
dex-skill-semantic-deduplication, dex-skill-quality-benchmarking, dex-master-orchestrator

## 14. Realistic Usage Example
### Tình huống thực tế:
Một lập trình viên hỏi: 'Làm sao để đo lường tỷ lệ đột biến bị tiêu diệt trong unit test?'. Ban đầu, Orchestrator kích hoạt nhầm kỹ năng `dex-unit-testing`. Sau khi chạy bài đánh giá Activation Evaluation và bổ sung từ khóa 'mutation testing, survived mutants' vào mô tả của `dex-mutation-testing`, Orchestrator đã chọn chính xác 100% kỹ năng kiểm thử đột biến chuyên sâu.
