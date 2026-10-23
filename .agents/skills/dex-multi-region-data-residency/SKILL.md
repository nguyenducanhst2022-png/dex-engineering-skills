---
name: dex-multi-region-data-residency
description: Architect multi-region data partitioning and replication topologies complying with strict legal data residency and sovereignty requirements (GDPR, APRA, HIPAA). Use when deploying global applications handling region-locked user data.
---

# dex-multi-region-data-residency

## 1. Purpose & Scope
Thiết kế kiến trúc phân vùng dữ liệu đa vùng (Multi-Region Data Partitioning) và cấu hình topo sao chép tuân thủ nghiêm ngặt các quy định pháp lý về chủ quyền dữ liệu (Data Residency & Data Sovereignty như GDPR, HIPAA, APRA); ngăn chặn việc dữ liệu nhạy cảm bị sao chép trái phép ra khỏi biên giới quốc gia.

## 2. When to Use
- Khi triển khai hệ thống toàn cầu phục vụ người dùng ở nhiều khu vực pháp lý có quy định khắt khe về nơi lưu trữ dữ liệu (EU, Mỹ, Singapore, Việt Nam).
- Khi cần cung cấp độ trễ đọc/ghi thấp cho người dùng ở nhiều lục địa khác nhau mà vẫn tôn trọng chủ quyền dữ liệu.
- Khi chuẩn bị hồ sơ kiểm toán bảo mật và tuân thủ pháp lý quốc tế.

## 3. When NOT to Use
- Khi ứng dụng chỉ hoạt động và phục vụ người dùng tại một quốc gia duy nhất.
- Khi dữ liệu xử lý là dữ liệu công khai, không chứa PII hoặc bí mật kinh doanh chịu ràng buộc địa lý.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Yêu cầu pháp lý theo từng vùng lãnh thổ, sơ đồ phân loại dữ liệu (Data Classification), topo mạng và hạ tầng đa đám mây (Multi-Region Cloud).
- **Quyền hạn truy cập:** Quyền cấu hình replication và phân quyền mạng trên cơ sở dữ liệu.

## 5. Core Concepts & Taxonomy
- **Geographic Partitioning (Geo-sharding):** Chia partition bảng dữ liệu dựa trên thuộc tính vị trí địa lý của người dùng (ví dụ: `region = 'eu-west-1'`).
- **Data Sovereignty Constraints:** Dữ liệu cá nhân (PII) bắt buộc lưu trữ và xử lý tại máy chủ thuộc ranh giới địa lý quy định.
- **Global Table Routing:** Hệ thống định tuyến ứng dụng tự động chuyển hướng kết nối database tới đúng cụm máy chủ khu vực dựa trên JWT token của tenant.

## 6. Step-by-Step Execution Workflow
1. Phân loại toàn bộ bảng dữ liệu thành 3 nhóm: Global Shared Data (không PII), Region-Pinned PII Data, và Ephemeral Logs.
2. Thiết lập cấu hình cơ sở dữ liệu hỗ trợ geo-partitioning (như CockroachDB, Spanner, hoặc PostgreSQL Sharding với Citus).
3. Gắn partition key theo khu vực (`jurisdiction_code`) cho toàn bộ bảng chứa dữ liệu nhạy cảm.
4. Cấu hình quy tắc sao chép (Replication Policy) ngăn chặn đồng bộ bảng Region-Pinned sang các vùng địa lý khác.
5. Xây dựng integration test tự động xác nhận câu truy vấn không bao giờ ghi dữ liệu EU sang cụm database đặt tại US.

## 7. Concrete Examples
### Ví dụ định nghĩa bảng Geo-Partitioned trong CockroachDB:
```sql
-- Định nghĩa bảng người dùng có ràng buộc vị trí địa lý dữ liệu
CREATE TABLE customer_profiles (
    customer_id UUID DEFAULT gen_random_uuid(),
    residence_region VARCHAR(10) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    encrypted_national_id BYTEA,
    created_at TIMESTAMPTZ DEFAULT clock_timestamp(),
    PRIMARY KEY (residence_region, customer_id)
) PARTITION BY LIST (residence_region) (
    PARTITION eu_region VALUES IN ('EU', 'DE', 'FR', 'NL'),
    PARTITION us_region VALUES IN ('US', 'CA'),
    PARTITION apac_region VALUES IN ('VN', 'SG', 'JP')
);

-- Cấu hình lưu trữ vật lý cho từng partition theo vùng dữ liệu
ALTER PARTITION eu_region OF TABLE customer_profiles 
    CONFIGURE ZONE USING constraints = '[+region=europe-west1]';

ALTER PARTITION us_region OF TABLE customer_profiles 
    CONFIGURE ZONE USING constraints = '[+region=us-central1]';

ALTER PARTITION apac_region OF TABLE customer_profiles 
    CONFIGURE ZONE USING constraints = '[+region=asia-southeast1]';
```

## 8. Anti-Patterns & Common Traps
- **Unbounded Global Replication:** Đồng bộ toàn bộ database ra toàn cầu mà không lọc các bảng chứa dữ liệu cá nhân.
- **Centralized Foreign Logging:** Bắn log chứa thông tin PII của người dùng châu Âu về cụm lưu trữ log tập trung đặt tại Mỹ.
- **Client-Side Region Spoofing:** Cho phép client tự ý gửi header khu vực mà không xác thực lại từ chứng thực người dùng.

## 9. Quality Gates & Acceptance Criteria
- **QG-06**: Không có dữ liệu PII nào được lưu trữ bên ngoài vùng địa lý được chỉ định trong cấu hình.
- **QG-11**: Các kết nối cross-region chỉ áp dụng cho dữ liệu đã được mã hóa và không chứa thông tin định danh cá nhân.
- **QG-14**: Đáp ứng các yêu cầu kiểm toán của GDPR Article 44-50 về chuyển giao dữ liệu quốc tế.

## 10. Security & Safety Boundaries
- Bắt buộc mã hóa dữ liệu cả khi lưu trữ (at rest) và khi truyền tải (in transit) bằng giao thức TLS 1.3 với cipher suites mạnh.
- Khóa mã hóa (KMS keys) cho từng vùng phải được quản lý tại hạ tầng của chính vùng đó (Regional KMS).

## 11. Platform Adapters
- **Database**: CockroachDB, Google Cloud Spanner, AWS Aurora Global Database with Write Forwarding.
- **Cloud**: AWS, GCP, Azure Multi-Region VPC Peering.

## 12. Deliverables & Output Artifacts
- Tệp DDL cấu hình phân vùng địa lý cơ sở dữ liệu.
- Ma trận phân loại dữ liệu và vị trí lưu trữ (Data Residency Matrix).
- Bộ kiểm thử tự động kiểm tra vi phạm lưu trữ dữ liệu ngoài vùng.

## 13. Related & Complementary Skills
dex-compliance-control-mapping, dex-privacy-impact-assessment, dex-database-engineering

## 14. Realistic Usage Example
```powershell
# Chạy bài kiểm thử xác minh ranh giới lưu trữ dữ liệu địa lý
pytest tests/compliance/test_data_residency_boundaries.py -v
```
