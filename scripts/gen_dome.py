"""Erzeugt das SolidCraft-Befehlsskript fuer designs/dome.sc (Stufe 1-4 = Plan-Schritte 2-5).
Aufruf: python gen_dome.py <stufe> <out.json>. Masse in mm; alle Annahmen stehen in P."""
import json, math, sys
from geo import build

P = {k: v["value"] for k, v in json.load(open(__import__("os").path.join(__import__("os").path.dirname(__file__), "..", "data", "params.json"))).items()}   # Zahlen stehen einmal in data/params.json (Herkunft, Reife dort)

cmds = []
names = []
def add(c, **p):
    cmds.append({"command": c, "params": p})
    if p.get("body_name"): names.append(p["body_name"])

COLORS = [  # (Namenspraefix, Farbe, Deckkraft) - Schicht 1
    ("T1_", "#b9c0c8", 1), ("T3_", "#cfcfca", 1), ("T4_", "#1c1c1c", 1), ("T5_Wasser", "#3c8ed0", 0.85), ("T6_Wasser", "#3c8ed0", 0.85),
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

def rect_body(name, cx, cy, z0, az_deg, along, across, h):
    """Quader um (cx,cy), Laengsachse 'along' in Richtung az, ab Hoehe z0 (rotierte Skizzenebene)."""
    a = math.radians(az_deg)
    xd = [round(math.cos(a), 6), round(math.sin(a), 6), 0]
    yd = [round(-math.sin(a), 6), round(math.cos(a), 6), 0]
    add("sketch.create", plane={"origin": [cx, cy, z0], "x_dir": xd, "y_dir": yd}, name=name+"_sk")
    add("sketch.rectangle.center", center=[0, 0], corner=[along/2, across/2])
    add("sketch.finish")
    add("solid.extrude", distance=h, operation="new", name=name, body_name=name)

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
    n = 0; dropped = 0
    for a, b in sorted(edges):
        if a not in keep or b not in keep: continue
        A, B = V(a), V(b)
        if any(in_door(tuple(A[i]+(B[i]-A[i])*t/10 for i in range(3))) for t in range(1, 10)):
            dropped += 1; continue
        d = [B[i]-A[i] for i in range(3)]; L = math.sqrt(sum(x*x for x in d)); u = [x/L for x in d]
        ext = 25
        s = [A[i]-u[i]*ext for i in range(3)]
        n += 1
        add("solid.cylinder", radius="strut_r", height=L+2*ext, base=[round(x, 2) for x in s],
            axis=[round(x, 6) for x in u], operation="new", name=f"T1_Strebe_{n:03d}", body_name=f"T1_Strebe_{n:03d}")
    # T3 Sockel: Zehneck-Prisma
    rs = P["dome_base_d"]/2 + P["sock_w"]
    pts10 = [[round(rs*math.cos(math.radians(36*i + 18)), 2), round(rs*math.sin(math.radians(36*i + 18)), 2)] for i in range(10)]
    add("sketch.create", plane="XY", name="T3_Sockel_sk")
    add("sketch.line", points=pts10, closed=True)
    add("sketch.finish")
    add("solid.extrude", distance="sock_h", operation="new", name="T3_Sockel", body_name="T3_Sockel")
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

def vessel(name, cx, cy, fz, d_out, h, wall, water_z):
    add("solid.cylinder", diameter=d_out, height=h, base=[cx, cy, fz], operation="new", name=name, body_name=name)
    add("solid.cylinder", diameter=d_out - 2*wall, height=h, base=[cx, cy, fz + 80], operation="cut", targets=[name], name=name + "_Hohlraum")
    return fz + water_z

def pools(fz):
    """T5 Zentralpool (Wasser D 3,89 m), T6 zweites Becken vor der Tuer (D 1,75 m), Wasserspiegel Z 515 (layout.json)."""
    for nm, src, wall in (("T5_Zentraltank", LAYOUT["pool"], P["wall"]), ("T6_Zweitbecken", LAYOUT["pool2"], 100)):
        x, y = LXY(src["cx"], src["cy"]); wz = vessel(nm, x, y, fz, src["d"] + 2*wall, src["water_z"] + 90, wall, src["water_z"])
        wn = "T5_Wasser" if nm.startswith("T5") else "T6_Wasser"
        add("solid.cylinder", diameter=src["d"] - (20 if nm.startswith("T6") else 0), height=20, base=[x, y, wz - 20], operation="new", name=wn, body_name=wn)

def tanks(fz):
    """T7: 4 Tanks (Kegelboden, Zylinder, Plattformring auf 4 Beinen) + Pump-/Filtermodule, Positionen aus layout.json."""
    for i, t in enumerate(LAYOUT["tanks"], 1):
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
        for k, m in enumerate(t["modules"], 1):
            mx, my = LXY(m["cx"], m["cy"])
            if math.hypot(mx - x, my - y) < t["d"]/2 + 150 or any(math.hypot(mx - px, my - py) < 350 for px, py in placed): continue   # OBJ-Module ueberlappen sich teils: nur freistehende
            placed.append((mx, my))
            rect_body(f"T7_Pumpe_{i}_{k}", mx, my, fz, m["yaw"] + ROT, m["l"], max(m["w"], 20), m["h"])

# T9: 14 halbe IBC-Wannen (layout.json), 8 aussen (mit Pflanzen), 6 innen
def t9(fz):
    for k, b in enumerate(LAYOUT["ibc_beds"], 1):
        x, y = LXY(b["cx"], b["cy"]); yaw = b["yaw"] + ROT; top = b["z1"]
        rect_body(f"T9_Substratbeet_{k:02d}", x, y, fz, yaw, b["length"] - (120 if "plants" in b else 300), b["width"] - (100 if "plants" in b else 0), top)   # Unterkante im OBJ unter dem Boden: auf Boden gekappt
        if "plants" in b:   # Aussenbeete: 3 Reihen x 10 Pflanzen (OBJ: 288 Toepfe, hier reduziert)
            ta = math.radians(yaw)
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
    pr = P["pipe_d"]/2; z = pr
    P0 = pol(9500, -90); P1 = pol(7600, -66); P2 = pol(6030, -66)
    def seg(A, B, nm, op, **kw):
        d = [B[0]-A[0], B[1]-A[1]]; L = math.hypot(*d)
        add("solid.cylinder", radius=pr, height=round(L, 1), base=[round(A[0], 1), round(A[1], 1), z], axis=[round(d[0]/L, 6), round(d[1]/L, 6), 0], operation=op, name=nm, **kw)
    seg(P0, P1, "T10_Zulaufrohr", "new", body_name="T10_Zulaufrohr")
    add("solid.sphere", radius=round(pr*1.15, 1), center=[round(P1[0], 1), round(P1[1], 1), z], operation="join", targets=["T10_Zulaufrohr"], name="T10_Knie")
    seg(P1, P2, "T10_Zulaufrohr_2", "join", targets=["T10_Zulaufrohr"])
    az = -36; apo = (P["dome_base_d"]/2 + P["sock_w"])*math.cos(math.radians(18))
    cx, cy = pol(apo + P["cab_y"]/2 + 20, az)
    rect_body("T11_Schaltschrank", round(cx, 1), round(cy, 1), 0, az+90, P["cab_x"], P["cab_y"], P["cab_z"])

if __name__ == "__main__":
    stage = int(sys.argv[1]); out = sys.argv[2]
    params()
    t1_t3_t4(P["sock_h"]) if False else None
    n, dropped = t1_t3_t4(P["sock_h"])
    if stage >= 2: pools(P["sock_h"]); tanks(P["sock_h"])
    if stage >= 3: t9(P["sock_h"])
    if stage >= 4: t10_t11(P["sock_h"])
    colors()
    json.dump({"commands": cmds}, open(out, "w"), indent=0)
    print(f"stufe {stage}: {len(cmds)} befehle, {n} streben, {dropped} fuer tuer entfernt")
