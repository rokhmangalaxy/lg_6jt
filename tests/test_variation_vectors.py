from pathlib import Path
import unittest,json,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1]
class VariationVectorsTest(unittest.TestCase):
    def test_all_variations_have_true_manual_paths(self):
        folder=R/'android-logo/app/src/main/assets/exploration'
        entries=json.loads((folder/'catalog.json').read_text())['reviewedEntries']
        for entry in entries:
            self.assertEqual(entry['format'],'manual-vector')
            data=json.loads((folder/(entry['id']+'.json')).read_text())
            self.assertEqual(data['construction'],'manual-geometric-v1')
            svg=ET.parse(R/entry['masterSvg']).getroot()
            self.assertFalse(svg.findall('.//{http://www.w3.org/2000/svg}image'))
            self.assertTrue(svg.findall('.//{http://www.w3.org/2000/svg}path'))
            for layer in data['layers']:
                self.assertEqual({c[0] for c in layer['commands']},{'M','L','Z'})
