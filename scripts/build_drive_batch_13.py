"""One new manual master plus nine verified byte-identical source aliases."""
from build_drive_batch_03 import layer, mirror, logo
from design_batch_io import export_batch
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1]
o=[(168,9),(325,91),(325,234),(168,362),(9,234),(9,91)]
i=[(168,30),(307,102),(307,225),(168,340),(27,225),(27,102)]
m=[(38,118),(50,112),(67,138),(87,87),(112,72),(112,288),(87,269),(87,168),(70,195),(54,172),(54,240),(38,221)]
c=[(168,44),(208,66),(208,144),(189,144),(189,88),(168,73),(143,88),(143,277),(166,294),(189,277),(189,230),(208,230),(208,295),(168,324),(125,295),(125,66)]
DATA={(11,9):logo(335,371,layer(1,o,i),layer(0,m,mirror(m,167.5),c))}
IDS={(11,9):'14Wp9mIqa_--b02AmFUuahVIsagUBkzwn'}
ALIAS_IDS=['1hy_Q8mc0HZVFWjnQQpxFQUq_DOyjbEKZ','1nRZLDTu6FhVVizwIo_66O6FUyiW-5paN','1d1W11PKtufqOxGl22pAmIz4e7wFMo89R','1ovG3j6Vc99yIGvS3HqXGaNmtkc8rDrTx','1KfcUB_yD0wOBEecb6fb0jpb9IMOWcW1x','1-DMOYuGRwxpH0aHGOM2W0gwvPLZLc_i6','1F0NHSqNnna1wBxR3D6zKD646_-ej3s3i','19OCt8d4AxX2IqYXMw2R69xG4n76EIdrr','1-5vODvv6tkYgbAl0aW0bPuVgu5v0ZYzm']
if __name__=='__main__':
    export_batch('13',DATA,IDS,total=99,groups={str(g):dict(redrawn=list(range(1,10)),pending=[]) for g in range(1,12)})
    out=R/'04-desain/variasi-svg/batch-13';p=json.loads((out/'progress.json').read_text())
    aliases=[]
    for n,drive_id in enumerate(ALIAS_IDS,1):
        a=R/f'google_drive/Max_a_Gambar_kotak_berisi__11_logo-{n:02}.png';b=R/f'google_drive/Max_a_Gambar_kotak_berisi__12_logo-{n:02}.png'
        digest=hashlib.sha256(b.read_bytes()).hexdigest();assert hashlib.sha256(a.read_bytes()).hexdigest()==digest
        aliases.append(dict(group=12,sourceNumber=n,driveId=drive_id,sourceName=b.name,sourceSha256=digest,duplicateOf=f'exp-011-{n:02}',status='exact-byte-duplicate-no-new-redraw'))
    p.update(apkBuildsPaused=False,buildPolicy='User explicitly requested an APK now; manual workflow dispatch only.',uniqueDriveMasters=99,driveSourcesCoveredIncludingDuplicates=108,remainingNotProcessed=234,progressPercent=round(108/342*100,2),redrawOnlyPercent=round(99/342*100,2),progressBasis='covered source files including nine verified duplicates / 342 reported files',sourceAliases=aliases)
    p['notes']=['99 unique Drive masters; nine duplicate sources reuse group 11 geometry.','108 sources covered, 234 not processed; collection not complete.','APK integration and manually authorized build follow in this turn.']
    (out/'progress.json').write_text(json.dumps(p,indent=2))
    page=(out/'perbandingan.html').read_text().replace('99 dari 342 sumber','99 master unik; 108 dari 342 sumber terpetakan').replace('<strong>243</strong>','<strong>234</strong>').replace('28.95%','31.58%').replace('Tidak ada build APK.','Pengguna meminta build APK setelah batch ini.')
    page=page.replace('</main>', '<h2>Audit duplikat kelompok 12</h2><p>Kesembilan PNG kelompok 12 identik SHA-256 dengan nomor yang sama pada kelompok 11. Tidak dibuat logo atau klaim redraw tambahan. 99 master unik + 9 sumber duplikat = 108 sumber terpetakan dari 342; sisa 234 (31,58%).</p></main>')
    (out/'perbandingan.html').write_text(page)
