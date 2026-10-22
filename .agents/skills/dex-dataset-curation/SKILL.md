---
name: dex-dataset-curation
description: Curate, clean, deduplicate, filter, and synthesize high-quality training and evaluation datasets for LLM fine-tuning and domain adaptation. Use when preparing fine-tuning data, removing contaminated samples, or curating synthetic datasets.
---

# dex-dataset-curation

## 1. Purpose & Scope
Thu thập, làm sạch, khử trùng lặp (Deduplication), kiểm duyệt chất lượng và sinh dữ liệu tổng hợp (Synthetic Data Generation) để xây dựng các tập dữ liệu huấn luyện (Training Sets) và kiểm thử (Evaluation Sets) chất lượng cao phục vụ việc Tinh chỉnh mô hình (Fine-tuning) hoặc thích ứng miền (Domain Adaptation); loại bỏ các mẫu dữ liệu nhiễm độc (Data Contamination) và đảm bảo cân bằng phân phối.

## 2. When to Use
- Khi chuẩn bị dữ liệu để Fine-tune mô hình mã nguồn mở (như Llama 3 hoặc Mistral) cho một bài toán chuyên ngành.
- Khi tập dữ liệu huấn luyện chứa nhiều bản ghi rác, định dạng lộn xộn, câu trả lời bị cụt ngủn hoặc chứa thông tin sai lệch.
- Khi cần tạo thêm hàng nghìn dữ liệu mẫu chất lượng cao từ một số ít dữ liệu hạt giống ban đầu (Few-shot Seeds) bằng kỹ thuật sinh dữ liệu tổng hợp.

## 3. When NOT to Use
- Xử lý làm sạch dữ liệu bảng kinh doanh thông thường trong kho dữ liệu (dùng `dex-data-quality-audits`).
- Thu thập web thông thường mà không nhằm mục đích huấn luyện AI.

## 4. Prerequisites & Input Context
**Đầu vào cần thiết:**
- Dữ liệu thô ban đầu (Lịch sử chat hỗ trợ khách hàng, tài liệu nội bộ, ticket giải quyết lỗi).
- Định dạng đích cần xuất (JSONL theo chuẩn OpenAI Fine-Tuning hoặc ShareGPT format).
- Bộ tiêu chuẩn kiểm duyệt chất lượng dữ liệu (Quality Criteria: Độ dài, Ngữ pháp, Độ an toàn).

**Điều kiện tiên quyết:**
- Có công cụ xử lý ngôn ngữ tự nhiên và tính toán độ tương đồng văn bản (MinHash LSH, FastText, Python Pandas/Polars).
- Có môi trường kiểm duyệt dữ liệu an toàn không để lộ dữ liệu mật của khách hàng.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**: Nắm vững cơ chế vận hành theo chuẩn Agent Skills, tuân thủ nghiêm ngặt tính xác định và ranh giới trách nhiệm.
- **Quy tắc quyết định kỹ thuật**:
- **Chất Lượng Luôn Quan Trọng Hơn Số Lượng (Quality > Quantity)**: 1,000 mẫu dữ liệu sạch và được kiểm duyệt cẩn thận sẽ mang lại hiệu quả Fine-tuning vượt trội so với 100,000 mẫu dữ liệu rác cào bừa bãi.
- **Tuyệt Đối Không Để Lộ Dữ Liệu Kiểm Thử (No Contamination)**: Bắt buộc phải kiểm tra để đảm bảo không có câu hỏi nào trong tập Validation Set xuất hiện trong tập Train Set.
- **Định Dạng JSONL Khắt Khe**: Mỗi dòng trong file JSONL phải là một đối tượng JSON độc lập, không có lỗi xuống dòng sai quy cách.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Mô hình sau khi Fine-tune tự động in thông tin cá nhân khách hàng cũ**: Do khâu làm sạch PII bị sót -> Khắc phục: Sử dụng thư viện chuyên dụng Microsoft Presidio kết hợp regex chuyên sâu để kiểm tra 2 lớp.
- **File nạp lên OpenAI báo lỗi cú pháp dòng 450**: Do chứa ký tự escape không hợp lệ -> Khắc phục: Viết script validate toàn bộ file JSONL bằng thư viện `json.loads` trước khi upload.

## 6. Step-by-Step Execution Workflow
1. Thu thập dữ liệu từ các nguồn thực tế: Lọc lấy các cuộc hội thoại được đánh giá 5 sao từ người dùng.
2. Làm sạch văn bản thô: Loại bỏ HTML tags, emoji rác, ký tự Unicode hỏng, chuẩn hóa khoảng trắng.
3. Khử trùng lặp thông minh (Fuzzy Deduplication): Sử dụng thuật toán MinHash LSH để loại bỏ các câu hỏi/câu trả lời gần giống nhau (> 85% tương đồng) nhằm tránh mô hình bị học vẹt (Overfitting).
4. Khử định danh (Anonymization & De-identification): Quét và thay thế toàn bộ thông tin PII (Tên thật, Email, Số điện thoại, Số thẻ ngân hàng) bằng các nhãn giả lập (`[TEN_KHACH_HANG]`, `[SO_DIEN_THOAI]`).
5. Lọc chất lượng bằng LLM (LLM-based Quality Filtering): Đánh giá từng cặp hội thoại xem câu trả lời có hữu ích, logic và đầy đủ hay không; loại bỏ các mẫu dưới 4/5 điểm.
6. Sinh dữ liệu tổng hợp (Synthetic Augmentation): Với các kịch bản hiếm gặp (Edge cases), dùng mô hình mạnh (như Claude 3.5 Sonnet) để sinh thêm các biến thể câu hỏi khác nhau.
7. Phân chia tập dữ liệu: Chia ngẫu nhiên có phân tầng thành Tập huấn luyện (Train Set: 85%) và Tập kiểm thử (Validation Set: 15%), đảm bảo không có sự rò rỉ dữ liệu giữa 2 tập.
8. Xuất file định dạng JSONL chuẩn mực và kiểm tra cú pháp trước khi nạp vào quy trình Fine-tuning.

## 7. Concrete Examples
### Ví dụ triển khai chuẩn mực:
```json
// data/fine_tune_train.jsonl (Định dạng OpenAI Chat Fine-Tuning chuẩn)
{"messages": [{"role": "system", "content": "Bạn là trợ lý kỹ thuật hỗ trợ giải quyết sự cố mạng."}, {"role": "user", "content": "Router nhấp nháy đèn đỏ là bị sao?"}, {"role": "assistant", "content": "Đèn đỏ nhấp nháy thường báo hiệu mất kết nối tín hiệu quang từ nhà mạng. Bạn vui lòng thử khởi động lại thiết bị trong 30 giây; nếu vẫn đỏ, hãy liên hệ tổng đài để kiểm tra đường cáp bên ngoài."}]}
```

### Lệnh xác minh & thực thi:
- Chạy script làm sạch và chuẩn hóa dataset: `python scripts/curate_dataset.py --input raw_data.csv --output clean_train.jsonl`
- Kiểm tra cú pháp định dạng file Fine-Tuning: `npx openai tools fine_tunes.prepare_data -f clean_train.jsonl`
- Kiểm tra trùng lặp dữ liệu: `python scripts/check_duplicates.py clean_train.jsonl`

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước kiểm tra biên và giả định hệ thống luôn ở trạng thái lý tưởng.
- **Anti-Pattern 2**: Không ghi nhận nhật ký kiểm toán hoặc bỏ qua việc xử lý ngoại lệ lúc runtime.
- **Trap**: Bỏ qua các rào chắn an toàn hoặc cố tình chạy script không qua kiểm thử tự động.

## 9. Quality Gates & Acceptance Criteria
- QG-03: 100% các dòng trong file dataset đạt chuẩn JSONL hợp lệ của OpenAI / Anthropic format.
- QG-07: 0 thông tin PII thực tế nào sót lại trong tập dữ liệu sau khi chạy qua bộ lọc làm sạch.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động trước khi coi là hoàn thành.

## 10. Security & Safety Boundaries
- Dữ liệu huấn luyện phải được lưu trữ trong thư mục được bảo vệ và có hợp đồng đồng thuận sử dụng dữ liệu từ người dùng (User Consent).
- Không bao giờ thực thi mã nguồn hoặc thay đổi cấu hình trên môi trường sản xuất mà thiếu cơ chế rollback an toàn.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Có thể kích hoạt trực tiếp từ terminal hoặc extension tương thích trong VS Code / Cursor / Windsurf.

## 12. Deliverables & Output Artifacts
- Tập dữ liệu huấn luyện sạch (`data/fine_tune_train.jsonl`).
- Tập dữ liệu kiểm thử độc lập (`data/fine_tune_val.jsonl`).
- Báo cáo thống kê phân phối độ dài token và từ vựng của dataset.

## 13. Related & Complementary Skills
- `dex-development-workflow`: Quy trình phát triển tiêu chuẩn.
- `dex-code-verification`: Xác minh chất lượng và tính đúng đắn của mã nguồn.
- `dex-master-orchestrator`: Bộ điều phối trung tâm kết nối kỹ năng này với các kỹ năng khác trong hệ thống.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư hoặc AI Agent tiếp nhận yêu cầu liên quan đến **dex-dataset-curation**.
1. Đọc kỹ đầu vào và các ràng buộc kỹ thuật tại mục 4.
2. Thực thi tuần tự 6 bước trong Workflow tại mục 6.
3. Chạy các lệnh kiểm chứng tại mục 7 và đối chiếu với Quality Gates tại mục 9.
4. Đóng gói deliverables theo danh sách tại mục 12 và báo cáo kết quả kèm bằng chứng xác thực.
