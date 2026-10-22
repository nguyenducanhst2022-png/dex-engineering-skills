# -*- coding: utf-8 -*-
"""
Pytest suite for UI/UX Pro Max Integration & Design Intelligence Bridge.
Tests source metadata, adapter skill structure, runtime detection (Option A & B),
real search execution across domains and stacks, non-hallucinatory fallbacks,
and Master Orchestrator dynamic routing boundaries.
"""

import os
import sys
import json
import pytest

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT_DIR, "scripts"))

from ui_ux_pro_max_runner import (
    detect_runtime,
    is_runtime_installed,
    search,
    VALID_DOMAINS,
    VALID_STACKS
)

def test_ui_ux_pro_max_source_metadata():
    """Verify source.json metadata, pinned commit, license, and checksum integrity."""
    source_file = os.path.join(ROOT_DIR, "integrations", "ui-ux-pro-max", "source.json")
    assert os.path.isfile(source_file), "source.json must exist in integrations/ui-ux-pro-max/"

    with open(source_file, "r", encoding="utf-8") as f:
        meta = json.load(f)

    assert meta["upstream_id"] == "source-d-ui-ux-pro-max"
    assert meta["name"] == "UI/UX Pro Max"
    assert meta["author"] == "NextLevelBuilder"
    assert meta["license"] == "MIT"
    assert meta["pinned_commit"] == "04cfb449bd8494811ad63e94172a308fa25a551a"
    assert meta["status"] == "ACTIVE_VERIFIED"
    assert len(meta["search_domains"]) == 12
    assert len(meta["supported_stacks"]) == 22
    assert len(meta["checksums_sha256"]) >= 5

def test_ui_ux_pro_max_adapter_structure():
    """Verify dex-ui-ux-pro-max-adapter skill exists and strictly implements all 14 mandatory sections."""
    skill_file = os.path.join(
        ROOT_DIR, "integrations", "ui-ux-pro-max", "dex-ui-ux-pro-max-adapter", "SKILL.md"
    )
    assert os.path.isfile(skill_file), "dex-ui-ux-pro-max-adapter/SKILL.md must exist"

    with open(skill_file, "r", encoding="utf-8") as f:
        content = f.read()

    assert "name: dex-ui-ux-pro-max-adapter" in content
    assert "description:" in content

    mandatory_sections = [
        "## 1. Purpose & Scope",
        "## 2. When to Use",
        "## 3. When NOT to Use",
        "## 4. Prerequisites & Input Context",
        "## 5. Core Concepts & Taxonomy",
        "## 6. Step-by-Step Execution Workflow",
        "## 7. Concrete Examples",
        "## 8. Anti-Patterns & Common Traps",
        "## 9. Quality Gates & Acceptance Criteria",
        "## 10. Security & Safety Boundaries",
        "## 11. Platform Adapters",
        "## 12. Deliverables & Output Artifacts",
        "## 13. Related & Complementary Skills",
        "## 14. Realistic Usage Example",
    ]

    for sec in mandatory_sections:
        assert sec in content, f"Missing section '{sec}' in dex-ui-ux-pro-max-adapter/SKILL.md"

def test_runtime_detection_available():
    """Verify that the local vendored or detected runtime is discovered and verified."""
    rt = detect_runtime()
    assert rt["installed"] is True
    assert rt["mode"] in ["EXTERNAL_ENV", "EXTERNAL_GLOBAL", "VENDORED_LOCAL"]
    assert os.path.isfile(rt["search_script"])
    assert is_runtime_installed() is True

def test_runtime_detection_missing(monkeypatch):
    """Verify that when runtime is missing, runner reports clean NOT INSTALLED without hallucinating."""
    import ui_ux_pro_max_runner

    # Point all discovery paths to nonexistent locations
    monkeypatch.setenv("UI_UX_PRO_MAX_PATH", "/nonexistent/fake/path")
    monkeypatch.setattr(ui_ux_pro_max_runner, "KNOWN_EXTERNAL_PATHS", ["/nonexistent/fake/global"])
    monkeypatch.setattr(ui_ux_pro_max_runner, "VENDORED_SEARCH_SCRIPT", "/nonexistent/fake/search.py")

    rt = ui_ux_pro_max_runner.detect_runtime()
    assert rt["installed"] is False
    assert rt["mode"] == "NOT_INSTALLED"

    res = ui_ux_pro_max_runner.search("fintech dashboard", json_output=True)
    assert isinstance(res, dict)
    assert res["status"] == "NOT_INSTALLED"
    assert "git clone" in res["error"]
    assert res["results"] == []

def test_real_design_system_search():
    """Execute real design system generation and verify comprehensive styling output."""
    res = search("fintech banking dashboard", design_system=True, output_format="markdown")
    assert isinstance(res, str)
    assert "## Design System:" in res
    assert "### Pattern" in res
    assert "### Style" in res
    assert "### Colors" in res
    assert "--color-primary" in res
    assert "### Typography" in res
    assert "Google Fonts:" in res
    assert "### Pre-Delivery Checklist" in res

def test_real_domain_search_style():
    """Execute real style domain search and verify returned UI style attributes."""
    res = search("fintech dashboard", domain="style", json_output=True)
    assert isinstance(res, dict)
    assert res["domain"] == "style"
    assert res["count"] > 0
    first_result = res["results"][0]
    assert "Style ID" in first_result
    assert "Primary Colors" in first_result
    assert "Accessibility" in first_result

def test_real_domain_search_ux():
    """Execute real UX domain search and verify UX rules and guidelines."""
    res = search("button feedback", domain="ux", json_output=True)
    assert isinstance(res, dict)
    assert res["domain"] == "ux"
    assert "results" in res

def test_real_stack_search_react():
    """Execute real stack-specific search for React."""
    res = search("responsive layout", stack="react", json_output=True)
    assert isinstance(res, dict)
    assert "results" in res

def test_real_stack_search_tailwind():
    """Execute real stack-specific search for HTML/Tailwind."""
    res = search("grid layout", stack="html-tailwind", json_output=True)
    assert isinstance(res, dict)
    assert "results" in res

def test_zero_results_query():
    """Verify that a query matching 0 results behaves gracefully without throwing."""
    res = search("zyxwvu987654321nonexistentterm", domain="style", json_output=True)
    assert isinstance(res, dict)
    assert res["count"] == 0
    assert res["results"] == []

def test_invalid_domain_query():
    """Verify that invalid domain raises ValueError."""
    with pytest.raises(ValueError) as excinfo:
        search("query", domain="invalid_domain_xyz")
    assert "Invalid domain" in str(excinfo.value)

def test_invalid_stack_query():
    """Verify that invalid stack raises ValueError."""
    with pytest.raises(ValueError) as excinfo:
        search("query", stack="invalid_stack_xyz")
    assert "Invalid stack" in str(excinfo.value)

def test_master_orchestrator_routing_ui_request():
    """Verify that Master Orchestrator routes UI design requests to UI/UX Pro Max and Design Tokens."""
    orchestrator_path = os.path.join(ROOT_DIR, ".agents", "skills", "dex-master-orchestrator", "SKILL.md")
    with open(orchestrator_path, "r", encoding="utf-8") as f:
        orch_content = f.read()

    assert "dex-ui-ux-pro-max-adapter" in orch_content
    assert "dex-design-system-tokens" in orch_content
    assert "integrations/ui-ux-pro-max" in orch_content

def test_master_orchestrator_routing_backend_exclusion():
    """Verify that Master Orchestrator explicitly excludes UI/UX Pro Max from backend/DevOps requests."""
    orchestrator_path = os.path.join(ROOT_DIR, ".agents", "skills", "dex-master-orchestrator", "SKILL.md")
    with open(orchestrator_path, "r", encoding="utf-8") as f:
        orch_content = f.read()

    assert "Chặn kích hoạt trên các tác vụ backend, database hoặc DevOps" in orch_content
