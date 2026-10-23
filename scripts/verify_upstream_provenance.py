"""Inspect exact upstream pins and license evidence without importing or executing content."""
import argparse
import base64
import concurrent.futures
import hashlib
import json
from pathlib import Path
import urllib.request
import urllib.error

ROOT = Path(__file__).resolve().parents[1]


def fetch(url):
    try:
        request = urllib.request.Request(url, headers={'User-Agent': 'DEX-provenance-audit', 'Accept': 'application/vnd.github+json'})
        with urllib.request.urlopen(request, timeout=20) as response:
            return {'http': response.status, 'data': json.load(response)}
    except (urllib.error.URLError, TimeoutError) as error:
        return {'http': getattr(error, 'code', None), 'error': str(error)}


def fetch_bytes(url):
    try:
        request = urllib.request.Request(url, headers={'User-Agent': 'DEX-provenance-audit'})
        with urllib.request.urlopen(request, timeout=20) as response:
            return {'http': response.status, 'bytes': response.read()}
    except (urllib.error.URLError, TimeoutError) as error:
        return {'http': getattr(error, 'code', None), 'error': str(error)}


def fetch_commit_header(url):
    try:
        request = urllib.request.Request(url, headers={'User-Agent': 'DEX-provenance-audit'})
        with urllib.request.urlopen(request, timeout=20) as response:
            return {'http': response.status, 'header': response.read(256).split(b'\n', 1)[0].decode('ascii', errors='replace')}
    except (urllib.error.URLError, TimeoutError) as error:
        return {'http': getattr(error, 'code', None), 'error': str(error)}


def inspect(source):
    repo = source['repository_url'].removeprefix('https://github.com/').removesuffix('.git')
    base = 'https://api.github.com/repos/' + repo
    pin = source['pinned_commit']
    commit = fetch(base + '/commits/' + pin)
    valid = commit.get('data', {}).get('sha') == pin
    commit_fallback = {}
    if not valid and commit.get('http') in (403, 429):
        commit_fallback = fetch_commit_header('https://github.com/' + repo + '/commit/' + pin + '.patch')
        valid = commit_fallback.get('header', '').startswith('From ' + pin + ' ')

    license_result = fetch(base + '/license?ref=' + pin) if valid else {}
    license_data = license_result.get('data', {})
    raw = base64.b64decode(license_data.get('content', '')) if license_data.get('encoding') == 'base64' else None
    license_url = base + '/license?ref=' + pin
    license_fallback = {}
    if valid and raw is None:
        # The root LICENSE was independently discovered at these exact pins.
        # Preserve the API error; raw pinned content supplies bytes, not SPDX metadata.
        license_url = 'https://raw.githubusercontent.com/' + repo + '/' + pin + '/LICENSE'
        license_fallback = fetch_bytes(license_url)
        raw = license_fallback.get('bytes')
    local = ROOT / source['license_file']
    upstream_license_path = ROOT / source.get('upstream_license_file', source['license_file'])
    candidate = fetch(base + '/commits/HEAD') if not valid else {}
    return {'id': source['upstream_id'], 'configured_pin': pin,
            'pin_status': 'VERIFIED' if valid else 'UNRESOLVED',
            'pin_purpose': source.get('pin_purpose', 'LEGACY_CONFIGURED_PIN'),
            'import_origin_verification': source.get('import_origin_verification', 'NOT_VERIFIED'),
            'pin_http': commit.get('http'), 'pin_error': commit.get('error'),
            'pin_verification_method': 'GITHUB_PATCH_EXACT_SHA' if valid and commit_fallback else 'GITHUB_COMMIT_API' if valid else None,
            'commit_fallback_http': commit_fallback.get('http'),
            'commit_fallback_header': commit_fallback.get('header'),
            'candidate_head_not_imported': candidate.get('data', {}).get('sha'),
            'license_at_pin_http': license_result.get('http'),
            'license_api_error': license_result.get('error'),
            'license_content_url': license_url,
            'license_fallback_http': license_fallback.get('http'),
            'license_at_pin_spdx': license_data.get('license', {}).get('spdx_id'),
            'license_at_pin_sha256': hashlib.sha256(raw).hexdigest() if raw is not None else None,
            'local_license_sha256': hashlib.sha256(local.read_bytes()).hexdigest() if local.is_file() else None,
            'license_bytes_match': (raw == local.read_bytes()) if raw is not None and local.is_file() else None,
            'upstream_license_bytes_match': (raw == upstream_license_path.read_bytes()) if raw is not None and upstream_license_path.is_file() else None,
            'content_review': 'NOT_VERIFIED', 'import_performed': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT/'docs/audits/DEX_V9_PROVENANCE_RECHECK.json')
    args = parser.parse_args()
    sources = json.loads((ROOT/'manifests/upstream-sources.json').read_text(encoding='utf-8'))['sources']
    with concurrent.futures.ThreadPoolExecutor(max_workers=7) as pool:
        results = list(pool.map(inspect, sources))
    args.output.write_text(json.dumps(results, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(results, indent=2))
    return 0 if all(x['pin_status']=='VERIFIED' for x in results) else 1


if __name__ == '__main__':
    raise SystemExit(main())
