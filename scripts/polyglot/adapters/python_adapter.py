# -*- coding: utf-8 -*-
"""
DEX Polyglot Script Engine — Python Adapter
"""

import sys
from typing import Optional
from .base import BaseAdapter
from ..core.result_schema import ExecutionResult
from ..core.executor import execute_command
from ..core.detector import probe_tool

class PythonAdapter(BaseAdapter):
    def __init__(self):
        super().__init__(
            language="python",
            display_name="Python 3",
            primary_tools=["python", "pytest", "ruff", "mypy", "flake8"]
        )

    def _get_python_cmd(self) -> str:
        return sys.executable

    def lint(self, cwd: str, dry_run: bool = False) -> ExecutionResult:
        # Check ruff or flake8 or fallback to py_compile
        py = self._get_python_cmd()
        if probe_tool("ruff")["available"]:
            return execute_command(["ruff", "check", "."], cwd=cwd, dry_run=dry_run, language=self.language, command_name="lint")
        elif probe_tool("flake8")["available"]:
            return execute_command(["flake8", "."], cwd=cwd, dry_run=dry_run, language=self.language, command_name="lint")
        else:
            # Fallback syntax compile
            return execute_command(
                [py, "-m", "compileall", "-q", "."],
                cwd=cwd,
                dry_run=dry_run,
                language=self.language,
                command_name="lint",
                evidence={"strategy": "compileall"}
            )

    def typecheck(self, cwd: str, dry_run: bool = False) -> ExecutionResult:
        if probe_tool("mypy")["available"]:
            return execute_command(["mypy", "."], cwd=cwd, dry_run=dry_run, language=self.language, command_name="typecheck")
        else:
            return self.require_tool("mypy", "typecheck", "Install via: pip install mypy")

    def build(self, cwd: str, dry_run: bool = False) -> ExecutionResult:
        py = self._get_python_cmd()
        return execute_command(
            [py, "-m", "build"],
            cwd=cwd,
            dry_run=dry_run,
            language=self.language,
            command_name="build"
        )

    def test(self, cwd: str, dry_run: bool = False, filter_name: Optional[str] = None) -> ExecutionResult:
        py = self._get_python_cmd()
        cmd = [py, "-m", "pytest"]
        if filter_name:
            cmd.extend(["-k", filter_name])
        return execute_command(
            cmd,
            cwd=cwd,
            dry_run=dry_run,
            language=self.language,
            command_name="test"
        )

    def audit(self, cwd: str, dry_run: bool = False) -> ExecutionResult:
        if probe_tool("pip-audit")["available"]:
            return execute_command(["pip-audit"], cwd=cwd, dry_run=dry_run, language=self.language, command_name="audit")
        else:
            return self.require_tool("pip-audit", "audit", "Install via: pip install pip-audit")

    def benchmark(self, cwd: str, dry_run: bool = False) -> ExecutionResult:
        py = self._get_python_cmd()
        cmd = [py, "-m", "pytest", "--benchmark-only"]
        return execute_command(cmd, cwd=cwd, dry_run=dry_run, language=self.language, command_name="benchmark")
