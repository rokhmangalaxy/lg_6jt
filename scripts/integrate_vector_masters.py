"""Append reviewed-in-session path masters, retaining every existing catalog index."""
from pathlib import Path
import json,re,shutil,subprocess
R=Path(__file__).resolve().parents[1]
A=R/'android-logo/app/src/main/assets/exploration'
K=R/'android-logo/app/src/main/java/id/mcm/logopreview/LogoCatalog.kt'
def integrate():
    manifest=json.loads((A/'catalog.json').read_text());known={e['id'] for e in manifest['reviewedEntries']}
    kotlin=K.read_text();files=re.findall(r'"([^"\n]+\.png)"',kotlin)
    names=re.findall(r'"(Variasi \d+)"',kotlin)
    original=files[:11];assert len(files)==len(names)
    for batch in range(3,14):
        progress=json.loads((R/f'04-desain/variasi-svg/batch-{batch:02}/progress.json').read_text())
        for e in progress['entries']:
            if e['id'] in known:continue
            target=e['id'];shutil.copyfile(R/e['pathJson'],A/f'{target}.json')
            subprocess.run(['node','-e',"const fs=require('fs'),{Resvg}=require(process.argv[1]);fs.writeFileSync(process.argv[3],new Resvg(fs.readFileSync(process.argv[2]),{fitTo:{mode:'width',value:400}}).render().asPng());",str(R/'.cache/mcm-redraw/node_modules/@resvg/resvg-js'),str(R/e['masterSvg']),str(A/f'{target}.png')],check=True)
            name=f'Variasi {len(files)+1:02}';asset=f'exploration/{target}.png'
            entry={**e,'asset':asset,'vectorAsset':f'exploration/{target}.json','name':name,'appIntegration':'included-by-explicit-user-build-request','status':'geometric-redraw-awaiting-user-review'}
            manifest['reviewedEntries'].append(entry);files.append(asset);names.append(name);known.add(target)
    assert files[:11]==original and len(files)==105
    manifest.update(version=5,scope='99 unique Drive path masters, four original selections, two studies; collection incomplete. User explicitly requested this interim APK.',sourceAliases=json.loads((R/'04-desain/variasi-svg/batch-13/progress.json').read_text())['sourceAliases'])
    (A/'catalog.json').write_text(json.dumps(manifest,indent=2))
    kotlin=re.sub(r'val files = arrayOf\(.*?\)\n', 'val files = arrayOf(\n        '+',\n        '.join(json.dumps(x) for x in files)+')\n',kotlin,count=1,flags=re.S)
    kotlin=re.sub(r'val names = arrayOf\(.*?\)\n','val names = arrayOf('+', '.join(json.dumps(x) for x in names)+')\n',kotlin,count=1,flags=re.S)
    K.write_text(kotlin)
    print('105 variations, 99 unique Drive masters. Existing 11 IDs and indices retained.')
if __name__=='__main__':integrate()
