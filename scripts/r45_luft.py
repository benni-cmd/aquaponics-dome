"""R45 Frage 4: Luftbedarf Pool (F4), Gebläsedruck und -leistung, Zeit bis Sauerstoffmangel bei Ausfall.

Aufruf: python -X utf8 scripts/r45_luft.py   (reine Rechnung; Eingaben aus data/system-specs.json und data/leitungsnetz.json laut Abschnitt 4)

AOTE = SOTE(Tiefe) x alpha x (beta Cs,T - C)/Cs,20 x theta^(T-20)   (Abwassertechnik-Standard, Quellen im Abschnitt 4)
"""
import math

G = 9.81
O2_LUFT_G_L = 0.27          # g O2 je Liter Luft bei ca. 28 C (23,2 Masse-% x 1,16 kg/m3)
CS20, CS28 = 9.09, 7.83     # mg/l Saettigung 20 C / 28 C (Standard Methods, Tabelle; [A] nicht neu gelesen)
BETA, THETA = 0.95, 1.024
C_BETRIEB = 5.0             # mg/l Sollwert im Pool [A]
TIEFE_POOL = 2.17           # m Ausstroemer ueber Boden 50 mm: Spiegel Z 515 - (-1705 + 50)
SOTE_JE_M = (0.06, 0.075)   # 6-7,5 %/m Reinwasser, feinblasig, Vollbelegung (wastewater.com); 6 %/m Default (aquakin)
ALPHA = (0.49, 0.8)         # Fein-Blasen alpha 0,49 (Tabelle wastewater.com) bis 0,8 [A, gereinigte Membranen]

O2_FISCH = (0.7, 1.1, 1.6)  # kg/Tag, system-specs
O2_NITRI = 0.6              # kg/Tag
O2_GESAMT = (1.3, 1.7, 2.2)
SPITZE = 1.5
VOL_M3 = 28.5               # Fischwasser

kor = (BETA * CS28 - C_BETRIEB) / CS20 * THETA ** 8
print(f"Korrektur DO/Temperatur: (0,95 x {CS28} - {C_BETRIEB}) / {CS20} x 1,024^8 = {kor:.2f}")


def luft_l_min(o2_kg_tag, sote, alpha):
    aote = sote * alpha * kor
    return o2_kg_tag * 1000 / (O2_LUFT_G_L * aote) / 1440, aote


print(f"\n== Luftbedarf Pool, Ausstroemertiefe {TIEFE_POOL:.2f} m ==")
print("Spalten: O2-Bedarf kg/Tag -> l/min bei (SOTE/m, alpha) = (6 %, 0,49) .. (7,5 %, 0,8); in Klammern AOTE")
for name, vals in (("nur Fisch", O2_FISCH), ("Fisch + Nitrifikation", O2_GESAMT)):
    for v in vals:
        q_hi, a_lo = luft_l_min(v, SOTE_JE_M[0] * TIEFE_POOL, ALPHA[0])
        q_lo, a_hi = luft_l_min(v, SOTE_JE_M[1] * TIEFE_POOL, ALPHA[1])
        print(f"{name:22s} {v:4.1f} kg/Tag: {q_lo:4.0f} .. {q_hi:4.0f} l/min  (AOTE {a_lo:.1%} .. {a_hi:.1%});  Spitze x1,5: {q_lo*SPITZE:4.0f} .. {q_hi*SPITZE:4.0f}")

print("\n== Gegenprobe zur 25-63 l/min-Rechnung der Netzliste (OTE 13 % ohne Korrektur) ==")
for v in (1.3, 2.2):
    print(f"{v} kg/Tag mit AOTE = SOTE 13 %: {v*1000/(O2_LUFT_G_L*0.13)/1440:.0f} l/min (wird um den Faktor {1/(0.13*0.0+kor*0.49):.1f}..{1/(kor*0.8):.1f} zu klein, weil SOTE Reinwasser/20 C/0 mg/l O2 gilt)")

print("\n== Gebläsedruck und Leistung ==")
druck_pool = 1000 * G * TIEFE_POOL / 1000   # kPa
for verl in (3.0, 5.0):
    p = druck_pool + verl
    print(f"Pool: statisch {druck_pool:.1f} kPa + Diffusor/Leitung {verl:.0f} kPa = {p:.1f} kPa")
for q in (130, 200, 260):
    for p in (25.0, 28.0):
        p_abs = 101.325 + p
        pad = 3.5 * 101325 * q / 60000 * ((p_abs / 101.325) ** (1 / 3.5) - 1)
        print(f"{q} l/min bei {p:.0f} kPa: adiabat {pad:5.0f} W, elektrisch bei Wirkungsgrad 40-50 %: {pad/0.5:4.0f}-{pad/0.4:4.0f} W")
print("Vergleich Katalog (Haendlerangaben): HIBLOW HP-200 200 l/min bei 20 kPa, 250 W; HP-120LL 120 l/min bei 17,7 kPa (max. 30 kPa), 100 W")

print("\n== Zeit bis Sauerstoffmangel bei Gebläseausfall (nur Verbrauch, ohne Wiederbelüftung durch Kaskaden) ==")
for c0, c1 in ((6.0, 3.0), (5.0, 3.0)):
    vorrat_g = (c0 - c1) * VOL_M3
    for o2 in (1.7, 1.7 * SPITZE):
        print(f"{c0:.0f} -> {c1:.0f} mg/l, Verbrauch {o2:.2f} kg/Tag = {o2*1000/24:.0f} g/h: {vorrat_g/(o2*1000/24):.1f} h")
