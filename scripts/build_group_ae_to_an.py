# -*- coding: utf-8 -*-
"""
DEX ENGINEERING SKILLS FRAMEWORK v8.0 — MASTER BUILDER
Sequentially executes all 5 group builders (AE to AN, Skills 301–400)
and verifies the native skill count reaches exactly 401.
"""

import os
import sys
import subprocess

if sys.stdout.encoding != "utf-8" and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SKILLS_DIR = os.path.join(ROOT, ".agents", "skills")

BUILDERS = [
    "scripts/build_group_ae_af.py",
    "scripts/build_group_ag_ah.py",
    "scripts/build_group_ai_aj.py",
    "scripts/build_group_ak_al.py",
    "scripts/build_group_am_an.py",
]

def run_master_build():
    print("=================================================================")
    print("DEX ENGINEERING SKILLS FRAMEWORK v8.0 — MASTER GENERATOR")
    print("Generating Skills 301–400 (Groups AE to AN)")
    print("=================================================================\n")

    for builder in BUILDERS:
        builder_path = os.path.join(ROOT, builder)
        print(f"--> Executing: {builder}")
        res = subprocess.run([sys.executable, builder_path], cwd=ROOT)
        if res.returncode != 0:
            print(f"ERROR: {builder} failed with returncode {res.returncode}")
            sys.exit(res.returncode)
        print()

    # Verify count
    dirs = [d for d in os.listdir(SKILLS_DIR) if os.path.isdir(os.path.join(SKILLS_DIR, d))]
    count = len(dirs)
    print(f"=================================================================")
    print(f"TOTAL NATIVE SKILLS ON DISK: {count} (Target: 401)")
    print(f"=================================================================")

    if count != 401:
        print(f"ERROR: Expected 401 native skills, found {count}!")
        sys.exit(1)
    else:
        print("PASS: Exactly 401 native skills present (1 Master Orchestrator + 400 Specialized).")

if __name__ == "__main__":
    run_master_build()
