# -*- coding: utf-8 -*-
"""
DEX Polyglot Script Engine — C++ Adapter
"""

import os
from typing import Optional
from .base import BaseAdapter
from ..core.result_schema import ExecutionResult
from ..core.executor import execute_command
from ..core.detector import probe_tool

INSTALL_CPP_GUIDE = "Install CMake and a C++ compiler: MSVC on Windows (Visual Studio Build Tools), GCC/Clang on Linux/macOS."

class CppAdapter(BaseAdapter):
    def __init__(self):
        super().__init__(
            language="cpp",
            display_name="C++ (CMake)",
            primary_tools=["cmake", "ninja", "make", "clang++", "g++"]
        )

    def lint(self, cwd: str, dry_run: bool = False) -> ExecutionResult:
        if probe_tool("clang-tidy")["available"]:
            return execute_command(["clang-tidy", "**/*.cpp", "--"], cwd=cwd, dry_run=dry_run, language=self.language, command_name="lint")
        else:
            missing = self.require_tool("cmake", "lint", INSTALL_CPP_GUIDE)
            if missing:
                return missing
            return execute_command(["cmake", "-S", ".", "-B", "build", "-Wdev"], cwd=cwd, dry_run=dry_run, language=self.language, command_name="lint")

    def typecheck(self, cwd: str, dry_run: bool = False) -> ExecutionResult:
        # C++ typecheck is performed during compilation check
        missing = self.require_tool("cmake", "typecheck", INSTALL_CPP_GUIDE)
        if missing:
            return missing
        return execute_command(["cmake", "-S", ".", "-B", "build"], cwd=cwd, dry_run=dry_run, language=self.language, command_name="typecheck")

    def build(self, cwd: str, dry_run: bool = False) -> ExecutionResult:
        missing = self.require_tool("cmake", "build", INSTALL_CPP_GUIDE)
        if missing:
            return missing
        # Generate & build
        return execute_command(["cmake", "--build", "build", "--config", "Release"], cwd=cwd, dry_run=dry_run, language=self.language, command_name="build")

    def test(self, cwd: str, dry_run: bool = False, filter_name: Optional[str] = None) -> ExecutionResult:
        missing = self.require_tool("ctest", "test", INSTALL_CPP_GUIDE)
        if missing:
            return missing
        cmd = ["ctest", "--test-dir", "build", "--output-on-failure"]
        if filter_name:
            cmd.extend(["-R", filter_name])
        return execute_command(cmd, cwd=cwd, dry_run=dry_run, language=self.language, command_name="test")

    def audit(self, cwd: str, dry_run: bool = False) -> ExecutionResult:
        if probe_tool("cppcheck")["available"]:
            return execute_command(["cppcheck", "--enable=all", "."], cwd=cwd, dry_run=dry_run, language=self.language, command_name="audit")
        else:
            return self.require_tool("cppcheck", "audit", "Install cppcheck via: winget install Cppcheck.Cppcheck / brew install cppcheck")

    def benchmark(self, cwd: str, dry_run: bool = False) -> ExecutionResult:
        missing = self.require_tool("ctest", "benchmark", INSTALL_CPP_GUIDE)
        if missing:
            return missing
        return execute_command(["ctest", "--test-dir", "build", "-L", "benchmark"], cwd=cwd, dry_run=dry_run, language=self.language, command_name="benchmark")
