# v9 security review
No upstream script was executed, global settings changed, destructive Git operation performed or release published. Native and external skills remain segregated. Read-only SkillOps commands do not execute commands embedded in skill text.

Unresolved findings:
- Polyglot executor uses capture_output and truncates after subprocess completion. This bounds reported output but not peak memory. Streaming drains or bounded spool handling are required before claiming bounded execution logs.
- Executor inherits the process environment; least-privilege environment filtering and child process-tree cancellation need review.
- Three configured upstream pins did not resolve; existing ACTIVE_VERIFIED labels are unsupported for these sources (see upstream evidence).
- Pre-existing PostgreSQL RLS guidance says omitting WITH CHECK always permits tenant reassignment. PostgreSQL can reuse USING as WITH CHECK for relevant policies; that claim needs correction after reviewing the exact policy composition. The original user-owned file was preserved.
- Full repository secret scanning, dependency vulnerability evaluation and executable source review were not performed.

No critical-security-clearance claim is made. Release gate remains NOT_READY.


## Current correction checkpoint ? 2026-10-22

Current fixes supersede the first three executor findings: bounded streaming capture replaces post-capture slicing; a runtime/OS environment allowlist replaces ambient inheritance; timeout and KeyboardInterrupt paths stop the direct child and attempt process-tree cleanup. A real delayed-child side-effect test passed on Windows. Strong containment of escaped descendants remains unverified. Corrected RLS omission, FORCE and trusted-search_path guidance in both skill and authoring source. Upstream statuses no longer assert ACTIVE_VERIFIED for unreviewed content; sync now returns nonzero for incomplete review. Full secret/dependency review remains incomplete.


## Three-pin resolution checkpoint - 2026-10-22
A/B/C now point to verified upstream reference baselines. GitHub exact-commit
resolution and git ls-remote HEAD agreed for each source. All seven configured
pins now resolve. See DEX_V9_PIN_CANDIDATES.json and DEX_V9_PROVENANCE_RECHECK.json.
The old invalid pins remain in manifest pin_history. Existing imported skills
still have unverified historical origin; their old claims were not rewritten
as if content had been re-imported. Exact A/B/C upstream licenses are retained
as UPSTREAM_LICENSE. REA's current pinned root license is MIT; its prior Apache
claim is historical and unverified. AAS root text is MIT, while GitHub's automatic
SPDX classification returned NOASSERTION. No external code was installed or run.
