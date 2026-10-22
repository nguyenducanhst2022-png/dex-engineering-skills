---
name: dex-service-discovery
description: Architect, tune, and debug resilient service discovery mechanisms using DNS-based, client-side, and control-plane registries (CoreDNS, Envoy, Consul). Use when microservices fail to resolve or route dynamically.
---

# dex-service-discovery

## 1. Purpose & Scope
Thiết kế, tinh chỉnh và xử lý sự cố cơ chế khám phá dịch vụ (Service Discovery: CoreDNS, Consul, Envoy Control Plane, AWS Cloud Map); bảo đảm các dịch vụ tìm thấy nhau một cách động, xử lý cân bằng tải phía client hoặc qua Service Mesh, và chống sụp đổ do ngộ độc bộ nhớ đệm DNS (DNS Cache Poisoning / TTL Misconfigurations).

## 2. When to Use
- Microservices gặp lỗi `Name or service not known` hoặc kết nối tới các IP của pod đã bị xóa (Stale IPs).
- Cụm CoreDNS trong Kubernetes bị quá tải CPU do các ứng dụng liên tục gửi truy vấn DNS mỗi khi gọi API.
- Cần kết nối linh hoạt giữa các dịch vụ chạy trên Kubernetes với các dịch vụ legacy chạy trên máy chủ ảo.

## 3. When NOT to Use
- Không cần thiết lập Consul cluster phức tạp nếu ứng dụng chỉ chạy thuần túy trên một cụm Kubernetes duy nhất (CoreDNS nội bộ là đủ).
- Không dùng hardcoded IP tĩnh cho các dịch vụ đám mây có tính co giãn động.

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Kiến trúc kết nối mạng giữa các dịch vụ.
- Cấu hình DNS client (ndots, search domains, resolv.conf).
- Cơ chế đăng ký dịch vụ (Service Registry: Kubernetes Service, Consul, Eureka).
- **Điều kiện tiên quyết**:
- Có quyền kiểm tra cấu hình CoreDNS hoặc Service Mesh trong cụm cluster.

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- CoreDNS `ndots:5` Problem: Mặc định trong Linux/Kubernetes, nếu tên miền có ít hơn 5 dấu chấm, client sẽ thử tìm kiếm lần lượt qua các search domains (`.default.svc.cluster.local`, `.svc.cluster.local`), sinh ra tới 4 truy vấn DNS lỗi trước khi hỏi ra ngoài Internet, làm nghẽn CoreDNS.
- Client-side vs Server-side Discovery: Server-side đi qua Load Balancer trung gian; Client-side (như gRPC/Envoy) tự hỏi Registry và kết nối trực tiếp tới IP đích, giảm một hop mạng.
- DNS Negative Caching: Khi một pod đang khởi động chưa kịp sẵn sàng, DNS có thể cache trạng thái NXDOMAIN làm ứng dụng không gọi được trong suốt thời gian TTL.
- **Quy tắc quyết định kỹ thuật**:
- Với các ứng dụng có tần suất gọi API lớn: bật NodeLocal DNSCache trong Kubernetes để giảm 80% tải cho CoreDNS.
- Đặt DNS TTL trong ứng dụng ở mức 5-30 giây để cân bằng giữa tốc độ cập nhật IP mới và giảm tải truy vấn.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- Ứng dụng Java (JVM) mặc định cache kết quả DNS thành công mãi mãi (TTL = infinity), khi pod đích đổi IP mới thì app Java vẫn kết nối vào IP cũ và ném lỗi Connection Refused.

## 6. Step-by-Step Execution Workflow
1. Rà soát cấu hình `/etc/resolv.conf` của ứng dụng và tinh chỉnh `ndots:2` nếu gọi domain ngoài.
2. Cài đặt và cấu hình NodeLocal DNSCache trên từng Kubernetes node.
3. Thiết lập thông số JVM `-Dnetworkaddress.cache.ttl=10` cho các dịch vụ Java.
4. Cấu hình Health-based Service Registration trong Consul hoặc Envoy.
5. Kiểm tra thời gian cập nhật danh sách endpoint khi một pod bị kill.

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```yaml
# Tối ưu hóa cấu hình DNS trong Kubernetes Pod Spec
spec:
  dnsConfig:
    options:
      - name: ndots
        value: "2"
      - name: single-request-reopen
  containers:
    - name: app
      image: app:v1
```

### Lệnh xác minh & thực thi:
```bash
# Kiểm tra độ trễ và đường đi phân giải DNS từ bên trong pod
kubectl exec -it app-pod -- nslookup payment-service.default.svc.cluster.local
```

## 8. Anti-Patterns & Common Traps
- Giữ nguyên thiết lập mặc định của JVM cache DNS vĩnh viễn trong môi trường Cloud động.
- Hardcode IP của máy chủ vào file cấu hình ứng dụng.

## 9. Quality Gates & Acceptance Criteria
- Thời gian phân giải DNS trung bình trong cụm phải dưới 1ms qua NodeLocal DNSCache.
- Cập nhật và định tuyến sang IP mới trong vòng 3 giây sau khi pod cũ bị hủy.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi chuyển sang bước tiếp theo.

## 10. Security & Safety Boundaries
- Bảo vệ Service Registry chống lại việc đăng ký giả mạo dịch vụ bằng cách áp dụng mTLS và Token Authentication.
- Không bao giờ thực thi câu lệnh có tính hủy diệt hoặc làm rò rỉ dữ liệu nhạy cảm ra ngoài môi trường kiểm thử.

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Hệ thống hỗ trợ**: Cloud Runtimes (AWS Lambda, Cloudflare Workers, Kubernetes), Linux, Windows 11.

## 12. Deliverables & Output Artifacts
- File cấu hình tối ưu CoreDNS và NodeLocal DNSCache.
- Báo cáo phân tích hiệu năng truy vấn DNS của cụm.

## 13. Related & Complementary Skills
dex-cloud-network-design, dex-service-failover, dex-kubernetes-policy-enforcement

## 14. Realistic Usage Example
### Tình huống thực tế:
Một hệ thống thanh toán bị chậm vào giờ cao điểm, các kỹ sư phát hiện CoreDNS bị quá tải với 50,000 queries/giây. Sau khi phân tích lỗi `ndots:5` và triển khai NodeLocal DNSCache, số lượng truy vấn tới CoreDNS trung tâm giảm 85%, độ trễ phân giải DNS giảm từ 30ms xuống 0.2ms, chấm dứt hoàn toàn hiện tượng timeout.
