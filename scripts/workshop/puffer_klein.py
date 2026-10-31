"""Kleiner Puffer T82 (W34, R37 Option A, D66): Stammloesungsfass 120 l auf dem Boden, darueber Regalboden mit Messzelle 20 l (Acryl, 4 Sondenstutzen d25),
Eisenchelat-Kanister 20 l und zwei Schlauchpumpen; Stand aus Rechteckrohr 30 x 30 x 2 mit Auffangrand. Grundflaeche 700 x 700 mm, Hoehe unter 1300 mm.
KS: Ursprung Mitte Standflaeche am Boden; X: Messzelle -X, Kanister +X; Y: vorn -Y (Pumpen, Fass wird nach vorn herausgezogen), hinten +Y (Ablauf, Kabel); Z hoch.
Aufruf: python scripts/workshop/puffer_klein.py [--render]   (schreibt auch die Ports ins Blatt data/components/puffer_klein.json)"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc

STEEL = "Stahl verzinkt"

def bar(b, name, a, z_, dims, material=STEEL):
    """Achsparalleles Rechteckrohr von Punkt a bis Punkt z_ (Mittellinie)."""
    ax = [i for i in range(3) if abs(z_[i] - a[i]) > 1e-9]
    assert len(ax) == 1, (name, a, z_)
    i = ax[0]
    lo, hi = (a, z_) if a[i] < z_[i] else (z_, a)
    plane = {0: ([0, 1, 0], [0, 0, 1]), 1: ([0, 0, 1], [1, 0, 0]), 2: ([1, 0, 0], [0, 1, 0])}[i]
    b.add("sketch.create", plane={"origin": list(lo), "x_dir": plane[0], "y_dir": plane[1]}, name="S_" + name)
    b.add("frame.profile.insert", profile=dict(kind="rect_tube", **dims), at=[0, 0], anchor="center")
    b.add("sketch.finish")
    b.add("solid.extrude", distance=abs(hi[i] - lo[i]), name="F_" + name, body_name=name)
    b.add("material.assign", bodies=[name], material=material)

def box(b, name, cx, cy, z0, lx, ly, h, material):
    b.add("solid.box", length=lx, width=ly, height=h, center=[cx, cy, z0 + h / 2], operation="new", name="B_" + name, body_name=name)
    b.add("material.assign", bodies=[name], material=material)

def cyl(b, name, d, h, base, axis, op="new", targets=None, body=None):
    kw = dict(diameter=d, height=h, base=[round(v, 3) for v in base], axis=axis, operation=op, name=name)
    if op == "new":
        kw["body_name"] = body or name
    else:
        kw["targets"] = targets
    b.add("solid.cylinder", **kw)

def derive(p):
    """Abgeleitete Lagen (Bauteil-KS) aus den Parametern: Regalboden, Messzelle, Stutzen, Pumpen; auch Quelle der Ports."""
    D = {}
    z0 = p["regal_z"]
    D["zelle_top"] = z0 + p["zelle_wall"] + p["zelle_ih"]                          # Oberkante Zellkoerper = Unterkante Deckel
    D["zelle_ox"], D["zelle_oy"] = p["zelle_ix"] + 2 * p["zelle_wall"], p["zelle_iy"] + 2 * p["zelle_wall"]
    D["zelle_oh"] = D["zelle_top"] - z0
    D["halter"] = [(p["zelle_cx"] + sx * p["halter_pitch"] / 2, p["zelle_cy"] + sy * p["halter_pitch"] / 2) for sy in (-1, 1) for sx in (-1, 1)]
    D["halter_tip"] = D["zelle_top"] + p["zelle_wall"] + p["halter_h"]
    D["zulauf"] = (p["zelle_cx"] - D["zelle_ox"] / 2 - 25, p["zelle_cy"], z0 + p["zelle_wall"] + p["zelle_zulauf_z"])
    D["ablauf"] = (p["zelle_cx"], p["zelle_cy"] + D["zelle_oy"] / 2 + 25, z0 + p["zelle_wall"] + p["zelle_ablauf_z"])
    D["entn"] = (p["fass_cx"] + p["fass_d"] / 2 + 35, p["fass_cy"], p["entn_z"])
    D["einf"] = (p["fass_cx"], p["fass_cy"] - 120, p["fass_h"] + p["einf_h"])
    D["pump_z"] = z0 + p["pump_h"] / 2
    D["kan_top"] = z0 + p["kan_h"] + p["kap_h"]
    D["kabel"] = (0.0, p["leg_pos"] + p["leg_w"] / 2 + 20, p["rail_z"])
    return D

def build():
    p, d = sc.load_params("puffer_klein")
    D = derive(p)
    unit = {k: v["einheit"] for k, v in d["parameter"].items()}
    b = sc.Build()
    b.params_to_design(p, d, unit)
    for nm, dens, col in ((STEEL, 7.85, "#aeb4b8"), ("HDPE blau", 0.95, "#2a4f8f"), ("Acryl klar", 1.19, "#cfe6ee"), ("PP schwarz", 0.91, "#2b2b2b"), ("Kanister HDPE", 0.95, "#e8e2c8"),
                          ("Pumpe Schlauch", 1.5, "#3a6ea5"), ("PA schwarz", 1.14, "#1f1f1f")):
        b.add("material.create", name=nm, density_g_cm3=dens, color=col, **({"pbr": {"metallic": 0.8, "roughness": 0.45, "dielectric_ior": 1.5}} if nm == STEEL else {}))
    root = "T82_Puffer_Klein"
    b.add("component.create", name=root, grounded=True)
    z0, lp, lw = p["regal_z"], p["leg_pos"], p["leg_w"]
    # --- Stand
    b.add("component.create", name="T82a_Stand")
    dims = dict(width=lw, height=lw, wall=p["leg_wall"])
    ztop = z0 - p["plate_t"]                                                       # Oberkante Pfosten und obere Riegel = Unterkante Regalboden
    inner = lp - lw / 2
    for sx in (-1, 1):
        for sy in (-1, 1):
            tag = f"{'p' if sx > 0 else 'm'}{'p' if sy > 0 else 'm'}"
            box(b, f"Fussplatte_{tag}", sx * lp, sy * lp, 0, p["foot"], p["foot"], p["foot_t"], STEEL)
            bar(b, f"Pfosten_{tag}", [sx * lp, sy * lp, p["foot_t"]], [sx * lp, sy * lp, ztop], dims)
    for k, sy in enumerate((-1, 1), 1):
        bar(b, f"Riegel_oben_x{k}", [-inner, sy * lp, p["rail_z"]], [inner, sy * lp, p["rail_z"]], dims)
    for k, sx in enumerate((-1, 1), 1):
        bar(b, f"Riegel_oben_y{k}", [sx * lp, -inner, p["rail_z"]], [sx * lp, inner, p["rail_z"]], dims)
        bar(b, f"Riegel_unten_y{k}", [sx * lp, -inner, p["low_rail_z"]], [sx * lp, inner, p["low_rail_z"]], dims)
    bar(b, "Riegel_oben_quer", [-inner, 0, p["rail_z"]], [inner, 0, p["rail_z"]], dims)
    bar(b, "Riegel_unten_hinten", [-inner, lp, p["low_rail_z"]], [inner, lp, p["low_rail_z"]], dims)
    box(b, "Regalboden", 0, 0, ztop, p["stand_w"], p["stand_w"], p["plate_t"], STEEL)
    e, rh, rt = p["stand_w"] / 2 - p["rim_t"] / 2, p["rim_h"], p["rim_t"]
    for sy in (-1, 1):
        box(b, f"Auffangrand_{'h' if sy > 0 else 'v'}", 0, sy * e, z0, p["stand_w"], rt, rh, STEEL)
    for sx in (-1, 1):
        box(b, f"Auffangrand_{'r' if sx > 0 else 'l'}", sx * e, 0, z0, rt, p["stand_w"] - 2 * rt, rh, STEEL)
    kx, ky, kz = D["kabel"]
    cyl(b, "Kabelverschraubung_R", p["kabel_od"], 20, [kx, ky - 20, kz], [0, 1, 0], body="Kabelverschraubung")
    cyl(b, "Kabelbohrung", 12, 22, [kx, ky - 21, kz], [0, 1, 0], op="cut", targets=["Kabelverschraubung"])
    b.add("material.assign", bodies=["Kabelverschraubung"], material="PA schwarz")
    # --- Fass 120 l
    b.add("component.activate", component=root)
    b.add("component.create", name="T82b_Fass")
    fx, fy, fd, fh, fl = p["fass_cx"], p["fass_cy"], p["fass_d"], p["fass_h"], p["fass_lid_t"]
    cyl(b, "Fass_R", fd, fh - fl, [fx, fy, 0], [0, 0, 1], body="Fass")
    cyl(b, "Fass_Hohl", fd - 2 * p["fass_wall"], fh, [fx, fy, p["fass_floor"]], [0, 0, 1], op="cut", targets=["Fass"])
    ex, ey, ez = D["entn"]
    cyl(b, "Entnahme_Loch", p["stu_id"], 20, [fx + fd / 2 - p["fass_wall"] - 5, ey, ez], [1, 0, 0], op="cut", targets=["Fass"])        # Loch durch die Fasswand; Stutzen als eigener Koerper (Boolean-Vereinigung mit der duennen Rundung scheitert)
    b.add("material.assign", bodies=["Fass"], material="HDPE blau")
    cyl(b, "Entnahme_Stutzen_R", p["stu_od"], ex - (fx + fd / 2), [fx + fd / 2, ey, ez], [1, 0, 0], body="Fass_Entnahmestutzen")
    cyl(b, "Entnahme_Bohrung", p["stu_id"], ex - (fx + fd / 2) + 2, [fx + fd / 2 - 1, ey, ez], [1, 0, 0], op="cut", targets=["Fass_Entnahmestutzen"])
    b.add("material.assign", bodies=["Fass_Entnahmestutzen"], material="HDPE blau")
    cyl(b, "Deckel_R", fd, fl, [fx, fy, fh - fl], [0, 0, 1], body="Fass_Deckel")
    ix, iy, iz = D["einf"]
    cyl(b, "Einfuell_R", p["einf_od"], p["einf_h"] + fl, [ix, iy, fh - fl], [0, 0, 1], op="join", targets=["Fass_Deckel"])
    cyl(b, "Einfuell_Bohrung", 25, p["einf_h"] + fl + 2, [ix, iy, fh - fl - 1], [0, 0, 1], op="cut", targets=["Fass_Deckel"])
    b.add("material.assign", bodies=["Fass_Deckel"], material="HDPE blau")
    # --- Messzelle 20 l (Acryl)
    b.add("component.activate", component=root)
    b.add("component.create", name="T82c_Messzelle")
    cx, cy, w = p["zelle_cx"], p["zelle_cy"], p["zelle_wall"]
    box(b, "Messzelle", cx, cy, z0, D["zelle_ox"], D["zelle_oy"], D["zelle_oh"], "Acryl klar")
    b.add("solid.box", length=p["zelle_ix"], width=p["zelle_iy"], height=p["zelle_ih"] + 2, center=[cx, cy, z0 + w + (p["zelle_ih"] + 2) / 2], operation="cut", targets=["Messzelle"], name="Messzelle_Hohl")
    zx, zy, zz = D["zulauf"]
    zface = zx + 25                                                                 # Zellwand aussen (x), Tuellenspitze 25 mm davor
    cyl(b, "Zulauf_R", 20, 26, [zface + 1, zy, zz], [-1, 0, 0], op="join", targets=["Messzelle"])
    cyl(b, "Zulauf_Bohrung", p["stu_id"], 25 + w + 4, [zface + w + 2, zy, zz], [-1, 0, 0], op="cut", targets=["Messzelle"])
    ax, ay, az = D["ablauf"]
    aface = ay - 25                                                                 # Zellwand aussen (y) hinten
    cyl(b, "Ablauf_R", p["stu_od"], 26, [ax, aface - 1, az], [0, 1, 0], op="join", targets=["Messzelle"])
    cyl(b, "Ablauf_Bohrung", p["stu_id"], 25 + w + 4, [ax, aface - w - 2, az], [0, 1, 0], op="cut", targets=["Messzelle"])
    box(b, "Messzelle_Deckel", cx, cy, D["zelle_top"], D["zelle_ox"], D["zelle_oy"], w, "Acryl klar")
    for k, (hx, hy) in enumerate(D["halter"], 1):
        cyl(b, f"Halter_R{k}", p["halter_od"], w + p["halter_h"] - 1, [hx, hy, D["zelle_top"] + 1], [0, 0, 1], op="join", targets=["Messzelle_Deckel"])
        cyl(b, f"Halter_Bohrung{k}", p["halter_id"], w + p["halter_h"] + 2, [hx, hy, D["zelle_top"] - 1], [0, 0, 1], op="cut", targets=["Messzelle_Deckel"])
    box(b, "Blende", cx, cy - D["zelle_oy"] / 2 - p["blende_t"] / 2, z0, D["zelle_ox"], p["blende_t"], D["zelle_oh"], "PP schwarz")
    # --- Kanister Eisenchelat 20 l
    b.add("component.activate", component=root)
    b.add("component.create", name="T82d_Kanister")
    kcx, kcy, kw = p["kan_cx"], p["kan_cy"], p["kan_wall"]
    box(b, "Kanister", kcx, kcy, z0, p["kan_l"], p["kan_w"], p["kan_h"], "Kanister HDPE")
    b.add("solid.box", length=p["kan_l"] - 2 * kw, width=p["kan_w"] - 2 * kw, height=p["kan_h"] - 2 * kw, center=[kcx, kcy, z0 + p["kan_h"] / 2], operation="cut", targets=["Kanister"], name="Kanister_Hohl")
    cyl(b, "Kappe_R", p["kap_d"], p["kap_h"], [kcx + 70, kcy - 100, z0 + p["kan_h"]], [0, 0, 1], body="Kanister_Schraubdeckel")
    b.add("material.assign", bodies=["Kanister_Schraubdeckel"], material="Kanister HDPE")
    # --- Pumpen
    b.add("component.activate", component=root)
    b.add("component.create", name="T82e_Pumpen")
    py, pz = p["pump_y"], D["pump_z"]
    for nm, sx in (("Pumpe_Base", -1), ("Pumpe_Eisen", 1)):
        px = sx * p["pump_x"]
        box(b, nm, px, py, z0, p["pump_l"], p["pump_w"], p["pump_h"], "Pumpe Schlauch")
        cyl(b, nm + "_Druck", p["tuelle_od"], p["tuelle_len"] + 1, [px, py - p["pump_w"] / 2 + 1, pz], [0, -1, 0], op="join", targets=[nm])
        cyl(b, nm + "_Saug", p["tuelle_od"], p["tuelle_len"] + 1, [px, py + p["pump_w"] / 2 - 1, pz], [0, 1, 0], op="join", targets=[nm])
    b.add("component.activate", component=root)
    for nm, pn, ds in ((root, "T82", d["beschreibung"]), ("T82a_Stand", "T82a", "Stand 700 x 700 aus Rechteckrohr 30x30x2 mit Regalboden und Auffangrand"), ("T82b_Fass", "T82b", "Stammloesungsfass 120 l HDPE opak mit Deckel, Entnahme- und Einfuellstutzen"),
                       ("T82c_Messzelle", "T82c", "Messzelle 20 l Acryl mit Deckel, 4 Sondenstutzen d25, Zulauf und Ablauf, Lichtschutz-Blende"), ("T82d_Kanister", "T82d", "Eisenchelat-Kanister 20 l HDPE"),
                       ("T82e_Pumpen", "T82e", "2 Schlauchpumpen (Dosierung Base und Eisen)")):
        b.add("component.metadata.set", component=nm, part_number=pn, description=ds, revision="A", properties={"Werkstoff": d["werkstoff"]["name"]})
    return b, p, d, D

def ports(p, D):
    """Ports (Name, DN/Mass, Lage Bauteil-KS (Spitze), Richtung) aus den Parametern."""
    f = lambda v: f"{round(v):d}"
    P = [["Messkreis Zulauf (Messzelle, 3 l/min)", "Tuelle d20, ID 16", f"x {f(D['zulauf'][0])}, y {f(D['zulauf'][1])}, z {f(D['zulauf'][2])}", "-X"],
         ["Ablauf Messzelle -> Pool", "Stutzen d25, ID 16", f"x {f(D['ablauf'][0])}, y {f(D['ablauf'][1])}, z {f(D['ablauf'][2])}", "+Y"]]
    for k, (hx, hy) in enumerate(D["halter"], 1):
        P.append([f"Sondenstutzen {k} (Deckel Messzelle)", "d25, Bohrung 16 (Sondenhalter, Liste R39/W35)", f"x {f(hx)}, y {f(hy)}, z {f(D['halter_tip'])}", "+Z"])
    P += [["Frischwasser / Ansetzen (Einfuellstutzen Fass)", "d32, Bohrung 25", f"x {f(D['einf'][0])}, y {f(D['einf'][1])}, z {f(D['einf'][2])}", "+Z"],
          ["Entnahme Stammloesung (Fass -> Pumpe Base)", "Stutzen d25, ID 16", f"x {f(D['entn'][0])}, y {f(D['entn'][1])}, z {f(D['entn'][2])}", "+X"]]
    for nm, sx, quelle in (("Base", -1, "aus dem Fass"), ("Eisen", 1, "aus dem Kanister")):
        x = sx * p["pump_x"]
        P.append([f"Saug {nm} (Pumpe {nm}, {quelle})", "Tuelle d12 (Schlauch 6/9)", f"x {f(x)}, y {f(p['pump_y'] + p['pump_w'] / 2 + p['tuelle_len'])}, z {f(D['pump_z'])}", "+Y"])
        P.append([f"Dosierleitung {nm} (Pumpe {nm}, Druckseite -> Pool)", "Tuelle d12 (Schlauch 6/9)", f"x {f(x)}, y {f(p['pump_y'] - p['pump_w'] / 2 - p['tuelle_len'])}, z {f(D['pump_z'])}", "-Y"])
    P.append(["Kabel (Netz 230 V, Sonden, Steuerung)", "Kabelverschraubung M20", f"x {f(D['kabel'][0])}, y {f(D['kabel'][1])}, z {f(D['kabel'][2])}", "+Y"])
    return P

if __name__ == "__main__":
    b, p, d, D = build()
    out = os.path.join(sc.ROOT, "designs", "components", "puffer_klein.sc")
    sc.run(b.write("puffer_klein"), out)
    ev = sc.evaluate(out)
    mn, mx = sc.bbox_all(ev)
    print("Koerper", len(ev["bodies"]), "bbox", [round(v) for v in mn], [round(v) for v in mx], "Masse leer", round(sum(x["mass_g"] for x in ev["bodies"]) / 1000, 1), "kg")
    pth = os.path.join(sc.ROOT, "data", "components", "puffer_klein.json")
    d["blatt"]["ports"] = ports(p, D)
    json.dump(d, open(pth, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if "--render" in sys.argv:
        rd = os.path.join(sc.ROOT, "renders", "components", "puffer_klein")
        os.makedirs(rd, exist_ok=True)
        sc.snapshot(out, os.path.join(rd, "puffer_klein-01-schraeg.png"), [0, 0, 600], 0.7, 0.35, 2600, w=1100, h=800)
        sc.snapshot(out, os.path.join(rd, "puffer_klein-02-vorn.png"), [0, 0, 600], 0.0, 0.0, 2600, w=1100, h=800)
        sc.snapshot(out, os.path.join(rd, "puffer_klein-03-schnitt.png"), [0, 0, 600], 1.5708, 0.0, 2600, w=1100, h=800, section="x=0")
