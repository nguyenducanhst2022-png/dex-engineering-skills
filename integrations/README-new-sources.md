# Upstream Sources E, F & G Integration Guide (v8.1.0)

> **Document Scope:** Architecture, usage triggers, runtime requirements, duplicate resolution, and security boundaries for the three new upstream repositories integrated into the DEX Engineering Skills Framework v8.1:
> - **Source E:** Supabase Agent Skills (`supabase/agent-skills`)
> - **Source F:** Superpowers (`obra/superpowers`)
> - **Source G:** Matt Pocock Skills (`mattpocock/skills`)

---

## 1. Upstream Source Provenance Summary

| Source Identifier | Source Name | Repository URL | Pinned Commit SHA | License | Isolated Adapter Path |
|:---|:---|:---|:---|:---|:---|
| `source-e-supabase` | **Supabase Agent Skills** | [https://github.com/supabase/agent-skills](https://github.com/supabase/agent-skills) | `c9be0e931b7930f7d02126d04774d904c381e7d7` | MIT | `integrations/supabase/dex-supabase-adapter/` |
| `source-f-superpowers` | **Superpowers** | [https://github.com/obra/superpowers](https://github.com/obra/superpowers) | `2ce8aa15d05bd57213e6f746f953aafb7ded7a8b` | MIT | `integrations/superpowers/dex-superpowers-adapter/` |
| `source-g-mattpocock` | **Matt Pocock Skills** | [https://github.com/mattpocock/skills](https://github.com/mattpocock/skills) | `5beb35b040e3de97e54fa9e386d7e42d15c295c2` | MIT | `integrations/mattpocock/dex-mattpocock-adapter/` |

---

## 2. Integration Architecture & Orchestrator Control Plane

All third-party capabilities reside strictly inside `integrations/` and do not alter the native 401 skills count (400 specialized skills + 1 orchestrator).

```
                      +---------------------------------------+
                      |       DEX MASTER ORCHESTRATOR         |
                      |          (Root Control Plane)         |
                      +-------------------+-------------------+
                                          |
        +---------------------------------+---------------------------------+
        |                                                                   |
+-------v-------------------------+                       +-----------------v------------------+
|   Native DEX Skills (001-400)   |                       |    Segregated Integrations (8)     |
|   - Groups A to AN              |                       |    - Sources A, B, C, D            |
|   - dex-database-engineering    |                       |    - dex-supabase-adapter (Source E)|
|   - dex-development-workflow    |<--- Complementary --->|    - dex-superpowers-adapter (Src F)|
|   - dex-root-cause-debugging    |                       |    - dex-mattpocock-adapter (Src G)|
+---------------------------------+                       +------------------------------------+
```

### Architectural Guardrails:
1. **DEX Master Orchestrator Supremacy**: External meta-routers (e.g., `using-superpowers`) are prohibited from intercepting root prompts. The DEX Master Orchestrator parses user intents, selects execution modes (`QUICK`, `STANDARD`, `STRICT`), and delegates tasks to adapters only when appropriate.
2. **Deterministic Fallbacks (Zero Hallucination)**: When external command-line tools (`supabase` CLI, specific Git worktree configurations, or Claude plugins) are unavailable on the host, adapters gracefully fall back to pure static analysis and standard local Git branching without halting.
3. **Strict License Attribution**: All upstream code, concepts, and structures retain their original MIT license notices and copyright statements (Supabase: Copyright (c) 2026 Supabase; Superpowers: Copyright (c) 2025 Jesse Vincent; Matt Pocock: Copyright (c) 2026 Matt Pocock).

---

## 3. Individual Source Technical Details

### Source E: Supabase Agent Skills (`dex-supabase-adapter`)
- **Core Domain:** BaaS PostgreSQL, Row-Level Security (RLS) hardening, connection pooling (Supavisor / PgBouncer), and Serverless Edge Function database transactions.
- **Trigger Conditions:** Requests involving Supabase schema design, RLS policy audits, multi-tenant database isolation, `(select auth.uid())` subquery optimization, or connection exhaustion errors on port 5432/6543.
- **When NOT to Use:** Non-PostgreSQL / NoSQL projects, purely visual frontend tasks, binary reverse engineering.
- **Runtime Checks:**
  ```bash
  supabase --version
  ```
  Fallback: Generates validated idempotent SQL migrations (`.sql`) for manual execution via Supabase Studio SQL Editor.

---

### Source F: Superpowers (`dex-superpowers-adapter`)
- **Core Domain:** Disciplined TDD loops (Red-Green-Refactor), systematic defect isolation, atomic checklist plan execution, and Git worktree isolation.
- **Trigger Conditions:** Requests requiring strict TDD cycles, complex multi-step plan tracking with verification checkpoints, or isolated branch worktrees.
- **When NOT to Use:** Quick one-line bugfixes (`QUICK MODE`), CI/CD environments without worktree permissions, prompt-interception attempts.
- **Runtime Checks:**
  ```bash
  git --version
  git worktree list
  ```
  Fallback: Standard local Git branch isolation (`git checkout -b <branch>`).

---

### Source G: Matt Pocock Skills (`dex-mattpocock-adapter`)
- **Core Domain:** Developer-agent interaction protocols, hypothesis-driven bug diagnosis, specification-to-ticket breakdown (`to-tickets`), and structured session handoff contracts (`handoff.md`).
- **Trigger Conditions:** Elusive, hard-to-reproduce bugs requiring a minimal reproduction harness, decomposing PRDs into bite-sized developer tickets, or preserving agent mental state across sessions.
- **When NOT to Use:** Database schema tuning, UI CSS token styling, binary inspection.
- **Runtime Checks:** Pure Markdown Universal Protocol; requires zero external binaries, completely self-contained.

---

## 4. Verification & Testing

Every adapter is validated against the **Agent Skills Specification** and the 14 mandatory section requirements:
```powershell
# 1. Run zero-dependency specification validator (401 native + 8 integrations)
python scripts/validate_pack.py

# 2. Run dedicated external sources test suite
pytest tests/test_external_sources_efg.py -v

# 3. Run full regression test suite
pytest tests/ -v
```
