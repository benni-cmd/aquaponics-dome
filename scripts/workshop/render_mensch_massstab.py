"""Seitenansicht der Menschenfigur mit Massstab (W29): aufrecht + messen + arbeiten nebeneinander, Massstabsbalken 1800 mm aus der Pixelhoehe der aufrechten Figur (Scheitel Z 1800, Fuss Z 0).
Aufruf: python scripts/workshop/render_mensch_massstab.py   (nach mensch.py --render)"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
from PIL import Image, ImageDraw, ImageFont

rd = os.path.join(sc.ROOT, "renders", "components", "mensch_referenz")
out = os.path.join(rd, "mensch_referenz-massstab.png")
files = [os.path.join(rd, f"mensch_referenz_{t}-seite.png") for t in ("aufrecht", "messen", "arbeiten")]
if not os.path.exists(files[0]):
    sc.snapshot(os.path.join(sc.ROOT, "designs", "components", "mensch_referenz.sc"), files[0], [0, 150, 900], 1.5708, 0.0, 4200, w=800, h=900)
ims = [Image.open(f).convert("RGB") for f in files]
def rows(im):
    px = im.load(); w, h = im.size
    bg = lambda y: px[5, y]
    ys = [y for y in range(h) if any(sum(abs(px[x, y][i] - bg(y)[i]) for i in range(3)) > 60 for x in range(0, w, 2))]
    return min(ys), max(ys)
y0, y1 = rows(ims[0])
pxmm = (y1 - y0) / 1800.0
W, H = sum(i.size[0] for i in ims) + 80, ims[0].size[1]
canvas = Image.new("RGB", (W, H), "white")
x = 80
for im in ims:
    canvas.paste(im, (x, 0)); x += im.size[0]
d = ImageDraw.Draw(canvas)
f = ImageFont.load_default()
d.line([(40, y0), (40, y1)], fill=(0, 0, 0), width=3)
for z in range(0, 1801, 300):
    yy = y1 - z * pxmm
    d.line([(30, yy), (50, yy)], fill=(0, 0, 0), width=2)
    d.text((2, yy - 5), f"{z}", fill=(0, 0, 0), font=f)
d.text((60, 10), "Massstab 1800 mm (aufrecht: Scheitel 1800, Fuss 0)   aufrecht | messen | arbeiten", fill=(0, 0, 0), font=f)
canvas.save(out)
print(out, round(pxmm, 4), "px/mm")
