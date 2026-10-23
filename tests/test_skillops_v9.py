import json
from pathlib import Path
import pytest
from scripts.skillops import audit

ROOT = Path(__file__).resolve().parents[1]

@pytest.fixture
def mini_repo(tmp_path):
    (tmp_path/'manifests').mkdir()
    (tmp_path/'integrations').mkdir()
    skill=tmp_path/'.agents/skills/dex-master-orchestrator'
    skill.mkdir(parents=True)
    (skill/'SKILL.md').write_text((ROOT/'.agents/skills/dex-master-orchestrator/SKILL.md').read_text(encoding='utf-8'),encoding='utf-8')
    target={'target_version':'9.0.0','target_native':2,'skills':[{'id':'dex-master-orchestrator'},{'id':'dex-missing-specialist'}]}
    (tmp_path/'manifests/native-skills.json').write_text(json.dumps(target),encoding='utf-8')
    (tmp_path/'manifests/dex-skills.json').write_text(json.dumps({'native_skills':[{'id':'dex-master-orchestrator'}]}),encoding='utf-8')
    return tmp_path

def test_incomplete_target_fails(mini_repo):
    result=audit(mini_repo)
    assert result['release_count_gate']=='FAIL'
    assert result['missing_target_skills']==['dex-missing-specialist']
    assert result['release']=='NOT_READY'

def test_extra_directory_cannot_substitute_for_missing_skill(mini_repo):
    (mini_repo/'.agents/skills/dex-unexpected').mkdir()
    result=audit(mini_repo)
    assert result['release_count_gate']=='FAIL'
    assert result['unexpected_skills']==['dex-unexpected']
    assert 'dex-unexpected' in result['invalid_skills']

def test_duplicate_discovery_is_not_synchronized(mini_repo):
    p=mini_repo/'manifests/dex-skills.json'
    p.write_text(json.dumps({'native_skills':[{'id':'dex-master-orchestrator'}]*2}),encoding='utf-8')
    assert not audit(mini_repo)['catalog_synchronized']

def test_metadata_does_not_claim_runtime_success():
    result=audit(ROOT)
    assert result['structural_gate']=='PASS'
    assert result['runtime_verified'] is None
    assert result['runtime_state']=='NOT_VERIFIED'
    assert result['release']=='NOT_READY'

def test_canonical_identifiers_are_unique():
    data=json.loads((ROOT/'manifests/native-skills.json').read_text(encoding='utf-8'))
    entries=data['skills']
    assert {x['index'] for x in entries}==set(range(data['target_native']))
    assert len({x['id'] for x in entries})==data['target_native']
