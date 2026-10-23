---
name: dex-legacy-strangler-migration
description: Execute legacy system modernization using the Strangler Fig pattern with routing facades, shadow traffic verification, and incremental cutover. Use when replacing monolithic systems with modern services while maintaining continuous production availability.
---

# dex-legacy-strangler-migration

## 1. Purpose & Scope
Thực hiện lộ trình hiện đại hóa ứng dụng cũ theo mẫu Strangler Fig Pattern; thiết lập API facade định tuyến thông minh, sao chép lưu lượng thực tế để kiểm tra chạy song song (shadow traffic verification), và chuyển đổi từng phần tính năng sang hệ thống mới với khả năng rollback tức thời.

## 2. When to Use
- Khi cần thay thế một hệ thống monolithic legacy cồng kềnh nhưng không thể dừng hoạt động để viết lại từ đầu (Big Bang rewrite).
- Khi muốn giảm thiểu rủi ro kinh doanh bằng cách bóc tách từng dịch vụ nhỏ và đưa vào sản xuất từng bước.
- Khi cần đối chiếu độ chính xác của kết quả xử lý giữa hệ thống mới và hệ thống cũ trên dữ liệu thực.

## 3. When NOT to Use
- Khi ứng dụng cũ quá nhỏ và không còn người sử dụng, có thể viết lại và chuyển đổi trong vài ngày.
- Khi hệ thống cũ không có bất kỳ API hoặc giao diện nào để gắn lớp định tuyến Facade.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Bản đồ chức năng hệ thống cũ, reverse proxy hoặc API gateway có khả năng định tuyến theo trọng số (weighted routing), hệ thống so sánh dữ liệu kết quả.
- **Quyền hạn truy cập:** Quyền cấu hình API Gateway / Load Balancer và phân tích log truy cập.

## 5. Core Concepts & Taxonomy
- **Strangler Facade:** Lớp trung gian đứng trước cả hệ thống cũ và mới, tiếp nhận toàn bộ request từ client và quyết định chuyển tiếp tới hệ thống phù hợp.
- **Dark Launch / Shadow Traffic:** Nhân bản request thật từ client để gửi song song tới hệ thống mới mà không trả kết quả cho client, dùng để so sánh độ trễ và tính chính xác.
- **Canary Cutover:** Chuyển dần lưu lượng thực từ 1%, 5%, 25%, 50% tới 100% sang hệ thống mới sau khi đã xác nhận tính ổn định.

## 6. Step-by-Step Execution Workflow
1. Đặt API Gateway hoặc Reverse Proxy (Envoy, Kong, NGINX) làm Strangler Facade đứng trước hệ thống legacy.
2. Lựa chọn một module nghiệp vụ cụ thể có ranh giới rõ ràng để xây dựng lại trên kiến trúc mới.
3. Cấu hình Shadow Traffic tại Facade để sao chép 100% request của module đó sang service mới và ghi log so sánh kết quả (`diff`).
4. Phân tích kết quả so sánh để khắc phục toàn bộ các điểm sai lệch logic trước khi phục vụ người dùng thật.
5. Bắt đầu chuyển đổi lưu lượng thực tế theo cơ chế Canary Cutover từ 5% lên 100% kèm theo giám sát lỗi.
6. Vô hiệu hóa và xóa bỏ mã nguồn legacy tương ứng sau khi hệ thống mới chạy ổn định sau thời gian bảo hành.

## 7. Concrete Examples
### Ví dụ cấu hình NGINX làm Strangler Facade hỗ trợ phân chia lưu lượng theo endpoint:
```nginx
upstream legacy_backend {
    server legacy-app.internal:8080;
}

upstream modern_service {
    server payment-v2.internal:3000;
}

server {
    listen 80;
    server_name api.dex.dev;

    # 1. Endpoint cũ đã được chuyển đổi hoàn toàn sang hệ thống mới
    location /api/v1/payments {
        proxy_pass http://modern_service;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $remote_addr;
    }

    # 2. Toàn bộ các endpoint còn lại tiếp tục trỏ về hệ thống Legacy
    location / {
        proxy_pass http://legacy_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $remote_addr;
    }
}
```

## 8. Anti-Patterns & Common Traps
- **Big Bang Switchover:** Cố gắng chuyển đổi 100% hệ thống trong một đêm gây ra thảm họa mất dữ liệu và dừng dịch vụ.
- **Dual Write without Reconciliation:** Ghi dữ liệu đồng thời vào hai database nhưng không có công cụ tự động đối soát sai lệch.
- **Permanent Half-Strangled State:** Dừng dự án khi mới chuyển đổi được 30%, để lại hai hệ thống chạy song song vĩnh viễn gây tăng gấp đôi chi phí vận hành.

## 9. Quality Gates & Acceptance Criteria
- **QG-03**: Hệ thống mới vượt qua giai đoạn shadow traffic với tỷ lệ kết quả khớp tối thiểu 99.99%.
- **QG-07**: Độ trễ p99 của service mới phải thấp hơn hoặc bằng hệ thống cũ trước khi cutover.
- **QG-10**: Cơ chế rollback về hệ thống cũ được kiểm tra và kích hoạt thành công trong dưới 60 giây.

## 10. Security & Safety Boundaries
- Kiểm tra xác thực và phân quyền nhất quán giữa lớp Facade và cả hai hệ thống backend.
- Ngăn chặn việc nhân bản request nhạy cảm trong shadow traffic gây trùng lặp giao dịch tài chính (ví dụ: cấm shadow các API trừ tiền trực tiếp).

## 11. Platform Adapters
- **API Gateways**: Envoy, Kong, NGINX, Cloudflare Workers.
- **Traffic Mirroring**: AWS VPC Traffic Mirroring, Istio VirtualService mirroring.

## 12. Deliverables & Output Artifacts
- Tệp cấu hình Strangler Facade Proxy.
- Báo cáo kết quả so sánh dữ liệu Shadow Traffic.
- Kế hoạch chuyển đổi từng giai đoạn và kịch bản rollback khẩn cấp.

## 13. Related & Complementary Skills
dex-zero-downtime-rollouts, dex-feature-flags, dex-change-impact-analysis

## 14. Realistic Usage Example
```powershell
# Chạy công cụ đối soát kết quả phản hồi giữa hệ thống cũ và mới
python scripts/diff_shadow_traffic.py --endpoint /api/v1/payments --samples 5000
```
