# DEX License Audit & Compatibility Assessment

**Date:** October 22, 2026  
**Auditor:** Principal AI Agent Architect & Legal Engineering Specialist  
**Standard:** Open Source Initiative (OSI) Compliance & Agent Skills Specification  

---

## 1. Executive Summary

This document evaluates the intellectual property rights, licenses, and redistribution obligations of all third-party repositories considered for ingestion into **DEX Engineering Skills**.

- **Source A (Agentic Awesome Skills):** MIT License (Permissive). 100% compatible with DEX.
- **Source B (Reverse Skill):** MIT License (Permissive). 100% compatible with DEX.
- **Source C (Reverse Engineer Anything - REA):** Apache 2.0 / MIT (Permissive). 100% compatible with DEX.

---

## 2. In-Depth License Compatibility Matrix

| Source Repository | Stated License | Commercial Use | Modification | Redistribution | Patent Grant | Attribution Required | Compatibility Status |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **sickn33/agentic-awesome-skills** | MIT | YES | YES | YES | Neutral | YES (Notice in file/docs) | **APPROVED** |
| **zhaoxuya520/reverse-skill** | MIT | YES | YES | YES | Neutral | YES (Notice in file/docs) | **APPROVED** |
| **morluto/rea** | Apache 2.0 / MIT | YES | YES | YES | Express | YES (Notice + Apache headers) | **APPROVED** |

---

## 3. Strict Compliance Obligations & Implementation

1. **Attribution Retention:**
   - Every imported skill must preserve the original author credit and license declaration in `data/imported_skills_manifest.json` and `THIRD_PARTY_NOTICES.md`.
2. **No License Viral Contamination:**
   - No GPL / AGPL copyleft skills are accepted into the DEX repository to prevent viral licensing obligations on user codebases.
3. **Patent Retaliation & Defenses:**
   - Source C's Apache 2.0 licensing grants explicit patent rights for contributors and users, shielding downstream adopters from patent infringement assertions regarding REA MCP tool schemas.

---

## 4. Rejection & Blacklist Criteria

The Skill Importer (`scripts/dex_skill_importer.py`) automatically rejects candidates if:
- Repository lacks an explicit OSI-approved license.
- Skill explicitly claims "All Rights Reserved" or "Proprietary Non-Commercial Use Only".
- Skill contains copyleft clauses (GPL-3.0, AGPL-3.0, SSPL) that conflict with permissive engineering reuse.
- Attribution headers have been stripped from upstream source files.
