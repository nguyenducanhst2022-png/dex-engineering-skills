#!/usr/bin/env python3
"""Flag thin SKILL.md files.

A sentence counts as "own content" when it is not the description, is not
repeated elsewhere in the same skill, and is not shared boilerplate (a
sentence appearing in more than BOILERPLATE_RATIO of all skills).

Default mode only reports (exit 0). Use --strict to fail when any skill has
fewer than --min-own sentences or repeats its description in the body.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / ".agents" / "skills"
BOILERPLATE_RATIO = 0.10
SENT_SPLIT = re.compile(r"(?<=[.!?])\s+")
NUMBERED = re.compile(r"^\d+\.\s+")


def parse(path: Path) -> tuple[str, list[str]]:
    text = path.read_text(encoding="utf-8")
    desc = ""
    body = text
    if text.startswith("---"):
        _, fm, body = text.split("---", 2)
        m = re.search(r'^description:\s*"?(.*?)"?\s*$', fm, re.M)
        desc = m.group(1).strip() if m else ""
    sentences: list[str] = []
    for line in body.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        line = NUMBERED.sub("", line)
        sentences.extend(s.strip() for s in SENT_SPLIT.split(line) if s.strip())
    return desc, sentences


def norm(s: str) -> str:
    return re.sub(r"\W+", " ", s.lower()).strip()


def analyze(skills_dir: Path) -> list[dict]:
    parsed = {p.parent.name: parse(p) for p in sorted(skills_dir.glob("*/SKILL.md"))}
    df = Counter()
    for _, sents in parsed.values():
        df.update({norm(s) for s in sents})
    limit = max(2, int(len(parsed) * BOILERPLATE_RATIO))
    results = []
    for name, (desc, sents) in parsed.items():
        counts = Counter(norm(s) for s in sents)
        d = norm(desc)
        own = {
            k for k, c in counts.items()
            if c == 1 and k != d and df[k] <= limit and k != norm(name)
        }
        results.append({
            "skill": name,
            "own_sentences": len(own),
            "repeats_description": bool(d) and counts.get(d, 0) > 0,
            "repeated_sentences": sum(1 for c in counts.values() if c > 1),
        })
    return results


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--min-own", type=int, default=25)
    ap.add_argument("--strict", action="store_true")
    ap.add_argument("--format", choices=["text", "json"], default="text")
    ap.add_argument("--skills-dir", type=Path, default=SKILLS_DIR)
    args = ap.parse_args()

    results = analyze(args.skills_dir)
    thin = [r for r in results if r["own_sentences"] < args.min_own or r["repeats_description"]]
    if args.format == "json":
        print(json.dumps({"total": len(results), "flagged": thin}, indent=2))
    else:
        for r in thin:
            print(f"THIN {r['skill']}: own={r['own_sentences']} "
                  f"repeats_description={r['repeats_description']} "
                  f"repeated={r['repeated_sentences']}")
        print(f"{len(thin)}/{len(results)} skills flagged (min-own={args.min_own})")
    return 1 if (args.strict and thin) else 0


if __name__ == "__main__":
    sys.exit(main())
