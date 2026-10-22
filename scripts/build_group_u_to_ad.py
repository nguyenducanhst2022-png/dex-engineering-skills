# -*- coding: utf-8 -*-
"""
DEX SKILLOPS — MASTER BUILDER FOR GROUPS U TO AD (Skills 201–300)
Runs all 5 sub-builders in sequence to generate/update the 100 specialized skills for v6.0.
"""

import os
import sys
import subprocess

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPTS_DIR = os.path.join(ROOT, "scripts")

BUILDERS = [
    "build_group_u_v.py",
    "build_group_w_x.py",
    "build_group_y_z.py",
    "build_group_aa_ab.py",
    "build_group_ac_ad.py"
]

def main():
    if sys.stdout.encoding != "utf-8" and hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    print("=== DEX SKILLOPS — MASTER BUILDER (Skills 201–300: Groups U to AD) ===")
    for b in BUILDERS:
        script_path = os.path.join(SCRIPTS_DIR, b)
        print(f"\n--- Running {b} ---")
        result = subprocess.run([sys.executable, script_path], capture_output=True, text=True, encoding="utf-8")
        print(result.stdout)
        if result.returncode != 0:
            print(f"ERROR: {b} failed with code {result.returncode}")
            print(result.stderr)
            sys.exit(result.returncode)

    print("\n[SUCCESS] All 100 specialized skills (201–300) generated successfully.")

if __name__ == "__main__":
    main()
