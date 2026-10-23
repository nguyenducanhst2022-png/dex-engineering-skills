# -*- coding: utf-8 -*-
"""
DEX SKILLOPS — Remediation Script for Dangling Skill References
Replaces outdated/aspirational skill names in Section 13 with verified canonical DEX skill IDs.
"""

import os
import re
import sys

REPLACEMENT_MAPPING = {
    'dex-frontend-architecture': 'dex-frontend-data-flow',
    'dex-unit-testing': 'dex-testing-engineering',
    'dex-database-design': 'dex-database-engineering',
    'dex-agent-loop-safety-cutoffs': 'dex-agent-execution-budget-controls',
    'dex-slsa-provenance-verification': 'dex-build-slsa-controls',
    'dex-backend-architecture': 'dex-software-architecture',
    'dex-performance-profiling': 'dex-performance-optimization',
    'dex-wcag-compliance-audit': 'dex-accessibility-automation',
    'dex-ci-pipeline-optimization': 'dex-cicd-automation',
    'dex-60fps-web-animation': 'dex-web-animation-performance',
    'dex-api-contract-testing': 'dex-contract-first-development',
    'dex-container-image-signing-cosign': 'dex-artifact-signature-verification',
    'dex-reproducible-build-audit': 'dex-build-slsa-controls',
    'dex-software-license-compliance-scan': 'dex-open-source-license-scanning',
    'dex-algorithm-optimization': 'dex-performance-optimization',
    'dex-mobile-first-responsive-patterns': 'dex-mobile-safe-area-layout',
    'dex-parquet-arrow-data-interop': 'dex-data-pipelines',
    'dex-agent-multi-turn-eval-harness': 'dex-agent-evaluation-harness',
    'dex-crypto-key-rotation-kms': 'dex-secrets-management',
    'dex-skill-provenance-ledger': 'dex-skill-provenance-revalidation',
    'dex-resilience-engineering': 'dex-reliability-engineering',
    'dex-cross-platform-engineering': 'dex-cli-engineering',
    'dex-git-flow-and-cherry-picking': 'dex-git-workflow',
    'dex-design-system-foundations': 'dex-design-system-tokens',
    'dex-visual-hierarchy-composition': 'dex-visual-hierarchy-audit',
    'dex-theme-lifecycle-management': 'dex-design-system-tokens',
    'dex-refactoring-mastery': 'dex-technical-debt-refactoring',
    'dex-incident-retrospective-authoring': 'dex-incident-postmortems',
    'dex-package-publishing-checks': 'dex-typescript-package-dual-publish',
    'dex-dependency-vulnerability-remediation': 'dex-dependency-management',
    'dex-code-review-excellence': 'dex-code-review',
    'dex-architecture-design': 'dex-software-architecture',
    'dex-integration-testing': 'dex-testing-engineering',
    'dex-resilience-circuit-breaker': 'dex-api-circuit-breaker-verification',
    'dex-fluid-typography-scaling': 'dex-fluid-typography-engineering',
}

def remediate_skills(skills_base):
    modified_files = []
    total_replacements = 0

    all_skill_dirs = [d for d in os.listdir(skills_base) if os.path.isdir(os.path.join(skills_base, d))]

    for s_name in sorted(all_skill_dirs):
        s_path = os.path.join(skills_base, s_name, 'SKILL.md')
        if not os.path.exists(s_path):
            continue

        with open(s_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Target Section 13 replacement
        rel_match = re.search(r'(## 13\.\s+Related.*?\n)(.*?)(?=\n##|\Z)', content, re.S)
        if not rel_match:
            continue

        header = rel_match.group(1)
        rel_text = rel_match.group(2)
        new_rel_text = rel_text
        file_replacements = 0

        for bad_ref, good_ref in REPLACEMENT_MAPPING.items():
            if bad_ref in new_rel_text:
                # Use word-boundary replacement for precision
                pattern = r'\b' + re.escape(bad_ref) + r'\b'
                new_rel_text, count = re.subn(pattern, good_ref, new_rel_text)
                file_replacements += count

        if file_replacements > 0:
            new_content = content[:rel_match.start()] + header + new_rel_text + content[rel_match.end():]
            with open(s_path, 'w', encoding='utf-8', newline='\n') as f:
                f.write(new_content)
            modified_files.append((s_name, file_replacements))
            total_replacements += file_replacements

    print(f"Remediation complete: {total_replacements} replacements across {len(modified_files)} files.")
    return modified_files

if __name__ == "__main__":
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    skills_base = os.path.join(repo_root, ".agents", "skills")
    remediate_skills(skills_base)
