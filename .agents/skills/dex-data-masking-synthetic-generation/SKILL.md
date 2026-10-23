---
name: dex-data-masking-synthetic-generation
description: Architect realistic data masking, pseudonymization, differential privacy, and synthetic data generation pipelines for staging environments. Use when safeguarding PII while enabling high-fidelity testing.
---

# dex-data-masking-synthetic-generation

## 1. Purpose & Scope
Thiết kế và triển khai quy trình che mờ dữ liệu (Data Masking), giả danh hóa (Pseudonymization), quyền riêng tư vi sai (Differential Privacy) và sinh dữ liệu tổng hợp (Synthetic Data) chân thực cho môi trường staging; bảo vệ thông tin PII trong khi vẫn đảm bảo độ tin cậy cao cho việc kiểm thử phần mềm.

## 2. When to Use
- Khi cần trích xuất dữ liệu từ môi trường production về môi trường staging/dev để tái hiện lỗi nhưng bị cấm bởi quy định bảo mật dữ liệu.
- Khi kiểm thử tải hoặc kiểm thử hệ thống đòi hỏi hàng triệu bản ghi có phân phối thống kê chân thực.
- Khi chia sẻ dữ liệu với đối tác nghiên cứu bên ngoài mà không được làm lộ thông tin khách hàng.

## 3. When NOT to Use
- Khi làm việc trên môi trường sản xuất thực tế phục vụ các giao dịch tiền tệ đòi hỏi thông tin khách hàng nguyên bản.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Lược đồ cơ sở dữ liệu, từ điển phân loại dữ liệu nhạy cảm, công cụ sinh dữ liệu (Faker, SDV, Presidio).
- **Quyền hạn truy cập:** Quyền đọc dữ liệu nguồn đã qua phân quyền kiểm toán và quyền ghi vào database staging.

## 5. Core Concepts & Taxonomy
- **Consistent Pseudonymization:** Mã hóa giả danh có tính tất định (Deterministic Masking) để cùng một mã khách hàng vẫn duy trì được các liên kết khóa ngoại (Foreign Keys) giữa các bảng.
- **Differential Privacy:** Thêm nhiễu toán học có kiểm soát vào dữ liệu thống kê để không một ai có thể suy đoán ngược lại sự hiện diện của một cá nhân cụ thể.
- **Synthetic Distribution Preservation:** Dữ liệu tổng hợp duy trì chính xác tỷ lệ phân phối, giá trị ngoại lai và tương quan giữa các cột giống như dữ liệu thật.

## 6. Step-by-Step Execution Workflow
1. Quét lược đồ dữ liệu để tự động nhận diện các cột chứa thông tin PII (Họ tên, Email, Số điện thoại, Số CCCD, Địa chỉ).
2. Áp dụng quy tắc biến đổi phù hợp cho từng loại trường: Che mờ một phần (Masking), Băm có muối (Salted Hash), hoặc Thay thế bằng dữ liệu giả hợp lệ (Faker).
3. Đảm bảo tính toàn vẹn tham chiếu (Referential Integrity) giữa các khóa ngoại trên toàn bộ các bảng liên quan.
4. Sử dụng mô hình tổng hợp thống kê (Copula hoặc GANs) để sinh các bảng dữ liệu số duy trì đúng phân phối xác suất.
5. Kiểm tra rà soát tập dữ liệu đầu ra để bảo đảm không còn bất kỳ dấu vết thông tin thật nào bị rò rỉ.
6. Đóng gói pipeline nạp dữ liệu sạch vào quy trình tự động làm mới môi trường Staging hàng tuần.

## 7. Concrete Examples
### Che mờ dữ liệu PII duy trì khóa ngoại nhất quán bằng Python:
```python
import hashlib
from faker import Faker

fake = Faker(['vi_VN'])
SALT = "c98fbc923a104e76a"

def mask_user_record(raw_user: dict) -> dict:
    # Băm tất định ID để bảo toàn khóa ngoại giữa các bảng
    user_hash = hashlib.sha256((str(raw_user["user_id"]) + SALT).encode()).hexdigest()[:12]
    masked_id = f"usr_{user_hash}"
    
    # Sinh dữ liệu giả lập tiếng Việt hợp lệ thay thế PII
    return {
        "user_id": masked_id,
        "full_name": fake.name(),
        "email": f"{masked_id}@example-staging.internal",
        "phone_number": fake.phone_number(),
        "created_at": raw_user["created_at"] # Giữ nguyên thuộc tính thời gian
    }
```

## 8. Anti-Patterns & Common Traps
- **Random Non-Deterministic Masking of Foreign Keys:** Che mờ ngẫu nhiên các khóa ID khiến toàn bộ các liên kết khóa ngoại (JOINs) giữa các bảng bị gãy đổ.
- **Reversible Weak Obfuscation:** Dùng phép mã hóa yếu (như Base64 hoặc phép dịch chuyển ký tự Caesar) có thể bị giải mã ngược lại dễ dàng.
- **Leaking PII in Unstructured Notes:** Che mờ các cột bảng nhưng bỏ quên các trường văn bản tự do (Notes/Logs) chứa thông tin nhạy cảm của khách hàng.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: 0% thông tin định danh PII thực tế xuất hiện trong cơ sở dữ liệu Staging.
- **QG-04**: 100% các ràng buộc khóa ngoại (Foreign Key Constraints) vẫn hợp lệ sau khi che mờ.
- **QG-06**: Phân phối thống kê của các trường số liệu tổng hợp đạt độ tương đồng Cosine >= 0.95 so với dữ liệu gốc.

## 10. Security & Safety Boundaries
- Tiêu hủy muối băm (Salt) hoặc lưu trữ trong Vault bảo mật để ngăn chặn các cuộc tấn công tra cứu ngược Rainbow Table.

## 11. Platform Adapters
- **Tools**: Microsoft Presidio, Faker, SDV (Synthetic Data Vault), PostgreSQL Anonymizer, dbt-osmosis.

## 12. Deliverables & Output Artifacts
- Kịch bản che mờ dữ liệu tự động cho database.
- Bộ quy tắc nhận diện PII và định nghĩa trường giả lập.
- Báo cáo kiểm toán xác nhận môi trường Staging sạch thông tin nhạy cảm.

## 13. Related & Complementary Skills
dex-metadata-catalog-lineage, dex-training-data-leakage-audit, dex-online-offline-feature-parity

## 14. Realistic Usage Example
```powershell
# Chạy pipeline che mờ dữ liệu từ dump production sang staging
python scripts/data/mask_database.py --source prod_dump.sql --target staging.sql

# Quét kiểm tra dữ liệu PII còn sót lại bằng Microsoft Presidio
python scripts/data/scan_pii_leakage.py --db-url "postgresql://staging-db/app"
```
