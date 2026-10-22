# DEX Engineering Skills Framework v5.0 — Dynamic Routing Matrix

> **Comprehensive Multi-Domain Dispatch Matrix for Master Orchestrator**  
> Covers 20 real-world engineering scenarios corresponding to Groups A through T, detailing primary/complementary skill chains, execution modes, and mandatory Quality Gates.

---

## 1. Routing Engine Overview

The `dex-master-orchestrator` parses incoming developer prompts, extracts semantic intent, and resolves execution plans through a Directed Acyclic Graph (DAG) of specialized skills.

```mermaid
graph TD
    Prompt[Engineering Request] --> Intent[Intent & Scope Extraction]
    Intent --> SelectMode{Select Mode}
    SelectMode -->|Trivial/Bugfix| QUICK[QUICK MODE]
    SelectMode -->|Feature/Refactor| STANDARD[STANDARD MODE]
    SelectMode -->|Arch/Infra/Sec| STRICT[STRICT MODE]
    
    Intent --> MapGroup[Map to Domain Group A-T]
    MapGroup --> ResolveDAG[Resolve Primary & Complementary DAG]
    ResolveDAG --> ExecuteChain[Execute Skills Sequentially/Concurrently]
    ExecuteChain --> EnforceGates[Enforce Quality Gates QG-01..15]
    EnforceGates --> Report[Generate Audit Report]
```

---

## 2. 20 Domain Benchmark Scenarios (Groups A to T)

### Scenario A: Core Engineering Workflow & Git Governance (Group A)

- **Trigger / Problem Statement:** Thiết lập chuẩn hóa quy trình phát triển, phân nhánh Git an toàn, atomic commit và quản lý layout codebase.
- **Execution Mode:** `STANDARD`
- **Mandatory Quality Gates:** `QG-01`, `QG-02`, `QG-03`, `QG-08`
- **Primary Skills:**
  - [`dex-development-workflow`](.agents/skills/dex-development-workflow/SKILL.md)
  - [`dex-git-workflow`](.agents/skills/dex-git-workflow/SKILL.md)
  - [`dex-code-organization`](.agents/skills/dex-code-organization/SKILL.md)
- **Complementary Skills:**
  - [`dex-repository-bootstrap`](.agents/skills/dex-repository-bootstrap/SKILL.md)
  - [`dex-semantic-version-automation`](.agents/skills/dex-semantic-version-automation/SKILL.md)

---

### Scenario B: Multi-Agent Architecture & Coordination (Group B)

- **Trigger / Problem Statement:** Thiết kế kiến trúc hệ thống multi-agent orchestration có khả năng phân quyền và giám sát agent con.
- **Execution Mode:** `STRICT`
- **Mandatory Quality Gates:** `QG-01`, `QG-02`, `QG-05`, `QG-09`, `QG-13`
- **Primary Skills:**
  - [`dex-multi-agent-orchestration`](.agents/skills/dex-multi-agent-orchestration/SKILL.md)
  - [`dex-software-architecture`](.agents/skills/dex-software-architecture/SKILL.md)
  - [`dex-agent-engineering`](.agents/skills/dex-agent-engineering/SKILL.md)
- **Complementary Skills:**
  - [`dex-tool-calling-contracts`](.agents/skills/dex-tool-calling-contracts/SKILL.md)
  - [`dex-concurrency-state`](.agents/skills/dex-concurrency-state/SKILL.md)

---

### Scenario C: Production Reliability & Progressive Rollouts (Group C)

- **Trigger / Problem Statement:** Phân tích tác động thay đổi blast radius, cấu hình feature flags động và thiết lập ngân sách lỗi SLO.
- **Execution Mode:** `STRICT`
- **Mandatory Quality Gates:** `QG-01`, `QG-03`, `QG-07`, `QG-10`
- **Primary Skills:**
  - [`dex-change-impact-analysis`](.agents/skills/dex-change-impact-analysis/SKILL.md)
  - [`dex-feature-flags`](.agents/skills/dex-feature-flags/SKILL.md)
  - [`dex-reliability-engineering`](.agents/skills/dex-reliability-engineering/SKILL.md)
- **Complementary Skills:**
  - [`dex-zero-downtime-rollouts`](.agents/skills/dex-zero-downtime-rollouts/SKILL.md)
  - [`dex-production-monitoring`](.agents/skills/dex-production-monitoring/SKILL.md)

---

### Scenario D: Frontend Performance & Core Web Vitals (Group D)

- **Trigger / Problem Statement:** Tối ưu hóa Core Web Vitals, loại bỏ layout shift, và tự động hóa kiểm thử visual regression.
- **Execution Mode:** `STANDARD`
- **Mandatory Quality Gates:** `QG-02`, `QG-04`, `QG-07`, `QG-14`
- **Primary Skills:**
  - [`dex-frontend-performance`](.agents/skills/dex-frontend-performance/SKILL.md)
  - [`dex-visual-regression`](.agents/skills/dex-visual-regression/SKILL.md)
  - [`dex-forms-and-validation`](.agents/skills/dex-forms-and-validation/SKILL.md)
- **Complementary Skills:**
  - [`dex-accessibility-automation`](.agents/skills/dex-accessibility-automation/SKILL.md)
  - [`dex-design-handoff-verification`](.agents/skills/dex-design-handoff-verification/SKILL.md)

---

### Scenario E: Event-Driven Backend & Distributed Processing (Group E)

- **Trigger / Problem Statement:** Xây dựng đường ống event-driven bất đồng bộ với consumer xử lý bình thản idempotent và worker hàng đợi.
- **Execution Mode:** `STRICT`
- **Mandatory Quality Gates:** `QG-02`, `QG-04`, `QG-09`, `QG-10`
- **Primary Skills:**
  - [`dex-event-driven-architecture`](.agents/skills/dex-event-driven-architecture/SKILL.md)
  - [`dex-idempotent-operations`](.agents/skills/dex-idempotent-operations/SKILL.md)
  - [`dex-background-job-queues`](.agents/skills/dex-background-job-queues/SKILL.md)
- **Complementary Skills:**
  - [`dex-api-engineering`](.agents/skills/dex-api-engineering/SKILL.md)
  - [`dex-distributed-consistency`](.agents/skills/dex-distributed-consistency/SKILL.md)

---

### Scenario F: Data Contracts & Storage Optimization (Group F)

- **Trigger / Problem Statement:** Thực thi tương thích schema giữa producer/consumer dữ liệu và tối ưu hóa kế hoạch thực thi câu lệnh SQL.
- **Execution Mode:** `STANDARD`
- **Mandatory Quality Gates:** `QG-02`, `QG-04`, `QG-08`
- **Primary Skills:**
  - [`dex-data-contracts`](.agents/skills/dex-data-contracts/SKILL.md)
  - [`dex-data-pipelines`](.agents/skills/dex-data-pipelines/SKILL.md)
  - [`dex-database-query-plans`](.agents/skills/dex-database-query-plans/SKILL.md)
- **Complementary Skills:**
  - [`dex-database-engineering`](.agents/skills/dex-database-engineering/SKILL.md)
  - [`dex-schema-evolution`](.agents/skills/dex-schema-evolution/SKILL.md)

---

### Scenario G: Enterprise RAG & Retrieval Quality Engineering (Group G)

- **Trigger / Problem Statement:** Triển khai tìm kiếm lai dense/sparse, reranking mô hình cross-encoder và kiểm soát chi phí token LLM.
- **Execution Mode:** `STANDARD`
- **Mandatory Quality Gates:** `QG-02`, `QG-04`, `QG-07`, `QG-13`
- **Primary Skills:**
  - [`dex-rag-pipelines`](.agents/skills/dex-rag-pipelines/SKILL.md)
  - [`dex-retrieval-evaluation`](.agents/skills/dex-retrieval-evaluation/SKILL.md)
  - [`dex-llm-cost-controls`](.agents/skills/dex-llm-cost-controls/SKILL.md)
- **Complementary Skills:**
  - [`dex-llm-integration`](.agents/skills/dex-llm-integration/SKILL.md)
  - [`dex-reranking-strategies`](.agents/skills/dex-reranking-strategies/SKILL.md)

---

### Scenario H: Governed Monorepo & Cross-Platform Tooling (Group H)

- **Trigger / Problem Statement:** Chuẩn hóa monorepo đa dự án, phát triển CLI hiệu năng cao và tự động hóa phát hành semantic release.
- **Execution Mode:** `STANDARD`
- **Mandatory Quality Gates:** `QG-01`, `QG-02`, `QG-03`, `QG-05`
- **Primary Skills:**
  - [`dex-monorepo-governance`](.agents/skills/dex-monorepo-governance/SKILL.md)
  - [`dex-cli-engineering`](.agents/skills/dex-cli-engineering/SKILL.md)
  - [`dex-semantic-version-automation`](.agents/skills/dex-semantic-version-automation/SKILL.md)
- **Complementary Skills:**
  - [`dex-developer-tooling`](.agents/skills/dex-developer-tooling/SKILL.md)
  - [`dex-cicd-automation`](.agents/skills/dex-cicd-automation/SKILL.md)

---

### Scenario I: Threat Modeling & Defensive Secrets Lifecycle (Group I)

- **Trigger / Problem Statement:** Mô hình hóa mối đe dọa STRIDE, thiết lập kiểm soát truy cập zero-trust và quản lý vòng đời secrets leases.
- **Execution Mode:** `STRICT`
- **Mandatory Quality Gates:** `QG-01`, `QG-06`, `QG-08`, `QG-11`
- **Primary Skills:**
  - [`dex-threat-modeling`](.agents/skills/dex-threat-modeling/SKILL.md)
  - [`dex-secrets-management`](.agents/skills/dex-secrets-management/SKILL.md)
  - [`dex-security-audit`](.agents/skills/dex-security-audit/SKILL.md)
- **Complementary Skills:**
  - [`dex-auth-session-lifecycle`](.agents/skills/dex-auth-session-lifecycle/SKILL.md)
  - [`dex-access-control-tenancy`](.agents/skills/dex-access-control-tenancy/SKILL.md)

---

### Scenario J: Cloud-Native Containers & Kubernetes Orchestration (Group J)

- **Trigger / Problem Statement:** Đóng gói container OCI tối giản an toàn và triển khai rolling update Kubernetes zero-downtime.
- **Execution Mode:** `STRICT`
- **Mandatory Quality Gates:** `QG-01`, `QG-06`, `QG-07`, `QG-11`
- **Primary Skills:**
  - [`dex-container-image-engineering`](.agents/skills/dex-container-image-engineering/SKILL.md)
  - [`dex-kubernetes-deployment`](.agents/skills/dex-kubernetes-deployment/SKILL.md)
  - [`dex-zero-downtime-rollouts`](.agents/skills/dex-zero-downtime-rollouts/SKILL.md)
- **Complementary Skills:**
  - [`dex-service-mesh-networking`](.agents/skills/dex-service-mesh-networking/SKILL.md)
  - [`dex-kubernetes-policy-enforcement`](.agents/skills/dex-kubernetes-policy-enforcement/SKILL.md)

---

### Scenario K: Mobile Offline Synchronization & Native Device Access (Group K)

- **Trigger / Problem Statement:** Kiến trúc engine đồng bộ offline-first trên di động giải quyết xung đột và tích hợp phần cứng sinh trắc.
- **Execution Mode:** `STANDARD`
- **Mandatory Quality Gates:** `QG-02`, `QG-04`, `QG-08`
- **Primary Skills:**
  - [`dex-android-app-architecture`](.agents/skills/dex-android-app-architecture/SKILL.md)
  - [`dex-mobile-offline-sync`](.agents/skills/dex-mobile-offline-sync/SKILL.md)
  - [`dex-native-device-integration`](.agents/skills/dex-native-device-integration/SKILL.md)
- **Complementary Skills:**
  - [`dex-ios-app-architecture`](.agents/skills/dex-ios-app-architecture/SKILL.md)
  - [`dex-mobile-performance-profiling`](.agents/skills/dex-mobile-performance-profiling/SKILL.md)

---

### Scenario L: Compliance Control Mapping & Operational Readiness (Group L)

- **Trigger / Problem Statement:** Ánh xạ kiểm soát tuân thủ SOC 2/ISO 27001 thành bằng chứng tự động và đánh giá mức độ sẵn sàng vận hành.
- **Execution Mode:** `STRICT`
- **Mandatory Quality Gates:** `QG-01`, `QG-06`, `QG-08`, `QG-14`
- **Primary Skills:**
  - [`dex-operational-readiness-review`](.agents/skills/dex-operational-readiness-review/SKILL.md)
  - [`dex-compliance-control-mapping`](.agents/skills/dex-compliance-control-mapping/SKILL.md)
  - [`dex-privacy-impact-assessment`](.agents/skills/dex-privacy-impact-assessment/SKILL.md)
- **Complementary Skills:**
  - [`dex-audit-trail-integrity`](.agents/skills/dex-audit-trail-integrity/SKILL.md)
  - [`dex-configuration-drift`](.agents/skills/dex-configuration-drift/SKILL.md)

---

### Scenario M: Advanced Verification & Mutation Testing (Group M)

- **Trigger / Problem Statement:** Đo lường độ hiệu quả test bằng phân tích đột biến mutation survival, cách ly flaky test và kiểm chứng bất biến.
- **Execution Mode:** `STRICT`
- **Mandatory Quality Gates:** `QG-02`, `QG-04`, `QG-09`
- **Primary Skills:**
  - [`dex-mutation-testing`](.agents/skills/dex-mutation-testing/SKILL.md)
  - [`dex-flaky-test-remediation`](.agents/skills/dex-flaky-test-remediation/SKILL.md)
  - [`dex-coverage-risk-analysis`](.agents/skills/dex-coverage-risk-analysis/SKILL.md)
- **Complementary Skills:**
  - [`dex-differential-testing`](.agents/skills/dex-differential-testing/SKILL.md)
  - [`dex-formal-invariant-checks`](.agents/skills/dex-formal-invariant-checks/SKILL.md)

---

### Scenario N: Distributed Systems Resilience & Traffic Shaping (Group N)

- **Trigger / Problem Statement:** Mô phỏng áp lực tải đỉnh điểm, thiết kế thuật toán giới hạn tốc độ token bucket và cắt giảm tải backpressure.
- **Execution Mode:** `STRICT`
- **Mandatory Quality Gates:** `QG-03`, `QG-07`, `QG-10`
- **Primary Skills:**
  - [`dex-load-and-stress-testing`](.agents/skills/dex-load-and-stress-testing/SKILL.md)
  - [`dex-rate-limiting-quotas`](.agents/skills/dex-rate-limiting-quotas/SKILL.md)
  - [`dex-traffic-shaping-backpressure`](.agents/skills/dex-traffic-shaping-backpressure/SKILL.md)
- **Complementary Skills:**
  - [`dex-service-failover`](.agents/skills/dex-service-failover/SKILL.md)
  - [`dex-distributed-consistency`](.agents/skills/dex-distributed-consistency/SKILL.md)

---

### Scenario O: Cloud Platform Governance & GitOps Workflows (Group O)

- **Trigger / Problem Statement:** Kiểm toán phân quyền IAM đám mây, quản lý danh mục dịch vụ nội bộ và đối soát trạng thái khai báo GitOps.
- **Execution Mode:** `STRICT`
- **Mandatory Quality Gates:** `QG-01`, `QG-06`, `QG-11`
- **Primary Skills:**
  - [`dex-cloud-iam-policy-review`](.agents/skills/dex-cloud-iam-policy-review/SKILL.md)
  - [`dex-gitops-workflows`](.agents/skills/dex-gitops-workflows/SKILL.md)
  - [`dex-kubernetes-policy-enforcement`](.agents/skills/dex-kubernetes-policy-enforcement/SKILL.md)
- **Complementary Skills:**
  - [`dex-platform-service-catalog`](.agents/skills/dex-platform-service-catalog/SKILL.md)
  - [`dex-cloud-resource-tagging`](.agents/skills/dex-cloud-resource-tagging/SKILL.md)

---

### Scenario P: Specialized Language & Systems Runtime Diagnostics (Group P)

- **Trigger / Problem Statement:** Kiểm toán khối Rust unsafe ngừa UB, phân tích tạm dừng GC JVM và chẩn đoán độ trễ event loop Node.js.
- **Execution Mode:** `STRICT`
- **Mandatory Quality Gates:** `QG-02`, `QG-05`, `QG-12`
- **Primary Skills:**
  - [`dex-rust-unsafe-audit`](.agents/skills/dex-rust-unsafe-audit/SKILL.md)
  - [`dex-cpp-memory-safety`](.agents/skills/dex-cpp-memory-safety/SKILL.md)
  - [`dex-nodejs-runtime-diagnostics`](.agents/skills/dex-nodejs-runtime-diagnostics/SKILL.md)
- **Complementary Skills:**
  - [`dex-go-concurrency-patterns`](.agents/skills/dex-go-concurrency-patterns/SKILL.md)
  - [`dex-jvm-performance-diagnostics`](.agents/skills/dex-jvm-performance-diagnostics/SKILL.md)

---

### Scenario Q: Advanced Multi-Agent MCP Protocols & Vector Indexing (Group Q)

- **Trigger / Problem Statement:** Xây dựng MCP Server chuẩn hóa, tối ưu hóa chỉ mục vector HNSW và thực thi schema JSON phản hồi nghiêm ngặt.
- **Execution Mode:** `STANDARD`
- **Mandatory Quality Gates:** `QG-02`, `QG-04`, `QG-13`
- **Primary Skills:**
  - [`dex-mcp-server-design`](.agents/skills/dex-mcp-server-design/SKILL.md)
  - [`dex-vector-index-design`](.agents/skills/dex-vector-index-design/SKILL.md)
  - [`dex-reranking-strategies`](.agents/skills/dex-reranking-strategies/SKILL.md)
- **Complementary Skills:**
  - [`dex-structured-llm-output`](.agents/skills/dex-structured-llm-output/SKILL.md)
  - [`dex-agent-memory-governance`](.agents/skills/dex-agent-memory-governance/SKILL.md)

---

### Scenario R: User Experience Journey Mapping & Accessibility (Group R)

- **Trigger / Problem Statement:** Vẽ bản đồ luồng mua hàng, tự động hóa kiểm định WCAG 2.2 AA và xác minh bàn giao design tokens.
- **Execution Mode:** `STANDARD`
- **Mandatory Quality Gates:** `QG-02`, `QG-08`, `QG-14`
- **Primary Skills:**
  - [`dex-user-journey-mapping`](.agents/skills/dex-user-journey-mapping/SKILL.md)
  - [`dex-accessibility-automation`](.agents/skills/dex-accessibility-automation/SKILL.md)
  - [`dex-design-handoff-verification`](.agents/skills/dex-design-handoff-verification/SKILL.md)
- **Complementary Skills:**
  - [`dex-product-requirements-writing`](.agents/skills/dex-product-requirements-writing/SKILL.md)
  - [`dex-usability-study-design`](.agents/skills/dex-usability-study-design/SKILL.md)

---

### Scenario S: Application Security Defense & Supply Chain Verification (Group S)

- **Trigger / Problem Statement:** Sàng lọc cảnh báo SAST, ký số và xác minh SBOM tiền phát hành, gia cố bảo mật CSP tiện ích mở rộng trình duyệt.
- **Execution Mode:** `STRICT`
- **Mandatory Quality Gates:** `QG-01`, `QG-06`, `QG-08`, `QG-11`
- **Primary Skills:**
  - [`dex-sast-finding-triage`](.agents/skills/dex-sast-finding-triage/SKILL.md)
  - [`dex-sbom-verification`](.agents/skills/dex-sbom-verification/SKILL.md)
  - [`dex-browser-extension-hardening`](.agents/skills/dex-browser-extension-hardening/SKILL.md)
- **Complementary Skills:**
  - [`dex-api-abuse-prevention`](.agents/skills/dex-api-abuse-prevention/SKILL.md)
  - [`dex-cryptographic-api-review`](.agents/skills/dex-cryptographic-api-review/SKILL.md)

---

### Scenario T: Autonomous SkillOps Lifecycle & Provenance Auditing (Group T)

- **Trigger / Problem Statement:** Chỉ mục hóa toàn bộ catalog kỹ năng, quét an ninh AST động, chấm điểm độ chính xác điều phối và quản lý nguồn gốc upstream.
- **Execution Mode:** `STRICT`
- **Mandatory Quality Gates:** `QG-01`, `QG-02`, `QG-08`, `QG-15`
- **Primary Skills:**
  - [`dex-skill-discovery-indexer`](.agents/skills/dex-skill-discovery-indexer/SKILL.md)
  - [`dex-skill-security-screening`](.agents/skills/dex-skill-security-screening/SKILL.md)
  - [`dex-skill-upstream-sync`](.agents/skills/dex-skill-upstream-sync/SKILL.md)
- **Complementary Skills:**
  - [`dex-skill-quality-benchmarking`](.agents/skills/dex-skill-quality-benchmarking/SKILL.md)
  - [`dex-skill-dependency-graph`](.agents/skills/dex-skill-dependency-graph/SKILL.md)

---

