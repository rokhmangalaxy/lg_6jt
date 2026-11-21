"""Ten hand-measured source-specific rasio polygon masters, design-only."""
from build_drive_batch_03 import layer,mirror,logo
from design_batch_io import export_batch
from pathlib import Path
import json,hashlib,math
R=Path(__file__).resolve().parents[1]
def circle(x,y,r):return [(round(x+r*math.cos(i*math.pi/8),3),round(y+r*math.sin(i*math.pi/8),3)) for i in range(16)]
# 18/01 diamond, four detached navy facets and compact navy lettering.
f1=[(215,37),(422,142),(215,261),(9,142)]
t1=[(16,130),(189,9),(213,31)]
u1=[(218,31),(243,9),(416,130)]
b1=[(16,154),(183,284),(213,265)]
v1=[(219,265),(416,154),(246,284)]
m1=[(88,107),(109,107),(130,132),(153,107),(174,107),(174,185),(149,185),(149,148),(130,168),(112,148),(112,185),(88,185)]
c1=[(200,106),(234,106),(242,109),(248,115),(251,123),(251,137),(226,137),(226,130),(222,126),(209,126),(205,130),(205,162),(209,166),(222,166),(226,162),(226,157),(251,157),(251,170),(248,178),(241,184),(232,187),(200,187),(191,184),(185,178),(182,169),(182,124),(185,115),(191,109)]
# 18/02 red gussets and navy I-beam rails with filleted junctions.
t2=[(74,9),(283,9),(283,26),(211,26),(203,27),(198,30),(196,36),(196,71),(159,71),(159,36),(157,30),(152,27),(145,26),(74,26)]
g2=[(79,31),(145,31),(151,33),(154,37),(154,54),(129,54)]
b2=[(58,233),(146,233),(153,231),(157,226),(159,219),(159,195),(196,195),(196,219),(198,226),(203,231),(211,233),(297,233),(297,250),(58,250)]
h2=[(63,228),(110,207),(154,207),(154,220),(152,225),(147,228)]
m2=[(9,81),(33,81),(64,117),(99,81),(119,81),(119,186),(89,186),(89,135),(65,159),(41,135),(41,186),(9,186)]
c2=[(150,80),(205,80),(215,84),(222,92),(225,101),(225,123),(191,123),(191,111),(188,108),(164,108),(161,111),(161,156),(164,159),(188,159),(191,156),(191,146),(225,146),(225,166),(221,175),(214,182),(205,186),(150,186),(140,182),(132,174),(129,165),(129,101),(133,92),(141,85)]
# 18/03 four frame facets, red tall central C.
t3=[(9,81),(168,9),(168,47),(9,108)]
b3=[(9,201),(168,263),(168,296),(9,223)]
m3=[(9,118),(35,107),(59,130),(92,93),(114,93),(114,220),(83,211),(83,150),(61,174),(38,150),(38,204),(9,193)]
c3=[(171,73),(218,95),(218,133),(188,133),(188,118),(171,110),(154,118),(154,193),(171,201),(188,193),(188,165),(218,165),(218,216),(171,238),(124,216),(124,95)]
# 18/04 segmented perspective rails, red central C.
t4=[(9,61),(182,9),(182,36),(9,82)]
u4=[(18,87),(182,46),(182,63),(48,92)]
b4=[(9,209),(180,257),(180,286),(9,228)]
v4=[(18,205),(48,201),(180,229),(180,247)]
m4=[(14,98),(39,98),(70,129),(102,98),(125,98),(125,195),(94,195),(94,150),(70,173),(46,150),(46,195),(14,195)]
c4=[(146,98),(182,84),(228,101),(228,135),(197,135),(197,117),(181,112),(165,117),(165,178),(181,183),(197,178),(197,164),(228,164),(228,195),(182,211),(134,195),(134,109),(137,102)]
# 18/05 oblique navy Ms/red C and two solid rails.
t5=[(110,9),(371,9),(349,35),(80,35)]
b5=[(38,155),(319,155),(286,185),(9,185)]
m5=[(50,46),(79,46),(90,73),(125,46),(156,46),(117,144),(84,144),(105,94),(74,118),(63,91),(42,144),(10,144)]
mr5=[(261,46),(294,46),(304,73),(340,46),(371,46),(332,144),(300,144),(320,94),(287,119),(277,93),(255,144),(223,144)]
c5=[(179,46),(249,46),(235,83),(206,83),(211,71),(186,71),(167,119),(193,119),(198,107),(225,107),(211,144),(128,144),(160,65),(166,53),(172,48)]
# 18/06 mounting holes cut through navy ring; red field with navy lettering.
o6=[(9,58),(189,9),(369,58),(369,194),(189,242),(9,194)]
i6=[(33,78),(189,36),(344,78),(344,174),(189,216),(33,174)]
f6=[(39,82),(189,42),(338,82),(338,169),(189,210),(39,169)]
m6=[(51,83),(74,83),(95,110),(116,83),(139,83),(139,168),(114,168),(114,127),(95,148),(76,127),(76,168),(51,168)]
c6=[(173,82),(202,82),(211,85),(219,92),(225,101),(225,117),(198,117),(198,109),(194,105),(179,105),(175,109),(175,143),(179,147),(194,147),(198,143),(198,136),(225,136),(225,150),(221,160),(213,167),(203,170),(173,170),(162,167),(154,160),(149,150),(149,102),(154,92),(162,85)]
# 18/07 red vertical C with tilted arms, navy double base rails.
m7=[(26,97),(51,83),(69,118),(93,57),(120,39),(120,205),(91,215),(91,128),(78,150),(71,157),(58,142),(57,224),(26,235)]
c7=[(174,9),(209,33),(209,109),(184,98),(184,54),(173,47),(158,56),(158,208),(173,216),(184,208),(184,180),(209,171),(209,206),(173,225),(131,206),(131,34)]
a7=[(9,250),(122,214),(157,228),(9,270)]
b7=[(16,279),(173,234),(330,279),(298,286),(173,253),(48,286)]
# 18/08 red hex C between angular high-shouldered navy Ms.
m8=[(9,102),(47,77),(73,102),(110,36),(152,9),(152,43),(142,49),(142,184),(152,190),(152,210),(108,185),(108,114),(81,152),(44,124),(44,169),(9,192)]
c8=[(214,17),(274,52),(274,87),(241,87),(241,72),(214,56),(184,73),(184,158),(214,176),(241,160),(241,144),(274,144),(274,178),(214,212),(152,178),(152,52)]
# 18/09 nested narrow diamond rings and four positive navy mounting dots.
o9=[(210,9),(406,140),(209,275),(9,140)]
i9=[(210,20),(393,140),(209,265),(23,140)]
r9=[(210,27),(384,140),(209,257),(33,140)]
j9=[(210,36),(372,140),(209,248),(46,140)]
m9=[(102,109),(116,109),(134,129),(150,109),(167,109),(167,176),(148,176),(148,143),(134,159),(120,143),(120,176),(102,176)]
c9=[(208,94),(238,109),(239,114),(239,133),(218,133),(218,122),(208,116),(197,122),(197,162),(208,168),(218,162),(218,151),(239,151),(239,173),(236,177),(208,191),(178,176),(176,172),(176,114),(179,109)]
# rasio1/01: wider red diamond with navy lettering and four separate tips.
f10=[(211,33),(412,138),(211,245),(9,138)]
t10=[(14,131),(192,9),(209,27)]
u10=[(214,27),(231,9),(407,131)]
b10=[(14,146),(189,266),(209,250)]
v10=[(214,250),(407,146),(234,266)]
m10=[(95,105),(115,105),(133,125),(152,105),(172,105),(172,174),(149,174),(149,140),(133,158),(116,140),(116,174),(95,174)]
c10=[(196,105),(228,105),(237,108),(243,115),(246,123),(246,132),(222,132),(222,125),(218,122),(206,122),(202,126),(202,153),(206,157),(218,157),(222,154),(222,148),(246,148),(246,158),(243,166),(236,172),(227,175),(196,175),(187,172),(181,165),(179,157),(179,124),(181,116),(187,108)]
DATA={
(18,1):logo(431,293,layer(1,t1,u1,b1,v1),layer(0,f1),layer(1,m1,[(x+171,y) for x,y in m1],c1)),
(18,2):logo(357,259,layer(1,t2,b2,m2,[(x+225,y) for x,y in m2]),layer(0,g2,mirror(g2,178.5),h2,mirror(h2,178.5),c2)),
(18,3):logo(343,305,layer(0,t3,mirror(t3,171.5),c3),layer(1,b3,mirror(b3,171.5),m3,mirror(m3,171.5))),
(18,4):logo(364,295,layer(0,t4,u4,mirror(b4,182),mirror(v4,182),c4),layer(1,mirror(t4,182),mirror(u4,182),b4,v4,m4,[(x+223,y) for x,y in m4])),
(18,5):logo(380,195,layer(0,t5,c5),layer(1,b5,m5,mr5)),
(18,6):logo(378,251,layer(1,o6,i6,*[circle(x,y,7) for x,y in [(25,68),(21,126),(25,184),(189,24),(351,68),(355,128),(351,184),(189,229)]]),layer(0,f6),layer(1,m6,[(x+183,y) for x,y in m6],c6)),
(18,7):logo(346,296,layer(0,c7),layer(1,m7,mirror(m7,173),a7,mirror(a7,173),b7)),
(18,8):logo(426,221,layer(0,c8),layer(1,m8,mirror(m8,213))),
(18,9):logo(415,284,layer(1,o9,i9),layer(0,r9,j9,c9),layer(1,m9,[(x+147,y) for x,y in m9],*[circle(x,y,7) for x,y in [(210,53),(65,140),(350,140),(209,232)]])),
(1,1):logo(421,275,layer(1,t10,u10,b10,v10),layer(0,f10),layer(1,m10,[(x+147,y) for x,y in m10],c10))}
VALUES=['1rKsC7GztAyscVjtegS1gwyAV6ehQ3iQz','1wdsblgFKpuF-kQJgpMJFgh-H0biVqn76','1MNviexi6u5CV7yQQAhtiBevG_V0-gcUp','1U4dBsY-_NAHrclh6NEEDejz0qprnhBtm','18jm2HoZjxM0cIS9Vjm19bClMfibr7LDb','1_dk4bMZOxZnYpYbwoaNNLTm_T9ndr_xd','1U29KLo7zknYyu-sxPk8riNH23vavY7Uk','1jl7hCin1U15gozLGQ17KrinmNYrQm3HC','1Zv2zVmlZi91j12I2o5khs0KfICU7jN7R','1tdJxWeEWS3Qfgwt4J2IRb2srC_Oe_cOh']
if __name__=='__main__':
    old=json.loads((R/'04-desain/variasi-svg/batch-22/progress.json').read_text())
    groups=old['groups'];groups['rasio-18']=dict(redrawn=list(range(1,10)),pending=[]);groups['rasio-1']=dict(redrawn=[1],pending=list(range(2,10)))
    names={k:f'Max_a_Gambar_kotak_rasio_1_{k[0]}_logo-{k[1]:02}.png' for k in DATA}
    seen={e['sourceSha256'] for p in (R/'04-desain/variasi-svg').glob('batch-*/progress.json') if p.parent.name!='batch-23' for e in json.loads(p.read_text())['entries']}
    for name in names.values():
        digest=hashlib.sha256((R/'google_drive'/name).read_bytes()).hexdigest()
        assert digest not in seen, f'Duplicate source requires alias audit: {name}'
        seen.add(digest)
    export_batch('23',DATA,dict(zip(DATA,VALUES)),199,groups,source_names=names,entry_ids={k:f'exp-rasio-{k[0]:03}-{k[1]:02}' for k in DATA})
    out=R/'04-desain/variasi-svg/batch-23';p=json.loads((out/'progress.json').read_text())
    p.update(uniqueDriveMasters=199,driveSourcesCoveredIncludingDuplicates=217,remainingNotProcessed=125,progressPercent=round(217/342*100,2),redrawOnlyPercent=round(199/342*100,2),progressBasis='199 manual masters + 18 verified duplicate source files / 342 reported files',sourceAliases=old['sourceAliases'],buildPolicy='Redraw only; all APK jobs paused; Android catalog unchanged.')
    for e in p['entries']:e.update(sourceFamily='rasio_1',appIntegration='deferred-no-apk-requested')
    (out/'progress.json').write_text(json.dumps(p,indent=2))
    page=(out/'perbandingan.html').read_text().replace('199 dari 342 sumber','199 master unik; 217 dari 342 sumber tercakup').replace('<strong>143</strong>','<strong>125</strong>').replace('58.19%','63.45%').replace('Kelompok 18 ·','Keluarga rasio_1 · Kelompok 18 ·').replace('Kelompok 1 ·','Keluarga rasio_1 · Kelompok 1 ·')
    page=page.replace('</main>','<h2>Audit terbatas</h2><p>199 master unik + 18 alias = 217/342 (63,45%), sisa 125. Redraw unik saja: 199/342 (58,19%). Sepuluh hash baru berbeda satu sama lain dan dari sumber master terdahulu. 342 bukan jumlah desain unik terverifikasi. Lubang mounting 18/06 transparan; empat titik navy 18/09 positif. Tidak ada build APK atau perubahan katalog aplikasi.</p></main>')
    (out/'perbandingan.html').write_text(page)
