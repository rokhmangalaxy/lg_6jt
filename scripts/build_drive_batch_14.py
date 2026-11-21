"""Ten hand-measured source-specific masters. No tracing, app integration or APK."""
from build_drive_batch_03 import layer,mirror,logo
from design_batch_io import export_batch
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1]
# 13/01: positive red diamond field; white MCM are independent recolorable shapes.
o1=[(208,9),(407,175),(208,342),(10,175)]
i1=[(208,34),(377,175),(208,317),(39,175)]
f1=[(208,45),(364,175),(208,306),(52,175)]
m1=[(78,166),(99,148),(114,171),(135,119),(159,99),(159,263),(136,244),(136,184),(116,214),(98,191),(98,217),(78,201)]
c1=[(208,68),(240,96),(240,149),(219,149),(219,108),(208,98),(197,108),(197,246),(208,256),(219,246),(219,206),(240,206),(240,260),(208,289),(176,260),(176,96)]
# 13/02: detached navy hexagon rails; navy M pair, tall red C.
cap2=[(175,9),(341,82),(341,102),(175,35),(10,102),(10,82)]
foot2=[(10,224),(175,291),(341,224),(341,246),(175,315),(10,246)]
m2=[(10,123),(44,108),(63,151),(87,93),(119,80),(119,265),(87,251),(87,179),(65,214),(40,175),(40,232),(10,218)]
c2=[(175,49),(216,73),(216,132),(185,132),(185,96),(175,89),(165,96),(165,229),(175,236),(185,229),(185,196),(216,196),(216,253),(175,277),(134,253),(134,73)]
# 13/03: angular navy Ms around the red elongated hexagonal C.
m3=[(9,67),(61,103),(123,48),(123,263),(88,231),(88,136),(61,165),(36,143),(36,212),(9,187)]
c3=[(194,9),(241,44),(241,105),(207,105),(207,63),(194,53),(181,63),(181,221),(194,231),(207,221),(207,181),(241,181),(241,240),(194,275),(147,240),(147,44)]
# 13/04: three separated navy triangle frame pieces, not a solid triangle.
cap4=[(201,9),(320,176),(262,135),(201,53),(141,135),(82,176)]
left4=[(10,295),(74,202),(74,240),(53,274),(171,274),(187,295)]
m4=[(83,196),(104,181),(119,207),(139,162),(158,147),(158,267),(136,267),(136,217),(120,245),(104,223),(104,267),(83,267)]
c4=[(201,115),(235,146),(235,192),(212,192),(212,157),(201,147),(190,157),(190,254),(201,265),(212,254),(212,229),(235,229),(235,270),(201,297),(167,270),(167,146)]
# 13/05: top-plane navy C and two separate red upright M faces.
c5=[(152,9),(291,83),(241,111),(205,92),(214,84),(152,50),(92,84),(152,116),(178,103),(223,128),(152,169),(10,89)]
m5=[(10,100),(46,120),(75,192),(101,147),(141,169),(141,315),(94,287),(94,216),(76,250),(48,210),(48,284),(10,262)]
# 13/06: nested shield rings. White lettering remains positive/recolorable.
o6=[(169,9),(329,85),(329,183),(315,218),(274,264),(226,305),(169,339),(112,305),(64,264),(23,218),(9,183),(9,85)]
i6=[(169,25),(315,95),(315,181),(302,212),(263,254),(216,294),(169,323),(122,294),(75,254),(36,212),(23,181),(23,95)]
f6=[(169,36),(303,102),(303,179),(291,205),(254,246),(210,284),(169,309),(128,284),(84,246),(47,205),(35,179),(35,102)]
m6=[(51,119),(69,119),(86,141),(110,103),(123,95),(123,245),(102,226),(102,173),(85,199),(69,175),(69,213),(51,192)]
c6=[(169,63),(204,88),(204,137),(181,137),(181,101),(169,92),(157,101),(157,254),(169,263),(181,254),(181,211),(204,211),(204,269),(169,291),(134,269),(134,88)]
# 13/07: short independent red/navy wing bars.
m7=[(89,106),(113,93),(124,120),(142,78),(169,62),(169,235),(143,218),(143,150),(125,180),(108,153),(108,195),(89,183)]
c7=[(216,31),(255,56),(255,112),(229,112),(229,78),(216,70),(203,78),(203,220),(216,228),(229,220),(229,185),(255,185),(255,240),(216,265),(177,240),(177,56)]
wing7=[(10,112),(81,112),(81,137),(22,137)]
bar7=[(26,149),(81,149),(81,178),(39,178)]
# 13/08: red upper/lower rails, navy Ms, tall red C.
cap8=[(145,9),(281,83),(281,111),(145,40),(10,111),(10,83)]
foot8=[(10,241),(145,312),(281,241),(281,269),(145,337),(10,269)]
m8=[(10,132),(32,120),(46,153),(66,102),(92,88),(92,261),(66,247),(66,178),(48,209),(30,177),(30,228),(10,217)]
c8=[(145,58),(184,80),(184,137),(157,137),(157,100),(145,92),(133,100),(133,252),(145,260),(157,252),(157,215),(184,215),(184,272),(145,294),(106,272),(106,80)]
# 13/09: long navy Ms; red C terminates in a long pointed tip.
m9=[(9,67),(59,104),(110,54),(110,278),(77,245),(77,153),(59,170),(38,153),(38,230),(9,202)]
c9=[(168,9),(210,43),(210,103),(181,103),(181,61),(168,51),(155,61),(155,246),(168,256),(181,246),(181,205),(210,205),(210,270),(193,287),(168,323),(144,287),(126,270),(126,43)]
# rasio 14/01: broad red diamond, navy split outer tips and block MCM.
o10a=[(9,139),(200,9),(218,30),(237,9),(422,139),(218,36)]
o10b=[(9,139),(218,241),(422,139),(237,268),(218,247),(199,268)]
f10=[(16,139),(218,40),(415,139),(218,237)]
m10=[(94,103),(119,103),(134,124),(152,103),(175,103),(175,179),(152,179),(152,137),(134,157),(116,137),(116,175),(94,175)]
# Chamfered corners measured by eye, not font glyph substitution.
c10=[(204,101),(236,101),(247,104),(253,113),(253,131),(230,131),(230,122),(225,118),(212,118),(207,122),(207,157),(211,161),(225,161),(230,157),(230,149),(253,149),(253,168),(247,176),(236,179),(201,179),(190,176),(183,168),(183,114),(189,105)]
DATA={
(13,1):logo(417,351,layer(0,o1,i1),layer(0,f1),layer(2,m1,mirror(m1,208.5),c1)),
(13,2):logo(351,324,layer(1,cap2,foot2,m2,mirror(m2,175.5)),layer(0,c2)),
(13,3):logo(388,283,layer(1,m3,mirror(m3,194)),layer(0,c3)),
(13,4):logo(403,305,layer(1,cap4,left4,mirror(left4,201.5)),layer(0,m4,mirror(m4,201.5),c4)),
(13,5):logo(305,325,layer(1,c5),layer(0,m5,mirror(m5,152.5))),
(13,6):logo(339,348,layer(1,o6,i6),layer(0,f6),layer(2,m6,mirror(m6,169.5),c6)),
(13,7):logo(432,283,layer(0,wing7,mirror(wing7,216),c7),layer(1,bar7,mirror(bar7,216),m7,mirror(m7,216))),
(13,8):logo(291,347,layer(0,cap8,foot8,c8),layer(1,m8,mirror(m8,145.5))),
(13,9):logo(337,332,layer(1,m9,mirror(m9,168.5)),layer(0,c9)),
(14,1):logo(431,276,layer(1,o10a,o10b),layer(0,f10),layer(1,m10,[(x+168,y) for x,y in m10],c10))}
# Align measured y origins to the actual source canvases, preserving aspect ratios.
DATA[13,7]['height']=253
for shape in DATA[13,7]['layers']:
    for cmd in shape['commands']:
        if cmd[0] in ('M','L'):cmd[2]-=22
DATA[13,8]['height']=337
for shape in DATA[13,8]['layers']:
    for cmd in shape['commands']:
        if cmd[0] in ('M','L'):cmd[2]=round(9+(cmd[2]-9)*319/328,2)
IDS={(13,n):v for n,v in enumerate(['1ABgmLlcHosOORDoK0qw2iLq_EnSy06-K','1CtZOQUyBSoPuccZtCeRgm9w8LVwnEUor','19Tr6f6Ss-0yWP5x_x9YI-m8WiMkAbvFB','1OeK-edGoH21SrRMSjj4ZofJKxfb3xbak','14rdfZzlw_qcUq2EfyFLG2DpOepsJp69m','1ZqNYeh3PD8D--cwvJj0D0kFDGYgO1SZc','1KUNM49hBAytKA5BF0JeojsG4UuKKNS2U','1pYpVQh0MsEiWbvvanS6zifDjnGbJhSj9','17QvpmfPs1_HA1rLTdWbJEghamPXBwUzF'],1)}
IDS[14,1]='1n-ksGC4eD40d0lUJ-4NP6RPyPuVHycZJ'
if __name__=='__main__':
    export_batch('14',DATA,IDS,109,{**{str(g):dict(redrawn=list(range(1,10)),pending=[]) for g in range(1,12)},'13':dict(redrawn=list(range(1,10)),pending=[]),'rasio-14':dict(redrawn=[1],pending=list(range(2,10)))},source_names={(14,1):'Max_a_Gambar_kotak_rasio_1_14_logo-01.png'},entry_ids={(14,1):'exp-rasio-014-01'})
    out=R/'04-desain/variasi-svg/batch-14';p=json.loads((out/'progress.json').read_text())
    a=R/'google_drive/Max_a_Gambar_kotak_berisi__13_logo-01.png';b=R/'google_drive/Max_a_Gambar_kotak_berisi__14_logo-01.png'
    digest=hashlib.sha256(a.read_bytes()).hexdigest();assert digest==hashlib.sha256(b.read_bytes()).hexdigest()
    old=json.loads((R/'04-desain/variasi-svg/batch-13/progress.json').read_text())['sourceAliases']
    aliases=old+[dict(group=14,sourceNumber=1,driveId='1knpdjmfDta6JtZLmOLvtR4vA6L7gC83w',sourceName=b.name,sourceSha256=digest,duplicateOf='exp-013-01',status='exact-byte-duplicate-no-new-redraw')]
    p.update(uniqueDriveMasters=109,driveSourcesCoveredIncludingDuplicates=119,remainingNotProcessed=223,progressPercent=round(119/342*100,2),redrawOnlyPercent=round(109/342*100,2),progressBasis='109 manual unique masters + 10 verified duplicate source files / 342 reported files',sourceAliases=aliases,buildPolicy='User requested continuation without APK; no workflow dispatch or app integration.')
    p['entries'][-1]['sourceFamily']='rasio_1';p['entries'][-1]['appIntegration']='deferred-no-apk-requested'
    (out/'progress.json').write_text(json.dumps(p,indent=2))
    page=(out/'perbandingan.html').read_text().replace('109 dari 342 sumber','109 master unik; 119 dari 342 sumber tercakup').replace('<strong>233</strong>','<strong>223</strong>').replace('31.87%','34.80%').replace('Kelompok 14 · Logo 01','Keluarga rasio_1 · Kelompok 14 · Logo 01')
    page=page.replace('</main>','<h2>Audit terbatas</h2><p>14/01 berisi identik byte dengan 13/01: satu alias, bukan redraw baru. Total 109 master unik + 10 sumber duplikat = 119/342 (34,80%), sisa 223. Redraw unik/342: 31,87%. Master kesepuluh berasal dari keluarga rasio_1, bukan berisi; ID terpisah mencegah benturan. Kelompok berisi 14/02–09 belum diaudit. Tidak ada integrasi aplikasi atau build APK.</p></main>')
    (out/'perbandingan.html').write_text(page)
