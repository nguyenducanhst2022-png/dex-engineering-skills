---
name: dex-cloud-database-failover-drills
description: Plan, orchestrate, and audit cloud database failover drills (AWS RDS Multi-AZ, Azure Flexible, Cloud SQL HA). Verify RTO, RPO, connection pool draining, and client reconnection.
---

# dex-cloud-database-failover-drills

## 1. Purpose & Scope
Lập kế hoạch, điều phối và kiểm toán các cuộc diễn tập chuyển đổi dự phòng cơ sở dữ liệu đám mây (Cloud Database Failover Drills: AWS RDS Multi-AZ, Azure Database Flexible Server HA, Google Cloud SQL HA); đo lường thực tế thời gian phục hồi mục tiêu (Recovery Time Objective - RTO) và điểm phục hồi mục tiêu (Recovery Point Objective - RPO); kiểm chứng tính bền bỉ của vùng đệm kết nối ứng dụng (Connection Pool Draining & Reconnection Logic), bảo đảm không xảy ra mất mát dữ liệu hoặc gián đoạn dịch vụ kéo dài.

## 2. When to Use
- Khi tiến hành diễn tập khắc phục thảm họa định kỳ (Disaster Recovery GameDay) cho hệ thống tài chính, ngân hàng hoặc thương mại điện tử.
- Khi cấu hình hoặc nâng cấp các cụm CSDL đám mây sang kiến trúc Multi-AZ hoặc Read-Replica tự động thăng cấp.
- Khi kiểm thử khả năng tự động kết nối lại (Auto-reconnect with Exponential Backoff) của các backend microservices.

## 3. When NOT to Use
- Khi cơ sở dữ liệu chỉ là môi trường phát triển cục bộ một node duy nhất (Single-Instance Local Dev).
- Khi bảo trì nâng cấp phần mềm ứng dụng thông thường không liên quan tới tầng lưu trữ dữ liệu.

## 4. Prerequisites & Input Context
- **Hạ tầng CSDL:** Cụm CSDL đám mây đã bật cơ chế High Availability (Multi-AZ replication).
- **Công cụ điều phối:** AWS CLI, Azure CLI, hoặc Terraform/Chaos Engineering tools (Chaos Mesh, Gremlin).

## 5. Core Concepts & Taxonomy
- **RTO (Recovery Time Objective):** Khoảng thời gian tối đa cho phép hệ thống CSDL ngừng trệ trước khi khôi phục lại trạng thái hoạt động bình thường (thường mục tiêu < 60s cho Multi-AZ).
- **RPO (Recovery Point Objective):** Lượng dữ liệu tối đa chấp nhận bị mất mát tính theo đơn vị thời gian do sự cố (mục tiêu RPO = 0 cho replication đồng bộ).
- **Split-Brain Prevention:** Cơ chế giải quyết tranh chấp ngăn chặn hai node CSDL cùng nhận quyền ghi (Primary) tại cùng một thời điểm.

## 6. Step-by-Step Execution Workflow
1. Thiết lập giám sát liên tục luồng giao dịch của ứng dụng với tải giả lập (Synthetic Traffic Generator).
2. Kích hoạt lệnh chuyển đổi dự phòng có chủ đích: `aws rds reboot-db-instance --force-failover`.
3. Đo đạc chính xác thời điểm máy chủ chính bắt đầu ngừng nhận kết nối (t0) đến khi replica được thăng cấp và DNS chuyển hướng hoàn tất (t1).
4. Theo dõi phản ứng của backend pooler (HikariCP, PgBouncer): ghi nhận tỷ lệ lỗi kết nối và thời gian tự phục hồi.
5. Thực hiện kiểm toán toàn vẹn dữ liệu: đối chiếu số lượng bản ghi ghi nhận được trong suốt thời gian diễn tập.
6. Lập báo cáo kiểm toán diễn tập failover kèm biểu đồ phân tích độ trễ và các khuyến nghị tối ưu tham số timeout.

## 7. Concrete Examples
### Kich ban tu dong hoa dien tap failover AWS RDS va do RTO bang Python:
```python
import boto3
import time
import psycopg2

RDS_IDENTIFIER = "production-postgres-ha"
DB_HOST = "production-postgres-ha.cxyz.us-east-1.rds.amazonaws.com"

def measure_database_failover():
    rds = boto3.client('rds', region_name='us-east-1')
    print(f"Triggering manual failover for {RDS_IDENTIFIER}...")
    
    start_time = time.time()
    rds.reboot_db_instance(DBInstanceIdentifier=RDS_IDENTIFIER, ForceFailover=True)
    
    downtime_start = None
    recovered_time = None
    
    # Vong lap kiem tra ket noi moi 1 giay
    for attempt in range(120):
        try:
            conn = psycopg2.connect(
                host=DB_HOST, dbname="app_db", user="db_user",
                password="secret_password", connect_timeout=2
            )
            cur = conn.cursor()
            cur.execute("SELECT inet_server_addr(), now();")
            server_ip, current_ts = cur.fetchone()
            conn.close()
            
            if downtime_start and not recovered_time:
                recovered_time = time.time()
                rto_seconds = recovered_time - downtime_start
                print(f"[RECOVERED] Failover completed! RTO: {rto_seconds:.2f}s | New Master IP: {server_ip}")
                break
            print(f"[{attempt}s] Connection healthy to master ({server_ip})")
        except Exception as e:
            if not downtime_start:
                downtime_start = time.time()
                print(f"[OUTAGE DETECTED] Master unreachable at {downtime_start - start_time:.2f}s mark.")
        time.sleep(1)

measure_database_failover()
```

## 8. Anti-Patterns & Common Traps
- **Infinite Connection Pool Timeout:** Đặt `connectionTimeout` trong pooler quá lớn (ví dụ 60 giây) khiến các luồng ứng dụng bị treo chờ đợi thay vì fail-fast và retry.
- **Hardcoded Master IP Addresses:** Cấu hình ứng dụng kết nối trực tiếp vào địa chỉ IP tĩnh thay vì sử dụng DNS CNAME Endpoint của AWS RDS, khiến ứng dụng không tự chuyển hướng sau khi failover.
- **Conducting Drills in Production Without Rollback Plan:** Diễn tập failover trên môi trường production trong giờ cao điểm mà không có kịch bản hủy khẩn cấp khi hệ thống replica bị trễ sao chép (replication lag).

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Thời gian RTO thực tế đo được không vượt quá 60 giây trong suốt quá trình chuyển đổi dự phòng.
- **QG-02**: Không có bất kỳ giao dịch nào đã commit thành công bị mất mát dữ liệu (RPO = 0).
- **QG-03**: Backend connection pooler tự động kết nối lại 100% các kết nối sạch sau khi node mới thăng cấp.

## 10. Security & Safety Boundaries
- Diễn tập phải được cấp quyền hạn thông qua Ticket phê duyệt thay đổi (Change Request) có chữ ký của Security & Reliability Lead.

## 11. Platform Adapters
- **Runtimes**: AWS RDS Multi-AZ, Azure Database Flexible Server, Cloud SQL HA, Chaos Mesh, PgBouncer.

## 12. Deliverables & Output Artifacts
- Kịch bản điều phối diễn tập tự động (`failover_drill_runner.py`).
- Báo cáo kết quả kiểm toán thời gian gián đoạn và RTO/RPO (`failover_audit_report.md`).

## 13. Related & Complementary Skills
dex-api-circuit-breaker-verification, dex-storage-backup-restore-drills, dex-operational-dependency-mapping

## 14. Realistic Usage Example
```bash
# Kich hoat failover co cuong che bang AWS CLI
aws rds reboot-db-instance --db-instance-identifier mydb --force-failover
```
