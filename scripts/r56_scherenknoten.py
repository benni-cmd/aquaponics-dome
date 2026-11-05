"""R56 Scherenknoten: Rechengrundlage (Geometrie der Schere, Profilvergleich Rund/Vierkant, grobe Statik).
Alle Kopfmasse sind Annahmen [A] aus dem Foto reference/chemnitz/laschenknoten-foto.jpg (kein Massstab, siehe R56).
Aufruf: python -X utf8 scripts/r56_scherenknoten.py   (Selbsttest am Ende, Exit 1 bei Fehler)"""
import math, sys

E, FY, FU = 210000.0, 235.0, 360.0          # N/mm2, S235 (R34: Tata/Applus)
GM0, GM1, GM2 = 1.0, 1.0, 1.25              # EN 1993-1-1/-1-8 Teilbeiwerte (Werte wie R34)
R = 6000.0                                   # Kuppelradius (layout.json)
L_NODE = {"A": 3279.0, "B": 3708.0}         # Knoten-Knoten (layout.json)
TILT = {s: math.degrees(math.asin(L / (2 * R))) for s, L in L_NODE.items()}   # Neigung gegen Tangentialebene

# --- Kopfmasse der Schere [A] (Prototyp)
P = dict(plate_d=110, plate_t=8, bolt_circle_r=37, center_hole=20,
         link_w=20, link_t=5, a_plate_to_pivot=50, b_pivot_to_nose=58,
         nose_w=10, nose_out=3, pivot_out=12, bend_r=63)

def tube_end_offset(tilt):
    """Abstand Knotenmitte -> Rohrende entlang der Strebenachse (Knick bei bend_r, Drehpunkt pivot_out vor dem Rohrende)."""
    along_bend = P["bend_r"] / math.cos(math.radians(tilt))
    pivot = along_bend + (P["bolt_circle_r"] + P["a_plate_to_pivot"] - P["bend_r"])
    return pivot + P["pivot_out"]

def round_tube(d, t):
    di = d - 2 * t
    return dict(name=f"Rund {d}x{t}", A=math.pi / 4 * (d**2 - di**2), I=math.pi / 64 * (d**4 - di**4), inner=di, outer=d)

def square_tube(a, t):
    ai = a - 2 * t
    return dict(name=f"Vierkant {a}x{a}x{t}", A=a * a - ai * ai, I=(a**4 - ai**4) / 12, inner=ai, outer=a)

def chi(lam, alpha):
    phi = 0.5 * (1 + alpha * (lam - 0.2) + lam**2)
    return min(1.0, 1 / (phi + math.sqrt(phi**2 - lam**2)))

def buckling(sec, L, alpha=0.49):
    ncr = math.pi**2 * E * sec["I"] / L**2
    lam = math.sqrt(sec["A"] * FY / ncr)
    return ncr / 1000, chi(lam, alpha) * sec["A"] * FY / GM1 / 1000, lam

def nose_retract(inner_r, outer_r):
    """Oeffnungswinkel (halber Scherenwinkel), bei dem die Nasenspitze innen liegt; Rueckkante muss dann noch passen."""
    tip = outer_r + P["nose_out"]                       # Nasenspitze im eingerasteten Zustand (Abstand Rohrachse)
    shift = tip - inner_r + 1.0                         # 1 mm Luft
    half = math.degrees(math.asin(shift / P["b_pivot_to_nose"]))
    back = P["link_w"] / 2 + shift                      # Rueckkante der Lasche wandert zur anderen Wand
    return half, back, tip

def main():
    out = []
    pr = lambda s="": (print(s), out.append(s))
    pr("== Neigung und Rohrlaenge")
    lens = {}
    for s in "AB":
        e = tube_end_offset(TILT[s]); lens[s] = L_NODE[s] - 2 * e
        pr(f"{s}: Neigung {TILT[s]:.2f} Grad, Knotenmitte->Rohrende {e:.1f} mm, Rohr {lens[s]:.0f} mm")
    pr(f"A+B+3 mm Saege = {lens['A'] + lens['B'] + 3:.0f} mm (passt in 7-m-Stange: {lens['A'] + lens['B'] + 3 <= 7000})")
    pr()
    pr("== Profile (Euler K=1 und chi*A*fy Kurve c, Laenge = Rohr B)")
    secs = [square_tube(30, 2), square_tube(30, 3), square_tube(40, 3), round_tube(33.7, 2.6), round_tube(42.4, 2.6), round_tube(48.3, 3.2)]
    for sc in secs:
        ncrA, nbA, _ = buckling(sc, lens["A"]); ncr, nb, lam = buckling(sc, lens["B"])
        kg = sc["A"] * 7.85e-3
        pr(f"{sc['name']:<18} A {sc['A']:6.0f} mm2  I {sc['I']:8.0f} mm4  {kg:4.2f} kg/m  innen {sc['inner']:.1f}  "
           f"Euler A/B {ncrA:5.1f}/{ncr:5.1f} kN  Nb,Rd A/B {nbA:5.1f}/{nb:5.1f} kN  lam_B {lam:.2f}")
        sc.update(ncrB=ncr, nbB=nb, kg=kg)
    pr()
    pr("== Nasen: Einrasten und Ausfahren (Rohr 42,4 x 2,6 und 40 x 40 x 3)")
    for nm, ri, ro in (("Rund 42,4x2,6", 18.6, 21.2), ("Vierkant 40x3", 17.0, 20.0), ("Vierkant 30x3", 12.0, 15.0)):
        half, back, tip = nose_retract(ri, ro)
        ok = back <= ri - 0.5
        pr(f"{nm}: Nasenspitze {tip:.1f} mm von Achse, halber Scherenwinkel zum Einziehen {half:.1f} Grad, Rueckkante dann {back:.1f} <= {ri - 0.5:.1f}: {ok}")
    pr()
    pr("== Kraftweg Schere (je Strebenende, Lasche 20 x 5, Nase 10 breit, Rohrwand 2,6)")
    t, nw = P["link_t"], P["nose_w"]
    v_nose = 2 * nw * t * FY / math.sqrt(3) / GM0 / 1000            # 2 Nasen, Abscheren (EN 1993-1-1 6.2.6)
    fb_wall = 2 * 2.5 * FU * t * 2.6 / GM2 / 1000                   # Lochleibung Rohrwand an 2 Nasen, Kontaktbreite = Laschendicke (Bolzenformel sinngemaess)
    v_bolt = 22.3                                                     # M10 8.8 je Scherflaeche (R34, EN 1993-1-8 Tab. 3.4)
    a_link = 2 * P["link_w"] * t; npl_link = a_link * FY / 1000
    e_kink = abs(-P["bend_r"] * math.tan(math.radians(TILT["B"])) + P["bolt_circle_r"] * math.tan(math.radians(TILT["B"])))
    w_links = 2 * P["link_w"] * t**2 / 6
    pr(f"Nasen abscheren 2 x {nw} x {t}: {v_nose:.1f} kN")
    pr(f"Lochleibung Rohrwand an 2 Nasen: {fb_wall:.1f} kN")
    pr(f"Plattenschraube M10 8.8 einschnittig: {v_bolt:.1f} kN; Drehpunktschraube nur Montage")
    pr(f"Laschenpaar plastisch: {npl_link:.1f} kN")
    pr(f"Knick-Exzentrizitaet an der Plattenschraube (B): {e_kink:.1f} mm -> Biegespannung je kN Strebenkraft {1000 * e_kink / w_links:.0f} N/mm2 (2 Laschen 20 x 5 flach)")
    f_kink = FY * w_links / e_kink / 1000
    pr(f"  -> Strebenkraft bis Fliessen am Knick ohne Plattenstuetzung: {f_kink:.1f} kN (Engpass; Platte stuetzt nur einseitig)")
    pr()
    # Masse je Knoten (6-wertig) und Teile
    m_plate = (math.pi / 4 * (P["plate_d"]**2 - P["center_hole"]**2 - 6 * 11**2)) * P["plate_t"] * 7.85e-6
    l_link = P["a_plate_to_pivot"] + P["b_pivot_to_nose"] + 2 * 15
    m_link = l_link * P["link_w"] * t * 7.85e-6
    pr(f"== Masse: Platte {m_plate:.2f} kg, Lasche {m_link:.3f} kg; 6-wertiger Knoten ohne Schrauben {m_plate + 12 * m_link:.2f} kg; 26 Knoten (130 Enden) {26 * m_plate + 260 * m_link:.1f} kg")
    # Selbsttest
    fails = 0
    def check(label, cond):
        nonlocal fails
        print(("PASS " if cond else "FAIL ") + label); fails += 0 if cond else 1
    check("Neigung B = 18,0 +-0,1", abs(TILT["B"] - 18.0) < 0.1)
    check("Neigung A = 15,9 +-0,1", abs(TILT["A"] - 15.86) < 0.1)
    check("I Rund 42,4x2,6 = 6,46 cm4 (Tabellenwert EN 10255) +-1 %", abs(round_tube(42.4, 2.6)["I"] - 64600) < 650)
    check("I Vierkant 30x3 scharfkantig = (30^4-24^4)/12 = 39 852", abs(square_tube(30, 3)["I"] - 39852) < 1)
    check("Vierkant 30x3 laesst die Schere 20 x 5 NICHT einziehen (Innenmass 24)", not (nose_retract(12.0, 15.0)[1] <= 11.5))
    check("chi(0)=1", chi(0.1, 0.49) == 1.0)
    return 1 if fails else 0

if __name__ == "__main__":
    sys.exit(main())
