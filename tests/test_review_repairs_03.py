import json,unittest
from pathlib import Path
from test_path_batches import PathBatch05Test
R=Path(__file__).resolve().parents[1]
class ReviewRepairs03Test(unittest.TestCase):
    batch=R/'04-desain/perbaikan-review/putaran-03'
    test_no_self_intersections=PathBatch05Test.test_polygons_do_not_self_intersect
    def load(self,key):return json.loads((self.batch/f'{key}.json').read_text())
    def test_progress(self):
        p=json.loads((self.batch/'review.json').read_text())
        self.assertEqual(len(p['records']),29)
        self.assertEqual(sum(r['status']=='corrected-awaiting-visual-review' for r in p['records']),23)
        self.assertEqual([r['variation'] for r in p['records'] if r['status']=='pending-source-comparison'],[115,169,205,304,313,322])
        self.assertFalse(p['applicationMappingApplied']);self.assertFalse(p['apkBuilt'])
    def test_contours_bounded(self):
        for f in self.batch.glob('exp-*.json'):
            d=json.loads(f.read_text())
            for layer in d['layers']:
                for c in layer['commands']:
                    self.assertIn(c[0],['M','L','Z'])
                    if len(c)==3:
                        self.assertTrue(0<=c[1]<=d['width'],(f,c))
                        self.assertTrue(0<=c[2]<=d['height'],(f,c))
    def test_center_triangle(self):
        d=self.load('exp-005-07')
        self.assertEqual(d['layers'][0]['commands'][2],['L',207,312])
    def test_bottom_band_clearance(self):
        d=self.load('exp-rasio-011-09');c=d['layers'][1]['commands'];band=[]
        for command in c:
            if command[0]=='Z':break
            band.append(command)
        self.assertEqual(min(c[2] for c in band),168)
        self.assertEqual(d['height'],215)
