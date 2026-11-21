"""Manual measured rasio-family polygons; no tracing, integration or APK."""
from build_drive_batch_03 import layer,mirror,logo
from design_batch_io import export_batch
from pathlib import Path
import json,hashlib,math
R=Path(__file__).resolve().parents[1]
# rasio14/07: oversize open M frame above small MCM.
t1=[(45,9),(180,91),(316,9),(316,46),(180,145),(45,46)]
s1=[(9,31),(98,100),(98,152),(57,120),(57,231),(9,263)]
m1=[(77,165),(98,165),(111,183),(124,165),(146,165),(146,229),(126,229),(126,196),(111,214),(97,196),(97,229),(77,229)]
c1=[(168,158),(192,158),(200,161),(205,167),(207,176),(207,187),(188,187),(188,180),(185,176),(175,176),(171,180),(171,211),(174,215),(185,215),(188,212),(188,205),(207,205),(207,217),(204,226),(197,232),(168,234),(159,230),(154,222),(152,213),(152,178),(154,168),(160,161)]
# rasio14/08: red nameplates with true transparent round mounting holes.
t2=[(103,9),(281,9),(342,68),(40,68)]
b2=[(40,192),(342,192),(282,248),(100,248)]
def hole(x,y,r):
    return [(round(x+r*math.cos(i*math.pi/8),3),round(y+r*math.sin(i*math.pi/8),3)) for i in range(16)]
m2=[(9,83),(46,83),(70,113),(97,82),(130,82),(130,181),(96,181),(96,130),(70,156),(63,156),(44,131),(44,179),(9,179)]
c2=[(163,81),(220,81),(232,84),(240,91),(243,102),(243,120),(209,120),(209,110),(205,105),(180,105),(175,110),(175,154),(179,158),(204,158),(208,154),(208,144),(243,144),(243,162),(238,173),(229,179),(217,181),(163,181),(152,178),(144,172),(140,161),(140,103),(144,91),(152,84)]
# rasio14/09: vertical hexagonal monogram with tall central navy C.
t3=[(150,9),(291,80),(291,110),(150,43),(9,110),(9,80)]
b3=[(9,229),(150,286),(291,229),(291,257),(150,326),(9,257)]
m3=[(9,120),(33,109),(49,133),(67,94),(97,80),(97,253),(67,241),(67,162),(50,191),(35,169),(35,229),(9,219)]
c3=[(150,55),(194,77),(194,138),(161,123),(161,104),(150,97),(140,103),(140,229),(150,235),(161,228),(161,194),(194,199),(194,256),(150,277),(107,257),(107,77)]
# rasio15/01: broad red diamond with navy tips and compact navy MCM.
f4=[(215,36),(422,136),(215,241),(9,136)]
t4=[(28,120),(195,10),(214,28)]
b4=[(29,153),(190,270),(214,248)]
m4=[(89,105),(110,105),(129,126),(151,104),(174,104),(174,175),(147,175),(147,142),(130,159),(112,142),(112,173),(89,173)]
c4=[(206,104),(232,104),(243,108),(250,116),(253,125),(253,135),(229,135),(229,127),(225,123),(211,123),(207,127),(207,155),(211,159),(225,159),(229,155),(229,149),(253,149),(253,159),(248,170),(240,175),(230,177),(206,177),(195,174),(187,167),(183,157),(183,128),(187,115),(195,107)]
# rasio15/02: two upward red arrows, navy side piers and navy MCM below.
a5=[(89,52),(158,9),(158,197),(128,197),(128,70),(89,95)]
s5=[(9,100),(37,82),(119,128),(119,177),(46,137),(46,197),(9,197)]
m5=[(9,214),(33,214),(59,238),(83,214),(109,214),(109,297),(82,297),(82,254),(59,275),(35,254),(35,297),(9,297)]
c5=[(148,214),(183,214),(196,218),(205,227),(210,238),(210,248),(181,248),(181,238),(177,234),(155,234),(151,238),(151,273),(155,277),(177,277),(181,273),(181,264),(210,264),(210,275),(205,287),(196,294),(184,297),(148,297),(135,293),(126,284),(122,271),(122,241),(126,227),(135,218)]
# rasio15/03: skewed red slab; positive white MCM follows rising capline.
f6=[(48,105),(381,35),(381,170),(16,241)]
t6=[(58,70),(386,9),(382,28),(49,96)]
b6=[(14,249),(378,179),(358,205),(9,270)]
m6=[(72,120),(98,115),(118,135),(137,109),(162,104),(162,186),(136,192),(136,147),(117,170),(98,152),(98,199),(72,205)]
c6=[(194,99),(232,93),(240,94),(247,99),(250,106),(250,119),(225,124),(225,114),(203,118),(200,122),(200,156),(203,159),(221,156),(225,152),(225,144),(250,139),(250,152),(246,164),(238,172),(226,176),(193,182),(184,181),(178,175),(175,165),(175,122),(178,111),(185,103)]
mr6=[(261,89),(286,85),(304,112),(323,79),(349,72),(349,157),(323,163),(323,117),(305,144),(286,126),(286,169),(261,174)]
# rasio15/04: six separated hexagon segments, navy MCM with rectangular C.
a7=[(187,9),(250,44),(250,79),(186,45),(122,79),(122,44)]
s7=[(9,105),(112,50),(112,84),(70,105)]
b7=[(9,212),(75,212),(112,232),(112,268)]
f7=[(122,238),(186,272),(250,238),(250,272),(186,307),(122,273)]
m7=[(9,116),(27,116),(66,149),(109,117),(124,117),(124,199),(96,199),(96,166),(66,187),(38,166),(38,199),(9,199)]
c7=[(150,117),(222,117),(237,133),(237,150),(209,150),(209,141),(164,141),(164,175),(209,175),(209,166),(237,166),(237,183),(222,199),(150,199),(135,184),(135,133)]
# rasio15/05: recessed middle rails with navy MCM.
t8=[(32,9),(151,9),(168,29),(199,29),(217,9),(336,9),(358,40),(225,40),(214,50),(154,50),(144,40),(9,40)]
b8=[(9,164),(151,164),(168,181),(199,181),(217,164),(358,164),(340,184),(221,184),(210,201),(157,201),(144,184),(26,184)]
m8=[(9,59),(39,59),(67,85),(96,58),(126,58),(126,152),(94,152),(94,105),(67,127),(40,105),(40,152),(9,152)]
c8=[(155,61),(216,61),(234,76),(234,95),(202,95),(202,87),(198,84),(173,84),(169,88),(169,123),(173,127),(198,127),(202,123),(202,117),(234,117),(234,135),(216,152),(155,152),(137,135),(137,78)]
# rasio15/06: perspective I-beam assembled from detached surfaces, navy MCM to right.
top9=[(43,53),(235,9),(284,17),(106,65)]
front9=[(108,71),(293,20),(293,40),(108,94)]
web9=[(35,57),(102,71),(102,94),(81,89),(80,158),(80,179),(18,158),(62,143),(62,83),(35,74)]
redweb9=[(86,95),(102,99),(102,171),(86,178)]
base9=[(86,185),(110,172),(191,198),(145,211)]
bluefoot9=[(9,164),(143,216),(143,251),(9,186)]
redfoot9=[(150,216),(199,201),(199,236),(150,249)]
m9=[(117,104),(137,104),(157,120),(186,91),(206,91),(206,176),(180,176),(180,135),(157,153),(139,138),(139,163),(117,158)]
c9=[(233,91),(267,91),(277,94),(283,101),(285,109),(285,126),(263,126),(263,106),(240,106),(238,110),(238,153),(241,157),(263,157),(263,144),(285,144),(285,161),(281,170),(274,175),(266,177),(233,177),(224,174),(218,167),(215,159),(215,109),(218,100),(224,94)]
mr9=[(292,91),(313,91),(333,120),(353,91),(373,91),(373,177),(350,177),(350,136),(333,157),(314,136),(314,177),(292,177)]
# rasio15/07: detached outer red triangle pieces and navy angular MCM.
t10=[(9,9),(70,9),(88,32),(23,32)]
s10=[(28,41),(118,41),(114,63),(79,63),(79,128)]
f10=[(143,143),(181,143),(204,168),(227,143),(267,143),(204,212)]
m10=[(86,70),(108,70),(123,86),(147,54),(167,54),(167,132),(143,132),(143,100),(126,121),(111,106),(111,132),(86,132)]
c10=[(186,54),(227,54),(240,66),(240,86),(218,86),(218,72),(197,72),(197,115),(218,115),(218,102),(240,102),(240,121),(227,133),(186,133),(175,121),(175,66)]
DATA={
(14,7):logo(361,271,layer(0,s1,mirror(s1,180.5)),layer(1,t1,m1,[(x+138,y) for x,y in m1],c1)),
(14,8):logo(382,256,layer(0,t2,b2,hole(113,34,9),hole(270,34,9),hole(110,222,9),hole(273,222,9)),layer(1,m2,mirror(m2,191),c2)),
(14,9):logo(300,334,layer(0,t3,b3),layer(1,m3,mirror(m3,150),c3)),
(15,1):logo(430,278,layer(1,t4,mirror(t4,215),b4,mirror(b4,215)),layer(0,f4),layer(1,m4,[(x+173,y) for x,y in m4],c4)),
(15,2):logo(324,305,layer(0,a5,mirror(a5,162)),layer(1,s5,mirror(s5,162),m5,[(x+212,y) for x,y in m5],c5)),
(15,3):logo(394,279,layer(1,t6,b6),layer(0,f6),layer(2,m6,mr6,c6)),
(15,4):logo(372,316,layer(0,a7,b7,mirror(b7,186)),layer(1,s7,mirror(s7,186),f7,m7,mirror(m7,186),c7)),
(15,5):logo(368,210,layer(0,t8),layer(1,b8,m8,mirror(m8,184),c8)),
(15,6):logo(382,260,layer(0,top9,front9,redweb9,base9,redfoot9),layer(1,web9,bluefoot9,m9,c9,mr9)),
(15,7):logo(413,220,layer(0,t10,mirror(t10,206.5),s10,mirror(s10,206.5),f10),layer(1,m10,mirror(m10,206.5),c10))}
VALUES=['14-G3H6Wsc9IpP7mkksqOWhpFOSgKMlHY','1dJfyEqxqJo4Sc1wfD7ttOKsImNCQdZhP','1bPRatIvT88fomQXOHu6dtUWdgwUqXHip','13uVI4MP47HyMdwE0ZGGs53PB34fqdRLy','1ROE2IoOtHLIiEINWIH8-FE-4OCA9vASw','10jpeM3P6flHrmjyZQLaHzMCzLjcNPSXw','1cW0UB2TeNGQsNTiSIrXXvG_PgeG7osMb','1xORNw-vJJPx_3HO9Rfn_nGl0vXNDVa6i','17xnrid8PpjTtx6Fdt57BW4GDYx2nlHms','1UL1aFMR-hrTSAoAynYChkJOUmpNhAlSB']
if __name__=='__main__':
    old=json.loads((R/'04-desain/variasi-svg/batch-19/progress.json').read_text())
    groups=old['groups'];groups['rasio-14']=dict(redrawn=list(range(1,10)),pending=[]);groups['rasio-15']=dict(redrawn=list(range(1,8)),pending=[8,9])
    names={k:f'Max_a_Gambar_kotak_rasio_1_{k[0]}_logo-{k[1]:02}.png' for k in DATA}
    seen={e['sourceSha256'] for p in (R/'04-desain/variasi-svg').glob('batch-*/progress.json') if p.parent.name!='batch-20' for e in json.loads(p.read_text())['entries']}
    for name in names.values():
        digest=hashlib.sha256((R/'google_drive'/name).read_bytes()).hexdigest()
        assert digest not in seen, f'Duplicate source requires alias audit: {name}'
        seen.add(digest)
    export_batch('20',DATA,dict(zip(DATA,VALUES)),169,groups,source_names=names,entry_ids={k:f'exp-rasio-{k[0]:03}-{k[1]:02}' for k in DATA})
    out=R/'04-desain/variasi-svg/batch-20';p=json.loads((out/'progress.json').read_text())
    p.update(uniqueDriveMasters=169,driveSourcesCoveredIncludingDuplicates=187,remainingNotProcessed=155,progressPercent=round(187/342*100,2),redrawOnlyPercent=round(169/342*100,2),progressBasis='169 manual masters + 18 verified duplicate source files / 342 reported files',sourceAliases=old['sourceAliases'],buildPolicy='Redraw only; all APK jobs paused; Android catalog unchanged.')
    for e in p['entries']:e.update(sourceFamily='rasio_1',appIntegration='deferred-no-apk-requested')
    (out/'progress.json').write_text(json.dumps(p,indent=2))
    page=(out/'perbandingan.html').read_text().replace('169 dari 342 sumber','169 master unik; 187 dari 342 sumber tercakup').replace('<strong>173</strong>','<strong>155</strong>').replace('49.42%','54.68%').replace('Kelompok 14 ·','Keluarga rasio_1 · Kelompok 14 ·').replace('Kelompok 15 ·','Keluarga rasio_1 · Kelompok 15 ·')
    page=page.replace('</main>','<h2>Audit terbatas</h2><p>169 master unik + 18 alias = 187/342 (54,68%), sisa 155. Redraw unik saja: 169/342 (49,42%). Sepuluh hash baru berbeda satu sama lain dan dari sumber master terdahulu. 342 bukan jumlah desain unik terverifikasi. Lubang nameplate 14/08 mengikuti latar. Tidak ada build APK atau perubahan katalog aplikasi.</p></main>')
    (out/'perbandingan.html').write_text(page)
