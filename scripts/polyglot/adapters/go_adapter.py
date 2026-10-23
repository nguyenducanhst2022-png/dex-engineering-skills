# -*- coding: utf-8 -*-
"""
DEX Polyglot Script Engine — Go Adapter
"""

import os
from typing import Optional
from .base import BaseAdapter
from ..core.result_schema import ExecutionResult
from ..core.executor import execute_command

INSTALL_GO_GUIDE = "Install Go toolchain from https://go.dev/dl/ (or winget install GoLang.Go / brew install go)"

class GoAdapter(BaseAdapter):
    def __init__(self):
        super().__init__(
            language="go",
            display_name="Go",
            primary_tools=["go", "golangci-lint", "gofmt"]
        )

    def lint(self, cwd: str, dry_run: bool = False) -> ExecutionResult:
        missing = self.require_tool("go", "lint", INSTALL_GO_GUIDE)
        if missing:
            return missing
        return execute_command(["go", "vet", "./..."], cwd=cwd, dry_run=dry_run, language=self.language, command_name="lint")

    def typecheck(self, cwd: str, dry_run: bool = False) -> ExecutionResult:
        missing = self.require_tool("go", "typecheck", INSTALL_GO_GUIDE)
        if missing:
            return missing
        return execute_command(["go", "build", "-v", "-o", os.devnull if hasattr(os, "devnull") else "NUL", "./..."], cwd=cwd, dry_run=dry_run, language=self.language, command_name="typecheck")

    def build(self, cwd: str, dry_run: bool = False) -> ExecutionResult:
        missing = self.require_tool("go", "build", INSTALL_GO_GUIDE)
        if missing:
            return missing
        return execute_command(["go", "build", "./..."], cwd=cwd, dry_run=dry_run, language=self.language, command_name="build")

    def test(self, cwd: str, dry_run: bool = False, filter_name: Optional[str] = None) -> ExecutionResult:
        missing = self.require_tool("go", "test", INSTALL_GO_GUIDE)
        if missing:
            return missing
        cmd = ["go", "test", "-v"]
        if filter_name:
            cmd.extend(["-run", filter_name])
        cmd.append("./...")
        return execute_command(cmd, cwd=cwd, dry_run=dry_run, language=self.language, command_name="test")

    def audit(self, cwd: str, dry_run: bool = False) -> ExecutionResult:
        missing = self.require_tool("go", "audit", INSTALL_GO_GUIDE + " then 'go install golang.org/x/vuln/cmd/govulncheck@latest'")
        if missing:
            return missing
        return execute_command(["govulncheck", "./..."], cwd=cwd, dry_run=dry_run, language=self.language, command_name="audit")

    def benchmark(self, cwd: str, dry_run: bool = False) -> ExecutionResult:
        missing = self.require_tool("go", "benchmark", INSTALL_GO_GUIDE)
        if missing:
            return missing
        return execute_command(["go", "test", "-bench=.", "./..."], cwd=cwd, dry_run=dry_run, language=self.language, command_name="benchmark")
