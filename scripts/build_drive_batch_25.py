"""Ten source-specific manual rasio polygon masters; design-only, no tracing/APK."""
from build_drive_batch_03 import layer,mirror,logo
from design_batch_io import export_batch
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1]
# 2/03 shallow red roof/base, navy Ms and tall C.
t1=[(9,58),(190,9),(370,58),(370,64),(190,42),(9,64)]
b1=[(9,183),(190,211),(370,183),(370,188),(190,245),(9,188)]
m1=[(9,78),(41,75),(66,107),(94,71),(125,68),(125,185),(92,179),(92,125),(66,155),(43,126),(43,176),(9,172)]
c1=[(190,60),(242,68),(242,115),(206,115),(206,94),(190,93),(175,95),(175,159),(190,162),(206,160),(206,140),(242,140),(242,185),(190,194),(138,185),(138,68)]
# 2/04 four alternating rails and navy Ms/red oblique C.
t2=[(232,9),(395,9),(375,29),(208,29)]
u2=[(194,38),(376,38),(362,52),(179,52)]
b2=[(30,183),(212,183),(197,197),(22,197)]
v2=[(28,205),(187,205),(169,223),(9,223)]
m2=[(46,62),(77,62),(82,99),(120,62),(159,62),(118,174),(83,174),(103,116),(70,151),(60,117),(43,174),(9,174)]
mr2=[(271,62),(303,62),(307,99),(341,62),(377,62),(344,174),(310,174),(326,116),(295,151),(283,117),(267,174),(235,174)]
c2=[(180,62),(261,62),(248,104),(213,104),(218,88),(193,88),(172,148),(199,148),(204,133),(239,133),(225,174),(128,174),(163,79),(168,69),(174,64)]
# 2/05 four detached red/navy facets around navy MCM.
t3=[(9,79),(179,9),(179,61),(9,94)]
u3=[(189,9),(359,79),(359,94),(189,61)]
b3=[(9,216),(179,252),(179,302),(9,233)]
v3=[(189,252),(359,216),(359,233),(189,302)]
m3=[(10,109),(42,104),(64,137),(87,98),(120,92),(120,223),(87,218),(87,157),(65,187),(44,158),(44,211),(10,205)]
c3=[(184,80),(238,90),(238,138),(201,138),(201,118),(184,116),(168,118),(168,197),(184,199),(201,197),(201,176),(238,176),(238,224),(184,234),(131,224),(131,90)]
# 2/06 inward-notched red strips and upright navy MCM.
t4=[(9,9),(128,9),(155,36),(226,36),(254,9),(371,9),(371,30),(262,30),(234,57),(147,57),(120,30),(9,30)]
b4=[(9,187),(125,187),(147,165),(233,165),(255,187),(371,187),(371,208),(247,208),(225,186),(155,186),(133,208),(9,208)]
m4=[(20,68),(51,68),(76,97),(100,68),(131,68),(131,154),(99,154),(99,113),(76,139),(53,113),(53,154),(20,154)]
c4=[(155,68),(226,68),(238,79),(238,103),(205,103),(205,91),(176,91),(176,132),(205,132),(205,119),(238,119),(238,143),(226,154),(155,154),(143,143),(143,80)]
# 2/07 red cap/base, long red C with diagonal arms, broad navy Ms.
t5=[(94,61),(188,9),(277,60),(277,97),(188,47),(94,97)]
b5=[(94,198),(187,246),(277,198),(277,234),(187,282),(94,234)]
m5=[(9,74),(45,92),(72,123),(130,89),(130,206),(94,188),(94,144),(70,167),(45,144),(45,195),(9,216)]
mr5=[(242,89),(302,124),(331,94),(372,69),(372,216),(334,196),(334,140),(307,165),(278,144),(278,188),(242,206)]
c5=[(184,65),(234,92),(234,130),(184,105),(171,112),(171,185),(184,192),(234,167),(234,205),(184,228),(138,205),(138,92)]
# 2/08 architectural roof with red center pier; detached navy MCM and red baseline.
t6=[(14,144),(131,45),(131,143)]
u6=[(139,38),(178,9),(214,37),(214,142),(139,142)]
b6=[(9,268),(346,268),(346,290),(9,290)]
m6=[(9,156),(40,156),(63,192),(85,156),(119,156),(119,256),(85,256),(85,209),(64,237),(41,209),(41,256),(9,256)]
c6=[(141,156),(211,156),(225,169),(225,197),(191,197),(191,181),(177,180),(163,181),(163,232),(177,234),(191,232),(191,219),(225,219),(225,244),(211,256),(141,256),(129,245),(129,169)]
# 2/09 navy outer cap/base, red side piers, navy Ms, pointed red tall C.
t7=[(28,86),(179,9),(327,86),(297,104),(179,46),(59,104)]
b7=[(28,266),(59,248),(179,307),(297,248),(327,266),(178,345)]
s7=[(9,94),(41,112),(41,241),(9,258)]
m7=[(49,121),(76,148),(96,113),(122,98),(122,255),(96,241),(96,175),(77,203),(61,180),(61,228),(49,235)]
c7=[(178,71),(225,96),(225,141),(194,141),(194,117),(178,109),(162,117),(162,235),(178,243),(194,235),(194,211),(225,211),(225,257),(178,281),(131,257),(131,96)]
# 3/01 broad white-letter diamond; four separately measured navy tips.
f8=[(220,33),(430,135),(219,242),(9,135)]
t8=[(16,123),(193,9),(218,28)]
u8=[(223,28),(247,9),(422,123)]
b8=[(16,146),(185,263),(217,247)]
v8=[(223,247),(422,146),(254,263)]
m8=[(96,99),(118,99),(136,128),(155,99),(176,99),(176,175),(152,175),(152,139),(136,160),(120,139),(120,175),(96,175)]
c8=[(205,99),(236,99),(245,102),(251,109),(254,117),(254,128),(230,128),(230,121),(226,117),(216,117),(212,121),(212,153),(216,157),(226,157),(230,153),(230,146),(254,146),(254,158),(250,167),(243,173),(235,175),(205,175),(196,172),(190,166),(187,157),(187,117),(191,108),(197,102)]
# 3/02 red cap and split-ended red base; navy Ms and tall C.
t9=[(9,91),(188,9),(367,91),(367,106),(188,40),(9,106)]
b9=[(24,229),(73,212),(188,254),(303,212),(351,229),(188,275)]
m9=[(9,118),(37,110),(65,139),(100,91),(126,79),(126,216),(92,205),(92,160),(68,191),(42,165),(42,212),(9,226)]
c9=[(188,53),(237,76),(237,116),(202,116),(202,95),(175,95),(175,196),(202,196),(202,175),(237,175),(237,216),(188,238),(140,217),(140,74)]
# 3/03 red chamfer strips outside navy nameplate, white positive MCM.
t10=[(74,9),(334,9),(365,39),(43,39)]
b10=[(9,126),(45,158),(365,158),(399,126),(399,139),(349,187),(60,187),(9,139)]
f10=[(34,49),(374,49),(399,74),(399,116),(364,148),(44,148),(9,116),(9,74)]
m10=[(58,62),(83,62),(106,89),(130,62),(154,62),(154,134),(128,134),(128,100),(106,123),(85,101),(85,134),(58,134)]
c10=[(184,62),(223,62),(232,65),(239,72),(242,80),(242,90),(215,90),(215,85),(211,81),(199,81),(194,85),(194,112),(198,116),(211,116),(215,112),(215,106),(242,106),(242,117),(238,126),(231,132),(222,134),(184,134),(175,131),(169,125),(166,116),(166,81),(169,72),(175,65)]
DATA={
(2,3):logo(380,253,layer(0,t1,b1),layer(1,m1,mirror(m1,190),c1)),
(2,4):logo(404,232,layer(0,t2,v2,c2),layer(1,u2,b2,m2,mr2)),
(2,5):logo(368,311,layer(0,u3,b3),layer(1,t3,v3,m3,mirror(m3,184),c3)),
(2,6):logo(380,209,layer(0,t4,b4),layer(1,m4,[(x+229,y) for x,y in m4],c4)),
(2,7):logo(381,291,layer(0,t5,b5,c5),layer(1,m5,mr5)),
(2,8):logo(355,299,layer(0,u6,b6),layer(1,t6,mirror(t6,177.5),m6,[(x+226,y) for x,y in m6],c6)),
(2,9):logo(355,354,layer(0,s7,mirror(s7,177.5),c7),layer(1,t7,b7,m7,mirror(m7,177.5))),
(3,1):logo(439,272,layer(1,t8,u8,b8,v8),layer(0,f8),layer(2,m8,[(x+169,y) for x,y in m8],c8)),
(3,2):logo(376,284,layer(0,t9,b9),layer(1,m9,mirror(m9,188),c9)),
(3,3):logo(408,196,layer(0,t10,b10),layer(1,f10),layer(2,m10,[(x+198,y) for x,y in m10],c10))}
VALUES=['1GKWicTGrhyBuagWmZsVslrJzUcALovKA','15EByEzW-Z2iQJPeXJWbXD-6ZR1yhQo5C','11qeDYWKaGUMhRcAk_kEPINOErfE0vyvl','1KCMtzhB_dyt0PNg2XJqy2NAuqCSRhxha','1So9ugcKjn5s5kFYF68tj2hDZOkdpTYCr','1xmlRNxXu2Xb51eJCBqZr8HmYVv3Wa2ed','1BCwVDJ9F76sAwzovgcLb0ugOMP_OtGMR','1IduNtj0j8O8gz9h1P2F2mBEtKLa-uofH','14CsUR1in57bPe6yUIKSp3VFI-WUIx_vl','1v_CpCIV2MAwFeEk7iBlrsJH53flyQTfn']
if __name__=='__main__':
    old=json.loads((R/'04-desain/variasi-svg/batch-24/progress.json').read_text())
    groups=old['groups'];groups['rasio-2']=dict(redrawn=list(range(1,10)),pending=[]);groups['rasio-3']=dict(redrawn=[1,2,3],pending=list(range(4,10)))
    names={k:f'Max_a_Gambar_kotak_rasio_1_{k[0]}_logo-{k[1]:02}.png' for k in DATA}
    seen={e['sourceSha256'] for p in (R/'04-desain/variasi-svg').glob('batch-*/progress.json') if p.parent.name!='batch-25' for e in json.loads(p.read_text())['entries']}
    for name in names.values():
        digest=hashlib.sha256((R/'google_drive'/name).read_bytes()).hexdigest()
        assert digest not in seen, f'Duplicate source requires alias audit: {name}'
        seen.add(digest)
    export_batch('25',DATA,dict(zip(DATA,VALUES)),219,groups,source_names=names,entry_ids={k:f'exp-rasio-{k[0]:03}-{k[1]:02}' for k in DATA})
    out=R/'04-desain/variasi-svg/batch-25';p=json.loads((out/'progress.json').read_text())
    p.update(uniqueDriveMasters=219,driveSourcesCoveredIncludingDuplicates=237,remainingNotProcessed=105,progressPercent=round(237/342*100,2),redrawOnlyPercent=round(219/342*100,2),progressBasis='219 manual masters + 18 verified duplicate source files / 342 reported files',sourceAliases=old['sourceAliases'],buildPolicy='Redraw only; all APK jobs paused; Android catalog unchanged.')
    for e in p['entries']:e.update(sourceFamily='rasio_1',appIntegration='deferred-no-apk-requested')
    (out/'progress.json').write_text(json.dumps(p,indent=2))
    page=(out/'perbandingan.html').read_text().replace('219 dari 342 sumber','219 master unik; 237 dari 342 sumber tercakup').replace('<strong>123</strong>','<strong>105</strong>').replace('64.04%','69.30%').replace('Kelompok 2 ·','Keluarga rasio_1 · Kelompok 2 ·').replace('Kelompok 3 ·','Keluarga rasio_1 · Kelompok 3 ·')
    page=page.replace('</main>','<h2>Audit terbatas</h2><p>219 master unik + 18 alias = 237/342 (69,30%), sisa 105. Redraw unik saja: 219/342 (64,04%). Sepuluh hash baru berbeda satu sama lain dan dari sumber master terdahulu. 342 bukan jumlah desain unik terverifikasi. Huruf putih 3/01 dan 3/03 positif; celah antarkomponen transparan. Tidak ada build APK atau perubahan katalog aplikasi.</p></main>')
    (out/'perbandingan.html').write_text(page)
