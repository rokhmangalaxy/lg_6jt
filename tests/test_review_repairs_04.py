import json,unittest
from pathlib import Path
from test_path_batches import PathBatch05Test
R=Path(__file__).resolve().parents[1]
class ReviewRepairs04Test(unittest.TestCase):
    batch=R/'04-desain/perbaikan-review/putaran-04'
    test_no_self_intersections=PathBatch05Test.test_polygons_do_not_self_intersect
    def test_consolidation_scope(self):
        p=json.loads((self.batch/'review.json').read_text())
        self.assertEqual(len(p['records']),29)
        self.assertEqual(sum(r['status']=='corrected-awaiting-visual-review' for r in p['records']),23)
        grouped=[r for r in p['records'] if r['status']=='consolidated-working-master-awaiting-review']
        self.assertEqual(len(grouped),6)
        self.assertEqual({r['representative'] for r in grouped},{205,313})
        self.assertEqual(p['progress']['remaining'],0)
        self.assertFalse(p['applicationMappingApplied'])
        self.assertEqual(len(list(self.batch.glob('*.svg'))),2)
    def test_masters_have_solid_native_geometry(self):
        for key in ['exp-rasio-001-01','exp-rasio-013-01']:
            d=json.loads((self.batch/f'{key}.json').read_text())
            self.assertEqual(d['construction'],'manual-geometric-v1')
            for layer in d['layers']:
                self.assertIn(layer['color'],[0,1,2])
                for c in layer['commands']:
                    self.assertIn(c[0],['M','L','Z'])
                    if len(c)==3:self.assertTrue(0<=c[1]<=d['width'] and 0<=c[2]<=d['height'])
