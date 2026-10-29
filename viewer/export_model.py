"""Exportiert designs/dome.sc fuer den 3D-Viewer: viewer/model.obj (+ .mtl-freie Geometrie je Koerper) und viewer/extras.json.

Warum zwei Teile: Die Exportgenauigkeit von SolidCraft richtet sich nach der Groesse jedes Koerpers. Kleine gekruemmte
Koerper (Salatkoepfe, Kugeln) wuerden Hunderte MB erzeugen (Test: 240 Kugeln = 1,25 GB). Sie werden deshalb NICHT
exportiert, sondern als Position/Radius in extras.json an den Viewer gegeben, der sie als einfache Kugeln zeichnet.
Aufruf: python viewer/export_model.py   (liest scripts/dome-script.json fuer Namen/Positionen, designs/dome.sc fuer die Geometrie)
"""
import json, os, re, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
CLI = r'C:\Program Files\SolidCraft\solidcraft-cli.exe'
SCRIPT = os.path.join(ROOT, 'scripts', 'dome-script.json')
DESIGN = os.path.join(ROOT, 'designs', 'dome.sc')
OUT = os.path.join(HERE, 'model.obj')
EXTRAS = os.path.join(HERE, 'extras.json')
SMALL = re.compile(r'(_Salat_|_Pflanze_|_Topf_)')   # kleine gekruemmte Koerper: als Extras zeichnen

cmds = json.load(open(SCRIPT, encoding='utf-8'))
cmds = cmds['commands'] if isinstance(cmds, dict) else cmds
bodies, extras, colors = [], [], {}
for c in cmds:
    p = c.get('params', {})
    if c['command'] == 'appearance.assign':
        for b in p.get('bodies', []):
            colors[b] = [p.get('color', '#b0b0b0'), p.get('opacity', 1)]
        continue
    n = p.get('body_name') or p.get('name')
    if not (c['command'].startswith('solid.') and n):
        continue
    if p.get('operation', 'new') != 'new':
        continue
    if SMALL.search(n):
        if c['command'] == 'solid.sphere':
            extras.append({'n': n, 'c': p.get('center'), 'r': p.get('radius')})
    else:
        bodies.append(n)

job = {'commands': [
    {'command': 'doc.open', 'params': {'path': DESIGN.replace('\\', '/'), 'read_only': True}},
    {'command': 'file.export', 'params': {'path': OUT.replace('\\', '/'), 'format': 'obj', 'quality': 'standard', 'bodies': bodies}},
]}
tmp = os.path.join(HERE, '.export-job.json')
json.dump(job, open(tmp, 'w'))
t = time.time()
r = subprocess.run([CLI, 'run', tmp, '--quiet'], capture_output=True, text=True)
os.remove(tmp)
json.dump({'plants': extras, 'colors': colors, 'built': time.strftime('%Y-%m-%d %H:%M:%S'), 'bodies': len(bodies)}, open(EXTRAS, 'w'))
size = os.path.getsize(OUT) / 1e6 if os.path.exists(OUT) else -1
print(f'export rc={r.returncode} {time.time()-t:.0f}s model.obj={size:.1f} MB bodies={len(bodies)} plants={len(extras)}')
sys.exit(r.returncode)
