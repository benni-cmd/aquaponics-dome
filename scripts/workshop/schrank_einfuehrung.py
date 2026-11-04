"""Schrank-Einfuehrung T89 (W37-3 Teil 4): Boden-Einfuehrungsplatte des Schaltschranks (800 x 500, Blech 3 mm) mit je einer Kabeleinfuehrung DN100 (230-V-Stamm) und DN50 (Signal-Stamm) aus W39
und je einem Leerrohr-Bogen 90 Grad aus W36 darunter (Muffe A offen, horizontal, unterflur). Nur das Bauteil: der STANDORT des Schranks ist OFFEN (E13), die Koordinaten sind lokal.
`designs/components/schaltschrank.sc` und `scripts/gen_dome.py` bleiben unangetastet (eigener Name `schrank_einfuehrung`, nicht `schaltschrank`).
KS: Mitte der Boden-Unterkante (Z 0 = Unterkante Schrankboden, Boden Z 0 bis 3), X Schrankbreite 800, Y Schranktiefe 500, Z hoch (nach oben in den Schrank). Eingefuegte Designs aus lt_kabeleinfuehrung_dn* und lt_leerrohr_bogen90_dn*.
Aufruf: python -X utf8 scripts/workshop/schrank_einfuehrung.py [--render]"""
import math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
import leitung as L
import leitung_w36 as W36
import leitung_w39 as W39

DD = os.path.join(sc.ROOT, "designs", "components").replace("\\", "/")
MATS = (("SE Blech", 7.85, "#9aa0a4"),)

def geom(p):
    g = {}
    for dn in (100, 50):
        kg = W39.kab_geom(dn)
        q = W36.LR[dn]
        leg = q["t"] + 20.0                                               # Schenkel des Leerrohr-Bogens (wie leitung_w36.leerrohr_bogen)
        R = q["R"]
        sign = -1 if dn == 100 else 1                                     # DN100 laeuft nach -X weg, DN50 nach +X
        cx = p["x_dn100"] if dn == 100 else p["x_dn50"]
        g[dn] = dict(kab=kg, leg=leg, R=R, cx=cx, cy=p["y_achse"], sign=sign,
                     ke_z=-kg["z_d1"],                                    # Einfuegung: Dichtungsunterkante liegt auf der Boden-Unterkante Z 0
                     z_muffe_top=-kg["z_d1"] + kg["t"],                   # Anschlag der Muffe der Einfuehrung (Leerrohr-Ende B oben)
                     a_x=cx + sign * (leg + R), a_z=-kg["z_d1"] + kg["t"] - (R + leg), hals=kg["hals"])
    return g

def build():
    p, d = sc.load_params("schrank_einfuehrung")
    g = geom(p)
    unit = {k: v["einheit"] for k, v in d["parameter"].items()}
    b = sc.Build()
    b.params_to_design(p, d, unit)
    for nm, dens, col in MATS:
        b.add("material.create", name=nm, density_g_cm3=dens, color=col)
    root = "T89_Schrank_Einfuehrung"
    b.add("component.create", name=root, grounded=True)
    bt = p["boden_t"]
    b.add("solid.box", length=p["cab_x"], width=p["cab_y"], height=bt, center=[0, 0, bt / 2], operation="new", name="R_Boden", body_name="Schrankboden")
    for dn in (100, 50):
        q = g[dn]
        b.add("solid.cylinder", diameter=q["hals"], height=bt + 2, base=[q["cx"], q["cy"], -1], operation="cut", targets=["Schrankboden"], name=f"Loch_DN{dn}")
    b.add("material.assign", bodies=["Schrankboden"], material="SE Blech")
    # Wandstummel: umlaufender Rahmen 2 mm, 100 hoch, steht auf dem Boden (zeigt die Schrankwand fuer die Interferenzpruefung)
    b.add("solid.box", length=p["cab_x"], width=p["cab_y"], height=p["wand_h"], center=[0, 0, bt + p["wand_h"] / 2], operation="new", name="R_Wand", body_name="Schrankwand")
    b.add("solid.box", length=p["cab_x"] - 2 * p["wand_t"], width=p["cab_y"] - 2 * p["wand_t"], height=p["wand_h"] + 2, center=[0, 0, bt + p["wand_h"] / 2], operation="cut", targets=["Schrankwand"], name="Wand_Innen")
    b.add("material.assign", bodies=["Schrankwand"], material="SE Blech")
    for dn in (100, 50):
        q = g[dn]
        b.add("component.insert_design", path=f"{DD}/lt_kabeleinfuehrung_dn{dn}.sc", name=f"KE_DN{dn}", translate=[q["cx"], q["cy"], round(q["ke_z"], 4)])
    for dn in (100, 50):
        q = g[dn]
        if q["sign"] > 0:      # Rot_y(-90): x' = -z, z' = x   (Muffe A oeffnet nach +X, Ende B zeigt nach +Z)
            R3 = [0, 0, -1, 0, 1, 0, 1, 0, 0]
        else:                  # danach Rot_z(180): x' = z, y' = -y   (Muffe A oeffnet nach -X)
            R3 = [0, 0, 1, 0, -1, 0, 1, 0, 0]
        m = [R3[0], R3[1], R3[2], round(q["a_x"], 4), R3[3], R3[4], R3[5], round(q["cy"], 4), R3[6], R3[7], R3[8], round(q["a_z"], 4)]
        b.add("component.insert_design", path=f"{DD}/lt_leerrohr_bogen90_dn{dn}.sc", name=f"LB_DN{dn}")
        b.add("occurrence.move", occurrence=f"LB_DN{dn}:1", space="world", matrix=m)
    b.add("component.activate", component=root)
    b.add("component.metadata.set", component=root, part_number="T89", description=d["beschreibung"], revision="A", properties={"Werkstoff": "Stahlblech (Platzhalter), PP, EPDM, PVC-U"})
    return b, g

if __name__ == "__main__":
    out = os.path.join(sc.ROOT, "designs", "components", "schrank_einfuehrung.sc")
    b, g = build()
    sc.run(b.write("schrank_einfuehrung"), out)
    ev = sc.evaluate(out)
    mn, mx = sc.bbox_all(ev)
    print("Koerper", len(ev["bodies"]), "bbox", [round(v, 1) for v in mn], [round(v, 1) for v in mx], "Masse g", round(ev["total"]["mass_g"]))
    for x in ev["bodies"]:
        print("  ", {k: (round(v, 1) if isinstance(v, float) else v) for k, v in x.items() if k in ("name", "component", "path", "mass_g")}, [round(v, 1) for v in x["bbox"]["min"]], [round(v, 1) for v in x["bbox"]["max"]])
    if "--render" in sys.argv:
        rd = os.path.join(sc.ROOT, "renders", "components", "schrank_einfuehrung")
        os.makedirs(rd, exist_ok=True)
        sc.snapshot(out, os.path.join(rd, "schrank_einfuehrung-01-schraeg.png"), [0, 0, -250], 0.6, 0.45, 2600, w=1100, h=760)
        sc.snapshot(out, os.path.join(rd, "schrank_einfuehrung-02-seite.png"), [0, 0, -250], 0.0, 0.0, 2600, w=1100, h=760)
        sc.snapshot(out, os.path.join(rd, "schrank_einfuehrung-03-schnitt.png"), [0, 0, -250], 0.0, 0.0, 2600, w=1100, h=760, section="y=0")
