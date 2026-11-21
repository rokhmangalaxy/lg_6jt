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
