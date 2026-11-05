"""Scherenknoten (W74, R56, Blatt docs/jobs/N-VERBINDER.md): EIN Bauteil, die Montage setzt nur Instanzen.

Teile (je eine Datei, alle im selben Rahmen):
  designs/components/knoten_schere_platte.sc   Plattenpaar (W83): obere und untere Lochplatte D 110 x 8, 6 Loecher auf r 37, Mittelbohrung;
                                               die Laschenaugen liegen dazwischen (1 Paar je Knoten)
  designs/components/knoten_schere_arm_a.sc    Schere (2 Laschen, Drehpunkt M8, Plattenschraube M10) + Rohrende 250 mm, Knick A
  designs/components/knoten_schere_arm_b.sc    wie A, Knick B (A und B unterscheiden sich NUR im Knickwinkel)
  designs/components/knoten_schere.sc          Detailmodell fuer den Viewer: Platte + ein Arm B (flach gebaut, eindeutige Koerpernamen)

Rahmen: Ursprung = Knotenpunkt, Z = Kuppelnormale n (aussen), Lochplatte in der Tangentialebene unter dem Knotenpunkt.
Arm: Plattenschraube auf +X (r 37), Strebe in Richtung +X, um die Neigung nach innen (-Z) abgekantet; die Rohrachse geht durch
den Ursprung. Wie auf dem Foto liegt die Platte OBEN auf den Laschen (Schraubenkopf auf der Platte, Mutter unter Lasche 1).
Montage: Instanz an den Knotenpunkt, Z auf n, X auf die Lochrichtung des Arms (data/components/knoten_schere.json).

Parameter: data/components/knoten_schere.json (wert, einheit, herkunft); die Knotentabelle (26 Knoten, 130 Arme) schreibt
dieses Skript in dieselbe Datei.
Aufruf: python -X utf8 scripts/workshop/knoten_schere.py [--table] [--render]
  ohne Schalter: Tabelle + alle vier Dateien bauen;  --table: nur Knotentabelle;  --render: Bilder (Probe-Knoten n01 im Scratchpad)"""
import itertools, json, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sc

PJ = os.path.join(sc.ROOT, "data", "components", "knoten_schere.json")
P, DOC = sc.load_params("knoten_schere")
UNIT = {k: v["einheit"] for k, v in DOC["parameter"].items()}
DES = os.path.join(sc.ROOT, "designs", "components")
OUT = {"platte": os.path.join(DES, "knoten_schere_platte.sc"), "A": os.path.join(DES, "knoten_schere_arm_a.sc"),
       "B": os.path.join(DES, "knoten_schere_arm_b.sc"), "detail": os.path.join(DES, "knoten_schere.sc")}
MAT, MATB, MATR = "Stahl Laserteil", "Stahl Schraube", "Stahl verzinkt"
Y = [0.0, 1.0, 0.0]
add = lambda a, b, s=1.0: [a[i] + s * b[i] for i in range(3)]
dot = lambda a, b: sum(a[i] * b[i] for i in range(3))
cross = lambda a, b: [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]
unit = lambda a: [x / math.sqrt(dot(a, a)) for x in a]
r4 = lambda v: [round(x, 4) for x in v]
BOLT_LEN = (25, 30, 35, 40, 45, 50, 55, 60)


def tilt(typ):
    """Neigung der Strebe gegen die Plattenebene: asin(L / 2R) (R41, R56)."""
    return math.degrees(math.asin(P[f"strut_{typ.lower()}"] / (2 * P["dome_r"])))


class Geo:
    """Alle abgeleiteten Lagen eines Arms (Typ A oder B) im Bauteilrahmen."""
    def __init__(self, typ):
        self.typ = typ
        self.deg = tilt(typ)
        th = math.radians(self.deg)
        self.u = [math.cos(th), 0.0, -math.sin(th)]               # Strebenachse
        self.nrm = [math.sin(th), 0.0, math.cos(th)]              # Normale der gekippten Laschenebene
        t = P["link_t"]
        # EINE Platte fuer A und B -> eine Plattenhoehe: Mittelebene aus B (bend_r), Knicklinie je Typ so, dass die Achse durch den Ursprung geht
        self.z_mid = -P["bend_r"] * math.tan(math.radians(tilt("B")))
        self.bend = -self.z_mid / math.tan(th)                    # Lage der Knicklinie (B = bend_r, A weiter aussen)
        self.z_plate_bot = self.z_mid + t                         # obere Platte liegt auf Lasche 2
        self.z_plate2_top = self.z_mid - t                        # untere Platte (W83) liegt unter Lasche 1
        self.z_plate2_bot = self.z_plate2_top - P["plate_t"]
        self.B0 = [self.bend, 0.0, self.z_mid]
        self.s_pivot = P["bolt_circle_r"] + P["a_plate_to_pivot"] - self.bend   # gleicher Laschenzuschnitt fuer A und B
        self.s_nose = self.s_pivot + P["b_pivot_to_nose"]
        self.s_tip = self.s_nose + P["nose_w"] / 2 + P["tip_past_nose"]
        self.s_tube = self.s_pivot + P["pivot_out"]
        self.nose_y = P["tube_d"] / 2 + P["nose_out"]
        self.ext = t * math.tan(th / 2) + 0.2                     # Zugabe der aeusseren Lasche am Knick (schliesst den Keil)
        self.tube0 = add(self.B0, self.u, self.s_tube)            # Rohrmund (Mitte)
        self.node_to_tube = math.hypot(self.B0[0], self.B0[2]) + self.s_tube

    def pt(self, s, n=0.0, y=0.0):
        return add(add(add(self.B0, self.u, s), self.nrm, n), Y, y)


def bolt_len(grip):
    return next(L for L in BOLT_LEN if L >= grip)


def materials(b):
    for nm, col in ((MAT, "#8a8378"), (MATB, "#c9ced3"), (MATR, "#b9c0c8")):
        b.add("material.create", name=nm, density_g_cm3=7.85, color=col, pbr={"metallic": 0.8, "roughness": 0.5, "dielectric_ior": 1.5})


def build_plate(b, z_bot, pre="", nm="Lochplatte"):
    nm = pre + nm
    pt = P["plate_t"]
    b.add("solid.cylinder", diameter=P["plate_d"], height=pt, base=[0, 0, round(z_bot, 4)], axis=[0, 0, 1], operation="new", name=pre + "Platte_F", body_name=nm)
    b.add("solid.cylinder", diameter=P["center_hole"], height=pt + 2, base=[0, 0, round(z_bot - 1, 4)], axis=[0, 0, 1], operation="cut", targets=[nm], name=pre + "Mittelbohrung")
    for k in range(int(P["holes"])):
        a = math.radians(360 / P["holes"] * k)
        b.add("solid.cylinder", diameter=P["plate_hole"], height=pt + 2, base=r4([P["bolt_circle_r"] * math.cos(a), P["bolt_circle_r"] * math.sin(a), z_bot - 1]),
              axis=[0, 0, 1], operation="cut", targets=[nm], name=f"{pre}Loch_{k + 1}")
    b.add("material.assign", bodies=[nm], material=MAT)
    return [nm]


def build_arm(b, g, pre=""):
    """Zwei Laschen, Rohrende mit zwei Gegenloechern; gibt (Koerper, Normteile) zurueck. Normteile werden danach umbenannt."""
    t, w2 = P["link_t"], P["link_w"] / 2
    bodies = []
    for k, side in ((1, -1), (2, 1)):                          # Lasche 1 unten (Nase -Y), Lasche 2 oben an der Platte (Nase +Y)
        body = f"{pre}Lasche_{k}"
        bodies.append(body)
        zb = g.z_mid - t if k == 1 else g.z_mid
        ext = 0.0 if k == 1 else g.ext                         # Knick nach unten: Lasche 1 innen (Wulst), Lasche 2 aussen (Zugabe)
        eye = [[round(P["bolt_circle_r"] + w2 * math.cos(a), 4), round(w2 * math.sin(a), 4)]
               for a in (math.pi / 2 + math.pi * j / 12 for j in range(13))]
        flat = eye + [[round(g.bend + ext, 4), -w2], [round(g.bend + ext, 4), w2]]
        b.add("sketch.create", plane={"origin": [0, 0, round(zb, 4)], "x_dir": [1, 0, 0], "y_dir": [0, 1, 0]}, name=f"S_{body}_flach")
        b.add("sketch.line", points=flat, closed=True)
        b.add("sketch.finish")
        b.add("solid.extrude", distance=t, name=f"F_{body}_flach", body_name=body)
        if k == 1:                                             # Biegewulst unter beiden Oberflaechen: verbindet flach und schraeg mit Volumen
            nb = unit([g.nrm[i] + (0, 0, 1)[i] for i in range(3)])
            cc = add(g.B0, nb, -t / 2)
            b.add("solid.cylinder", diameter=round(0.92 * t, 3), height=P["link_w"], base=r4(add(cc, Y, -w2)), axis=Y, operation="join", targets=[body], name=f"{pre}Knick_{k}")
        n0, n1, ny = g.s_nose - P["nose_w"] / 2, g.s_nose + P["nose_w"] / 2, g.nose_y
        s0 = -ext
        if side < 0:
            poly = [[s0, -w2], [n0, -w2], [n0, -ny], [n1, -ny], [n1, -w2], [g.s_tip, -w2], [g.s_tip, w2], [s0, w2]]
        else:
            poly = [[s0, -w2], [g.s_tip, -w2], [g.s_tip, w2], [n1, w2], [n1, ny], [n0, ny], [n0, w2], [s0, w2]]
        b.add("sketch.create", plane={"origin": r4(add(g.B0, g.nrm, -t if k == 1 else 0.0)), "x_dir": r4(g.u), "y_dir": Y}, name=f"S_{body}_schraeg")
        b.add("sketch.line", points=[[round(x, 4), round(y, 4)] for x, y in poly], closed=True)
        b.add("sketch.finish")
        b.add("solid.extrude", distance=t, operation="join", targets=[body], name=f"F_{body}_schraeg")
        b.add("solid.cylinder", diameter=P["plate_hole"], height=40, base=[P["bolt_circle_r"], 0, round(g.z_mid - 20, 4)], axis=[0, 0, 1], operation="cut", targets=[body], name=f"{pre}Auge_{k}")
        b.add("solid.cylinder", diameter=P["pivot_hole"], height=40, base=r4(g.pt(g.s_pivot, -20)), axis=r4(g.nrm), operation="cut", targets=[body], name=f"{pre}Drehloch_{k}")
        b.add("material.assign", bodies=[body], material=MAT)
    tube = f"{pre}Rohrstueck"
    bodies.append(tube)
    b.add("solid.cylinder", diameter=P["tube_d"], height=P["tube_len"], base=r4(g.tube0), axis=r4(g.u), operation="new", name=pre + "Rohr_F", body_name=tube)
    b.add("solid.cylinder", diameter=round(P["tube_d"] - 2 * P["tube_t"], 4), height=P["tube_len"] + 2, base=r4(add(g.tube0, g.u, -1)), axis=r4(g.u), operation="cut", targets=[tube], name=pre + "Rohr_innen")
    for k, side in ((1, -1), (2, 1)):                          # Gegenloch je Lasche, auf deren Mittelebene
        c = g.pt(g.s_nose, -t / 2 if k == 1 else t / 2)
        b.add("solid.cylinder", diameter=P["wall_hole"], height=P["tube_t"] + 4, base=r4(add(c, Y, side * (P["tube_d"] / 2 - P["tube_t"] - 2))),
              axis=[0, side, 0], operation="cut", targets=[tube], name=f"{pre}Gegenloch_{k}")
    b.add("material.assign", bodies=[tube], material=MATR)
    # Normteile: Plattenschraube M10 (Kopf auf der Platte), Drehpunkt M8
    wt10, wt8, nut10, nut8 = 2.0, 1.6, 8.4, 6.8
    top = [P["bolt_circle_r"], 0, g.z_plate_bot + P["plate_t"]]
    bot = [P["bolt_circle_r"], 0, g.z_plate2_bot]                # unter der unteren Platte (W83)
    l10 = bolt_len(2 * P["plate_t"] + 2 * t + 2 * wt10 + nut10 + 2)
    pv = g.pt(g.s_pivot)
    ptop, pbot = add(pv, g.nrm, t), add(pv, g.nrm, -t)
    l8 = bolt_len(2 * t + 2 * wt8 + nut8 + 2)
    neg = [-x for x in g.nrm]
    ins = [("washer", "M10", None, top, [0, 0, 1], "Platte_ScheibeO"), ("hex_bolt", "M10", l10, add(top, [0, 0, 1], wt10), [0, 0, 1], "Platte_Schraube"),
           ("washer", "M10", None, bot, [0, 0, -1], "Platte_ScheibeU"), ("hex_nut", "M10", None, add(bot, [0, 0, -1], wt10), [0, 0, -1], "Platte_Mutter"),
           ("washer", "M8", None, ptop, g.nrm, "Dreh_ScheibeO"), ("hex_bolt", "M8", l8, add(ptop, g.nrm, wt8), g.nrm, "Dreh_Schraube"),
           ("washer", "M8", None, pbot, neg, "Dreh_ScheibeU"), ("hex_nut", "M8", None, add(pbot, neg, wt8), neg, "Dreh_Mutter")]
    parts = []
    for fam, size, ln, p, d, nm in ins:
        kw = dict(family=fam, size=size, point=r4(p), direction=r4(d), name=pre + nm)
        if ln:
            kw["length"] = ln
        b.add("parts.insert", **kw)
        parts.append(pre + nm)
    return bodies, parts, {"M10": l10, "M8": l8}


def rename_parts(b, names, first=1):
    for j, nm in enumerate(names, first):
        b.add("body.rename", body=f"Body{j}", name=nm)
    b.add("material.assign", bodies=names, material=MATB)


def meta(b, comp, pn, desc):
    b.add("component.metadata.set", component=comp, part_number=pn, description=desc, revision="A",
          properties={"Werkstoff": "S235 Laserteil verzinkt / Rohr EN 10255 verzinkt / Schrauben 8.8 verzinkt"})


def design(which, explode=None):
    """which: 'platte' | 'A' | 'B' | 'detail'; explode: {koerper: [dx,dy,dz]} verschiebt Koerper (nur fuer Bilder)."""
    b = sc.Build()
    materials(b)
    b.params_to_design({k: v for k, v in P.items() if UNIT.get(k) in ("mm", "")}, DOC, UNIT)
    gB = Geo("B")
    if which == "platte":
        root = "60S_Knoten_Schere_Platte"
        b.add("component.create", name=root)
        meta(b, root, "T60S-P", "Plattenpaar (W83): 2 Lochplatten D110 x 8, je 6 Loecher D11 auf Lochkreis r37, Mittelbohrung D20; Laschenaugen dazwischen; ein Paar je Knoten")
        bodies = build_plate(b, gB.z_plate_bot) + build_plate(b, gB.z_plate2_bot, nm="Lochplatte_unten")
        parts = []
    else:
        typ = "B" if which == "detail" else which
        g = Geo(typ)
        root = "60S_Knoten_Schere" if which == "detail" else f"60S_Knoten_Schere_Arm_{typ}"
        b.add("component.create", name=root)
        meta(b, root, "T60S" if which == "detail" else f"T60S-{typ}",
             f"Scherenarm {typ}: 2 Laschen {P['link_w']:g} x {P['link_t']:g} mit Knick {g.deg:.1f} Grad, Nasen ausgefahren, M10-Plattenschraube, M8-Drehpunkt, "
             f"Rohrende Rund {P['tube_d']:g} x {P['tube_t']:g} ({P['tube_len']:g} mm Probestueck) mit 2 Gegenloechern D{P['wall_hole']:g}")
        bodies, parts, _ = build_arm(b, g)
        if which == "detail":
            bodies += build_plate(b, g.z_plate_bot) + build_plate(b, g.z_plate2_bot, nm="Lochplatte_unten")
        rename_parts(b, parts)
    if explode:
        for nm, v in explode.items():
            if any(abs(x) > 1e-9 for x in v):
                b.add("solid.move", bodies=[nm], translate=r4(v))
    return b, bodies + parts


# ---------- Knotentabelle: Plattenlage, Lochzuordnung, Drehwinkel, Achsversatz ----------
def axis_offset(typ, delta_deg):
    """Abstand Knotenpunkt -> Rohrachse, wenn der Arm um seine Plattenschraube (auf +X, r 37) um delta gedreht wird."""
    g = Geo(typ)
    d = math.radians(delta_deg)
    rc = P["bolt_circle_r"]
    rot = lambda v: [rc + (v[0] - rc) * math.cos(d) - v[1] * math.sin(d), (v[0] - rc) * math.sin(d) + v[1] * math.cos(d), v[2]]
    p0, p1 = rot([0, 0, 0]), rot(g.u)
    dvec = [p1[i] - p0[i] for i in range(3)]
    c = cross(p0, dvec)
    return math.sqrt(dot(c, c)) / math.sqrt(dot(dvec, dvec))


def node_table():
    arme = json.load(open(os.path.join(sc.ROOT, "data", "components", "knoten_arme.json"), encoding="utf-8"))
    H = int(P["holes"])
    step = 360 / H
    out = []
    for nid in sorted(arme, key=int):
        k = arme[nid]
        n = unit(k["n"])
        ref = [0, 0, 1] if abs(n[2]) < 0.9 else [1, 0, 0]       # Bezug fuer die Azimut-Null: Kuppel-Z (bzw. X am Scheitel)
        e1 = unit(add(ref, n, -dot(ref, n)))
        e2 = cross(n, e1)
        az = []
        for a in k["arme"]:
            up = add(a["u"], n, -dot(a["u"], n))
            az.append(math.degrees(math.atan2(dot(up, e2), dot(up, e1))) % 360)
        order = sorted(range(len(az)), key=lambda i: az[i])
        best = None
        for holes in itertools.combinations(range(H), len(az)):     # welche Loecher belegt (in Umlaufreihenfolge)
            for shift in range(len(az)):
                res = [((az[order[(j + shift) % len(az)]] - step * holes[j] + 180) % 360) - 180 for j in range(len(az))]
                lo, hi = min(res), max(res)
                if hi - lo > 180:
                    continue
                phi = (lo + hi) / 2                                    # Plattendrehung: halbiert den groessten Fehler
                worst = (hi - lo) / 2
                if best is None or worst < best[0] - 1e-9:
                    best = (worst, phi, holes, shift)
        worst, phi, holes, shift = best
        x_dir = unit(add([math.cos(math.radians(phi)) * x for x in e1], [math.sin(math.radians(phi)) * x for x in e2]))
        arms = []
        for j in range(len(az)):
            i = order[(j + shift) % len(az)]
            hole_ang = (phi + step * holes[j]) % 360
            delta = ((az[i] - hole_ang + 180) % 360) - 180
            a = k["arme"][i]
            arms.append({"arm": i + 1, "nachbar": a["nachbar"], "typ": a["typ"], "loch": holes[j] + 1,
                         "drehwinkel_loch_grad": round(step * holes[j], 3), "azimut_grad": round((az[i] - phi) % 360, 3),
                         "drehung_um_plattenschraube_grad": round(delta, 3), "achsversatz_mm": round(axis_offset(a["typ"], delta), 2)})
        arms.sort(key=lambda r: r["arm"])
        out.append({"knoten": f"n{int(nid):02d}", "wertigkeit": k["valenz"], "ursprung": k["pos"], "normale": r4(n),
                    "x_richtung": r4(x_dir), "arme": arms, "groesste_drehung_grad": round(worst, 3),
                    "groesster_achsversatz_mm": round(max(r["achsversatz_mm"] for r in arms), 2)})
    return out


def write_table():
    t = node_table()
    DOC["knoten"] = t
    mx = max(t, key=lambda r: r["groesster_achsversatz_mm"])
    DOC["auswertung"] = {
        "knoten": len(t), "arme": sum(len(r["arme"]) for r in t),
        "typ_a": sum(1 for r in t for a in r["arme"] if a["typ"] == "A"), "typ_b": sum(1 for r in t for a in r["arme"] if a["typ"] == "B"),
        "groesster_achsversatz_mm": mx["groesster_achsversatz_mm"], "bei_knoten": mx["knoten"],
        "groesste_drehung_grad": max(r["groesste_drehung_grad"] for r in t),
        "je_wertigkeit": {str(v): {"knoten": sum(1 for r in t if r["wertigkeit"] == v),
                                   "groesste_drehung_grad": max(r["groesste_drehung_grad"] for r in t if r["wertigkeit"] == v),
                                   "groesster_achsversatz_mm": max(r["groesster_achsversatz_mm"] for r in t if r["wertigkeit"] == v)} for v in (4, 5, 6)},
        "soll_achsversatz_mm": 5.0,
        "befehl": "python -X utf8 scripts/workshop/knoten_schere.py --table"}
    DOC["geometrie"] = {typ: {"neigung_grad": round(Geo(typ).deg, 3), "knicklinie_r_mm": round(Geo(typ).bend, 2), "drehpunkt_hinter_knick_mm": round(Geo(typ).s_pivot, 2), "knotenpunkt_bis_rohrende_mm": round(Geo(typ).node_to_tube, 2),
                              "rohr_mm": round(P[f"strut_{typ.lower()}"] - 2 * Geo(typ).node_to_tube, 1)} for typ in "AB"}
    DOC["geometrie"]["platte_unterkante_z_mm"] = round(Geo("B").z_plate_bot, 3)
    DOC["geometrie"]["untere_platte_oberkante_z_mm"] = round(Geo("B").z_plate2_top, 3)
    json.dump(DOC, open(PJ, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps(DOC["auswertung"], ensure_ascii=False))
    print(json.dumps(DOC["geometrie"], ensure_ascii=False))


def write_parts():
    """data/parts/knoten_schere.json fuer die Viewer-Detailansicht (Detailmodell knoten_schere.sc: Platte + Arm B).
    Explosion = dieselben Verschiebungen wie das Explosionsbild (render_knoten_schere.explode_vectors)."""
    import render_knoten_schere as rk
    ex = rk.explode_vectors()
    g = Geo("B")
    t = P["link_t"]

    def explo(body):
        v = ex[body]
        ln = math.sqrt(dot(v, v))
        return {"richtung": [round(x / ln, 4) for x in v], "abstand_mm": round(ln, 1)}
    bolts = {"M10": bolt_len(2 * P["plate_t"] + 2 * t + 2 * 2.0 + 8.4 + 2), "M8": bolt_len(2 * t + 2 * 1.6 + 6.8 + 2)}
    ausn = "Vorentwurf zur Abnahme durch Ben (N-VERBINDER); Katalog- und Stuecklisten-Eintrag erst nach Freigabe durch die Montage"
    norm_bezug = "Normteil, in ganz Europa im Schraubenhandel (D76); Haendler nicht recherchiert"

    def nt(id_, name, body, norm, masse, funk, eig):
        return {"id": id_, "name": name, "koerper": [body], "menge": 1, "typ": "normteil", "werkstoff": "stahl_verzinkt", "masse_mm": masse,
                "funktion": funk, "eigenschaften": eig, "norm": norm, "norm_konfidenz": "angenommen", "lebensmittelkontakt": "nein",
                "lebensmittelkontakt_konfidenz": "angenommen", "konfidenz": "angenommen", "quelle": "R56 Abschnitt 2 (M10 und M8, 8.8 [A])",
                "bezug": norm_bezug, "ausnahme": ausn, "explosion": explo(body)}
    common = {"norm_konfidenz": "angenommen", "lebensmittelkontakt": "nein", "lebensmittelkontakt_konfidenz": "angenommen", "konfidenz": "angenommen", "ausnahme": ausn}
    teile = [dict(common, id="lochplatte", name="Lochplatte oben", koerper=["Lochplatte"], menge=1, typ="platte", werkstoff="stahl_verzinkt",
                  masse_mm=f"Scheibe D {P['plate_d']:g} x {P['plate_t']:g}, {int(P['holes'])} Loecher D {P['plate_hole']:g} auf Lochkreis r {P['bolt_circle_r']:g}, Mittelbohrung D {P['center_hole']:g}",
                  funktion="Die Platte verbindet alle Streben eines Knotens. Jede Schere wird mit einer Schraube auf ein Loch geschraubt; solange die Schraube locker ist, dreht sich die Strebe um sie.",
                  eigenschaften=["Eine Platte fuer alle 26 Knoten (4-, 5- und 6-wertig).", "Laserteil S235, feuerverzinkt.",
                                 f"Liegt wie auf dem Foto OBEN auf den Laschen; Unterkante {-g.z_plate_bot:.1f} mm unter dem Knotenpunkt."],
                  norm="EN 10025-2 S235 (Blech) [A]", quelle="Blatt N-VERBINDER, R56 Abschnitt 2 (Foto ohne Massstab)", explosion=explo("Lochplatte")),
             dict(common, id="lochplatte_unten", name="Lochplatte unten", koerper=["Lochplatte_unten"], menge=1, typ="platte", werkstoff="stahl_verzinkt",
                  masse_mm=f"wie die obere: Scheibe D {P['plate_d']:g} x {P['plate_t']:g}, {int(P['holes'])} Loecher D {P['plate_hole']:g} auf r {P['bolt_circle_r']:g}, Mittelbohrung D {P['center_hole']:g}",
                  funktion="Die untere Platte (W83, Ben) klemmt die Laschenaugen von unten. Mit der oberen Platte bildet sie ein Paar: jede Plattenschraube geht durch beide Platten und beide Augen, die Augen sind zweischnittig gefasst.",
                  eigenschaften=["Gleiches Laserteil wie die obere Platte (ein Zuschnitt, 52 Stueck fuer 26 Knoten).",
                                 f"Oberkante {-g.z_plate2_top:.1f} mm unter dem Knotenpunkt; der Laschenknick liegt ausserhalb beider Platten (r {Geo('B').bend:.0f} bzw. {Geo('A').bend:.0f} gegen Plattenrand r {P['plate_d'] / 2:g})."],
                  norm="EN 10025-2 S235 (Blech) [A]", quelle="Wunschbuch W83 (Ben 05.11.); Masse wie obere Platte [A]", explosion=explo("Lochplatte_unten"))]
    for k, side in ((2, "+"), (1, "-")):
        teile.append(dict(common, id=f"lasche_{k}", name=f"Lasche {k} ({'oben, an der Platte' if k == 2 else 'unten'})", koerper=[f"Lasche_{k}"], menge=1,
                          typ="sonderteil", werkstoff="stahl_verzinkt",
                          masse_mm=f"Flachstahl {P['link_w']:g} x {t:g}, Auge bis Drehpunkt {P['a_plate_to_pivot']:g}, Drehpunkt bis Nase {P['b_pivot_to_nose']:g}, Nase {P['nose_w']:g} breit, Knick {g.deg:.1f} Grad (Arm A {tilt('A'):.1f} Grad)",
                          funktion="Zwei gekreuzte Laschen bilden die Schere. Liegen beide Augen deckungsgleich auf der Platte und sind verschraubt, stehen die Nasen durch die Gegenloecher aus dem Rohr: die Strebe ist eingerastet.",
                          eigenschaften=[f"Nase zeigt nach {side}Y quer zur Rohrachse und steht {P['nose_out']:g} mm ueber die Rohraussenwand.",
                                         "Gleicher Zuschnitt fuer A und B; nur Lage und Winkel des Knicks unterscheiden sich.",
                                         "Der Knick ist der statische Engpass (R56: 4,6 kN bei 5 mm, 11,8 kN bei 8 mm)."],
                          norm="EN 10025-2 S235, Laserzuschnitt, abgekantet [A]", quelle="R56 Abschnitte 1, 2 und 4", explosion=explo(f"Lasche_{k}")))
    teile.append(dict(common, id="rohrende", name="Rohrende der Strebe (Probestueck)", koerper=["Rohrstueck"], menge=1, typ="rohr", werkstoff="stahl_verzinkt",
                      masse_mm=f"Rundrohr {P['tube_d']:g} x {P['tube_t']:g}, Probestueck {P['tube_len']:g} mm, 2 Gegenloecher D {P['wall_hole']:g} gegenueber, {g.s_nose - g.s_tube:.0f} mm hinter dem Rohrmund",
                      funktion="Das Rohr ist die Strebe. In seinen zwei Gegenloechern sitzen die Nasen der Schere; ueber die Lochraender laeuft die Strebenkraft in die Laschen.",
                      eigenschaften=["Rund 42,4 x 2,6 verzinkt ist die Empfehlung aus R56 (offen bei Ben).",
                                     f"Rohrlaenge in der Kuppel: A {P['strut_a'] - 2 * Geo('A').node_to_tube:.0f} mm, B {P['strut_b'] - 2 * g.node_to_tube:.0f} mm.",
                                     "Gegenloecher mit Bohrlehre (Prisma) bohren."],
                      norm="EN 10255 (Gewinderohr verzinkt) [A]", quelle="R56 Abschnitte 3 und 5", explosion=explo("Rohrstueck")))
    teile += [
        nt("plattenschraube", f"Plattenschraube M10 x {bolts['M10']}", "Platte_Schraube", "ISO 4017 M10, 8.8 verzinkt", f"M10 x {bolts['M10']}",
           "Schraubt beide Laschenaugen auf ein Loch der Platte; traegt die ganze Strebenkraft (einschnittig).", ["Angezogen kann sich die Schere nicht mehr oeffnen."]),
        nt("plattenscheibe_oben", "Scheibe M10 oben", "Platte_ScheibeO", "ISO 7089 10, verzinkt", "10,5 x 20 x 2", "Liegt unter dem Schraubenkopf auf der Platte.", ["Flache Scheibe."]),
        nt("plattenscheibe_unten", "Scheibe M10 unten", "Platte_ScheibeU", "ISO 7089 10, verzinkt", "10,5 x 20 x 2", "Liegt unter der unteren Platte vor der Mutter.", ["Flache Scheibe."]),
        nt("plattenmutter", "Mutter M10", "Platte_Mutter", "ISO 4032 M10, 8 verzinkt", "M10", "Haelt die Plattenschraube.", ["Sechskantmutter."]),
        nt("drehschraube", f"Drehpunktschraube M8 x {bolts['M8']}", "Dreh_Schraube", "ISO 4017 M8, 8.8 verzinkt", f"M8 x {bolts['M8']}",
           "Haelt die zwei Laschen als Schere zusammen; traegt planmaessig nichts.", [f"Sitzt {P['pivot_out']:g} mm vor dem Rohrmund ausserhalb des Rohrs."]),
        nt("drehscheibe_oben", "Scheibe M8 oben", "Dreh_ScheibeO", "ISO 7089 8, verzinkt", "8,4 x 16 x 1,6", "Liegt unter dem Kopf der Drehpunktschraube.", ["Flache Scheibe."]),
        nt("drehscheibe_unten", "Scheibe M8 unten", "Dreh_ScheibeU", "ISO 7089 8, verzinkt", "8,4 x 16 x 1,6", "Liegt vor der Mutter der Drehpunktschraube.", ["Flache Scheibe."]),
        nt("drehmutter", "Mutter M8", "Dreh_Mutter", "ISO 4032 M8, 8 verzinkt", "M8", "Haelt die Drehpunktschraube.", ["Sechskantmutter."]),
    ]
    out = {"komponente": "knoten_schere", "datei": "designs/components/knoten_schere.sc", "teilenummer": "T60S", "stand": "pilot",
           "titel": "Scherenknoten (Plattenpaar + Schere je Strebe), Detailmodell mit einem Arm B",
           "kurz": "Zwei Lochplatten (oben und unten) verbinden die Streben eines Knotens; die Laschenaugen liegen dazwischen. Jede Strebe haengt mit einer Schere aus zwei gekreuzten Laschen an einem Plattenloch; die zwei Nasen der Schere stehen durch zwei Gegenloecher im Rohr. Die Montage setzt je Knoten ein Plattenpaar und 4, 5 oder 6 Arme.",
           "hinweis": "Abnahme-Vorlage fuer Ben (N-VERBINDER). Alle Kopfmasse sind Annahmen aus dem Foto ohne Massstab (R56). Offen bei Ben: Rundrohr statt Vierkant, Laschendicke 5 oder 8 mm, Lochbild der 5-wertigen Knoten.",
           "koerperzahl": 13,
           "gruppen": [{"id": "platte", "name": "Plattenpaar", "kurz": "Obere und untere Platte, ein Paar je Knoten (W83).", "teile": ["lochplatte", "lochplatte_unten", "plattenschraube", "plattenscheibe_oben", "plattenscheibe_unten", "plattenmutter"]},
                       {"id": "schere", "name": "Schere", "kurz": "Zwei Laschen mit Nasen und Drehpunkt; eine je Strebenende.", "teile": ["lasche_1", "lasche_2", "drehschraube", "drehscheibe_oben", "drehscheibe_unten", "drehmutter"]},
                       {"id": "rohr", "name": "Rohrende", "kurz": "Strebe mit zwei Gegenloechern.", "teile": ["rohrende"]}],
           "teile": teile}
    json.dump(out, open(os.path.join(sc.ROOT, "data", "parts", "knoten_schere.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("data/parts/knoten_schere.json:", len(teile), "Teile")


if __name__ == "__main__":
    if "--render" in sys.argv:
        import render_knoten_schere
        render_knoten_schere.main()
        sys.exit(0)
    write_table()
    write_parts()
    if "--table" in sys.argv:
        sys.exit(0)
    for which in ("platte", "A", "B", "detail"):
        b, names = design(which)
        sc.run(b.write(f"knoten-schere-{which}"), OUT[which])
        print("gespeichert", OUT[which], len(names), "Koerper")
