"""R35 Arbeitshoehe der NFT-Tische: Ergonomie, Zugang zu den Beeten, Verschattung (nachvollziehbare Rechnung).

Aufruf: python scripts/table_height.py   (nur Standardbibliothek, schreibt auf stdout)
Masse: docs/parts/nft_tisch.md, docs/parts/ibc_beet.md, data/layout.json (Z-Werte in mm, Boden Z 0).
"""
import math

# ---- Annahmen -------------------------------------------------------------------------------------------------------
HEIGHTS = [1550, 1600, 1750, 1900]      # Koerpergroesse mm: P5 Frau (DIN 33402-2 ca. 1,54-1,55 m), Job 1,60 und 1,90, Mitte
ELBOW = 0.63                             # Ellbogenhoehe / Koerperhoehe (docs: Mensch-Modell 1134 bei 1800)
SHOULDER = 0.818                         # Schulterhoehe / Koerperhoehe (Mensch-Modell 1472 bei 1800)
BAND_LIGHT = (-150, -100)                # mm gegen Ellbogen: leichte bis mittlere Arbeit (Ratgeber 10-15 cm unter Ellbogen)
BAND_FINE = (-50, 100)                   # Pflanzen setzen / Kontrolle: um Ellbogen bis etwas darueber
POT_OFFSET = (14, 54)                    # Topfloecher ueber Rinnenunterkante (nft_tisch.md: Z 1314-1354 bei 1300)
CHANNEL_H = 100                          # Rinne 130 x 100
CHANNEL_W = 130
HOLM = 50                                # Holm/Kragarm-Hoehe unter der Rinnenunterkante [A]
BED_RIM = 475                            # Beetrand Z (ibc_beet: Oberkante Z 475, Medium Z 400)
BED_SURFACE = 400
RINGS = {                                # (Rinnen, Abstand mm, Beetbreite mm)
    "aussen (4 Rinnen)": (4, 220, 800),
    "mitte (4 Rinnen)": (4, 263, 933),
    "innen (2 Rinnen, ueber Pool)": (2, 263, None),
}
HEIGHT_CANDIDATES = [840, 1000, 1100, 1200, 1300]


def person_rows(zu):
    rows = []
    for h in HEIGHTS:
        elbow, shoulder = ELBOW * h, SHOULDER * h
        lo, hi = zu + POT_OFFSET[0], zu + POT_OFFSET[1]
        rows.append((h, elbow, shoulder, lo - elbow, hi - elbow, hi - shoulder))
    return rows


def verdict(d_lo, d_hi, d_sh):
    if d_sh >= -100:
        return "ROT (Haende auf Schulterhoehe)"
    if d_lo >= -200 and d_hi <= BAND_FINE[1]:
        return "gruen"
    if d_lo >= -250 and d_hi <= 200:
        return "gelb"
    return "rot"


def ergonomics():
    print("=== 1. Ergonomie: Topfebene (Rinnenunterkante + 14..54) gegen Ellbogen und Schulter ===")
    print("Ellbogen = 0,63 H, Schulter = 0,818 H (Mensch-Modell; DIN 33402-2 alt: Ellbogen Frau P5 960, Mann P95 1175 mm).")
    print("Gruen: Topfebene -200 bis +100 mm gegen Ellbogen; gelb: bis -250 / +200; sonst rot; Schulter erreicht = rot.")
    for zu in HEIGHT_CANDIDATES:
        print(f"\nRinnenunterkante {zu} mm (Topfebene {zu + POT_OFFSET[0]}-{zu + POT_OFFSET[1]}):")
        for h, el, sh, dlo, dhi, dsh in person_rows(zu):
            print(f"  H {h}: Ellbogen {el:5.0f}, Schulter {sh:5.0f} -> Topfebene {dlo:+5.0f}..{dhi:+5.0f} mm gegen Ellbogen, {dsh:+5.0f} mm gegen Schulter  {verdict(dlo, dhi, dsh)}")
    print("\nZielhoehe fuer leichte Arbeit (Topfebene = Ellbogen - 150..-100) je Koerpergroesse -> Rinnenunterkante:")
    for h in HEIGHTS:
        el = ELBOW * h
        print(f"  H {h}: Topfebene {el + BAND_LIGHT[0]:.0f}-{el + BAND_LIGHT[1]:.0f} -> Rinnenunterkante {el + BAND_LIGHT[0] - 34:.0f}-{el + BAND_LIGHT[1] - 34:.0f}")
    mid = sum(ELBOW * h for h in (1600, 1750, 1900)) / 3
    print(f"  Mittel (1,60/1,75/1,90 m): Ellbogen {mid:.0f}")


def access():
    print("\n=== 2. Zugang zum Beet unter dem Tisch (Tischunterkante = Rinnenunterkante - Holm) ===")
    print(f"Beetrand Z {BED_RIM}, Medium Z {BED_SURFACE}, Holm {HOLM} mm [A]. Freie Hoehe ueber dem Beetrand:")
    for zu in HEIGHT_CANDIDATES:
        free = zu - HOLM - BED_RIM
        free_med = zu - HOLM - BED_SURFACE
        note = "gebueckt/kniend moeglich" if free >= 700 else ("nur kniend, Arme" if free >= 500 else "nur Haende/Unterarme")
        print(f"  Rinnenunterkante {zu}: Tischunterkante {zu - HOLM}, frei ueber Beetrand {free}, ueber Medium {free_med} -> {note}")
    print("Tomate 1,5-2,0 m (Stab/Schnur 2 m), Gurke/Paprika 1,5-2 m: Wuchshoehe ab Medium vs. freie Hoehe bis Rinnenunterkante:")
    for zu in HEIGHT_CANDIDATES:
        print(f"  Rinnenunterkante {zu}: {zu - BED_SURFACE} mm ab Medium")


def sky_shade(zu, rows, pitch, bed_w, tanphi_list, n=801):
    """Anteil der Beetpunkte (Querschnitt, Mitte der Beetbreite bei 0), die von der Himmelsrichtung nicht durch Rinnen verdeckt sind."""
    table_w = (rows - 1) * pitch + CHANNEL_W
    ch = []
    for i in range(rows):
        yc = (i - (rows - 1) / 2) * pitch
        ch.append((yc - CHANNEL_W / 2, yc + CHANNEL_W / 2))
    zb = BED_SURFACE
    z_lo, z_hi = zu, zu + CHANNEL_H
    ys = [(-bed_w / 2) + bed_w * k / (n - 1) for k in range(n)]
    out = []
    for t in tanphi_list:
        free = 0
        for y0 in ys:
            ya = y0 + (z_lo - zb) * t
            yb = y0 + (z_hi - zb) * t
            lo, hi = (ya, yb) if ya <= yb else (yb, ya)
            blocked = any(hi >= a and lo <= b for a, b in ch)
            if not blocked:
                free += 1
        out.append(free / n)
    return out


def shading():
    print("\n=== 3. Verschattung des Beetes unter dem Tisch (Querschnitt, Rinnen unendlich lang, nur Rinnenkoerper; Pflanzen darueber NICHT eingerechnet) ===")
    # diffuser Himmel (isotrop, cosinus-gewichtet), Rinnenrichtung beliebig (Azimut 0..180 gemittelt)
    zen = [i * 5 + 2.5 for i in range(18)]      # 2,5 .. 87,5 Grad
    azs = [i * 10 + 5 for i in range(18)]       # 5 .. 175 Grad relativ zur Rinnenrichtung
    for name, (rows, pitch, bed_w) in RINGS.items():
        if bed_w is None:
            continue
        print(f"\n{name}: Rinnenbreite {CHANNEL_W}, Abstand {pitch}, Beetbreite {bed_w}; Rinnenflaeche in der Draufsicht {rows * CHANNEL_W / bed_w * 100:.0f} % der Beetbreite")
        for zu in (1000, 1100, 1200, 1300):
            tot = 0.0
            wsum = 0.0
            for th in zen:
                w = math.sin(math.radians(th)) * math.cos(math.radians(th))
                tans = [math.tan(math.radians(th)) * abs(math.sin(math.radians(a))) for a in azs]
                fr = sky_shade(zu, rows, pitch, bed_w, tans, n=121)
                tot += w * sum(fr) / len(fr)
                wsum += w
            print(f"  Rinnenunterkante {zu}: Himmelssicht (Anteil des diffusen Himmelslichts) {tot / wsum * 100:4.1f} %")
        # direkte Sonne: Hoehenwinkel, Azimut gemittelt
        for e_name, e in (("Sommer Mittag 63 Grad", 63.4), ("Aequinoktium 40 Grad", 40.0), ("Winter Mittag 17 Grad", 16.6)):
            row = []
            for zu in (1000, 1100, 1200, 1300):
                tans = [abs(math.sin(math.radians(a))) / math.tan(math.radians(e)) for a in azs]
                fr = sky_shade(zu, rows, pitch, bed_w, tans, n=121)
                row.append(f"{zu}: {100 * sum(fr) / len(fr):4.1f} %")
            print(f"    direkte Sonne {e_name:24s} frei: " + "   ".join(row))


def dli():
    print("\n=== 4. Lichtmenge am Beet (Tagessumme PAR, mol/m2/Tag) ===")
    # Quelle: Solarserver/DWD Juni 2026 181,2 kWh/m2 (6,0 kWh/Tag), Dezember 2025 21 kWh/m2 (0,7 kWh/Tag), Januar 2026 26 kWh/m2 (0,8)
    months = {"Juni (6,0 kWh/m2/Tag)": 6.0, "Dezember (0,7 kWh/m2/Tag)": 0.7}
    factor = 2.05                               # mol PAR je MJ Globalstrahlung (MSU/ASHS: 43-45 % PAR, 4,57 umol/J)
    for transm, label in ((0.78, "Plane doppelt, 75-80 %"),):
        for m, kwh in months.items():
            out_dli = kwh * 3.6 * factor
            inside = out_dli * transm
            print(f"  {m}: aussen {out_dli:4.1f}, in der Kuppel ({label}) {inside:4.1f}")
            for pct in (25, 35, 50):
                print(f"      Beet mit {pct} % Himmelssicht: {inside * pct / 100:4.1f} mol/m2/Tag")
    print("  Bedarf: Salat 12-17 (Purdue, MSU, Cornell), Tomate 20-30, hochdrahtige Tomate/Gurke >= 25-30 (MSU).")


def wall_gap():
    print("\n=== 5. Abstand der aeussersten Rinne zur Kuppelhaut bei geaenderter Hoehe (Kugelnaeherung R 6000) ===")
    R = 6000.0
    base = 1300
    r0 = math.sqrt(R * R - base * base)
    for zu in (1000, 1100, 1200, 1300, 1400):
        r = math.sqrt(R * R - zu * zu)
        print(f"  Rinnenunterkante {zu}: Kuppelradius {r:6.1f} mm, Aenderung gegen 1300: {r - r0:+5.1f} mm -> Abstand ca. {21 + (r - r0):4.0f} mm (Basis 21 mm bei 1300, W25a)")


def legs():
    print("\n=== 6. Beine (Annahme: Bein 40 x 40 x 3, Holm 50, Knicklaenge = Beinhoehe) ===")
    I = (40 ** 4 - 34 ** 4) / 12
    for zu in (1000, 1100, 1300):
        L = zu - HOLM
        pcr = math.pi ** 2 * 210000 * I / (2 * L) ** 2 / 1000   # eingespannt-frei, K = 2
        print(f"  Rinnenunterkante {zu}: Beinlaenge {L} mm, Bein-Euler (K=2) {pcr:5.1f} kN, Stahlmenge Beine {L / (1300 - HOLM) * 100:3.0f} % von heute")


if __name__ == "__main__":
    ergonomics()
    access()
    shading()
    dli()
    wall_gap()
    legs()
