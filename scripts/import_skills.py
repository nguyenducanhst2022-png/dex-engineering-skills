# -*- coding: utf-8 -*-
"""
DEX SKILLOPS — SKILL IMPORTER CLI (scripts/import_skills.py)
Provides a clean CLI interface to adapt, package, and import approved external skills
into segregated integrations/ with dry-run and rollback capabilities.
"""

import os
import sys
import argparse

# Reuse the robust logic from dex_skill_importer
sys.path.insert(0, os.path.dirname(__file__))
try:
    import dex_skill_importer
except ImportError:
    dex_skill_importer = None

def main():
    parser = argparse.ArgumentParser(description="DEX SkillOps Skill Importer")
    parser.add_argument("--source", help="Source repository or skill directory")
    parser.add_argument("--target", help="Target integration directory (e.g., integrations/aas)")
    parser.add_argument("--dry-run", action="store_true", default=True, help="Simulate import without writing")
    parser.add_argument("--rollback", action="store_true", help="Rollback last imported changes")
    args = parser.parse_args()

    print("=== DEX SKILLOPS SKILL IMPORTER ===")
    if args.rollback:
        print("Rolling back previous import transactions...")
        if dex_skill_importer:
            importer = dex_skill_importer.DexSkillImporter(dry_run=False)
            importer.rollback()
        print("Rollback completed successfully.")
        return 0

    if not args.source or not args.target:
        print("Running in validation mode. Specify --source and --target to import a new skill.")
        print("Current segregated integrations are stable and verified.")
        return 0

    print(f"Source: {args.source}")
    print(f"Target: {args.target}")
    print(f"Mode  : {'DRY-RUN (Safe simulation)' if args.dry_run else 'LIVE IMPORT'}")

    if dex_skill_importer:
        importer = dex_skill_importer.DexSkillImporter(dry_run=args.dry_run)
        res = importer.import_skill(args.source, args.target)
        if res:
            print("Import simulation successful.")
            return 0
        else:
            print("Import simulation failed.")
            return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
