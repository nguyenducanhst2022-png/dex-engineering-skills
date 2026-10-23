# -*- coding: utf-8 -*-
"""
DEX Polyglot Script Engine — Java Adapter
"""

import os
from pathlib import Path
from typing import Optional
from .base import BaseAdapter
from ..core.result_schema import ExecutionResult
from ..core.executor import execute_command
from ..core.detector import probe_tool

INSTALL_JAVA_GUIDE = "Install OpenJDK (Temurin 17/21) and Maven/Gradle: https://adoptium.net / https://maven.apache.org"

class JavaAdapter(BaseAdapter):
    def __init__(self):
        super().__init__(
            language="java",
            display_name="Java (Maven / Gradle)",
            primary_tools=["mvn", "gradle", "javac", "java"]
        )

    def _get_build_tool(self, cwd: str) -> str:
        p = Path(cwd).resolve()
        if (p / "gradlew").exists() or (p / "gradlew.bat").exists() or (p / "build.gradle").exists():
            return "gradle"
        return "mvn"

    def lint(self, cwd: str, dry_run: bool = False) -> ExecutionResult:
        tool = self._get_build_tool(cwd)
        missing = self.require_tool(tool, "lint", INSTALL_JAVA_GUIDE)
        if missing:
            return missing
        if tool == "gradle":
            return execute_command(["gradle", "checkstyleMain"], cwd=cwd, dry_run=dry_run, language=self.language, command_name="lint")
        return execute_command(["mvn", "checkstyle:check"], cwd=cwd, dry_run=dry_run, language=self.language, command_name="lint")

    def typecheck(self, cwd: str, dry_run: bool = False) -> ExecutionResult:
        tool = self._get_build_tool(cwd)
        missing = self.require_tool(tool, "typecheck", INSTALL_JAVA_GUIDE)
        if missing:
            return missing
        if tool == "gradle":
            return execute_command(["gradle", "compileJava"], cwd=cwd, dry_run=dry_run, language=self.language, command_name="typecheck")
        return execute_command(["mvn", "compile"], cwd=cwd, dry_run=dry_run, language=self.language, command_name="typecheck")

    def build(self, cwd: str, dry_run: bool = False) -> ExecutionResult:
        tool = self._get_build_tool(cwd)
        missing = self.require_tool(tool, "build", INSTALL_JAVA_GUIDE)
        if missing:
            return missing
        if tool == "gradle":
            return execute_command(["gradle", "build", "-x", "test"], cwd=cwd, dry_run=dry_run, language=self.language, command_name="build")
        return execute_command(["mvn", "package", "-DskipTests"], cwd=cwd, dry_run=dry_run, language=self.language, command_name="build")

    def test(self, cwd: str, dry_run: bool = False, filter_name: Optional[str] = None) -> ExecutionResult:
        tool = self._get_build_tool(cwd)
        missing = self.require_tool(tool, "test", INSTALL_JAVA_GUIDE)
        if missing:
            return missing
        if tool == "gradle":
            cmd = ["gradle", "test"]
            if filter_name:
                cmd.extend(["--tests", filter_name])
            return execute_command(cmd, cwd=cwd, dry_run=dry_run, language=self.language, command_name="test")
        else:
            cmd = ["mvn", "test"]
            if filter_name:
                cmd.append(f"-Dtest={filter_name}")
            return execute_command(cmd, cwd=cwd, dry_run=dry_run, language=self.language, command_name="test")

    def audit(self, cwd: str, dry_run: bool = False) -> ExecutionResult:
        tool = self._get_build_tool(cwd)
        missing = self.require_tool(tool, "audit", INSTALL_JAVA_GUIDE)
        if missing:
            return missing
        if tool == "gradle":
            return execute_command(["gradle", "dependencyCheckAnalyze"], cwd=cwd, dry_run=dry_run, language=self.language, command_name="audit")
        return execute_command(["mvn", "dependency-check:check"], cwd=cwd, dry_run=dry_run, language=self.language, command_name="audit")

    def benchmark(self, cwd: str, dry_run: bool = False) -> ExecutionResult:
        tool = self._get_build_tool(cwd)
        missing = self.require_tool(tool, "benchmark", INSTALL_JAVA_GUIDE)
        if missing:
            return missing
        if tool == "gradle":
            return execute_command(["gradle", "jmh"], cwd=cwd, dry_run=dry_run, language=self.language, command_name="benchmark")
        return execute_command(["mvn", "clean", "package", "exec:exec"], cwd=cwd, dry_run=dry_run, language=self.language, command_name="benchmark")
