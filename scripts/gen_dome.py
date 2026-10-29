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
        moves[key].append([round(v, 9) for v in (x[0], y[0], u[0], A[0], x[1], y[1], u[1], A[1], x[2], y[2], u[2], A[2])])
    for key in ("A", "B"):   # erst alle Kopien (alle am Ursprung), dann jede Instanz absolut platzieren
        for _ in range(len(moves[key]) - 1): add("occurrence.copy", component=f"Strebe_{key}")
        for i, mat in enumerate(moves[key], 1): add("occurrence.move", occurrence=f"Strebe_{key}:{i}", matrix=mat, tolerance=1e-6, move_grounded=True)

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
    def in_door(p):
        x, y = rot(p[0], p[1], -da)   # x = radial, y = tangential
        return abs(x - rd) < 150 and abs(y - P["door_off"]) < P["door_w"]/2 + 40 and sock_z - 20 < p[2] < sock_z + P["door_h"] + 40
    import math as _m
    ring = sorted(base, key=lambda k: _m.atan2(V(k)[1], V(k)[0]))   # Basis-Zehneck: 10 Kanten
    edges = set(edges) | {tuple(sorted((ring[i], ring[(i+1) % len(ring)]))) for i in range(len(ring))}
    n = 0; dropped = 0; segs = []
    for a, b in sorted(edges):
        if a not in keep or b not in keep: continue
        A, B = V(a), V(b)
        if any(in_door(tuple(A[i]+(B[i]-A[i])*t/10 for i in range(3))) for t in range(1, 10)):
            dropped += 1; continue
        segs.append((A, B))
    act("03_Kuppel"); place_struts(segs)
    act("02_Gelaende")
    # T13 Erde (kein fester Boden, D13): grosse Erdebene, Oberkante = Bodenniveau sock_h; Becken/Beete schneiden Aussparungen ein
    add("solid.box", length=15000, width=15000, height=2600, center=[0, 0, sock_z - 1300], operation="new", name="T13_Erde", body_name="T13_Erde")
    # T3 Fundamentring (Zehneck, flach, ragt ueber die Erde): Streben sind hier verankert, kein Boden
    rs = P["dome_base_d"]/2 + P["sock_w"]; ri = P["dome_base_d"]/2
    ring = lambda r: [[round(r*math.cos(math.radians(36*i + 18)), 2), round(r*math.sin(math.radians(36*i + 18)), 2)] for i in range(10)]
    add("sketch.create", plane={"origin": [0, 0, sock_z], "x_dir": [1, 0, 0], "y_dir": [0, 1, 0]}, name="T3_Sockel_sk")
    add("sketch.line", points=ring(rs), closed=True)
    add("sketch.line", points=ring(ri), closed=True)
    add("sketch.finish")
    add("solid.extrude", distance=P["ring_h"], operation="new", name="T3_Sockel", body_name="T3_Sockel")
    gx, gy = pol(P["dome_base_d"]/2 + 75, P["door_az"])
    rect_body("T3_Tuerluecke", round(gx, 1), round(gy, 1), sock_z - 10, P["door_az"] + 90, P["door_w"] + 200, 700, P["ring_h"] + 20, op="cut", targets=["T3_Sockel"])
    act("03_Kuppel")
    # T4 Tuer: Rahmen (aussen/innen), Ebene radial zur Tuerflaeche
    ca, sa = math.cos(da), math.sin(da)
    ox, oy = rd*ca - P['door_off']*sa, rd*sa + P['door_off']*ca
    add("sketch.create", plane={"origin": [round(ox, 2), round(oy, 2), sock_z], "x_dir": [round(-sa, 6), round(ca, 6), 0], "y_dir": [0, 0, 1]}, name="T4_Tuer_sk")
    w, h, f = P["door_w"], P["door_h"], 60
    add("sketch.rectangle.two_point", p0=[-w/2, 0], p1=[w/2, h])
    add("sketch.rectangle.two_point", p0=[-w/2+f, 30], p1=[w/2-f, h-f])
    add("sketch.finish")
    add("solid.extrude", distance=60, direction="symmetric", operation="new", name="T4_Tuer", body_name="T4_Tuer")
    return n, dropped

LAYOUT = json.load(open(__import__("os").path.join(__import__("os").path.dirname(__file__), "..", "data", "layout.json")))
ROT = P["door_az"] - 167   # Layout-Drehung (docs/components.md)

def LXY(cx, cy):
    """Layout-Koordinate (OBJ-Azimut) -> Modell-Koordinate (um ROT gedreht)."""
    x, y = rot(cx, cy, math.radians(ROT)); return round(x, 1), round(y, 1)

def pools(fz):
    """T5 Zentralpool (Wasser D 3,89 m, Tiefe pool_depth, eingelassen) und T6 zweites Becken (D 1,75 m) vor der Tuer; Rand ueber dem Boden, Wasserspiegel Z 515.
    Der Sockel bekommt kreisrunde Aussparungen, nichts schwebt."""
    for nm, src, wall, depth, rim in (("T5_Zentraltank", LAYOUT["pool"], P["wall"], P["pool_depth"], P["pool_rim"]),
                                       ("T6_Zweitbecken", LAYOUT["pool2"], 60, P["pool2_depth"], P["pool_rim"])):
        x, y = LXY(src["cx"], src["cy"]); (x, y) = (round(x*1.02, 1), round(y*1.02, 1)) if nm.startswith("T6") else (x, y); d_out = src["d"] + 2*wall; z_bot = fz + src["water_z"] - depth; total = fz + rim - z_bot
        act("02_Gelaende")
        add("solid.cylinder", diameter=d_out + 20, height=total + 10, base=[x, y, z_bot - 5], operation="cut", targets=["T13_Erde"], name=nm + "_Aussparung")
        act("04_Wasserbecken")
        add("solid.cylinder", diameter=d_out, height=total, base=[x, y, z_bot], operation="new", name=nm, body_name=nm)
        add("solid.cylinder", diameter=d_out - 2*wall, height=total, base=[x, y, z_bot + 120], operation="cut", targets=[nm], name=nm + "_Hohlraum")
        wn = "T5_Wasser" if nm.startswith("T5") else "T6_Wasser"
        add("solid.cylinder", diameter=src["d"] - 10, height=fz + src["water_z"] - (z_bot + 120), base=[x, y, z_bot + 120], operation="new", name=wn, body_name=wn)

def tanks(fz):
    act("07_Tanks")
    """T7: 4 Tanks (Kegelboden, Zylinder, Plattformring auf 4 Beinen) + Pump-/Filtermodule, Positionen aus layout.json."""
    for i, t in enumerate(LAYOUT["tanks"], 1):
        act("07_Tanks")
        x, y = LXY(t["cx"], t["cy"]); pl = t["platform"][0]; yaw = pl["yaw"] + ROT; nm = f"T7_Tank_{i}"
        ztop = fz + pl["z1"]; cone_h = pl["z1"] - t["z0"]
        add("solid.cone", diameter=t["d"], top_diameter=60, height=cone_h, base=[x, y, ztop], axis=[0, 0, -1], operation="new", name=nm, body_name=nm)
        add("solid.cylinder", diameter=t["d"], height=t["z0"] + t["h"] - pl["z1"], base=[x, y, ztop], operation="join", targets=[nm], name=nm + "_Zylinder")
        add("solid.cylinder", diameter=t["d"] - 100, height=t["z0"] + t["h"] - pl["z1"], base=[x, y, ztop + 80], operation="cut", targets=[nm], name=nm + "_Hohlraum")
        rect_body(f"T7_Plattform_{i}", x, y, fz + pl["z0"], yaw, pl["length"] - 200, pl["width"] - 200, pl["height"])
        add("solid.cylinder", diameter=t["d"] + 20, height=pl["height"] + 20, base=[x, y, fz + pl["z0"] - 10], operation="cut", targets=[f"T7_Plattform_{i}"], name=f"T7_Plattform_{i}_Loch")
        a = math.radians(yaw)
        for sx in (-1, 1):
            for sy in (-1, 1):
                lx, ly = rot(sx*(pl["length"]/2 - 140), sy*(pl["width"]/2 - 140), a)
                add("solid.cylinder", radius=18, height=pl["z0"], base=[round(x+lx, 1), round(y+ly, 1), fz], operation="join", targets=[f"T7_Plattform_{i}"], name=f"T7_Plattform_{i}_Bein{(sx+1)+(sy+1)//2+1}")
        placed = []
        act("07_Tanks")
        for k, m in enumerate(t["modules"], 1):
            mx, my = LXY(m["cx"], m["cy"])
            if math.hypot(mx - x, my - y) < t["d"]/2 + 150 or any(math.hypot(mx - px, my - py) < 350 for px, py in placed): continue   # OBJ-Module ueberlappen sich teils: nur freistehende
            placed.append((mx, my))
            act("09_Technik")
            act("09_Technik"); rect_body(f"T7_Pumpe_{i}_{k}", mx, my, fz, m["yaw"] + ROT, m["l"], max(m["w"], 20), m["h"])

# T9: 14 halbe IBC-Wannen (layout.json), 8 aussen (mit Pflanzen), 6 innen
def t9(fz):
    for k, b in enumerate(LAYOUT["ibc_beds"], 1):
        x, y = LXY(b["cx"], b["cy"]); yaw = b["yaw"] + ROT; top = b["z1"]
        ln = b["length"] - (400 if "plants" in b else 300) - (500 if k == 4 else 0); wd = b["width"] - (100 if "plants" in b else 0)
        act("05_Beete")
        rect_body(f"T9_Substratbeet_{k:02d}", x, y, fz + b["z0"] + 5, yaw, ln, wd, top - b["z0"] - 5)   # eingelassen wie im OBJ
        act("02_Gelaende")
        rect_body(f"T9_Tasche_{k:02d}", x, y, fz + b["z0"], yaw, ln + 20, wd + 20, -b["z0"] + 1, op="cut", targets=["T13_Erde"])
        if "plants" in b:   # Aussenbeete: 3 Reihen x 10 Pflanzen (OBJ: 288 Toepfe, hier reduziert)
            ta = math.radians(yaw); act("10_Pflanzen")
            for r_ in range(3):
                for c_ in range(10):
                    lx, ly = rot((c_ - 4.5)*270, (r_ - 1)*270, ta)
                    plant(round(x + lx, 1), round(y + ly, 1), fz + top + 95, 90)

plants = [0]
def plant(x, y, z, r=90):
    plants[0] += 1
    add("solid.sphere", radius=r, center=[x, y, z], operation="new", name=f"T12_Salat_{plants[0]:03d}", body_name=f"T12_Salat_{plants[0]:03d}")

def t10_t11(fz):
    # Zulaufrohr (Frischwasser) nur AUSSEN: flach auf dem Boden, Bogen zur Sockelwand nahe dem Zweitbecken (OBJ-Azimut 166 -> Modell -55)
    act("08_Leitungen")
    pr = P["pipe_d"]/2; z = P["sock_h"] + pr
    P0 = pol(9500, -90); P1 = pol(7600, -66); P2 = pol(6030, -66)
    def seg(A, B, nm, op, **kw):
        d = [B[0]-A[0], B[1]-A[1]]; L = math.hypot(*d)
        add("solid.cylinder", radius=pr, height=round(L, 1), base=[round(A[0], 1), round(A[1], 1), z], axis=[round(d[0]/L, 6), round(d[1]/L, 6), 0], operation=op, name=nm, **kw)
    seg(P0, P1, "T10_Zulaufrohr", "new", body_name="T10_Zulaufrohr")
    add("solid.sphere", radius=round(pr*1.15, 1), center=[round(P1[0], 1), round(P1[1], 1), z], operation="join", targets=["T10_Zulaufrohr"], name="T10_Knie")
    seg(P1, P2, "T10_Zulaufrohr_2", "join", targets=["T10_Zulaufrohr"])
    az = -36; apo = (P["dome_base_d"]/2 + P["sock_w"])*math.cos(math.radians(18))
    cx, cy = pol(apo + P["cab_y"]/2 + 20, az)
    act("09_Technik")
    rect_body("T11_Schaltschrank", round(cx, 1), round(cy, 1), P["sock_h"], az+90, P["cab_x"], P["cab_y"], P["cab_z"])

if __name__ == "__main__":
    stage = int(sys.argv[1]); out = sys.argv[2]
    params()
    add("component.rename", component=0, name="Kuppel_Aquaponik")
    for nm in ASSEMBLIES: add("component.create", name=nm, activate=False)
    t1_t3_t4(P["sock_h"]) if False else None
    n, dropped = t1_t3_t4(P["sock_h"])
    if stage >= 2: pools(P["sock_h"]); tanks(P["sock_h"])
    if stage >= 3: t9(P["sock_h"])
    if stage >= 4: t10_t11(P["sock_h"])
    colors()
    json.dump({"commands": cmds}, open(out, "w"), indent=0)
    print(f"stufe {stage}: {len(cmds)} befehle, {n} streben, {dropped} fuer tuer entfernt")
