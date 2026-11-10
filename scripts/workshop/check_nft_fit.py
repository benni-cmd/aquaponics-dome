"""Passungspruefung der NFT-Tische (W16, D18): reine Geometrie aus data/layout.json und data/components/nft_tisch.json (kein CAD-Lauf).
Tisch-KS: X tangential CCW, Y radial nach INNEN (Platzierung yaw = az + 90 Grad = OBJ-yaw). Je Ring stehen die Tische auf den Sektorachsen des Zehnecks (az0 + 36 Grad x i; aussen 8 Tische i = 0-3 und 6-9, mitte 6 Tische i = 0-2 und 7-9, innen 10 Tische, Sektoren wie die Beete in layout.json).
Pruefungen: (1) Rinnenende samt Zulauf/Sammelrohr liegt >= corner_gap vor der Sektorgrenze je Reihe, (2) Footprints benachbarter Tische haben >= corner_gap Abstand, (3) Beine/Fussplatten liegen ausserhalb jedes Beet-Rechtecks (>= 30 mm),
(4) innen: Pfosten ausserhalb des Beckenrands (Aussenradius Pool + Abstand). Aufruf: python scripts/workshop/check_nft_fit.py   (exit 1 bei FAIL)"""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sc
import tisch_geom as TG
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
import variante as V

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

def bed_poly(b, fase=0.0):
    """Eckpunkte des Beet-Umrisses (Rechteck, optional 45-Grad-Fasen der Schenkel fase) in Weltkoordinaten, gegen den Uhrzeigersinn."""
    a = math.radians(b["yaw"])
    hl, hw, c = b["length"] / 2.0, b["width"] / 2.0, fase
    loc = []
    for sx, sy in ((1, 1), (-1, 1), (-1, -1), (1, -1)):
        pair = [(sx * hl, sy * (hw - c)), (sx * (hl - c), sy * hw)] if sx * sy > 0 else [(sx * (hl - c), sy * hw), (sx * hl, sy * (hw - c))]
        loc += pair if c else pair[:1]
    return [(b["cx"] + x * math.cos(a) - y * math.sin(a), b["cy"] + x * math.sin(a) + y * math.cos(a)) for x, y in loc]

def sat_gap(P, Q):
    """Abstand zweier konvexer Polygone aus den Kantennormalen: > 0 = getrennt (Untergrenze des echten Abstands), < 0 = Eindringtiefe."""
    best = -1e9
    for poly in (P, Q):
        for k in range(len(poly)):
            ex, ey = poly[(k + 1) % len(poly)][0] - poly[k][0], poly[(k + 1) % len(poly)][1] - poly[k][1]
            n = math.hypot(ex, ey)
            nx, ny = ey / n, -ex / n
            pa = [x * nx + y * ny for x, y in P]
            pb = [x * nx + y * ny for x, y in Q]
            best = max(best, max(min(pb) - max(pa), min(pa) - max(pb)))
    return best

def dome_planes():
    """Feldebenen der Kuppelhaut (Ebene durch die drei Strebenachsen je Dreiecksfeld, Normale nach aussen): [(n, d)]; die Kuppel ist konvex, ein Punkt liegt innen, wenn d - n.p >= 0 fuer alle Felder."""
    lay = json.load(open(os.path.join(sc.ROOT, "data", "layout.json"), encoding="utf-8"))["dome"]
    N = lay["nodes_list"]
    hp = json.load(open(os.path.join(sc.ROOT, "data", "components", "haut_paneel.json"), encoding="utf-8"))
    out = []
    for f in hp["felder"]:
        P = [(N[n]["x"], N[n]["y"], N[n]["z"]) for n in f["nodes"]]
        u = [P[1][k] - P[0][k] for k in range(3)]
        v = [P[2][k] - P[0][k] for k in range(3)]
        n = [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]]
        L = math.sqrt(sum(c * c for c in n))
        n = [c / L for c in n]
        c = [sum(q[k] for q in P) / 3 for k in range(3)]
        if sum(n[k] * c[k] for k in range(3)) < 0:
            n = [-c_ for c_ in n]
        out.append((n, sum(n[k] * P[0][k] for k in range(3))))
    return out

def main(variant="aussen"):
    """variant: "aussen" (Standard seit D43, 4 Rinnen) oder "aussen3" (Alternative, 3 Rinnen): die Variante ersetzt den Typ "aussen" in d["typen"], alles andere bleibt."""
    p, d = sc.load_params("nft_tisch")
    d["typen"] = dict(d["typen"])
    if variant != "aussen":
        d["typen"]["aussen"] = d["typen"][variant]
    lay = json.load(open(os.path.join(sc.ROOT, "data", "layout.json"), encoding="utf-8"))
    bj = json.load(open(os.path.join(sc.ROOT, "data", "components", "ibc_beet.json"), encoding="utf-8"))["typen"]
    beds = []                                                      # D37 (30.10.): alle 14 Beete exakt auf der Sektorachse (Azimut 5,3 + 36 k), Apothem = ap_c, yaw = Azimut + 90; Aussenbeete 800 x 2640 (D29), Innenbeete 933 x 1865
    for typ_b, key in (("aussen", "aussen_800"), ("mitte", "innen_933")):
        ac = d["typen"][typ_b]["ap_c"]
        for i_ in SECTORS[typ_b]:
            az_ = AZ0 + 36.0 * i_
            a_ = math.radians(az_)
            beds.append(dict(cx=ac * math.cos(a_), cy=ac * math.sin(a_), yaw=az_ + 90.0, length=bj[key]["laenge"], width=bj[key]["breite"], fase=bj[key].get("fase", 0.0), r=ac, az=az_, ring=typ_b))
    gaps = []                                                      # (7) Beet x Beet: kein Beet dringt in ein Nachbarbeet ein (D44: Innenbeet-Ecken anfasen, Fase aus ibc_beet.json)
    for i_ in range(len(beds)):
        for j_ in range(i_ + 1, len(beds)):
            if math.hypot(beds[i_]["cx"] - beds[j_]["cx"], beds[i_]["cy"] - beds[j_]["cy"]) < 3500:
                gaps.append((sat_gap(bed_poly(beds[i_], beds[i_]["fase"]), bed_poly(beds[j_], beds[j_]["fase"])), beds[i_]["ring"], beds[j_]["ring"]))
    pool = lay["pool"]
    pcx, pcy = 0.0, 0.0                                            # D35: Becken zentriert (Ringe konzentrisch; layout.json cx/cy -36/20 ist OBJ-Ungenauigkeit)
    ck = sc.Check("nft_fit" if variant == "aussen" else f"nft_fit[{variant}]")
    g_mit = min([g for g, a_, b_ in gaps if a_ == b_ == "mitte"] or [1e9]); g_aus = min([g for g, a_, b_ in gaps if a_ == b_ == "aussen"] or [1e9])
    ck.eq(f"Innenbeete (mitte) Beet x Beet Abstand {g_mit:.0f} mm >= 0 (Fase {bj['innen_933'].get('fase', 0):g}, D44; ohne Fase -35)", 1 if g_mit >= 0 else 0, 1)
    ck.eq(f"Aussenbeete Beet x Beet Abstand {g_aus:.0f} mm >= 0", 1 if g_aus >= 0 else 0, 1)
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
                ap = G["apc"]                                          # Tischmitte = Beetmitte exakt (D37: Beete auf der Sektorachse)
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
            nom = 2 * G["gap"] * math.cos(math.radians(18.0))             # nominal: zwei Tische mit je corner_gap an der gemeinsamen Sektorgrenze (Grenze unter 18 Grad zur Achse)
            ck.eq(f"{typ} Tisch {i}/{j}: Abstand der Footprints {dmin:.0f} >= {nom - 2:.0f} (2 x corner_gap x cos 18 Grad = {nom:.0f})", 1 if dmin >= nom - 2.0 else 0, 1)
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
        ck.eq(f"{typ} Beine/Fussplatten ausserhalb aller Beet-Rechtecke (kleinster Abstand {dleg:.0f} mm >= 40, Soll leg_clearance {p['leg_clearance']:.0f})", 1 if dleg >= 40 else 0, 1)
        # (3b) Portal: aeusserste Rinnenkante (Mitte +- 65) bleibt >= 15 mm von der Beininnenflaeche (Rinne ragt nicht in die Beine; W24)
        if G["art"] == "portal":
            edge = max(abs(r["y"]) + 65 for r in G["rows"])
            leg_in = G["yl"] - p["leg_w"] / 2.0
            ck.eq(f"{typ} Rinnenkante {edge:.0f} (aeusserste Reihe Mitte + 65) <= Beininnenflaeche {leg_in:.0f} - 15 (Luft {leg_in - edge:.0f} mm)", 1 if edge <= leg_in - 15 else 0, 1)
        # (4) innen: Pfosten ausserhalb des Pools
        if G["art"] == "ausleger":
            rim = TG.pool_outer_r()
            fpl = p["foot_plate"] / 2.0
            def dpool_for(cx, cy):
                return min(math.hypot(world(az, ap, x + dx, y + dy)[0] - cx, world(az, ap, x + dx, y + dy)[1] - cy) - rim for i in sect for (az, ap) in [tabs[i]] for (x, y) in G["legs"] for (dx, dy) in ((-fpl, -fpl), (fpl, -fpl), (fpl, fpl), (-fpl, fpl)))
            dpool_b = dpool_for(pcx, pcy)                                 # D35: Becken zentriert
            ck.eq(f"innen Fussplatten ausserhalb des Beckenrands (Aussenradius {rim:.0f}, Plattenkante, Becken zentriert (D35): Abstand {dpool_b:.0f} mm >= 5)", 1 if dpool_b >= 5 else 0, 1)
            # D121 (U3): Kragarm ueber dem Poolrand: Unterkante des tiefsten Bocks >= Poolrand (Soll 1200, params.json pool_rim ring_b2) + 5 mm; die Rinne liegt nur 30 mm ueber dem Rand
            zrow_ = lambda x: G["zc"] - (x - G["rows"][0]["xc"]) * G["slope"]
            unten = min(zrow_(x) - T.get("holm_h", p["holm_h"]) for x in G["xb"])
            rand_ = V.parameter("ring_b2")["pool_rim"]
            ck.eq(f"innen Kragarm-Unterkante {unten:.1f} >= Poolrand {rand_} + 5 mm (D121; Holm {T.get('holm_h', p['holm_h'])} hoch, Rinnenunterkante {G['zc']})", 1 if unten >= rand_ + 5 else 0, 1)
    # (6) Abstand der Tischkanten zur Kuppelhaut (W23-Befund 2): Rinnenenden (Oberkante Rinne = Boden + 100) und Beine gegen die Feldebenen (Strebenachsen), >= 15 mm (halbes Strebenrohr)
    planes = dome_planes()
    clr = lambda q: min(dd - (n[0] * q[0] + n[1] * q[1] + n[2] * q[2]) for n, dd in planes)
    for typ in ("aussen", "mitte", "innen"):
        G = TG.geometry(typ, p, d["typen"][typ])
        zr = lambda x: G["zc"] - (x - G["rows"][0]["xc"]) * G["slope"]
        worst = (1e9, "")
        for i in SECTORS[typ]:
            az = AZ0 + 36.0 * i
            pts = []
            for r in G["rows"]:
                for x in (r["xc"] - r["L"] / 2 - TG.E_IN, r["xc"] + r["L"] / 2 + TG.E_OUT):
                    for dy in (-65, 65):
                        pts.append((x, r["y"] + dy, zr(x) + 100, f"Rinnenende Reihe {r['k'] + 1} x {x:.0f}"))
            for (x, y) in G["legs"]:
                for dx in (-20, 20):
                    for dy in (-20, 20):
                        pts.append((x + dx, y + dy, zr(x), f"Bein x {x:.0f} y {y:.0f}"))
            for (x, y, z, nm) in pts:
                w = world(az, G["apc"], x, y)
                c = clr((w[0], w[1], z))
                if c < worst[0]:
                    worst = (c, f"Sektor {i}, {nm}")
        ck.eq(f"{typ} Abstand der Tischkanten zur Kuppelhaut {worst[0]:.0f} mm >= 15 ({worst[1]})", 1 if worst[0] >= 15 else 0, 1)
    print(f"   Tische gesamt {total_tables} (Soll 24), Rinnen-Topfloecher gesamt {total_holes}")
    ck.eq(f"NFT-Topfloecher gesamt {total_holes} >= 459 (R15/D27: Mindestzahl NFT)", 1 if total_holes >= 459 else 0, 1)
    thr = 654 if d["typen"]["aussen"]["n"] == 4 else 563
    ck.eq(f"NFT-Topfloecher gesamt {total_holes} >= {thr} (D32/D43: Soll 674 mit 4 Aussenrinnen, 570 mit 3 (Soll ca. 580 bei pitch {TG.rinne_pitch():g}), Toleranz 3 %)", 1 if total_holes >= thr else 0, 1)
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
    ck.eq(f"Laufweg A frei am Innenpfosten (Plattenaussenkante {Gi['ap_leg'] + p['foot_plate'] / 2.0:.0f} - Innenportal {Gm['apc'] - half(Gm):.0f}): {a_post:.0f} mm >= 500 (D29: nie unter 500; Becken zentriert, D35)", 1 if a_post >= 500 else 0, 1)
    ck.eq(f"Laufweg B Innenportal (bis {Gm['apc'] + half(Gm):.0f}) - Aussenportal (ab {Ga['apc'] - half(Ga):.0f}): {b_:.0f} mm >= 500 (Soll 600)", 1 if b_ >= 500 else 0, 1)
    ck.eq(f"Wandluft Aussenportal (bis {Ga['apc'] + half(Ga):.0f}) - Domwand-Apothem {wall_ap:.0f}: {c_:.0f} mm >= 100 (Soll 218)", 1 if c_ >= 100 else 0, 1)
    ck.eq("Tische gesamt (innen 10 + mitte 6 + aussen 8)", total_tables, 24)
    reach = min(r["ap"] for r in [max(Ga["rows"], key=lambda r: r["ap"])]) - (Ga["apc"] - half(Ga))          # entfernteste Reihenmitte (aeusserste Reihe) vom inneren Portalrand, Laufweg-B-Seite
    print(f"   Variante {variant}: Rinnen {len(Ga['rows']) * 8} aussen, Rinnenlaenge aussen je Tisch {sum(r['L'] for r in Ga['rows'])} mm, Tischbreite Rinnenband {Ga['Wt']:.0f}, entfernteste Reihe vom Laufweg B {reach:.0f} mm")
    return ck.done()

if __name__ == "__main__":
    rc = 0
    for v in ("aussen", "aussen3"):
        rc |= main(v)
    sys.exit(rc)
