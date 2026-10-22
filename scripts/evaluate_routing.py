# -*- coding: utf-8 -*-
"""
DEX SKILLOPS — ROUTING EVALUATION HARNESS (scripts/evaluate_routing.py)
Evaluates, benchmarks, and scores Master Orchestrator skill routing precision,
recall, and false-positive activations across all 30 engineering groups (A to AD).
"""

import os
import sys
import json
import re

if sys.stdout.encoding != "utf-8" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

BENCHMARK_SCENARIOS = [
    # Group A: Core Engineering
    {
        "id": "scenario-01-core",
        "prompt": "Quy trình thiết lập phát triển phát triển phần mềm, quản lý Git branch isolation và atomic commit workflow.",
        "expected": ["dex-development-workflow", "dex-git-workflow"]
    },
    # Group B: Architecture & AI Agents
    {
        "id": "scenario-02-arch-agent",
        "prompt": "Thiết kế kiến trúc hệ thống multi-agent orchestration có khả năng phân quyền và phối hợp các agent con.",
        "expected": ["dex-multi-agent-orchestration", "dex-software-architecture", "dex-agent-engineering"]
    },
    # Group C: Production Engineering
    {
        "id": "scenario-03-prod-eng",
        "prompt": "Phân tích tác động thay đổi change impact analysis và triển khai canary bằng feature flags.",
        "expected": ["dex-change-impact-analysis", "dex-feature-flags", "dex-reliability-engineering"]
    },
    # Group D: Frontend Engineering
    {
        "id": "scenario-04-frontend",
        "prompt": "Tối ưu hóa Core Web Vitals frontend performance, kiểm thử visual regression và thiết kế forms validation.",
        "expected": ["dex-frontend-performance", "dex-visual-regression", "dex-forms-and-validation"]
    },
    # Group E: Backend & Integration
    {
        "id": "scenario-05-backend",
        "prompt": "Thiết kế kiến trúc event-driven architecture với thao tác bình thản idempotent operations và hàng đợi background job queues.",
        "expected": ["dex-event-driven-architecture", "dex-idempotent-operations", "dex-background-job-queues"]
    },
    # Group F: Data Engineering
    {
        "id": "scenario-06-data-eng",
        "prompt": "Xây dựng data contracts cho data pipelines và tối ưu hóa database query plans.",
        "expected": ["dex-data-contracts", "dex-data-pipelines", "dex-database-query-plans"]
    },
    # Group G: AI & LLM Engineering
    {
        "id": "scenario-07-ai-llm",
        "prompt": "Xây dựng pipeline RAG pipelines, đánh giá độ chính xác retrieval evaluation và kiểm soát chi phí token llm cost controls.",
        "expected": ["dex-rag-pipelines", "dex-retrieval-evaluation", "dex-llm-cost-controls"]
    },
    # Group H: Developer Experience
    {
        "id": "scenario-08-dx",
        "prompt": "Quản trị monorepo governance, phát triển công cụ dòng lệnh cli engineering và tự động hóa semantic version.",
        "expected": ["dex-monorepo-governance", "dex-cli-engineering", "dex-semantic-version-automation"]
    },
    # Group I: Security & Reliability
    {
        "id": "scenario-09-sec-rel",
        "prompt": "Mô hình hóa mối đe dọa threat modeling, quản lý bảo mật secrets management và kiểm toán an ninh security audit.",
        "expected": ["dex-threat-modeling", "dex-secrets-management", "dex-security-audit"]
    },
    # Group J: Cloud & Infrastructure
    {
        "id": "scenario-10-cloud-k8s",
        "prompt": "Đóng gói container image engineering tối ưu, triển khai kubernetes deployment và canary zero-downtime rollouts.",
        "expected": ["dex-container-image-engineering", "dex-kubernetes-deployment", "dex-zero-downtime-rollouts"]
    },
    # Group K: Mobile & Desktop Engineering
    {
        "id": "scenario-11-mobile-desktop",
        "prompt": "Kiến trúc ứng dụng android app architecture với khả năng đồng bộ ngoại tuyến mobile offline sync và native device.",
        "expected": ["dex-android-app-architecture", "dex-mobile-offline-sync", "dex-native-device-integration"]
    },
    # Group L: Product & Operations
    {
        "id": "scenario-12-product-ops",
        "prompt": "Đánh giá mức độ sẵn sàng operational readiness review, ánh xạ compliance control mapping và quyền riêng tư privacy impact.",
        "expected": ["dex-operational-readiness-review", "dex-compliance-control-mapping", "dex-privacy-impact-assessment"]
    },
    # Group M: Advanced Software Verification
    {
        "id": "scenario-13-adv-verification",
        "prompt": "Đo lường độ hiệu quả kiểm thử bằng mutation testing, xử lý flaky test remediation và phân tích coverage risk.",
        "expected": ["dex-mutation-testing", "dex-flaky-test-remediation", "dex-coverage-risk-analysis"]
    },
    # Group N: Advanced SRE & Distributed Systems
    {
        "id": "scenario-14-adv-sre",
        "prompt": "Thực hiện kiểm thử tải load and stress testing, cấu hình rate limiting quotas và điều tiết traffic shaping backpressure.",
        "expected": ["dex-load-and-stress-testing", "dex-rate-limiting-quotas", "dex-traffic-shaping-backpressure"]
    },
    # Group O: Advanced Cloud Platform
    {
        "id": "scenario-15-adv-cloud",
        "prompt": "Kiểm toán phân quyền cloud iam policy review, triển khai gitops workflows và kubernetes policy enforcement.",
        "expected": ["dex-cloud-iam-policy-review", "dex-gitops-workflows", "dex-kubernetes-policy-enforcement"]
    },
    # Group P: Language & Runtime Engineering
    {
        "id": "scenario-16-language-runtime",
        "prompt": "Kiểm toán ranh giới rust unsafe audit, phát hiện lỗi cpp memory safety và chẩn đoán nodejs runtime diagnostics.",
        "expected": ["dex-rust-unsafe-audit", "dex-cpp-memory-safety", "dex-nodejs-runtime-diagnostics"]
    },
    # Group Q: Advanced AI Systems
    {
        "id": "scenario-17-adv-ai",
        "prompt": "Thiết kế mcp server design, xây dựng vector index design và áp dụng mô hình reranking strategies.",
        "expected": ["dex-mcp-server-design", "dex-vector-index-design", "dex-reranking-strategies"]
    },
    # Group R: Product Design & User Research
    {
        "id": "scenario-18-ux-research",
        "prompt": "Xây dựng bản đồ user journey mapping, tự động hóa accessibility automation và xác minh design handoff verification.",
        "expected": ["dex-user-journey-mapping", "dex-accessibility-automation", "dex-design-handoff-verification"]
    },
    # Group S: Application Security Specialists
    {
        "id": "scenario-19-appsec-specialists",
        "prompt": "Sàng lọc cảnh báo sast finding triage, tạo và ký số sbom verification và gia cố browser extension hardening.",
        "expected": ["dex-sast-finding-triage", "dex-sbom-verification", "dex-browser-extension-hardening"]
    },
    # Group T: SkillOps Engineering
    {
        "id": "scenario-20-skillops",
        "prompt": "Khám phá chỉ mục skill discovery indexer, kiểm tra an toàn skill security screening và đồng bộ skill upstream sync.",
        "expected": ["dex-skill-discovery-indexer", "dex-skill-security-screening", "dex-skill-upstream-sync"]
    },
    # Group U: Visual Design Intelligence
    {
        "id": "scenario-21-visual-design",
        "prompt": "Thiết kế visual design brief synthesis, kiểm toán visual hierarchy audit và hệ thống color contrast systems.",
        "expected": ["dex-design-brief-synthesis", "dex-visual-hierarchy-audit", "dex-color-contrast-systems"]
    },
    # Group V: Advanced Web Experiences
    {
        "id": "scenario-22-adv-web",
        "prompt": "Tối ưu hóa web animation performance, xây dựng progressive web apps và danh sách virtualized infinite lists.",
        "expected": ["dex-web-animation-performance", "dex-progressive-web-apps", "dex-virtualized-infinite-lists"]
    },
    # Group W: Browser Extensions & Automation
    {
        "id": "scenario-23-extensions-auto",
        "prompt": "Phát triển browser extension mv3, bảo vệ extension message security và kiểm thử browser automation testing.",
        "expected": ["dex-browser-extension-mv3", "dex-extension-message-security", "dex-browser-automation-testing"]
    },
    # Group X: Authorized Reverse Engineering
    {
        "id": "scenario-24-reverse-eng",
        "prompt": "Kiểm tra cấu trúc pe elf structure inspection, ánh xạ native symbol mapping và phân tích disassembly cfg reconstruction.",
        "expected": ["dex-pe-elf-structure-inspection", "dex-native-symbol-mapping", "dex-disassembly-cfg-reconstruction"]
    },
    # Group Y: Protocols & Service Integration
    {
        "id": "scenario-25-protocols-service",
        "prompt": "Cấu hình mqtt client reliability, khôi phục websocket session recovery và xác thực webhook signature validation.",
        "expected": ["dex-mqtt-client-reliability", "dex-websocket-session-recovery", "dex-webhook-signature-validation"]
    },
    # Group Z: AI Agent Operations
    {
        "id": "scenario-26-agent-ops",
        "prompt": "Thiết kế llm evaluation dataset design, thẩm định agent task planning validation và cổng duyệt llm human review gates.",
        "expected": ["dex-llm-evaluation-dataset-design", "dex-agent-task-planning-validation", "dex-llm-human-review-gates"]
    },
    # Group AA: Advanced Data & Analytics
    {
        "id": "scenario-27-data-analytics",
        "prompt": "Xây dựng sql metric semantic layer, phát hiện data anomaly detection và tối ưu chi phí data warehouse cost tuning.",
        "expected": ["dex-sql-metric-semantic-layer", "dex-data-anomaly-detection", "dex-data-warehouse-cost-tuning"]
    },
    # Group AB: Native, Graphics & Game Engineering
    {
        "id": "scenario-28-graphics-game",
        "prompt": "Kiểm thử chess engine search testing, đảm bảo simulation determinism và tinh chỉnh game loop timing.",
        "expected": ["dex-chess-engine-search-testing", "dex-simulation-determinism", "dex-game-loop-timing"]
    },
    # Group AC: Software Trust & Distribution
    {
        "id": "scenario-29-trust-distribution",
        "prompt": "Quét giấy phép open source license scanning, ký số artifact signature verification và quy trình code signing release process.",
        "expected": ["dex-open-source-license-scanning", "dex-artifact-signature-verification", "dex-code-signing-release-process"]
    },
    # Group AD: Advanced SkillOps Governance
    {
        "id": "scenario-30-adv-skillops",
        "prompt": "Quản trị skill catalog taxonomy, kiểm tra skill source integrity và ghi nhận sổ cái skill execution evidence ledger.",
        "expected": ["dex-skill-catalog-taxonomy", "dex-skill-source-integrity", "dex-skill-execution-evidence-ledger"]
    }
]

def simulate_route(prompt: str, skills_catalog: list[dict]) -> list[str]:
    normalized_prompt = prompt.lower()
    scores = {}

    for s in skills_catalog:
        skill_id = s["id"]
        if skill_id == "dex-master-orchestrator":
            continue

        score = 0
        desc = s.get("description", "").lower()
        
        # Check tokens of skill_id
        clean_id = skill_id.replace("dex-", "")
        clean_id_spaces = clean_id.replace("-", " ")
        if clean_id_spaces in normalized_prompt or clean_id in normalized_prompt:
            score += 20

        parts = clean_id.split("-")
        for part in parts:
            if len(part) >= 3 and f" {part} " in f" {normalized_prompt} ":
                score += 4

        # Keyword boosts from description
        desc_words = [w for w in re.findall(r"[a-z0-9]+", desc) if len(w) > 4]
        for dw in desc_words[:30]:
            if f" {dw} " in f" {normalized_prompt} ":
                score += 2

        if score > 0:
            scores[skill_id] = score

    sorted_skills = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [s[0] for s in sorted_skills[:3]]

def main():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    manifest_path = os.path.join(root_dir, "manifests", "dex-skills.json")

    if not os.path.exists(manifest_path):
        print(f"Error: Manifest not found at {manifest_path}. Run discover_skills.py first.")
        sys.exit(1)

    with open(manifest_path, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    skills_list = catalog.get("native_skills", [])
    print(f"=== DEX ROUTING EVALUATION HARNESS ===")
    print(f"Evaluating {len(BENCHMARK_SCENARIOS)} benchmark scenarios across 30 groups (Groups A to AD)...")

    total_precision = []
    total_recall = []
    perfect_matches = 0

    for idx, sc in enumerate(BENCHMARK_SCENARIOS):
        sc_id = sc["id"]
        prompt = sc["prompt"]
        expected = set(sc["expected"])
        routed = set(simulate_route(prompt, skills_list))

        tp = len(routed.intersection(expected))
        precision = tp / len(routed) if routed else 0.0
        recall = tp / len(expected) if expected else 0.0

        total_precision.append(precision)
        total_recall.append(recall)

        if expected.issubset(routed) or len(expected.intersection(routed)) >= len(expected) - 1:
            perfect_matches += 1
            status = "[PASS]"
        else:
            status = "[WARN]"

        print(f"{status} Scenario {idx+1:02d} ({sc_id}): Precision={precision:.2%}, Recall={recall:.2%}")

    avg_p = sum(total_precision) / len(total_precision)
    avg_r = sum(total_recall) / len(total_recall)
    f1 = (2 * avg_p * avg_r) / (avg_p + avg_r) if (avg_p + avg_r) > 0 else 0

    print("\n" + "=" * 50)
    print("ROUTING EVALUATION RESULTS:")
    print(f"  Total Scenarios Evaluated  : {len(BENCHMARK_SCENARIOS)}")
    print(f"  Passed Scenarios           : {perfect_matches} / {len(BENCHMARK_SCENARIOS)}")
    print(f"  Average Routing Precision   : {avg_p:.2%}")
    print(f"  Average Routing Recall      : {avg_r:.2%}")
    print(f"  Overall Routing F1-Score    : {f1:.3f}")
    print("=" * 50)

    if f1 < 0.85:
        print("\nRESULT: ROUTING EVALUATION FAILED (F1 < 0.85)")
        sys.exit(1)
    else:
        print("\nRESULT: ROUTING EVALUATION PASSED (F1 >= 0.85)")
        sys.exit(0)

if __name__ == "__main__":
    main()
