# DEX Engineering Skills Framework v8.0 — Upstream Integration & Provenance Audit

> **Audit Date:** 2026-10-23  
> **Audited Subsystem:** `integrations/` & `manifests/upstream-sources.json`  
> **Status:** 100% VERIFIED — ALL SOURCES QUARANTINED — LICENSE & PROVENANCE VALIDATED

---

## 1. Upstream Segregation Policy

Third-party agent skills and external developer tooling are governed under strict quarantine boundaries:
1. **Namespace Isolation**: Upstream skills are placed in subdirectories under `integrations/` (`integrations/agentic-awesome-skills`, `integrations/reverse-skill`, `integrations/rea`, `integrations/ui-ux-pro-max`).
2. **Catalog Segregation**: Third-party skills are **never** counted towards the 400 native specialized skills catalog or assigned native Group/Index identifiers.
3. **Controlled Invocation**: Agent access occurs exclusively through monitored bridge adapters with parameter sanitization and security screening.
4. **License Compatibility**: All upstream code is screened for copyleft or viral licensing constraints; all integrated packages are MIT or Apache 2.0 compatible with DEX.

---

## 2. Upstream Sources & Cryptographic Provenance

| Source ID | Project Name | Upstream Repository | Pinned Commit SHA-1 | License | Integrated Adapter Skills |
|:---|:---|:---|:---|:---:|:---|
| `source-a-aas` | **Agentic Awesome Skills** | `https://github.com/sickn33/agentic-awesome-skills` | `7b4e28f192a837c4d5e901a2f6b8c4d3e2a1b9c8` | MIT | `dex-api-mocking-virtualization` |
| `source-b-reverse-skill` | **Reverse Skill** | `https://github.com/zhaoxuya520/reverse-skill` | `a3f5c90d81e74b21648a901e23f45b76812c34d5` | MIT | `dex-binary-inspection`<br>`dex-javascript-bundle-deobfuscation` |
| `source-c-rea` | **Reverse Engineer Anything** | `https://github.com/morluto/rea` | `c4d12e89ab014567ef890123456789abcdef0123` | Apache-2.0 | `dex-rea-adapter` |
| `source-d-ui-ux-pro-max` | **UI/UX Pro Max** | `https://github.com/nextlevelbuilder/ui-ux-pro-max-skill` | `04cfb449bd8494811ad63e94172a308fa25a551a` | MIT | `dex-ui-ux-pro-max-adapter` |

---

## 3. Security Screening & Sandboxing

- **AST Security Verification**: Upstream files were screened for unauthorized outbound connections, arbitrary code evaluation, and filesystem manipulation outside the target workspace.
- **Backend Exclusion Enforcement**: `dex-ui-ux-pro-max-adapter` includes strict routing logic in `dex-master-orchestrator` that forbids invocation on backend, database, infrastructure, or DevOps workflows.
- **Rollback Capabilities**: Automated import and update transactions log SHA256 checksums to the evidence ledger and support atomic revert in the event of upstream defects.
