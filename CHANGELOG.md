# Changelog

All notable changes to the **DEX Engineering Skills Pack** are documented in this file.
This project strictly adheres to [Semantic Versioning 2.0.0](https://semver.org/).

---

## [4.0.0] - 2026-10-22

### Added — 30 New Specialized Skills across 3 New Disciplines (Groups J, K, L)
- **Group J: Cloud & Infrastructure (Skills 91–100)**:
  - `dex-container-image-engineering` (91): Minimal container images, multi-stage builds, non-root users, SBOM, and Trivy CVE scanning.
  - `dex-kubernetes-deployment` (92): Kubernetes workloads, probes, resource limits, PodDisruptionBudgets, and rolling updates.
  - `dex-infrastructure-as-code` (93): Terraform/OpenTofu, remote state locking, drift detection, and Checkov compliance scanning.
  - `dex-cloud-service-integration` (94): Workload Identity Federation, exponential backoff with jitter, and least privilege IAM.
  - `dex-zero-downtime-rollouts` (95): Blue-green and Argo canary rollouts with automated Prometheus metric gating.
  - `dex-service-mesh-networking` (96): Istio/Linkerd mTLS, fine-grained traffic routing, circuit breaking, and Envoy outlier detection.
  - `dex-network-troubleshooting` (97): DNS resolution, TLS cert chains, TCP connection states, HTTP latency, and tcpdump packet analysis.
  - `dex-slo-error-budgets` (98): SLIs, SLOs, rolling error budgets, multi-window burn rate alerting, and deployment freeze policies.
  - `dex-distributed-tracing` (99): OpenTelemetry standard instrumentation, W3C tracecontext propagation, and bottleneck latency analysis.
  - `dex-cloud-cost-finops` (100): Cost allocation tags, right-sizing, idle asset reclamation, savings plans, and unit economics.
- **Group K: Mobile & Desktop Engineering (Skills 101–110)**:
  - `dex-android-app-architecture` (101): Modern Android architecture with Jetpack Compose, MVVM/MVI, StateFlow, Room DB, and Hilt.
  - `dex-ios-app-architecture` (102): Modern iOS architecture with SwiftUI, Swift Concurrency (async/await, Actor), NavigationStack, and SwiftData.
  - `dex-electron-security` (103): Hardened Electron security with contextIsolation, nodeIntegration disabled, sandbox, and minimal contextBridge.
  - `dex-tauri-desktop-integration` (104): Lightweight Tauri v2 architecture with Rust backend commands, strict capabilities, and native controls.
  - `dex-mobile-offline-sync` (105): Offline-first architecture with local SQLite, mutation sync queues, CRDT/LWW conflict resolution, and background workers.
  - `dex-mobile-release-pipelines` (106): Fastlane mobile CI/CD pipelines, Android keystore signing, Match provisioning, and store distribution.
  - `dex-mobile-performance-profiling` (107): Mobile startup time profiling (TTID/TTFD), frame jank detection (60/120 fps), LeakCanary, and battery optimization.
  - `dex-desktop-ipc-design` (108): Type-safe desktop IPC interfaces using Zod/JSON Schema, bi-directional events, and main-process input validation.
  - `dex-native-device-integration` (109): Hardware device capabilities (Camera, Geolocation, Bluetooth BLE, Biometrics) with runtime permissions and fallbacks.
  - `dex-desktop-update-delivery` (110): Secure desktop auto-updates with cryptographic signatures (Minisign/Ed25519), delta updates, and atomic rollbacks.
- **Group L: Product & Operations Engineering (Skills 111–120)**:
  - `dex-privacy-impact-assessment` (111): GDPR/CCPA DPIA assessments, personal data classification, data minimization, and user rights automation.
  - `dex-compliance-control-mapping` (112): SOC 2 Type II, ISO 27001, HIPAA control mapping, and continuous automated evidence collection.
  - `dex-audit-trail-integrity` (113): Append-only tamper-evident audit logging with Merkle hash chaining, S3 Object Lock (WORM), and CloudEvents schema.
  - `dex-configuration-drift` (114): Continuous drift detection and automated self-healing across Kubernetes GitOps (ArgoCD/Flux) and Terraform.
  - `dex-product-discovery` (115): Structured product discovery, Jobs-to-be-Done (JTBD), Opportunity Solution Trees, and rapid prototyping hypothesis testing.
  - `dex-feature-prioritization` (116): Quantitative feature prioritization using RICE scoring, Value vs Effort, WSJF, and dependency graph analysis.
  - `dex-analytics-instrumentation` (117): Strict tracking plans, object_action taxonomy, Zod schemas, automated PII scrubbing, and dual client/server verification.
  - `dex-feedback-triage` (118): High-velocity user feedback classification, bug severity triage, semantic deduplication, and reproduction recipes.
  - `dex-runbook-automation` (119): Executable runbooks (SOPs) with pre-flight checks, interactive approval gates, guarded commands, and rollback procedures.
  - `dex-operational-readiness-review` (120): Production Operational Readiness Reviews (ORR) across reliability, security, observability, DR, and supportability.

### Changed
- **Total Native Skills Count**: Expanded to exactly **120 Specialized Skills + 1 Master Orchestrator (121 Skills Total)** in `.agents/skills/`.
- **Master Orchestrator Upgraded**: Updated `dex-master-orchestrator` with complete routing coverage across all 12 domains (Groups A–L) and 12 Quality Gates (QG-01 to QG-12).
- **Segregated Integration Architecture**: Relocated third-party upstream skills to `integrations/` (`integrations/aas`, `integrations/reverse-skill`, `integrations/rea`) ensuring clean segregation from native numbering.
- **Routing Matrix Expanded**: Added Scenarios M, N, O, P covering Cloud, Mobile, FinOps, and Compliance.
