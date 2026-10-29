"""Explorative Auswertung des OASIS-OBJ: lange schmale Koerper (Rohre/Rinnen), Topfreihen, Kuppelmitte.
Aufruf: python -I scripts/obj_explore.py [pfad.obj]  (Meter, SketchUp Y = oben)"""
import re, sys, math, collections
F = sys.argv[1] if len(sys.argv) > 1 else r'C:\Users\benkn\Downloads\Project_Oasis_Layout.obj'
verts, groups, cur = [], [], None
for line in open(F, encoding='utf-8', errors='replace'):
    if line.startswith('v '):
        p = line.split(); verts.append((float(p[1]), float(p[2]), float(p[3])))
        if cur is not None: cur['v'].add(len(verts) - 1)
    elif line.startswith('g '):
        cur = {'name': line[2:].strip(), 'v': set()}; groups.append(cur)
    elif line.startswith('f ') and cur is not None:
        for t in line.split()[1:]:
            i = int(t.split('/')[0]); cur['v'].add(i - 1 if i > 0 else len(verts) + i)
CX, CZ = 24.63, 63.34

def box(g):
    vs = [verts[i] for i in g['v']]
    return [(min(v[k] for v in vs), max(v[k] for v in vs)) for k in range(3)]

# 1) lange schmale Koerper
print('== lange schmale Koerper (max Kante > 1,0 m, kleinste < 0,25 m), nicht Struts/IBC/Tanks')
rows = []
for g in groups:
    if 'Acidome' in g['name'] or 'IBC' in g['name'] or 'potplant' in g['name']: continue
    b = box(g); d = sorted([b[k][1] - b[k][0] for k in range(3)])
    if d[2] > 1.0 and d[0] < 0.25:
        c = [(b[k][0] + b[k][1]) / 2 for k in range(3)]
        rows.append((round(d[2], 2), round(d[1], 2), round(d[0], 2), round(math.hypot(c[0] - CX, c[2] - CZ), 2),
                     round(math.degrees(math.atan2(c[2] - CZ, c[0] - CX)) % 360), round(c[1], 2), g['name'][:60]))
print(len(rows), 'Treffer')
agg = collections.Counter((r[0], r[1], r[2]) for r in rows)
for k, n in agg.most_common(25): print(n, 'x', k)
for r in rows[:15]: print(r)

# 2) Topfreihen: Cluster nach Hoehe und Radius
pots = [g for g in groups if 'potplant' in g['name']]
P = []
for g in pots:
    b = box(g); c = [(b[k][0] + b[k][1]) / 2 for k in range(3)]
    P.append((math.hypot(c[0] - CX, c[2] - CZ), math.degrees(math.atan2(c[2] - CZ, c[0] - CX)) % 360, c[1]))
print('== Toepfe', len(P))
byrow = collections.defaultdict(list)
for r, a, y in P: byrow[(round(r * 20) / 20, round(y * 50) / 50)].append(a)
print('Reihen-Cluster (r auf 5 cm, y auf 2 cm): ', len(byrow))
for k in sorted(byrow)[:60]:
    a = sorted(byrow[k]); print(k, 'n=', len(a), 'az', round(a[0]), '-', round(a[-1]))
