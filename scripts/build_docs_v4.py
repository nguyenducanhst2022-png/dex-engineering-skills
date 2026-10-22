# -*- coding: utf-8 -*-
"""
Documentation Generator for DEX Engineering Skills Pack v4.0.
Generates and updates:
- SKILLS_INDEX.md (120 Specialized Skills + 1 Master Orchestrator + Segregated Integrations)
- ROUTING_MATRIX.md (16 Real-World End-to-End Scenarios across all 12 groups)
- ARCHITECTURE.md (Technical Architecture, 12 Domain Groups, Control Plane & Integrations)
- INSTALL.md (Installation, Setup, and Codex instructions)
- CHANGELOG.md (Release notes for v4.0.0)
"""

import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

SKILL_GROUPS_V4 = [
    {
        "group_id": "GROUP A",
        "group_name": "Core Engineering (01–10)",
        "skills": [
            ("01", "dex-development-workflow", "Incremental development, task decomposition, and green-state loops.", "QG-01, QG-02"),
            ("02", "dex-task-delegation", "Scoped prompt engineering, task boundary definition, and context prep.", "QG-01, QG-02"),
            ("03", "dex-code-verification", "Independent verification, test harness execution, and anti-hallucination.", "QG-04, QG-10"),
            ("04", "dex-git-workflow", "Atomic commits, branch isolation, and destructive command interception.", "QG-02, QG-10"),
            ("05", "dex-code-organization", "Module boundaries, god-file elimination, and circular dependency removal.", "QG-03"),
            ("06", "dex-root-cause-debugging", "Scientific debugging, reproduction test suites, and root-cause fix.", "QG-04, QG-05"),
            ("07", "dex-performance-optimization", "Profiling flamegraphs, latency benchmarks, and memory leak triage.", "QG-08"),
            ("08", "dex-security-audit", "OWASP Top 10 auditing, SAST, secret detection, and CVE remediation.", "QG-09"),
            ("09", "dex-cicd-automation", "GitHub Actions workflows, build matrices, and branch protection gates.", "QG-04, QG-10"),
            ("10", "dex-release-engineering", "SemVer tagging, packaging artifacts, and changelog automation.", "QG-06, QG-10"),
        ]
    },
    {
        "group_id": "GROUP B",
        "group_name": "Software Architecture & AI Agents (11–20)",
        "skills": [
            ("11", "dex-production-monitoring", "Structured JSON logging, RED/USE metrics, and healthz probe endpoints.", "QG-07, QG-10"),
            ("12", "dex-technical-debt-refactoring", "Code smell triage, legacy test harnesses, and safe AST transforms.", "QG-03, QG-04"),
            ("13", "dex-software-architecture", "Modular monolith design, unidirectional data flow, and ADR documentation.", "QG-01, QG-06"),
            ("14", "dex-database-engineering", "3NF normalization, zero-downtime migrations, and query plan indexing.", "QG-06, QG-08"),
            ("15", "dex-api-engineering", "REST/GraphQL contracts, strict input validation, and backward compatibility.", "QG-01, QG-06"),
            ("16", "dex-testing-engineering", "Testing pyramid (Unit/Integration/E2E), boundary analysis, and coverage.", "QG-04"),
            ("17", "dex-agent-engineering", "Autonomous agent planning, system prompt governance, and guardrails.", "QG-01, QG-02"),
            ("18", "dex-multi-agent-orchestration", "Parallel agent dispatch, domain boundary partitioning, and cross-review.", "QG-02, QG-10"),
            ("19", "dex-context-engineering", "Long-term memory management via AGENTS.md, TASKS.md, and pruning.", "QG-01"),
            ("20", "dex-specification-driven", "Specification-driven development (SDD) and Given-When-Then criteria.", "QG-01, QG-04"),
        ]
    },
    {
        "group_id": "GROUP C",
        "group_name": "Production Engineering (21–30)",
        "skills": [
            ("21", "dex-change-impact-analysis", "Blast radius calculation, dependency mapping, and risk triage.", "QG-02, QG-06"),
            ("22", "dex-dependency-management", "Lockfile pinning, reproducible environments, and vulnerability scanning.", "QG-03, QG-09"),
            ("23", "dex-reliability-engineering", "Strict timeouts, exponential backoff retry, circuit breakers, and fallback.", "QG-07"),
            ("24", "dex-concurrency-state", "Race condition triage, mutex locking, and atomic state transitions.", "QG-07"),
            ("25", "dex-ux-accessibility", "WCAG 2.1 AA compliance, keyboard navigation, and responsive states.", "QG-03, QG-10"),
            ("26", "dex-feature-flags", "Canary deployment, percentage rollouts, and emergency kill-switches.", "QG-07, QG-10"),
            ("27", "dex-code-review", "Line-by-line diff review, blocker/nitpick classification, and PR quality.", "QG-03, QG-09"),
            ("28", "dex-acceptance-testing", "User Acceptance Testing (UAT), business scenario checks, and sign-off.", "QG-04, QG-10"),
            ("29", "dex-software-maintenance", "Software lifecycle maintenance, technical debt roadmap, and runtime EOL.", "QG-03, QG-10"),
            ("30", "dex-end-to-end-engineering", "Full-lifecycle engineering orchestrating spec to release and maintenance.", "QG-01 to QG-10"),
        ]
    },
    {
        "group_id": "GROUP D",
        "group_name": "Frontend Engineering (31–40)",
        "skills": [
            ("31", "dex-ui-component-contracts", "Strict TypeScript prop contracts, slots, and component encapsulation.", "QG-01, QG-03"),
            ("32", "dex-design-system-tokens", "W3C design tokens, CSS variables, dark/light modes, and spacing scales.", "QG-03"),
            ("33", "dex-frontend-data-flow", "Predictable global/local state, unidirectional flow, and normalization.", "QG-03, QG-07"),
            ("34", "dex-forms-and-validation", "Controlled/uncontrolled forms, Zod/Yup schemas, and accessible errors.", "QG-01, QG-09"),
            ("35", "dex-routing-navigation", "Client/server route guards, lazy loading, and history management.", "QG-01, QG-07"),
            ("36", "dex-frontend-performance", "Core Web Vitals (LCP, INP, CLS), bundle splitting, and virtual lists.", "QG-08"),
            ("37", "dex-ssr-seo-rendering", "Server-Side Rendering (SSR/SSG), OpenGraph tags, and hydration recovery.", "QG-01, QG-08"),
            ("38", "dex-internationalization", "i18n translation catalogs, pluralization, RTL layout, and date/currency.", "QG-01, QG-03"),
            ("39", "dex-visual-regression", "Automated pixel diffing, snapshot baselines, and cross-browser visual CI.", "QG-04, QG-10"),
            ("40", "dex-browser-compatibility", "Autoprefixer, polyfills, graceful degradation, and mobile Safari fixes.", "QG-04, QG-07"),
        ]
    },
    {
        "group_id": "GROUP E",
        "group_name": "Backend & Integration (41–50)",
        "skills": [
            ("41", "dex-domain-driven-design", "Aggregates, Value Objects, Domain Events, and Clean Architecture.", "QG-01, QG-03"),
            ("42", "dex-background-job-queues", "Async workers (BullMQ, Celery), retry backoff, and Dead Letter Queues.", "QG-07, QG-08"),
            ("43", "dex-caching-strategies", "Cache-aside, write-through, TTL invalidation, and Redis caching.", "QG-07, QG-08"),
            ("44", "dex-realtime-protocols", "WebSockets, Server-Sent Events (SSE), heartbeat, and reconnection.", "QG-07"),
            ("45", "dex-file-processing", "Streaming I/O, multipart uploads, virus scanning, and chunked storage.", "QG-08, QG-09"),
            ("46", "dex-search-engineering", "Full-text indexing, fuzzy search, BM25, and Elasticsearch integration.", "QG-06, QG-08"),
            ("47", "dex-event-driven-architecture", "Publish-subscribe (Kafka/RabbitMQ), schema registries, and outbox pattern.", "QG-06, QG-07"),
            ("48", "dex-idempotent-operations", "Idempotency keys, distributed locks, deduplication, and safe retries.", "QG-06, QG-07"),
            ("49", "dex-notification-delivery", "Multi-channel alerts (Email, SMS, Push, Slack), rate limits, and templates.", "QG-07, QG-10"),
            ("50", "dex-scheduled-workflows", "Distributed cron orchestration, missed execution handling, and stateful DAGs.", "QG-07, QG-10"),
        ]
    },
    {
        "group_id": "GROUP F",
        "group_name": "Data Engineering (51–60)",
        "skills": [
            ("51", "dex-data-contracts", "Data producer/consumer contracts, breaking change detection, and SLAs.", "QG-01, QG-06"),
            ("52", "dex-data-pipelines", "Batch ETL/ELT pipelines, streaming DAGs (Airflow/Dagster), and dbt models.", "QG-04, QG-05"),
            ("53", "dex-data-quality-audits", "Great Expectations suites, statistical distribution checks, and null audits.", "QG-03, QG-10"),
            ("54", "dex-data-lineage", "OpenLineage tracking, column-level provenance, and upstream impact graphs.", "QG-01, QG-06"),
            ("55", "dex-schema-evolution", "Additive migrations, deprecation policies, and expand-contract patterns.", "QG-06"),
            ("56", "dex-database-query-plans", "EXPLAIN ANALYZE, index scan tuning, locking inspection, and pg_stat.", "QG-08"),
            ("57", "dex-storage-lifecycle", "S3/GCS tiering, Coldline archival, multipart compaction, and cost control.", "QG-08, QG-10"),
            ("58", "dex-data-retention", "GDPR 'right to be forgotten', automated purging, soft-delete, and legal holds.", "QG-09, QG-10"),
            ("59", "dex-capacity-planning", "Load projection modeling, database read-replica scaling, and resource limits.", "QG-08"),
            ("60", "dex-disaster-recovery", "RTO/RPO targets, automated backups, cross-region replication, and failover.", "QG-07, QG-10"),
        ]
    },
    {
        "group_id": "GROUP G",
        "group_name": "AI & LLM Engineering (61–70)",
        "skills": [
            ("61", "dex-llm-integration", "Multi-provider SDKs, structured JSON outputs, streaming, and token limits.", "QG-01, QG-07"),
            ("62", "dex-rag-pipelines", "Chunking strategies, dense/sparse embeddings, and vector DB indexing.", "QG-04, QG-08"),
            ("63", "dex-retrieval-evaluation", "RAGAS metrics, Hit Rate@K, MRR, NDCG, and semantic faithfulness.", "QG-04, QG-10"),
            ("64", "dex-prompt-evaluation", "Few-shot optimization, regression prompt suites, and prompt versioning.", "QG-04, QG-05"),
            ("65", "dex-model-evaluation", "Benchmarking accuracy, latency, cost per 1M tokens, and task routing.", "QG-04, QG-08"),
            ("66", "dex-tool-calling-contracts", "JSON Schema tool definitions, error correction loops, and schema validation.", "QG-01, QG-03"),
            ("67", "dex-agent-permissions", "Human-in-the-loop gates, blast radius controls, and shell execution guards.", "QG-09, QG-10"),
            ("68", "dex-llm-cost-controls", "Token budgets, semantic caching, model downgrading, and cost alerts.", "QG-08, QG-10"),
            ("69", "dex-ai-observability", "OpenTelemetry traces, token attribution, latency percentiles, and spans.", "QG-07, QG-10"),
            ("70", "dex-dataset-curation", "Instruction dataset generation, PII sanitization, and JSONL validation.", "QG-03, QG-09"),
        ]
    },
    {
        "group_id": "GROUP H",
        "group_name": "Developer Experience (71–80)",
        "skills": [
            ("71", "dex-repository-bootstrap", "Zero-to-code project scaffolding, linters, pre-commit, and CI templates.", "QG-01, QG-03"),
            ("72", "dex-monorepo-governance", "Turborepo/Nx pipelines, package boundaries, and remote task caching.", "QG-04, QG-08"),
            ("73", "dex-cli-engineering", "POSIX argument parsing, interactive terminal UI, JSON mode, and exit codes.", "QG-01, QG-07"),
            ("74", "dex-plugin-architecture", "Microkernel pattern, extension lifecycle hooks, manifests, and sandboxes.", "QG-03, QG-07"),
            ("75", "dex-cross-platform-portability", "Windows/Linux/macOS pathing, CRLF/LF line endings, and matrix builds.", "QG-01, QG-04"),
            ("76", "dex-windows-packaging", "InnoSetup, MSIX, WinGet manifest publication, and Authenticode signing.", "QG-01, QG-09"),
            ("77", "dex-documentation-as-code", "Architecture Decision Records (ADR), doctests, and Mermaid diagrams.", "QG-01, QG-05"),
            ("78", "dex-code-generation", "Deterministic AST codegen, scaffolding engines (Plop), and SDK generators.", "QG-01, QG-06"),
            ("79", "dex-developer-tooling", "Devcontainers, Mise/Nix environments, Lefthook, and VS Code debug configs.", "QG-01, QG-08"),
            ("80", "dex-semantic-version-automation", "SemVer 2.0, Conventional Commits parsing, and automated GitHub releases.", "QG-01, QG-10"),
        ]
    },
    {
        "group_id": "GROUP I",
        "group_name": "Security & Reliability (81–90)",
        "skills": [
            ("81", "dex-auth-session-lifecycle", "JWT issuance, refresh token rotation, session revocation, and HttpOnly cookies.", "QG-03, QG-09"),
            ("82", "dex-access-control-tenancy", "RBAC/ABAC authorization, tenant scoping, and PostgreSQL Row-Level Security.", "QG-03, QG-09"),
            ("83", "dex-secrets-management", "Vault/AWS Secrets Manager injection, zero hardcoded credentials, and scanning.", "QG-03, QG-09"),
            ("84", "dex-supply-chain-security", "CycloneDX SBOM generation, dependency lockfile audits, and container Trivy.", "QG-03, QG-10"),
            ("85", "dex-threat-modeling", "Structured STRIDE analysis, attack surface mapping, and abuse cases.", "QG-01, QG-09"),
            ("86", "dex-property-based-testing", "Hypothesis/fast-check invariants, generative fuzzing, and case shrinking.", "QG-01, QG-05"),
            ("87", "dex-chaos-experiments", "Fault injection, network latency simulation (Toxiproxy), and circuit breakers.", "QG-04, QG-08"),
            ("88", "dex-experimentation-metrics", "Feature flags, A/B testing infrastructure, statistical p-value, and telemetry.", "QG-01, QG-08"),
            ("89", "dex-api-contract-evolution", "Backward compatibility diffing, RFC 8594 Sunset headers, and adapters.", "QG-06, QG-10"),
            ("90", "dex-incident-postmortems", "Blameless postmortems, chronological timeline, 5 Whys, and action items.", "QG-01, QG-10"),
        ]
    },
    {
        "group_id": "GROUP J",
        "group_name": "Cloud & Infrastructure (91–100)",
        "skills": [
            ("91", "dex-container-image-engineering", "Multi-stage builds, minimal base images, non-root users, SBOM, and Trivy.", "QG-01, QG-07"),
            ("92", "dex-kubernetes-deployment", "Deployments, probes, resource limits, PodDisruptionBudgets, and rolling updates.", "QG-01, QG-05"),
            ("93", "dex-infrastructure-as-code", "Terraform/OpenTofu, remote state locking, drift detection, and Checkov scan.", "QG-01, QG-07"),
            ("94", "dex-cloud-service-integration", "Workload Identity, exponential backoff with jitter, and least privilege IAM.", "QG-03, QG-07"),
            ("95", "dex-zero-downtime-rollouts", "Blue-green, Argo canary, progressive traffic shifting, and instant rollback.", "QG-01, QG-09"),
            ("96", "dex-service-mesh-networking", "Istio/Linkerd mTLS, traffic routing, circuit breaking, and Envoy outlier detection.", "QG-01, QG-07"),
            ("97", "dex-network-troubleshooting", "DNS, TLS cert chains, TCP SYN/RST, HTTP latency, and tcpdump packet analysis.", "QG-01, QG-06"),
            ("98", "dex-slo-error-budgets", "SLIs, SLOs, rolling error budgets, multi-window burn rate alerts, and freeze rules.", "QG-01, QG-08"),
            ("99", "dex-distributed-tracing", "OpenTelemetry, W3C tracecontext propagation, span lifecycle, and latency bottlenecks.", "QG-01, QG-07"),
            ("100", "dex-cloud-cost-finops", "Cloud cost allocation tags, right-sizing, idle asset cleanup, and unit economics.", "QG-01, QG-08"),
        ]
    },
    {
        "group_id": "GROUP K",
        "group_name": "Mobile & Desktop Engineering (101–110)",
        "skills": [
            ("101", "dex-android-app-architecture", "Jetpack Compose, MVVM/MVI, StateFlow, Room database, and Hilt DI.", "QG-01, QG-07"),
            ("102", "dex-ios-app-architecture", "SwiftUI, Swift Concurrency, NavigationStack, Observation, and SwiftData.", "QG-01, QG-07"),
            ("103", "dex-electron-security", "contextIsolation, nodeIntegration disabled, sandbox, minimal contextBridge, and CSP.", "QG-01, QG-07"),
            ("104", "dex-tauri-desktop-integration", "Tauri v2, Rust backend commands, strict capabilities, and minimal memory footprint.", "QG-01, QG-07"),
            ("105", "dex-mobile-offline-sync", "Offline-first SQLite/WatermelonDB, mutation sync queues, CRDT/LWW, and workers.", "QG-01, QG-08"),
            ("106", "dex-mobile-release-pipelines", "Fastlane automation, keystore signing, Match provisioning, and store uploads.", "QG-01, QG-07"),
            ("107", "dex-mobile-performance-profiling", "Startup time (TTID/TTFD), frame jank (60/120 fps), LeakCanary, and battery.", "QG-01, QG-08"),
            ("108", "dex-desktop-ipc-design", "Type-safe IPC schemas (Zod/JSON Schema), bi-directional events, and validation.", "QG-01, QG-07"),
            ("109", "dex-native-device-integration", "Camera, Geolocation, Bluetooth BLE, Biometrics, and graceful hardware fallbacks.", "QG-01, QG-07"),
            ("110", "dex-desktop-update-delivery", "Auto-updates, cryptographic signatures (Minisign/Ed25519), and atomic rollbacks.", "QG-01, QG-07"),
        ]
    },
    {
        "group_id": "GROUP L",
        "group_name": "Product & Operations Engineering (111–120)",
        "skills": [
            ("111", "dex-privacy-impact-assessment", "GDPR/CCPA DPIA, personal data classification, minimization, and user rights.", "QG-01, QG-07"),
            ("112", "dex-compliance-control-mapping", "SOC 2 Type II, ISO 27001, HIPAA control mapping, and automated evidence collection.", "QG-01, QG-08"),
            ("113", "dex-audit-trail-integrity", "Tamper-evident hash chaining, S3 Object Lock (WORM), and CloudEvents schema.", "QG-01, QG-07"),
            ("114", "dex-configuration-drift", "ArgoCD/Flux GitOps reconciliation, Terraform drift, and automated self-healing.", "QG-01, QG-08"),
            ("115", "dex-product-discovery", "Jobs-to-be-Done (JTBD), Opportunity Solution Trees, and assumption spike testing.", "QG-01, QG-02"),
            ("116", "dex-feature-prioritization", "RICE scoring, Value vs Effort matrix, WSJF, and dependency graph resolution.", "QG-01, QG-04"),
            ("117", "dex-analytics-instrumentation", "Strict tracking plans, object_action taxonomy, Zod schemas, and PII scrubbing.", "QG-01, QG-07"),
            ("118", "dex-feedback-triage", "High-velocity bug/feedback classification, deduplication, and reproduction recipes.", "QG-01, QG-08"),
            ("119", "dex-runbook-automation", "Guarded executable runbooks (SOPs), interactive approval gates, and rollbacks.", "QG-01, QG-09"),
            ("120", "dex-operational-readiness-review", "Production launch readiness review across reliability, security, support, and DR.", "QG-01, QG-09"),
        ]
    }
]

def build_skills_index():
    out = [
        "# DEX Skills Index & Quick Reference Catalog v4.0\n",
        "Bảng tra cứu nhanh toàn diện cho toàn bộ **121 Kỹ năng (1 Master Orchestrator + 120 Kỹ năng Chuyên biệt)** thuộc **DEX Engineering Skills Pack v4.0.0**.\n",
        "Tuân thủ nghiêm ngặt đặc tả [Agent Skills Specification](https://agentskills.io/specification) và chuẩn hóa đầy đủ 14 mục kỹ thuật bắt buộc.\n",
        "---\n\n",
        "## Master Orchestrator (00)\n\n",
        "| STT | Tên Kỹ Năng (`name`) | Phân Nhóm | Trách Nhiệm Cốt Lõi | Cổng Chất Lượng Kiểm Soát |",
        "|:---|:---|:---|:---|:---|",
        "| **00** | [`dex-master-orchestrator`](.agents/skills/dex-master-orchestrator/SKILL.md) | **Master Control Plane** | Điều phối toàn bộ 120 specialized skills, phân loại độ phức tạp (QUICK, STANDARD, STRICT), kiểm soát 12 Quality Gates và xuất báo cáo kiểm chứng minh bạch. | QG-01 đến QG-12 |\n\n",
        "---\n\n",
        "## 120 Kỹ Năng Chuyên Biệt Theo 12 Phân Nhóm Chuyên Ngành (Groups A–L)\n\n"
    ]

    for g in SKILL_GROUPS_V4:
        out.append(f"### {g['group_id']}: {g['group_name']}\n")
        out.append("| STT | Tên Kỹ Năng (`name`) | Trách Nhiệm Kỹ Thuật | Cổng Chất Lượng (Quality Gates) |")
        out.append("|:---|:---|:---|:---|")
        for stt, name, desc, qg in g["skills"]:
            out.append(f"| **{stt}** | [`{name}`](.agents/skills/{name}/SKILL.md) | {desc} | {qg} |")
        out.append("\n")

    out.append("---\n\n")
    out.append("## Segregated Upstream Integration Modules (`integrations/`)\n\n")
    out.append("Các kỹ năng mở rộng được nhập khẩu từ nguồn bên ngoài và lưu trữ độc lập trong thư mục `integrations/`, không tính gộp vào danh mục 120 kỹ năng bản địa:\n\n")
    out.append("| Module | Nguồn Gốc | Đường Dẫn | Trách Nhiệm |\n")
    out.append("|:---|:---|:---|:---|\n")
    out.append("| **API Mocking & Virtualization** | Source A: Agentic Awesome Skills | [`integrations/aas/dex-api-mocking-virtualization`](integrations/aas/dex-api-mocking-virtualization/SKILL.md) | Hermetic offline API mocking, WireMock, Mock Service Worker (MSW). |\n")
    out.append("| **Defensive Binary Inspection** | Source B: Reverse Skill | [`integrations/reverse-skill/dex-binary-inspection`](integrations/reverse-skill/dex-binary-inspection/SKILL.md) | Static PE/ELF header analysis, ASLR/DEP flags, and library dependencies. |\n")
    out.append("| **JavaScript Bundle Deobfuscation** | Source B: Reverse Skill | [`integrations/reverse-skill/dex-javascript-bundle-deobfuscation`](integrations/reverse-skill/dex-javascript-bundle-deobfuscation/SKILL.md) | Sourcemap reconstruction and web/Electron bundle security auditing. |\n")
    out.append("| **REA MCP Adapter** | Source C: Reverse Engineer Anything | [`integrations/rea/dex-rea-adapter`](integrations/rea/dex-rea-adapter/SKILL.md) | Standardized MCP adapter bridge to local REA reverse engineering engine. |\n")

    return "\n".join(out)

def build_routing_matrix():
    return """# DEX Dynamic Skill Routing Matrix v4.0

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
"""

def build_architecture_md():
    return """# DEX Engineering Skills Pack v4.0 — Technical Architecture

## 1. Architectural Mission & Overview

**DEX Engineering Skills Pack v4.0** is an enterprise-grade, deterministic AI Agent Skills Framework comprising:
- **120 Specialized Engineering Skills** across 12 distinct engineering domains.
- **1 Master Orchestrator** (`dex-master-orchestrator`) acting as root control plane.
- **Total: Exactly 121 Native DEX Skills** in `.agents/skills/`.
- **Segregated Multi-Source Integration Layer** (`integrations/`) managing third-party skills without polluting native numbering.

```mermaid
graph TD
    UserReq[User Request] --> MasterOrch[dex-master-orchestrator]
    
    subgraph DEX Core Domain Engine 120 Skills
        GrpA[Group A: Core Engineering 01-10]
        GrpB[Group B: Architecture & AI Agents 11-20]
        GrpC[Group C: Production Engineering 21-30]
        GrpD[Group D: Frontend Engineering 31-40]
        GrpE[Group E: Backend & Integration 41-50]
        GrpF[Group F: Data Engineering 51-60]
        GrpG[Group G: AI & LLM Engineering 61-70]
        GrpH[Group H: Developer Experience 71-80]
        GrpI[Group I: Security & Reliability 81-90]
        GrpJ[Group J: Cloud & Infrastructure 91-100]
        GrpK[Group K: Mobile & Desktop 101-110]
        GrpL[Group L: Product & Operations 111-120]
    end

    subgraph External Upstream Integrations integrations/
        AAS[integrations/aas - Mocking]
        RevSkill[integrations/reverse-skill - Binary/JS Audit]
        REA[integrations/rea - REA MCP Adapter]
    end

    MasterOrch --> GrpA & GrpB & GrpC & GrpD & GrpE & GrpF & GrpG & GrpH & GrpI & GrpJ & GrpK & GrpL
    MasterOrch -.->|Delegated Playbooks & Tools| AAS & RevSkill & REA
```

---

## 2. The 12 Technical Disciplines

1. **Group A: Core Engineering (01–10)**: Task breakdown, atomic Git, scientific debugging, profiling, security audit, release engineering.
2. **Group B: Architecture & AI Agents (11–20)**: Production telemetry, refactoring, Clean Architecture, database engineering, testing pyramid, agent governance.
3. **Group C: Production Engineering (21–30)**: Blast radius calculation, dependency pinning, resilience, state synchronization, a11y, feature flags.
4. **Group D: Frontend Engineering (31–40)**: Component contracts, design tokens, unidirectional data flow, Zod forms, client routing, Web Vitals, SSR/SEO.
5. **Group E: Backend & Integration (41–50)**: Domain-Driven Design, async worker queues, caching, WebSockets/SSE, search, event-driven streaming, idempotent operations.
6. **Group F: Data Engineering (51–60)**: Data contracts, batch/streaming ETL, data quality audits, OpenLineage, schema evolution, query plans, storage lifecycle.
7. **Group G: AI & LLM Engineering (61–70)**: LLM integration, RAG vector pipelines, retrieval evaluation (RAGAS), prompt evaluation, model evaluation, tool calling contracts.
8. **Group H: Developer Experience (71–80)**: Project scaffolding, monorepo governance, CLI engineering, plugin architecture, cross-platform portability, WinGet packaging.
9. **Group I: Security & Reliability (81–90)**: Auth session lifecycle, Row-Level Security tenancy, secret scanning, CycloneDX SBOM, STRIDE threat modeling, chaos engineering.
10. **Group J: Cloud & Infrastructure (91–100)**: Container image engineering, Kubernetes workloads, declarative IaC Terraform, Workload Identity, zero-downtime rollouts, Istio service mesh, network troubleshooting, SLO error budgets, OpenTelemetry distributed tracing, FinOps cloud cost optimization.
11. **Group K: Mobile & Desktop Engineering (101–110)**: Modern Android Compose, modern iOS SwiftUI, hardened Electron security, lightweight Tauri v2 integration, offline-first sync (CRDT/mutation queue), Fastlane release pipelines, mobile profiling, desktop IPC design, native hardware integration, desktop update delivery.
12. **Group L: Product & Operations Engineering (111–120)**: Privacy impact assessment (DPIA/GDPR), compliance control mapping (SOC 2/ISO 27001), tamper-evident audit trails (Merkle/WORM), configuration drift reconciliation, structured product discovery (JTBD), quantitative feature prioritization (RICE), analytics instrumentation, high-velocity feedback triage, runbook automation, operational readiness review (ORR).

---

## 3. The 12 Quality Gates (QG-01 to QG-12)

Every engineering change and skill execution in DEX v4.0 is governed by 12 quality gates:

- **QG-01**: Scope Control — Changes must remain strictly bounded within assigned scope.
- **QG-02**: Acceptance Criteria — Explicit Given-When-Then criteria met.
- **QG-03**: Frontmatter Validity — Valid YAML frontmatter, name matching directory.
- **QG-04**: Unique Identification — No identifier collisions across the catalog.
- **QG-05**: Distinct Responsibility — Orthogonal domain boundaries with zero unnecessary overlap.
- **QG-06**: Reference Integrity — All file, script, and markdown links are valid.
- **QG-07**: Security Boundaries — Zero credentials in code, least privilege enforcement.
- **QG-08**: License & Attribution — Upstream licenses documented in `THIRD_PARTY_NOTICES.md`.
- **QG-09**: Safe Import & Rollback — Verified dry-run execution and rollback capability.
- **QG-10**: Routing Validity — Dynamic dispatch accurately resolves valid catalog skills.
- **QG-11**: Executable Verification — Automated test suites execute with 100% PASS.
- **QG-12**: Git Hygiene & Review — Clean diff review and Conventional Commits.
"""

def build_install_md():
    return """# DEX Engineering Skills Pack v4.0 — Installation & Quickstart Guide

## 1. System Requirements

- **Operating System**: Windows 11, Windows 10 (WSL2 supported), macOS 13+, or Ubuntu 22.04+
- **Runtimes**: Python 3.10+ (Python 3.12 recommended), Node.js 20+ LTS
- **AI Coding Agent**: OpenAI Codex, Cursor, Windsurf, Claude Code, or VS Code with Agent Skills support

---

## 2. Installation Steps

### Step 1: Clone Repository
```bash
git clone https://github.com/nguyenducanhst2022-png/dex-engineering-skills.git
cd dex-engineering-skills
```

### Step 2: Install Python Dependencies
```bash
pip install -r requirements-dev.txt
# Hoặc cài đặt trực tiếp pytest:
pip install pytest
```

### Step 3: Run Validation & Verification
```bash
# Validate toàn bộ 121 kỹ năng DEX
python scripts/validate_skills.py

# Chạy toàn bộ test suite
pytest tests/ -v
```

---

## 3. Configuring for AI Coding Agents

### OpenAI Codex / Universal Coding Agents
Sao chép thư mục `.agents/` vào thư mục gốc của dự án bạn đang phát triển:
```bash
cp -r .agents /path/to/your/project/
```

Thêm chỉ dẫn vào file `AGENTS.md` trong dự án của bạn:
```markdown
# AGENTS.md
You have access to the DEX Engineering Skills Pack in `.agents/skills/`.
Always begin tasks by activating `dex-master-orchestrator`.
The Master Orchestrator will classify your task (QUICK, STANDARD, STRICT),
select the required specialized skills from Groups A through L (120 skills),
and enforce the 12 Quality Gates.
```
"""

def build_changelog():
    return """# Changelog

All notable changes to the **DEX Engineering Skills Pack** are documented in this file.
This project strictly adheres to [Semantic Versioning 2.0.0](https://semver.org/).

---

## [4.0.0] - 2026-10-22

### Added — 30 New Specialized Skills across 3 New Disciplines (Groups J, K, L)
- **Group J: Cloud & Infrastructure (Skills 91–100)**:
  - `dex-container-image-engineering` (91): Minimal container images, multi-stage builds, non-root users, SBOM, and Trivy CVE scanning.
  - `dex-kubernetes-deployment` (92): Kubernetes workloads, probes, resource limits, PodDisruptionBudgets, and rolling updates.
  - `dex-infrastructure-as-code` (93): Terraform/OpenTofu, remote state locking, drift detection, and Checkov compliance scanning.
  - `dex-cloud-service-integration` (94): Workload Identity Federation, exponential backoff with jitter, and least privilege IAM.
  - `dex-zero-downtime-rollouts` (95): Blue-green and Argo canary rollouts with automated Prometheus metric gating.
  - `dex-service-mesh-networking` (96): Istio/Linkerd mTLS, fine-grained traffic routing, circuit breaking, and Envoy outlier detection.
  - `dex-network-troubleshooting` (97): DNS resolution, TLS cert chains, TCP connection states, HTTP latency, and tcpdump packet analysis.
  - `dex-slo-error-budgets` (98): SLIs, SLOs, rolling error budgets, multi-window burn rate alerting, and deployment freeze policies.
  - `dex-distributed-tracing` (99): OpenTelemetry standard instrumentation, W3C tracecontext propagation, and bottleneck latency analysis.
  - `dex-cloud-cost-finops` (100): Cost allocation tags, right-sizing, idle asset reclamation, savings plans, and unit economics.
- **Group K: Mobile & Desktop Engineering (Skills 101–110)**:
  - `dex-android-app-architecture` (101): Modern Android architecture with Jetpack Compose, MVVM/MVI, StateFlow, Room DB, and Hilt.
  - `dex-ios-app-architecture` (102): Modern iOS architecture with SwiftUI, Swift Concurrency (async/await, Actor), NavigationStack, and SwiftData.
  - `dex-electron-security` (103): Hardened Electron security with contextIsolation, nodeIntegration disabled, sandbox, and minimal contextBridge.
  - `dex-tauri-desktop-integration` (104): Lightweight Tauri v2 architecture with Rust backend commands, strict capabilities, and native controls.
  - `dex-mobile-offline-sync` (105): Offline-first architecture with local SQLite, mutation sync queues, CRDT/LWW conflict resolution, and background workers.
  - `dex-mobile-release-pipelines` (106): Fastlane mobile CI/CD pipelines, Android keystore signing, Match provisioning, and store distribution.
  - `dex-mobile-performance-profiling` (107): Mobile startup time profiling (TTID/TTFD), frame jank detection (60/120 fps), LeakCanary, and battery optimization.
  - `dex-desktop-ipc-design` (108): Type-safe desktop IPC interfaces using Zod/JSON Schema, bi-directional events, and main-process input validation.
  - `dex-native-device-integration` (109): Hardware device capabilities (Camera, Geolocation, Bluetooth BLE, Biometrics) with runtime permissions and fallbacks.
  - `dex-desktop-update-delivery` (110): Secure desktop auto-updates with cryptographic signatures (Minisign/Ed25519), delta updates, and atomic rollbacks.
- **Group L: Product & Operations Engineering (Skills 111–120)**:
  - `dex-privacy-impact-assessment` (111): GDPR/CCPA DPIA assessments, personal data classification, data minimization, and user rights automation.
  - `dex-compliance-control-mapping` (112): SOC 2 Type II, ISO 27001, HIPAA control mapping, and continuous automated evidence collection.
  - `dex-audit-trail-integrity` (113): Append-only tamper-evident audit logging with Merkle hash chaining, S3 Object Lock (WORM), and CloudEvents schema.
  - `dex-configuration-drift` (114): Continuous drift detection and automated self-healing across Kubernetes GitOps (ArgoCD/Flux) and Terraform.
  - `dex-product-discovery` (115): Structured product discovery, Jobs-to-be-Done (JTBD), Opportunity Solution Trees, and rapid prototyping hypothesis testing.
  - `dex-feature-prioritization` (116): Quantitative feature prioritization using RICE scoring, Value vs Effort, WSJF, and dependency graph analysis.
  - `dex-analytics-instrumentation` (117): Strict tracking plans, object_action taxonomy, Zod schemas, automated PII scrubbing, and dual client/server verification.
  - `dex-feedback-triage` (118): High-velocity user feedback classification, bug severity triage, semantic deduplication, and reproduction recipes.
  - `dex-runbook-automation` (119): Executable runbooks (SOPs) with pre-flight checks, interactive approval gates, guarded commands, and rollback procedures.
  - `dex-operational-readiness-review` (120): Production Operational Readiness Reviews (ORR) across reliability, security, observability, DR, and supportability.

### Changed
- **Total Native Skills Count**: Expanded to exactly **120 Specialized Skills + 1 Master Orchestrator (121 Skills Total)** in `.agents/skills/`.
- **Master Orchestrator Upgraded**: Updated `dex-master-orchestrator` with complete routing coverage across all 12 domains (Groups A–L) and 12 Quality Gates (QG-01 to QG-12).
- **Segregated Integration Architecture**: Relocated third-party upstream skills to `integrations/` (`integrations/aas`, `integrations/reverse-skill`, `integrations/rea`) ensuring clean segregation from native numbering.
- **Routing Matrix Expanded**: Added Scenarios M, N, O, P covering Cloud, Mobile, FinOps, and Compliance.
"""

def main():
    print("=== DEX v4.0: GENERATING DOCUMENTATION SUITE ===")
    
    # 1. SKILLS_INDEX.md
    with open(os.path.join(ROOT_DIR, "SKILLS_INDEX.md"), "w", encoding="utf-8") as f:
        f.write(build_skills_index().strip() + "\n")
    print("  [UPDATED] SKILLS_INDEX.md")

    # 2. ROUTING_MATRIX.md
    with open(os.path.join(ROOT_DIR, "ROUTING_MATRIX.md"), "w", encoding="utf-8") as f:
        f.write(build_routing_matrix().strip() + "\n")
    print("  [UPDATED] ROUTING_MATRIX.md")

    # 3. ARCHITECTURE.md
    with open(os.path.join(ROOT_DIR, "ARCHITECTURE.md"), "w", encoding="utf-8") as f:
        f.write(build_architecture_md().strip() + "\n")
    print("  [UPDATED] ARCHITECTURE.md")

    # 4. INSTALL.md
    with open(os.path.join(ROOT_DIR, "INSTALL.md"), "w", encoding="utf-8") as f:
        f.write(build_install_md().strip() + "\n")
    print("  [UPDATED] INSTALL.md")

    # 5. CHANGELOG.md
    with open(os.path.join(ROOT_DIR, "CHANGELOG.md"), "w", encoding="utf-8") as f:
        f.write(build_changelog().strip() + "\n")
    print("  [UPDATED] CHANGELOG.md")

    print("Documentation suite generated successfully!")

if __name__ == "__main__":
    main()
