"""Keilschiene T43 (W27 Schritt 1, D39, R24): Alu-Kanal 25 x 15 (Lock Channel) mit Federdraht D2 und Schaumband, Laenge als Konfiguration A / B (je Strebe minus Knotenfreiraum).
Bezug: Mitte der Laenge, X Laengsrichtung, Z 0 = Unterkante Schaumband (Kontaktflaeche auf der Strebe), Kanal oeffnet nach +Z (aussen). Aufruf: python scripts/workshop/keilschiene.py [--render]"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc

def build():
    p, d = sc.load_params("keilschiene")
    unit = {k: v["einheit"] for k, v in d["parameter"].items()}
    b = sc.Build()
    b.params_to_design(p, d, unit)
    b.add("parameters.add", name="wire_len", expression="len - 2 * wire_clear")
    w, h, t, lip, ft = p["ch_w"], p["ch_h"], p["ch_wall"], p["ch_lip"], p["foam_t"]
    b.add("material.create", name="Aluminium Keilschiene", density_g_cm3=d["werkstoff"]["dichte_g_cm3"], color="#c4c9ce", pbr={"metallic": 0.8, "roughness": 0.45, "dielectric_ior": 1.5})
    b.add("material.create", name="Federstahl Keilschiene", density_g_cm3=7.85, color="#6e757b")
    b.add("material.create", name="Schaumband EPDM", density_g_cm3=d["parameter"]["foam_density"]["wert"], color="#222222")
    root = "T43_Keilschiene"
    b.add("component.create", name=root, grounded=True)
    plane = {"origin": [0, 0, 0], "x_dir": [0, 1, 0], "y_dir": [0, 0, 1]}          # Skizzenebene quer zur Schiene (Normale +X)
    # --- T43a Schaumband (auf der Strebenkante)
    b.add("component.create", name="T43a_Schaumband")
    b.add("sketch.create", plane=plane, name="S_Schaumband")
    b.add("sketch.rectangle.two_point", p0=[-p["foam_w"] / 2, 0], p1=[p["foam_w"] / 2, ft])
    b.add("sketch.finish")
    b.add("solid.extrude", distance="len", direction="symmetric", operation="new", name="E_Schaumband", body_name="Schaumband")
    b.add("material.assign", bodies=["Schaumband"], material="Schaumband EPDM")
    # --- T43b Kanal: U-Profil mit einwaerts gebogenen Lippen (Maulweite w - 2 * lip)
    b.add("component.activate", component=root)
    b.add("component.create", name="T43b_Kanal")
    z0 = ft
    pts = [[-w / 2, z0], [w / 2, z0], [w / 2, z0 + h], [w / 2 - lip, z0 + h], [w / 2 - lip, z0 + h - t], [w / 2 - t, z0 + h - t], [w / 2 - t, z0 + t],
           [-w / 2 + t, z0 + t], [-w / 2 + t, z0 + h - t], [-w / 2 + lip, z0 + h - t], [-w / 2 + lip, z0 + h], [-w / 2, z0 + h]]
    b.add("sketch.create", plane=plane, name="S_Kanal")
    b.add("sketch.line", points=pts, closed=True)
    b.add("sketch.finish")
    b.add("solid.extrude", distance="len", direction="symmetric", operation="new", name="E_Kanal", body_name="Kanal")
    b.add("material.assign", bodies=["Kanal"], material="Aluminium Keilschiene")
    # --- T43c Federdraht (gerade modelliert, real Zickzack-Feder), liegt im Kanalgrund mit 0,5 mm Luft
    b.add("component.activate", component=root)
    b.add("component.create", name="T43c_Federdraht")
    b.add("sketch.create", plane=plane, name="S_Federdraht")
    b.add("sketch.circle.center", center=[0, round(z0 + t + p["wire_gap"] + p["wire_d"] / 2, 3)], radius=p["wire_d"] / 2)
    b.add("sketch.finish")
    b.add("solid.extrude", distance="wire_len", direction="symmetric", operation="new", name="E_Federdraht", body_name="Federdraht")
    b.add("material.assign", bodies=["Federdraht"], material="Federstahl Keilschiene")
    b.add("component.activate", component=root)
    b.add("config.configure", params=["len"])
    b.add("config.row", name="A")
    b.add("config.row", name="B", **{"from": "A"}, values={"param:len": f"{d['typen']['B']['len']} mm"})
    b.add("config.activate", row="A")
    for nm, pn, ds in ((root, "T43", d["beschreibung"]), ("T43a_Schaumband", "T43a", "Schaumband EPDM 25 x 3"), ("T43b_Kanal", "T43b", "Alu-Kanal 25 x 15, Wand 1,5, Lippen 4"), ("T43c_Federdraht", "T43c", "Federdraht D2 (gerade modelliert)")):
        b.add("component.metadata.set", component=nm, part_number=pn, description=ds, revision="A", properties={"Werkstoff": d["werkstoff"]["name"]})
    return b

if __name__ == "__main__":
    out = os.path.join(sc.ROOT, "designs", "components", "keilschiene.sc")
    sc.run(build().write("keilschiene"), out)
    ev = sc.evaluate(out)
    print("Keilschiene A: Koerper", len(ev["bodies"]), "Masse", round(sum(x["mass_g"] for x in ev["bodies"]) / 1000, 3), "kg")
    if "--render" in sys.argv:
        rd = os.path.join(sc.ROOT, "renders", "components", "keilschiene")
        os.makedirs(rd, exist_ok=True)
        sc.snapshot(out, os.path.join(rd, "keilschiene-01-iso.png"), [1400, 0, 15], 0.7, 0.4, 260, w=1000, h=650)
        sc.snapshot(out, os.path.join(rd, "keilschiene-02-querschnitt.png"), [0, 0, 10], 1.5708, 0.0, 70, w=800, h=500, section="YZ,flip")
