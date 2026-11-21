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
# Rebuilt against attachment cell crops in their own 404x351 coordinate system.
# Unlike v1, preserve the narrow bottom V, separate side inlays and frame breaks.
def mirror_ref(p):return [(402-x,y) for x,y in p]
m8=[(32,72),(96,134),(148,87),(148,289),(117,239),(117,158),(96,182),(62,144),(64,225),(32,199)]
wing8=[(38,61),(96,102),(154,55),(144,79),(96,124)]
side8=[(75,170),(96,194),(105,185),(105,274)]
bottom8=[(157,266),(201,308),(245,266),(245,281),(201,346),(157,281)]
c8=[(201,59),(245,99),(245,145),(213,145),(213,108),(201,97),(190,108),(190,248),(201,259),(213,248),(213,203),(245,203),(245,258),(201,299),(157,258),(157,99)]
cap8=[(201,5),(245,70),(245,89),(207,53),(201,41),(195,53),(157,89),(157,70)]
# Cell 9 uses a split outer red diamond and an inner navy frame, not
# the oversized side arrowheads and extra lower bands of the rejected redraw.
m9=[(75,132),(95,117),(113,149),(128,112),(156,90),(156,253),(133,234),(133,155),(114,187),(98,163),(98,231),(75,213)]
c9=[(201,56),(235,84),(235,143),(210,143),(210,102),(201,93),(192,102),(192,243),(201,253),(210,243),(210,188),(235,188),(235,260),(201,291),(167,260),(167,84)]
redtop=[(201,3),(282,73),(282,77),(339,123),(339,138),(274,84),(274,80),(201,18),(128,80),(128,84),(63,138),(63,123),(120,77),(120,73)]
redside=[(54,129),(54,143),(23,171),(54,198),(54,214),(5,171)]
redlower=[(63,205),(125,259),(125,275),(63,221)]
redbottom=[(135,272),(201,330),(267,272),(267,289),(201,346),(135,289)]
navytop=[(201,27),(273,87),(273,102),(201,44),(129,102),(129,87)]
navyside=[(37,171),(64,148),(64,194)]
navybottom=[(107,188),(115,198),(123,188),(123,236),(201,304),(279,236),(279,188),(287,198),(295,188),(295,235),(201,318),(107,235)]
catalog={
'client-attachment-01':dict(width=400,height=436,layers=[layer(0,hex_outer,hex_inner),layer(2,m1,mirror(m1),c1)]),
'client-attachment-08':dict(width=404,height=351,layers=[layer(1,wing8,mirror_ref(wing8),side8,mirror_ref(side8),bottom8),layer(0,cap8,c8),layer(2,m8,mirror_ref(m8))]),
'client-attachment-09':dict(width=404,height=351,layers=[layer(0,redtop,redside,mirror_ref(redside),redlower,mirror_ref(redlower),redbottom),layer(1,navytop,navyside,mirror_ref(navyside),navybottom),layer(0,c9),layer(2,m9,mirror_ref(m9))])}
# Approved logo 04 uses the approved master without modification.
catalog['client-logo-04']=json.loads((R/'04-desain/redraw-geometris-04/mcm-04-geometris.json').read_text())
for name,data in catalog.items():
    data['construction']='manual-geometric-v1'
    if name in ('client-attachment-08','client-attachment-09'):
        cell=int(name[-2:]);data['referenceCell']=cell
        data['referenceCrop']=[465 if cell==8 else 902,755,404,351]
    (OUT/(name+'.json')).write_text(json.dumps(data,indent=2))
    (ASSETS/(name+'.json')).write_text(json.dumps(data,separators=(',',':')))
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {data["width"]} {data["height"]}" width="{data["width"]}" height="{data["height"]}">'+''.join(f'<path fill="{COLORS[l["color"]]}" fill-rule="evenodd" d="{path(l["commands"])}"/>' for l in data['layers'])+'</svg>'
    (OUT/(name+'.svg')).write_text(svg)
    for target,width,bg in [(ASSETS/(name+'.png'),800,None),(OUT/(name+'-preview.png'),800,'#D1D5DB')]:
        opt=dict(fitTo=dict(mode='width',value=width))
        if bg:opt['background']=bg
        subprocess.run(['node','-e',"const fs=require('fs'),{Resvg}=require(process.argv[1]);fs.writeFileSync(process.argv[3],new Resvg(fs.readFileSync(process.argv[2]),JSON.parse(process.argv[4])).render().asPng());",str(R/'.cache/mcm-redraw/node_modules/@resvg/resvg-js'),str(OUT/(name+'.svg')),str(target),json.dumps(opt)],check=True)
print('Built and installed four geometric logo assets')
