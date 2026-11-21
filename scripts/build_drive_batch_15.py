"""10 source-specific manual polygon masters; audit berisi 14 aliases. No APK."""
from build_drive_batch_03 import layer,mirror,logo
from design_batch_io import export_batch
from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parents[1]
# 15/01: a solid red diamond, not the double-ring motif from group 13.
f1=[(189,9),(369,162),(189,316),(9,162)]
m1=[(58,144),(82,123),(98,149),(119,98),(139,80),(139,245),(119,227),(119,168),(99,207),(81,176),(81,206),(58,187)]
c1=[(189,50),(224,80),(224,140),(201,140),(201,94),(189,84),(177,94),(177,231),(189,242),(201,231),(201,190),(224,190),(224,246),(189,278),(154,246),(154,80)]
# 15/02: thick separated navy upper/lower hexagonal rails, navy Ms, red C.
cap2=[(149,9),(288,90),(288,115),(149,34),(10,115),(10,90)]
foot2=[(10,219),(149,295),(288,219),(288,244),(149,318),(10,244)]
m2=[(10,133),(40,115),(54,159),(74,100),(100,84),(100,254),(74,240),(74,177),(53,213),(32,179),(32,228),(10,215)]
c2=[(149,52),(187,78),(187,133),(160,133),(160,94),(149,86),(138,94),(138,239),(149,247),(160,239),(160,197),(187,197),(187,253),(149,277),(111,253),(111,78)]
# 15/03: entirely red letters; three distinct navy wing bars each side.
m3=[(94,110),(114,95),(128,122),(144,64),(166,41),(166,214),(145,198),(145,141),(131,175),(113,144),(113,176),(94,160)]
c3=[(203,9),(233,34),(233,92),(211,92),(211,47),(203,40),(195,47),(195,210),(203,217),(211,210),(211,151),(233,151),(233,219),(203,241),(174,219),(174,34)]
w3a=[(9,60),(103,60),(119,85),(29,90)]
w3b=[(32,100),(86,100),(86,127),(49,127)]
w3c=[(54,137),(86,137),(86,164),(113,189),(77,172)]
# 15/04: open-bottom navy roof over a red MCM, with slanted M feet.
roof4=[(165,9),(320,100),(320,132),(165,43),(10,132),(10,100)]
m4=[(10,146),(42,129),(59,161),(79,111),(113,91),(113,247),(87,232),(87,182),(60,213),(36,185),(36,212),(10,228)]
c4=[(165,60),(205,86),(205,138),(178,138),(178,102),(165,92),(152,102),(152,239),(165,249),(178,239),(178,190),(205,190),(205,253),(165,281),(125,253),(125,86)]
# 15/05: two horizontal navy rails, red block Ms and a red pointed C.
roof5=[(49,10),(312,10),(351,47),(314,47),(294,29),(67,29),(47,47),(10,47)]
base5=[(10,171),(47,171),(67,190),(294,190),(314,171),(351,171),(312,208),(49,208)]
m5=[(10,60),(45,60),(68,95),(94,60),(129,60),(129,158),(96,158),(96,111),(68,146),(42,112),(42,158),(10,158)]
c5=[(180,35),(221,61),(221,94),(192,94),(192,74),(180,66),(169,74),(169,143),(180,151),(192,143),(192,130),(221,130),(221,164),(180,190),(140,164),(140,61)]
# 15/06: no outer shield; C and Ms form a tall diamond, two navy sidebars.
m6=[(39,137),(61,120),(74,158),(90,91),(116,56),(116,335),(91,320),(91,218),(74,252),(60,216),(60,304),(39,289)]
c6=[(163,9),(198,37),(198,124),(176,124),(176,52),(163,42),(151,52),(151,308),(163,318),(176,308),(176,219),(198,219),(198,334),(163,357),(128,334),(128,37)]
bar6=[(10,171),(32,149),(32,299),(10,284)]
# 15/07: navy roof and detached side rails, narrow red slivers then red MCM.
roof7=[(161,9),(308,76),(277,93),(161,39),(44,93),(14,77)]
bar7=[(9,85),(38,102),(38,235),(9,219)]
m7=[(48,116),(54,113),(66,146),(86,96),(113,77),(113,272),(87,257),(87,169),(67,201),(55,169),(55,277),(48,273)]
c7=[(161,51),(198,74),(198,132),(171,132),(171,88),(161,80),(151,88),(151,267),(161,275),(171,267),(171,194),(198,194),(198,274),(161,297),(124,274),(124,74)]
# 15/08: four detached diamond-frame pieces, tall navy letters.
roof8=[(200,9),(281,66),(249,66),(200,40),(151,66),(120,66)]
foot8=[(120,248),(151,248),(200,276),(249,248),(281,248),(200,309)]
side8=[(10,156),(111,76),(146,76),(43,156),(143,237),(110,237)]
m8=[(80,143),(102,128),(115,151),(132,106),(157,87),(157,230),(132,213),(132,166),(113,195),(100,165),(100,195),(80,180)]
c8=[(200,56),(233,78),(233,128),(209,128),(209,88),(200,82),(192,88),(192,223),(200,230),(209,223),(209,185),(233,185),(233,237),(200,259),(167,237),(167,78)]
# 15/09: downward chevron frame and oblique red Ms; central C opens to the right.
frame9=[(9,9),(167,105),(325,9),(325,202),(264,245),(264,217),(296,194),(296,60),(167,139),(38,60),(38,194),(70,217),(70,245),(9,202)]
m9=[(48,81),(71,95),(89,140),(106,117),(126,129),(126,244),(104,227),(104,160),(87,181),(67,150),(67,204),(48,191)]
c9=[(136,135),(167,153),(198,135),(198,181),(175,195),(175,171),(167,176),(159,171),(159,244),(167,251),(175,244),(175,226),(198,213),(198,254),(167,288),(136,254)]
# rasio 14/02: red cap, navy base. Measured rounded C represented by short chamfers.
roof10=[(179,9),(342,78),(342,98),(179,49),(15,98),(15,78)]
foot10=[(15,204),(179,251),(342,204),(342,226),(179,294),(15,226)]
m10=[(9,104),(40,104),(64,135),(90,104),(121,104),(121,198),(89,198),(89,148),(64,175),(38,148),(38,197),(9,197)]
c10=[(158,102),(201,102),(214,105),(224,113),(229,126),(229,141),(196,141),(196,132),(192,126),(170,126),(165,130),(164,139),(164,170),(168,177),(191,177),(196,172),(196,163),(229,163),(229,177),(225,190),(215,198),(202,201),(156,201),(143,197),(135,188),(131,175),(130,129),(133,117),(141,108)]
DATA={
(15,1):logo(379,325,layer(0,f1),layer(2,m1,mirror(m1,189.5),c1)),
(15,2):logo(298,327,layer(1,cap2,foot2,m2,mirror(m2,149)),layer(0,c2)),
(15,3):logo(407,250,layer(1,w3a,w3b,w3c,mirror(w3a,203.5),mirror(w3b,203.5),mirror(w3c,203.5)),layer(0,m3,mirror(m3,203.5),c3)),
(15,4):logo(330,290,layer(1,roof4),layer(0,m4,mirror(m4,165),c4)),
(15,5):logo(361,218,layer(1,roof5,base5),layer(0,m5,mirror(m5,180.5),c5)),
(15,6):logo(326,366,layer(1,bar6,mirror(bar6,163)),layer(0,m6,mirror(m6,163),c6)),
(15,7):logo(323,306,layer(1,roof7,bar7,mirror(bar7,161.5)),layer(0,m7,mirror(m7,161.5),c7)),
(15,8):logo(400,318,layer(1,roof8,foot8,m8,mirror(m8,200),c8),layer(0,side8,mirror(side8,200))),
(15,9):logo(334,297,layer(1,frame9),layer(0,m9,mirror(m9,167),c9)),
(14,2):logo(359,303,layer(0,roof10),layer(1,foot10,m10,[(x+229,y) for x,y in m10],c10))}
IDS={(15,n):v for n,v in enumerate(['1pBKaaFrRed0o-vv7iuRcMO3J9mcj70VQ','1gcSP97E23w3irrCFvszZbvJz_FBFM93G','1D3owlngiXzo0WUnhRbpvZSJdHpD43TiA','1Bg_FkX-QzczoclfS832Ij4Ywuq4d2iTo','1S-PeEMgkcnPlhA6w3Ql-6m1az1NBT6to','1LhUUsRYDq4TNqSysfXwAoA_yMigXsRjh','1nQ_n4NyLjbIpdtBwGsnOlhG9LEecrNZO','1N2xHAoD4Wv_0scpWZu2V4ofkNM9UTpTK','1Y0PCy7iGIMd19HavhCUgc43pZH30iee7'],1)}
IDS[14,2]='105Eh9PKuZNqKNCb9tQQ3m83oFWaCSdHK'
ALIAS_IDS=['1PUFj4UXocnG81LSzoH-D6XAz3ePcIXwz','1PGP8ChgSJMPqUvD0Knz-8PxTTqGHuHCM','1vqFXvYbltMc4BoAUeZO22pg1ehLf-MPo','1wi0X3uVXKS4hqRosni1Qs9My6i8ko1fk','1knY8hbx6cWqK0MfbeQ8Kwbc80vWAXRHz','1loBELtOFwp_tE0uFIRbr1hhwwpbkl6EF','1KR1EXUIH7NAkY1mp_hedH8UFa_t1CPqW','1U0FPzTtsJTOOj4TdehnyeWFsBLxtKW4O']
if __name__=='__main__':
    previous=json.loads((R/'04-desain/variasi-svg/batch-14/progress.json').read_text())
    groups=previous['groups'];groups['15']=dict(redrawn=list(range(1,10)),pending=[]);groups['rasio-14']=dict(redrawn=[1,2],pending=list(range(3,10)))
    export_batch('15',DATA,IDS,119,groups,source_names={(14,2):'Max_a_Gambar_kotak_rasio_1_14_logo-02.png'},entry_ids={(14,2):'exp-rasio-014-02'})
    out=R/'04-desain/variasi-svg/batch-15';p=json.loads((out/'progress.json').read_text());aliases=previous['sourceAliases']
    for n,drive_id in enumerate(ALIAS_IDS,2):
        src=R/f'google_drive/Max_a_Gambar_kotak_berisi__14_logo-{n:02}.png';original=R/f'google_drive/Max_a_Gambar_kotak_berisi__13_logo-{n:02}.png'
        digest=hashlib.sha256(src.read_bytes()).hexdigest();assert digest==hashlib.sha256(original.read_bytes()).hexdigest()
        aliases.append(dict(group=14,sourceNumber=n,driveId=drive_id,sourceName=src.name,sourceSha256=digest,duplicateOf=f'exp-013-{n:02}',status='exact-byte-duplicate-no-new-redraw'))
    p.update(uniqueDriveMasters=119,driveSourcesCoveredIncludingDuplicates=137,remainingNotProcessed=205,progressPercent=round(137/342*100,2),redrawOnlyPercent=round(119/342*100,2),progressBasis='119 manual masters + 18 verified duplicate source files / 342 reported files',sourceAliases=aliases,buildPolicy='Redraw only; all APK jobs paused; no app catalog changes.')
    for e in p['entries']:
        e['sourceFamily']='rasio_1' if e['id'].startswith('exp-rasio-') else 'berisi'
        e['appIntegration']='deferred-no-apk-requested'
    (out/'progress.json').write_text(json.dumps(p,indent=2))
    page=(out/'perbandingan.html').read_text().replace('119 dari 342 sumber','119 master unik; 137 dari 342 sumber tercakup').replace('<strong>223</strong>','<strong>205</strong>').replace('34.80%','40.06%').replace('Kelompok 14 · Logo 02','Keluarga rasio_1 · Kelompok 14 · Logo 02')
    page=page.replace('</main>','<h2>Audit terbatas dan progres</h2><p>Kelompok berisi 14/02–09 identik byte/SHA-256 dengan 13/02–09. Bersama alias 14/01 sebelumnya, seluruh kelompok berisi 14 adalah duplikat 13. Tidak dibuat ulang. Kumulatif 119 master + 18 alias = 137/342 sumber (40,06%), sisa 205. Redraw unik saja: 119/342 (34,80%). Total 342 belum diaudit global. Tidak ada build APK atau perubahan katalog Android.</p></main>')
    (out/'perbandingan.html').write_text(page)
