"""R34 Strebenkonzept: Verschnitt, Geometriegrenze, Toleranzen, Knickung (nachvollziehbare Rechnung).

Aufruf: python scripts/strut_cutting.py   (nur Standardbibliothek, schreibt auf stdout)
Eingabe: data/layout.json (dome.nodes_list, dome.strut_len_mm). Herkunft der Annahmen steht bei den Konstanten.
"""
import json
import math
import os
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
LAYOUT = os.path.join(HERE, "..", "data", "layout.json")

# ---- Annahmen (Herkunft: docs/parts/knoten.md, Job R34) ------------------------------------------------------------
E_NOM = 120          # mm Strebenende bis Knotenmitte im Modell (strut_end_offset)
INSERT = 80          # mm Stecktiefe (hub_insert)
BALL_R = 50          # mm Knotenkugel D100
PROFILE = 30         # mm Strebenprofil 30 x 30
ARM = 23.0           # mm Steckarm Aussenmass (23 x 23 x 3)
ARM_T = 3.0          # mm Steckarm Wand
KERF = 3.0           # mm Saegeschnitt (Job)
EDGE_CLEAR = 8.0     # mm Zuschlag Montagespiel/Schweissverzug am Knoten [A]
STOCK_MM = [3000, 3500, 4000, 6000, 6500, 7000]   # Job: gaengige Lagerlaengen; 7000 zusaetzlich (Handel listet 6/7/12 m)
E_MOD = 210000.0     # N/mm2

dome = json.load(open(LAYOUT, encoding="utf-8"))["dome"]
nodes = [(n["x"], n["y"], n["z"]) for n in dome["nodes_list"]]
lens = dome["strut_len_mm"]
A_NODE = min(lens)
B_NODE = max(lens)
N_A = sum(1 for v in lens if v == A_NODE)
N_B = sum(1 for v in lens if v == B_NODE)


def dist(p, q):
    return math.dist(p, q)


# ---- 1. Winkel zwischen Streben am Knoten -> kleinster Strebenabstand zur Kugel -------------------------------------
def min_angle_deg():
    best = (999.0, None)
    for i, p in enumerate(nodes):
        dirs = []
        for j, q in enumerate(nodes):
            if i == j:
                continue
            d = dist(p, q)
            if any(abs(d - L) <= 40 for L in (A_NODE, B_NODE)):
                dirs.append(tuple((q[k] - p[k]) / d for k in range(3)))
        for u, v in combinations(dirs, 2):
            c = max(-1.0, min(1.0, sum(a * b for a, b in zip(u, v))))
            ang = math.degrees(math.acos(c))
            if ang < best[0]:
                best = (ang, i)
    return best


ang_min, ang_node = min_angle_deg()
half_diag = PROFILE / 2 * math.sqrt(2)          # Ecke des Strebenquerschnitts
e_ball = math.sqrt(max(BALL_R ** 2 - half_diag ** 2, 0.0))   # Ende muss ausserhalb der Kugel liegen
e_pair = half_diag / math.sin(math.radians(ang_min / 2))    # zwei Streben beruehren sich nicht (Umkreis)
E_MIN = math.ceil(max(e_ball, e_pair) + EDGE_CLEAR)

L_FEAS = A_NODE - 2 * E_MIN         # laengste gemeinsame Rohrlaenge, die an der A-Strebe noch passt


# ---- 2. Verschnitt (1D) ---------------------------------------------------------------------------------------------
def best_bars(stock, la, na, lb, nb):
    """Minimale Stangenzahl fuer na Stuecke la und nb Stuecke lb aus Stangen der Laenge stock (Kerf je Stueck)."""
    wa, wb = la + KERF, lb + KERF
    if (na and wa > stock) or (nb and wb > stock):
        return None
    pats = []
    for a in range(0, na + 1):
        if a * wa > stock:
            break
        for b in range(0, nb + 1):
            if a * wa + b * wb <= stock and (a or b):
                pats.append((a, b))
    inf = 10 ** 9
    f = [[inf] * (nb + 1) for _ in range(na + 1)]
    f[0][0] = 0
    for a in range(na + 1):
        for b in range(nb + 1):
            if f[a][b] == inf:
                continue
            for pa, pb in pats:
                na2, nb2 = min(na, a + pa), min(nb, b + pb)
                if f[a][b] + 1 < f[na2][nb2]:
                    f[na2][nb2] = f[a][b] + 1
    return f[na][nb]


def variant_rows(name, la, lb, stocks=STOCK_MM):
    rows = []
    used = la * N_A + lb * N_B
    for s in stocks:
        bars = best_bars(s, la, N_A, lb, N_B)
        if bars is None:
            rows.append((s, None, None, None))
            continue
        total = bars * s
        rows.append((s, bars, total / 1000.0, 100.0 * (total - used) / total))
    return rows


# ---- 3. Knicken (Euler, gelenkig) und gestufte Saeule ----------------------------------------------------------------
def sq_tube_I(b, t):
    return (b ** 4 - (b - 2 * t) ** 4) / 12.0


def sq_tube_A(b, t):
    return b * b - (b - 2 * t) ** 2


def euler_kn(i_mm4, length):
    return math.pi ** 2 * E_MOD * i_mm4 / length ** 2 / 1000.0


def stepped_buckling_kn(length, segs):
    """Kleinste Knicklast (gelenkig) fuer EI(x); segs = Liste (x_start, x_end, I). Schiessverfahren mit RK4."""
    def ei(x):
        for a, b, i in segs:
            if a <= x <= b:
                return E_MOD * i
        return E_MOD * segs[-1][2]

    def endval(p):
        n = 2000
        h = length / n
        y, v = 0.0, 1.0
        x = 0.0
        for _ in range(n):
            def f(xx, yy, vv):
                return vv, -p / ei(xx) * yy
            k1 = f(x, y, v)
            k2 = f(x + h / 2, y + h / 2 * k1[0], v + h / 2 * k1[1])
            k3 = f(x + h / 2, y + h / 2 * k2[0], v + h / 2 * k2[1])
            k4 = f(x + h, y + h * k3[0], v + h * k3[1])
            y += h / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
            v += h / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
            x += h
        return y

    lo = 1.0
    hi = 1.0
    prev = endval(lo)
    while True:
        hi *= 1.15
        cur = endval(hi)
        if prev > 0 >= cur:
            break
        prev = cur
        lo = hi
        if hi > 1e7:
            return float("nan")
    for _ in range(40):
        mid = (lo + hi) / 2
        if endval(mid) > 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2 / 1000.0


def column_segments(node_len, e, insert, i_strut, i_arm, mid_ball=True):
    """Saeule Knotenmitte-Knotenmitte: Arm frei (0..e), Ueberlappung (e..e+insert), Strebe allein, symmetrisch."""
    segs = [(0.0, e, i_arm), (e, e + insert, i_strut + i_arm), (e + insert, node_len - e - insert, i_strut),
            (node_len - e - insert, node_len - e, i_strut + i_arm), (node_len - e, node_len, i_arm)]
    return segs


def fmt(v, nd=1):
    return "-" if v is None else f"{v:.{nd}f}"


def main():
    print("=== Eingaben ===")
    print(f"Streben: {N_A} x A (Knoten-Knoten {A_NODE}), {N_B} x B ({B_NODE}) aus data/layout.json")
    print(f"Steckaufnahme je Ende {E_NOM} mm -> Rohr A {A_NODE - 2 * E_NOM}, B {B_NODE - 2 * E_NOM}")
    print(f"kleinster Winkel zwischen zwei Streben an einem Knoten: {ang_min:.1f} Grad (Knoten Nr. {ang_node})")
    print(f"Mindestabstand Strebenende-Knotenmitte: Kugel {e_ball:.1f} mm, Strebenpaar {e_pair:.1f} mm, + {EDGE_CLEAR:.0f} mm Zuschlag -> E_MIN = {E_MIN} mm")
    print(f"=> laengste gemeinsame Rohrlaenge, die an der A-Strebe passt: {A_NODE} - 2 x {E_MIN} = {L_FEAS} mm")

    print("\n=== V2 wie im Job gestellt: EINE Laenge 3468 fuer alle ===")
    e_a = (A_NODE - (B_NODE - 2 * E_NOM)) / 2
    print(f"A-Strebe: Abstand Rohrende-Knotenmitte = ({A_NODE} - {B_NODE - 2 * E_NOM}) / 2 = {e_a:.1f} mm  (negativ: Rohr reicht {-e_a:.1f} mm ueber die Knotenmitte hinaus) -> geometrisch unmoeglich")
    print(f"Die geforderten 214,5 mm tieferes Einstecken wuerden das Strebenende auf {E_NOM - 214.5:.1f} mm bringen; Minimum waere {E_MIN} mm.")

    variants = []
    variants.append(("V1  Zuschnitt auf Mass, e=120 (A 3039 / B 3468)", A_NODE - 240, B_NODE - 240))
    # V1b: A und B zusammen in eine 6,5-m-Stange: e so waehlen, dass A+B+2 Kerf passen
    e_pair_fit = math.ceil((A_NODE + B_NODE - (6500 - 2 * KERF)) / 4)
    variants.append((f"V1b zwei Laengen, e={e_pair_fit} fuer A+B in 6,5 m", A_NODE - 2 * e_pair_fit, B_NODE - 2 * e_pair_fit))
    e_pair6 = math.ceil((A_NODE + B_NODE - (6000 - 2 * KERF)) / 4)
    variants.append((f"V1c zwei Laengen, e={e_pair6} fuer A+B in 6,0 m", A_NODE - 2 * e_pair6, B_NODE - 2 * e_pair6))
    variants.append((f"V2a gemeinsame Laenge {L_FEAS} (groesster Wert, A-Strebe e={E_MIN})", L_FEAS, L_FEAS))
    variants.append((f"V2b gemeinsame Laenge {A_NODE - 240} (A unveraendert, e_A=120)", A_NODE - 240, A_NODE - 240))
    l6 = int((6000 - KERF) // 2 - KERF)     # zwei Stuecke je 6,0-m-Stange
    variants.append((f"V2c gemeinsame Laenge {l6} (zwei je 6,0-m-Stange)", l6, l6))
    l7 = L_FEAS
    variants.append((f"V2d gemeinsame Laenge {l7} auf 7,0-m-Stangen", l7, l7))

    print("\n=== Verschnitt je Variante und Lagerlaenge (Stangenzahl / Einkauf in m / Verschnitt in Prozent des Einkaufs) ===")
    header = "Variante".ljust(66) + "".join(f"{s / 1000:>14.1f} m" for s in STOCK_MM)
    print(header)
    for name, la, lb in variants:
        rows = variant_rows(name, la, lb)
        cells = []
        for s, bars, tot, pct in rows:
            cells.append("  geht nicht" if bars is None else f"{bars:>4d}/{tot:>6.1f}/{pct:>4.1f}%")
        print(name.ljust(66) + " ".join(cells))
    exact = (N_A * (A_NODE - 240) + N_B * (B_NODE - 240)) / 1000
    print(f"Handler-Zuschnitt exakt V1: {exact:.1f} m Rohr, 0 % Verschnitt beim Besteller (Reststuecke bleiben beim Handler)")

    print("\n=== Armlaengen und freie Arme (Knotenmitte bis Rohrende e; frei sichtbar = e - Kugelradius) ===")
    for name, la, lb in variants:
        ea, eb = (A_NODE - la) / 2, (B_NODE - lb) / 2
        print(f"{name.ljust(66)} e_A={ea:6.1f}  e_B={eb:6.1f}  freier Arm A {ea - BALL_R:6.1f}  B {eb - BALL_R:6.1f}  Armlaenge ab Mitte A {ea + INSERT:6.1f}  B {eb + INSERT:6.1f}")

    print("\n=== Knicken (Euler, gelenkig, E = 210000 N/mm2) ===")
    for t in (2.0, 3.0):
        i_s = sq_tube_I(PROFILE, t)
        a_s = sq_tube_A(PROFILE, t)
        r = math.sqrt(i_s / a_s)
        print(f"Profil 30x30x{t:.0f}: I = {i_s:,.0f} mm4, A = {a_s:.0f} mm2, i = {r:.1f} mm; "
              f"Euler A-Strebe (Knoten-Knoten {A_NODE}) {euler_kn(i_s, A_NODE):.1f} kN (Schlankheit {A_NODE / r:.0f}), "
              f"B-Strebe ({B_NODE}) {euler_kn(i_s, B_NODE):.1f} kN (Schlankheit {B_NODE / r:.0f})")
    i_arm = (ARM ** 4 - (ARM - 2 * ARM_T) ** 4) / 12.0
    print(f"Steckarm 23x23x3: I = {i_arm:,.0f} mm4")
    print("Gestufte Saeule (Arm frei, Ueberlappung 80 mm, Strebe allein), Profil 30x30x2, gelenkig in der Knotenmitte:")
    i_s2 = sq_tube_I(PROFILE, 2.0)
    for label, node_len, e in (("A V1 e=120", A_NODE, 120.0), ("B V1 e=120", B_NODE, 120.0),
                               (f"B V2c e={(B_NODE - l6) / 2:.0f}", B_NODE, (B_NODE - l6) / 2),
                               (f"B V2a e={(B_NODE - L_FEAS) / 2:.0f}", B_NODE, (B_NODE - L_FEAS) / 2),
                               (f"A V2c e={(A_NODE - l6) / 2:.0f}", A_NODE, (A_NODE - l6) / 2)):
        segs = column_segments(node_len, e, INSERT, i_s2, i_arm)
        print(f"  {label.ljust(14)} Knicklast {stepped_buckling_kn(node_len, segs):5.2f} kN")

    print("\n=== Toleranzen und Spiel ===")
    print("Annahmen: Sage vor Ort +-1 mm [A], Haendlerzuschnitt +-4 mm [Q eBay-Angebot 30x30x3 'Toleranz +-4 mm'], Bohrlehre Lochabstand +-0,3 mm [A],")
    print("Lochspiel M10 in D11: +-0,5 mm je Gelenk, Armlaenge am Knoten +-1 mm (docs/parts/knoten.md Montage 6).")
    def uni(tol):
        return tol / math.sqrt(3)
    for label, cut in (("Bohrung vom Rohrende gemessen, Haendlerschnitt +-4", 4.0), ("Bohrung vom Rohrende gemessen, Saege vor Ort +-1", 1.0)):
        comps = [cut, 0.3, 0.5 * 2, 1.0 * 2]       # Schnitt, Lochlage, Lochspiel (2 Enden), Arme (2 Knoten)
        # Bohrung vom Ende: Schnitt wirkt ueber den Lochabstand nicht (beide Bohrungen am selben Rohr, je 50 mm vom Ende): Schnitt = Fehler der Rohrlaenge
        worst = sum(comps)
        rms = math.sqrt(sum(uni(c) ** 2 for c in comps))
        print(f"  {label.ljust(54)} je Strebe Worst-Case +-{worst:.1f} mm, RMS {rms:.1f} mm")
    comps = [0.3, 0.5 * 2, 1.0 * 2]
    worst = sum(comps)
    rms = math.sqrt(sum(uni(c) ** 2 for c in comps))
    print(f"  {'Lochabstand mit Bohrlehre (Loch zu Loch)'.ljust(54)} je Strebe Worst-Case +-{worst:.1f} mm, RMS {rms:.1f} mm")
    for label, rms_s in (("Haendlerschnitt", math.sqrt(sum(uni(c) ** 2 for c in [4.0, 0.3, 1.0, 2.0]))),
                         ("Bohrlehre", rms)):
        print(f"  Summenfehler RMS {label}: Basisring (10 B-Streben) {rms_s * math.sqrt(10):.1f} mm, Meridian Boden-Spitze (4 Streben) {rms_s * 2:.1f} mm, alle 65 Streben {rms_s * math.sqrt(65):.1f} mm")
    for t in (2.0, 3.0):
        clear = (PROFILE - 2 * t) - ARM
        print(f"  Spiel Arm 23 in Strebe 30x30x{t:.0f}: {clear:.1f} mm gesamt -> Kippen um {math.degrees(math.atan(clear / INSERT)):.1f} Grad auf {INSERT} mm Stecktiefe, {clear / INSERT * 1000:.0f} mm je Meter Strebe")

    print("\n=== Schraube M10 8.8 und Rohrwand (EN 1993-1-8 Tab. 3.4, gamma_M2 = 1,25) ===")
    as_m10, fub, fu_s = 58.0, 800.0, 360.0
    fv = 0.6 * fub * as_m10 / 1.25 / 1000
    print(f"Abscheren je Scherflaeche: 0,6 x {fub:.0f} x {as_m10:.0f} / 1,25 = {fv:.1f} kN; zwei Scherflaechen: {2 * fv:.1f} kN")
    for label, t, e2 in (("Strebenwand 2 mm", 2.0, PROFILE / 2), ("Strebenwand 3 mm", 3.0, PROFILE / 2), ("Steckarm 3 mm", 3.0, ARM / 2)):
        d0 = 11.0
        k1 = min(2.8 * e2 / d0 - 1.7, 2.5)
        e1 = 50.0
        ab = min(e1 / (3 * d0), fub / fu_s, 1.0)
        fb = k1 * ab * fu_s * 10.0 * t / 1.25 / 1000
        print(f"Lochleibung {label}: k1 = {k1:.2f}, alpha_b = {ab:.2f} -> {fb:.1f} kN je Wand, beide Waende {2 * fb:.1f} kN")
    print("Die Bohrung liegt bei allen Varianten 50 mm hinter dem Strebenende; tieferes Einstecken aendert Lochlage und Wandquerschnitt nicht.")


if __name__ == "__main__":
    main()
