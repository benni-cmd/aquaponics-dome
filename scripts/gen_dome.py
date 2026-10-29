"""Erzeugt das SolidCraft-Befehlsskript fuer designs/dome.sc (Stufe 1-4 = Plan-Schritte 2-5).
Aufruf: python gen_dome.py <stufe> <out.json>. Masse in mm; alle Annahmen stehen in P."""
import json, math, sys
from geo import build

P = dict(  # Parameter-Tabelle, von Ben bestaetigt 29.10.2026: Basis 12 m, Hoehe 6 m; Rest per Pixelvergleich mit ref-4 (Basis = 12 m)
    dome_base_d=12000, dome_h=6000, freq=2, sock_h=400, sock_w=250, strut_r=45,
    door_w=1000, door_h=2000, door_az=-54, door_off=1100,
    t5_d=3800, t5_h=1200, t6_d=2200, t6_h=900, t7_d=1100, t7_h=1200, t7_stand=500,
    bed_n=10, bed_len=2300, bed_w=900, bed_h=950, bed_r=4500,
    tub_len=2200, tub_w=720, tub_h=550,
    pipe_d=300, cab_x=800, cab_y=500, cab_z=1200, wall=160)

cmds = []
def add(c, **p): cmds.append({"command": c, "params": p})
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
        x, y = rot(x, y, -a0)
        return (x*R, y*R, z*R*zsq + cz)
    # Tuerflaeche: Streben, die den Tuerquader kreuzen, entfallen
    da = math.radians(P["door_az"]); rd = R*math.sqrt(1-zb*zb)*math.cos(math.radians(18))
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
    pts10 = [[round(rs*math.cos(math.radians(36*i)), 2), round(rs*math.sin(math.radians(36*i)), 2)] for i in range(10)]
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

def tank(name, cx, cy, z0, d, h, wall_expr, stand=0):
    add("solid.cylinder", diameter=d, height=h, base=[cx, cy, z0+stand], operation="new", name=name, body_name=name)
    add("solid.cylinder", diameter=f"({d}) - 2*wall", height=h, base=[cx, cy, z0+stand+P["wall"]], operation="cut", targets=[name], name=name+"_Hohlraum")
    for i in range(4 if stand else 0):
        lx, ly = cx+ (P["t7_d"]/2-60)*math.cos(math.radians(90*i+45)), cy+(P["t7_d"]/2-60)*math.sin(math.radians(90*i+45))
        add("solid.cylinder", radius=30, height=stand, base=[round(lx, 1), round(ly, 1), z0], operation="join", targets=[name], name=f"{name}_Fuss{i+1}")

def t5_t7(fz):
    tank("T5_Zentraltank", 0, 450, fz, "t5_d", "t5_h", "wall")
    add("solid.cylinder", diameter="t5_d - 2*wall", height=20, base=[0, 450, fz + P["t5_h"] - 250], operation="new", name="T5_Wasser", body_name="T5_Wasser")
    tank("T6_Mitteltank", 500, -2600, fz, "t6_d", "t6_h", "wall")
    pos = [(-3200, 500), (-2600, -1700), (3200, 300), (2700, 1800), (-1500, -3000), (2400, -2300)]
    for i, (x, y) in enumerate(pos, 1):
        # Schlauch (T10-Gruppe) vom Fasstank zum Rand des Zentraltanks
        dx, dy = 0 - x, 450 - y; dl = math.hypot(dx, dy); ux, uy = dx/dl, dy/dl
        sx, sy, sz = x + ux*P["t7_d"]/2, y + uy*P["t7_d"]/2, fz + P["t7_stand"] + P["t7_h"] - 150
        ex, ey, ez = ux*(dl - P["t5_d"]/2), uy*(dl - P["t5_d"]/2), fz + P["t5_h"] + 60
        d = [ex - (sx - x), ey - (sy - y), ez - sz]; L = math.sqrt(sum(q*q for q in d))
        add("solid.cylinder", radius=25, height=round(L, 1), base=[round(sx, 1), round(sy, 1), sz], axis=[round(q/L, 6) for q in d], operation="new", name=f"T10_Schlauch_{i}", body_name=f"T10_Schlauch_{i}")
        tank(f"T7_Fasstank_{i}", x, y, fz, "t7_d", "t7_h", "wall", stand=P["t7_stand"])

def t8_t9(fz):
    n = P["bed_n"]
    for i in range(n):
        az = 36*i + 18   # Zehneck-Seitenmitten
        cx, cy = pol(P["bed_r"], az)
        blen = P["bed_len"]
        if az == P["door_az"] % 360:   # Bett vor der Tuer: kuerzer und von der Tuer weg
            blen = 1200; t = math.radians(az+90)
            cx, cy = cx + -800*math.cos(t), cy + -800*math.sin(t)
        nm = f"T8_Anbaubett_{i+1:02d}"
        rect_body(nm, round(cx, 1), round(cy, 1), fz+P["bed_h"]-60, az+90, blen, P["bed_w"], 60)
        a = math.radians(az+90)
        for sx in (-1, 1):
            for sy in (-1, 1):
                lx, ly = rot(sx*(blen/2-80), sy*(P["bed_w"]/2-45), a)
                add("solid.cylinder", radius=30, height=P["bed_h"]-60, base=[round(cx+lx, 1), round(cy+ly, 1), fz], operation="join", targets=[nm], name=f"{nm}_Bein{(sx+1)//2*2+(sy+1)//2+1}")
        nc = 6 if blen > 1500 else 3
        for r in range(3):
            for c in range(nc):
                lx, ly = rot((c-(nc-1)/2)*330 + (r % 2)*165 - 82, (r-1)*270, a)   # gestaffelte Reihen
                add("solid.cylinder", diameter=70, height=70, base=[round(cx+lx, 1), round(cy+ly, 1), fz+P["bed_h"]-65], operation="cut", targets=[nm], name=f"{nm}_Loch{r*6+c+1}")
    # T9: vier Substratwannen unter Bett 7 (Azimut 270? -> hier Azimut 234 und 342)
    for k, az in enumerate((126, 198, 234, 342), 1):
        cx, cy = pol(P["bed_r"], az)
        rect_body(f"T9_Substratbeet_{k}", round(cx, 1), round(cy, 1), fz, az+90, P["tub_len"], P["tub_w"], P["tub_h"])

def t10_t11(fz):
    A = (-6577, 2394, 4400); B = (-1344, 1794, fz+1400)
    d = [B[i]-A[i] for i in range(3)]; L = math.sqrt(sum(x*x for x in d)); u = [round(x/L, 6) for x in d]
    add("solid.cylinder", diameter="pipe_d", height=round(L, 1), base=list(A), axis=u, operation="new", name="T10_Zulaufrohr", body_name="T10_Zulaufrohr")
    az = -18; apo = (P["dome_base_d"]/2 + P["sock_w"])*math.cos(math.radians(18))
    cx, cy = pol(apo + P["cab_y"]/2 + 20, az)
    rect_body("T11_Schaltschrank", round(cx, 1), round(cy, 1), 0, az+90, P["cab_x"], P["cab_y"], P["cab_z"])

if __name__ == "__main__":
    stage = int(sys.argv[1]); out = sys.argv[2]
    params()
    t1_t3_t4(P["sock_h"]) if False else None
    n, dropped = t1_t3_t4(P["sock_h"])
    if stage >= 2: t5_t7(P["sock_h"])
    if stage >= 3: t8_t9(P["sock_h"])
    if stage >= 4: t10_t11(P["sock_h"])
    json.dump({"commands": cmds}, open(out, "w"), indent=0)
    print(f"stufe {stage}: {len(cmds)} befehle, {n} streben, {dropped} fuer tuer entfernt")
