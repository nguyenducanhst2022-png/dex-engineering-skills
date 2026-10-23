# -*- coding: utf-8 -*-
"""
DEX Polyglot Script Engine — Reporting Subsystem
Formats ExecutionResult into Terminal text, JSON, or Markdown tables.
"""

from .result_schema import ExecutionResult

def format_result(result: ExecutionResult, output_format: str = "text") -> str:
    """Format an ExecutionResult into the specified format: text, json, or markdown."""
    fmt = output_format.lower()

    if fmt == "json":
        return result.to_json(indent=2)

    if fmt == "markdown":
        md = []
        status_badge = "✅ SUCCESS" if result.status == "SUCCESS" else (
            "⚠️ DRY-RUN" if result.status == "DRY_RUN" else (
                "🟡 NOT AVAILABLE" if result.status == "TOOL_NOT_AVAILABLE" else "❌ FAILED"
            )
        )
        md.append(f"### DEX Polyglot Execution: `{result.command}`")
        md.append(f"- **Status:** {status_badge}")
        md.append(f"- **Language:** `{result.language or 'auto'}`")
        md.append(f"- **Exit Code:** `{result.exit_code}`")
        md.append(f"- **Duration:** `{result.duration_ms} ms`")
        md.append(f"- **Timestamp:** `{result.timestamp}`\n")

        if result.commands_executed:
            md.append("**Commands Executed:**")
            for c in result.commands_executed:
                md.append(f"```bash\n{c}\n```")

        if result.warnings:
            md.append("**Warnings:**")
            for w in result.warnings:
                md.append(f"- ⚠️ {w}")

        if result.errors:
            md.append("**Errors:**")
            for e in result.errors:
                md.append(f"- ❌ {e}")

        if result.stdout.strip():
            md.append("<details><summary>Standard Output (stdout)</summary>\n")
            md.append(f"```text\n{result.stdout.strip()}\n```\n</details>")

        if result.stderr.strip():
            md.append("<details><summary>Standard Error (stderr)</summary>\n")
            md.append(f"```text\n{result.stderr.strip()}\n```\n</details>")

        return "\n".join(md)

    # Default to text format for CLI
    lines = []
    lines.append(f"==> [{result.status}] Command: {result.command} (Lang: {result.language or 'auto'}, Exit: {result.exit_code}, Time: {result.duration_ms}ms)")

    if result.commands_executed:
        for c in result.commands_executed:
            lines.append(f"    CMD: {c}")

    if result.warnings:
        for w in result.warnings:
            lines.append(f"    WARN: {w}")

    if result.errors:
        for e in result.errors:
            lines.append(f"    ERROR: {e}")

    if result.stdout.strip():
        lines.append("--- stdout ---")
        lines.append(result.stdout.strip())

    if result.stderr.strip():
        lines.append("--- stderr ---")
        lines.append(result.stderr.strip())

    return "\n".join(lines)
