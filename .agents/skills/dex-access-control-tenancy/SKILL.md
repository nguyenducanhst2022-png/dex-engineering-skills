---
name: dex-access-control-tenancy
description: Implement fine-grained access control, Role-Based Access Control (RBAC), Attribute-Based Access Control (ABAC), multi-tenant data isolation, row-level security (RLS), and tenant scoping policies. Use when implementing permissions, authorization, or multi-tenancy.
---

# dex-access-control-tenancy

## 1. Purpose & Scope
Thiết lập hệ thống phân quyền chi tiết (Fine-grained Authorization) và cách ly dữ liệu đa người thuê (Multi-Tenant Isolation); triển khai mô hình phân quyền theo vai trò (RBAC), phân quyền theo thuộc tính động (ABAC), và thực thi chính sách bảo vệ dữ liệu ở cấp độ dòng (Row-Level Security - RLS) trong cơ sở dữ liệu; đảm bảo người dùng chỉ truy cập đúng dữ liệu thuộc thẩm quyền của tổ chức mình.

## 2. When to Use
- Khi ứng dụng mở rộng từ đơn người dùng sang mô hình SaaS phục vụ nhiều tổ chức (Multi-tenant SaaS).
- Khi có nguy cơ người dùng thuộc công ty A xem hoặc sửa được hóa đơn của công ty B do thiếu điều kiện lọc `tenant_id`.
- Khi cần hỗ trợ phân quyền tùy biến linh hoạt cho từng phòng ban (Admin, Manager, Member, Guest).

## 3. When NOT to Use
- Xác thực danh tính ban đầu (dùng `dex-auth-session-lifecycle`).
- Kiểm soát truy cập tài nguyên hạ tầng đám mây cấp DevOps (dùng AWS IAM / Kubernetes RBAC).

## 4. Prerequisites & Input Context
**Đầu vào cần thiết:**
- Mô hình người thuê (Database per Tenant, Schema per Tenant, hoặc Shared Database with Tenant ID Column).
- Ma trận quyền hạn nghiệp vụ (Permissions Matrix: Roles -> Resources -> Actions).
- Ngữ cảnh người dùng (Tenant ID, User ID, Roles, Attributes, IP, Device).

**Điều kiện tiên quyết:**
- Người dùng đã được xác thực danh tính hợp lệ trước khi vào tầng kiểm tra quyền hạn.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**: Nắm vững cơ chế vận hành theo chuẩn Agent Skills, tuân thủ nghiêm ngặt tính xác định và ranh giới trách nhiệm.
- **Quy tắc quyết định kỹ thuật**:
- **Bảo Vệ Ở Tầng Cơ Sở Dữ Liệu (Defense in Depth with RLS)**: Không chỉ dựa vào câu lệnh `WHERE tenant_id = ?` ở mã nguồn backend; bắt buộc phải có chính sách Row-Level Security ở tầng Database để phòng ngừa lập trình viên quên viết điều kiện `WHERE`.
- **Nguyên Tắc Đặc Quyền Tối Thiểu (Least Privilege)**: Mặc định từ chối mọi quyền truy cập (Deny by Default); chỉ mở quyền khi người dùng có gán quyền tường minh.
- **Không Cho Phép Client Truyền `tenant_id` Tùy Ý**: `tenant_id` phải được trích xuất an toàn từ Access Token đã được ký số của người dùng, không được tin cậy tham số query string do client gửi lên.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Lập trình viên quên thêm `WHERE tenant_id = x` làm lộ thông tin khách hàng**: Do query tay bằng ORM -> Khắc phục: PostgreSQL RLS chặn ngay tại tầng DB, câu truy vấn tự động chỉ trả về dữ liệu của đúng tenant hiện tại.
- **Người dùng đổi quyền nhưng quyền cũ vẫn lưu trong token suốt 24h**: Do lưu quyền vào static JWT -> Khắc phục: Kiểm tra quyền hạn trực tiếp từ cache Redis hoặc dùng token có thời hạn ngắn 5 phút.

## 6. Step-by-Step Execution Workflow
1. Chọn mô hình cách ly đa người thuê: Khuyến nghị dùng CSDL chung với cột `tenant_id` kết hợp PostgreSQL Row-Level Security (RLS) để tối ưu chi phí và bảo mật tuyệt đối.
2. Kích hoạt RLS trên toàn bộ bảng dữ liệu chứa thông tin người dùng: `ALTER TABLE ... ENABLE ROW LEVEL SECURITY`.
3. Thiết lập chính sách bảo vệ RLS: Chỉ cho phép đọc/ghi dữ liệu khi cột `tenant_id` khớp với biến phiên hiện tại (`current_setting('app.current_tenant_id')`).
4. Triển khai middleware tự động gắn `tenant_id` vào mọi câu truy vấn hoặc thiết lập session context trước khi thực thi query.
5. Xây dựng tầng phân quyền RBAC/ABAC kiểm tra quyền hạn thao tác (ví dụ: `can(user, 'invoice:delete', invoice)`).
6. Viết bộ kiểm thử kiểm tra tính rò rỉ chéo tenant: Giả lập User công ty A cố tình truy vấn bản ghi của công ty B và kiểm tra xem hệ thống có trả về 403/404 hay không.

## 7. Concrete Examples
### Ví dụ triển khai chuẩn mực:
```sql
-- PostgreSQL Row-Level Security (RLS) Policy
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation_policy ON orders
  FOR ALL
  USING (tenant_id = NULLIF(current_setting('app.current_tenant_id', true), '')::uuid)
  WITH CHECK (tenant_id = NULLIF(current_setting('app.current_tenant_id', true), '')::uuid);
```

### Lệnh xác minh & thực thi:
- Kiểm tra trạng thái kích hoạt RLS: `SELECT tablename, rowsecurity FROM pg_tables WHERE schemaname = 'public';`
- Chạy kiểm thử truy cập chéo tenant: `npm run test:tenant-isolation`
- Kiểm tra chính sách phân quyền ABAC: `npm run test:permissions`

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước kiểm tra biên và giả định hệ thống luôn ở trạng thái lý tưởng.
- **Anti-Pattern 2**: Không ghi nhận nhật ký kiểm toán hoặc bỏ qua việc xử lý ngoại lệ lúc runtime.
- **Trap**: Bỏ qua các rào chắn an toàn hoặc cố tình chạy script không qua kiểm thử tự động.

## 9. Quality Gates & Acceptance Criteria
- QG-03: 100% các bảng dữ liệu nghiệp vụ nhạy cảm đều được kích hoạt Row-Level Security.
- QG-09: Kiểm thử truy cập chéo giữa 2 tenant trả về lỗi 403 Forbidden hoặc 404 Not Found.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động trước khi coi là hoàn thành.

## 10. Security & Safety Boundaries
- Thiết lập cơ chế kiểm tra đặc quyền khẩn cấp (Superadmin bypass) có ghi vết kiểm toán (Audit Trail) không thể xóa sửa.
- Không bao giờ thực thi mã nguồn hoặc thay đổi cấu hình trên môi trường sản xuất mà thiếu cơ chế rollback an toàn.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Có thể kích hoạt trực tiếp từ terminal hoặc extension tương thích trong VS Code / Cursor / Windsurf.

## 12. Deliverables & Output Artifacts
- Script SQL kích hoạt chính sách Row-Level Security trên Postgres.
- Middleware phân quyền và thiết lập tenant context (`tenant.middleware.ts`).
- Ma trận phân quyền chi tiết (RBAC/ABAC policy engine).

## 13. Related & Complementary Skills
- `dex-development-workflow`: Quy trình phát triển tiêu chuẩn.
- `dex-code-verification`: Xác minh chất lượng và tính đúng đắn của mã nguồn.
- `dex-master-orchestrator`: Bộ điều phối trung tâm kết nối kỹ năng này với các kỹ năng khác trong hệ thống.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư hoặc AI Agent tiếp nhận yêu cầu liên quan đến **dex-access-control-tenancy**.
1. Đọc kỹ đầu vào và các ràng buộc kỹ thuật tại mục 4.
2. Thực thi tuần tự 6 bước trong Workflow tại mục 6.
3. Chạy các lệnh kiểm chứng tại mục 7 và đối chiếu với Quality Gates tại mục 9.
4. Đóng gói deliverables theo danh sách tại mục 12 và báo cáo kết quả kèm bằng chứng xác thực.
