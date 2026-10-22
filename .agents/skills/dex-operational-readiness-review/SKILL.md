---
name: dex-operational-readiness-review
description: Conduct Production Operational Readiness Reviews (ORR) across reliability, security, observability, disaster recovery, and supportability. Use before launching major features or services to production.
---

# dex-operational-readiness-review

## 1. Purpose & Scope
Thiết kế, chuẩn hóa và chủ trì quy trình Đánh giá Mức độ Sẵn sàng Vận hành Sản xuất (Operational Readiness Review - ORR / Production Readiness Review - PRR); rà soát toàn diện hệ thống phần mềm và hạ tầng trước khi chính thức mở cổng cho người dùng thực tế; đánh giá nghiêm ngặt trên 5 trụ cột cốt lõi: Độ tin cậy (Reliability & SLOs), An toàn thông tin (Security & Threat Modeling), Khả năng quan sát (Observability: Dashboards & Alerts), Khả năng phục hồi thảm họa (Disaster Recovery & Backups) và Năng lực hỗ trợ vận hành (Supportability & Runbooks); ban hành quyết định Go / No-Go dựa trên bằng chứng kỹ thuật khách quan.

## 2. When to Use
- Khi một microservice mới, ứng dụng mới hoặc tính năng cốt lõi chuẩn bị ra mắt lần đầu trên môi trường Production.
- Khi hệ thống có đợt nâng cấp kiến trúc lớn (Chuyển đổi Monolith sang Microservices, Migrate Database, Đổi Cloud Provider).
- Khi doanh nghiệp chuẩn bị bước vào chiến dịch bán hàng quy mô lớn (Black Friday, Tết Mega Sale) đòi hỏi hệ thống chịu tải gấp 10 lần.

## 3. When NOT to Use
- Đánh giá chất lượng của một Pull Request thông thường (dùng `dex-code-review`).
- Kiểm tra tính tuân thủ pháp lý định kỳ hàng năm (dùng `dex-compliance-control-mapping`).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Kiến trúc hệ thống và sơ đồ luồng dữ liệu (Architecture & Data Flow Diagrams).
- Báo cáo kiểm thử tải (Load Testing & Capacity Benchmarks).
- Dashboard giám sát, Alerting rules, SLO definitions và Runbooks vận hành tương ứng.
- Báo cáo quét bảo mật (SAST, DAST, Container Scan, Pentest report).
- **Điều kiện tiên quyết**:
- Dịch vụ đã vượt qua toàn bộ các bài kiểm thử chức năng (E2E, Acceptance Tests) trên Staging.
- Các bên liên quan (Tech Lead, SRE Lead, Security Lead, Product Manager) tham gia phiên họp ORR.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- **The 5 Operational Pillars**: 1. Reliability (SLO, Circuit breaker, Graceful degradation); 2. Observability (Logs, Metrics, Traces, On-call alerts); 3. Security (Least privilege, Encryption, Pentest sign-off); 4. Scalability (Load test 3x peak, Auto-scaling); 5. Operability (Documented runbooks, On-call escalation path).
- **Evidence-Based Go/No-Go Decision**: Quyết định phát hành không dựa trên sự lạc quan hay áp lực tiến độ kinh doanh; mỗi tiêu chí bắt buộc phải có liên kết tới bằng chứng kỹ thuật cụ thể (Test report URL, Dashboard URL, Runbook URL).
- **Blast Radius Containment**: Đảm bảo dịch vụ mới có cơ chế cô lập phạm vi ảnh hưởng; nếu dịch vụ này sập hoàn toàn, các phần còn lại của hệ thống vẫn phải hoạt động bình thường (Graceful Degradation).
- **Quy tắc quyết định kỹ thuật**:
- **Quy Tắc No-Go Bắt Buộc (Hard Blockers)**: Tự động đánh No-Go nếu: 1. Thiếu Runbook xử lý sự cố; 2. Chưa thực hiện kiểm thử tải (Load Test); 3. Còn tồn tại lỗ hổng bảo mật mức CRITICAL hoặc HIGH; 4. Chưa cấu hình cảnh báo tới PagerDuty/Slack on-call.
- **Phải Có Phương Án Rollback Đã Được Kiểm Nghiệm**: Mọi đợt phát hành bắt buộc phải có phương án lùi xe (Rollback Plan) với thời gian thực thi dưới 15 phút.
- **Không Release Vào Chiều Thứ Sáu**: Cấm triển khai các đợt phát hành ORR lớn vào chiều thứ Sáu hoặc ngay trước kỳ nghỉ lễ trừ trường hợp khẩn cấp.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Ra mắt sản phẩm mới làm sập luôn hệ thống cũ**: Do dịch vụ mới gửi lượng truy vấn khổng lồ đánh sập cơ sở dữ liệu dùng chung -> Khắc phục: Yêu cầu cô lập connection pool và kiểm thử tải tích hợp trước khi duyệt ORR.
- **Hệ thống gặp sự cố lúc nửa đêm nhưng không ai nhận được cảnh báo**: Do cấu hình Alertmanager sai routing email thay vì gọi PagerDuty -> Khắc phục: Tiêu chí ORR bắt buộc phải diễn tập bắn thử 1 cảnh báo giả (Synthetic Alert) tới máy người trực on-call.

## 6. Step-by-Step Execution Workflow
1. Khởi tạo tài liệu ORR Checklist theo mẫu chuẩn trước ngày ra mắt dự kiến 2 tuần.
2. Đội ngũ phát triển điền thông tin và đính kèm bằng chứng kỹ thuật cho từng tiêu chí kiểm tra.
3. Tổ chức phiên họp thẩm định ORR chính thức với sự tham gia của Tech Lead, SRE, Security và Product Manager.
4. Thực hiện diễn tập tại chỗ: Bắn thử alert, kiểm tra khả năng khôi phục backup và chạy thử Runbook.
5. Đánh giá rủi ro và phân loại kết quả: GO (Đạt toàn bộ), CONDITIONAL GO (Đạt các mục chính, còn nợ một số mục nhỏ cam kết sửa trong 3 ngày), hoặc NO-GO (Dừng phát hành).
6. Nếu CONDITIONAL GO hoặc NO-GO: Lập danh sách Action Items gắn deadline và người chịu trách nhiệm.
7. Lưu trữ biên bản ký duyệt ORR vào kho tài liệu quản trị hệ thống.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```markdown
# Production Operational Readiness Review (ORR) Scorecard

### 1. Thông Tin Dịch Vụ
- **Tên Dịch Vụ**: Notification & Marketing Engine v2.0
- **Tech Lead**: Nguyen Van A | **SRE Lead**: Tran Van B | **Ngày Đánh Giá**: 2026-10-22
- **Quyết Định Cuối Cùng**: **GO (APPROVED FOR PRODUCTION)**

### 2. Bảng Đánh Giá 5 Trụ Cột Vận Hành

### Trụ Cột 1: Khả Năng Quan Sát (Observability) - [PASS]
- [x] Đã thiết lập Dashboard Grafana theo dõi: QPS, Error Rate 5xx, P99 Latency, CPU/RAM.
- [x] Đã cấu hình Alert P1/P2 tích hợp PagerDuty tới đội ngũ On-call (Đã test bắn alert thành công).
- [x] Log ứng dụng tuân thủ chuẩn JSON có gắn correlation `trace_id`.

### Trụ Cột 2: Độ Tin Cậy & Hiệu Năng (Reliability & Scalability) - [PASS]
- [x] Đã kiểm thử tải (Load Test) đạt 15,000 req/s (Gấp 3 lần tải dự kiến cao điểm) với P99 < 150ms.
- [x] Đã cấu hình Auto-scaling (HPA) từ 5 Pods lên tối đa 30 Pods dựa trên CPU và Queue Length.
- [x] Đã cấu hình Circuit Breaker ngắt kết nối an toàn khi nhà cung cấp SMS/Email bị nghẽn.

### Trụ Cột 3: An Toàn Thông Tin (Security) - [PASS]
- [x] Quét lỗ hổng Trivy 0 CVE Critical/High; SonarQube Pass Quality Gate.
- [x] Đã thực hiện Threat Modeling và mã hóa dữ liệu người dùng at-rest bằng AWS KMS.
- [x] IAM Role tuân thủ Least Privilege, không có static credentials.

### Trụ Cột 4: Sao Lưu & Khôi Phục (Disaster Recovery) - [PASS]
- [x] Database bật Automated Backup hàng ngày + Point-in-time recovery (PITR) 35 ngày.
- [x] Đã diễn tập restore thành công dữ liệu sang cụm Staging trong thời gian 18 phút (RTO < 30m).

### Trụ Cột 5: Năng Lực Vận Hành & Hỗ Trợ (Operability) - [PASS]
- [x] Có đầy đủ 3 Runbooks: `restart_workers.md`, `flush_stuck_queues.md`, `switch_sms_provider.md`.
- [x] Lịch trực On-call đã được cấu hình trên PagerDuty với 2 kỹ sư chính và 1 kỹ sư dự phòng.
- [x] Kế hoạch Rollback chi tiết sẵn sàng: Thời gian hoàn nguyên dự kiến < 5 phút qua ArgoCD.
```

### Lệnh xác minh & thực thi:
- Kiểm tra tính sẵn sàng của Dashboard: `curl -f -s https://grafana.internal/api/dashboards/uid/notification-engine`
- Bắn thử nghiệm alert kiểm tra hệ thống trực: `curl -X POST https://alertmanager.internal/api/v1/alerts -d '[{"labels":{"alertname":"ORRTestAlert","severity":"critical"}}]'`
- Kiểm tra kết quả báo cáo kiểm thử tải: Mở báo cáo HTML từ k6 hoặc Locust: `cat loadtest-report.summary`

## 8. Anti-Patterns & Common Traps
- **Duyệt ORR hình thức qua loa để kịp deadline tiếp thị**: Bỏ qua các cảnh báo đỏ để rồi hệ thống sập ngay trong giờ ra mắt.
- **Chỉ kỹ sư phát triển tự đánh giá và tự duyệt cho chính mình**: Thiếu góc nhìn phản biện khách quan từ đội ngũ SRE và Security.
- **Không ghi nhận biên bản và cam kết hành động**: Khiến các vấn đề kỹ thuật bị lãng quên sau khi sản phẩm đã lên sóng.

## 9. Quality Gates & Acceptance Criteria
- QG-01: 100% các tiêu chí bắt buộc trong ORR Checklist đều có bằng chứng nghiệm thu kỹ thuật đính kèm.
- QG-09: Thời gian phục hồi Rollback khi có sự cố được chứng minh thực tế dưới 15 phút.
- QG-11: Toàn bộ 4 bên liên quan (Tech, SRE, Sec, Product) đồng thuận ký duyệt quyết định GO.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi deploy.

## 10. Security & Safety Boundaries
- Báo cáo đánh giá ORR không chứa mật khẩu hoặc dữ liệu nhạy cảm của khách hàng.
- Mọi ngoại lệ an ninh (Security Exceptions) phải có chữ ký bảo lãnh bằng văn bản của CISO hoặc Head of Security.
- Không bao giờ lưu trữ hardcoded secret hoặc cấp quyền quá mức (over-permissioned IAM).

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Môi trường Vận hành & Tuân thủ**: Hỗ trợ GDPR/CCPA tooling, SOC 2 / ISO 27001 automation, ArgoCD drift, RICE spreadsheets, Jira/GitHub triage.

## 12. Deliverables & Output Artifacts
- Bản Đánh Giá Mức Độ Sẵn Sàng Vận Hành (ORR Scorecard / Report).
- Biên bản quyết định Go / No-Go chính thức.
- Danh sách các hạng mục tồn đọng cần theo dõi sau ra mắt (Post-Launch Action Items).

## 13. Related & Complementary Skills
- `dex-slo-error-budgets`: Xác lập mục tiêu cam kết chất lượng dịch vụ trong ORR.
- `dex-runbook-automation`: Đảm bảo các quy trình vận hành đã sẵn sàng trước khi ký duyệt.
- `dex-threat-modeling`: Đánh giá an ninh kiến trúc trước thềm ORR.

## 14. Realistic Usage Example
### Tình huống thực tế:
Một ngân hàng số chuẩn bị ra mắt tính năng cho vay tiêu dùng trực tuyến trong tuần tới. Tech Lead chủ trì buổi Operational Readiness Review (ORR) cùng SRE Lead và Security Lead. Khi rà soát trụ cột Khôi phục thảm họa, SRE phát hiện cơ chế sao lưu tự động của cụm DB mới chưa được kiểm tra khôi phục thử lần nào. Hội đồng thống nhất đánh dấu CONDITIONAL GO, yêu cầu đội ngũ thực hiện diễn tập khôi phục DB thành công trên môi trường thử nghiệm và nộp lại báo cáo trong 24 giờ trước khi mở cổng chính thức cho người dùng.
