"""R51: Beet-Siphon und Siphon-Schutz. Reine Rechnung, liest nichts ausser den Konstanten unten
(aus docs/parts/ibc_beet.md und scripts/workshop/ibc_beet.py; gen_dome.py, data/* bleiben unberuehrt).
Aufruf: python -X utf8 scripts/r51_rechnung.py
"""
import math
import sys

sys.path.insert(0, __file__.rsplit("scripts", 1)[0] + "scripts")

G, NU, K_RAU = 9.81, 1.0e-6, 0.0015e-3     # wie r45_beetablauf.py


def lam(re, di):
    return 64 / re if re < 2300 else 0.25 / math.log10(K_RAU / (3.7 * di) + 5.74 / re**0.9) ** 2


def siphon_q(di, h, l_rohr=0.6, k_ein=0.5):
    """Voll laufendes Standrohr (R45): h = (k_ein + lam*l/d + 1) v2/2g."""
    v = 1.0
    for _ in range(60):
        v = math.sqrt(2 * G * h / (k_ein + 1.0 + lam(v * di / NU, di) * l_rohr / di))
    return v * math.pi * di**2 / 4 * 60000


# --- Bauteil-Parameter (ibc_beet.md) -----------------------------------------------------------
P = dict(wall=4, floor_t=5, rim_w=20, rim_gap=75, media_depth=300, grid_t=8, post=60,
         standpipe_d=25, standpipe_over=265, bell_d=75, bell_wall=3, bell_h=295, bell_slot_w=10,
         bell_slot_h=40, bell_slot_z=15, air_hole=10, guard_d=110, guard_h=320, guard_wall=3,
         guard_hole=12, bulkhead_d=36)
TYPEN = {"aussen_933": (2953, 933, 637), "aussen_800": (2640, 800, 637), "innen_933": (1865, 933, 649)}
POR = 0.40   # Porositaet [A] wie ibc_beet.md

print("== 1. Beetgeometrie (Rechteck, Ecken vernachlaessigt; Kloetze/Rundungen < 3 %) ==")
geo = {}
for n, (L, W, H) in TYPEN.items():
    Li, Wi = L - 2 * P["rim_w"] - 2 * P["wall"], W - 2 * P["rim_w"] - 2 * P["wall"]
    z_ms = H - P["rim_gap"]
    z_m0 = z_ms - P["media_depth"]
    z_g0 = z_m0 - P["grid_t"]
    a = Li * Wi / 1e6
    wasserraum = a * (z_g0 - P["floor_t"]) / 1000 * 1000
    z_top = z_m0 + P["standpipe_over"]
    # Entleerung: von Standrohrkante (z_top) bis Luftloch/Schlitz-Unterkante (z_m0 + slot_z)
    z_break = z_m0 + P["bell_slot_z"]
    pore = a * (z_top - z_break) / 1000 * 1000 * POR
    geo[n] = dict(a=a, wasserraum=wasserraum, pore=pore, z_m0=z_m0, z_top=z_top, z_g0=z_g0)
    print(f"{n}: Li {Li} x Wi {Wi}, Flaeche {a:.2f} m2, z_m0 {z_m0}, Standrohr-OK {z_top} (lokal), "
          f"Wasserraum unter Sieb {wasserraum:.0f} l, Ablaufvolumen Standrohr-OK bis Schlitz-UK {pore:.0f} l")

print("\n== 2. Fluten und Entleeren (Ablaufvolumen aussen_933, R45: 234 l) ==")
V = 234.0
for qin in (3.3, 5.0, 7.8, 8.3):
    print(f"Zulauf {qin:4.1f} l/min -> Flutzeit {V/qin:5.1f} min (Zyklen/h bei Ablauf 5 min: {60/(V/qin+5):.2f})")
d25 = 22.0 / 1000
for h in (0.30, 0.45, 0.60):
    q = siphon_q(d25, h)
    print(f"d25 (ID 22,0) h {h:.2f} m: Siphon {q:4.1f} l/min -> Ablauf {V/q:4.1f} min; "
          f"Faktor gegen Zulauf 8,3: {q/8.3:4.1f}, gegen 3,3: {q/3.3:4.1f}")

print("\n== 3. Standard-Standrohre (Innen-Ø): was ein Zukaufsiphon durchlaesst (gleiches Rechenmodell, [E]) ==")
std = {"PVC-U d20 (ID 17,0)": 17.0, "d25 x1,5 (ID 22,0)": 22.0, "US 3/4 Sch40 (ID 20,9)": 20.9,
       "US 1 Sch40 (ID 26,6)": 26.6, "d32 x1,6 (ID 28,8)": 28.8}
for k, d in std.items():
    print(f"{k:24s}: h 0,30 {siphon_q(d/1000,0.30):5.1f}  h 0,45 {siphon_q(d/1000,0.45):5.1f}  h 0,60 {siphon_q(d/1000,0.60):5.1f} l/min")

print("\n== 4. Bell-Fluchtquerschnitte (heutiges Bauteil) ==")
a_sp = math.pi / 4 * 22.0**2
bell_id = P["bell_d"] - 2 * P["bell_wall"]
a_ring = math.pi / 4 * (bell_id**2 - P["standpipe_d"]**2)
a_slots = 2 * P["bell_slot_w"] * P["bell_slot_h"]
a_guard_ist = 12 * P["guard_hole"]**2
gap = (P["guard_d"] - 2 * P["guard_wall"] - P["bell_d"]) / 2
print(f"Standrohr-Fliessflaeche {a_sp:.0f} mm2; Ringraum Standrohr/Glocke {a_ring:.0f} mm2 ({a_ring/a_sp:.1f}x); "
      f"Glockenschlitze {a_slots} mm2 ({a_slots/a_sp:.1f}x); Luftloch {P['air_hole']**2} mm2")
print(f"Medienschutz heute: 12 Durchbrueche 12x12 = {a_guard_ist} mm2 ({a_guard_ist/a_sp:.1f}x Standrohr); "
      f"Ringspalt Glocke/Schutz {gap:.1f} mm; Schutz/Glocke Durchmesserverhaeltnis {P['guard_d']/P['bell_d']:.2f} (UH BIO-10: ca. 2)")
ringe_unten = 4 * P["guard_hole"]**2
print(f"  davon im letzten Ablaufabschnitt (Ring z 40, 4 Loecher): {ringe_unten} mm2 = {ringe_unten/a_sp:.1f}x Standrohr; "
      f"Anstroemgeschwindigkeit bei 50 l/min: {50/60000/(ringe_unten/1e6):.2f} m/s")

print("\n== 5. Schutz-Varianten: Lochgroesse gegen Korn, Oeffnungsflaeche ==")
for korn_min, korn_name in ((8, "Blaehton 8-16 (Handelsware)"), (12, "Korn ab 12 (W40-Vorgabe)")):
    print(f"{korn_name}: Oeffnung <= {0.75*korn_min:.0f} mm (0,75 x Kleinstkorn), empfohlen {korn_min-2} mm; Rundloch")
def schutz(loch, teilung, zeilen, d=P["guard_d"]):
    n_um = int(math.pi * d / teilung)
    n = n_um * zeilen
    a = n * math.pi / 4 * loch**2
    return n, a
for loch, teil, zeilen in ((6, 12, 6), (8, 14, 6), (8, 14, 10)):
    n, a = schutz(loch, teil, zeilen)
    print(f"Rundloch {loch} mm, Teilung {teil} mm, {zeilen} Zeilen (untere {zeilen*teil} mm): {n} Loecher, {a:.0f} mm2 = {a/a_sp:.1f}x Standrohr")
# Schlitzvariante: 6 mm breit, 60 mm lang, 24 Schlitze am Umfang, 1 Reihe
print(f"Schlitz 6 x 60 mm, 20 am Umfang: {20*6*60} mm2 = {20*6*60/a_sp:.1f}x Standrohr (Bohr-/Saegeaufwand 20 Schlitze statt ~100 Loecher)")

print("\n== 6. Wasserraum unter dem Siebboden: bleibt gefuellt (Glocke steht auf dem Sieb) und Entleerung nach Ziehen des Standrohrs ==")
SUM = {"aussen_933": 5, "aussen_993": 3, "innen_933": 6}
w993 = 2953 - 40 - 8, 993 - 40 - 8
print("Summe stehendes Wasser alter Stand (5 x aussen_933 640 l + 3 x aussen_993 684 l + 6 x innen 420 l):", 5 * 640 + 3 * 684 + 6 * 420, "l")
print("Summe Zielstand (8 x aussen_800 485 l + 6 x innen 420 l):", 8 * 485 + 6 * 420, "l")
CD = 0.6
for n in ("aussen_800", "aussen_933", "innen_933"):
    g = geo[n]
    h0 = (g["z_g0"] - P["floor_t"]) / 1000 + 0.02
    a_loch = math.pi / 4 * 0.036**2
    t = 2 * g["a"] / (CD * a_loch * math.sqrt(2 * G)) * math.sqrt(h0)
    print(f"{n}: Wasserraum {g['wasserraum']:.0f} l; bei gezogenem Standrohr (Loch D36, Cd {CD}, fallender Spiegel, Anfangshoehe {h0*1000:.0f} mm) leer in {t/60:.0f} min [E]")

print("\n== 7. Gewichte der empfohlenen Teile (Dichte PVC-U 1,4; V2A 7,9; Loecher abgezogen) ==")
def rohr(d, w, l, rho=1.4):
    return math.pi / 4 * (d**2 - (d - 2 * w)**2) * l / 1000 * rho / 1000
print(f"Standrohr d25 x 2 x 557 mm (Modell): {rohr(25,2,557):.2f} kg")
print(f"Glocke d75 x 3 x 295 + Deckel: {rohr(75,3,295)+math.pi/4*75**2*3/1000*1.4/1000:.2f} kg")
print(f"Medienschutz PVC-U d110 x 3 x 320 (12 Durchbrueche): {rohr(110,3,320):.2f} kg; mit 168 Loechern d6 etwa {rohr(110,3,320)-168*math.pi/4*6**2*3/1e6*1.4:.2f} kg")
umf = math.pi * 110 + 20
lb = umf * 340 * 1.5 / 1000 * (1 - 0.35) * 7.9 / 1000
print(f"Medienschutz V2A-Lochblech 1,5 mm RV 5-8 (Lochanteil 35 %), Zuschnitt {umf:.0f} x 340 mm: {lb:.2f} kg; "
      f"Zuschnitte je Tafel 1000 x 2000: {int(1000//umf)*int(2000//340)}")
print(f"Reinigungsschacht PVC-U d110 x 3 x 562 + Kappe: {rohr(110,3,562)+0.15:.2f} kg")
print(f"Lochanteil RV 5-8 (versetzt 60 Grad): {math.pi/(2*math.sqrt(3))*(5/8)**2*100:.0f} %; offene Flaeche 346 x 140 mm unten: {346*140*math.pi/(2*math.sqrt(3))*(5/8)**2:.0f} mm2 = {346*140*math.pi/(2*math.sqrt(3))*(5/8)**2/a_sp:.0f}x Standrohr")
