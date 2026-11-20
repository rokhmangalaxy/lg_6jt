"""Usage: python3 scripts/check_apk_assets.py path/to/app-release.apk"""
import re
import sys
import zipfile
from pathlib import Path

catalog = Path('android-logo/app/src/main/java/id/mcm/logopreview/LogoCatalog.kt').read_text()
expected = re.findall(r'"(client-[^"\n]+\.png)"', catalog)
assert len(expected) == 4 and len(set(expected)) == 4
with zipfile.ZipFile(sys.argv[1]) as apk:
    available = set(apk.namelist())
    actual = {name for name in available if name.startswith('assets/') and name.endswith('.png')}
    import json
    pilot=json.loads(apk.read('assets/exploration/catalog.json'))['reviewedEntries']
    assert len(pilot)==4
    for entry in pilot:
        assert entry['format']=='manual-vector'
        vector=json.loads(apk.read('assets/'+entry['vectorAsset']))
        assert vector['layers'] and vector['construction']=='manual-geometric-v1'
        assert apk.read('assets/'+entry['asset']).startswith(b'\x89PNG\r\n\x1a\n')
    assert actual == {'assets/' + name for name in expected} | {'assets/'+e['asset'] for e in pilot}, f'Unexpected/missing logos: {actual}'
    for filename in expected:
        path = 'assets/' + filename
        assert path in available, f'Missing APK asset: {path}'
        vector = 'assets/' + filename.removesuffix('.png') + '.json'
        assert vector in available, f'Missing vector source: {vector}'
        import json
        assert json.loads(apk.read(vector))['layers'], f'Empty vector source: {vector}'
        data = apk.read(path)
        assert data.startswith(b'\x89PNG\r\n\x1a\n'), f'Invalid PNG: {filename}'
print('PASS: release APK contains exactly the 4 selected catalog PNGs')
