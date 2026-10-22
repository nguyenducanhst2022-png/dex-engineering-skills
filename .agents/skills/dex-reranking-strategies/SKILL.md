---
name: dex-reranking-strategies
description: Implement multi-stage retrieval pipelines combining dense/sparse retrieval with Cross-Encoder and ColBERT rerankers (Cohere, BGE-Reranker) to boost top-K relevance. Use when raw vector search fails to rank the best chunk first.
---

# dex-reranking-strategies

## 1. Purpose & Scope
Thiết kế và triển khai đường ống truy xuất dữ liệu đa tầng (Multi-Stage Retrieval Pipelines); kết hợp giữa tầng truy hồi ứng viên nhanh (Dense Vector + BM25 Sparse Search) với tầng chấm điểm tái sắp xếp chuyên sâu (Reranking Layer: Cross-Encoders như Cohere Rerank, BGE-Reranker, ColBERT) nhằm đưa tài liệu chính xác nhất lên vị trí Top-1/Top-3 cho LLM.

## 2. When to Use
- Hệ thống RAG tìm kiếm ra đúng tài liệu chứa câu trả lời nhưng tài liệu đó lại nằm ở vị trí thứ 8 hoặc thứ 10, khiến LLM bỏ sót do hiện tượng 'Lost in the Middle'.
- Người dùng đặt câu hỏi phủ định hoặc so sánh phức tạp mà Bi-Encoder vector search thông thường hiểu sai ngữ nghĩa.
- Cần nâng cao chỉ số MRR (Mean Reciprocal Rank) và NDCG@5 cho công cụ tìm kiếm.

## 3. When NOT to Use
- Không chạy mô hình Cross-Encoder nặng nề trên toàn bộ cơ sở dữ liệu hàng triệu văn bản (chi phí tính toán cực lớn; chỉ chạy trên Top 30-50 ứng viên được truy hồi từ tầng 1).
- Không cần reranking nếu hệ thống chỉ tra cứu các tài liệu có cấu trúc với key chính xác.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Câu truy vấn của người dùng (Query).
- Danh sách tài liệu ứng viên từ tầng 1 (Top 30-50 retrieved chunks).
- Mô hình Reranker (API Cohere Rerank hoặc mô hình local như `bge-reranker-large`).
- **Điều kiện tiên quyết**:
- Có hạ tầng GPU hoặc API client hỗ trợ Cross-Encoder inference.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Bi-Encoder vs Cross-Encoder:
  + Bi-Encoder (Embedding thông thường): Mã hóa câu hỏi và văn bản độc lập thành 2 vectors rồi tính Cosine. Tốc độ siêu nhanh nhưng mất đi sự tương tác từ ngữ qua lại.
  + Cross-Encoder (Reranker): Đưa cả câu hỏi và văn bản vào mô hình transformer cùng lúc (`[CLS] Query [SEP] Document`). Mô hình chú ý toàn phần (Full Self-Attention) giữa từng từ trong câu hỏi và văn bản, mang lại độ chính xác vượt trội.
- Reciprocal Rank Fusion (RRF): Thuật toán kết hợp điểm số giữa Dense Search và BM25 trước khi chuyển sang Reranker.
- **Quy tắc quyết định kỹ thuật**:
- Tầng 1 (Retrieval): Lấy Top 40 ứng viên nhanh nhất bằng Hybrid Search (Vector + BM25).
- Tầng 2 (Reranking): Dùng Cross-Encoder chấm điểm lại 40 ứng viên đó và chỉ chọn ra Top 5 ứng viên có điểm số cao nhất gửi cho LLM.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Độ dài văn bản vượt quá context limit của mô hình reranker (thường là 512 tokens), khiến đoạn văn quan trọng ở cuối bị cắt bỏ (cần chunking văn bản hợp lý).

## 6. Step-by-Step Execution Workflow
1. Thực hiện Hybrid Search kết hợp pgvector và BM25 để lấy 50 chunks ứng viên.
2. Áp dụng thuật toán Reciprocal Rank Fusion (RRF) để gộp kết quả.
3. Gửi danh sách 50 chunks vào Cross-Encoder Reranker.
4. Lọc bỏ các chunks có điểm số liên quan dưới ngưỡng an toàn (Relevance Score < 0.65).
5. Sắp xếp lại danh sách và đưa Top 5 chunks chất lượng nhất vào prompt của LLM.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```python
from sentence_transformers import CrossEncoder

# Khởi tạo mô hình Cross-Encoder chuyên dụng cho Reranking
reranker = CrossEncoder('BAAI/bge-reranker-base')

def rerank_chunks(query: str, retrieved_chunks: list[str], top_k: int = 5) -> list[str]:
    # Chuẩn bị các cặp (Query, Document)
    pairs = [[query, chunk] for chunk in retrieved_chunks]
    scores = reranker.predict(pairs)
    
    # Kết hợp điểm và sắp xếp giảm dần
    scored_results = sorted(zip(retrieved_chunks, scores), key=lambda x: x[1], reverse=True)
    
    # Chỉ trả về Top K ứng viên có độ liên quan cao nhất
    return [chunk for chunk, score in scored_results[:top_k] if score > 0.5]
```

### Lệnh xác minh & thực thi:
```bash
# Đánh giá chỉ số NDCG và MRR trên tập kiểm thử bằng Ragas
pytest tests/eval/test_reranker_relevance.py
```

## 8. Anti-Patterns & Common Traps
- Gửi quá nhiều chunks (Top 20+) vào LLM làm loãng context và tăng chi phí token không cần thiết.
- Chỉ tin tưởng vào điểm similarity của vector search mà không có tầng reranker kiểm chứng ngữ nghĩa.

## 9. Quality Gates & Acceptance Criteria
- Tăng chỉ số Hit Rate@3 lên tối thiểu 25% so với phương pháp vector search thuần túy.
- Thời gian thực thi bước Reranking trên 30 ứng viên phải dưới 100ms.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Đảm bảo quy trình Reranking tôn trọng quyền truy cập (Access Control Lists) của người dùng trước khi chấm điểm.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ sinh thái AI / UX**: Hỗ trợ Model Context Protocol (MCP), LangChain/LlamaIndex, Figma, Playwright axe-core.

## 12. Deliverables & Output Artifacts
- Module Reranking tích hợp hoàn chỉnh.
- Bảng đối soát cải thiện chỉ số Hit Rate / MRR trước và sau khi áp dụng.

## 13. Related & Complementary Skills
dex-vector-index-design, dex-grounding-citation-audit, dex-structured-llm-output

## 14. Realistic Usage Example
### Tình huống thực tế:
Một hệ thống hỗ trợ kỹ thuật nội bộ của công ty viễn thông thường xuyên trả lời sai khi nhân viên hỏi 'Gói cước nào KHÔNG áp dụng cho thuê bao trả sau?'. Vector search chỉ tìm các từ khóa 'thuê bao trả sau' và trả về các gói có áp dụng. Sau khi bổ sung tầng BGE-Reranker, Cross-Encoder đã hiểu đúng ý nghĩa phủ định 'KHÔNG', đẩy đúng văn bản ngoại lệ lên Top 1 và giúp LLM trả lời chính xác 100%.
