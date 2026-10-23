---
name: dex-agent-reviewer-independence
description: Architect independent, uncorrupted reviewer agent workflows to evaluate code changes, architecture decisions, and task completion claims. Eliminate confirmation bias, enforce evidence-based grading, and separate creation from verification. Use in multi-agent governance.
---

# dex-agent-reviewer-independence

## 1. Purpose & Scope
Thiết kế và thực thi quy trình thẩm định độc lập (Independent Reviewer Workflows) giữa các tác nhân AI; loại bỏ hoàn toàn thiên kiến xác nhận (Confirmation Bias) khi một agent tự kiểm tra mã nguồn do chính nó viết ra; phân tách tuyệt đối trách nhiệm giữa Tác nhân Triển khai (Coder) và Tác nhân Thẩm định (Reviewer); và bảo đảm mọi quyết định phê duyệt đều dựa trên bằng chứng kiểm chứng thực nghiệm.

## 2. When to Use
- Khi xây dựng hệ sinh thái Multi-Agent tự động hóa phát triển phần mềm trong doanh nghiệp.
- Khi chuẩn bị sáp nhập (Merge) một Pull Request tự động do AI tạo ra vào nhánh chính của repository.
- Khi cần một đánh giá an ninh hoặc chất lượng khách quan không bị ảnh hưởng bởi ngữ cảnh hội thoại trước đó của coder agent.

## 3. When NOT to Use
- Khi tác vụ chỉ là sửa lỗi chính tả nhỏ 1 ký tự trong file tài liệu không có rủi ro logic.
- Khi hệ thống chỉ có một tác nhân duy nhất hoạt động trong môi trường tài nguyên cực kỳ hạn chế.

## 4. Prerequisites & Input Context
- **Môi trường cách ly:** Reviewer Agent phải được khởi tạo với một ngữ cảnh hội thoại hoàn toàn mới (Clean Context Window), không thừa hưởng lịch sử chat của Coder Agent.
- **Đầu vào thẩm định:** Bản Git Diff chi tiết, tài liệu yêu cầu ban đầu (SPEC/User Request), và báo cáo log kiểm thử thực tế.

## 5. Core Concepts & Taxonomy
- **Confirmation Bias in LLMs:** Hiện tượng một mô hình AI có xu hướng tự khen ngợi hoặc bỏ qua các lỗi tiềm ẩn trong đoạn code mà chính nó vừa tạo ra nếu được yêu cầu tự đánh giá lại trong cùng một hội thoại.
- **Blind Review Protocol:** Reviewer Agent chỉ được cung cấp: Yêu cầu bài toán, Git Diff, và kết quả chạy test. Reviewer không được biết các lời giải thích hay lời hứa hẹn của Coder Agent.
- **Evidence-Based Grading:** Reviewer không được phê duyệt dựa trên nhận định cảm tính; bắt buộc phải có dẫn chứng dòng code vi phạm hoặc kết quả test runner chứng minh đạt tiêu chuẩn.

## 6. Step-by-Step Execution Workflow
1. Coder Agent hoàn thành việc viết code và tạo bản patch Git Diff.
2. Hệ thống tự động đóng gói hồ sơ thẩm định bao gồm: Yêu cầu gốc, Git Diff, và kết quả chạy test tự động.
3. Khởi tạo Reviewer Agent với System Prompt chuyên biệt nhấn mạnh tư duy phản biện, hoài nghi và tập trung tìm kiếm lỗi bảo mật/biên.
4. Reviewer Agent độc lập đọc mã nguồn, phân tích tác động và chạy lại bộ kiểm thử trong môi trường hộp cát.
5. Reviewer Agent chấm điểm theo ma trận 5 tiêu chí: Tính đúng đắn logic, Độ bao phủ kiểm thử, An toàn bảo mật, Tuân thủ kiến trúc, và Hiệu năng.
6. Nếu có vi phạm: Reviewer trả về yêu cầu sửa đổi (Request Changes) kèm theo kịch bản kiểm thử chứng minh lỗi để Coder Agent khắc phục.

## 7. Concrete Examples
### System Prompt chuẩn tắc bảo đảm tính độc lập cho Reviewer Agent:
```markdown
Bạn là Principal Code Reviewer & Security Auditor. Nhiệm vụ của bạn là kiểm tra phản biện độc lập đối với bản Git Diff được cung cấp.

QUY TẮC BẮT BUỘC:
1. KHÔNG chấp nhận các lời khẳng định không có bằng chứng. Hãy tự mình kiểm tra logic từng dòng thay đổi.
2. TÌM KIẾM CÁC TRƯỜNG HỢP BIÊN: Giá trị null, mảng rỗng, chuỗi quá dài, lỗi tràn số, và xung đột bất đồng bộ.
3. RÀ SOÁT BẢO MẬT: Kiểm tra SQL Injection, Command Injection, XSS, rò rỉ secret keys, và vi phạm quyền hạn.
4. ĐỐI SOÁT VỚI YÊU CẦU GỐC: Đảm bảo bản vá giải quyết đúng vấn đề mà không phát sinh thêm code thừa ngoài phạm vi (Scope Creep).

KẾT QUẢ ĐẦU RA BẮT BUỘC THEO ĐỊNH DẠNG JSON:
{
  "decision": "APPROVE" | "REQUEST_CHANGES",
  "confidence_score": 0.0 - 1.0,
  "blocking_issues": [
    {"file": "string", "line": number, "description": "string", "reproduction_test": "string"}
  ],
  "verified_evidence": "string"
}
```

## 8. Anti-Patterns & Common Traps
- **Self-Review Loop:** Dùng cùng một phiên hội thoại và hỏi agent: *"Code bạn vừa viết đã hoàn hảo chưa?"*. Agent hầu như luôn trả lời *"Code đã hoàn hảo và sẵn sàng production"*.
- **Rubber-Stamping Reviewer:** Cấu hình reviewer agent với prompt quá dễ dãi, dẫn đến việc tự động APPROVE mọi thay đổi mà không kiểm tra chi tiết.
- **Subjective Nitpicking without Concrete Proof:** Reviewer từ chối code vì sở thích cá nhân về cách đặt tên biến mà không chỉ ra được lỗi sai kỹ thuật thực tế.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Reviewer Agent bắt buộc phải chạy trên một Context Window hoàn toàn mới và độc lập với Coder Agent.
- **QG-02**: Mọi quyết định `REQUEST_CHANGES` phải đi kèm tệp hoặc dòng mã cụ thể và mô tả kịch bản lỗi.
- **QG-03**: Không có mã nguồn nào được tự động merge nếu chưa có chữ ký số hoặc quyết định `APPROVE` từ Reviewer Agent.

## 10. Security & Safety Boundaries
- Tạo chốt chặn an ninh đa tầng độc lập, ngăn ngừa mã độc hoặc lỗi ngớ ngẩn lọt vào nhánh sản xuất chính.

## 11. Platform Adapters
- **Platforms**: GitHub PR Review Automation, GitLab Merge Request Approvals, Multi-Agent Frameworks.

## 12. Deliverables & Output Artifacts
- Bản thẩm định mã nguồn có cấu trúc JSON/Markdown (`review_decision.json`).
- Danh sách các trường hợp biên hoặc lỗ hổng được phát hiện.
- Bằng chứng kết quả chạy test độc lập của reviewer.

## 13. Related & Complementary Skills
dex-agent-engineering, dex-code-review, dex-multi-agent-orchestration

## 14. Realistic Usage Example
```bash
# Kich hoat Reviewer Agent doc lap tren ban diff git hien tai
python scripts/run_independent_review.py --diff HEAD~1 --spec docs/SPEC.md

# Kiem tra ket qua danh gia cua reviewer
cat docs/reviews/latest_review.json
```
