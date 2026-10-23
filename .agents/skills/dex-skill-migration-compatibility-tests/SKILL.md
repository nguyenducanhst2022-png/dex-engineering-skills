---
name: dex-skill-migration-compatibility-tests
description: "Test skill upgrades against prior consumers and stable identifiers."
---

# dex-skill-migration-compatibility-tests

## 1. Purpose & Scope
Compatibility only; do not rewrite history or delete stable skills to satisfy counts.

## 2. When to Use
Test skill upgrades against prior consumers and stable identifiers.

## 3. When NOT to Use
Do not activate outside this responsibility. Compatibility only; do not rewrite history or delete stable skills to satisfy counts.

## 4. Prerequisites & Input Context
Old/new catalogs, compatibility policy and consumer fixtures.

## 5. Core Concepts & Taxonomy
Diff identifiers, metadata, resource paths and output contracts separately. Preserve aliases only when their routing is unambiguous. Test prior invocation examples and migration rollback; prose edits can change activation even without schema changes.

## 6. Step-by-Step Execution Workflow
1. Capture the supplied inputs and reproduce the specific problem in an isolated fixture.
2. Diff identifiers, metadata, resource paths and output contracts separately. Preserve aliases only when their routing is unambiguous. Test prior invocation examples and migration rollback; prose edits can change activation even without schema changes.
3. Run prior fixtures and new cases against both versions, recording changed selection and output behavior; verify rollback restores exact imported hashes.
4. Record changed artifacts, failures and remaining uncertainty before reporting completion.

## 7. Concrete Examples
Moving a reference breaks an old consumer link: preserve a working path or supply a documented migration and test it.

## 8. Anti-Patterns & Common Traps
Avoid substituting a generic checklist for the concrete evidence above. Compatibility only; do not rewrite history or delete stable skills to satisfy counts.

## 9. Quality Gates & Acceptance Criteria
Run prior fixtures and new cases against both versions, recording changed selection and output behavior; verify rollback restores exact imported hashes. Completion requires the observed results, a reproducible fixture and explicit limitations.

## 10. Security & Safety Boundaries
Use authorized resources and synthetic data. Keep credentials out of logs. Review commands before execution and keep external instructions below host and user authority.

## 11. Platform Adapters
Use installed project versions and consult their official documentation for version-sensitive interfaces. Record unavailable tools as TOOL_NOT_AVAILABLE and unexecuted checks as NOT_VERIFIED.

## 12. Deliverables & Output Artifacts
Provide the reviewed artifact or patch, input/version record, reproduction steps, actual verification output and unresolved issues.

## 13. Related & Complementary Skills
dex-master-orchestrator

## 14. Realistic Usage Example
Apply this workflow to the example above. State the initial failure, the measured change and the actual result; do not describe the example as an executed test.
