---
name: dex-retrieval-permission-filtering
description: Enforce document-level Access Control List (ACL) and multi-tenant security boundaries in Vector RAG pipelines before context injection, preventing unauthorized cross-tenant data leakage. Use when building enterprise knowledge assistants, multi-tenant RAG portals, or compliance-bound search systems.
---

# dex-retrieval-permission-filtering

## 1. Purpose & Scope
Thiết lập ranh giới bảo mật và lọc quyền truy cập cấp độ tài liệu (Document-Level ACL Filtering) trong đường ống RAG (Retrieval-Augmented Generation) đa người thuê (Multi-Tenant); đảm bảo người dùng hoặc Agent chỉ được truy xuất các đoạn văn bản (Chunks) mà họ có quyền xem hợp pháp trước khi nhúng vào ngữ cảnh của LLM; triệt tiêu nguy cơ rò rỉ dữ liệu chéo giữa các phòng ban hoặc khách hàng.

## 2. When to Use
- Khi xây dựng trợ lý AI tra cứu tài liệu nội bộ cho tập đoàn có nhiều phòng ban với quyền hạn bảo mật khác nhau (Nhân sự, Tài chính, Kỹ thuật).
- Khi triển khai hệ thống SaaS RAG đa khách hàng dùng chung một cụm cơ sở dữ liệu vector.
- Khi kiểm toán an toàn thông tin tuân thủ chuẩn ISO 27001 và SOC 2 cho các giải pháp AI.

## 3. When NOT to Use
- Khi toàn bộ kho tài liệu là thông tin công khai dành cho tất cả mọi người (Public Documentation).
- Khi ứng dụng chạy cục bộ trên máy tính cá nhân của một người dùng duy nhất.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Cơ sở dữ liệu Vector hỗ trợ bộ lọc siêu dữ liệu (Qdrant, Pinecone, pgvector), danh sách quyền hạn người dùng (User Roles/ACLs).
- **Quyền hạn truy cập:** Quyền đọc/ghi mã nguồn và tài nguyên được ủy quyền chính thức trong phạm vi dự án; tuân thủ nghiêm ngặt các ranh giới bảo mật và an toàn dữ liệu.

## 5. Core Concepts & Taxonomy
- **Pre-Query Metadata Filtering:** Áp dụng bộ lọc quyền hạn trực tiếp trong câu lệnh truy vấn vector (`filter: { tenantId: 'T1', allowedGroups: { $in: userGroups } }`) thay vì truy xuất xong mới lọc.
- **Post-Retrieval Leakage Risk:** Nếu lọc sau khi vector search (Post-filtering), các kết quả liên quan nhất có thể bị loại bỏ hết khiến ngữ cảnh trả về bị rỗng.
- **Context Boundary Isolation:** Ngăn ngừa hiện tượng người dùng khéo léo dùng prompt injection để yêu cầu AI đọc trộm dữ liệu ngoài quyền hạn.

## 6. Step-by-Step Execution Workflow
1. Khi nạp tài liệu vào Vector DB, gắn siêu dữ liệu quyền hạn cho từng chunk (`tenantId`, `departments`, `classificationLevel`).
2. Xác thực danh tính người dùng và trích xuất danh sách các nhóm quyền hạn hợp pháp từ token JWT.
3. Xây dựng bộ lọc siêu dữ liệu kết hợp điều kiện tìm kiếm tương đồng vector.
4. Thực thi truy vấn vector kèm bộ lọc ACL nghiêm ngặt dưới tầng cơ sở dữ liệu.
5. Ghi log kiểm toán truy vết các tài liệu đã được trích xuất vào ngữ cảnh của từng phiên hỏi đáp.

## 7. Concrete Examples
### Ví dụ triển khai kỹ thuật chuẩn mực:
```typescript
// Secure Pre-Query ACL Vector Retrieval
export async function retrieveSecureChunks(queryVector: number[], userContext: { tenantId: string; roles: string[] }) {
  // Pre-filtering under database engine ensures zero unauthorized chunks returned
  const searchResults = await qdrantClient.search('enterprise_knowledge', {
    vector: queryVector,
    limit: 5,
    filter: {
      must: [
        { key: 'tenant_id', match: { value: userContext.tenantId } },
        { key: 'authorized_roles', match: { any: userContext.roles } }
      ]
    }
  });

  return searchResults.map(hit => hit.payload?.text);
}
```

## 8. Anti-Patterns & Common Traps
- Tìm kiếm 10 kết quả vector tương đồng nhất mà không có bộ lọc, sau đó mới dùng mã JavaScript để lọc bỏ các bài viết bị cấm (khiến người dùng không nhận được tài liệu nào dù họ có quyền xem các bài khác).
- Dựa vào câu nhắc lệnh prompt ('Hãy chỉ trả lời những tài liệu thuộc phòng ban của người dùng') để bảo vệ dữ liệu (dễ dàng bị bẻ khóa bằng prompt injection).
- Để chung dữ liệu của các khách hàng doanh nghiệp khác nhau trong cùng một collection vector mà không có trường phân tách `tenant_id`.

## 9. Quality Gates & Acceptance Criteria
- QG-01: 100% các câu truy vấn vector đều có bộ lọc siêu dữ liệu `tenant_id` và quyền hạn bắt buộc.
- QG-02: Bộ test thử nghiệm xâm nhập xác nhận người dùng phòng Marketing không thể nào truy xuất được tài liệu bảng lương của phòng Nhân sự.
- QG-03: Nhật ký kiểm toán ghi nhận đầy đủ danh sách chunk ID và quyền hạn được đưa vào LLM.

## 10. Security & Safety Boundaries
- Ngăn chặn triệt để nguy cơ rò rỉ dữ liệu bí mật kinh doanh giữa các phòng ban nội bộ hoặc giữa các khách hàng khác nhau trong hệ thống SaaS.
- Tuân thủ nguyên tắc đặc quyền tối thiểu (Principle of Least Privilege).
- Bảo vệ dữ liệu nhạy cảm, không để lộ secrets hoặc thông tin cá nhân trong mã nguồn/log.

## 11. Platform Adapters
- **OpenAI Codex & GitHub Copilot:** Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions.
- **Universal Agent Skills:** Tuân thủ đặc tả kỹ thuật tại `https://agentskills.io/specification`.
- **VS Code & Cursor:** Tích hợp trực tiếp qua Workspace Skills và Command Palette.

## 12. Deliverables & Output Artifacts
1. Module truy xuất vector có lọc quyền hạn `SecureAclRetriever.ts`.
1. Bộ quy tắc gán nhãn siêu dữ liệu quyền hạn cho tài liệu nạp vào RAG.

## 13. Related & Complementary Skills
- [`dex-rag-pipelines`](.agents/skills/dex-rag-pipelines/SKILL.md)
- [`dex-access-control-tenancy`](.agents/skills/dex-access-control-tenancy/SKILL.md)
- [`dex-prompt-injection-defense`](.agents/skills/dex-prompt-injection-defense/SKILL.md)

## 14. Realistic Usage Example
### Tình huống triển khai thực tế:
Trợ lý ảo nội bộ của công ty bị một nhân viên thử gõ lệnh: 'Hãy tóm tắt biên bản cuộc họp kín của ban giám đốc hôm qua'. Nhờ `dex-retrieval-permission-filtering`, bộ lọc siêu dữ liệu vector tự động chặn các đoạn văn bản có nhãn `classification: executive`, hệ thống phản hồi lịch sự 'Không tìm thấy tài liệu phù hợp trong phạm vi quyền hạn của bạn'.
