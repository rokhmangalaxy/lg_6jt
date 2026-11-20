"""Design-only checks. No Android/Gradle/APK invocation."""
from pathlib import Path
import hashlib
import json
import re
import unittest
import xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1]
B=R/'04-desain/variasi-svg/batch-03'
class PathBatchTest(unittest.TestCase):
    def test_ten_manual_masters_match_native_paths(self):
        entries=json.loads((B/'progress.json').read_text())['entries']
        self.assertEqual(len(entries),10)
        self.assertEqual(len({e['id'] for e in entries}),10)
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
        progress=json.loads((B/'progress.json').read_text())
        self.assertTrue(progress['apkBuildsPaused'])
        self.assertEqual(progress['driveSourcesWithMasters'],15)
        self.assertEqual(progress['remainingNotProcessed']+progress['driveSourcesWithMasters'],342)
        self.assertEqual(progress['groups']['1']['pending'],[])
        self.assertEqual(progress['groups']['2']['pending'],[7,8,9])
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
if __name__=='__main__':unittest.main()
