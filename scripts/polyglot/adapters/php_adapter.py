# -*- coding: utf-8 -*-
"""
DEX Polyglot Script Engine — PHP Adapter
"""

from typing import Optional
from .base import BaseAdapter
from ..core.result_schema import ExecutionResult
from ..core.executor import execute_command
from ..core.detector import probe_tool

INSTALL_PHP_GUIDE = "Install PHP 8.x and Composer: https://www.php.net / https://getcomposer.org (or winget install PHP.PHP / brew install php composer)"

class PhpAdapter(BaseAdapter):
    def __init__(self):
        super().__init__(
            language="php",
            display_name="PHP",
            primary_tools=["php", "composer", "phpunit", "phpstan"]
        )

    def lint(self, cwd: str, dry_run: bool = False) -> ExecutionResult:
        if probe_tool("phpstan")["available"]:
            return execute_command(["phpstan", "analyse"], cwd=cwd, dry_run=dry_run, language=self.language, command_name="lint")
        else:
            missing = self.require_tool("php", "lint", INSTALL_PHP_GUIDE)
            if missing:
                return missing
            return execute_command(
                ["php", "-l", "src/"],
                cwd=cwd,
                dry_run=dry_run,
                language=self.language,
                command_name="lint",
                evidence={"strategy": "php -l syntax lint"}
            )

    def typecheck(self, cwd: str, dry_run: bool = False) -> ExecutionResult:
        if probe_tool("phpstan")["available"]:
            return execute_command(["phpstan", "analyse", "--level=max"], cwd=cwd, dry_run=dry_run, language=self.language, command_name="typecheck")
        else:
            return self.require_tool("phpstan", "typecheck", INSTALL_PHP_GUIDE + " then 'composer require --dev phpstan/phpstan'")

    def build(self, cwd: str, dry_run: bool = False) -> ExecutionResult:
        missing = self.require_tool("composer", "build", INSTALL_PHP_GUIDE)
        if missing:
            return missing
        return execute_command(["composer", "install", "--no-dev", "--optimize-autoloader"], cwd=cwd, dry_run=dry_run, language=self.language, command_name="build")

    def test(self, cwd: str, dry_run: bool = False, filter_name: Optional[str] = None) -> ExecutionResult:
        missing = self.require_tool("composer", "test", INSTALL_PHP_GUIDE)
        if missing:
            return missing
        cmd = ["composer", "test"]
        if filter_name:
            cmd.extend(["--", "--filter", filter_name])
        return execute_command(cmd, cwd=cwd, dry_run=dry_run, language=self.language, command_name="test")

    def audit(self, cwd: str, dry_run: bool = False) -> ExecutionResult:
        missing = self.require_tool("composer", "audit", INSTALL_PHP_GUIDE)
        if missing:
            return missing
        return execute_command(["composer", "audit"], cwd=cwd, dry_run=dry_run, language=self.language, command_name="audit")

    def benchmark(self, cwd: str, dry_run: bool = False) -> ExecutionResult:
        missing = self.require_tool("composer", "benchmark", INSTALL_PHP_GUIDE)
        if missing:
            return missing
        return execute_command(["composer", "run", "benchmark"], cwd=cwd, dry_run=dry_run, language=self.language, command_name="benchmark")
