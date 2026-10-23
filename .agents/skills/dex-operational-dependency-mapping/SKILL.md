---
name: dex-operational-dependency-mapping
description: Map, analyze, and visualize service dependency graphs and critical operational paths. Identify Single Points of Failure (SPOF), evaluate blast radius, and accelerate incident triage.
---

# dex-operational-dependency-mapping

## 1. Purpose & Scope
Thiết lập bản đồ phụ thuộc vận hành hệ thống (Operational Dependency Mapping); thu thập và trực quan hóa đồ thị phụ thuộc giữa các dịch vụ microservices, cơ sở dữ liệu, hàng đợi và API bên thứ ba dựa trên dấu vết phân tán (Distributed Traces - OpenTelemetry), Service Mesh (Istio) hoặc công nghệ eBPF; phân tích đường găng trọng yếu (Critical Path), phát hiện các điểm lỗi đơn lẻ (Single Point of Failure - SPOF), đánh giá bán kính ảnh hưởng sự cố (Blast Radius Modeling) và tăng tốc độ xử lý sự cố.

## 2. When to Use
- Khi điều tra nguyên nhân gốc rễ (Root Cause Analysis - RCA) của các sự cố phức tạp liên quan đến nhiều dịch vụ gọi chéo nhau.
- Khi chuẩn bị thực hiện các đợt bảo trì hoặc thay đổi lớn về kiến trúc và cần biết dịch vụ nào sẽ bị ảnh hưởng nếu một node bị gián đoạn.
- Khi thiết kế kiến trúc hệ thống phân tán để loại bỏ các phụ thuộc vòng (Circular Dependencies) hoặc các nút thắt cổ chai ẩn.

## 3. When NOT to Use
- Khi hệ thống là một khối nguyên khối (Monolith) độc lập hoàn toàn không có tương tác với bất kỳ dịch vụ hay CSDL bên ngoài nào.
- Khi chỉ theo dõi các chỉ số tài nguyên phần cứng đơn giản (CPU/RAM usage máy chủ đơn lẻ).

## 4. Prerequisites & Input Context
- **Hạ tầng giám sát:** OpenTelemetry Instrumentation trên các dịch vụ, Jaeger/Tempo, hoặc eBPF-based agent (DeepFlow, Cilium Hubble).
- **Cơ sở dữ liệu đồ thị:** Neo4j hoặc NetworkX (Python) để mô hình hóa đồ thị có hướng (Directed Graph).

## 5. Core Concepts & Taxonomy
- **Critical Path Analysis:** Tuyến đường thực thi dài nhất hoặc quan trọng nhất trong chuỗi các cuộc gọi dịch vụ quyết định trực tiếp tới độ trễ phản hồi của người dùng cuối.
- **Blast Radius:** Phạm vi thiệt hại và danh sách tất cả các dịch vụ cấp dưới (Downstream Consumers) bị ngừng hoạt động nếu một dịch vụ cấp trên (Upstream Service) bị sập.
- **Circular Dependency Lock:** Hiện tượng dịch vụ A gọi B, B gọi C, và C lại quay ngược lại gọi A, tạo thành vòng lặp vô tận có thể làm sập toàn bộ hệ thống khi có tải cao.

## 6. Step-by-Step Execution Workflow
1. Thu thập dữ liệu dấu vết phân tán từ OpenTelemetry Collector hoặc dữ liệu mạng eBPF.
2. Trích xuất các cặp quan hệ nguồn - đích: `(caller_service, target_service, p95_latency, error_rate)`.
3. Xây dựng đồ thị có hướng (Directed Graph - DAG) bằng NetworkX hoặc truy vấn đồ thị Cypher trên Neo4j.
4. Thực hiện thuật toán phát hiện chu trình (Cycle Detection) để khẳng định không tồn tại phụ thuộc vòng giữa các dịch vụ.
5. Tính toán độ trung tâm (Betweenness Centrality) để xác định dịch vụ nào là Single Point of Failure (SPOF).
6. Xuất bản đồ phụ thuộc tương tác và tích hợp vào quy trình cảnh báo trực ban (PagerDuty / Slack Alert Enrichment).

## 7. Concrete Examples
### Script Python phan tich do thi phu thuoc dich vu va tim SPOF bang NetworkX:
```python
import networkx as nx
import json

def analyze_service_dependencies(edges_data):
    G = nx.DiGraph()

    # Them cac canh phu thuoc (Caller -> Callee)
    for edge in edges_data:
        G.add_edge(edge['caller'], edge['callee'], weight=edge.get('latency_ms', 10))

    print(f"Total Services: {G.number_of_nodes()} | Total Dependencies: {G.number_of_edges()}")

    # 1. Phat hien phu thuoc vong (Circular Dependencies)
    cycles = list(nx.simple_cycles(G))
    if cycles:
        print(f"[CRITICAL ALERT] Found {len(cycles)} Circular Dependency cycles:")
        for c in cycles:
            print("  Cycle: " + " -> ".join(c) + " -> " + c[0])
    else:
        print("[OK] No circular dependencies detected.")

    # 2. Xac dinh Single Point of Failure (SPOF) dua tren Betweenness Centrality
    centrality = nx.betweenness_centrality(G)
    sorted_spof = sorted(centrality.items(), key=lambda x: x[1], reverse=True)[:5]
    print("
Top 5 Critical Central Services (Potential SPOF):")
    for svc, score in sorted_spof:
        print(f"  - {svc:<24}: Centrality Score = {score:.4f}")

    # 3. Tinh toan Blast Radius neu mot dich vu bi sap
    target_failed_service = sorted_spof[0][0]
    affected_services = nx.ancestors(G, target_failed_service)
    print(f"
Blast Radius if '{target_failed_service}' fails: {len(affected_services)} upstream services affected!")
    for s in affected_services:
        print(f"  * {s}")

# Du lieu mau
edges = [
    {"caller": "api-gateway", "callee": "auth-service"},
    {"caller": "api-gateway", "callee": "order-service"},
    {"caller": "order-service", "callee": "payment-service"},
    {"caller": "order-service", "callee": "inventory-service"},
    {"caller": "payment-service", "callee": "auth-service"},
    {"caller": "inventory-service", "callee": "database-cluster"},
    {"caller": "auth-service", "callee": "database-cluster"}
]

analyze_service_dependencies(edges)
```

## 8. Anti-Patterns & Common Traps
- **Static Outdated Architecture Diagrams:** Dựa vào các biểu đồ vẽ tay trên Confluence hoặc Miro đã lỗi thời 2 năm trước thay vì sinh bản đồ tự động từ dữ liệu mạng thực tế.
- **Hidden Transitive Dependencies:** Bỏ qua các phụ thuộc gián tiếp (A gọi B, B gọi C) dẫn đến việc đánh giá sai lệch bán kính ảnh hưởng khi bảo trì dịch vụ C.
- **Ignoring Third-Party External APIs:** Không đưa các API của bên thứ ba (như Stripe, Twilio) vào đồ thị phụ thuộc khiến đội trực ban bị mù thông tin khi đối tác gặp sự cố.

## 9. Quality Gates & Acceptance Criteria
- **QG-01**: Đồ thị phụ thuộc được cập nhật tự động hàng ngày từ dữ liệu OpenTelemetry traces hoặc Service Mesh.
- **QG-02**: Không có bất kỳ chu trình phụ thuộc vòng (Circular Dependency) nào tồn tại giữa các dịch vụ cốt lõi.
- **QG-03**: Mọi dịch vụ được xác định là SPOF đều có phương án dự phòng hoặc Circuit Breaker bảo vệ.

## 10. Security & Safety Boundaries
- Dữ liệu dấu vết và bản đồ phụ thuộc phải được làm sạch các thông tin nhạy cảm (Sanitize authorization headers và credentials).

## 11. Platform Adapters
- **Runtimes**: OpenTelemetry, Jaeger, Istio Kiali, Cilium Hubble, NetworkX (Python), Neo4j.

## 12. Deliverables & Output Artifacts
- Mô-đun phân tích đồ thị phụ thuộc (`dependency_graph_analyzer.py`).
- Biểu đồ đồ thị phụ thuộc dạng ma trận và danh sách các điểm SPOF trọng yếu (`architecture_dependency_map.json`).

## 13. Related & Complementary Skills
dex-cloud-database-failover-drills, dex-api-circuit-breaker-verification, dex-release-progressive-metrics

## 14. Realistic Usage Example
```bash
# Trich xuat danh sach phu thuoc tu Jaeger API va phan tich do thi
python -m scripts.ops.map_dependencies --jaeger-url http://localhost:16686 --lookback 24h
```
