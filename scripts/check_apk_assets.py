"""Usage: python3 scripts/check_apk_assets.py path/to/app-release.apk"""
import re
import sys
import zipfile
from pathlib import Path

catalog = Path('android-logo/app/src/main/java/id/mcm/logopreview/LogoCatalog.kt').read_text()
expected = re.findall(r'"(variasi-[^"\n]+\.png)"', catalog)
assert len(expected) == 10 and len(set(expected)) == 10
with zipfile.ZipFile(sys.argv[1]) as apk:
    available = set(apk.namelist())
    for filename in expected:
        path = 'assets/' + filename
        assert path in available, f'Missing APK asset: {path}'
        data = apk.read(path)
        assert data.startswith(b'\x89PNG\r\n\x1a\n'), f'Invalid PNG: {filename}'
print('PASS: release APK contains all 10 catalog PNGs')
