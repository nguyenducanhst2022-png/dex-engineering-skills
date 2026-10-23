# DEX Engineering Skills Framework v10.0 — Installation & Integration Guide

> Comprehensive setup and integration guide for coding agents (OpenAI Codex, GitHub Copilot, Cursor, Windsurf, Claude Code, Antigravity).

---

## 1. Prerequisites

- **Operating System**: Windows 11 (Primary / Tested), macOS 14+, or Ubuntu 22.04+ LTS.
- **Python**: Version 3.10 or newer (tested on Python 3.12.10).
- **Node.js**: Version 20+ (recommended for full-stack and TypeScript contract validation).
- **Git**: Version 2.40 or newer.

---

## 2. Quick Start

### Clone Repository
```powershell
git clone https://github.com/nguyenducanhst2022-png/dex-engineering-skills.git
cd dex-engineering-skills
```

### Setup Python Virtual Environment
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1   # On Windows PowerShell
# source .venv/bin/activate    # On Linux/macOS

python -m pip install pytest==8.4.2
```

---

## 3. Validating the Installation

Verify that all **501 native skills**, **8 segregated integrations**, and the **Polyglot Script Engine** are operational:

```powershell
# 1. Run zero-dependency specification validator (501 native + 8 integrations)
python scripts/validate_skills.py

# 2. Run SkillOps 100-point quality audit & security screening
python scripts/audit_skills.py --export-v10

# 3. Benchmark dynamic routing accuracy across all 50 groups (A to AX)
python scripts/evaluate_routing_v10.py

# 4. Run Polyglot Toolchain Diagnostics
python scripts/polyglot/dex.py doctor

# 5. Verify individual skill quality (e.g. dex-development-workflow)
python scripts/polyglot/dex.py verify --skill dex-development-workflow

# 6. Run full pytest regression & functional test suite (>1,689 tests)
pytest -q
```

All tests, specification gates, and routing benchmarks will return 100% PASS with 0 errors.

---

## 4. Agent Integration

### OpenAI Codex / VS Code / Cursor
Reference or copy `.agents/skills` to your workspace:
```powershell
# Windows PowerShell symlink
New-Item -ItemType SymbolicLink -Path "$HOME\.codex\skills" -Target "$PWD\.agents\skills"
```

### Claude Code / Windsurf / Antigravity
Direct your agent to start from [`.agents/skills/dex-master-orchestrator/SKILL.md`](.agents/skills/dex-master-orchestrator/SKILL.md) as the root control plane.

---

## 5. V10 Evidence Commands

Run from the repository root:

```powershell
python scripts/polyglot/dex.py skills status --format json
python scripts/polyglot/dex.py skills validate --format json
```

These commands provide immutable evidence of catalog synchronization, release count compliance, and structural integrity.
