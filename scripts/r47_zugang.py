"""R47b: Inventar unzugaenglicher Rohrabschnitte (Z unter Bodenniveau 400 absolut) aus data/leitungstrassen.json.
Nur lesen. Aufruf: python -X utf8 scripts/r47_zugang.py
"""
import json, math, re
from collections import defaultdict

tr = json.load(open('data/leitungstrassen.json', encoding='utf-8'))['trassen']
netz = {k['id']: k for k in json.load(open('data/leitungsnetz.json', encoding='utf-8'))['kanten']}
WAND = {32: 1.6, 40: 1.9, 50: 2.4, 63: 3.0, 75: 3.6, 110: 5.3}
agg = defaultdict(lambda: [0.0, 0.0, set()])
gesamt = unter = 0.0
bandsum = defaultdict(float)
for t in tr:
    p = t['pfad']
    base = re.match(r'(K\d+)', t['id'])
    base = base.group(1) if base else t['id']
    for a, b in zip(p, p[1:]):
        L = math.dist(a, b) / 1000
        zm = (a[2] + b[2]) / 2
        gesamt += L
        bandsum[t.get('band')] += L
        agg[base][0] += L
        agg[base][2].add(t['dn'])
        if zm < 400:
            unter += L
            agg[base][1] += L
print(f'Gesamt {gesamt:.1f} m, davon unter Boden (Z<400 abs) {unter:.1f} m')
print('Band-Summen:', {k: round(v, 1) for k, v in bandsum.items()})
print('Kante  gesamt  unter  dn   Q l/min  v m/s (Di aus SDR21)')
for k, (g, u, dn) in sorted(agg.items(), key=lambda x: -x[1][1]):
    if u <= 0:
        continue
    e = netz.get(k, {})
    d = max(dn)
    q = e.get('soll_l_min')
    di = d - 2 * WAND.get(d, 0)
    v = (q / 60000) / (math.pi / 4 * (di / 1000) ** 2) if q else None
    print(f'{k:5s} {g:6.1f} {u:6.1f}  d{sorted(dn)}  {q}  {v and round(v,2)}  {e.get("von")}->{e.get("nach")}')
