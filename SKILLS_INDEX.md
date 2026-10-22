# DEX Skills Index & Quick Reference Catalog v4.0

Bảng tra cứu nhanh toàn diện cho toàn bộ **121 Kỹ năng (1 Master Orchestrator + 120 Kỹ năng Chuyên biệt)** thuộc **DEX Engineering Skills Pack v4.0.0**.

Tuân thủ nghiêm ngặt đặc tả [Agent Skills Specification](https://agentskills.io/specification) và chuẩn hóa đầy đủ 14 mục kỹ thuật bắt buộc.

---


## Master Orchestrator (00)


| STT | Tên Kỹ Năng (`name`) | Phân Nhóm | Trách Nhiệm Cốt Lõi | Cổng Chất Lượng Kiểm Soát |
|:---|:---|:---|:---|:---|
| **00** | [`dex-master-orchestrator`](.agents/skills/dex-master-orchestrator/SKILL.md) | **Master Control Plane** | Điều phối toàn bộ 120 specialized skills, phân loại độ phức tạp (QUICK, STANDARD, STRICT), kiểm soát 12 Quality Gates và xuất báo cáo kiểm chứng minh bạch. | QG-01 đến QG-12 |


---


## 120 Kỹ Năng Chuyên Biệt Theo 12 Phân Nhóm Chuyên Ngành (Groups A–L)


### GROUP A: Core Engineering (01–10)

| STT | Tên Kỹ Năng (`name`) | Trách Nhiệm Kỹ Thuật | Cổng Chất Lượng (Quality Gates) |
|:---|:---|:---|:---|
| **01** | [`dex-development-workflow`](.agents/skills/dex-development-workflow/SKILL.md) | Incremental development, task decomposition, and green-state loops. | QG-01, QG-02 |
| **02** | [`dex-task-delegation`](.agents/skills/dex-task-delegation/SKILL.md) | Scoped prompt engineering, task boundary definition, and context prep. | QG-01, QG-02 |
| **03** | [`dex-code-verification`](.agents/skills/dex-code-verification/SKILL.md) | Independent verification, test harness execution, and anti-hallucination. | QG-04, QG-10 |
| **04** | [`dex-git-workflow`](.agents/skills/dex-git-workflow/SKILL.md) | Atomic commits, branch isolation, and destructive command interception. | QG-02, QG-10 |
| **05** | [`dex-code-organization`](.agents/skills/dex-code-organization/SKILL.md) | Module boundaries, god-file elimination, and circular dependency removal. | QG-03 |
| **06** | [`dex-root-cause-debugging`](.agents/skills/dex-root-cause-debugging/SKILL.md) | Scientific debugging, reproduction test suites, and root-cause fix. | QG-04, QG-05 |
| **07** | [`dex-performance-optimization`](.agents/skills/dex-performance-optimization/SKILL.md) | Profiling flamegraphs, latency benchmarks, and memory leak triage. | QG-08 |
| **08** | [`dex-security-audit`](.agents/skills/dex-security-audit/SKILL.md) | OWASP Top 10 auditing, SAST, secret detection, and CVE remediation. | QG-09 |
| **09** | [`dex-cicd-automation`](.agents/skills/dex-cicd-automation/SKILL.md) | GitHub Actions workflows, build matrices, and branch protection gates. | QG-04, QG-10 |
| **10** | [`dex-release-engineering`](.agents/skills/dex-release-engineering/SKILL.md) | SemVer tagging, packaging artifacts, and changelog automation. | QG-06, QG-10 |


### GROUP B: Software Architecture & AI Agents (11–20)

| STT | Tên Kỹ Năng (`name`) | Trách Nhiệm Kỹ Thuật | Cổng Chất Lượng (Quality Gates) |
|:---|:---|:---|:---|
| **11** | [`dex-production-monitoring`](.agents/skills/dex-production-monitoring/SKILL.md) | Structured JSON logging, RED/USE metrics, and healthz probe endpoints. | QG-07, QG-10 |
| **12** | [`dex-technical-debt-refactoring`](.agents/skills/dex-technical-debt-refactoring/SKILL.md) | Code smell triage, legacy test harnesses, and safe AST transforms. | QG-03, QG-04 |
| **13** | [`dex-software-architecture`](.agents/skills/dex-software-architecture/SKILL.md) | Modular monolith design, unidirectional data flow, and ADR documentation. | QG-01, QG-06 |
| **14** | [`dex-database-engineering`](.agents/skills/dex-database-engineering/SKILL.md) | 3NF normalization, zero-downtime migrations, and query plan indexing. | QG-06, QG-08 |
| **15** | [`dex-api-engineering`](.agents/skills/dex-api-engineering/SKILL.md) | REST/GraphQL contracts, strict input validation, and backward compatibility. | QG-01, QG-06 |
| **16** | [`dex-testing-engineering`](.agents/skills/dex-testing-engineering/SKILL.md) | Testing pyramid (Unit/Integration/E2E), boundary analysis, and coverage. | QG-04 |
| **17** | [`dex-agent-engineering`](.agents/skills/dex-agent-engineering/SKILL.md) | Autonomous agent planning, system prompt governance, and guardrails. | QG-01, QG-02 |
| **18** | [`dex-multi-agent-orchestration`](.agents/skills/dex-multi-agent-orchestration/SKILL.md) | Parallel agent dispatch, domain boundary partitioning, and cross-review. | QG-02, QG-10 |
| **19** | [`dex-context-engineering`](.agents/skills/dex-context-engineering/SKILL.md) | Long-term memory management via AGENTS.md, TASKS.md, and pruning. | QG-01 |
| **20** | [`dex-specification-driven`](.agents/skills/dex-specification-driven/SKILL.md) | Specification-driven development (SDD) and Given-When-Then criteria. | QG-01, QG-04 |


### GROUP C: Production Engineering (21–30)

| STT | Tên Kỹ Năng (`name`) | Trách Nhiệm Kỹ Thuật | Cổng Chất Lượng (Quality Gates) |
|:---|:---|:---|:---|
| **21** | [`dex-change-impact-analysis`](.agents/skills/dex-change-impact-analysis/SKILL.md) | Blast radius calculation, dependency mapping, and risk triage. | QG-02, QG-06 |
| **22** | [`dex-dependency-management`](.agents/skills/dex-dependency-management/SKILL.md) | Lockfile pinning, reproducible environments, and vulnerability scanning. | QG-03, QG-09 |
| **23** | [`dex-reliability-engineering`](.agents/skills/dex-reliability-engineering/SKILL.md) | Strict timeouts, exponential backoff retry, circuit breakers, and fallback. | QG-07 |
| **24** | [`dex-concurrency-state`](.agents/skills/dex-concurrency-state/SKILL.md) | Race condition triage, mutex locking, and atomic state transitions. | QG-07 |
| **25** | [`dex-ux-accessibility`](.agents/skills/dex-ux-accessibility/SKILL.md) | WCAG 2.1 AA compliance, keyboard navigation, and responsive states. | QG-03, QG-10 |
| **26** | [`dex-feature-flags`](.agents/skills/dex-feature-flags/SKILL.md) | Canary deployment, percentage rollouts, and emergency kill-switches. | QG-07, QG-10 |
| **27** | [`dex-code-review`](.agents/skills/dex-code-review/SKILL.md) | Line-by-line diff review, blocker/nitpick classification, and PR quality. | QG-03, QG-09 |
| **28** | [`dex-acceptance-testing`](.agents/skills/dex-acceptance-testing/SKILL.md) | User Acceptance Testing (UAT), business scenario checks, and sign-off. | QG-04, QG-10 |
| **29** | [`dex-software-maintenance`](.agents/skills/dex-software-maintenance/SKILL.md) | Software lifecycle maintenance, technical debt roadmap, and runtime EOL. | QG-03, QG-10 |
| **30** | [`dex-end-to-end-engineering`](.agents/skills/dex-end-to-end-engineering/SKILL.md) | Full-lifecycle engineering orchestrating spec to release and maintenance. | QG-01 to QG-10 |


### GROUP D: Frontend Engineering (31–40)

| STT | Tên Kỹ Năng (`name`) | Trách Nhiệm Kỹ Thuật | Cổng Chất Lượng (Quality Gates) |
|:---|:---|:---|:---|
| **31** | [`dex-ui-component-contracts`](.agents/skills/dex-ui-component-contracts/SKILL.md) | Strict TypeScript prop contracts, slots, and component encapsulation. | QG-01, QG-03 |
| **32** | [`dex-design-system-tokens`](.agents/skills/dex-design-system-tokens/SKILL.md) | W3C design tokens, CSS variables, dark/light modes, and spacing scales. | QG-03 |
| **33** | [`dex-frontend-data-flow`](.agents/skills/dex-frontend-data-flow/SKILL.md) | Predictable global/local state, unidirectional flow, and normalization. | QG-03, QG-07 |
| **34** | [`dex-forms-and-validation`](.agents/skills/dex-forms-and-validation/SKILL.md) | Controlled/uncontrolled forms, Zod/Yup schemas, and accessible errors. | QG-01, QG-09 |
| **35** | [`dex-routing-navigation`](.agents/skills/dex-routing-navigation/SKILL.md) | Client/server route guards, lazy loading, and history management. | QG-01, QG-07 |
| **36** | [`dex-frontend-performance`](.agents/skills/dex-frontend-performance/SKILL.md) | Core Web Vitals (LCP, INP, CLS), bundle splitting, and virtual lists. | QG-08 |
| **37** | [`dex-ssr-seo-rendering`](.agents/skills/dex-ssr-seo-rendering/SKILL.md) | Server-Side Rendering (SSR/SSG), OpenGraph tags, and hydration recovery. | QG-01, QG-08 |
| **38** | [`dex-internationalization`](.agents/skills/dex-internationalization/SKILL.md) | i18n translation catalogs, pluralization, RTL layout, and date/currency. | QG-01, QG-03 |
| **39** | [`dex-visual-regression`](.agents/skills/dex-visual-regression/SKILL.md) | Automated pixel diffing, snapshot baselines, and cross-browser visual CI. | QG-04, QG-10 |
| **40** | [`dex-browser-compatibility`](.agents/skills/dex-browser-compatibility/SKILL.md) | Autoprefixer, polyfills, graceful degradation, and mobile Safari fixes. | QG-04, QG-07 |


### GROUP E: Backend & Integration (41–50)

| STT | Tên Kỹ Năng (`name`) | Trách Nhiệm Kỹ Thuật | Cổng Chất Lượng (Quality Gates) |
|:---|:---|:---|:---|
| **41** | [`dex-domain-driven-design`](.agents/skills/dex-domain-driven-design/SKILL.md) | Aggregates, Value Objects, Domain Events, and Clean Architecture. | QG-01, QG-03 |
| **42** | [`dex-background-job-queues`](.agents/skills/dex-background-job-queues/SKILL.md) | Async workers (BullMQ, Celery), retry backoff, and Dead Letter Queues. | QG-07, QG-08 |
| **43** | [`dex-caching-strategies`](.agents/skills/dex-caching-strategies/SKILL.md) | Cache-aside, write-through, TTL invalidation, and Redis caching. | QG-07, QG-08 |
| **44** | [`dex-realtime-protocols`](.agents/skills/dex-realtime-protocols/SKILL.md) | WebSockets, Server-Sent Events (SSE), heartbeat, and reconnection. | QG-07 |
| **45** | [`dex-file-processing`](.agents/skills/dex-file-processing/SKILL.md) | Streaming I/O, multipart uploads, virus scanning, and chunked storage. | QG-08, QG-09 |
| **46** | [`dex-search-engineering`](.agents/skills/dex-search-engineering/SKILL.md) | Full-text indexing, fuzzy search, BM25, and Elasticsearch integration. | QG-06, QG-08 |
| **47** | [`dex-event-driven-architecture`](.agents/skills/dex-event-driven-architecture/SKILL.md) | Publish-subscribe (Kafka/RabbitMQ), schema registries, and outbox pattern. | QG-06, QG-07 |
| **48** | [`dex-idempotent-operations`](.agents/skills/dex-idempotent-operations/SKILL.md) | Idempotency keys, distributed locks, deduplication, and safe retries. | QG-06, QG-07 |
| **49** | [`dex-notification-delivery`](.agents/skills/dex-notification-delivery/SKILL.md) | Multi-channel alerts (Email, SMS, Push, Slack), rate limits, and templates. | QG-07, QG-10 |
| **50** | [`dex-scheduled-workflows`](.agents/skills/dex-scheduled-workflows/SKILL.md) | Distributed cron orchestration, missed execution handling, and stateful DAGs. | QG-07, QG-10 |


### GROUP F: Data Engineering (51–60)

| STT | Tên Kỹ Năng (`name`) | Trách Nhiệm Kỹ Thuật | Cổng Chất Lượng (Quality Gates) |
|:---|:---|:---|:---|
| **51** | [`dex-data-contracts`](.agents/skills/dex-data-contracts/SKILL.md) | Data producer/consumer contracts, breaking change detection, and SLAs. | QG-01, QG-06 |
| **52** | [`dex-data-pipelines`](.agents/skills/dex-data-pipelines/SKILL.md) | Batch ETL/ELT pipelines, streaming DAGs (Airflow/Dagster), and dbt models. | QG-04, QG-05 |
| **53** | [`dex-data-quality-audits`](.agents/skills/dex-data-quality-audits/SKILL.md) | Great Expectations suites, statistical distribution checks, and null audits. | QG-03, QG-10 |
| **54** | [`dex-data-lineage`](.agents/skills/dex-data-lineage/SKILL.md) | OpenLineage tracking, column-level provenance, and upstream impact graphs. | QG-01, QG-06 |
| **55** | [`dex-schema-evolution`](.agents/skills/dex-schema-evolution/SKILL.md) | Additive migrations, deprecation policies, and expand-contract patterns. | QG-06 |
| **56** | [`dex-database-query-plans`](.agents/skills/dex-database-query-plans/SKILL.md) | EXPLAIN ANALYZE, index scan tuning, locking inspection, and pg_stat. | QG-08 |
| **57** | [`dex-storage-lifecycle`](.agents/skills/dex-storage-lifecycle/SKILL.md) | S3/GCS tiering, Coldline archival, multipart compaction, and cost control. | QG-08, QG-10 |
| **58** | [`dex-data-retention`](.agents/skills/dex-data-retention/SKILL.md) | GDPR 'right to be forgotten', automated purging, soft-delete, and legal holds. | QG-09, QG-10 |
| **59** | [`dex-capacity-planning`](.agents/skills/dex-capacity-planning/SKILL.md) | Load projection modeling, database read-replica scaling, and resource limits. | QG-08 |
| **60** | [`dex-disaster-recovery`](.agents/skills/dex-disaster-recovery/SKILL.md) | RTO/RPO targets, automated backups, cross-region replication, and failover. | QG-07, QG-10 |


### GROUP G: AI & LLM Engineering (61–70)

| STT | Tên Kỹ Năng (`name`) | Trách Nhiệm Kỹ Thuật | Cổng Chất Lượng (Quality Gates) |
|:---|:---|:---|:---|
| **61** | [`dex-llm-integration`](.agents/skills/dex-llm-integration/SKILL.md) | Multi-provider SDKs, structured JSON outputs, streaming, and token limits. | QG-01, QG-07 |
| **62** | [`dex-rag-pipelines`](.agents/skills/dex-rag-pipelines/SKILL.md) | Chunking strategies, dense/sparse embeddings, and vector DB indexing. | QG-04, QG-08 |
| **63** | [`dex-retrieval-evaluation`](.agents/skills/dex-retrieval-evaluation/SKILL.md) | RAGAS metrics, Hit Rate@K, MRR, NDCG, and semantic faithfulness. | QG-04, QG-10 |
| **64** | [`dex-prompt-evaluation`](.agents/skills/dex-prompt-evaluation/SKILL.md) | Few-shot optimization, regression prompt suites, and prompt versioning. | QG-04, QG-05 |
| **65** | [`dex-model-evaluation`](.agents/skills/dex-model-evaluation/SKILL.md) | Benchmarking accuracy, latency, cost per 1M tokens, and task routing. | QG-04, QG-08 |
| **66** | [`dex-tool-calling-contracts`](.agents/skills/dex-tool-calling-contracts/SKILL.md) | JSON Schema tool definitions, error correction loops, and schema validation. | QG-01, QG-03 |
| **67** | [`dex-agent-permissions`](.agents/skills/dex-agent-permissions/SKILL.md) | Human-in-the-loop gates, blast radius controls, and shell execution guards. | QG-09, QG-10 |
| **68** | [`dex-llm-cost-controls`](.agents/skills/dex-llm-cost-controls/SKILL.md) | Token budgets, semantic caching, model downgrading, and cost alerts. | QG-08, QG-10 |
| **69** | [`dex-ai-observability`](.agents/skills/dex-ai-observability/SKILL.md) | OpenTelemetry traces, token attribution, latency percentiles, and spans. | QG-07, QG-10 |
| **70** | [`dex-dataset-curation`](.agents/skills/dex-dataset-curation/SKILL.md) | Instruction dataset generation, PII sanitization, and JSONL validation. | QG-03, QG-09 |


### GROUP H: Developer Experience (71–80)

| STT | Tên Kỹ Năng (`name`) | Trách Nhiệm Kỹ Thuật | Cổng Chất Lượng (Quality Gates) |
|:---|:---|:---|:---|
| **71** | [`dex-repository-bootstrap`](.agents/skills/dex-repository-bootstrap/SKILL.md) | Zero-to-code project scaffolding, linters, pre-commit, and CI templates. | QG-01, QG-03 |
| **72** | [`dex-monorepo-governance`](.agents/skills/dex-monorepo-governance/SKILL.md) | Turborepo/Nx pipelines, package boundaries, and remote task caching. | QG-04, QG-08 |
| **73** | [`dex-cli-engineering`](.agents/skills/dex-cli-engineering/SKILL.md) | POSIX argument parsing, interactive terminal UI, JSON mode, and exit codes. | QG-01, QG-07 |
| **74** | [`dex-plugin-architecture`](.agents/skills/dex-plugin-architecture/SKILL.md) | Microkernel pattern, extension lifecycle hooks, manifests, and sandboxes. | QG-03, QG-07 |
| **75** | [`dex-cross-platform-portability`](.agents/skills/dex-cross-platform-portability/SKILL.md) | Windows/Linux/macOS pathing, CRLF/LF line endings, and matrix builds. | QG-01, QG-04 |
| **76** | [`dex-windows-packaging`](.agents/skills/dex-windows-packaging/SKILL.md) | InnoSetup, MSIX, WinGet manifest publication, and Authenticode signing. | QG-01, QG-09 |
| **77** | [`dex-documentation-as-code`](.agents/skills/dex-documentation-as-code/SKILL.md) | Architecture Decision Records (ADR), doctests, and Mermaid diagrams. | QG-01, QG-05 |
| **78** | [`dex-code-generation`](.agents/skills/dex-code-generation/SKILL.md) | Deterministic AST codegen, scaffolding engines (Plop), and SDK generators. | QG-01, QG-06 |
| **79** | [`dex-developer-tooling`](.agents/skills/dex-developer-tooling/SKILL.md) | Devcontainers, Mise/Nix environments, Lefthook, and VS Code debug configs. | QG-01, QG-08 |
| **80** | [`dex-semantic-version-automation`](.agents/skills/dex-semantic-version-automation/SKILL.md) | SemVer 2.0, Conventional Commits parsing, and automated GitHub releases. | QG-01, QG-10 |


### GROUP I: Security & Reliability (81–90)

| STT | Tên Kỹ Năng (`name`) | Trách Nhiệm Kỹ Thuật | Cổng Chất Lượng (Quality Gates) |
|:---|:---|:---|:---|
| **81** | [`dex-auth-session-lifecycle`](.agents/skills/dex-auth-session-lifecycle/SKILL.md) | JWT issuance, refresh token rotation, session revocation, and HttpOnly cookies. | QG-03, QG-09 |
| **82** | [`dex-access-control-tenancy`](.agents/skills/dex-access-control-tenancy/SKILL.md) | RBAC/ABAC authorization, tenant scoping, and PostgreSQL Row-Level Security. | QG-03, QG-09 |
| **83** | [`dex-secrets-management`](.agents/skills/dex-secrets-management/SKILL.md) | Vault/AWS Secrets Manager injection, zero hardcoded credentials, and scanning. | QG-03, QG-09 |
| **84** | [`dex-supply-chain-security`](.agents/skills/dex-supply-chain-security/SKILL.md) | CycloneDX SBOM generation, dependency lockfile audits, and container Trivy. | QG-03, QG-10 |
| **85** | [`dex-threat-modeling`](.agents/skills/dex-threat-modeling/SKILL.md) | Structured STRIDE analysis, attack surface mapping, and abuse cases. | QG-01, QG-09 |
| **86** | [`dex-property-based-testing`](.agents/skills/dex-property-based-testing/SKILL.md) | Hypothesis/fast-check invariants, generative fuzzing, and case shrinking. | QG-01, QG-05 |
| **87** | [`dex-chaos-experiments`](.agents/skills/dex-chaos-experiments/SKILL.md) | Fault injection, network latency simulation (Toxiproxy), and circuit breakers. | QG-04, QG-08 |
| **88** | [`dex-experimentation-metrics`](.agents/skills/dex-experimentation-metrics/SKILL.md) | Feature flags, A/B testing infrastructure, statistical p-value, and telemetry. | QG-01, QG-08 |
| **89** | [`dex-api-contract-evolution`](.agents/skills/dex-api-contract-evolution/SKILL.md) | Backward compatibility diffing, RFC 8594 Sunset headers, and adapters. | QG-06, QG-10 |
| **90** | [`dex-incident-postmortems`](.agents/skills/dex-incident-postmortems/SKILL.md) | Blameless postmortems, chronological timeline, 5 Whys, and action items. | QG-01, QG-10 |


### GROUP J: Cloud & Infrastructure (91–100)

| STT | Tên Kỹ Năng (`name`) | Trách Nhiệm Kỹ Thuật | Cổng Chất Lượng (Quality Gates) |
|:---|:---|:---|:---|
| **91** | [`dex-container-image-engineering`](.agents/skills/dex-container-image-engineering/SKILL.md) | Multi-stage builds, minimal base images, non-root users, SBOM, and Trivy. | QG-01, QG-07 |
| **92** | [`dex-kubernetes-deployment`](.agents/skills/dex-kubernetes-deployment/SKILL.md) | Deployments, probes, resource limits, PodDisruptionBudgets, and rolling updates. | QG-01, QG-05 |
| **93** | [`dex-infrastructure-as-code`](.agents/skills/dex-infrastructure-as-code/SKILL.md) | Terraform/OpenTofu, remote state locking, drift detection, and Checkov scan. | QG-01, QG-07 |
| **94** | [`dex-cloud-service-integration`](.agents/skills/dex-cloud-service-integration/SKILL.md) | Workload Identity, exponential backoff with jitter, and least privilege IAM. | QG-03, QG-07 |
| **95** | [`dex-zero-downtime-rollouts`](.agents/skills/dex-zero-downtime-rollouts/SKILL.md) | Blue-green, Argo canary, progressive traffic shifting, and instant rollback. | QG-01, QG-09 |
| **96** | [`dex-service-mesh-networking`](.agents/skills/dex-service-mesh-networking/SKILL.md) | Istio/Linkerd mTLS, traffic routing, circuit breaking, and Envoy outlier detection. | QG-01, QG-07 |
| **97** | [`dex-network-troubleshooting`](.agents/skills/dex-network-troubleshooting/SKILL.md) | DNS, TLS cert chains, TCP SYN/RST, HTTP latency, and tcpdump packet analysis. | QG-01, QG-06 |
| **98** | [`dex-slo-error-budgets`](.agents/skills/dex-slo-error-budgets/SKILL.md) | SLIs, SLOs, rolling error budgets, multi-window burn rate alerts, and freeze rules. | QG-01, QG-08 |
| **99** | [`dex-distributed-tracing`](.agents/skills/dex-distributed-tracing/SKILL.md) | OpenTelemetry, W3C tracecontext propagation, span lifecycle, and latency bottlenecks. | QG-01, QG-07 |
| **100** | [`dex-cloud-cost-finops`](.agents/skills/dex-cloud-cost-finops/SKILL.md) | Cloud cost allocation tags, right-sizing, idle asset cleanup, and unit economics. | QG-01, QG-08 |


### GROUP K: Mobile & Desktop Engineering (101–110)

| STT | Tên Kỹ Năng (`name`) | Trách Nhiệm Kỹ Thuật | Cổng Chất Lượng (Quality Gates) |
|:---|:---|:---|:---|
| **101** | [`dex-android-app-architecture`](.agents/skills/dex-android-app-architecture/SKILL.md) | Jetpack Compose, MVVM/MVI, StateFlow, Room database, and Hilt DI. | QG-01, QG-07 |
| **102** | [`dex-ios-app-architecture`](.agents/skills/dex-ios-app-architecture/SKILL.md) | SwiftUI, Swift Concurrency, NavigationStack, Observation, and SwiftData. | QG-01, QG-07 |
| **103** | [`dex-electron-security`](.agents/skills/dex-electron-security/SKILL.md) | contextIsolation, nodeIntegration disabled, sandbox, minimal contextBridge, and CSP. | QG-01, QG-07 |
| **104** | [`dex-tauri-desktop-integration`](.agents/skills/dex-tauri-desktop-integration/SKILL.md) | Tauri v2, Rust backend commands, strict capabilities, and minimal memory footprint. | QG-01, QG-07 |
| **105** | [`dex-mobile-offline-sync`](.agents/skills/dex-mobile-offline-sync/SKILL.md) | Offline-first SQLite/WatermelonDB, mutation sync queues, CRDT/LWW, and workers. | QG-01, QG-08 |
| **106** | [`dex-mobile-release-pipelines`](.agents/skills/dex-mobile-release-pipelines/SKILL.md) | Fastlane automation, keystore signing, Match provisioning, and store uploads. | QG-01, QG-07 |
| **107** | [`dex-mobile-performance-profiling`](.agents/skills/dex-mobile-performance-profiling/SKILL.md) | Startup time (TTID/TTFD), frame jank (60/120 fps), LeakCanary, and battery. | QG-01, QG-08 |
| **108** | [`dex-desktop-ipc-design`](.agents/skills/dex-desktop-ipc-design/SKILL.md) | Type-safe IPC schemas (Zod/JSON Schema), bi-directional events, and validation. | QG-01, QG-07 |
| **109** | [`dex-native-device-integration`](.agents/skills/dex-native-device-integration/SKILL.md) | Camera, Geolocation, Bluetooth BLE, Biometrics, and graceful hardware fallbacks. | QG-01, QG-07 |
| **110** | [`dex-desktop-update-delivery`](.agents/skills/dex-desktop-update-delivery/SKILL.md) | Auto-updates, cryptographic signatures (Minisign/Ed25519), and atomic rollbacks. | QG-01, QG-07 |


### GROUP L: Product & Operations Engineering (111–120)

| STT | Tên Kỹ Năng (`name`) | Trách Nhiệm Kỹ Thuật | Cổng Chất Lượng (Quality Gates) |
|:---|:---|:---|:---|
| **111** | [`dex-privacy-impact-assessment`](.agents/skills/dex-privacy-impact-assessment/SKILL.md) | GDPR/CCPA DPIA, personal data classification, minimization, and user rights. | QG-01, QG-07 |
| **112** | [`dex-compliance-control-mapping`](.agents/skills/dex-compliance-control-mapping/SKILL.md) | SOC 2 Type II, ISO 27001, HIPAA control mapping, and automated evidence collection. | QG-01, QG-08 |
| **113** | [`dex-audit-trail-integrity`](.agents/skills/dex-audit-trail-integrity/SKILL.md) | Tamper-evident hash chaining, S3 Object Lock (WORM), and CloudEvents schema. | QG-01, QG-07 |
| **114** | [`dex-configuration-drift`](.agents/skills/dex-configuration-drift/SKILL.md) | ArgoCD/Flux GitOps reconciliation, Terraform drift, and automated self-healing. | QG-01, QG-08 |
| **115** | [`dex-product-discovery`](.agents/skills/dex-product-discovery/SKILL.md) | Jobs-to-be-Done (JTBD), Opportunity Solution Trees, and assumption spike testing. | QG-01, QG-02 |
| **116** | [`dex-feature-prioritization`](.agents/skills/dex-feature-prioritization/SKILL.md) | RICE scoring, Value vs Effort matrix, WSJF, and dependency graph resolution. | QG-01, QG-04 |
| **117** | [`dex-analytics-instrumentation`](.agents/skills/dex-analytics-instrumentation/SKILL.md) | Strict tracking plans, object_action taxonomy, Zod schemas, and PII scrubbing. | QG-01, QG-07 |
| **118** | [`dex-feedback-triage`](.agents/skills/dex-feedback-triage/SKILL.md) | High-velocity bug/feedback classification, deduplication, and reproduction recipes. | QG-01, QG-08 |
| **119** | [`dex-runbook-automation`](.agents/skills/dex-runbook-automation/SKILL.md) | Guarded executable runbooks (SOPs), interactive approval gates, and rollbacks. | QG-01, QG-09 |
| **120** | [`dex-operational-readiness-review`](.agents/skills/dex-operational-readiness-review/SKILL.md) | Production launch readiness review across reliability, security, support, and DR. | QG-01, QG-09 |


---


## Segregated Upstream Integration Modules (`integrations/`)


Các kỹ năng mở rộng được nhập khẩu từ nguồn bên ngoài và lưu trữ độc lập trong thư mục `integrations/`, không tính gộp vào danh mục 120 kỹ năng bản địa:


| Module | Nguồn Gốc | Đường Dẫn | Trách Nhiệm |

|:---|:---|:---|:---|

| **API Mocking & Virtualization** | Source A: Agentic Awesome Skills | [`integrations/aas/dex-api-mocking-virtualization`](integrations/aas/dex-api-mocking-virtualization/SKILL.md) | Hermetic offline API mocking, WireMock, Mock Service Worker (MSW). |

| **Defensive Binary Inspection** | Source B: Reverse Skill | [`integrations/reverse-skill/dex-binary-inspection`](integrations/reverse-skill/dex-binary-inspection/SKILL.md) | Static PE/ELF header analysis, ASLR/DEP flags, and library dependencies. |

| **JavaScript Bundle Deobfuscation** | Source B: Reverse Skill | [`integrations/reverse-skill/dex-javascript-bundle-deobfuscation`](integrations/reverse-skill/dex-javascript-bundle-deobfuscation/SKILL.md) | Sourcemap reconstruction and web/Electron bundle security auditing. |

| **REA MCP Adapter** | Source C: Reverse Engineer Anything | [`integrations/rea/dex-rea-adapter`](integrations/rea/dex-rea-adapter/SKILL.md) | Standardized MCP adapter bridge to local REA reverse engineering engine. |
