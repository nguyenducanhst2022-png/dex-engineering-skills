# -*- coding: utf-8 -*-
"""
DEX Polyglot Script Engine — Safe Subprocess Executor
Executes commands with shell=False, bounded buffers (512KB), timeouts,
Windows .cmd resolution, and secret sanitization.
"""

import os
import sys
import time
import shutil
import platform
import subprocess
from pathlib import Path
from typing import List, Optional, Dict, Any

from .result_schema import ExecutionResult
from .security import sanitize_secrets, validate_path, is_safe_command

MAX_OUTPUT_BYTES = 512 * 1024  # 512 KB buffer cap
DEFAULT_TIMEOUT = 60  # seconds

def resolve_command_executable(cmd: str) -> Optional[str]:
    """
    Resolve executable path. On Windows, resolve .cmd, .bat, or .exe
    if the bare name is passed (e.g. npm -> npm.cmd).
    """
    if platform.system() == "Windows":
        # Check if already has an extension
        ext = os.path.splitext(cmd)[1].lower()
        if ext in [".exe", ".cmd", ".bat", ".com", ".ps1"]:
            found = shutil.which(cmd)
            if found:
                return found

        # Try appending Windows script extensions
        for test_ext in [".cmd", ".exe", ".bat", ".com"]:
            candidate = f"{cmd}{test_ext}"
            found = shutil.which(candidate)
            if found:
                return found

    return shutil.which(cmd)

def execute_command(
    cmd_args: List[str],
    cwd: Optional[str] = None,
    timeout: int = DEFAULT_TIMEOUT,
    dry_run: bool = False,
    language: Optional[str] = None,
    command_name: str = "execute",
    env: Optional[Dict[str, str]] = None,
    allowed_base_dir: Optional[str] = None,
    evidence: Optional[Dict[str, Any]] = None,
) -> ExecutionResult:
    """
    Execute a command safely using subprocess.run with shell=False.
    """
    start_time = time.time()
    ev = evidence or {}

    if not cmd_args:
        return ExecutionResult(
            command=command_name,
            language=language,
            status="FAILED",
            exit_code=1,
            duration_ms=0.0,
            commands_executed=[],
            evidence=ev,
            errors=["Empty command arguments provided."]
        )

    # 1. Security check: Destructive command patterns
    is_safe, reason = is_safe_command(cmd_args)
    if not is_safe:
        return ExecutionResult(
            command=command_name,
            language=language,
            status="FAILED",
            exit_code=126,
            duration_ms=0.0,
            commands_executed=cmd_args,
            evidence=ev,
            errors=[f"Security Policy Violation: {reason}"]
        )

    # 2. Path Traversal & CWD validation
    resolved_cwd = None
    if cwd:
        try:
            resolved_cwd = str(validate_path(cwd, allowed_base_dir))
        except PermissionError as e:
            return ExecutionResult(
                command=command_name,
                language=language,
                status="FAILED",
                exit_code=126,
                duration_ms=0.0,
                commands_executed=cmd_args,
                evidence=ev,
                errors=[str(e)]
            )
    else:
        resolved_cwd = os.getcwd()

    cmd_str = " ".join(cmd_args)

    # 3. Dry-run early exit
    if dry_run:
        return ExecutionResult.dry_run(
            command=command_name,
            language=language,
            commands_to_execute=[cmd_str],
            cwd=resolved_cwd,
            evidence=ev
        )

    # 4. Resolve executable (Windows .cmd awareness)
    binary = cmd_args[0]
    resolved_binary = resolve_command_executable(binary)

    if not resolved_binary:
        return ExecutionResult.tool_not_available(
            command=command_name,
            language=language or "unknown",
            tool_name=binary,
            install_guide=f"Ensure '{binary}' is installed and added to the PATH environment variable."
        )

    prepared_args = [resolved_binary] + cmd_args[1:]

    # 5. Execute subprocess
    merged_env = os.environ.copy()
    if env:
        merged_env.update(env)

    # Enforce UTF-8 where possible
    merged_env["PYTHONIOENCODING"] = "utf-8"
    merged_env["LC_ALL"] = "C.UTF-8"

    try:
        proc = subprocess.run(
            prepared_args,
            cwd=resolved_cwd,
            shell=False,
            capture_output=True,
            timeout=timeout,
            env=merged_env
        )
        duration_ms = (time.time() - start_time) * 1000.0

        # Cap output buffer to 512KB and sanitize
        raw_stdout = proc.stdout[:MAX_OUTPUT_BYTES].decode("utf-8", errors="replace")
        raw_stderr = proc.stderr[:MAX_OUTPUT_BYTES].decode("utf-8", errors="replace")

        clean_stdout = sanitize_secrets(raw_stdout)
        clean_stderr = sanitize_secrets(raw_stderr)

        warnings = []
        if len(proc.stdout) > MAX_OUTPUT_BYTES:
            warnings.append(f"stdout exceeded {MAX_OUTPUT_BYTES} bytes cap and was truncated.")
        if len(proc.stderr) > MAX_OUTPUT_BYTES:
            warnings.append(f"stderr exceeded {MAX_OUTPUT_BYTES} bytes cap and was truncated.")

        status = "SUCCESS" if proc.returncode == 0 else "FAILED"
        errors = [f"Process exited with non-zero code {proc.returncode}"] if proc.returncode != 0 else []

        return ExecutionResult(
            command=command_name,
            language=language,
            status=status,
            exit_code=proc.returncode,
            duration_ms=round(duration_ms, 2),
            commands_executed=[cmd_str],
            evidence=ev,
            stdout=clean_stdout,
            stderr=clean_stderr,
            warnings=warnings,
            errors=errors
        )

    except subprocess.TimeoutExpired as e:
        duration_ms = (time.time() - start_time) * 1000.0
        out = e.stdout[:MAX_OUTPUT_BYTES].decode("utf-8", errors="replace") if e.stdout else ""
        err = e.stderr[:MAX_OUTPUT_BYTES].decode("utf-8", errors="replace") if e.stderr else ""
        return ExecutionResult(
            command=command_name,
            language=language,
            status="FAILED",
            exit_code=-1,
            duration_ms=round(duration_ms, 2),
            commands_executed=[cmd_str],
            evidence=ev,
            stdout=sanitize_secrets(out),
            stderr=sanitize_secrets(err),
            warnings=[f"Execution timed out after {timeout} seconds."],
            errors=[f"Command exceeded timeout limit of {timeout}s."]
        )

    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000.0
        return ExecutionResult(
            command=command_name,
            language=language,
            status="FAILED",
            exit_code=1,
            duration_ms=round(duration_ms, 2),
            commands_executed=[cmd_str],
            evidence=ev,
            errors=[f"Subprocess invocation error: {str(e)}"]
        )
