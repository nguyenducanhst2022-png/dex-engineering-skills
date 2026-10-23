---
name: dex-postgres-rls-policy-verification
description: Verify, test, and audit PostgreSQL Row-Level Security (RLS) policies against multi-tenant isolation breaches, bypassing flaws, and role-specific permissions (SELECT, INSERT, UPDATE, DELETE). Use when auditing database security or preventing cross-tenant data leaks.
---

# dex-postgres-rls-policy-verification

## 1. Purpose & Scope
Xác minh và kiểm thử tự động các chính sách Row-Level Security (RLS) trong PostgreSQL; phát hiện sớm các lỗ hổng rò rỉ dữ liệu giữa các tenant, kiểm toán ma trận phân quyền 4 thao tác (SELECT, INSERT, UPDATE, DELETE) cho từng database role (anon, authenticated, tenant_user, tenant_admin); bảo đảm không có kẽ hở bypass RLS qua VIEW hoặc hàm SECURITY DEFINER.

## 2. When to Use
- Khi thiết kế hoặc nâng cấp lược đồ cơ sở dữ liệu đa người thuê (Multi-Tenant SaaS).
- Khi chuẩn bị phát hành migration thay đổi chính sách RLS trên các bảng chứa dữ liệu nhạy cảm.
- Khi cần chạy bộ kiểm thử tự động giả lập các vai trò người dùng khác nhau để chứng minh dữ liệu bị cô lập hoàn toàn.

## 3. When NOT to Use
- Khi ứng dụng sử dụng CSDL NoSQL (MongoDB, DynamoDB) không hỗ trợ cơ chế RLS của PostgreSQL.
- Khi hệ thống phân quyền được xử lý thuần túy tại tầng ứng dụng (Application-Level RBAC) mà không kích hoạt RLS tại tầng database.

## 4. Prerequisites & Input Context
- **Lược đồ CSDL:** Các bảng đã bật `ENABLE ROW LEVEL SECURITY` và các chính sách `CREATE POLICY` tương ứng.
- **Tài khoản kiểm thử:** Quyền tạo database roles tạm thời (`anon`, `authenticated_user_a`, `authenticated_user_b`) để chạy harness kiểm thử.

## 5. Core Concepts & Taxonomy
- **SET LOCAL ROLE:** Lệnh chuyển đổi ngữ cảnh thực thi trong một transaction mà không làm ảnh hưởng tới các kết nối khác của pooler.
- **InitPlan Caching:** Tối ưu hóa biểu thức RLS bằng `(SELECT auth.uid())` giúp PostgreSQL đánh giá 1 lần duy nhất thay vì $O(N)$ lần quét bảng.
- **WITH CHECK vs USING:** `USING` kiểm soát các hàng được phép nhìn thấy (SELECT/UPDATE/DELETE), trong khi `WITH CHECK` kiểm soát dữ liệu mới được chèn hoặc cập nhật (INSERT/UPDATE).

## 6. Step-by-Step Execution Workflow
1. Khởi tạo một transaction kiểm thử cô lập bằng `BEGIN;`.
2. Thiết lập session context giả lập vai trò người dùng: `SET LOCAL ROLE authenticated;` kèm `SET LOCAL "request.jwt.claims" = '{"sub": "uuid-user-a"}';`.
3. Thực hiện truy vấn `SELECT` trên bảng dữ liệu và khẳng định chỉ trả về dữ liệu thuộc tenant của user A.
4. Thực hiện thử nghiệm tấn công giả lập: User A cố tình `UPDATE` hoặc `DELETE` bản ghi của user B và xác nhận số hàng bị ảnh hưởng bằng 0.
5. Thực hiện thử nghiệm chèn dữ liệu chéo: User A cố tình `INSERT` bản ghi với `tenant_id` của user B và xác nhận PostgreSQL ném lỗi vi phạm policy `WITH CHECK`.
6. Hoàn tất kiểm thử bằng `ROLLBACK;` để giữ nguyên trạng thái database sạch sẽ.

## 7. Concrete Examples
### Kịch bản SQL kiểm thử RLS tự động cho hệ thống Multi-Tenant:
```sql
BEGIN;

-- 1. Thiet lap role authenticated va tenant context cua User A
SET LOCAL ROLE authenticated;
SELECT set_config('request.jwt.claims', '{"sub": "11111111-1111-1111-1111-111111111111"}', true);

-- 2. Kiem tra SELECT: User A chi thay du lieu cua minh
DO $$
DECLARE
    row_count integer;
BEGIN
    SELECT COUNT(*) INTO row_count FROM public.documents WHERE tenant_id != '11111111-1111-1111-1111-111111111111';
    IF row_count > 0 THEN
        RAISE EXCEPTION 'RLS LEAK DETECTED: User A can see % foreign documents!', row_count;
    END IF;
END $$;

-- 3. Kiem tra INSERT cheo tenant: Phai that bai do WITH CHECK
DO $$
BEGIN
    INSERT INTO public.documents (id, tenant_id, title)
    VALUES (gen_random_uuid(), '22222222-2222-2222-2222-222222222222', 'Illegal Doc');
    RAISE EXCEPTION 'RLS BYPASS: User A successfully inserted document for Tenant B!';
EXCEPTION WHEN insufficient_privilege THEN
    -- Ket qua mong doi: PostgreSQL chan thanh cong
    RAISE NOTICE 'SUCCESS: Cross-tenant insertion blocked by RLS.';
END $$;

ROLLBACK;
```

## 8. Anti-Patterns & Common Traps
- **Missing WITH CHECK Clause:** For ALL and UPDATE policies, omitted `WITH CHECK` falls back to `USING`; omission alone does not permit tenant reassignment. Inspect permissive OR and restrictive AND composition and test reassignment explicitly.
- **Unindexed Foreign Tenant ID:** Viết RLS filter dựa trên `tenant_id` nhưng quên đánh chỉ mục cho cột này, khiến mọi câu truy vấn của người dùng biến thành Full Table Scan.
- **Direct Querying as Superuser/postgres:** Chạy test kiểm thử bằng role `postgres` (mặc định bypass RLS) dẫn đến ảo giác an ninh rằng policy hoạt động tốt.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Enable RLS on tenant tables; assess FORCE ROW LEVEL SECURITY when table owners should also be subject to policies. Test application roles without superuser or BYPASSRLS privileges.
- **QG-02**: Không có bất kỳ policy nào cho phép user xem hoặc sửa đổi bản ghi của tenant khác trong kịch bản kiểm thử tự động.
- **QG-03**: SECURITY DEFINER functions use a controlled search_path containing only trusted schemas, with pg_temp last; schema-qualify sensitive objects and review CREATE/EXECUTE grants. Do not assume public is trusted.

## 10. Security & Safety Boundaries
- Tuân thủ nguyên tắc Least Privilege; cô lập hoàn toàn ranh giới dữ liệu giữa các khách hàng trên hạ tầng cơ sở dữ liệu dùng chung.

## 11. Platform Adapters
- **Runtimes**: PostgreSQL 14+, Supabase Cloud, AWS RDS Postgres, pgTAP, Python pytest-postgresql.

## 12. Deliverables & Output Artifacts
- Tệp kịch bản kiểm thử RLS tự động (`test_rls_isolation.sql`).
- Báo cáo ma trận phân quyền theo từng bảng và vai trò người dùng.
- Khuyến nghị tối ưu hóa chỉ mục và InitPlan subquery cho các policy lớn.

## 13. Related & Complementary Skills
dex-access-control-tenancy, dex-database-engineering, dex-supabase-adapter

## 14. Realistic Usage Example
```bash
# Chay bo kiem thu RLS bang psql tren moi truong staging
psql "$DATABASE_URL" -v ON_ERROR_STOP=1 -f tests/sql/test_rls_isolation.sql

# Kiem tra ma tran RLS bang script Python tu dong
python -m pytest tests/test_postgres_rls.py -v
```

Official policy semantics: https://www.postgresql.org/docs/current/sql-createpolicy.html
