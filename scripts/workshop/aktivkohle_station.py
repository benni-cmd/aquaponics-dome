"""Aktivkohle-Station T83 (W37-2, L05, D66, R45 Abschnitt 5): Sedimentvorfilter, 2 Kompositbehaelter 10 x 35 in Reihe (je 21 l Bett), Probehahn, Durchflussbegrenzer, Abzweige K41/K52.
KS: Mitte der Standflaeche von Behaelter 1 am Boden; X Laengsachse (Eingang -X, Ausgang +X), Y quer (K41 +Y, K52 -Y, Probehahn +Y), Z hoch; Leitungsachse Z = Mantelhoehe + Kopfhoehe/2.
Alles Handelsteile mit Handelsmass-Platzhaltern (Katalog offen, N-BESCHAFFUNG). Rohre stossen stumpf an Koepfe und Formstuecke (keine Ueberlappung).
Aufruf: python -X utf8 scripts/workshop/aktivkohle_station.py [--render]"""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
import leitung as L

MATS = (("AK PVC", 1.4, "#8d9296"), ("AK Hahn", 1.4, "#2a5da8"), ("AK Komposit", 1.5, "#d7dadc"), ("AK Kopf", 1.1, "#2f3338"),
        ("AK Kohle", 0.441, "#26282a"), ("AK Messing", 8.5, "#c9a43a"), ("AK PP", 0.91, "#e8e5d8"), ("AK Konsole", 0.95, "#9aa0a4"))

def geom(p):
    """Abgeleitete Lagen: Mantelhoehe, Leitungshoehe, Behaelterachsen, Rohr-Maße."""
    g = {}
    g["body_h"] = p["vessel_h"] - p["head_h"]
    g["zp"] = g["body_h"] + p["head_h"] / 2
    g["x_v"] = [0, p["vessel_pitch"]][: int(p["behaelter"])]
    g["x_sed"] = -p["vessel_pitch"]
    g["a"] = L.DEPTH[p["pipe_d"]] + L.od_f(p["pipe_d"]) / 2          # Arm des T-Stuecks d25 (Mitte bis Ende)
    return g

def cyl(b, name, base, axis, h, d, mat, op="new", targets=None):
    if op == "new":
        b.add("solid.cylinder", diameter=d, height=h, base=list(base), axis=list(axis), operation="new", name="R_" + name, body_name=name)
        b.add("material.assign", bodies=[name], material=mat)
    else:
        b.add("solid.cylinder", diameter=d, height=h, base=list(base), axis=list(axis), operation=op, targets=targets, name=f"R_{name}_{op}_{len(b.cmds)}")

def tube(b, name, p0, axis, length, d, mat="AK PVC"):
    """Rohr d (Wand L.wall_p) von p0 in Richtung axis (Einheitsvektor) mit Laenge length."""
    cyl(b, name, p0, axis, length, d, mat)
    cyl(b, name, [p0[i] - axis[i] for i in range(3)], axis, length + 2, d - 2 * L.wall_p(d), mat, op="cut", targets=[name])

def hahn(b, name, p0, axis, d, p):
    """Kugelhahn-Platzhalter: Koerper (Formstueck + 12), Bohrung, Spindel und Hebel (offen = parallel zur Rohrachse)."""
    ob = L.od_f(d) + 12
    Lh = p["hahn_l"]
    cyl(b, name, p0, axis, Lh, ob, "AK Hahn")
    cyl(b, name, [p0[i] - axis[i] for i in range(3)], axis, Lh + 2, d - 2 * L.wall_p(d), "AK Hahn", op="cut", targets=[name])
    mid = [p0[i] + axis[i] * Lh / 2 for i in range(3)]
    cyl(b, name + "_Spindel", [mid[0], mid[1], mid[2] + ob / 2], [0, 0, 1], 30, 14, "AK Hahn")
    w = max(8, d / 5)
    sx, sy = abs(axis[0]), abs(axis[1])
    size = [110 * sx + w * sy, 110 * sy + w * sx, 8]
    off = [axis[0] * 40, axis[1] * 40]
    b.add("solid.box", length=size[0], width=size[1], height=size[2], center=[mid[0] + off[0], mid[1] + off[1], mid[2] + ob / 2 + 30 + 4], operation="new", name="R_" + name + "_Hebel", body_name=name + "_Hebel")
    b.add("material.assign", bodies=[name + "_Hebel"], material="AK Hahn")

def tee(b, name, xc, zp, sy, d, a):
    """T-Stueck d (Lauf entlang X, Abgang in sy x Y), Formstueck-Aussen od_f, Bohrung d - 2 wall; Aussen solid + Bohrung geschnitten."""
    of, wi = L.od_f(d), d - 2 * L.wall_p(d)
    cyl(b, name, [xc - a, 0, zp], [1, 0, 0], 2 * a, of, "AK PVC")
    cyl(b, name, [xc, 0, zp], [0, sy, 0], a, of - 0.25, "AK PVC", op="join", targets=[name])           # Abgang 0,25 mm duenner: gleiche Durchmesser ineinander (Tangentennaht) brauchen im Kernel 60 s je Schnitt
    cyl(b, name, [xc - a - 1, 0, zp], [1, 0, 0], 2 * a + 2, wi, "AK PVC", op="cut", targets=[name])
    cyl(b, name, [xc, 0, zp], [0, sy, 0], a + 1, wi - 0.2, "AK PVC", op="cut", targets=[name])

def head(b, name, xc, p, g, with_lever=True):
    bh = g["body_h"]
    b.add("solid.box", length=p["head_w"], width=p["head_w"], height=p["head_h"], center=[xc, 0, bh + p["head_h"] / 2], operation="new", name="R_" + name, body_name=name)
    b.add("material.assign", bodies=[name], material="AK Kopf")
    if with_lever:
        cyl(b, name + "_Hebel", [xc, 0, p["vessel_h"]], [0, 0, 1], 40, 20, "AK Kopf")

def build(p=None):
    p0, d = sc.load_params("aktivkohle_station")
    p = dict(p0, **(p or {}))
    g = geom(p)
    unit = {k: v["einheit"] for k, v in d["parameter"].items()}
    b = sc.Build()
    b.params_to_design(p, d, unit)
    for nm, dens, col in MATS:
        b.add("material.create", name=nm, density_g_cm3=dens, color=col)
    root = "T83_Aktivkohle_Station"
    b.add("component.create", name=root, grounded=True)
    zp, a = g["zp"], g["a"]
    dn, da = p["pipe_d"], p["pipe_d_abz"]
    X, Yp, Ym = [1, 0, 0], [0, 1, 0], [0, -1, 0]
    # --- Vorfilter
    b.add("component.create", name="T83a_Vorfilter")
    xs = g["x_sed"]
    b.add("solid.box", length=p["sed_stand"], width=p["sed_stand"], height=g["body_h"] - p["sed_h"], center=[xs, 0, (g["body_h"] - p["sed_h"]) / 2], operation="new", name="R_Konsole", body_name="Konsole_Sediment")
    b.add("material.assign", bodies=["Konsole_Sediment"], material="AK Konsole")
    z_s = g["body_h"] - p["sed_h"]
    cyl(b, "Sedimentgehaeuse", [xs, 0, z_s], [0, 0, 1], p["sed_h"], p["sed_d"], "AK PP")
    cyl(b, "Sedimentgehaeuse", [xs, 0, z_s + p["sed_wall"]], [0, 0, 1], p["sed_h"] - p["sed_wall"] + 1, p["sed_d"] - 2 * p["sed_wall"], "AK PP", op="cut", targets=["Sedimentgehaeuse"])
    cyl(b, "Sedimentpatrone", [xs, 0, z_s + p["sed_wall"] + 6], [0, 0, 1], p["sed_cart_h"], p["sed_cart_d"], "AK PP")
    head(b, "Kopf_Sediment", xs, p, g, with_lever=False)
    # --- Behaelter
    b.add("component.activate", component=root)
    b.add("component.create", name="T83b_Behaelter")
    for k, xv in enumerate(g["x_v"], 1):
        cyl(b, f"Behaelter_{k}", [xv, 0, 0], [0, 0, 1], g["body_h"], p["vessel_d"], "AK Komposit")
        cyl(b, f"Behaelter_{k}", [xv, 0, p["vessel_wall"]], [0, 0, 1], g["body_h"] - p["vessel_wall"] + 1, p["vessel_d"] - 2 * p["vessel_wall"], "AK Komposit", op="cut", targets=[f"Behaelter_{k}"])
        cyl(b, f"Kohlebett_{k}", [xv, 0, p["bed_z0"]], [0, 0, 1], p["bed_l"], p["bed_d"], "AK Kohle")
        head(b, f"Kopf_{k}", xv, p, g)
    # --- Verrohrung
    b.add("component.activate", component=root)
    b.add("component.create", name="T83c_Verrohrung")
    hw = p["head_w"] / 2
    xe, xo = p["x_in"], p["x_out"]
    ha = p["hahn_l"]
    tube(b, "Rohr_Eingang", [xe, 0, zp], X, 110, dn)
    hahn(b, "Hahn_Eingang", [xe + 110, 0, zp], X, dn, p)
    x = xe + 110 + ha
    tube(b, "Rohr_Hahn_Sediment", [x, 0, zp], X, (xs - hw) - x, dn)
    tube(b, "Rohr_Sediment_B1", [xs + hw, 0, zp], X, (g["x_v"][0] - hw) - (xs + hw), dn)
    t1 = p["t1_x"]
    tube(b, "Rohr_B1_T1", [g["x_v"][0] + hw, 0, zp], X, (t1 - a) - (g["x_v"][0] + hw), dn)
    tee(b, "T_Probehahn", t1, zp, 1, dn, a)
    # Probehahn auf dem Abgang +Y
    tap_cy = a
    cyl(b, "Probehahn", [t1, tap_cy, zp], Yp, p["tap_l"], p["tap_d"], "AK Messing")
    cyl(b, "Probehahn", [t1, tap_cy + p["tap_l"], zp], Yp, p["spout_l"], p["spout_d"], "AK Messing", op="join", targets=["Probehahn"])
    cyl(b, "Probehahn", [t1, tap_cy + p["tap_l"] - 1, zp], Yp, p["spout_l"] + 2, p["spout_d"] - 4, "AK Messing", op="cut", targets=["Probehahn"])
    b.add("solid.box", length=8, width=40, height=8, center=[t1, tap_cy + p["tap_l"] / 2 - 5, zp + p["tap_d"] / 2 + 4], operation="new", name="R_Probehahn_Griff", body_name="Probehahn_Griff")
    b.add("material.assign", bodies=["Probehahn_Griff"], material="AK Messing")
    if int(p["behaelter"]) == 2:
        x2 = g["x_v"][1]
        tube(b, "Rohr_T1_B2", [t1 + a, 0, zp], X, (x2 - hw) - (t1 + a), dn)
        tube(b, "Rohr_B2_Begrenzer", [x2 + hw, 0, zp], X, p["lim_x"] - (x2 + hw), dn)
    else:
        tube(b, "Rohr_T1_Begrenzer", [t1 + a, 0, zp], X, p["lim_x"] - (t1 + a), dn)
    xl = p["lim_x"]
    cyl(b, "Begrenzer", [xl, 0, zp], X, p["lim_l"], p["lim_d"], "AK Messing")
    cyl(b, "Begrenzer", [xl - 1, 0, zp], X, p["lim_l"] + 2, dn - 2 * L.wall_p(dn), "AK Messing", op="cut", targets=["Begrenzer"])
    t2, t3 = p["t2_x"], p["t3_x"]
    tube(b, "Rohr_Begrenzer_T2", [xl + p["lim_l"], 0, zp], X, (t2 - a) - (xl + p["lim_l"]), dn)
    tee(b, "T_K41", t2, zp, 1, dn, a)
    tube(b, "Rohr_T2_T3", [t2 + a, 0, zp], X, (t3 - a) - (t2 + a), dn)
    tee(b, "T_K52", t3, zp, -1, dn, a)
    x_h = t3 + a + 45
    tube(b, "Rohr_T3_Hahn", [t3 + a, 0, zp], X, x_h - (t3 + a), dn)
    hahn(b, "Hahn_K40", [x_h, 0, zp], X, dn, p)
    tube(b, "Rohr_Ausgang_K40", [x_h + ha, 0, zp], X, xo - (x_h + ha), dn)
    # K41: Reduzierung d25 -> d20, Hahn d20, Rohr d20
    lr = L.DEPTH[dn] + L.DEPTH[da] + 6
    cyl(b, "Reduzierung_K41", [t2, a, zp], Yp, lr, L.od_f(dn), "AK PVC")
    cyl(b, "Reduzierung_K41", [t2, a - 1, zp], Yp, lr + 2, da - 2 * L.wall_p(da), "AK PVC", op="cut", targets=["Reduzierung_K41"])
    hahn(b, "Hahn_K41", [t2, a + lr, zp], Yp, da, p)
    tube(b, "Rohr_K41", [t2, a + lr + ha, zp], Yp, p["abz_y"] - (a + lr + ha), da)
    # K52: Hahn d25, Rohr d25
    hahn(b, "Hahn_K52", [t3, -a - ha, zp], Yp, dn, p)
    tube(b, "Rohr_K52", [t3, -a - ha - ((p["abz_y"]) - (a + ha)), zp], Yp, p["abz_y"] - (a + ha), dn)
    b.add("component.activate", component=root)
    for nm, pn, ds in ((root, "T83", d["beschreibung"]), ("T83a_Vorfilter", "T83a", "Sedimentgehaeuse 10 Zoll mit Patrone 20 um auf Konsole"),
                       ("T83b_Behaelter", "T83b", "Kompositbehaelter 10 x 35 mit Kopf und katalytischer Kohle (21 l Bett)"), ("T83c_Verrohrung", "T83c", "Verrohrung d25/d20, Kugelhaehne, T-Stuecke, Probehahn, Begrenzer 4 l/min")):
        b.add("component.metadata.set", component=nm, part_number=pn, description=ds, revision="A", properties={"Werkstoff": "PVC-U / Komposit / Messing"})
    return b

if __name__ == "__main__":
    out = os.path.join(sc.ROOT, "designs", "components", "aktivkohle_station.sc")
    sc.run(build().write("aktivkohle_station"), out)
    ev = sc.evaluate(out)
    mn, mx = sc.bbox_all(ev)
    print("Koerper", len(ev["bodies"]), "bbox", [round(v, 1) for v in mn], [round(v, 1) for v in mx])
    if "--render" in sys.argv:
        rd = os.path.join(sc.ROOT, "renders", "components", "aktivkohle_station")
        os.makedirs(rd, exist_ok=True)
        sc.snapshot(out, os.path.join(rd, "aktivkohle_station-01-schraeg.png"), [50, 0, 450], 0.6, 0.35, 2300, w=1100, h=720)
        sc.snapshot(out, os.path.join(rd, "aktivkohle_station-02-oben.png"), [50, 0, 450], 0.0, 1.5, 2300, w=1100, h=720)
        sc.snapshot(out, os.path.join(rd, "aktivkohle_station-03-schnitt.png"), [50, 0, 450], 0.0, 0.0, 2300, w=1100, h=720, section="y=0")
