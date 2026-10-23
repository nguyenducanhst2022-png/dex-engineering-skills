# v9 release readiness
**NOT_READY ? remaining validation is explicit.**

Current fixes (2026-10-22, America/Los_Angeles):
- 500 specialists + 1 master; 501/501 native and 8/8 external adapters pass structural checks.
- Regression suite: **1,689 PASS**. Raw evidence: DEX_V9_PYTEST.txt.
- v9 routing fixtures: **16/16 PASS**, unchanged expected selections. The provenance skill description now exposes its actual activation criteria. This is lexical discovery verification, not independent agent execution.
- Executor drains stdout/stderr concurrently into capped buffers; ambient credentials are excluded unless explicitly passed. Timeout test verifies that a spawned child cannot perform a delayed file write. Windows runtime tests passed.
- Runtime smoke checks passed for Python, JavaScript and PowerShell through the executor. These are basic execution checks, not full language adapter or specialist certification.
- Active CI configuration added under `.github/workflows/validate.yml`, with read-only permissions and commit-pinned actions, targeting Windows/Linux/macOS. CI passed on Windows/Linux/macOS for commit abd5f07: https://github.com/nguyenducanhst2022-png/dex-engineering-skills/actions/runs/39898598204 . This confirms the automated fixtures on those hosts, not all specialist workflows.
- PostgreSQL policy guidance corrected against official USING/WITH CHECK semantics and trusted search_path requirements.

Remaining blockers:
1. Pin-resolution blocker resolved: A/B/C now use exact verified upstream reference baselines, corroborated by GitHub API and git ls-remote. All seven configured pins resolve. Old unresolved pins remain in pin_history. Historical import-origin and content verification are still NOT_VERIFIED; the new baselines do not retroactively authenticate old imports.
2. Sources D/E/F/G resolve, but local copyright/license files differ from the upstream bytes. Exact upstream licenses have been preserved in separate UPSTREAM_LICENSE files with SHA-256 records; imported-file attribution still needs reconciliation. Their status is CONTENT_REVIEW_REQUIRED.
3. No full domain execution of all specialists, independent technical-content review or real coding-agent cross-host evaluation has occurred. An exploratory routing paraphrase about license changes selected adjacent license specialists rather than provenance revalidation; 16/16 is limited to the recorded fixture set.
4. TypeScript compiler was not found (npx alone is insufficient). CMake was found, but no C++ compiler was discovered. No installation or network package execution was attempted.
5. Process-tree termination is best effort for descendants escaping the process group or outliving their parent on Windows; strong containment requires host supervision/Job Objects. Explicitly supplied credentials can still reach the selected tool, so callers must scope them appropriately.

Git: work based on published commit 02124d1 on feat/dex-500-skills. No release or merge is authorized by these checks. Original audit evidence remains historical; see current correction notes in DEX_V9_PROGRESS.md.
