# -*- coding: utf-8 -*-
"""
Master generator for Group J (91-100), Group K (101-110), and Group L (111-120).
Total: 30 Specialized Skills for DEX Engineering Skills Pack v4.0.
"""

import sys
import os

# Add scripts directory to path
sys.path.insert(0, os.path.dirname(__file__))

import build_group_j
import build_group_k
import build_group_l

def main():
    print("=== DEX v4.0: BUILDING GROUPS J, K, L (30 NEW SKILLS) ===")
    build_group_j.main()
    print("-" * 50)
    build_group_k.main()
    print("-" * 50)
    build_group_l.main()
    print("=" * 50)
    print("All 30 skills (Groups J, K, L) built successfully!")

if __name__ == "__main__":
    main()
