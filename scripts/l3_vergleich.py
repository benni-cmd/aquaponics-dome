"""N-UNIFY-AUTOBAHN L3 (D156): Vergleich der ANORDNUNG Modell gegen Quelle (nicht der Masse).

Quelle: data/oasis-draufsicht.json (Mitten der Zeichnung, Tuer-Achse Az -72). Modell: Bauplaetze data/oasis-lage.json (L3) und Einbauten
data/becken-ports.json (Pumpensockel, Schwimmerhalter). Verglichen wird je Linie: Seite (Ost/West der Spiegelachse), Winkel zur Spiegelachse
(Quelle: Tuer-Achse -72, Modell: Mitte der Technik-Luecke -54, D157) und Reihenfolge nach Radius.
Aufruf (Projektordner): python -I -X utf8 scripts/l3_vergleich.py [--md]   -> Tabelle, Bild renders/l3-anordnung-vs-quelle.png (Quelle um 18 Grad
auf die Modell-Achse gedreht, blau; Modell orange). Exit 0 = Seite stimmt fuer jedes Teil und die Reihenfolge nach Radius je Linie ist gleich, sonst 1.
"""
import json
import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
Q = json.load(open(os.path.join(ROOT, "data", "oasis-draufsicht.json"), encoding="utf-8"))["teile"]
LAGE = {b["id"]: b["bauplatz"] for b in json.load(open(os.path.join(ROOT, "data", "oasis-lage.json"), encoding="utf-8"))["bauteile"] if b.get("bauplatz")}
PORTS = json.load(open(os.path.join(ROOT, "data", "becken-ports.json"), encoding="utf-8"))
ACHSE_Q, ACHSE_M = -72.0, -54.0
LINIE = {1: ["filterpumpe_1", "venturi_1", "hauptpumpe_1", "sump_1", "vortex_1", "bio_1", "sludge_1", "schwimmer_1"],
         2: ["filterpumpe_2", "venturi_2", "hauptpumpe_2", "sump_2", "vortex_2", "bio_2", "sludge_2", "schwimmer_2"],
         0: ["nursery", "feed"]}


def modell_xy(sid):
    for k, e in enumerate(PORTS["sumpf_einbauten"], 1):
        if sid == "hauptpumpe_%d" % k:
            return e["pumpensockel_mm"][:2]
        if sid == "schwimmer_%d" % k:
            return e["schwimmerhalter_mm"][:2]
    b = LAGE[sid]
    return b["x_mm"], b["y_mm"]


def rel(x, y, achse):
    return (math.degrees(math.atan2(y, x)) - achse + 180) % 360 - 180, math.hypot(x, y)


def main():
    zeilen, ok = [], True
    for ln, ids in LINIE.items():
        q = [(sid,) + rel(Q[sid]["x_mm"], Q[sid]["y_mm"], ACHSE_Q) for sid in ids]
        m = [(sid,) + rel(*modell_xy(sid), ACHSE_M) for sid in ids]
        rq = {s: i for i, (s, _, _) in enumerate(sorted(q, key=lambda t: t[2]), 1)}
        rm = {s: i for i, (s, _, _) in enumerate(sorted(m, key=lambda t: t[2]), 1)}
        for (sid, wq, r_q), (_, wm, r_m) in zip(q, m):
            seite = (ln == 0) or (math.copysign(1, wq) == math.copysign(1, wm))
            achse_ok = ln != 0 or abs(wm) <= 10.0
            ok &= seite and achse_ok
            zeilen.append((sid, wq, r_q, rq[sid], wm, r_m, rm[sid], "OK" if seite and achse_ok else "Seite falsch"))
        if [s for s, _, _ in sorted(q, key=lambda t: t[2])] != [s for s, _, _ in sorted(m, key=lambda t: t[2])]:
            zeilen.append(("Linie %d" % ln, 0, 0, 0, 0, 0, 0, "Reihenfolge nach Radius weicht ab"))
    md = "--md" in sys.argv
    print("| Teil | Quelle: Winkel zur Tuer-Achse | Quelle r (mm) | Rang r | Modell: Winkel zur Mittelachse | Modell r (mm) | Rang r | Urteil |" if md else "Teil           Quelle(Winkel, r, Rang)      Modell(Winkel, r, Rang)   Urteil")
    if md:
        print("|---|---|---|---|---|---|---|---|")
    for z in zeilen:
        if z[0].startswith("Linie"):
            print(("| %s | | | | | | | %s |" if md else "%-14s %s") % (z[0], z[7]))
            continue
        print(("| %s | %+.0f | %.0f | %d | %+.0f | %.0f | %d | %s |" if md else "%-14s %+5.0f %6.0f %2d        %+5.0f %6.0f %2d       %s") % z)
    bild()
    print("Ergebnis:", "Seite und Reihenfolge wie in der Quelle" if ok and not any(z[0].startswith("Linie") for z in zeilen) else "Abweichung (siehe Urteil)")
    return 0 if ok and not any(z[0].startswith("Linie") for z in zeilen) else 1


def bild():
    from PIL import Image, ImageDraw, ImageFont
    W, R = 1500, 6800.0
    k = (W / 2 - 20) / R
    P = lambda x, y: (W / 2 + x * k, W / 2 - y * k)
    im = Image.new("RGB", (W, W), "white")
    d = ImageDraw.Draw(im)
    try:
        f = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 17)
        fb = ImageFont.truetype("C:/Windows/Fonts/arialbd.ttf", 24)
    except OSError:
        f = fb = ImageFont.load_default()
    ecken = [(6000 * math.cos(math.radians(18 + 36 * t)), 6000 * math.sin(math.radians(18 + 36 * t))) for t in range(11)]
    d.line([P(*e) for e in ecken], fill=(170, 170, 170), width=2)
    for a, col in ((ACHSE_M, (230, 120, 20)), (ACHSE_Q, (120, 120, 120))):
        d.line([P(0, 0), P(6000 * math.cos(math.radians(a)), 6000 * math.sin(math.radians(a)))], fill=col, width=1)
    rot = math.radians(ACHSE_M - ACHSE_Q)
    for ids in LINIE.values():
        for sid in ids:
            x, y = Q[sid]["x_mm"], Q[sid]["y_mm"]
            xq, yq = x * math.cos(rot) - y * math.sin(rot), x * math.sin(rot) + y * math.cos(rot)
            xm, ym = modell_xy(sid)
            a, b = P(xq, yq), P(xm, ym)
            d.line([a, b], fill=(200, 200, 200), width=1)
            d.ellipse([a[0] - 6, a[1] - 6, a[0] + 6, a[1] + 6], outline=(30, 90, 200), width=3)
            d.ellipse([b[0] - 6, b[1] - 6, b[0] + 6, b[1] + 6], fill=(235, 120, 20))
            d.text((b[0] + 8, b[1] - 8), sid, fill=(0, 0, 0), font=f)
    d.text((20, 15), "Anordnung: Quelle (blau, um 18 Grad auf die Modell-Achse gedreht) gegen Modell L3 (orange)", fill=(0, 0, 0), font=fb)
    d.text((20, 48), "Linien gespiegelt um Az -54 (Mitte der Technik-Luecke, D157); grau: Tuer-Achse Az -72", fill=(0, 0, 0), font=f)
    im.save(os.path.join(ROOT, "renders", "l3-anordnung-vs-quelle.png"))


if __name__ == "__main__":
    sys.exit(main())
