---
name: dex-ux-design-research-synthesis
description: "Synthesize interview and usability evidence when identifying product problems; preserve contradictory findings and sampling uncertainty."
---

# dex-ux-design-research-synthesis

## 1. Purpose & Scope
Turn raw interview transcripts, usability observations, and support tickets into defensible themes, opportunity statements, and confidence-graded findings. Covers affinity coding, theme-matrix construction, contradiction preservation, and prioritization for product discovery. Does not cover statistical A/B design, survey sampling theory, or implementation of experiments and UI fixes.

## 2. When to Use
- After 5-12 semi-structured interviews or 5-8 moderated usability sessions when patterns are unclear.
- When stakeholders cite conflicting quotes and need a single traceable synthesis.
- When preparing discovery readout, problem framing, or roadmap input that must show evidence strength.
- When prior research exists and needs consolidation without losing minority views.

## 3. When NOT to Use
- Do not use to validate a shipped metric change; use experimentation and analytics skills instead.
- Do not use for pure market sizing, pricing analysis, or large-N survey inference.
- Do not use when no raw evidence exists yet; collect transcripts or session notes first.
- Do not use to write final PRDs or pixel specs; synthesis stops at prioritized opportunities.

## 4. Prerequisites & Input Context
- 5+ consented transcripts or notes with participant IDs, task context, and timestamps.
- Research questions, participant screener, and segment definitions.
- Usability task scripts, success criteria, and observer notes if applicable.
- Sampling frame and known gaps: recruited segments, dropouts, recruitment source.
- Tooling: spreadsheet or Dovetail / EnjoyHQ / Miro, plus a folder for anonymized excerpts.

## 5. Core Concepts & Taxonomy
- Observation: verbatim action or quote with ID, e.g., P04 failed to find promo field at checkout.
- Interpretation: hypothesized need or mental model inferred from one or more observations.
- Theme: recurring interpretation across participants and segments, supported by distinct IDs.
- Negative case: observation that contradicts a candidate theme and must be retained.
- Evidence strength: function of participant diversity, task realism, and convergence across methods.
- Severity vs. frequency: task-blocking impact scored independently from how many reported it.

## 6. Step-by-Step Execution Workflow
1. Sanitize and index: assign P01, P02 IDs and U01 session IDs, strip names and contacts, store mapping separately. Verify: `grep -r -i -E "gmail|@company|phone|\+[0-9]{7,}" ./notes/ || echo clean`.
2. Open-code 3 transcripts line-by-line with gerund labels like struggling-to-compare-plans, then freeze a draft codebook with definitions and exclusions.
3. Apply codebook to remaining transcripts in a participant-by-theme matrix; one row per participant, one column per code, cell holds excerpt ID.
4. Hold a 30-minute reconciliation on 20% overlap-coded material; compute simple agreement, keep disagreements as dual codes.
5. Cluster into candidate themes by user goal and segment, deliberately attach 1-2 conflicting excerpts to each theme.
6. Score opportunities with impact x evidence: task blockage 1-3, affected segments count, cross-method support. Sort, do not average away dissent.
7. Draft finding cards: claim, supporting IDs, contradicting IDs, segment limits, proposed follow-up test.

## 7. Concrete Examples
Finding card:
`[F-03] Checkout promo confusion — 4/8 (P02,P04,P06,P08) hesitated >40s or entered code in search box; P05 succeeded via help article. Confidence: Medium, convenience sample, first-time buyers only. Follow-up: tree test with relocated field.`

Check commands:
```bash
ls ./evidence/transcripts/P*.md | wc -l
rg -c "P0[0-9]" ./synthesis/theme-matrix.csv
rg "CONTRADICTS|NEGATIVE-CASE" ./synthesis/findings.md
```

Codebook entry:
`COMPARE-PLANS: participant attempts side-by-side evaluation. Include: toggling tabs. Exclude: price complaint without comparison.`

## 8. Anti-Patterns & Common Traps
- Treating one talkative participant with five quotes as five independent votes.
- Promoting vivid anecdotes over repeated task failures because the story is memorable.
- Collapsing stated satisfaction scores and observed completion into a single rating.
- Reporting raw counts as population percentages without confidence intervals or sampling caveats.
- Discarding inconvenient transcripts to make themes look cleaner.
- Presenting affinity clusters as proof of causality or demand.

## 9. Quality Gates & Acceptance Criteria
- Every theme links to 2+ distinct participant IDs and at least one raw excerpt ID.
- Contradictory evidence is explicitly labeled and preserved in the matrix.
- Sampling limits, segment coverage, and untested tasks are stated on the readout cover.
- A peer can pick two themes and locate the source excerpts in under 5 minutes.
- No causal language remains unless paired with a proposed falsification test.
- Prioritized opportunities each name owner, next method, and evidence gap.

## 10. Security & Safety Boundaries
- Work only from consented or synthetic data; never publish raw audio, names, or contact details.
- Redact direct identifiers, employer names, and sensitive disclosures before sharing beyond the research team.
- Store consent forms and de-identification keys separately with restricted access.
- Do not paste participant data into unapproved public tools; use project-approved toolchain.
- Review external readouts for re-identification risk when N is small or context is unique.

## 11. Platform Adapters
- Local markdown + CSV workflow: VS Code, Obsidian, or Excel; version with git.
- Dovetail / EnjoyHQ / Condens: import anonymized transcripts, export codebook CSV for audit.
- Miro / FigJam: affinity board must export to archived PNG + CSV backup, not board-only.
- If no tooling available, use `theme-matrix.csv` template and `findings.md` cards; record tool versions in methods note.

## 12. Deliverables & Output Artifacts
- Anonymized excerpt log with stable IDs and segment tags.
- Codebook v1.0 with definitions, inclusions, and exclusions.
- Participant-by-theme matrix in CSV with supporting and conflicting IDs.
- Finding cards with confidence, limits, and follow-up proposals.
- Prioritized opportunity list ranked by task impact and evidence strength.
- Methods appendix: recruitment source, dropout count, untested environments.

## 13. Related & Complementary Skills
- `dex-usability-study-design`: Provides task scripts and observation protocols that feed synthesis input.
- `dex-user-journey-mapping`: Turns synthesized themes into journey pain points and moments.
- `dex-product-discovery`: Uses ranked opportunities to frame bets and problem statements.
- `dex-grounding-citation-audit`: Verifies every claim traces to an excerpt ID without fabrication.
- `dex-design-critique-rubric`: Supplies structured lens for reviewing proposed fixes from findings.

## 14. Realistic Usage Example
Checkout discovery with 8 first-time buyers, 3 failures on promo-code entry. Build matrix, keep P05 success as negative case, score promo confusion high-impact / medium-evidence. Deliver F-03 card with IDs P02,P04,P06,P08 supporting and P05 contradicting, note convenience sample and desktop-only coverage, propose unmoderated tree test of two field placements before engineering.
