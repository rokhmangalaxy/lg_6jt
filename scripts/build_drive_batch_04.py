"""Manual measured polygons for Drive group 2/07–09. Design-only outputs."""
from pathlib import Path
import base64
import hashlib
import json
import subprocess
from build_drive_batch_03 import layer, mirror, logo
R=Path(__file__).resolve().parents[1]
OUT=R/'04-desain/variasi-svg/batch-04'
# Source 07: narrow navy M shoulders under independent red wing, pointed C.
m27=[(23,33),(71,78),(120,47),(120,237),(89,195),(89,110),(71,123),(54,105),(54,152),(23,110)]
c27=[(150,41),(197,41),(216,58),(216,117),(185,117),(185,75),(180,70),(167,70),(161,75),(161,223),(173,235),(185,223),(185,175),(216,175),(216,244),(173,306),(130,244),(130,58)]
wing27=[(9,9),(339,9),(309,34),(208,34),(202,31),(146,31),(140,34),(39,34)]
# Source 08: chamfered C ends, no enclosing outline; angular M pair.
m28=[(9,23),(13,23),(62,68),(106,34),(106,268),(73,246),(73,110),(57,122),(41,106),(41,225),(9,201)]
c28=[(137,9),(195,9),(215,28),(215,108),(178,92),(178,50),(174,46),(158,46),(154,50),(154,240),(158,245),(174,245),(178,241),(178,201),(215,183),(215,263),(195,282),(137,282),(117,263),(117,28)]
# Source 09: horizontally stretched diamond; two triangular counter accents.
outer29=[(196,9),(382,110),(382,164),(196,265),(9,164),(9,110)]
inner29=[(196,27),(369,120),(369,154),(196,247),(22,154),(22,120)]
field29=[(196,37),(360,124),(360,150),(196,238),(31,150),(31,125)]
m29=[(80,115),(97,105),(109,128),(123,93),(148,80),(148,199),(125,187),(125,143),(110,169),(96,146),(96,172),(80,163)]
c29=[(196,53),(229,72),(229,119),(205,119),(205,87),(196,81),(185,88),(185,190),(196,197),(205,191),(205,157),(229,157),(229,205),(196,227),(162,206),(162,73)]
triangle29=[(42,139),(65,126),(65,152)]
DATA={
    7:logo(348,314,layer(1,m27,mirror(m27,174)),layer(0,wing27,c27)),
    8:logo(335,291,layer(1,m28,mirror(m28,167.5)),layer(0,c28)),
    9:logo(391,274,layer(1,outer29,inner29),layer(0,field29,m29,mirror(m29,196),c29,triangle29,mirror(triangle29,196)))
}
IDS={7:'1CCQn9_aj7lSjj_yGdG9u5T02EqzhCMw-',8:'17uu9WqGHvwLqSX8i4EgEGmxJczzfNrKA',9:'1TL-cMeI6JIaqrrJ3iE6fqEqE-2PrSqkb'}

def generate():
    OUT.mkdir(parents=True,exist_ok=True)
    entries=[]
    for n,data in DATA.items():
        key=f'exp-002-{n:02}'
        source=R/f'google_drive/Max_a_Gambar_kotak_berisi__2_logo-{n:02}.png'
        entry=dict(id=key,group=2,sourceNumber=n,driveId=IDS[n],sourceName=source.name,
                   sourceSha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                   status='geometric-redraw-awaiting-user-review',
                   masterSvg=f'04-desain/variasi-svg/batch-04/{key}.svg',
                   pathJson=f'04-desain/variasi-svg/batch-04/{key}.json',
                   format='manual-vector',appIntegration='deferred-until-collection-complete')
        (OUT/f'{key}.json').write_text(json.dumps(data,indent=2))
        svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {data["width"]} {data["height"]}">'
        for l in data['layers']:
            d=' '.join(c[0]+' '+' '.join(str(v) for v in c[1:]) for c in l['commands'])
            svg+=f'<path fill="{["#DC2626","#173257","#FFFFFF"][l["color"]]}" fill-rule="evenodd" d="{d}"/>'
        (OUT/f'{key}.svg').write_text(svg+'</svg>')
        subprocess.run(['node','-e',"const fs=require('fs'),{Resvg}=require(process.argv[1]);fs.writeFileSync(process.argv[3],new Resvg(fs.readFileSync(process.argv[2]),{background:'#FFFFFF',fitTo:{mode:'width',value:700}}).render().asPng());",str(R/'.cache/mcm-redraw/node_modules/@resvg/resvg-js'),str(OUT/f'{key}.svg'),str(OUT/f'{key}-preview.png')],check=True)
        entries.append(entry)
    seen={}
    for source in sorted((R/'google_drive').glob('*logo-*.png')):
        digest=hashlib.sha256(source.read_bytes()).hexdigest()
        seen.setdefault(digest,[]).append(source.name)
    progress=dict(batch='04',apkBuildsPaused=True,newMasterCount=3,driveSourcesWithMasters=18,
                  reportedDriveFiles=342,remainingNotProcessed=324,
                  groups={str(g):dict(redrawn=list(range(1,10)),pending=[]) for g in (1,2)},
                  exactDuplicateAudit=dict(scope='downloaded PNG files only, not entire Drive folder',filesChecked=sum(map(len,seen.values())),duplicateGroups=[v for v in seen.values() if len(v)>1]),
                  visualReview=dict(scope='three new sources compared against downloaded group 1 and 2 references',result='distinct layouts; similar MCM motifs retained, not merged as duplicates',requiresUserApproval=True),
                  notes=['342 is the previously reported file count, not a verified unique-design total.',
                         'Historical batch progress is a snapshot, not a current cumulative ledger.',
                         'Colors flattened; hand-measured polygons regularized, not pixel-identical.',
                         'No Android build or app catalog change.'],entries=entries)
    (OUT/'progress.json').write_text(json.dumps(progress,indent=2))
    page='''<!doctype html><html lang="id"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Batch 04 · Kelompok 2 selesai</title><style>body{font:16px system-ui;background:#e9eef5;color:#173257;margin:0}main{max-width:1100px;margin:auto;padding:24px}.pair{display:grid;grid-template-columns:1fr 1fr;gap:16px}.card{background:white;border-radius:12px;padding:16px;overflow:auto}.art{height:350px;display:grid;place-items:center}.art img,.art svg{width:100%;height:100%;max-height:350px;object-fit:contain}h1{font-size:28px}h2{margin-top:36px}p{line-height:1.6}.hint{color:#526176}@media(max-width:600px){.pair{grid-template-columns:1fr}.art{height:260px}}</style><main><h1>Batch 04 · Tiga master path vektor</h1><p>Kelompok 1 dan 2 kini masing-masing memiliki master 9/9. Total 18 sumber Drive sudah dibuat path; koleksi keseluruhan belum selesai. Sumber asli di kiri, redraw koordinat manual di kanan. Warna bertekstur diratakan; bentuk dirapikan tanpa mengubah konsep. Semua hasil masih menunggu review visual pengguna. Tidak ada build APK.</p>'''
    for e in entries:
        encoded=base64.b64encode((R/'google_drive'/e['sourceName']).read_bytes()).decode()
        page+=f'<section><h2>Kelompok 2 · Logo {e["sourceNumber"]:02}</h2><p class="hint">{e["id"]}</p><div class="pair"><div class="card"><h3>Sumber Drive</h3><div class="art"><img alt="Sumber {e["id"]}" src="data:image/png;base64,{encoded}"></div></div><div class="card"><h3>Redraw geometris</h3><div class="art">{(R/e["masterSvg"]).read_text()}</div></div></div></section>'
    (OUT/'perbandingan.html').write_text(page+'</main></html>')
    print('3 manual SVG/JSON masters created. No APK build.')
if __name__=='__main__':generate()
