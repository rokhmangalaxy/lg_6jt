"""Third manual repair pass. Working vectors only; no tracing or catalog mutation."""
from pathlib import Path
import json,base64,math
R=Path(__file__).resolve().parents[1];O=R/'04-desain/perbaikan-review/putaran-03';O.mkdir(parents=True,exist_ok=True)
entries=json.loads((R/'android-logo/app/src/main/assets/exploration/catalog.json').read_text())['reviewedEntries']
review=json.loads((R/'04-desain/perbaikan-review/putaran-02/review.json').read_text())
def paths(cmds):
    result=[]
    for c in cmds:
        if c[0]=='M':result.append([])
        result[-1].append(c)
    return result

def polygon(points):
    clean=[]
    for point in points:
        if not clean or point!=clean[-1]:clean.append(point)
    return [['M' if i==0 else 'L',*p] for i,p in enumerate(clean)]+[['Z']]
def replace(data,layer,idx,points):
    p=paths(data['layers'][layer]['commands']);p[idx]=polygon(points)
    data['layers'][layer]['commands']=[c for part in p for c in part]

def clean_c(x0,y0,x1,y1,stem,bar,r,ri,gap):
    # Explicitly constructed C; circular corners approximated with six chords per quadrant.
    def arc(cx,cy,rad,a,b):
        return [(round(cx+rad*math.cos(math.radians(a+(b-a)*i/6)),3),round(cy+rad*math.sin(math.radians(a+(b-a)*i/6)),3)) for i in range(7)]
    mid=(y0+y1)/2;lo=mid-gap/2;hi=mid+gap/2
    left=x0+stem;top=y0+bar;bottom=y1-bar;right=x1-stem
    pts=[(x1,lo),(x1,y0+r)]
    pts+=arc(x1-r,y0+r,r,0,-90)[1:]
    pts+=[(x0+r,y0)]+arc(x0+r,y0+r,r,-90,-180)[1:]
    pts+=[(x0,y1-r)]+arc(x0+r,y1-r,r,180,90)[1:]
    pts+=[(x1-r,y1)]+arc(x1-r,y1-r,r,90,0)[1:]
    pts+=[(x1,hi),(right,hi),(right,bottom-ri)]
    pts+=arc(right-ri,bottom-ri,ri,0,90)[1:]
    pts+=[(left+ri,bottom)]+arc(left+ri,bottom-ri,ri,90,180)[1:]
    pts+=[(left,top+ri)]+arc(left+ri,top+ri,ri,180,270)[1:]
    pts+=[(right-ri,top)]+arc(right-ri,top+ri,ri,270,360)[1:]
    pts+=[(right,lo)]
    return pts
changes={49:'Segitiga dan C dipusatkan di x=207; kedua M dicerminkan sehingga margin bingkai seimbang.',122:'Kaki luar kedua M merah yang terlalu panjang dipendekkan ke garis bawah yang sesuai sumber; puncak bingkai navy dibuat simetris.',170:'C navy bawah dibuat berkontur membulat teratur dan counter simetris, bukan rangkaian sudut kasar.',206:'C navy dibangun ulang dengan radius sudut seragam dan ketebalan atas/bawah sama.',278:'C pada lettering bawah dirapikan dengan sudut membulat teratur, tanpa mengganti simbol atas.',281:'C tinggi dirapikan dengan radius luar 22 dan radius dalam 5; counter serta bukaan atas/bawah simetris.',284:'C lettering bawah dibuat membulat teratur; simbol merah/navy atas tidak disentuh.',290:'Cap merah atas disimetriskan terhadap x=166.5; kedua sudut luar dan lembah tengah disejajarkan.',302:'Dua bidang merah dipusatkan di x=170, sisi stem dibuat vertikal; pasangan cap navy disimetriskan terhadap sumbu sama.',303:'Bingkai navy bawah diturunkan 8 unit untuk memutus pertemuan dengan kaki M kanan; kanvas diperluas satu unit agar margin tetap.'}
results=[]
for n,change in changes.items():
    e=next(e for e in entries if int(e['name'].split()[-1])==n)
    d=json.loads((R/'android-logo/app/src/main/assets'/e['vectorAsset']).read_text())
    if n==49:
        replace(d,0,0,[(9,9),(405,9),(207,312)])
        replace(d,0,1,[(31,22),(383,22),(207,288)])
        p=paths(d['layers'][1]['commands'])
        p[1]=[[c[0],414-c[1],c[2]] if len(c)==3 else c for c in p[0]]
        p[2]=[[c[0],c[1]+2,c[2]] if len(c)==3 else c for c in p[2]]
        d['layers'][1]['commands']=[c for part in p for c in part]
    elif n==122:
        p=paths(d['layers'][1]['commands'])
        for i in [0,1]:p[i][10][2]=244;p[i][11][2]=240
        d['layers'][1]['commands']=[c for part in p for c in part]
        replace(d,0,0,[(161.5,9),(309,76),(278,93),(161.5,39),(45,93),(14,76)])
    elif n in [170,206,278,281,284]:
        settings={170:(122,214,210,297,29,21,20,5,16,4),206:(131,104,227,198,31,24,23,6,20,4),278:(113,236,187,305,24,19,17,5,17,4),281:(122,86,199,251,28,39,22,5,41,2),284:(112,186,187,260,24,20,18,5,18,4)}
        *args,index=settings[n]
        replace(d,1,index,clean_c(*args))
    elif n==290:
        replace(d,0,0,[(14,25),(57,10),(166.5,55),(276,10),(319,25),(166.5,97)])
    elif n==302:
        replace(d,0,0,[(145,26),(170,9),(195,26),(195,95),(145,95)])
        replace(d,0,1,[(145,218),(195,218),(195,282),(170,297),(145,282)])
        p=paths(d['layers'][1]['commands'])
        for i,j in [(0,2),(1,3)]:p[j]=[[c[0],340-c[1],c[2]] if len(c)==3 else c for c in p[i]]
        d['layers'][1]['commands']=[c for part in p for c in part]
    elif n==303:
        p=paths(d['layers'][1]['commands']);p[0]=[[c[0],c[1],c[2]+8] if len(c)==3 else c for c in p[0]]
        d['layers'][1]['commands']=[c for part in p for c in part];d['height']=215
    key=e['id'];(O/f'{key}.json').write_text(json.dumps(d,indent=2)+'\n')
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {d["width"]} {d["height"]}">'
    for l in d['layers']:
        path=' '.join(c[0]+' '+' '.join(map(str,c[1:])) for c in l['commands'])
        svg+=f'<path fill="{["#DC2626","#173257","#FFFFFF"][l["color"]]}" fill-rule="evenodd" d="{path}"/>'
    svg+='</svg>';(O/f'{key}.svg').write_text(svg)
    results.append(dict(variation=n,id=key,change=change,svg=svg))
    next(r for r in review['records'] if r['variation']==n).update(status='corrected-awaiting-visual-review',change=change,round=3)
review['progress']=dict(correctedWorkingCopies=23,totalRepairItems=29,remaining=6,percent=round(2300/29,1))
(O/'review.json').write_text(json.dumps(review,indent=2)+'\n')
page='''<!doctype html><html lang="id"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Perbaikan review 02</title><style>body{background:#111827;color:#e5e7eb;font:16px system-ui;margin:24px}main{max-width:1200px;margin:auto}.pair{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}.art{background:#d1d5db;color:#111827;padding:12px}.art img,.art svg{width:100%;height:280px;object-fit:contain}p{line-height:1.6}@media(max-width:650px){.pair{grid-template-columns:1fr}}</style><main><h1>Perbaikan review · putaran 03</h1><p>10 koreksi manual tambahan. Kumulatif 23/29 (79,3%); tersisa 6 item. Ini salinan kerja untuk review visual, belum diterapkan ke APK. Katalog, ID, favorit dan logo Sesuai tidak berubah. Enam item tersisa adalah anggota kandidat konsolidasi putaran 01; pemetaannya belum diterapkan.</p>'''
def img(p):return '<img src="data:image/png;base64,'+base64.b64encode(p.read_bytes()).decode()+'">'
for f in results:
    root=R/'android-logo/app/src/main/assets/temporary-review'
    page+=f'<h2>Variasi {f["variation"]:02}</h2><p>{f["change"]}</p><div class="pair"><div class="art">Asli'+img(root/f'{f["id"]}-source.png')+'</div><div class="art">Sebelum'+img(root/f'{f["id"]}-redraw.png')+'</div><div class="art">Koreksi'+f['svg']+'</div></div>'
(O/'perbandingan.html').write_text(page+'</main></html>')
print(review['progress'])
