# DEX Engineering Skills Pack v4.0 — Installation & Quickstart Guide

## 1. System Requirements

- **Operating System**: Windows 11, Windows 10 (WSL2 supported), macOS 13+, or Ubuntu 22.04+
- **Runtimes**: Python 3.10+ (Python 3.12 recommended), Node.js 20+ LTS
- **AI Coding Agent**: OpenAI Codex, Cursor, Windsurf, Claude Code, or VS Code with Agent Skills support

---

## 2. Installation Steps

### Step 1: Clone Repository
```bash
git clone https://github.com/nguyenducanhst2022-png/dex-engineering-skills.git
cd dex-engineering-skills
```

### Step 2: Install Python Dependencies
```bash
pip install -r requirements-dev.txt
# Hoặc cài đặt trực tiếp pytest:
pip install pytest
```

### Step 3: Run Validation & Verification
```bash
# Validate toàn bộ 121 kỹ năng DEX
python scripts/validate_skills.py

# Chạy toàn bộ test suite
pytest tests/ -v
```

---

## 3. Configuring for AI Coding Agents

### OpenAI Codex / Universal Coding Agents
Sao chép thư mục `.agents/` vào thư mục gốc của dự án bạn đang phát triển:
```bash
cp -r .agents /path/to/your/project/
```

Thêm chỉ dẫn vào file `AGENTS.md` trong dự án của bạn:
```markdown
# AGENTS.md
You have access to the DEX Engineering Skills Pack in `.agents/skills/`.
Always begin tasks by activating `dex-master-orchestrator`.
The Master Orchestrator will classify your task (QUICK, STANDARD, STRICT),
select the required specialized skills from Groups A through L (120 skills),
and enforce the 12 Quality Gates.
```
