"""N-VERBINDER Montage (D91): Lage der Scherenknoten-Instanzen und der Rundrohr-Streben im Modellrahmen.

Quelle: data/components/knoten_schere.json (Werkstatt, Layout-Rahmen = OBJ, Z ab Kuppelboden) und die Strebenachsen
segs (gen_dome.py t1_t3_t4, Modellrahmen: um ROT gedreht, Z ab Fundament). Je Knoten:
  Plattenpaar: Ursprung Knotenpunkt, Z = Normale, X = x_richtung (Werkstatt-Tabelle, um ROT gedreht)
  Arm: Bauteil-Rahmen -> erst um Z um drehwinkel_loch drehen, dann um die Achse der Plattenschraube (Lochkreis r) um
       drehung_um_plattenschraube -> Plattenrahmen -> Welt.
Strebe: Rundrohr vom Rohrmund des Arms am Knoten A bis zum Rohrmund am Knoten B (echte Lage der Schere; an den
5-wertigen Knoten liegt die Rohrachse bis 15 mm neben dem Knotenpunkt, D91 einheitliche 6-Loch-Platte).
Aufruf: python -X utf8 scripts/knoten_montage.py   (druckt die Auswertung; gen_dome.py importiert die Funktionen)"""
import json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(HERE, "workshop"))
import knoten_schere as KS   # Geo (Rohrmund, Achse je Typ), P (Lochkreis)

dot = lambda a, b: sum(a[i] * b[i] for i in range(3))
cross = lambda a, b: [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]
unit = lambda a: [x / math.sqrt(dot(a, a)) for x in a]
sub = lambda a, b: [a[i] - b[i] for i in range(3)]


def rz(deg):
    c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    return [[c, -s, 0], [s, c, 0], [0, 0, 1]]


def mm(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(3)) for j in range(3)] for i in range(3)]


def mv(A, v):
    return [sum(A[i][k] * v[k] for k in range(3)) for i in range(3)]


def matrix12(R, t):
    """3x3 Drehung + Verschiebung -> 12er-Liste fuer occurrence.move (Zeilen: r00 r01 r02 tx, ...)."""
    return [round(v, 9) for v in (R[0][0], R[0][1], R[0][2], t[0], R[1][0], R[1][1], R[1][2], t[1], R[2][0], R[2][1], R[2][2], t[2])]


def arm_local(arm):
    """Arm-Bauteil -> Plattenrahmen: (R, t) mit p_platte = R p + t."""
    th, de = arm["drehwinkel_loch_grad"], arm["drehung_um_plattenschraube_grad"]
    rc = KS.P["bolt_circle_r"]
    h = [rc * math.cos(math.radians(th)), rc * math.sin(math.radians(th)), 0.0]
    R = mm(rz(de), rz(th))
    t = sub(h, mv(rz(de), h))                       # Drehung um die Achse durch h
    return R, t


def knoten_welt(segs, rot_deg):
    """Knoten-Lagen im Modellrahmen: {knoten-id 'nNN': (Ursprung, R_platte)}; Ursprung aus den Strebenenden (wie knoten_anker)."""
    doc = json.load(open(os.path.join(ROOT, "data", "components", "knoten_schere.json"), encoding="utf-8"))
    lay = json.load(open(os.path.join(ROOT, "data", "layout.json"), encoding="utf-8"))["dome"]["nodes_list"]
    ra = math.radians(rot_deg)
    rotz = lambda v: [v[0] * math.cos(ra) - v[1] * math.sin(ra), v[0] * math.sin(ra) + v[1] * math.cos(ra), v[2]]
    ends = {}
    for A, B in segs:
        for q in (A, B):
            ends.setdefault(tuple(round(v / 20) for v in q), []).append(q)
    E = [tuple(sum(v[i] for v in l) / len(l) for i in range(3)) for l in ends.values()]
    out = {}
    for row in doc["knoten"]:
        i = int(row["knoten"][1:])
        n = lay[i - 1]
        x, y, _ = rotz([n["x"], n["y"], 0])
        e = min(E, key=lambda e: math.hypot(e[0] - x, e[1] - y))
        assert math.hypot(e[0] - x, e[1] - y) < 30, f"Knoten {row['knoten']} nicht an einem Strebenende"
        Z = unit(rotz(row["normale"])); X = rotz(row["x_richtung"])     # Tabelle auf 4 Stellen gerundet: X gegen Z orthonormieren (starre Matrix)
        X = unit([X[i] - dot(X, Z) * Z[i] for i in range(3)]); Y = cross(Z, X)
        R = [[X[0], Y[0], Z[0]], [X[1], Y[1], Z[1]], [X[2], Y[2], Z[2]]]
        out[row["knoten"]] = (list(e), R, row)
    return out


def montage(segs, rot_deg):
    """Rueckgabe: platten [(knoten, matrix12)], arme {'A'|'B': [(knoten, nachbar, matrix12)]}, streben [dict], auswertung."""
    K = knoten_welt(segs, rot_deg)
    geo = {t: KS.Geo(t) for t in "AB"}
    def nid(p):
        return min(K, key=lambda k: math.dist(K[k][0], p))
    platten, arme, mund = [], {"A": [], "B": []}, {}
    seg_pairs = {}
    for A, B in segs:
        a, b = nid(A), nid(B)
        seg_pairs[frozenset((a, b))] = (A, B, a, b)
    for k, (o, Rp, row) in sorted(K.items()):
        platten.append((k, matrix12(Rp, o)))
        for arm in row["arme"]:
            nb = f"n{arm['nachbar']:02d}"
            if frozenset((k, nb)) not in seg_pairs:
                continue                              # Strebe entfaellt (Basiskante des Tuerfelds): kein Arm
            Rl, tl = arm_local(arm)
            R = mm(Rp, Rl); t = [o[i] + mv(Rp, tl)[i] for i in range(3)]
            arme[arm["typ"]].append((k, nb, matrix12(R, t)))
            g = geo[arm["typ"]]
            mund[(k, nb)] = ([mv(R, g.tube0)[i] + t[i] for i in range(3)], unit(mv(R, g.u)), arm["typ"])
    streben, dev = [], []
    for (A, B, a, b) in seg_pairs.values():
        pa, ua, ta = mund[(a, b)]; pb, ub, tb = mund[(b, a)]
        assert ta == tb
        d = sub(pb, pa); L = math.sqrt(dot(d, d)); u = unit(d)
        streben.append({"knoten": (a, b), "typ": ta, "start": pa, "u": u, "laenge": L,
                        "knick_a": math.degrees(math.acos(max(-1, min(1, dot(u, ua))))),
                        "knick_b": math.degrees(math.acos(max(-1, min(1, -dot(u, ub)))))})
        dev.append(L)
    return platten, arme, streben, K


def strebe_matrix(s, center, L_nom):
    """Lage einer Streben-Instanz (scripts/components/strebe.py): Rohr L_nom mittig zwischen die zwei Rohrmuender,
    Z = Achse, X = Kuppel aussen (Laschennormale, senkrecht zur Achse), Y = Z x X (Nasenrichtung). Rueckgabe (matrix12, Spalt je Ende mm)."""
    u = s["u"]; gap = (s["laenge"] - L_nom) / 2
    p = [s["start"][i] + u[i] * gap for i in range(3)]
    m = [s["start"][i] + u[i] * s["laenge"] / 2 - center[i] for i in range(3)]
    x = unit([m[i] - dot(m, u) * u[i] for i in range(3)])
    y = cross(u, x)
    return matrix12([[x[0], y[0], u[0]], [x[1], y[1], u[1]], [x[2], y[2], u[2]]], p), gap


if __name__ == "__main__":
    segs = json.load(open(os.path.join(HERE, ".segs.json")))
    P = {k: v["value"] for k, v in json.load(open(os.path.join(ROOT, "data", "params.json"), encoding="utf-8")).items()}
    platten, arme, streben, K = montage(segs, P["door_az"] - 167)
    print("Platten", len(platten), "Arme A", len(arme["A"]), "B", len(arme["B"]), "Streben", len(streben))
    for t in "AB":
        L = [s["laenge"] for s in streben if s["typ"] == t]
        kn = [max(s["knick_a"], s["knick_b"]) for s in streben if s["typ"] == t]
        gaps = [(s["laenge"] - (KS.P['strut_' + t.lower()] - 2 * KS.Geo(t).node_to_tube)) / 2 for s in streben if s["typ"] == t]
        print(f"Typ {t}: Spalt Rohrende-Rohrmund je Ende {min(gaps):+.2f} .. {max(gaps):+.2f} mm")
        print(f"Typ {t}: n {len(L)}  Rohrmund-Rohrmund {min(L):.2f} .. {max(L):.2f} mm  Soll {KS.P['strut_' + t.lower()] - 2 * KS.Geo(t).node_to_tube:.2f}  groesster Achsknick {max(kn):.3f} Grad")
