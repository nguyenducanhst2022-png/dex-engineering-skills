# -*- coding: utf-8 -*-
"""
DEX Polyglot Script Engine — Base Language Adapter
Defines standard lifecycle operations: lint, typecheck, build, test, audit, benchmark.
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict, Any, List
from ..core.result_schema import ExecutionResult
from ..core.detector import probe_tool
from ..core.executor import execute_command

class BaseAdapter(ABC):
    """Abstract base class for all language adapters in the Polyglot Script Engine."""

    def __init__(self, language: str, display_name: str, primary_tools: List[str]):
        self.language = language
        self.display_name = display_name
        self.primary_tools = primary_tools

    def is_available(self) -> bool:
        """Check if any primary tool for this language is available on the host system."""
        for tool in self.primary_tools:
            info = probe_tool(tool)
            if info["available"]:
                return True
        return False

    def get_toolchain_info(self) -> Dict[str, Any]:
        """Query host status for all tools associated with this language."""
        tools_status = {}
        any_avail = False
        for tool in self.primary_tools:
            info = probe_tool(tool)
            tools_status[tool] = info
            if info["available"]:
                any_avail = True

        return {
            "language": self.language,
            "display_name": self.display_name,
            "available": any_avail,
            "tools": tools_status,
        }

    def require_tool(self, tool_name: str, command: str, install_guide: str) -> Optional[ExecutionResult]:
        """Helper to return standardized TOOL_NOT_AVAILABLE ExecutionResult if tool is missing."""
        info = probe_tool(tool_name)
        if not info["available"]:
            return ExecutionResult.tool_not_available(
                command=command,
                language=self.language,
                tool_name=tool_name,
                install_guide=install_guide
            )
        return None

    @abstractmethod
    def lint(self, cwd: str, dry_run: bool = False) -> ExecutionResult:
        pass

    @abstractmethod
    def typecheck(self, cwd: str, dry_run: bool = False) -> ExecutionResult:
        pass

    @abstractmethod
    def build(self, cwd: str, dry_run: bool = False) -> ExecutionResult:
        pass

    @abstractmethod
    def test(self, cwd: str, dry_run: bool = False, filter_name: Optional[str] = None) -> ExecutionResult:
        pass

    @abstractmethod
    def audit(self, cwd: str, dry_run: bool = False) -> ExecutionResult:
        pass

    @abstractmethod
    def benchmark(self, cwd: str, dry_run: bool = False) -> ExecutionResult:
        pass
