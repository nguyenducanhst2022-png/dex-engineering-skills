---
name: dex-skill-risk-scoring
description: Quantify operational, security, and privilege risk scores for Agent Skills based on tool access, filesystem mutation scope, network egress, and execution authority. Use when enforcing principle of least privilege and gating autonomous agent execution.
---

# dex-skill-risk-scoring

## 1. Purpose & Scope
Định lượng và đánh giá điểm số rủi ro vận hành, an ninh và đặc quyền của các kỹ năng Agent (Agent Skill Risk Scoring); dựa trên danh mục công cụ được phép gọi, phạm vi ghi/xóa hệ thống tệp, quyền truy cập mạng ra ngoài (Egress) và thẩm quyền thực thi lệnh; phục vụ việc thực thi nguyên tắc đặc quyền tối thiểu và thiết lập rào chắn kiểm soát Agent tự trị.

## 2. When to Use
- Trước khi cấp phép cho một kỹ năng mới được đưa vào danh mục kích hoạt tự động của Agent.
- Khi phân loại các kỹ năng cần có sự phê duyệt của con người (HITL) và các kỹ năng được tự do chạy.
- Khi xây dựng hồ sơ rủi ro an ninh cho toàn bộ hệ sinh thái kỹ năng của tổ chức.

## 3. When NOT to Use
- Khi đánh giá rủi ro tài chính của một khoản đầu tư.
- Khi kiểm thử hiệu năng tốc độ xử lý của kỹ năng.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Tệp `SKILL.md` và mã nguồn công cụ đi kèm, bảng trọng số rủi ro tiêu chuẩn (Risk Weight Matrix).
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; bảo vệ toàn vẹn tài sản kỹ nghệ và dữ liệu sản xuất.

## 5. Core Concepts & Taxonomy
- **Multi-Factor Risk Scoring:** Tính toán điểm số từ 0.0 (An toàn tuyệt đối) đến 10.0 (Nguy cơ cực cao) dựa trên 4 yếu tố: Thao tác tệp (Filesystem), Mạng (Network), Lệnh shell (Execution) và Tính phá hủy (Destructiveness).
- **Read-Only vs Mutating Capability:** Các kỹ năng chỉ đọc (như kiểm tra header nhị phân) có điểm rủi ro thấp hơn nhiều so với kỹ năng sửa đổi mã nguồn hoặc xóa cơ sở dữ liệu.
- **Risk Tier Classification:** Tier 1 (Safe: 0-3), Tier 2 (Moderate: 4-6), Tier 3 (High Risk: 7-8), Tier 4 (Critical: 9-10 - Bắt buộc duyệt kép).

## 6. Step-by-Step Execution Workflow
1. Phân tích cú pháp tệp `SKILL.md` để trích xuất danh sách công cụ và quyền hạn được đề cập trong Mục 4 và Mục 10.
2. Kiểm tra xem kỹ năng có yêu cầu quyền chạy lệnh terminal (`run_command`), sửa tệp (`edit_file`) hay kết nối mạng bên ngoài hay không.
3. Tính toán điểm rủi ro tổng hợp dựa trên công thức trọng số chuẩn hóa.
4. Gán cấp bậc rủi ro (Risk Tier) tương ứng vào siêu dữ liệu của kỹ năng trong manifest.
5. Lập báo cáo đánh giá rủi ro kho kỹ năng `SKILL_RISK_AUDIT_REPORT.md`.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```python
# Skill Operational Risk Scoring Calculator
def calculate_skill_risk(tool_permissions: list[str], network_egress: bool, destructive_actions: bool) -> tuple[float, str]:
    score = 1.0 # Baseline safe score

    if "run_command" in tool_permissions:
        score += 3.5
    if "write_file" in tool_permissions or "edit_file" in tool_permissions:
        score += 2.0
    if network_egress:
        score += 2.0
    if destructive_actions:
        score += 2.5

    score = min(10.0, score)

    if score <= 3.0: tier = "TIER_1_SAFE"
    elif score <= 6.0: tier = "TIER_2_MODERATE"
    elif score <= 8.5: tier = "TIER_3_HIGH"
    else: tier = "TIER_4_CRITICAL"

    return score, tier
```

## 8. Anti-Patterns & Common Traps
- Đánh đồng tất cả các kỹ năng đều có mức độ an toàn như nhau và cho phép Agent tự do chạy mọi công cụ.
- Cấp quyền thực thi shell (`run_command`) cho một kỹ năng chỉ làm nhiệm vụ đọc và tóm tắt tài liệu văn bản.
- Bỏ qua việc đánh giá quyền truy cập mạng, khiến kỹ năng có nguy cơ gửi dữ liệu ra máy chủ lạ.

## 9. Quality Gates & Acceptance Criteria
- QG-01: 100% các kỹ năng trong catalog đều được gán điểm rủi ro và Risk Tier rõ ràng trong manifest.
- QG-02: Toàn bộ kỹ năng thuộc Tier 3 và Tier 4 đều có quy định kiểm duyệt con người (HITL) bắt buộc.
- QG-03: Không có kỹ năng chỉ đọc nào bị cấp thừa quyền ghi hoặc quyền chạy lệnh terminal.

## 10. Security & Safety Boundaries
- Ngăn chặn việc Agent bị lạm dụng quyền hạn để thực thi các hành động phá hoại thông qua việc kiểm soát rủi ro chặt chẽ.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Bảng điểm số rủi ro kho kỹ năng `manifests/skill-risk-scores.json`.
1. Báo cáo kiểm toán hồ sơ rủi ro `SKILL_RISK_AUDIT_REPORT.md`.

## 13. Related & Complementary Skills
- [`dex-agent-permissions`](.agents/skills/dex-agent-permissions/SKILL.md)
- [`dex-llm-human-review-gates`](.agents/skills/dex-llm-human-review-gates/SKILL.md)
- [`dex-skill-security-screening`](.agents/skills/dex-skill-security-screening/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Thẩm định an toàn cho 100 kỹ năng mới. Kỹ sư kích hoạt `dex-skill-risk-scoring`, tự động chấm điểm cho toàn bộ 100 skills, nhận diện 12 kỹ năng thuộc Tier 3 (chứa lệnh can thiệp nhị phân hoặc sửa file) và tự động gắn cờ yêu cầu phê duyệt con người khi Agent kích hoạt, đảm bảo an toàn tuyệt đối.
