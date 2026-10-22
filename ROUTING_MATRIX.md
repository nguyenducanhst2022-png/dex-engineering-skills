# DEX Dynamic Routing Matrix v3.0

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


---

### Scenario K: Hermetic Offline Integration Testing & Mock Virtualization
- **Context**: Run integration tests against third-party payments and logistics APIs completely offline without network flakes or rate limits.
- **Complexity**: STANDARD MODE (Score 6)
- **Primary Skills**:
  - `dex-api-mocking-virtualization`: Setup MSW network interceptors and WireMock fault simulations.
  - `dex-testing-engineering`: Execute integration test suite with synthetic fixtures.
  - `dex-api-engineering`: Assert mock response schemas conform strictly to OpenAPI specs.
- **Complementary Skills**: `dex-code-verification`, `dex-cicd-automation`.
- **Enforced Quality Gates**: QG-01, QG-03, QG-04, QG-06, QG-10.
- **Key Deliverables**: Offline mock server configuration, hermetic integration test suite, and schema contract assertion report.

---

### Scenario L: Defensive Binary & Web Bundle Security Auditing
- **Context**: Inspect compiled release executables (PE/ELF) and production JavaScript bundles for exposed endpoints, unmitigated compiler flags, and REA decompilation.
- **Complexity**: STRICT MODE (Score 8)
- **Primary Skills**:
  - `dex-binary-inspection`: Verify ASLR, DEP/NX compiler mitigation flags, and imported DLL dependencies.
  - `dex-javascript-bundle-deobfuscation`: Extract sourcemaps, detect leaked staging endpoints and third-party SDKs.
  - `dex-rea-adapter`: Probe REA MCP availability for decompilation of suspicious native functions.
- **Complementary Skills**: `dex-security-audit`, `dex-threat-modeling`, `dex-incident-postmortems`.
- **Enforced Quality Gates**: QG-01, QG-04, QG-07, QG-09, QG-10.
- **Key Deliverables**: Binary security audit report, bundle exposure catalog, and REA evidence report.
