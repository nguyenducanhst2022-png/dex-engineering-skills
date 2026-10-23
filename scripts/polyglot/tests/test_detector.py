# -*- coding: utf-8 -*-
from pathlib import Path
import pytest
from scripts.polyglot.core.detector import detect_languages, probe_tool

FIXTURES_DIR = Path(__file__).parent / "fixtures"

def test_probe_python_available():
    info = probe_tool("python")
    assert info["available"] is True
    assert info["path"] is not None

def test_probe_missing_tool():
    info = probe_tool("nonexistent_fake_tool_xyz")
    assert info["available"] is False
    assert info["path"] is None

@pytest.mark.parametrize("lang", [
    "python", "typescript", "javascript", "powershell", "bash",
    "rust", "go", "cpp", "csharp", "java", "php"
])
def test_detect_all_11_fixtures(lang):
    fixture_path = FIXTURES_DIR / lang
    assert fixture_path.exists(), f"Fixture directory for {lang} must exist"
    detected = detect_languages(str(fixture_path))
    assert len(detected) > 0, f"Must detect language in {lang} fixture"
    detected_langs = [d["language"] for d in detected]
    assert lang in detected_langs, f"Expected {lang} in {detected_langs}"
