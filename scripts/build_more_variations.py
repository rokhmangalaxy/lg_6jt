"""Two new geometric studies based on shield/triangle families in original nine-logo reference."""
from pathlib import Path
import json,subprocess
R=Path(__file__).resolve().parents[1];O=R/'android-logo/app/src/main/assets/exploration';D=R/'04-desain/variasi-svg'
def layer(color,*polys):
    c=[]
    for p in polys:c += [['M',*p[0]],*[['L',*v] for v in p[1:]],['Z']]
    return dict(color=color,commands=c)
def mirror(p):return [(402-x,y) for x,y in p]
base=json.loads((R/'android-logo/logo-assets/client-attachment-08.json').read_text())
# Reuse the measured central MCM contours, not raster artwork.
letters=[base['layers'][1],base['layers'][2]]
shield=[(201,7),(286,76),(390,40),(390,187),(201,343),(12,187),(12,40),(116,76)]
inner=[(201,23),(284,91),(378,58),(378,181),(201,327),(24,181),(24,58),(118,91)]
wing=[(31,68),(94,105),(142,91),(96,128)]
triangle=[(8,44),(394,44),(201,343)]
cut=[(33,57),(369,57),(201,320)]
# Compact letters leave room for a new enclosing frame.
def scaled(l,sx,sy,cx=201,cy=175):
    return dict(color=l['color'],commands=[[c[0],round(cx+(c[1]-cx)*sx,2),round(cy+(c[2]-cy)*sy,2)] if len(c)>1 else c for c in l['commands']])
variants={
'geo-007':dict(width=404,height=351,layers=[layer(0,shield,inner),layer(1,wing,mirror(wing)),*[scaled(l,.9,.84) for l in letters]]),
'geo-008':dict(width=404,height=351,layers=[layer(0,triangle,cut),layer(1,[(201,319),(141,260),(201,290),(261,260)]),*[scaled(l,.67,.72,201,145) for l in letters]])}
manifest=json.loads((O/'catalog.json').read_text())
for name,data in variants.items():
    data['construction']='manual-geometric-v1';(O/f'{name}.json').write_text(json.dumps(data,separators=(',',':')))
    svg='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 404 351">'
    for l in data['layers']:
        d=' '.join(c[0]+' '+' '.join(str(n) for n in c[1:]) for c in l['commands'])
        svg+=f'<path fill="{["#DC2626","#173257","#FFFFFF"][l["color"]]}" fill-rule="evenodd" d="{d}"/>'
    svg+='</svg>';(D/f'{name}.svg').write_text(svg)
    subprocess.run(['node','-e',"const fs=require('fs'),{Resvg}=require(process.argv[1]);fs.writeFileSync(process.argv[3],new Resvg(fs.readFileSync(process.argv[2]),{fitTo:{mode:'width',value:800}}).render().asPng());",str(R/'.cache/mcm-redraw/node_modules/@resvg/resvg-js'),str(D/f'{name}.svg'),str(O/f'{name}.png')],check=True)
    manifest['reviewedEntries']=[e for e in manifest['reviewedEntries'] if e['id']!=name]
    manifest['reviewedEntries'].append(dict(id=name,name='Variasi '+name[-2:],asset=f'exploration/{name}.png',vectorAsset=f'exploration/{name}.json',masterSvg=f'04-desain/variasi-svg/{name}.svg',format='manual-vector',status='new-geometric-study',sourceName='Original nine-logo reference: shield/triangle family, not pixel-exact reproduction'))
manifest['version']=3;(O/'catalog.json').write_text(json.dumps(manifest,indent=2))
