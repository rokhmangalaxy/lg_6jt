"""Prepare reviewed pilot only. Never rename or modify the source Drive files."""
from pathlib import Path
import subprocess,hashlib,json
R=Path(__file__).resolve().parents[1]
OUT=R/'android-logo/app/src/main/assets/exploration';OUT.mkdir(parents=True,exist_ok=True)
entries=[]
for number,drive_id in [(1,'1IVHq9P1VGzAsMO5deUIAKPokgLzgn7Yz'),(8,'1Vvrn5uwVmy-MvJb2h65UJ5LZFoLuOKsO')]:
    source=R/f'google_drive/Max_a_Gambar_kotak_berisi__1_logo-{number:02}.png'
    stable_id=f'exp-001-{number:02}'
    subprocess.run(['convert',str(source),'-alpha','on','-fuzz','12%','-fill','none','-draw','matte 0,0 floodfill','-trim','+repage','-bordercolor','none','-border','16',str(OUT/f'{stable_id}.png')],check=True)
    entries.append(dict(id=stable_id,name=f'Eksplorasi 01–{number:02}',sourceName=source.name,driveId=drive_id,sourceSha256=hashlib.sha256(source.read_bytes()).hexdigest(),asset=f'exploration/{stable_id}.png',format='raster',group=1,sourceNumber=number,status='pilot-reviewed'))
assert len({e['sourceSha256'] for e in entries})==len(entries),'Exact source duplicate'
(OUT/'catalog.json').write_text(json.dumps(dict(version=1,driveFolderId='1fkCuPkqGe4jRAvKhTmi8Z78veYqmWGVh',reportedFolderFiles=342,reviewedEntries=entries,scope='Two-source pilot only; remaining Drive files not audited for duplicates.'),indent=2))
