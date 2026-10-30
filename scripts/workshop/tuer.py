"""Tuer komplett T50 (W20, D36, R13): Zarge aus Rechteckrohr (Schritt 2), Tuerblatt (Schritt 3) in der Feldebene des Basisfeldes BBB 149,2.
Feld-KS (siehe tuer_geom.py): Ursprung Mitte der Basiskante auf Z 0, X tangential, Y' hangaufwaerts in der Feldebene, Z' Feldnormale nach aussen. Zarge: Schwelle (s 0..rohr), Pfosten (je Seite, Lichte dazwischen), Sturz.
Aufruf: python scripts/workshop/tuer.py [--render]"""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
import tuer_geom as TGm

def rect_member(b, name, dims, origin, xdir, ydir, dist, symmetric=False):
    b.add("sketch.create", plane={"origin": origin, "x_dir": xdir, "y_dir": ydir}, name="S_" + name)
    b.add("frame.profile.insert", profile=dict(kind="rect_tube", **dims), at=[0, 0], anchor="center")
    b.add("sketch.finish")
    ex = dict(distance=dist, name="F_" + name, body_name=name)
    if symmetric:
        ex["direction"] = "symmetric"
    b.add("solid.extrude", **ex)
    b.add("material.assign", bodies=[name], material="Stahl verzinkt")

def build():
    p, d = sc.load_params("tuer")
    G = d["geometrie"]
    unit = {k: v["einheit"] for k, v in d["parameter"].items()}
    b = sc.Build()
    b.params_to_design(p, d, unit)
    r, wall, sh = p["rohr"], p["rohr_wand"], p["schwelle_h"]
    lw, lh = G["lichte_w"], G["lichte_h"]
    fw = G["zarge_aussen_w"]
    b.add("material.create", name="Stahl verzinkt", density_g_cm3=7.85, color="#aeb4b8", pbr={"metallic": 0.8, "roughness": 0.45, "dielectric_ior": 1.5})
    root = "T50_Tuer_Komplett"
    b.add("component.create", name=root, grounded=True)
    b.add("component.create", name="T50a_Zarge")
    dims = dict(width=r, height=r, wall=wall)
    # Schwelle: s 0..sh, ueber die ganze Zargenbreite; Plane normal +X (x_dir Y', y_dir Z'), symmetrisch um X 0
    rect_member(b, "Schwelle", dims, [0, sh / 2, 0], [0, 1, 0], [0, 0, 1], fw, symmetric=True)
    # Pfosten: von der Schwelle bis zum Sturz, in Y'-Richtung (Plane x_dir Z', y_dir X -> Normale +Y')
    for sg, nm in ((-1, "Pfosten_links"), (1, "Pfosten_rechts")):
        rect_member(b, nm, dims, [sg * (lw / 2 + r / 2), sh, 0], [0, 0, 1], [1, 0, 0], lh)
    # Sturz: ueber den Pfosten, s = sh + lh .. + r
    rect_member(b, "Sturz", dims, [0, sh + lh + r / 2, 0], [0, 1, 0], [0, 0, 1], fw, symmetric=True)
    b.add("component.activate", component=root)
    for nm, pn, ds in ((root, "T50", d["beschreibung"]), ("T50a_Zarge", "T50a", "Zarge aus Rechteckrohr 30 x 30 x 2: Schwelle, 2 Pfosten, Sturz (Lichte 1016 x 2008)")):
        b.add("component.metadata.set", component=nm, part_number=pn, description=ds, revision="B", properties={"Werkstoff": "Stahl verzinkt"})
    return b

if __name__ == "__main__":
    out = os.path.join(sc.ROOT, "designs", "components", "tuer_komplett.sc")
    sc.run(build().write("tuer_komplett"), out)
    ev = sc.evaluate(out)
    for x in ev["bodies"]:
        print(x["name"], x["faces"], round(x["mass_g"] / 1000, 2), "kg", [round(v, 1) for v in x["bbox"]["min"]], [round(v, 1) for v in x["bbox"]["max"]])
    if "--render" in sys.argv:
        rd = os.path.join(sc.ROOT, "renders", "components", "tuer_komplett")
        os.makedirs(rd, exist_ok=True)
        sc.snapshot(out, os.path.join(rd, "tuer_komplett-01-zarge.png"), [0, 1000, 0], 0.6, 0.3, 4200, w=1000, h=800)
