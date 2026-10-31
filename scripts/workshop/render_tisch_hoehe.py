"""Seitenansicht Tischhoehe 1000 mm (W33, R35/D60): NFT-Tisch (Typ mitte oder aussen) mit der Menschenfigur 1,80 m (mensch_referenz.sc) als Massstab.
Ansicht quer zur Rinne (Blick entlang +X): Figur steht auf dem Laufweg ausserhalb des Portalbocks und schaut zum Tisch; Seitenansicht Laengs: Figur am Ablaufende.
Aufruf: python scripts/workshop/render_tisch_hoehe.py [typ]   (Standard mitte) -> renders/components/nft_tisch_<typ>/nft_tisch_<typ>-07-hoehe-*.png"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
import tisch_geom as TG

D = os.path.join(sc.ROOT, "designs", "components")
typ = sys.argv[1] if len(sys.argv) > 1 else "mitte"
p, d = sc.load_params("nft_tisch")
G = TG.geometry(typ, p, d["typen"][typ])
OUT = os.path.join(sc.ROOT, "renders", "components", f"nft_tisch_{typ}")
os.makedirs(OUT, exist_ok=True)

def make(items):
    """items: [(datei, name, x, y, z)] -> Skript mit Einfuegen und Verschieben (Reihenfolge der Occurrences aus einem Probelauf, wie render_tisch_passung.py)."""
    def base():
        b = sc.Build()
        for (f, nm, *_r) in items:
            b.add("component.insert_design", path=os.path.join(D, f).replace("\\", "/"), name=nm)
        return b
    res = sc.run_results(base().write("hoehe-probe"))
    occ = [r["occurrence"] for r in res if "occurrence" in r]
    b = base()
    for (f, nm, x, y, z), o in zip(items, occ):
        b.add("occurrence.move", occurrence=o, translate=[round(x, 2), round(y, 2), round(z, 2)], space="world", move_grounded=True)
    return b

xb = G["xb"]
# Figur quer: Laufweg ausserhalb des Portals (-Y ist radial aussen), Blick +Y zum Tisch; Abstand 100 mm vor der Fussplattenkante
y_fig = -(G["yl"] + p["foot_plate"] / 2 + 100)
# Figur laengs: am Ablaufende (+X) hinter dem Sammelrohr, Blick +Y (seitlich zum Tisch); Y-Lage vor dem Tisch (radial aussen)
x_end = G["rows"][0]["xc"] + G["Lmin"] / 2 + 700
scenes = {
    "quer": ([("nft_tisch_%s.sc" % typ, "Tisch", 0, 0, 0), ("mensch_referenz.sc", "Figur", xb[0] + 400, y_fig, 0)], [xb[0], y_fig / 2, 900], 1.5708, 0.0, 4200),
    "laengs": ([("nft_tisch_%s.sc" % typ, "Tisch", 0, 0, 0), ("mensch_referenz.sc", "Figur", x_end, 0, 0)], [G["rows"][0]["xc"] + 350, 0, 800], 0.0, 0.0, 6200),
}
for nme, (items, tgt, yaw, pitch, dist) in scenes.items():
    out = os.path.join(sc.TMP, f"hoehe-{typ}-{nme}.sc")
    sc.run(make(items).write(f"hoehe-{nme}"), out)
    png = os.path.join(OUT, f"nft_tisch_{typ}-07-hoehe-{nme}.png")
    sc.snapshot(out, png, tgt, yaw, pitch, dist, w=1200, h=800)
    print(png)
