"""Passungspruefung der NFT-Tische (W16, D18): reine Geometrie aus data/layout.json und data/components/nft_tisch.json (kein CAD-Lauf).
Tisch-KS: X tangential CCW, Y radial nach INNEN (Platzierung yaw = az + 90 Grad = OBJ-yaw). Je Ring stehen die Tische auf den Sektorachsen des Zehnecks (az0 + 36 Grad x i; aussen 8 Tische i = 0-3 und 6-9, mitte 6 Tische i = 0-2 und 7-9, innen 10 Tische, Sektoren wie die Beete in layout.json).
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
    return ((ap - y) * u[0] + x * t[0], (ap - y) * u[1] + x * t[1])          # X = Tangente (CCW), Y radial nach innen (proper rotation, yaw = az + 90)

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
    par = json.load(open(os.path.join(sc.ROOT, "data", "params.json"), encoding="utf-8"))
    bj = json.load(open(os.path.join(sc.ROOT, "data", "components", "ibc_beet.json"), encoding="utf-8"))["typen"]
    ish, osh = par["inner_bed_shift"]["value"], par["outer_bed_shift"]["value"]
    beds = []                                                      # W17: Beete nach Radialbudget (M7 verschiebt radial, Aussenbeete 800 x 2640 laut D29)
    for b in lay["ibc_beds"]:
        outer = "plants" in b
        f = (b["r"] - (osh if outer else ish)) / b["r"]
        nb = dict(b, cx=b["cx"] * f, cy=b["cy"] * f, r=b["r"] - (osh if outer else ish))
        if outer:
            nb.update(length=bj["aussen_800"]["laenge"], width=bj["aussen_800"]["breite"])
        beds.append(nb)
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
            if G["art"] == "portal":                               # Tischmitte auf der Beetmitte (Radialbudget: ap_c = Beetmitte nach Verschiebung)
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
            fpl = p["foot_plate"] / 2.0
            dpool = min(math.hypot(world(az, ap, x + dx, y + dy)[0] - pcx, world(az, ap, x + dx, y + dy)[1] - pcy) - rim for i in sect for (az, ap) in [tabs[i]] for (x, y) in G["legs"] for (dx, dy) in ((-fpl, -fpl), (fpl, -fpl), (fpl, fpl), (-fpl, fpl)))
            ck.eq(f"innen Fussplatten ausserhalb des Beckenrands (Aussenradius {rim:.0f}, Plattenkante, Becken exzentrisch: Abstand {dpool:.0f} mm >= 5)", 1 if dpool >= 5 else 0, 1)
    print(f"   Tische gesamt {total_tables} (Soll 24), Rinnen-Topfloecher gesamt {total_holes}")
    ck.eq(f"NFT-Topfloecher gesamt {total_holes} >= 459 (R15/D27: Mindestzahl NFT)", 1 if total_holes >= 459 else 0, 1)
    ck.eq(f"NFT-Topfloecher gesamt {total_holes} >= 580 (D32: Soll ca. 580 bei pitch {TG.rinne_pitch():g})", 1 if total_holes >= 580 else 0, 1)
    # (5) Laufwege radial (D28/D29): Portalrand = Beet-Halbbreite + leg_clearance + foot_plate; Rand Pool, Portale, Wand
    Gm, Ga = TG.geometry("mitte", p, d["typen"]["mitte"]), TG.geometry("aussen", p, d["typen"]["aussen"])
    half = lambda G: G["bed_w"] / 2.0 + p["leg_clearance"] + p["foot_plate"]
    wall_ap = 5706.0
    a_ = Gm["apc"] - half(Gm) - TG.pool_outer_r()
    b_ = (Ga["apc"] - half(Ga)) - (Gm["apc"] + half(Gm))
    c_ = wall_ap - (Ga["apc"] + half(Ga))
    ck.eq(f"Laufweg A Beckenrand (Aussenradius {TG.pool_outer_r():.0f}) - Innenportal ({Gm['apc'] - half(Gm):.0f}): {a_:.0f} mm >= 500 (Soll 600)", 1 if a_ >= 500 else 0, 1)
    Gi = TG.geometry("innen", p, d["typen"]["innen"])
    a_post = (Gm["apc"] - half(Gm)) - (Gi["ap_leg"] + p["foot_plate"] / 2.0)
    ck.eq(f"Laufweg A frei am Innenpfosten (Plattenaussenkante {Gi['ap_leg'] + p['foot_plate'] / 2.0:.0f} - Innenportal {Gm['apc'] - half(Gm):.0f}): {a_post:.0f} mm >= 500 (D29: nie unter 500; OBJ-Beete/Becken-Exzentrizitaet nicht eingerechnet)", 1 if a_post >= 500 else 0, 1)
    ck.eq(f"Laufweg B Innenportal (bis {Gm['apc'] + half(Gm):.0f}) - Aussenportal (ab {Ga['apc'] - half(Ga):.0f}): {b_:.0f} mm >= 500 (Soll 600)", 1 if b_ >= 500 else 0, 1)
    ck.eq(f"Wandluft Aussenportal (bis {Ga['apc'] + half(Ga):.0f}) - Domwand-Apothem {wall_ap:.0f}: {c_:.0f} mm >= 100 (Soll 218)", 1 if c_ >= 100 else 0, 1)
    ck.eq("Tische gesamt (innen 10 + mitte 6 + aussen 8)", total_tables, 24)
    return ck.done()

if __name__ == "__main__":
    sys.exit(main())
