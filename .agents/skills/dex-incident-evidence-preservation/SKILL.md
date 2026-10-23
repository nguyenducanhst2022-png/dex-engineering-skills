---
name: dex-incident-evidence-preservation
description: Capture, cryptographically seal, and catalog volatile operational evidence during security incidents preserving forensic integrity and legal chain of custody. Use when handling active security intrusions and critical infrastructure failures.
---

# dex-incident-evidence-preservation

## 1. Purpose & Scope
Thu thập, niêm phong mật mã (Cryptographic Sealing) và lập danh mục các bằng chứng vận hành dễ bay hơi (Volatile Operational Evidence) trong quá trình xử lý sự cố an ninh; bảo đảm tính toàn vẹn điều tra số (Forensic Integrity) và chuỗi hành trình bằng chứng (Chain of Custody) phục vụ tố tụng pháp lý.

## 2. When to Use
- Khi phát hiện máy chủ hoặc cụm container bị xâm nhập và cần thu thập dấu vết trước khi kẻ tấn công kịp xóa dấu vết.
- Khi cần đóng băng trạng thái bộ nhớ RAM, nhật ký mạng và bảng tiến trình phục vụ điều tra nguyên nhân gốc rễ (Root Cause Analysis).
- Khi cơ quan pháp luật hoặc bảo hiểm an ninh mạng yêu cầu cung cấp bằng chứng có chứng thực toàn vẹn không bị làm sai lệch.

## 3. When NOT to Use
- Khi xử lý các lỗi ứng dụng thông thường (bug nhỏ) không liên quan đến hành vi xâm nhập hoặc vi phạm bảo mật.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Máy chủ hoặc container nghi vấn bị xâm nhập, công cụ thu thập chứng cứ (LiME, Volatility, dumpit, aws-cli), kho lưu trữ bằng chứng bảo mật (WORM - Write Once Read Many).
- **Quyền hạn truy cập:** Quyền quản trị điều tra số (Forensic Investigator) trên hạ tầng bị ảnh hưởng.

## 5. Core Concepts & Taxonomy
- **Order of Volatility:** Thứ tự ưu tiên thu thập bằng chứng từ dễ bay hơi nhất đến bền vững: Thanh ghi & Bộ nhớ đệm CPU -> Bộ nhớ RAM -> Trạng thái kết nối mạng -> Hệ thống tệp trên đĩa lưu trữ -> Sao lưu đĩa.
- **Cryptographic Chain of Custody:** Bản ghi bất biến ghi nhận ai là người thu thập, tại thời điểm nào, bằng công cụ gì, kèm mã băm SHA-256 được ký số ngay tại thời điểm trích xuất.
- **WORM Storage (Write Once, Read Many):** Lưu trữ bằng chứng vào các kho lưu trữ khóa cứng (như AWS S3 Object Lock) ngăn chặn bất kỳ ai (kể cả admin) xóa hoặc sửa đổi bằng chứng trong thời hạn quy định.

## 6. Step-by-Step Execution Workflow
1. Ngay lập tức cách ly máy chủ bị xâm nhập khỏi hệ thống mạng (Network Isolation) nhưng KHÔNG tắt nguồn để giữ nguyên bộ nhớ RAM.
2. Chụp ảnh bộ nhớ RAM (Memory Dump) và ghi lại bảng kết nối mạng, bảng định tuyến và danh sách tiến trình đang chạy.
3. Tính toán mã băm SHA-256 ngay lập tức cho từng tệp dữ liệu vừa thu thập.
4. Thực hiện chụp ảnh nhanh (Snapshot) toàn bộ các ổ đĩa lưu trữ của máy ảo.
5. Đẩy toàn bộ bằng chứng và tệp mã băm vào kho lưu trữ WORM S3 Object Lock.
6. Ký số biên bản chuỗi hành trình bằng chứng (Chain of Custody Document) và bàn giao cho đội điều tra chuyên trách.

## 7. Concrete Examples
### Kịch bản thu thập bằng chứng dễ bay hơi và niêm phong mã băm trên Linux:
```bash
#!/bin/bash
# forensic-capture.sh - Volatile Evidence Preservation
set -euo pipefail

TIMESTAMP=$(date -u +"%Y%m%d_%H%M%SZ")
OUTDIR="/tmp/forensic_${TIMESTAMP}"
mkdir -p "$OUTDIR"

echo "==> [1/3] Thu thap thong tin tien trinh va ket noi mang..."
ps auxwwf > "$OUTDIR/ps_tree.txt"
netstat -tulpn > "$OUTDIR/netstat.txt"
ip route show > "$OUTDIR/routes.txt"
uptime > "$OUTDIR/uptime.txt"

echo "==> [2/3] Niem phong ma bam SHA-256 cho toan bo bang chung..."
cd "$OUTDIR"
sha256sum * > SHA256SUMS

echo "==> [3/3] Day vao kho luu tru WORM S3 Object Lock..."
tar -czf "${OUTDIR}.tar.gz" -C "/tmp" "forensic_${TIMESTAMP}"
sha256sum "${OUTDIR}.tar.gz" > "${OUTDIR}.tar.gz.sha256"

# Tai len S3 voi che do khoa Compliance Mode (khong the sua/xoa trong 365 ngay)
aws s3 cp "${OUTDIR}.tar.gz" "s3://forensic-vault/evidence/${TIMESTAMP}/" \
  --object-lock-mode COMPLIANCE \
  --object-lock-retain-until-date "$(date -d '+1 year' -u +"%Y-%m-%dT%H:%M:%SZ")"

echo "==> Bang chung da duoc niem phong an toan tuyet doi!"
```

## 8. Anti-Patterns & Common Traps
- **Rebooting or Powering Down Host:** Khởi động lại hoặc tắt máy chủ khiến toàn bộ bằng chứng quý giá trong bộ nhớ RAM bị xóa sạch.
- **Modifying Files on Live Target:** Chạy các công cụ điều tra cài đặt trực tiếp trên máy bị xâm nhập làm thay đổi dấu thời gian (timestamps) của các tệp tin.
- **Storing Evidence on Shared Drives:** Lưu trữ bằng chứng trên ổ đĩa mạng thông thường có thể bị kẻ tấn công ghi đè hoặc tiêu hủy.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: 100% bằng chứng thu thập được đều có mã băm SHA-256 được tính toán ngay tại thời điểm tạo ra.
- **QG-04**: Toàn bộ bằng chứng được lưu trữ trong kho WORM Object Lock ngăn chặn chỉnh sửa.
- **QG-09**: Biên bản chuỗi hành trình bằng chứng ghi nhận đầy đủ chữ ký số và mốc thời gian UTC.

## 10. Security & Safety Boundaries
- Đảm bảo tính pháp lý của bằng chứng số để có thể sử dụng làm tài liệu chứng cứ hợp lệ trước tòa án hoặc cơ quan chức năng.

## 11. Platform Adapters
- **Forensic Tools**: LiME, Volatility 3, Autopsy, aws-cli, S3 Object Lock, Azure Immutable Blob.

## 12. Deliverables & Output Artifacts
- Gói dữ liệu bằng chứng đã niêm phong mã băm (Tarball + SHA256).
- Bản ghi chuỗi hành trình bằng chứng (Chain of Custody Document).
- Báo cáo điều tra số sơ bộ về các dấu hiệu xâm nhập (IoCs).

## 13. Related & Complementary Skills
dex-dns-tls-certificate-monitoring, dex-privacy-safe-observability, dex-saas-risk-surface-review

## 14. Realistic Usage Example
```powershell
# Xác thực tính toàn vẹn của gói bằng chứng forensic
Get-FileHash -Algorithm SHA256 ./evidence_20261022.tar.gz

# Kiểm tra trạng thái Object Lock của file bằng chứng trên S3
aws s3api get-object-retention --bucket forensic-vault --key evidence/20261022/evidence.tar.gz
```
