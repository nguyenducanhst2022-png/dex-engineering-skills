# -*- coding: utf-8 -*-
"""
DEX Polyglot Script Engine — Result Schema & Contract
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
import json

@dataclass
class ExecutionResult:
    command: str
    status: str  # "SUCCESS", "FAILED", "TOOL_NOT_AVAILABLE", "SKIPPED", "DRY_RUN"
    exit_code: int
    duration_ms: float
    schema_version: str = "1.0.0"
    language: Optional[str] = None
    commands_executed: List[str] = field(default_factory=list)
    evidence: Dict[str, Any] = field(default_factory=dict)
    stdout: str = ""
    stderr: str = ""
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ExecutionResult":
        return cls(**data)

    @classmethod
    def tool_not_available(
        cls,
        command: str,
        language: str,
        tool_name: str,
        install_guide: str,
        warnings: Optional[List[str]] = None
    ) -> "ExecutionResult":
        warns = warnings or []
        warns.append(f"Tool '{tool_name}' not available on host. {install_guide}")
        return cls(
            command=command,
            language=language,
            status="TOOL_NOT_AVAILABLE",
            exit_code=127,
            duration_ms=0.0,
            commands_executed=[],
            evidence={"tool_name": tool_name, "install_guide": install_guide},
            warnings=warns,
            errors=[f"Required toolchain '{tool_name}' is not installed or not in PATH."]
        )

    @classmethod
    def dry_run(
        cls,
        command: str,
        language: Optional[str],
        commands_to_execute: List[str],
        cwd: str,
        evidence: Optional[Dict[str, Any]] = None
    ) -> "ExecutionResult":
        ev = evidence or {}
        ev["dry_run"] = True
        ev["planned_cwd"] = cwd
        ev["planned_commands"] = commands_to_execute
        return cls(
            command=command,
            language=language,
            status="DRY_RUN",
            exit_code=0,
            duration_ms=0.0,
            commands_executed=commands_to_execute,
            evidence=ev,
            stdout="[DRY-RUN] No commands executed.",
            stderr="",
            warnings=["Execution skipped due to dry-run flag."]
        )
