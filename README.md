# DEX Engineering Skills Pack v4.0

> **120 Specialized Agent Skills + 1 Master Orchestrator (121 DEX Skills Total) + Multi-Source Skill Integration Framework**  
> Production-ready, deterministic engineering skills library adhering strictly to the [Agent Skills Specification](https://agentskills.io/specification).

[![Validate DEX Skills](https://img.shields.io/badge/Validate%20DEX%20Skills-100%25%20passed-brightgreen.svg?logo=githubactions&logoColor=white)](https://github.com/nguyenducanhst2022-png/dex-engineering-skills)
[![Version](https://img.shields.io/badge/version-4.0.0-blue.svg)](CHANGELOG.md)
[![Agent Skills Spec](https://img.shields.io/badge/Agent%20Skills-Standard%20Compliant-green.svg)](https://agentskills.io/specification)
[![Python Tests](https://img.shields.io/badge/tests-passed-brightgreen.svg)](tests/)

---

## 1. Overview

**DEX Engineering Skills Pack v4.0** is an industrial-strength agent skills ecosystem designed for modern AI coding agents (OpenAI Codex, Cursor, Windsurf, Claude Code, VS Code). It transforms ad-hoc prompting into disciplined, verified, and repeatable software engineering practices across the entire software development lifecycle.

### Key Capabilities
- **Exact 120+1 Architecture**: Exactly **120 Specialized Skills** spanning 12 distinct engineering domains (Groups A through L) plus **1 Master Orchestrator** (`dex-master-orchestrator`), totaling **121 Native DEX Skills** in `.agents/skills/`.
- **Segregated Multi-Source Integration Engine**: Upstream skills imported from external sources (`sickn33/agentic-awesome-skills`, `zhaoxuya520/reverse-skill`, `morluto/rea`) are cleanly isolated in `integrations/` and tracked via manifest without inflating the native 120 catalog.
- **14 Mandatory Sections Standard**: Every skill strictly contains the 14 mandatory sections (Purpose, Activation, Preconditions, Concepts, Workflow, Examples, Anti-Patterns, Quality Gates, Security, Platform Adapters, Deliverables, Related Skills, Realistic Usage) with zero stubs or placeholders.
- **12 Quality Gates (QG-01 to QG-12)**: Automated technical acceptance gates eliminating unverified claims, hallucinated passes, and scope creep.
- **Automated Validation Suite**: Zero-dependency Python validator (`scripts/validate_skills.py`) and pytest suite (`tests/`) ensuring 100% compliance.

---

## 2. Catalog of 12 Engineering Disciplines (120 Skills)

| Group | Range | Domain | Focus & Responsibilities |
|:---|:---|:---|:---|
| **Root** | `00` | **Master Orchestrator** | Intelligent request triage, mode selection (QUICK, STANDARD, STRICT), dynamic dispatch, 12 Quality Gates enforcement. |
| **Group A** | `01–10` | **Core Engineering** | Vibe Coding workflow, task delegation, terminal verification, Git workflows, code layout, root cause debugging, profiling, security audit, CI/CD, release engineering. |
| **Group B** | `11–20` | **Architecture & AI Agents** | Production monitoring, technical debt refactoring, software architecture, database engineering, API design, testing engineering, agent engineering, multi-agent orchestration, context engineering, specification-driven dev. |
| **Group C** | `21–30` | **Production Engineering** | Blast radius analysis, dependency management, reliability engineering, concurrency & state, a11y, feature flags, code review, acceptance testing, maintenance, end-to-end engineering. |
| **Group D** | `31–40` | **Frontend Engineering** | UI component contracts, design system tokens, frontend data flow, forms & validation, routing & navigation, web performance, SSR & SEO, internationalization, visual regression, browser compatibility. |
| **Group E** | `41–50` | **Backend & Integration** | Domain-Driven Design, background job queues, caching strategies, real-time protocols, file processing, search engineering, event-driven architecture, idempotent operations, notification delivery, scheduled workflows. |
| **Group F** | `51–60` | **Data Engineering** | Data contracts, data pipelines, data quality audits, data lineage, schema evolution, database query plans, storage lifecycle, data retention, capacity planning, disaster recovery. |
| **Group G** | `61–70` | **AI & LLM Engineering** | LLM integration, RAG pipelines, retrieval evaluation (RAGAS), prompt evaluation, model evaluation, tool calling contracts, agent permissions, token cost controls, AI observability, dataset curation. |
| **Group H** | `71–80` | **Developer Experience** | Repository bootstrap, monorepo governance, CLI engineering, plugin architecture, cross-platform portability, Windows packaging (WinGet), documentation-as-code, code generation, developer tooling, semantic versioning. |
| **Group I** | `81–90` | **Security & Reliability** | Auth session lifecycle, multi-tenant access control (RLS), secrets management, supply chain security (SBOM), threat modeling, property-based testing, chaos experiments, experimentation metrics, API contract evolution, incident postmortems. |
| **Group J** | `91–100` | **Cloud & Infrastructure** | Minimal container image engineering (Trivy/Syft), Kubernetes workload hardening, declarative IaC (Terraform/OpenTofu), cloud service integration (Workload Identity), zero-downtime rollouts (Argo Canary), service mesh networking (Istio mTLS), network troubleshooting, SLO & error budgets, distributed tracing (OpenTelemetry), cloud cost FinOps. |
| **Group K** | `101–110` | **Mobile & Desktop** | Modern Android architecture (Compose/MVVM), modern iOS architecture (SwiftUI/Observation), Electron security hardening, lightweight Tauri v2 desktop integration, offline-first sync (CRDT/mutation queue), mobile release pipelines (Fastlane), mobile performance profiling (TTID/Jank), desktop IPC design, native device hardware integration, desktop update delivery. |
| **Group L** | `111–120` | **Product & Operations** | Privacy impact assessment (DPIA/GDPR), compliance control mapping (SOC 2/ISO 27001), tamper-evident audit trails (Merkle/WORM), configuration drift reconciliation, structured product discovery (JTBD), quantitative feature prioritization (RICE), analytics instrumentation, high-velocity feedback triage, runbook automation, operational readiness review (ORR). |

Tra cứu danh mục chi tiết kèm liên kết từng kỹ năng tại: [SKILLS_INDEX.md](SKILLS_INDEX.md)

---

## 3. Segregated Multi-Source Integration Framework

DEX maintains a dedicated integration engine (`scripts/dex_skill_importer.py`) to systematically discover, audit, deduplicate, and import external capabilities without cluttering native numbering:
- **Source A (Agentic Awesome Skills)**: `https://github.com/sickn33/agentic-awesome-skills`
- **Source B (Reverse Skill)**: `https://github.com/zhaoxuya520/reverse-skill`
- **Source C (Reverse Engineer Anything - REA)**: `https://github.com/morluto/rea`

### Segregated Integration Modules (`integrations/`):
- [`integrations/aas/dex-api-mocking-virtualization`](integrations/aas/dex-api-mocking-virtualization/SKILL.md): Hermetic API mocking, WireMock, Mock Service Worker (MSW).
- [`integrations/reverse-skill/dex-binary-inspection`](integrations/reverse-skill/dex-binary-inspection/SKILL.md): Defensive static PE/ELF header analysis, ASLR/DEP validation.
- [`integrations/reverse-skill/dex-javascript-bundle-deobfuscation`](integrations/reverse-skill/dex-javascript-bundle-deobfuscation/SKILL.md): Web/Electron bundle auditing and sourcemap reconstruction.
- [`integrations/rea/dex-rea-adapter`](integrations/rea/dex-rea-adapter/SKILL.md): Model Context Protocol (MCP) bridge to the local REA reverse engineering engine.

### Integration CLI Usage:
```bash
# Discover candidates from upstream sources
python scripts/dex_skill_importer.py discover

# Audit security, secrets, and licenses
python scripts/dex_skill_importer.py audit --candidate dex-binary-inspection

# Check duplicate classification against DEX catalog
python scripts/dex_skill_importer.py compare --candidate dex-binary-inspection

# Probe REA MCP environment availability
python scripts/rea_mcp_probe.py --check
```

---

## 4. Quickstart & Integration

### A. Clone Repository
```bash
git clone https://github.com/nguyenducanhst2022-png/dex-engineering-skills.git
cd dex-engineering-skills
```

### B. Verify 121 Skills
```bash
# Run structural and frontmatter validation
python scripts/validate_skills.py

# Run comprehensive test suite
pytest tests/ -v
```

### C. Configure for AI Coding Agents
Copy `.agents/` directly into your workspace or target repository root. Point your agent instructions to `dex-master-orchestrator`:
```markdown
# AGENTS.md
You have access to the DEX Engineering Skills Pack in `.agents/skills/`.
For every task, begin by invoking `dex-master-orchestrator` to classify complexity,
select the required specialized skills from Groups A through L, and enforce the 12 Quality Gates.
```

---

## 5. Documentation & Architecture Reference

- [ARCHITECTURE.md](ARCHITECTURE.md): Multi-layer orchestrator architecture and routing mechanics.
- [SKILLS_INDEX.md](SKILLS_INDEX.md): Index of all 120 specialized skills with direct links and descriptions.
- [ROUTING_MATRIX.md](ROUTING_MATRIX.md): 16 end-to-end scenarios covering all engineering disciplines.
- [INSTALL.md](INSTALL.md): Installation and setup guide for Windows 11, Codex, and CI/CD.
- [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md): Upstream attribution, licenses, and provenance.
- [CHANGELOG.md](CHANGELOG.md): Detailed release notes for v4.0.0.

---

## 6. License

Distributed under the [MIT License](LICENSE).
