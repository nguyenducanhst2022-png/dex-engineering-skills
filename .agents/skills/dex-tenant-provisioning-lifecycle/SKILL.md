---
name: dex-tenant-provisioning-lifecycle
description: Orchestrate end-to-end multi-tenant provisioning, migration, suspension, and offboarding lifecycles with strict resource isolation. Use when building B2B SaaS platforms with automated self-service onboarding or enterprise tenant tiering.
---

# dex-tenant-provisioning-lifecycle

## 1. Purpose & Scope
Điều phối toàn diện vòng đời của tenant trong kiến trúc đa người thuê (Multi-Tenant SaaS); tự động hóa các giai đoạn khởi tạo (provisioning), nâng cấp schema, tạm khóa (suspension), di chuyển dữ liệu (migration) và xóa sạch dữ liệu (offboarding/purging) bảo đảm cách ly triệt để tài nguyên.

## 2. When to Use
- Khi xây dựng nền tảng B2B SaaS cho phép khách hàng doanh nghiệp tự đăng ký và khởi tạo workspace tự động.
- Khi cần nâng cấp hoặc chuyển đổi mô hình tenant giữa Shared Database (Row-Level Security) và Dedicated Database (Database-per-tenant).
- Khi thực hiện quy trình hủy hợp đồng và xóa toàn bộ dữ liệu khách hàng theo quyền được lãng quên (Right to be Forgotten).

## 3. When NOT to Use
- Khi ứng dụng chỉ phục vụ một tổ chức duy nhất (Single-tenant on-premise).
- Khi quản trị người dùng thông thường trong một ứng dụng B2C không có khái niệm tổ chức/tenant.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Mô hình cách ly tenant (Schema-per-tenant, DB-per-tenant, hoặc Table-RLS), kịch bản migration database, hệ thống thông báo trạng thái.
- **Quyền hạn truy cập:** Quyền tạo database/schema mới và gán quyền truy cập người dùng trong cơ sở dữ liệu.

## 5. Core Concepts & Taxonomy
- **Tenant Lifecycle State Machine:** Các trạng thái hợp lệ gồm: `PROVISIONING` -> `ACTIVE` -> `SUSPENDED` -> `ARCHIVED` -> `PURGED`.
- **Automated Provisioning Hook:** Chuỗi tác vụ tự động: tạo schema, nạp seed data mặc định, cấp quyền IAM, cấu hình DNS subdomain và tạo tài khoản quản trị.
- **Cryptographic Shredding:** Hủy khóa mã hóa riêng của tenant khi xóa để bảo đảm dữ liệu trên bản backup cũ cũng không thể bị giải mã.

## 6. Step-by-Step Execution Workflow
1. Nhận yêu cầu khởi tạo tenant mới từ hệ thống thanh toán hoặc onboarding flow kèm gói dịch vụ (tier).
2. Kích hoạt workflow khởi tạo: tạo schema database riêng hoặc gán `tenant_id` với Row-Level Security tương ứng.
3. Áp dụng toàn bộ database migrations mới nhất vào schema của tenant mới.
4. Nạp dữ liệu cấu hình ban đầu (seed roles, permissions, default settings) và phát sinh credentials quản trị.
5. Kiểm tra tính sẵn sàng bằng lệnh smoke test truy vấn schema tenant mới khởi tạo.
6. Chuyển trạng thái tenant sang `ACTIVE` và gửi thông báo sẵn sàng sử dụng cho khách hàng.

## 7. Concrete Examples
### Ví dụ workflow điều phối vòng đời tenant bằng TypeScript:
```typescript
export enum TenantStatus {
  PROVISIONING = 'PROVISIONING',
  ACTIVE = 'ACTIVE',
  SUSPENDED = 'SUSPENDED',
  PURGED = 'PURGED'
}

export class TenantLifecycleManager {
  async provisionTenant(tenantId: string, companyName: string): Promise<void> {
    console.log(`Starting automated provisioning for tenant: ${tenantId}`);
    try {
      // 1. Tạo database schema riêng biệt
      await db.raw(`CREATE SCHEMA IF NOT EXISTS tenant_${tenantId}`);
      
      // 2. Chạy migration schema
      await runMigrationsForSchema(`tenant_${tenantId}`);
      
      // 3. Khởi tạo tài khoản quản trị mặc định
      await seedTenantAdmin(`tenant_${tenantId}`);
      
      // 4. Cập nhật trạng thái
      await updateTenantRecord(tenantId, { status: TenantStatus.ACTIVE, provisionedAt: new Date() });
      console.log(`Tenant ${tenantId} successfully provisioned.`);
    } catch (error) {
      console.error(`Provisioning failed for ${tenantId}. Rolling back...`, error);
      await this.rollbackProvisioning(tenantId);
      throw error;
    }
  }

  async purgeTenant(tenantId: string): Promise<void> {
    // Thu hồi quyền truy cập ngay lập tức
    await updateTenantRecord(tenantId, { status: TenantStatus.PURGED });
    // Xóa sạch schema vật lý
    await db.raw(`DROP SCHEMA IF EXISTS tenant_${tenantId} CASCADE`);
  }
}
```

## 8. Anti-Patterns & Common Traps
- **Manual Tenant Setup:** Kỹ sư phải vào terminal chạy tay các lệnh SQL để tạo schema cho mỗi khách hàng mới.
- **Incomplete Offboarding:** Khách hàng hủy hợp đồng nhưng dữ liệu trong cache, S3 bucket và bảng phụ trợ vẫn bị bỏ quên.
- **Shared Encryption Key:** Dùng chung một encryption key cho tất cả tenants khiến không thể áp dụng cryptographic shredding khi hủy dịch vụ.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Bắt buộc có cơ chế rollback tự động hoàn toàn nếu quá trình khởi tạo thất bại ở bất kỳ bước nào.
- **QG-06**: Xác nhận tenant mới không thể truy cập bất kỳ dữ liệu nào thuộc về tenant khác.
- **QG-14**: Quá trình xóa tenant loại bỏ 100% dữ liệu PII đáp ứng tiêu chuẩn tuân thủ GDPR.

## 10. Security & Safety Boundaries
- Cô lập kết nối database qua connection pool riêng biệt hoặc gán session variable `app.current_tenant_id` trước mỗi truy vấn.
- Kiểm toán mọi hành động quản trị liên quan tới tenant trong audit trail không thể chỉnh sửa.

## 11. Platform Adapters
- **Database**: PostgreSQL Schemas, AWS Aurora Multi-Tenant, CockroachDB.
- **Identity**: Auth0 Organizations, AWS Cognito User Pools, Keycloak Realms.

## 12. Deliverables & Output Artifacts
- Mã nguồn Tenant Lifecycle Orchestration Engine.
- Kịch bản migration tự động cho multi-tenant.
- Bộ kiểm thử tự động kiểm tra rò rỉ dữ liệu chéo giữa các tenants.

## 13. Related & Complementary Skills
dex-access-control-tenancy, dex-database-engineering, dex-compliance-control-mapping

## 14. Realistic Usage Example
```powershell
# Chạy kiểm thử tự động quy trình khởi tạo và hủy tenant
pytest tests/tenancy/test_tenant_lifecycle.py -v
```
