"""R50: Rechnungen zu Fein- und Vortexfilter (nur Zahlen, kein Modellzugriff).

Aufruf: python -X utf8 scripts/r50_rechnung.py
Herkunft: E = eigene Rechnung, A = Annahme; Eingaben stehen oben und in docs/research/R50-fein-und-vortexfilter.md.
"""
from math import pi

Q_MAIN = 110.0   # l/min Hauptstrom je Linie (Netzliste, D55)
Q_SIDE = 12.5    # l/min Teilstrom Bodenablauf je Linie (K03)
m3h = lambda lmin: lmin * 60 / 1000


def area_circle(d_m):
    return pi / 4 * d_m ** 2


print("== 1 Feinfilter ==")
print(f"Hauptstrom {Q_MAIN} l/min = {m3h(Q_MAIN):.2f} m3/h = {Q_MAIN/60:.2f} l/s")
korb = 0.840
print(f"Eigenbau Siebkorb {korb} m2 -> Belastung {m3h(Q_MAIN)/korb:.2f} m/h")

# Trommelfilter: Mantelflaeche, Nennleistung gegen unseren Bedarf
drum = pi * 0.38 * 0.40
print(f"ENTRY 25: Trommel 0,38 x 0,40 m = {drum:.3f} m2 Mantel; 25 m3/h -> {25/drum:.0f} m/h; "
      f"unser Bedarf {m3h(Q_MAIN):.1f} m3/h = {m3h(Q_MAIN)/25*100:.0f} % der Nennleistung; "
      f"{m3h(Q_MAIN)/drum:.1f} m/h auf Gesamtmantel")
fiap = 28.61 * 3.6
print(f"FIAP 80.000 bei 100 um: {fiap:.0f} m3/h = {fiap/m3h(Q_MAIN):.1f}-fach unser Bedarf")
print(f"AquaForte ATF-1 25 m3/h = {25/m3h(Q_MAIN):.1f}-fach, Entry 25 {25/m3h(Q_MAIN):.1f}-fach")

# Beutelfilter Groesse 2: Beutelflaeche A (Annahme), Nennleistung 80 gpm (Zoro-Listung, 100 um)
bag_area = 0.5
bag_rate = 80 * 3.785 * 60 / 1000
print(f"Beutel Gr. 2 (A=0,5 m2 [A]): Belastung {m3h(Q_MAIN)/bag_area:.1f} m/h; Nennleistung 80 gpm = "
      f"{bag_rate:.1f} m3/h -> {m3h(Q_MAIN)/bag_rate*100:.0f} % der Nennleistung")

# Druckverlust sauberes Gewebe (laminar, Kapillarmodell) 100 um, offene Flaeche 35 % [A], Dicke 0,15 mm [A]
mu, rho, g = 1.0e-3, 998, 9.81
for load_mh, label in ((m3h(Q_MAIN)/korb, "Siebkorb"),):
    v_anf = load_mh / 3600
    v_open = v_anf / 0.35
    dp = 32 * mu * v_open * 0.15e-3 / (100e-6) ** 2
    print(f"sauberes Gewebe {label}: v_anf {v_anf*1000:.2f} mm/s, v_Oeffnung {v_open*1000:.2f} mm/s, "
          f"dp {dp:.2f} Pa = {dp/rho/g*1000:.2f} mm Wassersaeule (nur Gewebe, ohne Filterkuchen)")

# Heber-Reserve und Bedarf der Bauarten
print("Heber-Reserve 85 mm (R47/R48). Entry 25 verlangt 160 mm Ueberstand (Datenblatt) -> Fehlbetrag 75 mm")
loss = 195.0
for d in (75, 90, 110):
    f = (75 / d) ** 4.87
    f2 = (75 / d) ** 4.0
    print(f"  Heber d{d}: Verlust 195 mm * {f:.2f} (reine Reibung, d^-4,87) = {loss*f:.0f} mm, "
          f"bei d^-4 = {loss*f2:.0f} mm -> Reserve {85+loss-loss*f:.0f} bis {85+loss-loss*f2:.0f} mm [E, Annahme]")

# Schlammfracht
feed_total = 3.46  # kg/Tag beide Linien (R45)
for k in (0.15, 0.30):
    ts_line = feed_total / 2 * k
    print(f"TS je Linie bei {k} kg/kg Futter: {ts_line*1000:.0f} g/Tag; nach Absetzer (77 %): {ts_line*0.77*1000:.0f} g/Tag")
fracht = 130.0
for cap, label in ((0.21, "100 um (Mortensen 21 %)"), (0.48, "60 um (48 %)"), (0.99, "30 um (99 %)")):
    g_d = fracht * cap
    print(f"Fracht {fracht:.0f} g/Tag * {cap:.2f} ({label}) = {g_d:.0f} g/Tag = {g_d*7:.0f} g/Woche; "
          f"Kuchen bei 50 g/l [A] = {g_d*7/50:.1f} l/Woche = {g_d*7/50/1000/korb*1000:.1f} mm auf {korb} m2")
print(f"Spuelwasser nach Mortensen 200/100/50 l je kg Futter: je Linie (1,73 kg/Tag) "
      f"{1.73*200:.0f} / {1.73*100:.0f} / {1.73*50:.0f} l/Tag bei 30/60/100 um")

print("\n== 2 Vortex/Absetzer ==")
qs = m3h(Q_SIDE)
print(f"Teilstrom {Q_SIDE} l/min = {qs:.2f} m3/h; Vollstrom {m3h(Q_MAIN):.2f} m3/h")
print(f"Fuer Davidson-Beschickung 11,2 m/h im Vollstrom: {m3h(Q_MAIN)/11.2:.2f} m2 Beckenflaeche; "
      f"Teilstrom: {qs/11.2:.3f} m2")
cands = [
    ("heute Tank_klein (Leitrohr abgezogen) 0,346 m2", 0.346, 267),
    ("Aquaforte Turbo Vortex, D 350", area_circle(0.35), None),
    ("AquaLogistik Center-Vortex C20, Vortex D 450", area_circle(0.45), None),
    ("AquaLogistik C50, Vortex D 750", area_circle(0.75), None),
    ("Tripond/AquaLogistik Vortex 65, D 650", area_circle(0.65), None),
    ("PP Vortex 950, D 950", area_circle(0.95), None),
    ("PP Vortex 1250, D 1250", area_circle(1.25), None),
    ("Cone-Bottom PE 100 gal (D 23 in = 584 mm, 378 l)", area_circle(0.584), 378.5),
    ("Norwesco 125 gal (D 48 in = 1219 mm, 473 l)", area_circle(1.219), 473.2),
    ("Aquaponics Swirl GFK 750 l (Fl. aus 1,45 m D, A)", area_circle(1.45), 750),
]
for name, a, vol in cands:
    t = f", Verweilzeit {vol/Q_SIDE:.0f} min" if vol else ""
    print(f"{name}: A {a:.3f} m2, Beschickung Teilstrom {qs/a:.2f} m/h = {qs/a/3.6:.2f} mm/s{t}")
print("Eintrittsgeschwindigkeit Teilstrom: d50 (Innen 44 mm) / d110 (Innen 104 mm [A]) / d63 (Innen 57 mm)")
for name, di in (("d50 Innen 44", 0.044), ("d110 Innen 104", 0.104), ("d63 Innen 57", 0.057)):
    print(f"  {name} mm: {Q_SIDE/60/1000/area_circle(di):.3f} m/s bei {Q_SIDE} l/min; {Q_MAIN/60/1000/area_circle(di):.2f} m/s bei {Q_MAIN} l/min")
# Mindestdurchfluss PP Vortex 10 m3/h gegen Teilstrom
print(f"PP Vortex Mindestdurchfluss 10 m3/h = {10/qs:.0f}-fach Teilstrom; C20 Pumpenleistung 4 m3/h = {4/qs:.1f}-fach")
# Schlammvolumen
for v in (11, 14):
    print(f"Schlamm {v} l/Tag je Linie -> {v*7} l/Woche")
