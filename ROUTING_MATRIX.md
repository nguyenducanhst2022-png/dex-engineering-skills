# DEX Dynamic Skill Routing Matrix v4.0

Ma trận định tuyến động kích hoạt chính xác tổ hợp kỹ năng tối thiểu cần thiết cho 16 kịch bản kỹ thuật thực tế (Scenarios A through P) xuyên suốt 12 phân nhóm chuyên môn.

---

## 1. Routing Scenarios Catalog

### Scenario A: Emergency Database Migration Failure
- **Bối cảnh**: Migration cơ sở dữ liệu production bị lỗi giữa chừng, khóa bảng và gãy foreign keys.
- **Primary Skills**: `dex-root-cause-debugging`, `dex-database-engineering`, `dex-schema-evolution`
- **Complementary Skills**: `dex-disaster-recovery`, `dex-production-monitoring`, `dex-incident-postmortems`

### Scenario B: AI-Powered Search & RAG Service Implementation
- **Bối cảnh**: Xây dựng công cụ tìm kiếm tài liệu doanh nghiệp kết hợp hybrid search và tóm tắt bằng LLM.
- **Primary Skills**: `dex-rag-pipelines`, `dex-retrieval-evaluation`, `dex-llm-integration`
- **Complementary Skills**: `dex-search-engineering`, `dex-tool-calling-contracts`, `dex-llm-cost-controls`

### Scenario C: Monorepo Architecture Modernization
- **Bối cảnh**: Di chuyển 12 repository độc lập về một monorepo duy nhất có Turborepo remote caching.
- **Primary Skills**: `dex-monorepo-governance`, `dex-repository-bootstrap`, `dex-code-organization`
- **Complementary Skills**: `dex-developer-tooling`, `dex-cicd-automation`, `dex-semantic-version-automation`

### Scenario D: High-Concurrency Real-time Collaborative Canvas
- **Bối cảnh**: Phát triển bảng vẽ trực tuyến hỗ trợ 50,000 người dùng đồng thời qua WebSocket.
- **Primary Skills**: `dex-realtime-protocols`, `dex-concurrency-state`, `dex-event-driven-architecture`
- **Complementary Skills**: `dex-caching-strategies`, `dex-frontend-performance`, `dex-performance-optimization`

### Scenario E: Enterprise SaaS Multi-Tenant Isolation & Authentication
- **Bối cảnh**: Thiết lập SSO doanh nghiệp, thu hồi phiên làm việc tức thì và phân quyền Row-Level Security.
- **Primary Skills**: `dex-auth-session-lifecycle`, `dex-access-control-tenancy`, `dex-secrets-management`
- **Complementary Skills**: `dex-security-audit`, `dex-threat-modeling`, `dex-database-engineering`

### Scenario F: Mission-Critical Production Outage Postmortem
- **Bối cảnh**: Chủ trì buổi postmortem không đổ lỗi sau khi cổng thanh toán sập 45 phút.
- **Primary Skills**: `dex-incident-postmortems`, `dex-production-monitoring`, `dex-root-cause-debugging`
- **Complementary Skills**: `dex-reliability-engineering`, `dex-documentation-as-code`

### Scenario G: Cross-Platform Windows & POSIX Developer CLI Tooling
- **Bối cảnh**: Xây dựng CLI đa nền tảng có hỗ trợ gói WinGet, POSIX flags và shell completions.
- **Primary Skills**: `dex-cli-engineering`, `dex-cross-platform-portability`, `dex-windows-packaging`
- **Complementary Skills**: `dex-developer-tooling`, `dex-plugin-architecture`, `dex-release-engineering`

### Scenario H: Automated Release & Semantic Versioning Pipeline
- **Bối cảnh**: Tự động hóa phân tích commit conventional, sinh changelog và xuất bản đa registry.
- **Primary Skills**: `dex-semantic-version-automation`, `dex-release-engineering`, `dex-cicd-automation`
- **Complementary Skills**: `dex-git-workflow`, `dex-supply-chain-security`, `dex-code-verification`

### Scenario I: Data Contract Breaking Change Mitigation
- **Bối cảnh**: Phát hiện và xử lý thay đổi schema phá vỡ tương thích giữa event producers và data pipeline.
- **Primary Skills**: `dex-data-contracts`, `dex-schema-evolution`, `dex-data-quality-audits`
- **Complementary Skills**: `dex-data-pipelines`, `dex-data-lineage`, `dex-api-contract-evolution`

### Scenario J: Chaos Engineering & System Resilience Validation
- **Bối cảnh**: Thử nghiệm độ trễ mạng giả lập bằng Toxiproxy và kiểm tra circuit breaker fallback.
- **Primary Skills**: `dex-chaos-experiments`, `dex-reliability-engineering`, `dex-performance-optimization`
- **Complementary Skills**: `dex-production-monitoring`, `dex-property-based-testing`, `dex-capacity-planning`

### Scenario K: Hermetic Offline Integration Testing & Mock Virtualization
- **Bối cảnh**: Chạy bài kiểm thử tích hợp cô lập mạng hoàn toàn bằng stubs và mock server.
- **Primary Skills**: `dex-testing-engineering`, `dex-api-engineering`, `dex-code-verification`
- **Complementary Skills**: `dex-cicd-automation`, `dex-specification-driven`

### Scenario L: Defensive Binary & Web Bundle Security Auditing
- **Bối cảnh**: Kiểm toán an ninh tệp PE/ELF và bundle JavaScript để phát hiện endpoint nội bộ lộ lọt.
- **Primary Skills**: `dex-security-audit`, `dex-threat-modeling`, `dex-code-verification`
- **Complementary Skills**: `dex-supply-chain-security`, `dex-secrets-management`

### Scenario M: Zero-Downtime Multi-Region Kubernetes Rollout (Group J)
- **Bối cảnh**: Triển khai phiên bản microservice quan trọng lên cụm K8s với Argo Canary và phân tích Prometheus.
- **Primary Skills**: `dex-zero-downtime-rollouts`, `dex-kubernetes-deployment`, `dex-slo-error-budgets`
- **Complementary Skills**: `dex-service-mesh-networking`, `dex-distributed-tracing`, `dex-container-image-engineering`

### Scenario N: Offline-First Mobile Synchronization & Biometrics (Group K)
- **Bối cảnh**: Xây dựng ứng dụng di động hoạt động hoàn hảo khi mất mạng và đồng bộ nền khi có mạng.
- **Primary Skills**: `dex-mobile-offline-sync`, `dex-android-app-architecture`, `dex-native-device-integration`
- **Complementary Skills**: `dex-ios-app-architecture`, `dex-mobile-performance-profiling`, `dex-desktop-ipc-design`

### Scenario O: FinOps Cloud Cost Anomaly & Resource Right-Sizing (Group J)
- **Bối cảnh**: Hóa đơn đám mây tăng 40%; cần phân tích chi phí, dọn tài nguyên mồ côi và right-sizing.
- **Primary Skills**: `dex-cloud-cost-finops`, `dex-infrastructure-as-code`, `dex-capacity-planning`
- **Complementary Skills**: `dex-storage-lifecycle`, `dex-cloud-service-integration`

### Scenario P: Enterprise Compliance Audit & Tamper-Evident Trail (Group L)
- **Bối cảnh**: Chuẩn bị kiểm toán SOC 2 Type II, thiết lập audit log Merkle/WORM và rà soát drift.
- **Primary Skills**: `dex-compliance-control-mapping`, `dex-audit-trail-integrity`, `dex-privacy-impact-assessment`
- **Complementary Skills**: `dex-configuration-drift`, `dex-operational-readiness-review`, `dex-runbook-automation`
