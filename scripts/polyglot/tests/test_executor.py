# -*- coding: utf-8 -*-
import sys
import pytest
from scripts.polyglot.core.executor import execute_command, resolve_command_executable

def test_resolve_command_executable():
    # Python executable should always resolve
    py = resolve_command_executable(sys.executable)
    assert py is not None

def test_execute_command_success(tmp_path):
    res = execute_command([sys.executable, "-c", "print('hello polyglot')"], cwd=str(tmp_path))
    assert res.status == "SUCCESS"
    assert res.exit_code == 0
    assert "hello polyglot" in res.stdout
    assert res.duration_ms > 0

def test_execute_command_dry_run(tmp_path):
    res = execute_command([sys.executable, "-c", "import os; os.remove('fake.txt')"], cwd=str(tmp_path), dry_run=True)
    assert res.status == "DRY_RUN"
    assert res.exit_code == 0
    assert "[DRY-RUN]" in res.stdout

def test_execute_command_timeout(tmp_path):
    res = execute_command([sys.executable, "-c", "import time; time.sleep(5)"], cwd=str(tmp_path), timeout=1)
    assert res.status == "FAILED"
    assert res.exit_code == -1
    assert "timed out" in res.warnings[0].lower() or "timeout" in res.errors[0].lower()

def test_execute_command_missing_tool():
    res = execute_command(["nonexistent_dex_tool_12345", "--help"])
    assert res.status == "TOOL_NOT_AVAILABLE"
    assert res.exit_code == 127
