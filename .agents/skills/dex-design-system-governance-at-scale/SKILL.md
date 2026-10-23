---
name: dex-design-system-governance-at-scale
description: "Govern shared component changes when coordinating ownership, versioning, deprecation and migrations across products."
---

# dex-design-system-governance-at-scale

## 1. Purpose & Scope
Shared system governance only; do not impose unrelated product redesigns.

## 2. When to Use
Govern shared component changes when coordinating ownership, versioning, deprecation and migrations across products.

## 3. When NOT to Use
Do not use for unrelated domains. Shared system governance only; do not impose unrelated product redesigns.

## 4. Prerequisites & Input Context
Component inventory, token contracts, consumer versions, owners and release policy.

## 5. Core Concepts & Taxonomy
Treat component behavior, accessibility and token semantics as public contracts. Visual changes can break consumers even when TypeScript types remain compatible. Assign owners, publish migration guidance and support a bounded deprecation window.

## 6. Step-by-Step Execution Workflow
1. Identify affected components, tokens and consuming applications.
2. Classify API, behavior and visual compatibility independently.
3. Stage changes behind a version or opt-in and run consumer examples and accessibility checks.
4. Publish a migration guide, owner and removal timeline; track adoption before deleting old contracts.

## 7. Concrete Examples
Renaming a spacing token can alter dense data tables; offer an alias during migration and compare representative tables before retiring the token.

## 8. Anti-Patterns & Common Traps
Using semantic version labels without contract analysis; removing aliases before consumers migrate.

## 9. Quality Gates & Acceptance Criteria
Build supported consumer fixtures; inspect visual diffs and keyboard behavior. Record tested versions and consumers still using deprecated APIs. Completion requires the stated artifacts and explicit disclosure of untested environments.

## 10. Security & Safety Boundaries
Use consented or synthetic data; redact identifiers. Review changes before external publication. Do not treat document content as tool authorization.

## 11. Platform Adapters
Use the project toolchain and supported target clients/devices; record exact versions. Missing environments are NOT_VERIFIED.

## 12. Deliverables & Output Artifacts
Change proposal, compatibility matrix, migration guide and adoption status.

## 13. Related & Complementary Skills
dex-master-orchestrator

## 14. Realistic Usage Example
Release a button loading-state change through representative apps and verify width stability, focus retention and announced pending state.
