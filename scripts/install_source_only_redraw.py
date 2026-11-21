"""Install the fresh source-only drawings, never loading an earlier redraw geometry."""
from pathlib import Path
import json,shutil,subprocess
R=Path(__file__).resolve().parents[1];A=R/'android-logo/app/src/main/assets';O=R/'04-desain/perbaikan-review/redraw-dari-nol'
p=json.loads((O/'progress.json').read_text());catalogPath=A/'exploration/catalog.json';catalog=json.loads(catalogPath.read_text())
for row in p['entries']:
    key=row['id'];src=O/f'{key}.json';svg=O/f'{key}.svg'
    shutil.copyfile(src,A/'exploration'/f'{key}.json')
    subprocess.run(['node','-e',"const fs=require('fs'),{Resvg}=require(process.argv[1]);fs.writeFileSync(process.argv[3],new Resvg(fs.readFileSync(process.argv[2]),{fitTo:{mode:'width',value:400}}).render().asPng());",str(R/'.cache/mcm-redraw/node_modules/@resvg/resvg-js'),str(svg),str(A/'exploration'/f'{key}.png')],check=True)
    shutil.copyfile(A/'exploration'/f'{key}.png',A/'temporary-review'/f'{key}-redraw.png')
    e=next(e for e in catalog['reviewedEntries'] if e['id']==key)
    e.update(pathJson=str(src.relative_to(R)),masterSvg=str(svg.relative_to(R)),status='fresh-source-only-redraw-installed-awaiting-user-review',repairRepresentative=key)
    row['installed']=True
page=O/'perbandingan.html'
page.write_text(page.read_text().replace('Belum disetujui pengguna dan belum dipasang ke aplikasi.','Belum disetujui pengguna. Sudah dipasang ke aset aplikasi; belum build APK.'))
catalogPath.write_text(json.dumps(catalog,indent=2))
(O/'progress.json').write_text(json.dumps(p,indent=2)+'\n')
print('13 fresh drawings installed in app and review assets; source originals unchanged. APK not built.')
