---
name: dex-skill-quality-benchmarking
description: Benchmark, measure, and score the real-world engineering effectiveness, token efficiency, and completion fidelity of Agent Skills on representative tasks. Use to drive continuous empirical improvement across the skill framework.
---

# dex-skill-quality-benchmarking

## 1. Purpose & Scope
Đo lường, chấm điểm và thiết lập bài kiểm chuẩn chất lượng thực nghiệm (Skill Quality Benchmarking & Empirical Scoring); đánh giá hiệu quả giải quyết vấn đề kỹ thuật thực tế của từng kỹ năng trên các bài toán mẫu chuẩn hóa, đo lường mức độ tiết kiệm token, tính chính xác của các đoạn mã sinh ra và khả năng ngăn chặn lỗi hồi quy, bảo đảm bộ kỹ năng không chỉ đúng về mặt hình thức mà mang lại giá trị công nghệ thực chất.

## 2. When to Use
- Sau khi hoàn thành việc triển khai hoặc nâng cấp lớn toàn bộ danh mục kỹ năng.
- Định kỳ đo lường chất lượng trước khi phát hành một phiên bản lớn (Major Release v5.0.0).
- So sánh hiệu quả công việc của kỹ sư khi có sự trợ giúp của bộ kỹ năng DEX so với khi không có kỹ năng.

## 3. When NOT to Use
- Không đánh giá chất lượng chỉ dựa trên độ dài của file `SKILL.md` (chất lượng nằm ở độ chính xác của chỉ dẫn kỹ thuật và tính khả thi của ví dụ thực tế).
- Không chấm điểm đậu (Pass) nếu kết quả sinh ra không biên dịch được hoặc không vượt qua unit test thực tế.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Bộ bài tập kỹ thuật mẫu đại diện (Benchmark Test Fixtures: Repo mẫu, Bug tickets, Yêu cầu kiến trúc).
- Môi trường thực thi kiểm chứng tự động.
- Thước đo hiệu quả kỹ thuật (Engineering Fidelity Metrics: First-pass Pass Rate, Token Efficiency, Time to Resolution).
- **Điều kiện tiên quyết**:
- Có runner kiểm thử tự động có khả năng ghi nhận kết quả và đo thời gian thực thi.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Ba trụ cột của Skill Quality:
  1. First-Pass Correctness: Kỹ năng có giúp agent tạo ra giải pháp đúng ngay từ lần đầu tiên mà không cần con người sửa lỗi không?
  2. Domain Depth & Actionability: Hướng dẫn có đủ sâu sắc, chứa các thông số kỹ thuật chuẩn (chứ không phải các lời khuyên chung chung kiểu sách giáo khoa)?
  3. Safety & Boundary Integrity: Kỹ năng có hướng dẫn rõ ràng về những gì KHÔNG được làm để bảo vệ hệ thống không?
- Regression Prevention: Khi cập nhật nội dung một kỹ năng, bộ benchmark phải chứng minh rằng khả năng giải quyết các bài toán cũ không bị suy giảm.
- **Quy tắc quyết định kỹ thuật**:
- Một kỹ năng chỉ được đánh giá là Đạt chuẩn Chất lượng (Production-Ready) khi vượt qua tối thiểu 85% tiêu chí trong bảng chấm điểm thực nghiệm.
- Mọi ví dụ cấu hình và mã nguồn trong phần 7 và 14 của `SKILL.md` bắt buộc phải là cú pháp hợp lệ 100%.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Một kỹ năng cung cấp đoạn mã cấu hình mẫu bị sai cú pháp hoặc lỗi thời, khiến agent copy nguyên mẫu vào dự án làm hỏng tiến trình build của người dùng.

## 6. Step-by-Step Execution Workflow
1. Thiết kế bộ bài toán kiểm chuẩn đại diện cho từng nhóm kỹ năng.
2. Cho AI Agent nạp kỹ năng và giải quyết bài toán trên môi trường repository mẫu.
3. Chạy test suite tự động kiểm tra xem giải pháp có hoạt động chính xác không.
4. Đánh giá mức độ tiêu thụ token và số vòng lặp cần thiết để hoàn thành nhiệm vụ.
5. Tổng hợp điểm số chất lượng vào bảng xếp hạng chất lượng toàn hệ thống (Quality Scorecard).
6. Đưa ra danh sách các kỹ năng cần tiếp tục cải thiện nội dung chuyên môn.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```python
# Khung chấm điểm chất lượng kỹ năng thực nghiệm
def benchmark_skill_quality(skill_id, test_project_path, task_prompt):
    # 1. Chạy agent với skill được nạp
    result = run_agent_with_skill(skill_id, task_prompt, cwd=test_project_path)
    
    # 2. Kiểm tra mã nguồn sinh ra có biên dịch thành công không
    build_success = execute_command("npm run build", cwd=test_project_path).exit_code == 0
    
    # 3. Kiểm tra unit test có pass 100% không
    tests_pass = execute_command("npm test", cwd=test_project_path).exit_code == 0
    
    # 4. Tính toán điểm chất lượng tổng hợp
    quality_score = (
        (40 if build_success else 0) +
        (40 if tests_pass else 0) +
        (20 if result.tokens_used < 15000 else 10)
    )
    return {"skill": skill_id, "score": quality_score, "passed": quality_score >= 80}
```

### Lệnh xác minh & thực thi:
```bash
# Chạy toàn bộ bài đánh giá chất lượng và kiểm toán đặc tả kỹ năng
python scripts/validate_skills.py
```

## 8. Anti-Patterns & Common Traps
- Chấm điểm hoàn thành nhiệm vụ chỉ bằng cách đọc câu trả lời văn bản mà không chạy thử nghiệm mã nguồn thực tế.
- Đưa ra các bài test quá dễ dãi không phản ánh đúng độ phức tạp của môi trường doanh nghiệp thực tế.

## 9. Quality Gates & Acceptance Criteria
- 100% các kỹ năng trong catalog vượt qua bài kiểm tra đặc tả Agent Skills và 14 đề mục bắt buộc.
- Điểm số chất lượng thực nghiệm trung bình toàn framework đạt trên 85/100.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Mọi kịch bản kiểm chuẩn chất lượng phải tuân thủ nghiêm ngặt các ranh giới an toàn, không bao giờ kết nối tới hạ tầng thật.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ thống An ninh & SkillOps**: Tương thích GitHub Actions, SARIF, CycloneDX/SPDX, Semgrep, OWASP ZAP.

## 12. Deliverables & Output Artifacts
- Bảng tổng hợp điểm số chất lượng kỹ năng (Skill Quality Scorecard).
- Báo cáo kiểm toán chất lượng cuối cùng `VALIDATION_REPORT.md`.

## 13. Related & Complementary Skills
dex-skill-activation-evaluation, dex-agent-evaluation-harness, dex-master-orchestrator

## 14. Realistic Usage Example
### Tình huống thực tế:
Trước khi phát hành DEX v5.0.0, đội ngũ kiến trúc sư đã cho chạy bộ kiểm chuẩn chất lượng trên toàn bộ 200 kỹ năng với các dự án mẫu thực tế. Kết quả cho thấy các kỹ sư sử dụng kỹ năng DEX giải quyết các sự cố SRE và kiểm toán bảo mật nhanh hơn gấp 3.5 lần so với việc tự viết prompt từ đầu, và 100% các đoạn mã cấu hình sinh ra đều chạy được ngay lập tức mà không có lỗi cú pháp.
