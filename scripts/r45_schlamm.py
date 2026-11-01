"""R45 Frage 0: Schlammmenge, Spuelmenge, Fassgroesse, Wurmbett, freie Seite der Absetzer.

Reine Rechnung, aendert nichts. Aufruf: python -X utf8 scripts/r45_schlamm.py
Quellen der Eingaben stehen in docs/research/R45-hydraulik-auslegung.md (Abschnitt 0).
"""
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# --- Eingaben ---------------------------------------------------------------
FUTTER = (3.08, 3.46, 3.85)          # kg/Tag, data/system-specs.json (D61)
FEST_JE_FUTTER = (0.15, 0.30, 0.50)  # kg TS je kg Futter: Patent 0,15 / Fort Valley 0,3 (0,2-0,5)
ANTEIL_SWIRL = 0.23                  # Davidson & Summerfelt 2005 (Swirl, 7-8 % des Stroms)
KONZ_G_L = (8.6, 10.8)               # g TS/l Frischschlamm, Goddek u. a. 2018 Tab. 2
LINIEN = 2

print("== Schlammmenge beider Absetzer (l/Tag) ==")
for name, f, s in (("niedrig", FUTTER[0], FEST_JE_FUTTER[0]),
                   ("Mitte", FUTTER[1], FEST_JE_FUTTER[1]),
                   ("hoch", FUTTER[2], FEST_JE_FUTTER[2])):
    ts = f * s * ANTEIL_SWIRL
    lo, hi = ts * 1000 / KONZ_G_L[1], ts * 1000 / KONZ_G_L[0]
    print(f"{name:8s} TS {ts:.3f} kg/Tag -> {lo:5.1f} bis {hi:5.1f} l/Tag (je Linie {lo/LINIEN:4.1f} bis {hi/LINIEN:4.1f})")

ts_mitte = FUTTER[1] * FEST_JE_FUTTER[1] * ANTEIL_SWIRL
print(f"Wochenmasse Mitte: {ts_mitte*7:.2f} kg TS (beide), {ts_mitte*7/LINIEN:.2f} kg je Linie")

print("\n== Spuelung durch d40 (Torricelli) ==")
di = 0.034          # m, Innendurchmesser PVC-U d40 PN16 (3,0 mm Wand) [A]
cd = 0.6            # Ausflussbeiwert scharfkantig [A]
for h in (0.6, 0.85):
    q = cd * math.pi * di**2 / 4 * math.sqrt(2 * 9.81 * h)
    print(f"Druckhoehe {h:.2f} m: {q*1000:.2f} l/s = {q*60000:.0f} l/min -> 30 l in {30/(q*1000):.0f} s; Absetzer 267 l leer in {267/(q*1000):.0f} s")
print("Pumpe_klein foerdert 12,5 l/min in den Absetzer: offener Hahn = 750 l/h aus dem Pool")

print("\n== Fass ==")
for spuel in (20, 30, 40):
    for tage in (2, 3):
        woche = 7 / tage * spuel
        print(f"Spuelung {spuel} l alle {tage} Tage -> {woche:.0f} l/Woche je Linie")

print("\n== Wurmbett (Mishra 2003: max. getestet 1000 g VS/m2/Woche, Sandbett) ==")
vs_anteil = 0.75    # [A] organischer Anteil der TS
for sicher in (1, 2):
    flaeche = ts_mitte * 7 * vs_anteil * 1000 / (1000 / sicher)
    print(f"Sicherheit {sicher}: {flaeche:.2f} m2 beide Linien")

print("\n== Mischung (Mishra 2003: 15-50 % Schlamm-TS im Karton, 80 % Feuchte) ==")
for anteil in (0.15, 0.25, 0.50):
    karton = ts_mitte * 7 * (1 - anteil) / anteil
    gesamt_ts = ts_mitte * 7 + karton
    nass = gesamt_ts / 0.20
    print(f"Schlammanteil {anteil:.0%}: Karton {karton:.2f} kg trocken/Woche, Mischung {nass:.0f} kg bei 80 % Feuchte")

print("\n== Freie Seite der Absetzer (Bauskript, nur Bauteil-Mittelpunkte, Z rel. = abs - 400) ==")
cmds = json.loads((ROOT / "scripts" / "dome-script.json").read_text(encoding="utf-8"))["commands"]
pos = {}
for c in cmds:
    if c.get("command") == "occurrence.move":
        m = c["params"].get("matrix")
        if m and len(m) == 12:
            pos[c["params"]["occurrence"]] = (m[3], m[7], m[11] - 400)
for ab in ("Tank_klein:1", "Tank_klein:2"):
    ax, ay, _ = pos[ab]
    r = math.hypot(ax, ay)
    rad = (ax / r, ay / r)
    tan = (-rad[1], rad[0])
    print(f"{ab}: radial ({rad[0]:+.2f},{rad[1]:+.2f}) tangential ({tan[0]:+.2f},{tan[1]:+.2f})")
    for label, vx, vy in (("radial aussen", rad[0], rad[1]), ("radial innen", -rad[0], -rad[1]),
                          ("tangential +", tan[0], tan[1]), ("tangential -", -tan[0], -tan[1])):
        hits = []
        for n, (x, y, z) in pos.items():
            if n == ab or n.startswith(("Strebe", "Knoten", "Huelle")):
                continue
            dx, dy = x - ax, y - ay
            along = dx * vx + dy * vy
            side = abs(-dx * vy + dy * vx)
            if 150 < along < 1500 and side < 450 and z < 900:
                hits.append((round(along), n, round(z)))
        hits.sort()
        print(f"  {label:14s}: {len(hits)} Teile unter Z 900 in 0,15-1,5 m / +-0,45 m; naechstes: {hits[:2]}")
