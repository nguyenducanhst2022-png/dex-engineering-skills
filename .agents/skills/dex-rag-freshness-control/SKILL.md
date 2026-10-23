---
name: dex-rag-freshness-control
description: Engineer document freshness policies, real-time vector index invalidation, TTL expiration, and stale evidence detection in RAG systems. Use when retrieving dynamic domain knowledge where outdated data causes critical hallucinations.
---

# dex-rag-freshness-control

## 1. Purpose & Scope
Thiết kế và quản trị vòng đời cập nhật dữ liệu trong hệ thống RAG (RAG Freshness Control); cài đặt cơ chế hủy chỉ mục vector theo thời gian thực (Invalidation Hooks), chính sách hết hạn TTL, và tự động phát hiện bằng chứng lỗi thời (Stale Evidence Detection) nhằm ngăn ngừa tình trạng LLM trả lời dựa trên thông tin cũ đã bị hủy bỏ.

## 2. When to Use
- Khi dữ liệu tri thức của doanh nghiệp thay đổi thường xuyên (bảng giá sản phẩm, chính sách bảo hành, trạng thái tồn kho).
- Khi khách hàng hoặc quản trị viên chỉnh sửa/xóa tài liệu nguồn trên CMS và yêu cầu chatbot AI phải cập nhật câu trả lời ngay lập tức.
- Khi hệ thống bị ảo giác (hallucination) do truy hồi được cả phiên bản tài liệu cũ lẫn phiên bản mới cùng lúc.

## 3. When NOT to Use
- Khi tài liệu là văn bản lịch sử bất biến không bao giờ thay đổi (ví dụ: các bài báo khoa học đã xuất bản).
- Khi hệ thống không sử dụng RAG mà trả lời hoàn toàn từ tri thức tham số hóa trong weights của LLM.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Webhook sự kiện thay đổi dữ liệu từ CMS/Database (Create/Update/Delete events), Vector Database hỗ trợ xóa/cập nhật theo ID hoặc metadata filter.
- **Quyền hạn truy cập:** Quyền xóa và ghi đè vector trong index.

## 5. Core Concepts & Taxonomy
- **Event-Driven Invalidation:** Khi một tài liệu bị cập nhật, hệ thống lập tức phát sinh sự kiện để xóa toàn bộ các chunks cũ của tài liệu đó trong vector store và nạp chunks mới.
- **Time-to-Live (TTL) Decay:** Cơ chế tự động giảm điểm truy hồi của tài liệu theo thời gian hoặc tự động xóa tài liệu sau khi hết hạn hiệu lực.
- **Stale Evidence Guardrail:** Kiểm tra trường `effective_until` của tài liệu trong prompt; nếu tài liệu đã hết hạn, LLM được hướng dẫn từ chối sử dụng thông tin đó.

## 6. Step-by-Step Execution Workflow
1. Lắng nghe webhook sự kiện cập nhật tài liệu (`document.updated`, `document.deleted`) từ hệ thống nguồn.
2. Xác định danh sách `document_id` cần cập nhật và phát lệnh xóa toàn bộ các vector chunks liên quan khỏi Vector Store.
3. Phân đoạn lại tài liệu mới, gắn metadata phiên bản mới nhất (`version`, `valid_from`, `valid_to`) và sinh vector mới.
4. Nạp các vector mới vào index và xác nhận chỉ mục đã sẵn sàng phục vụ truy vấn.
5. Trong prompt template gửi tới LLM: đính kèm mốc thời gian hiện tại (`current_system_time`) và ngày xuất bản của từng đoạn trích.
6. Cài đặt luật guardrail: nếu hai tài liệu có nội dung mâu thuẫn, LLM bắt buộc phải ưu tiên tài liệu có ngày phát hành mới hơn.

## 7. Concrete Examples
### Ví dụ webhook handler tự động xóa và cập nhật vector chunks trong Qdrant:
```python
from qdrant_client import QdrantClient
from qdrant_client.http import models

def handle_document_update_event(event: dict, qdrant: QdrantClient, collection_name: str, embedding_service):
    doc_id = event["document_id"]
    new_text_content = event["content"]
    updated_at = event["updated_at"]

    # 1. Xóa toàn bộ các vector chunks cũ thuộc về document_id này
    qdrant.delete(
        collection_name=collection_name,
        points_selector=models.FilterSelector(
            filter=models.Filter(
                must=[models.FieldCondition(key="document_id", match=models.MatchValue(value=doc_id))]
            )
        )
    )
    print(f"Purged stale vectors for document: {doc_id}")

    # 2. Sinh chunks mới và nhúng vector mới
    new_chunks = chunk_document(new_text_content)
    points = []
    for idx, chunk in enumerate(new_chunks):
        vec = embedding_service.embed(chunk)
        points.append(models.PointStruct(
            id=f"{doc_id}_{idx}",
            vector=vec,
            payload={"document_id": doc_id, "text": chunk, "updated_at": updated_at}
        ))

    # 3. Nạp lại vector mới nhất vào Qdrant
    qdrant.upsert(collection_name=collection_name, points=points)
    print(f"Upserted {len(points)} fresh vector chunks for document: {doc_id}")
```

## 8. Anti-Patterns & Common Traps
- **Append-Only Vector Store:** Cập nhật tài liệu mới bằng cách nạp thêm vector mà không xóa vector cũ, khiến vector store chứa đầy rác và làm LLM trả lời thông tin cũ.
- **Ignoring Time Horizon in Prompts:** Không cung cấp ngày tháng trong prompt khiến LLM không có căn cứ để phân biệt tài liệu nào là mới nhất.
- **Delayed Batch Invalidation:** Gom các yêu cầu xóa tài liệu vào cron job chạy đêm, khiến các tài liệu đã xóa lúc 9h sáng vẫn tiếp tục được chatbot trả lời suốt cả ngày.

## 9. Quality Gates & Acceptance Criteria
- **QG-03**: Khi tài liệu nguồn bị sửa, thời gian để vector store phản ánh nội dung mới dưới 5 giây.
- **QG-09**: Kiểm thử tự động chứng minh LLM trả lời giá mới sau khi tài liệu bảng giá được cập nhật.
- **QG-10**: Các tài liệu đã hết hạn (quá ngày `valid_to`) không bao giờ được đưa vào context window của người dùng.

## 10. Security & Safety Boundaries
- Kiểm tra quyền sở hữu tài liệu khi nhận webhook cập nhật để tránh việc giả mạo webhook xóa vector của tổ chức khác.
- Lưu nhật ký kiểm toán (Audit Log) về mọi hành động cập nhật và hủy vector trong hệ thống.

## 11. Platform Adapters
- **Vector Stores**: Qdrant Payload Filters, Pinecone Metadata Filtering, pgvector.
- **Message Bus**: Apache Kafka, AWS SQS, Webhook Receivers.

## 12. Deliverables & Output Artifacts
- Webhook Invalidation Handler cho Vector Database.
- Prompt Template tích hợp cơ chế nhận biết thời gian và giải quyết mâu thuẫn tài liệu.
- Bộ kiểm thử tự động xác minh tính tươi mới của kết quả RAG.

## 13. Related & Complementary Skills
dex-rag-pipelines, dex-embedding-data-preparation, dex-retrieval-evaluation

## 14. Realistic Usage Example
```powershell
# Chạy kiểm thử tự động xác minh tính năng hủy vector cũ khi tài liệu cập nhật
pytest tests/ai/test_rag_freshness_invalidation.py -v
```
