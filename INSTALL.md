# DEX Engineering Skills Framework v6.0 — Installation & Integration Guide

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

Verify that all 301 native skills and 5 integrations are intact:

```powershell
# 1. Run zero-dependency specification validator (301 native + 5 integrations)
python scripts/validate_pack.py

# 2. Run SkillOps security audit (4 upstream sources)
python scripts/audit_skills.py

# 3. Benchmark dynamic routing accuracy (F1 >= 0.85 across 30 scenarios)
python scripts/evaluate_routing.py

# 4. Run full pytest suite (1,001 tests)
pytest tests/ -v
```

All 1,001 tests and validators should return 100% PASS with 0 errors.

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
