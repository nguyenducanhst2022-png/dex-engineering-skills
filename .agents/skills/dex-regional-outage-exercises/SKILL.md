---
name: dex-regional-outage-exercises
description: Simulate and execute controlled multi-region cloud outage drills, DNS failover rerouting, stateful database promotion, and RTO/RPO measurement. Use when proving disaster recovery readiness or passing enterprise business continuity audits.
---

# dex-regional-outage-exercises

## 1. Purpose & Scope
Mô phỏng và thực thi có kiểm soát các bài tập ứng phó sự cố sập trung tâm dữ liệu khu vực (Regional Cloud Outage Drills / Disaster Recovery); kiểm chứng cơ chế tự động chuyển vùng DNS, nâng cấp cơ sở dữ liệu phụ thành chính (Database Promotion), và đo lường chính xác các chỉ số RTO (Recovery Time Objective) và RPO (Recovery Point Objective).

## 2. When to Use
- Khi chuẩn bị cho các đợt diễn tập ứng phó thảm họa định kỳ theo yêu cầu của hội đồng quản trị hoặc kiểm toán tuân thủ (SOC 2, ISO 22301).
- Khi xác nhận năng lực phục vụ liên tục của hệ thống đa vùng (Multi-Region Active-Passive hoặc Active-Active).
- Khi kiểm chứng xem quy trình tài liệu vận hành thảm họa (Disaster Recovery Runbook) có thực sự hoạt động trong thực tế hay không.

## 3. When NOT to Use
- Khi hệ thống chỉ được mua gói hạ tầng đơn vùng (Single Region) và chưa có môi trường dự phòng thứ hai.
- Khi chưa có sự phê duyệt và giám sát trực tiếp từ đội ngũ chỉ huy sự cố (Incident Commander).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Kế hoạch diễn tập thảm họa đã phê duyệt, hệ thống DNS có hỗ trợ Health Checks và Failover (Route53, Cloudflare), cụm database có Replica tại vùng dự phòng.
- **Quyền hạn truy cập:** Quyền quản trị hạ tầng đám mây và DNS định tuyến mạng.

## 5. Core Concepts & Taxonomy
- **RTO (Recovery Time Objective):** Khoảng thời gian tối đa cho phép hệ thống phục hồi lại dịch vụ bình thường sau sự cố (ví dụ: RTO < 15 phút).
- **RPO (Recovery Point Objective):** Lượng dữ liệu tối đa chấp nhận bị mất mát tính theo đơn vị thời gian do độ trễ sao chép bất đồng bộ (ví dụ: RPO < 1 phút).
- **Split-Brain Prevention:** Cơ chế bảo đảm khi vùng dự phòng được nâng cấp làm chính thì vùng cũ phải bị cách ly hoàn toàn (fenced off) để tránh hai vùng cùng ghi dữ liệu mâu thuẫn.

## 6. Step-by-Step Execution Workflow
1. Họp thống nhất phạm vi diễn tập, phân công vai trò (Incident Commander, Tech Leads, Scribe) và xác định điều kiện dừng khẩn cấp (Abort Criteria).
2. Ghi nhận chỉ số latency sao chép database hiện tại để ước tính RPO ban đầu.
3. Kích hoạt giả lập sự cố sập vùng chính: ngắt toàn bộ lưu lượng vào vùng chính tại tầng DNS hoặc cô lập Security Groups.
4. Bắt đầu bấm giờ đo RTO; theo dõi hệ thống DNS tự động chuyển hướng request sang vùng dự phòng hoặc thực hiện chuyển đổi thủ công theo runbook.
5. Nâng cấp database replica tại vùng dự phòng thành primary write master.
6. Chạy bộ smoke test kiểm thử toàn diện trên vùng mới để xác nhận chức năng đọc/ghi bình thường.
7. Dừng bấm giờ, tính toán RTO/RPO thực tế, và thực hiện quy trình phục hồi về trạng thái ban đầu (Failback).

## 7. Concrete Examples
### Ví dụ kịch bản kiểm tra chuyển đổi DNS Failover trong Route53 bằng AWS CLI:
```bash
# 1. Giả lập vùng us-east-1 bị lỗi bằng cách chuyển trạng thái Health Check sang UNHEALTHY
aws route53 change-resource-record-sets \
  --hosted-zone-id Z123456EXAMPLE \
  --change-batch '{
    "Changes": [{
      "Action": "UPSERT",
      "ResourceRecordSet": {
        "Name": "health-primary.dex.dev.",
        "Type": "A",
        "TTL": 60,
        "ResourceRecords": [{"Value": "192.0.2.1"}]
      }
    }]
  }'

# 2. Theo dõi bản ghi DNS công khai xem đã chuyển hướng sang vùng dự phòng us-west-2 chưa
watch -n 5 "dig +short api.dex.dev"

# 3. Nâng cấp Read Replica tại us-west-2 thành Standalone Primary
aws rds promote-read-replica \
  --db-instance-identifier dex-db-us-west-2-replica
```

## 8. Anti-Patterns & Common Traps
- **Unannounced Production Drills:** Tự ý cắt mạng vùng chính trên môi trường thật mà không thông báo trước cho các bên liên quan.
- **Ignoring the Failback Phase:** Diễn tập chuyển đổi sang vùng mới thành công nhưng không có kế hoạch đưa dữ liệu và lưu lượng quay trở lại vùng ban đầu.
- **Unmeasured Drills:** Diễn tập xong nhưng không đo đạc thời gian RTO hoặc không tính toán lượng bản ghi bị mất mát (RPO).

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Có kế hoạch diễn tập và phê duyệt chính thức bằng văn bản từ cấp quản lý.
- **QG-03**: Thời gian phục hồi RTO thực tế đo được đáp ứng ngưỡng cam kết trong SLA.
- **QG-10**: Toàn bộ dữ liệu sau khi failover bảo đảm tính toàn vẹn và không bị xung đột khóa.

## 10. Security & Safety Boundaries
- Bảo đảm các chứng chỉ SSL/TLS và bí mật cấu hình (Secrets) đã được đồng bộ sẵn sàng tại vùng dự phòng từ trước.
- Cách ly triệt để vùng bị sập cũ để ngăn ngừa hiện tượng split-brain ghi đè dữ liệu.

## 11. Platform Adapters
- **DNS**: AWS Route 53 Application Recovery Controller, Cloudflare Load Balancing.
- **Databases**: AWS Aurora Global Database failover, PostgreSQL pg_promote.

## 12. Deliverables & Output Artifacts
- Báo cáo kết quả diễn tập thảm họa (Disaster Recovery Drill Report) kèm chỉ số RTO/RPO đo được.
- Tài liệu cập nhật Disaster Recovery Runbook.
- Danh sách các điểm cần khắc phục và cải tiến (Action Items).

## 13. Related & Complementary Skills
dex-operational-readiness-review, dex-reliability-engineering, dex-service-failover

## 14. Realistic Usage Example
```powershell
# Chạy script tự động đo lường độ trễ sao chép giữa hai vùng trước khi diễn tập
python scripts/measure_replication_lag.py --primary us-east-1 --standby us-west-2
```
