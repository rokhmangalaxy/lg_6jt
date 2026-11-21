"""Source-specific manually measured rasio polygons. Design only; no APK."""
from build_drive_batch_03 import layer,mirror,logo
from design_batch_io import export_batch
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1]
# 15/08: two open frame halves separated by diagonal gaps.
f1=[(9,9),(201,9),(179,31),(31,31),(31,149),(176,149),(154,170),(9,170)]
g1=[(215,9),(360,9),(360,170),(169,170),(191,149),(338,149),(338,31),(193,31)]
m1=[(48,54),(71,54),(92,76),(114,54),(137,54),(137,130),(111,130),(111,92),(92,110),(73,92),(73,130),(48,130)]
c1=[(167,54),(205,54),(223,69),(223,85),(198,85),(198,76),(194,73),(176,73),(172,77),(172,107),(176,111),(194,111),(198,107),(198,100),(223,100),(223,116),(206,130),(166,130),(154,125),(147,116),(147,69),(154,60)]
# 15/09: red upper chevron above twin navy peaks; bottom red rail.
t2=[(178,9),(235,69),(208,99),(177,69),(147,99),(119,70)]
f2=[(9,157),(98,57),(177,142),(258,57),(344,157),(297,157),(258,115),(221,154),(134,154),(95,115),(57,157)]
b2=[(9,256),(344,256),(344,278),(9,278)]
m2=[(30,169),(54,169),(77,194),(101,169),(125,169),(125,245),(98,245),(98,208),(77,228),(56,208),(56,245),(30,245)]
c2=[(152,168),(203,168),(218,181),(218,198),(190,198),(190,189),(166,189),(164,192),(164,224),(167,227),(188,227),(190,224),(190,216),(218,216),(218,233),(203,246),(152,246),(138,233),(138,181)]
# 16/01: diamond red field; navy unbroken top and bottom caps; white letters.
f3=[(213,49),(418,142),(213,237),(9,142)]
t3=[(30,125),(213,9),(397,125),(213,44)]
b3=[(30,159),(213,277),(397,159),(213,243)]
m3=[(86,110),(111,110),(128,134),(145,110),(170,110),(170,175),(146,175),(146,145),(128,163),(111,145),(111,175),(86,175)]
c3=[(192,110),(234,110),(241,112),(246,118),(248,125),(248,135),(223,135),(223,130),(220,126),(210,126),(206,130),(206,157),(210,161),(219,161),(223,157),(223,150),(248,150),(248,161),(245,169),(239,174),(232,175),(192,175),(184,172),(179,166),(178,157),(178,128),(180,119),(185,113)]
# 16/02: four red outer facets; central C has two tiny pointed lower notches.
t4=[(9,91),(175,9),(175,46),(9,116)]
b4=[(9,204),(175,251),(175,287),(9,224)]
m4=[(9,133),(36,116),(56,140),(78,101),(112,87),(112,217),(78,210),(78,162),(57,189),(41,168),(41,201),(9,193)]
c4=[(176,62),(225,80),(229,85),(229,121),(177,103),(162,109),(162,188),(178,194),(189,189),(189,184),(229,169),(229,216),(225,221),(179,233),(176,217),(173,233),(124,219),(124,85),(128,79)]
# 16/03: wide red top chamfer strip and stepped bottom strip, navy MCM.
t5=[(54,9),(328,9),(371,51),(327,47),(53,47),(9,51)]
b5=[(9,170),(58,170),(67,177),(314,177),(323,170),(371,170),(330,210),(51,210)]
m5=[(24,62),(55,62),(81,97),(110,62),(140,62),(140,160),(109,160),(109,118),(80,150),(55,117),(55,160),(24,160)]
c5=[(164,62),(226,62),(238,73),(238,101),(205,101),(205,89),(184,89),(184,135),(188,139),(202,139),(205,135),(205,124),(238,124),(238,149),(227,160),(164,160),(152,149),(152,74)]
# 16/04: red roof / navy foot, upright red C and navy Ms.
t6=[(9,49),(200,9),(390,49),(200,40)]
b6=[(9,187),(200,224),(390,187),(200,194)]
m6=[(16,62),(39,62),(75,101),(111,62),(134,62),(134,175),(98,175),(98,123),(75,149),(51,124),(51,175),(16,175)]
c6=[(164,56),(234,56),(252,73),(252,104),(214,104),(214,89),(211,87),(186,87),(183,90),(183,149),(186,152),(210,152),(214,149),(214,134),(252,134),(252,163),(234,180),(164,180),(147,163),(147,73)]
# 16/05: red detached vertical piers and small inner triangular tips.
p7=[(9,9),(48,34),(48,218),(9,243)]
a7=[(55,40),(99,69),(55,69)]
b7=[(55,184),(99,184),(55,213)]
m7=[(55,80),(78,80),(99,113),(122,80),(144,80),(144,173),(116,173),(116,132),(103,152),(95,152),(82,134),(82,173),(55,173)]
c7=[(165,80),(214,80),(223,89),(223,116),(196,116),(196,103),(182,103),(179,106),(179,148),(182,151),(196,151),(196,138),(223,138),(223,164),(214,173),(165,173),(153,163),(153,91)]
# 16/06: oblique navy Ms/red C, four alternating offset rail pieces.
t8=[(73,12),(229,12),(210,39),(54,39)]
u8=[(243,9),(378,9),(358,36),(222,36)]
b8=[(32,166),(204,166),(185,193),(9,193)]
v8=[(217,165),(344,165),(325,190),(198,190)]
m8=[(49,53),(87,53),(92,86),(122,53),(156,53),(125,152),(90,152),(107,101),(80,131),(70,100),(51,152),(15,152)]
c8=[(179,53),(252,53),(241,88),(211,88),(214,77),(199,77),(182,128),(198,128),(202,119),(233,119),(226,140),(212,150),(149,150),(142,143),(164,66)]
mr8=[(266,53),(297,53),(307,84),(334,53),(375,53),(345,150),(312,150),(327,101),(298,130),(286,101),(268,150),(235,150)]
# 16/07: split red roof, navy foot, central C made of separate facets.
t9=[(9,83),(186,9),(186,48),(9,112)]
b9=[(9,207),(186,244),(186,268),(9,229)]
m9=[(10,123),(41,111),(62,136),(89,97),(121,86),(121,216),(83,209),(83,164),(63,182),(42,164),(42,203),(10,198)]
c9a=[(186,64),(186,104),(173,110),(173,186),(186,191),(186,231),(133,219),(133,89),(137,82)]
c9b=[(190,64),(236,82),(241,87),(241,122),(190,104)]
c9c=[(190,191),(241,170),(241,215),(237,220),(190,231)]
# 16/08: red cap/base, navy open side chevrons and MCM.
t10=[(69,84),(214,9),(359,84),(214,40)]
b10=[(69,177),(214,251),(359,177),(214,220)]
s10=[(9,131),(65,89),(65,106),(33,131),(65,155),(65,171)]
m10=[(75,87),(99,87),(119,116),(139,87),(168,87),(168,174),(138,174),(138,136),(120,159),(103,137),(103,174),(75,174)]
c10=[(189,87),(238,87),(249,98),(249,120),(221,120),(221,108),(205,108),(205,154),(221,154),(221,142),(249,142),(249,163),(238,174),(189,174),(178,163),(178,98)]
DATA={
(15,8):logo(369,179,layer(1,f1,m1,[(x+184,y) for x,y in m1],c1),layer(0,g1)),
(15,9):logo(353,287,layer(0,t2,b2),layer(1,f2,m2,[(x+198,y) for x,y in m2],c2)),
(16,1):logo(426,285,layer(1,t3,b3),layer(0,f3),layer(2,m3,[(x+171,y) for x,y in m3],c3)),
(16,2):logo(352,296,layer(0,t4,mirror(t4,176),b4,mirror(b4,176)),layer(1,m4,mirror(m4,176),c4)),
(16,3):logo(380,218,layer(0,t5,b5),layer(1,m5,[(x+224,y) for x,y in m5],c5)),
(16,4):logo(399,233,layer(0,t6,c6),layer(1,b6,m6,mirror(m6,199.5))),
(16,5):logo(376,252,layer(0,p7,mirror(p7,188),a7,mirror(a7,188),b7,mirror(b7,188)),layer(1,m7,[(x+177,y) for x,y in m7],c7)),
(16,6):logo(387,202,layer(0,t8,v8,c8),layer(1,u8,b8,m8,mr8)),
(16,7):logo(373,276,layer(0,t9,mirror(t9,186.5)),layer(1,b9,mirror(b9,186.5),m9,mirror(m9,186.5),c9a,c9b,c9c)),
(16,8):logo(428,260,layer(0,t10,b10),layer(1,s10,mirror(s10,214),m10,[(x+184,y) for x,y in m10],c10))}
VALUES=['1OLxp2EoqcKoNdS6r23FZsiAEiR6yGs-w','1G5pb9IgCqr1nx30CvmZBXQRSP_7cfp74','15pkdCudcrnuUQrce3BJGLwRT-jCsnqa9','1jEA9C9kxU6ky_FsSm51D0l5hJ2pZTpy1','1IQNIk2eFV0uFQK9vrqkecAOeKgprIM1S','154eaFsIbi7k0zuNHQxJqh7cE6gkuGdF-','13WQfIXyrE8UgKMz_XgILMgMbzAXps0Dx','1r4n7RLJooN_oxY4QdFqXmdoh-E7ZfhnH','1nAEnq1lN5Zlx5KfcKjv5nRixDU_cS2y0','1wMkHCkTdsTV-uUu5vvPbtjuzv9qIitm0']
if __name__=='__main__':
    old=json.loads((R/'04-desain/variasi-svg/batch-20/progress.json').read_text())
    groups=old['groups'];groups['rasio-15']=dict(redrawn=list(range(1,10)),pending=[]);groups['rasio-16']=dict(redrawn=list(range(1,9)),pending=[9])
    names={k:f'Max_a_Gambar_kotak_rasio_1_{k[0]}_logo-{k[1]:02}.png' for k in DATA}
    seen={e['sourceSha256'] for p in (R/'04-desain/variasi-svg').glob('batch-*/progress.json') if p.parent.name!='batch-21' for e in json.loads(p.read_text())['entries']}
    for name in names.values():
        digest=hashlib.sha256((R/'google_drive'/name).read_bytes()).hexdigest()
        assert digest not in seen, f'Duplicate source requires alias audit: {name}'
        seen.add(digest)
    export_batch('21',DATA,dict(zip(DATA,VALUES)),179,groups,source_names=names,entry_ids={k:f'exp-rasio-{k[0]:03}-{k[1]:02}' for k in DATA})
    out=R/'04-desain/variasi-svg/batch-21';p=json.loads((out/'progress.json').read_text())
    p.update(uniqueDriveMasters=179,driveSourcesCoveredIncludingDuplicates=197,remainingNotProcessed=145,progressPercent=round(197/342*100,2),redrawOnlyPercent=round(179/342*100,2),progressBasis='179 manual masters + 18 verified duplicate source files / 342 reported files',sourceAliases=old['sourceAliases'],buildPolicy='Redraw only; all APK jobs paused; Android catalog unchanged.')
    for e in p['entries']:e.update(sourceFamily='rasio_1',appIntegration='deferred-no-apk-requested')
    (out/'progress.json').write_text(json.dumps(p,indent=2))
    page=(out/'perbandingan.html').read_text().replace('179 dari 342 sumber','179 master unik; 197 dari 342 sumber tercakup').replace('<strong>163</strong>','<strong>145</strong>').replace('52.34%','57.60%').replace('Kelompok 16 ·','Keluarga rasio_1 · Kelompok 16 ·').replace('Kelompok 15 ·','Keluarga rasio_1 · Kelompok 15 ·')
    page=page.replace('</main>','<h2>Audit terbatas</h2><p>179 master unik + 18 alias = 197/342 (57,60%), sisa 145. Redraw unik saja: 179/342 (52,34%). Sepuluh hash baru berbeda satu sama lain dan dari sumber master terdahulu. 342 bukan jumlah desain unik terverifikasi. Huruf putih 16/01 positif; celah antarsegmen transparan. Tidak ada build APK atau perubahan katalog aplikasi.</p></main>')
    (out/'perbandingan.html').write_text(page)
