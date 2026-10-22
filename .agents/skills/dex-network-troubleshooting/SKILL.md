---
name: dex-network-troubleshooting
description: Troubleshoot and diagnose network connectivity, DNS resolution, TLS certificates, TCP handshake states, HTTP latency, and packet drops using tcpdump, curl, dig, traceroute, and netstat. Use when debugging distributed networking and connectivity failures.
---

# dex-network-troubleshooting

## 1. Purpose & Scope
Chẩn đoán, cô lập và khắc phục sự cố mạng phân tán từ tầng liên kết tới tầng ứng dụng (L3 đến L7); xử lý các vấn đề phân giải tên miền (DNS Resolution), chứng chỉ TLS/SSL, bắt tay TCP (SYN/ACK, RST, Retransmission), độ trễ bất thường (High Latency), nghẽn băng thông, MTU Blackhole và rớt gói tin bằng các công cụ chuyên dụng: `dig`, `curl`, `tcpdump`, `traceroute`, `ss`, `openssl`.

## 2. When to Use
- Khi microservice không thể kết nối tới cơ sở dữ liệu hoặc external API (Lỗi `Connection refused`, `ETIMEDOUT`, `No route to host`).
- Khi xuất hiện lỗi DNS định kỳ (`i/o timeout`, `NXDOMAIN`, CoreDNS throttling).
- Khi kết nối HTTPS thất bại do lỗi chứng chỉ (`x509: certificate signed by unknown authority`, `SSL_ERROR_SYSCALL`).

## 3. When NOT to Use
- Tối ưu hóa câu lệnh truy vấn SQL (dùng `dex-database-query-plans`).
- Thiết lập cấu hình Istio VirtualService (dùng `dex-service-mesh-networking`).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào**:
- Địa chỉ Host/IP nguồn và đích, cổng dịch vụ (Port), giao thức (TCP, UDP, HTTP/1.1, HTTP/2).
- Mã lỗi hoặc chuỗi ngoại lệ mạng (Socket Exception).
- Môi trường chạy (Bare-metal, Docker container, K8s Pod).
- **Điều kiện tiên quyết**:
- Quyền truy cập terminal hoặc ephemeral debug container (`kubectl debug`).
- Bộ công cụ chẩn đoán mạng (`net-tools`, `iproute2`, `bind-tools`, `curl`, `openssl`).

## 5. Core Concepts & Taxonomy
- **Nguyên lý hoạt động cốt lõi**:
- **OSI Layer Isolation Methodology**: Kiểm tra tuần tự từ dưới lên: L3 (Ping / ARP) -> L4 (TCP Port connectivity bằng `nc` / `telnet`) -> L6 (TLS Handshake qua `openssl`) -> L7 (HTTP response bằng `curl`).
- **DNS Search Path Amplification (ndots:5 Trap)**: Trong K8s, truy vấn tên miền ngoài có thể bị gắn đuôi `.default.svc.cluster.local` tới 4 lần nếu không có dấu chấm kết thúc (`example.com.` vs `example.com`).
- **TCP RST vs Timeout Signatures**: `Connection Refused` (RST packet ngay lập tức -> Port không có process lắng nghe); `Connection Timed Out` (SYN gửi đi không phản hồi -> Firewall/Security Group chặn hoặc routing sai).
- **Quy tắc quyết định kỹ thuật**:
- **Chẩn Đoán Từ Pod Nội Tại**: Luôn thực hiện lệnh kiểm tra từ chính bên trong container bị lỗi hoặc ephemeral debug container chia sẻ network namespace (`kubectl debug -it <pod> --target=<container>`).
- **Kiểm Tra DNS Đầu Tiên**: Hơn 60% sự cố mạng phân tán bắt nguồn từ phân giải DNS chậm hoặc cache hỏng.
- **Không Đoán Mò Khi Chưa Bắt Gói Tin**: Sử dụng `tcpdump` để ghi lại file `.pcap` khi gặp lỗi TCP Reset chập chờn.
- **Các kịch bản hỏng hóc & Cách phòng ngừa**:
- **K8s Pod gọi domain ngoài bị chậm 5 giây**: Do CoreDNS bị nghẽn UDP request vì lỗi `ndots:5` -> Khắc phục: Giảm `ndots:2` trong Pod `dnsConfig` hoặc thêm dấu chấm vào cuối domain (`api.stripe.com.`).
- **Lỗi chứng chỉ TLS hết hạn làm sập kết nối**: Microservice từ chối kết nối tới upstream -> Khắc phục: Dùng `openssl s_client -connect host:443` để xem hạn dùng và chuỗi CA bundle.

## 6. Step-by-Step Execution Workflow
1. Thu thập thông tin lỗi chính xác: Host đích, Port, giao thức, tần suất xuất hiện.
2. Kiểm tra phân giải DNS: `dig +trace +stats destination.domain` và kiểm tra file `/etc/resolv.conf`.
3. Kiểm tra khả năng mở cổng TCP: `nc -zv -w 3 destination.ip port` hoặc `curl -v telnet://destination:port`.
4. Kiểm tra bắt tay TLS và chuỗi chứng chỉ: `openssl s_client -connect destination:443 -servername destination -showcerts`.
5. Đo lường chi tiết các mốc thời gian HTTP bằng cờ định dạng của curl: `curl -w "@curl-format.txt" -o /dev/null -s https://destination`.
6. Trường hợp lỗi phức tạp: Chạy `tcpdump -i any -nn port 8080 -w trace.pcap` và phân tích trên Wireshark.
7. Tổng hợp nguyên nhân gốc (RCA) và đưa ra giải pháp sửa đổi (Security Group, CoreDNS config, Route table).

## 7. Concrete Examples
### Ví dụ cấu hình / mã nguồn chuẩn mực:
```bash
# File định dạng đo thời gian latency chi tiết của curl: curl-format.txt
# time_namelookup:    %{time_namelookup}s\n
# time_connect:       %{time_connect}s\n
# time_appconnect:    %{time_appconnect}s (TLS Handshake)\n
# time_pretransfer:   %{time_pretransfer}s\n
# time_starttransfer: %{time_starttransfer}s (TTFB)\n
# time_total:         %{time_total}s\n

# Lệnh thực thi chẩn đoán một dòng:
curl -w "namelookup: %{time_namelookup}s | connect: %{time_connect}s | tls: %{time_appconnect}s | total: %{time_total}s\n" \
     -o /dev/null -sS https://api.internal.corp/healthz
```

### Lệnh xác minh & thực thi:
- Kiểm tra DNS cục bộ: `nslookup kubernetes.default`
- Kiểm tra kết nối TCP nhanh: `timeout 3 bash -c '</dev/tcp/10.0.0.1/443' && echo 'OPEN' || echo 'CLOSED'`
- Bắt gói tin TCP SYN/RST: `tcpdump -i any 'tcp[tcpflags] & (tcp-syn|tcp-rst) != 0' -c 20`
- Kiểm tra bảng định tuyến: `ip route get 8.8.8.8`

## 8. Anti-Patterns & Common Traps
- **Chỉ dùng `ping` để kết luận mạng bình thường**: ICMP có thể được mở nhưng TCP port 443 bị Security Group chặn.
- **Bỏ qua cờ `-servername` khi dùng `openssl s_client`**: Khiến server trả về chứng chỉ mặc định sai (SNI failure).
- **Khởi động lại toàn bộ cụm khi gặp lỗi DNS**: Xóa mất dấu vết log của CoreDNS mà không giải quyết được gốc rễ.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Xác định chính xác tầng mạng bị lỗi (L3, L4, L6, hay L7) kèm bằng chứng thực thi.
- QG-06: Đưa ra lệnh kiểm chứng có thể tái lập được (reproducible verification command).
- QG-11: Khắc phục sự cố mà không tạo thêm lỗ hổng an ninh trên tường lửa.
- Mọi thay đổi phải vượt qua bài kiểm thử tự động và xác minh an toàn trước khi deploy.

## 10. Security & Safety Boundaries
- Thận trọng khi dùng `tcpdump` trên production để không ghi lại payload chứa mật khẩu hoặc thẻ tín dụng dạng plain text.
- Xóa bỏ các debug pod hoặc công cụ chẩn đoán sau khi hoàn tất phiên làm việc.
- Không bao giờ lưu trữ hardcoded secret hoặc cấp quyền quá mức (over-permissioned IAM).

## 11. Platform Adapters
- **OpenAI Codex**: Tương thích hoàn toàn thông qua cấu trúc file `SKILL.md` và agent instructions tiêu chuẩn.
- **Universal Agent Skills**: Tuân thủ đặc tả tại `https://agentskills.io/specification`.
- **Môi trường Cloud & Container**: Hỗ trợ Docker, Kubernetes (EKS/GKE/AKS), Terraform/OpenTofu, OpenTelemetry.

## 12. Deliverables & Output Artifacts
- Báo cáo chẩn đoán mạng kèm kết quả các lệnh `dig`, `openssl`, `curl`.
- File capture gói tin `trace.pcap` (nếu cần thiết).
- Đề xuất khắc phục cấu hình định tuyến / DNS / tường lửa.

## 13. Related & Complementary Skills
- `dex-root-cause-debugging`: Phương pháp phân tích nguyên nhân gốc rễ sự cố.
- `dex-service-mesh-networking`: Chẩn đoán khi proxy Envoy can thiệp vào mạng.
- `dex-incident-postmortems`: Ghi nhận sự cố mạng vào báo cáo postmortem.

## 14. Realistic Usage Example
### Tình huống thực tế:
Một pod backend liên tục gặp lỗi timeout khi gọi dịch vụ thanh toán của bên thứ ba. Kỹ sư sử dụng `dex-network-troubleshooting`, chạy lệnh `curl -w` bên trong pod phát hiện `time_namelookup` mất tới 5.001 giây. Kiểm tra `/etc/resolv.conf` thấy cấu hình `options ndots:5` khiến truy vấn bị gửi tới CoreDNS nhiều lần trước khi ra ngoài. Kỹ sư tối ưu `dnsConfig` cho Pod, giảm thời gian phản hồi từ 5.1s xuống 45ms.
