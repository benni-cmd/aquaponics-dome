"""Exportiert designs/dome.sc fuer den 3D-Viewer: je Komponentendefinition EINMAL viewer/defs/<datei>.obj plus viewer/instances.json (Instanz -> Definition + 3x4-Matrix) und viewer/extras.json.

Warum so: Ein Gesamt-OBJ expandiert jede Instanz voll (14 Tische + 4 Tanks + 14 Beete = 320 MB). Definitionen einmal + Matrizen (three.js InstancedMesh) halten den Viewer klein.
Kleinteile (Koerper mit Bounding-Box-Diagonale < MIN_DIAG mm: Schrauben, Kappen, Lochkanten) kommen nicht in die Definition-OBJ; sie treiben die Dreieckszahl (Tesselierung richtet sich nach der Koerpergroesse). Sie stehen in einer eigenen Datei defs/<datei>.klein.obj, die der Viewer erst beim Einschalten von "Kleinteile unter 15 cm zeigen" laedt (W66). Das Modell selbst (dome.sc) bleibt unveraendert.
Definitionen werden zwischengespeichert (viewer/defs/.cache.json: Aenderungszeit der .sc + MIN_DIAG + FORMAT).
Aufruf: python viewer/export_model.py [--variante ring_b2]   (liest scripts/dome-script.json fuer Einbau und Matrizen, designs/components/*.sc fuer die Geometrie)
"""
import json, math, os, re, subprocess, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
CLI = r'C:\Program Files\SolidCraft\solidcraft-cli.exe'
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
import variante as V   # N-VARIANTEN V1a: --variante <v> / KREISLAUF_VARIANTE, Standard a_plus (= heutige Pfade)
VAR = V.aktiv()
SCRIPT = V.pfad('dome_script', VAR, root=ROOT)
OUT_DIR = V.pfad('viewer_dir', VAR, root=ROOT)   # a_plus: viewer/, ring_b2: viewer/varianten/ring_b2/ (defs/ und detail/ bleiben gemeinsam)
DEFS = os.path.join(HERE, 'defs')
MIN_DIAG = 150   # mm
FORMAT = 'v3'    # Cache-Schluessel: v2 = Kleinteile in <stem>.klein.obj statt verworfen, v3 = Anschlussteile bleiben im Hauptexport
ANSCHLUSS = [re.compile(m, re.I) for m in json.load(open(os.path.join(HERE, 'anschluesse.json'), encoding='utf-8'))['muster']] if os.path.exists(os.path.join(HERE, 'anschluesse.json')) else []
ANSCHLUSS_ID = '%08x' % (sum(ord(c) * (i + 1) for i, c in enumerate('|'.join(a.pattern for a in ANSCHLUSS))) & 0xffffffff)   # aendert sich mit der Liste
ist_anschluss = lambda name: any(a.search(name) for a in ANSCHLUSS)
KEEP_ALL = ('netztopf', 'salatkopf')   # Pflanzenteile sind klein, aber als Instanzen billig: alle Koerper behalten
fw = lambda p: os.path.abspath(p).replace(chr(92), '/')

def json_atomar(obj, pfad):   # Temp-Datei, dann umbenennen: der Browser sieht nie eine halb geschriebene JSON
    with open(pfad + '.tmp', 'w', encoding='utf-8') as f: json.dump(obj, f)
    os.replace(pfad + '.tmp', pfad)

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
    md = 0 if stem in KEEP_ALL else MIN_DIAG; key = f'{os.path.getmtime(path)}|{md}|{FORMAT}|{ANSCHLUSS_ID}'; out = os.path.join(DEFS, stem + '.obj'); out_k = os.path.join(DEFS, stem + '.klein.obj')
    if cache.get(stem) != key or not os.path.exists(out):
        json.dump({'commands': [{'command': 'doc.open', 'params': {'path': fw(path), 'read_only': True}}]}, open(tmp, 'w'))
        o = os.path.join(DEFS, '_ev.json')
        subprocess.run([CLI, 'eval', fw(path), '--json-out', o], capture_output=True)
        bodies = find(json.load(open(o, encoding='utf-8')), 'bodies') or []; os.remove(o)
        gross = lambda b: math.dist(b['bbox']['min'], b['bbox']['max']) >= md or ist_anschluss(b['name'])   # Anschlussteile immer im Hauptexport
        keep = [b['name'] for b in bodies if gross(b)]
        klein = [b['name'] for b in bodies if not gross(b)]

        def schreibe(namen, ziel):   # leere Liste: leere Datei (sonst exportiert die CLI womoeglich alle Koerper)
            if not namen:
                open(ziel, 'w').close(); return
            json.dump({'commands': [{'command': 'doc.open', 'params': {'path': fw(path), 'read_only': True}},
                                    {'command': 'file.export', 'params': {'path': fw(ziel), 'format': 'obj', 'bodies': namen}}]}, open(tmp, 'w'))
            r = subprocess.run([CLI, 'run', tmp, '--quiet'], capture_output=True, text=True)
            if r.returncode or not os.path.exists(ziel):
                print('Export fehlgeschlagen:', stem, (r.stdout + r.stderr)[-300:]); sys.exit(1)
        schreibe(keep, out + '.tmp'); os.replace(out + '.tmp', out)
        if klein:
            schreibe(klein, out_k + '.tmp'); os.replace(out_k + '.tmp', out_k)
        elif os.path.exists(out_k): os.remove(out_k)
        cache[stem] = key; exported += 1
    defs[stem] = {'cls': cls, 'kb': round(os.path.getsize(out) / 1024), 'klein_kb': round(os.path.getsize(out_k) / 1024) if os.path.exists(out_k) else 0}
if os.path.exists(tmp): os.remove(tmp)
json_atomar(cache, cache_p)

IDENT = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0]
insts = []
for cls, path in ins.items():
    stem = os.path.splitext(os.path.basename(path))[0]
    for i in range(1, copies.get(cls, 0) + 2):
        insts.append({'d': stem, 'n': f'{cls}:{i}', 'm': moves.get(f'{cls}:{i}', IDENT)})
built = time.strftime('%Y-%m-%d %H:%M:%S')
for f in os.listdir(HERE):   # Altlast: das fruehere Gesamt-OBJ
    if f.startswith('model') and f.endswith('.obj'): os.remove(os.path.join(HERE, f))
try: walk_z = json.load(open(os.path.join(ROOT, 'data', 'params.json'), encoding='utf-8'))['sock_h']['value']   # begehbarer Boden fuer den FPV-Modus
except Exception: walk_z = 400
os.makedirs(OUT_DIR, exist_ok=True)
json_atomar({'plants': [], 'colors': colors, 'built': built, 'bodies': len(insts)}, os.path.join(OUT_DIR, 'extras.json'))
json_atomar({'built': built, 'min_diag': MIN_DIAG, 'anschluss_immer_sichtbar': True, 'walk_z': walk_z, 'defs': defs, 'instances': insts}, os.path.join(OUT_DIR, 'instances.json'))   # zuletzt: erst jetzt zeigt das Modellverzeichnis auf den neuen Stand
subprocess.run([sys.executable, '-I', os.path.join(HERE, 'export_ansicht.py'), '--variante', VAR], capture_output=True, text=True)   # Nebendatei Werkstoff/Gruppe/Leitungsart passend zu diesem Export
size = sum(d['kb'] for d in defs.values()) / 1024; size_k = sum(d['klein_kb'] for d in defs.values()) / 1024
print(f'export {time.time()-t0:.0f}s defs={len(defs)} (neu {exported}) = {size:.1f} MB + Kleinteile {size_k:.1f} MB, instanzen={len(insts)}')
