"""Werkstatt WA-T (docs/jobs/N-AUTOBAHN-V2.md Abschnitt 3): Tragwerk der Wasserautobahn (Ring B2).
WA1 portal_joch_mitte_a/_b, WA2 ausleger_schlauch_<L>, WA2b ringstuetze_d75_b (Rev. B von T95), WA3 montageschiene_41 + lt_klemme_d75 + schienenverbinder_36,
WA4 ring_ecke_d75, WA7 pegelschacht_podest.

Hoehenkette (relativ Innenboden, absolut = +400), fuer alle Stuetzpunkte gleich:
  Ring-Achse 2145 -> Schelle unten 2101,5 (>= 2100) -> Schellen-Nabe oben 2199 -> Montageschiene 2212..2253 (Schlitz unten)
  -> Ausgleichsplatte 4 mm 2253..2257 -> Querriegel / Kragarm / Ausleger 2257..2297 (Korridor KR bis 2300).
Der Ring HAENGT unter der Schiene (Installationspraxis, Strut + Haengeschelle). Laege er auf der Schiene, laege die Schiene unter Z 2100.

Aufruf: python -X utf8 scripts/workshop/autobahn_t.py [joch|ausleger|stelze|schiene|klemme|verbinder|ecke|podest] [--json] [--render]"""
import sys, os, json, math
sys.path.insert(0, os.path.dirname(__file__))
import sc
import leitung as L
import ringleitung as R

DC = os.path.join(sc.ROOT, "designs", "components")
RD = os.path.join(sc.ROOT, "renders", "components", "autobahn")
MAT = {"AB stahl": (7.85, "#aeb4b8"), "AB epdm": (1.1, "#1a1a1a"), "AB pe100": (0.96, "#20242a"), "AB schiene": (7.85, "#c9ced2")}

# --------------------------------------------------------------------------- Hoehenkette und Lage (gemessen, siehe Blatt)
# N-UNIFY-AUTOBAHN U6 (D98, D139): Ring auf Rohrachse 1550 rel wie die Quelle (Oasis-Showcase); die ganze Hoehenkette sinkt um 595 mm (vorher achse 2145).
# gang_frei ist die lichte Hoehe unter dem Ring (Pruefwert, kein Mass der Quelle): mit 1550 liegt sie bei 1505 (Bedenken D111).
DZ_U6 = -595.0
Z = {k: v + DZ_U6 for k, v in dict(achse=2145.0, schelle_unten=2101.5, nabe=2199.0, schiene_u=2212.0, schiene_o=2253.0, platte_o=2257.0, traeger_o=2297.0, kr_oben=2300.0, gang_frei=2100.0).items()}
AP_MITTE = 3377.0          # [E] Tisch_mitte / Beet_innen_933 im Modell (nft_tisch.json ap_c 3277 + params ring_shift_mid 100, D63), scripts/dome-script.json
AP_INNEN, AP_AUSSEN = 1864.0, 5074.0
HALB = math.radians(18.0)
R_ECKE = AP_MITTE / math.cos(HALB)            # 3551 mm
SEITE = 2 * AP_MITTE * math.tan(HALB)         # 2194 mm
AUSL_ZIEL = {"innen": R_ECKE - AP_INNEN / math.cos(HALB), "aussen": AP_AUSSEN / math.cos(HALB) - R_ECKE}   # radial ab Ring wie Planer-Rechnung Abschn. 3, mit echten Radien

def mats(b, names):
    for n in names:
        d, c = MAT[n]; b.add("material.create", name=n, density_g_cm3=d, color=c)

def params(b, p):
    for k, v in p.items():
        if isinstance(v, (int, float)) and not isinstance(v, bool):
            b.add("parameters.add", name=k, expression=f"{v} mm")

def bx(b, nm, x0, x1, y0, y1, z0, z1, op="new", body=None, targets=None):
    kw = dict(length=x1 - x0, width=y1 - y0, height=z1 - z0, center=[(x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2], operation=op, name=nm)
    if op == "new": kw["body_name"] = body or nm
    else: kw["targets"] = targets
    b.add("solid.box", **kw)

def cyl(b, nm, d, h, base, axis, op="new", body=None, targets=None):
    kw = dict(diameter=d, height=h, base=base, axis=axis, operation=op, name=nm)
    if op == "new": kw["body_name"] = body or nm
    else: kw["targets"] = targets
    b.add("solid.cylinder", **kw)

def rohr4(b, nm, ax, a0, a1, c1, c2, s=40.0, w=3.0):
    """Quadratrohr s x s x w entlang Achse ax (0 X, 1 Y, 2 Z) von a0 bis a1; c1, c2 = Mitte der beiden anderen Achsen (in Reihenfolge)."""
    lo, hi = [0, 0, 0], [0, 0, 0]
    o = [i for i in range(3) if i != ax]
    lo[ax], hi[ax] = a0, a1
    lo[o[0]], hi[o[0]] = c1 - s / 2, c1 + s / 2
    lo[o[1]], hi[o[1]] = c2 - s / 2, c2 + s / 2
    bx(b, nm + "_R", lo[0], hi[0], lo[1], hi[1], lo[2], hi[2], body=nm)
    li, hj = list(lo), list(hi)
    li[ax] -= 1; hj[ax] += 1
    for i in o: li[i] += w; hj[i] -= w
    bx(b, nm + "_Innen", li[0], hj[0], li[1], hj[1], li[2], hj[2], op="cut", targets=[nm])

def meta(b, nm, pn, desc, werk):
    b.add("component.activate", component=nm)
    b.add("component.metadata.set", component=nm, part_number=pn, revision="A", properties={"Werkstoff": werk}, description=desc)

# =========================================================================== WA1 Portal-Joch (KS = Tisch-KS nft_tisch_mitte: X tangential CCW, Y radial innen, Z ab Innenboden)
# Bestand (solidcraft-cli eval designs/components/nft_tisch_mitte.sc): Bock 1 Beine x -478..-437, Diagonale aussen x -480..-478; Bock 2 Beine x 528..568,
# Diagonale aussen x 568..570; Beine y -567..-526 / 526..567, Hoehe 5..948 (Bock 1) / 932 (Bock 2); Laengsdiagonalen und Laengsstreben innen (zwischen den Boecken).
# Aussenkante je Bock = Diagonalen-Schrauben M6x40 bzw. Muttern (eval: Bock 1 bis x -484, Bock 2 bis x 574), nicht die Diagonale selbst
TISCH = {"a": dict(bein=(-478.0, -437.0), diag_aussen=(-484.0, -478.0), s=-1), "b": dict(bein=(528.0, 568.0), diag_aussen=(568.0, 574.0), s=1)}
JO = dict(profil=40.0, wand=3.0, luft_diag=2.0, bein_y0=526.0, bein_y1=567.0, ext_z0=150.0, klemm_z=((250.0, 310.0), (600.0, 660.0)), klemm_t=6.0, schraube_d=8.0,
          stirn_t=8.0, stirn_b=100.0, platte_b=60.0)

def jo_geom(seite):
    t, p = TISCH[seite], JO
    s = t["s"]
    if s < 0:
        e1 = t["diag_aussen"][0] - p["luft_diag"]; e0 = e1 - p["profil"]
        dist = (e1, t["bein"][0])                         # Distanzblech zwischen Verlaengerung und Bein
        px0, px1 = e0 - 12, t["bein"][1] + 12
        bolts = (e0 - 6, t["bein"][1] + 6)
    else:
        e0 = t["diag_aussen"][1] + p["luft_diag"]; e1 = e0 + p["profil"]
        dist = (t["bein"][1], e0)
        px0, px1 = t["bein"][0] - 12, e1 + 12
        bolts = (t["bein"][0] - 6, e1 + 6)
    xe = (e0 + e1) / 2
    y_end = p["bein_y1"]
    return dict(e0=e0, e1=e1, xe=xe, dist=dist, px=(px0, px1), bolts=bolts, y_end=y_end, y_flansch=y_end + p["stirn_t"],
                abstand_ecke=SEITE / 2 - abs(xe))

def joch(seite):
    p, g = JO, jo_geom(seite)
    b = sc.Build(); nm = f"WA1_Portal_Joch_Mitte_{seite.upper()}"
    params(b, {k: v for k, v in p.items() if not isinstance(v, tuple)}); mats(b, ["AB stahl"])
    b.add("component.create", name=nm, grounded=True)
    yc = (p["bein_y0"] + p["bein_y1"]) / 2
    bodies = []
    for sy, tag in ((1, "innen"), (-1, "aussen")):
        n = f"Verlaengerung_{tag}"; rohr4(b, n, 2, p["ext_z0"], Z["platte_o"], g["xe"], sy * yc); bodies.append(n)
        cap = f"Fusskappe_{tag}"; bx(b, cap, g["e0"], g["e1"], sy * yc - 20, sy * yc + 20, p["ext_z0"] - 4, p["ext_z0"]); bodies.append(cap)
        for k, (z0, z1) in enumerate(p["klemm_z"], 1):
            d = f"Distanz_{tag}_{k}"; bx(b, d, g["dist"][0], g["dist"][1], sy * yc - 20, sy * yc + 20, z0, z1); bodies.append(d)
            for side, (y0, y1) in (("aussen", (p["bein_y1"], p["bein_y1"] + p["klemm_t"])), ("innen", (p["bein_y0"] - p["klemm_t"], p["bein_y0"]))):
                yy = (y0, y1) if sy > 0 else (-y1, -y0)
                kp = f"Klemmplatte_{tag}_{k}_{side}"; bx(b, kp, g["px"][0], g["px"][1], yy[0], yy[1], z0, z1); bodies.append(kp)
                for j, xb in enumerate(g["bolts"]):
                    cyl(b, f"{kp}_Loch_{j + 1}", p["schraube_d"] + 1, yy[1] - yy[0] + 2, [xb, yy[0] - 1, (z0 + z1) / 2], [0, 1, 0], op="cut", targets=[kp])
            for j, xb in enumerate(g["bolts"]):
                sn = f"Schraube_{tag}_{k}_{j + 1}"
                y_lo = p["bein_y0"] - p["klemm_t"] - 8; y_hi = p["bein_y1"] + p["klemm_t"] + 8
                base = [xb, sy * y_lo if sy > 0 else -y_hi, (z0 + z1) / 2]
                cyl(b, sn, p["schraube_d"], y_hi - y_lo, base, [0, 1, 0]); bodies.append(sn)
    # Querriegel auf den Verlaengerungen, Stirnplatten fuer die Ausleger, Ausgleichsplatte unter dem Riegel ueber der Schiene
    rohr4(b, "Querriegel", 1, -g["y_end"], g["y_end"], g["xe"], (Z["platte_o"] + Z["traeger_o"]) / 2); bodies.append("Querriegel")
    for sy, tag in ((1, "innen"), (-1, "aussen")):
        n = f"Stirnplatte_{tag}"; y0, y1 = (g["y_end"], g["y_flansch"]) if sy > 0 else (-g["y_flansch"], -g["y_end"])
        bx(b, n, g["xe"] - p["stirn_b"] / 2, g["xe"] + p["stirn_b"] / 2, y0, y1, Z["platte_o"], Z["traeger_o"]); bodies.append(n)
    bx(b, "Ausgleichsplatte", g["xe"] - p["platte_b"] / 2, g["xe"] + p["platte_b"] / 2, -20.5, 20.5, Z["schiene_o"], Z["platte_o"]); bodies.append("Ausgleichsplatte")
    b.add("material.assign", bodies=bodies, material="AB stahl")
    meta(b, nm, f"WA1-{seite.upper()}", f"Portal-Joch Mitteltisch Bock {'1 (-X)' if seite == 'a' else '2 (+X)'}: 2 Verlaengerungen 40x40x3 neben den Bestandsbeinen, je 2 Klemmen (Platten 6 mm, 2 x M8), "
         f"Querriegel 40x40x3 auf Z {Z['platte_o']:g}..{Z['traeger_o']:g}, Ausgleichsplatte fuer Montageschiene 41, 2 Stirnplatten fuer Ausleger; kein Schweissen am Tisch", "Stahl S235 feuerverzinkt")
    return b, nm, g

def jo_ports(seite):
    g = jo_geom(seite)
    return [("Schiene (Auflage Oberkante Montageschiene 41)", (g["xe"], 0.0, Z["schiene_o"]), (0.0, 0.0, -1.0), "Auflage", "Schiene 41"),
            ("Ausleger innen (Stirnplatte)", (g["xe"], g["y_flansch"], (Z["platte_o"] + Z["traeger_o"]) / 2), (0.0, 1.0, 0.0), "Flansch", "2 x M10"),
            ("Ausleger aussen (Stirnplatte)", (g["xe"], -g["y_flansch"], (Z["platte_o"] + Z["traeger_o"]) / 2), (0.0, -1.0, 0.0), "Flansch", "2 x M10")]

# =========================================================================== WA2 Ausleger (KS: Flanschanlage x 0, Arm +X, Seiten +-Y, Armmitte z 0)
AU = dict(profil=40.0, wand=3.0, flansch_t=8.0, flansch_b=100.0, halter_raster=400.0, schlauch_ad_max=35.0, clip_wand=2.0, clip_b=20.0, halter_t=3.0,
          biege_r=210.0, sattel_t=4.0, schraube_d=10.0)

def au_geom(lg):
    p = AU
    yh = p["profil"] / 2 + p["halter_t"] + p["schlauch_ad_max"] / 2 + p["clip_wand"]      # Schlauchachse seitlich
    n = math.ceil((lg - p["flansch_t"]) / p["halter_raster"])
    xs = [p["flansch_t"] + (lg - p["flansch_t"]) * (k + 0.5) / n for k in range(n)] if n else []
    rs = p["biege_r"] - p["schlauch_ad_max"] / 2                                            # Sattelflaeche unter dem Schlauch
    return dict(yh=yh, xs=xs, rs=rs, sattel_b=2 * (yh + p["schlauch_ad_max"] / 2 + p["clip_wand"] + 5))

def ausleger(lg):
    p, g = AU, au_geom(lg)
    b = sc.Build(); nm = f"WA2_Ausleger_Schlauch_{lg:.0f}"
    params(b, dict(p, laenge=lg)); mats(b, ["AB stahl", "AB epdm"])
    b.add("component.create", name=nm, grounded=True)
    h = p["profil"] / 2
    bx(b, "Flansch", 0, p["flansch_t"], -p["flansch_b"] / 2, p["flansch_b"] / 2, -h, h)
    for j, sy in enumerate((-1, 1), 1):
        cyl(b, f"Flansch_Loch_{j}", p["schraube_d"] + 1, p["flansch_t"] + 2, [-1, sy * 38, 0], [1, 0, 0], op="cut", targets=["Flansch"])
    rohr4(b, "Arm", 0, p["flansch_t"], lg, 0.0, 0.0)
    bodies = ["Flansch", "Arm"]; rubber = []
    for k, x in enumerate(g["xs"], 1):
        for sy, tag in ((1, "l"), (-1, "r")):
            hn = f"Halter_{k}_{tag}"
            y0 = sy * h; y1 = sy * (h + p["halter_t"])
            bx(b, hn, x - p["clip_b"] / 2, x + p["clip_b"] / 2, min(y0, y1), max(y0, y1), -h, h)
            ro = p["schlauch_ad_max"] + 2 * p["clip_wand"]
            cyl(b, hn + "_Ring", ro, p["clip_b"], [x - p["clip_b"] / 2, sy * g["yh"], 0], [1, 0, 0], op="join", targets=[hn])
            cyl(b, hn + "_Ringloch", p["schlauch_ad_max"], p["clip_b"] + 2, [x - p["clip_b"] / 2 - 1, sy * g["yh"], 0], [1, 0, 0], op="cut", targets=[hn])
            bodies.append(hn)
    # Endbuegel: Stirnplatte + Viertel-Sattel R = Biegeradius Schlauch (6 x AD, Leitungsordnung R14) um die Achse Y bei (lg, -, -biege_r)
    sb = g["sattel_b"]; zc = -p["biege_r"]; ri = g["rs"] - p["sattel_t"]
    bx(b, "Endbuegel", lg, lg + 5, -sb / 2, sb / 2, -h, h)
    cyl(b, "Sattel_R", 2 * g["rs"], sb, [lg, -sb / 2, zc], [0, 1, 0], op="join", targets=["Endbuegel"])
    cyl(b, "Sattel_Innen", 2 * ri, sb + 2, [lg, -sb / 2 - 1, zc], [0, 1, 0], op="cut", targets=["Endbuegel"])
    bx(b, "Sattel_Cut_x", lg - g["rs"] - 10, lg, -sb / 2 - 2, sb / 2 + 2, zc - g["rs"] - 10, zc + g["rs"] + 10, op="cut", targets=["Endbuegel"])
    bx(b, "Sattel_Cut_z", lg - g["rs"] - 10, lg + g["rs"] + 10, -sb / 2 - 2, sb / 2 + 2, zc - g["rs"] - 10, zc, op="cut", targets=["Endbuegel"])
    bodies.append("Endbuegel")
    b.add("material.assign", bodies=bodies, material="AB stahl")
    meta(b, nm, f"WA2-{lg:.0f}", f"Ausleger Schlauch {lg:.0f}: Kragarm 40x40x3 mit Flansch 100x40x8 (2 x M10), {len(g['xs'])} Halterpaare (Raster <= {p['halter_raster']:g}) fuer Schlauch bis AD {p['schlauch_ad_max']:g} beidseits, "
         f"Endbuegel mit Sattel R {p['biege_r']:g} fuer den freien Fall; kein Kopfband (wuerde unter Z 2100 in den Gang ragen)", "Stahl S235 feuerverzinkt")
    return b, nm, g

def au_ports(lg):
    g = au_geom(lg)
    out = [("Flansch (an Joch/Stelze)", (0.0, 0.0, 0.0), (-1.0, 0.0, 0.0), "Flansch", "2 x M10")]
    for k, x in enumerate(g["xs"], 1):
        for sy, tag in ((1, "l"), (-1, "r")):
            out.append((f"Halter {k} {tag} (Schlauchachse)", (round(x, 1), sy * g["yh"], 0.0), (1.0, 0.0, 0.0), "Schlauchclip", f"AD <= {AU['schlauch_ad_max']:g}"))
    for sy, tag in ((1, "l"), (-1, "r")):
        out.append((f"Fall {tag} (Schlauch senkrecht nach dem Sattel)", (round(lg + AU["biege_r"], 1), sy * g["yh"], -AU["biege_r"]), (0.0, 0.0, -1.0), "Schlauchfuehrung", "frei"))
    return out

# =========================================================================== WA2b Ringstuetze Rev. B (KS wie T95: Pfosten im Ursprung, Kragarm +X, Ring entlang Y bei x 250)
def stelze():
    p = dict(R.RS); g = R.rs_geom(p)
    b = sc.Build(); nm = "T95B_Ringstuetze_d75_RevB"
    params(b, p); mats(b, ["AB stahl"])
    b.add("component.create", name=nm, grounded=True)
    pt = p["platte_t"]
    bx(b, "Platte_R", -p["platte_b"] / 2, p["platte_b"] / 2, -p["platte_b"] / 2, p["platte_b"] / 2, 0, pt, body="Fussplatte")
    a = p["anker_abstand"] / 2; bodies = ["Fussplatte"]
    for i, (sx, sy) in enumerate(((-1, -1), (1, -1), (1, 1), (-1, 1)), 1):
        cyl(b, f"Plattenloch_{i}", p["anker_d"] + 2, pt + 2, [sx * a, sy * a, -1], [0, 0, 1], op="cut", targets=["Fussplatte"])
        cyl(b, f"Anker_{i}_Schaft", p["anker_d"], p["anker_l"] + pt, [sx * a, sy * a, -p["anker_l"]], [0, 0, 1], body=f"Anker_{i}")
        cyl(b, f"Anker_{i}_Mutter", p["mutter_d"], p["mutter_h"], [sx * a, sy * a, pt], [0, 0, 1], op="join", targets=[f"Anker_{i}"]); bodies.append(f"Anker_{i}")
    rohr4(b, "Pfosten", 2, pt, g["z_top"], 0.0, 0.0, s=p["pfosten_b"], w=p["pfosten_w"]); bodies.append("Pfosten")
    zc = (Z["platte_o"] + Z["traeger_o"]) / 2
    assert abs(g["z_arm_bot"] - Z["platte_o"]) < 0.01 and abs(g["z_top"] - Z["traeger_o"]) < 0.01
    xs = p["ausladung"] + ec_geom()["stich"]                 # Bogenscheitel des Rings: Stelze steht auf der Winkelhalbierenden der Ecke
    x1 = xs + p["arm_ueber"]
    rohr4(b, "Kragarm", 0, p["pfosten_b"] / 2, x1, 0.0, zc, s=p["arm_b"], w=p["arm_w"]); bodies.append("Kragarm")
    cyl(b, "Kragarm_Loch", KL["stummel_d"] + 1, p["arm_b"] + 2, [xs, 0, Z["platte_o"] - 1], [0, 0, 1], op="cut", targets=["Kragarm"])
    rohr4(b, "Gegenarm", 0, -p["pfosten_b"] / 2 - 35, -p["pfosten_b"] / 2, 0.0, zc, s=p["arm_b"], w=p["arm_w"]); bodies.append("Gegenarm")
    xa = -p["pfosten_b"] / 2 - 35
    bx(b, "Stirnplatte_plus", x1, x1 + JO["stirn_t"], -JO["stirn_b"] / 2, JO["stirn_b"] / 2, Z["platte_o"], Z["traeger_o"]); bodies.append("Stirnplatte_plus")
    bx(b, "Stirnplatte_minus", xa - JO["stirn_t"], xa, -JO["stirn_b"] / 2, JO["stirn_b"] / 2, Z["platte_o"], Z["traeger_o"]); bodies.append("Stirnplatte_minus")
    b.add("material.assign", bodies=bodies, material="AB stahl")
    meta(b, nm, "T95-B", "Ringstuetze d75 Rev. B (Autobahn, steht an einer Ringecke): wie T95 (Fussplatte, Pfosten 50x50x3, Kragarm 40x40x3), aber ohne Haenger: der Schienenverbinder 36 liegt unter dem Kragarm bei x 250, "
         "die Scheitel-Schelle haengt am Kragarm ueber dem Bogenscheitel; "
         "Stirnplatten fuer Ausleger an beiden Armenden (+X am Kragarm, -X am Gegenarm). Rev. A bleibt fuer A+-freie Varianten gueltig", "Stahl S235 feuerverzinkt")
    return b, nm, dict(g, x_plus=x1 + JO["stirn_t"], x_minus=xa - JO["stirn_t"], x_scheitel=xs)

def st_ports():
    g = stelze()[2]; zc = (Z["platte_o"] + Z["traeger_o"]) / 2
    return [("Schienenecke (Auflage Oberkante Schienenverbinder 36)", (R.RS["ausladung"], 0.0, Z["platte_o"]), (0.0, 0.0, -1.0), "Auflage", "Verbinder 36"),
            ("Scheitel-Schelle (Stummel M8 durch den Kragarm)", (round(g["x_scheitel"], 2), 0.0, Z["traeger_o"]), (0.0, 0.0, 1.0), "Bohrung", "M8"),
            ("Ausleger +X (Stirnplatte Kragarm)", (g["x_plus"], 0.0, zc), (1.0, 0.0, 0.0), "Flansch", "2 x M10"),
            ("Ausleger -X (Stirnplatte Gegenarm)", (g["x_minus"], 0.0, zc), (-1.0, 0.0, 0.0), "Flansch", "2 x M10"),
            ("Fuss (Innenboden)", (0.0, 0.0, 0.0), (0.0, 0.0, -1.0), "Auflage + 4 Anker M10", "200x200")]

# =========================================================================== WA3 Montageschiene 41 (KS: Schiene entlang X ab 0, Schlitz unten z 0, Ruecken oben z 41)
SCH = dict(b=41.0, h=41.0, t=2.5, schlitz=22.0, laenge=round(SEITE - 2 * 20.5 * math.tan(HALB) - 2, 1))

def sch_profil():
    """C-Profil (Schlitz unten) als Polygon in (y, z)."""
    b, h, t, s = SCH["b"], SCH["h"], SCH["t"], SCH["schlitz"]
    yb, ys = b / 2, s / 2
    return [[-yb, 0], [-yb, h], [yb, h], [yb, 0], [ys, 0], [ys, t], [yb - t, t], [yb - t, h - t], [-yb + t, h - t], [-yb + t, t], [-ys, t], [-ys, 0]]

def sch_querschnitt():
    """Flaeche, Schwerpunkt und Iy (Biegung um die waagerechte Achse) aus Rechtecken des C-Profils [E]."""
    b, h, t, s = SCH["b"], SCH["h"], SCH["t"], SCH["schlitz"]
    lip = (b - s) / 2 - t
    rects = [(b, t, h - t / 2), (t, h - 2 * t, h / 2), (t, h - 2 * t, h / 2), (lip + t, t, t / 2), (lip + t, t, t / 2)]   # (breite, hoehe, z-mitte)
    A = sum(w * hh for w, hh, _ in rects); zs = sum(w * hh * z for w, hh, z in rects) / A
    I = sum(w * hh ** 3 / 12 + w * hh * (z - zs) ** 2 for w, hh, z in rects)
    return dict(A=A, zs=zs, I=I, W=I / max(zs, h - zs), kg_m=A * 7.85e-3)

def schiene(lg=None):
    lg = lg or SCH["laenge"]
    b = sc.Build(); nm = f"WA3_Montageschiene_41_{lg:.0f}"
    params(b, dict(SCH, laenge=lg)); mats(b, ["AB schiene"])
    b.add("component.create", name=nm, grounded=True)
    b.add("sketch.create", plane={"origin": [0, 0, 0], "x_dir": [0, 1, 0], "y_dir": [0, 0, 1]}, name="S_Schiene")
    b.add("sketch.line", points=sch_profil(), closed=True)
    b.add("sketch.finish")
    b.add("solid.extrude", distance=lg, operation="new", name="E_Schiene", body_name="Schiene")
    b.add("material.assign", bodies=["Schiene"], material="AB schiene")
    meta(b, nm, f"WA3-S41-{lg:.0f}", f"Montageschiene 41 x 41 x 2,5, Schlitz {SCH['schlitz']:g} unten, Laenge {lg:.0f} (Ringseite {SEITE:.0f} minus Gehrungsluft an beiden Ecken)", "Stahl S250GD sendzimirverzinkt")
    return b, nm, dict(lg=lg)

# =========================================================================== WA3 Rohrschelle d75 an der Schiene (KS: Rohrachse X durch Ursprung, Schienen-Unterkante bei z = schiene_u - achse)
KL = dict(rohr_d=75.0, einlage_t=3.0, ring_t=3.0, ring_b=30.0, nabe_b=20.0, nabe_h=12.0, stummel_d=8.0, mutter_b=20.0, mutter_l=30.0, mutter_h=6.0)

KL_ART = {"schiene": Z["schiene_u"] + SCH["t"], "ecke": Z["platte_o"], "stelze": Z["traeger_o"]}   # Auflage der Mutter (rel): Schienenlippe / Verbinder-Lasche / Kragarm der Stelze

def kl_geom(art="schiene"):
    p = KL; rr_i = p["rohr_d"] / 2 + p["einlage_t"]; rr_o = rr_i + p["ring_t"]
    z_nabe = rr_o - 1.5 + p["nabe_h"]; z_su = Z["schiene_u"] - Z["achse"]; z0 = KL_ART[art] - Z["achse"]
    return dict(rr_i=rr_i, rr_o=rr_o, z_nabe=z_nabe, z_su=z_su, z_mutter0=z0, z_mutter1=z0 + p["mutter_h"], unten=-rr_o, art=art)

def klemme(art="schiene"):
    p, g = KL, kl_geom(art)
    b = sc.Build(); nm = "LT_Klemme_d75_" + art.capitalize()
    params(b, p); mats(b, ["AB stahl", "AB epdm"])
    b.add("component.create", name=nm, grounded=True)
    rb = p["ring_b"]
    cyl(b, "Ring_R", 2 * g["rr_o"], rb, [-rb / 2, 0, 0], [1, 0, 0], body="Rohrschelle")
    bx(b, "Nabe_R", -rb / 2, rb / 2, -p["nabe_b"] / 2, p["nabe_b"] / 2, g["rr_o"] - 1.5, g["z_nabe"], op="join", targets=["Rohrschelle"])
    cyl(b, "Ring_Innen", 2 * g["rr_i"], rb + 2, [-rb / 2 - 1, 0, 0], [1, 0, 0], op="cut", targets=["Rohrschelle"])
    cyl(b, "Einlage_R", 2 * g["rr_i"], rb, [-rb / 2, 0, 0], [1, 0, 0], body="Schelleneinlage")
    cyl(b, "Einlage_Innen", p["rohr_d"], rb + 2, [-rb / 2 - 1, 0, 0], [1, 0, 0], op="cut", targets=["Schelleneinlage"])
    cyl(b, "Stummel_R", p["stummel_d"], g["z_mutter1"] - g["z_nabe"], [0, 0, g["z_nabe"]], [0, 0, 1], body="Gewindestummel")
    ml = p["mutter_l"] if art == "schiene" else 13.0; mb = p["mutter_b"] if art == "schiene" else 13.0      # Schienenmutter im Schlitz bzw. Sechskantmutter M8 (SW 13) mit Scheibe auf Lasche / Kragarm
    bx(b, "Schienenmutter_R", -ml / 2, ml / 2, -mb / 2, mb / 2, g["z_mutter0"], g["z_mutter1"], body="Schienenmutter")
    cyl(b, "Schienenmutter_Loch", p["stummel_d"], p["mutter_h"] + 2, [0, 0, g["z_mutter0"] - 1], [0, 0, 1], op="cut", targets=["Schienenmutter"])
    b.add("material.assign", bodies=["Rohrschelle", "Gewindestummel", "Schienenmutter"], material="AB stahl")
    b.add("material.assign", bodies=["Schelleneinlage"], material="AB epdm")
    wo = {"schiene": "in Schienenmutter (Montageschiene 41, Schlitz unten)", "ecke": "durch die Lasche des Schienenverbinders (Bogenscheitel), Mutter oben", "stelze": "durch Lasche und Kragarm der Stelze (Bogenscheitel), Mutter auf dem Kragarm"}[art]
    meta(b, nm, "LT-KL-75-" + art[0].upper(), f"Rohrschelle d75 mit EPDM-Einlage und Gewindestummel M8 {wo}; Rohr haengt darunter, Unterkante {Z['achse'] - g['rr_o']:.1f} rel", "Stahl verzinkt, EPDM")
    return b, nm, g

def kl_ports(art="schiene"):
    g = kl_geom(art)
    return [("Rohrachse (Ring d75)", (0.0, 0.0, 0.0), (1.0, 0.0, 0.0), "Aufnahme", "DN65"),
            ("Befestigung (Auflage der Mutter)", (0.0, 0.0, round(g["z_mutter0"], 2)), (0.0, 0.0, 1.0), "Mutter M8", "M8")]

# =========================================================================== WA3 Schienenverbinder 36 Grad (KS: Ecke im Ursprung, Schenkel entlang -X und entlang +36 Grad, Platte auf dem Schienenruecken z 0..4)
SV = dict(schenkel=160.0, b=41.0, t=4.0, loch_d=9.0)

def sv_poly():
    w = SV["b"] / 2; ls = SV["schenkel"]; a = math.radians(36.0)
    # Mittellinien: Schenkel 1 von (-ls, 0) nach (0, 0); Schenkel 2 von (0, 0) nach ls*(cos a, sin a). Aussenkontur des Gehrungsstosses.
    m = math.tan(math.radians(18.0)) * w
    u = (math.cos(a), math.sin(a)); n2 = (-u[1], u[0])
    pts = [[-ls, -w], [m, -w], [ls * u[0] + w * u[1], ls * u[1] - w * u[0]], [ls * u[0] - w * u[1], ls * u[1] + w * u[0]], [-m, w], [-ls, w]]
    return pts

def sv_lasche():
    """Lasche entlang der Winkelhalbierenden nach innen (108 Grad) bis ueber den Bogenscheitel des Rings (Stich der Ring-Ecke)."""
    st = ec_geom()["stich"]; u = (math.cos(math.radians(108.0)), math.sin(math.radians(108.0))); n = (-u[1], u[0]); w = 20.0; l1 = st + 25.0
    poly = [[n[0] * w, n[1] * w], [n[0] * w + u[0] * l1, n[1] * w + u[1] * l1], [-n[0] * w + u[0] * l1, -n[1] * w + u[1] * l1], [-n[0] * w, -n[1] * w]]
    return dict(poly=poly, scheitel=(u[0] * st, u[1] * st), stich=st, richtung=u)

def verbinder():
    b = sc.Build(); nm = "WA3_Schienenverbinder_36"
    params(b, SV); mats(b, ["AB stahl"])
    b.add("component.create", name=nm, grounded=True)
    b.add("sketch.create", plane={"origin": [0, 0, 0], "x_dir": [1, 0, 0], "y_dir": [0, 1, 0]}, name="S_Verbinder")
    b.add("sketch.line", points=[[round(x, 3), round(y, 3)] for x, y in sv_poly()], closed=True)
    b.add("sketch.finish")
    b.add("solid.extrude", distance=SV["t"], operation="new", name="E_Verbinder", body_name="Schienenverbinder")
    sl = sv_lasche()
    b.add("sketch.create", plane={"origin": [0, 0, 0], "x_dir": [1, 0, 0], "y_dir": [0, 1, 0]}, name="S_Lasche")
    b.add("sketch.line", points=[[round(x, 3), round(y, 3)] for x, y in sl["poly"]], closed=True)
    b.add("sketch.finish")
    b.add("solid.extrude", distance=SV["t"], operation="join", targets=["Schienenverbinder"], name="E_Lasche")
    cyl(b, "Loch_Scheitel", SV["loch_d"], SV["t"] + 2, [sl["scheitel"][0], sl["scheitel"][1], -1], [0, 0, 1], op="cut", targets=["Schienenverbinder"])
    a = math.radians(36.0)
    for k, s in enumerate((-110.0, -50.0), 1):
        cyl(b, f"Loch_1_{k}", SV["loch_d"], SV["t"] + 2, [s, 0, -1], [0, 0, 1], op="cut", targets=["Schienenverbinder"])
        cyl(b, f"Loch_2_{k}", SV["loch_d"], SV["t"] + 2, [-s * math.cos(a), -s * math.sin(a), -1], [0, 0, 1], op="cut", targets=["Schienenverbinder"])
    b.add("material.assign", bodies=["Schienenverbinder"], material="AB stahl")
    meta(b, nm, "WA3-SV36", "Schienenverbinder 36 Grad: Flachstahl 4 mm auf dem Ruecken beider Montageschienen an einer Ringecke, je Schenkel 2 Loecher fuer M8 in Schienenmutter, "
         "Lasche nach innen mit Loch ueber dem Bogenscheitel des Rings (Scheitel-Schelle)", "Stahl verzinkt")
    return b, nm, {}

# =========================================================================== WA4 Ring-Ecke d75, 36 Grad (KS: Port A im Ursprung, Lauf entlang +Z, Bogen in der XZ-Ebene)
EC = dict(d=75.0, sdr=17.0, r_faktor=25.0, schenkel=150.0)   # 25 x d: PE100+ Association (SDR17 25 x DN); Firat / Ostendorf nennen 20 x d -> der strengere Wert gilt

def ec_geom():
    p = EC; R_ = p["r_faktor"] * p["d"]; t = math.radians(36.0); e = p["d"] / p["sdr"]
    ex, ez = R_ - R_ * math.cos(t), p["schenkel"] + R_ * math.sin(t)
    end = (ex + math.sin(t) * p["schenkel"], 0.0, ez + math.cos(t) * p["schenkel"])
    tang = R_ * math.tan(t / 2)
    return dict(R=R_, wand=round(e, 2), di=p["d"] - 2 * round(e, 2), end=end, dir=(math.sin(t), 0.0, math.cos(t)), tangente=tang, bogen_l=R_ * t,
                stich=R_ * (1 / math.cos(t / 2) - 1), achs_l=2 * p["schenkel"] + R_ * t, ecke_bis_port=p["schenkel"] + tang)

def ecke():
    p, g = EC, ec_geom()
    b = sc.Build(); nm = "WA4_Ring_Ecke_d75_36"
    params(b, dict(p, radius=g["R"])); mats(b, ["AB pe100"])
    b.add("component.create", name=nm, grounded=True)
    L.bend(b, "Ring_Ecke", p["d"], g["di"], p["schenkel"], g["R"], 36, "AB pe100")
    meta(b, nm, "WA4-36", f"Ring-Ecke d75 36 Grad: Rohr PE-100 d75 SDR {p['sdr']:g} kalt gebogen, Radius {g['R']:.0f} ({p['r_faktor']:g} x d), Schenkel {p['schenkel']:g}; "
         "Anschluss an PVC-U nur ueber Klemmverbinder/Uebergang (siehe Blatt)", "PE-100 Trinkwasser")
    return b, nm, g

def ec_ports():
    g = ec_geom()
    return [("A", (0.0, 0.0, 0.0), (0.0, 0.0, -1.0), "Rohrende", "d75"), ("B", tuple(round(v, 3) for v in g["end"]), tuple(round(v, 5) for v in g["dir"]), "Rohrende", "d75")]

# =========================================================================== WA7 Pegelschacht-Podest (KS: Mitte Standflaeche am Boden; Fass steht mit seinem KS-Ursprung auf (0, 0, h))
K10 = dict(achse=1570.0, d=50, laenge_max=1200.0, gefaelle=0.01)       # Biofilter-Ueberlauf [Q docs/parts/tank.md], Laenge K10 bis Schacht hoechstens [A]
def podest_h():
    """Hoechste Fassboden-Lage, bei der K10 mit >= 1 % ueber laenge_max in die Zulauf-Muffe des Pegelschachts faellt:
    Achse K10 - Gefaelle - Bogen 90 d50 (Port zu Port senkrecht R + Muffentiefe) - Rohrstueck (2 Muffentiefen + 10) - Zulauf-Port ueber Fassboden."""
    bog = L.ports("lt_bogen90_d50")[1][1][2]
    stueck = 2 * L.DEPTH[50] + 10
    zport = R.ps_ports()[0][1][2]
    h = K10["achse"] - K10["gefaelle"] * K10["laenge_max"] - bog - stueck - zport
    return dict(h_max=h, bogen=bog, stueck=stueck, zport=zport)

PO = dict(b=480.0, profil=40.0, wand=3.0, platte_t=6.0, fuss_b=100.0, fuss_t=6.0, riegel_z=400.0, ring_h=60.0, ring_t=3.0, ring_luft=5.0, anker_d=8.0)

def po_geom():
    h = math.floor(podest_h()["h_max"] / 10) * 10
    return dict(h=h, top=h, x=PO["b"] / 2 - PO["profil"] / 2)

def podest():
    p, g = PO, po_geom()
    b = sc.Build(); nm = "WA7_Pegelschacht_Podest"
    params(b, dict(p, hoehe=g["h"])); mats(b, ["AB stahl"])
    b.add("component.create", name=nm, grounded=True)
    bodies = []; x = g["x"]; h = g["h"]
    zt0 = h - p["platte_t"] - p["profil"]
    for i, (sx, sy) in enumerate(((-1, -1), (1, -1), (1, 1), (-1, 1)), 1):
        bx(b, f"Fuss_{i}", sx * x - p["fuss_b"] / 2, sx * x + p["fuss_b"] / 2, sy * x - p["fuss_b"] / 2, sy * x + p["fuss_b"] / 2, 0, p["fuss_t"]); bodies.append(f"Fuss_{i}")
        cyl(b, f"Fuss_{i}_Loch", p["anker_d"] + 1, p["fuss_t"] + 2, [sx * x + sx * 32, sy * x + sy * 32, -1], [0, 0, 1], op="cut", targets=[f"Fuss_{i}"])
        rohr4(b, f"Bein_{i}", 2, p["fuss_t"], zt0, sx * x, sy * x); bodies.append(f"Bein_{i}")
    for nmr, z0 in (("Rahmen_oben", zt0), ("Rahmen_mitte", p["riegel_z"])):
        for k, sy in enumerate((-1, 1), 1):
            rohr4(b, f"{nmr}_x{k}", 0, -x - p["profil"] / 2, x + p["profil"] / 2, sy * x, z0 + p["profil"] / 2) if nmr == "Rahmen_oben" else rohr4(b, f"{nmr}_x{k}", 0, -x + p["profil"] / 2, x - p["profil"] / 2, sy * x, z0 + p["profil"] / 2)
            rohr4(b, f"{nmr}_y{k}", 1, -x + p["profil"] / 2, x - p["profil"] / 2, sy * x, z0 + p["profil"] / 2)
            bodies += [f"{nmr}_x{k}", f"{nmr}_y{k}"]
    bx(b, "Deckplatte", -p["b"] / 2, p["b"] / 2, -p["b"] / 2, p["b"] / 2, h - p["platte_t"], h); bodies.append("Deckplatte")
    ri = R.PS["fass_d"] / 2 + p["ring_luft"]
    cyl(b, "Haltering_R", 2 * (ri + p["ring_t"]), p["ring_h"], [0, 0, h], [0, 0, 1], body="Haltering")
    cyl(b, "Haltering_Innen", 2 * ri, p["ring_h"] + 2, [0, 0, h - 1], [0, 0, 1], op="cut", targets=["Haltering"])
    # Aussparungen fuer die Saugstutzen (radial +-30 Grad, Achse 100 ueber Fassboden) und den Notueberlauf (-X, Achse 440): Ring nur 60 hoch -> unter Achse 100 - 37 = 63
    bodies.append("Haltering")
    b.add("material.assign", bodies=bodies, material="AB stahl")
    meta(b, nm, "WA7", f"Pegelschacht-Podest: Stahlgestell 40x40x3, {p['b']:g} x {p['b']:g}, Deckplatte 6 mm auf Z {h:g} (Fassboden), Haltering 60 hoch gegen Verrutschen, 4 Fussplatten 100x100x6 mit Anker M8", "Stahl S235 feuerverzinkt")
    return b, nm, g

def po_ports():
    g = po_geom()
    return [("Fass (Ursprung Pegelschacht T94)", (0.0, 0.0, g["h"]), (0.0, 0.0, 1.0), "Auflage", "Fass d400"),
            ("Fuss (Innenboden)", (0.0, 0.0, 0.0), (0.0, 0.0, -1.0), "4 Fussplatten, je 1 Anker M8", "480x480")]

# =========================================================================== Lage im Modell (Vorschlag fuer Montage R1/R2; Instanzmatrix des Tisches = Joch-KS)
def lagen():
    """Stuetzpunkt je Ringecke aus scripts/dome-script.json: Joch am naechsten Bock eines Mitteltischs, sonst Stelze. Rueckgabe Liste dict."""
    cmds = json.load(open(os.path.join(sc.ROOT, "scripts", "dome-script.json"), encoding="utf-8"))["commands"]
    tische = {}; aussen = set(); innen = set()
    for c in cmds:
        if c["command"] != "occurrence.move":
            continue
        n = c["params"]["occurrence"]; m = c["params"]["matrix"]
        az = round(math.degrees(math.atan2(m[7], m[3])), 1)
        if n.startswith("Tisch_mitte"): tische[n] = dict(az=az, matrix=m)
        if n.startswith("Tisch_aussen"): aussen.add(round(az - 18.0, 1))
        if n.startswith("Tisch_innen"): innen.add(round(az - 18.0, 1))
    norm = lambda a: round((a + 180) % 360 - 180, 1)
    ecken = sorted({norm(t["az"] + s) for t in tische.values() for s in (-18, 18)} | {norm(a) for a in innen})
    out = []
    for e in ecken:
        cand = []
        for n, t in tische.items():
            if abs(norm(t["az"] - 18 - e)) < 0.5: cand.append((jo_geom("a")["abstand_ecke"], n, "a", t))
            if abs(norm(t["az"] + 18 - e)) < 0.5: cand.append((jo_geom("b")["abstand_ecke"], n, "b", t))
        need = {"innen": norm(e) in {norm(a) for a in innen}, "aussen": norm(e) in {norm(a) for a in aussen}}
        if cand:
            d, n, s, t = min(cand, key=lambda c: c[0])
            out.append(dict(ecke_az=e, art="joch", teil=f"portal_joch_mitte_{s}", tisch=n, bock=s, abstand_ecke=round(d, 1), matrix_tisch=t["matrix"], ausleger=need,
                            ausleger_laenge={"innen": AUSL["joch_innen"], "aussen": AUSL["joch_aussen"]}))
        else:
            innen_pf = not need["aussen"]
            r_sch = R_ECKE - ec_geom()["stich"]
            r_pf = r_sch - R.RS["ausladung"] - ec_geom()["stich"] if innen_pf else r_sch + R.RS["ausladung"] + ec_geom()["stich"]
            al = {"innen": AUSL["stelze_innen_pfosten_innen"] if innen_pf else AUSL["stelze_innen_pfosten_aussen"]}
            if need["aussen"]: al["aussen"] = AUSL["stelze_aussen_pfosten_aussen"]
            out.append(dict(ecke_az=e, art="stelze", teil="ringstuetze_d75_b", ausleger=need, pfosten="innen" if innen_pf else "aussen", r_pfosten=round(r_pf, 1), ausleger_laenge=al,
                            vorschlag=f"Pfosten auf der Winkelhalbierenden der Ecke bei r {r_pf:.0f}, Kragarm +X zeigt {'nach aussen' if innen_pf else 'zur Kuppelmitte'} zum Bogenscheitel; "
                                      f"Innen-Ausleger am {'Gegenarm -X' if innen_pf else 'Kragarm +X'}{', Aussen-Ausleger am Gegenarm -X' if need['aussen'] else ''}"))
    return out

def ausleger_laengen():
    """Laenge Flansch bis Endbuegel je Lage, so dass die Biegung bei AUSL_ZIEL ab Ring beginnt."""
    yj = jo_geom("a")["y_flansch"]; st = stelze()[2]
    return {"joch_innen": AUSL_ZIEL["innen"] - yj, "joch_aussen": AUSL_ZIEL["aussen"] - yj,
            "stelze_innen": AUSL_ZIEL["innen"] - (st["x_plus"] - st["x_scheitel"]), "stelze_aussen": AUSL_ZIEL["aussen"] - (st["x_scheitel"] - st["x_minus"])}

# Gewaehlte Laengen (3 Varianten): Stelze mit nur Innen-Ausleger steht mit dem Pfosten INNEN (Gegenarm -X zeigt zur Mitte), damit Ring und Ausleger sich am Pfosten
# ausgleichen (Kopfverschiebung, check_stelze); Stelze mit Innen- und Aussen-Ausleger (-17,7) steht mit dem Pfosten AUSSEN. Saettel liegen ausserhalb der Gaenge (check_ausleger).
AUSL = {"joch_innen": round(ausleger_laengen()["joch_innen"] / 10) * 10, "joch_aussen": round(ausleger_laengen()["joch_aussen"] / 10) * 10}
AUSL.update({"stelze_innen_pfosten_innen": AUSL["joch_innen"], "stelze_innen_pfosten_aussen": 1370, "stelze_aussen_pfosten_aussen": 1370})
# N-AUTOBAHN-FIX FIX-a / W-FIX-1 (docs/jobs/N-AUTOBAHN-FIX.md 2.2): Aussen-Ausleger kurz, Fallachse (Laenge + biege_r ab Flansch) bei r 4732 = Port Tisch aussen,
# also gleich hinter Gang B (bis r 4492) statt bei r 5400 unter der Kuppelhaut. Flansch r 3997 (Joch) bzw. 3869 (Stelze -17,7) [E, trassen_ring.fallleitungen()].
R_FALL_AUSSEN = 4732.0
AUSL["joch_aussen"] = 540   # (4732 - 3997 - 210) = 525 lag mit dem Sattelbeginn r 4472 noch 20 mm ueber Gang B (check_ausleger, Flansch r 3952); 540: Sattel ab r 4492, Fall r 4747
AUSL["stelze_aussen_pfosten_aussen"] = round((R_FALL_AUSSEN - 3869.0 - AU["biege_r"]) / 10) * 10   # 650
# W88 (Ben 05.11. abends, wunschbuch-ben.md): Innen-Schlaeuche fielen bei r 1567..1810 ueber dem Pool-Wasser und schlugen unten eine freie Schlaufe in der Luft.
# Neu faellt der Schlauch am Innentisch-Pfosten neben Gang A (Pfosten ap 2160, Rinnen bis r 2060, Gang A ab r 2195): Fallachse r 2120, Regelhahn vom Gang greifbar,
# danach mit Haltern unter dem Kragarm zum Port (r 1630). Flansch r aus check_ausleger: Joch 2802, Stelze Pfosten innen 3040, Stelze Pfosten aussen 3386.
R_FALL_INNEN = 2120.0
AUSL["joch_innen"] = 540   # Flansch im Modell r 2875 (Joch-KS je Tisch; check_ausleger rechnet mit 2802): 470 ergab Fall r 2193 an der Gangkante, 540 -> r ~2123
AUSL["stelze_innen_pfosten_innen"] = round((3040.0 - AU["biege_r"] - R_FALL_INNEN) / 10) * 10                         # 710
AUSL["stelze_innen_pfosten_aussen"] = round((3386.0 - AU["biege_r"] - R_FALL_INNEN) / 10) * 10                        # 1060

# =========================================================================== Ausgabe
def jobs(want):
    j = []
    if "joch" in want: j += [("portal_joch_mitte_a", lambda: joch("a")), ("portal_joch_mitte_b", lambda: joch("b"))]
    if "ausleger" in want: j += [(f"ausleger_schlauch_{v:.0f}", (lambda v=v: ausleger(v))) for v in sorted(set(AUSL.values()))]
    if "stelze" in want: j.append(("ringstuetze_d75_b", stelze))
    if "schiene" in want: j.append((f"montageschiene_41_{SCH['laenge']:.0f}", schiene))
    if "klemme" in want: j += [("lt_klemme_d75", klemme), ("lt_klemme_d75_ecke", lambda: klemme("ecke")), ("lt_klemme_d75_stelze", lambda: klemme("stelze"))]
    if "verbinder" in want: j.append(("schienenverbinder_36", verbinder))
    if "ecke" in want: j.append(("ring_ecke_d75", ecke))
    if "podest" in want: j.append(("pegelschacht_podest", podest))
    return j

CAM = {"portal_joch_mitte_a": ([-502, 0, 1200], 2.2, 0.25, 4200), "portal_joch_mitte_b": ([592, 0, 1200], 0.95, 0.25, 4200), "ringstuetze_d75_b": ([150, 0, 1150], 2.4, 0.15, 3600),
       "lt_klemme_d75": ([0, 0, 20], 0.8, 0.3, 450), "lt_klemme_d75_ecke": ([0, 0, 40], 0.8, 0.3, 500), "lt_klemme_d75_stelze": ([0, 0, 60], 0.8, 0.3, 600), "schienenverbinder_36": ([0, 40, 0], 0.6, 0.9, 700), "ring_ecke_d75": ([220, 0, 690], 0.0, 0.1, 2000),
       "pegelschacht_podest": ([0, 0, 420], 0.7, 0.3, 2200)}

def render(fname):
    os.makedirs(RD, exist_ok=True); path = os.path.join(DC, fname + ".sc"); out = os.path.join(RD, fname + ".png")
    if fname.startswith("ausleger_schlauch"):
        lg = float(fname.rsplit("_", 1)[1]); sc.snapshot(path, out, [lg / 2 + 100, 0, -60], 2.3, 0.3, lg * 1.6 + 600, w=1100, h=700)
    elif fname.startswith("montageschiene"):
        sc.snapshot(path, out, [100, 0, 20], 2.4, 0.35, 420, w=900, h=700)
    else:
        t, y, pi, d = CAM[fname]; sc.snapshot(path, out, t, y, pi, d, w=1000, h=1000)
    return out

def json_data():
    P = lambda lst: [{"name": n, "lage": [round(v, 3) for v in p], "richtung": list(d), "art": a, "dn": dn} for n, p, d, a, dn in lst]
    q = sch_querschnitt(); ph = podest_h()
    return {"quelle": "scripts/workshop/autobahn_t.py", "auftrag": "docs/jobs/N-AUTOBAHN-V2.md Abschnitt 3, WA-T (WA1 bis WA4, WA7)", "hoehenkette_rel": Z, "ring": {"apothem": AP_MITTE, "eckradius": round(R_ECKE, 1), "seite": round(SEITE, 1), "umfang_m": round(10 * SEITE / 1000, 2),
                                          "hinweis": "Planer-Blatt rechnete mit ap 3277 (nft_tisch.json); im Modell steht der Mittelring seit D63 auf 3377 (ring_shift_mid +100)"},
            "ausleger_ziel_ab_ring": {k: round(v, 1) for k, v in AUSL_ZIEL.items()}, "ausleger_laengen": AUSL,
            "lagen": lagen(),
            "teile": {
                "portal_joch_mitte_a": {"teilenummer": "WA1-A", "ks": "= Tisch-KS nft_tisch_mitte (Instanzmatrix des Tisches uebernehmen)", "geometrie": {k: (list(v) if isinstance(v, tuple) else v) for k, v in jo_geom("a").items()}, "ports": P(jo_ports("a"))},
                "portal_joch_mitte_b": {"teilenummer": "WA1-B", "ks": "= Tisch-KS nft_tisch_mitte (Instanzmatrix des Tisches uebernehmen)", "geometrie": {k: (list(v) if isinstance(v, tuple) else v) for k, v in jo_geom("b").items()}, "ports": P(jo_ports("b"))},
                **{f"ausleger_schlauch_{v:.0f}": {"teilenummer": f"WA2-{v:.0f}", "laenge": v, "ks": "Flanschanlage x 0, Arm +X, Armmitte z 0 (= Z 2277 rel im Modell)", "ports": P(au_ports(v))} for v in sorted(set(AUSL.values()))},
                "ringstuetze_d75_b": {"teilenummer": "T95-B", "ks": "wie T95 (Pfosten im Ursprung, Kragarm +X, Ring entlang Y bei x 250)", "ports": P(st_ports())},
                f"montageschiene_41_{SCH['laenge']:.0f}": {"teilenummer": f"WA3-S41-{SCH['laenge']:.0f}", "parameter": SCH, "querschnitt": {k: round(v, 2) for k, v in q.items()},
                                                          "ks": "Schiene entlang X ab 0, Schlitz unten z 0 (= Z 2212 rel), Ruecken z 41", "anzahl_im_ring": 10},
                **{("lt_klemme_d75" if a == "schiene" else f"lt_klemme_d75_{a}"): {"teilenummer": "LT-KL-75-" + a[0].upper(), "ks": "Rohrachse X durch Ursprung (= Z 2145 rel)", "unterkante": round(kl_geom(a)["unten"], 2), "ports": P(kl_ports(a))} for a in KL_ART},
                "schienenverbinder_36": {"teilenummer": "WA3-SV36", "ks": "Ecke der Schienen-Mittellinien im Ursprung, Platte z 0..4 auf dem Schienenruecken (= Z 2253 rel)", "anzahl_im_ring": 10},
                "ring_ecke_d75": {"teilenummer": "WA4-36", "parameter": EC, "geometrie": {k: (list(v) if isinstance(v, tuple) else round(v, 2)) for k, v in ec_geom().items()}, "ports": P(ec_ports())},
                "pegelschacht_podest": {"teilenummer": "WA7", "parameter": PO, "hoehe": po_geom()["h"], "k10_rechnung": {k: round(v, 1) for k, v in ph.items()}, "ports": P(po_ports())}}}

def write_json():
    """Nur der eigene Schluessel 'tragwerk' in data/components/autobahn_teile.json (WA-S schreibt 'schlauch'): lesen, ersetzen, schreiben."""
    p = os.path.join(sc.ROOT, "data", "components", "autobahn_teile.json")
    d = json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}
    d["tragwerk"] = json_data()
    open(p, "w", encoding="utf-8").write(json.dumps(d, indent=1, ensure_ascii=False) + "\n")
    return p

if __name__ == "__main__":
    want = [a for a in sys.argv[1:] if not a.startswith("--")] or ["joch", "ausleger", "stelze", "schiene", "klemme", "verbinder", "ecke", "podest"]
    for fname, fn in jobs(want):
        res = fn(); out = L.save(res[0], res[1], fname); print(fname, "->", out)
        if "--render" in sys.argv:
            print("Bild", render(fname))
    if "--json" in sys.argv:
        print("geschrieben", write_json())
