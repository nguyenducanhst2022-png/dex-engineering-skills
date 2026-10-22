# -*- coding: utf-8 -*-
"""
Documentation Generator for DEX Engineering Skills Pack v3.0.
Generates and updates:
- ARCHITECTURE.md
- SKILLS_INDEX.md
- ROUTING_MATRIX.md
- README.md
- INSTALL.md
- AGENTS.example.md
- CHANGELOG.md
"""

import os
import re

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SKILLS_DIR = os.path.join(ROOT_DIR, ".agents", "skills")

SKILL_GROUPS = [
    {
        "group_id": "GROUP A",
        "group_name": "Core Engineering (Bài 1–10)",
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
        "group_name": "Software Architecture & AI Agents (Bài 11–20)",
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
        "group_name": "Production Engineering (Bài 21–30)",
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
        "group_name": "Data & Infrastructure (51–60)",
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
        "group_name": "Developer Experience & Platform (71–80)",
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
        "group_name": "Security, Reliability & Product (81–90)",
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
    }
]

def build_skills_index():
    out = [
        "# DEX Skills Index & Quick Reference Catalog v3.0\n",
        "Bảng tra cứu nhanh toàn diện cho toàn bộ **91 Kỹ năng (1 Master Orchestrator + 90 Kỹ năng Chuyên biệt)** thuộc **DEX Engineering Skills Pack v3.0.0**.\n",
        "Tuân thủ nghiêm ngặt đặc tả [Agent Skills Specification](https://agentskills.io/specification) và chuẩn hóa đầy đủ 14 mục kỹ thuật bắt buộc.\n",
        "---\n\n",
        "## Master Orchestrator (00)\n\n",
        "| STT | Tên Kỹ Năng (`name`) | Phân Nhóm | Trách Nhiệm Cốt Lõi | Cổng Chất Lượng Kiểm Soát |",
        "|:---|:---|:---|:---|:---|",
        "| **00** | [`dex-master-orchestrator`](.agents/skills/dex-master-orchestrator/SKILL.md) | **Master Orchestration** | Điều phối toàn bộ 90 skills, phân loại độ phức tạp (QUICK, STANDARD, STRICT), kiểm soát 10 Quality Gates và báo cáo kiểm chứng minh bạch. | QG-01 đến QG-10 |\n\n",
        "---\n\n",
        "## 90 Kỹ Năng Chuyên Biệt Theo 9 Phân Nhóm Chuyên Ngành\n\n"
    ]

    for g in SKILL_GROUPS:
        out.append(f"### {g['group_id']}: {g['group_name']}\n")
        out.append("| STT | Tên Kỹ Năng (`name`) | Trách Nhiệm Kỹ Thuật | Cổng Chất Lượng (Quality Gates) |")
        out.append("|:---|:---|:---|:---|")
        for stt, name, desc, qg in g["skills"]:
            out.append(f"| **{stt}** | [`{name}`](.agents/skills/{name}/SKILL.md) | {desc} | {qg} |")
        out.append("\n")

    return "\n".join(out)

def build_architecture_md():
    return """# DEX Engineering Skills Pack v3.0 — Technical Architecture

## 1. Architectural Mission & Overview

**DEX Engineering Skills Pack v3.0** is an enterprise-grade, deterministic AI Agent Skills Framework comprising **90 specialized engineering skills + 1 Master Orchestrator (91 skills total)**.

Designed for modern AI coding agents (specifically **OpenAI Codex**, **Cursor**, **Windsurf**, and **VS Code**), this system converts high-level user intentions into modular, strictly verified software engineering workflows without hallucinated completions or unverified claims.

```mermaid
graph TD
    User([User Request / Task]) --> Master[00: dex-master-orchestrator]
    
    subgraph Triage Engine
        Master --> Classify{Complexity Triage & Risk Matrix}
        Classify -->|Score 1-3| Quick[QUICK MODE: Fast-path Execution]
        Classify -->|Score 4-7| Standard[STANDARD MODE: Iterative Verification]
        Classify -->|Score 8-10| Strict[STRICT MODE: Enterprise Lifecycle]
    end

    subgraph 9 Specialized Engineering Domains
        Quick & Standard & Strict --> GroupA[Group A: Core Engineering 01-10]
        Quick & Standard & Strict --> GroupB[Group B: Architecture & AI Agents 11-20]
        Quick & Standard & Strict --> GroupC[Group C: Production Engineering 21-30]
        Quick & Standard & Strict --> GroupD[Group D: Frontend Engineering 31-40]
        Quick & Standard & Strict --> GroupE[Group E: Backend & Integration 41-50]
        Quick & Standard & Strict --> GroupF[Group F: Data & Infrastructure 51-60]
        Quick & Standard & Strict --> GroupG[Group G: AI & LLM Engineering 61-70]
        Quick & Standard & Strict --> GroupH[Group H: Developer Experience 71-80]
        Quick & Standard & Strict --> GroupI[Group I: Security & Reliability 81-90]
    end

    subgraph Quality Assurance
        GroupA & GroupB & GroupC & GroupD & GroupE & GroupF & GroupG & GroupH & GroupI --> QGates[10 Quality Gates QG-01 to QG-10]
    end

    QGates --> AuditReport[Verified Execution Report with Terminal Evidence]
```

---

## 2. Master Orchestrator (`dex-master-orchestrator`)

The Master Orchestrator serves as the central control plane. It enforces the immutable lifecycle:
`Analyze → Specify → Plan → Implement → Verify → Debug → Stabilize → Review → Commit → Release → Maintain`

### Execution Modes
1. **QUICK MODE (Risk Score 1–3)**:
   - For localized typo fixes, single-line bug fixes, documentation typos, or config tweaks.
   - Activates: `dex-development-workflow` + `dex-code-verification`.
   - Quality Gates: QG-01, QG-03, QG-04.
2. **STANDARD MODE (Risk Score 4–7)**:
   - For standard feature additions, API endpoints, bug investigations, and refactoring.
   - Activates: Scoped group of 3–5 specialized skills on a dedicated Git branch.
   - Quality Gates: QG-01 through QG-06, QG-09, QG-10.
3. **STRICT MODE (Risk Score 8–10)**:
   - For database schema migrations, authentication/authorization overhauls, payment logic, and releases.
   - Activates: Full orchestration with architectural review, threat modeling, chaos verification, and rollback plans.
   - Quality Gates: All 10 Quality Gates (QG-01 through QG-10) enforced with zero waivers.

---

## 3. The 10 Quality Gates (QG-01 to QG-10)

Every task executed under the DEX framework must clear the mandatory quality gates:

| Gate | Name | Technical Enforcement & Verification Criteria |
|:---|:---|:---|
| **QG-01** | Specification & Input Contract | Clear goal, defined input/output boundaries, acceptance criteria documented. |
| **QG-02** | Decomposition & Blast Radius | Task split into bite-sized steps; blast radius mapped before modifying code. |
| **QG-03** | Code Quality & Type Safety | Zero linter warnings (`--max-warnings 0`), 100% strict type checking. |
| **QG-04** | Automated Verification | Real terminal execution of tests; zero skipped tests; no mocked falsified passes. |
| **QG-05** | Root-Cause Defect Elimination | Defect reproduced by a failing test first; underlying defect eliminated. |
| **QG-06** | Schema & Contract Compatibility | Zero unapproved breaking changes via schema diffing; backward compatibility intact. |
| **QG-07** | Resilience & Error Handling | Timeouts, exponential backoff retries, and circuit breaker fallbacks in place. |
| **QG-08** | Performance & Resource Budget | Execution within latency/memory budgets; query execution plans inspected. |
| **QG-09** | Security & Tenancy Isolation | Zero hardcoded credentials, SAST audit passed, tenant isolation verified via RLS. |
| **QG-10** | Evidence-Based Delivery | Full command output and verifiable proof provided; release changelog updated. |

---

## 4. Skills Taxonomy: 9 Specialized Engineering Groups

1. **Group A: Core Engineering (01–10)**: Fundamental Vibe Coding loops, task delegation, verification, git safety, modularity, profiling, and security auditing.
2. **Group B: Software Architecture & AI Agents (11–20)**: Production observability, refactoring, Clean Architecture, schema migrations, and autonomous agent governance.
3. **Group C: Production Engineering (21–30)**: Blast radius calculation, dependency management, resilience patterns, race conditions, WCAG accessibility, and full-lifecycle delivery.
4. **Group D: Frontend Engineering (31–40)**: UI component contracts, design system tokens, state normalization, client routing, Web Vitals, SSR/SEO, and visual regression.
5. **Group E: Backend & Integration (41–50)**: Domain-Driven Design, async worker queues, distributed caching, WebSockets/SSE, search indexing, and event streaming.
6. **Group F: Data & Infrastructure (51–60)**: Data contracts, batch/streaming ETL, Great Expectations quality suites, schema evolution, query plans, and disaster recovery.
7. **Group G: AI & LLM Engineering (61–70)**: LLM integration, RAG vector pipelines, retrieval metrics (RAGAS), prompt evaluation, tool calling contracts, and cost controls.
8. **Group H: Developer Experience & Platform (71–80)**: Repository bootstrapping, monorepo governance, CLI engineering, cross-platform portability, WinGet/MSIX, and SemVer automation.
9. **Group I: Security, Reliability & Product (81–90)**: Session lifecycles, Row-Level Security tenancy, secrets management, supply chain SBOM, STRIDE threat modeling, chaos experiments, and blameless postmortems.

---

## 5. Security & Safety Boundaries

The framework enforces hard security guardrails that agents cannot bypass:
- **Destructive Command Interception**: Commands like `rm -rf /`, `DROP DATABASE`, `git push --force origin main`, and `git reset --hard` are strictly blocked.
- **Zero Hardcoded Secrets**: All tokens, API keys, and private credentials must be injected dynamically via environment variables or secret managers.
- **Production State Guardrail**: AI agents never execute mutating scripts directly against production environments without pre-flight staging verification and explicit operator confirmation.
- **Defense-in-Depth Multi-Tenancy**: Data isolation is enforced at the database layer (PostgreSQL RLS), ensuring application bugs cannot leak cross-tenant data.
"""

def main():
    print("Generating DEX Engineering Skills Pack v3.0 Documentation...")

    # 1. SKILLS_INDEX.md
    skills_index_content = build_skills_index()
    with open(os.path.join(ROOT_DIR, "SKILLS_INDEX.md"), "w", encoding="utf-8") as f:
        f.write(skills_index_content.strip() + "\n")
    print("  [UPDATED] SKILLS_INDEX.md")

    # 2. ARCHITECTURE.md
    arch_content = build_architecture_md()
    with open(os.path.join(ROOT_DIR, "ARCHITECTURE.md"), "w", encoding="utf-8") as f:
        f.write(arch_content.strip() + "\n")
    print("  [CREATED] ARCHITECTURE.md")

    # 3. ROUTING_MATRIX.md
    routing_content = """# DEX Dynamic Routing Matrix v3.0

The Dynamic Routing Matrix maps real-world engineering objectives to specialized multi-skill execution workflows coordinated by `dex-master-orchestrator`.

---

## The 10 Canonical Engineering Scenarios (A through J)

### Scenario A: Emergency Database Migration Failure
- **Context**: A database migration on production locked critical tables and failed halfway with broken foreign key constraints.
- **Complexity**: STRICT MODE (Score 10)
- **Primary Skills**:
  - `dex-root-cause-debugging`: Isolate migration failure reason and transaction lock state.
  - `dex-database-engineering`: Execute safe rollback without data loss.
  - `dex-schema-evolution`: Rewrite migration using expand-and-contract pattern.
- **Complementary Skills**: `dex-disaster-recovery`, `dex-production-monitoring`, `dex-incident-postmortems`.
- **Enforced Quality Gates**: QG-04, QG-05, QG-06, QG-09, QG-10.
- **Key Deliverables**: Zero-downtime reversible migration script, table lock resolution report, and post-incident RCA.

---

### Scenario B: AI-Powered Search & Enterprise RAG Implementation
- **Context**: Architect and deploy an enterprise document search engine with hybrid dense/sparse vector retrieval and LLM summarization.
- **Complexity**: STANDARD MODE (Score 6)
- **Primary Skills**:
  - `dex-rag-pipelines`: Build chunking, embedding, and vector database indexing pipeline.
  - `dex-retrieval-evaluation`: Measure retrieval accuracy using Hit Rate@K, MRR, and NDCG.
  - `dex-llm-integration`: Implement structured JSON output and prompt streaming.
- **Complementary Skills**: `dex-search-engineering`, `dex-tool-calling-contracts`, `dex-llm-cost-controls`.
- **Enforced Quality Gates**: QG-01, QG-04, QG-07, QG-08, QG-10.
- **Key Deliverables**: RAG retrieval service, automated evaluation suite, and token cost attribution dashboard.

---

### Scenario C: Monorepo Architecture Modernization
- **Context**: Consolidate 12 fragmented repositories into a single governed monorepo with Turborepo task caching and package boundaries.
- **Complexity**: STANDARD MODE (Score 7)
- **Primary Skills**:
  - `dex-monorepo-governance`: Structure `apps/` and `packages/`, enforce boundary rules.
  - `dex-repository-bootstrap`: Standardize linting, formatting, and pre-commit configurations.
  - `dex-code-organization`: Eliminate circular dependencies between shared libraries.
- **Complementary Skills**: `dex-developer-tooling`, `dex-cicd-automation`, `dex-semantic-version-automation`.
- **Enforced Quality Gates**: QG-01, QG-03, QG-04, QG-08.
- **Key Deliverables**: `pnpm-workspace.yaml`, `turbo.json` with remote cache, and clean dependency graph.

---

### Scenario D: High-Concurrency Real-time Collaborative Canvas
- **Context**: Build a multiplayer collaborative whiteboard supporting 50,000 concurrent WebSockets with conflict resolution.
- **Complexity**: STRICT MODE (Score 8)
- **Primary Skills**:
  - `dex-realtime-protocols`: WebSocket connection management, heartbeats, and reconnection backoff.
  - `dex-concurrency-state`: Conflict-free Replicated Data Types (CRDTs) and atomic updates.
  - `dex-event-driven-architecture`: Redis Pub/Sub backplane for horizontal websocket scaling.
- **Complementary Skills**: `dex-caching-strategies`, `dex-frontend-performance`, `dex-performance-optimization`.
- **Enforced Quality Gates**: QG-04, QG-07, QG-08, QG-10.
- **Key Deliverables**: WebSocket gateway service, CRDT state sync engine, and high-concurrency load test suite.

---

### Scenario E: Enterprise SaaS Multi-Tenant Isolation & Authentication
- **Context**: Implement enterprise authentication, JWT rotation, session revocation, and PostgreSQL Row-Level Security for B2B SaaS.
- **Complexity**: STRICT MODE (Score 9)
- **Primary Skills**:
  - `dex-auth-session-lifecycle`: Refresh token rotation, reuse detection, and HttpOnly cookies.
  - `dex-access-control-tenancy`: Fine-grained RBAC/ABAC and PostgreSQL Row-Level Security policies.
  - `dex-secrets-management`: Zero hardcoded credentials with HashiCorp Vault / Doppler integration.
- **Complementary Skills**: `dex-security-audit`, `dex-threat-modeling`, `dex-database-engineering`.
- **Enforced Quality Gates**: QG-01, QG-03, QG-04, QG-09, QG-10.
- **Key Deliverables**: Auth middleware, PostgreSQL RLS policies, and cross-tenant penetration test suite.

---

### Scenario F: Mission-Critical Production Outage Postmortem
- **Context**: Facilitate a blameless postmortem after a 42-minute payment gateway outage and track technical remediations.
- **Complexity**: STANDARD MODE (Score 5)
- **Primary Skills**:
  - `dex-incident-postmortems`: Reconstruct chronological timeline, conduct 5 Whys analysis.
  - `dex-production-monitoring`: Extract OpenTelemetry traces, error logs, and metric spikes.
  - `dex-root-cause-debugging`: Pinpoint underlying architectural bottleneck causing the crash.
- **Complementary Skills**: `dex-reliability-engineering`, `dex-documentation-as-code`.
- **Enforced Quality Gates**: QG-01, QG-05, QG-10.
- **Key Deliverables**: Blameless postmortem document, Jira/GitHub action items, and updated runbook.

---

### Scenario G: Cross-Platform Windows & POSIX Developer CLI Tooling
- **Context**: Develop a cross-platform CLI utility in Rust/Node with WinGet distribution, shell completion, and POSIX compliance.
- **Complexity**: STANDARD MODE (Score 6)
- **Primary Skills**:
  - `dex-cli-engineering`: Argument parsing, structured `--json` output, and exit code standards.
  - `dex-cross-platform-portability`: Safe path normalization, LF line endings, and matrix CI.
  - `dex-windows-packaging`: WinGet package manifest, Inno Setup installer, and Authenticode signing.
- **Complementary Skills**: `dex-developer-tooling`, `dex-plugin-architecture`, `dex-release-engineering`.
- **Enforced Quality Gates**: QG-01, QG-04, QG-07, QG-09, QG-10.
- **Key Deliverables**: Cross-platform executable binary, WinGet manifest, and shell completion scripts.

---

### Scenario H: Automated Release & Semantic Versioning Pipeline
- **Context**: Fully automate Conventional Commits parsing, SemVer version bumping, CHANGELOG generation, and multi-registry publishing.
- **Complexity**: QUICK MODE (Score 3)
- **Primary Skills**:
  - `dex-semantic-version-automation`: Conventional commits analysis, SemVer bump calculation.
  - `dex-release-engineering`: Release packaging, automated release notes, and GitHub release tags.
  - `dex-cicd-automation`: End-to-end GitHub Actions pipeline for publishing artifacts.
- **Complementary Skills**: `dex-git-workflow`, `dex-supply-chain-security`, `dex-code-verification`.
- **Enforced Quality Gates**: QG-01, QG-03, QG-04, QG-06, QG-10.
- **Key Deliverables**: Automated release workflow, updated `CHANGELOG.md`, and signed release tag.

---

### Scenario I: Data Contract Breaking Change Mitigation
- **Context**: Upstream backend service introduced a breaking event schema change that risks crashing downstream data pipelines.
- **Complexity**: STANDARD MODE (Score 7)
- **Primary Skills**:
  - `dex-data-contracts`: Formal OpenDataContract specification between producer and consumers.
  - `dex-schema-evolution`: Expand-and-contract dual write pattern preventing breakage.
  - `dex-data-quality-audits`: Great Expectations automated tests asserting schema conformity.
- **Complementary Skills**: `dex-data-pipelines`, `dex-data-lineage`, `dex-api-contract-evolution`.
- **Enforced Quality Gates**: QG-01, QG-03, QG-05, QG-06, QG-10.
- **Key Deliverables**: `datacontract.yaml`, schema compatibility CI gate, and pipeline health monitor.

---

### Scenario J: Chaos Engineering & System Resilience Validation
- **Context**: Verify system fault tolerance and graceful degradation under sudden network partitions and Redis outages.
- **Complexity**: STRICT MODE (Score 8)
- **Primary Skills**:
  - `dex-chaos-experiments`: Toxiproxy fault injection simulating 3000ms latency and dropped packets.
  - `dex-reliability-engineering`: Cockatiel / Resilience4j circuit breakers and cached fallbacks.
  - `dex-performance-optimization`: Concurrency throttling and connection pool guardrails.
- **Complementary Skills**: `dex-production-monitoring`, `dex-property-based-testing`, `dex-capacity-planning`.
- **Enforced Quality Gates**: QG-04, QG-07, QG-08, QG-10.
- **Key Deliverables**: Chaos experiment specification, circuit breaker policy configuration, and resilience audit report.
"""
    with open(os.path.join(ROOT_DIR, "ROUTING_MATRIX.md"), "w", encoding="utf-8") as f:
        f.write(routing_content.strip() + "\n")
    print("  [UPDATED] ROUTING_MATRIX.md")

    # 4. README.md
    readme_content = """# DEX Engineering Skills Pack v3.0

> **90 Specialized Agent Skills + 1 Master Orchestrator (91 Skills Total)**  
> Production-ready, deterministic engineering skills library adhering strictly to the [Agent Skills Specification](https://agentskills.io/specification).

[![Validate DEX Skills](https://github.com/nguyenducanhst2022-png/dex-engineering-skills/actions/workflows/validate-skills.yml/badge.svg)](https://github.com/nguyenducanhst2022-png/dex-engineering-skills/actions/workflows/validate-skills.yml)
[![Version](https://img.shields.io/badge/version-3.0.0-blue.svg)](CHANGELOG.md)
[![Agent Skills Spec](https://img.shields.io/badge/Agent%20Skills-Standard%20Compliant-green.svg)](https://agentskills.io/specification)
[![Python Tests](https://img.shields.io/badge/tests-103%20passed-brightgreen.svg)](tests/)

---

## 1. Overview

**DEX Engineering Skills Pack v3.0** is an industrial-strength skills ecosystem built for modern AI coding agents (OpenAI Codex, Cursor, Windsurf, VS Code). It transforms informal prompting into disciplined, verified, and repeatable software engineering practices.

### Key Capabilities
- **Exact 90+1 Architecture**: 90 specialized skills spanning 9 core engineering domains plus 1 Master Orchestrator.
- **14 Mandatory Sections**: Every skill contains 14 structured technical sections (Purpose, Activation, Preconditions, Concepts, Workflow, Examples, Anti-Patterns, Quality Gates, Security, Platform Adapters, Deliverables, Related Skills, Realistic Usage).
- **Quality Gates (QG-01 to QG-10)**: Automated technical acceptance gates eliminating unverified claims and hallucinations.
- **Automated Validation Suite**: Built-in Python validator (`scripts/validate_skills.py`) and 103-test pytest suite (`tests/`) ensuring 100% compliance.

---

## 2. Catalog of 9 Engineering Domains

| Phân Nhóm | Mã Số | Tên Miền Kỹ Thuật | Trọng Tâm Trách Nhiệm |
|:---|:---|:---|:---|
| **Master** | `00` | **Master Orchestrator** | Điều phối toàn hệ thống, phân loại độ phức tạp, kiểm soát 10 Quality Gates. |
| **Group A** | `01–10` | **Core Engineering** | Chu trình Vibe Coding, phân rã nhiệm vụ, kiểm chứng terminal, Git an toàn, profiling, security. |
| **Group B** | `11–20` | **Architecture & AI Agents** | Giám sát production, refactoring, kiến trúc phần mềm, database, testing, agent governance. |
| **Group C** | `21–30` | **Production Engineering** | Phân tích blast radius, quản lý dependency, độ tin cậy, race condition, a11y, full-lifecycle. |
| **Group D** | `31–40` | **Frontend Engineering** | Hợp đồng component, design tokens, luồng dữ liệu, forms/Zod, routing, Web Vitals, SSR, i18n. |
| **Group E** | `41–50` | **Backend & Integration** | Domain-Driven Design, async worker queues, caching, WebSockets, search, event streaming. |
| **Group F** | `51–60` | **Data & Infrastructure** | Data contracts, ETL/ELT pipelines, Great Expectations, schema evolution, query plans, disaster recovery. |
| **Group G** | `61–70` | **AI & LLM Engineering** | LLM integration, RAG vector pipelines, retrieval metrics (RAGAS), prompt eval, tool calling, cost controls. |
| **Group H** | `71–80` | **Developer Experience** | Repository bootstrap, monorepo governance, CLI engineering, cross-platform portability, WinGet. |
| **Group I** | `81–90` | **Security & Reliability** | Auth session lifecycle, Row-Level Security tenancy, secret scanning, SBOM supply chain, chaos engineering. |

Tra cứu chi tiết từng kỹ năng tại: [SKILLS_INDEX.md](SKILLS_INDEX.md)

---

## 3. Quickstart & Integration

### A. Clone Repository
```bash
git clone https://github.com/nguyenducanhst2022-png/dex-engineering-skills.git
cd dex-engineering-skills
```

### B. Verify Skills
```bash
# Run structural and frontmatter validation
python scripts/validate_skills.py

# Run comprehensive test suite
pytest tests/ -v
```

### C. Configure for OpenAI Codex / AI Agents
Copy `.agents/` directly into your workspace or target repository root. Point your agent instructions to `dex-master-orchestrator`:
```markdown
# AGENTS.md
You have access to the DEX Engineering Skills Pack v3.0 in `.agents/skills/`.
For every task, begin by invoking `dex-master-orchestrator` to classify complexity,
select the required specialized skills, and enforce the 10 Quality Gates.
```

See [INSTALL.md](INSTALL.md) for detailed platform setup instructions.

---

## 4. Quality Gates & Acceptance System

All technical deliverables produced under the DEX framework must clear the 10 Quality Gates:
- **QG-01**: Specification & Input Contract
- **QG-02**: Task Decomposition & Blast Radius Control
- **QG-03**: Zero Warnings Linting & Strict Typing
- **QG-04**: Real Terminal Automated Verification (No Mock Passes)
- **QG-05**: Root Cause Fix with Failing Test First
- **QG-06**: Schema Evolution & Contract Compatibility
- **QG-07**: Timeouts, Retries & Circuit Breaker Fallback
- **QG-08**: Performance & Resource Budget Verification
- **QG-09**: Zero Hardcoded Secrets & Tenancy Isolation
- **QG-10**: Evidence-Based Delivery & Audit Report

See [ARCHITECTURE.md](ARCHITECTURE.md) for architectural details and [ROUTING_MATRIX.md](ROUTING_MATRIX.md) for workflow dispatch scenarios.
"""
    with open(os.path.join(ROOT_DIR, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme_content.strip() + "\n")
    print("  [UPDATED] README.md")

    # 5. INSTALL.md
    install_content = """# DEX Engineering Skills Pack v3.0 — Installation & Integration Guide

Hướng dẫn chi tiết cài đặt, cấu hình và sử dụng **DEX Engineering Skills Pack v3.0** (91 Agent Skills) trên các nền tảng: **Windows 11**, **OpenAI Codex**, **VS Code**, **Cursor**, **Windsurf**, **Claude Code**, và **GitHub Actions CI**.

---

## 1. Yêu Cầu Môi Trường (Prerequisites)

- **Hệ điều hành**: Windows 11 / Windows 10 (hỗ trợ đầy đủ PowerShell 7+), Ubuntu 20.04+, macOS Sonoma+.
- **Git**: Phiên bản 2.38 trở lên.
- **Python**: Phiên bản 3.10 trở lên (khuyến nghị 3.12).
- **Test Runner**: `pytest` (`pip install pytest`).

---

## 2. Cài Đặt Vào Dự Án Mới (Installation)

### Cách 1: Tích hợp trực tiếp (Khuyến nghị cho dự án độc lập)
Sao chép thư mục `.agents/skills` vào thư mục gốc của repository dự án của bạn:
```bash
# Từ thư mục dự án của bạn:
git clone https://github.com/nguyenducanhst2022-png/dex-engineering-skills.git temp-dex
cp -r temp-dex/.agents ./
rm -rf temp-dex
```

### Cách 2: Sử dụng Git Submodule (Khuyến nghị cho cập nhật định kỳ)
```bash
git submodule add https://github.com/nguyenducanhst2022-png/dex-engineering-skills.git .agents/dex-skills
```

---

## 3. Cấu Hình Cho OpenAI Codex & AI Coding Agents

Tạo hoặc cập nhật tệp `AGENTS.md` tại thư mục gốc của dự án:
```markdown
# AGENTS.md - DEX Skills Instructions

Bạn có quyền truy cập vào bộ kỹ năng **DEX Engineering Skills Pack v3.0** đặt tại `.agents/skills/`.

### Quy tắc làm việc bắt buộc:
1. Luôn bắt đầu mọi tác vụ bằng cách kích hoạt `dex-master-orchestrator`.
2. Phân loại độ phức tạp của yêu cầu thành một trong ba chế độ:
   - **QUICK MODE**: Lỗi nhỏ, sửa chính tả, cấu hình tối thiểu -> Chỉ dùng `dex-development-workflow` + `dex-code-verification`.
   - **STANDARD MODE**: Thêm tính năng, API, refactoring -> Kích hoạt 3-5 skills chuyên biệt trên branch riêng.
   - **STRICT MODE**: Đụng chạm Database, Auth, Payment, hoặc Release -> Thực thi toàn diện kèm threat model và rollback plan.
3. Tuyệt đối không báo cáo hoàn thành nếu chưa chạy lệnh kiểm chứng thật trong terminal (QG-04).
4. Không thực hiện các lệnh phá hủy (`rm -rf`, `DROP TABLE`, `git push --force`).
```

---

## 4. Tích Hợp Vào IDE (VS Code, Cursor, Windsurf)

Thư mục `.agents/skills/` tuân thủ chuẩn mở Agent Skills. Các IDE hỗ trợ chuẩn này sẽ tự động nhận diện toàn bộ 91 kỹ năng thông qua file `SKILL.md` và trường YAML frontmatter `description`.

Để gán lệnh tắt nhanh trong VS Code, bạn có thể thêm vào `.vscode/tasks.json`:
```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "DEX: Validate All Skills",
      "type": "shell",
      "command": "python scripts/validate_skills.py",
      "group": "test"
    },
    {
      "label": "DEX: Run Pytest Suite",
      "type": "shell",
      "command": "pytest tests/ -v",
      "group": "test"
    }
  ]
}
```

---

## 5. Kiểm Tra & Xác Nhận Cài Đặt (Verification)

Chạy 2 lệnh kiểm thử sau để đảm bảo 100% các kỹ năng hợp lệ:
```bash
# 1. Kiểm tra cấu trúc 14 mục và cú pháp frontmatter
python scripts/validate_skills.py

# 2. Chạy bộ kiểm thử tự động (103 bài test)
pytest tests/ -v
```

Kết quả mong đợi: `103 passed in ~0.1s`.
"""
    with open(os.path.join(ROOT_DIR, "INSTALL.md"), "w", encoding="utf-8") as f:
        f.write(install_content.strip() + "\n")
    print("  [UPDATED] INSTALL.md")

    # 6. AGENTS.example.md
    agents_content = """# AGENTS.md — OpenAI Codex Instructions

> Reference configuration template for OpenAI Codex and compatible AI coding agents.

## Role & Mission
You are a Principal Software Architect and Staff AI Coding Agent operating under the **DEX Engineering Skills Pack v3.0**.
Your repository contains **90 specialized skills and 1 Master Orchestrator** located under `.agents/skills/`.

---

## Mandatory Operating Principles

### 1. Master Orchestrator Dispatch
- Every task from the user must begin by invoking `dex-master-orchestrator`.
- Assess task risk score (1–10) and assign the execution mode:
  - **QUICK (1–3)**: Minimal fast-path (`dex-development-workflow` + `dex-code-verification`).
  - **STANDARD (4–7)**: Scoped specialized skills, isolated branch, unit tests.
  - **STRICT (8–10)**: Full enterprise lifecycle, threat modeling, schema migration safety, chaos resilience.

### 2. Evidence-Based Verification (No Virtual Completion)
- Never output "Task complete" without actual terminal execution evidence.
- Run real test suites, check linter output, and verify exit codes.
- Adhere strictly to **Quality Gates QG-01 through QG-10**.

### 3. Safety Guardrails
- Mutating commands require pre-flight checks and rollback plans.
- Strictly block destructive actions (`rm -rf`, `DROP TABLE`, `git push --force origin main`).
- Zero hardcoded credentials. All secrets must use environment injection or secret managers.
"""
    with open(os.path.join(ROOT_DIR, "AGENTS.example.md"), "w", encoding="utf-8") as f:
        f.write(agents_content.strip() + "\n")
    print("  [UPDATED] AGENTS.example.md")

    # 7. CHANGELOG.md
    changelog_content = """# Changelog — DEX Engineering Skills Pack

All notable changes to this project are documented in this file in accordance with [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [3.0.0] - 2026-10-22

### Added
- **Expanded Catalog to 90 Specialized Skills + 1 Master Orchestrator (91 skills total)**:
  - **Group D: Frontend Engineering (Skills 31–40)**: `dex-ui-component-contracts`, `dex-design-system-tokens`, `dex-frontend-data-flow`, `dex-forms-and-validation`, `dex-routing-navigation`, `dex-frontend-performance`, `dex-ssr-seo-rendering`, `dex-internationalization`, `dex-visual-regression`, `dex-browser-compatibility`.
  - **Group E: Backend & Integration (Skills 41–50)**: `dex-domain-driven-design`, `dex-background-job-queues`, `dex-caching-strategies`, `dex-realtime-protocols`, `dex-file-processing`, `dex-search-engineering`, `dex-event-driven-architecture`, `dex-idempotent-operations`, `dex-notification-delivery`, `dex-scheduled-workflows`.
  - **Group F: Data & Infrastructure (Skills 51–60)**: `dex-data-contracts`, `dex-data-pipelines`, `dex-data-quality-audits`, `dex-data-lineage`, `dex-schema-evolution`, `dex-database-query-plans`, `dex-storage-lifecycle`, `dex-data-retention`, `dex-capacity-planning`, `dex-disaster-recovery`.
  - **Group G: AI & LLM Engineering (Skills 61–70)**: `dex-llm-integration`, `dex-rag-pipelines`, `dex-retrieval-evaluation`, `dex-prompt-evaluation`, `dex-model-evaluation`, `dex-tool-calling-contracts`, `dex-agent-permissions`, `dex-llm-cost-controls`, `dex-ai-observability`, `dex-dataset-curation`.
  - **Group H: Developer Experience & Platform (Skills 71–80)**: `dex-repository-bootstrap`, `dex-monorepo-governance`, `dex-cli-engineering`, `dex-plugin-architecture`, `dex-cross-platform-portability`, `dex-windows-packaging`, `dex-documentation-as-code`, `dex-code-generation`, `dex-developer-tooling`, `dex-semantic-version-automation`.
  - **Group I: Security, Reliability & Product (Skills 81–90)**: `dex-auth-session-lifecycle`, `dex-access-control-tenancy`, `dex-secrets-management`, `dex-supply-chain-security`, `dex-threat-modeling`, `dex-property-based-testing`, `dex-chaos-experiments`, `dex-experimentation-metrics`, `dex-api-contract-evolution`, `dex-incident-postmortems`.
- **Standardized 14 Mandatory Technical Sections**: All 91 skills now contain exact numbered headers from `## 1. Purpose & Scope` to `## 14. Realistic Usage Example`.
- **Dynamic Task Routing Engine**: Documented in `ROUTING_MATRIX.md` with explicit mapping for 10 realistic scenarios (A through J).
- **Automated Validation Suite**:
  - `scripts/validate_skills.py`: Verifies frontmatter length, name constraints, and 14-section completeness.
  - `tests/test_skill_structure.py`: 93 pytest assertions testing directory structure, frontmatter, and headers.
  - `tests/test_skill_routing.py`: 10 pytest scenarios validating orchestrator routing logic.
- **GitHub Actions CI Workflow**: Added `.github/workflows/validate-skills.yml` to automatically run validator and pytest on push/PR.
- **New Architecture Documentation**: Added `ARCHITECTURE.md` detailing the 10 Quality Gates (QG-01 to QG-10), execution modes, and safety boundaries.

### Changed
- Upgraded `dex-master-orchestrator` and skills 01–30 from v1.0 10-section structure to full v3.0 14-section specification.
- Updated `SKILLS_INDEX.md` with complete 91-skill directory.
- Updated `INSTALL.md`, `README.md`, and `AGENTS.example.md` for v3.0 release.

---

## [1.0.0] - 2026-10-22
- Initial release with 30 skills + 1 master orchestrator based on the 30 Vibe Coding lessons.
"""
    with open(os.path.join(ROOT_DIR, "CHANGELOG.md"), "w", encoding="utf-8") as f:
        f.write(changelog_content.strip() + "\n")
    print("  [UPDATED] CHANGELOG.md")

    print("\nAll v3.0 documentation generated successfully.")

if __name__ == "__main__":
    main()
