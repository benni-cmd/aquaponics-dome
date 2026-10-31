"""M8 Lagesuche: Puffer-Station (T81) im Sektor rechts der Tuer und Drittbecken (D46) per Abstandsrechnung (reine Geometrie, kein CAD-Lauf).
Aufruf: python scripts/place_m8.py   (liest scripts/dome-script.json und scripts/.segs.json aus dem letzten Build; gibt die besten Lagen mit Abstaenden aus)
Rahmen: Modellkoordinaten (mm); Station-KS: X = gegen den Uhrzeigersinn-Gegenrichtung (-t), Y radial nach aussen (Rueckseite/Plattform zur Wand), Z hoch; Bezug Mitte der Standflaeche am Boden."""
import json, math, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cmds = json.load(open(os.path.join(ROOT, "scripts", "dome-script.json")))["commands"]
P = {c["params"]["name"]: float(c["params"]["expression"]) for c in cmds if c["command"] == "parameters.add"}
LAY = json.load(open(os.path.join(ROOT, "data", "layout.json")))
segs = json.load(open(os.path.join(ROOT, "scripts", ".segs.json")))
mv = {c["params"]["occurrence"]: c["params"]["matrix"] for c in cmds if c["command"] == "occurrence.move"}
FZ = P["sock_h"]; AP = P["dome_base_d"] / 2 * math.cos(math.radians(18)); SR = P["strut_r"]
DOOR = P["door_edge_az"]; ST_AZ = DOOR + 36.0   # Sektor rechts der Tuer (Blick nach innen: gegen den Uhrzeigersinn)
BOX = (-1220.0, 1200.0, -691.5, 1230.0, 2445.0)   # X0 X1 Y0 Y1 H der Station (docs/parts/puffer_station.md)
D3, D3_WALL = 1030.0, 60.0                         # Drittbecken Innen-D, Wand; ausen 1150

def rect(m, l, w):
    c, s = m[0], m[4]; return [(m[3] + u * c - v * s, m[7] + u * s + v * c) for u, v in ((-l / 2, -w / 2), (l / 2, -w / 2), (l / 2, w / 2), (-l / 2, w / 2))]
def seg_pt(p, a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]; t = max(0, min(1, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / (dx * dx + dy * dy)))
    return math.hypot(p[0] - a[0] - t * dx, p[1] - a[1] - t * dy)
def inside(p, R):
    s = [(R[(i + 1) % 4][0] - R[i][0]) * (p[1] - R[i][1]) - (R[(i + 1) % 4][1] - R[i][1]) * (p[0] - R[i][0]) for i in range(4)]
    return all(x >= 0 for x in s) or all(x <= 0 for x in s)
def rr_dist(A, B):
    if any(inside(p, B) for p in A) or any(inside(p, A) for p in B): return 0.0
    return min(seg_pt(p, Q[i], Q[(i + 1) % 4]) for A_, Q in ((A, B), (B, A)) for p in A_ for i in range(4))
def rc_dist(R, c, r):
    return (0.0 if inside(c, R) else min(seg_pt(c, R[i], R[(i + 1) % 4]) for i in range(4))) - r

rects = []   # Hindernisse im Grundriss: Portale (Beet + 115 je Seite), Innentische
for k, m in mv.items():
    cls = k.split(":")[0]
    if cls == "Beet_aussen_800": rects.append(("Aussenportal", rect(m, 2640, 800 + 230)))
    elif cls == "Beet_innen_933": rects.append(("Innenportal", rect(m, 1865, 933 + 230)))
    elif cls == "Tisch_innen": rects.append(("Innentisch", rect(m, 1700, 700)))
ROT = math.radians(P["door_az"] - 167)
r2 = math.hypot(LAY["pool2"]["cx"], LAY["pool2"]["cy"]) * P["pool2_r_factor"]
az = math.radians(DOOR); p2 = (r2 * math.cos(az), r2 * math.sin(az)); p2r = LAY["pool2"]["d"] / 2 + 60
pc, pcr = (0.0, 0.0), LAY["pool"]["d"] / 2 + P["wall"]
n_door = (math.cos(az), math.sin(az)); t_door = (-math.sin(az), math.cos(az))

def station_rect(r0, s):
    a = math.radians(ST_AZ); n = (math.cos(a), math.sin(a)); t = (-math.sin(a), math.cos(a))
    cx, cy = r0 * n[0] + s * t[0], r0 * n[1] + s * t[1]; X = (-t[0], -t[1]); Y = n
    x0, x1, y0, y1, h = BOX
    return [(cx + u * X[0] + v * Y[0], cy + u * X[1] + v * Y[1]) for u, v in ((x0, y0), (x1, y0), (x1, y1), (x0, y1))]

def pt_box_dist(p, R, z0, z1):
    """Abstand Punkt (x,y,z) zur Quaderflaeche: Grundriss Viereck R, Z z0..z1 (konvex)."""
    dxy = 0.0 if inside((p[0], p[1]), R) else min(seg_pt((p[0], p[1]), R[i], R[(i + 1) % 4]) for i in range(4))
    dz = max(z0 - p[2], 0.0, p[2] - z1); return math.hypot(dxy, dz)
def strut_clear(R):
    z0, z1 = FZ, FZ + BOX[4]; best = 1e9
    for A, B in segs:
        L = math.dist(A, B)
        if max(math.hypot(A[0], A[1]), math.hypot(B[0], B[1])) < 3000: continue
        for i in range(int(L / 25) + 1):
            f = i * 25 / L; p = tuple(A[j] + f * (B[j] - A[j]) for j in range(3))
            if p[2] > z1 + 400: continue
            best = min(best, pt_box_dist(p, R, z0, z1) - SR)
    return best
def wall_clear(R):   # Abstand der Rueckseite zur Fundamentring-Innenflaeche (Zehneck-Seiten, Apothem 5706); negativ = darueber
    nrm = [(math.cos(math.radians(DOOR + 36 * k)), math.sin(math.radians(DOOR + 36 * k))) for k in range(10)]
    return AP - max(p[0] * n[0] + p[1] * n[1] for p in R for n in nrm)
def corridor_clear(R):   # Abstand zur Tuerachse (Strecke Tuer -> Pool) minus halbe Gangbreite 450
    a, b = (AP * n_door[0], AP * n_door[1]), (pcr * n_door[0], pcr * n_door[1])
    return min(seg_pt(p, a, b) for p in R) - 450.0
def gaps(R, skip=()):
    g = {}
    g["Innentisch"] = min([rr_dist(R, q) for nm, q in rects if nm == "Innentisch"])
    g["Portal"] = min([rr_dist(R, q) for nm, q in rects if nm.endswith("portal")])
    g["Zentralpool"] = rc_dist(R, pc, pcr); g["Zweitbecken"] = rc_dist(R, p2, p2r)
    return g

def check():
    """Abstaende der in den Parametern gesetzten Lage (station_r/station_s, pool3_r/pool3_az); Exit 0 = Station Strebenabstand >= 100, Wand >= 100, Gaenge/Luecken >= Mindestwerte."""
    R = station_rect(P["station_r"], P["station_s"]); g = gaps(R); sc, w, cc = strut_clear(R), wall_clear(R), corridor_clear(R)
    c = (P["pool3_r"] * math.cos(math.radians(P["pool3_az"])), P["pool3_r"] * math.sin(math.radians(P["pool3_az"]))); r3 = (D3 + 2 * D3_WALL) / 2
    nrm = [(math.cos(math.radians(DOOR + 36 * k)), math.sin(math.radians(DOOR + 36 * k))) for k in range(10)]
    a, b = (AP * n_door[0], AP * n_door[1]), (pcr * n_door[0], pcr * n_door[1])
    g3 = {"Wand": AP - max(c[0] * n[0] + c[1] * n[1] for n in nrm) - r3, "Zweitbecken": math.dist(c, p2) - p2r - r3, "Zentralpool": math.hypot(*c) - pcr - r3,
          "Station": rc_dist(R, c, r3), "Tuerachse": seg_pt(c, a, b) - 450 - r3}
    for nm, q in rects: g3[nm] = min(g3.get(nm, 1e9), rc_dist(q, c, r3))
    ok = [sc >= 100, w >= 100, g["Innentisch"] >= 500, cc >= 0, min(g.values()) > 0, min(g3.values()) >= 400]
    print("Station: Strebenabstand", round(sc), "| Wand", round(w), "| Luecken", {k: round(v) for k, v in g.items()}, "| Tuergang-Rand", round(cc))
    print("Drittbecken:", {k: round(v) for k, v in g3.items()})
    print("PASS" if all(ok) else "FAIL", "M8-Lage (Strebe >= 100, Wand >= 100, Innentisch >= 500, Drittbecken-Luecken >= 400)")
    return all(ok)

if __name__ == "__main__":
    if "--check" in sys.argv: sys.exit(0 if check() else 1)
    res = []
    for r0 in range(3200, 4601, 50):
        for s in range(-700, 701, 50):
            R = station_rect(r0, s); w = wall_clear(R)
            if w < 100: continue
            g = gaps(R); cc = corridor_clear(R)
            if min(g.values()) < 500 or cc < 0: continue
            sc = strut_clear(R)
            res.append((sc, r0, s, round(w), {k: round(v) for k, v in g.items()}, round(cc)))
    res.sort(reverse=True)
    for r in res[:8]: print("Station Streben", round(r[0]), "r0", r[1], "s", r[2], "Wand", r[3], "Luecken", r[4], "Gang", r[5])
    print("zulaessig:", len(res), "| mit Strebenabstand >= 100:", sum(1 for r in res if r[0] >= 100))
