# DEX Engineering Skills Pack v3.0

> **90 Specialized Agent Skills + 1 Master Orchestrator (91 Skills Total)**  
> Production-ready, deterministic engineering skills library adhering strictly to the [Agent Skills Specification](https://agentskills.io/specification).

[![Validate DEX Skills](https://img.shields.io/badge/Validate%20DEX%20Skills-100%25%20passed-brightgreen.svg?logo=githubactions&logoColor=white)](https://github.com/nguyenducanhst2022-png/dex-engineering-skills)
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
