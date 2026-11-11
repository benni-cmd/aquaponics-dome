"""Bauteile Ring B2 (docs/jobs/N-VARIANTEN.md Abschnitt 4, Schritt V2): Pegelschacht, Ringstuetze d75, Entluefter d75, Ring-Abzweig d40/d32.
Booster = pumpe_gross (kein neues Teil). Ring-Abzweig = Bibliotheksteile (lt_t_d75, lt_reduzierung_*, lt_kugelhahn_*) mit Rohrstuecken, Geometrie
unveraendert aus leitung.py uebernommen (nur verschoben/gespiegelt), damit kein neues Formstueck entsteht.
Aufruf: python -X utf8 scripts/workshop/ringleitung.py [pegelschacht|ringstuetze|entluefter|abzweig] [--json] [--render]"""
import sys, os, json, math
sys.path.insert(0, os.path.dirname(__file__))
import sc
import leitung as L

DC = os.path.join(sc.ROOT, "designs", "components")
MAT = {"LT pehd": (0.95, "#3a3d40"), "LT pvc": (1.4, None), "LT epdm": (1.1, "#1a1a1a"), "LT stahl": (7.85, None), "Schwimmer orange": (0.9, "#f08a24"),
       "PA schwarz": (1.14, "#202020"), "AK Messing": (8.5, "#b5913a")}

def mats(b, names):
    for n in names:
        dens, col = MAT[n]
        col = col or L.COL.get(n.split()[-1], "#9aa0a6")
        b.add("material.create", name=n, density_g_cm3=dens, color=col)

def params(b, p):
    for k, v in p.items():
        if isinstance(v, (int, float)):
            b.add("parameters.add", name=k, expression=f"{v} mm")

def cyl(b, nm, d, h, base, axis, op="new", body=None, targets=None):
    kw = dict(diameter=d, height=h, base=base, axis=axis, operation=op, name=nm)
    if op == "new":
        kw["body_name"] = body or nm
    else:
        kw["targets"] = targets
    b.add("solid.cylinder", **kw)

def bx(b, nm, lx, wy, hz, c, op="new", body=None, targets=None):
    kw = dict(length=lx, width=wy, height=hz, center=c, operation=op, name=nm)
    if op == "new":
        kw["body_name"] = body or nm
    else:
        kw["targets"] = targets
    b.add("solid.box", **kw)

# =========================================================================== 1 Pegelschacht
# KS: Mitte Fassboden aussen (Z 0), Z hoch; Zulauf -X im Deckel, Saugstutzen radial bei +-30 Grad, Notueberlauf radial -X.
PS = dict(fass_d=400.0, fass_h=520.0, wand=4.0, boden=5.0, deckel_d=410.0, deckel_t=15.0,
          zulauf_d=50, zulauf_x=-100.0, saug_d=50, saug_z=100.0, saug_winkel=30.0, ueberlauf_d=63, ueberlauf_z=440.0,
          stutzen_r0=170.0, stutzen_r1=250.0, flansch_d_zu=10.0,
          stange_d=16.0, stange_x=100.0, stange_unten=150.0, schwimmer_d=50.0, schwimmer_h=40.0, schwimmer_bohrung=18.0,
          pegel_aus=250.0, pegel_ein=340.0, kabel_d=24.0, kabel_x=100.0, kabel_y=120.0, entl_d=20.0, entl_y=-120.0)

def ps_geom():
    p = PS
    ri = p["fass_d"] / 2 - p["wand"]
    zt = p["fass_h"]
    of_s, of_u = L.od_f(p["saug_d"]), L.od_f(p["ueberlauf_d"])
    bore_u = p["ueberlauf_d"] - 2 * L.wall_p(p["ueberlauf_d"])
    A = math.pi * (ri / 1000) ** 2                     # m2 Innenquerschnitt; A [m2] x Hoehe [mm] = Liter
    sohle_u = p["ueberlauf_z"] - bore_u / 2
    g = dict(ri=ri, ro=p["fass_d"] / 2, z_deckel=zt, z_deckel_top=zt + p["deckel_t"], of_s=of_s, of_u=of_u, bore_u=bore_u, A=A, sohle_ueberlauf=sohle_u,
             vol_aus_ein_l=A * (p["pegel_ein"] - p["pegel_aus"]), vol_ein_ueberlauf_l=A * (sohle_u - p["pegel_ein"]), vol_bis_ueberlauf_l=A * (sohle_u - p["boden"]),
             saug_dirs=[(math.cos(math.radians(s * p["saug_winkel"])), math.sin(math.radians(s * p["saug_winkel"])), 0.0) for s in (1, -1)])
    return g

def stutzen(b, nm, d, dirv, z, r0, r1, flansch_d, ro, ri, wand_body):
    """Tankdurchfuehrung radial: Rohr od_f(d) von r0 (innen) bis r1 (aussen, Klebemuffe d), Flansch innen und Ringmutter aussen, je 10 dick."""
    of = L.od_f(d); ux, uy, _ = dirv
    P = lambda r: [ux * r, uy * r, z]
    cyl(b, nm + "_Rohr", of, r1 - r0, P(r0), [ux, uy, 0], body=nm)
    cyl(b, nm + "_Flansch", flansch_d, 10, P(ri - 2 - 10), [ux, uy, 0], op="join", targets=[nm])
    cyl(b, nm + "_Mutter", flansch_d, 10, P(ro + 1), [ux, uy, 0], op="join", targets=[nm])
    cyl(b, nm + "_Muffe", d, L.DEPTH[d] + 1, P(r1 - L.DEPTH[d]), [ux, uy, 0], op="cut", targets=[nm])
    cyl(b, nm + "_Bohrung", d - 2 * L.wall_p(d), r1 - r0 + 2, P(r0 - 1), [ux, uy, 0], op="cut", targets=[nm])
    cyl(b, nm + "_Wandloch", of, 40, P(ri - 10), [ux, uy, 0], op="cut", targets=[wand_body])

def pegelschacht():
    p, g = PS, ps_geom()
    b = sc.Build(); nm = "T94_Pegelschacht"
    params(b, p); mats(b, ["LT pehd", "LT pvc", "Schwimmer orange", "PA schwarz"])
    b.add("component.create", name=nm, grounded=True)
    cyl(b, "Fass_R", p["fass_d"], p["fass_h"], [0, 0, 0], [0, 0, 1], body="Fass")
    cyl(b, "Fass_Innen", 2 * g["ri"], p["fass_h"], [0, 0, p["boden"]], [0, 0, 1], op="cut", targets=["Fass"])
    cyl(b, "Deckel_R", p["deckel_d"], p["deckel_t"], [0, 0, g["z_deckel"]], [0, 0, 1], body="Deckel")
    # Zulauf K10/K26: Stutzen d50 durch den Deckel, Klebemuffe oben, Tauchrohr-Anschluss unten (frei ueber dem Ueberlauf)
    of_z = L.od_f(p["zulauf_d"])
    z0, z1 = g["z_deckel"] - 30, g["z_deckel_top"] + 40
    cyl(b, "Zulauf_R", of_z, z1 - z0, [p["zulauf_x"], 0, z0], [0, 0, 1], body="Zulaufstutzen")
    cyl(b, "Zulauf_Kragen", of_z + 20, 8, [p["zulauf_x"], 0, g["z_deckel_top"]], [0, 0, 1], op="join", targets=["Zulaufstutzen"])
    cyl(b, "Zulauf_Muffe", p["zulauf_d"], L.DEPTH[p["zulauf_d"]] + 1, [p["zulauf_x"], 0, z1 - L.DEPTH[p["zulauf_d"]]], [0, 0, 1], op="cut", targets=["Zulaufstutzen"])
    cyl(b, "Zulauf_Bohrung", p["zulauf_d"] - 2 * L.wall_p(p["zulauf_d"]), z1 - z0 + 2, [p["zulauf_x"], 0, z0 - 1], [0, 0, 1], op="cut", targets=["Zulaufstutzen"])
    cyl(b, "Deckel_Zulaufloch", of_z, p["deckel_t"] + 2, [p["zulauf_x"], 0, g["z_deckel"] - 1], [0, 0, 1], op="cut", targets=["Deckel"])
    # Saugstutzen A/B (Booster) und Notueberlauf
    for k, dv in zip(("A", "B"), g["saug_dirs"]):
        stutzen(b, f"Saugstutzen_{k}", p["saug_d"], dv, p["saug_z"], p["stutzen_r0"], p["stutzen_r1"], g["of_s"] + 2 * p["flansch_d_zu"], g["ro"], g["ri"], "Fass")
    stutzen(b, "Notueberlauf", p["ueberlauf_d"], (-1.0, 0.0, 0.0), p["ueberlauf_z"], p["stutzen_r0"], p["stutzen_r1"], g["of_u"] + 2 * p["flansch_d_zu"], g["ro"], g["ri"], "Fass")
    # Schwimmerschalter: Stange am Deckel, zwei Ringschwimmer (AUS unten, EIN oben)
    cyl(b, "Stange_R", p["stange_d"], g["z_deckel_top"] + 20 - p["stange_unten"], [p["stange_x"], 0, p["stange_unten"]], [0, 0, 1], body="Schwimmerstange")
    cyl(b, "Deckel_Stangenloch", p["stange_d"] + 1, p["deckel_t"] + 2, [p["stange_x"], 0, g["z_deckel"] - 1], [0, 0, 1], op="cut", targets=["Deckel"])
    for tag, zp in (("AUS", p["pegel_aus"]), ("EIN", p["pegel_ein"])):
        cyl(b, f"Schwimmer_{tag}_R", p["schwimmer_d"], p["schwimmer_h"], [p["stange_x"], 0, zp - p["schwimmer_h"] / 2], [0, 0, 1], body=f"Schwimmer_{tag}")
        cyl(b, f"Schwimmer_{tag}_Bohrung", p["schwimmer_bohrung"], p["schwimmer_h"] + 2, [p["stange_x"], 0, zp - p["schwimmer_h"] / 2 - 1], [0, 0, 1], op="cut", targets=[f"Schwimmer_{tag}"])
    # Kabelverschraubung M20 und Entlueftungsbohrung im Deckel
    cyl(b, "Kabel_R", p["kabel_d"], 20, [p["kabel_x"], p["kabel_y"], g["z_deckel_top"]], [0, 0, 1], body="Kabelverschraubung")
    cyl(b, "Kabel_Bohrung", 8, 22, [p["kabel_x"], p["kabel_y"], g["z_deckel_top"] - 1], [0, 0, 1], op="cut", targets=["Kabelverschraubung"])
    cyl(b, "Deckel_Kabelloch", 8, p["deckel_t"] + 2, [p["kabel_x"], p["kabel_y"], g["z_deckel"] - 1], [0, 0, 1], op="cut", targets=["Deckel"])
    cyl(b, "Deckel_Entlueftung", p["entl_d"], p["deckel_t"] + 2, [0, p["entl_y"], g["z_deckel"] - 1], [0, 0, 1], op="cut", targets=["Deckel"])
    b.add("material.assign", bodies=["Fass", "Deckel"], material="LT pehd")
    b.add("material.assign", bodies=["Zulaufstutzen", "Saugstutzen_A", "Saugstutzen_B", "Notueberlauf", "Schwimmerstange"], material="LT pvc")
    b.add("material.assign", bodies=["Schwimmer_AUS", "Schwimmer_EIN"], material="Schwimmer orange")
    b.add("material.assign", bodies=["Kabelverschraubung"], material="PA schwarz")
    b.add("component.activate", component=nm)
    b.add("component.metadata.set", component=nm, part_number="T94", revision="A", properties={"Werkstoff": "PE-HD Fass, PVC-U Stutzen"},
          description=f"Pegelschacht Ring B2: Fass PE-HD 60 l (aussen {p['fass_d']:g} x {p['fass_h']:g}), Zulauf d50 im Deckel, 2 Saugstutzen d50 fuer die Booster, Notueberlauf d63, Schwimmerschalter AUS/EIN")
    return b, nm, g

def ps_ports():
    p, g = PS, ps_geom()
    out = [("Zulauf (K10/K26)", (p["zulauf_x"], 0.0, g["z_deckel_top"] + 40), (0.0, 0.0, 1.0), "Muffe", L.DN[p["zulauf_d"]])]
    for k, (ux, uy, _), kn in zip(("A", "B"), g["saug_dirs"], ("K61/K69", "K62/K70")):
        out.append((f"Saug {k} ({kn})", (ux * p["stutzen_r1"], uy * p["stutzen_r1"], p["saug_z"]), (ux, uy, 0.0), "Muffe", L.DN[p["saug_d"]]))
    out.append(("Notueberlauf (K67/K75)", (-p["stutzen_r1"], 0.0, p["ueberlauf_z"]), (-1.0, 0.0, 0.0), "Muffe", L.DN[p["ueberlauf_d"]]))
    out.append(("Kabel Schwimmer", (p["kabel_x"], p["kabel_y"], g["z_deckel_top"] + 20), (0.0, 0.0, 1.0), "Kabelverschraubung", "M20"))
    out.append(("Entlueftung", (0.0, p["entl_y"], g["z_deckel_top"]), (0.0, 0.0, 1.0), "Oeffnung", f"d{p['entl_d']:g}"))
    return [(n, tuple(round(c, 2) for c in pos), tuple(round(c, 4) for c in d), a, dn) for n, pos, d, a, dn in out]

# =========================================================================== 2 Ringstuetze d75
# KS: Mitte Fussplatte unten (Z 0 = Innenboden), Pfosten senkrecht; Kragarm nach +X; Rohr d75 laeuft entlang Y durch (ausladung, 0, achse_h).
RS = dict(achse_h=1550.0,   # U6 (D139): Ring auf 1550 wie die Quelle, vorher 2145
           ausladung=250.0, pfosten_b=50.0, pfosten_w=3.0, arm_b=40.0, arm_w=3.0, arm_ueber=60.0,
          platte_b=200.0, platte_t=10.0, anker_d=10.0, anker_l=100.0, anker_abstand=150.0,
          rohr_d=75.0, einlage_t=3.0, ring_t=3.0, ring_b=30.0, nabe_b=20.0, nabe_h=12.0, stange_d=10.0, mutter_d=17.0, mutter_h=8.0, stange_frei=50.0)

def rs_geom(p=None):
    p = p or RS
    rr_i = p["rohr_d"] / 2 + p["einlage_t"]; rr_o = rr_i + p["ring_t"]
    z_nabe_top = p["achse_h"] + rr_o - 1.5 + p["nabe_h"]
    z_arm_bot = z_nabe_top + p["mutter_h"] + p["stange_frei"]
    z_top = z_arm_bot + p["arm_b"]
    return dict(rr_i=rr_i, rr_o=rr_o, z_unten=p["achse_h"] - rr_o, z_nabe_top=z_nabe_top, z_arm_bot=z_arm_bot, z_top=z_top,
                arm_x0=p["pfosten_b"] / 2, arm_x1=p["ausladung"] + p["arm_ueber"])

def hohlprofil(b, nm, bb, w, c0, c1, axis):
    """Quadratrohr bb x bb x w von c0 bis c1 entlang axis (0 = X, 2 = Z)."""
    ln = c1 - c0
    if axis == 2:
        cx, cy, cz = 0, 0, (c0 + c1) / 2
        bx(b, nm + "_R", bb, bb, ln, [cx, cy, cz], body=nm)
        bx(b, nm + "_Innen", bb - 2 * w, bb - 2 * w, ln + 2, [cx, cy, cz], op="cut", targets=[nm])
    return

def ringstuetze(p=None):
    p = p or RS; g = rs_geom(p)
    b = sc.Build(); nm = "T95_Ringstuetze_d75"
    params(b, p); mats(b, ["LT stahl", "LT epdm"])
    b.add("component.create", name=nm, grounded=True)
    pt = p["platte_t"]
    bx(b, "Platte_R", p["platte_b"], p["platte_b"], pt, [0, 0, pt / 2], body="Fussplatte")
    a = p["anker_abstand"] / 2
    for i, (sx, sy) in enumerate(((-1, -1), (1, -1), (1, 1), (-1, 1)), 1):
        cyl(b, f"Plattenloch_{i}", p["anker_d"] + 2, pt + 2, [sx * a, sy * a, -1], [0, 0, 1], op="cut", targets=["Fussplatte"])
        cyl(b, f"Anker_{i}_Schaft", p["anker_d"], p["anker_l"] + pt, [sx * a, sy * a, -p["anker_l"]], [0, 0, 1], body=f"Anker_{i}")
        cyl(b, f"Anker_{i}_Mutter", p["mutter_d"], p["mutter_h"], [sx * a, sy * a, pt], [0, 0, 1], op="join", targets=[f"Anker_{i}"])
    # Pfosten (aufgeschweisst, Stoss auf der Platte) und Kragarm (seitlich an den Pfosten geschweisst, Stoss an der Pfostenflaeche)
    hohlprofil(b, "Pfosten", p["pfosten_b"], p["pfosten_w"], pt, g["z_top"], 2)
    ab, aw = p["arm_b"], p["arm_w"]
    zc = g["z_arm_bot"] + ab / 2; xc = (g["arm_x0"] + g["arm_x1"]) / 2; ln = g["arm_x1"] - g["arm_x0"]
    bx(b, "Arm_R", ln, ab, ab, [xc, 0, zc], body="Kragarm")
    bx(b, "Arm_Innen", ln + 2, ab - 2 * aw, ab - 2 * aw, [xc, 0, zc], op="cut", targets=["Kragarm"])
    cyl(b, "Arm_Stangenloch", p["stange_d"] + 1, ab + 2, [p["ausladung"], 0, g["z_arm_bot"] - 1], [0, 0, 1], op="cut", targets=["Kragarm"])
    # Haenger: Gewindestange M10 mit Mutter unter und ueber dem Arm
    z0 = g["z_nabe_top"]; z1 = g["z_top"] + p["mutter_h"] + 5
    cyl(b, "Stange_R", p["stange_d"], z1 - z0, [p["ausladung"], 0, z0], [0, 0, 1], body="Gewindestange")
    cyl(b, "Mutter_unten", p["mutter_d"], p["mutter_h"], [p["ausladung"], 0, g["z_arm_bot"] - p["mutter_h"]], [0, 0, 1], op="join", targets=["Gewindestange"])
    cyl(b, "Mutter_oben", p["mutter_d"], p["mutter_h"], [p["ausladung"], 0, g["z_top"]], [0, 0, 1], op="join", targets=["Gewindestange"])
    # Rohrschelle d75 mit EPDM-Einlage, Achse Y, Nabe oben (Gewinde M10, Stange steht auf)
    rb = p["ring_b"]
    cyl(b, "Ring_R", 2 * g["rr_o"], rb, [p["ausladung"], -rb / 2, p["achse_h"]], [0, 1, 0], body="Rohrschelle")
    bx(b, "Nabe_R", p["nabe_b"], rb, p["nabe_h"] + 1.5, [p["ausladung"], 0, z0 - (p["nabe_h"] + 1.5) / 2], op="join", targets=["Rohrschelle"])
    cyl(b, "Ring_Innen", 2 * g["rr_i"], rb + 2, [p["ausladung"], -rb / 2 - 1, p["achse_h"]], [0, 1, 0], op="cut", targets=["Rohrschelle"])
    cyl(b, "Einlage_R", 2 * g["rr_i"], rb, [p["ausladung"], -rb / 2, p["achse_h"]], [0, 1, 0], body="Schelleneinlage")
    cyl(b, "Einlage_Innen", p["rohr_d"], rb + 2, [p["ausladung"], -rb / 2 - 1, p["achse_h"]], [0, 1, 0], op="cut", targets=["Schelleneinlage"])
    b.add("material.assign", bodies=["Fussplatte", "Pfosten", "Kragarm", "Gewindestange", "Rohrschelle", "Anker_1", "Anker_2", "Anker_3", "Anker_4"], material="LT stahl")
    b.add("material.assign", bodies=["Schelleneinlage"], material="LT epdm")
    b.add("component.activate", component=nm)
    b.add("component.metadata.set", component=nm, part_number="T95", revision="A", properties={"Werkstoff": "Stahl verzinkt, EPDM-Einlage"},
          description=f"Ringstuetze d75: Bodenstuetze Quadratrohr {p['pfosten_b']:g}x{p['pfosten_w']:g} auf Fussplatte {p['platte_b']:g}x{p['platte_t']:g} mit 4 Ankern M10, Kragarm {p['arm_b']:g}x{p['arm_w']:g}, "
                      f"Haenger M10 mit Rohrschelle d75; Rohrachse {p['achse_h']:g} ueber Innenboden, Ausladung {p['ausladung']:g}, nichts unter dem Rohr")
    return b, nm, g

def rs_ports(p=None):
    p = p or RS
    return [("Rohrachse (Ring d75)", (p["ausladung"], 0.0, p["achse_h"]), (0.0, 1.0, 0.0), "Aufnahme", L.DN[75]),
            ("Fuss (Innenboden)", (0.0, 0.0, 0.0), (0.0, 0.0, -1.0), "Auflage + 4 Anker M10", "200x200")]

# =========================================================================== 3 Entluefter d75
# KS wie lt_t_d75: Lauf entlang X (Muffe A -X, Muffe B +X), Abgang +Z (nach oben einbauen, Hochpunkt des Halbrings).
EL = dict(d=75, abgang_d=25, abgang_od=40.0, nippel_kopf_d=40.0, nippel_kopf_h=17.6, gewinde_d=33.0, gewinde_h=15.0, ventil_d=52.0, ventil_h=100.0,
          kappe_d=30.0, kappe_h=15.0, luftloch_d=4.0)

def el_geom():
    p = EL; d = p["d"]; a = L.DEPTH[d] + L.od_f(d) / 2
    z_abg = L.od_f(d) / 2 + 40.0                            # Abgang-Muffe oben (40 mm Stutzen ueber dem Lauf)
    z_n0 = z_abg - L.DEPTH[p["abgang_d"]]                  # Nippel-Zapfen steckt in der Muffe
    z_kopf = z_abg + p["nippel_kopf_h"]
    z_v0 = z_kopf; z_v1 = z_v0 + p["ventil_h"]; z_top = z_v1 + p["kappe_h"]
    return dict(a=a, of=L.od_f(d), z_abg=z_abg, z_n0=z_n0, z_kopf=z_kopf, z_v0=z_v0, z_v1=z_v1, z_top=z_top, bore=d - 2 * L.wall_p(d))

def entluefter():
    p, g = EL, el_geom(); d = p["d"]; a, of = g["a"], g["of"]
    b = sc.Build(); nm = "T96_Entluefter_d75"
    params(b, p); mats(b, ["LT pvc", "AK Messing"])
    b.add("component.create", name=nm, grounded=True)
    cyl(b, "Lauf_R", of, 2 * a, [-a, 0, 0], [1, 0, 0], body="Entlueftungs_T")
    cyl(b, "Abgang_R", p["abgang_od"], g["z_abg"], [0, 0, 0], [0, 0, 1], op="join", targets=["Entlueftungs_T"])
    cyl(b, "Muffe_A", d, L.DEPTH[d] + 1, [-a - 1, 0, 0], [1, 0, 0], op="cut", targets=["Entlueftungs_T"])
    cyl(b, "Muffe_B", d, L.DEPTH[d] + 1, [a - L.DEPTH[d], 0, 0], [1, 0, 0], op="cut", targets=["Entlueftungs_T"])
    cyl(b, "Muffe_Abgang", p["abgang_d"], L.DEPTH[p["abgang_d"]] + 1, [0, 0, g["z_n0"]], [0, 0, 1], op="cut", targets=["Entlueftungs_T"])
    cyl(b, "Durchgang", g["bore"], 2 * a + 2, [-a - 1, 0, 0], [1, 0, 0], op="cut", targets=["Entlueftungs_T"])
    cyl(b, "Abgang_Bohrung", p["abgang_d"] - 2 * L.wall_p(p["abgang_d"]), g["z_n0"] + 1, [0, 0, 0], [0, 0, 1], op="cut", targets=["Entlueftungs_T"])
    # Uebergangsnippel PVC: Zapfen d25 in die Muffe, Sechskant, Aussengewinde 1" (d33) ins Ventil
    cyl(b, "Nippel_Zapfen", p["abgang_d"], L.DEPTH[p["abgang_d"]], [0, 0, g["z_n0"]], [0, 0, 1], body="Uebergangsnippel")
    cyl(b, "Nippel_Kopf", p["nippel_kopf_d"], p["nippel_kopf_h"], [0, 0, g["z_abg"]], [0, 0, 1], op="join", targets=["Uebergangsnippel"])
    cyl(b, "Nippel_Gewinde", p["gewinde_d"], p["gewinde_h"], [0, 0, g["z_kopf"]], [0, 0, 1], op="join", targets=["Uebergangsnippel"])
    cyl(b, "Nippel_Bohrung", 18, g["z_kopf"] + p["gewinde_h"] - g["z_n0"] + 2, [0, 0, g["z_n0"] - 1], [0, 0, 1], op="cut", targets=["Uebergangsnippel"])
    # Schnellentlueftungsventil (Schwimmer-Entlueftung) 1": Gehaeuse Messing, Innengewinde unten, Kappe mit Luftaustritt
    cyl(b, "Ventil_R", p["ventil_d"], p["ventil_h"], [0, 0, g["z_v0"]], [0, 0, 1], body="Entlueftungsventil")
    cyl(b, "Ventil_Kappe", p["kappe_d"], p["kappe_h"], [0, 0, g["z_v1"]], [0, 0, 1], op="join", targets=["Entlueftungsventil"])
    cyl(b, "Ventil_Gewinde", p["gewinde_d"] + 0.5, p["gewinde_h"] + 1, [0, 0, g["z_v0"] - 1], [0, 0, 1], op="cut", targets=["Entlueftungsventil"])
    cyl(b, "Ventil_Innen", 40, p["ventil_h"] - p["gewinde_h"] - 10, [0, 0, g["z_v0"] + p["gewinde_h"]], [0, 0, 1], op="cut", targets=["Entlueftungsventil"])
    cyl(b, "Ventil_Luftloch", p["luftloch_d"], p["kappe_h"] + 12, [0, 0, g["z_v1"] - 10], [0, 0, 1], op="cut", targets=["Entlueftungsventil"])
    b.add("material.assign", bodies=["Entlueftungs_T", "Uebergangsnippel"], material="LT pvc")
    b.add("material.assign", bodies=["Entlueftungsventil"], material="AK Messing")
    b.add("component.activate", component=nm)
    b.add("component.metadata.set", component=nm, part_number="T96", revision="A", properties={"Werkstoff": "PVC-U, Messing"},
          description="Entluefter d75 fuer den Hochpunkt des Halbrings: T d75 mit Abgang d25, Uebergangsnippel d25 auf 1 Zoll, Schnellentlueftungsventil 1 Zoll (Schwimmer)")
    return b, nm, g

def el_ports():
    g = el_geom(); a = g["a"]
    return [("A", (-a, 0.0, 0.0), (-1.0, 0.0, 0.0), "Muffe", L.DN[75]), ("B", (a, 0.0, 0.0), (1.0, 0.0, 0.0), "Muffe", L.DN[75]),
            ("Luftaustritt", (0.0, 0.0, round(g["z_top"], 2)), (0.0, 0.0, 1.0), "Oeffnung", "d4")]

# =========================================================================== 4 Ring-Abzweig d40 / d32 (Bibliotheksteile)
# KS: T d75 im Ursprung, Ringlauf entlang X (Muffen A -X, B +X), Abzweig nach unten (-Z): Rohrstueck d75 -> Reduziermuffe d75/d50 -> Rohrstueck d50
# -> Reduziermuffe d50/dk -> Rohrstueck dk -> Kugelhahn dk (Regler); Port Abgang = Muffe B des Hahns (Fallleitung steckt dort).
SPALT = 10.0                                            # sichtbarer Rohrspalt zwischen zwei Muffen (Rohrstueck = t1 + t2 + Spalt)

def ab_kette(dk):
    """Lage der Kette entlang -Z: [(art, fname|None, d, z_portA (oben), z_portB (unten))]."""
    t = L.ports("lt_t_d75"); zc = -t[2][1][2]          # Abgang C nach unten gespiegelt: -86,375
    ch = [("t", "lt_t_d75", 75, 0.0, zc)]
    z = zc
    def stub(d, z_top_port):
        Ls = 2 * L.DEPTH[d] + SPALT
        return ("rohr", None, d, z_top_port + L.DEPTH[d], z_top_port + L.DEPTH[d] - Ls)
    for d_in, fn, d_out in ((75, "lt_reduzierung_d75_d50", 50), (50, f"lt_reduzierung_d50_d{dk}", dk)):
        ch.append(stub(d_in, z)); zA = z - SPALT
        lr = L.ports(fn)[1][1][2]
        ch.append(("red", fn, d_out, zA, zA - lr)); z = zA - lr
    ch.append(stub(dk, z)); zA = z - SPALT
        # Kugelhahn
    lh = L.ports(f"lt_kugelhahn_d{dk}")[1][1][2]
    ch.append(("hahn", f"lt_kugelhahn_d{dk}", dk, zA, zA - lh))
    return ch

KEEP = {"solid.cylinder", "solid.box", "material.assign", "material.create"}

def embed(b, lib_build, tag, z_off, seen_mat):
    """Bibliotheks-Befehle einfuegen: an z = 0 gespiegelt und nach z_off verschoben (z' = z_off - z), Koerper/Features mit tag praefigiert."""
    ren = lambda n: f"{tag}" if n in ("T_Stueck", "Reduzierung", "Kugelhahn") else f"{tag}_{n}"
    for c in lib_build.cmds:
        cm, pr = c["command"], dict(c["params"])
        if cm not in KEEP:
            continue
        if cm == "material.create":
            if pr["name"] in seen_mat:
                continue
            seen_mat.add(pr["name"]); b.add(cm, **pr); continue
        if cm == "material.assign":
            pr["bodies"] = [ren(x) for x in pr["bodies"]]; b.add(cm, **pr); continue
        if "base" in pr:
            x, y, z = pr["base"]; pr["base"] = [x, y, z_off - z]
        if "center" in pr:
            x, y, z = pr["center"]; pr["center"] = [x, y, z_off - z]
        if "axis" in pr:
            ax = pr["axis"]; pr["axis"] = [ax[0], ax[1], -ax[2]]
        elif cm == "solid.cylinder":
            pr["axis"] = [0, 0, -1]
        pr["name"] = f"{tag}_{pr['name']}"
        if "body_name" in pr:
            pr["body_name"] = ren(pr["body_name"])
        if "targets" in pr:
            pr["targets"] = [ren(x) for x in pr["targets"]]
        b.add(cm, **pr)

def abzweig(dk):
    ch = ab_kette(dk)
    b = sc.Build(); nm = f"T97_Ring_Abzweig_d{dk}"
    b.add("parameters.add", name="d_ring", expression="75 mm"); b.add("parameters.add", name="d_abzweig", expression=f"{dk} mm"); b.add("parameters.add", name="spalt", expression=f"{SPALT} mm")
    seen = set()
    b.add("component.create", name=nm, grounded=True)
    builders = {"lt_t_d75": lambda: L.t_stueck(75), "lt_reduzierung_d75_d50": lambda: L.reduzierung(75, 50), f"lt_reduzierung_d50_d{dk}": lambda: L.reduzierung(50, dk),
                f"lt_kugelhahn_d{dk}": lambda: L.kugelhahn(dk)}
    tags = {"lt_t_d75": "T_d75", "lt_reduzierung_d75_d50": "Reduzierung_75_50", f"lt_reduzierung_d50_d{dk}": f"Reduzierung_50_{dk}", f"lt_kugelhahn_d{dk}": f"Kugelhahn_d{dk}"}
    stubs = []
    for art, fn, d, za, zb in ch:
        if art == "t":
            res = builders[fn](); embed(b, res[0], tags[fn], 0.0, seen)
            # t_stueck hat den Abgang nach +Z: Spiegelung z' = -z legt ihn nach unten
        elif art in ("red", "hahn"):
            res = builders[fn](); embed(b, res[0], tags[fn], za, seen)
        else:
            nmr = f"Rohrstueck_d{d}"
            cyl(b, nmr + "_R", d, za - zb, [0, 0, zb], [0, 0, 1], body=nmr)
            cyl(b, nmr + "_Bohrung", d - 2 * L.wall_p(d), za - zb + 2, [0, 0, zb - 1], [0, 0, 1], op="cut", targets=[nmr])
            stubs.append(nmr)
    if "LT pvc" not in seen:
        mats(b, ["LT pvc"])
    b.add("material.assign", bodies=stubs, material="LT pvc")
    b.add("component.activate", component=nm)
    b.add("component.metadata.set", component=nm, part_number=f"T97-{dk}", revision="A", properties={"Werkstoff": "PVC-U"},
          description=f"Ring-Abzweig d75 auf d{dk} aus Bibliotheksteilen: T d75, Reduziermuffen d75/d50 und d50/d{dk}, drei Rohrstuecke, Kugelhahn d{dk} als Regler; Abgang nach unten")
    return b, nm, ch

def ab_ports(dk):
    ch = ab_kette(dk); a = L.ports("lt_t_d75")[1][1][0]
    return [("A (Ring)", (-a, 0.0, 0.0), (-1.0, 0.0, 0.0), "Muffe", L.DN[75]), ("B (Ring)", (a, 0.0, 0.0), (1.0, 0.0, 0.0), "Muffe", L.DN[75]),
            (f"Abgang d{dk} (Fallleitung)", (0.0, 0.0, round(ch[-1][4], 3)), (0.0, 0.0, -1.0), "Muffe", L.DN[dk])]

# =========================================================================== Ausgabe
FILES = {"pegelschacht": "pegelschacht", "ringstuetze": "ringstuetze_d75", "entluefter": "entluefter_d75", "abzweig40": "ring_abzweig_d40", "abzweig32": "ring_abzweig_d32"}

def json_data():
    pg = ps_geom(); rg = rs_geom(); eg = el_geom()
    P = lambda lst: [{"name": n, "lage": list(p), "richtung": list(d), "art": a, "dn": dn} for n, p, d, a, dn in lst]
    return {"quelle": "scripts/workshop/ringleitung.py", "auftrag": "docs/jobs/N-VARIANTEN.md Abschnitt 4 Schritt V2", "booster": "pumpe_gross (vorhandenes Bauteil, kein neues Teil; Ports scripts/trassen_linie.py PORTS pumpe_gross)",
            "teile": {
                "pegelschacht": {"teilenummer": "T94", "parameter": PS, "ks": "Mitte Fassboden aussen, Z hoch",
                                 "pegel": {"saug_achse": PS["saug_z"], "aus": PS["pegel_aus"], "ein": PS["pegel_ein"], "sohle_notueberlauf": round(pg["sohle_ueberlauf"], 1), "fass_oberkante": PS["fass_h"]},
                                 "volumen_l": {"aus_bis_ein": round(pg["vol_aus_ein_l"], 1), "ein_bis_ueberlauf": round(pg["vol_ein_ueberlauf_l"], 1), "boden_bis_ueberlauf": round(pg["vol_bis_ueberlauf_l"], 1)},
                                 "ports": P(ps_ports())},
                "ringstuetze_d75": {"teilenummer": "T95", "parameter": RS, "ks": "Mitte Fussplatte unten = Innenboden, Rohr entlang Y", "unterkante_schelle": round(rg["z_unten"], 1), "hoehe_gesamt": round(rg["z_top"] + RS["mutter_h"] + 5, 1),
                                    "hinweis": "achse_h und ausladung sind Parameter: ringstuetze(dict(RS, achse_h=..., ausladung=...)) erzeugt die Variante", "ports": P(rs_ports())},
                "entluefter_d75": {"teilenummer": "T96", "parameter": EL, "ks": "wie lt_t_d75: Lauf X, Abgang +Z (oben)", "hoehe_ueber_achse": round(eg["z_top"], 1), "ports": P(el_ports())},
                "ring_abzweig_d40": {"teilenummer": "T97-40", "kette": [{"art": a, "teil": f, "d": d, "z_oben": round(za, 3), "z_unten": round(zb, 3), "laenge": round(za - zb, 3)} for a, f, d, za, zb in ab_kette(40)], "ports": P(ab_ports(40))},
                "ring_abzweig_d32": {"teilenummer": "T97-32", "kette": [{"art": a, "teil": f, "d": d, "z_oben": round(za, 3), "z_unten": round(zb, 3), "laenge": round(za - zb, 3)} for a, f, d, za, zb in ab_kette(32)], "ports": P(ab_ports(32))}}}

def render(key, fname):
    rd = os.path.join(sc.ROOT, "renders", "components", "ringleitung"); os.makedirs(rd, exist_ok=True)
    path = os.path.join(DC, fname + ".sc"); out = os.path.join(rd, fname + ".png")
    if key == "pegelschacht":
        sc.snapshot(path, out, [0, 0, 280], 3.14159, 0.3, 1500, w=1000, h=800, section="y=0")
    elif key == "ringstuetze":
        sc.snapshot(path, out, [120, 0, 1150], 2.4, 0.15, 3600, w=900, h=1100)
    elif key == "entluefter":
        sc.snapshot(path, out, [0, 0, 120], 3.14159, 0.2, 700, w=900, h=800, section="y=0")
    else:
        sc.snapshot(path, out, [0, 0, -170], 3.14159, 0.15, 900, w=800, h=1000, section="y=0")
    return out

if __name__ == "__main__":
    want = [a for a in sys.argv[1:] if not a.startswith("--")] or ["pegelschacht", "ringstuetze", "entluefter", "abzweig"]
    jobs = []
    if "pegelschacht" in want: jobs.append(("pegelschacht", pegelschacht))
    if "ringstuetze" in want: jobs.append(("ringstuetze", ringstuetze))
    if "entluefter" in want: jobs.append(("entluefter", entluefter))
    if "abzweig" in want: jobs += [("abzweig40", lambda: abzweig(40)), ("abzweig32", lambda: abzweig(32))]
    for key, fn in jobs:
        res = fn(); out = L.save(res[0], res[1], FILES[key]); print(FILES[key], "->", out)
        if "--render" in sys.argv:
            print("Bild", render(key, FILES[key]))
    if "--json" in sys.argv:
        p = os.path.join(sc.ROOT, "data", "components", "ringleitung_teile.json")
        open(p, "w", encoding="utf-8").write(json.dumps(json_data(), indent=1, ensure_ascii=False) + "\n"); print("geschrieben", p)
