"""R45 Frage 3: Beet-Sumpf je Linie. Pumpenarbeitspunkt, Sumpfvolumen aus Ablaufspitzen, Schalthaeufigkeit, Leistung.

Aufruf: python -X utf8 scripts/r45_sumpf.py   (reine Rechnung)
Pumpe (Beispiel, Standardprodukt): Teichpumpe 5300 l/h bei 0 m, Hmax 2,8 m, 60 W (Haendlerangaben OASE AquaMax Eco Classic 5500) [A: Kennlinie parabolisch angenommen]
"""
import math

G, NU = 9.81, 1.0e-6
Q0, H0, P_EL = 5300 / 60.0, 2.8, 60.0   # l/min bei 0 m, m, W
DI40 = 0.0362                            # PVC-U d40 x 1,9
BEETE, ZYKLEN_H, BEET_L = 7, 2, 234.0
ABLAUF_MIN, ABLAUF_Q = 5.0, 47.0         # R45 Frage 1: 47 l/min, 234 l in ca. 5 min


def lam(re):
    return 0.25 / math.log10(0.0015e-3 / (3.7 * DI40) + 5.74 / re ** 0.9) ** 2


def arbeitspunkt(h_stat, l_rohr=4.0, k_summe=2.0):
    """Schnittpunkt Pumpenkennlinie H = H0 (1 - (Q/Q0)^2) mit Anlage h_stat + (lam L/d + k) v2/2g."""
    q = 40.0
    for _ in range(80):
        a = math.pi * DI40**2 / 4
        v = q / 60000 / a
        h_an = h_stat + (lam(v * DI40 / NU) * l_rohr / DI40 + k_summe) * v * v / (2 * G)
        q = Q0 * math.sqrt(max(0.0, 1 - h_an / H0))
    v = q / 60000 / (math.pi * DI40**2 / 4)
    h_an = h_stat + (lam(v * DI40 / NU) * l_rohr / DI40 + k_summe) * v * v / (2 * G)
    return q, h_an, v


print("== Arbeitspunkt Beet-Sumpf-Pumpe (Foerderleitung d40, 4 m, 2 Boegen + Rueckschlagventil k_summe 2,0 [A]) ==")
for h_stat in (1.0, 1.25, 1.5):
    q, h, v = arbeitspunkt(h_stat)
    hyd = 1000 * G * q / 60000 * h
    print(f"statisch {h_stat:.2f} m: Q {q:5.1f} l/min  H gesamt {h:.2f} m  v {v:.2f} m/s  hydraulisch {hyd:4.1f} W  Wirkungsgrad {hyd/P_EL:.0%}")

q_p = arbeitspunkt(1.25)[0]
mittel = BEETE * BEET_L * ZYKLEN_H / 60.0
print(f"\nMittlerer Zulauf je Linie: {mittel:.1f} l/min; Pumpenlaufanteil {mittel/q_p:.0%}; Mittelleistung {P_EL*mittel/q_p:.0f} W je Linie, {2*P_EL*mittel/q_p:.0f} W beide, {2*P_EL*mittel/q_p*24/1000:.1f} kWh/Tag")


def simuliere(gruppe, start_versatz_min, dauer_h=1.0, q_pumpe=q_p, pumpe_aus=False, dt=0.05):
    """Je start_versatz_min Minuten laufen `gruppe` Beete gleichzeitig ab (je ABLAUF_MIN lang mit ABLAUF_Q); Sumpf-Fuellstand ueber der Pumpen-AUS-Marke."""
    starts = []
    t = 0.0
    while t < dauer_h * 60:
        starts.extend([t] * gruppe)
        t += start_versatz_min
    vol = vmax = 0.0
    maxn = 0
    t = 0.0
    while t < dauer_h * 60 + 10:
        n = sum(1 for s in starts if s <= t < s + ABLAUF_MIN)
        maxn = max(maxn, n)
        zu = n * ABLAUF_Q
        ab = 0.0 if pumpe_aus else (q_pumpe if vol > 0 or zu > q_pumpe else zu)
        vol = max(0.0, vol + (zu - ab) * dt)
        vmax = max(vmax, vol)
        t += dt
    return vmax, maxn


print("\n== Spitzenfuellstand ueber der Pumpen-AUS-Marke (l), immer 14 Ablaeufe je Stunde ==")
basis = 60 / (BEETE * ZYKLEN_H)
for gruppe in (1, 2, 3):
    vmax, n = simuliere(gruppe, basis * gruppe)
    print(f"{gruppe} Beet(e) gleichzeitig, alle {basis*gruppe:4.1f} min: max {n} gleichzeitig, Spitze {vmax:5.0f} l")
vmax, _ = simuliere(1, 4.3, pumpe_aus=True, dauer_h=0.2)
print(f"Pumpenausfall, gestaffelt: nach 12 min {vmax:.0f} l im Sumpf (= {vmax/BEET_L:.1f} Beete)")
print(f"Alle 7 Beete gleichzeitig (Steuerungsfehler): {BEETE*BEET_L:.0f} l Zulauf in {ABLAUF_MIN:.0f} min, minus Pumpe {q_p*ABLAUF_MIN:.0f} l = {BEETE*BEET_L - q_p*ABLAUF_MIN:.0f} l")

print("\n== Schaltspiel Schwimmerschalter (Pumpe laeuft, wenn Pegel >= EIN, bis AUS) ==")
for band in (50, 100, 150):
    t_aus = band / mittel
    t_ein = band / max(q_p - mittel, 0.1)
    print(f"Hysterese {band:3d} l: Pumpe aus {t_aus:4.1f} min, an {t_ein:4.1f} min -> {60/(t_aus+t_ein):4.1f} Starts/h")
print("Zum Vergleich Behaelter Ø 0,8 m: 1 cm Pegel = 5,0 l, 100 l = 200 mm")
