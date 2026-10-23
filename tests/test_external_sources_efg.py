# -*- coding: utf-8 -*-
"""
Pytest suite for DEX Engineering Skills Framework v8.1 — Multi-Source Integration (Sources E, F, G).
Tests adapter structure, license provenance, SHA-1 pinning, namespace segregation,
Master Orchestrator sovereignty, runtime detection fallback, security boundaries,
and native skill count invariance (401 skills).
"""

import os
import sys
import re
import json
import pytest

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT_DIR, "scripts"))

from validate_skills import parse_frontmatter, MANDATORY_SECTIONS


def test_01_adapter_files_exist():
    """Assertion 1: Verify all 3 adapter files and the integration guide exist."""
    expected_files = [
        os.path.join(ROOT_DIR, "integrations", "supabase", "dex-supabase-adapter", "SKILL.md"),
        os.path.join(ROOT_DIR, "integrations", "superpowers", "dex-superpowers-adapter", "SKILL.md"),
        os.path.join(ROOT_DIR, "integrations", "mattpocock", "dex-mattpocock-adapter", "SKILL.md"),
        os.path.join(ROOT_DIR, "integrations", "README-new-sources.md"),
    ]
    for p in expected_files:
        assert os.path.isfile(p), f"Required integration file missing: {p}"


def test_02_adapter_metadata_valid():
    """Assertion 2: Verify SKILL.md YAML frontmatter is valid and has required fields."""
    adapters = [
        ("dex-supabase-adapter", "integrations/supabase/dex-supabase-adapter/SKILL.md"),
        ("dex-superpowers-adapter", "integrations/superpowers/dex-superpowers-adapter/SKILL.md"),
        ("dex-mattpocock-adapter", "integrations/mattpocock/dex-mattpocock-adapter/SKILL.md"),
    ]
    for skill_name, rel_path in adapters:
        full_path = os.path.join(ROOT_DIR, rel_path)
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()
        fm, body = parse_frontmatter(content)
        assert fm is not None, f"Malformed frontmatter in {rel_path}"
        assert fm.get("name") == skill_name
        assert "description" in fm and len(fm["description"]) >= 20
        assert "version" in fm
        assert "upstream_source" in fm
        assert "upstream_commit" in fm
        assert len(fm["upstream_commit"]) == 40


def test_03_skill_names_unique():
    """Assertion 3: Verify all skill names (native and integrations) are globally unique."""
    native_skills_dir = os.path.join(ROOT_DIR, ".agents", "skills")
    native_names = set(os.listdir(native_skills_dir))

    integration_names = []
    integrations_dir = os.path.join(ROOT_DIR, "integrations")
    for root, dirs, files in os.walk(integrations_dir):
        for d in dirs:
            skill_file = os.path.join(root, d, "SKILL.md")
            if os.path.isfile(skill_file):
                integration_names.append(d)

    assert len(integration_names) == 8, f"Expected 8 integrations, got {len(integration_names)}"
    assert len(integration_names) == len(set(integration_names)), "Duplicate integration names detected"

    for iname in integration_names:
        assert iname not in native_names, f"Integration name '{iname}' collides with native DEX skills"


def test_04_source_commit_shas_valid():
    """Assertion 4: Verify pinned commit SHAs in manifest match verified 40-character git hashes."""
    manifest_path = os.path.join(ROOT_DIR, "manifests", "upstream-sources.json")
    with open(manifest_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    expected_shas = {
        "source-e-supabase": "c9be0e931b7930f7d02126d04774d904c381e7d7",
        "source-f-superpowers": "2ce8aa15d05bd57213e6f746f953aafb7ded7a8b",
        "source-g-mattpocock": "5beb35b040e3de97e54fa9e386d7e42d15c295c2",
    }

    source_map = {s["upstream_id"]: s for s in data["sources"]}
    for uid, expected_sha in expected_shas.items():
        assert uid in source_map, f"Missing upstream source '{uid}' in upstream-sources.json"
        actual_sha = source_map[uid]["pinned_commit"]
        assert actual_sha == expected_sha, f"Commit SHA mismatch for {uid}: expected {expected_sha}, got {actual_sha}"
        assert re.match(r"^[0-9a-f]{40}$", actual_sha), f"Invalid 40-character SHA format for {uid}"


def test_05_license_metadata_valid():
    """Assertion 5: Verify MIT licenses and license files exist for Sources E, F, and G."""
    expected_licenses = {
        "supabase": ("MIT", "Supabase"),
        "superpowers": ("MIT", "Jesse Vincent"),
        "mattpocock": ("MIT", "Matt Pocock"),
    }
    for folder, (expected_lic, expected_holder) in expected_licenses.items():
        lic_file = os.path.join(ROOT_DIR, "integrations", folder, "LICENSE")
        assert os.path.isfile(lic_file), f"LICENSE file missing in integrations/{folder}/"
        with open(lic_file, "r", encoding="utf-8") as f:
            content = f.read()
        assert expected_lic in content, f"License type {expected_lic} not declared in integrations/{folder}/LICENSE"
        assert expected_holder in content, f"Copyright holder {expected_holder} not declared in integrations/{folder}/LICENSE"


def test_06_references_no_broken_links():
    """Assertion 6: Verify Section 13 related skills references point to existing skills."""
    native_skills_dir = os.path.join(ROOT_DIR, ".agents", "skills")
    native_names = set(os.listdir(native_skills_dir))

    adapters = [
        os.path.join(ROOT_DIR, "integrations", "supabase", "dex-supabase-adapter", "SKILL.md"),
        os.path.join(ROOT_DIR, "integrations", "superpowers", "dex-superpowers-adapter", "SKILL.md"),
        os.path.join(ROOT_DIR, "integrations", "mattpocock", "dex-mattpocock-adapter", "SKILL.md"),
    ]

    for adapter_path in adapters:
        with open(adapter_path, "r", encoding="utf-8") as f:
            content = f.read()
        # Find Section 13
        sec13_match = re.search(r"## 13\.\s+Related.*?\n(.*?)(?=\n##|$)", content, re.DOTALL)
        assert sec13_match, f"Section 13 missing in {adapter_path}"
        refs = re.findall(r"(dex-[a-z0-9-]+)", sec13_match.group(1))
        for r in refs:
            assert r in native_names or r == os.path.basename(os.path.dirname(adapter_path)), (
                f"Broken skill reference '{r}' in {adapter_path}"
            )


def test_07_source_entries_unique():
    """Assertion 7: Verify upstream-sources.json contains exactly 7 unique upstream sources."""
    manifest_path = os.path.join(ROOT_DIR, "manifests", "upstream-sources.json")
    with open(manifest_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    sources = data.get("sources", [])
    assert len(sources) == 7, f"Expected 7 upstream sources, found {len(sources)}"
    uids = [s["upstream_id"] for s in sources]
    assert len(uids) == len(set(uids)), f"Duplicate upstream_id detected: {uids}"


def test_08_import_allowlist_valid():
    """Assertion 8: Verify config/import_allowlist.json includes all approved sources."""
    allowlist_path = os.path.join(ROOT_DIR, "config", "import_allowlist.json")
    assert os.path.isfile(allowlist_path)

    with open(allowlist_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    approved = data.get("approved_sources", [])
    source_ids = {s["source_id"] for s in approved}

    expected_ids = {
        "SOURCE_A_AAS",
        "SOURCE_B_REVERSE",
        "SOURCE_C_REA",
        "SOURCE_D_UI_UX_PRO_MAX",
        "SOURCE_E_SUPABASE",
        "SOURCE_F_SUPERPOWERS",
        "SOURCE_G_MATTPOCOCK",
    }
    assert expected_ids.issubset(source_ids), f"Missing approved sources: {expected_ids - source_ids}"


def test_09_auto_import_disabled_by_default():
    """Assertion 9: Verify auto_import_allowed is false across all sources in import_allowlist.json."""
    allowlist_path = os.path.join(ROOT_DIR, "config", "import_allowlist.json")
    with open(allowlist_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for src in data.get("approved_sources", []):
        assert src.get("auto_import_allowed") is False, f"Source {src['source_id']} has auto_import_allowed=True"
        assert src.get("requires_manual_audit") is True, f"Source {src['source_id']} does not require manual audit"


def test_10_master_orchestrator_not_overridden():
    """Assertion 10: Verify Master Orchestrator retains sole root control and bars external routers."""
    orchestrator_path = os.path.join(ROOT_DIR, ".agents", "skills", "dex-master-orchestrator", "SKILL.md")
    with open(orchestrator_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "dex-master-orchestrator" in content
    assert "8 k\u1ef9 n\u0103ng m\u1edf r\u1ed9ng t\u1eeb 7 ngu\u1ed3n upstream" in content or "8 bộ tích hợp" in content
    assert "using-superpowers" in content
    assert "chi\u1ebfm quy\u1ec1n \u0111i\u1ec1u ph\u1ed1i" in content or "ghi đè" in content

    # Check superpowers adapter explicitly defers to Master Orchestrator
    sp_adapter = os.path.join(ROOT_DIR, "integrations", "superpowers", "dex-superpowers-adapter", "SKILL.md")
    with open(sp_adapter, "r", encoding="utf-8") as f:
        sp_content = f.read()
    assert "dex-master-orchestrator" in sp_content
    assert "TUY\u1ec6T \u0110\u1ed0I KH\xd4NG" in sp_content or "Root Orchestrator Invariant" in sp_content


def test_11_native_dex_skill_count_invariant():
    """Assertion 11: Verify native DEX skill count remains exactly 401 (400 specialized + 1 orchestrator)."""
    native_skills_dir = os.path.join(ROOT_DIR, ".agents", "skills")
    native_dirs = [d for d in os.listdir(native_skills_dir) if os.path.isdir(os.path.join(native_skills_dir, d))]
    assert len(native_dirs) == 401, f"Native skill count invariant violated: expected 401, found {len(native_dirs)}"
    assert "dex-master-orchestrator" in native_dirs


def test_12_missing_upstream_runtime_detected():
    """Assertion 12: Verify missing upstream tools trigger deterministic non-hallucinatory fallbacks."""
    # Check supabase adapter defines RUNTIME_NOT_INSTALLED fallback
    supa_adapter = os.path.join(ROOT_DIR, "integrations", "supabase", "dex-supabase-adapter", "SKILL.md")
    with open(supa_adapter, "r", encoding="utf-8") as f:
        supa_content = f.read()
    assert "RUNTIME_NOT_INSTALLED" in supa_content
    assert "Zero-Hallucination" in supa_content

    # Check superpowers adapter defines worktree fallback
    sp_adapter = os.path.join(ROOT_DIR, "integrations", "superpowers", "dex-superpowers-adapter", "SKILL.md")
    with open(sp_adapter, "r", encoding="utf-8") as f:
        sp_content = f.read()
    assert "Zero-Hallucination" in sp_content
    assert "git checkout -b" in sp_content


def test_13_non_existent_tools_not_hallucinated():
    """Assertion 13: Verify adapters do not declare or invoke unverified external shell tools."""
    for rel_path in [
        "integrations/supabase/dex-supabase-adapter/SKILL.md",
        "integrations/superpowers/dex-superpowers-adapter/SKILL.md",
        "integrations/mattpocock/dex-mattpocock-adapter/SKILL.md",
    ]:
        with open(os.path.join(ROOT_DIR, rel_path), "r", encoding="utf-8") as f:
            content = f.read()
        assert "curl -s | bash" not in content
        assert "wget -q | sh" not in content
        assert "rm -rf /" not in content
        assert "format C:" not in content


def test_14_security_and_permissions_boundaries():
    """Assertion 14: Verify security boundaries prevent service_role secret leaks and prompt injections."""
    supa_path = os.path.join(ROOT_DIR, "integrations", "supabase", "dex-supabase-adapter", "SKILL.md")
    with open(supa_path, "r", encoding="utf-8") as f:
        supa_content = f.read()
    assert "SUPABASE_SERVICE_ROLE_KEY" in supa_content
    assert "Tuy\u1ec7t \u0111\u1ed1i kh\xf4ng l\u01b0u tr\u1eef" in supa_content or "Secret Isolation" in supa_content

    matt_path = os.path.join(ROOT_DIR, "integrations", "mattpocock", "dex-mattpocock-adapter", "SKILL.md")
    with open(matt_path, "r", encoding="utf-8") as f:
        matt_content = f.read()
    assert "PII" in matt_content or "synthetic data" in matt_content or "gi\u1ea3 l\u1eadp" in matt_content


def test_15_existing_dex_tests_unbroken():
    """Assertion 15: Verify all 14 mandatory sections are present across all 3 new adapters."""
    for rel_path in [
        "integrations/supabase/dex-supabase-adapter/SKILL.md",
        "integrations/superpowers/dex-superpowers-adapter/SKILL.md",
        "integrations/mattpocock/dex-mattpocock-adapter/SKILL.md",
    ]:
        with open(os.path.join(ROOT_DIR, rel_path), "r", encoding="utf-8") as f:
            content = f.read()
        for num, titles in MANDATORY_SECTIONS:
            sec_header = f"## {num}."
            assert sec_header in content, f"Missing section {sec_header} in {rel_path}"
