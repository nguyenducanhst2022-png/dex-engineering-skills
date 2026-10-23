---
name: dex-partition-fault-simulation
description: Simulate and verify distributed network partition faults (split-brain scenarios), analyzing CP vs AP tradeoffs, quorum consensus, and self-healing convergence. Use when verifying distributed databases or multi-node consensus algorithms.
---

# dex-partition-fault-simulation

## 1. Purpose & Scope
Mô phỏng và kiểm thử hành vi của hệ thống phân tán khi xảy ra phân mảnh mạng (Network Partition / Split-Brain Fault Simulation); phân tích thực tế các đánh đổi CAP (Consistency vs Availability), kiểm chứng cơ chế đồng thuận đa số (Quorum Consensus) và khả năng tự phục hồi hội tụ dữ liệu sau khi kết nối mạng được nối lại.

## 2. When to Use
- Khi phát triển hoặc kiểm thử các hệ thống sử dụng thuật toán đồng thuận phân tán (Raft, Paxos, Zab).
- Khi cấu hình cụm cơ sở dữ liệu phân tán (Elasticsearch, MongoDB Replica Set, Kafka, Redis Cluster) và cần xác minh cụm không bị chia đôi nhận ghi đồng thời.
- Khi thiết kế ứng dụng theo hướng Offline-First hoặc Partition-Tolerant.

## 3. When NOT to Use
- Khi hệ thống chỉ là một máy chủ đơn lẻ hoặc ứng dụng kết nối trực tiếp vào một database tập trung duy nhất.
- Khi chưa có môi trường staging cách ly an toàn (tuyệt đối không chạy bài test partition mạng trên production khi chưa có chuẩn bị).

## 4. Prerequisites & Input Context
- **Ngữ cảnh đầu vào:** Cụm phân tán tối thiểu 3-5 nodes, công cụ tiêm lỗi mạng (Toxiproxy, Chaos Mesh, Pumba, iptables), kịch bản phân tách cụm.
- **Quyền hạn truy cập:** Quyền thao tác iptables hoặc cấu hình proxy mạng trên môi trường thử nghiệm.

## 5. Core Concepts & Taxonomy
- **Network Partition (Split-Brain):** Hiện tượng một cụm $N$ node bị chia cắt thành hai hoặc nhiều phân vùng không thể gửi gói tin mạng cho nhau nhưng các node vẫn đang chạy.
- **Majority Quorum ($Q > N/2$):** Phân vùng nào nắm giữ đa số phiếu (> 50% số node) mới được quyền bầu chọn Leader và nhận lệnh ghi; phân vùng thiểu số bắt buộc phải từ chối ghi hoặc chuyển sang trạng thái read-only.
- **State Convergence:** Quá trình các node ở phân vùng thiểu số đồng bộ lại toàn bộ dữ liệu mới nhất từ Leader sau khi mạng được hàn gắn (network healed).

## 6. Step-by-Step Execution Workflow
1. Khởi động cụm thử nghiệm gồm 5 nodes phân tán (Node A, B, C, D, E) và xác định Leader hiện tại (ví dụ: Node A).
2. Sử dụng `iptables` hoặc Toxiproxy để chia cắt mạng: Phân vùng 1 gồm {A, B} và Phân vùng 2 gồm {C, D, E}.
3. Gửi lệnh ghi vào Phân vùng 1 {A, B}: xác nhận lệnh ghi bị từ chối hoặc timeout vì không đủ đa số (chỉ có 2/5 phiếu).
4. Xác nhận Phân vùng 2 {C, D, E} tự động phát hiện mất liên lạc với Leader A, tiến hành bầu cử mới và chọn ra Leader mới (ví dụ: Node C).
5. Gửi lệnh ghi vào Leader mới C: xác nhận ghi thành công vì có đủ đa số (3/5 phiếu).
6. Hàn gắn lại mạng (xóa luật iptables): xác nhận Node A từ bỏ quyền Leader cũ, chấp nhận hạ cấp thành Follower và đồng bộ lại các dữ liệu đã bỏ lỡ từ Node C.

## 7. Concrete Examples
### Ví dụ tiêm lỗi phân mảnh mạng bằng iptables trên môi trường Linux testing:
```bash
# Giả lập phân tách mạng giữa node-01 (Phân vùng thiểu số) và node-02, node-03
# Tại node-01: Chặn toàn bộ gói tin tới node-02 và node-03
iptables -A INPUT -s 10.0.0.2 -j DROP
iptables -A INPUT -s 10.0.0.3 -j DROP
iptables -A OUTPUT -d 10.0.0.2 -j DROP
iptables -A OUTPUT -d 10.0.0.3 -j DROP

# Kiểm tra xem node-01 có tự hạ cấp hoặc từ chối ghi không
curl -X POST http://localhost:8080/api/write -d '{"val": 42}'
# Kỳ vọng: HTTP 503 Service Unavailable / Quorum Not Reached

# Sau khi kiểm tra xong: Hàn gắn mạng bằng cách xóa các rule iptables
iptables -D INPUT -s 10.0.0.2 -j DROP
iptables -D INPUT -s 10.0.0.3 -j DROP
iptables -D OUTPUT -d 10.0.0.2 -j DROP
iptables -D OUTPUT -d 10.0.0.3 -j DROP
```

## 8. Anti-Patterns & Common Traps
- **Split-Brain Dual Leader:** Hệ thống bị chia đôi và cả hai bên đều tự nhận mình là Leader rồi nhận ghi dữ liệu, dẫn tới xung đột dữ liệu vĩnh viễn không thể hòa giải.
- **Even-Numbered Cluster without Arbiter:** Dựng cụm 2 hoặc 4 nodes mà không có node trọng tài (Arbiter), dẫn tới khi chia đôi tỷ lệ là 1:1 hoặc 2:2 và cả hai bên đều không đạt đa số.
- **Indefinite Hang on Partition:** Client gửi request vào phân vùng bị cô lập và bị treo kết nối vô thời hạn do không cấu hình timeout.

## 9. Quality Gates & Acceptance Criteria
- **QG-03**: Hệ thống chứng minh khả năng từ chối lệnh ghi tại phân vùng thiểu số khi bị phân mảnh mạng.
- **QG-09**: Sau khi hàn gắn mạng, 100% các nodes đạt trạng thái đồng thuận và dữ liệu hội tụ nhất quán hoàn toàn.
- **QG-10**: Quá trình bầu cử Leader mới tại phân vùng đa số hoàn tất trong vòng dưới 5 giây.

## 10. Security & Safety Boundaries
- Kiểm tra tính toàn vẹn của các gói tin bầu cử Leader thông qua chữ ký hoặc TLS mutual authentication (mTLS).
- Đảm bảo các node bị cô lập không tiếp tục cấp phát token hoặc phiên đăng nhập hợp lệ cho client.

## 11. Platform Adapters
- **Chaos Tools**: Chaos Mesh, Toxiproxy, Pumba, Jepsen.
- **Protocols**: Raft (etcd, HashiCorp Serf), Paxos.

## 12. Deliverables & Output Artifacts
- Kịch bản tự động hóa mô phỏng phân mảnh mạng (Chaos Experiment).
- Báo cáo phân tích hành vi Quorum Consensus và tính nhất quán dữ liệu.
- Kết quả kiểm chứng tự động hội tụ dữ liệu sau sự cố.

## 13. Related & Complementary Skills
dex-distributed-consistency, dex-clock-skew-resilience, dex-service-failover

## 14. Realistic Usage Example
```powershell
# Chạy bài kiểm tra tự động phân mảnh mạng với Toxiproxy
pytest tests/distributed/test_network_partition_chaos.py -v
```
