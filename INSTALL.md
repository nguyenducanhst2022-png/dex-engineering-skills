# DEX Engineering Skills Framework v5.0 — Installation & Integration Guide

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

pip install -r requirements-dev.txt   # If present, or install pytest pyyaml
pip install pytest pyyaml
```

---

## 3. Validating the Installation

Verify that all 201 native skills and 4 integrations are intact:

```powershell
# 1. Run zero-dependency specification validator
python scripts/validate_pack.py

# 2. Run SkillOps security audit
python scripts/audit_skills.py

# 3. Benchmark dynamic routing accuracy (F1 >= 0.85)
python scripts/evaluate_routing.py

# 4. Run full pytest suite (645 tests)
pytest tests/ -v
```

All 645 tests and validators should return 100% PASS with 0 errors.

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
