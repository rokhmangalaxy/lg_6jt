"""Ten source-specific hand-measured polygon masters; no trace or APK."""
from build_drive_batch_03 import layer,mirror,logo
from design_batch_io import export_batch
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1]
# 4/05 four separated hexagonal facets and a red tall chamfered C.
t1=[(9,86),(144,9),(144,51),(9,120)]
u1=[(154,9),(288,86),(288,120),(154,51)]
b1=[(9,225),(144,288),(144,332),(9,258)]
v1=[(154,288),(288,225),(288,258),(154,332)]
m1=[(9,130),(29,122),(48,151),(69,111),(96,100),(96,244),(68,234),(68,174),(49,198),(32,176),(32,224),(9,216)]
c1=[(120,95),(175,95),(189,110),(189,151),(160,151),(160,129),(136,129),(136,214),(160,214),(160,191),(189,191),(189,231),(175,247),(120,247),(107,233),(107,111)]
# 4/06 parallel red zigzag rails with a detached end segment each.
t2=[(111,66),(126,51),(210,51),(252,10),(302,10),(245,66)]
u2=[(258,66),(314,10),(365,9),(307,66)]
b2=[(16,241),(76,186),(124,186),(68,241)]
v2=[(81,241),(136,186),(271,186),(256,200),(174,200),(130,241)]
m2=[(9,82),(35,82),(66,119),(102,78),(128,78),(128,177),(96,177),(96,135),(65,164),(40,137),(40,178),(9,178)]
c2=[(152,78),(226,78),(241,92),(241,119),(209,119),(209,105),(169,105),(169,151),(209,151),(209,140),(241,140),(241,162),(226,177),(152,177),(138,163),(138,92)]
mr2=[(251,80),(275,80),(306,119),(337,80),(367,80),(367,177),(334,177),(334,135),(305,164),(279,136),(279,177),(251,177)]
# 4/07 red clipped slabs, navy MCM.
t3=[(9,9),(380,9),(380,21),(346,47),(42,47),(9,21)]
b3=[(42,160),(346,160),(380,187),(380,198),(9,198),(9,187)]
m3=[(42,59),(64,59),(91,92),(115,59),(142,59),(142,151),(114,151),(114,111),(91,135),(70,111),(70,151),(42,151)]
c3=[(165,59),(224,59),(237,71),(237,95),(207,95),(207,83),(181,83),(181,127),(207,127),(207,116),(237,116),(237,138),(224,151),(165,151),(152,138),(152,71)]
# 4/08 open hexagon, navy roof, red triangular side flags and lower chevron.
t4=[(68,100),(203,9),(337,100),(297,100),(203,47),(111,100)]
b4=[(68,196),(107,196),(203,250),(301,196),(337,196),(203,289)]
s4=[(9,146),(52,115),(52,180)]
m4=[(69,111),(91,110),(110,138),(133,106),(156,103),(156,197),(131,193),(131,151),(109,174),(93,152),(93,186),(69,185)]
c4=[(178,101),(229,101),(241,111),(241,138),(215,138),(215,125),(193,125),(193,174),(215,174),(215,162),(241,162),(241,186),(229,197),(178,198),(166,187),(166,112)]
mr4=[(251,103),(275,106),(297,137),(315,110),(337,111),(337,185),(313,186),(313,152),(295,174),(275,152),(275,193),(251,197)]
# 4/09 large folded emblem above compact navy initials.
t5=[(19,34),(61,10),(156,63),(255,10),(295,32),(155,112)]
l5=[(9,38),(59,66),(59,204),(9,175)]
r5=[(69,89),(102,107),(102,174),(69,198)]
v5=[(112,113),(153,136),(199,112),(199,143),(153,171),(112,144)]
m5=[(10,212),(35,212),(57,239),(81,212),(109,212),(109,291),(82,291),(82,252),(57,273),(35,252),(35,291),(10,291)]
c5=[(131,212),(190,212),(203,223),(203,244),(177,244),(177,233),(147,233),(147,268),(177,268),(177,261),(203,261),(203,280),(190,291),(131,291),(119,280),(119,223)]
# 5/01 red broad diamond with four navy tips; positive navy lettering.
d6=[(215,34),(420,136),(215,238),(9,136)]
t6=[(32,117),(189,10),(209,28)]
u6=[(219,28),(239,9),(394,117)]
b6=[(32,154),(188,262),(209,244)]
v6=[(219,244),(394,154),(239,262)]
m6=[(84,106),(109,106),(126,124),(142,106),(170,106),(170,167),(146,167),(146,133),(126,153),(107,133),(107,167),(84,167)]
c6=[(198,103),(231,103),(240,105),(247,110),(250,118),(250,130),(227,130),(227,124),(224,120),(208,120),(204,124),(204,148),(208,152),(224,152),(227,148),(227,142),(250,142),(250,154),(247,162),(240,167),(231,169),(198,169),(189,167),(183,162),(180,154),(180,119),(183,111),(189,106)]
# 5/02 red narrow tall C; two broad independently tapered navy Ms.
m7=[(9,65),(57,100),(118,46),(118,252),(84,231),(84,124),(59,146),(42,130),(42,224),(9,205)]
mr7=[(227,46),(287,98),(337,62),(337,204),(304,225),(304,130),(287,145),(261,122),(261,230),(227,251)]
c7=[(174,9),(219,38),(219,104),(185,119),(185,63),(174,56),(161,64),(161,234),(173,242),(185,234),(185,169),(219,154),(219,257),(173,286),(127,258),(127,39)]
# 5/03 red raised rail ends, compact navy Ms and rounded C.
t8=[(9,48),(83,48),(188,9),(291,48),(372,48),(372,62),(258,62),(188,38),(116,62),(9,62)]
b8=[(9,176),(116,176),(188,202),(258,176),(372,176),(372,190),(291,190),(188,230),(83,190),(9,190)]
m8=[(9,76),(39,76),(64,112),(90,76),(125,76),(125,164),(91,164),(91,123),(65,154),(40,125),(40,164),(9,164)]
c8=[(153,76),(221,76),(229,79),(234,85),(237,93),(237,111),(205,111),(205,101),(171,101),(171,141),(205,141),(205,129),(237,129),(237,147),(234,156),(229,161),(221,164),(153,164),(146,161),(140,156),(138,147),(138,93),(141,85),(146,79)]
# 5/04 two red oblique slabs with chamfered red? source initials all navy.
t9=[(88,9),(400,9),(385,31),(63,44)]
b9=[(28,145),(345,145),(327,170),(9,170)]
m9=[(72,54),(102,54),(106,78),(133,53),(169,53),(137,133),(106,133),(122,96),(91,119),(82,97),(66,133),(30,133)]
mr9=[(278,53),(301,53),(309,77),(337,52),(375,51),(338,133),(309,133),(326,97),(295,119),(285,98),(271,133),(244,133)]
c9=[(193,54),(266,53),(253,86),(224,86),(229,75),(203,75),(188,111),(213,111),(217,102),(246,102),(233,133),(164,133),(154,118),(173,70)]
# 5/05 four split frame facets, navy Ms and short angular C.
t10=[(9,92),(161,10),(161,57),(9,112)]
u10=[(172,10),(323,92),(323,112),(172,57)]
b10=[(9,210),(161,254),(161,296),(9,238)]
v10=[(172,254),(323,210),(323,238),(172,296)]
m10=[(9,124),(35,117),(54,142),(80,107),(108,102),(108,215),(79,210),(79,160),(57,187),(37,162),(37,205),(9,200)]
c10=[(132,100),(201,100),(216,116),(216,144),(182,144),(182,130),(147,130),(147,185),(182,185),(182,169),(216,169),(216,200),(201,216),(132,216),(117,200),(117,116)]
DATA={
(4,5):logo(297,341,layer(0,t1,v1,c1),layer(1,u1,b1,m1,mirror(m1,148.5))),
(4,6):logo(376,250,layer(0,t2,u2,b2,v2),layer(1,m2,mr2,c2)),
(4,7):logo(389,207,layer(0,t3,b3),layer(1,m3,[(x+204,y) for x,y in m3],c3)),
(4,8):logo(405,298,layer(0,b4,s4,mirror(s4,202.5)),layer(1,t4,m4,mr4,c4)),
(4,9):logo(314,300,layer(0,t5,r5,mirror(r5,156.5)),layer(1,l5,mirror(l5,156.5),v5,m5,[(x+200,y) for x,y in m5],c5)),
(5,1):logo(429,271,layer(1,t6,u6,b6,v6),layer(0,d6),layer(1,m6,[(x+175,y) for x,y in m6],c6)),
(5,2):logo(346,295,layer(0,c7),layer(1,m7,mr7)),
(5,3):logo(382,239,layer(0,t8,b8),layer(1,m8,[(x+239,y) for x,y in m8],c8)),
(5,4):logo(409,179,layer(0,t9,b9),layer(1,m9,mr9,c9)),
(5,5):logo(332,306,layer(0,t10,b10),layer(1,u10,v10,m10,mirror(m10,166),c10))}
VALUES=['1tz-QagibfBulVXXlt706GmUhvVFK7WlP','1s5Q8CjAPN-MppHhY41S5iuFCZP4KCK9a','1czw27ZoUHSikp7gfHUAogSSrCDIVFPJW','1nY3Os2cq4uh__BUXGPQK18tV6jZSwqI_','1k3O23TrtabZ-wmd_LRSkfMysdW-nrJoi','1rPSRJoQq1gBVF03aCoTMIexl6SZ4Hw0O','1czQd3tb_Bs1OaQ_FDWPE-_LB8PPFsD9y','1oNLbfpbE3ogb_8GQDxLyBRP9Dxupd-Yo','1sRCUJ2uaeWd9jfgxiX1e7yEelVmWfyI0','19E-Wis4LICo1g9KuAyRUSQudiU1QFkD5']
if __name__=='__main__':
    old=json.loads((R/'04-desain/variasi-svg/batch-26/progress.json').read_text())
    groups=old['groups'];groups['rasio-4']=dict(redrawn=list(range(1,10)),pending=[]);groups['rasio-5']=dict(redrawn=[1,2,3,4,5],pending=list(range(6,10)))
    names={k:f'Max_a_Gambar_kotak_rasio_1_{k[0]}_logo-{k[1]:02}.png' for k in DATA}
    seen={e['sourceSha256'] for p in (R/'04-desain/variasi-svg').glob('batch-*/progress.json') if p.parent.name!='batch-27' for e in json.loads(p.read_text())['entries']}
    for name in names.values():
        digest=hashlib.sha256((R/'google_drive'/name).read_bytes()).hexdigest()
        assert digest not in seen, f'Duplicate source requires alias audit: {name}'
        seen.add(digest)
    export_batch('27',DATA,dict(zip(DATA,VALUES)),239,groups,source_names=names,entry_ids={k:f'exp-rasio-{k[0]:03}-{k[1]:02}' for k in DATA})
    out=R/'04-desain/variasi-svg/batch-27';p=json.loads((out/'progress.json').read_text())
    p.update(uniqueDriveMasters=239,driveSourcesCoveredIncludingDuplicates=257,remainingNotProcessed=85,progressPercent=round(257/342*100,2),redrawOnlyPercent=round(239/342*100,2),progressBasis='239 manual masters + 18 verified duplicate source files / 342 reported files',sourceAliases=old['sourceAliases'],buildPolicy='Redraw only; all APK jobs paused; Android catalog unchanged.')
    for e in p['entries']:e.update(sourceFamily='rasio_1',appIntegration='deferred-no-apk-requested')
    (out/'progress.json').write_text(json.dumps(p,indent=2))
    page=(out/'perbandingan.html').read_text().replace('239 dari 342 sumber','239 master unik; 257 dari 342 sumber tercakup').replace('<strong>103</strong>','<strong>85</strong>').replace('69.88%','75.15%').replace('Kelompok 4 ·','Keluarga rasio_1 · Kelompok 4 ·').replace('Kelompok 5 ·','Keluarga rasio_1 · Kelompok 5 ·')
    page=page.replace('</main>','<h2>Audit terbatas</h2><p>239 master unik + 18 alias = 257/342 (75,15%), sisa 85. Redraw unik saja: 239/342 (69,88%). Sepuluh hash baru berbeda satu sama lain dan dari sumber master terdahulu. 342 bukan jumlah desain unik terverifikasi. MCM 5/01 navy positif, bukan lubang; seluruh batch tanpa bidang putih; celah antarkomponen transparan. Tidak ada build APK atau perubahan katalog aplikasi.</p></main>')
    (out/'perbandingan.html').write_text(page)
