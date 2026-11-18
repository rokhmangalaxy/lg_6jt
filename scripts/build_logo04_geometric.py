"""Manual geometric reconstruction of logo 04, not an image trace.
Render dependency: npm install --prefix .cache/mcm-redraw @resvg/resvg-js
"""
from pathlib import Path
import base64
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '04-desain/redraw-geometris-04'
OUT.mkdir(parents=True, exist_ok=True)
RED = '#DC2626'
# Symmetry axis x=170. Original silhouette/proportions are the reference,
# not a pixel-exact trace. Every segment below is deliberately straight.
DIAMOND = [(170,32),(308,150),(170,268),(32,150)]
M_LEFT = [(72,136),(89,122),(103,149),(117,104),(133,90),(133,212),
          (117,199),(117,151),(103,182),(87,151),(87,179),(72,166)]
M_RIGHT = [(340-x,y) for x,y in M_LEFT]
C = [(170,63),(196,84),(196,129),(179,129),(179,91),(170,82),
     (161,91),(161,209),(170,218),(179,209),(179,171),(196,171),
     (196,216),(170,237),(144,216),(144,84)]
CONTOURS = [DIAMOND, M_LEFT, C, M_RIGHT]
def contour(points):
    return 'M ' + ' L '.join(f'{x} {y}' for x,y in points) + ' Z'
d = ' '.join(contour(points) for points in CONTOURS)
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="340" height="300" viewBox="0 0 340 300" role="img" aria-labelledby="title desc">
<title id="title">MCM — redraw geometris logo 04</title>
<desc id="desc">Siluet diamond merah dengan MCM sebagai ruang negatif. Konstruksi manual, semua segmen lurus, kedua M bercermin pada x=170.</desc>
<path fill="{RED}" fill-rule="evenodd" d="{d}"/>
</svg>'''
(OUT/'mcm-04-geometris.svg').write_text(svg)
# Candidate native path data, intentionally NOT deployed into app assets.
commands=[]
for points in CONTOURS:
    commands += [['M',*points[0]], *[['L',*p] for p in points[1:]], ['Z']]
(OUT/'mcm-04-geometris.json').write_text(json.dumps(dict(width=340,height=300,layers=[dict(color=0,commands=commands)]),indent=2))
(OUT/'konstruksi.json').write_text(json.dumps(dict(axisX=170,red=RED,canvas=[340,300],diamond=DIAMOND,mLeft=M_LEFT,c=C,mRight=M_RIGHT),indent=2))
renderer = ROOT/'.cache/mcm-redraw/node_modules/@resvg/resvg-js'
for name,background,width in [('mcm-04-geometris-putih.png','#FFFFFF',2400),('mcm-04-geometris-transparan.png',None,2400),('preview-geometris.png','#FFFFFF',1000)]:
    options=dict(fitTo=dict(mode='width',value=width))
    if background:options['background']=background
    subprocess.run(['node','-e',"const fs=require('fs'),{Resvg}=require(process.argv[1]);fs.writeFileSync(process.argv[3],new Resvg(fs.readFileSync(process.argv[2]),JSON.parse(process.argv[4])).render().asPng());",str(renderer),str(OUT/'mcm-04-geometris.svg'),str(OUT/name),json.dumps(options)],check=True)
# Construction diagram is supplemental; main SVG contains no diagram or labels.
construction=svg.replace(f'<path fill="{RED}"', '<rect width="340" height="300" fill="white"/><path fill="#DC2626"')
construction=construction.replace('</svg>','''<g fill="none" stroke="#173257" stroke-width="0.6" opacity="0.7"><path stroke-dasharray="3 3" d="M170 12 V288 M12 150 H328"/><rect x="32" y="32" width="276" height="236"/></g></svg>''')
(OUT/'diagram-konstruksi.svg').write_text(construction)
original=base64.b64encode((ROOT/'04-desain/ekstraksi-logo-04/mcm-04-simbol.png').read_bytes()).decode()
svgdata=base64.b64encode(svg.encode()).decode()
pngdata=base64.b64encode((OUT/'mcm-04-geometris-putih.png').read_bytes()).decode()
page='''<!doctype html><html lang="id"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>MCM 04 · Redraw geometris</title><style>*{box-sizing:border-box}body{margin:0;color:#173257;background:#e9eef5;font:16px system-ui}main{max-width:1200px;margin:auto;padding:32px 20px}h1{font-size:28px}header p{max-width:850px;line-height:1.6;color:#526176}.controls{display:flex;flex-wrap:wrap;align-items:center;gap:16px;margin:24px 0}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,380px),1fr));gap:24px}article{background:#fff;padding:20px;border-radius:16px}h2{font-size:18px}.stage{background:var(--bg,#fff);height:420px;overflow:auto;border:1px solid #dbe2ec;display:block}.stage img,.stage svg{width:100%;height:auto;display:block;max-width:none}.actions{display:flex;flex-wrap:wrap;gap:12px;margin:20px 0}a,button{font:inherit;color:#173257;padding:12px 16px;background:#fff;border:1px solid #bdc9d8;border-radius:10px;text-decoration:none;cursor:pointer}a:focus-visible,button:focus-visible,input:focus-visible{outline:3px solid #dc2626}p,li{line-height:1.6}small{color:#526176}.note{font-size:14px;color:#526176}@media(max-width:500px){.stage{height:330px}}</style><main><header><small>MASTER KANDIDAT · LOGO NO. 4</small><h1>Dari piksel ke konstruksi geometris</h1><p>Bukan auto-trace: diamond dan inisial disusun ulang dari koordinat terukur. Segmen seluruhnya lurus, dua M saling bercermin. Ini kandidat perapian untuk disetujui, bukan penggantian otomatis logo dalam APK.</p></header><div class="controls"><label for="zoom">Pembesaran <output id="z">100%</output></label><input id="zoom" type="range" min="100" max="400" value="100" step="25"><button id="bg">Latar putih / abu-abu</button></div><section class="grid"><article><h2>Sumber raster</h2><div class="stage"><img alt="Ekstraksi asli logo no.4" src="data:image/png;base64,__ORIGINAL__"></div><p class="note">Sumber 339 × 300 px. Ketidakteraturan piksel akan terlihat saat diperbesar.</p></article><article><h2>Redraw geometris</h2><div class="stage">__SVG__</div><p class="note">Satu path, empat kontur, tanpa font, tanpa kurva. Inisial menjadi lubang transparan pada bidang merah.</p></article></section><div class="actions"><a download="mcm-04-geometris.svg" href="data:image/svg+xml;base64,__SVGDATA__">↓ Master SVG</a><a download="mcm-04-geometris-putih.png" href="data:image/png;base64,__PNGDATA__">↓ PNG latar putih</a></div><ul><li>Diamond: tepat empat sisi lurus.</li><li>Sumbu simetri vertikal: x = 170.</li><li>M kanan adalah pencerminan M kiri, bukan digambar terpisah.</li><li>C memakai chamfer/sudut potong; sudut yang tadinya membulat sengaja ditegaskan.</li><li>Proporsi mengikuti sumber, tetapi tidak diklaim identik piksel demi piksel.</li></ul><p class="note">Pada sumber raster, putih sudah menyatu dengan latar. Pada master SVG baru, area inisial transparan dan mengikuti warna permukaan. Pilih PNG putih untuk tampilan merah–putih yang sama. Belum diuji ukuran bordir atau kemiripan merek.</p></main><script>document.getElementById('zoom').oninput=e=>{document.getElementById('z').textContent=e.target.value+'%';document.querySelectorAll('.stage img,.stage svg').forEach(v=>v.style.width=e.target.value+'%')};let gray=false;document.getElementById('bg').onclick=()=>{gray=!gray;document.documentElement.style.setProperty('--bg',gray?'#d1d5db':'#fff')};</script></html>'''
page=page.replace('__ORIGINAL__',original).replace('__SVG__',svg).replace('__SVGDATA__',svgdata).replace('__PNGDATA__',pngdata)
(OUT/'perbandingan.html').write_text(page)
print('Built geometric SVG, JSON, transparent/white PNGs and standalone comparison')
