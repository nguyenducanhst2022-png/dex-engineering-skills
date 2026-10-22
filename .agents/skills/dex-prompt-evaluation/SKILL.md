---
name: dex-prompt-evaluation
description: Systematic prompt engineering, automated prompt evaluation, regression testing for prompts, few-shot optimization, and LLM-as-a-judge scoring frameworks. Use when refining prompt templates, preventing prompt regressions, or validating output quality.
---

# dex-prompt-evaluation

## 1. Purpose & Scope
Thiết kế, tối ưu hóa và kiểm thử tự động các mẫu câu lệnh (Prompt Engineering & Automated Evaluation); áp dụng các kỹ thuật Few-Shot, Chain-of-Thought (CoT), thiết lập bộ bài kiểm thử hồi quy cho prompt (Prompt Regression Testing) và áp dụng cơ chế đánh giá tự động bằng mô hình (LLM-as-a-Judge) để đảm bảo chất lượng phản hồi luôn ổn định và không bị suy thoái khi cập nhật prompt.

## 2. When to Use
- Khi sửa đổi nội dung System Prompt để cải tiến một tính năng nhưng lại vô tình làm hỏng các tính năng khác mà prompt từng làm tốt trước đó (Prompt Regression).
- Khi câu trả lời của mô hình AI không nhất quán, hay lan man hoặc không tuân thủ đúng giọng điệu (Tone of Voice) yêu cầu.
- Khi cần so sánh định lượng xem phiên bản Prompt v2 có thực sự tốt hơn Prompt v1 hay không.

## 3. When NOT to Use
- Đánh giá tốc độ truy vấn cơ sở dữ liệu hoặc trích xuất vector (dùng `dex-retrieval-evaluation`).
- Kiểm thử mã nguồn thông thường bằng unit test truyền thống không có yếu tố AI sinh ngữ nghĩa.

## 4. Prerequisites & Input Context
**Đầu vào cần thiết:**
- Mẫu prompt hiện tại và mẫu prompt mới dự kiến cập nhật.
- Tập dữ liệu kiểm thử các trường hợp đầu vào đa dạng (Test Cases: Normal cases, Edge cases, Adversarial injection cases).
- Tiêu chí đánh giá chất lượng (Rubrics: Độ chính xác, Tính súc tích, Giọng điệu, Định dạng).

**Điều kiện tiên quyết:**
- Có công cụ chạy kiểm thử prompt tự động (Promptfoo, DeepEval, LangSmith, hoặc custom Python test suite).
- Có khóa API để gọi mô hình giám khảo (Judge LLM: ví dụ GPT-4o) chấm điểm theo Rubric.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**: Nắm vững cơ chế vận hành theo chuẩn Agent Skills, tuân thủ nghiêm ngặt tính xác định và ranh giới trách nhiệm.
- **Quy tắc quyết định kỹ thuật**:
- **Prompt Phải Được Quản Lý Như Mã Nguồn (Prompt-as-Code)**: Tuyệt đối không chỉnh sửa prompt trực tiếp trên web console; mọi prompt phải được lưu trong Git repository, có versioning và được review qua Pull Request.
- **Không Thay Đổi Prompt Dựa Trên Cảm Tính 1 Trường Hợp**: Không bao giờ sửa toàn bộ prompt chỉ vì một câu trả lời duy nhất của khách hàng mà không chạy lại toàn bộ test suite kiểm tra tác động diện rộng.
- **Tối Giản Token Trong Prompt**: Luôn loại bỏ các từ ngữ dư thừa, lặp lại trong prompt để tiết kiệm chi phí và giữ sự tập trung cao nhất cho mô hình.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Prompt mới sửa được lỗi này nhưng lại sinh ra lỗi khác**: Đạt điểm cao ở câu hỏi mới nhưng lại trả lời sai 5 câu hỏi cũ -> Khắc phục: Bộ kiểm thử hồi quy tự động chặn merge PR vì điểm hồi quy bị giảm.
- **Mô hình giám khảo chấm điểm bất định (Flaky Evaluation)**: Lúc cho 4 điểm, lúc cho 2 điểm -> Khắc phục: Cung cấp barem chấm điểm cực kỳ chi tiết (Detailed Rubric with Examples) và đặt `temperature: 0.0` cho mô hình giám khảo.

## 6. Step-by-Step Execution Workflow
1. Định nghĩa bộ tiêu chí chấm điểm (Evaluation Rubrics): Xác định thang điểm từ 1 đến 5 hoặc PASS/FAIL cho các khía cạnh: Tính đúng đắn, Tính an toàn, Không lan man.
2. Thiết lập tập dữ liệu kiểm thử (Prompt Test Cases) bao quát cả các tình huống biên phức tạp và các câu hỏi bẫy.
3. Cấu hình kiểm thử tự động với Promptfoo hoặc DeepEval:
   - *Assertions dựa trên quy tắc*: Đầu ra bắt buộc phải chứa từ khóa X, không được chứa từ khóa Y, độ dài < 200 từ, format JSON hợp lệ.
   - *Assertions dựa trên ngữ nghĩa (LLM Judge)*: Chấm điểm xem câu trả lời có phản ánh đúng ý đồ của người dùng hay không.
4. Chạy kiểm thử song song giữa Prompt Cũ và Prompt Mới trên cùng một tập dữ liệu.
5. Phân tích kết quả: So sánh tỷ lệ PASS, điểm số trung bình, lượng token tiêu tốn và chi phí USD.
6. Chỉ chấp nhận hợp nhất (merge) Prompt mới khi điểm số tổng thể tăng và không làm rớt bất kỳ bài test hồi quy quan trọng nào.

## 7. Concrete Examples
### Ví dụ triển khai chuẩn mực:
```yaml
# promptfooconfig.yaml (Kiểm thử prompt tự động)
prompts:
  - file://prompts/summarizer_v1.txt
  - file://prompts/summarizer_v2.txt
providers:
  - openai:gpt-4o-mini
tests:
  - vars:
      input: 'Hợp đồng này quy định bên A thanh toán cho bên B 50 triệu vào ngày 1/11.'
    assert:
      - type: contains-json
      - type: javascript
        value: 'output.amount === 50000000'
      - type: llm-rubric
        value: 'Đầu ra tóm tắt ngắn gọn dưới 30 từ và nêu bật đúng số tiền.'
```

### Lệnh xác minh & thực thi:
- Chạy bộ kiểm thử prompt tự động với promptfoo: `npx promptfoo eval`
- Xem báo cáo trực quan so sánh prompt: `npx promptfoo view`
- Chạy kiểm thử prompt bằng Python: `pytest tests/prompts/test_prompts.py`

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước kiểm tra biên và giả định hệ thống luôn ở trạng thái lý tưởng.
- **Anti-Pattern 2**: Không ghi nhận nhật ký kiểm toán hoặc bỏ qua việc xử lý ngoại lệ lúc runtime.
- **Trap**: Bỏ qua các rào chắn an toàn hoặc cố tình chạy script không qua kiểm thử tự động.

## 9. Quality Gates & Acceptance Criteria
- QG-01: 100% các prompt đều có file kiểm thử tương ứng trong thư mục `tests/prompts/`.
- QG-05: Tỷ lệ PASS của bộ bài kiểm thử prompt đạt tối thiểu >= 90%.
- QG-06: 0 trường hợp lỗi hồi quy nghiêm trọng (Critical Regression) trên tập dữ liệu kiểm thử cốt lõi.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động trước khi coi là hoàn thành.

## 10. Security & Safety Boundaries
- Bộ bài kiểm thử bắt buộc phải bao gồm các ca kiểm thử tấn công (Jailbreak / Adversarial Prompts) để xác minh prompt không bị bẻ khóa.
- Không bao giờ thực thi mã nguồn hoặc thay đổi cấu hình trên môi trường sản xuất mà thiếu cơ chế rollback an toàn.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Có thể kích hoạt trực tiếp từ terminal hoặc extension tương thích trong VS Code / Cursor / Windsurf.

## 12. Deliverables & Output Artifacts
- File cấu hình kiểm thử prompt (`promptfooconfig.yaml` hoặc `test_prompts.py`).
- File mẫu prompt có versioning (`prompts/support_assistant_v2.txt`).
- Bảng báo cáo so sánh kết quả kiểm thử định lượng.

## 13. Related & Complementary Skills
- `dex-development-workflow`: Quy trình phát triển tiêu chuẩn.
- `dex-code-verification`: Xác minh chất lượng và tính đúng đắn của mã nguồn.
- `dex-master-orchestrator`: Bộ điều phối trung tâm kết nối kỹ năng này với các kỹ năng khác trong hệ thống.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư hoặc AI Agent tiếp nhận yêu cầu liên quan đến **dex-prompt-evaluation**.
1. Đọc kỹ đầu vào và các ràng buộc kỹ thuật tại mục 4.
2. Thực thi tuần tự 6 bước trong Workflow tại mục 6.
3. Chạy các lệnh kiểm chứng tại mục 7 và đối chiếu với Quality Gates tại mục 9.
4. Đóng gói deliverables theo danh sách tại mục 12 và báo cáo kết quả kèm bằng chứng xác thực.
