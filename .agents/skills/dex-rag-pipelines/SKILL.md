---
name: dex-rag-pipelines
description: Architect Retrieval-Augmented Generation (RAG) pipelines, semantic chunking strategies, vector embeddings, hybrid search (dense + sparse BM25), re-ranking, and context window assembly. Use when building question-answering systems, enterprise knowledge bases, or document search.
---

# dex-rag-pipelines

## 1. Purpose & Scope
Thiết kế và triển khai đường ống RAG (Retrieval-Augmented Generation) chuẩn sản xuất; tối ưu hóa chiến lược phân đoạn văn bản (Semantic Chunking), chuyển đổi vector nhúng (Embeddings), tìm kiếm lai (Hybrid Search kết hợp Vector Dense và BM25 Sparse), tái xếp hạng (Re-ranking) và đóng gói ngữ cảnh tối ưu vào cửa sổ ngữ cảnh của LLM, loại bỏ ảo giác và đảm bảo câu trả lời luôn có trích dẫn nguồn xác thực.

## 2. When to Use
- Khi xây dựng trợ lý AI tra cứu tài liệu nội bộ, hỏi đáp chính sách công ty, hỗ trợ khách hàng dựa trên cơ sở tri thức riêng.
- Khi LLM bị ảo giác (Hallucination) hoặc trả lời sai lệch thông tin kỹ thuật do không có ngữ cảnh cập nhật.
- Khi tìm kiếm ngữ nghĩa đơn thuần (Vector Search) trả về các đoạn văn bản không liên quan đến từ khóa chuyên ngành.

## 3. When NOT to Use
- Câu hỏi đơn giản về kiến thức phổ thông mà LLM đã được học sẵn trong dữ liệu gốc.
- Xử lý các phép toán tính tổng doanh thu chính xác trên hàng triệu dòng dữ liệu (khi đó phải dùng Text-to-SQL hoặc cơ sở dữ liệu quan hệ).

## 4. Prerequisites & Input Context
**Đầu vào cần thiết:**
- Tập tài liệu nguồn (PDF, Word, Markdown, HTML, Notion pages).
- Mô hình Embedding mục tiêu (OpenAI `text-embedding-3-small`, Cohere, Voyage AI, BGE).
- Cơ sở dữ liệu Vector (Qdrant, Pinecone, Milvus, pgvector, Weaviate).

**Điều kiện tiên quyết:**
- Vector Database đã được cài đặt, đánh chỉ mục HNSW (Hierarchical Navigable Small World) và kết nối sẵn sàng.
- Có công cụ trích xuất văn bản từ tệp tin (Unstructured, PyPDF, LlamaParse).

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**: Nắm vững cơ chế vận hành theo chuẩn Agent Skills, tuân thủ nghiêm ngặt tính xác định và ranh giới trách nhiệm.
- **Quy tắc quyết định kỹ thuật**:
- **Hybrid Search Là Bắt Buộc**: Tuyệt đối không chỉ dùng một mình Vector Search vì nó rất kém trong việc tìm kiếm các từ khóa chính xác như mã số định danh, ký hiệu lỗi phần mềm (ví dụ: `ERR_404_NOT_FOUND`).
- **Chunk Size Phải Phù Hợp Với Bài Toán**: Chunk quá nhỏ (100 tokens) sẽ thiếu ngữ cảnh; chunk quá to (2000 tokens) sẽ làm loãng thông tin và tốn token; kích thước 400-800 tokens là điểm ngọt (Sweet Spot).
- **Luôn Kèm Metadata Phân Quyền**: Khi truy vấn Vector DB, BẮT BUỘC phải lọc theo `tenant_id` hoặc quyền hạn của người dùng để ngăn nhân viên xem được tài liệu của phòng nhân sự/lương bổng.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Mô hình trả lời đúng nhưng trích dẫn nhầm nguồn**: Do chunking bị cắt vụn mất tiêu đề tài liệu -> Khắc phục: Bổ sung tiêu đề tài liệu và breadcrumbs vào đầu mỗi chunk trước khi embedding (Contextual Chunking).
- **LLM bị ảo giác khi tài liệu không có thông tin**: Do LLM cố gắng đoán mò -> Khắc phục: Huấn luyện qua System Prompt và đặt nhiệt độ thấp `temperature: 0.0`.

## 6. Step-by-Step Execution Workflow
1. Trích xuất và làm sạch văn bản: Loại bỏ thẻ HTML rác, bảng biểu bị vỡ, khoảng trắng thừa.
2. Phân đoạn văn bản (Chunking Strategy): Áp dụng Recursive Character Chunking hoặc Semantic Chunking với kích thước đoạn tối ưu (ví dụ: 500 tokens) kèm phần gối đầu (Overlap 10% - 50 tokens) để giữ nguyên vẹn ngữ cảnh.
3. Sinh Vector Embeddings và đẩy vào Vector Database kèm Metadata đầy đủ (Tên tài liệu, Trang số, Ngày tạo, ID phân quyền).
4. Khi người dùng hỏi: Áp dụng **Hybrid Search**: Chạy đồng thời Vector Search (tìm theo ý nghĩa ngữ nghĩa) và BM25 Keyword Search (tìm chính xác tên riêng, mã sản phẩm) rồi kết hợp điểm số qua thuật toán RRF (Reciprocal Rank Fusion).
5. Tái xếp hạng (Re-ranking): Sử dụng mô hình Cross-Encoder (như Cohere Rerank hoặc BGE-Reranker) để chọn ra Top 3-5 đoạn văn bản thực sự liên quan nhất.
6. Đóng gói Prompt Ngữ cảnh: Nhúng các đoạn trích dẫn vào System Prompt với chỉ dẫn nghiêm ngặt: *'Chỉ trả lời dựa trên ngữ cảnh được cung cấp; nếu không có thông tin, hãy trả lời là không biết, không được tự suy diễn'*. Khởi chạy LLM sinh câu trả lời kèm nguồn trích dẫn.

## 7. Concrete Examples
### Ví dụ triển khai chuẩn mực:
```typescript
// src/rag/ragPromptBuilder.ts
export function buildRagPrompt(query: string, contexts: RetrievedChunk[]) {
  const formattedContext = contexts
    .map((c, i) => `[Nguồn ${i + 1}] (${c.metadata.source}, Trang ${c.metadata.page}):\n${c.text}`)
    .join('\n\n');

  return `Bạn là trợ lý AI chuyên nghiệp. Hãy trả lời câu hỏi dưới đây chỉ dựa vào thông tin được cung cấp trong phần NGỮ CẢNH. Kèm theo số hiệu nguồn trích dẫn [Nguồn X] trong câu trả lời. Nếu ngữ cảnh không có thông tin, hãy trả lời: 'Tôi không tìm thấy thông tin này trong tài liệu.'\n\nNGỮ CẢNH:\n${formattedContext}\n\nCÂU HỎI:\n${query}`;
}
```

### Lệnh xác minh & thực thi:
- Kiểm tra truy vấn Vector DB: `curl http://localhost:6333/collections/knowledge/points/search ...`
- Chạy unit test quy trình RAG: `npm test -- tests/rag/retrievalPipeline.spec.ts`
- Đo lường độ tương đồng cosine của embedding mẫu.

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước kiểm tra biên và giả định hệ thống luôn ở trạng thái lý tưởng.
- **Anti-Pattern 2**: Không ghi nhận nhật ký kiểm toán hoặc bỏ qua việc xử lý ngoại lệ lúc runtime.
- **Trap**: Bỏ qua các rào chắn an toàn hoặc cố tình chạy script không qua kiểm thử tự động.

## 9. Quality Gates & Acceptance Criteria
- QG-04: Thời gian trích xuất tài liệu (Retrieval Latency) đạt dưới 200ms.
- QG-10: 100% câu trả lời đều có trích dẫn nguồn (Source Citation: File name, Page/Section) rõ ràng.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động trước khi coi là hoàn thành.

## 10. Security & Safety Boundaries
- Lọc sạch các chỉ dẫn Prompt Injection độc hại có thể ẩn giấu trong các tệp tài liệu do người dùng tải lên (Indirect Prompt Injection Defense).
- Không bao giờ thực thi mã nguồn hoặc thay đổi cấu hình trên môi trường sản xuất mà thiếu cơ chế rollback an toàn.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Có thể kích hoạt trực tiếp từ terminal hoặc extension tương thích trong VS Code / Cursor / Windsurf.

## 12. Deliverables & Output Artifacts
- Module phân đoạn và nhúng tài liệu (`src/rag/ingestionService.ts`).
- Module tìm kiếm lai và tái xếp hạng (`src/rag/hybridSearchService.ts`).
- Bộ test tích hợp kiểm chứng luồng hỏi đáp.

## 13. Related & Complementary Skills
- `dex-development-workflow`: Quy trình phát triển tiêu chuẩn.
- `dex-code-verification`: Xác minh chất lượng và tính đúng đắn của mã nguồn.
- `dex-master-orchestrator`: Bộ điều phối trung tâm kết nối kỹ năng này với các kỹ năng khác trong hệ thống.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư hoặc AI Agent tiếp nhận yêu cầu liên quan đến **dex-rag-pipelines**.
1. Đọc kỹ đầu vào và các ràng buộc kỹ thuật tại mục 4.
2. Thực thi tuần tự 6 bước trong Workflow tại mục 6.
3. Chạy các lệnh kiểm chứng tại mục 7 và đối chiếu với Quality Gates tại mục 9.
4. Đóng gói deliverables theo danh sách tại mục 12 và báo cáo kết quả kèm bằng chứng xác thực.
