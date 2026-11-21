"""Ten hand-measured source-specific polygon redraws; no tracing or APK."""
from build_drive_batch_03 import layer,mirror,logo
from design_batch_io import export_batch
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1]
# 12/03 downward red chevron, four separate navy piers and compact initials.
t1=[(47,9),(161,84),(278,9),(278,58),(160,147),(47,58)]
s1=[(9,79),(39,59),(39,187),(9,198)]
u1=[(47,69),(85,97),(85,173),(47,186)]
m1=[(16,203),(42,203),(63,223),(85,203),(113,203),(113,276),(84,276),(84,242),(64,261),(45,243),(45,276),(16,276)]
c1=[(139,203),(187,203),(196,206),(202,213),(205,222),(205,232),(175,232),(175,225),(171,222),(155,222),(151,225),(151,256),(155,259),(171,259),(175,256),(175,249),(205,249),(205,259),(202,268),(196,274),(187,276),(139,276),(130,273),(124,267),(121,259),(121,221),(124,212),(130,206)]
# 12/04 red flags and angular oblique MCM.
t2=[(82,9),(399,9),(382,36),(80,36),(59,46)]
b2=[(28,157),(333,157),(353,142),(326,182),(9,182)]
m2=[(17,147),(65,51),(96,51),(103,79),(138,51),(174,51),(129,142),(100,142),(123,94),(86,122),(76,95),(51,143)]
mr2=[(228,142),(272,51),(302,51),(309,79),(343,51),(378,51),(334,142),(305,142),(328,94),(291,122),(281,95),(258,142)]
c2=[(191,51),(263,51),(249,77),(201,77),(183,116),(231,116),(218,142),(139,142),(180,62),(184,56)]
# 12/05 split navy roof above two red roof slivers, long red rectangular C.
t3=[(32,82),(185,9),(185,33),(32,105)]
r3=[(16,120),(185,40),(185,61),(16,126)]
m3=[(16,135),(49,124),(65,149),(89,107),(122,95),(122,232),(90,232),(90,158),(65,198),(48,176),(48,232),(16,232)]
c3=[(133,94),(185,71),(238,94),(238,146),(199,146),(199,114),(169,114),(169,202),(199,202),(199,173),(238,173),(238,232),(133,232)]
b3=[(9,239),(362,239),(362,256),(9,256)]
# 12/06 two interrupted navy frame pieces, red slash inserts.
t4=[(9,9),(209,9),(186,31),(30,31),(30,154),(112,154),(88,178),(9,178)]
b4=[(296,9),(374,9),(374,178),(166,178),(190,154),(352,154),(352,31),(272,31)]
r4=[(222,9),(282,9),(255,36),(195,36)]
s4=[(128,154),(179,154),(153,178),(102,178)]
m4=[(43,52),(71,52),(92,74),(114,52),(144,52),(144,138),(114,138),(114,96),(92,118),(72,97),(72,138),(43,138)]
c4=[(167,51),(212,51),(221,54),(228,61),(231,70),(231,85),(202,85),(202,77),(198,73),(183,73),(179,77),(179,112),(183,116),(198,116),(202,112),(202,105),(231,105),(231,120),(228,129),(221,135),(212,138),(167,138),(159,135),(153,129),(150,120),(150,69),(153,60),(160,54)]
# 12/07 descending red keel, six short wing bars and navy tall Ms.
t5=[(9,30),(68,30),(68,48),(23,48)]
u5=[(28,55),(68,55),(68,73),(42,73)]
b5=[(46,81),(68,81),(211,134),(354,81),(376,81),(363,101),(211,160),(59,101)]
m5=[(80,5),(105,5),(124,26),(144,4),(168,4),(168,110),(142,101),(142,46),(124,65),(106,46),(106,89),(80,80)]
c5=[(191,3),(230,3),(239,6),(245,13),(248,22),(248,39),(222,39),(222,29),(219,25),(204,25),(200,29),(200,70),(204,74),(219,74),(222,70),(222,58),(248,58),(248,75),(245,85),(239,92),(230,95),(191,95),(183,92),(177,85),(174,76),(174,22),(177,13),(183,6)]
# 12/08 red hexagon ring, tall angular red C and navy Ms.
o6=[(9,86),(159,9),(309,87),(309,242),(159,319),(9,242)]
i6=[(29,97),(159,32),(290,98),(290,230),(159,296),(29,230)]
m6=[(38,106),(63,94),(73,125),(84,83),(114,70),(114,259),(88,247),(88,157),(74,191),(61,157),(61,234),(38,222)]
c6=[(124,68),(159,49),(194,68),(194,127),(165,127),(165,89),(150,89),(150,234),(165,234),(165,199),(194,199),(194,258),(159,276),(124,258)]
# 12/09 four independent top flags, two base flags, slanted navy initials.
t7=[(130,10),(287,10),(263,34),(110,34)]
u7=[(107,41),(259,41),(250,50),(98,50)]
v7=[(300,10),(423,10),(393,50),(264,50)]
b7=[(35,149),(181,149),(152,185),(9,185)]
w7=[(191,149),(333,149),(310,185),(163,185)]
m7=[(38,141),(93,59),(117,59),(124,83),(155,59),(194,59),(150,141),(119,141),(144,96),(110,119),(101,97),(75,141)]
mr7=[(238,141),(283,60),(310,60),(318,83),(348,60),(387,60),(343,141),(310,141),(335,97),(301,120),(291,98),(271,141)]
c7=[(211,60),(275,60),(263,83),(218,83),(201,116),(243,116),(230,141),(157,141),(199,68),(204,62)]
# 13/01 four navy tips, positive white initials on red diamond.
d8=[(9,123),(208,30),(406,123),(208,226)]
t8=[(12,116),(187,10),(207,28)]
u8=[(212,28),(232,9),(403,115)]
b8=[(12,129),(206,230),(182,245)]
v8=[(212,230),(403,129),(234,245)]
m8=[(84,96),(107,96),(123,115),(141,96),(163,96),(163,163),(139,163),(139,130),(123,147),(108,130),(108,160),(84,160)]
c8=[(191,96),(224,96),(233,99),(240,105),(242,112),(242,121),(217,121),(217,113),(214,110),(203,110),(200,114),(200,145),(203,149),(214,149),(217,145),(217,138),(242,138),(242,148),(239,156),(233,161),(225,163),(191,163),(183,160),(177,155),(174,148),(174,112),(177,104),(183,98)]
# 13/02 shallow red roof, navy keel and red broad C.
t9=[(9,80),(190,9),(372,79),(372,102),(190,42),(9,103)]
b9=[(9,199),(190,258),(372,199),(372,232),(190,291),(9,232)]
m9=[(9,115),(41,104),(63,127),(97,88),(130,83),(130,222),(91,209),(91,147),(64,172),(42,151),(42,198),(9,187)]
c9=[(155,83),(230,83),(238,86),(243,93),(243,130),(207,130),(207,115),(174,115),(174,189),(207,189),(207,170),(243,170),(243,207),(240,214),(234,219),(226,221),(155,221),(147,218),(142,212),(140,204),(140,100),(143,92),(148,86)]
# 13/03 red folded top, two navy side piers and central navy chevron.
t10=[(50,36),(93,9),(174,60),(257,9),(298,35),(174,111)]
s10=[(49,49),(90,74),(90,203),(49,178)]
f10=[(102,83),(174,125),(246,83),(246,130),(174,174),(102,131)]
m10=[(9,215),(40,215),(65,243),(90,215),(122,215),(122,292),(90,292),(90,255),(65,278),(40,255),(40,292),(9,292)]
c10=[(151,215),(197,215),(207,219),(213,226),(217,235),(217,247),(186,247),(186,238),(162,238),(162,270),(186,270),(186,261),(217,261),(217,275),(212,283),(205,289),(197,292),(151,292),(143,289),(136,283),(133,275),(133,233),(136,225),(143,218)]
DATA={
(12,3):logo(324,284,layer(0,t1),layer(1,s1,u1,mirror(s1,162),mirror(u1,162),m1,[(x+197,y) for x,y in m1],c1)),
(12,4):logo(408,191,layer(0,t2,b2),layer(1,m2,mr2,c2)),
(12,5):logo(371,265,layer(1,t3,[(190,9),(341,82),(341,105),(190,33)],m3,mirror(m3,185.5)),layer(0,r3,[(190,40),(355,120),(355,126),(190,61)],c3,b3)),
(12,6):logo(383,187,layer(1,t4,b4,m4,[(x+194,y) for x,y in m4],c4),layer(0,r4,s4)),
(12,7):logo(422,169,layer(0,t5,u5,mirror(t5,211),mirror(u5,211),b5),layer(1,m5,mirror(m5,211),c5)),
(12,8):logo(318,328,layer(0,o6,i6,c6),layer(1,m6,mirror(m6,159.5))),
(12,9):logo(431,194,layer(0,t7,v7,b7),layer(1,u7,w7,m7,mr7,c7)),
(13,1):logo(415,253,layer(1,t8,u8,b8,v8),layer(0,d8),layer(2,m8,[(x+168,y) for x,y in m8],c8)),
(13,2):logo(381,299,layer(0,t9,c9),layer(1,b9,m9,mirror(m9,190.5))),
(13,3):logo(348,301,layer(0,t10),layer(1,s10,mirror(s10,174.5),f10,m10,[(x+217,y) for x,y in m10],c10))}
VALUES=['1J82ZEWeJScHx6IDKYioxNtgYKjNNOiSJ','1uN8VqVlrTLJOJfltvPDgUhd8hDRsF8eW','1T3t0fFRkj5Lso2TnVpliNbaB7Lsbyjvv','1mgSJPNSnrP0Vv_atqs9YapXKVptMQDJ4','1zG1EZsff00gC-t_ERHnHCUNKTOP43GI8','1vlIkOtfHVGODjukyc6P3zfS8BXaREHqo','1Tp2IjZ7shZ6ZwKsgFM0MIv2pz_a_aW-U','1PN6yNfiCHY_Dg81vs1fT7Jn_Xwdz_f5e','1pT-o7j2pzeTxTcXOB4Ja1N9TMiti6FLG','1L61gZJMMyQLdQekJcBaq5wmlbia02Jm3']
if __name__=='__main__':
    old=json.loads((R/'04-desain/variasi-svg/batch-33/progress.json').read_text())
    groups=old['groups'];groups['rasio-12']=dict(redrawn=list(range(1,10)),pending=[]);groups['rasio-13']=dict(redrawn=[1,2,3],pending=list(range(4,10)))
    names={k:f'Max_a_Gambar_kotak_rasio_1_{k[0]}_logo-{k[1]:02}.png' for k in DATA}
    seen={e['sourceSha256'] for p in (R/'04-desain/variasi-svg').glob('batch-*/progress.json') if p.parent.name!='batch-34' for e in json.loads(p.read_text())['entries']}
    for name in names.values():
        digest=hashlib.sha256((R/'google_drive'/name).read_bytes()).hexdigest()
        assert digest not in seen, f'Duplicate source requires alias audit: {name}'
        seen.add(digest)
    export_batch('34',DATA,dict(zip(DATA,VALUES)),309,groups,source_names=names,entry_ids={k:f'exp-rasio-{k[0]:03}-{k[1]:02}' for k in DATA})
    out=R/'04-desain/variasi-svg/batch-34';p=json.loads((out/'progress.json').read_text())
    p.update(uniqueDriveMasters=309,driveSourcesCoveredIncludingDuplicates=327,remainingNotProcessed=15,progressPercent=round(327/342*100,2),redrawOnlyPercent=round(309/342*100,2),progressBasis='309 manual masters + 18 verified duplicate source files / 342 reported files',sourceAliases=old['sourceAliases'],buildPolicy='Redraw only; all APK jobs paused; Android catalog unchanged.')
    for e in p['entries']:e.update(sourceFamily='rasio_1',appIntegration='deferred-no-apk-requested')
    (out/'progress.json').write_text(json.dumps(p,indent=2))
    page=(out/'perbandingan.html').read_text().replace('309 dari 342 sumber','309 master unik; 327 dari 342 sumber tercakup').replace('<strong>33</strong>','<strong>15</strong>').replace('90.35%','95.61%').replace('Kelompok 13 ·','Keluarga rasio_1 · Kelompok 13 ·').replace('Kelompok 12 ·','Keluarga rasio_1 · Kelompok 12 ·')
    page=page.replace('</main>','<h2>Audit terbatas</h2><p>309 master unik + 18 alias = 327/342 (95,61%), sisa 15. Redraw unik saja: 309/342 (90,35%). Sepuluh hash baru berbeda satu sama lain dan dari sumber master terdahulu. 342 bukan jumlah desain unik terverifikasi. MCM putih 13/01 adalah bidang positif recolorable; frame hexagon 12/08 berlubang evenodd; C merahnya bidang positif terpisah. Celah antarkomponen transparan. Tidak ada build APK atau perubahan katalog aplikasi.</p></main>')
    (out/'perbandingan.html').write_text(page)
