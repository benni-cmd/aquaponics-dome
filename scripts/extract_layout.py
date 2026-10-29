"""Extrahiert aus dem OASIS-OBJ ein Layout in unserem Koordinatensystem -> data/layout.json und docs/layout.md.
Aufruf: python -I scripts/extract_layout.py [pfad.obj]
Koordinaten: Meter -> Millimeter. Ursprung = Kuppelmitte am Boden, X = SketchUp x, Y = -SketchUp z, Z = SketchUp y - 1,0
(Boden bei SketchUp y = 1,0). Azimut = atan2(Y, X) in Grad, gegen den Uhrzeigersinn von oben. yaw = Richtung der Laengsachse."""
import json, math, re, sys, collections, os
F = sys.argv[1] if len(sys.argv) > 1 else r'C:\Users\benkn\Downloads\Project_Oasis_Layout.obj'
HERE = os.path.dirname(os.path.abspath(__file__))
OUT_JSON = os.path.join(HERE, '..', 'data', 'layout.json')
OUT_MD = os.path.join(HERE, '..', 'docs', 'layout.md')
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

# Kuppelmitte aus den Strebengruppen
struts_g = [g for g in groups if 'Acidome' in g['name']]
xs = [verts[i][0] for g in struts_g for i in g['v']]; zs = [verts[i][2] for g in struts_g for i in g['v']]
CX, CZ = (min(xs) + max(xs)) / 2, (min(zs) + max(zs)) / 2
FLOOR = 1.0

def conv(v): return ((v[0] - CX) * 1000, -(v[2] - CZ) * 1000, (v[1] - FLOOR) * 1000)
def pts(g): return [conv(verts[i]) for i in g['v']]
def mean(a): return sum(a) / len(a)

def obb(g):
    """Orientierte Box in der Horizontalen (Hauptachse per Kovarianz), Hoehe in Z."""
    P = pts(g); mx, my = mean([p[0] for p in P]), mean([p[1] for p in P])
    sxx = mean([(p[0] - mx) ** 2 for p in P]); syy = mean([(p[1] - my) ** 2 for p in P]); sxy = mean([(p[0] - mx) * (p[1] - my) for p in P])
    th = 0.5 * math.atan2(2 * sxy, sxx - syy)
    c, s = math.cos(th), math.sin(th)
    u = [(p[0] - mx) * c + (p[1] - my) * s for p in P]; w = [-(p[0] - mx) * s + (p[1] - my) * c for p in P]
    z = [p[2] for p in P]
    cu, cw = (min(u) + max(u)) / 2, (min(w) + max(w)) / 2
    cx, cy = mx + cu * c - cw * s, my + cu * s + cw * c
    return dict(cx=round(cx), cy=round(cy), z0=round(min(z)), z1=round(max(z)), length=round(max(u) - min(u)),
                width=round(max(w) - min(w)), height=round(max(z) - min(z)), yaw=round(math.degrees(th) % 180, 1),
                r=round(math.hypot(cx, cy)), az=round(math.degrees(math.atan2(cy, cx)) % 360, 1))

def sel(pat): return [g for g in groups if re.search(pat, g['name'])]

L = {'frame': 'Ursprung Kuppelmitte am Boden, mm, X=SketchUp x, Y=-SketchUp z, Z=SketchUp y - 1000; az=atan2(Y,X)',
     'source': os.path.basename(F), 'dome_center_sketchup_m': [round(CX, 3), round(CZ, 3)]}

# Boden, Pool, zweites Wasserbecken
for g in groups:
    b = obb(g)
    if b['height'] < 10 and 3800 < b['length'] < 4000: L['pool'] = dict(d=b['length'], water_z=b['z0'], cx=b['cx'], cy=b['cy'])
    if b['height'] < 10 and 1650 < b['length'] < 1800: L['pool2'] = dict(d=b['length'], water_z=b['z0'], cx=b['cx'], cy=b['cy'], r=b['r'], az=b['az'])
    if b['height'] < 10 and b['length'] > 11000: L['floor'] = dict(size=[b['length'], b['width']], z=b['z0'])

# IBC-Beete
ibc = []
for g in sel(r'IBC_Open_Top'):
    b = obb(g); ibc.append(b)
ibc.sort(key=lambda b: (-b['r'] // 1000, b['az']))
L['ibc_beds'] = ibc

# Toepfe je Beet zuordnen (naechster IBC-Mittelpunkt)
pots = []
for g in sel(r'potplant'):
    P = pts(g); pots.append((mean([p[0] for p in P]), mean([p[1] for p in P]), mean([p[2] for p in P])))
per = collections.defaultdict(list)
for x, y, z in pots:
    k = min(range(len(ibc)), key=lambda i: math.hypot(x - ibc[i]['cx'], y - ibc[i]['cy']))
    per[k].append((x, y, z))
for k, lst in per.items():
    b = ibc[k]; c, s = math.cos(math.radians(b['yaw'])), math.sin(math.radians(b['yaw']))
    uu = sorted({round(((x - b['cx']) * c + (y - b['cy']) * s) / 10) * 10 for x, y, z in lst})
    ww = sorted({round((-(x - b['cx']) * s + (y - b['cy']) * c) / 10) * 10 for x, y, z in lst})
    zz = [z for _, _, z in lst]
    b['plants'] = dict(n=len(lst), z_min=round(min(zz)), z_max=round(max(zz)), distinct_along=len(uu), distinct_across=len(ww))
L['pots'] = dict(total=len(pots), size_mm=[50, 64, 63], per_bed=[len(per[k]) for k in range(len(ibc))])

# Tanks (Wand-Meshes je Tank), Plattform, Beine, Module, Fittings
tanks = {}
for g in groups:
    m = re.search(r'G_1000_plastic_tank(\d)', g['name'])
    if m: tanks.setdefault(int(m.group(1)), []).append(g)
T = []
for tid, gs in sorted(tanks.items()):
    body = [g for g in gs if re.match(r'Mesh\d+ Tank_', g['name'])]
    bb = [obb(g) for g in body]
    big = max(bb, key=lambda b: b['length'] * b['height'])
    base = [g for g in groups if re.search(rf'Base_of_tank{tid}\b', g['name'])]
    parts = [obb(g) for g in base]
    plat = [p for p in parts if p['height'] < 130 and p['length'] > 600]
    legs = [p for p in parts if p['length'] < 60 and p['width'] < 60 and p['height'] > 600]
    mods = [p for p in parts if 300 < p['length'] < 700 and 100 < p['height'] < 500 and p not in plat]
    fit = [obb(g) for g in gs if 'Bulkhead' in g['name'] or 'Slip' in g['name']]
    T.append(dict(id=tid, d=big['length'], h=big['height'], z0=big['z0'], cx=big['cx'], cy=big['cy'], r=big['r'], az=big['az'],
                  platform=plat[:1], legs=dict(n=len(legs), h=(legs[0]['height'] if legs else None)),
                  modules=[dict(cx=m['cx'], cy=m['cy'], z0=m['z0'], l=m['length'], w=m['width'], h=m['height'], yaw=m['yaw']) for m in mods[:8]],
                  fittings=[dict(cx=f['cx'], cy=f['cy'], z=f['z0'], size=f['length']) for f in fit[:6]], parts_total=len(parts)))
L['tanks'] = T

# erhoehte Hydroponik-Tische
tabs = [obb(g) for g in sel(r'Diferencia')]
L['hydro_tables'] = tabs
L['hydro_other'] = [obb(g) for g in sel(r'Grupo_|Hidrtoponia')][:6]

# Streben: Endpunkte, Laengen, Knoten
ends = []
slen = []
for g in struts_g:
    P = pts(g); c0 = (mean([p[0] for p in P]), mean([p[1] for p in P]), mean([p[2] for p in P]))
    A = max(P, key=lambda p: sum((p[i] - c0[i]) ** 2 for i in range(3)))
    B = max(P, key=lambda p: sum((p[i] - A[i]) ** 2 for i in range(3)))
    ends.append((A, B)); slen.append(math.dist(A, B))
nodes = []
for A, B in ends:
    for p in (A, B):
        for n in nodes:
            if math.dist(n['p'], p) < 250: n['m'].append(p); break
        else: nodes.append({'p': p, 'm': [p]})
nd = [dict(x=round(mean([q[0] for q in n['m']])), y=round(mean([q[1] for q in n['m']])), z=round(mean([q[2] for q in n['m']])), valence=len(n['m'])) for n in nodes]
L['dome'] = dict(struts=len(ends), strut_len_mm=sorted(round(x) for x in slen), nodes=len(nd), node_valence=dict(collections.Counter(n['valence'] for n in nd)),
                 apex_z=round(max(n['z'] for n in nd)), base_z=round(min(n['z'] for n in nd)), nodes_list=nd)

os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
json.dump(L, open(OUT_JSON, 'w'), indent=1)

# Markdown (Zahlen, lesbar)
o = []
o.append('# Layout aus dem OASIS-OBJ (erzeugt von `scripts/extract_layout.py`, nicht von Hand aendern)\n')
o.append(f"Koordinaten: {L['frame']}. Quelle `{L['source']}`. Rohdaten: `data/layout.json`.\n")
if 'pool' in L: o.append(f"- Pool: Durchmesser {L['pool']['d']} mm, Wasserspiegel Z {L['pool']['water_z']}, Mitte ({L['pool']['cx']}, {L['pool']['cy']}).")
if 'pool2' in L: o.append(f"- Zweites Becken: Durchmesser {L['pool2']['d']} mm, Wasserspiegel Z {L['pool2']['water_z']}, r {L['pool2']['r']}, az {L['pool2']['az']}.")
d = L['dome']
o.append(f"- Kuppel: {d['struts']} Streben, Laengen {sorted(set(d['strut_len_mm']))[:3]}...{sorted(set(d['strut_len_mm']))[-3:]} mm, {d['nodes']} Knoten, Wertigkeit {d['node_valence']}, Scheitel Z {d['apex_z']}, Basis Z {d['base_z']}.\n")
o.append('## IBC-Beete (Substratbeete), Maße in mm\n\n| # | r | az | Mitte x,y | Laenge | Breite | Hoehe | Z unten | yaw | Pflanzen |\n|---|---|---|---|---|---|---|---|---|---|')
for i, b in enumerate(ibc, 1):
    pl = b.get('plants', {}).get('n', 0)
    o.append(f"| {i} | {b['r']} | {b['az']} | {b['cx']},{b['cy']} | {b['length']} | {b['width']} | {b['height']} | {b['z0']} | {b['yaw']} | {pl} |")
o.append(f"\nPflanzen gesamt {L['pots']['total']} (je Topf ca. 50 x 64 x 63 mm); je Beet: {L['pots']['per_bed']}.\n")
o.append('## Tanks (Vortexfilter / Biofilter), Maße in mm\n\n| # | Durchm. | Hoehe | Z unten | r | az | Plattform | Beine | Module | Fittings |\n|---|---|---|---|---|---|---|---|---|---|')
for t in T:
    pl = t['platform'][0] if t['platform'] else None
    o.append(f"| {t['id']} | {t['d']} | {t['h']} | {t['z0']} | {t['r']} | {t['az']} | {('%dx%dx%d Z%d' % (pl['length'], pl['width'], pl['height'], pl['z0'])) if pl else '-'} | {t['legs']['n']}x h{t['legs']['h']} | {len(t['modules'])} | {len(t['fittings'])} |")
o.append('\n## Erhoehte Hydroponik-Tische, Maße in mm\n\n| r | az | Laenge | Breite | Dicke | Z unten | yaw |\n|---|---|---|---|---|---|---|')
for b in tabs:
    o.append(f"| {b['r']} | {b['az']} | {b['length']} | {b['width']} | {b['height']} | {b['z0']} | {b['yaw']} |")
open(OUT_MD, 'w', encoding='utf-8').write('\n'.join(o) + '\n')
print('Mitte (m):', round(CX, 2), round(CZ, 2), '| Streben', d['struts'], 'Knoten', d['nodes'], d['node_valence'], 'apex', d['apex_z'], 'base', d['base_z'])
print('IBC', len(ibc), 'Toepfe', len(pots), 'Tanks', len(T), 'Tische', len(tabs))
