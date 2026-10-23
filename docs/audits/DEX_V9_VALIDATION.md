# v9 validation evidence
- `python -m pytest -q`: 1,680 passed in 6.65s. Raw output: DEX_V9_PYTEST.txt.
- `python scripts/validate_skills.py`: 501/501 native and 8/8 external adapters structurally valid, zero structural errors. Raw output: DEX_V9_STRUCTURE.txt.
- `python scripts/polyglot/dex.py skills audit --format json`: canonical count PASS, structural gate PASS, release NOT_READY. Raw output: DEX_V9_INVENTORY.json.
- `git diff --check`: exit 0.

Tests include legacy content assertions and mock fixtures; their aggregate pass count does not establish specialist functional correctness. Native runtime verification count is unknown. The lightweight legacy frontmatter parser is not a full YAML/spec validator. Full spec tooling, exhaustive local-link/dependency checks, semantic duplication review and real host execution remain NOT_VERIFIED.


## Current correction checkpoint ? 2026-10-22

Current run supersedes the earlier count: 1,685 tests passed in 11.96s. New tests exercise capped dual-stream output, credential opt-in, timeout descendant side effects, legacy ACTIVE_VERIFIED rejection and exact upstream SHA matching. Python/JavaScript/PowerShell smoke execution passed; see DEX_V9_RUNTIME_SMOKE.json. 501 native + 8 external structural checks pass. No claim of all specialist runtime verification is made.


## Three-pin update validation

Current regression run: 1,689 tests passed in 12.77s. All seven configured pins resolve and all seven stored upstream license files match the fetched pinned bytes. Tests verify exact-SHA patch fallback during API rate limits, rejection of mismatched commit headers, preserved old-pin history, and the separation of verified reference pins from unverified import origins. Structural checks remain 501/501 native plus 8/8 external; routing remains 16/16.
