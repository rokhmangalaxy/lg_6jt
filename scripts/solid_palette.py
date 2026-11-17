"""Normalize concept rasters to the three-color working palette.
Run with Pillow and NumPy installed. Reads original PNGs; writes solid/.
"""
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1] / '03-konsep'
OUT = ROOT / 'solid'
OUT.mkdir(exist_ok=True)
NAVY = (23, 50, 87)
RED = (220, 38, 38)
WHITE = (255, 255, 255)
for src in sorted(ROOT.glob('variasi-*.png')):
    a = np.asarray(Image.open(src).convert('RGB')).astype(int)
    # Classify hue rather than nearest RGB: all blues and shadows share navy.
    light = a.min(axis=2) > 175
    red = (a[:,:,0] > a[:,:,1] * 1.35) & (a[:,:,0] > a[:,:,2] * 1.25) & ~light
    out = np.empty(a.shape, dtype=np.uint8)
    out[:] = NAVY
    out[light] = WHITE
    out[red] = RED
    im = Image.fromarray(out)
    if src.name.startswith('variasi-05'):
        # Frame is separate from the lettering: recolor its connected component.
        x = im.width // 2
        ys = np.flatnonzero(np.all(out[:,x,:] == NAVY, axis=1))
        ImageDraw.floodfill(im, (x, int(ys[0])), RED, thresh=0)
    colors = set(map(tuple, np.asarray(im).reshape(-1, 3)))
    assert colors == {NAVY, RED, WHITE}, (src.name, colors)
    im.save(OUT / src.name)
    print(src.name, 'OK: exactly 3 solid colors')
