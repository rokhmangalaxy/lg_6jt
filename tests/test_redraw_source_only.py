import json,unittest
from pathlib import Path
from test_path_batches import PathBatch05Test
R=Path(__file__).resolve().parents[1]
class FreshRedrawTest(unittest.TestCase):
    batch=R/'04-desain/perbaikan-review/redraw-dari-nol'
    test_no_self_intersections=PathBatch05Test.test_polygons_do_not_self_intersect
    def test_scope_and_bounds(self):
        p=json.loads((self.batch/'progress.json').read_text())
        self.assertEqual([e['variation'] for e in p['entries']],[5,49,50,122,123,128,179,184,188,290,294,301,328])
        self.assertEqual(len(list(self.batch.glob('*.svg'))),13)
        for row in p['entries']:
            self.assertTrue(row['installed'])
            data=json.loads((self.batch/f"{row['id']}.json").read_text())
            for layer in data['layers']:
                self.assertIn(layer['color'],[0,1,2])
                for c in layer['commands']:
                    if len(c)==3:self.assertTrue(0<=c[1]<=data['width'] and 0<=c[2]<=data['height'])
    def test_generator_does_not_load_old_redraws(self):
        code=(R/'scripts/redraw_review_from_source.py').read_text()
        self.assertNotIn('-redraw.png',code)
        self.assertNotIn("e['vectorAsset']",code)
        self.assertNotIn('putaran-',code)
        page=(self.batch/'perbandingan.html').read_text()
        self.assertNotIn('Sebelum',page)

    def test_triangle_letters_clear_inner_border(self):
        data=json.loads((self.batch/'exp-005-07.json').read_text())
        for c in data['layers'][1]['commands']:
            if len(c)==3:
                x,y=c[1:]
                self.assertGreaterEqual(y,56)
                left=70+(y-56)*430/659
                self.assertGreaterEqual(x,left)
                self.assertLessEqual(x,1000-left)
    def test_center_fold_179(self):
        data=json.loads((self.batch/'exp-rasio-016-02.json').read_text())
        cmds=data['layers'][1]['commands']
        for point in [['M',500,169],['L',500,276],['L',500,520],['L',500,628]]:
            self.assertIn(point,cmds)
