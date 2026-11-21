"""Ten hand-measured source-specific rasio masters; no tracing or Android build."""
from build_drive_batch_03 import layer,mirror,logo
from design_batch_io import export_batch
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1]
# 3/04 layered roof and rounded navy C.
t1=[(10,60),(180,9),(348,60),(348,75),(180,38),(10,75)]
u1=[(38,76),(179,46),(323,75),(323,86),(179,69),(38,87)]
b1=[(9,193),(179,221),(348,192),(348,208),(179,255),(9,209)]
m1=[(9,105),(39,101),(64,128),(88,96),(121,93),(121,193),(88,189),(88,145),(64,170),(41,146),(41,184),(9,181)]
c1=[(151,92),(207,92),(217,95),(224,102),(227,112),(227,132),(193,132),(193,122),(189,118),(171,118),(167,122),(167,165),(171,169),(189,169),(193,165),(193,154),(227,154),(227,176),(224,185),(217,192),(207,195),(151,195),(142,192),(135,185),(133,176),(133,111),(136,102),(143,95)]
# 3/05 single navy cap/base, red MCM with short-chord rounded C.
t2=[(9,112),(188,9),(365,111),(188,49)]
b2=[(9,217),(188,273),(365,217),(188,318)]
m2=[(9,122),(45,116),(64,146),(95,111),(124,108),(124,221),(89,216),(89,163),(64,190),(39,164),(39,210),(9,206)]
c2=[(162,102),(214,102),(225,105),(234,112),(239,123),(240,148),(202,148),(202,136),(198,131),(178,131),(174,135),(174,192),(178,196),(198,196),(202,192),(202,181),(240,181),(240,201),(237,211),(230,219),(220,224),(161,225),(151,222),(142,216),(137,208),(135,198),(135,129),(138,118),(144,110),(152,104)]
# 3/06 narrow tall C; open roof and base.
t3=[(9,75),(172,9),(334,75),(334,91),(172,38),(9,91)]
b3=[(12,254),(47,244),(171,285),(296,244),(331,254),(171,314)]
m3=[(9,108),(37,98),(57,148),(83,85),(111,75),(111,250),(79,240),(79,168),(57,205),(38,176),(38,235),(9,245)]
c3=[(172,54),(219,71),(219,125),(185,125),(185,99),(181,95),(164,95),(160,99),(160,222),(164,226),(181,226),(185,222),(185,197),(219,197),(219,251),(172,269),(125,251),(125,71)]
# 3/07 asymmetric sloping rails and oblique initials.
t4=[(47,86),(188,60),(203,43),(392,9),(375,36),(42,94)]
b4=[(27,224),(376,169),(373,181),(167,215),(155,229),(9,253)]
m4=[(39,109),(76,103),(94,131),(125,96),(161,90),(141,193),(104,199),(115,151),(81,184),(65,157),(55,204),(15,210)]
mr4=[(272,70),(304,65),(320,101),(351,58),(392,51),(374,157),(337,163),(347,112),(313,151),(291,124),(286,170),(254,175)]
c4=[(184,85),(248,74),(255,75),(260,81),(254,116),(223,121),(226,104),(200,108),(191,162),(218,158),(222,144),(250,139),(246,163),(242,173),(235,179),(168,190),(160,187),(155,181),(156,171),(168,106),(174,94)]
# 3/08 pointed navy Ms, red C and double chevron below with detached stubs.
m5=[(9,9),(41,38),(64,82),(114,56),(114,188),(85,174),(85,110),(57,127),(37,94),(37,174),(9,160)]
c5=[(171,23),(219,51),(219,93),(184,93),(184,67),(171,60),(157,67),(157,167),(171,173),(184,167),(184,147),(219,147),(219,188),(171,213),(123,188),(123,51)]
b5=[(54,170),(170,228),(286,170),(286,190),(170,247),(54,190)]
u5=[(47,193),(170,259),(293,193),(293,216),(170,280),(47,216)]
s5=[(9,170),(40,186),(40,204),(9,188)]
# 3/09 three separate roof panels, navy nameplate, white positive letters.
t6=[(9,103),(72,72),(72,100),(9,120)]
u6=[(89,53),(171,9),(171,67),(89,93)]
v6=[(184,10),(385,95),(385,115),(197,59),(184,63)]
f6=[(9,130),(197,69),(385,124),(385,240),(322,240),(309,249),(83,249),(70,240),(9,240)]
b6=[(9,249),(69,249),(81,259),(312,259),(325,249),(385,249),(346,277),(44,277)]
m6=[(30,141),(58,136),(81,160),(108,129),(137,126),(137,228),(105,227),(105,180),(82,204),(61,181),(61,225),(30,222)]
mr6=[(256,125),(285,126),(310,162),(335,134),(363,139),(363,222),(332,225),(332,181),(310,204),(288,180),(288,227),(256,228)]
c6=[(175,122),(219,122),(230,126),(238,134),(243,145),(243,166),(211,166),(211,155),(207,150),(189,150),(185,154),(185,200),(189,205),(207,205),(211,201),(211,189),(243,189),(243,207),(239,217),(231,225),(221,229),(174,229),(163,225),(155,218),(150,207),(150,144),(154,134),(163,126)]
# 4/01 navy ring, detached red diamond, white positive angular initials.
o7=[(215,9),(420,143),(215,281),(9,143)]
i7=[(215,33),(405,143),(215,257),(24,143)]
d7=[(215,43),(394,143),(215,245),(36,143)]
m7=[(94,115),(113,115),(133,136),(153,113),(172,112),(172,179),(151,179),(151,147),(133,165),(115,147),(115,176),(94,176)]
c7=[(193,110),(237,110),(248,119),(248,135),(226,135),(226,125),(206,125),(206,165),(226,165),(226,155),(248,155),(248,171),(237,180),(193,180),(183,171),(183,119)]
mr7=[(259,112),(279,113),(299,135),(318,115),(337,115),(337,176),(317,176),(317,147),(299,165),(281,147),(281,179),(259,179)]
# 4/02 red roof, navy base and Ms, chamfered red C.
t8=[(9,91),(177,9),(341,90),(177,50)]
b8=[(9,208),(176,250),(341,208),(176,290)]
m8=[(9,98),(37,97),(61,135),(88,95),(118,94),(118,208),(89,207),(89,154),(63,181),(40,154),(40,200),(9,200)]
c8=[(147,91),(205,91),(222,106),(222,132),(190,132),(190,120),(162,120),(162,181),(190,181),(190,166),(222,166),(222,194),(205,209),(147,209),(130,194),(130,107)]
# 4/03 clipped red slabs and navy chamfered initials.
t9=[(55,9),(304,9),(345,45),(9,45)]
b9=[(9,170),(345,170),(301,206),(55,206)]
m9=[(9,56),(36,56),(62,97),(94,56),(117,56),(117,160),(87,160),(87,115),(64,141),(39,115),(39,160),(9,160)]
c9=[(141,56),(211,56),(225,70),(225,96),(195,96),(195,85),(155,85),(155,131),(195,131),(195,119),(225,119),(225,146),(211,160),(141,160),(126,146),(126,70)]
# 4/04 two red roof chevrons, independent central navy triangle and navy MCM.
t10=[(9,140),(132,10),(181,64),(152,94),(132,73),(70,140)]
u10=[(193,64),(244,10),(362,140),(303,140),(244,73),(222,94)]
v10=[(125,140),(187,71),(249,140)]
m10=[(12,152),(41,152),(67,179),(94,152),(127,152),(127,236),(95,236),(95,194),(68,216),(43,194),(43,236),(12,236)]
c10=[(152,152),(221,152),(236,165),(236,186),(207,186),(207,174),(170,174),(170,213),(207,213),(207,202),(236,202),(236,223),(221,236),(152,236),(139,224),(139,164)]
DATA={
(3,4):logo(357,264,layer(0,t1,b1),layer(1,u1,m1,mirror(m1,179),c1)),
(3,5):logo(375,327,layer(1,t2,b2),layer(0,m2,mirror(m2,187.5),c2)),
(3,6):logo(343,323,layer(0,t3,b3),layer(1,m3,mirror(m3,171.5),c3)),
(3,7):logo(401,263,layer(0,t4,b4),layer(1,m4,mr4,c4)),
(3,8):logo(341,289,layer(0,c5,b5,s5,mirror(s5,170.5)),layer(1,m5,mirror(m5,170.5),u5)),
(3,9):logo(395,286,layer(0,t6,u6,v6,b6),layer(1,f6),layer(2,m6,mr6,c6)),
(4,1):logo(429,290,layer(1,o7,i7),layer(0,d7),layer(2,m7,mr7,c7)),
(4,2):logo(350,299,layer(0,t8,c8),layer(1,b8,m8,mirror(m8,175))),
(4,3):logo(354,215,layer(0,t9,b9),layer(1,m9,[(x+227,y) for x,y in m9],c9)),
(4,4):logo(373,246,layer(0,t10,u10),layer(1,v10,m10,[(x+236,y) for x,y in m10],c10))}
VALUES=['1kYU5uNIhaEXPXhytZ1TVUZZfSKhIaikK','1jynJzxsmgYcSf1WftIr5QKEV0h-ZIIen','1ErzoVR0kIsYQDUv41l97w3eqjc6gvErY','1JGcrdB37mZ8DSIedIOvWqEzvkbBca2Qg','1pwl87kIXzbOU938-idB6d7bYOoAOURBF','1brjyC4padurgCJPgz-cycwwDbB1DdBI-','1Auofz_4Tx8PkAMfYHsRL3zEm5y7yLpPG','1HAZygFMa5UQ6kZpj-Ua9sIAgVFuqYkAZ','1ez74IsR0XpQbuMuL1Cq0BxfZJ4xXq6wX','1E4DjpQV3hT1iQfLYSL1b_xdGUAZFBPxN']
if __name__=='__main__':
    old=json.loads((R/'04-desain/variasi-svg/batch-25/progress.json').read_text())
    groups=old['groups'];groups['rasio-3']=dict(redrawn=list(range(1,10)),pending=[]);groups['rasio-4']=dict(redrawn=[1,2,3,4],pending=list(range(5,10)))
    names={k:f'Max_a_Gambar_kotak_rasio_1_{k[0]}_logo-{k[1]:02}.png' for k in DATA}
    seen={e['sourceSha256'] for p in (R/'04-desain/variasi-svg').glob('batch-*/progress.json') if p.parent.name!='batch-26' for e in json.loads(p.read_text())['entries']}
    for name in names.values():
        digest=hashlib.sha256((R/'google_drive'/name).read_bytes()).hexdigest()
        assert digest not in seen, f'Duplicate source requires alias audit: {name}'
        seen.add(digest)
    export_batch('26',DATA,dict(zip(DATA,VALUES)),229,groups,source_names=names,entry_ids={k:f'exp-rasio-{k[0]:03}-{k[1]:02}' for k in DATA})
    out=R/'04-desain/variasi-svg/batch-26';p=json.loads((out/'progress.json').read_text())
    p.update(uniqueDriveMasters=229,driveSourcesCoveredIncludingDuplicates=247,remainingNotProcessed=95,progressPercent=round(247/342*100,2),redrawOnlyPercent=round(229/342*100,2),progressBasis='229 manual masters + 18 verified duplicate source files / 342 reported files',sourceAliases=old['sourceAliases'],buildPolicy='Redraw only; all APK jobs paused; Android catalog unchanged.')
    for e in p['entries']:e.update(sourceFamily='rasio_1',appIntegration='deferred-no-apk-requested')
    (out/'progress.json').write_text(json.dumps(p,indent=2))
    page=(out/'perbandingan.html').read_text().replace('229 dari 342 sumber','229 master unik; 247 dari 342 sumber tercakup').replace('<strong>113</strong>','<strong>95</strong>').replace('66.96%','72.22%').replace('Kelompok 4 ·','Keluarga rasio_1 · Kelompok 4 ·').replace('Kelompok 3 ·','Keluarga rasio_1 · Kelompok 3 ·')
    page=page.replace('</main>','<h2>Audit terbatas</h2><p>229 master unik + 18 alias = 247/342 (72,22%), sisa 95. Redraw unik saja: 229/342 (66,96%). Sepuluh hash baru berbeda satu sama lain dan dari sumber master terdahulu. 342 bukan jumlah desain unik terverifikasi. Huruf putih 3/09 dan 4/01 positif; ring 4/01 memiliki counter transparan; celah antarkomponen transparan. Tidak ada build APK atau perubahan katalog aplikasi.</p></main>')
    (out/'perbandingan.html').write_text(page)
