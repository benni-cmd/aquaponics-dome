"""Haut-Randprofil T41 (W19 Schritt 3): Aluminium-Kappe 30 x 8 (U-Profil, Wand 2, offen nach unten) als haut_profil.sc, Laenge als Konfiguration A 3279 / B 3708.
Bezug: Mitte der Laenge, Strebenachse, X Laengsrichtung, Z 0 = Unterkante Kappe. Aufruf: python scripts/workshop/haut_profil.py [--render]"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc

def build():
    p, d = sc.load_params("haut_profil")
    unit = {k: v["einheit"] for k, v in d["parameter"].items()}
    b = sc.Build()
    b.params_to_design(p, d, unit)
    w, h, t = p["cap_w"], p["cap_h"], p["cap_wall"]
    b.add("material.create", name="Aluminium", density_g_cm3=d["werkstoff"]["dichte_g_cm3"], color=d["werkstoff"]["farbe"], pbr={"metallic": 0.8, "roughness": 0.45, "dielectric_ior": 1.5})
    root = "T41_Haut_Profil"
    b.add("component.create", name=root, grounded=True)
    b.add("sketch.create", plane={"origin": [0, 0, 0], "x_dir": [0, 1, 0], "y_dir": [0, 0, 1]}, name="S_Kappe")
    pts = [[-w / 2, 0], [-w / 2, h], [w / 2, h], [w / 2, 0], [w / 2 - t, 0], [w / 2 - t, h - t], [-w / 2 + t, h - t], [-w / 2 + t, 0]]
    b.add("sketch.line", points=pts, closed=True)
    b.add("sketch.finish")
    b.add("solid.extrude", distance="len", direction="symmetric", operation="new", name="E_Kappe", body_name="Kappe")
    b.add("material.assign", bodies=["Kappe"], material="Aluminium")
    b.add("config.configure", params=["len"])
    b.add("config.row", name="A")
    b.add("config.row", name="B", **{"from": "A"}, values={"param:len": "3708 mm"})
    b.add("config.activate", row="A")
    b.add("component.metadata.set", component=root, part_number="T41", description=d["beschreibung"], revision="A", properties={"Werkstoff": d["werkstoff"]["name"]})
    return b

if __name__ == "__main__":
    out = os.path.join(sc.ROOT, "designs", "components", "haut_profil.sc")
    sc.run(build().write("haut_profil"), out)
    ev = sc.evaluate(out)
    bd = ev["bodies"][0]
    print("Kappe A: Flaechen", bd["faces"], "Volumen", round(bd["volume_mm3"] / 1000, 1), "cm3", "Masse", round(bd["mass_g"] / 1000, 2), "kg", [round(v, 1) for v in bd["bbox"]["min"]], [round(v, 1) for v in bd["bbox"]["max"]])
    if "--render" in sys.argv:
        rd = os.path.join(sc.ROOT, "renders", "components", "haut_profil")
        os.makedirs(rd, exist_ok=True)
        sc.snapshot(out, os.path.join(rd, "haut_profil-01-iso.png"), [0, 0, 4], 0.7, 0.4, 4800, w=1000, h=650)
        sc.snapshot(out, os.path.join(rd, "haut_profil-02-querschnitt.png"), [1640, 0, 4], 1.5708, 0.0, 120, w=800, h=500, section="YZ,flip")
