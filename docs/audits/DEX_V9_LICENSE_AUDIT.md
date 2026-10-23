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
