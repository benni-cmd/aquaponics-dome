import re, math, collections
F = r'C:\Users\benkn\Downloads\Project_Oasis_Layout.obj'
verts = []; groups = []; cur = None
for line in open(F, encoding='utf-8', errors='replace'):
    if line.startswith('v '):
        p = line.split(); verts.append((float(p[1]), float(p[2]), float(p[3])))
        if cur is not None: cur['v'].add(len(verts)-1)
    elif line.startswith('g '):
        cur = {'name': line[2:].strip(), 'v': set()}; groups.append(cur)
    elif line.startswith('f ') and cur is not None:
        for t in line.split()[1:]:
            i = int(t.split('/')[0]); cur['v'].add(i-1 if i > 0 else len(verts)+i)

def ctr(g):
    vs = [verts[i] for i in g['v']]
    return tuple(sum(v[k] for v in vs)/len(vs) for k in range(3)), [(min(v[k] for v in vs), max(v[k] for v in vs)) for k in range(3)]

dome = [ctr(g) for g in groups if g['name'].startswith('Mesh') and 'Acidome' in g['name'] or g['name'].startswith('Acidome')]
bx = [b for _, b in dome]
cx = (min(b[0][0] for b in bx) + max(b[0][1] for b in bx))/2
cz = (min(b[2][0] for b in bx) + max(b[2][1] for b in bx))/2
print('dome center x,z', round(cx, 2), round(cz, 2), 'ymax', round(max(b[1][1] for b in bx), 2), 'xspan', round(max(b[0][1] for b in bx)-min(b[0][0] for b in bx), 2))

def sel(pat):
    return [g for g in groups if re.search(pat, g['name'])]
def report(label, gs, maxprint=0):
    cs = [ctr(g)[0] for g in gs]
    r = [math.hypot(c[0]-cx, c[2]-cz) for c in cs]
    a = [(math.degrees(math.atan2(c[2]-cz, c[0]-cx)) % 360) for c in cs]
    ys = [c[1] for c in cs]
    print(f'{label}: n={len(gs)} r=[{min(r):.2f},{max(r):.2f}] y=[{min(ys):.2f},{max(ys):.2f}]')
    return cs, r, a, ys

pots, r, a, ys = report('potplant', sel(r'potplant'))
# Hoehen-Cluster
hc = collections.Counter(round(y, 1) for y in ys)
print('pot heights', sorted(hc.items()))
# Radius-Cluster
rc = collections.Counter(round(x, 0) for x in r)
print('pot radius (m, gerundet)', sorted(rc.items()))
ac = collections.Counter(int(x//30)*30 for x in a)
print('pot winkel (30-Grad-Klassen)', sorted(ac.items()))
for lab, pat in [('IBC', r'IBC_Open_Top'), ('tank', r'plastic_tank|^Tank_'), ('Base_of_tank', r'Base_of_tank'), ('Hidro Diferencia', r'Diferencia'),
                 ('Grupo cups', r'Grupo_'), ('3.89 discs', None)]:
    if pat is None: continue
    gs = sel(pat)
    if not gs: continue
    cs, rr, aa, yy = report(lab, gs)
    for c, r1, a1, g in list(zip(cs, rr, aa, gs))[:40]:
        bb = ctr(g)[1]
        print(f'   r={r1:5.2f} az={a1:5.0f} y={c[1]:.2f} dims=({bb[0][1]-bb[0][0]:.2f},{bb[1][1]-bb[1][0]:.2f},{bb[2][1]-bb[2][0]:.2f}) {g["name"][:40]}')
# freie Flaechen (Scheiben 3.89)
for g in groups:
    c, b = ctr(g)
    dx, dy, dz = b[0][1]-b[0][0], b[1][1]-b[1][0], b[2][1]-b[2][0]
    if dy < 0.01 and 3.5 < dx < 4.2:
        print('disc', round(math.hypot(c[0]-cx, c[2]-cz), 2), round(c[1], 2), round(dx, 2), g['name'][:50])
