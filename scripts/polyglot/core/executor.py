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
import threading
import signal
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
    Execute a command safely using bounded streaming capture with shell=False.
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

    # Only runtime/OS configuration is inherited. Credentials require explicit opt-in.
    allowed_env = {"PATH", "PATHEXT", "SYSTEMROOT", "WINDIR", "COMSPEC", "TEMP", "TMP",
                   "HOME", "USERPROFILE", "APPDATA", "LOCALAPPDATA", "PROGRAMFILES",
                   "PROGRAMFILES(X86)", "PROGRAMDATA", "VIRTUAL_ENV", "JAVA_HOME",
                   "DOTNET_ROOT", "CARGO_HOME", "RUSTUP_HOME", "GOPATH", "GOROOT"}
    merged_env = {k: v for k, v in os.environ.items() if k.upper() in allowed_env}
    if env:
        merged_env.update(env)
    merged_env["PYTHONIOENCODING"] = "utf-8"
    merged_env["LC_ALL"] = "C.UTF-8"

    buffers = [bytearray(), bytearray()]
    truncated = [False, False]

    def drain(stream, index):
        # Drain both pipes continuously; retain at most the configured cap per pipe.
        try:
            while True:
                chunk = stream.read(8192)
                if not chunk:
                    break
                remaining = MAX_OUTPUT_BYTES - len(buffers[index])
                buffers[index].extend(chunk[:remaining])
                if len(chunk) > remaining:
                    truncated[index] = True
        finally:
            stream.close()

    def stop_tree(proc):
        if os.name == "nt":
            # taskkill receives a numeric PID as an argument, never shell input.
            killer = os.path.join(os.environ.get("SystemRoot", r"C:\Windows"), "System32", "taskkill.exe")
            try:
                subprocess.run([killer, "/PID", str(proc.pid), "/T", "/F"],
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=5)
            except (OSError, subprocess.TimeoutExpired):
                pass
        else:
            try:
                os.killpg(proc.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        if proc.poll() is None:
            proc.kill()
        proc.wait(timeout=5)

    proc = None
    readers = []
    timed_out = False
    try:
        if timeout <= 0:
            raise ValueError("timeout must be positive")
        proc = subprocess.Popen(
            prepared_args, cwd=resolved_cwd, shell=False,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=merged_env,
            start_new_session=(os.name != "nt"),
        )
        for index, stream in enumerate((proc.stdout, proc.stderr)):
            thread = threading.Thread(target=drain, args=(stream, index), daemon=True)
            thread.start()
            readers.append(thread)
        try:
            proc.wait(timeout=timeout)
            # Children can retain inherited pipe handles after the parent exits.
            deadline = start_time + timeout
            for thread in readers:
                thread.join(max(0, deadline - time.time()))
            if any(thread.is_alive() for thread in readers):
                timed_out = True
                stop_tree(proc)
        except subprocess.TimeoutExpired:
            timed_out = True
            stop_tree(proc)
        for thread in readers:
            thread.join(5)
        warnings = [f"{name} exceeded {MAX_OUTPUT_BYTES} bytes cap and was truncated."
                    for index, name in enumerate(("stdout", "stderr")) if truncated[index]]
        if any(thread.is_alive() for thread in readers):
            warnings.append("Descendant pipe cleanup incomplete; process isolation requires host supervision.")
        if timed_out:
            warnings.insert(0, f"Execution timed out after {timeout} seconds.")
        exit_code = -1 if timed_out else proc.returncode
        return ExecutionResult(
            command=command_name, language=language,
            status="SUCCESS" if exit_code == 0 else "FAILED", exit_code=exit_code,
            duration_ms=round((time.time() - start_time) * 1000, 2),
            commands_executed=[cmd_str], evidence=ev,
            stdout=sanitize_secrets(bytes(buffers[0]).decode("utf-8", errors="replace")),
            stderr=sanitize_secrets(bytes(buffers[1]).decode("utf-8", errors="replace")),
            warnings=warnings,
            errors=([f"Command exceeded timeout limit of {timeout}s."] if timed_out else
                    [f"Process exited with non-zero code {exit_code}"] if exit_code else []),
        )
    except Exception as e:
        return ExecutionResult(
            command=command_name, language=language, status="FAILED", exit_code=1,
            duration_ms=round((time.time() - start_time) * 1000, 2),
            commands_executed=[cmd_str], evidence=ev,
            errors=[sanitize_secrets(f"Subprocess invocation error: {e}")],
        )
    finally:
        # Also runs for KeyboardInterrupt/cancellation; never leave a live direct child.
        if proc is not None and proc.poll() is None:
            stop_tree(proc)
