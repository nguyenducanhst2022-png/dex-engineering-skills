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

def test_large_dual_stream_output_is_bounded(tmp_path):
    from scripts.polyglot.core.executor import MAX_OUTPUT_BYTES
    code = "import os; os.write(1,b'x'*2000000); os.write(2,b'y'*2000000)"
    result = execute_command([sys.executable, '-c', code], cwd=str(tmp_path))
    assert result.exit_code == 0
    assert len(result.stdout) == MAX_OUTPUT_BYTES
    assert len(result.stderr) == MAX_OUTPUT_BYTES
    assert len(result.warnings) == 2


def test_ambient_credentials_require_explicit_environment(monkeypatch, tmp_path):
    monkeypatch.setenv('DEX_TEST_PRIVATE_TOKEN', 'fixture-value')
    code = "import os; print(os.environ.get('DEX_TEST_PRIVATE_TOKEN','absent'))"
    result = execute_command([sys.executable, '-c', code], cwd=str(tmp_path))
    assert result.stdout.strip() == 'absent'
    result = execute_command([sys.executable, '-c', code], cwd=str(tmp_path),
                             env={'DEX_TEST_PRIVATE_TOKEN': 'explicit-fixture'})
    assert result.stdout.strip() == 'explicit-fixture'


def test_timeout_stops_descendant_side_effect(tmp_path):
    marker = tmp_path / 'should-not-exist'
    child = "import time; from pathlib import Path; time.sleep(3); Path('should-not-exist').touch()"
    parent = "import subprocess,sys,time; subprocess.Popen([sys.executable,'-c'," + repr(child) + "]); time.sleep(20)"
    result = execute_command([sys.executable, '-c', parent], cwd=str(tmp_path), timeout=1)
    assert result.exit_code == -1
    import time
    time.sleep(3)
    assert not marker.exists()
