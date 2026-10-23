# DEX Engineering Skills Framework v9.0

**500 specialized skills + 1 master orchestrator, organized into 50 engineering groups.**

Focused engineering workflows for coding agents, with a Polyglot Script Engine, SkillOps tooling and seven segregated upstream sources. Discover relevant skills through catalog metadata, load instructions on demand and record verification evidence.

[![CI](https://github.com/nguyenducanhst2022-png/dex-engineering-skills/actions/workflows/validate.yml/badge.svg?branch=feat%2Fdex-500-skills)](https://github.com/nguyenducanhst2022-png/dex-engineering-skills/actions/workflows/validate.yml)
[![Version](https://img.shields.io/badge/version-9.0_candidate-blue)](docs/audits/DEX_V9_RELEASE_READINESS.md)
[![Skills](https://img.shields.io/badge/native_skills-501-blue)](SKILLS_INDEX.md)
[![Tests](https://img.shields.io/badge/tests-1689_passed-brightgreen)](docs/audits/DEX_V9_PYTEST.txt)
[![Routing](https://img.shields.io/badge/routing_fixtures-16%2F16-brightgreen)](docs/audits/DEX_V9_ROUTING_FIXTURES.json)

## What's included

- 500 specialists across Groups A-AX and one native root router, `dex-master-orchestrator`.
- 11 language adapters: Python, TypeScript, JavaScript, PowerShell, Bash, Rust, Go, C++, C#, Java and PHP.
- 8 external adapters under `integrations/`, excluded from the native count.
- Canonical inventory checks, structural validation, routing fixtures and upstream provenance verification.
- Automated CI for Windows, Linux and macOS.

v9 adds skills 401-500 in Groups AO-AX while preserving identifiers 001-400. Use the [skills index](SKILLS_INDEX.md) to find individual workflows.

## Quick start

The v9 implementation is on `feat/dex-500-skills`:

```sh
git clone --branch feat/dex-500-skills https://github.com/nguyenducanhst2022-png/dex-engineering-skills.git
cd dex-engineering-skills
python -m venv .venv
```

Activate `.venv` using `.venv\Scripts\Activate.ps1` in Windows PowerShell or `source .venv/bin/activate` on Linux/macOS, then run:

```sh
python -m pip install pytest==8.3.5
python scripts/polyglot/dex.py skills status --format json
python scripts/validate_skills.py
```

Open the repository in your coding-agent workspace and start with [dex-master-orchestrator](.agents/skills/dex-master-orchestrator/SKILL.md). Host discovery and tool permissions depend on the host. Cloning does not install upstream runtimes or change global agent settings.

## Engineering catalog

Each group contains ten specialists; the master orchestrator is separate.

| Group | Skill IDs | Domain |
|:---|:---|:---|
| A | 001-010 | Core Engineering |
| B | 011-020 | Architecture & AI Agents |
| C | 021-030 | Production Engineering |
| D | 031-040 | Frontend Engineering |
| E | 041-050 | Backend & Integration |
| F | 051-060 | Data Engineering |
| G | 061-070 | AI & LLM Engineering |
| H | 071-080 | Developer Experience |
| I | 081-090 | Security & Reliability |
| J | 091-100 | Cloud & Infrastructure |
| K | 101-110 | Mobile & Desktop Engineering |
| L | 111-120 | Product & Operations Engineering |
| M | 121-130 | Advanced Software Verification |
| N | 131-140 | Advanced SRE & Distributed Systems |
| O | 141-150 | Advanced Cloud Platform |
| P | 151-160 | Language & Runtime Engineering |
| Q | 161-170 | Advanced AI Systems |
| R | 171-180 | Product Design & User Research |
| S | 181-190 | Application Security Specialists |
| T | 191-200 | SkillOps Engineering |
| U | 201-210 | Visual Design Intelligence |
| V | 211-220 | Advanced Web Experiences |
| W | 221-230 | Browser Extensions & Automation |
| X | 231-240 | Authorized Reverse Engineering |
| Y | 241-250 | Protocols & Service Integration |
| Z | 251-260 | AI Agent Operations |
| AA | 261-270 | Advanced Data & Analytics |
| AB | 271-280 | Native, Graphics & Game Engineering |
| AC | 281-290 | Software Trust & Distribution |
| AD | 291-300 | Advanced SkillOps Governance |
| AE | 301-310 | Enterprise Software Architecture |
| AF | 311-320 | Distributed Systems Deep Engineering |
| AG | 321-330 | Applied AI Systems |
| AH | 331-340 | Extended Polyglot Engineering |
| AI | 341-350 | Advanced UI/UX Engineering |
| AJ | 351-360 | Authorized Software Inspection |
| AK | 361-370 | ML Platform & Data Systems |
| AL | 371-380 | Developer Platform & Polyglot Tooling |
| AM | 381-390 | Advanced Security & Trust |
| AN | 391-400 | SkillOps Quality & Governance |
| AO | 401-410 | Supabase & Advanced PostgreSQL |
| AP | 411-420 | Autonomous Agent Engineering |
| AQ | 421-430 | Streaming & Digital Media Systems |
| AR | 431-440 | Chess & Native Performance |
| AS | 441-450 | Windows & Desktop Systems |
| AT | 451-460 | Platform Resilience & Infrastructure |
| AU | 461-470 | Product Experience & Design Systems |
| AV | 471-480 | Advanced TypeScript & Full Stack |
| AW | 481-490 | Security, Privacy & Resilience Governance |
| AX | 491-500 | SkillOps Intelligence & Scalability |

The [canonical manifest](manifests/native-skills.json) defines stable identifiers and release targets. The [discovery manifest](manifests/dex-skills.json) records actual files.

Skills follow the YAML frontmatter and Markdown format of the [Agent Skills specification](https://agentskills.io/specification). DEX's 14-section structure is a repository convention, not an external specification requirement.

## Master orchestrator

The master identifies the task, selects the smallest sufficient skill set, checks tools and permissions, coordinates execution and records evidence.

| Mode | Typical work |
|:---|:---|
| QUICK | Narrow, reversible fixes and edits |
| STANDARD | Features, refactoring and integrations |
| STRICT | Changes with significant security, infrastructure, data-loss or release risk |

Metadata is searched first; full instructions and references are loaded only when needed. External instructions remain subordinate to host and user instructions.

## Polyglot Script Engine

Adapters share argument-based command execution, normalized results, dry-run support and tool discovery. The executor provides capped stdout/stderr buffers, timeouts, secret redaction, an inherited-environment allowlist and best-effort process-tree cleanup.

```sh
python scripts/polyglot/dex.py doctor --format json
python scripts/polyglot/dex.py test --lang python --cwd path/to/project --dry-run
python scripts/polyglot/dex.py generate --lang typescript --task auth_middleware --out generated
```

Review the target project and its commands before execution. Missing tools return `TOOL_NOT_AVAILABLE`. Tool discovery alone does not prove runtime readiness: CMake is not a C++ compiler, and npx does not establish a TypeScript compiler. See the recorded [Python, JavaScript and PowerShell smoke checks](docs/audits/DEX_V9_RUNTIME_SMOKE.json).

## SkillOps and verification

Read-only catalog commands:

```sh
python scripts/polyglot/dex.py skills status --format json
python scripts/polyglot/dex.py skills audit --format json
python scripts/polyglot/dex.py skills plan --format json
python scripts/polyglot/dex.py skills validate --format json
python scripts/polyglot/dex.py skills report --format json
```

`validate` checks structure and canonical inventory. `report` returns nonzero while release blockers remain. Other lifecycle operations retain existing standalone scripts; the full unified interface is still being developed.

Verification commands:

```sh
python -m pytest -q
python scripts/validate_skills.py
python scripts/evaluate_routing_v9.py
python scripts/verify_upstream_provenance.py
```

| Recorded check | Result | Evidence |
|:---|:---|:---|
| Native structural validation | 501/501 | [Output](docs/audits/DEX_V9_STRUCTURE.txt) |
| External adapter structure | 8/8 | [Output](docs/audits/DEX_V9_STRUCTURE.txt) |
| Regression tests | 1,689 passed | [Pytest](docs/audits/DEX_V9_PYTEST.txt) |
| v9 lexical routing fixtures | 16/16 | [Fixtures](docs/audits/DEX_V9_ROUTING_FIXTURES.json) |
| Configured upstream pins | 7/7 verified | [Provenance](docs/audits/DEX_V9_PROVENANCE_RECHECK.json) |
| Stored upstream license bytes | 7/7 match | [Provenance](docs/audits/DEX_V9_PROVENANCE_RECHECK.json) |

The current version is a development candidate. These recorded checks do not certify every specialist workflow. Remaining domain runtime, content and historical import-origin review is tracked in [release readiness](docs/audits/DEX_V9_RELEASE_READINESS.md).

## Upstream integrations

External adapters remain separate from native skills. These commits are verified reference baselines; they do not retroactively authenticate historical imports.

| Source | Pinned commit | Root license | Directory |
|:---|:---|:---|:---|
| [Agentic Awesome Skills](https://github.com/sickn33/agentic-awesome-skills) | [8bda5fa7](https://github.com/sickn33/agentic-awesome-skills/commit/8bda5fa7264cafe8259fc8212550d13bf690bfb0) | MIT | `integrations/aas/` |
| [Reverse Skill](https://github.com/zhaoxuya520/reverse-skill) | [cab634bd](https://github.com/zhaoxuya520/reverse-skill/commit/cab634bd855fc287f6e420c1f36fd1a6b9245960) | MIT | `integrations/reverse-skill/` |
| [Reverse Engineer Anything (REA)](https://github.com/morluto/rea) | [e32a0494](https://github.com/morluto/rea/commit/e32a0494d42dedd5e79ca341d20c53f07479d9bb) | MIT | `integrations/rea/` |
| [UI/UX Pro Max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | [04cfb449](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/commit/04cfb449bd8494811ad63e94172a308fa25a551a) | MIT | `integrations/ui-ux-pro-max/` |
| [Supabase Agent Skills](https://github.com/supabase/agent-skills) | [c9be0e93](https://github.com/supabase/agent-skills/commit/c9be0e931b7930f7d02126d04774d904c381e7d7) | MIT | `integrations/supabase/` |
| [Superpowers](https://github.com/obra/superpowers) | [2ce8aa15](https://github.com/obra/superpowers/commit/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b) | MIT | `integrations/superpowers/` |
| [Matt Pocock Skills](https://github.com/mattpocock/skills) | [5beb35b0](https://github.com/mattpocock/skills/commit/5beb35b040e3de97e54fa9e386d7e42d15c295c2) | MIT | `integrations/mattpocock/` |

The [source manifest](manifests/upstream-sources.json) records exact SHAs, license hashes and prior pin history. Exact upstream license text is stored in each source's `UPSTREAM_LICENSE`. During API rate limits, the verifier can check exact-SHA commit patch headers and retrieve pinned license bytes. It does not install or execute upstream code.

## Documentation

- [Skills index](SKILLS_INDEX.md)
- [Installation guide](INSTALL.md) and [architecture](ARCHITECTURE.md), including historical version details
- [Implementation progress](docs/audits/DEX_V9_PROGRESS.md)
- [Validation](docs/audits/DEX_V9_VALIDATION.md) and [release readiness](docs/audits/DEX_V9_RELEASE_READINESS.md)
- [Security audit](docs/audits/DEX_V9_SECURITY_AUDIT.md) and [license audit](docs/audits/DEX_V9_LICENSE_AUDIT.md)
- [Third-party notices](THIRD_PARTY_NOTICES.md)

## License

DEX Engineering Skills Framework uses the [MIT License](LICENSE). Upstream material retains its own license and attribution requirements.
