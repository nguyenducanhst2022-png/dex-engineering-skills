# DEX Engineering Skills Catalog Index (v6.0.0)

> Complete index of all **300 Specialized Engineering Skills** + **1 Master Orchestrator** (301 Native Skills) and **5 Segregated Integrations**.  
> Every skill strictly complies with the [Agent Skills Specification](https://agentskills.io/specification).

---

## 1. Master Orchestrator (Root Control Plane)

| ID | Name | Description | Path |
|:---|:---|:---|:---|
| `dex-master-orchestrator` | Master Orchestrator | Central control plane for dynamic triage, execution mode selection (QUICK, STANDARD, STRICT), 30-group routing, and 15 Quality Gates enforcement. | [dex-master-orchestrator](.agents/skills/dex-master-orchestrator/SKILL.md) |

---

## 2. Specialized Engineering Skills Catalog (300 Skills)

### Group A: Core Engineering (Skills 001–010)

| # | Skill ID | Description | Path |
|:---|:---|:---|:---|
| `001` | **`dex-development-workflow`** | Standard iterative development workflow for AI coding. | [dex-development-workflow](.agents/skills/dex-development-workflow/SKILL.md) |
| `002` | **`dex-task-delegation`** | Structure and delegate engineering tasks clearly to AI coding agents with defined goals, explicit scope boundaries, technical constraints, verification criteria, and reporting standards. | [dex-task-delegation](.agents/skills/dex-task-delegation/SKILL.md) |
| `003` | **`dex-code-verification`** | Rigorous code verification and quality assurance protocol for AI-generated code. | [dex-code-verification](.agents/skills/dex-code-verification/SKILL.md) |
| `004` | **`dex-git-workflow`** | Professional Git version control and safe upgrade workflow. | [dex-git-workflow](.agents/skills/dex-git-workflow/SKILL.md) |
| `005` | **`dex-code-organization`** | Clean project structuring and modular codebase organization. | [dex-code-organization](.agents/skills/dex-code-organization/SKILL.md) |
| `006` | **`dex-root-cause-debugging`** | Root cause analysis and deterministic bug resolution methodology. | [dex-root-cause-debugging](.agents/skills/dex-root-cause-debugging/SKILL.md) |
| `007` | **`dex-performance-optimization`** | Metrics-driven software performance profiling, bottleneck detection, algorithmic optimization, and benchmark verification. | [dex-performance-optimization](.agents/skills/dex-performance-optimization/SKILL.md) |
| `008` | **`dex-security-audit`** | Static and dynamic software security auditing, vulnerability classification, OWASP Top 10 mitigation, secret scanning, and patch verification. | [dex-security-audit](.agents/skills/dex-security-audit/SKILL.md) |
| `009` | **`dex-cicd-automation`** | Continuous Integration and Continuous Delivery (CI/CD) pipeline design, configuration, and automated test orchestration. | [dex-cicd-automation](.agents/skills/dex-cicd-automation/SKILL.md) |
| `010` | **`dex-release-engineering`** | Structured software release management, semantic versioning (SemVer), artifact packaging, automated changelog generation, and rollback planning. | [dex-release-engineering](.agents/skills/dex-release-engineering/SKILL.md) |

### Group AA: Advanced Data & Analytics (Skills 261–270)

| # | Skill ID | Description | Path |
|:---|:---|:---|:---|
| `261` | **`dex-sql-metric-semantic-layer`** | Engineer reusable business metric semantic layers (Cube, dbt Semantic Layer, MetricFlow) defining standardized dimensions, measures, time grains, and access policies. | [dex-sql-metric-semantic-layer](.agents/skills/dex-sql-metric-semantic-layer/SKILL.md) |
| `262` | **`dex-time-series-diagnostics`** | Diagnose temporal gaps, irregular sampling frequencies, seasonal trend decomposition (STL), stationarity violations, and sensor drift in high-volume time-series data. | [dex-time-series-diagnostics](.agents/skills/dex-time-series-diagnostics/SKILL.md) |
| `263` | **`dex-data-anomaly-detection`** | Engineer real-time and batch data anomaly detection systems with statistical z-score/IQR baselines, Isolation Forests, dynamic adaptive thresholds, and alert dampening. | [dex-data-anomaly-detection](.agents/skills/dex-data-anomaly-detection/SKILL.md) |
| `264` | **`dex-feature-store-engineering`** | Architect enterprise feature stores (Feast, Hopsworks) with dual online/offline storage synchronization, point-in-time correct join queries, feature definitions as code, and latency SLA guarantees. | [dex-feature-store-engineering](.agents/skills/dex-feature-store-engineering/SKILL.md) |
| `265` | **`dex-analytics-cohort-retention`** | Engineer scalable user retention cohort matrices, churn decay curves, lifetime value (LTV) projections, and behavioral cohort segmentation in SQL. | [dex-analytics-cohort-retention](.agents/skills/dex-analytics-cohort-retention/SKILL.md) |
| `266` | **`dex-ab-test-statistical-analysis`** | Conduct rigorous A/B test statistical analyses, verifying Sample Ratio Mismatch (SRM), applying two-tailed hypothesis tests, CUPED variance reduction, and sequential testing bounds. | [dex-ab-test-statistical-analysis](.agents/skills/dex-ab-test-statistical-analysis/SKILL.md) |
| `267` | **`dex-geospatial-data-pipelines`** | Architect high-throughput geospatial data pipelines using Uber H3 discrete global grids, Google S2 geometry, PostGIS spatial indexing, and GeoJSON/WKB serialization. | [dex-geospatial-data-pipelines](.agents/skills/dex-geospatial-data-pipelines/SKILL.md) |
| `268` | **`dex-data-warehouse-cost-tuning`** | Analyze and optimize BigQuery, Snowflake, and Databricks query compute costs, partition pruning, clustering strategies, slot reservations, and auto-suspend warehouse policies. | [dex-data-warehouse-cost-tuning](.agents/skills/dex-data-warehouse-cost-tuning/SKILL.md) |
| `269` | **`dex-backfill-reconciliation`** | Orchestrate safe, idempotent historical data backfills across partitioned analytical tables, verifying pre/post row counts, metric parity reconciliations, and preventing downstream cascade corruptions. | [dex-backfill-reconciliation](.agents/skills/dex-backfill-reconciliation/SKILL.md) |
| `270` | **`dex-machine-learning-data-drift`** | Monitor and quantify covariate feature drift and concept drift in production ML pipelines using Population Stability Index (PSI), Kolmogorov-Smirnov (KS) tests, and Wasserstein distance metrics. | [dex-machine-learning-data-drift](.agents/skills/dex-machine-learning-data-drift/SKILL.md) |

### Group AB: Native, Graphics & Game Engineering (Skills 271–280)

| # | Skill ID | Description | Path |
|:---|:---|:---|:---|
| `271` | **`dex-chess-engine-search-testing`** | Design deterministic search verification suites for chess engines and tree search algorithms, verifying perft move generation correctness, alpha-beta pruning invariants, transposition table hits, and quiescence stability. | [dex-chess-engine-search-testing](.agents/skills/dex-chess-engine-search-testing/SKILL.md) |
| `272` | **`dex-simulation-determinism`** | Engineer bit-level deterministic simulation loops using fixed-point arithmetic, isolated PRNG streams, and zero-float divergence across heterogeneous OS architectures (Windows/Linux/macOS). | [dex-simulation-determinism](.agents/skills/dex-simulation-determinism/SKILL.md) |
| `273` | **`dex-physics-engine-validation`** | Validate 2D/3D rigid-body physics engines, measuring energy conservation invariants, continuous collision detection (CCD) tunneling prevention, solver constraint stability, and restitution accuracy. | [dex-physics-engine-validation](.agents/skills/dex-physics-engine-validation/SKILL.md) |
| `274` | **`dex-game-loop-timing`** | Implement rock-solid game loop architectures with fixed timestep physics updates, accumulator buffer smoothing, variable frame rendering interpolation, and spiral-of-death panics. | [dex-game-loop-timing](.agents/skills/dex-game-loop-timing/SKILL.md) |
| `275` | **`dex-rendering-frame-pacing`** | Diagnose frame time variance, 1% low FPS, pipeline presentation latencies, and display VSync synchronization glitches. | [dex-rendering-frame-pacing](.agents/skills/dex-rendering-frame-pacing/SKILL.md) |
| `276` | **`dex-gpu-shader-profiling`** | Profile and optimize vertex, fragment, and compute shaders, minimizing register pressure, arithmetic intensity bottlenecks, texture bandwidth stalls, and branch divergence. | [dex-gpu-shader-profiling](.agents/skills/dex-gpu-shader-profiling/SKILL.md) |
| `277` | **`dex-gpu-resource-lifetime`** | Architect robust GPU memory allocators and resource lifetime managers across Vulkan, DirectX 12, and Metal, eliminating VRAM leaks, staging buffer stalls, and handling graphics device loss. | [dex-gpu-resource-lifetime](.agents/skills/dex-gpu-resource-lifetime/SKILL.md) |
| `278` | **`dex-native-plugin-abi-testing`** | Design cross-language C Foreign Function Interface (FFI) boundary tests, verifying struct memory layouts, calling conventions, string encoding boundaries, and pointer ownership transfer. | [dex-native-plugin-abi-testing](.agents/skills/dex-native-plugin-abi-testing/SKILL.md) |
| `279` | **`dex-real-time-input-latency`** | Diagnose and minimize end-to-end user input latency, raw input device polling, OS event pump queuing, render pipeline latency, and display scanout synchronization. | [dex-real-time-input-latency](.agents/skills/dex-real-time-input-latency/SKILL.md) |
| `280` | **`dex-asset-pipeline-optimization`** | Architect modern game and graphics asset compilation pipelines with GPU texture compression (BC1-7, ASTC, KTX2/Basis Universal), mesh level-of-detail (LOD) simplification, and streaming bundles. | [dex-asset-pipeline-optimization](.agents/skills/dex-asset-pipeline-optimization/SKILL.md) |

### Group AC: Software Trust & Distribution (Skills 281–290)

| # | Skill ID | Description | Path |
|:---|:---|:---|:---|
| `281` | **`dex-open-source-license-scanning`** | Automate open-source software (OSS) license compliance scanning, detecting copyleft contamination (GPL/AGPL), dual-licensing clauses, and license incompatibility risks across dependency trees. | [dex-open-source-license-scanning](.agents/skills/dex-open-source-license-scanning/SKILL.md) |
| `282` | **`dex-third-party-attribution`** | Generate accurate, legally compliant NOTICE and THIRD_PARTY_NOTICES files, aggregating copyright statements, author credits, and license texts from vendored dependencies. | [dex-third-party-attribution](.agents/skills/dex-third-party-attribution/SKILL.md) |
| `283` | **`dex-artifact-signature-verification`** | Implement cryptographic artifact signing and verification workflows using Sigstore (Cosign), GPG, and transparency logs (Rekor). | [dex-artifact-signature-verification](.agents/skills/dex-artifact-signature-verification/SKILL.md) |
| `284` | **`dex-dependency-vulnerability-intelligence`** | Triage and remediate software dependency vulnerabilities using OSV, NVD, and GitHub Advisory databases, prioritizing by Exploit Prediction Scoring System (EPSS), CISA KEV catalogs, and call-graph reachability analysis. | [dex-dependency-vulnerability-intelligence](.agents/skills/dex-dependency-vulnerability-intelligence/SKILL.md) |
| `285` | **`dex-secret-rotation-drills`** | Design zero-downtime secret rotation drills for database credentials, API signing keys, JWT secrets, and TLS certificates using dual-key overlaps and automated validation. | [dex-secret-rotation-drills](.agents/skills/dex-secret-rotation-drills/SKILL.md) |
| `286` | **`dex-code-signing-release-process`** | Establish automated, tamper-proof code signing pipelines for Windows Authenticode, macOS Notarization, and Linux GPG packages using Hardware Security Modules (HSM) and cloud key management. | [dex-code-signing-release-process](.agents/skills/dex-code-signing-release-process/SKILL.md) |
| `287` | **`dex-software-update-trust-chains`** | Architect secure software auto-update trust frameworks incorporating The Update Framework (TUF) principles, cryptographic manifest verification, downgrade attack prevention, and differential binary patches. | [dex-software-update-trust-chains](.agents/skills/dex-software-update-trust-chains/SKILL.md) |
| `288` | **`dex-vulnerability-disclosure-workflows`** | Establish standardized Coordinated Vulnerability Disclosure (CVD) workflows, drafting security. | [dex-vulnerability-disclosure-workflows](.agents/skills/dex-vulnerability-disclosure-workflows/SKILL.md) |
| `289` | **`dex-maintainer-contribution-governance`** | Establish open-source maintainer governance, automated CODEOWNERS enforcement, Contributor License Agreements (CLA/DCO), PR review checklists, and branch protection rules. | [dex-maintainer-contribution-governance](.agents/skills/dex-maintainer-contribution-governance/SKILL.md) |
| `290` | **`dex-release-reproducibility-audit`** | Audit and enforce bit-for-bit reproducible builds using diffoscope, containerized build environments, SOURCE_DATE_EPOCH timestamps, and deterministic compiler flags. | [dex-release-reproducibility-audit](.agents/skills/dex-release-reproducibility-audit/SKILL.md) |

### Group AD: Advanced SkillOps Governance (Skills 291–300)

| # | Skill ID | Description | Path |
|:---|:---|:---|:---|
| `291` | **`dex-skill-catalog-taxonomy`** | Govern multi-tier Agent Skill catalog taxonomies, classifying skills across domain groups (A-AD), capability primitives, operational risk levels, and progressive disclosure scopes. | [dex-skill-catalog-taxonomy](.agents/skills/dex-skill-catalog-taxonomy/SKILL.md) |
| `292` | **`dex-skill-source-integrity`** | Verify cryptographic source integrity, Git commit tree hashes, upstream tracking, and license attributions for imported and native skills. | [dex-skill-source-integrity](.agents/skills/dex-skill-source-integrity/SKILL.md) |
| `293` | **`dex-skill-risk-scoring`** | Quantify operational, security, and privilege risk scores for Agent Skills based on tool access, filesystem mutation scope, network egress, and execution authority. | [dex-skill-risk-scoring](.agents/skills/dex-skill-risk-scoring/SKILL.md) |
| `294` | **`dex-skill-reference-graph`** | Construct and validate the bidirectional cross-skill reference graph across all 300 skills, detecting broken relative links, orphaned skills, circular delegation deadlocks, and missing prerequisite relationships. | [dex-skill-reference-graph](.agents/skills/dex-skill-reference-graph/SKILL.md) |
| `295` | **`dex-skill-routing-conflict-tests`** | Design automated semantic disambiguation and routing conflict test suites, probing borderline intent prompts across overlapping skill domains to guarantee deterministic triage. | [dex-skill-routing-conflict-tests](.agents/skills/dex-skill-routing-conflict-tests/SKILL.md) |
| `296` | **`dex-skill-execution-evidence-ledger`** | Establish tamper-evident JSONL execution evidence ledgers recording real terminal commands, exit codes, stdout/stderr captures, and cryptographic checksums for skill quality validation. | [dex-skill-execution-evidence-ledger](.agents/skills/dex-skill-execution-evidence-ledger/SKILL.md) |
| `297` | **`dex-skill-documentation-drift`** | Detect, quantify, and reconcile documentation drift between executable CLI scripts, manifest registries, and markdown specification files across the skill framework. | [dex-skill-documentation-drift](.agents/skills/dex-skill-documentation-drift/SKILL.md) |
| `298` | **`dex-skill-upgrade-migrations`** | Orchestrate automated breaking change migrations for Agent Skills across framework versions, transforming deprecated frontmatter schemas, section reorganizations, and API adapters with compatibility shims. | [dex-skill-upgrade-migrations](.agents/skills/dex-skill-upgrade-migrations/SKILL.md) |
| `299` | **`dex-skill-rollback-verification`** | Design deterministic rollback procedures, state restoration drills, and backup verification for skill deployments, guaranteeing zero-downtime recovery from flawed skill updates. | [dex-skill-rollback-verification](.agents/skills/dex-skill-rollback-verification/SKILL.md) |
| `300` | **`dex-skill-retirement-governance`** | Govern the graceful deprecation, sunsetting, and archival lifecycle of obsolete Agent Skills, decoupling downstream dependencies, redirecting semantic intents, and maintaining historical provenance. | [dex-skill-retirement-governance](.agents/skills/dex-skill-retirement-governance/SKILL.md) |

### Group B: Architecture & AI Agents (Skills 011–020)

| # | Skill ID | Description | Path |
|:---|:---|:---|:---|
| `011` | **`dex-production-monitoring`** | Production observability, structured logging, application health checks, alerting thresholds, error telemetry, and post-deployment stability monitoring. | [dex-production-monitoring](.agents/skills/dex-production-monitoring/SKILL.md) |
| `012` | **`dex-technical-debt-refactoring`** | Systematic technical debt assessment, safe code refactoring, code smell eradication, and behavioral preservation. | [dex-technical-debt-refactoring](.agents/skills/dex-technical-debt-refactoring/SKILL.md) |
| `013` | **`dex-software-architecture`** | Software architectural design, component decomposition, modular boundary definition, and architectural decision records (ADRs). | [dex-software-architecture](.agents/skills/dex-software-architecture/SKILL.md) |
| `014` | **`dex-database-engineering`** | Database engineering, relational schema design, safe migrations, index optimization, ACID transaction management, and automated backup strategies. | [dex-database-engineering](.agents/skills/dex-database-engineering/SKILL.md) |
| `015` | **`dex-api-engineering`** | Production-grade API design, RESTful and GraphQL specifications, input schema validation, authentication middleware, error standardization, and backward compatibility contracts. | [dex-api-engineering](.agents/skills/dex-api-engineering/SKILL.md) |
| `016` | **`dex-testing-engineering`** | Comprehensive automated testing engineering, test plan formulation, unit testing, integration testing, end-to-end (E2E) testing, regression suites, and boundary analysis. | [dex-testing-engineering](.agents/skills/dex-testing-engineering/SKILL.md) |
| `017` | **`dex-agent-engineering`** | Autonomous AI coding agent behavior regulation, self-planning, bounded autonomous execution, and transparent verification reporting. | [dex-agent-engineering](.agents/skills/dex-agent-engineering/SKILL.md) |
| `018` | **`dex-multi-agent-orchestration`** | Multi-agent coordination, role division, concurrent subagent task execution, cross-agent peer reviews, and conflict-free code integration. | [dex-multi-agent-orchestration](.agents/skills/dex-multi-agent-orchestration/SKILL.md) |
| `019` | **`dex-context-engineering`** | AI context optimization, persistent project memory architecture, documentation governance, and context relevance filtering. | [dex-context-engineering](.agents/skills/dex-context-engineering/SKILL.md) |
| `020` | **`dex-specification-driven`** | Specification-Driven Development (SDD) methodology. | [dex-specification-driven](.agents/skills/dex-specification-driven/SKILL.md) |

### Group C: Production Engineering (Skills 021–030)

| # | Skill ID | Description | Path |
|:---|:---|:---|:---|
| `021` | **`dex-change-impact-analysis`** | Blast radius estimation, dependency mapping, regression risk assessment, and pre-modification impact analysis. | [dex-change-impact-analysis](.agents/skills/dex-change-impact-analysis/SKILL.md) |
| `022` | **`dex-dependency-management`** | Deterministic dependency management, lockfile synchronization, runtime environment isolation, vulnerability scanning, and package bloat auditing. | [dex-dependency-management](.agents/skills/dex-dependency-management/SKILL.md) |
| `023` | **`dex-reliability-engineering`** | System resilience, fault tolerance, graceful degradation, circuit breakers, timeout deadlines, and exponential backoff retry patterns. | [dex-reliability-engineering](.agents/skills/dex-reliability-engineering/SKILL.md) |
| `024` | **`dex-concurrency-state`** | Concurrency control, distributed locks, race condition elimination, atomic state transitions, and deadlock prevention. | [dex-concurrency-state](.agents/skills/dex-concurrency-state/SKILL.md) |
| `025` | **`dex-ux-accessibility`** | User experience (UX) engineering, responsive design, accessibility (a11y) compliance (WCAG 2. | [dex-ux-accessibility](.agents/skills/dex-ux-accessibility/SKILL.md) |
| `026` | **`dex-feature-flags`** | Feature flags engineering, progressive delivery, staged canary rollouts, kill switches, and flag cleanup lifecycles. | [dex-feature-flags](.agents/skills/dex-feature-flags/SKILL.md) |
| `027` | **`dex-code-review`** | Comprehensive Git diff code review, Pull Request assessment, quality gate validation, and constructive feedback generation. | [dex-code-review](.agents/skills/dex-code-review/SKILL.md) |
| `028` | **`dex-acceptance-testing`** | User Acceptance Testing (UAT), end-user journey simulation, acceptance criteria verification, and product acceptance reporting. | [dex-acceptance-testing](.agents/skills/dex-acceptance-testing/SKILL.md) |
| `029` | **`dex-software-maintenance`** | Long-term software maintenance, application lifecycle management, dependency upgrade roadmaps, technical debt prioritization, and deprecation policies. | [dex-software-maintenance](.agents/skills/dex-software-maintenance/SKILL.md) |
| `030` | **`dex-end-to-end-engineering`** | Full-lifecycle end-to-end software engineering meta-workflow integrating all 29 DEX engineering skills. | [dex-end-to-end-engineering](.agents/skills/dex-end-to-end-engineering/SKILL.md) |

### Group D: Frontend Engineering (Skills 031–040)

| # | Skill ID | Description | Path |
|:---|:---|:---|:---|
| `031` | **`dex-ui-component-contracts`** | Define and enforce strict UI component contracts, TypeScript props interfaces, component state boundaries, and accessible slots. | [dex-ui-component-contracts](.agents/skills/dex-ui-component-contracts/SKILL.md) |
| `032` | **`dex-design-system-tokens`** | Manage design system tokens, typography scales, color palettes, spacing units, and dark mode theming variables across web platforms. | [dex-design-system-tokens](.agents/skills/dex-design-system-tokens/SKILL.md) |
| `033` | **`dex-frontend-data-flow`** | Architect unidirectional frontend state management, server cache synchronization, optimistic UI updates, and normalized client stores. | [dex-frontend-data-flow](.agents/skills/dex-frontend-data-flow/SKILL.md) |
| `034` | **`dex-forms-and-validation`** | Build accessible, performant frontend forms with schema-based validation (Zod/Yup), controlled/uncontrolled inputs, dirty state tracking, and inline error feedback. | [dex-forms-and-validation](.agents/skills/dex-forms-and-validation/SKILL.md) |
| `035` | **`dex-routing-navigation`** | Architect single-page and multi-page routing, route guards, nested layouts, scroll restoration, code-splitting, and deep linking. | [dex-routing-navigation](.agents/skills/dex-routing-navigation/SKILL.md) |
| `036` | **`dex-frontend-performance`** | Profile and optimize Core Web Vitals (LCP, FID/INP, CLS), JavaScript bundle size, image assets, DOM size, and client-side rendering bottlenecks. | [dex-frontend-performance](.agents/skills/dex-frontend-performance/SKILL.md) |
| `037` | **`dex-ssr-seo-rendering`** | Implement Server-Side Rendering (SSR), Static Site Generation (SSG), Incremental Static Regeneration (ISR), dynamic Open Graph metadata, structured JSON-LD, and hydration error eradication. | [dex-ssr-seo-rendering](.agents/skills/dex-ssr-seo-rendering/SKILL.md) |
| `038` | **`dex-internationalization`** | Implement robust internationalization (i18n), localized number/currency formatting (L10n), pluralization rules, RTL layout support, and translation key management. | [dex-internationalization](.agents/skills/dex-internationalization/SKILL.md) |
| `039` | **`dex-visual-regression`** | Automate visual regression testing, pixel-diff comparisons, responsive viewport snapshots, and UI baseline management with Playwright/Percy. | [dex-visual-regression](.agents/skills/dex-visual-regression/SKILL.md) |
| `040` | **`dex-browser-compatibility`** | Ensure cross-browser CSS and JavaScript compatibility across Chrome, Safari, Firefox, Edge, and iOS WebKit. | [dex-browser-compatibility](.agents/skills/dex-browser-compatibility/SKILL.md) |

### Group E: Backend & Integration (Skills 041–050)

| # | Skill ID | Description | Path |
|:---|:---|:---|:---|
| `041` | **`dex-domain-driven-design`** | Implement Domain-Driven Design (DDD) tactical patterns: Entities, Value Objects, Aggregates, Domain Events, Repositories, and Clean Architecture boundaries. | [dex-domain-driven-design](.agents/skills/dex-domain-driven-design/SKILL.md) |
| `042` | **`dex-background-job-queues`** | Architect robust background job processing with message queues (BullMQ/Celery/Sidekiq), dead-letter queues (DLQ), rate limiting, worker concurrency, and progress tracking. | [dex-background-job-queues](.agents/skills/dex-background-job-queues/SKILL.md) |
| `043` | **`dex-caching-strategies`** | Implement multi-layer caching strategies (Cache-Aside, Write-Through, Write-Behind), TTL expirations, cache stampede mitigation, and Redis clustering. | [dex-caching-strategies](.agents/skills/dex-caching-strategies/SKILL.md) |
| `044` | **`dex-realtime-protocols`** | Architect realtime communication protocols (WebSockets, Server-Sent Events, WebRTC, Long Polling), connection lifecycles, heartbeat pings, and reconnection backoffs. | [dex-realtime-protocols](.agents/skills/dex-realtime-protocols/SKILL.md) |
| `045` | **`dex-file-processing`** | Implement streaming multipart file uploads, chunked uploads, magic-byte validation, secure cloud storage (S3/GCS), and virus scanning. | [dex-file-processing](.agents/skills/dex-file-processing/SKILL.md) |
| `046` | **`dex-search-engineering`** | Design full-text search, semantic search, inverted index optimization, faceted filtering, and autocomplete using Elasticsearch, Meilisearch, or PostgreSQL tsvector. | [dex-search-engineering](.agents/skills/dex-search-engineering/SKILL.md) |
| `047` | **`dex-event-driven-architecture`** | Architect event-driven distributed systems, pub/sub topologies, event schemas, Outbox Pattern, message brokers (Kafka/RabbitMQ), and consumer error handling. | [dex-event-driven-architecture](.agents/skills/dex-event-driven-architecture/SKILL.md) |
| `048` | **`dex-idempotent-operations`** | Design strictly idempotent API endpoints, distributed idempotency keys, duplicate request filtering, and atomic token reservations. | [dex-idempotent-operations](.agents/skills/dex-idempotent-operations/SKILL.md) |
| `049` | **`dex-notification-delivery`** | Architect multi-channel notification systems (Email, SMS, Push, In-app), dynamic templating, delivery providers (SendGrid/Twilio/FCM), rate limiting, and failure fallbacks. | [dex-notification-delivery](.agents/skills/dex-notification-delivery/SKILL.md) |
| `050` | **`dex-scheduled-workflows`** | Architect scheduled cron workflows, distributed recurring jobs, time-zone handling, missed-execution recovery, and distributed schedule locks. | [dex-scheduled-workflows](.agents/skills/dex-scheduled-workflows/SKILL.md) |

### Group F: Data Engineering (Skills 051–060)

| # | Skill ID | Description | Path |
|:---|:---|:---|:---|
| `051` | **`dex-data-contracts`** | Define and enforce data contracts between data producers and data consumers, schema validation, semantic change alerts, and SLA guarantees. | [dex-data-contracts](.agents/skills/dex-data-contracts/SKILL.md) |
| `052` | **`dex-data-pipelines`** | Architect scalable data pipelines, batch ETL/ELT workflows, stream processing (Kafka/Spark/Flink), idempotent data transformations, and stateful DAGs with Airflow/Dagster. | [dex-data-pipelines](.agents/skills/dex-data-pipelines/SKILL.md) |
| `053` | **`dex-data-quality-audits`** | Implement automated data quality testing, Great Expectations suites, anomaly detection, nullability audits, and statistical distributions. | [dex-data-quality-audits](.agents/skills/dex-data-quality-audits/SKILL.md) |
| `054` | **`dex-data-lineage`** | Track and visualize data lineage, metadata graphs, column-level provenance, impact analysis, and OpenLineage/Marquez integrations. | [dex-data-lineage](.agents/skills/dex-data-lineage/SKILL.md) |
| `055` | **`dex-schema-evolution`** | Manage backward and forward schema evolution for Avro, Protobuf, JSON Schema, and relational databases. | [dex-schema-evolution](.agents/skills/dex-schema-evolution/SKILL.md) |
| `056` | **`dex-database-query-plans`** | Analyze and optimize database execution plans using EXPLAIN ANALYZE, detect Seq Scans, eliminate temporary spills, tune index strategies, and benchmark SQL queries. | [dex-database-query-plans](.agents/skills/dex-database-query-plans/SKILL.md) |
| `057` | **`dex-storage-lifecycle`** | Architect object storage tiering, lifecycle transition policies, cold-storage archiving (Glacier/Archive), and multipart retention on AWS S3 / Cloudflare R2. | [dex-storage-lifecycle](.agents/skills/dex-storage-lifecycle/SKILL.md) |
| `058` | **`dex-data-retention`** | Implement data retention policies, automated PII data purging, soft-delete lifecycles, hard-delete schedules, and GDPR/CCPA right-to-be-forgotten compliance. | [dex-data-retention](.agents/skills/dex-data-retention/SKILL.md) |
| `059` | **`dex-capacity-planning`** | Calculate infrastructure resource forecasting, load modeling, database IOPS projection, horizontal autoscaling thresholds, and peak traffic planning. | [dex-capacity-planning](.agents/skills/dex-capacity-planning/SKILL.md) |
| `060` | **`dex-disaster-recovery`** | Architect Disaster Recovery (DR) strategies, RPO/RTO SLAs, multi-region replication, automated database failover, and cold/warm backup drills. | [dex-disaster-recovery](.agents/skills/dex-disaster-recovery/SKILL.md) |

### Group G: AI & LLM Engineering (Skills 061–070)

| # | Skill ID | Description | Path |
|:---|:---|:---|:---|
| `061` | **`dex-llm-integration`** | Integrate Large Language Model APIs (OpenAI, Anthropic, Gemini, local Ollama), structured JSON outputs, streaming responses, fallback model routing, and token usage optimization. | [dex-llm-integration](.agents/skills/dex-llm-integration/SKILL.md) |
| `062` | **`dex-rag-pipelines`** | Architect Retrieval-Augmented Generation (RAG) pipelines, semantic chunking strategies, vector embeddings, hybrid search (dense + sparse BM25), re-ranking, and context window assembly. | [dex-rag-pipelines](.agents/skills/dex-rag-pipelines/SKILL.md) |
| `063` | **`dex-retrieval-evaluation`** | Evaluate information retrieval quality in RAG systems using Hit Rate, Mean Reciprocal Rank (MRR), NDCG, Context Relevance, and Ragas metrics. | [dex-retrieval-evaluation](.agents/skills/dex-retrieval-evaluation/SKILL.md) |
| `064` | **`dex-prompt-evaluation`** | Systematic prompt engineering, automated prompt evaluation, regression testing for prompts, few-shot optimization, and LLM-as-a-judge scoring frameworks. | [dex-prompt-evaluation](.agents/skills/dex-prompt-evaluation/SKILL.md) |
| `065` | **`dex-model-evaluation`** | Benchmark and evaluate foundation LLMs and fine-tuned models on task-specific datasets, measuring accuracy, latency, cost per token, and hallucination rates. | [dex-model-evaluation](.agents/skills/dex-model-evaluation/SKILL.md) |
| `066` | **`dex-tool-calling-contracts`** | Define and validate JSON Schema tool-calling contracts for LLMs, handle multi-tool orchestration, validate parameter schemas, and safely parse tool execution results. | [dex-tool-calling-contracts](.agents/skills/dex-tool-calling-contracts/SKILL.md) |
| `067` | **`dex-agent-permissions`** | Establish least-privilege security boundaries, human-in-the-loop authorization gates, tool execution sandboxes, and audit logs for autonomous AI agents. | [dex-agent-permissions](.agents/skills/dex-agent-permissions/SKILL.md) |
| `068` | **`dex-llm-cost-controls`** | Implement LLM token budgeting, semantic caching (GPTCache), cost tracking, rate limiting, and model fallback cascades to optimize API spend. | [dex-llm-cost-controls](.agents/skills/dex-llm-cost-controls/SKILL.md) |
| `069` | **`dex-ai-observability`** | Implement comprehensive AI observability, OpenTelemetry tracing, LLM spans, token metrics, prompt/completion logging, and Langfuse/Arize integrations. | [dex-ai-observability](.agents/skills/dex-ai-observability/SKILL.md) |
| `070` | **`dex-dataset-curation`** | Curate, clean, deduplicate, filter, and synthesize high-quality training and evaluation datasets for LLM fine-tuning and domain adaptation. | [dex-dataset-curation](.agents/skills/dex-dataset-curation/SKILL.md) |

### Group H: Developer Experience (Skills 071–080)

| # | Skill ID | Description | Path |
|:---|:---|:---|:---|
| `071` | **`dex-repository-bootstrap`** | Scaffold production-grade software repositories from scratch with standardized directory layouts, linting, formatting, pre-commit hooks, CI templates, license, editorconfig, and reproducible dev environments. | [dex-repository-bootstrap](.agents/skills/dex-repository-bootstrap/SKILL.md) |
| `072` | **`dex-monorepo-governance`** | Govern monorepo architectures, workspace dependencies, isolated package boundaries, task caching pipelines (Nx/Turborepo), affected graph builds, and cross-package versioning. | [dex-monorepo-governance](.agents/skills/dex-monorepo-governance/SKILL.md) |
| `073` | **`dex-cli-engineering`** | Engineer industrial-grade command-line interfaces (CLIs), argument parsing, interactive terminal UX, POSIX flag conventions, exit code semantics, structured stdout/stderr, and auto-completion. | [dex-cli-engineering](.agents/skills/dex-cli-engineering/SKILL.md) |
| `074` | **`dex-plugin-architecture`** | Architect extensible plugin systems, micro-kernel architectures, extension lifecycle hooks, manifest specifications, sandboxed runtime execution, and dynamic loading. | [dex-plugin-architecture](.agents/skills/dex-plugin-architecture/SKILL.md) |
| `075` | **`dex-cross-platform-portability`** | Achieve cross-platform portability across Windows, Linux, and macOS, addressing POSIX vs Windows paths, line endings (CRLF vs LF), shell differences, file system case sensitivity, and environment variable handling. | [dex-cross-platform-portability](.agents/skills/dex-cross-platform-portability/SKILL.md) |
| `076` | **`dex-windows-packaging`** | Package and distribute applications for Windows environments, automating MSIX/InnoSetup builds, WinGet manifest publication, code signing with Authenticode, PowerShell automation scripts, and Windows Service management. | [dex-windows-packaging](.agents/skills/dex-windows-packaging/SKILL.md) |
| `077` | **`dex-documentation-as-code`** | Manage technical documentation as code, maintaining Architecture Decision Records (ADR), executable docs, doctests, OpenAPI specs, Mermaid diagrams, and automated doc generation pipelines. | [dex-documentation-as-code](.agents/skills/dex-documentation-as-code/SKILL.md) |
| `078` | **`dex-code-generation`** | Design deterministic code generators, AST transformations, scaffolding engines (Plop/Hygen), schema-driven codegen (OpenAPI/Protobuf to client SDKs), and macro systems. | [dex-code-generation](.agents/skills/dex-code-generation/SKILL.md) |
| `079` | **`dex-developer-tooling`** | Configure developer tooling, Devcontainers, Nix/Mise environments, Git hooks (Lefthook), editor integration (VS Code / Neovim), language server protocol (LSP), and debug configurations. | [dex-developer-tooling](.agents/skills/dex-developer-tooling/SKILL.md) |
| `080` | **`dex-semantic-version-automation`** | Automate Semantic Versioning (SemVer 2. | [dex-semantic-version-automation](.agents/skills/dex-semantic-version-automation/SKILL.md) |

### Group I: Security & Reliability (Skills 081–090)

| # | Skill ID | Description | Path |
|:---|:---|:---|:---|
| `081` | **`dex-auth-session-lifecycle`** | Implement robust authentication and session lifecycle management, JWT issuance and validation, refresh token rotation, revocation blacklists, CSRF/CORS defenses, and session hijacking mitigations. | [dex-auth-session-lifecycle](.agents/skills/dex-auth-session-lifecycle/SKILL.md) |
| `082` | **`dex-access-control-tenancy`** | Implement fine-grained access control, Role-Based Access Control (RBAC), Attribute-Based Access Control (ABAC), multi-tenant data isolation, row-level security (RLS), and tenant scoping policies. | [dex-access-control-tenancy](.agents/skills/dex-access-control-tenancy/SKILL.md) |
| `083` | **`dex-secrets-management`** | Manage application secrets, zero-hardcoded credentials policy, secret rotation, HashiCorp Vault / AWS Secrets Manager integration, runtime secret injection, and pre-commit leak detection. | [dex-secrets-management](.agents/skills/dex-secrets-management/SKILL.md) |
| `084` | **`dex-supply-chain-security`** | Secure software supply chain, Software Bill of Materials (SBOM) generation, dependency pinning and auditing, vulnerable package mitigation, container base image scanning, and build provenance with SLSA. | [dex-supply-chain-security](.agents/skills/dex-supply-chain-security/SKILL.md) |
| `085` | **`dex-threat-modeling`** | Conduct structured threat modeling, STRIDE analysis, attack surface mapping, abuse case definition, security control mapping, and risk prioritization. | [dex-threat-modeling](.agents/skills/dex-threat-modeling/SKILL.md) |
| `086` | **`dex-property-based-testing`** | Implement property-based testing, generative fuzzing, system invariant verification with Hypothesis / fast-check / QuickCheck, edge-case discovery, and test case shrinking. | [dex-property-based-testing](.agents/skills/dex-property-based-testing/SKILL.md) |
| `087` | **`dex-chaos-experiments`** | Design and execute chaos engineering experiments, fault injection, latency simulation, network partitions, circuit breaker verification, and resilience validation. | [dex-chaos-experiments](.agents/skills/dex-chaos-experiments/SKILL.md) |
| `088` | **`dex-experimentation-metrics`** | Architect feature flagging, experimentation platforms, A/B testing infrastructure, statistical significance evaluation, rollout strategies (canary/percentage), and metric telemetry. | [dex-experimentation-metrics](.agents/skills/dex-experimentation-metrics/SKILL.md) |
| `089` | **`dex-api-contract-evolution`** | Manage API contract evolution, backward compatibility guarantees, schema diffing, deprecation policies, sunset headers, migration adapters, and versioning strategies. | [dex-api-contract-evolution](.agents/skills/dex-api-contract-evolution/SKILL.md) |
| `090` | **`dex-incident-postmortems`** | Facilitate blameless incident postmortems, timeline reconstruction, root cause analysis (5 Whys / Fishbone), corrective action item tracking, SLA/SLO impact calculation, and post-incident learning reviews. | [dex-incident-postmortems](.agents/skills/dex-incident-postmortems/SKILL.md) |

### Group J: Cloud & Infrastructure (Skills 091–100)

| # | Skill ID | Description | Path |
|:---|:---|:---|:---|
| `091` | **`dex-container-image-engineering`** | Engineer production-grade, secure, minimal container images using multi-stage builds, non-root users, distroless/alpine bases, reproducible layers, SBOM generation (Syft), and vulnerability scanning (Trivy). | [dex-container-image-engineering](.agents/skills/dex-container-image-engineering/SKILL.md) |
| `092` | **`dex-kubernetes-deployment`** | Design, deploy, and manage production Kubernetes workloads including Deployments, StatefulSets, DaemonSets, resource requests/limits, liveness/readiness/startup probes, PodDisruptionBudgets, and rolling updates. | [dex-kubernetes-deployment](.agents/skills/dex-kubernetes-deployment/SKILL.md) |
| `093` | **`dex-infrastructure-as-code`** | Manage cloud and system resources declaratively using Terraform, OpenTofu, or Pulumi with remote state locking, modular design, drift detection, checkov security scanning, and strict plan validation. | [dex-infrastructure-as-code](.agents/skills/dex-infrastructure-as-code/SKILL.md) |
| `094` | **`dex-cloud-service-integration`** | Integrate application services securely with managed cloud resources (IAM, S3/GCS, SQS/PubSub, RDS, DynamoDB/Firestore) using Workload Identity Federation, exponential backoff, and least privilege access. | [dex-cloud-service-integration](.agents/skills/dex-cloud-service-integration/SKILL.md) |
| `095` | **`dex-zero-downtime-rollouts`** | Execute blue-green, canary, and progressive rollouts using Argo Rollouts, Flagger, or ingress traffic shifting with automated metric analysis, health checks, and instant rollbacks. | [dex-zero-downtime-rollouts](.agents/skills/dex-zero-downtime-rollouts/SKILL.md) |
| `096` | **`dex-service-mesh-networking`** | Architect and operate service mesh networking (Istio, Linkerd, Envoy) with mutual TLS (mTLS), fine-grained traffic routing, circuit breaking, fault injection, and telemetry. | [dex-service-mesh-networking](.agents/skills/dex-service-mesh-networking/SKILL.md) |
| `097` | **`dex-network-troubleshooting`** | Troubleshoot and diagnose network connectivity, DNS resolution, TLS certificates, TCP handshake states, HTTP latency, and packet drops using tcpdump, curl, dig, traceroute, and netstat. | [dex-network-troubleshooting](.agents/skills/dex-network-troubleshooting/SKILL.md) |
| `098` | **`dex-slo-error-budgets`** | Define, track, and operationalize Service Level Indicators (SLIs), Service Level Objectives (SLOs), Error Budgets, and multi-window burn rate alerts. | [dex-slo-error-budgets](.agents/skills/dex-slo-error-budgets/SKILL.md) |
| `099` | **`dex-distributed-tracing`** | Implement distributed tracing using OpenTelemetry (OTel), W3C tracecontext propagation, span lifecycle instrumentation, baggage attributes, and bottleneck latency analysis. | [dex-distributed-tracing](.agents/skills/dex-distributed-tracing/SKILL.md) |
| `100` | **`dex-cloud-cost-finops`** | Analyze, attribute, and optimize cloud infrastructure costs using FinOps principles, resource right-sizing, idle asset reclamation, spot/savings plan strategies, and unit economics. | [dex-cloud-cost-finops](.agents/skills/dex-cloud-cost-finops/SKILL.md) |

### Group K: Mobile & Desktop Engineering (Skills 101–110)

| # | Skill ID | Description | Path |
|:---|:---|:---|:---|
| `101` | **`dex-android-app-architecture`** | Architect scalable, robust Android applications using MVVM/MVI, Jetpack Compose, Kotlin Coroutines & StateFlow, Room database, and Hilt dependency injection. | [dex-android-app-architecture](.agents/skills/dex-android-app-architecture/SKILL.md) |
| `102` | **`dex-ios-app-architecture`** | Architect resilient iOS applications using SwiftUI, Swift Concurrency (async/await, Actor), NavigationStack, Observation framework, SwiftData/CoreData, and modular SPM. | [dex-ios-app-architecture](.agents/skills/dex-ios-app-architecture/SKILL.md) |
| `103` | **`dex-electron-security`** | Harden Electron desktop applications by enforcing process isolation, contextIsolation, nodeIntegration disablement, sandboxing, minimal contextBridge IPC APIs, and CSP. | [dex-electron-security](.agents/skills/dex-electron-security/SKILL.md) |
| `104` | **`dex-tauri-desktop-integration`** | Build lightweight, high-performance desktop apps using Tauri v2, Rust backend commands, strict permission capabilities, OS system tray, native window controls, and minimal memory footprint. | [dex-tauri-desktop-integration](.agents/skills/dex-tauri-desktop-integration/SKILL.md) |
| `105` | **`dex-mobile-offline-sync`** | Design offline-first mobile/desktop architectures using local databases (SQLite/WatermelonDB/Realm), mutation sync queues, conflict resolution (LWW, CRDTs), and background workers. | [dex-mobile-offline-sync](.agents/skills/dex-mobile-offline-sync/SKILL.md) |
| `106` | **`dex-mobile-release-pipelines`** | Automate mobile release pipelines with Fastlane, Android keystore signing, iOS provisioning profiles & certificates, semantic version codes, and store submission. | [dex-mobile-release-pipelines](.agents/skills/dex-mobile-release-pipelines/SKILL.md) |
| `107` | **`dex-mobile-performance-profiling`** | Profile mobile startup time (TTID/TTFD), frame rendering & jank detection (60/120 fps), memory leak detection (LeakCanary, Instruments Allocations), and battery drain. | [dex-mobile-performance-profiling](.agents/skills/dex-mobile-performance-profiling/SKILL.md) |
| `108` | **`dex-desktop-ipc-design`** | Design secure, type-safe desktop inter-process communication (IPC) interfaces using JSON Schema/Zod/Protobuf, bi-directional event buses, strict main-process validation, and privilege boundaries. | [dex-desktop-ipc-design](.agents/skills/dex-desktop-ipc-design/SKILL.md) |
| `109` | **`dex-native-device-integration`** | Integrate device capabilities (Camera, Geolocation, Bluetooth BLE, Biometrics, File System Access) across mobile and desktop with runtime permissions and graceful fallbacks. | [dex-native-device-integration](.agents/skills/dex-native-device-integration/SKILL.md) |
| `110` | **`dex-desktop-update-delivery`** | Manage desktop application auto-updates, update channels (alpha/beta/stable), cryptographic artifact signatures (codesign/minisign), delta updates, and atomic rollbacks. | [dex-desktop-update-delivery](.agents/skills/dex-desktop-update-delivery/SKILL.md) |

### Group L: Product & Operations Engineering (Skills 111–120)

| # | Skill ID | Description | Path |
|:---|:---|:---|:---|
| `111` | **`dex-privacy-impact-assessment`** | Conduct Data Protection and Privacy Impact Assessments (DPIA/PIA) adhering to GDPR, CCPA, and ISO 27701 with personal data classification, data flow mapping, and minimization safeguards. | [dex-privacy-impact-assessment](.agents/skills/dex-privacy-impact-assessment/SKILL.md) |
| `112` | **`dex-compliance-control-mapping`** | Map engineering, cloud, and process controls to compliance frameworks (SOC 2 Type II, ISO 27001, HIPAA, PCI-DSS) with automated evidence collection. | [dex-compliance-control-mapping](.agents/skills/dex-compliance-control-mapping/SKILL.md) |
| `113` | **`dex-audit-trail-integrity`** | Implement append-only, tamper-evident audit logging with cryptographic hash chaining (Merkle trees, HMAC), immutable storage (S3 Object Lock / WORM), non-repudiation, and CloudEvents schemas. | [dex-audit-trail-integrity](.agents/skills/dex-audit-trail-integrity/SKILL.md) |
| `114` | **`dex-configuration-drift`** | Detect, analyze, and reconcile configuration drift across Kubernetes GitOps (ArgoCD/Flux), cloud infrastructure (Terraform/OpenTofu), and application settings. | [dex-configuration-drift](.agents/skills/dex-configuration-drift/SKILL.md) |
| `115` | **`dex-product-discovery`** | Structure product discovery, user research synthesis, Jobs-to-be-Done (JTBD), opportunity solution trees, assumption testing, and rapid prototyping hypotheses. | [dex-product-discovery](.agents/skills/dex-product-discovery/SKILL.md) |
| `116` | **`dex-feature-prioritization`** | Prioritize product features and technical initiatives quantitatively using RICE, Value vs Effort, WSJF, and dependency graph analysis. | [dex-feature-prioritization](.agents/skills/dex-feature-prioritization/SKILL.md) |
| `117` | **`dex-analytics-instrumentation`** | Instrument product and business analytics with strict tracking plans, event taxonomy (object_action), schema validation, PII scrubbing, and dual client/server verification. | [dex-analytics-instrumentation](.agents/skills/dex-analytics-instrumentation/SKILL.md) |
| `118` | **`dex-feedback-triage`** | Triage, classify, and route high-velocity user feedback, bug reports, and app reviews into actionable engineering tasks using automated categorization and deduplication. | [dex-feedback-triage](.agents/skills/dex-feedback-triage/SKILL.md) |
| `119` | **`dex-runbook-automation`** | Author, validate, and execute operational runbooks (SOPs) with pre-flight checks, interactive approval gates, guarded commands, and rollback procedures. | [dex-runbook-automation](.agents/skills/dex-runbook-automation/SKILL.md) |
| `120` | **`dex-operational-readiness-review`** | Conduct Production Operational Readiness Reviews (ORR) across reliability, security, observability, disaster recovery, and supportability. | [dex-operational-readiness-review](.agents/skills/dex-operational-readiness-review/SKILL.md) |

### Group M: Advanced Software Verification (Skills 121–130)

| # | Skill ID | Description | Path |
|:---|:---|:---|:---|
| `121` | **`dex-static-analysis-rule-authoring`** | Design, test, and tune custom static analysis rules (AST matching, Semgrep, ESLint custom rules, CodeQL) to catch architectural violations, API misuse, and security anti-patterns with near-zero false positives. | [dex-static-analysis-rule-authoring](.agents/skills/dex-static-analysis-rule-authoring/SKILL.md) |
| `122` | **`dex-mutation-testing`** | Evaluate test suite effectiveness by injecting controlled faults (mutations) into source code to verify whether existing tests catch them, identifying assertion weaknesses. | [dex-mutation-testing](.agents/skills/dex-mutation-testing/SKILL.md) |
| `123` | **`dex-api-fuzz-testing`** | Execute coverage-guided and schema-based API fuzz testing (Schemathesis, RESTler) to discover 500 errors, unhandled boundary exceptions, memory leaks, and serialization flaws. | [dex-api-fuzz-testing](.agents/skills/dex-api-fuzz-testing/SKILL.md) |
| `124` | **`dex-differential-testing`** | Compare behavior, output equivalence, and performance between two software implementations (legacy vs rewritten, compiler versions, or competing algorithms) across randomized inputs. | [dex-differential-testing](.agents/skills/dex-differential-testing/SKILL.md) |
| `125` | **`dex-flaky-test-remediation`** | Systematically detect, isolate, diagnose, and remediate non-deterministic (flaky) tests caused by race conditions, network latency, shared mutable state, and unseeded randomness. | [dex-flaky-test-remediation](.agents/skills/dex-flaky-test-remediation/SKILL.md) |
| `126` | **`dex-test-data-management`** | Architect secure, isolated, synthetic, and ephemeral test data fixtures and databases with automated teardown and masking. | [dex-test-data-management](.agents/skills/dex-test-data-management/SKILL.md) |
| `127` | **`dex-compatibility-matrix-testing`** | Define, automate, and execute matrix-based compatibility testing across operating systems, runtime versions, browsers, and dependency sets. | [dex-compatibility-matrix-testing](.agents/skills/dex-compatibility-matrix-testing/SKILL.md) |
| `128` | **`dex-reproducible-benchmarking`** | Design, isolate, measure, and statistically analyze software benchmarks with controlled noise, CPU pinning, warmups, and variance tracking. | [dex-reproducible-benchmarking](.agents/skills/dex-reproducible-benchmarking/SKILL.md) |
| `129` | **`dex-formal-invariant-checks`** | Specify, model, and verify critical domain invariants using stateful property-based testing and formal assertion contracts. | [dex-formal-invariant-checks](.agents/skills/dex-formal-invariant-checks/SKILL.md) |
| `130` | **`dex-coverage-risk-analysis`** | Correlate code coverage metrics with code churn, production defect density, and business criticality to prioritize high-value test engineering. | [dex-coverage-risk-analysis](.agents/skills/dex-coverage-risk-analysis/SKILL.md) |

### Group N: Advanced SRE & Distributed Systems (Skills 131–140)

| # | Skill ID | Description | Path |
|:---|:---|:---|:---|
| `131` | **`dex-load-and-stress-testing`** | Design, script, and execute realistic load, spike, endurance, and stress tests using tools like K6, Locust, or Gatling to establish saturation points, latency percentiles, and capacity limits. | [dex-load-and-stress-testing](.agents/skills/dex-load-and-stress-testing/SKILL.md) |
| `132` | **`dex-traffic-shaping-backpressure`** | Implement traffic shaping, backpressure mechanisms, leaky/token buckets, priority queues, and load-shedding to prevent cascading failures under extreme load. | [dex-traffic-shaping-backpressure](.agents/skills/dex-traffic-shaping-backpressure/SKILL.md) |
| `133` | **`dex-rate-limiting-quotas`** | Design and enforce multi-tier rate limiting and quota management using algorithms like Sliding Window Log, Token Bucket, and Redis-backed distributed stores. | [dex-rate-limiting-quotas](.agents/skills/dex-rate-limiting-quotas/SKILL.md) |
| `134` | **`dex-distributed-consistency`** | Analyze, design, and resolve distributed consistency challenges across microservices, including Saga patterns, transactional outboxes, idempotency keys, and conflict resolution. | [dex-distributed-consistency](.agents/skills/dex-distributed-consistency/SKILL.md) |
| `135` | **`dex-service-failover`** | Architect, configure, and validate automated service failover, multi-region routing, health-checking protocols, and circuit breakers (Envoy, Resilience4j). | [dex-service-failover](.agents/skills/dex-service-failover/SKILL.md) |
| `136` | **`dex-alert-quality-engineering`** | Audit, refine, and eliminate noisy monitoring alerts by tuning thresholds, implementing deduplication, and ensuring all alerts are actionable with runbooks. | [dex-alert-quality-engineering](.agents/skills/dex-alert-quality-engineering/SKILL.md) |
| `137` | **`dex-log-pipeline-design`** | Design scalable, structured, observable log collection and processing pipelines with correlation IDs, redaction of sensitive data (PII), and tiered storage policies. | [dex-log-pipeline-design](.agents/skills/dex-log-pipeline-design/SKILL.md) |
| `138` | **`dex-metric-cardinality-control`** | Audit, manage, and prevent metric cardinality explosions in Prometheus and Datadog by enforcing label budgets, drop rules, and recording rules. | [dex-metric-cardinality-control](.agents/skills/dex-metric-cardinality-control/SKILL.md) |
| `139` | **`dex-oncall-handover`** | Structure and execute comprehensive on-call shifts, handovers, runbook updates, and incident post-shift briefings with zero knowledge loss. | [dex-oncall-handover](.agents/skills/dex-oncall-handover/SKILL.md) |
| `140` | **`dex-operational-game-days`** | Plan, orchestrate, and facilitate controlled chaos engineering game days and failure injection exercises to validate team incident response and system resilience. | [dex-operational-game-days](.agents/skills/dex-operational-game-days/SKILL.md) |

### Group O: Advanced Cloud Platform (Skills 141–150)

| # | Skill ID | Description | Path |
|:---|:---|:---|:---|
| `141` | **`dex-serverless-architecture`** | Architect, optimize, and secure event-driven serverless architectures (AWS Lambda, Google Cloud Run) mitigating cold starts, managing concurrency limits, and ensuring idempotency. | [dex-serverless-architecture](.agents/skills/dex-serverless-architecture/SKILL.md) |
| `142` | **`dex-edge-runtime-engineering`** | Build ultra-low latency globally distributed applications on Edge runtimes (Cloudflare Workers, V8 isolates, Fastly Compute) managing memory constraints and edge caching. | [dex-edge-runtime-engineering](.agents/skills/dex-edge-runtime-engineering/SKILL.md) |
| `143` | **`dex-cloud-iam-policy-review`** | Audit, sanitize, and enforce Least-Privilege IAM policies, role boundaries, and access conditions across AWS, GCP, and Azure. | [dex-cloud-iam-policy-review](.agents/skills/dex-cloud-iam-policy-review/SKILL.md) |
| `144` | **`dex-cloud-network-design`** | Architect secure, isolated, and scalable cloud network topologies including VPCs, private subnets, transit gateways, VPC peering, and egress filtering. | [dex-cloud-network-design](.agents/skills/dex-cloud-network-design/SKILL.md) |
| `145` | **`dex-gitops-workflows`** | Implement declarative continuous deployment and reconciliation using GitOps engines (ArgoCD, FluxCD), managing environment drift, secrets, and rollbacks. | [dex-gitops-workflows](.agents/skills/dex-gitops-workflows/SKILL.md) |
| `146` | **`dex-kubernetes-policy-enforcement`** | Author, validate, and enforce cluster governance policies using admission controllers (OPA Gatekeeper, Kyverno) to prevent privilege escalations and unconstrained resource usage. | [dex-kubernetes-policy-enforcement](.agents/skills/dex-kubernetes-policy-enforcement/SKILL.md) |
| `147` | **`dex-platform-service-catalog`** | Design and curate Internal Developer Platform (IDP) service catalogs (Backstage, Port) providing golden paths, service ownership, API documentation, and self-service scaffolding. | [dex-platform-service-catalog](.agents/skills/dex-platform-service-catalog/SKILL.md) |
| `148` | **`dex-environment-promotion`** | Design deterministic, automated promotion pipelines moving identical immutable release artifacts across Dev, Staging, and Production with rigorous gate checks. | [dex-environment-promotion](.agents/skills/dex-environment-promotion/SKILL.md) |
| `149` | **`dex-service-discovery`** | Architect, tune, and debug resilient service discovery mechanisms using DNS-based, client-side, and control-plane registries (CoreDNS, Envoy, Consul). | [dex-service-discovery](.agents/skills/dex-service-discovery/SKILL.md) |
| `150` | **`dex-cloud-resource-tagging`** | Design, enforce, and automate cloud resource tagging taxonomies (FinOps, Cost Allocation, Ownership, Lifecycle) using policy-as-code and automated remediations. | [dex-cloud-resource-tagging](.agents/skills/dex-cloud-resource-tagging/SKILL.md) |

### Group P: Language & Runtime Engineering (Skills 151–160)

| # | Skill ID | Description | Path |
|:---|:---|:---|:---|
| `151` | **`dex-typescript-type-safety`** | Architect strict, bulletproof TypeScript systems leveraging branded types, template literals, conditional types, and runtime schema boundaries (Zod) without resorting to 'any'. | [dex-typescript-type-safety](.agents/skills/dex-typescript-type-safety/SKILL.md) |
| `152` | **`dex-nodejs-runtime-diagnostics`** | Diagnose and resolve Node. | [dex-nodejs-runtime-diagnostics](.agents/skills/dex-nodejs-runtime-diagnostics/SKILL.md) |
| `153` | **`dex-python-project-engineering`** | Standardize production-grade Python projects using modern packaging (Poetry, Hatch, uv), strict type checking (Mypy, Pyright), linting (Ruff), and virtual environment isolation. | [dex-python-project-engineering](.agents/skills/dex-python-project-engineering/SKILL.md) |
| `154` | **`dex-rust-unsafe-audit`** | Audit, verify, and minimize 'unsafe' code blocks in Rust, validating ownership invariants, raw pointer arithmetic, FFI boundaries, and undefined behavior using Miri and Loom. | [dex-rust-unsafe-audit](.agents/skills/dex-rust-unsafe-audit/SKILL.md) |
| `155` | **`dex-cpp-memory-safety`** | Detect, eliminate, and prevent memory safety bugs in modern C++ (C++17/20) using AddressSanitizer (ASan), UndefinedBehaviorSanitizer (UBSan), smart pointers, and RAII principles. | [dex-cpp-memory-safety](.agents/skills/dex-cpp-memory-safety/SKILL.md) |
| `156` | **`dex-go-concurrency-patterns`** | Architect, synchronize, and debug high-throughput Go concurrent systems using channels, worker pools, sync. | [dex-go-concurrency-patterns](.agents/skills/dex-go-concurrency-patterns/SKILL.md) |
| `157` | **`dex-jvm-performance-diagnostics`** | Diagnose and tune JVM memory, garbage collection pauses (G1GC, ZGC), thread contention, and JIT compilation using JFR, async-profiler, and visualgc. | [dex-jvm-performance-diagnostics](.agents/skills/dex-jvm-performance-diagnostics/SKILL.md) |
| `158` | **`dex-dotnet-application-engineering`** | Architect, optimize, and diagnose modern cross-platform . | [dex-dotnet-application-engineering](.agents/skills/dex-dotnet-application-engineering/SKILL.md) |
| `159` | **`dex-webassembly-integration`** | Compile, integrate, and optimize WebAssembly (WASM) modules across browser and server runtimes (Wasmtime, Wasmer), managing linear memory, FFI boundary overhead, and sandbox security. | [dex-webassembly-integration](.agents/skills/dex-webassembly-integration/SKILL.md) |
| `160` | **`dex-ffi-boundary-contracts`** | Design, document, and validate robust Foreign Function Interface (FFI) boundaries (C ABI) across languages, ensuring memory ownership contracts, alignment, and error translation. | [dex-ffi-boundary-contracts](.agents/skills/dex-ffi-boundary-contracts/SKILL.md) |

### Group Q: Advanced AI Systems (Skills 161–170)

| # | Skill ID | Description | Path |
|:---|:---|:---|:---|
| `161` | **`dex-mcp-server-design`** | Architect, implement, and secure Model Context Protocol (MCP) servers exposing tools, resources, and prompts to AI agents with strict JSON-RPC schemas and permission boundaries. | [dex-mcp-server-design](.agents/skills/dex-mcp-server-design/SKILL.md) |
| `162` | **`dex-vector-index-design`** | Architect, configure, and benchmark vector search indexes (HNSW, IVF-PQ) across vector databases (Qdrant, Pinecone, pgvector), balancing recall, latency, and RAM costs. | [dex-vector-index-design](.agents/skills/dex-vector-index-design/SKILL.md) |
| `163` | **`dex-reranking-strategies`** | Implement multi-stage retrieval pipelines combining dense/sparse retrieval with Cross-Encoder and ColBERT rerankers (Cohere, BGE-Reranker) to boost top-K relevance. | [dex-reranking-strategies](.agents/skills/dex-reranking-strategies/SKILL.md) |
| `164` | **`dex-structured-llm-output`** | Enforce reliable, validated JSON schema and Pydantic/Zod structured outputs from LLMs using constrained decoding, tool-calling APIs, and automatic self-correction. | [dex-structured-llm-output](.agents/skills/dex-structured-llm-output/SKILL.md) |
| `165` | **`dex-prompt-injection-defense`** | Architect defense-in-depth protections against direct and indirect prompt injection, jailbreaks, and data exfiltration using dual-LLM boundaries, input sanitizers, and tool permission guards. | [dex-prompt-injection-defense](.agents/skills/dex-prompt-injection-defense/SKILL.md) |
| `166` | **`dex-grounding-citation-audit`** | Audit, score, and verify factual grounding and citation integrity in RAG systems, detecting hallucinations and ungrounded claims using NLI and LLM-as-a-judge frameworks. | [dex-grounding-citation-audit](.agents/skills/dex-grounding-citation-audit/SKILL.md) |
| `167` | **`dex-agent-memory-governance`** | Architect, maintain, and govern short-term, working, and long-term memory for AI agents, implementing summarization, eviction, privacy boundaries, and stale context pruning. | [dex-agent-memory-governance](.agents/skills/dex-agent-memory-governance/SKILL.md) |
| `168` | **`dex-multimodal-input-pipelines`** | Design, validate, and optimize multimodal input pipelines (images, audio, PDF documents) for vision and speech LLMs, managing resolution, token costs, and PII masking. | [dex-multimodal-input-pipelines](.agents/skills/dex-multimodal-input-pipelines/SKILL.md) |
| `169` | **`dex-agent-evaluation-harness`** | Design, automate, and score end-to-end AI agent trajectory evaluations measuring tool-call accuracy, task success rate, step efficiency, and regression resilience. | [dex-agent-evaluation-harness](.agents/skills/dex-agent-evaluation-harness/SKILL.md) |
| `170` | **`dex-llm-fallback-routing`** | Architect resilient, cost-aware multi-LLM routing, load-balancing, and fallback cascades across providers (OpenAI, Anthropic, DeepSeek, Local Ollama) managing rate limits, context windows, and cost optimization. | [dex-llm-fallback-routing](.agents/skills/dex-llm-fallback-routing/SKILL.md) |

### Group R: Product Design & User Research (Skills 171–180)

| # | Skill ID | Description | Path |
|:---|:---|:---|:---|
| `171` | **`dex-user-journey-mapping`** | Map, analyze, and optimize end-to-end user journeys, friction points, drop-off phases, and emotional arcs to align engineering delivery with user experience. | [dex-user-journey-mapping](.agents/skills/dex-user-journey-mapping/SKILL.md) |
| `172` | **`dex-information-architecture`** | Structure, categorize, and label application information, navigation systems, and content hierarchies using card sorting, taxonomy modeling, and findability principles. | [dex-information-architecture](.agents/skills/dex-information-architecture/SKILL.md) |
| `173` | **`dex-usability-study-design`** | Design, facilitate, and synthesize task-based usability studies (moderated and unmoderated) using think-aloud protocols and SUS scoring. | [dex-usability-study-design](.agents/skills/dex-usability-study-design/SKILL.md) |
| `174` | **`dex-accessibility-automation`** | Automate accessibility audits (WCAG 2. | [dex-accessibility-automation](.agents/skills/dex-accessibility-automation/SKILL.md) |
| `175` | **`dex-design-handoff-verification`** | Verify and enforce pixel, typography, spacing, and state consistency between Figma design tokens and production frontend code using Storybook and visual regression tools. | [dex-design-handoff-verification](.agents/skills/dex-design-handoff-verification/SKILL.md) |
| `176` | **`dex-product-requirements-writing`** | Author structured, unambiguous, engineering-ready Product Requirement Documents (PRDs) with clear problem statements, user stories, edge cases, and measurable success metrics. | [dex-product-requirements-writing](.agents/skills/dex-product-requirements-writing/SKILL.md) |
| `177` | **`dex-conversion-funnel-analysis`** | Instrument, analyze, and optimize conversion funnels, drop-off rates, and user friction across acquisition, activation, and checkout flows using event schemas and cohort analytics. | [dex-conversion-funnel-analysis](.agents/skills/dex-conversion-funnel-analysis/SKILL.md) |
| `178` | **`dex-feature-adoption-analysis`** | Measure, segment, and evaluate post-release feature adoption, retention curves, and engagement depth across user cohorts. | [dex-feature-adoption-analysis](.agents/skills/dex-feature-adoption-analysis/SKILL.md) |
| `179` | **`dex-user-consent-ux`** | Design, implement, and audit transparent, accessible, and compliant user consent flows and privacy controls (GDPR, CCPA, Cookie banners) avoiding dark patterns. | [dex-user-consent-ux](.agents/skills/dex-user-consent-ux/SKILL.md) |
| `180` | **`dex-supportability-engineering`** | Design, instrument, and automate user-facing self-service diagnostics, actionable error states, debug bundles, and supportability runbooks. | [dex-supportability-engineering](.agents/skills/dex-supportability-engineering/SKILL.md) |

### Group S: Application Security Specialists (Skills 181–190)

| # | Skill ID | Description | Path |
|:---|:---|:---|:---|
| `181` | **`dex-sast-finding-triage`** | Triage, validate, and remediate Static Application Security Testing (SAST) findings, eliminating false positives and tracing true-positive source-to-sink taint flows. | [dex-sast-finding-triage](.agents/skills/dex-sast-finding-triage/SKILL.md) |
| `182` | **`dex-dast-scoping`** | Define authorized scopes, scan profiles, boundary exclusions, and rate limits for Dynamic Application Security Testing (DAST) using OWASP ZAP or Burp Suite. | [dex-dast-scoping](.agents/skills/dex-dast-scoping/SKILL.md) |
| `183` | **`dex-api-abuse-prevention`** | Architect, detect, and mitigate automated API abuse, credential stuffing, scraping, and bot attacks using behavioral fingerprinting, proof-of-work challenges, and adaptive throttling. | [dex-api-abuse-prevention](.agents/skills/dex-api-abuse-prevention/SKILL.md) |
| `184` | **`dex-web-security-headers`** | Design, configure, and audit HTTP security headers including strict Content Security Policy (CSP), HSTS, Permissions-Policy, and secure cookie attributes. | [dex-web-security-headers](.agents/skills/dex-web-security-headers/SKILL.md) |
| `185` | **`dex-browser-extension-hardening`** | Harden browser extensions across Manifest V3, content script isolation, cross-origin communication, and CSP to prevent token theft and malicious page injection. | [dex-browser-extension-hardening](.agents/skills/dex-browser-extension-hardening/SKILL.md) |
| `186` | **`dex-sbom-verification`** | Generate, sign, and verify Software Bill of Materials (SBOM) using CycloneDX and SPDX standards, integrating Syft and Cosign to secure the software supply chain. | [dex-sbom-verification](.agents/skills/dex-sbom-verification/SKILL.md) |
| `187` | **`dex-vulnerability-remediation`** | Prioritize, triage, and remediate CVE vulnerabilities across dependencies and container base images using risk-based reachability analysis (EPSS, KEV) and automated patch upgrades. | [dex-vulnerability-remediation](.agents/skills/dex-vulnerability-remediation/SKILL.md) |
| `188` | **`dex-security-logging-detection`** | Design, instrument, and validate tamper-evident security audit logs and detection rules (Sigma, SIEM) capturing authentication, authorization, and privilege escalation events. | [dex-security-logging-detection](.agents/skills/dex-security-logging-detection/SKILL.md) |
| `189` | **`dex-cryptographic-api-review`** | Audit, verify, and enforce correct cryptographic API usage, key derivation (Argon2id, PBKDF2), secure random generation, and authenticated encryption (AES-GCM, ChaCha20-Poly1305). | [dex-cryptographic-api-review](.agents/skills/dex-cryptographic-api-review/SKILL.md) |
| `190` | **`dex-secure-build-runners`** | Harden CI/CD execution environments and GitHub Actions runners, enforcing least-privilege tokens, ephemeral sandboxes, and protection against untrusted pull requests (pwn-request attacks). | [dex-secure-build-runners](.agents/skills/dex-secure-build-runners/SKILL.md) |

### Group T: SkillOps Engineering (Skills 191–200)

| # | Skill ID | Description | Path |
|:---|:---|:---|:---|
| `191` | **`dex-skill-discovery-indexer`** | Discover, parse, validate, and index Agent Skills across local and remote repositories, generating structured catalogs and searchable capability manifests. | [dex-skill-discovery-indexer](.agents/skills/dex-skill-discovery-indexer/SKILL.md) |
| `192` | **`dex-skill-license-provenance`** | Track, audit, and document open-source licenses, author attributions, and exact upstream commit provenance for third-party imported skills. | [dex-skill-license-provenance](.agents/skills/dex-skill-license-provenance/SKILL.md) |
| `193` | **`dex-skill-semantic-deduplication`** | Identify, analyze, and consolidate functionally identical or near-duplicate Agent Skills across repositories using semantic similarity and intent clustering. | [dex-skill-semantic-deduplication](.agents/skills/dex-skill-semantic-deduplication/SKILL.md) |
| `194` | **`dex-skill-security-screening`** | Inspect, screen, and sandbox untrusted third-party skill instructions, scripts, and MCP permissions for prompt injection, backdoors, and unsafe execution risks. | [dex-skill-security-screening](.agents/skills/dex-skill-security-screening/SKILL.md) |
| `195` | **`dex-skill-import-packaging`** | Package, adapt, and import validated third-party skills into isolated integrations with schema normalization, dry-run capabilities, and automated rollback. | [dex-skill-import-packaging](.agents/skills/dex-skill-import-packaging/SKILL.md) |
| `196` | **`dex-skill-upstream-sync`** | Track, diff, and synchronize pinned upstream repositories, detecting remote updates and breaking changes without overwriting local modifications. | [dex-skill-upstream-sync](.agents/skills/dex-skill-upstream-sync/SKILL.md) |
| `197` | **`dex-skill-activation-evaluation`** | Evaluate, benchmark, and optimize skill activation precision and recall across realistic user intent prompts, tuning metadata to eradicate false activations. | [dex-skill-activation-evaluation](.agents/skills/dex-skill-activation-evaluation/SKILL.md) |
| `198` | **`dex-skill-host-adapters`** | Adapt, negotiate capabilities, and transform Agent Skills for seamless execution across different AI coding hosts (OpenAI Codex, Claude Desktop, Cursor, Copilot Workspace). | [dex-skill-host-adapters](.agents/skills/dex-skill-host-adapters/SKILL.md) |
| `199` | **`dex-skill-dependency-graph`** | Model, validate, and traverse the directed acyclic graph (DAG) of skill dependencies and orchestration pipelines, detecting circular references and sequencing errors. | [dex-skill-dependency-graph](.agents/skills/dex-skill-dependency-graph/SKILL.md) |
| `200` | **`dex-skill-quality-benchmarking`** | Benchmark, measure, and score the real-world engineering effectiveness, token efficiency, and completion fidelity of Agent Skills on representative tasks. | [dex-skill-quality-benchmarking](.agents/skills/dex-skill-quality-benchmarking/SKILL.md) |

### Group U: Visual Design Intelligence (Skills 201–210)

| # | Skill ID | Description | Path |
|:---|:---|:---|:---|
| `201` | **`dex-design-brief-synthesis`** | Synthesize business requirements, user personas, and brand identity into an actionable visual design brief with aesthetic tokens, layout guidelines, and accessibility constraints. | [dex-design-brief-synthesis](.agents/skills/dex-design-brief-synthesis/SKILL.md) |
| `202` | **`dex-visual-hierarchy-audit`** | Audit and restructure visual hierarchy, content emphasis, information density, and reading order across complex screens to eliminate competing focal points. | [dex-visual-hierarchy-audit](.agents/skills/dex-visual-hierarchy-audit/SKILL.md) |
| `203` | **`dex-layout-composition-patterns`** | Evaluate and engineer responsive layout compositions including 12-column grids, asymmetric Bento boxes, editorial flows, and split-screen dashboards. | [dex-layout-composition-patterns](.agents/skills/dex-layout-composition-patterns/SKILL.md) |
| `204` | **`dex-color-contrast-systems`** | Engineer mathematical APCA and WCAG 2. | [dex-color-contrast-systems](.agents/skills/dex-color-contrast-systems/SKILL.md) |
| `205` | **`dex-fluid-typography-engineering`** | Implement mathematical fluid typography scales using CSS clamp(), responsive modular scales, dynamic optical sizing, and optimal line-height geometry. | [dex-fluid-typography-engineering](.agents/skills/dex-fluid-typography-engineering/SKILL.md) |
| `206` | **`dex-motion-interaction-specification`** | Specify purposeful UI motion choreographies, spring physics curves, transition durations, and strict prefers-reduced-motion accessibility fallbacks. | [dex-motion-interaction-specification](.agents/skills/dex-motion-interaction-specification/SKILL.md) |
| `207` | **`dex-dashboard-data-storytelling`** | Architect analytical dashboard layouts that convey data stories, prioritize high-value KPI metrics, separate operational signals from decorative charts, and facilitate decision-making. | [dex-dashboard-data-storytelling](.agents/skills/dex-dashboard-data-storytelling/SKILL.md) |
| `208` | **`dex-design-reference-evaluation`** | Critically analyze visual design references, competitor benchmarks, and design inspiration against product requirements to extract reusable design principles without copyright infringement. | [dex-design-reference-evaluation](.agents/skills/dex-design-reference-evaluation/SKILL.md) |
| `209` | **`dex-design-system-documentation`** | Author living design system documentation, component anatomies, token tables, interactive storybook examples, and usage do's and don'ts. | [dex-design-system-documentation](.agents/skills/dex-design-system-documentation/SKILL.md) |
| `210` | **`dex-ui-visual-qa-review`** | Conduct rigorous visual quality assurance (Visual QA) reviews against production builds, verifying pixel alignment, spacing token adherence, font rendering, and edge-case states. | [dex-ui-visual-qa-review](.agents/skills/dex-ui-visual-qa-review/SKILL.md) |

### Group V: Advanced Web Experiences (Skills 211–220)

| # | Skill ID | Description | Path |
|:---|:---|:---|:---|
| `211` | **`dex-web-animation-performance`** | Profile and optimize 60fps web animation performance, eliminating layout thrashing, forced synchronous layouts, and excessive composite layers using GPU transforms and Will-Change budgets. | [dex-web-animation-performance](.agents/skills/dex-web-animation-performance/SKILL.md) |
| `212` | **`dex-media-delivery-pipelines`** | Engineer modern responsive media pipelines supporting next-gen image formats (AVIF, WebP), adaptive audio, responsive picture elements, CDN image transformations, and blurhash placeholders. | [dex-media-delivery-pipelines](.agents/skills/dex-media-delivery-pipelines/SKILL.md) |
| `213` | **`dex-hls-dash-playback`** | Architect resilient HTTP Live Streaming (HLS) and MPEG-DASH adaptive bitrate playback engines with automated buffer stall recovery, multi-track audio, and WebVTT captions. | [dex-hls-dash-playback](.agents/skills/dex-hls-dash-playback/SKILL.md) |
| `214` | **`dex-progressive-web-apps`** | Engineer installable Progressive Web Apps (PWA) with Workbox offline caching strategies, background sync, Web App Manifests, service worker lifecycle governance, and seamless app updates. | [dex-progressive-web-apps](.agents/skills/dex-progressive-web-apps/SKILL.md) |
| `215` | **`dex-web-push-permission-flow`** | Design high-conversion, contextual Web Push notification permission request flows, VAPID key authentication, and graceful push message delivery with fallback notification badges. | [dex-web-push-permission-flow](.agents/skills/dex-web-push-permission-flow/SKILL.md) |
| `216` | **`dex-search-interface-experience`** | Architect accessible, instant search interfaces with debounced typeahead suggestions, faceted multi-attribute filters, keyboard navigation (combobox pattern), and empty search recovery. | [dex-search-interface-experience](.agents/skills/dex-search-interface-experience/SKILL.md) |
| `217` | **`dex-virtualized-infinite-lists`** | Implement high-performance windowed list virtualization (TanStack Virtual, react-window) supporting dynamic row heights, scroll restoration, sticky headers, and stable infinite paging. | [dex-virtualized-infinite-lists](.agents/skills/dex-virtualized-infinite-lists/SKILL.md) |
| `218` | **`dex-web-canvas-rendering`** | Engineer interactive, high-DPI HTML5 2D Canvas interfaces with dirty-rectangle redraw optimizations, spatial indexing (quadtrees), pan-zoom transformations, and pointer hit detection. | [dex-web-canvas-rendering](.agents/skills/dex-web-canvas-rendering/SKILL.md) |
| `219` | **`dex-webgpu-rendering-fundamentals`** | Design safe, high-performance WebGPU rendering pipelines, WGSL shader compilations, memory buffer lifecycle management, and device-loss recovery with WebGL2 fallback. | [dex-webgpu-rendering-fundamentals](.agents/skills/dex-webgpu-rendering-fundamentals/SKILL.md) |
| `220` | **`dex-frontend-error-recovery`** | Implement robust frontend error boundaries, optimistic mutation rollbacks, exponential backoff network retries, and contextual fallback states to prevent white-screen crashes. | [dex-frontend-error-recovery](.agents/skills/dex-frontend-error-recovery/SKILL.md) |

### Group W: Browser Extensions & Automation (Skills 221–230)

| # | Skill ID | Description | Path |
|:---|:---|:---|:---|
| `221` | **`dex-browser-extension-mv3`** | Architect Manifest V3 browser extensions with non-persistent background service workers, declarativeNetRequest rules, minimal permission scopes, and cross-browser packaging (Chrome, Firefox, Edge, Safari). | [dex-browser-extension-mv3](.agents/skills/dex-browser-extension-mv3/SKILL.md) |
| `222` | **`dex-extension-message-security`** | Secure asynchronous message channels between content scripts, popup UIs, devtools panels, and background service workers with strict sender origin validation and typed schemas. | [dex-extension-message-security](.agents/skills/dex-extension-message-security/SKILL.md) |
| `223` | **`dex-extension-background-lifecycle`** | Engineer resilient Manifest V3 background service workers with chrome. | [dex-extension-background-lifecycle](.agents/skills/dex-extension-background-lifecycle/SKILL.md) |
| `224` | **`dex-extension-content-script-isolation`** | Enforce strict DOM boundaries between untrusted host web page scripts and extension content scripts using isolated worlds, CustomEvent communication bridges, and Shadow DOM encapsulation. | [dex-extension-content-script-isolation](.agents/skills/dex-extension-content-script-isolation/SKILL.md) |
| `225` | **`dex-extension-storage-migration`** | Manage schema versioning, asynchronous data migrations, and corruption recovery for chrome. | [dex-extension-storage-migration](.agents/skills/dex-extension-storage-migration/SKILL.md) |
| `226` | **`dex-browser-automation-testing`** | Design deterministic, flake-free browser automation suites using Playwright/Puppeteer with locator best practices, explicit network idle waits, and isolated browser contexts. | [dex-browser-automation-testing](.agents/skills/dex-browser-automation-testing/SKILL.md) |
| `227` | **`dex-cdp-observability`** | Harness the Chrome DevTools Protocol (CDP) for low-level performance trace capture, memory heap snapshot analysis, network throttle simulation, and console telemetry auditing. | [dex-cdp-observability](.agents/skills/dex-cdp-observability/SKILL.md) |
| `228` | **`dex-headless-ui-verification`** | Detect and reconcile behavioral and visual discrepancies between headless browser runners (Linux CI) and actual user graphical browsers (Windows/macOS) including font subpixel antialiasing and GPU acceleration flags. | [dex-headless-ui-verification](.agents/skills/dex-headless-ui-verification/SKILL.md) |
| `229` | **`dex-web-permission-ux`** | Design progressive, user-centric browser permission request experiences for Camera, Microphone, Geolocation, Notifications, and Storage with pre-prompt primers and graceful denial recovery. | [dex-web-permission-ux](.agents/skills/dex-web-permission-ux/SKILL.md) |
| `230` | **`dex-cross-origin-integration`** | Architect secure cross-origin communication between parent applications and embedded iframes using postMessage with origin whitelisting, Content Security Policy frame-ancestors, and COOP/COEP isolation headers. | [dex-cross-origin-integration](.agents/skills/dex-cross-origin-integration/SKILL.md) |

### Group X: Authorized Reverse Engineering (Skills 231–240)

| # | Skill ID | Description | Path |
|:---|:---|:---|:---|
| `231` | **`dex-pe-elf-structure-inspection`** | Inspect compiled PE (Windows) and ELF (Linux) executable headers, section tables (. | [dex-pe-elf-structure-inspection](.agents/skills/dex-pe-elf-structure-inspection/SKILL.md) |
| `232` | **`dex-native-symbol-mapping`** | Reconstruct native symbol tables, demangle Itanium/MSVC C++ function signatures, map cross-reference graphs, and correlate debug symbol databases (PDB, DWARF) with stripped binaries. | [dex-native-symbol-mapping](.agents/skills/dex-native-symbol-mapping/SKILL.md) |
| `233` | **`dex-disassembly-cfg-reconstruction`** | Analyze disassembled machine code (x86-64, ARM64) to reconstruct function basic blocks, control flow graphs (CFG), loop invariants, and calling convention parameter transfers using safe CLI utilities (objdump, llvm-objdump). | [dex-disassembly-cfg-reconstruction](.agents/skills/dex-disassembly-cfg-reconstruction/SKILL.md) |
| `234` | **`dex-managed-assembly-inspection`** | Inspect compiled . | [dex-managed-assembly-inspection](.agents/skills/dex-managed-assembly-inspection/SKILL.md) |
| `235` | **`dex-electron-artifact-analysis`** | Extract and audit packaged Electron ASAR archives, inspect webPreferences security flags (nodeIntegration, contextIsolation, sandbox), and audit preload script IPC boundary exposures. | [dex-electron-artifact-analysis](.agents/skills/dex-electron-artifact-analysis/SKILL.md) |
| `236` | **`dex-javascript-sourcemap-recovery`** | Reconstruct original TypeScript/JavaScript source trees from production sourcemap files (. | [dex-javascript-sourcemap-recovery](.agents/skills/dex-javascript-sourcemap-recovery/SKILL.md) |
| `237` | **`dex-mobile-package-static-audit`** | Perform static security audits on authorized Android APK/AAB packages and iOS IPA bundles, analyzing AndroidManifest. | [dex-mobile-package-static-audit](.agents/skills/dex-mobile-package-static-audit/SKILL.md) |
| `238` | **`dex-firmware-metadata-inspection`** | Examine embedded device firmware binary image headers, partition layouts (U-Boot, kernel, rootfs SquashFS), entropy distributions, and hardware architecture metadata using binwalk / dumpimage. | [dex-firmware-metadata-inspection](.agents/skills/dex-firmware-metadata-inspection/SKILL.md) |
| `239` | **`dex-binary-diff-regression`** | Perform binary-level diffing between build versions to isolate patch regression evidence, compiler flag shifts, and unintended symbol removals using safe utilities (radiff2, diffoscope). | [dex-binary-diff-regression](.agents/skills/dex-binary-diff-regression/SKILL.md) |
| `240` | **`dex-reverse-evidence-chain`** | Establish immutable forensic evidence chains for authorized technical audits with cryptographic artifact hashing (SHA-256, BLAKE3), timestamped execution logs, toolchain provenance tracking, and objective observation reporting. | [dex-reverse-evidence-chain](.agents/skills/dex-reverse-evidence-chain/SKILL.md) |

### Group Y: Protocols & Service Integration (Skills 241–250)

| # | Skill ID | Description | Path |
|:---|:---|:---|:---|
| `241` | **`dex-mqtt-client-reliability`** | Architect resilient MQTT 3. | [dex-mqtt-client-reliability](.agents/skills/dex-mqtt-client-reliability/SKILL.md) |
| `242` | **`dex-websocket-session-recovery`** | Engineer self-healing WebSocket connection managers with bi-directional heartbeats, sequence-numbered message acknowledgement, backoff reconnection, and state synchronization. | [dex-websocket-session-recovery](.agents/skills/dex-websocket-session-recovery/SKILL.md) |
| `243` | **`dex-stream-processing-semantics`** | Design deterministic stream processing pipelines with Kafka/Pulsar partition ordering, consumer offset commits, idempotency keys, and at-least-once to exactly-once delivery semantics. | [dex-stream-processing-semantics](.agents/skills/dex-stream-processing-semantics/SKILL.md) |
| `244` | **`dex-event-schema-registry`** | Govern asynchronous event schemas using Confluent/Apicurio Schema Registry, enforcing Backward/Forward/Full compatibility rules, Avro/Protobuf/JSON Schema validation, and CI schema drift gates. | [dex-event-schema-registry](.agents/skills/dex-event-schema-registry/SKILL.md) |
| `245` | **`dex-http-client-connection-pooling`** | Benchmark and optimize HTTP client connection pools, socket reuse, keep-alive lifecycles, and DNS caching across high-throughput microservice communication. | [dex-http-client-connection-pooling](.agents/skills/dex-http-client-connection-pooling/SKILL.md) |
| `246` | **`dex-oauth-oidc-integration`** | Architect secure OAuth 2. | [dex-oauth-oidc-integration](.agents/skills/dex-oauth-oidc-integration/SKILL.md) |
| `247` | **`dex-webhook-signature-validation`** | Implement robust webhook ingestion endpoints with HMAC-SHA256 signature verification, replay attack prevention using timestamp tolerances, raw body preservation, and dead-letter queue routing. | [dex-webhook-signature-validation](.agents/skills/dex-webhook-signature-validation/SKILL.md) |
| `248` | **`dex-api-pagination-cursors`** | Engineer high-performance cursor-based and keyset pagination APIs, eliminating OFFSET performance degradation on millions of rows, handling opaque cursor token encoding, and ensuring stable bidirectional scrolling. | [dex-api-pagination-cursors](.agents/skills/dex-api-pagination-cursors/SKILL.md) |
| `249` | **`dex-service-contract-simulation`** | Construct hermetic wire-level mock virtualization and fault injection environments for external HTTP/gRPC APIs using WireMock, MSW, or Prism. | [dex-service-contract-simulation](.agents/skills/dex-service-contract-simulation/SKILL.md) |
| `250` | **`dex-offline-message-delivery`** | Design client-side outbox queues with persistent storage (IndexedDB/SQLite), automatic retry loops with jitter, idempotency token headers, and optimistic UI synchronization. | [dex-offline-message-delivery](.agents/skills/dex-offline-message-delivery/SKILL.md) |

### Group Z: AI Agent Operations (Skills 251–260)

| # | Skill ID | Description | Path |
|:---|:---|:---|:---|
| `251` | **`dex-llm-evaluation-dataset-design`** | Construct high-coverage, rubric-scored LLM evaluation datasets with golden baseline outputs, edge-case adversarial inputs, semantic diversity sampling, and automated scoring rubrics. | [dex-llm-evaluation-dataset-design](.agents/skills/dex-llm-evaluation-dataset-design/SKILL.md) |
| `252` | **`dex-agent-task-planning-validation`** | Validate AI agent task decomposition plans before execution, detecting dependency cycles, unachievable prerequisites, missing tool capabilities, and excessive scope creep. | [dex-agent-task-planning-validation](.agents/skills/dex-agent-task-planning-validation/SKILL.md) |
| `253` | **`dex-agent-trace-replay`** | Capture, serialize, and deterministically replay multi-turn AI agent execution traces, step-by-step tool invocations, and environmental observations for debugging and auditing. | [dex-agent-trace-replay](.agents/skills/dex-agent-trace-replay/SKILL.md) |
| `254` | **`dex-llm-human-review-gates`** | Design secure Human-in-the-Loop (HITL) review gates, authorization thresholds, risk-weighted approval policies, and non-blocking interactive approval modals for autonomous agent operations. | [dex-llm-human-review-gates](.agents/skills/dex-llm-human-review-gates/SKILL.md) |
| `255` | **`dex-retrieval-permission-filtering`** | Enforce document-level Access Control List (ACL) and multi-tenant security boundaries in Vector RAG pipelines before context injection, preventing unauthorized cross-tenant data leakage. | [dex-retrieval-permission-filtering](.agents/skills/dex-retrieval-permission-filtering/SKILL.md) |
| `256` | **`dex-multimodal-evaluation`** | Design evaluation harnesses for vision, audio, and document layout multimodal models, quantifying OCR extraction precision, chart interpretation accuracy, visual grounding, and hallucination rates. | [dex-multimodal-evaluation](.agents/skills/dex-multimodal-evaluation/SKILL.md) |
| `257` | **`dex-ai-safety-red-teaming`** | Conduct adversarial red-teaming simulations against AI agent pipelines, probing prompt injection, jailbreaks, indirect tool abuse, data exfiltration, and privilege escalation vulnerabilities. | [dex-ai-safety-red-teaming](.agents/skills/dex-ai-safety-red-teaming/SKILL.md) |
| `258` | **`dex-agent-long-running-task-checkpoints`** | Implement fault-tolerant checkpointing and resumption tokens for long-running AI agent workflows, persisting scratchpad states, tool execution graphs, and recovery idempotency. | [dex-agent-long-running-task-checkpoints](.agents/skills/dex-agent-long-running-task-checkpoints/SKILL.md) |
| `259` | **`dex-mcp-client-integration`** | Architect type-safe Model Context Protocol (MCP) client connections across Stdio and SSE transports, managing protocol handshakes, dynamic tool discovery, resource subscriptions, and strict schema validation. | [dex-mcp-client-integration](.agents/skills/dex-mcp-client-integration/SKILL.md) |
| `260` | **`dex-inference-latency-optimization`** | Profile and optimize end-to-end LLM inference latency, tuning Time-to-First-Token (TTFT), tokens-per-second throughput, KV-cache utilization, prompt prefix caching, and speculative decoding. | [dex-inference-latency-optimization](.agents/skills/dex-inference-latency-optimization/SKILL.md) |

---

## 3. Segregated Upstream Integrations (Isolated Capabilities)

Third-party imported skills are maintained in `integrations/` to prevent catalog count pollution:

| Source | Skill ID | Description | Path |
|:---|:---|:---|:---|
| **AAS** | `dex-api-mocking-virtualization` | Hermetic API mocking, WireMock integration, and MSW client interception. | [dex-api-mocking-virtualization](integrations/aas/dex-api-mocking-virtualization/SKILL.md) |
| **Reverse Skill** | `dex-binary-inspection` | Defensive static binary inspection, PE/ELF header analysis, and DLL auditing. | [dex-binary-inspection](integrations/reverse-skill/dex-binary-inspection/SKILL.md) |
| **Reverse Skill** | `dex-javascript-bundle-deobfuscation` | Deobfuscate minified JS/Electron bundles and audit exposed endpoints. | [dex-javascript-bundle-deobfuscation](integrations/reverse-skill/dex-javascript-bundle-deobfuscation/SKILL.md) |
| **REA** | `dex-rea-adapter` | Model Context Protocol (MCP) bridge connecting agents to REA tools. | [dex-rea-adapter](integrations/rea/dex-rea-adapter/SKILL.md) |
| **UI/UX Pro Max** | `dex-ui-ux-pro-max-adapter` | Design intelligence bridge to UI/UX Pro Max search engine for UI styles, palettes, and stacks. | [dex-ui-ux-pro-max-adapter](integrations/ui-ux-pro-max/dex-ui-ux-pro-max-adapter/SKILL.md) |
