"""Bildverlauf W17 (Radialbudget): ein Sektor im Tisch-KS des Aussentischs (X tangential, Y radial NACH INNEN, Ursprung = Aussenbeet-Mitte ap 4973): Aussentisch + Aussenbeet 800, Mitteltisch + Innenbeet 933, Beckenrand und Domwand als Platten.
Draufsicht mit Massen (PIL) und Querschnitt Wand-Beet-Weg. Aufruf: python scripts/workshop/render_radialbudget.py"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
import tisch_geom as TG

D = os.path.join(sc.ROOT, "designs", "components")
OUT = os.path.join(sc.ROOT, "renders", "components", "nft_passung")
os.makedirs(OUT, exist_ok=True)
p, d = sc.load_params("nft_tisch")
Ga, Gm = TG.geometry("aussen", p, d["typen"]["aussen"]), TG.geometry("mitte", p, d["typen"]["mitte"])
WALL_AP, POOL_R = 5706.0, TG.pool_outer_r()
yA = Ga["apc"]                                    # Y im Sektor-KS: Y = ap_aussen - ap
y_of = lambda ap: yA - ap
items = [("nft_tisch_aussen.sc", "Tisch_aussen", 0), ("ibc_beet_aussen_800.sc", "Beet_aussen", 0),
         ("nft_tisch_mitte.sc", "Tisch_mitte", y_of(Gm["apc"])), ("ibc_beet_innen_933.sc", "Beet_innen", y_of(Gm["apc"]))]

def base():
    b = sc.Build()
    b.add("material.create", name="Wand", density_g_cm3=2.0, color="#c9b99a")
    b.add("solid.box", length=7000, width=150, height=650, center=[0, y_of(POOL_R) - 75, 325], operation="new", name="Pool_R", body_name="Beckenwand")
    b.add("solid.box", length=7000, width=120, height=2200, center=[0, y_of(WALL_AP) - 60, 1100], operation="new", name="Dom_R", body_name="Domwand")
    b.add("material.assign", bodies=["Beckenwand", "Domwand"], material="Wand")
    for f, nm, y in items:
        b.add("component.insert_design", path=os.path.join(D, f).replace("\\", "/"), name=nm)
    return b

res = sc.run_results(base().write("radial-probe"))
occ = [r["occurrence"] for r in res if "occurrence" in r]
b = base()
for (f, nm, y), o in zip(items, occ):
    if y:
        b.add("occurrence.move", occurrence=o, translate=[0, round(y, 3), 0], move_grounded=True)
out = os.path.join(sc.TMP, "radialbudget.sc")
sc.run(b.write("radialbudget"), out)
mid = y_of(0.5 * (Ga["apc"] + Gm["apc"]))
top = os.path.join(OUT, "radialbudget-01-draufsicht.png")
sc.snapshot(out, top, [0, mid, 0], 0.0, 1.5707, 5200, w=1400, h=900)
sec = os.path.join(OUT, "radialbudget-02-querschnitt.png")
sc.snapshot(out, sec, [0, mid, 900], 0.0, 0.0, 5200, w=1400, h=800, section="x=0")
try:                                                     # Masse in die Draufsicht schreiben (PIL, falls vorhanden)
    from PIL import Image, ImageDraw
    im = Image.open(top).convert("RGB")
    dr = ImageDraw.Draw(im)
    half = lambda G: G["bed_w"] / 2.0 + p["leg_clearance"] + p["foot_plate"]
    txt = [f"Beckenrand aussen {POOL_R:.0f}", f"Laufweg A {Gm['apc'] - half(Gm) - POOL_R:.0f}", f"Innenportal {Gm['apc'] - half(Gm):.0f}..{Gm['apc'] + half(Gm):.0f} (Beet 933)",
           f"Laufweg B {(Ga['apc'] - half(Ga)) - (Gm['apc'] + half(Gm)):.0f}", f"Aussenportal {Ga['apc'] - half(Ga):.0f}..{Ga['apc'] + half(Ga):.0f} (Beet 800)", f"Wandluft {WALL_AP - (Ga['apc'] + half(Ga)):.0f} bis Apothem {WALL_AP:.0f}"]
    for i, t in enumerate(txt):
        dr.text((20, 20 + 22 * i), t, fill=(0, 0, 0))
    im.save(top)
except ImportError:
    print("PIL fehlt: Draufsicht ohne Masse")
print(top, sec)
