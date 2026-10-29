"""Gemeinsame Geometrie der NFT-Tische (W16, D18): Reihen, Rinnenlaengen je Reihe, Portal-/Auslegerbock, Verteiler-/Sammelrohr-Linien.
Tisch-KS: X = Rinnenachse (tangential, CCW wie OBJ-yaw = Azimut + 90 Grad, +X = Sammelrohr/tiefes Ende), Y = radial nach INNEN (Richtung Kuppelmitte; mit yaw = Azimut + 90 Grad ist Y = Z x X), Z hoch; Ursprung = Tischmitte auf der Sektorachse (Beetmitte bzw. Poolmitte-Radius ap_c), Z = 0 Boden.
Wird von nft_tisch.py (Bau), rinnen_reihen.py (Rinnenvarianten) und check_nft_fit.py (Pruefung) benutzt."""
import json, math, os
import sc

T18 = math.tan(math.radians(18.0))
E_IN, E_OUT = 169.0, 79.0          # Ueberstand ueber das Rinnenende: Zulaufseite (Tuelle 29 + Schlauch 70 + Stutzen 45 + halbes Verteilerrohr 12,5 + Rohrwand-Aussen 12,5), Ablaufseite (Stutzen 34 + Sammelrohr D50: 54 + 25)

def bed_outer_w(typ):
    """Beet-Aussenbreite aus data/components/ibc_beet.json (einzige Quelle): aussen -> aussen_993 (breiteste), mitte -> innen_933."""
    d = json.load(open(os.path.join(sc.ROOT, "data", "components", "ibc_beet.json"), encoding="utf-8"))["typen"]
    return {"aussen": d["aussen_993"]["breite"], "mitte": d["innen_933"]["breite"]}.get(typ)

def pool_outer_r():
    """Aussenradius des Zentralpools: Wasserradius (layout.json pool.d/2) + Wandstaerke (data/params.json wall)."""
    lay = json.load(open(os.path.join(sc.ROOT, "data", "layout.json"), encoding="utf-8"))
    par = json.load(open(os.path.join(sc.ROOT, "data", "params.json"), encoding="utf-8"))
    return lay["pool"]["d"] / 2.0 + par["wall"]["value"]

def hole_plan(L, phi, pitch=250.0, margin=46.0):
    """Lochzahl und Versatz (shift) einer Rinne der Laenge L so, dass das Lochraster (relativ zur Rinnenmitte) die Phase phi mod pitch hat:
    Loch i bei x = shift + (i - (n-1)/2) x pitch. Zickzack: benachbarte Reihen haben phi 0 und pitch/2. Alle Loecher bleiben >= margin (Rippe 20 + Lochradius 26) vom Rinnenende."""
    best = None
    for n in range(int(L // pitch), 0, -1):
        base = (phi + (n - 1) * pitch / 2.0) % pitch          # shift mod pitch
        for sh in (base, base - pitch, base + pitch):
            ext = abs(sh) + (n - 1) * pitch / 2.0
            if ext <= L / 2.0 - margin and (best is None or abs(sh) < abs(best[1])):
                best = (n, sh) if best is None or n == best[0] else best
        if best:
            return best[0], round(best[1], 2)
    return 0, 0.0

def geometry(typ, p, T, pitch=250.0):
    """Reihen und Boecke eines Tischtyps aus den Tischparametern p (nft_tisch.json parameter) und Typ-Daten T."""
    n, rp, apc = T["n"], T["rinnen_abstand"], T["ap_c"]
    gap = p["corner_gap"]
    rows = []
    for k in range(n):
        y = (k - (n - 1) / 2.0) * rp
        ap = apc - y                                           # Y zeigt radial nach innen
        side = 2 * ap * T18
        L = round(side - 2 * gap - E_IN - E_OUT)
        nh, sh = hole_plan(L, 0.0 if k % 2 == 0 else pitch / 2.0, pitch)
        rows.append(dict(k=k, y=y, ap=ap, side=side, L=L, n_holes=nh, phase="ab"[k % 2], shift=sh, xc=(E_IN - E_OUT) / 2.0))
    Wt = (n - 1) * rp + 130
    bw = bed_outer_w(typ)
    zc, slope = T["z_rinne_mitte"], p["slope_pct"] / 100.0
    Lmin = min(r["L"] for r in rows)
    xb = [rows[0]["xc"] - (Lmin / 2.0 - p["bock_inset"]), rows[0]["xc"] + (Lmin / 2.0 - p["bock_inset"])]       # zwei Boecke innerhalb der kuerzesten Reihe
    G = dict(typ=typ, n=n, rp=rp, apc=apc, rows=rows, Wt=Wt, zc=zc, slope=slope, gap=gap, xb=xb, Lmin=Lmin, bed_w=bw)
    if bw:      # Portalbock: Beine ausserhalb der Beet-Aussenbreite
        yl = bw / 2.0 + p["leg_clearance"] + p["foot_plate"] / 2.0          # Abstand bis zur Fussplattenkante
        G.update(art="portal", legs=[(x, s * yl) for x in xb for s in (-1, 1)], yl=yl)
    else:       # innen: Ausleger ueber den Pool, Pfosten ausserhalb des Beckenrands
        ap_leg = pool_outer_r() + p["leg_clearance"] + p["foot_plate"] / 2.0
        yl = apc - ap_leg                                      # negativ: Pfosten ausserhalb (radial aussen = -Y)
        G.update(art="ausleger", legs=[(x, yl) for x in xb], yl=yl, ap_leg=ap_leg)
    return G

def rect_pts(x0, x1, y0, y1, step=25.0):
    """Randpunkte eines Rechtecks (Tisch-KS, Draufsicht)."""
    pts = []
    nx, ny = max(2, int((x1 - x0) / step)), max(2, int((y1 - y0) / step))
    for i in range(nx + 1):
        x = x0 + (x1 - x0) * i / nx
        pts += [(x, y0), (x, y1)]
    for j in range(ny + 1):
        y = y0 + (y1 - y0) * j / ny
        pts += [(x0, y), (x1, y)]
    return pts

def footprint_pts(G, p):
    """Punkte der Draufsicht-Umrisse aller Teile eines Tisches (Rinnen samt Kappen/Tuelle, Verteiler-/Sammelrohr, Beine mit Fussplatte)."""
    pts = []
    for r in G["rows"]:
        x0 = r["xc"] - r["L"] / 2.0 - 29.0 - 0.0
        x1 = r["xc"] + r["L"] / 2.0 + 34.0
        pts += rect_pts(x0, x1, r["y"] - 65, r["y"] + 65)
    t = T18
    y0, y1 = -G["Wt"] / 2.0 - 60, G["Wt"] / 2.0 + 60
    for sgn, rad in ((-1, 12.5), (1, 25.0)):           # Zulaufverteiler (-X), Sammelrohr (+X): Linien entlang der Sektorgrenze
        for k in range(int((y1 - y0) / 25) + 1):
            y = y0 + k * 25.0
            ap = G["apc"] - y
            xb = sgn * (ap * t - G["gap"])
            pts += [(xb - sgn * 2 * rad, y), (xb, y)]            # Aussenkante an der Grenzlinie, Rohrachse eine Rohrbreite innen
    fp = p["foot_plate"] / 2.0
    for (x, y) in G["legs"]:
        pts += rect_pts(x - fp, x + fp, y - fp, y + fp, 20.0)
    return pts
