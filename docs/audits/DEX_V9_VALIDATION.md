# v9 validation evidence
- `python -m pytest -q`: 1,680 passed in 6.65s. Raw output: DEX_V9_PYTEST.txt.
- `python scripts/validate_skills.py`: 501/501 native and 8/8 external adapters structurally valid, zero structural errors. Raw output: DEX_V9_STRUCTURE.txt.
- `python scripts/polyglot/dex.py skills audit --format json`: canonical count PASS, structural gate PASS, release NOT_READY. Raw output: DEX_V9_INVENTORY.json.
- `git diff --check`: exit 0.

Tests include legacy content assertions and mock fixtures; their aggregate pass count does not establish specialist functional correctness. Native runtime verification count is unknown. The lightweight legacy frontmatter parser is not a full YAML/spec validator. Full spec tooling, exhaustive local-link/dependency checks, semantic duplication review and real host execution remain NOT_VERIFIED.
