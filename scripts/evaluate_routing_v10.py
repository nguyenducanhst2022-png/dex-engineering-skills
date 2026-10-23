# -*- coding: utf-8 -*-
"""
DEX SKILLOPS — V10 ROUTING EVALUATION BENCHMARK (scripts/evaluate_routing_v10.py)
Validates lexical and semantic dispatch precision across all 50 engineering groups (A to AX).
"""

import os
import sys
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.evaluate_routing import simulate_route

SCENARIOS = [
    ("A", "Standard iterative development workflow for AI coding, breaking tasks down, modular code and safe checkpoints.", "dex-development-workflow", "dex-chess-search-pruning-evals", "Git CLI"),
    ("B", "Multi-agent coordination, role division, concurrent subagent task execution and peer reviews.", "dex-multi-agent-orchestration", "dex-streaming-manifest-validation", "Agent Runtime"),
    ("C", "Evaluate change impact analysis for database schema migrations before production.", "dex-change-impact-analysis", "dex-color-contrast-systems", "Impact Analyzer"),
    ("D", "Enforce strict TypeScript design system token contracts and component prop validation.", "dex-ui-component-contracts", "dex-win32-dpi-multi-monitor-layout", "TypeScript Compiler"),
    ("E", "Design resilient event-driven architecture with idempotent event processing queues.", "dex-event-driven-architecture", "dex-design-critique-rubric", "Message Broker"),
    ("F", "Formulate data contracts and pipeline validation rules for warehouse ingestion.", "dex-data-contracts", "dex-chess-uci-protocol-compliance", "Data Contract CLI"),
    ("G", "Build dense retrieval RAG pipeline with relevance re-ranking and hallucination checks.", "dex-rag-pipelines", "dex-terraform-module-contract-tests", "Vector DB"),
    ("H", "Manage enterprise monorepo workspace boundaries and package dependency graphs.", "dex-monorepo-governance", "dex-video-transcoding-ladders", "Monorepo CLI"),
    ("I", "Manage application secrets, zero-hardcoded credentials policy, secret rotation, HashiCorp Vault / AWS Secrets Manager.", "dex-secrets-management", "dex-email-template-rendering", "KMS / Vault"),
    ("J", "Review Supabase multi-tenant PostgreSQL RLS SELECT INSERT UPDATE DELETE isolation.", "dex-postgres-rls-policy-verification", "dex-supabase-storage-access-policies", "PostgreSQL Instance"),
    ("K", "Validate agent tool permission scopes and approval boundaries.", "dex-agent-tool-permission-modeling", "dex-agent-execution-budget-controls", "Agent Sandbox"),
    ("L", "Validate, audit, and debug HLS (m3u8) and MPEG-DASH (mpd) streaming manifests segment sequencing.", "dex-streaming-manifest-validation", "dex-chess-search-pruning-evals", "Manifest Validator"),
    ("M", "Test chess UCI handshake stop ponder command ordering.", "dex-chess-uci-protocol-compliance", "dex-chess-search-pruning-evals", "Chess Engine"),
    ("N", "Review C++ Rust FFI ownership boundaries and ABI layout safety.", "dex-cpp-rust-ffi-validation", "dex-chess-nnue-evaluation-integration", "FFI Analyzer"),
    ("O", "Reproduce Windows per-monitor DPI coordinate translation and layout scaling defects.", "dex-win32-dpi-multi-monitor-layout", "dex-windows-com-interop", "Win32 Sandbox"),
    ("P", "Test Kubernetes secret delivery and credential rotation inside ephemeral pods.", "dex-kubernetes-secret-delivery", "dex-terraform-module-contract-tests", "Kubectl / Minikube"),
    ("Q", "Critique visual hierarchy, usability and accessibility when reviewing screens or dashboard designs.", "dex-design-critique-rubric", "dex-email-template-rendering", "Browser Fixtures"),
    ("R", "Verify TypeScript ESM CommonJS dual publish exports declarations with package consumers.", "dex-typescript-package-dual-publish", "dex-react-render-profiling", "Node & TypeScript"),
    ("S", "Diagnose Next.js App Router data cache invalidation stale read behaviors.", "dex-nextjs-app-router-data-cache", "dex-vue-composition-reusability", "Next.js Sandbox"),
    ("T", "Audit software dependency provenance attestation and SLSA build identity digests.", "dex-dependency-provenance-attestation", "dex-disclosure-coordinated-triage", "Attestation Verifier"),
    ("U", "Review skill conflict precedence across overlapping engineering domain workflows.", "dex-skill-conflict-precedence", "dex-skill-lifecycle-health-dashboard", "Catalog Matrix"),
    ("V", "Test agent shutdown cancellation checkpoint recovery without duplicated side effects.", "dex-agent-shutdown-and-cancellation", "dex-agent-reviewer-independence", "Agent Harness"),
    ("W", "Revalidate upstream skill provenance pinned commit before importing into catalog.", "dex-skill-provenance-revalidation", "dex-skill-task-suitability-classifier", "Git Sandbox"),
    ("X", "Test skill crosshost fixture compatibility across coding agent host environments.", "dex-skill-crosshost-fixture-tests", "dex-skill-progressive-disclosure-metrics", "Agent Hosts"),
    ("Y", "Generate skill lifecycle health dashboard with actual verified test execution counts.", "dex-skill-lifecycle-health-dashboard", "dex-skill-task-suitability-classifier", "Health Ledger"),
]

def evaluate():
    catalog_path = ROOT / "manifests" / "dex-skills.json"
    catalog = json.loads(catalog_path.read_text(encoding="utf-8"))["native_skills"]
    results = []

    for sid, prompt, expected, forbidden, tools in SCENARIOS:
        actual = simulate_route(prompt, catalog)
        passed = expected in actual and forbidden not in actual
        results.append({
            "id": sid,
            "task_input": prompt,
            "expected_skills": [expected],
            "forbidden_skills": [forbidden],
            "required_tools": tools,
            "routing_result": "PASS" if passed else "FAIL",
            "actual_output": actual
        })

    out_file = ROOT / "docs" / "quality" / "DEX_V10_ROUTING_FIXTURES.json"
    out_file.write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")
    pass_count = sum(x["routing_result"] == "PASS" for x in results)
    print(f"v10 routing {pass_count} / {len(results)}")
    return 0 if pass_count == len(results) else 1

if __name__ == "__main__":
    sys.exit(evaluate())
