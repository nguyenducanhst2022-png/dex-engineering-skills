# v9 upstream license and provenance audit

Current license metadata is discovery evidence, not an approval of imported content. License text, copyright and imported-file hashes at each pinned revision need reconciliation. No source was imported or repinned.

| Source | Pin resolution | Current license metadata | Local license file |

|---|---|---|---|

| source-a-aas | FAIL / unresolved | MIT | False |

| source-b-reverse-skill | FAIL / unresolved | MIT | False |

| source-c-rea | FAIL / unresolved | MIT | False |

| source-d-ui-ux-pro-max | PASS | MIT | True |

| source-e-supabase | PASS | MIT | True |

| source-f-superpowers | PASS | MIT | True |

| source-g-mattpocock | PASS | MIT | True |



Sources A/B/C returned HTTP 422 for configured commit lookups; D/E/F/G resolved. HTTP failure is evidence that this lookup failed, not proof of why the pin is invalid. Current repository license metadata does not prove the license at a pinned revision. All seven sources still need complete content, package and executable review.

Raw HTTP evidence: DEX_V9_UPSTREAM_EVIDENCE.json.


## Current correction checkpoint ? 2026-10-22

Current recheck: DEX_V9_PROVENANCE_RECHECK.json records license hashes at exact resolved pins, rather than current HEAD license metadata. Existing D/E/F/G local license bytes differ; exact upstream copies are now retained separately as UPSTREAM_LICENSE with hashes in the source manifest. Original notices were preserved rather than silently replaced. A/B/C have no license evidence at their unresolved configured pins. Content-level attribution is still not verified. No pin was silently repointed and no source code was imported.


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
