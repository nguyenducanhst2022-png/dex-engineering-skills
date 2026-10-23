---
name: dex-build-cache-integrity
description: Safeguard, audit, and cryptographically verify local and remote build artifact caches against cache poisoning, stale dependency injection, and non-hermetic invalidation leaks. Use when operating enterprise-scale shared build caches.
---

# dex-build-cache-integrity

## 1. Purpose & Scope
Bảo vệ, kiểm toán và xác minh mật mã tính toàn vẹn của bộ nhớ đệm bản dựng (Build Cache Integrity); ngăn ngừa các cuộc tấn công đầu độc cache (Cache Poisoning), tiêm nhiễm phụ thuộc lỗi thời và rò rỉ vô hiệu hóa không khép kín trong các hệ thống cache dùng chung.

## 2. When to Use
- Khi nhiều kỹ sư và máy chủ CI cùng đọc/ghi vào một bộ nhớ đệm bản dựng từ xa (Shared Remote Cache).
- Khi phát hiện một artifact bị lỗi hoặc chứa mã độc vô tình được lưu vào cache và lây lan sang máy của các kỹ sư khác.
- Khi hệ thống không tự động vô hiệu hóa cache (invalidation) dù mã nguồn thư viện liên quan đã thay đổi.

## 3. When NOT to Use
- Khi chỉ sử dụng bộ nhớ đệm cục bộ cá nhân trên một máy đơn lẻ không chia sẻ với bất kỳ ai.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Máy chủ lưu trữ remote cache (S3, MinIO, GCP Storage), khóa bí mật ký cache (HMAC secret), cấu hình build tool.
- **Quyền hạn truy cập:** Quyền quản trị máy chủ cache và cấu hình phân quyền truy cập read/write.

## 5. Core Concepts & Taxonomy
- **Cache Poisoning:** Kẻ tấn công hoặc một máy bị nhiễm gửi một artifact độc hại ứng với một mã băm đầu vào hợp lệ vào cache chung, khiến toàn bộ hệ thống tải về mã độc đó.
- **Cryptographic Cache Signing:** Mọi artifact đưa vào remote cache phải được ký bằng khóa bí mật chỉ có máy chủ CI tin cậy nắm giữ; máy trạm của lập trình viên chỉ có quyền Đọc (Read-Only).
- **Input Key Determinism:** Đảm bảo mã băm của cache key bao quát toàn bộ các yếu tố môi trường (compiler flags, OS architecture, dependencies hashes).

## 6. Step-by-Step Execution Workflow
1. Thiết lập phân quyền truy cập cache nghiêm ngặt: Chỉ các runner CI chính thức mới có quyền Ghi (Write) vào remote cache; máy cá nhân chỉ có quyền Đọc (Read-Only).
2. Cấu hình cơ chế ký số mã băm (HMAC-SHA256) cho từng artifact được đưa lên cache.
3. Quét định kỳ kho lưu trữ cache để phát hiện và tiêu hủy các artifact bất thường hoặc quá hạn.
4. Kiểm tra độ nhạy của cache key: thay đổi một cờ compiler và xác minh rằng cache key bị thay đổi tương ứng.
5. Xây dựng nút khẩn cấp (Emergency Flush Button) cho phép xóa sạch toàn bộ remote cache trong vòng 30 giây khi phát hiện sự cố.
6. Lập báo cáo kiểm toán tính toàn vẹn và tỷ lệ trúng/trượt của hệ thống cache.

## 7. Concrete Examples
### Xác minh chữ ký số của artifact trước khi giải nén cache trong Python:
```python
import hmac
import hashlib

def verify_and_extract_cache(artifact_bytes: bytes, received_signature: str, secret_key: bytes, output_path: str):
    # Tinh toan chu ky HMAC cua du lieu artifact
    expected_signature = hmac.new(secret_key, artifact_bytes, hashlib.sha256).hexdigest()
    
    # So sanh chu ky an toan theo thoi gian co dinh (Timing-Safe)
    if not hmac.compare_digest(expected_signature, received_signature):
        raise SecurityError("Canh bao an ninh: Chu ky cache khong hop le! Nghi van dau doc cache!")
        
    with open(output_path, "wb") as f:
        f.write(artifact_bytes)
    print(f"Xac thuc toan ven thanh cong: {output_path}")
```

## 8. Anti-Patterns & Common Traps
- **Global Read-Write Cache Tokens:** Chia sẻ một token có quyền Ghi vào remote cache cho toàn bộ máy lập trình viên cá nhân.
- **Excluding Compiler Flags from Cache Key:** Chỉ băm nội dung file nguồn mà bỏ qua cờ biên dịch (như `-O3` vs `-O0`) khiến lấy nhầm bản build debug cho production.
- **Never Evicting Stale Cache:** Để cache tích tụ qua nhiều năm tiêu tốn hàng terabyte dung lượng mà không có chính sách hết hạn (TTL).

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Máy trạm cá nhân không có quyền ghi đè hoặc đưa artifact mới vào remote cache sản xuất.
- **QG-04**: 100% artifact tải về từ remote cache đều vượt qua kiểm tra tính toàn vẹn chữ ký HMAC.
- **QG-09**: Khả năng dọn sạch toàn bộ cache bị ô nhiễm (Cache Invalidation) thực hiện thành công trong dưới 60 giây.

## 10. Security & Safety Boundaries
- Cách ly máy chủ cache trong mạng nội bộ và yêu cầu xác thực TLS có chứng chỉ tương hỗ (mTLS) khi truyền tải artifact.

## 11. Platform Adapters
- **Storage**: AWS S3, MinIO, GCP Cloud Storage, Azure Blob.
- **Build Caches**: Bazel Remote Cache, Turborepo Remote Cache, Gradle Enterprise, sccache.

## 12. Deliverables & Output Artifacts
- Cấu hình phân quyền truy cập Remote Cache (Read-Only vs Read-Write).
- Script ký số và xác minh chữ ký HMAC cho artifact.
- Quy trình xử lý khẩn cấp khi nghi ngờ cache bị đầu độc.

## 13. Related & Complementary Skills
dex-polyglot-build-orchestration, dex-toolchain-reproducibility-audit, dex-binary-provenance-matching

## 14. Realistic Usage Example
```powershell
# Kiểm tra kết nối và tính toàn vẹn của sccache (Rust / C++ compiler cache)
sccache --show-stats

# Xóa sạch cache cục bộ và kiểm tra lại trạng thái
sccache --zero-stats
```
