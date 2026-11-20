"""Manual coordinate masters for the two Drive variations; never traces PNG pixels."""
from pathlib import Path
import json, subprocess
R=Path(__file__).resolve().parents[1]
O=R/'android-logo/app/src/main/assets/exploration'
D=R/'04-desain/variasi-svg';D.mkdir(parents=True,exist_ok=True)
def layer(color,*contours):
    cmds=[]
    for p in contours:cmds.extend([['M',*p[0]],*[['L',*v] for v in p[1:]],['Z']])
    return dict(color=color,commands=cmds)
def mirror(p,axis):return [(axis*2-x,y) for x,y in p]
m1=[(54,147),(78,131),(90,157),(107,113),(131,93),(131,251),(109,233),(109,172),(91,214),(75,181),(75,207),(54,191)]
c1=[(180,61),(205,81),(216,96),(216,145),(193,145),(193,95),(180,84),(167,96),(167,251),(180,264),(193,251),(193,196),(216,196),(216,272),(202,286),(158,286),(144,272),(144,96),(155,81)]
left8=[(9,161),(156,43),(156,286)]
m8=[(51,163),(141,91),(141,269),(120,250),(120,166),(106,188),(90,159),(90,207)]
center8=[(166,101),(200,73),(234,101),(234,139),(210,148),(210,109),(200,102),(191,109),(191,235),(200,242),(210,235),(210,190),(234,181),(234,263),(200,291),(166,263)]
cap8=[(166,42),(200,16),(234,42),(234,83),(200,58),(166,83)]
bottom8=[(166,277),(200,305),(234,277),(234,303),(200,329),(166,303)]
data={
'exp-001-01':dict(width=360,height=344,layers=[layer(0,[(180,8),(350,172),(180,336),(10,172)]),layer(2,m1,mirror(m1,180),c1)]),
'exp-001-08':dict(width=400,height=344,layers=[layer(0,left8,mirror(left8,200)),layer(1,center8,cap8,bottom8),layer(2,m8,mirror(m8,200))])}
manifest=json.loads((O/'catalog.json').read_text())
for name,logo in data.items():
    logo['construction']='manual-geometric-v1'
    (O/f'{name}.json').write_text(json.dumps(logo,separators=(',',':')))
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {logo["width"]} {logo["height"]}">'
    for l in logo['layers']:
        path=' '.join(c[0]+' '+' '.join(str(v) for v in c[1:]) for c in l['commands'])
        svg+=f'<path fill="{["#DC2626","#173257","#FFFFFF"][l["color"]]}" fill-rule="evenodd" d="{path}"/>'
    svg+='</svg>'
    (D/f'{name}.svg').write_text(svg)
    subprocess.run(['node','-e',"const fs=require('fs'),{Resvg}=require(process.argv[1]);fs.writeFileSync(process.argv[3],new Resvg(fs.readFileSync(process.argv[2]),{fitTo:{mode:'width',value:800}}).render().asPng());",str(R/'.cache/mcm-redraw/node_modules/@resvg/resvg-js'),str(D/f'{name}.svg'),str(O/f'{name}.png')],check=True)
    for entry in manifest['reviewedEntries']:
        if entry['id']==name:entry.update(format='manual-vector',vectorAsset=f'exploration/{name}.json',masterSvg=f'04-desain/variasi-svg/{name}.svg',name='Variasi 05' if name.endswith('01') else 'Variasi 06')
manifest['version']=2
(O/'catalog.json').write_text(json.dumps(manifest,indent=2))
