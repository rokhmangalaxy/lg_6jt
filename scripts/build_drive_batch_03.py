"""Ten manual geometric reconstructions. Outputs design masters only; never builds APK."""
from pathlib import Path
import json,hashlib,subprocess,base64
R=Path(__file__).resolve().parents[1]
OUT=R/'04-desain/variasi-svg/batch-03';OUT.mkdir(parents=True,exist_ok=True)
def layer(color,*polys):
    commands=[]
    for poly in polys:commands += [['M',*poly[0]],*[['L',*v] for v in poly[1:]],['Z']]
    return dict(color=color,commands=commands)
def mirror(poly,x):return [(round(2*x-a,2),b) for a,b in poly]
def logo(w,h,*layers):return dict(width=w,height=h,construction='manual-geometric-v1',layers=list(layers))
# G1-05: triangular M shoulders, separate wing bars, pointed C foot.
m15=[(26,63),(69,63),(94,101),(116,66),(140,51),(140,218),(115,183),(115,111),(94,144),(73,111),(75,146)]
c15=[(187.5,9),(225,33),(225,97),(200,97),(200,50),(187.5,41),(175,50),(175,211),(187.5,223),(200,211),(200,155),(225,155),(225,231),(187.5,289),(150,231),(150,33)]
w15=[(9,32),(144,32),(116,54),(21,54)]
# G1-06: shield frame, centered navy initials, symmetric Ms.
m16=[(45,94),(66,86),(81,116),(96,84),(118,73),(118,271),(96,252),(96,146),(81,173),(65,145),(65,226),(45,207)]
c16=[(163,51),(201,72),(201,126),(176,133),(176,91),(163,84),(151,92),(151,259),(163,268),(176,259),(176,209),(201,209),(201,273),(163,302),(125,273),(125,72)]
o16=[(163,9),(317,60),(317,222),(163,345),(9,222),(9,60)]
i16=[(163,37),(295,80),(295,211),(163,317),(31,211),(31,80)]
# G1-07: stacked roof, small central C and open-bottom frame.
m17=[(9,94),(37,111),(51,161),(70,129),(95,143),(95,283),(70,269),(70,184),(55,209),(32,168),(32,249),(9,236)]
c17=[(137,133),(168,151),(168,191),(146,202),(146,177),(137,171),(129,177),(129,270),(137,276),(146,270),(146,245),(168,235),(168,287),(137,305),(106,287),(106,151)]
roof17=[(137,9),(262,80),(235,100),(137,49),(39,100),(12,80)]
roof17b=[(70,114),(137,74),(204,114),(170,134),(137,115),(104,134)]
bottom17=[(9,247),(137,318),(265,247),(265,276),(137,347),(9,276)]
# G1-09: slim red center, navy Ms and separated red lower strips.
m19=[(9,66),(52,103),(112,41),(112,246),(85,228),(85,128),(61,151),(36,125),(36,199),(9,183)]
c19=[(168,9),(211,37),(211,118),(182,110),(182,54),(168,45),(155,54),(155,261),(168,271),(182,261),(182,186),(211,186),(211,278),(168,309),(125,278),(125,37)]
b19=[(9,198),(96,247),(96,277),(9,229)]
# G2-01: double diamond with white negative-space MCM in red center.
o21=[(193,9),(377,153),(193,305),(9,153)]
i21=[(193,29),(354,153),(193,286),(31,153)]
d21=[(193,42),(341,153),(193,274),(45,153)]
m21=[(83,137),(103,125),(113,145),(128,109),(150,95),(150,220),(128,205),(128,160),(113,184),(99,161),(99,187),(83,176)]
c21=[(193,66),(225,90),(225,136),(204,136),(204,102),(193,94),(184,103),(184,215),(193,222),(204,214),(204,174),(225,174),(225,229),(193,252),(162,229),(162,89)]
# G2-02: broader center than G1-09; no lower strips.
m22=[(9,98),(38,80),(55,119),(79,57),(109,39),(109,270),(79,249),(79,149),(58,193),(38,146),(38,223),(9,206)]
c22=[(160,9),(200,35),(200,111),(172,96),(172,54),(160,46),(148,54),(148,249),(160,258),(172,249),(172,200),(200,185),(200,271),(160,295),(120,271),(120,35)]
# G2-03: red crown, navy Ms and slanted C terminals.
m23=[(32,64),(59,84),(83,138),(105,102),(136,83),(136,244),(108,226),(108,150),(85,190),(60,149),(60,196),(32,179)]
c23=[(187,51),(225,75),(225,129),(198,117),(198,92),(187,84),(177,92),(177,221),(187,229),(198,221),(198,192),(225,178),(225,237),(187,261),(150,237),(150,75)]
roof23=[(9,22),(100,62),(187,9),(275,62),(365,22),(344,50),(275,90),(187,38),(100,90),(30,50)]
# G2-04: wide flattened hexagon, navy upper/lower bands, separate red side bars.
m24=[(40,83),(68,75),(85,106),(104,65),(130,57),(130,196),(104,188),(104,129),(85,159),(65,129),(65,178),(40,170)]
c24=[(177,43),(211,54),(211,103),(186,103),(186,77),(177,73),(168,77),(168,175),(177,180),(186,175),(186,149),(211,149),(211,199),(177,211),(143,199),(143,54)]
top24=[(177,9),(346,62),(346,79),(177,31),(9,79),(9,62)]
bot24=[(9,172),(177,220),(346,172),(346,190),(177,245),(9,190)]
side24=[(9,91),(28,85),(28,166),(9,160)]
# G2-05: italic mark; handwritten skewed polygons, asymmetric source retained.
m25=[(9,182),(53,92),(90,47),(100,83),(165,35),(125,171),(91,171),(111,110),(83,134),(75,107),(56,151)]
mr25=[(231,171),(271,36),(292,36),(303,78),(366,34),(341,137),(306,166),(320,104),(295,128),(283,105),(269,147)]
c25=[(177,36),(257,36),(246,77),(209,94),(221,62),(199,62),(174,146),(194,146),(201,126),(234,114),(218,171),(137,171)]
t25=[(176,23),(197,9),(371,9),(354,23)]
b25=[(10,196),(32,182),(228,182),(209,196)]
# G2-06: navy outer hexagon + red inset field + negative initials.
o26=[(161,9),(312,88),(312,252),(161,336),(9,252),(9,89)]
i26=[(161,28),(296,100),(296,241),(161,317),(24,241),(24,100)]
d26=[(161,41),(286,106),(286,235),(161,306),(36,235),(36,106)]
m26=[(48,135),(65,125),(76,147),(91,110),(112,99),(112,249),(91,239),(91,165),(77,191),(63,166),(63,221),(48,213)]
c26=[(161,68),(195,89),(195,145),(172,145),(172,107),(161,99),(150,107),(150,238),(161,246),(172,238),(172,197),(195,197),(195,254),(161,277),(127,254),(127,89)]
DATA={
(1,5):logo(375,297,layer(0,m15,mirror(m15,187.5)),layer(0,w15,mirror(w15,187.5)),layer(0,c15)),
(1,6):logo(326,354,layer(0,o16,i16),layer(1,m16,mirror(m16,163),c16)),
(1,7):logo(274,354,layer(0,roof17,roof17b,bottom17),layer(1,m17,mirror(m17,137),c17)),
(1,9):logo(335,317,layer(1,m19,mirror(m19,168)),layer(0,c19,b19,mirror(b19,168))),
(2,1):logo(386,313,layer(0,o21,i21),layer(0,d21,m21,mirror(m21,193),c21)),
(2,2):logo(319,303,layer(1,m22,mirror(m22,160)),layer(0,c22)),
(2,3):logo(374,270,layer(0,roof23,c23),layer(1,m23,mirror(m23,187))),
(2,4):logo(355,254,layer(1,top24,bot24),layer(0,m24,mirror(m24,177),c24,side24,mirror(side24,177))),
(2,5):logo(381,204,layer(1,m25,mr25),layer(0,c25,t25,b25)),
(2,6):logo(322,345,layer(1,o26,i26),layer(0,d26,m26,mirror(m26,161),c26))}
IDS={(1,5):'1RIrzJpkMmS4Q4tu_85LjlM0PPB0dWMne',(1,6):'1HlW_E3M3LHz9ddIR_WfjFp3SvnxhRjBm',(1,7):'1NKizrU2i63S7bsRYKNUguLeOllyxbyat',(1,9):'1gfszrYaow3XWHHpZaA7INrJyLqtFWhD7',(2,1):'1W9Qprp4WVM0cDpz1cZAG-k7KlsF-gJ8c',(2,2):'1IBuI5PQu68mjxIzi-yasCPeV2N4vtE6n',(2,3):'1VFWI3qAY3uyXgTu1KUCTg0ZeQwAsjidE',(2,4):'1WobAExx5YpO4zz4Zl9z_nH8Mcsc40USH',(2,5):'1UrJuqKuK8hAiBcBFruXHzBJNP3Yh3Qhy',(2,6):'1ZLvApBQd05hCv_aw44BYC_fxh6_npoox'}

def generate():
    entries=[];seen={}
    # Limited exact-byte audit: all downloaded sources, not the full Drive folder.
    for source in sorted((R/'google_drive').glob('*logo-*.png')):
        digest=hashlib.sha256(source.read_bytes()).hexdigest()
        seen.setdefault(digest,[]).append(source.name)
    for (group,n),data in DATA.items():
        key=f'exp-{group:03}-{n:02}';source=R/f'google_drive/Max_a_Gambar_kotak_berisi__{group}_logo-{n:02}.png'
        digest=hashlib.sha256(source.read_bytes()).hexdigest()
        entry=dict(id=key,group=group,sourceNumber=n,driveId=IDS[group,n],sourceName=source.name,sourceSha256=digest,status='geometric-redraw-awaiting-user-review',masterSvg=f'04-desain/variasi-svg/batch-03/{key}.svg',pathJson=f'04-desain/variasi-svg/batch-03/{key}.json',format='manual-vector',appIntegration='deferred-until-collection-complete')
        (OUT/f'{key}.json').write_text(json.dumps(data,indent=2))
        svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {data["width"]} {data["height"]}">'
        for l in data['layers']:
            d=' '.join(c[0]+' '+' '.join(str(v) for v in c[1:]) for c in l['commands'])
            svg+=f'<path fill="{["#DC2626","#173257","#FFFFFF"][l["color"]]}" fill-rule="evenodd" d="{d}"/>'
        svg+='</svg>';(OUT/f'{key}.svg').write_text(svg)
        subprocess.run(['node','-e',"const fs=require('fs'),{Resvg}=require(process.argv[1]);fs.writeFileSync(process.argv[3],new Resvg(fs.readFileSync(process.argv[2]),{background:'#FFFFFF',fitTo:{mode:'width',value:700}}).render().asPng());",str(R/'.cache/mcm-redraw/node_modules/@resvg/resvg-js'),str(OUT/f'{key}.svg'),str(OUT/f'{key}-preview.png')],check=True)
        entries.append(entry)
    progress=dict(batch='03',apkBuildsPaused=True,newMasterCount=len(entries),driveSourcesWithMasters=15,reportedDriveFiles=342,remainingNotProcessed=327,groups={'1':dict(redrawn=list(range(1,10)),pending=[]),'2':dict(redrawn=list(range(1,7)),pending=[7,8,9])},exactDuplicateAudit=dict(scope='15 downloaded PNG files only',filesChecked=sum(map(len,seen.values())),duplicateGroups=[v for v in seen.values() if len(v)>1]),notes=['No claim of pixel-identical reconstruction or production approval.','M pairs are symmetrized except italic source 2/05; source palette flattened.','No app catalog changes; existing 11 logo IDs and favorites remain untouched.'],entries=entries)
    (OUT/'progress.json').write_text(json.dumps(progress,indent=2))
    page='''<!doctype html><html lang="id"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Batch 03 · 10 master vektor</title><style>body{font:16px system-ui;background:#e9eef5;color:#173257;margin:0}main{max-width:1100px;margin:auto;padding:24px}.pair{display:grid;grid-template-columns:1fr 1fr;gap:16px}.card{background:white;border-radius:12px;padding:16px;overflow:auto}.art{height:350px;display:grid;place-items:center}.art img,.art svg{width:100%;height:100%;max-height:350px;object-fit:contain}h1{font-size:28px}h2{margin-top:36px}p{line-height:1.6}.hint{color:#526176}@media(max-width:600px){.pair{grid-template-columns:1fr}.art{height:260px}}</style><main><h1>Batch 03 · 10 master path vektor</h1><p>Kelompok 1 selesai 9/9; kelompok 2 selesai 6/9. Semua perbandingan berdampingan: raster sumber dan redraw koordinat manual. Bentuk serta ruang negatif dipertahankan secara geometris, bukan klaim identik piksel. Tekstur warna diratakan. Tidak ada build APK atau perubahan katalog aplikasi.</p>'''
    for e in entries:
        encoded=base64.b64encode((R/'google_drive'/e['sourceName']).read_bytes()).decode()
        page+=f'<section><h2>Kelompok {e["group"]} · Logo {e["sourceNumber"]:02}</h2><p class="hint">ID tetap: {e["id"]}</p><div class="pair"><div class="card"><h3>Sumber Drive</h3><div class="art"><img alt="Sumber {e["id"]}" src="data:image/png;base64,{encoded}"></div></div><div class="card"><h3>Redraw geometris</h3><div class="art">{(R/e["masterSvg"]).read_text()}</div></div></div></section>'
    (OUT/'perbandingan.html').write_text(page+'</main></html>')
    print('Built 10 design masters. No Android build. No app assets modified.')
if __name__=='__main__':generate()
