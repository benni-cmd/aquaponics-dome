"""Erzeugt das SolidCraft-Befehlsskript fuer designs/dome.sc (Stufe 1-4 = Plan-Schritte 2-5).
Aufruf: python gen_dome.py <stufe> <out.json>. Masse in mm; alle Annahmen stehen in P."""
import json, math, os, sys
from geo import build

P = {k: v["value"] for k, v in json.load(open(__import__("os").path.join(__import__("os").path.dirname(__file__), "..", "data", "params.json"))).items()}   # Zahlen stehen einmal in data/params.json (Herkunft, Reife dort)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cmds = []
names = []
def add(c, **p):
    cmds.append({"command": c, "params": p})
    if p.get("body_name"): names.append(p["body_name"])

COLORS = [  # (Namenspraefix, Farbe, Deckkraft) - Schicht 1
    ("T1_", "#b9c0c8", 1), ("T3_", "#cfcfca", 1), ("T13_", "#7a5c3a", 1), ("T4_", "#1c1c1c", 1), ("T5_Wasser", "#3c8ed0", 0.85), ("T6_Wasser", "#3c8ed0", 0.85),
    ("T7_Plattform", "#9a9a96", 1), ("T7_Pumpe", "#555a60", 1), ("T5_", "#93b49a", 1), ("T6_", "#93b49a", 1), ("T7_", "#93b49a", 1), ("T8_", "#f3f3f1", 1), ("T9_", "#ffffff", 1),
    ("T10_Zulaufrohr", "#5fa8e0", 1), ("T10_Schlauch", "#8cc8f0", 1), ("T11_", "#8b9096", 1), ("T12_", "#4c9a3c", 1)]

def colors():
    left = list(names)
    for pre, col, op in COLORS:
        grp = [n for n in left if n.startswith(pre)]
        left = [n for n in left if n not in grp]
        if grp: add("appearance.assign", bodies=grp, color=col, opacity=op)
def rot(x, y, a): c, s = math.cos(a), math.sin(a); return (x*c - y*s, x*s + y*c)
def pol(r, az): a = math.radians(az); return (r*math.cos(a), r*math.sin(a))

def params():
    for k, v in P.items():
        add("parameters.add", name=k, expression=str(v), comment="dome-build Parameter")

def rect_body(name, cx, cy, z0, az_deg, along, across, h, op="new", targets=None):
    """Quader um (cx,cy), Laengsachse 'along' in Richtung az, ab Hoehe z0 (rotierte Skizzenebene)."""
    a = math.radians(az_deg)
    xd = [round(math.cos(a), 6), round(math.sin(a), 6), 0]
    yd = [round(-math.sin(a), 6), round(math.cos(a), 6), 0]
    add("sketch.create", plane={"origin": [cx, cy, z0], "x_dir": xd, "y_dir": yd}, name=name+"_sk")
    add("sketch.rectangle.center", center=[0, 0], corner=[along/2, across/2])
    add("sketch.finish")
    if op == "new": add("solid.extrude", distance=h, operation="new", name=name, body_name=name)
    else: add("solid.extrude", distance=h, operation=op, targets=targets, name=name)

def component_file(fname, cls, assembly, fn):
    """Bauteilklasse als eigene Datei designs/components/<fname>.sc bauen (fn erzeugt Koerper in Weltlage) und im Dom verknuepfen (Instanz im Ursprung)."""
    global cmds, names
    saved, savedn = cmds, names; cmds, names = [], []
    fn(); colors()
    data = cmds; cmds, names = saved, savedn
    tmp = os.path.join(ROOT, "scripts", "_comp.json"); json.dump({"commands": data}, open(tmp, "w"))
    out = os.path.join(ROOT, "designs", "components", fname + ".sc")
    r = __import__("subprocess").run([r"C:\Program Files\SolidCraft\solidcraft-cli.exe", "run", tmp, "--save", out, "--quiet"], capture_output=True, text=True)
    if r.returncode: raise SystemExit(f"Komponente {fname} fehlgeschlagen: {r.stderr[-400:]}{r.stdout[-400:]}")
    os.remove(tmp)
    act(assembly); add("component.insert_design", path=out.replace("\\", "/"), name=cls)

ASSEMBLIES = ["01_Layout", "02_Gelaende", "03_Kuppel", "04_Wasserbecken", "05_Beete", "06_NFT", "07_Tanks", "08_Leitungen", "09_Technik", "10_Pflanzen"]

def act(name):
    """Baugruppe aktivieren: neue Koerper/Instanzen entstehen darin (Wurzel bleibt frei von losen Koerpern)."""
    add("component.activate", component=name)

def place_struts(segs):
    """Streben als Instanzen der Komponenten strebe_a/strebe_b (component.insert_design + occurrence.copy), Platzierung per Matrix."""
    R = P["dome_base_d"]/2; cnt = {"A": 0, "B": 0}
    for key, fct in (("A", 0.5465), ("B", 0.6180)):
        add("component.insert_design", path=os.path.join(ROOT, "designs", "components", f"strebe_{key.lower()}.sc").replace("\\", "/"), name=f"Strebe_{key}")
    moves = {"A": [], "B": []}
    for A, B in segs:
        d = [B[i]-A[i] for i in range(3)]; L = math.sqrt(sum(x*x for x in d)); u = [x/L for x in d]
        key = "A" if abs(L - 0.5465*R) < abs(L - 0.6180*R) else "B"
        h = [1, 0, 0] if abs(u[0]) < 0.9 else [0, 1, 0]
        x = [h[1]*u[2]-h[2]*u[1], h[2]*u[0]-h[0]*u[2], h[0]*u[1]-h[1]*u[0]]; xl = math.sqrt(sum(q*q for q in x)); x = [q/xl for q in x]
        y = [u[1]*x[2]-u[2]*x[1], u[2]*x[0]-u[0]*x[2], u[0]*x[1]-u[1]*x[0]]
        o = P["strut_end_offset"]   # Strebe beginnt 120 mm hinter dem Knoten (Komponente = Knoten-Knoten minus 2 x Endversatz)
        moves[key].append([round(v, 9) for v in (x[0], y[0], u[0], A[0] + u[0]*o, x[1], y[1], u[1], A[1] + u[1]*o, x[2], y[2], u[2], A[2] + u[2]*o)])
    for key in ("A", "B"):   # erst alle Kopien (alle am Ursprung), dann jede Instanz absolut platzieren
        for _ in range(len(moves[key]) - 1): add("occurrence.copy", component=f"Strebe_{key}")
        for i, mat in enumerate(moves[key], 1): add("occurrence.move", occurrence=f"Strebe_{key}:{i}", matrix=mat, tolerance=1e-6, move_grounded=True)

def erde_fn(sock_z):
    add("solid.box", length=15000, width=15000, height=2600, center=[0, 0, sock_z - 1300], operation="new", name="T13_Erde", body_name="T13_Erde")
    for nm, src, wall, depth in (("Pool", LAYOUT["pool"], P["wall"], P["pool_depth"]), ("Zweitbecken", LAYOUT["pool2"], 60, P["pool2_depth"])):
        x, y, d_out, z_bot, total = pool_dims(sock_z, src, wall, depth, nm)
        add("solid.cylinder", diameter=d_out + 20, height=total + 10, base=[x, y, z_bot - 5], operation="cut", targets=["T13_Erde"], name=nm + "_Aussparung")
    for k, b in enumerate(LAYOUT["ibc_beds"], 1):
        x, y = bed_xy(b); ln, wd = bed_dims(k, b)
        rect_body(f"T9_Tasche_{k:02d}", x, y, sock_z + b["z0"] - 200, bed_yaw(b), ln + 20, wd + 20, -b["z0"] + 201, op="cut", targets=["T13_Erde"])

def ring_fn(sock_z):
    rs = P["dome_base_d"]/2 + P["sock_w"]; ri = P["dome_base_d"]/2
    ring = lambda r: [[round(r*math.cos(math.radians(36*i + 18)), 2), round(r*math.sin(math.radians(36*i + 18)), 2)] for i in range(10)]
    add("sketch.create", plane={"origin": [0, 0, sock_z], "x_dir": [1, 0, 0], "y_dir": [0, 1, 0]}, name="T3_Sockel_sk")
    add("sketch.line", points=ring(rs), closed=True)
    add("sketch.line", points=ring(ri), closed=True)
    add("sketch.finish")
    add("solid.extrude", distance=P["ring_h"], operation="new", name="T3_Sockel", body_name="T3_Sockel")
    gx, gy = pol(P["dome_base_d"]/2*math.cos(math.radians(18)) + 150, P["door_edge_az"])
    rect_body("T3_Tuerluecke", round(gx, 1), round(gy, 1), sock_z - 10, P["door_edge_az"] + 90, P["door_w"] + 200, 700, P["ring_h"] + 20, op="cut", targets=["T3_Sockel"])

def tuer_komplett(segs, base_z):
    """M3 (D36, W20): Werkstatt-Komponente tuer_komplett.sc (T50) als Instanz im Basisfeld BBB. Feld-KS der Komponente: Ursprung Mitte der Basiskante (Knoten 24 -> 22) auf Basisknotenhoehe,
    X tangential (24 -> 22 = gegen den Uhrzeigersinn), Y hangaufwaerts in der Feldebene, Z Feldnormale nach aussen; Neigung der Feldebene aus dem Modell (Basismitte -> Feldspitze, Knoten 6)."""
    az = math.radians(P["door_edge_az"]); ap = P["dome_base_d"]/2 * math.cos(math.radians(18))
    n = (math.cos(az), math.sin(az)); t = (-math.sin(az), math.cos(az))
    ends = {tuple(round(v / 20) for v in q): q for A, B in segs for q in (A, B)}
    apex = min((q for q in ends.values() if abs((math.degrees(math.atan2(q[1], q[0])) - P["door_edge_az"] + 180) % 360 - 180) < 1 and q[2] > base_z + 1000), key=lambda q: q[2])
    tilt = math.atan2(ap - math.hypot(apex[0], apex[1]), apex[2] - base_z); c, s = math.cos(tilt), math.sin(tilt)
    print(f"tuer_komplett: Feldspitze Z {apex[2]:.0f} r {math.hypot(apex[0], apex[1]):.0f}, Neigung {math.degrees(tilt):.2f} Grad")
    act("03_Kuppel"); add("component.insert_design", path=os.path.join(ROOT, "designs", "components", "tuer_komplett.sc").replace("\\", "/"), name="Tuer_Komplett")
    X, Y, Z = (t[0], t[1], 0.0), (-s*n[0], -s*n[1], c), (c*n[0], c*n[1], s)
    add("occurrence.move", occurrence="Tuer_Komplett:1", matrix=[round(v, 9) for v in (X[0], Y[0], Z[0], ap*n[0], X[1], Y[1], Z[1], ap*n[1], X[2], Y[2], Z[2], base_z)], tolerance=1e-6, move_grounded=True)

NODE_FILES = {}   # Knoten-Index (1-26 wie layout.json nodes_list) -> Dateiname
def knoten_anker(segs):
    """26 Knoten (Werkstatt: knoten_<wertigkeit>_n<ii>.sc, Ursprung Knotenmitte, Armrichtungen im OBJ-Rahmen -> Drehung um ROT) an den Strebenenden + 10 Fundamentanker an den Basisknoten (X radial nach aussen)."""
    ends = {}
    for A, B in segs:
        for q in (A, B): ends.setdefault(tuple(round(v / 20) for v in q), []).append(q)
    E = [tuple(sum(v[i] for v in l)/len(l) for i in range(3)) for l in ends.values()]
    base_z = min(e[2] for e in E)
    for i, n in enumerate(LAYOUT["dome"]["nodes_list"], 1):
        x, y = rot(n["x"], n["y"], math.radians(ROT)); e = min(E, key=lambda e: math.hypot(e[0] - x, e[1] - y))
        place_instances(f"Knoten_n{i:02d}", os.path.join(ROOT, "designs", "components", f"knoten_{n['valence']}_n{i:02d}.sc"), [(round(e[0], 1), round(e[1], 1), round(e[2], 1), ROT)], "03_Kuppel")
    anchors = [(round(e[0], 1), round(e[1], 1), round(e[2], 1), math.degrees(math.atan2(e[1], e[0]))) for e in E if abs(e[2] - base_z) < 5]
    place_instances("Fundamentanker", os.path.join(ROOT, "designs", "components", "fundamentanker.sc"), anchors, "02_Gelaende")

def t1_t3_t4(sock_z):
    pts, edges = build(P["freq"])
    zcut = -0.01
    keep = {k for k, p in pts.items() if p[2] >= zcut}
    zb = 0.0
    # Radius so, dass der Basisring-Umkreis = dome_base_d/2
    R = (P["dome_base_d"]/2) / math.sqrt(1 - zb*zb)
    zsq = P['dome_h']/((1-zb)*R)   # Hoehe/Breite = 0,5: Kuppel in Z gestaucht
    cz = sock_z + P['strut_r'] + 30 - zb*R*zsq   # Basisring liegt auf dem Sockel
    # Basisring auf gleiche Hoehe setzen; Drehung: Basisknoten bei Azimut 0
    base = [k for k in keep if abs(pts[k][2]) < 1e-3]
    a0 = math.atan2(pts[base[0]][1], pts[base[0]][0])
    def V(k):
        x, y, z = pts[k]
        if abs(z) < 1e-3: z = zb
        x, y = rot(x, y, -a0 + math.radians(18))   # Knoten bei door_az + 36k (OBJ: Tuer sitzt an einem Basisknoten)
        return (x*R, y*R, z*R*zsq + cz)
    # Tuerflaeche: Streben, die den Tuerquader kreuzen, entfallen
    da = math.radians(P["door_az"]); rd = R*math.sqrt(1-zb*zb) - 100
    n = 0; dropped = 0; segs = []
    for a, b in sorted(edges):
        if a not in keep or b not in keep: continue
        A, B = V(a), V(b)
        if a in base and b in base:   # Basiskante des Tuerdreiecks (R13) entfaellt: Schwelle/Pfosten ersetzen sie
            ma = math.degrees(math.atan2((A[1]+B[1])/2, (A[0]+B[0])/2))
            if abs((ma - P["door_edge_az"] + 180) % 360 - 180) < 2: dropped += 1; continue
        segs.append((A, B))
    act("03_Kuppel"); place_struts(segs); knoten_anker(segs)
    act("02_Gelaende")
    # 02_Gelaende: Erdflaeche (mit Aussparungen fuer Becken und Beete) und Fundamentring (Streben hier verankert) als Komponenten
    component_file("erdflaeche", "Erdflaeche", "02_Gelaende", lambda: erde_fn(sock_z))
    component_file("fundamentring", "Fundamentring", "02_Gelaende", lambda: ring_fn(sock_z))
    act("03_Kuppel")
    tuer_komplett(segs, cz)
    return n, dropped

LAYOUT = json.load(open(__import__("os").path.join(__import__("os").path.dirname(__file__), "..", "data", "layout.json")))
ROT = P["door_az"] - 167   # Layout-Drehung (docs/components.md)
DOOR_OBJ_AZ = 149.2   # D36: Tuer im Basisfeld BBB; im Modell door_edge_az = DOOR_OBJ_AZ + ROT (-72 = 149,2 - 221,2)

def LXY(cx, cy):
    """Layout-Koordinate (OBJ-Azimut) -> Modell-Koordinate (um ROT gedreht)."""
    x, y = rot(cx, cy, math.radians(ROT)); return round(x, 1), round(y, 1)

def pool_dims(fz, src, wall, depth, nm):
    x, y = LXY(src["cx"], src["cy"])
    if nm.startswith("Zweit"):   # D36: Zweitbecken auf die Tuerachse (OBJ-Azimut 149,2, Tuer im Basisfeld BBB), Radius wie im OBJ mal pool2_r_factor (D42: Abstand zum Innentisch und Zentralpool)
        r = math.hypot(src["cx"], src["cy"]) * P["pool2_r_factor"]; x, y = LXY(r * math.cos(math.radians(DOOR_OBJ_AZ)), r * math.sin(math.radians(DOOR_OBJ_AZ)))
    else: x, y = 0.0, 0.0   # D35: Zentralpool auf der Kuppelachse (alle Ringe konzentrisch; OBJ-Abweichung 41 mm)
    d_out = src["d"] + 2*wall; z_bot = fz + src["water_z"] - depth
    return x, y, d_out, z_bot, fz + P["pool_rim"] - z_bot

def bed_obj(b):
    """D41: Beet exakt auf der Sektorachse (OBJ-Azimut 5,3 + 36 k, Apothem = ap_c der Tische aus nft_tisch.json = Radialbudget, yaw = Azimut + 90): Tischmitte = Beetmitte ohne OBJ-Streuung (Beetlage nur ~100 mm genau, D21). Rueckgabe (x, y, yaw) im OBJ-Rahmen."""
    az = 5.3 + 36.0 * round((b["az"] - 5.3) / 36.0); ap = NFT_APC["aussen" if "plants" in b else "mitte"]
    return ap * math.cos(math.radians(az)), ap * math.sin(math.radians(az)), az + 90.0

def bed_xy(b):
    x, y = LXY(*bed_obj(b)[:2]); return x, y

def bed_yaw(b): return bed_obj(b)[2] + ROT

def bed_dims(k, b):
    return (BED_OUT_L, BED_OUT_W) if "plants" in b else (b["length"], b["width"])   # echte Wannenmasse der Werkstatt-Beete (Tasche +20 mm Spiel); Aussenbeet 2640 x 800 (W17, D29)
BED_OUT_L, BED_OUT_W = 2640, 800

def pool_fn(fz, nm, src, wall, depth, tn):
    x, y, d_out, z_bot, total = pool_dims(fz, src, wall, depth, nm)
    add("solid.cylinder", diameter=d_out, height=total, base=[x, y, z_bot], operation="new", name=tn, body_name=tn)
    add("solid.cylinder", diameter=d_out - 2*wall, height=total, base=[x, y, z_bot + 120], operation="cut", targets=[tn], name=tn + "_Hohlraum")
    wn = tn.split("_")[0] + "_Wasser"
    add("solid.cylinder", diameter=src["d"] - 10, height=fz + src["water_z"] - (z_bot + 120), base=[x, y, z_bot + 120], operation="new", name=wn, body_name=wn)

def pools(fz):
    """04_Wasserbecken: Zentralpool (T5) und Zweitbecken (T6) als Komponenten; eingelassen, Rand Z 650, Wasserspiegel Z 515."""
    component_file("pool_zentral", "Pool", "04_Wasserbecken", lambda: pool_fn(fz, "Pool", LAYOUT["pool"], P["wall"], P["pool_depth"], "T5_Zentraltank"))
    component_file("zweitbecken", "Zweitbecken", "04_Wasserbecken", lambda: pool_fn(fz, "Zweitbecken", LAYOUT["pool2"], 60, P["pool2_depth"], "T6_Zweitbecken"))

def rect_corners(cx, cy, l, w, yaw):
    c, s = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
    return [(cx + u*c - v*s, cy + u*s + v*c) for u, v in ((-l/2, -w/2), (l/2, -w/2), (l/2, w/2), (-l/2, w/2))]

def rect_gap(A, B):
    """Trennabstand zweier Rechtecke im Grundriss (SAT; negativ = Ueberlappung)."""
    g = -1e9
    for Q in (A, B):
        for i in range(4):
            e = (Q[(i+1) % 4][0] - Q[i][0], Q[(i+1) % 4][1] - Q[i][1]); m = math.hypot(*e); n = (-e[1]/m, e[0]/m)
            pa = [p[0]*n[0] + p[1]*n[1] for p in A]; pb = [p[0]*n[0] + p[1]*n[1] for p in B]
            g = max(g, min(pa) - max(pb), min(pb) - max(pa))
    return g

def tank_offsets():
    """D22: OBJ-Plattformen von Tank 1/3 (-83 mm) und Tank 2 / Innenbeet 12 (-77 mm) ueberlappen im Grundriss, die Werkstatt-Rahmen (Beine an den Ecken) stossen dort durch Nachbarplattform bzw. Beet.
    Der kleinere Tank samt Pumpentafeln rueckt um (tank_clear - Luecke) von der Nachbarplattform bzw. dem Beet weg (Layout-Koordinaten)."""
    T = LAYOUT["tanks"]; pl = [t["platform"][0] for t in T]; off = {i: [0.0, 0.0] for i in range(len(T))}
    rc = lambda i: rect_corners(pl[i]["cx"] + off[i][0], pl[i]["cy"] + off[i][1], pl[i]["length"], pl[i]["width"], pl[i]["yaw"])
    obstacles = lambda i: [(rc(j), (pl[j]["cx"] + off[j][0], pl[j]["cy"] + off[j][1])) for j in range(len(T)) if j != i and pl[j]["length"] >= pl[i]["length"] and not (pl[j]["length"] == pl[i]["length"] and j < i)] +         [(rect_corners(*bed_obj(b)[:2], b["length"], b["width"], bed_obj(b)[2]), bed_obj(b)[:2]) for b in LAYOUT["ibc_beds"] if "plants" not in b]
    p2r = math.hypot(LAYOUT["pool2"]["cx"], LAYOUT["pool2"]["cy"]) * P["pool2_r_factor"]; p2 = (p2r * math.cos(math.radians(DOOR_OBJ_AZ)), p2r * math.sin(math.radians(DOOR_OBJ_AZ))); p2h = LAYOUT["pool2"]["d"] / 2 + 60
    def pool2_obst(i):   # D42: Zweitbecken als Quadrat (Seite = Aussendurchmesser) mit einer Seite zum Tank gedreht = beruehrt den Kreis nur in Tankrichtung
        yaw = math.degrees(math.atan2(pl[i]["cy"] + off[i][1] - p2[1], pl[i]["cx"] + off[i][0] - p2[0])); return (rect_corners(p2[0], p2[1], 2 * p2h, 2 * p2h, yaw), p2)
    for _ in range(3):
        for i in range(len(T)):
            for R, (ox, oy) in obstacles(i) + [pool2_obst(i)]:
                gap = rect_gap(rc(i), R)
                if gap < P["tank_clear"]:
                    dx, dy = pl[i]["cx"] + off[i][0] - ox, pl[i]["cy"] + off[i][1] - oy; d = math.hypot(dx, dy); mv = P["tank_clear"] - gap
                    off[i][0] += dx/d*mv; off[i][1] += dy/d*mv
    return off

def tanks(fz):
    """07_Tanks/09_Technik: 4 Tanks (Werkstatt: tank_klein x2, tank_gross, tank_gross_t3) und 8 Pumpentafeln (pumpe_klein/gross, je Tank 2) als Instanzen; Ursprung Tank = Mitte Standflaeche am Boden, Drehung = Plattform-yaw; Positionen aus layout.json plus tank_offsets."""
    tk = {"klein": [], "gross": [], "gross_t3": []}; pk = {"klein": [], "gross": []}; off = tank_offsets()
    for i, t in enumerate(LAYOUT["tanks"]):
        dx, dy = off[i]; x, y = LXY(t["cx"] + dx, t["cy"] + dy); yaw = t["platform"][0]["yaw"] + ROT
        tk["klein" if t["d"] < 800 else ("gross_t3" if i == 2 else "gross")].append((x, y, fz, yaw))
        placed = []
        for m in t["modules"]:
            if m["l"] < 500: continue   # 384-mm-Kassetten = Stuetzrippen der Plattform (D16, Teil der Tank-Komponente)
            mx, my = LXY(m["cx"] + dx, m["cy"] + dy)
            if any(math.hypot(mx - px, my - py) < 100 for px, py in placed): continue   # OBJ-Duplikate zusammenfassen
            placed.append((mx, my)); pk["klein" if t["d"] < 800 else "gross"].append((mx, my, fz, m["yaw"] + ROT))
    for v, items in tk.items():
        if items: place_instances("Tank_" + v, os.path.join(ROOT, "designs", "components", f"tank_{v}.sc"), items, "07_Tanks")
    for v, items in pk.items():
        place_instances("Pumpe_" + v, os.path.join(ROOT, "designs", "components", f"pumpe_{v}.sc"), items, "09_Technik")

def place_instances(cls, path, items, assembly):
    """Werkstatt-Komponente verknuepfen (eine Definition) und je Eintrag (x, y, z, yaw_grad) eine Instanz setzen (erst alle Kopien am Ursprung, dann absolut verschieben)."""
    act(assembly); add("component.insert_design", path=path.replace("\\", "/"), name=cls)
    for _ in range(len(items) - 1): add("occurrence.copy", component=cls)
    for i, (x, y, z, yaw) in enumerate(items, 1):
        c, s_ = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
        add("occurrence.move", occurrence=f"{cls}:{i}", matrix=[round(v, 9) for v in (c, -s_, 0, x, s_, c, 0, y, 0, 0, 1, z)], tolerance=1e-6, move_grounded=True)

# T9: 14 halbe IBC-Wannen (layout.json) als Instanzen der Werkstatt-Komponenten ibc_beet_{aussen_933,aussen_993,innen_933}; Ursprung = Mitte Wannenunterseite
def t9(fz):
    groups = {}
    for k, b in enumerate(LAYOUT["ibc_beds"], 1):
        x, y = bed_xy(b)
        v = "innen_933" if "plants" not in b else "aussen_800"
        groups.setdefault(v, []).append((x, y, fz + b["z0"], bed_yaw(b)))
    for v, items in groups.items():
        place_instances("Beet_" + v, os.path.join(ROOT, "designs", "components", f"ibc_beet_{v}.sc"), items, "05_Beete")

# T8: 24 NFT-Tische Rev. B (W16, D18) als Instanzen nft_tisch_{aussen,mitte,innen}: je Sektor eine Tischinstanz, Tischkoordinaten X tangential, Y radial INNEN, yaw = Azimut + 90 Grad (volle 360 Grad); Ursprung = Mitte Standflaeche am Boden.
# Portaltische (aussen, mitte) stehen auf der Beetmitte (Radius des Beets auf der Sektorachse), wie die Beete um outer_bed_shift/inner_bed_shift nach innen (Radialbudget D28/D29, M7); innen auf ap_c 1864.
SECTORS = {"innen": list(range(10)), "mitte": [0, 1, 2, 7, 8, 9], "aussen": [0, 1, 2, 3, 6, 7, 8, 9]}
NFT_APC = {k: v["ap_c"] for k, v in json.load(open(os.path.join(ROOT, "data", "components", "nft_tisch.json"), encoding="utf-8"))["typen"].items()}   # Radialbudget (W17): Tischmitte = Beetmitte
NFT_POTS = []                                                # Rinnen-Topfpositionen (x, y, z Topfboden), von nft() gefuellt, von pots() gesetzt

def nft(fz):
    tp = json.load(open(os.path.join(ROOT, "data", "nft_pots.json")))["typen"]
    for typ, sectors in SECTORS.items():
        items = []
        for i in sectors:
            az = 5.3 + 36.0 * i; ap = NFT_APC[typ]
            x, y = LXY(ap * math.cos(math.radians(az)), ap * math.sin(math.radians(az))); yaw = az + 90 + ROT; c, s = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
            items.append((x, y, fz, yaw))
            for u, v, z in tp[typ]["pots"]: NFT_POTS.append((round(x + u*c - v*s, 1), round(y + u*s + v*c, 1), round(fz + z, 1)))
        place_instances("Tisch_" + typ, os.path.join(ROOT, "designs", "components", f"nft_tisch_{typ}.sc"), items, "06_NFT")

# T10/T12: Netztoepfe und Salatkoepfe in den 8 Aussenbeeten als Instanzen (Positionen je Topf aus data/pots.json = OBJ, Beet-Koordinaten); Netztopf-Ursprung Mitte Boden, Salatkopf-Ursprung Kragenoberkante (Boden + 63)
PLANTS = json.load(open(os.path.join(ROOT, "data", "pots.json")))
def bed_pot_grid():
    """Topfraster im Aussenbeet 2640 x 800 (D34): quadratisches Raster `pot_pitch` (Salatkopf 95-125 mm breit), `pot_margin` zur Wanne, symmetrisch zur Beetmitte; (u laengs, v quer)."""
    nu, nv = int((BED_OUT_L - 2*P["pot_margin"]) // P["pot_pitch"]) + 1, int((BED_OUT_W - 2*P["pot_margin"]) // P["pot_pitch"]) + 1
    return [((i - (nu - 1)/2) * P["pot_pitch"], (j - (nv - 1)/2) * P["pot_pitch"]) for i in range(nu) for j in range(nv)]

def pots(fz, with_heads):
    pots_, heads = [], []
    grid = bed_pot_grid()
    for k, b in enumerate(LAYOUT["ibc_beds"]):
        if "plants" not in b: continue
        cx, cy = bed_xy(b); yaw = bed_yaw(b); c, s = math.cos(math.radians(yaw)), math.sin(math.radians(yaw))
        for u, v in grid:
            x, y = round(cx + u*c - v*s, 1), round(cy + u*s + v*c, 1); zb = round(fz + P["pot_base_z"], 1)
            pots_.append((x, y, zb, 0)); heads.append((x, y, zb + 63, 0))
    for x, y, zb in NFT_POTS: pots_.append((x, y, zb, 0)); heads.append((x, y, round(zb + 63, 1), 0))   # Rinnen-Toepfe (D33: 586, Lochabstand 200)
    place_instances("Netztopf", os.path.join(ROOT, "designs", "components", "netztopf.sc"), pots_, "10_Pflanzen")
    if with_heads: place_instances("Salatkopf", os.path.join(ROOT, "designs", "components", "salatkopf.sc"), heads[:int(P["salat_n"])], "10_Pflanzen")

plants = [0]
def plant(x, y, z, r=90):
    plants[0] += 1
    add("solid.sphere", radius=r, center=[x, y, z], operation="new", name=f"T12_Salat_{plants[0]:03d}", body_name=f"T12_Salat_{plants[0]:03d}")

def rohr_fn():
    # Zulaufrohr (Frischwasser) nur AUSSEN: flach auf dem Boden, Bogen zur Fundamentringwand nahe dem Zweitbecken (OBJ-Azimut 166 -> Modell -55)
    pr = P["pipe_d"]/2; z = P["sock_h"] + pr
    P0 = pol(9500, -90); P1 = pol(7600, -48); P2 = pol(6120, -48)
    def seg(A, B, nm, op, **kw):
        d = [B[0]-A[0], B[1]-A[1]]; L = math.hypot(*d)
        add("solid.cylinder", radius=pr, height=round(L, 1), base=[round(A[0], 1), round(A[1], 1), z], axis=[round(d[0]/L, 6), round(d[1]/L, 6), 0], operation=op, name=nm, **kw)
    seg(P0, P1, "T10_Zulaufrohr", "new", body_name="T10_Zulaufrohr")
    add("solid.sphere", radius=round(pr*1.15, 1), center=[round(P1[0], 1), round(P1[1], 1), z], operation="join", targets=["T10_Zulaufrohr"], name="T10_Knie")
    seg(P1, P2, "T10_Zulaufrohr_2", "join", targets=["T10_Zulaufrohr"])

def schrank_fn():
    az = -36; apo = (P["dome_base_d"]/2 + P["sock_w"])*math.cos(math.radians(18))
    cx, cy = pol(apo + P["cab_y"]/2 + 20, az)
    rect_body("T11_Schaltschrank", round(cx, 1), round(cy, 1), P["sock_h"], az+90, P["cab_x"], P["cab_y"], P["cab_z"])

def t10_t11(fz):
    component_file("zulaufrohr", "Zulaufrohr", "08_Leitungen", rohr_fn)
    component_file("schaltschrank", "Schaltschrank", "09_Technik", schrank_fn)

if __name__ == "__main__":
    stage = int(sys.argv[1]); out = sys.argv[2]
    params()
    add("component.rename", component=0, name="Kuppel_Aquaponik")
    for nm in ASSEMBLIES: add("component.create", name=nm, activate=False)
    t1_t3_t4(P["sock_h"]) if False else None
    n, dropped = t1_t3_t4(P["sock_h"])
    if stage >= 2: pools(P["sock_h"]); tanks(P["sock_h"])
    if stage >= 3: t9(P["sock_h"]); nft(P["sock_h"])
    if stage >= 5: pots(P["sock_h"], P["salat_n"] > 0)
    if stage >= 4: t10_t11(P["sock_h"])
    colors()
    json.dump({"commands": cmds}, open(out, "w"), indent=0)
    print(f"stufe {stage}: {len(cmds)} befehle, {n} streben, {dropped} fuer tuer entfernt")
