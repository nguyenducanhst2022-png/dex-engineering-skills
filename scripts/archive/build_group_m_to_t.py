# -*- coding: utf-8 -*-
"""
Master runner for generating all 80 new specialized skills (121-200) across Groups M through T.
"""

import subprocess
import sys

def main():
    scripts = [
        "scripts/build_group_m_n.py",
        "scripts/build_group_o_p.py",
        "scripts/build_group_q_r.py",
        "scripts/build_group_s_t.py"
    ]
    for s in scripts:
        print(f"\n--- Running {s} ---")
        res = subprocess.run([sys.executable, s])
        if res.returncode != 0:
            print(f"FAILED: {s}")
            sys.exit(res.returncode)
    print("\nALL 80 NEW SKILLS (121-200) SUCCESSFULLY GENERATED!")

if __name__ == "__main__":
    main()
