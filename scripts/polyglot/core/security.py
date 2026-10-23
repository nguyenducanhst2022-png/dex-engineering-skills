# -*- coding: utf-8 -*-
"""
DEX Polyglot Script Engine — Security Subsystem
Handles secret sanitization, path traversal validation, and command safety screening.
"""

import os
import re
from pathlib import Path
from typing import Optional, List, Tuple

# Patterns to sanitize from outputs, logs, and evidence
SECRET_PATTERNS = [
    # AWS Access Key ID
    (re.compile(r"\b(AKIA|ABIA|ACCA|ASIA)[0-9A-Z]{16}\b"), r"\1[REDACTED_AWS_KEY]"),
    # GitHub Tokens
    (re.compile(r"\b(gh[pousr]_[A-Za-z0-9_]{36,})\b"), r"[REDACTED_GITHUB_TOKEN]"),
    (re.compile(r"\b(github_pat_[A-Za-z0-9_]{82})\b"), r"[REDACTED_GITHUB_PAT]"),
    # Generic Private Key blocks
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----[\s\S]*?-----END [A-Z ]*PRIVATE KEY-----"), r"[REDACTED_PRIVATE_KEY]"),
    # OpenAI API Keys
    (re.compile(r"\bsk-[a-zA-Z0-9_-]{32,}\b"), r"[REDACTED_OPENAI_KEY]"),
    # Slack Tokens
    (re.compile(r"\bxox[baprs]-[0-9a-zA-Z]{10,}\b"), r"[REDACTED_SLACK_TOKEN]"),
    # Connection string credentials (postgres://user:pass@host)
    (re.compile(r"(://[^:\s]+):([^@\s]+)@"), r"\1:[REDACTED_PASSWORD]@"),
    # Generic password assignments
    (re.compile(r"(?i)(password|secret|token|api_key|apikey)\s*[:=]\s*['\"]?([A-Za-z0-9_!@#$%^&*()\-+=]{8,})['\"]?"), r"\1=[REDACTED]"),
]

# Blacklisted command tokens / patterns
DESTRUCTIVE_COMMAND_PATTERNS = [
    re.compile(r"(?i)\brm\s+(-[a-z]*r[a-z]*f|-rf|-fr)\s+([/\\]|\*|~|/\*)"),
    re.compile(r"(?i)\bmkfs(\.[a-z0-9]+)?\b"),
    re.compile(r"(?i)\bdd\s+if=.*of=(/dev/|\\\\.\\[a-z]:)"),
    re.compile(r"(?i)\bformat\s+[a-z]:\s+/fs:"),
    re.compile(r"(?i)\b(del|rmdir)\s+/[sS]\s+/[qQ]\s+[cC]:\\"),
]

def sanitize_secrets(text: Optional[str]) -> str:
    """Redact secrets and sensitive tokens from text output."""
    if not text:
        return ""
    result = text
    for pattern, replacement in SECRET_PATTERNS:
        result = pattern.sub(replacement, result)
    return result

def validate_path(target_path: str, base_dir: Optional[str] = None) -> Path:
    """
    Validate that target_path resolves inside base_dir to prevent path traversal.
    If base_dir is None, resolves the path and ensures it does not contain relative escapes.
    Raises PermissionError if path attempts to escape base_dir.
    """
    target = Path(target_path)

    if base_dir is not None:
        base = Path(base_dir).resolve()
        if not target.is_absolute():
            target = (base / target).resolve()
        else:
            target = target.resolve()

        try:
            target.relative_to(base)
        except ValueError:
            raise PermissionError(
                f"Path traversal detected: Target path '{target}' escapes allowed base directory '{base}'."
            )
        return target
    else:
        return target.resolve()

    return target

def is_safe_command(cmd_args: List[str]) -> Tuple[bool, str]:
    """
    Validate whether a command line is safe from catastrophic destructive patterns.
    Returns (True, "") if safe, or (False, reason) if destructive.
    """
    if not cmd_args:
        return True, ""

    joined = " ".join(cmd_args)
    for pattern in DESTRUCTIVE_COMMAND_PATTERNS:
        if pattern.search(joined):
            return False, f"Command contains blacklisted destructive pattern: '{joined}'"

    return True, ""
