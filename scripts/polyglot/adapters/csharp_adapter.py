# -*- coding: utf-8 -*-
"""
DEX Polyglot Script Engine — C# (.NET) Adapter
"""

from typing import Optional
from .base import BaseAdapter
from ..core.result_schema import ExecutionResult
from ..core.executor import execute_command

INSTALL_DOTNET_GUIDE = "Install .NET SDK from https://dotnet.microsoft.com/download (or winget install Microsoft.DotNet.SDK.8 / brew install dotnet)"

class CSharpAdapter(BaseAdapter):
    def __init__(self):
        super().__init__(
            language="csharp",
            display_name="C# (.NET)",
            primary_tools=["dotnet"]
        )

    def lint(self, cwd: str, dry_run: bool = False) -> ExecutionResult:
        missing = self.require_tool("dotnet", "lint", INSTALL_DOTNET_GUIDE)
        if missing:
            return missing
        return execute_command(["dotnet", "format", "--verify-no-changes"], cwd=cwd, dry_run=dry_run, language=self.language, command_name="lint")

    def typecheck(self, cwd: str, dry_run: bool = False) -> ExecutionResult:
        missing = self.require_tool("dotnet", "typecheck", INSTALL_DOTNET_GUIDE)
        if missing:
            return missing
        return execute_command(["dotnet", "build", "--no-incremental"], cwd=cwd, dry_run=dry_run, language=self.language, command_name="typecheck")

    def build(self, cwd: str, dry_run: bool = False) -> ExecutionResult:
        missing = self.require_tool("dotnet", "build", INSTALL_DOTNET_GUIDE)
        if missing:
            return missing
        return execute_command(["dotnet", "build", "-c", "Release"], cwd=cwd, dry_run=dry_run, language=self.language, command_name="build")

    def test(self, cwd: str, dry_run: bool = False, filter_name: Optional[str] = None) -> ExecutionResult:
        missing = self.require_tool("dotnet", "test", INSTALL_DOTNET_GUIDE)
        if missing:
            return missing
        cmd = ["dotnet", "test"]
        if filter_name:
            cmd.extend(["--filter", filter_name])
        return execute_command(cmd, cwd=cwd, dry_run=dry_run, language=self.language, command_name="test")

    def audit(self, cwd: str, dry_run: bool = False) -> ExecutionResult:
        missing = self.require_tool("dotnet", "audit", INSTALL_DOTNET_GUIDE)
        if missing:
            return missing
        return execute_command(["dotnet", "list", "package", "--vulnerable"], cwd=cwd, dry_run=dry_run, language=self.language, command_name="audit")

    def benchmark(self, cwd: str, dry_run: bool = False) -> ExecutionResult:
        missing = self.require_tool("dotnet", "benchmark", INSTALL_DOTNET_GUIDE)
        if missing:
            return missing
        return execute_command(["dotnet", "run", "-c", "Release", "--", "--filter", "*Benchmark*"], cwd=cwd, dry_run=dry_run, language=self.language, command_name="benchmark")
