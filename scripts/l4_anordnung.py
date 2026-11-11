"""N-UNIFY-AUTOBAHN L4 (D161): Becken-Kette Wand an Wand, Filter-Podeste Kante an Kante, Notluftpumpe unter dem Podest.

Baut auf scripts/l3_anordnung.py auf (gleiche Pruefregeln, Spiegelachse Az -54, D157) und aendert:
  1. Becken-Kette auf der Mittelachse: Fischtank (Huelle r 2095) - Anzucht (Huelle Ø 1520) - Lebendfutter (Huelle Ø 830), Spalt SPALT_BECKEN.
     Die Kette laeuft zwischen den Fuessen der Innentische bei Az -71,7 und -35,7 durch (Abstand wird gemessen).
  2. Je Linie Vortex- und Biofilter-Podest Kante an Kante (Spalt SPALT_PODEST, Podest-Aussenmass 780 / 980 aus scripts/.compbox.json),
     Paar-Achse tangential, Vortex naeher an der Mittelachse (Quelle: Vortex 38 Grad, Biofilter 49 Grad neben der Tuer-Achse).
  3. Sumpf-Gruben und Schlammsammler neu gesucht (Regeln wie L3).
Aufruf (Projektordner): python -I -X utf8 scripts/l4_anordnung.py [--schreiben]   (Bild renders/l4-anordnung.png)
Die Messung nach dem Bau: scripts/check_walkways_voll.py (Gaenge, Tuer-Gang 900), scripts/check_lage_konflikte.py (Ueberlappung).
"""
import json
import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import l3_anordnung as L   # noqa: E402

SPALT_BECKEN, SPALT_PODEST = 30.0, 20.0
FISCH_HUELLE = 2095.0
NURSERY_R, FEED_R = 760.0, 415.0
PODEST_HALB = {"vortex": 390.0, "bio": 490.0}
INNENTISCH_FUESSE = [(-71.7, (-84.0, 2160.0), (174.0, 2160.0)), (-35.7, (-84.0, 2160.0), (174.0, 2160.0))]   # Az Tisch, Fuesse (tangential, r) aus tisch_geom
FUSSPLATTE = 80.0
# gefundene Lage (Gittersuche in main --suchen), phi zur Mittelachse Az -54
PAAR = (50.0, 3350.0)          # Mitte des Podest-Paars Linie 1 (Linie 2 gespiegelt)
SUMPF = (22.0, 4300.0, 283.0)  # Gittersuche: 103 Grad; um 180 gedreht (gleicher Grundriss), damit Pumpe innen und Schwimmer aussen liegen wie in der Quelle
SCHLAMM = (32.0, 5400.0)

r_n = FISCH_HUELLE + SPALT_BECKEN + NURSERY_R
r_f = r_n + NURSERY_R + SPALT_BECKEN + FEED_R


def paar_lagen(phi, r):
    """Vortex- und Biofilter-Mitte (phi, r) einer Linie: Paar-Achse tangential, Mittenabstand 390 + Spalt + 490."""
    x, y = L.pol(phi, r)
    a = math.radians(L.ACHSE_M + phi + 90.0 * (1 if phi >= 0 else -1))   # tangential, von der Mittelachse weg
    d = PODEST_HALB["vortex"] + SPALT_PODEST + PODEST_HALB["bio"]
    f_v = PODEST_HALB["bio"] + SPALT_PODEST / 2 - d / 2   # Paar-Mitte = Mitte zwischen den Aussenkanten
    vx, vy = x - math.cos(a) * (d / 2 - (PODEST_HALB["bio"] - PODEST_HALB["vortex"]) / 2), y - math.sin(a) * (d / 2 - (PODEST_HALB["bio"] - PODEST_HALB["vortex"]) / 2)
    bx, by = vx + math.cos(a) * d, vy + math.sin(a) * d
    to = lambda px, py: ((math.degrees(math.atan2(py, px)) - L.ACHSE_M + 180) % 360 - 180, math.hypot(px, py))
    return to(vx, vy), to(bx, by), math.degrees(a)


def setzen(paar=PAAR, sumpf=SUMPF, schlamm=SCHLAMM):
    L.ACHSE.clear()
    L.ACHSE.update({"nursery": (0.0, r_n), "feed": (0.0, r_f)})
    (pv, rv), (pb, rb), yaw = paar_lagen(*paar)
    L.PLAN["vortex"], L.PLAN["bio"] = (pv, rv), (pb, rb)
    L.PLAN["sump"] = (sumpf[0], sumpf[1])
    L.SUMPF_LANG.update({"sump_1": sumpf[2], "sump_2": 2 * L.ACHSE_M - sumpf[2]})
    L.PLAN["sludge"] = schlamm
    L.PLAN["filterpumpe"] = (paar[0], 1702.0)
    L.PLAN["venturi"] = (paar[0], 2450.0)
    L.WEST.clear()
    return yaw


ERLAUBT = ("nursery    zum Innenring", "nursery    liegt im Tuer-Gang", "nursery    - feed", "vortex_1   - bio_1", "vortex_2   - bio_2", "feed       liegt im Tuer-Gang")


DURCHGANG = 1000.0   # 900-mm-Tuer-Gang um die Becken-Kette herum (Westseite) + 100 mm Rasterreserve der Gangkarte (gemessen 11.11.: 900 endete bei r 3342)


def podest_quadrate():
    """[(name, [Ecken])] der Podeste je Linie (Kanten parallel zur Paar-Achse)."""
    pl = L.plaetze()
    out = []
    for ln in (1, 2):
        phi = PAAR[0] if ln == 1 else -PAAR[0]
        yaw = L.ACHSE_M + phi + 90.0 * (1 if phi >= 0 else -1)
        for t in ("vortex", "bio"):
            x, y = pl["%s_%d" % (t, ln)][:2]
            h = PODEST_HALB[t]
            out.append(("%s_%d" % (t, ln), L.G.rect_corners(x, y, 2 * h, 2 * h, yaw)))
    return out


def fehler():
    f, info, ringe = L.pruefen(L.plaetze())
    f = [e for e in f if not e.startswith(ERLAUBT)]
    pl = L.plaetze()
    nx, ny = pl["nursery"][:2]
    u = (math.cos(math.radians(L.TUER)), math.sin(math.radians(L.TUER)))
    for nm, q in podest_quadrate():
        if nm.endswith("_2"):   # Westlinie: Durchgang zwischen Anzuchtbecken und Podest
            d = L.pkt_poly((nx, ny), q) - NURSERY_R
            if d < DURCHGANG:
                f.append("%-10s Podest zum Anzuchtbecken %.0f mm (Durchgang Soll >= %.0f)" % (nm, d, DURCHGANG))
        for px, py in q:   # gerader Tuer-Gang ab der Tuer: Podest-Ecken ausserhalb des Streifens +-450
            quer, laengs = abs(-px * u[1] + py * u[0]), px * u[0] + py * u[1]
            if laengs > L.GANG_BIS_R and quer < L.GANG / 2 + 50.0:
                f.append("%-10s Podest-Ecke im Tuer-Gang (quer %.0f)" % (nm, quer)); break
    return f


def fuss_abstand():
    """Kleinster Abstand Anzuchtbecken-Huelle zu einer Innentisch-Fussplatte (mm)."""
    x, y, _, _ = L.plaetze()["nursery"]
    best = 1e9
    for az, *fuesse in INNENTISCH_FUESSE:
        for t, r in fuesse:
            a = math.radians(az)
            fx, fy = r * math.cos(a) - t * math.sin(a), r * math.sin(a) + t * math.cos(a)
            best = min(best, math.hypot(fx - x, fy - y) - NURSERY_R - FUSSPLATTE / 2 * math.sqrt(2))
    return best


def suchen():
    global PAAR
    best = None
    for phi in range(14, 80, 2):
        for r in range(2700, 5600, 50):
            PAAR = (float(phi), float(r)); setzen(paar=PAAR, sumpf=(0.0, 99999.0, 0.0), schlamm=(0.0, 99999.0))
            e = [x for x in fehler() if ("vortex" in x or "bio" in x) and "99999" not in x and "sump" not in x and "sludge" not in x]
            if not e:
                sc = abs(r - 3400) + 15 * abs(phi - 40)
                if best is None or sc < best[0]:
                    best = (sc, float(phi), float(r))
    print("Paar", best)
    paar = PAAR = (best[1], best[2])
    bs = None
    for phi in range(4, 80, 2):
        for r in range(2500, 5700, 50):
            for lang in range(0, 360, 15):
                setzen(paar=paar, sumpf=(float(phi), float(r), L.ACHSE_M + phi + lang), schlamm=(0.0, 99999.0))
                e = [x for x in fehler() if "sump" in x and "99999" not in x]
                if not e:
                    sc = abs(r - 4300) + 20 * abs(phi - 21)
                    if bs is None or sc < bs[0]:
                        bs = (sc, float(phi), float(r), L.ACHSE_M + phi + lang)
    print("Sumpf", bs)
    sumpf = bs[1:] if bs else (0.0, 99999.0, 0.0)
    bl = None
    for phi in range(4, 80, 2):
        for r in range(2700, 5650, 50):
            setzen(paar=paar, sumpf=sumpf, schlamm=(float(phi), float(r)))
            e = [x for x in fehler() if "sludge" in x]
            if not e:
                sc = -r + 10 * abs(phi - 30)
                if bl is None or sc < bl[0]:
                    bl = (sc, float(phi), float(r))
    print("Schlamm", bl)
    return paar, sumpf, (bl[1:] if bl else None)


def main():
    if "--suchen" in sys.argv:
        print(suchen())
        return 0
    yaw = setzen()
    f = fehler()
    pl = L.plaetze()
    for k, (x, y, phi, r) in sorted(pl.items()):
        print("%-14s phi %+6.1f  r %5.0f  ->  x %7.0f  y %7.0f" % (k, phi, r, x, y))
    vx = pl["vortex_1"]; bx = pl["bio_1"]
    print("Podest-Paar Linie 1: Mittenabstand %.0f mm (Kante an Kante bei %.0f), Paar-Richtung %.1f Grad" % (math.hypot(vx[0] - bx[0], vx[1] - bx[1]), PODEST_HALB["vortex"] + SPALT_PODEST + PODEST_HALB["bio"], yaw))
    print("Becken-Kette: Fischtank r %.0f | Anzucht Mitte r %.0f (Spalt %.0f) | Lebendfutter Mitte r %.0f (Spalt %.0f)" % (FISCH_HUELLE, r_n, SPALT_BECKEN, r_f, SPALT_BECKEN))
    print("Abstand Anzucht - Innentisch-Fussplatte: %.0f mm" % fuss_abstand())
    for e in f:
        print("FAIL", e)
    print("Fehler:", len(f))
    L.bild(pl, L.ring_rechtecke(), os.path.join(ROOT, "renders", "l4-anordnung.png"))
    if "--schreiben" in sys.argv:
        L.schreiben(pl)
        p = os.path.join(ROOT, "data", "oasis-lage.json")
        lage = json.load(open(p, encoding="utf-8"))
        for b in lage["bauteile"]:
            if b["id"] in ("vortex_1", "vortex_2", "bio_1", "bio_2"):
                lnr = 1 if b["id"].endswith("1") else 2
                b["bauplatz"]["drehung_grad"] = round(yaw if lnr == 1 else 2 * L.ACHSE_M - yaw + 180.0, 2)   # Podest-Kanten parallel zur Paar-Achse
                b["bauplatz"]["quelle"] = "L4 (D161): Podeste Kante an Kante, scripts/l4_anordnung.py"
            elif b["id"] == "luftpumpe":   # Notluftpumpe unter dem Podest Vortex 2 (D161 Punkt 3; 405 x 230 x 320 in 640 x 640 x 537 lichtem Raum)
                v2 = pl["vortex_2"]
                py = 2 * L.ACHSE_M - yaw   # Paar-Achse Linie 2 (von der Mittelachse weg)
                ox, oy = -235.0 * math.cos(math.radians(py)), -235.0 * math.sin(math.radians(py))   # an den Podestrand zur Gangseite (Pumpenkante 40 mm hinter der Podestkante = Innenkante Rahmen)
                b["bauplatz"].update(x_mm=round(v2[0] + ox, 1), y_mm=round(v2[1] + oy, 1), drehung_grad=round(py + 90.0, 2), quelle="L4 (D161): unter dem Podest Vortex 2, am Rand zur Gangseite")
            elif b.get("bauplatz", {}).get("quelle", "").startswith("L3"):
                b["bauplatz"]["quelle"] = "L4 (D161): scripts/l4_anordnung.py"
        lage["meta"]["l4"] = "11.11.2026 N-UNIFY-AUTOBAHN L4: Becken-Kette Wand an Wand, Filter-Podeste Kante an Kante (scripts/l4_anordnung.py, D161)"
        json.dump(lage, open(p, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    return 1 if f else 0


if __name__ == "__main__":
    sys.exit(main())
