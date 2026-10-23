---
name: dex-hybrid-search-fusion
description: Combine dense semantic vector search with sparse lexical keyword matching using Reciprocal Rank Fusion (RRF) and dynamic score balancing. Use when optimizing RAG retrieval quality across diverse domain vocabularies.
---

# dex-hybrid-search-fusion

## 1. Purpose & Scope
Thiết kế và tối ưu hóa hệ thống tìm kiếm lai (Hybrid Search Fusion); kết hợp truy hồi ngữ nghĩa dựa trên dense vector (HNSW) với tìm kiếm từ khóa chính xác dựa trên sparse lexical (BM25), áp dụng thuật toán Reciprocal Rank Fusion (RRF) và hiệu chỉnh trọng số $\alpha$ để nâng cao chỉ số Recall và MRR.

## 2. When to Use
- Khi người dùng tìm kiếm chứa các từ khóa chính xác như mã lỗi kỹ thuật, tên model, số hiệu hợp đồng mà vector embedding thường xử lý kém.
- Khi muốn có độ hồi tưởng cao (High Recall) mà không bị phụ thuộc hoàn toàn vào một mô hình biểu diễn duy nhất.
- Khi nâng cấp hệ thống RAG enterprise phục vụ các miền kiến thức chuyên sâu (Y tế, Pháp luật, Kỹ thuật phần mềm).

## 3. When NOT to Use
- Khi dữ liệu chỉ gồm các câu hỏi hội thoại đơn giản không có thuật ngữ chuyên ngành.
- Khi hạ tầng bị hạn chế tài nguyên không thể vận hành đồng thời cả vector index và inverted index.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Câu truy vấn của người dùng, Dense Vector Store (Qdrant, pgvector), Sparse Lexical Index (Elasticsearch, BM25).
- **Quyền hạn truy cập:** Quyền thực thi câu lệnh tìm kiếm trên cả hai hệ thống chỉ mục.

## 5. Core Concepts & Taxonomy
- **Reciprocal Rank Fusion (RRF):** Thuật toán kết hợp bảng xếp hạng không phụ thuộc vào thang điểm tuyệt đối, chấm điểm dựa trên thứ hạng: $RRF(d) = \sum_{m \in M} \frac{1}{k + r_m(d)}$ với hằng số làm mượt $k \approx 60$.
- **Dense-Sparse Alpha Tuning:** Công thức kết hợp điểm số có trọng số: $Score = \alpha \cdot Score_{dense} + (1 - \alpha) \cdot Score_{sparse}$, với $\alpha \in [0, 1]$.
- **Lexical Gap vs Semantic Drift:** Lexical search giải quyết bài toán thiếu từ khóa chính xác; Semantic search giải quyết bài toán đồng nghĩa và đa nghĩa.

## 6. Step-by-Step Execution Workflow
1. Tiếp nhận câu truy vấn và sinh embedding vector song song với việc tokenize từ khóa BM25.
2. Phát lệnh truy vấn song song: lấy Top-K (ví dụ: K=50) từ Vector Search và Top-K từ BM25 Lexical Search.
3. Chuẩn hóa danh sách kết quả và áp dụng thuật toán Reciprocal Rank Fusion (RRF) để tính điểm hợp nhất cho từng tài liệu.
4. Sắp xếp lại danh sách tài liệu theo điểm RRF giảm dần.
5. Lấy Top-N kết quả cao nhất (ví dụ: N=5 hoặc N=10) để đưa vào context window của LLM hoặc gửi sang bộ Reranker chuyên sâu.
6. Đánh giá chất lượng truy hồi định kỳ bằng tập dữ liệu golden test thông qua các chỉ số MRR@10 và HitRate@5.

## 7. Concrete Examples
### Ví dụ thuật toán Reciprocal Rank Fusion (RRF) trong Python:
```python
def reciprocal_rank_fusion(dense_results: list[str], sparse_results: list[str], k=60) -> list[tuple[str, float]]:
    scores = {}

    # 1. Tính điểm từ bảng xếp hạng Dense Search
    for rank, doc_id in enumerate(dense_results, start=1):
        scores[doc_id] = scores.get(doc_id, 0.0) + (1.0 / (k + rank))

    # 2. Tính điểm từ bảng xếp hạng Sparse BM25 Search
    for rank, doc_id in enumerate(sparse_results, start=1):
        scores[doc_id] = scores.get(doc_id, 0.0) + (1.0 / (k + rank))

    # 3. Sắp xếp kết quả tổng hợp theo điểm số giảm dần
    sorted_docs = sorted(scores.items(), key=lambda item: item[1], reverse=True)
    return sorted_docs
```

## 8. Anti-Patterns & Common Traps
- **Direct Score Addition:** Cộng trực tiếp điểm Cosine Similarity (thang 0-1) với điểm BM25 thô (thang 0-100+) mà không chuẩn hóa làm lệch kết quả hoàn toàn.
- **Sequential Execution:** Chạy lần lượt Vector Search rồi mới chạy BM25 Search làm tăng gấp đôi độ trễ truy hồi.
- **Ignoring Exact Code IDs:** Không có sparse search khiến các truy vấn tìm kiếm mã lỗi cụ thể như `ERR_CONN_RESET_8080` bị vector search trả về các bài viết giải thích chung chung.

## 9. Quality Gates & Acceptance Criteria
- **QG-03**: Hệ thống chứng minh khả năng tìm thấy chính xác tài liệu chứa mã lỗi kỹ thuật mà Vector Search đơn thuần bỏ sót.
- **QG-07**: Tổng thời gian thực thi tìm kiếm lai song song duy trì dưới 100ms.
- **QG-09**: Chỉ số HitRate@5 trên tập đánh giá mẫu đạt tối thiểu 92%.

## 10. Security & Safety Boundaries
- Áp dụng bộ lọc phân quyền (Tenant/User Permissions Filter) đồng bộ trên cả hai đường truy vấn Dense và Sparse.
- Làm sạch câu truy vấn để phòng chống các đòn tấn công SQL/Lucene Injection trên sparse search engine.

## 11. Platform Adapters
- **Engines**: Qdrant Hybrid Search, Elasticsearch 8.x with Dense Vectors, pgvector with pg_trgm.
- **Rerankers**: Cohere Rerank, BGE-Reranker-Large.

## 12. Deliverables & Output Artifacts
- Module thực thi tìm kiếm lai Hybrid Search Fusion với thuật toán RRF.
- Bộ công cụ benchmark đánh giá hiệu năng truy hồi (Recall, MRR).
- Báo cáo so sánh chất lượng giữa Single Search và Hybrid Search.

## 13. Related & Complementary Skills
dex-rag-pipelines, dex-retrieval-evaluation, dex-vector-index-design

## 14. Realistic Usage Example
```powershell
# Chạy bài benchmark đánh giá chất lượng tìm kiếm lai trên tập dữ liệu mẫu
python scripts/evaluate_hybrid_search.py --dataset tests/fixtures/eval_queries.json
```
