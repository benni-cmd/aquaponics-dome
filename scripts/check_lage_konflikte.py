"""N-UNIFY-AUTOBAHN L2: Konflikte der Quell-Lage messen (D117: nur notieren, nicht verschieben).

Aufruf (Projektordner): python -I -X utf8 scripts/check_lage_konflikte.py [--md]
Liest wie scripts/check_lage_quelle.py viewer/instances.json + viewer/detail/<definition>.json (Fussabdruck = konvexe Huelle der Koerper-Boxen je
Instanz, Becken als Kreis aus dem Koerper). Misst:
  1. Ueberlappung (Koerper-Boxen je Koerper, nur bei gemeinsamem Hoehenbereich) zwischen den Teilen der Lage (Becken, Sumpf, Tanks mit Podest, Schlamm, Tische, Beete, Pumpen, Luft, Permakultur,
     Regentank, Schrank) - Paare mit Schnittflaeche > 0, Tiefe = kleinste Breite der Schnittflaeche.
  2. Tuer-Achse: Gang 900 mm (D29) von der Tuer (Az -72, Zehneck-Innenkante) bis zum Fischtank-Rand; welche Teile im Gang stehen.
  3. Engster Abstand zwischen Nachbarn je Paar unter 500 mm (Laufweg, D62) als Liste.
Exit 0 immer (Messung, kein Gate). Schreibt nichts.
"""
import math
import os
import sys

sys.argv = [sys.argv[0], "--ohne-bild"] + sys.argv[1:]
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_lage_quelle as C   # noqa: E402

DEFS = {   # Definition -> Kurzname, Kreis-Koerper (Becken) oder None
    "pool_zentral": ("Fischtank", "T5_Zentraltank"), "zweitbecken": ("Anzuchtbecken", "T6_Zweitbecken"), "becken_dritt_klein": ("Lebendfutter", "T14k_Wanne"),
    "sumpftank": ("Sumpftank", None), "sumpftank_spiegel": ("Sumpftank", None), "tank_klein": ("Vortex", "Tank"), "podest_vortex": ("Podest Vortex", None),
    "tank_gross": ("Biofilter", "Tank"), "tank_gross_t3": ("Biofilter", "Tank"), "podest_biofilter": ("Podest Biofilter", None),
    "schlamm_sammelbehaelter": ("Schlammsammler", None), "nft_tisch_innen": ("NFT innen", None), "nft_tisch_mitte": ("NFT mitte", None),
    "nft_tisch_aussen": ("NFT aussen", None), "ibc_beet_aussen_800": ("Beet aussen", None), "ibc_beet_innen_933": ("Beet mitte", None),
    "permakultur_modul": ("Permakultur", None), "geblaese_luft": ("Geblaese", None), "notluftpumpe": ("Notluftpumpe", None),
    "regentank_5m3": ("Regentank", None), "puffer_klein": ("Puffer klein", None), "schaltschrank": ("Schaltschrank", None),
    "aktivkohle_station": ("Aktivkohle-Station", None), "tauchpumpe_modul": ("Tauchpumpe", None),
}
# Teile, die im Grundriss ueber anderen stehen duerfen (Tisch ueber Beet = Portal, Tank auf Podest, Pumpe im Sumpf/Becken)
ERLAUBT = {frozenset(("NFT aussen", "Beet aussen")), frozenset(("NFT mitte", "Beet mitte")), frozenset(("Vortex", "Podest Vortex")),
           frozenset(("Biofilter", "Podest Biofilter")), frozenset(("Tauchpumpe", "Sumpftank"))}
TUER_AZ, GANG = -72.0, 900.0
MIN_TIEFE, MIN_FLAECHE = 20.0, 2000.0   # Rauschgrenze: Box-Naeherung duenner Profile (Beruehrung unter 20 mm Tiefe oder 20 cm2 Flaeche zaehlt nicht)
WAND_AP = 6000.0 * math.cos(math.radians(18))


def kreis_poly(cx, cy, r, n=72):
    return [(cx + r * math.cos(2 * math.pi * k / n), cy + r * math.sin(2 * math.pi * k / n)) for k in range(n)]


def area(p):
    return 0.5 * sum(p[i][0] * p[(i + 1) % len(p)][1] - p[(i + 1) % len(p)][0] * p[i][1] for i in range(len(p)))


def ccw(p):
    return p if area(p) >= 0 else p[::-1]


def clip(subj, clipp):
    """Sutherland-Hodgman: Schnitt zweier konvexer Polygone (gegen den Uhrzeigersinn)."""
    out = subj
    for i in range(len(clipp)):
        a, b = clipp[i], clipp[(i + 1) % len(clipp)]
        inp, out = out, []
        if not inp:
            break
        side = lambda q: (b[0] - a[0]) * (q[1] - a[1]) - (b[1] - a[1]) * (q[0] - a[0])
        for j in range(len(inp)):
            p, q = inp[j], inp[(j + 1) % len(inp)]
            sp, sq = side(p), side(q)
            if sp >= 0:
                out.append(p)
            if (sp >= 0) != (sq >= 0):
                t = sp / (sp - sq)
                out.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
    return out


def breite(poly):
    """kleinste Breite eines konvexen Polygons (Rotating calipers ueber die Kanten)."""
    best = 1e18
    for i in range(len(poly)):
        a, b = poly[i], poly[(i + 1) % len(poly)]
        L = math.hypot(b[0] - a[0], b[1] - a[1])
        if L < 1e-6:
            continue
        n = (-(b[1] - a[1]) / L, (b[0] - a[0]) / L)
        pr = [(q[0] - a[0]) * n[0] + (q[1] - a[1]) * n[1] for q in poly]
        best = min(best, max(pr) - min(pr))
    return best


def abstand(A, B):
    """kleinster Abstand zweier konvexer Polygone ohne Ueberlappung (Punkt-Kante)."""
    def pk(p, a, b):
        dx, dy = b[0] - a[0], b[1] - a[1]
        t = max(0.0, min(1.0, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / (dx * dx + dy * dy or 1)))
        return math.hypot(p[0] - a[0] - t * dx, p[1] - a[1] - t * dy)
    d = 1e18
    for P, Q in ((A, B), (B, A)):
        for p in P:
            for i in range(len(Q)):
                d = min(d, pk(p, Q[i], Q[(i + 1) % len(Q)]))
    return d


def koerper(i, kb):
    """[(Polygon, z_min, z_max)] je Koerper der Instanz (Box im lokalen Rahmen gedreht; Becken-Huelle als Kreis)."""
    m = i["m"]
    out = []
    for k in C.detail(i["d"]) or []:
        lo, hi = k["bbox"]["min"], k["bbox"]["max"]
        z0, z1 = lo[2] + m[11], hi[2] + m[11]
        if kb and (k["name"] == kb or abs((hi[0] - lo[0]) - (hi[1] - lo[1])) < 1.0):   # Becken: Huelle und runde Koerper (Wasser) als Kreis, nicht als Box (L4)
            cx, cy = C.xy(m, (lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2)
            out.append((ccw(kreis_poly(cx, cy, max(hi[0] - lo[0], hi[1] - lo[1]) / 2)), z0, z1))
        else:
            out.append((ccw([C.xy(m, u, v) for u, v in ((lo[0], lo[1]), (hi[0], lo[1]), (hi[0], hi[1]), (lo[0], hi[1]))]), z0, z1))
    return out


def teile():
    out, n = [], {}
    for i in C.INSTANCES:
        if i["d"] not in DEFS:
            continue
        name, kb = DEFS[i["d"]]
        ks = koerper(i, kb)
        if not ks:
            continue
        n[name] = n.get(name, 0) + 1
        h = C.hull([q for k in ks for q in k[0]])
        out.append({"name": "%s %d" % (name, n[name]), "art": name, "poly": ccw(h), "koerper": ks})
    return out


def schnitt(A, B):
    """groesste Schnitt-Tiefe (kleinste Breite) zweier Teile ueber alle Koerperpaare mit gemeinsamem Hoehenbereich; (Tiefe, Flaeche m2, z-Bereich) oder None."""
    best = None
    for pa, a0, a1 in A["koerper"]:
        for pb, b0, b1 in B["koerper"]:
            if min(a1, b1) - max(a0, b0) <= 1.0:
                continue
            s = clip(pa, pb)
            if len(s) >= 3 and area(s) > MIN_FLAECHE:
                w = breite(s)
                if w < MIN_TIEFE:
                    continue
                if best is None or w > best[0]:
                    best = (w, area(s) / 1e6, (max(a0, b0), min(a1, b1)))
    return best


def main():
    T = teile()
    ueber, eng = [], []
    for a in range(len(T)):
        for b in range(a + 1, len(T)):
            A, B = T[a], T[b]
            if frozenset((A["art"], B["art"])) in ERLAUBT or A["art"] == B["art"] == "Tauchpumpe":
                continue
            s = clip(A["poly"], B["poly"])
            if len(s) >= 3 and area(s) > 1.0:
                k = schnitt(A, B)
                if k:
                    ueber.append((k[0], k[1], A["name"], B["name"], k[2]))
            else:
                d = abstand(A["poly"], B["poly"])
                if d < 500.0 and "Tauchpumpe" not in (A["art"], B["art"]):
                    eng.append((d, A["name"], B["name"]))
    ueber.sort(reverse=True)
    eng.sort()
    # Tuer-Gang: Rechteck entlang Az -72 von r 2250 (Fischtank-Rand) bis zur Wand, Breite GANG
    u = (math.cos(math.radians(TUER_AZ)), math.sin(math.radians(TUER_AZ)))
    v = (-u[1], u[0])
    r0, r1 = 2250.0, WAND_AP
    gang = ccw([(u[0] * r + v[0] * s, u[1] * r + v[1] * s) for r, s in ((r0, -GANG / 2), (r1, -GANG / 2), (r1, GANG / 2), (r0, GANG / 2))])
    im_gang = []
    for t in T:
        s = clip(t["poly"], gang)
        if len(s) >= 3 and area(s) > 1.0:
            im_gang.append((t["name"], breite(s), area(s) / 1e6))
    md = "--md" in sys.argv
    print("Modellstand %s: %d Teile im Grundriss" % (C.I["built"], len(T)))
    print("1. Ueberlappungen im Grundriss (nicht erlaubt; Tiefe = kleinste Breite der Schnittflaeche): %d Paare" % len(ueber))
    for w, a_, x, y, z in ueber:
        print(("| %s | %s | %.0f mm | %.3f m2 | %.0f bis %.0f |" if md else "   %-20s x %-20s Tiefe %5.0f mm, Flaeche %.3f m2, Hoehe abs %.0f bis %.0f") % (x, y, w, a_, z[0], z[1]))
    print("2. Tuer-Gang 900 mm (Az -72, r 2250 bis %.0f): %d Teile im Gang" % (WAND_AP, len(im_gang)))
    for nm, w, a_ in im_gang:
        print("   %-20s Breite im Gang %4.0f mm, Flaeche %.2f m2" % (nm, w, a_))
    print("3. Abstand unter 500 mm zwischen Nachbarn (ohne Ueberlappung): %d Paare" % len(eng))
    for d, x, y in eng:
        print("   %-20s - %-20s %4.0f mm" % (x, y, d))
    return 0


if __name__ == "__main__":
    sys.exit(main())
