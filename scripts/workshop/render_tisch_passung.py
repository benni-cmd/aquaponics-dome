"""Kontextbilder W16 (Passung): (1) Draufsicht auf die Ecke zwischen zwei benachbarten Tischen mit Beeten (Layout-Koordinaten), (2) Querschnitt durch Bock und Beet im Tisch-KS.
Aufruf: python scripts/workshop/render_tisch_passung.py [typ]   (Standard aussen)"""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
import tisch_geom as TG

D = os.path.join(sc.ROOT, "designs", "components")
OUT = os.path.join(sc.ROOT, "renders", "components", "nft_passung")
os.makedirs(OUT, exist_ok=True)
typ = sys.argv[1] if len(sys.argv) > 1 else "aussen"
p, d = sc.load_params("nft_tisch")
G = TG.geometry(typ, p, d["typen"][typ])
lay = json.load(open(os.path.join(sc.ROOT, "data", "layout.json"), encoding="utf-8"))
beds = lay["ibc_beds"]
bed_file = {"aussen": "ibc_beet_aussen_933.sc", "mitte": "ibc_beet_innen_933.sc"}.get(typ)

def make(items):
    """items: [(datei, name, yaw_deg, x, y, z)] -> Skript mit Einfuegen; Reihenfolge der Occurrences wird aus einem Probelauf gelesen."""
    def base():
        b = sc.Build()
        for (f, nm, *_r) in items:
            b.add("component.insert_design", path=os.path.join(D, f).replace("\\", "/"), name=nm)
        return b
    res = sc.run_results(base().write("passung-probe"))
    occ = [r["occurrence"] for r in res if "occurrence" in r]
    b = base()
    for (f, nm, yaw, x, y, z), o in zip(items, occ):
        if yaw:
            b.add("occurrence.move", occurrence=o, axis=[0, 0, 1], angle=f"{yaw:.4f} deg", origin=[0, 0, 0], space="world", move_grounded=True)
        b.add("occurrence.move", occurrence=o, translate=[round(x, 2), round(y, 2), round(z, 2)], space="world", move_grounded=True)
    return b

# (1) Ecke: Tische der Sektoren 2 und 3 (aussen) bzw. 1 und 2 (mitte)
i0 = 2 if typ == "aussen" else 1
items = []
az_corner = 5.3 + 36 * (i0 + 0.5)
for i in (i0, i0 + 1):
    az = 5.3 + 36 * i
    b_ = min((b for b in beds if abs(b["r"] - G["apc"]) < 400), key=lambda b: abs(((b["az"] - az + 180) % 360) - 180))
    ap = b_["r"] * math.cos(math.radians(b_["az"] - az))
    a = math.radians(az)
    items.append((f"nft_tisch_{typ}.sc", f"Tisch_{i}", az + 90, ap * math.cos(a), ap * math.sin(a), 0))
    if bed_file:
        items.append((bed_file, f"Beet_{i}", b_["yaw"], b_["cx"], b_["cy"], b_["z0"]))
out = os.path.join(sc.TMP, f"passung-{typ}-ecke.sc")
sc.run(make(items).write("passung-ecke"), out)
ac = math.radians(az_corner)
tgt = [G["apc"] * math.cos(ac), G["apc"] * math.sin(ac), 600]
sc.snapshot(out, os.path.join(OUT, f"passung_{typ}-01-ecke-draufsicht.png"), tgt, 0.0, 1.5, 5200, w=1100, h=800)
sc.snapshot(out, os.path.join(OUT, f"passung_{typ}-02-ecke-iso.png"), tgt, 0.8, 0.55, 6500, w=1100, h=700)
# (2) Querschnitt im Tisch-KS: Tisch + Beet unter dem Tisch, Schnitt durch den ersten Bock
if bed_file:
    b_loc = [(f"nft_tisch_{typ}.sc", "Tisch", 0, 0, 0, 0), (bed_file, "Beet", 0, 0, 0, -162)]
    out2 = os.path.join(sc.TMP, f"passung-{typ}-quer.sc")
    sc.run(make(b_loc).write("passung-quer"), out2)
    sc.snapshot(out2, os.path.join(OUT, f"passung_{typ}-03-querschnitt-bock-beet.png"), [G["xb"][0], 0, 700], 1.5708, 0.0, 3800, w=1100, h=700, section=f"x={G['xb'][0]:.0f}")
print(OUT)
