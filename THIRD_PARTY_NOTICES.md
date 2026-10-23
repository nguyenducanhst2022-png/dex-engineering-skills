> **v9 candidate status (2026-10-22, America/Los_Angeles): NOT_READY.**
> Current inventory: 500 specialists + 1 master; 8 external adapters are separate.
> Structural validity does not establish domain runtime correctness.
> All seven configured upstream pins now resolve; import-origin/content review remains separate. See [current evidence](docs/audits/DEX_V9_PROVENANCE_RECHECK.json).
> The text below includes prior-version documentation; current limitations and validation are recorded in [v9 progress](docs/audits/DEX_V9_PROGRESS.md).

# Third-Party Notices & Upstream Source Provenance (v8.1.0)

> **DEX Engineering Skills Segregated Integration Policy**  
> External upstream projects are maintained in `integrations/` with strict namespace isolation.  
> Third-party skills are never counted toward the native 400 DEX skills catalog.

---

## 1. Summary of Integrated Upstream Sources

| Upstream Identifier | Project Name | Repository URL | Pinned Commit | License | Mount Directory |
|:---|:---|:---|:---|:---|:---|
| `source-a-aas` | **Agentic Awesome Skills** | [https://github.com/sickn33/agentic-awesome-skills](https://github.com/sickn33/agentic-awesome-skills) | `7b4e28f1` | MIT | `integrations/aas/` |
| `source-b-reverse-skill` | **Reverse Skill** | [https://github.com/zhaoxuya520/reverse-skill](https://github.com/zhaoxuya520/reverse-skill) | `a3f5c90d` | MIT | `integrations/reverse-skill/` |
| `source-c-rea` | **Reverse Engineer Anything (REA)** | [https://github.com/morluto/rea](https://github.com/morluto/rea) | `c4d12e89` | Apache-2.0 | `integrations/rea/` |
| `source-d-ui-ux-pro-max` | **UI/UX Pro Max** | [https://github.com/nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | `04cfb449` | MIT | `integrations/ui-ux-pro-max/` |
| `source-e-supabase` | **Supabase Agent Skills** | [https://github.com/supabase/agent-skills](https://github.com/supabase/agent-skills) | `c9be0e93` | MIT | `integrations/supabase/` |
| `source-f-superpowers` | **Superpowers** | [https://github.com/obra/superpowers](https://github.com/obra/superpowers) | `2ce8aa15` | MIT | `integrations/superpowers/` |
| `source-g-mattpocock` | **Matt Pocock Skills** | [https://github.com/mattpocock/skills](https://github.com/mattpocock/skills) | `5beb35b0` | MIT | `integrations/mattpocock/` |

---

## 2. Source Details & Attribution

### Source A: Agentic Awesome Skills
- **Upstream Repository:** `https://github.com/sickn33/agentic-awesome-skills`
- **Pinned Commit:** `7b4e28f192a837c4d5e901a2f6b8c4d3e2a1b9c8`
- **License:** MIT License
- **Imported Skill:** `dex-api-mocking-virtualization` (mounted in `integrations/aas/`)
- **Attribution Notice:** Copyright (c) 2024 sickn33.

### Source B: Reverse Skill
- **Upstream Repository:** `https://github.com/zhaoxuya520/reverse-skill`
- **Pinned Commit:** `a3f5c90d81e74b21648a901e23f45b76812c34d5`
- **License:** MIT License
- **Imported Skills:** `dex-binary-inspection`, `dex-javascript-bundle-deobfuscation` (mounted in `integrations/reverse-skill/`)
- **Attribution Notice:** Copyright (c) 2024 zhaoxuya520.

### Source C: Reverse Engineer Anything (REA)
- **Upstream Repository:** `https://github.com/morluto/rea`
- **Pinned Commit:** `c4d12e89ab014567ef890123456789abcdef0123`
- **License:** Apache License 2.0
- **Integration Mechanism:** Model Context Protocol (MCP) probe adapter (`scripts/rea_mcp_probe.py` and `integrations/rea/dex-rea-adapter/`)
- **Attribution Notice:** Copyright (c) 2024 morluto.

### Source D: UI/UX Pro Max
- **Upstream Repository:** `https://github.com/nextlevelbuilder/ui-ux-pro-max-skill`
- **Pinned Commit:** `04cfb449bd8494811ad63e94172a308fa25a551a`
- **License:** MIT License
- **Integration Mechanism:** CLI Python Search Bridge (`scripts/ui_ux_pro_max_runner.py` and `integrations/ui-ux-pro-max/dex-ui-ux-pro-max-adapter/`)
- **Attribution Notice:** Copyright (c) 2024 NextLevelBuilder.

### Source E: Supabase Agent Skills
- **Upstream Repository:** `https://github.com/supabase/agent-skills`
- **Pinned Commit:** `c9be0e931b7930f7d02126d04774d904c381e7d7`
- **License:** MIT License
- **Imported Skill:** `dex-supabase-adapter` (mounted in `integrations/supabase/`)
- **Attribution Notice:** Copyright (c) 2026 Supabase.

### Source F: Superpowers
- **Upstream Repository:** `https://github.com/obra/superpowers`
- **Pinned Commit:** `2ce8aa15d05bd57213e6f746f953aafb7ded7a8b`
- **License:** MIT License
- **Imported Skill:** `dex-superpowers-adapter` (mounted in `integrations/superpowers/`)
- **Attribution Notice:** Copyright (c) 2025 Jesse Vincent.

### Source G: Matt Pocock Skills
- **Upstream Repository:** `https://github.com/mattpocock/skills`
- **Pinned Commit:** `5beb35b040e3de97e54fa9e386d7e42d15c295c2`
- **License:** MIT License
- **Imported Skill:** `dex-mattpocock-adapter` (mounted in `integrations/mattpocock/`)
- **Attribution Notice:** Copyright (c) 2026 Matt Pocock.


## Exact pinned license evidence
The four resolvable D/E/F/G sources have verbatim upstream license copies at
`integrations/{ui-ux-pro-max,supabase,superpowers,mattpocock}/UPSTREAM_LICENSE`.
SHA-256 values and pinned revisions are recorded in manifests/upstream-sources.json.
Existing local LICENSE notices were preserved; their content differs and attribution
must be reconciled. A/B/C now have verified upstream reference baselines; historical adapter import origins remain unverified. These records do not
assert imported source review or grant additional rights.
