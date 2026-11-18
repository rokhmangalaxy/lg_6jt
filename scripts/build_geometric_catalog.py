"""Coordinate-built client catalog; no tracing. Run after build_logo04_geometric.py."""
from pathlib import Path
import json, subprocess, shutil
R=Path(__file__).resolve().parents[1]
OUT=R/'04-desain/redraw-geometris-katalog';OUT.mkdir(exist_ok=True)
ASSETS=R/'android-logo/logo-assets'
COLORS=['#DC2626','#173257','#FFFFFF']
def mirror(p):return [(400-x,y) for x,y in p]
def layer(color,*contours):
    commands=[]
    for p in contours:commands += [['M',*p[0]],*[['L',*q] for q in p[1:]],['Z']]
    return dict(color=color,commands=commands)
def path(commands):return ' '.join(c[0]+' '+' '.join(str(n) for n in c[1:]) for c in commands)
# Hexagon frame: consistent concentric six-sided polygons. Two M outlines mirrored.
hex_outer=[(200,20),(372,119),(372,317),(200,416),(28,317),(28,119)]
hex_inner=[(200,48),(348,133),(348,303),(200,388),(52,303),(52,133)]
m1=[(62,150),(79,140),(101,181),(119,126),(145,108),(145,350),(119,335),(119,224),(101,263),(81,223),(81,307),(62,296)]
c1=[(200,66),(244,92),(244,178),(213,178),(213,124),(200,114),(187,124),(187,314),(200,324),(213,314),(213,245),(244,230),(244,345),(200,372),(156,345),(156,92)]
# Wing-shaped mark: common x=200 axis, explicit straight diagonals.
m8=[(28,103),(93,168),(145,116),(145,344),(112,284),(112,224),(94,245),(61,207),(61,276),(28,247)]
wing8=[(34,93),(94,133),(150,88),(94,158)]
low8=[(80,247),(126,322),(200,388),(274,322),(320,247),(300,310),(200,414),(100,310)]
c8=[(200,89),(249,137),(249,194),(214,194),(214,145),(200,132),(186,145),(186,310),(200,323),(214,310),(214,259),(249,259),(249,321),(200,369),(151,321),(151,137)]
# Diamond mark. Red and navy frames have deliberate breaks beside the M shoulders.
m9=[(67,175),(92,154),(106,188),(124,150),(153,126),(153,309),(126,285),(126,229),(107,260),(90,231),(90,280),(67,259)]
c9=[(200,94),(236,125),(236,189),(211,189),(211,148),(200,137),(189,148),(189,302),(200,313),(211,302),(211,255),(236,255),(236,326),(200,358),(164,326),(164,125)]
redtop=[(200,29),(346,155),(346,173),(200,47),(54,173),(54,155)]
redbottom=[(54,271),(200,397),(346,271),(346,289),(200,415),(54,289)]
redside=[(45,163),(45,182),(15,208),(45,234),(45,253),(0,208)]
navytop=[(200,55),(279,123),(279,140),(200,73),(121,140),(121,123)]
navybottom=[(111,272),(135,309),(200,365),(265,309),(289,272),(283,321),(200,393),(117,321)]
navyside=[(26,208),(57,181),(57,235)]
shadow=[(105,272),(118,248),(118,294),(154,325),(154,342),(101,296)]
catalog={
'client-attachment-01':dict(width=400,height=436,layers=[layer(0,hex_outer,hex_inner),layer(2,m1,mirror(m1),c1)]),
'client-attachment-08':dict(width=400,height=436,layers=[layer(1,wing8,mirror(wing8),low8),layer(0,[(200,29),(249,106),(249,127),(200,80),(151,127),(151,106)]),layer(0,c8),layer(2,m8,mirror(m8))]),
'client-attachment-09':dict(width=400,height=436,layers=[layer(0,redtop,redbottom,redside,mirror(redside)),layer(1,navytop,navybottom,navyside,mirror(navyside)),layer(0,c9),layer(2,m9,mirror(m9))])}
# Approved logo 04 uses the approved master without modification.
catalog['client-logo-04']=json.loads((R/'04-desain/redraw-geometris-04/mcm-04-geometris.json').read_text())
for name,data in catalog.items():
    data['construction']='manual-geometric-v1'
    (OUT/(name+'.json')).write_text(json.dumps(data,indent=2))
    (ASSETS/(name+'.json')).write_text(json.dumps(data,separators=(',',':')))
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {data["width"]} {data["height"]}" width="{data["width"]}" height="{data["height"]}">'+''.join(f'<path fill="{COLORS[l["color"]]}" fill-rule="evenodd" d="{path(l["commands"])}"/>' for l in data['layers'])+'</svg>'
    (OUT/(name+'.svg')).write_text(svg)
    for target,width,bg in [(ASSETS/(name+'.png'),800,None),(OUT/(name+'-preview.png'),800,'#D1D5DB')]:
        opt=dict(fitTo=dict(mode='width',value=width))
        if bg:opt['background']=bg
        subprocess.run(['node','-e',"const fs=require('fs'),{Resvg}=require(process.argv[1]);fs.writeFileSync(process.argv[3],new Resvg(fs.readFileSync(process.argv[2]),JSON.parse(process.argv[4])).render().asPng());",str(R/'.cache/mcm-redraw/node_modules/@resvg/resvg-js'),str(OUT/(name+'.svg')),str(target),json.dumps(opt)],check=True)
print('Built and installed four geometric logo assets')
