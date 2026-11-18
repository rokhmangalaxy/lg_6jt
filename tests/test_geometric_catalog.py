import json
from pathlib import Path
import unittest
R=Path(__file__).resolve().parents[1]
class CatalogTest(unittest.TestCase):
    def test_all_four_are_manual_closed_straight_paths(self):
        files=list((R/'android-logo/logo-assets').glob('*.json'))
        self.assertEqual(len(files),4)
        for file in files:
            d=json.loads(file.read_text())
            self.assertEqual(d['construction'],'manual-geometric-v1')
            for layer in d['layers']:
                self.assertIn(layer['color'],range(3))
                commands=layer['commands']
                self.assertEqual({c[0] for c in commands},{'M','L','Z'})
                self.assertEqual(commands[0][0],'M');self.assertEqual(commands[-1][0],'Z')
                self.assertEqual(sum(c[0]=='M' for c in commands),sum(c[0]=='Z' for c in commands))
                for c in commands:
                    if len(c)>1:
                        self.assertTrue(0<=c[1]<=d['width'])
                        self.assertTrue(0<=c[2]<=d['height'])
    def test_approved_logo04_geometry_unchanged(self):
        original=json.loads((R/'04-desain/redraw-geometris-04/mcm-04-geometris.json').read_text())
        app=json.loads((R/'android-logo/logo-assets/client-logo-04.json').read_text())
        self.assertEqual(original['layers'],app['layers'])
