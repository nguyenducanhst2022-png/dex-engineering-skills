---
name: dex-vector-index-design
description: Architect, configure, and benchmark vector search indexes (HNSW, IVF-PQ) across vector databases (Qdrant, Pinecone, pgvector), balancing recall, latency, and RAM costs. Use when building semantic search and RAG retrieval pipelines.
---

# dex-vector-index-design

## 1. Purpose & Scope
Thiết kế, cấu hình và đo lường chỉ mục tìm kiếm vector (Vector Index Design: HNSW, IVF-PQ, ScaNN) trên các cơ sở dữ liệu vector chuyên dụng (Qdrant, pgvector, Milvus, Pinecone); cân bằng giữa độ chính xác truy hồi (Recall), độ trễ tìm kiếm (Latency) và chi phí bộ nhớ RAM, tối ưu hóa cho các hệ thống RAG và Semantic Search quy mô hàng triệu vectors.

## 2. When to Use
- Hệ thống RAG gặp hiện tượng tìm kiếm chậm (>200ms) hoặc trả về các tài liệu không liên quan.
- Bộ nhớ RAM của cụm Vector Database bị phình to quá mức khi mở rộng lên hàng triệu bản ghi.
- Cần lựa chọn giữa thuật toán đồ thị HNSW (chính xác, ngốn RAM) hay lượng tử hóa IVF-PQ (tiết kiệm RAM, giảm chút recall).

## 3. When NOT to Use
- Không cần dùng Vector Index phức tạp nếu tập dữ liệu chỉ có dưới 5,000 documents (tìm kiếm cosine flat exact search là đủ nhanh).
- Không dùng Vector Search thuần túy cho các truy vấn tìm kiếm chính xác từ khóa mã lỗi hoặc ID (hãy kết hợp Hybrid Search với BM25).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Số lượng chiều của vector (Embedding dimensions: ví dụ 1536 với OpenAI text-embedding-3-small, 768 với BAAI bge).
- Thước đo khoảng cách (Distance metric: Cosine, Dot Product, Euclidean).
- Tổng số lượng vector dự kiến trong 12 tháng tới.
- **Điều kiện tiên quyết**:
- Có quyền truy cập cấu hình index trong pgvector hoặc Qdrant cluster.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- HNSW (Hierarchical Navigable Small World): Thuật toán tìm kiếm lân cận gần đúng (ANN) trên đồ thị phân tầng. Ưu điểm: Tốc độ truy vấn siêu nhanh và recall cực cao (>95%). Nhược điểm: Tốn nhiều RAM để duy trì cấu trúc đồ thị.
- Scalar Quantization (SQ) & Product Quantization (PQ): Kỹ thuật nén vector từ float32 (4 bytes/chiều) xuống int8 hoặc 4-bit, giảm 75% dung lượng RAM với mức giảm recall không đáng kể (<2%).
- HNSW Tuning Parameters:
  + `m`: Số lượng liên kết tối đa của mỗi node trên đồ thị (16-64).
  + `ef_construction`: Độ sâu tìm kiếm khi xây dựng index (càng cao index build càng lâu nhưng recall càng tốt).
  + `ef_search`: Độ sâu tìm kiếm khi query (điều chỉnh động để cân bằng giữa latency và recall).
- **Quy tắc quyết định kỹ thuật**:
- Nếu dữ liệu > 10 triệu vectors và RAM có hạn: bắt buộc bật Product Quantization (IVF-PQ) hoặc Scalar Quantization.
- Nếu sử dụng OpenAI Embeddings đã chuẩn hóa độ dài (normalized): sử dụng Dot Product (Inner Product) thay vì Cosine để tăng tốc độ tính toán.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Xây dựng index HNSW trên bảng cơ sở dữ liệu trước khi nạp dữ liệu lớn, khiến quá trình bulk insert chậm gấp 50 lần (phải nạp dữ liệu xong mới tạo index).

## 6. Step-by-Step Execution Workflow
1. Phân tích kích thước chiều vector và đặc tính phân phối của embedding model.
2. Lựa chọn distance metric phù hợp (Cosine vs Dot Product).
3. Cấu hình các thông số HNSW (`m=16, ef_construction=128, ef_search=64`).
4. Chạy bài benchmark đo lường đồ thị đánh đổi (Tradeoff curve) giữa Recall@10 và Latency (ms).
5. Thiết lập cơ chế lọc metadata (Payload filtering) có index để tối ưu hóa truy vấn kết hợp.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```sql
-- Cấu hình HNSW Index tối ưu trong pgvector trên PostgreSQL
CREATE INDEX ON document_embeddings 
USING hnsw (embedding vector_cosine_ops)
WITH (
  m = 16,
  ef_construction = 128
);

-- Tinh chỉnh ef_search khi truy vấn thời gian thực
SET hnsw.ef_search = 64;
SELECT id, title FROM document_embeddings 
ORDER BY embedding <=> '[0.012, -0.045, ...]' 
LIMIT 5;
```

### Lệnh xác minh & thực thi:
```bash
# Đo lường recall và QPS của vector index bằng công cụ ann-benchmarks
python run.py --dataset glove-100-angular --algorithm hnswlib
```

## 8. Anti-Patterns & Common Traps
- Sử dụng distance metric không khớp với embedding model (ví dụ model yêu cầu Cosine nhưng index lại dùng Euclidean).
- Quên cấu hình index cho các trường lọc metadata (Payload indexes) khiến vector DB phải quét tuần tự toàn bộ bảng.

## 9. Quality Gates & Acceptance Criteria
- Recall@10 đạt tối thiểu 92% so với phép tìm kiếm chính xác (Exact Flat Search).
- Độ trễ truy vấn P95 duy trì dưới 25ms trên tập dữ liệu 1 triệu vectors.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Áp dụng Tenant Isolation (lọc theo `tenant_id`) ngay tại bước lọc trước (Pre-filtering) của vector search để ngăn rò rỉ dữ liệu giữa các khách hàng.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ sinh thái AI / UX**: Hỗ trợ Model Context Protocol (MCP), LangChain/LlamaIndex, Figma, Playwright axe-core.

## 12. Deliverables & Output Artifacts
- Script tạo và tinh chỉnh Vector Index (SQL hoặc Qdrant config).
- Báo cáo phân tích đường cong đánh đổi Recall vs Latency.

## 13. Related & Complementary Skills
dex-reranking-strategies, dex-grounding-citation-audit, dex-database-design

## 14. Realistic Usage Example
### Tình huống thực tế:
Một ứng dụng tra cứu luật pháp có 2 triệu điều khoản lưu trong pgvector bị chậm tới 450ms cho mỗi lượt tìm kiếm và máy chủ hết sạch RAM. Chuyên gia tái cấu trúc chỉ mục sang HNSW với `m=16` kết hợp Scalar Quantization nén vector sang int8. Kết quả: RAM giảm từ 24GB xuống 6GB, độ trễ truy vấn giảm từ 450ms xuống 18ms trong khi độ chính xác tra cứu vẫn giữ nguyên 96%.
