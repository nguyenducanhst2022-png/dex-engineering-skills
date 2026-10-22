---
name: dex-model-evaluation
description: Benchmark and evaluate foundation LLMs and fine-tuned models on task-specific datasets, measuring accuracy, latency, cost per token, and hallucination rates. Use when selecting LLM providers, validating model upgrades, or comparing fine-tuned models.
---

# dex-model-evaluation

## 1. Purpose & Scope
Đánh giá, so sánh và chuẩn đối sánh (Benchmarking & Model Evaluation) giữa các mô hình ngôn ngữ lớn (OpenAI, Anthropic, Gemini, Llama 3, Mistral, mô hình Fine-tuned); đo lường toàn diện dựa trên 4 trục cốt lõi: Tính đúng đắn (Accuracy / F1), Độ trễ phản hồi (Latency / TTFT), Tỷ lệ ảo giác (Hallucination Rate) và Chi phí trên mỗi 1,000 requests, giúp đưa ra quyết định lựa chọn mô hình tối ưu cho từng bài toán.

## 2. When to Use
- Khi cần quyết định nên sử dụng mô hình đắt tiền (như GPT-4o) hay mô hình nhẹ giá rẻ (như GPT-4o-mini, Claude 3.5 Haiku) cho một tính năng cụ thể.
- Khi nhà cung cấp phát hành phiên bản mô hình mới và cần xác minh xem việc nâng cấp có làm gãy tính năng hiện tại không.
- Khi đánh giá xem việc Fine-tuning mô hình nguồn mở (Llama 3) có mang lại kết quả tốt hơn mô hình thương mại đóng hay không.

## 3. When NOT to Use
- Tinh chỉnh nội dung câu chữ của một câu lệnh đơn lẻ (dùng `dex-prompt-evaluation`).
- Đo lường chỉ số hiệu năng mạng thông thường (dùng `dex-performance-optimization`).

## 4. Prerequisites & Input Context
**Đầu vào cần thiết:**
- Danh sách các mô hình ứng viên cần so sánh.
- Tập dữ liệu benchmark chuẩn đặc thù cho nghiệp vụ (Task-specific Benchmark Dataset: tối thiểu 200 - 500 mẫu).
- Ma trận trọng số quyết định (Accuracy weight, Latency weight, Cost weight).

**Điều kiện tiên quyết:**
- Có quyền truy cập API hoặc môi trường chạy suy luận cục bộ (Ollama / vLLM) cho các mô hình ứng viên.
- Có công cụ đo lường tự động (EleutherAI LM Eval Harness, DeepEval, hoặc custom benchmark harness).

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**: Nắm vững cơ chế vận hành theo chuẩn Agent Skills, tuân thủ nghiêm ngặt tính xác định và ranh giới trách nhiệm.
- **Quy tắc quyết định kỹ thuật**:
- **Quy Tắc Mô Hình Nhỏ Nhất Khả Thi (Smallest Viable Model)**: Luôn ưu tiên chọn mô hình nhỏ nhất, rẻ nhất và nhanh nhất mà vẫn đáp ứng được ngưỡng chất lượng tối thiểu yêu cầu (ví dụ: nếu model rẻ $0.15/1M tokens đạt 92% độ chính xác, trong khi model đắt $5/1M tokens đạt 94%, hãy chọn model rẻ).
- **Đo Lường Trên Dữ Liệu Thực Tế Riêng**: Không bao giờ tin vào các bảng điểm benchmark tổng hợp trên mạng (như MMLU, GSM8K); bắt buộc phải tự đo lường trên tập dữ liệu nghiệp vụ thực tế của công ty.
- **Kiểm Soát Tính Ổn Định Phiên Bản**: Ghim chặt chuỗi định danh phiên bản cụ thể của mô hình (ví dụ: `gpt-4o-2024-08-06`) thay vì dùng alias chung chung `gpt-4o` để tránh việc nhà cung cấp tự ý cập nhật ngầm làm đổi hành vi.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Mô hình mới đạt điểm cao nhưng sinh token quá chậm**: Người dùng phải chờ 4 giây mới thấy chữ đầu tiên -> Khắc phục: Đưa chỉ số TTFT (Time to First Token) thành tiêu chí loại trừ bắt buộc (< 1.2s).
- **Mô hình nhỏ bị ảo giác ở các trường hợp biên**: -> Khắc phục: Áp dụng kiến trúc định tuyến thông minh (Router): Các câu hỏi dễ dùng mô hình nhỏ, khi phát hiện độ khó cao thì tự động chuyển sang mô hình lớn.

## 6. Step-by-Step Execution Workflow
1. Chuẩn bị tập dữ liệu đánh giá đặc thù của dự án: Bao gồm đầu vào thực tế và đầu ra chuẩn mực do con người xác thực.
2. Thiết lập kịch bản benchmark tự động gửi cùng một tập câu hỏi đến tất cả các mô hình ứng viên trong cùng điều kiện.
3. Đo lường chỉ số chất lượng: Tỷ lệ chính xác (Accuracy), F1-Score, hoặc điểm số chấm từ Giám khảo LLM độc lập.
4. Đo lường chỉ số kỹ thuật: Thời gian trả token đầu tiên (TTFT - Time to First Token), Tốc độ sinh token (Tokens per Second), Tỷ lệ lỗi (Error rate / 5xx).
5. Tính toán chi phí: Chi phí trên 1,000 lượt yêu cầu thực tế dựa trên bảng giá token của từng nhà cung cấp.
6. Lập ma trận Pareto đối chiếu giữa Chất lượng và Chi phí/Độ trễ.
7. Đưa ra kết luận lựa chọn mô hình tối ưu theo tiêu chí ROI (Return on Investment).

## 7. Concrete Examples
### Ví dụ triển khai chuẩn mực:
```markdown
# MODEL EVALUATION SUMMARY: Customer Support Ticket Triage

| Model | Accuracy | p95 Latency | Cost / 1k Requests | Verdict |
|:---|:---:|:---:|:---:|:---|
| **GPT-4o** | 94.2% | 1.85s | $7.50 | Quá đắt cho quy mô lớn |
| **Claude 3.5 Haiku** | 93.8% | 0.82s | $0.80 | **ĐƯỢC CHỌN (Best Speed & ROI)** |
| **Llama-3-8B-Local** | 86.1% | 0.45s | $0.20 (Infra) | Chưa đạt ngưỡng chất lượng 90% |
```

### Lệnh xác minh & thực thi:
- Chạy script benchmark đa mô hình: `python scripts/benchmark_models.py --models gpt-4o-mini,claude-3-5-haiku --dataset data/eval.json`
- Xuất bảng so sánh tổng hợp: `python scripts/generate_model_report.py`
- Kiểm tra chi phí ước tính trên 1 triệu lượt gọi.

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước kiểm tra biên và giả định hệ thống luôn ở trạng thái lý tưởng.
- **Anti-Pattern 2**: Không ghi nhận nhật ký kiểm toán hoặc bỏ qua việc xử lý ngoại lệ lúc runtime.
- **Trap**: Bỏ qua các rào chắn an toàn hoặc cố tình chạy script không qua kiểm thử tự động.

## 9. Quality Gates & Acceptance Criteria
- QG-04: Mô hình được chọn phải đáp ứng SLA thời gian phản hồi (p95 latency < 2.0s).
- QG-10: Có bảng số liệu đánh giá chi tiết so sánh Accuracy, Latency, Cost giữa tối thiểu 2 mô hình ứng viên.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động trước khi coi là hoàn thành.

## 10. Security & Safety Boundaries
- Khi gửi dữ liệu đánh giá lên các nhà cung cấp mô hình thương mại, đảm bảo dữ liệu đã được làm sạch và nhà cung cấp có cam kết không sử dụng dữ liệu khách hàng để huấn luyện (Zero Data Retention Policy).
- Không bao giờ thực thi mã nguồn hoặc thay đổi cấu hình trên môi trường sản xuất mà thiếu cơ chế rollback an toàn.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Có thể kích hoạt trực tiếp từ terminal hoặc extension tương thích trong VS Code / Cursor / Windsurf.

## 12. Deliverables & Output Artifacts
- Script chạy benchmark tự động (`scripts/benchmark_models.py`).
- Báo cáo đánh giá so sánh mô hình (`docs/model_evaluation_report.md`).
- Cấu hình chỉ định model được chọn trong file môi trường dự án.

## 13. Related & Complementary Skills
- `dex-development-workflow`: Quy trình phát triển tiêu chuẩn.
- `dex-code-verification`: Xác minh chất lượng và tính đúng đắn của mã nguồn.
- `dex-master-orchestrator`: Bộ điều phối trung tâm kết nối kỹ năng này với các kỹ năng khác trong hệ thống.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư hoặc AI Agent tiếp nhận yêu cầu liên quan đến **dex-model-evaluation**.
1. Đọc kỹ đầu vào và các ràng buộc kỹ thuật tại mục 4.
2. Thực thi tuần tự 6 bước trong Workflow tại mục 6.
3. Chạy các lệnh kiểm chứng tại mục 7 và đối chiếu với Quality Gates tại mục 9.
4. Đóng gói deliverables theo danh sách tại mục 12 và báo cáo kết quả kèm bằng chứng xác thực.
