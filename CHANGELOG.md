# Changelog — DEX Engineering Skills Pack

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
