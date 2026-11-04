"""Geblaese-Baugruppe Luft T85 (W37-3 Teil 1, R45 Abschnitt 4, R53 Abschnitt 4 und 5): Linear-Membranpumpe (Platzhalterquader 240 x 180 x 230 mit 4 Gummifuessen, Stutzen d20 oben, Netzkabel) plus
Luftleitung ueber den hoechsten Wasserspiegel (Schleife: Rohr d20 senkrecht, Bogen R80, waagerecht, Rueckschlagventil d20, Austrittsrohr). Die Baugruppe wird zweimal gebraucht (N+1).
KS: Mitte der Standflaeche der Pumpe am Boden (Z 0 = Aufstellflaeche im Schrankbereich, Standort E13 OFFEN); X Richtung Luftaustritt (+X), Y quer, Z hoch; Rohrachse der Schleife bei Z = apex_z (710: Rand Z 650 + 60 wie Schwimmerventil).
Rohre stossen stumpf an das Rueckschlagventil (Muffentiefe nicht modelliert). Alle Masse Handelsmass-Platzhalter, Pumpentyp NICHT gewaehlt (Kennlinie bei 26 kPa OFFEN).
Aufruf: python -X utf8 scripts/workshop/geblaese_luft.py [--render]"""
import math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
import leitung as L

MATS = (("GL Pumpe", 1.0, "#2f3a44"), ("GL Fuss", 1.2, "#161616"), ("GL PVC", 1.4, "#3d6f9e"), ("GL Hahn", 1.4, "#2a5da8"), ("GL Kabel", 1.3, "#111111"))

def geom(p):
    g = {}
    g["z_top"] = p["foot_h"] + p["box_z"]                                 # Oberkante Gehaeuse
    g["z0"] = g["z_top"] + p["out_l"]                                     # Ende Stutzen = Anfang der Schleife
    g["od"], g["idd"] = p["out_d"], p["out_d"] - 2 * L.wall_p(p["out_d"])
    g["l1"] = p["apex_z"] - g["z0"] - p["bend_r"]                         # senkrechter Schenkel bis Bogenanfang
    g["x_bend"] = p["bend_r"]                                             # Bogenende (waagerecht) bei x = R
    g["rsv_of"] = L.od_f(p["out_d"]); g["rsv_ob"] = g["rsv_of"] + 12
    g["rsv_dp"] = L.DEPTH[p["out_d"]]; g["rsv_lb"] = 50.0
    g["rsv_L"] = g["rsv_lb"] + 2 * g["rsv_dp"]
    g["x_rsv"] = p["bend_r"] + p["arm_l"]                                 # Rueckschlagventil: Anfang
    g["x_tube"] = g["x_rsv"] + g["rsv_L"]
    g["x_end"] = g["x_tube"] + p["out_tube_l"]                            # Port Luftaustritt
    g["dens"] = p["pump_mass_g"] / (p["box_x"] * p["box_y"] * p["box_z"] / 1000.0)
    return g

def bend2(b, body, od, idd, z0, l1, R, l2, mat):
    """Rohrbogen 90 Grad ab (0,0,z0): Schenkel l1 nach +Z, Bogen R nach +X, Schenkel l2 nach +X (wie leitung.bend, aber ungleiche Schenkel und Versatz z0)."""
    b.add("solid.cylinder", diameter=od, height=l1, base=[0, 0, z0], operation="new", name=body + "_L1", body_name=body)
    b.add("sketch.create", plane={"origin": [0, 0, z0 + l1], "x_dir": [1, 0, 0], "y_dir": [0, 1, 0]}, name="S_Bogen")
    b.add("sketch.circle.center", center=[0, 0], radius=od / 2)
    b.add("sketch.finish")
    b.add("solid.revolve", axis={"origin": [R, 0, z0 + l1], "dir": [0, 1, 0]}, angle="90 deg", operation="join", targets=[body], name=body + "_Bogen")
    b.add("solid.extrude", face=[R, 0, z0 + l1 + R], face_body=body, distance=l2, operation="join", targets=[body], name=body + "_L2")
    tool = body + "_Werkzeug"
    b.add("solid.cylinder", diameter=idd, height=l1 + 1, base=[0, 0, z0 - 1], operation="new", name=tool + "_1", body_name=tool)
    b.add("sketch.create", plane={"origin": [0, 0, z0 + l1], "x_dir": [1, 0, 0], "y_dir": [0, 1, 0]}, name="S_BogenBohr")
    b.add("sketch.circle.center", center=[0, 0], radius=idd / 2)
    b.add("sketch.finish")
    b.add("solid.revolve", axis={"origin": [R, 0, z0 + l1], "dir": [0, 1, 0]}, angle="90 deg", operation="join", targets=[tool], name=tool + "_Bogen")
    b.add("solid.extrude", face=[R, 0, z0 + l1 + R], face_body=tool, distance=l2 + 2, operation="join", targets=[tool], name=tool + "_2")
    b.add("solid.combine", target=body, tools=[tool], operation="cut")
    b.add("material.assign", bodies=[body], material=mat)

def build(p=None):
    p0, d = sc.load_params("geblaese_luft")
    p = dict(p0, **(p or {}))
    g = geom(p)
    unit = {k: v["einheit"] for k, v in d["parameter"].items()}
    b = sc.Build()
    b.params_to_design(p, d, unit)
    for nm, dens, col in MATS:
        b.add("material.create", name=nm, density_g_cm3=round(g["dens"], 4) if nm == "GL Pumpe" else dens, color=col)
    root = "T85_Geblaese_Luft"
    b.add("component.create", name=root, grounded=True)
    zc = p["foot_h"] + p["box_z"] / 2
    b.add("solid.box", length=p["box_x"], width=p["box_y"], height=p["box_z"], center=[0, 0, round(zc, 3)], operation="new", name="R_Gehaeuse", body_name="Pumpe")
    b.add("material.assign", bodies=["Pumpe"], material="GL Pumpe")
    for i, (sx, sy) in enumerate(((1, 1), (-1, 1), (1, -1), (-1, -1)), 1):
        b.add("solid.cylinder", diameter=p["foot_d"], height=p["foot_h"], base=[sx * p["foot_x"], sy * p["foot_y"], 0], operation="new", name=f"R_Fuss{i}", body_name=f"Gummifuss_{i}")
        b.add("material.assign", bodies=[f"Gummifuss_{i}"], material="GL Fuss")
    # Netzkabel (Stummel an der Rueckseite, -Y)
    b.add("solid.cylinder", diameter=p["cable_d"], height=p["cable_l"], base=[p["cable_x"], -p["box_y"] / 2, round(zc, 3)], axis=[0, -1, 0], operation="new", name="R_Kabel", body_name="Netzkabel")
    b.add("material.assign", bodies=["Netzkabel"], material="GL Kabel")
    # Stutzen d20 oben
    od, idd = g["od"], g["idd"]
    b.add("solid.cylinder", diameter=od, height=p["out_l"], base=[0, 0, g["z_top"]], operation="new", name="R_Stutzen", body_name="Stutzen_Luft")
    b.add("solid.cylinder", diameter=idd, height=p["out_l"] + 2, base=[0, 0, g["z_top"] - 1], operation="cut", targets=["Stutzen_Luft"], name="Stutzenbohrung")
    b.add("material.assign", bodies=["Stutzen_Luft"], material="GL PVC")
    # Schleife
    bend2(b, "Rohrschleife", od, idd, g["z0"], g["l1"], p["bend_r"], p["arm_l"], "GL PVC")
    # Rueckschlagventil d20 (A nach B = +X), Muster W39 lt_rueckschlagventil
    za = p["apex_z"]
    b.add("solid.cylinder", diameter=g["rsv_ob"], height=g["rsv_lb"], base=[g["x_rsv"] + g["rsv_dp"], 0, za], axis=[1, 0, 0], operation="new", name="R_RSV", body_name="Rueckschlagventil")
    for x0, nm in ((g["x_rsv"], "A"), (g["x_rsv"] + g["rsv_dp"] + g["rsv_lb"], "B")):
        b.add("solid.cylinder", diameter=g["rsv_of"], height=g["rsv_dp"], base=[x0, 0, za], axis=[1, 0, 0], operation="join", targets=["Rueckschlagventil"], name="RSV_Stutzen_" + nm)
    b.add("solid.cylinder", diameter=idd, height=g["rsv_L"] + 2, base=[g["x_rsv"] - 1, 0, za], axis=[1, 0, 0], operation="cut", targets=["Rueckschlagventil"], name="RSV_Durchgang")
    b.add("material.assign", bodies=["Rueckschlagventil"], material="GL Hahn")
    # Austrittsrohr
    b.add("solid.cylinder", diameter=od, height=p["out_tube_l"], base=[g["x_tube"], 0, za], axis=[1, 0, 0], operation="new", name="R_Austritt", body_name="Rohr_Austritt")
    b.add("solid.cylinder", diameter=idd, height=p["out_tube_l"] + 2, base=[g["x_tube"] - 1, 0, za], axis=[1, 0, 0], operation="cut", targets=["Rohr_Austritt"], name="Austrittbohrung")
    b.add("material.assign", bodies=["Rohr_Austritt"], material="GL PVC")
    b.add("component.metadata.set", component=root, part_number="T85", description=d["beschreibung"], revision="A", properties={"Werkstoff": "Gehaeuse Aluminium/Kunststoff (Platzhalter), PVC-U"})
    return b, g

if __name__ == "__main__":
    out = os.path.join(sc.ROOT, "designs", "components", "geblaese_luft.sc")
    b, g = build()
    sc.run(b.write("geblaese_luft"), out)
    ev = sc.evaluate(out)
    mn, mx = sc.bbox_all(ev)
    print("Koerper", len(ev["bodies"]), "bbox", [round(v, 1) for v in mn], [round(v, 1) for v in mx], "Masse g", round(ev["total"]["mass_g"]), [(x["name"], round(x["mass_g"])) for x in ev["bodies"]])
    if "--render" in sys.argv:
        rd = os.path.join(sc.ROOT, "renders", "components", "geblaese_luft")
        os.makedirs(rd, exist_ok=True)
        sc.snapshot(out, os.path.join(rd, "geblaese_luft-01-schraeg.png"), [200, 0, 370], 0.6, 0.35, 1500, w=1100, h=760)
        sc.snapshot(out, os.path.join(rd, "geblaese_luft-02-seite.png"), [200, 0, 370], 0.0, 0.0, 1500, w=1100, h=760)
        sc.snapshot(out, os.path.join(rd, "geblaese_luft-03-schnitt.png"), [200, 0, 370], 3.14159, 0.0, 1500, w=1100, h=760, section="XZ")
