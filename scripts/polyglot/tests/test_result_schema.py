# -*- coding: utf-8 -*-
import json
import pytest
from scripts.polyglot.core.result_schema import ExecutionResult

def test_execution_result_serialization():
    res = ExecutionResult(
        command="test",
        language="python",
        status="SUCCESS",
        exit_code=0,
        duration_ms=42.5,
        commands_executed=["pytest"],
        evidence={"passed": 10},
        stdout="All passed",
        stderr="",
        warnings=[],
        errors=[]
    )
    d = res.to_dict()
    assert d["schema_version"] == "1.0.0"
    assert d["command"] == "test"
    assert d["status"] == "SUCCESS"
    assert d["exit_code"] == 0

    json_str = res.to_json()
    parsed = json.loads(json_str)
    assert parsed["duration_ms"] == 42.5

def test_tool_not_available_factory():
    res = ExecutionResult.tool_not_available(
        command="build",
        language="rust",
        tool_name="cargo",
        install_guide="Install rustup"
    )
    assert res.status == "TOOL_NOT_AVAILABLE"
    assert res.exit_code == 127
    assert "cargo" in res.errors[0]
    assert "Install rustup" in res.warnings[0]

def test_dry_run_factory():
    res = ExecutionResult.dry_run(
        command="test",
        language="typescript",
        commands_to_execute=["npm test"],
        cwd="/workspace"
    )
    assert res.status == "DRY_RUN"
    assert res.exit_code == 0
    assert "[DRY-RUN]" in res.stdout
