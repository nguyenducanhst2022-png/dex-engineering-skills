---
name: dex-visual-asset-licensing
description: "Track licenses and attribution when selecting or redistributing icons, images, fonts and other visual assets."
---

# dex-visual-asset-licensing

## 1. Purpose & Scope
Maintain a verifiable ledger linking every shipped icon, image, font, illustration, and pattern to its license version, source evidence, permitted uses, and required attribution.

## 2. When to Use
- When adding a new icon set, stock photo, illustration pack, or web font to a repository or design system.
- When preparing a web, mobile, desktop, or marketing build that bundles or embeds third-party visual files.
- When replacing placeholder assets with final production assets before release.

## 3. When NOT to Use
- When reviewing source-code dependency licenses without any visual-asset component.
- When commissioning fully original in-house artwork where no third-party grant applies and ownership is documented elsewhere.
- When assessing patent, trademark clearance, or model-release privacy beyond copyright license tracking.

## 4. Prerequisites & Input Context
**Required inputs:**
- Complete asset inventory with file paths, SHA-256 hashes, creators, source URLs, and acquisition dates.
- License texts or snapshots for each asset, including version number and effective date.
- Intended distribution channels: SaaS UI, mobile bundle, desktop installer, NPM package, docs site, or print.

**Preconditions:**
- Read access to the asset repository and build output directory.
- Defined list of target platforms where embedding or redistribution will occur.
- A designated reviewer for ambiguous grants.

## 5. Core Concepts & Taxonomy
- **Provenance chain:** Author to distributor to project acquisition record, preserving the exact license version that applied at download time.
- **Grant dimensions:** Separate permissions for viewing, modifying, embedding in apps or PDFs, redistributing source files, and commercial use.
- **Font-specific constraints:** Desktop, webfont, app-embedding, ebook, and server licenses are distinct products with different fees.
- **Attribution obligation:** Required credit text, placement, and preservation of copyright notices and license copies.
- **Non-evidence signals:** Search-result previews, installed system fonts, Figma community duplicates, and AI-generated lookalikes confer no redistribution grant.
- **Failure modes:** Mixed-source folders inheriting the most permissive license, expired subscriptions, and seat-limited licenses exceeded by team size.

## 6. Step-by-Step Execution Workflow
1. Collect every candidate file: `find assets/ -type f \( -name "*.png" -o -name "*.svg" -o -name "*.jpg" -o -name "*.jpeg" -o -name "*.webp" -o -name "*.gif" -o -name "*.woff2" -o -name "*.woff" -o -name "*.ttf" -o -name "*.otf" \) -exec sha256sum {} \; > asset-hashes.txt`.
2. Capture source evidence per file: screenshot source page, save URL, download date, account or order ID, and license PDF in `licenses/<asset-id>/`.
3. Classify the grant: commercial allowed, modification allowed, redistribution allowed, embedding allowed, attribution required, share-alike triggered.
4. Check restrictions against the ship plan: webfont pageview caps, app-install limits, seat counts, trademark or logo-use bans, no-derivatives clauses.
5. Generate attribution strings and wire them into the product About screen, NOTICE file, and docs credits page.
6. Quarantine unresolved files in `assets/quarantine/`, substitute approved alternatives, then rebuild and verify no quarantined filename shipped: `find dist/ -path "*quarantine*" -print | grep . && echo "QUARANTINED FILES IN DIST" || echo "clean"`.
7. Freeze the final ledger as `ASSET_LICENSE_LEDGER.csv` with hash, version, grant summary, and reviewer sign-off.

## 7. Concrete Examples
### Ledger entry pattern:
```csv
asset_id,path,sha256_short,source,license,version,embedding,attribution
icon-arrow,assets/icons/arrow.svg,9f2c41ab,https://example-icons.com/pack-v3,CC-BY-4.0,4.0,no-embed-limit,"Arrow icons by Example Icons, CC-BY-4.0"
grotesk-regular,assets/fonts/grotesk-regular.woff2,vendor-portal-2026-03-14,Commercial-App-500k,2024-06,app-embed-500k-installs,"See LICENSES/grotesk.txt"
hero-photo,assets/images/hero.jpg,71bd0e22,stock-agency-order-88412,Standard-Royalty-Free,2025-01,web-only-500k-views,"Credited in NOTICE"
```

### Check commands:
- List embedded fonts in a PDF export: `pdffonts dist/report.pdf`
- List image assets bundled in a web build: `find dist/assets -type f | sort`
- Verify no quarantined hash ships (compare hash field only, where approved-hashes.txt contains bare SHA-256 hashes one per line): `sha256sum dist/assets/* | cut -d ' ' -f1 | grep -v -x -F -f approved-hashes.txt && echo "UNAPPROVED HASHES FOUND" || echo "all hashes approved"`
- Audit font license headers: `exiftool -Copyright -Rights -UsageTerms -License assets/fonts/*`

## 8. Anti-Patterns & Common Traps
- Treating royalty-free, free-download, or Creative-Commons-search-filtered as permission to modify and resell.
- Copying a single LICENSE file across a folder containing files from five different authors.
- Embedding a desktop-licensed font in a mobile app or EPUB because it renders correctly in Figma.
- Stripping EXIF, XMP, or SVG metadata that carried author and copyright fields.
- Assuming an expired stock subscription still covers new campaigns or new app versions.

## 9. Quality Gates & Acceptance Criteria
- QG-01: Every file in the shipped bundle has a matching hash entry in the ledger with zero unmapped files.
- QG-02: Each entry records license name, version, source URL or order ID, and acquisition date.
- QG-03: Attribution text renders in the product and in source distributions where the grant mandates it.
- QG-04: Files with ambiguous, expired, or seat-exceeded grants are quarantined and absent from `dist/`.
- QG-05: Ledger and NOTICE diff is reviewed and approved before release tagging.

## 10. Security & Safety Boundaries
- Redact order emails, invoices, and account identifiers before committing evidence to a shared repository.
- Store full purchase receipts in a restricted vault; commit only minimal proof references.
- Never download assets from untrusted mirrors to bypass paywalls or seat limits.
- Do not present ledger completion as legal advice or guaranteed clearance.

## 11. Platform Adapters
- **Web:** Record webfont pageview tier, subset files shipped, and self-host versus CDN license terms.
- **iOS / Android:** Record app-embedding addendum, install-count tier, and OS-specific font-rendering subset.
- **Desktop / Electron:** Record installer redistribution rights and bundled-resource disclosure path.
- **Docs / Marketing export:** Record print-run, broadcast, and merchandise exclusions separately from software use.

## 12. Deliverables & Output Artifacts
- `ASSET_LICENSE_LEDGER.csv` mapping shipped hashes to license versions and evidence paths.
- `NOTICE` or `ATTRIBUTION.md` with exact credit strings required by each grant.
- `licenses/` snapshot directory with source captures and license PDFs.
- Quarantine report listing replaced files, reasons, and substitute asset IDs.
- Build verification log showing bundle hash reconciliation output.

## 13. Related & Complementary Skills
- `dex-open-source-license-scanning`: Covers code dependency license detection that pairs with visual-asset tracking.
- `dex-third-party-attribution`: Standardizes credit-screen and NOTICE generation for mixed third-party content.
- `dex-upstream-license-diffing`: Detects license text changes on re-downloaded icon or font packs.
- `dex-sbom-verification`: Adds shipped-asset hashes to supply-chain bills of materials.

## 14. Realistic Usage Example
A marketing dashboard export bundles 240 Feather-style icons, a client logo, and Grotesk-Regular webfont. The ledger shows icons under MIT with preserved copyright header, the logo restricted to nominative use with no modification, and the font limited to 100k monthly pageviews. The font pageview cap is exceeded, so the team subsets the font, upgrades to the 500k tier, stores the order ID, updates `ATTRIBUTION.md`, rebuilds, and confirms the hash field of `sha256sum dist/assets/*` matches only approved hashes before tagging v2.14.
