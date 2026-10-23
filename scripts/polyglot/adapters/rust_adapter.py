# -*- coding: utf-8 -*-
"""
DEX Polyglot Script Engine — Rust Adapter
"""

from typing import Optional
from .base import BaseAdapter
from ..core.result_schema import ExecutionResult
from ..core.executor import execute_command

INSTALL_RUST_GUIDE = "Install Rust & Cargo via rustup: https://rustup.rs (or winget install Rustlang.Rustup / brew install rust)"

class RustAdapter(BaseAdapter):
    def __init__(self):
        super().__init__(
            language="rust",
            display_name="Rust",
            primary_tools=["cargo", "rustc", "rustfmt", "clippy"]
        )

    def lint(self, cwd: str, dry_run: bool = False) -> ExecutionResult:
        missing = self.require_tool("cargo", "lint", INSTALL_RUST_GUIDE)
        if missing:
            return missing
        return execute_command(["cargo", "clippy", "--", "-D", "warnings"], cwd=cwd, dry_run=dry_run, language=self.language, command_name="lint")

    def typecheck(self, cwd: str, dry_run: bool = False) -> ExecutionResult:
        missing = self.require_tool("cargo", "typecheck", INSTALL_RUST_GUIDE)
        if missing:
            return missing
        return execute_command(["cargo", "check"], cwd=cwd, dry_run=dry_run, language=self.language, command_name="typecheck")

    def build(self, cwd: str, dry_run: bool = False) -> ExecutionResult:
        missing = self.require_tool("cargo", "build", INSTALL_RUST_GUIDE)
        if missing:
            return missing
        return execute_command(["cargo", "build", "--release"], cwd=cwd, dry_run=dry_run, language=self.language, command_name="build")

    def test(self, cwd: str, dry_run: bool = False, filter_name: Optional[str] = None) -> ExecutionResult:
        missing = self.require_tool("cargo", "test", INSTALL_RUST_GUIDE)
        if missing:
            return missing
        cmd = ["cargo", "test"]
        if filter_name:
            cmd.extend(["--", filter_name])
        return execute_command(cmd, cwd=cwd, dry_run=dry_run, language=self.language, command_name="test")

    def audit(self, cwd: str, dry_run: bool = False) -> ExecutionResult:
        missing = self.require_tool("cargo", "audit", INSTALL_RUST_GUIDE + " then 'cargo install cargo-audit'")
        if missing:
            return missing
        return execute_command(["cargo", "audit"], cwd=cwd, dry_run=dry_run, language=self.language, command_name="audit")

    def benchmark(self, cwd: str, dry_run: bool = False) -> ExecutionResult:
        missing = self.require_tool("cargo", "benchmark", INSTALL_RUST_GUIDE)
        if missing:
            return missing
        return execute_command(["cargo", "bench"], cwd=cwd, dry_run=dry_run, language=self.language, command_name="benchmark")
