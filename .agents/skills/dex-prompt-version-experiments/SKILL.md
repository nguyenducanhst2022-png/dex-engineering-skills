---
name: dex-prompt-version-experiments
description: Manage prompt versions in Git, execute automated regression evaluations against golden benchmarks, and conduct prompt A/B testing. Use when iterating system prompts or protecting LLM behavior against regression.
---

# dex-prompt-version-experiments

## 1. Purpose & Scope
Quản trị vòng đời và phiên bản hóa câu lệnh mẫu (Prompt Versioning as Code); lưu vết lịch sử prompt trong Git, tự động hóa kiểm thử hồi quy (Prompt Regression Testing) trên bộ dữ liệu chuẩn (Golden Dataset), và đo lường định lượng sự cải thiện chất lượng trước khi triển khai lên môi trường sản xuất.

## 2. When to Use
- Khi lập trình viên thay đổi System Prompt hoặc Few-shot examples và cần chứng minh thay đổi đó không làm hỏng các tính năng cũ.
- Khi tiến hành thử nghiệm A/B Testing giữa hai phiên bản prompt trên môi trường thử nghiệm.
- Khi cần rollback nhanh chóng về phiên bản prompt cũ khi phát hiện sự cố trên môi trường sản xuất.

## 3. When NOT to Use
- Khi câu lệnh chỉ là câu chat tự do dùng một lần của người dùng cuối.
- Khi logic nghiệp vụ được giải quyết bằng mã nguồn truyền thống mà không sử dụng LLM.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Thư mục lưu trữ prompt (`prompts/`), tập dữ liệu chuẩn mực (Golden Dataset gồm các cặp input/expected_output), công cụ đo lường tự động (LLM-as-a-judge hoặc rule-based assertion).
- **Quyền hạn truy cập:** Quyền ghi vào thư mục prompt và quyền gọi API mô hình để chạy đánh giá.

## 5. Core Concepts & Taxonomy
- **Prompt-as-Code:** Coi prompt như mã nguồn phần mềm: có phiên bản SemVer, được lưu trong Git, có quy trình code review và CI kiểm thử tự động.
- **Golden Regression Suite:** Tập hợp các ca kiểm thử kinh điển đại diện cho các hành vi bắt buộc của hệ thống (edge cases, an toàn, định dạng JSON).
- **Pass Rate Delta ($\Delta$):** Sự thay đổi về tỷ lệ vượt qua bài test giữa prompt mới và prompt cũ: bắt buộc $\Delta_{pass} \ge 0$ và 0 lỗi hồi quy nghiêm trọng (Zero Regressions on Critical Cases).

## 6. Step-by-Step Execution Workflow
1. Lưu trữ các prompt trong kho mã nguồn dưới dạng tệp có cấu trúc (ví dụ: `prompts/coder_agent/v1.2.0.yaml`).
2. Khi có đề xuất tối ưu hóa prompt: tạo branch mới và cập nhật nội dung prompt thành phiên bản mới (ví dụ: `v1.3.0.yaml`).
3. Kích hoạt CI tự động chạy bộ kiểm thử hồi quy: nạp 100 câu hỏi từ Golden Dataset và gọi model với cả hai phiên bản prompt cũ và mới.
4. Đánh giá kết quả bằng bộ thẩm định tự động (chấm điểm định dạng, độ chính xác nội dung, và kiểm tra an toàn).
5. Lập bảng so sánh đối đầu (Win/Tie/Loss matrix) giữa hai phiên bản prompt.
6. Chỉ cho phép merge pull request nếu phiên bản prompt mới đạt tỷ lệ thắng áp đảo và không có lỗi hồi quy trên các ca kiểm thử bảo mật.

## 7. Concrete Examples
### Ví dụ tệp định nghĩa Prompt-as-Code (`prompts/extractor/v2.1.0.yaml`):
```yaml
name: entity_extractor_prompt
version: "2.1.0"
author: "staff-ai-engineer"
model: "gpt-4o"
temperature: 0.1
system_prompt: |
  You are an expert enterprise data extraction engine.
  Extract all technical entities from the provided input text.
  Respond STRICTLY with valid JSON following this schema:
  {"entities": [{"name": string, "category": string, "confidence": float}]}
few_shot_examples:
  - input: "PostgreSQL 16 was released with improved query planning."
    output: '{"entities": [{"name": "PostgreSQL 16", "category": "DATABASE", "confidence": 0.99}]}'
metadata:
  changelog: "Added few-shot example for database version extraction"
```

## 8. Anti-Patterns & Common Traps
- **Hardcoded String Prompts:** Nhúng trực tiếp chuỗi prompt dài hàng nghìn ký tự vào giữa mã nguồn backend khiến không thể test độc lập hoặc theo dõi lịch sử thay đổi.
- **Vibe-Based Prompting:** Sửa prompt rồi tự thử 1-2 câu hỏi thủ công thấy 'có vẻ ổn' (vibe check) rồi deploy thẳng lên production gây sập tính năng của khách hàng khác.
- **Untracked Production Prompts:** Sửa prompt trực tiếp trên web UI của nhà cung cấp LLM mà không lưu vết về Git repository.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Tệp prompt được định nghĩa theo chuẩn YAML Prompt-as-Code có đầy đủ số phiên bản SemVer.
- **QG-04**: Tỷ lệ vượt qua bài test hồi quy trên Golden Dataset của prompt mới đạt tối thiểu bằng hoặc cao hơn phiên bản cũ.
- **QG-13**: 100% câu trả lời sinh ra từ prompt mới tuân thủ đúng định dạng JSON schema bắt buộc.

## 10. Security & Safety Boundaries
- Quét kiểm tra bảo mật: đảm bảo prompt mới không vô tình làm suy yếu các chỉ thị phòng chống Jailbreak hoặc làm lộ System Instructions.
- Không lưu thông tin nhạy cảm hoặc bí mật API trong nội dung của các few-shot examples.

## 11. Platform Adapters
- **Prompt Tools**: LangSmith, Promptfoo, DeepEval, OpenPipe.
- **CI Integration**: GitHub Actions prompt regression matrix.

## 12. Deliverables & Output Artifacts
- Tệp đặc tả Prompt-as-Code chuẩn hóa có quản lý phiên bản Git.
- Báo cáo kết quả kiểm thử hồi quy so sánh giữa phiên bản mới và cũ (A/B Test Report).
- Bảng đối soát Win/Loss matrix trên Golden Dataset.

## 13. Related & Complementary Skills
dex-llm-evaluation-dataset-design, dex-ai-safety-red-teaming, dex-semantic-version-automation

## 14. Realistic Usage Example
```powershell
# Chạy bộ kiểm thử hồi quy tự động so sánh hai phiên bản prompt
python scripts/evaluate_prompt_experiment.py --baseline prompts/v1.yaml --candidate prompts/v2.yaml
```
