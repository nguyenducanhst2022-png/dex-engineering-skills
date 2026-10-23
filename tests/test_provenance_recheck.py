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

def test_verified_reference_pin_does_not_authenticate_import(monkeypatch, tmp_path):
    import base64
    import hashlib
    license_bytes=b'MIT License\nFixture only\n'
    local=tmp_path/'UPSTREAM_LICENSE'
    local.write_bytes(license_bytes)
    sha='a'*40
    def fake_fetch(url):
        if '/commits/' in url:
            return {'http':200,'data':{'sha':sha}}
        return {'http':200,'data':{'encoding':'base64','content':base64.b64encode(license_bytes).decode(),'license':{'spdx_id':'MIT'}}}
    monkeypatch.setattr('scripts.verify_upstream_provenance.fetch', fake_fetch)
    result=inspect({'upstream_id':'fixture','repository_url':'https://github.com/example/test','pinned_commit':sha,'license_file':str(local),'pin_purpose':'UPSTREAM_REFERENCE_BASELINE'})
    assert result['pin_status']=='VERIFIED'
    assert result['license_at_pin_sha256']==hashlib.sha256(license_bytes).hexdigest()
    assert result['upstream_license_bytes_match'] is True
    assert result['import_origin_verification']=='NOT_VERIFIED'
    assert result['content_review']=='NOT_VERIFIED'


def test_replaced_source_pins_retain_history_and_exact_license_bytes():
    import hashlib
    from pathlib import Path
    root=Path(__file__).resolve().parents[1]
    sources=json.loads((root/'manifests/upstream-sources.json').read_text(encoding='utf-8'))['sources']
    evidence={r['id']:r for r in json.loads((root/'docs/audits/DEX_V9_PIN_CANDIDATES.json').read_text(encoding='utf-8'))}
    for source in sources[:3]:
        assert source['pinned_commit']==evidence[source['upstream_id']]['sha']
        assert source['pin_history'][-1]['pin_verification']=='UNRESOLVED'
        assert source['pin_purpose']=='UPSTREAM_REFERENCE_BASELINE'
        assert source['content_verification']=='NOT_VERIFIED'
        assert hashlib.sha256((root/source['upstream_license_file']).read_bytes()).hexdigest()==source['upstream_license_sha256']

def test_license_fallback_retains_api_failure(monkeypatch, tmp_path):
    sha='a'*40
    local=tmp_path/'LICENSE'
    local.write_bytes(b'MIT fixture')
    def fake_fetch(url):
        return {'http':200,'data':{'sha':sha}} if '/commits/' in url else {'http':403,'error':'rate limited'}
    monkeypatch.setattr('scripts.verify_upstream_provenance.fetch',fake_fetch)
    monkeypatch.setattr('scripts.verify_upstream_provenance.fetch_bytes',lambda url:{'http':200,'bytes':b'MIT fixture'})
    result=inspect({'upstream_id':'test','repository_url':'https://github.com/example/test','pinned_commit':sha,'license_file':str(local)})
    assert result['pin_status']=='VERIFIED'
    assert result['license_at_pin_http']==403
    assert result['license_fallback_http']==200
    assert result['license_at_pin_spdx'] is None
    assert result['license_bytes_match'] is True
    assert '/'+sha+'/LICENSE' in result['license_content_url']

def test_rate_limited_pin_uses_exact_patch_header(monkeypatch, tmp_path):
    sha='a'*40
    monkeypatch.setattr('scripts.verify_upstream_provenance.fetch',lambda url:{'http':403,'error':'rate limited'})
    monkeypatch.setattr('scripts.verify_upstream_provenance.fetch_commit_header',lambda url:{'http':200,'header':'From '+sha+' Mon Sep 17 00:00:00 2001'})
    monkeypatch.setattr('scripts.verify_upstream_provenance.fetch_bytes',lambda url:{'http':200,'bytes':b'MIT fixture'})
    result=inspect({'upstream_id':'test','repository_url':'https://github.com/example/test','pinned_commit':sha,'license_file':str(tmp_path/'absent')})
    assert result['pin_status']=='VERIFIED'
    assert result['pin_http']==403
    assert result['pin_verification_method']=='GITHUB_PATCH_EXACT_SHA'
    monkeypatch.setattr('scripts.verify_upstream_provenance.fetch_commit_header',lambda url:{'http':200,'header':'From '+'b'*40+' Mon Sep 17 00:00:00 2001'})
    assert inspect({'upstream_id':'test','repository_url':'https://github.com/example/test','pinned_commit':sha,'license_file':str(tmp_path/'absent')})['pin_status']=='UNRESOLVED'
