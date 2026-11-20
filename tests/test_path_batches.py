"""Design-only checks. No Android/Gradle/APK invocation."""
from pathlib import Path
import hashlib
import json
import unittest
import xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1]
class PathBatchTest(unittest.TestCase):
    batch=R/'04-desain/variasi-svg/batch-03'
    count=10
    total=15
    pending=[7,8,9]

    def test_manual_masters_match_native_paths(self):
        entries=json.loads((self.batch/'progress.json').read_text())['entries']
        self.assertEqual(len(entries),self.count)
        self.assertEqual(len({e['id'] for e in entries}),self.count)
        for entry in entries:
            with self.subTest(id=entry['id']):
                data=json.loads((R/entry['pathJson']).read_text())
                self.assertEqual(data['construction'],'manual-geometric-v1')
                root=ET.parse(R/entry['masterSvg']).getroot()
                self.assertEqual(root.get('viewBox'),f'0 0 {data["width"]} {data["height"]}')
                self.assertFalse(root.findall('.//{http://www.w3.org/2000/svg}image'))
                self.assertFalse(root.findall('.//{http://www.w3.org/2000/svg}text'))
                paths=root.findall('{http://www.w3.org/2000/svg}path')
                self.assertEqual(len(paths),len(data['layers']))
                for path,layer in zip(paths,data['layers']):
                    self.assertEqual(path.get('fill'),['#DC2626','#173257','#FFFFFF'][layer['color']])
                    self.assertEqual(path.get('fill-rule'),'evenodd')
                    expected=' '.join(c[0]+' '+' '.join(str(v) for v in c[1:]) for c in layer['commands'])
                    self.assertEqual(path.get('d'),expected)
                    self.assertEqual({c[0] for c in layer['commands']},{'M','L','Z'})
                    opened=False;polygon=[]
                    for command in layer['commands']:
                        if command[0]=='M':
                            self.assertFalse(opened);opened=True;polygon=[]
                        if command[0] in ('M','L'):
                            self.assertTrue(opened)
                            x,y=command[1:];self.assertTrue(0<=x<=data['width']);self.assertTrue(0<=y<=data['height']);polygon.append((x,y))
                        if command[0]=='Z':
                            self.assertTrue(opened);self.assertGreaterEqual(len(polygon),3)
                            area=sum(x1*y2-x2*y1 for (x1,y1),(x2,y2) in zip(polygon,polygon[1:]+polygon[:1]))
                            self.assertGreater(abs(area),1);opened=False
                    self.assertFalse(opened)
    def test_progress_and_limited_audit_are_consistent(self):
        progress=json.loads((self.batch/'progress.json').read_text())
        self.assertTrue(progress['apkBuildsPaused'])
        self.assertEqual(progress['driveSourcesWithMasters'],self.total)
        self.assertEqual(progress['remainingNotProcessed']+progress['driveSourcesWithMasters'],342)
        self.assertEqual(progress['groups']['1']['pending'],[])
        self.assertEqual(progress['groups']['2']['pending'],self.pending)
        for e in progress['entries']:
            self.assertEqual(e['appIntegration'],'deferred-until-collection-complete')
            self.assertRegex(e['sourceSha256'],r'^[0-9a-f]{64}$')
            source=R/'google_drive'/e['sourceName']
            if source.exists():self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(),e['sourceSha256'])
    def test_apk_job_is_explicitly_paused(self):
        workflow=(R/'.github/workflows/android-apk.yml').read_text()
        block=workflow.split('\n  build:\n',1)[1]
        self.assertIn('    if: ${{ false }}',block.split('    runs-on:',1)[0])
        self.assertIn("test_path_batches.py",workflow)
class PathBatch04Test(PathBatchTest):
    batch=R/'04-desain/variasi-svg/batch-04'
    count=3
    total=18
    pending=[]

    def test_no_cross_batch_ids_or_geometry_duplicates(self):
        previous=json.loads((R/'04-desain/variasi-svg/batch-03/progress.json').read_text())
        current=json.loads((self.batch/'progress.json').read_text())
        self.assertFalse({e['id'] for e in previous['entries']} & {e['id'] for e in current['entries']})
        known={hashlib.sha256(p.read_bytes()).hexdigest() for p in (R/'04-desain/variasi-svg').rglob('*.svg') if p.parent!=self.batch}
        for e in current['entries']:
            digest=hashlib.sha256((R/e['masterSvg']).read_bytes()).hexdigest()
            self.assertNotIn(digest,known)
            known.add(digest)
        self.assertTrue(current['visualReview']['requiresUserApproval'])
        self.assertEqual(current['exactDuplicateAudit']['filesChecked'],18)
        self.assertEqual(current['exactDuplicateAudit']['duplicateGroups'],[])

class PathBatch05Test(PathBatchTest):
    batch=R/'04-desain/variasi-svg/batch-05'
    count=10
    total=28
    pending=[]

    def test_full_capacity_and_provenance(self):
        progress=json.loads((self.batch/'progress.json').read_text())
        self.assertEqual(progress['newMasterCount'],10)
        self.assertEqual(progress['groups']['3']['redrawn'],list(range(1,10)))
        self.assertEqual(progress['groups']['4']['redrawn'],[1])
        self.assertEqual(progress['exactDuplicateAudit']['filesChecked'],28)
        self.assertEqual(progress['exactDuplicateAudit']['duplicateGroups'],[])
        known={hashlib.sha256(p.read_bytes()).hexdigest() for p in (R/'04-desain/variasi-svg').rglob('*.svg') if p.parent!=self.batch}
        previous_ids=set()
        for batch in ('03','04'):
            previous=json.loads((R/f'04-desain/variasi-svg/batch-{batch}/progress.json').read_text())
            previous_ids.update(e['id'] for e in previous['entries'])
        for e in progress['entries']:
            self.assertNotIn(e['id'],previous_ids)
            digest=hashlib.sha256((R/e['masterSvg']).read_bytes()).hexdigest()
            self.assertNotIn(digest,known)
            known.add(digest)

    def test_polygons_do_not_self_intersect(self):
        def orient(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
        def crossing(a,b,c,d):
            return orient(a,b,c)*orient(a,b,d)<0 and orient(c,d,a)*orient(c,d,b)<0
        for path in self.batch.glob('exp-*.json'):
            data=json.loads(path.read_text())
            for layer in data['layers']:
                poly=[]
                for command in layer['commands']:
                    if command[0]=='M':poly=[command[1:]]
                    elif command[0]=='L':poly.append(command[1:])
                    else:
                        edges=list(zip(poly,poly[1:]+poly[:1]))
                        for i,(a,b) in enumerate(edges):
                            self.assertNotEqual(a,b)
                            for j,(c,d) in enumerate(edges):
                                if j>i+1 and not (i==0 and j==len(edges)-1):
                                    self.assertFalse(crossing(a,b,c,d),(path.name,i,j))

    def test_negative_spaces_and_split_center_are_transparent(self):
        def painted(key,point):
            x,y=point
            data=json.loads((self.batch/f'{key}.json').read_text())
            for layer in data['layers']:
                inside=False;poly=[]
                for command in layer['commands']:
                    if command[0]=='M':poly=[command[1:]]
                    elif command[0]=='L':poly.append(command[1:])
                    else:
                        for (x1,y1),(x2,y2) in zip(poly,poly[1:]+poly[:1]):
                            if (y1>y)!=(y2>y) and x<(x2-x1)*(y-y1)/(y2-y1)+x1:inside=not inside
                if inside:return True
            return False
        # Transparent counters rather than white paint; center seam stays open.
        for key,point in [('exp-003-09',(208,180)),('exp-003-09',(208,40)),('exp-003-09',(208,280)),('exp-003-04',(175,120)),('exp-003-02',(152,160)),('exp-004-01',(165,160))]:
            self.assertFalse(painted(key,point),(key,point))
        for key,point in [('exp-003-09',(180,180)),('exp-003-09',(40,162)),('exp-003-04',(20,120)),('exp-003-02',(18,170)),('exp-004-01',(20,156))]:
            self.assertTrue(painted(key,point),(key,point))

class PathBatch06Test(PathBatchTest):
    batch=R/'04-desain/variasi-svg/batch-06'
    count=10
    total=38
    pending=[]
    test_polygons_do_not_self_intersect=PathBatch05Test.test_polygons_do_not_self_intersect

    def test_full_capacity_and_no_duplicate_master_ids(self):
        progress=json.loads((self.batch/'progress.json').read_text())
        self.assertEqual(progress['newMasterCount'],10)
        self.assertEqual(progress['groups']['4']['redrawn'],list(range(1,10)))
        self.assertEqual(progress['groups']['5']['redrawn'],[1,2])
        self.assertEqual(progress['exactDuplicateAudit']['filesChecked'],38)
        self.assertEqual(progress['exactDuplicateAudit']['duplicateGroups'],[])
        previous_ids=set()
        for batch in ('03','04','05'):
            previous=json.loads((R/f'04-desain/variasi-svg/batch-{batch}/progress.json').read_text())
            previous_ids.update(e['id'] for e in previous['entries'])
        known={hashlib.sha256(p.read_bytes()).hexdigest() for p in (R/'04-desain/variasi-svg').rglob('*.svg') if p.parent!=self.batch}
        for e in progress['entries']:
            self.assertNotIn(e['id'],previous_ids)
            digest=hashlib.sha256((R/e['masterSvg']).read_bytes()).hexdigest()
            self.assertNotIn(digest,known)
            known.add(digest)

    def test_badge_bolt_holes_and_counters_are_transparent(self):
        def painted(key,x,y):
            data=json.loads((self.batch/f'{key}.json').read_text())
            for layer in data['layers']:
                inside=False;poly=[]
                for c in layer['commands']:
                    if c[0]=='M':poly=[c[1:]]
                    elif c[0]=='L':poly.append(c[1:])
                    else:
                        for (x1,y1),(x2,y2) in zip(poly,poly[1:]+poly[:1]):
                            if (y1>y)!=(y2>y) and x<(x2-x1)*(y-y1)/(y2-y1)+x1:inside=not inside
                if inside:return True
            return False
        for key,x,y in [('exp-004-08',42,103),('exp-004-08',354,103),('exp-004-08',177,103),('exp-004-03',125,160),('exp-004-05',188,180),('exp-004-09',160,180),('exp-005-01',180,180),('exp-005-02',190,160)]:
            self.assertFalse(painted(key,x,y),(key,x,y))
        for key,x,y in [('exp-004-08',60,103),('exp-004-08',10,103),('exp-004-03',142,160),('exp-004-05',160,180),('exp-004-09',135,180),('exp-005-02',150,160)]:
            self.assertTrue(painted(key,x,y),(key,x,y))

if __name__=='__main__':unittest.main()
