"""R38 Plane: Schnitt- und Nahtmuster der Kuppelhuelle (nachvollziehbare Rechnung, nur Standardbibliothek).

Aufruf:  python scripts/plane_nesting.py [--svg] [--json]
  ohne Schalter: Kennzahlen auf stdout; --json schreibt data/plane-zuschnitt.json; --svg schreibt docs/plane/*.svg
Eingabe: data/layout.json (dome.nodes_list), data/components/haut_paneel.json (felder). Das Modell wird nicht veraendert.

Modell der Rechnung
- Die Huelle besteht aus 40 ebenen Dreiecken (26 Knoten, 65 Streben). Eine EINHEIT ist eine Gruppe von Dreiecken, die als ein
  Luftkissen aus zwei Folienlagen (innen/aussen) zugeschnitten wird. Innerhalb einer Einheit liegt die Folie ohne Schnitt ueber
  den Streben ("Scharnier", Falz); die Einheit wird als Netz in die Ebene abgewickelt (aufspannender Baum der Scharnier-Streben).
- Streben im Inneren einer Einheit, die kein Scharnier sind ("Abnaeher"), muessen im Netz geschlossen werden: Ueberlappnaht
  auf der Strebe, je Lage. Streben zwischen zwei Einheiten sind "Fugen" (beide Einheiten klemmen ihre Kante in die Keilschiene).
- Kissen-Variante "geschweisst": die zwei Lagen sind am Umfang der Einheit verschweisst (luftdicht je Einheit, ein Ventil je
  Einheit). Variante "geklemmt": keine Umfangsnaht, beide Lagen werden nur in der Keilschiene geklemmt (ein gemeinsamer
  Luftraum, undicht an den Knoten, Geblaese gleicht aus).
- Masse: nominale Strebenlaengen (A 3279, B 3708) aus den gemessenen Knotenabstaenden, damit gleiche Typen gleiche Zuschnitte
  ergeben (Messabweichung der Knoten +-1 mm).
"""
import json
import math
import os
import sys
from itertools import product

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
LAYOUT = os.path.join(ROOT, "data", "layout.json")
HAUT = os.path.join(ROOT, "data", "components", "haut_paneel.json")
OUT_JSON = os.path.join(ROOT, "data", "plane-zuschnitt.json")
OUT_SVG = os.path.join(ROOT, "docs", "plane")

# ---- Annahmen (Herkunft steht dabei; Q = Quelle, E = errechnet, A = Annahme) ----------------------------------------------
OVERSTAND = 100.0      # mm [Q R24 / huelle_folie.md] Ueberstand der Folie ueber die Strebenachse an Fugen und Fussrand
DART_ALLOW = 25.0      # mm [A] Nahtzugabe je Seite an Abnaehern (Ueberlappnaht 50 mm, Heizkeil-Maschine, siehe R38)
WELD_OFF = 45.0        # mm [A] Lage der Umfangsnaht ausserhalb der Strebenachse (Kanalhalbbreite 12,5 + 32 mm Luft)
SEAM_W = 15.0          # mm [Q Leister COMET 500: 2 x 15 mm Nahtbreite] Breite einer Schweissspur
NODE_CLEAR = 130.0     # mm [Q docs/parts/keilschiene.md] Knotenfreiraum je Schienenende
ROLL_WIDTHS = [4000.0, 6000.0, 8000.0, 10000.0, 12000.0]   # mm [Q Haga 4/6 m; Agtec 1,0-14,5 m; USGR 3,05-15,2 m]
CUT_GAP = 0.0          # mm Abstand zwischen Zuschnitten im Nesting (gemeinsame Schnittlinie)
A_NOM, B_NOM = 3279.0, 3708.0
DOOR_CUT = (1026.0, 2043.0)   # mm [Q huelle_folie.md] Planenausschnitt Tuerfeld
EPS = 1e-6
RECOMMENDED = "V2"


# ---- Grundfunktionen ------------------------------------------------------------------------------------------------------
def sub(a, b): return tuple(x - y for x, y in zip(a, b))
def dot(a, b): return sum(x * y for x, y in zip(a, b))
def cross3(a, b): return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])
def dist(a, b): return math.dist(a, b)
def ekey(a, b): return (a, b) if a < b else (b, a)


def area2(pts):
    return 0.5 * sum(pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1] for i in range(len(pts)))


def perimeter(pts):
    return sum(math.dist(pts[i], pts[(i + 1) % len(pts)]) for i in range(len(pts)))


def ccw(pts):
    return pts if area2(pts) > 0 else pts[::-1]


def bbox(pts):
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    return min(xs), min(ys), max(xs), max(ys)


def rot(pts, deg, c=(0.0, 0.0)):
    t = math.radians(deg); co, si = math.cos(t), math.sin(t)
    return [(c[0] + (x - c[0]) * co - (y - c[1]) * si, c[1] + (x - c[0]) * si + (y - c[1]) * co) for x, y in pts]


def norm0(pts):
    x0, y0, _, _ = bbox(pts)
    return [(x - x0, y - y0) for x, y in pts]


def seg_cross(p1, p2, p3, p4):
    """echter Schnitt zweier Strecken (Beruehren und Ueberlagern zaehlt nicht)"""
    def o(a, b, c): return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    d1, d2, d3, d4 = o(p3, p4, p1), o(p3, p4, p2), o(p1, p2, p3), o(p1, p2, p4)
    e = 1e-3
    return ((d1 > e and d2 < -e) or (d1 < -e and d2 > e)) and ((d3 > e and d4 < -e) or (d3 < -e and d4 > e))


def inside(pt, poly, strict=True):
    """Punkt im Polygon (Strahlverfahren); Punkte auf dem Rand gelten nicht als innen"""
    n = len(poly); x, y = pt; c = False
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        # Randtest
        cr = (b[0] - a[0]) * (y - a[1]) - (b[1] - a[1]) * (x - a[0])
        if abs(cr) < 1e-2 and min(a[0], b[0]) - 1e-3 <= x <= max(a[0], b[0]) + 1e-3 and min(a[1], b[1]) - 1e-3 <= y <= max(a[1], b[1]) + 1e-3:
            return False
        if (a[1] > y) != (b[1] > y) and x < (b[0] - a[0]) * (y - a[1]) / (b[1] - a[1]) + a[0]:
            c = not c
    return c


def centroid(pts):
    a = area2(pts); cx = cy = 0.0
    for i in range(len(pts)):
        p, q = pts[i], pts[(i + 1) % len(pts)]
        f = p[0] * q[1] - q[0] * p[1]
        cx += (p[0] + q[0]) * f; cy += (p[1] + q[1]) * f
    return (cx / (6 * a), cy / (6 * a))


def overlap(P, Q):
    """zwei einfache Polygone ueberdecken sich (Flaeche > 0)"""
    bp, bq = bbox(P), bbox(Q)
    if bp[2] <= bq[0] + 1e-3 or bq[2] <= bp[0] + 1e-3 or bp[3] <= bq[1] + 1e-3 or bq[3] <= bp[1] + 1e-3:
        return False
    for i in range(len(P)):
        for j in range(len(Q)):
            if seg_cross(P[i], P[(i + 1) % len(P)], Q[j], Q[(j + 1) % len(Q)]):
                return True
    for pt in P:
        if inside(pt, Q): return True
    for pt in Q:
        if inside(pt, P): return True
    if inside(centroid(P), Q) or inside(centroid(Q), P): return True
    return False


def offset_poly(pts, dists):
    """Aussenversatz eines CCW-Polygons; dists[i] gilt fuer die Kante pts[i] -> pts[i+1] (Gehrung an den Ecken)"""
    n = len(pts); lines = []
    for i in range(n):
        p, q = pts[i], pts[(i + 1) % n]
        dx, dy = q[0] - p[0], q[1] - p[1]; L = math.hypot(dx, dy)
        nx, ny = dy / L, -dx / L
        lines.append(((p[0] + nx * dists[i], p[1] + ny * dists[i]), (dx / L, dy / L)))
    out = []
    for j in range(n):
        (p1, d1), (p2, d2) = lines[j - 1], lines[j]
        det = d1[0] * d2[1] - d1[1] * d2[0]
        if abs(det) < 1e-9:
            out.append(p2); continue
        t = ((p2[0] - p1[0]) * d2[1] - (p2[1] - p1[1]) * d2[0]) / det
        out.append((p1[0] + d1[0] * t, p1[1] + d1[1] * t))
    return out


def signature(pts):
    """Formgleichheit inkl. Spiegelung/Drehung (Zuschnitt darf gewendet werden), 10-mm-Raster"""
    def seq(P):
        P = ccw(P); n = len(P); s = []
        for i in range(n):
            a, b, c = P[i - 1], P[i], P[(i + 1) % n]
            v1 = (b[0] - a[0], b[1] - a[1]); v2 = (c[0] - b[0], c[1] - b[1])
            turn = math.degrees(math.atan2(v1[0] * v2[1] - v1[1] * v2[0], v1[0] * v2[0] + v1[1] * v2[1]))
            s.append((round(math.hypot(*v2) / 10.0), round(turn)))
        return min(tuple(s[k:] + s[:k]) for k in range(n))
    return min(seq(pts), seq([(-x, y) for x, y in pts]))


# ---- 1. Geometrie der Huelle ------------------------------------------------------------------------------------------------
def load_dome():
    dome = json.load(open(LAYOUT, encoding="utf-8"))["dome"]
    nodes = [(n["x"], n["y"], n["z"]) for n in dome["nodes_list"]]
    felder = json.load(open(HAUT, encoding="utf-8"))["felder"]
    tris = []
    for i, f in enumerate(felder):
        a, b, c = f["nodes"]
        nrm = cross3(sub(nodes[b], nodes[a]), sub(nodes[c], nodes[a]))
        g = tuple(sum(nodes[k][d] for k in (a, b, c)) / 3 for d in range(3))
        if dot(nrm, g) < 0: b, c = c, b          # CCW von aussen gesehen
        tris.append(dict(id=i, nodes=(a, b, c), typ=f["typ"], door=bool(f["door"]), basis=bool(f["basis"]), az=f["az"], z=f["z"]))
    edge_tris = {}
    for t in tris:
        a, b, c = t["nodes"]
        for u, v in ((a, b), (b, c), (c, a)):
            edge_tris.setdefault(ekey(u, v), []).append(t["id"])
    nom = {}
    meas = {}
    for k in edge_tris:
        d = dist(nodes[k[0]], nodes[k[1]])
        meas[k] = d
        nom[k] = A_NOM if d < 3500 else B_NOM
    return nodes, tris, edge_tris, nom, meas


def flat_tri(t, nom):
    a, b, c = t["nodes"]
    lab, lac, lbc = nom[ekey(a, b)], nom[ekey(a, c)], nom[ekey(b, c)]
    x = (lab ** 2 + lac ** 2 - lbc ** 2) / (2 * lab)
    return {a: (0.0, 0.0), b: (lab, 0.0), c: (x, math.sqrt(max(lac ** 2 - x * x, 0.0)))}


def tri_area_nom(t, nom):
    P = flat_tri(t, nom); return abs(area2(list(P.values())))


# ---- 2. Einheiten (Netze) --------------------------------------------------------------------------------------------------
class Unit:
    def __init__(self, uid, tri_ids, G, hinges=None):
        self.id = uid; self.tris = sorted(tri_ids); self.G = G
        nodes, tris, edge_tris, nom, meas = G
        S = set(self.tris)
        inner = [(k, [t for t in ts if t in S]) for k, ts in edge_tris.items()]
        inner = [(k, ts) for k, ts in inner if len(ts) == 2]
        self.inner = [k for k, _ in inner]
        if hinges is not None:
            self.hinges = list(hinges); self.darts = [k for k in self.inner if k not in set(hinges)]
            self._unfold(); return
        # aufspannender Baum mit moeglichst langen Scharnieren -> kuerzeste Abnaeher (Kruskal)
        parent = {t: t for t in self.tris}
        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]; x = parent[x]
            return x
        self.hinges, self.darts = [], []
        for k, ts in sorted(inner, key=lambda e: -nom[e[0]]):
            r1, r2 = find(ts[0]), find(ts[1])
            if r1 != r2:
                parent[r1] = r2; self.hinges.append(k)
            else:
                self.darts.append(k)
        self._unfold()

    def _unfold(self):
        nodes, tris, edge_tris, nom, meas = self.G
        S = set(self.tris); P = {}
        root = self.tris[0]; P[root] = flat_tri(tris[root], nom)
        todo = [root]; seen = {root}
        hset = set(self.hinges)
        while todo:
            t = todo.pop(0)
            a, b, c = tris[t]["nodes"]
            for u, v in ((a, b), (b, c), (c, a)):
                k = ekey(u, v)
                if k not in hset: continue
                for o in edge_tris[k]:
                    if o == t or o in seen or o not in S: continue
                    w = [n for n in tris[o]["nodes"] if n not in k][0]
                    pu, pv = P[t][u], P[t][v]
                    pw_par = [P[t][n] for n in tris[t]["nodes"] if n not in k][0]
                    L = nom[k]; e = ((pv[0] - pu[0]) / L, (pv[1] - pu[1]) / L)
                    side = e[0] * (pw_par[1] - pu[1]) - e[1] * (pw_par[0] - pu[0])
                    luw, lvw = nom[ekey(u, w)], nom[ekey(v, w)]
                    x = (L * L + luw ** 2 - lvw ** 2) / (2 * L); h = math.sqrt(max(luw ** 2 - x * x, 0.0))
                    nrm = (-e[1], e[0]); sg = -1.0 if side > 0 else 1.0
                    pw = (pu[0] + e[0] * x + nrm[0] * h * sg, pu[1] + e[1] * x + nrm[1] * h * sg)
                    P[o] = {u: pu, v: pv, w: pw}
                    seen.add(o); todo.append(o)
        self.P = P
        # Randkanten (gerichtet, CCW) des Netzes
        dset = set(self.darts); edges = []
        for t in self.tris:
            a, b, c = tris[t]["nodes"]
            for u, v in ((a, b), (b, c), (c, a)):
                k = ekey(u, v)
                if k in hset: continue
                kind = "abnaeher" if k in dset else ("fuge" if len(edge_tris[k]) == 2 else "rand")
                edges.append(dict(p=P[t][u], q=P[t][v], strut=k, kind=kind, tri=t))
        start = {}
        for e in edges:
            key = (round(e["p"][0], 2), round(e["p"][1], 2))
            assert key not in start, "Netz beruehrt sich selbst in einem Punkt (Einheit %s)" % self.id
            start[key] = e
        loop = [edges[0]]
        while True:
            q = loop[-1]["q"]; nxt = start[(round(q[0], 2), round(q[1], 2))]
            if nxt is loop[0]: break
            loop.append(nxt)
        assert len(loop) == len(edges), "Randschleife unvollstaendig (Einheit %s)" % self.id
        self.loop = loop
        self.outline = [e["p"] for e in loop]
        assert area2(self.outline) > 0
        # Netz darf sich nicht ueberlappen
        tl = [list(P[t].values()) for t in self.tris]
        for i in range(len(tl)):
            for j in range(i + 1, len(tl)):
                assert not overlap(ccw(tl[i]), ccw(tl[j])), "Netz ueberlappt sich (Einheit %s)" % self.id
        self.net_area = abs(area2(self.outline))
        self.door = any(tris[t]["door"] for t in self.tris)

    # Schnittkontur: Fugen/Rand mit OVERSTAND, Abnaeher mit DART_ALLOW
    def cut_poly(self):
        d = [OVERSTAND if e["kind"] != "abnaeher" else DART_ALLOW for e in self.loop]
        return offset_poly(self.outline, d)

    def weld_poly(self):
        d = [WELD_OFF if e["kind"] != "abnaeher" else 0.0 for e in self.loop]
        return offset_poly(self.outline, d)

    def weld_len(self):
        W = self.weld_poly(); n = len(W); tot = 0.0
        for i in range(n):
            if self.loop[i]["kind"] != "abnaeher":
                tot += math.dist(W[i], W[(i + 1) % n])
        return tot

    def dart_len(self):
        return sum(self.G[3][k] for k in self.darts)

    def crossings(self):
        """T-Kreuzungen: Abnaeher-Naht endet an der Umfangsnaht (Knoten am Rand der Einheit, nicht von allen Nachbarn umgeben)"""
        nodes, tris, edge_tris, nom, meas = self.G
        S = set(self.tris); c = 0
        star = {}
        for t in tris:
            for n in t["nodes"]: star.setdefault(n, set()).add(t["id"])
        for k in self.darts:
            for n in k:
                if not star[n] <= S: c += 1
        return c

    def sig(self):
        return signature(self.outline)


def build_units(groups, G, prefix):
    return [Unit("%s%02d" % (prefix, i + 1), g, G) for i, g in enumerate(groups)]


def best_net(uid, tri_ids, G):
    """waehlt unter allen Abnaeher-Moeglichkeiten das Netz mit der kleinsten Mindestbreite (dann kuerzester Abnaeher)"""
    from itertools import combinations
    nodes, tris, edge_tris, nom, meas = G
    base = Unit(uid, tri_ids, G)
    c = len(base.darts); best = None
    for dd in combinations(base.inner, c):
        hs = [k for k in base.inner if k not in dd]
        try:
            u = Unit(uid, tri_ids, G, hinges=hs)
        except (AssertionError, KeyError):
            continue
        if len(u.P) != len(u.tris): continue
        key = (round(min_width_orient(u.cut_poly())["h"]), sum(nom[k] for k in dd))
        if best is None or key < best[0]: best = (key, u)
    return best[1]


def rotate_unit(u, nperm, k, uid):
    nodes, tris, edge_tris, nom, meas = u.G
    tp = {tuple(sorted(t["nodes"])): t["id"] for t in tris}
    ids = list(u.tris); hs = list(u.hinges)
    for _ in range(k):
        ids = [tp[tuple(sorted(nperm[n] for n in tris[t]["nodes"]))] for t in ids]
        hs = [ekey(nperm[a], nperm[b]) for a, b in hs]
    return Unit(uid, ids, u.G, hinges=hs)


# ---- 3. Symmetrie (5-zaehlig um die Z-Achse) und Gruppenbildung ------------------------------------------------------------
def symmetry(G):
    nodes, tris, edge_tris, nom, meas = G
    co, si = math.cos(math.radians(72)), math.sin(math.radians(72))
    nperm = []
    for (x, y, z) in nodes:
        r = (x * co - y * si, x * si + y * co, z)
        j = min(range(len(nodes)), key=lambda k: dist(nodes[k], r))
        assert dist(nodes[j], r) < 20, "keine 5-zaehlige Symmetrie"
        nperm.append(j)
    tkey = {tuple(sorted(t["nodes"])): t["id"] for t in tris}
    tperm = [tkey[tuple(sorted(nperm[n] for n in t["nodes"]))] for t in tris]
    return nperm, tperm


def orbits(perm):
    seen = set(); orbs = []
    for i in range(len(perm)):
        if i in seen: continue
        o = [i]; j = perm[i]
        while j != i:
            o.append(j); j = perm[j]
        seen.update(o); orbs.append(o)
    return orbs


def adjacency(G):
    nodes, tris, edge_tris, nom, meas = G
    adj = {t["id"]: set() for t in tris}
    for k, ts in edge_tris.items():
        if len(ts) == 2:
            adj[ts[0]].add(ts[1]); adj[ts[1]].add(ts[0])
    return adj


def rhombus_groupings(G, tperm, limit=4000):
    """alle drehsymmetrischen Paarungen (20 Rauten) -> beste nach Zahl verschiedener Formen"""
    nodes, tris, edge_tris, nom, meas = G
    adj = adjacency(G)
    def rotp(p): return tuple(sorted((tperm[p[0]], tperm[p[1]])))
    def porbit(p):
        o = [tuple(sorted(p))]
        for _ in range(4): o.append(rotp(o[-1]))
        return o
    sols = []; cov = [False] * len(tris)
    def dfs(chosen):
        if len(sols) >= limit: return
        t = next((i for i in range(len(tris)) if not cov[i]), None)
        if t is None:
            sols.append(list(chosen)); return
        for u in sorted(adj[t]):
            orb = porbit((t, u)); flat = [x for p in orb for x in p]
            if len(set(flat)) != 10 or any(cov[x] for x in flat): continue
            for x in flat: cov[x] = True
            chosen.extend(orb); dfs(chosen); del chosen[-5:]
            for x in flat: cov[x] = False
    dfs([])
    return sols


def gore_domain(G, tperm):
    """ein Sektor je Dreiecksbahn: zusammenhaengende Wahl eines Vertreters je Bahn mit kuerzestem Umfang"""
    nodes, tris, edge_tris, nom, meas = G
    orbs = orbits(tperm); adj = adjacency(G)
    best = None
    for pick in product(*[range(len(o)) for o in orbs]):
        D = [orbs[i][p] for i, p in enumerate(pick)]
        S = set(D); seen = {D[0]}; st = [D[0]]
        while st:
            x = st.pop()
            for y in adj[x]:
                if y in S and y not in seen: seen.add(y); st.append(y)
        if len(seen) != len(D): continue
        per = sum(nom[k] for k, ts in edge_tris.items() if len([t for t in ts if t in S]) == 1)
        if best is None or per < best[0] - 1e-6: best = (per, D)
    return best[1]


def rot_group(D, tperm, k):
    g = list(D)
    for _ in range(k): g = [tperm[t] for t in g]
    return sorted(g)


# ---- 4. Streckenklassen und Kennzahlen -------------------------------------------------------------------------------------
def classify_struts(units, G):
    nodes, tris, edge_tris, nom, meas = G
    owner = {}
    for u in units:
        for t in u.tris: owner[t] = u
    cls = {}
    for k, ts in edge_tris.items():
        if len(ts) == 1: cls[k] = "rand"
        elif owner[ts[0]] is owner[ts[1]]:
            cls[k] = "abnaeher" if k in owner[ts[0]].darts else "scharnier"
        else: cls[k] = "fuge"
    return cls


def channel_lengths(cls, nom):
    tot = {"rand": 0.0, "fuge": 0.0, "scharnier": 0.0, "abnaeher": 0.0}; cnt = {k: 0 for k in tot}
    for k, c in cls.items():
        tot[c] += nom[k] - 2 * NODE_CLEAR; cnt[c] += 1
    return tot, cnt


def vertex_defects(G):
    nodes, tris, edge_tris, nom, meas = G
    ang = {}
    for t in tris:
        P = flat_tri(t, nom)
        for n, p in P.items():
            others = [q for m, q in P.items() if m != n]
            v1 = (others[0][0] - p[0], others[0][1] - p[1]); v2 = (others[1][0] - p[0], others[1][1] - p[1])
            a = math.degrees(math.acos((v1[0] * v2[0] + v1[1] * v2[1]) / (math.hypot(*v1) * math.hypot(*v2))))
            ang.setdefault(n, []).append(a)
    out = {}
    for n, l in ang.items():
        bnd = any(len(edge_tris[k]) == 1 for k in edge_tris if n in k)
        out[n] = dict(valence=len(l), summe=sum(l), defekt=360 - sum(l), rand=bnd)
    return out


# ---- 5. Nesting auf Rollenbreite (Bahnen mit abwechselnder Lage, Kandidaten je Zuschnitt-Typ) --------------------------------
_CAND_CACHE = {}


def min_width_orient(poly):
    """Drehung mit der kleinsten Bahnhoehe (Raster 0,5 Grad)"""
    best = None
    for k in range(0, 360):
        r = norm0(rot(poly, k * 0.5)); h = bbox(r)[3]
        if best is None or h < best[0] - 1e-6: best = (h, k * 0.5, r)
    return dict(h=best[0], th=best[1], a=best[2], w=bbox(best[2])[2])


def pitch(A, B):
    """kleinster Abstand der Startpunkte (x) von B nach A in einer Bahn, so dass A und B sich nicht ueberdecken"""
    dx = max(bbox(A)[2], bbox(B)[2]) + 1.0; step = 25.0
    while dx > 0:
        if overlap(A, [(x + dx, y) for x, y in B]): break
        dx -= step
    lo, up = dx, dx + step           # lo ueberdeckt, up nicht
    for _ in range(13):
        mid = (lo + up) / 2
        if overlap(A, [(x + mid, y) for x, y in B]): lo = mid
        else: up = mid
    return up + CUT_GAP


def candidates(poly, keep=4):
    """Lagen eines Zuschnitts in der Bahn: Kante parallel zur Rollenrichtung oder Mindestbreite; B = gedreht/gespiegelt"""
    sg = signature(poly)
    if sg in _CAND_CACHE: return _CAND_CACHE[sg]
    angs = []
    n = len(poly)
    for i in range(n):
        d = (poly[(i + 1) % n][0] - poly[i][0], poly[(i + 1) % n][1] - poly[i][1])
        a = -math.degrees(math.atan2(d[1], d[0]))
        angs += [a, a + 180.0]
    bw = None
    for k in range(0, 360):
        r = norm0(rot(poly, k * 0.5)); h = bbox(r)[3]
        if bw is None or h < bw[0] - 1e-6: bw = (h, k * 0.5)
    angs.append(bw[1])
    seen = []; cands = []
    for a in angs:
        a = round(a % 360.0, 1)
        if a in seen: continue
        seen.append(a)
        A = norm0(rot(poly, a)); h = bbox(A)[3]; w = bbox(A)[2]
        c = centroid(A)
        for tname, B in (("dreh180", norm0(rot(A, 180, c))), ("spiegel_x", norm0([(-x, y) for x, y in A])),
                         ("spiegel_y", norm0([(x, -y) for x, y in A]))):
            if abs(bbox(B)[3] - h) > 1.0: continue          # gleiche Bahnhoehe verlangt
            Ac, Bc = ccw(A), ccw(B)
            p1, p2 = pitch(Ac, Bc), pitch(Bc, Ac)
            cands.append(dict(a=Ac, b=Bc, h=h, w=w, p1=p1, p2=p2, th=a, mode=tname, score=h * (p1 + p2) / 2))
    cands.sort(key=lambda c: c["score"])
    out = []; hs = set()
    for c in cands:
        key = round(c["h"] / 20)
        if key in hs: continue
        hs.add(key); out.append(c)
        if len(out) >= keep: break
    _CAND_CACHE[sg] = out
    return out


def lane_len(c, m):
    """Laenge einer Bahn mit m Zuschnitten in Lage a,b,a,b,..."""
    if m <= 0: return 0.0
    x = 0.0
    for i in range(1, m):
        x += c["p1"] if i % 2 == 1 else c["p2"]
    return x + c["w"]


def nest(types, W):
    """types: Liste (name, poly, n). Beste Aufteilung der Rollenbreite W in Bahnen; Rollenlaenge L"""
    info = [(name, n, candidates(poly)) for name, poly, n in types]
    best = None
    for choice in product(*[range(len(c)) for _, _, c in info]):
        cs = [info[i][2][j] for i, j in enumerate(choice)]
        if any(c["h"] > W for c in cs): continue
        for ks in product(*[range(1, int(W // c["h"]) + 1) for c in cs]):
            if sum(k * c["h"] for k, c in zip(ks, cs)) > W + 1e-6: continue
            L = 0.0
            for k, c, (_, n, _) in zip(ks, cs, info):
                L = max(L, lane_len(c, math.ceil(n / k)))
            cand = (L, sum(k * c["h"] for k, c in zip(ks, cs)), ks, choice)
            if best is None or cand[:2] < best[:2]: best = cand
    if best is None: return None
    L, used, ks, choice = best
    lanes = []; y = 0.0
    for (name, n, cl), j, k in zip(info, choice, ks):
        c = cl[j]
        cnt = [n // k + (1 if i < n % k else 0) for i in range(k)]
        for m in cnt:
            lanes.append(dict(type=name, y=y, h=c["h"], count=m, c=c)); y += c["h"]
    return dict(W=W, L=L, lanes=lanes, used_w=y)


def placed(nst):
    """alle Zuschnitte der Rollenbelegung als (Typ, Polygon) - zur Ueberlappungs-Probe und fuer das SVG"""
    out = []
    for ln in nst["lanes"]:
        c = ln["c"]; x = 0.0
        for i in range(ln["count"]):
            if i > 0: x += c["p1"] if i % 2 == 1 else c["p2"]
            base = c["a"] if i % 2 == 0 else c["b"]
            out.append((ln["type"], [(px + x, py + ln["y"]) for px, py in base]))
    return out


def best_roll(types, widths):
    total = sum(abs(area2(p)) * n for _, p, n in types); rows = []
    for W in widths:
        r = nest(types, W)
        if r is not None:
            rows.append(dict(W=W, L=r["L"], flaeche=W * r["L"], verschnitt=1 - total / (W * r["L"]), nest=r))
    return min(rows, key=lambda r: r["verschnitt"]) if rows else None, rows


def nest_report(types, widths=ROLL_WIDTHS):
    """(a) eine gemeinsame Rolle fuer alle Zuschnitt-Typen, (b) je Typ eine eigene Rolle; jeweils beste Standardbreite"""
    total = sum(abs(area2(p)) * n for _, p, n in types)
    common, rows = best_roll(types, widths)
    sep = []
    for t in types:
        b, _ = best_roll([t], widths)
        sep.append(dict(typ=t[0], **b))
    sep_area = sum(r["flaeche"] for r in sep)
    separate = dict(rollen=sep, flaeche=sep_area, verschnitt=1 - total / sep_area)
    bester = common
    if common is None or separate["verschnitt"] < common["verschnitt"] - 0.02:
        bester = dict(W=None, L=None, flaeche=sep_area, verschnitt=separate["verschnitt"], getrennt=True)
    return dict(summe_flaeche=total, gemeinsam=common, getrennt=separate, bester=bester, standard=rows)


# ---- 6. Varianten ----------------------------------------------------------------------------------------------------------
def variant_metrics(vid, name, units, G, joint):
    nodes, tris, edge_tris, nom, meas = G
    cls = classify_struts(units, G)
    ch_len, ch_cnt = channel_lengths(cls, nom)
    sigs = {}
    for u in units: sigs.setdefault(u.sig(), []).append(u)
    # Zuschnitt-Typen: Tuerfeld-Einheit zaehlt als eigener Zuschnitt (Ausschnitt), nest-Typ = Grundform
    cuts = {}
    for sg, us in sigs.items():
        full = [u for u in us if not u.door]; dr = [u for u in us if u.door]
        cuts[sg] = dict(units=us, n=len(us), door=len(dr))
    n_shapes = len(sigs)
    n_cut_types = n_shapes + (1 if any(u.door for u in units) else 0)
    perim_weld = sum(u.weld_len() for u in units) if joint == "geschweisst" else 0.0
    darts = sum(u.dart_len() for u in units) * 2 / 1000.0        # beide Lagen
    perim_weld /= 1000.0
    cross = sum(u.crossings() for u in units) * 2 if True else 0  # je Lage ein T-Stoss
    cutpolys = [(u, u.cut_poly()) for u in units]
    types = []
    for sg, c in cuts.items():
        types.append(("T%d" % (len(types) + 1), c["units"][0].cut_poly(), c["n"]))
    nr = nest_report(types)
    max_area = max(abs(area2(p)) for _, p in cutpolys) / 1e6
    return dict(id=vid, name=name, gelenk=joint, einheiten=len(units), formen=n_shapes, zuschnitt_typen=n_cut_types,
                zuschnitte_gesamt=len(units) * 2, schnittlaenge_m=sum(perimeter(p) for _, p in cutpolys) / 1000.0,
                umfangsnaht_m=perim_weld, abnaeher_m=darts, naht_gesamt_m=perim_weld + darts,
                t_kreuzungen=cross, ventile=len(units) if joint == "geschweisst" else 1,
                schiene_einfach_m=ch_len["rand"] / 1000.0, schiene_doppel_m=ch_len["fuge"] / 1000.0,
                streben=ch_cnt, max_einheit_m2=max_area, nest=nr, types=types, units=units, cls=cls)


# ---- 7. Zusatzrechnungen -----------------------------------------------------------------------------------------------------
def dihedral_deg(G, k):
    """Knickwinkel der Huelle an einer Strebe (180 = eben); aus den Aussennormalen der zwei Dreiecke"""
    nodes, tris, edge_tris, nom, meas = G
    ns = []
    for t in edge_tris[k]:
        a, b, c = tris[t]["nodes"]
        n = cross3(sub(nodes[b], nodes[a]), sub(nodes[c], nodes[a])); L = math.sqrt(dot(n, n))
        ns.append(tuple(x / L for x in n))
    return 180.0 - math.degrees(math.acos(max(-1.0, min(1.0, dot(ns[0], ns[1])))))


def strip_shrink(width_mm, radius_mm):
    """Parallele gerade Bahn der Breite w auf Kugel R: Randlaenge gegen Mittellinie (Verkuerzung, Naeherung cos)"""
    return 1.0 - math.cos(width_mm / (2.0 * radius_mm))


def canon_frame(u):
    """Drehung/Verschiebung, die die laengste Kante der Strebenachsen-Kontur waagerecht an den Boden legt"""
    pts = u.outline; n = len(pts)
    i = max(range(n), key=lambda j: math.dist(pts[j], pts[(j + 1) % n]))
    d = (pts[(i + 1) % n][0] - pts[i][0], pts[(i + 1) % n][1] - pts[i][1])
    th = -math.degrees(math.atan2(d[1], d[0]))
    r = rot(pts, th)
    x0, y0 = bbox(rot(u.cut_poly(), th))[:2]
    return th, (x0, y0)


def to_frame(P, th, off):
    return [(x - off[0], y - off[1]) for x, y in rot(P, th)]


def door_cut_poly(u):
    """Planenausschnitt der Tuer im Netz: Mitte der Basiskante, 1026 breit, von Basiskante -100 mm bis 2043 mm in die Flaeche"""
    nodes, tris, edge_tris, nom, meas = u.G
    t = next(t for t in u.tris if tris[t]["door"])
    a, b, c = tris[t]["nodes"]
    for p, q in ((a, b), (b, c), (c, a)):
        if len(edge_tris[ekey(p, q)]) == 1:
            P = u.P[t]; pp, qq = P[p], P[q]; w = [n for n in tris[t]["nodes"] if n not in (p, q)][0]
            L = math.dist(pp, qq); e = ((qq[0] - pp[0]) / L, (qq[1] - pp[1]) / L)
            nrm = (-e[1], e[0])              # nach innen (CCW-Dreieck: links der Kante)
            m = ((pp[0] + qq[0]) / 2, (pp[1] + qq[1]) / 2)
            hw = DOOR_CUT[0] / 2
            return [(m[0] - e[0] * hw - nrm[0] * OVERSTAND, m[1] - e[1] * hw - nrm[1] * OVERSTAND),
                    (m[0] + e[0] * hw - nrm[0] * OVERSTAND, m[1] + e[1] * hw - nrm[1] * OVERSTAND),
                    (m[0] + e[0] * hw + nrm[0] * DOOR_CUT[1], m[1] + e[1] * hw + nrm[1] * DOOR_CUT[1]),
                    (m[0] - e[0] * hw + nrm[0] * DOOR_CUT[1], m[1] - e[1] * hw + nrm[1] * DOOR_CUT[1])]
    return None


# ---- 8. Ausgabe: Zuschnitt-Typen, JSON, SVG ----------------------------------------------------------------------------------
COLORS = ["#4c8dc7", "#e0a030", "#6bb26b", "#c46aa0", "#8a7fd0", "#d0715a"]


def cut_types(units):
    """Zuschnitt-Typen einer Variante: gleiche Form (Z1, Z2, ...) und gesondert das Tuerfeld (Planenausschnitt)"""
    groups = {}
    for u in units:
        groups.setdefault((u.sig(), u.door), []).append(u)
    out = []
    for i, ((sg, door), us) in enumerate(sorted(groups.items(), key=lambda kv: (kv[0][1], -len(kv[1])))):
        out.append(dict(id="Z%d" % (i + 1), door=door, units=us, rep=us[0]))
    return out


def edge_dims(u, th, off):
    """Beschriftung: Kantenlaenge auf der Strebenachse (nominal) an der Schnittkante"""
    res = []
    n = len(u.loop)
    cutp = to_frame(u.cut_poly(), th, off)
    ax = to_frame(u.outline, th, off)
    for i, e in enumerate(u.loop):
        res.append(dict(kind=e["kind"], laenge=u.G[3][e["strut"]], a=ax[i], b=ax[(i + 1) % n], ca=cutp[i], cb=cutp[(i + 1) % n]))
    return res


def svg_header(w, h, title):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" font-family="Arial,Helvetica,sans-serif">'
            '<rect width="100%%" height="100%%" fill="#ffffff"/>'
            '<text x="16" y="26" font-size="18" font-weight="bold" fill="#111">%s</text>' % (w, h, title))


def svg_pattern(ct, variant_name, path, count_text):
    u = ct["rep"]; th, off = canon_frame(u)
    cut = to_frame(u.cut_poly(), th, off); ax = to_frame(u.outline, th, off); wl = to_frame(u.weld_poly(), th, off)
    xs = [p[0] for p in cut]; ys = [p[1] for p in cut]
    W, H = max(xs), max(ys)
    sc = min(1000.0 / W, 620.0 / H); mx, my = 60, 90
    def X(x): return mx + x * sc
    def Y(y): return my + (H - y) * sc            # y nach oben
    svg = [svg_header(int(W * sc + 2 * mx) + 40, int(H * sc + my + 70 + 5 * 20 + 50), "%s - Zuschnitt %s (%s)" % (variant_name, ct["id"], count_text))]
    pts = lambda P: " ".join("%.1f,%.1f" % (X(x), Y(y)) for x, y in P)
    svg.append('<polygon points="%s" fill="#eaf4fb" stroke="#111" stroke-width="2"/>' % pts(cut))
    svg.append('<polygon points="%s" fill="none" stroke="#777" stroke-width="1.2" stroke-dasharray="8 5"/>' % pts(ax))
    if any(e["kind"] != "abnaeher" for e in u.loop):
        svg.append('<polygon points="%s" fill="none" stroke="#1f5fd0" stroke-width="1.5" stroke-dasharray="2 4"/>' % pts(wl))
    for k in u.hinges:                              # Scharnier-Linien (Falz ueber der Strebe)
        for t in u.tris:
            P = u.P[t]
            if k[0] in P and k[1] in P and all(n in P for n in k):
                a, b = to_frame([P[k[0]], P[k[1]]], th, off)
                svg.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#2a9d3a" stroke-width="2" stroke-dasharray="14 4 3 4"/>' % (X(a[0]), Y(a[1]), X(b[0]), Y(b[1])))
                break
    for d in edge_dims(u, th, off):
        mxp, myp = (d["a"][0] + d["b"][0]) / 2, (d["a"][1] + d["b"][1]) / 2
        if d["kind"] == "abnaeher":
            svg.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#d02020" stroke-width="3"/>' % (X(d["a"][0]), Y(d["a"][1]), X(d["b"][0]), Y(d["b"][1])))
        cx = sum(p[0] for p in ax) / len(ax); cy = sum(p[1] for p in ax) / len(ax)
        vx, vy = mxp - cx, myp - cy; L = math.hypot(vx, vy) or 1
        tx, ty = X(mxp + vx / L * 330), Y(myp + vy / L * 330)
        svg.append('<text x="%.1f" y="%.1f" font-size="13" text-anchor="middle" fill="#111">%d mm%s</text>'
                   % (tx, ty, round(d["laenge"]), " (Abnaeher)" if d["kind"] == "abnaeher" else ""))
    if ct["door"]:
        dc = door_cut_poly(u)
        if dc:
            svg.append('<polygon points="%s" fill="#ffffff" stroke="#188038" stroke-width="2.5"/>' % pts(to_frame(dc, th, off)))
            c = centroid(to_frame(dc, th, off))
            svg.append('<text x="%.1f" y="%.1f" font-size="13" text-anchor="middle" fill="#188038">Ausschnitt 1026 x 2043</text>' % (X(c[0]), Y(c[1])))
    ly = int(H * sc + my + 70)
    leg = [("#111", "Schnittkante = Strebenachse + %d mm Ueberstand (Abnaeher: + %d mm Nahtzugabe)" % (OVERSTAND, DART_ALLOW), ""),
           ("#777", "Strebenachse (Knoten zu Knoten, nominal)", "8 5"),
           ("#1f5fd0", "Umfangsnaht (Heizkeil, 2 x %d mm) %d mm ausserhalb der Achse, beide Lagen" % (SEAM_W, WELD_OFF), "2 4"),
           ("#2a9d3a", "Falz ueber der Strebe: Folie nicht schneiden, nicht klemmen", "14 4 3 4"),
           ("#d02020", "Abnaeher: beide Kanten ueberlappen und verschweissen, je Lage", "")]
    for i, (col, txt, dash) in enumerate(leg):
        svg.append('<line x1="16" y1="%d" x2="60" y2="%d" stroke="%s" stroke-width="3" %s/><text x="70" y="%d" font-size="13" fill="#111">%s</text>'
                   % (ly + i * 20, ly + i * 20, col, ('stroke-dasharray="%s"' % dash) if dash else "", ly + 4 + i * 20, txt))
    svg.append('<text x="16" y="%d" font-size="13" fill="#111">Flaeche der Schnittkontur %.2f m2 je Lage - Masse in mm, Blatt je Lage zweimal schneiden (innen/aussen), Ansicht von aussen, Spiegeln erlaubt.</text>'
               % (ly + 5 * 20 + 6, abs(area2(cut)) / 1e6))
    svg.append("</svg>")
    open(path, "w", encoding="utf-8").write("\n".join(svg))


def svg_nesting(v, roll, types_names, path, title):
    nst = roll["nest"]; pl = placed(nst)
    W, L = nst["W"], nst["L"]
    sc = min(1500.0 / L, 340.0 / W); mx, my = 50, 70
    names = sorted({t for t, _ in pl})
    col = {n: COLORS[i % len(COLORS)] for i, n in enumerate(names)}
    svg = [svg_header(int(L * sc + 2 * mx), int(W * sc + my + 70), title)]
    svg.append('<rect x="%d" y="%d" width="%.1f" height="%.1f" fill="#f3f3f3" stroke="#333" stroke-width="2"/>' % (mx, my, L * sc, W * sc))
    for n, P in pl:
        svg.append('<polygon points="%s" fill="%s" fill-opacity="0.55" stroke="#111" stroke-width="1"/>'
                   % (" ".join("%.1f,%.1f" % (mx + x * sc, my + y * sc) for x, y in P), col[n]))
    svg.append('<text x="%d" y="%d" font-size="14" fill="#111">Rolle %.0f mm breit x %.1f m lang (je Lage)  -  Verschnitt %.1f %%  -  Zuschnitte %d</text>'
               % (mx, my + int(W * sc) + 28, W, L / 1000, roll["verschnitt"] * 100, len(pl)))
    for i, n in enumerate(names):
        svg.append('<rect x="%d" y="%d" width="14" height="14" fill="%s"/><text x="%d" y="%d" font-size="13">%s</text>'
                   % (mx + i * 140, my + int(W * sc) + 40, col[n], mx + 20 + i * 140, my + int(W * sc) + 52, types_names.get(n, n)))
    svg.append("</svg>")
    open(path, "w", encoding="utf-8").write("\n".join(svg))


def svg_feldplan(units, G, cls, path, title):
    nodes, tris, edge_tris, nom, meas = G
    owner = {t: u for u in units for t in u.tris}
    pts2 = lambda t: [(nodes[n][0], -nodes[n][1]) for n in tris[t]["nodes"]]
    xs = [p[0] for n in nodes for p in [n]]; ys = [-n[1] for n in nodes]
    x0, x1, y0, y1 = min(xs) - 700, max(xs) + 700, min(ys) - 700, max(ys) + 700
    sc = 900.0 / (x1 - x0); mx, my = 30, 70
    X = lambda x: mx + (x - x0) * sc; Y = lambda y: my + (y - y0) * sc
    svg = [svg_header(int((x1 - x0) * sc + 2 * mx), int((y1 - y0) * sc + my + 110), title)]
    ids = sorted(u.id for u in units); col = {i: COLORS[k % len(COLORS)] for k, i in enumerate(ids)}
    shape_col = {}
    for u in units:
        sg = (u.sig(), u.door); shape_col.setdefault(sg, COLORS[len(shape_col) % len(COLORS)])
    for t in tris:
        P = pts2(t["id"]); u = owner[t["id"]]
        svg.append('<polygon points="%s" fill="%s" fill-opacity="0.45" stroke="none"/>' % (" ".join("%.1f,%.1f" % (X(x), Y(y)) for x, y in P), shape_col[(u.sig(), u.door)]))
    sty = {"rand": ("#111", 4), "fuge": ("#d02020", 3), "scharnier": ("#2a9d3a", 2), "abnaeher": ("#1f5fd0", 4)}
    for k, c in cls.items():
        a, b = nodes[k[0]], nodes[k[1]]; s, w = sty[c]
        svg.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%d" %s/>'
                   % (X(a[0]), Y(-a[1]), X(b[0]), Y(-b[1]), s, w, 'stroke-dasharray="6 4"' if c == "scharnier" else ""))
    for u in units:
        gx = sum(sum(nodes[n][0] for n in tris[t]["nodes"]) / 3 for t in u.tris) / len(u.tris)
        gy = sum(sum(-nodes[n][1] for n in tris[t]["nodes"]) / 3 for t in u.tris) / len(u.tris)
        svg.append('<text x="%.1f" y="%.1f" font-size="13" font-weight="bold" text-anchor="middle" fill="#111">%s</text>' % (X(gx), Y(gy) + 4, u.id + ("T" if u.door else "")))
    ly = int((y1 - y0) * sc + my + 24)
    for i, (txt, c, w, d) in enumerate([("Fuge zwischen zwei Kissen: Doppelschiene, jede Seite klemmt ihre Lagen", "#d02020", 3, ""),
                                         ("Falz ueber der Strebe im Kissen: keine Schiene", "#2a9d3a", 2, "6 4"),
                                         ("Fussrand: einfache Schiene und Bodenbefestigung", "#111", 4, "")]):
        svg.append('<line x1="16" y1="%d" x2="60" y2="%d" stroke="%s" stroke-width="%d" %s/><text x="70" y="%d" font-size="13">%s</text>'
                   % (ly + i * 20, ly + i * 20, c, w, ('stroke-dasharray="%s"' % d) if d else "", ly + 4 + i * 20, txt))
    svg.append('<text x="16" y="%d" font-size="12" fill="#444">Draufsicht (Norden oben), Flaechen gleicher Farbe haben denselben Zuschnitt; T = Tuerfeld mit Planenausschnitt.</text>' % (ly + 76))
    svg.append("</svg>")
    open(path, "w", encoding="utf-8").write("\n".join(svg))


def montage_order(units, G):
    nodes, tris, edge_tris, nom, meas = G
    def key(u):
        z = sum(tris[t]["z"] for t in u.tris) / len(u.tris)
        return (not u.door, round(z / 600), sum(tris[t]["az"] for t in u.tris) / len(u.tris))
    return [u.id for u in sorted(units, key=key)]


def unit_record(u, G, ctype):
    nodes, tris, edge_tris, nom, meas = G
    cut = u.cut_poly()
    return dict(id=u.id, zuschnitt=ctype, tuer=u.door, dreiecke=u.tris, typen=[tris[t]["typ"] for t in u.tris],
                scharniere=[list(k) for k in u.hinges], abnaeher=[list(k) for k in u.darts],
                netto_m2=round(u.net_area / 1e6, 3), schnitt_m2=round(abs(area2(cut)) / 1e6, 3),
                umfangsnaht_m=round(u.weld_len() / 1000, 3), abnaeher_m=round(u.dart_len() / 1000, 3))


# ---- 9. Selbsttests ----------------------------------------------------------------------------------------------------------
def selftest(G, variants, X):
    nodes, tris, edge_tris, nom, meas = G
    ok = []
    def chk(name, cond, info=""):
        ok.append(bool(cond)); print("  [%s] %s %s" % ("ok" if cond else "FEHLER", name, info))
    chk("26 Knoten, 40 Dreiecke, 65 Streben", len(nodes) == 26 and len(tris) == 40 and len(edge_tris) == 65)
    net = sum(tri_area_nom(t, nom) for t in tris) / 1e6
    chk("Netto-Huelle 209,98 m2 +-0,2 %", abs(net - 209.98) / 209.98 < 0.002, "(%.2f m2)" % net)
    lens = sorted(round(nom[k]) for k in edge_tris)
    chk("30 Streben A (3279) + 35 Streben B (3708)", lens.count(3279) == 30 and lens.count(3708) == 35)
    aab = next(t for t in tris if t["typ"] == "AAB"); bbb = next(t for t in tris if t["typ"] == "BBB")
    single = X["single"]
    a1 = abs(area2(single[aab["id"]].cut_poly())) / 1e6; b1 = abs(area2(single[bbb["id"]].cut_poly())) / 1e6
    chk("Dreieck mit 100 mm Ueberstand AAB 6,09 / BBB 7,12 m2 (huelle_folie.md)", abs(a1 - 6.09) < 0.02 and abs(b1 - 7.12) < 0.02, "(%.3f / %.3f)" % (a1, b1))
    for v in variants:
        cov = sorted(t for u in v["units"] for t in u.tris)
        chk("%s: jedes Dreieck genau einer Einheit" % v["id"], cov == list(range(40)))
        # Randbuchhaltung: Summe der Aussenkanten der Einheiten = 2 x Fugen + Rand
        s_out = sum(G[3][e["strut"]] for u in v["units"] for e in u.loop if e["kind"] != "abnaeher")
        s_cls = sum(2 * nom[k] if c == "fuge" else (nom[k] if c == "rand" else 0) for k, c in v["cls"].items())
        chk("%s: Randkanten = 2 x Fugen + Fussrand" % v["id"], abs(s_out - s_cls) < 1e-6)
        b = v["nest"]
        rolls = ([b["gemeinsam"]] if b["gemeinsam"] and not b["bester"].get("getrennt") else b["getrennt"]["rollen"])
        for r in rolls:
            pl = placed(r["nest"]); bad = 0
            for i in range(len(pl)):
                bb = bbox(pl[i][1])
                if bb[0] < -1e-3 or bb[1] < -1e-3 or bb[3] > r["W"] + 1e-3 or bb[2] > r["L"] + 1e-3: bad += 1
                for j in range(i + 1, len(pl)):
                    if overlap(pl[i][1], pl[j][1]): bad += 1
            exp = sum(n for _, _, n in v["types"]) if len(rolls) == 1 else None
            chk("%s: Nesting %s ohne Ueberdeckung, innerhalb der Rolle" % (v["id"], r.get("typ", "gemeinsam")), bad == 0, "(%d Zuschnitte)" % len(pl))
    return all(ok)


# ---- 10. Hauptrechnung -------------------------------------------------------------------------------------------------------
def roll_text(nr):
    b = nr["bester"]
    if b.get("getrennt"):
        return "; ".join("%s: %.0f m x %.1f m" % (r["typ"], r["W"] / 1000, r["L"] / 1000) for r in nr["getrennt"]["rollen"])
    return "gemeinsam %.0f m x %.1f m" % (b["W"] / 1000, b["L"] / 1000)


def main(argv):
    G = load_dome(); nodes, tris, edge_tris, nom, meas = G
    nperm, tperm = symmetry(G)
    net = sum(tri_area_nom(t, nom) for t in tris) / 1e6
    print("Netto-Huelle aus nominalen Kanten: %.2f m2 (R24: 209,9; ohne Tuerfeld 208)" % net)
    single = build_units([[t["id"]] for t in tris], G, "D")
    sols = rhombus_groupings(G, tperm)
    best = None
    for s in sols:
        us = build_units([list(p) for p in s], G, "R")
        key = (len({u.sig() for u in us}), sum(perimeter(u.outline) for u in us))
        if best is None or key < best[0]: best = (key, us)
    rh = best[1]
    D = gore_domain(G, tperm)
    g0 = best_net("S01", D, G)
    gores = [g0] + [rotate_unit(g0, nperm, k, "S%02d" % (k + 1)) for k in range(1, 5)]
    print("symmetrische Rauten-Paarungen: %d, Sektor = %d Dreiecke mit %d Abnaeher" % (len(sols), len(D), len(g0.darts)))
    variants = [
        variant_metrics("V1", "Dreieckskissen (40), geschweisst", single, G, "geschweisst"),
        variant_metrics("V2", "Rautenkissen (20), geschweisst", rh, G, "geschweisst"),
        variant_metrics("V3", "Sektorkissen (5 a 8 Dreiecke), geschweisst", gores, G, "geschweisst"),
        variant_metrics("V4", "Dreiecke (40), nur geklemmt", single, G, "geklemmt"),
        variant_metrics("V4b", "Rauten (20), nur geklemmt", rh, G, "geklemmt"),
    ]
    for v in variants:
        b = v["nest"]["bester"]
        print("%-4s %-44s Einh %2d Formen %d Zuschnitt-Typen %d | Naht %6.1f m (Umfang %6.1f + Abnaeher %5.1f) T-Kreuz %2d Ventile %2d max %5.1f m2 | "
              "Schiene einfach %5.1f doppelt %6.1f m | Rollen %s Verschnitt %.1f %%"
              % (v["id"], v["name"], v["einheiten"], v["formen"], v["zuschnitt_typen"], v["naht_gesamt_m"], v["umfangsnaht_m"], v["abnaeher_m"],
                 v["t_kreuzungen"], v["ventile"], v["max_einheit_m2"], v["schiene_einfach_m"], v["schiene_doppel_m"], roll_text(v["nest"]), b["verschnitt"] * 100))
    # Zusatzzahlen
    d = vertex_defects(G)
    dn = sorted({(x["valence"], round(x["defekt"], 1)) for x in d.values() if not x["rand"]})
    print("Winkeldefekt innerer Knoten (Wertigkeit, Grad):", dn)
    R = math.sqrt(sum(c * c for c in nodes[3]))
    hinge_deg = sorted(dihedral_deg(G, k) for u in rh for k in u.hinges)
    print("Knickwinkel der Falz-Streben der Rauten: %.1f bis %.1f Grad (180 = eben); Kugelradius %.0f mm" % (hinge_deg[0], hinge_deg[-1], R))
    for w in (2000, 3000, 4000, 6000):
        print("  parallele gerade Bahn %d mm breit auf R %.0f mm: Randverkuerzung %.1f %%" % (w, R, strip_shrink(w, R) * 100))
    X = dict(single=single, rh=rh, gores=gores, tperm=tperm)
    print("Selbsttest:")
    ok = selftest(G, variants, X)
    print("Selbsttest gesamt:", "bestanden" if ok else "FEHLER")
    if "--json" in argv or "--svg" in argv:
        write_outputs(G, variants, X, argv, dict(defekte=dn, knick=(hinge_deg[0], hinge_deg[-1]), radius=R))
    return variants, G, X


def types_for_variant(v):
    cts = cut_types(v["units"])
    return cts


def write_outputs(G, variants, X, argv, extra):
    nodes, tris, edge_tris, nom, meas = G
    rec = next(v for v in variants if v["id"] == RECOMMENDED)
    cts = cut_types(rec["units"])
    ctid = {}
    for ct in cts:
        for u in ct["units"]: ctid[u.id] = ct["id"]
    if "--svg" in argv:
        os.makedirs(OUT_SVG, exist_ok=True)
        for ct in cts:
            cnt = "%d Stueck%s" % (len(ct["units"]), ", Tuerfeld" if ct["door"] else "")
            svg_pattern(ct, rec["name"], os.path.join(OUT_SVG, "zuschnitt-%s-%s.svg" % (rec["id"].lower(), ct["id"].lower())), cnt)
        # Nesting: gemeinsame Rolle oder getrennte Rollen
        names = {}
        nm = rec["nest"]
        # Typ-Namen der Nesting-Typen (T1, T2 ...) -> Zuschnitt-Typ (Z..): ueber die Signatur
        tmap = {}
        for t_name, poly, n in rec["types"]:
            for ct in cts:
                if not ct["door"] and signature(ct["rep"].outline) == signature(ct["rep"].outline) and abs(abs(area2(poly)) - abs(area2(ct["rep"].cut_poly()))) < 1.0:
                    tmap[t_name] = ct["id"]
        names = {k: "%s (%d Stueck)" % (v, next(len(c["units"]) for c in cts if c["id"] == v) + sum(len(c["units"]) for c in cts if c["door"] and c["rep"].sig() == next(cc for cc in cts if cc["id"] == v)["rep"].sig())) for k, v in tmap.items()}
        if nm["bester"].get("getrennt"):
            for r in nm["getrennt"]["rollen"]:
                svg_nesting(rec, r, names, os.path.join(OUT_SVG, "nesting-%s-%s.svg" % (rec["id"].lower(), r["typ"].lower())), "%s - Nesting %s" % (rec["name"], names.get(r["typ"], r["typ"])))
        else:
            svg_nesting(rec, nm["gemeinsam"], names, os.path.join(OUT_SVG, "nesting-%s.svg" % rec["id"].lower()), "%s - Nesting auf gemeinsamer Rolle" % rec["name"])
        svg_feldplan(rec["units"], G, rec["cls"], os.path.join(OUT_SVG, "feldplan-%s.svg" % rec["id"].lower()), "%s - Feldplan (welches Kissen liegt wo)" % rec["name"])
        print("SVG geschrieben nach", OUT_SVG)
    if "--json" in argv:
        out = dict(
            meta=dict(
                auftrag="R38", stand="2026-10-31", skript="scripts/plane_nesting.py",
                parameter=dict(ueberstand_mm=OVERSTAND, nahtzugabe_abnaeher_mm=DART_ALLOW, umfangsnaht_ausserhalb_achse_mm=WELD_OFF,
                               nahtbreite_mm=SEAM_W, knotenfreiraum_mm=NODE_CLEAR, rollenbreiten_mm=ROLL_WIDTHS, empfohlen=RECOMMENDED),
                herkunft="Q = R24/huelle_folie.md/keilschiene.md; A = Annahme im Skript; Rollenbreiten laut docs/research/R38.md"),
            varianten=[dict(id=v["id"], name=v["name"], naht=v["gelenk"], einheiten=v["einheiten"], formen=v["formen"],
                            zuschnitt_typen=v["zuschnitt_typen"], zuschnitte_gesamt=v["zuschnitte_gesamt"],
                            schnittlaenge_m=round(v["schnittlaenge_m"], 1), umfangsnaht_m=round(v["umfangsnaht_m"], 1),
                            abnaeher_naht_m=round(v["abnaeher_m"], 1), naht_gesamt_m=round(v["naht_gesamt_m"], 1),
                            t_kreuzungen=v["t_kreuzungen"], ventile=v["ventile"], max_einheit_m2=round(v["max_einheit_m2"], 1),
                            schiene_einfach_m=round(v["schiene_einfach_m"], 1), schiene_doppel_m=round(v["schiene_doppel_m"], 1),
                            streben=v["streben"], verschnitt_prozent=round(v["nest"]["bester"]["verschnitt"] * 100, 1),
                            rollen=roll_text(v["nest"]),
                            rollenbedarf=[dict(typ=r["typ"], breite_mm=r["W"], laenge_m=round(r["L"] / 1000, 2), flaeche_m2=round(r["flaeche"] / 1e6, 1),
                                               verschnitt_prozent=round(r["verschnitt"] * 100, 1)) for r in v["nest"]["getrennt"]["rollen"]],
                            gemeinsame_rolle=None if not v["nest"]["gemeinsam"] else dict(breite_mm=v["nest"]["gemeinsam"]["W"], laenge_m=round(v["nest"]["gemeinsam"]["L"] / 1000, 2),
                                                                                         flaeche_m2=round(v["nest"]["gemeinsam"]["flaeche"] / 1e6, 1),
                                                                                         verschnitt_prozent=round(v["nest"]["gemeinsam"]["verschnitt"] * 100, 1)))
                       for v in variants],
            geometrie=dict(netto_huelle_m2=round(sum(tri_area_nom(t, nom) for t in tris) / 1e6, 2), winkeldefekt_innere_knoten=extra["defekte"],
                           knick_falz_grad=[round(extra["knick"][0], 1), round(extra["knick"][1], 1)], kugelradius_mm=round(extra["radius"])),
            empfehlung=dict(variante=rec["id"], name=rec["name"], montage_reihenfolge=montage_order(rec["units"], G),
                            zuschnitte=[dict(id=ct["id"], anzahl=len(ct["units"]), tuerfeld=ct["door"], einheiten=[u.id for u in ct["units"]],
                                             kante_nominal_mm=[round(nom[e["strut"]]) for e in ct["rep"].loop], schnitt_m2=round(abs(area2(ct["rep"].cut_poly())) / 1e6, 2),
                                             umfangsnaht_m=round(ct["rep"].weld_len() / 1000, 2),
                                             polygon_achse_mm=[[round(x, 1), round(y, 1)] for x, y in to_frame(ct["rep"].outline, *canon_frame(ct["rep"]))],
                                             polygon_schnitt_mm=[[round(x, 1), round(y, 1)] for x, y in to_frame(ct["rep"].cut_poly(), *canon_frame(ct["rep"]))],
                                             tuer_ausschnitt_mm=([[round(x, 1), round(y, 1)] for x, y in to_frame(door_cut_poly(ct["rep"]), *canon_frame(ct["rep"]))] if ct["door"] else None))
                                        for ct in cts],
                            einheiten=[unit_record(u, G, ctid[u.id]) for u in rec["units"]],
                            streben_klassen={"%d-%d" % k: c for k, c in sorted(rec["cls"].items())}),
        )
        json.dump(out, open(OUT_JSON, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("JSON geschrieben nach", OUT_JSON)


if __name__ == "__main__":
    main(sys.argv[1:])
