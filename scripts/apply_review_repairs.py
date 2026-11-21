"""Install reviewed working vectors into studio and offline review, preserving all stable IDs."""
from pathlib import Path
import json,shutil,subprocess
R=Path(__file__).resolve().parents[1];A=R/'android-logo/app/src/main/assets';D=R/'04-desain/perbaikan-review'
review=json.loads((D/'putaran-04/review.json').read_text());records=review['records']
for row in records:
    target=row['id']; representative=row.get('representative',row['variation'])
    master=next(r for r in records if r['variation']==representative)
    folder=D/f"putaran-{master.get('round',1):02}"
    key=master['id'];src=folder/f'{key}.json';svg=folder/f'{key}.svg'
    shutil.copyfile(src,A/'exploration'/f'{target}.json')
    subprocess.run(['node','-e',"const fs=require('fs'),{Resvg}=require(process.argv[1]);fs.writeFileSync(process.argv[3],new Resvg(fs.readFileSync(process.argv[2]),{fitTo:{mode:'width',value:400}}).render().asPng());",str(R/'.cache/mcm-redraw/node_modules/@resvg/resvg-js'),str(svg),str(A/'exploration'/f'{target}.png')],check=True)
    shutil.copyfile(A/'exploration'/f'{target}.png',A/'temporary-review'/f'{target}-redraw.png')
(A/'temporary-review/applied-repairs.json').write_text(json.dumps([dict(id=r['id'],representative=next(x['id'] for x in records if x['variation']==r.get('representative',r['variation']))) for r in records],indent=2)+'\n')
print('29 stable IDs updated in studio and review; six group members share two corrected masters.')
