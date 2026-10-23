---
name: dex-dns-tls-certificate-monitoring
description: Automate proactive monitoring, validation, and alerting for DNS record integrity, DNSSEC validation, TLS certificate expiration, and Certificate Transparency (CT) log entries. Use when eliminating public service outages and subdomain takeovers.
---

# dex-dns-tls-certificate-monitoring

## 1. Purpose & Scope
Tự động hóa giám sát chủ động, xác thực và cảnh báo tính toàn vẹn của bản ghi DNS, trạng thái DNSSEC, thời hạn chứng chỉ số TLS/SSL và nhật ký minh bạch chứng chỉ (Certificate Transparency Logs); ngăn ngừa sự cố sập dịch vụ do hết hạn chứng chỉ và rủi ro chiếm đoạt tên miền phụ (Subdomain Takeover).

## 2. When to Use
- Khi sự cố sập website nghiêm trọng xảy ra do chứng chỉ SSL/TLS bị hết hạn vào lúc nửa đêm mà không ai hay biết.
- Khi hệ thống sở hữu hàng trăm tên miền phụ (subdomains) trỏ vào các dịch vụ đám mây cũ có nguy cơ bị chiếm quyền sở hữu.
- Khi cần phát hiện kịp thời các chứng chỉ giả mạo được cấp phát trái phép cho tên miền của tổ chức.

## 3. When NOT to Use
- Khi ứng dụng chỉ hoạt động trong môi trường phát triển cục bộ (`localhost`) không có tên miền công khai.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Danh sách tên miền công khai của tổ chức, thông tin nhà cung cấp DNS, webhook nhận cảnh báo (Slack, PagerDuty).
- **Quyền hạn truy cập:** Quyền truy vấn DNS công cộng và theo dõi CT logs.

## 5. Core Concepts & Taxonomy
- **Certificate Transparency (CT) Logs:** Cơ sở dữ liệu bất biến công khai ghi lại mọi chứng chỉ TLS được các Certificate Authority (CA) phát hành trên toàn cầu; cho phép chủ sở hữu phát hiện ngay lập tức chứng chỉ cấp sai.
- **Subdomain Takeover:** Lỗ hổng xảy ra khi bản ghi DNS (CNAME) trỏ về một dịch vụ đám mây (S3 bucket, GitHub Pages) đã bị xóa, cho phép kẻ tấn công tạo tài nguyên trùng tên để chiếm quyền tên miền.
- **Expiration Runway:** Cảnh báo sớm theo nhiều cấp độ: 30 ngày (Thông báo), 14 ngày (Cảnh báo), 7 ngày (Khẩn cấp).

## 6. Step-by-Step Execution Workflow
1. Khởi tạo danh mục toàn bộ tên miền chính và tên miền phụ đang hoạt động của tổ chức.
2. Thiết lập tiến trình quét định kỳ kiểm tra thời hạn chứng chỉ TLS, thuật toán mã hóa và chuỗi xác thực chứng chỉ.
3. Kiểm tra tính hợp lệ của bản ghi DNSSEC để bảo vệ chống giả mạo DNS Cache Poisoning.
4. Quét phát hiện các bản ghi CNAME mồ côi (Dangling DNS records) để phòng chống Subdomain Takeover.
5. Đăng ký theo dõi nhật ký Certificate Transparency qua các dịch vụ như Certstream để nhận cảnh báo theo thời gian thực.
6. Tích hợp cảnh báo đa kênh tới đội trực vận hành (PagerDuty / Slack) khi thời hạn chứng chỉ còn dưới 15 ngày.

## 7. Concrete Examples
### Kịch bản kiểm tra thời hạn chứng chỉ TLS và cảnh báo sớm trong Python:
```python
import ssl
import socket
from datetime import datetime, timezone

def check_tls_expiration(hostname: str, port: int = 443, warning_days: int = 15):
    context = ssl.create_default_context()
    with socket.create_connection((hostname, port), timeout=5) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()
            
    # Trich xuat ngay het han tu chung chi x509
    expire_str = cert['notAfter']
    expire_date = datetime.strptime(expire_str, "%b %d %H:%M:%S %Y %Z").replace(tzinfo=timezone.utc)
    remaining_days = (expire_date - datetime.now(timezone.utc)).days
    
    print(f"Domain: {hostname} | Chung chi het han: {expire_date} (Con {remaining_days} ngay)")
    
    if remaining_days <= warning_days:
        raise AlertError(f"KHAN CAP: Chung chi TLS cho {hostname} chi con {remaining_days} ngay! Can gia han ngay lap tuc!")
    return remaining_days
```

## 8. Anti-Patterns & Common Traps
- **Single Reminder Calendar Event:** Chỉ đặt một lịch nhắc nhở cá nhân trên Google Calendar cho một kỹ sư (khi họ nghỉ phép thì cả hệ thống bị sập).
- **Ignoring CT Logs:** Không theo dõi CT logs khiến tin tặc có thể cấu kết với một CA nội bộ để cấp chứng chỉ mạo danh mà không bị phát hiện.
- **Wildcard Cert Neglect:** Dùng chứng chỉ wildcard (`*.domain.com`) cho hàng trăm server nhưng không tự động hóa quy trình phân phối sau khi gia hạn.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: 100% tên miền công khai được giám sát tự động với tần suất quét tối thiểu 1 lần/ngày.
- **QG-04**: Cảnh báo khẩn cấp kích hoạt khi bất kỳ chứng chỉ nào còn dưới 14 ngày trước ngày hết hạn.
- **QG-07**: 0% bản ghi DNS mồ côi (Dangling CNAME) trỏ về tài nguyên không tồn tại.

## 10. Security & Safety Boundaries
- Bảo vệ thương hiệu khỏi các cuộc tấn công Man-in-the-Middle và lừa đảo mạo danh thông qua việc phát hiện tức thì chứng chỉ giả mạo.

## 11. Platform Adapters
- **Monitoring Tools**: Certstream, sslmate, testssl.sh, Cloudflare DNS, Route53, Prometheus Blackbox Exporter.

## 12. Deliverables & Output Artifacts
- Kịch bản giám sát thời hạn chứng chỉ TLS tự động.
- Bộ công cụ quét lỗ hổng Subdomain Takeover.
- Cấu hình webhook gửi cảnh báo khẩn cấp tới PagerDuty/Slack.

## 13. Related & Complementary Skills
dex-incident-evidence-preservation, dex-saas-risk-surface-review, dex-secretless-cicd-oidc

## 14. Realistic Usage Example
```powershell
# Kiểm tra chứng chỉ TLS và cấu hình bảo mật bằng testssl.sh
bash testssl.sh --quiet --fast https://my-org.domain.com

# Quét tìm các bản ghi DNS mồ côi bằng subjack
subjack -w subdomains.txt -t 100 -timeout 30 -ssl -v
```
