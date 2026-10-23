---
name: dex-vector-embedding-migration
description: Orchestrate zero-downtime migration, re-indexing, and dimension alignment across dense vector embeddings and vector databases. Use when upgrading embedding models or transitioning vector infrastructure.
---

# dex-vector-embedding-migration

## 1. Purpose & Scope
Điều phối quy trình chuyển đổi (migration), tái lập chỉ mục (re-indexing) và căn chỉnh chiều vector (dimension alignment) giữa các mô hình embedding hoặc cơ sở dữ liệu vector mà không làm gián đoạn dịch vụ truy hồi đang chạy (Zero-Downtime).

## 2. When to Use
- Khi nâng cấp mô hình embedding từ phiên bản cũ (ví dụ: OpenAI Ada-002, 1536 chiều) sang mô hình mới hơn (text-embedding-3-small/large, Voyage, BGE).
- Khi di chuyển hạ tầng vector database từ giải pháp tự host (Chroma, Faiss) sang nền tảng phân tán đám mây (Qdrant, Pinecone, pgvector).
- Khi số lượng vector tăng lên hàng trăm triệu cần tái cấu trúc chỉ mục HNSW/IVFFlat để tiết kiệm RAM.

## 3. When NOT to Use
- Khi hệ thống chỉ là ứng dụng cá nhân nhỏ có thể tạm dừng dịch vụ trong vài giờ để chạy lại toàn bộ từ đầu.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Vector database hiện tại, kho dữ liệu gốc (raw documents), mô hình embedding mới, chỉ mục vector đích.
- **Quyền hạn truy cập:** Quyền tạo collection mới và chuyển đổi alias định tuyến truy vấn trong vector database.

## 5. Core Concepts & Taxonomy
- **Dual-Indexing (Blue/Green Collections):** Nạp và sinh embedding mới vào Collection Green trong khi Collection Blue vẫn tiếp tục phục vụ lưu lượng tìm kiếm của người dùng.
- **Dimension Incompatibility:** Vector sinh từ hai mô hình embedding khác nhau không thể so sánh khoảng cách với nhau (kể cả khi chúng có cùng số chiều).
- **Alias Flipping:** Hoán đổi trỏ alias của ứng dụng từ collection cũ sang collection mới trong 1 thao tác nguyên tử (atomic operation) khi re-indexing hoàn tất.

## 6. Step-by-Step Execution Workflow
1. Khởi tạo Collection mới (Target/Green) với cấu hình số chiều và độ đo khoảng cách (Cosine, Dot Product) của mô hình mới.
2. Cấu hình cơ chế ghi kép (Dual-Writing): các bản ghi tạo mới hoặc cập nhật được sinh embedding và ghi vào cả hai Collection.
3. Chạy pipeline xử lý lô nạp lại toàn bộ dữ liệu lịch sử từ kho lưu trữ gốc vào Collection mới bằng mô hình embedding mới.
4. Thực hiện kiểm thử đối soát chất lượng truy hồi (Retrieval Benchmark): so sánh điểm NDCG@10 giữa hai collection trên tập câu hỏi chuẩn.
5. Thực hiện đổi hướng truy vấn (Alias Switch) từ Blue sang Green một cách nguyên tử.
6. Theo dõi lỗi và độ trễ trong 48 giờ trước khi giải phóng tài nguyên của Collection cũ.

## 7. Concrete Examples
### Hoán đổi Alias nguyên tử trong Qdrant sau khi hoàn tất Re-indexing:
```python
from qdrant_client import QdrantClient
from qdrant_client.http import models

client = QdrantClient(host="localhost", port=6333)

def switch_vector_collection_alias(alias_name: str, old_coll: str, new_coll: str):
    # Thao tac nguyen tu: xoa alias khoi coll cu va tro sang coll moi ngay lap tuc
    client.update_collection_aliases(
        change_aliases_operations=[
            models.DeleteAliasOperation(delete_alias=models.DeleteAlias(alias_name=alias_name)),
            models.CreateAliasOperation(create_alias=models.CreateAlias(collection_name=new_coll, alias_name=alias_name))
        ]
    )
    print(f"Da hoan doi alias '{alias_name}' tu {old_coll} sang {new_coll} thanh cong khong downtime!")
```

## 8. Anti-Patterns & Common Traps
- **Direct In-Place Mutation:** Xóa và ghi đè vector trực tiếp trên collection đang chạy khiến người dùng gặp lỗi gián đoạn tìm kiếm trong nhiều giờ.
- **Cross-Model Distance Calculation:** Dùng vector query của mô hình mới để tìm kiếm trong collection chứa vector của mô hình cũ.
- **Missing Document Backlog:** Quên nạp các bản ghi được tạo ra trong khoảng thời gian pipeline re-indexing đang chạy.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Tỷ lệ lỗi truy vấn của người dùng duy trì ở mức 0% trong suốt quá trình hoán đổi alias.
- **QG-04**: Số lượng vector trong Collection mới khớp chính xác 100% với số lượng tài liệu trong kho dữ liệu gốc.
- **QG-06**: Điểm chất lượng truy hồi (NDCG@10) của mô hình mới cao hơn hoặc bằng mô hình cũ trên tập benchmark.

## 10. Security & Safety Boundaries
- Duy trì các bộ lọc phân quyền bảo mật (Tenant ID / Metadata ACLs) nguyên vẹn trên collection mới.

## 11. Platform Adapters
- **Vector Databases**: Qdrant, Pinecone, Milvus, Weaviate, pgvector.
- **Embeddings**: OpenAI, Cohere, Voyage AI, HuggingFace Transformers.

## 12. Deliverables & Output Artifacts
- Kịch bản điều phối Re-indexing không downtime.
- Pipeline kiểm thử chất lượng truy hồi so sánh (A/B retrieval eval).
- Hướng dẫn rollback dự phòng khi xảy ra sự cố.

## 13. Related & Complementary Skills
dex-embedding-data-preparation, dex-hybrid-search-fusion, dex-rag-freshness-control

## 14. Realistic Usage Example
```powershell
# Chạy job nạp lại embedding vào collection mới
python scripts/ml/reindex_embeddings.py --source s3://knowledge-base/ --target-collection v2_knowledge

# Hoán đổi alias sang collection mới
python scripts/ml/swap_collection_alias.py --alias knowledge_prod --new-collection v2_knowledge
```
