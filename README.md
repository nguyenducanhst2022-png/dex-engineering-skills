# DEX Engineering Skills Framework v6.0

> **300 Specialized Agent Skills + 1 Master Orchestrator (301 Native DEX Skills Total) + 4 Segregated Upstream Integrations (5 Integration Skills) + SkillOps Lifecycle Suite**  
> Industrial-strength, deterministic agent skills ecosystem adhering strictly to the [Agent Skills Specification](https://agentskills.io/specification).

[![Validate DEX Skills](https://img.shields.io/badge/Validate%20DEX%20Skills-301%2F301%20passed-brightgreen.svg?logo=githubactions&logoColor=white)](https://github.com/nguyenducanhst2022-png/dex-engineering-skills)
[![Version](https://img.shields.io/badge/version-6.0.0-blue.svg)](CHANGELOG.md)
[![Agent Skills Spec](https://img.shields.io/badge/Agent%20Skills-Standard%20Compliant-green.svg)](https://agentskills.io/specification)
[![Python Tests](https://img.shields.io/badge/tests-1001%20passed-brightgreen.svg)](tests/)
[![Routing F1-Score](https://img.shields.io/badge/Routing%20F1-0.903-success.svg)](scripts/evaluate_routing.py)

---

## 1. Overview & Vision

**DEX Engineering Skills Framework v6.0** represents the state of the art in production-ready AI agent capabilities. Designed for modern coding agents (OpenAI Codex, GitHub Copilot, Cursor, Windsurf, Claude Code, and VS Code), DEX converts unstructured agent prompts into disciplined, verifiable, and repeatable software engineering procedures.

### Core Architecture Pillars
- **Strict 300+1 Taxonomy**: Exactly **300 Specialized Skills** organized into 30 distinct engineering domains (Groups A through AD, exactly 10 skills each) plus **1 Master Orchestrator** (`dex-master-orchestrator`), totaling **301 Native DEX Skills** in `.agents/skills/`.
- **Complete SkillOps Toolchain**: A dedicated operations framework in `scripts/` providing automated discovery, security auditing, routing evaluation (F1 >= 0.85), upstream synchronization, and third-party packaging.
- **Segregated Multi-Source Integration**: External capabilities from curated repositories (`sickn33/agentic-awesome-skills`, `zhaoxuya520/reverse-skill`, `morluto/rea`, `nextlevelbuilder/ui-ux-pro-max-skill`) remain completely isolated in `integrations/`, accessible via MCP adapters and manifests without polluting native numbering.
- **14 Mandatory Sections Standard**: Every skill strictly implements all 14 mandatory sections (Purpose, Activation Triggers, Preconditions, Key Concepts, Step-by-Step Workflow, Concrete Examples, Anti-Patterns, Verification Quality Gates, Security & Risk Mitigation, Platform Adapters, Deliverables, Related Skills, Realistic Usage, and Verification Commands). Zero stubs. Zero empty placeholders.
- **15 Quality Gates (QG-01 to QG-15)**: Automated technical acceptance gates enforcing terminal evidence, hermetic reproducibility, and strict boundary safety.
- **Full Pytest Suite**: 1,001 comprehensive automated tests executing across structure, YAML metadata, registry consistency, security screening, DAG dependencies, 30 routing scenarios, and 16 real-world evaluations.

---

## 2. Catalog of 30 Engineering Disciplines (300 Skills + 1 Orchestrator)

| Group | Range | Domain | Focus & Responsibilities |
|:---|:---|:---|:---|
| **Root** | `000` | **Master Orchestrator** | Intelligent request triage, mode selection (QUICK, STANDARD, STRICT), dynamic dispatch across 300 skills, and 15 Quality Gates enforcement. |
| **Group A** | `001–010` | **Core Engineering** | Trunk-based Git workflows, task delegation, terminal verification, code layout, root cause debugging, profiling, security audit, CI/CD, and release engineering. |
| **Group B** | `011–020` | **Architecture & AI Agents** | Production monitoring, technical debt refactoring, software architecture, database engineering, API design, testing engineering, agent engineering, multi-agent orchestration, context engineering, and specification-driven development. |
| **Group C** | `021–030` | **Production Engineering** | Change blast radius analysis, dependency management, reliability engineering, concurrency & state, accessibility, feature flags, code review, acceptance testing, maintenance, and end-to-end engineering. |
| **Group D** | `031–040` | **Frontend Engineering** | UI component contracts, design system tokens, frontend data flow, forms & validation, routing & navigation, web performance, SSR & SEO, internationalization, visual regression, and browser compatibility. |
| **Group E** | `041–050` | **Backend & Integration** | Domain-Driven Design, background job queues, caching strategies, real-time protocols, file processing, search engineering, event-driven architecture, idempotent operations, notification delivery, and scheduled workflows. |
| **Group F** | `051–060` | **Data Engineering** | Data contracts, data pipelines, data quality audits, data lineage, schema evolution, database query plans, storage lifecycle, data retention, capacity planning, and disaster recovery. |
| **Group G** | `061–070` | **AI & LLM Engineering** | LLM integration, RAG pipelines, retrieval evaluation (RAGAS), prompt evaluation, model evaluation, tool calling contracts, agent permissions, token cost controls, AI observability, and dataset curation. |
| **Group H** | `071–080` | **Developer Experience** | Repository bootstrap, monorepo governance, CLI engineering, plugin architecture, cross-platform portability, Windows packaging (WinGet), documentation-as-code, code generation, developer tooling, and semantic versioning. |
| **Group I** | `081–090` | **Security & Reliability** | Auth session lifecycle, multi-tenant access control (RLS), secrets management, supply chain security (SBOM), threat modeling, property-based testing, chaos experiments, experimentation metrics, API contract evolution, and incident postmortems. |
| **Group J** | `091–100` | **Cloud & Infrastructure** | Minimal container image engineering (Trivy/Syft), Kubernetes workload hardening, declarative IaC (Terraform/OpenTofu), cloud service integration (Workload Identity), zero-downtime rollouts (Argo Canary), service mesh networking (Istio mTLS), network troubleshooting, SLO & error budgets, distributed tracing (OpenTelemetry), and cloud cost FinOps. |
| **Group K** | `101–110` | **Mobile & Desktop Engineering** | Modern Android architecture (Compose/MVVM), modern iOS architecture (SwiftUI/Observation), Electron security hardening, lightweight Tauri v2 desktop integration, offline-first sync (CRDT/mutation queue), mobile release pipelines (Fastlane), mobile performance profiling (TTID/Jank), desktop IPC design, native device hardware integration, and desktop update delivery. |
| **Group L** | `111–120` | **Product & Operations Engineering** | Privacy impact assessment (DPIA/GDPR), compliance control mapping (SOC 2/ISO 27001), tamper-evident audit trails (Merkle/WORM), configuration drift reconciliation, structured product discovery (JTBD), quantitative feature prioritization (RICE), analytics instrumentation, high-velocity feedback triage, runbook automation, and operational readiness review (ORR). |
| **Group M** | `121–130` | **Advanced Software Verification** | Mutation survival analysis (mutmut/cargo-mutants), automated flaky test remediation, coverage risk hotspots, differential regression testing, static analysis custom rule authoring (Semgrep/CodeQL), hermetic test data management, formal invariant verification (TLA+/SMT), reproducible benchmarking (Criterion/Hyperfine), API contract fuzzing (Echidna/Atheris), and cross-platform compatibility matrices. |
| **Group N** | `131–140` | **Advanced SRE & Distributed Systems** | High-scale load & stress testing (k6/Locust), adaptive token-bucket rate limiting & quotas, backpressure load shedding, multi-region service failover, distributed data consistency (Saga/2PC), alert noise reduction, log pipeline engineering (Vector/FluentBit), operational game days, metric cardinality control (Mimir/Thanos), and supportability diagnostic tooling. |
| **Group O** | `141–150` | **Advanced Cloud Platform** | Least-privilege Cloud IAM review, internal developer platform service catalogs (Backstage), Kubernetes admission policy enforcement (Kyverno/Gatekeeper), declarative GitOps workflows (ArgoCD/Flux), multi-cloud VPC network topology, serverless function architecture, cloud resource tagging governance, edge runtime deployment (Cloudflare/Fastly), dynamic service discovery (Consul/CoreDNS), and immutable environment promotion. |
| **Group P** | `151–160` | **Language & Runtime Engineering** | Rust unsafe memory auditing, modern C++20 memory safety (RAII/ASan), Node.js event loop diagnostics, Go goroutine concurrency patterns, JVM garbage collection tuning (ZGC/G1), TypeScript strict type safety, C# .NET memory pooling, WebAssembly integration, Python packaging & wheel engineering (UV/Ruff), and multi-language FFI boundary safety contracts. |
| **Group Q** | `161–170` | **Advanced AI Systems** | Model Context Protocol (MCP) server architecture, vector index optimization (HNSW/IVF), cross-encoder reranking strategies, strict JSON schema output enforcement, multi-modal vision/audio pipelines, prompt injection red-teaming & defense, agent evaluation harnesses, hierarchical agent memory governance, semantic grounding & citation audits, and resilient LLM fallback routing. |
| **Group R** | `171–180` | **Product Design & User Research** | User journey friction mapping, automated WCAG 2.2 AA accessibility testing, design token handoff verification, product requirements writing (PRD/RFC), usability benchmark study design, user consent & privacy UX (GDPR/CPRA), information architecture auditing, conversion funnel drop-off analysis, feature adoption cohort tracking, and on-call engineering handover workflows. |
| **Group S** | `181–190` | **Application Security Specialists** | Automated SAST finding triage & remediation, cryptographically signed SBOM verification (In-toto/Cosign), production browser extension CSP hardening, API abuse & credential stuffing defense, cryptographic API & cipher suite review, dynamic AST scoping, offensive security logging & detection, secure CI/CD build runner sandboxing, automated vulnerability patch remediation, and strict web security headers. |
| **Group T** | `191–200` | **SkillOps Engineering** | Skill discovery indexing & catalog sync, AST-based dynamic security screening, automated routing precision & recall benchmarking, upstream source synchronization, skill dependency graph DAG validation, semantic deduplication & overlap scoring, cross-agent host adapters (Codex/Cursor/Claude), automated skill packaging & distribution, semantic activation evaluation, and license provenance audit. |
| **Group U** | `201–210` | **Visual Design Intelligence** | Design brief synthesis, visual reference evaluation, design system documentation, layout composition patterns, color contrast & APCA systems, fluid typography engineering, motion interaction specification, headless UI verification, visual hierarchy audits, and design-to-code QA reviews. |
| **Group V** | `211–220` | **Advanced Web Experiences** | Web animation performance, progressive web apps (PWA), virtualized infinite lists, search interface UX, web push permission flows, Web Canvas rendering, HLS/DASH media playback, frontend error recovery, web permission UX, and cross-origin integration. |
| **Group W** | `221–230` | **Browser Extensions & Automation** | Manifest V3 architecture, background service worker lifecycle, content script DOM isolation, extension message channel security, storage migration, Chrome DevTools Protocol (CDP) observability, browser automation testing, mobile package auditing, Electron artifact analysis, and firmware metadata inspection. |
| **Group X** | `231–240` | **Authorized Reverse Engineering** | PE/COFF and ELF binary header inspection, native symbol table mapping, disassembly CFG reconstruction, managed .NET/Java assembly analysis, JavaScript sourcemap recovery, binary diffing regression detection, hardware firmware metadata, and defensible evidence chain compilation. |
| **Group Y** | `241–250` | **Protocols & Service Integration** | MQTT client reliability & QoS persistence, WebSocket session resumption, timing-safe webhook HMAC validation, HTTP connection pooling & keep-alive, service contract simulation, offline messaging, event schema registries, OAuth 2.0 / OIDC integrations, API pagination cursors, and secret rotation drills. |
| **Group Z** | `251–260` | **AI Agent Operations** | LLM evaluation dataset curation, agent multi-step task planning validation, human-in-the-loop review gates, agent execution trace replay, AI safety red teaming & injection defense, retrieval permission filtering, multimodal evaluation, long-running agent checkpoints, ML data drift monitoring, and inference latency optimization. |
| **Group AA** | `261–270` | **Advanced Data & Analytics** | SQL metric semantic layers, statistical data anomaly detection, columnar data warehouse cost tuning, H3/S2 geospatial data pipelines, event stream processing semantics, feature store engineering, time-series diagnostics, A/B test statistical analysis, backfill data reconciliation, and cohort retention modeling. |
| **Group AB** | `271–280` | **Native, Graphics & Game Engineering** | Chess engine alpha-beta search testing, deterministic fixed-point simulation, game loop frame pacing, WebGPU rendering pipelines, GPU shader performance profiling, real-time input latency reduction, asset pipeline optimization, native plugin ABI testing, physics engine validation, and GPU resource lifetime management. |
| **Group AC** | `281–290` | **Software Trust & Distribution** | Open source license scanning & copyleft detection, cryptographic artifact signature verification, HSM-backed code signing release processes, tamper-evident software update trust chains, bit-for-bit release reproducibility audits, dependency vulnerability intelligence, third-party licensing attribution, maintainer contribution governance, vulnerability disclosure workflows, and media delivery pipelines. |
| **Group AD** | `291–300` | **Advanced SkillOps Governance** | Multi-tier skill catalog taxonomies, SHA256 skill source integrity verification, immutable execution evidence ledgers, automated routing conflict & overlap tests, documentation drift detection, DAG reference graphs, semantic upgrade migrations, multi-variant rollback verification, quantitative skill risk scoring, and skill retirement lifecycle governance. |

---

## 3. Master Orchestrator & Execution Modes

The **DEX Master Orchestrator** (`dex-master-orchestrator`) acts as the top-level cognitive dispatcher. It determines the appropriate skills to activate based on user intent, technical context, and task complexity:

```
[User Request]
       │
       ▼
[dex-master-orchestrator]
       │
       ├─► Analysis: Intent, scope, technical constraints, risk profile
       │
       ├─► Mode Selection:
       │     ├─► QUICK    : Simple bugfixes, docs, single-file edits (QG-01..03)
       │     ├─► STANDARD : Features, refactors, performance, API integrations (QG-01..08)
       │     └─► STRICT   : Infrastructure, database schemas, security, releases (QG-01..15)
       │
       ├─► Dynamic Dispatch: Resolves primary skills & complementary chains (Groups A..AD)
       │
       ├─► Execution: Step-by-step workflow with terminal verification evidence
       │
       └─► Audit Report: Summary of changed files, commands executed, and Quality Gate evidence
```

### Quality Gates (QG-01 to QG-15)
1. **QG-01**: Clean Git tree or explicit stash before destructive changes.
2. **QG-02**: Static syntax and lint verification (zero errors).
3. **QG-03**: Terminal execution verification (real terminal output, no mock claims).
4. **QG-04**: Unit and integration test pass rate 100%.
5. **QG-05**: Code verification and type checking pass.
6. **QG-06**: Security baseline check (no hardcoded secrets or unsafe eval).
7. **QG-07**: Performance budget and resource footprint verification.
8. **QG-08**: Documentation integrity and symbol links verified.
9. **QG-09**: Formal invariant checks and state transition safety.
10. **QG-10**: Distributed consistency and failure mode resilience.
11. **QG-11**: Cloud IAM least-privilege policy review.
12. **QG-12**: Language runtime memory safety and zero undefined behavior.
13. **QG-13**: Prompt injection defense and LLM output schema conformity.
14. **QG-14**: Accessibility (WCAG 2.2 AA) and privacy UX compliance.
15. **QG-15**: SkillOps manifest alignment and provenance tracking.

---

## 4. Segregated Multi-Source Integration Engine

Third-party skills remain isolated in `integrations/` to protect the integrity of the native 300 catalog:

| Upstream Source | Pinned Commit | License | Isolation Directory | Adapter Mechanism |
|:---|:---|:---|:---|:---|
| **Agentic Awesome Skills (AAS)** | `7b4e28f1` | MIT | `integrations/aas/` | Native Spec Mirror |
| **Reverse Skill** | `a3f5c90d` | MIT | `integrations/reverse-skill/` | Defensive CLI Wrappers |
| **Reverse Engineer Anything (REA)**| `c4d12e89` | Apache-2.0 | `integrations/rea/` | MCP Bridge (`dex-rea-adapter`) |
| **UI/UX Pro Max** | `04cfb449` | MIT | `integrations/ui-ux-pro-max/` | CLI Search Bridge (`dex-ui-ux-pro-max-adapter`) |

Tracked in machine-readable format via `manifests/upstream-sources.json`.

---

## 5. Verification & Test Suite

Run the full verification and pytest suite:

```powershell
# 1. Run zero-dependency specification validator (301 native + 5 integrations)
python scripts/validate_pack.py

# 2. Run SkillOps security audit (4 upstream sources)
python scripts/audit_skills.py

# 3. Benchmark dynamic routing accuracy (F1 >= 0.85)
python scripts/evaluate_routing.py

# 4. Execute all 1,001 pytest unit, integration, and evaluation tests
pytest tests/ -v
```

---

## 6. Documentation Quick Links

- **[SKILLS_INDEX.md](SKILLS_INDEX.md)**: Full catalog of all 300 skills + orchestrator + integrations.
- **[ROUTING_MATRIX.md](ROUTING_MATRIX.md)**: 30 end-to-end engineering routing scenarios (A to AD).
- **[ARCHITECTURE.md](ARCHITECTURE.md)**: Detailed system blueprint and SkillOps lifecycle design.
- **[INSTALL.md](INSTALL.md)**: Step-by-step setup for Windows 11, OpenAI Codex, VS Code, and Claude Code.
- **[VALIDATION_REPORT.md](VALIDATION_REPORT.md)**: Complete Quality Gates QG-01 to QG-15 verification report.
- **[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)**: Attribution and licenses for integrated upstream projects.
- **[CHANGELOG.md](CHANGELOG.md)**: Version 6.0.0 release notes and migration details.

---

## 7. License

DEX Engineering Skills Framework is licensed under the [MIT License](LICENSE).
