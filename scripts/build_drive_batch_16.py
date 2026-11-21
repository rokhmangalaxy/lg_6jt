"""Ten individually measured polygon reconstructions; design-only, no auto-trace."""
from build_drive_batch_03 import layer,mirror,logo
from design_batch_io import export_batch
from pathlib import Path
import json
R=Path(__file__).resolve().parents[1]
# 16/01: four split navy diamond tips; red field and positive white letters.
f1=[(245,38),(482,134),(245,228),(8,134)]
t1=[(28,118),(240,9),(240,33)]
b1=[(28,150),(240,234),(240,258)]
m1=[(106,98),(135,98),(152,134),(170,98),(199,98),(200,171),(177,171),(177,135),(158,171),(146,171),(128,135),(128,171),(105,171)]
c1=[(236,96),(259,96),(271,99),(279,106),(284,117),(285,128),(260,128),(258,121),(252,117),(245,117),(239,121),(237,129),(237,144),(240,151),(247,153),(254,151),(259,143),(285,143),(282,157),(276,167),(266,172),(249,174),(233,173),(221,169),(214,162),(211,151),(210,125),(213,112),(222,102)]
# 16/02: open slanted-tip red C; asymmetric shoulder segments regularized symmetrically.
m2=[(9,110),(45,91),(77,124),(104,63),(148,34),(148,243),(108,219),(107,133),(78,183),(49,152),(49,218),(9,218)]
c2=[(220,6),(286,49),(286,116),(246,102),(246,79),(220,60),(193,80),(193,186),(220,205),(246,186),(246,163),(286,177),(286,215),(220,258),(154,215),(154,49)]
# 16/03: red roof/foot with short flat ends; low horizontal navy MCM.
roof3=[(211,9),(414,93),(325,93),(211,48),(98,93),(9,93)]
foot3=[(9,209),(98,209),(211,252),(325,209),(414,209),(211,287)]
m3=[(9,100),(56,100),(80,149),(112,100),(152,100),(152,202),(116,202),(116,149),(88,202),(72,202),(45,147),(45,202),(9,202)]
c3=[(181,100),(251,99),(269,118),(269,142),(232,142),(232,132),(195,132),(195,174),(232,174),(232,163),(269,163),(269,183),(249,202),(179,202),(160,184),(160,119)]
# 16/04: right-leaning independent MCM; red horizontal cap and foot.
roof4=[(175,9),(467,9),(455,42),(133,42)]
foot4=[(28,169),(398,169),(321,207),(9,207)]
m4=[(33,156),(84,56),(123,56),(120,101),(167,56),(214,56),(168,156),(129,156),(151,111),(106,156),(94,156),(91,110),(71,156)]
c4=[(239,56),(313,56),(299,86),(246,86),(226,128),(279,128),(266,156),(196,156),(185,143),(216,71)]
mr4=[(278,156),(325,56),(366,56),(363,100),(405,56),(450,56),(404,156),(367,156),(388,111),(348,156),(336,156),(333,111),(313,156)]
# 16/05: separated navy hex rails; red top/bottom/side fields, NOT a red rectangle behind letters.
roof5=[(205,7),(400,84),(400,98),(205,21),(9,98),(9,84)]
foot5=[(9,208),(205,282),(400,208),(400,222),(205,296),(9,222)]
redtop5=[(205,29),(381,95),(29,95)]
redfoot5=[(29,209),(381,209),(205,275)]
side5=[(9,104),(28,97),(28,207),(9,201)]
m5=[(47,107),(80,107),(96,145),(113,107),(147,107),(147,201),(116,201),(116,158),(96,195),(76,158),(76,201),(47,201)]
c5=[(178,107),(236,107),(249,122),(249,146),(217,146),(217,136),(212,133),(197,133),(192,136),(192,175),(217,175),(217,164),(249,164),(249,185),(233,201),(177,201),(161,186),(161,121)]
# 16/06: red central C and detached cap/foot; four navy bars around Ms.
roof6=[(227,9),(303,49),(303,74),(227,37),(151,74),(151,49)]
foot6=[(151,176),(227,213),(303,176),(303,201),(227,240),(151,201)]
bar6=[(17,74),(54,49),(143,49),(143,73)]
low6=[(9,177),(143,177),(143,202),(43,202)]
m6=[(34,82),(80,82),(106,118),(132,82),(169,82),(169,170),(135,170),(135,131),(105,165),(73,131),(73,170),(34,170)]
c6=[(227,59),(274,84),(274,114),(238,114),(238,102),(227,96),(215,103),(215,144),(227,151),(238,144),(238,130),(274,130),(274,168),(227,193),(179,168),(179,84)]
# 16/07: red C is drawn on three folded facets with thin transparent joins.
outer7=[(9,67),(46,98),(46,199),(9,178)]
inner7=[(49,102),(70,115),(96,81),(96,135),(71,164),(49,144)]
post7=[(98,79),(104,65),(142,43),(142,204),(98,181)]
ct7=[(148,49),(225,9),(300,48),(257,71),(225,52),(189,73)]
cl7=[(148,53),(188,77),(188,172),(148,195)]
cb7=[(148,199),(188,176),(225,195),(257,176),(300,198),(225,237)]
cu7=[(257,75),(300,52),(300,86),(257,108)]
cd7=[(257,143),(300,165),(300,194),(257,172)]
# 16/08: red detached triangles above/below; two-piece navy rails and navy MCM.
roof8=[(222,7),(337,62),(109,62)]
foot8=[(123,204),(320,204),(222,269)]
bar8=[(9,84),(36,67),(197,67),(169,84)]
low8=[(10,194),(104,194),(125,211),(37,211)]
m8=[(30,93),(71,93),(96,131),(122,93),(159,93),(159,186),(124,186),(124,146),(95,183),(65,145),(65,186),(30,186)]
c8=[(192,93),(266,93),(280,108),(280,132),(243,132),(243,122),(207,122),(207,161),(243,161),(243,151),(280,151),(280,170),(262,186),(191,186),(173,171),(173,110)]
# 16/09: navy slanted field with positive white, individually slanted MCM shapes.
roof9=[(169,9),(470,9),(453,42),(119,42)]
foot9=[(42,183),(385,183),(325,222),(9,222)]
field9=[(93,52),(450,52),(391,174),(9,174)]
m9=[(45,159),(96,71),(129,71),(129,108),(168,70),(209,70),(166,159),(134,159),(155,115),(111,159),(103,159),(101,113),(74,159)]
c9=[(243,70),(298,70),(287,95),(242,95),(222,135),(271,135),(260,159),(200,159),(190,154),(186,146),(189,133),(211,90),(219,79),(229,73)]
mr9=[(272,159),(312,70),(345,70),(347,107),(382,70),(419,70),(378,159),(347,159),(368,116),(329,158),(320,115),(302,159)]
# rasio 14/03: red downward chevron and detached tall navy posts, navy horizontal MCM.
roof10=[(9,10),(164,87),(319,10),(319,57),(164,136),(9,58)]
post10=[(9,65),(53,87),(53,230),(9,254)]
m10=[(64,146),(84,146),(98,171),(112,146),(130,146),(130,223),(112,223),(112,182),(98,206),(81,181),(81,223),(64,223)]
c10=[(153,146),(178,146),(187,149),(192,157),(193,177),(174,177),(174,167),(171,164),(162,164),(157,168),(157,207),(161,210),(171,210),(174,206),(174,196),(193,196),(193,216),(187,223),(178,226),(153,226),(143,223),(137,216),(137,158),(142,150)]
DATA={
(16,1):logo(490,266,layer(1,t1,mirror(t1,245),b1,mirror(b1,245)),layer(0,f1),layer(2,m1,[(x+190,y) for x,y in m1],c1)),
(16,2):logo(440,264,layer(1,m2,mirror(m2,220)),layer(0,c2)),
(16,3):logo(421,296,layer(0,roof3,foot3),layer(1,m3,[(x+269,y) for x,y in m3],c3)),
(16,4):logo(476,215,layer(0,roof4,foot4),layer(1,m4,c4,mr4)),
(16,5):logo(409,303,layer(1,roof5,foot5),layer(0,redtop5,redfoot5,side5,mirror(side5,204.5)),layer(1,m5,[(x+216,y) for x,y in m5],c5)),
(16,6):logo(454,249,layer(0,roof6,foot6,c6),layer(1,bar6,mirror(bar6,227),low6,mirror(low6,227),m6,[(x+251,y) for x,y in m6])),
(16,7):logo(450,245,layer(1,outer7,inner7,post7,mirror(outer7,225),mirror(inner7,225),mirror(post7,225)),layer(0,ct7,cl7,cb7,cu7,cd7)),
(16,8):logo(444,274,layer(0,roof8,foot8),layer(1,bar8,mirror(bar8,222),low8,mirror(low8,222),m8,[(x+259,y) for x,y in m8],c8)),
(16,9):logo(479,231,layer(0,roof9,foot9),layer(1,field9),layer(2,m9,c9,mr9)),
(14,3):logo(328,264,layer(0,roof10),layer(1,post10,mirror(post10,164),m10,[(x+134,y) for x,y in m10],c10))}
IDS={(16,n):v for n,v in enumerate(['1SgEUdBbQVDcWZi26bZhJOexXIf0iv13L','1GrK7vTYFz6l8oZEQZ5EDx8HoAQgg8BeU','1cLDbeYN4o40vjigk15ucmx718p58v9qC','1DTjHFFOdIAN3ZXTI6oZ_Lp2D07R1zBKf','1uy-78vtl09atK1I0O5P_VEHUZ4Wm_BbZ','1TOK9xUyXd22tr4z0S3vg6dg58gBaXPyJ','1f0stcgDYFRTbLD1qjqnnUGaUhDn-QxBq','1UaFhym6DhLTB0L2oxFhAoXOr_TrhV5Dk','1HQsPL8J-nYQsSvz2QmJa4tB9iSwCB8rI'],1)}
IDS[14,3]='1Uwh42PzP0kB7KJ4xPZEtjtDv0V1vjwIj'
if __name__=='__main__':
    previous=json.loads((R/'04-desain/variasi-svg/batch-15/progress.json').read_text())
    groups=previous['groups'];groups['16']=dict(redrawn=list(range(1,10)),pending=[]);groups['rasio-14']=dict(redrawn=[1,2,3],pending=list(range(4,10)))
    export_batch('16',DATA,IDS,129,groups,source_names={(14,3):'Max_a_Gambar_kotak_rasio_1_14_logo-03.png'},entry_ids={(14,3):'exp-rasio-014-03'})
    out=R/'04-desain/variasi-svg/batch-16';p=json.loads((out/'progress.json').read_text())
    p.update(uniqueDriveMasters=129,driveSourcesCoveredIncludingDuplicates=147,remainingNotProcessed=195,progressPercent=round(147/342*100,2),redrawOnlyPercent=round(129/342*100,2),progressBasis='129 manual masters + 18 verified duplicate source files / 342 reported files',sourceAliases=previous['sourceAliases'],buildPolicy='Redraw only; all APK jobs paused; app catalog unchanged.')
    for e in p['entries']:
        e['sourceFamily']='rasio_1' if e['id'].startswith('exp-rasio-') else 'berisi'
        e['appIntegration']='deferred-no-apk-requested'
    (out/'progress.json').write_text(json.dumps(p,indent=2))
    page=(out/'perbandingan.html').read_text().replace('129 dari 342 sumber','129 master unik; 147 dari 342 sumber tercakup').replace('<strong>213</strong>','<strong>195</strong>').replace('37.72%','42.98%').replace('Kelompok 14 · Logo 03','Keluarga rasio_1 · Kelompok 14 · Logo 03')
    page=page.replace('</main>','<h2>Progres dan audit terbatas</h2><p>Sepuluh sumber baru tidak memiliki hash identik dengan sumber master sebelumnya. Motif serupa tidak otomatis digabung. Kumulatif 129 master unik + 18 alias terdahulu = 147/342 (42,98%), sisa 195. Redraw unik saja 129/342 (37,72%). 342 bukan jumlah desain unik terverifikasi; audit hanya PNG yang diunduh. Tidak ada build APK atau perubahan katalog aplikasi.</p></main>')
    (out/'perbandingan.html').write_text(page)
