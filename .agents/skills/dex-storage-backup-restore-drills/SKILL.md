---
name: dex-storage-backup-restore-drills
description: Automate, execute, and verify end-to-end storage and database backup restoration drills. Audit cryptographic checksums, snapshot integrity, and measure Recovery Time Objectives (RTO).
---

# dex-storage-backup-restore-drills

## 1. Purpose & Scope
Thiết kế, tự động hóa và kiểm chứng toàn diện quy trình phục hồi sao lưu dữ liệu (Storage & Database Backup Restoration Drills); kiểm tra tính hợp lệ của các bản sao lưu (AWS S3 Versioning, PostgreSQL WAL-G/pg_dump, EBS Snapshots); thực hiện phục hồi thực tế vào một môi trường cách ly (Isolated Sandbox); đối soát mã băm mật mã học (Cryptographic SHA-256 Checksums), kiểm tra tính nhất quán giao dịch và chứng minh khả năng phục hồi dữ liệu trong thời gian cam kết RTO/RPO mà không làm ảnh hưởng tới hệ thống chính.

## 2. When to Use
- Khi tiến hành diễn tập kiểm toán tuân thủ định kỳ hàng quý hoặc hàng năm theo tiêu chuẩn SOC 2, HIPAA, hoặc ISO 27001.
- Khi thiết lập quy trình kiểm tra tự động xem các bản sao lưu hàng đêm có thực sự giải nén và nạp lại được vào database hay không.
- Khi thay đổi phiên bản cơ sở dữ liệu lớn (Major Version Upgrade) và cần chắc chắn bản backup tương thích với engine mới.

## 3. When NOT to Use
- Khi sao chép tệp tạm thời giữa các thư mục cục bộ của máy tính phát triển.
- Khi kiểm thử logic nghiệp vụ thông thường không liên quan tới sự cố mất mát dữ liệu hoặc thảm họa hạ tầng.

## 4. Prerequisites & Input Context
- **Hạ tầng lưu trữ:** Kho lưu trữ sao lưu có bật bảo vệ chống ghi đè/xóa (S3 Object Lock / WORM storage).
- **Môi trường diễn tập:** Cụm tài nguyên Sandbox biệt lập với hạ tầng production.

## 5. Core Concepts & Taxonomy
- **Backup vs Restore Verification:** Bản sao lưu chỉ có giá trị khi nó đã được chứng minh là có thể phục hồi thành công (An unverified backup is not a backup).
- **WORM (Write Once, Read Many):** Chính sách khóa dữ liệu bất biến ngăn chặn mã độc tống tiền (Ransomware) hoặc kẻ tấn công có quyền quản trị xóa bỏ các bản sao lưu.
- **Point-in-Time Recovery (PITR):** Khả năng phục hồi trạng thái cơ sở dữ liệu về đúng một giây cụ thể trong quá khứ bằng cách kết hợp bản Base Backup với chuỗi nhật ký Write-Ahead Logs (WAL).

## 6. Step-by-Step Execution Workflow
1. Lựa chọn ngẫu nhiên một bản sao lưu gần nhất từ kho lưu trữ bất biến (S3 WORM Bucket).
2. Xác thực tính toàn vẹn của tệp nhị phân thông qua chữ ký số hoặc mã băm SHA-256.
3. Khởi tạo một cụm cơ sở dữ liệu hoặc máy chủ lưu trữ mới trong mạng VPC Sandbox cách ly.
4. Thực hiện tiến trình nạp phục hồi dữ liệu (Restore) và ghi nhận thời gian hoàn thành (Actual RTO).
5. Chạy bộ kịch bản kiểm tra tính toàn vẹn dữ liệu tự động (Data Consistency Checks): đếm số hàng các bảng quan trọng, kiểm tra ràng buộc khóa ngoại.
6. Hủy bỏ môi trường Sandbox và xuất báo cáo kiểm toán diễn tập phục hồi có chữ ký số xác thực.

## 7. Concrete Examples
### Kich ban tu dong phuc hoi PostgreSQL tu S3 vao Sandbox va kiem tra toan ven:
```bash
#!/usr/bin/env bash
set -euo pipefail

BACKUP_BUCKET="s3://corp-backups-immutable-worm/postgres"
SANDBOX_CONTAINER="postgres-restore-sandbox"
LATEST_BACKUP=$(aws s3 ls "${BACKUP_BUCKET}/" | sort | tail -n 1 | awk '{print $4}')

echo "=== STARTING RESTORE DRILL FOR: ${LATEST_BACKUP} ==="
START_TIME=$(date +%s)

# 1. Tai ban sao luu kem checksum
aws s3 cp "${BACKUP_BUCKET}/${LATEST_BACKUP}" ./latest_backup.dump
aws s3 cp "${BACKUP_BUCKET}/${LATEST_BACKUP}.sha256" ./latest_backup.sha256

# 2. Xac thuc ma bam toan ven
sha256sum -c latest_backup.sha256

# 3. Khoi tao container Postgres moi tinh trong sandbox
docker run -d --name "${SANDBOX_CONTAINER}" -e POSTGRES_PASSWORD=restore_pass -p 5433:5432 postgres:16-alpine
sleep 5

# 4. Thuc hien restore
pg_restore -h localhost -p 5433 -U postgres -d postgres -v latest_backup.dump

END_TIME=$(date +%s)
RTO_SECONDS=$((END_TIME - START_TIME))
echo "Restore completed successfully in ${RTO_SECONDS} seconds."

# 5. Kiem tra toan ven du lieu (Data Integrity Check)
COUNT_USERS=$(psql -h localhost -p 5433 -U postgres -t -c "SELECT COUNT(*) FROM public.users;")
echo "Integrity Verification: public.users count = ${COUNT_USERS}"

# 6. Don dep sandbox
docker rm -f "${SANDBOX_CONTAINER}"
rm -f latest_backup.dump latest_backup.sha256
echo "Restore drill PASSED and sandbox cleaned."
```

## 8. Anti-Patterns & Common Traps
- **Trusting Successful Backup Logs Blindly:** Tin tưởng tuyệt đối vào thông báo "Backup Finished with Code 0" mà không bao giờ thực hiện diễn tập khôi phục thực tế, đến khi thảm họa xảy ra mới phát hiện tệp backup bị rỗng hoặc lỗi mã hóa.
- **Restoring Directly into Production VPC:** Chạy diễn tập phục hồi trong cùng mạng VPC của môi trường production làm phát sinh nguy cơ xung đột IP hoặc ghi đè nhầm vào CSDL thật.
- **Ignoring Encryption Key Availability:** Sao lưu dữ liệu có mã hóa nhưng lưu khóa giải mã chung với máy chủ chính; khi máy chủ chính gặp nạn, không thể giải mã được bản sao lưu.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Tệp sao lưu vượt qua kiểm tra mã băm SHA-256 khớp 100% với giá trị ghi nhận lúc tạo bản sao lưu.
- **QG-02**: Quá trình phục hồi vào môi trường Sandbox hoàn tất thành công với mã thoát 0 mà không có lỗi cú pháp.
- **QG-03**: Số lượng bản ghi và tính toàn vẹn của các bảng dữ liệu cốt lõi khớp chính xác với trạng thái tại thời điểm sao lưu.

## 10. Security & Safety Boundaries
- Kho lưu trữ bản sao lưu phải được cấu hình quyền bất biến (Object Lock / WORM) ngăn chặn việc xóa bỏ vô tình hoặc cố ý từ bất kỳ ai.

## 11. Platform Adapters
- **Runtimes**: AWS S3 Object Lock, PostgreSQL pg_restore / WAL-G, Velero (Kubernetes), Docker Sandbox.

## 12. Deliverables & Output Artifacts
- Kịch bản diễn tập phục hồi sao lưu tự động (`automated_restore_drill.sh`).
- Báo cáo kiểm toán kết quả diễn tập phục hồi hàng quý (`restore_drill_audit.pdf`).

## 13. Related & Complementary Skills
dex-cloud-database-failover-drills, dex-api-circuit-breaker-verification, dex-operational-dependency-mapping

## 14. Realistic Usage Example
```bash
# Xac thuc ma bam cua tep backup truoc khi dien tap
sha256sum -c backup_2026_10_23.dump.sha256
```
