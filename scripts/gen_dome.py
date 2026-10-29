"""Erzeugt das SolidCraft-Befehlsskript fuer designs/dome.sc (Stufe 1-4 = Plan-Schritte 2-5).
Aufruf: python gen_dome.py <stufe> <out.json>. Masse in mm; alle Annahmen stehen in P."""
import json, math, sys
from geo import build

P = dict(  # Parameter-Tabelle, von Ben bestaetigt 29.10.2026: Basis 12 m, Hoehe 6 m; Rest per Pixelvergleich mit ref-4 (Basis = 12 m)
    dome_base_d=12000, dome_h=6000, freq=2, sock_h=400, sock_w=250, strut_r=45,
    door_w=1000, door_h=2000, door_az=-54, door_off=1100,
    t5_d=4210, t5_h=1200, t6_d=2200, t6_h=900, t7_d=1100, t7_h=1200, t7_stand=500,
    bed_n=10, bed_len=2300, bed_w=900, bed_h=950, bed_r=4500,
    tub_len=2200, tub_w=720, tub_h=550,
    pipe_d=300, cab_x=800, cab_y=500, cab_z=1200, wall=160)

cmds = []
names = []
def add(c, **p):
    cmds.append({"command": c, "params": p})
    if p.get("body_name"): names.append(p["body_name"])

COLORS = [  # (Namenspraefix, Farbe, Deckkraft) - Schicht 1
    ("T1_", "#b9c0c8", 1), ("T3_", "#cfcfca", 1), ("T4_", "#1c1c1c", 1), ("T5_Wasser", "#3c8ed0", 0.85),
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

AZ0 = 111   # Azimut-Abbildung OBJ -> Modell (Tuerseite OBJ ~195 Grad -> Modell -54 Grad)

def t5_t7(fz):
    """T5 Zentralpool in der Mitte (OBJ: Wasser D 3,89 m); T7 = 4 Tanks auf Plattformen (OBJ), T6 Mitteltank entfaellt (nicht im OBJ)."""
    tank("T5_Zentraltank", 0, 0, fz, "t5_d", "t5_h", "wall")
    add("solid.cylinder", diameter="t5_d - 2*wall", height=20, base=[0, 0, fz + P["t5_h"] - 250], operation="new", name="T5_Wasser", body_name="T5_Wasser")
    specs = [(147, 670, 1080, 750), (237, 670, 1080, 750), (131, 930, 1440, 1010), (252, 930, 1440, 1010)]   # OBJ-Azimut, D, H, Beinhoehe
    for i, (oaz, d, h, leg) in enumerate(specs, 1):
        az = oaz + AZ0; x, y = pol(3350, az); x, y = round(x, 1), round(y, 1); nm = f"T7_Tank_{i}"
        add("solid.cylinder", diameter=d, height=h, base=[x, y, fz + leg + 70], operation="new", name=nm, body_name=nm)
        add("solid.cylinder", diameter=d - 2*60, height=h, base=[x, y, fz + leg + 70 + 60], operation="cut", targets=[nm], name=nm + "_Hohlraum")
        rect_body(f"T7_Plattform_{i}", x, y, fz + leg, az, 710, 710, 70)
        for sx in (-1, 1):
            for sy in (-1, 1):
                lx, ly = rot(sx*300, sy*300, math.radians(az))
                add("solid.cylinder", radius=20, height=leg, base=[round(x+lx, 1), round(y+ly, 1), fz], operation="join", targets=[f"T7_Plattform_{i}"], name=f"{nm}_Bein{(sx+1)+(sy+1)//2+1}")
        mx, my = pol(3350 - 700, az)   # Pump-/Filtermodul daneben
        rect_body(f"T7_Pumpe_{i}", round(mx, 1), round(my, 1), fz, az, 460, 350, 200)
        ux, uy = -math.cos(math.radians(az)), -math.sin(math.radians(az))   # Schlauch zum Pool
        sx_, sy_, sz_ = x + ux*d/2, y + uy*d/2, fz + leg + 200
        ex, ey, ez = ux*(3350 - d/2 - P["t5_d"]/2), uy*(3350 - d/2 - P["t5_d"]/2), fz + P["t5_h"] + 60
        dd = [ex - (sx_ - x) - 0, ey - (sy_ - y) - 0, ez - sz_]; L = math.sqrt(sum(q*q for q in dd))
        add("solid.cylinder", radius=25, height=round(L, 1), base=[round(sx_, 1), round(sy_, 1), sz_], axis=[round(q/L, 6) for q in dd], operation="new", name=f"T10_Schlauch_{i}", body_name=f"T10_Schlauch_{i}")

plants = [0]
def plant(x, y, z, r=90):
    plants[0] += 1
    add("solid.sphere", radius=r, center=[x, y, z], operation="new", name=f"T12_Salat_{plants[0]:03d}", body_name=f"T12_Salat_{plants[0]:03d}")

# T9: 14 halbe IBC-Wannen (OBJ): (OBJ-Azimut, Radius, Laenge)
T9_OUT = [(az, 5000, 3000) for az in (355, 319, 247, 31, 140, 67, 283, 103)]
T9_IN = [(az, 3300, ln) for az, ln in zip((318, 103, 283, 67, 30, 354), (1600, 1200, 2000, 1600, 1200, 2000))]

def t9(fz):
    for k, (oaz, r, ln) in enumerate(T9_OUT + T9_IN, 1):
        az = oaz + AZ0; cx, cy = pol(r, az); cx, cy = round(cx, 1), round(cy, 1)
        rect_body(f"T9_Substratbeet_{k:02d}", cx, cy, fz, az + 90, ln, 700, 640)
        ta = math.radians(az + 90); n = int(ln // 400)
        for r_ in range(2):
            for c_ in range(n):
                lx, ly = rot((c_ - (n - 1)/2)*400, (r_ - 0.5)*300, ta)
                plant(round(cx + lx, 1), round(cy + ly, 1), fz + 640 + 112, 110)

def t10_t11(fz):
    A = (-6577, 2394, 4400); B = (-1488, 1488, fz+1400)
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
    if stage >= 3: t9(P["sock_h"])
    if stage >= 4: t10_t11(P["sock_h"])
    colors()
    json.dump({"commands": cmds}, open(out, "w"), indent=0)
    print(f"stufe {stage}: {len(cmds)} befehle, {n} streben, {dropped} fuer tuer entfernt")
