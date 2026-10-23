# -*- coding: utf-8 -*-
"""
DEX Polyglot Script Engine — PowerShell Adapter
"""

import platform
from typing import Optional
from .base import BaseAdapter
from ..core.result_schema import ExecutionResult
from ..core.executor import execute_command
from ..core.detector import probe_tool

class PowerShellAdapter(BaseAdapter):
    def __init__(self):
        super().__init__(
            language="powershell",
            display_name="PowerShell",
            primary_tools=["pwsh", "powershell"]
        )

    def _get_shell(self) -> str:
        if probe_tool("pwsh")["available"]:
            return "pwsh"
        return "powershell"

    def lint(self, cwd: str, dry_run: bool = False) -> ExecutionResult:
        sh = self._get_shell()
        missing = self.require_tool(sh, "lint", "Install PowerShell or PowerShell Core (pwsh)")
        if missing:
            return missing
        cmd = [sh, "-NoProfile", "-NonInteractive", "-Command", "Invoke-ScriptAnalyzer -Path . -Recurse"]
        return execute_command(cmd, cwd=cwd, dry_run=dry_run, language=self.language, command_name="lint")

    def typecheck(self, cwd: str, dry_run: bool = False) -> ExecutionResult:
        # PowerShell dynamic typing verification via AST parser
        sh = self._get_shell()
        cmd = [
            sh, "-NoProfile", "-NonInteractive", "-Command",
            "$files = Get-ChildItem -Filter *.ps1 -Recurse; foreach ($f in $files) { [System.Management.Automation.Language.Parser]::ParseFile($f.FullName, [ref]$null, [ref]$errors); if ($errors) { exit 1 } }"
        ]
        return execute_command(cmd, cwd=cwd, dry_run=dry_run, language=self.language, command_name="typecheck")

    def build(self, cwd: str, dry_run: bool = False) -> ExecutionResult:
        # Module manifest validation or packaging
        sh = self._get_shell()
        cmd = [sh, "-NoProfile", "-NonInteractive", "-Command", "Get-ChildItem -Filter *.psd1 -Recurse | ForEach-Object { Test-ModuleManifest $_.FullName }"]
        return execute_command(cmd, cwd=cwd, dry_run=dry_run, language=self.language, command_name="build")

    def test(self, cwd: str, dry_run: bool = False, filter_name: Optional[str] = None) -> ExecutionResult:
        sh = self._get_shell()
        pester_cmd = "Invoke-Pester -Output Detailed"
        if filter_name:
            pester_cmd = f"Invoke-Pester -FullNameFilter '*{filter_name}*' -Output Detailed"
        cmd = [sh, "-NoProfile", "-NonInteractive", "-Command", pester_cmd]
        return execute_command(cmd, cwd=cwd, dry_run=dry_run, language=self.language, command_name="test")

    def audit(self, cwd: str, dry_run: bool = False) -> ExecutionResult:
        sh = self._get_shell()
        cmd = [sh, "-NoProfile", "-NonInteractive", "-Command", "Invoke-ScriptAnalyzer -Path . -Recurse -Severity Warning,Error"]
        return execute_command(cmd, cwd=cwd, dry_run=dry_run, language=self.language, command_name="audit")

    def benchmark(self, cwd: str, dry_run: bool = False) -> ExecutionResult:
        sh = self._get_shell()
        cmd = [sh, "-NoProfile", "-NonInteractive", "-Command", "Measure-Command { Get-ChildItem -Recurse }"]
        return execute_command(cmd, cwd=cwd, dry_run=dry_run, language=self.language, command_name="benchmark")
