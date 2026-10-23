# -*- coding: utf-8 -*-
"""
DEX Polyglot Script Engine — Bash Adapter
"""

from typing import Optional
from .base import BaseAdapter
from ..core.result_schema import ExecutionResult
from ..core.executor import execute_command
from ..core.detector import probe_tool

class BashAdapter(BaseAdapter):
    def __init__(self):
        super().__init__(
            language="bash",
            display_name="Bash / POSIX Shell",
            primary_tools=["bash", "sh", "shellcheck", "bats"]
        )

    def lint(self, cwd: str, dry_run: bool = False) -> ExecutionResult:
        if probe_tool("shellcheck")["available"]:
            return execute_command(["shellcheck", "**/*.sh"], cwd=cwd, dry_run=dry_run, language=self.language, command_name="lint")
        else:
            missing = self.require_tool("bash", "lint", "Install Bash (Git Bash on Windows, or via apt/brew)")
            if missing:
                return missing
            # Basic syntax check via bash -n
            return execute_command(
                ["bash", "-c", "for f in *.sh; do [ -f \"$f\" ] && bash -n \"$f\"; done"],
                cwd=cwd,
                dry_run=dry_run,
                language=self.language,
                command_name="lint",
                evidence={"strategy": "bash -n syntax check"}
            )

    def typecheck(self, cwd: str, dry_run: bool = False) -> ExecutionResult:
        # Bash does not have a static typechecker; runs shellcheck strict
        return self.lint(cwd, dry_run=dry_run)

    def build(self, cwd: str, dry_run: bool = False) -> ExecutionResult:
        missing = self.require_tool("bash", "build", "Install Bash")
        if missing:
            return missing
        return execute_command(["bash", "-c", "chmod +x *.sh 2>/dev/null || true"], cwd=cwd, dry_run=dry_run, language=self.language, command_name="build")

    def test(self, cwd: str, dry_run: bool = False, filter_name: Optional[str] = None) -> ExecutionResult:
        if probe_tool("bats")["available"]:
            cmd = ["bats", "test/"]
            if filter_name:
                cmd.extend(["-f", filter_name])
            return execute_command(cmd, cwd=cwd, dry_run=dry_run, language=self.language, command_name="test")
        else:
            missing = self.require_tool("bash", "test", "Install bats or bash")
            if missing:
                return missing
            return execute_command(["bash", "-c", "for f in test*.sh; do [ -f \"$f\" ] && bash \"$f\"; done"], cwd=cwd, dry_run=dry_run, language=self.language, command_name="test")

    def audit(self, cwd: str, dry_run: bool = False) -> ExecutionResult:
        if probe_tool("shellcheck")["available"]:
            return execute_command(["shellcheck", "-s", "bash", "-S", "warning", "**/*.sh"], cwd=cwd, dry_run=dry_run, language=self.language, command_name="audit")
        else:
            return self.require_tool("shellcheck", "audit", "Install shellcheck via: winget install koalaman.shellcheck / brew install shellcheck")

    def benchmark(self, cwd: str, dry_run: bool = False) -> ExecutionResult:
        missing = self.require_tool("bash", "benchmark", "Install Bash")
        if missing:
            return missing
        return execute_command(["bash", "-c", "time (for f in *.sh; do [ -f \"$f\" ] && bash \"$f\" >/dev/null 2>&1; done)"], cwd=cwd, dry_run=dry_run, language=self.language, command_name="benchmark")
