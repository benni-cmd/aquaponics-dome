"""Querschnitt Wand-Beet-Tisch-Weg fuer die Aussentisch-Varianten aussen (3 Rinnen) und aussen4 (4 Rinnen), W24. Reines PIL-Schemabild aus tisch_geom + Kuppelhaut-Feldebenen (kein CAD-Lauf).
Horizontal: Apothem ap (mm, innen links, Domwand rechts), vertikal: Z. Tisch im Schnitt durch die Tischmitte (x = 0); die Kuppelhaut ist im Schnitt durch das Rinnenende der aeussersten Reihe (x = Ende, Sektor 6) gezeichnet.
Aufruf: python scripts/workshop/render_aussen4_schnitt.py"""
import os, sys, math
sys.path.insert(0, os.path.dirname(__file__))
import sc
import tisch_geom as TG
import check_nft_fit as C
from PIL import Image, ImageDraw, ImageFont

OUT = os.path.join(sc.ROOT, "renders", "components", "nft_passung")
os.makedirs(OUT, exist_ok=True)
p, d = sc.load_params("nft_tisch")
planes = C.dome_planes()
FONT = ImageFont.load_default()
AP0, AP1, Z1 = 4150.0, 5800.0, 2300.0
SC = 0.5                                                      # gleicher Massstab in ap und z (px/mm)
W, H, M = int((AP1 - AP0) * SC) + 80, int(Z1 * SC) + 80, 40
sx = SC
X = lambda ap: M + (ap - AP0) * sx
Y = lambda z: H - M - z * sx

def haut_z(ap, az, x_t):
    """Obere Grenze z der Kuppelhaut (Minimum ueber die Feldebenen mit n_z > 0) an Apothem ap, tangentialer Lage x_t."""
    a = math.radians(az)
    u, t = (math.cos(a), math.sin(a)), (-math.sin(a), math.cos(a))
    px, py = ap * u[0] + x_t * t[0], ap * u[1] + x_t * t[1]
    zs = [(dd - n[0] * px - n[1] * py) / n[2] for n, dd in planes if n[2] > 1e-6]
    return min(zs)

def panel(variant, G, row_hdr):
    im = Image.new("RGB", (W, H), "white")
    dr = ImageDraw.Draw(im)
    apc = G["apc"]
    az = C.AZ0 + 36.0 * 6
    # Kuppelhaut bei Rinnenende der aeussersten Reihe
    r0 = max(G["rows"], key=lambda r: r["ap"])
    xe = r0["xc"] - r0["L"] / 2 - TG.E_IN
    pts = []
    ap = AP0
    while ap <= AP1:
        z = haut_z(ap, az, xe)
        if z < Z1 * 1.6:
            pts.append((X(ap), Y(z)))
        ap += 10
    if len(pts) > 1:
        dr.line(pts, fill=(200, 60, 40), width=3)
    dr.text((X(AP0) + 8, Y(2200)), f"Kuppelhaut im Schnitt x = {xe:.0f} (Rinnenende R1); die Beine stehen bei kleinerem |x|, nicht im Schnitt der Haut", fill=(200, 60, 40), font=FONT)
    # Domwand Apothem 5706, Boden
    dr.line([(X(5706), Y(0)), (X(5706), Y(2300))], fill=(120, 120, 120), width=2)
    dr.text((X(5706) - 70, Y(2150)), "Domwand 5706", fill=(90, 90, 90), font=FONT)
    dr.line([(X(AP0), Y(0)), (X(AP1), Y(0))], fill=(60, 60, 60), width=2)
    # Beet 800 x 637
    bw = G["bed_w"]
    dr.rectangle([X(apc - bw / 2), Y(637), X(apc + bw / 2), Y(0)], outline=(60, 120, 60), width=2)
    dr.text((X(apc) - 30, Y(300)), f"Beet {bw:.0f}", fill=(60, 120, 60), font=FONT)
    # Beine + Fussplatten + Holm
    fp, lc = p["foot_plate"], p["leg_clearance"]
    for s in (-1, 1):
        yl = s * G["yl"]
        apl = apc - yl
        dr.rectangle([X(apl - fp / 2), Y(5), X(apl + fp / 2), Y(0)], fill=(90, 90, 90))
        dr.rectangle([X(apl - 20), Y(G["zc"] - 65), X(apl + 20), Y(5)], outline=(90, 90, 90), width=2)
    dr.rectangle([X(apc - G["yl"]), Y(G["zc"] - 65), X(apc + G["yl"]), Y(G["zc"] - 125)], outline=(90, 90, 90), width=2)
    # Rinnen 130 x 100
    for r in G["rows"]:
        a = apc - r["y"]
        dr.rectangle([X(a - 65), Y(G["zc"] + 100), X(a + 65), Y(G["zc"])], outline=(30, 90, 170), width=2)
        dr.text((X(a) - 8, Y(G["zc"] + 150)), f"R{r['k'] + 1}", fill=(30, 90, 170), font=FONT)
        dr.text((X(a) - 22, Y(G["zc"] + 220)), f"{r['ap']:.0f}", fill=(30, 90, 170), font=FONT)
    # Laufwege / Masse
    Gm = TG.geometry("mitte", p, d["typen"]["mitte"])
    half = lambda g: g["bed_w"] / 2 + lc + fp
    lb0, lb1 = Gm["apc"] + half(Gm), apc - half(G)
    dr.line([(X(lb0), Y(60)), (X(lb1), Y(60))], fill=(0, 0, 0), width=3)
    dr.text((X(AP0) + 10, Y(110)), f"Laufweg B {lb1 - lb0:.1f} (ab Innenportal {lb0:.0f})", fill=(0, 0, 0), font=FONT)
    wl0, wl1 = apc + half(G), 5706.0
    dr.line([(X(wl0), Y(60)), (X(wl1), Y(60))], fill=(0, 0, 0), width=3)
    dr.text((X(wl0) + 10, Y(110)), f"Wandluft {wl1 - wl0:.0f}", fill=(0, 0, 0), font=FONT)
    dr.text((M, 8), f"W24 {variant}: {G['n']} Rinnen, Abstand {G['rp']:.0f}, Versatz {G['ymid']:.0f}, Rinnenkante {max(abs(r['y']) for r in G['rows']) + 65:.0f} (Bein {G['yl'] - p['leg_w'] / 2:.0f}), Toepfe/Tisch {sum(r['n_holes'] for r in G['rows'])}", fill=(0, 0, 0), font=FONT)
    return im

out = Image.new("RGB", (2 * W + 4, H), "white")
for k, v in enumerate(("aussen", "aussen4")):
    G = TG.geometry("aussen", p, d["typen"][v])
    out.paste(panel(v, G, None), (k * (W + 4), 0))
fn = os.path.join(OUT, "aussen4-querschnitt.png")
out.save(fn)
print(fn)
