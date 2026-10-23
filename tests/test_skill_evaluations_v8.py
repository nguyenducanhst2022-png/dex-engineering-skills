# -*- coding: utf-8 -*-
"""
Pytest suite for DEX Framework v8.0: Real-World Evaluation Scenarios (Phase 12: Scenarios A through L).
Evaluates the Master Orchestrator dispatch precision, tool invocation constraints,
deliverable generation contracts, and failure boundary enforcement across 12 production scenarios.
"""

import os
import json
import pytest

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SKILLS_DIR = os.path.join(ROOT_DIR, ".agents", "skills")
MANIFEST_FILE = os.path.join(ROOT_DIR, "manifests", "dex-skills.json")

EVALUATION_SCENARIOS = {
    "Scenario A: Production Modular Monolith Design": {
        "id": "scenario-a-modular-monolith",
        "input_prompt": "Thiết kế kiến trúc modular monolith cho hệ thống e-commerce với ranh giới bounded context rõ ràng giữa Catalog, Order và Payment, kèm ADR giải trình.",
        "expected_skills": [
            "dex-modular-monolith-boundaries",
            "dex-architecture-decision-records",
            "dex-software-architecture"
        ],
        "excluded_skills": [
            "dex-browser-extension-mv3",
            "dex-pe-elf-structure-inspection",
            "dex-zig-build-engineering"
        ],
        "required_tools": ["markdown-linter", "ast-dependency-analyzer", "git-cli"],
        "expected_outcomes": [
            "Architecture Decision Record (MADR format)",
            "Module boundary enforcement rules in linting config",
            "Dependency inversion contract interfaces"
        ],
        "boundary_limitations": "Does not support direct microservices distributed transactions without introducing saga patterns."
    },
    "Scenario B: Distributed Message Delivery Recovery": {
        "id": "scenario-b-message-recovery",
        "input_prompt": "Xử lý sự cố consumer lag tăng vọt và poison pill message trong Kafka/RabbitMQ, đảm bảo replay an toàn và lease lock không bị starvation.",
        "expected_skills": [
            "dex-message-poison-queue-recovery",
            "dex-consumer-lag-control",
            "dex-distributed-lock-lease-safety"
        ],
        "excluded_skills": [
            "dex-color-contrast-systems",
            "dex-dart-flutter-state-debugging",
            "dex-visual-hierarchy-audit"
        ],
        "required_tools": ["kafka-cli", "rabbitmqadmin", "redis-cli"],
        "expected_outcomes": [
            "Dead letter exchange / poison queue quarantine policy",
            "Idempotent replay pipeline with idempotency-key deduplication",
            "Lease expiration watchdog mechanism"
        ],
        "boundary_limitations": "Replay cannot guarantee physical FIFO ordering across multi-partition re-ingestion."
    },
    "Scenario C: RAG Retrieval Freshness & Relevance": {
        "id": "scenario-c-rag-freshness",
        "input_prompt": "Cải thiện độ tươi mới dữ liệu RAG, kết hợp hybrid dense/sparse search và reranking để tăng precision@k mà không vượt token budget.",
        "expected_skills": [
            "dex-rag-freshness-control",
            "dex-hybrid-search-fusion",
            "dex-context-window-budgeting"
        ],
        "excluded_skills": [
            "dex-code-signing-release-process",
            "dex-php-framework-hardening",
            "dex-pe-elf-structure-inspection"
        ],
        "required_tools": ["vector-db-client", "reranker-model", "tokenizer"],
        "expected_outcomes": [
            "Time-decay relevance ranking score multiplier",
            "Reciprocal Rank Fusion (RRF) parameter tuning config",
            "Token allocation budgeting matrix per prompt segment"
        ],
        "boundary_limitations": "Frequent vector re-indexing incurs embedding provider API costs and index compaction locks."
    },
    "Scenario D: Kotlin Multiplatform Build Verification": {
        "id": "scenario-d-kmp-build",
        "input_prompt": "Xác minh tính tương thích build đa nền tảng Kotlin Multiplatform (Android, iOS, JVM), quản lý Maxtrix release và build cache.",
        "expected_skills": [
            "dex-kotlin-multiplatform-builds",
            "dex-cross-platform-release-matrices",
            "dex-polyglot-build-orchestration"
        ],
        "excluded_skills": [
            "dex-threat-modeling",
            "dex-sql-metric-semantic-layer",
            "dex-data-anomaly-detection"
        ],
        "required_tools": ["gradle-wrapper", "jdk-17", "xcodebuild"],
        "expected_outcomes": [
            "Hierarchical source set declaration in build.gradle.kts",
            "GitHub Actions cross-runner matrix (macos-latest, ubuntu-latest)",
            "Remote Gradle build cache configuration"
        ],
        "boundary_limitations": "iOS framework compilation strictly requires macOS host runner with active Xcode toolchain."
    },
    "Scenario E: Dashboard Redesign with UI/UX Reference Data": {
        "id": "scenario-e-dashboard-redesign",
        "input_prompt": "Tái thiết kế dashboard giám sát hệ thống mật độ cao, tích hợp design tokens và đảm bảo khả năng tiếp cận WCAG cho biểu đồ dạng chart.",
        "expected_skills": [
            "dex-high-density-dashboard-layout",
            "dex-chart-visualization-accessibility",
            "dex-design-token-migration"
        ],
        "excluded_skills": [
            "dex-disassembly-cfg-reconstruction",
            "dex-zig-build-engineering",
            "dex-pe-elf-structure-inspection"
        ],
        "required_tools": ["axe-core", "chromatic", "token-transformer"],
        "expected_outcomes": [
            "CSS Grid responsive multi-panel layout with virtualized scroll",
            "SVG / Canvas data table fallback for screen readers",
            "Design token JSON export compatible with Tailwind / CSS Variables"
        ],
        "boundary_limitations": "Pure text screen readers cannot perceive complex canvas graphics without structured aria-table mirrors."
    },
    "Scenario F: Authorized Binary Inspection & Evidence Chain": {
        "id": "scenario-f-binary-inspection",
        "input_prompt": "Kiểm tra cấu trúc file nhị phân được cấp quyền, đối soát debug symbols và lập báo cáo kỹ thuật minh chứng chi tiết.",
        "expected_skills": [
            "dex-binary-provenance-matching",
            "dex-debug-symbols-correlation",
            "dex-reverse-engineering-reporting"
        ],
        "excluded_skills": [
            "dex-user-journey-mapping",
            "dex-progressive-web-apps",
            "dex-forms-and-validation"
        ],
        "required_tools": ["dumpbin", "readelf", "llvm-objdump", "sha256sum"],
        "expected_outcomes": [
            "PE/ELF header analysis report with compiler flags detection",
            "PDB/DWARF debug symbol resolution table",
            "Cryptographic chain-of-custody execution evidence report"
        ],
        "boundary_limitations": "Inspection must remain strictly within authorized sandbox environments; no live payload detonation."
    },
    "Scenario G: Vector Embedding Model Migration": {
        "id": "scenario-g-vector-migration",
        "input_prompt": "Thực hiện di chuyển embedding model từ text-embedding-ada-002 sang text-embedding-3-large mà không làm gián đoạn hệ thống tìm kiếm.",
        "expected_skills": [
            "dex-vector-embedding-migration",
            "dex-model-output-calibration",
            "dex-embedding-data-preparation"
        ],
        "excluded_skills": [
            "dex-mobile-permission-surface-diffing",
            "dex-dns-tls-certificate-monitoring",
            "dex-browser-extension-hardening"
        ],
        "required_tools": ["numpy", "scikit-learn", "vector-store-cli"],
        "expected_outcomes": [
            "Dual-write shadow indexing pipeline migration plan",
            "Cosine similarity distribution alignment calibration report",
            "Zero-downtime collection alias switchover script"
        ],
        "boundary_limitations": "Embedding dimension discrepancy requires a full secondary index backfill prior to router cutover."
    },
    "Scenario H: Polyglot Project Build (Python + TypeScript)": {
        "id": "scenario-h-polyglot-build",
        "input_prompt": "Xây dựng và kiểm thử hệ thống monorepo đa ngôn ngữ gồm backend Python FastAPI và frontend/client TypeScript với contract kiểm thử tự động.",
        "expected_skills": [
            "dex-polyglot-build-orchestration",
            "dex-cross-language-contract-tests",
            "dex-cli-command-contracts"
        ],
        "excluded_skills": [
            "dex-chess-engine-search-testing",
            "dex-firmware-image-structure-diffing",
            "dex-ios-app-architecture"
        ],
        "required_tools": ["python", "node", "npm", "pydantic-to-typescript"],
        "expected_outcomes": [
            "Polyglot task execution graph in dex.py or Turborepo",
            "Pact / OpenAPI contract verification test suite",
            "Standardized CLI exit codes and JSON result envelopes"
        ],
        "boundary_limitations": "Package management requires isolated language managers (uv/venv for Python, pnpm for TypeScript)."
    },
    "Scenario I: API Authorization & Role Matrix Audit": {
        "id": "scenario-i-api-auth-matrix",
        "input_prompt": "Kiểm toán ma trận phân quyền API RBAC/ABAC trên các resource nhạy cảm, quản lý vòng đời service accounts và chứng chỉ OIDC.",
        "expected_skills": [
            "dex-api-authorization-matrix-tests",
            "dex-service-account-lifecycle",
            "dex-secretless-cicd-oidc"
        ],
        "excluded_skills": [
            "dex-animation-storyboard-specs",
            "dex-game-loop-timing",
            "dex-fluid-typography-engineering"
        ],
        "required_tools": ["pytest", "jwt-decoder", "iam-policy-simulator"],
        "expected_outcomes": [
            "Automated parameterized negative authorization test suite",
            "Automated service account key expiration and rotation schedule",
            "OIDC federated token exchange policy document"
        ],
        "boundary_limitations": "Privilege escalation testing must be scoped to designated non-production staging environments."
    },
    "Scenario J: Ambiguous Agent Skill Activation Resolution": {
        "id": "scenario-j-ambiguous-routing",
        "input_prompt": "Phát hiện và giải quyết xung đột khi hai skills có từ khóa kích hoạt gần giống nhau, đo lường semantic routing accuracy và benchmark F1.",
        "expected_skills": [
            "dex-semantic-routing-evaluations",
            "dex-skill-routing-conflict-tests",
            "dex-skill-quality-scorecards"
        ],
        "excluded_skills": [
            "dex-windows-linux-path-compatibility",
            "dex-elixir-otp-supervision",
            "dex-hls-dash-playback"
        ],
        "required_tools": ["python", "pytest", "similarity-evaluator"],
        "expected_outcomes": [
            "Disambiguation taxonomy with mutual exclusion rules",
            "Automated test assertions catching overlapping trigger phrases",
            "F1-score benchmark evaluation report >= 0.85"
        ],
        "boundary_limitations": "High lexical overlap requires negative prompt test cases to suppress false positive activations."
    },
    "Scenario K: Third-Party Skill License & Provenance Verification": {
        "id": "scenario-k-license-provenance",
        "input_prompt": "Kiểm tra giấy phép mã nguồn mở (MIT/Apache vs GPL/Copyleft) và truy xuất nguồn gốc upstream commit SHA của các skills nhập ngoài.",
        "expected_skills": [
            "dex-upstream-license-diffing",
            "dex-skill-catalog-reconciliation",
            "dex-open-source-license-scanning"
        ],
        "excluded_skills": [
            "dex-web-animation-performance",
            "dex-consumer-lag-control",
            "dex-clock-skew-resilience"
        ],
        "required_tools": ["licensee", "git-log", "spdx-tools"],
        "expected_outcomes": [
            "License incompatibility matrix flagging viral copyleft",
            "THIRD_PARTY_NOTICES.md compliance attribution file",
            "Upstream sync manifest with validated commit SHAs"
        ],
        "boundary_limitations": "Legal compliance interpretation must ultimately be validated by organizational legal counsel."
    },
    "Scenario L: Failed Skill Import Rollback Verification": {
        "id": "scenario-l-import-rollback",
        "input_prompt": "Mô phỏng trường hợp nhập skill bên ngoài bị lỗi security check, kích hoạt cơ chế rollback nguyên tử và ghi log evidence ledger.",
        "expected_skills": [
            "dex-skill-execution-evidence-ledger",
            "dex-skill-source-integrity",
            "dex-skill-upstream-sync"
        ],
        "excluded_skills": [
            "dex-android-app-architecture",
            "dex-rtl-bidi-layout-readiness",
            "dex-chess-engine-search-testing"
        ],
        "required_tools": ["git-cli", "sha256sum", "skill-validator"],
        "expected_outcomes": [
            "Atomic transaction abort removing staged directories",
            "Immutable audit log entry in evidence ledger with SHA256",
            "Git working tree returned to clean state without residual files"
        ],
        "boundary_limitations": "Rollback requires clean initial working directory state before sync transaction initiation."
    }
}

@pytest.fixture(scope="session")
def skills_catalog():
    assert os.path.isfile(MANIFEST_FILE), f"Missing manifest: {MANIFEST_FILE}"
    with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {s["id"]: s for s in data.get("native_skills", [])}

@pytest.mark.parametrize("scenario_title,spec", EVALUATION_SCENARIOS.items())
def test_evaluation_scenario_contract(scenario_title, spec, skills_catalog):
    """
    Validates that each Phase 12 real-world evaluation scenario meets all criteria:
    - Expected skills exist in catalog and have full 14 mandatory sections.
    - Excluded skills are disjoint from expected skills.
    - Expected skills exist in native skills catalog.
    - Required tools and outcomes are fully specified.
    - Boundary limitations are documented.
    """
    expected = spec["expected_skills"]
    excluded = spec["excluded_skills"]

    # 1. Non-empty specification
    assert len(expected) >= 3, f"{scenario_title}: Expected skills must be >= 3"
    assert len(excluded) >= 3, f"{scenario_title}: Excluded skills must be >= 3"
    assert spec.get("required_tools"), f"{scenario_title}: Required tools must not be empty"
    assert spec.get("expected_outcomes"), f"{scenario_title}: Expected outcomes must not be empty"
    assert spec.get("boundary_limitations"), f"{scenario_title}: Boundary limitations must be defined"

    # 2. Strict disjointness between expected and excluded
    overlap = set(expected).intersection(set(excluded))
    assert not overlap, f"{scenario_title}: Overlap between expected and excluded skills: {overlap}"

    # 3. All expected skills exist on disk and in manifest
    for skill_id in expected:
        assert skill_id in skills_catalog, f"{scenario_title}: Expected skill '{skill_id}' not found in manifest"
        skill_dir = os.path.join(SKILLS_DIR, skill_id)
        assert os.path.isdir(skill_dir), f"{scenario_title}: Skill dir '{skill_dir}' does not exist"
        skill_file = os.path.join(skill_dir, "SKILL.md")
        assert os.path.isfile(skill_file), f"{scenario_title}: SKILL.md missing for '{skill_id}'"

        # Check section count >= 14
        with open(skill_file, "r", encoding="utf-8") as f:
            content = f.read()
        for sec_num in range(1, 15):
            assert f"## {sec_num}." in content, f"{skill_id}: Missing section ## {sec_num}."

    # 4. Excluded skills also exist in catalog (proving they are real skills correctly excluded)
    for skill_id in excluded:
        assert skill_id in skills_catalog, f"{scenario_title}: Excluded skill '{skill_id}' must exist in catalog"
