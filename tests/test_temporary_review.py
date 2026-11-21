from pathlib import Path
import json, unittest
R=Path(__file__).resolve().parents[1]
class TemporaryReviewTest(unittest.TestCase):
    def test_offline_pairs_and_stable_ids(self):
        folder=R/'android-logo/app/src/main/assets/temporary-review'
        rows=json.loads((folder/'index.json').read_text())
        self.assertEqual(len(rows),324)
        self.assertEqual(len({r['id'] for r in rows}),324)
        audit=json.loads((R/'04-desain/variasi-svg/batch-36/audit_inventory.json').read_text())
        self.assertEqual({r['id'] for r in rows},{r['masterId'] for r in audit['records'] if r['kind']=='manual-master'})
        for r in rows:
            for kind in ['source','redraw']:
                self.assertTrue((folder/f"{r['id']}-{kind}.png").is_file())
    def test_isolated_local_notes_and_entrypoint(self):
        code=(R/'android-logo/app/src/main/java/id/mcm/logopreview/TemporaryReviewActivity.kt').read_text()
        for value in ['temporary-logo-review','status:$id','note:$id','putBoolean("dark"','Salin catatan','Perlu perbaikan','Sesuai']:
            self.assertIn(value,code)
        main=(R/'android-logo/app/src/main/java/id/mcm/logopreview/MainActivity.kt').read_text()
        self.assertIn('TemporaryReviewActivity::class.java',main)

    def test_repair_shortcut_baseline_matches_user_review(self):
        rows=json.loads((R/'android-logo/app/src/main/assets/temporary-review/repair-shortcuts.json').read_text())
        review=json.loads((R/'04-desain/perbaikan-review/putaran-04/review.json').read_text())
        self.assertEqual(len(rows),29)
        self.assertEqual({r['id'] for r in rows},{r['id'] for r in review['records']})
        catalog=json.loads((R/'android-logo/app/src/main/assets/exploration/catalog.json').read_text())['reviewedEntries']
        for row in rows:
            entry=next(e for e in catalog if e['id']==row['id'])
            self.assertEqual(int(entry['name'].split()[-1]),row['variation'])

    def test_corrected_vectors_and_review_previews_are_installed(self):
        applied=json.loads((R/'android-logo/app/src/main/assets/temporary-review/applied-repairs.json').read_text())
        final=json.loads((R/'04-desain/perbaikan-review/putaran-04/review.json').read_text())['records']
        self.assertEqual(len(applied),29)
        for row in applied:
            representative=next(r for r in final if r['id']==row['representative'])
            folder=R/f"04-desain/perbaikan-review/putaran-{representative.get('round',1):02}"
            assets=R/'android-logo/app/src/main/assets'
            self.assertEqual(json.loads((assets/'exploration'/f"{row['id']}.json").read_text()),json.loads((folder/f"{row['representative']}.json").read_text()))
            self.assertEqual((assets/'exploration'/f"{row['id']}.png").read_bytes(),(assets/'temporary-review'/f"{row['id']}-redraw.png").read_bytes())
