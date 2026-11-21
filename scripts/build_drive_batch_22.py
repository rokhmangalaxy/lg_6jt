"""Ten source-specific rasio masters from manual polygon measurements. No APK."""
from build_drive_batch_03 import layer,mirror,logo
from design_batch_io import export_batch
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1]
# 16/09: red stepped I-beam rails and navy rounded C.
t1=[(9,9),(359,9),(359,28),(339,28),(313,51),(313,62),(272,62),(272,39),(94,39),(94,62),(53,62),(53,51),(29,28),(9,28)]
b1=[(9,217),(29,217),(53,195),(53,184),(94,184),(94,206),(272,206),(272,184),(313,184),(313,195),(339,217),(359,217),(359,235),(9,235)]
m1=[(28,74),(57,74),(79,107),(101,74),(134,74),(134,173),(101,173),(101,129),(79,155),(59,129),(59,173),(28,173)]
c1=[(155,73),(220,73),(227,78),(231,85),(231,113),(196,113),(196,100),(176,100),(176,149),(196,149),(196,136),(231,136),(231,161),(227,169),(220,173),(155,173),(147,170),(143,163),(143,85),(147,78)]
# 17/01: outlined gap between red diamond and four navy tips; white block letters.
f2=[(213,37),(404,144),(208,262),(9,144)]
t2=[(9,143),(195,9),(211,29)]
b2=[(9,146),(188,287),(206,268)]
tr2=[(215,29),(233,9),(404,143)]
br2=[(211,268),(404,146),(227,287)]
m2=[(88,113),(110,113),(127,135),(146,113),(168,113),(168,185),(144,185),(144,149),(127,168),(110,149),(110,185),(88,185)]
c2=[(188,113),(232,112),(244,122),(244,138),(221,138),(221,128),(200,128),(200,167),(221,167),(221,157),(244,157),(244,175),(232,185),(188,185),(177,175),(177,122)]
# 17/02: notched red roof, navy flanking M posts, lower red C.
t3=[(9,72),(146,9),(183,32),(220,9),(357,72),(318,87),(221,45),(183,72),(145,45),(48,87)]
m3=[(9,83),(39,95),(64,119),(106,75),(138,61),(136,98),(115,115),(115,215),(88,215),(88,141),(64,166),(40,143),(40,215),(9,215)]
c3=[(151,99),(215,98),(241,119),(241,148),(205,148),(205,131),(161,131),(161,194),(205,194),(205,177),(241,177),(241,208),(215,228),(151,228),(126,208),(126,119)]
# 17/03: red cap/base with detached navy side brackets, navy MCM.
t4=[(54,70),(181,9),(307,70),(307,95),(181,45),(54,95)]
b4=[(54,203),(181,254),(307,203),(307,228),(181,288),(54,228)]
s4=[(9,93),(44,77),(44,101),(29,108),(29,190),(44,197),(44,222),(9,206)]
m4=[(41,115),(63,108),(78,133),(100,98),(130,94),(130,206),(99,204),(99,150),(78,176),(61,154),(61,192),(41,185)]
c4=[(153,94),(208,94),(221,108),(221,132),(194,133),(194,121),(168,121),(168,182),(194,182),(194,171),(221,170),(221,193),(208,206),(153,206),(141,194),(141,108)]
# 17/04: independently measured oblique type and sharply tapered offset rails.
t5=[(71,21),(151,18),(134,34),(55,36)]
u5=[(175,5),(390,5),(380,13),(144,34)]
b5=[(18,156),(252,137),(223,164),(9,164)]
v5=[(262,137),(338,137),(322,152),(245,152)]
m5=[(51,47),(88,47),(95,76),(130,46),(163,46),(132,128),(99,128),(113,94),(78,122),(69,92),(53,129),(17,129)]
c5=[(185,45),(255,45),(243,77),(210,77),(215,64),(200,64),(184,110),(198,110),(202,101),(233,101),(225,121),(214,128),(153,128),(147,125),(145,120),(147,112),(168,57),(174,49)]
mr5=[(267,46),(299,46),(306,76),(340,46),(375,46),(342,128),(310,128),(324,94),(288,122),(280,92),(263,128),(231,128)]
# 17/05: tall red pointed C with short upper/lower right arms; navy side Ms.
m6=[(9,47),(54,78),(109,40),(109,275),(77,257),(77,113),(55,128),(42,117),(42,245),(9,224)]
c6=[(164,9),(210,36),(210,107),(179,107),(179,63),(165,54),(150,63),(150,248),(164,257),(179,248),(179,200),(210,200),(210,280),(164,308),(118,280),(118,36)]
# 17/06: plain red chamfer rails; navy chamfered C with slightly oblique side.
t7=[(40,9),(335,9),(366,39),(9,39)]
b7=[(9,173),(366,173),(336,202),(39,202)]
m7=[(12,54),(47,54),(70,84),(96,53),(129,53),(129,159),(94,159),(94,104),(70,134),(44,105),(44,159),(12,159)]
c7=[(155,53),(220,52),(237,66),(237,91),(203,91),(203,77),(172,77),(172,134),(203,134),(203,120),(237,119),(237,144),(220,159),(155,159),(138,145),(138,68)]
# 17/07: navy roof and Ms; tall red C, open right arm separation.
t8=[(15,79),(162,9),(309,79),(286,92),(162,35),(39,92)]
m8=[(9,89),(34,103),(53,124),(80,89),(107,76),(107,277),(78,264),(78,150),(54,175),(32,153),(32,252),(9,240)]
c8=[(162,43),(210,66),(210,117),(178,135),(178,91),(162,83),(147,91),(147,254),(162,263),(178,254),(178,210),(210,192),(210,282),(162,305),(114,282),(114,66)]
# 17/08: red rectangular frame with inward side notches; transparent window.
o9=[(9,9),(381,9),(381,62),(368,75),(368,107),(381,120),(381,170),(9,170),(9,120),(23,107),(23,75),(9,62)]
i9=[(26,26),(365,26),(365,58),(355,68),(355,114),(365,124),(365,154),(26,154),(26,124),(35,114),(35,68),(26,58)]
m9=[(46,42),(74,42),(92,69),(114,40),(142,40),(142,139),(114,139),(114,88),(92,112),(73,89),(73,139),(46,139)]
c9=[(166,40),(223,40),(239,53),(239,76),(210,77),(210,65),(180,65),(180,116),(210,116),(210,105),(239,104),(239,127),(223,141),(166,141),(150,128),(150,54)]
# 17/09: red pointed C; navy Ms with oblique outer caps and feet; double V below.
m10=[(9,10),(66,46),(95,19),(125,19),(125,146),(104,137),(104,70),(68,94),(41,78),(41,109),(9,95)]
c10=[(154,18),(222,18),(239,31),(239,62),(203,62),(203,46),(170,46),(170,110),(203,110),(203,94),(239,94),(239,132),(187,159),(135,132),(135,33)]
b10=[(9,106),(187,183),(366,106),(351,137),(187,204),(24,137)]
f10=[(30,150),(187,213),(344,150),(338,167),(187,239),(37,167)]
DATA={
(16,9):logo(368,244,layer(0,t1,b1),layer(1,m1,[(x+212,y) for x,y in m1],c1)),
(17,1):logo(413,296,layer(1,t2,tr2,b2,br2),layer(0,f2),layer(2,m2,[(x+166,y) for x,y in m2],c2)),
(17,2):logo(366,236,layer(0,t3,c3),layer(1,m3,mirror(m3,183))),
(17,3):logo(362,297,layer(0,t4,b4),layer(1,s4,mirror(s4,181),m4,mirror(m4,181),c4)),
(17,4):logo(394,172,layer(0,u5,b5,c5),layer(1,t5,v5,m5,mr5)),
(17,5):logo(328,317,layer(0,c6),layer(1,m6,mirror(m6,164))),
(17,6):logo(375,211,layer(0,t7,b7),layer(1,m7,[(x+234,y) for x,y in m7],c7)),
(17,7):logo(325,313,layer(0,c8),layer(1,t8,m8,mirror(m8,162.5))),
(17,8):logo(390,179,layer(0,o9,i9),layer(1,m9,[(x+201,y) for x,y in m9],c9)),
(17,9):logo(375,248,layer(0,c10,b10),layer(1,m10,mirror(m10,187.5),f10))}
VALUES=['16GCfk7oF-b04hgiiWCiVCN1SKhaHcKo0','12JOCvGTmojJ1jdsS2SKj4CiOj_0r7X7u','1uFWJT0nEAkA4gXHlvgw7b3inGUFeoQrG','1rSBxnAOyfSyqB_rNvB_FakYnjGdloavS','17YGrpLz42aiIgpIw8FzaIKbcyiIm_vVa','1T9kFXA2EIxSJ6n4jbgwZ5dawzEKTsnNb','190ZRvBDOkQId-NehOva1zJ4C4WoQ1Vs5','1zlTQtqdMOi3KhWewhd1PCVIJFAhF0i2T','1GPqiEThw53yRLLDp8iYWry-xvAe-cd6U','1PPYuY_I3rlmciO9M4z94_KwQaLpwhRpZ']
if __name__=='__main__':
    old=json.loads((R/'04-desain/variasi-svg/batch-21/progress.json').read_text())
    groups=old['groups'];groups['rasio-16']=dict(redrawn=list(range(1,10)),pending=[]);groups['rasio-17']=dict(redrawn=list(range(1,10)),pending=[])
    names={k:f'Max_a_Gambar_kotak_rasio_1_{k[0]}_logo-{k[1]:02}.png' for k in DATA}
    seen={e['sourceSha256'] for p in (R/'04-desain/variasi-svg').glob('batch-*/progress.json') if p.parent.name!='batch-22' for e in json.loads(p.read_text())['entries']}
    for name in names.values():
        digest=hashlib.sha256((R/'google_drive'/name).read_bytes()).hexdigest()
        assert digest not in seen, f'Duplicate source requires alias audit: {name}'
        seen.add(digest)
    export_batch('22',DATA,dict(zip(DATA,VALUES)),189,groups,source_names=names,entry_ids={k:f'exp-rasio-{k[0]:03}-{k[1]:02}' for k in DATA})
    out=R/'04-desain/variasi-svg/batch-22';p=json.loads((out/'progress.json').read_text())
    p.update(uniqueDriveMasters=189,driveSourcesCoveredIncludingDuplicates=207,remainingNotProcessed=135,progressPercent=round(207/342*100,2),redrawOnlyPercent=round(189/342*100,2),progressBasis='189 manual masters + 18 verified duplicate source files / 342 reported files',sourceAliases=old['sourceAliases'],buildPolicy='Redraw only; all APK jobs paused; Android catalog unchanged.')
    for e in p['entries']:e.update(sourceFamily='rasio_1',appIntegration='deferred-no-apk-requested')
    (out/'progress.json').write_text(json.dumps(p,indent=2))
    page=(out/'perbandingan.html').read_text().replace('189 dari 342 sumber','189 master unik; 207 dari 342 sumber tercakup').replace('<strong>153</strong>','<strong>135</strong>').replace('55.26%','60.53%').replace('Kelompok 16 ·','Keluarga rasio_1 · Kelompok 16 ·').replace('Kelompok 17 ·','Keluarga rasio_1 · Kelompok 17 ·')
    page=page.replace('</main>','<h2>Audit terbatas</h2><p>189 master unik + 18 alias = 207/342 (60,53%), sisa 135. Redraw unik saja: 189/342 (55,26%). Sepuluh hash baru berbeda satu sama lain dan dari sumber master terdahulu. 342 bukan jumlah desain unik terverifikasi. Huruf putih 17/01 positif; celah antarsegmen transparan. Tidak ada build APK atau perubahan katalog aplikasi.</p></main>')
    (out/'perbandingan.html').write_text(page)
