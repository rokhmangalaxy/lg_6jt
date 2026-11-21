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
        self.assertIn("    if: ${{ false }}",block.split('    runs-on:',1)[0])
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

class PathBatch07Test(PathBatchTest):
    batch=R/'04-desain/variasi-svg/batch-07'
    count=10
    total=48
    pending=[]
    test_polygons_do_not_self_intersect=PathBatch05Test.test_polygons_do_not_self_intersect

    def test_full_capacity_unique_masters_and_percentage(self):
        progress=json.loads((self.batch/'progress.json').read_text())
        self.assertEqual(progress['newMasterCount'],10)
        self.assertEqual(progress['groups']['5']['redrawn'],list(range(1,10)))
        self.assertEqual(progress['groups']['6']['redrawn'],[1,2,3])
        self.assertEqual(progress['exactDuplicateAudit']['filesChecked'],48)
        self.assertEqual(progress['exactDuplicateAudit']['duplicateGroups'],[])
        self.assertEqual(progress['remainingNotProcessed'],294)
        self.assertEqual(progress['progressPercent'],14.04)
        self.assertEqual(progress['progressPercent'],round(self.total/342*100,2))
        page=(self.batch/'perbandingan.html').read_text()
        self.assertIn('48 dari 342',page)
        self.assertIn('14.04%',page)
        previous_ids=set()
        for batch in ('03','04','05','06'):
            previous=json.loads((R/f'04-desain/variasi-svg/batch-{batch}/progress.json').read_text())
            previous_ids.update(e['id'] for e in previous['entries'])
        known={hashlib.sha256(p.read_bytes()).hexdigest() for p in (R/'04-desain/variasi-svg').rglob('*.svg') if p.parent!=self.batch}
        for e in progress['entries']:
            self.assertNotIn(e['id'],previous_ids)
            digest=hashlib.sha256((R/e['masterSvg']).read_bytes()).hexdigest()
            self.assertNotIn(digest,known)
            known.add(digest)

    def test_split_hexagon_and_oblique_counters(self):
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
        for key,x,y in [('exp-005-08',149,290),('exp-005-08',149,330),('exp-005-08',130,180),('exp-005-06',55,180),('exp-005-07',200,270),('exp-006-01',175,180),('exp-006-02',175,160)]:
            self.assertFalse(painted(key,x,y),(key,x,y))
        for key,x,y in [('exp-005-08',160,290),('exp-005-08',160,325),('exp-005-06',40,180),('exp-005-07',200,300),('exp-006-01',197,180),('exp-006-02',140,160)]:
            self.assertTrue(painted(key,x,y),(key,x,y))

class PathBatch08Test(PathBatchTest):
    batch=R/'04-desain/variasi-svg/batch-08'
    count=10
    total=58
    pending=[]
    test_polygons_do_not_self_intersect=PathBatch05Test.test_polygons_do_not_self_intersect

    def test_full_capacity_unique_masters_and_percentage(self):
        progress=json.loads((self.batch/'progress.json').read_text())
        self.assertEqual(progress['newMasterCount'],10)
        self.assertEqual(progress['groups']['6']['redrawn'],list(range(1,10)))
        self.assertEqual(progress['groups']['7']['redrawn'],[1,2,3,4])
        self.assertEqual(progress['exactDuplicateAudit']['filesChecked'],58)
        self.assertEqual(progress['exactDuplicateAudit']['duplicateGroups'],[])
        self.assertEqual(progress['remainingNotProcessed'],284)
        self.assertEqual(progress['progressPercent'],16.96)
        self.assertEqual(progress['progressPercent'],round(self.total/342*100,2))
        page=(self.batch/'perbandingan.html').read_text()
        self.assertIn('58 dari 342',page)
        self.assertIn('16.96%',page)
        previous_ids=set()
        for batch in ('03','04','05','06','07'):
            previous=json.loads((R/f'04-desain/variasi-svg/batch-{batch}/progress.json').read_text())
            previous_ids.update(e['id'] for e in previous['entries'])
        known={hashlib.sha256(p.read_bytes()).hexdigest() for p in (R/'04-desain/variasi-svg').rglob('*.svg') if p.parent!=self.batch}
        for e in progress['entries']:
            self.assertNotIn(e['id'],previous_ids)
            digest=hashlib.sha256((R/e['masterSvg']).read_bytes()).hexdigest()
            self.assertNotIn(digest,known)
            known.add(digest)

    def test_counters_separate_stripes_and_broken_diamond(self):
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
        for key,x,y in [('exp-006-05',140,160),('exp-007-02',135,160),('exp-007-03',40,146),('exp-007-04',147,170),('exp-006-06',201,47),('exp-006-09',178,268),('exp-006-09',178,313)]:
            self.assertFalse(painted(key,x,y),(key,x,y))
        for key,x,y in [('exp-006-05',165,160),('exp-007-02',160,160),('exp-007-03',40,158),('exp-007-04',125,170),('exp-006-06',201,20),('exp-006-09',178,290),('exp-006-09',178,333)]:
            self.assertTrue(painted(key,x,y),(key,x,y))

class PathBatch09Test(PathBatchTest):
    batch=R/'04-desain/variasi-svg/batch-09'
    count=10
    total=68
    pending=[]
    test_polygons_do_not_self_intersect=PathBatch05Test.test_polygons_do_not_self_intersect

    def test_full_capacity_unique_masters_and_percentage(self):
        progress=json.loads((self.batch/'progress.json').read_text())
        self.assertEqual(progress['newMasterCount'],10)
        self.assertEqual(progress['groups']['7']['redrawn'],list(range(1,10)))
        self.assertEqual(progress['groups']['8']['redrawn'],[1,2,3,4,5])
        self.assertEqual(progress['exactDuplicateAudit']['filesChecked'],68)
        self.assertEqual(progress['exactDuplicateAudit']['duplicateGroups'],[])
        self.assertEqual(progress['remainingNotProcessed'],274)
        self.assertEqual(progress['progressPercent'],19.88)
        self.assertEqual(progress['progressPercent'],round(self.total/342*100,2))
        page=(self.batch/'perbandingan.html').read_text()
        self.assertIn('68 dari 342',page)
        self.assertIn('19.88%',page)
        previous_ids=set()
        for batch in ('03','04','05','06','07','08'):
            previous=json.loads((R/f'04-desain/variasi-svg/batch-{batch}/progress.json').read_text())
            previous_ids.update(e['id'] for e in previous['entries'])
        known={hashlib.sha256(p.read_bytes()).hexdigest() for p in (R/'04-desain/variasi-svg').rglob('*.svg') if p.parent!=self.batch}
        for e in progress['entries']:
            self.assertNotIn(e['id'],previous_ids)
            digest=hashlib.sha256((R/e['masterSvg']).read_bytes()).hexdigest()
            self.assertNotIn(digest,known)
            known.add(digest)

    def test_counterplates_split_axis_and_wing_gaps(self):
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
        for key,x,y in [('exp-007-07',179,20),('exp-007-07',179,285),('exp-007-06',60,100),('exp-007-09',50,144),('exp-008-04',28,180),('exp-008-01',135,180),('exp-008-05',195,160)]:
            self.assertFalse(painted(key,x,y),(key,x,y))
        for key,x,y in [('exp-007-07',166,20),('exp-007-07',166,285),('exp-007-06',60,110),('exp-007-09',80,144),('exp-008-04',15,180),('exp-008-01',160,180),('exp-008-05',160,160)]:
            self.assertTrue(painted(key,x,y),(key,x,y))

class PathBatch10Test(PathBatchTest):
    batch=R/'04-desain/variasi-svg/batch-10'
    count=10
    total=78
    pending=[]
    test_polygons_do_not_self_intersect=PathBatch05Test.test_polygons_do_not_self_intersect

    def test_full_capacity_unique_masters_and_percentage(self):
        progress=json.loads((self.batch/'progress.json').read_text())
        self.assertEqual(progress['newMasterCount'],10)
        self.assertEqual(progress['groups']['8']['redrawn'],list(range(1,10)))
        self.assertEqual(progress['groups']['9']['redrawn'],[1,2,3,4,5,6])
        self.assertEqual(progress['exactDuplicateAudit']['filesChecked'],78)
        self.assertEqual(progress['exactDuplicateAudit']['duplicateGroups'],[])
        self.assertEqual(progress['remainingNotProcessed'],264)
        self.assertEqual(progress['progressPercent'],22.81)
        self.assertEqual(progress['progressPercent'],round(self.total/342*100,2))
        page=(self.batch/'perbandingan.html').read_text()
        self.assertIn('78 dari 342',page)
        self.assertIn('22.81%',page)
        previous_ids=set()
        for batch in ('03','04','05','06','07','08','09'):
            previous=json.loads((R/f'04-desain/variasi-svg/batch-{batch}/progress.json').read_text())
            previous_ids.update(e['id'] for e in previous['entries'])
        known={hashlib.sha256(p.read_bytes()).hexdigest() for p in (R/'04-desain/variasi-svg').rglob('*.svg') if p.parent!=self.batch}
        for e in progress['entries']:
            self.assertNotIn(e['id'],previous_ids)
            digest=hashlib.sha256((R/e['masterSvg']).read_bytes()).hexdigest()
            self.assertNotIn(digest,known)
            known.add(digest)

    def test_detached_red_tips_counterplates_and_wing_gaps(self):
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
        for key,x,y in [('exp-009-06',85,168),('exp-009-06',310,168),('exp-009-01',170,180),('exp-008-08',140,170),('exp-008-06',33,110),('exp-008-06',190,110),('exp-009-04',60,90)]:
            self.assertFalse(painted(key,x,y),(key,x,y))
        for key,x,y in [('exp-009-06',70,168),('exp-009-06',325,168),('exp-009-06',95,168),('exp-009-01',195,180),('exp-008-08',160,170),('exp-008-06',18,110),('exp-008-06',160,110),('exp-009-04',60,70)]:
            self.assertTrue(painted(key,x,y),(key,x,y))

class PathBatch11Test(PathBatchTest):
    batch=R/'04-desain/variasi-svg/batch-11'
    count=10
    total=88
    pending=[]
    test_polygons_do_not_self_intersect=PathBatch05Test.test_polygons_do_not_self_intersect

    def test_full_capacity_unique_masters_and_percentage(self):
        progress=json.loads((self.batch/'progress.json').read_text())
        self.assertEqual(progress['newMasterCount'],10)
        self.assertEqual(progress['groups']['9']['redrawn'],list(range(1,10)))
        self.assertEqual(progress['groups']['10']['redrawn'],[1,2,3,4,5,6,7])
        self.assertEqual(progress['exactDuplicateAudit']['filesChecked'],88)
        self.assertEqual(progress['exactDuplicateAudit']['duplicateGroups'],[])
        self.assertEqual(progress['remainingNotProcessed'],254)
        self.assertEqual(progress['progressPercent'],25.73)
        self.assertEqual(progress['progressPercent'],round(self.total/342*100,2))
        page=(self.batch/'perbandingan.html').read_text()
        self.assertIn('88 dari 342',page)
        self.assertIn('25.73%',page)
        previous_ids=set()
        for batch in ('03','04','05','06','07','08','09','10'):
            previous=json.loads((R/f'04-desain/variasi-svg/batch-{batch}/progress.json').read_text())
            previous_ids.update(e['id'] for e in previous['entries'])
        known={hashlib.sha256(p.read_bytes()).hexdigest() for p in (R/'04-desain/variasi-svg').rglob('*.svg') if p.parent!=self.batch}
        for e in progress['entries']:
            self.assertNotIn(e['id'],previous_ids)
            digest=hashlib.sha256((R/e['masterSvg']).read_bytes()).hexdigest()
            self.assertNotIn(digest,known)
            known.add(digest)

    def test_outer_band_gaps_counterplates_and_wing_stripes(self):
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
        for key,x,y in [('exp-010-07',36,150),('exp-010-07',20,240),('exp-009-09',50,69),('exp-009-09',204,110),('exp-010-01',165,180),('exp-010-04',50,90),('exp-010-03',140,180)]:
            self.assertFalse(painted(key,x,y),(key,x,y))
        for key,x,y in [('exp-010-07',50,150),('exp-010-07',20,150),('exp-010-07',20,250),('exp-009-09',50,50),('exp-009-09',175,110),('exp-010-01',190,180),('exp-010-04',50,100),('exp-010-04',50,70),('exp-010-03',161,180)]:
            self.assertTrue(painted(key,x,y),(key,x,y))

class PathBatch12Test(PathBatchTest):
    batch=R/'04-desain/variasi-svg/batch-12'
    count=10
    total=98
    pending=[]
    test_polygons_do_not_self_intersect=PathBatch05Test.test_polygons_do_not_self_intersect

    def test_full_capacity_unique_masters_and_percentage(self):
        progress=json.loads((self.batch/'progress.json').read_text())
        self.assertEqual(progress['newMasterCount'],10)
        self.assertEqual(progress['groups']['10']['redrawn'],list(range(1,10)))
        self.assertEqual(progress['groups']['11']['redrawn'],[1,2,3,4,5,6,7,8])
        self.assertEqual(progress['exactDuplicateAudit']['filesChecked'],98)
        self.assertEqual(progress['exactDuplicateAudit']['duplicateGroups'],[])
        self.assertEqual(progress['remainingNotProcessed'],244)
        self.assertEqual(progress['progressPercent'],28.65)
        self.assertEqual(progress['progressPercent'],round(self.total/342*100,2))
        page=(self.batch/'perbandingan.html').read_text()
        self.assertIn('98 dari 342',page)
        self.assertIn('28.65%',page)
        previous_ids=set()
        for batch in ('03','04','05','06','07','08','09','10','11'):
            previous=json.loads((R/f'04-desain/variasi-svg/batch-{batch}/progress.json').read_text())
            previous_ids.update(e['id'] for e in previous['entries'])
        known={hashlib.sha256(p.read_bytes()).hexdigest() for p in (R/'04-desain/variasi-svg').rglob('*.svg') if p.parent!=self.batch}
        for e in progress['entries']:
            self.assertNotIn(e['id'],previous_ids)
            digest=hashlib.sha256((R/e['masterSvg']).read_bytes()).hexdigest()
            self.assertNotIn(digest,known)
            known.add(digest)

    def test_positive_initials_detached_tips_and_wing_gaps(self):
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
        for key,x,y in [('exp-011-07',84,151),('exp-011-07',203,150),('exp-011-07',161,150),('exp-010-08',60,94),('exp-011-03',60,101),('exp-011-08',180,116),('exp-011-04',170,160)]:
            self.assertFalse(painted(key,x,y),(key,x,y))
        for key,x,y in [('exp-011-07',65,151),('exp-011-07',145,151),('exp-011-07',174,151),('exp-010-08',60,80),('exp-010-08',60,110),('exp-011-03',60,120),('exp-011-08',150,116),('exp-011-04',140,160)]:
            self.assertTrue(painted(key,x,y),(key,x,y))

class PathBatch13Test(PathBatchTest):
    batch=R/'04-desain/variasi-svg/batch-13'
    count=1
    total=99
    pending=[]
    test_polygons_do_not_self_intersect=PathBatch05Test.test_polygons_do_not_self_intersect

    def test_progress_and_limited_audit_are_consistent(self):
        p=json.loads((self.batch/'progress.json').read_text())
        self.assertFalse(p['apkBuildsPaused'])
        self.assertEqual(p['uniqueDriveMasters'],99)
        self.assertEqual(p['driveSourcesCoveredIncludingDuplicates'],108)
        self.assertEqual(p['remainingNotProcessed'],234)
        self.assertEqual(p['progressPercent'],round(108/342*100,2))
        self.assertEqual(p['redrawOnlyPercent'],round(99/342*100,2))
        self.assertEqual(len(p['sourceAliases']),9)
        for alias in p['sourceAliases']:
            source=R/'google_drive'/alias['sourceName']
            original=R/f"google_drive/Max_a_Gambar_kotak_berisi__11_logo-{alias['sourceNumber']:02}.png"
            if source.exists() and original.exists():
                self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(),alias['sourceSha256'])
                self.assertEqual(source.read_bytes(),original.read_bytes())

    def test_integrated_catalog_and_native_geometry(self):
        import re
        assets=R/'android-logo/app/src/main/assets'
        entries=json.loads((assets/'exploration/catalog.json').read_text())['reviewedEntries']
        self.assertEqual(len(entries),101)
        self.assertEqual(len({e['id'] for e in entries}),101)
        self.assertFalse(any(e['id'].startswith('exp-012-') for e in entries))
        kotlin=(R/'android-logo/app/src/main/java/id/mcm/logopreview/LogoCatalog.kt').read_text()
        files=re.findall(r'"([^"\n]+\.png)"',kotlin)
        self.assertEqual(len(files),105)
        self.assertEqual(files[:11],['client-logo-04.png','client-attachment-01.png','client-attachment-08.png','client-attachment-09.png','exploration/exp-001-01.png','exploration/exp-001-08.png','exploration/geo-007.png','exploration/geo-008.png','exploration/exp-001-02.png','exploration/exp-001-03.png','exploration/exp-001-04.png'])
        self.assertEqual(set(files[4:]),{e['asset'] for e in entries})
        for e in entries:
            self.assertTrue((assets/e['asset']).read_bytes().startswith(b'\x89PNG'))
            native=json.loads((assets/e['vectorAsset']).read_text())
            if 'pathJson' in e:self.assertEqual(native,json.loads((R/e['pathJson']).read_text()))

class PathBatch14Test(PathBatchTest):
    batch=R/'04-desain/variasi-svg/batch-14'
    count=10
    total=109
    test_polygons_do_not_self_intersect=PathBatch05Test.test_polygons_do_not_self_intersect

    def test_progress_and_limited_audit_are_consistent(self):
        p=json.loads((self.batch/'progress.json').read_text())
        self.assertTrue(p['apkBuildsPaused'])
        self.assertEqual(p['newMasterCount'],10)
        self.assertEqual(p['uniqueDriveMasters'],109)
        self.assertEqual(p['driveSourcesCoveredIncludingDuplicates'],119)
        self.assertEqual(p['remainingNotProcessed'],223)
        self.assertEqual(p['progressPercent'],34.8)
        self.assertEqual(p['redrawOnlyPercent'],31.87)
        self.assertEqual(len(p['sourceAliases']),10)
        self.assertEqual(p['entries'][-1]['id'],'exp-rasio-014-01')
        self.assertEqual(p['entries'][-1]['sourceName'],'Max_a_Gambar_kotak_rasio_1_14_logo-01.png')
        previous_ids=set()
        for path in (R/'04-desain/variasi-svg').glob('batch-*/progress.json'):
            if path.parent!=self.batch:
                previous_ids.update(e['id'] for e in json.loads(path.read_text())['entries'])
        self.assertFalse(previous_ids & {e['id'] for e in p['entries']})
        known={hashlib.sha256(f.read_bytes()).hexdigest() for f in (R/'04-desain/variasi-svg').rglob('*.svg') if f.parent!=self.batch}
        for e in p['entries']:
            self.assertNotIn(hashlib.sha256((R/e['masterSvg']).read_bytes()).hexdigest(),known)
            src=R/'google_drive'/e['sourceName']
            if src.exists():self.assertEqual(hashlib.sha256(src.read_bytes()).hexdigest(),e['sourceSha256'])
        alias=p['sourceAliases'][-1]
        self.assertEqual(alias['duplicateOf'],'exp-013-01')
        source=R/'google_drive'/alias['sourceName']
        if source.exists():self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(),p['entries'][0]['sourceSha256'])
        self.assertEqual(len(json.loads((R/'android-logo/app/src/main/assets/exploration/catalog.json').read_text())['reviewedEntries']),101)

class PathBatch15Test(PathBatchTest):
    batch=R/'04-desain/variasi-svg/batch-15'
    count=10
    total=119
    test_polygons_do_not_self_intersect=PathBatch05Test.test_polygons_do_not_self_intersect

    def test_progress_and_limited_audit_are_consistent(self):
        p=json.loads((self.batch/'progress.json').read_text())
        self.assertTrue(p['apkBuildsPaused'])
        self.assertEqual(p['newMasterCount'],10)
        self.assertEqual(p['uniqueDriveMasters'],119)
        self.assertEqual(p['driveSourcesCoveredIncludingDuplicates'],137)
        self.assertEqual(p['remainingNotProcessed'],205)
        self.assertEqual(p['progressPercent'],40.06)
        self.assertEqual(p['redrawOnlyPercent'],34.8)
        self.assertEqual(len(p['sourceAliases']),18)
        self.assertEqual(p['entries'][-1]['id'],'exp-rasio-014-02')
        previous_ids=set()
        known=set()
        for f in (R/'04-desain/variasi-svg').glob('batch-*/progress.json'):
            if f.parent!=self.batch:
                previous_ids.update(e['id'] for e in json.loads(f.read_text())['entries'])
        for f in (R/'04-desain/variasi-svg').rglob('*.svg'):
            if f.parent!=self.batch:known.add(hashlib.sha256(f.read_bytes()).hexdigest())
        for e in p['entries']:
            self.assertNotIn(e['id'],previous_ids)
            digest=hashlib.sha256((R/e['masterSvg']).read_bytes()).hexdigest()
            self.assertNotIn(digest,known);known.add(digest)
            source=R/'google_drive'/e['sourceName']
            if source.exists():self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(),e['sourceSha256'])
        for alias in p['sourceAliases'][-8:]:
            n=alias['sourceNumber']
            self.assertEqual(alias['duplicateOf'],f'exp-013-{n:02}')
            source=R/'google_drive'/alias['sourceName']
            original=R/f'google_drive/Max_a_Gambar_kotak_berisi__13_logo-{n:02}.png'
            if source.exists() and original.exists():
                self.assertEqual(source.read_bytes(),original.read_bytes())
                self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(),alias['sourceSha256'])
        self.assertEqual(len(json.loads((R/'android-logo/app/src/main/assets/exploration/catalog.json').read_text())['reviewedEntries']),101)

class PathBatch16Test(PathBatchTest):
    batch=R/'04-desain/variasi-svg/batch-16'
    count=10
    total=129
    test_polygons_do_not_self_intersect=PathBatch05Test.test_polygons_do_not_self_intersect

    def test_progress_and_limited_audit_are_consistent(self):
        p=json.loads((self.batch/'progress.json').read_text())
        old=json.loads((R/'04-desain/variasi-svg/batch-15/progress.json').read_text())
        self.assertTrue(p['apkBuildsPaused'])
        self.assertEqual(p['newMasterCount'],10)
        self.assertEqual(p['uniqueDriveMasters'],129)
        self.assertEqual(p['driveSourcesCoveredIncludingDuplicates'],147)
        self.assertEqual(p['remainingNotProcessed'],195)
        self.assertEqual(p['progressPercent'],42.98)
        self.assertEqual(p['redrawOnlyPercent'],37.72)
        self.assertEqual(p['sourceAliases'],old['sourceAliases'])
        self.assertEqual(len(p['sourceAliases']),18)
        self.assertEqual(p['groups']['16']['redrawn'],list(range(1,10)))
        self.assertEqual(p['groups']['rasio-14']['redrawn'],[1,2,3])
        self.assertEqual(p['entries'][-1]['id'],'exp-rasio-014-03')
        previous_ids=set();previous_sources=set();known=set()
        for f in (R/'04-desain/variasi-svg').glob('batch-*/progress.json'):
            if f.parent!=self.batch:
                for e in json.loads(f.read_text())['entries']:
                    previous_ids.add(e['id']);previous_sources.add(e['sourceSha256'])
        for f in (R/'04-desain/variasi-svg').rglob('*.svg'):
            if f.parent!=self.batch:known.add(hashlib.sha256(f.read_bytes()).hexdigest())
        for e in p['entries']:
            self.assertNotIn(e['id'],previous_ids)
            self.assertNotIn(e['sourceSha256'],previous_sources)
            previous_sources.add(e['sourceSha256'])
            digest=hashlib.sha256((R/e['masterSvg']).read_bytes()).hexdigest()
            self.assertNotIn(digest,known);known.add(digest)
            source=R/'google_drive'/e['sourceName']
            if source.exists():self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(),e['sourceSha256'])
        self.assertEqual(len(json.loads((R/'android-logo/app/src/main/assets/exploration/catalog.json').read_text())['reviewedEntries']),101)

class PathBatch17Test(PathBatchTest):
    batch=R/'04-desain/variasi-svg/batch-17'
    count=10
    total=139
    test_polygons_do_not_self_intersect=PathBatch05Test.test_polygons_do_not_self_intersect

    def test_progress_and_limited_audit_are_consistent(self):
        p=json.loads((self.batch/'progress.json').read_text())
        old=json.loads((R/'04-desain/variasi-svg/batch-16/progress.json').read_text())
        self.assertTrue(p['apkBuildsPaused'])
        self.assertEqual(p['newMasterCount'],10)
        self.assertEqual(p['uniqueDriveMasters'],139)
        self.assertEqual(p['driveSourcesCoveredIncludingDuplicates'],157)
        self.assertEqual(p['remainingNotProcessed'],185)
        self.assertEqual(p['progressPercent'],45.91)
        self.assertEqual(p['redrawOnlyPercent'],40.64)
        self.assertEqual(p['sourceAliases'],old['sourceAliases'])
        self.assertEqual(len(p['sourceAliases']),18)
        self.assertEqual(p['groups']['17']['redrawn'],list(range(1,10)))
        self.assertEqual(p['groups']['rasio-14']['redrawn'],[1,2,3,4])
        self.assertEqual(p['entries'][-1]['id'],'exp-rasio-014-04')
        previous_ids=set();previous_sources=set();known=set()
        for f in (R/'04-desain/variasi-svg').glob('batch-*/progress.json'):
            if f.parent!=self.batch:
                for e in json.loads(f.read_text())['entries']:
                    previous_ids.add(e['id']);previous_sources.add(e['sourceSha256'])
        for f in (R/'04-desain/variasi-svg').rglob('*.svg'):
            if f.parent!=self.batch:known.add(hashlib.sha256(f.read_bytes()).hexdigest())
        for e in p['entries']:
            self.assertNotIn(e['id'],previous_ids)
            self.assertNotIn(e['sourceSha256'],previous_sources)
            previous_sources.add(e['sourceSha256'])
            digest=hashlib.sha256((R/e['masterSvg']).read_bytes()).hexdigest()
            self.assertNotIn(digest,known);known.add(digest)
            source=R/'google_drive'/e['sourceName']
            if source.exists():self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(),e['sourceSha256'])
        self.assertEqual(len(json.loads((R/'android-logo/app/src/main/assets/exploration/catalog.json').read_text())['reviewedEntries']),101)

class PathBatch18Test(PathBatchTest):
    batch=R/'04-desain/variasi-svg/batch-18'
    count=10
    total=149
    test_polygons_do_not_self_intersect=PathBatch05Test.test_polygons_do_not_self_intersect

    def test_progress_and_limited_audit_are_consistent(self):
        p=json.loads((self.batch/'progress.json').read_text())
        old=json.loads((R/'04-desain/variasi-svg/batch-17/progress.json').read_text())
        self.assertTrue(p['apkBuildsPaused'])
        self.assertEqual(p['newMasterCount'],10)
        self.assertEqual(p['uniqueDriveMasters'],149)
        self.assertEqual(p['driveSourcesCoveredIncludingDuplicates'],167)
        self.assertEqual(p['remainingNotProcessed'],175)
        self.assertEqual(p['progressPercent'],48.83)
        self.assertEqual(p['redrawOnlyPercent'],43.57)
        self.assertEqual(p['sourceAliases'],old['sourceAliases'])
        self.assertEqual(len(p['sourceAliases']),18)
        self.assertEqual(p['groups']['18']['redrawn'],list(range(1,10)))
        self.assertEqual(p['groups']['rasio-14']['redrawn'],[1,2,3,4,5])
        self.assertEqual(p['entries'][-1]['id'],'exp-rasio-014-05')
        previous_ids=set();previous_sources=set();known=set()
        for f in (R/'04-desain/variasi-svg').glob('batch-*/progress.json'):
            if f.parent!=self.batch:
                for e in json.loads(f.read_text())['entries']:
                    previous_ids.add(e['id']);previous_sources.add(e['sourceSha256'])
        for f in (R/'04-desain/variasi-svg').rglob('*.svg'):
            if f.parent!=self.batch:known.add(hashlib.sha256(f.read_bytes()).hexdigest())
        for e in p['entries']:
            self.assertNotIn(e['id'],previous_ids)
            self.assertNotIn(e['sourceSha256'],previous_sources)
            previous_sources.add(e['sourceSha256'])
            digest=hashlib.sha256((R/e['masterSvg']).read_bytes()).hexdigest()
            self.assertNotIn(digest,known);known.add(digest)
            source=R/'google_drive'/e['sourceName']
            if source.exists():self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(),e['sourceSha256'])
        self.assertEqual(len(json.loads((R/'android-logo/app/src/main/assets/exploration/catalog.json').read_text())['reviewedEntries']),101)

    def test_source_specific_colors_and_positive_letters(self):
        data=json.loads((self.batch/'exp-018-02.json').read_text())
        self.assertEqual(data['layers'][1]['color'],1)
        self.assertEqual(data['layers'][1]['commands'][0],['M',62,176])
        for name in ('exp-018-01','exp-rasio-014-05'):
            d=json.loads((self.batch/f'{name}.json').read_text())
            self.assertIn(2,{l['color'] for l in d['layers']})

class PathBatch19Test(PathBatchTest):
    batch=R/'04-desain/variasi-svg/batch-19'
    count=10
    total=159
    test_polygons_do_not_self_intersect=PathBatch05Test.test_polygons_do_not_self_intersect

    def test_progress_and_limited_audit_are_consistent(self):
        p=json.loads((self.batch/'progress.json').read_text())
        old=json.loads((R/'04-desain/variasi-svg/batch-18/progress.json').read_text())
        self.assertTrue(p['apkBuildsPaused'])
        self.assertEqual(p['newMasterCount'],10)
        self.assertEqual(p['uniqueDriveMasters'],159)
        self.assertEqual(p['driveSourcesCoveredIncludingDuplicates'],177)
        self.assertEqual(p['remainingNotProcessed'],165)
        self.assertEqual(p['progressPercent'],51.75)
        self.assertEqual(p['redrawOnlyPercent'],46.49)
        self.assertEqual(p['sourceAliases'],old['sourceAliases'])
        self.assertEqual(len(p['sourceAliases']),18)
        self.assertEqual(p['groups']['19']['redrawn'],list(range(1,10)))
        self.assertEqual(p['groups']['rasio-14']['redrawn'],[1,2,3,4,5,6])
        self.assertEqual(p['entries'][-1]['id'],'exp-rasio-014-06')
        previous_ids=set();previous_sources=set();known=set()
        for f in (R/'04-desain/variasi-svg').glob('batch-*/progress.json'):
            if f.parent!=self.batch:
                for e in json.loads(f.read_text())['entries']:
                    previous_ids.add(e['id']);previous_sources.add(e['sourceSha256'])
        for f in (R/'04-desain/variasi-svg').rglob('*.svg'):
            if f.parent!=self.batch:known.add(hashlib.sha256(f.read_bytes()).hexdigest())
        for e in p['entries']:
            self.assertNotIn(e['id'],previous_ids)
            self.assertNotIn(e['sourceSha256'],previous_sources)
            previous_sources.add(e['sourceSha256'])
            digest=hashlib.sha256((R/e['masterSvg']).read_bytes()).hexdigest()
            self.assertNotIn(digest,known);known.add(digest)
            source=R/'google_drive'/e['sourceName']
            if source.exists():self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(),e['sourceSha256'])
        self.assertEqual(len(json.loads((R/'android-logo/app/src/main/assets/exploration/catalog.json').read_text())['reviewedEntries']),101)

class PathBatch20Test(PathBatchTest):
    batch=R/'04-desain/variasi-svg/batch-20'
    count=10
    total=169
    test_polygons_do_not_self_intersect=PathBatch05Test.test_polygons_do_not_self_intersect

    def test_progress_and_limited_audit_are_consistent(self):
        p=json.loads((self.batch/'progress.json').read_text())
        old=json.loads((R/'04-desain/variasi-svg/batch-19/progress.json').read_text())
        self.assertTrue(p['apkBuildsPaused'])
        self.assertEqual(p['newMasterCount'],10)
        self.assertEqual(p['uniqueDriveMasters'],169)
        self.assertEqual(p['driveSourcesCoveredIncludingDuplicates'],187)
        self.assertEqual(p['remainingNotProcessed'],155)
        self.assertEqual(p['progressPercent'],54.68)
        self.assertEqual(p['redrawOnlyPercent'],49.42)
        self.assertEqual(p['sourceAliases'],old['sourceAliases'])
        self.assertEqual(len(p['sourceAliases']),18)
        self.assertEqual(p['groups']['rasio-15']['redrawn'],list(range(1,8)))
        self.assertEqual(p['groups']['rasio-14']['redrawn'],list(range(1,10)))
        self.assertEqual(p['entries'][-1]['id'],'exp-rasio-015-07')
        previous_ids=set();previous_sources=set();known=set()
        for f in (R/'04-desain/variasi-svg').glob('batch-*/progress.json'):
            if f.parent!=self.batch:
                for e in json.loads(f.read_text())['entries']:
                    previous_ids.add(e['id']);previous_sources.add(e['sourceSha256'])
        for f in (R/'04-desain/variasi-svg').rglob('*.svg'):
            if f.parent!=self.batch:known.add(hashlib.sha256(f.read_bytes()).hexdigest())
        for e in p['entries']:
            self.assertNotIn(e['id'],previous_ids)
            self.assertNotIn(e['sourceSha256'],previous_sources)
            previous_sources.add(e['sourceSha256'])
            digest=hashlib.sha256((R/e['masterSvg']).read_bytes()).hexdigest()
            self.assertNotIn(digest,known);known.add(digest)
            source=R/'google_drive'/e['sourceName']
            if source.exists():self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(),e['sourceSha256'])
        self.assertEqual(len(json.loads((R/'android-logo/app/src/main/assets/exploration/catalog.json').read_text())['reviewedEntries']),101)

    def test_nameplate_holes_and_positive_white_letters(self):
        plate=json.loads((self.batch/'exp-rasio-014-08.json').read_text())
        self.assertEqual(plate['layers'][0]['color'],0)
        self.assertEqual(sum(c[0]=='M' for c in plate['layers'][0]['commands']),6)
        self.assertEqual(sum(c[0]=='Z' for c in plate['layers'][0]['commands']),6)
        self.assertNotIn(2,{l['color'] for l in plate['layers']})
        slab=json.loads((self.batch/'exp-rasio-015-03.json').read_text())
        self.assertEqual(slab['layers'][-1]['color'],2)
        self.assertEqual(sum(c[0]=='M' for c in slab['layers'][-1]['commands']),3)

class PathBatch21Test(PathBatchTest):
    batch=R/'04-desain/variasi-svg/batch-21'
    count=10
    total=179
    test_polygons_do_not_self_intersect=PathBatch05Test.test_polygons_do_not_self_intersect

    def test_progress_and_limited_audit_are_consistent(self):
        p=json.loads((self.batch/'progress.json').read_text())
        old=json.loads((R/'04-desain/variasi-svg/batch-20/progress.json').read_text())
        self.assertTrue(p['apkBuildsPaused'])
        self.assertEqual(p['newMasterCount'],10)
        self.assertEqual(p['uniqueDriveMasters'],179)
        self.assertEqual(p['driveSourcesCoveredIncludingDuplicates'],197)
        self.assertEqual(p['remainingNotProcessed'],145)
        self.assertEqual(p['progressPercent'],57.6)
        self.assertEqual(p['redrawOnlyPercent'],52.34)
        self.assertEqual(p['sourceAliases'],old['sourceAliases'])
        self.assertEqual(len(p['sourceAliases']),18)
        self.assertEqual(p['groups']['rasio-15']['redrawn'],list(range(1,10)))
        self.assertEqual(p['groups']['rasio-16']['redrawn'],list(range(1,9)))
        self.assertEqual(p['entries'][-1]['id'],'exp-rasio-016-08')
        previous_ids=set();previous_sources=set();known=set()
        for f in (R/'04-desain/variasi-svg').glob('batch-*/progress.json'):
            if f.parent!=self.batch:
                for e in json.loads(f.read_text())['entries']:
                    previous_ids.add(e['id']);previous_sources.add(e['sourceSha256'])
        for f in (R/'04-desain/variasi-svg').rglob('*.svg'):
            if f.parent!=self.batch:known.add(hashlib.sha256(f.read_bytes()).hexdigest())
        for e in p['entries']:
            self.assertNotIn(e['id'],previous_ids)
            self.assertNotIn(e['sourceSha256'],previous_sources)
            previous_sources.add(e['sourceSha256'])
            digest=hashlib.sha256((R/e['masterSvg']).read_bytes()).hexdigest()
            self.assertNotIn(digest,known);known.add(digest)
            source=R/'google_drive'/e['sourceName']
            if source.exists():self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(),e['sourceSha256'])
        self.assertEqual(len(json.loads((R/'android-logo/app/src/main/assets/exploration/catalog.json').read_text())['reviewedEntries']),101)

    def test_source_specific_colors_and_split_c(self):
        diamond=json.loads((self.batch/'exp-rasio-016-01.json').read_text())
        self.assertEqual(diamond['layers'][-1]['color'],2)
        self.assertEqual(sum(c[0]=='M' for c in diamond['layers'][-1]['commands']),3)
        upright=json.loads((self.batch/'exp-rasio-016-04.json').read_text())
        self.assertEqual(upright['layers'][0]['color'],0)
        split=json.loads((self.batch/'exp-rasio-016-07.json').read_text())
        self.assertEqual(sum(c[0]=='M' for c in split['layers'][1]['commands']),7)

class PathBatch22Test(PathBatchTest):
    batch=R/'04-desain/variasi-svg/batch-22'
    count=10
    total=189
    test_polygons_do_not_self_intersect=PathBatch05Test.test_polygons_do_not_self_intersect

    def test_progress_and_limited_audit_are_consistent(self):
        p=json.loads((self.batch/'progress.json').read_text())
        old=json.loads((R/'04-desain/variasi-svg/batch-21/progress.json').read_text())
        self.assertTrue(p['apkBuildsPaused'])
        self.assertEqual(p['newMasterCount'],10)
        self.assertEqual(p['uniqueDriveMasters'],189)
        self.assertEqual(p['driveSourcesCoveredIncludingDuplicates'],207)
        self.assertEqual(p['remainingNotProcessed'],135)
        self.assertEqual(p['progressPercent'],60.53)
        self.assertEqual(p['redrawOnlyPercent'],55.26)
        self.assertEqual(p['sourceAliases'],old['sourceAliases'])
        self.assertEqual(len(p['sourceAliases']),18)
        self.assertEqual(p['groups']['rasio-17']['redrawn'],list(range(1,10)))
        self.assertEqual(p['groups']['rasio-16']['redrawn'],list(range(1,10)))
        self.assertEqual(p['entries'][-1]['id'],'exp-rasio-017-09')
        previous_ids=set();previous_sources=set();known=set()
        for f in (R/'04-desain/variasi-svg').glob('batch-*/progress.json'):
            if f.parent!=self.batch:
                for e in json.loads(f.read_text())['entries']:
                    previous_ids.add(e['id']);previous_sources.add(e['sourceSha256'])
        for f in (R/'04-desain/variasi-svg').rglob('*.svg'):
            if f.parent!=self.batch:known.add(hashlib.sha256(f.read_bytes()).hexdigest())
        for e in p['entries']:
            self.assertNotIn(e['id'],previous_ids)
            self.assertNotIn(e['sourceSha256'],previous_sources)
            previous_sources.add(e['sourceSha256'])
            digest=hashlib.sha256((R/e['masterSvg']).read_bytes()).hexdigest()
            self.assertNotIn(digest,known);known.add(digest)
            source=R/'google_drive'/e['sourceName']
            if source.exists():self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(),e['sourceSha256'])
        self.assertEqual(len(json.loads((R/'android-logo/app/src/main/assets/exploration/catalog.json').read_text())['reviewedEntries']),101)

    def test_positive_letters_and_transparent_frame(self):
        diamond=json.loads((self.batch/'exp-rasio-017-01.json').read_text())
        self.assertEqual(diamond['layers'][-1]['color'],2)
        self.assertEqual(sum(c[0]=='M' for c in diamond['layers'][-1]['commands']),3)
        frame=json.loads((self.batch/'exp-rasio-017-08.json').read_text())
        self.assertEqual(frame['layers'][0]['color'],0)
        self.assertEqual(sum(c[0]=='M' for c in frame['layers'][0]['commands']),2)
        self.assertNotIn(2,{l['color'] for l in frame['layers']})

class PathBatch23Test(PathBatchTest):
    batch=R/'04-desain/variasi-svg/batch-23'
    count=10
    total=199
    test_polygons_do_not_self_intersect=PathBatch05Test.test_polygons_do_not_self_intersect

    def test_progress_and_limited_audit_are_consistent(self):
        p=json.loads((self.batch/'progress.json').read_text())
        old=json.loads((R/'04-desain/variasi-svg/batch-22/progress.json').read_text())
        self.assertTrue(p['apkBuildsPaused'])
        self.assertEqual(p['newMasterCount'],10)
        self.assertEqual(p['uniqueDriveMasters'],199)
        self.assertEqual(p['driveSourcesCoveredIncludingDuplicates'],217)
        self.assertEqual(p['remainingNotProcessed'],125)
        self.assertEqual(p['progressPercent'],63.45)
        self.assertEqual(p['redrawOnlyPercent'],58.19)
        self.assertEqual(p['sourceAliases'],old['sourceAliases'])
        self.assertEqual(len(p['sourceAliases']),18)
        self.assertEqual(p['groups']['rasio-18']['redrawn'],list(range(1,10)))
        self.assertEqual(p['groups']['rasio-1']['redrawn'],[1])
        self.assertEqual(p['entries'][-1]['id'],'exp-rasio-001-01')
        previous_ids=set();previous_sources=set();known=set()
        for f in (R/'04-desain/variasi-svg').glob('batch-*/progress.json'):
            if f.parent!=self.batch:
                for e in json.loads(f.read_text())['entries']:
                    previous_ids.add(e['id']);previous_sources.add(e['sourceSha256'])
        for f in (R/'04-desain/variasi-svg').rglob('*.svg'):
            if f.parent!=self.batch:known.add(hashlib.sha256(f.read_bytes()).hexdigest())
        for e in p['entries']:
            self.assertNotIn(e['id'],previous_ids)
            self.assertNotIn(e['sourceSha256'],previous_sources)
            previous_sources.add(e['sourceSha256'])
            digest=hashlib.sha256((R/e['masterSvg']).read_bytes()).hexdigest()
            self.assertNotIn(digest,known);known.add(digest)
            source=R/'google_drive'/e['sourceName']
            if source.exists():self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(),e['sourceSha256'])
        self.assertEqual(len(json.loads((R/'android-logo/app/src/main/assets/exploration/catalog.json').read_text())['reviewedEntries']),101)

    def test_mounting_holes_and_positive_dots(self):
        plate=json.loads((self.batch/'exp-rasio-018-06.json').read_text())
        self.assertEqual(sum(c[0]=='M' for c in plate['layers'][0]['commands']),10)
        self.assertNotIn(2,{l['color'] for l in plate['layers']})
        diamond=json.loads((self.batch/'exp-rasio-018-09.json').read_text())
        self.assertEqual(sum(c[0]=='M' for c in diamond['layers'][-1]['commands']),6)
        arch=json.loads((self.batch/'exp-rasio-018-07.json').read_text())
        self.assertEqual(max(c[2] for c in arch['layers'][0]['commands'] if c[0] in ('M','L')),225)

class PathBatch24Test(PathBatchTest):
    batch=R/'04-desain/variasi-svg/batch-24'
    count=10
    total=209
    test_polygons_do_not_self_intersect=PathBatch05Test.test_polygons_do_not_self_intersect

    def test_progress_and_limited_audit_are_consistent(self):
        p=json.loads((self.batch/'progress.json').read_text())
        old=json.loads((R/'04-desain/variasi-svg/batch-23/progress.json').read_text())
        self.assertTrue(p['apkBuildsPaused'])
        self.assertEqual(p['newMasterCount'],10)
        self.assertEqual(p['uniqueDriveMasters'],209)
        self.assertEqual(p['driveSourcesCoveredIncludingDuplicates'],227)
        self.assertEqual(p['remainingNotProcessed'],115)
        self.assertEqual(p['progressPercent'],66.37)
        self.assertEqual(p['redrawOnlyPercent'],61.11)
        self.assertEqual(p['sourceAliases'],old['sourceAliases'])
        self.assertEqual(len(p['sourceAliases']),18)
        self.assertEqual(p['groups']['rasio-1']['redrawn'],list(range(1,10)))
        self.assertEqual(p['groups']['rasio-2']['redrawn'],[1,2])
        self.assertEqual(p['entries'][-1]['id'],'exp-rasio-002-02')
        previous_ids=set();previous_sources=set();known=set()
        for f in (R/'04-desain/variasi-svg').glob('batch-*/progress.json'):
            if f.parent!=self.batch:
                for e in json.loads(f.read_text())['entries']:
                    previous_ids.add(e['id']);previous_sources.add(e['sourceSha256'])
        for f in (R/'04-desain/variasi-svg').rglob('*.svg'):
            if f.parent!=self.batch:known.add(hashlib.sha256(f.read_bytes()).hexdigest())
        for e in p['entries']:
            self.assertNotIn(e['id'],previous_ids)
            self.assertNotIn(e['sourceSha256'],previous_sources)
            previous_sources.add(e['sourceSha256'])
            digest=hashlib.sha256((R/e['masterSvg']).read_bytes()).hexdigest()
            self.assertNotIn(digest,known);known.add(digest)
            source=R/'google_drive'/e['sourceName']
            if source.exists():self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(),e['sourceSha256'])
        self.assertEqual(len(json.loads((R/'android-logo/app/src/main/assets/exploration/catalog.json').read_text())['reviewedEntries']),101)

    def test_mounting_holes_and_white_letters(self):
        plate=json.loads((self.batch/'exp-rasio-001-06.json').read_text())
        self.assertEqual(sum(c[0]=='M' for c in plate['layers'][1]['commands']),7)
        self.assertEqual(plate['layers'][-1]['color'],2)
        self.assertEqual(sum(c[0]=='M' for c in plate['layers'][-1]['commands']),3)
        hexagon=json.loads((self.batch/'exp-rasio-002-02.json').read_text())
        self.assertEqual([l['color'] for l in hexagon['layers']],[1,0])

class PathBatch25Test(PathBatchTest):
    batch=R/'04-desain/variasi-svg/batch-25'
    count=10
    total=219
    test_polygons_do_not_self_intersect=PathBatch05Test.test_polygons_do_not_self_intersect

    def test_progress_and_limited_audit_are_consistent(self):
        p=json.loads((self.batch/'progress.json').read_text())
        old=json.loads((R/'04-desain/variasi-svg/batch-24/progress.json').read_text())
        self.assertTrue(p['apkBuildsPaused'])
        self.assertEqual(p['newMasterCount'],10)
        self.assertEqual(p['uniqueDriveMasters'],219)
        self.assertEqual(p['driveSourcesCoveredIncludingDuplicates'],237)
        self.assertEqual(p['remainingNotProcessed'],105)
        self.assertEqual(p['progressPercent'],69.30)
        self.assertEqual(p['redrawOnlyPercent'],64.04)
        self.assertEqual(p['sourceAliases'],old['sourceAliases'])
        self.assertEqual(len(p['sourceAliases']),18)
        self.assertEqual(p['groups']['rasio-2']['redrawn'],list(range(1,10)))
        self.assertEqual(p['groups']['rasio-3']['redrawn'],[1,2,3])
        self.assertEqual(p['entries'][-1]['id'],'exp-rasio-003-03')
        previous_ids=set();previous_sources=set();known=set()
        for f in (R/'04-desain/variasi-svg').glob('batch-*/progress.json'):
            if f.parent!=self.batch:
                for e in json.loads(f.read_text())['entries']:
                    previous_ids.add(e['id']);previous_sources.add(e['sourceSha256'])
        for f in (R/'04-desain/variasi-svg').rglob('*.svg'):
            if f.parent!=self.batch:known.add(hashlib.sha256(f.read_bytes()).hexdigest())
        for e in p['entries']:
            self.assertNotIn(e['id'],previous_ids)
            self.assertNotIn(e['sourceSha256'],previous_sources)
            previous_sources.add(e['sourceSha256'])
            digest=hashlib.sha256((R/e['masterSvg']).read_bytes()).hexdigest()
            self.assertNotIn(digest,known);known.add(digest)
            source=R/'google_drive'/e['sourceName']
            if source.exists():self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(),e['sourceSha256'])
        self.assertEqual(len(json.loads((R/'android-logo/app/src/main/assets/exploration/catalog.json').read_text())['reviewedEntries']),101)

    def test_positive_white_letters_and_source_colors(self):
        for name in ('exp-rasio-003-01','exp-rasio-003-03'):
            plate=json.loads((self.batch/(name+'.json')).read_text())
            self.assertEqual(plate['layers'][-1]['color'],2)
            self.assertEqual(sum(c[0]=='M' for c in plate['layers'][-1]['commands']),3)
        plate=json.loads((self.batch/'exp-rasio-002-08.json').read_text())
        self.assertEqual([l['color'] for l in plate['layers']],[0,1])

if __name__=='__main__':unittest.main()
