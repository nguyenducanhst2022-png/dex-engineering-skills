# -*- coding: utf-8 -*-
"""
Pytest suite for REA MCP Adapter and Diagnostic Probe (rea_mcp_probe.py).
Tests MCP detection, schema integrity, and zero-hallucination fallback messages.
"""

import os
import sys
import pytest

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(ROOT_DIR, "scripts"))

from rea_mcp_probe import probe_rea_mcp, REA_TOOL_SCHEMAS

def test_rea_tool_schemas_integrity():
    """Verify REA tool schemas follow standard MCP JSON Schema format."""
    assert len(REA_TOOL_SCHEMAS) >= 3
    tool_names = [t["name"] for t in REA_TOOL_SCHEMAS]
    assert "rea_inspect_binary" in tool_names
    assert "rea_decompile_function" in tool_names
    assert "rea_extract_symbols" in tool_names

    for tool in REA_TOOL_SCHEMAS:
        assert "description" in tool
        assert "parameters" in tool
        assert tool["parameters"]["type"] == "object"
        assert "binary_path" in tool["parameters"]["properties"]

def test_rea_probe_environment_fallback():
    """Verify that when REA MCP is absent, probe provides non-hallucinatory guidance."""
    res = probe_rea_mcp()
    assert "mcp_server" in res
    assert "status" in res
    assert "guidance" in res
    assert "npx rea-agents setup" in res["guidance"]

def test_rea_adapter_skill_structure():
    """Verify dex-rea-adapter skill exists in integrations/rea and contains 14 mandatory sections."""
    skill_file = os.path.join(ROOT_DIR, "integrations", "rea", "dex-rea-adapter", "SKILL.md")
    if not os.path.isfile(skill_file):
        skill_file = os.path.join(ROOT_DIR, ".agents", "skills", "dex-rea-adapter", "SKILL.md")
    assert os.path.isfile(skill_file)

    with open(skill_file, "r", encoding="utf-8") as f:
        content = f.read()

    assert "name: dex-rea-adapter" in content
    assert "## 1. Purpose & Scope" in content
    assert "## 14. Realistic Usage Example" in content
    assert "Giao thức Ngữ cảnh Mô hình" in content or "Model Context Protocol" in content
