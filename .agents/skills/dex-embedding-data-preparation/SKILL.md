---
name: dex-embedding-data-preparation
description: Prepare, chunk, enrich, and deduplicate textual corpora for high-quality dense vector embedding generation. Use when ingesting knowledge bases, technical documentation, or customer support archives into enterprise vector stores.
---

# dex-embedding-data-preparation

## 1. Purpose & Scope
Chuẩn bị, phân đoạn (chunking), làm giàu metadata và khử trùng lặp dữ liệu văn bản trước khi đưa vào mô hình sinh vector embedding; áp dụng các chiến lược phân đoạn ngữ nghĩa (Semantic Chunking) để duy trì tính toàn vẹn của ngữ cảnh và tối ưu hóa độ chính xác truy hồi.

## 2. When to Use
- Khi nạp kho tài liệu kỹ thuật, cẩm nang nghiệp vụ hoặc dữ liệu hỏi đáp (FAQ) vào Vector Database (Pinecone, Qdrant, Milvus, pgvector).
- Khi các đoạn văn bản bị cắt cụt ngang câu hoặc chia tách tiêu đề khỏi nội dung làm giảm sút chất lượng tìm kiếm RAG.
- Khi cần làm giàu metadata (tác giả, ngày ban hành, phiên bản, thẻ danh mục) để phục vụ bộ lọc phân quyền.

## 3. When NOT to Use
- Khi dữ liệu đầu vào là văn bản ngắn dưới 100 từ có thể nhúng trực tiếp toàn bộ mà không cần phân đoạn.
- Khi xây dựng hệ thống tìm kiếm từ khóa thuần túy (Lexical Full-Text Search) chỉ cần chỉ mục nghịch đảo BM25.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Văn bản thô (Markdown, PDF, HTML, DOCX), mô hình tokenizer tương ứng với embedding model (ví dụ: `cl100k_base` cho OpenAI text-embedding-3).
- **Quyền hạn truy cập:** Quyền đọc kho dữ liệu tài liệu nguồn và quyền ghi vào pipeline xử lý dữ liệu.

## 5. Core Concepts & Taxonomy
- **Semantic Chunking:** Phân đoạn văn bản dựa trên khoảng cách ngữ nghĩa giữa các câu liên tiếp thay vì cắt cứng theo số lượng ký tự hoặc tokens.
- **Chunk Overlap:** Phần giao thoa giữa hai đoạn liên tiếp (ví dụ: 10-20% kích thước chunk) để bảo toàn mối liên kết ngữ cảnh ở ranh giới cắt.
- **Metadata Enrichment:** Tự động bổ sung tóm tắt, từ khóa trích xuất, và chuỗi breadcrumb tiêu đề (`H1 > H2 > H3`) vào đầu mỗi chunk.

## 6. Step-by-Step Execution Workflow
1. Làm sạch văn bản thô: loại bỏ mã HTML thừa, chuẩn hóa khoảng trắng và ký tự ngắt dòng UTF-8.
2. Phân tích cấu trúc phân cấp tài liệu dựa trên các thẻ tiêu đề Markdown (H1, H2, H3).
3. Áp dụng giải pháp phân đoạn thích ứng: ưu tiên cắt theo ranh giới đoạn văn và câu hoàn chỉnh với giới hạn token mục tiêu (ví dụ: 512 tokens kèm overlap 64 tokens).
4. Ghép chuỗi ngữ cảnh cha (Hierarchy Breadcrumb) vào đầu mỗi chunk để model embedding hiểu được vị trí của đoạn văn.
5. Tính toán mã băm nội dung (SHA-256) và kiểm tra tương đồng Cosine để loại bỏ các chunk trùng lặp hoặc cận trùng lặp.
6. Xuất danh sách chunks chuẩn hóa kèm metadata đầy đủ để nạp vào embedding pipeline.

## 7. Concrete Examples
### Ví dụ phân đoạn văn bản bảo toàn tiêu đề cha (Hierarchy Breadcrumb) trong Python:
```python
import tiktoken

def create_enriched_chunks(doc_title: str, section_header: str, paragraphs: list[str], max_tokens=500, overlap=50) -> list[dict]:
    enc = tiktoken.get_encoding("cl100k_base")
    header_prefix = f"Document: {doc_title} > Section: {section_header}\nContent: "
    prefix_tokens = len(enc.encode(header_prefix))
    available_tokens = max_tokens - prefix_tokens

    chunks = []
    current_text = ""

    for p in paragraphs:
        test_text = f"{current_text}\n\n{p}".strip() if current_text else p
        if len(enc.encode(test_text)) <= available_tokens:
            current_text = test_text
        else:
            if current_text:
                chunks.append({
                    "text": header_prefix + current_text,
                    "metadata": {"doc": doc_title, "section": section_header, "token_count": len(enc.encode(header_prefix + current_text))}
                })
            current_text = p

    if current_text:
        chunks.append({
            "text": header_prefix + current_text,
            "metadata": {"doc": doc_title, "section": section_header, "token_count": len(enc.encode(header_prefix + current_text))}
        })

    return chunks
```

## 8. Anti-Patterns & Common Traps
- **Fixed-Character Blind Slicing:** Cắt chuỗi theo `text[i:i+1000]` làm đứt đôi từ ngữ và chia tách bảng dữ liệu hoặc khối mã code thành các mảnh vô nghĩa.
- **Orphan Chunking:** Lưu trữ đoạn trích mà không lưu metadata nguồn, dẫn tới khi LLM trả lời không thể trích dẫn được trang tài liệu gốc.
- **Ingesting Duplicate Chunks:** Nạp nhiều phiên bản tài liệu gần giống nhau làm lãng phí dung lượng vector database và gây nhiễu kết quả truy hồi.

## 9. Quality Gates & Acceptance Criteria
- **QG-02**: 100% các chunk tạo ra có số lượng tokens nằm trong khoảng giới hạn của embedding model.
- **QG-06**: Quá trình làm sạch dữ liệu kiểm tra và loại bỏ hoàn toàn các thông tin PII nhạy cảm hoặc mật khẩu.
- **QG-09**: Tất cả các chunk đều chứa metadata trích dẫn nguồn hợp lệ.

## 10. Security & Safety Boundaries
- Quét và lọc thông tin định danh cá nhân (PII Redaction) trước khi gửi văn bản tới API sinh embedding bên thứ ba.
- Phân quyền truy cập tài liệu bằng cách gắn danh sách quyền (Access Control List / Tenant ID) vào metadata của từng chunk.

## 11. Platform Adapters
- **Frameworks**: LangChain TextSplitters, LlamaIndex NodeParsers, Unstructured.io.
- **Tokenizers**: `tiktoken`, HuggingFace `tokenizers`.

## 12. Deliverables & Output Artifacts
- Pipeline làm sạch và phân đoạn dữ liệu văn bản.
- Bộ kiểm thử tự động xác minh không làm đứt đôi câu văn.
- Báo cáo thống kê phân bố kích thước chunk và tỷ lệ trùng lặp đã loại bỏ.

## 13. Related & Complementary Skills
dex-rag-pipelines, dex-hybrid-search-fusion, dex-context-window-budgeting

## 14. Realistic Usage Example
```powershell
# Chạy pipeline xử lý dữ liệu và tạo embedding chunks
python scripts/prepare_embeddings.py --input docs/manuals --output chunks.jsonl
```
