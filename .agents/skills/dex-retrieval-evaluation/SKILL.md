---
name: dex-retrieval-evaluation
description: Evaluate information retrieval quality in RAG systems using Hit Rate, Mean Reciprocal Rank (MRR), NDCG, Context Relevance, and Ragas metrics. Use when benchmarking search algorithms, evaluating embedding models, or tuning vector retrieval.
---

# dex-retrieval-evaluation

## 1. Purpose & Scope
Đo lường, đánh giá và kiểm thử định lượng chất lượng của tầng trích xuất thông tin (Information Retrieval Evaluation) trong hệ thống RAG; tính toán các chỉ số khoa học chuẩn mực (Hit Rate @ K, MRR - Mean Reciprocal Rank, NDCG - Normalized Discounted Cumulative Gain, Context Relevance) và sử dụng khung đánh giá tự động (Ragas / TruLens) để tối ưu hóa thuật toán tìm kiếm dựa trên số liệu thực tế.

## 2. When to Use
- Khi người dùng phàn nàn rằng hệ thống RAG tìm kiếm không đúng tài liệu họ cần.
- Khi cần quyết định lựa chọn giữa 2 mô hình Embedding khác nhau (ví dụ: OpenAI vs. Cohere vs. BGE) hoặc so sánh giữa các kích thước chunking.
- Khi chuẩn bị đưa hệ thống RAG vào môi trường sản xuất và cần số liệu đo lường chất lượng định lượng.

## 3. When NOT to Use
- Đánh giá phong cách viết văn hoặc độ mượt mà của câu trả lời do LLM sinh ra (dùng `dex-prompt-evaluation`).
- Đánh giá hiệu năng tốc độ mạng của API (dùng `dex-performance-optimization`).

## 4. Prerequisites & Input Context
**Đầu vào cần thiết:**
- Tập dữ liệu kiểm thử vàng (Evaluation Golden Dataset: Cặp câu hỏi và ID tài liệu liên quan chuẩn xác - Ground Truth).
- Danh sách kết quả trích xuất Top-K từ hệ thống tìm kiếm.
- Framework đánh giá (Ragas, TruLens, hoặc custom Python evaluation scripts).

**Điều kiện tiên quyết:**
- Có bộ dữ liệu thử nghiệm tối thiểu 50-100 câu hỏi tiêu biểu đại diện cho các hành vi người dùng thật kèm đáp án đối chiếu.
- Tầng trích xuất (Retrieval engine) có API trả về danh sách ID và điểm số tương đồng của từng kết quả.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**: Nắm vững cơ chế vận hành theo chuẩn Agent Skills, tuân thủ nghiêm ngặt tính xác định và ranh giới trách nhiệm.
- **Quy tắc quyết định kỹ thuật**:
- **Quyết Định Dựa Trên Dữ Liệu**: Chỉ thay đổi mô hình Embedding hoặc chiến lược Chunking khi các chỉ số đo lường (Hit Rate, MRR) trên Golden Dataset chứng minh sự cải thiện rõ rệt.
- **Không Tối Ưu Quá Mức Trên Mẫu Nhỏ (Overfitting)**: Tập dữ liệu kiểm thử vàng phải đủ đa dạng, bao gồm cả câu hỏi ngắn, câu hỏi dài, từ đồng nghĩa và từ viết tắt chuyên ngành.
- **Ưu Tiên Hit Rate Hơn Rerank**: Nếu tài liệu đúng thậm chí còn không lọt vào Top 20 ban đầu của Vector DB, thì thuật toán Re-ranker phía sau sẽ hoàn toàn vô dụng; do đó phải tối ưu bước trích xuất ban đầu đạt Hit Rate cao trước.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Hit Rate quá thấp (< 60%)**: Do người dùng dùng từ đồng nghĩa mà Embedding model không hiểu -> Khắc phục: Bổ sung thuật toán Sparse BM25 và mở rộng truy vấn (Query Expansion bằng LLM).
- **MRR thấp (Tài liệu đúng toàn nằm ở vị trí số 8, số 9)**: -> Khắc phục: Bổ sung bước Cross-Encoder Re-ranker để đẩy tài liệu đúng lên vị trí số 1 hoặc số 2.

## 6. Step-by-Step Execution Workflow
1. Xây dựng tập dữ liệu kiểm thử vàng (Golden Dataset): Với mỗi câu hỏi, chuyên gia nghiệp vụ xác định chính xác những đoạn văn bản nào là câu trả lời đúng (Ground Truth).
2. Chạy tầng trích xuất cho toàn bộ tập câu hỏi với cấu hình hiện tại (Baseline): Ghi nhận Top-K kết quả (ví dụ K=5).
3. Tính toán các chỉ số xếp hạng truyền thống:
   - *Hit Rate @ 5*: Tỷ lệ phần trăm các câu hỏi mà tài liệu đúng nằm trong Top 5 kết quả (Mục tiêu >= 85%).
   - *Mean Reciprocal Rank (MRR)*: Vị trí của tài liệu đúng xuất hiện càng cao thì điểm càng lớn (1/vị trí).
   - *NDCG @ 5*: Đánh giá mức độ phù hợp và thứ tự sắp xếp của toàn bộ danh sách kết quả.
4. Đánh giá ngữ nghĩa bằng LLM-as-a-Judge (Ragas Framework):
   - *Context Relevance*: Đo lường xem ngữ cảnh trích xuất có bị thừa thãi thông tin rác hay không.
   - *Faithfulness*: Đo lường xem câu trả lời có hoàn toàn dựa vào ngữ cảnh hay có yếu tố ảo giác.
5. Tinh chỉnh các tham số (Tuning): Thay đổi kích thước chunk, đổi mô hình embedding, bổ sung Re-ranker, tinh chỉnh trọng số Hybrid Search (Dense vs. Sparse weight).
6. Đo lường lại và lập bảng so sánh số liệu trước/sau rõ ràng.

## 7. Concrete Examples
### Ví dụ triển khai chuẩn mực:
```python
# scripts/evaluate_retrieval.py (Tính toán Hit Rate & MRR chuẩn mực)
def calculate_retrieval_metrics(golden_data, retrieve_fn, k=5):
    hits = 0
    reciprocal_ranks = []
    for item in golden_data:
        results = retrieve_fn(item['query'], top_k=k)
        retrieved_ids = [r['id'] for r in results]
        target_id = item['target_doc_id']
        if target_id in retrieved_ids:
            hits += 1
            rank = retrieved_ids.index(target_id) + 1
            reciprocal_ranks.append(1.0 / rank)
        else:
            reciprocal_ranks.append(0.0)
    hit_rate = hits / len(golden_data)
    mrr = sum(reciprocal_ranks) / len(golden_data)
    print(f'Hit Rate @ {k}: {hit_rate:.2%} | MRR @ {k}: {mrr:.4f}')
    return {'hit_rate': hit_rate, 'mrr': mrr}
```

### Lệnh xác minh & thực thi:
- Chạy script kiểm toán trích xuất: `python scripts/evaluate_retrieval.py --dataset golden_set.json --k 5`
- Chạy framework Ragas: `ragas evaluate --dataset test_rag_dataset.json`
- Xuất báo cáo điểm số chi tiết ra file CSV: `python scripts/export_eval_metrics.py`

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước kiểm tra biên và giả định hệ thống luôn ở trạng thái lý tưởng.
- **Anti-Pattern 2**: Không ghi nhận nhật ký kiểm toán hoặc bỏ qua việc xử lý ngoại lệ lúc runtime.
- **Trap**: Bỏ qua các rào chắn an toàn hoặc cố tình chạy script không qua kiểm thử tự động.

## 9. Quality Gates & Acceptance Criteria
- QG-04: Chỉ số Hit Rate @ 5 trên Golden Dataset đạt tối thiểu >= 85%.
- QG-10: Báo cáo đo lường có đầy đủ bảng số liệu so sánh Hit Rate, MRR, NDCG giữa các phiên bản cấu hình.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động trước khi coi là hoàn thành.

## 10. Security & Safety Boundaries
- Tập dữ liệu kiểm thử vàng (Golden Dataset) phải được làm sạch các thông tin bí mật trước khi lưu trữ trong kho mã nguồn.
- Không bao giờ thực thi mã nguồn hoặc thay đổi cấu hình trên môi trường sản xuất mà thiếu cơ chế rollback an toàn.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Có thể kích hoạt trực tiếp từ terminal hoặc extension tương thích trong VS Code / Cursor / Windsurf.

## 12. Deliverables & Output Artifacts
- Script kiểm toán đánh giá trích xuất (`scripts/evaluate_retrieval.py`).
- Tập dữ liệu vàng chuẩn hóa (`data/golden_evaluation_dataset.json`).
- Báo cáo kết quả so sánh chất lượng các mô hình.

## 13. Related & Complementary Skills
- `dex-development-workflow`: Quy trình phát triển tiêu chuẩn.
- `dex-code-verification`: Xác minh chất lượng và tính đúng đắn của mã nguồn.
- `dex-master-orchestrator`: Bộ điều phối trung tâm kết nối kỹ năng này với các kỹ năng khác trong hệ thống.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư hoặc AI Agent tiếp nhận yêu cầu liên quan đến **dex-retrieval-evaluation**.
1. Đọc kỹ đầu vào và các ràng buộc kỹ thuật tại mục 4.
2. Thực thi tuần tự 6 bước trong Workflow tại mục 6.
3. Chạy các lệnh kiểm chứng tại mục 7 và đối chiếu với Quality Gates tại mục 9.
4. Đóng gói deliverables theo danh sách tại mục 12 và báo cáo kết quả kèm bằng chứng xác thực.
