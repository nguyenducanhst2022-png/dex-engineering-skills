---
name: dex-platform-service-catalog
description: Design and curate Internal Developer Platform (IDP) service catalogs (Backstage, Port) providing golden paths, service ownership, API documentation, and self-service scaffolding. Use to scale developer autonomy.
---

# dex-platform-service-catalog

## 1. Purpose & Scope
Thiết kế, xây dựng và quản trị Cổng danh mục dịch vụ nội bộ (Internal Developer Platform Service Catalog: Spotify Backstage, Port); thiết lập các 'con đường hoàng kim' (Golden Paths), định rõ quyền sở hữu dịch vụ (Service Ownership), tập trung hóa tài liệu API và cung cấp khả năng tự phục vụ (Self-service Scaffolding) cho các kỹ sư phần mềm.

## 2. When to Use
- Số lượng microservices trong công ty vượt quá 50 dịch vụ, không ai nắm rõ dịch vụ nào do ai quản lý.
- Lập trình viên mới mất hàng tuần chỉ để xin quyền và dựng môi trường tạo mới một service.
- Tài liệu API bị phân mảnh và lạc hậu trên nhiều trang wiki khác nhau.

## 3. When NOT to Use
- Không dựng hệ thống IDP cồng kềnh cho các công ty chỉ có dưới 15 kỹ sư phần mềm (chỉ cần file README và tài liệu chung).
- Không biến Service Catalog thành một công cụ quan liêu gây cản trở tốc độ phát triển.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Danh sách các microservices hiện có trong công ty.
- Thông tin đội ngũ sở hữu (Teams, Slack channels, On-call rotation).
- Bản mẫu scaffolding chuẩn (Software Templates cho Node, Python, Go).
- **Điều kiện tiên quyết**:
- Có hệ thống Git tập trung và định danh người dùng SSO (GitHub Org, Okta, Google Workspace).

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- Golden Path: Một lộ trình mẫu được hỗ trợ đầy đủ bởi đội Platform (bao gồm template repo, CI/CD có sẵn, monitoring mặc định), giúp kỹ sư đi nhanh nhất mà không phải phát minh lại cái bánh xe.
- `catalog-info.yaml`: File siêu dữ liệu nằm ngay trong mã nguồn của mỗi service khai báo tên, mô tả, team sở hữu, tài liệu API và dependencies.
- Service Scorecard: Bảng đánh giá mức độ hoàn thiện của service (ví dụ: đã có CI chưa, coverage > 70% chưa, có runbook chưa).
- **Quy tắc quyết định kỹ thuật**:
- Mọi repository mới tạo ra bắt buộc phải có file `catalog-info.yaml` tại thư mục gốc.
- Template scaffolding phải sinh ra một ứng dụng hoàn chỉnh có thể deploy ngay lập tức lên môi trường Dev.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Triển khai Backstage nhưng không ai cập nhật thông tin khiến catalog trở thành 'nghĩa địa thông tin cũ'.

## 6. Step-by-Step Execution Workflow
1. Chuẩn hóa schema của file `catalog-info.yaml` cho toàn công ty.
2. Cài đặt và cấu hình Backstage hoặc Port kết nối với GitHub/GitLab.
3. Xây dựng các Software Templates mẫu (ví dụ: Fastify Microservice, Go Gin API) kèm đầy đủ Dockerfile và CI.
4. Tích hợp Scorecard để tự động chấm điểm độ sẵn sàng sản xuất của từng service.
5. Đào tạo và hướng dẫn các đội ngũ áp dụng Golden Path cho dự án mới.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```yaml
# catalog-info.yaml
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: order-processing-service
  description: 'Xử lý và thanh toán các đơn hàng trực tuyến'
  tags: ['ecommerce', 'golang', 'p0']
spec:
  type: service
  lifecycle: production
  owner: team-checkout
  system: core-banking
  providesApis: ['order-api-v1']
```

### Lệnh xác minh & thực thi:
```bash
# Xác minh tính hợp lệ của catalog-info.yaml bằng CLI
npx @backstage/cli catalog check
```

## 8. Anti-Patterns & Common Traps
- Xây dựng Golden Path nhưng ép buộc cứng nhắc, không cho phép ngoại lệ khi có yêu cầu kỹ thuật đặc biệt.
- Để tình trạng các dịch vụ 'mồ côi' (Orphan services) không có đội ngũ nào chịu trách nhiệm.

## 9. Quality Gates & Acceptance Criteria
- 100% microservices trên production đều có team sở hữu và link PagerDuty rõ ràng.
- Thời gian từ khi kỹ sư chọn template đến khi ứng dụng chạy trên dev dưới 10 phút.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Quyền tạo mới tài nguyên hạ tầng qua self-service portal phải tuân thủ hạn mức ngân sách và có ranh giới bảo mật định sẵn.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ thống hỗ trợ**: Cloud Runtimes (AWS Lambda, Cloudflare Workers, Kubernetes), Linux, Windows 11.

## 12. Deliverables & Output Artifacts
- Cổng thông tin Backstage/Port hoạt động ổn định.
- Bộ Golden Path Templates chuẩn cho các ngôn ngữ chính của công ty.

## 13. Related & Complementary Skills
dex-environment-promotion, dex-gitops-workflows, dex-oncall-handover

## 14. Realistic Usage Example
### Tình huống thực tế:
Một tập đoàn mở rộng từ 40 lên 120 kỹ sư, việc tạo một service mới thường mất 2 tuần để xin quyền hạ tầng và cấu hình CI. Đội Platform ra mắt Backstage Golden Path: kỹ sư chỉ cần nhập tên service trên giao diện web, hệ thống tự động sinh Git repo, cấu hình CI/CD, đăng ký DNS, tạo cụm test và xuất sẵn template Grafana trong đúng 8 phút.
