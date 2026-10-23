import json
from scripts.sync_upstream import check_upstream_sources
from scripts.verify_upstream_provenance import inspect


def test_sync_does_not_trust_legacy_active_verified(tmp_path, capsys):
    p=tmp_path/'sources.json'
    p.write_text(json.dumps({'sources':[{'upstream_id':'test','name':'test','repository_url':'https://example.test','pinned_commit':'a'*40,'mount_path':'integrations','status':'ACTIVE_VERIFIED'}]}))
    assert check_upstream_sources(str(p)) == 1
    assert 'RESULT: NOT_VERIFIED' in capsys.readouterr().out


def test_provenance_requires_exact_resolved_sha(monkeypatch):
    monkeypatch.setattr('scripts.verify_upstream_provenance.fetch', lambda url: {'http':200,'data':{'sha':'b'*40}})
    result=inspect({'upstream_id':'test','repository_url':'https://github.com/example/test','pinned_commit':'a'*40,'license_file':'does-not-exist'})
    assert result['pin_status']=='UNRESOLVED'
    assert result['content_review']=='NOT_VERIFIED'
    assert not result['import_performed']
