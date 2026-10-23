# -*- coding: utf-8 -*-
import pytest
from scripts.polyglot.core.registry import REGISTRY

def test_registry_contains_all_11_languages():
    langs = REGISTRY.list_languages()
    expected = [
        "bash", "cpp", "csharp", "go", "java", "javascript",
        "php", "powershell", "python", "rust", "typescript"
    ]
    assert sorted(langs) == sorted(expected)

def test_python_adapter_dry_run(tmp_path):
    adapter = REGISTRY.get_adapter("python")
    assert adapter is not None
    res = adapter.test(cwd=str(tmp_path), dry_run=True)
    assert res.status == "DRY_RUN"
    assert res.exit_code == 0

def test_typescript_adapter_dry_run(tmp_path):
    adapter = REGISTRY.get_adapter("typescript")
    assert adapter is not None
    res = adapter.lint(cwd=str(tmp_path), dry_run=True)
    assert res.status in ["DRY_RUN", "TOOL_NOT_AVAILABLE"]

def test_rust_adapter_behavior(tmp_path):
    adapter = REGISTRY.get_adapter("rust")
    assert adapter is not None
    res = adapter.test(cwd=str(tmp_path), dry_run=False)
    # If cargo is installed -> SUCCESS/FAILED; if not -> TOOL_NOT_AVAILABLE
    assert res.status in ["SUCCESS", "FAILED", "TOOL_NOT_AVAILABLE"]
    if res.status == "TOOL_NOT_AVAILABLE":
        assert "cargo" in res.errors[0]

def test_go_adapter_behavior(tmp_path):
    adapter = REGISTRY.get_adapter("go")
    assert adapter is not None
    res = adapter.lint(cwd=str(tmp_path), dry_run=False)
    assert res.status in ["SUCCESS", "FAILED", "TOOL_NOT_AVAILABLE"]
