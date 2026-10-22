---
name: dex-capacity-planning
description: Calculate infrastructure resource forecasting, load modeling, database IOPS projection, horizontal autoscaling thresholds, and peak traffic planning. Use when sizing cloud servers, preparing for flash sales, or projecting infrastructure scaling.
---

# dex-capacity-planning

## 1. Purpose & Scope
Tính toán, dự báo và lập kế hoạch năng lực hạ tầng phần mềm (Capacity Planning & Resource Forecasting); mô hình hóa tải truy cập người dùng, ước tính nhu cầu CPU, RAM, băng thông mạng và IOPS cơ sở dữ liệu; thiết lập ngưỡng tự động co giãn (Horizontal Pod Autoscaling - HPA) và chuẩn bị hạ tầng chịu tải cho các đợt cao điểm mua sắm (Mega Sale / Black Friday).

## 2. When to Use
- Trước khi tổ chức các chiến dịch tiếp thị lớn, ngày hội giảm giá bùng nổ traffic (Flash Sale).
- Khi ứng dụng liên tục gặp tình trạng nghẽn CPU hoặc cạn kiệt IOPS cơ sở dữ liệu vào các khung giờ cao điểm trong ngày.
- Khi lập dự toán ngân sách hạ tầng điện toán đám mây cho quý hoặc năm tài chính tiếp theo.

## 3. When NOT to Use
- Tối ưu một hàm thuật toán cụ thể trong mã nguồn (dùng `dex-performance-optimization`).
- Xử lý sự cố sập máy chủ đang diễn ra khẩn cấp trên production (dùng `dex-incident-postmortems`).

## 4. Prerequisites & Input Context
**Đầu vào cần thiết:**
- Số lượng người dùng hoạt động đồng thời dự kiến (Concurrent Active Users - CCU).
- Tỷ lệ phân bổ hành vi người dùng (Request Profiles: 80% Đọc, 15% Tìm kiếm, 5% Thanh toán).
- Chỉ số tiêu thụ tài nguyên trung bình của một request (CPU ms per request, Memory per connection).

**Điều kiện tiên quyết:**
- Có kết quả kiểm thử chịu tải (Load Testing / Stress Testing) thực tế từ các công cụ như k6 hoặc Locust.
- Đã thiết lập hệ thống thu thập chỉ số tài nguyên hạ tầng (Datadog, Prometheus, AWS CloudWatch).

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**: Nắm vững cơ chế vận hành theo chuẩn Agent Skills, tuân thủ nghiêm ngặt tính xác định và ranh giới trách nhiệm.
- **Quy tắc quyết định kỹ thuật**:
- **Hệ Số An Toàn Luôn Tối Thiểu 1.5x - 2.0x**: Luôn chuẩn bị hạ tầng lớn hơn 50% đến 100% so với dự báo đỉnh cao nhất của đội ngũ marketing.
- **Không Chờ Đợi Autoscaling Phản Ứng Trong Flash Sale**: Đối với các sự kiện có traffic tăng vọt theo từng giây (từ 100 lên 50,000 CCU trong 10 giây), autoscaling sẽ không kịp phản ứng (thường mất 2-3 phút để bật máy chủ mới); BẮT BUỘC phải Pre-scale máy chủ sẵn sàng trước giờ G.
- **Database Là Nút Cổ Chai Cuối Cùng**: Web servers có thể mở rộng hàng trăm pods dễ dàng, nhưng Database ghi chỉ có 1 Primary instance; mọi phép tính toán năng lực phải lấy giới hạn ghi của Database làm mốc chặn trên.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **Cạn kiệt IOPS khiến Database bị treo cứng**: Do dùng ổ đĩa gp2/gp3 bị hết Burst Balance IOPS -> Khắc phục: Chuyển sang Provisioned IOPS (io2) hoặc nâng mức Baseline IOPS trước ngày sự kiện.
- **Hết Connection Pool làm sập web server**: 50 instances mới bật lên cùng mở 100 connections làm vượt quá `max_connections` của Postgres -> Khắc phục: Đặt PgBouncer hoặc AWS RDS Proxy đứng trước Database để quản lý connection pooling tập trung.

## 6. Step-by-Step Execution Workflow
1. Xác định lưu lượng đỉnh kỳ vọng: Ước tính số lượt yêu cầu trên giây (Peak Requests Per Second - Peak RPS) trong kịch bản cao nhất.
2. Phân tích hồ sơ tài nguyên của từng loại API: API đọc tốn bao nhiêu CPU/RAM, API ghi tốn bao nhiêu IOPS database.
3. Tính toán số lượng máy chủ Web/App cần thiết: $\text{Số Instances} = \frac{\text{Peak RPS} \times \text{Latency}}{\text{Max Concurrency Per Instance}} \times \text{Hệ số dự phòng 1.5}$.
4. Tính toán năng lực cơ sở dữ liệu: Dự phóng IOPS cần thiết, kích thước Connection Pool và dung lượng RAM của Buffer Pool để giữ toàn bộ dữ liệu nóng trong RAM.
5. Thiết lập quy tắc tự động co giãn (Autoscaling Rules): Kích hoạt mở rộng thêm máy chủ khi CPU trung bình vượt quá 65% hoặc số lượng kết nối đồng thời tăng cao.
6. Lên kế hoạch 'Làm Nóng' hạ tầng (Pre-warming): Chủ động tăng số lượng máy chủ và dung lượng Provisioned IOPS trước giờ diễn ra sự kiện 30 phút để tránh độ trễ lúc co giãn.
7. Lập phương án cắt tải khẩn cấp (Load Shedding): Chuẩn bị sẵn cơ chế từ chối các request không thiết yếu khi hệ thống chạm ngưỡng 95% công suất tối đa.

## 7. Concrete Examples
### Ví dụ triển khai chuẩn mực:
```yaml
# k8s/hpa.yaml (Tự động co giãn theo CPU và Custom Metric)
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: checkout-service-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: checkout-service
  minReplicas: 5
  maxReplicas: 50
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 65
```

### Lệnh xác minh & thực thi:
- Chạy kịch bản test tải mô phỏng lưu lượng đỉnh: `k6 run --vus 2000 --duration 10m load_test_peak.js`
- Kiểm tra cấu hình Kubernetes HPA: `kubectl get hpa api-gateway-hpa`
- Xem chỉ số IOPS và CPU database trên AWS CLI: `aws cloudwatch get-metric-statistics ...`

## 8. Anti-Patterns & Common Traps
- **Anti-Pattern 1**: Bỏ qua các bước kiểm tra biên và giả định hệ thống luôn ở trạng thái lý tưởng.
- **Anti-Pattern 2**: Không ghi nhận nhật ký kiểm toán hoặc bỏ qua việc xử lý ngoại lệ lúc runtime.
- **Trap**: Bỏ qua các rào chắn an toàn hoặc cố tình chạy script không qua kiểm thử tự động.

## 9. Quality Gates & Acceptance Criteria
- QG-04: Kịch bản kiểm thử tải đạt mục tiêu Peak RPS mà không có lỗi HTTP 5xx vượt quá 0.1%.
- QG-10: Có tài liệu bảng tính toán năng lực chi tiết (Capacity Sizing Spreadsheet) được lưu trong repository.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động trước khi coi là hoàn thành.

## 10. Security & Safety Boundaries
- Tự động co giãn phải có giới hạn trên tối đa (`max_replicas`) để ngăn chặn việc tài nguyên bị nhân bản vô tận do tin tặc tấn công từ chối dịch vụ (DDoS) làm cạn kiệt ngân sách đám mây.
- Không bao giờ thực thi mã nguồn hoặc thay đổi cấu hình trên môi trường sản xuất mà thiếu cơ chế rollback an toàn.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **CLI & IDE Adapters**: Có thể kích hoạt trực tiếp từ terminal hoặc extension tương thích trong VS Code / Cursor / Windsurf.

## 12. Deliverables & Output Artifacts
- Bản kế hoạch năng lực hạ tầng (`docs/capacity_planning_report.md`).
- File cấu hình Autoscaling (Kubernetes HPA YAML hoặc Terraform AutoScaling Group).
- Kịch bản k6 mô phỏng hồ sơ tải cao điểm.

## 13. Related & Complementary Skills
- `dex-development-workflow`: Quy trình phát triển tiêu chuẩn.
- `dex-code-verification`: Xác minh chất lượng và tính đúng đắn của mã nguồn.
- `dex-master-orchestrator`: Bộ điều phối trung tâm kết nối kỹ năng này với các kỹ năng khác trong hệ thống.

## 14. Realistic Usage Example
### Tình huống thực tế:
Kỹ sư hoặc AI Agent tiếp nhận yêu cầu liên quan đến **dex-capacity-planning**.
1. Đọc kỹ đầu vào và các ràng buộc kỹ thuật tại mục 4.
2. Thực thi tuần tự 6 bước trong Workflow tại mục 6.
3. Chạy các lệnh kiểm chứng tại mục 7 và đối chiếu với Quality Gates tại mục 9.
4. Đóng gói deliverables theo danh sách tại mục 12 và báo cáo kết quả kèm bằng chứng xác thực.
