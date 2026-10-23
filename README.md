# DEX Engineering Skills Framework v8.0

> **400 Specialized Agent Skills + 1 Master Orchestrator (401 Native DEX Skills Total) + 4 Segregated Upstream Integrations (5 Integration Skills) + Polyglot Script Engine (11 Languages) + SkillOps Lifecycle Suite**  
> Industrial-strength, deterministic agent skills ecosystem adhering strictly to the [Agent Skills Specification](https://agentskills.io/specification).

[![Validate DEX Skills](https://img.shields.io/badge/Validate%20DEX%20Skills-401%2F401%20passed-brightgreen.svg?logo=githubactions&logoColor=white)](https://github.com/nguyenducanhst2022-png/dex-engineering-skills)
[![Version](https://img.shields.io/badge/version-8.0.0-blue.svg)](CHANGELOG.md)
[![Agent Skills Spec](https://img.shields.io/badge/Agent%20Skills-Standard%20Compliant-green.svg)](https://agentskills.io/specification)
[![Python Tests](https://img.shields.io/badge/tests-1360%20passed-brightgreen.svg)](tests/)
[![Routing F1-Score](https://img.shields.io/badge/Routing%20F1-0.927-success.svg)](scripts/evaluate_routing.py)

---

## 1. Overview & Vision

**DEX Engineering Skills Framework v8.0** represents the state of the art in production-ready AI agent capabilities. Designed for modern coding agents (OpenAI Codex, GitHub Copilot, Cursor, Windsurf, Claude Code, and VS Code), DEX converts unstructured agent prompts into disciplined, verifiable, and repeatable software engineering procedures.

### Core Architecture Pillars
- **Strict 400+1 Taxonomy**: Exactly **400 Specialized Skills** organized into 40 distinct canonical engineering domains (Groups A through AN, exactly 10 skills each) plus **1 Master Orchestrator** (`dex-master-orchestrator`), totaling **401 Native DEX Skills** in `.agents/skills/`.
- **DEX Polyglot Script Engine v8.0**: Unified automation runtime supporting **11 programming languages** (Python, TypeScript, JavaScript, PowerShell, Bash, Rust, Go, C++, C#, Java, PHP) with standardized JSON execution envelopes (`result.schema.json`), dry-run execution, timeout controls, output truncation guards, and automated toolchain absence fallback (`TOOL_NOT_AVAILABLE`).
- **Complete SkillOps Toolchain**: Dedicated operations framework in `scripts/` providing automated discovery, AST security screening, routing accuracy benchmarking (F1 = 0.927), upstream synchronization, and evidence ledger logging.
- **Segregated Multi-Source Integration**: External capabilities from curated repositories (`sickn33/agentic-awesome-skills`, `zhaoxuya520/reverse-skill`, `morluto/rea`, `nextlevelbuilder/ui-ux-pro-max-skill`) remain strictly isolated in `integrations/`, accessible via MCP adapters and manifests without polluting native numbering.
- **14 Mandatory Sections Standard**: Every skill strictly implements all 14 mandatory sections (Purpose & Scope, When to Use, When NOT to Use, Prerequisites & Input Context, Core Concepts & Taxonomy, Step-by-Step Execution Workflow, Concrete Examples, Anti-Patterns & Common Traps, Quality Gates & Acceptance Criteria, Security & Safety Boundaries, Platform Adapters, Deliverables & Output Artifacts, Related & Complementary Skills, and Realistic Usage Example). Zero stubs. Zero empty placeholders.
- **15 Quality Gates (QG-01 to QG-15)**: Automated technical acceptance gates enforcing terminal evidence, hermetic reproducibility, and strict boundary safety.
- **Full Pytest Suite**: 1,360 comprehensive automated tests executing across structure, YAML metadata, registry consistency, security screening, DAG dependencies, 40 routing scenarios, and 28 real-world evaluations.

---

## 2. Catalog of 40 Engineering Disciplines (400 Skills + 1 Orchestrator)

| Group | Range | Domain | Focus & Responsibilities |
|:---|:---|:---|:---|
| **Root** | `000` | **Master Orchestrator** | Intelligent request triage, mode selection (QUICK, STANDARD, STRICT), dynamic dispatch across 400 skills, Polyglot engine coordination, and 15 Quality Gates enforcement. |
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
| **Group AE** | `301–310` | **Enterprise Architecture & Migration** | Architecture Decision Records (MADR), modular monolith bounded contexts, saga compensation workflows, CQRS projection management, multi-region data residency, tenant provisioning lifecycles, legacy strangler migration, public API deprecation policies, configuration schema design, and contract-first API development. |
| **Group AF** | `311–320` | **Advanced Distributed Systems** | Exactly-once stream claims auditing, message poison queue & DLQ recovery, distributed lock lease safety, scheduler misfire recovery, regional outage simulation exercises, partition fault simulation, event replay safety, consumer lag mitigation, hot partition dampening, and distributed clock skew resilience. |
| **Group AG** | `321–330` | **Applied AI & Foundation Model Systems** | Embedding dataset curation & chunking, hybrid dense/sparse search fusion (RRF), RAG index freshness control, context window budgeting, agent tool output sanitization, model output probability calibration, AI feedback labeling workflows, prompt versioning experiments, inference provider rate controls, and human-AI collaborative workflow design. |
| **Group AH** | `331–340` | **Extended Polyglot Engineering** | Kotlin Multiplatform build orchestration, Swift modern concurrency review, Dart/Flutter state lifecycle debugging, Ruby Gem engineering, PHP framework hardening, Scala effect systems, Elixir OTP supervision trees, Zig native build engineering, Lua embedding safety, and shell portability testing across platforms. |
| **Group AI** | `341–350` | **Advanced UI/UX & Specialized Interfaces** | Design token migration (W3C DTCG), component state visual matrices, typography scale localization, high-density dashboard layouts, gesture interaction accessibility (WCAG 2.5), RTL/BiDi bidirectional layout readiness, animation storyboard specifications, accessible chart visualizations, perceived performance engineering, and cross-platform UI parity. |
| **Group AJ** | `351–360` | **Authorized Software & System Inspection** | Binary provenance matching (SLSA), debug symbols correlation (PDB/DWARF), toolchain reproducibility audits, installer package static review (MSI/PKG), SBOM-to-binary correlation, mobile permission surface diffing, JavaScript bundle obfuscation audits, macOS entitlements review, firmware image structure diffing, and defensible reverse engineering reporting. |
| **Group AK** | `361–370` | **ML Platform & Production Engineering** | Online-offline feature parity, training data leakage audits, model serving canary rollouts, ML experiment reproducibility (DVC), data label quality assessment (Cleanlab), batch inference pipeline tuning, vector embedding migration, real-time analytics windowing, metadata catalog lineage, and data masking with synthetic generation. |
| **Group AL** | `371–380` | **Developer Platform & Polyglot Tooling** | Developer workstation bootstrapping, toolchain version pinning (mise), polyglot build orchestration, build cache integrity, cross-language contract tests (Pact), reproducible devcontainers, CLI command contract specifications, Windows/Linux path compatibility, package publishing preflights, and monorepo template conformance. |
| **Group AM** | `381–390` | **Advanced Application & Infrastructure Security** | Secretless CI/CD authentication (OIDC), ephemeral test credential lifecycle (Vault), container runtime isolation (gVisor/Kata), API authorization matrix testing (BOLA/BOPLA), privacy-safe observability, DNS/TLS certificate monitoring, incident forensic evidence preservation (WORM), SaaS risk surface reviews, dependency update risk scoring, and service account governance. |
| **Group AN** | `391–400` | **SkillOps Quality, Governance & Interoperability** | Skill catalog reconciliation, Agent Skills specification compatibility, skill example test fixtures, instruction injection security testing, runtime capability probing, semantic routing evaluations, upstream license diffing, cross-platform release matrices, skill quality scorecards, and execution sandbox policies. |

---

## 3. DEX Polyglot Script Engine v8.0

The **Polyglot Script Engine** provides deterministic multi-language execution and automation across 11 programming languages:

```
scripts/polyglot/
├── core/
│   ├── result_schema.py    # Structured JSON contract (exit_code, stdout, stderr, execution_time_ms)
│   ├── security.py         # Path traversal defense, secret redaction, destructive command blocking
│   ├── executor.py         # Safe subprocess execution (shell=False, 512KB cap, timeout enforcement)
│   ├── detector.py         # Workspace language scanner & confidence scoring
│   ├── registry.py         # Adapter registration and discovery
│   ├── reporting.py        # Text, JSON, and Markdown formatters
│   └── generator.py        # Code and companion test scaffolding
├── adapters/
│   ├── base.py             # Base adapter interface with dry-run support
│   ├── python.py           # Python 3 / Pytest / Ruff adapter
│   ├── typescript.py       # TypeScript / Node / Jest adapter
│   ├── javascript.py       # JavaScript / Node / Vitest adapter
│   ├── powershell.py       # PowerShell 5.1 / Pwsh adapter
│   ├── bash.py             # Bash / POSIX shell adapter
│   ├── rust.py             # Rust / Cargo / Clippy adapter
│   ├── go.py               # Go / Go test / GolangCI-Lint adapter
│   ├── cpp.py              # C++ / CMake / Clang adapter
│   ├── csharp.py           # C# / .NET SDK adapter
│   ├── java.py             # Java / Maven / Gradle adapter
│   └── php.py              # PHP / Composer / PHPUnit adapter
├── wrappers/
│   ├── dex.ps1             # PowerShell entry point
│   ├── dex.bat             # Windows CMD entry point
│   └── dex.sh              # POSIX Bash entry point
├── schemas/
│   └── result.schema.json  # JSON schema for execution results
├── tests/                  # 37 automated tests across 6 modules
└── dex.py                  # Unified CLI orchestrator
```

### CLI Command Reference
```powershell
# Check framework status and detected languages
python scripts/polyglot/dex.py status

# Perform comprehensive toolchain diagnostics
python scripts/polyglot/dex.py doctor

# Run type checking across detected or specified languages
python scripts/polyglot/dex.py typecheck --lang python

# Execute unit and integration tests
python scripts/polyglot/dex.py test --lang python

# Perform static security audit and secret screening
python scripts/polyglot/dex.py audit

# Generate code scaffolding with companion tests
python scripts/polyglot/dex.py generate --lang typescript --name auth-middleware
```

---

## 4. Master Orchestrator & Execution Modes

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
       │     └─► STRICT   : Infrastructure, distributed systems, security, releases (QG-01..15)
       │
       ├─► Dynamic Dispatch: Resolves primary skills & complementary chains (Groups A..AN)
       │
       ├─► Polyglot Engine: Executes build, test, and lint tasks across 11 languages
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

## 5. Segregated Multi-Source Integration Engine

Third-party skills remain isolated in `integrations/` to protect the integrity of the native 400 catalog:

| Upstream Source | Pinned Commit | License | Isolation Directory | Adapter Mechanism |
|:---|:---|:---|:---|:---|
| **Agentic Awesome Skills (AAS)** | `7b4e28f1` | MIT | `integrations/agentic-awesome-skills/` | Native Spec Mirror (`dex-api-mocking-virtualization`) |
| **Reverse Skill** | `a3f5c90d` | MIT | `integrations/reverse-skill/` | Defensive CLI Wrappers (`dex-binary-inspection`, `dex-javascript-bundle-deobfuscation`) |
| **Reverse Engineer Anything (REA)**| `c4d12e89` | Apache-2.0 | `integrations/rea/` | MCP Bridge (`dex-rea-adapter`) |
| **UI/UX Pro Max** | `04cfb449` | MIT | `integrations/ui-ux-pro-max/` | CLI Search Bridge (`dex-ui-ux-pro-max-adapter`) |

Tracked in machine-readable format via `manifests/upstream-sources.json`.

---

## 6. Verification & Test Suite

Run the full verification and pytest suite:

```powershell
# 1. Run zero-dependency specification validator (401 native + 5 integrations)
python scripts/validate_pack.py

# 2. Run SkillOps security audit (401 native skills + 4 upstream sources)
python scripts/audit_skills.py

# 3. Benchmark dynamic routing accuracy across 40 groups (F1 >= 0.85)
python scripts/evaluate_routing.py

# 4. Run Polyglot Engine CLI diagnostics
python scripts/polyglot/dex.py doctor

# 5. Execute all 1,360 pytest unit, integration, polyglot, and evaluation tests
pytest tests/ scripts/polyglot/tests/ -v
```

---

## 7. Documentation Quick Links

- **[SKILLS_INDEX.md](SKILLS_INDEX.md)**: Full catalog of all 400 skills + orchestrator + integrations.
- **[ROUTING_MATRIX.md](ROUTING_MATRIX.md)**: 40 end-to-end engineering routing scenarios (A to AN).
- **[ARCHITECTURE.md](ARCHITECTURE.md)**: Detailed system blueprint, Polyglot Engine, and SkillOps lifecycle design.
- **[INSTALL.md](INSTALL.md)**: Step-by-step setup for Windows 11, OpenAI Codex, VS Code, and Claude Code.
- **[VALIDATION_REPORT.md](VALIDATION_REPORT.md)**: Complete Quality Gates QG-01 to QG-15 verification report.
- **[THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)**: Attribution and licenses for integrated upstream projects.
- **[CHANGELOG.md](CHANGELOG.md)**: Version 8.0.0 release notes and migration details.

---

## 8. License

DEX Engineering Skills Framework is licensed under the [MIT License](LICENSE).
