"""Build 20 editable geometric MCM explorations from original SVG paths (no fonts)."""
from pathlib import Path
import html, subprocess, json
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'03-konsep/lettering-mcm-20'
NAVY='#173257';RED='#DC2626'
def poly(points,color=NAVY):return f'<polygon points="{points}" fill="{color}"/>'
def path(d,color=NAVY):return f'<path d="{d}" fill="{color}"/>'
def rect(x,y,w,h,c=RED):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}"/>'
M='0,140 0,0 24,0 50,49 76,0 100,0 100,140 75,140 75,49 50,94 25,49 25,140'
C='100,0 100,30 28,30 28,110 100,110 100,140 0,140 0,0'
def m(c=NAVY,points=M):return poly(points,c)
def c(color=NAVY,points=C):return poly(points,color)
def group(content,x=0,y=0,sx=1,sy=1):return f'<g transform="translate({x} {y}) scale({sx} {sy})">{content}</g>'
def trip(a=None,b=None,d=None,gap=22):return (a or m())+group(b or c(),100+gap)+group(d or m(),200+2*gap)
def stroke(d,width=20,color=NAVY):return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="square" stroke-linejoin="miter"/>'
items=[]
def add(name,desc,body,w=344,h=140):items.append((name,desc,body,w,h))
add('Geometris Tegas','Batang tebal dan potongan lurus; dasar pembanding.',trip())
add('Rapat Vertikal','Huruf ramping, lebih tinggi, dengan ruang antarhuruf rapat.',group(trip(gap=14),sx=.78,sy=1.16),256,163)
add('Bentang Lebar','Proporsi melebar dan valley M lebih rendah.',group(trip(a=m(points='0,140 0,0 24,0 50,72 76,0 100,0 100,140 75,140 75,65 50,120 25,65 25,140'),d=m(points='0,140 0,0 24,0 50,72 76,0 100,0 100,140 75,140 75,65 50,120 25,65 25,140')),sx=1.18,sy=.86),406,121)
add('C Pilar','C lebih tinggi menjadi pusat; dua M sejajar di sisi.',group(m(),0,18)+group(c(RED),122,0,1,1.26)+group(m(),244,18),344,177)
add('Maju Presisi','Seluruh lettering condong, bukan wadah miring.',f'<g transform="translate(30 0) skewX(-12)">{trip()}</g>',374)
add('Stencil Lurus','Satu celah horizontal lebar membagi lettering menjadi bidang produksi.',trip()+rect(-1,63,347,13,'white'))
M7='0,140 0,0 25,0 50,32 75,0 100,0 100,140 73,140 73,54 50,78 27,54 27,140'
add('Puncak Pendek','Valley M dangkal dengan C berujung tebal merah.',trip(m(points=M7),c(RED),m(points=M7)))
M8='0,140 0,0 23,0 50,70 77,0 100,0 100,140 72,140 72,68 50,121 28,68 28,140'
add('Valley Dalam','M berlekuk dalam; bukaan C dipersempit dengan ujung tebal.',trip(m(RED,M8),c(points='100,0 100,48 73,48 73,28 28,28 28,112 73,112 73,92 100,92 100,140 0,140 0,0'),m(RED,M8)))
add('Potong Diagonal','Celah diagonal memisahkan bagian atas dan bawah.',trip()+poly('-5,80 350,39 350,53 -5,94','white'))
add('Sambungan Bawah','Tiga inisial dihubungkan oleh satu bidang bawah.',trip()+rect(18,124,308,16),344,140)
add('Dua Bidang','Dua zona warna solid, dipisahkan celah lurus tipis.',f'<defs><clipPath id="top"><rect x="-2" y="0" width="350" height="63"/></clipPath><clipPath id="bottom"><rect x="-2" y="75" width="350" height="70"/></clipPath></defs><g clip-path="url(#top)">{trip(m(RED),c(RED),m(RED))}</g><g clip-path="url(#bottom)">{trip()}</g>')
sm='M 10 130 V 10 L 50 76 L 90 10 V 130';sc='M 90 10 H 10 V 130 H 90'
add('Monoline Struktural','Ketebalan garis seragam; C terbuka dan sudut tegas.',trip(stroke(sm,18),stroke(sc,18,RED),stroke(sm,18)))
add('Rel Ganda','Batang rangkap yang terpisah celah putih; perlu uji ukuran kecil.',trip(stroke(sm,30)+stroke(sm,10,'white'),stroke(sc,30,RED)+stroke(sc,10,'white'),stroke(sm,30)+stroke(sm,10,'white')))
M14='0,140 0,0 28,0 28,28 50,28 50,52 72,52 72,0 100,0 100,140 74,140 74,86 50,86 50,62 26,62 26,140'
add('Bahu Bertingkat','Konstruksi M bertingkat; motif proses bertahap.',trip(m(points=M14),c(RED),m(points=M14)))
add('Ujung Terbuka','C berupa tiga batang terpisah; M memakai puncak rata.',trip(m(points='0,140 0,0 28,0 50,43 72,0 100,0 100,140 74,140 74,53 50,99 26,53 26,140'),rect(0,0,100,27,NAVY)+rect(0,39,27,62,RED)+rect(0,113,100,27,NAVY),m(points='0,140 0,0 28,0 50,43 72,0 100,0 100,140 74,140 74,53 50,99 26,53 26,140')))
C16='100,0 100,28 35,28 27,36 27,104 35,112 100,112 100,140 15,140 0,125 0,15 15,0'
add('Chamfer Metal','Sudut luar C dipotong; M diberi chamfer pada kaki.',trip(m()+poly('0,126 14,140 0,140','white')+poly('86,140 100,126 100,140','white'),c(RED,C16),m()+poly('0,126 14,140 0,140','white')+poly('86,140 100,126 100,140','white')))
M17='0,140 0,0 25,0 57,58 78,0 100,0 100,140 74,140 74,66 59,110 24,49 24,140'
add('Sayap Seimbang','Dua M saling bercermin dengan bidang C sebagai poros.',m(points=M17)+group(c(RED),122)+f'<g transform="translate(344 0) scale(-1 1)">{m(points=M17)}</g>')
ml='0,140 0,35 22,35 22,46 35,35 52,35 66,47 79,35 95,35 110,50 110,140 88,140 88,65 78,58 68,65 68,140 46,140 46,65 35,58 22,66 22,140'
cl='94,35 94,59 26,59 26,116 94,116 94,140 14,140 0,126 0,49 14,35'
add('mcm Huruf Kecil','Interpretasi lowercase bersudut, tanpa wadah.',poly(ml)+group(poly(cl,RED),132)+group(poly(ml),248),358)
add('C Jembatan','C lebih lebar dan rendah, dua M menjadi pilar samping.',group(m(),0,0,.84,1)+group(c(RED),102,20,1.18,.72)+group(m(),238,0,.84,1),322)
M20='0,122 0,0 23,0 50,53 77,0 100,0 100,122 75,122 75,49 50,95 25,49 25,122'
add('Kaki Terpisah','Batang huruf diangkat dari tiga kaki merah yang terpisah.',trip(m(points=M20),group(c(points=C),0,0,1,.87),m(points=M20))+rect(0,132,100,12)+rect(122,132,100,12)+rect(244,132,100,12),344,144)
OUT.mkdir(parents=True,exist_ok=True);(OUT/'svg').mkdir(exist_ok=True);(OUT/'png').mkdir(exist_ok=True)
cards=[];manifest=[]
for i,(name,desc,body,w,h) in enumerate(items,1):
 scale=min(620/w,205/h);x=(800-w*scale)/2;y=(400-h*scale)/2
 svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 400" width="1600" height="800" role="img" aria-label="MCM {i:02d} {html.escape(name)}"><title>MCM {i:02d} — {html.escape(name)}</title><rect width="800" height="400" fill="white"/><g transform="translate({x:.3f} {y:.3f}) scale({scale:.5f})">{body}</g></svg>'
 # Scope clip IDs per SVG so multiple inline previews cannot interfere.
 svg=svg.replace('id="top"',f'id="top{i}"').replace('url(#top)',f'url(#top{i})').replace('id="bottom"',f'id="bottom{i}"').replace('url(#bottom)',f'url(#bottom{i})')
 file=OUT/'svg'/f'mcm-{i:02d}.svg';file.write_text(svg)
 subprocess.run(['node','-e',"const fs=require('fs');const {Resvg}=require(process.argv[1]);fs.writeFileSync(process.argv[3],new Resvg(fs.readFileSync(process.argv[2])).render().asPng())",str(ROOT/'.cache/mcm-render/node_modules/@resvg/resvg-js'),str(file),str(OUT/'png'/f'mcm-{i:02d}.png')],check=True)
 cards.append(f'<article><div class="label">{i:02d} · {html.escape(name)}</div>{svg}<p>{html.escape(desc)}</p><button onclick="download(this,\'svg\')">↓ SVG</button> <button onclick="download(this,\'png\')">↓ PNG</button></article>')
 manifest.append(dict(number=i,name=name,description=desc,svg=f'svg/mcm-{i:02d}.svg',png=f'png/mcm-{i:02d}.png'))
(OUT/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
page='''<!doctype html><html lang="id"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>20 lettering MCM</title><style>*{box-sizing:border-box}body{margin:0;background:#e9eef5;color:#173257;font:16px system-ui}main{max-width:1250px;margin:auto;padding:32px 20px}h1{font-size:30px;margin-bottom:10px}header p{max-width:780px;line-height:1.6;color:#526176}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,440px),1fr));gap:24px;margin-top:30px}article{padding:22px;border-radius:20px;background:#e9eef5;box-shadow:7px 7px 16px #c2cbd7,-7px -7px 16px white}svg{display:block;width:100%;height:auto;background:#fff;border-radius:12px;margin:18px 0}.label{font-size:14px;font-weight:700}article p{font-size:14px;line-height:1.5;min-height:42px;color:#526176}button{padding:12px 18px;border-radius:10px;border:1px solid #c2cbd7;color:#173257;background:#f5f7fa;font:inherit;cursor:pointer}button:focus-visible{outline:3px solid #dc2626}footer{padding:30px 0;color:#526176;font-size:13px;line-height:1.6}</style><main><header><small>EKSPLORASI LETTERING · PT MENARA CIPTA METALINDO</small><h1>20 cara membaca MCM</h1><p>Tanpa wadah kotak atau lingkaran. Bandingkan bentuk huruf terlebih dahulu, bukan mockup. Merah dan biru tetap warna kerja; beberapa potongan tipis perlu diuji sebelum bordir. SVG berupa path/polygon, tidak bergantung font.</p></header><section class="grid">'''+''.join(cards)+'''</section><footer>Eksplorasi tipografi geometris, bukan master final. Makna desain adalah usulan, bukan filosofi resmi perusahaan. Belum dilakukan pengecekan kemiripan merek, uji keterbacaan, dan uji produksi. 20 variasi ini belum dimasukkan ke APK.</footer></main><script>
function save(blob,name){const url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),30000)}
function download(button,type){const article=button.closest('article'),svg=article.querySelector('svg'),n=[...document.querySelectorAll('article')].indexOf(article)+1,name='mcm-'+String(n).padStart(2,'0');const data=new XMLSerializer().serializeToString(svg);const blob=new Blob([data],{type:'image/svg+xml;charset=utf-8'});if(type==='svg'){save(blob,name+'.svg');return}const url=URL.createObjectURL(blob),im=new Image();im.onload=()=>{const c=document.createElement('canvas');c.width=1600;c.height=800;c.getContext('2d').drawImage(im,0,0,1600,800);c.toBlob(png=>{if(png)save(png,name+'.png')},'image/png');URL.revokeObjectURL(url)};im.onerror=()=>{URL.revokeObjectURL(url);alert('Gagal mengekspor PNG. Silakan gunakan SVG.')};im.src=url}
</script></html>'''
(OUT/'index.html').write_text(page)
print('Built',len(items),'SVGs, PNGs and standalone gallery')
if __name__=='__main__':assert len(items)==20
