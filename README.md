# DEX Engineering Skills Framework v10.0

[![CI](https://github.com/nguyenducanhst2022-png/dex-engineering-skills/actions/workflows/validate.yml/badge.svg?branch=main)](https://github.com/nguyenducanhst2022-png/dex-engineering-skills/actions/workflows/validate.yml)

A catalog of **501 native agent skills**: 500 specialists in 50 groups (A–AX, ten skills each, IDs 001–500) plus one root router, `dex-master-orchestrator`. Eight external adapters live under `integrations/` and are not part of the native count.

Skills use the YAML frontmatter + Markdown format of the [Agent Skills specification](https://agentskills.io/specification). DEX's 14-section body structure is a repository convention, not a spec requirement.

## Layout

| Path | Contents |
|:---|:---|
| `.agents/skills/<name>/SKILL.md` | The 501 native skills |
| `integrations/` | 7 upstream sources (8 adapters), kept separate from native skills |
| `manifests/` | `native-skills.json` (canonical IDs), `dex-skills.json` (discovered files), `upstream-sources.json` (pins, license hashes) |
| `scripts/` | Validation, audit, routing evaluation; `scripts/polyglot/dex.py` CLI |
| `tests/` | pytest suite |
| `docs/quality/`, `docs/audits/` | Audit records and evidence |
| `.github/workflows/validate.yml` | CI on Ubuntu, Windows and macOS (Python 3.12) |

Find individual skills in the [skills index](SKILLS_INDEX.md). Group/domain mapping is in the index and [`manifests/native-skills.json`](manifests/native-skills.json).

## Quick start

```sh
git clone https://github.com/nguyenducanhst2022-png/dex-engineering-skills.git
cd dex-engineering-skills
python3 -m venv .venv
. .venv/bin/activate          # Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
python -m pytest -q
python scripts/validate_skills.py
```

See [INSTALL.md](INSTALL.md) for agent setup and the full set of checks.

## Using the skills

Open the repository in your coding-agent workspace (or point the agent's skills directory at `.agents/skills`) and start from [`dex-master-orchestrator`](.agents/skills/dex-master-orchestrator/SKILL.md). The orchestrator picks the smallest sufficient skill set and runs in one of three modes: QUICK (small reversible edits), STANDARD (features, refactors, integrations) or STRICT (security, infrastructure, data-loss or release risk). Skill discovery and tool permissions depend on the host agent; cloning installs no runtimes and changes no global settings.

## Polyglot CLI

`scripts/polyglot/dex.py` wraps adapters for Python, TypeScript, JavaScript, PowerShell, Bash, Rust, Go, C++, C#, Java and PHP, plus read-only catalog commands:

```sh
python scripts/polyglot/dex.py doctor --format json          # which toolchains exist on this host
python scripts/polyglot/dex.py skills status --format json
python scripts/polyglot/dex.py skills validate --format json
python scripts/polyglot/dex.py verify --skill dex-development-workflow
```

Missing toolchains are reported as `TOOL_NOT_AVAILABLE`; finding a tool does not prove the runtime is usable.

## Status

Structural validation (501/501 native, 8/8 integrations), the quality audit (avg 85.4/100), 25/25 routing fixtures and 1,702 tests pass. The catalog itself reports `"release": "NOT_READY"`: domain runtime/cross-host evaluation, upstream provenance/licensing review, and independent semantic/content review are still open (`python scripts/polyglot/dex.py skills report --format json` exits 1 until they are resolved).

## Upstream integrations

| Source | Pinned commit | License | Directory |
|:---|:---|:---|:---|
| [Agentic Awesome Skills](https://github.com/sickn33/agentic-awesome-skills) | `8bda5fa7` | MIT | `integrations/aas/` |
| [Reverse Skill](https://github.com/zhaoxuya520/reverse-skill) | `cab634bd` | MIT | `integrations/reverse-skill/` |
| [REA](https://github.com/morluto/rea) | `e32a0494` | MIT | `integrations/rea/` |
| [UI/UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | `04cfb449` | MIT | `integrations/ui-ux-pro-max/` |
| [Supabase Agent Skills](https://github.com/supabase/agent-skills) | `c9be0e93` | MIT | `integrations/supabase/` |
| [Superpowers](https://github.com/obra/superpowers) | `2ce8aa15` | MIT | `integrations/superpowers/` |
| [Matt Pocock Skills](https://github.com/mattpocock/skills) | `5beb35b0` | MIT | `integrations/mattpocock/` |

Full SHAs and license hashes: [`manifests/upstream-sources.json`](manifests/upstream-sources.json). Each source's license text is in its `UPSTREAM_LICENSE`.

## Documentation

[Skills index](SKILLS_INDEX.md) · [Install](INSTALL.md) · [Architecture](ARCHITECTURE.md) · [Routing matrix](ROUTING_MATRIX.md) · [V10 baseline](docs/quality/BASELINE_V10.md) · [Defect register](docs/quality/DEFECT_REGISTER.md) · [Third-party notices](THIRD_PARTY_NOTICES.md) · [Changelog](CHANGELOG.md)

## License

[MIT](LICENSE). Upstream material keeps its own license and attribution terms.
