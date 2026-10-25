import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import check_skill_depth as csd  # noqa: E402


def _skill(root, name, desc, body):
    d = root / name
    d.mkdir()
    (d / "SKILL.md").write_text(f'---\nname: {name}\ndescription: "{desc}"\n---\n{body}', encoding="utf-8")


def test_flags_repeated_description_and_counts_own(tmp_path):
    _skill(tmp_path, "thin", "Do the thing.", "# thin\n## When\nDo the thing.\nOnly once here.\n")
    _skill(tmp_path, "rich", "Rich skill.", "# rich\n" + "\n".join(f"Fact number {i}." for i in range(30)))
    res = {r["skill"]: r for r in csd.analyze(tmp_path)}
    assert res["thin"]["repeats_description"] is True
    assert res["thin"]["own_sentences"] == 1
    assert res["rich"]["repeats_description"] is False
    assert res["rich"]["own_sentences"] == 30


def test_repo_runs_report_only():
    assert csd.main.__name__ == "main"
    assert len(csd.analyze(csd.SKILLS_DIR)) > 0
