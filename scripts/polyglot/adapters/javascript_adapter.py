# -*- coding: utf-8 -*-
"""
DEX Polyglot Script Engine — JavaScript Adapter
"""

from typing import Optional
from .base import BaseAdapter
from ..core.result_schema import ExecutionResult
from ..core.executor import execute_command
from ..core.detector import probe_tool

class JavaScriptAdapter(BaseAdapter):
    def __init__(self):
        super().__init__(
            language="javascript",
            display_name="JavaScript (Node.js)",
            primary_tools=["node", "npm", "npx", "yarn", "pnpm"]
        )

    def lint(self, cwd: str, dry_run: bool = False) -> ExecutionResult:
        missing = self.require_tool("npx", "lint", "Install Node.js from https://nodejs.org")
        if missing:
            return missing
        return execute_command(["npx", "eslint", "."], cwd=cwd, dry_run=dry_run, language=self.language, command_name="lint")

    def typecheck(self, cwd: str, dry_run: bool = False) -> ExecutionResult:
        # JS can use jsdoc typechecking via tsc or skip
        missing = self.require_tool("npx", "typecheck", "Install Node.js from https://nodejs.org")
        if missing:
            return missing
        return execute_command(["npx", "tsc", "--allowJs", "--checkJs", "--noEmit"], cwd=cwd, dry_run=dry_run, language=self.language, command_name="typecheck")

    def build(self, cwd: str, dry_run: bool = False) -> ExecutionResult:
        missing = self.require_tool("npm", "build", "Install Node.js from https://nodejs.org")
        if missing:
            return missing
        return execute_command(["npm", "run", "build"], cwd=cwd, dry_run=dry_run, language=self.language, command_name="build")

    def test(self, cwd: str, dry_run: bool = False, filter_name: Optional[str] = None) -> ExecutionResult:
        missing = self.require_tool("npm", "test", "Install Node.js from https://nodejs.org")
        if missing:
            return missing
        cmd = ["npm", "test"]
        if filter_name:
            cmd.extend(["--", filter_name])
        return execute_command(cmd, cwd=cwd, dry_run=dry_run, language=self.language, command_name="test")

    def audit(self, cwd: str, dry_run: bool = False) -> ExecutionResult:
        missing = self.require_tool("npm", "audit", "Install Node.js from https://nodejs.org")
        if missing:
            return missing
        return execute_command(["npm", "audit"], cwd=cwd, dry_run=dry_run, language=self.language, command_name="audit")

    def benchmark(self, cwd: str, dry_run: bool = False) -> ExecutionResult:
        missing = self.require_tool("npm", "benchmark", "Install Node.js from https://nodejs.org")
        if missing:
            return missing
        return execute_command(["npm", "run", "benchmark"], cwd=cwd, dry_run=dry_run, language=self.language, command_name="benchmark")
