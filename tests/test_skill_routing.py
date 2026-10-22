# -*- coding: utf-8 -*-
"""
Pytest suite for DEX Engineering Skills Pack v4.0: Routing Matrix Verification.
Tests the Master Orchestrator dynamic skill dispatch engine across 16 realistic scenarios (A through P)
covering all 12 specialized engineering groups and segregated upstream integrations.
"""

import os
import pytest

SCENARIOS = {
    "Scenario A: Emergency Database Migration Failure": {
        "description": "A production database migration failed halfway, causing locked tables and broken foreign keys.",
        "primary_skills": ["dex-root-cause-debugging", "dex-database-engineering", "dex-schema-evolution"],
        "complementary_skills": ["dex-disaster-recovery", "dex-production-monitoring", "dex-incident-postmortems"],
    },
    "Scenario B: AI-Powered Search & RAG Service Implementation": {
        "description": "Build an enterprise document search engine with hybrid dense/sparse retrieval and LLM summarization.",
        "primary_skills": ["dex-rag-pipelines", "dex-retrieval-evaluation", "dex-llm-integration"],
        "complementary_skills": ["dex-search-engineering", "dex-tool-calling-contracts", "dex-llm-cost-controls"],
    },
    "Scenario C: Monorepo Architecture Modernization": {
        "description": "Migrate 12 independent repositories into a governed monorepo with Turborepo remote caching and boundary rules.",
        "primary_skills": ["dex-monorepo-governance", "dex-repository-bootstrap", "dex-code-organization"],
        "complementary_skills": ["dex-developer-tooling", "dex-cicd-automation", "dex-semantic-version-automation"],
    },
    "Scenario D: High-Concurrency Real-time Collaborative Canvas": {
        "description": "Develop a real-time multiplayer whiteboard supporting 50,000 concurrent WebSocket connections.",
        "primary_skills": ["dex-realtime-protocols", "dex-concurrency-state", "dex-event-driven-architecture"],
        "complementary_skills": ["dex-caching-strategies", "dex-frontend-performance", "dex-performance-optimization"],
    },
    "Scenario E: Enterprise SaaS Multi-Tenant Isolation & Authentication": {
        "description": "Implement enterprise SSO, session revocation, and PostgreSQL Row-Level Security for a B2B SaaS platform.",
        "primary_skills": ["dex-auth-session-lifecycle", "dex-access-control-tenancy", "dex-secrets-management"],
        "complementary_skills": ["dex-security-audit", "dex-threat-modeling", "dex-database-engineering"],
    },
    "Scenario F: Mission-Critical Production Outage Postmortem": {
        "description": "Facilitate a blameless postmortem after a 45-minute checkout outage and track corrective action items.",
        "primary_skills": ["dex-incident-postmortems", "dex-production-monitoring", "dex-root-cause-debugging"],
        "complementary_skills": ["dex-reliability-engineering", "dex-slo-error-budgets", "dex-documentation-as-code"],
    },
    "Scenario G: Cross-Platform Windows & POSIX Developer CLI Tooling": {
        "description": "Develop a developer CLI in Rust/Node with WinGet package distribution, POSIX compliance, and shell completions.",
        "primary_skills": ["dex-cli-engineering", "dex-cross-platform-portability", "dex-windows-packaging"],
        "complementary_skills": ["dex-developer-tooling", "dex-plugin-architecture", "dex-release-engineering"],
    },
    "Scenario H: Automated Release & Semantic Versioning Pipeline": {
        "description": "Implement fully automated Conventional Commits parsing, CHANGELOG generation, and multi-registry publishing.",
        "primary_skills": ["dex-semantic-version-automation", "dex-release-engineering", "dex-cicd-automation"],
        "complementary_skills": ["dex-git-workflow", "dex-supply-chain-security", "dex-code-verification"],
    },
    "Scenario I: Data Contract Breaking Change Mitigation": {
        "description": "Detect breaking changes between upstream event producers and downstream analytics data pipelines.",
        "primary_skills": ["dex-data-contracts", "dex-schema-evolution", "dex-data-quality-audits"],
        "complementary_skills": ["dex-data-pipelines", "dex-data-lineage", "dex-api-contract-evolution"],
    },
    "Scenario J: Chaos Engineering & System Resilience Validation": {
        "description": "Design Toxiproxy network latency simulations and verify Cockatiel/Resilience4j circuit breaker fallback.",
        "primary_skills": ["dex-chaos-experiments", "dex-reliability-engineering", "dex-performance-optimization"],
        "complementary_skills": ["dex-production-monitoring", "dex-property-based-testing", "dex-capacity-planning"],
    },
    "Scenario K: Hermetic Offline Integration Testing & Mock Virtualization": {
        "description": "Run integration tests against third-party payments and logistics APIs completely offline without network flakes.",
        "primary_skills": ["dex-api-mocking-virtualization", "dex-testing-engineering", "dex-api-engineering"],
        "complementary_skills": ["dex-code-verification", "dex-cicd-automation"],
    },
    "Scenario L: Defensive Binary & Web Bundle Security Auditing": {
        "description": "Inspect compiled release executables (PE/ELF) and production JavaScript bundles for exposed endpoints and ASLR/DEP flags.",
        "primary_skills": ["dex-binary-inspection", "dex-javascript-bundle-deobfuscation", "dex-rea-adapter"],
        "complementary_skills": ["dex-security-audit", "dex-threat-modeling"],
    },
    "Scenario M: Zero-Downtime Multi-Region Kubernetes Rollout": {
        "description": "Deploy mission-critical payment services to Kubernetes with progressive Canary analysis and instant rollbacks.",
        "primary_skills": ["dex-zero-downtime-rollouts", "dex-kubernetes-deployment", "dex-slo-error-budgets"],
        "complementary_skills": ["dex-service-mesh-networking", "dex-distributed-tracing", "dex-container-image-engineering"],
    },
    "Scenario N: Offline-First Mobile Synchronization & Device Biometrics": {
        "description": "Build an offline-first mobile inspection app with local SQLite storage, mutation queues, and FaceID authentication.",
        "primary_skills": ["dex-mobile-offline-sync", "dex-android-app-architecture", "dex-native-device-integration"],
        "complementary_skills": ["dex-ios-app-architecture", "dex-mobile-performance-profiling", "dex-desktop-ipc-design"],
    },
    "Scenario O: FinOps Cloud Cost Anomaly & Resource Right-Sizing": {
        "description": "Investigate a 40% cloud bill surge, reclaim orphaned EBS volumes, right-size compute, and model unit economics.",
        "primary_skills": ["dex-cloud-cost-finops", "dex-infrastructure-as-code", "dex-capacity-planning"],
        "complementary_skills": ["dex-storage-lifecycle", "dex-cloud-service-integration"],
    },
    "Scenario P: Enterprise Compliance Audit & Tamper-Evident Logging": {
        "description": "Conduct SOC 2 Type II control mapping, configure append-only Merkle audit logs, and reconcile GitOps drift.",
        "primary_skills": ["dex-compliance-control-mapping", "dex-audit-trail-integrity", "dex-privacy-impact-assessment"],
        "complementary_skills": ["dex-configuration-drift", "dex-operational-readiness-review", "dex-runbook-automation"],
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
        for sub in ["aas", "reverse-skill", "rea"]:
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
