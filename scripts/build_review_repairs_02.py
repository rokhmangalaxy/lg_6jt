"""Second manual geometry pass; working copies only, stable application assets untouched."""
from pathlib import Path
import json,base64
R=Path(__file__).resolve().parents[1];O=R/'04-desain/perbaikan-review/putaran-02';O.mkdir(parents=True,exist_ok=True)
entries=json.loads((R/'android-logo/app/src/main/assets/exploration/catalog.json').read_text())['reviewedEntries']
review=json.loads((R/'04-desain/perbaikan-review/putaran-01/review.json').read_text())

def paths(cmds):
    result=[]
    for c in cmds:
        if c[0]=='M':result.append([])
        result[-1].append(c)
    return result

def polygon(points):return [['M' if i==0 else 'L',*p] for i,p in enumerate(points)]+[['Z']]
def replace(data,layer,idx,points):
    p=paths(data['layers'][layer]['commands']);p[idx]=polygon(points)
    data['layers'][layer]['commands']=[c for part in p for c in part]

changes={
64:'Kedua kaki dalam M dipendekkan 12 unit; sisi bawah dinaikkan sejajar agar ruang ke bingkai bertambah tanpa mengubah C.',
123:'Cap navy atas/bawah dibuat simetris terhadap y=159; ujung dalam menjadi garis miring sejajar sisi luar, bukan siku horizontal.',
128:'M kanan dicerminkan dari M kiri terhadap sumbu x=210.5; margin luar kanan kembali 9 unit dan konstruksi kaki sama.',
179:'C dibangun ulang dengan kontur luar simetris dan counter heksagonal sederhana; takik liar di ujung bawah dihapus sesuai izin perapian.',
184:'Dua celah potong counter C dibuat sejajar: offset vertikal 14 unit di atas/bawah, lebar tegak lurus sekitar 13 unit.',
188:'Kedua transisi dalam atas M diluruskan menjadi satu diagonal tanpa sisi hampir vertikal pendek; pasangan kanan dicerminkan.',
287:'Kontur merah atas disatukan tepat pada seam navy x=130 dan x=230. Celah 1 unit di sisi kiri dihilangkan, seam kanan tetap bertemu.',
294:'Dua bidang navy kanan memakai garis potong diagonal sejajar x+y=479/491 sehingga jarak celah konstan, tanpa ujung yang melebar.',
301:'Kedua cap merah dan strip navy atas dicerminkan terhadap x=203; tebal strip 12 unit dan jarak merah–navy 4 unit dipertahankan vertikal.',
328:'C dibangun ulang simetris terhadap x=175; tebal stem 26 unit, counter atas/bawah mengikuti kemiringan yang konsisten tanpa takik.'}
results=[]
for n,change in changes.items():
    e=next(e for e in entries if int(e['name'].split()[-1])==n)
    d=json.loads((R/'android-logo/app/src/main/assets'/e['vectorAsset']).read_text())
    if n==64:
        p=paths(d['layers'][1]['commands'])
        for i in [0,1]:
            p[i][5][2]-=12;p[i][6][2]-=12
        d['layers'][1]['commands']=[c for part in p for c in part]
    elif n==123:
        top=[(200,9),(281,66),(200,40),(119,66)]
        replace(d,0,0,top);replace(d,0,1,[(x,318-y) for x,y in top])
    elif n==128:
        p=paths(d['layers'][1]['commands']);p[1]=[[c[0],421-c[1],c[2]] if len(c)==3 else c for c in p[0]]
        d['layers'][1]['commands']=[c for part in p for c in part]
    elif n==179:
        replace(d,1,2,[(176,62),(229,82),(229,121),(185,104),(162,113),(162,184),(185,193),(229,176),(229,215),(176,235),(124,215),(124,82)])
    elif n==184:
        # Inner lips share slope 5/13 with the left counter edges, not the old 18/51 vs 21/51 mismatch.
        replace(d,1,5,[(190,64),(241,84),(241,111),(190,91)])
        replace(d,1,6,[(190,204),(241,184),(241,218),(190,231)])
    elif n==188:
        p=paths(d['layers'][1]['commands']);del p[0][5]
        p[1]=[[c[0],366-c[1],c[2]] if len(c)==3 else c for c in p[0]]
        d['layers'][1]['commands']=[c for part in p for c in part]
    elif n==287:
        replace(d,1,0,[(130,9),(180,49),(230,9),(231,91),(180,130),(129,91)])
    elif n==294:
        replace(d,1,2,[(372,119),(372,154),(293,198)])
        replace(d,1,3,[(341,74),(372,74),(372,107),(341,138)])
    elif n==301:
        top=[(10,62),(135,9),(203,9),(59,78)]
        replace(d,0,0,top);replace(d,0,1,[(406-x,y) for x,y in top])
        leftA=[(10,66),(57,82),(57,94),(10,78)]
        leftB=[(61,82),(203,18),(203,30),(61,94)]
        replace(d,1,0,leftA);replace(d,1,1,leftB)
        replace(d,1,2,[(406-x,y) for x,y in leftB]);replace(d,1,3,[(406-x,y) for x,y in leftA])
    elif n==328:
        replace(d,1,2,[(134,95),(175,108),(216,95),(216,127),(190,135),(190,128),(175,133),(160,128),(160,173),(175,178),(190,173),(190,162),(216,154),(216,193),(175,207),(134,193)])
    key=e['id'];(O/f'{key}.json').write_text(json.dumps(d,indent=2)+'\n')
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {d["width"]} {d["height"]}">'
    for l in d['layers']:
        path=' '.join(c[0]+' '+' '.join(map(str,c[1:])) for c in l['commands'])
        svg+=f'<path fill="{["#DC2626","#173257","#FFFFFF"][l["color"]]}" fill-rule="evenodd" d="{path}"/>'
    svg+='</svg>';(O/f'{key}.svg').write_text(svg)
    results.append(dict(variation=n,id=key,change=change,svg=svg))
    next(r for r in review['records'] if r['variation']==n).update(status='corrected-awaiting-visual-review',change=change,round=2)
review['progress']=dict(correctedWorkingCopies=13,totalRepairItems=29,remaining=16,percent=round(1300/29,1))
(O/'review.json').write_text(json.dumps(review,indent=2)+'\n')
page='''<!doctype html><html lang="id"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Perbaikan review 02</title><style>body{background:#111827;color:#e5e7eb;font:16px system-ui;margin:24px}main{max-width:1200px;margin:auto}.pair{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}.art{background:#d1d5db;color:#111827;padding:12px}.art img,.art svg{width:100%;height:280px;object-fit:contain}p{line-height:1.6}@media(max-width:650px){.pair{grid-template-columns:1fr}}</style><main><h1>Perbaikan review · putaran 02</h1><p>10 koreksi manual tambahan. Kumulatif 13/29 (44,8%); tersisa 16 item. Ini salinan kerja untuk review visual, belum diterapkan ke APK. Katalog, ID, favorit dan logo Sesuai tidak berubah. Kandidat konsolidasi pada putaran 01 tetap belum diterapkan.</p>'''
def img(p):return '<img src="data:image/png;base64,'+base64.b64encode(p.read_bytes()).decode()+'">'
for f in results:
    root=R/'android-logo/app/src/main/assets/temporary-review'
    page+=f'<h2>Variasi {f["variation"]:02}</h2><p>{f["change"]}</p><div class="pair"><div class="art">Asli'+img(root/f'{f["id"]}-source.png')+'</div><div class="art">Sebelum'+img(root/f'{f["id"]}-redraw.png')+'</div><div class="art">Koreksi'+f['svg']+'</div></div>'
(O/'perbandingan.html').write_text(page+'</main></html>')
print(review['progress'])
