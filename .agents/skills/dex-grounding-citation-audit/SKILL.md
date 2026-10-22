---
name: dex-grounding-citation-audit
description: Audit, score, and verify factual grounding and citation integrity in RAG systems, detecting hallucinations and ungrounded claims using NLI and LLM-as-a-judge frameworks. Use when delivering high-stakes answers in legal, medical, or financial domains.
---

# dex-grounding-citation-audit

## 1. Purpose & Scope
Kiểm toán, chấm điểm và xác minh tính có căn cứ thực tế (Factual Grounding) và tính toàn vẹn của trích dẫn nguồn (Citation Integrity) trong các hệ thống RAG; phát hiện và loại bỏ các ảo giác (Hallucinations) và các tuyên bố vô căn cứ bằng mô hình Natural Language Inference (NLI) và khung đánh giá LLM-as-a-Judge chuyên sâu.

## 2. When to Use
- Ứng dụng AI trả lời các câu hỏi pháp lý, y tế, tài chính hoặc chính sách nội bộ yêu cầu độ chính xác 100%.
- Xuất hiện tình trạng LLM trích dẫn nguồn giả (Fake citations: trích dẫn tới tài liệu không hề chứa thông tin đó).
- Cần đo lường chỉ số Faithfulness và Groundedness trước khi phát hành tính năng RAG cho khách hàng.

## 3. When NOT to Use
- Không áp dụng kiểm tra trích dẫn khắt khe cho các tác vụ sáng tạo nội dung tiếp thị hoặc brainstorm ý tưởng.
- Không phụ thuộc vào một model duy nhất để vừa tự sinh câu trả lời vừa tự chấm điểm chính mình mà không có cơ chế đối soát độc lập.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Câu truy vấn của người dùng (Query).
- Các đoạn văn bản gốc được truy hồi làm ngữ cảnh (Retrieved Contexts).
- Câu trả lời kèm các chỉ mục trích dẫn do LLM sinh ra (Answer with Citations).
- **Điều kiện tiên quyết**:
- Có khung đánh giá chất lượng RAG (Ragas, TruLens, DeepEval hoặc mô hình NLI cục bộ).

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Grounding / Faithfulness: Tỉ lệ phần trăm các tuyên bố (Claims) trong câu trả lời có thể được chứng minh trực tiếp dựa trên ngữ cảnh cung cấp. Điểm = 1.0 nghĩa là không có bất kỳ ảo giác nào.
- Citation Recall & Precision:
  + Citation Precision: Mọi câu được trích dẫn [1] thì tài liệu [1] phải thực sự hỗ trợ câu đó.
  + Citation Recall: Mọi thông tin quan trọng lấy từ tài liệu phải được gắn trích dẫn đầy đủ.
- Claim Decomposition: Tách câu trả lời thành từng mệnh đề độc lập (Atomic Claims) và kiểm tra từng mệnh đề đối với ngữ cảnh nguồn bằng mô hình NLI (Entailment vs Neutral/Contradiction).
- **Quy tắc quyết định kỹ thuật**:
- Nếu Faithfulness Score < 0.90: từ chối hiển thị câu trả lời và thông báo 'Tài liệu không đủ thông tin để trả lời an toàn'.
- Bất kỳ trích dẫn nào không map được tới văn bản gốc trong context phải bị tự động gỡ bỏ hoặc gắn cờ cảnh báo.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- LLM tự bịa ra một điều luật hoặc một con số lãi suất không có trong tài liệu và gắn kèm trích dẫn giả mạo `[Doc 1]`, khiến người dùng tin tưởng mù quáng.

## 6. Step-by-Step Execution Workflow
1. Thu thập bộ ba (Query, Retrieved Context, Generated Answer).
2. Sử dụng thuật toán Claim Decomposition tách câu trả lời thành danh sách các mệnh đề nguyên tử.
3. Chạy mô hình NLI phân loại từng mệnh đề: `Entailed` (Có căn cứ), `Contradicted` (Mâu thuẫn), hoặc `Neutral` (Không có bằng chứng).
4. Kiểm tra tính hợp lệ của từng thẻ trích dẫn `[1]`, `[2]` tương ứng với đoạn văn bản gốc.
5. Xuất báo cáo Factual Grounding Score và chặn các câu trả lời có nguy cơ ảo giác cao.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```python
# Kiểm toán Grounding bằng Ragas Framework
from ragas.metrics import faithfulness
from ragas import evaluate
from datasets import Dataset

data = {
    "question": ["Chính sách hoàn tiền của công ty trong bao nhiêu ngày?"],
    "contexts": [["Khách hàng có quyền yêu cầu hoàn tiền trong vòng 30 ngày kể từ ngày mua hàng."]],
    "answer": ["Bạn có thể hoàn tiền trong 30 ngày [1], và được tặng thêm voucher 100k [2]."]
}

dataset = Dataset.from_dict(data)
# Mệnh đề 'tặng thêm voucher 100k' không có trong context sẽ bị đánh tụt điểm faithfulness
result = evaluate(dataset, metrics=[faithfulness])
print(f"Factual Grounding Score: {result['faithfulness']}")
```

### Lệnh xác minh & thực thi:
```bash
# Đánh giá chỉ số Faithfulness trên bộ dữ liệu test RAG
python scripts/audit_rag_grounding.py --dataset data/rag_testset.json
```

## 8. Anti-Patterns & Common Traps
- Cho phép LLM trả lời dựa trên kiến thức chung được huấn luyện sẵn khi đang chạy ở chế độ RAG chính sách nghiêm ngặt.
- Hiển thị trích dẫn chung chung ở cuối bài mà không chỉ rõ câu nào được trích từ tài liệu nào.

## 9. Quality Gates & Acceptance Criteria
- Faithfulness Score đạt tối thiểu 0.95 trên 100% các câu trả lời thuộc lĩnh vực pháp lý và tài chính.
- 0 trích dẫn rác (hallucinated citations) được chấp nhận trên giao diện người dùng.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Không ghi lại các dữ liệu nhạy cảm của khách hàng trong quá trình lưu trữ log kiểm toán grounding.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ sinh thái AI / UX**: Hỗ trợ Model Context Protocol (MCP), LangChain/LlamaIndex, Figma, Playwright axe-core.

## 12. Deliverables & Output Artifacts
- Module kiểm toán Factual Grounding tự động.
- Dashboard hiển thị tỉ lệ Hallucination rate và Citation accuracy theo thời gian thực.

## 13. Related & Complementary Skills
dex-reranking-strategies, dex-vector-index-design, dex-agent-evaluation-harness

## 14. Realistic Usage Example
### Tình huống thực tế:
Một ngân hàng triển khai chatbot trả lời chính sách cho vay cho khách hàng. Ban đầu chatbot thỉnh thoảng 'bịa' thêm ưu đãi giảm lãi suất 2% không có thật trong cẩm nang. Sau khi tích hợp Grounding & Citation Audit, mọi câu trả lời đều được kiểm tra NLI trước khi gửi tới khách hàng; các câu trả lời chứa thông tin không có căn cứ bị chặn đứng ngay lập tức, bảo đảm uy tín và tuân thủ pháp lý cho ngân hàng.
