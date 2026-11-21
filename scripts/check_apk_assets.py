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
    assert len(pilot)==326
    for entry in pilot:
        assert entry['format']=='manual-vector'
        vector=json.loads(apk.read('assets/'+entry['vectorAsset']))
        assert vector['layers'] and vector['construction']=='manual-geometric-v1'
        assert apk.read('assets/'+entry['asset']).startswith(b'\x89PNG\r\n\x1a\n')
    review=json.loads(apk.read('assets/temporary-review/index.json'))
    assert len(review)==324 and len({e['id'] for e in review})==324
    shortcuts=json.loads(apk.read('assets/temporary-review/repair-shortcuts.json'))
    assert len(shortcuts)==29 and len({e['id'] for e in shortcuts})==29
    assert {e['id'] for e in shortcuts}<={e['id'] for e in review}
    assert shortcuts==json.loads(Path('android-logo/app/src/main/assets/temporary-review/repair-shortcuts.json').read_text())
    review_paths={f"assets/temporary-review/{e['id']}-{kind}.png" for e in review for kind in ('source','redraw')}
    import hashlib
    for name in review_paths:
        content=apk.read(name)
        assert content.startswith(b'\x89PNG\r\n\x1a\n')
        assert hashlib.sha256(content).digest()==hashlib.sha256((Path('android-logo/app/src/main')/name).read_bytes()).digest()
    assert actual == {'assets/' + name for name in expected} | {'assets/'+e['asset'] for e in pilot} | review_paths, f'Unexpected/missing logos: {actual}'
    for filename in expected:
        path = 'assets/' + filename
        assert path in available, f'Missing APK asset: {path}'
        vector = 'assets/' + filename.removesuffix('.png') + '.json'
        assert vector in available, f'Missing vector source: {vector}'
        import json
        assert json.loads(apk.read(vector))['layers'], f'Empty vector source: {vector}'
        data = apk.read(path)
        assert data.startswith(b'\x89PNG\r\n\x1a\n'), f'Invalid PNG: {filename}'
print('PASS: 330 catalog variations with native paths unchanged; 324 separate offline review pairs verified')
