# Installation

## Prerequisites

- Python 3.10+ (CI uses 3.12; also verified locally with 3.13.5)
- Git
- Optional: language toolchains (Node.js, Rust, Go, …) only if you run the polyglot adapters against projects in those languages. Check with `python scripts/polyglot/dex.py doctor`.

## 1. Clone and create a virtual environment

```sh
git clone https://github.com/nguyenducanhst2022-png/dex-engineering-skills.git
cd dex-engineering-skills
python3 -m venv .venv
. .venv/bin/activate          # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
```

pytest is the only dependency; the scripts use the standard library.


## 2. Run the tests and checks

Keep the venv **activated** while running these: a toolchain detector uses `shutil.which("python")`, so it needs `python` on `PATH`.

```sh
python -m pytest -q                                              # 1,702 tests
python scripts/validate_skills.py                               # 501 native + 8 integrations
python scripts/audit_skills.py --export-v10                     # rewrites docs/quality/SKILL_AUDIT_V10.json
python scripts/evaluate_routing_v10.py                          # 25 routing fixtures
python scripts/polyglot/dex.py verify --skill dex-development-workflow
python scripts/polyglot/dex.py skills validate --format json
```

These are the same steps CI runs (`.github/workflows/validate.yml`). All exit 0 when the catalog is healthy.

`python scripts/polyglot/dex.py skills report --format json` intentionally exits 1 while release blockers remain (`"release": "NOT_READY"`); that is not an install failure.

## 3. Connect your agent

Skills live in `.agents/skills/`. Either open the repository as the agent workspace, or point the agent's skills directory at that folder, then start from `.agents/skills/dex-master-orchestrator/SKILL.md`. Where the agent looks for skills depends on the host; consult its documentation.
