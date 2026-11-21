"""Ten source-specific hand-measured polygon masters. No tracing or APK."""
from build_drive_batch_03 import layer,mirror,logo
from design_batch_io import export_batch
from pathlib import Path
import json,hashlib,math
R=Path(__file__).resolve().parents[1]
# 13/04 two detached red bent rails and chamfered navy initials.
t1=[(9,38),(42,10),(357,10),(387,38),(387,48),(361,48),(349,35),(50,35),(38,48),(9,48)]
b1=[(9,168),(38,168),(50,178),(347,178),(358,168),(387,168),(387,176),(354,203),(42,203),(9,176)]
m1=[(28,59),(57,59),(83,89),(107,59),(142,59),(142,157),(107,157),(107,106),(83,133),(61,106),(61,157),(28,157)]
c1=[(166,59),(231,59),(244,71),(244,97),(209,97),(209,83),(187,83),(187,132),(209,132),(209,118),(244,118),(244,144),(230,157),(166,157),(153,145),(153,71)]
# 13/05 outward pointing navy Ms, red block C and two red diagonal inserts.
m2=[(9,2),(67,44),(110,2),(133,2),(133,36),(70,91),(40,70),(40,108),(9,135)]
c2=[(167,2),(225,2),(244,20),(244,33),(174,33),(174,87),(244,87),(244,98),(224,118),(162,118),(143,99),(143,23)]
s2=[(97,84),(133,50),(133,98),(97,124)]
# 13/06 tilted bars and individually oblique initials.
t3=[(39,88),(376,9),(360,40),(18,116)]
b3=[(33,234),(380,162),(362,192),(10,265)]
m3=[(10,225),(25,127),(60,120),(79,149),(112,109),(148,102),(133,198),(98,206),(105,161),(75,196),(53,170),(46,216)]
mr3=[(247,176),(263,79),(299,72),(313,104),(348,63),(383,55),(367,152),(330,159),(338,110),(308,149),(287,124),(280,169)]
c3=[(174,97),(239,84),(251,94),(247,114),(212,122),(213,114),(188,119),(180,163),(207,157),(209,147),(243,140),(240,165),(224,181),(158,194),(145,184),(156,112)]
# 13/07 tall red hexagonal C and swept navy Ms.
m4=[(9,86),(54,120),(65,82),(113,49),(113,267),(81,246),(81,126),(60,168),(37,151),(37,221),(9,203)]
c4=[(124,39),(178,9),(231,38),(231,101),(190,101),(190,58),(165,61),(165,255),(190,255),(190,198),(231,198),(231,274),(177,305),(124,276)]
# 13/08 plate rails with four transparent mounting holes.
t5=[(9,53),(61,9),(321,9),(372,53)]
b5=[(9,180),(372,180),(321,222),(61,222)]
def hole(x,y):
    # Regular 16-sided approximation to the small round source hole.
    return [(round(x+7.5*math.cos(i*math.pi/8),2),round(y+7.5*math.sin(i*math.pi/8),2)) for i in range(16)]
m5=[(9,70),(45,70),(70,97),(96,70),(132,70),(132,166),(96,166),(96,115),(70,141),(44,115),(44,166),(9,166)]
c5=[(156,70),(225,70),(237,81),(237,108),(201,108),(201,97),(176,97),(175,137),(178,140),(198,140),(201,137),(201,128),(237,128),(237,154),(225,166),(155,166),(142,156),(142,82)]
# 13/09 detached red hexagonal caps, navy tall C and tapered Ms.
t6=[(34,94),(176,9),(307,94),(267,94),(174,44),(80,94)]
b6=[(31,224),(78,224),(173,282),(268,224),(310,224),(174,316)]
m6=[(9,113),(54,139),(80,108),(113,95),(113,229),(80,210),(80,155),(58,178),(41,166),(41,206),(9,206)]
c6=[(134,105),(213,105),(222,112),(222,151),(188,151),(188,135),(159,135),(159,192),(188,192),(188,177),(222,177),(222,212),(214,220),(134,220),(126,213),(126,112)]
# Unnumbered rasio_1/01: continuous navy cap/base, positive white MCM.
t7=[(38,130),(226,9),(416,130),(226,48)]
b7=[(45,198),(225,280),(411,198),(225,318)]
d7=[(9,162),(226,59),(446,162),(226,269)]
m7=[(85,127),(90,123),(107,120),(131,149),(156,120),(180,120),(180,207),(152,207),(152,163),(131,186),(111,164),(111,207),(85,207)]
c7=[(211,120),(246,120),(256,123),(263,130),(266,139),(266,154),(239,154),(239,146),(235,142),(220,142),(216,146),(216,183),(220,187),(235,187),(239,183),(239,177),(266,177),(266,191),(263,200),(255,206),(245,209),(211,209),(201,206),(193,200),(189,191),(189,139),(193,131),(201,123)]
# Unnumbered /02 nested open-bottom navy and red M frames, small navy initials.
o8=[(9,9),(160,92),(311,9),(311,228),(282,247),(282,65),(160,130),(39,65),(39,247),(9,228)]
i8=[(48,80),(160,142),(272,80),(272,254),(250,273),(250,132),(160,180),(70,132),(70,273),(48,254)]
m8=[(82,192),(95,192),(107,213),(120,192),(134,192),(134,256),(119,256),(119,226),(107,243),(96,227),(96,256),(82,256)]
c8=[(148,192),(169,192),(176,198),(180,205),(180,216),(166,216),(166,211),(163,208),(156,208),(153,211),(153,238),(156,241),(163,241),(166,238),(166,232),(180,232),(180,244),(176,251),(170,256),(148,256),(142,251),(139,244),(139,204),(143,197)]
# Unnumbered /03 shallow red cap/base and separate triangular fills.
t9=[(10,77),(187,9),(365,77),(365,94),(187,48),(10,94)]
u9=[(41,94),(187,61),(334,94)]
b9=[(10,224),(187,270),(365,224),(365,242),(187,307),(10,242)]
v9=[(42,224),(333,224),(187,257)]
m9=[(9,109),(38,109),(68,145),(98,109),(129,109),(129,212),(95,212),(95,163),(68,189),(41,163),(41,212),(9,212)]
c9=[(158,109),(216,109),(233,125),(233,150),(201,150),(201,140),(197,136),(178,136),(174,140),(174,182),(178,186),(197,186),(201,182),(201,175),(234,175),(234,197),(218,212),(157,212),(147,206),(140,197),(139,128),(147,118)]
# Unnumbered /04 oblique navy initials and plain detached red bars.
t10=[(131,6),(385,6),(355,33),(102,33)]
b10=[(41,162),(297,162),(266,187),(14,187)]
m10=[(9,149),(54,48),(84,48),(92,78),(130,47),(166,47),(122,148),(88,148),(109,99),(76,122),(65,98),(42,149)]
mr10=[(233,148),(276,47),(308,47),(316,78),(354,47),(390,47),(346,148),(311,148),(333,99),(299,122),(288,98),(266,148)]
c10=[(189,47),(249,47),(259,61),(248,86),(216,86),(220,77),(217,73),(200,73),(196,77),(178,117),(181,121),(199,121),(205,108),(240,108),(231,132),(210,147),(150,147),(141,133),(169,63)]
DATA={
(13,4):logo(396,212,layer(0,t1,b1),layer(1,m1,[(x+226,y) for x,y in m1],c1)),
(13,5):logo(385,144,layer(0,c2,s2,mirror(s2,192)),layer(1,m2,mirror(m2,192.5))),
(13,6):logo(392,273,layer(0,t3,b3),layer(1,m3,mr3,c3)),
(13,7):logo(357,314,layer(0,c4),layer(1,m4,mirror(m4,178.5))),
(13,8):logo(381,231,layer(1,t5,hole(73,33),hole(309,33),b5,hole(73,201),hole(309,201)),layer(0,m5,[(x+238,y) for x,y in m5],c5)),
(13,9):logo(345,325,layer(0,t6,b6),layer(1,m6,mirror(m6,172.5),c6)),
(0,1):logo(455,327,layer(1,t7,b7),layer(0,d7),layer(2,m7,[(x+190,y) for x,y in m7],c7)),
(0,2):logo(321,282,layer(1,o8,m8,[(x+104,y) for x,y in m8],c8),layer(0,i8)),
(0,3):logo(374,316,layer(0,t9,u9,b9,v9),layer(1,m9,[(x+235,y) for x,y in m9],c9)),
(0,4):logo(399,191,layer(0,t10,b10),layer(1,m10,mr10,c10))}
VALUES=['1WjYUUvVGETVFEc1yaM1Z6RBKV6yfcxRZ','1lcpTuZwAn-jpiAKA7dUn1v7lRMSQzBt0','1V-tE7604a7TNoTk_w0dMxcjBtXL_4jAy','1mJUNHRRyZI-UcZskBSePGPes-sy5Rafa','1Ujm4-P1C48kk3zVCXkJSwnMYE2g_S8Pr','1z3EQxzLummrwu9H8z6HPv9ZVRoE-fXfV','1epOJSbHnP8BkGZxiWlZKn9O7_LAiQYwK','1MdwywPoacl0zATReeZ9-ZLl7fBqUh1gj','14sr-fC6D-ItN4Nvp39RfMm9cMEylzcT5','14uRAWkFyIUstTS4XG6Pj8VKo1Qym19z6']
if __name__=='__main__':
    old=json.loads((R/'04-desain/variasi-svg/batch-34/progress.json').read_text())
    groups=old['groups'];groups['rasio-13']=dict(redrawn=list(range(1,10)),pending=[]);groups['rasio-unnumbered']=dict(redrawn=[1,2,3,4],pending=list(range(5,10)))
    names={k:(f'Max_a_Gambar_kotak_rasio_1_{k[0]}_logo-{k[1]:02}.png' if k[0] else f'Max_a_Gambar_kotak_rasio_1_logo-{k[1]:02}.png') for k in DATA}
    ids={k:(f'exp-rasio-{k[0]:03}-{k[1]:02}' if k[0] else f'exp-rasio-unnumbered-{k[1]:02}') for k in DATA}
    seen={e['sourceSha256'] for p in (R/'04-desain/variasi-svg').glob('batch-*/progress.json') if p.parent.name!='batch-35' for e in json.loads(p.read_text())['entries']}
    for name in names.values():
        digest=hashlib.sha256((R/'google_drive'/name).read_bytes()).hexdigest()
        assert digest not in seen, f'Duplicate source requires alias audit: {name}'
        seen.add(digest)
    export_batch('35',DATA,dict(zip(DATA,VALUES)),319,groups,source_names=names,entry_ids=ids)
    out=R/'04-desain/variasi-svg/batch-35';p=json.loads((out/'progress.json').read_text())
    p.update(uniqueDriveMasters=319,driveSourcesCoveredIncludingDuplicates=337,remainingNotProcessed=5,progressPercent=round(337/342*100,2),redrawOnlyPercent=round(319/342*100,2),progressBasis='319 manual masters + 18 verified duplicate source files / 342 reported files',sourceAliases=old['sourceAliases'],buildPolicy='Redraw only; all APK jobs paused; Android catalog unchanged.')
    for e in p['entries']:e.update(sourceFamily='rasio_1' if e['group'] else 'rasio_1_unnumbered',appIntegration='deferred-no-apk-requested')
    (out/'progress.json').write_text(json.dumps(p,indent=2))
    page=(out/'perbandingan.html').read_text().replace('319 dari 342 sumber','319 master unik; 337 dari 342 sumber tercakup').replace('<strong>23</strong>','<strong>5</strong>').replace('93.27%','98.54%').replace('Kelompok 13 ·','Keluarga rasio_1 · Kelompok 13 ·').replace('Kelompok 0 ·','Keluarga rasio_1 tanpa nomor tambahan ·')
    page=page.replace('</main>','<h2>Audit terbatas</h2><p>319 master unik + 18 alias = 337/342 (98,54%), sisa 5. Redraw unik saja: 319/342 (93,27%). Sepuluh hash baru berbeda satu sama lain dan dari sumber master terdahulu. 342 bukan total desain unik terverifikasi. Kelompok tanpa nomor tambahan dibedakan dari kelompok 1; group=0 hanya sentinel internal, bukan nama file sumber. Empat lubang mounting 13/08 transparan, bukan bidang putih; MCM putih rasio tanpa nomor/01 positif recolorable. Tidak ada build APK atau perubahan katalog aplikasi.</p></main>')
    (out/'perbandingan.html').write_text(page)
