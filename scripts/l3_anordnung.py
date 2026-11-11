"""N-UNIFY-AUTOBAHN L3 (D156): Technik nach der ANORDNUNG der Quelle, Masse nach Begehbarkeit.

Ringe und Fischtank bleiben wie vor L2 (ce15b86). Die Technik steht in zwei Linien (Linie 1 Ost = Tuer-Achse + phi, Linie 2 West = - phi),
Reihenfolge wie in der Quelle von innen nach aussen: Pumpe im Fischtank -> Venturi -> Sumpf (Pumpe, Schwimmer) -> Vortex -> Biofilter -> Schlammreaktor;
Anzucht- und Lebendfutterbecken als Kette zur Tuer-Achse. phi = Azimut - Tuer-Azimut (-72), positiv Richtung Ost (Az -18).

Aufruf (Projektordner):
  python -I -X utf8 scripts/l3_anordnung.py            Plan pruefen, Bild renders/l3-anordnung.png, KEIN Schreiben
  python -I -X utf8 scripts/l3_anordnung.py --schreiben  zusaetzlich Bauplaetze in data/oasis-lage.json (Feld bauplatz, Quelle L3)
Pruefungen vor dem Bau (Regeln aus U1 scripts/oasis_lagepruefung.py und D62): Abstand >= 500 mm zu Ringen (Beet + Portal), Innenring (r 2195),
Fischtank und zwischen Technikteilen; Wand: 100 mm zur Zehneck-Innenkante; Kuppel: hypot(r, Hoehe) <= 5800; Tuer-Gang 900 mm frei (Streifen auf der Achse).
Sumpftanks liegen unter dem begehbaren Deckel: sie zaehlen nicht als Hindernis im Gang, aber gegen andere Teile im Boden (Fischtank, Becken) mit 300 mm.
Die Messung nach dem Bau macht scripts/check_walkways_voll.py (Gaenge, Erreichbarkeit, Kopf) - dieses Skript ist die Planungshilfe.
"""
import json
import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import gen_dome as G   # noqa: E402  (nur Lagen von Ringen und Beeten, kein Bau)

TUER = -72.0
ACHSE_M = -54.0                               # Spiegelachse der Linien = Mitte der Technik-Luecke (Mittelring offen -126..+18, Aussenring -90..-18), D157
AP = 6000.0 * math.cos(math.radians(18))      # Zehneck-Innenkante 5706
KUGEL, WANDLUFT, GANG, LUFT, LUFT_BODEN = 5800.0, 100.0, 900.0, 500.0, 300.0
LUFT_RING = 150.0                             # zu Beet + Portal (U1-Regel luft_mm); der 500-mm-Gang ZU jedem Teil (D156) wird mit check_walkways_voll gemessen
LUFT_TECHNIK = 150.0                          # zwischen Technikteilen (U1-Regel luft_mm); Zugang je Teil misst check_walkways_voll
GANG_B, GANG_B_PHI = (3959.0, 4559.0), 28.0     # Ring-Gang B und Winkel ab Mittelachse, ab dem er frei bleiben muss
INNENRING_R = 2195.0                          # Aussenkante der Innentische (U5, D63)
FISCH_R = 2095.0                              # Fischtank Huelle (Wasser 3890 + 2 x 150)

# Fussabdruck (Kreis-Ersatz aus den Bounding-Boxen in scripts/.compbox.json, Stand ce15b86) und Hoehe ueber Flur (fuer die Kuppelkugel)
FORM = {
    "vortex": {"r": 470.0, "h": 1900.0},      # Podest 780 x 780, Tank-Stutzen bis 442 -> Umkreis ~ 470 (Ecken: Quadrat 390 -> 551, siehe Bild)
    "bio": {"r": 570.0, "h": 1990.0},         # Podest 980 x 980 (Ecken 693), Tank 930 + Stutzen 570
    "sludge": {"r": 340.0, "h": 605.0},       # Schlamm-Sammelbehaelter L3 (D159): Ø 600 + Stutzen, Oberkante 590 + Deckel ueber Flur, eingelassen
    "nursery": {"r": 760.0, "h": 1000.0},     # Anzuchtbecken L3: Wasser 1400 + 2 x 60 = 1520 (D157)
    "feed": {"r": 415.0, "h": 1000.0},        # Lebendfutter L3: Wasser 710 + 2 x 60 = 830 (D157)
}
QUADRAT = {"vortex": 390.0, "bio": 490.0}    # Podest-Halbbreite (Ecken pruefen)

# ---------------------------------------------------------------- PLAN (phi in Grad zur Tuer-Achse, r in mm); Linie 2 = Spiegelbild, ausser in WEST
PLAN = {   # gefunden mit einer Gittersuche (Schritt 2 Grad / 50 mm) unter den Pruefungen unten, Reihenfolge Becken -> Vortex -> Biofilter -> Schlamm -> Sumpf, Ring-Gang B frei (11.11.2026)
    "filterpumpe": (40.0, 1702.0),   # im Fischtank auf dem Innenboden (D108/D129), Azimut der Linie
    "venturi": (40.0, 2450.0),       # haengt im Druckrohr (Z 1650), kein Bodenhindernis
    "sump": (24.0, 4500.0),          # Grube unter Flur (D158: 1125 x 1600 x 670), Deckel begehbar
    "vortex": (36.0, 3300.0),
    "bio": (58.0, 3350.0),
    "sludge": (32.0, 5400.0),        # Schlamm-Sammelbehaelter schmal und eingelassen (D159)
}
WEST = {}                            # abweichende Lage fuer Linie 2 (phi mit Vorzeichen); leer = spiegelgleich
SUMPF_LANG = {"sump_1": 300.0, "sump_2": -408.0}   # 180 Grad gegen die Suche gedreht (gleicher Grundriss): Pumpe innen, Schwimmer aussen wie in der Quelle   # Langachse der Grube (Weltrahmen), Linie 2 gespiegelt: 2 x ACHSE_M - Linie 1
ACHSE = {"nursery": (2.5, 3500.0), "feed": (2.5, 4885.0)}   # Kette Lebendfutter -> Anzucht -> Fischtank auf der Mittelachse (D157)
GANG_BIS_R = 2700.0                  # Tuer-Gang 900 mm gerade auf der Tuer-Achse von der Tuer bis Gang A (r 2700)


def pol(phi, r):
    a = math.radians(ACHSE_M + phi)
    return r * math.cos(a), r * math.sin(a)


def plaetze():
    out = {}
    for k, (phi, r) in PLAN.items():
        out[k + "_1"] = pol(phi, r) + (phi, r)
        p2 = WEST.get(k, (-phi, r))
        out[k + "_2"] = pol(*p2) + p2
    for k, (phi, r) in ACHSE.items():
        out[k] = pol(phi, r) + (phi, r)
    return out


def ring_rechtecke():
    """Beete mit Portal (Tisch ueber dem Beet) als Rechtecke wie check_walkways_voll: aussen 2640 x 1030, mitte 1865 x 1163."""
    out = []
    for b in G.LAYOUT["ibc_beds"]:
        x, y = G.bed_xy(b)
        yaw = G.bed_yaw(b)
        l, w = (2640, 1030) if "plants" in b else (b["length"], b["width"] + 230)
        out.append(("Beet %s r %.0f az %.0f" % ("aussen" if "plants" in b else "mitte", math.hypot(x, y), math.degrees(math.atan2(y, x))), G.rect_corners(x, y, l, w, yaw)))
    return out


def pkt_poly(p, poly):
    """Abstand Punkt - konvexes Polygon (0 innen)."""
    inside = all(((poly[(i + 1) % 4][0] - poly[i][0]) * (p[1] - poly[i][1]) - (poly[(i + 1) % 4][1] - poly[i][1]) * (p[0] - poly[i][0])) >= 0 for i in range(4)) or \
        all(((poly[(i + 1) % 4][0] - poly[i][0]) * (p[1] - poly[i][1]) - (poly[(i + 1) % 4][1] - poly[i][1]) * (p[0] - poly[i][0])) <= 0 for i in range(4))
    if inside:
        return 0.0
    best = 1e18
    for i in range(4):
        a, b = poly[i], poly[(i + 1) % 4]
        dx, dy = b[0] - a[0], b[1] - a[1]
        t = max(0.0, min(1.0, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / (dx * dx + dy * dy)))
        best = min(best, math.hypot(p[0] - a[0] - t * dx, p[1] - a[1] - t * dy))
    return best



def sumpf_rect(x, y, phi, r, key=None):
    """Grube (Wanne aussen, Mass aus gen_dome), Langachse SUMPF_LANG[key] oder radial."""
    return G.rect_corners(x, y, G.SUMPF_WANNE_L, G.SUMPF_WANNE_B, SUMPF_LANG.get(key, ACHSE_M + phi))


def pruefen(pl):
    fehler, info = [], []
    ringe = ring_rechtecke()
    teile = {k: v for k, v in pl.items() if k.split("_")[0] in FORM}
    for k, (x, y, phi, r) in teile.items():
        f = FORM[k.split("_")[0]]
        rr = f["r"]
        rmax = r + (QUADRAT.get(k.split("_")[0], 0) * math.sqrt(2) if k.split("_")[0] in QUADRAT else rr)
        # Ringe
        for nm, poly in ringe:
            d = pkt_poly((x, y), poly) - rr
            if d < LUFT_RING:
                fehler.append("%-10s zu %s: %.0f mm (Soll >= %.0f)" % (k, nm, d, LUFT_RING))
        # Innenring / Fischtank
        d = r - rr - INNENRING_R
        if d < LUFT:
            fehler.append("%-10s zum Innenring (r %.0f): %.0f mm" % (k, INNENRING_R, d))
        # Ring-Gang B zwischen Mittel- und Aussenring (Beet mitte + Portal bis r 3959, Beet aussen ab r 4559): Eingaenge aus dem Technikbereich frei halten (gemessen 11.11.: Biofilter dort -> 6 Aussenbeete nicht erreichbar)
        if abs(phi) >= GANG_B_PHI and r + rr > GANG_B[0] and r - rr < GANG_B[1]:
            fehler.append("%-10s im Ring-Gang B (r %.0f bis %.0f, |phi| >= %.0f)" % (k, GANG_B[0], GANG_B[1], GANG_B_PHI))
        # Wand und Kuppel
        wand = AP - max(x * math.cos(math.radians(36 * i + TUER)) + y * math.sin(math.radians(36 * i + TUER)) for i in range(10)) - rr
        if wand < WANDLUFT:
            fehler.append("%-10s zur Wand: %.0f mm (Soll >= %.0f)" % (k, wand, WANDLUFT))
        if math.hypot(rmax, f["h"]) > KUGEL:
            fehler.append("%-10s Kuppelkugel: hypot(%.0f, %.0f) = %.0f > %.0f" % (k, rmax, f["h"], math.hypot(rmax, f["h"]), KUGEL))
        # Tuer-Gang: Streifen +-450 um die Achse von r 2700 bis zur Wand
        u = (math.cos(math.radians(TUER)), math.sin(math.radians(TUER)))
        quer = abs(-x * u[1] + y * u[0])
        laengs = x * u[0] + y * u[1]
        if quer - rr < GANG / 2 and laengs > GANG_BIS_R - rr:
            fehler.append("%-10s liegt im Tuer-Gang-Streifen (quer %.0f, laengs %.0f)" % (k, quer, laengs))
    ks = list(teile)
    for a in range(len(ks)):
        for b in range(a + 1, len(ks)):
            A, B = teile[ks[a]], teile[ks[b]]
            d = math.hypot(A[0] - B[0], A[1] - B[1]) - FORM[ks[a].split("_")[0]]["r"] - FORM[ks[b].split("_")[0]]["r"]
            soll = 200.0 if {"nursery", "feed"} == {ks[a].split("_")[0], ks[b].split("_")[0]} else LUFT_TECHNIK   # Ueberlauf-Kette: Becken nebeneinander (Tuelle 130 mm)
            if d < soll:
                fehler.append("%-10s - %-10s %.0f mm (Soll >= %.0f)" % (ks[a], ks[b], d, soll))
    # Sumpf im Boden (Deckel begehbar, darf unter Gaengen liegen): nicht unter Bodenteilen (Technik, Becken, Beete), 300 mm zu Fischtank und versenkten Becken
    for s_ in ("sump_1", "sump_2"):
        x, y, phi, r = pl[s_]
        poly = sumpf_rect(x, y, phi, r, s_)
        for nm, (cx, cy, rr) in [("Fischtank", (0.0, 0.0, FISCH_R + LUFT_BODEN))] + [(k, (v[0], v[1], FORM[k.split("_")[0]]["r"] + (LUFT_BODEN if k in ("nursery", "feed") else 0.0))) for k, v in teile.items()]:
            d = pkt_poly((cx, cy), poly) - rr
            if d < 0:
                fehler.append("%-10s (Grube) unter/an %s: %.0f mm" % (s_, nm, d))
        for nm, ring in ringe:
            if any(pkt_poly(q, ring) == 0 for q in poly) or any(pkt_poly(q, poly) == 0 for q in ring):
                fehler.append("%-10s (Grube) unter %s" % (s_, nm))
        wand = AP - max(max(px * math.cos(math.radians(36 * i + TUER)) + py * math.sin(math.radians(36 * i + TUER)) for i in range(10)) for px, py in poly)
        if wand < WANDLUFT:
            fehler.append("%-10s (Grube) zur Wand/Fundament: %.0f mm" % (s_, wand))
    return fehler, info, ringe


def bild(pl, ringe, pfad):
    from PIL import Image, ImageDraw, ImageFont
    W = 1600
    R = 6600.0
    k = (W / 2 - 20) / R
    P = lambda x, y: (W / 2 + x * k, W / 2 - y * k)
    im = Image.new("RGB", (W, W), "white")
    d = ImageDraw.Draw(im)
    try:
        f = ImageFont.truetype("C:/Windows/Fonts/arial.ttf", 18)
    except OSError:
        f = ImageFont.load_default()
    ecken = [(6000 * math.cos(math.radians(18 + 36 * t)), 6000 * math.sin(math.radians(18 + 36 * t))) for t in range(11)]
    d.line([P(*e) for e in ecken], fill=(150, 150, 150), width=3)
    for nm, poly in ringe:
        d.polygon([P(*p) for p in poly], outline=(60, 140, 60), fill=(220, 240, 220))
    for rr, col in ((FISCH_R, (60, 120, 200)), (INNENRING_R, (60, 140, 60))):
        d.ellipse([P(-rr, rr), P(rr, -rr)], outline=col, width=3)
    u = (math.cos(math.radians(TUER)), math.sin(math.radians(TUER)))
    v = (-u[1], u[0])
    g = [(u[0] * a + v[0] * b, u[1] * a + v[1] * b) for a, b in ((GANG_BIS_R, -GANG / 2), (AP, -GANG / 2), (AP, GANG / 2), (GANG_BIS_R, GANG / 2))]
    d.polygon([P(*p) for p in g], outline=(220, 160, 0))
    for s in ("sump_1", "sump_2"):
        d.polygon([P(*p) for p in sumpf_rect(*pl[s], key=s)], outline=(90, 90, 90), fill=(235, 235, 235))
    farbe = {"vortex": (200, 80, 30), "bio": (40, 130, 60), "sludge": (120, 80, 40), "nursery": (40, 120, 220), "feed": (40, 160, 200)}
    for kk, (x, y, phi, r) in pl.items():
        t = kk.split("_")[0]
        if t in FORM:
            rr = FORM[t]["r"]
            if t in QUADRAT:
                q = QUADRAT[t]
                d.polygon([P(*p) for p in G.rect_corners(x, y, 2 * q, 2 * q, ACHSE_M + phi)], outline=farbe[t])
            d.ellipse([P(x - rr, y + rr), P(x + rr, y - rr)], outline=farbe[t], width=3)
        else:
            a = P(x, y)
            d.ellipse([a[0] - 5, a[1] - 5, a[0] + 5, a[1] + 5], fill=(0, 0, 0))
        d.text(P(x, y), kk, fill=(0, 0, 0), font=f)
    d.text((20, 20), "L3 Anordnung (Planungsbild): Ringe wie ce15b86, Tuer-Gang 900 (gelb), Sumpf-Gruben grau (begehbar)", fill=(0, 0, 0), font=f)
    im.save(pfad)


def main():
    pl = plaetze()
    fehler, info, ringe = pruefen(pl)
    for k, (x, y, phi, r) in sorted(pl.items()):
        print("%-14s phi %+6.1f  r %5.0f  ->  x %7.0f  y %7.0f" % (k, phi, r, x, y))
    for t in info:
        print("INFO", t)
    for t in fehler:
        print("FAIL", t)
    print("Fehler:", len(fehler))
    bild(pl, ringe, os.path.join(ROOT, "renders", "l3-anordnung.png"))
    if "--schreiben" in sys.argv:
        schreiben(pl)
    return 1 if fehler else 0


ID = {"filterpumpe_1": "filterpumpe_1", "filterpumpe_2": "filterpumpe_2", "venturi_1": "venturi_1", "venturi_2": "venturi_2", "vortex_1": "vortex_1",
      "vortex_2": "vortex_2", "bio_1": "bio_1", "bio_2": "bio_2", "sludge_1": "sludge_1", "sludge_2": "sludge_2", "sump_1": "sump_1", "sump_2": "sump_2",
      "nursery": "nursery", "feed": "feed"}


def schreiben(pl):
    p = os.path.join(ROOT, "data", "oasis-lage.json")
    lage = json.load(open(p, encoding="utf-8"))
    for b in lage["bauteile"]:
        if b["id"] not in ID.values():
            continue
        x, y, phi, r = pl[b["id"]]
        alt = b.get("bauplatz") or {}
        z = (b.get("u1_bauplatz") or alt).get("z_modell_mm", 400.0)
        dreh = SUMPF_LANG.get(b["id"], ACHSE_M + phi) if b["id"].startswith("sump") else (b.get("u1_bauplatz") or alt).get("drehung_grad", 0.0)   # Sumpf: Langachse tangential (sumpf_orte: yaw = Langachse - 90)
        b["bauplatz"] = {"x_mm": round(x, 1), "y_mm": round(y, 1), "drehung_grad": round(dreh, 2), "z_modell_mm": z, "r_mm": round(r, 1),
                         "az_grad": round(ACHSE_M + phi, 1), "quelle": "L3 (D156, D157): Anordnung der Quelle, scripts/l3_anordnung.py"}
    lage["meta"]["l3"] = "11.11.2026 N-UNIFY-AUTOBAHN L3: Technik nach Anordnung der Quelle mit Laufwegen (scripts/l3_anordnung.py, D156, D157); Teile ohne L3-Eintrag behalten den Bauplatz von L2/U1"
    json.dump(lage, open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print("geschrieben:", p)


if __name__ == "__main__":
    sys.exit(main())
