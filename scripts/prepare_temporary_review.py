"""Package removable offline review assets; does not modify the app catalog."""
from pathlib import Path
import json,shutil
R=Path(__file__).resolve().parents[1]
audit=json.loads((R/'04-desain/variasi-svg/batch-36/audit_inventory.json').read_text())
out=R/'android-logo/app/src/main/assets/temporary-review';out.mkdir(exist_ok=True)
rows=[]
for e in audit['records']:
    if e['kind']!='manual-master':continue
    key=e['masterId']
    shutil.copyfile(R/'google_drive'/e['sourceName'],out/f'{key}-source.png')
    preview=R/e['masterSvg'];preview=preview.with_name(preview.stem+'-preview.png')
    if not preview.exists():
        preview=R/'android-logo/app/src/main/assets'/f'exploration/{key}.png'
    shutil.copyfile(preview,out/f'{key}-redraw.png')
    rows.append(dict(id=key,sourceName=e['sourceName']))
(out/'index.json').write_text(json.dumps(rows,indent=2))
print(f'{len(rows)} offline review pairs; original catalog unchanged')
