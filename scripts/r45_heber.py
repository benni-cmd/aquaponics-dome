"""R45 Frage 2: Heber-Reserve K01/K17 neu gerechnet, mit Rohrlaengen aus data/leitungstrassen.json.

Aufruf: python -X utf8 scripts/r45_heber.py   (nur Lesen)
Erweitert scripts/heber_rechnung.py (Blasius, glatt) um:
 - Colebrook/Swamee-Jain mit Rauheit k (neu 0,0015 mm, gealtert 0,05 mm [A])
 - Verlustbeiwerte-Faelle aus zwei Quellen: Engineering Toolbox (Bogen 90 Langradius flansch 0,2 / gewindet 0,7, Standard flansch 0,3 / gewindet 1,5;
   T Durchgang flansch 0,2 / gewindet 0,9) und Crane TP-410 (nach MathWorks-Doku: glatter Bogen 30 fT, Gehrungsbogen 90 Grad 60 fT; fT(2 Zoll) = 0,019 [A])
 - Varianten: Rohr d75, Langbogen, Filter tiefer, Pumpe statt Heber
Alle Rohre PVC-U SDR 21: d63 x 3,0 (Innen 57,0), d75 x 3,6 (Innen 67,8).
"""
import json
import math
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TR = json.load(open(os.path.join(ROOT, "data", "leitungstrassen.json"), encoding="utf-8"))
G, NU = 9.81, 1.0e-6
SPIEGEL, EINLAUF = 915.0, 720.0
LINIEN = {"K01 (Linie 1)": ["K01", "K01-m", "K01-b"], "K17 (Linie 2)": ["K17", "K17-m", "K17-b"]}
ABS_T = {"K01 (Linie 1)": "K01-m", "K17 (Linie 2)": "K17-m"}


def laenge(t):
    p = t["pfad"]
    return sum(math.dist(p[i], p[i + 1]) for i in range(len(p) - 1))


def zaehle_boegen(pfad_ids):
    """Richtungswechsel > 20 Grad zwischen aufeinanderfolgenden Segmenten aller Teilstuecke (Stossstellen der Teile mitgerechnet)."""
    pts = []
    for tid in pfad_ids:
        t = next(x for x in TR["trassen"] if x["id"] == tid)
        for p in t["pfad"]:
            if not pts or math.dist(pts[-1], p) > 1e-6:
                pts.append(p)
    n90 = n45 = 0
    for a, b, c in zip(pts, pts[1:], pts[2:]):
        u = [b[i] - a[i] for i in range(3)]
        v = [c[i] - b[i] for i in range(3)]
        cosw = sum(x * y for x, y in zip(u, v)) / (math.hypot(*u) * math.hypot(*v))
        w = math.degrees(math.acos(max(-1, min(1, cosw))))
        if w > 70:
            n90 += 1
        elif w > 20:
            n45 += 1
    return n90, n45


def lam(re, di, k):
    if re < 2300:
        return 64 / re
    return 0.25 / math.log10(k / 1000.0 / (3.7 * di) + 5.74 / re ** 0.9) ** 2


def verlust(laengen, di, q1, q2, kb, kt, n90, k_rauh, extra_k=0.0, dn_wechsel=0.0):
    """Verlust in mm: Eintritt 0,5, Austritt 1,0, n90 Boegen (kb), 2 T im Durchgang (kt), Reibung vor/hinter dem Absetzer-T."""
    vor, hint = laengen
    a = math.pi * di * di / 4
    out = 0.0
    parts = {}
    v1, v2 = q1 / 60000 / a, q2 / 60000 / a
    h1, h2 = v1 * v1 / (2 * G) * 1000, v2 * v2 / (2 * G) * 1000
    f1, f2 = lam(v1 * di / NU, di, k_rauh), lam(v2 * di / NU, di, k_rauh)
    parts["Reibung"] = f1 / di * vor / 1000 * h1 + f2 / di * hint / 1000 * h2
    parts["Eintritt"] = 0.5 * h1
    parts["Boegen"] = (n90 / 2) * kb * h1 + (n90 / 2) * kb * h2     # zwei Boegen vor, zwei hinter dem Absetzer-T
    parts["T"] = kt * h1 + kt * h2
    parts["Austritt"] = 1.0 * h2
    parts["extra"] = extra_k * h2 + dn_wechsel
    return sum(parts.values()), parts


def strecken(namen):
    ids = LINIEN[namen]
    vor = hint = 0.0
    seen = False
    for tid in ids:
        t = next(x for x in TR["trassen"] if x["id"] == tid)
        if seen:
            hint += laenge(t)
        else:
            vor += laenge(t)
        if tid == ABS_T[namen]:
            seen = True
    return vor, hint


FT = 0.019  # fT Crane fuer 2 Zoll [A]
FAELLE = [
    # Name, Kb, Kt
    ("ET Langbogen flansch 0,2 / T 0,2", 0.2, 0.2),
    ("ET Standard flansch 0,3 / T 0,2", 0.3, 0.2),
    ("Crane glatt 30 fT = 0,57 / T 20 fT = 0,38", 30 * FT, 20 * FT),
    ("ET Langbogen gewindet 0,7 / T 0,9", 0.7, 0.9),
    ("Crane Gehrung 60 fT = 1,14 / T 0,9", 60 * FT, 0.9),
]

if __name__ == "__main__":
    d63, d75 = 0.057, 0.0678
    print(f"Druckhoehe {SPIEGEL - EINLAUF:.0f} mm (Spiegel {SPIEGEL:.0f} - Einlaufachse {EINLAUF:.0f}); Grenze Reserve 30 mm [A, loop-state]")
    for namen, ids in LINIEN.items():
        n90, n45 = zaehle_boegen(ids)
        vor, hint = strecken(namen)
        print(f"\n== {namen}: {vor:.0f} + {hint:.0f} mm = {vor + hint:.0f} mm Rohr, {n90} Boegen 90, {n45} Boegen kleiner als 90 ==")
        for rau_name, rau in (("neu k 0,0015", 0.0015), ("gealtert k 0,05", 0.05)):
            print(f"  -- Rauheit {rau_name} mm, Strom 97,5 / 110 l/min --")
            for fname, kb, kt in FAELLE:
                v, _ = verlust((vor, hint), d63, 97.5, 110.0, kb, kt, n90, rau)
                res = SPIEGEL - EINLAUF - v
                print(f"   {fname:44s} Verlust {v:5.0f} mm  Reserve {res:5.0f} mm{'  <-- unter 30' if res < 30 else ''}")

        print("  -- Varianten, Rauheit gealtert, schlechtester Fall (Crane Gehrung/T 0,9) und Mittel (Crane glatt) --")
        for label, kw in (("schlecht", dict(kb=60 * FT, kt=0.9)), ("Mittel", dict(kb=30 * FT, kt=20 * FT))):
            def res(di=d63, kb=kw["kb"], kt=kw["kt"], n=n90, extra=0.0, head_plus=0.0):
                v, _ = verlust((vor, hint), di, 97.5, 110.0, kb, kt, n, 0.05, extra_k=extra)
                return SPIEGEL - EINLAUF + head_plus - v
            print(f"   [{label}] Ist                                   {res():5.0f} mm")
            print(f"   [{label}] d75 durchgehend (+2 Reduzierstuecke)  {res(di=d75, extra=0.3):5.0f} mm")
            print(f"   [{label}] Langbogen 0,2 statt Kb               {res(kb=0.2):5.0f} mm")
            print(f"   [{label}] Filter-Grube +100 mm tiefer          {res(head_plus=100):5.0f} mm")
            print(f"   [{label}] d75 + Langbogen 0,2                  {res(di=d75, kb=0.2, extra=0.3):5.0f} mm")

    print("\n== Pumpe statt Heber (Leistung fuer die Foerderhoehe 0,25 m, Wirkungsgrad 25 % wie Netz R21) ==")
    q = 110 / 60000
    print(f"  P = rho g Q H / eta = {1000 * G * q * 0.25 / 0.25:.0f} W je Linie bei 0,25 m, plus Saugschutz, Trockenlauf, Steuerung")
