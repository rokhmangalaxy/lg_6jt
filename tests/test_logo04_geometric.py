"""Run: python -m unittest discover -s tests -p 'test_logo04_geometric.py'."""
from pathlib import Path
import json
import re
import struct
import unittest
import xml.etree.ElementTree as ET

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'04-desain/redraw-geometris-04'

class GeometricLogo04Test(unittest.TestCase):
    def setUp(self):
        self.geometry=json.loads((OUT/'konstruksi.json').read_text())
        self.svg=ET.parse(OUT/'mcm-04-geometris.svg').getroot()
    def test_svg_is_font_free_straight_geometry(self):
        ns='{http://www.w3.org/2000/svg}'
        paths=self.svg.findall(ns+'path')
        self.assertEqual(len(paths),1)
        self.assertEqual(paths[0].get('fill-rule'),'evenodd')
        self.assertEqual(paths[0].get('fill'),'#DC2626')
        d=paths[0].get('d')
        self.assertEqual(set(re.findall('[A-Za-z]',d)),{'M','L','Z'})
        self.assertEqual(d.count('M'),4)
        self.assertEqual(d.count('Z'),4)
        self.assertFalse(self.svg.findall('.//'+ns+'text'))
        self.assertFalse(self.svg.findall('.//'+ns+'image'))
    def test_m_letters_are_exact_mirrors(self):
        self.assertEqual([[340-x,y] for x,y in self.geometry['mLeft']],self.geometry['mRight'])
    def test_four_sided_diamond_and_holes_inside(self):
        self.assertEqual(self.geometry['diamond'],[[170,32],[308,150],[170,268],[32,150]])
        for key in ('mLeft','c','mRight'):
            for x,y in self.geometry[key]:
                self.assertLess(abs(x-170)/138+abs(y-150)/118,1)
    def test_native_candidate_matches_master_dimensions(self):
        data=json.loads((OUT/'mcm-04-geometris.json').read_text())
        self.assertEqual([data['width'],data['height']],[340,300])
        commands=data['layers'][0]['commands']
        self.assertEqual(sum(c[0]=='M' for c in commands),4)
        self.assertEqual(sum(c[0]=='Z' for c in commands),4)
        self.assertEqual({c[0] for c in commands},{'M','L','Z'})
    def test_png_exports_have_requested_width(self):
        for name in ('mcm-04-geometris-putih.png','mcm-04-geometris-transparan.png'):
            data=(OUT/name).read_bytes()
            self.assertEqual(data[:8],b'\x89PNG\r\n\x1a\n')
            width,height=struct.unpack('>II',data[16:24])
            self.assertEqual(width,2400)
            self.assertAlmostEqual(width/height,340/300,places=3)

if __name__=='__main__':unittest.main()
