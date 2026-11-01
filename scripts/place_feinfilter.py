"""M10-PLAN: Standortsuche fuer die zwei Feinfilter (T55) per Abstandsrechnung (reine Geometrie, nur Lesen, kein CAD-Lauf).
Aufruf: python -X utf8 scripts/place_feinfilter.py   (liest scripts/dome-script.json, data/layout.json, scripts/.compbox.json; schreibt nichts)
Hindernisse wie check_walkways_voll.py (Knie-Scheibe 0,3 m ueber Flur): Portale, Innentisch-Fuesse, Tanks/Pumpentafeln/Puffer, Becken, Zehneck-Wand; dazu die Bedienzone des Puffers.
Filter-Grundriss 770 x 680 mm (Behaelter 630 x 440 mit Stutzen); Einlauf-Port -X, Auslauf-Port +X, Bedienseite (Ablass, Korb heben) -Y.
Kriterium: Abstand Bedienseite und beide Stirnseiten >= GAP (500), Rueckseite >= BACK (150, Spuelschlauch); Lage nicht in der Bedienzone des Puffers."""
import json, math, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cmds = json.load(open(os.path.join(ROOT, "scripts", "dome-script.json")))["commands"]
P = {c["params"]["name"]: float(c["params"]["expression"]) for c in cmds if c["command"] == "parameters.add"}
LAY = json.load(open(os.path.join(ROOT, "data", "layout.json")))
mv = {c["params"]["occurrence"]: c["params"]["matrix"] for c in cmds if c["command"] == "occurrence.move"}
FZ = P["sock_h"]; AP = P["dome_base_d"] / 2 * math.cos(math.radians(18)); DOOR = P["door_edge_az"]
CELL, EXT = 50, 6100; N = 2 * EXT // CELL
GAP, BACK = float(os.environ.get("FGAP", 500)), float(os.environ.get("FBACK", 150))
FL, FW = float(os.environ.get("FFL", 770)), float(os.environ.get("FFW", 680))   # Filter-Grundriss mit Stutzen (docs/parts/feinfilter.md: ca. 770 x 680)
EXCL = set(filter(None, os.environ.get("FEXCL", "").split(",")))   # z.B. FEXCL=Tank_klein,Pumpe_klein = Variante ohne Absetzer (R44 Kandidat A)
BOX = {k.split(":")[0]: json.loads(json.dumps(v)) for k, v in json.load(open(os.path.join(ROOT, "scripts", ".compbox.json"))).items()}

def poly(m, bx):
    x0, y0, z0, x1, y1, z1 = bx; c, s = m[0], m[4]
    return [(m[3] + u * c - v * s, m[7] + u * s + v * c) for u, v in ((x0, y0), (x1, y0), (x1, y1), (x0, y1))], (m[11] + z0, m[11] + z1)

sys.path.insert(0, os.path.join(ROOT, "scripts", "workshop")); import sc as WSC, tisch_geom as TG
tp, td = WSC.load_params("nft_tisch")
obst = []   # (name, polygon | ("circle", cx, cy, r), zmin, zmax)
for k, m in mv.items():
    cls = k.split(":")[0]
    if cls in ("Beet_aussen_800", "Beet_innen_933"):
        l, w = (2640, 800 + 230) if cls == "Beet_aussen_800" else (1865, 933 + 230)
        pg, _ = poly(m, (-l / 2, -w / 2, 0, l / 2, w / 2, 0)); obst.append((k, pg, FZ, FZ + 1500))
    elif cls == "Tisch_innen":
        for (x, y) in TG.geometry("innen", tp, td["typen"]["innen"])["legs"]:
            pl_ = [(m[0] * (x + sx * tp["foot_plate"] / 2) + m[1] * (y + sy * tp["foot_plate"] / 2) + m[3], m[4] * (x + sx * tp["foot_plate"] / 2) + m[5] * (y + sy * tp["foot_plate"] / 2) + m[7]) for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
            obst.append((k + " Fuss", pl_, FZ, FZ + 900))
    elif cls in ("Tank_klein", "Tank_gross", "Tank_gross_t3", "Pumpe_klein", "Pumpe_gross", "Puffer_Klein") and cls not in EXCL:
        bx = BOX[cls.lower()]
        pg, (za, zb) = poly(m, bx); obst.append((k, pg, za, zb))
pools = [("Zentralpool", (0.0, 0.0), LAY["pool"]["d"] / 2 + P["wall"]),
         ("Zweitbecken", (P["pool2_r"] * math.cos(math.radians(P["pool2_az"])), P["pool2_r"] * math.sin(math.radians(P["pool2_az"]))), LAY["pool2"]["d"] / 2 + 60),
         ("Drittbecken", (P["pool3_r"] * math.cos(math.radians(P["pool3_az"])), P["pool3_r"] * math.sin(math.radians(P["pool3_az"]))), P["pool3_d"] / 2 + 60)]
for nm, c, r in pools: obst.append((nm, ("circle",) + c + (r,), -1e9, 1e9))
# Bedienzone des Puffers (700 breit x 650 tief vor der Front, Puffer-KS -Y), als Sperrflaeche fuer den Filter
mp = mv["Puffer_Klein:1"]; BZ, _ = poly(mp, (-350, -350 - 650, 0, 350, -350, 0))

def inside_poly(x, y, pg):
    s = 0
    for i in range(len(pg)):
        a, b = pg[i], pg[(i + 1) % len(pg)]; v = (b[0] - a[0]) * (y - a[1]) - (b[1] - a[1]) * (x - a[0]); s |= 1 if v >= 0 else 2
    return s != 3
def cell_xy(i, j): return (-EXT + (i + 0.5) * CELL, -EXT + (j + 0.5) * CELL)
Z = FZ + 300
occ = [[False] * N for _ in range(N)]
for nm, pg, za, zb in obst:
    if not (za <= Z <= zb): continue
    if pg[0] == "circle": _, cx, cy, r = pg; xs, ys = [cx - r, cx + r], [cy - r, cy + r]
    else: xs, ys = [p[0] for p in pg], [p[1] for p in pg]
    for j in range(max(0, int((min(ys) + EXT) // CELL)), min(N, int((max(ys) + EXT) // CELL) + 1)):
        for i in range(max(0, int((min(xs) + EXT) // CELL)), min(N, int((max(xs) + EXT) // CELL) + 1)):
            x, y = cell_xy(i, j)
            if (pg[0] == "circle" and math.hypot(x - cx, y - cy) <= r) or (pg[0] != "circle" and inside_poly(x, y, pg)): occ[j][i] = True
nrm = [(math.cos(math.radians(DOOR + 36 * k)), math.sin(math.radians(DOOR + 36 * k))) for k in range(10)]
dn = (math.cos(math.radians(DOOR)), math.sin(math.radians(DOOR)))
for j in range(N):
    for i in range(N):
        x, y = cell_xy(i, j)
        if max(x * n[0] + y * n[1] for n in nrm) > AP:
            gap = abs(x * -dn[1] + y * dn[0]) <= P["door_w"] / 2 and x * dn[0] + y * dn[1] > AP - 200
            if not gap: occ[j][i] = True

def edt1(f):
    n = len(f); INF = 1e20; v = [0] * n; zz = [0.0] * (n + 1); k = 0; zz[0] = -INF; zz[1] = INF; d = [0.0] * n
    for q in range(1, n):
        while True:
            s = ((f[q] + q * q) - (f[v[k]] + v[k] * v[k])) / (2 * q - 2 * v[k])
            if s <= zz[k] and k > 0: k -= 1
            else: break
        if s <= zz[k]: s = zz[k]
        k += 1; v[k] = q; zz[k] = s; zz[k + 1] = INF
    k = 0
    for q in range(n):
        while zz[k + 1] < q: k += 1
        d[q] = (q - v[k]) ** 2 + f[v[k]]
    return d
INF = 1e12
g = [[0.0 if occ[j][i] else INF for i in range(N)] for j in range(N)]
for i in range(N):
    col = edt1([g[j][i] for j in range(N)])
    for j in range(N): g[j][i] = col[j]
for j in range(N): g[j] = edt1(g[j])
D = [[math.sqrt(v) * CELL for v in row] for row in g]   # Abstand Zellmitte zum naechsten belegten Zellmittelpunkt (mm)
def dist_at(x, y):
    i, j = int((x + EXT) // CELL), int((y + EXT) // CELL)
    return max(D[j][i] - CELL / 2, 0.0) if 0 <= i < N and 0 <= j < N else 0.0

def side_clear(cx, cy, yaw):
    """Kleinster Abstand je Seite des Filter-Grundrisses (Punkte auf dem Rand, Schritt 25 mm), Seiten im Filter-KS: front -Y, back +Y, links -X (Einlauf), rechts +X (Auslauf)."""
    c, s = math.cos(yaw), math.sin(yaw); out = {}
    for name, pts in (("front", [(u, -FW / 2) for u in range(-int(FL / 2), int(FL / 2) + 1, 25)]), ("back", [(u, FW / 2) for u in range(-int(FL / 2), int(FL / 2) + 1, 25)]),
                      ("einlauf", [(-FL / 2, v) for v in range(-int(FW / 2), int(FW / 2) + 1, 25)]), ("auslauf", [(FL / 2, v) for v in range(-int(FW / 2), int(FW / 2) + 1, 25)])):
        out[name] = min(dist_at(cx + u * c - v * s, cy + u * s + v * c) for u, v in pts)
    return out
def rect(cx, cy, yaw):
    c, s = math.cos(yaw), math.sin(yaw); return [(cx + u * c - v * s, cy + u * s + v * c) for u, v in ((-FL / 2, -FW / 2), (FL / 2, -FW / 2), (FL / 2, FW / 2), (-FL / 2, FW / 2))]

# Linien: Pumpen gross nach Lage (Ost: Pumpe_gross:1,2 an Tank_gross:1; West: Pumpe_gross:3,4 an Tank_gross_t3:1)
PUMP = {"Ost": [mv["Pumpe_gross:1"], mv["Pumpe_gross:2"]], "West": [mv["Pumpe_gross:3"], mv["Pumpe_gross:4"]]}
pr = LAY["pool"]["d"] / 2 + P["wall"]
def pipe_proxy(cx, cy, yaw, line):
    c, s = math.cos(yaw), math.sin(yaw)
    ein = (cx - FL / 2 * c, cy - FL / 2 * s); aus = (cx + FL / 2 * c, cy + FL / 2 * s)
    d_pool = abs(math.hypot(*ein) - pr)
    d_pump = min(math.hypot(aus[0] - m[3], aus[1] - m[7]) for m in PUMP[line])
    return d_pool, d_pump

def search(line, az0, az1, need_all):
    res = []
    for j in range(N):
        for i in range(N):
            if D[j][i] < FW / 2 + BACK - 30: continue
            x, y = cell_xy(i, j); r = math.hypot(x, y)
            if not (pr + 100 < r < AP): continue
            az = math.degrees(math.atan2(y, x))
            if not ((az0 <= az <= az1) if az0 <= az1 else (az >= az0 or az <= az1)): continue
            for k in range(24):
                yaw = math.radians(15 * k); sc = side_clear(x, y, yaw)
                if any(inside_poly(px, py, BZ) for px, py in rect(x, y, yaw)): continue
                if any(inside_poly(bx, by, rect(x, y, yaw)) for bx, by in BZ): continue
                m_ = min(sc["front"], sc["einlauf"], sc["auslauf"]); ok = m_ >= GAP and sc["back"] >= BACK
                res.append((ok, m_, sc["back"], x, y, 15 * k, az, r, sc))
    return res

if __name__ == "__main__":
    print("Raster", CELL, "mm, Scheibe Z", Z, "(Flur", FZ, "+300); Hindernisse:", len(obst) + 0, "; Anforderung Bedienseite+Stirnseiten >=", GAP, ", Rueckseite >=", BACK)
    allres = search("X", -180, 180, True)   # gesamte Kuppel, getrennte Orte (>700 mm Abstand) je Mindestluecke
    for thr in (500, 400, 350, 300, 250):
        g_ = [r for r in allres if r[1] >= thr and r[2] >= BACK]; cl = []
        for t in sorted(g_, key=lambda r: -r[1]):
            if all(math.hypot(t[3] - o[3], t[4] - o[4]) > 700 for o in cl): cl.append(t)
        print(f"Gesamte Kuppel, Luecke >= {thr}: {len(g_)} Kandidaten, {len(cl)} getrennte Orte (x, y, Luecke):", [(round(t[3]), round(t[4]), round(t[1])) for t in cl[:5]])
    for line, (a0, a1) in (("Ost", (-72, 126)), ("West", (126, -72))):
        res = search(line, a0, a1, True)
        good = [r for r in res if r[0]]
        print(f"\n== Linie {line} (Azimut {a0}..{a1}): Kandidaten {len(res)}, davon erfuellt {len(good)}")
        pool_ = good if good else sorted(res, key=lambda r: -r[1])[:400]
        scored = []
        for ok, m_, back, x, y, yd, az, r, sc in pool_:
            dp, dq = pipe_proxy(x, y, math.radians(yd), line); scored.append((dp + dq, dp, dq, m_, back, x, y, yd, az, r, sc))
        scored.sort(key=lambda t: t[0] if good else -t[3])
        for t in scored[:6]:
            tot, dp, dq, m_, back, x, y, yd, az, r, sc = t
            print(f"  Mitte x{x:.0f} y{y:.0f} (Az {az:.0f}, r {r:.0f}) Drehung {yd}  Luecke min Bedien/Stirn {m_:.0f}  Rueckseite {back:.0f}  Rohr Pool~{dp:.0f} Pumpe~{dq:.0f}  Seiten " + " ".join(f"{k} {v:.0f}" for k, v in sc.items()))
