"""Exportiert designs/dome.sc fuer den 3D-Viewer: je Komponentendefinition EINMAL viewer/defs/<datei>.obj plus viewer/instances.json (Instanz -> Definition + 3x4-Matrix) und viewer/extras.json.

Warum so: Ein Gesamt-OBJ expandiert jede Instanz voll (14 Tische + 4 Tanks + 14 Beete = 320 MB). Definitionen einmal + Matrizen (three.js InstancedMesh) halten den Viewer klein.
Kleinteile (Koerper mit Bounding-Box-Diagonale < MIN_DIAG mm: Schrauben, Kappen, Lochkanten) kommen nicht in die Definition-OBJ; sie treiben die Dreieckszahl (Tesselierung richtet sich nach der Koerpergroesse). Das Modell selbst (dome.sc) bleibt unveraendert.
Definitionen werden zwischengespeichert (viewer/defs/.cache.json: Aenderungszeit der .sc + MIN_DIAG).
Aufruf: python viewer/export_model.py   (liest scripts/dome-script.json fuer Einbau und Matrizen, designs/components/*.sc fuer die Geometrie)
"""
import json, math, os, re, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
CLI = r'C:\Program Files\SolidCraft\solidcraft-cli.exe'
SCRIPT = os.path.join(ROOT, 'scripts', 'dome-script.json')
DEFS = os.path.join(HERE, 'defs')
MIN_DIAG = 150   # mm
KEEP_ALL = ('netztopf', 'salatkopf')   # Pflanzenteile sind klein, aber als Instanzen billig: alle Koerper behalten
fw = lambda p: os.path.abspath(p).replace(chr(92), '/')

def find(o, key):
    if isinstance(o, dict):
        if key in o and isinstance(o[key], list): return o[key]
        for v in o.values():
            r = find(v, key)
            if r is not None: return r
    elif isinstance(o, list):
        for v in o:
            r = find(v, key)
            if r is not None: return r

cmds = json.load(open(SCRIPT, encoding='utf-8'))
cmds = cmds['commands'] if isinstance(cmds, dict) else cmds
colors, ins, copies, moves = {}, {}, {}, {}
for c in cmds:
    p = c.get('params', {})
    if c['command'] == 'appearance.assign':
        for b in p.get('bodies', []): colors[b] = [p.get('color', '#b0b0b0'), p.get('opacity', 1)]
    elif c['command'] == 'component.insert_design': ins[p['name']] = p['path']
    elif c['command'] == 'occurrence.copy': copies[p['component']] = copies.get(p['component'], 0) + 1
    elif c['command'] == 'occurrence.move': moves[p['occurrence']] = p['matrix']

os.makedirs(DEFS, exist_ok=True)
cache_p = os.path.join(DEFS, '.cache.json')
cache = json.load(open(cache_p)) if os.path.exists(cache_p) else {}
t0 = time.time(); defs = {}; exported = 0; tmp = os.path.join(DEFS, '_job.json')
for cls, path in ins.items():
    stem = os.path.splitext(os.path.basename(path))[0]
    if stem in defs: continue
    md = 0 if stem in KEEP_ALL else MIN_DIAG; key = f'{os.path.getmtime(path)}|{md}'; out = os.path.join(DEFS, stem + '.obj')
    if cache.get(stem) != key or not os.path.exists(out):
        json.dump({'commands': [{'command': 'doc.open', 'params': {'path': fw(path), 'read_only': True}}]}, open(tmp, 'w'))
        o = os.path.join(DEFS, '_ev.json')
        subprocess.run([CLI, 'eval', fw(path), '--json-out', o], capture_output=True)
        bodies = find(json.load(open(o, encoding='utf-8')), 'bodies') or []; os.remove(o)
        keep = [b['name'] for b in bodies if math.dist(b['bbox']['min'], b['bbox']['max']) >= md]
        json.dump({'commands': [{'command': 'doc.open', 'params': {'path': fw(path), 'read_only': True}},
                                {'command': 'file.export', 'params': {'path': fw(out + '.tmp'), 'format': 'obj', 'bodies': keep}}]}, open(tmp, 'w'))
        r = subprocess.run([CLI, 'run', tmp, '--quiet'], capture_output=True, text=True)
        if r.returncode or not os.path.exists(out + '.tmp'):
            print('Export fehlgeschlagen:', stem, (r.stdout + r.stderr)[-300:]); sys.exit(1)
        os.replace(out + '.tmp', out); cache[stem] = key; exported += 1
    defs[stem] = {'cls': cls, 'kb': round(os.path.getsize(out) / 1024)}
if os.path.exists(tmp): os.remove(tmp)
json.dump(cache, open(cache_p, 'w'))

IDENT = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0]
insts = []
for cls, path in ins.items():
    stem = os.path.splitext(os.path.basename(path))[0]
    for i in range(1, copies.get(cls, 0) + 2):
        insts.append({'d': stem, 'n': f'{cls}:{i}', 'm': moves.get(f'{cls}:{i}', IDENT)})
built = time.strftime('%Y-%m-%d %H:%M:%S')
for f in os.listdir(HERE):   # Altlast: das fruehere Gesamt-OBJ
    if f.startswith('model') and f.endswith('.obj'): os.remove(os.path.join(HERE, f))
json.dump({'built': built, 'min_diag': MIN_DIAG, 'defs': defs, 'instances': insts}, open(os.path.join(HERE, 'instances.json'), 'w'))
json.dump({'plants': [], 'colors': colors, 'built': built, 'bodies': len(insts)}, open(os.path.join(HERE, 'extras.json'), 'w'))
size = sum(d['kb'] for d in defs.values()) / 1024
print(f'export {time.time()-t0:.0f}s defs={len(defs)} (neu {exported}) = {size:.1f} MB, instanzen={len(insts)}')
