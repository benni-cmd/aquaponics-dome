"""Maengel-Inventur N-REWORK (Pruefer): nur lesen. Eingabe: viewer/instances.json (Runde 70), data/bom_koerper.json, data/leitungsnetz.json, data/leitungstrassen.json.
Aufruf: python -I -X utf8 inventur.py <repo-root> <out.json>"""
import json, math, sys, collections, os

ROOT, OUT = sys.argv[1], sys.argv[2]
inst = json.load(open(os.path.join(ROOT, 'viewer', 'instances.json'), encoding='utf-8'))
bomk = json.load(open(os.path.join(ROOT, 'data', 'bom_koerper.json'), encoding='utf-8'))['komponenten']
net = json.load(open(os.path.join(ROOT, 'data', 'leitungsnetz.json'), encoding='utf-8'))
tr = json.load(open(os.path.join(ROOT, 'data', 'leitungstrassen.json'), encoding='utf-8'))

def bbox_union(d):
    b = bomk.get(d)
    if not b or not b['bodies']:
        return None
    lo = [min(x['bbox_min'][i] for x in b['bodies']) for i in range(3)]
    hi = [max(x['bbox_max'][i] for x in b['bodies']) for i in range(3)]
    return lo, hi

def apply(m, p):
    return [m[0]*p[0]+m[1]*p[1]+m[2]*p[2]+m[3], m[4]*p[0]+m[5]*p[1]+m[6]*p[2]+m[7], m[8]*p[0]+m[9]*p[1]+m[10]*p[2]+m[11]]

def inverse(m, q):  # Rotation orthonormal angenommen
    d = [q[0]-m[3], q[1]-m[7], q[2]-m[11]]
    return [m[0]*d[0]+m[4]*d[1]+m[8]*d[2], m[1]*d[0]+m[5]*d[1]+m[9]*d[2], m[2]*d[0]+m[6]*d[1]+m[10]*d[2]]

def box_dist(local, lo, hi):
    dx = max(lo[0]-local[0], 0, local[0]-hi[0]); dy = max(lo[1]-local[1], 0, local[1]-hi[1]); dz = max(lo[2]-local[2], 0, local[2]-hi[2])
    return math.sqrt(dx*dx+dy*dy+dz*dz)

SKIP = ('netztopf', 'salatkopf', 'huelle_', 'strebe_', 'knoten_', 'erdflaeche', 'mensch_', 'fundamentring', 'fundamentanker', 'luft_scheibe')
objs = []
for a in inst['instances']:
    d = a['d']
    if d.startswith(('netztopf', 'salatkopf')):
        continue
    bb = bbox_union(d)
    if not bb:
        continue
    o = {'d': d, 'n': a['n'], 'm': a['m'], 'lo': bb[0], 'hi': bb[1], 'lt': d.startswith('lt_')}
    o['pos'] = apply(a['m'], [(bb[0][i]+bb[1][i])/2 for i in range(3)])
    o['solid'] = (not o['lt']) and not d.startswith(SKIP)
    objs.append(o)

pipes = []
for o in objs:
    if o['d'].startswith('lt_rohr_'):
        lo, hi = o['lo'], o['hi']
        o['A'] = apply(o['m'], [0, 0, lo[2]]); o['B'] = apply(o['m'], [0, 0, hi[2]])
        o['len'] = hi[2]-lo[2]; o['r'] = (hi[0]-lo[0])/2
        pipes.append(o)
fit = [o for o in objs if o['lt'] and not o['d'].startswith('lt_rohr_')]
solids = [o for o in objs if o['solid']]

def dist_to_obj(p, o, exclude=None):
    """Abstand eines Weltpunkts zum Objekt (Rohr: Achse minus Radius; sonst Kasten)."""
    if o.get('A') is not None:
        a, b = o['A'], o['B']
        ab = [b[i]-a[i] for i in range(3)]; L2 = sum(x*x for x in ab) or 1
        t = max(0, min(1, sum((p[i]-a[i])*ab[i] for i in range(3))/L2))
        q = [a[i]+t*ab[i] for i in range(3)]
        return max(0, math.dist(p, q)-o['r'])
    return box_dist(inverse(o['m'], p), o['lo'], o['hi'])

TOL = 25.0
res = {'pipes': len(pipes), 'fittings': len(fit)}
# 1. Rohrenden
frei = []; an_bauteil = collections.Counter(); an_lt = 0
for pp in pipes:
    for end, P in (('A', pp['A']), ('B', pp['B'])):
        nb = None
        for o in fit + pipes:
            if o is pp:
                continue
            if dist_to_obj(P, o) <= TOL:
                nb = 'lt'; break
        if nb:
            an_lt += 1; continue
        hit = None
        for s in solids:
            if dist_to_obj(P, s) <= 40:
                hit = s['n']; break
        if hit:
            an_bauteil[hit] += 1
        else:
            frei.append({'rohr': pp['n'], 'd': pp['d'], 'ende': end, 'ort': [round(v) for v in P], 'laenge': round(pp['len'])})
res['rohrenden_gesamt'] = 2*len(pipes); res['an_lt_stueck'] = an_lt; res['an_bauteil'] = dict(an_bauteil); res['frei_ins_leere'] = frei
# 2. Formstuecke ohne genug Nachbarn
need = lambda d: 3 if d.startswith('lt_t_') else 2
isol = []
for f in fit:
    nbr = 0
    ctr = f['pos']
    for o in fit + pipes:
        if o is f: continue
        # Nachbar: irgendein Punkt der Box des Formstuecks (8 Ecken+Mitte) nah am anderen
        if o.get('A') is not None:
            near = min(dist_to_obj(c, o) for c in corners(f)) if False else None
        # einfacher: Abstand Mitte-zu-Mitte gegen Groesse
    # Platzhalter, unten ersetzt
res['formstuecke_isoliert'] = None
def corners(o):
    lo, hi = o['lo'], o['hi']
    return [apply(o['m'], [x, y, z]) for x in (lo[0], hi[0]) for y in (lo[1], hi[1]) for z in (lo[2], hi[2])]
def touching(f, o):
    return any(dist_to_obj(c, o) <= TOL for c in corners(f)) or (o.get('A') is None and any(box_dist(inverse(f['m'], c), f['lo'], f['hi']) <= TOL for c in corners(o)))
isol = []
for f in fit:
    nbr = [o for o in fit+pipes if o is not f and touching(f, o)]
    f['nbr'] = nbr
    kn = len(nbr)
    if kn < need(f['d']):
        isol.append({'teil': f['n'], 'd': f['d'], 'nachbarn': kn, 'soll': need(f['d']), 'ort': [round(v) for v in f['pos']]})
res['formstuecke_zu_wenig_nachbarn'] = isol
# 3. Bogenketten: Bogen - (Rohr <=300) - Bogen
def is_bend(o): return o['d'].startswith('lt_bogen')
adj = {id(o): [x for x in (o['nbr'] if 'nbr' in o else []) ] for o in fit}
for pp in pipes:
    pp['nbr'] = [o for o in fit+pipes if o is not pp and (dist_to_obj(pp['A'], o) <= TOL or dist_to_obj(pp['B'], o) <= TOL)]
seen = set(); ketten = []
def chain(start):
    stack = [(start, 1)]; comp = {id(start)}; best = 1
    n_b = {id(start)}
    q = [start]
    while q:
        cur = q.pop()
        for nb in cur['nbr']:
            if id(nb) in comp: continue
            if is_bend(nb) or (nb.get('A') is not None and nb['len'] <= 300) or nb['d'].startswith(('lt_kupplung', 'lt_reduz')):
                comp.add(id(nb)); q.append(nb)
    return comp
by_id = {id(o): o for o in fit+pipes}
for f in fit:
    if is_bend(f) and id(f) not in seen:
        comp = chain(f); seen |= comp
        bends = [by_id[i] for i in comp if is_bend(by_id[i])]
        if len(bends) >= 3:
            ketten.append({'boegen': len(bends), 'teile': len(comp), 'von': [round(v) for v in bends[0]['pos']], 'd': sorted(set(b['d'] for b in bends)), 'ort': [round(sum(b['pos'][i] for b in bends)/len(bends)) for i in range(3)]})
ketten.sort(key=lambda k: -k['boegen'])
res['bogenketten_ab3'] = ketten
res['boegen_gesamt'] = sum(1 for f in fit if is_bend(f))
# 4. Rohre durch massive Bauteile (Beet-Kasten exakt, Tank/Pool als Zylinder)
cyl = {}
def inside(o, p):
    loc = inverse(o['m'], p)
    d = o['d']
    if d.startswith(('tank_', 'pool_', 'zweitbecken', 'becken_dritt', 'puffer_')):
        r = (o['hi'][0]-o['lo'][0])/2; cx = (o['hi'][0]+o['lo'][0])/2; cy = (o['hi'][1]+o['lo'][1])/2
        return math.hypot(loc[0]-cx, loc[1]-cy) < r-30 and o['lo'][2]+30 < loc[2] < o['hi'][2]-30
    return all(o['lo'][i]+30 < loc[i] < o['hi'][i]-30 for i in range(3))
durch = collections.defaultdict(lambda: collections.Counter())
for pp in pipes:
    n = max(2, int(pp['len']//40))
    for k in range(1, n):
        t = k/n
        P = [pp['A'][i]+t*(pp['B'][i]-pp['A'][i]) for i in range(3)]
        for s in solids:
            if s['d'].startswith(('ibc_beet', 'tank_', 'pool_', 'zweitbecken', 'becken_dritt', 'puffer_', 'feinfilter', 'pumpe_', 'aktivkohle', 'schaltschrank', 'nft_tisch')) and inside(s, P):
                durch[pp['n']][s['n']] += 1
res['rohre_durch_bauteile'] = [{'rohr': k, 'bauteile': dict(v), 'd': next(p['d'] for p in pipes if p['n'] == k)} for k, v in durch.items()]
# 5. Halter an Leitungen
res['halter_leitung_instanzen'] = sum(1 for a in inst['instances'] if a['d'].startswith(('lt_schelle', 'lt_klemme')))
res['halter_sonstige_instanzen'] = {a: sum(1 for x in inst['instances'] if x['d'] == a) for a in set(x['d'] for x in inst['instances'] if x['d'].startswith('halter_'))}
# 6. Schwebende: Rohr, dessen Mittelpunkt >300 mm ueber Boden und kein Halter/Bauteil in 300 mm  (nur Zahl)
hoch = [pp for pp in pipes if min(pp['A'][2], pp['B'][2]) > 600]
res['rohre_hoeher_600'] = [{'rohr': p['n'], 'z': round(min(p['A'][2], p['B'][2])), 'ort': [round(v) for v in p['pos']]} for p in hoch]
# 7. Netz: Kanten ohne Trasse
tk = set(t.get('kante') for t in tr['trassen'] if t.get('kante'))
kan = {k['id']: k for k in net['kanten']}
no = []
for kid, k in kan.items():
    if kid in tk or any(str(t['id']).startswith(kid) for t in tr['trassen']):
        continue
    no.append({'kante': kid, 'von': k['von'], 'nach': k['nach'], 'medium': k['medium'], 'dn': k['dn']})
res['kanten_gesamt'] = len(kan); res['kanten_ohne_trasse'] = no
# Knoten-Bauteile ohne Instanz
have = set(o['d'] for o in objs)
nodes = []
for n_ in net['knoten']:
    bt = n_.get('bauteil'); mod = n_.get('modell')
    nodes.append({'id': n_['id'], 'bauteil': bt, 'typ': n_['typ'], 'instanz': (bt in have) if bt else False})
res['knoten_ohne_instanz'] = [n_ for n_ in nodes if not n_['instanz']]
# 8. Trassen: Abdeckung durch gebaute Stuecke (Stichproben entlang des Pfads)
def seg_samples(path, step=50):
    out = []
    for i in range(len(path)-1):
        a, b = path[i], path[i+1]; L = math.dist(a, b); n = max(1, int(L//step))
        for k in range(n+1):
            t = k/n; out.append([a[j]+t*(b[j]-a[j]) for j in range(3)])
    return out
cov = []
for t in tr['trassen']:
    s = seg_samples(t['pfad'])
    ok = sum(1 for p in s if any(dist_to_obj(p, o) <= 60 for o in fit+pipes))
    cov.append({'id': t['id'], 'kante': t.get('kante'), 'dn': t['dn'], 'proben': len(s), 'abgedeckt': ok, 'anteil': round(ok/len(s), 2), 'pfadlaenge': round(sum(math.dist(t['pfad'][i], t['pfad'][i+1]) for i in range(len(t['pfad'])-1)))})
res['trassen_abdeckung'] = cov
# 9. Rohre je Dn/Laenge Kurzstuecke
kurz = [p for p in pipes if p['len'] < 120]
res['rohre_unter_120mm'] = [{'rohr': p['n'], 'laenge': round(p['len'])} for p in kurz]
# 10. Tank-Anschluesse: je Stutzen Weltposition und naechstes lt-Stueck
ports = []
tank_ports = {
    'tank_klein': [('Zulauf', 'Zulaufrohr'), ('Auslauf', 'Auslaufrohr'), ('Schlammstutzen', 'Schlammstutzen'), ('Ablaufstutzen', 'Ablaufstutzen')],
    'tank_gross': [('Zulauf', 'Zulaufrohr'), ('Schlammstutzen', 'Schlammstutzen'), ('Ablaufstutzen', 'Ablaufstutzen')],
    'tank_gross_t3': [('Zulauf', 'Zulaufrohr'), ('Schlammstutzen', 'Schlammstutzen'), ('Ablaufstutzen', 'Ablaufstutzen')],
}
for o in objs:
    if o['d'] in tank_ports:
        for (nm, body) in tank_ports[o['d']]:
            bb = [b for b in bomk[o['d']]['bodies'] if b['name'] == body]
            if not bb: continue
            b = bb[0]
            # freies Ende: Ecke des Stutzenkastens, die am weitesten vom Tank-Mittelpunkt (lokal x,y=0) liegt
            cs = [[x, y, z] for x in (b['bbox_min'][0], b['bbox_max'][0]) for y in (b['bbox_min'][1], b['bbox_max'][1]) for z in (b['bbox_min'][2], b['bbox_max'][2])]
            far = max(cs, key=lambda c: math.hypot(c[0], c[1]))
            mid = [(b['bbox_min'][i]+b['bbox_max'][i])/2 for i in range(3)]
            # Austritt: Mitte des Stutzens an der aeusseren Kante
            ang = math.atan2(mid[1], mid[0]) if (abs(mid[0]) > 1 or abs(mid[1]) > 1) else None
            end_local = [mid[0], mid[1], mid[2]]
            if ang is not None:
                rmax = max(math.hypot(c[0], c[1]) for c in cs)
                end_local = [rmax*math.cos(ang), rmax*math.sin(ang), mid[2]]
            elif nm in ('Schlammstutzen', 'Ablaufstutzen'):
                end_local = [mid[0], mid[1], b['bbox_min'][2]]
            W = apply(o['m'], end_local)
            near = None; nd = 1e9
            for q in fit+pipes:
                dd = dist_to_obj(W, q)
                if dd < nd: nd, near = dd, q['n']
            ports.append({'tank': o['n'], 'anschluss': nm, 'ort': [round(v) for v in W], 'naechstes_lt': near, 'abstand_mm': round(nd)})
res['tank_anschluesse'] = ports
json.dump(res, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print({k: (len(v) if isinstance(v, (list, dict)) else v) for k, v in res.items()})
