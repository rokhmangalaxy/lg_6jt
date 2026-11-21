"""Ten manually measured rasio polygon designs; no tracing or APK."""
from build_drive_batch_03 import layer,mirror,logo
from design_batch_io import export_batch
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1]
# 5/06 hooked navy M feet and elongated angular red C.
m1=[(9,12),(58,58),(108,9),(118,9),(118,166),(143,191),(122,191),(83,154),(83,82),(60,104),(40,85),(40,178),(9,149)]
c1=[(146,9),(223,9),(242,28),(242,70),(207,92),(207,47),(165,47),(165,144),(207,144),(207,137),(242,114),(242,157),(207,191),(165,191),(127,154),(127,28)]
# 5/07 navy hexagonal counter-frame, red inset, white positive lettering.
o2=[(201,9),(392,74),(392,173),(201,239),(9,173),(9,74)]
i2=[(201,23),(380,83),(380,164),(201,223),(21,164),(21,83)]
d2=[(201,29),(374,88),(374,159),(201,217),(27,159),(27,88)]
m2=[(53,88),(78,86),(100,109),(123,86),(148,86),(148,167),(123,167),(123,124),(100,147),(79,126),(79,162),(53,157)]
c2=[(175,85),(233,85),(239,88),(243,93),(244,101),(244,116),(217,116),(217,106),(188,106),(188,146),(217,146),(217,135),(244,135),(244,152),(241,160),(236,166),(230,167),(175,167),(169,165),(164,160),(162,153),(162,101),(164,94),(169,88)]
# 5/08 tall red pointed C, independently measured winged Ms.
m3=[(9,82),(53,114),(96,61),(117,46),(117,245),(85,225),(85,127),(55,156),(38,145),(38,221),(9,203)]
mr3=[(232,46),(255,61),(295,114),(339,80),(339,203),(310,221),(310,145),(294,156),(264,127),(264,225),(232,245)]
c3=[(175,9),(222,39),(222,100),(192,122),(192,61),(175,50),(158,61),(158,231),(175,242),(192,231),(192,191),(222,169),(222,254),(174,282),(126,254),(126,39)]
# 5/09 six detached navy wing rails and red open cap/base.
t4=[(82,70),(200,9),(316,70),(259,70),(200,37),(141,70)]
b4=[(76,185),(141,185),(199,222),(259,185),(322,185),(199,251)]
s4=[(9,83),(74,83),(74,103),(20,103)]
s4b=[(16,116),(74,116),(74,138),(27,138)]
s4c=[(23,151),(74,151),(74,172),(34,172)]
m4=[(87,84),(103,84),(122,119),(143,84),(159,84),(159,172),(140,172),(140,130),(122,153),(106,131),(106,172),(87,172)]
c4=[(175,84),(223,84),(228,87),(231,92),(231,117),(210,117),(210,103),(188,103),(188,155),(210,155),(210,141),(231,141),(231,163),(228,169),(223,173),(175,173),(170,170),(167,165),(167,92),(170,87)]
# 6/01 diamond with four separate navy tips, white positive angular MCM.
d5=[(220,38),(422,138),(218,245),(9,138)]
t5=[(19,125),(202,9),(218,28)]
u5=[(223,28),(240,9),(412,125)]
b5=[(20,151),(192,272),(216,252)]
v5=[(222,252),(412,151),(241,272)]
m5=[(93,109),(115,109),(135,136),(155,109),(178,109),(178,178),(155,178),(155,145),(135,170),(115,147),(115,178),(93,178)]
c5=[(199,109),(241,109),(252,119),(252,135),(231,135),(231,125),(209,125),(209,162),(231,162),(231,152),(252,152),(252,169),(241,178),(199,178),(188,169),(188,119)]
# 6/02 open red cap/base and navy compact initials.
t6=[(40,76),(177,9),(313,76),(313,99),(177,44),(40,99)]
b6=[(44,216),(176,262),(308,216),(308,239),(176,294),(44,239)]
m6=[(9,110),(35,110),(62,136),(91,110),(115,110),(115,210),(86,210),(86,160),(63,184),(39,162),(39,210),(9,210)]
c6=[(145,110),(209,110),(225,125),(225,149),(197,149),(197,132),(156,132),(156,188),(197,188),(197,175),(225,175),(225,194),(209,210),(145,210),(128,194),(128,125)]
# 6/03 split red stepped cap with two navy inner facets and lower navy arrow.
t7=[(9,85),(28,62),(94,62),(192,9),(192,38),(98,85)]
u7=[(199,9),(297,62),(362,62),(381,85),(292,85),(199,38)]
a7=[(130,85),(191,55),(191,71),(160,85)]
a7r=[(199,55),(259,85),(230,85),(199,71)]
b7=[(9,194),(98,194),(126,210),(26,210)]
b7r=[(292,194),(380,194),(363,210),(265,210)]
v7=[(123,194),(151,194),(195,219),(238,194),(266,194),(195,238)]
m7=[(23,96),(54,96),(83,127),(113,96),(142,96),(142,185),(113,185),(113,137),(83,167),(54,137),(54,185),(23,185)]
c7=[(168,96),(223,96),(239,111),(239,132),(212,132),(212,117),(181,117),(181,164),(212,164),(212,151),(239,151),(239,171),(223,185),(168,185),(153,171),(153,111)]
# 6/04 red ring with transparent window and two red internal triangles.
o8=[(201,9),(388,79),(388,205),(200,283),(9,205),(9,83)]
i8=[(201,48),(380,97),(380,196),(201,243),(17,196),(17,97)]
a8=[(133,81),(201,58),(269,81)]
b8=[(133,212),(269,212),(201,234)]
m8=[(31,104),(58,100),(88,132),(119,94),(145,91),(145,202),(115,198),(115,148),(88,173),(62,149),(62,192),(31,187)]
c8=[(172,90),(230,90),(244,106),(244,127),(215,127),(215,112),(187,112),(187,180),(215,180),(215,163),(244,163),(244,187),(230,202),(172,202),(158,187),(158,106)]
# 6/05 red rails and C, navy oblique Ms.
t9=[(139,9),(387,9),(375,28),(120,28)]
b9=[(24,151),(278,151),(260,170),(9,170)]
m9=[(61,42),(82,42),(98,74),(137,42),(170,42),(130,141),(98,141),(119,92),(87,119),(72,88),(51,141),(16,141)]
mr9=[(272,43),(300,43),(314,74),(352,43),(385,43),(345,141),(313,141),(335,92),(302,119),(286,88),(265,141),(232,141)]
c9=[(191,42),(260,42),(249,72),(200,72),(184,112),(234,112),(223,141),(151,141),(144,132),(173,58)]
# 6/06 six detached frame facets, navy tapered Ms and chamfered C.
t10=[(114,63),(206,10),(293,62),(293,83),(206,38),(114,87)]
b10=[(119,226),(207,270),(296,226),(296,246),(207,298),(119,247)]
s10=[(9,126),(110,66),(110,89),(33,126)]
v10=[(9,185),(35,185),(113,224),(113,244)]
m10=[(55,130),(80,120),(102,144),(129,113),(154,107),(154,209),(125,199),(125,160),(103,183),(81,162),(81,192),(55,184)]
c10=[(179,101),(232,101),(248,117),(248,146),(220,146),(220,128),(193,128),(193,185),(220,185),(220,168),(248,168),(248,196),(232,211),(179,211),(164,196),(164,117)]
DATA={
(5,6):logo(376,201,layer(0,c1),layer(1,m1,mirror(m1,188))),
(5,7):logo(401,248,layer(1,o2,i2),layer(0,d2),layer(2,m2,mirror(m2,202),c2)),
(5,8):logo(348,291,layer(0,c3),layer(1,m3,mr3)),
(5,9):logo(398,260,layer(0,t4,b4),layer(1,s4,s4b,s4c,mirror(s4,199.5),mirror(s4b,199.5),mirror(s4c,199.5),m4,[(x+151,y) for x,y in m4],c4)),
(6,1):logo(431,281,layer(1,t5,u5,b5,v5),layer(0,d5),layer(2,m5,[(x+169,y) for x,y in m5],c5)),
(6,2):logo(352,303,layer(0,t6,b6),layer(1,m6,[(x+228,y) for x,y in m6],c6)),
(6,3):logo(390,247,layer(0,t7,u7,b7),layer(1,a7,a7r,b7r,v7,m7,[(x+227,y) for x,y in m7],c7)),
(6,4):logo(397,292,layer(0,o8,i8,a8,b8),layer(1,m8,mirror(m8,199.5),c8)),
(6,5):logo(396,179,layer(0,t9,b9,c9),layer(1,m9,mr9)),
(6,6):logo(411,307,layer(0,t10,b10),layer(1,s10,mirror(s10,205.5),v10,mirror(v10,205.5),m10,mirror(m10,205.5),c10))}
VALUES=['13EiTGJO9jsfw-H4UdIokH_gQjf4K1Nwc','1Z-Xhye7nZKY_R4wmj9PDUa8FESgz1BS2','1t23u7bjyWBV4FJzUOBmiavimdSrkp8Oc','1nGt-l1OUTFjIagaGFBtd41_WtF9CuDdM','14aX5uinc_xH7Z910tsXCddsn2FoXEL68','141rRzJ-6yZyIzCBvWt0pZvoC7IvRJ0DO','1yrTicVw7-kIPXHshVPg4XvHkUIROcfyE','1XjJhvF3Lci7yw86cT6uiPJt6Tl6Pdu8n','1TG-WunFAxhV7xFpmavHwrDwoNdzdd5Ns','1Yr0Hg4HdiYTD4Mm1KMoJdl8R1MVCC_88']
if __name__=='__main__':
    old=json.loads((R/'04-desain/variasi-svg/batch-27/progress.json').read_text())
    groups=old['groups'];groups['rasio-5']=dict(redrawn=list(range(1,10)),pending=[]);groups['rasio-6']=dict(redrawn=[1,2,3,4,5,6],pending=list(range(7,10)))
    names={k:f'Max_a_Gambar_kotak_rasio_1_{k[0]}_logo-{k[1]:02}.png' for k in DATA}
    seen={e['sourceSha256'] for p in (R/'04-desain/variasi-svg').glob('batch-*/progress.json') if p.parent.name!='batch-28' for e in json.loads(p.read_text())['entries']}
    for name in names.values():
        digest=hashlib.sha256((R/'google_drive'/name).read_bytes()).hexdigest()
        assert digest not in seen, f'Duplicate source requires alias audit: {name}'
        seen.add(digest)
    export_batch('28',DATA,dict(zip(DATA,VALUES)),249,groups,source_names=names,entry_ids={k:f'exp-rasio-{k[0]:03}-{k[1]:02}' for k in DATA})
    out=R/'04-desain/variasi-svg/batch-28';p=json.loads((out/'progress.json').read_text())
    p.update(uniqueDriveMasters=249,driveSourcesCoveredIncludingDuplicates=267,remainingNotProcessed=75,progressPercent=round(267/342*100,2),redrawOnlyPercent=round(249/342*100,2),progressBasis='249 manual masters + 18 verified duplicate source files / 342 reported files',sourceAliases=old['sourceAliases'],buildPolicy='Redraw only; all APK jobs paused; Android catalog unchanged.')
    for e in p['entries']:e.update(sourceFamily='rasio_1',appIntegration='deferred-no-apk-requested')
    (out/'progress.json').write_text(json.dumps(p,indent=2))
    page=(out/'perbandingan.html').read_text().replace('249 dari 342 sumber','249 master unik; 267 dari 342 sumber tercakup').replace('<strong>93</strong>','<strong>75</strong>').replace('72.81%','78.07%').replace('Kelompok 6 ·','Keluarga rasio_1 · Kelompok 6 ·').replace('Kelompok 5 ·','Keluarga rasio_1 · Kelompok 5 ·')
    page=page.replace('</main>','<h2>Audit terbatas</h2><p>249 master unik + 18 alias = 267/342 (78,07%), sisa 75. Redraw unik saja: 249/342 (72,81%). Sepuluh hash baru berbeda satu sama lain dan dari sumber master terdahulu. 342 bukan jumlah desain unik terverifikasi. MCM putih 5/07 dan 6/01 positif; ring 5/07 dan 6/04 transparan; celah antarkomponen transparan. Tidak ada build APK atau perubahan katalog aplikasi.</p></main>')
    (out/'perbandingan.html').write_text(page)
