"""N-UNIFY-AUTOBAHN U1: Lage-Probe. Passt die Soll-Lage der Quelle (um 18 Grad gedreht, `data/oasis-soll.json`) in die gebaute Kuppel?

Aufruf (Projektordner):
  python -I -X utf8 scripts/oasis_lagepruefung.py             rechnet und schreibt data/oasis-lage.json
  python -I -X utf8 scripts/oasis_lagepruefung.py --pruefen   rechnet neu, prueft die Abnahme (Exit 0/1) und dass die Datei aktuell ist

Eingabe: data/oasis-soll.json (nie von Hand aendern), viewer/instances.json (Instanz-Matrizen, Stand im Feld `built`),
         viewer/detail/<komponente>.json (Koerper-Boxen, nur lesen).
Annahme zur Reihenfolge: gerechnet wird NACH dem Entfernen der Ist-Teile aus Paket Abschnitt C (Absetzer, Biofilter-Tanks, Pumpen,
Feinfilter, Pegelschacht, Schlammfass, Zweit-/Drittbecken, Gebl. aussen). Bleibende Hindernisse: Tische, Beete (+115 Portal), Ring-Stelzen,
Puffer klein, Pool-Huelle, Schaltschrank und Aktivkohle-Station (beide ausserhalb), Sockel/Zehneck-Wand.

Regeln (jede mit Quelle im Kopf von `constraints`):
  Luft 150 mm zwischen Fussabdruecken, die sich in Z beruehren oder ueberlappen · Wandluft 100 mm zur Zehneck-Innenkante (Apothema 5706, D29)
  · Kuppelkugel 5800 mm (Aufgabe U1; Knoten liegen auf r 6000, Streben/Knoten 200 mm tief) auch in der Hoehe (Kopffreiheit)
  · Tuer-Gang 900 mm breit von der Tuer (Az -72) bis zum Zentralpool (D29) · Laufweg 500 mm: Flutung von der Tuer (wie check_walkways_voll.py).
Suche: je Teil der erste regelkonforme Platz in aufsteigender Verschiebung gegen die gedrehte Zeichnung (Raster 50 mm bis 750 mm, D99; darueber 100 mm bis 3600 mm),
vier Reihenfolgen, die beste zaehlt. Teile ohne Platz in der Kuppel gehen als Vorbau nach aussen (D109), ebenso Teile, die den Zugang ueber 500-mm-Gaenge abschnueren;
Verschiebungen ueber 750 mm tragen D110, Einbauten (Pumpen, Schwimmer im Wirt) D108. `--ohne a,b` rechnet ohne bleibende Hindernisse (Vergleich, schreibt nichts); `--bild <pfad>` zeichnet.
"""
import json
import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOLL = os.path.join(ROOT, "data", "oasis-soll.json")
INST = os.path.join(ROOT, "viewer", "instances.json")   # seit U7 (D141) ein Kreislauf
DETAIL = os.path.join(ROOT, "viewer", "detail")
OUT = os.path.join(ROOT, "data", "oasis-lage.json")

FLOOR = 400.0            # D94: Fussboden der Quelle = Modell-Z 400
GAP = 150.0              # Aufgabe U1: Luft zwischen Koerpern
WALL_GAP = 100.0         # D29 Wandluft
APOTHEM = 6000.0 * math.cos(math.radians(18))   # Zehneck-Innenkante, wie check_walkways_voll.py (AP)
SOCKEL_APOTHEM = APOTHEM + 250.0                # Sockel aussen (sock_w 250, Detail fundamentring: Umkreis 6250)
DOME_R = 5800.0          # Aufgabe U1: Kuppelinnenraum
DOOR_AZ = -72.0          # params door_edge_az
DOOR_W = 1000.0          # params door_w
CORRIDOR_W = 900.0       # D29 Tuer-Gang
POOL_R_OUT = 2095.0      # viewer/detail/pool_zentral.json T5_Zentraltank (Huelle aussen)
MAX_SHIFT = 750.0        # D99
GRID = 50.0
SEARCH_MAX = 3600.0      # Suche ueber 750 mm hinaus (Raster dort 100 mm)
CELL = 50                # Laufwegraster wie check_walkways_voll.py
FOOT_PODEST = 50.0       # [A] Podest steht je Seite 50 mm ueber dem Tank (U2 baut `podest_*`)


# ---------------------------------------------------------------- Geometrie
def rot(x, y, deg):
    c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    return x * c - y * s, x * s + y * c


def rect(cx, cy, x0, y0, x1, y1, yaw):
    """Rechteck mit lokalen Grenzen (x0..x1, y0..y1), gedreht um yaw, verschoben nach (cx, cy)."""
    pts = []
    for u, v in ((x0, y0), (x1, y0), (x1, y1), (x0, y1)):
        a, b = rot(u, v, yaw)
        pts.append((cx + a, cy + b))
    return ("p", pts)


def circle(cx, cy, r):
    return ("c", cx, cy, r)


def bbox(sh):
    if sh[0] == "c":
        return sh[1] - sh[3], sh[2] - sh[3], sh[1] + sh[3], sh[2] + sh[3]
    xs = [p[0] for p in sh[1]]
    ys = [p[1] for p in sh[1]]
    return min(xs), min(ys), max(xs), max(ys)


def pts_of(sh):
    return sh[1] if sh[0] == "p" else [(sh[1], sh[2])]


def seg_dist(p, a, b):
    ax, ay = a
    bx, by = b
    dx, dy = bx - ax, by - ay
    L = dx * dx + dy * dy
    t = 0.0 if L == 0 else max(0.0, min(1.0, ((p[0] - ax) * dx + (p[1] - ay) * dy) / L))
    return math.hypot(p[0] - ax - t * dx, p[1] - ay - t * dy)


def pt_in_poly(p, pg):
    s = 0
    for i in range(len(pg)):
        a, b = pg[i], pg[(i + 1) % len(pg)]
        v = (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0])
        s |= 1 if v >= 0 else 2
    return s != 3


def pt_poly_dist(p, pg):
    if pt_in_poly(p, pg):
        return 0.0
    return min(seg_dist(p, pg[i], pg[(i + 1) % len(pg)]) for i in range(len(pg)))


def poly_poly_dist(A, B):
    """Abstand zweier konvexer Polygone, 0 bei Ueberlappung."""
    for P, Q in ((A, B), (B, A)):   # Trennachsen-Test
        for i in range(len(P)):
            a, b = P[i], P[(i + 1) % len(P)]
            nx, ny = b[1] - a[1], a[0] - b[0]
            pa = [nx * q[0] + ny * q[1] for q in P]
            qa = [nx * q[0] + ny * q[1] for q in Q]
            if max(pa) < min(qa) or max(qa) < min(pa):
                break
        else:
            continue
        break
    else:
        return 0.0
    d = min(seg_dist(p, B[i], B[(i + 1) % len(B)]) for p in A for i in range(len(B)))
    return min(d, min(seg_dist(p, A[i], A[(i + 1) % len(A)]) for p in B for i in range(len(A))))


def dist(a, b, cap=1e4):
    """Abstand zweier Formen (Kreis oder konvexes Polygon), 0 bei Ueberlappung; ab `cap` genuegt eine Untergrenze (schneller)."""
    ba, bb = bbox(a), bbox(b)
    gx = max(ba[0] - bb[2], bb[0] - ba[2], 0.0)
    gy = max(ba[1] - bb[3], bb[1] - ba[3], 0.0)
    lower = math.hypot(gx, gy)
    if lower >= cap:
        return lower
    if a[0] == "c" and b[0] == "c":
        return max(0.0, math.hypot(a[1] - b[1], a[2] - b[2]) - a[3] - b[3])
    if a[0] == "c":
        return max(0.0, pt_poly_dist((a[1], a[2]), b[1]) - a[3])
    if b[0] == "c":
        return max(0.0, pt_poly_dist((b[1], b[2]), a[1]) - b[3])
    return poly_poly_dist(a[1], b[1])


def hull(points):
    pts = sorted(set((round(x, 3), round(y, 3)) for x, y in points))
    if len(pts) < 3:
        return pts

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
    lo, up = [], []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    for p in reversed(pts):
        while len(up) >= 2 and cross(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


def az_r(x, y):
    return math.degrees(math.atan2(y, x)), math.hypot(x, y)


def wall_normals():
    return [(math.cos(math.radians(DOOR_AZ + 36 * k)), math.sin(math.radians(DOOR_AZ + 36 * k))) for k in range(10)]


NORMALS = wall_normals()
DOOR_DIR = (math.cos(math.radians(DOOR_AZ)), math.sin(math.radians(DOOR_AZ)))


def decagon(apothem):
    R = apothem / math.cos(math.radians(18))
    return ("p", [(R * math.cos(math.radians(DOOR_AZ + 18 + 36 * k)), R * math.sin(math.radians(DOOR_AZ + 18 + 36 * k))) for k in range(10)])


# ---------------------------------------------------------------- Eingaben
def load_json(p):
    return json.load(open(p, encoding="utf-8"))


SOLL_DATA = load_json(SOLL)
INST_DATA = load_json(INST)
INSTANCES = INST_DATA["instances"]
_detail_cache = {}


def detail_bodies(comp):
    if comp not in _detail_cache:
        p = os.path.join(DETAIL, comp + ".json")
        _detail_cache[comp] = load_json(p)["koerper"] if os.path.exists(p) else None
    return _detail_cache[comp]


def body_box(comp, name_part=None):
    """(xmin, ymin, zmin, xmax, ymax, zmax) lokal aus den Koerper-Boxen (alle oder nur Namen mit name_part)."""
    ks = detail_bodies(comp)
    if ks is None:
        return None
    ks = [k for k in ks if name_part is None or name_part in k["name"]]
    return tuple([min(k["bbox"]["min"][i] for k in ks) for i in range(3)] + [max(k["bbox"]["max"][i] for k in ks) for i in range(3)])


def inst_list(defn):
    return [i for i in INSTANCES if i["d"] == defn]


def inst_hull(i, extra=0.0):
    """konvexe Huelle aller Koerper-Boxen einer Instanz (XY, Modellkoordinaten) und Z-Bereich absolut."""
    ks = detail_bodies(i["d"])
    m = i["m"]
    pts, z0, z1 = [], 1e9, -1e9
    for k in ks:
        lo, hi = k["bbox"]["min"], k["bbox"]["max"]
        for u in (lo[0], hi[0]):
            for v in (lo[1], hi[1]):
                pts.append((m[0] * u + m[1] * v + m[3], m[4] * u + m[5] * v + m[7]))
        z0, z1 = min(z0, m[11] + lo[2]), max(z1, m[11] + hi[2])
    h = hull(pts)
    if extra:
        cx = sum(p[0] for p in h) / len(h)
        cy = sum(p[1] for p in h) / len(h)
        h = [(p[0] + extra * (p[0] - cx) / max(1e-9, math.hypot(p[0] - cx, p[1] - cy)), p[1] + extra * (p[1] - cy) / max(1e-9, math.hypot(p[0] - cx, p[1] - cy))) for p in h]
    return ("p", h), z0, z1


def yaw_of(i):
    return math.degrees(math.atan2(i["m"][4], i["m"][0]))


def solid(name, shape, z0, z1, **kw):
    d = dict(name=name, shape=shape, z0=z0, z1=z1, walkable=False, aussen=False)
    d.update(kw)
    return d


def build_obstacles():
    """Bleibende Hindernisse (nach dem Entfernen der Teile aus Paket Abschnitt C)."""
    obs = []
    for defn in ("nft_tisch_aussen", "nft_tisch_mitte", "nft_tisch_innen"):
        for n, i in enumerate(inst_list(defn)):
            sh, z0, z1 = inst_hull(i)
            obs.append(solid("%s:%d" % (defn, n + 1), sh, z0, z1, quelle=defn))
    for defn, l_pad in (("ibc_beet_aussen_800", 115.0), ("ibc_beet_innen_933", 115.0)):   # Portal = Beet + 115 je Seite (D54)
        b = body_box(defn)
        for n, i in enumerate(inst_list(defn)):
            sh = rect(i["m"][3], i["m"][7], b[0], b[1] - l_pad, b[3], b[4] + l_pad, yaw_of(i))
            obs.append(solid("%s:%d" % (defn, n + 1), sh, i["m"][11] + b[2], i["m"][11] + 1500 - 400 + 400, quelle=defn))
    for n, i in enumerate(inst_list("ringstuetze_d75_b")):   # 200 x 200 Fussplatte und Pfosten bis 2100 (check_walkways_voll.py)
        obs.append(solid("ringstuetze_d75_b:%d" % (n + 1), rect(i["m"][3], i["m"][7], -100, -100, 100, 100, yaw_of(i)), FLOOR, FLOOR + 2100, quelle="ringstuetze_d75_b"))
    for n, i in enumerate(inst_list("puffer_klein")):
        sh, z0, z1 = inst_hull(i)
        obs.append(solid("puffer_klein:%d" % (n + 1), sh, z0, z1, quelle="puffer_klein"))
    obs.append(solid("pool_huelle", circle(0.0, 0.0, POOL_R_OUT), FLOOR - 1200, FLOOR + 1200, quelle="pool_zentral (T5_Zentraltank, Radius 2095)"))
    for n, i in enumerate(inst_list("aktivkohle_station")):
        sh, z0, z1 = inst_hull(i)
        obs.append(solid("aktivkohle_station:%d" % (n + 1), sh, z0, z1, aussen=True, quelle="aktivkohle_station (r 7906)"))
    # Schaltschrank aussen (params technik_x/technik_y, cab 800 x 500 x 1200; Rueckwand tangential)
    obs.append(solid("schaltschrank", rect(500.0, -6490.0, -400, -250, 400, 250, -85.6 + 90), FLOOR, FLOOR + 1200, aussen=True, quelle="params technik_x/technik_y, cab_x/cab_y/cab_z"))
    return obs


# ---------------------------------------------------------------- Soll-Teile
SOLL_BY_ID = {b["id"]: b for b in SOLL_DATA["bauteile"]}
IN_SCOPE = [b["id"] for b in SOLL_DATA["bauteile"] if b["im_umfang"]]


def nominal(bid):
    """Mittelpunkt in der gedrehten Zeichnung (Modellkoordinaten): Primitive, sonst Symbol."""
    L = SOLL_BY_ID[bid]["lage"]
    if "mittelpunkt_x_mm" in L:
        return L["mittelpunkt_x_mm"], L["mittelpunkt_y_mm"]
    return None


def prim(bid, typ):
    for p in SOLL_BY_ID[bid]["lage"].get("zeichnung_primitive", []):
        if p.get("typ") == typ:
            return p
    return None


def symbol(bid, typ=None):
    for s in SOLL_BY_ID[bid]["lage"].get("symbole", []):
        if typ is None or s.get("typ") == typ:
            return s
    return None


TANK_K = body_box("tank_klein")     # Vortex = vorhandener Behaelter (D100)
TANK_G = body_box("tank_gross")     # Biofilter = vorhandener Behaelter (D100)
BLOWER = body_box("geblaese_luft")  # Belueftungsanlage: vorhandenes Gebl. (D103)
PODEST_V = 1900 - 1323   # D100: Vortex-Ueberlauf (Leitrohr-Oberkante 1323) auf Soll-Wasserspiegel 1900
PODEST_B = 1800 - 1570   # D100: Biofilter-Ueberlauf gebaut 1570 auf Soll-Wasserspiegel 1800


def aim(frm, to):
    return math.degrees(math.atan2(to[1] - frm[1], to[0] - frm[0]))


def spec_for(bid, soll_pos):
    d = _spec_for(bid, soll_pos)
    if d is not None and "rectspec" in d:
        rs, y0 = d["rectspec"], d["yaw"]
        d["fn"] = lambda c, yw=None, rs=rs, y0=y0: rect(c[0], c[1], rs[0], rs[1], rs[2], rs[3], y0 if yw is None else yw)
        d.setdefault("yaw_range", 30.0)
    elif d is not None:
        d.setdefault("yaw_range", 0.0)
        if d.get("fn") is not None:
            f0 = d["fn"]
            d["fn"] = lambda c, yw=None, f0=f0: f0(c)
    return d


def _spec_for(bid, soll_pos):
    """Fussabdruck (Funktion Mittelpunkt -> Form), Z-Bereich absolut, Gruppe, Drehung. None = Teil ohne eigene Standflaeche."""
    L = SOLL_BY_ID[bid]
    nom = soll_pos
    if bid in ("nursery", "feed"):
        r_in = 1000.0 if bid == "nursery" else 500.0
        r = r_in + 60.0       # [A] Wand/Rand 60 mm wie `zweitbecken` (Aussen 1867 bei innen 1747)
        yaw = aim(nom, (0.0, 0.0))   # Ueberlauf zeigt zur Mitte (Kette von aussen nach innen, A13)
        return dict(gruppe="frei", fn=lambda c, r=r: circle(c[0], c[1], r), z0=FLOOR, z1=FLOOR + 1000, yaw=yaw, z_bauplatz=FLOOR,
                    mass="Kreis Aussen %d mm (Innen %d + 60)" % (2 * r, 2 * r_in))
    if bid.startswith("vortex"):
        line = bid[-1]
        tgt = nominal("bio_" + line)
        yaw = aim(nom, tgt)
        b = TANK_K
        x0, x1 = min(b[0], -(344 + FOOT_PODEST)), max(b[3], 344 + FOOT_PODEST)
        y0, y1 = min(b[1], -(344 + FOOT_PODEST)), max(b[4], 344 + FOOT_PODEST)
        return dict(gruppe="frei", rectspec=(x0, y0, x1, y1), z0=FLOOR, z1=FLOOR + PODEST_V + b[5],
                    yaw=yaw, z_bauplatz=FLOOR + PODEST_V, mass="Box %d x %d (Tank %d + Stutzen + Podest %d)" % (x1 - x0, y1 - y0, 2 * 344, PODEST_V))
    if bid.startswith("bio"):
        line = bid[-1]
        yaw = aim(nom, (0.0, 0.0))
        b = TANK_G
        x0, x1 = min(b[0], -(465 + FOOT_PODEST)), max(b[3], 465 + FOOT_PODEST)
        y0, y1 = min(b[1], -(465 + FOOT_PODEST)), max(b[4], 465 + FOOT_PODEST)
        return dict(gruppe="frei", rectspec=(x0, y0, x1, y1), z0=FLOOR, z1=FLOOR + PODEST_B + b[5],
                    yaw=yaw, z_bauplatz=FLOOR + PODEST_B, mass="Box %d x %d (Tank %d + Stutzen + Podest %d)" % (x1 - x0, y1 - y0, 2 * 465, PODEST_B))
    if bid.startswith("sludge"):
        return dict(gruppe="frei", fn=lambda c: circle(c[0], c[1], 450.0), z0=FLOOR, z1=FLOOR + 900, yaw=0.0, z_bauplatz=FLOOR,
                    mass="Kreis 900 mm (Sammelbehaelter 350 l [A], Quelle zeichnet 900)")
    if bid.startswith("hauptpumpe") or bid.startswith("schwimmer"):   # liegen in der Zeichnung im Rechteck des Sumpfs
        zb = FLOOR - 500 if bid.startswith("hauptpumpe") else FLOOR + (-110)   # Pumpe auf dem Sumpfboden; Schwimmer am Hochstand -110
        return dict(gruppe="einbau", host="sump_" + bid[-1], fn=None, z0=zb, z1=zb + 300, yaw=0.0, z_bauplatz=zb,
                    mass="Kreis 275 mm (Quelle)" if bid.startswith("hauptpumpe") else "Punkt (Schwimmerschalter)")
    if bid.startswith("sump"):
        p = prim(bid, "rechteck")
        return dict(gruppe="frei", rectspec=(-1487.5, -562.5, 1487.5, 562.5), yaw_range=15.0, z0=FLOOR - 500, z1=FLOOR, yaw=108.0, z_bauplatz=FLOOR - 500,
                    walkable=True, mass="Rechteck 2975 x 1125 (Quelle, massstaeblich), im Boden -500..0")
    if bid in ("luftpumpe_1", "luftpumpe_2"):
        b = BLOWER
        yaw = aim(nom, (0.0, 0.0))
        return dict(gruppe="frei", rectspec=(b[0], b[1], b[3], b[4]), z0=FLOOR, z1=FLOOR + b[5], yaw=yaw, z_bauplatz=FLOOR,
                    innen=True, mass="Box %d x %d (geblaese_luft)" % (b[3] - b[0], b[4] - b[1]))
    if bid == "luftpumpe":
        yaw = aim(nom, (0.0, 0.0))
        return dict(gruppe="frei", rectspec=(-150, -125, 150, 125), z0=FLOOR, z1=FLOOR + 250, yaw=yaw, z_bauplatz=FLOOR,
                    innen=True, mass="Box 300 x 250 [A] (Notluftpumpe, Luftstein im Fischtank)")
    if bid in ("permakultur", "rain", "tap"):
        p = prim(bid, "rechteck")
        w, h = p["breite_mm"], p["hoehe_mm"]
        return dict(gruppe="aussen", rectspec=(-w / 2, -h / 2, w / 2, h / 2), z0=FLOOR, z1=FLOOR + 1500, yaw=18.0, z_bauplatz=FLOOR,
                    aussen=True, mass="Platzhalter %d x %d (Quelle, schematisch)" % (w, h))
    if bid in ("filterpumpe_1", "filterpumpe_2"):   # D102: Tauchpumpe im Fischtank; Quelle zeichnet sie am Tank (r 2662)
        return dict(gruppe="einbau", host="fish", fn=None, z0=FLOOR - 1000, z1=FLOOR - 600, yaw=0.0, z_bauplatz=FLOOR - 1000, mass="Kreis 275 mm (Quelle)")
    if bid in ("venturi_1", "venturi_2"):
        return dict(gruppe="frei", fn=lambda c: circle(c[0], c[1], 150.0), z0=FLOOR + 700, z1=FLOOR + 1300, yaw=0.0, z_bauplatz=FLOOR + 1250,
                    mass="Kreis 300 mm [A] (Injektor im Druckrohr, Hoehe Rand Fischtank)")
    if bid == "nachspeise":
        return dict(gruppe="frei", fn=lambda c: circle(c[0], c[1], 150.0), z0=FLOOR + 800, z1=FLOOR + 1400, yaw=0.0, z_bauplatz=FLOOR + 750,
                    mass="Kreis 300 mm [A] (Schwimmerventil am Rand des Fischtanks, Rand 1200 ueber Flur, steht nicht auf dem Boden)")
    return None


# ---------------------------------------------------------------- Regeln je Lage
def extent(sh, n):
    if sh[0] == "c":
        return n[0] * sh[1] + n[1] * sh[2] + sh[3]
    return max(n[0] * p[0] + n[1] * p[1] for p in sh[1])


def rmax(sh):
    if sh[0] == "c":
        return math.hypot(sh[1], sh[2]) + sh[3]
    return max(math.hypot(*p) for p in sh[1])


CORRIDOR = rect(0.0, 0.0, POOL_R_OUT, -CORRIDOR_W / 2, APOTHEM, CORRIDOR_W / 2, DOOR_AZ)               # Tuer-Gang innen (D29)
FORECOURT = rect(0.0, 0.0, SOCKEL_APOTHEM, -CORRIDOR_W / 2, SOCKEL_APOTHEM + 1500, CORRIDOR_W / 2, DOOR_AZ)   # [A] Tuer-Vorplatz aussen 900 x 1500
SOCKEL = decagon(SOCKEL_APOTHEM)


TOL = 0.0   # mm; `--pruefen` setzt 0,5 (Rundung der gespeicherten Lage auf 0,01 mm und 0,001 Grad)


def z_touch(a0, a1, b0, b1):
    return a0 <= b1 and b0 <= a1   # Beruehrung zaehlt als Ueberlappung (Deckel des Sumpfs auf Flurhoehe)


def violations(spec, shape, others, inside=True):
    """Liste der verletzten Regeln fuer einen Fussabdruck; leere Liste = Lage zulaessig."""
    v = []
    z0, z1 = spec["z0"], spec["z1"]
    if inside and not spec.get("aussen"):
        r = rmax(shape)
        if r > DOME_R + TOL:
            v.append("kuppel_kreis: Umkreis %.0f > %.0f" % (r, DOME_R))
        if max(extent(shape, n) for n in NORMALS) > APOTHEM - WALL_GAP + TOL:
            v.append("wandluft: %.0f mm zur Zehneck-Wand, Soll >= %.0f" % (APOTHEM - max(extent(shape, n) for n in NORMALS), WALL_GAP))
        ztop = max(0.0, z1 - FLOOR)
        if math.hypot(r, ztop) > DOME_R + TOL and ztop > 0:
            v.append("kopffreiheit: Umkreis %.0f in %.0f mm Hoehe ausserhalb Kugel %.0f" % (r, ztop, DOME_R))
        if not spec.get("walkable") and z0 < FLOOR + 1700 and z1 > FLOOR and dist(shape, CORRIDOR, 1.0) <= 0:
            v.append("tuer_gang: im 900-mm-Gang Tuer (Az %.0f) - Zentralpool" % DOOR_AZ)
    if spec.get("aussen"):
        if dist(shape, SOCKEL) < GAP - TOL:
            v.append("sockel: %.0f mm zum Sockel, Soll >= %.0f" % (dist(shape, SOCKEL), GAP))
        if dist(shape, FORECOURT) <= 0:
            v.append("tuer_vorplatz: im 900 x 1500 Vorplatz vor der Tuer")
    for o in others:
        if not z_touch(z0, z1, o["z0"], o["z1"]):
            continue
        d = dist(shape, o["shape"], GAP + 1)
        if d < GAP - TOL:
            v.append("kollision %s: %.0f mm, Soll >= %.0f" % (o["name"], d, GAP))
    return v


def offsets(maxd, grid=GRID):
    n = int(maxd // grid)
    out = [(dx * grid, dy * grid) for dx in range(-n, n + 1) for dy in range(-n, n + 1) if math.hypot(dx * grid, dy * grid) <= maxd + 1e-9]
    out.sort(key=lambda o: (round(math.hypot(*o), 6), math.atan2(o[1], o[0])))
    return out


OFFS_750 = offsets(MAX_SHIFT)
OFFS_FAR = None


def nearest_gap(spec, shape, others):
    best = (1e9, None)
    for o in others:
        if z_touch(spec["z0"], spec["z1"], o["z0"], o["z1"]) and not o.get("walkable"):
            d = dist(shape, o["shape"])
            if d < best[0]:
                best = (d, o["name"])
    return best


def pos_dict(x, y, yaw, z):
    az, r = az_r(x, y)
    return {"x_mm": round(x, 2), "y_mm": round(y, 2), "drehung_grad": round(yaw % 360 if yaw % 360 <= 180 else yaw % 360 - 360, 3), "z_modell_mm": round(z, 1), "r_mm": round(r, 1), "az_grad": round(az, 1)}


# ---------------------------------------------------------------- bleibende Gruppen (Lage aus dem Modell, nur Z aendert sich)
def stay_groups():
    """id -> (Liste Instanz-Plaetze (x,y,yaw), z_bauplatz, Hinweis). Lage nach Modell (D97, D98), Hoehe nach Soll."""
    G = {}
    for bid, defn in (("nft_aussen", "nft_tisch_aussen"), ("nft_mitte", "nft_tisch_mitte"), ("nft_innen", "nft_tisch_innen")):
        G[bid] = ([(i["m"][3], i["m"][7], yaw_of(i)) for i in inst_list(defn)], FLOOR,
                  "Standflaeche Flur; Rinnen-Wasserspiegel auf Soll ueber Tisch-Hoehenparameter (U3), Lage nach Modell (D97)")
    for bid, defn in (("fd_aussen", "ibc_beet_aussen_800"), ("fd_mitte", "ibc_beet_innen_933")):
        G[bid] = ([(i["m"][3], i["m"][7], yaw_of(i)) for i in inst_list(defn)], FLOOR,
                  "Beet-Boden auf dem Flur (D97: +162 bis +209 gegen Ist); Flutstand 250 ueber Standrohr (U3)")

    def half(i):
        az = math.degrees(math.atan2(i["m"][7], i["m"][3]))
        return 1 if -72 < az < 108 else 2
    corners = inst_list("ring_ecke_d75")
    for k in (1, 2):
        G["ring_%d" % k] = ([(i["m"][3], i["m"][7], yaw_of(i)) for i in corners if half(i) == k], FLOOR + 1550, "Rohrachse 1550 ueber Flur (Ist 2145); Lage nach Modell (D98)")
    for bid, defn, k in (("abf_nft_1", "ring_abzweig_d32", 1), ("abf_nft_2", "ring_abzweig_d32", 2), ("abf_fd_1", "ring_abzweig_d40", 1), ("abf_fd_2", "ring_abzweig_d40", 2)):
        G[bid] = ([(i["m"][3], i["m"][7], yaw_of(i)) for i in inst_list(defn) if half(i) == k], FLOOR + 1550, "Abzweige am Ring, Rohrachse 1550 (Ist 2145)")
    return G


def nearest_valve(pos, zrel):
    best = None
    for i in inst_list("lt_kugelhahn_d63"):
        if abs(i["m"][11] - FLOOR - zrel) < 5:
            d = math.hypot(i["m"][3] - pos[0], i["m"][7] - pos[1])
            if best is None or d < best[0]:
                best = (d, i)
    return best


# ---------------------------------------------------------------- Suche: groesstes Teil zuerst, kleinste Verschiebung, mehrere Reihenfolgen
ORDERS = [
    ["nursery", "sump_1", "sump_2", "bio_1", "bio_2", "feed", "vortex_1", "vortex_2", "sludge_1", "sludge_2", "luftpumpe_1", "luftpumpe_2", "luftpumpe", "nachspeise", "venturi_1", "venturi_2", "permakultur", "rain", "tap"],
    ["sump_1", "sump_2", "nursery", "bio_1", "bio_2", "feed", "vortex_1", "vortex_2", "sludge_1", "sludge_2", "luftpumpe_1", "luftpumpe_2", "luftpumpe", "nachspeise", "venturi_1", "venturi_2", "permakultur", "rain", "tap"],
    ["nursery", "feed", "bio_1", "bio_2", "sump_1", "sump_2", "vortex_1", "vortex_2", "sludge_1", "sludge_2", "luftpumpe_1", "luftpumpe_2", "luftpumpe", "nachspeise", "venturi_1", "venturi_2", "permakultur", "rain", "tap"],
    ["bio_1", "bio_2", "sump_1", "sump_2", "nursery", "feed", "vortex_1", "vortex_2", "sludge_1", "sludge_2", "luftpumpe_1", "luftpumpe_2", "luftpumpe", "nachspeise", "venturi_1", "venturi_2", "permakultur", "rain", "tap"],
]
YAW_STEPS = (0.0, 15.0, -15.0)


def greedy(order, obstacles, parts):
    """Je Teil der erste regelkonforme Platz in aufsteigender Verschiebung (Raster 50 mm, bis SEARCH_MAX); Teile ohne Platz bleiben an der Zeichnung (OFFEN)."""
    global OFFS_FAR
    if OFFS_FAR is None:
        OFFS_FAR = OFFS_750 + [o for o in offsets(SEARCH_MAX, 100.0) if math.hypot(*o) > MAX_SHIFT]
    placed, pos, fail = [], {}, []
    for bid in order:
        nom, spec = parts[bid]["nom"], parts[bid]["spec"]
        steps = YAW_STEPS if spec["yaw_range"] else (0.0,)
        found = None
        for dx, dy in OFFS_FAR:
            c = (nom[0] + dx, nom[1] + dy)
            for ys in steps:
                yw = spec["yaw"] + (ys if spec["yaw_range"] >= abs(ys) else 0.0)
                if not violations(spec, spec["fn"](c, yw), obstacles + placed):
                    found = (c[0], c[1], yw)
                    break
            if found:
                break
        if found is None:
            fail.append(bid)
            found = (nom[0], nom[1], spec["yaw"])
        pos[bid] = found
        placed.append(solid(bid, spec["fn"]((found[0], found[1]), found[2]), spec["z0"], spec["z1"], walkable=spec.get("walkable", False), aussen=spec.get("aussen", False), soll=True))
    return pos, fail


def place_outside(fail, pos, parts, obstacles):
    """Teile ohne Platz in der Kuppel: naechster regelkonformer Platz AUSSEN (>= 150 mm vom Sockel, nicht im Tuer-Vorplatz), D109."""
    placed = [solid(i, parts[i]["spec"]["fn"]((pos[i][0], pos[i][1]), pos[i][2]), parts[i]["spec"]["z0"], parts[i]["spec"]["z1"], walkable=parts[i]["spec"].get("walkable", False),
                    aussen=parts[i]["spec"].get("aussen", False), soll=True) for i in pos if i not in fail]
    res = {}
    for bid in fail:
        spec = dict(parts[bid]["spec"])
        spec["aussen"] = True
        nom = parts[bid]["nom"]
        found = None
        for dx, dy in OFFS_FAR:
            c = (nom[0] + dx, nom[1] + dy)
            for ys in ((0.0, 15.0, -15.0) if spec["yaw_range"] else (0.0,)):
                yw = spec["yaw"] + ys
                if not violations(spec, spec["fn"](c, yw), obstacles + placed):
                    found = (c[0], c[1], yw)
                    break
            if found:
                break
        found = found or (nom[0], nom[1], spec["yaw"])
        res[bid] = found
        parts[bid]["spec"] = spec
        placed.append(solid(bid, spec["fn"]((found[0], found[1]), found[2]), spec["z0"], spec["z1"], walkable=spec.get("walkable", False), aussen=True, soll=True))
    return res


_BASE_BLOCKED = {}


def walk_blocked(obstacles, extra):
    """Namen der Hindernisse und Soll-Teile, die in der Kniescheibe (0,3 m) NICHT ueber 500-mm-Gaenge von der Tuer erreichbar sind; vorher schon Unerreichbare zaehlen nicht."""
    z = FLOOR + 300
    key = tuple(sorted(o["name"] for o in obstacles))
    if key not in _BASE_BLOCKED:
        solids = [o for o in obstacles if not o["walkable"] and not o["aussen"]]
        ok = flood(clearance(raster(solids, z)))
        _BASE_BLOCKED[key] = {o["name"] for o in solids if o["z0"] <= z <= o["z1"] and not reachable(o["shape"], ok)}
    solids = [o for o in list(obstacles) + list(extra) if not o["walkable"] and not o["aussen"]]
    ok = flood(clearance(raster(solids, z)))
    return sorted(o["name"] for o in solids if o["z0"] <= z <= o["z1"] and o["name"] not in _BASE_BLOCKED[key] and not reachable(o["shape"], ok))


def refine_reach(parts, obstacles, pos, fail):
    """Teile, die den Zugang zu Tischen, Beeten und Soll-Teilen abschnueren, gehen als Vorbau nach aussen (D109): jeweils das Teil, dessen Wegnahme die meisten Sperren aufhebt."""
    fail = list(fail)
    for _ in range(8):
        pos.update(place_outside(fail, pos, parts, obstacles))
        inside = [i for i in ORDER if i not in fail and not parts[i]["spec"].get("aussen") and i not in ("nachspeise", "venturi_1", "venturi_2")]   # Armaturen am Tank/Rohr gehen nicht in den Vorbau
        sol = {i: solid(i, parts[i]["spec"]["fn"]((pos[i][0], pos[i][1]), pos[i][2]), parts[i]["spec"]["z0"], parts[i]["spec"]["z1"], walkable=parts[i]["spec"].get("walkable", False), soll=True) for i in ORDER if i not in fail and not parts[i]["spec"].get("aussen")}
        blocked = walk_blocked(obstacles, sol.values())
        sol = {k: v for k, v in sol.items() if k in inside}
        print("  Erreichbarkeit: %d gesperrt %s (Vorbau: %s)" % (len(blocked), blocked[:6], fail), flush=True)
        if not blocked:
            break
        best = min(inside, key=lambda b: (len(walk_blocked(obstacles, [v for k, v in sol.items() if k != b])), -math.hypot(pos[b][0] - parts[b]["nom"][0], pos[b][1] - parts[b]["nom"][1])))
        fail.append(best)
    return fail


def greedy_best(parts, obstacles):
    best = None
    for n, order in enumerate(ORDERS):
        pos, fail = greedy(order, obstacles, parts)
        shifts = [math.hypot(pos[i][0] - parts[i]["nom"][0], pos[i][1] - parts[i]["nom"][1]) for i in pos]
        key = (len(fail), sum(1 for v in shifts if v > MAX_SHIFT), round(max(shifts)), round(sum(shifts)))
        print("  Reihenfolge %d: ohne Platz %s, Teile ueber %.0f mm: %d, groesste Verschiebung %.0f, Summe %.0f" % (n + 1, fail, MAX_SHIFT, key[1], key[2], key[3]), flush=True)
        if best is None or key < best[0]:
            best = (key, pos, n + 1, fail)
    return best[1], best[2], best[3]


# ---------------------------------------------------------------- Lauf
ORDER = ["sump_1", "sump_2", "bio_1", "bio_2", "vortex_1", "vortex_2", "sludge_1", "sludge_2", "nursery", "feed",
         "luftpumpe_1", "luftpumpe_2", "luftpumpe", "nachspeise", "venturi_1", "venturi_2", "permakultur", "rain", "tap"]


def soll_info(bid):
    n = nominal(bid)
    if n is None:
        return None
    az, r = az_r(*n)
    return {"x_mm": round(n[0], 1), "y_mm": round(n[1], 1), "r_mm": round(r, 1), "az_grad": round(az, 1)}


NOM_SHAPES = {}
LAST = {}


def solve(removed=()):
    """Lage aller Soll-Teile mit eigener Standflaeche; `removed` = Namen bleibender Hindernisse, die fuer die Alternative B entfallen."""
    obstacles = [o for o in build_obstacles() if o["name"] not in removed]
    parts = {}
    for bid in ORDER:
        nom = nominal(bid)
        parts[bid] = {"spec": spec_for(bid, nom), "nom": nom}
    pos3, order_nr, fail = greedy_best(parts, obstacles)
    fail = refine_reach(parts, obstacles, pos3, fail)
    yaws = {i: round(c[2], 1) for i, c in pos3.items()}
    pos = {i: (round(c[0]), round(c[1])) for i, c in pos3.items()}
    shapes = {i: (parts[i]["spec"], parts[i]["spec"]["fn"](pos[i], yaws[i])) for i in ORDER}
    fail = set(fail)
    placed = {i: solid(i, shapes[i][1], parts[i]["spec"]["z0"], parts[i]["spec"]["z1"], walkable=parts[i]["spec"].get("walkable", False), aussen=parts[i]["spec"].get("aussen", False), soll=True) for i in ORDER}
    others = list(obstacles) + list(placed.values())
    res = {}
    for bid in ORDER:
        spec, nom = parts[bid]["spec"], parts[bid]["nom"]
        sh0 = spec["fn"](nom)
        NOM_SHAPES[bid] = sh0
        shift = math.hypot(pos[bid][0] - nom[0], pos[bid][1] - nom[1])
        mine = [o for o in others if o["name"] != bid]
        c_bau = violations(spec, shapes[bid][1], mine)
        modus = "zeichnung" if shift <= MAX_SHIFT else "annahme"
        ort = "aussen (Vorbau)" if (spec.get("aussen") and bid in fail) else ("aussen (Platzhalter)" if spec.get("aussen") else "innen")
        d = (VORBAU_D,) if bid in fail else ((SHIFT_D,) if modus == "annahme" else None)
        entry = {"ort": ort, "gruppe": spec["gruppe"], "soll_lage": soll_info(bid), "fussabdruck": {"mass": spec["mass"], "z_von_mm": round(spec["z0"], 1), "z_bis_mm": round(spec["z1"], 1)},
                 "konflikte_soll_lage": violations(spec, sh0, obstacles), "modus": modus, "annahme": d[0] if d else None,
                 "verschiebung_mm": round(shift, 1), "bauplatz": pos_dict(pos[bid][0], pos[bid][1], yaws[bid], spec["z_bauplatz"]), "konflikte_bauplatz": c_bau, "alternativen": []}
        entry["status"] = "OFFEN" if (c_bau or (modus == "annahme" and not entry["annahme"])) else "OK"
        if bid in fail:
            entry["alternativen"] = [{"text": "innen ohne Regelverletzung gibt es keinen Platz (150 mm Luft, Wandluft 100, Tuer-Gang 900, Kuppelkugel 5800)", "gewaehlt": False},
                                     {"text": "Vorbau aussen am naechsten freien Platz, %.0f mm von der Zeichnung" % shift, "gewaehlt": True}]
        gap, who = nearest_gap(spec, shapes[bid][1], mine)
        entry["kleinster_abstand_mm"] = round(gap, 0) if gap < 1e8 else None
        entry["naechstes_teil"] = who
        res[bid] = entry
    # Einbauten: Sumpf-Gruppe wandert mit dem Sumpf, Filterpumpen stehen im Fischtank
    for bid in ("hauptpumpe_1", "hauptpumpe_2", "schwimmer_1", "schwimmer_2"):
        spec = spec_for(bid, nominal(bid))
        host = res[spec["host"]]
        nom = nominal(bid)
        hs = nominal(spec["host"])
        dx, dy = host["bauplatz"]["x_mm"] - hs[0], host["bauplatz"]["y_mm"] - hs[1]
        p2 = (nom[0] + dx, nom[1] + dy)
        inside = pt_in_poly(nom, spec_for(spec["host"], hs)["fn"](hs)[1])
        res[bid] = {"gruppe": "einbau", "soll_lage": soll_info(bid), "fussabdruck": {"mass": spec["mass"], "z_von_mm": round(spec["z0"], 1), "z_bis_mm": round(spec["z1"], 1)},
                    "konflikte_soll_lage": [], "annahme": EINBAU_D, "alternativen": [], "modus": "einbau", "status": "OK" if inside and EINBAU_D else "OFFEN", "wirt": spec["host"],
                    "verschiebung_mm": host["verschiebung_mm"], "bauplatz": pos_dict(p2[0], p2[1], 0.0, spec["z_bauplatz"]),
                    "konflikte_bauplatz": [] if inside else ["liegt in der Zeichnung nicht im Rechteck des Sumpfs"],
                    "kleinster_abstand_mm": None, "naechstes_teil": None, "hinweis": "liegt in der Zeichnung im Rechteck des Sumpfs und wandert mit ihm (starre Gruppe)"}
    for bid in ("filterpumpe_1", "filterpumpe_2"):
        nom = nominal(bid)
        az, r = az_r(*nom)
        r_in = 1940.0 - 100.0 - 137.5   # Wasserradius pool_zentral (T5_Wasser 1940) minus 100 mm Wandabstand minus Pumpenradius
        p2 = (r_in * math.cos(math.radians(az)), r_in * math.sin(math.radians(az)))
        res[bid] = {"gruppe": "einbau", "soll_lage": soll_info(bid), "fussabdruck": {"mass": "Kreis 275 mm (Quelle)", "z_von_mm": FLOOR - 1000, "z_bis_mm": FLOOR - 600},
                    "konflikte_soll_lage": [], "annahme": EINBAU_D, "alternativen": [], "modus": "einbau", "status": "OK" if EINBAU_D else "OFFEN", "wirt": "fish",
                    "verschiebung_mm": round(math.hypot(p2[0] - nom[0], p2[1] - nom[1]), 1), "bauplatz": pos_dict(p2[0], p2[1], 0.0, FLOOR - 1000),
                    "konflikte_bauplatz": [], "kleinster_abstand_mm": None, "naechstes_teil": None,
                    "hinweis": "Tauchpumpe am Boden des Fischtanks (D102), gleiches Azimut wie gezeichnet; die Quelle zeichnet sie am Tankrand"}
    LAST["obstacles"], LAST["shapes"] = obstacles, shapes
    return obstacles, others, res, shapes


def stay_entries(others):
    """bleibende Gruppen: Lage aus dem Modell, Hoehe nach Soll."""
    out = {}
    for bid, (pl, z, note) in stay_groups().items():
        out[bid] = {"gruppe": "bleibt", "soll_lage": None, "modus": "bleibt", "status": "OK", "annahme": None, "verschiebung_mm": 0.0, "alternativen": [],
                    "konflikte_bauplatz": [], "konflikte_soll_lage": [], "plaetze": [pos_dict(x, y, yaw, z) for x, y, yaw in pl], "hinweis": note}
        Lg = SOLL_BY_ID[bid]["lage"]
        if "bogen_radius_mm" in Lg:
            out[bid]["soll_lage"] = {"bogen_radius_mm": Lg["bogen_radius_mm"], "hinweis": "Bogen der Zeichnung ist schematisch (A16); Lage nach Modell (D97)"}
        else:
            out[bid]["soll_lage"] = {"hinweis": "Linienzug/Abzweige der Zeichnung; Lage nach Modell (D98)"}
    out["fish"] = {"gruppe": "bleibt", "soll_lage": {"x_mm": 0.0, "y_mm": 0.0, "r_mm": 0.0, "az_grad": 0.0}, "modus": "bleibt", "status": "OK", "annahme": None, "verschiebung_mm": 0.0,
                   "alternativen": [], "bauplatz": pos_dict(0.0, 0.0, 0.0, FLOOR - 1000), "konflikte_bauplatz": [], "konflikte_soll_lage": [],
                   "fussabdruck": {"mass": "Kreis Aussen %d mm (Wasser innen 3880; Quelle Durchmesser 4000, D96: Modellmass bleibt)" % (2 * POOL_R_OUT), "z_von_mm": FLOOR - 1000, "z_bis_mm": FLOOR + 1200},
                   "hinweis": "Pool-Huelle bleibt in der Mitte; Boden -1000, Rand 1200 (U3)"}
    valve = {"z0": FLOOR + 1500, "z1": FLOOR + 1600, "walkable": False}
    pl, conf = [], []
    for s in SOLL_BY_ID["kupplungshahn"]["lage"]["symbole"]:
        b = nearest_valve((s["x_mm"], s["y_mm"]), 2145)
        i = b[1]
        pl.append(pos_dict(i["m"][3], i["m"][7], yaw_of(i), FLOOR + 1550))
        conf += ["%s (Hahn bei Az %.0f)" % (v, az_r(i["m"][3], i["m"][7])[0]) for v in violations(valve, circle(i["m"][3], i["m"][7], 60.0), others)]
    out["kupplungshahn"] = {"gruppe": "bleibt", "soll_lage": {"hinweis": "Symbole bei Az 108 und -72, r 3375"}, "modus": "bleibt", "status": "OK", "annahme": None, "verschiebung_mm": 0.0,
                            "alternativen": [], "plaetze": pl, "konflikte_bauplatz": [], "konflikte_soll_lage": [], "hinweis": "Hahn des Modells auf Rohrachse 1550 (Ist 2145); im Betrieb offen (D98)",
                            "hinweise_gang": conf}
    for bid in ("ringende_1", "ringende_2"):
        n = nominal(bid)
        out[bid] = {"gruppe": "bleibt", "soll_lage": soll_info(bid), "modus": "zeichnung", "status": "OK", "annahme": None, "verschiebung_mm": 0.0, "alternativen": [],
                    "bauplatz": pos_dict(n[0], n[1], aim(n, (0.0, 0.0)) + 180, FLOOR + 1550), "konflikte_bauplatz": [], "konflikte_soll_lage": [],
                    "hinweis": "Hahn d63 am Ring-Ende in den Sumpf der Linie (D98), Lage der Zeichnung; hinweise_gang nennt Gang-Regeln",
                    "hinweise_gang": violations(valve, circle(n[0], n[1], 60.0), others)}
    return out


# ---------------------------------------------------------------- Laufweg 500: Flutung von der Tuer (wie check_walkways_voll.py)
EXT = 6100
NCELL = 2 * EXT // CELL


def raster(solids, z):
    n = NCELL
    lab = [-1] * (n * n)
    for oi, o in enumerate(solids):
        if not (o["z0"] <= z <= o["z1"]):
            continue
        sh = o["shape"]
        b = bbox(sh)
        for j in range(max(0, int((b[1] + EXT) // CELL)), min(n, int((b[3] + EXT) // CELL) + 1)):
            for i in range(max(0, int((b[0] + EXT) // CELL)), min(n, int((b[2] + EXT) // CELL) + 1)):
                x, y = -EXT + (i + 0.5) * CELL, -EXT + (j + 0.5) * CELL
                if (math.hypot(x - sh[1], y - sh[2]) <= sh[3]) if sh[0] == "c" else pt_in_poly((x, y), sh[1]):
                    lab[j * n + i] = oi
    for j in range(n):
        for i in range(n):
            x, y = -EXT + (i + 0.5) * CELL, -EXT + (j + 0.5) * CELL
            if max(x * nn[0] + y * nn[1] for nn in NORMALS) > APOTHEM and lab[j * n + i] == -1:
                gap = abs(-x * DOOR_DIR[1] + y * DOOR_DIR[0]) <= DOOR_W / 2 and x * DOOR_DIR[0] + y * DOOR_DIR[1] > APOTHEM - 200
                if not gap:
                    lab[j * n + i] = -2
    return lab


def clearance(lab):
    n = NCELL
    INF = 10 ** 9
    d = [0 if lab[k] != -1 else INF for k in range(n * n)]
    for j in range(n):
        for i in range(n):
            k = j * n + i
            if d[k]:
                for dj, di, w in ((-1, -1, 71), (-1, 0, 50), (-1, 1, 71), (0, -1, 50)):
                    jj, ii = j + dj, i + di
                    if 0 <= jj < n and 0 <= ii < n and d[jj * n + ii] + w < d[k]:
                        d[k] = d[jj * n + ii] + w
    for j in range(n - 1, -1, -1):
        for i in range(n - 1, -1, -1):
            k = j * n + i
            if d[k]:
                for dj, di, w in ((1, 1, 71), (1, 0, 50), (1, -1, 71), (0, 1, 50)):
                    jj, ii = j + dj, i + di
                    if 0 <= jj < n and 0 <= ii < n and d[jj * n + ii] + w < d[k]:
                        d[k] = d[jj * n + ii] + w
    return d


def flood(d):
    from collections import deque
    n = NCELL
    sx, sy = (APOTHEM - 300) * DOOR_DIR[0], (APOTHEM - 300) * DOOR_DIR[1]
    si, sj = int((sx + EXT) // CELL), int((sy + EXT) // CELL)
    start = None
    for r in range(0, 14):
        for dj in range(-r, r + 1):
            for di in range(-r, r + 1):
                k = (sj + dj) * n + si + di
                if start is None and d[k] >= 250:
                    start = (si + di, sj + dj)
    ok = [False] * (n * n)
    if start is None:
        return ok
    q = deque([start])
    ok[start[1] * n + start[0]] = True
    while q:
        i, j = q.popleft()
        for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ii, jj = i + di, j + dj
            if 0 <= ii < n and 0 <= jj < n and not ok[jj * n + ii] and d[jj * n + ii] >= 250:
                ok[jj * n + ii] = True
                q.append((ii, jj))
    return ok


def reachable(sh, ok, reach=400.0):
    n = NCELL
    b = bbox(sh)
    for j in range(max(0, int((b[1] - reach + EXT) // CELL)), min(n, int((b[3] + reach + EXT) // CELL) + 1)):
        for i in range(max(0, int((b[0] - reach + EXT) // CELL)), min(n, int((b[2] + reach + EXT) // CELL) + 1)):
            if ok[j * n + i]:
                p = (-EXT + (i + 0.5) * CELL, -EXT + (j + 0.5) * CELL)
                if dist(circle(p[0], p[1], 0.0), sh) <= reach:
                    return True
    return False


def walk_probe(obstacles, others):
    """Erreichbarkeit je Hindernis in Knie- (0,3 m) und Kopfscheibe (1,7 m): ohne und mit den Soll-Teilen."""
    solid_before = [o for o in obstacles if not o["walkable"] and not o["aussen"]]
    solid_after = [o for o in others if not o["walkable"] and not o["aussen"]]
    out = {}
    for tag, solids in (("ohne_soll", solid_before), ("mit_soll", solid_after)):
        res = {}
        for sname, z in (("knie", FLOOR + 300), ("kopf", FLOOR + 1700)):
            ok = flood(clearance(raster(solids, z)))
            for o in solids:
                if o["z0"] <= z <= o["z1"]:
                    res.setdefault(o["name"], {})[sname] = reachable(o["shape"], ok)
        out[tag] = res
    return out


def walk_summary(obstacles, others, probe):
    before, after = probe["ohne_soll"], probe["mit_soll"]
    def ok_of(d):
        return all(d.values())
    new_blocked = sorted(n for n, v in after.items() if not ok_of(v) and n in before and ok_of(before[n]))
    old_blocked = sorted(n for n, v in before.items() if not ok_of(v))
    soll_blocked = sorted(n for n, v in after.items() if n not in before and not ok_of(v))
    return {"neu_blockiert": new_blocked, "schon_vorher_nicht_erreichbar": old_blocked, "soll_teile_nicht_erreichbar": soll_blocked,
            "regel": "Flutung von der Tuer (Az %.0f) ueber Zellen mit Abstand >= 250 mm (= 500 mm Gang), 50-mm-Raster, Knie 0,3 m und Kopf 1,7 m; erreichbar = geflutete Zelle hoechstens 400 mm vom Bauteil" % DOOR_AZ}


# ---------------------------------------------------------------- Ausgabe
def build_output():
    obstacles, others, res, shapes = solve()
    stay = stay_entries(others)
    probe = walk_probe(obstacles, others)
    walk = walk_summary(obstacles, others, probe)
    items = []
    for b in SOLL_DATA["bauteile"]:
        if not b["im_umfang"]:
            continue
        bid = b["id"]
        e = res.get(bid) or stay.get(bid)
        row = {"id": bid, "name": b["name"], "anzahl": b["anzahl"]}
        row.update({k: v for k, v in e.items() if not k.startswith("_")})
        if bid in walk["soll_teile_nicht_erreichbar"]:
            row["laufweg"] = "nicht erreichbar (500 mm)"
        elif bid in probe["mit_soll"]:
            row["laufweg"] = "erreichbar" if all(probe["mit_soll"][bid].values()) else "nicht erreichbar (500 mm)"
        items.append(row)
    free = [r for r in items if r["modus"] == "zeichnung" and r["gruppe"] in ("frei", "aussen")]
    exceptions = [r["id"] for r in items if r["modus"] in ("annahme", "einbau")]
    meta = {
        "titel": "Lage-Probe der Soll-Lage (Oasis-Showcase, 18 Grad gedreht) gegen die gebaute Kuppel, N-UNIFY-AUTOBAHN U1",
        "erzeugt_von": "scripts/oasis_lagepruefung.py (python -I -X utf8 scripts/oasis_lagepruefung.py)",
        "eingaben": {"oasis-soll.json": "data/oasis-soll.json", "instanzen": "viewer/instances.json (built %s, %d Instanzen)" % (INST_DATA["built"], len(INSTANCES)), "detail": "viewer/detail/*.json"},
        "regeln": {"luft_mm": GAP, "wandluft_mm": WALL_GAP, "zehneck_apothema_mm": round(APOTHEM, 1), "kuppelkugel_mm": DOME_R, "tuer_gang_mm": CORRIDOR_W, "tuer_az_grad": DOOR_AZ,
                   "max_verschiebung_mm": MAX_SHIFT, "raster_mm": GRID, "fussboden_z_mm": FLOOR, "laufweg_mm": 500},
        "annahmen_im_skript": {"podest_ueberstand_mm": FOOT_PODEST, "podest_vortex_mm": PODEST_V, "podest_biofilter_mm": PODEST_B, "wand_becken_mm": 60,
                               "hindernis_beet": "Beet + 115 mm je Seite (Portal, D54)", "tuer_vorplatz_aussen": "900 x 1500 mm [A]"},
        "zaehlung": {"bauteile_im_umfang": len(items), "mit_bauplatz": sum(1 for r in items if r.get("bauplatz") or r.get("plaetze")),
                     "frei_oder_aussen_zeichnung": len(free), "groesste_verschiebung_zeichnung_mm": max([r["verschiebung_mm"] for r in free] or [0]),
                     "ausnahmen_annahme_oder_einbau": exceptions, "offen": [r["id"] for r in items if r["status"] == "OFFEN"],
                     "konflikte_nach_verschiebung": sum(len(r.get("konflikte_bauplatz", [])) for r in items)},
        "gangprobe": walk,
        "hinweise": [],
    }
    return {"meta": meta, "bauteile": items}


def draw(path, obstacles, shapes):
    """PNG der Probe (Draufsicht, mm/Pixel 10): grau = bleibende Hindernisse, rot = Soll-Lage der Zeichnung, gruen = Bauplatz, blau = Tuer-Gang."""
    from PIL import Image, ImageDraw
    S, X0, X1, Y0, Y1 = 10.0, -6600, 6600, -6700, 2200
    W, H = int((X1 - X0) / S), int((Y1 - Y0) / S)
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)

    def px(p):
        return ((p[0] - X0) / S, (Y1 - p[1]) / S)

    def outline(sh, col, width=2, fill=None):
        if sh[0] == "c":
            a, b = px((sh[1] - sh[3], sh[2] + sh[3])), px((sh[1] + sh[3], sh[2] - sh[3]))
            d.ellipse([a, b], outline=col, width=width, fill=fill)
        else:
            d.polygon([px(p) for p in sh[1]], outline=col, fill=fill)
            d.line([px(p) for p in sh[1] + [sh[1][0]]], fill=col, width=width)
    outline(decagon(SOCKEL_APOTHEM), (120, 120, 120), 2)
    outline(decagon(APOTHEM), (0, 0, 0), 3)
    outline(circle(0.0, 0.0, DOME_R), (200, 200, 200), 1)
    outline(CORRIDOR, (90, 140, 255), 1, fill=(225, 235, 255))
    for o in obstacles:
        outline(o["shape"], (90, 90, 90), 1, fill=(215, 215, 215))
    for bid, (spec, sh) in shapes.items():
        outline(NOM_SHAPES[bid], (220, 40, 40), 2)
        outline(sh, (20, 150, 60), 3)
        c = px(sum((p[0] for p in pts_of(sh))) / len(pts_of(sh)) and (sum(p[0] for p in pts_of(sh)) / len(pts_of(sh)), sum(p[1] for p in pts_of(sh)) / len(pts_of(sh))))
        d.text((c[0] - 18, c[1] - 6), bid, fill=(0, 90, 30))
    im.save(path)


def show(out):
    z = out["meta"]["zaehlung"]
    print("Bauteile im Umfang %d, mit Bauplatz %d, frei/aussen nach Zeichnung %d (groesste Verschiebung %.0f mm, Grenze %.0f)" % (z["bauteile_im_umfang"], z["mit_bauplatz"], z["frei_oder_aussen_zeichnung"], z["groesste_verschiebung_zeichnung_mm"], MAX_SHIFT))
    print("Ausnahmen (annahme/einbau): %s" % z["ausnahmen_annahme_oder_einbau"])
    print("OFFEN: %s" % z["offen"])
    print("Konflikte nach Verschiebung: %d" % z["konflikte_nach_verschiebung"])
    g = out["meta"]["gangprobe"]
    print("Laufweg: neu blockiert %s | Soll-Teile nicht erreichbar %s | schon vorher nicht erreichbar %d" % (g["neu_blockiert"], g["soll_teile_nicht_erreichbar"], len(g["schon_vorher_nicht_erreichbar"])))
    for r in out["bauteile"]:
        if r["gruppe"] in ("frei", "aussen", "einbau") or r["konflikte_bauplatz"] or r.get("hinweise_gang"):
            b = r.get("bauplatz") or {}
            print("  %-14s %-8s %-9s %-6s Versch. %6.0f  x %7.0f y %7.0f dreh %6.1f z %6.0f  Abst %s %s | vorher: %s%s" % (
                r["id"], r["gruppe"], r["modus"], r["status"], r["verschiebung_mm"], b.get("x_mm", 0), b.get("y_mm", 0), b.get("drehung_grad", 0), b.get("z_modell_mm", 0),
                r.get("kleinster_abstand_mm"), r.get("naechstes_teil") or "", "; ".join(r["konflikte_soll_lage"])[:150] or "frei",
                (" | GANG: " + "; ".join(r["hinweise_gang"])[:140]) if r.get("hinweise_gang") else ""))


def verify_file():
    """`--pruefen`: liest data/oasis-lage.json und misst jede Lage am Modell neu (Sekunden); rechnet die Suche nicht neu."""
    global TOL
    TOL = 0.5
    err = []
    if not os.path.exists(OUT):
        return ["data/oasis-lage.json fehlt (erst ohne --pruefen rechnen)"], None
    out = load_json(OUT)
    items = out["bauteile"]
    z = out["meta"]["zaehlung"]
    if len(items) != 40:
        err.append("Bauteile im Umfang %d statt 40" % len(items))
    if [r["id"] for r in items] != IN_SCOPE:
        err.append("Bauteile der Datei weichen von data/oasis-soll.json ab")
    if out["meta"]["eingaben"]["instanzen"].split("built ")[1].split(",")[0] != INST_DATA["built"]:
        err.append("Export hat sich geaendert (built %s): Lage neu rechnen" % INST_DATA["built"])
    obstacles = build_obstacles()
    removed = set(out["meta"].get("entfernte_hindernisse", []))
    obstacles = [o for o in obstacles if o["name"] not in removed]
    placed = {}
    for r in items:
        if r["gruppe"] in ("frei", "aussen"):
            b = r["bauplatz"]
            spec = spec_for(r["id"], nominal(r["id"]))
            if r.get("ort", "").startswith("aussen"):
                spec["aussen"] = True
            placed[r["id"]] = (spec, spec["fn"]((b["x_mm"], b["y_mm"]), b["drehung_grad"]))
    solids = [solid(i, sh, sp["z0"], sp["z1"], walkable=sp.get("walkable", False), aussen=sp.get("aussen", False)) for i, (sp, sh) in placed.items()]
    n_conf = 0
    max_free = 0.0
    for r in items:
        if not (r.get("bauplatz") or r.get("plaetze")):
            err.append("%s ohne Bauplatz" % r["id"])
            continue
        if r["status"] != "OK":
            err.append("%s Status %s" % (r["id"], r["status"]))
        if r["id"] in placed:
            sp, sh = placed[r["id"]]
            v = violations(sp, sh, obstacles + [o for o in solids if o["name"] != r["id"]])
            n_conf += len(v)
            for x in v:
                err.append("%s: %s" % (r["id"], x))
            b = r["bauplatz"]
            nom = nominal(r["id"])
            shift = math.hypot(b["x_mm"] - nom[0], b["y_mm"] - nom[1])
            if r["modus"] == "zeichnung":
                max_free = max(max_free, shift)
                if shift > MAX_SHIFT:
                    err.append("%s: Verschiebung %.0f > %.0f ohne ANNAHME" % (r["id"], shift, MAX_SHIFT))
            elif not r.get("annahme"):
                err.append("%s: Verschiebung %.0f > %.0f ohne ANNAHME (D-Nummer fehlt)" % (r["id"], shift, MAX_SHIFT))
            if not sp.get("aussen") and rmax(sh) > DOME_R + TOL:
                err.append("%s ausserhalb der Kuppel (Umkreis %.0f)" % (r["id"], rmax(sh)))
        elif r["modus"] == "einbau" and not r.get("annahme"):
            err.append("%s: Einbau ohne D-Nummer" % r["id"])
    g = out["meta"]["gangprobe"]
    if g["soll_teile_nicht_erreichbar"] or g["neu_blockiert"]:
        err.append("Laufweg: nicht erreichbar %s, neu blockiert %s" % (g["soll_teile_nicht_erreichbar"], g["neu_blockiert"]))
    print("Bauteile %d, alle mit Bauplatz: %s" % (len(items), "ja" if not any("ohne Bauplatz" in e for e in err) else "nein"))
    print("Kollisionen/Regelverletzungen nach Verschiebung (neu gemessen aus der Datei): %d" % n_conf)
    print("groesste Verschiebung gegen die Zeichnung (Modus zeichnung): %.0f mm (Grenze %.0f)" % (max_free, MAX_SHIFT))
    print("Ausnahmen mit ANNAHME: %s" % ", ".join("%s=%s" % (r["id"], r["annahme"]) for r in items if r["modus"] in ("annahme", "einbau")))
    print("Laufweg: nicht erreichbar %s | neu blockiert %s" % (g["soll_teile_nicht_erreichbar"], g["neu_blockiert"]))
    return err, out


def main():
    if "--ohne" in sys.argv:   # Vergleichsrechnung: Hindernisse entfernen, Ergebnis nur anzeigen (schreibt nichts)
        rem = tuple(sys.argv[sys.argv.index("--ohne") + 1].split(","))
        obs, others, res, shapes = solve(removed=rem)
        print("ohne %s: Teile ohne Platz in der Kuppel (Vorbau): %s" % (", ".join(rem), [b for b, e in res.items() if e.get("ort") == "aussen (Vorbau)"]))
        print("Teile ueber 750 mm Verschiebung: %s" % [b for b, e in res.items() if e["gruppe"] == "frei" and e["verschiebung_mm"] > MAX_SHIFT])
        return 0
    if "--pruefen" in sys.argv:
        err, _ = verify_file()
        print("PRUEFUNG: %s" % ("BESTANDEN" if not err else "FEHLER (%d): %s" % (len(err), " | ".join(err[:12]))))
        return 1 if err else 0
    out = build_output()
    if "--bild" in sys.argv:
        draw(sys.argv[sys.argv.index("--bild") + 1], LAST["obstacles"], LAST["shapes"])
    open(OUT, "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, indent=1) + "\n")
    show(out)
    print("geschrieben: %s" % os.path.relpath(OUT, ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
