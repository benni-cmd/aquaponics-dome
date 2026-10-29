"""Passungspruefung der NFT-Tische (W16, D18): reine Geometrie aus data/layout.json und data/components/nft_tisch.json (kein CAD-Lauf).
Je Ring stehen die Tische auf den Sektorachsen des Zehnecks (az0 + 36 Grad x i; aussen 8 Tische i = 0-3 und 6-9, mitte 6 Tische i = 0-2 und 7-9, innen 10 Tische, Sektoren wie die Beete in layout.json).
Pruefungen: (1) Rinnenende samt Zulauf/Sammelrohr liegt >= corner_gap vor der Sektorgrenze je Reihe, (2) Footprints benachbarter Tische haben >= corner_gap Abstand, (3) Beine/Fussplatten liegen ausserhalb jedes Beet-Rechtecks (>= 30 mm),
(4) innen: Pfosten ausserhalb des Beckenrands (Aussenradius Pool + Abstand). Aufruf: python scripts/workshop/check_nft_fit.py   (exit 1 bei FAIL)"""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
import tisch_geom as TG

SECTORS = {"innen": list(range(10)), "mitte": [0, 1, 2, 7, 8, 9], "aussen": [0, 1, 2, 3, 6, 7, 8, 9]}
AZ0 = 5.3

def world(az_deg, ap, x, y):
    a = math.radians(az_deg)
    u, t = (math.cos(a), math.sin(a)), (-math.sin(a), math.cos(a))
    return ((ap + y) * u[0] + x * t[0], (ap + y) * u[1] + x * t[1])

def bed_dist(pt, bed):
    """vorzeichenbehafteter Abstand eines Punktes zum Beet-Rechteck (negativ = innen)."""
    a = math.radians(bed["yaw"])
    dx, dy = pt[0] - bed["cx"], pt[1] - bed["cy"]
    lx, ly = dx * math.cos(a) + dy * math.sin(a), -dx * math.sin(a) + dy * math.cos(a)
    ex, ey = abs(lx) - bed["length"] / 2.0, abs(ly) - bed["width"] / 2.0
    if ex <= 0 and ey <= 0:
        return max(ex, ey)
    return math.hypot(max(ex, 0), max(ey, 0))

def main():
    p, d = sc.load_params("nft_tisch")
    lay = json.load(open(os.path.join(sc.ROOT, "data", "layout.json"), encoding="utf-8"))
    beds = lay["ibc_beds"]
    pool = lay["pool"]
    pcx, pcy = pool["cx"], pool["cy"]
    ck = sc.Check("nft_fit")
    total_tables, total_holes = 0, 0
    for typ in ("innen", "mitte", "aussen"):
        T = d["typen"][typ]
        G = TG.geometry(typ, p, T)
        sect = SECTORS[typ]
        tabs = {}
        for i in sect:
            az = AZ0 + 36.0 * i
            ap = G["apc"]
            if G["art"] == "portal":                               # Tischmitte auf der Beetmitte (Radius des Beets auf der Sektorachse)
                b = min((b for b in beds if abs(b["r"] - G["apc"]) < 400), key=lambda b: abs(((b["az"] - az + 180) % 360) - 180))
                ap = b["r"] * math.cos(math.radians(b["az"] - az))
            tabs[i] = (az, ap)
        total_tables += len(sect)
        total_holes += sum(r["n_holes"] for r in G["rows"]) * len(sect)
        # (1) Rinnenlaenge je Reihe
        for r in G["rows"]:
            need = r["L"] + TG.E_IN + TG.E_OUT + 2 * G["gap"]
            ck.eq(f"{typ} Reihe {r['k'] + 1} (ap {r['ap']:.0f}): Rinne {r['L']} + Ueberstaende + 2 x {G['gap']:.0f} <= Zehneck-Seite {r['side']:.0f}", 1 if need <= r["side"] + 0.5 else 0, 1)
        # (2) Footprints benachbarter Tische
        fp = TG.footprint_pts(G, p)
        dmin_all = 1e9
        for i in sect:
            j = (i + 1) % 10
            if j not in tabs:
                continue
            A = [world(tabs[i][0], tabs[i][1], x, y) for (x, y) in fp]
            B = [world(tabs[j][0], tabs[j][1], x, y) for (x, y) in fp]
            dmin = min(math.hypot(a[0] - b[0], a[1] - b[1]) for a in A for b in B)
            dmin_all = min(dmin_all, dmin)
            ck.eq(f"{typ} Tisch {i}/{j}: Abstand der Footprints >= {G['gap']:.0f}", 1 if dmin >= G["gap"] else 0, 1)
        print(f"   {typ}: kleinster Footprint-Abstand {dmin_all:.0f} mm, Rinnenlaengen {[r['L'] for r in G['rows']]}, Loecher je Reihe {[r['n_holes'] for r in G['rows']]}")
        # (3) Beine ausserhalb der Beete
        dleg = 1e9
        for i in sect:
            az, ap = tabs[i]
            for (x, y) in G["legs"]:
                fpl = p["foot_plate"] / 2.0
                for (dx, dy) in ((-fpl, -fpl), (fpl, -fpl), (fpl, fpl), (-fpl, fpl), (0, 0)):
                    w = world(az, ap, x + dx, y + dy)
                    dleg = min(dleg, min(bed_dist(w, b) for b in beds))
        ck.eq(f"{typ} Beine/Fussplatten ausserhalb aller Beet-Rechtecke (kleinster Abstand {dleg:.0f} mm >= 30)", 1 if dleg >= 30 else 0, 1)
        # (4) innen: Pfosten ausserhalb des Pools
        if G["art"] == "ausleger":
            rim = TG.pool_outer_r()
            dpool = min(math.hypot(world(az, ap, x, y)[0] - pcx, world(az, ap, x, y)[1] - pcy) - rim for i in sect for (az, ap) in [tabs[i]] for (x, y) in G["legs"])
            ck.eq(f"innen Pfosten ausserhalb des Beckenrands (Aussenradius {rim:.0f}, Abstand {dpool:.0f} mm >= 30)", 1 if dpool >= 30 else 0, 1)
    print(f"   Tische gesamt {total_tables} (Soll 24), Rinnen-Topfloecher gesamt {total_holes}")
    ck.eq("Tische gesamt (innen 10 + mitte 6 + aussen 8)", total_tables, 24)
    return ck.done()

if __name__ == "__main__":
    sys.exit(main())
