# -*- coding: utf-8 -*-
import pytest
from pathlib import Path
from scripts.polyglot.core.security import sanitize_secrets, validate_path, is_safe_command

def test_sanitize_secrets_aws():
    text = "Error connecting with AKIAIOSFODNN7EXAMPLE key"
    sanitized = sanitize_secrets(text)
    assert "AKIA[REDACTED_AWS_KEY]" in sanitized
    assert "AKIAIOSFODNN7EXAMPLE" not in sanitized

def test_sanitize_secrets_github_token():
    text = "Pushing with token ghp_123456789012345678901234567890123456"
    sanitized = sanitize_secrets(text)
    assert "[REDACTED_GITHUB_TOKEN]" in sanitized
    assert "ghp_123456789012345678901234567890123456" not in sanitized

def test_sanitize_secrets_connection_string():
    text = "Connecting to postgresql://admin:SuperSecretPass123!@db.internal:5432/app"
    sanitized = sanitize_secrets(text)
    assert "[REDACTED_PASSWORD]" in sanitized
    assert "SuperSecretPass123!" not in sanitized

def test_validate_path_safe(tmp_path):
    sub = tmp_path / "subdir"
    sub.mkdir()
    validated = validate_path(str(sub), base_dir=str(tmp_path))
    assert validated == sub.resolve()

def test_validate_path_traversal_blocked(tmp_path):
    with pytest.raises(PermissionError):
        validate_path(str(tmp_path / ".." / "outside"), base_dir=str(tmp_path))

def test_is_safe_command():
    safe, _ = is_safe_command(["pytest", "tests/"])
    assert safe is True

    unsafe, reason = is_safe_command(["rm", "-rf", "/"])
    assert unsafe is False
    assert "blacklisted" in reason

    unsafe_win, _ = is_safe_command(["del", "/s", "/q", "c:\\"])
    assert unsafe_win is False
