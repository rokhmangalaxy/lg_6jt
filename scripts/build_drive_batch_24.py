"""Ten source-specific hand-measured rasio polygon masters; no APK."""
from build_drive_batch_03 import layer,mirror,logo
from design_batch_io import export_batch
from pathlib import Path
import json,hashlib,math
R=Path(__file__).resolve().parents[1]
def circle(x,y,r):return [(round(x+r*math.cos(i*math.pi/8),3),round(y+r*math.sin(i*math.pi/8),3)) for i in range(16)]
# 1/02 four open roof/base chevrons, red outside and navy inside.
t1=[(15,84),(180,9),(343,84),(310,84),(180,35),(50,84)]
u1=[(70,85),(180,43),(290,85),(233,85),(180,66),(128,85)]
b1=[(15,215),(50,215),(180,266),(310,215),(343,215),(180,291)]
v1=[(70,215),(128,215),(180,234),(233,215),(290,215),(180,258)]
m1=[(9,104),(40,104),(66,133),(93,104),(122,104),(122,198),(89,198),(89,152),(65,179),(42,153),(42,198),(9,198)]
c1=[(157,104),(201,104),(213,107),(222,115),(227,126),(227,142),(193,142),(193,132),(189,128),(165,128),(162,132),(162,172),(166,176),(189,176),(193,172),(193,162),(227,162),(227,178),(222,189),(212,196),(200,198),(157,198),(145,194),(135,185),(131,174),(131,129),(135,116),(145,108)]
# 1/03 red roof and pointed red C, navy Ms with angled side feet.
t2=[(9,92),(190,9),(370,90),(370,113),(190,46),(9,113)]
m2=[(9,127),(30,119),(59,144),(105,95),(134,85),(134,223),(96,223),(96,164),(65,189),(43,174),(43,223),(9,235)]
c2=[(190,66),(238,84),(238,127),(201,127),(201,111),(178,111),(178,187),(201,187),(201,171),(238,171),(238,200),(190,228),(142,200),(142,84)]
# 1/04 navy slanted rounded C, red tapered strips.
t3=[(162,10),(374,9),(318,50),(75,50)]
b3=[(64,168),(318,168),(233,208),(9,209)]
m3=[(44,62),(77,62),(86,101),(122,62),(158,62),(130,157),(95,157),(108,116),(75,146),(61,116),(48,157),(13,157)]
mr3=[(266,62),(298,62),(309,95),(340,62),(377,62),(348,157),(314,157),(326,116),(295,146),(281,116),(269,157),(236,157)]
c3=[(198,62),(236,62),(246,65),(250,70),(251,78),(245,103),(211,103),(215,92),(194,92),(183,130),(203,130),(206,120),(238,120),(233,138),(227,148),(218,154),(207,157),(159,157),(150,154),(146,148),(145,140),(148,128),(159,91),(165,78),(175,69),(186,64)]
# 1/05 red cap/base and C, detached navy bracket stubs and Ms.
t4=[(84,57),(190,9),(294,56),(294,79),(190,36),(84,79)]
b4=[(84,210),(190,253),(294,210),(294,233),(190,277),(84,233)]
s4=[(9,64),(62,64),(76,58),(76,79),(9,79)]
v4=[(9,210),(76,210),(76,231),(62,225),(9,225)]
m4=[(9,94),(40,94),(68,122),(91,99),(128,82),(128,211),(92,197),(92,143),(69,167),(46,144),(46,197),(9,197)]
c4=[(154,83),(218,83),(230,88),(240,97),(240,129),(203,129),(203,115),(200,112),(175,112),(172,115),(172,172),(175,176),(200,176),(203,173),(203,160),(240,160),(240,191),(230,201),(218,206),(154,206),(144,201),(138,192),(138,99),(144,89)]
# 1/06 red side chevrons, navy plate, positive white MCM, six transparent holes.
f5=[(106,9),(314,9),(377,92),(315,172),(104,172),(41,92)]
s5=[(74,9),(96,9),(31,92),(93,172),(71,172),(9,92)]
m5=[(83,53),(108,53),(124,74),(141,53),(166,53),(166,130),(140,130),(140,97),(124,115),(109,97),(109,130),(83,130)]
c5=[(190,53),(224,53),(233,56),(240,63),(243,72),(243,81),(216,81),(216,75),(212,71),(202,71),(198,75),(198,109),(202,113),(212,113),(216,109),(216,103),(243,103),(243,114),(239,122),(232,128),(223,130),(190,130),(181,127),(175,120),(172,112),(172,72),(176,63),(182,56)]
# 1/07 red I-beam rails with short-chord rounded joints; navy MCM.
t6=[(9,9),(345,9),(345,33),(208,33),(202,36),(197,42),(194,49),(194,76),(158,76),(158,49),(156,42),(152,37),(146,33),(9,33)]
b6=[(9,236),(139,236),(146,234),(152,229),(155,222),(155,191),(195,191),(195,220),(197,226),(201,231),(207,235),(214,236),(345,236),(345,258),(9,258)]
m6=[(9,87),(39,87),(62,115),(86,87),(116,87),(116,181),(84,181),(84,135),(62,158),(42,136),(42,181),(9,181)]
c6=[(143,87),(214,87),(227,99),(227,126),(194,126),(194,115),(190,111),(164,111),(160,115),(160,154),(164,158),(190,158),(194,154),(194,145),(227,145),(227,168),(214,180),(143,180),(133,176),(127,167),(127,101),(133,92)]
# 1/08 red letters, open-bottom Ms; navy cap/base.
t7=[(27,77),(183,9),(338,77),(313,87),(183,34),(54,87)]
b7=[(25,208),(57,198),(183,251),(307,198),(338,208),(183,279)]
m7=[(9,91),(62,120),(95,92),(122,92),(122,191),(88,191),(88,145),(59,166),(42,153),(42,191),(9,191)]
c7=[(145,92),(217,92),(230,104),(230,133),(196,133),(196,121),(193,118),(167,118),(164,121),(164,163),(167,166),(193,166),(196,163),(196,152),(230,152),(230,180),(217,191),(145,191),(132,179),(132,105)]
# 1/09 split two-tier roof; navy Ms, long pointed red C.
t8=[(13,83),(183,9),(183,57),(67,102)]
u8=[(78,107),(183,63),(183,102),(135,123)]
m8=[(9,92),(41,103),(70,157),(93,123),(128,135),(128,261),(90,246),(90,180),(63,210),(40,180),(40,226),(9,213)]
c8=[(185,111),(232,133),(232,171),(195,185),(195,154),(173,154),(173,245),(195,245),(195,222),(232,208),(232,265),(185,286),(138,265),(138,134)]
# 2/01 diamond with small rectangular C aperture; four separate navy tips.
f9=[(213,37),(417,145),(213,251),(9,145)]
t9=[(9,140),(187,9),(211,30)]
u9=[(215,30),(239,9),(417,140)]
b9=[(9,150),(186,279),(211,257)]
v9=[(215,257),(417,150),(239,279)]
m9=[(86,108),(111,108),(130,133),(148,108),(174,108),(174,183),(147,183),(147,145),(130,167),(113,146),(113,183),(86,183)]
c9=[(199,107),(228,107),(238,110),(245,115),(247,122),(247,135),(223,135),(223,126),(217,124),(206,125),(206,165),(217,166),(223,164),(223,156),(247,156),(247,170),(243,177),(235,181),(227,183),(199,183),(189,181),(182,176),(179,168),(179,122),(182,114),(189,109)]
# 2/02 navy cap/base and tall C, red inner cap and side Ms.
t10=[(14,93),(169,9),(325,93),(305,104),(169,38),(34,104)]
u10=[(44,110),(169,48),(295,110),(267,126),(169,79),(71,126)]
b10=[(9,248),(169,307),(329,248),(329,256),(169,341),(9,256)]
m10=[(9,115),(38,131),(58,171),(78,137),(108,123),(108,272),(79,261),(79,187),(59,219),(39,187),(39,248),(9,237)]
c10=[(169,96),(217,118),(219,122),(219,165),(185,165),(185,147),(169,140),(153,147),(153,242),(169,248),(185,242),(185,218),(219,218),(219,268),(169,291),(120,269),(119,265),(119,123),(122,118)]
DATA={
(1,2):logo(357,299,layer(0,t1,b1),layer(1,u1,v1,m1,[(x+227,y) for x,y in m1],c1)),
(1,3):logo(379,244,layer(0,t2,c2),layer(1,m2,mirror(m2,189.5))),
(1,4):logo(386,218,layer(0,t3,b3),layer(1,m3,mr3,c3)),
(1,5):logo(377,286,layer(0,t4,b4,c4),layer(1,s4,mirror(s4,188.5),v4,mirror(v4,188.5),m4,mirror(m4,188.5))),
(1,6):logo(417,181,layer(0,s5,mirror(s5,208.5)),layer(1,f5,*[circle(x,y,7) for x,y in [(114,28),(306,28),(62,92),(357,92),(112,153),(305,153)]]),layer(2,m5,[(x+167,y) for x,y in m5],c5)),
(1,7):logo(354,267,layer(0,t6,b6),layer(1,m6,[(x+228,y) for x,y in m6],c6)),
(1,8):logo(364,287,layer(1,t7,b7),layer(0,m7,mirror(m7,182),c7)),
(1,9):logo(370,295,layer(0,t8,mirror(t8,185),c8),layer(1,u8,mirror(u8,185),m8,mirror(m8,185))),
(2,1):logo(426,288,layer(1,t9,u9,b9,v9),layer(0,f9),layer(1,m9,[(x+168,y) for x,y in m9],c9)),
(2,2):logo(338,350,layer(1,t10,b10,c10),layer(0,u10,m10,mirror(m10,169)))}
VALUES=['1_2jEZ697BPdmyn10coLExIClJ0YzAqLQ','1XMd8kjP5dmj9HqwmXLdlXijRKe6CeTUZ','1q_viFpmjEA1J1da5AoatPERmaZ9agSCE','1_rUT7KoThQrmOk0n--PSQJ7RN3n1snt2','1quS4z_0kCP6XxlqDKbajs4vAZxwVW6xe','1DTAUXvrB_xzyPxLJR3mDIpuc0hN2Whkc','1MAa4EatzeGo_kVChj03Ug9DQC4FMurVL','1b7HE54Oc6EHjGfBRRr663n2wYtLgELP6','1LTopCP0o7ZQ_qUnjKZQ_OqmXGZk3gx0o','13N5wPZft78D24LORaZlnc5rS3uRFuTT3']
if __name__=='__main__':
    old=json.loads((R/'04-desain/variasi-svg/batch-23/progress.json').read_text())
    groups=old['groups'];groups['rasio-1']=dict(redrawn=list(range(1,10)),pending=[]);groups['rasio-2']=dict(redrawn=[1,2],pending=list(range(3,10)))
    names={k:f'Max_a_Gambar_kotak_rasio_1_{k[0]}_logo-{k[1]:02}.png' for k in DATA}
    seen={e['sourceSha256'] for p in (R/'04-desain/variasi-svg').glob('batch-*/progress.json') if p.parent.name!='batch-24' for e in json.loads(p.read_text())['entries']}
    for name in names.values():
        digest=hashlib.sha256((R/'google_drive'/name).read_bytes()).hexdigest()
        assert digest not in seen, f'Duplicate source requires alias audit: {name}'
        seen.add(digest)
    export_batch('24',DATA,dict(zip(DATA,VALUES)),209,groups,source_names=names,entry_ids={k:f'exp-rasio-{k[0]:03}-{k[1]:02}' for k in DATA})
    out=R/'04-desain/variasi-svg/batch-24';p=json.loads((out/'progress.json').read_text())
    p.update(uniqueDriveMasters=209,driveSourcesCoveredIncludingDuplicates=227,remainingNotProcessed=115,progressPercent=round(227/342*100,2),redrawOnlyPercent=round(209/342*100,2),progressBasis='209 manual masters + 18 verified duplicate source files / 342 reported files',sourceAliases=old['sourceAliases'],buildPolicy='Redraw only; all APK jobs paused; Android catalog unchanged.')
    for e in p['entries']:e.update(sourceFamily='rasio_1',appIntegration='deferred-no-apk-requested')
    (out/'progress.json').write_text(json.dumps(p,indent=2))
    page=(out/'perbandingan.html').read_text().replace('209 dari 342 sumber','209 master unik; 227 dari 342 sumber tercakup').replace('<strong>133</strong>','<strong>115</strong>').replace('61.11%','66.37%').replace('Kelompok 2 ·','Keluarga rasio_1 · Kelompok 2 ·').replace('Kelompok 1 ·','Keluarga rasio_1 · Kelompok 1 ·')
    page=page.replace('</main>','<h2>Audit terbatas</h2><p>209 master unik + 18 alias = 227/342 (66,37%), sisa 115. Redraw unik saja: 209/342 (61,11%). Sepuluh hash baru berbeda satu sama lain dan dari sumber master terdahulu. 342 bukan jumlah desain unik terverifikasi. Enam lubang mounting 1/06 transparan; MCM putih positif. Tidak ada build APK atau perubahan katalog aplikasi.</p></main>')
    (out/'perbandingan.html').write_text(page)
