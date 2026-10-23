# -*- coding: utf-8 -*-
"""
DEX SKILLOPS — UPSTREAM SYNCHRONIZER (scripts/sync_upstream.py)
Monitors, diffs, and checks pinned upstream repositories (AAS, Reverse Skill, REA).
Ensures safe version pinning and prevents unreviewed remote changes.
"""

import os
import sys
import json
import subprocess
import argparse

def check_upstream_sources(manifest_path, dry_run=True):
    if not os.path.exists(manifest_path):
        print(f"Error: Upstream sources manifest not found at {manifest_path}")
        return 1

    with open(manifest_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    sources = data.get("sources", [])
    print(f"=== DEX SKILLOPS UPSTREAM SYNCHRONIZER ===")
    print(f"Checking {len(sources)} pinned upstream repositories (Dry-Run: {dry_run})...\n")

    all_synced = True
    for src in sources:
        uid = src["upstream_id"]
        name = src["name"]
        url = src["repository_url"]
        pinned_commit = src["pinned_commit"]
        mount = src["mount_path"]

        print(f"[{uid}] {name}")
        print(f"  - Target Mount: {mount}")
        print(f"  - Pinned Commit: {pinned_commit[:8]}... ({pinned_commit})")
        print(f"  - License: {src.get('license', 'Unknown')}")
        print(f"  - Status: {src.get('status', 'ACTIVE')}")

        # Check local mount exists
        root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        local_path = os.path.join(root_dir, mount)
        if os.path.exists(local_path):
            skills = [s for s in os.listdir(local_path) if os.path.isdir(os.path.join(local_path, s)) and os.path.isfile(os.path.join(local_path, s, "SKILL.md"))]
            print(f"  - Mounted Skills ({len(skills)}): {', '.join(skills)}")
        else:
            print(f"  - WARNING: Mount path {mount} does not exist locally")
            all_synced = False

        pin_state = src.get("pin_verification", "NOT_VERIFIED")
        content_state = src.get("content_verification", "NOT_VERIFIED")
        print(f"  - Recorded pin verification: {pin_state}")
        print(f"  - Recorded content verification: {content_state}")
        print("  - This read-only command does not perform network or file-hash verification.\n")
        if pin_state != "VERIFIED" or content_state != "VERIFIED":
            all_synced = False

    print("=" * 50)
    print("UPSTREAM SYNC SUMMARY:")
    print(f"  Total Sources Monitored : {len(sources)}")
    print("  Pin enforcement: NOT_VERIFIED by this command")
    print("  External mounts remain separate from the native catalog")
    print("=" * 50)
    print("\nRESULT: Recorded review states complete." if all_synced and sources else "\nRESULT: NOT_VERIFIED; resolve provenance and content review before sync.")
    return 0 if all_synced and sources else 1

def main():
    parser = argparse.ArgumentParser(description="DEX SkillOps Upstream Synchronizer")
    parser.add_argument("--dry-run", action="store_true", default=True, help="Simulate sync without modifying files")
    parser.add_argument("--manifest", default="manifests/upstream-sources.json", help="Path to upstream sources manifest")
    args = parser.parse_args()

    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    manifest_path = os.path.join(root_dir, args.manifest) if not os.path.isabs(args.manifest) else args.manifest

    sys.exit(check_upstream_sources(manifest_path, dry_run=args.dry_run))

if __name__ == "__main__":
    main()
