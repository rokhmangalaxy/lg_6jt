"""Final five source-specific manual polygon masters; no tracing or APK."""
from build_drive_batch_03 import layer,mirror,logo
from design_batch_io import export_batch
from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parents[1]
# Unnumbered /05: notched navy roof/base; tall red initials.
t1=[(10,91),(158,9),(306,91),(306,120),(195,75),(195,67),(158,44),(122,67),(122,75),(10,120)]
b1=[(10,244),(121,288),(121,296),(158,319),(195,296),(195,288),(306,244),(306,273),(158,355),(10,273)]
m1=[(10,137),(35,128),(56,156),(84,120),(106,115),(106,251),(78,246),(78,182),(55,206),(36,186),(36,237),(10,228)]
c1=[(119,129),(158,105),(197,128),(197,172),(168,172),(168,151),(150,151),(150,213),(168,213),(168,197),(197,197),(197,232),(158,253),(119,232)]
# /06: two I-beam red rails with short-chord rounded recesses.
t2=[(10,10),(353,10),(353,23),(330,23),(324,25),(320,29),(318,35),(318,50),(320,55),(348,55),(348,69),(259,69),(259,60),(278,60),(282,56),(282,43),(80,43),(76,46),(76,56),(80,60),(95,60),(95,69),(10,69),(10,55),(34,55),(39,51),(39,31),(36,27),(31,24),(10,24)]
b2=[(10,191),(95,191),(95,200),(80,200),(76,204),(76,218),(282,218),(282,205),(278,201),(259,200),(259,191),(348,191),(348,204),(323,204),(318,209),(318,228),(321,233),(326,236),(351,236),(351,250),(10,250),(10,237),(29,237),(35,235),(39,231),(39,210),(36,206),(10,205)]
m2=[(10,81),(36,81),(63,114),(94,81),(119,81),(119,179),(88,179),(88,132),(64,158),(40,135),(40,179),(10,179)]
c2=[(150,81),(208,81),(226,96),(226,120),(192,120),(192,110),(188,106),(170,106),(166,110),(166,150),(170,154),(188,154),(192,150),(192,141),(226,141),(226,164),(209,179),(150,179),(132,164),(132,97)]
# /07: downfold red cap/base, navy tapered Ms and perspective C.
t3=[(9,10),(175,62),(342,10),(342,33),(175,85),(9,34)]
b3=[(9,191),(175,239),(342,191),(342,215),(175,265),(9,215)]
m3=[(9,52),(40,63),(68,115),(104,83),(126,91),(126,206),(94,197),(94,135),(65,161),(41,136),(41,185),(9,175)]
c3=[(141,95),(175,105),(208,95),(215,102),(215,127),(187,135),(187,126),(175,124),(160,127),(160,172),(175,178),(187,174),(187,161),(215,153),(215,188),(175,206),(134,188),(134,102)]
# /08: tall red hexagonal C with diagonal open mouth, navy swept Ms.
m4=[(9,109),(40,90),(60,115),(85,60),(118,40),(118,268),(85,249),(85,135),(60,176),(40,143),(40,222),(9,205)]
c4=[(126,36),(171,9),(216,36),(216,94),(182,115),(182,64),(171,56),(160,64),(160,239),(171,246),(182,239),(182,175),(216,195),(216,272),(171,298),(126,272)]
# /09: split red tower, detached navy roof legs, red MCM and two navy baselines.
t5=[(158,33),(190,10),(190,149),(158,149)]
s5=[(22,140),(149,45),(149,149),(118,149),(118,101),(28,155),(22,155)]
m5=[(22,164),(55,164),(79,193),(103,164),(137,164),(137,262),(104,262),(104,210),(79,237),(54,212),(54,262),(22,262)]
c5=[(165,164),(222,164),(239,180),(239,203),(207,203),(207,193),(203,189),(183,189),(179,193),(179,233),(183,237),(203,237),(207,233),(207,225),(239,225),(239,247),(222,262),(165,262),(147,247),(147,180)]
b5=[(22,272),(363,272),(363,286),(22,286)]
u5=[(9,295),(377,295),(377,315),(9,315)]
DATA={
(0,5):logo(316,363,layer(1,t1,b1),layer(0,m1,mirror(m1,158),c1)),
(0,6):logo(361,259,layer(0,t2,b2),layer(1,m2,[(x+229,y) for x,y in m2],c2)),
(0,7):logo(351,274,layer(0,t3,b3),layer(1,m3,mirror(m3,175.5),c3)),
(0,8):logo(342,307,layer(0,c4),layer(1,m4,mirror(m4,171))),
(0,9):logo(386,324,layer(0,t5,[(194,9),(229,32),(229,149),(194,149)],m5,[(x+227,y) for x,y in m5],c5),layer(1,s5,mirror(s5,192.5),b5,u5))}
VALUES=['1b5eoneoO0Tp__YyiV6QLc8yD1_qaq5Y-','1SCXtwrcR3DOfw4PRHxdsAK7W31rBwGOP','16MsmVHxiNxP0IeuUCNr6Trhs-SwPB__K','1Ki92W259lKUy7cMKv9ds1oMf_ZoB7kMY','1_gMP-STT-r-6t8o-QUu0sFLFmm1wQ-kZ']
if __name__=='__main__':
    old=json.loads((R/'04-desain/variasi-svg/batch-35/progress.json').read_text())
    groups=old['groups'];groups['rasio-unnumbered']=dict(redrawn=list(range(1,10)),pending=[])
    names={k:f'Max_a_Gambar_kotak_rasio_1_logo-{k[1]:02}.png' for k in DATA}
    ids={k:f'exp-rasio-unnumbered-{k[1]:02}' for k in DATA}
    seen={e['sourceSha256'] for p in (R/'04-desain/variasi-svg').glob('batch-*/progress.json') if p.parent.name!='batch-36' for e in json.loads(p.read_text())['entries']}
    for name in names.values():
        digest=hashlib.sha256((R/'google_drive'/name).read_bytes()).hexdigest()
        assert digest not in seen, f'Duplicate source requires alias audit: {name}'
        seen.add(digest)
    export_batch('36',DATA,dict(zip(DATA,VALUES)),324,groups,source_names=names,entry_ids=ids)
    out=R/'04-desain/variasi-svg/batch-36';p=json.loads((out/'progress.json').read_text())
    p.update(uniqueDriveMasters=324,driveSourcesCoveredIncludingDuplicates=342,remainingNotProcessed=0,progressPercent=100.0,redrawOnlyPercent=round(324/342*100,2),progressBasis='324 manual masters + 18 verified duplicate source files / 342 reported files',sourceAliases=old['sourceAliases'],buildPolicy='Redraw only; all APK jobs paused; Android catalog unchanged.')
    for e in p['entries']:e.update(sourceFamily='rasio_1_unnumbered',appIntegration='deferred-no-apk-requested')
    (out/'progress.json').write_text(json.dumps(p,indent=2))
    page=(out/'perbandingan.html').read_text().replace('324 dari 342 sumber','324 master unik; 342 dari 342 sumber tercakup').replace('<strong>18</strong>','<strong>0</strong>').replace('94.74%','100.00%').replace('Koleksi keseluruhan belum selesai.','Cakupan file sumber selesai; persetujuan visual dan integrasi aplikasi belum selesai.').replace('Kelompok 0 ·','Keluarga rasio_1 tanpa nomor tambahan ·')
    page=page.replace('</main>','<h2>Audit penutupan sumber</h2><p>324 master unik + 18 alias = 342/342 (100%), sisa 0. Redraw unik saja: 324/342 (94,74%). Lima hash baru berbeda satu sama lain dan dari master terdahulu. Tidak ada desain tambahan untuk mengejar target 10 karena hanya lima sumber tersisa. Inventaris lokal dan alias dicocokkan oleh audit_inventory.json. Ini bukan klaim seluruh motif unik secara visual atau final produksi; semua master tetap menunggu persetujuan visual. Tidak ada build APK atau perubahan katalog aplikasi.</p></main>')
    (out/'perbandingan.html').write_text(page)
    # Reconcile all downloaded source bytes, not a fresh remote folder listing.
    masters=[e for f in sorted((R/'04-desain/variasi-svg').glob('batch-*/progress.json')) for e in json.loads(f.read_text())['entries']]
    catalog=json.loads((R/'android-logo/app/src/main/assets/exploration/catalog.json').read_text())
    known={e['id'] for e in masters}
    masters += [e for e in catalog['reviewedEntries'] if e['id'] in {'exp-001-01','exp-001-08'} and e['id'] not in known]
    assert len(masters)==324 and len({e['id'] for e in masters})==324
    assert len({e['sourceSha256'] for e in masters})==324
    byid={e['id']:e for e in masters}
    records=[]
    for e in masters:
        src=R/'google_drive'/e['sourceName']
        assert hashlib.sha256(src.read_bytes()).hexdigest()==e['sourceSha256']
        assert (R/e['masterSvg']).is_file()
        native=e.get('pathJson') or 'android-logo/app/src/main/assets/'+e['vectorAsset']
        assert (R/native).is_file()
        records.append(dict(sourceName=e['sourceName'],driveId=e['driveId'],sourceSha256=e['sourceSha256'],masterId=e['id'],masterSvg=e['masterSvg'],pathJson=native,kind='manual-master'))
    for e in p['sourceAliases']:
        assert hashlib.sha256((R/'google_drive'/e['sourceName']).read_bytes()).hexdigest()==e['sourceSha256']==byid[e['duplicateOf']]['sourceSha256']
        records.append(dict(sourceName=e['sourceName'],driveId=e['driveId'],sourceSha256=e['sourceSha256'],masterId=e['duplicateOf'],kind='exact-byte-alias'))
    actual={f.name for f in (R/'google_drive').glob('*logo-*.png')}
    covered={e['sourceName'] for e in records}
    expected={f'Max_a_Gambar_kotak_berisi__{g}_logo-{n:02}.png' for g in range(1,20) for n in range(1,10)} | {f'Max_a_Gambar_kotak_rasio_1_{g}_logo-{n:02}.png' for g in range(1,19) for n in range(1,10)} | {f'Max_a_Gambar_kotak_rasio_1_logo-{n:02}.png' for n in range(1,10)}
    assert len(records)==len(covered)==len(expected)==342 and actual==covered==expected
    assert len({e['driveId'] for e in records})==342
    audit=dict(scope='All 342 downloaded PNG sources matched against provenance; not a fresh full remote listing or semantic visual deduplication.',sourceFolder='1fkCuPkqGe4jRAvKhTmi8Z78veYqmWGVh',downloadedPngCount=342,manualMasterCount=324,exactByteAliasCount=18,uniqueSourceSha256Count=324,uncoveredSources=[],unexpectedLocalSources=[],visualApproval='pending',records=sorted(records,key=lambda e:e['sourceName']))
    (out/'audit_inventory.json').write_text(json.dumps(audit,indent=2))
    print('Reconciled 342 downloaded PNGs: 324 manual masters + 18 exact-byte aliases; 0 uncovered.')
