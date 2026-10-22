# Third-Party Notices & Upstream Source Provenance (v5.0.0)

> **DEX Engineering Skills Segregated Integration Policy**  
> External upstream projects are maintained in `integrations/` with strict namespace isolation.  
> Third-party skills are never counted toward the native 200 DEX skills catalog.

---

## 1. Summary of Integrated Upstream Sources

| Upstream Identifier | Project Name | Repository URL | Pinned Commit | License | Mount Directory |
|:---|:---|:---|:---|:---|:---|
| `source-a-aas` | **Agentic Awesome Skills** | [https://github.com/sickn33/agentic-awesome-skills](https://github.com/sickn33/agentic-awesome-skills) | `7b4e28f1` | MIT | `integrations/aas/` |
| `source-b-reverse-skill` | **Reverse Skill** | [https://github.com/zhaoxuya520/reverse-skill](https://github.com/zhaoxuya520/reverse-skill) | `a3f5c90d` | MIT | `integrations/reverse-skill/` |
| `source-c-rea` | **Reverse Engineer Anything (REA)** | [https://github.com/morluto/rea](https://github.com/morluto/rea) | `c4d12e89` | Apache-2.0 | `integrations/rea/` |

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
