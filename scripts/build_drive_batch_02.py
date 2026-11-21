"""Manual geometric redraw of Drive group 1 / cells 02,03,04; never raster tracing."""
from pathlib import Path
import json,hashlib,base64,subprocess
R=Path(__file__).resolve().parents[1]
O=R/'android-logo/app/src/main/assets/exploration';D=R/'04-desain/variasi-svg';B=D/'batch-02';B.mkdir(parents=True,exist_ok=True)
def layer(color,*polys):
    c=[]
    for p in polys:c += [['M',*p[0]],*[['L',*q] for q in p[1:]],['Z']]
    return dict(color=color,commands=c)
def mirror(p,axis):return [(2*axis-x,y) for x,y in p]
# Source 02: independent red M pair, no enclosing diamond. Axis x=180.
m2=[(9,87),(60,127),(91,71),(120,51),(120,276),(88,256),(88,141),(63,182),(40,151),(40,236),(9,216)]
c2=[(180,9),(228,42),(228,120),(196,126),(196,62),(180,51),(164,63),(164,257),(180,269),(196,257),(196,198),(228,198),(228,277),(180,310),(132,277),(132,42)]
# Source 03: concentric navy hexagon, red MCM, straight sloped shoulders.
outer3=[(163,9),(317,95),(317,260),(163,346),(9,260),(9,95)]
inner3=[(163,34),(296,109),(296,246),(163,321),(30,246),(30,109)]
m3=[(42,116),(64,104),(75,139),(91,91),(113,78),(113,279),(91,266),(91,166),(76,198),(61,168),(61,251),(42,240)]
c3=[(163,49),(201,71),(201,131),(175,131),(175,90),(163,82),(151,90),(151,267),(163,275),(175,267),(175,225),(201,225),(201,285),(163,307),(125,285),(125,71)]
# Source 04: wing segments are separate polygons, not an oversized new frame.
m4=[(80,96),(95,76),(121,112),(141,66),(165,45),(165,213),(141,198),(141,120),(123,156),(104,129),(104,177),(80,157)]
c4=[(213,9),(251,37),(251,87),(226,94),(226,52),(213,41),(201,52),(201,197),(213,207),(226,197),(226,155),(251,155),(251,216),(213,243),(175,216),(175,37)]
wing4=[(9,75),(95,75),(109,95),(25,95)]
bar4=[(32,107),(73,107),(73,125),(45,125)]
small4=[(49,134),(73,134),(73,151),(60,151)]
batch={
2:dict(width=360,height=320,layers=[layer(0,m2,mirror(m2,180)),layer(1,c2)]),
3:dict(width=326,height=355,layers=[layer(1,outer3,inner3),layer(0,m3,mirror(m3,163),c3)]),
4:dict(width=426,height=252,layers=[layer(0,wing4,mirror(wing4,213),bar4,mirror(bar4,213),small4,mirror(small4,213)),layer(0,m4,mirror(m4,213)),layer(1,c4)])}
ids={2:'19yJxNN4xRt_NqpJyOWM6qACQ17scOId6',3:'1FE1MMC1Kpar0jHaCJ4Qm5k59HiOcu-8o',4:'1BpPfhJefVWsIvKLq5u8MObm1GWkAY1ch'}
manifest=json.loads((O/'catalog.json').read_text());report=[]
previous={e.get('sourceSha256') for e in manifest['reviewedEntries'] if e.get('sourceSha256') and e.get('id') not in {f'exp-001-{n:02}' for n in batch}}
for n,data in batch.items():
    name=f'exp-001-{n:02}';number=n+7;source=R/f'google_drive/Max_a_Gambar_kotak_berisi__1_logo-{n:02}.png'
    digest=hashlib.sha256(source.read_bytes()).hexdigest()
    assert digest not in previous,'Exact source duplicate';previous.add(digest)
    data['construction']='manual-geometric-v1';(O/f'{name}.json').write_text(json.dumps(data,separators=(',',':')))
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {data["width"]} {data["height"]}">'
    for l in data['layers']:
        path=' '.join(c[0]+' '+' '.join(str(v) for v in c[1:]) for c in l['commands'])
        svg+=f'<path fill="{["#DC2626","#173257","#FFFFFF"][l["color"]]}" fill-rule="evenodd" d="{path}"/>'
    svg+='</svg>';(D/f'{name}.svg').write_text(svg)
    subprocess.run(['node','-e',"const fs=require('fs'),{Resvg}=require(process.argv[1]);fs.writeFileSync(process.argv[3],new Resvg(fs.readFileSync(process.argv[2]),{fitTo:{mode:'width',value:800}}).render().asPng());",str(R/'.cache/mcm-redraw/node_modules/@resvg/resvg-js'),str(D/f'{name}.svg'),str(O/f'{name}.png')],check=True)
    entry=dict(id=name,name=f'Variasi {number:02}',asset=f'exploration/{name}.png',vectorAsset=f'exploration/{name}.json',masterSvg=f'04-desain/variasi-svg/{name}.svg',sourceName=source.name,driveId=ids[n],sourceSha256=digest,format='manual-vector',group=1,sourceNumber=n,status='batch-02-geometric-redraw')
    manifest['reviewedEntries']=[e for e in manifest['reviewedEntries'] if e['id']!=name]+[entry];report.append(entry)
manifest.update(version=4,scope='Five Drive sources redrawn manually (group 1: 01,02,03,04,08), plus two original-reference geometric studies. Remaining Drive files not audited.')
(O/'catalog.json').write_text(json.dumps(manifest,indent=2))
(B/'progress.json').write_text(json.dumps(dict(driveSourcesRedrawn=[1,2,3,4,8],group1Pending=[5,6,7,9],entries=report,duplicateCheck='SHA256 on the five downloaded sources only; visual similarity is reviewed, not a full-folder duplicate audit.'),indent=2))
page='''<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Redraw batch 02</title><style>body{font:16px system-ui;color:#173257;background:#e9eef5;margin:24px}main{max-width:1000px;margin:auto}.pair{display:grid;grid-template-columns:1fr 1fr;gap:12px}.card{background:white;border-radius:12px;padding:16px}img,svg{width:100%;height:330px;object-fit:contain}p{line-height:1.6}</style><main><h1>Batch 02 · Variasi 09–11</h1><p>Kiri sumber Drive; kanan redraw geometris manual. Warna dibuat solid, garis dirapikan dan kedua M disimetriskan. Tidak identik piksel; semua area di luar artwork transparan. Belum persetujuan produksi.</p>'''
for e in report:
    src=R/'google_drive'/e['sourceName'];encoded=base64.b64encode(src.read_bytes()).decode()
    page+=f'<h2>{e["name"]} · kelompok 1 / logo {e["sourceNumber"]:02}</h2><div class="pair"><div class="card"><h3>Sumber raster</h3><img alt="Referensi" src="data:image/png;base64,{encoded}"></div><div class="card"><h3>Redraw vektor</h3>{(R/e["masterSvg"]).read_text()}</div></div>'
(B/'perbandingan.html').write_text(page+'</main>')
print('Added 3 manual vector masters; Drive group 1 progress: 5/9')
