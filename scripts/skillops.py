"""Read-only SkillOps evidence, exposed through the existing dex entrypoint."""
import json
from pathlib import Path
from scripts.validate_skills import validate_skill


def audit(root):
    root = Path(root).resolve()
    target = json.loads((root / 'manifests/native-skills.json').read_text(encoding='utf-8'))
    expected = {x['id'] for x in target['skills']}
    base = root / '.agents/skills'
    actual = {p.name for p in base.iterdir() if p.is_dir()}
    errors = {name: validate_skill(str(base / name), name) for name in sorted(actual)}
    errors = {k: v for k, v in errors.items() if v}
    missing = sorted(expected - actual)
    unexpected = sorted(actual - expected)
    catalog = json.loads((root / 'manifests/dex-skills.json').read_text(encoding='utf-8'))
    discovered = [x['id'] for x in catalog['native_skills']]
    synchronized = len(discovered) == len(set(discovered)) and set(discovered) == actual
    count_ok = len(actual) == target['target_native'] and not missing and not unexpected
    return {
        'target_version': target['target_version'], 'target_native': target['target_native'],
        'native_specialized': len(actual - {'dex-master-orchestrator'}),
        'master_orchestrators': int('dex-master-orchestrator' in actual),
        'external_adapters': len(list((root / 'integrations').rglob('SKILL.md'))),
        'runtime_verified': None, 'runtime_state': 'NOT_VERIFIED',
        'structurally_valid': len(actual) - len(errors), 'invalid_skills': errors,
        'missing_target_skills': missing, 'unexpected_skills': unexpected,
        'catalog_synchronized': synchronized,
        'release_count_gate': 'PASS' if count_ok else 'FAIL',
        'structural_gate': 'PASS' if not errors and count_ok and synchronized else 'FAIL',
        'release': 'NOT_READY',
        'release_blockers': ['Domain runtime and cross-host evaluation not completed',
                             'Upstream provenance and licensing require completed review',
                             'Semantic routing and independent technical content review incomplete'],
    }


def run(args):
    result = audit(args.cwd)
    if args.skills_command == 'plan':
        result = {k: result[k] for k in ('target_version', 'missing_target_skills', 'release_blockers')}
    print(json.dumps(result, indent=2) if args.format == 'json' else '\n'.join(f'{k}: {v}' for k, v in result.items()))
    if args.skills_command == 'validate':
        return 0 if result['structural_gate'] == 'PASS' else 1
    if args.skills_command == 'report':
        return 0 if result['release'] == 'READY' else 1
    return 0
