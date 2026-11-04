"""W40-BEET 1a: Rechnung fuer Variante V3 (Sperrboden, Kerben-Glocke). Reine Rechnung, liest nichts ausser den Konstanten unten
(Quellen: data/components/ibc_beet.json, docs/jobs/W40-BEET.md, scripts/r51_rechnung.py; gen_dome.py und data/* bleiben unberuehrt).
Aufruf: python -X utf8 scripts/w40_beet_rechnung.py
Ausgabe: Restwasser (Film), Ablaufvolumen, Entleerzeit d25, Flutzeit, Vergleich V0 (heute) gegen V3, Summe Systemvolumen."""
import math

G, NU, K_RAU = 9.81, 1.0e-6, 0.0015e-3     # wie r45_beetablauf.py / r51_rechnung.py


def lam(re, di):
    return 64 / re if re < 2300 else 0.25 / math.log10(K_RAU / (3.7 * di) + 5.74 / re ** 0.9) ** 2


def siphon_q(di, h, l_rohr=0.6, k_ein=0.5):
    """Voll laufendes Standrohr (R45): h = (k_ein + lam*l/d + 1) v2/2g; Rueckgabe l/min."""
    v = 1.0
    for _ in range(60):
        v = math.sqrt(2 * G * h / (k_ein + 1.0 + lam(v * di / NU, di) * l_rohr / di))
    return v * math.pi * di ** 2 / 4 * 60000


P = dict(wall=4, floor_t=5, rim_w=20, rim_gap=75, media_depth=300, media_gap=2, grid_t=8,
         standpipe_d=25, standpipe_id=22.0, standpipe_over=265, bell_d=75, bell_wall=3,
         bell_slot_h_alt=40, bell_slot_z_alt=15,        # V0 heute (R03)
         kerbe_w=10, kerbe_h=12, kerbe_z=0, kerbe_n=4,   # V3
         guard_d=110)
TYPEN = {"aussen_800": dict(L=2640, W=800, H=637, fase=0, n=8, wasserraum_l=485),
         "innen_933": dict(L=1865, W=933, H=649, fase=120, n=6, wasserraum_l=420),
         "aussen_933": dict(L=2953, W=933, H=637, fase=0, n=5, wasserraum_l=640)}
POR = 0.40            # Porositaet [A] wie ibc_beet.md
R45_V = 234.0         # R45: Ablaufvolumen aussen_933 (feste Annahme)
HEADS = (0.30, 0.45, 0.60)

print("== 1. Geometrie und Restwasser je Typ (Film = Flaeche x Kerbenhoehe x Porositaet) ==")
res = {}
for n, T in TYPEN.items():
    L, W, H = T["L"], T["W"], T["H"]
    Li, Wi = L - 2 * P["rim_w"] - 2 * P["wall"], W - 2 * P["rim_w"] - 2 * P["wall"]
    lm, wm = Li - 2 * P["media_gap"], Wi - 2 * P["media_gap"]       # Kontur Medium und Siebboden
    a_mm2 = lm * wm
    if T["fase"]:                                                      # W26/D44: 45-Grad-Fasen, Medium-Fase c - d x (2 - sqrt 2)
        cm = T["fase"] - (W - wm) / 2.0 * (2 - math.sqrt(2))
        a_mm2 -= 2 * cm * cm
    a = a_mm2 / 1e6
    z_ms = H - P["rim_gap"]
    z_m0 = z_ms - P["media_depth"]
    z_top = z_m0 + P["standpipe_over"]
    film = a * P["kerbe_h"] / 1000 * 1000 * POR                        # l
    v0_zone = (z_top - (z_m0 + P["bell_slot_z_alt"])) / 1000
    v_r45def = a * v0_zone * 1000 * POR                                # bis Schlitz-Unterkante (R45-Definition, V0)
    z_break_v3 = z_m0 + P["kerbe_z"] + P["kerbe_h"]                    # Luft tritt ein, wenn der Spiegel unter die Kerbenoberkante faellt
    v_v3 = a * (z_top - z_break_v3) / 1000 * 1000 * POR
    res[n] = dict(a=a, film=film, v_r45def=v_r45def, v_v3=v_v3, z_m0=z_m0, z_top=z_top, z_break=z_break_v3)
    print(f"{n}: Siebboden-/Medienflaeche {a:.3f} m2, z_m0 {z_m0}, Standrohrkante z {z_top}, Kerben-Oberkante z {z_break_v3:.0f}; "
          f"Film {film:.1f} l (Wasserraum V0 {T['wasserraum_l']} l)")

print("\n== 2. Entleerzeit d25 (ID 22,0; Rechenmodell R45/R51) ==")
q = {h: siphon_q(P["standpipe_id"] / 1000, h) for h in HEADS}
print("Siphon-Leistung: " + ", ".join(f"h {h:.2f} m: {q[h]:.1f} l/min" for h in HEADS))
for n in TYPEN:
    r = res[n]
    for label, v in (("R45-Definition (Standrohrkante bis Schlitz-UK, V0)", r["v_r45def"]), ("V3-Geometrie (Standrohrkante bis Kerben-OK)", r["v_v3"])):
        t = [v / q[h] for h in HEADS]
        print(f"{n}: {label}: {v:.0f} l -> {min(t):.1f} bis {max(t):.1f} min")
print(f"Referenz R45: {R45_V:.0f} l -> {R45_V / q[0.60]:.1f} bis {R45_V / q[0.30]:.1f} min (Sollbereich 4,3 bis 6,1 min)")
r8 = res["aussen_800"]
print(f"ABWEICHUNG: aussen_800 {r8['v_r45def']:.0f} l -> {r8['v_r45def'] / q[0.60]:.1f} bis {r8['v_r45def'] / q[0.30]:.1f} min liegt unter R45 4,3 bis 6,1 min, "
      f"weil das Beet kleiner ist als aussen_933 (R45 rechnet fest {R45_V:.0f} l). aussen_933 mit eigener Flaeche: "
      f"{res['aussen_933']['v_r45def']:.0f} l -> {res['aussen_933']['v_r45def'] / q[0.60]:.1f} bis {res['aussen_933']['v_r45def'] / q[0.30]:.1f} min "
      f"(R45 setzt fest {R45_V:.0f} l an, Herkunft dieser Zahl nicht nachvollzogen). Sollbereich bleibt Massstab, nicht geaendert.")

print("\n== 3. Kerben-Flaeche gegen Standrohr ==")
a_sp = math.pi / 4 * P["standpipe_id"] ** 2
a_k = P["kerbe_n"] * P["kerbe_w"] * P["kerbe_h"]
a_alt = 2 * P["kerbe_w"] * P["bell_slot_h_alt"]
print(f"Standrohr-Fliessflaeche {a_sp:.0f} mm2; V3 {P['kerbe_n']} Kerben {P['kerbe_w']} x {P['kerbe_h']} = {a_k} mm2 ({a_k / a_sp:.2f}x, Soll >= 1); V0 2 Schlitze 10 x 40 = {a_alt} mm2")

print("\n== 4. Fluten (Zulauf 3,3 bis 8,3 l/min je Beet, R45/R51) ==")
for n in ("aussen_800", "innen_933"):
    v = res[n]["v_v3"]
    print(f"{n}: Flutvolumen {v:.0f} l: Flutzeit {v / 8.3:.0f} bis {v / 3.3:.0f} min; Zyklen je Stunde (Ablauf 5 min): {60 / (v / 8.3 + 5):.1f} bis {60 / (v / 3.3 + 5):.1f}")
print("Anspringen bei 3,3 l/min ist nicht gerechnet, nur am Muster pruefbar.")

print("\n== 5. Systemvolumen: stehendes Wasser alt gegen neu (Zielstand 8 x aussen_800 + 6 x innen_933) ==")
alt = 8 * TYPEN["aussen_800"]["wasserraum_l"] + 6 * TYPEN["innen_933"]["wasserraum_l"]
neu = 8 * res["aussen_800"]["film"] + 6 * res["innen_933"]["film"]
print(f"V0: 8 x {TYPEN['aussen_800']['wasserraum_l']} + 6 x {TYPEN['innen_933']['wasserraum_l']} = {alt} l stehendes Wasser unter dem Medium; "
      f"V3: 8 x {res['aussen_800']['film']:.1f} + 6 x {res['innen_933']['film']:.1f} = {neu:.0f} l Film; Differenz {alt - neu:.0f} l")

print("\n== 6. Optionale Nachlaufbohrung d4 im Standrohr (nur wenn der Film am Muster zu gross ist) ==")
for cd in (0.6, 0.3):
    qn = cd * math.pi / 4 * (4e-3) ** 2 * math.sqrt(2 * G * 0.26) * 60000
    print(f"Cd {cd}: {qn:.2f} l/min bei 0,26 m Druckhoehe (Blatt nennt etwa 0,5 l/min: haengt an Cd, am Muster pruefen)")
