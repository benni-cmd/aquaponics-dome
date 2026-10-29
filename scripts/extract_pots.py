"""Topfpositionen je Aussenbeet aus dem OASIS-OBJ (Gruppen 'potplant') in Beet-Koordinaten -> data/pots.json.
Aufruf: python -I scripts/extract_pots.py [pfad.obj]   Ergebnis je Beet (Index wie layout.json ibc_beds): Liste [u, v, z] in mm, u = laengs (yaw), v = quer, z = Hoehe ueber Boden.
Gleiche Konvention wie extract_layout.py (Zuordnung zum naechsten Beetmittelpunkt)."""
import json, math, os, sys
sys.argv = sys.argv[:1] + sys.argv[1:2]
HERE = os.path.dirname(os.path.abspath(__file__))
src = open(os.path.join(HERE, 'extract_layout.py'), encoding='utf-8').read()
head = src[:src.index('# Toepfe je Beet zuordnen')]   # bis inkl. Beetermittlung (ibc), ohne Schreiben
ns = {'__file__': os.path.join(HERE, 'extract_layout.py'), 'sys': sys}
exec(compile(head.replace("OUT_JSON =", "OUT_JSON_ =").replace("OUT_MD =", "OUT_MD_ ="), 'extract_layout', 'exec'), ns)
ibc, sel, pts, mean = ns['ibc'], ns['sel'], ns['pts'], ns['mean']
pots = [tuple(mean([p[i] for p in pts(g)]) for i in range(3)) for g in sel(r'potplant')]
per = {k: [] for k in range(len(ibc))}
for x, y, z in pots:
    k = min(range(len(ibc)), key=lambda i: math.hypot(x - ibc[i]['cx'], y - ibc[i]['cy'])); b = ibc[k]
    c, s = math.cos(math.radians(b['yaw'])), math.sin(math.radians(b['yaw']))
    per[k].append([round((x - b['cx']) * c + (y - b['cy']) * s, 1), round(-(x - b['cx']) * s + (y - b['cy']) * c, 1), round(z, 1)])
json.dump({'unit': 'mm', 'frame': 'Beetmitte, u laengs (yaw), v quer, z ueber Boden', 'total': len(pots), 'per_bed': [per[k] for k in range(len(ibc))]},
          open(os.path.join(HERE, '..', 'data', 'pots.json'), 'w'), separators=(',', ':'))
print('Toepfe', len(pots), 'je Beet', [len(per[k]) for k in range(len(ibc))])
