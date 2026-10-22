# -*- coding: utf-8 -*-
"""
Pytest suite for DEX Engineering Skills Framework v6.0: Routing Matrix Verification.
Tests the Master Orchestrator dynamic skill dispatch engine across 30 realistic scenarios (A through AD)
covering all 30 specialized engineering groups (Groups A to AD) and segregated upstream integrations.
"""

import os
import pytest

SCENARIOS = {
    "Scenario A: Core Engineering Workflow & Git Governance (Group A)": {
        "description": "Establish standardized development workflows, trunk-based Git hygiene, and atomic branch isolation.",
        "primary_skills": ["dex-development-workflow", "dex-git-workflow", "dex-code-organization"],
        "complementary_skills": ["dex-repository-bootstrap", "dex-semantic-version-automation"],
    },
    "Scenario B: Multi-Agent Architecture & Coordination (Group B)": {
        "description": "Design modular multi-agent orchestration frameworks with delegation boundaries and supervision contracts.",
        "primary_skills": ["dex-multi-agent-orchestration", "dex-software-architecture", "dex-agent-engineering"],
        "complementary_skills": ["dex-tool-calling-contracts", "dex-concurrency-state"],
    },
    "Scenario C: Production Reliability & Progressive Rollouts (Group C)": {
        "description": "Analyze change blast radiuses, configure dynamic feature toggles, and enforce error budget policies.",
        "primary_skills": ["dex-change-impact-analysis", "dex-feature-flags", "dex-reliability-engineering"],
        "complementary_skills": ["dex-zero-downtime-rollouts", "dex-production-monitoring"],
    },
    "Scenario D: Frontend Performance & Core Web Vitals (Group D)": {
        "description": "Optimize critical rendering path, eliminate layout shifts, and automate visual regression test suites.",
        "primary_skills": ["dex-frontend-performance", "dex-visual-regression", "dex-forms-and-validation"],
        "complementary_skills": ["dex-accessibility-automation", "dex-design-handoff-verification"],
    },
    "Scenario E: Event-Driven Backend & Distributed Processing (Group E)": {
        "description": "Build asynchronous event-driven pipelines with idempotent consumer semantics and resilient background workers.",
        "primary_skills": ["dex-event-driven-architecture", "dex-idempotent-operations", "dex-background-job-queues"],
        "complementary_skills": ["dex-api-engineering", "dex-distributed-consistency"],
    },
    "Scenario F: Data Contracts & Storage Optimization (Group F)": {
        "description": "Enforce schema compatibility between streaming producers and consumers while tuning complex SQL execution plans.",
        "primary_skills": ["dex-data-contracts", "dex-data-pipelines", "dex-database-query-plans"],
        "complementary_skills": ["dex-database-engineering", "dex-schema-evolution"],
    },
    "Scenario G: Enterprise RAG & Retrieval Quality Engineering (Group G)": {
        "description": "Implement hybrid dense/sparse vector retrieval with cross-encoder reranking and token cost guardrails.",
        "primary_skills": ["dex-rag-pipelines", "dex-retrieval-evaluation", "dex-llm-cost-controls"],
        "complementary_skills": ["dex-llm-integration", "dex-reranking-strategies"],
    },
    "Scenario H: Governed Monorepo & Cross-Platform Tooling (Group H)": {
        "description": "Standardize cross-boundary monorepos, high-performance developer CLIs, and automated semantic release workflows.",
        "primary_skills": ["dex-monorepo-governance", "dex-cli-engineering", "dex-semantic-version-automation"],
        "complementary_skills": ["dex-developer-tooling", "dex-cicd-automation"],
    },
    "Scenario I: Threat Modeling & Defensive Secrets Lifecycle (Group I)": {
        "description": "Conduct STRIDE threat modeling sessions, establish zero-trust identity policies, and manage short-lived secret leases.",
        "primary_skills": ["dex-threat-modeling", "dex-secrets-management", "dex-security-audit"],
        "complementary_skills": ["dex-auth-session-lifecycle", "dex-access-control-tenancy"],
    },
    "Scenario J: Cloud-Native Containers & Kubernetes Orchestration (Group J)": {
        "description": "Engineer multi-stage unprivileged OCI container images and deploy zero-downtime Kubernetes applications.",
        "primary_skills": ["dex-container-image-engineering", "dex-kubernetes-deployment", "dex-zero-downtime-rollouts"],
        "complementary_skills": ["dex-service-mesh-networking", "dex-kubernetes-policy-enforcement"],
    },
    "Scenario K: Mobile Offline Synchronization & Native Device Access (Group K)": {
        "description": "Architect offline-first mobile synchronization engines with conflict resolution and biometric hardware integration.",
        "primary_skills": ["dex-android-app-architecture", "dex-mobile-offline-sync", "dex-native-device-integration"],
        "complementary_skills": ["dex-ios-app-architecture", "dex-mobile-performance-profiling"],
    },
    "Scenario L: Compliance Control Mapping & Operational Readiness (Group L)": {
        "description": "Map SOC2/ISO controls to automated infrastructure evidence and conduct operational readiness reviews prior to launch.",
        "primary_skills": ["dex-operational-readiness-review", "dex-compliance-control-mapping", "dex-privacy-impact-assessment"],
        "complementary_skills": ["dex-audit-trail-integrity", "dex-configuration-drift"],
    },
    "Scenario M: Advanced Verification & Mutation Testing (Group M)": {
        "description": "Evaluate test quality through mutation survival analysis, quarantine flaky tests, and verify formal system invariants.",
        "primary_skills": ["dex-mutation-testing", "dex-flaky-test-remediation", "dex-coverage-risk-analysis"],
        "complementary_skills": ["dex-differential-testing", "dex-formal-invariant-checks"],
    },
    "Scenario N: Distributed Systems Resilience & Traffic Shaping (Group N)": {
        "description": "Simulate peak traffic stress, design adaptive token-bucket rate limiters, and enforce backpressure load shedding.",
        "primary_skills": ["dex-load-and-stress-testing", "dex-rate-limiting-quotas", "dex-traffic-shaping-backpressure"],
        "complementary_skills": ["dex-service-failover", "dex-distributed-consistency"],
    },
    "Scenario O: Cloud Platform Governance & GitOps Workflows (Group O)": {
        "description": "Audit least-privilege IAM policies, manage internal developer service catalogs, and reconcile declarative GitOps state.",
        "primary_skills": ["dex-cloud-iam-policy-review", "dex-gitops-workflows", "dex-kubernetes-policy-enforcement"],
        "complementary_skills": ["dex-platform-service-catalog", "dex-cloud-resource-tagging"],
    },
    "Scenario P: Specialized Language & Systems Runtime Diagnostics (Group P)": {
        "description": "Audit Rust unsafe blocks for UB hazards, profile JVM garbage collection pauses, and diagnose Node event loop latency.",
        "primary_skills": ["dex-rust-unsafe-audit", "dex-cpp-memory-safety", "dex-nodejs-runtime-diagnostics"],
        "complementary_skills": ["dex-go-concurrency-patterns", "dex-jvm-performance-diagnostics"],
    },
    "Scenario Q: Advanced Multi-Agent MCP Protocols & Vector Indexing (Group Q)": {
        "description": "Implement Model Context Protocol (MCP) servers, construct HNSW vector indices, and enforce structured JSON schemas.",
        "primary_skills": ["dex-mcp-server-design", "dex-vector-index-design", "dex-reranking-strategies"],
        "complementary_skills": ["dex-structured-llm-output", "dex-agent-memory-governance"],
    },
    "Scenario R: User Experience Journey Mapping & Accessibility (Group R)": {
        "description": "Map complex user purchase funnels, automate WCAG 2.2 AA accessibility audits, and verify design token handoffs.",
        "primary_skills": ["dex-user-journey-mapping", "dex-accessibility-automation", "dex-design-handoff-verification"],
        "complementary_skills": ["dex-product-requirements-writing", "dex-usability-study-design"],
    },
    "Scenario S: Application Security Defense & Supply Chain Verification (Group S)": {
        "description": "Triage SAST findings, sign and verify cryptographic SBOMs, and harden production browser extension execution context.",
        "primary_skills": ["dex-sast-finding-triage", "dex-sbom-verification", "dex-browser-extension-hardening"],
        "complementary_skills": ["dex-api-abuse-prevention", "dex-cryptographic-api-review"],
    },
    "Scenario T: Autonomous SkillOps Lifecycle & Provenance Auditing (Group T)": {
        "description": "Index skill catalogs, execute dynamic security screening, benchmark routing accuracy, and track upstream sync provenance.",
        "primary_skills": ["dex-skill-discovery-indexer", "dex-skill-security-screening", "dex-skill-upstream-sync"],
        "complementary_skills": ["dex-skill-quality-benchmarking", "dex-skill-dependency-graph"],
    },
    "Scenario U: Visual Design Intelligence & Theme Systems (Group U)": {
        "description": "Synthesize visual design briefs, audit typographic hierarchy, enforce APCA/WCAG contrast ratios, and generate design tokens.",
        "primary_skills": ["dex-design-brief-synthesis", "dex-visual-hierarchy-audit", "dex-color-contrast-systems"],
        "complementary_skills": ["dex-fluid-typography-engineering", "dex-layout-composition-patterns"],
    },
    "Scenario V: Advanced Web Experiences & Offline Delivery (Group V)": {
        "description": "Profile 60fps web animation performance, engineer offline-first progressive web apps with service workers, and virtualize massive datasets.",
        "primary_skills": ["dex-web-animation-performance", "dex-progressive-web-apps", "dex-virtualized-infinite-lists"],
        "complementary_skills": ["dex-web-canvas-rendering", "dex-hls-dash-playback"],
    },
    "Scenario W: Browser Extensions & CDP Automation (Group W)": {
        "description": "Architect Manifest V3 browser extensions, secure isolated content script message channels, and automate deep CDP observability.",
        "primary_skills": ["dex-browser-extension-mv3", "dex-extension-message-security", "dex-browser-automation-testing"],
        "complementary_skills": ["dex-extension-background-lifecycle", "dex-cdp-observability"],
    },
    "Scenario X: Authorized Reverse Engineering & Binary Inspection (Group X)": {
        "description": "Inspect PE/COFF and ELF binary headers, reconstruct control flow graphs from disassembly, and resolve unstripped debug symbols.",
        "primary_skills": ["dex-pe-elf-structure-inspection", "dex-native-symbol-mapping", "dex-disassembly-cfg-reconstruction"],
        "complementary_skills": ["dex-managed-assembly-inspection", "dex-reverse-evidence-chain"],
    },
    "Scenario Y: Protocols, Webhooks & Real-Time Messaging (Group Y)": {
        "description": "Harden MQTT IoT client reliability with QoS session preservation, recover interrupted WebSocket sessions, and verify HMAC webhook signatures.",
        "primary_skills": ["dex-mqtt-client-reliability", "dex-websocket-session-recovery", "dex-webhook-signature-validation"],
        "complementary_skills": ["dex-http-client-connection-pooling", "dex-service-contract-simulation"],
    },
    "Scenario Z: AI Agent Operations & Red Teaming (Group Z)": {
        "description": "Curate representative golden datasets for LLM benchmarking, validate multi-step agent plans against safety constraints, and enforce human review gates.",
        "primary_skills": ["dex-llm-evaluation-dataset-design", "dex-agent-task-planning-validation", "dex-llm-human-review-gates"],
        "complementary_skills": ["dex-agent-trace-replay", "dex-ai-safety-red-teaming"],
    },
    "Scenario AA: Advanced Data Analytics & Anomaly Detection (Group AA)": {
        "description": "Model unified SQL metric semantic layers, detect streaming statistical time series anomalies, and optimize columnar warehouse queries.",
        "primary_skills": ["dex-sql-metric-semantic-layer", "dex-data-anomaly-detection", "dex-data-warehouse-cost-tuning"],
        "complementary_skills": ["dex-geospatial-data-pipelines", "dex-stream-processing-semantics"],
    },
    "Scenario AB: Native Systems, Graphics & Simulation (Group AB)": {
        "description": "Implement alpha-beta minimax chess search with bitboards, enforce deterministic fixed-point physics simulations, and manage GPU shader buffers.",
        "primary_skills": ["dex-chess-engine-search-testing", "dex-simulation-determinism", "dex-game-loop-timing"],
        "complementary_skills": ["dex-webgpu-rendering-fundamentals", "dex-gpu-shader-profiling"],
    },
    "Scenario AC: Software Trust, Licensing & Reproducible Distribution (Group AC)": {
        "description": "Audit dual-license compliance and copyleft obligations, verify Sigstore/Cosign container signatures, and enforce HSM code signing.",
        "primary_skills": ["dex-open-source-license-scanning", "dex-artifact-signature-verification", "dex-code-signing-release-process"],
        "complementary_skills": ["dex-software-update-trust-chains", "dex-release-reproducibility-audit"],
    },
    "Scenario AD: Advanced SkillOps Governance & Drift Prevention (Group AD)": {
        "description": "Govern multi-tier skill catalog taxonomies, verify SHA256 integrity trees against tampering, and record immutable execution ledgers.",
        "primary_skills": ["dex-skill-catalog-taxonomy", "dex-skill-source-integrity", "dex-skill-execution-evidence-ledger"],
        "complementary_skills": ["dex-skill-routing-conflict-tests", "dex-skill-documentation-drift"],
    },
}

class RoutingEngine:
    """Simulates the Master Orchestrator dynamic skill dispatch engine."""
    def __init__(self, catalog):
        self.catalog = catalog

    def route_scenario(self, scenario_name):
        spec = SCENARIOS.get(scenario_name)
        if not spec:
            raise ValueError(f"Unknown scenario: {scenario_name}")
        return spec["primary_skills"], spec["complementary_skills"]

@pytest.fixture
def available_skills():
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    skills = set()
    
    # 1. Native DEX Skills in .agents/skills
    native_dir = os.path.join(root, ".agents", "skills")
    if os.path.isdir(native_dir):
        for d in os.listdir(native_dir):
            if os.path.isdir(os.path.join(native_dir, d)):
                skills.add(d)

    # 2. Segregated Upstream Integrations in integrations/
    int_dir = os.path.join(root, "integrations")
    if os.path.isdir(int_dir):
        for sub in os.listdir(int_dir):
            sub_path = os.path.join(int_dir, sub)
            if os.path.isdir(sub_path):
                for d in os.listdir(sub_path):
                    if os.path.isdir(os.path.join(sub_path, d)):
                        skills.add(d)
                        
    return skills

@pytest.mark.parametrize("scenario_key", list(SCENARIOS.keys()))
def test_scenario_routing_validity(scenario_key, available_skills):
    """Verify that every scenario in the routing matrix routes to valid, existing skills."""
    engine = RoutingEngine(available_skills)
    primaries, complementaries = engine.route_scenario(scenario_key)

    assert len(primaries) >= 2, f"Scenario {scenario_key} must have at least 2 primary skills"
    assert len(complementaries) >= 2, f"Scenario {scenario_key} must have at least 2 complementary skills"

    for skill in primaries:
        assert skill in available_skills, f"Primary skill '{skill}' from {scenario_key} not found in skills catalog"

    for skill in complementaries:
        assert skill in available_skills, f"Complementary skill '{skill}' from {scenario_key} not found in skills catalog"
