"""Ten source-specific manually authored rasio masters; no tracing/APK."""
from build_drive_batch_03 import layer,mirror,logo
from design_batch_io import export_batch
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1]
# 6/07 broad swept Ms, red C and two independent lower chevrons.
m1=[(9,10),(74,74),(102,50),(131,40),(131,166),(102,149),(102,96),(75,115),(38,82),(38,128),(9,148)]
c1=[(181,25),(221,40),(221,81),(195,81),(195,61),(169,61),(169,129),(195,129),(195,112),(221,112),(221,148),(181,166),(141,148),(141,40)]
b1=[(28,145),(44,134),(181,200),(317,134),(333,145),(181,217)]
v1=[(26,154),(181,224),(335,154),(181,252)]
# 6/08 double diamond counter rings with navy positive lettering.
o2=[(216,10),(424,123),(214,266),(9,123)]
i2=[(216,27),(402,123),(214,245),(31,123)]
r2=[(216,36),(391,124),(214,236),(42,124)]
j2=[(216,54),(371,124),(214,212),(62,124)]
m2=[(105,110),(122,104),(138,120),(153,98),(174,92),(174,168),(155,163),(155,132),(139,148),(123,133),(123,154),(105,148)]
c2=[(199,87),(231,87),(239,91),(245,99),(245,117),(226,117),(226,107),(205,107),(205,150),(226,150),(226,139),(245,139),(245,158),(239,166),(231,170),(199,170),(191,166),(185,158),(185,99),(191,91)]
# 6/09 navy cap plus red inner cap, tall navy Ms and red C.
t3=[(24,76),(178,9),(330,76),(316,79),(178,41),(38,79)]
u3=[(51,85),(178,49),(303,85),(272,101),(178,73),(82,101)]
b3=[(48,223),(177,268),(305,223),(305,230),(177,300),(48,230)]
m3=[(9,80),(37,91),(69,139),(100,123),(124,111),(124,228),(94,216),(94,178),(70,186),(38,149),(38,224),(9,212)]
c3=[(178,98),(219,113),(219,151),(192,151),(192,137),(164,137),(164,203),(192,203),(192,189),(219,189),(219,229),(178,245),(135,229),(135,113)]
# 7/01 red diamond with single navy cap/base and white positive MCM.
d4=[(219,51),(429,132),(219,231),(9,132)]
t4=[(55,106),(219,10),(381,106),(219,42)]
b4=[(55,165),(219,241),(381,165),(219,271)]
m4=[(90,109),(117,109),(134,131),(150,109),(176,109),(176,179),(151,179),(151,143),(134,162),(114,143),(114,174),(90,168)]
c4=[(197,109),(245,109),(255,119),(255,132),(231,132),(231,124),(213,124),(210,127),(210,161),(213,164),(231,164),(231,155),(255,155),(255,170),(245,179),(197,179),(186,169),(186,120)]
mr4=[(265,109),(292,109),(307,131),(323,110),(349,110),(349,168),(326,174),(326,143),(308,162),(290,143),(290,179),(265,179)]
# 7/02 thick red roof, navy angular C and separately tapered Ms.
t5=[(10,103),(181,9),(352,103),(298,128),(181,68),(63,128)]
m5=[(9,111),(38,127),(62,157),(84,137),(114,123),(114,287),(83,270),(83,179),(62,201),(42,179),(42,253),(9,235)]
c5=[(181,88),(237,115),(237,165),(203,148),(203,142),(181,130),(157,142),(157,215),(181,228),(203,215),(203,208),(237,191),(237,234),(181,262),(124,234),(124,115)]
# 7/03 shallow red cap/base and wide navy C with short chamfers.
t6=[(9,77),(186,9),(361,77),(361,84),(186,45),(9,84)]
b6=[(9,175),(186,215),(361,175),(361,185),(186,255),(9,185)]
m6=[(9,97),(42,89),(67,119),(95,82),(126,78),(126,185),(94,178),(94,134),(67,166),(41,140),(41,171),(9,164)]
c6=[(151,77),(220,77),(233,90),(233,118),(201,118),(201,104),(172,104),(170,106),(170,156),(172,159),(201,159),(201,145),(233,145),(233,171),(220,185),(151,185),(137,172),(137,90)]
# 7/04 three upper and three lower red extrusion facets, each separate.
t7=[(11,36),(66,9),(369,9),(326,36)]
u7=[(10,42),(325,42),(325,82),(43,82),(43,62),(10,52)]
w7=[(332,42),(369,16),(369,26),(341,49),(341,82),(332,82)]
b7=[(43,195),(325,195),(325,237),(10,237),(43,210)]
v7=[(332,195),(341,195),(341,210),(369,215),(337,237),(332,237)]
z7=[(10,244),(338,244),(369,222),(369,234),(338,255),(10,255)]
m7=[(20,96),(52,96),(73,121),(94,96),(126,96),(126,185),(94,185),(94,146),(73,166),(52,146),(52,185),(20,185)]
c7=[(156,95),(219,95),(233,108),(233,131),(201,131),(201,117),(175,117),(175,163),(201,163),(201,150),(233,150),(233,171),(219,185),(156,185),(143,172),(143,108)]
# 7/05 large red open M frame with positive navy M nested, compact initials below.
f8=[(9,50),(36,63),(36,9),(142,67),(253,9),(253,63),(279,50),(279,201),(226,225),(226,70),(142,113),(60,70),(60,225),(9,201)]
a8=[(72,88),(142,128),(214,88),(214,225),(187,207),(187,148),(143,173),(99,148),(99,207),(72,225)]
m8=[(16,235),(40,235),(57,257),(75,235),(97,235),(97,299),(75,299),(75,272),(57,287),(40,272),(40,299),(16,299)]
c8=[(118,234),(166,234),(177,244),(177,259),(153,259),(153,250),(132,250),(132,283),(153,283),(153,275),(177,275),(177,289),(166,299),(118,299),(107,289),(107,244)]
# 7/06 four detached red/navy compass facets around navy initials.
t9=[(123,79),(222,9),(317,79),(317,94),(222,63),(123,94)]
b9=[(123,211),(222,243),(317,211),(317,232),(222,295),(123,232)]
s9=[(10,151),(108,85),(108,99),(43,151),(108,206),(108,222)]
m9=[(91,126),(115,109),(135,136),(153,109),(178,109),(178,194),(153,194),(153,154),(135,176),(115,154),(115,184),(91,173)]
c9=[(200,109),(244,109),(255,120),(255,141),(232,141),(232,130),(228,127),(215,127),(211,130),(211,173),(215,176),(228,176),(232,173),(232,163),(255,163),(255,183),(244,194),(200,194),(188,183),(188,120)]
# 7/07 two interlocking open outer brackets, compact navy MCM.
l10=[(9,101),(189,9),(263,43),(38,131),(38,215),(84,238),(84,290),(9,253)]
r10=[(278,49),(352,83),(352,242),(169,330),(97,295),(329,212),(329,124),(278,103)]
m10=[(50,137),(75,132),(95,156),(113,130),(138,129),(138,212),(112,212),(112,175),(95,193),(77,176),(77,212),(50,212)]
c10=[(162,129),(210,129),(222,141),(222,161),(198,161),(198,149),(175,149),(175,190),(198,190),(198,181),(222,181),(222,200),(210,212),(162,212),(150,200),(150,141)]
mr10=[(232,129),(256,130),(273,154),(293,130),(318,132),(318,208),(295,212),(295,175),(276,193),(258,175),(258,212),(232,212)]
DATA={
(6,7):logo(362,261,layer(0,c1,b1),layer(1,m1,mirror(m1,181),v1)),
(6,8):logo(433,275,layer(1,o2,i2,m2,mirror(m2,216),c2),layer(0,r2,j2)),
(6,9):logo(354,309,layer(0,u3,b3,c3),layer(1,t3,m3,mirror(m3,177))),
(7,1):logo(438,280,layer(1,t4,b4),layer(0,d4),layer(2,m4,mr4,c4)),
(7,2):logo(362,296,layer(0,t5),layer(1,m5,mirror(m5,181),c5)),
(7,3):logo(371,264,layer(0,t6,b6),layer(1,m6,mirror(m6,185.5),c6)),
(7,4):logo(379,264,layer(0,t7,u7,w7,b7,v7,z7),layer(1,m7,[(x+228,y) for x,y in m7],c7)),
(7,5):logo(289,308,layer(0,f8),layer(1,a8,m8,[(x+170,y) for x,y in m8],c8)),
(7,6):logo(430,304,layer(0,t9,b9),layer(1,s9,mirror(s9,215.5),m9,mirror(m9,219),c9)),
(7,7):logo(361,340,layer(0,l10),layer(1,r10,m10,mr10,c10))}
VALUES=['1Pvm5RTUB4x-MTHbaKT4oPCGG9O0pCto3','1P-ACDjIOPaCae0kPVnZNo2Q_Z6VLfoaC','1lFJkfG4TXl_ifav2bCT6oIbDmL9N2V2U','17wg0oJFoai1TxvNs5Eud8Qfzn_uMuBl0','10HwkaMIhRQ-VsRQx3FduPqlWOqQIP3NM','1FCSeYcgD3jEnjTscKWSUH404oU6xFGg1','1vjHGruNUWRVuNNX61J4WcLqjMVXtyW4u','1fgu2mBhugKClg5dT3VmCg2aT2r4A1B5i','1jR0QaQHlR5yzUSQ7LhhYz374HqMTXZLy','1VaspDzRXc0HmiCkZyS4-T_rKuTCacjVS']
if __name__=='__main__':
    old=json.loads((R/'04-desain/variasi-svg/batch-28/progress.json').read_text())
    groups=old['groups'];groups['rasio-6']=dict(redrawn=list(range(1,10)),pending=[]);groups['rasio-7']=dict(redrawn=list(range(1,8)),pending=[8,9])
    names={k:f'Max_a_Gambar_kotak_rasio_1_{k[0]}_logo-{k[1]:02}.png' for k in DATA}
    seen={e['sourceSha256'] for p in (R/'04-desain/variasi-svg').glob('batch-*/progress.json') if p.parent.name!='batch-29' for e in json.loads(p.read_text())['entries']}
    for name in names.values():
        digest=hashlib.sha256((R/'google_drive'/name).read_bytes()).hexdigest()
        assert digest not in seen, f'Duplicate source requires alias audit: {name}'
        seen.add(digest)
    export_batch('29',DATA,dict(zip(DATA,VALUES)),259,groups,source_names=names,entry_ids={k:f'exp-rasio-{k[0]:03}-{k[1]:02}' for k in DATA})
    out=R/'04-desain/variasi-svg/batch-29';p=json.loads((out/'progress.json').read_text())
    p.update(uniqueDriveMasters=259,driveSourcesCoveredIncludingDuplicates=277,remainingNotProcessed=65,progressPercent=round(277/342*100,2),redrawOnlyPercent=round(259/342*100,2),progressBasis='259 manual masters + 18 verified duplicate source files / 342 reported files',sourceAliases=old['sourceAliases'],buildPolicy='Redraw only; all APK jobs paused; Android catalog unchanged.')
    for e in p['entries']:e.update(sourceFamily='rasio_1',appIntegration='deferred-no-apk-requested')
    (out/'progress.json').write_text(json.dumps(p,indent=2))
    page=(out/'perbandingan.html').read_text().replace('259 dari 342 sumber','259 master unik; 277 dari 342 sumber tercakup').replace('<strong>83</strong>','<strong>65</strong>').replace('75.73%','80.99%').replace('Kelompok 6 ·','Keluarga rasio_1 · Kelompok 6 ·').replace('Kelompok 7 ·','Keluarga rasio_1 · Kelompok 7 ·')
    page=page.replace('</main>','<h2>Audit terbatas</h2><p>259 master unik + 18 alias = 277/342 (80,99%), sisa 65. Redraw unik saja: 259/342 (75,73%). Sepuluh hash baru berbeda satu sama lain dan dari sumber master terdahulu. 342 bukan jumlah desain unik terverifikasi. MCM putih 7/01 positif; dua ring 6/08 memiliki counter transparan; celah antarkomponen transparan. Tidak ada build APK atau perubahan katalog aplikasi.</p></main>')
    (out/'perbandingan.html').write_text(page)
