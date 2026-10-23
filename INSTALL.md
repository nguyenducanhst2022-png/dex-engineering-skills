> **v9 candidate status (2026-10-22, America/Los_Angeles): NOT_READY.**
> Current inventory: 500 specialists + 1 master; 8 external adapters are separate.
> Structural validity does not establish domain runtime correctness.
> All seven configured upstream pins now resolve; import-origin/content review remains separate. See [current evidence](docs/audits/DEX_V9_PROVENANCE_RECHECK.json).
> The text below includes prior-version documentation; current limitations and validation are recorded in [v9 progress](docs/audits/DEX_V9_PROGRESS.md).

# DEX Engineering Skills Framework v8.0 — Installation & Integration Guide

> Comprehensive setup instructions for Windows 11, OpenAI Codex, VS Code, Cursor, and Claude Code.

---

## 1. Prerequisites

- **Operating System**: Windows 11 (Primary / Recommended), macOS 14+, or Ubuntu 22.04+ LTS.
- **Python**: Version 3.10 or newer (tested on Python 3.12).
- **Git**: Version 2.40 or newer.
- **Coding Agent**: OpenAI Codex, GitHub Copilot, Cursor, Windsurf, or Claude Code.

---

## 2. Installation Steps

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

pip install pytest pyyaml
```

---

## 3. Validating the Installation

Verify that all 401 native skills, 5 integrations, and Polyglot Script Engine are intact:

```powershell
# 1. Run zero-dependency specification validator (401 native + 5 integrations)
python scripts/validate_pack.py

# 2. Run SkillOps security audit (401 native skills + 4 upstream sources)
python scripts/audit_skills.py

# 3. Benchmark dynamic routing accuracy (F1 >= 0.85 across 40 scenarios)
python scripts/evaluate_routing.py

# 4. Run Polyglot Toolchain Diagnostics
python scripts/polyglot/dex.py doctor

# 5. Run full pytest suite (1,360 tests)
pytest tests/ scripts/polyglot/tests/ -v
```

All 1,360 tests and validators should return 100% PASS with 0 errors.

---

## 4. Agent Integration

### OpenAI Codex / VS Code
Copy or symlink the `.agents/skills` directory to your agent workspace:
```powershell
# Windows PowerShell symlink
New-Item -ItemType SymbolicLink -Path "$HOME\.codex\skills" -Target "$PWD\.agents\skills"
```

### Claude Code / Cursor
Reference `.agents/skills/dex-master-orchestrator/SKILL.md` as the primary instruction file in your workspace settings.

## v9 evidence commands
Run from the repository root with Python 3:

```text
python scripts/polyglot/dex.py skills status --format json
python scripts/polyglot/dex.py skills validate --format json
python scripts/polyglot/dex.py skills report --format json
```

These commands are read-only. `validate` checks structure and canonical inventory;
`report` exits 1 while release blockers remain. No global agent installation is performed.
The existing discovery/import/sync scripts remain available; create, compare, routing,
dependencies, quality, import, sync and rollback are not yet unified under `dex skills`.
