---
name: dex-documentation-as-code
description: Manage technical documentation as code, maintaining Architecture Decision Records (ADR), executable docs, doctests, OpenAPI specs, Mermaid diagrams, and automated doc generation pipelines. Use when documenting architectures, APIs, or engineering practices.
---

# dex-documentation-as-code

## 1. Purpose & Scope
Quản lý và duy trì tài liệu kỹ thuật theo triết lý 'Tài liệu như Mã nguồn' (Documentation-as-Code); đồng bộ hóa tài liệu cùng mã nguồn trong Git, ghi chép các quyết định kiến trúc quan trọng thông qua Architecture Decision Records (ADRs), tích hợp sơ đồ đồ họa dạng văn bản (Mermaid), và tự động kiểm thử tính đúng đắn của ví dụ mã trong tài liệu (Doctests).

## 2. When to Use
- Khi tài liệu dự án bị lỗi thời (Out-of-date) so với mã nguồn thực tế đang chạy.
- Khi các đoạn code ví dụ trong tài liệu hướng dẫn bị lỗi cú pháp do không ai kiểm thử.
- Khi cần lưu vết lý do tại sao nhóm lại chọn công nghệ A thay vì công nghệ B (Kiến trúc không được ghi chép).

## 3. When NOT to Use
- Tài liệu marketing quảng bá sản phẩm hoặc bài viết mạng xã hội.

## 4. Prerequisites & Input Context
**Đầu vào cần thiết:**
- Các quyết định thiết kế kiến trúc đang thảo luận.
- Mã nguồn API và các ghi chú mã nguồn (JSDoc, Docstrings, Rustdoc).
- Công cụ sinh tài liệu tĩnh (VitePress, Docusaurus, MkDocs, Astro Starlight).

**Điều kiện tiên quyết:**
- Kho tài liệu nằm cùng trong Git repo (`docs/`) và tuân thủ quy trình Pull Request như code.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**: Nắm vững cơ chế vận hành theo chuẩn Agent Skills, tuân thủ nghiêm ngặt tính xác định và ranh giới trách nhiệm.
- **Quy tắc quyết định kỹ thuật**:
- **Mọi Quyết Định Kiến Trúc Quan Trọng Đều Phải Có ADR**: Không chấp nhận thay đổi cấu trúc cốt lõi mà không có file ADR giải thích bối cảnh, các giải pháp thay thế và lý do lựa chọn.
- **Executable Code Samples (Code Mẫu Phải Chạy Được)**: Các ví dụ mã trong tài liệu phải được kiểm thử tự động trong CI (sử dụng doctest hoặc markdown runner).
- **Không Dùng Ảnh Chụp Màn Hình Cho Sơ Đồ Kỹ Thuật**: Tất cả sơ đồ kiến trúc, flowchart, sequence diagram phải được vẽ bằng Mermaid text.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Người dùng làm theo tài liệu bị lỗi 'Command not found'**: Do tài liệu viết sai lệnh hoặc phiên bản cũ -> Khắc phục: CI chạy kiểm tra markdown doctest tự động phát hiện lỗi.
- **Links trong tài liệu bị 404 sau khi đổi tên file**: Do không kiểm tra link -> Khắc phục: Cài đặt markdown-link-check vào pipeline CI.

## 6. Step-by-Step Execution Workflow
1. Thiết lập cấu trúc thư mục tài liệu chuẩn: `docs/adr/` (Quyết định kiến trúc), `docs/guides/` (Hướng dẫn), `docs/api/` (Tài liệu API).
2. Khởi tạo mẫu ADR theo chuẩn MADR (Markdown Architectural Decision Records).
3. Nhúng sơ đồ kiến trúc bằng mã nguồn Mermaid trực tiếp trong Markdown để dễ dàng theo dõi diff trên GitHub.
4. Tự động trích xuất tài liệu API từ OpenAPI/Swagger specs hoặc code docstrings.
5. Cấu hình kiểm thử tài liệu tự động (Doctests / Markdown link checking): Đảm bảo các đoạn code mẫu thực sự biên dịch và chạy được.
6. Tích hợp pipeline CI kiểm tra liên kết hỏng (Broken links) và tự động build/deploy trang tài liệu tĩnh khi merge vào branch main.

## 7. Concrete Examples
### Ví dụ triển khai chuẩn mực:
```markdown
# ADR 0005: Use PostgreSQL as Primary Relational Store

## Context
We need an ACID-compliant database to handle transactional payment workflows.

## Considered Options
1. PostgreSQL 16
2. MongoDB 7.0
3. MySQL 8.0

## Decision
We choose PostgreSQL 16 because of its robust JSONB support, row-level security, and mature ecosystem.

## Consequences
- Positive: Strong relational consistency, excellent tooling.
- Negative: Requires connection pooling (PgBouncer) under high concurrency.
```

### Lệnh xác minh & thực thi:
- Kiểm tra liên kết hỏng trong tài liệu: `npx markdown-link-check docs/**/*.md`
- Kiểm tra và thực thi code blocks trong markdown: `npx markdown-doctest`
- Build thử nghiệm trang tài liệu tĩnh: `npm run docs:build`

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước kiểm tra biên và giả định hệ thống luôn ở trạng thái lý tưởng.
- **Anti-Pattern 2**: Không ghi nhận nhật ký kiểm toán hoặc bỏ qua việc xử lý ngoại lệ lúc runtime.
- **Trap**: Bỏ qua các rào chắn an toàn hoặc cố tình chạy script không qua kiểm thử tự động.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Tài liệu chứa đầy đủ bối cảnh, sơ đồ Mermaid và ví dụ thực tế.
- QG-05: 0 liên kết bị hỏng (Broken Links: 0) và 100% doctests chạy thành công.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động trước khi coi là hoàn thành.

## 10. Security & Safety Boundaries
- Tuyệt đối không để lộ mật khẩu, API key nội bộ hoặc địa chỉ IP môi trường staging/production trong các ví dụ tài liệu.
- Không bao giờ thực thi mã nguồn hoặc thay đổi cấu hình trên môi trường sản xuất mà thiếu cơ chế rollback an toàn.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Có thể kích hoạt trực tiếp từ terminal hoặc extension tương thích trong VS Code / Cursor / Windsurf.

## 12. Deliverables & Output Artifacts
- Thư mục ADRs (`docs/adr/0001-record-architecture-decisions.md`).
- Trang tài liệu tĩnh được sinh tự động.
- Sơ đồ Mermaid phản ánh chính xác kiến trúc hệ thống.

## 13. Related & Complementary Skills
- `dex-development-workflow`: Quy trình phát triển tiêu chuẩn.
- `dex-code-verification`: Xác minh chất lượng và tính đúng đắn của mã nguồn.
- `dex-master-orchestrator`: Bộ điều phối trung tâm kết nối kỹ năng này với các kỹ năng khác trong hệ thống.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư hoặc AI Agent tiếp nhận yêu cầu liên quan đến **dex-documentation-as-code**.
1. Đọc kỹ đầu vào và các ràng buộc kỹ thuật tại mục 4.
2. Thực thi tuần tự 6 bước trong Workflow tại mục 6.
3. Chạy các lệnh kiểm chứng tại mục 7 và đối chiếu với Quality Gates tại mục 9.
4. Đóng gói deliverables theo danh sách tại mục 12 và báo cáo kết quả kèm bằng chứng xác thực.
