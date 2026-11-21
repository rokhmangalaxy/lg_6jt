"""Non-destructive manual review corrections; no APK/catalog edits."""
from pathlib import Path
import json,base64,subprocess,hashlib
R=Path(__file__).resolve().parents[1];O=R/'04-desain/perbaikan-review/putaran-01';O.mkdir(parents=True,exist_ok=True)
entries=json.loads((R/'android-logo/app/src/main/assets/exploration/catalog.json').read_text())['reviewedEntries']
notes={5:'sudut terlalu lancip',44:'Bagian atas huruf c',49:'',50:'garis putih yng menempel dari bawah huruf c',64:'Sisi dalam kaki huruf M terlalu mepet ke bawah',115:'',122:'',123:'Atas bawah aneh yang siku biru',128:'Huruf M sisi kanan tidak sesuai',169:'',170:'Huruf c kasar, tidak sama, harusnya rapi',179:'Udah sama, tapi modifikasi huruf c agar rapi, gpp tidak sama, logo aslinya memang sudah jelek',184:'garis potong putih atas bawah tidak konsisten lebarnya',188:'Sisi dalam atas bagian huruf M kasar, kurang rapi',205:'',206:'Huruf c kurang rapi',278:'Huruf c kurang rapi',281:'Huruf c kurang rapi',284:'Huruf c kurang rapi',287:'bagian atas ada space putih tipis',290:'atas warna merah kurang rapi',294:'biru pojok kanan kurang rapi',301:'bagian atas kurang rapi',302:'',303:'',304:'',313:'',322:'',328:'Huruf c kurang rapi'}
records=[dict(variation=n,id=e['id'],sourceName=e['sourceName'],userStatus='Perlu perbaikan',userNote=notes[n],status='pending-source-comparison') for e in entries if (n:=int(e['name'].split()[-1])) in notes]
groups=[dict(members=[115,169,205],representative=205,reason='Diamond merah dengan MCM navy dan empat tip navy; proporsi 205 paling seimbang untuk master kerja.'),dict(members=[304,313,322],representative=313,reason='Diamond merah dengan MCM putih; 313 dipilih sebagai master kerja. Cap kontinu 322 adalah detail yang sengaja tidak dijadikan varian terpisah pada usulan konsolidasi.')]
# Chamfered polygon rounding, preserving the original diamond bounding box and letters.
def rounded_polygon(vertices,cut):
    import math
    result=[]
    for i,p in enumerate(vertices):
        a=vertices[i-1];b=vertices[(i+1)%len(vertices)]
        def towards(q):
            d=math.dist(p,q);return (p[0]+(q[0]-p[0])*cut/d,p[1]+(q[1]-p[1])*cut/d)
        start=towards(a);end=towards(b)
        for t in [0,.25,.5,.75,1]:
            result.append(['M' if not result else 'L',round((1-t)**2*start[0]+2*(1-t)*t*p[0]+t*t*end[0],2),round((1-t)**2*start[1]+2*(1-t)*t*p[1]+t*t*end[1],2)])
    return result+[['Z']]
fixed=[]
for number in [5,44,50]:
    e=next(e for e in entries if e['name']==f'Variasi {number:02}')
    data=json.loads((R/'android-logo/app/src/main/assets'/e['vectorAsset']).read_text())
    if number==5:
        data['layers'][0]['commands']=rounded_polygon([(180,8),(350,172),(180,336),(10,172)],18)
        change='Empat ujung diamond dilunakkan dengan chord pendek; huruf putih tidak diubah.'
    elif number==44:
        commands=data['layers'][1]['commands'];commands[0]=['M',192,9];del commands[1]
        change='Cap C merah dibuat satu apex di tengah mengikuti sumber, bukan puncak datar dua titik.'
    else:
        # The center slit must end below the C counter, not meet its bottom vertex.
        commands=data['layers'][1]['commands']
        commands[4]=['L',152,292];commands[5]=['L',145,292]
        change='Ujung atas slit tengah diturunkan dari y=275 ke y=292 agar terpisah 17 unit dari ujung counter C, tetap terbuka ke bawah.'
    key=e['id'];(O/f'{key}.json').write_text(json.dumps(data,indent=2))
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {data["width"]} {data["height"]}">'
    for l in data['layers']:
        d=' '.join(c[0]+' '+' '.join(map(str,c[1:])) for c in l['commands'])
        svg+=f'<path fill="{["#DC2626","#173257","#FFFFFF"][l["color"]]}" fill-rule="evenodd" d="{d}"/>'
    svg+='</svg>';(O/f'{key}.svg').write_text(svg)
    fixed.append(dict(variation=number,id=key,change=change,svg=svg))
    next(r for r in records if r['variation']==number).update(status='corrected-awaiting-visual-review',change=change)
page='''<!doctype html><html lang="id"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Perbaikan review 01</title><style>body{background:#111827;color:#e5e7eb;font:16px system-ui;margin:24px}main{max-width:1200px;margin:auto}.pair{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}.art{background:#d1d5db;padding:12px}.art img,.art svg{width:100%;height:280px;object-fit:contain}p{line-height:1.6}@media(max-width:650px){.pair{grid-template-columns:1fr}}</style><main><h1>Perbaikan review · putaran 01</h1><p>29 item perlu perbaikan. Tiga koreksi awal; dua kelompok kandidat konsolidasi. Tidak ada build APK, perubahan katalog, penghapusan ID atau perubahan logo berstatus Sesuai. Penilaian kemiripan visual bukan skor 90% terukur.</p>'''
def image(path):return '<img src="data:image/png;base64,'+base64.b64encode(path.read_bytes()).decode()+'">'
for f in fixed:
    root=R/'android-logo/app/src/main/assets/temporary-review'
    page+=f'<h2>Variasi {f["variation"]:02}</h2><p>{f["change"]}</p><div class="pair"><div class="art">Asli'+image(root/f'{f["id"]}-source.png')+'</div><div class="art">Sebelum'+image(root/f'{f["id"]}-redraw.png')+'</div><div class="art">Koreksi'+f['svg']+'</div></div>'
for g in groups:
    page+=f'<h2>Kandidat konsolidasi {g["members"]} → {g["representative"]}</h2><p>{g["reason"]} Belum diterapkan ke aplikasi.</p><div class="pair">'
    for n in g['members']:
        e=next(e for e in entries if e['name']==f'Variasi {n:02}')
        page+=f'<div class="art">Variasi {n}'+image(R/'android-logo/app/src/main/assets/temporary-review'/f'{e["id"]}-source.png')+'</div>'
    page+='</div>'
page+='</main></html>'; (O/'perbandingan.html').write_text(page)
(O/'review.json').write_text(json.dumps(dict(scope='29 user-marked repairs only; approved items unchanged',records=records,consolidationCandidates=groups,applicationMappingApplied=False,apkBuilt=False,excludedNote=dict(variation=98,reason='Application feature note, not geometry')),indent=2))
print('29 review items recorded; 3 corrected working copies; 2 consolidation candidates; app unchanged.')
