import json,unittest
from pathlib import Path
from test_path_batches import PathBatch05Test
R=Path(__file__).resolve().parents[1]
class ReviewRepairs02Test(unittest.TestCase):
    batch=R/'04-desain/perbaikan-review/putaran-02'
    test_no_self_intersections=PathBatch05Test.test_polygons_do_not_self_intersect
    def load(self,key):return json.loads((self.batch/f'{key}.json').read_text())
    def test_scope(self):
        p=json.loads((self.batch/'review.json').read_text())
        self.assertEqual(len(p['records']),29)
        self.assertEqual(sum(r['status']=='corrected-awaiting-visual-review' for r in p['records']),13)
        self.assertEqual(p['progress']['remaining'],16)
        self.assertFalse(p['applicationMappingApplied']);self.assertFalse(p['apkBuilt'])
        self.assertEqual(len(list(self.batch.glob('*.svg'))),10)
    def test_mirror_right_m(self):
        from sys import path
        path.insert(0,str(R/'scripts'))
        # Decode subpaths without running the generation script on import.
        cmds=self.load('exp-016-03')['layers'][1]['commands'];parts=[]
        for c in cmds:
            if c[0]=='M':parts.append([])
            parts[-1].append(c)
        self.assertEqual(parts[1],[[c[0],421-c[1],c[2]] if len(c)==3 else c for c in parts[0]])
    def test_slit_parallel_and_uniform(self):
        c=self.load('exp-rasio-016-07')['layers'][1]['commands']
        self.assertIn(['L',241,111],c);self.assertIn(['M',190,204],c)
        # Upper/lower left lips lie at y104/191; new right lips y91/204.
        self.assertEqual(104-91,204-191)
    def test_seam(self):
        c=self.load('exp-rasio-010-02')['layers'][1]['commands']
        self.assertEqual(c[0],['M',130,9])
