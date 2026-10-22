# Changelog — DEX Engineering Skills Framework

All notable changes to the DEX Engineering Skills Framework will be documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [5.0.0] - 2026-10-22

### Major Architecture Upgrade: 200 Specialized Skills + Full SkillOps Lifecycle Suite

#### Added
- **80 New Specialized Skills across Groups M through T (Skills 121–200)**:
  - **Group M (Skills 121–130) — Advanced Software Verification**: `dex-mutation-testing`, `dex-flaky-test-remediation`, `dex-coverage-risk-analysis`, `dex-differential-testing`, `dex-static-analysis-rule-authoring`, `dex-test-data-management`, `dex-formal-invariant-checks`, `dex-reproducible-benchmarking`, `dex-api-fuzz-testing`, `dex-compatibility-matrix-testing`.
  - **Group N (Skills 131–140) — Advanced SRE & Distributed Systems**: `dex-load-and-stress-testing`, `dex-rate-limiting-quotas`, `dex-traffic-shaping-backpressure`, `dex-service-failover`, `dex-distributed-consistency`, `dex-alert-quality-engineering`, `dex-log-pipeline-design`, `dex-operational-game-days`, `dex-metric-cardinality-control`, `dex-supportability-engineering`.
  - **Group O (Skills 141–150) — Advanced Cloud Platform**: `dex-cloud-iam-policy-review`, `dex-platform-service-catalog`, `dex-kubernetes-policy-enforcement`, `dex-gitops-workflows`, `dex-cloud-network-design`, `dex-serverless-architecture`, `dex-cloud-resource-tagging`, `dex-edge-runtime-engineering`, `dex-service-discovery`, `dex-environment-promotion`.
  - **Group P (Skills 151–160) — Specialized Language & Runtime Engineering**: `dex-rust-unsafe-audit`, `dex-cpp-memory-safety`, `dex-nodejs-runtime-diagnostics`, `dex-go-concurrency-patterns`, `dex-jvm-performance-diagnostics`, `dex-typescript-type-safety`, `dex-dotnet-application-engineering`, `dex-webassembly-integration`, `dex-python-project-engineering`, `dex-ffi-boundary-contracts`.
  - **Group Q (Skills 161–170) — Advanced AI Systems**: `dex-mcp-server-design`, `dex-vector-index-design`, `dex-reranking-strategies`, `dex-structured-llm-output`, `dex-multimodal-input-pipelines`, `dex-prompt-injection-defense`, `dex-agent-evaluation-harness`, `dex-agent-memory-governance`, `dex-grounding-citation-audit`, `dex-llm-fallback-routing`.
  - **Group R (Skills 171–180) — Product Design & User Research**: `dex-user-journey-mapping`, `dex-accessibility-automation`, `dex-design-handoff-verification`, `dex-product-requirements-writing`, `dex-usability-study-design`, `dex-user-consent-ux`, `dex-information-architecture`, `dex-conversion-funnel-analysis`, `dex-feature-adoption-analysis`, `dex-oncall-handover`.
  - **Group S (Skills 181–190) — Application Security Specialists**: `dex-sast-finding-triage`, `dex-sbom-verification`, `dex-browser-extension-hardening`, `dex-api-abuse-prevention`, `dex-cryptographic-api-review`, `dex-dast-scoping`, `dex-security-logging-detection`, `dex-secure-build-runners`, `dex-vulnerability-remediation`, `dex-web-security-headers`.
  - **Group T (Skills 191–200) — SkillOps Engineering**: `dex-skill-discovery-indexer`, `dex-skill-security-screening`, `dex-skill-quality-benchmarking`, `dex-skill-upstream-sync`, `dex-skill-dependency-graph`, `dex-skill-semantic-deduplication`, `dex-skill-host-adapters`, `dex-skill-import-packaging`, `dex-skill-activation-evaluation`, `dex-skill-license-provenance`.
- **Master Orchestrator v5.0 Upgrade (`dex-master-orchestrator`)**:
  - Comprehensive 20-group routing coverage across 200 skills.
  - Three execution modes: `QUICK`, `STANDARD`, `STRICT`.
  - Quality Gates expanded from 12 to 15 (QG-01 to QG-15).
- **SkillOps Management CLI Suite in `scripts/`**:
  - `discover_skills.py`: Full catalog indexing & taxonomy alignment.
  - `audit_skills.py`: AST-based security screening & spec compliance (0 Critical, 0 High).
  - `evaluate_routing.py`: Dynamic routing precision & recall benchmarking harness (F1 = 0.854 across 20 scenarios).
  - `sync_upstream.py`: Upstream source provenance and pinned commit verification.
  - `import_skills.py`: Third-party skill packaging and rollback manager.
  - `validate_pack.py`: Fast zero-dependency spec validator.
- **Machine-Readable Manifests in `manifests/`**:
  - `dex-skills.json`: Complete canonical catalog of 201 native skills + 5 segregated integrations.
  - `upstream-sources.json`: Pinned commits and licenses for AAS, Reverse Skill, REA, and UI/UX Pro Max.
- **UI/UX Pro Max Integration (`integrations/ui-ux-pro-max/`)**:
  - Integrated NextLevelBuilder UI/UX Pro Max design intelligence engine (MIT License, pinned commit `04cfb449`).
  - Added `dex-ui-ux-pro-max-adapter` with 12 search domains and 22 framework-specific implementation stacks.
  - Built hybrid runtime bridge `scripts/ui_ux_pro_max_runner.py` with zero-pip dependencies.
- **Pytest Suite Expansion**:
  - Total tests expanded from 645 to 659 tests (100% PASS in 1.27s).
  - New test module: `test_ui_ux_pro_max.py` (14 comprehensive integration tests).

#### Changed
- Enforced strict 14-section layout across all 200 specialized skills.
- Isolated upstream integration skills into `integrations/` to guarantee native 200 catalog integrity.

---

## [4.0.0] - 2026-10-22

### 120 Specialized Skills + Master Orchestrator + Segregated Multi-Source Integration
- Added 30 new specialized skills across Groups J, K, and L.
- Implemented `scripts/dex_skill_importer.py` for external repository import.
- Pinned upstream sources: AAS, Reverse Skill, and REA.
