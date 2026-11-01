"""R41 Laschen-Scheiben-Knoten: Abkantwinkel, Laschenlaenge, Knicklast, Teilezahl (nachvollziehbare Rechnung).

Aufruf: python -X utf8 scripts/lasche_check.py   (nur Standardbibliothek, schreibt auf stdout, aendert nichts)
Eingabe: data/layout.json (dome.nodes_list, dome.strut_len_mm). Herkunft der Annahmen steht bei den Konstanten.
Kennzeichnung: [E] eigene Rechnung, [A] Annahme, [Q] Quelle (siehe docs/research/R41.md).
Selbsttest laeuft am Ende mit; bei Fehler Abbruch mit Exit-Code 1.
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LAYOUT = os.path.join(HERE, "..", "data", "layout.json")

# ---- Annahmen ------------------------------------------------------------------------------------------------------
E_MOD = 210000.0     # N/mm2 Stahl [Q: EN 1993-1-1 Abschn. 3.2.6, gleicher Wert wie R34]
FY = 235.0           # N/mm2 S235 [A]
FU = 360.0           # N/mm2 S235 [A]
GAMMA_M2 = 1.25      # EN 1993-1-8 Tab. 2.1 [Q]
DISC_R = 55.0        # mm Scheibenradius (Foto-Schaetzung D ca. 100-110 mm) [A]
RK = 37.0            # mm Lochkreisradius der Scheibenschrauben [A]
TUBE_GAP = 15.0      # mm Abstand Rohrende zum Scheibenrand (Montagespiel) [A]
BOLT_BEHIND = 50.0   # mm Rohrschraube hinter dem Rohrende (gleiches Mass wie Querbolzen knoten.md, bolt_dist) [A]
LASCHE_B = 40.0      # mm Laschenbreite [A] (Foto: eher 20-25 mm, hier bewusst grosszuegig)
LASCHE_T = 6.0       # mm Laschendicke [A]
BOLT_D = 10.0        # mm Schraube M10 [A, gleiche Groesse wie Kugelknoten]
HOLE_D = 11.0        # mm Durchgangsloch M10, ISO 273 mittel [Q, wie knoten.md]
TUBE_I = 29419.0     # mm4 Rohr 30x30x2: (30^4-26^4)/12 [E]; Strebenprofil laut R34
R34_TUBE_LEN = 2995  # mm V2c, eine Rohrlaenge (D59)
R_SPHERE = None      # wird aus layout.json bestimmt


def load():
    d = json.load(open(LAYOUT, encoding="utf-8"))["dome"]
    nodes = [(n["x"], n["y"], n["z"], n["valence"]) for n in d["nodes_list"]]
    lens = sorted(set(d["strut_len_mm"]))
    return d, nodes, lens


def sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def dot(a, b):
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def norm(a):
    return math.sqrt(dot(a, a))


def unit(a):
    n = norm(a)
    return (a[0] / n, a[1] / n, a[2] / n)


def cross(a, b):
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def build(d, nodes, lens):
    """Kugel (Mitte auf Hoehe base_z), Nachbarn je Knoten, Strebenwinkel gegen Tangentialebene, Winkel in der Ebene."""
    cz = d["base_z"]
    centre = (0.0, 0.0, cz)
    radii = [norm(sub(n[:3], centre)) for n in nodes]
    r = sum(radii) / len(radii)
    nb = {i: [] for i in range(len(nodes))}
    for i in range(len(nodes)):
        for j in range(len(nodes)):
            if i == j:
                continue
            dist = norm(sub(nodes[j][:3], nodes[i][:3]))
            for L in lens:
                if abs(dist - L) < 40:
                    nb[i].append((j, "A" if L == lens[0] else "B", dist))
    out = {}
    for i, n in enumerate(nodes):
        nrm = unit(sub(n[:3], centre))
        # Basis der Tangentialebene
        ref = (0.0, 0.0, 1.0) if abs(nrm[2]) < 0.9 else (1.0, 0.0, 0.0)
        e1 = unit(cross(ref, nrm))
        e2 = cross(nrm, e1)
        arms = []
        for j, typ, dist in nb[i]:
            v = unit(sub(nodes[j][:3], n[:3]))
            tilt = math.degrees(math.asin(dot(v, nrm)))          # negativ: Strebe neigt von der Ebene weg, nach innen
            ang = math.degrees(math.atan2(dot(v, e2), dot(v, e1))) % 360.0
            arms.append({"to": j, "typ": typ, "len": dist, "tilt": tilt, "ang": ang})
        arms.sort(key=lambda a: a["ang"])
        out[i] = arms
    return r, out


def gaps(arms):
    a = [x["ang"] for x in arms]
    return [(a[(k + 1) % len(a)] - a[k]) % 360.0 for k in range(len(a))]


def signature(arms):
    """Knotenform bis auf Drehung und Spiegelung: zyklische Folge (Strebentyp, Winkel zum naechsten), gerundet 1 Grad."""
    g = gaps(arms)
    seq = [(arms[k]["typ"], round(g[k])) for k in range(len(arms))]
    cands = []
    n = len(seq)
    mirror = [(arms[n - 1 - k]["typ"], round(g[(n - 2 - k) % n])) for k in range(n)]
    for s in (seq, mirror):
        for k in range(len(s)):
            cands.append(tuple(s[k:] + s[:k]))
    return min(cands)


def angle_signature(arms):
    """Nur Winkelfolge in der Ebene (Lochbild der Scheibe), zyklisch, mit Spiegelung."""
    g = [round(x) for x in gaps(arms)]
    cands = []
    for s in (g, g[::-1]):
        for k in range(len(s)):
            cands.append(tuple(s[k:] + s[:k]))
    return min(cands)


def stepped_euler(segments):
    """Kleinste Knicklast eines beidseits gelenkigen Stufenstabs, segments=[(Laenge mm, EI Nmm2)], exakte Uebertragung.
    Findet die erste Nullstelle von y(L)(P) durch Absuchen + Bisektion."""
    total = sum(s[0] for s in segments)

    def yend(P):
        y, yp = 0.0, 1.0
        for L, EI in segments:
            k = math.sqrt(P / EI)
            c, s = math.cos(k * L), math.sin(k * L)
            y, yp = y * c + yp * s / k, -y * k * s + yp * c
        return y

    lo = 1.0
    hi = 1.0
    f_lo = yend(lo)
    p = lo
    step = 1.02
    while p < 5e7:
        p2 = p * step
        if yend(p2) * f_lo <= 0:
            lo, hi = p, p2
            break
        p = p2
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if yend(lo) * yend(mid) <= 0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi), total


def euler(EI, L, K=1.0):
    return math.pi ** 2 * EI / (K * L) ** 2


def lasche_geometry(L_node, tube_len):
    """Rohrende-Abstand von der Knotenmitte, freie Laschenlaenge (Scheibenrand bis Rohrende), Laschenlaenge Loch zu Loch."""
    end = (L_node - tube_len) / 2.0                 # Rohrende bis Knotenmitte (Achsmass)
    free = end - DISC_R                              # sichtbar freie Lasche zwischen Scheibenrand und Rohrende
    total = (end + BOLT_BEHIND) - RK                 # Loch (Scheibenschraube, Radius RK) bis Loch (Rohrschraube)
    return end, free, total


def tube_len_max(L_min_node):
    return L_min_node - 2.0 * (DISC_R + TUBE_GAP)


def main(quiet=False):
    d, nodes, lens = load()
    R, arms = build(d, nodes, lens)
    LA, LB = lens[0], lens[-1]
    p = print if not quiet else (lambda *a, **k: None)

    p("== 1. Kugel und Strebenwinkel [E] ==")
    p("Kugelradius aus layout.json: %.1f mm (Mittelpunkt auf base_z %s)" % (R, d["base_z"]))
    tilts = {"A": [], "B": []}
    for i, ar in arms.items():
        for a in ar:
            tilts[a["typ"]].append(abs(a["tilt"]))
    for t, L in (("A", LA), ("B", LB)):
        tl = tilts[t]
        th = math.degrees(math.asin(L / (2 * R)))
        p("Strebe %s: Knotenabstand %d mm, Winkel gegen Tangentialebene mess %.2f..%.2f Grad, Formel asin(L/2R)=%.2f Grad"
          % (t, L, min(tl), max(tl), th))
    p("Abkantwinkel der Lasche (Scheibe in der Tangentialebene) = Neigung der Strebe: A %.1f / B %.1f Grad" %
      (sum(tilts["A"]) / len(tilts["A"]), sum(tilts["B"]) / len(tilts["B"])))
    h_note = []
    for t, th in (("A", sum(tilts["A"]) / len(tilts["A"])), ("B", sum(tilts["B"]) / len(tilts["B"]))):
        h_note.append((t, th))
    p("Exzentrizitaet [E]: Knickt die Lasche im Abstand r von der Mitte ab, liegt die Stabachse dort e = r*tan(theta) neben der "
      "Plattenmitte; bei r=RK=%.0f mm: A %.1f mm, B %.1f mm" % (
          RK, RK * math.tan(math.radians(h_note[0][1])), RK * math.tan(math.radians(h_note[1][1]))))
    p("Achsen treffen sich in einem Punkt, wenn die Scheibenebene um h = r*tan(theta) ueber dem Knotenpunkt liegt und die Lasche "
      "genau dort abknickt (r je Typ verschieden: A %.0f mm / B %.0f mm bei h = 12 mm)" % (
          12 / math.tan(math.radians(h_note[0][1])), 12 / math.tan(math.radians(h_note[1][1]))))

    p("\n== 2. Winkel in der Ebene und Teilezahl [E] ==")
    sig_full, sig_ang = {}, {}
    mins = []
    for i, ar in arms.items():
        sig_full.setdefault((nodes[i][3], signature(ar)), []).append(i)
        sig_ang.setdefault((nodes[i][3], angle_signature(ar)), []).append(i)
        mins.append(min(gaps(ar)))
    p("Kleinster Winkel zwischen zwei Streben in der Ebene: %.1f Grad (kleinster Wert aller Knoten)" % min(mins))
    p("Verschiedene Knotenformen (Wertigkeit + Strebentyp + Winkelfolge, auf 1 Grad gerundet, bis auf Drehung/Spiegelung): %d von %d Knoten"
      % (len(sig_full), len(nodes)))
    p("Verschiedene Scheiben-Lochbilder (nur Winkelfolge je Wertigkeit): %d" % len(sig_ang))
    p("Laschentypen: 2 (A, B) bei Abkantung je Typ, ohne Rohrenden-Variation; Laschen insgesamt %d (je Strebe 2)" % (2 * d["strut_len_mm"].__len__()))
    p("Bei freier Laschendrehung um die Einzelschraube reicht 1 Scheibe (6 Loecher + Mittelloch) fuer alle Knoten; die Lasche "
      "in der Ebene hat dann Versatz bis RK*sin(Abweichung vom 60-Grad-Raster)")
    worst = 0.0
    for i, ar in arms.items():
        g = gaps(ar)
        n = len(ar)
        raster = 360.0 / 6.0
        # Abweichung des Strebenwinkels von dem naechsten Loch eines 6er-Lochkreises (Drehung frei gewaehlt, einfache Schaetzung)
        best = min(max(abs(((a["ang"] - ar[0]["ang"] - off) + 30) % 60 - 30) for a in ar) for off in range(0, 60))
        worst = max(worst, best)
    p("Groesste Abweichung vom 60-Grad-Raster eines gemeinsamen Lochkreises: %.1f Grad -> in-plane Versatz e = RK*sin(.) = %.1f mm"
      % (worst, RK * math.sin(math.radians(worst))))

    p("\n== 3. Laschenlaenge und Rohrlaenge [E] ==")
    p("Annahmen: Scheibenradius %.0f, Lochkreis RK %.0f, Rohrspiel %.0f, Rohrschraube %.0f mm hinter Rohrende (alle [A])"
      % (DISC_R, RK, TUBE_GAP, BOLT_BEHIND))
    tmax = tube_len_max(LA)
    p("Groesste gemeinsame Rohrlaenge: %.0f mm (= %d - 2*(%.0f+%.0f)); V2c-Laenge %d mm passt: %s" % (
        tmax, LA, DISC_R, TUBE_GAP, R34_TUBE_LEN, "ja" if R34_TUBE_LEN <= tmax else "nein"))
    p("%-22s %8s %8s %10s %10s" % ("Fall", "Ende-Mitte", "frei", "Lasche L-L", "Knoten"))
    rows = []
    for name, tl in (("V2c 2995", R34_TUBE_LEN), ("max %d" % tmax, tmax)):
        for t, L in (("A", LA), ("B", LB)):
            end, free, tot = lasche_geometry(L, tl)
            rows.append((name, t, tl, end, free, tot))
            p("%-22s %8.1f %8.1f %10.1f   Strebe %s" % (name, end, free, tot, t))

    p("\n== 4. Knicklast der Lasche [E nach Euler, EN 1993-1-1 Pkt 6.3.1 Idee, ohne Imperfektionsbeiwert] ==")
    I_weak = LASCHE_B * LASCHE_T ** 3 / 12.0
    p("Lasche %.0f x %.0f mm, I_schwach = %.0f mm4, i = %.2f mm" % (LASCHE_B, LASCHE_T, I_weak, math.sqrt(I_weak / (LASCHE_B * LASCHE_T))))
    p("%-12s %-10s %8s %9s %9s %9s" % ("Fall", "Strebe", "frei mm", "K=1 kN", "K=0.7 kN", "K=2 kN"))
    for name, t, tl, end, free, tot in rows:
        P1 = euler(E_MOD * I_weak, free, 1.0) / 1000
        P07 = euler(E_MOD * I_weak, free, 0.7) / 1000
        P2 = euler(E_MOD * I_weak, free, 2.0) / 1000
        p("%-12s %-10s %8.1f %9.1f %9.1f %9.1f" % (name, t, free, P1, P07, P2))
    p("Querschnitt: Npl = %.1f kN, Nu,Rd netto = %.1f kN (EN 1993-1-1 6.2.3, 0.9*Anet*fu/gM2)" % (
        LASCHE_B * LASCHE_T * FY / 1000, 0.9 * (LASCHE_B - HOLE_D) * LASCHE_T * FU / GAMMA_M2 / 1000))
    # Lochleibung der Lasche (EN 1993-1-8 Tab. 3.4): Randabstand e1 = 2*d0
    e1 = 2 * HOLE_D
    ab = min(e1 / (3 * HOLE_D), 800.0 / FU, 1.0)
    k1 = 2.5
    Fb = k1 * ab * FU * BOLT_D * LASCHE_T / GAMMA_M2 / 1000
    AS_M10 = 58.0   # mm2 Spannungsquerschnitt M10, Gewinde in der Scherfuge (wie R34: 22,3 kN)
    Fv = 0.6 * 800.0 * AS_M10 / GAMMA_M2 / 1000
    p("Lochleibung Lasche t=%.0f (e1=%.0f): %.1f kN; M10 8.8 Abscheren je Schnittflaeche %.1f kN (Gewinde, EN 1993-1-8 Tab 3.4, wie R34)" % (
        LASCHE_T, e1, Fb, Fv))

    p("\n== 5. Strebe als Stufenstab (Rohr 30x30x2 + Lasche an beiden Enden), gelenkig am Scheibenbolzen [E] ==")
    p("%-12s %-8s %12s %12s %9s" % ("Fall", "Strebe", "nur Rohr kN", "Stufenstab", "Abfall"))
    for name, t, tl, end, free, tot in rows:
        # Stab von Scheibenschraube zu Scheibenschraube: Lasche (end-RK) je Seite + Rohr; Rohrschraube sitzt im Rohr, dort volle Rohrsteifigkeit
        # Konservativ: Lasche zaehlt bis zum Rohrende (Laschenanteil im Rohr = Rohr steif)
        lasche_len = end - RK
        segs = [(lasche_len, E_MOD * I_weak), (tl, E_MOD * TUBE_I), (lasche_len, E_MOD * I_weak)]
        P, Ltot = stepped_euler(segs)
        P_tube = euler(E_MOD * TUBE_I, Ltot) / 1000
        p("%-12s %-8s %12.2f %12.2f %8.0f %%" % (name, t, P_tube, P / 1000, (1 - P / 1000 / P_tube) * 100))

    p("\n== 5b. Empfindlichkeit: Laschendicke und Breite (Strebe B, Stufenstab, K=1) [E] ==")
    p("%-12s %6s %6s %10s %12s" % ("Fall", "b mm", "t mm", "I_schw mm4", "Stufenstab kN"))
    for name, t, tl, end, free, tot in rows:
        if t != "B":
            continue
        for b_, t_ in ((40, 6), (40, 8), (40, 10), (60, 10), (60, 12)):
            I_ = b_ * t_ ** 3 / 12.0
            ll = end - RK
            P, Ltot = stepped_euler([(ll, E_MOD * I_), (tl, E_MOD * TUBE_I), (ll, E_MOD * I_)])
            p("%-12s %6d %6d %10.0f %12.2f" % (name, b_, t_, I_, P / 1000))
    arm_I = (23.0 ** 4 - 17.0 ** 4) / 12.0
    p("Vergleich Kugelknoten-Steckarm 23x23x3 (knoten.md): I = %.0f mm4 (= %.0fx die Lasche 40x6); R34 rechnete dort 4,41 kN (B, V2c)" % (arm_I, arm_I / I_weak))

    p("\n== 6. Stahlmasse Laschen (E, ohne Zugaben) ==")
    mass_l = 0.0
    nb_ends = {"A": 0, "B": 0}
    for ar in arms.values():
        for a in ar:
            nb_ends[a["typ"]] += 1
    for t, L in (("A", LA), ("B", LB)):
        end, free, tot = lasche_geometry(L, R34_TUBE_LEN)
        m = LASCHE_B * LASCHE_T * (tot + LASCHE_B) * 7.85e-6   # +Endrundungen
        mass_l += m * nb_ends[t]
        p("Lasche %s: Loch-zu-Loch %.0f mm, %.2f kg, %d Stueck" % (t, tot, m, nb_ends[t]))
    disc = math.pi * DISC_R ** 2 * 8.0 * 7.85e-6
    p("Laschen gesamt %.0f kg, Scheiben %d x 8 mm Stahl %.2f kg = %.0f kg; Summe %.0f kg (Kugelknoten laut knoten.md: ca. 155 kg)" % (
        mass_l, len(nodes), disc, disc * len(nodes), mass_l + disc * len(nodes)))
    return {"R": R, "arms": arms, "nodes": nodes, "lens": lens, "tilts": tilts, "n_sig": len(sig_full), "n_ang": len(sig_ang),
            "rows": rows, "mins": mins}


def selftest():
    # Euler-Lehrbuchwert: 100x10 Flachstahl, I_schwach, L=1000, K=1: pi^2*E*I/L^2
    I = 100 * 10 ** 3 / 12.0
    assert abs(euler(E_MOD * I, 1000) - math.pi ** 2 * E_MOD * I / 1e6) < 1e-6
    # Stufenstab mit gleichen Segmenten == einfacher Euler
    P, _ = stepped_euler([(500, E_MOD * I), (500, E_MOD * I)])
    assert abs(P - euler(E_MOD * I, 1000)) / P < 1e-4, P
    # R34-Wert: Rohr 30x30x2, B 3708 -> 4,4 kN
    assert abs(euler(E_MOD * TUBE_I, 3708) / 1000 - 4.43) < 0.05
    res = main(quiet=True)
    assert len(res["nodes"]) == 26
    assert sum(len(a) for a in res["arms"].values()) == 130          # 65 Streben x 2 Enden
    for i, a in res["arms"].items():
        assert len(a) == res["nodes"][i][3], (i, len(a))             # Nachbarzahl == Wertigkeit
    for t, L in (("A", res["lens"][0]), ("B", res["lens"][-1])):
        th = math.degrees(math.asin(L / (2 * res["R"])))
        assert all(abs(x - th) < 0.15 for x in res["tilts"][t]), t
    assert min(res["mins"]) > 50
    print("\nSelbsttest bestanden")


if __name__ == "__main__":
    try:
        main()
        selftest()
    except AssertionError as e:
        print("Selbsttest FEHLER:", e)
        sys.exit(1)
