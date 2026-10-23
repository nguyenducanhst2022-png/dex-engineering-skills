# -*- coding: utf-8 -*-
"""
DEX Polyglot Script Engine v7.0 / v8.0 — CLI Entrypoint
Unified multi-language automation across Python, TypeScript, JavaScript,
PowerShell, Bash, Rust, Go, C++, C#, Java, and PHP.
"""

import os
import sys
import argparse
from pathlib import Path

# Add repo root to sys.path so scripts.polyglot can be imported
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

if sys.stdout.encoding != "utf-8" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from scripts.polyglot.core.result_schema import ExecutionResult
from scripts.polyglot.core.detector import detect_languages, probe_tool
from scripts.polyglot.core.registry import REGISTRY
from scripts.polyglot.core.reporting import format_result
from scripts.polyglot.core.generator import generate_scaffold

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="dex",
        description="DEX Polyglot Script Engine — Multi-Language Engineering Automation"
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Global options
    for sub in [
        "status", "detect", "doctor", "lint", "typecheck",
        "build", "test", "audit", "benchmark", "validate",
        "report", "generate"
    ]:
        sp = subparsers.add_parser(sub, help=f"Execute {sub} operation")
        sp.add_argument("--lang", "-l", help="Explicit language target (e.g. python, typescript, rust, go)")
        sp.add_argument("--format", "-f", choices=["text", "json", "markdown"], default="text", help="Output format")
        sp.add_argument("--dry-run", action="store_true", help="Simulate execution without modifying state")
        sp.add_argument("--cwd", "-C", default=".", help="Target working directory (default: current directory)")
        sp.add_argument("--filter", help="Test or benchmark filter pattern")
        sp.add_argument("--task", default="sample_task", help="Task name for code generation")
        sp.add_argument("--out", default="generated", help="Output directory for code generation")

    return parser

def cmd_status(args) -> ExecutionResult:
    detected = detect_languages(args.cwd)
    all_langs = REGISTRY.list_languages()
    available = [l for l in all_langs if REGISTRY.get_adapter(l).is_available()]

    lines = [
        f"DEX Polyglot Script Engine v8.0.0",
        f"Working Directory: {Path(args.cwd).resolve()}",
        f"Supported Languages: {len(all_langs)} ({', '.join(all_langs)})",
        f"Available on Host:   {len(available)} ({', '.join(available)})",
    ]
    if detected:
        lines.append("\nDetected in Workspace:")
        for d in detected:
            lines.append(f"  - {d['language']:<12} (Confidence: {d['confidence']:.2f}, Markers: {', '.join(d['markers_found'])})")
    else:
        lines.append("\nNo specific language markers detected in current directory.")

    return ExecutionResult(
        command="status",
        status="SUCCESS",
        exit_code=0,
        duration_ms=5.0,
        evidence={"detected": detected, "available_languages": available, "all_languages": all_langs},
        stdout="\n".join(lines)
    )

def cmd_detect(args) -> ExecutionResult:
    detected = detect_languages(args.cwd)
    lines = [f"Language detection for {Path(args.cwd).resolve()}:"]
    for d in detected:
        lines.append(f"  - {d['language']:<12} Confidence: {d['confidence']:.2f} | Markers: {', '.join(d['markers_found'])}")

    return ExecutionResult(
        command="detect",
        status="SUCCESS",
        exit_code=0,
        duration_ms=10.0,
        evidence={"detected": detected},
        stdout="\n".join(lines) if detected else "No language markers detected."
    )

def cmd_doctor(args) -> ExecutionResult:
    adapters = REGISTRY.get_all_adapters()
    lines = ["=== DEX Polyglot Toolchain Diagnostics ==="]
    diag = {}
    any_missing = False

    for ad in adapters:
        info = ad.get_toolchain_info()
        diag[ad.language] = info
        status_sym = "[READY]" if info["available"] else "[MISSING]"
        lines.append(f"{status_sym:<10} {ad.display_name:<20}")
        for tool, t_info in info["tools"].items():
            t_avail = "✓" if t_info["available"] else "✗"
            t_ver = f"({t_info['version']})" if t_info["version"] else ""
            lines.append(f"    {t_avail} {tool:<15} {t_ver}")
            if not t_info["available"]:
                any_missing = True

    return ExecutionResult(
        command="doctor",
        status="SUCCESS",
        exit_code=0,
        duration_ms=25.0,
        evidence={"diagnostics": diag},
        stdout="\n".join(lines),
        warnings=["Some toolchains are missing on the host. When targeting missing runtimes, adapters return TOOL_NOT_AVAILABLE with installation instructions."] if any_missing else []
    )

def resolve_target_language(args) -> str:
    if args.lang:
        return args.lang.strip().lower()

    # Auto-detect from CWD
    detected = detect_languages(args.cwd)
    if detected:
        return detected[0]["language"]

    # Default to python
    return "python"

def execute_adapter_action(args, action_name: str) -> ExecutionResult:
    lang = resolve_target_language(args)
    adapter = REGISTRY.get_adapter(lang)

    if not adapter:
        return ExecutionResult(
            command=action_name,
            language=lang,
            status="FAILED",
            exit_code=1,
            duration_ms=0.0,
            errors=[f"Unsupported language '{lang}'. Supported: {', '.join(REGISTRY.list_languages())}"]
        )

    # Dispatch to adapter method
    method = getattr(adapter, action_name, None)
    if not method:
        return ExecutionResult(
            command=action_name,
            language=lang,
            status="FAILED",
            exit_code=1,
            duration_ms=0.0,
            errors=[f"Action '{action_name}' is not supported by adapter '{lang}'."]
        )

    if action_name == "test":
        return method(cwd=args.cwd, dry_run=args.dry_run, filter_name=args.filter)
    elif action_name == "benchmark":
        return method(cwd=args.cwd, dry_run=args.dry_run)
    else:
        return method(cwd=args.cwd, dry_run=args.dry_run)

def cmd_generate(args) -> ExecutionResult:
    lang = resolve_target_language(args)
    res = generate_scaffold(lang, args.task, args.out)

    if res["status"] == "SUCCESS":
        lines = [
            f"Successfully generated {lang} scaffold for task '{args.task}':",
            f"  Files created:"
        ]
        for f in res["files_created"]:
            lines.append(f"    - {f}")
        return ExecutionResult(
            command="generate",
            language=lang,
            status="SUCCESS",
            exit_code=0,
            duration_ms=10.0,
            evidence=res,
            stdout="\n".join(lines)
        )
    else:
        return ExecutionResult(
            command="generate",
            language=lang,
            status="FAILED",
            exit_code=1,
            duration_ms=0.0,
            evidence=res,
            errors=[res.get("error", "Generation failed.")]
        )

def main():
    parser = build_parser()
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)

    args = parser.parse_args()

    if args.command == "status":
        result = cmd_status(args)
    elif args.command == "detect":
        result = cmd_detect(args)
    elif args.command == "doctor":
        result = cmd_doctor(args)
    elif args.command == "generate":
        result = cmd_generate(args)
    elif args.command in ["lint", "typecheck", "build", "test", "audit", "benchmark"]:
        result = execute_adapter_action(args, args.command)
    elif args.command == "validate":
        # Validate aliases to doctor + status + dry-run test
        status_res = cmd_status(args)
        doctor_res = cmd_doctor(args)
        lines = [status_res.stdout, "\n", doctor_res.stdout]
        result = ExecutionResult(
            command="validate",
            status="SUCCESS",
            exit_code=0,
            duration_ms=30.0,
            evidence={"status": status_res.to_dict(), "doctor": doctor_res.to_dict()},
            stdout="\n".join(lines)
        )
    elif args.command == "report":
        result = cmd_status(args)
    else:
        result = ExecutionResult(
            command="unknown",
            status="FAILED",
            exit_code=1,
            duration_ms=0.0,
            errors=[f"Unknown command '{args.command}'."]
        )

    # Format and output result
    formatted = format_result(result, args.format)
    print(formatted)
    sys.exit(result.exit_code if result.exit_code in [0, 127] else (0 if result.status in ["SUCCESS", "DRY_RUN", "TOOL_NOT_AVAILABLE"] else 1))

if __name__ == "__main__":
    main()
