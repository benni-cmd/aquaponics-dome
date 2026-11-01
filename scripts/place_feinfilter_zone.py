"""M10-PLAN: gelockerte Standortsuche Feinfilter (T55) nach Bedienzone, ergaenzt scripts/place_feinfilter.py (nur Lesen, kein CAD-Lauf).
Aufruf: python -X utf8 scripts/place_feinfilter_zone.py
Kriterium BEDIENZONE: vor der Front ein freier Streifen 630 x 500 mm, Stirn- und Rueckseite je >= 150 mm frei (Rohranschluss, Spuelschlauch);
nie in der Bedienzone des Puffers; nach Einbau bleiben alle Bauteile ueber 500-mm-Gang erreichbar, die Bediengasse des Filters und die Puffer-Bedienzone auch;
Gangzellen, die weiter als 700 mm vom Filter verloren gehen, werden gezaehlt (0 = nur lokaler Verlust)."""
import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import place_feinfilter as F
from collections import deque
N, CELL, EXT = F.N, F.CELL, F.EXT

def occ_at(x, y):
    i, j = int((x + EXT) // CELL), int((y + EXT) // CELL)
    return F.occ[j][i] if 0 <= i < N and 0 <= j < N else True
def zone_free(cx, cy, yaw, u0, u1, v0, v1, pad=25):
    c, s = math.cos(yaw), math.sin(yaw); u = u0 - pad
    while u <= u1 + pad:
        v = v0 - pad
        while v <= v1 + pad:
            if occ_at(cx + u * c - v * s, cy + u * s + v * c): return False
            v += 25
        u += 25
    return True
def zone_test(cx, cy, yd, depth=500, end=150, back=150, body=630.0):
    yaw = math.radians(yd); FL, FW = F.FL, F.FW
    if not (zone_free(cx, cy, yaw, -FL / 2, FL / 2, -FW / 2, FW / 2, 0) and zone_free(cx, cy, yaw, -body / 2, body / 2, -FW / 2 - depth, -FW / 2)
            and zone_free(cx, cy, yaw, -FL / 2 - end, -FL / 2, -FW / 2, FW / 2) and zone_free(cx, cy, yaw, FL / 2, FL / 2 + end, -FW / 2, FW / 2)
            and zone_free(cx, cy, yaw, -FL / 2, FL / 2, FW / 2, FW / 2 + back)): return False
    R = F.rect(cx, cy, yaw)
    return not (any(F.inside_poly(p[0], p[1], F.BZ) for p in R) or any(F.inside_poly(b[0], b[1], R) for b in F.BZ))

def edt_of(o):
    g = [[0.0 if o[j][i] else F.INF for i in range(N)] for j in range(N)]
    for i in range(N):
        col = F.edt1([g[j][i] for j in range(N)])
        for j in range(N): g[j][i] = col[j]
    for j in range(N): g[j] = F.edt1(g[j])
    return [[max(math.sqrt(v) * CELL - CELL / 2, 0.0) for v in row] for row in g]
def flood(Dm, thr, seed):
    ok = [[False] * N for _ in range(N)]; q = deque(); best = None
    for dj in range(-12, 13):
        for di in range(-12, 13):
            jj, ii = seed[1] + dj, seed[0] + di
            if 0 <= jj < N and 0 <= ii < N and Dm[jj][ii] >= thr and (best is None or abs(dj) + abs(di) < best[0]): best = (abs(dj) + abs(di), jj, ii)
    ok[best[1]][best[2]] = True; q.append((best[1], best[2]))
    while q:
        j, i = q.popleft()
        for dj, di in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            jj, ii = j + dj, i + di
            if 0 <= jj < N and 0 <= ii < N and not ok[jj][ii] and Dm[jj][ii] >= thr: ok[jj][ii] = True; q.append((jj, ii))
    return ok

lab = [[-1] * N for _ in range(N)]   # Hindernis-Nummer je Zelle
for oi, (nm, pg, za, zb) in enumerate(F.obst):
    if not (za <= F.Z <= zb): continue
    if pg[0] == "circle": _, cx_, cy_, r_ = pg; xs, ys = [cx_ - r_, cx_ + r_], [cy_ - r_, cy_ + r_]
    else: xs, ys = [p[0] for p in pg], [p[1] for p in pg]
    for j in range(max(0, int((min(ys) + EXT) // CELL)), min(N, int((max(ys) + EXT) // CELL) + 1)):
        for i in range(max(0, int((min(xs) + EXT) // CELL)), min(N, int((max(xs) + EXT) // CELL) + 1)):
            x, y = F.cell_xy(i, j)
            if (pg[0] == "circle" and math.hypot(x - cx_, y - cy_) <= r_) or (pg[0] != "circle" and F.inside_poly(x, y, pg)): lab[j][i] = oi
SP = ((F.AP - 350) * math.cos(math.radians(F.DOOR)), (F.AP - 350) * math.sin(math.radians(F.DOOR)))
SEED = (int((SP[0] + EXT) // CELL), int((SP[1] + EXT) // CELL))
def reached(ok):
    got = set()
    for j in range(N):
        for i in range(N):
            oi = lab[j][i]
            if oi < 0 or oi in got: continue
            if any(0 <= j + dj < N and 0 <= i + di < N and ok[j + dj][i + di] for dj in range(-9, 10) for di in range(-9, 10) if dj * dj + di * di <= 81): got.add(oi)
    return {F.obst[o][0] for o in got if F.obst[o][2] <= F.Z <= F.obst[o][3]}
def with_filter(cx, cy, yd):
    o2 = [row[:] for row in F.occ]; R = F.rect(cx, cy, math.radians(yd)); xs, ys = [p[0] for p in R], [p[1] for p in R]
    for j in range(int((min(ys) + EXT) // CELL), int((max(ys) + EXT) // CELL) + 1):
        for i in range(int((min(xs) + EXT) // CELL), int((max(xs) + EXT) // CELL) + 1):
            if F.inside_poly(*F.cell_xy(i, j), R): o2[j][i] = True
    return o2
def near_pt(ok, px, py, rad):
    return any(ok[int((py + dj * 50 + EXT) // CELL)][int((px + di * 50 + EXT) // CELL)] and math.hypot(di * 50, dj * 50) <= rad for dj in range(-3, 4) for di in range(-3, 4))
def seg_d(p, a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]; t = max(0, min(1, ((p[0] - a[0]) * dx + (p[1] - a[1]) * dy) / (dx * dx + dy * dy))); return math.hypot(p[0] - a[0] - t * dx, p[1] - a[1] - t * dy)
def full_check(base, cx, cy, yd):
    ok0, r0 = base; ok2 = flood(edt_of(with_filter(cx, cy, yd)), 250, SEED); r2 = reached(ok2)
    yaw = math.radians(yd); c, s = math.cos(yaw), math.sin(yaw); fp = (cx + (F.FW / 2 + 250) * s, cy - (F.FW / 2 + 250) * c)
    m = F.mv["Puffer_Klein:1"]; v = -350 - 325; pp = (m[3] - v * m[4], m[7] + v * m[0])
    R = F.rect(cx, cy, yaw)
    far = 0
    for j in range(N):
        for i in range(N):
            if ok0[j][i] and not ok2[j][i]:
                p = F.cell_xy(i, j)
                if not F.inside_poly(p[0], p[1], R) and min(seg_d(p, R[k], R[(k + 1) % 4]) for k in range(4)) > 700: far += 1
    return sorted(r0 - r2), near_pt(ok2, fp[0], fp[1], 100), near_pt(ok2, pp[0], pp[1], 150), far

if __name__ == "__main__":
    print("Raster", CELL, "mm, Filter-Grundriss", F.FL, "x", F.FW, "- Kriterium Bedienzone 630 x 500 vorn, Stirn/Rueck >= 150")
    ok0 = flood(edt_of(F.occ), 250, SEED); base = (ok0, reached(ok0)); print("Basis: erreichbare Bauteile", len(base[1]))
    for line, (a0, a1) in (("Ost", (-72, 126)), ("West", (126, -72))):
        got = []
        for j in range(N):
            for i in range(N):
                if F.D[j][i] < 300: continue
                x, y = F.cell_xy(i, j); r = math.hypot(x, y); az = math.degrees(math.atan2(y, x))
                if not (F.pr + 50 < r < F.AP - 100): continue
                if not ((a0 <= az <= a1) if a0 <= a1 else (az >= a0 or az <= a1)): continue
                for k in range(24):
                    if zone_test(x, y, 15 * k):
                        dp, dq = F.pipe_proxy(x, y, math.radians(15 * k), line); got.append((dp + dq, x, y, 15 * k, az, r, dp, dq))
        got.sort(); print(f"== Linie {line}: {len(got)} Kandidaten (Lage x Drehung); getrennte Orte, geprueft:")
        done = []
        for t in got:
            if len(done) >= 3: break
            if any(math.hypot(t[1] - d[1], t[2] - d[2]) < 600 for d in done): continue
            unr, front, puf, far = full_check(base, t[1], t[2], t[3])
            if unr or not front or not puf: continue
            done.append(t); print(f"  Mitte x{t[1]:.0f} y{t[2]:.0f} Drehung {t[3]} (Az {t[4]:.0f}, r {t[5]:.0f}); Rohr Pool~{t[6]:.0f} Pumpe~{t[7]:.0f}; Gangzellen verloren >700 mm vom Filter: {far}")
