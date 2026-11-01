"""R45 Frage 1: Beet-Ablauf d25 gegen d40 (L03). Siphon-Kapazitaet und Geschwindigkeiten.

Reine Rechnung. Aufruf: python -X utf8 scripts/r45_beetablauf.py
Innendurchmesser = d - 2 x Wand (EN 1452, SDR 21: d25 1,5 / d32 1,6 / d40 1,9 / d50 2,4 mm; d25 Mindestwand 1,5).
"""
import math

G = 9.81
NU = 1.0e-6         # m2/s Wasser ca. 20 C
K_RAU = 0.0015e-3   # m, Hersteller-/Lehrbuchwert PVC (glatt) [A]


def innen(d, wand):
    return (d - 2 * wand) / 1000.0


def lam(re, di):
    """Darcy-Reibungszahl: laminar 64/Re, sonst Swamee-Jain (explizit, turbulent)."""
    if re < 2300:
        return 64 / re
    return 0.25 / math.log10(K_RAU / (3.7 * di) + 5.74 / re**0.9) ** 2


def siphon_q(di, h, l_rohr, k_ein):
    """Voll laufendes Standrohr: Energiegleichung h = (k_ein + lam*l/d + 1) v2/2g, iterativ."""
    v = 1.0
    for _ in range(60):
        re = v * di / NU
        f = lam(re, di)
        v = math.sqrt(2 * G * h / (k_ein + 1.0 + f * l_rohr / di))
    return v * math.pi * di**2 / 4 * 60000, v


rohre = {"d25": innen(25, 1.5), "d32": innen(32, 1.6), "d40": innen(40, 1.9), "d50": innen(50, 2.4)}
print("Innendurchmesser mm:", {k: round(v * 1000, 1) for k, v in rohre.items()})

print("\n== Geschwindigkeit bei Q = 36 l/min (Soll: 234 l in 6,5 min) ==")
q = 36 / 60000
for k, di in rohre.items():
    v = q / (math.pi * di**2 / 4)
    print(f"{k}: {v:.2f} m/s")

print("\n== Was das Standrohr als Siphon wirklich durchlaesst (Druckhoehe h = Wasserstand ueber Austritt) ==")
print("Eintritt K 0,5 (Rohr in Glocke, scharfkantig) + Austritt 1,0; Rohrlaenge 0,6 m (Standrohr 0,53 + Stutzen)")
for k in ("d25", "d32", "d40"):
    di = rohre[k]
    for h in (0.30, 0.45, 0.60):
        qs, v = siphon_q(di, h, 0.6, 0.5)
        print(f"{k} h {h:.2f} m: {qs:5.1f} l/min  v {v:.2f} m/s  -> 234 l in {234/qs:.1f} min")

print("\n== Sammelleitung d40 (Innen-Ø 36,2 mm) bei gleichzeitigem Siphon-Ablauf ==")
di = rohre["d40"]
for n in (1, 2, 3):
    qs, _ = siphon_q(rohre["d25"], 0.45, 0.6, 0.5)
    v = n * qs / 60000 / (math.pi * di**2 / 4)
    print(f"{n} Beet(e) gleichzeitig a {qs:.0f} l/min: {n*qs:.0f} l/min, v {v:.2f} m/s (Grenze 1,5)")
di = rohre["d50"]
for n in (3, 4):
    qs, _ = siphon_q(rohre["d25"], 0.45, 0.6, 0.5)
    v = n * qs / 60000 / (math.pi * di**2 / 4)
    print(f"{n} Beete in d50 (Innen-Ø {di*1000:.1f}): {n*qs:.0f} l/min, v {v:.2f} m/s")

print("\n== Druckverlust Stutzen d25 (0,1 m) + Reduzierung auf d40 bei 36 l/min ==")
di = rohre["d25"]
v = q / (math.pi * di**2 / 4)
f = lam(v * di / NU, di)
dp_m = (f * 0.1 / di + 0.5 + 1.0) * v**2 / (2 * G)   # Reibung + Erweiterung (Borda ~1,0 bei grosser Aufweitung) [A]
print(f"v {v:.2f} m/s, lambda {f:.3f}, Verlust {dp_m*1000:.0f} mm WS (Reibung + Erweiterung)")
