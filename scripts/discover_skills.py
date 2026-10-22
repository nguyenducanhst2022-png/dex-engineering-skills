# -*- coding: utf-8 -*-
"""
DEX SKILLOPS — DISCOVERY & INDEXER (scripts/discover_skills.py)
Scans .agents/skills/ and integrations/, parses Agent Skills YAML frontmatter,
and outputs a structured catalog manifest (manifests/dex-skills.json) with exact
Group A through Group T assignments.
"""

import os
import sys
import re
import json
import argparse

SKILL_CANONICAL_GROUPS = {
    # Group A: Core Engineering (01-10)
    "dex-development-workflow": ("Group A", "Core Engineering", 1),
    "dex-task-delegation": ("Group A", "Core Engineering", 2),
    "dex-code-verification": ("Group A", "Core Engineering", 3),
    "dex-git-workflow": ("Group A", "Core Engineering", 4),
    "dex-code-organization": ("Group A", "Core Engineering", 5),
    "dex-root-cause-debugging": ("Group A", "Core Engineering", 6),
    "dex-performance-optimization": ("Group A", "Core Engineering", 7),
    "dex-security-audit": ("Group A", "Core Engineering", 8),
    "dex-cicd-automation": ("Group A", "Core Engineering", 9),
    "dex-release-engineering": ("Group A", "Core Engineering", 10),

    # Group B: Software Architecture & AI Agents (11-20)
    "dex-production-monitoring": ("Group B", "Architecture & AI Agents", 11),
    "dex-technical-debt-refactoring": ("Group B", "Architecture & AI Agents", 12),
    "dex-software-architecture": ("Group B", "Architecture & AI Agents", 13),
    "dex-database-engineering": ("Group B", "Architecture & AI Agents", 14),
    "dex-api-engineering": ("Group B", "Architecture & AI Agents", 15),
    "dex-testing-engineering": ("Group B", "Architecture & AI Agents", 16),
    "dex-agent-engineering": ("Group B", "Architecture & AI Agents", 17),
    "dex-multi-agent-orchestration": ("Group B", "Architecture & AI Agents", 18),
    "dex-context-engineering": ("Group B", "Architecture & AI Agents", 19),
    "dex-specification-driven": ("Group B", "Architecture & AI Agents", 20),

    # Group C: Production Engineering (21-30)
    "dex-change-impact-analysis": ("Group C", "Production Engineering", 21),
    "dex-dependency-management": ("Group C", "Production Engineering", 22),
    "dex-reliability-engineering": ("Group C", "Production Engineering", 23),
    "dex-concurrency-state": ("Group C", "Production Engineering", 24),
    "dex-ux-accessibility": ("Group C", "Production Engineering", 25),
    "dex-feature-flags": ("Group C", "Production Engineering", 26),
    "dex-code-review": ("Group C", "Production Engineering", 27),
    "dex-acceptance-testing": ("Group C", "Production Engineering", 28),
    "dex-software-maintenance": ("Group C", "Production Engineering", 29),
    "dex-end-to-end-engineering": ("Group C", "Production Engineering", 30),

    # Group D: Frontend Engineering (31-40)
    "dex-ui-component-contracts": ("Group D", "Frontend Engineering", 31),
    "dex-design-system-tokens": ("Group D", "Frontend Engineering", 32),
    "dex-frontend-data-flow": ("Group D", "Frontend Engineering", 33),
    "dex-forms-and-validation": ("Group D", "Frontend Engineering", 34),
    "dex-routing-navigation": ("Group D", "Frontend Engineering", 35),
    "dex-frontend-performance": ("Group D", "Frontend Engineering", 36),
    "dex-ssr-seo-rendering": ("Group D", "Frontend Engineering", 37),
    "dex-internationalization": ("Group D", "Frontend Engineering", 38),
    "dex-visual-regression": ("Group D", "Frontend Engineering", 39),
    "dex-browser-compatibility": ("Group D", "Frontend Engineering", 40),

    # Group E: Backend & Integration (41-50)
    "dex-domain-driven-design": ("Group E", "Backend & Integration", 41),
    "dex-background-job-queues": ("Group E", "Backend & Integration", 42),
    "dex-caching-strategies": ("Group E", "Backend & Integration", 43),
    "dex-realtime-protocols": ("Group E", "Backend & Integration", 44),
    "dex-file-processing": ("Group E", "Backend & Integration", 45),
    "dex-search-engineering": ("Group E", "Backend & Integration", 46),
    "dex-event-driven-architecture": ("Group E", "Backend & Integration", 47),
    "dex-idempotent-operations": ("Group E", "Backend & Integration", 48),
    "dex-notification-delivery": ("Group E", "Backend & Integration", 49),
    "dex-scheduled-workflows": ("Group E", "Backend & Integration", 50),

    # Group F: Data Engineering (51-60)
    "dex-data-contracts": ("Group F", "Data Engineering", 51),
    "dex-data-pipelines": ("Group F", "Data Engineering", 52),
    "dex-data-quality-audits": ("Group F", "Data Engineering", 53),
    "dex-data-lineage": ("Group F", "Data Engineering", 54),
    "dex-schema-evolution": ("Group F", "Data Engineering", 55),
    "dex-database-query-plans": ("Group F", "Data Engineering", 56),
    "dex-storage-lifecycle": ("Group F", "Data Engineering", 57),
    "dex-data-retention": ("Group F", "Data Engineering", 58),
    "dex-capacity-planning": ("Group F", "Data Engineering", 59),
    "dex-disaster-recovery": ("Group F", "Data Engineering", 60),

    # Group G: AI & LLM Engineering (61-70)
    "dex-llm-integration": ("Group G", "AI & LLM Engineering", 61),
    "dex-rag-pipelines": ("Group G", "AI & LLM Engineering", 62),
    "dex-retrieval-evaluation": ("Group G", "AI & LLM Engineering", 63),
    "dex-prompt-evaluation": ("Group G", "AI & LLM Engineering", 64),
    "dex-model-evaluation": ("Group G", "AI & LLM Engineering", 65),
    "dex-tool-calling-contracts": ("Group G", "AI & LLM Engineering", 66),
    "dex-agent-permissions": ("Group G", "AI & LLM Engineering", 67),
    "dex-llm-cost-controls": ("Group G", "AI & LLM Engineering", 68),
    "dex-ai-observability": ("Group G", "AI & LLM Engineering", 69),
    "dex-dataset-curation": ("Group G", "AI & LLM Engineering", 70),

    # Group H: Developer Experience (71-80)
    "dex-repository-bootstrap": ("Group H", "Developer Experience", 71),
    "dex-monorepo-governance": ("Group H", "Developer Experience", 72),
    "dex-cli-engineering": ("Group H", "Developer Experience", 73),
    "dex-plugin-architecture": ("Group H", "Developer Experience", 74),
    "dex-cross-platform-portability": ("Group H", "Developer Experience", 75),
    "dex-windows-packaging": ("Group H", "Developer Experience", 76),
    "dex-documentation-as-code": ("Group H", "Developer Experience", 77),
    "dex-code-generation": ("Group H", "Developer Experience", 78),
    "dex-developer-tooling": ("Group H", "Developer Experience", 79),
    "dex-semantic-version-automation": ("Group H", "Developer Experience", 80),

    # Group I: Security & Reliability (81-90)
    "dex-auth-session-lifecycle": ("Group I", "Security & Reliability", 81),
    "dex-access-control-tenancy": ("Group I", "Security & Reliability", 82),
    "dex-secrets-management": ("Group I", "Security & Reliability", 83),
    "dex-supply-chain-security": ("Group I", "Security & Reliability", 84),
    "dex-threat-modeling": ("Group I", "Security & Reliability", 85),
    "dex-property-based-testing": ("Group I", "Security & Reliability", 86),
    "dex-chaos-experiments": ("Group I", "Security & Reliability", 87),
    "dex-experimentation-metrics": ("Group I", "Security & Reliability", 88),
    "dex-api-contract-evolution": ("Group I", "Security & Reliability", 89),
    "dex-incident-postmortems": ("Group I", "Security & Reliability", 90),

    # Group J: Cloud & Infrastructure (91-100)
    "dex-container-image-engineering": ("Group J", "Cloud & Infrastructure", 91),
    "dex-kubernetes-deployment": ("Group J", "Cloud & Infrastructure", 92),
    "dex-infrastructure-as-code": ("Group J", "Cloud & Infrastructure", 93),
    "dex-cloud-service-integration": ("Group J", "Cloud & Infrastructure", 94),
    "dex-zero-downtime-rollouts": ("Group J", "Cloud & Infrastructure", 95),
    "dex-service-mesh-networking": ("Group J", "Cloud & Infrastructure", 96),
    "dex-network-troubleshooting": ("Group J", "Cloud & Infrastructure", 97),
    "dex-slo-error-budgets": ("Group J", "Cloud & Infrastructure", 98),
    "dex-distributed-tracing": ("Group J", "Cloud & Infrastructure", 99),
    "dex-cloud-cost-finops": ("Group J", "Cloud & Infrastructure", 100),

    # Group K: Mobile & Desktop Engineering (101-110)
    "dex-android-app-architecture": ("Group K", "Mobile & Desktop Engineering", 101),
    "dex-ios-app-architecture": ("Group K", "Mobile & Desktop Engineering", 102),
    "dex-electron-security": ("Group K", "Mobile & Desktop Engineering", 103),
    "dex-tauri-desktop-integration": ("Group K", "Mobile & Desktop Engineering", 104),
    "dex-mobile-offline-sync": ("Group K", "Mobile & Desktop Engineering", 105),
    "dex-mobile-release-pipelines": ("Group K", "Mobile & Desktop Engineering", 106),
    "dex-mobile-performance-profiling": ("Group K", "Mobile & Desktop Engineering", 107),
    "dex-desktop-ipc-design": ("Group K", "Mobile & Desktop Engineering", 108),
    "dex-native-device-integration": ("Group K", "Mobile & Desktop Engineering", 109),
    "dex-desktop-update-delivery": ("Group K", "Mobile & Desktop Engineering", 110),

    # Group L: Product & Operations Engineering (111-120)
    "dex-privacy-impact-assessment": ("Group L", "Product & Operations Engineering", 111),
    "dex-compliance-control-mapping": ("Group L", "Product & Operations Engineering", 112),
    "dex-audit-trail-integrity": ("Group L", "Product & Operations Engineering", 113),
    "dex-configuration-drift": ("Group L", "Product & Operations Engineering", 114),
    "dex-product-discovery": ("Group L", "Product & Operations Engineering", 115),
    "dex-feature-prioritization": ("Group L", "Product & Operations Engineering", 116),
    "dex-analytics-instrumentation": ("Group L", "Product & Operations Engineering", 117),
    "dex-feedback-triage": ("Group L", "Product & Operations Engineering", 118),
    "dex-runbook-automation": ("Group L", "Product & Operations Engineering", 119),
    "dex-operational-readiness-review": ("Group L", "Product & Operations Engineering", 120),

    # Group M: Advanced Software Verification (121-130)
    "dex-static-analysis-rule-authoring": ("Group M", "Advanced Software Verification", 121),
    "dex-mutation-testing": ("Group M", "Advanced Software Verification", 122),
    "dex-api-fuzz-testing": ("Group M", "Advanced Software Verification", 123),
    "dex-differential-testing": ("Group M", "Advanced Software Verification", 124),
    "dex-flaky-test-remediation": ("Group M", "Advanced Software Verification", 125),
    "dex-test-data-management": ("Group M", "Advanced Software Verification", 126),
    "dex-compatibility-matrix-testing": ("Group M", "Advanced Software Verification", 127),
    "dex-reproducible-benchmarking": ("Group M", "Advanced Software Verification", 128),
    "dex-formal-invariant-checks": ("Group M", "Advanced Software Verification", 129),
    "dex-coverage-risk-analysis": ("Group M", "Advanced Software Verification", 130),

    # Group N: Advanced SRE & Distributed Systems (131-140)
    "dex-load-and-stress-testing": ("Group N", "Advanced SRE & Distributed Systems", 131),
    "dex-traffic-shaping-backpressure": ("Group N", "Advanced SRE & Distributed Systems", 132),
    "dex-rate-limiting-quotas": ("Group N", "Advanced SRE & Distributed Systems", 133),
    "dex-distributed-consistency": ("Group N", "Advanced SRE & Distributed Systems", 134),
    "dex-service-failover": ("Group N", "Advanced SRE & Distributed Systems", 135),
    "dex-alert-quality-engineering": ("Group N", "Advanced SRE & Distributed Systems", 136),
    "dex-log-pipeline-design": ("Group N", "Advanced SRE & Distributed Systems", 137),
    "dex-metric-cardinality-control": ("Group N", "Advanced SRE & Distributed Systems", 138),
    "dex-oncall-handover": ("Group N", "Advanced SRE & Distributed Systems", 139),
    "dex-operational-game-days": ("Group N", "Advanced SRE & Distributed Systems", 140),

    # Group O: Advanced Cloud Platform (141-150)
    "dex-serverless-architecture": ("Group O", "Advanced Cloud Platform", 141),
    "dex-edge-runtime-engineering": ("Group O", "Advanced Cloud Platform", 142),
    "dex-cloud-iam-policy-review": ("Group O", "Advanced Cloud Platform", 143),
    "dex-cloud-network-design": ("Group O", "Advanced Cloud Platform", 144),
    "dex-gitops-workflows": ("Group O", "Advanced Cloud Platform", 145),
    "dex-kubernetes-policy-enforcement": ("Group O", "Advanced Cloud Platform", 146),
    "dex-platform-service-catalog": ("Group O", "Advanced Cloud Platform", 147),
    "dex-environment-promotion": ("Group O", "Advanced Cloud Platform", 148),
    "dex-service-discovery": ("Group O", "Advanced Cloud Platform", 149),
    "dex-cloud-resource-tagging": ("Group O", "Advanced Cloud Platform", 150),

    # Group P: Language & Runtime Engineering (151-160)
    "dex-typescript-type-safety": ("Group P", "Language & Runtime Engineering", 151),
    "dex-nodejs-runtime-diagnostics": ("Group P", "Language & Runtime Engineering", 152),
    "dex-python-project-engineering": ("Group P", "Language & Runtime Engineering", 153),
    "dex-rust-unsafe-audit": ("Group P", "Language & Runtime Engineering", 154),
    "dex-cpp-memory-safety": ("Group P", "Language & Runtime Engineering", 155),
    "dex-go-concurrency-patterns": ("Group P", "Language & Runtime Engineering", 156),
    "dex-jvm-performance-diagnostics": ("Group P", "Language & Runtime Engineering", 157),
    "dex-dotnet-application-engineering": ("Group P", "Language & Runtime Engineering", 158),
    "dex-webassembly-integration": ("Group P", "Language & Runtime Engineering", 159),
    "dex-ffi-boundary-contracts": ("Group P", "Language & Runtime Engineering", 160),

    # Group Q: Advanced AI Systems (161-170)
    "dex-mcp-server-design": ("Group Q", "Advanced AI Systems", 161),
    "dex-vector-index-design": ("Group Q", "Advanced AI Systems", 162),
    "dex-reranking-strategies": ("Group Q", "Advanced AI Systems", 163),
    "dex-structured-llm-output": ("Group Q", "Advanced AI Systems", 164),
    "dex-prompt-injection-defense": ("Group Q", "Advanced AI Systems", 165),
    "dex-grounding-citation-audit": ("Group Q", "Advanced AI Systems", 166),
    "dex-agent-memory-governance": ("Group Q", "Advanced AI Systems", 167),
    "dex-multimodal-input-pipelines": ("Group Q", "Advanced AI Systems", 168),
    "dex-agent-evaluation-harness": ("Group Q", "Advanced AI Systems", 169),
    "dex-llm-fallback-routing": ("Group Q", "Advanced AI Systems", 170),

    # Group R: Product Design & User Research (171-180)
    "dex-user-journey-mapping": ("Group R", "Product Design & User Research", 171),
    "dex-information-architecture": ("Group R", "Product Design & User Research", 172),
    "dex-usability-study-design": ("Group R", "Product Design & User Research", 173),
    "dex-accessibility-automation": ("Group R", "Product Design & User Research", 174),
    "dex-design-handoff-verification": ("Group R", "Product Design & User Research", 175),
    "dex-product-requirements-writing": ("Group R", "Product Design & User Research", 176),
    "dex-conversion-funnel-analysis": ("Group R", "Product Design & User Research", 177),
    "dex-feature-adoption-analysis": ("Group R", "Product Design & User Research", 178),
    "dex-user-consent-ux": ("Group R", "Product Design & User Research", 179),
    "dex-supportability-engineering": ("Group R", "Product Design & User Research", 180),

    # Group S: Application Security Specialists (181-190)
    "dex-sast-finding-triage": ("Group S", "Application Security Specialists", 181),
    "dex-dast-scoping": ("Group S", "Application Security Specialists", 182),
    "dex-api-abuse-prevention": ("Group S", "Application Security Specialists", 183),
    "dex-web-security-headers": ("Group S", "Application Security Specialists", 184),
    "dex-browser-extension-hardening": ("Group S", "Application Security Specialists", 185),
    "dex-sbom-verification": ("Group S", "Application Security Specialists", 186),
    "dex-vulnerability-remediation": ("Group S", "Application Security Specialists", 187),
    "dex-security-logging-detection": ("Group S", "Application Security Specialists", 188),
    "dex-cryptographic-api-review": ("Group S", "Application Security Specialists", 189),
    "dex-secure-build-runners": ("Group S", "Application Security Specialists", 190),

    # Group T: SkillOps Engineering (191-200)
    "dex-skill-discovery-indexer": ("Group T", "SkillOps Engineering", 191),
    "dex-skill-license-provenance": ("Group T", "SkillOps Engineering", 192),
    "dex-skill-semantic-deduplication": ("Group T", "SkillOps Engineering", 193),
    "dex-skill-security-screening": ("Group T", "SkillOps Engineering", 194),
    "dex-skill-import-packaging": ("Group T", "SkillOps Engineering", 195),
    "dex-skill-upstream-sync": ("Group T", "SkillOps Engineering", 196),
    "dex-skill-activation-evaluation": ("Group T", "SkillOps Engineering", 197),
    "dex-skill-host-adapters": ("Group T", "SkillOps Engineering", 198),
    "dex-skill-dependency-graph": ("Group T", "SkillOps Engineering", 199),
    "dex-skill-quality-benchmarking": ("Group T", "SkillOps Engineering", 200),
}

def parse_frontmatter(content):
    if not content.startswith("---"):
        return None, "File does not start with ---"
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None, "Malformed frontmatter delimiters"
    fm_text = parts[1].strip()
    data = {}
    lines = fm_text.splitlines()
    current_key = None
    current_val = []
    for line in lines:
        if ":" in line and not line.startswith(" ") and not line.startswith("\t"):
            if current_key:
                data[current_key] = "\n".join(current_val).strip()
            k, v = line.split(":", 1)
            current_key = k.strip()
            current_val = [v.strip()]
        elif current_key:
            current_val.append(line.strip())
    if current_key:
        data[current_key] = " ".join(current_val).strip()
    return data, parts[2]

def discover_all_skills(root_dir):
    skills_base = os.path.join(root_dir, ".agents", "skills")
    integrations_base = os.path.join(root_dir, "integrations")

    catalog = {
        "framework": "DEX Engineering Skills Framework",
        "version": "5.0.0",
        "target_skills_count": 201,
        "native_skills": [],
        "segregated_integrations": []
    }

    if not os.path.exists(skills_base):
        print(f"Error: {skills_base} not found")
        return catalog

    skill_dirs = [d for d in os.listdir(skills_base) if os.path.isdir(os.path.join(skills_base, d))]
    
    # Sort by canonical index: 0 for orchestrator, then 1 to 200
    def sort_key(s_name):
        if s_name == "dex-master-orchestrator":
            return 0
        return SKILL_CANONICAL_GROUPS.get(s_name, ("Custom", "Custom", 999))[2]

    ordered_dirs = sorted(skill_dirs, key=sort_key)

    for s_name in ordered_dirs:
        s_path = os.path.join(skills_base, s_name, "SKILL.md")
        if not os.path.exists(s_path):
            continue
        with open(s_path, "r", encoding="utf-8") as f:
            content = f.read()
        fm, body = parse_frontmatter(content)
        if not fm:
            continue
        
        if s_name == "dex-master-orchestrator":
            grp_code, grp_title, idx = "Root", "Master Orchestrator", 0
        else:
            grp_code, grp_title, idx = SKILL_CANONICAL_GROUPS.get(s_name, ("Custom", "Specialized Skill", 999))
        
        rel_match = re.search(r"## 13\.\s+Related & Complementary Skills\s*\n(.*?)(?=\n##|$)", body, re.S)
        related = []
        if rel_match:
            rel_text = rel_match.group(1)
            related = re.findall(r"(dex-[a-z0-9-]+)", rel_text)
            related = [r for r in related if r != s_name]

        item = {
            "id": s_name,
            "index": idx,
            "name": fm.get("name", s_name),
            "description": fm.get("description", ""),
            "version": fm.get("version", "5.0.0"),
            "group": grp_code,
            "domain": grp_title,
            "path": f".agents/skills/{s_name}/SKILL.md",
            "related_skills": related[:5]
        }
        catalog["native_skills"].append(item)

    # Segregated Integrations
    if os.path.exists(integrations_base):
        for root, dirs, files in os.walk(integrations_base):
            for d in sorted(dirs):
                skill_path = os.path.join(root, d, "SKILL.md")
                if os.path.isfile(skill_path):
                    with open(skill_path, "r", encoding="utf-8") as f:
                        c = f.read()
                    fm, _ = parse_frontmatter(c)
                    rel_dir = os.path.relpath(os.path.join(root, d), root_dir).replace("\\", "/")
                    catalog["segregated_integrations"].append({
                        "id": d,
                        "name": fm.get("name", d) if fm else d,
                        "description": fm.get("description", "") if fm else "",
                        "path": f"{rel_dir}/SKILL.md"
                    })

    return catalog

def main():
    parser = argparse.ArgumentParser(description="DEX SkillOps Discovery and Indexer")
    parser.add_argument("--output", default="manifests/dex-skills.json", help="Path to output JSON manifest")
    parser.add_argument("--root", default=os.path.abspath(os.path.join(os.path.dirname(__file__), "..")), help="Repository root")
    args = parser.parse_args()

    root_dir = args.root
    out_file = os.path.join(root_dir, args.output) if not os.path.isabs(args.output) else args.output
    os.makedirs(os.path.dirname(out_file), exist_ok=True)

    print(f"=== DEX SKILLOPS DISCOVERY & INDEXER ===")
    print(f"Scanning repository at: {root_dir}")
    
    catalog = discover_all_skills(root_dir)
    print(f"Discovered native DEX skills: {len(catalog['native_skills'])}")
    print(f"Discovered segregated integrations: {len(catalog['segregated_integrations'])}")

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=2, ensure_ascii=False)

    print(f"Manifest written successfully to: {out_file}")

if __name__ == "__main__":
    main()
