"""Ten manually measured source-specific rasio polygon masters. No tracing/APK."""
from build_drive_batch_03 import layer,mirror,logo
from design_batch_io import export_batch
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1]
# 7/08 six separate roof piers and compact navy initials above red baseline.
s1=[(9,170),(66,128),(66,190),(9,190)]
p1=[(75,91),(127,57),(127,159),(75,188)]
a1=[(141,35),(184,10),(184,130),(141,153)]
b1=[(9,300),(363,300),(363,316),(9,316)]
m1=[(9,202),(43,202),(66,228),(90,202),(126,202),(126,289),(91,289),(91,248),(66,271),(41,248),(41,289),(9,289)]
c1=[(152,202),(222,202),(235,214),(235,236),(201,236),(201,223),(172,223),(172,267),(201,267),(201,257),(235,257),(235,278),(222,289),(152,289),(138,277),(138,214)]
# 7/09 navy cap, two red lower facets and navy initials.
t2=[(14,93),(167,9),(322,93),(322,118),(167,55),(14,118)]
b2=[(10,207),(163,276),(163,331),(10,246)]
m2=[(10,130),(40,124),(63,151),(87,124),(117,124),(117,215),(87,215),(87,170),(64,195),(40,171),(40,207),(10,194)]
c2=[(138,124),(197,124),(208,135),(208,159),(180,159),(180,146),(156,146),(154,149),(154,188),(156,191),(180,191),(180,180),(208,180),(208,202),(197,214),(138,214),(126,202),(126,135)]
# 8/01 broad red diamond, four navy tips and white positive MCM.
d3=[(213,32),(417,128),(212,230),(9,128)]
t3=[(24,110),(188,10),(210,26)]
u3=[(216,26),(239,10),(400,110)]
b3=[(24,149),(187,252),(210,236)]
v3=[(216,236),(400,149),(239,252)]
m3=[(87,92),(110,92),(129,119),(149,92),(171,93),(171,170),(147,170),(147,130),(129,153),(110,131),(110,169),(87,169)]
c3=[(194,91),(250,91),(250,119),(225,119),(225,108),(207,108),(207,153),(225,153),(225,142),(250,142),(250,158),(244,165),(236,170),(194,170),(186,165),(180,159),(180,103),(186,97)]
# 8/02 red main roof, two separate navy outer tips and two flat baselines.
t4=[(75,101),(188,9),(299,101),(246,101),(188,62),(129,101)]
s4=[(19,101),(138,26),(138,38),(59,101)]
b4=[(9,236),(366,236),(366,253),(9,253)]
v4=[(9,262),(366,262),(366,275),(9,275)]
m4=[(9,119),(39,119),(67,160),(92,119),(127,119),(127,226),(94,226),(94,178),(67,209),(39,178),(39,226),(9,226)]
c4=[(153,119),(220,119),(236,134),(236,160),(202,160),(202,146),(200,144),(176,144),(174,146),(174,198),(176,201),(200,201),(202,198),(202,186),(236,186),(236,210),(220,226),(153,226),(138,211),(138,135)]
# 8/03 red initials and navy open hexagonal cap/base.
t5=[(32,71),(185,10),(339,71),(339,90),(185,43),(32,90)]
b5=[(32,215),(185,259),(339,215),(339,239),(185,294),(32,239)]
m5=[(10,98),(40,98),(68,140),(100,98),(131,98),(131,207),(100,207),(100,156),(69,190),(39,158),(39,208),(10,208)]
c5=[(160,97),(208,97),(228,114),(228,136),(199,136),(199,121),(168,121),(168,181),(199,181),(199,165),(228,165),(228,188),(208,206),(160,206),(139,188),(139,115)]
# 8/04 stepped red outer oblique rails with navy MCM, diagonal C aperture.
t6=[(12,68),(96,10),(340,10),(300,39),(112,39),(70,68)]
b6=[(46,217),(91,184),(255,184),(290,161),(374,161),(296,217)]
m6=[(9,82),(39,82),(63,105),(109,63),(138,63),(138,168),(104,168),(104,110),(62,151),(39,128),(39,169),(9,169)]
mr6=[(251,63),(277,63),(311,104),(345,63),(375,63),(375,151),(341,151),(341,120),(311,144),(283,120),(283,146),(251,165)]
c6=[(168,63),(243,63),(243,75),(226,94),(181,94),(181,135),(223,135),(243,154),(243,166),(168,166),(148,147),(148,82)]
# 8/05 red roof/base and C with detached navy shoulder facets.
t7=[(71,61),(176,9),(280,59),(280,85),(176,44),(71,85)]
s7=[(9,89),(61,63),(61,87),(28,102)]
b7=[(48,201),(176,258),(303,201),(303,225),(176,291),(48,225)]
m7=[(12,108),(31,118),(61,143),(98,96),(118,89),(118,215),(92,203),(92,152),(59,189),(38,174),(38,218),(12,204)]
c7=[(150,86),(200,86),(220,104),(220,133),(189,133),(189,115),(160,115),(160,191),(189,191),(189,171),(220,171),(220,201),(200,220),(150,220),(130,201),(130,104)]
# 8/06 red I-beam flanges, two navy rails with small downward teeth.
t8=[(9,10),(375,10),(375,24),(358,28),(342,41),(43,41),(27,28),(9,24)]
b8=[(9,223),(27,220),(43,206),(342,206),(358,220),(375,223),(375,237),(9,237)]
u8=[(43,49),(342,49),(342,66),(314,66),(303,81),(294,66),(91,66),(80,81),(70,66),(43,66)]
v8=[(43,186),(342,186),(342,198),(43,198)]
m8=[(20,77),(54,77),(78,113),(103,77),(135,77),(135,178),(102,178),(102,138),(77,166),(51,138),(51,178),(20,178)]
c8=[(163,76),(220,76),(239,93),(239,114),(207,114),(207,101),(176,101),(176,155),(207,155),(207,136),(239,136),(239,156),(220,174),(163,174),(145,157),(145,93)]
# 8/07 narrow red tall C and navy jagged-shoulder Ms.
m9=[(9,120),(41,97),(58,131),(81,71),(112,50),(112,285),(80,270),(80,159),(57,198),(42,177),(42,260),(9,243)]
c9=[(175,9),(223,41),(223,108),(190,123),(190,70),(175,56),(155,70),(155,220),(175,235),(190,220),(190,176),(223,159),(223,248),(175,281),(122,248),(122,42)]
# 8/08 red initials and four red rails, detached navy vertical diamond tips.
t10=[(83,72),(189,9),(293,72),(243,72),(189,43),(138,72)]
b10=[(91,240),(138,240),(189,271),(240,240),(288,240),(189,302)]
s10=[(9,80),(132,80),(124,90),(9,90)]
v10=[(9,221),(124,221),(132,231),(9,231)]
m10=[(9,103),(36,103),(68,148),(103,103),(128,103),(128,211),(97,211),(97,162),(68,196),(39,162),(39,211),(9,211)]
c10=[(157,103),(221,103),(238,118),(238,142),(207,142),(207,128),(169,128),(169,187),(207,187),(207,174),(238,174),(238,198),(221,213),(157,213),(139,198),(139,119)]
DATA={
(7,8):logo(372,325,layer(0,s1,mirror(s1,186),p1,mirror(p1,187),b1),layer(1,a1,mirror(a1,186),m1,[(x+237,y) for x,y in m1],c1)),
(7,9):logo(333,340,layer(0,b2,mirror(b2,166.5)),layer(1,t2,m2,mirror(m2,166.5),c2)),
(8,1):logo(426,261,layer(1,t3,u3,b3,v3),layer(0,d3),layer(2,m3,[(x+172,y) for x,y in m3],c3)),
(8,2):logo(375,284,layer(0,t4,b4),layer(1,s4,mirror(s4,187.5),v4,m4,[(x+237,y) for x,y in m4],c4)),
(8,3):logo(370,303,layer(1,t5,b5),layer(0,m5,[(x+226,y) for x,y in m5],c5)),
(8,4):logo(384,227,layer(0,t6,b6),layer(1,m6,mr6,c6)),
(8,5):logo(351,300,layer(0,t7,b7,c7),layer(1,s7,mirror(s7,175.5),m7,mirror(m7,176))),
(8,6):logo(384,246,layer(0,t8,b8),layer(1,u8,v8,m8,[(x+230,y) for x,y in m8],c8)),
(8,7):logo(345,295,layer(0,c9),layer(1,m9,mirror(m9,172.5))),
(8,8):logo(377,311,layer(1,t10,b10),layer(0,s10,mirror(s10,188.5),v10,mirror(v10,188.5),m10,[(x+239,y) for x,y in m10],c10))}
VALUES=['1XB-UCaBSorlRHf9PITw8GP3fXvXQkYGK','1nJcE6UvGAAPJcAzQ8D41jfECV3inwvto','1S5nXsVsN8nibZSHBpHyPeFJgE6M7cAtY','1t2xLw22OBw1GBxZYxOPX2jE-BdVG3zKP','1X-hWfU-YA3VAoKMZ0QrRV_GNA6eOrbji','1BDpyGESNKbr_GnTNqOCGiH24vW6lHdsG','1eI1hsQCZTsuvw0-6Nq7Axa4Te-8Rc4nl','1_e_qbrL2wrTsv36vZ80cjhFSdz18R5k6','1WyAVOnbivmueILet05iYDb84eCfKUj94','13mnTPXRPURL6Z3iX6NuIEyx9GrVaGEzE']
if __name__=='__main__':
    old=json.loads((R/'04-desain/variasi-svg/batch-29/progress.json').read_text())
    groups=old['groups'];groups['rasio-7']=dict(redrawn=list(range(1,10)),pending=[]);groups['rasio-8']=dict(redrawn=list(range(1,9)),pending=[9])
    names={k:f'Max_a_Gambar_kotak_rasio_1_{k[0]}_logo-{k[1]:02}.png' for k in DATA}
    seen={e['sourceSha256'] for p in (R/'04-desain/variasi-svg').glob('batch-*/progress.json') if p.parent.name!='batch-30' for e in json.loads(p.read_text())['entries']}
    for name in names.values():
        digest=hashlib.sha256((R/'google_drive'/name).read_bytes()).hexdigest()
        assert digest not in seen, f'Duplicate source requires alias audit: {name}'
        seen.add(digest)
    export_batch('30',DATA,dict(zip(DATA,VALUES)),269,groups,source_names=names,entry_ids={k:f'exp-rasio-{k[0]:03}-{k[1]:02}' for k in DATA})
    out=R/'04-desain/variasi-svg/batch-30';p=json.loads((out/'progress.json').read_text())
    p.update(uniqueDriveMasters=269,driveSourcesCoveredIncludingDuplicates=287,remainingNotProcessed=55,progressPercent=round(287/342*100,2),redrawOnlyPercent=round(269/342*100,2),progressBasis='269 manual masters + 18 verified duplicate source files / 342 reported files',sourceAliases=old['sourceAliases'],buildPolicy='Redraw only; all APK jobs paused; Android catalog unchanged.')
    for e in p['entries']:e.update(sourceFamily='rasio_1',appIntegration='deferred-no-apk-requested')
    (out/'progress.json').write_text(json.dumps(p,indent=2))
    page=(out/'perbandingan.html').read_text().replace('269 dari 342 sumber','269 master unik; 287 dari 342 sumber tercakup').replace('<strong>73</strong>','<strong>55</strong>').replace('78.65%','83.92%').replace('Kelompok 8 ·','Keluarga rasio_1 · Kelompok 8 ·').replace('Kelompok 7 ·','Keluarga rasio_1 · Kelompok 7 ·')
    page=page.replace('</main>','<h2>Audit terbatas</h2><p>269 master unik + 18 alias = 287/342 (83,92%), sisa 55. Redraw unik saja: 269/342 (78,65%). Sepuluh hash baru berbeda satu sama lain dan dari sumber master terdahulu. 342 bukan jumlah desain unik terverifikasi. MCM putih 8/01 positif; enam panel atap 7/08 dan empat bidang rail 8/06 terpisah; celah antarkomponen transparan. Tidak ada build APK atau perubahan katalog aplikasi.</p></main>')
    (out/'perbandingan.html').write_text(page)
