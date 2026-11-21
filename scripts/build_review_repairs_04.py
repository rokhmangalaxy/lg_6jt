"""Prepare two consolidated working masters; keep application ID mapping untouched."""
from pathlib import Path
import json,base64,math
R=Path(__file__).resolve().parents[1];O=R/'04-desain/perbaikan-review/putaran-04';O.mkdir(parents=True,exist_ok=True)
entries=json.loads((R/'android-logo/app/src/main/assets/exploration/catalog.json').read_text())['reviewedEntries']
review=json.loads((R/'04-desain/perbaikan-review/putaran-03/review.json').read_text())
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
groups={205:[115,169,205],313:[304,313,322]}
changes={205:'Master untuk 115/169/205: empat tip navy dicerminkan terhadap x=211 dan y=138; diamond merah diseimbangkan; M kanan dicerminkan dan C dirapikan.',313:'Master untuk 304/313/322: dipilih bentuk empat tip navy versi 313, bukan cap kontinu 322; tip dan diamond diseimbangkan; M dicerminkan, C putih dirapikan.'}
results=[]
for n,change in changes.items():
    e=next(e for e in entries if int(e['name'].split()[-1])==n)
    d=json.loads((R/'android-logo/app/src/main/assets'/e['vectorAsset']).read_text())
    cx,cy=(211,138) if n==205 else (208,127)
    tip=[(14,131),(192,9),(208.5,27)] if n==205 else [(12,116),(187,10),(205.5,28)]
    replace(d,0,0,tip)
    replace(d,0,1,[(2*cx-x,y) for x,y in tip])
    replace(d,0,2,[(x,2*cy-y) for x,y in tip])
    replace(d,0,3,[(2*cx-x,2*cy-y) for x,y in tip])
    diamond=[(211,33),(413,138),(211,243),(9,138)] if n==205 else [(9,127),(208,30),(407,127),(208,224)]
    replace(d,1,0,diamond)
    p=paths(d['layers'][2]['commands'])
    p[1]=[[c[0],2*cx-c[1],c[2]] if len(c)==3 else c for c in p[0]]
    d['layers'][2]['commands']=[c for part in p for c in part]
    params=(179,105,243,175,23,18,15,4,16) if n==205 else (174,96,242,163,24,16,14,4,17)
    replace(d,2,2,clean_c(*params))
    key=e['id'];(O/f'{key}.json').write_text(json.dumps(d,indent=2)+'\n')
    svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {d["width"]} {d["height"]}">'
    for l in d['layers']:
        path=' '.join(c[0]+' '+' '.join(map(str,c[1:])) for c in l['commands'])
        svg+=f'<path fill="{["#DC2626","#173257","#FFFFFF"][l["color"]]}" fill-rule="evenodd" d="{path}"/>'
    svg+='</svg>';(O/f'{key}.svg').write_text(svg)
    results.append(dict(variation=n,id=key,change=change,svg=svg))
    for r in review['records']:
        if r['variation'] in groups[n]:r.update(status='consolidated-working-master-awaiting-review',representative=n,change=change,round=4)
review['progress']=dict(individualCorrections=23,consolidatedMembers=6,consolidatedMasters=2,totalRepairItems=29,remaining=0,percent=100)
review['applicationMappingApplied']=False
review['consolidationCandidates']=[dict(g,workingMasterPrepared=True,applicationMappingApplied=False) for g in review['consolidationCandidates']]
(O/'review.json').write_text(json.dumps(review,indent=2)+'\n')
page='''<!doctype html><html lang="id"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Perbaikan review 02</title><style>body{background:#111827;color:#e5e7eb;font:16px system-ui;margin:24px}main{max-width:1200px;margin:auto}.pair{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}.art{background:#d1d5db;color:#111827;padding:12px}.art img,.art svg{width:100%;height:280px;object-fit:contain}p{line-height:1.6}@media(max-width:650px){.pair{grid-template-columns:1fr}}</style><main><h1>Perbaikan review · putaran 04</h1><p>Dua master konsolidasi untuk enam item tersisa. Cakupan salinan kerja 29/29 (100%): 23 koreksi individual dan enam item menjadi dua master. Ini salinan kerja untuk review visual, belum diterapkan ke APK. Katalog, ID, favorit dan logo Sesuai tidak berubah. 115/169/205 → 205; 304/313/322 → 313. Belum mengurangi katalog aplikasi.</p>'''
def img(p):return '<img src="data:image/png;base64,'+base64.b64encode(p.read_bytes()).decode()+'">'
for f in results:
    root=R/'android-logo/app/src/main/assets/temporary-review'
    page+=f'<h2>Variasi {f["variation"]:02}</h2><p>{f["change"]}</p><div class="pair"><div class="art">Asli'+img(root/f'{f["id"]}-source.png')+'</div><div class="art">Sebelum'+img(root/f'{f["id"]}-redraw.png')+'</div><div class="art">Koreksi'+f['svg']+'</div></div>'
page+='<h2>Anggota yang diwakili</h2><p>Sumber asli tetap diarsipkan; tidak ada rating atau catatan perangkat yang digabung otomatis.</p><div class="pair">'
for members in groups.values():
    for number in members:
        original=next(row for row in entries if int(row['name'].split()[-1])==number)
        page+=f'<div class="art">Variasi {number}'+img(R/'android-logo/app/src/main/assets/temporary-review'/f'{original["id"]}-source.png')+'</div>'
page+='</div>'
(O/'perbandingan.html').write_text(page+'</main></html>')
print(review['progress'])
