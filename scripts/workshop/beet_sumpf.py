"""Beet-Sumpf T92 (W37-1 Teil 1, L04, R45 Abschnitt 3): eingegrabener PE-Rundtank Oe 800 x 1000 mit Schachtaufsatz und begehbarem Deckel,
Zulauf d50 bei 800 mm, zwei Teichpumpen (E19) mit Rueckschlagventil d40 auf eine Foerderleitung, drei Schwimmer, Entlueftung d32, zwei Kabeldurchfuehrungen.
KS: Ursprung Mitte Tankboden aussen, Z hoch; Zulauf -X, Pumpen +X, Schwimmerstange -X.
Bauweise: Einzelkoerper, die sich nur beruehren (Boolean-Vereinigung duenner Mantel scheitert, Blatt Start-Hinweis 3); Durchbrueche im Deckel und in der Wand = Aussen-Oe des Formstuecks.
Aufruf: python -X utf8 scripts/workshop/beet_sumpf.py [--render]   (schreibt die Ports ins Blatt data/components/beet_sumpf.json)"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
import leitung as L
import leitung_w39 as W39

PE, PVC, PUMP, HAHN, PA = "PE Tank", "PVC grau", "Pumpe blau", "LT hahn", "PA schwarz"   # Namen wie data/katalog.json sc_material (check_parts)

def cyl(b, name, d, h, base, axis=(0, 0, 1), op="new", targets=None, body=None, mat=None):
    kw = dict(diameter=d, height=h, base=[round(v, 3) for v in base], axis=list(axis), operation=op, name=name)
    if op == "new":
        kw["body_name"] = body or name
    else:
        kw["targets"] = targets
    b.add("solid.cylinder", **kw)
    if op == "new" and mat:
        b.add("material.assign", bodies=[body or name], material=mat)

def tube(b, name, od, idd, h, base, axis=(0, 0, 1), mat=PVC):
    """Rohr/Huelse als ein Koerper: Vollzylinder minus Bohrung (Schnitt am selben Koerper ist robust)."""
    cyl(b, name + "_R", od, h, base, axis, body=name)
    ax = [a * -1 for a in axis]
    start = [base[i] - axis[i] for i in range(3)]
    cyl(b, name + "_Bohrung", idd, h + 2, start, axis, op="cut", targets=[name])
    b.add("material.assign", bodies=[name], material=mat)

def derive(p):
    D = {}
    D["top"] = p["tank_h"] + p["aufsatz_h"]                       # Unterkante Deckel
    D["deck_top"] = D["top"] + p["deckel_t"]
    zd = p["zulauf_d"]
    D["zul_z"] = p["zulauf_sohle"] + zd / 2                      # Achse Zulauf
    D["zul_od"] = L.od_f(zd)
    D["zul_len"] = L.DEPTH[zd] + 20                              # Tankverbinder: Muffe aussen + 20 mm Kragen [A]
    D["zul_x"] = -p["tank_d"] / 2 - D["zul_len"]                 # Muffenebene (Port)
    n = int(p["pumpen"])
    D["pumpen_y"] = [0.0] if n == 1 else [-p["pumpe_dy"], p["pumpe_dy"]]
    D["pump_top"] = p["tank_floor"] + p["pumpe_h"]
    g = W39.rsv_geom(p["foerder_d"])
    D["rsv"] = g
    D["rsv_top"] = p["rsv_z"] + g["L"]
    D["f_od"] = L.od_f(p["foerder_d"])                           # Durchfuehrung Foerderleitung (Muffe)
    D["f_top"] = D["deck_top"] + L.DEPTH[p["foerder_d"]] + 14    # Muffenebene oben (Port)
    D["entl"] = (-150.0, -200.0)
    D["entl_od"] = L.od_f(p["entl_d"])
    D["entl_top"] = D["deck_top"] + 60
    D["kabel"] = [(-150.0, 170.0), (-30.0, 240.0)]
    D["kabel_top"] = D["deck_top"] + 30
    D["schwimmer"] = [("AUS", p["pegel_aus"]), ("EIN", p["pegel_ein"]), ("ALARM", p["pegel_alarm"])]
    return D

def build():
    p, d = sc.load_params("beet_sumpf")
    D = derive(p)
    unit = {k: v["einheit"] for k, v in d["parameter"].items()}
    b = sc.Build()
    b.params_to_design(p, d, unit)
    for nm, dens, col in ((PE, 0.95, "#3b3f44"), (PVC, 1.4, "#8d9296"), (PUMP, 0.4, "#2f5d3a"), (HAHN, 1.4, "#2a5da8"), (PA, 1.14, "#1f1f1f")):
        b.add("material.create", name=nm, density_g_cm3=dens, color=col)
    root = "T92_Beet_Sumpf"
    b.add("component.create", name=root, grounded=True)
    R, w, fl = p["tank_d"] / 2, p["tank_wall"], p["tank_floor"]
    # --- Tank, Aufsatz, Deckel
    b.add("component.create", name="T92a_Behaelter")
    cyl(b, "Tank_R", p["tank_d"], p["tank_h"], [0, 0, 0], body="Tank")
    cyl(b, "Tank_Hohl", p["tank_d"] - 2 * w, p["tank_h"] - fl - w, [0, 0, fl], op="cut", targets=["Tank"])
    cyl(b, "Tank_Oeffnung", p["oeffnung_d"], w + 2, [0, 0, p["tank_h"] - w - 1], op="cut", targets=["Tank"])
    cyl(b, "Tank_Zulaufloch", D["zul_od"], w + 4, [-R + w + 2, 0, D["zul_z"]], axis=(-1, 0, 0), op="cut", targets=["Tank"])
    b.add("material.assign", bodies=["Tank"], material=PE)
    tube(b, "Schachtaufsatz", p["aufsatz_d"], p["aufsatz_d"] - 2 * p["aufsatz_wall"], p["aufsatz_h"], [0, 0, p["tank_h"]], mat=PE)
    cyl(b, "Deckel_R", p["deckel_d"], p["deckel_t"], [0, 0, D["top"]], body="Deckel")
    holes = [("Foerder", p["pumpe_x"], 0.0, D["f_od"]), ("Entl", D["entl"][0], D["entl"][1], D["entl_od"])] + [(f"Kabel{k}", x, y, p["kabel_d"]) for k, (x, y) in enumerate(D["kabel"], 1)]
    for nm, x, y, od in holes:
        cyl(b, f"Deckel_Loch_{nm}", od, p["deckel_t"] + 2, [x, y, D["top"] - 1], op="cut", targets=["Deckel"])
    b.add("material.assign", bodies=["Deckel"], material=PE)
    # --- Zulauf (Tankverbinder d50, aussen)
    b.add("component.activate", component=root)
    b.add("component.create", name="T92b_Zulauf")
    zd = p["zulauf_d"]
    cyl(b, "Zulauf_R", D["zul_od"], D["zul_len"] + w, [-R + w, 0, D["zul_z"]], axis=(-1, 0, 0), body="Zulauf_Tankverbinder")
    cyl(b, "Zulauf_Muffe", zd, L.DEPTH[zd] + 1, [D["zul_x"] - 1, 0, D["zul_z"]], axis=(1, 0, 0), op="cut", targets=["Zulauf_Tankverbinder"])
    cyl(b, "Zulauf_Durchgang", zd - 2 * L.wall_p(zd), D["zul_len"] + w + 2, [-R + w + 1, 0, D["zul_z"]], axis=(-1, 0, 0), op="cut", targets=["Zulauf_Tankverbinder"])
    b.add("material.assign", bodies=["Zulauf_Tankverbinder"], material=PVC)
    # --- Pumpen und Foerderleitung
    b.add("component.activate", component=root)
    b.add("component.create", name="T92c_Pumpen")
    fd, g = p["foerder_d"], D["rsv"]
    fid = fd - 2 * L.wall_p(fd)
    px = p["pumpe_x"]
    for k, py in enumerate(D["pumpen_y"], 1):
        b.add("solid.box", length=p["pumpe_l"], width=p["pumpe_w"], height=p["pumpe_h"], center=[px, py, fl + p["pumpe_h"] / 2], operation="new", name=f"B_Pumpe_{k}", body_name=f"Pumpe_{k}")
        b.add("material.assign", bodies=[f"Pumpe_{k}"], material=PUMP)
        tube(b, f"Steigrohr_{k}_unten", fd, fid, p["rsv_z"] - D["pump_top"], [px, py, D["pump_top"]])
        tube(b, f"Rueckschlagventil_{k}", g["ob"], g["wi"], g["L"], [px, py, p["rsv_z"]], mat=HAHN)
        top = p["sammel_z"] - fd / 2 if len(D["pumpen_y"]) > 1 else D["top"]
        tube(b, f"Steigrohr_{k}_oben", fd, fid, top - D["rsv_top"], [px, py, D["rsv_top"]])
    if len(D["pumpen_y"]) > 1:
        y0 = -p["pumpe_dy"] - fd / 2
        tube(b, "Sammelrohr", fd, fid, 2 * p["pumpe_dy"] + fd, [px, y0, p["sammel_z"]], axis=(0, 1, 0))
        tube(b, "Steigrohr_Deckel", fd, fid, D["top"] - (p["sammel_z"] + fd / 2), [px, 0, p["sammel_z"] + fd / 2])
    tube(b, "Durchfuehrung_Foerder", D["f_od"], fd, D["f_top"] - D["top"], [px, 0, D["top"]])
    # --- Schwimmer, Entlueftung, Kabel
    b.add("component.activate", component=root)
    b.add("component.create", name="T92d_Schwimmer")
    sx = p["stange_x"]
    cyl(b, "Schwimmerstange", p["stange_d"], D["top"] - fl, [sx, 0, fl], mat=PVC)
    for nm, z in D["schwimmer"]:
        cyl(b, f"Schwimmer_{nm}", p["schwimmer_d"], p["schwimmer_h"], [sx, p["stange_d"] / 2 + p["schwimmer_d"] / 2 + 5, z - p["schwimmer_h"] / 2], mat=PA)
    ex, ey = D["entl"]
    tube(b, "Entlueftung", D["entl_od"], p["entl_d"] - 2 * L.wall_p(p["entl_d"]), D["entl_top"] - D["top"], [ex, ey, D["top"]])
    cyl(b, "Insektengitter_Kappe", D["entl_od"] + 20, 20, [ex, ey, D["entl_top"]], mat=PA)
    for k, (kx, ky) in enumerate(D["kabel"], 1):
        tube(b, f"Kabelverschraubung_{k}", p["kabel_d"], 16, D["kabel_top"] - D["top"], [kx, ky, D["top"]], mat=PA)
    b.add("component.activate", component=root)
    for nm, pn, ds in ((root, "T92", d["beschreibung"]), ("T92a_Behaelter", "T92a", "PE-Rundtank Oe 800 x 1000, Schachtaufsatz Oe 600 x 200, Deckel Oe 700 begehbar"),
                       ("T92b_Zulauf", "T92b", "Tankverbinder d50 (Zulauf der Beetablaeufe K14/K30), Sohle 800 mm"),
                       ("T92c_Pumpen", "T92c", f"{len(D['pumpen_y'])} Teichpumpen (Platzhalter), Steigrohre d40 mit Rueckschlagventil, Sammelrohr, Deckeldurchfuehrung K58/K59"),
                       ("T92d_Schwimmer", "T92d", "Schwimmerstange mit 3 Schwimmern (AUS/EIN/ALARM), Entlueftung d32 mit Gitter, 2 Kabelverschraubungen M25")):
        b.add("component.metadata.set", component=nm, part_number=pn, description=ds, revision="A", properties={"Werkstoff": d["werkstoff"]["name"]})
    return b, p, d, D

def ports(p, D):
    f = lambda v: f"{round(v):d}"
    P = [["Zulauf Beetablaeufe (K14 Linie 1 / K30 Linie 2)", f"Muffe d{p['zulauf_d']:g} (Tankverbinder), Sohle {p['zulauf_sohle']:g} ueber Tankboden", f"x {f(D['zul_x'])}, y 0, z {f(D['zul_z'])}", "-X"],
         ["Foerderleitung zum Ruecklauf (K58 Linie 1 / K59 Linie 2)", f"Muffe d{p['foerder_d']:g}, hinter {len(D['pumpen_y'])} Rueckschlagventilen d40", f"x {f(p['pumpe_x'])}, y 0, z {f(D['f_top'])}", "+Z"],
         ["Entlueftung mit Insektengitter", f"d{p['entl_d']:g}", f"x {f(D['entl'][0])}, y {f(D['entl'][1])}, z {f(D['entl_top'] + 20)}", "+Z"],
         ["Kabeldurchfuehrung 1 (Pumpen 230 V, 3 Schwimmer)", "Kabelverschraubung M25", f"x {f(D['kabel'][0][0])}, y {f(D['kabel'][0][1])}, z {f(D['kabel_top'])}", "+Z"],
         ["Kabeldurchfuehrung 2 (Ablaufwaechter der Beete 12 V, A+ R47 4.1)", "Kabelverschraubung M25", f"x {f(D['kabel'][1][0])}, y {f(D['kabel'][1][1])}, z {f(D['kabel_top'])}", "+Z"]]
    return P

if __name__ == "__main__":
    b, p, d, D = build()
    out = os.path.join(sc.ROOT, "designs", "components", "beet_sumpf.sc")
    sc.run(b.write("beet_sumpf"), out)
    ev = sc.evaluate(out)
    mn, mx = sc.bbox_all(ev)
    print("Koerper", len(ev["bodies"]), "bbox", [round(v) for v in mn], [round(v) for v in mx], "Masse leer", round(sum(x["mass_g"] for x in ev["bodies"]) / 1000, 1), "kg")
    pth = os.path.join(sc.ROOT, "data", "components", "beet_sumpf.json")
    d["blatt"]["ports"] = ports(p, D)
    json.dump(d, open(pth, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if "--render" in sys.argv:
        rd = os.path.join(sc.ROOT, "renders", "components", "beet_sumpf")
        os.makedirs(rd, exist_ok=True)
        sc.snapshot(out, os.path.join(rd, "beet_sumpf-01-schraeg.png"), [0, 0, 620], 0.7, 0.35, 3000, w=1100, h=900)
        sc.snapshot(out, os.path.join(rd, "beet_sumpf-02-schnitt.png"), [0, 0, 620], 3.14159, 0.0, 3000, w=1100, h=900, section="y=0")
        sc.snapshot(out, os.path.join(rd, "beet_sumpf-03-schnitt-x.png"), [0, 0, 620], -1.5708, 0.0, 3000, w=1100, h=900, section="x=100")
