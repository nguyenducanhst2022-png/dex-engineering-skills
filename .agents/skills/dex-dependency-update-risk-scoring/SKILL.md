---
name: dex-dependency-update-risk-scoring
description: Score, prioritize, and automate dependency updates using semantic risk models, changelog diffing, maintainer reputation heuristics, and regression impact analysis. Use when balancing vulnerability patching against release stability.
---

# dex-dependency-update-risk-scoring

## 1. Purpose & Scope
Chấm điểm rủi ro, phân loại ưu tiên và tự động hóa quá trình cập nhật thư viện phụ thuộc (Dependency Updates); sử dụng mô hình rủi ro ngữ nghĩa, phân tích sai khác changelog, chỉ số uy tín người duy trì gói và phân tích tác động hồi quy; cân bằng hoàn hảo giữa việc vá lỗ hổng bảo mật và độ ổn định của hệ thống.

## 2. When to Use
- Khi hàng tuần nhận được hàng trăm thông báo cập nhật tự động (Dependabot / Renovate PRs) gây quá tải cho đội ngũ kỹ sư review.
- Khi phân vân không biết nên cập nhật ngay một thư viện chứa lỗ hổng CVE hay chờ kiểm thử kỹ hơn do sợ gãy ứng dụng.
- Khi cần phát hiện kịp thời các vụ tấn công chuỗi cung ứng (Package Hijacking / Malicious Version Release) trên npm hoặc PyPI.

## 3. When NOT to Use
- Khi dự án không có bất kỳ thư viện phụ thuộc bên ngoài nào (Zero Dependency Codebase).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** File lockfile dự án (`package-lock.json`, `poetry.lock`, `Cargo.lock`), báo cáo quét lỗ hổng (Snyk, Trivy, Dependabot), cơ sở dữ liệu CVSS/EPSS.
- **Quyền hạn truy cập:** Quyền tạo Pull Request và đọc siêu dữ liệu các gói từ registry.

## 5. Core Concepts & Taxonomy
- **EPSS (Exploit Prediction Scoring System):** Chỉ số xác suất lỗ hổng bảo mật bị khai thác thực tế ngoài tự nhiên trong 30 ngày tới (giúp ưu tiên vá lỗi nguy cơ cao trước).
- **Semantic Versioning Blast Radius:** Đánh giá mức độ rủi ro theo loại bản cập nhật: Patch (Rủi ro thấp), Minor (Rủi ro trung bình), Major (Rủi ro cao - khả năng phá vỡ tương thích).
- **Maintainer Anomaly Detection:** Gắn cờ cảnh báo nếu một gói thư viện phổ biến đột ngột được chuyển giao cho một tài khoản tác giả mới hoặc phát hành bản cập nhật lúc nửa đêm với mã bị làm rối.

## 6. Step-by-Step Execution Workflow
1. Thu thập danh sách các bản cập nhật thư viện đang chờ xử lý từ công cụ quét tự động.
2. Tính toán điểm rủi ro tổng hợp (Composite Risk Score) dựa trên: EPSS score, CVSS severity, khoảng cách phiên bản (SemVer), và chỉ số uy tín gói (OpenSSF Scorecard).
3. Tự động hợp nhất (Auto-Merge) các bản vá lỗi Patch có điểm rủi ro thấp và vượt qua 100% test suite.
4. Với các bản cập nhật Major, trích xuất và phân tích cú pháp changelog để làm nổi bật các thay đổi phá vỡ tương thích (Breaking Changes).
5. Kiểm tra thời gian tồn tại của bản phát hành: không tự động cài đặt các bản phát hành mới ra mắt dưới 72 giờ (Cool-off Period) để phòng ngừa gói độc hại.
6. Phân bổ công việc review cho các kỹ sư phụ trách module tương ứng.

## 7. Concrete Examples
### Hàm tính toán điểm số rủi ro cập nhật thư viện trong Python:
```python
def calculate_update_risk(semver_type: str, cvss_score: float, epss_score: float, package_age_days: int) -> dict:
    score = 0.0
    
    # 1. Rủi ro thay đổi tương thích (SemVer)
    if semver_type == "major": score += 40.0
    elif semver_type == "minor": score += 15.0
    elif semver_type == "patch": score += 5.0
    
    # 2. Mức độ khẩn cấp an ninh (EPSS va CVSS)
    if epss_score > 0.5: score += 30.0 # Nguy co rat cao dang bi khai thac
    score += cvss_score * 2.0
    
    # 3. Yếu tố an toàn thời gian phát hành (Cool-off Period)
    if package_age_days < 3:
        quarantine = True
        reason = "Goi moi phat hanh duoi 72 gio, can cach ly de phong ma doc chuoi cung ung!"
    else:
        quarantine = False
        reason = "Du dieu kien danh gia cap nhat."
        
    return {"risk_score": score, "quarantine": quarantine, "reason": reason}
```

## 8. Anti-Patterns & Common Traps
- **Blind Auto-Merging Everything:** Tự động hợp nhất mọi PR của Dependabot mà không qua kiểm thử khiến production bị sập khi thư viện bên thứ ba gặp lỗi.
- **Ignoring Updates for Years:** Để thư viện lỗi thời qua nhiều năm khiến việc nâng cấp sau này trở thành cơn ác mộng tái cấu trúc toàn diện.
- **Immediate Zero-Day Adoption:** Cài đặt phiên bản mới ngay sau 5 phút phát hành mà không có thời gian quan sát cộng đồng.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Các bản cập nhật tự động bắt buộc phải vượt qua 100% bộ kiểm thử tích hợp trước khi hợp nhất.
- **QG-04**: Áp dụng thời gian cách ly tối thiểu 72 giờ (Cool-off Period) cho các gói thư viện mới phát hành.
- **QG-08**: Các lỗ hổng bảo mật có chỉ số EPSS > 0.3 được đưa vào danh sách xử lý khẩn cấp trong vòng 48 giờ.

## 10. Security & Safety Boundaries
- Chặn đứng các vụ tấn công đầu độc mã nguồn mở (như vụ việc xz-utils hoặc event-stream) bằng cơ chế cách ly thời gian.

## 11. Platform Adapters
- **Tools**: Renovate, Dependabot, OpenSSF Scorecard, Snyk, Trivy, Socket.dev.

## 12. Deliverables & Output Artifacts
- Ma trận chấm điểm rủi ro cập nhật phụ thuộc.
- Cấu hình Renovate / Dependabot có thiết lập thời gian cách ly.
- Quy trình tự động phân loại và hợp nhất an toàn.

## 13. Related & Complementary Skills
dex-saas-risk-surface-review, dex-package-publishing-preflight, dex-sbom-binary-correlation

## 14. Realistic Usage Example
```powershell
# Kiểm tra điểm số bảo mật OpenSSF Scorecard của một thư viện mã nguồn mở
docker run -e GITHUB_AUTH_TOKEN=$TOKEN gcr.io/openssf/scorecard:stable --repo=github.com/expressjs/express

# Chạy quét lỗ hổng và chấm điểm rủi ro bằng Trivy
trivy fs --scanners vuln .
```
