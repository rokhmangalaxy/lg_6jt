"""Design-only export helpers; no Android integration or build commands."""
from pathlib import Path
import base64
import hashlib
import html
import json
import subprocess
R=Path(__file__).resolve().parents[1]
PALETTE=['#DC2626','#173257','#FFFFFF']
def export_batch(batch,data_by_source,drive_ids,total,groups):
    out=R/f'04-desain/variasi-svg/batch-{batch}'
    out.mkdir(parents=True,exist_ok=True)
    entries=[]
    for (group,n),data in data_by_source.items():
        key=f'exp-{group:03}-{n:02}'
        source=R/f'google_drive/Max_a_Gambar_kotak_berisi__{group}_logo-{n:02}.png'
        entry=dict(id=key,group=group,sourceNumber=n,driveId=drive_ids[group,n],sourceName=source.name,
                   sourceSha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                   status='geometric-redraw-awaiting-user-review',
                   masterSvg=f'04-desain/variasi-svg/batch-{batch}/{key}.svg',
                   pathJson=f'04-desain/variasi-svg/batch-{batch}/{key}.json',
                   format='manual-vector',appIntegration='deferred-until-collection-complete')
        (out/f'{key}.json').write_text(json.dumps(data,indent=2))
        svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {data["width"]} {data["height"]}">'
        for l in data['layers']:
            d=' '.join(c[0]+' '+' '.join(str(v) for v in c[1:]) for c in l['commands'])
            svg+=f'<path fill="{PALETTE[l["color"]]}" fill-rule="evenodd" d="{d}"/>'
        (out/f'{key}.svg').write_text(svg+'</svg>')
        subprocess.run(['node','-e',"const fs=require('fs'),{Resvg}=require(process.argv[1]);fs.writeFileSync(process.argv[3],new Resvg(fs.readFileSync(process.argv[2]),{background:'#FFFFFF',fitTo:{mode:'width',value:700}}).render().asPng());",str(R/'.cache/mcm-redraw/node_modules/@resvg/resvg-js'),str(out/f'{key}.svg'),str(out/f'{key}-preview.png')],check=True)
        entries.append(entry)
    seen={}
    for source in sorted((R/'google_drive').glob('*logo-*.png')):
        digest=hashlib.sha256(source.read_bytes()).hexdigest()
        seen.setdefault(digest,[]).append(source.name)
    progress=dict(batch=batch,apkBuildsPaused=True,newMasterCount=len(entries),driveSourcesWithMasters=total,
                  reportedDriveFiles=342,remainingNotProcessed=342-total,progressPercent=round(total/342*100,2),progressBasis='source files with path masters / previously reported Drive file count; not verified unique designs',groups=groups,
                  exactDuplicateAudit=dict(scope='downloaded PNG files only, not entire Drive folder',filesChecked=sum(map(len,seen.values())),duplicateGroups=[v for v in seen.values() if len(v)>1]),
                  visualReview=dict(scope='new sources compared against downloaded references; no full-folder visual audit',result='source-specific layouts retained; similar motifs not automatically merged',requiresUserApproval=True),
                  notes=['342 is a previously reported file count, not a verified unique-design total.',
                         'Historical progress files are snapshots.',
                         'Colors flattened; hand-measured polygons regularized, not pixel-identical.',
                         'No Android build or app catalog change.'],entries=entries)
    (out/'progress.json').write_text(json.dumps(progress,indent=2))
    page=f'''<!doctype html><html lang="id"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Batch {batch} · {len(entries)} master</title><style>body{{font:16px system-ui;background:#e9eef5;color:#173257;margin:0}}main{{max-width:1100px;margin:auto;padding:24px}}.pair{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}.card{{background:white;border-radius:12px;padding:16px;overflow:auto}}.art{{height:350px;display:grid;place-items:center}}.art img,.art svg{{width:100%;height:100%;max-height:350px;object-fit:contain}}h1{{font-size:28px}}h2{{margin-top:36px}}p{{line-height:1.6}}.hint{{color:#526176}}button{{padding:10px 18px;border-radius:8px;border:1px solid #9baabd;background:white;color:#173257;cursor:pointer}}body.gray .art{{background:#D1D5DB}}@media(max-width:600px){{.pair{{grid-template-columns:1fr}}.art{{height:260px}}}}</style><main><h1>Batch {batch} · {len(entries)} master path vektor</h1><p>Sudah redraw <strong>{total} dari 342 sumber</strong> · Sisa <strong>{342-total}</strong> · Progres <strong>{total/342*100:.2f}%</strong>. Acuan: jumlah file Drive yang sebelumnya dilaporkan, bukan total desain unik terverifikasi. Koleksi keseluruhan belum selesai. Sumber asli di kiri, redraw koordinat manual di kanan. Warna bertekstur diratakan; hasil menunggu review visual pengguna. Tidak ada build APK.</p><button onclick="document.body.classList.toggle('gray')">Latar master: putih / abu-abu</button><p class="hint">Latar abu-abu membantu memeriksa lubang transparan. Raster sumber tetap memiliki latar putih aslinya. SVG master tidak berisi raster atau font.</p>'''
    for e in entries:
        encoded=base64.b64encode((R/'google_drive'/e['sourceName']).read_bytes()).decode()
        page+=f'<section><h2>Kelompok {e["group"]} · Logo {e["sourceNumber"]:02}</h2><p class="hint">{html.escape(e["id"])}</p><div class="pair"><div class="card"><h3>Sumber Drive</h3><div class="art"><img alt="Sumber {e["id"]}" src="data:image/png;base64,{encoded}"></div></div><div class="card"><h3>Redraw geometris</h3><div class="art">{(R/e["masterSvg"]).read_text()}</div></div></div></section>'
    (out/'perbandingan.html').write_text(page+'</main></html>')
    print(f'{len(entries)} manual SVG/JSON masters created. No APK build.')
