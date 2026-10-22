# DEX Engineering Skills Framework v5.0 — Architectural Specification

> **Principal Architecture Blueprint for 200 Specialized Skills + Master Orchestrator + SkillOps Framework**

---

## 1. System Topology & Directory Structure

DEX v5.0 is organized into three strictly separated tiers: Native Skills Catalog, Segregated Integrations, and SkillOps Toolchain.

```
dex-engineering-skills/
├── .agents/skills/                    # Native DEX Catalog (Exactly 201 skills)
│   ├── dex-master-orchestrator/       # Master Control Plane (Skill 000)
│   ├── dex-development-workflow/      # Skill 001 (Group A)
│   │   └── SKILL.md                   # 14 Mandatory Sections
│   └── ...                            # Skills 002 to 200 (Groups A to T)
├── integrations/                      # Segregated Third-Party Upstream Integrations
│   ├── aas/                           # Agentic Awesome Skills (MIT)
│   ├── reverse-skill/                 # Reverse Skill (MIT)
│   └── rea/                           # Reverse Engineer Anything (Apache-2.0, MCP Adapter)
├── manifests/                         # Machine-Readable Catalog Registry
│   ├── dex-skills.json                # Complete metadata index of 201 native skills
│   └── upstream-sources.json          # Pinned commits and licensing for upstream repos
├── scripts/                           # SkillOps Lifecycle Toolchain
│   ├── discover_skills.py             # Catalog indexing and taxonomy normalization
│   ├── audit_skills.py                # Static AST and security screening (QG-06, QG-15)
│   ├── evaluate_routing.py            # Dynamic routing accuracy benchmark (F1 >= 0.85)
│   ├── sync_upstream.py               # Upstream provenance verification
│   ├── import_skills.py               # Packaging and rollback engine
│   └── validate_pack.py               # Zero-dependency specification validator
├── tests/                             # Comprehensive Pytest Test Suite (645 tests)
│   ├── test_skill_structure.py        # Validates directory and file presence
│   ├── test_skill_metadata.py         # Validates YAML frontmatter conformity
│   ├── test_skill_registry.py         # Asserts exact 200+1 counts and group taxonomy
│   ├── test_skill_security.py         # Screens against unsafe tokens and injection
│   ├── test_skill_dependencies.py     # DAG cycle detection and dangling links
│   └── test_skill_routing.py          # 20-scenario routing matrix validation
└── docs/                              # Framework Specifications & Audit Trails
```

---

## 2. 20-Group Domain Taxonomy (Groups A through T)

Every specialized skill belongs to exactly one domain group with exactly 10 skills per group:

| Domain Group | Focus | Skills Range |
|:---|:---|:---|
| **Group A: Core Engineering** | Trunk-based Git, code layout, root-cause debugging, CI/CD | `001–010` |
| **Group B: Architecture & AI Agents** | Multi-agent orchestration, context engineering, architecture | `011–020` |
| **Group C: Production Engineering** | Blast radius, dependency management, reliability, feature flags | `021–030` |
| **Group D: Frontend Engineering** | Performance, visual regression, design tokens, forms validation | `031–040` |
| **Group E: Backend & Integration** | DDD, event-driven systems, idempotent operations, job queues | `041–050` |
| **Group F: Data Engineering** | Data contracts, pipelines, schema evolution, query optimization | `051–060` |
| **Group G: AI & LLM Engineering** | RAG pipelines, RAGAS retrieval eval, token cost optimization | `061–070` |
| **Group H: Developer Experience** | Monorepo governance, CLI engineering, semantic versioning | `071–080` |
| **Group I: Security & Reliability** | STRIDE threat modeling, secrets management, supply chain SBOM | `081–090` |
| **Group J: Cloud & Infrastructure** | Unprivileged OCI images, Kubernetes rollouts, IaC, FinOps | `091–100` |
| **Group K: Mobile & Desktop** | Offline-first sync, Android/iOS architecture, Tauri desktop | `101–110` |
| **Group L: Product & Operations** | Compliance mapping, audit trails, operational readiness reviews | `111–120` |
| **Group M: Advanced Verification** | Mutation testing, flaky test remediation, invariant verification | `121–130` |
| **Group N: Advanced SRE** | High-scale load testing, rate limiting quotas, backpressure | `131–140` |
| **Group O: Advanced Cloud Platform** | Least-privilege IAM review, GitOps workflows, Kubernetes policy | `141–150` |
| **Group P: Language & Runtime** | Rust unsafe audit, C++ memory safety, Node/JVM diagnostics | `151–160` |
| **Group Q: Advanced AI Systems** | MCP servers, vector indices, structured JSON schemas | `161–170` |
| **Group R: Product Design & UX** | User journey maps, WCAG accessibility, design token handoff | `171–180` |
| **Group S: Application Security** | SAST triage, signed SBOMs, browser extension CSP hardening | `181–190` |
| **Group T: SkillOps Engineering** | Catalog indexing, security screening, routing F1 evaluation | `191–200` |

---

## 3. Dynamic Skill Routing & Execution Pipeline

The Master Orchestrator resolves requests into execution DAGs based on:
1. **Keyword & Semantic Parsing**: Matches incoming terms with skill triggers.
2. **Domain Boundary Mapping**: Identifies the primary discipline (Groups A to T).
3. **Execution Mode Assignment**:
   - `QUICK`: Single-file bugfixes, small tasks (Gates QG-01 to QG-03).
   - `STANDARD`: Feature implementation, refactoring (Gates QG-01 to QG-08).
   - `STRICT`: Production infra, security, database, or releases (Gates QG-01 to QG-15).
4. **DAG Topological Sort**: Dispatches prerequisite skills before downstream dependents.
5. **Quality Gate Verification**: Blocks progress if terminal evidence or tests fail.

---

## 4. Security & Isolation Architecture

DEX enforces strict defense-in-depth security:
- **No Unsafe Execution**: SKILL.md files never execute arbitrary code; they specify deterministic agent workflows.
- **Air-Gapped Operation**: Native skills require zero network connectivity during static evaluation.
- **AST Security Screening**: Automated AST scanner (`scripts/audit_skills.py`) detects and blocks dangerous shell tokens (`curl | sh`, `rm -rf /`, `eval(...)`).
- **Segregated Third-Party Upstream**: External code resides in `integrations/` with pinned SHA-1 commits and independent licenses.
