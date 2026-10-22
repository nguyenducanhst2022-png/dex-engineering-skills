---
name: dex-search-engineering
description: Design full-text search, semantic search, inverted index optimization, faceted filtering, and autocomplete using Elasticsearch, Meilisearch, or PostgreSQL tsvector. Use when implementing search bars, faceted filters, or ranking search results.
---

# dex-search-engineering

## 1. Purpose & Scope
Thiết kế và tối ưu hóa hệ thống tìm kiếm toàn văn (Full-Text Search) và tìm kiếm ngữ nghĩa; cấu hình bộ chỉ mục đảo (Inverted Index), tính toán độ tương đồng và xếp hạng kết quả (BM25 / TF-IDF), hỗ trợ bộ lọc đa chiều (Faceted Filtering), tự động hoàn thành từ khóa (Autocomplete) và xử lý lỗi chính tả (Typo Tolerance).

## 2. When to Use
- Khi câu truy vấn tìm kiếm bằng `LIKE '%keyword%'` trên cơ sở dữ liệu SQL trở nên quá chậm (>500ms) và gây nghẽn CPU.
- Khi người dùng cần tìm kiếm thông minh: Tìm không dấu, tìm từ đồng nghĩa, chấp nhận gõ sai chính tả nhẹ 1-2 ký tự.
- Khi xây dựng thanh tìm kiếm gợi ý tức thì (Search-as-you-type) hoặc bộ lọc sản phẩm đa thuộc tính trên trang thương mại điện tử.

## 3. When NOT to Use
- Tra cứu chính xác theo khóa chính (Primary Key lookup: `WHERE id = 123`).
- Xử lý các phép toán số liệu tài chính đòi hỏi tính toán số học chính xác tuyệt đối.

## 4. Prerequisites & Input Context
**Đầu vào cần thiết:**
- Mô hình dữ liệu cần đánh chỉ mục (Sản phẩm, Bài viết, Tài liệu).
- Công cụ tìm kiếm mục tiêu (PostgreSQL Full-Text Search `tsvector`, Meilisearch, Elasticsearch, OpenSearch).
- Danh sách các thuộc tính tìm kiếm (Searchable attributes) và thuộc tính lọc (Filterable attributes).

**Điều kiện tiên quyết:**
- Công cụ tìm kiếm mục tiêu đã được cài đặt và kết nối qua network ổn định.
- Đã thiết lập cơ chế đồng bộ dữ liệu từ DB chính sang Search Engine (qua CDC Debezium, Outbox worker hoặc application hooks).

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**: Nắm vững cơ chế vận hành theo chuẩn Agent Skills, tuân thủ nghiêm ngặt tính xác định và ranh giới trách nhiệm.
- **Quy tắc quyết định kỹ thuật**:
- **Cấm Dùng `LIKE %...%` Cho Dữ Liệu Lớn**: Tuyệt đối không dùng toán tử `LIKE '%...'` trên bảng trên 50,000 dòng vì sẽ làm Full Table Scan; bắt buộc phải dùng Inverted Index.
- **Không Tìm Kiếm Toàn Bộ Thuộc Tính**: Chỉ đánh chỉ mục tìm kiếm trên các trường thực sự cần thiết (tiêu đề, tóm tắt, tag); không đưa toàn bộ dữ liệu log hoặc JSON thô vào searchable attributes.
- **Chống Đơ UI Khi Autocomplete**: Phía client bắt buộc phải có Debounce (ví dụ: 300ms) trước khi gửi truy vấn tìm kiếm lên server.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Dữ liệu trong Search Engine bị lệch so với Database chính**: Do mạng chập chờn lúc gọi đồng bộ -> Khắc phục: Sử dụng Transactional Outbox Pattern hoặc chạy cronjob đối chiếu lại dữ liệu định kỳ mỗi đêm.
- **Bộ nhớ Search Engine bị phình to quá mức**: Do lưu trữ quá nhiều trường dữ liệu thừa trong index -> Khắc phục: Chỉ lưu các trường cần tìm kiếm và ID, khi hiển thị chi tiết thì đọc từ primary DB.

## 6. Step-by-Step Execution Workflow
1. Lựa chọn công nghệ: Dùng **PostgreSQL `tsvector` + GIN Index** nếu quy mô vừa (<1 triệu bản ghi) để tránh phức tạp hạ tầng; dùng **Meilisearch / Elasticsearch** nếu cần tìm kiếm tốc độ siêu cao, typo tolerance mạnh và quy mô lớn.
2. Thiết kế Index Schema: Phân loại rạch ròi giữa `Searchable Attributes` (title, description), `Filterable Attributes` (category, price_range, in_stock) và `Sortable Attributes` (created_at, rating).
3. Cấu hình bộ phân tích ngôn ngữ (Language Analyzers / Tokenizers) và bộ loại bỏ từ dừng (Stop words).
4. Triển khai cơ chế đồng bộ dữ liệu (Data Sync): Đảm bảo khi bản ghi trong DB được tạo/sửa/xóa, chỉ mục tìm kiếm được cập nhật tương ứng.
5. Xây dựng API tìm kiếm hỗ trợ phân trang (Pagination), làm nổi bật từ khóa (Highlighting) và Faceted Search counts.
6. Kiểm tra độ chính xác và hiệu năng truy vấn dưới 50ms.

## 7. Concrete Examples
### Ví dụ triển khai chuẩn mực:
```sql
-- PostgreSQL Full-Text Search với GIN Index tối ưu
ALTER TABLE products ADD COLUMN tsv tsvector GENERATED ALWAYS AS (
  setweight(to_tsvector('simple', coalesce(title, '')), 'A') ||
  setweight(to_tsvector('simple', coalesce(description, '')), 'B')
) STORED;

CREATE INDEX idx_products_tsv ON products USING GIN(tsv);
```

### Lệnh xác minh & thực thi:
- Kiểm tra câu lệnh tìm kiếm trong PostgreSQL: `EXPLAIN ANALYZE SELECT * FROM products WHERE tsv_content @@ to_tsquery('simple', 'laptop');`
- Kiểm tra trạng thái Meilisearch Index: `curl http://localhost:7700/indexes/products/stats`
- Chạy unit test tìm kiếm: `npm test -- tests/search/productSearch.spec.ts`

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước kiểm tra biên và giả định hệ thống luôn ở trạng thái lý tưởng.
- **Anti-Pattern 2**: Không ghi nhận nhật ký kiểm toán hoặc bỏ qua việc xử lý ngoại lệ lúc runtime.
- **Trap**: Bỏ qua các rào chắn an toàn hoặc cố tình chạy script không qua kiểm thử tự động.

## 9. Quality Gates & Acceptance Criteria
- QG-04: Thời gian phản hồi của truy vấn tìm kiếm p95 đạt dưới 50ms.
- QG-05: Kịch bản kiểm tra tìm kiếm có dấu, không dấu và gõ sai chính tả 1 ký tự đều trả về đúng kết quả mong đợi.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động trước khi coi là hoàn thành.

## 10. Security & Safety Boundaries
- Làm sạch chuỗi truy vấn của người dùng trước khi đưa vào Search Query để ngăn chặn tấn công Search Injection (Lucene query injection).
- Đảm bảo các bộ lọc phân quyền (Tenant ID, Permissions) luôn được áp dụng ngầm trong mọi câu truy vấn.
- Không bao giờ thực thi mã nguồn hoặc thay đổi cấu hình trên môi trường sản xuất mà thiếu cơ chế rollback an toàn.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Có thể kích hoạt trực tiếp từ terminal hoặc extension tương thích trong VS Code / Cursor / Windsurf.

## 12. Deliverables & Output Artifacts
- File cấu hình Index và Schema (`src/search/indexes/productIndex.ts`).
- Service tìm kiếm và đồng bộ dữ liệu (`src/search/searchService.ts`).
- File unit test kiểm tra độ chính xác của kết quả tìm kiếm.

## 13. Related & Complementary Skills
- `dex-development-workflow`: Quy trình phát triển tiêu chuẩn.
- `dex-code-verification`: Xác minh chất lượng và tính đúng đắn của mã nguồn.
- `dex-master-orchestrator`: Bộ điều phối trung tâm kết nối kỹ năng này với các kỹ năng khác trong hệ thống.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư hoặc AI Agent tiếp nhận yêu cầu liên quan đến **dex-search-engineering**.
1. Đọc kỹ đầu vào và các ràng buộc kỹ thuật tại mục 4.
2. Thực thi tuần tự 6 bước trong Workflow tại mục 6.
3. Chạy các lệnh kiểm chứng tại mục 7 và đối chiếu với Quality Gates tại mục 9.
4. Đóng gói deliverables theo danh sách tại mục 12 và báo cáo kết quả kèm bằng chứng xác thực.
