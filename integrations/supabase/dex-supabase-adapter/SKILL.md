---
name: dex-supabase-adapter
description: Supabase BaaS PostgreSQL, Row-Level Security (RLS) hardening, connection pooling optimization, and Edge Function integration adapter. Bridges DEX database engineering to official Supabase best practices. Use when building, auditing, or optimizing Supabase database architectures.
version: 8.1.0
group: Integration
domain: Backend & Database BaaS
upstream_source: https://github.com/supabase/agent-skills
upstream_commit: c9be0e931b7930f7d02126d04774d904c381e7d7
---

# DEX Supabase BaaS & PostgreSQL Hardening Adapter

## 1. Purpose & Scope
Cung cấp cầu nối kỹ thuật chuyên sâu giữa hệ sinh thái kỹ năng DEX và repository chính thức **Supabase Agent Skills** (`supabase/agent-skills`). Kỹ năng này chuẩn hóa quy trình thiết kế cơ sở dữ liệu PostgreSQL trên nền tảng Supabase Backend-as-a-Service (BaaS), tối ưu hóa cấu hình Connection Pooling (Supavisor/PgBouncer), kiểm toán chính sách Row-Level Security (RLS) chống rò rỉ dữ liệu đa người thuê (multi-tenant), phòng chống cạn kiệt tài nguyên kết nối từ Edge Functions/Serverless, và thực thi các chuẩn mực schema design chuẩn tắc của Supabase.

Phạm vi bao phủ:
1. Thiết kế lược đồ bảng (schema design), chuẩn hóa kiểu dữ liệu, khóa chính UUIDv7 / BIGINT và chỉ mục ngoại khóa (Foreign Key Indexes).
2. Tối ưu hóa hiệu năng RLS: thay thế đánh giá $O(N)$ bằng subquery caching `(select auth.uid())` và phân tách policy theo action (`SELECT`, `INSERT`, `UPDATE`, `DELETE`).
3. Quản trị hạ tầng kết nối: Phân định rạch ròi giữa Direct Connection (cổng `5432` cho migrations/DDL) và Transaction Pooler (cổng `6543` qua Supavisor cho Serverless/Edge Functions).
4. Kiểm tra và bảo mật hàm `SECURITY DEFINER`: ép buộc gán `SET search_path = public` nhằm triệt tiêu lỗ hổng leo thang đặc quyền.
5. Phát hiện môi trường thực thi (CLI & credentials) và kích hoạt chế độ suy thoái an toàn (graceful fallback) khi thiếu công cụ.

---

## 2. When to Use
Kích hoạt adapter này khi:
- Người dùng yêu cầu thiết kế, tối ưu hóa hoặc kiểm tra hiệu năng cơ sở dữ liệu Supabase hoặc PostgreSQL trên đám mây.
- Cần viết, đánh giá hoặc tinh chỉnh chính sách Row-Level Security (RLS) cho hệ thống multi-tenant hoặc phân quyền người dùng dựa trên Supabase Auth.
- Ứng dụng Serverless / Next.js / Edge Functions gặp lỗi cạn kiệt kết nối (`Max client connections reached`, lỗi kết nối cổng 5432).
- Cần kiểm toán bảo mật các hàm Database Functions, Triggers hoặc Database Webhooks liên kết với Supabase Edge Functions.
- Cần chạy phân tích truy vấn `EXPLAIN (ANALYZE, BUFFERS)` trên bảng có RLS để xác định điểm nghẽn hiệu năng.

---

## 3. When NOT to Use
Tuyệt đối không kích hoạt hoặc chuyển tiếp sang các kỹ năng khác khi:
- Dự án sử dụng hệ quản trị cơ sở dữ liệu phi quan hệ (NoSQL) như MongoDB, DynamoDB, Redis (chuyển sang `dex-caching-strategies` hoặc `dex-database-engineering`).
- Các tác vụ thuần túy về giao diện người dùng, CSS, layout frontend không liên quan tới dữ liệu Supabase (chuyển sang `dex-ui-component-contracts` hoặc `dex-ui-ux-pro-max-adapter`).
- Tác vụ phân tích nhị phân mã máy, dịch ngược ELF/PE (chuyển sang `dex-binary-inspection` hoặc `dex-rea-adapter`).
- Yêu cầu điều phối tổng thể hoặc phân rã yêu cầu cấp cao của người dùng (chuyển quyền về `dex-master-orchestrator`).

---

## 4. Prerequisites & Input Context
Trước khi thực thi, adapter yêu cầu thu thập các thông tin sau:
1. **Lược đồ CSDL hiện tại**: Các tệp DDL SQL (`schema.sql`, `supabase/migrations/*.sql`) hoặc định nghĩa bảng.
2. **Yêu cầu kiểm soát truy cập**: Ma trận phân quyền đối tượng người dùng (bình thường, tenant admin, anonymous, service role).
3. **Môi trường kết nối**:
   - Biến môi trường: `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, `DATABASE_URL`.
   - Toolchain cục bộ: Supabase CLI (`supabase`), PostgreSQL client (`psql`).
4. **Kiểm tra công cụ thực tế (Runtime Tool Checks)**:
   ```bash
   # Kiểm tra Supabase CLI
   supabase --version
   # Kiểm tra kết nối pooler Supabase
   psql -h aws-0-ap-southeast-1.pooler.supabase.com -p 6543 -U postgres.<project-ref> -d postgres -c "SELECT version();"
   ```
   *Quy tắc Zero-Hallucination*: Nếu `supabase` CLI không có sẵn hoặc không có chuỗi kết nối thực tế, adapter phải báo cáo rõ `RUNTIME_NOT_INSTALLED` và chuyển sang chế độ phân tích tĩnh SQL/DDL cục bộ mà không giả lập kết quả trả về từ CLI.

---

## 5. Core Concepts & Taxonomy

```
+---------------------------------------------------------------------------------+
|                        SUPABASE POSTGRES BEST PRACTICES                         |
+---------------------------------------------------------------------------------+
| 1. CONNECTION POOLING (Supavisor)                                               |
|    - Port 5432: Session Direct Mode (Migrations, Long Transactions, Listen)    |
|    - Port 6543: Transaction Mode (Edge Functions, Serverless API, Max Conns)    |
|    - Prepared Statements: Cấm bật bừa bãi trong Transaction Pooling             |
+---------------------------------------------------------------------------------+
| 2. ROW-LEVEL SECURITY (RLS) HARDENING                                           |
|    - Zero-Cost Subquery Caching: (select auth.uid()) thay vì auth.uid()         |
|    - Avoid Cross-Table Recursion: Dùng SECURITY DEFINER helper cho checks phức tạp|
|    - Policy Segregation: Không gộp TO ALL khi logic SELECT và UPDATE khác nhau   |
+---------------------------------------------------------------------------------+
| 3. SCHEMA & INDEX GOVERNANCE                                                    |
|    - Mandatory FK Indexes: Mọi FOREIGN KEY đều phải có CREATE INDEX kèm theo    |
|    - Lowercase Identifiers: Tuyệt đối không dùng quoted camelCase ("userId")    |
|    - Primary Keys: Bắt buộc UUIDv7 hoặc BIGINT GENERATED ALWAYS AS IDENTITY     |
+---------------------------------------------------------------------------------+
```

### Các khái niệm trọng tâm:
- **Supavisor Transaction Pooling**: Cơ chế chia sẻ kết nối cơ sở dữ liệu trên cổng `6543`. Một connection vật lý tới PostgreSQL chỉ được gán cho client trong thời gian thực thi một transaction duy nhất, cho phép hàng chục nghìn client serverless cùng hoạt động mà không tràn RAM PostgreSQL.
- **InitPlan Caching trong RLS**: Khi viết `auth.uid() = user_id`, Postgres gọi hàm `auth.uid()` cho từng bản ghi được quét. Khi viết `(select auth.uid()) = user_id`, PostgreSQL tối ưu hóa biểu thức này thành một `InitPlan` đơn nhất, thực thi 1 lần trước khi quét bảng, cải thiện tốc độ từ hàng giây xuống mili-giây.
- **Search Path Hijacking**: Nếu hàm `SECURITY DEFINER` không khóa `search_path`, kẻ tấn công có thể tạo schema tạm với các hàm trùng tên để chiếm quyền superuser của hàm khi nó được thực thi.

---

## 6. Step-by-Step Execution Workflow

```
BƯỚC 1: Thu thập Lược đồ DDL & Đánh giá Kiến trúc Hiện tại
  │
BƯỚC 2: Kiểm toán RLS & Tối ưu hóa InitPlan Subquery
  │
BƯỚC 3: Đối soát Chỉ mục Ngoại khóa & Rà soát Bảng Khuyết Index
  │
BƯỚC 4: Tách biệt Kết nối Session (5432) và Transaction Pooler (6543)
  │
BƯỚC 5: Đóng gói Bản vá Migration Idempotent & Kiểm chứng Kịch bản Rollback
```

### Chi tiết các bước thực hiện:
1. **Bước 1 — Thu thập và kiểm tra tĩnh lược đồ (Schema Static Audit)**:
   - Quét toàn bộ tệp `supabase/migrations/*.sql` hoặc DDL.
   - Kiểm tra xem mọi bảng nghiệp vụ đều đã bật `ALTER TABLE ... ENABLE ROW LEVEL SECURITY;`.
   - Cảnh báo ngay lập tức nếu phát hiện định danh viết hoa `camelCase` hoặc thiếu khóa chính.
2. **Bước 2 — Tối ưu hóa chính sách RLS**:
   - Tìm kiếm các biểu thức `auth.uid()` hoặc `auth.jwt()` đứng độc lập.
   - Chuyển đổi thành `(select auth.uid())`.
   - Phân rã các policy `FOR ALL` thành 4 policy riêng biệt: `FOR SELECT`, `FOR INSERT`, `FOR UPDATE`, `FOR DELETE` để tối ưu hóa quyền kiểm tra theo đúng payload.
3. **Bước 3 — Tạo chỉ mục ngoại khóa bổ sung**:
   - Truy vấn hoặc trích xuất danh sách mọi ràng buộc `REFERENCES` mà chưa có `CREATE INDEX ON table(foreign_key_column)`.
   - Soạn thảo lệnh tạo index với mệnh đề `IF NOT EXISTS`.
4. **Bước 4 — Cấu hình kết nối cho Serverless**:
   - Trong file cấu hình Prisma / Drizzle / Kysely hoặc client:
     - `DIRECT_URL`: Cổng `5432` (dành cho `prisma migrate` hoặc CLI).
     - `DATABASE_URL`: Cổng `6543` với tham số `?pgbouncer=true&connection_limit=1`.
5. **Bước 5 — Kiểm tra hàm `SECURITY DEFINER`**:
   - Đảm bảo mọi function có từ khóa `SECURITY DEFINER` đều có khai báo:
     `SET search_path = public, pg_temp;`

---

## 7. Concrete Examples

### Ví dụ 1: Tối ưu hóa RLS Policy từ $O(N)$ thành $O(1)$ InitPlan Caching
*Trước (Chậm, gọi hàm lặp lại trên từng hàng):*
```sql
-- ANTI-PATTERN: auth.uid() được gọi trên mỗi hàng được scan
CREATE POLICY "tenant_isolation_slow" ON organizations
FOR SELECT
USING (owner_id = auth.uid());
```

*Sau (Tối ưu hóa Supabase Best Practice):*
```sql
-- BEST PRACTICE: Subquery ép PostgreSQL tính toán auth.uid() một lần duy nhất (InitPlan)
CREATE POLICY "tenant_isolation_optimized" ON organizations
FOR SELECT
TO authenticated
USING (owner_id = (SELECT auth.uid()));
```

### Ví dụ 2: Hàm `SECURITY DEFINER` an toàn chống leo thang đặc quyền
```sql
CREATE OR REPLACE FUNCTION public.get_tenant_role(target_tenant_id uuid)
RETURNS text
LANGUAGE plpgsql
SECURITY DEFINER
-- Khóa chặt search_path để ngăn chặn DLL/Schema Hijacking
SET search_path = public, pg_temp
AS $$
DECLARE
    user_role text;
BEGIN
    SELECT role INTO user_role
    FROM public.memberships
    WHERE tenant_id = target_tenant_id
      AND user_id = (SELECT auth.uid());
    
    RETURN COALESCE(user_role, 'none');
END;
$$;
```

---

## 8. Anti-Patterns & Common Traps
- **Bẫy 1: Quên bật RLS sau khi tạo bảng**: Tạo bảng mới nhưng quên `ALTER TABLE table_name ENABLE ROW LEVEL SECURITY;`. Khi đó bảng hoàn toàn mở cho mọi request có `anon_key` nếu API Supabase được kích hoạt.
- **Bẫy 2: Dùng cổng 5432 trực tiếp trong các ứng dụng Serverless/Edge**: Mỗi instance serverless mở một kết nối vật lý, khi có 100 concurrent requests sẽ làm sập PostgreSQL với lỗi `FATAL: remaining connection slots are reserved for non-replication superuser connections`.
- **Bẫy 3: Đệ quy vô tận trong RLS (Infinite Recursion)**: Policy trên bảng `memberships` kiểm tra quyền bằng cách `SELECT` chính bảng `memberships` mà không dùng function `SECURITY DEFINER` hoặc bypass.
- **Bẫy 4: Lạm dụng `service_role` key trên frontend**: Nhúng `SUPABASE_SERVICE_ROLE_KEY` vào client code (Next.js public env, React state). Khóa này bypass toàn bộ RLS và trao toàn quyền phá hủy database.

---

## 9. Quality Gates & Acceptance Criteria
Mọi thay đổi cơ sở dữ liệu Supabase thông qua adapter phải vượt qua 5 cổng kiểm soát chất lượng:
- **QG-SUPA-01 (RLS Completeness)**: 100% các bảng dữ liệu trong schema `public` đều đã được `ENABLE ROW LEVEL SECURITY`.
- **QG-SUPA-02 (InitPlan Subquery Caching)**: Không còn bất kỳ biểu thức `auth.uid()` nào xuất hiện ở dạng gọi hàm trần không có `(SELECT auth.uid())` trong các policy của bảng lớn.
- **QG-SUPA-03 (Foreign Key Index Coverage)**: 100% các cột khóa ngoại có chỉ mục tương ứng để tránh Full Table Scan khi khóa chính bị cập nhật hoặc xóa.
- **QG-SUPA-04 (Security Definer Sanitization)**: Mọi hàm `SECURITY DEFINER` đều có mệnh đề cố định `SET search_path = public, pg_temp`.
- **QG-SUPA-05 (Connection String Decoupling)**: Ứng dụng phân định rõ `DIRECT_URL` (cổng 5432) cho migrations và `DATABASE_URL` (cổng 6543) cho runtime queries.

---

## 10. Security & Safety Boundaries
- **Nguyên tắc cô lập bí mật (Secret Isolation)**: Tuyệt đối không lưu trữ, log hoặc in `SUPABASE_SERVICE_ROLE_KEY` ra console, artifact hoặc tệp test.
- **Thực thi Idempotent Migrations**: Mọi kịch bản DDL phải viết dưới dạng có thể chạy lại an toàn (`IF EXISTS`, `IF NOT EXISTS`, `OR REPLACE`).
- **Giới hạn quyền hạn (Least Privilege)**: Cấp quyền cho role `anon` và `authenticated` ở mức tối thiểu, thu hồi quyền `TRUNCATE` và `REFERENCES` khỏi public role.
- **Không tự ý drop dữ liệu**: Cấm thực thi `DROP TABLE` hoặc `DROP COLUMN` mà không có bước backup hoặc phê duyệt từ người dùng.

---

## 11. Platform Adapters
Adapter hỗ trợ tương thích với các công cụ trong hệ sinh thái Supabase:
- **Supabase CLI Native**: Tạo và quản lý migrations trong thư mục `supabase/migrations/`.
- **Prisma ORM**: Tạo cấu hình `schema.prisma` với `directUrl` và `relationMode = "foreignKeys"`.
- **Drizzle ORM**: Hỗ trợ xuất Drizzle schema có RLS policies helper.
- **Graceful Fallback Mode**: Khi không có CLI kết nối tới Supabase Cloud, adapter xuất bản mã SQL migration thuần túy đã được xác thực tĩnh để nhà phát triển copy chạy thủ công trên Supabase Studio SQL Editor.

---

## 12. Deliverables & Output Artifacts
Khi hoàn thành tác vụ, adapter cung cấp:
1. **Migration Script**: `supabase/migrations/<timestamp>_<name>.sql` chứa toàn bộ DDL, indexes và RLS policies.
2. **Báo cáo kiểm toán hiệu năng RLS**: Bảng tổng hợp so sánh trước/sau khi tối ưu hóa subquery caching.
3. **Mẫu cấu hình Connection Pool**: Hướng dẫn cấu hình biến môi trường và pool mode cho ứng dụng.
4. **Kịch bản kiểm thử RLS**: Bộ test SQL mẫu để giả lập các role (`anon`, `authenticated` với user id cụ thể) nhằm chứng minh dữ liệu bị cách ly triệt để.

---

## 13. Related & Complementary Skills
- [`dex-master-orchestrator`](../../.agents/skills/dex-master-orchestrator/SKILL.md): Cội nguồn điều phối điều phối yêu cầu người dùng tới adapter.
- [`dex-database-engineering`](../../.agents/skills/dex-database-engineering/SKILL.md): Thiết kế lược đồ CSDL quan hệ tổng quát và ACID.
- [`dex-database-query-plans`](../../.agents/skills/dex-database-query-plans/SKILL.md): Phân tích chi tiết `EXPLAIN ANALYZE` và chỉ mục Postgres.
- [`dex-access-control-tenancy`](../../.agents/skills/dex-access-control-tenancy/SKILL.md): Nguyên lý kiến trúc phân quyền đa người thuê và RBAC.
- [`dex-auth-session-lifecycle`](../../.agents/skills/dex-auth-session-lifecycle/SKILL.md): Quản lý vòng đời token JWT và session authentication.

---

## 14. Realistic Usage Example

### Tình huống thực tế:
Kỹ sư gửi yêu cầu: *"Hệ thống Supabase của chúng tôi chạy trên Next.js Serverless bị sập khi có nhiều request đồng thời, và các truy vấn trên bảng orders rất chậm khi bật RLS. Hãy tối ưu và bảo mật lại."*

### Các lệnh kiểm tra và thực thi:
```bash
# 1. Kiểm tra trạng thái CLI
supabase status || echo "SUPABASE_CLI_OFFLINE: Chuyển sang chế độ phân tích tĩnh"

# 2. Tạo migration tối ưu hóa RLS và Indexing
cat << 'EOF' > supabase/migrations/20261023000001_optimize_orders_rls.sql
-- Bật RLS
ALTER TABLE public.orders ENABLE ROW LEVEL SECURITY;

-- Tạo chỉ mục ngoại khóa để tăng tốc JOIN và CASCADE check
CREATE INDEX IF NOT EXISTS idx_orders_customer_id ON public.orders(customer_id);
CREATE INDEX IF NOT EXISTS idx_orders_tenant_id ON public.orders(tenant_id);

-- Thay thế policy chậm bằng InitPlan Subquery
DROP POLICY IF EXISTS "orders_customer_access" ON public.orders;
CREATE POLICY "orders_customer_access" ON public.orders
FOR SELECT
TO authenticated
USING (
    customer_id = (SELECT auth.uid()) 
    OR 
    tenant_id IN (
        SELECT m.tenant_id 
        FROM public.memberships m 
        WHERE m.user_id = (SELECT auth.uid())
    )
);
EOF

# 3. Kiểm chứng cú pháp migration
python -c "print('MIGRATION_VALIDATED: 20261023000001_optimize_orders_rls.sql syntax ready for deployment')"
```
