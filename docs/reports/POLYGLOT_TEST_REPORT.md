# DEX Engineering Skills Framework v8.0 — Polyglot Script Engine Test Report

> **Audit Date:** 2026-10-23  
> **Framework Subsystem:** `scripts/polyglot/` (v8.0.0)  
> **Status:** 100% PASSED (37 / 37 Pytest Tests)

---

## 1. Subsystem Architecture & Capabilities

The **DEX Polyglot Script Engine** enables coding agents to execute builds, run tests, perform typechecks, enforce linting, audit code, and generate scaffoldings across 11 programming languages:

| Language | Primary Tools | Available on Host | Missing Toolchain Fallback Status |
|:---|:---|:---:|:---|
| **Python** | python, pytest, ruff, mypy | **YES** (`Python 3.12.10`, `pytest 8.4.2`) | N/A (Available) |
| **TypeScript** | node, npm, npx, tsc | **YES** (`Node v24.22.0`, `npm 11.19.1`) | N/A (Available) |
| **JavaScript** | node, npm, npx | **YES** (`Node v24.22.0`, `npm 11.19.1`) | N/A (Available) |
| **PowerShell** | powershell 5.1 / pwsh | **YES** (`powershell.exe`) | N/A (Available) |
| **C++ (CMake)** | cmake, ninja, clang | **YES** (`CMake 4.5.0-rc1`) | N/A (Available) |
| **Bash / POSIX** | bash, sh, bats | NO | Graceful `TOOL_NOT_AVAILABLE` (Exit 127) |
| **Rust** | cargo, rustc, clippy | NO | Graceful `TOOL_NOT_AVAILABLE` (Exit 127) |
| **Go** | go, gofmt, golangci-lint | NO | Graceful `TOOL_NOT_AVAILABLE` (Exit 127) |
| **C# (.NET)** | dotnet | NO | Graceful `TOOL_NOT_AVAILABLE` (Exit 127) |
| **Java** | javac, java, mvn, gradle | NO | Graceful `TOOL_NOT_AVAILABLE` (Exit 127) |
| **PHP** | php, composer, phpunit | NO | Graceful `TOOL_NOT_AVAILABLE` (Exit 127) |

---

## 2. Safety & Security Guardrails

The Polyglot Engine enforces multi-layer isolation:
1. **Subprocess Isolation**: Strictly uses `subprocess.run(shell=False)` with argument lists; zero raw shell string interpolation.
2. **Path Traversal Defense**: All input paths are validated against directory roots; path traversal attempts (e.g. `../../etc/passwd`) raise `PermissionError`.
3. **Secret Scrubbing**: Output streams are continuously filtered against common secret patterns (API keys, tokens, Bearer headers, SSH keys).
4. **Output Bounds**: STDOUT and STDERR streams are capped at 512KB with clear truncation flags.
5. **Execution Timeouts**: Every subprocess is bound by a configurable timeout (default 60s); runaway processes are terminated automatically.
6. **Destructive Command Blocking**: Commands matching dangerous patterns (`rm -rf /`, `mkfs`, `:(){ :|:& };:`, `drop database`) are rejected before execution.

---

## 3. Pytest Polyglot Test Suite Results

Command: `pytest scripts/polyglot/tests/ -v`

| Test Module | Coverage Area | Tests Run | Result |
|:---|:---|:---:|:---:|
| `test_result_schema.py` | JSON serialization, deserialization, envelope conformance | 3 | **PASS** |
| `test_security.py` | Secret redaction, path traversal checks, command blocking | 6 | **PASS** |
| `test_executor.py` | Subprocess execution, timeouts, output truncation, Windows `.cmd` resolution | 5 | **PASS** |
| `test_detector.py` | 11-language scanning, markers detection, confidence scoring | 13 | **PASS** |
| `test_adapters.py` | Base adapter dry-runs, toolchain absence returns `TOOL_NOT_AVAILABLE` | 5 | **PASS** |
| `test_cli.py` | CLI commands (`status`, `doctor`, `detect`, `test`, `generate`) | 5 | **PASS** |
| **Total** | **Comprehensive Polyglot Framework Coverage** | **37** | **100% PASS** |
