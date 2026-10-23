# -*- coding: utf-8 -*-
import sys
import subprocess
import json
import pytest

def test_cli_status():
    proc = subprocess.run([sys.executable, "scripts/polyglot/dex.py", "status"], capture_output=True, text=True)
    assert proc.returncode == 0
    assert "DEX Polyglot Script Engine" in proc.stdout
    assert "Supported Languages: 11" in proc.stdout

def test_cli_status_json():
    proc = subprocess.run([sys.executable, "scripts/polyglot/dex.py", "status", "-f", "json"], capture_output=True, text=True)
    assert proc.returncode == 0
    data = json.loads(proc.stdout)
    assert data["status"] == "SUCCESS"
    assert data["schema_version"] == "1.0.0"
    assert len(data["evidence"]["all_languages"]) == 11

def test_cli_doctor():
    proc = subprocess.run([sys.executable, "scripts/polyglot/dex.py", "doctor"], capture_output=True, text=True)
    assert proc.returncode == 0
    assert "DEX Polyglot Toolchain Diagnostics" in proc.stdout

def test_cli_dry_run():
    proc = subprocess.run([sys.executable, "scripts/polyglot/dex.py", "test", "--dry-run"], capture_output=True, text=True)
    assert proc.returncode == 0
    assert "[DRY_RUN]" in proc.stdout

def test_cli_generate(tmp_path):
    out_dir = str(tmp_path / "gen")
    proc = subprocess.run([sys.executable, "scripts/polyglot/dex.py", "generate", "--lang", "python", "--task", "sample_job", "--out", out_dir], capture_output=True, text=True)
    assert proc.returncode == 0
    assert "Successfully generated" in proc.stdout
