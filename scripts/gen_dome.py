"""Erzeugt das SolidCraft-Befehlsskript fuer designs/dome.sc (Stufe 1-4 = Plan-Schritte 2-5).
Aufruf: python gen_dome.py <stufe> <out.json>. Masse in mm; alle Annahmen stehen in P."""
import json, math, sys
from geo import build

P = dict(  # Parameter-Tabelle (siehe docs/packages/dome-build.md)
    dome_base_d=7000, freq=3, sock_h=400, sock_w=300, strut_r=20,
    door_w=900, door_h=2000, door_az=-54,
    t5_d=2600, t5_h=900, t6_d=1400, t6_h=700, t7_d=700, t7_h=1000, t7_stand=400,
    bed_n=10, bed_len=1500, bed_w=700, bed_h=900, bed_r=2500,
    tub_len=1500, tub_w=600, tub_h=400,
    pipe_d=200, cab_x=500, cab_y=300, cab_z=800, wall=80)

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
    zcut = -0.19
    keep = {k for k, p in pts.items() if p[2] >= zcut}
    zb = -0.18
    # Radius so, dass der Basisring-Umkreis = dome_base_d/2
    R = (P["dome_base_d"]/2) / math.sqrt(1 - zb*zb)
    cz = sock_z - zb*R
    # Basisring auf gleiche Hoehe setzen; Drehung: Basisknoten bei Azimut 0
    base = [k for k in keep if pts[k][2] < 0]
    a0 = math.atan2(pts[base[0]][1], pts[base[0]][0])
    def V(k):
        x, y, z = pts[k]
        if z < 0: z = zb
        x, y = rot(x, y, -a0)
        return (x*R, y*R, z*R + cz)
    # Tuerflaeche: Streben, die den Tuerquader kreuzen, entfallen
    da = math.radians(P["door_az"]); rd = R*math.sqrt(1-zb*zb)*math.cos(math.radians(18))
    def in_door(p):
        x, y = rot(p[0], p[1], -da)   # x = radial, y = tangential
        return abs(x - rd) < 150 and abs(y) < P["door_w"]/2 + 40 and sock_z - 20 < p[2] < sock_z + P["door_h"] + 40
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
    ox, oy = rd*ca, rd*sa
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
        add("solid.cylinder", radius=20, height=stand, base=[round(lx, 1), round(ly, 1), z0], operation="join", targets=[name], name=f"{name}_Fuss{i+1}")

def t5_t7(fz):
    tank("T5_Zentraltank", 0, 350, fz, "t5_d", "t5_h", "wall")
    tank("T6_Mitteltank", 650, -850, fz, "t6_d", "t6_h", "wall")
    pos = [(-2000, 150), (-1350, -350), (1250, -1900), (1900, 900), (1550, 1450), (-300, -1950)]
    for i, (x, y) in enumerate(pos, 1):
        tank(f"T7_Fasstank_{i}", x, y, fz, "t7_d", "t7_h", "wall", stand=P["t7_stand"])

def t8_t9(fz):
    n = P["bed_n"]
    for i in range(n):
        az = 36*i + 18   # Zehneck-Seitenmitten
        if abs(((az - P["door_az"]) + 180) % 360 - 180) < 1: pass
        cx, cy = pol(P["bed_r"], az)
        nm = f"T8_Anbaubett_{i+1:02d}"
        rect_body(nm, round(cx, 1), round(cy, 1), fz+P["bed_h"]-60, az+90, P["bed_len"], P["bed_w"], 60)
        a = math.radians(az+90)
        for sx in (-1, 1):
            for sy in (-1, 1):
                lx, ly = rot(sx*(P["bed_len"]/2-60), sy*(P["bed_w"]/2-60), a)
                add("solid.cylinder", radius=20, height=P["bed_h"]-60, base=[round(cx+lx, 1), round(cy+ly, 1), fz], operation="join", targets=[nm], name=f"{nm}_Bein{(sx+1)//2*2+(sy+1)//2+1}")
        for r in range(2):
            for c in range(4):
                lx, ly = rot((c-1.5)*330, (r-0.5)*300, a)
                add("solid.cylinder", diameter=50, height=70, base=[round(cx+lx, 1), round(cy+ly, 1), fz+P["bed_h"]-65], operation="cut", targets=[nm], name=f"{nm}_Loch{r*4+c+1}")
    # T9: zwei Substratwannen unter Bett 7 (Azimut 270? -> hier Azimut 234 und 342)
    for k, az in enumerate((234, 342), 1):
        cx, cy = pol(P["bed_r"], az)
        rect_body(f"T9_Substratbeet_{k}", round(cx, 1), round(cy, 1), fz, az+90, P["tub_len"], P["tub_w"], P["tub_h"])

def t10_t11(fz):
    A = (2900, 2900, fz+1500); B = (919, 1269, fz+950)
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
