"""Vollstaendige Laufwegkarte (M10 Schritt 0, D54): alle Hindernisse als Grundriss in zwei Hoehenscheiben (Knie 0,3 m, Kopf 1,7 m ueber Boden), 50-mm-Raster, Abstand zum naechsten Hindernis (Chamfer-Transformation mit Hindernis-Nummer).
Engstelle = Grenze zwischen zwei Hindernis-Einzugsgebieten (Voronoi-Kante) mit Weite 2 x Abstand < 600 mm; rot < 500, gelb 500-600. Erreichbarkeit: Flutung von der Tuer ueber Zellen mit Abstand >= 250 mm (= 500 mm Gang); Bauteil erreichbar, wenn eine geflutete Zelle <= 450 mm vom Grundriss liegt.
Aufruf: python scripts/check_walkways_voll.py   (schreibt docs/walkway-map.md, renders/walkway-map-knie.png, renders/walkway-map-kopf.png)
Hindernisse: Portale (Beet + 115 je Seite, bis 1,5 m), Innentische, Tanks/Pumpentafeln/Puffer-Station (Komponenten-Bounding-Box je Instanz, Z-Bereich), Becken (Kreis), Zehneck-Wand ausser an der Tuer; Plane, Streben, Figuren, Pflanzen nicht."""
import json, math, os, subprocess, sys, tempfile
from PIL import Image, ImageDraw
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLI = r"C:\Program Files\SolidCraft\solidcraft-cli.exe"
cmds = json.load(open(os.path.join(ROOT, "scripts", "dome-script.json")))["commands"]
P = {c["params"]["name"]: float(c["params"]["expression"]) for c in cmds if c["command"] == "parameters.add"}
LAY = json.load(open(os.path.join(ROOT, "data", "layout.json")))
mv = {c["params"]["occurrence"]: c["params"]["matrix"] for c in cmds if c["command"] == "occurrence.move"}
FZ = P["sock_h"]; AP = P["dome_base_d"] / 2 * math.cos(math.radians(18)); DOOR = P["door_edge_az"]
CELL, EXT = int(os.environ.get("WCELL", 50)), 6100; N = 2 * EXT // CELL   # WCELL=100 fuer schnelle Probelaeufe
CACHE = os.path.join(ROOT, "scripts", ".compbox.json")

def comp_box(name):
    """Bounding-Box einer Komponentendatei (lokal) aus eval, gecacht nach Datei und mtime."""
    path = os.path.join(ROOT, "designs", "components", name + ".sc"); key = f"{name}:{os.path.getmtime(path):.0f}"
    cache = json.load(open(CACHE)) if os.path.exists(CACHE) else {}
    if key not in cache:
        out = os.path.join(tempfile.gettempdir(), name + "_box.json"); subprocess.run([CLI, "eval", path, "--json-out", out], capture_output=True)
        bs = json.load(open(out, encoding="utf-8"))["bodies"]
        cache[key] = [min(b["bbox"]["min"][i] for b in bs) for i in range(3)] + [max(b["bbox"]["max"][i] for b in bs) for i in range(3)]
        json.dump(cache, open(CACHE, "w"))
    return cache[key]

def poly(m, bx):
    x0, y0, z0, x1, y1, z1 = bx; c, s = m[0], m[4]
    return [(m[3] + u * c - v * s, m[7] + u * s + v * c) for u, v in ((x0, y0), (x1, y0), (x1, y1), (x0, y1))], (m[11] + z0, m[11] + z1)

sys.path.insert(0, os.path.join(ROOT, "scripts", "workshop")); import sc as WSC, tisch_geom as TG
tp, td = WSC.load_params("nft_tisch")
obst = []   # (name, polygon | ("circle", cx, cy, r), zmin, zmax)
for k, m in mv.items():
    cls = k.split(":")[0]
    if cls == "Beet_aussen_800": l, w = 2640, 800 + 230
    elif cls == "Beet_innen_933": l, w = 1865, 933 + 230
    elif cls == "Tisch_innen":   # Innentisch steht auf Pfosten (Rinnen ab 1,0 m): im Knie nur die Fussplatten (80 mm), keine ganze Tischflaeche
        for (x, y) in TG.geometry("innen", tp, td["typen"]["innen"])["legs"]:
            pl_ = [(m[0] * (x + sx * tp["foot_plate"] / 2) + m[1] * (y + sy * tp["foot_plate"] / 2) + m[3], m[4] * (x + sx * tp["foot_plate"] / 2) + m[5] * (y + sy * tp["foot_plate"] / 2) + m[7]) for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1))]
            obst.append((k + " Fuss", pl_, FZ, FZ + 900))
        continue
    else: l = None
    if l:
        pg, _ = poly(m, (-l / 2, -w / 2, 0, l / 2, w / 2, 0)); obst.append((k, pg, FZ, FZ + 1500)); continue
    if cls in ("Tank_klein", "Tank_gross", "Tank_gross_t3", "Pumpe_klein", "Pumpe_gross", "Puffer_Station", "Puffer_Klein"):
        pg, (za, zb) = poly(m, comp_box({"Puffer_Station": "puffer_station", "Puffer_Klein": "puffer_klein"}.get(cls, cls.lower())))
        if max(math.hypot(*p) for p in pg) < AP + 200: obst.append((k, pg, za, zb))   # Vorbau ausserhalb der Wand (D62) liegt nicht im Innenraum
pools = [("Zentralpool", (0.0, 0.0), LAY["pool"]["d"] / 2 + P["wall"]), ("Zweitbecken", (P["pool2_r"] * math.cos(math.radians(P["pool2_az"])), P["pool2_r"] * math.sin(math.radians(P["pool2_az"]))), LAY["pool2"]["d"] / 2 + 60),
         ("Drittbecken", (P["pool3_r"] * math.cos(math.radians(P["pool3_az"])), P["pool3_r"] * math.sin(math.radians(P["pool3_az"]))), P["pool3_d"] / 2 + 60)]
for nm, c, r in pools: obst.append((nm, ("circle",) + c + (r,), -1e9, 1e9))

def inside_poly(x, y, pg):
    s = 0
    for i in range(len(pg)):
        a, b = pg[i], pg[(i + 1) % len(pg)]; v = (b[0] - a[0]) * (y - a[1]) - (b[1] - a[1]) * (x - a[0]); s |= 1 if v >= 0 else 2
    return s != 3
def cell_xy(i, j): return (-EXT + (i + 0.5) * CELL, -EXT + (j + 0.5) * CELL)
def rasterize(z):
    lab = [[-1] * N for _ in range(N)]   # Hindernis-Nr. (-1 frei, -2 Wand)
    names = []
    for oi, (nm, pg, za, zb) in enumerate(obst):
        if not (za <= z <= zb): continue
        names.append(oi)
        if pg[0] == "circle": _, cx, cy, r = pg; xs, ys = [cx - r, cx + r], [cy - r, cy + r]
        else: xs, ys = [p[0] for p in pg], [p[1] for p in pg]
        for j in range(max(0, int((min(ys) + EXT) // CELL)), min(N, int((max(ys) + EXT) // CELL) + 1)):
            for i in range(max(0, int((min(xs) + EXT) // CELL)), min(N, int((max(xs) + EXT) // CELL) + 1)):
                x, y = cell_xy(i, j)
                if (pg[0] == "circle" and math.hypot(x - cx, y - cy) <= r) or (pg[0] != "circle" and inside_poly(x, y, pg)): lab[j][i] = oi
    nrm = [(math.cos(math.radians(DOOR + 36 * k)), math.sin(math.radians(DOOR + 36 * k))) for k in range(10)]
    dn = (math.cos(math.radians(DOOR)), math.sin(math.radians(DOOR)))
    for j in range(N):
        for i in range(N):
            x, y = cell_xy(i, j)
            if max(x * n[0] + y * n[1] for n in nrm) > AP:
                gap = abs(x * -dn[1] + y * dn[0]) <= P["door_w"] / 2 and x * dn[0] + y * dn[1] > AP - 200   # Tuerloch im Fundamentring
                if not gap and lab[j][i] == -1: lab[j][i] = -2
    return lab
def chamfer(lab):
    INF = 10 ** 9; d = [[0 if lab[j][i] != -1 else INF for i in range(N)] for j in range(N)]; src = [[lab[j][i] for i in range(N)] for j in range(N)]
    def relax(j, i, jj, ii, w):
        if 0 <= jj < N and 0 <= ii < N and d[jj][ii] + w < d[j][i]: d[j][i] = d[jj][ii] + w; src[j][i] = src[jj][ii]
    for j in range(N):
        for i in range(N):
            if d[j][i]:
                for dj, di, w in ((-1, -1, 71), (-1, 0, 50), (-1, 1, 71), (0, -1, 50)): relax(j, i, j + dj, i + di, w)
    for j in range(N - 1, -1, -1):
        for i in range(N - 1, -1, -1):
            if d[j][i]:
                for dj, di, w in ((1, 1, 71), (1, 0, 50), (1, -1, 71), (0, 1, 50)): relax(j, i, j + dj, i + di, w)
    return d, src
def flood(d, thr, seed):
    from collections import deque
    ok = [[False] * N for _ in range(N)]; q = deque()
    si, sj = seed
    best = None
    for dj in range(-12, 13):
        for di in range(-12, 13):
            jj, ii = sj + dj, si + di
            if 0 <= jj < N and 0 <= ii < N and d[jj][ii] >= thr and (best is None or abs(dj) + abs(di) < best[0]): best = (abs(dj) + abs(di), jj, ii)
    if best: ok[best[1]][best[2]] = True; q.append((best[1], best[2]))
    while q:
        j, i = q.popleft()
        for dj, di in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            jj, ii = j + dj, i + di
            if 0 <= jj < N and 0 <= ii < N and not ok[jj][ii] and d[jj][ii] >= thr: ok[jj][ii] = True; q.append((jj, ii))
    return ok
def clusters(cells):
    seen = set(); out = []
    for c in cells:
        if c in seen: continue
        comp = [c]; seen.add(c); k = 0
        while k < len(comp):
            j, i = comp[k]; k += 1
            for dj in (-2, -1, 0, 1, 2):
                for di in (-2, -1, 0, 1, 2):
                    n = (j + dj, i + di)
                    if n in cells and n not in seen: seen.add(n); comp.append(n)
        out.append(comp)
    return out
def polar(i, j):
    x, y = cell_xy(i, j); return round(math.degrees(math.atan2(y, x))), round(math.hypot(x, y))

lines = ["# Laufwegkarte (M10 Schritt 0, D54)", "", "Erzeugt von `scripts/check_walkways_voll.py` aus `scripts/dome-script.json` (Raster 50 mm). Weite = 2 x Abstand zum naechsten Hindernis an der Grenze zweier Hindernisse (Voronoi-Kante). Rot < 500 mm, gelb 500-600 mm. Ort als Azimut (Modellrahmen, Grad) / Radius (mm).", ""]
seed_pt = (AP - 350) * math.cos(math.radians(DOOR)), (AP - 350) * math.sin(math.radians(DOOR)); seed = (int((seed_pt[0] + EXT) // CELL), int((seed_pt[1] + EXT) // CELL))
nm_of = lambda oi: "Wand" if oi == -2 else obst[oi][0]
summary = {}
for sl, h in [s_ for s_ in (("knie", 300), ("kopf", 1700)) if s_[0] in os.environ.get("WSLICES", "knie,kopf")]:
    lab = rasterize(FZ + h); d, src = chamfer(lab)
    red, yel = set(), set()
    for j in range(1, N - 1):
        for i in range(1, N - 1):
            if lab[j][i] != -1: continue
            for dj, di in ((0, 1), (1, 0), (1, 1), (1, -1)):
                a, b = src[j][i], src[j + dj][i + di]
                if a != b and lab[j + dj][i + di] == -1 and d[j][i] >= 25:   # Voronoi-Kante im freien Raum
                    w = d[j][i] + d[j + dj][i + di]
                    if w < 500: red.add((j, i))
                    elif w < 600: yel.add((j, i))
    ok250 = flood(d, 250, seed); ok300 = flood(d, 300, seed)
    if os.environ.get("WDEBUG"):
        for rr in (2300, 2450, 2600):
            print(sl, "r", rr, [(a, d[int((rr * math.sin(math.radians(a)) + EXT) // CELL)][int((rr * math.cos(math.radians(a)) + EXT) // CELL)], int(ok250[int((rr * math.sin(math.radians(a)) + EXT) // CELL)][int((rr * math.cos(math.radians(a)) + EXT) // CELL)])) for a in range(-90, 270, 18)])
    for thr in (150, 200, 220):
        reach = flood(d, thr, seed); print(sl, "Gang >=", 2 * thr, "mm: erreichte Zellen", sum(map(sum, reach)), "Bauteile:", sorted({nm_of(src[j][i]) for j in range(N) for i in range(N) if reach[j][i] and d[j][i] <= thr + 200 and lab[j][i] == -1 and src[j][i] >= 0 and obst[src[j][i]][0].startswith(("Tank", "Pumpe", "Puffer", "Dritt", "Zweit", "Zentral"))}))
    lines += [f"## Scheibe {sl} ({h / 1000:.1f} m ueber Boden)", ""]
    for col, cells in (("rot", red), ("gelb", yel)):
        rows = []
        for comp in clusters(cells):
            if len(comp) < 3: continue
            j, i = min(comp, key=lambda c: d[c[0]][c[1]]); pairs = {tuple(sorted((nm_of(src[c[0]][c[1]]), nm_of(src[c[0] + dj][c[1] + di])))) for c in comp for dj, di in ((0, 1), (1, 0)) if 0 <= c[0] + dj < N and 0 <= c[1] + di < N and src[c[0] + dj][c[1] + di] != src[c[0]][c[1]]}
            wmin = 2 * d[j][i]; ci = sum(c[1] for c in comp) // len(comp); cj = sum(c[0] for c in comp) // len(comp)
            rows.append((wmin, polar(ci, cj), len(comp) * CELL, sorted(pairs)[:2]))
        rows.sort()
        lines += [f"### {col}: {len(rows)} Engstellen", ""] + [f"- Weite ca. {w} mm bei {p[0]} Grad / {p[1]} mm (Laenge ca. {ln} mm): {' | '.join(' x '.join(pr) for pr in pairs)}" for w, p, ln, pairs in rows[:30]] + [""]
        summary[(sl, col)] = len(rows)
    acc = []
    for oi, (nm, pg, za, zb) in enumerate(obst):
        if not (FZ + h >= za and FZ + h <= zb): continue
        cells = [(j, i) for j in range(N) for i in range(N) if ok250[j][i] and lab[j][i] == -1 and src[j][i] == oi and d[j][i] <= 450 + 100]
        acc.append((nm, len(cells) > 0))
    lines += ["### Erreichbarkeit der Bauteile (Zelle mit >= 500 mm Gang <= 450 mm vom Grundriss)", ""] + [f"- {'erreichbar' if a else 'NICHT erreichbar'}: {n}" for n, a in acc if (not a) or n.startswith(("Tank", "Pumpe", "Puffer", "Drittbecken", "Zweitbecken", "Zentralpool"))] + [""]
    # Bild
    S = 3; im = Image.new("RGB", (N * S // 2, N * S // 2), (235, 235, 235)); dr = ImageDraw.Draw(im); sc = S / 2
    for j in range(N):
        for i in range(N):
            if lab[j][i] != -1: col = (70, 70, 70) if lab[j][i] != -2 else (150, 120, 90)
            elif ok300[j][i]: col = (170, 220, 170)
            elif ok250[j][i]: col = (240, 220, 120)
            else: col = (200, 215, 235)
            dr.rectangle([i * sc, (N - 1 - j) * sc, (i + 1) * sc, (N - j) * sc], fill=col)
    for cells, col in ((red, (220, 40, 40)), (yel, (235, 150, 20))):
        for j, i in cells: dr.rectangle([i * sc - 1, (N - 1 - j) * sc - 1, (i + 1) * sc + 1, (N - j) * sc + 1], fill=col)
    dr.text((8, 8), f"Laufwegkarte {sl} ({h} mm): gruen >= 600, gelb 500-600 (Gang), blau nicht erreichbar, rote/orange Linien = Engstellen < 500 / 500-600", fill=(0, 0, 0))
    im.save(os.path.join(ROOT, "renders", f"walkway-map-{sl}.png"))
lines += ["## Zusammenfassung", ""] + [f"- {k[0]} {k[1]}: {v} Engstellen" for k, v in summary.items()]
open(os.path.join(ROOT, "docs", "walkway-map.md"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
print("\n".join(lines[-6:]))
