import json,unittest
from pathlib import Path
from test_path_batches import PathBatch05Test
R=Path(__file__).resolve().parents[1]
class ReviewRepairsTest(unittest.TestCase):
    batch=R/'04-desain/perbaikan-review/putaran-01'
    test_no_self_intersections=PathBatch05Test.test_polygons_do_not_self_intersect
    def test_review_scope_and_changes(self):
        p=json.loads((self.batch/'review.json').read_text())
        self.assertEqual(len(p['records']),29)
        self.assertEqual(len({e['id'] for e in p['records']}),29)
        self.assertFalse(p['applicationMappingApplied'])
        self.assertEqual(sum(e['status']=='corrected-awaiting-visual-review' for e in p['records']),3)
        self.assertEqual(p['consolidationCandidates'][0]['members'],[115,169,205])
        self.assertEqual(p['consolidationCandidates'][1]['members'],[304,313,322])
        a=json.loads((self.batch/'exp-005-02.json').read_text())
        self.assertEqual(a['layers'][1]['commands'][0],['M',192,9])
        a=json.loads((self.batch/'exp-005-08.json').read_text())
        self.assertEqual(a['layers'][1]['commands'][4:6],[['L',152,292],['L',145,292]])
